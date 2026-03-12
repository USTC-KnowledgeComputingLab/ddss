import { jest, describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { main } from "../ddss/chain.ts";
import { Fact, Idea } from "../ddss/orm.ts";
import { createTempDb } from "./utils.ts";

describe("chain", () => {
    let sequelize: any;
    let cleanup: any;
    let addr: string;

    beforeEach(async () => {
        const db = await createTempDb();
        sequelize = db.sequelize;
        cleanup = db.cleanup;
        addr = db.addr;
    });

    afterEach(async () => {
        await cleanup();
        jest.restoreAllMocks();
    });

    const runMain = async (sequelize: any, maxIterations: number = 3) => {
        let calls = 0;
        // We need to spy on Fact.findAll because it's the driver of the loop
        // We can't easily access the original method if we overwrite it with spy unless we save it.

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
            console.error("Unexpected error in runMain:", e);
            throw e;
        } finally {
            spy.mockRestore();
        }
    };

    it("test_chain_simple_modus_ponens", async () => {
        // Add initial facts: a => b and => a
        await Fact.bulkCreate([{ data: "a\n----\nb\n" }, { data: "----\na\n" }]);

        await runMain(sequelize);

        const facts = await Fact.findAll();
        const factsData = facts.map((f) => f.data);
        expect(factsData).toContain("----\nb\n");
    });

    it("test_chain_multi_premise", async () => {
        // Add initial facts: a, b => c and => a and => b
        await Fact.bulkCreate([{ data: "a\nb\n----\nc\n" }, { data: "----\na\n" }, { data: "----\nb\n" }]);

        await runMain(sequelize);

        const facts = await Fact.findAll();
        const factsData = facts.map((f) => f.data);
        expect(factsData).toContain("----\nc\n");
    });

    it("test_chain_no_inference_without_matching_facts", async () => {
        // Add facts that don't match: a => b and => c
        await Fact.bulkCreate([{ data: "a\n----\nb\n" }, { data: "----\nc\n" }]);

        await runMain(sequelize);

        const facts = await Fact.findAll();
        const factsData = facts.map((f) => f.data);

        expect(factsData).toHaveLength(2);
        expect(factsData).toContain("a\n----\nb\n");
        expect(factsData).toContain("----\nc\n");
    });

    it("test_chain_multiple_inferences", async () => {
        // Add facts for chained inference: a => b, b => c, => a
        await Fact.bulkCreate([{ data: "a\n----\nb\n" }, { data: "b\n----\nc\n" }, { data: "----\na\n" }]);

        await runMain(sequelize, 5);

        const facts = await Fact.findAll();
        const factsData = facts.map((f) => f.data);

        expect(factsData).toContain("----\nb\n");
        expect(factsData).toContain("----\nc\n");
    });

    it("test_chain_duplicate_facts_not_added", async () => {
        // Add facts that will produce a duplicate: a => c and b => c, with => a and => b
        // Both derive => c, but only one should be added.

        await Fact.bulkCreate([
            { data: "a\n----\nc\n" },
            { data: "b\n----\nc\n" },
            { data: "----\na\n" },
            { data: "----\nb\n" },
        ]);

        await runMain(sequelize, 5);

        const facts = await Fact.findAll();
        const factsData = facts.map((f) => f.data);

        expect(facts.length).toBe(5); // 4 original + 1 inferred
        const cCount = factsData.filter((d) => d === "----\nc\n").length;
        expect(cCount).toBe(1);
    });
});
