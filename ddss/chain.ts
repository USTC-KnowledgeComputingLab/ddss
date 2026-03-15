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

        for (const rule of chain) {
            const ds = rule.toString();
            const idea = strRuleGetStrIdea(ds);
            if (idea) {
                await insertOrIgnore(Idea, idea);
            } else {
                await insertOrIgnore(Fact, ds);
            }
        }

        await new Promise((resolve) => setTimeout(resolve, 0));
    }
}
