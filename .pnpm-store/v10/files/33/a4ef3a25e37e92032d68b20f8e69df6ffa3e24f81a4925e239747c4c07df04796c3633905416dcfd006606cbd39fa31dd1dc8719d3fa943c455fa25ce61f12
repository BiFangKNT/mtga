/*!
 * vue-router v5.0.4
 * (c) 2026 Eduardo San Martin Morote
 * @license MIT
 */
import { pascalCase } from "scule";
import { resolve } from "pathe";
import { isPackageExists } from "local-pkg";

//#region src/unplugin/utils/index.ts
const ts = String.raw;
/**
* Pads a single-line string with spaces.
*
* @internal
*
* @param spaces The number of spaces to pad with.
* @param str The string to pad, none if omitted.
* @returns The padded string.
*/
function pad(spaces, str = "") {
	return " ".repeat(spaces) + str;
}
/**
* Formats an array of union items as a multiline union type.
*
* @internal
*
* @param items The items to format.
* @param spaces The number of spaces to indent each line.
* @returns The formatted multiline union type.
*/
function formatMultilineUnion(items, spaces) {
	return (items.length ? items : ["never"]).map((s) => `| ${s}`).join(`\n${pad(spaces)}`);
}
/**
* Converts a string value to a string literal, escaping as necessary.
*
* @internal
*
* @param str the string to convert to a string type
* @returns The string wrapped in single quotes and escaped.
* @example
* toStringLiteral('hello') // returns "'hello'"
* toStringLiteral("it's fine") // returns "'it\'s fine'"
*/
function toStringLiteral(str) {
	return `'${str.replace(/\\/g, "\\\\").replace(/'/g, "\\'")}'`;
}

