import { t as __exportAll } from "./chunk-15K8U1wQ.mjs";
import { Composer, LineCounter, Parser, isAlias, isDocument, isMap, isPair, isScalar, isSeq, parseDocument } from "yaml";
import { unionWith } from "eslint-visitor-keys";

//#region src/utils.ts
/**
* Gets the static value for the given node.
*/
function getStaticYAMLValue(node) {
	return getValue(node, null);
}
/**
* Gets the static value for the given node with YAML version.
*/
function getValue(node, version$1) {
	return resolver[node.type](node, version$1);
}
const resolver = {
	Program(node) {
		return node.body.length === 0 ? null : node.body.length === 1 ? resolver.YAMLDocument(node.body[0]) : node.body.map((n) => resolver.YAMLDocument(n));
	},
	YAMLDocument(node) {
		return node.content ? getValue(node.content, node.version) : null;
	},
	YAMLMapping(node, version$1) {
		const result = {};
		for (const pair of node.pairs) Object.assign(result, getValue(pair, version$1));
		return result;
	},
	YAMLPair(node, version$1) {
		const result = {};
		let key = node.key ? getValue(node.key, version$1) : null;
		if (typeof key !== "string" && typeof key !== "number") key = String(key);
		result[key] = node.value ? getValue(node.value, version$1) : null;
		return result;
	},
	YAMLSequence(node, version$1) {
		const result = [];
		for (const entry of node.entries) result.push(entry ? getValue(entry, version$1) : null);
		return result;
	},
	YAMLScalar(node) {
		return node.value;
	},
	YAMLAlias(node, version$1) {
		const anchor = findAnchor(node);
		return anchor ? getValue(anchor.parent, version$1) : null;
	},
	YAMLWithMeta(node, version$1) {
		if (node.tag) {
			const value = node.value;
			if (value == null) return getTaggedValue(node.tag, "", "", version$1);
			if (value.type === "YAMLScalar") {
				if (value.style === "plain") return getTaggedValue(node.tag, value.strValue, value.strValue, version$1);
				if (value.style === "double-quoted" || value.style === "single-quoted") return getTaggedValue(node.tag, value.raw, value.strValue, version$1);
			}
			for (const tagResolver of tagNodeResolvers[version$1 || "1.2"]) if (tagResolver.tag === node.tag.tag && tagResolver.testNode(value)) return tagResolver.resolveNode(value);
		}
		if (node.value == null) return null;
		return getValue(node.value, version$1);
	}
};
/**
* Find Anchor
*/
function findAnchor(node) {
	let p = node.parent;
	let doc = null;
	while (p) {
		if (p.type === "YAMLDocument") {
			doc = p;
			break;
		}
		p = p.parent;
	}
	const anchors = doc.anchors[node.name];
	if (!anchors) return null;
	let target = {
		anchor: null,
		distance: Infinity
	};
	for (const anchor of anchors) if (anchor.range[0] < node.range[0]) {
		const distance = node.range[0] - anchor.range[0];
		if (target.distance >= distance) target = {
			anchor,
			distance
		};
	}
	return target.anchor;
}
/**
* Get tagged value
*/
function getTaggedValue(tag, text, str, version$1) {
	for (const tagResolver of tagResolvers[version$1 || "1.2"]) if (tagResolver.tag === tag.tag && tagResolver.testString(str)) return tagResolver.resolveString(str);
	const tagText = tag.tag.startsWith("!") ? tag.tag : `!<${tag.tag}>`;
	return parseDocument(`${version$1 ? `%YAML ${version$1}` : ""}
---
${tagText} ${text}`).toJSON();
}

//#endregion
//#region src/tags/omap.ts
const OMAP = {
	tag: "tag:yaml.org,2002:omap",
	testNode(node) {
		return node.type === "YAMLSequence" && node.entries.every((e) => e?.type === "YAMLMapping" && e.pairs.length === 1);
	},
	resolveNode(node) {
		const seq = node;
		const result = {};
		for (const e of seq.entries) {
			const map = e;
			for (const p of map.pairs) {
				const key = p.key ? getStaticYAMLValue(p.key) : p.key;
				result[key] = p.value ? getStaticYAMLValue(p.value) : p.value;
			}
		}
		return result;
	}
};

//#endregion
//#region src/tags/set.ts
const SET = {
	tag: "tag:yaml.org,2002:set",
	testNode(node) {
		return node.type === "YAMLMapping" && node.pairs.every((p) => p.key != null && p.value == null);
	},
	resolveNode(node) {
		const map = node;
		const result = [];
		for (const p of map.pairs) result.push(getStaticYAMLValue(p.key));
		return result;
	}
};

//#endregion
//#region src/tags/tags1.2.ts
const NULL$1 = {
	tag: "tag:yaml.org,2002:null",
	testString(str) {
		return !str || str === "null" || str === "Null" || str === "NULL" || str === "~";
	},
	resolveString() {
		return null;
	}
};
const TRUE$1 = {
	tag: "tag:yaml.org,2002:bool",
	testString(str) {
		return str === "true" || str === "True" || str === "TRUE";
	},
	resolveString() {
		return true;
	}
};
const FALSE$1 = {
	tag: "tag:yaml.org,2002:bool",
	testString(str) {
		return str === "false" || str === "False" || str === "FALSE";
	},
	resolveString() {
		return false;
	}
};
const INT$1 = {
	tag: "tag:yaml.org,2002:int",
	testString(str) {
		return /^[+-]?\d+$/u.test(str);
	},
	resolveString(str) {
		return parseInt(str, 10);
	}
};
const INT_BASE8$1 = {
	tag: "tag:yaml.org,2002:int",
	testString(str) {
		return /^0o[0-7]+$/u.test(str);
	},
	resolveString(str) {
		return parseInt(str.slice(2), 8);
	}
};
const INT_BASE16$1 = {
	tag: "tag:yaml.org,2002:int",
	testString(str) {
		return /^0x[\dA-Fa-f]+$/u.test(str);
	},
	resolveString(str) {
		return parseInt(str.slice(2), 16);
	}
};
const FLOAT$1 = {
	tag: "tag:yaml.org,2002:float",
	testString(str) {
		return /^[+-]?(?:\.\d+|\d+(?:\.\d*)?)(?:e[+-]?\d+)?$/iu.test(str);
	},
	resolveString(str) {
		return parseFloat(str);
	}
};
const INFINITY$1 = {
	tag: "tag:yaml.org,2002:float",
	testString(str) {
		return /^[+-]?(?:\.inf|\.Inf|\.INF)$/u.test(str);
	},
	resolveString(str) {
		return str.startsWith("-") ? -Infinity : Infinity;
	}
};
const NAN$1 = {
	tag: "tag:yaml.org,2002:float",
	testString(str) {
		return str === ".NaN" || str === ".nan" || str === ".NAN";
	},
	resolveString() {
		return NaN;
	}
};
const STR$1 = {
	tag: "tag:yaml.org,2002:str",
	testString() {
		return true;
	},
	resolveString(str) {
		return str;
	}
};
const tagResolvers$2 = [
	NULL$1,
	TRUE$1,
	FALSE$1,
	INT$1,
	INT_BASE8$1,
	INT_BASE16$1,
	FLOAT$1,
	INFINITY$1,
	NAN$1,
	STR$1
];
const tagNodeResolvers$2 = [OMAP, SET];

