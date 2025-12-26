import { jest, describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { main } from "../ddss/dump.ts";
import { Fact, Idea } from "../ddss/orm.ts";
import { createTempDb } from "./utils.ts";

describe("dump", () => {
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
        logSpy.mockRestore();
        jest.restoreAllMocks();
    });

    const getCapturedOutput = () => {
        return logSpy.mock.calls.map((args: any[]) => args.join(" ")).join("\n");
    };

    it("test_dump_facts_correctly", async () => {
        await Fact.create({ data: "a\n----\nb\n" });
        await main(addr, sequelize);
        expect(getCapturedOutput()).toContain("fact: a => b");
    });

    it("test_dump_ideas_correctly", async () => {
        await Idea.create({ data: "x\n----\ny\n" });
        await main(addr, sequelize);
        expect(getCapturedOutput()).toContain("idea: x => y");
    });

    it("test_dump_multiple_entries", async () => {
        await Fact.create({ data: "a\n----\nb\n" });
        await Fact.create({ data: "c\n----\nd\n" });
        await Idea.create({ data: "x\n----\ny\n" });
        await Idea.create({ data: "p\n----\nq\n" });

        await main(addr, sequelize);

        const output = getCapturedOutput();
        expect(output).toContain("idea: x => y");
        expect(output).toContain("idea: p => q");
        expect(output).toContain("fact: a => b");
        expect(output).toContain("fact: c => d");
    });

    it("test_dump_empty_database", async () => {
        await main(addr, sequelize);
        expect(getCapturedOutput().trim()).toBe("");
    });

    it("test_dump_order", async () => {
        await Fact.create({ data: "a\n----\nb\n" });
        await Idea.create({ data: "x\n----\ny\n" });

        await main(addr, sequelize);

        const output = getCapturedOutput();
        const ideaPos = output.indexOf("idea: x => y");
        const factPos = output.indexOf("fact: a => b");

        expect(ideaPos).toBeGreaterThan(-1);
        expect(factPos).toBeGreaterThan(-1);
        expect(ideaPos).toBeLessThan(factPos);
    });

    it("test_dump_with_simple_fact", async () => {
        await Fact.create({ data: "----\nsimple\n" });
        await main(addr, sequelize);
        expect(getCapturedOutput()).toContain("fact:  => simple");
    });
});