//#endregion
//#region src/unplugin/core/utils.ts
function warn(msg, type = "warn") {
	console[type](`⚠️  [vue-router]: ${msg}`);
}
function logTree(tree, log) {
	log(printTree(tree));
}
const MAX_LEVEL = 1e3;
function printTree(tree, level = 0, parentPre = "", treeStr = "") {
	if (typeof tree !== "object" || level >= MAX_LEVEL) return "";
	if (tree instanceof Map) {
		const total = tree.size;
		let index = 0;
		for (const [_key, child] of tree) {
			const hasNext = index++ < total - 1;
			const { children } = child;
			treeStr += `${`${parentPre}${hasNext ? "├" : "└"}${"─" + (children.size > 0 ? "┬" : "")} `}${child}\n`;
			if (children) treeStr += printTree(children, level + 1, `${parentPre}${hasNext ? "│" : " "} `);
		}
	} else {
		const children = tree.children;
		treeStr = `${tree}\n`;
		if (children) treeStr += printTree(children, level + 1);
	}
	return treeStr;
}
/**
* Type safe alternative to Array.isArray
* https://github.com/microsoft/TypeScript/pull/48228
*/
const isArray = Array.isArray;
function trimExtension(path, extensions) {
	for (const extension of extensions) {
		const lastDot = path.endsWith(extension) ? -extension.length : 0;
		if (lastDot < 0) return path.slice(0, lastDot);
	}
	return path;
}
function throttle(fn, wait, initialWait) {
	let pendingExecutionTimeout = null;
	let pendingExecution = false;
	let executionTimeout = null;
	return () => {
		if (pendingExecutionTimeout == null) {
			pendingExecutionTimeout = setTimeout(() => {
				pendingExecutionTimeout = null;
				if (pendingExecution) {
					pendingExecution = false;
					fn();
				}
			}, wait);
			executionTimeout = setTimeout(() => {
				executionTimeout = null;
				fn();
			}, initialWait);
		} else if (executionTimeout == null) pendingExecution = true;
	};
}
const LEADING_SLASH_RE = /^\//;
const TRAILING_SLASH_RE = /\/$/;
const ESCAPED_TRAILING_SLASH_RE = /\\\/$/;
function joinPath(...paths) {
	let result = "";
	for (const path of paths) result = result.replace(TRAILING_SLASH_RE, "") + (path && "/" + path.replace(LEADING_SLASH_RE, ""));
	return result || "/";
}
function paramToName({ paramName, modifier, isSplat }) {
	return `${isSplat ? "$" : ""}${paramName.charAt(0).toUpperCase() + paramName.slice(1)}${modifier}`;
}
/**
* Creates a name based of the node path segments.
*
* @param node - the node to get the path from
* @param parent - the parent node
* @returns a route name
*/
function getPascalCaseRouteName(node) {
	if (node.parent?.isRoot() && node.value.pathSegment === "") return "Root";
	let name = node.value.subSegments.map((segment) => {
		if (typeof segment === "string") return pascalCase(segment);
		return paramToName(segment);
	}).join("");
	if (node.value.components.size && node.children.has("index")) name += "Parent";
	const parent = node.parent;
	return (parent && !parent.isRoot() ? getPascalCaseRouteName(parent).replace(/Parent$/, "") : "") + name;
}
/**
* Joins the path segments of a node into a name that corresponds to the filepath represented by the node.
*
* @param node - the node to get the path from
* @returns a route name
*/
function getFileBasedRouteName(node) {
	if (!node.parent) return "";
	return getFileBasedRouteName(node.parent) + "/" + (node.value.rawSegment === "index" ? "" : node.value.rawSegment);
}
function mergeRouteRecordOverride(a, b) {
	const merged = {};
	const keys = [...new Set([...Object.keys(a), ...Object.keys(b)])];
	for (const key of keys) if (key === "alias") merged[key] = [].concat(a.alias || [], b.alias || []);
	else if (key === "meta") merged[key] = mergeDeep(a[key] || {}, b[key] || {});
	else if (key === "params") merged[key] = {
		path: {
			...a[key]?.path,
			...b[key]?.path
		},
		query: {
			...a[key]?.query,
			...b[key]?.query
		}
	};
	else merged[key] = b[key] ?? a[key];
	return merged;
}
function isObject(obj) {
	return obj && typeof obj === "object";
}
function mergeDeep(...objects) {
	return objects.reduce((prev, obj) => {
		Object.keys(obj).forEach((key) => {
			const pVal = prev[key];
			const oVal = obj[key];
			if (Array.isArray(pVal) && Array.isArray(oVal)) prev[key] = pVal.concat(...oVal);
			else if (isObject(pVal) && isObject(oVal)) prev[key] = mergeDeep(pVal, oVal);
			else prev[key] = oVal;
		});
		return prev;
	}, {});
}
/**
* Returns a route path to be used by the router with any defined prefix from an absolute path to a file. Since it
* returns a route path, it will remove the extension from the file.
*
* @param options - RoutesFolderOption to apply
* @param filePath - absolute path to file
* @returns a route path to be used by the router with any defined prefix
*/
function asRoutePath({ src, path = "", extensions }, filePath) {
	return trimExtension(typeof path === "string" ? path + filePath.slice(src.length + 1) : path(filePath), extensions);
}
function appendExtensionListToPattern(filePatterns, extensions) {
	const extensionPattern = extensions.length === 1 ? extensions[0] : `.{${extensions.map((extension) => extension.replace(".", "")).join(",")}}`;
	return Array.isArray(filePatterns) ? filePatterns.map((filePattern) => `${filePattern}${extensionPattern}`) : `${filePatterns}${extensionPattern}`;
}
var ImportsMap = class {
	map = /* @__PURE__ */ new Map();
	constructor() {}
	add(path, importEntry) {
		if (!this.map.has(path)) this.map.set(path, /* @__PURE__ */ new Map());
		const imports = this.map.get(path);
		if (typeof importEntry === "string") imports.set(importEntry, importEntry);
		else imports.set(importEntry.as || importEntry.name, importEntry.name);
		return this;
	}
	/**
	* Check if the given path has the given import name.
	*
	* @param path - the path to check
	* @param name - the import name to check
	*/
	has(path, name) {
		return this.map.has(path) && this.map.get(path).has(name);
	}
	/**
	* Add a default import. Alias for `add(path, { name: 'default', as })`.
	*
	* @param path - the path to import from
	* @param as - the name to import as
	*/
	addDefault(path, as) {
		return this.add(path, {
			name: "default",
			as
		});
	}
	/**
	* Get the list of imports for the given path.
	*
	* @param path - the path to get the import list for
	* @returns the list of imports for the given path
	*/
	getImportList(path) {
		if (!this.map.has(path)) return [];
		return Array.from(this.map.get(path)).map(([as, name]) => ({
			as: as || name,
			name
		}));
	}
	toString() {
		let importStatements = "";
		for (const [path, imports] of this.map) {
			if (!imports.size) continue;
			const fromImportPath = toStringLiteral(path);
			if (imports.size === 1) {
				const [[importName, maybeDefault]] = [...imports.entries()];
				if (maybeDefault === "default") {
					importStatements += `import ${importName} from ${fromImportPath}\n`;
					continue;
				}
			}
			importStatements += `import { ${Array.from(imports).map(([as, name]) => as === name ? name : `${name} as ${as}`).join(", ")} } from ${fromImportPath}\n`;
		}
		return importStatements;
	}
	get size() {
		return this.map.size;
	}
};

