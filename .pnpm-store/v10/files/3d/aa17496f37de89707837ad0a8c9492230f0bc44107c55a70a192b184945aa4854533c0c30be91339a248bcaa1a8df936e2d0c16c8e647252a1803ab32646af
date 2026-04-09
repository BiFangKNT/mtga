import { execSync } from "node:child_process";

//#region ../nuxi/src/utils/packageManagers.ts
function getPackageManagerVersion(name) {
	return execSync(`${name} --version`).toString("utf8").trim();
}

//#endregion
export { getPackageManagerVersion as t };