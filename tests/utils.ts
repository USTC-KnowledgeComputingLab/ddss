import { initializeDatabase } from "../ddss/orm.ts";
import * as fs from "node:fs";
import * as path from "node:path";
import * as os from "node:os";

export async function createTempDb() {
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "ddss-test-"));
    const dbPath = path.join(tmpDir, "test.db");
    // Sequelize sqlite dialect expects "sqlite:/path/to/db" or "sqlite:memory:"
    const addr = `sqlite:${dbPath}`;

    const sequelize = await initializeDatabase(addr);

    return {
        sequelize,
        addr,
        cleanup: async () => {
            await sequelize.close();
            fs.rmSync(tmpDir, { recursive: true, force: true });
        },
    };
}