//#endregion
//#region src/unplugin/options.ts
/**
* Resolves an overridable option by calling the function with the existing
* value if it's a function, otherwise returning the passed `value`. If `value`
* is undefined, it returns the `defaultValue` instead.
*
* @param defaultValue default value for the option
* @param value and overridable option
*
* @internal
*/
function resolveOverridableOption(defaultValue, value) {
	return typeof value === "function" ? value(defaultValue) : value ?? defaultValue;
}
/**
* Default options for experimental param parsers.
*/
const DEFAULT_PARAM_PARSERS_OPTIONS = { dir: ["src/params"] };
/**
* Default plugin options.
*/
const DEFAULT_OPTIONS = {
	extensions: [".vue"],
	exclude: [],
	routesFolder: "src/pages",
	filePatterns: ["**/*"],
	routeBlockLang: "json5",
	getRouteName: getFileBasedRouteName,
	importMode: "async",
	root: process.cwd(),
	dts: isPackageExists("typescript"),
	logs: false,
	_inspect: false,
	pathParser: { dotNesting: true },
	watch: !process.env.CI,
	experimental: {}
};
function normalizeRoutesFolderOption(routesFolder) {
	return (isArray(routesFolder) ? routesFolder : [routesFolder]).map((routeOption) => normalizeRouteOption(typeof routeOption === "string" ? { src: routeOption } : routeOption));
}
function normalizeRouteOption(routeOption) {
	return {
		...routeOption,
		filePatterns: routeOption.filePatterns ? typeof routeOption.filePatterns === "function" ? routeOption.filePatterns : isArray(routeOption.filePatterns) ? routeOption.filePatterns : [routeOption.filePatterns] : void 0,
		exclude: routeOption.exclude ? typeof routeOption.exclude === "function" ? routeOption.exclude : isArray(routeOption.exclude) ? routeOption.exclude : [routeOption.exclude] : void 0
	};
}
/**
* Normalize user options with defaults and resolved paths.
*
* @param options - user provided options
* @returns normalized options
*/
function resolveOptions(options) {
	const root = options.root || DEFAULT_OPTIONS.root;
	const routesFolder = normalizeRoutesFolderOption(options.routesFolder || DEFAULT_OPTIONS.routesFolder).map((routeOption) => ({
		...routeOption,
		src: resolve(root, routeOption.src)
	}));
	const paramParsers = options.experimental?.paramParsers ? options.experimental.paramParsers === true ? DEFAULT_PARAM_PARSERS_OPTIONS : {
		...DEFAULT_PARAM_PARSERS_OPTIONS,
		...options.experimental.paramParsers
	} : void 0;
	const paramParsersDir = (paramParsers?.dir ? isArray(paramParsers.dir) ? paramParsers.dir : [paramParsers.dir] : []).map((dir) => resolve(root, dir));
	const autoExportsDataLoaders = options.experimental?.autoExportsDataLoaders ? (isArray(options.experimental.autoExportsDataLoaders) ? options.experimental.autoExportsDataLoaders : [options.experimental.autoExportsDataLoaders]).map((path) => resolve(root, path)) : void 0;
	const experimental = {
		...options.experimental,
		autoExportsDataLoaders,
		paramParsers: paramParsers && {
			...paramParsers,
			dir: paramParsersDir
		}
	};
	if (options.extensions) options.extensions = options.extensions.map((ext) => {
		if (!ext.startsWith(".")) {
			warn(`Invalid extension "${ext}". Extensions must start with a dot.`);
			return "." + ext;
		}
		return ext;
	}).sort((a, b) => b.length - a.length);
	const filePatterns = options.filePatterns ? isArray(options.filePatterns) ? options.filePatterns : [options.filePatterns] : DEFAULT_OPTIONS.filePatterns;
	const exclude = options.exclude ? isArray(options.exclude) ? options.exclude : [options.exclude] : DEFAULT_OPTIONS.exclude;
	return {
		...DEFAULT_OPTIONS,
		...options,
		experimental,
		routesFolder,
		filePatterns,
		exclude
	};
}
/**
* Merge all the possible extensions as an array of unique values
* @param options - user provided options
* @internal
*/
function mergeAllExtensions(options) {
	const allExtensions = new Set(options.extensions);
	for (const routeOption of options.routesFolder) if (routeOption.extensions) {
		const extensions = resolveOverridableOption(options.extensions, routeOption.extensions);
		for (const ext of extensions) allExtensions.add(ext);
	}
	return Array.from(allExtensions.values());
}

//#endregion
export { formatMultilineUnion as _, resolveOverridableOption as a, ts as b, appendExtensionListToPattern as c, getPascalCaseRouteName as d, joinPath as f, warn as g, throttle as h, resolveOptions as i, asRoutePath as l, mergeRouteRecordOverride as m, DEFAULT_PARAM_PARSERS_OPTIONS as n, ESCAPED_TRAILING_SLASH_RE as o, logTree as p, mergeAllExtensions as r, ImportsMap as s, DEFAULT_OPTIONS as t, getFileBasedRouteName as u, pad as v, toStringLiteral as y };