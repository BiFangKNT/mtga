import { t as __exportAll } from "./chunk-DQk6qfdC.mjs";
import * as yamlESLintParser from "yaml-eslint-parser";
import { VisitorKeys, getStaticYAMLValue, parseForESLint, parseYAML, traverseNodes } from "yaml-eslint-parser";
import path from "node:path";
import naturalCompare from "natural-compare";
import diffModule from "diff-sequences";
import escapeStringRegexp from "escape-string-regexp";
import { CallMethodStep, ConfigCommentParser, Directive, TextSourceCodeBase, VisitNodeStep } from "@eslint/plugin-kit";
import { TokenStore } from "@ota-meshi/ast-token-store";

//#region src/utils/index.ts
/**
* Define the rule.
* @param ruleName ruleName
* @param rule rule module
*/
function createRule(ruleName, rule) {
	return {
		meta: {
			...rule.meta,
			docs: {
				...rule.meta.docs,
				url: `https://ota-meshi.github.io/eslint-plugin-yml/rules/${ruleName}.html`,
				ruleId: `yml/${ruleName}`,
				ruleName
			}
		},
		create(context) {
			const sourceCode = context.sourceCode;
			if (typeof sourceCode.parserServices?.defineCustomBlocksVisitor === "function" && path.extname(context.filename) === ".vue") return sourceCode.parserServices.defineCustomBlocksVisitor(context, yamlESLintParser, {
				target: ["yaml", "yml"],
				create(blockContext) {
					return rule.create(blockContext, { customBlock: true });
				}
			});
			return rule.create(context, { customBlock: false });
		}
	};
}

//#endregion
//#region src/utils/ast-utils.ts
/**
* Checks if the given token is a comment token or not.
* @param {Token} token The token to check.
* @returns {boolean} `true` if the token is a comment token.
*/
function isCommentToken(token) {
	return Boolean(token && (token.type === "Block" || token.type === "Line"));
}
/**
* Determines whether two adjacent tokens are on the same line.
* @param {Object} left The left token object.
* @param {Object} right The right token object.
* @returns {boolean} Whether or not the tokens are on the same line.
* @public
*/
function isTokenOnSameLine(left, right) {
	return left.loc.end.line === right.loc.start.line;
}
/**
* Check whether the given token is a question.
* @param token The token to check.
* @returns `true` if the token is a question.
*/
function isQuestion(token) {
	return token != null && token.type === "Punctuator" && token.value === "?";
}
/**
* Check whether the given token is a hyphen.
* @param token The token to check.
* @returns `true` if the token is a hyphen.
*/
function isHyphen(token) {
	return token != null && token.type === "Punctuator" && token.value === "-";
}
/**
* Check whether the given token is a colon.
* @param token The token to check.
* @returns `true` if the token is a colon.
*/
function isColon(token) {
	return token != null && token.type === "Punctuator" && token.value === ":";
}
/**
* Check whether the given token is a comma.
* @param token The token to check.
* @returns `true` if the token is a comma.
*/
function isComma(token) {
	return token != null && token.type === "Punctuator" && token.value === ",";
}
/**
* Checks if the given token is an opening square bracket token or not.
* @param token The token to check.
* @returns `true` if the token is an opening square bracket token.
*/
function isOpeningBracketToken(token) {
	return token != null && token.value === "[" && token.type === "Punctuator";
}
/**
* Checks if the given token is a closing square bracket token or not.
* @param token The token to check.
* @returns `true` if the token is a closing square bracket token.
*/
function isClosingBracketToken(token) {
	return token != null && token.value === "]" && token.type === "Punctuator";
}
/**
* Checks if the given token is an opening brace token or not.
* @param token The token to check.
* @returns `true` if the token is an opening brace token.
*/
function isOpeningBraceToken(token) {
	return token != null && token.value === "{" && token.type === "Punctuator";
}
/**
* Checks if the given token is a closing brace token or not.
* @param token The token to check.
* @returns `true` if the token is a closing brace token.
*/
function isClosingBraceToken(token) {
	return token != null && token.value === "}" && token.type === "Punctuator";
}

//#endregion
//#region src/rules/block-mapping-colon-indicator-newline.ts
var block_mapping_colon_indicator_newline_default = createRule("block-mapping-colon-indicator-newline", {
	meta: {
		docs: {
			description: "enforce consistent line breaks after `:` indicator",
			categories: ["standard"],
			extensionRule: false,
			layout: true
		},
		fixable: "whitespace",
		schema: [{ enum: ["always", "never"] }],
		messages: {
			unexpectedLinebreakAfterIndicator: "Unexpected line break after this `:` indicator.",
			expectedLinebreakAfterIndicator: "Expected a line break after this `:` indicator."
		},
		type: "layout"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const option = context.options[0] || "never";
		/**
		* Get the colon token from the given pair node.
		*/
		function getColonToken(pair) {
			const limitIndex = pair.key ? pair.key.range[1] : pair.range[0];
			let candidateColon = sourceCode.getTokenBefore(pair.value);
			while (candidateColon && !isColon(candidateColon)) {
				candidateColon = sourceCode.getTokenBefore(candidateColon);
				if (candidateColon && candidateColon.range[1] <= limitIndex) return null;
			}
			if (!candidateColon || !isColon(candidateColon)) return null;
			return candidateColon;
		}
		/**
		* Checks whether the newline between the given value node and the colon can be removed.
		*/
		function canRemoveNewline(value) {
			const node = value.type === "YAMLWithMeta" ? value.value : value;
			if (node && (node.type === "YAMLSequence" || node.type === "YAMLMapping") && node.style === "block") return false;
			return true;
		}
		return { YAMLMapping(node) {
			if (node.style !== "block") return;
			for (const pair of node.pairs) {
				const value = pair.value;
				if (!value) continue;
				const colon = getColonToken(pair);
				if (!colon) return;
				if (colon.loc.end.line < value.loc.start.line) {
					if (option === "never") {
						if (!canRemoveNewline(value)) return;
						context.report({
							loc: colon.loc,
							messageId: "unexpectedLinebreakAfterIndicator",
							fix(fixer) {
								const spaceCount = value.loc.start.column - colon.loc.end.column;
								if (spaceCount < 1 && value.loc.start.line < value.loc.end.line) return null;
								const spaces = " ".repeat(Math.max(spaceCount, 1));
								return fixer.replaceTextRange([colon.range[1], value.range[0]], spaces);
							}
						});
					}
				} else if (option === "always") context.report({
					loc: colon.loc,
					messageId: "expectedLinebreakAfterIndicator",
					fix(fixer) {
						const spaces = `\n${" ".repeat(value.loc.start.column)}`;
						return fixer.replaceTextRange([colon.range[1], value.range[0]], spaces);
					}
				});
			}
		} };
	}
});

//#endregion
//#region src/rules/block-mapping-question-indicator-newline.ts
var block_mapping_question_indicator_newline_default = createRule("block-mapping-question-indicator-newline", {
	meta: {
		docs: {
			description: "enforce consistent line breaks after `?` indicator",
			categories: ["standard"],
			extensionRule: false,
			layout: true
		},
		fixable: "whitespace",
		schema: [{ enum: ["always", "never"] }],
		messages: {
			unexpectedLinebreakAfterIndicator: "Unexpected line break after this `?` indicator.",
			expectedLinebreakAfterIndicator: "Expected a line break after this `?` indicator."
		},
		type: "layout"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const option = context.options[0] || "never";
		return { YAMLMapping(node) {
			if (node.style !== "block") return;
			for (const pair of node.pairs) {
				const key = pair.key;
				if (!key) continue;
				const question = sourceCode.getFirstToken(pair);
				if (!question || !isQuestion(question)) continue;
				if (question.loc.end.line < key.loc.start.line) {
					if (option === "never") context.report({
						loc: question.loc,
						messageId: "unexpectedLinebreakAfterIndicator",
						fix(fixer) {
							const spaceCount = key.loc.start.column - question.loc.end.column;
							if (spaceCount < 1 && key.loc.start.line < key.loc.end.line) return null;
							const spaces = " ".repeat(Math.max(spaceCount, 1));
							return fixer.replaceTextRange([question.range[1], key.range[0]], spaces);
						}
					});
				} else if (option === "always") context.report({
					loc: question.loc,
					messageId: "expectedLinebreakAfterIndicator",
					fix(fixer) {
						const spaces = `\n${" ".repeat(key.loc.start.column)}`;
						return fixer.replaceTextRange([question.range[1], key.range[0]], spaces);
					}
				});
			}
		} };
	}
});

//#endregion
//#region src/utils/yaml.ts
/**
* Check if you are using tabs for indentation.
* If you're using tabs, you're not sure if your YAML was parsed successfully, so almost all rules stop auto-fix.
*/
function hasTabIndent(context) {
	for (const line of context.sourceCode.getLines()) {
		if (/^\s*\t/u.test(line)) return true;
		if (/^\s*-\s*\t/u.test(line)) return true;
	}
	return false;
}
/**
* Calculate the required indentation for a given YAMLMapping pairs.
* Before calling this function, make sure that no flow style exists above the given mapping.
*/
function calcExpectIndentForPairs(mapping, context) {
	const sourceCode = context.sourceCode;
	let parentNode = mapping.parent;
	if (parentNode.type === "YAMLWithMeta") {
		const before = sourceCode.getTokenBefore(parentNode);
		if (before == null || before.loc.end.line < parentNode.loc.start.line) return calcExpectIndentFromBaseNode(parentNode, mapping.pairs[0], context);
		parentNode = parentNode.parent;
	}
	if (parentNode.type === "YAMLDocument") {
		const mappingIndent = getActualIndent(mapping, context);
		const firstPairIndent = getActualIndent(mapping.pairs[0], context);
		if (mappingIndent == null) return firstPairIndent;
		if (firstPairIndent != null && compareIndent(mappingIndent, firstPairIndent) < 0) return firstPairIndent;
		return mappingIndent;
	}
	if (parentNode.type === "YAMLSequence") {
		const hyphen = sourceCode.getTokenBefore(mapping);
		if (!isHyphen(hyphen)) return null;
		if (hyphen.loc.start.line === mapping.loc.start.line) {
			const hyphenIndent = getActualIndent(hyphen, context);
			if (hyphenIndent == null) return null;
			return `${hyphenIndent} ${sourceCode.text.slice(hyphen.range[1], mapping.range[0])}`;
		}
		return getActualIndent(mapping, context);
	}
	if (parentNode.type !== "YAMLPair") return null;
	return calcExpectIndentFromBaseNode(parentNode, mapping.pairs[0], context);
}
/**
* Calculate the required indentation for a given YAMLSequence entries.
*/
function calcExpectIndentForEntries(sequence, context) {
	const sourceCode = context.sourceCode;
	let parentNode = sequence.parent;
	if (parentNode.type === "YAMLWithMeta") {
		const before = sourceCode.getTokenBefore(parentNode);
		if (before == null || before.loc.end.line < parentNode.loc.start.line) return calcExpectIndentFromBaseNode(parentNode, sequence.entries[0], context);
		parentNode = parentNode.parent;
	}
	if (parentNode.type === "YAMLDocument") {
		const sequenceIndent = getActualIndent(sequence, context);
		const firstPairIndent = getActualIndent(sequence.entries[0], context);
		if (sequenceIndent == null) return firstPairIndent;
		if (firstPairIndent != null && compareIndent(sequenceIndent, firstPairIndent) < 0) return firstPairIndent;
		return sequenceIndent;
	}
	if (parentNode.type === "YAMLSequence") {
		const hyphen = sourceCode.getTokenBefore(sequence);
		if (!isHyphen(hyphen)) return null;
		if (hyphen.loc.start.line === sequence.loc.start.line) {
			const hyphenIndent = getActualIndent(hyphen, context);
			if (hyphenIndent == null) return null;
			return `${hyphenIndent} ${sourceCode.text.slice(hyphen.range[1], sequence.range[0])}`;
		}
		return getActualIndent(sequence, context);
	}
	if (parentNode.type !== "YAMLPair") return null;
	return calcExpectIndentFromBaseNode(parentNode, sequence.entries[0], context);
}
/**
* Calculate the required indentation from a given base node.
*/
function calcExpectIndentFromBaseNode(baseNode, node, context) {
	const baseIndent = getActualIndent(baseNode, context);
	if (baseIndent == null) return null;
	const indent = getActualIndent(node, context);
	if (indent != null && compareIndent(baseIndent, indent) < 0) return indent;
	return incIndent(baseIndent, context);
}
/**
* Get the actual indentation for a given node.
*/
function getActualIndent(node, context) {
	const before = context.sourceCode.getTokenBefore(node, { includeComments: true });
	if (!before || before.loc.end.line < node.loc.start.line) return getActualIndentFromLine(node.loc.start.line, context);
	return null;
}
/**
* Get the actual indentation for a given line.
*/
function getActualIndentFromLine(line, context) {
	const lineText = context.sourceCode.getLines()[line - 1];
	return /^[^\S\n\r\u2028\u2029]*/u.exec(lineText)[0];
}
/**
* Returns the indent that is incremented.
*/
function incIndent(indent, context) {
	const numOfIndent = getNumOfIndent(context);
	return `${indent}${numOfIndent === 2 ? "  " : numOfIndent === 4 ? "    " : " ".repeat(numOfIndent)}`;
}
/**
* Get the number of indentation offset
*/
function getNumOfIndent(context, optionValue) {
	const num = optionValue ?? context.settings?.yml?.indent;
	return num == null || num < 2 ? 2 : num;
}
/**
* Check if the indent is increasing.
*/
function compareIndent(a, b) {
	const minLen = Math.min(a.length, b.length);
	for (let index = 0; index < minLen; index++) if (a[index] !== b[index]) return NaN;
	return a.length > b.length ? 1 : a.length < b.length ? -1 : 0;
}
/**
* Check if the given node is key node.
*/
function isKeyNode(node) {
	if (node.parent.type === "YAMLWithMeta") return isKeyNode(node.parent);
	return node.parent.type === "YAMLPair" && node.parent.key === node;
}
/**
* Unwrap meta
*/
function unwrapMeta(node) {
	if (!node) return node;
	if (node.type === "YAMLWithMeta") return node.value;
	return node;
}
/**
* Adjust indent
*/
function* processIndentFix(fixer, baseIndent, targetNode, context) {
	const sourceCode = context.sourceCode;
	if (targetNode.type === "YAMLWithMeta") {
		yield* metaIndent(targetNode);
		return;
	}
	if (targetNode.type === "YAMLPair") {
		yield* pairIndent(targetNode);
		return;
	}
	yield* contentIndent(targetNode);
	/**
	* for YAMLContent
	*/
	function* contentIndent(contentNode) {
		const actualIndent = getActualIndent(contentNode, context);
		if (actualIndent != null && compareIndent(baseIndent, actualIndent) < 0) return;
		let nextBaseIndent = baseIndent;
		const expectValueIndent = incIndent(baseIndent, context);
		if (actualIndent != null) {
			yield fixIndent(fixer, sourceCode, expectValueIndent, contentNode);
			nextBaseIndent = expectValueIndent;
		}
		if (contentNode.type === "YAMLMapping") {
			for (const p of contentNode.pairs) yield* processIndentFix(fixer, nextBaseIndent, p, context);
			if (contentNode.style === "flow") {
				const close = sourceCode.getLastToken(contentNode);
				if (close.value === "}") {
					const closeActualIndent = getActualIndent(close, context);
					if (closeActualIndent != null && compareIndent(closeActualIndent, nextBaseIndent) < 0) yield fixIndent(fixer, sourceCode, nextBaseIndent, close);
				}
			}
		} else if (contentNode.type === "YAMLSequence") for (const e of contentNode.entries) {
			if (!e) continue;
			yield* processIndentFix(fixer, nextBaseIndent, e, context);
		}
	}
	/**
	* for YAMLWithMeta
	*/
	function* metaIndent(metaNode) {
		let nextBaseIndent = baseIndent;
		const actualIndent = getActualIndent(metaNode, context);
		if (actualIndent != null) if (compareIndent(baseIndent, actualIndent) < 0) nextBaseIndent = actualIndent;
		else {
			const expectMetaIndent = incIndent(baseIndent, context);
			yield fixIndent(fixer, sourceCode, expectMetaIndent, metaNode);
			nextBaseIndent = expectMetaIndent;
		}
		if (metaNode.value) yield* processIndentFix(fixer, nextBaseIndent, metaNode.value, context);
	}
	/**
	* for YAMLPair
	*/
	function* pairIndent(pairNode) {
		let nextBaseIndent = baseIndent;
		const actualIndent = getActualIndent(pairNode, context);
		if (actualIndent != null) if (compareIndent(baseIndent, actualIndent) < 0) nextBaseIndent = actualIndent;
		else {
			const expectKeyIndent = incIndent(baseIndent, context);
			yield fixIndent(fixer, sourceCode, expectKeyIndent, pairNode);
			nextBaseIndent = expectKeyIndent;
		}
		if (pairNode.value) yield* processIndentFix(fixer, nextBaseIndent, pairNode.value, context);
	}
}
/**
* Fix indent
*/
function fixIndent(fixer, sourceCode, indent, node) {
	const prevToken = sourceCode.getTokenBefore(node, { includeComments: true });
	return fixer.replaceTextRange([prevToken.range[1], node.range[0]], `\n${indent}`);
}

//#endregion
//#region src/rules/block-mapping.ts
const OPTIONS_ENUM$1 = [
	"always",
	"never",
	"ignore"
];
/**
* Parse options
*/
function parseOptions$5(option) {
	const opt = {
		singleline: "ignore",
		multiline: "always"
	};
	if (option) if (typeof option === "string") {
		opt.singleline = option;
		opt.multiline = option;
	} else {
		if (typeof option.singleline === "string") opt.singleline = option.singleline;
		if (typeof option.multiline === "string") opt.multiline = option.multiline;
	}
	return opt;
}
var block_mapping_default = createRule("block-mapping", {
	meta: {
		docs: {
			description: "require or disallow block style mappings.",
			categories: ["standard"],
			extensionRule: false,
			layout: false
		},
		fixable: "code",
		schema: [{ anyOf: [{ enum: ["always", "never"] }, {
			type: "object",
			properties: {
				singleline: { enum: OPTIONS_ENUM$1 },
				multiline: { enum: OPTIONS_ENUM$1 }
			},
			additionalProperties: false
		}] }],
		messages: {
			required: "Must use block style mappings.",
			disallow: "Must use flow style mappings."
		},
		type: "layout"
	},
	create(context) {
		if (!context.sourceCode.parserServices?.isYAML) return {};
		const options = parseOptions$5(context.options[0]);
		let styleStack = null;
		/**
		* Moves the stack down.
		*/
		function downStack(node) {
			if (styleStack) {
				if (node.style === "flow") styleStack.hasFlowStyle = true;
				else if (node.style === "block") styleStack.hasBlockStyle = true;
			}
			styleStack = {
				upper: styleStack,
				node,
				flowStyle: node.style === "flow",
				blockStyle: node.style === "block",
				withinFlowStyle: styleStack && (styleStack.withinFlowStyle || styleStack.flowStyle) || false,
				withinBlockStyle: styleStack && (styleStack.withinBlockStyle || styleStack.blockStyle) || false
			};
		}
		/**
		* Moves the stack up.
		*/
		function upStack() {
			if (styleStack && styleStack.upper) {
				styleStack.upper.hasNullPair = styleStack.upper.hasNullPair || styleStack.hasNullPair;
				styleStack.upper.hasBlockLiteralOrFolded = styleStack.upper.hasBlockLiteralOrFolded || styleStack.hasBlockLiteralOrFolded;
				styleStack.upper.hasBlockStyle = styleStack.upper.hasBlockStyle || styleStack.hasBlockStyle;
				styleStack.upper.hasFlowStyle = styleStack.upper.hasFlowStyle || styleStack.hasFlowStyle;
			}
			styleStack = styleStack && styleStack.upper;
		}
		return {
			YAMLSequence: downStack,
			YAMLMapping: downStack,
			YAMLPair(node) {
				if (node.key == null || node.value == null) styleStack.hasNullPair = true;
			},
			YAMLScalar(node) {
				if (styleStack && (node.style === "folded" || node.style === "literal")) styleStack.hasBlockLiteralOrFolded = true;
			},
			"YAMLSequence:exit": upStack,
			"YAMLMapping:exit"(node) {
				const mappingInfo = styleStack;
				upStack();
				if (node.pairs.length === 0) return;
				const optionType = node.loc.start.line < node.loc.end.line ? options.multiline : options.singleline;
				if (optionType === "ignore") return;
				if (node.style === "flow") {
					if (optionType === "never") return;
					if (isKeyNode(node)) return;
					const canFix = canFixToBlock$1(mappingInfo, node) && !hasTabIndent(context);
					context.report({
						loc: node.loc,
						messageId: "required",
						fix: canFix && buildFixFlowToBlock$1(node, context) || null
					});
				} else if (node.style === "block") {
					if (optionType === "always") return;
					const canFix = canFixToFlow$1(mappingInfo, node) && !hasTabIndent(context);
					context.report({
						loc: node.loc,
						messageId: "disallow",
						fix: canFix && buildFixBlockToFlow$1(node, context) || null
					});
				}
			}
		};
	}
});
/**
* Check if it can be converted to block style.
*/
function canFixToBlock$1(mappingInfo, node) {
	if (mappingInfo.hasNullPair || mappingInfo.hasBlockLiteralOrFolded) return false;
	if (mappingInfo.withinFlowStyle) return false;
	for (const pair of node.pairs) {
		const key = pair.key;
		if (key.loc.start.line < key.loc.end.line) return false;
	}
	return true;
}
/**
* Check if it can be converted to flow style.
*/
function canFixToFlow$1(mappingInfo, node) {
	if (mappingInfo.hasNullPair || mappingInfo.hasBlockLiteralOrFolded) return false;
	if (mappingInfo.hasBlockStyle) return false;
	for (const pair of node.pairs) {
		const value = unwrapMeta(pair.value);
		const key = unwrapMeta(pair.key);
		if (value && value.type === "YAMLScalar" && value.style === "plain") {
			if (value.loc.start.line < value.loc.end.line) return false;
			if (/[[\]{}]/u.test(value.strValue)) return false;
			if (value.strValue.includes(",")) return false;
		}
		if (key && key.type === "YAMLScalar" && key.style === "plain") {
			if (/[[\]{]/u.test(key.strValue)) return false;
			if (/[,}]/u.test(key.strValue)) return false;
		}
	}
	return true;
}
/**
* Build the fixer function that makes the flow style to block style.
*/
function buildFixFlowToBlock$1(node, context) {
	return function* (fixer) {
		const sourceCode = context.sourceCode;
		const open = sourceCode.getFirstToken(node);
		const close = sourceCode.getLastToken(node);
		if (open?.value !== "{" || close?.value !== "}") return;
		const expectIndent = calcExpectIndentForPairs(node, context);
		if (expectIndent == null) return;
		const openPrevToken = sourceCode.getTokenBefore(open, { includeComments: true });
		if (!openPrevToken) yield fixer.removeRange([sourceCode.ast.range[0], open.range[1]]);
		else if (openPrevToken.loc.end.line < open.loc.start.line) yield fixer.removeRange([openPrevToken.range[1], open.range[1]]);
		else yield fixer.remove(open);
		let prev = open;
		for (const pair of node.pairs) {
			const prevToken = sourceCode.getTokenBefore(pair, {
				includeComments: true,
				filter: (token) => !isComma(token)
			});
			yield* removeComma(prev, prevToken);
			yield fixer.replaceTextRange([prevToken.range[1], pair.range[0]], `\n${expectIndent}`);
			const colonToken = sourceCode.getTokenAfter(pair.key, isColon);
			if (colonToken.range[1] === sourceCode.getTokenAfter(colonToken, { includeComments: true }).range[0]) yield fixer.insertTextAfter(colonToken, " ");
			yield* processIndentFix(fixer, expectIndent, pair.value, context);
			prev = pair;
		}
		yield* removeComma(prev, close);
		yield fixer.remove(close);
		/**
		* Remove between commas
		*/
		function* removeComma(a, b) {
			for (const token of sourceCode.getTokensBetween(a, b, { includeComments: true })) if (isComma(token)) yield fixer.remove(token);
		}
	};
}
/**
* Build the fixer function that makes the block style to flow style.
*/
function buildFixBlockToFlow$1(node, _context) {
	return function* (fixer) {
		yield fixer.insertTextBefore(node, "{");
		const pairs = [...node.pairs];
		const lastPair = pairs.pop();
		for (const pair of pairs) yield fixer.insertTextAfter(pair, ",");
		yield fixer.insertTextAfter(lastPair || node, "}");
	};
}

