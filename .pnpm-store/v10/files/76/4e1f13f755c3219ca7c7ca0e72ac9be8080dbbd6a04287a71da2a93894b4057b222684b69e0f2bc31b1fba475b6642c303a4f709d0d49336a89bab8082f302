import { _ as withTrailingSlash } from "./utils-ExLpYVUV.mjs";
import fs from "node:fs";
import process from "node:process";
import { dirname, isAbsolute, relative, resolve } from "pathe";
import { Buffer as Buffer$1 } from "node:buffer";
import path from "node:path";

//#region node_modules/.pnpm/@jridgewell+sourcemap-codec@1.5.5/node_modules/@jridgewell/sourcemap-codec/dist/sourcemap-codec.mjs
var comma = ",".charCodeAt(0);
var semicolon = ";".charCodeAt(0);
var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
var intToChar = new Uint8Array(64);
var charToInt = new Uint8Array(128);
for (let i = 0; i < chars.length; i++) {
	const c = chars.charCodeAt(i);
	intToChar[i] = c;
	charToInt[c] = i;
}
function decodeInteger(reader, relative$1) {
	let value = 0;
	let shift = 0;
	let integer = 0;
	do {
		integer = charToInt[reader.next()];
		value |= (integer & 31) << shift;
		shift += 5;
	} while (integer & 32);
	const shouldNegate = value & 1;
	value >>>= 1;
	if (shouldNegate) value = -2147483648 | -value;
	return relative$1 + value;
}
function hasMoreVlq(reader, max) {
	if (reader.pos >= max) return false;
	return reader.peek() !== comma;
}
var bufLength = 1024 * 16;
var StringReader = class {
	constructor(buffer) {
		this.pos = 0;
		this.buffer = buffer;
	}
	next() {
		return this.buffer.charCodeAt(this.pos++);
	}
	peek() {
		return this.buffer.charCodeAt(this.pos);
	}
	indexOf(char) {
		const { buffer, pos } = this;
		const idx = buffer.indexOf(char, pos);
		return idx === -1 ? buffer.length : idx;
	}
};
function decode(mappings) {
	const { length } = mappings;
	const reader = new StringReader(mappings);
	const decoded = [];
	let genColumn = 0;
	let sourcesIndex = 0;
	let sourceLine = 0;
	let sourceColumn = 0;
	let namesIndex = 0;
	do {
		const semi = reader.indexOf(";");
		const line = [];
		let sorted = true;
		let lastCol = 0;
		genColumn = 0;
		while (reader.pos < semi) {
			let seg;
			genColumn = decodeInteger(reader, genColumn);
			if (genColumn < lastCol) sorted = false;
			lastCol = genColumn;
			if (hasMoreVlq(reader, semi)) {
				sourcesIndex = decodeInteger(reader, sourcesIndex);
				sourceLine = decodeInteger(reader, sourceLine);
				sourceColumn = decodeInteger(reader, sourceColumn);
				if (hasMoreVlq(reader, semi)) {
					namesIndex = decodeInteger(reader, namesIndex);
					seg = [
						genColumn,
						sourcesIndex,
						sourceLine,
						sourceColumn,
						namesIndex
					];
				} else seg = [
					genColumn,
					sourcesIndex,
					sourceLine,
					sourceColumn
				];
			} else seg = [genColumn];
			line.push(seg);
			reader.pos++;
		}
		if (!sorted) sort(line);
		decoded.push(line);
		reader.pos = semi + 1;
	} while (reader.pos <= length);
	return decoded;
}
function sort(line) {
	line.sort(sortComparator$1);
}
function sortComparator$1(a, b) {
	return a[0] - b[0];
}

