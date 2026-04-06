export default {
    testMatch: ["<rootDir>/tests/test_*.ts"],
    collectCoverage: true,
    extensionsToTreatAsEsm: [".ts"],
    transform: {
        "^.+\\.tsx?$": ["@swc/jest"],
    },
};