//#endregion
//#region src/rules/block-sequence-hyphen-indicator-newline.ts
var block_sequence_hyphen_indicator_newline_default = createRule("block-sequence-hyphen-indicator-newline", {
	meta: {
		docs: {
			description: "enforce consistent line breaks after `-` indicator",
			categories: ["standard"],
			extensionRule: false,
			layout: true
		},
		fixable: "whitespace",
		schema: [{ enum: ["always", "never"] }, {
			type: "object",
			properties: {
				nestedHyphen: { enum: ["always", "never"] },
				blockMapping: { enum: ["always", "never"] }
			},
			additionalProperties: false
		}],
		messages: {
			unexpectedLinebreakAfterIndicator: "Unexpected line break after this `-` indicator.",
			expectedLinebreakAfterIndicator: "Expected a line break after this `-` indicator."
		},
		type: "layout"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const style = context.options[0] || "never";
		const nestedHyphenStyle = context.options[1]?.nestedHyphen || "always";
		const blockMappingStyle = context.options[1]?.blockMapping || style;
		/**
		* Get style from given hyphen
		*/
		function getStyleOption(hyphen, entry) {
			const next = sourceCode.getTokenAfter(hyphen);
			if (next && isHyphen(next)) return nestedHyphenStyle;
			if (entry.type === "YAMLMapping" && entry.style === "block") return blockMappingStyle;
			return style;
		}
		return { YAMLSequence(node) {
			if (node.style !== "block") return;
			for (const entry of node.entries) {
				if (!entry) continue;
				const hyphen = sourceCode.getTokenBefore(entry);
				if (!hyphen) continue;
				if (hyphen.loc.end.line < entry.loc.start.line) {
					if (getStyleOption(hyphen, entry) === "never") context.report({
						loc: hyphen.loc,
						messageId: "unexpectedLinebreakAfterIndicator",
						fix(fixer) {
							const spaceCount = entry.loc.start.column - hyphen.loc.end.column;
							if (spaceCount < 1 && entry.loc.start.line < entry.loc.end.line) return null;
							const spaces = " ".repeat(Math.max(spaceCount, 1));
							return fixer.replaceTextRange([hyphen.range[1], entry.range[0]], spaces);
						}
					});
				} else if (getStyleOption(hyphen, entry) === "always") context.report({
					loc: hyphen.loc,
					messageId: "expectedLinebreakAfterIndicator",
					fix(fixer) {
						const spaces = `\n${" ".repeat(entry.loc.start.column)}`;
						return fixer.replaceTextRange([hyphen.range[1], entry.range[0]], spaces);
					}
				});
			}
		} };
	}
});

//#endregion
//#region src/rules/block-sequence.ts
const OPTIONS_ENUM = [
	"always",
	"never",
	"ignore"
];
/**
* Parse options
*/
function parseOptions$4(option) {
	const opt = {
		singleline: "ignore",
		multiline: "always"
	};
	if (option) if (typeof option === "string") {
		opt.singleline = option;
		opt.multiline = option;
	} else {
		if (typeof option.singleline === "string") opt.singleline = option.singleline;
		if (typeof option.multiline === "string") opt.multiline = option.multiline;
	}
	return opt;
}
var block_sequence_default = createRule("block-sequence", {
	meta: {
		docs: {
			description: "require or disallow block style sequences.",
			categories: ["standard"],
			extensionRule: false,
			layout: false
		},
		fixable: "code",
		schema: [{ anyOf: [{ enum: ["always", "never"] }, {
			type: "object",
			properties: {
				singleline: { enum: OPTIONS_ENUM },
				multiline: { enum: OPTIONS_ENUM }
			},
			additionalProperties: false
		}] }],
		messages: {
			required: "Must use block style sequences.",
			disallow: "Must use flow style sequences."
		},
		type: "layout"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const options = parseOptions$4(context.options[0]);
		let styleStack = null;
		/**
		* Moves the stack down.
		*/
		function downStack(node) {
			if (styleStack) {
				if (node.style === "flow") styleStack.hasFlowStyle = true;
				else if (node.style === "block") styleStack.hasBlockStyle = true;
			}
			styleStack = {
				upper: styleStack,
				node,
				flowStyle: node.style === "flow",
				blockStyle: node.style === "block",
				withinFlowStyle: styleStack && (styleStack.withinFlowStyle || styleStack.flowStyle) || false,
				withinBlockStyle: styleStack && (styleStack.withinBlockStyle || styleStack.blockStyle) || false
			};
		}
		/**
		* Moves the stack up.
		*/
		function upStack() {
			if (styleStack && styleStack.upper) {
				styleStack.upper.hasNullPair = styleStack.upper.hasNullPair || styleStack.hasNullPair;
				styleStack.upper.hasBlockLiteralOrFolded = styleStack.upper.hasBlockLiteralOrFolded || styleStack.hasBlockLiteralOrFolded;
				styleStack.upper.hasBlockStyle = styleStack.upper.hasBlockStyle || styleStack.hasBlockStyle;
				styleStack.upper.hasFlowStyle = styleStack.upper.hasFlowStyle || styleStack.hasFlowStyle;
			}
			styleStack = styleStack && styleStack.upper;
		}
		return {
			YAMLMapping: downStack,
			YAMLSequence: downStack,
			YAMLPair(node) {
				if (node.key == null || node.value == null) styleStack.hasNullPair = true;
			},
			YAMLScalar(node) {
				if (styleStack && (node.style === "folded" || node.style === "literal")) styleStack.hasBlockLiteralOrFolded = true;
			},
			"YAMLMapping:exit": upStack,
			"YAMLSequence:exit"(node) {
				const sequenceInfo = styleStack;
				upStack();
				if (node.entries.length === 0) return;
				const optionType = node.loc.start.line < node.loc.end.line ? options.multiline : options.singleline;
				if (optionType === "ignore") return;
				if (node.style === "flow") {
					if (optionType === "never") return;
					if (isKeyNode(node)) return;
					const canFix = canFixToBlock(sequenceInfo, node, sourceCode) && !hasTabIndent(context);
					context.report({
						loc: node.loc,
						messageId: "required",
						fix: canFix && buildFixFlowToBlock(node, context) || null
					});
				} else if (node.style === "block") {
					if (optionType === "always") return;
					const canFix = canFixToFlow(sequenceInfo, node, context) && !hasTabIndent(context);
					context.report({
						loc: node.loc,
						messageId: "disallow",
						fix: canFix && buildFixBlockToFlow(node, context) || null
					});
				}
			}
		};
	}
});
/**
* Check if it can be converted to block style.
*/
function canFixToBlock(sequenceInfo, node, sourceCode) {
	if (sequenceInfo.hasNullPair || sequenceInfo.hasBlockLiteralOrFolded) return false;
	if (sequenceInfo.withinFlowStyle) return false;
	for (const entry of node.entries) if (entry.type === "YAMLMapping" && entry.style === "block") for (const pair of entry.pairs) {
		if (pair.key) {
			if (pair.key.loc.start.line < pair.key.loc.end.line) return false;
			if (pair.key.type === "YAMLMapping") return false;
		}
		if (pair.value) {
			const colon = sourceCode.getTokenBefore(pair.value);
			if (colon?.value === ":") {
				if (colon.range[1] === pair.value.range[0]) return false;
			}
		}
	}
	return true;
}
/**
* Check if it can be converted to flow style.
*/
function canFixToFlow(sequenceInfo, node, context) {
	if (sequenceInfo.hasNullPair || sequenceInfo.hasBlockLiteralOrFolded) return false;
	if (sequenceInfo.hasBlockStyle) return false;
	if (node.parent.type === "YAMLWithMeta") {
		const metaIndent = getActualIndent(node.parent, context);
		if (metaIndent != null) {
			for (let line = node.loc.start.line; line <= node.loc.end.line; line++) if (compareIndent(metaIndent, getActualIndentFromLine(line, context)) > 0) return false;
		}
	}
	for (const entry of node.entries) {
		const value = unwrapMeta(entry);
		if (value && value.type === "YAMLScalar" && value.style === "plain") {
			if (value.strValue.includes(",")) return false;
		}
	}
	return true;
}
/**
* Build the fixer function that makes the flow style to block style.
*/
function buildFixFlowToBlock(node, context) {
	return function* (fixer) {
		const sourceCode = context.sourceCode;
		const open = sourceCode.getFirstToken(node);
		const close = sourceCode.getLastToken(node);
		if (open?.value !== "[" || close?.value !== "]") return;
		const expectIndent = calcExpectIndentForEntries(node, context);
		if (expectIndent == null) return;
		const openPrevToken = sourceCode.getTokenBefore(open, { includeComments: true });
		if (!openPrevToken) yield fixer.removeRange([sourceCode.ast.range[0], open.range[1]]);
		else if (openPrevToken.loc.end.line < open.loc.start.line) yield fixer.removeRange([openPrevToken.range[1], open.range[1]]);
		else yield fixer.remove(open);
		let prev = open;
		for (const entry of node.entries) {
			const prevToken = sourceCode.getTokenBefore(entry, {
				includeComments: true,
				filter: (token) => !isComma(token)
			});
			yield* removeComma(prev, prevToken);
			yield fixer.replaceTextRange([prevToken.range[1], entry.range[0]], `\n${expectIndent}- `);
			yield* processEntryIndent(`${expectIndent}  `, entry);
			prev = entry;
		}
		yield* removeComma(prev, close);
		yield fixer.remove(close);
		/**
		* Remove between commas
		*/
		function* removeComma(a, b) {
			for (const token of sourceCode.getTokensBetween(a, b, { includeComments: true })) if (isComma(token)) yield fixer.remove(token);
		}
		/**
		* Indent
		*/
		function* processEntryIndent(baseIndent, entry) {
			if (entry.type === "YAMLWithMeta" && entry.value) yield* processIndentFix(fixer, baseIndent, entry.value, context);
			else if (entry.type === "YAMLMapping") {
				for (const p of entry.pairs) if (p.range[0] === entry.range[0]) {
					if (p.value) yield* processIndentFix(fixer, baseIndent, p.value, context);
				} else yield* processIndentFix(fixer, baseIndent, p, context);
				if (entry.style === "flow") {
					const close = sourceCode.getLastToken(entry);
					if (close.value === "}") {
						const actualIndent = getActualIndent(close, context);
						if (actualIndent != null && compareIndent(actualIndent, baseIndent) < 0) yield fixIndent(fixer, sourceCode, baseIndent, close);
					}
				}
			} else if (entry.type === "YAMLSequence") for (const e of entry.entries) {
				if (!e) continue;
				yield* processIndentFix(fixer, baseIndent, e, context);
			}
		}
	};
}
/**
* Build the fixer function that makes the block style to flow style.
*/
function buildFixBlockToFlow(node, context) {
	const sourceCode = context.sourceCode;
	return function* (fixer) {
		const entries = node.entries.filter((e) => e != null);
		if (entries.length !== node.entries.length) return;
		const firstEntry = entries.shift();
		const lastEntry = entries.pop();
		const firstHyphen = sourceCode.getTokenBefore(firstEntry);
		yield fixer.replaceText(firstHyphen, " ");
		yield fixer.insertTextBefore(firstEntry, "[");
		if (lastEntry) yield fixer.insertTextAfter(firstEntry, ",");
		for (const entry of entries) {
			const hyphen = sourceCode.getTokenBefore(entry);
			yield fixer.replaceText(hyphen, " ");
			yield fixer.insertTextAfter(entry, ",");
		}
		if (lastEntry) {
			const lastHyphen = sourceCode.getTokenBefore(lastEntry);
			yield fixer.replaceText(lastHyphen, " ");
		}
		yield fixer.insertTextAfter(lastEntry || firstEntry || node, "]");
	};
}

//#endregion
//#region src/rules/file-extension.ts
var file_extension_default = createRule("file-extension", {
	meta: {
		docs: {
			description: "enforce YAML file extension",
			categories: [],
			extensionRule: false,
			layout: false
		},
		schema: [{
			type: "object",
			properties: {
				extension: { enum: ["yaml", "yml"] },
				caseSensitive: { type: "boolean" }
			},
			additionalProperties: false
		}],
		messages: { unexpected: `Expected extension '{{expected}}' but used extension '{{actual}}'.` },
		type: "suggestion"
	},
	create(context) {
		if (!context.sourceCode.parserServices?.isYAML) return {};
		const expected = context.options[0]?.extension || "yaml";
		const caseSensitive = context.options[0]?.caseSensitive ?? true;
		return { Program(node) {
			const filename = context.filename;
			const actual = path.extname(filename);
			if ((caseSensitive ? actual : actual.toLocaleLowerCase()) === `.${expected}`) return;
			context.report({
				node,
				loc: node.loc.start,
				messageId: "unexpected",
				data: {
					expected: `.${expected}`,
					actual
				}
			});
		} };
	}
});

//#endregion
//#region src/rules/flow-mapping-curly-newline.ts
const OPTION_VALUE = { oneOf: [{ enum: ["always", "never"] }, {
	type: "object",
	properties: {
		multiline: { type: "boolean" },
		minProperties: {
			type: "integer",
			minimum: 0
		},
		consistent: { type: "boolean" }
	},
	additionalProperties: false,
	minProperties: 1
}] };
/**
* Normalizes a given option value.
*/
function normalizeOptionValue(value) {
	let multiline = false;
	let minProperties = Number.POSITIVE_INFINITY;
	let consistent = false;
	if (value) if (value === "always") minProperties = 0;
	else if (value === "never") minProperties = Number.POSITIVE_INFINITY;
	else {
		multiline = Boolean(value.multiline);
		minProperties = value.minProperties || Number.POSITIVE_INFINITY;
		consistent = Boolean(value.consistent);
	}
	else consistent = true;
	return {
		multiline,
		minProperties,
		consistent
	};
}
/**
* Determines if ObjectExpression, ObjectPattern, ImportDeclaration or ExportNamedDeclaration
* node needs to be checked for missing line breaks
* @param {ASTNode} node Node under inspection
* @param {Object} options option specific to node type
* @param {Token} first First object property
* @param {Token} last Last object property
* @returns {boolean} `true` if node needs to be checked for missing line breaks
*/
function areLineBreaksRequired(node, options, first, last) {
	const objectProperties = node.pairs;
	return objectProperties.length >= options.minProperties || options.multiline && objectProperties.length > 0 && first.loc.start.line !== last.loc.end.line;
}
var flow_mapping_curly_newline_default = createRule("flow-mapping-curly-newline", {
	meta: {
		docs: {
			description: "enforce consistent line breaks inside braces",
			categories: ["standard"],
			extensionRule: "object-curly-newline",
			layout: true
		},
		fixable: "whitespace",
		schema: [OPTION_VALUE],
		messages: {
			unexpectedLinebreakBeforeClosingBrace: "Unexpected line break before this closing brace.",
			unexpectedLinebreakAfterOpeningBrace: "Unexpected line break after this opening brace.",
			expectedLinebreakBeforeClosingBrace: "Expected a line break before this closing brace.",
			expectedLinebreakAfterOpeningBrace: "Expected a line break after this opening brace."
		},
		type: "layout"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const options = normalizeOptionValue(context.options[0]);
		/**
		* Reports a given node if it violated this rule.
		* @param {ASTNode} node A node to check. This is an ObjectExpression, ObjectPattern, ImportDeclaration or ExportNamedDeclaration node.
		* @returns {void}
		*/
		function check(node) {
			if (isKeyNode(node)) return;
			const openBrace = sourceCode.getFirstToken(node, (token) => token.value === "{");
			const closeBrace = sourceCode.getLastToken(node, (token) => token.value === "}");
			let first = sourceCode.getTokenAfter(openBrace, { includeComments: true });
			let last = sourceCode.getTokenBefore(closeBrace, { includeComments: true });
			const needsLineBreaks = areLineBreaksRequired(node, options, first, last);
			const hasCommentsFirstToken = isCommentToken(first);
			const hasCommentsLastToken = isCommentToken(last);
			const hasQuestionsLastToken = isQuestion(last);
			first = sourceCode.getTokenAfter(openBrace);
			last = sourceCode.getTokenBefore(closeBrace);
			if (needsLineBreaks) {
				if (isTokenOnSameLine(openBrace, first)) context.report({
					messageId: "expectedLinebreakAfterOpeningBrace",
					node,
					loc: openBrace.loc,
					fix(fixer) {
						if (hasCommentsFirstToken || hasTabIndent(context)) return null;
						const indent = incIndent(getActualIndentFromLine(openBrace.loc.start.line, context), context);
						return fixer.insertTextAfter(openBrace, `\n${indent}`);
					}
				});
				if (isTokenOnSameLine(last, closeBrace)) context.report({
					messageId: "expectedLinebreakBeforeClosingBrace",
					node,
					loc: closeBrace.loc,
					fix(fixer) {
						if (hasCommentsLastToken || hasTabIndent(context)) return null;
						const indent = getActualIndentFromLine(closeBrace.loc.start.line, context);
						return fixer.insertTextBefore(closeBrace, `\n${indent}`);
					}
				});
			} else {
				const consistent = options.consistent;
				const hasLineBreakBetweenOpenBraceAndFirst = !isTokenOnSameLine(openBrace, first);
				const hasLineBreakBetweenCloseBraceAndLast = !isTokenOnSameLine(last, closeBrace);
				if (!consistent && hasLineBreakBetweenOpenBraceAndFirst || consistent && hasLineBreakBetweenOpenBraceAndFirst && !hasLineBreakBetweenCloseBraceAndLast) context.report({
					messageId: "unexpectedLinebreakAfterOpeningBrace",
					node,
					loc: openBrace.loc,
					fix(fixer) {
						if (hasCommentsFirstToken || hasTabIndent(context)) return null;
						return fixer.removeRange([openBrace.range[1], first.range[0]]);
					}
				});
				if (!consistent && hasLineBreakBetweenCloseBraceAndLast || consistent && !hasLineBreakBetweenOpenBraceAndFirst && hasLineBreakBetweenCloseBraceAndLast) {
					if (hasQuestionsLastToken) return;
					context.report({
						messageId: "unexpectedLinebreakBeforeClosingBrace",
						node,
						loc: closeBrace.loc,
						fix(fixer) {
							if (hasCommentsLastToken || hasTabIndent(context)) return null;
							return fixer.removeRange([last.range[1], closeBrace.range[0]]);
						}
					});
				}
			}
		}
		return { YAMLMapping(node) {
			if (node.style === "flow") check(node);
		} };
	}
});

//#endregion
//#region src/rules/flow-mapping-curly-spacing.ts
/**
* Parse rule options and return helpers for spacing checks.
* @param options The options tuple from the rule configuration.
* @param sourceCode The sourceCode object for node lookup.
*/
function parseOptions$3(options, sourceCode) {
	const spaced = options[0] ?? "never";
	/**
	* Determines whether an exception option is set relative to the base spacing.
	* @param option The option to check.
	*/
	function isOptionSet(option) {
		return options[1] ? options[1][option] === (spaced === "never") : false;
	}
	const arraysInObjectsException = isOptionSet("arraysInObjects");
	const objectsInObjectsException = isOptionSet("objectsInObjects");
	const emptyObjects = options[1]?.emptyObjects ?? "ignore";
	/**
	* Whether the opening brace must be spaced, considering exceptions.
	* @param spaced The primary spaced option string.
	* @param second The token after the opening brace.
	*/
	function isOpeningCurlyBraceMustBeSpaced(spaced, second) {
		const targetPenultimateType = arraysInObjectsException && isOpeningBracketToken(second) ? "YAMLSequence" : objectsInObjectsException && isOpeningBraceToken(second) ? "YAMLMapping" : null;
		const node = sourceCode.getNodeByRangeIndex(second.range[0]);
		return targetPenultimateType && node?.type === targetPenultimateType ? spaced === "never" : spaced === "always";
	}
	/**
	* Whether the closing brace must be spaced, considering exceptions.
	* @param spaced The primary spaced option string.
	* @param penultimate The token before the closing brace.
	*/
	function isClosingCurlyBraceMustBeSpaced(spaced, penultimate) {
		const targetPenultimateType = arraysInObjectsException && isClosingBracketToken(penultimate) ? "YAMLSequence" : objectsInObjectsException && isClosingBraceToken(penultimate) ? "YAMLMapping" : null;
		const node = sourceCode.getNodeByRangeIndex(penultimate.range[0]);
		return targetPenultimateType && node?.type === targetPenultimateType ? spaced === "never" : spaced === "always";
	}
	return {
		spaced,
		emptyObjects,
		isOpeningCurlyBraceMustBeSpaced,
		isClosingCurlyBraceMustBeSpaced
	};
}
var flow_mapping_curly_spacing_default = createRule("flow-mapping-curly-spacing", {
	meta: {
		docs: {
			description: "enforce consistent spacing inside braces",
			categories: ["standard"],
			extensionRule: "object-curly-spacing",
			layout: true
		},
		type: "layout",
		fixable: "whitespace",
		schema: [{
			type: "string",
			enum: ["always", "never"]
		}, {
			type: "object",
			properties: {
				arraysInObjects: { type: "boolean" },
				objectsInObjects: { type: "boolean" },
				emptyObjects: {
					type: "string",
					enum: [
						"ignore",
						"always",
						"never"
					]
				}
			},
			additionalProperties: false
		}],
		messages: {
			requireSpaceBefore: "A space is required before '{{token}}'.",
			requireSpaceAfter: "A space is required after '{{token}}'.",
			unexpectedSpaceBefore: "There should be no space before '{{token}}'.",
			unexpectedSpaceAfter: "There should be no space after '{{token}}'.",
			requiredSpaceInEmptyObject: "A space is required in empty flow mapping.",
			unexpectedSpaceInEmptyObject: "There should be no space in empty flow mapping."
		}
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const options = parseOptions$3(context.options, sourceCode);
		/**
		* Reports that there shouldn't be a space after the first token
		* @param node The node to report in the event of an error.
		* @param token The token to use for the report.
		*/
		function reportNoBeginningSpace(node, token) {
			const nextToken = sourceCode.getTokenAfter(token, { includeComments: true });
			context.report({
				node,
				loc: {
					start: token.loc.end,
					end: nextToken.loc.start
				},
				messageId: "unexpectedSpaceAfter",
				data: { token: token.value },
				fix(fixer) {
					return fixer.removeRange([token.range[1], nextToken.range[0]]);
				}
			});
		}
		/**
		* Reports that there shouldn't be a space before the last token
		* @param node The node to report in the event of an error.
		* @param token The token to use for the report.
		*/
		function reportNoEndingSpace(node, token) {
			const previousToken = sourceCode.getTokenBefore(token, { includeComments: true });
			context.report({
				node,
				loc: {
					start: previousToken.loc.end,
					end: token.loc.start
				},
				messageId: "unexpectedSpaceBefore",
				data: { token: token.value },
				fix(fixer) {
					return fixer.removeRange([previousToken.range[1], token.range[0]]);
				}
			});
		}
		/**
		* Reports that there should be a space after the first token
		* @param node The node to report in the event of an error.
		* @param token The token to use for the report.
		*/
		function reportRequiredBeginningSpace(node, token) {
			context.report({
				node,
				loc: token.loc,
				messageId: "requireSpaceAfter",
				data: { token: token.value },
				fix(fixer) {
					return fixer.insertTextAfter(token, " ");
				}
			});
		}
		/**
		* Reports that there should be a space before the last token
		* @param node The node to report in the event of an error.
		* @param token The token to use for the report.
		*/
		function reportRequiredEndingSpace(node, token) {
			context.report({
				node,
				loc: token.loc,
				messageId: "requireSpaceBefore",
				data: { token: token.value },
				fix(fixer) {
					return fixer.insertTextBefore(token, " ");
				}
			});
		}
		/**
		* Determines if spacing in curly braces is valid.
		* @param node The AST node to check.
		* @param first The first token to check (should be the opening brace)
		* @param second The second token to check (should be first after the opening brace)
		* @param penultimate The penultimate token to check (should be last before closing brace)
		* @param last The last token to check (should be closing brace)
		*/
		function validateBraceSpacing(node, spaced, openingToken, second, penultimate, closingToken) {
			if (isTokenOnSameLine(openingToken, second)) {
				const firstSpaced = sourceCode.isSpaceBetween(openingToken, second);
				if (options.isOpeningCurlyBraceMustBeSpaced(spaced, second)) {
					if (!firstSpaced) reportRequiredBeginningSpace(node, openingToken);
				} else if (firstSpaced && second.type !== "Line") reportNoBeginningSpace(node, openingToken);
			}
			if (isTokenOnSameLine(penultimate, closingToken)) {
				const lastSpaced = sourceCode.isSpaceBetween(penultimate, closingToken);
				if (options.isClosingCurlyBraceMustBeSpaced(spaced, penultimate)) {
					if (!lastSpaced) reportRequiredEndingSpace(node, closingToken);
				} else if (lastSpaced) reportNoEndingSpace(node, closingToken);
			}
		}
		/**
		* Gets '}' token of an object node.
		*
		* Because the last token of object patterns might be a type annotation,
		* this traverses tokens preceded by the last property, then returns the
		* first '}' token.
		* @param node The node to get. This node is an
		*      ObjectExpression or an ObjectPattern. And this node has one or
		*      more properties.
		* @returns '}' token.
		*/
		function getClosingBraceOfObject(node) {
			const lastProperty = node.pairs[node.pairs.length - 1];
			return sourceCode.getTokenAfter(lastProperty, isClosingBraceToken);
		}
		/**
		* Reports a given object node if spacing in curly braces is invalid.
		* @param node An ObjectExpression or ObjectPattern node to check.
		*/
		function checkSpaceInEmptyObject(node) {
			if (options.emptyObjects === "ignore") return;
			const openingToken = sourceCode.getFirstToken(node);
			const closingToken = sourceCode.getLastToken(node);
			const second = sourceCode.getTokenAfter(openingToken, { includeComments: true });
			if (second !== closingToken && isCommentToken(second)) {
				const penultimate = sourceCode.getTokenBefore(closingToken, { includeComments: true });
				validateBraceSpacing(node, options.emptyObjects, openingToken, second, penultimate, closingToken);
				return;
			}
			if (!isTokenOnSameLine(openingToken, closingToken)) return;
			const sourceBetween = sourceCode.text.slice(openingToken.range[1], closingToken.range[0]);
			if (sourceBetween.trim() !== "") return;
			if (options.emptyObjects === "always") {
				if (sourceBetween) return;
				context.report({
					node,
					loc: {
						start: openingToken.loc.end,
						end: closingToken.loc.start
					},
					messageId: "requiredSpaceInEmptyObject",
					fix(fixer) {
						return fixer.replaceTextRange([openingToken.range[1], closingToken.range[0]], " ");
					}
				});
			} else if (options.emptyObjects === "never") {
				if (!sourceBetween) return;
				context.report({
					node,
					loc: {
						start: openingToken.loc.end,
						end: closingToken.loc.start
					},
					messageId: "unexpectedSpaceInEmptyObject",
					fix(fixer) {
						return fixer.removeRange([openingToken.range[1], closingToken.range[0]]);
					}
				});
			}
		}
		/**
		* Reports a given mapping node if spacing in curly braces is invalid.
		* @param node A YAMLMapping node to check.
		*/
		function checkForObject(node) {
			if (node.pairs.length === 0) {
				checkSpaceInEmptyObject(node);
				return;
			}
			const openingToken = sourceCode.getFirstToken(node);
			const closingToken = getClosingBraceOfObject(node);
			const second = sourceCode.getTokenAfter(openingToken, { includeComments: true });
			const penultimate = sourceCode.getTokenBefore(closingToken, { includeComments: true });
			validateBraceSpacing(node, options.spaced, openingToken, second, penultimate, closingToken);
		}
		return { YAMLMapping(node) {
			if (node.style === "flow") checkForObject(node);
		} };
	}
});