//#endregion
//#region src/tags/tags1.1.ts
const NULL = NULL$1;
const TRUE = {
	tag: "tag:yaml.org,2002:bool",
	testString(str) {
		return /^(?:y|Y|yes|Yes|YES|true|True|TRUE|on|On|ON)$/u.test(str);
	},
	resolveString() {
		return true;
	}
};
const FALSE = {
	tag: "tag:yaml.org,2002:bool",
	testString(str) {
		return /^(?:n|N|no|No|NO|false|False|FALSE|off|Off|OFF)$/u.test(str);
	},
	resolveString() {
		return false;
	}
};
const INT = {
	tag: "tag:yaml.org,2002:int",
	testString(str) {
		return /^[+-]?(?:0|[1-9][\d_]*)$/u.test(str);
	},
	resolveString(str) {
		return resolveInt(str, 0, 10);
	}
};
const INT_BASE2 = {
	tag: "tag:yaml.org,2002:int",
	testString(str) {
		return /^[+-]?0b[01_]+$/u.test(str);
	},
	resolveString(str) {
		return resolveInt(str, 2, 2);
	}
};
const INT_BASE8 = {
	tag: "tag:yaml.org,2002:int",
	testString(str) {
		return /^[+-]?0[0-7_]+$/u.test(str);
	},
	resolveString(str) {
		return resolveInt(str, 1, 8);
	}
};
const INT_BASE16 = {
	tag: "tag:yaml.org,2002:int",
	testString(str) {
		return /^[+-]?0x[\dA-F_a-f]+$/u.test(str);
	},
	resolveString(str) {
		return resolveInt(str, 2, 16);
	}
};
const INT_BASE60 = {
	tag: "tag:yaml.org,2002:int",
	testString(str) {
		return /^[+-]?[1-9][\d_]*(?::[0-5]?\d)+$/u.test(str);
	},
	resolveString(str) {
		return resolveBase60(str.split(/:/u), true);
	}
};
const FLOAT = {
	tag: "tag:yaml.org,2002:float",
	testString(str) {
		return /^[+-]?(?:\d[\d_]*)?\.[\d_]*(?:e[+-]?\d+)?$/iu.test(str) || /^[+-]?(?:\d[\d_]*)?(?:e[+-]?\d+)?$/iu.test(str);
	},
	resolveString(str) {
		return parseFloat(str.replace(/_/gu, ""));
	}
};
const FLOAT_BASE60 = {
	tag: "tag:yaml.org,2002:float",
	testString(str) {
		return /^[+-]?\d[\d_]*(?::[0-5]?\d)+\.[\d_]*$/u.test(str);
	},
	resolveString(str) {
		return resolveBase60(str.split(/:/u), false);
	}
};
const INFINITY = INFINITY$1;
const NAN = NAN$1;
const STR = STR$1;
const tagResolvers$1 = [
	NULL,
	TRUE,
	FALSE,
	INT_BASE8,
	INT,
	INT_BASE2,
	INT_BASE16,
	INT_BASE60,
	FLOAT,
	FLOAT_BASE60,
	INFINITY,
	NAN,
	STR
];
const tagNodeResolvers$1 = [OMAP, SET];
/**
* Resolve int value
*/
function resolveInt(value, skip, radix) {
	if (value.startsWith("-") || value.startsWith("+")) return parseInt(value[0] + value.slice(skip + 1).replace(/_/gu, ""), radix);
	return parseInt(value.slice(skip).replace(/_/gu, ""), radix);
}
/**
* Resolve base 60 number value
*/
function resolveBase60(values, isInt) {
	let first = values.shift().replace(/_/gu, "");
	const last = values.pop().replace(/_/gu, "");
	let minus = false;
	if (first.startsWith("-") || first.startsWith("+")) {
		minus = first.startsWith("-");
		first = first.slice(1);
	}
	let value = parseInt(first, 10);
	while (values.length) {
		value *= 60;
		value += parseInt(values.shift().replace(/_/gu, ""), 10);
	}
	value *= 60;
	value += isInt ? parseInt(last, 10) : parseFloat(last);
	return minus ? -value : value;
}

//#endregion
//#region src/tags/index.ts
const tagResolvers = {
	next: tagResolvers$2,
	"1.2": tagResolvers$2,
	"1.1": tagResolvers$1
};
const tagNodeResolvers = {
	next: tagNodeResolvers$2,
	"1.2": tagNodeResolvers$2,
	"1.1": tagNodeResolvers$1
};

