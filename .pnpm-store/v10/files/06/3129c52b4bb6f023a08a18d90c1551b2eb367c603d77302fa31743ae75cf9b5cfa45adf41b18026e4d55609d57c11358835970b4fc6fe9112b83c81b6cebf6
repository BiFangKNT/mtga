const NullProtoObj = /* @__PURE__ */ (() => {
	const e = function() {};
	return e.prototype = Object.create(null), Object.freeze(e.prototype), e;
})();
/**
* Create a new router context.
*/
function createRouter() {
	return {
		root: { key: "" },
		static: new NullProtoObj()
	};
}
function expandGroupDelimiters(path) {
	let i = 0;
	let depth = 0;
	for (; i < path.length; i++) {
		const c = path.charCodeAt(i);
		if (c === 92) {
			i++;
			continue;
		}
		if (c === 40) {
			depth++;
			continue;
		}
		if (c === 41 && depth > 0) {
			depth--;
			continue;
		}
		if (c === 123 && depth === 0) break;
	}
	if (i >= path.length) return;
	let j = i + 1;
	depth = 0;
	for (; j < path.length; j++) {
		const c = path.charCodeAt(j);
		if (c === 92) {
			j++;
			continue;
		}
		if (c === 40) {
			depth++;
			continue;
		}
		if (c === 41 && depth > 0) {
			depth--;
			continue;
		}
		if (c === 125 && depth === 0) break;
	}
	if (j >= path.length) return;
	const mod = path[j + 1];
	const hasMod = mod === "?" || mod === "+" || mod === "*";
	const pre = path.slice(0, i);
	const body = path.slice(i + 1, j);
	const suf = path.slice(j + (hasMod ? 2 : 1));
	if (!hasMod) return [pre + body + suf];
	if (mod === "?") return [pre + body + suf, pre + suf];
	if (body.includes("/")) throw new Error("unsupported group repetition across segments");
	return [`${pre}(?:${body})${mod}${suf}`];
}
const UNNAMED_GROUP_PREFIX = "__rou3_unnamed_";
const _unnamedGroupPrefixLength = 15;
function hasSegmentWildcard(segment) {
	let depth = 0;
	for (let i = 0; i < segment.length; i++) {
		const ch = segment.charCodeAt(i);
		if (ch === 92) {
			i++;
			continue;
		}
		if (ch === 40) {
			depth++;
			continue;
		}
		if (ch === 41 && depth > 0) {
			depth--;
			continue;
		}
		if (ch === 42 && depth === 0) return true;
	}
	return false;
}
function replaceSegmentWildcards(segment, unnamedStart, toGroupKey = toUnnamedGroupKey) {
	let depth = 0;
	let nextIndex = unnamedStart;
	let replaced = "";
	for (let i = 0; i < segment.length; i++) {
		const ch = segment.charCodeAt(i);
		if (ch === 92) {
			replaced += segment[i];
			if (i + 1 < segment.length) replaced += segment[++i];
			continue;
		}
		if (ch === 40) {
			depth++;
			replaced += segment[i];
			continue;
		}
		if (ch === 41 && depth > 0) {
			depth--;
			replaced += segment[i];
			continue;
		}
		if (ch === 42 && depth === 0) {
			replaced += `(?<${toGroupKey(nextIndex++)}>[^/]*)`;
			continue;
		}
		replaced += segment[i];
	}
	return [replaced, nextIndex];
}
function toUnnamedGroupKey(index) {
	return `${UNNAMED_GROUP_PREFIX}${index}`;
}
function normalizeUnnamedGroupKey(key) {
	return key.startsWith("__rou3_unnamed_") ? key.slice(_unnamedGroupPrefixLength) : key;
}
function encodeEscapes(path) {
	return path.replace(/\\:/g, "�A").replace(/\\\(/g, "�B").replace(/\\\)/g, "�C").replace(/\\\{/g, "�D").replace(/\\\}/g, "�E");
}
function decodeEscaped(segment) {
	return segment.replace(/\uFFFD([A-E])/g, (_, c) => c === "A" ? ":" : c === "B" ? "(" : c === "C" ? ")" : c === "D" ? "{" : "}");
}
function expandModifiers(segments) {
	for (let i = 0; i < segments.length; i++) {
		const m = segments[i].match(/^(.*:[\w-]+(?:\([^)]*\))?)([?+*])$/);
		if (!m) continue;
		const pre = segments.slice(0, i);
		const suf = segments.slice(i + 1);
		if (m[2] === "?") return ["/" + pre.concat(m[1]).concat(suf).join("/"), "/" + pre.concat(suf).join("/")];
		const name = m[1].match(/:([\w-]+)/)?.[1] || "_";
		const wc = "/" + [
			...pre,
			`**:${name}`,
			...suf
		].join("/");
		const without = "/" + [...pre, ...suf].join("/");
		return m[2] === "+" ? [wc] : [wc, without];
	}
}
function normalizePath(path) {
	if (!path.includes("/.")) return path;
	const r = [];
	for (const s of path.split("/")) if (s === ".") continue;
	else if (s === ".." && r.length > 1) r.pop();
	else r.push(s);
	return r.join("/") || "/";
}
function splitPath(path) {
	const [_, ...s] = path.split("/");
	return s[s.length - 1] === "" ? s.slice(0, -1) : s;
}
function getMatchParams(segments, paramsMap) {
	const params = new NullProtoObj();
	for (const [index, name] of paramsMap) {
		const segment = index < 0 ? segments.slice(-(index + 1)).join("/") : segments[index];
		if (typeof name === "string") params[name] = segment;
		else {
			const match = segment.match(name);
			if (match) for (const key in match.groups) params[normalizeUnnamedGroupKey(key)] = match.groups[key];
		}
	}
	return params;
}
/**
* Add a route to the router context.
*/
function addRoute(ctx, method = "", path, data) {
	method = method.toUpperCase();
	if (path.charCodeAt(0) !== 47) path = `/${path}`;
	const groupExpanded = expandGroupDelimiters(path);
	if (groupExpanded) {
		for (const expandedPath of groupExpanded) addRoute(ctx, method, expandedPath, data);
		return;
	}
	path = encodeEscapes(path);
	const segments = splitPath(path);
	const expanded = expandModifiers(segments);
	if (expanded) {
		for (const p of expanded) addRoute(ctx, method, p, data);
		return;
	}
	let node = ctx.root;
	let _unnamedParamIndex = 0;
	const paramsMap = [];
	const paramsRegexp = [];
	for (let i = 0; i < segments.length; i++) {
		let segment = segments[i];
		if (segment.startsWith("**")) {
			if (!node.wildcard) node.wildcard = { key: "**" };
			node = node.wildcard;
			paramsMap.push([
				-(i + 1),
				segment.split(":")[1] || "_",
				segment.length === 2
			]);
			break;
		}
		if (segment === "*" || segment.includes(":") || segment.includes("(") || hasSegmentWildcard(segment)) {
			if (!node.param) node.param = { key: "*" };
			node = node.param;
			if (segment === "*") paramsMap.push([
				i,
				String(_unnamedParamIndex++),
				true
			]);
			else if (segment.includes(":", 1) || segment.includes("(") || hasSegmentWildcard(segment) || !/^:[\w-]+$/.test(segment)) {
				const [regexp, nextIndex] = getParamRegexp(segment, _unnamedParamIndex);
				_unnamedParamIndex = nextIndex;
				paramsRegexp[i] = regexp;
				node.hasRegexParam = true;
				paramsMap.push([
					i,
					regexp,
					false
				]);
			} else paramsMap.push([
				i,
				segment.slice(1),
				false
			]);
			continue;
		}
		if (segment === "\\*") segment = segments[i] = "*";
		else if (segment === "\\*\\*") segment = segments[i] = "**";
		segment = segments[i] = decodeEscaped(segment);
		const child = node.static?.[segment];
		if (child) node = child;
		else {
			const staticNode = { key: segment };
			if (!node.static) node.static = new NullProtoObj();
			node.static[segment] = staticNode;
			node = staticNode;
		}
	}
	const hasParams = paramsMap.length > 0;
	if (!node.methods) node.methods = new NullProtoObj();
	node.methods[method] ??= [];
	node.methods[method].push({
		data: data || null,
		paramsRegexp,
		paramsMap: hasParams ? paramsMap : void 0
	});
	if (!hasParams) ctx.static["/" + segments.join("/")] = node;
}
function getParamRegexp(segment, unnamedStart = 0) {
	let _i = unnamedStart;
	let _s = "", _d = 0;
	for (let j = 0; j < segment.length; j++) {
		const c = segment.charCodeAt(j);
		if (c === 40) _d++;
		else if (c === 41 && _d > 0) _d--;
		else if (c === 92 && _d === 0 && j + 1 < segment.length) {
			const n = segment[j + 1];
			if (n !== ":" && n !== "(" && n !== "*" && n !== "\\") {
				_s += "￾" + n;
				j++;
				continue;
			}
		}
		_s += segment[j];
	}
	[_s, _i] = replaceSegmentWildcards(_s, _i);
	const regex = _s.replace(/:([\w-]+)(?:\(([^)]*)\))?/g, (_, id, p) => `(?<${id}>${p || "[^/]+"})`).replace(/\((?![?<])/g, () => `(?<${toUnnamedGroupKey(_i++)}>`).replace(/\./g, "\\.").replace(/\uFFFE(.)/g, (_, c) => /[.*+?^${}()|[\]\\]/.test(c) ? `\\${c}` : c);
	return [new RegExp(`^${regex}$`), _i];
}
/**
* Find a route by path.
*/
function findRoute(ctx, method = "", path, opts) {
	if (opts?.normalize) path = normalizePath(path);
	if (path.charCodeAt(path.length - 1) === 47) path = path.slice(0, -1);
	const staticNode = ctx.static[path];
	if (staticNode && staticNode.methods) {
		const staticMatch = staticNode.methods[method] || staticNode.methods[""];
		if (staticMatch !== void 0) return staticMatch[0];
	}
	const segments = splitPath(path);
	const match = _lookupTree(ctx.root, method, segments, 0)?.[0];
	if (match === void 0) return;
	if (opts?.params === false) return match;
	return {
		data: match.data,
		params: match.paramsMap ? getMatchParams(segments, match.paramsMap) : void 0
	};
}
function _lookupTree(node, method, segments, index) {
	if (index === segments.length) {
		if (node.methods) {
			const match = node.methods[method] || node.methods[""];
			if (match) return match;
		}
		if (node.param && node.param.methods) {
			const match = node.param.methods[method] || node.param.methods[""];
			if (match) {
				const pMap = match[0].paramsMap;
				if (pMap?.[pMap?.length - 1]?.[2]) return match;
			}
		}
		if (node.wildcard && node.wildcard.methods) {
			const match = node.wildcard.methods[method] || node.wildcard.methods[""];
			if (match) {
				const pMap = match[0].paramsMap;
				if (pMap?.[pMap?.length - 1]?.[2]) return match;
			}
		}
		return;
	}
	const segment = segments[index];
	if (node.static) {
		const staticChild = node.static[segment];
		if (staticChild) {
			const match = _lookupTree(staticChild, method, segments, index + 1);
			if (match) return match;
		}
	}
	if (node.param) {
		const match = _lookupTree(node.param, method, segments, index + 1);
		if (match) {
			if (node.param.hasRegexParam) {
				const exactMatch = match.find((m) => m.paramsRegexp[index]?.test(segment)) || match.find((m) => !m.paramsRegexp[index]);
				return exactMatch ? [exactMatch] : void 0;
			}
			return match;
		}
	}
	if (node.wildcard && node.wildcard.methods) return node.wildcard.methods[method] || node.wildcard.methods[""];
}
/**
* Remove a route from the router context.
*/
function removeRoute(ctx, method, path) {
	const groupExpanded = expandGroupDelimiters(path);
	if (groupExpanded) {
		for (const expandedPath of groupExpanded) removeRoute(ctx, method, expandedPath);
		return;
	}
	path = encodeEscapes(path);
	const segments = splitPath(path);
	const modExpanded = expandModifiers(segments);
	if (modExpanded) {
		for (const expandedPath of modExpanded) removeRoute(ctx, method, expandedPath);
		return;
	}
	_remove(ctx.root, method || "", segments, 0);
}
function _remove(node, method, segments, index) {
	if (index === segments.length) {
		if (node.methods && method in node.methods) {
			delete node.methods[method];
			if (Object.keys(node.methods).length === 0) node.methods = void 0;
		}
		return;
	}
	const segment = segments[index];
	if (segment.startsWith("**")) {
		if (node.wildcard) {
			_remove(node.wildcard, method, segments, index + 1);
			if (_isEmptyNode(node.wildcard)) node.wildcard = void 0;
		}
		return;
	}
	if (_isParamSegment(segment)) {
		if (node.param) {
			_remove(node.param, method, segments, index + 1);
			if (_isEmptyNode(node.param)) node.param = void 0;
		}
		return;
	}
	const decodedSegment = decodeEscaped(segment);
	const childNode = node.static?.[decodedSegment];
	if (childNode) {
		_remove(childNode, method, segments, index + 1);
		if (_isEmptyNode(childNode)) {
			delete node.static[decodedSegment];
			if (Object.keys(node.static).length === 0) node.static = void 0;
		}
	}
}
function _isParamSegment(segment) {
	return segment === "*" || segment.includes(":") || segment.includes("(") || hasSegmentWildcard(segment);
}
function _isEmptyNode(node) {
	return node.methods === void 0 && node.static === void 0 && node.param === void 0 && node.wildcard === void 0;
}
/**
* Find all route patterns that match the given path.
*/
function findAllRoutes(ctx, method = "", path, opts) {
	if (opts?.normalize) path = normalizePath(path);
	if (path.charCodeAt(path.length - 1) === 47) path = path.slice(0, -1);
	const segments = splitPath(path);
	const matches = _findAll(ctx.root, method, segments, 0);
	if (opts?.params === false) return matches;
	return matches.map((m) => {
		return {
			data: m.data,
			params: m.paramsMap ? getMatchParams(segments, m.paramsMap) : void 0
		};
	});
}
function _findAll(node, method, segments, index, matches = []) {
	const segment = segments[index];
	if (node.wildcard && node.wildcard.methods) {
		const match = node.wildcard.methods[method] || node.wildcard.methods[""];
		if (match) matches.push(...match);
	}
	if (node.param) {
		_findAll(node.param, method, segments, index + 1, matches);
		if (index === segments.length && node.param.methods) {
			const match = node.param.methods[method] || node.param.methods[""];
			if (match) {
				const pMap = match[0].paramsMap;
				if (pMap?.[pMap?.length - 1]?.[2]) matches.push(...match);
			}
		}
	}
	const staticChild = node.static?.[segment];
	if (staticChild) _findAll(staticChild, method, segments, index + 1, matches);
	if (index === segments.length && node.methods) {
		const match = node.methods[method] || node.methods[""];
		if (match) matches.push(...match);
	}
	return matches;
}
const _P = "￾";
function replaceEscapesOutsideGroups(segment) {
	let r = "", d = 0;
	for (let i = 0; i < segment.length; i++) {
		const c = segment.charCodeAt(i);
		if (c === 40) d++;
		else if (c === 41 && d > 0) d--;
		else if (c === 92 && d === 0 && i + 1 < segment.length) {
			const n = segment[i + 1];
			if (n !== ":" && n !== "(" && n !== "*" && n !== "\\") {
				r += _P + n;
				i++;
				continue;
			}
		}
		r += segment[i];
	}
	return r;
}
function resolveEscapePlaceholders(str) {
	return str.replace(/\uFFFE(.)/g, (_, c) => /[.*+?^${}()|[\]\\]/.test(c) ? `\\${c}` : c);
}
function routeToRegExp(route = "/") {
	const groupExpanded = expandGroupDelimiters(route);
	if (groupExpanded) {
		const sources = groupExpanded.map((expandedRoute) => routeToRegExp(expandedRoute).source.slice(1, -1));
		return new RegExp(`^(?:${sources.join("|")})$`);
	}
	return _routeToRegExp(route);
}
function _routeToRegExp(route) {
	const reSegments = [];
	let idCtr = 0;
	for (const segment of route.split("/")) {
		if (!segment) continue;
		if (segment === "*") reSegments.push(`(?<${toRegExpUnnamedKey(idCtr++)}>[^/]*)`);
		else if (segment.startsWith("**")) reSegments.push(segment === "**" ? "?(?<_>.*)" : `?(?<${segment.slice(3)}>.+)`);
		else if (segment.includes(":") || /(^|[^\\])\(/.test(segment) || hasSegmentWildcard(segment)) {
			const modMatch = segment.match(/^(.*:[\w-]+(?:\([^)]*\))?)([?+*])$/);
			if (modMatch) {
				const [, base, mod] = modMatch;
				const name = base.match(/:([\w-]+)/)?.[1] || `_${idCtr++}`;
				if (mod === "?") {
					const inner = base.replace(/:([\w-]+)(?:\(([^)]*)\))?/g, (_, id, pattern) => `(?<${id}>${pattern || "[^/]+"})`).replace(/\./g, "\\.");
					if (reSegments.length > 0) {
						const prevQ = reSegments.pop();
						reSegments.push(`${prevQ}(?:/${inner})?`);
					} else reSegments.push(`?${inner}?`);
					continue;
				}
				const pattern = base.match(/:(\w+)(?:\(([^)]*)\))?/)?.[2];
				if (reSegments.length > 0) {
					const prevMod = reSegments.pop();
					if (pattern) {
						const repeated = `${pattern}(?:/${pattern})*`;
						reSegments.push(mod === "+" ? `${prevMod}/(?<${name}>${repeated})` : `${prevMod}(?:/(?<${name}>${repeated}))?`);
					} else reSegments.push(mod === "+" ? `${prevMod}/(?<${name}>.+)` : `${prevMod}(?:/(?<${name}>.*))?`);
				} else if (pattern) {
					const repeated = `${pattern}(?:/${pattern})*`;
					reSegments.push(mod === "+" ? `?(?<${name}>${repeated})` : `?(?<${name}>${repeated})?`);
				} else reSegments.push(mod === "+" ? `?(?<${name}>.+)` : `?(?<${name}>.*)`);
				continue;
			}
			let dynamicSegment = replaceEscapesOutsideGroups(segment);
			[dynamicSegment, idCtr] = replaceSegmentWildcards(dynamicSegment, idCtr, toRegExpUnnamedKey);
			reSegments.push(resolveEscapePlaceholders(dynamicSegment.replace(/:([\w-]+)(?:\(([^)]*)\))?/g, (_, id, pattern) => `(?<${id}>${pattern || "[^/]+"})`).replace(/(^|[^\\])\((?![?<])/g, (_, p) => `${p}(?<${toRegExpUnnamedKey(idCtr++)}>`).replace(/\./g, "\\.")));
		} else reSegments.push(segment.replace(/\\(.)/g, "$1").replace(/[.*+?^${}()|[\]]/g, "\\$&"));
	}
	return new RegExp(`^/${reSegments.join("/")}/?$`);
}
function toRegExpUnnamedKey(index) {
	return `_${index}`;
}
export { NullProtoObj, addRoute, createRouter, findAllRoutes, findRoute, removeRoute, routeToRegExp };