//#endregion
//#region src/rules/flow-sequence-bracket-newline.ts
var flow_sequence_bracket_newline_default = createRule("flow-sequence-bracket-newline", {
	meta: {
		docs: {
			description: "enforce linebreaks after opening and before closing flow sequence brackets",
			categories: ["standard"],
			extensionRule: "array-bracket-newline",
			layout: true
		},
		fixable: "whitespace",
		schema: [{ oneOf: [{ enum: [
			"always",
			"never",
			"consistent"
		] }, {
			type: "object",
			properties: {
				multiline: { type: "boolean" },
				minItems: {
					type: ["integer", "null"],
					minimum: 0
				}
			},
			additionalProperties: false
		}] }],
		messages: {
			unexpectedOpeningLinebreak: "There should be no linebreak after '['.",
			unexpectedClosingLinebreak: "There should be no linebreak before ']'.",
			missingOpeningLinebreak: "A linebreak is required after '['.",
			missingClosingLinebreak: "A linebreak is required before ']'."
		},
		type: "layout"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		/**
		* Normalizes a given option value.
		* @param {string|Object|undefined} option An option value to parse.
		* @returns {{multiline: boolean, minItems: number}} Normalized option object.
		*/
		function normalizeOptionValue(option) {
			let consistent = false;
			let multiline = false;
			let minItems = 0;
			if (option) if (option === "consistent") {
				consistent = true;
				minItems = Number.POSITIVE_INFINITY;
			} else if (option === "always" || typeof option !== "string" && option.minItems === 0) minItems = 0;
			else if (option === "never") minItems = Number.POSITIVE_INFINITY;
			else {
				multiline = Boolean(option.multiline);
				minItems = option.minItems || Number.POSITIVE_INFINITY;
			}
			else {
				consistent = false;
				multiline = true;
				minItems = Number.POSITIVE_INFINITY;
			}
			return {
				consistent,
				multiline,
				minItems
			};
		}
		/**
		* Reports that there shouldn't be a linebreak after the first token
		* @param {ASTNode} node The node to report in the event of an error.
		* @param {Token} token The token to use for the report.
		* @returns {void}
		*/
		function reportNoBeginningLinebreak(node, token) {
			context.report({
				node,
				loc: token.loc,
				messageId: "unexpectedOpeningLinebreak",
				fix(fixer) {
					if (hasTabIndent(context)) return null;
					const nextToken = sourceCode.getTokenAfter(token, { includeComments: true });
					if (isCommentToken(nextToken)) return null;
					return fixer.removeRange([token.range[1], nextToken.range[0]]);
				}
			});
		}
		/**
		* Reports that there shouldn't be a linebreak before the last token
		* @param {ASTNode} node The node to report in the event of an error.
		* @param {Token} token The token to use for the report.
		* @returns {void}
		*/
		function reportNoEndingLinebreak(node, token) {
			context.report({
				node,
				loc: token.loc,
				messageId: "unexpectedClosingLinebreak",
				fix(fixer) {
					if (hasTabIndent(context)) return null;
					const previousToken = sourceCode.getTokenBefore(token, { includeComments: true });
					if (isCommentToken(previousToken)) return null;
					return fixer.removeRange([previousToken.range[1], token.range[0]]);
				}
			});
		}
		/**
		* Reports that there should be a linebreak after the first token
		* @param {ASTNode} node The node to report in the event of an error.
		* @param {Token} token The token to use for the report.
		* @returns {void}
		*/
		function reportRequiredBeginningLinebreak(node, token) {
			context.report({
				node,
				loc: token.loc,
				messageId: "missingOpeningLinebreak",
				fix(fixer) {
					if (hasTabIndent(context)) return null;
					const indent = incIndent(getActualIndentFromLine(token.loc.start.line, context), context);
					return fixer.insertTextAfter(token, `\n${indent}`);
				}
			});
		}
		/**
		* Reports that there should be a linebreak before the last token
		* @param {ASTNode} node The node to report in the event of an error.
		* @param {Token} token The token to use for the report.
		* @returns {void}
		*/
		function reportRequiredEndingLinebreak(node, token) {
			context.report({
				node,
				loc: token.loc,
				messageId: "missingClosingLinebreak",
				fix(fixer) {
					if (hasTabIndent(context)) return null;
					const indent = getActualIndentFromLine(token.loc.start.line, context);
					return fixer.insertTextBefore(token, `\n${indent}`);
				}
			});
		}
		/**
		* Reports a given node if it violated this rule.
		* @param {ASTNode} node A node to check. This is an ArrayExpression node or an ArrayPattern node.
		* @returns {void}
		*/
		function check(node) {
			if (isKeyNode(node)) return;
			const elements = node.entries;
			const options = normalizeOptionValue(context.options[0]);
			const openBracket = sourceCode.getFirstToken(node);
			const closeBracket = sourceCode.getLastToken(node);
			const firstIncComment = sourceCode.getTokenAfter(openBracket, { includeComments: true });
			const lastIncComment = sourceCode.getTokenBefore(closeBracket, { includeComments: true });
			const first = sourceCode.getTokenAfter(openBracket);
			const last = sourceCode.getTokenBefore(closeBracket);
			if (elements.length >= options.minItems || options.multiline && elements.length > 0 && firstIncComment.loc.start.line !== lastIncComment.loc.end.line || elements.length === 0 && firstIncComment.type === "Block" && firstIncComment.loc.start.line !== lastIncComment.loc.end.line && firstIncComment === lastIncComment || options.consistent && openBracket.loc.end.line !== first.loc.start.line) {
				if (isTokenOnSameLine(openBracket, first)) reportRequiredBeginningLinebreak(node, openBracket);
				if (isTokenOnSameLine(last, closeBracket)) reportRequiredEndingLinebreak(node, closeBracket);
			} else {
				if (!isTokenOnSameLine(openBracket, first)) reportNoBeginningLinebreak(node, openBracket);
				if (!isTokenOnSameLine(last, closeBracket)) reportNoEndingLinebreak(node, closeBracket);
			}
		}
		return { YAMLSequence(node) {
			if (node.style === "flow") check(node);
		} };
	}
});

//#endregion
//#region src/rules/flow-sequence-bracket-spacing.ts
var flow_sequence_bracket_spacing_default = createRule("flow-sequence-bracket-spacing", {
	meta: {
		docs: {
			description: "enforce consistent spacing inside flow sequence brackets",
			categories: ["standard"],
			extensionRule: "array-bracket-spacing",
			layout: true
		},
		type: "layout",
		fixable: "whitespace",
		schema: [{
			type: "string",
			enum: ["always", "never"]
		}, {
			type: "object",
			properties: {
				singleValue: { type: "boolean" },
				objectsInArrays: { type: "boolean" },
				arraysInArrays: { type: "boolean" }
			},
			additionalProperties: false
		}],
		messages: {
			unexpectedSpaceAfter: "There should be no space after '{{tokenValue}}'.",
			unexpectedSpaceBefore: "There should be no space before '{{tokenValue}}'.",
			missingSpaceAfter: "A space is required after '{{tokenValue}}'.",
			missingSpaceBefore: "A space is required before '{{tokenValue}}'."
		}
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const spaced = context.options[0] === "always";
		/**
		* Determines whether an option is set, relative to the spacing option.
		* If spaced is "always", then check whether option is set to false.
		* If spaced is "never", then check whether option is set to true.
		* @param option The option to exclude.
		* @returns Whether or not the property is excluded.
		*/
		function isOptionSet(option) {
			return context.options[1] ? context.options[1][option] === !spaced : false;
		}
		const options = {
			spaced,
			singleElementException: isOptionSet("singleValue"),
			objectsInArraysException: isOptionSet("objectsInArrays"),
			arraysInArraysException: isOptionSet("arraysInArrays"),
			isOpeningBracketMustBeSpaced(node) {
				if (options.singleElementException && node.entries.length === 1) return !options.spaced;
				const firstElement = node.entries[0];
				return firstElement && (options.objectsInArraysException && isObjectType(firstElement) || options.arraysInArraysException && isArrayType(firstElement)) ? !options.spaced : options.spaced;
			},
			isClosingBracketMustBeSpaced(node) {
				if (options.singleElementException && node.entries.length === 1) return !options.spaced;
				const lastElement = node.entries[node.entries.length - 1];
				return lastElement && (options.objectsInArraysException && isObjectType(lastElement) || options.arraysInArraysException && isArrayType(lastElement)) ? !options.spaced : options.spaced;
			}
		};
		/**
		* Reports that there shouldn't be a space after the first token
		* @param node The node to report in the event of an error.
		* @param token The token to use for the report.
		*/
		function reportNoBeginningSpace(node, token) {
			const nextToken = sourceCode.getTokenAfter(token);
			context.report({
				node,
				loc: {
					start: token.loc.end,
					end: nextToken.loc.start
				},
				messageId: "unexpectedSpaceAfter",
				data: { tokenValue: token.value },
				fix(fixer) {
					return fixer.removeRange([token.range[1], nextToken.range[0]]);
				}
			});
		}
		/**
		* Reports that there shouldn't be a space before the last token
		* @param node The node to report in the event of an error.
		* @param token The token to use for the report.
		*/
		function reportNoEndingSpace(node, token) {
			const previousToken = sourceCode.getTokenBefore(token);
			context.report({
				node,
				loc: {
					start: previousToken.loc.end,
					end: token.loc.start
				},
				messageId: "unexpectedSpaceBefore",
				data: { tokenValue: token.value },
				fix(fixer) {
					return fixer.removeRange([previousToken.range[1], token.range[0]]);
				}
			});
		}
		/**
		* Reports that there should be a space after the first token
		* @param node The node to report in the event of an error.
		* @param token The token to use for the report.
		*/
		function reportRequiredBeginningSpace(node, token) {
			context.report({
				node,
				loc: token.loc,
				messageId: "missingSpaceAfter",
				data: { tokenValue: token.value },
				fix(fixer) {
					return fixer.insertTextAfter(token, " ");
				}
			});
		}
		/**
		* Reports that there should be a space before the last token
		* @param node The node to report in the event of an error.
		* @param token The token to use for the report.
		*/
		function reportRequiredEndingSpace(node, token) {
			context.report({
				node,
				loc: token.loc,
				messageId: "missingSpaceBefore",
				data: { tokenValue: token.value },
				fix(fixer) {
					return fixer.insertTextBefore(token, " ");
				}
			});
		}
		/**
		* Determines if a node is an object type
		* @param node The node to check.
		* @returns Whether or not the node is an object type.
		*/
		function isObjectType(node) {
			return node && node.type === "YAMLMapping";
		}
		/**
		* Determines if a node is an array type
		* @param node The node to check.
		* @returns Whether or not the node is an array type.
		*/
		function isArrayType(node) {
			return node && node.type === "YAMLSequence";
		}
		/**
		* Validates the spacing around array brackets
		* @param node The node we're checking for spacing
		*/
		function validateArraySpacing(node) {
			if (options.spaced && node.entries.length === 0) return;
			const first = sourceCode.getFirstToken(node);
			const last = sourceCode.getLastToken(node);
			const second = sourceCode.getTokenAfter(first, { includeComments: true });
			const penultimate = sourceCode.getTokenBefore(last, { includeComments: true });
			if (isTokenOnSameLine(first, second)) {
				if (options.isOpeningBracketMustBeSpaced(node)) {
					if (!sourceCode.isSpaceBetween(first, second)) reportRequiredBeginningSpace(node, first);
				} else if (sourceCode.isSpaceBetween(first, second)) reportNoBeginningSpace(node, first);
			}
			if (first !== penultimate && isTokenOnSameLine(penultimate, last)) {
				if (options.isClosingBracketMustBeSpaced(node)) {
					if (!sourceCode.isSpaceBetween(penultimate, last)) reportRequiredEndingSpace(node, last);
				} else if (sourceCode.isSpaceBetween(penultimate, last)) reportNoEndingSpace(node, last);
			}
		}
		return { YAMLSequence(node) {
			if (node.style === "flow") validateArraySpacing(node);
		} };
	}
});

