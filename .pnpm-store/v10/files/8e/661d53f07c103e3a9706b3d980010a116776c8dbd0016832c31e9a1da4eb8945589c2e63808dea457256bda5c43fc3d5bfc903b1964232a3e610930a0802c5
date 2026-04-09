import escapeStringRegexp from "escape-string-regexp";
import { encodePath, joinURL, withTrailingSlash, withoutLeadingSlash, withoutTrailingSlash } from "ufo";
//#region src/converters.ts
const collator = new Intl.Collator("en-US");
function flattenTree(tree) {
	const infos = [];
	(function walk(node) {
		const defaults = node.files.filter((f) => f.viewName === "default");
		const views = node.files.filter((f) => f.viewName !== "default");
		const byGroupPath = /* @__PURE__ */ new Map();
		for (const f of defaults.length > 0 ? defaults : node.files) {
			const key = f.groups.join(",");
			let group = byGroupPath.get(key);
			if (!group) {
				group = [];
				byGroupPath.set(key, group);
			}
			group.push(f);
		}
		for (const [groupKey, groupFiles] of byGroupPath) {
			const primary = groupFiles[0];
			const segments = [];
			for (const seg of primary.originalSegments) if (!seg.every((t) => t.type === "group")) segments.push(seg);
			infos.push({
				file: primary.path,
				relativePath: primary.relativePath,
				segments,
				groups: primary.groups,
				siblingFiles: [...groupFiles, ...views.filter((v) => v.groups.join(",") === groupKey)]
			});
		}
		for (const child of node.children.values()) walk(child);
	})(tree.root);
	return infos;
}
/** Deep-clone a VueRoute array. */
function cloneRoutes(routes) {
	return routes.map((r) => cloneRoute(r));
}
function cloneRoute(route) {
	const clone = {
		path: route.path,
		file: route.file,
		children: route.children.length ? cloneRoutes(route.children) : []
	};
	if (route.name !== void 0) clone.name = route.name;
	if (route.modes) clone.modes = [...route.modes];
	if (route.meta) {
		clone.meta = { ...route.meta };
		if (route.meta.groups) clone.meta.groups = [...route.meta.groups];
	}
	if (route.components) clone.components = { ...route.components };
	for (const key of Object.keys(route)) if (!(key in clone)) clone[key] = route[key];
	return clone;
}
function optionsToKey(options) {
	if (!options) return "";
	const parts = [];
	if (options.getRouteName) parts.push("n");
	if (options.onDuplicateRouteName) parts.push("d");
	if (options.attrs) for (const [k, v] of Object.entries(options.attrs)) parts.push(`a:${k}=${v.join(",")}`);
	return parts.join("|");
}
/**
* Convert a route tree to Vue Router 4 route definitions.
*
* Results are cached on the tree and deep-cloned on return, so mutations
* to the returned array do not affect the cache. The cache is automatically
* invalidated when `addFile` / `removeFile` mark the tree as dirty.
*/
function toVueRouter4(tree, options) {
	const key = optionsToKey(options);
	const cached = tree["~cachedVueRouter"];
	if (!tree["~dirty"] && cached && cached.optionsKey === key) return cloneRoutes(cached.routes);
	const fileInfos = flattenTree(tree);
	fileInfos.sort((a, b) => a.relativePath.length - b.relativePath.length || collator.compare(a.relativePath, b.relativePath));
	const routes = [];
	for (const info of fileInfos) {
		const route = {
			name: "",
			path: "",
			file: info.file,
			children: [],
			groups: info.groups,
			siblingFiles: info.siblingFiles
		};
		let parent = routes;
		if (info.segments.length === 0) route.path = "/";
		for (let i = 0; i < info.segments.length; i++) {
			const seg = info.segments[i];
			const isIndex = isIndexSegment(seg);
			const segmentName = isIndex ? "index" : seg.map((t) => t.type === "group" ? "" : t.value).join("");
			route.name += (route.name && "/") + segmentName;
			const nextSeg = i < info.segments.length - 1 ? info.segments[i + 1] : void 0;
			const routePath = `/${toVueRouterSegment(seg, { hasSucceeding: !!nextSeg && !isIndexSegment(nextSeg) })}`;
			const normalizedFullPath = joinURL(route.path || "/", isIndex ? "/" : routePath).replaceAll("([^/]*)*", "(.*)*");
			const match = parent.find((r) => r.name === route.name && r.path === normalizedFullPath);
			if (match?.children) {
				parent = match.children;
				route.path = "";
			} else if (segmentName === "index" && !route.path) route.path += "/";
			else if (segmentName !== "index") route.path += routePath;
		}
		parent.push(route);
	}
	const result = prepareRoutes(routes, void 0, options);
	tree["~cachedVueRouter"] = {
		routes: result,
		optionsKey: key
	};
	tree["~dirty"] = false;
	return cloneRoutes(result);
}
function toRou3(tree) {
	return flattenTree(tree).map((info) => {
		let path = "/";
		for (const segment of info.segments) {
			let part = "";
			for (const token of segment) switch (token.type) {
				case "group": break;
				case "static":
					part += token.value;
					break;
				case "dynamic":
					part += token.value ? `:${token.value}` : "*";
					break;
				case "catchall":
					part += token.value ? `**:${token.value}` : "**";
					break;
				case "optional": throw new TypeError("[unrouting] `toRou3` does not support optional parameters");
				case "repeatable": throw new TypeError("[unrouting] `toRou3` does not support repeatable parameters");
				case "optional-repeatable": throw new TypeError("[unrouting] `toRou3` does not support optional repeatable parameters");
			}
			if (part) path = joinURL(path, part);
		}
		return {
			path,
			file: info.file
		};
	});
}
function toRegExp(tree) {
	return flattenTree(tree).map((info) => {
		const keys = [];
		let source = "^";
		for (const segment of info.segments) {
			let re = "";
			for (const token of segment) {
				const key = sanitizeCaptureGroup(token.value);
				switch (token.type) {
					case "group": break;
					case "static":
						re += escapeStringRegexp(token.value);
						break;
					case "dynamic":
						keys.push(key);
						re += `(?<${key}>[^/]+)`;
						break;
					case "optional":
						keys.push(key);
						re += `(?<${key}>[^/]*)`;
						break;
					case "repeatable":
						keys.push(key);
						re += `(?<${key}>[^/]+(?:/[^/]+)*)`;
						break;
					case "optional-repeatable":
						keys.push(key);
						re += `(?<${key}>[^/]*(?:/[^/]+)*)`;
						break;
					case "catchall":
						keys.push(key);
						re += `(?<${key}>.*)`;
						break;
				}
			}
			const isOptional = segment.every((t) => t.type === "optional" || t.type === "catchall" || t.type === "group" || t.type === "optional-repeatable");
			if (re) source += isOptional ? `(?:\\/${re})?` : `\\/${re}`;
		}
		source += "\\/?$";
		return {
			pattern: new RegExp(source),
			keys,
			file: info.file
		};
	});
}
function compareRoutes(a, b) {
	const aScore = a.scoreSegments;
	const bScore = b.scoreSegments;
	const len = Math.max(aScore.length, bScore.length);
	for (let i = 0; i < len; i++) {
		const sa = aScore[i] ?? -Infinity;
		const sb = bScore[i] ?? -Infinity;
		if (sa !== sb) return sb - sa;
	}
	return collator.compare(a.path, b.path);
}
/**
* Convert a single parsed segment (an array of tokens returned by
* `parseSegment`) into a Vue Router 4 path segment string.
*
* @example
* const tokens = parseSegment('[id]')
* toVueRouterSegment(tokens) // => ':id()'
*/
function toVueRouterSegment(tokens, options) {
	const hasSucceeding = options?.hasSucceeding ?? false;
	let out = "";
	for (const token of tokens) switch (token.type) {
		case "group": continue;
		case "static":
			out += encodePath(token.value).replace(/:/g, "\\:");
			break;
		case "dynamic":
			out += `:${token.value}()`;
			break;
		case "optional":
			out += `:${token.value}?`;
			break;
		case "repeatable":
			out += `:${token.value}+`;
			break;
		case "optional-repeatable":
			out += `:${token.value}*`;
			break;
		case "catchall":
			out += hasSucceeding ? `:${token.value}([^/]*)*` : `:${token.value}(.*)*`;
			break;
	}
	return out;
}
/**
* Convert an array of parsed path segments into a full Vue Router 4 path
* string. Automatically determines `hasSucceeding` for each segment so that
* mid-path catchalls use the restrictive `([^/]*)*` pattern.
*
* @example
* const parsed = parsePath(['users/[id].vue'])[0]
* toVueRouterPath(parsed.segments) // => '/users/:id()'
*/
function toVueRouterPath(segments) {
	let path = "";
	for (let i = 0; i < segments.length; i++) {
		const seg = segments[i];
		if (seg.every((t) => t.type === "group")) continue;
		if (isIndexSegment(seg)) continue;
		const hasSucceeding = !!segments.slice(i + 1).find((s) => !isIndexSegment(s) && !s.every((t) => t.type === "group"));
		path += `/${toVueRouterSegment(seg, { hasSucceeding })}`;
	}
	return path || "/";
}
function isIndexSegment(tokens) {
	return tokens.length === 1 && tokens[0].type === "static" && tokens[0].value === "";
}
const INDEX_RE = /\/index$/;
const SLASH_RE = /\//g;
function defaultGetRouteName(rawName) {
	return rawName.replace(INDEX_RE, "").replace(SLASH_RE, "-") || "index";
}
function prepareRoutes(routes, parent, options, names = /* @__PURE__ */ new Map()) {
	const getRouteName = options?.getRouteName || defaultGetRouteName;
	const attrs = options?.attrs;
	for (const route of routes) route.scoreSegments = computeScoreSegments(route);
	routes.sort(compareRoutes);
	return routes.map((route) => {
		let name = getRouteName(route.name);
		let path = route.path;
		if (parent && path[0] === "/") path = path.slice(1);
		const children = route.children.length ? prepareRoutes(route.children, route, options, names) : [];
		if (children.some((c) => c.path === "")) name = void 0;
		if (name !== void 0) {
			if (options?.onDuplicateRouteName) {
				const existingFile = names.get(name);
				if (existingFile) options.onDuplicateRouteName(name, route.file, existingFile);
			}
			names.set(name, route.file);
		}
		const out = {
			path,
			file: route.file,
			children
		};
		if (name !== void 0) out.name = name;
		if (route.groups.length > 0) out.meta = {
			...out.meta,
			groups: route.groups
		};
		const views = route.siblingFiles.filter((f) => f.viewName !== "default");
		if (views.length > 0) {
			out.components = { default: route.file };
			for (const v of views) out.components[v.viewName] = v.path;
		}
		const allModes = /* @__PURE__ */ new Set();
		for (const f of route.siblingFiles) if (f.modes) for (const m of f.modes) allModes.add(m);
		if (attrs && allModes.size > 0) {
			let modesConsumed = false;
			for (const [attrName, attrValues] of Object.entries(attrs)) {
				const matched = attrValues.filter((v) => allModes.has(v));
				if (matched.length === 1) {
					out[attrName] = matched[0];
					modesConsumed = true;
				}
			}
			if (!modesConsumed) out.modes = [...allModes];
		} else if (allModes.size > 0) out.modes = [...allModes];
		return out;
	});
}
/** Unescaped colon = dynamic param marker in vue-router path format. */
const UNESCAPED_COLON_RE = /(?:^|[^\\]):/;
function computeScoreSegments(route) {
	return route.path.split("/").filter(Boolean).map((part) => {
		if (part.includes("(.*)*") || part.includes("([^/]*)*")) return -400;
		if (UNESCAPED_COLON_RE.test(part)) return part.includes("?") ? 100 : part.includes("+") ? 200 : part.includes("*") ? 50 : 300;
		return 400;
	});
}
function sanitizeCaptureGroup(value) {
	return value.replace(/^(\d)/, "_$1").replace(/\./g, "");
}
//#endregion
//#region src/parse.ts
const VIEW_MATCH_RE = /(?<=[\w\]])@([\w-]+)(?:\.|$)/;
const VIEW_STRIP_RE = /(?<=[\w\]])@[\w-]+/;
const DEFAULT_EXT_RE = /\.\w+$/;
function parsePath(filePaths, options = {}) {
	const EXT_RE = options.extensions ? new RegExp(`\\.(${options.extensions.map((ext) => ext.replace(/^\./, "").replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})$`) : DEFAULT_EXT_RE;
	const sortedRoots = [...options.roots || []].sort((a, b) => b.length - a.length);
	return parsePathInner(filePaths, EXT_RE, sortedRoots.length > 0 ? new RegExp(`^(?:${sortedRoots.map((root) => escapeStringRegexp(withTrailingSlash(root))).join("|")})`) : void 0, options.modes || [], options.warn);
}
function compileParsePath(options = {}) {
	const EXT_RE = options.extensions ? new RegExp(`\\.(${options.extensions.map((ext) => ext.replace(/^\./, "").replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})$`) : DEFAULT_EXT_RE;
	const sortedRoots = [...options.roots || []].sort((a, b) => b.length - a.length);
	const PREFIX_RE = sortedRoots.length > 0 ? new RegExp(`^(?:${sortedRoots.map((root) => escapeStringRegexp(withTrailingSlash(root))).join("|")})`) : void 0;
	const supportedModes = options.modes || [];
	const warn = options.warn;
	const fn = (filePaths) => parsePathInner(filePaths, EXT_RE, PREFIX_RE, supportedModes, warn);
	fn["~compiled"] = true;
	return fn;
}
function parsePathInner(filePaths, EXT_RE, PREFIX_RE, supportedModes, warn) {
	const results = [];
	for (let filePath of filePaths) {
		const originalFilePath = filePath;
		if (PREFIX_RE) filePath = filePath.replace(PREFIX_RE, "");
		filePath = filePath.replace(EXT_RE, "");
		let namedView;
		const viewMatch = filePath.match(VIEW_MATCH_RE);
		if (viewMatch) {
			namedView = viewMatch[1];
			filePath = filePath.replace(VIEW_STRIP_RE, "");
		}
		const modes = [];
		let scanning = true;
		while (scanning) {
			scanning = false;
			for (const mode of supportedModes) if (filePath.endsWith(`.${mode}`)) {
				modes.unshift(mode);
				filePath = filePath.slice(0, -(mode.length + 1));
				scanning = true;
				break;
			}
		}
		const normalized = withoutLeadingSlash(withoutTrailingSlash(filePath));
		const segments = normalized === "/" ? [""] : normalized.split("/");
		const hasModes = modes.length > 0;
		const hasMeta = hasModes || !!namedView;
		results.push({
			file: originalFilePath,
			segments: segments.map((s) => parseSegment(s, originalFilePath, warn)),
			meta: hasMeta ? {
				...hasModes ? { modes } : void 0,
				...namedView ? { name: namedView } : void 0
			} : void 0
		});
	}
	return results;
}
const PARAM_CHAR_RE = /[\w.]/;
function parseSegment(segment, absolutePath, warn) {
	if (segment === "") return [{
		type: "static",
		value: ""
	}];
	let state = "initial";
	let i = 0;
	let buffer = "";
	const tokens = [];
	function flush(type) {
		tokens.push({
			type,
			value: buffer
		});
		buffer = "";
	}
	while (i < segment.length) {
		const c = segment[i];
		switch (state) {
			case "initial":
				buffer = "";
				if (c === "[") state = "dynamic";
				else if (c === "(") state = "group";
				else {
					i--;
					state = "static";
				}
				break;
			case "static":
				if (c === "[") {
					flush(state);
					state = "dynamic";
				} else if (c === "(") {
					flush(state);
					state = "group";
				} else buffer += c;
				break;
			case "catchall":
			case "dynamic":
			case "optional":
			case "group":
				if (buffer === "...") {
					buffer = "";
					state = "catchall";
				}
				if (c === "[" && state === "dynamic") state = "optional";
				if (c === "]" && (state !== "optional" || segment[i - 1] === "]")) {
					if (!buffer) throw new Error("Empty param");
					if (segment[i + 1] === "+") {
						tokens.push({
							type: state === "optional" ? "optional-repeatable" : "repeatable",
							value: buffer
						});
						buffer = "";
						i++;
					} else flush(state);
					state = "initial";
				} else if (c === ")" && state === "group") {
					if (!buffer) throw new Error("Empty group");
					flush(state);
					state = "initial";
				} else if (c && PARAM_CHAR_RE.test(c)) buffer += c;
				else if ((state === "dynamic" || state === "optional") && c !== "[" && c !== "]") warn?.(`'${c}' is not allowed in a dynamic route parameter and has been ignored. Consider renaming '${absolutePath}'.`);
				break;
		}
		i++;
	}
	if (state === "dynamic") throw new Error(`Unfinished param "${buffer}"`);
	if (state === "group") throw new Error(`Unfinished group "${buffer}"`);
	if (state !== "initial" && buffer) flush(state);
	if (tokens.length === 1 && tokens[0].type === "static" && tokens[0].value === "index") tokens[0].value = "";
	return tokens;
}
//#endregion
//#region src/tree.ts
function createNode(rawSegment, segment, parent) {
	return {
		rawSegment,
		segment,
		files: [],
		children: /* @__PURE__ */ new Map(),
		parent
	};
}
/**
* Build a route tree from file paths.
*
* Accepts `string[]`, `InputFile[]`, or `ParsedPath[]`.
* On collision, the file with the lowest priority number wins.
*/
function buildTree(input, options = {}) {
	const root = createNode("", [{
		type: "static",
		value: ""
	}], null);
	const fileIndex = /* @__PURE__ */ new Map();
	if (input.length === 0) return {
		root,
		"~dirty": true,
		"~fileIndex": fileIndex
	};
	if (isParsedPaths(input)) for (const p of input) insertParsedPath(root, p, 0, options, fileIndex);
	else if (isInputFiles(input)) {
		const paths = input.map((f) => f.path);
		const priorities = input.map((f) => f.priority ?? 0);
		const parsed = parsePath(paths, options);
		for (let i = 0; i < parsed.length; i++) insertParsedPath(root, parsed[i], priorities[i], options, fileIndex);
	} else {
		const parsed = parsePath(input, options);
		for (const p of parsed) insertParsedPath(root, p, 0, options, fileIndex);
	}
	return {
		root,
		"~dirty": true,
		"~fileIndex": fileIndex
	};
}
function isParsedPaths(input) {
	const first = input[0];
	return !!first && typeof first === "object" && "segments" in first;
}
function isInputFiles(input) {
	const first = input[0];
	return !!first && typeof first === "object" && "path" in first && !("segments" in first);
}
function insertParsedPath(root, parsedPath, priority, options, fileIndex) {
	let current = root;
	const groups = [];
	for (const segment of parsedPath.segments) {
		if (segment.every((token) => token.type === "group")) {
			for (const token of segment) groups.push(token.value);
			continue;
		}
		const key = segmentToKey(segment);
		if (!current.children.has(key)) current.children.set(key, createNode(key, segment, current));
		current = current.children.get(key);
	}
	const viewName = parsedPath.meta?.name || "default";
	const modes = parsedPath.meta?.modes;
	const dedupeKey = `${viewName}\0${groups.join(",")}\0${modes?.slice().sort().join(",") ?? ""}`;
	const fileEntry = {
		"path": parsedPath.file,
		"relativePath": reconstructRelativePath(parsedPath),
		viewName,
		modes,
		"groups": [...groups],
		"originalSegments": parsedPath.segments,
		priority,
		"~dedupeKey": dedupeKey
	};
	const existing = current.files.find((f) => f["~dedupeKey"] === dedupeKey);
	if (!existing) {
		current.files.push(fileEntry);
		fileIndex?.set(parsedPath.file, current);
		return;
	}
	const strategy = options.duplicateStrategy || "first-wins";
	if (strategy === "error") throw new Error(`Duplicate route file for view "${viewName}": "${existing.path}" and "${parsedPath.file}"`);
	const idx = current.files.indexOf(existing);
	if (strategy === "last-wins" || priority < existing.priority) {
		fileIndex?.delete(existing.path);
		current.files[idx] = fileEntry;
		fileIndex?.set(parsedPath.file, current);
	}
}
/**
* Add a single file to an existing route tree.
*
* Parses the file path and inserts it into the tree in-place, avoiding a full
* rebuild. Useful for dev-server HMR when a file is added or renamed.
*
* The `options` parameter accepts either raw `BuildTreeOptions` or a
* pre-compiled `CompiledParsePath` (from `compileParsePath()`) for faster
* repeated calls.
*/
function addFile(tree, filePath, options = {}) {
	const path = typeof filePath === "string" ? filePath : filePath.path;
	const priority = typeof filePath === "string" ? 0 : filePath.priority ?? 0;
	const parseOne = isCompiledParsePath(options) ? options : parsePath;
	const parseOpts = isCompiledParsePath(options) ? void 0 : options;
	const [parsed] = parseOne([path], parseOpts);
	insertParsedPath(tree.root, parsed, priority, isCompiledParsePath(options) ? {} : options, tree["~fileIndex"]);
	tree["~dirty"] = true;
}
/**
* Remove a file from an existing route tree by its original file path.
*
* Prunes empty structural nodes left behind. Returns `true` if the file was
* found and removed.
*/
function removeFile(tree, filePath) {
	const node = tree["~fileIndex"]?.get(filePath);
	if (node) {
		const idx = node.files.findIndex((f) => f.path === filePath);
		if (idx !== -1) {
			node.files.splice(idx, 1);
			tree["~fileIndex"].delete(filePath);
			pruneEmptyAncestors(node);
			tree["~dirty"] = true;
			return true;
		}
	}
	const removed = removeFromNode(tree.root, filePath);
	if (removed) tree["~dirty"] = true;
	return removed;
}
function removeFromNode(node, filePath) {
	const idx = node.files.findIndex((f) => f.path === filePath);
	if (idx !== -1) {
		node.files.splice(idx, 1);
		pruneEmptyAncestors(node);
		return true;
	}
	for (const child of node.children.values()) if (removeFromNode(child, filePath)) return true;
	return false;
}
function pruneEmptyAncestors(node) {
	let current = node;
	while (current && current.parent) if (current.files.length === 0 && current.children.size === 0) {
		current.parent.children.delete(current.rawSegment);
		current = current.parent;
	} else break;
}
/** Walk the tree depth-first, calling `visitor` for each non-root node. */
function walkTree(tree, visitor) {
	function walk(node, depth) {
		if (depth > 0) visitor(node, depth, node.parent);
		for (const child of node.children.values()) walk(child, depth + 1);
	}
	walk(tree.root, 0);
}
/** True if the node has files attached (is a "page node"). */
function isPageNode(node) {
	return node.files.length > 0;
}
function isCompiledParsePath(options) {
	return typeof options === "function" && options["~compiled"] === true;
}
function tokenToString(token) {
	switch (token.type) {
		case "static": return token.value;
		case "dynamic": return `[${token.value}]`;
		case "optional": return `[[${token.value}]]`;
		case "catchall": return `[...${token.value}]`;
		case "repeatable": return `[${token.value}]+`;
		case "optional-repeatable": return `[[${token.value}]]+`;
		case "group": return `(${token.value})`;
		default: return token.value;
	}
}
function segmentToKey(segment) {
	return segment.map(tokenToString).join("");
}
function reconstructRelativePath(parsedPath) {
	const ext = parsedPath.file.match(/\.[^./]+$/)?.[0] || "";
	return parsedPath.segments.map((seg) => seg.map((t) => t.type === "static" && t.value === "" ? "index" : tokenToString(t)).join("")).join("/") + ext;
}
//#endregion
export { addFile, buildTree, compileParsePath, isPageNode, parsePath, parseSegment, removeFile, toRegExp, toRou3, toVueRouter4, toVueRouterPath, toVueRouterSegment, walkTree };
