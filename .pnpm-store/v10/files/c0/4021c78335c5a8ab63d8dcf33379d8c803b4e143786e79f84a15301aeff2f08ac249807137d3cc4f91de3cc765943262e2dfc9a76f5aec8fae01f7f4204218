import { parseArgs as e } from "node:util";
const t = /\d/, n = [
	`-`,
	`_`,
	`/`,
	`.`
];
function r(e = ``) {
	if (!t.test(e)) return e !== e.toLowerCase();
}
function i(e, t) {
	let i = t ?? n, a = [];
	if (!e || typeof e != `string`) return a;
	let o = ``, s, c;
	for (let t of e) {
		let e = i.includes(t);
		if (e === !0) {
			a.push(o), o = ``, s = void 0;
			continue;
		}
		let n = r(t);
		if (c === !1) {
			if (s === !1 && n === !0) {
				a.push(o), o = t, s = n;
				continue;
			}
			if (s === !0 && n === !1 && o.length > 1) {
				let e = o.at(-1);
				a.push(o.slice(0, Math.max(0, o.length - 1))), o = e + t, s = n;
				continue;
			}
		}
		o += t, s = n, c = e;
	}
	return a.push(o), a;
}
function a(e) {
	return e ? e[0].toUpperCase() + e.slice(1) : ``;
}
function o(e) {
	return e ? e[0].toLowerCase() + e.slice(1) : ``;
}
function s(e, t) {
	return e ? (Array.isArray(e) ? e : i(e)).map((e) => a(t?.normalize ? e.toLowerCase() : e)).join(``) : ``;
}
function c(e, t) {
	return o(s(e || ``, t));
}
function l(e, t) {
	return e ? (Array.isArray(e) ? e : i(e)).map((e) => e.toLowerCase()).join(t ?? `-`) : ``;
}
function u(e) {
	return Array.isArray(e) ? e : e === void 0 ? [] : [e];
}
function d(e, t = ``) {
	let n = [];
	for (let t of e) for (let [e, r] of t.entries()) n[e] = Math.max(n[e] || 0, r.length);
	return e.map((e) => e.map((e, r) => t + e[r === 0 ? `padStart` : `padEnd`](n[r])).join(`  `)).join(`
`);
}
function f(e) {
	return typeof e == `function` ? e() : e;
}
var p = class extends Error {
	code;
	constructor(e, t) {
		super(e), this.name = `CLIError`, this.code = t;
	}
};
function m(t = [], n = {}) {
	let r = new Set(n.boolean || []), i = new Set(n.string || []), a = n.alias || {}, o = n.default || {}, s = /* @__PURE__ */ new Map(), c = /* @__PURE__ */ new Map();
	for (let [e, t] of Object.entries(a)) {
		let n = t;
		for (let t of n) s.set(e, t), c.has(t) || c.set(t, []), c.get(t).push(e), s.set(t, e), c.has(e) || c.set(e, []), c.get(e).push(t);
	}
	let l = {};
	function u(e) {
		if (r.has(e)) return `boolean`;
		let t = c.get(e) || [];
		for (let e of t) if (r.has(e)) return `boolean`;
		return `string`;
	}
	let d = new Set([
		...r,
		...i,
		...Object.keys(a),
		...Object.values(a).flat(),
		...Object.keys(o)
	]);
	for (let e of d) l[e] || (l[e] = {
		type: u(e),
		default: o[e]
	});
	for (let [e, t] of s.entries()) e.length === 1 && l[t] && !l[t].short && (l[t].short = e);
	let f = [], p = {};
	for (let e = 0; e < t.length; e++) {
		let n = t[e];
		if (n === `--`) {
			f.push(...t.slice(e));
			break;
		}
		if (n.startsWith(`--no-`)) {
			let e = n.slice(5);
			p[e] = !0;
			continue;
		}
		f.push(n);
	}
	let m;
	try {
		m = e({
			args: f,
			options: Object.keys(l).length > 0 ? l : void 0,
			allowPositionals: !0,
			strict: !1
		});
	} catch {
		m = {
			values: {},
			positionals: f
		};
	}
	let h = { _: [] };
	h._ = m.positionals;
	for (let [e, t] of Object.entries(m.values)) h[e] = t;
	for (let [e] of Object.entries(p)) {
		h[e] = !1;
		let t = s.get(e);
		t && (h[t] = !1);
		let n = c.get(e);
		if (n) for (let e of n) h[e] = !1;
	}
	for (let [e, t] of s.entries()) h[e] !== void 0 && h[t] === void 0 && (h[t] = h[e]), h[t] !== void 0 && h[e] === void 0 && (h[e] = h[t]);
	return h;
}
const h = (() => {
	let e = globalThis.process?.env ?? {};
	return e.NO_COLOR === `1` || e.TERM === `dumb` || e.TEST || e.CI;
})(), g = (e, t = 39) => (n) => h ? n : `\u001B[${e}m${n}\u001B[${t}m`, _ = g(1, 22), v = g(36), y = g(90), b = g(4, 24);
function x(e, t) {
	let n = {
		boolean: [],
		string: [],
		alias: {},
		default: {}
	}, r = S(t);
	for (let e of r) {
		if (e.type === `positional`) continue;
		e.type === `string` || e.type === `enum` ? n.string.push(e.name) : e.type === `boolean` && n.boolean.push(e.name), e.default !== void 0 && (n.default[e.name] = e.default), e.alias && (n.alias[e.name] = e.alias);
		let t = c(e.name), r = l(e.name);
		if (t !== e.name || r !== e.name) {
			let i = u(n.alias[e.name] || []);
			t !== e.name && !i.includes(t) && i.push(t), r !== e.name && !i.includes(r) && i.push(r), i.length > 0 && (n.alias[e.name] = i);
		}
	}
	let i = m(e, n), [ ...a] = i._, o = new Proxy(i, { get(e, t) {
		return e[t] ?? e[c(t)] ?? e[l(t)];
	} });
	for (let [, e] of r.entries()) if (e.type === `positional`) {
		let t = a.shift();
		if (t !== void 0) o[e.name] = t;
		else if (e.default === void 0 && e.required !== !1) throw new p(`Missing required positional argument: ${e.name.toUpperCase()}`, `EARG`);
		else o[e.name] = e.default;
	} else if (e.type === `enum`) {
		let t = o[e.name], n = e.options || [];
		if (t !== void 0 && n.length > 0 && !n.includes(t)) throw new p(`Invalid value for argument: ${v(`--${e.name}`)} (${v(t)}). Expected one of: ${n.map((e) => v(e)).join(`, `)}.`, `EARG`);
	} else if (e.required && o[e.name] === void 0) throw new p(`Missing required argument: --${e.name}`, `EARG`);
	return o;
}
function S(e) {
	let t = [];
	for (let [n, r] of Object.entries(e || {})) t.push({
		...r,
		name: n,
		alias: u(r.alias)
	});
	return t;
}
function C(e) {
	return e;
}
async function w(e, t) {
	let n = await f(e.args || {}), r = x(t.rawArgs, n), i = {
		rawArgs: t.rawArgs,
		args: r,
		data: t.data,
		cmd: e
	};
	typeof e.setup == `function` && await e.setup(i);
	let a;
	try {
		let n = await f(e.subCommands);
		if (n && Object.keys(n).length > 0) {
			let r = t.rawArgs.findIndex((e) => !e.startsWith(`-`)), i = t.rawArgs[r];
			if (i) {
				if (!n[i]) throw new p(`Unknown command ${v(i)}`, `E_UNKNOWN_COMMAND`);
				let e = await f(n[i]);
				e && await w(e, { rawArgs: t.rawArgs.slice(r + 1) });
			} else if (!e.run) throw new p(`No command specified.`, `E_NO_COMMAND`);
		}
		typeof e.run == `function` && (a = await e.run(i));
	} finally {
		typeof e.cleanup == `function` && await e.cleanup(i);
	}
	return { result: a };
}
async function T(e, t, n) {
	let r = await f(e.subCommands);
	if (r && Object.keys(r).length > 0) {
		let n = t.findIndex((e) => !e.startsWith(`-`)), i = t[n], a = await f(r[i]);
		if (a) return T(a, t.slice(n + 1), e);
	}
	return [e, n];
}
async function E(e, t) {
	try {
		console.log(await O(e, t) + `
`);
	} catch (e) {
		console.error(e);
	}
}
const D = /^no[-A-Z]/;
async function O(e, t) {
	let n = await f(e.meta || {}), r = S(await f(e.args || {})), i = await f(t?.meta || {}), a = `${i.name ? `${i.name} ` : ``}` + (n.name || process.argv[1]), o = [], s = [], c = [], l = [];
	for (let e of r) if (e.type === `positional`) {
		let t = e.name.toUpperCase(), n = e.required !== !1 && e.default === void 0, r = e.default ? `="${e.default}"` : ``;
		s.push([
			v(t + r),
			e.description || ``,
			e.valueHint ? `<${e.valueHint}>` : ``
		]), l.push(n ? `<${t}>` : `[${t}]`);
	} else {
		let t = e.required === !0 && e.default === void 0, n = [...(e.alias || []).map((e) => `-${e}`), `--${e.name}`].join(`, `) + (e.type === `string` && (e.valueHint || e.default) ? `=${e.valueHint ? `<${e.valueHint}>` : `"${e.default || ``}"`}` : ``) + (e.type === `enum` && e.options ? `=<${e.options.join(`|`)}>` : ``);
		if (o.push([v(n + (t ? ` (required)` : ``)), e.description || ``]), e.type === `boolean` && (e.default === !0 || e.negativeDescription) && !D.test(e.name)) {
			let n = [...(e.alias || []).map((e) => `--no-${e}`), `--no-${e.name}`].join(`, `);
			o.push([v(n + (t ? ` (required)` : ``)), e.negativeDescription || ``]);
		}
		t && l.push(n);
	}
	if (e.subCommands) {
		let t = [], n = await f(e.subCommands);
		for (let [e, r] of Object.entries(n)) {
			let n = await f((await f(r))?.meta);
			n?.hidden || (c.push([v(e), n?.description || ``]), t.push(e));
		}
		l.push(t.join(`|`));
	}
	let u = [], p = n.version || i.version;
	u.push(y(`${n.description} (${a + (p ? ` v${p}` : ``)})`), ``);
	let m = o.length > 0 || s.length > 0;
	return u.push(`${b(_(`USAGE`))} ${v(`${a}${m ? ` [OPTIONS]` : ``} ${l.join(` `)}`)}`, ``), s.length > 0 && (u.push(b(_(`ARGUMENTS`)), ``), u.push(d(s, `  `)), u.push(``)), o.length > 0 && (u.push(b(_(`OPTIONS`)), ``), u.push(d(o, `  `)), u.push(``)), c.length > 0 && (u.push(b(_(`COMMANDS`)), ``), u.push(d(c, `  `)), u.push(``, `Use ${v(`${a} <command> --help`)} for more information about a command.`)), u.filter((e) => typeof e == `string`).join(`
`);
}
async function k(e, t = {}) {
	let n = t.rawArgs || process.argv.slice(2), r = t.showUsage || E;
	try {
		if (n.includes(`--help`) || n.includes(`-h`)) await r(...await T(e, n)), process.exit(0);
		else if (n.length === 1 && n[0] === `--version`) {
			let t = typeof e.meta == `function` ? await e.meta() : await e.meta;
			if (!t?.version) throw new p(`No version specified`, `E_NO_VERSION`);
			console.log(t.version);
		} else await w(e, { rawArgs: n });
	} catch (t) {
		t instanceof p ? (await r(...await T(e, n)), console.error(t.message)) : console.error(t, `
`), process.exit(1);
	}
}
export { k as n, C as t };
