import typescript from "@rollup/plugin-typescript";
import terser from "@rollup/plugin-terser";

export default {
    input: "ddss/main.ts",
    output: {
        file: "dist/index.js",
        format: "es",
        banner: "#!/usr/bin/env node",
    },
    plugins: [typescript(), terser()],
    external: [
        "atsds",
        "atsds-bnf",
        "atsds-egg",
        "commander",
        "mariadb",
        "mysql2",
        "pg",
        "sequelize",
        "sqlite3",
        /^node:/,
    ],
};
