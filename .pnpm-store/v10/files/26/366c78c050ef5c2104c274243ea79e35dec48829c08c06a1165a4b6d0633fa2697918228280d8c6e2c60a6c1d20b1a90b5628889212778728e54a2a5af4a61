import { resolve } from "node:path";
import { withCache } from "./cache.js";
import { findFileRecursive } from "./fs.js";
export const getTSConfigPath = ({ configPath, cwd }) => withCache("tsconfig-path", configPath, () => {
    const potentialPaths = [
        ...configPath ? [configPath] : [],
        "tsconfig.json",
        "jsconfig.json"
    ];
    const foundConfigPath = findFileRecursive(cwd, potentialPaths);
    const warning = getConfigPathWarning(configPath, foundConfigPath);
    return {
        path: foundConfigPath,
        warnings: [warning]
    };
});
function getConfigPathWarning(configPath, foundConfigPath) {
    if (!configPath) {
        return;
    }
    if (foundConfigPath && resolve(configPath) === resolve(foundConfigPath)) {
        return;
    }
    return {
        option: "tsconfig",
        title: `No tsconfig found at \`${configPath}\``
    };
}
//# sourceMappingURL=tsconfig.js.map