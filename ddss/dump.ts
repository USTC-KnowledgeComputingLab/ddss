import { unparse } from "atsds-bnf";
import { initializeDatabase, Fact, Idea } from "./orm.js";
import type { Sequelize } from "sequelize";

export async function main(addr: string, sequelize?: Sequelize) {
    if (!sequelize) {
        sequelize = await initializeDatabase(addr);
    }

    try {
        const ideas = await Idea.findAll();
        for (const idea of ideas) {
            console.log("idea:", unparse(idea.data));
        }

        const facts = await Fact.findAll();
        for (const fact of facts) {
            console.log("fact:", unparse(fact.data));
        }
    } finally {
        // Session is handled by main or caller
    }
}
