import { t as __exportAll } from "./rolldown-runtime-95iHPtFO.mjs";
import { o as logLevelArgs, t as cwdArgs } from "./_shared-BsGoKfo3.mjs";
import { n as logger } from "./logger-B4ge7MhP.mjs";
import { r as relativeToProcess } from "./kit-DUlGqV3Z.mjs";
import { t as getNuxtVersion } from "./versions-Bg99eDSc.mjs";
import { n as fetchModules, r as getRegistryFromContent, t as checkNuxtCompatibility } from "./_utils-Co1L4CHe.mjs";
import { t as prepare_default } from "./prepare-etx17Cow.mjs";
import { join } from "node:path";
import process from "node:process";
import { defineCommand, runCommand } from "citty";
import { colors } from "consola/utils";
import { hasTTY } from "std-env";
import { autocompleteMultiselect, cancel, confirm, isCancel, select, spinner } from "@clack/prompts";
import { resolve as resolve$1 } from "pathe";
import { fileURLToPath } from "node:url";
import * as fs from "node:fs";
import { existsSync } from "node:fs";
import { joinURL } from "ufo";
import { readPackageJSON } from "pkg-types";
import { satisfies } from "semver";
import { homedir } from "node:os";
import { addDependency, detectPackageManager } from "nypm";
import { $fetch } from "ofetch";
import { Fzf, byLengthAsc } from "fzf";
import { updateConfig } from "c12/update";

//#region ../nuxi/src/commands/_utils.ts
const nuxiCommands = [
	"add",
	"add-template",
	"analyze",
	"build",
	"cleanup",
	"_dev",
	"dev",
	"devtools",
	"generate",
	"info",
	"init",
	"module",
	"prepare",
	"preview",
	"start",
	"test",
	"typecheck",
	"upgrade"
];
function isNuxiCommand(command) {
	return nuxiCommands.includes(command);
}

//#endregion
//#region ../nuxi/src/run.ts
globalThis.__nuxt_cli__ = globalThis.__nuxt_cli__ || {
	startTime: Date.now(),
	entry: fileURLToPath(new URL("../../bin/nuxi.mjs", import.meta.url)),
	devEntry: fileURLToPath(new URL("../dev/index.mjs", import.meta.url))
};
async function runCommand$1(command, argv = process.argv.slice(2), data = {}) {
	argv.push("--no-clear");
	if (command.meta && "name" in command.meta && typeof command.meta.name === "string") {
		const name = command.meta.name;
		if (!isNuxiCommand(name)) throw new Error(`Invalid command ${name}`);
	} else throw new Error(`Invalid command, must be named`);
	return await runCommand(command, {
		rawArgs: argv,
		data: { overrides: data.overrides || {} }
	});
}

//#endregion
//#region ../nuxi/src/commands/module/_autocomplete.ts
const TRAILING_DOT_RE = /\.$/;
/**
* Interactive fuzzy search for selecting Nuxt modules
* Returns object with selected module npm package names and cancellation status
*/
async function selectModulesAutocomplete(options) {
	const { modules, message = "Search and select modules:" } = options;
	if (!hasTTY) {
		logger.warn("Interactive module selection requires a TTY. Skipping.");
		return {
			selected: [],
			cancelled: false
		};
	}
	const sortedModules = modules.toSorted((a, b) => {
		if (a.type === "official" && b.type !== "official") return -1;
		if (a.type !== "official" && b.type === "official") return 1;
		return a.npm.localeCompare(b.npm);
	});
	const fzf = new Fzf(sortedModules, {
		selector: (m) => `${m.npm} ${m.name} ${m.category}`,
		casing: "case-insensitive",
		tiebreakers: [byLengthAsc]
	});
	const clackOptions = sortedModules.map((m) => ({
		value: m.npm,
		label: m.npm,
		hint: m.description.replace(TRAILING_DOT_RE, "")
	}));
	const filter = (search, option) => {
		if (!search) return true;
		return fzf.find(search).some((r) => r.item.npm === option.value);
	};
	const result = await autocompleteMultiselect({
		message,
		options: clackOptions,
		filter,
		required: false
	});
	if (isCancel(result)) return {
		selected: [],
		cancelled: true
	};
	return {
		selected: result,
		cancelled: false
	};
}