//#endregion
//#region src/rules/indent.ts
const ITERATION_OPTS = Object.freeze({ includeComments: true });
/**
* Parse options
*/
function parseOptions$2(context) {
	const [indentOption, objectOptions] = context.options;
	const numOfIndent = getNumOfIndent(context, indentOption);
	let indentBlockSequences = true;
	let indicatorValueIndent = numOfIndent;
	let alignMultilineFlowScalars = false;
	if (objectOptions) {
		if (objectOptions.indentBlockSequences === false) indentBlockSequences = false;
		if (objectOptions.indicatorValueIndent != null) indicatorValueIndent = objectOptions.indicatorValueIndent;
		if (objectOptions.alignMultilineFlowScalars != null) alignMultilineFlowScalars = objectOptions.alignMultilineFlowScalars;
	}
	return {
		numOfIndent,
		indentBlockSequences,
		indicatorValueIndent,
		alignMultilineFlowScalars
	};
}
var indent_default = createRule("indent", {
	meta: {
		docs: {
			description: "enforce consistent indentation",
			categories: ["standard"],
			extensionRule: false,
			layout: true
		},
		fixable: "whitespace",
		schema: [{
			type: "integer",
			minimum: 2
		}, {
			type: "object",
			properties: {
				indentBlockSequences: { type: "boolean" },
				indicatorValueIndent: {
					type: "integer",
					minimum: 2
				},
				alignMultilineFlowScalars: { type: "boolean" }
			},
			additionalProperties: false
		}],
		messages: { wrongIndentation: "Expected indentation of {{expected}} spaces but found {{actual}} spaces." },
		type: "layout"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		if (hasTabIndent(context)) return {};
		const { numOfIndent, indentBlockSequences, indicatorValueIndent, alignMultilineFlowScalars } = parseOptions$2(context);
		const indents = /* @__PURE__ */ new Map();
		const indicators = /* @__PURE__ */ new Set();
		const blockLiteralMarks = /* @__PURE__ */ new Set();
		const scalars = /* @__PURE__ */ new Map();
		/**
		* Set offset to the given tokens.
		* @param token The token to set.
		* @param offset The offset of the tokens.
		* @param baseToken The token of the base offset.
		*/
		function setOffset(token, offset, baseToken, options) {
			setIndent(token, offset * numOfIndent, baseToken, options && { indentWhenBaseIsNotFirst: options.offsetWhenBaseIsNotFirst && options.offsetWhenBaseIsNotFirst * numOfIndent });
		}
		/**
		* Set indent to the given tokens.
		* @param token The token to set.
		* @param indent The indent of the tokens.
		* @param baseToken The token of the base indent.
		*/
		function setIndent(token, indent, baseToken, options) {
			if (token == null) return;
			if (Array.isArray(token)) for (const t of token) setIndent(t, indent, baseToken, options);
			else indents.set(token, {
				baseToken,
				indent,
				indentWhenBaseIsNotFirst: options?.indentWhenBaseIsNotFirst ?? null
			});
		}
		/**
		* Process the given node list.
		* @param {(AST.YAMLNode|null)[]} nodeList The node to process.
		* @param {number} offset The offset to set.
		* @returns {void}
		*/
		function processNodeList(nodeList, left, right, offset) {
			let lastToken = left;
			const alignTokens = /* @__PURE__ */ new Set();
			for (const node of nodeList) {
				if (node == null) continue;
				const elementTokens = {
					firstToken: sourceCode.getFirstToken(node),
					lastToken: sourceCode.getLastToken(node)
				};
				let t = lastToken;
				while ((t = sourceCode.getTokenAfter(t, ITERATION_OPTS)) != null && t.range[1] <= elementTokens.firstToken.range[0]) alignTokens.add(t);
				alignTokens.add(elementTokens.firstToken);
				lastToken = elementTokens.lastToken;
			}
			if (right != null) {
				let t = lastToken;
				while ((t = sourceCode.getTokenAfter(t, ITERATION_OPTS)) != null && t.range[1] <= right.range[0]) alignTokens.add(t);
			}
			alignTokens.delete(left);
			setOffset([...alignTokens], offset, left);
			if (right != null) setOffset(right, 0, left);
		}
		/**
		* Calculate the indentation for the values in the mapping.
		*/
		function calcMappingPairValueIndent(node, indent) {
			if (indentBlockSequences) return indent;
			if (node.type === "YAMLSequence" && node.style === "block") return 0;
			return indent;
		}
		/**
		* Calculate the indentation for the values in the indicator.
		*/
		function calcIndicatorValueIndent(token) {
			return isBeginningToken(token) ? indicatorValueIndent : numOfIndent;
		}
		/**
		* Checks whether the given token is a beginning token.
		*/
		function isBeginningToken(token) {
			const before = sourceCode.getTokenBefore(token, (t) => !indicators.has(t));
			if (!before) return true;
			return before.loc.end.line < token.loc.start.line;
		}
		const documents = [];
		return {
			YAMLDocument(node) {
				documents.push(node);
				const first = sourceCode.getFirstToken(node, ITERATION_OPTS);
				if (!first) return;
				indents.set(first, {
					baseToken: null,
					indentWhenBaseIsNotFirst: null,
					indent: 0,
					expectedIndent: 0
				});
				processNodeList([...node.directives, node.content], first, null, 0);
			},
			YAMLMapping(node) {
				if (node.style === "flow") {
					const open = sourceCode.getFirstToken(node);
					const close = sourceCode.getLastToken(node);
					processNodeList(node.pairs, open, close, 1);
				} else if (node.style === "block") {
					const first = sourceCode.getFirstToken(node);
					processNodeList(node.pairs, first, null, 0);
				}
			},
			YAMLSequence(node) {
				if (node.style === "flow") {
					const open = sourceCode.getFirstToken(node);
					const close = sourceCode.getLastToken(node);
					processNodeList(node.entries, open, close, 1);
				} else if (node.style === "block") {
					const first = sourceCode.getFirstToken(node);
					processNodeList(node.entries, first, null, 0);
					for (const entry of node.entries) {
						if (!entry) continue;
						const hyphen = sourceCode.getTokenBefore(entry, isHyphen);
						indicators.add(hyphen);
						setIndent(sourceCode.getFirstToken(entry), calcIndicatorValueIndent(hyphen), hyphen);
					}
				}
			},
			YAMLPair(node) {
				const pairFirst = sourceCode.getFirstToken(node);
				const keyToken = node.key && sourceCode.getFirstToken(node.key);
				const colonToken = findColonToken();
				const questionToken = isQuestion(pairFirst) ? pairFirst : null;
				if (questionToken) {
					indicators.add(questionToken);
					if (node.key) setIndent(keyToken, calcMappingPairValueIndent(node.key, calcIndicatorValueIndent(questionToken)), questionToken);
				}
				if (colonToken) {
					indicators.add(colonToken);
					if (questionToken) setOffset(colonToken, 0, questionToken, { offsetWhenBaseIsNotFirst: 1 });
					else if (keyToken) setOffset(colonToken, 1, keyToken);
				}
				if (node.value) {
					const valueToken = sourceCode.getFirstToken(node.value);
					if (colonToken) setIndent(valueToken, calcMappingPairValueIndent(node.value, calcIndicatorValueIndent(colonToken)), colonToken);
					else if (keyToken) setOffset(valueToken, 1, keyToken);
				}
				/** Find colon indicator token */
				function findColonToken() {
					if (node.value) return sourceCode.getTokenBefore(node.value, isColon);
					if (node.key) {
						const token = sourceCode.getTokenAfter(node.key, isColon);
						if (token && token.range[0] < node.range[1]) return token;
					}
					const tokens = sourceCode.getTokens(node, isColon);
					if (tokens.length) return tokens[0];
					return null;
				}
			},
			YAMLWithMeta(node) {
				const anchorToken = node.anchor && sourceCode.getFirstToken(node.anchor);
				const tagToken = node.tag && sourceCode.getFirstToken(node.tag);
				let baseToken;
				if (anchorToken && tagToken) if (anchorToken.range[0] < tagToken.range[0]) {
					setOffset(tagToken, 0, anchorToken, { offsetWhenBaseIsNotFirst: 1 });
					baseToken = anchorToken;
				} else {
					setOffset(anchorToken, 0, tagToken, { offsetWhenBaseIsNotFirst: 1 });
					baseToken = tagToken;
				}
				else baseToken = anchorToken || tagToken;
				if (node.value) setOffset(sourceCode.getFirstToken(node.value), 1, baseToken);
			},
			YAMLScalar(node) {
				if (node.style === "folded" || node.style === "literal") {
					if (!node.value.trim()) return;
					const mark = sourceCode.getFirstToken(node);
					const literal = sourceCode.getLastToken(node);
					setOffset(literal, 1, mark);
					scalars.set(literal, node);
					blockLiteralMarks.add(mark);
				} else scalars.set(sourceCode.getFirstToken(node), node);
			},
			"Program:exit"(node) {
				const lineIndentsWk = [];
				let tokensOnSameLine = [];
				for (const token of [...node.comments, ...node.tokens].sort((a, b) => a.range[0] - b.range[0])) if (tokensOnSameLine.length === 0 || tokensOnSameLine[0].loc.start.line === token.loc.start.line) tokensOnSameLine.push(token);
				else {
					const lineIndent = processExpectedIndent(tokensOnSameLine);
					lineIndentsWk[lineIndent.line] = lineIndent;
					tokensOnSameLine = [token];
				}
				if (tokensOnSameLine.length >= 1) {
					const lineIndent = processExpectedIndent(tokensOnSameLine);
					lineIndentsWk[lineIndent.line] = lineIndent;
				}
				validateLines(processMissingLines(lineIndentsWk));
			}
		};
		/**
		* Process the expected indent for given line tokens
		*/
		function processExpectedIndent(lineTokens) {
			const lastToken = lineTokens[lineTokens.length - 1];
			let lineExpectedIndent = null;
			let cacheExpectedIndent = null;
			const indicatorData = [];
			const firstToken = lineTokens.shift();
			let token = firstToken;
			let expectedIndent = getExpectedIndent(token);
			if (expectedIndent != null) {
				lineExpectedIndent = expectedIndent;
				cacheExpectedIndent = expectedIndent;
			}
			while (token && indicators.has(token) && expectedIndent != null) {
				const nextToken = lineTokens.shift();
				if (!nextToken) break;
				const nextExpectedIndent = getExpectedIndent(nextToken);
				if (nextExpectedIndent == null || expectedIndent >= nextExpectedIndent) {
					lineTokens.unshift(nextToken);
					break;
				}
				indicatorData.push({
					indicator: token,
					next: nextToken,
					expectedOffset: nextExpectedIndent - expectedIndent - 1,
					actualOffset: nextToken.range[0] - token.range[1]
				});
				if (blockLiteralMarks.has(nextToken)) {
					lineTokens.unshift(nextToken);
					break;
				}
				token = nextToken;
				expectedIndent = nextExpectedIndent;
				cacheExpectedIndent = expectedIndent;
			}
			if (lineExpectedIndent == null) while ((token = lineTokens.shift()) != null) {
				lineExpectedIndent = getExpectedIndent(token);
				if (lineExpectedIndent != null) break;
			}
			const scalarNode = scalars.get(lastToken);
			if (scalarNode) lineTokens.pop();
			if (cacheExpectedIndent != null) while ((token = lineTokens.shift()) != null) {
				const indent = indents.get(token);
				if (indent) indent.expectedIndent = cacheExpectedIndent;
			}
			let lastScalar = null;
			if (scalarNode) {
				const expectedScalarIndent = getExpectedIndent(lastToken);
				if (expectedScalarIndent != null) lastScalar = {
					expectedIndent: expectedScalarIndent,
					token: lastToken,
					node: scalarNode
				};
			}
			const { line, column } = firstToken.loc.start;
			return {
				expectedIndent: lineExpectedIndent,
				actualIndent: column,
				firstToken,
				line,
				indicatorData,
				lastScalar
			};
		}
		/**
		* Get the expected indent from given token
		*/
		function getExpectedIndent(token) {
			if (token.type === "Marker") return 0;
			const indent = indents.get(token);
			if (!indent) return null;
			if (indent.expectedIndent != null) return indent.expectedIndent;
			if (indent.baseToken == null) return null;
			const baseIndent = getExpectedIndent(indent.baseToken);
			if (baseIndent == null) return null;
			let offsetIndent = indent.indent;
			if (offsetIndent === 0 && indent.indentWhenBaseIsNotFirst != null) {
				let before = indent.baseToken;
				while ((before = sourceCode.getTokenBefore(before, ITERATION_OPTS)) != null) if (!indicators.has(before)) break;
				if (before?.loc.end.line === indent.baseToken.loc.start.line) offsetIndent = indent.indentWhenBaseIsNotFirst;
			}
			return indent.expectedIndent = baseIndent + offsetIndent;
		}
		/**
		* Calculates the indent for lines with missing indent information.
		*/
		function processMissingLines(lineIndents) {
			const results = [];
			const commentLines = [];
			for (const lineIndent of lineIndents) {
				if (!lineIndent) continue;
				const line = lineIndent.line;
				if (lineIndent.firstToken.type === "Block") {
					const last = commentLines[commentLines.length - 1];
					if (last && last.range[1] === line - 1) {
						last.range[1] = line;
						last.commentLineIndents.push(lineIndent);
					} else commentLines.push({
						range: [line, line],
						commentLineIndents: [lineIndent]
					});
				} else if (lineIndent.expectedIndent != null) {
					const indent = {
						line,
						expectedIndent: lineIndent.expectedIndent,
						actualIndent: lineIndent.actualIndent,
						indicatorData: lineIndent.indicatorData
					};
					if (!results[line]) results[line] = indent;
					if (lineIndent.lastScalar) {
						const scalarNode = lineIndent.lastScalar.node;
						if (scalarNode.style === "literal" || scalarNode.style === "folded") processBlockLiteral(indent, scalarNode, lineIndent.lastScalar.expectedIndent);
						else {
							let expectedIndent = lineIndent.lastScalar.expectedIndent;
							if (alignMultilineFlowScalars) {
								if (!isBeginningToken(lineIndent.lastScalar.token)) expectedIndent = lineIndent.lastScalar.node.loc.start.column;
							}
							processMultilineScalar(indent, scalarNode, expectedIndent);
						}
					}
				}
			}
			processComments(commentLines, lineIndents);
			return results;
			/**
			* Process comments.
			*/
			function processComments(commentLines, lineIndents) {
				for (const { range, commentLineIndents } of commentLines) {
					let prev = results.slice(0, range[0]).filter((data) => data).pop();
					const next = results.slice(range[1] + 1).filter((data) => data).shift();
					if (isBlockLiteral(prev)) prev = void 0;
					const expectedIndents = [];
					let either;
					if (prev && next) {
						expectedIndents.unshift(next.expectedIndent);
						if (next.expectedIndent < prev.expectedIndent) {
							let indent = next.expectedIndent + numOfIndent;
							while (indent <= prev.expectedIndent) {
								expectedIndents.unshift(indent);
								indent += numOfIndent;
							}
						}
					} else if (either = prev || next) {
						expectedIndents.unshift(either.expectedIndent);
						if (!next) {
							let indent = either.expectedIndent - numOfIndent;
							while (indent >= 0) {
								expectedIndents.push(indent);
								indent -= numOfIndent;
							}
						}
					}
					if (!expectedIndents.length) continue;
					let expectedIndent = expectedIndents[0];
					for (const commentLineIndent of commentLineIndents) {
						if (results[commentLineIndent.line]) continue;
						expectedIndent = Math.min(expectedIndents.find((indent, index) => {
							if (indent <= commentLineIndent.actualIndent) return true;
							return (expectedIndents[index + 1] ?? -1) < commentLineIndent.actualIndent && commentLineIndent.actualIndent < indent;
						}) ?? expectedIndent, expectedIndent);
						results[commentLineIndent.line] = {
							line: commentLineIndent.line,
							expectedIndent,
							actualIndent: commentLineIndent.actualIndent,
							indicatorData: commentLineIndent.indicatorData
						};
					}
				}
				/**
				* Checks whether given prev data is block literal
				*/
				function isBlockLiteral(prev) {
					if (!prev) return false;
					for (let prevLine = prev.line; prevLine >= 0; prevLine--) {
						const prevLineIndent = lineIndents[prev.line];
						if (!prevLineIndent) continue;
						if (prevLineIndent.lastScalar) {
							const scalarNode = prevLineIndent.lastScalar.node;
							if (scalarNode.style === "literal" || scalarNode.style === "folded") {
								if (scalarNode.loc.start.line <= prev.line && prev.line <= scalarNode.loc.end.line) return true;
							}
						}
						return false;
					}
					return false;
				}
			}
			/**
			* Process block literal
			*/
			function processBlockLiteral(lineIndent, scalarNode, expectedIndent) {
				if (scalarNode.indent != null) {
					if (lineIndent.expectedIndent < lineIndent.actualIndent) {
						lineIndent.expectedIndent = lineIndent.actualIndent;
						return;
					}
					lineIndent.indentBlockScalar = { node: scalarNode };
				}
				const firstLineActualIndent = lineIndent.actualIndent;
				for (let scalarLine = lineIndent.line + 1; scalarLine <= scalarNode.loc.end.line; scalarLine++) {
					const actualLineIndent = getActualLineIndent(scalarLine);
					if (actualLineIndent == null) continue;
					results[scalarLine] = {
						line: scalarLine,
						expectedIndent,
						actualIndent: Math.min(firstLineActualIndent, actualLineIndent),
						indicatorData: []
					};
				}
			}
			/**
			* Process for a multiline-scalar
			*/
			function processMultilineScalar(lineIndent, scalarNode, expectedIndent) {
				for (let scalarLine = lineIndent.line + 1; scalarLine <= scalarNode.loc.end.line; scalarLine++) {
					const scalarActualIndent = getActualLineIndent(scalarLine);
					if (scalarActualIndent == null) continue;
					results[scalarLine] = {
						line: scalarLine,
						expectedIndent,
						actualIndent: scalarActualIndent,
						indicatorData: []
					};
				}
			}
		}
		/**
		* Validate lines
		*/
		function validateLines(lineIndents) {
			for (const lineIndent of lineIndents) {
				if (!lineIndent) continue;
				if (lineIndent.actualIndent !== lineIndent.expectedIndent) context.report({
					loc: {
						start: {
							line: lineIndent.line,
							column: 0
						},
						end: {
							line: lineIndent.line,
							column: lineIndent.actualIndent
						}
					},
					messageId: "wrongIndentation",
					data: {
						expected: String(lineIndent.expectedIndent),
						actual: String(lineIndent.actualIndent)
					},
					fix: buildFix(lineIndent, lineIndents)
				});
				else if (lineIndent.indicatorData.length) {
					for (const indicatorData of lineIndent.indicatorData) if (indicatorData.actualOffset !== indicatorData.expectedOffset) {
						const indicatorLoc = indicatorData.indicator.loc.end;
						const loc = indicatorData.next.loc.start;
						context.report({
							loc: {
								start: indicatorLoc,
								end: loc
							},
							messageId: "wrongIndentation",
							data: {
								expected: String(indicatorData.expectedOffset),
								actual: String(indicatorData.actualOffset)
							},
							fix: buildFix(lineIndent, lineIndents)
						});
					}
				}
			}
		}
		/**
		* Build the fixer function that makes collect indentation.
		*/
		function buildFix(lineIndent, lineIndents) {
			const { line, expectedIndent } = lineIndent;
			const document = documents.find((doc) => doc.loc.start.line <= line && line <= doc.loc.end.line) || sourceCode.ast;
			let startLine = document.loc.start.line;
			let endLine = document.loc.end.line;
			for (let lineIndex = line - 1; lineIndex >= document.loc.start.line; lineIndex--) {
				const li = lineIndents[lineIndex];
				if (!li) continue;
				if (li.expectedIndent < expectedIndent) {
					if (expectedIndent <= li.actualIndent) return null;
					for (const indicator of li.indicatorData) if (indicator.actualOffset !== indicator.expectedOffset) return null;
					startLine = lineIndex + 1;
					break;
				}
			}
			for (let lineIndex = line + 1; lineIndex <= document.loc.end.line; lineIndex++) {
				const li = lineIndents[lineIndex];
				if (!li) continue;
				if (li && li.expectedIndent < expectedIndent) {
					if (expectedIndent <= li.actualIndent) return null;
					endLine = lineIndex - 1;
					break;
				}
			}
			for (let lineIndex = startLine; lineIndex <= endLine; lineIndex++) {
				const li = lineIndents[lineIndex];
				if (li?.indentBlockScalar) {
					const blockLiteral = li.indentBlockScalar.node;
					const diff = li.expectedIndent - li.actualIndent;
					const mark = sourceCode.getFirstToken(blockLiteral);
					const num = /\d+/u.exec(mark.value)?.[0];
					if (num != null) {
						if (Number(num) + diff >= 10) return null;
					}
				}
			}
			return function* (fixer) {
				let stacks = null;
				for (let lineIndex = startLine; lineIndex <= endLine; lineIndex++) {
					const li = lineIndents[lineIndex];
					if (!li) continue;
					const lineExpectedIndent = li.expectedIndent;
					if (stacks == null) {
						if (li.expectedIndent !== li.actualIndent) yield* fixLine(fixer, li);
					} else {
						if (stacks.indent < lineExpectedIndent) stacks = {
							indent: lineExpectedIndent,
							parentIndent: stacks.indent,
							upper: stacks
						};
						else if (lineExpectedIndent < stacks.indent) stacks = stacks.upper;
						if (li.actualIndent <= stacks.parentIndent) yield* fixLine(fixer, li);
					}
					if (li.indicatorData) for (const indicatorData of li.indicatorData) yield fixer.replaceTextRange([indicatorData.indicator.range[1], indicatorData.next.range[0]], " ".repeat(indicatorData.expectedOffset));
				}
			};
		}
		/**
		* Fix a line
		*/
		function* fixLine(fixer, li) {
			if (li.indentBlockScalar) {
				const blockLiteral = li.indentBlockScalar.node;
				const diff = li.expectedIndent - li.actualIndent;
				const mark = sourceCode.getFirstToken(blockLiteral);
				yield fixer.replaceText(mark, mark.value.replace(/\d+/u, (num) => `${Number(num) + diff}`));
			}
			const expectedIndent = li.expectedIndent;
			yield fixer.replaceTextRange([sourceCode.getIndexFromLoc({
				line: li.line,
				column: 0
			}), sourceCode.getIndexFromLoc({
				line: li.line,
				column: li.actualIndent
			})], " ".repeat(expectedIndent));
		}
		/**
		* Get actual indent from given line
		*/
		function getActualLineIndent(line) {
			const lineText = sourceCode.lines[line - 1];
			if (!lineText.length) return null;
			return /^\s*/u.exec(lineText)[0].length;
		}
	}
});

