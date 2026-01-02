import { Op, type Sequelize } from "sequelize";
import { unparse } from "atsds-bnf";
import { Fact, Idea, initializeDatabase } from "./orm.ts";

export async function main(sequelize: Sequelize) {
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
        }

        await new Promise((resolve) => setTimeout(resolve, 0));
    }
}
