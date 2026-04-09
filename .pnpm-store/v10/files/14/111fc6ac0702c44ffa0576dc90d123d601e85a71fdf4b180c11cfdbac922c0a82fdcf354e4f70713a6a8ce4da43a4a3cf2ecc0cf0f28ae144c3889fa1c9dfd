import { t as e } from "../rolldown-runtime.mjs";
import t from "node:fs";
import n from "node:fs/promises";
import r from "node:stream";
import i, { basename as a, join as o, posix as s, win32 as c } from "node:path";
import l, { EventEmitter as u } from "events";
import d from "fs";
import { EventEmitter as f } from "node:events";
import { StringDecoder as ee } from "node:string_decoder";
import p, { dirname as m, parse as te } from "path";
import ne from "assert";
import { Buffer as re } from "buffer";
import * as ie from "zlib";
import ae from "zlib";
import oe from "node:assert";
import { randomBytes as se } from "node:crypto";
var ce = e({
	Header: () => I,
	Pack: () => ni,
	PackJob: () => Ir,
	PackSync: () => ri,
	Parser: () => Jn,
	Pax: () => hn,
	ReadEntry: () => yn,
	Unpack: () => _a,
	UnpackSync: () => ya,
	WriteEntry: () => Dr,
	WriteEntrySync: () => Or,
	WriteEntryTar: () => kr,
	c: () => ci,
	create: () => ci,
	extract: () => ba,
	filesFilter: () => Zn,
	list: () => Qn,
	r: () => Ea,
	replace: () => Ea,
	t: () => Qn,
	types: () => Xt,
	x: () => ba
}), le = Object.defineProperty, ue = (e, t) => {
	for (var n in t) le(e, n, {
		get: t[n],
		enumerable: !0
	});
}, de = typeof process == `object` && process ? process : {
	stdout: null,
	stderr: null
}, fe = (e) => !!e && typeof e == `object` && (e instanceof Ue || e instanceof r || pe(e) || me(e)), pe = (e) => !!e && typeof e == `object` && e instanceof f && typeof e.pipe == `function` && e.pipe !== r.Writable.prototype.pipe, me = (e) => !!e && typeof e == `object` && e instanceof f && typeof e.write == `function` && typeof e.end == `function`, h = Symbol(`EOF`), g = Symbol(`maybeEmitEnd`), _ = Symbol(`emittedEnd`), he = Symbol(`emittingEnd`), ge = Symbol(`emittedError`), _e = Symbol(`closed`), ve = Symbol(`read`), ye = Symbol(`flush`), be = Symbol(`flushChunk`), v = Symbol(`encoding`), xe = Symbol(`decoder`), y = Symbol(`flowing`), Se = Symbol(`paused`), Ce = Symbol(`resume`), b = Symbol(`buffer`), x = Symbol(`pipes`), S = Symbol(`bufferLength`), we = Symbol(`bufferPush`), Te = Symbol(`bufferShift`), C = Symbol(`objectMode`), w = Symbol(`destroyed`), Ee = Symbol(`error`), De = Symbol(`emitData`), Oe = Symbol(`emitEnd`), ke = Symbol(`emitEnd2`), T = Symbol(`async`), Ae = Symbol(`abort`), je = Symbol(`aborted`), Me = Symbol(`signal`), Ne = Symbol(`dataListeners`), E = Symbol(`discarded`), Pe = (e) => Promise.resolve().then(e), Fe = (e) => e(), Ie = (e) => e === `end` || e === `finish` || e === `prefinish`, Le = (e) => e instanceof ArrayBuffer || !!e && typeof e == `object` && e.constructor && e.constructor.name === `ArrayBuffer` && e.byteLength >= 0, Re = (e) => !Buffer.isBuffer(e) && ArrayBuffer.isView(e), ze = class {
	src;
	dest;
	opts;
	ondrain;
	constructor(e, t, n) {
		this.src = e, this.dest = t, this.opts = n, this.ondrain = () => e[Ce](), this.dest.on(`drain`, this.ondrain);
	}
	unpipe() {
		this.dest.removeListener(`drain`, this.ondrain);
	}
	proxyErrors(e) {}
	end() {
		this.unpipe(), this.opts.end && this.dest.end();
	}
}, Be = class extends ze {
	unpipe() {
		this.src.removeListener(`error`, this.proxyErrors), super.unpipe();
	}
	constructor(e, t, n) {
		super(e, t, n), this.proxyErrors = (e) => this.dest.emit(`error`, e), e.on(`error`, this.proxyErrors);
	}
}, Ve = (e) => !!e.objectMode, He = (e) => !e.objectMode && !!e.encoding && e.encoding !== `buffer`, Ue = class extends f {
	[y] = !1;
	[Se] = !1;
	[x] = [];
	[b] = [];
	[C];
	[v];
	[T];
	[xe];
	[h] = !1;
	[_] = !1;
	[he] = !1;
	[_e] = !1;
	[ge] = null;
	[S] = 0;
	[w] = !1;
	[Me];
	[je] = !1;
	[Ne] = 0;
	[E] = !1;
	writable = !0;
	readable = !0;
	constructor(...e) {
		let t = e[0] || {};
		if (super(), t.objectMode && typeof t.encoding == `string`) throw TypeError(`Encoding and objectMode may not be used together`);
		Ve(t) ? (this[C] = !0, this[v] = null) : He(t) ? (this[v] = t.encoding, this[C] = !1) : (this[C] = !1, this[v] = null), this[T] = !!t.async, this[xe] = this[v] ? new ee(this[v]) : null, t && t.debugExposeBuffer === !0 && Object.defineProperty(this, `buffer`, { get: () => this[b] }), t && t.debugExposePipes === !0 && Object.defineProperty(this, `pipes`, { get: () => this[x] });
		let { signal: n } = t;
		n && (this[Me] = n, n.aborted ? this[Ae]() : n.addEventListener(`abort`, () => this[Ae]()));
	}
	get bufferLength() {
		return this[S];
	}
	get encoding() {
		return this[v];
	}
	set encoding(e) {
		throw Error(`Encoding must be set at instantiation time`);
	}
	setEncoding(e) {
		throw Error(`Encoding must be set at instantiation time`);
	}
	get objectMode() {
		return this[C];
	}
	set objectMode(e) {
		throw Error(`objectMode must be set at instantiation time`);
	}
	get async() {
		return this[T];
	}
	set async(e) {
		this[T] = this[T] || !!e;
	}
	[Ae]() {
		this[je] = !0, this.emit(`abort`, this[Me]?.reason), this.destroy(this[Me]?.reason);
	}
	get aborted() {
		return this[je];
	}
	set aborted(e) {}
	write(e, t, n) {
		if (this[je]) return !1;
		if (this[h]) throw Error(`write after end`);
		if (this[w]) return this.emit(`error`, Object.assign(Error(`Cannot call write after a stream was destroyed`), { code: `ERR_STREAM_DESTROYED` })), !0;
		typeof t == `function` && (n = t, t = `utf8`), t ||= `utf8`;
		let r = this[T] ? Pe : Fe;
		if (!this[C] && !Buffer.isBuffer(e)) {
			if (Re(e)) e = Buffer.from(e.buffer, e.byteOffset, e.byteLength);
			else if (Le(e)) e = Buffer.from(e);
			else if (typeof e != `string`) throw Error(`Non-contiguous data written to non-objectMode stream`);
		}
		return this[C] ? (this[y] && this[S] !== 0 && this[ye](!0), this[y] ? this.emit(`data`, e) : this[we](e), this[S] !== 0 && this.emit(`readable`), n && r(n), this[y]) : e.length ? (typeof e == `string` && !(t === this[v] && !this[xe]?.lastNeed) && (e = Buffer.from(e, t)), Buffer.isBuffer(e) && this[v] && (e = this[xe].write(e)), this[y] && this[S] !== 0 && this[ye](!0), this[y] ? this.emit(`data`, e) : this[we](e), this[S] !== 0 && this.emit(`readable`), n && r(n), this[y]) : (this[S] !== 0 && this.emit(`readable`), n && r(n), this[y]);
	}
	read(e) {
		if (this[w]) return null;
		if (this[E] = !1, this[S] === 0 || e === 0 || e && e > this[S]) return this[g](), null;
		this[C] && (e = null), this[b].length > 1 && !this[C] && (this[b] = [this[v] ? this[b].join(``) : Buffer.concat(this[b], this[S])]);
		let t = this[ve](e || null, this[b][0]);
		return this[g](), t;
	}
	[ve](e, t) {
		if (this[C]) this[Te]();
		else {
			let n = t;
			e === n.length || e === null ? this[Te]() : typeof n == `string` ? (this[b][0] = n.slice(e), t = n.slice(0, e), this[S] -= e) : (this[b][0] = n.subarray(e), t = n.subarray(0, e), this[S] -= e);
		}
		return this.emit(`data`, t), !this[b].length && !this[h] && this.emit(`drain`), t;
	}
	end(e, t, n) {
		return typeof e == `function` && (n = e, e = void 0), typeof t == `function` && (n = t, t = `utf8`), e !== void 0 && this.write(e, t), n && this.once(`end`, n), this[h] = !0, this.writable = !1, (this[y] || !this[Se]) && this[g](), this;
	}
	[Ce]() {
		this[w] || (!this[Ne] && !this[x].length && (this[E] = !0), this[Se] = !1, this[y] = !0, this.emit(`resume`), this[b].length ? this[ye]() : this[h] ? this[g]() : this.emit(`drain`));
	}
	resume() {
		return this[Ce]();
	}
	pause() {
		this[y] = !1, this[Se] = !0, this[E] = !1;
	}
	get destroyed() {
		return this[w];
	}
	get flowing() {
		return this[y];
	}
	get paused() {
		return this[Se];
	}
	[we](e) {
		this[C] ? this[S] += 1 : this[S] += e.length, this[b].push(e);
	}
	[Te]() {
		return this[C] ? --this[S] : this[S] -= this[b][0].length, this[b].shift();
	}
	[ye](e = !1) {
		do		;
while (this[be](this[Te]()) && this[b].length);
		!e && !this[b].length && !this[h] && this.emit(`drain`);
	}
	[be](e) {
		return this.emit(`data`, e), this[y];
	}
	pipe(e, t) {
		if (this[w]) return e;
		this[E] = !1;
		let n = this[_];
		return t ||= {}, e === de.stdout || e === de.stderr ? t.end = !1 : t.end = t.end !== !1, t.proxyErrors = !!t.proxyErrors, n ? t.end && e.end() : (this[x].push(t.proxyErrors ? new Be(this, e, t) : new ze(this, e, t)), this[T] ? Pe(() => this[Ce]()) : this[Ce]()), e;
	}
	unpipe(e) {
		let t = this[x].find((t) => t.dest === e);
		t && (this[x].length === 1 ? (this[y] && this[Ne] === 0 && (this[y] = !1), this[x] = []) : this[x].splice(this[x].indexOf(t), 1), t.unpipe());
	}
	addListener(e, t) {
		return this.on(e, t);
	}
	on(e, t) {
		let n = super.on(e, t);
		if (e === `data`) this[E] = !1, this[Ne]++, !this[x].length && !this[y] && this[Ce]();
		else if (e === `readable` && this[S] !== 0) super.emit(`readable`);
		else if (Ie(e) && this[_]) super.emit(e), this.removeAllListeners(e);
		else if (e === `error` && this[ge]) {
			let e = t;
			this[T] ? Pe(() => e.call(this, this[ge])) : e.call(this, this[ge]);
		}
		return n;
	}
	removeListener(e, t) {
		return this.off(e, t);
	}
	off(e, t) {
		let n = super.off(e, t);
		return e === `data` && (this[Ne] = this.listeners(`data`).length, this[Ne] === 0 && !this[E] && !this[x].length && (this[y] = !1)), n;
	}
	removeAllListeners(e) {
		let t = super.removeAllListeners(e);
		return (e === `data` || e === void 0) && (this[Ne] = 0, !this[E] && !this[x].length && (this[y] = !1)), t;
	}
	get emittedEnd() {
		return this[_];
	}
	[g]() {
		!this[he] && !this[_] && !this[w] && this[b].length === 0 && this[h] && (this[he] = !0, this.emit(`end`), this.emit(`prefinish`), this.emit(`finish`), this[_e] && this.emit(`close`), this[he] = !1);
	}
	emit(e, ...t) {
		let n = t[0];
		if (e !== `error` && e !== `close` && e !== w && this[w]) return !1;
		if (e === `data`) return !this[C] && !n ? !1 : this[T] ? (Pe(() => this[De](n)), !0) : this[De](n);
		if (e === `end`) return this[Oe]();
		if (e === `close`) {
			if (this[_e] = !0, !this[_] && !this[w]) return !1;
			let e = super.emit(`close`);
			return this.removeAllListeners(`close`), e;
		} else if (e === `error`) {
			this[ge] = n, super.emit(Ee, n);
			let e = !this[Me] || this.listeners(`error`).length ? super.emit(`error`, n) : !1;
			return this[g](), e;
		} else if (e === `resume`) {
			let e = super.emit(`resume`);
			return this[g](), e;
		} else if (e === `finish` || e === `prefinish`) {
			let t = super.emit(e);
			return this.removeAllListeners(e), t;
		}
		let r = super.emit(e, ...t);
		return this[g](), r;
	}
	[De](e) {
		for (let t of this[x]) t.dest.write(e) === !1 && this.pause();
		let t = this[E] ? !1 : super.emit(`data`, e);
		return this[g](), t;
	}
	[Oe]() {
		return this[_] ? !1 : (this[_] = !0, this.readable = !1, this[T] ? (Pe(() => this[ke]()), !0) : this[ke]());
	}
	[ke]() {
		if (this[xe]) {
			let e = this[xe].end();
			if (e) {
				for (let t of this[x]) t.dest.write(e);
				this[E] || super.emit(`data`, e);
			}
		}
		for (let e of this[x]) e.end();
		let e = super.emit(`end`);
		return this.removeAllListeners(`end`), e;
	}
	async collect() {
		let e = Object.assign([], { dataLength: 0 });
		this[C] || (e.dataLength = 0);
		let t = this.promise();
		return this.on(`data`, (t) => {
			e.push(t), this[C] || (e.dataLength += t.length);
		}), await t, e;
	}
	async concat() {
		if (this[C]) throw Error(`cannot concat in objectMode`);
		let e = await this.collect();
		return this[v] ? e.join(``) : Buffer.concat(e, e.dataLength);
	}
	async promise() {
		return new Promise((e, t) => {
			this.on(w, () => t(Error(`stream destroyed`))), this.on(`error`, (e) => t(e)), this.on(`end`, () => e());
		});
	}
	[Symbol.asyncIterator]() {
		this[E] = !1;
		let e = !1, t = async () => (this.pause(), e = !0, {
			value: void 0,
			done: !0
		});
		return {
			next: () => {
				if (e) return t();
				let n = this.read();
				if (n !== null) return Promise.resolve({
					done: !1,
					value: n
				});
				if (this[h]) return t();
				let r, i, a = (e) => {
					this.off(`data`, o), this.off(`end`, s), this.off(w, c), t(), i(e);
				}, o = (e) => {
					this.off(`error`, a), this.off(`end`, s), this.off(w, c), this.pause(), r({
						value: e,
						done: !!this[h]
					});
				}, s = () => {
					this.off(`error`, a), this.off(`data`, o), this.off(w, c), t(), r({
						done: !0,
						value: void 0
					});
				}, c = () => a(Error(`stream destroyed`));
				return new Promise((e, t) => {
					i = t, r = e, this.once(w, c), this.once(`error`, a), this.once(`end`, s), this.once(`data`, o);
				});
			},
			throw: t,
			return: t,
			[Symbol.asyncIterator]() {
				return this;
			},
			[Symbol.asyncDispose]: async () => {}
		};
	}
	[Symbol.iterator]() {
		this[E] = !1;
		let e = !1, t = () => (this.pause(), this.off(Ee, t), this.off(w, t), this.off(`end`, t), e = !0, {
			done: !0,
			value: void 0
		});
		return this.once(`end`, t), this.once(Ee, t), this.once(w, t), {
			next: () => {
				if (e) return t();
				let n = this.read();
				return n === null ? t() : {
					done: !1,
					value: n
				};
			},
			throw: t,
			return: t,
			[Symbol.iterator]() {
				return this;
			},
			[Symbol.dispose]: () => {}
		};
	}
	destroy(e) {
		if (this[w]) return e ? this.emit(`error`, e) : this.emit(w), this;
		this[w] = !0, this[E] = !0, this[b].length = 0, this[S] = 0;
		let t = this;
		return typeof t.close == `function` && !this[_e] && t.close(), e ? this.emit(`error`, e) : this.emit(w), this;
	}
	static get isStream() {
		return fe;
	}
}, We = d.writev, D = Symbol(`_autoClose`), O = Symbol(`_close`), Ge = Symbol(`_ended`), k = Symbol(`_fd`), Ke = Symbol(`_finished`), A = Symbol(`_flags`), qe = Symbol(`_flush`), Je = Symbol(`_handleChunk`), Ye = Symbol(`_makeBuf`), Xe = Symbol(`_mode`), Ze = Symbol(`_needDrain`), Qe = Symbol(`_onerror`), $e = Symbol(`_onopen`), et = Symbol(`_onread`), tt = Symbol(`_onwrite`), j = Symbol(`_open`), M = Symbol(`_path`), nt = Symbol(`_pos`), N = Symbol(`_queue`), rt = Symbol(`_read`), it = Symbol(`_readSize`), P = Symbol(`_reading`), at = Symbol(`_remain`), ot = Symbol(`_size`), st = Symbol(`_write`), ct = Symbol(`_writing`), lt = Symbol(`_defaultFlag`), ut = Symbol(`_errored`), dt = class extends Ue {
	[ut] = !1;
	[k];
	[M];
	[it];
	[P] = !1;
	[ot];
	[at];
	[D];
	constructor(e, t) {
		if (t ||= {}, super(t), this.readable = !0, this.writable = !1, typeof e != `string`) throw TypeError(`path must be a string`);
		this[ut] = !1, this[k] = typeof t.fd == `number` ? t.fd : void 0, this[M] = e, this[it] = t.readSize || 16 * 1024 * 1024, this[P] = !1, this[ot] = typeof t.size == `number` ? t.size : Infinity, this[at] = this[ot], this[D] = typeof t.autoClose == `boolean` ? t.autoClose : !0, typeof this[k] == `number` ? this[rt]() : this[j]();
	}
	get fd() {
		return this[k];
	}
	get path() {
		return this[M];
	}
	write() {
		throw TypeError(`this is a readable stream`);
	}
	end() {
		throw TypeError(`this is a readable stream`);
	}
	[j]() {
		d.open(this[M], `r`, (e, t) => this[$e](e, t));
	}
	[$e](e, t) {
		e ? this[Qe](e) : (this[k] = t, this.emit(`open`, t), this[rt]());
	}
	[Ye]() {
		return Buffer.allocUnsafe(Math.min(this[it], this[at]));
	}
	[rt]() {
		if (!this[P]) {
			this[P] = !0;
			let e = this[Ye]();
			if (e.length === 0) return process.nextTick(() => this[et](null, 0, e));
			d.read(this[k], e, 0, e.length, null, (e, t, n) => this[et](e, t, n));
		}
	}
	[et](e, t, n) {
		this[P] = !1, e ? this[Qe](e) : this[Je](t, n) && this[rt]();
	}
	[O]() {
		if (this[D] && typeof this[k] == `number`) {
			let e = this[k];
			this[k] = void 0, d.close(e, (e) => e ? this.emit(`error`, e) : this.emit(`close`));
		}
	}
	[Qe](e) {
		this[P] = !0, this[O](), this.emit(`error`, e);
	}
	[Je](e, t) {
		let n = !1;
		return this[at] -= e, e > 0 && (n = super.write(e < t.length ? t.subarray(0, e) : t)), (e === 0 || this[at] <= 0) && (n = !1, this[O](), super.end()), n;
	}
	emit(e, ...t) {
		switch (e) {
			case `prefinish`:
			case `finish`: return !1;
			case `drain`: return typeof this[k] == `number` && this[rt](), !1;
			case `error`: return this[ut] ? !1 : (this[ut] = !0, super.emit(e, ...t));
			default: return super.emit(e, ...t);
		}
	}
}, ft = class extends dt {
	[j]() {
		let e = !0;
		try {
			this[$e](null, d.openSync(this[M], `r`)), e = !1;
		} finally {
			e && this[O]();
		}
	}
	[rt]() {
		let e = !0;
		try {
			if (!this[P]) {
				this[P] = !0;
				do {
					let e = this[Ye](), t = e.length === 0 ? 0 : d.readSync(this[k], e, 0, e.length, null);
					if (!this[Je](t, e)) break;
				} while (!0);
				this[P] = !1;
			}
			e = !1;
		} finally {
			e && this[O]();
		}
	}
	[O]() {
		if (this[D] && typeof this[k] == `number`) {
			let e = this[k];
			this[k] = void 0, d.closeSync(e), this.emit(`close`);
		}
	}
}, pt = class extends l {
	readable = !1;
	writable = !0;
	[ut] = !1;
	[ct] = !1;
	[Ge] = !1;
	[N] = [];
	[Ze] = !1;
	[M];
	[Xe];
	[D];
	[k];
	[lt];
	[A];
	[Ke] = !1;
	[nt];
	constructor(e, t) {
		t ||= {}, super(t), this[M] = e, this[k] = typeof t.fd == `number` ? t.fd : void 0, this[Xe] = t.mode === void 0 ? 438 : t.mode, this[nt] = typeof t.start == `number` ? t.start : void 0, this[D] = typeof t.autoClose == `boolean` ? t.autoClose : !0;
		let n = this[nt] === void 0 ? `w` : `r+`;
		this[lt] = t.flags === void 0, this[A] = t.flags === void 0 ? n : t.flags, this[k] === void 0 && this[j]();
	}
	emit(e, ...t) {
		if (e === `error`) {
			if (this[ut]) return !1;
			this[ut] = !0;
		}
		return super.emit(e, ...t);
	}
	get fd() {
		return this[k];
	}
	get path() {
		return this[M];
	}
	[Qe](e) {
		this[O](), this[ct] = !0, this.emit(`error`, e);
	}
	[j]() {
		d.open(this[M], this[A], this[Xe], (e, t) => this[$e](e, t));
	}
	[$e](e, t) {
		this[lt] && this[A] === `r+` && e && e.code === `ENOENT` ? (this[A] = `w`, this[j]()) : e ? this[Qe](e) : (this[k] = t, this.emit(`open`, t), this[ct] || this[qe]());
	}
	end(e, t) {
		return e && this.write(e, t), this[Ge] = !0, !this[ct] && !this[N].length && typeof this[k] == `number` && this[tt](null, 0), this;
	}
	write(e, t) {
		return typeof e == `string` && (e = Buffer.from(e, t)), this[Ge] ? (this.emit(`error`, Error(`write() after end()`)), !1) : this[k] === void 0 || this[ct] || this[N].length ? (this[N].push(e), this[Ze] = !0, !1) : (this[ct] = !0, this[st](e), !0);
	}
	[st](e) {
		d.write(this[k], e, 0, e.length, this[nt], (e, t) => this[tt](e, t));
	}
	[tt](e, t) {
		e ? this[Qe](e) : (this[nt] !== void 0 && typeof t == `number` && (this[nt] += t), this[N].length ? this[qe]() : (this[ct] = !1, this[Ge] && !this[Ke] ? (this[Ke] = !0, this[O](), this.emit(`finish`)) : this[Ze] && (this[Ze] = !1, this.emit(`drain`))));
	}
	[qe]() {
		if (this[N].length === 0) this[Ge] && this[tt](null, 0);
		else if (this[N].length === 1) this[st](this[N].pop());
		else {
			let e = this[N];
			this[N] = [], We(this[k], e, this[nt], (e, t) => this[tt](e, t));
		}
	}
	[O]() {
		if (this[D] && typeof this[k] == `number`) {
			let e = this[k];
			this[k] = void 0, d.close(e, (e) => e ? this.emit(`error`, e) : this.emit(`close`));
		}
	}
}, mt = class extends pt {
	[j]() {
		let e;
		if (this[lt] && this[A] === `r+`) try {
			e = d.openSync(this[M], this[A], this[Xe]);
		} catch (e) {
			if (e?.code === `ENOENT`) return this[A] = `w`, this[j]();
			throw e;
		}
		else e = d.openSync(this[M], this[A], this[Xe]);
		this[$e](null, e);
	}
	[O]() {
		if (this[D] && typeof this[k] == `number`) {
			let e = this[k];
			this[k] = void 0, d.closeSync(e), this.emit(`close`);
		}
	}
	[st](e) {
		let t = !0;
		try {
			this[tt](null, d.writeSync(this[k], e, 0, e.length, this[nt])), t = !1;
		} finally {
			if (t) try {
				this[O]();
			} catch {}
		}
	}
}, ht = new Map([
	[`C`, `cwd`],
	[`f`, `file`],
	[`z`, `gzip`],
	[`P`, `preservePaths`],
	[`U`, `unlink`],
	[`strip-components`, `strip`],
	[`stripComponents`, `strip`],
	[`keep-newer`, `newer`],
	[`keepNewer`, `newer`],
	[`keep-newer-files`, `newer`],
	[`keepNewerFiles`, `newer`],
	[`k`, `keep`],
	[`keep-existing`, `keep`],
	[`keepExisting`, `keep`],
	[`m`, `noMtime`],
	[`no-mtime`, `noMtime`],
	[`p`, `preserveOwner`],
	[`L`, `follow`],
	[`h`, `follow`],
	[`onentry`, `onReadEntry`]
]), gt = (e) => !!e.sync && !!e.file, _t = (e) => !e.sync && !!e.file, vt = (e) => !!e.sync && !e.file, yt = (e) => !e.sync && !e.file, bt = (e) => !!e.file, xt = (e) => ht.get(e) || e, St = (e = {}) => {
	if (!e) return {};
	let t = {};
	for (let [n, r] of Object.entries(e)) {
		let e = xt(n);
		t[e] = r;
	}
	return t.chmod === void 0 && t.noChmod === !1 && (t.chmod = !0), delete t.noChmod, t;
}, Ct = (e, t, n, r, i) => Object.assign((a = [], o, s) => {
	Array.isArray(a) && (o = a, a = {}), typeof o == `function` && (s = o, o = void 0), o = o ? Array.from(o) : [];
	let c = St(a);
	if (i?.(c, o), gt(c)) {
		if (typeof s == `function`) throw TypeError(`callback not supported for sync tar functions`);
		return e(c, o);
	} else if (_t(c)) {
		let e = t(c, o);
		return s ? e.then(() => s(), s) : e;
	} else if (vt(c)) {
		if (typeof s == `function`) throw TypeError(`callback not supported for sync tar functions`);
		return n(c, o);
	} else if (yt(c)) {
		if (typeof s == `function`) throw TypeError(`callback only supported with file option`);
		return r(c, o);
	}
	throw Error(`impossible options??`);
}, {
	syncFile: e,
	asyncFile: t,
	syncNoFile: n,
	asyncNoFile: r,
	validate: i
}), wt = ae.constants || { ZLIB_VERNUM: 4736 }, F = Object.freeze(Object.assign(Object.create(null), {
	Z_NO_FLUSH: 0,
	Z_PARTIAL_FLUSH: 1,
	Z_SYNC_FLUSH: 2,
	Z_FULL_FLUSH: 3,
	Z_FINISH: 4,
	Z_BLOCK: 5,
	Z_OK: 0,
	Z_STREAM_END: 1,
	Z_NEED_DICT: 2,
	Z_ERRNO: -1,
	Z_STREAM_ERROR: -2,
	Z_DATA_ERROR: -3,
	Z_MEM_ERROR: -4,
	Z_BUF_ERROR: -5,
	Z_VERSION_ERROR: -6,
	Z_NO_COMPRESSION: 0,
	Z_BEST_SPEED: 1,
	Z_BEST_COMPRESSION: 9,
	Z_DEFAULT_COMPRESSION: -1,
	Z_FILTERED: 1,
	Z_HUFFMAN_ONLY: 2,
	Z_RLE: 3,
	Z_FIXED: 4,
	Z_DEFAULT_STRATEGY: 0,
	DEFLATE: 1,
	INFLATE: 2,
	GZIP: 3,
	GUNZIP: 4,
	DEFLATERAW: 5,
	INFLATERAW: 6,
	UNZIP: 7,
	BROTLI_DECODE: 8,
	BROTLI_ENCODE: 9,
	Z_MIN_WINDOWBITS: 8,
	Z_MAX_WINDOWBITS: 15,
	Z_DEFAULT_WINDOWBITS: 15,
	Z_MIN_CHUNK: 64,
	Z_MAX_CHUNK: Infinity,
	Z_DEFAULT_CHUNK: 16384,
	Z_MIN_MEMLEVEL: 1,
	Z_MAX_MEMLEVEL: 9,
	Z_DEFAULT_MEMLEVEL: 8,
	Z_MIN_LEVEL: -1,
	Z_MAX_LEVEL: 9,
	Z_DEFAULT_LEVEL: -1,
	BROTLI_OPERATION_PROCESS: 0,
	BROTLI_OPERATION_FLUSH: 1,
	BROTLI_OPERATION_FINISH: 2,
	BROTLI_OPERATION_EMIT_METADATA: 3,
	BROTLI_MODE_GENERIC: 0,
	BROTLI_MODE_TEXT: 1,
	BROTLI_MODE_FONT: 2,
	BROTLI_DEFAULT_MODE: 0,
	BROTLI_MIN_QUALITY: 0,
	BROTLI_MAX_QUALITY: 11,
	BROTLI_DEFAULT_QUALITY: 11,
	BROTLI_MIN_WINDOW_BITS: 10,
	BROTLI_MAX_WINDOW_BITS: 24,
	BROTLI_LARGE_MAX_WINDOW_BITS: 30,
	BROTLI_DEFAULT_WINDOW: 22,
	BROTLI_MIN_INPUT_BLOCK_BITS: 16,
	BROTLI_MAX_INPUT_BLOCK_BITS: 24,
	BROTLI_PARAM_MODE: 0,
	BROTLI_PARAM_QUALITY: 1,
	BROTLI_PARAM_LGWIN: 2,
	BROTLI_PARAM_LGBLOCK: 3,
	BROTLI_PARAM_DISABLE_LITERAL_CONTEXT_MODELING: 4,
	BROTLI_PARAM_SIZE_HINT: 5,
	BROTLI_PARAM_LARGE_WINDOW: 6,
	BROTLI_PARAM_NPOSTFIX: 7,
	BROTLI_PARAM_NDIRECT: 8,
	BROTLI_DECODER_RESULT_ERROR: 0,
	BROTLI_DECODER_RESULT_SUCCESS: 1,
	BROTLI_DECODER_RESULT_NEEDS_MORE_INPUT: 2,
	BROTLI_DECODER_RESULT_NEEDS_MORE_OUTPUT: 3,
	BROTLI_DECODER_PARAM_DISABLE_RING_BUFFER_REALLOCATION: 0,
	BROTLI_DECODER_PARAM_LARGE_WINDOW: 1,
	BROTLI_DECODER_NO_ERROR: 0,
	BROTLI_DECODER_SUCCESS: 1,
	BROTLI_DECODER_NEEDS_MORE_INPUT: 2,
	BROTLI_DECODER_NEEDS_MORE_OUTPUT: 3,
	BROTLI_DECODER_ERROR_FORMAT_EXUBERANT_NIBBLE: -1,
	BROTLI_DECODER_ERROR_FORMAT_RESERVED: -2,
	BROTLI_DECODER_ERROR_FORMAT_EXUBERANT_META_NIBBLE: -3,
	BROTLI_DECODER_ERROR_FORMAT_SIMPLE_HUFFMAN_ALPHABET: -4,
	BROTLI_DECODER_ERROR_FORMAT_SIMPLE_HUFFMAN_SAME: -5,
	BROTLI_DECODER_ERROR_FORMAT_CL_SPACE: -6,
	BROTLI_DECODER_ERROR_FORMAT_HUFFMAN_SPACE: -7,
	BROTLI_DECODER_ERROR_FORMAT_CONTEXT_MAP_REPEAT: -8,
	BROTLI_DECODER_ERROR_FORMAT_BLOCK_LENGTH_1: -9,
	BROTLI_DECODER_ERROR_FORMAT_BLOCK_LENGTH_2: -10,
	BROTLI_DECODER_ERROR_FORMAT_TRANSFORM: -11,
	BROTLI_DECODER_ERROR_FORMAT_DICTIONARY: -12,
	BROTLI_DECODER_ERROR_FORMAT_WINDOW_BITS: -13,
	BROTLI_DECODER_ERROR_FORMAT_PADDING_1: -14,
	BROTLI_DECODER_ERROR_FORMAT_PADDING_2: -15,
	BROTLI_DECODER_ERROR_FORMAT_DISTANCE: -16,
	BROTLI_DECODER_ERROR_DICTIONARY_NOT_SET: -19,
	BROTLI_DECODER_ERROR_INVALID_ARGUMENTS: -20,
	BROTLI_DECODER_ERROR_ALLOC_CONTEXT_MODES: -21,
	BROTLI_DECODER_ERROR_ALLOC_TREE_GROUPS: -22,
	BROTLI_DECODER_ERROR_ALLOC_CONTEXT_MAP: -25,
	BROTLI_DECODER_ERROR_ALLOC_RING_BUFFER_1: -26,
	BROTLI_DECODER_ERROR_ALLOC_RING_BUFFER_2: -27,
	BROTLI_DECODER_ERROR_ALLOC_BLOCK_TYPE_TREES: -30,
	BROTLI_DECODER_ERROR_UNREACHABLE: -31
}, wt)), Tt = re.concat, Et = Object.getOwnPropertyDescriptor(re, `concat`), Dt = (e) => e, Ot = Et?.writable === !0 || Et?.set !== void 0 ? (e) => {
	re.concat = e ? Dt : Tt;
} : (e) => {}, kt = Symbol(`_superWrite`), At = class extends Error {
	code;
	errno;
	constructor(e, t) {
		super(`zlib: ` + e.message, { cause: e }), this.code = e.code, this.errno = e.errno, this.code ||= `ZLIB_ERROR`, this.message = `zlib: ` + e.message, Error.captureStackTrace(this, t ?? this.constructor);
	}
	get name() {
		return `ZlibError`;
	}
}, jt = Symbol(`flushFlag`), Mt = class extends Ue {
	#t = !1;
	#i = !1;
	#s;
	#n;
	#r;
	#e;
	#o;
	get sawError() {
		return this.#t;
	}
	get handle() {
		return this.#e;
	}
	get flushFlag() {
		return this.#s;
	}
	constructor(e, t) {
		if (!e || typeof e != `object`) throw TypeError(`invalid options for ZlibBase constructor`);
		if (super(e), this.#s = e.flush ?? 0, this.#n = e.finishFlush ?? 0, this.#r = e.fullFlushFlag ?? 0, typeof ie[t] != `function`) throw TypeError(`Compression method not supported: ` + t);
		try {
			this.#e = new ie[t](e);
		} catch (e) {
			throw new At(e, this.constructor);
		}
		this.#o = (e) => {
			this.#t || (this.#t = !0, this.close(), this.emit(`error`, e));
		}, this.#e?.on(`error`, (e) => this.#o(new At(e))), this.once(`end`, () => this.close);
	}
	close() {
		this.#e && (this.#e.close(), this.#e = void 0, this.emit(`close`));
	}
	reset() {
		if (!this.#t) return ne(this.#e, `zlib binding closed`), this.#e.reset?.();
	}
	flush(e) {
		this.ended || (typeof e != `number` && (e = this.#r), this.write(Object.assign(re.alloc(0), { [jt]: e })));
	}
	end(e, t, n) {
		return typeof e == `function` && (n = e, t = void 0, e = void 0), typeof t == `function` && (n = t, t = void 0), e && (t ? this.write(e, t) : this.write(e)), this.flush(this.#n), this.#i = !0, super.end(n);
	}
	get ended() {
		return this.#i;
	}
	[kt](e) {
		return super.write(e);
	}
	write(e, t, n) {
		if (typeof t == `function` && (n = t, t = `utf8`), typeof e == `string` && (e = re.from(e, t)), this.#t) return;
		ne(this.#e, `zlib binding closed`);
		let r = this.#e._handle, i = r.close;
		r.close = () => {};
		let a = this.#e.close;
		this.#e.close = () => {}, Ot(!0);
		let o;
		try {
			let t = typeof e[jt] == `number` ? e[jt] : this.#s;
			o = this.#e._processChunk(e, t), Ot(!1);
		} catch (e) {
			Ot(!1), this.#o(new At(e, this.write));
		} finally {
			this.#e && (this.#e._handle = r, r.close = i, this.#e.close = a, this.#e.removeAllListeners(`error`));
		}
		this.#e && this.#e.on(`error`, (e) => this.#o(new At(e, this.write)));
		let s;
		if (o) if (Array.isArray(o) && o.length > 0) {
			let e = o[0];
			s = this[kt](re.from(e));
			for (let e = 1; e < o.length; e++) s = this[kt](o[e]);
		} else s = this[kt](re.from(o));
		return n && n(), s;
	}
}, Nt = class extends Mt {
	#t;
	#i;
	constructor(e, t) {
		e ||= {}, e.flush = e.flush || F.Z_NO_FLUSH, e.finishFlush = e.finishFlush || F.Z_FINISH, e.fullFlushFlag = F.Z_FULL_FLUSH, super(e, t), this.#t = e.level, this.#i = e.strategy;
	}
	params(e, t) {
		if (!this.sawError) {
			if (!this.handle) throw Error(`cannot switch params when binding is closed`);
			if (!this.handle.params) throw Error(`not supported in this implementation`);
			if (this.#t !== e || this.#i !== t) {
				this.flush(F.Z_SYNC_FLUSH), ne(this.handle, `zlib binding closed`);
				let n = this.handle.flush;
				this.handle.flush = (e, t) => {
					typeof e == `function` && (t = e, e = this.flushFlag), this.flush(e), t?.();
				};
				try {
					this.handle.params(e, t);
				} finally {
					this.handle.flush = n;
				}
				this.handle && (this.#t = e, this.#i = t);
			}
		}
	}
}, Pt = class extends Nt {
	#t;
	constructor(e) {
		super(e, `Gzip`), this.#t = e && !!e.portable;
	}
	[kt](e) {
		return this.#t ? (this.#t = !1, e[9] = 255, super[kt](e)) : super[kt](e);
	}
}, Ft = class extends Nt {
	constructor(e) {
		super(e, `Unzip`);
	}
}, It = class extends Mt {
	constructor(e, t) {
		e ||= {}, e.flush = e.flush || F.BROTLI_OPERATION_PROCESS, e.finishFlush = e.finishFlush || F.BROTLI_OPERATION_FINISH, e.fullFlushFlag = F.BROTLI_OPERATION_FLUSH, super(e, t);
	}
}, Lt = class extends It {
	constructor(e) {
		super(e, `BrotliCompress`);
	}
}, Rt = class extends It {
	constructor(e) {
		super(e, `BrotliDecompress`);
	}
}, zt = class extends Mt {
	constructor(e, t) {
		e ||= {}, e.flush = e.flush || F.ZSTD_e_continue, e.finishFlush = e.finishFlush || F.ZSTD_e_end, e.fullFlushFlag = F.ZSTD_e_flush, super(e, t);
	}
}, Bt = class extends zt {
	constructor(e) {
		super(e, `ZstdCompress`);
	}
}, Vt = class extends zt {
	constructor(e) {
		super(e, `ZstdDecompress`);
	}
}, Ht = (e, t) => {
	if (Number.isSafeInteger(e)) e < 0 ? Wt(e, t) : Ut(e, t);
	else throw Error(`cannot encode number outside of javascript safe integer range`);
	return t;
}, Ut = (e, t) => {
	t[0] = 128;
	for (var n = t.length; n > 1; n--) t[n - 1] = e & 255, e = Math.floor(e / 256);
}, Wt = (e, t) => {
	t[0] = 255;
	var n = !1;
	e *= -1;
	for (var r = t.length; r > 1; r--) {
		var i = e & 255;
		e = Math.floor(e / 256), n ? t[r - 1] = Jt(i) : i === 0 ? t[r - 1] = 0 : (n = !0, t[r - 1] = Yt(i));
	}
}, Gt = (e) => {
	let t = e[0], n = t === 128 ? qt(e.subarray(1, e.length)) : t === 255 ? Kt(e) : null;
	if (n === null) throw Error(`invalid base256 encoding`);
	if (!Number.isSafeInteger(n)) throw Error(`parsed number outside of javascript safe integer range`);
	return n;
}, Kt = (e) => {
	for (var t = e.length, n = 0, r = !1, i = t - 1; i > -1; i--) {
		var a = Number(e[i]), o;
		r ? o = Jt(a) : a === 0 ? o = a : (r = !0, o = Yt(a)), o !== 0 && (n -= o * 256 ** (t - i - 1));
	}
	return n;
}, qt = (e) => {
	for (var t = e.length, n = 0, r = t - 1; r > -1; r--) {
		var i = Number(e[r]);
		i !== 0 && (n += i * 256 ** (t - r - 1));
	}
	return n;
}, Jt = (e) => (255 ^ e) & 255, Yt = (e) => (255 ^ e) + 1 & 255, Xt = {};
ue(Xt, {
	code: () => en,
	isCode: () => Zt,
	isName: () => Qt,
	name: () => $t
});
var Zt = (e) => $t.has(e), Qt = (e) => en.has(e), $t = new Map([
	[`0`, `File`],
	[``, `OldFile`],
	[`1`, `Link`],
	[`2`, `SymbolicLink`],
	[`3`, `CharacterDevice`],
	[`4`, `BlockDevice`],
	[`5`, `Directory`],
	[`6`, `FIFO`],
	[`7`, `ContiguousFile`],
	[`g`, `GlobalExtendedHeader`],
	[`x`, `ExtendedHeader`],
	[`A`, `SolarisACL`],
	[`D`, `GNUDumpDir`],
	[`I`, `Inode`],
	[`K`, `NextFileHasLongLinkpath`],
	[`L`, `NextFileHasLongPath`],
	[`M`, `ContinuationFile`],
	[`N`, `OldGnuLongPath`],
	[`S`, `SparseFile`],
	[`V`, `TapeVolumeHeader`],
	[`X`, `OldExtendedHeader`]
]), en = new Map(Array.from($t).map((e) => [e[1], e[0]])), I = class {
	cksumValid = !1;
	needPax = !1;
	nullBlock = !1;
	block;
	path;
	mode;
	uid;
	gid;
	size;
	cksum;
	#t = `Unsupported`;
	linkpath;
	uname;
	gname;
	devmaj = 0;
	devmin = 0;
	atime;
	ctime;
	mtime;
	charset;
	comment;
	constructor(e, t = 0, n, r) {
		Buffer.isBuffer(e) ? this.decode(e, t || 0, n, r) : e && this.#i(e);
	}
	decode(e, t, n, r) {
		if (t ||= 0, !e || !(e.length >= t + 512)) throw Error(`need 512 bytes for header`);
		this.path = n?.path ?? nn(e, t, 100), this.mode = n?.mode ?? r?.mode ?? L(e, t + 100, 8), this.uid = n?.uid ?? r?.uid ?? L(e, t + 108, 8), this.gid = n?.gid ?? r?.gid ?? L(e, t + 116, 8), this.size = n?.size ?? r?.size ?? L(e, t + 124, 12), this.mtime = n?.mtime ?? r?.mtime ?? rn(e, t + 136, 12), this.cksum = L(e, t + 148, 12), r && this.#i(r, !0), n && this.#i(n);
		let i = nn(e, t + 156, 1);
		if (Zt(i) && (this.#t = i || `0`), this.#t === `0` && this.path.slice(-1) === `/` && (this.#t = `5`), this.#t === `5` && (this.size = 0), this.linkpath = nn(e, t + 157, 100), e.subarray(t + 257, t + 265).toString() === `ustar\x0000`) if (this.uname = n?.uname ?? r?.uname ?? nn(e, t + 265, 32), this.gname = n?.gname ?? r?.gname ?? nn(e, t + 297, 32), this.devmaj = n?.devmaj ?? r?.devmaj ?? L(e, t + 329, 8) ?? 0, this.devmin = n?.devmin ?? r?.devmin ?? L(e, t + 337, 8) ?? 0, e[t + 475] !== 0) this.path = nn(e, t + 345, 155) + `/` + this.path;
		else {
			let i = nn(e, t + 345, 130);
			i && (this.path = i + `/` + this.path), this.atime = n?.atime ?? r?.atime ?? rn(e, t + 476, 12), this.ctime = n?.ctime ?? r?.ctime ?? rn(e, t + 488, 12);
		}
		let a = 256;
		for (let n = t; n < t + 148; n++) a += e[n];
		for (let n = t + 156; n < t + 512; n++) a += e[n];
		this.cksumValid = a === this.cksum, this.cksum === void 0 && a === 256 && (this.nullBlock = !0);
	}
	#i(e, t = !1) {
		Object.assign(this, Object.fromEntries(Object.entries(e).filter(([e, n]) => !(n == null || e === `path` && t || e === `linkpath` && t || e === `global`))));
	}
	encode(e, t = 0) {
		if (e ||= this.block = Buffer.alloc(512), this.#t === `Unsupported` && (this.#t = `0`), !(e.length >= t + 512)) throw Error(`need 512 bytes for header`);
		let n = this.ctime || this.atime ? 130 : 155, r = tn(this.path || ``, n), i = r[0], a = r[1];
		this.needPax = !!r[2], this.needPax = mn(e, t, 100, i) || this.needPax, this.needPax = R(e, t + 100, 8, this.mode) || this.needPax, this.needPax = R(e, t + 108, 8, this.uid) || this.needPax, this.needPax = R(e, t + 116, 8, this.gid) || this.needPax, this.needPax = R(e, t + 124, 12, this.size) || this.needPax, this.needPax = fn(e, t + 136, 12, this.mtime) || this.needPax, e[t + 156] = Number(this.#t.codePointAt(0)), this.needPax = mn(e, t + 157, 100, this.linkpath) || this.needPax, e.write(`ustar\x0000`, t + 257, 8), this.needPax = mn(e, t + 265, 32, this.uname) || this.needPax, this.needPax = mn(e, t + 297, 32, this.gname) || this.needPax, this.needPax = R(e, t + 329, 8, this.devmaj) || this.needPax, this.needPax = R(e, t + 337, 8, this.devmin) || this.needPax, this.needPax = mn(e, t + 345, n, a) || this.needPax, e[t + 475] === 0 ? (this.needPax = mn(e, t + 345, 130, a) || this.needPax, this.needPax = fn(e, t + 476, 12, this.atime) || this.needPax, this.needPax = fn(e, t + 488, 12, this.ctime) || this.needPax) : this.needPax = mn(e, t + 345, 155, a) || this.needPax;
		let o = 256;
		for (let n = t; n < t + 148; n++) o += e[n];
		for (let n = t + 156; n < t + 512; n++) o += e[n];
		return this.cksum = o, R(e, t + 148, 8, this.cksum), this.cksumValid = !0, this.needPax;
	}
	get type() {
		return this.#t === `Unsupported` ? this.#t : $t.get(this.#t);
	}
	get typeKey() {
		return this.#t;
	}
	set type(e) {
		let t = String(en.get(e));
		if (Zt(t) || t === `Unsupported`) this.#t = t;
		else if (Zt(e)) this.#t = e;
		else throw TypeError(`invalid entry type: ` + e);
	}
}, tn = (e, t) => {
	let n = e, r = ``, i, a = s.parse(e).root || `.`;
	if (Buffer.byteLength(n) < 100) i = [
		n,
		r,
		!1
	];
	else {
		r = s.dirname(n), n = s.basename(n);
		do
			Buffer.byteLength(n) <= 100 && Buffer.byteLength(r) <= t ? i = [
				n,
				r,
				!1
			] : Buffer.byteLength(n) > 100 && Buffer.byteLength(r) <= t ? i = [
				n.slice(0, 99),
				r,
				!0
			] : (n = s.join(s.basename(r), n), r = s.dirname(r));
		while (r !== a && i === void 0);
		i ||= [
			e.slice(0, 99),
			``,
			!0
		];
	}
	return i;
}, nn = (e, t, n) => e.subarray(t, t + n).toString(`utf8`).replace(/\0.*/, ``), rn = (e, t, n) => an(L(e, t, n)), an = (e) => e === void 0 ? void 0 : /* @__PURE__ */ new Date(e * 1e3), L = (e, t, n) => Number(e[t]) & 128 ? Gt(e.subarray(t, t + n)) : sn(e, t, n), on = (e) => isNaN(e) ? void 0 : e, sn = (e, t, n) => on(parseInt(e.subarray(t, t + n).toString(`utf8`).replace(/\0.*$/, ``).trim(), 8)), cn = {
	12: 8589934591,
	8: 2097151
}, R = (e, t, n, r) => r === void 0 ? !1 : r > cn[n] || r < 0 ? (Ht(r, e.subarray(t, t + n)), !0) : (ln(e, t, n, r), !1), ln = (e, t, n, r) => e.write(un(r, n), t, n, `ascii`), un = (e, t) => dn(Math.floor(e).toString(8), t), dn = (e, t) => (e.length === t - 1 ? e : Array(t - e.length - 1).join(`0`) + e + ` `) + `\0`, fn = (e, t, n, r) => r === void 0 ? !1 : R(e, t, n, r.getTime() / 1e3), pn = Array(156).join(`\0`), mn = (e, t, n, r) => r === void 0 ? !1 : (e.write(r + pn, t, n, `utf8`), r.length !== Buffer.byteLength(r) || r.length > n), hn = class e {
	atime;
	mtime;
	ctime;
	charset;
	comment;
	gid;
	uid;
	gname;
	uname;
	linkpath;
	dev;
	ino;
	nlink;
	path;
	size;
	mode;
	global;
	constructor(e, t = !1) {
		this.atime = e.atime, this.charset = e.charset, this.comment = e.comment, this.ctime = e.ctime, this.dev = e.dev, this.gid = e.gid, this.global = t, this.gname = e.gname, this.ino = e.ino, this.linkpath = e.linkpath, this.mtime = e.mtime, this.nlink = e.nlink, this.path = e.path, this.size = e.size, this.uid = e.uid, this.uname = e.uname;
	}
	encode() {
		let e = this.encodeBody();
		if (e === ``) return Buffer.allocUnsafe(0);
		let t = Buffer.byteLength(e), n = 512 * Math.ceil(1 + t / 512), r = Buffer.allocUnsafe(n);
		for (let e = 0; e < 512; e++) r[e] = 0;
		new I({
			path: (`PaxHeader/` + a(this.path ?? ``)).slice(0, 99),
			mode: this.mode || 420,
			uid: this.uid,
			gid: this.gid,
			size: t,
			mtime: this.mtime,
			type: this.global ? `GlobalExtendedHeader` : `ExtendedHeader`,
			linkpath: ``,
			uname: this.uname || ``,
			gname: this.gname || ``,
			devmaj: 0,
			devmin: 0,
			atime: this.atime,
			ctime: this.ctime
		}).encode(r), r.write(e, 512, t, `utf8`);
		for (let e = t + 512; e < r.length; e++) r[e] = 0;
		return r;
	}
	encodeBody() {
		return this.encodeField(`path`) + this.encodeField(`ctime`) + this.encodeField(`atime`) + this.encodeField(`dev`) + this.encodeField(`ino`) + this.encodeField(`nlink`) + this.encodeField(`charset`) + this.encodeField(`comment`) + this.encodeField(`gid`) + this.encodeField(`gname`) + this.encodeField(`linkpath`) + this.encodeField(`mtime`) + this.encodeField(`size`) + this.encodeField(`uid`) + this.encodeField(`uname`);
	}
	encodeField(e) {
		if (this[e] === void 0) return ``;
		let t = this[e], n = t instanceof Date ? t.getTime() / 1e3 : t, r = ` ` + (e === `dev` || e === `ino` || e === `nlink` ? `SCHILY.` : ``) + e + `=` + n + `
`, i = Buffer.byteLength(r), a = Math.floor(Math.log(i) / Math.log(10)) + 1;
		return i + a >= 10 ** a && (a += 1), a + i + r;
	}
	static parse(t, n, r = !1) {
		return new e(gn(_n(t), n), r);
	}
}, gn = (e, t) => t ? Object.assign({}, t, e) : e, _n = (e) => e.replace(/\n$/, ``).split(`
`).reduce(vn, Object.create(null)), vn = (e, t) => {
	let n = parseInt(t, 10);
	if (n !== Buffer.byteLength(t) + 1) return e;
	t = t.slice((n + ` `).length);
	let r = t.split(`=`), i = r.shift();
	if (!i) return e;
	let a = i.replace(/^SCHILY\.(dev|ino|nlink)/, `$1`), o = r.join(`=`);
	return e[a] = /^([A-Z]+\.)?([mac]|birth|creation)time$/.test(a) ? /* @__PURE__ */ new Date(Number(o) * 1e3) : /^[0-9]+$/.test(o) ? +o : o, e;
}, z = (process.env.TESTING_TAR_FAKE_PLATFORM || process.platform) === `win32` ? (e) => e && e.replaceAll(/\\/g, `/`) : (e) => e, yn = class extends Ue {
	extended;
	globalExtended;
	header;
	startBlockSize;
	blockRemain;
	remain;
	type;
	meta = !1;
	ignore = !1;
	path;
	mode;
	uid;
	gid;
	uname;
	gname;
	size = 0;
	mtime;
	atime;
	ctime;
	linkpath;
	dev;
	ino;
	nlink;
	invalid = !1;
	absolute;
	unsupported = !1;
	constructor(e, t, n) {
		switch (super({}), this.pause(), this.extended = t, this.globalExtended = n, this.header = e, this.remain = e.size ?? 0, this.startBlockSize = 512 * Math.ceil(this.remain / 512), this.blockRemain = this.startBlockSize, this.type = e.type, this.type) {
			case `File`:
			case `OldFile`:
			case `Link`:
			case `SymbolicLink`:
			case `CharacterDevice`:
			case `BlockDevice`:
			case `Directory`:
			case `FIFO`:
			case `ContiguousFile`:
			case `GNUDumpDir`: break;
			case `NextFileHasLongLinkpath`:
			case `NextFileHasLongPath`:
			case `OldGnuLongPath`:
			case `GlobalExtendedHeader`:
			case `ExtendedHeader`:
			case `OldExtendedHeader`:
				this.meta = !0;
				break;
			default: this.ignore = !0;
		}
		if (!e.path) throw Error(`no path provided for tar.ReadEntry`);
		this.path = z(e.path), this.mode = e.mode, this.mode && (this.mode &= 4095), this.uid = e.uid, this.gid = e.gid, this.uname = e.uname, this.gname = e.gname, this.size = this.remain, this.mtime = e.mtime, this.atime = e.atime, this.ctime = e.ctime, this.linkpath = e.linkpath ? z(e.linkpath) : void 0, this.uname = e.uname, this.gname = e.gname, t && this.#t(t), n && this.#t(n, !0);
	}
	write(e) {
		let t = e.length;
		if (t > this.blockRemain) throw Error(`writing more to entry than is appropriate`);
		let n = this.remain, r = this.blockRemain;
		return this.remain = Math.max(0, n - t), this.blockRemain = Math.max(0, r - t), this.ignore ? !0 : n >= t ? super.write(e) : super.write(e.subarray(0, n));
	}
	#t(e, t = !1) {
		e.path &&= z(e.path), e.linkpath &&= z(e.linkpath), Object.assign(this, Object.fromEntries(Object.entries(e).filter(([e, n]) => !(n == null || e === `path` && t))));
	}
}, bn = (e, t, n, r = {}) => {
	e.file && (r.file = e.file), e.cwd && (r.cwd = e.cwd), r.code = n instanceof Error && n.code || t, r.tarCode = t, !e.strict && r.recoverable !== !1 ? (n instanceof Error && (r = Object.assign(n, r), n = n.message), e.emit(`warn`, t, n, r)) : n instanceof Error ? e.emit(`error`, Object.assign(n, r)) : e.emit(`error`, Object.assign(Error(`${t}: ${n}`), r));
}, xn = 1024 * 1024, Sn = Buffer.from([31, 139]), Cn = Buffer.from([
	40,
	181,
	47,
	253
]), wn = Math.max(Sn.length, Cn.length), B = Symbol(`state`), Tn = Symbol(`writeEntry`), V = Symbol(`readEntry`), En = Symbol(`nextEntry`), Dn = Symbol(`processEntry`), H = Symbol(`extendedHeader`), On = Symbol(`globalExtendedHeader`), kn = Symbol(`meta`), An = Symbol(`emitMeta`), U = Symbol(`buffer`), W = Symbol(`queue`), G = Symbol(`ended`), jn = Symbol(`emittedEnd`), Mn = Symbol(`emit`), K = Symbol(`unzip`), Nn = Symbol(`consumeChunk`), Pn = Symbol(`consumeChunkSub`), Fn = Symbol(`consumeBody`), In = Symbol(`consumeMeta`), Ln = Symbol(`consumeHeader`), Rn = Symbol(`consuming`), zn = Symbol(`bufferConcat`), Bn = Symbol(`maybeEnd`), Vn = Symbol(`writing`), q = Symbol(`aborted`), Hn = Symbol(`onDone`), Un = Symbol(`sawValidEntry`), Wn = Symbol(`sawNullBlock`), Gn = Symbol(`sawEOF`), Kn = Symbol(`closeStream`), qn = () => !0, Jn = class extends u {
	file;
	strict;
	maxMetaEntrySize;
	filter;
	brotli;
	zstd;
	writable = !0;
	readable = !1;
	[W] = [];
	[U];
	[V];
	[Tn];
	[B] = `begin`;
	[kn] = ``;
	[H];
	[On];
	[G] = !1;
	[K];
	[q] = !1;
	[Un];
	[Wn] = !1;
	[Gn] = !1;
	[Vn] = !1;
	[Rn] = !1;
	[jn] = !1;
	constructor(e = {}) {
		super(), this.file = e.file || ``, this.on(Hn, () => {
			(this[B] === `begin` || this[Un] === !1) && this.warn(`TAR_BAD_ARCHIVE`, `Unrecognized archive format`);
		}), e.ondone ? this.on(Hn, e.ondone) : this.on(Hn, () => {
			this.emit(`prefinish`), this.emit(`finish`), this.emit(`end`);
		}), this.strict = !!e.strict, this.maxMetaEntrySize = e.maxMetaEntrySize || xn, this.filter = typeof e.filter == `function` ? e.filter : qn;
		let t = e.file && (e.file.endsWith(`.tar.br`) || e.file.endsWith(`.tbr`));
		this.brotli = !(e.gzip || e.zstd) && e.brotli !== void 0 ? e.brotli : t ? void 0 : !1;
		let n = e.file && (e.file.endsWith(`.tar.zst`) || e.file.endsWith(`.tzst`));
		this.zstd = !(e.gzip || e.brotli) && e.zstd !== void 0 ? e.zstd : n ? !0 : void 0, this.on(`end`, () => this[Kn]()), typeof e.onwarn == `function` && this.on(`warn`, e.onwarn), typeof e.onReadEntry == `function` && this.on(`entry`, e.onReadEntry);
	}
	warn(e, t, n = {}) {
		bn(this, e, t, n);
	}
	[Ln](e, t) {
		this[Un] === void 0 && (this[Un] = !1);
		let n;
		try {
			n = new I(e, t, this[H], this[On]);
		} catch (e) {
			return this.warn(`TAR_ENTRY_INVALID`, e);
		}
		if (n.nullBlock) this[Wn] ? (this[Gn] = !0, this[B] === `begin` && (this[B] = `header`), this[Mn](`eof`)) : (this[Wn] = !0, this[Mn](`nullBlock`));
		else if (this[Wn] = !1, !n.cksumValid) this.warn(`TAR_ENTRY_INVALID`, `checksum failure`, { header: n });
		else if (!n.path) this.warn(`TAR_ENTRY_INVALID`, `path is required`, { header: n });
		else {
			let e = n.type;
			if (/^(Symbolic)?Link$/.test(e) && !n.linkpath) this.warn(`TAR_ENTRY_INVALID`, `linkpath required`, { header: n });
			else if (!/^(Symbolic)?Link$/.test(e) && !/^(Global)?ExtendedHeader$/.test(e) && n.linkpath) this.warn(`TAR_ENTRY_INVALID`, `linkpath forbidden`, { header: n });
			else {
				let e = this[Tn] = new yn(n, this[H], this[On]);
				this[Un] || (e.remain ? e.on(`end`, () => {
					e.invalid || (this[Un] = !0);
				}) : this[Un] = !0), e.meta ? e.size > this.maxMetaEntrySize ? (e.ignore = !0, this[Mn](`ignoredEntry`, e), this[B] = `ignore`, e.resume()) : e.size > 0 && (this[kn] = ``, e.on(`data`, (e) => this[kn] += e), this[B] = `meta`) : (this[H] = void 0, e.ignore = e.ignore || !this.filter(e.path, e), e.ignore ? (this[Mn](`ignoredEntry`, e), this[B] = e.remain ? `ignore` : `header`, e.resume()) : (e.remain ? this[B] = `body` : (this[B] = `header`, e.end()), this[V] ? this[W].push(e) : (this[W].push(e), this[En]())));
			}
		}
	}
	[Kn]() {
		queueMicrotask(() => this.emit(`close`));
	}
	[Dn](e) {
		let t = !0;
		if (!e) this[V] = void 0, t = !1;
		else if (Array.isArray(e)) {
			let [t, ...n] = e;
			this.emit(t, ...n);
		} else this[V] = e, this.emit(`entry`, e), e.emittedEnd || (e.on(`end`, () => this[En]()), t = !1);
		return t;
	}
	[En]() {
		do		;
while (this[Dn](this[W].shift()));
		if (this[W].length === 0) {
			let e = this[V];
			!e || e.flowing || e.size === e.remain ? this[Vn] || this.emit(`drain`) : e.once(`drain`, () => this.emit(`drain`));
		}
	}
	[Fn](e, t) {
		let n = this[Tn];
		if (!n) throw Error(`attempt to consume body without entry??`);
		let r = n.blockRemain ?? 0, i = r >= e.length && t === 0 ? e : e.subarray(t, t + r);
		return n.write(i), n.blockRemain || (this[B] = `header`, this[Tn] = void 0, n.end()), i.length;
	}
	[In](e, t) {
		let n = this[Tn], r = this[Fn](e, t);
		return !this[Tn] && n && this[An](n), r;
	}
	[Mn](e, t, n) {
		this[W].length === 0 && !this[V] ? this.emit(e, t, n) : this[W].push([
			e,
			t,
			n
		]);
	}
	[An](e) {
		switch (this[Mn](`meta`, this[kn]), e.type) {
			case `ExtendedHeader`:
			case `OldExtendedHeader`:
				this[H] = hn.parse(this[kn], this[H], !1);
				break;
			case `GlobalExtendedHeader`:
				this[On] = hn.parse(this[kn], this[On], !0);
				break;
			case `NextFileHasLongPath`:
			case `OldGnuLongPath`: {
				let e = this[H] ?? Object.create(null);
				this[H] = e, e.path = this[kn].replace(/\0.*/, ``);
				break;
			}
			case `NextFileHasLongLinkpath`: {
				let e = this[H] || Object.create(null);
				this[H] = e, e.linkpath = this[kn].replace(/\0.*/, ``);
				break;
			}
			default: throw Error(`unknown meta: ` + e.type);
		}
	}
	abort(e) {
		this[q] = !0, this.emit(`abort`, e), this.warn(`TAR_ABORT`, e, { recoverable: !1 });
	}
	write(e, t, n) {
		if (typeof t == `function` && (n = t, t = void 0), typeof e == `string` && (e = Buffer.from(e, typeof t == `string` ? t : `utf8`)), this[q]) return n?.(), !1;
		if ((this[K] === void 0 || this.brotli === void 0 && this[K] === !1) && e) {
			if (this[U] && (e = Buffer.concat([this[U], e]), this[U] = void 0), e.length < wn) return this[U] = e, n?.(), !0;
			for (let t = 0; this[K] === void 0 && t < Sn.length; t++) e[t] !== Sn[t] && (this[K] = !1);
			let t = !1;
			if (this[K] === !1 && this.zstd !== !1) {
				t = !0;
				for (let n = 0; n < Cn.length; n++) if (e[n] !== Cn[n]) {
					t = !1;
					break;
				}
			}
			let r = this.brotli === void 0 && !t;
			if (this[K] === !1 && r) if (e.length < 512) if (this[G]) this.brotli = !0;
			else return this[U] = e, n?.(), !0;
			else try {
				new I(e.subarray(0, 512)), this.brotli = !1;
			} catch {
				this.brotli = !0;
			}
			if (this[K] === void 0 || this[K] === !1 && (this.brotli || t)) {
				let r = this[G];
				this[G] = !1, this[K] = this[K] === void 0 ? new Ft({}) : t ? new Vt({}) : new Rt({}), this[K].on(`data`, (e) => this[Nn](e)), this[K].on(`error`, (e) => this.abort(e)), this[K].on(`end`, () => {
					this[G] = !0, this[Nn]();
				}), this[Vn] = !0;
				let i = !!this[K][r ? `end` : `write`](e);
				return this[Vn] = !1, n?.(), i;
			}
		}
		this[Vn] = !0, this[K] ? this[K].write(e) : this[Nn](e), this[Vn] = !1;
		let r = this[W].length > 0 ? !1 : this[V] ? this[V].flowing : !0;
		return !r && this[W].length === 0 && this[V]?.once(`drain`, () => this.emit(`drain`)), n?.(), r;
	}
	[zn](e) {
		e && !this[q] && (this[U] = this[U] ? Buffer.concat([this[U], e]) : e);
	}
	[Bn]() {
		if (this[G] && !this[jn] && !this[q] && !this[Rn]) {
			this[jn] = !0;
			let e = this[Tn];
			if (e && e.blockRemain) {
				let t = this[U] ? this[U].length : 0;
				this.warn(`TAR_BAD_ARCHIVE`, `Truncated input (needed ${e.blockRemain} more bytes, only ${t} available)`, { entry: e }), this[U] && e.write(this[U]), e.end();
			}
			this[Mn](Hn);
		}
	}
	[Nn](e) {
		if (this[Rn] && e) this[zn](e);
		else if (!e && !this[U]) this[Bn]();
		else if (e) {
			if (this[Rn] = !0, this[U]) {
				this[zn](e);
				let t = this[U];
				this[U] = void 0, this[Pn](t);
			} else this[Pn](e);
			for (; this[U] && this[U]?.length >= 512 && !this[q] && !this[Gn];) {
				let e = this[U];
				this[U] = void 0, this[Pn](e);
			}
			this[Rn] = !1;
		}
		(!this[U] || this[G]) && this[Bn]();
	}
	[Pn](e) {
		let t = 0, n = e.length;
		for (; t + 512 <= n && !this[q] && !this[Gn];) switch (this[B]) {
			case `begin`:
			case `header`:
				this[Ln](e, t), t += 512;
				break;
			case `ignore`:
			case `body`:
				t += this[Fn](e, t);
				break;
			case `meta`:
				t += this[In](e, t);
				break;
			default: throw Error(`invalid state: ` + this[B]);
		}
		t < n && (this[U] = this[U] ? Buffer.concat([e.subarray(t), this[U]]) : e.subarray(t));
	}
	end(e, t, n) {
		return typeof e == `function` && (n = e, t = void 0, e = void 0), typeof t == `function` && (n = t, t = void 0), typeof e == `string` && (e = Buffer.from(e, t)), n && this.once(`finish`, n), this[q] || (this[K] ? (e && this[K].write(e), this[K].end()) : (this[G] = !0, (this.brotli === void 0 || this.zstd === void 0) && (e ||= Buffer.alloc(0)), e && this.write(e), this[Bn]())), this;
	}
}, Yn = (e) => {
	let t = e.length - 1, n = -1;
	for (; t > -1 && e.charAt(t) === `/`;) n = t, t--;
	return n === -1 ? e : e.slice(0, n);
}, Xn = (e) => {
	let t = e.onReadEntry;
	e.onReadEntry = t ? (e) => {
		t(e), e.resume();
	} : (e) => e.resume();
}, Zn = (e, t) => {
	let n = new Map(t.map((e) => [Yn(e), !0])), r = e.filter, i = (e, t = ``) => {
		let r = t || te(e).root || `.`, a;
		if (e === r) a = !1;
		else {
			let t = n.get(e);
			a = t === void 0 ? i(m(e), r) : t;
		}
		return n.set(e, a), a;
	};
	e.filter = r ? (e, t) => r(e, t) && i(Yn(e)) : (e) => i(Yn(e));
}, Qn = Ct((e) => {
	let n = new Jn(e), r = e.file, i;
	try {
		i = t.openSync(r, `r`);
		let a = t.fstatSync(i), o = e.maxReadSize || 16 * 1024 * 1024;
		if (a.size < o) {
			let e = Buffer.allocUnsafe(a.size), r = t.readSync(i, e, 0, a.size, 0);
			n.end(r === e.byteLength ? e : e.subarray(0, r));
		} else {
			let e = 0, r = Buffer.allocUnsafe(o);
			for (; e < a.size;) {
				let a = t.readSync(i, r, 0, o, e);
				if (a === 0) break;
				e += a, n.write(r.subarray(0, a));
			}
			n.end();
		}
	} finally {
		if (typeof i == `number`) try {
			t.closeSync(i);
		} catch {}
	}
}, (e, n) => {
	let r = new Jn(e), i = e.maxReadSize || 16 * 1024 * 1024, a = e.file;
	return new Promise((e, n) => {
		r.on(`error`, n), r.on(`end`, e), t.stat(a, (e, t) => {
			if (e) n(e);
			else {
				let e = new dt(a, {
					readSize: i,
					size: t.size
				});
				e.on(`error`, n), e.pipe(r);
			}
		});
	});
}, (e) => new Jn(e), (e) => new Jn(e), (e, t) => {
	t?.length && Zn(e, t), e.noResume || Xn(e);
}), $n = (e, t, n) => (e &= 4095, n && (e = (e | 384) & -19), t && (e & 256 && (e |= 64), e & 32 && (e |= 8), e & 4 && (e |= 1)), e), { isAbsolute: er, parse: tr } = c, nr = (e) => {
	let t = ``, n = tr(e);
	for (; er(e) || n.root;) {
		let r = e.charAt(0) === `/` && e.slice(0, 4) !== `//?/` ? `/` : n.root;
		e = e.slice(r.length), t += r, n = tr(e);
	}
	return [t, e];
}, rr = [
	`|`,
	`<`,
	`>`,
	`?`,
	`:`
], ir = rr.map((e) => String.fromCodePoint(61440 + Number(e.codePointAt(0)))), ar = new Map(rr.map((e, t) => [e, ir[t]])), or = new Map(ir.map((e, t) => [e, rr[t]])), sr = (e) => rr.reduce((e, t) => e.split(t).join(ar.get(t)), e), cr = (e) => ir.reduce((e, t) => e.split(t).join(or.get(t)), e), lr = (e, t) => t ? (e = z(e).replace(/^\.(\/|$)/, ``), Yn(t) + `/` + e) : z(e), ur = 16 * 1024 * 1024, dr = Symbol(`process`), fr = Symbol(`file`), pr = Symbol(`directory`), mr = Symbol(`symlink`), hr = Symbol(`hardlink`), gr = Symbol(`header`), _r = Symbol(`read`), vr = Symbol(`lstat`), yr = Symbol(`onlstat`), br = Symbol(`onread`), xr = Symbol(`onreadlink`), Sr = Symbol(`openfile`), Cr = Symbol(`onopenfile`), J = Symbol(`close`), wr = Symbol(`mode`), Tr = Symbol(`awaitDrain`), Er = Symbol(`ondrain`), Y = Symbol(`prefix`), Dr = class extends Ue {
	path;
	portable;
	myuid = process.getuid && process.getuid() || 0;
	myuser = process.env.USER || ``;
	maxReadSize;
	linkCache;
	statCache;
	preservePaths;
	cwd;
	strict;
	mtime;
	noPax;
	noMtime;
	prefix;
	fd;
	blockLen = 0;
	blockRemain = 0;
	buf;
	pos = 0;
	remain = 0;
	length = 0;
	offset = 0;
	win32;
	absolute;
	header;
	type;
	linkpath;
	stat;
	onWriteEntry;
	#t = !1;
	constructor(e, t = {}) {
		let n = St(t);
		super(), this.path = z(e), this.portable = !!n.portable, this.maxReadSize = n.maxReadSize || ur, this.linkCache = n.linkCache || /* @__PURE__ */ new Map(), this.statCache = n.statCache || /* @__PURE__ */ new Map(), this.preservePaths = !!n.preservePaths, this.cwd = z(n.cwd || process.cwd()), this.strict = !!n.strict, this.noPax = !!n.noPax, this.noMtime = !!n.noMtime, this.mtime = n.mtime, this.prefix = n.prefix ? z(n.prefix) : void 0, this.onWriteEntry = n.onWriteEntry, typeof n.onwarn == `function` && this.on(`warn`, n.onwarn);
		let r = !1;
		if (!this.preservePaths) {
			let [e, t] = nr(this.path);
			e && typeof t == `string` && (this.path = t, r = e);
		}
		this.win32 = !!n.win32 || process.platform === `win32`, this.win32 && (this.path = cr(this.path.replaceAll(/\\/g, `/`)), e = e.replaceAll(/\\/g, `/`)), this.absolute = z(n.absolute || p.resolve(this.cwd, e)), this.path === `` && (this.path = `./`), r && this.warn(`TAR_ENTRY_INFO`, `stripping ${r} from absolute path`, {
			entry: this,
			path: r + this.path
		});
		let i = this.statCache.get(this.absolute);
		i ? this[yr](i) : this[vr]();
	}
	warn(e, t, n = {}) {
		return bn(this, e, t, n);
	}
	emit(e, ...t) {
		return e === `error` && (this.#t = !0), super.emit(e, ...t);
	}
	[vr]() {
		d.lstat(this.absolute, (e, t) => {
			if (e) return this.emit(`error`, e);
			this[yr](t);
		});
	}
	[yr](e) {
		this.statCache.set(this.absolute, e), this.stat = e, e.isFile() || (e.size = 0), this.type = Ar(e), this.emit(`stat`, e), this[dr]();
	}
	[dr]() {
		switch (this.type) {
			case `File`: return this[fr]();
			case `Directory`: return this[pr]();
			case `SymbolicLink`: return this[mr]();
			default: return this.end();
		}
	}
	[wr](e) {
		return $n(e, this.type === `Directory`, this.portable);
	}
	[Y](e) {
		return lr(e, this.prefix);
	}
	[gr]() {
		if (!this.stat) throw Error(`cannot write header before stat`);
		this.type === `Directory` && this.portable && (this.noMtime = !0), this.onWriteEntry?.(this), this.header = new I({
			path: this[Y](this.path),
			linkpath: this.type === `Link` && this.linkpath !== void 0 ? this[Y](this.linkpath) : this.linkpath,
			mode: this[wr](this.stat.mode),
			uid: this.portable ? void 0 : this.stat.uid,
			gid: this.portable ? void 0 : this.stat.gid,
			size: this.stat.size,
			mtime: this.noMtime ? void 0 : this.mtime || this.stat.mtime,
			type: this.type === `Unsupported` ? void 0 : this.type,
			uname: this.portable ? void 0 : this.stat.uid === this.myuid ? this.myuser : ``,
			atime: this.portable ? void 0 : this.stat.atime,
			ctime: this.portable ? void 0 : this.stat.ctime
		}), this.header.encode() && !this.noPax && super.write(new hn({
			atime: this.portable ? void 0 : this.header.atime,
			ctime: this.portable ? void 0 : this.header.ctime,
			gid: this.portable ? void 0 : this.header.gid,
			mtime: this.noMtime ? void 0 : this.mtime || this.header.mtime,
			path: this[Y](this.path),
			linkpath: this.type === `Link` && this.linkpath !== void 0 ? this[Y](this.linkpath) : this.linkpath,
			size: this.header.size,
			uid: this.portable ? void 0 : this.header.uid,
			uname: this.portable ? void 0 : this.header.uname,
			dev: this.portable ? void 0 : this.stat.dev,
			ino: this.portable ? void 0 : this.stat.ino,
			nlink: this.portable ? void 0 : this.stat.nlink
		}).encode());
		let e = this.header?.block;
		if (!e) throw Error(`failed to encode header`);
		super.write(e);
	}
	[pr]() {
		if (!this.stat) throw Error(`cannot create directory entry without stat`);
		this.path.slice(-1) !== `/` && (this.path += `/`), this.stat.size = 0, this[gr](), this.end();
	}
	[mr]() {
		d.readlink(this.absolute, (e, t) => {
			if (e) return this.emit(`error`, e);
			this[xr](t);
		});
	}
	[xr](e) {
		this.linkpath = z(e), this[gr](), this.end();
	}
	[hr](e) {
		if (!this.stat) throw Error(`cannot create link entry without stat`);
		this.type = `Link`, this.linkpath = z(p.relative(this.cwd, e)), this.stat.size = 0, this[gr](), this.end();
	}
	[fr]() {
		if (!this.stat) throw Error(`cannot create file entry without stat`);
		if (this.stat.nlink > 1) {
			let e = `${this.stat.dev}:${this.stat.ino}`, t = this.linkCache.get(e);
			if (t?.indexOf(this.cwd) === 0) return this[hr](t);
			this.linkCache.set(e, this.absolute);
		}
		if (this[gr](), this.stat.size === 0) return this.end();
		this[Sr]();
	}
	[Sr]() {
		d.open(this.absolute, `r`, (e, t) => {
			if (e) return this.emit(`error`, e);
			this[Cr](t);
		});
	}
	[Cr](e) {
		if (this.fd = e, this.#t) return this[J]();
		if (!this.stat) throw Error(`should stat before calling onopenfile`);
		this.blockLen = 512 * Math.ceil(this.stat.size / 512), this.blockRemain = this.blockLen;
		let t = Math.min(this.blockLen, this.maxReadSize);
		this.buf = Buffer.allocUnsafe(t), this.offset = 0, this.pos = 0, this.remain = this.stat.size, this.length = this.buf.length, this[_r]();
	}
	[_r]() {
		let { fd: e, buf: t, offset: n, length: r, pos: i } = this;
		if (e === void 0 || t === void 0) throw Error(`cannot read file without first opening`);
		d.read(e, t, n, r, i, (e, t) => {
			if (e) return this[J](() => this.emit(`error`, e));
			this[br](t);
		});
	}
	[J](e = () => {}) {
		this.fd !== void 0 && d.close(this.fd, e);
	}
	[br](e) {
		if (e <= 0 && this.remain > 0) {
			let e = Object.assign(Error(`encountered unexpected EOF`), {
				path: this.absolute,
				syscall: `read`,
				code: `EOF`
			});
			return this[J](() => this.emit(`error`, e));
		}
		if (e > this.remain) {
			let e = Object.assign(Error(`did not encounter expected EOF`), {
				path: this.absolute,
				syscall: `read`,
				code: `EOF`
			});
			return this[J](() => this.emit(`error`, e));
		}
		if (!this.buf) throw Error(`should have created buffer prior to reading`);
		if (e === this.remain) for (let t = e; t < this.length && e < this.blockRemain; t++) this.buf[t + this.offset] = 0, e++, this.remain++;
		let t = this.offset === 0 && e === this.buf.length ? this.buf : this.buf.subarray(this.offset, this.offset + e);
		this.write(t) ? this[Er]() : this[Tr](() => this[Er]());
	}
	[Tr](e) {
		this.once(`drain`, e);
	}
	write(e, t, n) {
		if (typeof t == `function` && (n = t, t = void 0), typeof e == `string` && (e = Buffer.from(e, typeof t == `string` ? t : `utf8`)), this.blockRemain < e.length) {
			let e = Object.assign(Error(`writing more data than expected`), { path: this.absolute });
			return this.emit(`error`, e);
		}
		return this.remain -= e.length, this.blockRemain -= e.length, this.pos += e.length, this.offset += e.length, super.write(e, null, n);
	}
	[Er]() {
		if (!this.remain) return this.blockRemain && super.write(Buffer.alloc(this.blockRemain)), this[J]((e) => e ? this.emit(`error`, e) : this.end());
		if (!this.buf) throw Error(`buffer lost somehow in ONDRAIN`);
		this.offset >= this.length && (this.buf = Buffer.allocUnsafe(Math.min(this.blockRemain, this.buf.length)), this.offset = 0), this.length = this.buf.length - this.offset, this[_r]();
	}
}, Or = class extends Dr {
	sync = !0;
	[vr]() {
		this[yr](d.lstatSync(this.absolute));
	}
	[mr]() {
		this[xr](d.readlinkSync(this.absolute));
	}
	[Sr]() {
		this[Cr](d.openSync(this.absolute, `r`));
	}
	[_r]() {
		let e = !0;
		try {
			let { fd: t, buf: n, offset: r, length: i, pos: a } = this;
			if (t === void 0 || n === void 0) throw Error(`fd and buf must be set in READ method`);
			let o = d.readSync(t, n, r, i, a);
			this[br](o), e = !1;
		} finally {
			if (e) try {
				this[J](() => {});
			} catch {}
		}
	}
	[Tr](e) {
		e();
	}
	[J](e = () => {}) {
		this.fd !== void 0 && d.closeSync(this.fd), e();
	}
}, kr = class extends Ue {
	blockLen = 0;
	blockRemain = 0;
	buf = 0;
	pos = 0;
	remain = 0;
	length = 0;
	preservePaths;
	portable;
	strict;
	noPax;
	noMtime;
	readEntry;
	type;
	prefix;
	path;
	mode;
	uid;
	gid;
	uname;
	gname;
	header;
	mtime;
	atime;
	ctime;
	linkpath;
	size;
	onWriteEntry;
	warn(e, t, n = {}) {
		return bn(this, e, t, n);
	}
	constructor(e, t = {}) {
		let n = St(t);
		super(), this.preservePaths = !!n.preservePaths, this.portable = !!n.portable, this.strict = !!n.strict, this.noPax = !!n.noPax, this.noMtime = !!n.noMtime, this.onWriteEntry = n.onWriteEntry, this.readEntry = e;
		let { type: r } = e;
		if (r === `Unsupported`) throw Error(`writing entry that should be ignored`);
		this.type = r, this.type === `Directory` && this.portable && (this.noMtime = !0), this.prefix = n.prefix, this.path = z(e.path), this.mode = e.mode === void 0 ? void 0 : this[wr](e.mode), this.uid = this.portable ? void 0 : e.uid, this.gid = this.portable ? void 0 : e.gid, this.uname = this.portable ? void 0 : e.uname, this.gname = this.portable ? void 0 : e.gname, this.size = e.size, this.mtime = this.noMtime ? void 0 : n.mtime || e.mtime, this.atime = this.portable ? void 0 : e.atime, this.ctime = this.portable ? void 0 : e.ctime, this.linkpath = e.linkpath === void 0 ? void 0 : z(e.linkpath), typeof n.onwarn == `function` && this.on(`warn`, n.onwarn);
		let i = !1;
		if (!this.preservePaths) {
			let [e, t] = nr(this.path);
			e && typeof t == `string` && (this.path = t, i = e);
		}
		this.remain = e.size, this.blockRemain = e.startBlockSize, this.onWriteEntry?.(this), this.header = new I({
			path: this[Y](this.path),
			linkpath: this.type === `Link` && this.linkpath !== void 0 ? this[Y](this.linkpath) : this.linkpath,
			mode: this.mode,
			uid: this.portable ? void 0 : this.uid,
			gid: this.portable ? void 0 : this.gid,
			size: this.size,
			mtime: this.noMtime ? void 0 : this.mtime,
			type: this.type,
			uname: this.portable ? void 0 : this.uname,
			atime: this.portable ? void 0 : this.atime,
			ctime: this.portable ? void 0 : this.ctime
		}), i && this.warn(`TAR_ENTRY_INFO`, `stripping ${i} from absolute path`, {
			entry: this,
			path: i + this.path
		}), this.header.encode() && !this.noPax && super.write(new hn({
			atime: this.portable ? void 0 : this.atime,
			ctime: this.portable ? void 0 : this.ctime,
			gid: this.portable ? void 0 : this.gid,
			mtime: this.noMtime ? void 0 : this.mtime,
			path: this[Y](this.path),
			linkpath: this.type === `Link` && this.linkpath !== void 0 ? this[Y](this.linkpath) : this.linkpath,
			size: this.size,
			uid: this.portable ? void 0 : this.uid,
			uname: this.portable ? void 0 : this.uname,
			dev: this.portable ? void 0 : this.readEntry.dev,
			ino: this.portable ? void 0 : this.readEntry.ino,
			nlink: this.portable ? void 0 : this.readEntry.nlink
		}).encode());
		let a = this.header?.block;
		if (!a) throw Error(`failed to encode header`);
		super.write(a), e.pipe(this);
	}
	[Y](e) {
		return lr(e, this.prefix);
	}
	[wr](e) {
		return $n(e, this.type === `Directory`, this.portable);
	}
	write(e, t, n) {
		typeof t == `function` && (n = t, t = void 0), typeof e == `string` && (e = Buffer.from(e, typeof t == `string` ? t : `utf8`));
		let r = e.length;
		if (r > this.blockRemain) throw Error(`writing more to entry than is appropriate`);
		return this.blockRemain -= r, super.write(e, n);
	}
	end(e, t, n) {
		return this.blockRemain && super.write(Buffer.alloc(this.blockRemain)), typeof e == `function` && (n = e, t = void 0, e = void 0), typeof t == `function` && (n = t, t = void 0), typeof e == `string` && (e = Buffer.from(e, t ?? `utf8`)), n && this.once(`finish`, n), e ? super.end(e, n) : super.end(n), this;
	}
}, Ar = (e) => e.isFile() ? `File` : e.isDirectory() ? `Directory` : e.isSymbolicLink() ? `SymbolicLink` : `Unsupported`, jr = class e {
	tail;
	head;
	length = 0;
	static create(t = []) {
		return new e(t);
	}
	constructor(e = []) {
		for (let t of e) this.push(t);
	}
	*[Symbol.iterator]() {
		for (let e = this.head; e; e = e.next) yield e.value;
	}
	removeNode(e) {
		if (e.list !== this) throw Error(`removing node which does not belong to this list`);
		let t = e.next, n = e.prev;
		return t && (t.prev = n), n && (n.next = t), e === this.head && (this.head = t), e === this.tail && (this.tail = n), this.length--, e.next = void 0, e.prev = void 0, e.list = void 0, t;
	}
	unshiftNode(e) {
		if (e === this.head) return;
		e.list && e.list.removeNode(e);
		let t = this.head;
		e.list = this, e.next = t, t && (t.prev = e), this.head = e, this.tail ||= e, this.length++;
	}
	pushNode(e) {
		if (e === this.tail) return;
		e.list && e.list.removeNode(e);
		let t = this.tail;
		e.list = this, e.prev = t, t && (t.next = e), this.tail = e, this.head ||= e, this.length++;
	}
	push(...e) {
		for (let t = 0, n = e.length; t < n; t++) Nr(this, e[t]);
		return this.length;
	}
	unshift(...e) {
		for (var t = 0, n = e.length; t < n; t++) Pr(this, e[t]);
		return this.length;
	}
	pop() {
		if (!this.tail) return;
		let e = this.tail.value, t = this.tail;
		return this.tail = this.tail.prev, this.tail ? this.tail.next = void 0 : this.head = void 0, t.list = void 0, this.length--, e;
	}
	shift() {
		if (!this.head) return;
		let e = this.head.value, t = this.head;
		return this.head = this.head.next, this.head ? this.head.prev = void 0 : this.tail = void 0, t.list = void 0, this.length--, e;
	}
	forEach(e, t) {
		t ||= this;
		for (let n = this.head, r = 0; n; r++) e.call(t, n.value, r, this), n = n.next;
	}
	forEachReverse(e, t) {
		t ||= this;
		for (let n = this.tail, r = this.length - 1; n; r--) e.call(t, n.value, r, this), n = n.prev;
	}
	get(e) {
		let t = 0, n = this.head;
		for (; n && t < e; t++) n = n.next;
		if (t === e && n) return n.value;
	}
	getReverse(e) {
		let t = 0, n = this.tail;
		for (; n && t < e; t++) n = n.prev;
		if (t === e && n) return n.value;
	}
	map(t, n) {
		n ||= this;
		let r = new e();
		for (let e = this.head; e;) r.push(t.call(n, e.value, this)), e = e.next;
		return r;
	}
	mapReverse(t, n) {
		n ||= this;
		var r = new e();
		for (let e = this.tail; e;) r.push(t.call(n, e.value, this)), e = e.prev;
		return r;
	}
	reduce(e, t) {
		let n, r = this.head;
		if (arguments.length > 1) n = t;
		else if (this.head) r = this.head.next, n = this.head.value;
		else throw TypeError(`Reduce of empty list with no initial value`);
		for (var i = 0; r; i++) n = e(n, r.value, i), r = r.next;
		return n;
	}
	reduceReverse(e, t) {
		let n, r = this.tail;
		if (arguments.length > 1) n = t;
		else if (this.tail) r = this.tail.prev, n = this.tail.value;
		else throw TypeError(`Reduce of empty list with no initial value`);
		for (let t = this.length - 1; r; t--) n = e(n, r.value, t), r = r.prev;
		return n;
	}
	toArray() {
		let e = Array(this.length);
		for (let t = 0, n = this.head; n; t++) e[t] = n.value, n = n.next;
		return e;
	}
	toArrayReverse() {
		let e = Array(this.length);
		for (let t = 0, n = this.tail; n; t++) e[t] = n.value, n = n.prev;
		return e;
	}
	slice(t = 0, n = this.length) {
		n < 0 && (n += this.length), t < 0 && (t += this.length);
		let r = new e();
		if (n < t || n < 0) return r;
		t < 0 && (t = 0), n > this.length && (n = this.length);
		let i = this.head, a = 0;
		for (a = 0; i && a < t; a++) i = i.next;
		for (; i && a < n; a++, i = i.next) r.push(i.value);
		return r;
	}
	sliceReverse(t = 0, n = this.length) {
		n < 0 && (n += this.length), t < 0 && (t += this.length);
		let r = new e();
		if (n < t || n < 0) return r;
		t < 0 && (t = 0), n > this.length && (n = this.length);
		let i = this.length, a = this.tail;
		for (; a && i > n; i--) a = a.prev;
		for (; a && i > t; i--, a = a.prev) r.push(a.value);
		return r;
	}
	splice(e, t = 0, ...n) {
		e > this.length && (e = this.length - 1), e < 0 && (e = this.length + e);
		let r = this.head;
		for (let t = 0; r && t < e; t++) r = r.next;
		let i = [];
		for (let e = 0; r && e < t; e++) i.push(r.value), r = this.removeNode(r);
		r ? r !== this.tail && (r = r.prev) : r = this.tail;
		for (let e of n) r = Mr(this, r, e);
		return i;
	}
	reverse() {
		let e = this.head, t = this.tail;
		for (let t = e; t; t = t.prev) {
			let e = t.prev;
			t.prev = t.next, t.next = e;
		}
		return this.head = t, this.tail = e, this;
	}
};
function Mr(e, t, n) {
	let r = new Fr(n, t, t ? t.next : e.head, e);
	return r.next === void 0 && (e.tail = r), r.prev === void 0 && (e.head = r), e.length++, r;
}
function Nr(e, t) {
	e.tail = new Fr(t, e.tail, void 0, e), e.head ||= e.tail, e.length++;
}
function Pr(e, t) {
	e.head = new Fr(t, void 0, e.head, e), e.tail ||= e.head, e.length++;
}
var Fr = class {
	list;
	next;
	prev;
	value;
	constructor(e, t, n, r) {
		this.list = r, this.value = e, t ? (t.next = this, this.prev = t) : this.prev = void 0, n ? (n.prev = this, this.next = n) : this.next = void 0;
	}
}, Ir = class {
	path;
	absolute;
	entry;
	stat;
	readdir;
	pending = !1;
	ignore = !1;
	piped = !1;
	constructor(e, t) {
		this.path = e || `./`, this.absolute = t;
	}
}, Lr = Buffer.alloc(1024), Rr = Symbol(`onStat`), zr = Symbol(`ended`), X = Symbol(`queue`), Br = Symbol(`current`), Vr = Symbol(`process`), Hr = Symbol(`processing`), Ur = Symbol(`processJob`), Z = Symbol(`jobs`), Wr = Symbol(`jobDone`), Gr = Symbol(`addFSEntry`), Kr = Symbol(`addTarEntry`), qr = Symbol(`stat`), Jr = Symbol(`readdir`), Yr = Symbol(`onreaddir`), Xr = Symbol(`pipe`), Zr = Symbol(`entry`), Qr = Symbol(`entryOpt`), $r = Symbol(`writeEntryClass`), ei = Symbol(`write`), ti = Symbol(`ondrain`), ni = class extends Ue {
	sync = !1;
	opt;
	cwd;
	maxReadSize;
	preservePaths;
	strict;
	noPax;
	prefix;
	linkCache;
	statCache;
	file;
	portable;
	zip;
	readdirCache;
	noDirRecurse;
	follow;
	noMtime;
	mtime;
	filter;
	jobs;
	[$r];
	onWriteEntry;
	[X];
	[Z] = 0;
	[Hr] = !1;
	[zr] = !1;
	constructor(e = {}) {
		if (super(), this.opt = e, this.file = e.file || ``, this.cwd = e.cwd || process.cwd(), this.maxReadSize = e.maxReadSize, this.preservePaths = !!e.preservePaths, this.strict = !!e.strict, this.noPax = !!e.noPax, this.prefix = z(e.prefix || ``), this.linkCache = e.linkCache || /* @__PURE__ */ new Map(), this.statCache = e.statCache || /* @__PURE__ */ new Map(), this.readdirCache = e.readdirCache || /* @__PURE__ */ new Map(), this.onWriteEntry = e.onWriteEntry, this[$r] = Dr, typeof e.onwarn == `function` && this.on(`warn`, e.onwarn), this.portable = !!e.portable, e.gzip || e.brotli || e.zstd) {
			if ((e.gzip ? 1 : 0) + (e.brotli ? 1 : 0) + (e.zstd ? 1 : 0) > 1) throw TypeError(`gzip, brotli, zstd are mutually exclusive`);
			if (e.gzip && (typeof e.gzip != `object` && (e.gzip = {}), this.portable && (e.gzip.portable = !0), this.zip = new Pt(e.gzip)), e.brotli && (typeof e.brotli != `object` && (e.brotli = {}), this.zip = new Lt(e.brotli)), e.zstd && (typeof e.zstd != `object` && (e.zstd = {}), this.zip = new Bt(e.zstd)), !this.zip) throw Error(`impossible`);
			let t = this.zip;
			t.on(`data`, (e) => super.write(e)), t.on(`end`, () => super.end()), t.on(`drain`, () => this[ti]()), this.on(`resume`, () => t.resume());
		} else this.on(`drain`, this[ti]);
		this.noDirRecurse = !!e.noDirRecurse, this.follow = !!e.follow, this.noMtime = !!e.noMtime, e.mtime && (this.mtime = e.mtime), this.filter = typeof e.filter == `function` ? e.filter : () => !0, this[X] = new jr(), this[Z] = 0, this.jobs = Number(e.jobs) || 4, this[Hr] = !1, this[zr] = !1;
	}
	[ei](e) {
		return super.write(e);
	}
	add(e) {
		return this.write(e), this;
	}
	end(e, t, n) {
		return typeof e == `function` && (n = e, e = void 0), typeof t == `function` && (n = t, t = void 0), e && this.add(e), this[zr] = !0, this[Vr](), n && n(), this;
	}
	write(e) {
		if (this[zr]) throw Error(`write after end`);
		return e instanceof yn ? this[Kr](e) : this[Gr](e), this.flowing;
	}
	[Kr](e) {
		let t = z(p.resolve(this.cwd, e.path));
		if (!this.filter(e.path, e)) e.resume();
		else {
			let n = new Ir(e.path, t);
			n.entry = new kr(e, this[Qr](n)), n.entry.on(`end`, () => this[Wr](n)), this[Z] += 1, this[X].push(n);
		}
		this[Vr]();
	}
	[Gr](e) {
		let t = z(p.resolve(this.cwd, e));
		this[X].push(new Ir(e, t)), this[Vr]();
	}
	[qr](e) {
		e.pending = !0, this[Z] += 1, d[this.follow ? `stat` : `lstat`](e.absolute, (t, n) => {
			e.pending = !1, --this[Z], t ? this.emit(`error`, t) : this[Rr](e, n);
		});
	}
	[Rr](e, t) {
		this.statCache.set(e.absolute, t), e.stat = t, this.filter(e.path, t) ? t.isFile() && t.nlink > 1 && e === this[Br] && !this.linkCache.get(`${t.dev}:${t.ino}`) && !this.sync && this[Ur](e) : e.ignore = !0, this[Vr]();
	}
	[Jr](e) {
		e.pending = !0, this[Z] += 1, d.readdir(e.absolute, (t, n) => {
			if (e.pending = !1, --this[Z], t) return this.emit(`error`, t);
			this[Yr](e, n);
		});
	}
	[Yr](e, t) {
		this.readdirCache.set(e.absolute, t), e.readdir = t, this[Vr]();
	}
	[Vr]() {
		if (!this[Hr]) {
			this[Hr] = !0;
			for (let e = this[X].head; e && this[Z] < this.jobs; e = e.next) if (this[Ur](e.value), e.value.ignore) {
				let t = e.next;
				this[X].removeNode(e), e.next = t;
			}
			this[Hr] = !1, this[zr] && this[X].length === 0 && this[Z] === 0 && (this.zip ? this.zip.end(Lr) : (super.write(Lr), super.end()));
		}
	}
	get [Br]() {
		return this[X] && this[X].head && this[X].head.value;
	}
	[Wr](e) {
		this[X].shift(), --this[Z], this[Vr]();
	}
	[Ur](e) {
		if (!e.pending) {
			if (e.entry) {
				e === this[Br] && !e.piped && this[Xr](e);
				return;
			}
			if (!e.stat) {
				let t = this.statCache.get(e.absolute);
				t ? this[Rr](e, t) : this[qr](e);
			}
			if (e.stat && !e.ignore) {
				if (!this.noDirRecurse && e.stat.isDirectory() && !e.readdir) {
					let t = this.readdirCache.get(e.absolute);
					if (t ? this[Yr](e, t) : this[Jr](e), !e.readdir) return;
				}
				if (e.entry = this[Zr](e), !e.entry) {
					e.ignore = !0;
					return;
				}
				e === this[Br] && !e.piped && this[Xr](e);
			}
		}
	}
	[Qr](e) {
		return {
			onwarn: (e, t, n) => this.warn(e, t, n),
			noPax: this.noPax,
			cwd: this.cwd,
			absolute: e.absolute,
			preservePaths: this.preservePaths,
			maxReadSize: this.maxReadSize,
			strict: this.strict,
			portable: this.portable,
			linkCache: this.linkCache,
			statCache: this.statCache,
			noMtime: this.noMtime,
			mtime: this.mtime,
			prefix: this.prefix,
			onWriteEntry: this.onWriteEntry
		};
	}
	[Zr](e) {
		this[Z] += 1;
		try {
			return new this[$r](e.path, this[Qr](e)).on(`end`, () => this[Wr](e)).on(`error`, (e) => this.emit(`error`, e));
		} catch (e) {
			this.emit(`error`, e);
		}
	}
	[ti]() {
		this[Br] && this[Br].entry && this[Br].entry.resume();
	}
	[Xr](e) {
		e.piped = !0, e.readdir && e.readdir.forEach((t) => {
			let n = e.path, r = n === `./` ? `` : n.replace(/\/*$/, `/`);
			this[Gr](r + t);
		});
		let t = e.entry, n = this.zip;
		if (!t) throw Error(`cannot pipe without source`);
		n ? t.on(`data`, (e) => {
			n.write(e) || t.pause();
		}) : t.on(`data`, (e) => {
			super.write(e) || t.pause();
		});
	}
	pause() {
		return this.zip && this.zip.pause(), super.pause();
	}
	warn(e, t, n = {}) {
		bn(this, e, t, n);
	}
}, ri = class extends ni {
	sync = !0;
	constructor(e) {
		super(e), this[$r] = Or;
	}
	pause() {}
	resume() {}
	[qr](e) {
		let t = this.follow ? `statSync` : `lstatSync`;
		this[Rr](e, d[t](e.absolute));
	}
	[Jr](e) {
		this[Yr](e, d.readdirSync(e.absolute));
	}
	[Xr](e) {
		let t = e.entry, n = this.zip;
		if (e.readdir && e.readdir.forEach((t) => {
			let n = e.path, r = n === `./` ? `` : n.replace(/\/*$/, `/`);
			this[Gr](r + t);
		}), !t) throw Error(`Cannot pipe without source`);
		n ? t.on(`data`, (e) => {
			n.write(e);
		}) : t.on(`data`, (e) => {
			super[ei](e);
		});
	}
}, ii = (e, t) => {
	let n = new ri(e), r = new mt(e.file, { mode: e.mode || 438 });
	n.pipe(r), oi(n, t);
}, ai = (e, t) => {
	let n = new ni(e), r = new pt(e.file, { mode: e.mode || 438 });
	n.pipe(r);
	let i = new Promise((e, t) => {
		r.on(`error`, t), r.on(`close`, e), n.on(`error`, t);
	});
	return si(n, t).catch((e) => n.emit(`error`, e)), i;
}, oi = (e, t) => {
	t.forEach((t) => {
		t.charAt(0) === `@` ? Qn({
			file: i.resolve(e.cwd, t.slice(1)),
			sync: !0,
			noResume: !0,
			onReadEntry: (t) => e.add(t)
		}) : e.add(t);
	}), e.end();
}, si = async (e, t) => {
	for (let n of t) n.charAt(0) === `@` ? await Qn({
		file: i.resolve(String(e.cwd), n.slice(1)),
		noResume: !0,
		onReadEntry: (t) => {
			e.add(t);
		}
	}) : e.add(n);
	e.end();
}, ci = Ct(ii, ai, (e, t) => {
	let n = new ri(e);
	return oi(n, t), n;
}, (e, t) => {
	let n = new ni(e);
	return si(n, t).catch((e) => n.emit(`error`, e)), n;
}, (e, t) => {
	if (!t?.length) throw TypeError(`no paths specified to add to archive`);
}), li = (process.env.__FAKE_PLATFORM__ || process.platform) === `win32`, { O_CREAT: ui, O_NOFOLLOW: di, O_TRUNC: fi, O_WRONLY: pi } = d.constants, mi = Number(process.env.__FAKE_FS_O_FILENAME__) || d.constants.UV_FS_O_FILEMAP || 0, hi = li && !!mi, gi = 512 * 1024, _i = mi | fi | ui | pi, vi = !li && typeof di == `number` ? di | fi | ui | pi : null, yi = vi === null ? hi ? (e) => e < gi ? _i : `w` : () => `w` : () => vi, bi = (e, n, r) => {
	try {
		return t.lchownSync(e, n, r);
	} catch (e) {
		if (e?.code !== `ENOENT`) throw e;
	}
}, xi = (e, n, r, i) => {
	t.lchown(e, n, r, (e) => {
		i(e && e?.code !== `ENOENT` ? e : null);
	});
}, Si = (e, t, n, r, a) => {
	t.isDirectory() ? Ci(i.resolve(e, t.name), n, r, (o) => {
		if (o) return a(o);
		xi(i.resolve(e, t.name), n, r, a);
	}) : xi(i.resolve(e, t.name), n, r, a);
}, Ci = (e, n, r, i) => {
	t.readdir(e, { withFileTypes: !0 }, (t, a) => {
		if (t) {
			if (t.code === `ENOENT`) return i();
			if (t.code !== `ENOTDIR` && t.code !== `ENOTSUP`) return i(t);
		}
		if (t || !a.length) return xi(e, n, r, i);
		let o = a.length, s = null, c = (t) => {
			if (!s) {
				if (t) return i(s = t);
				if (--o === 0) return xi(e, n, r, i);
			}
		};
		for (let t of a) Si(e, t, n, r, c);
	});
}, wi = (e, t, n, r) => {
	t.isDirectory() && Ti(i.resolve(e, t.name), n, r), bi(i.resolve(e, t.name), n, r);
}, Ti = (e, n, r) => {
	let i;
	try {
		i = t.readdirSync(e, { withFileTypes: !0 });
	} catch (t) {
		let i = t;
		if (i?.code === `ENOENT`) return;
		if (i?.code === `ENOTDIR` || i?.code === `ENOTSUP`) return bi(e, n, r);
		throw i;
	}
	for (let t of i) wi(e, t, n, r);
	return bi(e, n, r);
}, Ei = class extends Error {
	path;
	code;
	syscall = `chdir`;
	constructor(e, t) {
		super(`${t}: Cannot cd into '${e}'`), this.path = e, this.code = t;
	}
	get name() {
		return `CwdError`;
	}
}, Di = class extends Error {
	path;
	symlink;
	syscall = `symlink`;
	code = `TAR_SYMLINK_ERROR`;
	constructor(e, t) {
		super(`TAR_SYMLINK_ERROR: Cannot extract through symbolic link`), this.symlink = e, this.path = t;
	}
	get name() {
		return `SymlinkError`;
	}
}, Oi = (e, n) => {
	t.stat(e, (t, r) => {
		(t || !r.isDirectory()) && (t = new Ei(e, t?.code || `ENOTDIR`)), n(t);
	});
}, ki = (e, r, a) => {
	e = z(e);
	let o = r.umask ?? 18, s = r.mode | 448, c = (s & o) !== 0, l = r.uid, u = r.gid, d = typeof l == `number` && typeof u == `number` && (l !== r.processUid || u !== r.processGid), f = r.preserve, ee = r.unlink, p = z(r.cwd), m = (n, r) => {
		n ? a(n) : r && d ? Ci(r, l, u, (e) => m(e)) : c ? t.chmod(e, s, a) : a();
	};
	if (e === p) return Oi(e, m);
	if (f) return n.mkdir(e, {
		mode: s,
		recursive: !0
	}).then((e) => m(null, e ?? void 0), m);
	Ai(p, z(i.relative(p, e)).split(`/`), s, ee, p, void 0, m);
}, Ai = (e, n, r, a, o, s, c) => {
	if (n.length === 0) return c(null, s);
	let l = n.shift(), u = z(i.resolve(e + `/` + l));
	t.mkdir(u, r, ji(u, n, r, a, o, s, c));
}, ji = (e, n, r, i, a, o, s) => (c) => {
	c ? t.lstat(e, (l, u) => {
		if (l) l.path = l.path && z(l.path), s(l);
		else if (u.isDirectory()) Ai(e, n, r, i, a, o, s);
		else if (i) t.unlink(e, (c) => {
			if (c) return s(c);
			t.mkdir(e, r, ji(e, n, r, i, a, o, s));
		});
		else {
			if (u.isSymbolicLink()) return s(new Di(e, e + `/` + n.join(`/`)));
			s(c);
		}
	}) : (o ||= e, Ai(e, n, r, i, a, o, s));
}, Mi = (e) => {
	let n = !1, r;
	try {
		n = t.statSync(e).isDirectory();
	} catch (e) {
		r = e?.code;
	} finally {
		if (!n) throw new Ei(e, r ?? `ENOTDIR`);
	}
}, Ni = (e, n) => {
	e = z(e);
	let r = n.umask ?? 18, a = n.mode | 448, o = (a & r) !== 0, s = n.uid, c = n.gid, l = typeof s == `number` && typeof c == `number` && (s !== n.processUid || c !== n.processGid), u = n.preserve, d = n.unlink, f = z(n.cwd), ee = (n) => {
		n && l && Ti(n, s, c), o && t.chmodSync(e, a);
	};
	if (e === f) return Mi(f), ee();
	if (u) return ee(t.mkdirSync(e, {
		mode: a,
		recursive: !0
	}) ?? void 0);
	let p = z(i.relative(f, e)).split(`/`), m;
	for (let e = p.shift(), n = f; e && (n += `/` + e); e = p.shift()) {
		n = z(i.resolve(n));
		try {
			t.mkdirSync(n, a), m ||= n;
		} catch {
			let e = t.lstatSync(n);
			if (e.isDirectory()) continue;
			if (d) {
				t.unlinkSync(n), t.mkdirSync(n, a), m ||= n;
				continue;
			} else if (e.isSymbolicLink()) return new Di(n, n + `/` + p.join(`/`));
		}
	}
	return ee(m);
}, Pi = Object.create(null), Fi = 1e4, Ii = /* @__PURE__ */ new Set(), Li = (e) => {
	Ii.has(e) ? Ii.delete(e) : Pi[e] = e.normalize(`NFD`).toLocaleLowerCase(`en`).toLocaleUpperCase(`en`), Ii.add(e);
	let t = Pi[e], n = Ii.size - Fi;
	if (n > Fi / 10) {
		for (let e of Ii) if (Ii.delete(e), delete Pi[e], --n <= 0) break;
	}
	return t;
}, Ri = (process.env.TESTING_TAR_FAKE_PLATFORM || process.platform) === `win32`, zi = (e) => e.split(`/`).slice(0, -1).reduce((e, t) => {
	let n = e.at(-1);
	return n !== void 0 && (t = o(n, t)), e.push(t || `/`), e;
}, []), Bi = class {
	#t = /* @__PURE__ */ new Map();
	#i = /* @__PURE__ */ new Map();
	#s = /* @__PURE__ */ new Set();
	reserve(e, t) {
		e = Ri ? [`win32 parallelization disabled`] : e.map((e) => Yn(o(Li(e))));
		let n = new Set(e.map((e) => zi(e)).reduce((e, t) => e.concat(t)));
		this.#i.set(t, {
			dirs: n,
			paths: e
		});
		for (let n of e) {
			let e = this.#t.get(n);
			e ? e.push(t) : this.#t.set(n, [t]);
		}
		for (let e of n) {
			let n = this.#t.get(e);
			if (!n) this.#t.set(e, [new Set([t])]);
			else {
				let e = n.at(-1);
				e instanceof Set ? e.add(t) : n.push(new Set([t]));
			}
		}
		return this.#r(t);
	}
	#n(e) {
		let t = this.#i.get(e);
		if (!t) throw Error(`function does not have any path reservations`);
		return {
			paths: t.paths.map((e) => this.#t.get(e)),
			dirs: [...t.dirs].map((e) => this.#t.get(e))
		};
	}
	check(e) {
		let { paths: t, dirs: n } = this.#n(e);
		return t.every((t) => t && t[0] === e) && n.every((t) => t && t[0] instanceof Set && t[0].has(e));
	}
	#r(e) {
		return this.#s.has(e) || !this.check(e) ? !1 : (this.#s.add(e), e(() => this.#e(e)), !0);
	}
	#e(e) {
		if (!this.#s.has(e)) return !1;
		let t = this.#i.get(e);
		if (!t) throw Error(`invalid reservation`);
		let { paths: n, dirs: r } = t, i = /* @__PURE__ */ new Set();
		for (let t of n) {
			let n = this.#t.get(t);
			if (!n || n?.[0] !== e) continue;
			let r = n[1];
			if (!r) {
				this.#t.delete(t);
				continue;
			}
			if (n.shift(), typeof r == `function`) i.add(r);
			else for (let e of r) i.add(e);
		}
		for (let t of r) {
			let n = this.#t.get(t), r = n?.[0];
			if (!(!n || !(r instanceof Set))) if (r.size === 1 && n.length === 1) {
				this.#t.delete(t);
				continue;
			} else if (r.size === 1) {
				n.shift();
				let e = n[0];
				typeof e == `function` && i.add(e);
			} else r.delete(e);
		}
		return this.#s.delete(e), i.forEach((e) => this.#r(e)), !0;
	}
}, Vi = () => process.umask(), Hi = Symbol(`onEntry`), Ui = Symbol(`checkFs`), Wi = Symbol(`checkFs2`), Gi = Symbol(`isReusable`), Q = Symbol(`makeFs`), Ki = Symbol(`file`), qi = Symbol(`directory`), Ji = Symbol(`link`), Yi = Symbol(`symlink`), Xi = Symbol(`hardlink`), Zi = Symbol(`ensureNoSymlink`), Qi = Symbol(`unsupported`), $i = Symbol(`checkPath`), ea = Symbol(`stripAbsolutePath`), ta = Symbol(`mkdir`), $ = Symbol(`onError`), na = Symbol(`pending`), ra = Symbol(`pend`), ia = Symbol(`unpend`), aa = Symbol(`ended`), oa = Symbol(`maybeClose`), sa = Symbol(`skip`), ca = Symbol(`doChown`), la = Symbol(`uid`), ua = Symbol(`gid`), da = Symbol(`checkedCwd`), fa = (process.env.TESTING_TAR_FAKE_PLATFORM || process.platform) === `win32`, pa = 1024, ma = (e, n) => {
	if (!fa) return t.unlink(e, n);
	let r = e + `.DELETE.` + se(16).toString(`hex`);
	t.rename(e, r, (e) => {
		if (e) return n(e);
		t.unlink(r, n);
	});
}, ha = (e) => {
	if (!fa) return t.unlinkSync(e);
	let n = e + `.DELETE.` + se(16).toString(`hex`);
	t.renameSync(e, n), t.unlinkSync(n);
}, ga = (e, t, n) => e !== void 0 && e === e >>> 0 ? e : t !== void 0 && t === t >>> 0 ? t : n, _a = class extends Jn {
	[aa] = !1;
	[da] = !1;
	[na] = 0;
	reservations = new Bi();
	transform;
	writable = !0;
	readable = !1;
	uid;
	gid;
	setOwner;
	preserveOwner;
	processGid;
	processUid;
	maxDepth;
	forceChown;
	win32;
	newer;
	keep;
	noMtime;
	preservePaths;
	unlink;
	cwd;
	strip;
	processUmask;
	umask;
	dmode;
	fmode;
	chmod;
	constructor(e = {}) {
		if (e.ondone = () => {
			this[aa] = !0, this[oa]();
		}, super(e), this.transform = e.transform, this.chmod = !!e.chmod, typeof e.uid == `number` || typeof e.gid == `number`) {
			if (typeof e.uid != `number` || typeof e.gid != `number`) throw TypeError(`cannot set owner without number uid and gid`);
			if (e.preserveOwner) throw TypeError(`cannot preserve owner in archive and also set owner explicitly`);
			this.uid = e.uid, this.gid = e.gid, this.setOwner = !0;
		} else this.uid = void 0, this.gid = void 0, this.setOwner = !1;
		this.preserveOwner = e.preserveOwner === void 0 && typeof e.uid != `number` ? !!(process.getuid && process.getuid() === 0) : !!e.preserveOwner, this.processUid = (this.preserveOwner || this.setOwner) && process.getuid ? process.getuid() : void 0, this.processGid = (this.preserveOwner || this.setOwner) && process.getgid ? process.getgid() : void 0, this.maxDepth = typeof e.maxDepth == `number` ? e.maxDepth : pa, this.forceChown = e.forceChown === !0, this.win32 = !!e.win32 || fa, this.newer = !!e.newer, this.keep = !!e.keep, this.noMtime = !!e.noMtime, this.preservePaths = !!e.preservePaths, this.unlink = !!e.unlink, this.cwd = z(i.resolve(e.cwd || process.cwd())), this.strip = Number(e.strip) || 0, this.processUmask = this.chmod ? typeof e.processUmask == `number` ? e.processUmask : Vi() : 0, this.umask = typeof e.umask == `number` ? e.umask : this.processUmask, this.dmode = e.dmode || 511 & ~this.umask, this.fmode = e.fmode || 438 & ~this.umask, this.on(`entry`, (e) => this[Hi](e));
	}
	warn(e, t, n = {}) {
		return (e === `TAR_BAD_ARCHIVE` || e === `TAR_ABORT`) && (n.recoverable = !1), super.warn(e, t, n);
	}
	[oa]() {
		this[aa] && this[na] === 0 && (this.emit(`prefinish`), this.emit(`finish`), this.emit(`end`));
	}
	[ea](e, t) {
		let n = e[t], { type: r } = e;
		if (!n || this.preservePaths) return !0;
		let [a, o] = nr(n), s = o.replaceAll(/\\/g, `/`).split(`/`);
		if (s.includes(`..`) || fa && /^[a-z]:\.\.$/i.test(s[0] ?? ``)) {
			if (t === `path` || r === `Link`) return this.warn(`TAR_ENTRY_ERROR`, `${t} contains '..'`, {
				entry: e,
				[t]: n
			}), !1;
			let a = i.posix.dirname(e.path), o = i.posix.normalize(i.posix.join(a, s.join(`/`)));
			if (o.startsWith(`../`) || o === `..`) return this.warn(`TAR_ENTRY_ERROR`, `${t} escapes extraction directory`, {
				entry: e,
				[t]: n
			}), !1;
		}
		return a && (e[t] = String(o), this.warn(`TAR_ENTRY_INFO`, `stripping ${a} from absolute ${t}`, {
			entry: e,
			[t]: n
		})), !0;
	}
	[$i](e) {
		let t = z(e.path), n = t.split(`/`);
		if (this.strip) {
			if (n.length < this.strip) return !1;
			if (e.type === `Link`) {
				let t = z(String(e.linkpath)).split(`/`);
				if (t.length >= this.strip) e.linkpath = t.slice(this.strip).join(`/`);
				else return !1;
			}
			n.splice(0, this.strip), e.path = n.join(`/`);
		}
		if (isFinite(this.maxDepth) && n.length > this.maxDepth) return this.warn(`TAR_ENTRY_ERROR`, `path excessively deep`, {
			entry: e,
			path: t,
			depth: n.length,
			maxDepth: this.maxDepth
		}), !1;
		if (!this[ea](e, `path`) || !this[ea](e, `linkpath`)) return !1;
		if (e.absolute = i.isAbsolute(e.path) ? z(i.resolve(e.path)) : z(i.resolve(this.cwd, e.path)), !this.preservePaths && typeof e.absolute == `string` && e.absolute.indexOf(this.cwd + `/`) !== 0 && e.absolute !== this.cwd) return this.warn(`TAR_ENTRY_ERROR`, `path escaped extraction target`, {
			entry: e,
			path: z(e.path),
			resolvedPath: e.absolute,
			cwd: this.cwd
		}), !1;
		if (e.absolute === this.cwd && e.type !== `Directory` && e.type !== `GNUDumpDir`) return !1;
		if (this.win32) {
			let { root: t } = i.win32.parse(String(e.absolute));
			e.absolute = t + sr(String(e.absolute).slice(t.length));
			let { root: n } = i.win32.parse(e.path);
			e.path = n + sr(e.path.slice(n.length));
		}
		return !0;
	}
	[Hi](e) {
		if (!this[$i](e)) return e.resume();
		switch (oe.equal(typeof e.absolute, `string`), e.type) {
			case `Directory`:
			case `GNUDumpDir`: e.mode && (e.mode |= 448);
			case `File`:
			case `OldFile`:
			case `ContiguousFile`:
			case `Link`:
			case `SymbolicLink`: return this[Ui](e);
			default: return this[Qi](e);
		}
	}
	[$](e, t) {
		e.name === `CwdError` ? this.emit(`error`, e) : (this.warn(`TAR_ENTRY_ERROR`, e, { entry: t }), this[ia](), t.resume());
	}
	[ta](e, t, n) {
		ki(z(e), {
			uid: this.uid,
			gid: this.gid,
			processUid: this.processUid,
			processGid: this.processGid,
			umask: this.processUmask,
			preserve: this.preservePaths,
			unlink: this.unlink,
			cwd: this.cwd,
			mode: t
		}, n);
	}
	[ca](e) {
		return this.forceChown || this.preserveOwner && (typeof e.uid == `number` && e.uid !== this.processUid || typeof e.gid == `number` && e.gid !== this.processGid) || typeof this.uid == `number` && this.uid !== this.processUid || typeof this.gid == `number` && this.gid !== this.processGid;
	}
	[la](e) {
		return ga(this.uid, e.uid, this.processUid);
	}
	[ua](e) {
		return ga(this.gid, e.gid, this.processGid);
	}
	[Ki](e, n) {
		let r = typeof e.mode == `number` ? e.mode & 4095 : this.fmode, i = new pt(String(e.absolute), {
			flags: yi(e.size),
			mode: r,
			autoClose: !1
		});
		i.on(`error`, (r) => {
			i.fd && t.close(i.fd, () => {}), i.write = () => !0, this[$](r, e), n();
		});
		let a = 1, o = (r) => {
			if (r) {
				i.fd && t.close(i.fd, () => {}), this[$](r, e), n();
				return;
			}
			--a === 0 && i.fd !== void 0 && t.close(i.fd, (t) => {
				t ? this[$](t, e) : this[ia](), n();
			});
		};
		i.on(`finish`, () => {
			let n = String(e.absolute), r = i.fd;
			if (typeof r == `number` && e.mtime && !this.noMtime) {
				a++;
				let i = e.atime || /* @__PURE__ */ new Date(), s = e.mtime;
				t.futimes(r, i, s, (e) => e ? t.utimes(n, i, s, (t) => o(t && e)) : o());
			}
			if (typeof r == `number` && this[ca](e)) {
				a++;
				let i = this[la](e), s = this[ua](e);
				typeof i == `number` && typeof s == `number` && t.fchown(r, i, s, (e) => e ? t.chown(n, i, s, (t) => o(t && e)) : o());
			}
			o();
		});
		let s = this.transform && this.transform(e) || e;
		s !== e && (s.on(`error`, (t) => {
			this[$](t, e), n();
		}), e.pipe(s)), s.pipe(i);
	}
	[qi](e, n) {
		let r = typeof e.mode == `number` ? e.mode & 4095 : this.dmode;
		this[ta](String(e.absolute), r, (r) => {
			if (r) {
				this[$](r, e), n();
				return;
			}
			let i = 1, a = () => {
				--i === 0 && (n(), this[ia](), e.resume());
			};
			e.mtime && !this.noMtime && (i++, t.utimes(String(e.absolute), e.atime || /* @__PURE__ */ new Date(), e.mtime, a)), this[ca](e) && (i++, t.chown(String(e.absolute), Number(this[la](e)), Number(this[ua](e)), a)), a();
		});
	}
	[Qi](e) {
		e.unsupported = !0, this.warn(`TAR_ENTRY_UNSUPPORTED`, `unsupported entry type: ${e.type}`, { entry: e }), e.resume();
	}
	[Yi](e, t) {
		let n = z(i.relative(this.cwd, i.resolve(i.dirname(String(e.absolute)), String(e.linkpath)))).split(`/`);
		this[Zi](e, this.cwd, n, () => this[Ji](e, String(e.linkpath), `symlink`, t), (n) => {
			this[$](n, e), t();
		});
	}
	[Xi](e, t) {
		let n = z(i.resolve(this.cwd, String(e.linkpath))), r = z(String(e.linkpath)).split(`/`);
		this[Zi](e, this.cwd, r, () => this[Ji](e, n, `link`, t), (n) => {
			this[$](n, e), t();
		});
	}
	[Zi](e, n, r, a, o) {
		let s = r.shift();
		if (this.preservePaths || s === void 0) return a();
		let c = i.resolve(n, s);
		t.lstat(c, (t, n) => {
			if (t) return a();
			if (n?.isSymbolicLink()) return o(new Di(c, i.resolve(c, r.join(`/`))));
			this[Zi](e, c, r, a, o);
		});
	}
	[ra]() {
		this[na]++;
	}
	[ia]() {
		this[na]--, this[oa]();
	}
	[sa](e) {
		this[ia](), e.resume();
	}
	[Gi](e, t) {
		return e.type === `File` && !this.unlink && t.isFile() && t.nlink <= 1 && !fa;
	}
	[Ui](e) {
		this[ra]();
		let t = [e.path];
		e.linkpath && t.push(e.linkpath), this.reservations.reserve(t, (t) => this[Wi](e, t));
	}
	[Wi](e, n) {
		let r = (e) => {
			n(e);
		}, a = () => {
			this[ta](this.cwd, this.dmode, (t) => {
				if (t) {
					this[$](t, e), r();
					return;
				}
				this[da] = !0, o();
			});
		}, o = () => {
			if (e.absolute !== this.cwd) {
				let t = z(i.dirname(String(e.absolute)));
				if (t !== this.cwd) return this[ta](t, this.dmode, (t) => {
					if (t) {
						this[$](t, e), r();
						return;
					}
					s();
				});
			}
			s();
		}, s = () => {
			t.lstat(String(e.absolute), (n, i) => {
				if (i && (this.keep || this.newer && i.mtime > (e.mtime ?? i.mtime))) {
					this[sa](e), r();
					return;
				}
				if (n || this[Gi](e, i)) return this[Q](null, e, r);
				if (i.isDirectory()) {
					if (e.type === `Directory`) {
						let n = this.chmod && e.mode && (i.mode & 4095) !== e.mode, a = (t) => this[Q](t ?? null, e, r);
						return n ? t.chmod(String(e.absolute), Number(e.mode), a) : a();
					}
					if (e.absolute !== this.cwd) return t.rmdir(String(e.absolute), (t) => this[Q](t ?? null, e, r));
				}
				if (e.absolute === this.cwd) return this[Q](null, e, r);
				ma(String(e.absolute), (t) => this[Q](t ?? null, e, r));
			});
		};
		this[da] ? o() : a();
	}
	[Q](e, t, n) {
		if (e) {
			this[$](e, t), n();
			return;
		}
		switch (t.type) {
			case `File`:
			case `OldFile`:
			case `ContiguousFile`: return this[Ki](t, n);
			case `Link`: return this[Xi](t, n);
			case `SymbolicLink`: return this[Yi](t, n);
			case `Directory`:
			case `GNUDumpDir`: return this[qi](t, n);
		}
	}
	[Ji](e, n, r, i) {
		t[r](n, String(e.absolute), (t) => {
			t ? this[$](t, e) : (this[ia](), e.resume()), i();
		});
	}
}, va = (e) => {
	try {
		return [null, e()];
	} catch (e) {
		return [e, null];
	}
}, ya = class extends _a {
	sync = !0;
	[Q](e, t) {
		return super[Q](e, t, () => {});
	}
	[Ui](e) {
		if (!this[da]) {
			let t = this[ta](this.cwd, this.dmode);
			if (t) return this[$](t, e);
			this[da] = !0;
		}
		if (e.absolute !== this.cwd) {
			let t = z(i.dirname(String(e.absolute)));
			if (t !== this.cwd) {
				let n = this[ta](t, this.dmode);
				if (n) return this[$](n, e);
			}
		}
		let [n, r] = va(() => t.lstatSync(String(e.absolute)));
		if (r && (this.keep || this.newer && r.mtime > (e.mtime ?? r.mtime))) return this[sa](e);
		if (n || this[Gi](e, r)) return this[Q](null, e);
		if (r.isDirectory()) {
			if (e.type === `Directory`) {
				let [n] = this.chmod && e.mode && (r.mode & 4095) !== e.mode ? va(() => {
					t.chmodSync(String(e.absolute), Number(e.mode));
				}) : [];
				return this[Q](n, e);
			}
			let [n] = va(() => t.rmdirSync(String(e.absolute)));
			this[Q](n, e);
		}
		let [a] = e.absolute === this.cwd ? [] : va(() => ha(String(e.absolute)));
		this[Q](a, e);
	}
	[Ki](e, n) {
		let r = typeof e.mode == `number` ? e.mode & 4095 : this.fmode, i = (r) => {
			let i;
			try {
				t.closeSync(a);
			} catch (e) {
				i = e;
			}
			(r || i) && this[$](r || i, e), n();
		}, a;
		try {
			a = t.openSync(String(e.absolute), yi(e.size), r);
		} catch (e) {
			return i(e);
		}
		let o = this.transform && this.transform(e) || e;
		o !== e && (o.on(`error`, (t) => this[$](t, e)), e.pipe(o)), o.on(`data`, (e) => {
			try {
				t.writeSync(a, e, 0, e.length);
			} catch (e) {
				i(e);
			}
		}), o.on(`end`, () => {
			let n = null;
			if (e.mtime && !this.noMtime) {
				let r = e.atime || /* @__PURE__ */ new Date(), i = e.mtime;
				try {
					t.futimesSync(a, r, i);
				} catch (a) {
					try {
						t.utimesSync(String(e.absolute), r, i);
					} catch {
						n = a;
					}
				}
			}
			if (this[ca](e)) {
				let r = this[la](e), i = this[ua](e);
				try {
					t.fchownSync(a, Number(r), Number(i));
				} catch (a) {
					try {
						t.chownSync(String(e.absolute), Number(r), Number(i));
					} catch {
						n ||= a;
					}
				}
			}
			i(n);
		});
	}
	[qi](e, n) {
		let r = typeof e.mode == `number` ? e.mode & 4095 : this.dmode, i = this[ta](String(e.absolute), r);
		if (i) {
			this[$](i, e), n();
			return;
		}
		if (e.mtime && !this.noMtime) try {
			t.utimesSync(String(e.absolute), e.atime || /* @__PURE__ */ new Date(), e.mtime);
		} catch {}
		if (this[ca](e)) try {
			t.chownSync(String(e.absolute), Number(this[la](e)), Number(this[ua](e)));
		} catch {}
		n(), e.resume();
	}
	[ta](e, t) {
		try {
			return Ni(z(e), {
				uid: this.uid,
				gid: this.gid,
				processUid: this.processUid,
				processGid: this.processGid,
				umask: this.processUmask,
				preserve: this.preservePaths,
				unlink: this.unlink,
				cwd: this.cwd,
				mode: t
			});
		} catch (e) {
			return e;
		}
	}
	[Zi](e, n, r, a, o) {
		if (this.preservePaths || r.length === 0) return a();
		let s = n;
		for (let e of r) {
			s = i.resolve(s, e);
			let [c, l] = va(() => t.lstatSync(s));
			if (c) return a();
			if (l.isSymbolicLink()) return o(new Di(s, i.resolve(n, r.join(`/`))));
		}
		a();
	}
	[Ji](e, n, r, i) {
		let a = `${r}Sync`;
		try {
			t[a](n, String(e.absolute)), i(), e.resume();
		} catch (t) {
			return this[$](t, e);
		}
	}
}, ba = Ct((e) => {
	let n = new ya(e), r = e.file, i = t.statSync(r);
	new ft(r, {
		readSize: e.maxReadSize || 16 * 1024 * 1024,
		size: i.size
	}).pipe(n);
}, (e, n) => {
	let r = new _a(e), i = e.maxReadSize || 16 * 1024 * 1024, a = e.file;
	return new Promise((e, n) => {
		r.on(`error`, n), r.on(`close`, e), t.stat(a, (e, t) => {
			if (e) n(e);
			else {
				let e = new dt(a, {
					readSize: i,
					size: t.size
				});
				e.on(`error`, n), e.pipe(r);
			}
		});
	});
}, (e) => new ya(e), (e) => new _a(e), (e, t) => {
	t?.length && Zn(e, t);
}), xa = (e, n) => {
	let r = new ri(e), i = !0, a, o;
	try {
		try {
			a = t.openSync(e.file, `r+`);
		} catch (n) {
			if (n?.code === `ENOENT`) a = t.openSync(e.file, `w+`);
			else throw n;
		}
		let s = t.fstatSync(a), c = Buffer.alloc(512);
		t: for (o = 0; o < s.size; o += 512) {
			for (let e = 0, n = 0; e < 512; e += n) {
				if (n = t.readSync(a, c, e, c.length - e, o + e), o === 0 && c[0] === 31 && c[1] === 139) throw Error(`cannot append to compressed archives`);
				if (!n) break t;
			}
			let n = new I(c);
			if (!n.cksumValid) break;
			let r = 512 * Math.ceil((n.size || 0) / 512);
			if (o + r + 512 > s.size) break;
			o += r, e.mtimeCache && n.mtime && e.mtimeCache.set(String(n.path), n.mtime);
		}
		i = !1, Sa(e, r, o, a, n);
	} finally {
		if (i) try {
			t.closeSync(a);
		} catch {}
	}
}, Sa = (e, t, n, r, i) => {
	let a = new mt(e.file, {
		fd: r,
		start: n
	});
	t.pipe(a), wa(t, i);
}, Ca = (e, n) => {
	n = Array.from(n);
	let r = new ni(e), i = (n, r, i) => {
		let a = (e, r) => {
			e ? t.close(n, (t) => i(e)) : i(null, r);
		}, o = 0;
		if (r === 0) return a(null, 0);
		let s = 0, c = Buffer.alloc(512), l = (i, u) => {
			if (i || u === void 0) return a(i);
			if (s += u, s < 512 && u) return t.read(n, c, s, c.length - s, o + s, l);
			if (o === 0 && c[0] === 31 && c[1] === 139) return a(Error(`cannot append to compressed archives`));
			if (s < 512) return a(null, o);
			let d = new I(c);
			if (!d.cksumValid) return a(null, o);
			let f = 512 * Math.ceil((d.size ?? 0) / 512);
			if (o + f + 512 > r || (o += f + 512, o >= r)) return a(null, o);
			e.mtimeCache && d.mtime && e.mtimeCache.set(String(d.path), d.mtime), s = 0, t.read(n, c, 0, 512, o, l);
		};
		t.read(n, c, 0, 512, o, l);
	};
	return new Promise((a, o) => {
		r.on(`error`, o);
		let s = `r+`, c = (l, u) => {
			if (l && l.code === `ENOENT` && s === `r+`) return s = `w+`, t.open(e.file, s, c);
			if (l || !u) return o(l);
			t.fstat(u, (s, c) => {
				if (s) return t.close(u, () => o(s));
				i(u, c.size, (t, i) => {
					if (t) return o(t);
					let s = new pt(e.file, {
						fd: u,
						start: i
					});
					r.pipe(s), s.on(`error`, o), s.on(`close`, a), Ta(r, n);
				});
			});
		};
		t.open(e.file, s, c);
	});
}, wa = (e, t) => {
	t.forEach((t) => {
		t.charAt(0) === `@` ? Qn({
			file: i.resolve(e.cwd, t.slice(1)),
			sync: !0,
			noResume: !0,
			onReadEntry: (t) => e.add(t)
		}) : e.add(t);
	}), e.end();
}, Ta = async (e, t) => {
	for (let n of t) n.charAt(0) === `@` ? await Qn({
		file: i.resolve(String(e.cwd), n.slice(1)),
		noResume: !0,
		onReadEntry: (t) => e.add(t)
	}) : e.add(n);
	e.end();
}, Ea = Ct(xa, Ca, () => {
	throw TypeError(`file is required`);
}, () => {
	throw TypeError(`file is required`);
}, (e, t) => {
	if (!bt(e)) throw TypeError(`file is required`);
	if (e.gzip || e.brotli || e.zstd || e.file.endsWith(`.br`) || e.file.endsWith(`.tbr`)) throw TypeError(`cannot append to compressed archives`);
	if (!t?.length) throw TypeError(`no paths specified to add/replace`);
});
Ct(Ea.syncFile, Ea.asyncFile, Ea.syncNoFile, Ea.asyncNoFile, (e, t = []) => {
	Ea.validate?.(e, t), Da(e);
});
var Da = (e) => {
	let t = e.filter;
	e.mtimeCache ||= /* @__PURE__ */ new Map(), e.filter = t ? (n, r) => t(n, r) && !((e.mtimeCache?.get(n) ?? r.mtime ?? 0) > (r.mtime ?? 0)) : (t, n) => !((e.mtimeCache?.get(t) ?? n.mtime ?? 0) > (n.mtime ?? 0));
};
export { ce as t };