//#endregion
//#region src/convert.ts
const isPair$1 = isPair;
var PreTokens = class {
	constructor(array, ctx) {
		this.index = 0;
		this.array = array;
		this.ctx = ctx;
	}
	first() {
		let cst;
		while (cst = this.array[this.index]) {
			if (processCommentOrSpace(cst, this.ctx)) {
				this.index++;
				continue;
			}
			return cst;
		}
		return null;
	}
	consume() {
		const cst = this.first();
		if (cst) this.index++;
		return cst;
	}
	back() {
		this.index--;
	}
	each(callback) {
		let cst;
		while (cst = this.consume()) callback(cst);
	}
};
/** Checks whether the give cst node is plain scaler */
function isPlainScalarCST(cst) {
	return cst.type === "scalar";
}
/** Checks whether the give cst node is double-quoted-scalar */
function isDoubleQuotedScalarCST(cst) {
	return cst.type === "double-quoted-scalar";
}
/** Checks whether the give cst node is single-quoted-scalar */
function isSingleQuotedScalarCST(cst) {
	return cst.type === "single-quoted-scalar";
}
/** Checks whether the give cst node is alias scalar */
function isAliasScalarCST(cst) {
	return cst.type === "alias";
}
/** Checks whether the give cst node is anchor */
function isAnchorCST(cst) {
	return cst.type === "anchor";
}
/** Checks whether the give cst node is tag */
function isTagCST(cst) {
	return cst.type === "tag";
}
/** Get node type name */
function getNodeType(node) {
	/* istanbul ignore next */
	return isMap(node) ? "MAP" : isSeq(node) ? "SEQ" : isScalar(node) ? "SCALAR" : isAlias(node) ? "ALIAS" : isPair$1(node) ? "PAIR" : isDocument(node) ? "DOCUMENT" : "unknown";
}
/**
* Convert yaml root to YAMLProgram
*/
function convertRoot(docs, ctx) {
	const { cstNodes } = docs;
	const ast = {
		type: "Program",
		body: [],
		comments: ctx.comments,
		sourceType: "module",
		tokens: ctx.tokens,
		parent: null,
		...ctx.getConvertLocation(0, ctx.code.length)
	};
	let directives = [];
	let bufferDoc = null;
	const cstDocs = [];
	for (const n of cstNodes) {
		if (processCommentOrSpace(n, ctx)) continue;
		if (n.type === "doc-end") {
			/* istanbul ignore if */
			if (!bufferDoc) throw ctx.throwUnexpectedTokenError(n);
			bufferDoc.docEnd = n;
			cstDocs.push(bufferDoc);
			bufferDoc = null;
			n.end?.forEach((t) => processAnyToken(t, ctx));
			continue;
		}
		if (bufferDoc) {
			cstDocs.push(bufferDoc);
			bufferDoc = null;
		}
		if (n.type === "directive") {
			directives.push(n);
			continue;
		}
		if (n.type === "document") {
			bufferDoc = {
				doc: n,
				node: docs.nodes[cstDocs.length],
				directives
			};
			directives = [];
			continue;
		}
		/* istanbul ignore next */
		throw ctx.throwUnexpectedTokenError(n);
	}
	if (bufferDoc) {
		cstDocs.push(bufferDoc);
		bufferDoc = null;
	}
	if (directives.length > 0) cstDocs.push({
		doc: null,
		node: null,
		directives
	});
	if (cstDocs.length > 0) {
		let startIndex = 0;
		ast.body = cstDocs.map((doc) => {
			const result = convertDocument(docs, doc, ctx, ast, startIndex);
			startIndex = result.range[1];
			return result;
		});
	} else {
		const index = skipSpaces(ctx.code, 0);
		ast.body.push({
			type: "YAMLDocument",
			directives: [],
			content: null,
			parent: ast,
			anchors: {},
			version: docs.streamInfo.directives.yaml.version,
			...ctx.getConvertLocation(index, index)
		});
	}
	sort(ctx.comments);
	sort(ctx.tokens);
	const lastBody = ast.body[ast.body.length - 1];
	if (lastBody) adjustEndLoc(lastBody, ctx.comments[ctx.comments.length - 1]);
	return ast;
}
/**
* Convert YAML.Document to YAMLDocument
*/
function convertDocument(docs, { directives, doc, node, docEnd }, ctx, parent, startIndex) {
	if (!doc || !node) {
		const docStartIndex = skipSpaces(ctx.code, startIndex);
		const loc$1 = ctx.getConvertLocation(docStartIndex, docStartIndex);
		const ast$1 = {
			type: "YAMLDocument",
			directives: [],
			content: null,
			parent,
			anchors: {},
			version: docs.streamInfo.directives.yaml.version,
			...loc$1
		};
		ast$1.directives.push(...convertDocumentHead(null, directives, ctx, ast$1));
		let last$1 = ast$1.directives[ast$1.directives.length - 1];
		if (docEnd) last$1 = ctx.addToken("Marker", toRange(docEnd));
		adjustEndLoc(ast$1, last$1);
		return ast$1;
	}
	const loc = ctx.getConvertLocation(skipSpaces(ctx.code, startIndex), node.range[1]);
	const ast = {
		type: "YAMLDocument",
		directives: [],
		content: null,
		parent,
		anchors: {},
		version: node.directives.yaml.version,
		...loc
	};
	ast.directives.push(...convertDocumentHead(node.directives, directives, ctx, ast));
	let last = ast.directives[ast.directives.length - 1];
	const startTokens = new PreTokens(doc.start, ctx);
	let t;
	while (t = startTokens.consume()) {
		if (t.type === "doc-start") {
			last = ctx.addToken("Marker", toRange(t));
			continue;
		}
		startTokens.back();
		break;
	}
	ast.content = convertDocumentBody(startTokens, doc.value || null, node.contents, ctx, ast);
	last = ast.content || last;
	if (doc.end) doc.end.forEach((token) => processAnyToken(token, ctx));
	if (docEnd) last = ctx.addToken("Marker", toRange(docEnd));
	adjustEndLoc(ast, last);
	return ast;
}
/**
* Convert YAML.Document.Parsed to YAMLDirective[]
*/
function* convertDocumentHead(node, directives, ctx, parent) {
	for (const n of directives) yield convertDirective(node, n, ctx, parent);
}
/**
* Convert CSTDirective to YAMLDirective
*/
function convertDirective(node, cst, ctx, parent) {
	const loc = ctx.getConvertLocation(...toRange(cst));
	const value = ctx.code.slice(...loc.range);
	const parts = cst.source.trim().split(/[\t ]+/);
	const name$1 = parts.shift();
	let ast;
	if (name$1 === "%YAML") ast = {
		type: "YAMLDirective",
		value,
		kind: "YAML",
		version: node ? node.yaml.version : cst.source.slice(6).trim(),
		parent,
		...loc
	};
	else if (name$1 === "%TAG") {
		const [handle, prefix] = parts;
		ast = {
			type: "YAMLDirective",
			value,
			kind: "TAG",
			handle,
			prefix,
			parent,
			...loc
		};
	} else ast = {
		type: "YAMLDirective",
		value,
		kind: null,
		parent,
		...loc
	};
	ctx.addToken("Directive", loc.range);
	return ast;
}
/**
* Convert Document body to YAMLContent
*/
function convertDocumentBody(preTokens, cst, node, ctx, parent) {
	if (cst) return convertContentNode(preTokens, cst, node, ctx, parent, parent);
	const token = preTokens.first();
	if (token) {
		if (isScalar(node) && node.source === "") return convertAnchorAndTag(preTokens, node, ctx, parent, null, parent, ctx.getConvertLocation(node.range[0], node.range[1]));
		/* istanbul ignore next */
		throw ctx.throwUnexpectedTokenError(token);
	}
	return null;
}
/**
* Convert ContentNode to YAMLContent
*/
function convertContentNode(preTokens, cst, node, ctx, parent, doc) {
	/* istanbul ignore if */
	if (!node) throw ctx.throwError(`unknown error: AST is null. Unable to process content CST (${cst.type}).`, cst);
	/* istanbul ignore if */
	if (node.srcToken !== cst) throw ctx.throwError(`unknown error: CST is mismatched. Unable to process content CST (${cst.type}: ${node.srcToken?.type}).`, cst);
	if (cst.type === "block-scalar") {
		/* istanbul ignore if */
		if (!isScalar(node)) throw ctx.throwError(`unknown error: AST is not Scalar (${getNodeType(node)}). Unable to process Scalar CST.`, cst);
		return convertBlockScalar(preTokens, cst, node, ctx, parent, doc);
	}
	if (cst.type === "block-seq") {
		/* istanbul ignore if */
		if (!isSeq(node)) throw ctx.throwError(`unknown error: AST is not Seq (${getNodeType(node)}). Unable to process Seq CST.`, cst);
		return convertSequence(preTokens, cst, node, ctx, parent, doc);
	}
	if (cst.type === "block-map") {
		/* istanbul ignore if */
		if (!isMap(node)) throw ctx.throwError(`unknown error: AST is not Map and Pair (${getNodeType(node)}). Unable to process Map CST.`, cst);
		return convertMapping(preTokens, cst, node, ctx, parent, doc);
	}
	if (cst.type === "flow-collection") return convertFlowCollection(preTokens, cst, node, ctx, parent, doc);
	if (isPlainScalarCST(cst)) {
		/* istanbul ignore if */
		if (!isScalar(node)) throw ctx.throwError(`unknown error: AST is not Scalar (${getNodeType(node)}). Unable to process Scalar CST.`, cst);
		return convertPlain(preTokens, cst, node, ctx, parent, doc);
	}
	if (isDoubleQuotedScalarCST(cst)) {
		/* istanbul ignore if */
		if (!isScalar(node)) throw ctx.throwError(`unknown error: AST is not Scalar (${getNodeType(node)}). Unable to process Scalar CST.`, cst);
		return convertQuoteDouble(preTokens, cst, node, ctx, parent, doc);
	}
	if (isSingleQuotedScalarCST(cst)) {
		/* istanbul ignore if */
		if (!isScalar(node)) throw ctx.throwError(`unknown error: AST is not Scalar (${getNodeType(node)}). Unable to process Scalar CST.`, cst);
		return convertQuoteSingle(preTokens, cst, node, ctx, parent, doc);
	}
	if (isAliasScalarCST(cst)) {
		/* istanbul ignore if */
		if (!isAlias(node)) throw ctx.throwError(`unknown error: AST is not Alias (${getNodeType(node)}). Unable to process Alias CST.`, cst);
		return convertAlias(preTokens, cst, node, ctx, parent, doc);
	}
	/* istanbul ignore next */
	throw new Error(`Unsupported node: ${cst.type}`);
}
/**
* Convert Map to YAMLBlockMapping
*/
function convertMapping(preTokens, cst, node, ctx, parent, doc) {
	if (isPair$1(node)) {
		/* istanbul ignore if */
		if (node.srcToken !== cst.items[0]) throw ctx.throwError(`unknown error: CST is mismatched. Unable to process mapping CST (${cst.type}: "CollectionItem").`, cst);
	} else if (node.srcToken !== cst) throw ctx.throwError(`unknown error: CST is mismatched. Unable to process mapping CST (${cst.type}: ${node.srcToken?.type}).`, cst);
	const ast = {
		type: "YAMLMapping",
		style: "block",
		pairs: [],
		parent,
		...ctx.getConvertLocation(cst.offset, cst.offset)
	};
	const items = getPairs(node);
	let firstKeyInd;
	let lastKeyInd;
	for (const item of cst.items) {
		const startTokens = new PreTokens(item.start, ctx);
		let token;
		let keyInd = null;
		while (token = startTokens.consume()) {
			if (token.type === "explicit-key-ind") {
				/* istanbul ignore if */
				if (keyInd) throw ctx.throwUnexpectedTokenError(token);
				lastKeyInd = keyInd = ctx.addToken("Punctuator", toRange(token));
				firstKeyInd ??= keyInd;
				continue;
			}
			startTokens.back();
			break;
		}
		const pair = items.shift();
		if (!pair) {
			const t = startTokens.first() || keyInd || item.key || item.sep?.[0] || item.value;
			if (!t) break;
			/* istanbul ignore next */
			throw ctx.throwUnexpectedTokenError(t);
		}
		ast.pairs.push(convertMappingItem(keyInd, startTokens, item, pair, ctx, ast, doc));
	}
	adjustStartLoc(ast, firstKeyInd);
	adjustStartLoc(ast, ast.pairs[0]);
	adjustEndLoc(ast, ast.pairs[ast.pairs.length - 1] || lastKeyInd);
	if (!isMap(node)) return ast;
	return convertAnchorAndTag(preTokens, node, ctx, parent, ast, doc, ast);
}
/**
* Convert FlowCollection to YAMLFlowMapping
*/
function convertFlowCollection(preTokens, cst, node, ctx, parent, doc) {
	if (cst.start.type === "flow-map-start") {
		const startToken = ctx.addToken("Punctuator", toRange(cst.start));
		/* istanbul ignore if */
		if (!isMap(node) && !isPair$1(node)) throw ctx.throwError(`unknown error: AST is not Map and Pair (${getNodeType(node)}). Unable to process flow map CST.`, cst);
		return convertFlowMapping(preTokens, startToken, cst, node, ctx, parent, doc);
	}
	if (cst.start.type === "flow-seq-start") {
		const startToken = ctx.addToken("Punctuator", toRange(cst.start));
		/* istanbul ignore if */
		if (!isSeq(node) || !node.flow) throw ctx.throwError(`unknown error: AST is not flow Seq (${getNodeType(node)}). Unable to process flow seq CST.`, cst);
		return convertFlowSequence(preTokens, startToken, cst, node, ctx, parent, doc);
	}
	/* istanbul ignore next */
	throw ctx.throwUnexpectedTokenError(cst.start);
}
/**
* Convert FlowMap to YAMLFlowMapping
*/
function convertFlowMapping(preTokens, startToken, cst, node, ctx, parent, doc) {
	const ast = {
		type: "YAMLMapping",
		style: "flow",
		pairs: [],
		parent,
		...ctx.getConvertLocation(startToken.range[0], cst.offset)
	};
	const items = getPairs(node);
	let lastToken;
	for (const item of cst.items) {
		const startTokens = new PreTokens(item.start, ctx);
		let token;
		let keyInd = null;
		while (token = startTokens.consume()) {
			if (token.type === "comma") {
				lastToken = ctx.addToken("Punctuator", toRange(token));
				continue;
			}
			if (token.type === "explicit-key-ind") {
				/* istanbul ignore if */
				if (keyInd) throw ctx.throwUnexpectedTokenError(token);
				lastToken = keyInd = ctx.addToken("Punctuator", toRange(token));
				continue;
			}
			startTokens.back();
			break;
		}
		const pair = items.shift();
		if (!pair) {
			const t = startTokens.first() || keyInd || item.key || item.sep?.[0] || item.value;
			if (!t) break;
			/* istanbul ignore next */
			throw ctx.throwUnexpectedTokenError(t);
		}
		ast.pairs.push(convertMappingItem(keyInd, startTokens, item, pair, ctx, ast, doc));
	}
	let mapEnd;
	for (const token of cst.end) {
		if (processCommentOrSpace(token, ctx)) continue;
		if (token.type === "flow-map-end") {
			mapEnd = ctx.addToken("Punctuator", toRange(token));
			continue;
		}
		/* istanbul ignore next */
		throw ctx.throwUnexpectedTokenError(token);
	}
	adjustEndLoc(ast, mapEnd || ast.pairs[ast.pairs.length - 1] || lastToken);
	if (!isMap(node)) return ast;
	return convertAnchorAndTag(preTokens, node, ctx, parent, ast, doc, ast);
}
/**
* Convert FlowSeq to YAMLFlowSequence
*/
function convertFlowSequence(preTokens, startToken, cst, node, ctx, parent, doc) {
	const ast = {
		type: "YAMLSequence",
		style: "flow",
		entries: [],
		parent,
		...ctx.getConvertLocation(startToken.range[0], cst.offset)
	};
	let lastToken;
	const items = [...node.items];
	for (const item of cst.items) {
		const startTokens = new PreTokens(item.start, ctx);
		let token;
		while (token = startTokens.consume()) {
			if (token.type === "comma") {
				lastToken = ctx.addToken("Punctuator", toRange(token));
				continue;
			}
			startTokens.back();
			break;
		}
		if (items.length === 0) {
			const t = startTokens.first() || item.key || item.sep?.[0] || item.value;
			if (!t) break;
			/* istanbul ignore next */
			throw ctx.throwUnexpectedTokenError(t);
		}
		const entry = items.shift();
		if (isPair$1(entry) || (item.key || item.sep) && isMap(entry)) ast.entries.push(convertMap(startTokens, item, entry));
		else ast.entries.push(convertFlowSequenceItem(startTokens, item.value || null, entry || null, ctx, ast, doc, (ast.entries[ast.entries.length - 1] || lastToken || startToken).range[1]));
	}
	let seqEnd;
	for (const token of cst.end) {
		if (processCommentOrSpace(token, ctx)) continue;
		if (token.type === "flow-seq-end") {
			seqEnd = ctx.addToken("Punctuator", toRange(token));
			continue;
		}
		/* istanbul ignore next */
		throw ctx.throwUnexpectedTokenError(token);
	}
	adjustEndLoc(ast, seqEnd || ast.entries[ast.entries.length - 1] || lastToken);
	return convertAnchorAndTag(preTokens, node, ctx, parent, ast, doc, ast);
	/** Convert CollectionItem to YAMLBlockMapping */
	function convertMap(pairPreTokens, pairCst, entry) {
		const startTokens = pairPreTokens;
		let keyInd = null;
		let token;
		while (token = startTokens.consume()) {
			if (token.type === "comma") {
				ctx.addToken("Punctuator", toRange(token));
				continue;
			}
			if (token.type === "explicit-key-ind") {
				/* istanbul ignore if */
				if (keyInd) throw ctx.throwUnexpectedTokenError(token);
				keyInd = ctx.addToken("Punctuator", toRange(token));
				continue;
			}
			startTokens.back();
			break;
		}
		const pairStartToken = pairCst.key ?? pairCst.sep[0];
		const mapAst = {
			type: "YAMLMapping",
			style: "block",
			pairs: [],
			parent: ast,
			...ctx.getConvertLocation(keyInd?.range[0] ?? pairStartToken.offset, keyInd?.range[1] ?? pairStartToken.offset)
		};
		const pair = convertMappingItem(keyInd, startTokens, pairCst, getPairs(entry)[0], ctx, mapAst, doc);
		mapAst.pairs.push(pair);
		adjustStartLoc(mapAst, keyInd || pair);
		adjustEndLoc(mapAst, pair || keyInd);
		return mapAst;
	}
}
/**
* Convert Pair to YAMLPair
*/
function convertMappingItem(keyInd, preTokens, cst, node, ctx, parent, doc) {
	const start = keyInd?.range[0] ?? preTokens.first()?.offset ?? cst.key?.offset ?? cst.sep?.[0]?.offset ?? cst.value?.offset ?? -1;
	const ast = {
		type: "YAMLPair",
		key: null,
		value: null,
		parent,
		...ctx.getConvertLocation(start, start)
	};
	ast.key = convertMappingKey(preTokens, cst.key || null, node.key, ctx, ast, doc, start);
	const valueStartTokens = new PreTokens(cst.sep || [], ctx);
	let valueInd;
	let token;
	while (token = valueStartTokens.consume()) {
		if (token.type === "map-value-ind") {
			/* istanbul ignore if */
			if (valueInd) throw ctx.throwUnexpectedTokenError(token);
			valueInd = ctx.addToken("Punctuator", toRange(token));
			continue;
		}
		valueStartTokens.back();
		break;
	}
	ast.value = convertMappingValue(valueStartTokens, cst.value || null, node.value, ctx, ast, doc, start);
	adjustEndLoc(ast, ast.value || valueInd || ast.key || keyInd);
	return ast;
}
/**
* Convert MapKey to YAMLContent
*/
function convertMappingKey(preTokens, cst, node, ctx, parent, doc, indexForError) {
	if (cst) return convertContentNode(preTokens, cst, node, ctx, parent, doc);
	/* istanbul ignore if */
	if (!isScalarOrNull(node)) throw ctx.throwError(`unknown error: AST is not Scalar and null (${getNodeType(node)}). Unable to process empty map key CST.`, preTokens.first() ?? indexForError);
	return convertAnchorAndTag(preTokens, node, ctx, parent, null, doc, null);
}
/**
* Convert MapValue to YAMLContent
*/
function convertMappingValue(preTokens, cst, node, ctx, parent, doc, indexForError) {
	if (cst) return convertContentNode(preTokens, cst, node, ctx, parent, doc);
	/* istanbul ignore if */
	if (!isScalarOrNull(node)) throw ctx.throwError(`unknown error: AST is not Scalar and null (${getNodeType(node)}). Unable to process empty map value CST.`, preTokens.first() ?? indexForError);
	return convertAnchorAndTag(preTokens, node, ctx, parent, null, doc, null);
}
/**
* Convert BlockSeq to YAMLBlockSequence
*/
function convertSequence(preTokens, cst, node, ctx, parent, doc) {
	const ast = {
		type: "YAMLSequence",
		style: "block",
		entries: [],
		parent,
		...ctx.getConvertLocation(cst.offset, cst.offset)
	};
	const items = [...node.items];
	let lastSeqInd;
	for (const item of cst.items) {
		const startTokens = new PreTokens(item.start, ctx);
		let seqInd;
		let token;
		while (token = startTokens.consume()) {
			if (token.type === "seq-item-ind") {
				/* istanbul ignore if */
				if (seqInd) throw ctx.throwUnexpectedTokenError(token);
				lastSeqInd = seqInd = ctx.addToken("Punctuator", toRange(token));
				continue;
			}
			startTokens.back();
			break;
		}
		if (items.length === 0) {
			const t = startTokens.first() || item.key || item.sep?.[0] || item.value;
			if (!t) break;
			/* istanbul ignore next */
			throw ctx.throwUnexpectedTokenError(t);
		}
		ast.entries.push(convertSequenceItem(startTokens, item, items.shift() || null, ctx, ast, doc, (ast.entries[ast.entries.length - 1] || ast).range[1]));
	}
	adjustEndLoc(ast, ast.entries[ast.entries.length - 1] || lastSeqInd);
	return convertAnchorAndTag(preTokens, node, ctx, parent, ast, doc, ast);
}
/**
* Convert SeqItem to YAMLContent
*/
function convertSequenceItem(preTokens, cst, node, ctx, parent, doc, indexForError) {
	/* istanbul ignore if */
	if (cst.key) throw ctx.throwUnexpectedTokenError(cst.key);
	/* istanbul ignore if */
	if (cst.sep) throw ctx.throwUnexpectedTokenError(cst.sep);
	if (cst.value) {
		if (isPair$1(node)) {
			if (cst.value.type === "block-map") return convertMapping(preTokens, cst.value, node, ctx, parent, doc);
			if (cst.value.type === "flow-collection") return convertFlowCollection(preTokens, cst.value, node, ctx, parent, doc);
			throw ctx.throwError(`unknown error: CST is not block-map and flow-collection (${cst.value.type}). Unable to process Pair AST.`, cst.value);
		}
		return convertContentNode(preTokens, cst.value, node, ctx, parent, doc);
	}
	/* istanbul ignore if */
	if (!isScalarOrNull(node)) throw ctx.throwError(`unknown error: AST is not Scalar and null (${getNodeType(node)}). Unable to process empty seq item CST.`, preTokens.first() ?? indexForError);
	return convertAnchorAndTag(preTokens, node, ctx, parent, null, doc, null);
}
/**
* Convert FlowSeqItem to YAMLContent
*/
function convertFlowSequenceItem(preTokens, cst, node, ctx, parent, doc, indexForError) {
	if (cst) return convertContentNode(preTokens, cst, node, ctx, parent, doc);
	/* istanbul ignore if */
	if (!isScalarOrNull(node)) throw ctx.throwError(`unknown error: AST is not Scalar and null (${getNodeType(node)}). Unable to process empty seq item CST.`, preTokens.first() ?? indexForError);
	return convertAnchorAndTag(preTokens, node, ctx, parent, null, doc, null);
}
/**
* Convert PlainValue to YAMLPlainScalar
*/
function convertPlain(preTokens, cst, node, ctx, parent, doc) {
	const loc = ctx.getConvertLocation(...toRange(cst));
	let ast;
	if (loc.range[0] < loc.range[1]) {
		const strValue = node.source || cst.source;
		const value = parseValueFromText(strValue, doc.version || "1.2");
		ast = {
			type: "YAMLScalar",
			style: "plain",
			strValue,
			value,
			raw: ctx.code.slice(...loc.range),
			parent,
			...loc
		};
		const type = typeof value;
		if (type === "boolean") ctx.addToken("Boolean", loc.range);
		else if (type === "number" && isFinite(Number(value))) ctx.addToken("Numeric", loc.range);
		else if (value === null) ctx.addToken("Null", loc.range);
		else ctx.addToken("Identifier", loc.range);
		ast = convertAnchorAndTag(preTokens, node, ctx, parent, ast, doc, loc);
	} else ast = convertAnchorAndTag(preTokens, node, ctx, parent, null, doc, loc);
	cst.end?.forEach((t) => processAnyToken(t, ctx));
	return ast;
	/**
	* Parse value from text
	*/
	function parseValueFromText(str, version$1) {
		for (const tagResolver of tagResolvers[version$1]) if (tagResolver.testString(str)) return tagResolver.resolveString(str);
		return str;
	}
}
/**
* Convert QuoteDouble to YAMLDoubleQuotedScalar
*/
function convertQuoteDouble(preTokens, cst, node, ctx, parent, doc) {
	const loc = ctx.getConvertLocation(...toRange(cst));
	const strValue = node.source;
	const ast = {
		type: "YAMLScalar",
		style: "double-quoted",
		strValue,
		value: strValue,
		raw: ctx.code.slice(...loc.range),
		parent,
		...loc
	};
	ctx.addToken("String", loc.range);
	cst.end?.forEach((t) => processAnyToken(t, ctx));
	return convertAnchorAndTag(preTokens, node, ctx, parent, ast, doc, ast);
}
/**
* Convert QuoteSingle to YAMLSingleQuotedScalar
*/
function convertQuoteSingle(preTokens, cst, node, ctx, parent, doc) {
	const loc = ctx.getConvertLocation(...toRange(cst));
	const strValue = node.source;
	const ast = {
		type: "YAMLScalar",
		style: "single-quoted",
		strValue,
		value: strValue,
		raw: ctx.code.slice(...loc.range),
		parent,
		...loc
	};
	ctx.addToken("String", loc.range);
	cst.end?.forEach((t) => processAnyToken(t, ctx));
	return convertAnchorAndTag(preTokens, node, ctx, parent, ast, doc, ast);
}
/**
* Convert BlockLiteral to YAMLBlockLiteral
*/
function convertBlockScalar(preTokens, cst, node, ctx, parent, doc) {
	let headerToken, ast;
	let blockStart = cst.offset;
	for (const token of cst.props) {
		if (processCommentOrSpace(token, ctx)) {
			blockStart = token.offset + token.source.length;
			continue;
		}
		if (token.type === "block-scalar-header") {
			headerToken = ctx.addToken("Punctuator", toRange(token));
			blockStart = headerToken.range[1];
			continue;
		}
		/* istanbul ignore next */
		throw ctx.throwUnexpectedTokenError(token);
	}
	const headerValue = headerToken.value;
	const end = node.source ? getBlockEnd(blockStart + cst.source.length, ctx) : ctx.lastSkipSpaces(cst.offset, headerToken.range[1]);
	const loc = ctx.getConvertLocation(headerToken.range[0], end);
	if (headerValue.startsWith(">")) {
		ast = {
			type: "YAMLScalar",
			style: "folded",
			...parseHeader(headerValue),
			value: node.source,
			parent,
			...loc
		};
		const text = ctx.code.slice(blockStart, end);
		const offset = /^[^\S\n\r]*/.exec(text)[0].length;
		const tokenRange = [blockStart + offset, end];
		if (tokenRange[0] < tokenRange[1]) ctx.addToken("BlockFolded", tokenRange);
	} else {
		ast = {
			type: "YAMLScalar",
			style: "literal",
			...parseHeader(headerValue),
			value: node.source,
			parent,
			...loc
		};
		const text = ctx.code.slice(blockStart, end);
		const offset = /^[^\S\n\r]*/.exec(text)[0].length;
		const tokenRange = [blockStart + offset, end];
		if (tokenRange[0] < tokenRange[1]) ctx.addToken("BlockLiteral", tokenRange);
	}
	return convertAnchorAndTag(preTokens, node, ctx, parent, ast, doc, ast);
	/** Get chomping kind */
	function parseHeader(header) {
		const parsed = /([+-]?)(\d*)([+-]?)$/u.exec(header);
		let indent = null;
		let chomping = "clip";
		if (parsed) {
			indent = parsed[2] ? Number(parsed[2]) : null;
			const chompingStr = parsed[3] || parsed[1];
			chomping = chompingStr === "+" ? "keep" : chompingStr === "-" ? "strip" : "clip";
		}
		return {
			chomping,
			indent
		};
	}
}
/**
* Get the end index from give block end
*/
function getBlockEnd(end, ctx) {
	let index = end;
	if (ctx.code[index - 1] === "\n" && index > 1) {
		index--;
		if (ctx.code[index - 1] === "\r" && index > 1) index--;
	}
	return index;
}
/**
* Convert Alias to YAMLAlias
*/
function convertAlias(preTokens, cst, _node, ctx, parent, _doc) {
	const [start, end] = toRange(cst);
	const loc = ctx.getConvertLocation(start, ctx.lastSkipSpaces(start, end));
	const ast = {
		type: "YAMLAlias",
		name: cst.source.slice(1),
		parent,
		...loc
	};
	ctx.addToken("Punctuator", [loc.range[0], loc.range[0] + 1]);
	const tokenRange = [loc.range[0] + 1, loc.range[1]];
	if (tokenRange[0] < tokenRange[1]) ctx.addToken("Identifier", tokenRange);
	const token = preTokens.first();
	/* istanbul ignore if */
	if (token) throw ctx.throwUnexpectedTokenError(token);
	cst.end?.forEach((t) => processAnyToken(t, ctx));
	return ast;
}
/**
* Convert Anchor and Tag
*/
function convertAnchorAndTag(preTokens, node, ctx, parent, value, doc, valueLoc) {
	let meta = null;
	/**
	* Get YAMLWithMeta
	*/
	function getMetaAst(cst) {
		if (meta) return meta;
		meta = {
			type: "YAMLWithMeta",
			anchor: null,
			tag: null,
			value,
			parent,
			...valueLoc ? {
				range: [...valueLoc.range],
				loc: cloneLoc(valueLoc.loc)
			} : ctx.getConvertLocation(...toRange(cst))
		};
		if (value) value.parent = meta;
		return meta;
	}
	preTokens.each((cst) => {
		if (isAnchorCST(cst)) {
			const ast = getMetaAst(cst);
			const anchor = convertAnchor(cst, ctx, ast, doc);
			ast.anchor = anchor;
			adjustStartLoc(ast, anchor);
			adjustEndLoc(ast, anchor);
		} else if (isTagCST(cst)) {
			const ast = getMetaAst(cst);
			const tag = convertTag(cst, node?.tag ?? null, ctx, ast);
			ast.tag = tag;
			adjustStartLoc(ast, tag);
			adjustEndLoc(ast, tag);
		} else
 /* istanbul ignore next */
		throw ctx.throwUnexpectedTokenError(cst);
	});
	return meta || value;
}
/**
* Convert anchor to YAMLAnchor
*/
function convertAnchor(cst, ctx, parent, doc) {
	const name$1 = cst.source.slice(1);
	const loc = ctx.getConvertLocation(...toRange(cst));
	const ast = {
		type: "YAMLAnchor",
		name: name$1,
		parent,
		...loc
	};
	(doc.anchors[name$1] || (doc.anchors[name$1] = [])).push(ast);
	const punctuatorRange = [loc.range[0], loc.range[0] + 1];
	ctx.addToken("Punctuator", punctuatorRange);
	const tokenRange = [punctuatorRange[1], loc.range[1]];
	if (tokenRange[0] < tokenRange[1]) ctx.addToken("Identifier", tokenRange);
	return ast;
}
/**
* Convert tag to YAMLTag
*/
function convertTag(cst, tag, ctx, parent) {
	const offset = cst.source.startsWith("!!") ? 2 : 1;
	let resolvedTag = tag ?? cst.source.slice(offset);
	if (resolvedTag === "!") resolvedTag = "tag:yaml.org,2002:str";
	const loc = ctx.getConvertLocation(...toRange(cst));
	const ast = {
		type: "YAMLTag",
		tag: resolvedTag,
		raw: cst.source,
		parent,
		...loc
	};
	const punctuatorRange = [loc.range[0], loc.range[0] + offset];
	ctx.addToken("Punctuator", punctuatorRange);
	const tokenRange = [punctuatorRange[1], loc.range[1]];
	if (tokenRange[0] < tokenRange[1]) ctx.addToken("Identifier", tokenRange);
	return ast;
}
/** Checks whether the give node is scaler or null */
function isScalarOrNull(node) {
	return isScalar(node) || node == null;
}
/** Get the pairs from the give node */
function getPairs(node) {
	return isMap(node) ? [...node.items] : [node];
}
/**
* Process comments or spaces
*/
function processCommentOrSpace(node, ctx) {
	if (node.type === "space" || node.type === "newline") return true;
	/* istanbul ignore if */
	if (node.type === "flow-error-end" || node.type === "error") throw ctx.throwUnexpectedTokenError(node);
	if (node.type === "comment") {
		const comment = {
			type: "Block",
			value: node.source.slice(1),
			...ctx.getConvertLocation(...toRange(node))
		};
		ctx.addComment(comment);
		return true;
	}
	return false;
}
/**
* Process any token
*/
function processAnyToken(node, ctx) {
	/* istanbul ignore if */
	if (!processCommentOrSpace(node, ctx)) throw ctx.throwUnexpectedTokenError(node);
}
/**
* Sort tokens
*/
function sort(tokens) {
	return tokens.sort((a, b) => {
		if (a.range[0] > b.range[0]) return 1;
		if (a.range[0] < b.range[0]) return -1;
		if (a.range[1] > b.range[1]) return 1;
		if (a.range[1] < b.range[1]) return -1;
		return 0;
	});
}
/**
* clone the location.
*/
function clonePos(loc) {
	return {
		line: loc.line,
		column: loc.column
	};
}
/**
* clone the location.
*/
function cloneLoc(loc) {
	return {
		start: clonePos(loc.start),
		end: clonePos(loc.end)
	};
}
/**
* Gets the first index with whitespace skipped.
*/
function skipSpaces(str, startIndex) {
	const len = str.length;
	for (let index = startIndex; index < len; index++) if (str[index].trim()) return index;
	return len;
}
/** SourceToken to location range */
function toRange(token) {
	return [token.offset, token.offset + token.source.length];
}
/** Adjust start location */
function adjustStartLoc(ast, first) {
	if (first && first.range[0] < ast.range[0]) {
		ast.range[0] = first.range[0];
		ast.loc.start = clonePos(first.loc.start);
	}
}
/** Adjust end location */
function adjustEndLoc(ast, last) {
	if (last && ast.range[1] < last.range[1]) {
		ast.range[1] = last.range[1];
		ast.loc.end = clonePos(last.loc.end);
	}
}

