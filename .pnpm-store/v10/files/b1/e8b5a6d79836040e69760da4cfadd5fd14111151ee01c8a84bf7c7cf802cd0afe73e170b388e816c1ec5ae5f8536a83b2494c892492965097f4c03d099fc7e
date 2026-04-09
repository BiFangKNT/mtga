import { a as legacyRootDirArgs, i as extendsArgs, n as dotEnvArgs, o as logLevelArgs, r as envNameArgs, s as profileArgs, t as cwdArgs } from "./_shared-BsGoKfo3.mjs";
import { n as logger, t as debug } from "./logger-B4ge7MhP.mjs";
import "./env-BRiVSJMz.mjs";
import "./ascii-AoH-yOf6.mjs";
import "./profile-q-JV7Qxl.mjs";
import { t as initialize } from "./dev-D5McAnmo.mjs";
import "./kit-DUlGqV3Z.mjs";
import "./versions-Bg99eDSc.mjs";
import "./banner-C2vxTb-6.mjs";
import "./fs-B8DrLsZ2.mjs";
import "./nuxt-CsZm8Jhw.mjs";
import process from "node:process";
import { defineCommand } from "citty";
import { colors } from "consola/utils";
import { isBun, isDeno, isTest } from "std-env";
import { resolve } from "pathe";
import { satisfies } from "semver";
import { getArgs, parseArgs } from "listhen/cli";
import { fork } from "node:child_process";

//#region ../nuxi/src/dev/pool.ts
var ForkPool = class {
	pool = [];
	poolSize;
	rawArgs;
	listenOverrides;
	warming = false;
	constructor(options) {
		this.rawArgs = options.rawArgs;
		this.poolSize = options.poolSize ?? 2;
		this.listenOverrides = options.listenOverrides;
		for (const signal of [
			"exit",
			"SIGTERM",
			"SIGINT",
			"SIGQUIT"
		]) process.once(signal, () => {
			this.killAll(signal === "exit" ? 0 : signal);
		});
	}
	startWarming() {
		if (this.warming) return;
		this.warming = true;
		for (let i = 0; i < this.poolSize; i++) this.warmFork();
	}
	async getFork(context, onMessage) {
		const readyFork = this.pool.find((f) => f.state === "ready");
		if (readyFork) {
			readyFork.state = "active";
			if (onMessage) this.attachMessageHandler(readyFork.process, onMessage);
			await this.sendContext(readyFork.process, context);
			if (this.warming) this.warmFork();
			return () => this.killFork(readyFork);
		}
		const warmingFork = this.pool.find((f) => f.state === "warming");
		if (warmingFork) {
			await warmingFork.ready;
			warmingFork.state = "active";
			if (onMessage) this.attachMessageHandler(warmingFork.process, onMessage);
			await this.sendContext(warmingFork.process, context);
			if (this.warming) this.warmFork();
			return () => this.killFork(warmingFork);
		}
		debug("No pre-warmed forks available, starting cold fork");
		const coldFork = this.createFork();
		await coldFork.ready;
		coldFork.state = "active";
		if (onMessage) this.attachMessageHandler(coldFork.process, onMessage);
		await this.sendContext(coldFork.process, context);
		return () => this.killFork(coldFork);
	}
	attachMessageHandler(childProc, onMessage) {
		childProc.on("message", (message) => {
			if (message.type !== "nuxt:internal:dev:fork-ready") onMessage(message);
		});
	}
	warmFork() {
		const fork = this.createFork();
		fork.ready.then(() => {
			if (fork.state === "warming") fork.state = "ready";
		}).catch(() => {
			this.removeFork(fork);
		});
		this.pool.push(fork);
	}
	createFork() {
		const childProc = fork(globalThis.__nuxt_cli__.devEntry, this.rawArgs, {
			execArgv: ["--enable-source-maps", process.argv.find((a) => a.includes("--inspect"))].filter(Boolean),
			env: {
				...process.env,
				__NUXT__FORK: "true"
			}
		});
		let readyResolve;
		let readyReject;
		const pooledFork = {
			process: childProc,
			ready: new Promise((resolve, reject) => {
				readyResolve = resolve;
				readyReject = reject;
			}),
			state: "warming"
		};
		childProc.on("message", (message) => {
			if (message.type === "nuxt:internal:dev:fork-ready") readyResolve();
		});
		childProc.on("error", (err) => {
			readyReject(err);
			this.removeFork(pooledFork);
		});
		childProc.on("close", (errorCode) => {
			if (pooledFork.state === "active" && errorCode) process.exit(errorCode);
			this.removeFork(pooledFork);
		});
		return pooledFork;
	}
	async sendContext(childProc, context) {
		childProc.send({
			type: "nuxt:internal:dev:context",
			listenOverrides: this.listenOverrides,
			context
		});
	}
	killFork(fork, signal = "SIGTERM") {
		fork.state = "dead";
		if (fork.process) fork.process.kill(signal === 0 && isDeno ? "SIGTERM" : signal);
		this.removeFork(fork);
	}
	removeFork(fork) {
		const index = this.pool.indexOf(fork);
		if (index > -1) this.pool.splice(index, 1);
	}
	killAll(signal) {
		for (const fork of this.pool) this.killFork(fork, signal);
	}
	getStats() {
		return {
			total: this.pool.length,
			warming: this.pool.filter((f) => f.state === "warming").length,
			ready: this.pool.filter((f) => f.state === "ready").length,
			active: this.pool.filter((f) => f.state === "active").length
		};
	}
};

