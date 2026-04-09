import { n as tryResolveNuxt } from "./kit-DUlGqV3Z.mjs";
import { readFileSync } from "node:fs";
import { resolveModulePath } from "exsolve";
import { readPackageJSON } from "pkg-types";
import { coerce } from "semver";

//#region ../nuxi/src/utils/versions.ts
async function getNuxtVersion(cwd, cache = true) {
	const nuxtPkg = await readPackageJSON("nuxt", {
		url: cwd,
		try: true,
		cache
	});
	if (nuxtPkg) return nuxtPkg.version;
	const pkg = await readPackageJSON(cwd);
	const pkgDep = pkg?.dependencies?.nuxt || pkg?.devDependencies?.nuxt;
	return pkgDep && coerce(pkgDep)?.version || "3.0.0";
}
function getPkgVersion(cwd, pkg) {
	return getPkgJSON(cwd, pkg)?.version ?? "";
}
function getPkgJSON(cwd, pkg) {
	for (const url of [cwd, tryResolveNuxt(cwd)]) {
		if (!url) continue;
		const p = resolveModulePath(`${pkg}/package.json`, {
			from: url,
			try: true
		});
		if (p) return JSON.parse(readFileSync(p, "utf-8"));
	}
	return null;
}

//#endregion
export { getPkgJSON as n, getPkgVersion as r, getNuxtVersion as t };