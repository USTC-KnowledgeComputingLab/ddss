import typescript from "@rollup/plugin-typescript";

export default {
    input: "ddss/main.ts",
    output: {
        file: "dist/index.js",
        format: "es",
        banner: "#!/usr/bin/env node",
    },
    plugins: [typescript()],
    external: ["atsds", "atsds-bnf", "atsds-egg", "commander", "sequelize", "sqlite3", /^node:/],
};