//#endregion
//#region src/options.ts
/**
* ESLint parserOptions to `yaml`'s Composer options.
*/
function parserOptionsToYAMLOption(options) {
	if (!options) return {};
	const result = {};
	const version$1 = options.defaultYAMLVersion;
	if (typeof version$1 === "string" || typeof version$1 === "number") {
		const sVer = String(version$1);
		if (sVer === "1.2" || sVer === "1.1") result.version = sVer;
		else result.version = "next";
	}
	return result;
}

//#endregion
//#region src/context.ts
var Context = class {
	constructor(origCode, parserOptions) {
		this.tokens = [];
		this.comments = [];
		this.locsMap = /* @__PURE__ */ new Map();
		this.options = parserOptionsToYAMLOption(parserOptions);
		this.code = origCode;
		this.lineCounter = new LineCounter();
	}
	getLocFromIndex(index) {
		let loc = this.locsMap.get(index);
		if (!loc) {
			const { line, col } = this.lineCounter.linePos(index);
			loc = {
				line,
				column: col - 1
			};
			this.locsMap.set(index, loc);
		}
		return {
			line: loc.line,
			column: loc.column
		};
	}
	/**
	* Get the location information of the given range.
	*/
	getConvertLocation(start, end) {
		return {
			range: [start, end],
			loc: {
				start: this.getLocFromIndex(start),
				end: this.getLocFromIndex(end)
			}
		};
	}
	addComment(comment) {
		this.comments.push(comment);
	}
	/**
	* Add token to tokens
	*/
	addToken(type, range) {
		const token = {
			type,
			value: this.code.slice(...range),
			...this.getConvertLocation(...range)
		};
		this.tokens.push(token);
		return token;
	}
	/* istanbul ignore next */
	throwUnexpectedTokenError(cst) {
		const token = "source" in cst ? `'${cst.source}'` : cst.type;
		throw this.throwError(`Unexpected token: ${token}`, cst);
	}
	throwError(message, cst) {
		const offset = typeof cst === "number" ? cst : "offset" in cst ? cst.offset : cst.range[0];
		const loc = this.getLocFromIndex(offset);
		throw new ParseError(message, offset, loc.line, loc.column);
	}
	/**
	* Gets the last index with whitespace skipped.
	*/
	lastSkipSpaces(startIndex, endIndex) {
		const str = this.code;
		for (let index = endIndex - 1; index >= startIndex; index--) if (str[index].trim()) return index + 1;
		return startIndex;
	}
};

