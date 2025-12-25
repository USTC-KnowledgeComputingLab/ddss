import * as readline from "node:readline";
import { parse } from "atsds-bnf";
import { initializeDatabase, insertOrIgnore, Fact, Idea } from "./orm.js";
import { strRuleGetStrIdea } from "./utility.js";
import type { Sequelize } from "sequelize";

export async function main(addr: string, sequelize?: Sequelize) {
    if (!sequelize) {
        sequelize = await initializeDatabase(addr);
    }

    const rl = readline.createInterface({
        input: process.stdin,
        terminal: false,
    });

    try {
        for await (const line of rl) {
            const data = line.trim();
            if (data === "" || data.startsWith("//")) {
                continue;
            }

            try {
                const ds = parse(data);
                const dsStr = ds.toString();
                await insertOrIgnore(Fact, dsStr);
                const idea = strRuleGetStrIdea(dsStr);
                if (idea) {
                    await insertOrIgnore(Idea, idea);
                }
            } catch (e) {
                console.error(`error: ${e}`);
            }
        }
    } finally {
        rl.close();
    }
}
