import { a as legacyRootDirArgs, i as extendsArgs, n as dotEnvArgs, o as logLevelArgs, r as envNameArgs, s as profileArgs, t as cwdArgs } from "./_shared-BsGoKfo3.mjs";
import "./logger-B4ge7MhP.mjs";
import "./env-BRiVSJMz.mjs";
import "./ascii-AoH-yOf6.mjs";
import "./profile-q-JV7Qxl.mjs";
import "./kit-DUlGqV3Z.mjs";
import "./versions-Bg99eDSc.mjs";
import "./banner-C2vxTb-6.mjs";
import "./fs-B8DrLsZ2.mjs";
import { t as build_default } from "./dev-DmuOeJjt.mjs";
import { defineCommand } from "citty";

//#region ../nuxi/src/commands/generate.ts
var generate_default = defineCommand({
	meta: {
		name: "generate",
		description: "Build Nuxt and prerender all routes"
	},
	args: {
		...cwdArgs,
		...logLevelArgs,
		preset: {
			type: "string",
			description: "Nitro server preset"
		},
		...dotEnvArgs,
		...envNameArgs,
		...extendsArgs,
		...profileArgs,
		...legacyRootDirArgs
	},
	async run(ctx) {
		ctx.args.prerender = true;
		await build_default.run(ctx);
	}
});

//#endregion
export { generate_default as default };