//#endregion
//#region src/utils/casing.ts
const allowedCaseOptions = [
	"camelCase",
	"kebab-case",
	"PascalCase",
	"snake_case",
	"SCREAMING_SNAKE_CASE"
];
/**
* Checks whether the given string has symbols.
* @param {string} str
*/
function hasSymbols(str) {
	return /[\u0021-\u0023\u0025-\u002c./\u003a-\u0040\u005b-\u005e`\u007b-\u007d]/u.test(str);
}
/**
* Checks whether the given string has upper.
* @param {string} str
*/
function hasUpper(str) {
	return /[A-Z]/u.test(str);
}
/**
* Checks whether the given string has lower.
* @param {string} str
*/
function hasLower(str) {
	return /[a-z]/u.test(str);
}
/**
* Checks whether the given string is kebab-case.
* @param {string} str
*/
function isKebabCase(str) {
	if (hasUpper(str) || hasSymbols(str) || str.startsWith("-") || /_|--|\s/u.test(str)) return false;
	return true;
}
/**
* Checks whether the given string is snake_case.
* @param {string} str
*/
function isSnakeCase(str) {
	if (hasUpper(str) || hasSymbols(str) || /-|__|\s/u.test(str)) return false;
	return true;
}
/**
* Checks whether the given string is SCREAMING_SNAKE_CASE.
* @param {string} str
*/
function isScreamingSnakeCase(str) {
	if (hasLower(str) || hasSymbols(str) || /-|__|\s/u.test(str)) return false;
	return true;
}
/**
* Checks whether the given string is camelCase.
* @param {string} str
*/
function isCamelCase(str) {
	if (hasSymbols(str) || /^[A-Z]/u.test(str) || /[\s\-_]/u.test(str)) return false;
	return true;
}
/**
* Checks whether the given string is PascalCase.
* @param {string} str
*/
function isPascalCase(str) {
	if (hasSymbols(str) || /^[a-z]/u.test(str) || /[\s\-_]/u.test(str)) return false;
	return true;
}
const checkersMap = {
	"kebab-case": isKebabCase,
	snake_case: isSnakeCase,
	SCREAMING_SNAKE_CASE: isScreamingSnakeCase,
	camelCase: isCamelCase,
	PascalCase: isPascalCase
};
/**
* Return case checker
* @param name type of checker to return ('camelCase', 'kebab-case', 'PascalCase')
*/
function getChecker(name) {
	return checkersMap[name] || isPascalCase;
}

//#endregion
//#region src/rules/key-name-casing.ts
var key_name_casing_default = createRule("key-name-casing", {
	meta: {
		docs: {
			description: "enforce naming convention to key names",
			categories: null,
			extensionRule: false,
			layout: false
		},
		schema: [{
			type: "object",
			properties: {
				camelCase: {
					type: "boolean",
					default: true
				},
				PascalCase: {
					type: "boolean",
					default: false
				},
				SCREAMING_SNAKE_CASE: {
					type: "boolean",
					default: false
				},
				"kebab-case": {
					type: "boolean",
					default: false
				},
				snake_case: {
					type: "boolean",
					default: false
				},
				ignores: {
					type: "array",
					items: { type: "string" },
					uniqueItems: true,
					additionalItems: false
				}
			},
			additionalProperties: false
		}],
		messages: { doesNotMatchFormat: "Key name `{{name}}` must match one of the following formats: {{formats}}" },
		type: "suggestion"
	},
	create(context) {
		if (!context.sourceCode.parserServices?.isYAML) return {};
		const option = { ...context.options[0] };
		if (option.camelCase !== false) option.camelCase = true;
		const ignores = option.ignores ? option.ignores.map((ignore) => new RegExp(ignore)) : [];
		const formats = Object.keys(option).filter((key) => allowedCaseOptions.includes(key)).filter((key) => option[key]);
		const checkers = formats.map(getChecker);
		/**
		* Check whether a given name is a valid.
		*/
		function isValid(name) {
			if (ignores.some((regex) => regex.test(name))) return true;
			return checkers.length ? checkers.some((c) => c(name)) : true;
		}
		return { YAMLPair(node) {
			if (!node.key) return;
			const name = String(getStaticYAMLValue(node.key));
			if (!isValid(name)) context.report({
				loc: node.key.loc,
				messageId: "doesNotMatchFormat",
				data: {
					name,
					formats: formats.join(", ")
				}
			});
		} };
	}
});

//#endregion
//#region src/rules/key-spacing.ts
/**
* Checks whether a string contains a line terminator as defined in
* http://www.ecma-international.org/ecma-262/5.1/#sec-7.3
* @param {string} str String to test.
* @returns {boolean} True if str contains a line terminator.
*/
function containsLineTerminator(str) {
	return /[\n\r\u2028\u2029]/u.test(str);
}
/**
* Gets the last element of an array.
* @param {Array} arr An array.
* @returns {any} Last element of arr.
*/
function last(arr) {
	return arr[arr.length - 1];
}
/**
* Checks whether a node is contained on a single line.
* @param {ASTNode} node AST Node being evaluated.
* @returns {boolean} True if the node is a single line.
*/
function isSingleLine(node) {
	return node.loc.end.line === node.loc.start.line;
}
/**
* Checks whether the properties on a single line.
* @param {ASTNode[]} properties List of Property AST nodes.
* @returns {boolean} True if all properties is on a single line.
*/
function isSingleLineProperties(properties) {
	const [firstProp] = properties;
	const lastProp = last(properties);
	return firstProp.loc.start.line === lastProp.loc.end.line;
}
/**
* Initializes a single option property from the configuration with defaults for undefined values
* @param {Object} fromOptions Object to be initialized from
* @returns {Object} The object with correctly initialized options and values
*/
function initOptionProperty(fromOptions) {
	const mode = fromOptions.mode || "strict";
	let beforeColon, afterColon;
	if (typeof fromOptions.beforeColon !== "undefined") beforeColon = fromOptions.beforeColon;
	else beforeColon = false;
	if (typeof fromOptions.afterColon !== "undefined") afterColon = fromOptions.afterColon;
	else afterColon = true;
	let align = void 0;
	if (typeof fromOptions.align !== "undefined") if (typeof fromOptions.align === "object") align = fromOptions.align;
	else align = {
		on: fromOptions.align,
		mode,
		beforeColon,
		afterColon
	};
	return {
		mode,
		beforeColon,
		afterColon,
		align
	};
}
/**
* Initializes all the option values (singleLine, multiLine and align) from the configuration with defaults for undefined values
* @param {Object} fromOptions Object to be initialized from
* @returns {Object} The object with correctly initialized options and values
*/
function initOptions(fromOptions) {
	let align, multiLine, singleLine;
	if (typeof fromOptions.align === "object") {
		align = {
			...initOptionProperty(fromOptions.align),
			on: fromOptions.align.on || "colon",
			mode: fromOptions.align.mode || "strict"
		};
		multiLine = initOptionProperty(fromOptions.multiLine || fromOptions);
		singleLine = initOptionProperty(fromOptions.singleLine || fromOptions);
	} else {
		multiLine = initOptionProperty(fromOptions.multiLine || fromOptions);
		singleLine = initOptionProperty(fromOptions.singleLine || fromOptions);
		if (multiLine.align) align = {
			on: multiLine.align.on,
			mode: multiLine.align.mode || multiLine.mode,
			beforeColon: multiLine.align.beforeColon,
			afterColon: multiLine.align.afterColon
		};
	}
	return {
		align,
		multiLine,
		singleLine
	};
}
const ON_SCHEMA = { enum: ["colon", "value"] };
const OBJECT_WITHOUT_ON_SCHEMA = {
	type: "object",
	properties: {
		mode: { enum: ["strict", "minimum"] },
		beforeColon: { type: "boolean" },
		afterColon: { type: "boolean" }
	},
	additionalProperties: false
};
const ALIGN_OBJECT_SCHEMA = {
	type: "object",
	properties: {
		on: ON_SCHEMA,
		...OBJECT_WITHOUT_ON_SCHEMA.properties
	},
	additionalProperties: false
};
var key_spacing_default = createRule("key-spacing", {
	meta: {
		docs: {
			description: "enforce consistent spacing between keys and values in mapping pairs",
			categories: ["standard"],
			extensionRule: "key-spacing",
			layout: true
		},
		fixable: "whitespace",
		schema: [{ anyOf: [
			{
				type: "object",
				properties: {
					align: { anyOf: [ON_SCHEMA, ALIGN_OBJECT_SCHEMA] },
					...OBJECT_WITHOUT_ON_SCHEMA.properties
				},
				additionalProperties: false
			},
			{
				type: "object",
				properties: {
					singleLine: OBJECT_WITHOUT_ON_SCHEMA,
					multiLine: {
						type: "object",
						properties: {
							align: { anyOf: [ON_SCHEMA, ALIGN_OBJECT_SCHEMA] },
							...OBJECT_WITHOUT_ON_SCHEMA.properties
						},
						additionalProperties: false
					}
				},
				additionalProperties: false
			},
			{
				type: "object",
				properties: {
					singleLine: OBJECT_WITHOUT_ON_SCHEMA,
					multiLine: OBJECT_WITHOUT_ON_SCHEMA,
					align: ALIGN_OBJECT_SCHEMA
				},
				additionalProperties: false
			}
		] }],
		messages: {
			extraKey: "Extra space after key '{{key}}'.",
			extraValue: "Extra space before value for key '{{key}}'.",
			missingKey: "Missing space after key '{{key}}'.",
			missingValue: "Missing space before value for key '{{key}}'."
		},
		type: "layout"
	},
	create
});
/**
* Create rule visitor
*/
function create(context) {
	const sourceCode = context.sourceCode;
	if (!sourceCode.parserServices?.isYAML) return {};
	const { multiLine: multiLineOptions, singleLine: singleLineOptions, align: alignmentOptions } = initOptions(context.options[0] || {});
	/**
	* Determines if the given property is key-value property.
	* @param {ASTNode} property Property node to check.
	* @returns {boolean} Whether the property is a key-value property.
	*/
	function isKeyValueProperty(property) {
		return property.key != null && property.value != null;
	}
	/**
	* Starting from the given a node (a property.key node here) looks forward
	* until it finds the last token before a colon punctuator and returns it.
	* @param {ASTNode} node The node to start looking from.
	* @returns {ASTNode} The last token before a colon punctuator.
	*/
	function getLastTokenBeforeColon(node) {
		const colonToken = sourceCode.getTokenAfter(node, isColon);
		return sourceCode.getTokenBefore(colonToken);
	}
	/**
	* Starting from the given a node (a property.key node here) looks forward
	* until it finds the colon punctuator and returns it.
	* @param {ASTNode} node The node to start looking from.
	* @returns {ASTNode} The colon punctuator.
	*/
	function getNextColon(node) {
		return sourceCode.getTokenAfter(node, isColon);
	}
	/**
	* Gets an object literal property's key as the identifier name or string value.
	* @param {ASTNode} property Property node whose key to retrieve.
	* @returns {string} The property's key.
	*/
	function getKey(property) {
		const key = property.key;
		if (key.type !== "YAMLScalar") return sourceCode.getText().slice(key.range[0], key.range[1]);
		return String(key.value);
	}
	/**
	* Checks if whitespace can be change.
	*/
	function canChangeSpaces(property, side) {
		if (side === "value") {
			if (isQuestion(sourceCode.getTokenBefore(property.key)) && property.key.loc.end.line < property.value.loc.start.line) return false;
		}
		return true;
	}
	/**
	* Checks if whitespace can be removed.
	*/
	function canRemoveSpaces(property, side, whitespace) {
		if (side === "key") {
			if (property.key.type === "YAMLAlias") return false;
			if (property.key.type === "YAMLWithMeta" && property.key.value == null) return false;
			if (property.parent.style === "block") {
				if (containsLineTerminator(whitespace)) {
					if (isQuestion(sourceCode.getTokenBefore(property.key))) return false;
				}
			}
		} else {
			if (property.parent.style === "block") {
				if (property.parent.parent.type !== "YAMLSequence" || property.parent.parent.style !== "flow") return false;
			}
			const keyValue = property.key.type === "YAMLWithMeta" ? property.key.value : property.key;
			if (!keyValue) return false;
			if (keyValue.type === "YAMLScalar") {
				if (keyValue.style === "plain") return false;
			}
			if (keyValue.type === "YAMLAlias") return false;
			if (property.value.type === "YAMLSequence" && property.value.style === "block") return false;
			if (containsLineTerminator(whitespace)) {
				if (property.value.type === "YAMLMapping" && property.value.style === "block") return false;
			}
		}
		return true;
	}
	/**
	* Checks if whitespace can be insert.
	*/
	function canInsertSpaces(property, side) {
		if (side === "key") {
			if (property.key.type === "YAMLScalar") {
				if (property.key.style === "plain" && typeof property.key.value === "string" && property.key.value.endsWith(":")) return false;
				if (property.key.style === "folded" || property.key.style === "literal") return false;
			}
		}
		return true;
	}
	/**
	* Reports an appropriately-formatted error if spacing is incorrect on one
	* side of the colon.
	* @param {ASTNode} property Key-value pair in an object literal.
	* @param {string} side Side being verified - either "key" or "value".
	* @param {string} whitespace Actual whitespace string.
	* @param {int} expected Expected whitespace length.
	* @param {string} mode Value of the mode as "strict" or "minimum"
	* @returns {void}
	*/
	function report(property, side, whitespace, expected, mode) {
		const diff = whitespace.length - expected;
		const nextColon = getNextColon(property.key);
		const tokenBeforeColon = sourceCode.getTokenBefore(nextColon, { includeComments: true });
		const tokenAfterColon = sourceCode.getTokenAfter(nextColon, { includeComments: true });
		if (!((mode === "strict" ? diff !== 0 : diff < 0 || diff > 0 && expected === 0) && !(expected && containsLineTerminator(whitespace)))) return;
		if (!canChangeSpaces(property, side) || expected === 0 && !canRemoveSpaces(property, side, whitespace) || whitespace.length === 0 && !canInsertSpaces(property, side)) return;
		const { locStart, locEnd, missingLoc } = side === "key" ? {
			locStart: tokenBeforeColon.loc.end,
			locEnd: nextColon.loc.start,
			missingLoc: tokenBeforeColon.loc
		} : {
			locStart: nextColon.loc.start,
			locEnd: tokenAfterColon.loc.start,
			missingLoc: tokenAfterColon.loc
		};
		const { loc, messageId } = diff > 0 ? {
			loc: {
				start: locStart,
				end: locEnd
			},
			messageId: side === "key" ? "extraKey" : "extraValue"
		} : {
			loc: missingLoc,
			messageId: side === "key" ? "missingKey" : "missingValue"
		};
		context.report({
			node: property[side],
			loc,
			messageId,
			data: { key: getKey(property) },
			fix(fixer) {
				if (diff > 0) {
					if (side === "key") return fixer.removeRange([tokenBeforeColon.range[1], tokenBeforeColon.range[1] + diff]);
					return fixer.removeRange([tokenAfterColon.range[0] - diff, tokenAfterColon.range[0]]);
				}
				const spaces = " ".repeat(-diff);
				if (side === "key") return fixer.insertTextAfter(tokenBeforeColon, spaces);
				return fixer.insertTextBefore(tokenAfterColon, spaces);
			}
		});
	}
	/**
	* Gets the number of characters in a key, including quotes around string
	* keys and braces around computed property keys.
	* @param {ASTNode} property Property of on object literal.
	* @returns {int} Width of the key.
	*/
	function getKeyWidth(pair) {
		const startToken = sourceCode.getFirstToken(pair);
		return getLastTokenBeforeColon(pair.key).range[1] - startToken.range[0];
	}
	/**
	* Gets the whitespace around the colon in an object literal property.
	* @param {ASTNode} property Property node from an object literal.
	* @returns {Object} Whitespace before and after the property's colon.
	*/
	function getPropertyWhitespace(pair) {
		const whitespace = /(\s*):(\s*)/u.exec(sourceCode.getText().slice(pair.key.range[1], pair.value.range[0]));
		if (whitespace) return {
			beforeColon: whitespace[1],
			afterColon: whitespace[2]
		};
		return null;
	}
	/**
	* Verifies spacing of property conforms to specified options.
	* @param  {ASTNode} node Property node being evaluated.
	* @param {Object} lineOptions Configured singleLine or multiLine options
	* @returns {void}
	*/
	function verifySpacing(node, lineOptions) {
		const actual = getPropertyWhitespace(node);
		if (actual) {
			report(node, "key", actual.beforeColon, lineOptions.beforeColon ? 1 : 0, lineOptions.mode);
			report(node, "value", actual.afterColon, lineOptions.afterColon ? 1 : 0, lineOptions.mode);
		}
	}
	/**
	* Verifies spacing of each property in a list.
	* @param {ASTNode[]} properties List of Property AST nodes.
	* @param {Object} lineOptions Configured singleLine or multiLine options
	* @returns {void}
	*/
	function verifyListSpacing(properties, lineOptions) {
		const length = properties.length;
		for (let i = 0; i < length; i++) verifySpacing(properties[i], lineOptions);
	}
	if (alignmentOptions) return defineAlignmentVisitor(alignmentOptions);
	return defineSpacingVisitor();
	/**
	* Define alignment rule visitor
	*/
	function defineAlignmentVisitor(alignmentOptions) {
		return { YAMLMapping(node) {
			if (isSingleLine(node)) verifyListSpacing(node.pairs.filter(isKeyValueProperty), singleLineOptions);
			else verifyAlignment(node);
		} };
		/**
		* Verifies correct vertical alignment of a group of properties.
		* @param {ASTNode[]} properties List of Property AST nodes.
		* @returns {void}
		*/
		function verifyGroupAlignment(properties) {
			const length = properties.length;
			const widths = properties.map(getKeyWidth);
			const align = alignmentOptions.on;
			let targetWidth = Math.max(...widths);
			let beforeColon, afterColon, mode;
			if (alignmentOptions && length > 1) {
				beforeColon = alignmentOptions.beforeColon ? 1 : 0;
				afterColon = alignmentOptions.afterColon ? 1 : 0;
				mode = alignmentOptions.mode;
			} else {
				beforeColon = multiLineOptions.beforeColon ? 1 : 0;
				afterColon = multiLineOptions.afterColon ? 1 : 0;
				mode = alignmentOptions.mode;
			}
			targetWidth += align === "colon" ? beforeColon : afterColon;
			for (let i = 0; i < length; i++) {
				const property = properties[i];
				const whitespace = getPropertyWhitespace(property);
				if (whitespace) {
					const width = widths[i];
					if (align === "value") {
						report(property, "key", whitespace.beforeColon, beforeColon, mode);
						report(property, "value", whitespace.afterColon, targetWidth - width, mode);
					} else {
						report(property, "key", whitespace.beforeColon, targetWidth - width, mode);
						report(property, "value", whitespace.afterColon, afterColon, mode);
					}
				}
			}
		}
		/**
		* Checks whether a property is a member of the property group it follows.
		* @param {ASTNode} lastMember The last Property known to be in the group.
		* @param {ASTNode} candidate The next Property that might be in the group.
		* @returns {boolean} True if the candidate property is part of the group.
		*/
		function continuesPropertyGroup(lastMember, candidate) {
			const groupEndLine = lastMember.loc.start.line;
			const candidateStartLine = candidate.loc.start.line;
			if (candidateStartLine - groupEndLine <= 1) return true;
			const leadingComments = sourceCode.getCommentsBefore(candidate);
			if (leadingComments.length && leadingComments[0].loc.start.line - groupEndLine <= 1 && candidateStartLine - last(leadingComments).loc.end.line <= 1) {
				for (let i = 1; i < leadingComments.length; i++) if (leadingComments[i].loc.start.line - leadingComments[i - 1].loc.end.line > 1) return false;
				return true;
			}
			return false;
		}
		/**
		* Creates groups of properties.
		* @param  {ASTNode} node ObjectExpression node being evaluated.
		* @returns {Array.<ASTNode[]>} Groups of property AST node lists.
		*/
		function createGroups(node) {
			if (node.pairs.length === 1) return [node.pairs];
			return node.pairs.reduce((groups, property) => {
				const currentGroup = last(groups);
				const prev = last(currentGroup);
				if (!prev || continuesPropertyGroup(prev, property)) currentGroup.push(property);
				else groups.push([property]);
				return groups;
			}, [[]]);
		}
		/**
		* Verifies vertical alignment, taking into account groups of properties.
		* @param  {ASTNode} node ObjectExpression node being evaluated.
		* @returns {void}
		*/
		function verifyAlignment(node) {
			createGroups(node).forEach((group) => {
				const properties = group.filter(isKeyValueProperty);
				if (properties.length > 0 && isSingleLineProperties(properties)) verifyListSpacing(properties, multiLineOptions);
				else verifyGroupAlignment(properties);
			});
		}
	}
	/**
	* Define spacing rule visitor
	*/
	function defineSpacingVisitor() {
		return { YAMLPair(node) {
			if (!isKeyValueProperty(node)) return;
			verifySpacing(node, isSingleLine(node.parent) ? singleLineOptions : multiLineOptions);
		} };
	}
}

//#endregion
//#region src/rules/no-empty-document.ts
var no_empty_document_default = createRule("no-empty-document", {
	meta: {
		docs: {
			description: "disallow empty document",
			categories: ["recommended", "standard"],
			extensionRule: false,
			layout: false
		},
		schema: [],
		messages: { unexpectedEmpty: "Empty documents are forbidden." },
		type: "suggestion"
	},
	create(context) {
		if (!context.sourceCode.parserServices?.isYAML) return {};
		/**
		* Checks if the given node is empty
		*/
		function isEmptyNode(node) {
			if (!node) return true;
			if (node.type === "YAMLWithMeta") return isEmptyNode(node.value);
			return false;
		}
		return { YAMLDocument(node) {
			if (isEmptyNode(node.content)) context.report({
				node,
				messageId: "unexpectedEmpty"
			});
		} };
	}
});

//#endregion
//#region src/rules/no-empty-key.ts
var no_empty_key_default = createRule("no-empty-key", {
	meta: {
		docs: {
			description: "disallow empty mapping keys",
			categories: ["recommended", "standard"],
			extensionRule: false,
			layout: false
		},
		schema: [],
		messages: { unexpectedEmpty: "Empty mapping keys are forbidden." },
		type: "suggestion"
	},
	create(context) {
		if (!context.sourceCode.parserServices?.isYAML) return {};
		/**
		* Checks if the given node is empty
		*/
		function isEmptyNode(node) {
			if (!node) return true;
			if (node.type === "YAMLWithMeta") return isEmptyNode(node.value);
			return false;
		}
		return { YAMLPair(node) {
			if (isEmptyNode(node.key)) context.report({
				node,
				messageId: "unexpectedEmpty"
			});
		} };
	}
});

//#endregion
//#region src/rules/no-empty-mapping-value.ts
var no_empty_mapping_value_default = createRule("no-empty-mapping-value", {
	meta: {
		docs: {
			description: "disallow empty mapping values",
			categories: ["recommended", "standard"],
			extensionRule: false,
			layout: false
		},
		schema: [],
		messages: { unexpectedEmpty: "Empty mapping values are forbidden." },
		type: "suggestion"
	},
	create(context) {
		if (!context.sourceCode.parserServices?.isYAML) return {};
		/**
		* Checks if the given node is empty
		*/
		function isEmptyNode(node) {
			if (!node) return true;
			if (node.type === "YAMLWithMeta") return isEmptyNode(node.value);
			return false;
		}
		return { YAMLPair(node) {
			if (isEmptyNode(node.value)) context.report({
				node,
				messageId: "unexpectedEmpty"
			});
		} };
	}
});

//#endregion
//#region src/rules/no-empty-sequence-entry.ts
var no_empty_sequence_entry_default = createRule("no-empty-sequence-entry", {
	meta: {
		docs: {
			description: "disallow empty sequence entries",
			categories: ["recommended", "standard"],
			extensionRule: false,
			layout: false
		},
		schema: [],
		messages: { unexpectedEmpty: "Empty sequence entries are forbidden." },
		type: "suggestion"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		/**
		* Checks if the given node is empty
		*/
		function isEmptyNode(node) {
			if (!node) return true;
			if (node.type === "YAMLWithMeta") return isEmptyNode(node.value);
			return false;
		}
		return { YAMLSequence(node) {
			if (node.style !== "block") return;
			node.entries.forEach((entry, index) => {
				if (isEmptyNode(entry)) context.report({
					node: getHyphen(node, index) || node,
					messageId: "unexpectedEmpty"
				});
			});
		} };
		/**
		* Get hyphen token from given entry index
		*/
		function getHyphen(node, index) {
			if (index === 0) {
				const token = sourceCode.getFirstToken(node);
				return isHyphen(token) ? token : null;
			}
			const prev = node.entries[index - 1];
			if (prev) {
				const token = sourceCode.getTokenAfter(prev);
				return isHyphen(token) ? token : null;
			}
			const prevHyphen = getHyphen(node, index - 1);
			if (prevHyphen) {
				const token = sourceCode.getTokenAfter(prevHyphen);
				return isHyphen(token) ? token : null;
			}
			return null;
		}
	}
});

//#endregion
//#region src/rules/no-irregular-whitespace.ts
const ALL_IRREGULARS = /[\v\f\u0085\u00a0\u1680\u180e\u2000-\u200b\u2028\u2029\u202f\u205f\u3000\ufeff]/u;
const IRREGULAR_WHITESPACE = /[\v\f\u0085\u00a0\u1680\u180e\u2000-\u200b\u202f\u205f\u3000\ufeff]+/gu;
const IRREGULAR_LINE_TERMINATORS = /[\u2028\u2029]/gu;
var no_irregular_whitespace_default = createRule("no-irregular-whitespace", {
	meta: {
		docs: {
			description: "disallow irregular whitespace",
			categories: ["recommended", "standard"],
			extensionRule: "no-irregular-whitespace",
			layout: false
		},
		schema: [{
			type: "object",
			properties: {
				skipComments: {
					type: "boolean",
					default: false
				},
				skipQuotedScalars: {
					type: "boolean",
					default: true
				}
			},
			additionalProperties: false
		}],
		messages: { disallow: "Irregular whitespace not allowed." },
		type: "problem"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		let errorIndexes = [];
		const options = context.options[0] || {};
		const skipComments = Boolean(options.skipComments);
		const skipQuotedScalars = options.skipQuotedScalars !== false;
		/**
		* Removes errors that occur inside a string node
		* @param node to check for matching errors.
		* @private
		*/
		function removeWhitespaceError(node) {
			const [startIndex, endIndex] = node.range;
			errorIndexes = errorIndexes.filter((errorIndex) => errorIndex < startIndex || endIndex <= errorIndex);
		}
		/**
		* Checks scalar nodes for errors that we are choosing to ignore and calls the relevant methods to remove the errors
		* @param node to check for matching errors.
		* @returns {void}
		* @private
		*/
		function removeInvalidNodeErrorsInScalar(node) {
			if (skipQuotedScalars && (node.style === "double-quoted" || node.style === "single-quoted")) {
				if (ALL_IRREGULARS.test(sourceCode.getText(node))) removeWhitespaceError(node);
			}
		}
		/**
		* Checks comment nodes for errors that we are choosing to ignore and calls the relevant methods to remove the errors
		* @param node to check for matching errors.
		* @private
		*/
		function removeInvalidNodeErrorsInComment(node) {
			if (ALL_IRREGULARS.test(node.value)) removeWhitespaceError(node);
		}
		/**
		* Checks the program source for irregular whitespaces and irregular line terminators
		* @returns {void}
		* @private
		*/
		function checkForIrregularWhitespace() {
			const source = sourceCode.getText();
			let match;
			while ((match = IRREGULAR_WHITESPACE.exec(source)) !== null) errorIndexes.push(match.index);
			while ((match = IRREGULAR_LINE_TERMINATORS.exec(source)) !== null) errorIndexes.push(match.index);
		}
		checkForIrregularWhitespace();
		if (!errorIndexes.length) return {};
		return {
			YAMLScalar: removeInvalidNodeErrorsInScalar,
			"Program:exit"() {
				if (skipComments) sourceCode.getAllComments().forEach(removeInvalidNodeErrorsInComment);
				for (const errorIndex of errorIndexes) context.report({
					loc: sourceCode.getLocFromIndex(errorIndex),
					messageId: "disallow"
				});
			}
		};
	}
});

//#endregion
//#region src/rules/no-multiple-empty-lines.ts
var no_multiple_empty_lines_default = createRule("no-multiple-empty-lines", {
	meta: {
		docs: {
			description: "disallow multiple empty lines",
			categories: ["standard"],
			extensionRule: "no-multiple-empty-lines",
			layout: true
		},
		fixable: "whitespace",
		schema: [{
			type: "object",
			properties: {
				max: {
					type: "integer",
					minimum: 0
				},
				maxEOF: {
					type: "integer",
					minimum: 0
				},
				maxBOF: {
					type: "integer",
					minimum: 0
				}
			},
			required: ["max"],
			additionalProperties: false
		}],
		messages: {
			blankBeginningOfFile: "Too many blank lines at the beginning of file. Max of {{max}} allowed.",
			blankEndOfFile: "Too many blank lines at the end of file. Max of {{max}} allowed.",
			consecutiveBlank: "More than {{max}} blank {{pluralizedLines}} not allowed."
		},
		type: "layout"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const maxOption = context.options[0]?.max ?? 2;
		const options = {
			max: maxOption,
			maxEOF: context.options[0]?.maxEOF ?? maxOption,
			maxBOF: context.options[0]?.maxBOF ?? maxOption
		};
		const allLines = [...sourceCode.lines];
		if (allLines[allLines.length - 1] === "") allLines.pop();
		const ignoreLineIndexes = /* @__PURE__ */ new Set();
		/**
		* Verify
		*/
		function verifyEmptyLines(startLineIndex, endLineIndex) {
			const emptyLineCount = endLineIndex - startLineIndex;
			let messageId, max;
			if (startLineIndex === 0) {
				messageId = "blankBeginningOfFile";
				max = options.maxBOF;
			} else if (endLineIndex === allLines.length) {
				messageId = "blankEndOfFile";
				max = options.maxEOF;
			} else {
				messageId = "consecutiveBlank";
				max = options.max;
			}
			if (emptyLineCount > max) context.report({
				loc: {
					start: {
						line: startLineIndex + max + 1,
						column: 0
					},
					end: {
						line: endLineIndex + 1,
						column: 0
					}
				},
				messageId,
				data: {
					max: String(max),
					pluralizedLines: max === 1 ? "line" : "lines"
				},
				fix(fixer) {
					const rangeStart = sourceCode.getIndexFromLoc({
						line: startLineIndex + max + 1,
						column: 0
					});
					const rangeEnd = endLineIndex < allLines.length ? sourceCode.getIndexFromLoc({
						line: endLineIndex + 1,
						column: 0
					}) : sourceCode.text.length;
					return fixer.removeRange([rangeStart, rangeEnd]);
				}
			});
		}
		return {
			YAMLScalar(node) {
				for (let lineIndex = node.loc.start.line - 1; lineIndex < node.loc.end.line; lineIndex++) ignoreLineIndexes.add(lineIndex);
			},
			"Program:exit"() {
				let startEmptyLineIndex = null;
				for (let lineIndex = 0; lineIndex < allLines.length; lineIndex++) if (!allLines[lineIndex].trim() && !ignoreLineIndexes.has(lineIndex)) startEmptyLineIndex ??= lineIndex;
				else {
					if (startEmptyLineIndex != null) verifyEmptyLines(startEmptyLineIndex, lineIndex);
					startEmptyLineIndex = null;
				}
				if (startEmptyLineIndex != null) verifyEmptyLines(startEmptyLineIndex, allLines.length);
			}
		};
	}
});

//#endregion
//#region src/rules/no-tab-indent.ts
var no_tab_indent_default = createRule("no-tab-indent", {
	meta: {
		docs: {
			description: "disallow tabs for indentation.",
			categories: ["recommended", "standard"],
			extensionRule: false,
			layout: false
		},
		schema: [],
		messages: { disallow: "Unexpected tabs." },
		type: "problem"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		return { Program() {
			const lines = sourceCode.lines;
			for (let lineIndex = 0; lineIndex < lines.length; lineIndex++) {
				const line = lines[lineIndex];
				const res = /^([^\S\t]*(?:-[^\S\t]+)?)\t+/u.exec(line);
				if (res) context.report({
					loc: {
						start: {
							line: lineIndex + 1,
							column: res[1].length
						},
						end: {
							line: lineIndex + 1,
							column: res[0].length
						}
					},
					messageId: "disallow"
				});
			}
		} };
	}
});

//#endregion
//#region src/rules/no-trailing-zeros.ts
var no_trailing_zeros_default = createRule("no-trailing-zeros", {
	meta: {
		docs: {
			description: "disallow trailing zeros for floats",
			categories: ["standard"],
			extensionRule: false,
			layout: true
		},
		fixable: "code",
		schema: [],
		messages: { wrongZeros: "Trailing zeros are not allowed, fix to `{{fixed}}`." },
		type: "layout"
	},
	create(context) {
		if (!context.sourceCode.parserServices?.isYAML) return {};
		return { YAMLScalar(node) {
			if (node.style !== "plain") return;
			else if (typeof node.value !== "number") return;
			const floating = parseFloatingPoint(node.strValue);
			if (!floating) return;
			let { decimalPart } = floating;
			while (decimalPart.endsWith("_")) decimalPart = decimalPart.slice(0, -1);
			if (!decimalPart.endsWith("0")) return;
			while (decimalPart.endsWith("0")) {
				decimalPart = decimalPart.slice(0, -1);
				while (decimalPart.endsWith("_")) decimalPart = decimalPart.slice(0, -1);
			}
			const fixed = decimalPart ? `${floating.sign}${floating.intPart}.${decimalPart}${floating.expPart}` : `${floating.sign}${floating.intPart || "0"}${floating.expPart}`;
			context.report({
				node,
				messageId: "wrongZeros",
				data: { fixed },
				fix(fixer) {
					return fixer.replaceText(node, fixed);
				}
			});
		} };
	}
});
/** Parse floating point number string */
function parseFloatingPoint(str) {
	const parts = str.split(".");
	if (parts.length !== 2) return null;
	let decimalPart, expPart, intPart, sign;
	const expIndex = parts[1].search(/e/iu);
	if (expIndex >= 0) {
		decimalPart = parts[1].slice(0, expIndex);
		expPart = parts[1].slice(expIndex);
	} else {
		decimalPart = parts[1];
		expPart = "";
	}
	if (parts[0].startsWith("-") || parts[0].startsWith("+")) {
		sign = parts[0][0];
		intPart = parts[0].slice(1);
	} else {
		sign = "";
		intPart = parts[0];
	}
	return {
		sign,
		intPart,
		decimalPart,
		expPart
	};
}

//#endregion
//#region src/rules/plain-scalar.ts
const SYMBOLS = new Set([
	":",
	"{",
	"}",
	"[",
	"]",
	",",
	"&",
	"*",
	"#",
	"|",
	"+",
	"%",
	"\"",
	"'",
	"\\"
]);
/**
* String list to RegExp list
*/
function toRegExps(patterns) {
	return patterns.map((p) => new RegExp(p, "u"));
}
/**
* Checks whether given node is string value scalar
*/
function isStringScalar(node) {
	return typeof node.value === "string";
}
var plain_scalar_default = createRule("plain-scalar", {
	meta: {
		docs: {
			description: "require or disallow plain style scalar.",
			categories: ["standard"],
			extensionRule: false,
			layout: false
		},
		fixable: "code",
		schema: [{ enum: ["always", "never"] }, {
			type: "object",
			properties: {
				ignorePatterns: {
					type: "array",
					items: { type: "string" }
				},
				overrides: {
					type: "object",
					properties: { mappingKey: { enum: [
						"always",
						"never",
						null
					] } },
					additionalProperties: false
				}
			},
			additionalProperties: false
		}],
		messages: {
			required: "Must use plain style scalar.",
			disallow: "Must use quoted style scalar."
		},
		type: "layout"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const valueOption = {
			prefer: context.options[0] || "always",
			ignorePatterns: []
		};
		const overridesMappingKey = context.options[1]?.overrides?.mappingKey;
		const keyOption = overridesMappingKey ? {
			prefer: overridesMappingKey,
			ignorePatterns: []
		} : valueOption;
		if (context.options[1]?.ignorePatterns) valueOption.ignorePatterns = toRegExps(context.options[1]?.ignorePatterns);
		else {
			if (valueOption.prefer === "always") valueOption.ignorePatterns = toRegExps([String.raw`[\v\f\u0085\u00a0\u1680\u180e\u2000-\u200b\u2028\u2029\u202f\u205f\u3000\ufeff]`]);
			if (overridesMappingKey && keyOption.prefer === "always") keyOption.ignorePatterns = toRegExps([String.raw`[\v\f\u0085\u00a0\u1680\u180e\u2000-\u200b\u2028\u2029\u202f\u205f\u3000\ufeff]`]);
		}
		let currentDocument;
		/**
		* Check if it can be converted to plain.
		*/
		function canToPlain(node) {
			if (node.value !== node.value.trim()) return false;
			for (let index = 0; index < node.value.length; index++) {
				const char = node.value[index];
				if (SYMBOLS.has(char)) return false;
				if (index === 0) {
					if (char === "-" || char === "?") {
						const next = node.value[index + 1];
						if (next && !next.trim()) return false;
					} else if (char === "!") {
						const next = node.value[index + 1];
						if (next && (!next.trim() || next === "!" || next === "<")) return false;
					}
				}
			}
			const parent = node.parent.type === "YAMLWithMeta" ? node.parent.parent : node.parent;
			if (parent.type === "YAMLPair") {
				if (parent.key === node) {
					const colon = sourceCode.getTokenAfter(node);
					if (colon && colon.value === ":") {
						const next = sourceCode.getTokenAfter(colon);
						if (colon.range[1] === next?.range[0]) return false;
					}
				}
			}
			return true;
		}
		/**
		* Verify node for `always`
		*/
		function verifyAlways(node) {
			if (node.style !== "double-quoted" && node.style !== "single-quoted") return;
			if (!canToPlain(node)) return;
			try {
				if (getStaticYAMLValue(parseForESLint(node.value, { defaultYAMLVersion: currentDocument?.version }).ast) !== node.value) return;
			} catch {
				return;
			}
			context.report({
				node,
				messageId: "required",
				fix(fixer) {
					return fixer.replaceText(node, node.value);
				}
			});
		}
		/**
		* Verify node for `never`
		*/
		function verifyNever(node) {
			if (node.style !== "plain") return;
			const text = node.value;
			context.report({
				node,
				messageId: "disallow",
				fix(fixer) {
					return fixer.replaceText(node, `"${text.replace(/(["\\])/gu, "\\$1").replace(/\r?\n|[\u2028\u2029]/gu, "\\n")}"`);
				}
			});
		}
		/**
		* Checks whether the given node is within key
		*/
		function withinKey(node) {
			const parent = node.parent;
			if (parent.type === "YAMLPair" && parent.key === node) return true;
			const grandParent = parent.parent;
			if (grandParent.type === "YAMLWithMeta") return withinKey(grandParent);
			return false;
		}
		return {
			YAMLDocument(node) {
				currentDocument = node;
			},
			YAMLScalar(node) {
				if (!isStringScalar(node)) return;
				const option = withinKey(node) ? keyOption : valueOption;
				if (option.ignorePatterns.some((p) => p.test(node.value))) return;
				if (option.prefer === "always") verifyAlways(node);
				else verifyNever(node);
			}
		};
	}
});

