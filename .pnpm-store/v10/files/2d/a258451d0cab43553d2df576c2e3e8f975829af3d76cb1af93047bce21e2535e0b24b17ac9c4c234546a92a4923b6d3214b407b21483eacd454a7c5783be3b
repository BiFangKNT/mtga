import { a as resolve$1, i as relative, n as basename$1, r as dirname$1 } from "./libs/nypm.mjs";
import { createWriteStream, existsSync, readdirSync, renameSync } from "node:fs";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { PassThrough, Readable, pipeline } from "node:stream";
import { pipeline as pipeline$1 } from "node:stream/promises";
import { spawn, spawnSync } from "node:child_process";
import { homedir, tmpdir } from "node:os";
import { promisify } from "node:util";
import { join } from "node:path";
//#region src/_utils.ts
async function download(url, filePath, options = {}) {
	const infoPath = filePath + ".json";
	const info = JSON.parse(await readFile(infoPath, "utf8").catch(() => "{}"));
	const etag = (await sendFetch(url, {
		method: "HEAD",
		headers: options.headers
	}).catch(() => void 0))?.headers.get("etag");
	if (info.etag === etag && existsSync(filePath)) return;
	if (typeof etag === "string") info.etag = etag;
	const response = await sendFetch(url, { headers: options.headers });
	if (response.status >= 400) throw new Error(`Failed to download ${url}: ${response.status} ${response.statusText}`);
	const stream = createWriteStream(filePath);
	await promisify(pipeline)(response.body, stream);
	await writeFile(infoPath, JSON.stringify(info), "utf8");
}
const inputRegex = /^(?<repo>[-\w.]+\/[-\w.]+)(?<subdir>[^#]+)?(?<ref>#[-\w./@]+)?/;
const expandedInputRegex = /^(?<repo>[-\w.]+(?:\/[-\w.]+)+?)(?:::(?<subdir>[^#]*))?(?<ref>#[-\w./@]+)?$/;
function parseGitURI(input, options) {
	const useExpanded = options?.expandRepo || input.includes("::");
	const m = input.match(useExpanded ? expandedInputRegex : inputRegex)?.groups || {};
	const subdir = useExpanded ? m.subdir ? "/" + m.subdir : "/" : m.subdir || "/";
	return {
		repo: m.repo || "",
		subdir,
		ref: m.ref ? m.ref.slice(1) : "main"
	};
}
function debug(...args) {
	if (process.env.DEBUG) console.debug("[giget]", ...args);
}
async function sendFetch(url, options = {}) {
	if (options.headers?.["sec-fetch-mode"]) options.mode = options.headers["sec-fetch-mode"];
	const res = await fetch(url, {
		...options,
		headers: normalizeHeaders(options.headers)
	}).catch((error) => {
		throw new Error(`Failed to download ${url}: ${error}`, { cause: error });
	});
	if (options.validateStatus && res.status >= 400) throw new Error(`Failed to fetch ${url}: ${res.status} ${res.statusText}`);
	return res;
}
function cacheDirectory() {
	const cacheDir = process.env.XDG_CACHE_HOME ? resolve$1(process.env.XDG_CACHE_HOME, "giget") : resolve$1(homedir(), ".cache/giget");
	if (process.platform === "win32") {
		const windowsCacheDir = resolve$1(tmpdir(), "giget");
		if (!existsSync(windowsCacheDir) && existsSync(cacheDir)) try {
			renameSync(cacheDir, windowsCacheDir);
		} catch {}
		return windowsCacheDir;
	}
	return cacheDir;
}
function normalizeHeaders(headers = {}) {
	const normalized = {};
	for (const [key, value] of Object.entries(headers)) {
		if (!value) continue;
		normalized[key.toLowerCase()] = value;
	}
	return normalized;
}
function currentShell() {
	if (process.env.SHELL) return process.env.SHELL;
	if (process.platform === "win32") return "cmd.exe";
	return "/bin/bash";
}
function startShell(cwd) {
	cwd = resolve$1(cwd);
	const shell = currentShell();
	console.info(`(experimental) Opening shell in ${relative(process.cwd(), cwd)}...`);
	spawnSync(shell, [], {
		cwd,
		shell: true,
		stdio: "inherit"
	});
}
//#endregion
//#region src/git.ts
const git = (input, options) => {
	const parsed = parseGitCloneURI(input);
	return {
		name: parsed.name,
		version: parsed.subdir ? `${parsed.version || "default"}-${parsed.subdir.replaceAll("/", "-")}` : parsed.version,
		tar: ({ auth } = {}) => _cloneAndTar(parsed, auth ?? options.auth)
	};
};
function parseGitCloneURI(input, opts = {}) {
	const cwd = opts.cwd ?? process.cwd();
	let uri = input.replace(/#.*$/, "");
	let pathSubdir;
	if (/^[./]/.test(input)) uri = resolve$1(cwd, uri);
	else if (/^https?:\/\//.test(uri)) {
		const httpMatch = /^(https?:\/\/[^/]+)\/([\w.-]+\/[\w.-]+?)(?:\.git)?(?:\/(.+))?$/.exec(uri);
		if (httpMatch) {
			const [, origin, repo, rest] = httpMatch;
			uri = `${origin}/${repo}`;
			if (rest) pathSubdir = rest;
		}
	} else if (uri.includes("@")) {
		const sshMatch = /^(.*?:[\w.-]+\/[\w.-]+?)(?:\.git)?(?:\/(.+))?$/.exec(uri);
		if (sshMatch) {
			const [, repoUri, rest] = sshMatch;
			uri = repoUri;
			if (rest) pathSubdir = rest;
		}
	} else {
		const hostMap = {
			"github:": "https://github.com/",
			"gh:": "https://github.com/",
			"gitlab:": "https://gitlab.com/",
			"bitbucket:": "https://bitbucket.org/",
			"sourcehut:": "https://git.sr.ht/~"
		};
		const host = /^(.+?:)/.exec(uri)?.at(1);
		if (host && hostMap[host]) uri = uri.replace(host, hostMap[host]);
		else if (!host) uri = `${(process.env.GIGET_GIT_HOST || "https://github.com/").replace(/\/$/, "")}/${uri}`;
		const httpMatch = /^(https?:\/\/[^/]+\/~?[\w.-]+\/[\w.-]+?)(?:\.git)?(?:\/(.+))?$/.exec(uri);
		if (httpMatch) {
			const [, repoUri, rest] = httpMatch;
			uri = repoUri;
			if (rest) pathSubdir = rest;
		}
	}
	const name = uri.replace(/^https?:\/\//, "").replace(/^.+@/, "").replace(/(\.git)?(#.*)?$/, "").replace(/^\W+/, "").replaceAll(/[:/]/g, "-");
	const [version, hashSubdir] = /#(.+)$/.exec(input)?.at(1)?.split(":") ?? [];
	const resolvedVersion = version || void 0;
	const subdir = hashSubdir || pathSubdir;
	return {
		uri,
		name,
		...resolvedVersion && { version: resolvedVersion },
		...subdir && { subdir }
	};
}
async function _cloneAndTar(parsed, token) {
	const tmpDir = await mkdtemp(join(tmpdir(), "giget-git-"));
	if (token && /[\r\n]/.test(token)) throw new Error("Auth token must not contain newline characters");
	const execEnv = {
		...process.env,
		GIT_TERMINAL_PROMPT: "0"
	};
	if (token) {
		execEnv.GIT_CONFIG_COUNT = "1";
		execEnv.GIT_CONFIG_KEY_0 = "http.extraHeader";
		execEnv.GIT_CONFIG_VALUE_0 = `Authorization: Bearer ${token}`;
	}
	const execOpts = {
		env: execEnv,
		timeout: 6e4
	};
	const status = _createStatus();
	const gitExec = (args) => _gitSpawn(args, execOpts, status);
	const gitExecIn = (args) => _gitSpawn(args, {
		...execOpts,
		cwd: tmpDir
	}, status);
	try {
		const cloneArgs = [
			"clone",
			"--progress",
			"--depth",
			"1"
		];
		if (parsed.subdir) cloneArgs.push("--filter=blob:none", "--sparse", "--no-checkout");
		if (parsed.version) cloneArgs.push("--branch", parsed.version);
		cloneArgs.push("--", parsed.uri, tmpDir);
		try {
			status.update("Cloning...");
			await gitExec(cloneArgs);
			status.update("Cloned.");
		} catch (cloneError) {
			if (!parsed.version) throw cloneError;
			debug("Shallow clone failed, falling back to full clone:", cloneError);
			status.update("Shallow clone failed, cloning...");
			await rm(tmpDir, {
				recursive: true,
				force: true
			});
			await mkdir(tmpDir, { recursive: true });
			await gitExecIn(["init"]);
			await gitExecIn([
				"remote",
				"add",
				"origin",
				parsed.uri
			]);
			await gitExecIn(["fetch", "origin"]);
			await gitExecIn(["checkout", parsed.version]);
			status.update("Fetched.");
		}
		if (parsed.subdir) {
			status.update(`Sparse checkout ${parsed.subdir}...`);
			await gitExecIn([
				"sparse-checkout",
				"set",
				parsed.subdir
			]);
			await gitExecIn(["checkout"]);
		}
		status.update("Packing...");
		const tarDir = parsed.subdir ? join(tmpDir, parsed.subdir) : tmpDir;
		const { create } = await import("./libs/tar.mjs").then((n) => n.t);
		status.done();
		const stream = create({
			gzip: true,
			cwd: tarDir,
			filter: (path) => !path.startsWith(".git/") && path !== ".git" && !path.startsWith("./.git/") && path !== "./.git"
		}, ["."]).pipe(new PassThrough());
		let cleaned = false;
		const cleanup = () => {
			if (cleaned) return;
			cleaned = true;
			rm(tmpDir, {
				recursive: true,
				force: true
			});
		};
		stream.on("end", cleanup);
		stream.on("error", cleanup);
		stream.on("close", cleanup);
		return stream;
	} catch (error) {
		status.done();
		await rm(tmpDir, {
			recursive: true,
			force: true
		});
		throw error;
	}
}
const _spinnerFrames = [
	"⠋",
	"⠙",
	"⠹",
	"⠸",
	"⠼",
	"⠴",
	"⠦",
	"⠧",
	"⠇",
	"⠏"
];
function _gitSpawn(args, opts, status) {
	return new Promise((resolve, reject) => {
		const proc = spawn("git", args, {
			...opts,
			stdio: [
				"ignore",
				"pipe",
				"pipe"
			]
		});
		proc.stdout.resume();
		let lastLine = "";
		proc.stderr?.on("data", (chunk) => {
			const str = chunk.toString();
			for (const line of str.split(/[\r\n]/)) {
				const clean = line.trim();
				if (clean) lastLine = clean;
			}
			if (status) status.update(lastLine);
		});
		proc.on("close", (code) => {
			if (code === 0) resolve(lastLine);
			else reject(/* @__PURE__ */ new Error(`git ${args[0]} exited with code ${code}. Is git installed?`));
		});
		proc.on("error", (err) => {
			if (err.code === "ENOENT") reject(/* @__PURE__ */ new Error("git is not installed or not found in PATH"));
			else reject(err);
		});
	});
}
function _createStatus() {
	if (!process.stderr.isTTY) return {
		update(_text) {},
		done() {}
	};
	let msg = "";
	let frame = 0;
	const render = () => {
		const spinner = _spinnerFrames[frame % _spinnerFrames.length];
		frame++;
		process.stderr.write(`\x1B[2K\r\x1B[2m${spinner} ${msg}\x1B[0m`);
	};
	const interval = setInterval(render, 80);
	return {
		update(text) {
			msg = text;
			render();
		},
		done() {
			clearInterval(interval);
			process.stderr.write("\x1B[2K\r");
		}
	};
}
//#endregion
//#region src/providers.ts
const http = async (input, options) => {
	if (input.endsWith(".json")) return await _httpJSON(input, options);
	const url = new URL(input);
	let name = basename$1(url.pathname);
	try {
		const head = await sendFetch(url.href, {
			method: "HEAD",
			validateStatus: true,
			headers: { authorization: options.auth ? `Bearer ${options.auth}` : void 0 }
		});
		if ((head.headers.get("content-type") || "").includes("application/json")) return await _httpJSON(input, options);
		const filename = head.headers.get("content-disposition")?.match(/filename="?(.+)"?/)?.[1];
		if (filename) name = filename.split(".")[0];
	} catch (error) {
		debug(`Failed to fetch HEAD for ${url.href}:`, error);
	}
	return {
		name: `${name}-${url.href.slice(0, 8)}`,
		version: "",
		subdir: "",
		tar: url.href,
		defaultDir: name,
		headers: { Authorization: options.auth ? `Bearer ${options.auth}` : void 0 }
	};
};
const _httpJSON = async (input, options) => {
	const info = await (await sendFetch(input, {
		validateStatus: true,
		headers: { authorization: options.auth ? `Bearer ${options.auth}` : void 0 }
	})).json();
	if (!info.tar || !info.name) throw new Error(`Invalid template info from ${input}. name or tar fields are missing!`);
	return info;
};
const github = (input, options) => {
	const parsed = parseGitURI(input);
	const githubAPIURL = process.env.GIGET_GITHUB_URL || "https://api.github.com";
	return {
		name: parsed.repo.replace("/", "-"),
		version: parsed.ref,
		subdir: parsed.subdir,
		headers: {
			Authorization: options.auth ? `Bearer ${options.auth}` : void 0,
			Accept: "application/vnd.github+json",
			"X-GitHub-Api-Version": "2022-11-28"
		},
		url: `${githubAPIURL.replace("api.github.com", "github.com")}/${parsed.repo}/tree/${parsed.ref}${parsed.subdir}`,
		tar: `${githubAPIURL}/repos/${parsed.repo}/tarball/${parsed.ref}`
	};
};
const gitlab = (input, options) => {
	const parsed = parseGitURI(input, { expandRepo: true });
	const gitlab = process.env.GIGET_GITLAB_URL || "https://gitlab.com";
	return {
		name: parsed.repo.replace("/", "-"),
		version: parsed.ref,
		subdir: parsed.subdir,
		headers: {
			authorization: options.auth ? `Bearer ${options.auth}` : void 0,
			"sec-fetch-mode": "same-origin"
		},
		url: `${gitlab}/${parsed.repo}/tree/${parsed.ref}${parsed.subdir}`,
		tar: `${gitlab}/${parsed.repo}/-/archive/${parsed.ref}.tar.gz`
	};
};
const bitbucket = (input, options) => {
	const parsed = parseGitURI(input);
	return {
		name: parsed.repo.replace("/", "-"),
		version: parsed.ref,
		subdir: parsed.subdir,
		headers: { authorization: options.auth ? `Bearer ${options.auth}` : void 0 },
		url: `https://bitbucket.com/${parsed.repo}/src/${parsed.ref}${parsed.subdir}`,
		tar: `https://bitbucket.org/${parsed.repo}/get/${parsed.ref}.tar.gz`
	};
};
const sourcehut = (input, options) => {
	const parsed = parseGitURI(input);
	return {
		name: parsed.repo.replace("/", "-"),
		version: parsed.ref,
		subdir: parsed.subdir,
		headers: { authorization: options.auth ? `Bearer ${options.auth}` : void 0 },
		url: `https://git.sr.ht/~${parsed.repo}/tree/${parsed.ref}/item${parsed.subdir}`,
		tar: `https://git.sr.ht/~${parsed.repo}/archive/${parsed.ref}.tar.gz`
	};
};
const providers = {
	http,
	https: http,
	git,
	github,
	gh: github,
	gitlab,
	bitbucket,
	sourcehut
};
//#endregion
//#region src/registry.ts
const DEFAULT_REGISTRY = "https://raw.githubusercontent.com/unjs/giget/main/templates";
const registryProvider = (registryEndpoint = DEFAULT_REGISTRY, options = {}) => {
	return (async (input) => {
		const start = Date.now();
		const registryURL = `${registryEndpoint}/${input}.json`;
		const result = await sendFetch(registryURL, { headers: { authorization: options.auth ? `Bearer ${options.auth}` : void 0 } });
		if (result.status >= 400) throw new Error(`Failed to download ${input} template info from ${registryURL}: ${result.status} ${result.statusText}`);
		const info = await result.json();
		if (!info.tar || !info.name) throw new Error(`Invalid template info from ${registryURL}. name or tar fields are missing!`);
		debug(`Fetched ${input} template info from ${registryURL} in ${Date.now() - start}ms`);
		return info;
	});
};
//#endregion
//#region src/giget.ts
const sourceProtoRe = /^([\w+-.]+):/;
async function downloadTemplate(input, options = {}) {
	options.registry = process.env.GIGET_REGISTRY ?? options.registry;
	options.auth = process.env.GIGET_AUTH ?? options.auth;
	const registry = options.registry === false ? void 0 : registryProvider(options.registry, { auth: options.auth });
	let providerName = options.provider || (registry ? "registry" : "github");
	let source = input;
	const sourceProviderMatch = input.match(sourceProtoRe);
	if (sourceProviderMatch) {
		providerName = sourceProviderMatch[1];
		source = input.slice(sourceProviderMatch[0].length);
		if (providerName === "http" || providerName === "https") source = input;
	}
	if (providerName.endsWith("+git")) {
		source = `${providerName.slice(0, -4)}:${source}`;
		providerName = "git";
	}
	const provider = options.providers?.[providerName] || providers[providerName] || registry;
	if (!provider) throw new Error(`Unsupported provider: ${providerName}`);
	const template = await Promise.resolve().then(() => provider(source, { auth: options.auth })).catch((error) => {
		throw new Error(`Failed to download template from ${providerName}: ${error.message}`);
	});
	if (!template) throw new Error(`Failed to resolve template from ${providerName}`);
	template.name = (template.name || "template").replace(/[^\da-z-]/gi, "-");
	template.defaultDir = (template.defaultDir || template.name).replace(/[^\da-z-]/gi, "-");
	const tarPath = resolve$1(resolve$1(cacheDirectory(), providerName, template.name), (template.version || template.name) + ".tar.gz");
	if (options.preferOffline && existsSync(tarPath)) options.offline = true;
	if (!options.offline) {
		await mkdir(dirname$1(tarPath), { recursive: true });
		const s = Date.now();
		if (typeof template.tar === "function") {
			const tarFn = template.tar;
			await (async () => {
				const stream = await tarFn({ auth: options.auth });
				await pipeline$1(stream instanceof Readable ? stream : Readable.fromWeb(stream), createWriteStream(tarPath));
			})().catch((error) => {
				if (!existsSync(tarPath)) throw error;
				debug("Download error. Using cached version:", error);
				options.offline = true;
			});
		} else await download(template.tar, tarPath, { headers: {
			Authorization: options.auth ? `Bearer ${options.auth}` : void 0,
			...normalizeHeaders(template.headers)
		} }).catch((error) => {
			if (!existsSync(tarPath)) throw error;
			debug("Download error. Using cached version:", error);
			options.offline = true;
		});
		debug(`Downloaded to ${tarPath} in ${Date.now() - s}ms`);
	}
	if (!existsSync(tarPath)) throw new Error(`Tarball not found: ${tarPath} (offline: ${options.offline})`);
	const extractPath = resolve$1(resolve$1(options.cwd || "."), options.dir || template.defaultDir);
	if (options.forceClean) await rm(extractPath, {
		recursive: true,
		force: true
	});
	if (!options.force && existsSync(extractPath) && readdirSync(extractPath).length > 0) throw new Error(`Destination ${extractPath} already exists.`);
	await mkdir(extractPath, { recursive: true });
	const s = Date.now();
	const subdir = template.subdir?.replace(/^\//, "") || "";
	const { extract } = await import("./libs/tar.mjs").then((n) => n.t);
	await extract({
		file: tarPath,
		cwd: extractPath,
		onReadEntry(entry) {
			entry.path = entry.path.split("/").splice(1).join("/");
			if (subdir) if (entry.path.startsWith(subdir + "/")) entry.path = entry.path.slice(subdir.length);
			else entry.path = "";
		}
	});
	debug(`Extracted to ${extractPath} in ${Date.now() - s}ms`);
	if (options.install) {
		debug("Installing dependencies...");
		const { installDependencies } = await import("./libs/nypm.mjs").then((n) => n.t);
		await installDependencies({
			cwd: extractPath,
			silent: options.silent,
			...typeof options.install === "object" ? options.install : {}
		});
	}
	return {
		...template,
		source,
		dir: extractPath
	};
}
//#endregion
export { registryProvider as n, startShell as r, downloadTemplate as t };