//#endregion
//#region ../nuxi/src/commands/module/add.ts
var add_exports = /* @__PURE__ */ __exportAll({ default: () => add_default });
const PROTOCOL_RE = /^https?:\/\//;
const TRAILING_SLASH_RE = /\/$/;
const REGEX_SPECIAL_RE = /[.*+?^${}()|[\]\\]/g;
var add_default = defineCommand({
	meta: {
		name: "add",
		description: "Add Nuxt modules"
	},
	args: {
		...cwdArgs,
		...logLevelArgs,
		moduleName: {
			type: "positional",
			description: "Specify one or more modules to install by name, separated by spaces"
		},
		skipInstall: {
			type: "boolean",
			description: "Skip npm install"
		},
		skipConfig: {
			type: "boolean",
			description: "Skip nuxt.config.ts update"
		},
		dev: {
			type: "boolean",
			description: "Install modules as dev dependencies"
		}
	},
	async setup(ctx) {
		const cwd = resolve$1(ctx.args.cwd);
		let modules = ctx.args._.map((e) => e.trim()).filter(Boolean);
		const projectPkg = await readPackageJSON(cwd).catch(() => ({}));
		if (!projectPkg.dependencies?.nuxt && !projectPkg.devDependencies?.nuxt) {
			logger.warn(`No ${colors.cyan("nuxt")} dependency detected in ${colors.cyan(relativeToProcess(cwd))}.`);
			const shouldContinue = await confirm({
				message: `Do you want to continue anyway?`,
				initialValue: false
			});
			if (isCancel(shouldContinue) || shouldContinue !== true) process.exit(1);
		}
		if (modules.length === 0) {
			const modulesSpinner = spinner();
			modulesSpinner.start("Fetching available modules");
			const [allModules, nuxtVersion] = await Promise.all([fetchModules(), getNuxtVersion(cwd)]);
			const compatibleModules = allModules.filter((m) => !m.compatibility.nuxt || checkNuxtCompatibility(m, nuxtVersion));
			modulesSpinner.stop("Modules loaded");
			const result = await selectModulesAutocomplete({
				modules: compatibleModules,
				message: "Search modules to add (Esc to finish):"
			});
			if (result.selected.length === 0) {
				cancel("No modules selected.");
				process.exit(0);
			}
			modules = result.selected;
		}
		const resolvedModules = [];
		for (const moduleName of modules) {
			const resolvedModule = await resolveModule(moduleName, cwd);
			if (resolvedModule) resolvedModules.push(resolvedModule);
		}
		if (resolvedModules.length === 0) {
			cancel("No modules to add.");
			process.exit(1);
		}
		logger.info(`Resolved ${resolvedModules.map((x) => colors.cyan(x.pkgName)).join(", ")}, adding module${resolvedModules.length > 1 ? "s" : ""}...`);
		await addModules(resolvedModules, {
			...ctx.args,
			cwd
		}, projectPkg);
		if (!ctx.args.skipInstall) await runCommand$1(prepare_default, Object.entries(ctx.args).filter(([k]) => k in cwdArgs || k in logLevelArgs).map(([k, v]) => `--${k}=${v}`));
	}
});
async function addModules(modules, { skipInstall = false, skipConfig = false, cwd, dev = false }, projectPkg) {
	if (!skipInstall) {
		const installedModules = [];
		const notInstalledModules = [];
		const dependencies = new Set([...Object.keys(projectPkg.dependencies || {}), ...Object.keys(projectPkg.devDependencies || {})]);
		for (const module of modules) if (dependencies.has(module.pkgName)) installedModules.push(module);
		else notInstalledModules.push(module);
		if (installedModules.length > 0) {
			const installedModulesList = installedModules.map((module) => colors.cyan(module.pkgName)).join(", ");
			const are = installedModules.length > 1 ? "are" : "is";
			logger.info(`${installedModulesList} ${are} already installed`);
		}
		if (notInstalledModules.length > 0) {
			const isDev = Boolean(projectPkg.devDependencies?.nuxt) || dev;
			const notInstalledModulesList = notInstalledModules.map((module) => colors.cyan(module.pkg)).join(", ");
			const dependency = notInstalledModules.length > 1 ? "dependencies" : "dependency";
			const a = notInstalledModules.length > 1 ? "" : " a";
			logger.info(`Installing ${notInstalledModulesList} as${a}${isDev ? " development" : ""} ${dependency}`);
			const packageManager = await detectPackageManager(cwd);
			if (await addDependency(notInstalledModules.map((module) => module.pkg), {
				cwd,
				dev: isDev,
				installPeerDependencies: true,
				packageManager,
				workspace: packageManager?.name === "pnpm" && existsSync(resolve$1(cwd, "pnpm-workspace.yaml"))
			}).then(() => true).catch(async (error) => {
				logger.error(String(error));
				const result = await confirm({
					message: `Install failed for ${notInstalledModules.map((module) => colors.cyan(module.pkg)).join(", ")}. Do you want to continue adding the module${notInstalledModules.length > 1 ? "s" : ""} to ${colors.cyan("nuxt.config")}?`,
					initialValue: false
				});
				if (isCancel(result)) return false;
				return result;
			}) !== true) return;
		}
	}
	if (!skipConfig) await updateConfig({
		cwd,
		configFile: "nuxt.config",
		async onCreate() {
			logger.info(`Creating ${colors.cyan("nuxt.config.ts")}`);
			return getDefaultNuxtConfig();
		},
		async onUpdate(config) {
			if (!config.modules) config.modules = [];
			for (const resolved of modules) {
				if (config.modules.includes(resolved.pkgName)) {
					logger.info(`${colors.cyan(resolved.pkgName)} is already in the ${colors.cyan("modules")}`);
					continue;
				}
				logger.info(`Adding ${colors.cyan(resolved.pkgName)} to the ${colors.cyan("modules")}`);
				config.modules.push(resolved.pkgName);
			}
		}
	}).catch((error) => {
		logger.error(`Failed to update ${colors.cyan("nuxt.config")}: ${error.message}`);
		logger.error(`Please manually add ${colors.cyan(modules.map((module) => module.pkgName).join(", "))} to the ${colors.cyan("modules")} in ${colors.cyan("nuxt.config.ts")}`);
		return null;
	});
}
function getDefaultNuxtConfig() {
	return `
// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: []
})`;
}
const packageRegex = /^(@[a-z0-9-~][a-z0-9-._~]*\/)?([a-z0-9-~][a-z0-9-._~]*)(@[^@]+)?$/;
async function resolveModule(moduleName, cwd) {
	let pkgName = moduleName;
	let pkgVersion;
	const reMatch = moduleName.match(packageRegex);
	if (reMatch) {
		if (reMatch[3]) {
			pkgName = `${reMatch[1] || ""}${reMatch[2] || ""}`;
			pkgVersion = reMatch[3].slice(1);
		}
	} else {
		logger.error(`Invalid package name ${colors.cyan(pkgName)}.`);
		return false;
	}
	const matchedModule = (await fetchModules().catch((err) => {
		logger.warn(`Cannot search in the Nuxt Modules database: ${err}`);
		return [];
	})).find((module) => module.name === moduleName || pkgVersion && module.name === pkgName || module.npm === pkgName || module.aliases?.includes(pkgName));
	if (matchedModule?.npm) pkgName = matchedModule.npm;
	if (matchedModule && matchedModule.compatibility.nuxt) {
		const nuxtVersion = await getNuxtVersion(cwd);
		if (!checkNuxtCompatibility(matchedModule, nuxtVersion)) {
			logger.warn(`The module ${colors.cyan(pkgName)} is not compatible with Nuxt ${colors.cyan(nuxtVersion)} (requires ${colors.cyan(matchedModule.compatibility.nuxt)})`);
			const shouldContinue = await confirm({
				message: "Do you want to continue installing incompatible version?",
				initialValue: false
			});
			if (isCancel(shouldContinue) || !shouldContinue) return false;
		}
		const versionMap = matchedModule.compatibility.versionMap;
		if (versionMap) {
			for (const [_nuxtVersion, _moduleVersion] of Object.entries(versionMap)) if (satisfies(nuxtVersion, _nuxtVersion)) {
				if (!pkgVersion) pkgVersion = _moduleVersion;
				else {
					logger.warn(`Recommended version of ${colors.cyan(pkgName)} for Nuxt ${colors.cyan(nuxtVersion)} is ${colors.cyan(_moduleVersion)} but you have requested ${colors.cyan(pkgVersion)}.`);
					const result = await select({
						message: "Choose a version:",
						options: [{
							value: _moduleVersion,
							label: _moduleVersion
						}, {
							value: pkgVersion,
							label: pkgVersion
						}]
					});
					if (isCancel(result)) return false;
					pkgVersion = result;
				}
				break;
			}
		}
	}
	let version = pkgVersion || "latest";
	const meta = await detectNpmRegistry(pkgName.startsWith("@") ? pkgName.split("/")[0] : null);
	const headers = {};
	if (meta.authToken) headers.Authorization = `Bearer ${meta.authToken}`;
	const pkgDetails = await $fetch(joinURL(meta.registry, `${pkgName}`), { headers }).catch(() => null);
	if (!pkgDetails) {
		logger.error(`Failed to fetch package details for ${colors.cyan(pkgName)}.`);
		return false;
	}
	if (pkgDetails["dist-tags"]?.[version]) version = pkgDetails["dist-tags"][version];
	else version = Object.keys(pkgDetails.versions)?.findLast((v) => satisfies(v, version)) || version;
	const pkg = pkgDetails.versions[version] || {};
	const pkgDependencies = Object.assign(pkg.dependencies || {}, pkg.devDependencies || {});
	if (!pkgDependencies.nuxt && !pkgDependencies["nuxt-edge"] && !pkgDependencies["@nuxt/kit"]) {
		logger.warn(`It seems that ${colors.cyan(pkgName)} is not a Nuxt module.`);
		const shouldContinue = await confirm({
			message: `Do you want to continue installing ${colors.cyan(pkgName)} anyway?`,
			initialValue: false
		});
		if (isCancel(shouldContinue) || !shouldContinue) return false;
	}
	return {
		nuxtModule: matchedModule,
		pkg: `${pkgName}@${version}`,
		pkgName,
		pkgVersion: version
	};
}
function getNpmrcPaths() {
	const userNpmrcPath = join(homedir(), ".npmrc");
	return [join(process.cwd(), ".npmrc"), userNpmrcPath];
}
async function getAuthToken(registry) {
	const paths = getNpmrcPaths();
	const registryHost = registry.replace(PROTOCOL_RE, "").replace(TRAILING_SLASH_RE, "").replace(REGEX_SPECIAL_RE, "\\$&");
	const authTokenRegex = new RegExp(`^//${registryHost}/:_authToken=(.+)$`, "m");
	for (const npmrcPath of paths) {
		let fd;
		try {
			fd = await fs.promises.open(npmrcPath, "r");
			if (await fd.stat().then((r) => r.isFile())) {
				const authTokenMatch = (await fd.readFile("utf-8")).match(authTokenRegex)?.[1];
				if (authTokenMatch) return authTokenMatch.trim();
			}
		} catch {} finally {
			await fd?.close();
		}
	}
	return null;
}
async function detectNpmRegistry(scope) {
	const registry = await getRegistry(scope);
	return {
		registry,
		authToken: await getAuthToken(registry)
	};
}
async function getRegistry(scope) {
	if (process.env.COREPACK_NPM_REGISTRY) return process.env.COREPACK_NPM_REGISTRY;
	const registry = await getRegistryFromFile(getNpmrcPaths(), scope);
	if (registry) process.env.COREPACK_NPM_REGISTRY = registry;
	return registry || "https://registry.npmjs.org";
}
async function getRegistryFromFile(paths, scope) {
	for (const npmrcPath of paths) {
		let fd;
		try {
			fd = await fs.promises.open(npmrcPath, "r");
			if (await fd.stat().then((r) => r.isFile())) {
				const registry = getRegistryFromContent(await fd.readFile("utf-8"), scope);
				if (registry) return registry;
			}
		} catch {} finally {
			await fd?.close();
		}
	}
	return null;
}

//#endregion
export { runCommand$1 as i, add_exports as n, selectModulesAutocomplete as r, add_default as t };