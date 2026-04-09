import { a as legacyRootDirArgs, n as dotEnvArgs, o as logLevelArgs, r as envNameArgs, t as cwdArgs } from "./_shared-BsGoKfo3.mjs";
import process from "node:process";
import { defineCommand } from "citty";
import { isTest } from "std-env";
import { resolve } from "pathe";

//#region ../nuxi/src/commands/dev-child.ts
var dev_child_default = defineCommand({
	meta: {
		name: "_dev",
		description: "Run Nuxt development server (internal command to start child process)"
	},
	args: {
		...cwdArgs,
		...logLevelArgs,
		...envNameArgs,
		...dotEnvArgs,
		...legacyRootDirArgs,
		clear: {
			type: "boolean",
			description: "Clear console on restart",
			negativeDescription: "Disable clear console on restart"
		}
	},
	async run(ctx) {
		if (!process.send && !isTest) console.warn("`nuxi _dev` is an internal command and should not be used directly. Please use `nuxi dev` instead.");
		const cwd = resolve(ctx.args.cwd || ctx.args.rootDir);
		const { initialize } = await import("./dev-DmuOeJjt.mjs");
		await initialize({
			cwd,
			args: ctx.args
		}, ctx);
	}
});

//#endregion
export { dev_child_default as default };