//#endregion
//#region src/rules/quotes.ts
var quotes_default = createRule("quotes", {
	meta: {
		docs: {
			description: "enforce the consistent use of either double, or single quotes",
			categories: ["standard"],
			extensionRule: false,
			layout: true
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: {
				prefer: { enum: ["double", "single"] },
				avoidEscape: { type: "boolean" }
			},
			additionalProperties: false
		}],
		messages: { wrongQuotes: "Strings must use {{description}}." },
		type: "layout"
	},
	create(context) {
		if (!context.sourceCode.parserServices?.isYAML) return {};
		const objectOption = context.options[0] || {};
		const prefer = objectOption.prefer || "double";
		const avoidEscape = objectOption.avoidEscape !== false;
		return { YAMLScalar(node) {
			let description;
			if (node.style === "double-quoted" && prefer === "single") {
				if (avoidEscape && node.strValue.includes("'")) return;
				let preChar = "";
				for (const char of node.raw) {
					if (preChar === "\\") {
						if (char === "\\" || char === "\"") {
							preChar = "";
							continue;
						}
						return;
					}
					preChar = char;
				}
				description = "singlequote";
			} else if (node.style === "single-quoted" && prefer === "double") {
				if (avoidEscape && (node.strValue.includes("\"") || node.strValue.includes("\\"))) return;
				description = "doublequote";
			} else return;
			context.report({
				node,
				messageId: "wrongQuotes",
				data: { description },
				fix(fixer) {
					const text = node.raw.slice(1, -1);
					if (prefer === "double") return fixer.replaceText(node, `"${text.replace(/''/gu, "'").replace(/(["\\])/gu, "\\$1")}"`);
					return fixer.replaceText(node, `'${text.replace(/\\(["\\])/gu, "$1").replace(/'/gu, "''")}'`);
				}
			});
		} };
	}
});

//#endregion
//#region src/rules/require-string-key.ts
var require_string_key_default = createRule("require-string-key", {
	meta: {
		docs: {
			description: "disallow mapping keys other than strings",
			categories: null,
			extensionRule: false,
			layout: false
		},
		schema: [],
		messages: { expectedString: "The key must be a string." },
		type: "suggestion"
	},
	create(context) {
		if (!context.sourceCode.parserServices?.isYAML) return {};
		let anchors = {};
		/**
		* Find Anchor
		*/
		function findAnchor(alias) {
			const target = {
				anchor: null,
				distance: Infinity
			};
			for (const anchor of anchors[alias.name] || []) if (anchor.range[0] < alias.range[0]) {
				const distance = alias.range[0] - anchor.range[0];
				if (target.distance >= distance) {
					target.anchor = anchor;
					target.distance = distance;
				}
			}
			return target.anchor;
		}
		/**
		* Checks if the given node is string
		*/
		function isStringNode(node) {
			if (!node) return false;
			if (node.type === "YAMLWithMeta") {
				if (node.tag && node.tag.tag === "tag:yaml.org,2002:str") return true;
				return isStringNode(node.value);
			}
			if (node.type === "YAMLAlias") {
				const anchor = findAnchor(node);
				if (!anchor) return false;
				return isStringNode(anchor.parent);
			}
			if (node.type !== "YAMLScalar") return false;
			return typeof node.value === "string";
		}
		return {
			YAMLDocument() {
				anchors = {};
			},
			YAMLAnchor(node) {
				(anchors[node.name] || (anchors[node.name] = [])).push(node);
			},
			YAMLPair(node) {
				if (!isStringNode(node.key)) context.report({
					node: node.key || node,
					messageId: "expectedString"
				});
			}
		};
	}
});

//#endregion
//#region src/utils/calc-shortest-edit-script.ts
const diff = typeof diffModule === "function" ? diffModule : diffModule.default;
/**
* Given the contents of two sequences, returns diff information.
* @param a The first sequence.
* @param b The second sequence.
* @param [options] The options object.
* @param [options.isEqual] A function that returns true if two elements are equal.
* @returns An array of diff objects.
*/
function calcShortestEditScript(a, b) {
	let aIndex = 0;
	let bIndex = 0;
	const result = [];
	diff(a.length, b.length, (aIndex, bIndex) => a[aIndex] === b[bIndex], (nCommon, aCommon, bCommon) => {
		pushDelIns(aIndex, aCommon, bIndex, bCommon);
		aIndex = aCommon + nCommon;
		bIndex = bCommon + nCommon;
		if (nCommon > 0) for (let index = 0; index < nCommon; index++) {
			const elementA = a[aCommon + index];
			const elementB = b[bCommon + index];
			result.push({
				type: "common",
				a: elementA,
				b: elementB
			});
		}
	});
	pushDelIns(aIndex, a.length, bIndex, b.length);
	return result;
	/**
	* Pushes delete and insert sequences to the result.
	* @param aStart The start index of the delete sequence in `a`.
	* @param aEnd The end index of the delete sequence in `a`.
	* @param bStart The start index of the insert sequence in `b`.
	* @param bEnd The end index of the insert sequence in `b`.
	*/
	function pushDelIns(aStart, aEnd, bStart, bEnd) {
		for (const element of a.slice(aStart, aEnd)) result.push({
			type: "delete",
			a: element
		});
		for (const element of b.slice(bStart, bEnd)) result.push({
			type: "insert",
			b: element
		});
	}
}

//#endregion
//#region src/rules/sort-keys.ts
/**
* Checks whether the given string is new line.
*/
function isNewLine(char) {
	return char === "\n" || char === "\r" || char === "\u2028" || char === "\u2029";
}
/**
* Gets the property name of the given `YAMLPair` node.
*/
function getPropertyName(node, sourceCode) {
	const prop = node.key;
	if (prop == null) return "";
	const target = prop.type === "YAMLWithMeta" ? prop.value : prop;
	if (target == null) return "";
	if (target.type === "YAMLScalar" && typeof target.value === "string") return target.value;
	return sourceCode.text.slice(...target.range);
}
var YAMLPairData = class {
	mapping;
	node;
	index;
	anchorAlias;
	cachedName = null;
	get reportLoc() {
		return this.node.key?.loc ?? this.node.loc;
	}
	constructor(mapping, node, index, anchorAlias) {
		this.mapping = mapping;
		this.node = node;
		this.index = index;
		this.anchorAlias = anchorAlias;
	}
	get name() {
		return this.cachedName ??= getPropertyName(this.node, this.mapping.sourceCode);
	}
	getPrev() {
		const prevIndex = this.index - 1;
		return prevIndex >= 0 ? this.mapping.pairs[prevIndex] : null;
	}
};
var YAMLMappingData = class {
	node;
	sourceCode;
	anchorAliasMap;
	cachedProperties = null;
	constructor(node, sourceCode, anchorAliasMap) {
		this.node = node;
		this.sourceCode = sourceCode;
		this.anchorAliasMap = anchorAliasMap;
	}
	get pairs() {
		return this.cachedProperties ??= this.node.pairs.map((e, index) => new YAMLPairData(this, e, index, this.anchorAliasMap.get(e)));
	}
	getPath(sourceCode) {
		let path = "";
		let curr = this.node;
		let p = curr.parent;
		while (p) {
			if (p.type === "YAMLPair") {
				const name = getPropertyName(p, sourceCode);
				if (/^[$a-z_][\w$]*$/iu.test(name)) path = `.${name}${path}`;
				else path = `[${JSON.stringify(name)}]${path}`;
			} else if (p.type === "YAMLSequence") path = `[${p.entries.indexOf(curr)}]${path}`;
			curr = p;
			p = curr.parent;
		}
		if (path.startsWith(".")) path = path.slice(1);
		return path;
	}
};
/**
* Check if given options are CompatibleWithESLintOptions
*/
function isCompatibleWithESLintOptions(options) {
	if (options.length === 0) return true;
	if (typeof options[0] === "string" || options[0] == null) return true;
	return false;
}
/**
* Build function which check that the given 2 names are in specific order.
*/
function buildValidatorFromType$1(order, insensitive, natural) {
	let compare = natural ? ([a, b]) => naturalCompare(a, b) <= 0 : ([a, b]) => a <= b;
	if (insensitive) {
		const baseCompare = compare;
		compare = ([a, b]) => baseCompare([a.toLowerCase(), b.toLowerCase()]);
	}
	if (order === "desc") {
		const baseCompare = compare;
		compare = (args) => baseCompare(args.reverse());
	}
	return (a, b) => compare([a.name, b.name]);
}
/**
* Parse options
*/
function parseOptions$1(options, sourceCode) {
	if (isCompatibleWithESLintOptions(options)) {
		const type = options[0] ?? "asc";
		const obj = options[1] ?? {};
		const insensitive = obj.caseSensitive === false;
		const natural = Boolean(obj.natural);
		const minKeys = obj.minKeys ?? 2;
		const allowLineSeparatedGroups = obj.allowLineSeparatedGroups || false;
		return [{
			isTargetMapping: (data) => data.node.pairs.length >= minKeys,
			ignore: () => false,
			isValidOrder: buildValidatorFromType$1(type, insensitive, natural),
			orderText: `${natural ? "natural " : ""}${insensitive ? "insensitive " : ""}${type}ending`,
			allowLineSeparatedGroups
		}];
	}
	return options.map((opt) => {
		const order = opt.order;
		const pathPattern = new RegExp(opt.pathPattern);
		const hasProperties = opt.hasProperties ?? [];
		const minKeys = opt.minKeys ?? 2;
		const allowLineSeparatedGroups = opt.allowLineSeparatedGroups || false;
		if (!Array.isArray(order)) {
			const type = order.type ?? "asc";
			const insensitive = order.caseSensitive === false;
			const natural = Boolean(order.natural);
			return {
				isTargetMapping,
				ignore: () => false,
				isValidOrder: buildValidatorFromType$1(type, insensitive, natural),
				orderText: `${natural ? "natural " : ""}${insensitive ? "insensitive " : ""}${type}ending`,
				allowLineSeparatedGroups
			};
		}
		const parsedOrder = [];
		for (const o of order) if (typeof o === "string") parsedOrder.push({
			test: (data) => data.name === o,
			isValidNestOrder: () => true
		});
		else {
			const keyPattern = o.keyPattern ? new RegExp(o.keyPattern) : null;
			const nestOrder = o.order ?? {};
			const type = nestOrder.type ?? "asc";
			const insensitive = nestOrder.caseSensitive === false;
			const natural = Boolean(nestOrder.natural);
			parsedOrder.push({
				test: (data) => keyPattern ? keyPattern.test(data.name) : true,
				isValidNestOrder: buildValidatorFromType$1(type, insensitive, natural)
			});
		}
		return {
			isTargetMapping,
			ignore: (data) => parsedOrder.every((p) => !p.test(data)),
			isValidOrder(a, b) {
				for (const p of parsedOrder) {
					const matchA = p.test(a);
					const matchB = p.test(b);
					if (!matchA || !matchB) {
						if (matchA) return true;
						if (matchB) return false;
						continue;
					}
					return p.isValidNestOrder(a, b);
				}
				return false;
			},
			orderText: "specified",
			allowLineSeparatedGroups
		};
		/**
		* Checks whether given node is verify target
		*/
		function isTargetMapping(data) {
			if (data.node.pairs.length < minKeys) return false;
			if (hasProperties.length > 0) {
				const names = new Set(data.pairs.map((p) => p.name));
				if (!hasProperties.every((name) => names.has(name))) return false;
			}
			return pathPattern.test(data.getPath(sourceCode));
		}
	});
}
const ALLOW_ORDER_TYPES = ["asc", "desc"];
const ORDER_OBJECT_SCHEMA$1 = {
	type: "object",
	properties: {
		type: { enum: ALLOW_ORDER_TYPES },
		caseSensitive: { type: "boolean" },
		natural: { type: "boolean" }
	},
	additionalProperties: false
};
var sort_keys_default = createRule("sort-keys", {
	meta: {
		docs: {
			description: "require mapping keys to be sorted",
			categories: null,
			extensionRule: false,
			layout: false
		},
		fixable: "code",
		schema: { oneOf: [{
			type: "array",
			items: {
				type: "object",
				properties: {
					pathPattern: { type: "string" },
					hasProperties: {
						type: "array",
						items: { type: "string" }
					},
					order: { oneOf: [{
						type: "array",
						items: { anyOf: [{ type: "string" }, {
							type: "object",
							properties: {
								keyPattern: { type: "string" },
								order: ORDER_OBJECT_SCHEMA$1
							},
							additionalProperties: false
						}] },
						uniqueItems: true
					}, ORDER_OBJECT_SCHEMA$1] },
					minKeys: {
						type: "integer",
						minimum: 2
					},
					allowLineSeparatedGroups: { type: "boolean" }
				},
				required: ["pathPattern", "order"],
				additionalProperties: false
			},
			minItems: 1
		}, {
			type: "array",
			items: [{ enum: ALLOW_ORDER_TYPES }, {
				type: "object",
				properties: {
					caseSensitive: { type: "boolean" },
					natural: { type: "boolean" },
					minKeys: {
						type: "integer",
						minimum: 2
					},
					allowLineSeparatedGroups: { type: "boolean" }
				},
				additionalProperties: false
			}],
			additionalItems: false
		}] },
		messages: {
			shouldBeBefore: "Expected mapping keys to be in {{orderText}} order. '{{thisName}}' should be before '{{targetName}}'.",
			shouldBeAfter: "Expected mapping keys to be in {{orderText}} order. '{{thisName}}' should be after '{{targetName}}'."
		},
		type: "suggestion"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const parsedOptions = parseOptions$1(context.options, sourceCode);
		/**
		* Checks whether the given two pairs are in should be kept order.
		*/
		function shouldKeepOrder(prevData, nextData) {
			if (prevData.anchorAlias.aliases.size === 0 && prevData.anchorAlias.anchors.size === 0 || nextData.anchorAlias.aliases.size === 0 && nextData.anchorAlias.anchors.size === 0) return false;
			for (const aliasName of nextData.anchorAlias.aliases) if (prevData.anchorAlias.anchors.has(aliasName)) return true;
			for (const anchorName of nextData.anchorAlias.anchors) if (prevData.anchorAlias.aliases.has(anchorName)) return true;
			return false;
		}
		/**
		* Check ignore
		*/
		function ignore(data, option) {
			if (!data.node.key && !data.node.value) return true;
			return option.ignore(data);
		}
		/**
		* Group YAML pairs.
		*/
		function groupingPairs(pairs, option) {
			const groups = [];
			let group = [];
			let prev = null;
			for (const pair of pairs) {
				if (ignore(pair, option)) {
					prev = pair;
					continue;
				}
				if (prev && option.allowLineSeparatedGroups && hasBlankLine(prev, pair)) {
					if (group.length > 0) {
						groups.push(group);
						group = [];
					}
				}
				group.push(pair);
				prev = pair;
			}
			if (group.length > 0) groups.push(group);
			return groups;
		}
		/**
		* Sort pairs by bubble sort.
		*/
		function bubbleSort(pairs, option) {
			const l = pairs.length;
			const result = [...pairs];
			let swapped;
			do {
				swapped = false;
				for (let nextIndex = 1; nextIndex < l; nextIndex++) {
					const prevIndex = nextIndex - 1;
					if (option.isValidOrder(result[prevIndex], result[nextIndex]) || shouldKeepOrder(result[prevIndex], result[nextIndex])) continue;
					[result[prevIndex], result[nextIndex]] = [result[nextIndex], result[prevIndex]];
					swapped = true;
				}
			} while (swapped);
			return result;
		}
		/**
		* Verify for pairs order
		*/
		function verifyPairs(pairs, option) {
			const editScript = calcShortestEditScript(pairs, bubbleSort(pairs, option));
			for (let index = 0; index < editScript.length; index++) {
				const edit = editScript[index];
				if (edit.type !== "delete") continue;
				const insertEditIndex = editScript.findIndex((e) => e.type === "insert" && e.b === edit.a);
				if (insertEditIndex === -1) continue;
				if (index < insertEditIndex) {
					const target = findInsertAfterTarget(edit.a, insertEditIndex);
					if (!target) continue;
					context.report({
						loc: edit.a.reportLoc,
						messageId: "shouldBeAfter",
						data: {
							thisName: edit.a.name,
							targetName: target.name,
							orderText: option.orderText
						},
						*fix(fixer) {
							if (edit.a.mapping.node.style === "flow") yield* fixToMoveDownForFlow(fixer, edit.a, target);
							else yield* fixToMoveDownForBlock(fixer, edit.a, target);
						}
					});
				} else {
					const target = findInsertBeforeTarget(edit.a, insertEditIndex);
					if (!target) continue;
					context.report({
						loc: edit.a.reportLoc,
						messageId: "shouldBeBefore",
						data: {
							thisName: edit.a.name,
							targetName: target.name,
							orderText: option.orderText
						},
						*fix(fixer) {
							if (edit.a.mapping.node.style === "flow") yield* fixToMoveUpForFlow(fixer, edit.a, target);
							else yield* fixToMoveUpForBlock(fixer, edit.a, target);
						}
					});
				}
			}
			/**
			* Find insert after target
			*/
			function findInsertAfterTarget(pair, insertEditIndex) {
				let candidate = null;
				for (let index = insertEditIndex - 1; index >= 0; index--) {
					const edit = editScript[index];
					if (edit.type === "delete" && edit.a === pair) break;
					if (edit.type !== "common") continue;
					candidate = edit.a;
					break;
				}
				const pairIndex = pairs.indexOf(pair);
				if (candidate) for (let index = pairIndex + 1; index < pairs.length; index++) {
					const element = pairs[index];
					if (element === candidate) return candidate;
					if (shouldKeepOrder(pair, element)) break;
				}
				let lastTarget = null;
				for (let index = pairIndex + 1; index < pairs.length; index++) {
					const element = pairs[index];
					if (option.isValidOrder(element, pair) && !shouldKeepOrder(pair, element)) {
						lastTarget = element;
						continue;
					}
					return lastTarget;
				}
				return lastTarget;
			}
			/**
			* Find insert before target
			*/
			function findInsertBeforeTarget(pair, insertEditIndex) {
				let candidate = null;
				for (let index = insertEditIndex + 1; index < editScript.length; index++) {
					const edit = editScript[index];
					if (edit.type === "delete" && edit.a === pair) break;
					if (edit.type !== "common") continue;
					candidate = edit.a;
					break;
				}
				const pairIndex = pairs.indexOf(pair);
				if (candidate) for (let index = pairIndex - 1; index >= 0; index--) {
					const element = pairs[index];
					if (element === candidate) return candidate;
					if (shouldKeepOrder(element, pair)) break;
				}
				let lastTarget = null;
				for (let index = pairIndex - 1; index >= 0; index--) {
					const element = pairs[index];
					if (option.isValidOrder(pair, element) && !shouldKeepOrder(element, pair)) {
						lastTarget = element;
						continue;
					}
					return lastTarget;
				}
				return lastTarget;
			}
		}
		/**
		* Checks whether the given two properties have a blank line between them.
		*/
		function hasBlankLine(prev, next) {
			const tokenOrNodes = [...sourceCode.getTokensBetween(prev.node, next.node, { includeComments: true }), next.node];
			let prevLoc = prev.node.loc;
			for (const t of tokenOrNodes) {
				const loc = t.loc;
				if (loc.start.line - prevLoc.end.line > 1) return true;
				prevLoc = loc;
			}
			return false;
		}
		let pairStack = {
			upper: null,
			anchors: /* @__PURE__ */ new Set(),
			aliases: /* @__PURE__ */ new Set()
		};
		const anchorAliasMap = /* @__PURE__ */ new Map();
		return {
			YAMLPair() {
				pairStack = {
					upper: pairStack,
					anchors: /* @__PURE__ */ new Set(),
					aliases: /* @__PURE__ */ new Set()
				};
			},
			YAMLAnchor(node) {
				if (pairStack) pairStack.anchors.add(node.name);
			},
			YAMLAlias(node) {
				if (pairStack) pairStack.aliases.add(node.name);
			},
			"YAMLPair:exit"(node) {
				anchorAliasMap.set(node, pairStack);
				const { anchors, aliases } = pairStack;
				pairStack = pairStack.upper;
				pairStack.anchors = new Set([...pairStack.anchors, ...anchors]);
				pairStack.aliases = new Set([...pairStack.aliases, ...aliases]);
			},
			"YAMLMapping:exit"(node) {
				const data = new YAMLMappingData(node, sourceCode, anchorAliasMap);
				const option = parsedOptions.find((o) => o.isTargetMapping(data));
				if (!option) return;
				for (const pairs of groupingPairs(data.pairs, option)) verifyPairs(pairs, option);
			}
		};
		/**
		* Fix by moving the node after the target node for flow.
		*/
		function* fixToMoveDownForFlow(fixer, data, moveTarget) {
			const beforeToken = sourceCode.getTokenBefore(data.node);
			let insertCode, removeRange, insertTargetToken;
			const afterCommaToken = sourceCode.getTokenAfter(data.node);
			if (isComma(afterCommaToken)) {
				removeRange = [beforeToken.range[1], afterCommaToken.range[1]];
				const moveTargetAfterToken = sourceCode.getTokenAfter(moveTarget.node);
				if (isComma(moveTargetAfterToken)) {
					insertTargetToken = moveTargetAfterToken;
					insertCode = sourceCode.text.slice(...removeRange);
				} else {
					insertTargetToken = sourceCode.getLastToken(moveTarget.node);
					insertCode = sourceCode.text.slice(beforeToken.range[1], afterCommaToken.range[0]);
					insertCode = `,${insertCode}`;
				}
			} else if (isComma(beforeToken)) {
				removeRange = [beforeToken.range[0], data.node.range[1]];
				insertCode = sourceCode.text.slice(...removeRange);
				insertTargetToken = sourceCode.getLastToken(moveTarget.node);
			} else {
				removeRange = [beforeToken.range[1], data.node.range[1]];
				insertCode = `,${sourceCode.text.slice(...removeRange)}`;
				insertTargetToken = sourceCode.getLastToken(moveTarget.node);
			}
			yield fixer.removeRange(removeRange);
			yield fixer.insertTextAfterRange(insertTargetToken.range, insertCode);
		}
		/**
		* Fix by moving the node before the target node for flow.
		*/
		function* fixToMoveUpForFlow(fixer, data, moveTarget) {
			const beforeCommaToken = sourceCode.getTokenBefore(data.node);
			let insertCode, removeRange, insertTargetToken;
			const afterCommaToken = sourceCode.getTokenAfter(data.node);
			const moveTargetBeforeToken = sourceCode.getTokenBefore(moveTarget.node);
			if (isComma(afterCommaToken)) {
				removeRange = [beforeCommaToken.range[1], afterCommaToken.range[1]];
				insertCode = sourceCode.text.slice(...removeRange);
				insertTargetToken = moveTargetBeforeToken;
			} else {
				removeRange = [beforeCommaToken.range[0], data.node.range[1]];
				if (isComma(moveTargetBeforeToken)) {
					insertCode = sourceCode.text.slice(...removeRange);
					insertTargetToken = sourceCode.getTokenBefore(moveTargetBeforeToken);
				} else {
					insertCode = `${sourceCode.text.slice(beforeCommaToken.range[1], data.node.range[1])},`;
					insertTargetToken = moveTargetBeforeToken;
				}
			}
			yield fixer.insertTextAfterRange(insertTargetToken.range, insertCode);
			yield fixer.removeRange(removeRange);
		}
		/**
		* Fix by moving the node after the target node for block.
		*/
		function* fixToMoveDownForBlock(fixer, data, moveTarget) {
			const nodeLocs = getPairRangeForBlock(data.node);
			const moveTargetLocs = getPairRangeForBlock(moveTarget.node);
			if (nodeLocs.loc.start.column === 0) {
				const removeRange = [getNewlineStartIndex(nodeLocs.range[0]), nodeLocs.range[1]];
				const moveTargetRange = [getNewlineStartIndex(moveTargetLocs.range[0]), moveTargetLocs.range[1]];
				const insertCode = sourceCode.text.slice(...removeRange);
				const isAtFileStart = nodeLocs.loc.start.line === 1;
				if (isAtFileStart) {
					const removeRangeEnd = nodeLocs.range[1];
					const len = sourceCode.text.length;
					if (removeRangeEnd < len) {
						const ch = sourceCode.text[removeRangeEnd];
						if (isNewLine(ch)) if (ch === "\r" && removeRangeEnd + 1 < len && sourceCode.text[removeRangeEnd + 1] === "\n") removeRange[1] += 2;
						else removeRange[1] += 1;
					}
				}
				yield fixer.removeRange(removeRange);
				yield fixer.insertTextAfterRange(moveTargetRange, `${isAtFileStart ? "\n" : ""}${insertCode}`);
			} else {
				const nextToken = sourceCode.getTokenAfter(data.node, { includeComments: true });
				const removeRange = [data.node.range[0], nextToken.range[0]];
				yield fixer.removeRange(removeRange);
				const insertCode = `\n${sourceCode.text.slice(sourceCode.getIndexFromLoc({
					line: nodeLocs.loc.start.line,
					column: 0
				}), data.node.range[0]).replace(/\S/g, " ")}${sourceCode.text.slice(data.node.range[0], nodeLocs.range[1])}`;
				yield fixer.insertTextAfterRange(moveTargetLocs.range, insertCode);
			}
		}
		/**
		* Fix by moving the node before the target node for block.
		*/
		function* fixToMoveUpForBlock(fixer, data, moveTarget) {
			const nodeLocs = getPairRangeForBlock(data.node);
			const moveTargetLocs = getPairRangeForBlock(moveTarget.node);
			if (moveTargetLocs.loc.start.column === 0) {
				const removeRange = [getNewlineStartIndex(nodeLocs.range[0]), nodeLocs.range[1]];
				const moveTargetRange = [getNewlineStartIndex(moveTargetLocs.range[0]), moveTargetLocs.range[1]];
				const insertCode = sourceCode.text.slice(...removeRange);
				yield fixer.insertTextBeforeRange(moveTargetRange, `${insertCode}${moveTargetLocs.loc.start.line === 1 ? "\n" : ""}`);
				yield fixer.removeRange(removeRange);
			} else {
				const diffIndent = nodeLocs.indentColumn - moveTargetLocs.indentColumn;
				const insertCode = `${sourceCode.text.slice(nodeLocs.range[0] + diffIndent, nodeLocs.range[1])}\n${sourceCode.text.slice(nodeLocs.range[0], nodeLocs.range[0] + diffIndent)}`;
				yield fixer.insertTextBeforeRange(moveTargetLocs.range, insertCode);
				const removeRange = [getNewlineStartIndex(nodeLocs.range[0]), nodeLocs.range[1]];
				yield fixer.removeRange(removeRange);
			}
		}
		/**
		* Get start index of newline
		*/
		function getNewlineStartIndex(nextIndex) {
			for (let index = nextIndex; index >= 0; index--) {
				const char = sourceCode.text[index];
				if (isNewLine(sourceCode.text[index])) {
					if (sourceCode.text[index - 1] === "\r" && char === "\n") return index - 1;
					return index;
				}
			}
			return 0;
		}
		/**
		* Get range from given pair
		*/
		function getPairRangeForBlock(node) {
			let end;
			const afterToken = sourceCode.getTokenAfter(node, {
				includeComments: true,
				filter: (t) => !isCommentToken(t) || node.loc.end.line < t.loc.start.line
			});
			if (!afterToken || node.loc.end.line < afterToken.loc.start.line) {
				const line = afterToken ? afterToken.loc.start.line - 1 : node.loc.end.line;
				end = {
					loc: {
						line,
						column: sourceCode.lines[line - 1].length
					},
					get index() {
						return sourceCode.getIndexFromLoc(this.loc);
					}
				};
			} else end = {
				index: node.range[1],
				loc: node.loc.end
			};
			const beforeToken = sourceCode.getTokenBefore(node);
			if (beforeToken) {
				const next = sourceCode.getTokenAfter(beforeToken, { includeComments: true });
				if (beforeToken.loc.end.line < next.loc.start.line || beforeToken.loc.end.line < node.loc.start.line) {
					const start = {
						line: beforeToken.loc.end.line < next.loc.start.line ? next.loc.start.line : node.loc.start.line,
						column: 0
					};
					return {
						range: [sourceCode.getIndexFromLoc(start), end.index],
						loc: {
							start,
							end: end.loc
						},
						indentColumn: next.loc.start.column
					};
				}
				return {
					range: [beforeToken.range[1], end.index],
					loc: {
						start: beforeToken.loc.end,
						end: end.loc
					},
					indentColumn: node.range[0] - beforeToken.range[1]
				};
			}
			let next = node;
			for (const beforeComment of sourceCode.getTokensBefore(node, { includeComments: true }).reverse()) {
				if (beforeComment.loc.end.line + 1 < next.loc.start.line) {
					const start = {
						line: next.loc.start.line,
						column: 0
					};
					return {
						range: [sourceCode.getIndexFromLoc(start), end.index],
						loc: {
							start,
							end: end.loc
						},
						indentColumn: next.loc.start.column
					};
				}
				next = beforeComment;
			}
			const start = {
				line: node.loc.start.line,
				column: 0
			};
			return {
				range: [sourceCode.getIndexFromLoc(start), end.index],
				loc: {
					start,
					end: end.loc
				},
				indentColumn: node.loc.start.column
			};
		}
	}
});

