import { computed } from "./runtime-core.esm-bundler-Cyv4obHQ.js";
import { defineStore, usePayloadStore } from "./payload-BX9lTMvN.js";
import { useOptionsStore } from "./options-D_MMddT_.js";
/**
* Fuse.js v7.1.0 - Lightweight fuzzy-search (http://fusejs.io)
*
* Copyright (c) 2025 Kiro Risk (http://kiro.me)
* All Rights Reserved. Apache Software License 2.0
*
* http://www.apache.org/licenses/LICENSE-2.0
*/
function isArray(value) {
	return !Array.isArray ? getTag(value) === "[object Array]" : Array.isArray(value);
}
const INFINITY = Infinity;
function baseToString(value) {
	if (typeof value == "string") return value;
	let result = value + "";
	return result == "0" && 1 / value == -INFINITY ? "-0" : result;
}
function toString(value) {
	return value == null ? "" : baseToString(value);
}
function isString(value) {
	return typeof value === "string";
}
function isNumber(value) {
	return typeof value === "number";
}
function isBoolean(value) {
	return value === true || value === false || isObjectLike(value) && getTag(value) == "[object Boolean]";
}
function isObject(value) {
	return typeof value === "object";
}
function isObjectLike(value) {
	return isObject(value) && value !== null;
}
function isDefined(value) {
	return value !== void 0 && value !== null;
}
function isBlank(value) {
	return !value.trim().length;
}
function getTag(value) {
	return value == null ? value === void 0 ? "[object Undefined]" : "[object Null]" : Object.prototype.toString.call(value);
}
const INCORRECT_INDEX_TYPE = "Incorrect 'index' type";
const LOGICAL_SEARCH_INVALID_QUERY_FOR_KEY = (key) => `Invalid value for key ${key}`;
const PATTERN_LENGTH_TOO_LARGE = (max) => `Pattern length exceeds max of ${max}.`;
const MISSING_KEY_PROPERTY = (name) => `Missing ${name} property in key`;
const INVALID_KEY_WEIGHT_VALUE = (key) => `Property 'weight' in key '${key}' must be a positive integer`;
const hasOwn = Object.prototype.hasOwnProperty;
var KeyStore = class {
	constructor(keys) {
		this._keys = [];
		this._keyMap = {};
		let totalWeight = 0;
		keys.forEach((key) => {
			let obj = createKey(key);
			this._keys.push(obj);
			this._keyMap[obj.id] = obj;
			totalWeight += obj.weight;
		});
		this._keys.forEach((key) => {
			key.weight /= totalWeight;
		});
	}
	get(keyId) {
		return this._keyMap[keyId];
	}
	keys() {
		return this._keys;
	}
	toJSON() {
		return JSON.stringify(this._keys);
	}
};
function createKey(key) {
	let path = null;
	let id = null;
	let src = null;
	let weight = 1;
	let getFn = null;
	if (isString(key) || isArray(key)) {
		src = key;
		path = createKeyPath(key);
		id = createKeyId(key);
	} else {
		if (!hasOwn.call(key, "name")) throw new Error(MISSING_KEY_PROPERTY("name"));
		const name = key.name;
		src = name;
		if (hasOwn.call(key, "weight")) {
			weight = key.weight;
			if (weight <= 0) throw new Error(INVALID_KEY_WEIGHT_VALUE(name));
		}
		path = createKeyPath(name);
		id = createKeyId(name);
		getFn = key.getFn;
	}
	return {
		path,
		id,
		weight,
		src,
		getFn
	};
}
function createKeyPath(key) {
	return isArray(key) ? key : key.split(".");
}
function createKeyId(key) {
	return isArray(key) ? key.join(".") : key;
}
function get(obj, path) {
	let list = [];
	let arr = false;
	const deepGet = (obj$1, path$1, index) => {
		if (!isDefined(obj$1)) return;
		if (!path$1[index]) list.push(obj$1);
		else {
			let key = path$1[index];
			const value = obj$1[key];
			if (!isDefined(value)) return;
			if (index === path$1.length - 1 && (isString(value) || isNumber(value) || isBoolean(value))) list.push(toString(value));
			else if (isArray(value)) {
				arr = true;
				for (let i = 0, len = value.length; i < len; i += 1) deepGet(value[i], path$1, index + 1);
			} else if (path$1.length) deepGet(value, path$1, index + 1);
		}
	};
	deepGet(obj, isString(path) ? path.split(".") : path, 0);
	return arr ? list : list[0];
}
const MatchOptions = {
	includeMatches: false,
	findAllMatches: false,
	minMatchCharLength: 1
};
const BasicOptions = {
	isCaseSensitive: false,
	ignoreDiacritics: false,
	includeScore: false,
	keys: [],
	shouldSort: true,
	sortFn: (a, b) => a.score === b.score ? a.idx < b.idx ? -1 : 1 : a.score < b.score ? -1 : 1
};
const FuzzyOptions = {
	location: 0,
	threshold: .6,
	distance: 100
};
const AdvancedOptions = {
	useExtendedSearch: false,
	getFn: get,
	ignoreLocation: false,
	ignoreFieldNorm: false,
	fieldNormWeight: 1
};
var Config = {
	...BasicOptions,
	...MatchOptions,
	...FuzzyOptions,
	...AdvancedOptions
};
const SPACE = /[^ ]+/g;
function norm(weight = 1, mantissa = 3) {
	const cache = new Map();
	const m = Math.pow(10, mantissa);
	return {
		get(value) {
			const numTokens = value.match(SPACE).length;
			if (cache.has(numTokens)) return cache.get(numTokens);
			const norm$1 = 1 / Math.pow(numTokens, .5 * weight);
			const n = parseFloat(Math.round(norm$1 * m) / m);
			cache.set(numTokens, n);
			return n;
		},
		clear() {
			cache.clear();
		}
	};
}
var FuseIndex = class {
	constructor({ getFn = Config.getFn, fieldNormWeight = Config.fieldNormWeight } = {}) {
		this.norm = norm(fieldNormWeight, 3);
		this.getFn = getFn;
		this.isCreated = false;
		this.setIndexRecords();
	}
	setSources(docs = []) {
		this.docs = docs;
	}
	setIndexRecords(records = []) {
		this.records = records;
	}
	setKeys(keys = []) {
		this.keys = keys;
		this._keysMap = {};
		keys.forEach((key, idx) => {
			this._keysMap[key.id] = idx;
		});
	}
	create() {
		if (this.isCreated || !this.docs.length) return;
		this.isCreated = true;
		if (isString(this.docs[0])) this.docs.forEach((doc, docIndex) => {
			this._addString(doc, docIndex);
		});
		else this.docs.forEach((doc, docIndex) => {
			this._addObject(doc, docIndex);
		});
		this.norm.clear();
	}
	add(doc) {
		const idx = this.size();
		if (isString(doc)) this._addString(doc, idx);
		else this._addObject(doc, idx);
	}
	removeAt(idx) {
		this.records.splice(idx, 1);
		for (let i = idx, len = this.size(); i < len; i += 1) this.records[i].i -= 1;
	}
	getValueForItemAtKeyId(item, keyId) {
		return item[this._keysMap[keyId]];
	}
	size() {
		return this.records.length;
	}
	_addString(doc, docIndex) {
		if (!isDefined(doc) || isBlank(doc)) return;
		let record = {
			v: doc,
			i: docIndex,
			n: this.norm.get(doc)
		};
		this.records.push(record);
	}
	_addObject(doc, docIndex) {
		let record = {
			i: docIndex,
			$: {}
		};
		this.keys.forEach((key, keyIndex) => {
			let value = key.getFn ? key.getFn(doc) : this.getFn(doc, key.path);
			if (!isDefined(value)) return;
			if (isArray(value)) {
				let subRecords = [];
				const stack = [{
					nestedArrIndex: -1,
					value
				}];
				while (stack.length) {
					const { nestedArrIndex, value: value$1 } = stack.pop();
					if (!isDefined(value$1)) continue;
					if (isString(value$1) && !isBlank(value$1)) {
						let subRecord = {
							v: value$1,
							i: nestedArrIndex,
							n: this.norm.get(value$1)
						};
						subRecords.push(subRecord);
					} else if (isArray(value$1)) value$1.forEach((item, k) => {
						stack.push({
							nestedArrIndex: k,
							value: item
						});
					});
				}
				record.$[keyIndex] = subRecords;
			} else if (isString(value) && !isBlank(value)) {
				let subRecord = {
					v: value,
					n: this.norm.get(value)
				};
				record.$[keyIndex] = subRecord;
			}
		});
		this.records.push(record);
	}
	toJSON() {
		return {
			keys: this.keys,
			records: this.records
		};
	}
};
function createIndex(keys, docs, { getFn = Config.getFn, fieldNormWeight = Config.fieldNormWeight } = {}) {
	const myIndex = new FuseIndex({
		getFn,
		fieldNormWeight
	});
	myIndex.setKeys(keys.map(createKey));
	myIndex.setSources(docs);
	myIndex.create();
	return myIndex;
}
function parseIndex(data, { getFn = Config.getFn, fieldNormWeight = Config.fieldNormWeight } = {}) {
	const { keys, records } = data;
	const myIndex = new FuseIndex({
		getFn,
		fieldNormWeight
	});
	myIndex.setKeys(keys);
	myIndex.setIndexRecords(records);
	return myIndex;
}
function computeScore$1(pattern, { errors = 0, currentLocation = 0, expectedLocation = 0, distance = Config.distance, ignoreLocation = Config.ignoreLocation } = {}) {
	const accuracy = errors / pattern.length;
	if (ignoreLocation) return accuracy;
	const proximity = Math.abs(expectedLocation - currentLocation);
	if (!distance) return proximity ? 1 : accuracy;
	return accuracy + proximity / distance;
}
function convertMaskToIndices(matchmask = [], minMatchCharLength = Config.minMatchCharLength) {
	let indices = [];
	let start = -1;
	let end = -1;
	let i = 0;
	for (let len = matchmask.length; i < len; i += 1) {
		let match = matchmask[i];
		if (match && start === -1) start = i;
		else if (!match && start !== -1) {
			end = i - 1;
			if (end - start + 1 >= minMatchCharLength) indices.push([start, end]);
			start = -1;
		}
	}
	if (matchmask[i - 1] && i - start >= minMatchCharLength) indices.push([start, i - 1]);
	return indices;
}
const MAX_BITS = 32;
function search(text, pattern, patternAlphabet, { location = Config.location, distance = Config.distance, threshold = Config.threshold, findAllMatches = Config.findAllMatches, minMatchCharLength = Config.minMatchCharLength, includeMatches = Config.includeMatches, ignoreLocation = Config.ignoreLocation } = {}) {
	if (pattern.length > MAX_BITS) throw new Error(PATTERN_LENGTH_TOO_LARGE(MAX_BITS));
	const patternLen = pattern.length;
	const textLen = text.length;
	const expectedLocation = Math.max(0, Math.min(location, textLen));
	let currentThreshold = threshold;
	let bestLocation = expectedLocation;
	const computeMatches = minMatchCharLength > 1 || includeMatches;
	const matchMask = computeMatches ? Array(textLen) : [];
	let index;
	while ((index = text.indexOf(pattern, bestLocation)) > -1) {
		let score = computeScore$1(pattern, {
			currentLocation: index,
			expectedLocation,
			distance,
			ignoreLocation
		});
		currentThreshold = Math.min(score, currentThreshold);
		bestLocation = index + patternLen;
		if (computeMatches) {
			let i = 0;
			while (i < patternLen) {
				matchMask[index + i] = 1;
				i += 1;
			}
		}
	}
	bestLocation = -1;
	let lastBitArr = [];
	let finalScore = 1;
	let binMax = patternLen + textLen;
	const mask = 1 << patternLen - 1;
	for (let i = 0; i < patternLen; i += 1) {
		let binMin = 0;
		let binMid = binMax;
		while (binMin < binMid) {
			const score$1 = computeScore$1(pattern, {
				errors: i,
				currentLocation: expectedLocation + binMid,
				expectedLocation,
				distance,
				ignoreLocation
			});
			if (score$1 <= currentThreshold) binMin = binMid;
			else binMax = binMid;
			binMid = Math.floor((binMax - binMin) / 2 + binMin);
		}
		binMax = binMid;
		let start = Math.max(1, expectedLocation - binMid + 1);
		let finish = findAllMatches ? textLen : Math.min(expectedLocation + binMid, textLen) + patternLen;
		let bitArr = Array(finish + 2);
		bitArr[finish + 1] = (1 << i) - 1;
		for (let j = finish; j >= start; j -= 1) {
			let currentLocation = j - 1;
			let charMatch = patternAlphabet[text.charAt(currentLocation)];
			if (computeMatches) matchMask[currentLocation] = +!!charMatch;
			bitArr[j] = (bitArr[j + 1] << 1 | 1) & charMatch;
			if (i) bitArr[j] |= (lastBitArr[j + 1] | lastBitArr[j]) << 1 | 1 | lastBitArr[j + 1];
			if (bitArr[j] & mask) {
				finalScore = computeScore$1(pattern, {
					errors: i,
					currentLocation,
					expectedLocation,
					distance,
					ignoreLocation
				});
				if (finalScore <= currentThreshold) {
					currentThreshold = finalScore;
					bestLocation = currentLocation;
					if (bestLocation <= expectedLocation) break;
					start = Math.max(1, 2 * expectedLocation - bestLocation);
				}
			}
		}
		const score = computeScore$1(pattern, {
			errors: i + 1,
			currentLocation: expectedLocation,
			expectedLocation,
			distance,
			ignoreLocation
		});
		if (score > currentThreshold) break;
		lastBitArr = bitArr;
	}
	const result = {
		isMatch: bestLocation >= 0,
		score: Math.max(.001, finalScore)
	};
	if (computeMatches) {
		const indices = convertMaskToIndices(matchMask, minMatchCharLength);
		if (!indices.length) result.isMatch = false;
		else if (includeMatches) result.indices = indices;
	}
	return result;
}
function createPatternAlphabet(pattern) {
	let mask = {};
	for (let i = 0, len = pattern.length; i < len; i += 1) {
		const char = pattern.charAt(i);
		mask[char] = (mask[char] || 0) | 1 << len - i - 1;
	}
	return mask;
}
const stripDiacritics = String.prototype.normalize ? (str) => str.normalize("NFD").replace(/[\u0300-\u036F\u0483-\u0489\u0591-\u05BD\u05BF\u05C1\u05C2\u05C4\u05C5\u05C7\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06DC\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED\u0711\u0730-\u074A\u07A6-\u07B0\u07EB-\u07F3\u07FD\u0816-\u0819\u081B-\u0823\u0825-\u0827\u0829-\u082D\u0859-\u085B\u08D3-\u08E1\u08E3-\u0903\u093A-\u093C\u093E-\u094F\u0951-\u0957\u0962\u0963\u0981-\u0983\u09BC\u09BE-\u09C4\u09C7\u09C8\u09CB-\u09CD\u09D7\u09E2\u09E3\u09FE\u0A01-\u0A03\u0A3C\u0A3E-\u0A42\u0A47\u0A48\u0A4B-\u0A4D\u0A51\u0A70\u0A71\u0A75\u0A81-\u0A83\u0ABC\u0ABE-\u0AC5\u0AC7-\u0AC9\u0ACB-\u0ACD\u0AE2\u0AE3\u0AFA-\u0AFF\u0B01-\u0B03\u0B3C\u0B3E-\u0B44\u0B47\u0B48\u0B4B-\u0B4D\u0B56\u0B57\u0B62\u0B63\u0B82\u0BBE-\u0BC2\u0BC6-\u0BC8\u0BCA-\u0BCD\u0BD7\u0C00-\u0C04\u0C3E-\u0C44\u0C46-\u0C48\u0C4A-\u0C4D\u0C55\u0C56\u0C62\u0C63\u0C81-\u0C83\u0CBC\u0CBE-\u0CC4\u0CC6-\u0CC8\u0CCA-\u0CCD\u0CD5\u0CD6\u0CE2\u0CE3\u0D00-\u0D03\u0D3B\u0D3C\u0D3E-\u0D44\u0D46-\u0D48\u0D4A-\u0D4D\u0D57\u0D62\u0D63\u0D82\u0D83\u0DCA\u0DCF-\u0DD4\u0DD6\u0DD8-\u0DDF\u0DF2\u0DF3\u0E31\u0E34-\u0E3A\u0E47-\u0E4E\u0EB1\u0EB4-\u0EB9\u0EBB\u0EBC\u0EC8-\u0ECD\u0F18\u0F19\u0F35\u0F37\u0F39\u0F3E\u0F3F\u0F71-\u0F84\u0F86\u0F87\u0F8D-\u0F97\u0F99-\u0FBC\u0FC6\u102B-\u103E\u1056-\u1059\u105E-\u1060\u1062-\u1064\u1067-\u106D\u1071-\u1074\u1082-\u108D\u108F\u109A-\u109D\u135D-\u135F\u1712-\u1714\u1732-\u1734\u1752\u1753\u1772\u1773\u17B4-\u17D3\u17DD\u180B-\u180D\u1885\u1886\u18A9\u1920-\u192B\u1930-\u193B\u1A17-\u1A1B\u1A55-\u1A5E\u1A60-\u1A7C\u1A7F\u1AB0-\u1ABE\u1B00-\u1B04\u1B34-\u1B44\u1B6B-\u1B73\u1B80-\u1B82\u1BA1-\u1BAD\u1BE6-\u1BF3\u1C24-\u1C37\u1CD0-\u1CD2\u1CD4-\u1CE8\u1CED\u1CF2-\u1CF4\u1CF7-\u1CF9\u1DC0-\u1DF9\u1DFB-\u1DFF\u20D0-\u20F0\u2CEF-\u2CF1\u2D7F\u2DE0-\u2DFF\u302A-\u302F\u3099\u309A\uA66F-\uA672\uA674-\uA67D\uA69E\uA69F\uA6F0\uA6F1\uA802\uA806\uA80B\uA823-\uA827\uA880\uA881\uA8B4-\uA8C5\uA8E0-\uA8F1\uA8FF\uA926-\uA92D\uA947-\uA953\uA980-\uA983\uA9B3-\uA9C0\uA9E5\uAA29-\uAA36\uAA43\uAA4C\uAA4D\uAA7B-\uAA7D\uAAB0\uAAB2-\uAAB4\uAAB7\uAAB8\uAABE\uAABF\uAAC1\uAAEB-\uAAEF\uAAF5\uAAF6\uABE3-\uABEA\uABEC\uABED\uFB1E\uFE00-\uFE0F\uFE20-\uFE2F]/g, "") : (str) => str;
var BitapSearch = class {
	constructor(pattern, { location = Config.location, threshold = Config.threshold, distance = Config.distance, includeMatches = Config.includeMatches, findAllMatches = Config.findAllMatches, minMatchCharLength = Config.minMatchCharLength, isCaseSensitive = Config.isCaseSensitive, ignoreDiacritics = Config.ignoreDiacritics, ignoreLocation = Config.ignoreLocation } = {}) {
		this.options = {
			location,
			threshold,
			distance,
			includeMatches,
			findAllMatches,
			minMatchCharLength,
			isCaseSensitive,
			ignoreDiacritics,
			ignoreLocation
		};
		pattern = isCaseSensitive ? pattern : pattern.toLowerCase();
		pattern = ignoreDiacritics ? stripDiacritics(pattern) : pattern;
		this.pattern = pattern;
		this.chunks = [];
		if (!this.pattern.length) return;
		const addChunk = (pattern$1, startIndex) => {
			this.chunks.push({
				pattern: pattern$1,
				alphabet: createPatternAlphabet(pattern$1),
				startIndex
			});
		};
		const len = this.pattern.length;
		if (len > MAX_BITS) {
			let i = 0;
			const remainder = len % MAX_BITS;
			const end = len - remainder;
			while (i < end) {
				addChunk(this.pattern.substr(i, MAX_BITS), i);
				i += MAX_BITS;
			}
			if (remainder) {
				const startIndex = len - MAX_BITS;
				addChunk(this.pattern.substr(startIndex), startIndex);
			}
		} else addChunk(this.pattern, 0);
	}
	searchIn(text) {
		const { isCaseSensitive, ignoreDiacritics, includeMatches } = this.options;
		text = isCaseSensitive ? text : text.toLowerCase();
		text = ignoreDiacritics ? stripDiacritics(text) : text;
		if (this.pattern === text) {
			let result$1 = {
				isMatch: true,
				score: 0
			};
			if (includeMatches) result$1.indices = [[0, text.length - 1]];
			return result$1;
		}
		const { location, distance, threshold, findAllMatches, minMatchCharLength, ignoreLocation } = this.options;
		let allIndices = [];
		let totalScore = 0;
		let hasMatches = false;
		this.chunks.forEach(({ pattern, alphabet, startIndex }) => {
			const { isMatch, score, indices } = search(text, pattern, alphabet, {
				location: location + startIndex,
				distance,
				threshold,
				findAllMatches,
				minMatchCharLength,
				includeMatches,
				ignoreLocation
			});
			if (isMatch) hasMatches = true;
			totalScore += score;
			if (isMatch && indices) allIndices = [...allIndices, ...indices];
		});
		let result = {
			isMatch: hasMatches,
			score: hasMatches ? totalScore / this.chunks.length : 1
		};
		if (hasMatches && includeMatches) result.indices = allIndices;
		return result;
	}
};
var BaseMatch = class {
	constructor(pattern) {
		this.pattern = pattern;
	}
	static isMultiMatch(pattern) {
		return getMatch(pattern, this.multiRegex);
	}
	static isSingleMatch(pattern) {
		return getMatch(pattern, this.singleRegex);
	}
	search() {}
};
function getMatch(pattern, exp) {
	const matches = pattern.match(exp);
	return matches ? matches[1] : null;
}
var ExactMatch = class extends BaseMatch {
	constructor(pattern) {
		super(pattern);
	}
	static get type() {
		return "exact";
	}
	static get multiRegex() {
		return /^="(.*)"$/;
	}
	static get singleRegex() {
		return /^=(.*)$/;
	}
	search(text) {
		const isMatch = text === this.pattern;
		return {
			isMatch,
			score: isMatch ? 0 : 1,
			indices: [0, this.pattern.length - 1]
		};
	}
};
var InverseExactMatch = class extends BaseMatch {
	constructor(pattern) {
		super(pattern);
	}
	static get type() {
		return "inverse-exact";
	}
	static get multiRegex() {
		return /^!"(.*)"$/;
	}
	static get singleRegex() {
		return /^!(.*)$/;
	}
	search(text) {
		const index = text.indexOf(this.pattern);
		const isMatch = index === -1;
		return {
			isMatch,
			score: isMatch ? 0 : 1,
			indices: [0, text.length - 1]
		};
	}
};
var PrefixExactMatch = class extends BaseMatch {
	constructor(pattern) {
		super(pattern);
	}
	static get type() {
		return "prefix-exact";
	}
	static get multiRegex() {
		return /^\^"(.*)"$/;
	}
	static get singleRegex() {
		return /^\^(.*)$/;
	}
	search(text) {
		const isMatch = text.startsWith(this.pattern);
		return {
			isMatch,
			score: isMatch ? 0 : 1,
			indices: [0, this.pattern.length - 1]
		};
	}
};
var InversePrefixExactMatch = class extends BaseMatch {
	constructor(pattern) {
		super(pattern);
	}
	static get type() {
		return "inverse-prefix-exact";
	}
	static get multiRegex() {
		return /^!\^"(.*)"$/;
	}
	static get singleRegex() {
		return /^!\^(.*)$/;
	}
	search(text) {
		const isMatch = !text.startsWith(this.pattern);
		return {
			isMatch,
			score: isMatch ? 0 : 1,
			indices: [0, text.length - 1]
		};
	}
};
var SuffixExactMatch = class extends BaseMatch {
	constructor(pattern) {
		super(pattern);
	}
	static get type() {
		return "suffix-exact";
	}
	static get multiRegex() {
		return /^"(.*)"\$$/;
	}
	static get singleRegex() {
		return /^(.*)\$$/;
	}
	search(text) {
		const isMatch = text.endsWith(this.pattern);
		return {
			isMatch,
			score: isMatch ? 0 : 1,
			indices: [text.length - this.pattern.length, text.length - 1]
		};
	}
};
var InverseSuffixExactMatch = class extends BaseMatch {
	constructor(pattern) {
		super(pattern);
	}
	static get type() {
		return "inverse-suffix-exact";
	}
	static get multiRegex() {
		return /^!"(.*)"\$$/;
	}
	static get singleRegex() {
		return /^!(.*)\$$/;
	}
	search(text) {
		const isMatch = !text.endsWith(this.pattern);
		return {
			isMatch,
			score: isMatch ? 0 : 1,
			indices: [0, text.length - 1]
		};
	}
};
var FuzzyMatch = class extends BaseMatch {
	constructor(pattern, { location = Config.location, threshold = Config.threshold, distance = Config.distance, includeMatches = Config.includeMatches, findAllMatches = Config.findAllMatches, minMatchCharLength = Config.minMatchCharLength, isCaseSensitive = Config.isCaseSensitive, ignoreDiacritics = Config.ignoreDiacritics, ignoreLocation = Config.ignoreLocation } = {}) {
		super(pattern);
		this._bitapSearch = new BitapSearch(pattern, {
			location,
			threshold,
			distance,
			includeMatches,
			findAllMatches,
			minMatchCharLength,
			isCaseSensitive,
			ignoreDiacritics,
			ignoreLocation
		});
	}
	static get type() {
		return "fuzzy";
	}
	static get multiRegex() {
		return /^"(.*)"$/;
	}
	static get singleRegex() {
		return /^(.*)$/;
	}
	search(text) {
		return this._bitapSearch.searchIn(text);
	}
};
var IncludeMatch = class extends BaseMatch {
	constructor(pattern) {
		super(pattern);
	}
	static get type() {
		return "include";
	}
	static get multiRegex() {
		return /^'"(.*)"$/;
	}
	static get singleRegex() {
		return /^'(.*)$/;
	}
	search(text) {
		let location = 0;
		let index;
		const indices = [];
		const patternLen = this.pattern.length;
		while ((index = text.indexOf(this.pattern, location)) > -1) {
			location = index + patternLen;
			indices.push([index, location - 1]);
		}
		const isMatch = !!indices.length;
		return {
			isMatch,
			score: isMatch ? 0 : 1,
			indices
		};
	}
};
const searchers = [
	ExactMatch,
	IncludeMatch,
	PrefixExactMatch,
	InversePrefixExactMatch,
	InverseSuffixExactMatch,
	SuffixExactMatch,
	InverseExactMatch,
	FuzzyMatch
];
const searchersLen = searchers.length;
const SPACE_RE = / +(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)/;
const OR_TOKEN = "|";
function parseQuery(pattern, options = {}) {
	return pattern.split(OR_TOKEN).map((item) => {
		let query = item.trim().split(SPACE_RE).filter((item$1) => item$1 && !!item$1.trim());
		let results = [];
		for (let i = 0, len = query.length; i < len; i += 1) {
			const queryItem = query[i];
			let found = false;
			let idx = -1;
			while (!found && ++idx < searchersLen) {
				const searcher = searchers[idx];
				let token = searcher.isMultiMatch(queryItem);
				if (token) {
					results.push(new searcher(token, options));
					found = true;
				}
			}
			if (found) continue;
			idx = -1;
			while (++idx < searchersLen) {
				const searcher = searchers[idx];
				let token = searcher.isSingleMatch(queryItem);
				if (token) {
					results.push(new searcher(token, options));
					break;
				}
			}
		}
		return results;
	});
}
const MultiMatchSet = new Set([FuzzyMatch.type, IncludeMatch.type]);
var ExtendedSearch = class {
	constructor(pattern, { isCaseSensitive = Config.isCaseSensitive, ignoreDiacritics = Config.ignoreDiacritics, includeMatches = Config.includeMatches, minMatchCharLength = Config.minMatchCharLength, ignoreLocation = Config.ignoreLocation, findAllMatches = Config.findAllMatches, location = Config.location, threshold = Config.threshold, distance = Config.distance } = {}) {
		this.query = null;
		this.options = {
			isCaseSensitive,
			ignoreDiacritics,
			includeMatches,
			minMatchCharLength,
			findAllMatches,
			ignoreLocation,
			location,
			threshold,
			distance
		};
		pattern = isCaseSensitive ? pattern : pattern.toLowerCase();
		pattern = ignoreDiacritics ? stripDiacritics(pattern) : pattern;
		this.pattern = pattern;
		this.query = parseQuery(this.pattern, this.options);
	}
	static condition(_, options) {
		return options.useExtendedSearch;
	}
	searchIn(text) {
		const query = this.query;
		if (!query) return {
			isMatch: false,
			score: 1
		};
		const { includeMatches, isCaseSensitive, ignoreDiacritics } = this.options;
		text = isCaseSensitive ? text : text.toLowerCase();
		text = ignoreDiacritics ? stripDiacritics(text) : text;
		let numMatches = 0;
		let allIndices = [];
		let totalScore = 0;
		for (let i = 0, qLen = query.length; i < qLen; i += 1) {
			const searchers$1 = query[i];
			allIndices.length = 0;
			numMatches = 0;
			for (let j = 0, pLen = searchers$1.length; j < pLen; j += 1) {
				const searcher = searchers$1[j];
				const { isMatch, indices, score } = searcher.search(text);
				if (isMatch) {
					numMatches += 1;
					totalScore += score;
					if (includeMatches) {
						const type = searcher.constructor.type;
						if (MultiMatchSet.has(type)) allIndices = [...allIndices, ...indices];
						else allIndices.push(indices);
					}
				} else {
					totalScore = 0;
					numMatches = 0;
					allIndices.length = 0;
					break;
				}
			}
			if (numMatches) {
				let result = {
					isMatch: true,
					score: totalScore / numMatches
				};
				if (includeMatches) result.indices = allIndices;
				return result;
			}
		}
		return {
			isMatch: false,
			score: 1
		};
	}
};
const registeredSearchers = [];
function register(...args) {
	registeredSearchers.push(...args);
}
function createSearcher(pattern, options) {
	for (let i = 0, len = registeredSearchers.length; i < len; i += 1) {
		let searcherClass = registeredSearchers[i];
		if (searcherClass.condition(pattern, options)) return new searcherClass(pattern, options);
	}
	return new BitapSearch(pattern, options);
}
const LogicalOperator = {
	AND: "$and",
	OR: "$or"
};
const KeyType = {
	PATH: "$path",
	PATTERN: "$val"
};
const isExpression = (query) => !!(query[LogicalOperator.AND] || query[LogicalOperator.OR]);
const isPath = (query) => !!query[KeyType.PATH];
const isLeaf = (query) => !isArray(query) && isObject(query) && !isExpression(query);
const convertToExplicit = (query) => ({ [LogicalOperator.AND]: Object.keys(query).map((key) => ({ [key]: query[key] })) });
function parse(query, options, { auto = true } = {}) {
	const next = (query$1) => {
		let keys = Object.keys(query$1);
		const isQueryPath = isPath(query$1);
		if (!isQueryPath && keys.length > 1 && !isExpression(query$1)) return next(convertToExplicit(query$1));
		if (isLeaf(query$1)) {
			const key = isQueryPath ? query$1[KeyType.PATH] : keys[0];
			const pattern = isQueryPath ? query$1[KeyType.PATTERN] : query$1[key];
			if (!isString(pattern)) throw new Error(LOGICAL_SEARCH_INVALID_QUERY_FOR_KEY(key));
			const obj = {
				keyId: createKeyId(key),
				pattern
			};
			if (auto) obj.searcher = createSearcher(pattern, options);
			return obj;
		}
		let node = {
			children: [],
			operator: keys[0]
		};
		keys.forEach((key) => {
			const value = query$1[key];
			if (isArray(value)) value.forEach((item) => {
				node.children.push(next(item));
			});
		});
		return node;
	};
	if (!isExpression(query)) query = convertToExplicit(query);
	return next(query);
}
function computeScore(results, { ignoreFieldNorm = Config.ignoreFieldNorm }) {
	results.forEach((result) => {
		let totalScore = 1;
		result.matches.forEach(({ key, norm: norm$1, score }) => {
			const weight = key ? key.weight : null;
			totalScore *= Math.pow(score === 0 && weight ? Number.EPSILON : score, (weight || 1) * (ignoreFieldNorm ? 1 : norm$1));
		});
		result.score = totalScore;
	});
}
function transformMatches(result, data) {
	const matches = result.matches;
	data.matches = [];
	if (!isDefined(matches)) return;
	matches.forEach((match) => {
		if (!isDefined(match.indices) || !match.indices.length) return;
		const { indices, value } = match;
		let obj = {
			indices,
			value
		};
		if (match.key) obj.key = match.key.src;
		if (match.idx > -1) obj.refIndex = match.idx;
		data.matches.push(obj);
	});
}
function transformScore(result, data) {
	data.score = result.score;
}
function format(results, docs, { includeMatches = Config.includeMatches, includeScore = Config.includeScore } = {}) {
	const transformers = [];
	if (includeMatches) transformers.push(transformMatches);
	if (includeScore) transformers.push(transformScore);
	return results.map((result) => {
		const { idx } = result;
		const data = {
			item: docs[idx],
			refIndex: idx
		};
		if (transformers.length) transformers.forEach((transformer) => {
			transformer(result, data);
		});
		return data;
	});
}
var Fuse = class {
	constructor(docs, options = {}, index) {
		this.options = {
			...Config,
			...options
		};
		if (this.options.useExtendedSearch && false);
		this._keyStore = new KeyStore(this.options.keys);
		this.setCollection(docs, index);
	}
	setCollection(docs, index) {
		this._docs = docs;
		if (index && !(index instanceof FuseIndex)) throw new Error(INCORRECT_INDEX_TYPE);
		this._myIndex = index || createIndex(this.options.keys, this._docs, {
			getFn: this.options.getFn,
			fieldNormWeight: this.options.fieldNormWeight
		});
	}
	add(doc) {
		if (!isDefined(doc)) return;
		this._docs.push(doc);
		this._myIndex.add(doc);
	}
	remove(predicate = () => false) {
		const results = [];
		for (let i = 0, len = this._docs.length; i < len; i += 1) {
			const doc = this._docs[i];
			if (predicate(doc, i)) {
				this.removeAt(i);
				i -= 1;
				len -= 1;
				results.push(doc);
			}
		}
		return results;
	}
	removeAt(idx) {
		this._docs.splice(idx, 1);
		this._myIndex.removeAt(idx);
	}
	getIndex() {
		return this._myIndex;
	}
	search(query, { limit = -1 } = {}) {
		const { includeMatches, includeScore, shouldSort, sortFn, ignoreFieldNorm } = this.options;
		let results = isString(query) ? isString(this._docs[0]) ? this._searchStringList(query) : this._searchObjectList(query) : this._searchLogical(query);
		computeScore(results, { ignoreFieldNorm });
		if (shouldSort) results.sort(sortFn);
		if (isNumber(limit) && limit > -1) results = results.slice(0, limit);
		return format(results, this._docs, {
			includeMatches,
			includeScore
		});
	}
	_searchStringList(query) {
		const searcher = createSearcher(query, this.options);
		const { records } = this._myIndex;
		const results = [];
		records.forEach(({ v: text, i: idx, n: norm$1 }) => {
			if (!isDefined(text)) return;
			const { isMatch, score, indices } = searcher.searchIn(text);
			if (isMatch) results.push({
				item: text,
				idx,
				matches: [{
					score,
					value: text,
					norm: norm$1,
					indices
				}]
			});
		});
		return results;
	}
	_searchLogical(query) {
		const expression = parse(query, this.options);
		const evaluate = (node, item, idx) => {
			if (!node.children) {
				const { keyId, searcher } = node;
				const matches = this._findMatches({
					key: this._keyStore.get(keyId),
					value: this._myIndex.getValueForItemAtKeyId(item, keyId),
					searcher
				});
				if (matches && matches.length) return [{
					idx,
					item,
					matches
				}];
				return [];
			}
			const res = [];
			for (let i = 0, len = node.children.length; i < len; i += 1) {
				const child = node.children[i];
				const result = evaluate(child, item, idx);
				if (result.length) res.push(...result);
				else if (node.operator === LogicalOperator.AND) return [];
			}
			return res;
		};
		const records = this._myIndex.records;
		const resultMap = {};
		const results = [];
		records.forEach(({ $: item, i: idx }) => {
			if (isDefined(item)) {
				let expResults = evaluate(expression, item, idx);
				if (expResults.length) {
					if (!resultMap[idx]) {
						resultMap[idx] = {
							idx,
							item,
							matches: []
						};
						results.push(resultMap[idx]);
					}
					expResults.forEach(({ matches }) => {
						resultMap[idx].matches.push(...matches);
					});
				}
			}
		});
		return results;
	}
	_searchObjectList(query) {
		const searcher = createSearcher(query, this.options);
		const { keys, records } = this._myIndex;
		const results = [];
		records.forEach(({ $: item, i: idx }) => {
			if (!isDefined(item)) return;
			let matches = [];
			keys.forEach((key, keyIndex) => {
				matches.push(...this._findMatches({
					key,
					value: item[keyIndex],
					searcher
				}));
			});
			if (matches.length) results.push({
				idx,
				item,
				matches
			});
		});
		return results;
	}
	_findMatches({ key, value, searcher }) {
		if (!isDefined(value)) return [];
		let matches = [];
		if (isArray(value)) value.forEach(({ v: text, i: idx, n: norm$1 }) => {
			if (!isDefined(text)) return;
			const { isMatch, score, indices } = searcher.searchIn(text);
			if (isMatch) matches.push({
				score,
				key,
				value: text,
				idx,
				norm: norm$1,
				indices
			});
		});
		else {
			const { v: text, n: norm$1 } = value;
			const { isMatch, score, indices } = searcher.searchIn(text);
			if (isMatch) matches.push({
				score,
				key,
				value: text,
				norm: norm$1,
				indices
			});
		}
		return matches;
	}
};
Fuse.version = "7.1.0";
Fuse.createIndex = createIndex;
Fuse.parseIndex = parseIndex;
Fuse.config = Config;
Fuse.parseQuery = parse;
register(ExtendedSearch);
const useSearchResults = defineStore("search", () => {
	const state = useOptionsStore();
	const data = usePayloadStore();
	const filtered = computed(() => {
		let modules = data.modules || [];
		if (!state.search.includeUnreached) modules = modules.filter((item) => item.sourceSize);
		if (!state.search.includeNodeModules) modules = modules.filter((item) => !item.id.includes("/node_modules/"));
		if (!state.search.includeVirtual) modules = modules.filter((item) => !item.virtual);
		return modules;
	});
	const results = computed(() => {
		const modules = filtered.value;
		if (!state.search.text) return modules;
		if (state.search.exactSearch) return modules.filter((item) => item.id.includes(state.search.text) || item.plugins.some((plugin) => plugin.name.includes(state.search.text)));
		else {
			const fuse = new Fuse(modules, {
				shouldSort: true,
				keys: ["id", "plugins"]
			});
			return fuse.search(state.search.text).map((i) => i.item);
		}
	});
	const resultsSorted = computed(() => {
		if (state.search.text) return results.value;
		const cloned = [...results.value];
		if (state.view.sort === "time-asc") cloned.sort((a, b) => b.totalTime - a.totalTime);
		if (state.view.sort === "time-desc") cloned.sort((a, b) => a.totalTime - b.totalTime);
		return cloned;
	});
	return {
		results,
		resultsSorted,
		filtered
	};
});
export { useSearchResults };
