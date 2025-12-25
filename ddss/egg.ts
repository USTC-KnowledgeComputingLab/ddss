import { Rule } from "atsds";
import { Search } from "./egraph.js";
import { initializeDatabase, insertOrIgnore, Fact, Idea } from "./orm.js";
import { type Sequelize, Op } from "sequelize";

export async function main(addr: string, sequelize?: Sequelize) {
    if (!sequelize) {
        sequelize = await initializeDatabase(addr);
    }

    try {
        const search = new Search();
        let pool: Rule[] = [];
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
                pool.push(new Rule(idea.data));
            }

            const newFacts = await Fact.findAll({
                where: { id: { [Op.gt]: maxFact } },
                order: [["id", "ASC"]],
            });
            for (const fact of newFacts) {
                maxFact = Math.max(maxFact, fact.id);
                search.add(new Rule(fact.data));
            }

            search.rebuild();
            const tasks: Promise<void>[] = [];
            const nextPool: Rule[] = [];

            for (const i of pool) {
                let found = false;
                for (const o of search.execute(i)) {
                    tasks.push(insertOrIgnore(Fact, o.toString()));
                    count++;
                    if (i.toString() === o.toString()) {
                        found = true;
                        break;
                    }
                }
                if (!found) {
                    nextPool.push(i);
                }
            }
            pool = nextPool;
            await Promise.all(tasks);

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
