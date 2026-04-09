import { existsSync, readFileSync } from "node:fs";
import { cwd } from "node:process";
import { withCache } from "./cache.js";
import { resolveJson } from "./resolvers.js";
export var TailwindcssVersion;
(function (TailwindcssVersion) {
    TailwindcssVersion[TailwindcssVersion["V3"] = 3] = "V3";
    TailwindcssVersion[TailwindcssVersion["V4"] = 4] = "V4";
})(TailwindcssVersion || (TailwindcssVersion = {}));
export function isTailwindcssInstalled() {
    try {
        return existsSync(resolveJson("tailwindcss/package.json", cwd()));
    }
    catch {
        return false;
    }
}
export function isSupportedVersion(version) {
    return version === TailwindcssVersion.V3 || version === TailwindcssVersion.V4;
}
export function isTailwindcssVersion3(version) {
    return version === TailwindcssVersion.V3;
}
export function isTailwindcssVersion4(version) {
    return version === TailwindcssVersion.V4;
}
export function getTailwindcssVersion() {
    const packageJsonPath = resolveJson("tailwindcss/package.json", cwd());
    return withCache("version", packageJsonPath, () => {
        try {
            const packageJson = JSON.parse(readFileSync(packageJsonPath, "utf-8"));
            return parseSemanticVersion(packageJson.version);
        }
        catch {
            throw new Error("Error reading Tailwind CSS package.json");
        }
    });
}
function parseSemanticVersion(version) {
    const [major, minor, patchString] = version.split(".");
    const [patch, identifier] = patchString.split("-");
    return { identifier, major: +major, minor: +minor, patch: +patch };
}
//# sourceMappingURL=tailwindcss.js.map