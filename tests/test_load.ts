import { jest, describe, it, expect, beforeEach, afterEach } from "@jest/globals";

// Mock readline
const mockCreateInterface = jest.fn();
jest.unstable_mockModule("node:readline/promises", () => ({
    createInterface: mockCreateInterface,
}));

const { main } = await import("../ddss/load.ts");
const { Fact, Idea } = await import("../ddss/orm.ts");
const { createTempDb } = await import("./utils.ts");

describe("load", () => {
    let sequelize: any;
    let cleanup: any;
    let addr: string;
    let mockRl: any;

    beforeEach(async () => {
        const db = await createTempDb();
        sequelize = db.sequelize;
        cleanup = db.cleanup;
        addr = db.addr;

        mockRl = {
            [Symbol.asyncIterator]: jest.fn(),
            close: jest.fn(),
        };
        mockCreateInterface.mockReturnValue(mockRl);
    });

    afterEach(async () => {
        await cleanup();
        jest.restoreAllMocks();
    });

    const setInput = (lines: string[]) => {
        mockRl[Symbol.asyncIterator].mockImplementation(async function* () {
            for (const line of lines) {
                yield line;
            }
        });
    };

    it("test_load_valid_fact", async () => {
        setInput(["a => b"]);
        await main(sequelize);

        const facts = await Fact.findAll();
        expect(facts.map((f: any) => f.data)).toContain("a\n----\nb\n");
    });

    it("test_load_generates_idea", async () => {
        setInput(["a => b"]);
        await main(sequelize);

        const ideas = await Idea.findAll();
        expect(ideas.map((i: any) => i.data)).toContain("----\na\n");
    });

    it("test_load_multiple_entries", async () => {
        setInput(["a => b", "c => d", "simple"]);
        await main(sequelize);

        const facts = await Fact.findAll();
        const factData = facts.map((f: any) => f.data);
        expect(factData).toContain("a\n----\nb\n");
        expect(factData).toContain("c\n----\nd\n");
        expect(factData).toContain("----\nsimple\n");
    });
});
