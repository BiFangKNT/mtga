import { t as cwdArgs } from "./_shared-BsGoKfo3.mjs";
import { n as logger } from "./logger-B4ge7MhP.mjs";
import { t as templateNames } from "./templates-wxuD_F_w.mjs";
import { t as templates } from "./templates-BQDUIkuM.mjs";
import { resolve } from "node:path";
import process from "node:process";
import { defineCommand, runCommand as runCommand$1, runMain as runMain$1 } from "citty";
import { colors } from "consola/utils";
import { provider } from "std-env";
import { consola } from "consola";
import { fileURLToPath } from "node:url";
import tab from "@bomb.sh/tab/citty";

//#region ../nuxi/src/commands/index.ts
const _rDefault = (r) => r.default || r;
const commands = {
	"add": () => import("./add-D-RRzz1Y.mjs").then((n) => n.n).then(_rDefault),
	"add-template": () => import("./add-template-B0_8lFIJ.mjs").then(_rDefault),
	"analyze": () => import("./analyze-C512gBX4.mjs").then(_rDefault),
	"build": () => import("./build-CIg9T7rh.mjs").then(_rDefault),
	"cleanup": () => import("./cleanup-B1pvEjaJ.mjs").then(_rDefault),
	"_dev": () => import("./dev-child-BTslI2Ui.mjs").then(_rDefault),
	"dev": () => import("./dev-CY-a7lb7.mjs").then(_rDefault),
	"devtools": () => import("./devtools-BFJLyinx.mjs").then(_rDefault),
	"generate": () => import("./generate-Bs-I-Nn8.mjs").then(_rDefault),
	"info": () => import("./info-C2RRE7Hj.mjs").then(_rDefault),
	"init": () => import("./init-3K6qv8Y1.mjs").then(_rDefault),
	"module": () => import("./module-BOwFh5iR.mjs").then(_rDefault),
	"prepare": () => import("./prepare-etx17Cow.mjs").then((n) => n.n).then(_rDefault),
	"preview": () => import("./preview-Dpml-raz.mjs").then(_rDefault),
	"start": () => import("./preview-Dpml-raz.mjs").then(_rDefault),
	"test": () => import("./test-3ArLMqkP.mjs").then(_rDefault),
	"typecheck": () => import("./typecheck-DzNAMeid.mjs").then(_rDefault),
	"upgrade": () => import("./upgrade-CUwAlsGk.mjs").then(_rDefault)
};

//#endregion
//#region ../nuxi/src/utils/console.ts
function wrapReporter(reporter) {
	return { log(logObj, ctx) {
		if (!logObj.args || !logObj.args.length) return;
		const msg = logObj.args[0];
		if (typeof msg === "string" && !process.env.DEBUG) {
			if (msg.startsWith("[Vue Router warn]: No match found for location with path")) return;
			if (msg.includes("ExperimentalWarning: The Fetch API is an experimental feature")) return;
			if (msg.startsWith("Sourcemap") && msg.includes("node_modules")) return;
		}
		return reporter.log(logObj, ctx);
	} };
}
function setupGlobalConsole(opts = {}) {
	consola.options.reporters = consola.options.reporters.map(wrapReporter);
	if (opts.dev) consola.wrapAll();
	else consola.wrapConsole();
	process.on("unhandledRejection", (err) => consola.error("[unhandledRejection]", err));
	process.on("uncaughtException", (err) => consola.error("[uncaughtException]", err));
}

//#endregion
//#region ../nuxi/src/utils/engines.ts
async function checkEngines() {
	const satisfies = await import("semver/functions/satisfies.js").then((r) => r.default || r);
	const currentNode = process.versions.node;
	const nodeRange = ">= 18.0.0";
	if (!satisfies(currentNode, nodeRange)) logger.warn(`Current version of Node.js (${colors.cyan(currentNode)}) is unsupported and might cause issues.\n       Please upgrade to a compatible version ${colors.cyan(nodeRange)}.`);
}

//#endregion
//#region package.json
var name = "@nuxt/cli";
var version = "3.34.0";
var description = "Nuxt CLI";

//#endregion
//#region ../nuxi/src/data/nitro-presets.ts
const nitroPresets = [
	"alwaysdata",
	"aws-amplify",
	"aws-lambda",
	"azure-functions",
	"azure-swa",
	"bun",
	"cleavr",
	"cli",
	"cloudflare-dev",
	"cloudflare-durable",
	"cloudflare-module",
	"cloudflare-module-legacy",
	"cloudflare-pages",
	"cloudflare-pages-static",
	"cloudflare-worker",
	"deno-deploy",
	"deno-server",
	"deno-server-legacy",
	"digital-ocean",
	"edgio",
	"firebase",
	"firebase-app-hosting",
	"flight-control",
	"genezio",
	"github-pages",
	"gitlab-pages",
	"heroku",
	"iis-handler",
	"iis-node",
	"koyeb",
	"netlify",
	"netlify-builder",
	"netlify-edge",
	"netlify-legacy",
	"netlify-static",
	"node-cluster",
	"node-listener",
	"node-server",
	"platform-sh",
	"render-com",
	"service-worker",
	"static",
	"stormkit",
	"vercel",
	"vercel-edge",
	"vercel-static",
	"winterjs",
	"zeabur",
	"zeabur-static",
	"zerops",
	"zerops-static"
];

