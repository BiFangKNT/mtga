import { a as legacyRootDirArgs, o as logLevelArgs, t as cwdArgs } from "./_shared-BsGoKfo3.mjs";
import { n as logger } from "./logger-B4ge7MhP.mjs";
import { r as relativeToProcess, t as loadKit } from "./kit-DUlGqV3Z.mjs";
import { t as getNuxtVersion } from "./versions-Bg99eDSc.mjs";
import "./fs-B8DrLsZ2.mjs";
import { r as nuxtVersionToGitIdentifier, t as cleanupNuxtDirs } from "./nuxt-CsZm8Jhw.mjs";
import { t as getPackageManagerVersion } from "./packageManagers-BadBU-Pz.mjs";
import process from "node:process";
import { defineCommand } from "citty";
import { colors } from "consola/utils";
import { cancel, intro, isCancel, note, outro, select, spinner, tasks } from "@clack/prompts";
import { resolve } from "pathe";
import { existsSync } from "node:fs";
import { findWorkspaceDir, readPackageJSON } from "pkg-types";
import { addDependency, dedupeDependencies, detectPackageManager } from "nypm";

//#region ../nuxi/src/commands/upgrade.ts
function checkNuxtDependencyType(pkg) {
	if (pkg.dependencies?.nuxt) return "dependencies";
	if (pkg.devDependencies?.nuxt) return "devDependencies";
	return "dependencies";
}
const nuxtVersionTags = {
	"3.x": "3x",
	"4.x": "latest"
};
function getNightlyDependency(dep, nuxtVersion) {
	return `${dep}@npm:${dep}-nightly@${nuxtVersionTags[nuxtVersion]}`;
}
async function getNightlyVersion(packageNames) {
	const nuxtVersion = await select({
		message: "Which nightly Nuxt release channel do you want to install?",
		options: [{
			value: "3.x",
			label: "3.x"
		}, {
			value: "4.x",
			label: "4.x"
		}],
		initialValue: "4.x"
	});
	if (isCancel(nuxtVersion)) {
		cancel("Operation cancelled.");
		process.exit(1);
	}
	return {
		npmPackages: packageNames.map((p) => getNightlyDependency(p, nuxtVersion)),
		nuxtVersion
	};
}
async function getRequiredNewVersion(packageNames, channel) {
	switch (channel) {
		case "nightly": return getNightlyVersion(packageNames);
		case "v3": return {
			npmPackages: packageNames.map((p) => `${p}@3`),
			nuxtVersion: "3.x"
		};
		case "v3-nightly": return {
			npmPackages: packageNames.map((p) => getNightlyDependency(p, "3.x")),
			nuxtVersion: "3.x"
		};
		case "v4": return {
			npmPackages: packageNames.map((p) => `${p}@4`),
			nuxtVersion: "4.x"
		};
		case "v4-nightly": return {
			npmPackages: packageNames.map((p) => getNightlyDependency(p, "4.x")),
			nuxtVersion: "4.x"
		};
		default: return {
			npmPackages: packageNames.map((p) => `${p}@latest`),
			nuxtVersion: "4.x"
		};
	}
}
var upgrade_default = defineCommand({
	meta: {
		name: "upgrade",
		description: "Upgrade Nuxt"
	},
	args: {
		...cwdArgs,
		...logLevelArgs,
		...legacyRootDirArgs,
		dedupe: {
			type: "boolean",
			description: "Dedupe dependencies after upgrading"
		},
		force: {
			type: "boolean",
			alias: "f",
			description: "Force upgrade to recreate lockfile and node_modules"
		},
		channel: {
			type: "string",
			alias: "ch",
			default: "stable",
			description: "Specify a channel to install from (default: stable)",
			valueHint: "stable|nightly|v3|v4|v4-nightly|v3-nightly"
		}
	},
	async run(ctx) {
		const cwd = resolve(ctx.args.cwd || ctx.args.rootDir);
		intro(colors.cyan("Upgrading Nuxt ..."));
		const [packageManager, workspaceDir = cwd] = await Promise.all([detectPackageManager(cwd), findWorkspaceDir(cwd, { try: true })]);
		if (!packageManager) {
			logger.error(`Unable to determine the package manager used by this project.\n\nNo lock files found in ${colors.cyan(relativeToProcess(cwd))}, and no ${colors.cyan("packageManager")} field specified in ${colors.cyan("package.json")}.`);
			logger.info(`Please either add the ${colors.cyan("packageManager")} field to ${colors.cyan("package.json")} or execute the installation command for your package manager. For example, you can use ${colors.cyan("pnpm i")}, ${colors.cyan("npm i")}, ${colors.cyan("bun i")}, or ${colors.cyan("yarn i")}, and then try again.`);
			process.exit(1);
		}
		const { name: packageManagerName, lockFile: lockFileCandidates } = packageManager;
		const packageManagerVersion = getPackageManagerVersion(packageManagerName);
		logger.step(`Package manager: ${colors.cyan(packageManagerName)} ${packageManagerVersion}`);
		const currentVersion = await getNuxtVersion(cwd, false) || "[unknown]";
		logger.step(`Current Nuxt version: ${colors.cyan(currentVersion)}`);
		const pkg = await readPackageJSON(cwd).catch(() => null);
		const nuxtDependencyType = pkg ? checkNuxtDependencyType(pkg) : "dependencies";
		const { npmPackages, nuxtVersion } = await getRequiredNewVersion(["nuxt", ...pkg ? [
			"@nuxt/kit",
			"@nuxt/schema",
			"@nuxt/vite-builder",
			"@nuxt/webpack-builder",
			"@nuxt/rspack-builder"
		].filter((p) => pkg.dependencies?.[p] || pkg.devDependencies?.[p]) : []], ctx.args.channel);
		const toRemove = ["node_modules"];
		const lockFile = normaliseLockFile(workspaceDir, lockFileCandidates);
		if (lockFile) toRemove.push(lockFile);
		const forceRemovals = toRemove.map((p) => colors.cyan(p)).join(" and ");
		let method = ctx.args.force ? "force" : ctx.args.dedupe ? "dedupe" : void 0;
		if (!method) {
			const result = await select({
				message: `Would you like to dedupe your lockfile, or recreate ${forceRemovals}? This can fix problems with hoisted dependency versions and ensure you have the most up-to-date dependencies.`,
				options: [
					{
						label: "dedupe lockfile",
						value: "dedupe",
						hint: "recommended"
					},
					{
						label: `recreate ${forceRemovals}`,
						value: "force"
					},
					{
						label: "skip",
						value: "skip"
					}
				],
				initialValue: "dedupe"
			});
			if (isCancel(result)) {
				cancel("Operation cancelled.");
				process.exit(1);
			}
			method = result;
		}
		const versionType = ctx.args.channel === "nightly" ? "nightly" : `latest ${ctx.args.channel}`;
		const spin = spinner();
		spin.start("Upgrading Nuxt");
		await tasks([
			{
				title: `Installing ${versionType} Nuxt ${nuxtVersion} release`,
				task: async () => {
					await addDependency(npmPackages, {
						cwd,
						packageManager,
						dev: nuxtDependencyType === "devDependencies",
						workspace: packageManager?.name === "pnpm" && existsSync(resolve(cwd, "pnpm-workspace.yaml"))
					});
					return "Nuxt packages installed";
				}
			},
			...method === "force" ? [{
				title: `Recreating ${forceRemovals}`,
				task: async () => {
					await dedupeDependencies({ recreateLockfile: true });
					return "Lockfile recreated";
				}
			}] : [],
			...method === "dedupe" ? [{
				title: "Deduping dependencies",
				task: async () => {
					await dedupeDependencies();
					return "Dependencies deduped";
				}
			}] : [],
			{
				title: "Cleaning up build directories",
				task: async () => {
					let buildDir = ".nuxt";
					try {
						const { loadNuxtConfig } = await loadKit(cwd);
						buildDir = (await loadNuxtConfig({ cwd })).buildDir;
					} catch {}
					await cleanupNuxtDirs(cwd, buildDir);
					return "Build directories cleaned";
				}
			}
		]);
		spin.stop();
		if (method === "force") logger.info(`If you encounter any issues, revert the changes and try with ${colors.cyan("--no-force")}`);
		const upgradedVersion = await getNuxtVersion(cwd, false) || "[unknown]";
		if (upgradedVersion === "[unknown]") return;
		if (upgradedVersion === currentVersion) outro(`You were already using the latest version of Nuxt (${colors.green(currentVersion)})`);
		else {
			logger.success(`Successfully upgraded Nuxt from ${colors.cyan(currentVersion)} to ${colors.green(upgradedVersion)}`);
			if (currentVersion === "[unknown]") return;
			const commitA = nuxtVersionToGitIdentifier(currentVersion);
			const commitB = nuxtVersionToGitIdentifier(upgradedVersion);
			if (commitA && commitB) note(`https://github.com/nuxt/nuxt/compare/${commitA}...${commitB}`, "Changelog");
			outro("✨ Upgrade complete!");
		}
	}
});
function normaliseLockFile(cwd, lockFiles) {
	if (typeof lockFiles === "string") lockFiles = [lockFiles];
	const lockFile = lockFiles?.find((file) => existsSync(resolve(cwd, file)));
	if (lockFile === void 0) {
		logger.error(`Unable to find any lock files in ${colors.cyan(relativeToProcess(cwd))}.`);
		return;
	}
	return lockFile;
}

//#endregion
export { upgrade_default as default };