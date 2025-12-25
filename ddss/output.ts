import { unparse } from "atsds-bnf";
import { initializeDatabase, Fact, Idea } from "./orm.js";
import { type Sequelize, Op } from "sequelize";

export async function main(addr: string, sequelize?: Sequelize) {
    if (!sequelize) {
        sequelize = await initializeDatabase(addr);
    }

    try {
        let maxFact = -1;
        let maxIdea = -1;

        while (true) {
            const begin = Date.now();
            let count = 0;

            const newIdeas = await Idea.findAll({
                where: { id: { [Op.gt]: maxIdea } },
                order: [["id", "ASC"]],
            });
            for (const idea of newIdeas) {
                maxIdea = Math.max(maxIdea, idea.id);
                console.log("idea:", unparse(idea.data));
                count++;
            }

            const newFacts = await Fact.findAll({
                where: { id: { [Op.gt]: maxFact } },
                order: [["id", "ASC"]],
            });
            for (const fact of newFacts) {
                maxFact = Math.max(maxFact, fact.id);
                console.log("fact:", unparse(fact.data));
                count++;
            }

            const end = Date.now();
            const duration = (end - begin) / 1000;
            if (count === 0) {
                const delay = Math.max(0, 0.1 - duration);
                await new Promise((resolve) => setTimeout(resolve, delay * 1000));
            }
        }
    } catch (err) {
        // Handle error
    }
}
