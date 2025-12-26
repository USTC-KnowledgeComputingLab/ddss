import { jest, describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { main } from "../ddss/ds.ts";
import { Fact, Idea } from "../ddss/orm.ts";
import { createTempDb } from "./utils.ts";

describe("ds", () => {
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

    const runMain = async (addr: string, sequelize: any, maxIterations: number = 3) => {
        let calls = 0;
        // We need to spy on Fact.findAll because it's the driver of the loop
        // However, Fact.findAll is called in every iteration.
        // We can't easily access the original method if we overwrite it with spy unless we save it.
        // Note: jest.spyOn(Fact, 'findAll') preserves the original implementation by default?
        // No, we want to call original implementation N times, then throw.

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
            await main(addr, sequelize);
        } catch (e: any) {
            if (e.message === "ForceStop") return;
            console.error("Unexpected error in runMain:", e);
            throw e;
        } finally {
            spy.mockRestore();
        }
    };

    it("test_ds_simple_modus_ponens", async () => {
        // Add initial facts: a => b and => a
        await Fact.bulkCreate([{ data: "a\n----\nb\n" }, { data: "----\na\n" }]);

        await runMain(addr, sequelize);

        const facts = await Fact.findAll();
        const factsData = facts.map((f) => f.data);
        expect(factsData).toContain("----\nb\n");
    });

    it("test_ds_multi_premise_with_idea", async () => {
        // Add initial facts: a, b => c and => a
        await Fact.bulkCreate([{ data: "a\nb\n----\nc\n" }, { data: "----\na\n" }]);

        await runMain(addr, sequelize);

        const facts = await Fact.findAll();
        const factsData = facts.map((f) => f.data);
        expect(factsData).toContain("b\n----\nc\n");

        const ideas = await Idea.findAll();
        const ideasData = ideas.map((i) => i.data);
        expect(ideasData).toContain("----\nb\n");
    });

    it("test_ds_no_inference_without_matching_facts", async () => {
        // Add facts that don't match: a => b and => c
        await Fact.bulkCreate([{ data: "a\n----\nb\n" }, { data: "----\nc\n" }]);

        await runMain(addr, sequelize);

        const facts = await Fact.findAll();
        const factsData = facts.map((f) => f.data);

        expect(factsData).toHaveLength(2);
        expect(factsData).toContain("a\n----\nb\n");
        expect(factsData).toContain("----\nc\n");
    });

    it("test_ds_multiple_inferences", async () => {
        // Add facts for chained inference: a => b, b => c, => a
        await Fact.bulkCreate([{ data: "a\n----\nb\n" }, { data: "b\n----\nc\n" }, { data: "----\na\n" }]);

        // Needs more iterations
        await runMain(addr, sequelize, 5);

        const facts = await Fact.findAll();
        const factsData = facts.map((f) => f.data);

        expect(factsData).toContain("----\nb\n");
        expect(factsData).toContain("----\nc\n");
    });

    it("test_ds_duplicate_facts_not_added", async () => {
        // Add facts that will produce a duplicate: a => b twice with => a
        // "a\n----\nc\n" and "b\n----\nc\n" (Wait, python test says a=>b twice?
        // No, Python test says:
        // sess.add(Facts(data="a\n----\nc\n"))
        // sess.add(Facts(data="b\n----\nc\n"))
        // sess.add(Facts(data="----\na\n"))
        // sess.add(Facts(data="----\nb\n"))
        // So a=>c and b=>c, with =>a and =>b. Both derive =>c.

        await Fact.bulkCreate([
            { data: "a\n----\nc\n" },
            { data: "b\n----\nc\n" },
            { data: "----\na\n" },
            { data: "----\nb\n" },
        ]);

        await runMain(addr, sequelize, 5);

        const facts = await Fact.findAll();
        const factsData = facts.map((f) => f.data);

        expect(facts.length).toBe(5); // 4 original + 1 inferred
        const cCount = factsData.filter((d) => d === "----\nc\n").length;
        expect(cCount).toBe(1);
    });
});
