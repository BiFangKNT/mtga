#!/usr/bin/env node
import { t as C } from "./dist-B2ebky9O.mjs";
import { t as ViteNodeServer } from "./server-Bk_vRgMj.mjs";
import "./constants-DRkacFwN.mjs";
import { h as toArray } from "./utils-ExLpYVUV.mjs";
import { n as installSourcemapsSupport } from "./source-map-CysB5F9m.mjs";
import { r as ViteNodeRunner } from "./client-C7yCjfvf.mjs";
import { r as handleMessage, s as viteNodeHmrPlugin, t as createHotContext } from "./hmr-qEG3qSgW.mjs";
import process from "node:process";
import { createServer, loadEnv, version } from "vite";
import { resolve } from "node:path";
import cac from "cac";

//#region package.json
var version$1 = "5.3.0";

//#endregion
//#region src/cli.ts
const cli = cac("vite-node");
cli.option("-r, --root <path>", "Use specified root directory").option("-c, --config <path>", "Use specified config file").option("-m, --mode <mode>", "Set env mode").option("-w, --watch", "Restart on file changes, similar to \"nodemon\"").option("--inspect", "Enable Node.js inspector").option("--inspect-addr [host:port]", "Enable Node.js inspector with specified address").option("--script", "Use vite-node as a script runner").option("--options <options>", "Use specified Vite server options").option("-v, --version", "Output the version number").option("-h, --help", "Display help for command");
cli.command("[...files]").allowUnknownOptions().action(run);
cli.parse(process.argv, { run: false });
if (cli.args.length === 0) cli.runMatchedCommand();
else {
	const i = cli.rawArgs.indexOf(cli.args[0]) + 1;
	const scriptArgs = cli.rawArgs.slice(i).filter((it) => it !== "--");
	const executeArgs = [
		...cli.rawArgs.slice(0, i),
		"--",
		...scriptArgs
	];
	cli.parse(executeArgs);
}
async function run(files, options = {}) {
	if (options.inspect || options.inspectAddr) {
		const { open } = await import("node:inspector");
		const [host, port] = options.inspectAddr?.split(":") || ["127.0.0.1", "9229"];
		open(Number(port), host, false);
	}
	if (options.script) {
		files = [files[0]];
		options = {};
		process.argv = [
			process.argv[0],
			resolve(files[0]),
			...process.argv.slice(2).filter((arg) => arg !== "--script" && arg !== files[0])
		];
	} else process.argv = [...process.argv.slice(0, 2), ...options["--"] || []];
	if (options.version) {
		cli.version(version$1);
		cli.outputVersion();
		process.exit(0);
	}
	if (options.help) {
		cli.version(version$1).outputHelp();
		process.exit(0);
	}
	if (!files.length) {
		console.error(C.red("No files specified."));
		cli.version(version$1).outputHelp();
		process.exit(1);
	}
	const serverOptions = options.options ? parseServerOptions(options.options) : {};
	const server = await createServer({
		logLevel: "error",
		configFile: options.config,
		root: options.root,
		mode: options.mode,
		server: {
			hmr: !!options.watch,
			watch: options.watch ? void 0 : null
		},
		plugins: [options.watch && viteNodeHmrPlugin()]
	});
	if (Number(version.split(".")[0]) < 6) await server.pluginContainer.buildStart({});
	else await server.environments.client.pluginContainer.buildStart({});
	const env = loadEnv(server.config.mode, server.config.envDir, "");
	for (const key in env) process.env[key] ??= env[key];
	const node = new ViteNodeServer(server, serverOptions);
	installSourcemapsSupport({ getSourceMap: (source) => node.getSourceMap(source) });
	const runner = new ViteNodeRunner({
		root: server.config.root,
		base: server.config.base,
		fetchModule(id) {
			return node.fetchModule(id);
		},
		resolveId(id, importer) {
			return node.resolveId(id, importer);
		},
		createHotContext(runner$1, url) {
			return createHotContext(runner$1, server.emitter, files, url);
		}
	});
	await runner.executeId("/@vite/env");
	for (const file of files) await runner.executeFile(file);
	if (!options.watch) await server.close();
	server.emitter?.on("message", (payload) => {
		handleMessage(runner, server.emitter, files, payload);
	});
	if (options.watch) {
		process.on("uncaughtException", (err) => {
			console.error(C.red("[vite-node] Failed to execute file: \n"), err);
		});
		if (process.env.VITE_TEST_WATCHER_DEBUG) {
			const nodePath = await import("node:path");
			async function waitForWatched(files$1) {
				while (!files$1.every((file) => isWatched(file))) await new Promise((resolve$1) => setTimeout(resolve$1, 20));
			}
			function isWatched(file) {
				const watched = server.watcher.getWatched();
				const resolved = nodePath.resolve(file);
				const dir = nodePath.dirname(resolved);
				const base = nodePath.basename(resolved);
				return watched[dir]?.includes(base);
			}
			await waitForWatched(files);
			console.log("[debug] watcher is ready");
		}
	}
}
function parseServerOptions(serverOptions) {
	const inlineOptions = serverOptions.deps?.inline === true ? true : toArray(serverOptions.deps?.inline);
	return {
		...serverOptions,
		deps: {
			...serverOptions.deps,
			inlineFiles: toArray(serverOptions.deps?.inlineFiles),
			inline: inlineOptions !== true ? inlineOptions.map((dep) => {
				return dep.startsWith("/") && dep.endsWith("/") ? new RegExp(dep) : dep;
			}) : true,
			external: toArray(serverOptions.deps?.external).map((dep) => {
				return dep.startsWith("/") && dep.endsWith("/") ? new RegExp(dep) : dep;
			}),
			moduleDirectories: serverOptions.deps?.moduleDirectories ? toArray(serverOptions.deps?.moduleDirectories) : void 0
		},
		transformMode: {
			...serverOptions.transformMode,
			ssr: toArray(serverOptions.transformMode?.ssr).map((dep) => new RegExp(dep)),
			web: toArray(serverOptions.transformMode?.web).map((dep) => new RegExp(dep))
		}
	};
}

//#endregion
export {  };