//#endregion
//#region src/rules/sort-sequence-values.ts
var YAMLEntryData = class {
	sequence;
	node;
	index;
	anchorAlias;
	cached = null;
	cachedRange = null;
	cachedAroundTokens = null;
	get reportLoc() {
		if (this.node) return this.node.loc;
		const aroundTokens = this.aroundTokens;
		return {
			start: aroundTokens.before.loc.end,
			end: aroundTokens.after.loc.start
		};
	}
	get range() {
		if (this.node) return this.node.range;
		if (this.cachedRange) return this.cachedRange;
		const aroundTokens = this.aroundTokens;
		return this.cachedRange = [aroundTokens.before.range[1], aroundTokens.after.range[0]];
	}
	get aroundTokens() {
		if (this.cachedAroundTokens) return this.cachedAroundTokens;
		const sourceCode = this.sequence.sourceCode;
		if (this.node) return this.cachedAroundTokens = {
			before: sourceCode.getTokenBefore(this.node),
			after: sourceCode.getTokenAfter(this.node)
		};
		const before = this.index > 0 ? this.sequence.entries[this.index - 1].aroundTokens.after : sourceCode.getFirstToken(this.sequence.node);
		return this.cachedAroundTokens = {
			before,
			after: sourceCode.getTokenAfter(before)
		};
	}
	constructor(sequence, node, index, anchorAlias) {
		this.sequence = sequence;
		this.node = node;
		this.index = index;
		this.anchorAlias = anchorAlias;
	}
	get value() {
		return (this.cached ?? (this.cached = { value: this.node == null ? null : getStaticYAMLValue(this.node) })).value;
	}
};
var YAMLSequenceData = class {
	node;
	sourceCode;
	anchorAliasMap;
	cachedEntries = null;
	constructor(node, sourceCode, anchorAliasMap) {
		this.node = node;
		this.sourceCode = sourceCode;
		this.anchorAliasMap = anchorAliasMap;
	}
	get entries() {
		return this.cachedEntries ??= this.node.entries.map((e, index) => new YAMLEntryData(this, e, index, this.anchorAliasMap.get(e)));
	}
};
/**
* Build function which check that the given 2 names are in specific order.
*/
function buildValidatorFromType(order, insensitive, natural) {
	let compareValue = ([a, b]) => a <= b;
	let compareText = compareValue;
	if (natural) compareText = ([a, b]) => naturalCompare(a, b) <= 0;
	if (insensitive) {
		const baseCompareText = compareText;
		compareText = ([a, b]) => baseCompareText([a.toLowerCase(), b.toLowerCase()]);
	}
	if (order === "desc") {
		const baseCompareText = compareText;
		compareText = (args) => baseCompareText(args.reverse());
		const baseCompareValue = compareValue;
		compareValue = (args) => baseCompareValue(args.reverse());
	}
	return (a, b) => {
		if (typeof a.value === "string" && typeof b.value === "string") return compareText([a.value, b.value]);
		const type = getYAMLPrimitiveType(a.value);
		if (type && type === getYAMLPrimitiveType(b.value)) return compareValue([a.value, b.value]);
		return true;
	};
}
/**
* Parse options
*/
function parseOptions(options, sourceCode) {
	return options.map((opt) => {
		const order = opt.order;
		const pathPattern = new RegExp(opt.pathPattern);
		const minValues = opt.minValues ?? 2;
		if (!Array.isArray(order)) {
			const type = order.type ?? "asc";
			const insensitive = order.caseSensitive === false;
			const natural = Boolean(order.natural);
			return {
				isTargetArray,
				ignore: () => false,
				isValidOrder: buildValidatorFromType(type, insensitive, natural),
				orderText(data) {
					if (typeof data.value === "string") return `${natural ? "natural " : ""}${insensitive ? "insensitive " : ""}${type}ending`;
					return `${type}ending`;
				}
			};
		}
		const parsedOrder = [];
		for (const o of order) if (typeof o === "string") parsedOrder.push({
			test: (v) => v.value === o,
			isValidNestOrder: () => true
		});
		else {
			const valuePattern = o.valuePattern ? new RegExp(o.valuePattern) : null;
			const nestOrder = o.order ?? {};
			const type = nestOrder.type ?? "asc";
			const insensitive = nestOrder.caseSensitive === false;
			const natural = Boolean(nestOrder.natural);
			parsedOrder.push({
				test: (v) => valuePattern ? Boolean(getYAMLPrimitiveType(v.value)) && valuePattern.test(String(v.value)) : true,
				isValidNestOrder: buildValidatorFromType(type, insensitive, natural)
			});
		}
		return {
			isTargetArray,
			ignore: (v) => parsedOrder.every((p) => !p.test(v)),
			isValidOrder(a, b) {
				for (const p of parsedOrder) {
					const matchA = p.test(a);
					const matchB = p.test(b);
					if (!matchA || !matchB) {
						if (matchA) return true;
						if (matchB) return false;
						continue;
					}
					return p.isValidNestOrder(a, b);
				}
				return false;
			},
			orderText: () => "specified"
		};
		/**
		* Checks whether given node data is verify target
		*/
		function isTargetArray(data) {
			if (data.node.entries.length < minValues) return false;
			let path = "";
			let curr = data.node;
			let p = curr.parent;
			while (p) {
				if (p.type === "YAMLPair") {
					const name = getPropertyName(p);
					if (/^[$a-z_][\w$]*$/iu.test(name)) path = `.${name}${path}`;
					else path = `[${JSON.stringify(name)}]${path}`;
				} else if (p.type === "YAMLSequence") path = `[${p.entries.indexOf(curr)}]${path}`;
				curr = p;
				p = curr.parent;
			}
			if (path.startsWith(".")) path = path.slice(1);
			return pathPattern.test(path);
		}
	});
	/**
	* Gets the property name of the given `YAMLPair` node.
	*/
	function getPropertyName(node) {
		const prop = node.key;
		if (prop == null) return "";
		const target = prop.type === "YAMLWithMeta" ? prop.value : prop;
		if (target == null) return "";
		if (target.type === "YAMLScalar" && typeof target.value === "string") return target.value;
		return sourceCode.text.slice(...target.range);
	}
}
/**
* Get the type name from given value when value is primitive like value
*/
function getYAMLPrimitiveType(val) {
	const t = typeof val;
	if (t === "string" || t === "number" || t === "boolean" || t === "bigint") return t;
	if (val === null) return "null";
	if (val === void 0) return "undefined";
	if (val instanceof RegExp) return "regexp";
	return null;
}
const ORDER_OBJECT_SCHEMA = {
	type: "object",
	properties: {
		type: { enum: ["asc", "desc"] },
		caseSensitive: { type: "boolean" },
		natural: { type: "boolean" }
	},
	additionalProperties: false
};
var sort_sequence_values_default = createRule("sort-sequence-values", {
	meta: {
		docs: {
			description: "require sequence values to be sorted",
			categories: null,
			extensionRule: false,
			layout: false
		},
		fixable: "code",
		schema: {
			type: "array",
			items: {
				type: "object",
				properties: {
					pathPattern: { type: "string" },
					order: { oneOf: [{
						type: "array",
						items: { anyOf: [{ type: "string" }, {
							type: "object",
							properties: {
								valuePattern: { type: "string" },
								order: ORDER_OBJECT_SCHEMA
							},
							additionalProperties: false
						}] },
						uniqueItems: true
					}, ORDER_OBJECT_SCHEMA] },
					minValues: {
						type: "integer",
						minimum: 2
					}
				},
				required: ["pathPattern", "order"],
				additionalProperties: false
			},
			minItems: 1
		},
		messages: {
			shouldBeBefore: "Expected sequence values to be in {{orderText}} order. '{{thisValue}}' should be before '{{targetValue}}'.",
			shouldBeAfter: "Expected sequence values to be in {{orderText}} order. '{{thisValue}}' should be after '{{targetValue}}'."
		},
		type: "suggestion"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const parsedOptions = parseOptions(context.options, sourceCode);
		/**
		* Checks whether the given two entries are in should be kept order.
		*/
		function shouldKeepOrder(prevData, nextData) {
			if (prevData.anchorAlias.aliases.size === 0 && prevData.anchorAlias.anchors.size === 0 || nextData.anchorAlias.aliases.size === 0 && nextData.anchorAlias.anchors.size === 0) return false;
			for (const aliasName of nextData.anchorAlias.aliases) if (prevData.anchorAlias.anchors.has(aliasName)) return true;
			for (const anchorName of nextData.anchorAlias.anchors) if (prevData.anchorAlias.aliases.has(anchorName)) return true;
			return false;
		}
		/**
		* Sort entries by bubble sort.
		*/
		function bubbleSort(entries, option) {
			const l = entries.length;
			const result = [...entries];
			let swapped;
			do {
				swapped = false;
				for (let nextIndex = 1; nextIndex < l; nextIndex++) {
					const prevIndex = nextIndex - 1;
					if (option.isValidOrder(result[prevIndex], result[nextIndex]) || shouldKeepOrder(result[prevIndex], result[nextIndex])) continue;
					[result[prevIndex], result[nextIndex]] = [result[nextIndex], result[prevIndex]];
					swapped = true;
				}
			} while (swapped);
			return result;
		}
		/**
		* Verify for sequence entries
		*/
		function verifyArrayElements(entries, option) {
			const editScript = calcShortestEditScript(entries, bubbleSort(entries, option));
			for (let index = 0; index < editScript.length; index++) {
				const edit = editScript[index];
				if (edit.type !== "delete") continue;
				const insertEditIndex = editScript.findIndex((e) => e.type === "insert" && e.b === edit.a);
				if (insertEditIndex === -1) continue;
				if (index < insertEditIndex) {
					const target = findInsertAfterTarget(edit.a, insertEditIndex);
					if (!target) continue;
					context.report({
						loc: edit.a.reportLoc,
						messageId: "shouldBeAfter",
						data: {
							thisValue: toText(edit.a),
							targetValue: toText(target),
							orderText: option.orderText(edit.a)
						},
						*fix(fixer) {
							if (edit.a.sequence.node.style === "flow") yield* fixToMoveDownForFlow(fixer, edit.a, target);
							else yield* fixToMoveDownForBlock(fixer, edit.a, target);
						}
					});
				} else {
					const target = findInsertBeforeTarget(edit.a, insertEditIndex);
					if (!target) continue;
					context.report({
						loc: edit.a.reportLoc,
						messageId: "shouldBeBefore",
						data: {
							thisValue: toText(edit.a),
							targetValue: toText(target),
							orderText: option.orderText(edit.a)
						},
						*fix(fixer) {
							if (edit.a.sequence.node.style === "flow") yield* fixToMoveUpForFlow(fixer, edit.a, target);
							else yield* fixToMoveUpForBlock(fixer, edit.a, target);
						}
					});
				}
			}
			/**
			* Find insert after target
			*/
			function findInsertAfterTarget(entry, insertEditIndex) {
				let candidate = null;
				for (let index = insertEditIndex - 1; index >= 0; index--) {
					const edit = editScript[index];
					if (edit.type === "delete" && edit.a === entry) break;
					if (edit.type !== "common") continue;
					candidate = edit.a;
					break;
				}
				const entryIndex = entries.indexOf(entry);
				if (candidate) for (let index = entryIndex + 1; index < entries.length; index++) {
					const element = entries[index];
					if (element === candidate) return candidate;
					if (shouldKeepOrder(entry, element)) break;
				}
				let lastTarget = null;
				for (let index = entryIndex + 1; index < entries.length; index++) {
					const element = entries[index];
					if (option.isValidOrder(element, entry) && !shouldKeepOrder(entry, element)) {
						lastTarget = element;
						continue;
					}
					return lastTarget;
				}
				return lastTarget;
			}
			/**
			* Find insert before target
			*/
			function findInsertBeforeTarget(entry, insertEditIndex) {
				let candidate = null;
				for (let index = insertEditIndex + 1; index < editScript.length; index++) {
					const edit = editScript[index];
					if (edit.type === "delete" && edit.a === entry) break;
					if (edit.type !== "common") continue;
					candidate = edit.a;
					break;
				}
				const entryIndex = entries.indexOf(entry);
				if (candidate) for (let index = entryIndex - 1; index >= 0; index--) {
					const element = entries[index];
					if (element === candidate) return candidate;
					if (shouldKeepOrder(element, entry)) break;
				}
				let lastTarget = null;
				for (let index = entryIndex - 1; index >= 0; index--) {
					const element = entries[index];
					if (option.isValidOrder(entry, element) && !shouldKeepOrder(element, entry)) {
						lastTarget = element;
						continue;
					}
					return lastTarget;
				}
				return lastTarget;
			}
		}
		/**
		* Convert to display text.
		*/
		function toText(data) {
			if (getYAMLPrimitiveType(data.value)) return String(data.value);
			return sourceCode.getText(data.node);
		}
		let entryStack = {
			upper: null,
			anchors: /* @__PURE__ */ new Set(),
			aliases: /* @__PURE__ */ new Set()
		};
		const anchorAliasMap = /* @__PURE__ */ new Map();
		return {
			"YAMLSequence > *"(node) {
				if (!node.parent.entries.includes(node)) return;
				entryStack = {
					upper: entryStack,
					anchors: /* @__PURE__ */ new Set(),
					aliases: /* @__PURE__ */ new Set()
				};
				if (node.type === "YAMLAlias") entryStack.aliases.add(node.name);
			},
			YAMLAnchor(node) {
				if (entryStack) entryStack.anchors.add(node.name);
			},
			YAMLAlias(node) {
				if (entryStack) entryStack.aliases.add(node.name);
			},
			"YAMLSequence > *:exit"(node) {
				if (!node.parent.entries.includes(node)) return;
				anchorAliasMap.set(node, entryStack);
				const { anchors, aliases } = entryStack;
				entryStack = entryStack.upper;
				entryStack.anchors = new Set([...entryStack.anchors, ...anchors]);
				entryStack.aliases = new Set([...entryStack.aliases, ...aliases]);
			},
			"YAMLSequence:exit"(node) {
				const data = new YAMLSequenceData(node, sourceCode, anchorAliasMap);
				const option = parsedOptions.find((o) => o.isTargetArray(data));
				if (!option) return;
				verifyArrayElements(data.entries.filter((d) => !option.ignore(d)), option);
			}
		};
		/**
		* Fix by moving the node after the target node for flow.
		*/
		function* fixToMoveDownForFlow(fixer, data, moveTarget) {
			const beforeToken = data.aroundTokens.before;
			const afterToken = data.aroundTokens.after;
			let insertCode, removeRange, insertTargetToken;
			if (isComma(afterToken)) {
				removeRange = [beforeToken.range[1], afterToken.range[1]];
				const moveTargetAfterToken = moveTarget.aroundTokens.after;
				if (isComma(moveTargetAfterToken)) {
					insertTargetToken = moveTargetAfterToken;
					insertCode = sourceCode.text.slice(...removeRange);
				} else {
					insertTargetToken = moveTarget.node ? sourceCode.getLastToken(moveTarget.node) : moveTarget.aroundTokens.before;
					insertCode = sourceCode.text.slice(beforeToken.range[1], afterToken.range[0]);
					insertCode = `,${insertCode}`;
				}
			} else if (isComma(beforeToken)) {
				removeRange = [beforeToken.range[0], data.range[1]];
				insertCode = sourceCode.text.slice(...removeRange);
				insertTargetToken = moveTarget.node ? sourceCode.getLastToken(moveTarget.node) : moveTarget.aroundTokens.before;
			} else {
				removeRange = [beforeToken.range[1], data.range[1]];
				insertCode = `,${sourceCode.text.slice(...removeRange)}`;
				insertTargetToken = moveTarget.node ? sourceCode.getLastToken(moveTarget.node) : moveTarget.aroundTokens.before;
			}
			yield fixer.removeRange(removeRange);
			yield fixer.insertTextAfterRange(insertTargetToken.range, insertCode);
		}
		/**
		* Fix by moving the node before the target node for flow.
		*/
		function* fixToMoveUpForFlow(fixer, data, moveTarget) {
			const beforeToken = data.aroundTokens.before;
			const afterToken = data.aroundTokens.after;
			let insertCode, removeRange, insertTargetToken;
			if (isComma(afterToken)) {
				removeRange = [beforeToken.range[1], afterToken.range[1]];
				insertCode = sourceCode.text.slice(...removeRange);
				insertTargetToken = moveTarget.aroundTokens.before;
			} else {
				removeRange = [beforeToken.range[0], data.range[1]];
				if (isComma(moveTarget.aroundTokens.before)) {
					insertCode = sourceCode.text.slice(...removeRange);
					insertTargetToken = sourceCode.getTokenBefore(moveTarget.aroundTokens.before);
				} else {
					insertCode = `${sourceCode.text.slice(beforeToken.range[1], data.range[1])},`;
					insertTargetToken = moveTarget.aroundTokens.before;
				}
			}
			yield fixer.insertTextAfterRange(insertTargetToken.range, insertCode);
			yield fixer.removeRange(removeRange);
		}
		/**
		* Fix by moving the node after the target node for block.
		*/
		function* fixToMoveDownForBlock(fixer, data, moveTarget) {
			const moveDataList = data.sequence.entries.slice(data.index, moveTarget.index + 1);
			let replacementCodeRange = getBlockEntryRange(data);
			for (const target of moveDataList.reverse()) {
				const range = getBlockEntryRange(target);
				yield fixer.replaceTextRange(range, sourceCode.text.slice(...replacementCodeRange));
				replacementCodeRange = range;
			}
		}
		/**
		* Fix by moving the node before the target node for block.
		*/
		function* fixToMoveUpForBlock(fixer, data, moveTarget) {
			const moveDataList = data.sequence.entries.slice(moveTarget.index, data.index + 1);
			let replacementCodeRange = getBlockEntryRange(data);
			for (const target of moveDataList) {
				const range = getBlockEntryRange(target);
				yield fixer.replaceTextRange(range, sourceCode.text.slice(...replacementCodeRange));
				replacementCodeRange = range;
			}
		}
		/**
		* Get range of entry
		*/
		function getBlockEntryRange(data) {
			return [getBlockEntryStartOffset(data), getBlockEntryEndOffset(data)];
		}
		/**
		* Get start offset of entry
		*/
		function getBlockEntryStartOffset(data) {
			const beforeHyphenToken = sourceCode.getTokenBefore(data.aroundTokens.before);
			if (!beforeHyphenToken) {
				const comment = sourceCode.getTokenBefore(data.aroundTokens.before, { includeComments: true });
				if (comment && data.aroundTokens.before.loc.start.column <= comment.loc.start.column) return comment.range[0];
				return data.aroundTokens.before.range[0];
			}
			let next = sourceCode.getTokenAfter(beforeHyphenToken, { includeComments: true });
			while (beforeHyphenToken.loc.end.line === next.loc.start.line && next.range[1] < data.aroundTokens.before.range[0]) next = sourceCode.getTokenAfter(next, { includeComments: true });
			return next.range[0];
		}
		/**
		* Get start offset of entry
		*/
		function getBlockEntryEndOffset(data) {
			const valueEndToken = data.node ?? data.aroundTokens.before;
			let last = valueEndToken;
			let afterToken = sourceCode.getTokenAfter(last, { includeComments: true });
			while (afterToken && valueEndToken.loc.end.line === afterToken.loc.start.line) {
				last = afterToken;
				afterToken = sourceCode.getTokenAfter(last, { includeComments: true });
			}
			return last.range[1];
		}
	}
});

