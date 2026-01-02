import { jest, describe, it, expect, beforeEach, afterEach } from "@jest/globals";
import { main } from "../ddss/egg.ts";
import { Fact, Idea } from "../ddss/orm.ts";
import { createTempDb } from "./utils.ts";

describe("egg", () => {
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

    it("test_egg_symmetry_ab_to_ba", async () => {
        await Fact.create({ data: "----\n(binary == a b)\n" });
        await Idea.create({ data: "----\n(binary == b a)\n" });

        await runMain(sequelize);

        const facts = await Fact.findAll();
        const factData = facts.map((f) => f.data);
        expect(factData).toContain("----\n(binary == b a)\n");
    });

    it("test_egg_transitivity_abc", async () => {
        await Fact.bulkCreate([{ data: "----\n(binary == a b)\n" }, { data: "----\n(binary == b c)\n" }]);
        await Idea.create({ data: "----\n(binary == a c)\n" });

        await runMain(sequelize);

        const facts = await Fact.findAll();
        const factData = facts.map((f) => f.data);
        expect(factData).toContain("----\n(binary == a c)\n");
    });

    it("test_egg_congruence_fx_fy", async () => {
        await Fact.create({ data: "----\n(binary == x y)\n" });
        await Idea.create({ data: "----\n(binary == (unary f x) (unary f y))\n" });

        await runMain(sequelize);

        const facts = await Fact.findAll();
        const factData = facts.map((f) => f.data);
        expect(factData).toContain("----\n(binary == (unary f x) (unary f y))\n");
    });

    it("test_egg_substitution_fx_with_xy", async () => {
        await Fact.bulkCreate([{ data: "----\n(unary f x)\n" }, { data: "----\n(binary == x y)\n" }]);
        await Idea.create({ data: "----\n(unary f y)\n" });

        await runMain(sequelize);

        const facts = await Fact.findAll();
        const factData = facts.map((f) => f.data);
        expect(factData).toContain("----\n(unary f y)\n");
    });

    it("test_egg_complex_situation", async () => {
        await Fact.bulkCreate([
            { data: "----\n(binary == a b)\n" },
            { data: "----\n(binary == b c)\n" },
            { data: "----\n(unary f a)\n" },
        ]);
        await Idea.bulkCreate([
            { data: "----\n(binary == b a)\n" },
            { data: "----\n(binary == a c)\n" },
            { data: "----\n(binary == (unary f b) (unary f c))\n" },
            { data: "----\n(unary f c)\n" },
        ]);

        await runMain(sequelize, 5);

        const facts = await Fact.findAll();
        const factData = facts.map((f) => f.data);
        expect(factData).toContain("----\n(binary == b a)\n");
        expect(factData).toContain("----\n(binary == a c)\n");
        expect(factData).toContain("----\n(binary == (unary f b) (unary f c))\n");
        expect(factData).toContain("----\n(unary f c)\n");
    });

    // Variable based tests
    it("test_egg_symmetry_with_variables", async () => {
        await Fact.create({ data: "----\n(binary == (unary a `x) (unary b `x))\n" });
        await Idea.create({ data: "----\n(binary == (unary b t) (unary a t))\n" });

        await runMain(sequelize);

        const facts = await Fact.findAll();
        const factData = facts.map((f) => f.data);
        expect(factData).toContain("----\n(binary == (unary b t) (unary a t))\n");
    });

    it("test_egg_transitivity_with_variables", async () => {
        await Fact.bulkCreate([
            { data: "----\n(binary == (unary a `x) (unary b `x))\n" },
            { data: "----\n(binary == (unary b `x) (unary c `x))\n" },
        ]);
        await Idea.create({ data: "----\n(binary == (unary a t) (unary c t))\n" });

        await runMain(sequelize);

        const facts = await Fact.findAll();
        const factData = facts.map((f) => f.data);
        expect(factData).toContain("----\n(binary == (unary a t) (unary c t))\n");
    });
});
