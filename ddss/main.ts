import { Command } from "commander";
import * as path from "node:path";
import * as os from "node:os";
import * as fs from "node:fs";
import { initializeDatabase } from "./orm.js";
import { main as ds } from "./ds.js";
import { main as egg } from "./egg.js";
import { main as input } from "./input.js";
import { main as output } from "./output.js";
import { main as load } from "./load.js";
import { main as dump } from "./dump.js";

import { fileURLToPath } from "node:url";

const componentMap: Record<string, any> = {
    ds,
    egg,
    input,
    output,
    load,
    dump,
};

async function run(addr: string, components: string[]) {
    const sequelize = await initializeDatabase(addr);

    try {
        const promises = components.map((name) => {
            const component = componentMap[name];
            if (!component) {
                console.error(`error: unsupported component: ${name}`);
                process.exit(1);
            }
            return component(addr, sequelize);
        });

        // Run all components in parallel.
        // Note: Some components like input/output run forever.
        await Promise.all(promises);
    } catch (err) {
        // Handle error
    } finally {
        await sequelize.close();
    }
}

export function cli() {
    const program = new Command();

    program
        .name("ddss")
        .description("DDSS - Distributed Deductive System Sorts: Run DDSS with an interactive deductive environment.")
        .option("-a, --addr <url>", "Database address URL. If not provided, uses a temporary SQLite database.")
        .option("-c, --component <names...>", "Components to run.", ["input", "output", "ds", "egg"])
        .action(async (options) => {
            let addr = options.addr;
            if (!addr) {
                const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "ddss-"));
                const dbPath = path.join(tmpDir, "ddss.db");
                addr = `sqlite:///${dbPath}`;
            }

            console.log(`addr: ${addr}`);
            await run(addr, options.component);
        });

    program.parse();
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
    cli();
}