//#endregion
//#region node_modules/.pnpm/@jridgewell+resolve-uri@3.1.2/node_modules/@jridgewell/resolve-uri/dist/resolve-uri.mjs
const schemeRegex = /^[\w+.-]+:\/\//;
/**
* Matches the parts of a URL:
* 1. Scheme, including ":", guaranteed.
* 2. User/password, including "@", optional.
* 3. Host, guaranteed.
* 4. Port, including ":", optional.
* 5. Path, including "/", optional.
* 6. Query, including "?", optional.
* 7. Hash, including "#", optional.
*/
const urlRegex = /^([\w+.-]+:)\/\/([^@/#?]*@)?([^:/#?]*)(:\d+)?(\/[^#?]*)?(\?[^#]*)?(#.*)?/;
/**
* File URLs are weird. They dont' need the regular `//` in the scheme, they may or may not start
* with a leading `/`, they can have a domain (but only if they don't start with a Windows drive).
*
* 1. Host, optional.
* 2. Path, which may include "/", guaranteed.
* 3. Query, including "?", optional.
* 4. Hash, including "#", optional.
*/
const fileRegex = /^file:(?:\/\/((?![a-z]:)[^/#?]*)?)?(\/?[^#?]*)(\?[^#]*)?(#.*)?/i;
function isAbsoluteUrl(input) {
	return schemeRegex.test(input);
}
function isSchemeRelativeUrl(input) {
	return input.startsWith("//");
}
function isAbsolutePath(input) {
	return input.startsWith("/");
}
function isFileUrl(input) {
	return input.startsWith("file:");
}
function isRelative(input) {
	return /^[.?#]/.test(input);
}
function parseAbsoluteUrl(input) {
	const match = urlRegex.exec(input);
	return makeUrl(match[1], match[2] || "", match[3], match[4] || "", match[5] || "/", match[6] || "", match[7] || "");
}
function parseFileUrl(input) {
	const match = fileRegex.exec(input);
	const path$1 = match[2];
	return makeUrl("file:", "", match[1] || "", "", isAbsolutePath(path$1) ? path$1 : "/" + path$1, match[3] || "", match[4] || "");
}
function makeUrl(scheme, user, host, port, path$1, query, hash) {
	return {
		scheme,
		user,
		host,
		port,
		path: path$1,
		query,
		hash,
		type: 7
	};
}
function parseUrl(input) {
	if (isSchemeRelativeUrl(input)) {
		const url$1 = parseAbsoluteUrl("http:" + input);
		url$1.scheme = "";
		url$1.type = 6;
		return url$1;
	}
	if (isAbsolutePath(input)) {
		const url$1 = parseAbsoluteUrl("http://foo.com" + input);
		url$1.scheme = "";
		url$1.host = "";
		url$1.type = 5;
		return url$1;
	}
	if (isFileUrl(input)) return parseFileUrl(input);
	if (isAbsoluteUrl(input)) return parseAbsoluteUrl(input);
	const url = parseAbsoluteUrl("http://foo.com/" + input);
	url.scheme = "";
	url.host = "";
	url.type = input ? input.startsWith("?") ? 3 : input.startsWith("#") ? 2 : 4 : 1;
	return url;
}
function stripPathFilename(path$1) {
	if (path$1.endsWith("/..")) return path$1;
	const index = path$1.lastIndexOf("/");
	return path$1.slice(0, index + 1);
}
function mergePaths(url, base) {
	normalizePath(base, base.type);
	if (url.path === "/") url.path = base.path;
	else url.path = stripPathFilename(base.path) + url.path;
}
/**
* The path can have empty directories "//", unneeded parents "foo/..", or current directory
* "foo/.". We need to normalize to a standard representation.
*/
function normalizePath(url, type) {
	const rel = type <= 4;
	const pieces = url.path.split("/");
	let pointer = 1;
	let positive = 0;
	let addTrailingSlash = false;
	for (let i = 1; i < pieces.length; i++) {
		const piece = pieces[i];
		if (!piece) {
			addTrailingSlash = true;
			continue;
		}
		addTrailingSlash = false;
		if (piece === ".") continue;
		if (piece === "..") {
			if (positive) {
				addTrailingSlash = true;
				positive--;
				pointer--;
			} else if (rel) pieces[pointer++] = piece;
			continue;
		}
		pieces[pointer++] = piece;
		positive++;
	}
	let path$1 = "";
	for (let i = 1; i < pointer; i++) path$1 += "/" + pieces[i];
	if (!path$1 || addTrailingSlash && !path$1.endsWith("/..")) path$1 += "/";
	url.path = path$1;
}
/**
* Attempts to resolve `input` URL/path relative to `base`.
*/
function resolve$2(input, base) {
	if (!input && !base) return "";
	const url = parseUrl(input);
	let inputType = url.type;
	if (base && inputType !== 7) {
		const baseUrl = parseUrl(base);
		const baseType = baseUrl.type;
		switch (inputType) {
			case 1: url.hash = baseUrl.hash;
			case 2: url.query = baseUrl.query;
			case 3:
			case 4: mergePaths(url, baseUrl);
			case 5:
				url.user = baseUrl.user;
				url.host = baseUrl.host;
				url.port = baseUrl.port;
			case 6: url.scheme = baseUrl.scheme;
		}
		if (baseType > inputType) inputType = baseType;
	}
	normalizePath(url, inputType);
	const queryHash = url.query + url.hash;
	switch (inputType) {
		case 2:
		case 3: return queryHash;
		case 4: {
			const path$1 = url.path.slice(1);
			if (!path$1) return queryHash || ".";
			if (isRelative(base || input) && !isRelative(path$1)) return "./" + path$1 + queryHash;
			return path$1 + queryHash;
		}
		case 5: return url.path + queryHash;
		default: return url.scheme + "//" + url.user + url.host + url.port + url.path + queryHash;
	}
}

//#endregion
//#region node_modules/.pnpm/@jridgewell+trace-mapping@0.3.31/node_modules/@jridgewell/trace-mapping/dist/trace-mapping.mjs
function stripFilename(path$1) {
	if (!path$1) return "";
	const index = path$1.lastIndexOf("/");
	return path$1.slice(0, index + 1);
}
function resolver(mapUrl, sourceRoot) {
	const from = stripFilename(mapUrl);
	const prefix = sourceRoot ? sourceRoot + "/" : "";
	return (source) => resolve$2(prefix + (source || ""), from);
}
var COLUMN = 0;
var SOURCES_INDEX = 1;
var SOURCE_LINE = 2;
var SOURCE_COLUMN = 3;
var NAMES_INDEX = 4;
function maybeSort(mappings, owned) {
	const unsortedIndex = nextUnsortedSegmentLine(mappings, 0);
	if (unsortedIndex === mappings.length) return mappings;
	if (!owned) mappings = mappings.slice();
	for (let i = unsortedIndex; i < mappings.length; i = nextUnsortedSegmentLine(mappings, i + 1)) mappings[i] = sortSegments(mappings[i], owned);
	return mappings;
}
function nextUnsortedSegmentLine(mappings, start) {
	for (let i = start; i < mappings.length; i++) if (!isSorted(mappings[i])) return i;
	return mappings.length;
}
function isSorted(line) {
	for (let j = 1; j < line.length; j++) if (line[j][COLUMN] < line[j - 1][COLUMN]) return false;
	return true;
}
function sortSegments(line, owned) {
	if (!owned) line = line.slice();
	return line.sort(sortComparator);
}
function sortComparator(a, b) {
	return a[COLUMN] - b[COLUMN];
}
var found = false;
function binarySearch(haystack, needle, low, high) {
	while (low <= high) {
		const mid = low + (high - low >> 1);
		const cmp = haystack[mid][COLUMN] - needle;
		if (cmp === 0) {
			found = true;
			return mid;
		}
		if (cmp < 0) low = mid + 1;
		else high = mid - 1;
	}
	found = false;
	return low - 1;
}
function upperBound(haystack, needle, index) {
	for (let i = index + 1; i < haystack.length; index = i++) if (haystack[i][COLUMN] !== needle) break;
	return index;
}
function lowerBound(haystack, needle, index) {
	for (let i = index - 1; i >= 0; index = i--) if (haystack[i][COLUMN] !== needle) break;
	return index;
}
function memoizedState() {
	return {
		lastKey: -1,
		lastNeedle: -1,
		lastIndex: -1
	};
}
function memoizedBinarySearch(haystack, needle, state, key) {
	const { lastKey, lastNeedle, lastIndex } = state;
	let low = 0;
	let high = haystack.length - 1;
	if (key === lastKey) {
		if (needle === lastNeedle) {
			found = lastIndex !== -1 && haystack[lastIndex][COLUMN] === needle;
			return lastIndex;
		}
		if (needle >= lastNeedle) low = lastIndex === -1 ? 0 : lastIndex;
		else high = lastIndex;
	}
	state.lastKey = key;
	state.lastNeedle = needle;
	return state.lastIndex = binarySearch(haystack, needle, low, high);
}
function parse(map) {
	return typeof map === "string" ? JSON.parse(map) : map;
}
var LINE_GTR_ZERO = "`line` must be greater than 0 (lines start at line 1)";
var COL_GTR_EQ_ZERO = "`column` must be greater than or equal to 0 (columns start at column 0)";
var LEAST_UPPER_BOUND = -1;
var GREATEST_LOWER_BOUND = 1;
var TraceMap = class {
	constructor(map, mapUrl) {
		const isString = typeof map === "string";
		if (!isString && map._decodedMemo) return map;
		const parsed = parse(map);
		const { version, file, names, sourceRoot, sources, sourcesContent } = parsed;
		this.version = version;
		this.file = file;
		this.names = names || [];
		this.sourceRoot = sourceRoot;
		this.sources = sources;
		this.sourcesContent = sourcesContent;
		this.ignoreList = parsed.ignoreList || parsed.x_google_ignoreList || void 0;
		const resolve$3 = resolver(mapUrl, sourceRoot);
		this.resolvedSources = sources.map(resolve$3);
		const { mappings } = parsed;
		if (typeof mappings === "string") {
			this._encoded = mappings;
			this._decoded = void 0;
		} else if (Array.isArray(mappings)) {
			this._encoded = void 0;
			this._decoded = maybeSort(mappings, isString);
		} else if (parsed.sections) throw new Error(`TraceMap passed sectioned source map, please use FlattenMap export instead`);
		else throw new Error(`invalid source map: ${JSON.stringify(parsed)}`);
		this._decodedMemo = memoizedState();
		this._bySources = void 0;
		this._bySourceMemos = void 0;
	}
};
function cast(map) {
	return map;
}
function decodedMappings(map) {
	var _a;
	return (_a = cast(map))._decoded || (_a._decoded = decode(cast(map)._encoded));
}
function originalPositionFor(map, needle) {
	let { line, column, bias } = needle;
	line--;
	if (line < 0) throw new Error(LINE_GTR_ZERO);
	if (column < 0) throw new Error(COL_GTR_EQ_ZERO);
	const decoded = decodedMappings(map);
	if (line >= decoded.length) return OMapping(null, null, null, null);
	const segments = decoded[line];
	const index = traceSegmentInternal(segments, cast(map)._decodedMemo, line, column, bias || GREATEST_LOWER_BOUND);
	if (index === -1) return OMapping(null, null, null, null);
	const segment = segments[index];
	if (segment.length === 1) return OMapping(null, null, null, null);
	const { names, resolvedSources } = map;
	return OMapping(resolvedSources[segment[SOURCES_INDEX]], segment[SOURCE_LINE] + 1, segment[SOURCE_COLUMN], segment.length === 5 ? names[segment[NAMES_INDEX]] : null);
}
function OMapping(source, line, column, name) {
	return {
		source,
		line,
		column,
		name
	};
}
function traceSegmentInternal(segments, memo, line, column, bias) {
	let index = memoizedBinarySearch(segments, column, memo, line);
	if (found) index = (bias === LEAST_UPPER_BOUND ? upperBound : lowerBound)(segments, column, index);
	else if (bias === LEAST_UPPER_BOUND) index++;
	if (index === -1 || index === segments.length) return -1;
	return index;
}

//#endregion
//#region src/source-map-handler.ts
let errorFormatterInstalled = false;
const fileContentsCache = {};
const sourceMapCache = {};
const reSourceMap = /^data:application\/json[^,]+base64,/;
let retrieveFileHandlers = [];
let retrieveMapHandlers = [];
function globalProcessVersion() {
	if (typeof process === "object" && process !== null) return process.version;
	else return "";
}
function handlerExec(list) {
	return function(arg) {
		for (let i = 0; i < list.length; i++) {
			const ret = list[i](arg);
			if (ret) return ret;
		}
		return null;
	};
}
let retrieveFile = handlerExec(retrieveFileHandlers);
retrieveFileHandlers.push((path$1) => {
	path$1 = path$1.trim();
	if (path$1.startsWith("file:")) path$1 = path$1.replace(/file:\/\/\/(\w:)?/, (protocol, drive) => {
		return drive ? "" : "/";
	});
	if (path$1 in fileContentsCache) return fileContentsCache[path$1];
	let contents = "";
	try {
		if (fs.existsSync(path$1)) contents = fs.readFileSync(path$1, "utf8");
	} catch {}
	return fileContentsCache[path$1] = contents;
});
function supportRelativeURL(file, url) {
	if (!file) return url;
	const dir = path.dirname(file);
	const match = /^\w+:\/\/[^/]*/.exec(dir);
	let protocol = match ? match[0] : "";
	const startPath = dir.slice(protocol.length);
	if (protocol && /^\/\w:/.test(startPath)) {
		protocol += "/";
		return protocol + path.resolve(dir.slice(protocol.length), url).replace(/\\/g, "/");
	}
	return protocol + path.resolve(dir.slice(protocol.length), url);
}
function retrieveSourceMapURL(source) {
	const fileData = retrieveFile(source);
	if (!fileData) return null;
	const re = /\/\/[@#]\s*sourceMappingURL=([^\s'"]+)\s*$|\/\*[@#]\s*sourceMappingURL=[^\s*'"]+\s*\*\/\s*$/gm;
	let lastMatch, match;
	while (match = re.exec(fileData)) lastMatch = match;
	if (!lastMatch) return null;
	return lastMatch[1];
}
let retrieveSourceMap = handlerExec(retrieveMapHandlers);
retrieveMapHandlers.push((source) => {
	let sourceMappingURL = retrieveSourceMapURL(source);
	if (!sourceMappingURL) return null;
	let sourceMapData;
	if (reSourceMap.test(sourceMappingURL)) {
		const rawData = sourceMappingURL.slice(sourceMappingURL.indexOf(",") + 1);
		sourceMapData = Buffer$1.from(rawData, "base64").toString();
		sourceMappingURL = source;
	} else {
		sourceMappingURL = supportRelativeURL(source, sourceMappingURL);
		sourceMapData = retrieveFile(sourceMappingURL);
	}
	if (!sourceMapData) return null;
	return {
		url: sourceMappingURL,
		map: sourceMapData
	};
});
function mapSourcePosition(position) {
	if (!position.source) return position;
	let sourceMap = sourceMapCache[position.source];
	if (!sourceMap) {
		const urlAndMap = retrieveSourceMap(position.source);
		const map = urlAndMap && urlAndMap.map;
		if (map && !(typeof map === "object" && "mappings" in map && map.mappings === "")) {
			sourceMap = sourceMapCache[position.source] = {
				url: urlAndMap.url,
				map: new TraceMap(map)
			};
			if (sourceMap.map?.sourcesContent) sourceMap.map.sources.forEach((source, i) => {
				const contents = sourceMap.map?.sourcesContent?.[i];
				if (contents && source && sourceMap.url) {
					const url = supportRelativeURL(sourceMap.url, source);
					fileContentsCache[url] = contents;
				}
			});
		} else sourceMap = sourceMapCache[position.source] = {
			url: null,
			map: null
		};
	}
	if (sourceMap && sourceMap.map && sourceMap.url) {
		const originalPosition = originalPositionFor(sourceMap.map, position);
		if (originalPosition.source !== null) {
			originalPosition.source = supportRelativeURL(sourceMap.url, originalPosition.source);
			return originalPosition;
		}
	}
	return position;
}
function mapEvalOrigin(origin) {
	let match = /^eval at ([^(]+) \((.+):(\d+):(\d+)\)$/.exec(origin);
	if (match) {
		const position = mapSourcePosition({
			name: null,
			source: match[2],
			line: +match[3],
			column: +match[4] - 1
		});
		return `eval at ${match[1]} (${position.source}:${position.line}:${position.column + 1})`;
	}
	match = /^eval at ([^(]+) \((.+)\)$/.exec(origin);
	if (match) return `eval at ${match[1]} (${mapEvalOrigin(match[2])})`;
	return origin;
}
function CallSiteToString() {
	let fileName;
	let fileLocation = "";
	if (this.isNative()) fileLocation = "native";
	else {
		fileName = this.getScriptNameOrSourceURL();
		if (!fileName && this.isEval()) {
			fileLocation = this.getEvalOrigin();
			fileLocation += ", ";
		}
		if (fileName) fileLocation += fileName;
		else fileLocation += "<anonymous>";
		const lineNumber = this.getLineNumber();
		if (lineNumber != null) {
			fileLocation += `:${lineNumber}`;
			const columnNumber = this.getColumnNumber();
			if (columnNumber) fileLocation += `:${columnNumber}`;
		}
	}
	let line = "";
	const functionName = this.getFunctionName();
	let addSuffix = true;
	const isConstructor = this.isConstructor();
	if (!(this.isToplevel() || isConstructor)) {
		let typeName = this.getTypeName();
		if (typeName === "[object Object]") typeName = "null";
		const methodName = this.getMethodName();
		if (functionName) {
			if (typeName && functionName.indexOf(typeName) !== 0) line += `${typeName}.`;
			line += functionName;
			if (methodName && functionName.indexOf(`.${methodName}`) !== functionName.length - methodName.length - 1) line += ` [as ${methodName}]`;
		} else line += `${typeName}.${methodName || "<anonymous>"}`;
	} else if (isConstructor) line += `new ${functionName || "<anonymous>"}`;
	else if (functionName) line += functionName;
	else {
		line += fileLocation;
		addSuffix = false;
	}
	if (addSuffix) line += ` (${fileLocation})`;
	return line;
}
function cloneCallSite(frame) {
	const object = {};
	Object.getOwnPropertyNames(Object.getPrototypeOf(frame)).forEach((name) => {
		const key = name;
		object[key] = /^(?:is|get)/.test(name) ? function() {
			return frame[key].call(frame);
		} : frame[key];
	});
	object.toString = CallSiteToString;
	return object;
}
function wrapCallSite(frame, state) {
	if (state === void 0) state = {
		nextPosition: null,
		curPosition: null
	};
	if (frame.isNative()) {
		state.curPosition = null;
		return frame;
	}
	const source = frame.getFileName() || frame.getScriptNameOrSourceURL();
	if (source) {
		const line = frame.getLineNumber();
		let column = frame.getColumnNumber() - 1;
		const headerLength = /^v(?:10\.1[6-9]|10\.[2-9]\d|10\.\d{3,}|1[2-9]\d*|[2-9]\d|\d{3,}|11\.11)/.test(globalProcessVersion()) ? 0 : 62;
		if (line === 1 && column > headerLength && !frame.isEval()) column -= headerLength;
		const position = mapSourcePosition({
			name: null,
			source,
			line,
			column
		});
		state.curPosition = position;
		frame = cloneCallSite(frame);
		const originalFunctionName = frame.getFunctionName;
		frame.getFunctionName = function() {
			if (state.nextPosition == null) return originalFunctionName();
			return state.nextPosition.name || originalFunctionName();
		};
		frame.getFileName = function() {
			return position.source ?? null;
		};
		frame.getLineNumber = function() {
			return position.line;
		};
		frame.getColumnNumber = function() {
			return position.column + 1;
		};
		frame.getScriptNameOrSourceURL = function() {
			return position.source;
		};
		return frame;
	}
	let origin = frame.isEval() && frame.getEvalOrigin();
	if (origin) {
		origin = mapEvalOrigin(origin);
		frame = cloneCallSite(frame);
		frame.getEvalOrigin = function() {
			return origin || void 0;
		};
		return frame;
	}
	return frame;
}
function prepareStackTrace(error, stack) {
	const errorString = `${error.name || "Error"}: ${error.message || ""}`;
	const state = {
		nextPosition: null,
		curPosition: null
	};
	const processedStack = [];
	for (let i = stack.length - 1; i >= 0; i--) {
		processedStack.push(`\n    at ${wrapCallSite(stack[i], state)}`);
		state.nextPosition = state.curPosition;
	}
	state.curPosition = state.nextPosition = null;
	return errorString + processedStack.reverse().join("");
}
const originalRetrieveFileHandlers = retrieveFileHandlers.slice(0);
const originalRetrieveMapHandlers = retrieveMapHandlers.slice(0);
function install(options) {
	options = options || {};
	if (options.retrieveFile) {
		if (options.overrideRetrieveFile) retrieveFileHandlers.length = 0;
		retrieveFileHandlers.unshift(options.retrieveFile);
	}
	if (options.retrieveSourceMap) {
		if (options.overrideRetrieveSourceMap) retrieveMapHandlers.length = 0;
		retrieveMapHandlers.unshift(options.retrieveSourceMap);
	}
	if (!errorFormatterInstalled) {
		errorFormatterInstalled = true;
		Error.prepareStackTrace = prepareStackTrace;
	}
}

//#endregion
//#region src/source-map.ts
let SOURCEMAPPING_URL = "sourceMa";
SOURCEMAPPING_URL += "ppingURL";
const VITE_NODE_SOURCEMAPPING_SOURCE = "//# sourceMappingSource=vite-node";
const VITE_NODE_SOURCEMAPPING_URL = `${SOURCEMAPPING_URL}=data:application/json;charset=utf-8`;
function withInlineSourcemap(result, options) {
	const map = result.map;
	let code = result.code;
	if (!map || code.includes(VITE_NODE_SOURCEMAPPING_SOURCE)) return result;
	if ("sources" in map) map.sources = map.sources?.map((source) => {
		if (!source) return source;
		if (isAbsolute(source)) {
			const actualPath = !source.startsWith(withTrailingSlash(options.root)) && source.startsWith("/") ? resolve(options.root, source.slice(1)) : source;
			return relative(dirname(options.filepath), actualPath);
		}
		return source;
	});
	const OTHER_SOURCE_MAP_REGEXP = new RegExp(`//# ${SOURCEMAPPING_URL}=data:application/json[^,]+base64,([A-Za-z0-9+/=]+)$`, "gm");
	while (OTHER_SOURCE_MAP_REGEXP.test(code)) code = code.replace(OTHER_SOURCE_MAP_REGEXP, "");
	if (!options.noFirstLineMapping && map.mappings.startsWith(";")) map.mappings = `AAAA,CAAA${map.mappings}`;
	const sourceMap = Buffer$1.from(JSON.stringify(map), "utf-8").toString("base64");
	result.code = `${code.trimEnd()}\n\n${VITE_NODE_SOURCEMAPPING_SOURCE}\n//# ${VITE_NODE_SOURCEMAPPING_URL};base64,${sourceMap}\n`;
	return result;
}
function extractSourceMap(code) {
	const regexp = new RegExp(`//# ${VITE_NODE_SOURCEMAPPING_URL};base64,(.+)`, "gm");
	let lastMatch, match;
	while (match = regexp.exec(code)) lastMatch = match;
	if (lastMatch) return JSON.parse(Buffer$1.from(lastMatch[1], "base64").toString("utf-8"));
	return null;
}
function installSourcemapsSupport(options) {
	install({ retrieveSourceMap(source) {
		const map = options.getSourceMap(source);
		if (map) return {
			url: source,
			map
		};
		return null;
	} });
}

//#endregion
export { originalPositionFor as a, TraceMap as i, installSourcemapsSupport as n, withInlineSourcemap as r, extractSourceMap as t };