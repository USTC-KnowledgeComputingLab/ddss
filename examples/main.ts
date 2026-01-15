import * as fs from "node:fs";
import * as path from "node:path";
import * as os from "node:os";
import { Op, type Sequelize } from "sequelize";
import { Rule, List, Variable, type Term, Item } from "atsds";
import { parse, unparse } from "atsds-bnf";
import { Fact, Idea, initializeDatabase, insertOrIgnore } from "../ddss/orm.ts";
import { main as ds } from "../ddss/ds.ts";
import { main as egg } from "../ddss/egg.ts";
import { strRuleGetStrIdea } from "../ddss/utility.ts";

function extractBinaryFromTerm(term: Term): [Item, Term, Term] | null {
    const t = term.term();
    if (t instanceof List && t.length() === 4 && t.getitem(0).toString() === "binary") {
        const opTerm = t.getitem(1).term();
        if (opTerm instanceof Item) {
            return [opTerm, t.getitem(2), t.getitem(3)];
        }
    }
    return null;
}

function extractEqualityFromRule(rule: Rule): [Term, Term] | null {
    if (rule.length() !== 0) {
        return null;
    }
    const res = extractBinaryFromTerm(rule.conclusion());
    if (res && res[0].toString() === "==") {
        return [res[1], res[2]];
    }
    return null;
}

function extractLiteralFromTerm(term: Term): [Item | Variable, Item] | null {
    const res = extractBinaryFromTerm(term);
    if (res && res[0].toString() === "::") {
        const lhs = res[1].term();
        const rhs = res[2].term();
        if (lhs instanceof List && rhs instanceof Item) {
            if (
                lhs.length() === 3 &&
                lhs.getitem(0).toString() === "function" &&
                lhs.getitem(1).toString() === "Literal"
            ) {
                const val = lhs.getitem(2).term();
                if (val instanceof Item || val instanceof Variable) {
                    return [val, rhs];
                }
            }
        }
    }
    return null;
}

async function arithmetic() {
    const ops: Record<string, (a: number, b: number) => number | null> = {
        "+": (a, b) => a + b,
        "-": (a, b) => a - b,
        "*": (a, b) => a * b,
        "/": (a, b) => (b !== 0 ? a / b : null),
    };

    const typesMap: Record<string, (v: string) => number> = {
        Int: (v) => Number.parseInt(v, 10),
        Float: (v) => Number.parseFloat(v),
    };

    let maxIdea = -1;

    while (true) {
        const newIdeas = await Idea.findAll({
            where: { id: { [Op.gt]: maxIdea } },
        });

        for (const idea of newIdeas) {
            maxIdea = Math.max(maxIdea, idea.id);
            const rule = new Rule(idea.data);
            const eq = extractEqualityFromRule(rule);
            if (!eq) continue;

            const [lhsTerm, rhsTerm] = eq;
            const sides: Array<["lhs" | "rhs", Term, Term]> = [
                ["lhs", lhsTerm, rhsTerm],
                ["rhs", rhsTerm, lhsTerm],
            ];

            for (const [label, binExpr, valExpr] of sides) {
                const binRes = extractBinaryFromTerm(binExpr);
                if (binRes) {
                    const opStr = binRes[0].toString();
                    const func = ops[opStr];
                    if (func) {
                        const v1Lit = extractLiteralFromTerm(binRes[1]);
                        const v2Lit = extractLiteralFromTerm(binRes[2]);
                        const vResLit = extractLiteralFromTerm(valExpr);

                        if (v1Lit && v2Lit && vResLit) {
                            const [val1, type1] = v1Lit;
                            const [val2, type2] = v2Lit;
                            const [valRes, typeRes] = vResLit;

                            const val1Str = val1.toString();
                            const val2Str = val2.toString();
                            const typeStr = typeRes.toString();

                            if (
                                val1 instanceof Item &&
                                val2 instanceof Item &&
                                valRes instanceof Variable &&
                                type1.toString() === type2.toString() &&
                                type1.toString() === typeRes.toString()
                            ) {
                                const conv = typesMap[typeStr];
                                if (conv) {
                                    const a = conv(val1Str);
                                    const b = conv(val2Str);
                                    const res = func(a, b);

                                    if (res !== null) {
                                        const v1Str = `(binary :: (function Literal ${val1Str}) ${typeStr})`;
                                        const v2Str = `(binary :: (function Literal ${val2Str}) ${typeStr})`;
                                        const resStr = `(binary :: (function Literal ${res}) ${typeStr})`;

                                        let factStr: string;
                                        if (label === "lhs") {
                                            factStr = `(binary == (binary ${opStr} ${v1Str} ${v2Str}) ${resStr})`;
                                        } else {
                                            factStr = `(binary == ${resStr} (binary ${opStr} ${v1Str} ${v2Str}))`;
                                        }

                                        await insertOrIgnore(Fact, new Rule(factStr).toString());
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        await new Promise((resolve) => setTimeout(resolve, 0));
    }
}

async function output(abortController: AbortController) {
    let maxFact = -1;
    let maxIdea = -1;

    while (true) {
        const newIdeas = await Idea.findAll({
            where: { id: { [Op.gt]: maxIdea } },
        });
        for (const idea of newIdeas) {
            maxIdea = Math.max(maxIdea, idea.id);
            console.log("idea:", unparse(idea.data));
        }

        const newFacts = await Fact.findAll({
            where: { id: { [Op.gt]: maxFact } },
        });
        for (const fact of newFacts) {
            maxFact = Math.max(maxFact, fact.id);
            console.log("fact:", unparse(fact.data));

            const rule = new Rule(fact.data);
            if (rule.length() === 0) {
                const term = rule.conclusion().term();
                if (
                    term instanceof List &&
                    term.length() >= 2 &&
                    term.getitem(0).toString() === "function" &&
                    term.getitem(1).toString() === "Query"
                ) {
                    console.log("status:", unparse(fact.data));
                    abortController.abort();
                    return;
                }
            }
        }

        await new Promise((resolve) => setTimeout(resolve, 0));
    }
}

async function load(fileName: string) {
    const content = fs.readFileSync(fileName, "utf-8");
    const lines = content.split("\n");

    for (const line of lines) {
        const data = line.trim();
        if (data === "" || data.startsWith("//")) continue;

        try {
            const dsStr = parse(data);
            await insertOrIgnore(Fact, dsStr);
            const idea = strRuleGetStrIdea(dsStr);
            if (idea) {
                await insertOrIgnore(Idea, idea);
            }
        } catch (e) {
            console.error(`error: ${(e as Error).message}`);
        }
    }
}

async function run(addr: string, fileName: string) {
    const sequelize = await initializeDatabase(addr);
    const abortController = new AbortController();

    try {
        await load(fileName);
        await Promise.race([
            ds(sequelize),
            egg(sequelize),
            output(abortController),
            arithmetic(),
            new Promise((_, reject) => {
                abortController.signal.addEventListener("abort", () => reject(new Error("Abort")));
            }),
        ]).catch((e) => {
            if (e.message !== "Abort") throw e;
        });
    } finally {
        await sequelize.close();
    }
}

function main() {
    const fileName = process.argv[2];
    if (!fileName) {
        console.error("Please provide a dsp file");
        process.exit(1);
    }
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "ddss-"));
    const dbPath = path.join(tmpDir, "ddss.sqlite");
    const addr = `sqlite://${dbPath}`;

    run(addr, fileName).catch(console.error);
}

main();
