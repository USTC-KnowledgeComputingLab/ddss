import * as readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { parse } from "atsds-bnf";
import { initializeDatabase, insertOrIgnore, Fact, Idea } from "./orm.js";
import { strRuleGetStrIdea, patchStdout } from "./utility.js";
import type { Sequelize } from "sequelize";

export async function main(addr: string, sequelize?: Sequelize) {
    if (!sequelize) {
        sequelize = await initializeDatabase(addr);
    }

    const rl = readline.createInterface({ input, output });
    rl.setPrompt("input: ");
    const unpatch = patchStdout(rl);

    try {
        rl.prompt(); // Initial prompt

        for await (const line of rl) {
            const data = line.trim();
            if (data === "" || data.startsWith("//")) {
                rl.prompt();
                continue;
            }

            try {
                const ds = parse(data);
                const dsStr = ds.toString();

                await insertOrIgnore(Fact, dsStr);
                const idea = strRuleGetStrIdea(dsStr);
                if (idea) {
                    await insertOrIgnore(Idea, idea);
                }
            } catch (e) {
                console.error(`error: ${e}`);
            }
            rl.prompt();
        }
    } catch (err) {
        // Silent catch for unexpected termination
    } finally {
        unpatch();
        rl.close();
    }
}
