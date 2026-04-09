import { resolveModulePath } from "exsolve";
import "node:fs";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import "node:url";
import "node:os";
import { join, normalize } from "pathe";
import "jiti";
import "rc9";
import "defu";
import "pkg-types";
import { dirname, extname } from "node:path";

//#region src/loader.ts
const SUPPORTED_EXTENSIONS = Object.freeze([
	".js",
	".ts",
	".mjs",
	".cjs",
	".mts",
	".cts",
	".json",
	".jsonc",
	".json5",
	".yaml",
	".yml",
	".toml"
]);

//#endregion
//#region src/update.ts
const UPDATABLE_EXTS = [
	".js",
	".ts",
	".mjs",
	".cjs",
	".mts",
	".cts"
];
/**
* @experimental Update a config file or create a new one.
*/
async function updateConfig(opts) {
	const { parseModule } = await import("magicast");
	let configFile = tryResolve(`./${opts.configFile}`, opts.cwd, SUPPORTED_EXTENSIONS) || tryResolve(`./.config/${opts.configFile}`, opts.cwd, SUPPORTED_EXTENSIONS) || tryResolve(`./.config/${opts.configFile.split(".")[0]}`, opts.cwd, SUPPORTED_EXTENSIONS);
	let created = false;
	if (!configFile) {
		configFile = join(opts.cwd, opts.configFile + (opts.createExtension || ".ts"));
		const createResult = await opts.onCreate?.({ configFile }) ?? true;
		if (!createResult) throw new Error("Config file creation aborted.");
		const content = typeof createResult === "string" ? createResult : `export default {}\n`;
		await mkdir(dirname(configFile), { recursive: true });
		await writeFile(configFile, content, "utf8");
		created = true;
	}
	const ext = extname(configFile);
	if (!UPDATABLE_EXTS.includes(ext)) throw new Error(`Unsupported config file extension: ${ext} (${configFile}) (supported: ${UPDATABLE_EXTS.join(", ")})`);
	const _module = parseModule(await readFile(configFile, "utf8"), opts.magicast);
	const defaultExport = _module.exports.default;
	if (!defaultExport) throw new Error("Default export is missing in the config file!");
	const configObj = defaultExport.$type === "function-call" ? defaultExport.$args[0] : defaultExport;
	await opts.onUpdate?.(configObj);
	await writeFile(configFile, _module.generate().code);
	return {
		configFile,
		created
	};
}
function tryResolve(path, cwd, extensions) {
	const res = resolveModulePath(path, {
		try: true,
		from: join(cwd, "/"),
		extensions,
		suffixes: ["", "/index"],
		cache: false
	});
	return res ? normalize(res) : void 0;
}

//#endregion
export { updateConfig };