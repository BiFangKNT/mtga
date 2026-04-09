//#region rolldown:runtime
var __defProp = Object.defineProperty;
var __exportAll = (all, symbols) => {
	let target = {};
	for (var name$2 in all) {
		__defProp(target, name$2, {
			get: all[name$2],
			enumerable: true
		});
	}
	if (symbols) {
		__defProp(target, Symbol.toStringTag, { value: "Module" });
	}
	return target;
};

//#endregion
//#region src/token-store/token-store.ts
/**
* Binary search for the index of the first token that is after the given location.
*/
function search(tokens, location) {
	let minIndex = 0;
	let maxIndex = tokens.length - 1;
	while (minIndex <= maxIndex) {
		const index = Math.floor((minIndex + maxIndex) / 2);
		const tokenStartLocation = tokens[index].range[0];
		if (tokenStartLocation < location) minIndex = index + 1;
		else if (tokenStartLocation > location) maxIndex = index - 1;
		else return index;
	}
	return minIndex;
}
/**
* Get the index of the first token that is after the given location.
*/
function getFirstIndex(tokens, indexMap, startLoc) {
	let index = indexMap.get(startLoc);
	if (index == null) index = search(tokens, startLoc);
	while (index < tokens.length && tokens[index].range[1] <= tokens[index].range[0]) index++;
	return index;
}
/**
* Get the index of the last token that is before the given location.
*/
function getLastIndex(tokens, indexMap, endLoc) {
	let index = indexMap.get(endLoc);
	if (index != null) index--;
	else index = search(tokens, endLoc) - 1;
	while (index >= 0 && tokens[index].range[1] <= tokens[index].range[0]) index--;
	return index;
}
/**
* Normalizes the options for cursor methods.
*/
function normalizeSkipOptions(options, ctx) {
	if (typeof options === "number") return {
		filter: ctx.isNotComment,
		skip: options
	};
	if (typeof options === "function") return {
		filter: (n) => {
			if (ctx.isComment(n)) return false;
			return options(n);
		},
		skip: 0
	};
	let filter;
	if (options?.includeComments) filter = options?.filter ?? (() => true);
	else if (options?.filter) {
		const baseFilter = options?.filter;
		filter = (token) => {
			if (ctx.isComment(token)) return false;
			return baseFilter(token);
		};
	} else filter = ctx.isNotComment;
	return {
		filter,
		skip: options?.skip ?? 0
	};
}
/**
* Normalizes the options for cursor methods with count.
*/
function normalizeCountOptions(options, ctx) {
	if (typeof options === "number") return {
		filter: ctx.isNotComment,
		count: options
	};
	if (typeof options === "function") return {
		filter: (n) => {
			if (ctx.isComment(n)) return false;
			return options(n);
		},
		count: 0
	};
	let filter;
	if (options?.includeComments) filter = options?.filter ?? (() => true);
	else if (options?.filter) {
		const baseFilter = options?.filter;
		filter = (token) => {
			if (ctx.isComment(token)) return false;
			return baseFilter(token);
		};
	} else filter = ctx.isNotComment;
	return {
		filter,
		count: options?.count ?? 0
	};
}
const PRIVATE = Symbol("private");
var TokenStore = class {
	[PRIVATE];
	constructor(params) {
		const allTokens = [...params.tokens].sort((a, b) => a.range[0] - b.range[0]);
		const tokenStartToIndex = /* @__PURE__ */ new Map();
		for (let i = 0; i < allTokens.length; i++) {
			const token = allTokens[i];
			if (token.range[0] < token.range[1]) tokenStartToIndex.set(token.range[0], i);
		}
		this[PRIVATE] = {
			allTokens,
			tokenStartToIndex,
			ctx: {
				isComment: params.isComment,
				isNotComment: (token) => !params.isComment(token)
			},
			cacheAllComments: null
		};
	}
	/**
	* Gets all tokens, including comments.
	*/
	getAllTokens() {
		return this[PRIVATE].allTokens;
	}
	/**
	* Gets all comments.
	*/
	getAllComments() {
		const { ctx, allTokens, cacheAllComments } = this[PRIVATE];
		if (cacheAllComments) return cacheAllComments;
		const result = [];
		for (const token of allTokens) if (ctx.isComment(token)) result.push(token);
		this[PRIVATE].cacheAllComments = result;
		return result;
	}
	getFirstToken(node, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, skip } = normalizeSkipOptions(options, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, node.range[0]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, node.range[1]);
		let skipped = 0;
		for (let i = startIndex; i <= endIndex && i < allTokens.length; i++) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			if (skipped < skip) {
				skipped++;
				continue;
			}
			return token;
		}
		return null;
	}
	getFirstTokens(node, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, count } = normalizeCountOptions(options, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, node.range[0]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, node.range[1]);
		const result = [];
		for (let i = startIndex; i <= endIndex && i < allTokens.length; i++) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			result.push(token);
			if (count > 0 && result.length >= count) break;
		}
		return result;
	}
	getLastToken(node, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, skip } = normalizeSkipOptions(options, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, node.range[0]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, node.range[1]);
		let skipped = 0;
		for (let i = endIndex; i >= startIndex && i >= 0; i--) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			if (skipped < skip) {
				skipped++;
				continue;
			}
			return token;
		}
		return null;
	}
	getLastTokens(node, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, count } = normalizeCountOptions(options, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, node.range[0]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, node.range[1]);
		const result = [];
		for (let i = endIndex; i >= startIndex && i >= 0; i--) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			result.unshift(token);
			if (count > 0 && result.length >= count) break;
		}
		return result;
	}
	/**
	* Gets the token that follows a given node or token.
	*/
	getTokenAfter(node, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, skip } = normalizeSkipOptions(options, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, node.range[1]);
		let skipped = 0;
		for (let i = startIndex; i < allTokens.length; i++) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			if (skipped < skip) {
				skipped++;
				continue;
			}
			return token;
		}
		return null;
	}
	getTokensAfter(node, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, count } = normalizeCountOptions(options, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, node.range[1]);
		const result = [];
		for (let i = startIndex; i < allTokens.length; i++) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			result.push(token);
			if (count > 0 && result.length >= count) break;
		}
		return result;
	}
	/**
	* Gets the token that precedes a given node or token.
	*/
	getTokenBefore(node, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, skip } = normalizeSkipOptions(options, ctx);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, node.range[0]);
		let skipped = 0;
		for (let i = endIndex; i >= 0; i--) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			if (skipped < skip) {
				skipped++;
				continue;
			}
			return token;
		}
		return null;
	}
	/**
	* Gets the `count` tokens that precedes a given node or token.
	*/
	getTokensBefore(node, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, count } = normalizeCountOptions(options, ctx);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, node.range[0]);
		const result = [];
		for (let i = endIndex; i >= 0; i--) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			result.unshift(token);
			if (count > 0 && result.length >= count) break;
		}
		return result;
	}
	getFirstTokenBetween(left, right, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, skip } = normalizeSkipOptions(options, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, left.range[1]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, right.range[0]);
		let skipped = 0;
		for (let i = startIndex; i <= endIndex && i < allTokens.length; i++) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			if (skipped < skip) {
				skipped++;
				continue;
			}
			return token;
		}
		return null;
	}
	getFirstTokensBetween(left, right, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, count } = normalizeCountOptions(options, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, left.range[1]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, right.range[0]);
		const result = [];
		for (let i = startIndex; i <= endIndex && i < allTokens.length; i++) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			result.push(token);
			if (count > 0 && result.length >= count) break;
		}
		return result;
	}
	getLastTokenBetween(left, right, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, skip } = normalizeSkipOptions(options, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, left.range[1]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, right.range[0]);
		let skipped = 0;
		for (let i = endIndex; i >= startIndex; i--) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			if (skipped < skip) {
				skipped++;
				continue;
			}
			return token;
		}
		return null;
	}
	getLastTokensBetween(left, right, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, count } = normalizeCountOptions(options, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, left.range[1]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, right.range[0]);
		const result = [];
		for (let i = endIndex; i >= startIndex; i--) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			result.unshift(token);
			if (count > 0 && result.length >= count) break;
		}
		return result;
	}
	/**
	* Gets all tokens that are related to the given node.
	*/
	getTokens(node, options) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, count } = normalizeCountOptions(options, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, node.range[0]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, node.range[1]);
		const result = [];
		for (let i = startIndex; i <= endIndex && i < allTokens.length; i++) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			result.push(token);
			if (count > 0 && result.length >= count) break;
		}
		return result;
	}
	/**
	* Gets all of the tokens between two non-overlapping nodes.
	*/
	getTokensBetween(left, right, paddingOrOptions) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const { filter, count } = normalizeCountOptions(paddingOrOptions, ctx);
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, left.range[1]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, right.range[0]);
		const result = [];
		for (let i = startIndex; i <= endIndex && i < allTokens.length; i++) {
			const token = allTokens[i];
			if (filter && !filter(token)) continue;
			result.push(token);
			if (count > 0 && result.length >= count) break;
		}
		return result;
	}
	/**
	* Gets all comment tokens inside the given node or token.
	*/
	getCommentsInside(nodeOrToken) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, nodeOrToken.range[0]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, nodeOrToken.range[1]);
		const result = [];
		for (let i = startIndex; i <= endIndex && i < allTokens.length; i++) {
			const token = allTokens[i];
			if (ctx.isComment(token)) result.push(token);
		}
		return result;
	}
	/**
	* Gets all comment tokens directly before the given node or token.
	*/
	getCommentsBefore(nodeOrToken) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, nodeOrToken.range[0]);
		const result = [];
		for (let i = endIndex; i >= 0; i--) {
			const token = allTokens[i];
			if (ctx.isComment(token)) result.unshift(token);
			else break;
		}
		return result;
	}
	/**
	* Gets all comment tokens directly after the given node or token.
	*/
	getCommentsAfter(nodeOrToken) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, nodeOrToken.range[1]);
		const result = [];
		for (let i = startIndex; i < allTokens.length; i++) {
			const token = allTokens[i];
			if (ctx.isComment(token)) result.push(token);
			else break;
		}
		return result;
	}
	/**
	* Checks if there are any comment tokens between two non-overlapping nodes.
	*/
	commentsExistBetween(left, right) {
		const { ctx, allTokens, tokenStartToIndex } = this[PRIVATE];
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, left.range[1]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, right.range[0]);
		for (let i = startIndex; i <= endIndex && i < allTokens.length; i++) {
			const token = allTokens[i];
			if (ctx.isComment(token)) return true;
		}
		return false;
	}
	/**
	* Checks if there is whitespace between two non-overlapping nodes.
	*/
	isSpaceBetween(left, right) {
		if (left.range[1] >= right.range[0]) return false;
		const { allTokens, tokenStartToIndex } = this[PRIVATE];
		const startIndex = getFirstIndex(allTokens, tokenStartToIndex, left.range[1]);
		const endIndex = getLastIndex(allTokens, tokenStartToIndex, right.range[0]);
		let prev = left;
		for (let i = startIndex; i <= endIndex && i < allTokens.length; i++) {
			const token = allTokens[i];
			if (prev.range[1] < token.range[0]) return true;
			prev = token;
		}
		return prev.range[1] < right.range[0];
	}
};

//#endregion
//#region package.json
var name$1 = "@ota-meshi/ast-token-store";
var version$1 = "0.3.0";

//#endregion
//#region src/meta.ts
var meta_exports = /* @__PURE__ */ __exportAll({
	name: () => name,
	version: () => version
});
const name = name$1;
const version = version$1;

//#endregion
//#region src/index.ts
const meta = { ...meta_exports };

//#endregion
export { TokenStore, meta };