#!/usr/bin/env node
import { i as relative } from "./_chunks/libs/nypm.mjs";
import { r as startShell, t as downloadTemplate } from "./_chunks/giget.mjs";
import { n as runMain, t as defineCommand } from "./_chunks/libs/citty.mjs";
//#endregion
//#region src/cli.ts
runMain(defineCommand({
	meta: {
		name: "giget",
		version: "3.1.2",
		description: "Download templates and git repositories with pleasure!"
	},
	args: {
		template: {
			type: "positional",
			required: true,
			description: "Template name or a URI describing provider, repository, subdir, and branch/ref"
		},
		dir: {
			type: "positional",
			description: "A relative or absolute path where to extract the template",
			required: false
		},
		auth: {
			type: "string",
			description: "Custom Authorization token to use for downloading template. (Can be overridden with `GIGET_AUTH` environment variable)"
		},
		cwd: {
			type: "string",
			description: "Set current working directory to resolve dirs relative to it"
		},
		force: {
			type: "boolean",
			description: "Clone to existing directory even if exists"
		},
		forceClean: {
			type: "boolean",
			description: "Remove any existing directory or file recursively before cloning"
		},
		offline: {
			type: "boolean",
			description: "Do not attempt to download and use cached version"
		},
		preferOffline: {
			type: "boolean",
			description: "Use cache if exists otherwise try to download"
		},
		shell: {
			type: "boolean",
			description: "Open a new shell with the current working directory set to the cloned directory (experimental)"
		},
		install: {
			type: "boolean",
			description: "Install dependencies after cloning"
		},
		verbose: {
			type: "boolean",
			description: "Show verbose debugging info"
		}
	},
	run: async ({ args }) => {
		if (args.verbose) process.env.DEBUG = process.env.DEBUG || "true";
		let r;
		try {
			r = await downloadTemplate(args.template, {
				dir: args.dir,
				force: args.force,
				forceClean: args.forceClean,
				offline: args.offline,
				preferOffline: args.preferOffline,
				auth: args.auth,
				install: args.install
			});
		} catch (error) {
			if (args.verbose) console.error(error);
			else {
				const message = error instanceof Error ? error.message : `Failed to download ${args.template}: unknown error`;
				console.error(message);
			}
			process.exitCode = 1;
			return;
		}
		const _from = r.name || r.url;
		const _to = relative(process.cwd(), r.dir) || "./";
		console.log(`✨ Successfully cloned \`${_from}\` to \`${_to}\`\n`);
		if (args.shell) startShell(r.dir);
	}
}));
//#endregion
export {};
