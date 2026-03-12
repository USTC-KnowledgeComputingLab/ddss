import type { Sequelize } from "sequelize";
import { unparse } from "atsds-bnf";
import { Fact, Idea } from "./orm.ts";

export async function main(sequelize: Sequelize): Promise<void> {
    const ideas = await Idea.findAll();
    for (const idea of ideas) {
        console.log("idea:", unparse(idea.data));
    }

    const facts = await Fact.findAll();
    for (const fact of facts) {
        console.log("fact:", unparse(fact.data));
    }
}
