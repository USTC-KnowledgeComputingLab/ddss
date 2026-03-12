import { Op, type Sequelize } from "sequelize";
import { Chain } from "atsds";
import type { Rule } from "atsds";
import { Fact, Idea, insertOrIgnore } from "./orm.ts";
import { strRuleGetStrIdea } from "./utility.ts";

export async function main(sequelize: Sequelize): Promise<void> {
    const chain = new Chain();
    let maxFact = -1;

    while (true) {
        const newFacts = await Fact.findAll({
            where: { id: { [Op.gt]: maxFact } },
        });

        for (const fact of newFacts) {
            maxFact = Math.max(maxFact, fact.id);
            chain.add(fact.data);
        }

        const tasks: Promise<void>[] = [];

        const handler = (rule: Rule) => {
            const ds = rule.toString();
            tasks.push(insertOrIgnore(Fact, ds));
            const idea = strRuleGetStrIdea(ds);
            if (idea) {
                tasks.push(insertOrIgnore(Idea, idea));
            }
            return false;
        };

        chain.execute(handler);
        await Promise.all(tasks);

        await new Promise((resolve) => setTimeout(resolve, 0));
    }
}
