//#region ../nuxi/src/commands/_shared.ts
const cwdArgs = { cwd: {
	type: "string",
	description: "Specify the working directory",
	valueHint: "directory",
	default: "."
} };
const logLevelArgs = { logLevel: {
	type: "string",
	description: "Specify build-time log level",
	valueHint: "silent|info|verbose"
} };
const envNameArgs = { envName: {
	type: "string",
	description: "The environment to use when resolving configuration overrides (default is `production` when building, and `development` when running the dev server)"
} };
const dotEnvArgs = { dotenv: {
	type: "string",
	description: "Path to `.env` file to load, relative to the root directory"
} };
const extendsArgs = { extends: {
	type: "string",
	description: "Extend from a Nuxt layer",
	valueHint: "layer-name",
	alias: ["e"]
} };
const profileArgs = { profile: {
	type: "string",
	description: "Profile performance. Use --profile for CPU only, --profile=verbose for full report.",
	default: void 0,
	valueHint: "verbose"
} };
const legacyRootDirArgs = {
	cwd: {
		...cwdArgs.cwd,
		description: "Specify the working directory, this takes precedence over ROOTDIR (default: `.`)",
		default: void 0
	},
	rootDir: {
		type: "positional",
		description: "Specifies the working directory (default: `.`)",
		required: false,
		default: "."
	}
};

//#endregion
export { legacyRootDirArgs as a, extendsArgs as i, dotEnvArgs as n, logLevelArgs as o, envNameArgs as r, profileArgs as s, cwdArgs as t };