//#endregion
//#region ../nuxi/src/completions.ts
async function initCompletions(command) {
	const completion = await tab(command);
	const devCommand = completion.commands.get("dev");
	if (devCommand) {
		const portOption = devCommand.options.get("port");
		if (portOption) portOption.handler = (complete) => {
			complete("3000", "Default development port");
			complete("3001", "Alternative port");
			complete("8080", "Common alternative port");
		};
		const hostOption = devCommand.options.get("host");
		if (hostOption) hostOption.handler = (complete) => {
			complete("localhost", "Local development");
			complete("0.0.0.0", "Listen on all interfaces");
			complete("127.0.0.1", "Loopback address");
		};
	}
	const buildCommand = completion.commands.get("build");
	if (buildCommand) {
		const presetOption = buildCommand.options.get("preset");
		if (presetOption) presetOption.handler = (complete) => {
			for (const preset of nitroPresets) complete(preset, "");
		};
	}
	const initCommand = completion.commands.get("init");
	if (initCommand) {
		const templateOption = initCommand.options.get("template");
		if (templateOption) templateOption.handler = (complete) => {
			for (const template in templates) complete(template, templates[template]?.description || "");
		};
	}
	const addCommand = completion.commands.get("add");
	if (addCommand) {
		const cwdOption = addCommand.options.get("cwd");
		if (cwdOption) cwdOption.handler = (complete) => {
			complete(".", "Current directory");
		};
	}
	for (const cmdName of [
		"dev",
		"build",
		"generate",
		"preview",
		"prepare",
		"init"
	]) {
		const cmd = completion.commands.get(cmdName);
		if (cmd) {
			const logLevelOption = cmd.options.get("logLevel");
			if (logLevelOption) logLevelOption.handler = (complete) => {
				complete("silent", "No logs");
				complete("info", "Standard logging");
				complete("verbose", "Detailed logging");
			};
		}
	}
	return completion;
}

//#endregion
//#region src/run.ts
globalThis.__nuxt_cli__ = globalThis.__nuxt_cli__ || {
	startTime: Date.now(),
	entry: fileURLToPath(new URL("../../bin/nuxi.mjs", import.meta.url)),
	devEntry: fileURLToPath(new URL("../dev/index.mjs", import.meta.url))
};
async function runMain() {
	await initCompletions(main);
	return runMain$1(main);
}
async function runCommand(name, argv = process.argv.slice(2), data = {}) {
	argv.push("--no-clear");
	if (!(name in commands)) throw new Error(`Invalid command ${name}`);
	return await runCommand$1(await commands[name](), {
		rawArgs: argv,
		data: { overrides: data.overrides || {} }
	});
}

//#endregion
//#region src/main.ts
const _main = defineCommand({
	meta: {
		name: name.endsWith("nightly") ? name : "nuxi",
		version,
		description
	},
	args: {
		...cwdArgs,
		command: {
			type: "positional",
			required: false
		}
	},
	subCommands: commands,
	async setup(ctx) {
		const command = ctx.args._[0];
		setupGlobalConsole({ dev: command === "dev" });
		let backgroundTasks;
		if (command !== "_dev" && provider !== "stackblitz") backgroundTasks = Promise.all([checkEngines()]).catch((err) => logger.error(String(err)));
		if (command === "init") await backgroundTasks;
		if (command === "add" && ctx.rawArgs[1] && templateNames.includes(ctx.rawArgs[1])) {
			logger.warn(`${colors.yellow("Deprecated:")} Using ${colors.cyan("nuxt add <template> <name>")} is deprecated.`);
			logger.info(`Please use ${colors.cyan("nuxt add-template <template> <name>")} instead.`);
			await runCommand("add-template", [...ctx.rawArgs.slice(1)]).catch((err) => {
				console.error(err.message);
				process.exit(1);
			});
			process.exit(0);
		}
		if (ctx.args.command && !(ctx.args.command in commands)) {
			const cwd = resolve(ctx.args.cwd);
			try {
				const { x } = await import("tinyexec");
				await x(`nuxt-${ctx.args.command}`, ctx.rawArgs.slice(1), {
					nodeOptions: {
						stdio: "inherit",
						cwd
					},
					throwOnError: true
				});
			} catch (err) {
				if (err instanceof Error && "code" in err && err.code === "ENOENT") return;
			}
			process.exit();
		}
	}
});
const main = _main;

//#endregion
export { main, runCommand, runMain };