import { jest, describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { main } from "../ddss/output.ts";
import { Fact, Idea } from "../ddss/orm.ts";
import { createTempDb } from "./utils.ts";

describe("output", () => {
    let sequelize: any;
    let cleanup: any;
    let addr: string;
    let logSpy: any;

    beforeEach(async () => {
        const db = await createTempDb();
        sequelize = db.sequelize;
        cleanup = db.cleanup;
        addr = db.addr;
        logSpy = jest.spyOn(console, "log").mockImplementation(() => {});
    });

    afterEach(async () => {
        await cleanup();
        jest.restoreAllMocks();
    });

    const getCapturedOutput = () => {
        return logSpy.mock.calls.map((args: any[]) => args.join(" ")).join("\n");
    };

    const runMain = async (sequelize: any, maxIterations: number = 3) => {
        let calls = 0;
        const originalFindAll = Fact.findAll;
        const spy = jest.spyOn(Fact, "findAll");

        spy.mockImplementation(async (options: any) => {
            calls++;
            const result = await originalFindAll.call(Fact, options);

            if (calls > maxIterations) {
                throw new Error("ForceStop");
            }
            return result;
        });

        try {
            await main(sequelize);
        } catch (e: any) {
            if (e.message === "ForceStop") return;
            throw e;
        } finally {
            spy.mockRestore();
        }
    };

    it("test_output_formats_facts_correctly", async () => {
        await Fact.create({ data: "a\n----\nb\n" });
        await runMain(sequelize);
        expect(getCapturedOutput()).toContain("fact: a => b");
    });

    it("test_output_formats_ideas_correctly", async () => {
        await Idea.create({ data: "x\n----\ny\n" });
        await runMain(sequelize);
        expect(getCapturedOutput()).toContain("idea: x => y");
    });

    it("test_output_multiple_entries", async () => {
        await Fact.create({ data: "a\n----\nb\n" });
        await Fact.create({ data: "c\n----\nd\n" });
        await Idea.create({ data: "x\n----\ny\n" });
        await Idea.create({ data: "p\n----\nq\n" });

        await runMain(sequelize);

        const output = getCapturedOutput();
        expect(output).toContain("idea: x => y");
        expect(output).toContain("idea: p => q");
        expect(output).toContain("fact: a => b");
        expect(output).toContain("fact: c => d");
    });
});
