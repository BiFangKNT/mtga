#!/usr/bin/env node
import { createRequire } from "node:module";
import { defineCommand, runMain } from "citty";
import { join, normalize, resolve } from "pathe";
import { x } from "tinyexec";
import * as fs from "node:fs";
import { existsSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { join as join$1 } from "node:path";
var name = "nypm";
var version = "0.6.4";
var description = "Unified Package Manager for Node.js";
const packageManagers = [
	{
		name: "npm",
		command: "npm",
		lockFile: "package-lock.json"
	},
	{
		name: "pnpm",
		command: "pnpm",
		lockFile: "pnpm-lock.yaml",
		files: ["pnpm-workspace.yaml"]
	},
	{
		name: "bun",
		command: "bun",
		lockFile: ["bun.lockb", "bun.lock"]
	},
	{
		name: "yarn",
		command: "yarn",
		lockFile: "yarn.lock",
		files: [".yarnrc.yml"]
	},
	{
		name: "deno",
		command: "deno",
		lockFile: "deno.lock",
		files: ["deno.json"]
	}
];
async function detectPackageManager(cwd, options = {}) {
	const detected = await findup(resolve(cwd || "."), async (path) => {
		if (!options.ignorePackageJSON) {
			const packageJSONPath = join(path, "package.json");
			if (existsSync(packageJSONPath)) {
				const packageJSON = JSON.parse(await readFile(packageJSONPath, "utf8"));
				if (packageJSON?.packageManager) {
					const { name, version = "0.0.0", buildMeta, warnings } = parsePackageManagerField(packageJSON.packageManager);
					if (name) {
						const majorVersion = version.split(".")[0];
						const packageManager = packageManagers.find((pm) => pm.name === name && pm.majorVersion === majorVersion) || packageManagers.find((pm) => pm.name === name);
						return {
							name,
							command: name,
							version,
							majorVersion,
							buildMeta,
							warnings,
							files: packageManager?.files,
							lockFile: packageManager?.lockFile
						};
					}
				}
			}
			if (existsSync(join(path, "deno.json"))) return packageManagers.find((pm) => pm.name === "deno");
		}
		if (!options.ignoreLockFile) {
			for (const packageManager of packageManagers) if ([packageManager.lockFile, packageManager.files].flat().filter(Boolean).some((file) => existsSync(resolve(path, file)))) return { ...packageManager };
		}
	}, { includeParentDirs: options.includeParentDirs ?? true });
	if (!detected && !options.ignoreArgv) {
		const scriptArg = process.argv[1];
		if (scriptArg) {
			for (const packageManager of packageManagers) if (new RegExp(`[/\\\\]\\.?${packageManager.command}`).test(scriptArg)) return packageManager;
		}
	}
	return detected;
}
async function findup(cwd, match, options = {}) {
	const segments = normalize(cwd).split("/");
	while (segments.length > 0) {
		const result = await match(segments.join("/") || "/");
		if (result || !options.includeParentDirs) return result;
		segments.pop();
	}
}
async function readPackageJSON(cwd) {
	return findup(cwd, (p) => {
		const pkgPath = join$1(p, "package.json");
		if (existsSync(pkgPath)) return readFile(pkgPath, "utf8").then((data) => JSON.parse(data));
	});
}
function cached(fn) {
	let v;
	return () => {
		if (v === void 0) v = fn().then((r) => {
			v = r;
			return v;
		});
		return v;
	};
}
const hasCorepack = cached(async () => {
	if (globalThis.process?.versions?.webcontainer) return false;
	try {
		const { exitCode } = await x("corepack", ["--version"]);
		return exitCode === 0;
	} catch {
		return false;
	}
});
async function executeCommand(command, args, options = {}) {
	const xArgs = command !== "npm" && command !== "bun" && command !== "deno" && options.corepack !== false && await hasCorepack() ? ["corepack", [command, ...args]] : [command, args];
	const { exitCode, stdout, stderr } = await x(xArgs[0], xArgs[1], { nodeOptions: {
		cwd: resolve(options.cwd || process.cwd()),
		env: options.env,
		stdio: options.silent ? "pipe" : "inherit"
	} });
	if (exitCode !== 0) throw new Error(`\`${xArgs.flat().join(" ")}\` failed.${options.silent ? [
		"",
		stdout,
		stderr
	].join("\n") : ""}`);
}
const NO_PACKAGE_MANAGER_DETECTED_ERROR_MSG = "No package manager auto-detected.";
async function resolveOperationOptions(options = {}) {
	const cwd = options.cwd || process.cwd();
	const env = {
		...process.env,
		...options.env
	};
	const packageManager = (typeof options.packageManager === "string" ? packageManagers.find((pm) => pm.name === options.packageManager) : options.packageManager) || await detectPackageManager(options.cwd || process.cwd());
	if (!packageManager) throw new Error(NO_PACKAGE_MANAGER_DETECTED_ERROR_MSG);
	return {
		cwd,
		env,
		silent: options.silent ?? false,
		packageManager,
		dev: options.dev ?? false,
		workspace: options.workspace,
		global: options.global ?? false,
		dry: options.dry ?? false,
		corepack: options.corepack ?? true
	};
}
function getWorkspaceArgs(options) {
	if (!options.workspace) return [];
	const workspacePkg = typeof options.workspace === "string" && options.workspace !== "" ? options.workspace : void 0;
	if (options.packageManager.name === "pnpm") return workspacePkg ? ["--filter", workspacePkg] : ["--workspace-root"];
	if (options.packageManager.name === "npm") return workspacePkg ? ["-w", workspacePkg] : ["--workspaces"];
	if (options.packageManager.name === "yarn") if (!options.packageManager.majorVersion || options.packageManager.majorVersion === "1") return workspacePkg ? ["--cwd", workspacePkg] : ["-W"];
	else return workspacePkg ? ["workspace", workspacePkg] : [];
	return [];
}
function parsePackageManagerField(packageManager) {
	const [name, _version] = (packageManager || "").split("@");
	const [version, buildMeta] = _version?.split("+") || [];
	if (name && name !== "-" && /^(@[a-z0-9-~][a-z0-9-._~]*\/)?[a-z0-9-~][a-z0-9-._~]*$/.test(name)) return {
		name,
		version,
		buildMeta
	};
	const sanitized = (name || "").replace(/\W+/g, "");
	return {
		name: sanitized,
		version,
		buildMeta,
		warnings: [`Abnormal characters found in \`packageManager\` field, sanitizing from \`${name}\` to \`${sanitized}\``]
	};
}
async function installDependencies(options = {}) {
	const resolvedOptions = await resolveOperationOptions(options);
	const commandArgs = options.frozenLockFile ? {
		npm: ["ci"],
		yarn: ["install", "--immutable"],
		bun: ["install", "--frozen-lockfile"],
		pnpm: ["install", "--frozen-lockfile"],
		deno: ["install", "--frozen"]
	}[resolvedOptions.packageManager.name] : ["install"];
	if (options.ignoreWorkspace && resolvedOptions.packageManager.name === "pnpm") commandArgs.push("--ignore-workspace");
	if (!resolvedOptions.dry) await executeCommand(resolvedOptions.packageManager.command, commandArgs, {
		cwd: resolvedOptions.cwd,
		silent: resolvedOptions.silent,
		corepack: resolvedOptions.corepack
	});
	return { exec: {
		command: resolvedOptions.packageManager.command,
		args: commandArgs
	} };
}
async function addDependency(name, options = {}) {
	const resolvedOptions = await resolveOperationOptions(options);
	const names = Array.isArray(name) ? name : [name];
	if (resolvedOptions.packageManager.name === "deno") {
		for (let i = 0; i < names.length; i++) if (!/^(npm|jsr|file):.+$/.test(names[i] || "")) names[i] = `npm:${names[i]}`;
	}
	if (names.length === 0) return {};
	const args = (resolvedOptions.packageManager.name === "yarn" ? [
		...getWorkspaceArgs(resolvedOptions),
		resolvedOptions.global && resolvedOptions.packageManager.majorVersion === "1" ? "global" : "",
		"add",
		resolvedOptions.dev ? "-D" : "",
		...names
	] : [
		resolvedOptions.packageManager.name === "npm" ? "install" : "add",
		...getWorkspaceArgs(resolvedOptions),
		resolvedOptions.dev ? "-D" : "",
		resolvedOptions.global ? "-g" : "",
		...names
	]).filter(Boolean);
	if (!resolvedOptions.dry) await executeCommand(resolvedOptions.packageManager.command, args, {
		cwd: resolvedOptions.cwd,
		silent: resolvedOptions.silent,
		corepack: resolvedOptions.corepack
	});
	if (!resolvedOptions.dry && options.installPeerDependencies) {
		const existingPkg = await readPackageJSON(resolvedOptions.cwd);
		const peerDeps = [];
		const peerDevDeps = [];
		const _require = createRequire(join$1(resolvedOptions.cwd, "/_.js"));
		for (const _name of names) {
			const pkgName = _name.match(/^(.[^@]+)/)?.[0];
			const pkg = await readPackageJSON(_require.resolve(pkgName));
			if (!pkg?.peerDependencies || pkg?.name !== pkgName) continue;
			for (const [peerDependency, version] of Object.entries(pkg.peerDependencies)) {
				if (pkg.peerDependenciesMeta?.[peerDependency]?.optional) continue;
				if (existingPkg?.dependencies?.[peerDependency] || existingPkg?.devDependencies?.[peerDependency]) continue;
				(pkg.peerDependenciesMeta?.[peerDependency]?.dev ? peerDevDeps : peerDeps).push(`${peerDependency}@${version}`);
			}
		}
		if (peerDeps.length > 0) await addDependency(peerDeps, { ...resolvedOptions });
		if (peerDevDeps.length > 0) await addDevDependency(peerDevDeps, { ...resolvedOptions });
	}
	return { exec: {
		command: resolvedOptions.packageManager.command,
		args
	} };
}
async function addDevDependency(name, options = {}) {
	return await addDependency(name, {
		...options,
		dev: true
	});
}
async function removeDependency(name, options = {}) {
	const resolvedOptions = await resolveOperationOptions(options);
	const names = Array.isArray(name) ? name : [name];
	if (names.length === 0) return {};
	const args = (resolvedOptions.packageManager.name === "yarn" ? [
		resolvedOptions.global && resolvedOptions.packageManager.majorVersion === "1" ? "global" : "",
		...getWorkspaceArgs(resolvedOptions),
		"remove",
		resolvedOptions.dev ? "-D" : "",
		resolvedOptions.global ? "-g" : "",
		...names
	] : [
		resolvedOptions.packageManager.name === "npm" ? "uninstall" : "remove",
		...getWorkspaceArgs(resolvedOptions),
		resolvedOptions.dev ? "-D" : "",
		resolvedOptions.global ? "-g" : "",
		...names
	]).filter(Boolean);
	if (!resolvedOptions.dry) await executeCommand(resolvedOptions.packageManager.command, args, {
		cwd: resolvedOptions.cwd,
		silent: resolvedOptions.silent,
		corepack: resolvedOptions.corepack
	});
	return { exec: {
		command: resolvedOptions.packageManager.command,
		args
	} };
}
async function dedupeDependencies(options = {}) {
	const resolvedOptions = await resolveOperationOptions(options);
	const isSupported = !["bun", "deno"].includes(resolvedOptions.packageManager.name);
	if (options.recreateLockfile ?? !isSupported) {
		const lockfiles = Array.isArray(resolvedOptions.packageManager.lockFile) ? resolvedOptions.packageManager.lockFile : [resolvedOptions.packageManager.lockFile];
		for (const lockfile of lockfiles) if (lockfile) fs.rmSync(resolve(resolvedOptions.cwd, lockfile), { force: true });
		return await installDependencies(resolvedOptions);
	}
	if (isSupported) {
		const isyarnv1 = resolvedOptions.packageManager.name === "yarn" && resolvedOptions.packageManager.majorVersion === "1";
		if (!resolvedOptions.dry) await executeCommand(resolvedOptions.packageManager.command, [isyarnv1 ? "install" : "dedupe"], {
			cwd: resolvedOptions.cwd,
			silent: resolvedOptions.silent,
			corepack: resolvedOptions.corepack
		});
		return { exec: {
			command: resolvedOptions.packageManager.command,
			args: [isyarnv1 ? "install" : "dedupe"]
		} };
	}
	throw new Error(`Deduplication is not supported for ${resolvedOptions.packageManager.name}`);
}
async function runScript(name, options = {}) {
	const resolvedOptions = await resolveOperationOptions(options);
	const args = [
		resolvedOptions.packageManager.name === "deno" ? "task" : "run",
		name,
		...options.args || []
	];
	if (!resolvedOptions.dry) await executeCommand(resolvedOptions.packageManager.command, args, {
		cwd: resolvedOptions.cwd,
		env: resolvedOptions.env,
		silent: resolvedOptions.silent,
		corepack: resolvedOptions.corepack
	});
	return { exec: {
		command: resolvedOptions.packageManager.command,
		args
	} };
}
const operationArgs = {
	cwd: {
		type: "string",
		description: "Current working directory"
	},
	workspace: {
		type: "boolean",
		description: "Add to workspace"
	},
	silent: {
		type: "boolean",
		description: "Run in silent mode"
	},
	corepack: {
		type: "boolean",
		default: true,
		description: "Use corepack"
	},
	dry: {
		type: "boolean",
		description: "Run in dry run mode (does not execute commands)"
	}
};
const install = defineCommand({
	meta: { description: "Install dependencies" },
	args: {
		...operationArgs,
		name: {
			type: "positional",
			description: "Dependency name",
			required: false
		},
		dev: {
			type: "boolean",
			alias: "D",
			description: "Add as dev dependency"
		},
		global: {
			type: "boolean",
			alias: "g",
			description: "Add globally"
		},
		"frozen-lockfile": {
			type: "boolean",
			description: "Install dependencies with frozen lock file"
		},
		"install-peer-dependencies": {
			type: "boolean",
			description: "Also install peer dependencies"
		}
	},
	run: async ({ args }) => {
		handleRes(await (args._.length > 0 ? addDependency(args._, args) : installDependencies(args)), args);
	}
});
const remove = defineCommand({
	meta: { description: "Remove dependencies" },
	args: {
		name: {
			type: "positional",
			description: "Dependency name",
			required: true
		},
		...operationArgs
	},
	run: async ({ args }) => {
		handleRes(await removeDependency(args._, args), args);
	}
});
const detect = defineCommand({
	meta: { description: "Detect the current package manager" },
	args: { cwd: {
		type: "string",
		description: "Current working directory"
	} },
	run: async ({ args }) => {
		const cwd = resolve(args.cwd || ".");
		const packageManager = await detectPackageManager(cwd);
		if (packageManager?.warnings) for (const warning of packageManager.warnings) console.warn(warning);
		if (!packageManager) {
			console.error(`Cannot detect package manager in "${cwd}"`);
			return process.exit(1);
		}
		console.log(`Detected package manager in "${cwd}": "${packageManager.name}@${packageManager.version}"`);
	}
});
const dedupe = defineCommand({
	meta: { description: "Dedupe dependencies" },
	args: {
		cwd: {
			type: "string",
			description: "Current working directory"
		},
		silent: {
			type: "boolean",
			description: "Run in silent mode"
		},
		recreateLockFile: {
			type: "boolean",
			description: "Recreate lock file"
		}
	},
	run: async ({ args }) => {
		handleRes(await dedupeDependencies(args), args);
	}
});
const run = defineCommand({
	meta: { description: "Run script" },
	args: {
		name: {
			type: "positional",
			description: "Script name",
			required: true
		},
		...operationArgs
	},
	run: async ({ args }) => {
		handleRes(await runScript(args.name, {
			...args,
			args: args._.slice(1)
		}), args);
	}
});
runMain(defineCommand({
	meta: {
		name,
		version,
		description
	},
	subCommands: {
		install,
		i: install,
		add: install,
		remove,
		rm: remove,
		uninstall: remove,
		un: remove,
		detect,
		dedupe,
		run
	}
}));
function handleRes(result, args) {
	if (args.dry && !args.silent) console.log(`${result.exec?.command} ${result.exec?.args.join(" ")}`);
}
export {};