//#endregion
//#region src/rules/spaced-comment.ts
/**
* Escapes the control characters of a given string.
* @param {string} s A string to escape.
* @returns {string} An escaped string.
*/
function escapeText(s) {
	return `(?:${escapeStringRegexp(s)})`;
}
/**
* Escapes the control characters of a given string.
* And adds a repeat flag.
* @param {string} s A string to escape.
* @returns {string} An escaped string.
*/
function escapeAndRepeat(s) {
	return `${escapeText(s)}+`;
}
/**
* Creates string pattern for exceptions.
* Generated pattern:
*
* 1. A space or an exception pattern sequence.
* @param {string[]} exceptions An exception pattern list.
* @returns {string} A regular expression string for exceptions.
*/
function createExceptionsPattern(exceptions) {
	let pattern = "";
	if (exceptions.length === 0) pattern += "\\s";
	else {
		pattern += "(?:\\s|";
		if (exceptions.length === 1) pattern += escapeAndRepeat(exceptions[0]);
		else {
			pattern += "(?:";
			pattern += exceptions.map(escapeAndRepeat).join("|");
			pattern += ")";
		}
		pattern += "$)";
	}
	return pattern;
}
/**
* Creates RegExp object for `always` mode.
* Generated pattern for beginning of comment:
*
* 1. First, a marker or nothing.
* 2. Next, a space or an exception pattern sequence.
* @param {string[]} markers A marker list.
* @param {string[]} exceptions An exception pattern list.
* @returns {RegExp} A RegExp object for the beginning of a comment in `always` mode.
*/
function createAlwaysStylePattern(markers, exceptions) {
	let pattern = "^";
	if (markers.length === 1) pattern += escapeText(markers[0]);
	else {
		pattern += "(?:";
		pattern += markers.map(escapeText).join("|");
		pattern += ")";
	}
	pattern += "?";
	pattern += createExceptionsPattern(exceptions);
	return new RegExp(pattern, "u");
}
/**
* Creates RegExp object for `never` mode.
* Generated pattern for beginning of comment:
*
* 1. First, a marker or nothing (captured).
* 2. Next, a space or a tab.
* @param {string[]} markers A marker list.
* @returns {RegExp} A RegExp object for `never` mode.
*/
function createNeverStylePattern(markers) {
	const pattern = `^(${markers.map(escapeText).join("|")})?[ \t]+`;
	return new RegExp(pattern, "u");
}
var spaced_comment_default = createRule("spaced-comment", {
	meta: {
		docs: {
			description: "enforce consistent spacing after the `#` in a comment",
			categories: ["standard"],
			extensionRule: "spaced-comment",
			layout: false
		},
		fixable: "whitespace",
		schema: [{ enum: ["always", "never"] }, {
			type: "object",
			properties: {
				exceptions: {
					type: "array",
					items: { type: "string" }
				},
				markers: {
					type: "array",
					items: { type: "string" }
				}
			},
			additionalProperties: false
		}],
		messages: {
			unexpectedSpaceAfterMarker: "Unexpected space after marker ({{refChar}}) in comment.",
			expectedExceptionAfter: "Expected exception block, space after '{{refChar}}' in comment.",
			unexpectedSpaceAfter: "Unexpected space after '{{refChar}}' in comment.",
			expectedSpaceAfter: "Expected space after '{{refChar}}' in comment."
		},
		type: "suggestion"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		if (!sourceCode.parserServices?.isYAML) return {};
		const requireSpace = context.options[0] !== "never";
		const config = context.options[1] || {};
		const markers = config.markers || [];
		const exceptions = config.exceptions || [];
		const styleRules = {
			beginRegex: requireSpace ? createAlwaysStylePattern(markers, exceptions) : createNeverStylePattern(markers),
			hasExceptions: exceptions.length > 0,
			captureMarker: new RegExp(`^(${markers.map(escapeText).join("|")})`, "u"),
			markers: new Set(markers)
		};
		/**
		* Reports a beginning spacing error with an appropriate message.
		* @param {ASTNode} node A comment node to check.
		* @param {string} messageId An error message to report.
		* @param {Array} match An array of match results for markers.
		* @param {string} refChar Character used for reference in the error message.
		* @returns {void}
		*/
		function reportBegin(node, messageId, match, refChar) {
			context.report({
				node,
				fix(fixer) {
					const start = node.range[0];
					let end = start + 1;
					if (requireSpace) {
						if (match) end += match[0].length;
						return fixer.insertTextAfterRange([start, end], " ");
					}
					end += match[0].length;
					return fixer.replaceTextRange([start, end], `#${match?.[1] ? match[1] : ""}`);
				},
				messageId,
				data: { refChar }
			});
		}
		/**
		* Reports a given comment if it's invalid.
		* @param {ASTNode} node a comment node to check.
		* @returns {void}
		*/
		function checkCommentForSpace(node) {
			if (node.value.length === 0 || styleRules.markers.has(node.value)) return;
			const beginMatch = styleRules.beginRegex.exec(node.value);
			if (requireSpace) {
				if (!beginMatch) {
					const hasMarker = styleRules.captureMarker.exec(node.value);
					const marker = hasMarker ? `#${hasMarker[0]}` : "#";
					if (styleRules.hasExceptions) reportBegin(node, "expectedExceptionAfter", hasMarker, marker);
					else reportBegin(node, "expectedSpaceAfter", hasMarker, marker);
				}
			} else if (beginMatch) if (!beginMatch[1]) reportBegin(node, "unexpectedSpaceAfter", beginMatch, "#");
			else reportBegin(node, "unexpectedSpaceAfterMarker", beginMatch, beginMatch[1]);
		}
		return { Program() {
			sourceCode.getAllComments().forEach(checkCommentForSpace);
		} };
	}
});

//#endregion
//#region src/rules/vue-custom-block/no-parsing-error.ts
var no_parsing_error_default = createRule("vue-custom-block/no-parsing-error", {
	meta: {
		docs: {
			description: "disallow parsing errors in Vue custom blocks",
			categories: ["recommended", "standard"],
			extensionRule: false,
			layout: false
		},
		schema: [],
		messages: {},
		type: "problem"
	},
	create(context, { customBlock }) {
		if (!customBlock) return {};
		const parseError = context.sourceCode.parserServices.parseError;
		if (parseError && typeof parseError === "object") {
			let loc = void 0;
			if ("column" in parseError && "lineNumber" in parseError) loc = {
				line: parseError.lineNumber,
				column: parseError.column
			};
			return { Program(node) {
				context.report({
					node,
					loc,
					message: parseError.message
				});
			} };
		}
		return {};
	}
});

//#endregion
//#region src/utils/rules.ts
const rules$1 = [
	block_mapping_colon_indicator_newline_default,
	block_mapping_question_indicator_newline_default,
	block_mapping_default,
	block_sequence_hyphen_indicator_newline_default,
	block_sequence_default,
	file_extension_default,
	flow_mapping_curly_newline_default,
	flow_mapping_curly_spacing_default,
	flow_sequence_bracket_newline_default,
	flow_sequence_bracket_spacing_default,
	indent_default,
	key_name_casing_default,
	key_spacing_default,
	no_empty_document_default,
	no_empty_key_default,
	no_empty_mapping_value_default,
	no_empty_sequence_entry_default,
	no_irregular_whitespace_default,
	no_multiple_empty_lines_default,
	no_tab_indent_default,
	no_trailing_zeros_default,
	plain_scalar_default,
	quotes_default,
	require_string_key_default,
	sort_keys_default,
	sort_sequence_values_default,
	spaced_comment_default,
	no_parsing_error_default
];

//#endregion
//#region src/configs/flat/base.ts
var base_default = [{ plugins: { get yml() {
	return src_default;
} } }, {
	files: [
		"*.yaml",
		"**/*.yaml",
		"*.yml",
		"**/*.yml"
	],
	language: "yml/yaml",
	rules: {
		"no-irregular-whitespace": "off",
		"no-unused-vars": "off",
		"spaced-comment": "off"
	}
}];

//#endregion
//#region src/configs/flat/recommended.ts
var recommended_default = [...base_default, { rules: {
	"yml/no-empty-document": "error",
	"yml/no-empty-key": "error",
	"yml/no-empty-mapping-value": "error",
	"yml/no-empty-sequence-entry": "error",
	"yml/no-irregular-whitespace": "error",
	"yml/no-tab-indent": "error",
	"yml/vue-custom-block/no-parsing-error": "error"
} }];

//#endregion
//#region src/configs/flat/standard.ts
var standard_default = [...base_default, { rules: {
	"yml/block-mapping-colon-indicator-newline": "error",
	"yml/block-mapping-question-indicator-newline": "error",
	"yml/block-mapping": "error",
	"yml/block-sequence-hyphen-indicator-newline": "error",
	"yml/block-sequence": "error",
	"yml/flow-mapping-curly-newline": "error",
	"yml/flow-mapping-curly-spacing": "error",
	"yml/flow-sequence-bracket-newline": "error",
	"yml/flow-sequence-bracket-spacing": "error",
	"yml/indent": "error",
	"yml/key-spacing": "error",
	"yml/no-empty-document": "error",
	"yml/no-empty-key": "error",
	"yml/no-empty-mapping-value": "error",
	"yml/no-empty-sequence-entry": "error",
	"yml/no-irregular-whitespace": "error",
	"yml/no-multiple-empty-lines": "error",
	"yml/no-tab-indent": "error",
	"yml/no-trailing-zeros": "error",
	"yml/plain-scalar": "error",
	"yml/quotes": "error",
	"yml/spaced-comment": "error",
	"yml/vue-custom-block/no-parsing-error": "error"
} }];

//#endregion
//#region src/configs/flat/prettier.ts
var prettier_default = [...base_default, { rules: {
	"yml/block-mapping-colon-indicator-newline": "off",
	"yml/block-mapping-question-indicator-newline": "off",
	"yml/block-sequence-hyphen-indicator-newline": "off",
	"yml/flow-mapping-curly-newline": "off",
	"yml/flow-mapping-curly-spacing": "off",
	"yml/flow-sequence-bracket-newline": "off",
	"yml/flow-sequence-bracket-spacing": "off",
	"yml/indent": "off",
	"yml/key-spacing": "off",
	"yml/no-multiple-empty-lines": "off",
	"yml/no-trailing-zeros": "off",
	"yml/quotes": "off"
} }];

//#endregion
//#region package.json
var name$1 = "eslint-plugin-yml";
var version$1 = "3.3.1";

//#endregion
//#region src/meta.ts
var meta_exports = /* @__PURE__ */ __exportAll({
	name: () => name,
	version: () => version
});
const name = name$1;
const version = version$1;

//#endregion
//#region src/language/yaml-source-code.ts
/**
* @fileoverview The YAMLSourceCode class.
*/
const commentParser = new ConfigCommentParser();
/**
* Pattern to match ESLint inline configuration comments in YAML.
* Matches: eslint, eslint-disable, eslint-enable, eslint-disable-line, eslint-disable-next-line
*/
const INLINE_CONFIG = /^\s*eslint(?:-enable|-disable(?:(?:-next)?-line)?)?(?:\s|$)/u;
/**
* YAML Source Code Object
*/
var YAMLSourceCode = class extends TextSourceCodeBase {
	hasBOM;
	parserServices;
	visitorKeys;
	tokenStore;
	#steps = null;
	#cacheTokensAndComments = null;
	#inlineConfigComments = null;
	/**
	* Creates a new instance.
	*/
	constructor(config) {
		super({
			ast: config.ast,
			text: config.text
		});
		this.hasBOM = Boolean(config.hasBOM);
		this.parserServices = config.parserServices;
		this.visitorKeys = config.visitorKeys || {};
		this.tokenStore = new TokenStore({
			tokens: [...config.ast.tokens, ...config.ast.comments],
			isComment: (token) => token.type === "Block"
		});
	}
	traverse() {
		if (this.#steps != null) return this.#steps;
		const steps = [];
		this.#steps = steps;
		const root = this.ast;
		steps.push(new CallMethodStep({
			target: "onCodePathStart",
			args: [{}, root]
		}));
		traverseNodes(root, {
			enterNode(n) {
				steps.push(new VisitNodeStep({
					target: n,
					phase: 1,
					args: [n]
				}));
			},
			leaveNode(n) {
				steps.push(new VisitNodeStep({
					target: n,
					phase: 2,
					args: [n]
				}));
			}
		});
		steps.push(new CallMethodStep({
			target: "onCodePathEnd",
			args: [{}, root]
		}));
		return steps;
	}
	/**
	* Gets all tokens and comments.
	*/
	get tokensAndComments() {
		return this.#cacheTokensAndComments ??= [...this.ast.tokens, ...this.ast.comments].sort((a, b) => a.range[0] - b.range[0]);
	}
	getLines() {
		return this.lines;
	}
	getAllComments() {
		return this.tokenStore.getAllComments();
	}
	/**
	* Returns an array of all inline configuration nodes found in the source code.
	* This includes eslint-disable, eslint-enable, eslint-disable-line,
	* eslint-disable-next-line, and eslint (for inline config) comments.
	*/
	getInlineConfigNodes() {
		if (!this.#inlineConfigComments) this.#inlineConfigComments = this.ast.comments.filter((comment) => INLINE_CONFIG.test(comment.value));
		return this.#inlineConfigComments;
	}
	/**
	* Returns directives that enable or disable rules along with any problems
	* encountered while parsing the directives.
	*/
	getDisableDirectives() {
		const problems = [];
		const directives = [];
		this.getInlineConfigNodes().forEach((comment) => {
			const directive = commentParser.parseDirective(comment.value);
			if (!directive) return;
			const { label, value, justification } = directive;
			if (label === "eslint-disable-line" && comment.loc.start.line !== comment.loc.end.line) {
				const message = `${label} comment should not span multiple lines.`;
				problems.push({
					ruleId: null,
					message,
					loc: comment.loc
				});
				return;
			}
			switch (label) {
				case "eslint-disable":
				case "eslint-enable":
				case "eslint-disable-next-line":
				case "eslint-disable-line": {
					const directiveType = label.slice(7);
					directives.push(new Directive({
						type: directiveType,
						node: comment,
						value,
						justification
					}));
					break;
				}
			}
		});
		return {
			problems,
			directives
		};
	}
	/**
	* Returns inline rule configurations along with any problems
	* encountered while parsing the configurations.
	*/
	applyInlineConfig() {
		const problems = [];
		const configs = [];
		this.getInlineConfigNodes().forEach((comment) => {
			const directive = commentParser.parseDirective(comment.value);
			if (!directive) return;
			const { label, value } = directive;
			if (label === "eslint") {
				const parseResult = commentParser.parseJSONLikeConfig(value);
				if (parseResult.ok) configs.push({
					config: { rules: parseResult.config },
					loc: comment.loc
				});
				else problems.push({
					ruleId: null,
					message: parseResult.error.message,
					loc: comment.loc
				});
			}
		});
		return {
			configs,
			problems
		};
	}
	getNodeByRangeIndex(index) {
		let node = find([this.ast]);
		if (!node) return null;
		while (true) {
			const child = find(this._getChildren(node));
			if (!child) return node;
			node = child;
		}
		/**
		* Finds a node that contains the given index.
		*/
		function find(nodes) {
			for (const node of nodes) if (node.range[0] <= index && index < node.range[1]) return node;
			return null;
		}
	}
	getFirstToken(node, options) {
		return this.tokenStore.getFirstToken(node, options);
	}
	getFirstTokens(node, options) {
		return this.tokenStore.getFirstTokens(node, options);
	}
	getLastToken(node, options) {
		return this.tokenStore.getLastToken(node, options);
	}
	getLastTokens(node, options) {
		return this.tokenStore.getLastTokens(node, options);
	}
	getTokenBefore(node, options) {
		return this.tokenStore.getTokenBefore(node, options);
	}
	getTokensBefore(node, options) {
		return this.tokenStore.getTokensBefore(node, options);
	}
	getTokenAfter(node, options) {
		return this.tokenStore.getTokenAfter(node, options);
	}
	getTokensAfter(node, options) {
		return this.tokenStore.getTokensAfter(node, options);
	}
	getFirstTokenBetween(left, right, options) {
		return this.tokenStore.getFirstTokenBetween(left, right, options);
	}
	getFirstTokensBetween(left, right, options) {
		return this.tokenStore.getFirstTokensBetween(left, right, options);
	}
	getLastTokenBetween(left, right, options) {
		return this.tokenStore.getLastTokenBetween(left, right, options);
	}
	getLastTokensBetween(left, right, options) {
		return this.tokenStore.getLastTokensBetween(left, right, options);
	}
	getTokens(node, options) {
		return this.tokenStore.getTokens(node, options);
	}
	getTokensBetween(left, right, options) {
		return this.tokenStore.getTokensBetween(left, right, options);
	}
	getCommentsInside(nodeOrToken) {
		return this.tokenStore.getCommentsInside(nodeOrToken);
	}
	getCommentsBefore(nodeOrToken) {
		return this.tokenStore.getCommentsBefore(nodeOrToken);
	}
	getCommentsAfter(nodeOrToken) {
		return this.tokenStore.getCommentsAfter(nodeOrToken);
	}
	commentsExistBetween(first, second) {
		return this.tokenStore.commentsExistBetween(first, second);
	}
	isSpaceBetween(first, second) {
		const [left, right] = first.range[1] <= second.range[0] ? [first, second] : [second, first];
		return this.tokenStore.isSpaceBetween(left, right);
	}
	/**
	* Compatibility for ESLint's SourceCode API
	* @deprecated YAML does not have scopes
	*/
	getScope(node) {
		if (node?.type !== "Program") return null;
		return createFakeGlobalScope(this.ast);
	}
	/**
	* Compatibility for ESLint's SourceCode API
	* @deprecated YAML does not have scopes
	*/
	get scopeManager() {
		return {
			scopes: [],
			globalScope: createFakeGlobalScope(this.ast),
			acquire: (node) => {
				if (node.type === "Program") return createFakeGlobalScope(this.ast);
				return null;
			},
			getDeclaredVariables: () => [],
			addGlobals: () => {}
		};
	}
	/**
	* Compatibility for ESLint's SourceCode API
	* @deprecated
	*/
	isSpaceBetweenTokens(first, second) {
		return this.isSpaceBetween(first, second);
	}
	_getChildren(node) {
		const keys = this.visitorKeys[node.type] || [];
		const children = [];
		for (const key of keys) {
			const value = node[key];
			if (Array.isArray(value)) {
				for (const element of value) if (isNode(element)) children.push(element);
			} else if (isNode(value)) children.push(value);
		}
		return children;
	}
};
/**
* Determines whether the given value is a YAML AST node.
*/
function isNode(value) {
	return typeof value === "object" && value !== null && typeof value.type === "string" && Array.isArray(value.range) && Boolean(value.loc) && typeof value.loc === "object";
}
/**
* Creates a fake global scope for YAML files.
* @deprecated YAML does not have scopes
*/
function createFakeGlobalScope(node) {
	const fakeGlobalScope = {
		type: "global",
		block: node,
		set: /* @__PURE__ */ new Map(),
		through: [],
		childScopes: [],
		variableScope: null,
		variables: [],
		references: [],
		functionExpressionScope: false,
		isStrict: false,
		upper: null,
		implicit: {
			variables: [],
			set: /* @__PURE__ */ new Map()
		}
	};
	fakeGlobalScope.variableScope = fakeGlobalScope;
	return fakeGlobalScope;
}

//#endregion
//#region src/language/yaml-language.ts
/**
* The YAML language implementation for ESLint.
*/
var YAMLLanguage = class {
	/**
	* The type of file to read.
	*/
	fileType = "text";
	/**
	* The line number at which the parser starts counting.
	*/
	lineStart = 1;
	/**
	* The column number at which the parser starts counting.
	*/
	columnStart = 0;
	/**
	* The name of the key that holds the type of the node.
	*/
	nodeTypeKey = "type";
	/**
	* Validates the language options.
	*/
	validateLanguageOptions(_languageOptions) {}
	normalizeLanguageOptions(languageOptions) {
		return {
			ecmaVersion: "latest",
			...languageOptions,
			parserOptions: { ...languageOptions.parserOptions }
		};
	}
	/**
	* Parses the given file into an AST.
	*/
	parse(file, context) {
		const text = file.body;
		try {
			return {
				ok: true,
				ast: parseYAML(text, {
					filePath: file.path,
					defaultYAMLVersion: context.languageOptions?.parserOptions?.defaultYAMLVersion
				})
			};
		} catch (error) {
			const message = error instanceof Error ? error.message : String(error);
			const parseError = error;
			return {
				ok: false,
				errors: [{
					message,
					line: parseError.lineNumber ?? 1,
					column: parseError.column ?? 1
				}]
			};
		}
	}
	/**
	* Creates a new SourceCode object for the given file and parse result.
	*/
	createSourceCode(file, parseResult) {
		return new YAMLSourceCode({
			text: file.body,
			ast: parseResult.ast,
			hasBOM: file.bom,
			parserServices: { isYAML: true },
			visitorKeys: VisitorKeys
		});
	}
};

//#endregion
//#region src/index.ts
const configs = {
	base: base_default,
	recommended: recommended_default,
	standard: standard_default,
	prettier: prettier_default,
	"flat/base": base_default,
	"flat/recommended": recommended_default,
	"flat/standard": standard_default,
	"flat/prettier": prettier_default
};
const rules = Object.fromEntries(rules$1.map((r) => [r.meta.docs.ruleName, r]));
const languages = { yaml: new YAMLLanguage() };
var src_default = {
	meta: meta_exports,
	configs,
	rules,
	languages
};

//#endregion
export { configs, src_default as default, languages, meta_exports as meta, rules };