//#endregion
//#region ../nuxi/src/commands/dev.ts
const startTime = Date.now();
const forkSupported = !isTest && (!isBun || isBunForkSupported());
const listhenArgs = getArgs();
const command = defineCommand({
	meta: {
		name: "dev",
		description: "Run Nuxt development server"
	},
	args: {
		...cwdArgs,
		...logLevelArgs,
		...dotEnvArgs,
		...legacyRootDirArgs,
		...envNameArgs,
		...extendsArgs,
		clear: {
			type: "boolean",
			description: "Clear console on restart",
			default: false
		},
		fork: {
			type: "boolean",
			description: forkSupported ? "Disable forked mode" : "Enable forked mode",
			negativeDescription: "Disable forked mode",
			default: forkSupported,
			alias: ["f"]
		},
		...listhenArgs,
		port: {
			...listhenArgs.port,
			description: "Port to listen on (default: `NUXT_PORT || NITRO_PORT || PORT || nuxtOptions.devServer.port`)",
			alias: ["p"]
		},
		open: {
			...listhenArgs.open,
			alias: ["o"],
			default: false
		},
		host: {
			...listhenArgs.host,
			alias: ["h"],
			description: "Host to listen on (default: `NUXT_HOST || NITRO_HOST || HOST || nuxtOptions.devServer?.host`)"
		},
		clipboard: {
			...listhenArgs.clipboard,
			default: false
		},
		...profileArgs,
		sslCert: {
			type: "string",
			description: "(DEPRECATED) Use `--https.cert` instead."
		},
		sslKey: {
			type: "string",
			description: "(DEPRECATED) Use `--https.key` instead."
		}
	},
	async run(ctx) {
		const cwd = resolve(ctx.args.cwd || ctx.args.rootDir);
		const listenOverrides = resolveListenOverrides(ctx.args);
		const { listener, close, onRestart, onReady } = await initialize({
			cwd,
			args: ctx.args
		}, {
			data: ctx.data,
			listenOverrides,
			showBanner: true
		});
		if (!ctx.args.fork || ctx.args.profile) return {
			listener,
			close
		};
		const pool = new ForkPool({
			rawArgs: ctx.rawArgs,
			poolSize: 2,
			listenOverrides
		});
		onReady((_address) => {
			pool.startWarming();
			if (startTime) debug(`Dev server ready for connections in ${Date.now() - startTime}ms`);
		});
		let cleanupCurrentFork;
		async function restartWithFork() {
			const context = {
				cwd,
				args: ctx.args
			};
			cleanupCurrentFork?.();
			cleanupCurrentFork = await pool.getFork(context, (message) => {
				if (message.type === "nuxt:internal:dev:ready") {
					if (startTime) debug(`Dev server ready for connections in ${Date.now() - startTime}ms`);
				} else if (message.type === "nuxt:internal:dev:restart") restartWithFork();
				else if (message.type === "nuxt:internal:dev:rejection") {
					logger.info(`Restarting Nuxt due to error: ${colors.cyan(message.message)}`);
					restartWithFork();
				}
			});
		}
		onRestart(async () => {
			await close();
			await restartWithFork();
		});
		return { async close() {
			cleanupCurrentFork?.();
			await Promise.all([listener.close(), close()]);
		} };
	}
});
function resolveListenOverrides(args) {
	if (process.env._PORT) return {
		port: process.env._PORT || 0,
		hostname: "127.0.0.1",
		showURL: false
	};
	const options = parseArgs({
		...args,
		"host": args.host || process.env.NUXT_HOST || process.env.NITRO_HOST || process.env.HOST,
		"port": args.port || process.env.NUXT_PORT || process.env.NITRO_PORT || process.env.PORT,
		"https": args.https !== false && args.https !== "false",
		"https.cert": args["https.cert"] || args.sslCert || process.env.NUXT_SSL_CERT || process.env.NITRO_SSL_CERT,
		"https.key": args["https.key"] || args.sslKey || process.env.NUXT_SSL_KEY || process.env.NITRO_SSL_KEY
	});
	return {
		...options,
		_https: args.https,
		get https() {
			const httpsArg = this._https;
			if (httpsArg === false || httpsArg === "false") return false;
			return httpsArg ? options.https : false;
		}
	};
}
function isBunForkSupported() {
	const bunVersion = globalThis.Bun.version;
	return satisfies(bunVersion, ">=1.2");
}

//#endregion
export { command as default };