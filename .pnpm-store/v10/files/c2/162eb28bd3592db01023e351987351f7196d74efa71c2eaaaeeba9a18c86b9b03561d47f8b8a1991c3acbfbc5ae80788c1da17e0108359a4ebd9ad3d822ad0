import { a as legacyRootDirArgs, i as extendsArgs, n as dotEnvArgs, o as logLevelArgs, t as cwdArgs } from "./_shared-BsGoKfo3.mjs";
import { t as loadKit } from "./kit-DUlGqV3Z.mjs";
import process from "node:process";
import { defineCommand } from "citty";
import { isBun } from "std-env";
import { resolve } from "pathe";
import { resolveModulePath } from "exsolve";
import { readTSConfig } from "pkg-types";
import { x } from "tinyexec";

//#region ../nuxi/src/commands/typecheck.ts
var typecheck_default = defineCommand({
	meta: {
		name: "typecheck",
		description: "Runs `vue-tsc` to check types throughout your app."
	},
	args: {
		...cwdArgs,
		...logLevelArgs,
		...dotEnvArgs,
		...extendsArgs,
		...legacyRootDirArgs
	},
	async run(ctx) {
		process.env.NODE_ENV = process.env.NODE_ENV || "production";
		const cwd = resolve(ctx.args.cwd || ctx.args.rootDir);
		const [supportsProjects, resolvedTypeScript, resolvedVueTsc] = await Promise.all([
			readTSConfig(cwd).then((r) => !!r.references?.length),
			resolveModulePath("typescript", { try: true }),
			resolveModulePath("vue-tsc/bin/vue-tsc.js", { try: true }),
			writeTypes(cwd, ctx.args.dotenv, ctx.args.logLevel, {
				...ctx.data?.overrides,
				...ctx.args.extends && { extends: ctx.args.extends }
			})
		]);
		const typeCheckArgs = supportsProjects ? ["-b", "--noEmit"] : ["--noEmit"];
		if (resolvedTypeScript && resolvedVueTsc) return await x(resolvedVueTsc, typeCheckArgs, {
			throwOnError: true,
			nodeOptions: {
				stdio: "inherit",
				cwd
			}
		});
		if (isBun) {
			await x("bun", [
				"install",
				"typescript",
				"vue-tsc",
				"--global",
				"--silent"
			], {
				throwOnError: true,
				nodeOptions: {
					stdio: "inherit",
					cwd
				}
			});
			return await x("bunx", ["vue-tsc", ...typeCheckArgs], {
				throwOnError: true,
				nodeOptions: {
					stdio: "inherit",
					cwd
				}
			});
		}
		await x("npx", [
			"-p",
			"vue-tsc",
			"-p",
			"typescript",
			"vue-tsc",
			...typeCheckArgs
		], {
			throwOnError: true,
			nodeOptions: {
				stdio: "inherit",
				cwd
			}
		});
	}
});
async function writeTypes(cwd, dotenv, logLevel, overrides) {
	const { loadNuxt, buildNuxt, writeTypes } = await loadKit(cwd);
	const nuxt = await loadNuxt({
		cwd,
		dotenv: {
			cwd,
			fileName: dotenv
		},
		overrides: {
			_prepare: true,
			logLevel,
			...overrides
		}
	});
	await writeTypes(nuxt);
	await buildNuxt(nuxt);
	await nuxt.close();
}

//#endregion
export { typecheck_default as default };