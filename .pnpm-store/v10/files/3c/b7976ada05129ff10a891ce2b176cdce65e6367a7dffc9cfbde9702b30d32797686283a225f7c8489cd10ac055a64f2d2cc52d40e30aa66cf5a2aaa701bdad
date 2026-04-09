import { t as e } from "../rolldown-runtime.mjs";
import { createRequire as t } from "node:module";
import { existsSync as n } from "node:fs";
import { readFile as r } from "node:fs/promises";
import { PassThrough as i } from "node:stream";
import { spawn as a } from "node:child_process";
import { delimiter as o, dirname as s, normalize as c, resolve as l } from "node:path";
import { cwd as u } from "node:process";
import d from "node:readline";
const f = /^[A-Za-z]:\//;
function p(e = ``) {
	return e && e.replace(/\\/g, `/`).replace(f, (e) => e.toUpperCase());
}
const ee = /^[/\\]{2}/, te = /^[/\\](?![/\\])|^[/\\]{2}(?!\.)|^[A-Za-z]:[/\\]/, m = /^[A-Za-z]:$/, h = /^\/([A-Za-z]:)?$/, g = function(e) {
	if (e.length === 0) return `.`;
	e = p(e);
	let t = e.match(ee), n = x(e), r = e[e.length - 1] === `/`;
	return e = b(e, !n), e.length === 0 ? n ? `/` : r ? `./` : `.` : (r && (e += `/`), m.test(e) && (e += `/`), t ? n ? `//${e}` : `//./${e}` : n && !x(e) ? `/${e}` : e);
}, _ = function(...e) {
	let t = ``;
	for (let n of e) if (n) if (t.length > 0) {
		let e = t[t.length - 1] === `/`, r = n[0] === `/`;
		e && r ? t += n.slice(1) : t += e || r ? n : `/${n}`;
	} else t += n;
	return g(t);
};
function v() {
	return typeof process < `u` && typeof process.cwd == `function` ? process.cwd().replace(/\\/g, `/`) : `/`;
}
const y = function(...e) {
	e = e.map((e) => p(e));
	let t = ``, n = !1;
	for (let r = e.length - 1; r >= -1 && !n; r--) {
		let i = r >= 0 ? e[r] : v();
		!i || i.length === 0 || (t = `${i}/${t}`, n = x(i));
	}
	return t = b(t, !n), n && !x(t) ? `/${t}` : t.length > 0 ? t : `.`;
};
function b(e, t) {
	let n = ``, r = 0, i = -1, a = 0, o = null;
	for (let s = 0; s <= e.length; ++s) {
		if (s < e.length) o = e[s];
		else if (o === `/`) break;
		else o = `/`;
		if (o === `/`) {
			if (!(i === s - 1 || a === 1)) if (a === 2) {
				if (n.length < 2 || r !== 2 || n[n.length - 1] !== `.` || n[n.length - 2] !== `.`) {
					if (n.length > 2) {
						let e = n.lastIndexOf(`/`);
						e === -1 ? (n = ``, r = 0) : (n = n.slice(0, e), r = n.length - 1 - n.lastIndexOf(`/`)), i = s, a = 0;
						continue;
					} else if (n.length > 0) {
						n = ``, r = 0, i = s, a = 0;
						continue;
					}
				}
				t && (n += n.length > 0 ? `/..` : `..`, r = 2);
			} else n.length > 0 ? n += `/${e.slice(i + 1, s)}` : n = e.slice(i + 1, s), r = s - i - 1;
			i = s, a = 0;
		} else o === `.` && a !== -1 ? ++a : a = -1;
	}
	return n;
}
const x = function(e) {
	return te.test(e);
}, S = function(e, t) {
	let n = y(e).replace(h, `$1`).split(`/`), r = y(t).replace(h, `$1`).split(`/`);
	if (r[0][1] === `:` && n[0][1] === `:` && n[0] !== r[0]) return r.join(`/`);
	let i = [...n];
	for (let e of i) {
		if (r[0] !== e) break;
		n.shift(), r.shift();
	}
	return [...n.map(() => `..`), ...r].join(`/`);
}, C = function(e) {
	let t = p(e).replace(/\/$/, ``).split(`/`).slice(0, -1);
	return t.length === 1 && m.test(t[0]) && (t[0] += `/`), t.join(`/`) || (x(e) ? `/` : `.`);
}, ne = function(e, t) {
	let n = p(e).split(`/`), r = ``;
	for (let e = n.length - 1; e >= 0; e--) {
		let t = n[e];
		if (t) {
			r = t;
			break;
		}
	}
	return t && r.endsWith(t) ? r.slice(0, -t.length) : r;
};
globalThis.process?.platform;
var w = (e, t) => () => (t || e((t = { exports: {} }).exports, t), t.exports), T = t(import.meta.url);
const re = /^path$/i, E = {
	key: `PATH`,
	value: ``
};
function D(e) {
	for (let t in e) {
		if (!Object.prototype.hasOwnProperty.call(e, t) || !re.test(t)) continue;
		let n = e[t];
		return n ? {
			key: t,
			value: n
		} : E;
	}
	return E;
}
function O(e, t) {
	let n = t.value.split(o), r = [], i = e, a;
	do
		r.push(l(i, `node_modules`, `.bin`)), a = i, i = s(i);
	while (i !== a);
	let c = r.concat(n).join(o);
	return {
		key: t.key,
		value: c
	};
}
function k(e, t) {
	let n = {
		...process.env,
		...t
	}, r = O(e, D(n));
	return n[r.key] = r.value, n;
}
const A = (e) => {
	let t = e.length, n = new i(), r = () => {
		--t === 0 && n.emit(`end`);
	};
	for (let t of e) t.pipe(n, { end: !1 }), t.on(`end`, r);
	return n;
};
var j = w(((e, t) => {
	t.exports = a, a.sync = o;
	var n = T(`fs`);
	function r(e, t) {
		var n = t.pathExt === void 0 ? process.env.PATHEXT : t.pathExt;
		if (!n || (n = n.split(`;`), n.indexOf(``) !== -1)) return !0;
		for (var r = 0; r < n.length; r++) {
			var i = n[r].toLowerCase();
			if (i && e.substr(-i.length).toLowerCase() === i) return !0;
		}
		return !1;
	}
	function i(e, t, n) {
		return !e.isSymbolicLink() && !e.isFile() ? !1 : r(t, n);
	}
	function a(e, t, r) {
		n.stat(e, function(n, a) {
			r(n, n ? !1 : i(a, e, t));
		});
	}
	function o(e, t) {
		return i(n.statSync(e), e, t);
	}
})), M = w(((e, t) => {
	t.exports = r, r.sync = i;
	var n = T(`fs`);
	function r(e, t, r) {
		n.stat(e, function(e, n) {
			r(e, e ? !1 : a(n, t));
		});
	}
	function i(e, t) {
		return a(n.statSync(e), t);
	}
	function a(e, t) {
		return e.isFile() && o(e, t);
	}
	function o(e, t) {
		var n = e.mode, r = e.uid, i = e.gid, a = t.uid === void 0 ? process.getuid && process.getuid() : t.uid, o = t.gid === void 0 ? process.getgid && process.getgid() : t.gid, s = 64, c = 8, l = 1, u = s | c;
		return n & l || n & c && i === o || n & s && r === a || n & u && a === 0;
	}
})), N = w(((e, t) => {
	T(`fs`);
	var n = process.platform === `win32` || global.TESTING_WINDOWS ? j() : M();
	t.exports = r, r.sync = i;
	function r(e, t, i) {
		if (typeof t == `function` && (i = t, t = {}), !i) {
			if (typeof Promise != `function`) throw TypeError(`callback not provided`);
			return new Promise(function(n, i) {
				r(e, t || {}, function(e, t) {
					e ? i(e) : n(t);
				});
			});
		}
		n(e, t || {}, function(e, n) {
			e && (e.code === `EACCES` || t && t.ignoreErrors) && (e = null, n = !1), i(e, n);
		});
	}
	function i(e, t) {
		try {
			return n.sync(e, t || {});
		} catch (e) {
			if (t && t.ignoreErrors || e.code === `EACCES`) return !1;
			throw e;
		}
	}
})), P = w(((e, t) => {
	let n = process.platform === `win32` || process.env.OSTYPE === `cygwin` || process.env.OSTYPE === `msys`, r = T(`path`), i = n ? `;` : `:`, a = N(), o = (e) => Object.assign(Error(`not found: ${e}`), { code: `ENOENT` }), s = (e, t) => {
		let r = t.colon || i, a = e.match(/\//) || n && e.match(/\\/) ? [``] : [...n ? [process.cwd()] : [], ...(t.path || process.env.PATH || ``).split(r)], o = n ? t.pathExt || process.env.PATHEXT || `.EXE;.CMD;.BAT;.COM` : ``, s = n ? o.split(r) : [``];
		return n && e.indexOf(`.`) !== -1 && s[0] !== `` && s.unshift(``), {
			pathEnv: a,
			pathExt: s,
			pathExtExe: o
		};
	}, c = (e, t, n) => {
		typeof t == `function` && (n = t, t = {}), t ||= {};
		let { pathEnv: i, pathExt: c, pathExtExe: l } = s(e, t), u = [], d = (n) => new Promise((a, s) => {
			if (n === i.length) return t.all && u.length ? a(u) : s(o(e));
			let c = i[n], l = /^".*"$/.test(c) ? c.slice(1, -1) : c, d = r.join(l, e);
			a(f(!l && /^\.[\\\/]/.test(e) ? e.slice(0, 2) + d : d, n, 0));
		}), f = (e, n, r) => new Promise((i, o) => {
			if (r === c.length) return i(d(n + 1));
			let s = c[r];
			a(e + s, { pathExt: l }, (a, o) => {
				if (!a && o) if (t.all) u.push(e + s);
				else return i(e + s);
				return i(f(e, n, r + 1));
			});
		});
		return n ? d(0).then((e) => n(null, e), n) : d(0);
	};
	t.exports = c, c.sync = (e, t) => {
		t ||= {};
		let { pathEnv: n, pathExt: i, pathExtExe: c } = s(e, t), l = [];
		for (let o = 0; o < n.length; o++) {
			let s = n[o], u = /^".*"$/.test(s) ? s.slice(1, -1) : s, d = r.join(u, e), f = !u && /^\.[\\\/]/.test(e) ? e.slice(0, 2) + d : d;
			for (let e = 0; e < i.length; e++) {
				let n = f + i[e];
				try {
					if (a.sync(n, { pathExt: c })) if (t.all) l.push(n);
					else return n;
				} catch {}
			}
		}
		if (t.all && l.length) return l;
		if (t.nothrow) return null;
		throw o(e);
	};
})), F = w(((e, t) => {
	let n = (e = {}) => {
		let t = e.env || process.env;
		return (e.platform || process.platform) === `win32` ? Object.keys(t).reverse().find((e) => e.toUpperCase() === `PATH`) || `Path` : `PATH`;
	};
	t.exports = n, t.exports.default = n;
})), I = w(((e, t) => {
	let n = T(`path`), r = P(), i = F();
	function a(e, t) {
		let a = e.options.env || process.env, o = process.cwd(), s = e.options.cwd != null, c = s && process.chdir !== void 0 && !process.chdir.disabled;
		if (c) try {
			process.chdir(e.options.cwd);
		} catch {}
		let l;
		try {
			l = r.sync(e.command, {
				path: a[i({ env: a })],
				pathExt: t ? n.delimiter : void 0
			});
		} catch {} finally {
			c && process.chdir(o);
		}
		return l &&= n.resolve(s ? e.options.cwd : ``, l), l;
	}
	function o(e) {
		return a(e) || a(e, !0);
	}
	t.exports = o;
})), L = w(((e, t) => {
	let n = /([()\][%!^"`<>&|;, *?])/g;
	function r(e) {
		return e = e.replace(n, `^$1`), e;
	}
	function i(e, t) {
		return e = `${e}`, e = e.replace(/(?=(\\+?)?)\1"/g, `$1$1\\"`), e = e.replace(/(?=(\\+?)?)\1$/, `$1$1`), e = `"${e}"`, e = e.replace(n, `^$1`), t && (e = e.replace(n, `^$1`)), e;
	}
	t.exports.command = r, t.exports.argument = i;
})), R = w(((e, t) => {
	t.exports = /^#!(.*)/;
})), z = w(((e, t) => {
	let n = R();
	t.exports = (e = ``) => {
		let t = e.match(n);
		if (!t) return null;
		let [r, i] = t[0].replace(/#! ?/, ``).split(` `), a = r.split(`/`).pop();
		return a === `env` ? i : i ? `${a} ${i}` : a;
	};
})), B = w(((e, t) => {
	let n = T(`fs`), r = z();
	function i(e) {
		let t = Buffer.alloc(150), i;
		try {
			i = n.openSync(e, `r`), n.readSync(i, t, 0, 150, 0), n.closeSync(i);
		} catch {}
		return r(t.toString());
	}
	t.exports = i;
})), V = w(((e, t) => {
	let n = T(`path`), r = I(), i = L(), a = B(), o = process.platform === `win32`, s = /\.(?:com|exe)$/i, c = /node_modules[\\/].bin[\\/][^\\/]+\.cmd$/i;
	function l(e) {
		e.file = r(e);
		let t = e.file && a(e.file);
		return t ? (e.args.unshift(e.file), e.command = t, r(e)) : e.file;
	}
	function u(e) {
		if (!o) return e;
		let t = l(e), r = !s.test(t);
		if (e.options.forceShell || r) {
			let r = c.test(t);
			e.command = n.normalize(e.command), e.command = i.command(e.command), e.args = e.args.map((e) => i.argument(e, r)), e.args = [
				`/d`,
				`/s`,
				`/c`,
				`"${[e.command].concat(e.args).join(` `)}"`
			], e.command = process.env.comspec || `cmd.exe`, e.options.windowsVerbatimArguments = !0;
		}
		return e;
	}
	function d(e, t, n) {
		t && !Array.isArray(t) && (n = t, t = null), t = t ? t.slice(0) : [], n = Object.assign({}, n);
		let r = {
			command: e,
			args: t,
			options: n,
			file: void 0,
			original: {
				command: e,
				args: t
			}
		};
		return n.shell ? r : u(r);
	}
	t.exports = d;
})), ie = w(((e, t) => {
	let n = process.platform === `win32`;
	function r(e, t) {
		return Object.assign(Error(`${t} ${e.command} ENOENT`), {
			code: `ENOENT`,
			errno: `ENOENT`,
			syscall: `${t} ${e.command}`,
			path: e.command,
			spawnargs: e.args
		});
	}
	function i(e, t) {
		if (!n) return;
		let r = e.emit;
		e.emit = function(n, i) {
			if (n === `exit`) {
				let n = a(i, t);
				if (n) return r.call(e, `error`, n);
			}
			return r.apply(e, arguments);
		};
	}
	function a(e, t) {
		return n && e === 1 && !t.file ? r(t.original, `spawn`) : null;
	}
	function o(e, t) {
		return n && e === 1 && !t.file ? r(t.original, `spawnSync`) : null;
	}
	t.exports = {
		hookChildProcess: i,
		verifyENOENT: a,
		verifyENOENTSync: o,
		notFoundError: r
	};
})), H = w(((e, t) => {
	let n = T(`child_process`), r = V(), i = ie();
	function a(e, t, a) {
		let o = r(e, t, a), s = n.spawn(o.command, o.args, o.options);
		return i.hookChildProcess(s, o), s;
	}
	function o(e, t, a) {
		let o = r(e, t, a), s = n.spawnSync(o.command, o.args, o.options);
		return s.error = s.error || i.verifyENOENTSync(s.status, o), s;
	}
	t.exports = a, t.exports.spawn = a, t.exports.sync = o, t.exports._parse = r, t.exports._enoent = i;
}))(), U = class extends Error {
	result;
	output;
	get exitCode() {
		if (this.result.exitCode !== null) return this.result.exitCode;
	}
	constructor(e, t) {
		super(`Process exited with non-zero status (${e.exitCode})`), this.result = e, this.output = t;
	}
};
const W = {
	timeout: void 0,
	persist: !1
}, G = { windowsHide: !0 };
function K(e, t) {
	return {
		command: c(e),
		args: t ?? []
	};
}
function q(e) {
	let t = new AbortController();
	for (let n of e) {
		if (n.aborted) return t.abort(), n;
		n.addEventListener(`abort`, () => {
			t.abort(n.reason);
		}, { signal: t.signal });
	}
	return t.signal;
}
async function J(e) {
	let t = ``;
	for await (let n of e) t += n.toString();
	return t;
}
var Y = class {
	_process;
	_aborted = !1;
	_options;
	_command;
	_args;
	_resolveClose;
	_processClosed;
	_thrownError;
	get process() {
		return this._process;
	}
	get pid() {
		return this._process?.pid;
	}
	get exitCode() {
		if (this._process && this._process.exitCode !== null) return this._process.exitCode;
	}
	constructor(e, t, n) {
		this._options = {
			...W,
			...n
		}, this._command = e, this._args = t ?? [], this._processClosed = new Promise((e) => {
			this._resolveClose = e;
		});
	}
	kill(e) {
		return this._process?.kill(e) === !0;
	}
	get aborted() {
		return this._aborted;
	}
	get killed() {
		return this._process?.killed === !0;
	}
	pipe(e, t, n) {
		return ae(e, t, {
			...n,
			stdin: this
		});
	}
	async *[Symbol.asyncIterator]() {
		let e = this._process;
		if (!e) return;
		let t = [];
		this._streamErr && t.push(this._streamErr), this._streamOut && t.push(this._streamOut);
		let n = A(t), r = d.createInterface({ input: n });
		for await (let e of r) yield e.toString();
		if (await this._processClosed, e.removeAllListeners(), this._thrownError) throw this._thrownError;
		if (this._options?.throwOnError && this.exitCode !== 0 && this.exitCode !== void 0) throw new U(this);
	}
	async _waitForOutput() {
		let e = this._process;
		if (!e) throw Error(`No process was started`);
		let [t, n] = await Promise.all([this._streamOut ? J(this._streamOut) : ``, this._streamErr ? J(this._streamErr) : ``]);
		if (await this._processClosed, this._options?.stdin && await this._options.stdin, e.removeAllListeners(), this._thrownError) throw this._thrownError;
		let r = {
			stderr: n,
			stdout: t,
			exitCode: this.exitCode
		};
		if (this._options.throwOnError && this.exitCode !== 0 && this.exitCode !== void 0) throw new U(this, r);
		return r;
	}
	then(e, t) {
		return this._waitForOutput().then(e, t);
	}
	_streamOut;
	_streamErr;
	spawn() {
		let e = u(), t = this._options, n = {
			...G,
			...t.nodeOptions
		}, r = [];
		this._resetState(), t.timeout !== void 0 && r.push(AbortSignal.timeout(t.timeout)), t.signal !== void 0 && r.push(t.signal), t.persist === !0 && (n.detached = !0), r.length > 0 && (n.signal = q(r)), n.env = k(e, n.env);
		let { command: i, args: o } = K(this._command, this._args), s = (0, H._parse)(i, o, n), c = a(s.command, s.args, s.options);
		if (c.stderr && (this._streamErr = c.stderr), c.stdout && (this._streamOut = c.stdout), this._process = c, c.once(`error`, this._onError), c.once(`close`, this._onClose), t.stdin !== void 0 && c.stdin && t.stdin.process) {
			let { stdout: e } = t.stdin.process;
			e && e.pipe(c.stdin);
		}
	}
	_resetState() {
		this._aborted = !1, this._processClosed = new Promise((e) => {
			this._resolveClose = e;
		}), this._thrownError = void 0;
	}
	_onError = (e) => {
		if (e.name === `AbortError` && (!(e.cause instanceof Error) || e.cause.name !== `TimeoutError`)) {
			this._aborted = !0;
			return;
		}
		this._thrownError = e;
	};
	_onClose = () => {
		this._resolveClose && this._resolveClose();
	};
};
const X = (e, t, n) => {
	let r = new Y(e, t, n);
	return r.spawn(), r;
}, ae = X;
var oe = e({
	detectPackageManager: () => $,
	installDependencies: () => fe,
	packageManagers: () => Q
});
async function se(e, t, n = {}) {
	let r = g(e).split(`/`);
	for (; r.length > 0;) {
		let e = await t(r.join(`/`) || `/`);
		if (e || !n.includeParentDirs) return e;
		r.pop();
	}
}
function ce(e) {
	let t;
	return () => (t === void 0 && (t = e().then((e) => (t = e, t))), t);
}
const Z = ce(async () => {
	if (globalThis.process?.versions?.webcontainer) return !1;
	try {
		let { exitCode: e } = await X(`corepack`, [`--version`]);
		return e === 0;
	} catch {
		return !1;
	}
});
async function le(e, t, n = {}) {
	let r = e !== `npm` && e !== `bun` && e !== `deno` && n.corepack !== !1 && await Z() ? [`corepack`, [e, ...t]] : [e, t], { exitCode: i, stdout: a, stderr: o } = await X(r[0], r[1], { nodeOptions: {
		cwd: y(n.cwd || process.cwd()),
		env: n.env,
		stdio: n.silent ? `pipe` : `inherit`
	} });
	if (i !== 0) throw Error(`\`${r.flat().join(` `)}\` failed.${n.silent ? [
		``,
		a,
		o
	].join(`
`) : ``}`);
}
async function ue(e = {}) {
	let t = e.cwd || process.cwd(), n = {
		...process.env,
		...e.env
	}, r = (typeof e.packageManager == `string` ? Q.find((t) => t.name === e.packageManager) : e.packageManager) || await $(e.cwd || process.cwd());
	if (!r) throw Error(`No package manager auto-detected.`);
	return {
		cwd: t,
		env: n,
		silent: e.silent ?? !1,
		packageManager: r,
		dev: e.dev ?? !1,
		workspace: e.workspace,
		global: e.global ?? !1,
		dry: e.dry ?? !1,
		corepack: e.corepack ?? !0
	};
}
function de(e) {
	let [t, n] = (e || ``).split(`@`), [r, i] = n?.split(`+`) || [];
	if (t && t !== `-` && /^(@[a-z0-9-~][a-z0-9-._~]*\/)?[a-z0-9-~][a-z0-9-._~]*$/.test(t)) return {
		name: t,
		version: r,
		buildMeta: i
	};
	let a = (t || ``).replace(/\W+/g, ``);
	return {
		name: a,
		version: r,
		buildMeta: i,
		warnings: [`Abnormal characters found in \`packageManager\` field, sanitizing from \`${t}\` to \`${a}\``]
	};
}
const Q = [
	{
		name: `npm`,
		command: `npm`,
		lockFile: `package-lock.json`
	},
	{
		name: `pnpm`,
		command: `pnpm`,
		lockFile: `pnpm-lock.yaml`,
		files: [`pnpm-workspace.yaml`]
	},
	{
		name: `bun`,
		command: `bun`,
		lockFile: [`bun.lockb`, `bun.lock`]
	},
	{
		name: `yarn`,
		command: `yarn`,
		lockFile: `yarn.lock`,
		files: [`.yarnrc.yml`]
	},
	{
		name: `deno`,
		command: `deno`,
		lockFile: `deno.lock`,
		files: [`deno.json`]
	}
];
async function $(e, t = {}) {
	let i = await se(y(e || `.`), async (e) => {
		if (!t.ignorePackageJSON) {
			let t = _(e, `package.json`);
			if (n(t)) {
				let e = JSON.parse(await r(t, `utf8`));
				if (e?.packageManager) {
					let { name: t, version: n = `0.0.0`, buildMeta: r, warnings: i } = de(e.packageManager);
					if (t) {
						let e = n.split(`.`)[0], a = Q.find((n) => n.name === t && n.majorVersion === e) || Q.find((e) => e.name === t);
						return {
							name: t,
							command: t,
							version: n,
							majorVersion: e,
							buildMeta: r,
							warnings: i,
							files: a?.files,
							lockFile: a?.lockFile
						};
					}
				}
			}
			if (n(_(e, `deno.json`))) return Q.find((e) => e.name === `deno`);
		}
		if (!t.ignoreLockFile) {
			for (let t of Q) if ([t.lockFile, t.files].flat().filter(Boolean).some((t) => n(y(e, t)))) return { ...t };
		}
	}, { includeParentDirs: t.includeParentDirs ?? !0 });
	if (!i && !t.ignoreArgv) {
		let e = process.argv[1];
		if (e) {
			for (let t of Q) if (RegExp(`[/\\\\]\\.?${t.command}`).test(e)) return t;
		}
	}
	return i;
}
async function fe(e = {}) {
	let t = await ue(e), n = e.frozenLockFile ? {
		npm: [`ci`],
		yarn: [`install`, `--immutable`],
		bun: [`install`, `--frozen-lockfile`],
		pnpm: [`install`, `--frozen-lockfile`],
		deno: [`install`, `--frozen`]
	}[t.packageManager.name] : [`install`];
	return e.ignoreWorkspace && t.packageManager.name === `pnpm` && n.push(`--ignore-workspace`), t.dry || await le(t.packageManager.command, n, {
		cwd: t.cwd,
		silent: t.silent,
		corepack: t.corepack
	}), { exec: {
		command: t.packageManager.command,
		args: n
	} };
}
export { y as a, S as i, ne as n, C as r, oe as t };