//#endregion
//#region src/yaml-cst-parse.ts
/** Parse yaml to CST */
function parseAllDocsToCST(ctx) {
	const { lineCounter } = ctx;
	const parser = new Parser(lineCounter.addNewLine);
	const composer = new Composer({
		...ctx.options,
		keepSourceTokens: true,
		lineCounter
	});
	const cstNodes = [...parser.parse(ctx.code)];
	const nodes = [];
	for (const doc of composer.compose(cstNodes)) {
		for (const error of doc.errors) throw ctx.throwError(error.message, error.pos[0]);
		nodes.push(doc);
	}
	return {
		nodes,
		cstNodes,
		streamInfo: composer.streamInfo()
	};
}

//#endregion
//#region src/parser.ts
/**
* Parse YAML source code
*/
function parseYAML(code, options) {
	const ctx = new Context(code, options);
	return convertRoot(parseAllDocsToCST(ctx), ctx);
}

//#endregion
//#region src/visitor-keys.ts
const yamlKeys = {
	Program: ["body"],
	YAMLDocument: ["directives", "content"],
	YAMLDirective: [],
	YAMLMapping: ["pairs"],
	YAMLPair: ["key", "value"],
	YAMLSequence: ["entries"],
	YAMLWithMeta: [
		"anchor",
		"tag",
		"value"
	],
	YAMLScalar: [],
	YAMLAlias: [],
	YAMLAnchor: [],
	YAMLTag: []
};
const KEYS = unionWith(yamlKeys);

