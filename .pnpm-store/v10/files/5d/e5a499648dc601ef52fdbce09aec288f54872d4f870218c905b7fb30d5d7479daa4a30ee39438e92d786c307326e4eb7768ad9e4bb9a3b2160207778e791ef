import { a as legacyRootDirArgs, t as cwdArgs } from "./_shared-BsGoKfo3.mjs";
import { n as logger } from "./logger-B4ge7MhP.mjs";
import { n as tryResolveNuxt } from "./kit-DUlGqV3Z.mjs";
import "./versions-Bg99eDSc.mjs";
import { t as getBuilder } from "./banner-C2vxTb-6.mjs";
import { t as formatInfoBox } from "./formatting-BVTBOej7.mjs";
import { t as getPackageManagerVersion } from "./packageManagers-BadBU-Pz.mjs";
import process from "node:process";
import { defineCommand } from "citty";
import { colors } from "consola/utils";
import { isBun, isDeno, isMinimal } from "std-env";
import { box } from "@clack/prompts";
import { resolve } from "pathe";
import { readPackageJSON } from "pkg-types";
import os from "node:os";
import { detectPackageManager } from "nypm";
import { writeText } from "tinyclip";

//#region ../nuxi/package.json
var version = "3.34.0";

//#endregion
//#region ../nuxi/src/commands/info.ts
const LEADING_SLASH_RE = /^\//;
var info_default = defineCommand({
	meta: {
		name: "info",
		description: "Get information about Nuxt project"
	},
	args: {
		...cwdArgs,
		...legacyRootDirArgs
	},
	async run(ctx) {
		const cwd = resolve(ctx.args.cwd || ctx.args.rootDir);
		const nuxtConfig = await getNuxtConfig(cwd);
		const { dependencies = {}, devDependencies = {} } = await readPackageJSON(cwd).catch(() => ({}));
		const nuxtPath = tryResolveNuxt(cwd);
		async function getDepVersion(name) {
			for (const url of [cwd, nuxtPath]) {
				if (!url) continue;
				const pkg = await readPackageJSON(name, { url }).catch(() => null);
				if (pkg) return pkg.version;
			}
			return dependencies[name] || devDependencies[name];
		}
		async function listModules(arr = []) {
			const info = [];
			for (let m of arr) {
				if (Array.isArray(m)) m = m[0];
				const name = normalizeConfigModule(m, cwd);
				if (name) {
					const v = await getDepVersion(name.split("/").splice(0, 2).join("/"));
					info.push(`\`${v ? `${name}@${v}` : name}\``);
				}
			}
			return info.join(", ");
		}
		const nuxtVersion = await getDepVersion("nuxt") || await getDepVersion("nuxt-nightly") || await getDepVersion("nuxt-edge") || await getDepVersion("nuxt3") || "-";
		const isLegacy = nuxtVersion.startsWith("2");
		const builder = !isLegacy ? nuxtConfig.builder || "vite" : nuxtConfig.bridge?.vite ? "vite" : nuxtConfig.buildModules?.includes("nuxt-vite") ? "vite" : "webpack";
		let packageManager = (await detectPackageManager(cwd))?.name;
		if (packageManager) packageManager += `@${getPackageManagerVersion(packageManager)}`;
		const osType = os.type();
		const builderInfo = typeof builder === "string" ? getBuilder(cwd, builder) : {
			name: "custom",
			version: "0.0.0"
		};
		const infoObj = {
			"Operating system": osType === "Darwin" ? `macOS ${os.release()}` : osType === "Windows_NT" ? `Windows ${os.release()}` : `${osType} ${os.release()}`,
			"CPU": `${os.cpus()[0]?.model || "unknown"} (${os.cpus().length} cores)`,
			...isBun ? { "Bun version": Bun?.version } : isDeno ? { "Deno version": Deno?.version.deno } : { "Node.js version": process.version },
			"nuxt/cli version": version,
			"Package manager": packageManager ?? "unknown",
			"Nuxt version": nuxtVersion,
			"Nitro version": await getDepVersion("nitropack") || await getDepVersion("nitro"),
			"Builder": builderInfo.name === "custom" ? "custom" : `${builderInfo.name.toLowerCase()}@${builderInfo.version}`,
			"Config": Object.keys(nuxtConfig).map((key) => `\`${key}\``).sort().join(", "),
			"Modules": await listModules(nuxtConfig.modules),
			...isLegacy ? { "Build modules": await listModules(nuxtConfig.buildModules || []) } : {}
		};
		logger.info(`Nuxt root directory: ${colors.cyan(nuxtConfig.rootDir || cwd)}\n`);
		const boxStr = formatInfoBox(infoObj);
		let firstColumnLength = 0;
		let secondColumnLength = 0;
		const entries = Object.entries(infoObj).map(([label, val]) => {
			if (label.length > firstColumnLength) firstColumnLength = label.length + 4;
			if ((val || "").length > secondColumnLength) secondColumnLength = (val || "").length + 2;
			return [label, val || "-"];
		});
		let copyStr = `| ${" ".repeat(firstColumnLength)} | ${" ".repeat(secondColumnLength)} |\n| ${"-".repeat(firstColumnLength)} | ${"-".repeat(secondColumnLength)} |\n`;
		for (const [label, value] of entries) if (!isMinimal) copyStr += `| ${`**${label}**`.padEnd(firstColumnLength)} | ${(value.includes("`") ? value : `\`${value}\``).padEnd(secondColumnLength)} |\n`;
		if (!isMinimal && await writeText(copyStr).then(() => true).catch(() => false)) box(`\n${boxStr}`, ` Nuxt project info ${colors.gray("(copied to clipboard) ")}`, {
			contentAlign: "left",
			titleAlign: "left",
			width: "auto",
			titlePadding: 2,
			contentPadding: 2,
			rounded: true
		});
		else logger.info(`Nuxt project info:\n${copyStr}`, { withGuide: false });
		const isNuxt3 = !isLegacy;
		const isBridge = !isNuxt3 && infoObj["Build modules"]?.includes("bridge");
		const repo = isBridge ? "nuxt/bridge" : "nuxt/nuxt";
		const docsURL = isNuxt3 || isBridge ? "https://nuxt.com" : "https://v2.nuxt.com";
		logger.info(`👉 Read documentation: ${colors.cyan(docsURL)}`);
		if (isNuxt3 || isBridge) {
			logger.info(`👉 Report an issue: ${colors.cyan(`https://github.com/${repo}/issues/new?template=bug-report.yml`)}`, { spacing: 0 });
			logger.info(`👉 Suggest an improvement: ${colors.cyan(`https://github.com/${repo}/discussions/new`)}`, { spacing: 0 });
		}
	}
});
function normalizeConfigModule(module, rootDir) {
	if (!module) return null;
	if (typeof module === "string") return module.split(rootDir).pop().split("node_modules").pop().replace(LEADING_SLASH_RE, "");
	if (typeof module === "function") return `${module.name}()`;
	if (Array.isArray(module)) return normalizeConfigModule(module[0], rootDir);
	return null;
}
async function getNuxtConfig(rootDir) {
	try {
		const { createJiti } = await import("jiti");
		const jiti = createJiti(rootDir, {
			interopDefault: true,
			alias: {
				"~": rootDir,
				"@": rootDir
			}
		});
		globalThis.defineNuxtConfig = (c) => c;
		const result = await jiti.import("./nuxt.config", { default: true });
		delete globalThis.defineNuxtConfig;
		return result;
	} catch {
		return {};
	}
}

//#endregion
export { info_default as default };