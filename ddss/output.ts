import { Op, type Sequelize } from "sequelize";
import { unparse } from "atsds-bnf";
import { Fact, Idea, initializeDatabase } from "./orm.ts";

export async function main(addr: string, sequelize?: Sequelize) {
    if (!sequelize) {
        sequelize = await initializeDatabase(addr);
    }

    let maxFact = -1;
    let maxIdea = -1;

    while (true) {
        let count = 0;

        const newIdeas = await Idea.findAll({
            where: { id: { [Op.gt]: maxIdea } },
        });
        for (const idea of newIdeas) {
            maxIdea = Math.max(maxIdea, idea.id);
            console.log("idea:", unparse(idea.data));
            count++;
        }

        const newFacts = await Fact.findAll({
            where: { id: { [Op.gt]: maxFact } },
        });
        for (const fact of newFacts) {
            maxFact = Math.max(maxFact, fact.id);
            console.log("fact:", unparse(fact.data));
            count++;
        }

        if (count === 0) {
            await new Promise((resolve) => setTimeout(resolve, 0));
        }
    }
}
