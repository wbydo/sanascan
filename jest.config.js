const { pathsToModuleNameMapper } = require('ts-jest/utils');
const { compilerOptions } = require('./tsconfig');

module.exports = {
  preset: "ts-jest",
  testEnvironment: "node",
  modulePaths: ["<rootDir>/src/"],
  moduleNameMapper: pathsToModuleNameMapper(
    compilerOptions.paths,
    { prefix: "<rootDir>/" }
  ),
  testMatch: ["<rootDir>/tests/ts/**/*.test.ts"]
};
