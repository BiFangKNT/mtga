import { n as logger } from "./logger-B4ge7MhP.mjs";
import { r as rmRecursive } from "./fs-B8DrLsZ2.mjs";
import { dirname, resolve } from "pathe";
import { promises } from "node:fs";
import { hash } from "ohash";

//#region ../nuxi/src/utils/nuxt.ts
const GIT_ID_RE = /\.([0-9a-f]{7,8})$/;
async function cleanupNuxtDirs(rootDir, buildDir) {
	logger.info("Cleaning up generated Nuxt files and caches...");
	await rmRecursive([
		buildDir,
		".output",
		"dist",
		"node_modules/.vite",
		"node_modules/.cache"
	].map((dir) => resolve(rootDir, dir)));
}
function nuxtVersionToGitIdentifier(version) {
	const id = GIT_ID_RE.exec(version);
	if (id?.[1]) return id[1];
	return `v${version}`;
}
function resolveNuxtManifest(nuxt) {
	const manifest = {
		_hash: null,
		project: { rootDir: nuxt.options.rootDir },
		versions: { nuxt: nuxt._version }
	};
	manifest._hash = hash(manifest);
	return manifest;
}
async function writeNuxtManifest(nuxt, manifest = resolveNuxtManifest(nuxt)) {
	const manifestPath = resolve(nuxt.options.buildDir, "nuxt.json");
	await promises.mkdir(dirname(manifestPath), { recursive: true });
	await promises.writeFile(manifestPath, JSON.stringify(manifest, null, 2), "utf-8");
	return manifest;
}
async function loadNuxtManifest(buildDir) {
	const manifestPath = resolve(buildDir, "nuxt.json");
	return await promises.readFile(manifestPath, "utf-8").then((data) => JSON.parse(data)).catch(() => null);
}

//#endregion
export { writeNuxtManifest as a, resolveNuxtManifest as i, loadNuxtManifest as n, nuxtVersionToGitIdentifier as r, cleanupNuxtDirs as t };