//#endregion
//#region src/traverse.ts
/**
* Check that the given key should be traversed or not.
* @this {Traversable}
* @param key The key to check.
* @returns `true` if the key should be traversed.
*/
function fallbackKeysFilter(key) {
	let value = null;
	return key !== "comments" && key !== "leadingComments" && key !== "loc" && key !== "parent" && key !== "range" && key !== "tokens" && key !== "trailingComments" && (value = this[key]) !== null && typeof value === "object" && (typeof value.type === "string" || Array.isArray(value));
}
/**
* Get the keys of the given node to traverse it.
* @param node The node to get.
* @returns The keys to traverse.
*/
function getFallbackKeys(node) {
	return Object.keys(node).filter(fallbackKeysFilter, node);
}
/**
* Get the keys of the given node to traverse it.
* @param node The node to get.
* @returns The keys to traverse.
*/
function getKeys(node, visitorKeys) {
	return ((visitorKeys || KEYS)[node.type] || getFallbackKeys(node)).filter((key) => !getNodes(node, key).next().done);
}
/**
* Get the nodes of the given node.
* @param node The node to get.
*/
function* getNodes(node, key) {
	const child = node[key];
	if (Array.isArray(child)) {
		for (const c of child) if (isNode(c)) yield c;
	} else if (isNode(child)) yield child;
}
/**
* Check whether a given value is a node.
* @param x The value to check.
* @returns `true` if the value is a node.
*/
function isNode(x) {
	return x !== null && typeof x === "object" && typeof x.type === "string";
}
/**
* Traverse the given node.
* @param node The node to traverse.
* @param parent The parent node.
* @param visitor The node visitor.
*/
function traverse(node, parent, visitor) {
	visitor.enterNode(node, parent);
	const keys = getKeys(node, visitor.visitorKeys);
	for (const key of keys) for (const child of getNodes(node, key)) traverse(child, node, visitor);
	visitor.leaveNode(node, parent);
}
/**
* Traverse the given AST tree.
* @param node Root node to traverse.
* @param visitor Visitor.
*/
function traverseNodes(node, visitor) {
	traverse(node, null, visitor);
}

//#endregion
//#region src/errors.ts
/**
* YAML parse errors.
*/
var ParseError = class extends SyntaxError {
	/**
	* Initialize this ParseError instance.
	* @param message The error message.
	* @param offset The offset number of this error.
	* @param line The line number of this error.
	* @param column The column number of this error.
	*/
	constructor(message, offset, line, column) {
		super(message);
		this.index = offset;
		this.lineNumber = line;
		this.column = column;
	}
};

//#endregion
//#region src/meta.ts
var meta_exports = /* @__PURE__ */ __exportAll({
	name: () => name,
	version: () => version
});
const name = "yaml-eslint-parser";
const version = "2.0.0";

//#endregion
//#region src/index.ts
const VisitorKeys = KEYS;
/**
* Parse source code
*/
function parseForESLint(code, options) {
	return {
		ast: parseYAML(code, options),
		visitorKeys: KEYS,
		services: { isYAML: true }
	};
}

//#endregion
export { ParseError, VisitorKeys, getStaticYAMLValue, meta_exports as meta, name, parseForESLint, parseYAML, traverseNodes };