import { t as __exportAll } from "./chunk-pbuEa-1d.js";
import module from "node:module";
import { Chars, FirstConsumedChars, canReorder, followPaths, getCapturingGroupNumber, getClosestAncestor, getConsumedChars, getEffectiveMaximumRepetition, getFirstCharAfter, getFirstConsumedChar, getFirstConsumedCharAfter, getLengthRange, getLongestPrefix, getMatchingDirection, getMatchingDirectionFromAssertionKind, hasSomeAncestor, hasSomeDescendant, hasStrings, invertMatchingDirection, isEmpty, isEmptyBackreference, isPotentiallyEmpty, isPotentiallyZeroLength, isStrictBackreference, isZeroLength, matchesAllCharacters, matchesNoCharacters, toCache, toCharSet, toUnicodeSet } from "regexp-ast-analysis";
import { RegExpParser, RegExpValidator, parseRegExpLiteral, visitRegExpAST } from "@eslint-community/regexpp";
import * as eslintUtils from "@eslint-community/eslint-utils";
import { CALL, CONSTRUCT, READ, ReferenceTracker, hasSideEffect, isCommentToken, isOpeningBracketToken, isOpeningParenToken } from "@eslint-community/eslint-utils";
import { CharSet, CombinedTransformer, DFA, JS, NFA, Transformers, isDisjointWith, transform, visitAst } from "refa";
import * as jsdocTypeParser from "jsdoc-type-pratt-parser";
import * as commentParser from "comment-parser";
import { analyse } from "scslre";
//#region lib/utils/replacements-utils.ts
function parseReplacementsForString(text) {
	return baseParseReplacements([...text].map((s) => ({ value: s })), () => ({}));
}
function baseParseReplacements(chars, getData) {
	const elements = [];
	let token;
	let index = 0;
	while (token = chars[index++]) {
		if (token.value === "$") {
			const next = chars[index++];
			if (next) {
				if (next.value === "$" || next.value === "&" || next.value === "`" || next.value === "'") {
					elements.push({
						type: "DollarElement",
						kind: next.value,
						...getData(token, next)
					});
					continue;
				}
				if (parseNumberRef(token, next)) continue;
				if (parseNamedRef(token, next)) continue;
				index--;
			}
		}
		elements.push({
			type: "CharacterElement",
			value: token.value,
			...getData(token, token)
		});
	}
	return elements;
	function parseNumberRef(dollarToken, startToken) {
		if (!/^\d$/u.test(startToken.value)) return false;
		if (startToken.value === "0") {
			const next = chars[index++];
			if (next) {
				if (/^[1-9]$/u.test(next.value)) {
					const ref = Number(next.value);
					elements.push({
						type: "ReferenceElement",
						ref,
						refText: startToken.value + next.value,
						...getData(dollarToken, next)
					});
					return true;
				}
				index--;
			}
			return false;
		}
		const ref = Number(startToken.value);
		elements.push({
			type: "ReferenceElement",
			ref,
			refText: startToken.value,
			...getData(dollarToken, startToken)
		});
		return true;
	}
	function parseNamedRef(dollarToken, startToken) {
		if (startToken.value !== "<") return false;
		const startIndex = index;
		let t;
		while (t = chars[index++]) if (t.value === ">") {
			const ref = chars.slice(startIndex, index - 1).map((c) => c.value).join("");
			elements.push({
				type: "ReferenceElement",
				ref,
				refText: ref,
				...getData(dollarToken, t)
			});
			return true;
		}
		index = startIndex;
		return false;
	}
}
//#endregion
//#region lib/utils/string-literal-parser/tokenizer.ts
const CP_BACK_SLASH$1 = "\\".codePointAt(0);
const CP_BACKTICK$1 = "`".codePointAt(0);
const CP_CR = "\r".codePointAt(0);
const CP_LF = "\n".codePointAt(0);
const CP_OPENING_BRACE$1 = "{".codePointAt(0);
const CP_a = "a".codePointAt(0);
const CP_A = "A".codePointAt(0);
const CP_n = "n".codePointAt(0);
const CP_r = "r".codePointAt(0);
const CP_t = "t".codePointAt(0);
const CP_b = "b".codePointAt(0);
const CP_v = "v".codePointAt(0);
const CP_f = "f".codePointAt(0);
const CP_u = "u".codePointAt(0);
const CP_x = "x".codePointAt(0);
const CP_0 = "0".codePointAt(0);
const CP_7 = "7".codePointAt(0);
const CP_8 = "8".codePointAt(0);
const CP_9 = "9".codePointAt(0);
var Tokenizer = class {
	source;
	pos;
	end;
	ecmaVersion;
	constructor(source, options) {
		this.source = source;
		this.pos = options.start;
		this.end = options.end ?? null;
		this.ecmaVersion = options.ecmaVersion;
	}
	*parseTokens(quote) {
		const inTemplate = quote === CP_BACKTICK$1;
		const endIndex = this.end ?? this.source.length;
		while (this.pos < endIndex) {
			const start = this.pos;
			const cp = this.source.codePointAt(start);
			if (cp == null) throw new Error("Unterminated string constant");
			this.pos = inc(start, cp);
			if (cp === quote) break;
			if (cp === CP_BACK_SLASH$1) {
				const { value, kind } = this.readEscape(inTemplate);
				yield {
					type: "EscapeToken",
					kind,
					value,
					range: [start, this.pos]
				};
			} else if (cp === CP_CR || cp === CP_LF) if (inTemplate) {
				if (cp === CP_CR && this.source.codePointAt(this.pos) === CP_LF) this.pos++;
				yield {
					type: "CharacterToken",
					value: "\n",
					range: [start, this.pos]
				};
			} else throw new Error("Unterminated string constant");
			else {
				if (this.ecmaVersion >= 2019 && (cp === 8232 || cp === 8233) && !inTemplate) throw new Error("Unterminated string constant");
				yield {
					type: "CharacterToken",
					value: String.fromCodePoint(cp),
					range: [start, this.pos]
				};
			}
		}
	}
	readEscape(inTemplate) {
		const cp = this.source.codePointAt(this.pos);
		if (cp == null) throw new Error("Invalid or unexpected token");
		this.pos = inc(this.pos, cp);
		switch (cp) {
			case CP_n: return {
				value: "\n",
				kind: "special"
			};
			case CP_r: return {
				value: "\r",
				kind: "special"
			};
			case CP_t: return {
				value: "	",
				kind: "special"
			};
			case CP_b: return {
				value: "\b",
				kind: "special"
			};
			case CP_v: return {
				value: "\v",
				kind: "special"
			};
			case CP_f: return {
				value: "\f",
				kind: "special"
			};
			case CP_CR: if (this.source.codePointAt(this.pos) === CP_LF) this.pos++;
			case CP_LF: return {
				value: "",
				kind: "eol"
			};
			case CP_x: return {
				value: String.fromCodePoint(this.readHex(2)),
				kind: "hex"
			};
			case CP_u: return {
				value: String.fromCodePoint(this.readUnicode()),
				kind: "unicode"
			};
			default:
				if (CP_0 <= cp && cp <= CP_7) {
					let octalStr = /^[0-7]+/u.exec(this.source.slice(this.pos - 1, this.pos + 2))[0];
					let octal = parseInt(octalStr, 8);
					if (octal > 255) {
						octalStr = octalStr.slice(0, -1);
						octal = parseInt(octalStr, 8);
					}
					this.pos += octalStr.length - 1;
					const nextCp = this.source.codePointAt(this.pos);
					if ((octalStr !== "0" || nextCp === CP_8 || nextCp === CP_9) && inTemplate) throw new Error("Octal literal in template string");
					return {
						value: String.fromCodePoint(octal),
						kind: "octal"
					};
				}
				return {
					value: String.fromCodePoint(cp),
					kind: "char"
				};
		}
	}
	readUnicode() {
		const cp = this.source.codePointAt(this.pos);
		if (cp === CP_OPENING_BRACE$1) {
			if (this.ecmaVersion < 2015) throw new Error(`Unexpected character '${String.fromCodePoint(cp)}'`);
			this.pos++;
			const endIndex = this.source.indexOf("}", this.pos);
			if (endIndex < 0) throw new Error("Invalid Unicode escape sequence");
			const code = this.readHex(endIndex - this.pos);
			this.pos++;
			if (code > 1114111) throw new Error("Code point out of bounds");
			return code;
		}
		return this.readHex(4);
	}
	readHex(length) {
		let total = 0;
		for (let i = 0; i < length; i++, this.pos++) {
			const cp = this.source.codePointAt(this.pos);
			if (cp == null) throw new Error(`Invalid hexadecimal escape sequence`);
			let val;
			if (CP_a <= cp) val = cp - CP_a + 10;
			else if (CP_A <= cp) val = cp - CP_A + 10;
			else if (CP_0 <= cp && cp <= CP_9) val = cp - CP_0;
			else throw new Error(`Invalid hexadecimal escape sequence`);
			if (val >= 16) throw new Error(`Invalid hexadecimal escape sequence`);
			total = total * 16 + val;
		}
		return total;
	}
};
/**
* Get next index
*/
function inc(pos, cp) {
	return pos + (cp >= 65536 ? 2 : 1);
}
//#endregion
//#region lib/utils/string-literal-parser/parser.ts
function parseStringLiteral(source, option) {
	const startIndex = option?.start ?? 0;
	const cp = source.codePointAt(startIndex);
	const ecmaVersion = option?.ecmaVersion ?? Infinity;
	const tokenizer = new Tokenizer(source, {
		start: startIndex + 1,
		end: option?.end,
		ecmaVersion: ecmaVersion >= 6 && ecmaVersion < 2015 ? ecmaVersion + 2009 : ecmaVersion
	});
	const tokens = [...tokenizer.parseTokens(cp)];
	return {
		tokens,
		get value() {
			return tokens.map((t) => t.value).join("");
		},
		range: [startIndex, tokenizer.pos]
	};
}
function* parseStringTokens(source, option) {
	const startIndex = option?.start ?? 0;
	const ecmaVersion = option?.ecmaVersion ?? Infinity;
	yield* new Tokenizer(source, {
		start: startIndex,
		end: option?.end,
		ecmaVersion: ecmaVersion >= 6 && ecmaVersion < 2015 ? ecmaVersion + 2009 : ecmaVersion
	}).parseTokens();
}
//#endregion
//#region lib/utils/ast-utils/utils.ts
/**
* Get a parent node
* The AST node used by ESLint always has a `parent`, but since there is no `parent` on Types, use this function.
*/
function getParent(node) {
	if (!node) return null;
	return node.parent;
}
/**
* Find the variable of a given name.
*/
function findVariable$1(context, node) {
	return eslintUtils.findVariable(getScope(context, node), node);
}
/**
* Finds a variable of the form `{var,let,const} identifier ( = <init> )?`.
*
* The returned variable is also guaranteed to have exactly one definition.
*
* @param context
* @param expression
*/
function findSimpleVariable(context, identifier) {
	const variable = findVariable$1(context, identifier);
	if (!variable || variable.defs.length !== 1) return null;
	const def = variable.defs[0];
	if (def.type !== "Variable" || def.node.id.type !== "Identifier") return null;
	return variable;
}
/**
* Get the value of a given node if it's a constant of string.
*/
function getStringIfConstant(context, node) {
	if (node.type === "BinaryExpression" || node.type === "MemberExpression" || node.type === "Identifier" || node.type === "TemplateLiteral") {
		const evaluated = getStaticValue(context, node);
		return evaluated && String(evaluated.value);
	}
	return eslintUtils.getStringIfConstant(node, getScope(context, node));
}
/**
* Get the value of a given node if it's a static value.
*/
function getStaticValue(context, node) {
	if (node.type === "BinaryExpression") {
		if (node.operator === "+") {
			const left = getStaticValue(context, node.left);
			if (left == null) return null;
			const right = getStaticValue(context, node.right);
			if (right == null) return null;
			return { value: left.value + right.value };
		}
	} else if (node.type === "MemberExpression") {
		if (getPropertyName$1(node, context) === "source") {
			const object = getStaticValue(context, node.object);
			if (object && object.value instanceof RegExp) return { value: object.value.source };
		}
	} else if (node.type === "TemplateLiteral") {
		const expressions = [];
		for (const expr of node.expressions) {
			const exprValue = getStaticValue(context, expr);
			if (!exprValue) return null;
			expressions.push(exprValue);
		}
		let value = node.quasis[0].value.cooked;
		for (let i = 0; i < expressions.length; ++i) {
			value += String(expressions[i].value);
			value += node.quasis[i + 1].value.cooked;
		}
		return { value };
	} else if (node.type === "Identifier") {
		const deRef = dereferenceVariable(context, node);
		if (deRef !== node) return getStaticValue(context, deRef);
	}
	return eslintUtils.getStaticValue(node, getScope(context, node));
}
/**
* Gets the scope for the current node
*/
function getScope(context, currentNode) {
	const scopeManager = context.sourceCode.scopeManager;
	let node = currentNode;
	for (; node; node = node.parent || null) {
		const scope = scopeManager.acquire(node, false);
		if (scope) {
			if (scope.type === "function-expression-name") return scope.childScopes[0];
			return scope;
		}
	}
	return scopeManager.scopes[0];
}
function findFunction(context, id) {
	let target = id;
	const set = /* @__PURE__ */ new Set();
	for (;;) {
		if (set.has(target)) return null;
		set.add(target);
		const calleeVariable = findVariable$1(context, target);
		if (!calleeVariable) return null;
		if (calleeVariable.defs.length === 1) {
			const def = calleeVariable.defs[0];
			if (def.node.type === "FunctionDeclaration") return def.node;
			if (def.type === "Variable" && def.parent.kind === "const" && def.node.init) {
				if (def.node.init.type === "FunctionExpression" || def.node.init.type === "ArrowFunctionExpression") return def.node.init;
				if (def.node.init.type === "Identifier") {
					target = def.node.init;
					continue;
				}
			}
		}
		return null;
	}
}
/**
* Checks whether given node is expected method call
*/
function isKnownMethodCall(node, methods) {
	const mem = node.callee;
	if (mem.type !== "MemberExpression" || mem.computed || mem.property.type !== "Identifier") return false;
	const argLength = methods[mem.property.name];
	if (node.arguments.length !== argLength) return false;
	if (node.arguments.some((arg) => arg.type === "SpreadElement")) return false;
	if (mem.object.type === "Super") return false;
	return true;
}
/**
* Parse replacements string
*/
function parseReplacements(context, node) {
	return baseParseReplacements(parseStringLiteral(context.sourceCode.text, {
		start: node.range[0],
		end: node.range[1]
	}).tokens.filter((t) => t.value), (start, end) => {
		return { range: [start.range[0], end.range[1]] };
	});
}
/**
* Creates source range from the given offset range of the value of the given
* string literal.
*
* @param sourceCode The ESLint source code instance.
* @param node The string literal to report.
* @returns
*/
function getStringValueRange(sourceCode, node, startOffset, endOffset) {
	if (!node.range) return null;
	if (node.value.length < endOffset) return null;
	try {
		const raw = sourceCode.text.slice(node.range[0] + 1, node.range[1] - 1);
		let valueIndex = 0;
		let start = null;
		for (const t of parseStringTokens(raw)) {
			const endIndex = valueIndex + t.value.length;
			if (start == null && valueIndex <= startOffset && startOffset < endIndex) start = t.range[0];
			if (start != null && valueIndex < endOffset && endOffset <= endIndex) {
				const end = t.range[1];
				const nodeStart = node.range[0] + 1;
				return [nodeStart + start, nodeStart + end];
			}
			valueIndex = endIndex;
		}
	} catch {}
	return null;
}
/**
* Check if the given expression node is regexp literal.
*/
function isRegexpLiteral(node) {
	return node.type === "Literal" && "regex" in node;
}
/**
* Check if the given expression node is string literal.
*/
function isStringLiteral(node) {
	return node.type === "Literal" && typeof node.value === "string";
}
/**
* Returns the string value of the property name accessed.
*
* This is guaranteed to return `null` for private properties.
*
* @param node
* @returns
*/
function getPropertyName$1(node, context) {
	const prop = node.property;
	if (prop.type === "PrivateIdentifier") return null;
	if (!node.computed) return prop.name;
	if (context) return getStringIfConstant(context, prop);
	if (isStringLiteral(prop)) return prop.value;
	return null;
}
/**
* Converts an range into a source location.
*/
function astRangeToLocation(sourceCode, range) {
	return {
		start: sourceCode.getLocFromIndex(range[0]),
		end: sourceCode.getLocFromIndex(range[1])
	};
}
/**
* If the given expression is the identifier of an owned variable, then the
* value of the variable will be returned.
*
* Owned means that the variable is readonly and only referenced by this
* expression.
*
* In all other cases, the given expression will be returned as is.
*
* Note: This will recursively dereference owned variables. I.e. of the given
* identifier resolves to a variable `a` that is assigned an owned variable `b`,
* then this will return the value of `b`. Example:
*
* ```js
* const c = 5;
* const b = c;
* const a = b;
*
* foo(a);
* ```
*
* Dereferencing `a` in `foo(a)` will return `5`.
*/
function dereferenceOwnedVariable(context, expression) {
	if (expression.type === "Identifier") {
		const variable = findSimpleVariable(context, expression);
		if (!variable) return expression;
		const def = variable.defs[0];
		const grandParent = getParent(def.parent);
		if (grandParent && grandParent.type === "ExportNamedDeclaration") return expression;
		if (variable.references.length !== 2) return expression;
		const [initRef, thisRef] = variable.references;
		if (!(initRef.init && initRef.writeExpr && initRef.writeExpr === def.node.init) || thisRef.identifier !== expression) return expression;
		return dereferenceOwnedVariable(context, def.node.init);
	}
	return expression;
}
/**
* If the given expression is the identifier of a variable, then the value of
* the variable will be returned if that value can be statically known.
*
* This method assumes that the value of the variable is immutable. This is
* important because it means that expression that resolve to primitives
* (numbers, string, ...) behave as expected. However, if the value is mutable
* (e.g. arrays and objects), then the object might be mutated. This is because
* objects are passed by reference. So the reference can be statically known
* (the value of the variable) but the value of the object cannot be statically
* known. If the object is immutable (e.g. RegExp and symbols), then they behave
* like primitives.
*/
function dereferenceVariable(context, expression) {
	if (expression.type === "Identifier") {
		const variable = findSimpleVariable(context, expression);
		if (variable) {
			const def = variable.defs[0];
			if (def.node.init) {
				if (def.parent.kind === "const") return dereferenceVariable(context, def.node.init);
				const refs = variable.references;
				const inits = refs.filter((r) => r.init).length;
				const reads = refs.filter((r) => r.isReadOnly()).length;
				if (inits === 1 && reads + inits === refs.length) return dereferenceVariable(context, def.node.init);
			}
		}
	}
	return expression;
}
//#endregion
//#region lib/utils/ast-utils/extract-expression-references.ts
/** Extract references from the given expression */
function* extractExpressionReferences(node, context) {
	yield* iterateReferencesForExpression(node, context, {
		variables: /* @__PURE__ */ new Set(),
		functions: /* @__PURE__ */ new Map()
	});
}
/** Extract references from the given identifier */
function* extractExpressionReferencesForVariable(node, context) {
	yield* iterateReferencesForVariable(node, context, {
		variables: /* @__PURE__ */ new Set(),
		functions: /* @__PURE__ */ new Map()
	});
}
/** Iterate references from the given expression */
function* iterateReferencesForExpression(expression, context, alreadyChecked) {
	let node = expression;
	let parent = getParent(node);
	while (parent?.type === "ChainExpression" || parent?.type === "TSNonNullExpression" || parent?.type === "TSAsExpression") {
		node = parent;
		parent = getParent(node);
	}
	if (!parent || parent.type === "ExpressionStatement") {
		yield {
			node,
			type: "unused"
		};
		return;
	}
	if (parent.type === "MemberExpression") if (parent.object === node) yield {
		node,
		type: "member",
		memberExpression: parent
	};
	else yield {
		node,
		type: "unknown"
	};
	else if (parent.type === "AssignmentExpression") if (parent.right === node && parent.operator === "=") yield* iterateReferencesForESPattern(node, parent.left, context, alreadyChecked);
	else yield {
		node,
		type: "unknown"
	};
	else if (parent.type === "VariableDeclarator") if (parent.init === node) {
		if (getParent(getParent(parent))?.type === "ExportNamedDeclaration") yield {
			node,
			type: "exported"
		};
		yield* iterateReferencesForESPattern(node, parent.id, context, alreadyChecked);
	} else yield {
		node,
		type: "unknown"
	};
	else if (parent.type === "CallExpression") {
		const argIndex = parent.arguments.indexOf(node);
		if (argIndex > -1) {
			if (parent.callee.type === "Identifier") {
				const fn = findFunction(context, parent.callee);
				if (fn) {
					yield* iterateReferencesForFunctionArgument(node, fn, argIndex, context, alreadyChecked);
					return;
				}
			}
			yield {
				node,
				type: "argument",
				callExpression: parent
			};
		} else yield {
			node,
			type: "call"
		};
	} else if (parent.type === "ExportSpecifier" || parent.type === "ExportDefaultDeclaration") yield {
		node,
		type: "exported"
	};
	else if (parent.type === "ForOfStatement") if (parent.right === node) yield {
		node,
		type: "iteration",
		for: parent
	};
	else yield {
		node,
		type: "unknown"
	};
	else if (parent.type === "IfStatement" || parent.type === "ConditionalExpression" || parent.type === "LogicalExpression" || parent.type === "UnaryExpression") if (isUsedInTest(parent, node)) {} else yield {
		node,
		type: "unknown"
	};
	else yield {
		node,
		type: "unknown"
	};
}
/** Checks whether the expression is used in the test. */
function isUsedInTest(parent, node) {
	if (parent.type === "IfStatement") return parent.test === node;
	if (parent.type === "ConditionalExpression") return parent.test === node;
	if (parent.type === "LogicalExpression") return parent.operator === "&&" && parent.left === node;
	if (parent.type === "UnaryExpression") return parent.operator === "!" && parent.argument === node;
	return false;
}
/** Iterate references for the given pattern node. */
function* iterateReferencesForESPattern(expression, pattern, context, alreadyChecked) {
	let target = pattern;
	while (target.type === "AssignmentPattern") target = target.left;
	if (target.type === "Identifier") yield* iterateReferencesForVariable(target, context, alreadyChecked);
	else if (target.type === "ObjectPattern" || target.type === "ArrayPattern") yield {
		node: expression,
		type: "destructuring",
		pattern: target
	};
	else yield {
		node: expression,
		type: "unknown"
	};
}
/** Iterate references for the given variable id node. */
function* iterateReferencesForVariable(identifier, context, alreadyChecked) {
	const variable = findVariable$1(context, identifier);
	if (!variable) {
		yield {
			node: identifier,
			type: "unknown"
		};
		return;
	}
	if (alreadyChecked.variables.has(variable)) return;
	alreadyChecked.variables.add(variable);
	if (variable.eslintUsed) yield {
		node: identifier,
		type: "exported"
	};
	const readReferences = variable.references.filter((ref) => ref.isRead());
	if (!readReferences.length) {
		yield {
			node: identifier,
			type: "unused"
		};
		return;
	}
	for (const reference of readReferences) {
		if (reference.identifier.type === "JSXIdentifier") continue;
		yield* iterateReferencesForExpression(reference.identifier, context, alreadyChecked);
	}
}
/** Iterate references for the given function argument. */
function* iterateReferencesForFunctionArgument(expression, fn, argIndex, context, alreadyChecked) {
	let alreadyIndexes = alreadyChecked.functions.get(fn);
	if (!alreadyIndexes) {
		alreadyIndexes = /* @__PURE__ */ new Set();
		alreadyChecked.functions.set(fn, alreadyIndexes);
	}
	if (alreadyIndexes.has(argIndex)) return;
	alreadyIndexes.add(argIndex);
	const params = fn.params.slice(0, argIndex + 1);
	const argNode = params[argIndex];
	if (!argNode || params.some((param) => param?.type === "RestElement")) {
		yield {
			node: expression,
			type: "unknown"
		};
		return;
	}
	yield* iterateReferencesForESPattern(expression, argNode, context, alreadyChecked);
}
//#endregion
//#region lib/utils/ast-utils/extract-property-references.ts
/** Extract property references from the given expression */
function* extractPropertyReferences(node, context) {
	if (isShallowCopy(node)) {
		yield* iteratePropertyReferencesForShallowCopy(node, context);
		return;
	}
	for (const ref of extractExpressionReferences(node, context)) if (ref.type === "member") yield* iteratePropertyReferencesForMemberExpression(ref.memberExpression, context);
	else if (ref.type === "destructuring") yield* iteratePropertyReferencesForPattern(ref.pattern, context);
	else if (ref.type === "iteration") yield* iteratePropertyReferencesForForOf(ref.for, context);
	else {
		if (ref.node !== node && isShallowCopy(ref.node)) {
			yield* iteratePropertyReferencesForShallowCopy(ref.node, context);
			return;
		}
		yield {
			type: "unknown",
			node: ref.node
		};
	}
}
/** Extract property references from the given pattern */
function* extractPropertyReferencesForPattern(node, context) {
	yield* iteratePropertyReferencesForPattern(node, context);
}
/** Checks whether the given expression is shallow copied. */
function isShallowCopy(node) {
	const parent = getParent(node);
	if (parent?.type === "SpreadElement") {
		const spreadParent = getParent(parent);
		if (spreadParent?.type === "ObjectExpression" || spreadParent?.type === "ArrayExpression") return true;
	}
	return false;
}
/** Iterate property references from the given member expression */
function* iteratePropertyReferencesForMemberExpression(node, context) {
	const property = getProperty(node, context);
	if (property == null) {
		yield {
			type: "unknown",
			node,
			*extractPropertyReferences() {
				yield* extractPropertyReferences(node, context);
			}
		};
		return;
	}
	yield {
		type: "member",
		name: property,
		node,
		*extractPropertyReferences() {
			yield* extractPropertyReferences(node, context);
		}
	};
}
/** Iterate property references from the given object pattern */
function* iteratePropertyReferencesForObjectPattern(node, context) {
	for (const prop of node.properties) {
		if (prop.type === "RestElement") {
			yield* iteratePropertyReferencesForPattern(prop.argument, context);
			continue;
		}
		const property = getProperty(prop, context);
		if (property == null) {
			yield {
				type: "unknown",
				node,
				*extractPropertyReferences() {
					yield* iteratePropertyReferencesForPattern(prop.value, context);
				}
			};
			continue;
		}
		yield {
			type: "destructuring",
			name: property,
			node: prop,
			*extractPropertyReferences() {
				yield* iteratePropertyReferencesForPattern(prop.value, context);
			}
		};
	}
}
/** Iterate property references from the given array pattern */
function* iteratePropertyReferencesForArrayPattern(node, context) {
	let index = 0;
	for (; index < node.elements.length; index++) {
		const element = node.elements[index];
		if (!element) continue;
		if (element.type === "RestElement") {
			for (const ref of iteratePropertyReferencesForPattern(element.argument, context)) yield offsetRef(ref, index);
			index++;
			break;
		}
		yield {
			type: "destructuring",
			name: String(index),
			node: element,
			*extractPropertyReferences() {
				yield* iteratePropertyReferencesForPattern(element, context);
			}
		};
	}
	for (; index < node.elements.length; index++) {
		const element = node.elements[index];
		if (!element) continue;
		yield {
			type: "unknown",
			node: element,
			*extractPropertyReferences() {
				yield* iteratePropertyReferencesForPattern(element, context);
			}
		};
	}
}
/** Iterate property references from the given for of statement */
function* iteratePropertyReferencesForForOf(node, context) {
	yield {
		type: "iteration",
		node,
		*extractPropertyReferences() {
			let left = node.left;
			if (left.type === "VariableDeclaration") left = left.declarations[0].id;
			yield* iteratePropertyReferencesForPattern(left, context);
		}
	};
}
/** Iterate property references from the given pattern */
function* iteratePropertyReferencesForPattern(node, context) {
	let target = node;
	while (target.type === "AssignmentPattern") target = target.left;
	if (target.type === "Identifier") for (const exprRef of extractExpressionReferencesForVariable(target, context)) yield* extractPropertyReferences(exprRef.node, context);
	else if (target.type === "ObjectPattern") yield* iteratePropertyReferencesForObjectPattern(target, context);
	else if (target.type === "ArrayPattern") yield* iteratePropertyReferencesForArrayPattern(target, context);
	else yield {
		type: "unknown",
		node: target
	};
}
/** Iterate property references from the given shallow copy expression */
function* iteratePropertyReferencesForShallowCopy(node, context) {
	const spread = node.parent;
	const spreadParent = spread.parent;
	if (spreadParent.type === "ObjectExpression") yield* extractPropertyReferences(spreadParent, context);
	else if (spreadParent.type === "ArrayExpression") {
		const index = spreadParent.elements.indexOf(spread);
		if (index === 0) {
			yield* extractPropertyReferences(spreadParent, context);
			return;
		}
		if (spreadParent.elements.slice(0, index).some((e) => e?.type === "SpreadElement")) for (const ref of extractPropertyReferences(spreadParent, context)) yield {
			type: "unknown",
			node: ref.node,
			extractPropertyReferences: ref.extractPropertyReferences
		};
		else for (const ref of extractPropertyReferences(spreadParent, context)) yield offsetRef(ref, -index);
	}
}
function getProperty(node, context) {
	if (node.type === "MemberExpression") {
		if (node.computed) {
			if (node.property.type === "Literal") {
				if (typeof node.property.value === "string" || typeof node.property.value === "number") return String(node.property.value);
			}
			return getStringIfConstant(context, node.property);
		} else if (node.property.type === "Identifier") return node.property.name;
	}
	if (node.type === "Property") {
		if (node.key.type === "Literal") {
			if (typeof node.key.value === "string" || typeof node.key.value === "number") return String(node.key.value);
		}
		if (node.computed) return getStringIfConstant(context, node.key);
		else if (node.key.type === "Identifier") return node.key.name;
	}
	return null;
}
/** Moves the reference position of the index reference. */
function offsetRef(ref, offset) {
	if (ref.type === "member" || ref.type === "destructuring") {
		const num = Number(ref.name) + offset;
		if (!Number.isNaN(num)) return {
			...ref,
			name: String(num)
		};
	}
	return ref;
}
//#endregion
//#region lib/utils/ast-utils/regex.ts
/**
* Creates source range of the flags of the given regexp node
* @param flagsNode The expression that contributes the flags.
*/
function getFlagsRange(flagsNode) {
	if (!flagsNode) return null;
	if (isRegexpLiteral(flagsNode)) return [flagsNode.range[1] - flagsNode.regex.flags.length, flagsNode.range[1]];
	if (isStringLiteral(flagsNode)) return [flagsNode.range[0] + 1, flagsNode.range[1] - 1];
	return null;
}
/**
* Creates SourceLocation of the flags of the given regexp node
* @param sourceCode The ESLint source code instance.
* @param regexpNode The node to report.
*/
function getFlagsLocation(sourceCode, regexpNode, flagsNode) {
	const range = getFlagsRange(flagsNode);
	if (range == null) return flagsNode?.loc ?? regexpNode.loc;
	if (range[0] === range[1]) range[0]--;
	return {
		start: sourceCode.getLocFromIndex(range[0]),
		end: sourceCode.getLocFromIndex(range[1])
	};
}
/**
* Creates source range of the given flag in the given flags node
* @param flagsNode The expression that contributes the flags.
*/
function getFlagRange(sourceCode, flagsNode, flag) {
	if (!flagsNode || !flag) return null;
	if (isRegexpLiteral(flagsNode)) {
		const index = flagsNode.regex.flags.indexOf(flag);
		if (index === -1) return null;
		const start = flagsNode.range[1] - flagsNode.regex.flags.length + index;
		return [start, start + 1];
	}
	if (isStringLiteral(flagsNode)) {
		const index = flagsNode.value.indexOf(flag);
		if (index === -1) return null;
		return getStringValueRange(sourceCode, flagsNode, index, index + 1);
	}
	return null;
}
/**
* Creates source location of the given flag in the given flags node
* @param flagsNode The expression that contributes the flags.
*/
function getFlagLocation(sourceCode, regexpNode, flagsNode, flag) {
	const range = getFlagRange(sourceCode, flagsNode, flag);
	if (range == null) return flagsNode?.loc ?? regexpNode.loc;
	return {
		start: sourceCode.getLocFromIndex(range[0]),
		end: sourceCode.getLocFromIndex(range[1])
	};
}
//#endregion
//#region lib/utils/ast-utils/pattern-source.ts
/**
* A range in source code that can be edited.
*/
var PatternReplaceRange = class PatternReplaceRange {
	range;
	type;
	constructor(range, type) {
		if (!range || range[0] < 0 || range[0] > range[1]) throw new Error(`Invalid range: ${JSON.stringify(range)}`);
		this.range = range;
		this.type = type;
	}
	static fromLiteral(node, sourceCode, nodeRange, range) {
		if (!node.range) return null;
		const start = range.start - nodeRange.start;
		const end = range.end - nodeRange.start;
		if (isRegexpLiteral(node)) {
			const nodeStart = node.range[0] + 1;
			return new PatternReplaceRange([nodeStart + start, nodeStart + end], "RegExp");
		}
		if (isStringLiteral(node)) {
			const astRange = getStringValueRange(sourceCode, node, start, end);
			if (astRange) {
				const quote = sourceCode.text[node.range[0]];
				return new PatternReplaceRange(astRange, quote === "'" ? "SingleQuotedString" : "DoubleQuotedString");
			}
		}
		return null;
	}
	getAstLocation(sourceCode) {
		return astRangeToLocation(sourceCode, this.range);
	}
	escape(text) {
		if (this.type === "DoubleQuotedString" || this.type === "SingleQuotedString") {
			const base = text.replace(/\\/gu, "\\\\").replace(/\n/gu, "\\n").replace(/\r/gu, "\\r").replace(/\t/gu, "\\t");
			if (this.type === "DoubleQuotedString") return base.replace(/"/gu, "\\\"");
			return base.replace(/'/gu, "\\'");
		}
		return text.replace(/\n/gu, "\\n").replace(/\r/gu, "\\r");
	}
	replace(fixer, text) {
		return fixer.replaceTextRange(this.range, this.escape(text));
	}
	remove(fixer) {
		return fixer.removeRange(this.range);
	}
	insertAfter(fixer, text) {
		return fixer.insertTextAfterRange(this.range, this.escape(text));
	}
	insertBefore(fixer, text) {
		return fixer.insertTextBeforeRange(this.range, this.escape(text));
	}
};
var PatternSegment = class {
	sourceCode;
	node;
	value;
	start;
	end;
	constructor(sourceCode, node, value, start) {
		this.sourceCode = sourceCode;
		this.node = node;
		this.value = value;
		this.start = start;
		this.end = start + value.length;
	}
	contains(range) {
		return this.start <= range.start && range.end <= this.end;
	}
	getOwnedRegExpLiteral() {
		if (isRegexpLiteral(this.node)) return this.node;
		if (this.node.type === "MemberExpression" && this.node.object.type !== "Super" && isRegexpLiteral(this.node.object) && getPropertyName$1(this.node) === "source") return this.node.object;
		return null;
	}
	getReplaceRange(range) {
		if (!this.contains(range)) return null;
		const regexp = this.getOwnedRegExpLiteral();
		if (regexp) return PatternReplaceRange.fromLiteral(regexp, this.sourceCode, this, range);
		if (this.node.type === "Literal") return PatternReplaceRange.fromLiteral(this.node, this.sourceCode, this, range);
		return null;
	}
	getAstRange(range) {
		const replaceRange = this.getReplaceRange(range);
		if (replaceRange) return replaceRange.range;
		return this.node.range;
	}
};
var PatternSource = class PatternSource {
	sourceCode;
	node;
	value;
	segments;
	/**
	* If the pattern of a regexp is defined by a RegExp object, this value
	* will be non-null. This is the case for simple RegExp literals
	* (e.g. `/foo/`) and RegExp constructors (e.g. `RegExp(/foo/, "i")`).
	*
	* If the pattern source is defined by a string value
	* (e.g. `RegExp("foo")`), then this will be `null`.
	*/
	regexpValue;
	isStringValue() {
		return this.regexpValue === null;
	}
	constructor(sourceCode, node, value, segments, regexpValue) {
		this.sourceCode = sourceCode;
		this.node = node;
		this.value = value;
		this.segments = segments;
		this.regexpValue = regexpValue;
	}
	static fromExpression(context, expression) {
		expression = dereferenceOwnedVariable(context, expression);
		if (isRegexpLiteral(expression)) return PatternSource.fromRegExpLiteral(context, expression);
		const sourceCode = context.sourceCode;
		const flat = flattenPlus(context, expression);
		const items = [];
		let value = "";
		for (const e of flat) {
			if (e.type === "PrivateIdentifier") return null;
			const staticValue = getStaticValue(context, e);
			if (!staticValue) return null;
			if (flat.length === 1 && staticValue.value instanceof RegExp) return PatternSource.fromRegExpObject(context, e, staticValue.value.source, staticValue.value.flags);
			if (typeof staticValue.value !== "string") return null;
			items.push(new PatternSegment(sourceCode, e, staticValue.value, value.length));
			value += staticValue.value;
		}
		return new PatternSource(sourceCode, expression, value, items, null);
	}
	static fromRegExpObject(context, expression, source, flags) {
		const sourceCode = context.sourceCode;
		return new PatternSource(sourceCode, expression, source, [new PatternSegment(sourceCode, expression, source, 0)], {
			source,
			flags,
			ownedNode: null
		});
	}
	static fromRegExpLiteral(context, expression) {
		const sourceCode = context.sourceCode;
		return new PatternSource(sourceCode, expression, expression.regex.pattern, [new PatternSegment(sourceCode, expression, expression.regex.pattern, 0)], {
			source: expression.regex.pattern,
			flags: expression.regex.flags,
			ownedNode: expression
		});
	}
	getSegment(range) {
		const segments = this.getSegments(range);
		if (segments.length === 1) return segments[0];
		return null;
	}
	getSegments(range) {
		return this.segments.filter((item) => item.start < range.end && range.start < item.end);
	}
	getReplaceRange(range) {
		const segment = this.getSegment(range);
		if (segment) return segment.getReplaceRange(range);
		return null;
	}
	/**
	* Returns an approximate AST range for the given pattern range.
	*
	* DO NOT use this in fixes to edit source code. Use
	* {@link PatternSource.getReplaceRange} instead.
	*/
	getAstRange(range) {
		const overlapping = this.getSegments(range);
		if (overlapping.length === 1) return overlapping[0].getAstRange(range);
		let min = Infinity;
		let max = -Infinity;
		for (const item of overlapping) {
			min = Math.min(min, item.node.range[0]);
			max = Math.max(max, item.node.range[1]);
		}
		if (min > max) return this.node.range;
		return [min, max];
	}
	/**
	* Returns an approximate AST source location for the given pattern range.
	*
	* DO NOT use this in fixes to edit source code. Use
	* {@link PatternSource.getReplaceRange} instead.
	*/
	getAstLocation(range) {
		return astRangeToLocation(this.sourceCode, this.getAstRange(range));
	}
	/**
	* Returns all RegExp literals nodes that are owned by this pattern.
	*
	* This means that the returned RegExp literals are only used to create
	* this pattern and for nothing else.
	*/
	getOwnedRegExpLiterals() {
		const literals = [];
		for (const segment of this.segments) {
			const regexp = segment.getOwnedRegExpLiteral();
			if (regexp) literals.push(regexp);
		}
		return literals;
	}
};
/**
* Flattens binary + expressions into an array.
*
* This will automatically dereference owned constants.
*/
function flattenPlus(context, e) {
	if (e.type === "BinaryExpression" && e.operator === "+") return [...e.left.type !== "PrivateIdentifier" ? flattenPlus(context, e.left) : [e.left], ...flattenPlus(context, e.right)];
	const deRef = dereferenceOwnedVariable(context, e);
	if (deRef !== e) return flattenPlus(context, deRef);
	return [e];
}
//#endregion
//#region lib/utils/extract-capturing-group-references.ts
const WELL_KNOWN_ARRAY_METHODS = {
	toString: {},
	toLocaleString: {},
	pop: { result: "element" },
	push: {},
	concat: { result: "array" },
	join: {},
	reverse: { result: "array" },
	shift: { result: "element" },
	slice: { result: "array" },
	sort: {
		elementParameters: [0, 1],
		result: "array"
	},
	splice: { result: "array" },
	unshift: {},
	indexOf: {},
	lastIndexOf: {},
	every: { elementParameters: [0] },
	some: { elementParameters: [0] },
	forEach: { elementParameters: [0] },
	map: { elementParameters: [0] },
	filter: {
		elementParameters: [0],
		result: "array"
	},
	reduce: { elementParameters: [1] },
	reduceRight: { elementParameters: [1] },
	find: {
		elementParameters: [0],
		result: "element"
	},
	findIndex: { elementParameters: [0] },
	fill: {},
	copyWithin: { result: "array" },
	entries: {},
	keys: {},
	values: { result: "iterator" },
	includes: {},
	flatMap: { elementParameters: [0] },
	flat: {},
	at: { result: "element" },
	findLast: {
		elementParameters: [0],
		result: "element"
	},
	findLastIndex: { elementParameters: [0] },
	toReversed: { result: "array" },
	toSorted: {
		elementParameters: [0, 1],
		result: "array"
	},
	toSpliced: { result: "array" },
	with: { result: "array" }
};
/**
* Extracts the usage of the capturing group.
*/
function* extractCapturingGroupReferences(node, flags, typeTracer, countOfCapturingGroup, context, options) {
	const ctx = {
		flags,
		countOfCapturingGroup,
		context,
		isString: options.strictTypes ? (n) => typeTracer.isString(n) : (n) => typeTracer.maybeString(n)
	};
	for (const ref of extractExpressionReferences(node, context)) if (ref.type === "argument") yield* iterateForArgument(ref.callExpression, ref.node, ctx);
	else if (ref.type === "member") yield* iterateForMember(ref.memberExpression, ref.node, ctx);
	else yield {
		type: "UnknownUsage",
		node: ref.node
	};
}
/** Iterate the capturing group references for given argument expression node. */
function* iterateForArgument(callExpression, argument, ctx) {
	if (!isKnownMethodCall(callExpression, {
		match: 1,
		search: 1,
		replace: 2,
		replaceAll: 2,
		matchAll: 1,
		split: 1
	})) return;
	if (callExpression.arguments[0] !== argument) return;
	if (!ctx.isString(callExpression.callee.object)) {
		yield {
			type: "UnknownUsage",
			node: argument
		};
		return;
	}
	if (callExpression.callee.property.name === "match") yield* iterateForStringMatch(callExpression, argument, ctx);
	else if (callExpression.callee.property.name === "search") yield {
		type: "WithoutRef",
		node: argument,
		on: "search"
	};
	else if (callExpression.callee.property.name === "replace" || callExpression.callee.property.name === "replaceAll") yield* iterateForStringReplace(callExpression, argument, ctx, callExpression.callee.property.name);
	else if (callExpression.callee.property.name === "matchAll") yield* iterateForStringMatchAll(callExpression, argument, ctx);
	else if (callExpression.callee.property.name === "split") yield {
		type: "Split",
		node: callExpression
	};
}
/** Iterate the capturing group references for given member expression node. */
function* iterateForMember(memberExpression, object, ctx) {
	const parent = getCallExpressionFromCalleeExpression(memberExpression);
	if (!parent || !isKnownMethodCall(parent, {
		test: 1,
		exec: 1
	})) return;
	if (parent.callee.property.name === "test") yield {
		type: "WithoutRef",
		node: object,
		on: "test"
	};
	else if (parent.callee.property.name === "exec") yield* iterateForRegExpExec(parent, object, ctx);
}
/** Iterate the capturing group references for String.prototype.match(). */
function* iterateForStringMatch(node, argument, ctx) {
	if (ctx.flags.global) yield {
		type: "WithoutRef",
		node: argument,
		on: "match"
	};
	else {
		let useRet = false;
		for (const ref of iterateForExecResult(node, ctx)) {
			useRet = true;
			yield ref;
		}
		if (!useRet) yield {
			type: "WithoutRef",
			node: argument,
			on: "match"
		};
	}
}
/** Iterate the capturing group references for String.prototype.replace() and String.prototype.replaceAll(). */
function* iterateForStringReplace(node, argument, ctx, on) {
	const replacementNode = node.arguments[1];
	if (replacementNode.type === "FunctionExpression" || replacementNode.type === "ArrowFunctionExpression") yield* iterateForReplacerFunction(replacementNode, argument, on, ctx);
	else {
		const replacement = node.arguments[1];
		if (!replacement) {
			yield {
				type: "UnknownUsage",
				node: argument,
				on
			};
			return;
		}
		if (replacement.type === "Literal") yield* verifyForReplaceReplacementLiteral(replacement, argument, on, ctx);
		else {
			const evaluated = getStaticValue(ctx.context, replacement);
			if (!evaluated || typeof evaluated.value !== "string") {
				yield {
					type: "UnknownUsage",
					node: argument,
					on
				};
				return;
			}
			yield* verifyForReplaceReplacement(evaluated.value, argument, on);
		}
	}
}
/** Iterate the capturing group references for String.prototype.matchAll(). */
function* iterateForStringMatchAll(node, argument, ctx) {
	let useRet = false;
	for (const iterationRef of extractPropertyReferences(node, ctx.context)) {
		if (!iterationRef.extractPropertyReferences) {
			yield {
				type: "UnknownUsage",
				node: argument,
				on: "matchAll"
			};
			return;
		}
		if (hasNameRef(iterationRef)) {
			if (iterationRef.type === "member" && isWellKnownArrayMethodName(iterationRef.name)) {
				const call = getCallExpressionFromCalleeExpression(iterationRef.node);
				if (call) for (const cgRef of iterateForArrayMethodOfStringMatchAll(call, iterationRef.name, argument, ctx)) {
					useRet = true;
					yield cgRef;
					if (cgRef.type === "UnknownRef") return;
				}
				continue;
			}
			if (Number.isNaN(Number(iterationRef.name))) continue;
		}
		for (const ref of iterationRef.extractPropertyReferences()) for (const cgRef of iterateForRegExpMatchArrayReference(ref)) {
			useRet = true;
			yield cgRef;
			if (cgRef.type === "UnknownRef") return;
		}
	}
	if (!useRet) yield {
		type: "WithoutRef",
		node: argument,
		on: "matchAll"
	};
}
/** Iterate the capturing group references for RegExp.prototype.exec() . */
function* iterateForRegExpExec(node, object, ctx) {
	let useRet = false;
	for (const ref of iterateForExecResult(node, ctx)) {
		useRet = true;
		yield ref;
	}
	if (!useRet) yield {
		type: "WithoutRef",
		node: object,
		on: "exec"
	};
}
/** Iterate the capturing group references for RegExp.prototype.exec() and String.prototype.match() result */
function* iterateForExecResult(node, ctx) {
	for (const ref of extractPropertyReferences(node, ctx.context)) for (const cgRef of iterateForRegExpMatchArrayReference(ref)) {
		yield cgRef;
		if (cgRef.type === "UnknownRef") return;
	}
}
/** Iterate the capturing group references for String.prototype.replace(regexp, "str") and String.prototype.replaceAll(regexp, "str") */
function* verifyForReplaceReplacementLiteral(substr, argument, on, ctx) {
	let useReplacement = false;
	for (const replacement of parseReplacements(ctx.context, substr)) if (replacement.type === "ReferenceElement") {
		useReplacement = true;
		if (typeof replacement.ref === "number") yield {
			type: "ReplacementRef",
			kind: "index",
			ref: replacement.ref,
			range: replacement.range
		};
		else yield {
			type: "ReplacementRef",
			kind: "name",
			ref: replacement.ref,
			range: replacement.range
		};
	}
	if (!useReplacement) yield {
		type: "WithoutRef",
		node: argument,
		on
	};
}
/** Iterate the capturing group references for String.prototype.replace(regexp, str) and String.prototype.replaceAll(regexp, str) */
function* verifyForReplaceReplacement(substr, argument, on) {
	let useReplacement = false;
	for (const replacement of parseReplacementsForString(substr)) if (replacement.type === "ReferenceElement") {
		useReplacement = true;
		if (typeof replacement.ref === "number") yield {
			type: "ReplacementRef",
			kind: "index",
			ref: replacement.ref
		};
		else yield {
			type: "ReplacementRef",
			kind: "name",
			ref: replacement.ref
		};
	}
	if (!useReplacement) yield {
		type: "WithoutRef",
		node: argument,
		on
	};
}
/** Iterate the capturing group references for String.prototype.replace(regexp, fn) and String.prototype.replaceAll(regexp, fn) */
function* iterateForReplacerFunction(replacementNode, argument, on, ctx) {
	if (replacementNode.params.length < 2 && !replacementNode.params.some((arg) => arg.type === "RestElement")) {
		yield {
			type: "WithoutRef",
			node: argument,
			on
		};
		return;
	}
	for (let index = 0; index < replacementNode.params.length; index++) {
		const arg = replacementNode.params[index];
		if (arg.type === "RestElement") {
			yield {
				type: "UnknownRef",
				kind: "replacerFunction",
				arg
			};
			return;
		}
		if (index === 0) continue;
		else if (index <= ctx.countOfCapturingGroup) yield {
			type: "ReplacerFunctionRef",
			kind: "index",
			ref: index,
			arg
		};
		else if (ctx.countOfCapturingGroup + 3 === index) if (arg.type === "Identifier" || arg.type === "ObjectPattern") for (const ref of extractPropertyReferencesForPattern(arg, ctx.context)) if (hasNameRef(ref)) yield {
			type: "ReplacerFunctionRef",
			kind: "name",
			ref: ref.name,
			prop: ref
		};
		else yield {
			type: "ReplacerFunctionRef",
			kind: "name",
			ref: null,
			prop: ref,
			arg: null
		};
		else yield {
			type: "ReplacerFunctionRef",
			kind: "name",
			ref: null,
			arg,
			prop: null
		};
	}
}
/** Iterate the capturing group references for RegExpMatchArray reference. */
function* iterateForRegExpMatchArrayReference(ref) {
	if (hasNameRef(ref)) if (ref.name === "groups") for (const namedRef of ref.extractPropertyReferences()) yield getNamedArrayRef(namedRef);
	else if (ref.name === "indices") for (const indicesRef of ref.extractPropertyReferences()) yield* iterateForRegExpIndicesArrayReference(indicesRef);
	else {
		if (ref.name === "input" || ref.name === "index") return;
		yield getIndexArrayRef(ref);
	}
	else yield {
		type: "UnknownRef",
		kind: "array",
		prop: ref
	};
}
/** Iterate the capturing group references for RegExpIndicesArray reference. */
function* iterateForRegExpIndicesArrayReference(ref) {
	if (hasNameRef(ref)) if (ref.name === "groups") for (const namedRef of ref.extractPropertyReferences()) yield getNamedArrayRef(namedRef);
	else yield getIndexArrayRef(ref);
	else yield {
		type: "UnknownRef",
		kind: "array",
		prop: ref
	};
}
/** Iterate the capturing group references for Array method of String.prototype.matchAll(). */
function* iterateForArrayMethodOfStringMatchAll(node, methodsName, argument, ctx) {
	const arrayMethod = WELL_KNOWN_ARRAY_METHODS[methodsName];
	if (arrayMethod.elementParameters && node.arguments[0] && (node.arguments[0].type === "FunctionExpression" || node.arguments[0].type === "ArrowFunctionExpression")) {
		const fnNode = node.arguments[0];
		for (const index of arrayMethod.elementParameters) {
			const param = fnNode.params[index];
			if (param) for (const ref of extractPropertyReferencesForPattern(param, ctx.context)) yield* iterateForRegExpMatchArrayReference(ref);
		}
	}
	if (arrayMethod.result) {
		if (arrayMethod.result === "element") for (const ref of extractPropertyReferences(node, ctx.context)) yield* iterateForRegExpMatchArrayReference(ref);
		else if (arrayMethod.result === "array" || arrayMethod.result === "iterator") yield* iterateForStringMatchAll(node, argument, ctx);
	}
}
/** Checks whether the given reference is a named reference. */
function hasNameRef(ref) {
	return ref.type === "destructuring" || ref.type === "member";
}
/** Get the index array ref from PropertyReference */
function getIndexArrayRef(ref) {
	const numRef = Number(ref.name);
	if (Number.isFinite(numRef)) return {
		type: "ArrayRef",
		kind: "index",
		ref: numRef,
		prop: ref
	};
	return {
		type: "ArrayRef",
		kind: "index",
		ref: null,
		prop: ref
	};
}
/** Get the named array ref from PropertyReference */
function getNamedArrayRef(namedRef) {
	if (hasNameRef(namedRef)) return {
		type: "ArrayRef",
		kind: "name",
		ref: namedRef.name,
		prop: namedRef
	};
	return {
		type: "ArrayRef",
		kind: "name",
		ref: null,
		prop: namedRef
	};
}
/** Gets the CallExpression from the given callee node. */
function getCallExpressionFromCalleeExpression(expression) {
	const parent = getParent(expression);
	if (!parent || parent.type !== "CallExpression" || parent.callee !== expression) return null;
	return parent;
}
/** Checks whether the given name is a well known array method name. */
function isWellKnownArrayMethodName(name) {
	return Boolean(WELL_KNOWN_ARRAY_METHODS[name]);
}
//#endregion
//#region lib/utils/get-usage-of-pattern.ts
let UsageOfPattern = /* @__PURE__ */ function(UsageOfPattern) {
	/** The pattern was only used via `.source`. */
	UsageOfPattern[UsageOfPattern["partial"] = 0] = "partial";
	/** The pattern was (probably) used the whole pattern as a regular expression. */
	UsageOfPattern[UsageOfPattern["whole"] = 1] = "whole";
	/** The pattern was used partial and whole. */
	UsageOfPattern[UsageOfPattern["mixed"] = 2] = "mixed";
	/** The pattern cannot determine how was used. */
	UsageOfPattern[UsageOfPattern["unknown"] = 3] = "unknown";
	return UsageOfPattern;
}({});
/**
* Returns the usage of pattern.
*/
function getUsageOfPattern(node, context) {
	const usageSet = /* @__PURE__ */ new Set();
	for (const usage of iterateUsageOfPattern(node, context)) {
		if (usage === UsageOfPattern.unknown) return UsageOfPattern.unknown;
		usageSet.add(usage);
	}
	if (usageSet.has(UsageOfPattern.partial)) return usageSet.has(UsageOfPattern.whole) ? UsageOfPattern.mixed : UsageOfPattern.partial;
	return usageSet.has(UsageOfPattern.whole) ? UsageOfPattern.whole : UsageOfPattern.unknown;
}
/** Iterate the usage of pattern for the given expression node. */
function* iterateUsageOfPattern(node, context) {
	for (const ref of extractExpressionReferences(node, context)) if (ref.type === "member") yield* iterateUsageOfPatternForMemberExpression(ref.memberExpression, context);
	else if (ref.type === "destructuring") {
		if (ref.pattern.type === "ObjectPattern") yield* iterateUsageOfPatternForObjectPattern(ref.pattern, context);
	} else if (ref.type === "unused") {} else if (ref.type === "argument") if (ref.callExpression.arguments[0] === ref.node && ref.callExpression.callee.type === "MemberExpression") {
		const member = ref.callExpression.callee;
		const propName = !member.computed ? member.property.name : getStringIfConstant(context, member.property);
		if (propName === "match" || propName === "matchAll" || propName === "split" || propName === "replace" || propName === "replaceAll" || propName === "search") yield UsageOfPattern.whole;
		else yield UsageOfPattern.unknown;
	} else yield UsageOfPattern.unknown;
	else yield UsageOfPattern.unknown;
}
/** Iterate the usage of pattern for the given member expression node. */
function* iterateUsageOfPatternForMemberExpression(node, context) {
	yield* iterateUsageOfPatternForPropName(!node.computed ? node.property.name : getStringIfConstant(context, node.property));
}
/** Iterate the usage of pattern for the given member expression node. */
function* iterateUsageOfPatternForPropName(propName) {
	const regexpPropName = propName;
	if (regexpPropName === "source") {
		yield UsageOfPattern.partial;
		return;
	}
	if (regexpPropName === "compile" || regexpPropName === "dotAll" || regexpPropName === "flags" || regexpPropName === "global" || regexpPropName === "ignoreCase" || regexpPropName === "multiline" || regexpPropName === "sticky" || regexpPropName === "unicode") return;
	yield UsageOfPattern.whole;
}
/** Iterate the usage of pattern for the given object pattern node. */
function* iterateUsageOfPatternForObjectPattern(node, context) {
	for (const prop of node.properties) {
		if (prop.type === "RestElement") continue;
		let propName;
		if (!prop.computed) propName = prop.key.type === "Identifier" ? prop.key.name : String(prop.key.value);
		else propName = getStringIfConstant(context, prop.key);
		yield* iterateUsageOfPatternForPropName(propName);
	}
}
//#endregion
//#region lib/utils/util.ts
/**
* Throws if the function is called. This is useful for ensuring that a switch statement is exhaustive.
*/
function assertNever(value) {
	throw new Error(`Invalid value: ${value}`);
}
/**
* Returns a cached version of the given function for lazy evaluation.
*
* For the cached function to behave correctly, the given function must be pure.
*/
function lazy(fn) {
	let cached;
	return () => {
		if (cached === void 0) cached = fn();
		return cached;
	};
}
/**
* Returns a cached version of the given function. A `WeakMap` is used internally.
*
* For the cached function to behave correctly, the given function must be pure.
*/
function cachedFn(fn) {
	const cache = /* @__PURE__ */ new WeakMap();
	return (key) => {
		let cached = cache.get(key);
		if (cached === void 0) {
			cached = fn(key);
			cache.set(key, cached);
		}
		return cached;
	};
}
/**
* Returns all code points of the given string.
*/
function toCodePoints(s) {
	return [...s].map((c) => c.codePointAt(0));
}
/**
* Returns an array of the given iterable in reverse order.
*/
function reversed(iter) {
	return [...iter].reverse();
}
//#endregion
//#region lib/utils/regex-syntax.ts
const RESERVED_DOUBLE_PUNCTUATORS = "&!#$%*+,.:;<=>?@^`~-";
/**
* A single character set of ClassSetReservedDoublePunctuator.
*
* `&& !! ## $$ %% ** ++ ,, .. :: ;; << == >> ?? @@ ^^ `` ~~ --` are ClassSetReservedDoublePunctuator
*/
const RESERVED_DOUBLE_PUNCTUATOR_CHARS = new Set(RESERVED_DOUBLE_PUNCTUATORS);
/**
* Same as {@link RESERVED_DOUBLE_PUNCTUATOR_CHARS} but as code points.
*/
const RESERVED_DOUBLE_PUNCTUATOR_CP = new Set(toCodePoints(RESERVED_DOUBLE_PUNCTUATORS));
const RESERVED_DOUBLE_PUNCTUATOR_PATTERN = /&&|!!|##|\$\$|%%|\*\*|\+\+|,,|\.\.|::|;;|<<|==|>>|\?\?|@@|\^\^|``|~~|--/u;
/**
* Returns whether the given raw of a character literal is an octal escape
* sequence.
*/
function isOctalEscape(raw) {
	return /^\\[0-7]{1,3}$/u.test(raw);
}
/**
* Returns whether the given raw of a character literal is a control escape
* sequence.
*/
function isControlEscape(raw) {
	return /^\\c[A-Za-z]$/u.test(raw);
}
/**
* Returns whether the given raw of a character literal is a hexadecimal escape
* sequence.
*/
function isHexadecimalEscape(raw) {
	return /^\\x[\dA-Fa-f]{2}$/u.test(raw);
}
/**
* Returns whether the given raw of a character literal is a unicode escape
* sequence.
*/
function isUnicodeEscape(raw) {
	return /^\\u[\dA-Fa-f]{4}$/u.test(raw);
}
/**
* Returns whether the given raw of a character literal is a unicode code point
* escape sequence.
*/
function isUnicodeCodePointEscape(raw) {
	return /^\\u\{[\dA-Fa-f]{1,8}\}$/u.test(raw);
}
let EscapeSequenceKind = /* @__PURE__ */ function(EscapeSequenceKind) {
	EscapeSequenceKind["octal"] = "octal";
	EscapeSequenceKind["control"] = "control";
	EscapeSequenceKind["hexadecimal"] = "hexadecimal";
	EscapeSequenceKind["unicode"] = "unicode";
	EscapeSequenceKind["unicodeCodePoint"] = "unicode code point";
	return EscapeSequenceKind;
}({});
/**
* Returns which escape sequence kind was used for the given raw of a character literal.
*/
function getEscapeSequenceKind(raw) {
	if (raw[0] !== "\\") return null;
	if (isOctalEscape(raw)) return EscapeSequenceKind.octal;
	if (isControlEscape(raw)) return EscapeSequenceKind.control;
	if (isHexadecimalEscape(raw)) return EscapeSequenceKind.hexadecimal;
	if (isUnicodeEscape(raw)) return EscapeSequenceKind.unicode;
	if (isUnicodeCodePointEscape(raw)) return EscapeSequenceKind.unicodeCodePoint;
	return null;
}
/**
* Returns whether the given raw of a character literal is an octal escape
* sequence, a control escape sequence, a hexadecimal escape sequence, a unicode
* escape sequence, or a unicode code point escape sequence.
*/
function isEscapeSequence(raw) {
	return getEscapeSequenceKind(raw) !== null;
}
/**
* Returns whether the given raw of a character literal is a hexadecimal escape
* sequence, a unicode escape sequence, or a unicode code point escape sequence.
*/
function isHexLikeEscape(raw) {
	const kind = getEscapeSequenceKind(raw);
	return kind === EscapeSequenceKind.hexadecimal || kind === EscapeSequenceKind.unicode || kind === EscapeSequenceKind.unicodeCodePoint;
}
const flagsCache = /* @__PURE__ */ new Map();
/**
* Given some flags, this will return a parsed flags object.
*
* Non-standard flags will be ignored.
*/
function parseFlags(flags) {
	let cached = flagsCache.get(flags);
	if (cached === void 0) {
		cached = {
			dotAll: flags.includes("s"),
			global: flags.includes("g"),
			hasIndices: flags.includes("d"),
			ignoreCase: flags.includes("i"),
			multiline: flags.includes("m"),
			sticky: flags.includes("y"),
			unicode: flags.includes("u"),
			unicodeSets: flags.includes("v")
		};
		flagsCache.set(flags, cached);
	}
	return cached;
}
//#endregion
//#region lib/utils/regexp-ast/common.ts
/**
* This operations is equal to:
*
* ```
* concat(
*     getFirstConsumedChar(element, direction, flags),
*     getFirstConsumedCharAfter(element, direction, flags),
* )
* ```
*/
function getFirstConsumedCharPlusAfter(element, direction, flags) {
	const consumed = getFirstConsumedChar(element, direction, flags);
	if (!consumed.empty) return consumed;
	return FirstConsumedChars.concat([consumed, getFirstConsumedCharAfter(element, direction, flags)], flags);
}
/**
* Extract capturing group data
*/
function extractCaptures(pattern) {
	const groups = [];
	visitRegExpAST(pattern, { onCapturingGroupEnter(group) {
		groups.push(group);
	} });
	groups.sort((a, b) => a.start - b.start);
	const names = /* @__PURE__ */ new Set();
	for (const group of groups) if (group.name !== null) names.add(group.name);
	return {
		groups,
		names,
		count: groups.length
	};
}
/**
* Returns whether the given node is or contains a capturing group.
*/
function hasCapturingGroup(node) {
	return hasSomeDescendant(node, (d) => d.type === "CapturingGroup");
}
//#endregion
//#region lib/utils/regexp-ast/ast.ts
const parser = new RegExpParser();
/**
* Get Reg Exp node from given expression node
*/
function getRegExpNodeFromExpression(node, context) {
	if (node.type === "Literal") {
		if ("regex" in node && node.regex) try {
			return parser.parsePattern(node.regex.pattern, 0, node.regex.pattern.length, {
				unicode: node.regex.flags.includes("u"),
				unicodeSets: node.regex.flags.includes("v")
			});
		} catch {
			return null;
		}
		return null;
	}
	const evaluated = getStaticValue(context, node);
	if (!evaluated || !(evaluated.value instanceof RegExp)) return null;
	try {
		return parseRegExpLiteral(evaluated.value);
	} catch {
		return null;
	}
}
//#endregion
//#region lib/utils/regexp-ast/is-equals.ts
/**
* Returns whether the two given character element as equal in the characters
* that they accept.
*
* This is equivalent to `toUnicodeSet(a).equals(toUnicodeSet(b))` but implemented
* more efficiently.
*/
function isEqualChar(a, b, flags) {
	if (a.type === "Character") {
		if (b.type === "Character") {
			if (a.value === b.value) return true;
		} else if (b.type === "CharacterSet") return false;
	} else if (a.type === "CharacterSet") {
		if (b.type === "Character") return false;
		else if (b.type === "CharacterSet") return a.raw === b.raw;
	} else if (a.type === "CharacterClassRange") {
		if (b.type === "CharacterClassRange") return a.min.value === b.min.value && a.max.value === b.max.value;
	}
	if (a.raw === b.raw) return true;
	return toUnicodeSet(a, flags).equals(toUnicodeSet(b, flags));
}
const EQUALS_CHECKER = {
	Alternative(a, b, flags, shortCircuit) {
		return isEqualConcatenation(a.elements, b.elements, flags, shortCircuit);
	},
	Assertion(a, b, flags, shortCircuit) {
		if (a.kind === "start" || a.kind === "end")
 /* istanbul ignore next */
		return a.kind === b.kind;
		if (a.kind === "word") return b.kind === "word" && a.negate === b.negate;
		if (a.kind === "lookahead" || a.kind === "lookbehind") {
			if (b.kind === a.kind && a.negate === b.negate) return isEqualSet(a.alternatives, b.alternatives, flags, shortCircuit);
			return false;
		}
		/* istanbul ignore next */
		return false;
	},
	Backreference(a, b) {
		return a.ref === b.ref;
	},
	CapturingGroup(a, b, flags, shortCircuit) {
		return a.name === b.name && isEqualSet(a.alternatives, b.alternatives, flags, shortCircuit);
	},
	Character(a, b, flags) {
		return isEqualChar(a, b, flags);
	},
	CharacterClass(a, b, flags) {
		return isEqualChar(a, b, flags);
	},
	CharacterClassRange(a, b, flags) {
		return isEqualChar(a, b, flags);
	},
	CharacterSet(a, b, flags) {
		return isEqualChar(a, b, flags);
	},
	ClassIntersection(a, b, flags, shortCircuit) {
		return isEqualSet([a.left, a.right], [b.left, b.right], flags, shortCircuit);
	},
	ClassStringDisjunction(a, b, flags, shortCircuit) {
		return isEqualSet(a.alternatives, b.alternatives, flags, shortCircuit);
	},
	ClassSubtraction(a, b, flags, shortCircuit) {
		return isEqualNodes(a.left, b.left, flags, shortCircuit) && isEqualNodes(a.right, b.right, flags, shortCircuit);
	},
	ExpressionCharacterClass(a, b, flags) {
		return a.negate === b.negate && isEqualNodes(a.expression, b.expression, flags);
	},
	Flags(a, b) {
		/* istanbul ignore next */
		return a.dotAll === b.dotAll && a.global === b.global && a.ignoreCase === b.ignoreCase && a.multiline === b.multiline && a.hasIndices === b.hasIndices && a.sticky === b.sticky && a.unicode === b.unicode && a.unicodeSets === b.unicodeSets;
	},
	Group(a, b, flags, shortCircuit) {
		return isEqualSet(a.alternatives, b.alternatives, flags, shortCircuit);
	},
	ModifierFlags(a, b) {
		return a.dotAll === b.dotAll && a.ignoreCase === b.ignoreCase && a.multiline === b.multiline;
	},
	Modifiers(a, b, flags, shortCircuit) {
		return isEqualNodes(a.add, b.add, flags, shortCircuit) && (a.remove == null && b.remove == null || a.remove != null && b.remove != null && isEqualNodes(a.remove, b.remove, flags, shortCircuit));
	},
	Pattern(a, b, flags, shortCircuit) {
		return isEqualSet(a.alternatives, b.alternatives, flags, shortCircuit);
	},
	Quantifier(a, b, flags, shortCircuit) {
		return a.min === b.min && a.max === b.max && a.greedy === b.greedy && isEqualNodes(a.element, b.element, flags, shortCircuit);
	},
	RegExpLiteral(a, b, flags, shortCircuit) {
		return isEqualNodes(a.pattern, b.pattern, flags, shortCircuit) && isEqualNodes(a.flags, b.flags, flags, shortCircuit);
	},
	StringAlternative(a, b, flags, shortCircuit) {
		return isEqualConcatenation(a.elements, b.elements, flags, shortCircuit);
	}
};
/**
* Returns whether the given nodes is a `ToCharSetElement`
*/
function isToCharSetElement(node) {
	return node.type === "Character" || node.type === "CharacterClass" || node.type === "CharacterClassRange" || node.type === "CharacterSet";
}
/** Check whether given nodes is equals or not. */
function isEqualNodes(a, b, flags, shortCircuit) {
	if (isToCharSetElement(a) && isToCharSetElement(b)) return isEqualChar(a, b, flags);
	if (a.type !== b.type) return false;
	if (shortCircuit) {
		const kind = shortCircuit(a, b);
		if (kind != null) return kind;
	}
	if (/[(*+?[\\{|]/u.test(a.raw) || /[(*+?[\\{|]/u.test(b.raw)) return EQUALS_CHECKER[a.type](a, b, flags, shortCircuit);
	return a.raw === b.raw;
}
/** Check whether given elements are equals or not. */
function isEqualConcatenation(a, b, flags, shortCircuit) {
	if (a.length !== b.length) return false;
	for (let index = 0; index < a.length; index++) {
		const ae = a[index];
		const be = b[index];
		if (!isEqualNodes(ae, be, flags, shortCircuit)) return false;
	}
	return true;
}
/** Check whether given alternatives are equals or not. */
function isEqualSet(a, b, flags, shortCircuit) {
	if (a.length !== b.length) return false;
	const beList = [...b];
	for (const ae of a) {
		const bIndex = beList.findIndex((be) => isEqualNodes(ae, be, flags, shortCircuit));
		if (bIndex >= 0) beList.splice(bIndex, 1);
		else return false;
	}
	return true;
}
//#endregion
//#region lib/utils/regexp-ast/is-covered.ts
var NormalizedOther = class NormalizedOther {
	type = "NormalizedOther";
	node;
	static fromNode(node) {
		return new NormalizedOther(node);
	}
	constructor(node) {
		this.node = node;
	}
};
/**
* Code point range list
* Character, CharacterClass and CharacterSet are converted to this.
*/
var NormalizedCharacter = class NormalizedCharacter {
	type = "NormalizedCharacter";
	charSet;
	static fromElement(element, options) {
		return new NormalizedCharacter(toCharSet(element, options.flags));
	}
	static fromChars(charSet) {
		return new NormalizedCharacter(charSet);
	}
	constructor(charSet) {
		this.charSet = charSet;
	}
};
/**
* Normalized alternative
* Alternative and Quantifier are converted to this.
* If there is only one element of alternative, it will be skipped. e.g. /a/
*/
var NormalizedAlternative = class NormalizedAlternative {
	type = "NormalizedAlternative";
	raw;
	elements;
	static fromAlternative(node, options) {
		const normalizeElements = [...NormalizedAlternative.normalizedElements(function* () {
			for (const element of node.elements) {
				const normal = normalizeNode(element, options);
				if (normal.type === "NormalizedAlternative") yield* normal.elements;
				else yield normal;
			}
		})];
		if (normalizeElements.length === 1) return normalizeElements[0];
		return new NormalizedAlternative(normalizeElements, node);
	}
	static fromQuantifier(node, options) {
		const normalizeElements = [...NormalizedAlternative.normalizedElements(function* () {
			const normalizeElement = normalizeNode(node.element, options);
			for (let index = 0; index < node.min; index++) yield normalizeElement;
		})];
		if (normalizeElements.length === 1) return normalizeElements[0];
		return new NormalizedAlternative(normalizeElements, node);
	}
	static fromElements(elements, node) {
		return new NormalizedAlternative([...NormalizedAlternative.normalizedElements(function* () {
			yield* elements;
		})], node);
	}
	static *normalizedElements(generate) {
		for (const node of generate()) if (node.type === "NormalizedAlternative") yield* node.elements;
		else yield node;
	}
	constructor(elements, node) {
		this.raw = node.raw;
		this.elements = elements;
	}
};
/**
* Normalized disjunctions
* CapturingGroup, Group and Pattern are converted to this.
* If there is only one element of disjunctions, it will be skipped. e.g. /(abc)/
*/
var NormalizedDisjunctions = class NormalizedDisjunctions {
	type = "NormalizedDisjunctions";
	raw;
	getAlternatives;
	normalizedAlternatives;
	static fromNode(node, options) {
		if (node.alternatives.length === 1) return NormalizedAlternative.fromAlternative(node.alternatives[0], options);
		return new NormalizedDisjunctions(node, () => {
			return node.alternatives.map((alt) => {
				const n = normalizeNode(alt, options);
				if (n.type === "NormalizedAlternative") return n;
				return NormalizedAlternative.fromElements([n], alt);
			});
		});
	}
	static fromAlternatives(alternatives, node) {
		return new NormalizedDisjunctions(node, () => alternatives);
	}
	constructor(node, getAlternatives) {
		this.raw = node.raw;
		this.getAlternatives = getAlternatives;
	}
	get alternatives() {
		if (!this.normalizedAlternatives) this.normalizedAlternatives = this.getAlternatives();
		return this.normalizedAlternatives;
	}
};
/**
* Normalized lookaround assertion
* LookaheadAssertion and LookbehindAssertion are converted to this.
*/
var NormalizedLookaroundAssertion = class NormalizedLookaroundAssertion {
	type = "NormalizedLookaroundAssertion";
	raw;
	node;
	options;
	normalizedAlternatives;
	static fromNode(node, options) {
		return new NormalizedLookaroundAssertion(node, options);
	}
	constructor(node, options) {
		this.raw = node.raw;
		this.node = node;
		this.options = options;
	}
	get alternatives() {
		if (this.normalizedAlternatives) return this.normalizedAlternatives;
		this.normalizedAlternatives = [];
		for (const alt of this.node.alternatives) {
			const node = normalizeNode(alt, this.options);
			if (node.type === "NormalizedAlternative") this.normalizedAlternatives.push(node);
			else this.normalizedAlternatives.push(NormalizedAlternative.fromElements([node], alt));
		}
		return this.normalizedAlternatives;
	}
	get kind() {
		return this.node.kind;
	}
	get negate() {
		return this.node.negate;
	}
};
/**
* Normalized optional node
* Quantifier is converted to this.
* The exactly quantifier of the number will be converted to NormalizedAlternative.
*/
var NormalizedOptional = class NormalizedOptional {
	type = "NormalizedOptional";
	raw;
	max;
	node;
	options;
	normalizedElement;
	static fromQuantifier(node, options) {
		let alt = null;
		if (node.min > 0) alt = NormalizedAlternative.fromQuantifier(node, options);
		const max = node.max - node.min;
		if (max > 0) {
			const optional = new NormalizedOptional(node, options, max);
			if (alt) {
				if (alt.type === "NormalizedAlternative") return NormalizedAlternative.fromElements([...alt.elements, optional], node);
				return NormalizedAlternative.fromElements([alt, optional], node);
			}
			return optional;
		}
		if (alt) return alt;
		return NormalizedOther.fromNode(node);
	}
	constructor(node, options, max) {
		this.raw = node.raw;
		this.max = max;
		this.node = node;
		this.options = options;
	}
	get element() {
		return this.normalizedElement ?? (this.normalizedElement = normalizeNode(this.node.element, this.options));
	}
	decrementMax(dec = 1) {
		if (this.max <= dec) return null;
		if (this.max === Infinity) return this;
		const opt = new NormalizedOptional(this.node, this.options, this.max - dec);
		opt.normalizedElement = this.normalizedElement;
		return opt;
	}
};
/** Checks whether the right node is covered by the left node. */
function isCoveredNode(left, right, options) {
	return isCoveredForNormalizedNode(normalizeNode(left, options), normalizeNode(right, options), options);
}
/** Checks whether the right node is covered by the left node. */
function isCoveredForNormalizedNode(left, right, options) {
	if (right.type === "NormalizedDisjunctions") return right.alternatives.every((r) => isCoveredForNormalizedNode(left, r, options));
	if (left.type === "NormalizedDisjunctions") return isCoveredAnyNode(left.alternatives, right, options);
	if (left.type === "NormalizedAlternative") {
		if (right.type === "NormalizedAlternative") return isCoveredAltNodes(left.elements, right.elements, options);
		return isCoveredAltNodes(left.elements, [right], options);
	} else if (right.type === "NormalizedAlternative") return isCoveredAltNodes([left], right.elements, options);
	if (left.type === "NormalizedOptional" || right.type === "NormalizedOptional") return isCoveredAltNodes([left], [right], options);
	if (left.type === "NormalizedOther" || right.type === "NormalizedOther") {
		if (left.type === "NormalizedOther" && right.type === "NormalizedOther") return isEqualNodes(left.node, right.node, options.flags);
		return false;
	}
	if (left.type === "NormalizedLookaroundAssertion" || right.type === "NormalizedLookaroundAssertion") {
		if (left.type === "NormalizedLookaroundAssertion" && right.type === "NormalizedLookaroundAssertion") {
			if (left.kind === right.kind && !left.negate && !right.negate) return right.alternatives.every((r) => isCoveredAnyNode(left.alternatives, r, options));
			return isEqualNodes(left.node, right.node, options.flags);
		}
		return false;
	}
	if (right.type === "NormalizedCharacter") return right.charSet.isSubsetOf(left.charSet);
	return false;
}
const cacheNormalizeNode = /* @__PURE__ */ new WeakMap();
function normalizeNode(node, options) {
	let n = cacheNormalizeNode.get(node);
	if (n) return n;
	n = normalizeNodeWithoutCache(node, options);
	cacheNormalizeNode.set(node, n);
	return n;
}
function normalizeNodeWithoutCache(node, options) {
	switch (node.type) {
		case "CharacterSet":
		case "CharacterClass":
		case "Character":
		case "CharacterClassRange":
		case "ExpressionCharacterClass":
		case "ClassIntersection":
		case "ClassSubtraction":
		case "ClassStringDisjunction":
		case "StringAlternative": {
			const set = toUnicodeSet(node, options.flags);
			if (set.accept.isEmpty) return NormalizedCharacter.fromChars(set.chars);
			const alternatives = set.wordSets.map((wordSet) => {
				return NormalizedAlternative.fromElements(wordSet.map(NormalizedCharacter.fromChars), node);
			});
			return NormalizedDisjunctions.fromAlternatives(alternatives, node);
		}
		case "Alternative": return NormalizedAlternative.fromAlternative(node, options);
		case "Quantifier": return NormalizedOptional.fromQuantifier(node, options);
		case "CapturingGroup":
		case "Group":
		case "Pattern": return NormalizedDisjunctions.fromNode(node, options);
		case "Assertion":
			if (node.kind === "lookahead" || node.kind === "lookbehind") return NormalizedLookaroundAssertion.fromNode(node, options);
			return NormalizedOther.fromNode(node);
		case "RegExpLiteral": return normalizeNode(node.pattern, options);
		case "Backreference":
		case "Flags":
		case "ModifierFlags":
		case "Modifiers": return NormalizedOther.fromNode(node);
		default: return assertNever(node);
	}
}
/** Check whether the right node is covered by the left nodes. */
function isCoveredAnyNode(left, right, options) {
	for (const e of left) if (isCoveredForNormalizedNode(e, right, options)) return true;
	return false;
}
/** Check whether the right nodes is covered by the left nodes. */
function isCoveredAltNodes(leftNodes, rightNodes, options) {
	const left = options.canOmitRight ? omitEnds(leftNodes) : [...leftNodes];
	const right = options.canOmitRight ? omitEnds(rightNodes) : [...rightNodes];
	while (left.length && right.length) {
		const le = left.shift();
		const re = right.shift();
		if (re.type === "NormalizedOptional") if (le.type === "NormalizedOptional") {
			if (!isCoveredForNormalizedNode(le.element, re.element, options)) return false;
			const decrementLe = le.decrementMax(re.max);
			if (decrementLe) return isCoveredAltNodes([decrementLe, ...left], right, options);
			const decrementRe = re.decrementMax(le.max);
			if (decrementRe) return isCoveredAltNodes(left, [decrementRe, ...right], options);
		} else {
			if (!isCoveredForNormalizedNode(le, re.element, options)) return false;
			if (!isCoveredAltNodes([le, ...left], right, options)) return false;
			const decrementRe = re.decrementMax();
			if (decrementRe) return isCoveredAltNodes(left, [decrementRe, ...right], options);
		}
		else if (le.type === "NormalizedOptional") {
			if (isCoveredAltNodes(left, [re, ...right], options)) return true;
			if (!isCoveredForNormalizedNode(le.element, re, options)) return false;
			const decrementLe = le.decrementMax();
			if (decrementLe) {
				if (isCoveredAltNodes([decrementLe, ...left], right, options)) return true;
			}
		} else if (!isCoveredForNormalizedNode(le, re, options)) return false;
	}
	if (!options.canOmitRight) {
		if (right.length) return false;
	}
	return !left.length;
}
/**
* Exclude the end optionals.
*/
function omitEnds(nodes) {
	for (let index = nodes.length - 1; index >= 0; index--) if (nodes[index].type !== "NormalizedOptional") return nodes.slice(0, index + 1);
	return [];
}
//#endregion
//#region lib/utils/regexp-ast/quantifier.ts
/**
* Get the offsets of the given quantifier
*/
function getQuantifierOffsets(qNode) {
	return [qNode.element.end - qNode.start, qNode.raw.length - (qNode.greedy ? 0 : 1)];
}
/**
* Returns the string representation of the given quantifier.
*/
function quantToString(quant) {
	if (quant.max < quant.min || quant.min < 0 || !Number.isInteger(quant.min) || !(Number.isInteger(quant.max) || quant.max === Infinity)) throw new Error(`Invalid quantifier { min: ${quant.min}, max: ${quant.max} }`);
	let value;
	if (quant.min === 0 && quant.max === 1) value = "?";
	else if (quant.min === 0 && quant.max === Infinity) value = "*";
	else if (quant.min === 1 && quant.max === Infinity) value = "+";
	else if (quant.min === quant.max) value = `{${quant.min}}`;
	else if (quant.max === Infinity) value = `{${quant.min},}`;
	else value = `{${quant.min},${quant.max}}`;
	if (quant.greedy === false) return `${value}?`;
	return value;
}
//#endregion
//#region lib/utils/regexp-ast/case-variation.ts
/**
* Returns flags equivalent to the given flags but with the `i` flag set.
*/
const getIgnoreCaseFlags = cachedFn((flags) => {
	return flags.ignoreCase ? flags : toCache({
		...flags,
		ignoreCase: true
	});
});
/**
* Returns flags equivalent to the given flags but without the `i` flag set.
*/
const getCaseSensitiveFlags = cachedFn((flags) => {
	return flags.ignoreCase === false ? flags : toCache({
		...flags,
		ignoreCase: false
	});
});
/**
* Returns whether the given element **will not** behave the same with or
* without the `i` flag.
*
* @param wholeCharacterClass Whether character classes will be checked as a
* whole or as a list of character class elements.
*
* If `false`, then the character class is case-variant if any of its elements
* is case-variant.
*
* Examples:
* - `wholeCharacterClass: true`: `isCaseVariant(/[a-zA-Z]/) -> false`
* - `wholeCharacterClass: false`: `isCaseVariant(/[a-zA-Z]/) -> true`
*/
function isCaseVariant(element, flags, wholeCharacterClass = true) {
	const unicodeLike = Boolean(flags.unicode || flags.unicodeSets);
	const iSet = getIgnoreCaseFlags(flags);
	const iUnset = getCaseSensitiveFlags(flags);
	/** Whether the given character class element is case variant */
	function ccElementIsCaseVariant(e) {
		switch (e.type) {
			case "Character": return toCharSet(e, iSet).size !== 1;
			case "CharacterClassRange": return !toCharSet(e, iSet).equals(toCharSet(e, iUnset));
			case "CharacterSet": switch (e.kind) {
				case "word": return unicodeLike;
				case "property": return !toUnicodeSet(e, iSet).equals(toUnicodeSet(e, iUnset));
				default: return false;
			}
			case "CharacterClass":
				if (!wholeCharacterClass) return e.elements.some(ccElementIsCaseVariant);
				return !toUnicodeSet(e, iSet).equals(toUnicodeSet(e, iUnset));
			case "ExpressionCharacterClass": return ccElementIsCaseVariant(e.expression);
			case "ClassIntersection":
			case "ClassSubtraction": return !toUnicodeSet(e, iSet).equals(toUnicodeSet(e, iUnset));
			case "ClassStringDisjunction":
				if (!wholeCharacterClass) return e.alternatives.some(ccElementIsCaseVariant);
				return !toUnicodeSet(e, iSet).equals(toUnicodeSet(e, iUnset));
			case "StringAlternative": return e.elements.some(ccElementIsCaseVariant);
			default: return assertNever(e);
		}
	}
	return hasSomeDescendant(element, (d) => {
		switch (d.type) {
			case "Assertion": return unicodeLike && d.kind === "word";
			case "Backreference": {
				const outside = getReferencedGroupsFromBackreference(d).filter((resolved) => !hasSomeDescendant(element, resolved));
				if (outside.length === 0) return false;
				return !isEmptyBackreference(d, flags) && outside.some((resolved) => isCaseVariant(resolved, flags));
			}
			case "Character":
			case "CharacterClassRange":
			case "CharacterSet":
			case "CharacterClass":
			case "ExpressionCharacterClass":
			case "ClassIntersection":
			case "ClassSubtraction":
			case "ClassStringDisjunction":
			case "StringAlternative": return ccElementIsCaseVariant(d);
			default: return false;
		}
	}, (d) => {
		return d.type !== "CharacterClass" && d.type !== "CharacterClassRange" && d.type !== "ExpressionCharacterClass" && d.type !== "ClassStringDisjunction";
	});
}
/**
* Returns the actually referenced capturing group from the given backreference.
*/
function getReferencedGroupsFromBackreference(backRef) {
	return [backRef.resolved].flat().filter((group) => {
		const closestAncestor = getClosestAncestor(backRef, group);
		return closestAncestor !== group && closestAncestor.type === "Alternative";
	});
}
//#endregion
//#region lib/utils/regexp-ast/simplify-quantifier.ts
/** Returns whether the given node contains any assertions. */
const containsAssertions$1 = cachedFn((node) => {
	return hasSomeDescendant(node, (n) => n.type === "Assertion");
});
/** A cached (and curried) version of {@link getConsumedChars}. */
const cachedGetPossiblyConsumedChar = cachedFn((flags) => {
	return cachedFn((element) => getConsumedChars(element, flags));
});
const CANNOT_SIMPLIFY = { canSimplify: false };
/**
* Returns whether a quantifier `A{n,m}` can be simplified to `A{n}` where `n<m`.
*/
function canSimplifyQuantifier(quantifier, flags, parser) {
	if (quantifier.min === quantifier.max) return CANNOT_SIMPLIFY;
	if (isZeroLength(quantifier, flags)) return CANNOT_SIMPLIFY;
	if (containsAssertions$1(quantifier)) return CANNOT_SIMPLIFY;
	const direction = getMatchingDirection(quantifier);
	const preceding = getPrecedingQuantifiers(quantifier, direction, flags);
	if (!preceding) return CANNOT_SIMPLIFY;
	return canAbsorb(preceding, {
		direction,
		flags,
		parser,
		quantifier
	});
}
/**
* Returns whether all of the given quantifiers can fully absorb the given
* quantifier.
*/
function canAbsorb(initialPreceding, options) {
	const { direction, flags, parser, quantifier } = options;
	const preceding = removeTargetQuantifier(initialPreceding, quantifier, direction, flags);
	if (!preceding) return CANNOT_SIMPLIFY;
	const dependencies = [...preceding];
	const CAN_SIMPLIFY = {
		canSimplify: true,
		dependencies
	};
	const fast = everyMaybe(preceding, (q) => canAbsorbElementFast(q, quantifier.element, flags));
	if (typeof fast === "boolean") return fast ? CAN_SIMPLIFY : CANNOT_SIMPLIFY;
	const formal = everyMaybe(fast, (q) => canAbsorbElementFormal(q, quantifier.element, parser));
	if (typeof formal === "boolean") return formal ? CAN_SIMPLIFY : CANNOT_SIMPLIFY;
	return formal.every((q) => {
		const parts = splitQuantifierIntoTails(q, direction, flags);
		if (!parts) return false;
		const result = canAbsorb(parts, options);
		if (result.canSimplify) dependencies.push(...result.dependencies);
		return result.canSimplify;
	}) ? CAN_SIMPLIFY : CANNOT_SIMPLIFY;
}
/**
* A maybe bool version `Array.every`. If at least one item maps to `false`,
* `false` will be returned. If all items map to `true`, `true` will be
* returned. Otherwise, all items that map to maybe will be returned.
*/
function everyMaybe(array, fn) {
	const maybe = [];
	for (const item of array) {
		const result = fn(item);
		if (result === false) return false;
		if (result === void 0) maybe.push(item);
	}
	if (maybe.length === 0) return true;
	return maybe;
}
/**
* Returns whether `Q = QE*`.
*
* This is implemented using a fast method based on single-character quantifiers.
*/
function canAbsorbElementFast(quantifier, element, flags) {
	if (!quantifier.greedy) return false;
	if (!isNonFinite(quantifier, flags)) return false;
	const qChar = cachedGetPossiblyConsumedChar(flags)(quantifier.element);
	const eChar = cachedGetPossiblyConsumedChar(flags)(element);
	if (qChar.chars.isDisjointWith(eChar.chars)) return false;
	if (eChar.exact && !eChar.chars.without(qChar.chars).isEmpty) return false;
	if (containsAssertions$1(quantifier) || containsAssertions$1(element)) return;
	if (quantifier.element.type === "Character" || quantifier.element.type === "CharacterClass" || quantifier.element.type === "CharacterSet") {
		if (quantifier.max !== Infinity) return false;
		if (qChar.exact && qChar.chars.isSupersetOf(eChar.chars)) return true;
	}
}
/** Returns whether the given node accepts a non-finite language. */
function isNonFinite(node, flags) {
	return hasSomeDescendant(node, (n) => n.type === "Quantifier" && n.max === Infinity && !isZeroLength(n.element, flags), (n) => n.type !== "Assertion");
}
/** Returns the NFA for the given element. */
function toNfa(element, parser) {
	const { expression, maxCharacter } = parser.parseElement(element, {
		maxNodes: 1e3,
		assertions: "throw",
		backreferences: "throw"
	});
	return NFA.fromRegex(expression, { maxCharacter }, {}, new NFA.LimitedNodeFactory(1e3));
}
/**
* Returns whether `Q = QE*`.
*
* This is implemented using a slow NFA/DFA based method.
*/
function canAbsorbElementFormal(quantifier, element, parser) {
	if (containsAssertions$1(quantifier) || containsAssertions$1(element)) return;
	try {
		const qNfa = toNfa(quantifier, parser);
		const qDfa = DFA.fromFA(qNfa, new DFA.LimitedNodeFactory(1e3));
		const eNfa = toNfa(element, parser);
		eNfa.quantify(0, 1);
		qNfa.append(eNfa);
		const qeDfa = DFA.fromFA(qNfa, new DFA.LimitedNodeFactory(1e3));
		qDfa.minimize();
		qeDfa.minimize();
		return qDfa.structurallyEqual(qeDfa);
	} catch {}
}
/**
* Returns all quantifiers that precede a hypothetical element after the given quantifier.
*/
function splitQuantifierIntoTails(quantifier, direction, flags) {
	if (isPotentiallyZeroLength(quantifier, flags)) return;
	return getTailQuantifiers(quantifier.element, direction, flags);
}
/**
* Removes the given target quantifier from the list of quantifiers. This is
* done by replacing quantifiers that contain the target quantifier with their
* tail quantifiers.
*
* The returned quantifiers are guaranteed to not contain the target.
*/
function removeTargetQuantifier(quantifiers, target, direction, flags) {
	const result = [];
	for (const q of quantifiers) if (hasSomeDescendant(q, target)) {
		const inner = splitQuantifierIntoTails(q, direction, flags);
		if (inner === void 0) return;
		const mapped = removeTargetQuantifier(inner, target, direction, flags);
		if (mapped === void 0) return;
		result.push(...mapped);
	} else result.push(q);
	return result;
}
/** Unions the given quantifier sets. */
function unionQuantifiers(sets) {
	const result = [];
	for (const set of sets) {
		if (set === void 0) return;
		result.push(...set);
	}
	if (result.length === 0) return void 0;
	return [...new Set(result)];
}
/**
* Returns all quantifier that are guaranteed to always be at the end of the given element.
*/
function getTailQuantifiers(element, direction, flags) {
	switch (element.type) {
		case "Assertion":
		case "Backreference":
		case "Character":
		case "CharacterClass":
		case "CharacterSet":
		case "ExpressionCharacterClass": return;
		case "Quantifier": return [element];
		case "Group":
		case "CapturingGroup": return unionQuantifiers(element.alternatives.map((a) => getTailQuantifiers(a, direction, flags)));
		case "Alternative": {
			const elements = direction === "ltr" ? reversed(element.elements) : element.elements;
			for (const e of elements) {
				if (isEmpty(e, flags)) continue;
				if (e.type === "Quantifier") return [e];
				return;
			}
			const { parent } = element;
			if (parent.type === "Pattern") return;
			if (parent.type === "Assertion") return;
			return getPrecedingQuantifiers(parent, direction, flags);
		}
		default: return assertNever(element);
	}
}
/**
* Returns the quantifier always directly preceding the given element, if any.
*/
function getPrecedingQuantifiers(element, direction, flags) {
	const parent = element.parent;
	if (parent.type === "Quantifier") {
		if (parent.max === 0) return;
		if (parent.max === 1) return getPrecedingQuantifiers(parent, direction, flags);
		return unionQuantifiers([getPrecedingQuantifiers(parent, direction, flags), getTailQuantifiers(parent.element, direction, flags)]);
	}
	if (parent.type !== "Alternative") return;
	const inc = direction === "ltr" ? -1 : 1;
	const { elements } = parent;
	const elementIndex = elements.indexOf(element);
	for (let precedingIndex = elementIndex + inc; precedingIndex >= 0 && precedingIndex < elements.length; precedingIndex += inc) {
		const preceding = parent.elements[precedingIndex];
		if (isEmpty(preceding, flags)) continue;
		return getTailQuantifiers(preceding, direction, flags);
	}
	if (parent.parent.type === "Pattern") return;
	return getPrecedingQuantifiers(parent.parent, direction, flags);
}
//#endregion
//#region lib/utils/ts-util.ts
const require = module.createRequire(import.meta.url);
/**
* Get TypeScript tools
*/
function getTypeScriptTools(context) {
	const sourceCode = context.sourceCode;
	const ts = getTypeScript();
	const tsNodeMap = sourceCode.parserServices.esTreeNodeToTSNodeMap;
	const usedTS = Boolean(ts && tsNodeMap);
	const hasFullTypeInformation = usedTS && sourceCode.parserServices.hasFullTypeInformation !== false;
	const checker = hasFullTypeInformation && sourceCode.parserServices.program && sourceCode.parserServices.program.getTypeChecker() || null;
	return {
		tsNodeMap: tsNodeMap || /* @__PURE__ */ new Map(),
		checker,
		usedTS,
		hasFullTypeInformation
	};
}
let cacheTypeScript;
/**
* Get TypeScript tools
*/
function getTypeScript() {
	try {
		return cacheTypeScript ??= require("typescript");
	} catch (e) {
		if (e.code === "MODULE_NOT_FOUND") return;
		if (typeof require === "undefined" || typeof require.define === "function") return;
		if (typeof e.message === "string" && e.message.includes("Dynamic require") && e.message.includes("is not supported")) return;
		throw e;
	}
}
/**
* Check if a given type is an array-like type or not.
*/
function isArrayLikeObject(tsType) {
	const ts = getTypeScript();
	return isObject(tsType) && (tsType.objectFlags & (ts.ObjectFlags.ArrayLiteral | ts.ObjectFlags.EvolvingArray | ts.ObjectFlags.Tuple)) !== 0;
}
/**
* Check if a given type is an interface type or not.
*/
function isClassOrInterface(tsType) {
	const ts = getTypeScript();
	return isObject(tsType) && (tsType.objectFlags & ts.ObjectFlags.ClassOrInterface) !== 0;
}
/**
* Check if a given type is an object type or not.
*/
function isObject(tsType) {
	const ts = getTypeScript();
	return (tsType.flags & ts.TypeFlags.Object) !== 0;
}
/**
* Check if a given type is a reference type or not.
*/
function isReferenceObject(tsType) {
	const ts = getTypeScript();
	return isObject(tsType) && (tsType.objectFlags & ts.ObjectFlags.Reference) !== 0;
}
/**
* Check if a given type is a union-or-intersection type or not.
*/
function isUnionOrIntersection(tsType) {
	const ts = getTypeScript();
	return (tsType.flags & ts.TypeFlags.UnionOrIntersection) !== 0;
}
/**
* Check if a given type is a type-parameter type or not.
*/
function isTypeParameter(tsType) {
	const ts = getTypeScript();
	return (tsType.flags & ts.TypeFlags.TypeParameter) !== 0;
}
/**
* Check if a given type is an any type or not.
*/
function isAny(tsType) {
	const ts = getTypeScript();
	return (tsType.flags & ts.TypeFlags.Any) !== 0;
}
/**
* Check if a given type is an unknown type or not.
*/
function isUnknown(tsType) {
	const ts = getTypeScript();
	return (tsType.flags & ts.TypeFlags.Unknown) !== 0;
}
/**
* Check if a given type is an string-like type or not.
*/
function isStringLine(tsType) {
	const ts = getTypeScript();
	return (tsType.flags & ts.TypeFlags.StringLike) !== 0;
}
/**
* Check if a given type is an number-like type or not.
*/
function isNumberLike(tsType) {
	const ts = getTypeScript();
	return (tsType.flags & ts.TypeFlags.NumberLike) !== 0;
}
/**
* Check if a given type is an boolean-like type or not.
*/
function isBooleanLike(tsType) {
	const ts = getTypeScript();
	return (tsType.flags & ts.TypeFlags.BooleanLike) !== 0;
}
/**
* Check if a given type is an bigint-like type or not.
*/
function isBigIntLike(tsType) {
	const ts = getTypeScript();
	return (tsType.flags & ts.TypeFlags.BigIntLike) !== 0;
}
/**
* Check if a given type is an null type or not.
*/
function isNull(tsType) {
	const ts = getTypeScript();
	return (tsType.flags & ts.TypeFlags.Null) !== 0;
}
//#endregion
//#region lib/utils/type-tracker/jsdoc.ts
var JSDocParams = class {
	params = [];
	isEmpty() {
		return this.params.length === 0;
	}
	add(paths, param) {
		const name = paths.shift();
		if (paths.length > 0) {
			for (const rootParam of this.params) if (rootParam.name === name) {
				rootParam.add(paths, param);
				return;
			}
		}
		this.params.push(new JSDocParam(name || null, param));
	}
	get(paths) {
		const { name, index } = paths.shift();
		if (name) {
			for (const param of this.params) if (param.name === name) return paths.length ? param.get(paths) : param.param;
		}
		if (index != null) {
			const param = this.params[index];
			if (param) return paths.length ? param.get(paths) : param.param;
		}
		return null;
	}
};
var JSDocParam = class extends JSDocParams {
	name;
	param;
	constructor(name, param) {
		super();
		this.name = name;
		this.param = param;
	}
};
const TAGS = {
	param: [
		"param",
		"arg",
		"argument"
	],
	returns: ["returns", "return"],
	type: ["type"]
};
var JSDoc = class {
	parsed;
	params = null;
	constructor(parsed) {
		this.parsed = parsed;
	}
	getTag(name) {
		for (const tag of this.genTags(name)) return tag;
		return null;
	}
	parseParams() {
		if (this.params) return this.params;
		const params = this.params = new JSDocParams();
		for (const param of this.genTags("param")) {
			const paths = (param.name || "").split(/\./u);
			params.add(paths, param);
		}
		return params;
	}
	*genTags(name) {
		const names = TAGS[name];
		for (const tag of this.parsed.tags) if (names.includes(tag.tag)) yield tag;
	}
};
/**
* Get the JSDoc comment for a given expression node.
*/
function getJSDoc(node, context) {
	const sourceCode = context.sourceCode;
	const jsdoc = findJSDocComment(node, sourceCode);
	if (jsdoc) try {
		const parsed = commentParser.parse(`/*${jsdoc.value}*/`)[0];
		return new JSDoc(parsed);
	} catch {}
	return null;
}
/**
* Finds a JSDoc comment for the given node.
*/
function findJSDocComment(node, sourceCode) {
	let target = node;
	let tokenBefore = null;
	while (target) {
		tokenBefore = sourceCode.getTokenBefore(target, { includeComments: true });
		if (!tokenBefore) return null;
		if (tokenBefore.type === "Keyword" && target.type === "VariableDeclarator") {
			if (tokenBefore.value === "const" || tokenBefore.value === "let" || tokenBefore.value === "var") {
				target = tokenBefore;
				continue;
			}
		}
		if (tokenBefore.type === "Punctuator") {
			if (tokenBefore.value === "(") {
				target = tokenBefore;
				continue;
			}
		}
		if (isCommentToken(tokenBefore)) {
			if (tokenBefore.type === "Line") {
				target = tokenBefore;
				continue;
			}
		}
		break;
	}
	if (tokenBefore && tokenBefore.type === "Block" && tokenBefore.value[0] === "*") return tokenBefore;
	return null;
}
/**
* Parse JSDoc type text
*/
function parseTypeText(text) {
	try {
		return jsdocTypeParser.tryParse(text);
	} catch {
		if (text.trim() === "function") return jsdocTypeParser.tryParse("Function");
		return null;
	}
}
//#endregion
//#region lib/utils/type-tracker/type-data/common.ts
/** Check whether given type is TypeClass */
function isTypeClass(type) {
	if (!type) return false;
	if (typeof type === "string") return false;
	return true;
}
/** Checks whither given types is equals */
function isEquals(t1, t2) {
	if (t1 === t2) return true;
	if (isTypeClass(t1) && isTypeClass(t2)) return t1.equals(t2);
	return false;
}
/**
* Checks if the result has the given type.
*/
function hasType(result, type) {
	if (result == null) return false;
	if (typeof result === "string") return result === type;
	return result.has(type);
}
function createObject(t) {
	return Object.assign(Object.create(null), t);
}
var TypeCollection = class {
	generator;
	unknownIndex = null;
	constructor(generator) {
		const that = this;
		this.generator = generator ? function* () {
			let index = 0;
			for (const t of generator()) {
				if (t != null) yield t;
				else that.unknownIndex ??= index;
				index++;
			}
		} : () => [][Symbol.iterator]();
	}
	has(type) {
		for (const t of this.generator()) if (typeof t === "string") {
			if (t === type) return true;
		} else if (t.has(type)) return true;
		return false;
	}
	isOneType() {
		let first = null;
		for (const t of this.all()) if (first == null) first = t;
		else if (!isEquals(first, t)) return false;
		return true;
	}
	*tuple() {
		let index = 0;
		for (const t of this.generator()) {
			if (this.unknownIndex != null && index < this.unknownIndex) return;
			yield t;
			index++;
		}
	}
	*all() {
		const set = /* @__PURE__ */ new Set();
		for (const t of this.generator()) if (!set.has(t)) {
			set.add(t);
			yield t;
		}
	}
	*strings() {
		const set = /* @__PURE__ */ new Set();
		for (const t of this.all()) if (typeof t === "string") {
			const str = t;
			if (!set.has(str)) {
				set.add(t);
				yield str;
			}
		} else for (const str of t.typeNames()) if (!set.has(str)) {
			set.add(t);
			yield str;
		}
	}
};
/**
* Get the type name from given type.
*/
function getTypeName(type) {
	if (type == null) return null;
	if (typeof type === "string") return type;
	return type.typeNames().join("|");
}
//#endregion
//#region lib/utils/type-tracker/type-data/object.ts
const getObjectPrototypes = lazy(() => createObject({
	constructor: UNKNOWN_FUNCTION,
	toString: RETURN_STRING,
	toLocaleString: RETURN_STRING,
	valueOf: RETURN_UNKNOWN_OBJECT,
	hasOwnProperty: RETURN_BOOLEAN,
	isPrototypeOf: RETURN_BOOLEAN,
	propertyIsEnumerable: RETURN_BOOLEAN
}));
var TypeObject = class {
	type = "Object";
	propertiesGenerator;
	constructor(propertiesGenerator) {
		this.propertiesGenerator = propertiesGenerator ?? (() => {
			return [][Symbol.iterator]();
		});
	}
	*allProperties() {
		const set = /* @__PURE__ */ new Set();
		for (const t of this.propertiesGenerator()) {
			if (set.has(t[0])) continue;
			set.add(t[0]);
			yield t;
		}
	}
	has(type) {
		return type === "Object";
	}
	paramType() {
		return null;
	}
	propertyType(name) {
		for (const [key, getValue] of this.allProperties()) if (key === name) return getValue();
		return getObjectPrototypes()[name] || null;
	}
	iterateType() {
		return null;
	}
	returnType() {
		return null;
	}
	typeNames() {
		return ["Object"];
	}
	equals(o) {
		if (o.type !== "Object") return false;
		const itr2 = o.allProperties();
		const props2 = /* @__PURE__ */ new Map();
		for (const [key1, get1] of this.allProperties()) {
			const get2 = props2.get(key1);
			if (get2) {
				if (!isEquals(get1(), get2())) return false;
			} else {
				let e2 = itr2.next();
				while (!e2.done) {
					const [key2, get] = e2.value;
					props2.set(key2, get);
					if (key1 === key2) {
						if (!isEquals(get1(), get())) return false;
						break;
					}
					e2 = itr2.next();
				}
				if (e2.done) return false;
			}
		}
		if (!itr2.next().done) return false;
		return true;
	}
};
const UNKNOWN_OBJECT = new TypeObject();
/** Build Object constructor type */
function buildObjectConstructor() {
	const RETURN_ARG = new TypeFunction(
		/**
		* Function Type that Return argument
		*/
		function returnArg(_selfType, argTypes) {
			return argTypes[0]?.() ?? null;
		}
	);
	return new TypeGlobalFunction((_thisType, [argType]) => argType?.() ?? UNKNOWN_OBJECT, createObject({
		getPrototypeOf: null,
		getOwnPropertyDescriptor: null,
		getOwnPropertyNames: RETURN_STRING_ARRAY,
		create: null,
		defineProperty: null,
		defineProperties: null,
		seal: RETURN_ARG,
		freeze: RETURN_ARG,
		preventExtensions: null,
		isSealed: RETURN_BOOLEAN,
		isFrozen: RETURN_BOOLEAN,
		isExtensible: RETURN_BOOLEAN,
		keys: RETURN_STRING_ARRAY,
		assign: new TypeFunction(
			/**
			* Function Type that Return assign objects
			*/
			function returnAssign(selfType, argTypes) {
				return new TypeObject(function* () {
					for (const getType of [selfType, ...argTypes].reverse()) {
						const s = getType?.();
						if (isTypeClass(s) && s.type === "Object") yield* s.allProperties();
					}
				});
			}
		),
		getOwnPropertySymbols: RETURN_UNKNOWN_ARRAY,
		is: RETURN_BOOLEAN,
		setPrototypeOf: null,
		values: RETURN_UNKNOWN_ARRAY,
		entries: RETURN_UNKNOWN_ARRAY,
		getOwnPropertyDescriptors: null,
		fromEntries: null,
		hasOwn: RETURN_BOOLEAN,
		groupBy: null,
		prototype: null
	}));
}
//#endregion
//#region lib/utils/type-tracker/type-data/number.ts
var TypeNumber = class {
	type = "Number";
	has(type) {
		return type === "Number";
	}
	paramType() {
		return null;
	}
	propertyType(name) {
		return getPrototypes$9()[name] || null;
	}
	iterateType() {
		return null;
	}
	returnType() {
		return null;
	}
	typeNames() {
		return ["Number"];
	}
	equals(o) {
		return o.type === "Number";
	}
};
const NUMBER = new TypeNumber();
/** Build Number constructor type */
function buildNumberConstructor() {
	return new TypeGlobalFunction(() => NUMBER, createObject({
		MAX_VALUE: NUMBER,
		MIN_VALUE: NUMBER,
		NaN: NUMBER,
		NEGATIVE_INFINITY: NUMBER,
		POSITIVE_INFINITY: NUMBER,
		EPSILON: NUMBER,
		isFinite: RETURN_BOOLEAN,
		isInteger: RETURN_BOOLEAN,
		isNaN: RETURN_BOOLEAN,
		isSafeInteger: RETURN_BOOLEAN,
		MAX_SAFE_INTEGER: NUMBER,
		MIN_SAFE_INTEGER: NUMBER,
		parseFloat: RETURN_NUMBER,
		parseInt: RETURN_NUMBER,
		prototype: null
	}));
}
const getPrototypes$9 = lazy(() => createObject({
	...getObjectPrototypes(),
	toString: RETURN_STRING,
	toFixed: RETURN_STRING,
	toExponential: RETURN_STRING,
	toPrecision: RETURN_STRING,
	valueOf: RETURN_NUMBER,
	toLocaleString: RETURN_STRING
}));
//#endregion
//#region lib/utils/type-tracker/type-data/string.ts
var TypeString = class {
	type = "String";
	has(type) {
		return type === "String";
	}
	paramType() {
		return null;
	}
	propertyType(name) {
		if (name === "0") return this;
		return getPrototypes$8()[name] || null;
	}
	iterateType() {
		return this;
	}
	returnType() {
		return null;
	}
	typeNames() {
		return ["String"];
	}
	equals(o) {
		return o.type === "String";
	}
};
const STRING = new TypeString();
/** Build String constructor type */
function buildStringConstructor() {
	return new TypeGlobalFunction(() => STRING, createObject({
		fromCharCode: RETURN_STRING,
		fromCodePoint: RETURN_STRING,
		raw: RETURN_STRING,
		prototype: null
	}));
}
const getPrototypes$8 = lazy(() => createObject({
	...getObjectPrototypes(),
	toString: RETURN_STRING,
	charAt: RETURN_STRING,
	charCodeAt: RETURN_NUMBER,
	concat: RETURN_STRING,
	indexOf: RETURN_NUMBER,
	lastIndexOf: RETURN_NUMBER,
	localeCompare: RETURN_NUMBER,
	match: RETURN_STRING_ARRAY,
	replace: RETURN_STRING,
	search: RETURN_NUMBER,
	slice: RETURN_STRING,
	split: RETURN_STRING_ARRAY,
	substring: RETURN_STRING,
	toLowerCase: RETURN_STRING,
	toLocaleLowerCase: RETURN_STRING,
	toUpperCase: RETURN_STRING,
	toLocaleUpperCase: RETURN_STRING,
	trim: RETURN_STRING,
	substr: RETURN_STRING,
	valueOf: RETURN_STRING,
	codePointAt: RETURN_NUMBER,
	includes: RETURN_BOOLEAN,
	endsWith: RETURN_BOOLEAN,
	normalize: RETURN_STRING,
	repeat: RETURN_STRING,
	startsWith: RETURN_BOOLEAN,
	anchor: RETURN_STRING,
	big: RETURN_STRING,
	blink: RETURN_STRING,
	bold: RETURN_STRING,
	fixed: RETURN_STRING,
	fontcolor: RETURN_STRING,
	fontsize: RETURN_STRING,
	italics: RETURN_STRING,
	link: RETURN_STRING,
	small: RETURN_STRING,
	strike: RETURN_STRING,
	sub: RETURN_STRING,
	sup: RETURN_STRING,
	padStart: RETURN_STRING,
	padEnd: RETURN_STRING,
	trimLeft: RETURN_STRING,
	trimRight: RETURN_STRING,
	trimStart: RETURN_STRING,
	trimEnd: RETURN_STRING,
	matchAll: null,
	replaceAll: RETURN_STRING,
	at: RETURN_STRING,
	isWellFormed: RETURN_BOOLEAN,
	toWellFormed: RETURN_STRING,
	length: NUMBER,
	0: STRING,
	[Symbol.iterator]: null
}));
//#endregion
//#region lib/utils/type-tracker/type-data/bigint.ts
var TypeBigInt = class {
	type = "BigInt";
	has(type) {
		return type === "BigInt";
	}
	paramType() {
		return null;
	}
	propertyType(name) {
		return getPrototypes$7()[name] || null;
	}
	iterateType() {
		return null;
	}
	returnType() {
		return null;
	}
	typeNames() {
		return ["BigInt"];
	}
	equals(o) {
		return o.type === "BigInt";
	}
};
const BIGINT = new TypeBigInt();
/** Build BigInt constructor type */
function buildBigIntConstructor() {
	return new TypeGlobalFunction(() => BIGINT, createObject({
		asIntN: RETURN_BIGINT,
		asUintN: RETURN_BIGINT,
		prototype: null
	}));
}
const getPrototypes$7 = lazy(() => createObject({
	...getObjectPrototypes(),
	toString: RETURN_STRING,
	toLocaleString: RETURN_STRING,
	valueOf: RETURN_BIGINT,
	[Symbol.toStringTag]: STRING
}));
//#endregion
//#region lib/utils/type-tracker/type-data/boolean.ts
var TypeBoolean = class {
	type = "Boolean";
	has(type) {
		return type === "Boolean";
	}
	paramType() {
		return null;
	}
	propertyType(name) {
		return getPrototypes$6()[name] || null;
	}
	iterateType() {
		return null;
	}
	returnType() {
		return null;
	}
	typeNames() {
		return ["Boolean"];
	}
	equals(o) {
		return o.type === "Boolean";
	}
};
const BOOLEAN = new TypeBoolean();
/** Build BigInt constructor type */
function buildBooleanConstructor() {
	return new TypeGlobalFunction(() => BOOLEAN, createObject({ prototype: null }));
}
const getPrototypes$6 = lazy(() => createObject({
	...getObjectPrototypes(),
	valueOf: RETURN_BOOLEAN
}));
//#endregion
//#region lib/utils/type-tracker/type-data/regexp.ts
var TypeRegExp = class {
	type = "RegExp";
	has(type) {
		return type === "RegExp";
	}
	paramType() {
		return null;
	}
	propertyType(name) {
		return getPrototypes$5()[name] || null;
	}
	iterateType() {
		return null;
	}
	returnType() {
		return null;
	}
	typeNames() {
		return ["RegExp"];
	}
	equals(o) {
		return o.type === "RegExp";
	}
};
const REGEXP = new TypeRegExp();
/** Build RegExp constructor type */
function buildRegExpConstructor() {
	return new TypeGlobalFunction(() => REGEXP, createObject({
		$1: STRING,
		$2: STRING,
		$3: STRING,
		$4: STRING,
		$5: STRING,
		$6: STRING,
		$7: STRING,
		$8: STRING,
		$9: STRING,
		$_: STRING,
		"$&": STRING,
		"$+": STRING,
		"$`": STRING,
		"$'": STRING,
		input: STRING,
		lastParen: STRING,
		leftContext: STRING,
		rightContext: STRING,
		lastMatch: NUMBER,
		prototype: null,
		[Symbol.species]: null
	}));
}
const getPrototypes$5 = lazy(() => createObject({
	...getObjectPrototypes(),
	exec: RETURN_STRING_ARRAY,
	test: RETURN_BOOLEAN,
	source: STRING,
	global: BOOLEAN,
	ignoreCase: BOOLEAN,
	multiline: BOOLEAN,
	lastIndex: NUMBER,
	compile: RETURN_REGEXP,
	flags: STRING,
	sticky: BOOLEAN,
	unicode: BOOLEAN,
	dotAll: BOOLEAN,
	hasIndices: BOOLEAN,
	unicodeSets: BOOLEAN,
	[Symbol.match]: null,
	[Symbol.replace]: null,
	[Symbol.search]: null,
	[Symbol.split]: null,
	[Symbol.matchAll]: null
}));
//#endregion
//#region lib/utils/type-tracker/type-data/function.ts
var TypeFunction = class {
	type = "Function";
	fn;
	constructor(fn) {
		this.fn = fn;
	}
	has(type) {
		return type === "Function";
	}
	returnType(thisType, argTypes, meta) {
		return this.fn(thisType, argTypes, meta);
	}
	paramType() {
		return null;
	}
	propertyType(name) {
		return getPrototypes$4()[name] || null;
	}
	iterateType() {
		return null;
	}
	typeNames() {
		return ["Function"];
	}
	equals(_o) {
		return false;
	}
};
var TypeGlobalFunction = class extends TypeFunction {
	props;
	constructor(fn, props) {
		super(fn);
		this.props = props;
	}
	propertyType(name) {
		return this.props[name] || super.propertyType(name);
	}
};
const UNKNOWN_FUNCTION = new TypeFunction(
	/** Unknown Function Type */
	function returnUnknown() {
		return null;
	}
);
/** Build Function constructor type */
function buildFunctionConstructor() {
	return new TypeGlobalFunction(
		/** Function Type that Return Function */
		function returnFunction() {
			return UNKNOWN_FUNCTION;
		},
		createObject({ prototype: null })
	);
}
const RETURN_VOID = new TypeFunction(
	/** Function Type that Return void */
	function retVoid() {
		return "undefined";
	}
);
const RETURN_STRING = new TypeFunction(
	/** Function Type that Return string */
	function returnString() {
		return STRING;
	}
);
const RETURN_NUMBER = new TypeFunction(
	/** Function Type that Return number */
	function returnNumber() {
		return NUMBER;
	}
);
const RETURN_BOOLEAN = new TypeFunction(
	/** Function Type that Return boolean */
	function returnBoolean() {
		return BOOLEAN;
	}
);
const RETURN_UNKNOWN_ARRAY = new TypeFunction(
	/**
	* Function Type that Return unknown array
	*/
	function returnUnknownArray() {
		return UNKNOWN_ARRAY;
	}
);
const RETURN_STRING_ARRAY = new TypeFunction(
	/**
	* Function Type that Return unknown array
	*/
	function returnStringArray() {
		return STRING_ARRAY;
	}
);
const RETURN_UNKNOWN_OBJECT = new TypeFunction(
	/** Function Type that Return Object */
	function returnObject() {
		return UNKNOWN_OBJECT;
	}
);
const RETURN_REGEXP = new TypeFunction(
	/** Function Type that Return RegExp */
	function returnRegExp() {
		return REGEXP;
	}
);
const RETURN_BIGINT = new TypeFunction(
	/** Function Type that Return BigInt */
	function returnBigInt() {
		return BIGINT;
	}
);
const RETURN_SELF = new TypeFunction(
	/**
	* Function Type that Return self array
	*/
	function returnSelf(selfType) {
		return selfType?.() ?? null;
	}
);
const getPrototypes$4 = lazy(() => createObject({
	...getObjectPrototypes(),
	toString: RETURN_STRING,
	bind: RETURN_SELF,
	length: NUMBER,
	name: STRING,
	apply: UNKNOWN_FUNCTION,
	call: UNKNOWN_FUNCTION,
	arguments: null,
	caller: UNKNOWN_FUNCTION,
	prototype: null,
	[Symbol.hasInstance]: null,
	[Symbol.metadata]: null
}));
//#endregion
//#region lib/utils/type-tracker/type-data/iterable.ts
const getPrototypes$3 = lazy(() => {
	return createObject({
		...getObjectPrototypes(),
		[Symbol.iterator]: null
	});
});
var TypeIterable = class {
	type = "Iterable";
	param0;
	constructor(param0) {
		this.param0 = param0;
	}
	has(_type) {
		return false;
	}
	paramType(index) {
		if (index === 0) return this.param0();
		return null;
	}
	propertyType(name) {
		return getPrototypes$3()[name] || null;
	}
	iterateType() {
		return this.paramType(0);
	}
	returnType() {
		return null;
	}
	typeNames() {
		const param0 = getTypeName(this.iterateType());
		return [`Iterable${param0 != null ? `<${param0}>` : ""}`];
	}
	equals(o) {
		if (o.type !== "Iterable") return false;
		return isEquals(this.iterateType(), o.iterateType());
	}
};
const UNKNOWN_ITERABLE = new TypeIterable(() => null);
//#endregion
//#region lib/utils/type-tracker/type-data/union-or-intersection.ts
var TypeUnionOrIntersection = class TypeUnionOrIntersection {
	type = "TypeUnionOrIntersection";
	collection;
	static buildType(generator) {
		const collection = new TypeCollection(generator);
		if (collection.isOneType()) {
			for (const t of collection.all()) return t;
			return null;
		}
		return new TypeUnionOrIntersection(() => collection.all());
	}
	constructor(generator) {
		this.collection = new TypeCollection(generator);
	}
	has(type) {
		return this.collection.has(type);
	}
	paramType() {
		return null;
	}
	propertyType(name) {
		const baseCollection = this.collection;
		return TypeUnionOrIntersection.buildType(function* () {
			for (const type of baseCollection.all()) {
				const propType = isTypeClass(type) ? type.propertyType(name) : null;
				if (propType) yield propType;
			}
		});
	}
	iterateType() {
		const baseCollection = this.collection;
		return TypeUnionOrIntersection.buildType(function* () {
			for (const type of baseCollection.all()) if (isTypeClass(type)) {
				const itrType = type.iterateType();
				if (itrType) yield itrType;
			}
		});
	}
	returnType(thisType, argTypes) {
		const baseCollection = this.collection;
		return TypeUnionOrIntersection.buildType(function* () {
			for (const type of baseCollection.all()) if (isTypeClass(type)) {
				const itrType = type.returnType(thisType, argTypes);
				if (itrType) yield itrType;
			}
		});
	}
	typeNames() {
		return [...this.collection.strings()].sort();
	}
	equals(o) {
		if (o.type !== "TypeUnionOrIntersection") return false;
		const itr1 = this.collection.all();
		const itr2 = o.collection.all();
		let e1 = itr1.next();
		let e2 = itr2.next();
		while (!e1.done && !e2.done) {
			if (!isEquals(e1.value, e2.value)) return false;
			e1 = itr1.next();
			e2 = itr2.next();
		}
		return e1.done === e2.done;
	}
};
//#endregion
//#region lib/utils/type-tracker/type-data/array.ts
var TypeArray = class {
	type = "Array";
	collection;
	maybeTuple;
	constructor(generator, maybeTuple) {
		this.collection = new TypeCollection(generator);
		this.maybeTuple = maybeTuple ?? false;
	}
	has(type) {
		return type === "Array";
	}
	paramType(index) {
		if (index === 0) return TypeUnionOrIntersection.buildType(() => this.collection.all());
		return null;
	}
	at(index) {
		if (!this.maybeTuple) return null;
		let i = 0;
		for (const t of this.collection.tuple()) {
			if (i === index) return t;
			i++;
		}
		return null;
	}
	propertyType(name) {
		if (name === "0") return this.paramType(0);
		return getPrototypes$2()[name] || null;
	}
	iterateType() {
		return this.paramType(0);
	}
	returnType() {
		return null;
	}
	typeNames() {
		const param0 = getTypeName(this.iterateType());
		return [`Array${param0 ? `<${param0}>` : ""}`];
	}
	equals(o) {
		if (o.type !== "Array") return false;
		return isEquals(this.iterateType(), o.iterateType());
	}
};
const UNKNOWN_ARRAY = new TypeArray();
const STRING_ARRAY = new TypeArray(() => [STRING][Symbol.iterator]());
/** Build Array constructor type */
function buildArrayConstructor() {
	return new TypeGlobalFunction(() => UNKNOWN_ARRAY, createObject({
		isArray: RETURN_BOOLEAN,
		from: RETURN_UNKNOWN_ARRAY,
		of: RETURN_UNKNOWN_ARRAY,
		prototype: null,
		[Symbol.species]: null,
		fromAsync: null
	}));
}
const getPrototypes$2 = lazy(() => {
	const RETURN_ARRAY_ELEMENT = new TypeFunction(
		/**
		* Function Type that Return array element
		*/
		function returnArrayElement(selfType) {
			const type = selfType?.();
			if (!isTypeClass(type)) return null;
			return type.paramType(0);
		}
	);
	const RETURN_SELF = new TypeFunction(
		/**
		* Function Type that Return self array
		*/
		function returnSelf(selfType) {
			return selfType?.() ?? null;
		}
	);
	const RETURN_CONCAT = new TypeFunction(
		/**
		* Function Type that Return concat array
		*/
		function returnConcat(selfType, argTypes) {
			return new TypeArray(function* () {
				for (const getType of [selfType, ...argTypes]) {
					const s = getType?.();
					if (isTypeClass(s)) yield s.iterateType();
					else yield null;
				}
			});
		}
	);
	const RETURN_ENTRIES = new TypeFunction(
		/**
		* Function Type that Return entries
		*/
		function(selfType) {
			return new TypeIterable(() => {
				return new TypeArray(function* () {
					yield NUMBER;
					const type = selfType?.();
					if (isTypeClass(type)) yield type.iterateType();
				});
			});
		}
	);
	const RETURN_KEYS = new TypeFunction(
		/**
		* Function Type that Return keys
		*/
		function() {
			return new TypeIterable(() => {
				return NUMBER;
			});
		}
	);
	const RETURN_VALUES = new TypeFunction(
		/**
		* Function Type that Return values
		*/
		function(selfType) {
			return new TypeIterable(() => {
				const type = selfType?.();
				if (isTypeClass(type)) return type.iterateType();
				return null;
			});
		}
	);
	const RETURN_MAP = new TypeFunction(
		/**
		* Function Type that Return map
		*/
		function(selfType, [argType]) {
			return new TypeArray(function* () {
				const type = argType?.();
				if (isTypeClass(type)) yield type.returnType(selfType, [() => {
					const s = selfType?.();
					return isTypeClass(s) ? s.iterateType() : null;
				}, () => NUMBER]);
			});
		}
	);
	return createObject({
		...getObjectPrototypes(),
		toString: RETURN_STRING,
		toLocaleString: RETURN_STRING,
		pop: RETURN_ARRAY_ELEMENT,
		push: RETURN_NUMBER,
		concat: RETURN_CONCAT,
		join: RETURN_STRING,
		reverse: RETURN_SELF,
		shift: RETURN_ARRAY_ELEMENT,
		slice: RETURN_SELF,
		sort: RETURN_SELF,
		splice: RETURN_SELF,
		unshift: RETURN_NUMBER,
		indexOf: RETURN_NUMBER,
		lastIndexOf: RETURN_NUMBER,
		every: RETURN_BOOLEAN,
		some: RETURN_BOOLEAN,
		forEach: RETURN_VOID,
		map: RETURN_MAP,
		filter: RETURN_SELF,
		reduce: null,
		reduceRight: null,
		find: RETURN_ARRAY_ELEMENT,
		findIndex: RETURN_NUMBER,
		fill: RETURN_UNKNOWN_ARRAY,
		copyWithin: RETURN_SELF,
		entries: RETURN_ENTRIES,
		keys: RETURN_KEYS,
		values: RETURN_VALUES,
		includes: RETURN_BOOLEAN,
		flatMap: RETURN_UNKNOWN_ARRAY,
		flat: RETURN_UNKNOWN_ARRAY,
		at: RETURN_ARRAY_ELEMENT,
		findLast: RETURN_ARRAY_ELEMENT,
		findLastIndex: RETURN_NUMBER,
		toReversed: RETURN_SELF,
		toSorted: RETURN_SELF,
		toSpliced: RETURN_SELF,
		with: RETURN_SELF,
		length: NUMBER,
		0: null,
		[Symbol.iterator]: null,
		[Symbol.unscopables]: null
	});
});
//#endregion
//#region lib/utils/type-tracker/type-data/map.ts
const getPrototypes$1 = lazy(() => {
	const RETURN_MAP_VALUE = new TypeFunction(
		/**
		* Function Type that Return Map value
		*/
		function returnMapValue(selfType) {
			const type = selfType?.();
			if (!isTypeClass(type)) return null;
			return type.paramType(1);
		}
	);
	const RETURN_SELF = new TypeFunction(
		/**
		* Function Type that Return self array
		*/
		function returnSelf(selfType) {
			return selfType?.() ?? null;
		}
	);
	const RETURN_ENTRIES = new TypeFunction(
		/**
		* Function Type that Return entries
		*/
		function(selfType) {
			return new TypeIterable(() => {
				return new TypeArray(function* () {
					const type = selfType?.();
					if (isTypeClass(type)) {
						yield type.paramType(0);
						yield type.paramType(1);
					} else {
						yield null;
						yield null;
					}
				}, true);
			});
		}
	);
	const RETURN_KEYS = new TypeFunction(
		/**
		* Function Type that Return keys
		*/
		function(selfType) {
			return new TypeIterable(() => {
				const type = selfType?.();
				if (isTypeClass(type)) return type.paramType(0);
				return null;
			});
		}
	);
	const RETURN_VALUES = new TypeFunction(
		/**
		* Function Type that Return values
		*/
		function(selfType) {
			return new TypeIterable(() => {
				const type = selfType?.();
				if (isTypeClass(type)) return type.paramType(1);
				return null;
			});
		}
	);
	return createObject({
		...getObjectPrototypes(),
		clear: RETURN_VOID,
		delete: RETURN_BOOLEAN,
		forEach: RETURN_VOID,
		get: RETURN_MAP_VALUE,
		has: RETURN_BOOLEAN,
		set: RETURN_SELF,
		size: NUMBER,
		entries: RETURN_ENTRIES,
		keys: RETURN_KEYS,
		values: RETURN_VALUES,
		[Symbol.iterator]: null,
		[Symbol.toStringTag]: STRING
	});
});
var TypeMap = class {
	type = "Map";
	param0;
	param1;
	constructor(param0, param1) {
		this.param0 = param0;
		this.param1 = param1;
	}
	has(type) {
		return type === "Map";
	}
	paramType(index) {
		if (index === 0) return this.param0();
		if (index === 1) return this.param1();
		return null;
	}
	propertyType(name) {
		return getPrototypes$1()[name] || null;
	}
	iterateType() {
		const map = this;
		return new TypeArray(function* () {
			yield map.paramType(0);
			yield map.paramType(1);
		}, true);
	}
	returnType() {
		return null;
	}
	typeNames() {
		const param0 = getTypeName(this.paramType(0));
		const param1 = getTypeName(this.paramType(1));
		return [`Map${param0 != null && param1 != null ? `<${param0},${param1}>` : ""}`];
	}
	equals(o) {
		if (o.type !== "Map") return false;
		return isEquals(this.paramType(0), o.paramType(0)) && isEquals(this.paramType(1), o.paramType(1));
	}
};
const UNKNOWN_MAP = new TypeMap(() => null, () => null);
/** Build Map constructor type */
function buildMapConstructor() {
	return new TypeGlobalFunction(mapConstructor, createObject({
		prototype: null,
		[Symbol.species]: null,
		groupBy: null
	}));
}
/**
* Map constructor type
*/
function mapConstructor(_thisType, argTypes, meta) {
	if (!meta?.isConstructor) return null;
	const arg = argTypes[0]?.();
	if (isTypeClass(arg) && arg.type === "Array") {
		const iterateType = arg.iterateType();
		if (isTypeClass(iterateType) && iterateType.type === "Array") return new TypeMap(() => iterateType.at(0), () => iterateType.at(1));
	}
	return UNKNOWN_MAP;
}
//#endregion
//#region lib/utils/type-tracker/type-data/set.ts
const getPrototypes = lazy(() => {
	const RETURN_SELF = new TypeFunction(
		/**
		* Function Type that Return self array
		*/
		function returnSelf(selfType) {
			return selfType?.() ?? null;
		}
	);
	const RETURN_ENTRIES = new TypeFunction(
		/**
		* Function Type that Return entries
		*/
		function(selfType) {
			return new TypeIterable(() => {
				return new TypeArray(function* () {
					const type = selfType?.();
					if (isTypeClass(type)) {
						yield type.iterateType();
						yield type.iterateType();
					} else {
						yield null;
						yield null;
					}
				}, true);
			});
		}
	);
	const RETURN_KEYS = new TypeFunction(
		/**
		* Function Type that Return keys
		*/
		function(selfType) {
			return new TypeIterable(() => {
				const type = selfType?.();
				if (isTypeClass(type)) return type.iterateType();
				return null;
			});
		}
	);
	const RETURN_VALUES = new TypeFunction(
		/**
		* Function Type that Return values
		*/
		function(selfType) {
			return new TypeIterable(() => {
				const type = selfType?.();
				if (isTypeClass(type)) return type.iterateType();
				return null;
			});
		}
	);
	return createObject({
		...getObjectPrototypes(),
		clear: RETURN_VOID,
		delete: RETURN_BOOLEAN,
		forEach: RETURN_VOID,
		has: RETURN_BOOLEAN,
		add: RETURN_SELF,
		size: NUMBER,
		entries: RETURN_ENTRIES,
		keys: RETURN_KEYS,
		values: RETURN_VALUES,
		[Symbol.iterator]: null,
		[Symbol.toStringTag]: STRING,
		difference: RETURN_SELF,
		intersection: RETURN_SELF,
		isDisjointFrom: RETURN_BOOLEAN,
		isSubsetOf: RETURN_BOOLEAN,
		isSupersetOf: RETURN_BOOLEAN,
		symmetricDifference: RETURN_SELF,
		union: RETURN_SELF
	});
});
var TypeSet = class {
	type = "Set";
	param0;
	constructor(param0) {
		this.param0 = param0;
	}
	has(type) {
		return type === "Set";
	}
	paramType(index) {
		if (index === 0) return this.param0();
		return null;
	}
	propertyType(name) {
		return getPrototypes()[name] || null;
	}
	iterateType() {
		return this.paramType(0);
	}
	returnType() {
		return null;
	}
	typeNames() {
		const param0 = getTypeName(this.iterateType());
		return [`Set${param0 != null ? `<${param0}>` : ""}`];
	}
	equals(o) {
		if (o.type !== "Set") return false;
		return isEquals(this.iterateType(), o.iterateType());
	}
};
const UNKNOWN_SET = new TypeSet(() => null);
/** Build Set constructor type */
function buildSetConstructor() {
	return new TypeGlobalFunction(setConstructor, createObject({
		prototype: null,
		[Symbol.species]: null
	}));
}
/**
* Set constructor type
*/
function setConstructor(_thisType, argTypes, meta) {
	if (!meta?.isConstructor) return null;
	const arg = argTypes[0]?.();
	if (isTypeClass(arg)) return new TypeSet(() => arg.iterateType());
	return UNKNOWN_SET;
}
//#endregion
//#region lib/utils/type-tracker/type-data/global.ts
var TypeGlobal = class {
	type = "Global";
	has(_type) {
		return false;
	}
	paramType() {
		return null;
	}
	propertyType(name) {
		return getProperties()[name] || null;
	}
	iterateType() {
		return null;
	}
	returnType() {
		return null;
	}
	typeNames() {
		return ["Global"];
	}
	equals(o) {
		return o.type === "Global";
	}
};
const GLOBAL = new TypeGlobal();
const getProperties = lazy(() => createObject({
	String: buildStringConstructor(),
	Number: buildNumberConstructor(),
	Boolean: buildBooleanConstructor(),
	RegExp: buildRegExpConstructor(),
	BigInt: buildBigIntConstructor(),
	Array: buildArrayConstructor(),
	Object: buildObjectConstructor(),
	Function: buildFunctionConstructor(),
	Map: buildMapConstructor(),
	Set: buildSetConstructor(),
	isFinite: RETURN_BOOLEAN,
	isNaN: RETURN_BOOLEAN,
	parseFloat: RETURN_NUMBER,
	parseInt: RETURN_NUMBER,
	decodeURI: RETURN_STRING,
	decodeURIComponent: RETURN_STRING,
	encodeURI: RETURN_STRING,
	encodeURIComponent: RETURN_STRING,
	escape: RETURN_STRING,
	unescape: RETURN_STRING,
	globalThis: GLOBAL,
	window: GLOBAL,
	self: GLOBAL,
	global: GLOBAL,
	undefined: "undefined",
	Infinity: NUMBER,
	NaN: NUMBER
}));
//#endregion
//#region lib/utils/type-tracker/type-data/index.ts
/** Get BinaryExpression calc type */
function binaryNumOp(getTypes) {
	const [t1, t2] = getTypes();
	return TypeUnionOrIntersection.buildType(function* () {
		let unknown = true;
		if (hasType(t1, "Number") || hasType(t2, "Number")) {
			unknown = false;
			yield NUMBER;
		}
		if (hasType(t1, "BigInt") && hasType(t2, "BigInt")) {
			unknown = false;
			yield BIGINT;
		}
		if (unknown) {
			yield NUMBER;
			yield BIGINT;
		}
	});
}
/** Get condition type */
function resultBool() {
	return BOOLEAN;
}
/** Get BinaryExpression bitwise type */
function binaryBitwise() {
	return NUMBER;
}
const BI_OPERATOR_TYPES = createObject({
	"==": resultBool,
	"!=": resultBool,
	"===": resultBool,
	"!==": resultBool,
	"<": resultBool,
	"<=": resultBool,
	">": resultBool,
	">=": resultBool,
	in: resultBool,
	instanceof: resultBool,
	"-": binaryNumOp,
	"*": binaryNumOp,
	"/": binaryNumOp,
	"%": binaryNumOp,
	"^": binaryNumOp,
	"**": binaryNumOp,
	"&": binaryNumOp,
	"|": binaryNumOp,
	"<<": binaryBitwise,
	">>": binaryBitwise,
	">>>": binaryBitwise,
	"+": (getTypes) => {
		const [t1, t2] = getTypes();
		return TypeUnionOrIntersection.buildType(function* () {
			let unknown = true;
			if (hasType(t1, "String") || hasType(t2, "String")) {
				unknown = false;
				yield STRING;
			}
			if (hasType(t1, "Number") && hasType(t2, "Number")) {
				unknown = false;
				yield NUMBER;
			}
			if (hasType(t1, "BigInt") && hasType(t2, "BigInt")) {
				unknown = false;
				yield BIGINT;
			}
			if (unknown) {
				yield STRING;
				yield NUMBER;
				yield BIGINT;
			}
		});
	}
});
/** Get UnaryExpression calc type */
function unaryNumOp(getType) {
	const t = getType();
	return TypeUnionOrIntersection.buildType(function* () {
		let unknown = true;
		if (hasType(t, "Number")) {
			unknown = false;
			yield NUMBER;
		}
		if (hasType(t, "BigInt")) {
			unknown = false;
			yield BIGINT;
		}
		if (unknown) {
			yield NUMBER;
			yield BIGINT;
		}
	});
}
const UN_OPERATOR_TYPES = createObject({
	"!": resultBool,
	delete: resultBool,
	"+": unaryNumOp,
	"-": unaryNumOp,
	"~": unaryNumOp,
	void: () => "undefined",
	typeof: () => STRING
});
//#endregion
//#region lib/utils/type-tracker/utils.ts
/**
* Find the variable of a given name.
*/
function findVariable(context, node) {
	return findVariable$1(context, node);
}
/**
* Get the property name from a MemberExpression node or a Property node.
*/
function getPropertyName(context, node) {
	return eslintUtils.getPropertyName(node, getScope(context, node));
}
/**
*  Check whether a given node is parenthesized or not.
*/
function isParenthesized(context, node) {
	return eslintUtils.isParenthesized(node, context.sourceCode);
}
//#endregion
//#region lib/utils/type-tracker/tracker.ts
const ts = getTypeScript();
const cacheTypeTracker = /* @__PURE__ */ new WeakMap();
/**
* Create Type tracker
*/
function createTypeTracker(context) {
	const programNode = context.sourceCode.ast;
	const cache = cacheTypeTracker.get(programNode);
	if (cache) return cache;
	const { tsNodeMap, checker, usedTS } = getTypeScriptTools(context);
	const cacheTypeInfo = /* @__PURE__ */ new WeakMap();
	const tracker = {
		isString,
		maybeString,
		isRegExp,
		getTypes
	};
	cacheTypeTracker.set(programNode, tracker);
	return tracker;
	/**
	* Checks if the given node is string.
	*/
	function isString(node) {
		return hasType(getType(node), "String");
	}
	/**
	* Checks if the given node is maybe string.
	*/
	function maybeString(node) {
		if (isString(node)) return true;
		if (usedTS) return false;
		return getType(node) == null;
	}
	/**
	* Checks if the given node is RegExp.
	*/
	function isRegExp(node) {
		return hasType(getType(node), "RegExp");
	}
	/**
	* Get the type names from given node.
	*/
	function getTypes(node) {
		const result = getType(node);
		if (result == null) return [];
		if (typeof result === "string") return [result];
		return result.typeNames();
	}
	/**
	* Get the type name from given node.
	*/
	function getType(node) {
		if (cacheTypeInfo.has(node)) return cacheTypeInfo.get(node) ?? null;
		cacheTypeInfo.set(node, null);
		try {
			const type = getTypeWithoutCache(node);
			cacheTypeInfo.set(node, type);
			return type;
		} catch {
			return null;
		}
	}
	/**
	* Get the type name from given node.
	*/
	function getTypeWithoutCache(node) {
		if (node.type === "Literal") {
			if (typeof node.value === "string") return STRING;
			if (typeof node.value === "boolean") return BOOLEAN;
			if (typeof node.value === "number") return NUMBER;
			if ("regex" in node && node.regex) return REGEXP;
			if ("bigint" in node && node.bigint) return BIGINT;
			if (node.value == null) return "null";
		} else if (node.type === "TemplateLiteral") return STRING;
		if (usedTS) return getTypeByTs(node);
		const jsdoc = getJSDoc(node, context);
		if (jsdoc) {
			if (isParenthesized(context, node)) {
				const type = typeTextToTypeInfo(jsdoc.getTag("type")?.type);
				if (type) return type;
			}
		}
		if (node.type === "ArrowFunctionExpression" || node.type === "FunctionExpression") {
			if (jsdoc) {
				const type = typeTextToTypeInfo(jsdoc.getTag("returns")?.type);
				if (type) return new TypeFunction(() => type);
			}
		}
		if (node.type === "FunctionExpression") return UNKNOWN_FUNCTION;
		if (node.type === "ArrowFunctionExpression") {
			if (node.body.type !== "BlockStatement") {
				const body = node.body;
				return new TypeFunction(() => getType(body));
			}
			return UNKNOWN_FUNCTION;
		}
		if (node.type === "ArrayExpression") return new TypeArray(function* () {
			for (const element of node.elements) if (!element) yield null;
			else if (element.type !== "SpreadElement") yield getType(element);
			else {
				const argType = getType(element.argument);
				if (isTypeClass(argType)) yield argType.iterateType();
				else yield null;
			}
		}, node.elements.every((e) => e && e.type !== "SpreadElement"));
		else if (node.type === "ObjectExpression") return new TypeObject(function* () {
			for (let index = node.properties.length - 1; index >= 0; index--) {
				const property = node.properties[index];
				if (property.type !== "SpreadElement") {
					if (property.value.type === "ObjectPattern" || property.value.type === "ArrayPattern" || property.value.type === "RestElement" || property.value.type === "AssignmentPattern") continue;
					const name = getPropertyName(context, property);
					if (name != null) {
						const value = property.value;
						yield [name, () => getType(value)];
					}
				} else {
					const spreadType = getType(property.argument);
					if (isTypeClass(spreadType) && spreadType.type === "Object") yield* spreadType.allProperties();
				}
			}
		});
		else if (node.type === "BinaryExpression") {
			const type = BI_OPERATOR_TYPES[node.operator];
			if (type) return type(() => [getType(node.left), getType(node.right)]);
		} else if (node.type === "UnaryExpression") {
			const type = UN_OPERATOR_TYPES[node.operator];
			if (type) return type(() => getType(node.argument));
		} else if (node.type === "AssignmentExpression") return getType(node.right);
		else if (node.type === "SequenceExpression") return getType(node.expressions[node.expressions.length - 1]);
		else if (node.type === "ChainExpression") return getType(node.expression);
		else if (node.type === "ClassExpression") return null;
		else if (node.type === "Identifier") {
			const variable = findVariable(context, node);
			if (variable) {
				if (variable.defs.length === 1) {
					const def = variable.defs[0];
					if (def.type === "Variable") {
						const idJsdoc = getJSDoc(def.node, context);
						if (idJsdoc) {
							const type = typeTextToTypeInfo(idJsdoc.getTag("type")?.type);
							if (type) return type;
							const returnType = typeTextToTypeInfo(idJsdoc.getTag("returns")?.type);
							if (returnType) return new TypeFunction(() => returnType);
						}
						if (def.parent.kind === "const") if (def.node.init) {
							const type = getType(def.node.init);
							if (type) return type;
						} else {
							const parent = getParent(def.parent);
							if (parent) {
								if (parent?.type === "ForOfStatement") {
									const rightType = getType(parent.right);
									if (isTypeClass(rightType)) {
										const type = rightType.iterateType();
										if (type) return type;
									}
								} else if (parent?.type === "ForInStatement") return STRING;
							}
						}
					} else if (def.type === "Parameter") {
						const fnJsdoc = getJSDoc(def.node, context);
						if (fnJsdoc) {
							const jsdocParams = fnJsdoc.parseParams();
							if (!jsdocParams.isEmpty()) {
								const type = typeTextToTypeInfo(jsdocParams.get(getParamPath(def.name.name, def.name, context))?.type);
								if (type) return type;
							}
						}
						const parent = getParent(def.name);
						if (parent) {
							if (parent.type === "RestElement") {
								const pp = getParent(parent);
								if (pp) {
									if (pp.type === "ArrayPattern") return UNKNOWN_ARRAY;
									if (pp.type === "ObjectPattern") return UNKNOWN_OBJECT;
									if (pp.type === "FunctionExpression" || pp.type === "FunctionDeclaration" || pp.type === "ArrowFunctionExpression") return UNKNOWN_ARRAY;
								}
							} else if (parent.type === "AssignmentPattern") return getType(parent.right);
						}
					} else if (def.type === "FunctionName") {
						const fnJsdoc = getJSDoc(def.node, context);
						if (fnJsdoc) {
							const type = typeTextToTypeInfo(fnJsdoc.getTag("returns")?.type);
							if (type) return new TypeFunction(() => type);
						}
						return UNKNOWN_FUNCTION;
					}
				} else if (variable.defs.length === 0) {
					const type = GLOBAL.propertyType(node.name);
					if (type) return type;
				}
			}
		} else if (node.type === "NewExpression") {
			if (node.callee.type !== "Super") {
				const type = getType(node.callee);
				if (isTypeClass(type)) {
					const argTypes = [];
					for (const arg of node.arguments) argTypes.push(arg.type === "SpreadElement" ? null : () => {
						return getType(arg);
					});
					return type.returnType(null, argTypes, { isConstructor: true });
				}
			}
		} else if (node.type === "CallExpression" || node.type === "TaggedTemplateExpression") {
			const argTypes = [];
			if (node.type === "CallExpression") for (const arg of node.arguments) argTypes.push(arg.type === "SpreadElement" ? null : () => {
				return getType(arg);
			});
			const callee = node.type === "CallExpression" ? node.callee : node.tag;
			if (callee.type === "MemberExpression") {
				const mem = callee;
				if (mem.object.type !== "Super") {
					let propertyName = null;
					if (!mem.computed) {
						if (mem.property.type === "Identifier") propertyName = mem.property.name;
					} else if (hasType(getType(mem.property), "Number")) propertyName = "0";
					if (propertyName != null) {
						if (propertyName === "toString" || propertyName === "toLocaleString") return STRING;
						const objectType = getType(mem.object);
						if (isTypeClass(objectType)) {
							const type = objectType.propertyType(propertyName);
							if (isTypeClass(type)) return type.returnType(() => objectType, argTypes);
						}
					}
				}
			} else if (callee.type !== "Super") {
				const type = getType(callee);
				if (isTypeClass(type)) return type.returnType(null, argTypes);
			}
		} else if (node.type === "MemberExpression") {
			if (node.object.type !== "Super") {
				let propertyName = null;
				if (!node.computed) {
					if (node.property.type === "Identifier") propertyName = node.property.name;
				} else if (hasType(getType(node.property), "Number")) propertyName = "0";
				if (propertyName != null) {
					const objectType = getType(node.object);
					if (isTypeClass(objectType)) {
						const type = objectType.propertyType(propertyName);
						if (type) return type;
					}
				}
			}
		}
		return usedTS ? getTypeByTs(node) : null;
	}
	/**
	* Get type from given node by ts types.
	*/
	function getTypeByTs(node) {
		const tsNode = tsNodeMap.get(node);
		const tsType = tsNode && checker?.getTypeAtLocation(tsNode) || null;
		return tsType && getTypeFromTsType(tsType);
	}
	/**
	* Check if the name of the given type is expected or not.
	*/
	function getTypeFromTsType(tsType) {
		if (isStringLine(tsType)) return STRING;
		if (isNumberLike(tsType)) return NUMBER;
		if (isBooleanLike(tsType)) return BOOLEAN;
		if (isBigIntLike(tsType)) return BIGINT;
		if (isAny(tsType) || isUnknown(tsType)) return null;
		if (isArrayLikeObject(tsType)) return UNKNOWN_ARRAY;
		if (isReferenceObject(tsType) && tsType.target !== tsType) return getTypeFromTsType(tsType.target);
		if (isTypeParameter(tsType)) {
			const constraintType = getConstraintType(tsType);
			if (constraintType) return getTypeFromTsType(constraintType);
			return null;
		}
		if (isUnionOrIntersection(tsType)) return TypeUnionOrIntersection.buildType(function* () {
			for (const t of tsType.types) {
				const tn = getTypeFromTsType(t);
				if (tn) yield tn;
			}
		});
		if (isClassOrInterface(tsType)) {
			const name = tsType.symbol.escapedName;
			const typeName = /^Readonly(?<typeName>.*)/u.exec(name)?.groups.typeName ?? name;
			return typeName === "Array" ? UNKNOWN_ARRAY : typeName;
		}
		if (isObject(tsType)) return UNKNOWN_OBJECT;
		return checker ? checker.typeToString(tsType) : null;
	}
	/**
	* Get the constraint type of a given type parameter type if exists.
	*/
	function getConstraintType(tsType) {
		const symbol = tsType.symbol;
		const declarations = symbol && symbol.declarations;
		const declaration = declarations && declarations[0];
		if (declaration && ts.isTypeParameterDeclaration(declaration) && declaration.constraint != null) return checker?.getTypeFromTypeNode(declaration.constraint);
	}
}
/** Get type from jsdoc type text */
function typeTextToTypeInfo(typeText) {
	if (typeText == null) return null;
	return jsDocTypeNodeToTypeInfo(parseTypeText(typeText));
}
/** Get type from jsdoc-type-pratt-parser's RootResult */
function jsDocTypeNodeToTypeInfo(node) {
	if (node == null) return null;
	if (node.type === "JsdocTypeName") return typeNameToTypeInfo(node.value);
	if (node.type === "JsdocTypeStringValue") return STRING;
	if (node.type === "JsdocTypeNumber") return NUMBER;
	if (node.type === "JsdocTypeAsserts") return BOOLEAN;
	if (node.type === "JsdocTypeOptional" || node.type === "JsdocTypeNullable" || node.type === "JsdocTypeNotNullable" || node.type === "JsdocTypeParenthesis") return jsDocTypeNodeToTypeInfo(node.element);
	if (node.type === "JsdocTypeVariadic") return new TypeArray(function* () {
		if (node.element) yield jsDocTypeNodeToTypeInfo(node.element);
		else yield null;
	});
	if (node.type === "JsdocTypeUnion" || node.type === "JsdocTypeIntersection") return TypeUnionOrIntersection.buildType(function* () {
		for (const e of node.elements) yield jsDocTypeNodeToTypeInfo(e);
	});
	if (node.type === "JsdocTypeGeneric") {
		const subject = jsDocTypeNodeToTypeInfo(node.left);
		if (hasType(subject, "Array")) return new TypeArray(function* () {
			yield jsDocTypeNodeToTypeInfo(node.elements[0]);
		});
		if (hasType(subject, "Map")) return new TypeMap(() => jsDocTypeNodeToTypeInfo(node.elements[0]), () => jsDocTypeNodeToTypeInfo(node.elements[1]));
		if (hasType(subject, "Set")) return new TypeSet(() => jsDocTypeNodeToTypeInfo(node.elements[0]));
		if (subject === UNKNOWN_ITERABLE) return new TypeIterable(() => jsDocTypeNodeToTypeInfo(node.elements[0]));
		return subject;
	}
	if (node.type === "JsdocTypeObject") return new TypeObject(function* () {
		for (const element of node.elements) if (element.type === "JsdocTypeObjectField") {
			if (typeof element.key !== "string") continue;
			yield [element.key, () => element.right ? jsDocTypeNodeToTypeInfo(element.right) : null];
		} else if (element.type === "JsdocTypeJsdocObjectField") {
			if (element.left.type === "JsdocTypeNullable" && element.left.element.type === "JsdocTypeName") yield [element.left.element.value, () => element.right ? jsDocTypeNodeToTypeInfo(element.right) : null];
		}
	});
	if (node.type === "JsdocTypeTuple") {
		if (node.elements[0].type === "JsdocTypeKeyValue") {
			const elements = node.elements;
			return new TypeArray(function* () {
				for (const element of elements) if (element.right) yield jsDocTypeNodeToTypeInfo(element.right);
			});
		}
		const elements = node.elements;
		return new TypeArray(function* () {
			for (const element of elements) yield jsDocTypeNodeToTypeInfo(element);
		});
	}
	if (node.type === "JsdocTypeFunction") {
		if (node.returnType) {
			const returnType = node.returnType;
			return new TypeFunction(() => jsDocTypeNodeToTypeInfo(returnType));
		}
		return UNKNOWN_FUNCTION;
	}
	if (node.type === "JsdocTypeTypeof") return new TypeFunction(() => jsDocTypeNodeToTypeInfo(node.element));
	if (node.type === "JsdocTypeReadonlyArray") return jsDocTypeNodeToTypeInfo(node.element);
	if (node.type === "JsdocTypeConditional") {
		const trueType = jsDocTypeNodeToTypeInfo(node.trueType);
		const falseType = jsDocTypeNodeToTypeInfo(node.falseType);
		if (trueType && falseType) return TypeUnionOrIntersection.buildType(function* () {
			yield trueType;
			yield falseType;
		});
		return trueType ?? falseType;
	}
	if (node.type === "JsdocTypeTemplateLiteral") return STRING;
	if (node.type === "JsdocTypeAny" || node.type === "JsdocTypeUnknown" || node.type === "JsdocTypeNull" || node.type === "JsdocTypeUndefined") return null;
	if (node.type === "JsdocTypeImport" || node.type === "JsdocTypeKeyof" || node.type === "JsdocTypeNamePath" || node.type === "JsdocTypePredicate" || node.type === "JsdocTypeSpecialNamePath" || node.type === "JsdocTypeSymbol" || node.type === "JsdocTypeAssertsPlain" || node.type === "JsdocTypeInfer") return null;
	throw assertNever(node);
}
/** Get type from type name */
function typeNameToTypeInfo(name) {
	if (name === "String" || name === "string") return STRING;
	if (name === "Number" || name === "number") return NUMBER;
	if (name === "Boolean" || name === "boolean") return BOOLEAN;
	if (name === "BigInt" || name === "bigint") return BIGINT;
	if (name === "RegExp") return REGEXP;
	if (name === "Array" || name === "array") return UNKNOWN_ARRAY;
	if (name === "Function" || name === "function") return UNKNOWN_FUNCTION;
	if (name === "Object" || name === "object") return UNKNOWN_OBJECT;
	if (name === "Record") return UNKNOWN_OBJECT;
	if (name === "Map") return UNKNOWN_MAP;
	if (name === "Set") return UNKNOWN_SET;
	if (name === "Generator" || name === "Iterable" || name === "IterableIterator") return UNKNOWN_ITERABLE;
	return null;
}
/**
* Get function param path for param node
*/
function getParamPath(name, node, context) {
	const parent = getParent(node);
	if (!parent) return [{
		name,
		index: null
	}];
	if (parent.type === "FunctionDeclaration" || parent.type === "ArrowFunctionExpression" || parent.type === "FunctionExpression") return [{
		name,
		index: parent.params.indexOf(node)
	}];
	if (parent.type === "AssignmentPattern") return getParamPath(name, parent, context);
	if (parent.type === "ArrayPattern") {
		const path = {
			name,
			index: parent.elements.indexOf(node)
		};
		return getParamPath(null, parent, context).concat([path]);
	}
	if (parent.type === "Property") {
		const object = getParent(parent);
		const path = {
			name: getPropertyName(context, parent),
			index: object.properties.indexOf(parent)
		};
		return getParamPath(null, object, context).concat([path]);
	}
	if (parent.type === "RestElement") return getParamPath(name, parent, context);
	return [{
		name,
		index: null
	}];
}
//#endregion
//#region lib/utils/unicode.ts
const CP_SPACE = " ".codePointAt(0);
const CP_BAN = "!".codePointAt(0);
"#".codePointAt(0);
const CP_DOLLAR = "$".codePointAt(0);
"%".codePointAt(0);
"&".codePointAt(0);
const CP_OPENING_PAREN = "(".codePointAt(0);
const CP_CLOSING_PAREN = ")".codePointAt(0);
const CP_STAR = "*".codePointAt(0);
const CP_PLUS = "+".codePointAt(0);
",".codePointAt(0);
const CP_MINUS = "-".codePointAt(0);
const CP_DOT = ".".codePointAt(0);
const CP_SLASH = "/".codePointAt(0);
const CP_COLON = ":".codePointAt(0);
";".codePointAt(0);
"<".codePointAt(0);
"=".codePointAt(0);
">".codePointAt(0);
const CP_QUESTION = "?".codePointAt(0);
const CP_AT = "@".codePointAt(0);
const CP_OPENING_BRACKET = "[".codePointAt(0);
const CP_BACK_SLASH = "\\".codePointAt(0);
const CP_CLOSING_BRACKET = "]".codePointAt(0);
const CP_CARET = "^".codePointAt(0);
const CP_BACKTICK = "`".codePointAt(0);
const CP_APOSTROPHE = "'".codePointAt(0);
const CP_OPENING_BRACE = "{".codePointAt(0);
const CP_PIPE = "|".codePointAt(0);
const CP_CLOSING_BRACE = "}".codePointAt(0);
const CP_TILDE = "~".codePointAt(0);
const CP_NEL = "".codePointAt(0);
"\xA0".codePointAt(0);
" ".codePointAt(0);
const CP_MONGOLIAN_VOWEL_SEPARATOR = "᠎".codePointAt(0);
" ".codePointAt(0);
" ".codePointAt(0);
const CP_ZWSP = "​".codePointAt(0);
const CP_ZWNJ = "‌".codePointAt(0);
const CP_ZWJ = "‍".codePointAt(0);
const CP_LRM = "‎".codePointAt(0);
const CP_RLM = "‏".codePointAt(0);
"\u2028".codePointAt(0);
"\u2029".codePointAt(0);
" ".codePointAt(0);
" ".codePointAt(0);
const CP_BRAILLE_PATTERN_BLANK = "⠀".codePointAt(0);
"　".codePointAt(0);
"﻿".codePointAt(0);
const CP_DIGIT_ZERO = "0".codePointAt(0);
const CP_DIGIT_NINE = "9".codePointAt(0);
const CP_SMALL_A = "a".codePointAt(0);
const CP_SMALL_Z = "z".codePointAt(0);
const CP_CAPITAL_A = "A".codePointAt(0);
const CP_CAPITAL_Z = "Z".codePointAt(0);
const CP_LOW_LINE = "_".codePointAt(0);
const CP_RANGE_SMALL_LETTER = [CP_SMALL_A, CP_SMALL_Z];
const CP_RANGE_CAPITAL_LETTER = [CP_CAPITAL_A, CP_CAPITAL_Z];
/**
* Checks if the given code point is within the code point range.
* @param codePoint The code point to check.
* @param range The range of code points of the range.
* @returns `true` if the given character is within the character class range.
*/
function isCodePointInRange(codePoint, [start, end]) {
	return start <= codePoint && codePoint <= end;
}
/**
* Checks if the given code point is digit.
*/
function isDigit(codePoint) {
	return Chars.digit({}).has(codePoint);
}
/**
* Checks if the given code point is lowercase.
*/
function isLowercaseLetter(codePoint) {
	return isCodePointInRange(codePoint, CP_RANGE_SMALL_LETTER);
}
/**
* Checks if the given code point is uppercase.
*/
function isUppercaseLetter(codePoint) {
	return isCodePointInRange(codePoint, CP_RANGE_CAPITAL_LETTER);
}
/**
* Checks if the given code point is letter.
*/
function isLetter(codePoint) {
	return isLowercaseLetter(codePoint) || isUppercaseLetter(codePoint);
}
/**
* Checks if the given code point is symbol.
*/
function isSymbol(codePoint) {
	return isCodePointInRange(codePoint, [CP_BAN, CP_SLASH]) || isCodePointInRange(codePoint, [CP_COLON, CP_AT]) || isCodePointInRange(codePoint, [CP_OPENING_BRACKET, CP_BACKTICK]) || isCodePointInRange(codePoint, [CP_OPENING_BRACE, CP_TILDE]);
}
/**
* Checks if the given code point is space.
*/
function isSpace(codePoint) {
	return Chars.space({}).has(codePoint);
}
/**
* Checks if the given code point is invisible character.
*/
function isInvisible(codePoint) {
	if (isSpace(codePoint)) return true;
	return codePoint === CP_MONGOLIAN_VOWEL_SEPARATOR || codePoint === CP_NEL || codePoint === CP_ZWSP || codePoint === CP_ZWNJ || codePoint === CP_ZWJ || codePoint === CP_LRM || codePoint === CP_RLM || codePoint === CP_BRAILLE_PATTERN_BLANK;
}
//#endregion
//#region lib/utils/index.ts
const regexpRules = /* @__PURE__ */ new WeakMap();
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
				url: `https://ota-meshi.github.io/eslint-plugin-regexp/rules/${ruleName}.html`,
				ruleId: `regexp/${ruleName}`,
				ruleName
			}
		},
		create: rule.create
	};
}
/**
* Define the RegExp visitor rule.
*/
function defineRegexpVisitor(context, rule) {
	const programNode = context.sourceCode.ast;
	let visitor;
	let rules = regexpRules.get(programNode);
	if (!rules) {
		rules = [];
		regexpRules.set(programNode, rules);
		visitor = buildRegexpVisitor(context, rules, () => {
			regexpRules.delete(programNode);
		});
	} else visitor = {};
	let createLiteralVisitor;
	let createSourceVisitor;
	if ("createVisitor" in rule) {
		createLiteralVisitor = rule.createVisitor;
		createSourceVisitor = rule.createVisitor;
	} else {
		createLiteralVisitor = rule.createLiteralVisitor;
		createSourceVisitor = rule.createSourceVisitor;
	}
	rules.push({
		createLiteralVisitor,
		createSourceVisitor,
		visitInvalid: rule.visitInvalid,
		visitUnknown: rule.visitUnknown
	});
	return visitor;
}
function buildRegexpVisitor(context, rules, programExit) {
	const parser = new RegExpParser();
	/**
	* Verify a given regular expression.
	* @param patternNode The regular expression pattern to verify.
	* @param flags The flags of the regular expression.
	*/
	function verify(patternNode, flagsNode, regexpNode, patternSource, flagsString, ownsFlags, createVisitor) {
		const flags = parseFlags(flagsString || "");
		if (!patternSource) {
			visitUnknownForRules(rules, {
				pattern: null,
				patternSource: null,
				...buildUnparsableRegExpContextBase({
					patternSource,
					patternNode,
					regexpNode,
					context,
					flags,
					flagsString,
					flagsNode,
					ownsFlags
				})
			});
			return;
		}
		let parsedPattern;
		try {
			parsedPattern = parser.parsePattern(patternSource.value, 0, patternSource.value.length, flags);
		} catch (error) {
			if (error instanceof SyntaxError) visitInvalidForRules(rules, {
				pattern: patternSource.value,
				patternSource,
				error,
				...buildUnparsableRegExpContextBase({
					patternSource,
					patternNode,
					regexpNode,
					context,
					flags,
					flagsString,
					flagsNode,
					ownsFlags
				})
			});
			return;
		}
		const helpers = buildRegExpContextBase({
			patternSource,
			regexpNode,
			flagsNode,
			context,
			flags,
			parsedPattern
		});
		visitRegExpAST(parsedPattern, createVisitor(helpers));
	}
	const ownedRegExpLiterals = /* @__PURE__ */ new Set();
	return {
		"Program:exit": programExit,
		Literal(node) {
			if (!isRegexpLiteral(node) || ownedRegExpLiterals.has(node)) return;
			const flagsString = node.regex.flags;
			verify(node, node, node, PatternSource.fromRegExpLiteral(context, node), flagsString, true, (base) => {
				return createLiteralVisitorFromRules(rules, {
					node,
					flagsString,
					ownsFlags: true,
					regexpNode: node,
					...base
				});
			});
		},
		Program(program) {
			const tracker = new ReferenceTracker(context.sourceCode.getScope(program));
			const regexpDataList = [];
			for (const { node } of tracker.iterateGlobalReferences({ RegExp: {
				[CALL]: true,
				[CONSTRUCT]: true
			} })) {
				const newOrCall = node;
				const [patternArg, flagsArg] = newOrCall.arguments;
				if (!patternArg || patternArg.type === "SpreadElement") continue;
				const patternSource = PatternSource.fromExpression(context, patternArg);
				patternSource?.getOwnedRegExpLiterals().forEach((n) => ownedRegExpLiterals.add(n));
				let flagsNode = null;
				let flagsString = null;
				let ownsFlags = false;
				if (flagsArg) {
					if (flagsArg.type !== "SpreadElement") {
						flagsNode = dereferenceOwnedVariable(context, flagsArg);
						flagsString = getStringIfConstant(context, flagsNode);
						ownsFlags = isStringLiteral(flagsNode);
					}
				} else if (patternSource && patternSource.regexpValue) {
					flagsString = patternSource.regexpValue.flags;
					ownsFlags = Boolean(patternSource.regexpValue.ownedNode);
					flagsNode = patternSource.regexpValue.ownedNode;
				} else {
					flagsString = "";
					ownsFlags = true;
				}
				regexpDataList.push({
					call: newOrCall,
					patternNode: patternArg,
					patternSource,
					flagsNode,
					flagsString,
					ownsFlags
				});
			}
			for (const { call, patternNode, patternSource, flagsNode, flagsString, ownsFlags } of regexpDataList) verify(patternNode, flagsNode, call, patternSource, flagsString, ownsFlags, (base) => {
				return createSourceVisitorFromRules(rules, {
					node: patternNode,
					flagsString,
					ownsFlags,
					regexpNode: call,
					...base
				});
			});
		}
	};
}
/** Create a visitor handler from the given rules */
function createLiteralVisitorFromRules(rules, context) {
	const handlers = [];
	for (const rule of rules) if (rule.createLiteralVisitor) handlers.push(rule.createLiteralVisitor(context));
	return composeRegExpVisitors(handlers);
}
/** Create a visitor handler from the given rules */
function createSourceVisitorFromRules(rules, context) {
	const handlers = [];
	for (const rule of rules) if (rule.createSourceVisitor) handlers.push(rule.createSourceVisitor(context));
	return composeRegExpVisitors(handlers);
}
/** Calls a visit function for all the given rules */
function visitInvalidForRules(rules, context) {
	for (const rule of rules) rule.visitInvalid?.(context);
}
/** Calls a visit function for all the given rules */
function visitUnknownForRules(rules, context) {
	for (const rule of rules) rule.visitUnknown?.(context);
}
/** Returns a single visitor handler that executes all the given handlers. */
function composeRegExpVisitors(handlers) {
	const handler = {};
	for (const visitor of handlers) {
		const entries = Object.entries(visitor);
		for (const [key, fn] of entries) {
			const orig = handler[key];
			if (orig) handler[key] = (node) => {
				orig(node);
				fn(node);
			};
			else handler[key] = fn;
		}
	}
	return handler;
}
/**
* Composite all given visitors.
*/
function compositingVisitors(visitor, ...visitors) {
	for (const v of visitors) for (const key in v) {
		const orig = visitor[key];
		if (orig) visitor[key] = (...args) => {
			orig(...args);
			v[key](...args);
		};
		else visitor[key] = v[key];
	}
	return visitor;
}
/**
* Build RegExpContextBase
*/
function buildRegExpContextBase({ patternSource, regexpNode, flagsNode, context, flags, parsedPattern }) {
	const sourceCode = context.sourceCode;
	let cacheUsageOfPattern = null;
	const cacheCapturingGroupReferenceMap = /* @__PURE__ */ new Map();
	const getAllCapturingGroups = lazy(() => extractCaptures(parsedPattern).groups);
	return {
		getRegexpLocation: (range, offsets) => {
			if (offsets) return patternSource.getAstLocation({
				start: range.start + offsets[0],
				end: range.start + offsets[1]
			});
			return patternSource.getAstLocation(range);
		},
		getFlagsLocation: () => getFlagsLocation(sourceCode, regexpNode, flagsNode),
		getFlagLocation: (flag) => getFlagLocation(sourceCode, regexpNode, flagsNode, flag),
		fixReplaceNode: (node, replacement) => {
			return fixReplaceNode(patternSource, node, replacement);
		},
		fixReplaceQuant: (qNode, replacement) => {
			return fixReplaceQuant(patternSource, qNode, replacement);
		},
		fixReplaceFlags: (newFlags, includePattern) => {
			return fixReplaceFlags(patternSource, regexpNode, flagsNode, newFlags, includePattern ?? true);
		},
		getUsageOfPattern: () => cacheUsageOfPattern ??= getUsageOfPattern(regexpNode, context),
		getCapturingGroupReferences: (options) => {
			const strictTypes = Boolean(options?.strictTypes ?? true);
			const cacheCapturingGroupReference = cacheCapturingGroupReferenceMap.get(strictTypes);
			if (cacheCapturingGroupReference) return cacheCapturingGroupReference;
			const countOfCapturingGroup = getAllCapturingGroups().length;
			const capturingGroupReferences = [...extractCapturingGroupReferences(regexpNode, flags, createTypeTracker(context), countOfCapturingGroup, context, { strictTypes })];
			cacheCapturingGroupReferenceMap.set(strictTypes, capturingGroupReferences);
			return capturingGroupReferences;
		},
		getAllCapturingGroups,
		pattern: parsedPattern.raw,
		patternAst: parsedPattern,
		patternSource,
		flags: toCache(flags)
	};
}
/**
* Build UnparsableRegExpContextBase
*/
function buildUnparsableRegExpContextBase({ patternSource, patternNode, regexpNode, context, flags: originalFlags, flagsString, flagsNode, ownsFlags }) {
	const sourceCode = context.sourceCode;
	return {
		regexpNode,
		node: patternNode,
		flags: toCache(originalFlags),
		flagsString,
		ownsFlags,
		getFlagsLocation: () => getFlagsLocation(sourceCode, regexpNode, flagsNode),
		getFlagLocation: (flag) => getFlagLocation(sourceCode, regexpNode, flagsNode, flag),
		fixReplaceFlags: (newFlags, includePattern) => {
			return fixReplaceFlags(patternSource, regexpNode, flagsNode, newFlags, includePattern ?? true);
		}
	};
}
/**
* Creates a new fix that replaces the given node with a given string.
*
* The string will automatically be escaped if necessary.
*/
function fixReplaceNode(patternSource, regexpNode, replacement) {
	return (fixer) => {
		const range = patternSource.getReplaceRange(regexpNode);
		if (range == null) return null;
		let text;
		if (typeof replacement === "string") text = replacement;
		else {
			text = replacement();
			if (text == null) return null;
		}
		return range.replace(fixer, text);
	};
}
/**
* Creates a new fix that replaces the given quantifier (but not the quantified
* element) with a given string.
*
* This will not change the greediness of the quantifier.
*/
function fixReplaceQuant(patternSource, quantifier, replacement) {
	return (fixer) => {
		let text;
		if (typeof replacement !== "function") text = replacement;
		else {
			text = replacement();
			if (text == null) return null;
		}
		const offset = getQuantifierOffsets(quantifier);
		if (typeof text !== "string") {
			if (text.greedy !== void 0 && text.greedy !== quantifier.greedy) offset[1] += 1;
			text = quantToString(text);
		}
		const range = patternSource.getReplaceRange({
			start: quantifier.start + offset[0],
			end: quantifier.start + offset[1]
		});
		if (range == null) return null;
		return range.replace(fixer, text);
	};
}
/**
* Returns a new fixer that replaces the current flags with the given flags.
*
* @param includePattern Whether the whole pattern is to be included in the fix.
*
* Fixes that change the pattern generally assume that the flags don't change,
* so changing the flags should conflict with all pattern fixes.
*/
function fixReplaceFlags(patternSource, regexpNode, flagsNode, replacement, includePattern) {
	return (fixer) => {
		let newFlags;
		if (typeof replacement === "string") newFlags = replacement;
		else {
			newFlags = replacement();
			if (newFlags == null) return null;
		}
		if (!/^[a-z]*$/iu.test(newFlags)) return null;
		if (includePattern && isRegexpLiteral(regexpNode)) return fixer.replaceText(regexpNode, `/${regexpNode.regex.pattern}/${newFlags}`);
		let flagsFix;
		if (isRegexpLiteral(regexpNode)) flagsFix = fixer.replaceTextRange(getFlagsRange(regexpNode), newFlags);
		else if (flagsNode) {
			const range = getFlagsRange(flagsNode);
			if (range == null) return null;
			flagsFix = fixer.replaceTextRange(range, newFlags);
		} else {
			if (regexpNode.arguments.length !== 1) return null;
			const end = regexpNode.range[1];
			flagsFix = fixer.replaceTextRange([end - 1, end], `, "${newFlags}")`);
		}
		if (!includePattern) return flagsFix;
		if (!patternSource) return null;
		const patternRange = patternSource.getReplaceRange({
			start: 0,
			end: patternSource.value.length
		});
		if (patternRange == null) return null;
		return [patternRange.replace(fixer, patternSource.value), flagsFix];
	};
}
/**
* Returns whether the concatenation of the two string might create new escape
* sequences or elements.
*/
function mightCreateNewElement(before, after) {
	if (before.endsWith("\\c") && /^[a-z]/iu.test(after)) return true;
	if (/(?:^|[^\\])(?:\\{2})*\\(?:x[\dA-Fa-f]?|u[\dA-Fa-f]{0,3})$/u.test(before) && /^[\da-f]/iu.test(after)) return true;
	if (/(?:^|[^\\])(?:\\{2})*\\u$/u.test(before) && /^\{[\da-f]*(?:\}[\s\S]*)?$/iu.test(after) || /(?:^|[^\\])(?:\\{2})*\\u\{[\da-f]*$/u.test(before) && /^(?:[\da-f]+\}?|\})/iu.test(after)) return true;
	if (/(?:^|[^\\])(?:\\{2})*\\0[0-7]?$/u.test(before) && /^[0-7]/u.test(after) || /(?:^|[^\\])(?:\\{2})*\\[1-7]$/u.test(before) && /^[0-7]/u.test(after)) return true;
	if (/(?:^|[^\\])(?:\\{2})*\\[1-9]\d*$/u.test(before) && /^\d/u.test(after) || /(?:^|[^\\])(?:\\{2})*\\k$/u.test(before) && after[0] === "<" || /(?:^|[^\\])(?:\\{2})*\\k<[^<>]*$/u.test(before)) return true;
	if (/(?:^|[^\\])(?:\\{2})*\\p$/iu.test(before) && /^\{[\w=]*(?:\}[\s\S]*)?$/u.test(after) || /(?:^|[^\\])(?:\\{2})*\\p\{[\w=]*$/iu.test(before) && /^[\w=]+(?:\}[\s\S]*)?$|^\}/u.test(after)) return true;
	if (/(?:^|[^\\])(?:\\{2})*\{\d*$/u.test(before) && /^[\d,}]/u.test(after) || /(?:^|[^\\])(?:\\{2})*\{\d+,$/u.test(before) && /^(?:\d+(?:\}|$)|\})/u.test(after) || /(?:^|[^\\])(?:\\{2})*\{\d+,\d*$/u.test(before) && after[0] === "}") return true;
	return false;
}
/**
* Removes the given character class element from its character class.
*
* If the given element is not a direct element of a character class, an error
* will be thrown.
*/
function fixRemoveCharacterClassElement(context, element) {
	const cc = element.parent;
	if (cc.type !== "CharacterClass") throw new Error("Only call this function for character class elements.");
	return context.fixReplaceNode(element, () => {
		const textBefore = cc.raw.slice(0, element.start - cc.start);
		const textAfter = cc.raw.slice(element.end - cc.start);
		if (mightCreateNewElement(textBefore, textAfter)) return null;
		const elementIndex = cc.elements.indexOf(element);
		const elementBefore = cc.elements[elementIndex - 1];
		const elementAfter = cc.elements[elementIndex + 1];
		if (elementBefore && elementAfter && elementBefore.type === "Character" && elementBefore.raw === "-" && elementAfter.type === "Character") return null;
		if (textAfter[0] === "-" && elementBefore && elementBefore.type === "Character" || textAfter[0] === "^" && !cc.negate && !elementBefore) return "\\";
		return "";
	});
}
/**
* Removes the given alternative from its parent.
*/
function fixRemoveAlternative(context, alternative) {
	const { parent } = alternative;
	if (parent.alternatives.length === 1) return context.fixReplaceNode(alternative, "[]");
	return context.fixReplaceNode(parent, () => {
		let { start, end } = alternative;
		if (parent.alternatives[0] === alternative) end++;
		else start--;
		return parent.raw.slice(0, start - parent.start) + parent.raw.slice(end - parent.start);
	});
}
function fixRemoveStringAlternative(context, alternative) {
	const { parent } = alternative;
	if (parent.alternatives.length === 1) return context.fixReplaceNode(parent, "[]");
	return context.fixReplaceNode(parent, () => {
		let { start, end } = alternative;
		if (parent.alternatives[0] === alternative) end++;
		else start--;
		return parent.raw.slice(0, start - parent.start) + parent.raw.slice(end - parent.start);
	});
}
/**
* Check the siblings to see if the regex doesn't change when unwrapped.
*/
function canUnwrapped(node, text) {
	let textBefore, textAfter;
	const parent = node.parent;
	if (parent.type === "Alternative") {
		textBefore = parent.raw.slice(0, node.start - parent.start);
		textAfter = parent.raw.slice(node.end - parent.start);
	} else if (parent.type === "Quantifier") {
		const alt = parent.parent;
		textBefore = alt.raw.slice(0, node.start - alt.start);
		textAfter = alt.raw.slice(node.end - alt.start);
	} else return true;
	return !mightCreateNewElement(textBefore, text) && !mightCreateNewElement(text, textAfter);
}
//#endregion
//#region lib/rules/confusing-quantifier.ts
var confusing_quantifier_default = createRule("confusing-quantifier", {
	meta: {
		docs: {
			description: "disallow confusing quantifiers",
			category: "Best Practices",
			recommended: true,
			default: "warn"
		},
		schema: [],
		messages: { confusing: "This quantifier is confusing because its minimum is {{min}} but it can match the empty string. Maybe replace it with `{{proposal}}` to reflect that it can match the empty string?" },
		type: "problem"
	},
	create(context) {
		function createVisitor({ node, flags, getRegexpLocation }) {
			return { onQuantifierEnter(qNode) {
				if (qNode.min > 0 && isPotentiallyEmpty(qNode.element, flags)) {
					const proposal = quantToString({
						...qNode,
						min: 0
					});
					context.report({
						node,
						loc: getRegexpLocation(qNode, getQuantifierOffsets(qNode)),
						messageId: "confusing",
						data: {
							min: String(qNode.min),
							proposal
						}
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/utils/mention.ts
/** Formats the given Unicode code point as `U+0000`. */
function formatCodePoint(value) {
	return `U+${value.toString(16).padStart(4, "0")}`;
}
/**
* Creates a string that mentions the given character class element.
*
* This is a specialized version of {@link mention} that will add
* character-related information if possible.
*/
function mentionChar(element) {
	if (element.type === "Character") {
		const value = formatCodePoint(element.value);
		return `'${escape(element.raw)}' (${value})`;
	}
	if (element.type === "CharacterClassRange") {
		const min = formatCodePoint(element.min.value);
		const max = formatCodePoint(element.max.value);
		return `'${escape(element.raw)}' (${min} - ${max})`;
	}
	return mention(element);
}
/**
* Creates a string that mentions the given character class element.
*/
function mention(element) {
	return `'${escape(typeof element === "string" ? element : element.raw)}'`;
}
/** Escape control characters in the given string */
function escape(value) {
	return value.replace(/\\(?<char>[\s\S])/gu, (m, char) => {
		if (char.charCodeAt(0) < 32) return escapeControl(char);
		return m;
	}).replace(/[\0-\x1f]/gu, escapeControl);
}
/**
* Assuming that the given character is a control character, this function will
* return an escape sequence for that character.
*/
function escapeControl(control) {
	if (control === "	") return control;
	if (control === "\n") return "\\n";
	if (control === "\r") return "\\r";
	return `\\x${control.charCodeAt(0).toString(16).padStart(2, "0")}`;
}
/**
* Joins the given list of strings as an English list.
*/
function joinEnglishList(list) {
	if (list.length === 0) return "none";
	if (list.length === 1) return list[0];
	if (list.length === 2) return `${list[0]} and ${list[1]}`;
	let result = list[0];
	for (let i = 1; i < list.length - 1; i++) result += `, ${list[i]}`;
	result += `, and ${list[list.length - 1]}`;
	return result;
}
//#endregion
//#region lib/rules/control-character-escape.ts
const CONTROL_CHARS$1 = new Map([
	[0, "\\0"],
	[9, "\\t"],
	[10, "\\n"],
	[11, "\\v"],
	[12, "\\f"],
	[13, "\\r"]
]);
/**
* Returns whether the regex is represented by a RegExp literal in source code
* at the given range.
*/
function isRegExpLiteralAt({ node, patternSource }, at) {
	if (isRegexpLiteral(node)) return true;
	const replaceRange = patternSource.getReplaceRange(at);
	if (replaceRange && replaceRange.type === "RegExp") return true;
	return false;
}
var control_character_escape_default = createRule("control-character-escape", {
	meta: {
		docs: {
			description: "enforce consistent escaping of control characters",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { unexpected: "Unexpected control character escape {{actual}}. Use '{{expected}}' instead." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, getRegexpLocation, fixReplaceNode } = regexpContext;
			return { onCharacterEnter(cNode) {
				if (cNode.parent.type === "CharacterClassRange") return;
				const expectedRaw = CONTROL_CHARS$1.get(cNode.value);
				if (expectedRaw === void 0) return;
				if (cNode.raw === expectedRaw) return;
				if (!isRegExpLiteralAt(regexpContext, cNode) && cNode.raw === String.fromCodePoint(cNode.value)) return;
				context.report({
					node,
					loc: getRegexpLocation(cNode),
					messageId: "unexpected",
					data: {
						actual: mentionChar(cNode),
						expected: expectedRaw
					},
					fix: fixReplaceNode(cNode, expectedRaw)
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/grapheme-string-literal.ts
const segmenter$1 = new Intl.Segmenter();
var grapheme_string_literal_default = createRule("grapheme-string-literal", {
	meta: {
		docs: {
			description: "enforce single grapheme in string literal",
			category: "Stylistic Issues",
			recommended: false
		},
		schema: [],
		messages: { onlySingleCharacters: "Only single characters and graphemes are allowed inside character classes. Use regular alternatives (e.g. `{{alternatives}}`) for strings instead." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, getRegexpLocation } = regexpContext;
			function isMultipleGraphemes(saNode) {
				if (saNode.elements.length <= 1) return false;
				const string = String.fromCodePoint(...saNode.elements.map((element) => element.value));
				return [...segmenter$1.segment(string)].length > 1;
			}
			function buildAlternativeExample(saNode) {
				return `(?:${saNode.parent.alternatives.filter(isMultipleGraphemes).map((alt) => alt.raw).join("|")}|[...])`;
			}
			return { onStringAlternativeEnter(saNode) {
				if (!isMultipleGraphemes(saNode)) return;
				context.report({
					node,
					loc: getRegexpLocation(saNode),
					messageId: "onlySingleCharacters",
					data: { alternatives: buildAlternativeExample(saNode) }
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/hexadecimal-escape.ts
var hexadecimal_escape_default = createRule("hexadecimal-escape", {
	meta: {
		docs: {
			description: "enforce consistent usage of hexadecimal escape",
			category: "Stylistic Issues",
			recommended: false
		},
		fixable: "code",
		schema: [{ enum: ["always", "never"] }],
		messages: {
			expectedHexEscape: "Expected hexadecimal escape ('{{hexEscape}}'), but {{unexpectedKind}} escape ('{{rejectEscape}}') is used.",
			unexpectedHexEscape: "Unexpected hexadecimal escape ('{{hexEscape}}')."
		},
		type: "suggestion"
	},
	create(context) {
		const always = context.options[0] !== "never";
		function verifyForAlways({ node, getRegexpLocation, fixReplaceNode }, kind, cNode) {
			if (kind !== EscapeSequenceKind.unicode && kind !== EscapeSequenceKind.unicodeCodePoint) return;
			const hexEscape = `\\x${cNode.value.toString(16).padStart(2, "0")}`;
			context.report({
				node,
				loc: getRegexpLocation(cNode),
				messageId: "expectedHexEscape",
				data: {
					hexEscape,
					unexpectedKind: kind,
					rejectEscape: cNode.raw
				},
				fix: fixReplaceNode(cNode, hexEscape)
			});
		}
		function verifyForNever({ node, getRegexpLocation, fixReplaceNode }, kind, cNode) {
			if (kind !== EscapeSequenceKind.hexadecimal) return;
			context.report({
				node,
				loc: getRegexpLocation(cNode),
				messageId: "unexpectedHexEscape",
				data: { hexEscape: cNode.raw },
				fix: fixReplaceNode(cNode, () => `\\u00${cNode.raw.slice(2)}`)
			});
		}
		const verify = always ? verifyForAlways : verifyForNever;
		function createVisitor(regexpContext) {
			return { onCharacterEnter(cNode) {
				if (cNode.value > 255) return;
				const kind = getEscapeSequenceKind(cNode.raw);
				if (!kind) return;
				verify(regexpContext, kind, cNode);
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/letter-case.ts
const CASE_SCHEMA = [
	"lowercase",
	"uppercase",
	"ignore"
];
const DEFAULTS = {
	caseInsensitive: "lowercase",
	unicodeEscape: "lowercase",
	hexadecimalEscape: "lowercase",
	controlEscape: "uppercase"
};
function parseOptions(option) {
	if (!option) return DEFAULTS;
	return {
		caseInsensitive: option.caseInsensitive || DEFAULTS.caseInsensitive,
		unicodeEscape: option.unicodeEscape || DEFAULTS.unicodeEscape,
		hexadecimalEscape: option.hexadecimalEscape || DEFAULTS.hexadecimalEscape,
		controlEscape: option.controlEscape || DEFAULTS.controlEscape
	};
}
const CODE_POINT_CASE_CHECKER = {
	lowercase: isLowercaseLetter,
	uppercase: isUppercaseLetter
};
const STRING_CASE_CHECKER = {
	lowercase: (s) => s.toLowerCase() === s,
	uppercase: (s) => s.toUpperCase() === s
};
const CONVERTER = {
	lowercase: (s) => s.toLowerCase(),
	uppercase: (s) => s.toUpperCase()
};
var letter_case_default = createRule("letter-case", {
	meta: {
		docs: {
			description: "enforce into your favorite case",
			category: "Stylistic Issues",
			recommended: false
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: {
				caseInsensitive: { enum: CASE_SCHEMA },
				unicodeEscape: { enum: CASE_SCHEMA },
				hexadecimalEscape: { enum: CASE_SCHEMA },
				controlEscape: { enum: CASE_SCHEMA }
			},
			additionalProperties: false
		}],
		messages: { unexpected: "'{{char}}' is not in {{case}}" },
		type: "layout"
	},
	create(context) {
		const options = parseOptions(context.options[0]);
		function report({ node, getRegexpLocation, fixReplaceNode }, reportNode, letterCase, convertText) {
			context.report({
				node,
				loc: getRegexpLocation(reportNode),
				messageId: "unexpected",
				data: {
					char: reportNode.raw,
					case: letterCase
				},
				fix: fixReplaceNode(reportNode, () => convertText(CONVERTER[letterCase]))
			});
		}
		function verifyCharacterInCaseInsensitive(regexpContext, cNode) {
			if (cNode.parent.type === "CharacterClassRange" || options.caseInsensitive === "ignore") return;
			if (CODE_POINT_CASE_CHECKER[options.caseInsensitive](cNode.value) || !isLetter(cNode.value)) return;
			report(regexpContext, cNode, options.caseInsensitive, (converter) => converter(String.fromCodePoint(cNode.value)));
		}
		function verifyCharacterClassRangeInCaseInsensitive(regexpContext, ccrNode) {
			if (options.caseInsensitive === "ignore") return;
			if (CODE_POINT_CASE_CHECKER[options.caseInsensitive](ccrNode.min.value) || !isLetter(ccrNode.min.value) || CODE_POINT_CASE_CHECKER[options.caseInsensitive](ccrNode.max.value) || !isLetter(ccrNode.max.value)) return;
			report(regexpContext, ccrNode, options.caseInsensitive, (converter) => `${converter(String.fromCodePoint(ccrNode.min.value))}-${converter(String.fromCodePoint(ccrNode.max.value))}`);
		}
		function verifyCharacterInUnicodeEscape(regexpContext, cNode) {
			if (options.unicodeEscape === "ignore") return;
			const parts = /^(?<prefix>\\u\{?)(?<code>.*?)(?<suffix>\}?)$/u.exec(cNode.raw);
			if (STRING_CASE_CHECKER[options.unicodeEscape](parts.groups.code)) return;
			report(regexpContext, cNode, options.unicodeEscape, (converter) => `${parts.groups.prefix}${converter(parts.groups.code)}${parts.groups.suffix}`);
		}
		function verifyCharacterInHexadecimalEscape(regexpContext, cNode) {
			if (options.hexadecimalEscape === "ignore") return;
			const parts = /^\\x(?<code>.*)$/u.exec(cNode.raw);
			if (STRING_CASE_CHECKER[options.hexadecimalEscape](parts.groups.code)) return;
			report(regexpContext, cNode, options.hexadecimalEscape, (converter) => `\\x${converter(parts.groups.code)}`);
		}
		function verifyCharacterInControl(regexpContext, cNode) {
			if (options.controlEscape === "ignore") return;
			const parts = /^\\c(?<code>.*)$/u.exec(cNode.raw);
			if (STRING_CASE_CHECKER[options.controlEscape](parts.groups.code)) return;
			report(regexpContext, cNode, options.controlEscape, (converter) => `\\c${converter(parts.groups.code)}`);
		}
		function createVisitor(regexpContext) {
			const { flags } = regexpContext;
			return {
				onCharacterEnter(cNode) {
					if (flags.ignoreCase) verifyCharacterInCaseInsensitive(regexpContext, cNode);
					const escapeKind = getEscapeSequenceKind(cNode.raw);
					if (escapeKind === EscapeSequenceKind.unicode || escapeKind === EscapeSequenceKind.unicodeCodePoint) verifyCharacterInUnicodeEscape(regexpContext, cNode);
					if (escapeKind === EscapeSequenceKind.hexadecimal) verifyCharacterInHexadecimalEscape(regexpContext, cNode);
					if (escapeKind === EscapeSequenceKind.control) verifyCharacterInControl(regexpContext, cNode);
				},
				...flags.ignoreCase ? { onCharacterClassRangeEnter(ccrNode) {
					verifyCharacterClassRangeInCaseInsensitive(regexpContext, ccrNode);
				} } : {}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/match-any.ts
const OPTION_SS1 = "[\\s\\S]";
const OPTION_SS2 = "[\\S\\s]";
const OPTION_CARET = "[^]";
const OPTION_DOTALL = "dotAll";
var match_any_default = createRule("match-any", {
	meta: {
		docs: {
			description: "enforce match any character style",
			category: "Stylistic Issues",
			recommended: true
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { allows: {
				type: "array",
				items: {
					type: "string",
					enum: [
						OPTION_SS1,
						OPTION_SS2,
						OPTION_CARET,
						OPTION_DOTALL
					]
				},
				uniqueItems: true,
				minItems: 1
			} },
			additionalProperties: false
		}],
		messages: { unexpected: "Unexpected using {{expr}} to match any character." },
		type: "suggestion"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		const allowList = context.options[0]?.allows ?? [OPTION_SS1, OPTION_DOTALL];
		const allows = new Set(allowList);
		const preference = allowList[0] || null;
		/**
		* Fix source code
		* @param fixer
		*/
		function fix(fixer, { node, flags, patternSource }, regexpNode) {
			if (!preference) return null;
			if (preference === OPTION_DOTALL) {
				if (!flags.dotAll) return null;
				if (!isRegexpLiteral(node)) return null;
				const range = patternSource.getReplaceRange(regexpNode);
				if (range == null) return null;
				const afterRange = [range.range[1], node.range[1]];
				return [range.replace(fixer, "."), fixer.replaceTextRange(afterRange, sourceCode.text.slice(...afterRange))];
			}
			if (regexpNode.type === "CharacterClass" && preference[0] === "[" && preference.endsWith("]")) return patternSource.getReplaceRange({
				start: regexpNode.start + 1,
				end: regexpNode.end - 1
			})?.replace(fixer, preference.slice(1, -1)) ?? null;
			return patternSource.getReplaceRange(regexpNode)?.replace(fixer, preference) ?? null;
		}
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation } = regexpContext;
			function onClass(ccNode) {
				if (matchesAllCharacters(ccNode, flags) && !hasStrings(ccNode, flags) && !allows.has(ccNode.raw)) context.report({
					node,
					loc: getRegexpLocation(ccNode),
					messageId: "unexpected",
					data: { expr: mention(ccNode) },
					fix(fixer) {
						return fix(fixer, regexpContext, ccNode);
					}
				});
			}
			return {
				onCharacterSetEnter(csNode) {
					if (csNode.kind === "any" && flags.dotAll && !allows.has(OPTION_DOTALL)) context.report({
						node,
						loc: getRegexpLocation(csNode),
						messageId: "unexpected",
						data: { expr: mention(csNode) },
						fix(fixer) {
							return fix(fixer, regexpContext, csNode);
						}
					});
				},
				onCharacterClassEnter: onClass,
				onExpressionCharacterClassEnter: onClass
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/negation.ts
/** Checks whether the given character class is negatable. */
function isNegatableCharacterClassElement$1(node) {
	return node.type === "CharacterClass" || node.type === "ExpressionCharacterClass" || node.type === "CharacterSet" && (node.kind !== "property" || !node.strings);
}
var negation_default = createRule("negation", {
	meta: {
		docs: {
			description: "enforce use of escapes on negation",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { unexpected: "Unexpected negated character class. Use '{{negatedCharSet}}' instead." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, getRegexpLocation, fixReplaceNode, flags }) {
			return { onCharacterClassEnter(ccNode) {
				if (!ccNode.negate || ccNode.elements.length !== 1) return;
				const element = ccNode.elements[0];
				if (!isNegatableCharacterClassElement$1(element)) return;
				if (element.type !== "CharacterSet" && !element.negate) return;
				if (flags.ignoreCase && !flags.unicodeSets && element.type === "CharacterSet" && element.kind === "property") {
					const ccSet = toUnicodeSet(ccNode, flags);
					const negatedElementSet = toUnicodeSet({
						...element,
						negate: !element.negate
					}, flags);
					if (!ccSet.equals(negatedElementSet)) return;
				}
				const negatedCharSet = getNegationText(element);
				context.report({
					node,
					loc: getRegexpLocation(ccNode),
					messageId: "unexpected",
					data: { negatedCharSet },
					fix: fixReplaceNode(ccNode, negatedCharSet)
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
/**
* Gets the text that negation the CharacterSet.
*/
function getNegationText(node) {
	if (node.type === "CharacterSet") {
		let kind = node.raw[1];
		if (kind.toLowerCase() === kind) kind = kind.toUpperCase();
		else kind = kind.toLowerCase();
		return `\\${kind}${node.raw.slice(2)}`;
	}
	if (node.type === "CharacterClass") return `[${node.elements.map((e) => e.raw).join("")}]`;
	if (node.type === "ExpressionCharacterClass") return `[${node.raw.slice(2, -1)}]`;
	return assertNever(node);
}
//#endregion
//#region lib/rules/no-contradiction-with-assertion.ts
/**
* Returns whether the given assertions is guaranteed to always trivially
* reject or accept.
*
* @param assertion
*/
function isTrivialAssertion(assertion, dir, flags) {
	if (assertion.kind !== "word") {
		if (getMatchingDirectionFromAssertionKind(assertion.kind) !== dir) return true;
	}
	if (assertion.kind === "lookahead" || assertion.kind === "lookbehind") {
		if (isPotentiallyEmpty(assertion.alternatives, flags)) return true;
	}
	const look = FirstConsumedChars.toLook(getFirstConsumedChar(assertion, dir, flags));
	if (look.char.isEmpty || look.char.isAll) return true;
	const after = getFirstCharAfter(assertion, dir, flags);
	if (!after.edge) {
		if (look.exact && look.char.isSupersetOf(after.char)) return true;
		if (look.char.isDisjointWith(after.char)) return true;
	}
	return false;
}
/**
* Returns the next elements always reachable from the given element without
* consuming characters
*/
function* getNextElements(start, dir, flags) {
	let element = start;
	for (;;) {
		const parent = element.parent;
		if (parent.type === "CharacterClass" || parent.type === "CharacterClassRange" || parent.type === "ClassIntersection" || parent.type === "ClassSubtraction" || parent.type === "StringAlternative") return;
		if (parent.type === "Quantifier") if (parent.max === 1) {
			element = parent;
			continue;
		} else return;
		const elements = parent.elements;
		const index = elements.indexOf(element);
		const inc = dir === "ltr" ? 1 : -1;
		for (let i = index + inc; i >= 0 && i < elements.length; i += inc) {
			const e = elements[i];
			yield e;
			if (!isZeroLength(e, flags)) return;
		}
		const grandParent = parent.parent;
		if ((grandParent.type === "Group" || grandParent.type === "CapturingGroup" || grandParent.type === "Assertion" && getMatchingDirectionFromAssertionKind(grandParent.kind) !== dir) && grandParent.alternatives.length === 1) {
			element = grandParent;
			continue;
		}
		return;
	}
}
/**
* Goes through the given element and all of its children until a the condition
* returns true or a character is (potentially) consumed.
*/
function tryFindContradictionIn(element, dir, condition, flags) {
	if (condition(element)) return true;
	if (element.type === "CapturingGroup" || element.type === "Group") {
		let some = false;
		element.alternatives.forEach((a) => {
			if (tryFindContradictionInAlternative(a, dir, condition, flags)) some = true;
		});
		return some;
	}
	if (element.type === "Quantifier" && element.max === 1) return tryFindContradictionIn(element.element, dir, condition, flags);
	if (element.type === "Assertion" && (element.kind === "lookahead" || element.kind === "lookbehind") && getMatchingDirectionFromAssertionKind(element.kind) === dir) element.alternatives.forEach((a) => tryFindContradictionInAlternative(a, dir, condition, flags));
	return false;
}
/**
* Goes through all elements of the given alternative until the condition
* returns true or a character is (potentially) consumed.
*/
function tryFindContradictionInAlternative(alternative, dir, condition, flags) {
	if (condition(alternative)) return true;
	const { elements } = alternative;
	const first = dir === "ltr" ? 0 : elements.length;
	const inc = dir === "ltr" ? 1 : -1;
	for (let i = first; i >= 0 && i < elements.length; i += inc) {
		const e = elements[i];
		if (tryFindContradictionIn(e, dir, condition, flags)) return true;
		if (!isZeroLength(e, flags)) break;
	}
	return false;
}
/**
* Returns whether the 2 look chars are disjoint (== mutually exclusive).
*/
function disjoint(a, b) {
	if (a.edge && b.edge) return false;
	return a.char.isDisjointWith(b.char);
}
var no_contradiction_with_assertion_default = createRule("no-contradiction-with-assertion", {
	meta: {
		docs: {
			description: "disallow elements that contradict assertions",
			category: "Possible Errors",
			recommended: true
		},
		schema: [],
		messages: {
			alternative: "The alternative {{ alt }} can never be entered because it contradicts with the assertion {{ assertion }}. Either change the alternative or assertion to resolve the contradiction.",
			cannotEnterQuantifier: "The quantifier {{ quant }} can never be entered because its element contradicts with the assertion {{ assertion }}. Change or remove the quantifier or change the assertion to resolve the contradiction.",
			alwaysEnterQuantifier: "The quantifier {{ quant }} is always entered despite having a minimum of 0. This is because the assertion {{ assertion }} contradicts with the element(s) after the quantifier. Either set the minimum to 1 ({{ newQuant }}) or change the assertion.",
			removeQuantifier: "Remove the quantifier.",
			changeQuantifier: "Change the quantifier to {{ newQuant }}."
		},
		hasSuggestions: true,
		type: "problem"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation, fixReplaceQuant, fixReplaceNode } = regexpContext;
			/** Analyses the given assertion. */
			function analyseAssertion(assertion, dir) {
				if (isTrivialAssertion(assertion, dir, flags)) return;
				const assertionLook = FirstConsumedChars.toLook(getFirstConsumedChar(assertion, dir, flags));
				for (const element of getNextElements(assertion, dir, flags)) if (tryFindContradictionIn(element, dir, contradicts, flags)) break;
				/** Whether the alternative contradicts the current assertion. */
				function contradictsAlternative(alternative) {
					let consumed = getFirstConsumedChar(alternative, dir, flags);
					if (consumed.empty) consumed = FirstConsumedChars.concat([consumed, getFirstConsumedCharAfter(alternative, dir, flags)], flags);
					if (disjoint(assertionLook, FirstConsumedChars.toLook(consumed))) {
						context.report({
							node,
							loc: getRegexpLocation(alternative),
							messageId: "alternative",
							data: {
								assertion: mention(assertion),
								alt: mention(alternative)
							}
						});
						return true;
					}
					return false;
				}
				/** Whether the alternative contradicts the current assertion. */
				function contradictsQuantifier(quant) {
					if (quant.max === 0) return false;
					if (quant.min !== 0) return false;
					const consumed = getFirstConsumedChar(quant.element, dir, flags);
					if (disjoint(assertionLook, FirstConsumedChars.toLook(consumed))) {
						context.report({
							node,
							loc: getRegexpLocation(quant),
							messageId: "cannotEnterQuantifier",
							data: {
								assertion: mention(assertion),
								quant: mention(quant)
							},
							suggest: [{
								messageId: "removeQuantifier",
								fix: fixReplaceNode(quant, "")
							}]
						});
						return true;
					}
					if (disjoint(assertionLook, getFirstCharAfter(quant, dir, flags))) {
						const newQuant = quantToString({
							...quant,
							min: 1
						});
						context.report({
							node,
							loc: getRegexpLocation(quant),
							messageId: "alwaysEnterQuantifier",
							data: {
								assertion: mention(assertion),
								quant: mention(quant),
								newQuant
							},
							suggest: [{
								messageId: "changeQuantifier",
								data: { newQuant },
								fix: fixReplaceQuant(quant, {
									min: 1,
									max: quant.max
								})
							}]
						});
						return true;
					}
					return false;
				}
				/** Whether the element contradicts the current assertion. */
				function contradicts(element) {
					if (element.type === "Alternative") return contradictsAlternative(element);
					else if (element.type === "Quantifier") return contradictsQuantifier(element);
					return false;
				}
			}
			return { onAssertionEnter(assertion) {
				analyseAssertion(assertion, "ltr");
				analyseAssertion(assertion, "rtl");
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-control-character.ts
const CONTROL_CHARS = new Map([
	[0, "\\0"],
	[9, "\\t"],
	[10, "\\n"],
	[11, "\\v"],
	[12, "\\f"],
	[13, "\\r"]
]);
const ALLOWED_CONTROL_CHARS = /^\\[0fnrtv]$/u;
var no_control_character_default = createRule("no-control-character", {
	meta: {
		docs: {
			description: "disallow control characters",
			category: "Possible Errors",
			recommended: false
		},
		schema: [],
		messages: {
			unexpected: "Unexpected control character {{ char }}.",
			escape: "Use {{ escape }} instead."
		},
		type: "suggestion",
		hasSuggestions: true
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, patternSource, getRegexpLocation, fixReplaceNode } = regexpContext;
			function isBadEscapeRaw(raw, cp) {
				return raw.codePointAt(0) === cp || raw.startsWith("\\x") || raw.startsWith("\\u");
			}
			function isAllowedEscapeRaw(raw) {
				return ALLOWED_CONTROL_CHARS.test(raw) || raw[0] === "\\" && ALLOWED_CONTROL_CHARS.test(raw.slice(1));
			}
			/**
			* Whether the given char is represented using an unwanted escape
			* sequence.
			*/
			function isBadEscape(char) {
				const range = patternSource.getReplaceRange(char)?.range;
				const sourceRaw = range ? context.sourceCode.text.slice(...range) : char.raw;
				if (isAllowedEscapeRaw(char.raw) || isAllowedEscapeRaw(sourceRaw)) return false;
				return isBadEscapeRaw(char.raw, char.value) || char.raw[0] === "\\" && isBadEscapeRaw(char.raw.slice(1), char.value);
			}
			return { onCharacterEnter(cNode) {
				if (cNode.value <= 31 && isBadEscape(cNode)) {
					const suggest = [];
					const allowedEscape = CONTROL_CHARS.get(cNode.value);
					if (allowedEscape !== void 0) suggest.push({
						messageId: "escape",
						data: { escape: mention(allowedEscape) },
						fix: fixReplaceNode(cNode, allowedEscape)
					});
					context.report({
						node,
						loc: getRegexpLocation(cNode),
						messageId: "unexpected",
						data: { char: mentionChar(cNode) },
						suggest
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/utils/refa.ts
/**
* Create a `JS.RegexppAst` object as required by refa's `JS.Parser.fromAst`
* method and `ParsedLiteral` interface of the scslre library.
*/
function getJSRegexppAst(context, ignoreSticky = false) {
	const { flags, flagsString, patternAst } = context;
	return {
		pattern: patternAst,
		flags: {
			type: "Flags",
			raw: flagsString ?? "",
			parent: null,
			start: NaN,
			end: NaN,
			dotAll: flags.dotAll ?? false,
			global: flags.global ?? false,
			hasIndices: flags.hasIndices ?? false,
			ignoreCase: flags.ignoreCase ?? false,
			multiline: flags.multiline ?? false,
			sticky: !ignoreSticky && (flags.sticky ?? false),
			unicode: flags.unicode ?? false,
			unicodeSets: flags.unicodeSets ?? false
		}
	};
}
/**
* Returns a `JS.Parser` for the given regex context.
*/
const getParser = cachedFn((context) => JS.Parser.fromAst(getJSRegexppAst(context)));
/**
* Asserts that the given flags are valid (no `u` and `v` flag together).
* @param flags
*/
function assertValidFlags(flags) {
	if (!JS.isFlags(flags)) throw new Error(`Invalid flags: ${JSON.stringify(flags)}`);
}
/**
* Returns a regexp literal source of the given char set or char.
*/
function toCharSetSource(charSetOrChar, flags) {
	assertValidFlags(flags);
	let charSet;
	if (typeof charSetOrChar === "number") charSet = JS.createCharSet([charSetOrChar], flags);
	else charSet = charSetOrChar;
	return JS.toLiteral({
		type: "Concatenation",
		elements: [{
			type: "CharacterClass",
			characters: charSet
		}]
	}, { flags }).source;
}
//#endregion
//#region lib/rules/no-dupe-characters-character-class.ts
/**
* Grouping the given character class elements.
* @param elements The elements to grouping.
*/
function groupElements(elements, flags) {
	const duplicates = [];
	const characters = /* @__PURE__ */ new Map();
	const characterRanges = /* @__PURE__ */ new Map();
	const characterSetAndClasses = /* @__PURE__ */ new Map();
	/**
	* If the given element is a duplicate of another element, it will be added
	* to the the duplicates array. Otherwise, it will be added to the given
	* group.
	*/
	function addToGroup(group, key, element) {
		const current = group.get(key);
		if (current !== void 0) duplicates.push({
			element: current,
			duplicate: element
		});
		else group.set(key, element);
	}
	for (const e of elements) if (e.type === "Character") {
		const key = toCharSet(e, flags).ranges[0].min;
		addToGroup(characters, key, e);
	} else if (e.type === "CharacterClassRange") addToGroup(characterRanges, buildRangeKey(toCharSet(e, flags)), e);
	else if (e.type === "CharacterSet" || e.type === "CharacterClass" || e.type === "ClassStringDisjunction" || e.type === "ExpressionCharacterClass") {
		const key = e.raw;
		addToGroup(characterSetAndClasses, key, e);
	} else assertNever(e);
	return {
		duplicates,
		characters: [...characters.values()],
		characterRanges: [...characterRanges.values()],
		characterSetAndClasses: [...characterSetAndClasses.values()]
	};
	function buildRangeKey(rangeCharSet) {
		return rangeCharSet.ranges.map((r) => String.fromCodePoint(r.min, r.max)).join(",");
	}
}
/**
* Returns whether the given character is within the bounds of the given char range.
*/
function inRange$1({ min, max }, char) {
	return min <= char && char <= max;
}
var no_dupe_characters_character_class_default = createRule("no-dupe-characters-character-class", {
	meta: {
		type: "suggestion",
		docs: {
			description: "disallow duplicate characters in the RegExp character class",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: {
			duplicate: "Unexpected duplicate {{duplicate}}.",
			duplicateNonObvious: "Unexpected duplicate. {{duplicate}} is a duplicate of {{element}}.",
			subset: "{{subsetElement}} is already included in {{element}}.",
			subsetOfMany: "{{subsetElement}} is already included by the elements {{elements}}.",
			overlap: "Unexpected overlap of {{elementA}} and {{elementB}} was found '{{overlap}}'."
		}
	},
	create(context) {
		/**
		* Report a duplicate element.
		*/
		function reportDuplicate(regexpContext, duplicate, element) {
			const { node, getRegexpLocation } = regexpContext;
			if (duplicate.raw === element.raw) context.report({
				node,
				loc: getRegexpLocation(duplicate),
				messageId: "duplicate",
				data: { duplicate: mentionChar(duplicate) },
				fix: fixRemoveCharacterClassElement(regexpContext, duplicate)
			});
			else context.report({
				node,
				loc: getRegexpLocation(duplicate),
				messageId: "duplicateNonObvious",
				data: {
					duplicate: mentionChar(duplicate),
					element: mentionChar(element)
				},
				fix: fixRemoveCharacterClassElement(regexpContext, duplicate)
			});
		}
		/**
		* Reports that the elements intersect.
		*/
		function reportOverlap({ node, getRegexpLocation }, element, intersectElement, overlap) {
			context.report({
				node,
				loc: getRegexpLocation(element),
				messageId: "overlap",
				data: {
					elementA: mentionChar(element),
					elementB: mentionChar(intersectElement),
					overlap
				}
			});
		}
		/**
		* Report the element included in the element.
		*/
		function reportSubset(regexpContext, subsetElement, element) {
			const { node, getRegexpLocation } = regexpContext;
			context.report({
				node,
				loc: getRegexpLocation(subsetElement),
				messageId: "subset",
				data: {
					subsetElement: mentionChar(subsetElement),
					element: mentionChar(element)
				},
				fix: fixRemoveCharacterClassElement(regexpContext, subsetElement)
			});
		}
		/**
		* Report the element included in the element.
		*/
		function reportSubsetOfMany(regexpContext, subsetElement, elements) {
			const { node, getRegexpLocation } = regexpContext;
			context.report({
				node,
				loc: getRegexpLocation(subsetElement),
				messageId: "subsetOfMany",
				data: {
					subsetElement: mentionChar(subsetElement),
					elements: `'${elements.map((e) => e.raw).join("")}' (${elements.map(mentionChar).join(", ")})`
				},
				fix: fixRemoveCharacterClassElement(regexpContext, subsetElement)
			});
		}
		function createVisitor(regexpContext) {
			const { flags } = regexpContext;
			return { onCharacterClassEnter(ccNode) {
				const { duplicates, characters, characterRanges, characterSetAndClasses } = groupElements(ccNode.elements, flags);
				const elementsOtherThanCharacter = [...characterRanges, ...characterSetAndClasses];
				const subsets = /* @__PURE__ */ new Set();
				for (const { element, duplicate } of duplicates) {
					reportDuplicate(regexpContext, duplicate, element);
					subsets.add(duplicate);
				}
				for (const char of characters) for (const other of elementsOtherThanCharacter) if (toUnicodeSet(other, flags).chars.has(char.value)) {
					reportSubset(regexpContext, char, other);
					subsets.add(char);
					break;
				}
				for (const element of elementsOtherThanCharacter) for (const other of elementsOtherThanCharacter) {
					if (element === other || subsets.has(other)) continue;
					if (toUnicodeSet(element, flags).isSubsetOf(toUnicodeSet(other, flags))) {
						reportSubset(regexpContext, element, other);
						subsets.add(element);
						break;
					}
				}
				const characterTotal = toUnicodeSet(characters.filter((c) => !subsets.has(c)), flags);
				for (const element of elementsOtherThanCharacter) {
					if (subsets.has(element)) continue;
					const totalOthers = characterTotal.union(...elementsOtherThanCharacter.filter((e) => !subsets.has(e) && e !== element).map((e) => toUnicodeSet(e, flags)));
					const elementCharSet = toUnicodeSet(element, flags);
					if (elementCharSet.isSubsetOf(totalOthers)) {
						reportSubsetOfMany(regexpContext, element, ccNode.elements.filter((e) => !subsets.has(e) && e !== element).filter((e) => !toUnicodeSet(e, flags).isDisjointWith(elementCharSet)));
						subsets.add(element);
					}
				}
				for (let i = 0; i < characterRanges.length; i++) {
					const range = characterRanges[i];
					if (subsets.has(range)) continue;
					for (let j = i + 1; j < elementsOtherThanCharacter.length; j++) {
						const other = elementsOtherThanCharacter[j];
						if (range === other || subsets.has(other)) continue;
						const intersection = toUnicodeSet(range, flags).intersect(toUnicodeSet(other, flags));
						if (intersection.isEmpty) continue;
						const interestingRanges = intersection.chars.ranges.filter((r) => inRange$1(r, range.min.value) || inRange$1(r, range.max.value));
						assertValidFlags(flags);
						const interest = JS.createCharSet(interestingRanges, flags);
						if (!interest.isEmpty) {
							reportOverlap(regexpContext, range, other, toCharSetSource(interest, flags));
							break;
						}
					}
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/utils/char-ranges.ts
const ALL_RANGES = [{
	min: 0,
	max: 1114111
}];
const ALPHANUMERIC_RANGES = [
	{
		min: CP_DIGIT_ZERO,
		max: CP_DIGIT_NINE
	},
	{
		min: CP_CAPITAL_A,
		max: CP_CAPITAL_Z
	},
	{
		min: CP_SMALL_A,
		max: CP_SMALL_Z
	}
];
/**
* Returns all character ranges allowed by the user.
*/
function getAllowedCharRanges(allowedByRuleOption, context) {
	let target = allowedByRuleOption || context.settings.regexp?.allowedCharacterRanges;
	if (!target) return ALPHANUMERIC_RANGES;
	if (typeof target === "string") target = [target];
	const allowed = [];
	for (const range of target) if (range === "all") return ALL_RANGES;
	else if (range === "alphanumeric") {
		if (target.length === 1) return ALPHANUMERIC_RANGES;
		allowed.push(...ALPHANUMERIC_RANGES);
	} else {
		const chars = [...range];
		if (chars.length !== 3 || chars[1] !== "-") throw new Error(`Invalid format: The range ${JSON.stringify(range)} is not of the form \`<char>-<char>\`.`);
		const min = chars[0].codePointAt(0);
		const max = chars[2].codePointAt(0);
		allowed.push({
			min,
			max
		});
	}
	return allowed;
}
/**
* Returns the schema of a value accepted by {@link getAllowedCharRanges}.
*/
function getAllowedCharValueSchema() {
	return { anyOf: [
		{ enum: ["all", "alphanumeric"] },
		{
			type: "array",
			items: [{ enum: ["all", "alphanumeric"] }],
			minItems: 1,
			additionalItems: false
		},
		{
			type: "array",
			items: { anyOf: [{ const: "alphanumeric" }, {
				type: "string",
				pattern: /^(?:[\ud800-\udbff][\udc00-\udfff]|[^\ud800-\udfff])-(?:[\ud800-\udbff][\udc00-\udfff]|[^\ud800-\udfff])$/.source
			}] },
			uniqueItems: true,
			minItems: 1,
			additionalItems: false
		}
	] };
}
/**
* Returns whether the given range is in the given list of ranges.
*/
function inRange(ranges, min, max = min) {
	for (const range of ranges) if (range.min <= min && max <= range.max) return true;
	return false;
}
//#endregion
//#region lib/utils/partial-parser.ts
var Context = class {
	/**
	* The ancestor nodes of the alternative + the alternative itself.
	*/
	ancestors;
	alternative;
	constructor(alternative) {
		this.alternative = alternative;
		const ancestors = /* @__PURE__ */ new Set();
		for (let n = alternative; n; n = n.parent) ancestors.add(n);
		this.ancestors = ancestors;
	}
};
var PartialParser = class {
	parser;
	options;
	nativeCache = /* @__PURE__ */ new WeakMap();
	constructor(parser, options = {}) {
		this.parser = parser;
		this.options = options;
	}
	/**
	* Parses the given element while guaranteeing that all paths of the returned
	* expression go through the given alternative.
	*/
	parse(node, alternative) {
		switch (node.type) {
			case "Pattern": return {
				type: "Expression",
				alternatives: this.parseAlternatives(node.alternatives, new Context(alternative))
			};
			case "Alternative": return {
				type: "Expression",
				alternatives: [this.parseAlternative(node, new Context(alternative))]
			};
			default: return {
				type: "Expression",
				alternatives: [{
					type: "Concatenation",
					elements: [this.parseElement(node, new Context(alternative))]
				}]
			};
		}
	}
	parseAlternatives(alternatives, context) {
		const ancestor = alternatives.find((a) => context.ancestors.has(a));
		if (ancestor) return [this.parseAlternative(ancestor, context)];
		const result = [];
		for (const a of alternatives) result.push(...this.parser.parseElement(a, this.options).expression.alternatives);
		return result;
	}
	parseAlternative(alternative, context) {
		return {
			type: "Concatenation",
			elements: alternative.elements.map((e) => this.parseElement(e, context))
		};
	}
	parseStringAlternatives(alternatives, context) {
		const ancestor = alternatives.find((a) => context.ancestors.has(a));
		if (ancestor) return [this.parseStringAlternative(ancestor)];
		return alternatives.map((a) => this.parseStringAlternative(a));
	}
	parseStringAlternative(alternative) {
		return {
			type: "Concatenation",
			elements: alternative.elements.map((e) => this.nativeParseElement(e))
		};
	}
	parseElement(element, context) {
		if (!context.ancestors.has(element)) return this.nativeParseElement(element);
		switch (element.type) {
			case "Assertion":
			case "Backreference":
			case "Character":
			case "CharacterSet":
			case "ExpressionCharacterClass": return this.nativeParseElement(element);
			case "CharacterClassRange":
				if (context.alternative === element.min) return this.nativeParseElement(context.alternative);
				else if (context.alternative === element.max) return this.nativeParseElement(context.alternative);
				return this.nativeParseElement(element);
			case "CharacterClass": return this.parseCharacterClass(element, context);
			case "ClassStringDisjunction": return {
				type: "Alternation",
				alternatives: this.parseStringAlternatives(element.alternatives, context)
			};
			case "Group":
			case "CapturingGroup": return {
				type: "Alternation",
				alternatives: this.parseAlternatives(element.alternatives, context)
			};
			case "Quantifier": {
				const alternatives = element.element.type === "Group" || element.element.type === "CapturingGroup" ? this.parseAlternatives(element.element.alternatives, context) : [{
					type: "Concatenation",
					elements: [this.parseElement(element.element, context)]
				}];
				return {
					type: "Quantifier",
					min: element.min,
					max: element.max,
					lazy: !element.greedy,
					alternatives
				};
			}
			default: throw assertNever(element);
		}
	}
	parseCharacterClass(cc, context) {
		if (cc.negate || !context.ancestors.has(cc) || context.alternative.type === "Alternative") return this.nativeParseElement(cc);
		for (const e of cc.elements) if (context.ancestors.has(e)) return this.parseElement(e, context);
		return this.nativeParseElement(cc);
	}
	nativeParseElement(element) {
		let cached = this.nativeCache.get(element);
		if (!cached) {
			cached = this.nativeParseElementUncached(element);
			this.nativeCache.set(element, cached);
		}
		return cached;
	}
	nativeParseElementUncached(element) {
		if (element.type === "CharacterClassRange") {
			const range = {
				min: element.min.value,
				max: element.max.value
			};
			return {
				type: "CharacterClass",
				characters: JS.createCharSet([range], this.parser.flags)
			};
		} else if (element.type === "ClassStringDisjunction") return {
			type: "Alternation",
			alternatives: element.alternatives.map((a) => this.parseStringAlternative(a))
		};
		const { expression } = this.parser.parseElement(element, this.options);
		if (expression.alternatives.length === 1) {
			const elements = expression.alternatives[0].elements;
			if (elements.length === 1) return elements[0];
		}
		return {
			type: "Alternation",
			alternatives: expression.alternatives
		};
	}
};
//#endregion
//#region lib/rules/no-dupe-disjunctions.ts
/**
* Returns whether the node or the elements of the node are effectively
* quantified with a star.
*/
function isStared(node) {
	let max = getEffectiveMaximumRepetition(node);
	if (node.type === "Quantifier") max *= node.max;
	return max > 10;
}
/**
* Check has after pattern
*/
function hasNothingAfterNode(node) {
	const md = getMatchingDirection(node);
	for (let p = node;; p = p.parent) {
		if (p.type === "Assertion" || p.type === "Pattern") return true;
		if (p.type !== "Alternative") {
			const parent = p.parent;
			if (parent.type === "Quantifier") {
				if (parent.max > 1) return false;
			} else {
				const lastIndex = md === "ltr" ? parent.elements.length - 1 : 0;
				if (parent.elements[lastIndex] !== p) return false;
			}
		}
	}
}
/**
* Returns whether the given RE AST contains assertions.
*/
function containsAssertions(expression) {
	try {
		visitAst(expression, { onAssertionEnter() {
			throw new Error();
		} });
		return false;
	} catch {
		return true;
	}
}
/**
* Returns whether the given RE AST contains assertions or unknowns.
*/
function containsAssertionsOrUnknowns(expression) {
	try {
		visitAst(expression, {
			onAssertionEnter() {
				throw new Error();
			},
			onUnknownEnter() {
				throw new Error();
			}
		});
		return false;
	} catch {
		return true;
	}
}
/**
* Returns whether the given nodes contains any features that cannot be
* expressed by pure regular expression. This mainly includes assertions and
* backreferences.
*/
function isNonRegular(node) {
	return hasSomeDescendant(node, (d) => d.type === "Assertion" || d.type === "Backreference");
}
/**
* Create an NFA from the given element.
*
* The `partial` value determines whether the NFA perfectly represents the given
* element. Some elements might contain features that cannot be represented
* using NFA in which case a partial NFA will be created (e.g. the NFA of
* `a|\bfoo\b` is equivalent to the NFA of `a`).
*/
function toNFA(parser, element) {
	try {
		const { expression, maxCharacter } = parser.parseElement(element, {
			backreferences: "unknown",
			assertions: "parse"
		});
		let e;
		if (containsAssertions(expression)) e = transform(Transformers.simplify({
			ignoreAmbiguity: true,
			ignoreOrder: true
		}), expression);
		else e = expression;
		return {
			nfa: NFA.fromRegex(e, { maxCharacter }, {
				assertions: "disable",
				unknowns: "disable"
			}),
			partial: containsAssertionsOrUnknowns(e)
		};
	} catch {
		return {
			nfa: NFA.empty({ maxCharacter: parser.maxCharacter }),
			partial: true
		};
	}
}
/**
* Yields all nested alternatives in the given root alternative.
*
* This will yield actual alternative nodes as well as character class
* elements. The elements of a non-negated character class (e.g. `[abc]`) can
* be thought of as an alternative. That's why they are returned.
*
* Note: If a group contains only a single alternative, then this group won't
* be yielded by this function. This is because the partial NFA of that single
* alternative is that same as the partial NFA of the parent alternative of the
* group. A similar condition applies for the elements of character classes.
*/
function* iterateNestedAlternatives(alternative) {
	for (const e of alternative.elements) {
		if (e.type === "Group" || e.type === "CapturingGroup") for (const a of e.alternatives) {
			if (e.alternatives.length > 1) yield a;
			yield* iterateNestedAlternatives(a);
		}
		if (e.type === "CharacterClass" && !e.negate) {
			const nested = [];
			const addToNested = (charElement) => {
				switch (charElement.type) {
					case "CharacterClassRange": {
						const min = charElement.min;
						const max = charElement.max;
						if (min.value === max.value) nested.push(charElement);
						else if (min.value + 1 === max.value) nested.push(min, max);
						else nested.push(charElement, min, max);
						break;
					}
					case "ClassStringDisjunction":
						nested.push(...charElement.alternatives);
						break;
					case "CharacterClass":
						if (!charElement.negate) charElement.elements.forEach(addToNested);
						else nested.push(charElement);
						break;
					case "Character":
					case "CharacterSet":
					case "ExpressionCharacterClass":
						nested.push(charElement);
						break;
					default: throw assertNever(charElement);
				}
			};
			e.elements.forEach(addToNested);
			if (nested.length > 1) yield* nested;
		}
	}
}
/**
* This will return all partial alternatives.
*
* A partial alternative is the NFA of the given alternative but with one
* nested alternative missing.
*/
function* iteratePartialAlternatives(alternative, parser) {
	if (isNonRegular(alternative)) return;
	const maxCharacter = parser.maxCharacter;
	const partialParser = new PartialParser(parser, {
		assertions: "throw",
		backreferences: "throw"
	});
	for (const nested of iterateNestedAlternatives(alternative)) try {
		const expression = partialParser.parse(alternative, nested);
		yield {
			nested,
			nfa: NFA.fromRegex(expression, { maxCharacter })
		};
	} catch {}
}
function unionAll(nfas) {
	if (nfas.length === 0) throw new Error("Cannot union 0 NFAs.");
	else if (nfas.length === 1) return nfas[0];
	const total = nfas[0].copy();
	for (let i = 1; i < nfas.length; i++) total.union(nfas[i]);
	return total;
}
const MAX_DFA_NODES = 1e5;
function isSubsetOf(superset, subset) {
	try {
		const a = DFA.fromIntersection(superset, subset, new DFA.LimitedNodeFactory(MAX_DFA_NODES));
		const b = DFA.fromFA(subset, new DFA.LimitedNodeFactory(MAX_DFA_NODES));
		a.minimize();
		b.minimize();
		return a.structurallyEqual(b);
	} catch {
		return null;
	}
}
var SubsetRelation = /* @__PURE__ */ function(SubsetRelation) {
	SubsetRelation[SubsetRelation["none"] = 0] = "none";
	SubsetRelation[SubsetRelation["leftEqualRight"] = 1] = "leftEqualRight";
	SubsetRelation[SubsetRelation["leftSubsetOfRight"] = 2] = "leftSubsetOfRight";
	SubsetRelation[SubsetRelation["leftSupersetOfRight"] = 3] = "leftSupersetOfRight";
	SubsetRelation[SubsetRelation["unknown"] = 4] = "unknown";
	return SubsetRelation;
}(SubsetRelation || {});
function getSubsetRelation(left, right) {
	try {
		const inter = DFA.fromIntersection(left, right, new DFA.LimitedNodeFactory(MAX_DFA_NODES));
		inter.minimize();
		const l = DFA.fromFA(left, new DFA.LimitedNodeFactory(MAX_DFA_NODES));
		l.minimize();
		const r = DFA.fromFA(right, new DFA.LimitedNodeFactory(MAX_DFA_NODES));
		r.minimize();
		const subset = l.structurallyEqual(inter);
		const superset = r.structurallyEqual(inter);
		if (subset && superset) return SubsetRelation.leftEqualRight;
		else if (subset) return SubsetRelation.leftSubsetOfRight;
		else if (superset) return SubsetRelation.leftSupersetOfRight;
		return SubsetRelation.none;
	} catch {
		return SubsetRelation.unknown;
	}
}
/**
* The `getSubsetRelation` function assumes that both NFAs perfectly represent
* their language.
*
* This function adjusts their subset relation to account for partial NFAs.
*/
function getPartialSubsetRelation(left, leftIsPartial, right, rightIsPartial) {
	const relation = getSubsetRelation(left, right);
	if (!leftIsPartial && !rightIsPartial) return relation;
	if (relation === SubsetRelation.none || relation === SubsetRelation.unknown) return relation;
	if (leftIsPartial && !rightIsPartial) switch (relation) {
		case SubsetRelation.leftEqualRight: return SubsetRelation.leftSupersetOfRight;
		case SubsetRelation.leftSubsetOfRight: return SubsetRelation.none;
		case SubsetRelation.leftSupersetOfRight: return SubsetRelation.leftSupersetOfRight;
		default: return assertNever(relation);
	}
	if (rightIsPartial && !leftIsPartial) switch (relation) {
		case SubsetRelation.leftEqualRight: return SubsetRelation.leftSubsetOfRight;
		case SubsetRelation.leftSubsetOfRight: return SubsetRelation.leftSubsetOfRight;
		case SubsetRelation.leftSupersetOfRight: return SubsetRelation.none;
		default: return assertNever(relation);
	}
	return SubsetRelation.none;
}
/**
* Returns the regex source of the given FA.
*/
function faToSource(fa, flags) {
	try {
		assertValidFlags(flags);
		return JS.toLiteral(fa.toRegex(), { flags }).source;
	} catch {
		return "<ERROR>";
	}
}
/**
* Tries to find duplication in the given alternatives
*/
function* findDuplicationAstFast(alternatives, flags) {
	const shortCircuit = (a) => {
		return a.type === "CapturingGroup" ? false : null;
	};
	for (let i = 0; i < alternatives.length; i++) {
		const alternative = alternatives[i];
		for (let j = 0; j < i; j++) {
			const other = alternatives[j];
			if (isEqualNodes(other, alternative, flags, shortCircuit)) yield {
				type: "Duplicate",
				alternative,
				others: [other]
			};
		}
	}
}
/**
* Tries to find duplication in the given alternatives
*/
function* findDuplicationAst(alternatives, flags, hasNothingAfter) {
	const isCoveredOptions = {
		flags,
		canOmitRight: hasNothingAfter
	};
	const isCoveredOptionsNoPrefix = {
		flags,
		canOmitRight: false
	};
	for (let i = 0; i < alternatives.length; i++) {
		const alternative = alternatives[i];
		for (let j = 0; j < i; j++) {
			const other = alternatives[j];
			if (isCoveredNode(other, alternative, isCoveredOptions)) if (isEqualNodes(other, alternative, flags)) yield {
				type: "Duplicate",
				alternative,
				others: [other]
			};
			else if (hasNothingAfter && !isCoveredNode(other, alternative, isCoveredOptionsNoPrefix)) yield {
				type: "PrefixSubset",
				alternative,
				others: [other]
			};
			else yield {
				type: "Subset",
				alternative,
				others: [other]
			};
		}
	}
}
/**
* Tries to find duplication in the given alternatives.
*
* It will search for prefix duplications. I.e. the alternative `ab` in `a|ab`
* is a duplicate of `a` because if `ab` accepts, `a` will have already accepted
* the input string. This makes `ab` effectively useless.
*
* This operation will modify the given NFAs.
*/
function* findPrefixDuplicationNfa(alternatives, parser) {
	if (alternatives.length === 0) return;
	const all = NFA.all({ maxCharacter: alternatives[0][0].maxCharacter });
	for (let i = 0; i < alternatives.length; i++) {
		const [nfa, partial, alternative] = alternatives[i];
		if (!partial) {
			const overlapping = alternatives.slice(0, i).filter(([otherNfa]) => !isDisjointWith(nfa, otherNfa));
			if (overlapping.length >= 1) {
				const othersNfa = unionAll(overlapping.map(([n]) => n));
				const others = overlapping.map(([, , a]) => a);
				if (isSubsetOf(othersNfa, nfa)) yield {
					type: "PrefixSubset",
					alternative,
					others
				};
				else {
					const nested = tryFindNestedSubsetResult(overlapping.map((o) => [o[0], o[2]]), othersNfa, alternative, parser);
					if (nested) yield {
						...nested,
						type: "PrefixNestedSubset"
					};
				}
			}
		}
		nfa.append(all);
	}
}
/**
* Tries to find duplication in the given alternatives.
*/
function* findDuplicationNfa(alternatives, flags, { hasNothingAfter, parser, ignoreOverlap }) {
	const previous = [];
	for (let i = 0; i < alternatives.length; i++) {
		const alternative = alternatives[i];
		const { nfa, partial } = toNFA(parser, alternative);
		const overlapping = previous.filter(([otherNfa]) => !isDisjointWith(nfa, otherNfa));
		if (overlapping.length >= 1) {
			const othersNfa = unionAll(overlapping.map(([n]) => n));
			const othersPartial = overlapping.some(([, p]) => p);
			const others = overlapping.map(([, , a]) => a);
			const relation = getPartialSubsetRelation(nfa, partial, othersNfa, othersPartial);
			switch (relation) {
				case SubsetRelation.leftEqualRight:
					if (others.length === 1) yield {
						type: "Duplicate",
						alternative,
						others: [others[0]]
					};
					else yield {
						type: "Subset",
						alternative,
						others
					};
					break;
				case SubsetRelation.leftSubsetOfRight:
					yield {
						type: "Subset",
						alternative,
						others
					};
					break;
				case SubsetRelation.leftSupersetOfRight:
					if (canReorder([alternative, ...others], flags)) for (const other of others) yield {
						type: "Subset",
						alternative: other,
						others: [alternative]
					};
					else yield {
						type: "Superset",
						alternative,
						others
					};
					break;
				case SubsetRelation.none:
				case SubsetRelation.unknown: {
					const nested = tryFindNestedSubsetResult(overlapping.map((o) => [o[0], o[2]]), othersNfa, alternative, parser);
					if (nested) {
						yield nested;
						break;
					}
					if (!ignoreOverlap) yield {
						type: "Overlap",
						alternative,
						others,
						overlap: NFA.fromIntersection(nfa, othersNfa)
					};
					break;
				}
				default: throw assertNever(relation);
			}
		}
		previous.push([
			nfa,
			partial,
			alternative
		]);
	}
	if (hasNothingAfter) yield* findPrefixDuplicationNfa(previous, parser);
}
/**
* Given an alternative and list of overlapping other alternatives, this will
* try to find a nested alternative within the given alternative such that the
* nested alternative is a subset of the other alternatives.
*/
function tryFindNestedSubsetResult(others, othersNfa, alternative, parser) {
	const disjointElements = /* @__PURE__ */ new Set();
	for (const { nested, nfa: nestedNfa } of iteratePartialAlternatives(alternative, parser)) {
		if (hasSomeAncestor(nested, (a) => disjointElements.has(a))) continue;
		if (isDisjointWith(othersNfa, nestedNfa)) {
			disjointElements.add(nested);
			continue;
		}
		if (isSubsetOf(othersNfa, nestedNfa)) return {
			type: "NestedSubset",
			alternative,
			nested,
			others: others.filter((o) => !isDisjointWith(o[0], nestedNfa)).map((o) => o[1])
		};
	}
}
/**
* Tries to find duplication in the given alternatives
*/
function* findDuplication(alternatives, flags, options) {
	if (options.fastAst) yield* findDuplicationAstFast(alternatives, flags);
	else yield* findDuplicationAst(alternatives, flags, options.hasNothingAfter);
	if (!options.noNfa) yield* findDuplicationNfa(alternatives, flags, options);
}
const RESULT_TYPE_ORDER = [
	"Duplicate",
	"Subset",
	"NestedSubset",
	"PrefixSubset",
	"PrefixNestedSubset",
	"Superset",
	"Overlap"
];
/**
* Returns an array of the given results that is sorted by result type from
* most important to least important.
*/
function deduplicateResults(unsorted, { reportExp }) {
	const results = [...unsorted].sort((a, b) => RESULT_TYPE_ORDER.indexOf(a.type) - RESULT_TYPE_ORDER.indexOf(b.type));
	const seen = /* @__PURE__ */ new Map();
	return results.filter(({ alternative, type }) => {
		const firstSeen = seen.get(alternative);
		if (firstSeen === void 0) {
			seen.set(alternative, type);
			return true;
		}
		if (reportExp && firstSeen === "PrefixSubset" && type !== "PrefixSubset") {
			seen.set(alternative, type);
			return true;
		}
		return false;
	});
}
function mentionNested(nested) {
	if (nested.type === "Alternative" || nested.type === "StringAlternative") return mention(nested);
	return mentionChar(nested);
}
/**
* Returns a fix that removes the given alternative.
*/
function fixRemoveNestedAlternative(context, alternative) {
	switch (alternative.type) {
		case "Alternative": return fixRemoveAlternative(context, alternative);
		case "StringAlternative": return fixRemoveStringAlternative(context, alternative);
		case "Character":
		case "CharacterClassRange":
		case "CharacterSet":
		case "CharacterClass":
		case "ExpressionCharacterClass":
		case "ClassStringDisjunction":
			if (alternative.parent.type !== "CharacterClass") return () => null;
			return fixRemoveCharacterClassElement(context, alternative);
		default: throw assertNever(alternative);
	}
}
var ReportOption = /* @__PURE__ */ function(ReportOption) {
	ReportOption["all"] = "all";
	ReportOption["trivial"] = "trivial";
	ReportOption["interesting"] = "interesting";
	return ReportOption;
}(ReportOption || {});
var ReportExponentialBacktracking = /* @__PURE__ */ function(ReportExponentialBacktracking) {
	ReportExponentialBacktracking["none"] = "none";
	ReportExponentialBacktracking["certain"] = "certain";
	ReportExponentialBacktracking["potential"] = "potential";
	return ReportExponentialBacktracking;
}(ReportExponentialBacktracking || {});
var ReportUnreachable = /* @__PURE__ */ function(ReportUnreachable) {
	ReportUnreachable["certain"] = "certain";
	ReportUnreachable["potential"] = "potential";
	return ReportUnreachable;
}(ReportUnreachable || {});
var MaybeBool = /* @__PURE__ */ function(MaybeBool) {
	MaybeBool[MaybeBool["false"] = 0] = "false";
	MaybeBool[MaybeBool["true"] = 1] = "true";
	MaybeBool[MaybeBool["maybe"] = 2] = "maybe";
	return MaybeBool;
}(MaybeBool || {});
var no_dupe_disjunctions_default = createRule("no-dupe-disjunctions", {
	meta: {
		docs: {
			description: "disallow duplicate disjunctions",
			category: "Possible Errors",
			recommended: true
		},
		hasSuggestions: true,
		schema: [{
			type: "object",
			properties: {
				report: {
					type: "string",
					enum: [
						"all",
						"trivial",
						"interesting"
					]
				},
				reportExponentialBacktracking: { enum: [
					"none",
					"certain",
					"potential"
				] },
				reportUnreachable: { enum: ["certain", "potential"] }
			},
			additionalProperties: false
		}],
		messages: {
			duplicate: "Unexpected duplicate alternative. This alternative can be removed.{{cap}}{{exp}}",
			subset: "Unexpected useless alternative. This alternative is a strict subset of {{others}} and can be removed.{{cap}}{{exp}}",
			nestedSubset: "Unexpected useless element. All paths of {{root}} that go through {{nested}} are a strict subset of {{others}}. This element can be removed.{{cap}}{{exp}}",
			prefixSubset: "Unexpected useless alternative. This alternative is already covered by {{others}} and can be removed.{{cap}}",
			prefixNestedSubset: "Unexpected useless element. All paths of {{root}} that go through {{nested}} are already covered by {{others}}. This element can be removed.{{cap}}",
			superset: "Unexpected superset. This alternative is a superset of {{others}}. It might be possible to remove the other alternative(s).{{cap}}{{exp}}",
			overlap: "Unexpected overlap. This alternative overlaps with {{others}}. The overlap is {{expr}}.{{cap}}{{exp}}",
			remove: "Remove the {{alternative}} {{type}}.",
			replaceRange: "Replace {{range}} with {{replacement}}."
		},
		type: "suggestion"
	},
	create(context) {
		const reportExponentialBacktracking = context.options[0]?.reportExponentialBacktracking ?? ReportExponentialBacktracking.potential;
		const reportUnreachable = context.options[0]?.reportUnreachable ?? ReportUnreachable.certain;
		const report = context.options[0]?.report ?? ReportOption.trivial;
		const allowedRanges = getAllowedCharRanges(void 0, context);
		function createVisitor(regexpContext) {
			const { flags, node, getRegexpLocation, getUsageOfPattern } = regexpContext;
			const parser = getParser(regexpContext);
			/** Returns the filter information for the given node */
			function getFilterInfo(parentNode) {
				const usage = getUsageOfPattern();
				let stared;
				if (isStared(parentNode)) stared = MaybeBool.true;
				else if (usage === UsageOfPattern.partial || usage === UsageOfPattern.mixed) stared = MaybeBool.maybe;
				else stared = MaybeBool.false;
				let nothingAfter;
				if (!hasNothingAfterNode(parentNode)) nothingAfter = MaybeBool.false;
				else if (usage === UsageOfPattern.partial || usage === UsageOfPattern.mixed) nothingAfter = MaybeBool.maybe;
				else nothingAfter = MaybeBool.true;
				let reportExp;
				switch (reportExponentialBacktracking) {
					case ReportExponentialBacktracking.none:
						reportExp = false;
						break;
					case ReportExponentialBacktracking.certain:
						reportExp = stared === MaybeBool.true;
						break;
					case ReportExponentialBacktracking.potential:
						reportExp = stared !== MaybeBool.false;
						break;
					default: assertNever(reportExponentialBacktracking);
				}
				let reportPrefix;
				switch (reportUnreachable) {
					case ReportUnreachable.certain:
						reportPrefix = nothingAfter === MaybeBool.true;
						break;
					case ReportUnreachable.potential:
						reportPrefix = nothingAfter !== MaybeBool.false;
						break;
					default: assertNever(reportUnreachable);
				}
				return {
					stared,
					nothingAfter,
					reportExp,
					reportPrefix
				};
			}
			/** Verify group node */
			function verify(parentNode) {
				const info = getFilterInfo(parentNode);
				let results = filterResults([...findDuplication(parentNode.alternatives, flags, {
					fastAst: false,
					noNfa: false,
					ignoreOverlap: !info.reportExp && report !== ReportOption.all,
					hasNothingAfter: info.reportPrefix,
					parser
				})], info);
				results = deduplicateResults(results, info);
				results.forEach((result) => reportResult(result, info));
			}
			/** Filters the results of a parent node. */
			function filterResults(results, { nothingAfter, reportExp, reportPrefix }) {
				switch (report) {
					case ReportOption.all: return results;
					case ReportOption.trivial: return results.filter(({ type }) => {
						switch (type) {
							case "Duplicate":
							case "Subset":
							case "NestedSubset": return true;
							case "Overlap":
							case "Superset": return reportExp;
							case "PrefixSubset":
							case "PrefixNestedSubset": return reportPrefix;
							default: throw assertNever(type);
						}
					});
					case ReportOption.interesting: return results.filter(({ type }) => {
						switch (type) {
							case "Duplicate":
							case "Subset":
							case "NestedSubset": return true;
							case "Overlap": return reportExp;
							case "Superset": return reportExp || nothingAfter === MaybeBool.false;
							case "PrefixSubset":
							case "PrefixNestedSubset": return reportPrefix;
							default: throw assertNever(type);
						}
					});
					default: throw assertNever(report);
				}
			}
			function printChar(char) {
				if (inRange(allowedRanges, char)) return String.fromCodePoint(char);
				if (char === 0) return "\\0";
				if (char <= 255) return `\\x${char.toString(16).padStart(2, "0")}`;
				if (char <= 65535) return `\\u${char.toString(16).padStart(4, "0")}`;
				return `\\u{${char.toString(16)}}`;
			}
			function getSuggestions(result) {
				if (result.type === "Overlap" || result.type === "Superset") return [];
				const alternative = result.type === "NestedSubset" || result.type === "PrefixNestedSubset" ? result.nested : result.alternative;
				if (hasSomeDescendant(alternative, (d) => d.type === "CapturingGroup")) return [];
				if (alternative.type === "Character" && alternative.parent.type === "CharacterClassRange") {
					const range = alternative.parent;
					let replacement;
					if (range.min.value + 1 === range.max.value) replacement = range.min === alternative ? range.max.raw : range.min.raw;
					else if (range.min === alternative) replacement = `${printChar(range.min.value + 1)}-${range.max.raw}`;
					else {
						const max = printChar(range.max.value - 1);
						replacement = `${range.min.raw}-${max}`;
					}
					return [{
						messageId: "replaceRange",
						data: {
							range: mentionChar(range),
							replacement: mention(replacement)
						},
						fix: regexpContext.fixReplaceNode(range, replacement)
					}];
				}
				return [{
					messageId: "remove",
					data: {
						alternative: mentionNested(alternative),
						type: alternative.type === "Alternative" ? "alternative" : "element"
					},
					fix: fixRemoveNestedAlternative(regexpContext, alternative)
				}];
			}
			function reportResult(result, { stared }) {
				let exp;
				if (stared === MaybeBool.true) exp = " This ambiguity is likely to cause exponential backtracking.";
				else if (stared === MaybeBool.maybe) exp = " This ambiguity might cause exponential backtracking.";
				else exp = "";
				const reportAlternative = result.type === "NestedSubset" || result.type === "PrefixNestedSubset" ? result.nested : result.alternative;
				const loc = getRegexpLocation(reportAlternative);
				const cap = hasSomeDescendant(reportAlternative, (d) => d.type === "CapturingGroup") ? " Careful! This alternative contains capturing groups which might be difficult to remove." : "";
				const others = mention(result.others.map((a) => a.raw).join("|"));
				const suggest = getSuggestions(result);
				switch (result.type) {
					case "Duplicate":
						context.report({
							node,
							loc,
							messageId: "duplicate",
							data: {
								exp,
								cap,
								others
							},
							suggest
						});
						break;
					case "Subset":
						context.report({
							node,
							loc,
							messageId: "subset",
							data: {
								exp,
								cap,
								others
							},
							suggest
						});
						break;
					case "NestedSubset":
						context.report({
							node,
							loc,
							messageId: "nestedSubset",
							data: {
								exp,
								cap,
								others,
								root: mention(result.alternative),
								nested: mentionNested(result.nested)
							},
							suggest
						});
						break;
					case "PrefixSubset":
						context.report({
							node,
							loc,
							messageId: "prefixSubset",
							data: {
								exp,
								cap,
								others
							},
							suggest
						});
						break;
					case "PrefixNestedSubset":
						context.report({
							node,
							loc,
							messageId: "prefixNestedSubset",
							data: {
								exp,
								cap,
								others,
								root: mention(result.alternative),
								nested: mentionNested(result.nested)
							},
							suggest
						});
						break;
					case "Superset":
						context.report({
							node,
							loc,
							messageId: "superset",
							data: {
								exp,
								cap,
								others
							},
							suggest
						});
						break;
					case "Overlap":
						context.report({
							node,
							loc,
							messageId: "overlap",
							data: {
								exp,
								cap,
								others,
								expr: mention(faToSource(result.overlap, flags))
							},
							suggest
						});
						break;
					default: throw assertNever(result);
				}
			}
			return {
				onPatternEnter: verify,
				onGroupEnter: verify,
				onCapturingGroupEnter: verify,
				onAssertionEnter(aNode) {
					if (aNode.kind === "lookahead" || aNode.kind === "lookbehind") verify(aNode);
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-empty-alternative.ts
/**
* Returns the source before and after the alternatives of the given capturing group.
*/
function getCapturingGroupOuterSource(node) {
	const first = node.alternatives[0];
	const last = node.alternatives[node.alternatives.length - 1];
	const innerStart = first.start - node.start;
	const innerEnd = last.end - node.start;
	return [node.raw.slice(0, innerStart), node.raw.slice(innerEnd)];
}
function getFixedNode(regexpNode, alt) {
	let quant;
	if (regexpNode.alternatives.at(0) === alt) quant = "??";
	else if (regexpNode.alternatives.at(-1) === alt) quant = "?";
	else return null;
	let replacement = `(?:${regexpNode.alternatives.filter((a) => a !== alt).map((a) => a.raw).join("|")})${quant}`;
	if (regexpNode.type === "CapturingGroup") {
		const [before, after] = getCapturingGroupOuterSource(regexpNode);
		replacement = `${before}${replacement}${after}`;
	} else if (regexpNode.parent?.type === "Quantifier") replacement = `(?:${replacement})`;
	return replacement;
}
var no_empty_alternative_default = createRule("no-empty-alternative", {
	meta: {
		docs: {
			description: "disallow alternatives without elements",
			category: "Possible Errors",
			recommended: true,
			default: "warn"
		},
		schema: [],
		hasSuggestions: true,
		messages: {
			empty: "This empty alternative might be a mistake. If not, use a quantifier instead.",
			suggest: "Use a quantifier instead."
		},
		type: "problem"
	},
	create(context) {
		function createVisitor({ node, getRegexpLocation, fixReplaceNode }) {
			function verifyAlternatives(regexpNode, suggestFixer) {
				if (regexpNode.alternatives.length >= 2) for (let i = 0; i < regexpNode.alternatives.length; i++) {
					const alt = regexpNode.alternatives[i];
					const isLast = i === regexpNode.alternatives.length - 1;
					if (alt.elements.length === 0) {
						const index = alt.start;
						const loc = isLast ? getRegexpLocation({
							start: index - 1,
							end: index
						}) : getRegexpLocation({
							start: index,
							end: index + 1
						});
						const fixed = suggestFixer(alt);
						context.report({
							node,
							loc,
							messageId: "empty",
							suggest: fixed ? [{
								messageId: "suggest",
								fix: fixReplaceNode(regexpNode, fixed)
							}] : void 0
						});
						return;
					}
				}
			}
			return {
				onGroupEnter: (gNode) => verifyAlternatives(gNode, (alt) => getFixedNode(gNode, alt)),
				onCapturingGroupEnter: (cgNode) => verifyAlternatives(cgNode, (alt) => getFixedNode(cgNode, alt)),
				onPatternEnter: (pNode) => verifyAlternatives(pNode, (alt) => getFixedNode(pNode, alt)),
				onClassStringDisjunctionEnter: (csdNode) => verifyAlternatives(csdNode, () => null)
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-empty-capturing-group.ts
var no_empty_capturing_group_default = createRule("no-empty-capturing-group", {
	meta: {
		docs: {
			description: "disallow capturing group that captures empty.",
			category: "Possible Errors",
			recommended: true
		},
		schema: [],
		messages: { unexpected: "Unexpected capture empty." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, flags, getRegexpLocation }) {
			return { onCapturingGroupEnter(cgNode) {
				if (isZeroLength(cgNode, flags)) context.report({
					node,
					loc: getRegexpLocation(cgNode),
					messageId: "unexpected"
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-empty-character-class.ts
var no_empty_character_class_default = createRule("no-empty-character-class", {
	meta: {
		docs: {
			description: "disallow character classes that match no characters",
			category: "Possible Errors",
			recommended: true
		},
		schema: [],
		messages: {
			empty: "This character class matches no characters because it is empty.",
			cannotMatchAny: "This character class cannot match any characters."
		},
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, getRegexpLocation, flags } = regexpContext;
			return {
				onCharacterClassEnter(ccNode) {
					if (matchesNoCharacters(ccNode, flags)) context.report({
						node,
						loc: getRegexpLocation(ccNode),
						messageId: ccNode.elements.length ? "cannotMatchAny" : "empty"
					});
				},
				onExpressionCharacterClassEnter(ccNode) {
					if (matchesNoCharacters(ccNode, flags)) context.report({
						node,
						loc: getRegexpLocation(ccNode),
						messageId: "cannotMatchAny"
					});
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-empty-group.ts
var no_empty_group_default = createRule("no-empty-group", {
	meta: {
		docs: {
			description: "disallow empty group",
			category: "Possible Errors",
			recommended: true
		},
		schema: [],
		messages: { unexpected: "Unexpected empty group." },
		type: "suggestion"
	},
	create(context) {
		function verifyGroup({ node, getRegexpLocation }, gNode) {
			if (gNode.alternatives.every((alt) => alt.elements.length === 0)) context.report({
				node,
				loc: getRegexpLocation(gNode),
				messageId: "unexpected"
			});
		}
		function createVisitor(regexpContext) {
			return {
				onGroupEnter(gNode) {
					verifyGroup(regexpContext, gNode);
				},
				onCapturingGroupEnter(cgNode) {
					verifyGroup(regexpContext, cgNode);
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-empty-lookarounds-assertion.ts
var no_empty_lookarounds_assertion_default = createRule("no-empty-lookarounds-assertion", {
	meta: {
		docs: {
			description: "disallow empty lookahead assertion or empty lookbehind assertion",
			category: "Possible Errors",
			recommended: true
		},
		schema: [],
		messages: { unexpected: "Unexpected empty {{kind}}. It will trivially {{result}} all inputs." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, flags, getRegexpLocation }) {
			return { onAssertionEnter(aNode) {
				if (aNode.kind !== "lookahead" && aNode.kind !== "lookbehind") return;
				if (isPotentiallyEmpty(aNode.alternatives, flags)) context.report({
					node,
					loc: getRegexpLocation(aNode),
					messageId: "unexpected",
					data: {
						kind: aNode.kind,
						result: aNode.negate ? "reject" : "accept"
					}
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-empty-string-literal.ts
var no_empty_string_literal_default = createRule("no-empty-string-literal", {
	meta: {
		docs: {
			description: "disallow empty string literals in character classes",
			category: "Best Practices",
			recommended: true
		},
		schema: [],
		messages: { unexpected: "Unexpected empty string literal." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, getRegexpLocation } = regexpContext;
			return { onClassStringDisjunctionEnter(csdNode) {
				if (csdNode.alternatives.every((alt) => alt.elements.length === 0)) context.report({
					node,
					loc: getRegexpLocation(csdNode),
					messageId: "unexpected"
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-escape-backspace.ts
var no_escape_backspace_default = createRule("no-escape-backspace", {
	meta: {
		docs: {
			description: "disallow escape backspace (`[\\b]`)",
			category: "Possible Errors",
			recommended: true
		},
		schema: [],
		hasSuggestions: true,
		messages: {
			unexpected: "Unexpected '[\\b]'. Use '\\u0008' instead.",
			suggest: "Use '\\u0008'."
		},
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, getRegexpLocation, fixReplaceNode }) {
			return { onCharacterEnter(cNode) {
				if (cNode.value === 8 && cNode.raw === "\\b") context.report({
					node,
					loc: getRegexpLocation(cNode),
					messageId: "unexpected",
					suggest: [{
						messageId: "suggest",
						fix: fixReplaceNode(cNode, "\\u0008")
					}]
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-extra-lookaround-assertions.ts
var no_extra_lookaround_assertions_default = createRule("no-extra-lookaround-assertions", {
	meta: {
		docs: {
			description: "disallow unnecessary nested lookaround assertions",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: {
			canBeInlined: "This {{kind}} assertion is useless and can be inlined.",
			canBeConvertedIntoGroup: "This {{kind}} assertion is useless and can be converted into a group."
		},
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			return { onAssertionEnter(aNode) {
				if (aNode.kind === "lookahead" || aNode.kind === "lookbehind") verify(regexpContext, aNode);
			} };
		}
		function verify(regexpContext, assertion) {
			for (const alternative of assertion.alternatives) {
				const nested = alternative.elements.at(assertion.kind === "lookahead" ? -1 : 0);
				if (nested?.type === "Assertion" && nested.kind === assertion.kind && !nested.negate) reportLookaroundAssertion(regexpContext, nested);
			}
		}
		function reportLookaroundAssertion({ node, getRegexpLocation, fixReplaceNode }, assertion) {
			let messageId, replaceText;
			if (assertion.alternatives.length === 1) {
				messageId = "canBeInlined";
				replaceText = assertion.alternatives[0].raw;
			} else {
				messageId = "canBeConvertedIntoGroup";
				replaceText = `(?:${assertion.alternatives.map((alt) => alt.raw).join("|")})`;
			}
			context.report({
				node,
				loc: getRegexpLocation(assertion),
				messageId,
				data: { kind: assertion.kind },
				fix: fixReplaceNode(assertion, replaceText)
			});
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-invalid-regexp.ts
/** Returns the position of the error */
function getErrorIndex(error) {
	const index = error.index;
	if (typeof index === "number") return index;
	return null;
}
var no_invalid_regexp_default = createRule("no-invalid-regexp", {
	meta: {
		docs: {
			description: "disallow invalid regular expression strings in `RegExp` constructors",
			category: "Possible Errors",
			recommended: true
		},
		schema: [],
		messages: {
			error: "{{message}}",
			duplicateFlag: "Duplicate {{flag}} flag.",
			uvFlag: "Regex 'u' and 'v' flags cannot be used together."
		},
		type: "problem"
	},
	create(context) {
		function visitInvalid(regexpContext) {
			const { node, error, patternSource } = regexpContext;
			let loc = void 0;
			const index = getErrorIndex(error);
			if (index !== null && index >= 0 && index <= patternSource.value.length) loc = patternSource.getAstLocation({
				start: Math.max(index - 1, 0),
				end: Math.min(index + 1, patternSource.value.length)
			});
			context.report({
				node,
				loc: loc ?? void 0,
				messageId: "error",
				data: { message: error.message }
			});
		}
		/** Checks for the combination of `u` and `v` flags */
		function visitUnknown(regexpContext) {
			const { node, flags, flagsString, getFlagsLocation } = regexpContext;
			const flagSet = /* @__PURE__ */ new Set();
			for (const flag of flagsString ?? "") {
				if (flagSet.has(flag)) {
					context.report({
						node,
						loc: getFlagsLocation(),
						messageId: "duplicateFlag",
						data: { flag }
					});
					return;
				}
				flagSet.add(flag);
			}
			if (flags.unicode && flags.unicodeSets) context.report({
				node,
				loc: getFlagsLocation(),
				messageId: "uvFlag"
			});
		}
		return defineRegexpVisitor(context, {
			visitInvalid,
			visitUnknown
		});
	}
});
//#endregion
//#region lib/rules/no-invisible-character.ts
var no_invisible_character_default = createRule("no-invisible-character", {
	meta: {
		docs: {
			description: "disallow invisible raw character",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { unexpected: "Unexpected invisible character. Use '{{instead}}' instead." },
		type: "suggestion"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		function createLiteralVisitor({ node, flags, getRegexpLocation, fixReplaceNode }) {
			return { onCharacterEnter(cNode) {
				if (cNode.raw === " ") return;
				if (cNode.raw.length === 1 && isInvisible(cNode.value)) {
					const instead = toCharSetSource(cNode.value, flags);
					context.report({
						node,
						loc: getRegexpLocation(cNode),
						messageId: "unexpected",
						data: { instead },
						fix: fixReplaceNode(cNode, instead)
					});
				}
			} };
		}
		/**
		* Verify a given string literal.
		*/
		function verifyString({ node, flags }) {
			const text = sourceCode.getText(node);
			let index = 0;
			for (const c of text) {
				if (c === " ") continue;
				const cp = c.codePointAt(0);
				if (isInvisible(cp)) {
					const instead = toCharSetSource(cp, flags);
					const range = [node.range[0] + index, node.range[0] + index + c.length];
					context.report({
						node,
						loc: {
							start: sourceCode.getLocFromIndex(range[0]),
							end: sourceCode.getLocFromIndex(range[1])
						},
						messageId: "unexpected",
						data: { instead },
						fix(fixer) {
							return fixer.replaceTextRange(range, instead);
						}
					});
				}
				index += c.length;
			}
		}
		return defineRegexpVisitor(context, {
			createLiteralVisitor,
			createSourceVisitor(regexpContext) {
				if (regexpContext.node.type === "Literal") verifyString(regexpContext);
				return {};
			}
		});
	}
});
//#endregion
//#region lib/rules/no-lazy-ends.ts
function* extractLazyEndQuantifiers(alternatives) {
	for (const { elements } of alternatives) if (elements.length > 0) {
		const last = elements[elements.length - 1];
		switch (last.type) {
			case "Quantifier":
				if (!last.greedy && last.min !== last.max) yield last;
				else if (last.max === 1) {
					const element = last.element;
					if (element.type === "Group" || element.type === "CapturingGroup") yield* extractLazyEndQuantifiers(element.alternatives);
				}
				break;
			case "CapturingGroup":
			case "Group":
				yield* extractLazyEndQuantifiers(last.alternatives);
				break;
			default: break;
		}
	}
}
var no_lazy_ends_default = createRule("no-lazy-ends", {
	meta: {
		docs: {
			description: "disallow lazy quantifiers at the end of an expression",
			category: "Possible Errors",
			recommended: true,
			default: "warn"
		},
		schema: [{
			type: "object",
			properties: { ignorePartial: { type: "boolean" } },
			additionalProperties: false
		}],
		hasSuggestions: true,
		messages: {
			uselessElement: "The quantifier and the quantified element can be removed because the quantifier is lazy and has a minimum of 0.",
			uselessQuantifier: "The quantifier can be removed because the quantifier is lazy and has a minimum of 1.",
			uselessRange: "The quantifier can be replaced with '{{{min}}}' because the quantifier is lazy and has a minimum of {{min}}.",
			suggestMakeGreedy: "Make the quantifier greedy. (This changes the behavior of the regex.)",
			suggestRemoveElement: "Remove the quantified element. (This does not changes the behavior of the regex.)",
			suggestRemoveQuantifier: "Remove the quantifier. (This does not changes the behavior of the regex.)",
			suggestRange: "Replace the quantifier with '{{{min}}}'. (This does not changes the behavior of the regex.)"
		},
		type: "problem"
	},
	create(context) {
		const ignorePartial = context.options[0]?.ignorePartial ?? true;
		function createVisitor({ node, getRegexpLocation, getUsageOfPattern, fixReplaceNode }) {
			if (ignorePartial) {
				if (getUsageOfPattern() !== UsageOfPattern.whole) return {};
			}
			return { onPatternEnter(pNode) {
				for (const lazy of extractLazyEndQuantifiers(pNode.alternatives)) {
					const makeGreedy = {
						messageId: "suggestMakeGreedy",
						fix: fixReplaceNode(lazy, lazy.raw.slice(0, -1))
					};
					if (lazy.min === 0) {
						const replacement = pNode.alternatives.length === 1 && pNode.alternatives[0].elements.length === 1 && pNode.alternatives[0].elements[0] === lazy ? "(?:)" : "";
						context.report({
							node,
							loc: getRegexpLocation(lazy),
							messageId: "uselessElement",
							suggest: [{
								messageId: "suggestRemoveElement",
								fix: fixReplaceNode(lazy, replacement)
							}, makeGreedy]
						});
					} else if (lazy.min === 1) context.report({
						node,
						loc: getRegexpLocation(lazy),
						messageId: "uselessQuantifier",
						suggest: [{
							messageId: "suggestRemoveQuantifier",
							fix: fixReplaceNode(lazy, lazy.element.raw)
						}, makeGreedy]
					});
					else context.report({
						node,
						loc: getRegexpLocation(lazy),
						messageId: "uselessRange",
						data: { min: String(lazy.min) },
						suggest: [{
							messageId: "suggestRange",
							data: { min: String(lazy.min) },
							fix: fixReplaceNode(lazy, `${lazy.element.raw}{${lazy.min}}`)
						}, makeGreedy]
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-legacy-features.ts
const STATIC_PROPERTIES = [
	"input",
	"$_",
	"lastMatch",
	"$&",
	"lastParen",
	"$+",
	"leftContext",
	"$`",
	"rightContext",
	"$'",
	"$1",
	"$2",
	"$3",
	"$4",
	"$5",
	"$6",
	"$7",
	"$8",
	"$9"
];
const PROTOTYPE_METHODS = ["compile"];
var no_legacy_features_default = createRule("no-legacy-features", {
	meta: {
		docs: {
			description: "disallow legacy RegExp features",
			category: "Best Practices",
			recommended: true
		},
		schema: [{
			type: "object",
			properties: {
				staticProperties: {
					type: "array",
					items: { enum: STATIC_PROPERTIES },
					uniqueItems: true
				},
				prototypeMethods: {
					type: "array",
					items: { enum: PROTOTYPE_METHODS },
					uniqueItems: true
				}
			},
			additionalProperties: false
		}],
		messages: {
			forbiddenStaticProperty: "'{{name}}' static property is forbidden.",
			forbiddenPrototypeMethods: "RegExp.prototype.{{name}} method is forbidden."
		},
		type: "suggestion"
	},
	create(context) {
		const staticProperties = context.options[0]?.staticProperties ?? STATIC_PROPERTIES;
		const prototypeMethods = context.options[0]?.prototypeMethods ?? PROTOTYPE_METHODS;
		const typeTracer = createTypeTracker(context);
		return {
			...staticProperties.length ? { Program(program) {
				const tracker = new ReferenceTracker(context.sourceCode.getScope(program));
				const regexpTraceMap = {};
				for (const sp of staticProperties) regexpTraceMap[sp] = { [READ]: true };
				for (const { node, path } of tracker.iterateGlobalReferences({ RegExp: regexpTraceMap })) context.report({
					node,
					messageId: "forbiddenStaticProperty",
					data: { name: path.join(".") }
				});
			} } : {},
			...prototypeMethods.length ? { MemberExpression(node) {
				if (node.computed || node.property.type !== "Identifier" || !prototypeMethods.includes(node.property.name) || node.object.type === "Super") return;
				if (typeTracer.isRegExp(node.object)) context.report({
					node,
					messageId: "forbiddenPrototypeMethods",
					data: { name: node.property.name }
				});
			} } : {}
		};
	}
});
//#endregion
//#region lib/utils/fix-simplify-quantifier.ts
/**
* Returns a fixer to simplify the given quantifier.
*/
function fixSimplifyQuantifier(quantifier, result, { fixReplaceNode }) {
	const ancestor = getClosestAncestor(quantifier, ...result.dependencies);
	let replacement;
	if (quantifier.min === 0) replacement = "";
	else if (quantifier.min === 1) replacement = quantifier.element.raw;
	else replacement = quantifier.element.raw + quantToString({
		min: quantifier.min,
		max: quantifier.min,
		greedy: true
	});
	return [replacement, fixReplaceNode(ancestor, () => {
		return ancestor.raw.slice(0, quantifier.start - ancestor.start) + replacement + ancestor.raw.slice(quantifier.end - ancestor.start);
	})];
}
//#endregion
//#region lib/rules/no-misleading-capturing-group.ts
/**
* Returns all quantifiers that are always at the start of the given element.
*/
function* getStartQuantifiers(root, direction, flags) {
	if (Array.isArray(root)) {
		for (const a of root) yield* getStartQuantifiers(a, direction, flags);
		return;
	}
	switch (root.type) {
		case "Character":
		case "CharacterClass":
		case "CharacterSet":
		case "ExpressionCharacterClass":
		case "Backreference": break;
		case "Assertion": break;
		case "Alternative": {
			const elements = direction === "ltr" ? root.elements : reversed(root.elements);
			for (const e of elements) {
				if (isEmpty(e, flags)) continue;
				yield* getStartQuantifiers(e, direction, flags);
				break;
			}
			break;
		}
		case "CapturingGroup": break;
		case "Group":
			yield* getStartQuantifiers(root.alternatives, direction, flags);
			break;
		case "Quantifier":
			yield root;
			if (root.max === 1) yield* getStartQuantifiers(root.element, direction, flags);
			break;
		default: yield assertNever(root);
	}
}
const getCache = cachedFn((_flags) => /* @__PURE__ */ new WeakMap());
/**
* Returns the largest character set such that `L(chars) ⊆ L(element)`.
*/
function getSingleRepeatedChar(element, flags, cache = getCache(flags)) {
	let value = cache.get(element);
	if (value === void 0) {
		value = uncachedGetSingleRepeatedChar(element, flags, cache);
		cache.set(element, value);
	}
	return value;
}
/**
* Returns the largest character set such that `L(chars) ⊆ L(element)`.
*/
function uncachedGetSingleRepeatedChar(element, flags, cache) {
	switch (element.type) {
		case "Alternative": {
			let total = void 0;
			for (const e of element.elements) {
				const c = getSingleRepeatedChar(e, flags, cache);
				if (total === void 0) total = c;
				else total = total.intersect(c);
				if (total.isEmpty) return total;
			}
			return total ?? Chars.empty(flags);
		}
		case "Assertion": return Chars.empty(flags);
		case "Backreference": return Chars.empty(flags);
		case "Character":
		case "CharacterClass":
		case "CharacterSet":
		case "ExpressionCharacterClass": {
			const set = toUnicodeSet(element, flags);
			if (set.accept.isEmpty) return set.chars;
			return set.wordSets.map((wordSet) => {
				let total = void 0;
				for (const c of wordSet) {
					if (total === void 0) total = c;
					else total = total.intersect(c);
					if (total.isEmpty) return total;
				}
				return total ?? Chars.empty(flags);
			}).reduce((a, b) => a.union(b));
		}
		case "CapturingGroup":
		case "Group": return element.alternatives.map((a) => getSingleRepeatedChar(a, flags, cache)).reduce((a, b) => a.union(b));
		case "Quantifier":
			if (element.max === 0) return Chars.empty(flags);
			return getSingleRepeatedChar(element.element, flags, cache);
		default: return assertNever(element);
	}
}
/**
* Yields all non-constant (min != max) quantifiers that trade characters with
* the given start quantifiers.
*/
function getTradingQuantifiersAfter(start, startChar, direction, flags) {
	const results = [];
	followPaths(start, "next", startChar, {
		join(states) {
			return CharSet.empty(startChar.maximum).union(...states);
		},
		continueAfter(_, state) {
			return !state.isEmpty;
		},
		continueInto(element, state) {
			return element.type !== "Assertion" && !state.isEmpty;
		},
		leave(element, state) {
			switch (element.type) {
				case "Assertion":
				case "Backreference":
				case "Character":
				case "CharacterClass":
				case "CharacterSet":
				case "ExpressionCharacterClass": return state.intersect(getSingleRepeatedChar(element, flags));
				case "CapturingGroup":
				case "Group":
				case "Quantifier": return state;
				default: return assertNever(element);
			}
		},
		enter(element, state) {
			if (element.type === "Quantifier" && element.min !== element.max) {
				const qChar = getSingleRepeatedChar(element, flags);
				const intersection = qChar.intersect(state);
				if (!intersection.isEmpty) results.push({
					quant: element,
					quantRepeatedChar: qChar,
					intersection
				});
			}
			return state;
		}
	}, direction);
	return results;
}
var no_misleading_capturing_group_default = createRule("no-misleading-capturing-group", {
	meta: {
		docs: {
			description: "disallow capturing groups that do not behave as one would expect",
			category: "Possible Errors",
			recommended: true
		},
		hasSuggestions: true,
		schema: [{
			type: "object",
			properties: { reportBacktrackingEnds: { type: "boolean" } },
			additionalProperties: false
		}],
		messages: {
			removeQuant: "{{quant}} can be removed because it is already included by {{cause}}. This makes the capturing group misleading, because it actually captures less text than its pattern suggests.",
			replaceQuant: "{{quant}} can be replaced with {{fix}} because of {{cause}}. This makes the capturing group misleading, because it actually captures less text than its pattern suggests.",
			suggestionRemove: "Remove {{quant}}.",
			suggestionReplace: "Replace {{quant}} with {{fix}}.",
			nonAtomic: "The quantifier {{quant}} is not atomic for the characters {{chars}}, so it might capture fewer characters than expected. This makes the capturing group misleading, because the quantifier will capture fewer characters than its pattern suggests in some edge cases.",
			suggestionNonAtomic: "Make the quantifier atomic by adding {{fix}}. Careful! This is going to change the behavior of the regex in some edge cases.",
			trading: "The quantifier {{quant}} can exchange characters ({{chars}}) with {{other}}. This makes the capturing group misleading, because the quantifier will capture fewer characters than its pattern suggests."
		},
		type: "problem"
	},
	create(context) {
		const reportBacktrackingEnds = context.options[0]?.reportBacktrackingEnds ?? true;
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation } = regexpContext;
			const parser = getParser(regexpContext);
			/**
			* Reports all quantifiers at the start of the given capturing
			* groups that can be simplified.
			*/
			function reportStartQuantifiers(capturingGroup) {
				const direction = getMatchingDirection(capturingGroup);
				const startQuantifiers = getStartQuantifiers(capturingGroup.alternatives, direction, flags);
				for (const quantifier of startQuantifiers) {
					const result = canSimplifyQuantifier(quantifier, flags, parser);
					if (!result.canSimplify) return;
					const cause = joinEnglishList(result.dependencies.map((d) => mention(d)));
					const [replacement, fix] = fixSimplifyQuantifier(quantifier, result, regexpContext);
					if (quantifier.min === 0) {
						const removesCapturingGroup = hasCapturingGroup(quantifier);
						context.report({
							node,
							loc: getRegexpLocation(quantifier),
							messageId: "removeQuant",
							data: {
								quant: mention(quantifier),
								cause
							},
							suggest: removesCapturingGroup ? void 0 : [{
								messageId: "suggestionRemove",
								data: { quant: mention(quantifier) },
								fix
							}]
						});
					} else context.report({
						node,
						loc: getRegexpLocation(quantifier),
						messageId: "replaceQuant",
						data: {
							quant: mention(quantifier),
							fix: mention(replacement),
							cause
						},
						suggest: [{
							messageId: "suggestionReplace",
							data: {
								quant: mention(quantifier),
								fix: mention(replacement)
							},
							fix
						}]
					});
				}
			}
			/**
			* Quantifiers at the end of the a capturing groups that can
			* exchange characters with another quantifier outside the capturing group.
			*/
			function reportTradingEndQuantifiers(capturingGroup) {
				const direction = getMatchingDirection(capturingGroup);
				const endQuantifiers = getStartQuantifiers(capturingGroup.alternatives, invertMatchingDirection(direction), flags);
				for (const quantifier of endQuantifiers) {
					if (!quantifier.greedy) continue;
					if (quantifier.min === quantifier.max) continue;
					const qChar = getSingleRepeatedChar(quantifier, flags);
					if (qChar.isEmpty) continue;
					for (const trader of getTradingQuantifiersAfter(quantifier, qChar, direction, flags)) {
						if (hasSomeDescendant(capturingGroup, trader.quant)) continue;
						if (trader.quant.min >= 1 && !isPotentiallyZeroLength(trader.quant.element, flags)) context.report({
							node,
							loc: getRegexpLocation(quantifier),
							messageId: "trading",
							data: {
								quant: mention(quantifier),
								other: mention(trader.quant),
								chars: toCharSetSource(trader.intersection, flags)
							}
						});
					}
				}
			}
			return { onCapturingGroupLeave(capturingGroup) {
				reportStartQuantifiers(capturingGroup);
				if (reportBacktrackingEnds) reportTradingEndQuantifiers(capturingGroup);
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-misleading-unicode-character.ts
const segmenter = new Intl.Segmenter();
/** Returns whether the given string starts with a valid surrogate pair. */
function startsWithSurrogate(s) {
	if (s.length < 2) return false;
	const h = s.charCodeAt(0);
	const l = s.charCodeAt(1);
	return h >= 55296 && h <= 56319 && l >= 56320 && l <= 57343;
}
/**
* Returns the problem (if any) with the given grapheme.
*/
function getProblem(grapheme, flags) {
	if (grapheme.length > 2 || grapheme.length === 2 && !startsWithSurrogate(grapheme)) return "Multi";
	else if (!flags.unicode && !flags.unicodeSets && startsWithSurrogate(grapheme)) return "Surrogate";
	return null;
}
/** Returns the last grapheme of the quantified element. */
function getGraphemeBeforeQuant(quant) {
	const alt = quant.parent;
	let start = quant.start;
	for (let i = alt.elements.indexOf(quant) - 1; i >= 0; i--) {
		const e = alt.elements[i];
		if (e.type === "Character" && !isEscapeSequence(e.raw)) start = e.start;
		else break;
	}
	const before = alt.raw.slice(start - alt.start, quant.element.end - alt.start);
	const segments = [...segmenter.segment(before)];
	return segments[segments.length - 1].segment;
}
/** Returns all grapheme problem in the given character class. */
function getGraphemeProblems(cc, flags) {
	const offset = cc.negate ? 2 : 1;
	const ignoreElements = cc.elements.filter((element) => element.type === "CharacterClass" || element.type === "ExpressionCharacterClass" || element.type === "ClassStringDisjunction");
	const problems = [];
	for (const { segment, index } of segmenter.segment(cc.raw.slice(offset, -1))) {
		const problem = getProblem(segment, flags);
		if (problem !== null) {
			const start = offset + index + cc.start;
			const end = start + segment.length;
			if (ignoreElements.some((ignore) => ignore.start <= start && end <= ignore.end)) continue;
			problems.push({
				grapheme: segment,
				problem,
				start,
				end,
				elements: cc.elements.filter((e) => e.start < end && e.end > start)
			});
		}
	}
	return problems;
}
/** Returns a fix for the given problems (if possible). */
function getGraphemeProblemsFix(problems, cc, flags) {
	if (cc.negate) return null;
	if (!problems.every((p) => p.start === p.elements[0].start && p.end === p.elements[p.elements.length - 1].end)) return null;
	const prefixGraphemes = problems.map((p) => p.grapheme);
	let ccRaw = cc.raw;
	for (let i = problems.length - 1; i >= 0; i--) {
		const { start, end } = problems[i];
		ccRaw = ccRaw.slice(0, start - cc.start) + ccRaw.slice(end - cc.start);
	}
	if (flags.unicodeSets) return `[\\q{${prefixGraphemes.join("|")}}${ccRaw.slice(1, -1)}]`;
	if (ccRaw.startsWith("[^")) ccRaw = `[\\${ccRaw.slice(1)}`;
	let fix = prefixGraphemes.sort((a, b) => b.length - a.length).join("|");
	let singleAlternative = problems.length === 1;
	if (ccRaw !== "[]") {
		fix += `|${ccRaw}`;
		singleAlternative = false;
	}
	if (singleAlternative && cc.parent.type === "Alternative") return fix;
	if (cc.parent.type === "Alternative" && cc.parent.elements.length === 1) return fix;
	return `(?:${fix})`;
}
var no_misleading_unicode_character_default = createRule("no-misleading-unicode-character", {
	meta: {
		docs: {
			description: "disallow multi-code-point characters in character classes and quantifiers",
			category: "Possible Errors",
			recommended: true
		},
		schema: [{
			type: "object",
			properties: { fixable: { type: "boolean" } },
			additionalProperties: false
		}],
		fixable: "code",
		hasSuggestions: true,
		messages: {
			characterClass: "The character(s) {{ graphemes }} are all represented using multiple {{ unit }}.{{ uFlag }}",
			quantifierMulti: "The character {{ grapheme }} is represented using multiple Unicode code points. The quantifier only applies to the last code point {{ last }} and not to the whole character.",
			quantifierSurrogate: "The character {{ grapheme }} is represented using a surrogate pair. The quantifier only applies to the tailing surrogate {{ last }} and not to the whole character.",
			fixCharacterClass: "Move the character(s) {{ graphemes }} outside the character class.",
			fixQuantifier: "Wrap a group around {{ grapheme }}."
		},
		type: "problem"
	},
	create(context) {
		const fixable = context.options[0]?.fixable ?? false;
		function makeFix(fix, messageId, data) {
			if (fixable) return { fix };
			return { suggest: [{
				messageId,
				data,
				fix
			}] };
		}
		function createVisitor(regexpContext) {
			const { node, patternSource, flags, getRegexpLocation, fixReplaceNode } = regexpContext;
			return {
				onCharacterClassEnter(ccNode) {
					const problems = getGraphemeProblems(ccNode, flags);
					if (problems.length === 0) return;
					const range = {
						start: problems[0].start,
						end: problems[problems.length - 1].end
					};
					const fix = getGraphemeProblemsFix(problems, ccNode, flags);
					const graphemes = problems.map((p) => mention(p.grapheme)).join(", ");
					const uFlag = problems.every((p) => p.problem === "Surrogate");
					context.report({
						node,
						loc: getRegexpLocation(range),
						messageId: "characterClass",
						data: {
							graphemes,
							unit: flags.unicode || flags.unicodeSets ? "code points" : "char codes",
							uFlag: uFlag ? " Use the `u` flag." : ""
						},
						...makeFix(fixReplaceNode(ccNode, () => fix), "fixCharacterClass", { graphemes })
					});
				},
				onQuantifierEnter(qNode) {
					if (qNode.element.type !== "Character") return;
					const grapheme = getGraphemeBeforeQuant(qNode);
					const problem = getProblem(grapheme, flags);
					if (problem === null) return;
					context.report({
						node,
						loc: getRegexpLocation(qNode),
						messageId: `quantifier${problem}`,
						data: {
							grapheme: mention(grapheme),
							last: mentionChar(qNode.element)
						},
						...makeFix((fixer) => {
							const range = patternSource.getReplaceRange({
								start: qNode.element.end - grapheme.length,
								end: qNode.element.end
							});
							if (!range) return null;
							return range.replace(fixer, `(?:${grapheme})`);
						}, "fixQuantifier", { grapheme: mention(grapheme) })
					});
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-missing-g-flag.ts
function parseOption$2(userOption) {
	let strictTypes = true;
	if (userOption) {
		if (userOption.strictTypes != null) strictTypes = userOption.strictTypes;
	}
	return { strictTypes };
}
var no_missing_g_flag_default = createRule("no-missing-g-flag", {
	meta: {
		docs: {
			description: "disallow missing `g` flag in patterns used in `String#matchAll` and `String#replaceAll`",
			category: "Possible Errors",
			recommended: true
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { strictTypes: { type: "boolean" } },
			additionalProperties: false
		}],
		messages: { missingGlobalFlag: "The pattern given to the argument of `String#{{method}}()` requires the `g` flag, but is missing it." },
		type: "problem"
	},
	create(context) {
		const { strictTypes } = parseOption$2(context.options[0]);
		const typeTracer = createTypeTracker(context);
		/** The logic of this rule */
		function visit(regexpContext) {
			const { regexpNode, flags, flagsString } = regexpContext;
			if (flags.global || flagsString == null) return;
			for (const ref of extractExpressionReferences(regexpNode, context)) verifyExpressionReference(ref, regexpContext);
		}
		function verifyExpressionReference(ref, { regexpNode, fixReplaceFlags, flagsString }) {
			if (ref.type !== "argument") return;
			const node = ref.callExpression;
			if (node.arguments[0] !== ref.node || !isKnownMethodCall(node, {
				matchAll: 1,
				replaceAll: 2
			})) return;
			if (strictTypes ? !typeTracer.isString(node.callee.object) : !typeTracer.maybeString(node.callee.object)) return;
			context.report({
				node: ref.node,
				messageId: "missingGlobalFlag",
				data: { method: node.callee.property.name },
				fix: buildFixer()
			});
			function buildFixer() {
				if (node.arguments[0] !== regexpNode || (regexpNode.type === "NewExpression" || regexpNode.type === "CallExpression") && regexpNode.arguments[1] && regexpNode.arguments[1].type !== "Literal") return null;
				return fixReplaceFlags(`${flagsString}g`, false);
			}
		}
		return defineRegexpVisitor(context, {
			createVisitor(regexpContext) {
				visit(regexpContext);
				return {};
			},
			visitInvalid: visit,
			visitUnknown: visit
		});
	}
});
//#endregion
//#region lib/rules/no-non-standard-flag.ts
const STANDARD_FLAGS = "dgimsuvy";
var no_non_standard_flag_default = createRule("no-non-standard-flag", {
	meta: {
		docs: {
			description: "disallow non-standard flags",
			category: "Best Practices",
			recommended: true
		},
		schema: [],
		messages: { unexpected: "Unexpected non-standard flag '{{flag}}'." },
		type: "suggestion"
	},
	create(context) {
		/** The logic of this rule */
		function visit({ regexpNode, getFlagsLocation, flagsString }) {
			if (flagsString) {
				const nonStandard = [...flagsString].filter((f) => !STANDARD_FLAGS.includes(f));
				if (nonStandard.length > 0) context.report({
					node: regexpNode,
					loc: getFlagsLocation(),
					messageId: "unexpected",
					data: { flag: nonStandard[0] }
				});
			}
		}
		return defineRegexpVisitor(context, {
			createVisitor(regexpContext) {
				visit(regexpContext);
				return {};
			},
			visitInvalid: visit,
			visitUnknown: visit
		});
	}
});
//#endregion
//#region lib/rules/no-obscure-range.ts
var no_obscure_range_default = createRule("no-obscure-range", {
	meta: {
		docs: {
			description: "disallow obscure character ranges",
			category: "Best Practices",
			recommended: true
		},
		schema: [{
			type: "object",
			properties: { allowed: getAllowedCharValueSchema() },
			additionalProperties: false
		}],
		messages: { unexpected: "Unexpected obscure character range. The characters of {{range}} are not obvious." },
		type: "suggestion"
	},
	create(context) {
		const allowedRanges = getAllowedCharRanges(context.options[0]?.allowed, context);
		function createVisitor({ node, getRegexpLocation }) {
			return { onCharacterClassRangeEnter(rNode) {
				const { min, max } = rNode;
				if (min.value === max.value) return;
				if (isControlEscape(min.raw) && isControlEscape(max.raw)) return;
				if (isOctalEscape(min.raw) && isOctalEscape(max.raw)) return;
				if ((isHexLikeEscape(min.raw) || min.value === 0) && isHexLikeEscape(max.raw)) return;
				if (!isEscapeSequence(min.raw) && !isEscapeSequence(max.raw) && inRange(allowedRanges, min.value, max.value)) return;
				context.report({
					node,
					loc: getRegexpLocation(rNode),
					messageId: "unexpected",
					data: { range: mentionChar(rNode) }
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-octal.ts
var no_octal_default = createRule("no-octal", {
	meta: {
		docs: {
			description: "disallow octal escape sequence",
			category: "Best Practices",
			recommended: false
		},
		schema: [],
		messages: {
			unexpected: "Unexpected octal escape sequence '{{expr}}'.",
			replaceHex: "Replace the octal escape sequence with a hexadecimal escape sequence."
		},
		type: "suggestion",
		hasSuggestions: true
	},
	create(context) {
		function createVisitor({ node, fixReplaceNode, getRegexpLocation }) {
			return { onCharacterEnter(cNode) {
				if (cNode.raw === "\\0") return;
				if (!isOctalEscape(cNode.raw)) return;
				if (cNode.raw.startsWith("\\0") || !(cNode.parent.type === "CharacterClass" || cNode.parent.type === "CharacterClassRange")) context.report({
					node,
					loc: getRegexpLocation(cNode),
					messageId: "unexpected",
					data: { expr: cNode.raw },
					suggest: [{
						messageId: "replaceHex",
						fix: fixReplaceNode(cNode, () => {
							return `\\x${cNode.value.toString(16).padStart(2, "0")}`;
						})
					}]
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-optional-assertion.ts
/**
* Checks whether the given quantifier is quantifier with a minimum of 0.
*/
function isZeroQuantifier(node) {
	return node.min === 0;
}
/**
* Returns whether the given assertion is optional in regard to the given quantifier with a minimum of 0.
*
* Optional means that all paths in the element if the quantifier which contain the given assertion also have do not
* consume characters. For more information and examples on optional assertions, see the documentation page of this
* rule.
*/
function isOptional(assertion, quantifier, flags) {
	let element = assertion;
	while (element.parent !== quantifier) {
		const parent = element.parent;
		if (parent.type === "Alternative") {
			for (const e of parent.elements) {
				if (e === element) continue;
				if (!isZeroLength(e, flags)) return false;
			}
			if (parent.parent.type === "Pattern") throw new Error("The given assertion is not a descendant of the given quantifier.");
			element = parent.parent;
		} else {
			if (parent.max > 1 && !isZeroLength(parent, flags)) return false;
			element = parent;
		}
	}
	return true;
}
var no_optional_assertion_default = createRule("no-optional-assertion", {
	meta: {
		docs: {
			description: "disallow optional assertions",
			category: "Possible Errors",
			recommended: true
		},
		schema: [],
		messages: { optionalAssertion: "This assertion effectively optional and does not change the pattern. Either remove the assertion or change the parent quantifier '{{quantifier}}'." },
		type: "problem"
	},
	create(context) {
		function createVisitor({ node, flags, getRegexpLocation }) {
			const zeroQuantifierStack = [];
			return {
				onQuantifierEnter(q) {
					if (isZeroQuantifier(q)) zeroQuantifierStack.unshift(q);
				},
				onQuantifierLeave(q) {
					if (zeroQuantifierStack[0] === q) zeroQuantifierStack.shift();
				},
				onAssertionEnter(assertion) {
					const q = zeroQuantifierStack[0];
					if (q && isOptional(assertion, q, flags)) context.report({
						node,
						loc: getRegexpLocation(assertion),
						messageId: "optionalAssertion",
						data: { quantifier: q.raw.substr(q.element.raw.length) }
					});
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-potentially-useless-backreference.ts
var no_potentially_useless_backreference_default = createRule("no-potentially-useless-backreference", {
	meta: {
		docs: {
			description: "disallow backreferences that reference a group that might not be matched",
			category: "Possible Errors",
			recommended: true,
			default: "warn"
		},
		schema: [],
		messages: { potentiallyUselessBackreference: "Some paths leading to the backreference do not go through the referenced capturing group or the captured text might be reset before reaching the backreference." },
		type: "problem"
	},
	create(context) {
		function createVisitor({ node, flags, getRegexpLocation }) {
			return { onBackreferenceEnter(backreference) {
				if (isEmptyBackreference(backreference, flags)) return;
				if (!isStrictBackreference(backreference)) context.report({
					node,
					loc: getRegexpLocation(backreference),
					messageId: "potentiallyUselessBackreference"
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-standalone-backslash.ts
var no_standalone_backslash_default = createRule("no-standalone-backslash", {
	meta: {
		docs: {
			description: "disallow standalone backslashes (`\\`)",
			category: "Best Practices",
			recommended: false
		},
		schema: [],
		messages: { unexpected: "Unexpected standalone backslash (`\\`). It looks like an escape sequence, but it's a single `\\` character pattern." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, getRegexpLocation }) {
			return { onCharacterEnter(cNode) {
				if (cNode.value === CP_BACK_SLASH && cNode.raw === "\\") context.report({
					node,
					loc: getRegexpLocation(cNode),
					messageId: "unexpected"
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-super-linear-backtracking.ts
/**
* Returns the combined source location of the two given locations.
*/
function unionLocations(a, b) {
	/** x < y */
	function less(x, y) {
		if (x.line < y.line) return true;
		else if (x.line > y.line) return false;
		return x.column < y.column;
	}
	return {
		start: { ...less(a.start, b.start) ? a.start : b.start },
		end: { ...less(a.end, b.end) ? b.end : a.end }
	};
}
var no_super_linear_backtracking_default = createRule("no-super-linear-backtracking", {
	meta: {
		docs: {
			description: "disallow exponential and polynomial backtracking",
			category: "Possible Errors",
			recommended: true
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { report: { enum: ["certain", "potential"] } },
			additionalProperties: false
		}],
		messages: {
			self: "This quantifier can reach itself via the loop {{parent}}. Using any string accepted by {{attack}}, this can be exploited to cause at least polynomial backtracking.{{exp}}",
			trade: "The quantifier {{start}} can exchange characters with {{end}}. Using any string accepted by {{attack}}, this can be exploited to cause at least polynomial backtracking.{{exp}}"
		},
		type: "problem"
	},
	create(context) {
		const reportUncertain = (context.options[0]?.report ?? "certain") === "potential";
		function createVisitor(regexpContext) {
			const { node, patternAst, flags, getRegexpLocation, fixReplaceNode, getUsageOfPattern } = regexpContext;
			const result = analyse(getJSRegexppAst(regexpContext), {
				reportTypes: { Move: false },
				assumeRejectingSuffix: reportUncertain && getUsageOfPattern() !== UsageOfPattern.whole
			});
			for (const report of result.reports) {
				const exp = report.exponential ? " This is going to cause exponential backtracking resulting in exponential worst-case runtime behavior." : getUsageOfPattern() !== UsageOfPattern.whole ? " This might cause exponential backtracking." : "";
				const attack = `/${report.character.literal.source}+/${flags.ignoreCase ? "i" : ""}`;
				const fix = fixReplaceNode(patternAst, () => report.fix()?.source ?? null);
				if (report.type === "Self") context.report({
					node,
					loc: getRegexpLocation(report.quant),
					messageId: "self",
					data: {
						exp,
						attack,
						parent: mention(report.parentQuant)
					},
					fix
				});
				else if (report.type === "Trade") context.report({
					node,
					loc: unionLocations(getRegexpLocation(report.startQuant), getRegexpLocation(report.endQuant)),
					messageId: "trade",
					data: {
						exp,
						attack,
						start: mention(report.startQuant),
						end: mention(report.endQuant)
					},
					fix
				});
			}
			return {};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-super-linear-move.ts
/**
* Removes duplicates from the given reports.
*/
function dedupeReports(reports) {
	const seen = /* @__PURE__ */ new Set();
	const result = [];
	for (const r of reports) if (!seen.has(r.quant)) {
		result.push(r);
		seen.add(r.quant);
	}
	return result;
}
/**
* Returns all quantifiers that are reachable from the start of the
* given node without consuming or asserting any characters.
*/
function* findReachableQuantifiers(node, flags) {
	switch (node.type) {
		case "CapturingGroup":
		case "Group":
		case "Pattern":
			for (const a of node.alternatives) yield* findReachableQuantifiers(a, flags);
			break;
		case "Assertion":
			if (node.kind === "lookahead" || node.kind === "lookbehind") for (const a of node.alternatives) yield* findReachableQuantifiers(a, flags);
			break;
		case "Quantifier":
			yield node;
			break;
		case "Alternative": {
			const dir = getMatchingDirection(node);
			for (let i = 0; i < node.elements.length; i++) {
				const elementIndex = dir === "ltr" ? i : node.elements.length - 1 - i;
				const element = node.elements[elementIndex];
				yield* findReachableQuantifiers(element, flags);
				if (!isPotentiallyEmpty(element, flags)) break;
			}
			break;
		}
		default: break;
	}
}
const TRANSFORMER_OPTIONS = {
	ignoreAmbiguity: true,
	ignoreOrder: true
};
const PASS_1 = Transformers.simplify(TRANSFORMER_OPTIONS);
const PASS_2 = new CombinedTransformer([
	Transformers.inline(TRANSFORMER_OPTIONS),
	Transformers.removeDeadBranches(TRANSFORMER_OPTIONS),
	Transformers.replaceAssertions({
		...TRANSFORMER_OPTIONS,
		replacement: "empty-set"
	})
]);
var no_super_linear_move_default = createRule("no-super-linear-move", {
	meta: {
		docs: {
			description: "disallow quantifiers that cause quadratic moves",
			category: "Possible Errors",
			recommended: false
		},
		schema: [{
			type: "object",
			properties: {
				report: { enum: ["certain", "potential"] },
				ignoreSticky: { type: "boolean" },
				ignorePartial: { type: "boolean" }
			},
			additionalProperties: false
		}],
		messages: { unexpected: "Any attack string {{attack}} plus some rejecting suffix will cause quadratic runtime because of this quantifier." },
		type: "problem"
	},
	create(context) {
		const reportUncertain = (context.options[0]?.report ?? "certain") === "potential";
		const ignoreSticky = context.options[0]?.ignoreSticky ?? true;
		const ignorePartial = context.options[0]?.ignorePartial ?? true;
		function getScslreReports(regexpContext, assumeRejectingSuffix) {
			const { flags } = regexpContext;
			return analyse(getJSRegexppAst(regexpContext, true), {
				reportTypes: {
					Move: true,
					Self: false,
					Trade: false
				},
				assumeRejectingSuffix
			}).reports.map((r) => {
				if (r.type !== "Move") throw new Error("Unexpected report type");
				return {
					quant: r.quant,
					attack: `/${r.character.literal.source}+/${flags.ignoreCase ? "i" : ""}`
				};
			});
		}
		/**
		* Returns reports found using a simple quantifier approach.
		*
		* The main idea of the approach implemented here is the follows: If
		* there is a star quantifier q that can consume a non-empty word w
		* without asserting characters outside of w and that can be reached
		* without consuming or asserting characters, then we can construct an
		* attack string w^n.
		*
		* Example: /(?:ab){2,}:/
		* Here, q is `(?:ab){2,}` and w is `ab`. By repeating "ab", we can
		* create attack strings for which the regex will take O(n^2) time to
		* move across.
		*/
		function* getSimpleReports(regexpContext, assumeRejectingSuffix) {
			const { patternAst, flags } = regexpContext;
			const parser = JS.Parser.fromAst(getJSRegexppAst(regexpContext, true));
			for (const q of findReachableQuantifiers(patternAst, flags)) {
				if (q.max !== Infinity) continue;
				if (q.element.type === "Assertion" || q.element.type === "Backreference") continue;
				let e = parser.parseElement(q.element, {
					assertions: "parse",
					backreferences: "disable"
				}).expression;
				e = transform(PASS_1, e);
				e = transform(PASS_2, e);
				if (e.alternatives.length === 0) continue;
				let hasCharacters = false;
				visitAst(e, { onCharacterClassEnter() {
					hasCharacters = true;
				} });
				if (!hasCharacters) continue;
				if (!assumeRejectingSuffix) {
					const after = getFirstConsumedCharAfter(q, getMatchingDirection(q), flags);
					if (after.empty && after.look.char.isAll) continue;
				}
				yield {
					quant: q,
					attack: `/${JS.toLiteral({
						type: "Quantifier",
						alternatives: e.alternatives,
						min: 1,
						max: Infinity,
						lazy: false
					}).source}/${flags.ignoreCase ? "i" : ""}`
				};
			}
		}
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation, getUsageOfPattern } = regexpContext;
			if (ignoreSticky && flags.sticky) return {};
			const usage = getUsageOfPattern();
			if (ignorePartial && usage === UsageOfPattern.partial) return {};
			const assumeRejectingSuffix = reportUncertain && usage !== UsageOfPattern.whole;
			for (const report of dedupeReports([...getSimpleReports(regexpContext, assumeRejectingSuffix), ...getScslreReports(regexpContext, assumeRejectingSuffix)])) context.report({
				node,
				loc: getRegexpLocation(report.quant),
				messageId: "unexpected",
				data: { attack: report.attack }
			});
			return {};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-trivially-nested-assertion.ts
function isLookaround(node) {
	return node.type === "Assertion" && (node.kind === "lookahead" || node.kind === "lookbehind");
}
/**
* If the given lookaround only contains a single assertion, then this
* assertion will be returned.
*/
function getTriviallyNestedAssertion(node) {
	const alternatives = node.alternatives;
	if (alternatives.length === 1) {
		const elements = alternatives[0].elements;
		if (elements.length === 1) {
			const element = elements[0];
			if (element.type === "Assertion") return element;
		}
	}
	return null;
}
/**
* Returns the raw of an assertion that is the negation of the given assertion.
*/
function getNegatedRaw(assertion) {
	if (assertion.kind === "word") return assertion.negate ? "\\b" : "\\B";
	else if (assertion.kind === "lookahead") return `(?${assertion.negate ? "=" : "!"}${assertion.raw.slice(3)}`;
	else if (assertion.kind === "lookbehind") return `(?<${assertion.negate ? "=" : "!"}${assertion.raw.slice(4)}`;
	return null;
}
var no_trivially_nested_assertion_default = createRule("no-trivially-nested-assertion", {
	meta: {
		docs: {
			description: "disallow trivially nested assertions",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { unexpected: "Unexpected trivially nested assertion." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, fixReplaceNode, getRegexpLocation }) {
			return { onAssertionEnter(aNode) {
				if (aNode.parent.type === "Quantifier") return;
				if (!isLookaround(aNode)) return;
				const nested = getTriviallyNestedAssertion(aNode);
				if (nested === null) return;
				if (aNode.negate && isLookaround(nested) && nested.negate && hasSomeDescendant(nested, (d) => d.type === "CapturingGroup")) return;
				const replacement = aNode.negate ? getNegatedRaw(nested) : nested.raw;
				if (replacement === null) return;
				context.report({
					node,
					loc: getRegexpLocation(aNode),
					messageId: "unexpected",
					fix: fixReplaceNode(aNode, replacement)
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-trivially-nested-quantifier.ts
/**
* Returns a new quant which is the combination of both given quantifiers.
*/
function getCombinedQuant(parent, child) {
	if (parent.max === 0 || child.max === 0) return null;
	else if (parent.greedy === child.greedy) {
		const greedy = parent.greedy;
		const a = child.min;
		const b = child.max;
		const c = parent.min;
		const d = parent.max;
		if (b === Infinity && c === 0 ? a <= 1 : c === d || b * c + 1 >= a * (c + 1)) return {
			min: a * c,
			max: b * d,
			greedy
		};
		return null;
	}
	return null;
}
/**
* Given a parent quantifier and a child quantifier, this will return a
* simplified child quant.
*/
function getSimplifiedChildQuant(parent, child) {
	if (parent.max === 0 || child.max === 0) return null;
	else if (parent.greedy !== child.greedy) return null;
	let min = child.min;
	let max = child.max;
	if (min === 0 && parent.min === 0) min = 1;
	if (parent.max === Infinity && (min === 0 || min === 1) && max > 1) max = 1;
	return {
		min,
		max,
		greedy: child.greedy
	};
}
/**
* Returns whether the given quantifier is a trivial constant zero or constant
* one quantifier.
*/
function isTrivialQuantifier(quant) {
	return quant.min === quant.max && (quant.min === 0 || quant.min === 1);
}
/**
* Iterates over the alternatives of the given group and yields all quantifiers
* that are the only element of their respective alternative.
*/
function* iterateSingleQuantifiers(group) {
	for (const { elements } of group.alternatives) if (elements.length === 1) {
		const single = elements[0];
		if (single.type === "Quantifier") yield single;
	}
}
var no_trivially_nested_quantifier_default = createRule("no-trivially-nested-quantifier", {
	meta: {
		docs: {
			description: "disallow nested quantifiers that can be rewritten as one quantifier",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: {
			nested: "These two quantifiers are trivially nested and can be replaced with '{{quant}}'.",
			childOne: "This nested quantifier can be removed.",
			childSimpler: "This nested quantifier can be simplified to '{{quant}}'."
		},
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, fixReplaceNode, fixReplaceQuant, getRegexpLocation }) {
			return { onQuantifierEnter(qNode) {
				if (isTrivialQuantifier(qNode)) return;
				const element = qNode.element;
				if (element.type !== "Group") return;
				for (const child of iterateSingleQuantifiers(element)) {
					if (isTrivialQuantifier(child)) continue;
					if (element.alternatives.length === 1) {
						const quant = getCombinedQuant(qNode, child);
						if (!quant) continue;
						const quantStr = quantToString(quant);
						const replacement = child.element.raw + quantStr;
						context.report({
							node,
							loc: getRegexpLocation(qNode),
							messageId: "nested",
							data: { quant: quantStr },
							fix: fixReplaceNode(qNode, replacement)
						});
					} else {
						const quant = getSimplifiedChildQuant(qNode, child);
						if (!quant) continue;
						if (quant.min === child.min && quant.max === child.max) continue;
						if (quant.min === 1 && quant.max === 1) context.report({
							node,
							loc: getRegexpLocation(child),
							messageId: "childOne",
							fix: fixReplaceNode(child, child.element.raw)
						});
						else {
							quant.greedy = void 0;
							context.report({
								node,
								loc: getRegexpLocation(child),
								messageId: "childSimpler",
								data: { quant: quantToString(quant) },
								fix: fixReplaceQuant(child, quant)
							});
						}
					}
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-unused-capturing-group.ts
/**
* Returns an identifier for the given capturing group.
*
* This is either the name of the group or its number.
*/
function getCapturingGroupIdentifier(group) {
	if (group.name) return `'${group.name}'`;
	return `number ${getCapturingGroupNumber(group)}`;
}
var no_unused_capturing_group_default = createRule("no-unused-capturing-group", {
	meta: {
		docs: {
			description: "disallow unused capturing group",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: {
				fixable: { type: "boolean" },
				allowNamed: { type: "boolean" }
			},
			additionalProperties: false
		}],
		messages: {
			unusedCapturingGroup: "Capturing group {{identifier}} is defined but never used.",
			makeNonCapturing: "Making this a non-capturing group."
		},
		type: "suggestion",
		hasSuggestions: true
	},
	create(context) {
		const fixable = context.options[0]?.fixable ?? false;
		const allowNamed = context.options[0]?.allowNamed ?? false;
		function reportUnused(unused, regexpContext) {
			const { node, getRegexpLocation, fixReplaceNode, getAllCapturingGroups } = regexpContext;
			if (allowNamed) {
				for (const cgNode of unused) if (cgNode.name) unused.delete(cgNode);
			}
			const fixableGroups = /* @__PURE__ */ new Set();
			for (const group of [...getAllCapturingGroups()].reverse()) if (unused.has(group)) fixableGroups.add(group);
			else break;
			for (const cgNode of unused) {
				const fix = fixableGroups.has(cgNode) ? fixReplaceNode(cgNode, cgNode.raw.replace(/^\((?:\?<[^<>]+>)?/u, "(?:")) : null;
				context.report({
					node,
					loc: getRegexpLocation(cgNode),
					messageId: "unusedCapturingGroup",
					data: { identifier: getCapturingGroupIdentifier(cgNode) },
					fix: fixable ? fix : null,
					suggest: fix ? [{
						messageId: "makeNonCapturing",
						fix
					}] : null
				});
			}
		}
		function getCapturingGroupReferences(regexpContext) {
			const capturingGroupReferences = regexpContext.getCapturingGroupReferences();
			if (!capturingGroupReferences.length) return null;
			const indexRefs = [];
			const namedRefs = [];
			let hasUnknownName = false;
			let hasSplit = false;
			for (const ref of capturingGroupReferences) {
				if (ref.type === "UnknownUsage" || ref.type === "UnknownRef") return null;
				if (ref.type === "ArrayRef" || ref.type === "ReplacementRef" || ref.type === "ReplacerFunctionRef") if (ref.kind === "index") if (ref.ref != null) indexRefs.push(ref.ref);
				else return null;
				else if (ref.ref) namedRefs.push(ref.ref);
				else hasUnknownName = true;
				else if (ref.type === "Split") hasSplit = true;
			}
			return {
				unusedIndexRef(index) {
					if (hasSplit) return false;
					return !indexRefs.includes(index);
				},
				unusedNamedRef(name) {
					if (hasUnknownName) return false;
					return !namedRefs.includes(name);
				}
			};
		}
		function createVisitor(regexpContext) {
			const references = getCapturingGroupReferences(regexpContext);
			if (!references) return {};
			const unused = /* @__PURE__ */ new Set();
			const allCapturingGroups = regexpContext.getAllCapturingGroups();
			for (let index = 0; index < allCapturingGroups.length; index++) {
				const cgNode = allCapturingGroups[index];
				if (cgNode.references.length || !references.unusedIndexRef(index + 1)) continue;
				if (cgNode.name && !references.unusedNamedRef(cgNode.name)) continue;
				unused.add(cgNode);
			}
			reportUnused(unused, regexpContext);
			return {};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-useless-assertions.ts
function containsAssertion(n) {
	return hasSomeDescendant(n, (d) => d.type === "Assertion");
}
/**
* Returns whether the given lookaround asserts exactly one character in the given direction.
*/
function isSingleCharacterAssertion(assertion, direction, flags) {
	switch (assertion.kind) {
		case "word": return false;
		case "start": return direction === "rtl";
		case "end": return direction === "ltr";
		default: break;
	}
	if (getMatchingDirectionFromAssertionKind(assertion.kind) !== direction) return false;
	return assertion.alternatives.every((alt) => {
		if (!containsAssertion(alt)) {
			const range = getLengthRange(alt, flags);
			return range.min === 1 && range.max === 1;
		}
		let consumed = false;
		let asserted = false;
		const elements = direction === "ltr" ? alt.elements : [...alt.elements].reverse();
		for (const e of elements) if (!consumed) {
			if (e.type === "Assertion" && isSingleCharacterAssertion(e, direction, flags)) {
				asserted = true;
				continue;
			}
			if (containsAssertion(e)) return false;
			const range = getLengthRange(e, flags);
			if (range.max === 0) continue;
			else if (range.min === 1 && range.max === 1) consumed = true;
			else return false;
		} else {
			const otherDir = invertMatchingDirection(direction);
			if (e.type === "Assertion" && isSingleCharacterAssertion(e, otherDir, flags)) continue;
			return false;
		}
		return consumed || asserted;
	});
}
/**
* Combines 2 look chars such that the result is equivalent to 2 adjacent
* assertions `(?=a)(?=b)`.
*/
function firstLookCharsIntersection(a, b) {
	const char = a.char.intersect(b.char);
	return {
		char: a.char.intersect(b.char),
		exact: a.exact && b.exact || char.isEmpty,
		edge: a.edge && b.edge
	};
}
/**
* Creates a {@link GetFirstCharAfter} function that will reorder assertions to
* get the maximum information after the characters after the given assertions.
*
* Conceptually, this will reorder adjacent assertions such that given
* assertion is moved as far as possible in the opposite direction of natural
* matching direction. E.g. when given `$` in `a(?!a)(?<=\w)$`, the characters
* after `$` will be returned as if the pattern was `a$(?!a)(?<=\w)`.
*
* @param forbidden A list of assertions that may not be reordered.
*/
function createReorderingGetFirstCharAfter(forbidden) {
	/** Whether the given element or one of its descendants is forbidden. */
	function hasForbidden(element) {
		if (element.type === "Assertion" && forbidden.has(element)) return true;
		for (const f of forbidden) if (hasSomeDescendant(element, f)) return true;
		return false;
	}
	return (afterThis, direction, flags) => {
		let result = getFirstCharAfter(afterThis, direction, flags);
		if (afterThis.parent.type === "Alternative") {
			const { elements } = afterThis.parent;
			const inc = direction === "ltr" ? -1 : 1;
			const start = elements.indexOf(afterThis);
			for (let i = start + inc; i >= 0 && i < elements.length; i += inc) {
				const other = elements[i];
				if (!isZeroLength(other, flags)) break;
				if (hasForbidden(other)) break;
				const otherResult = FirstConsumedChars.toLook(getFirstConsumedChar(other, direction, flags));
				result = firstLookCharsIntersection(result, otherResult);
			}
		}
		return result;
	};
}
function removeAlternative(alternative) {
	const parent = alternative.parent;
	if (parent.alternatives.length > 1) {
		let { start, end } = alternative;
		if (parent.alternatives[0] === alternative) end++;
		else start--;
		return [parent, parent.raw.slice(0, start - parent.start) + parent.raw.slice(end - parent.start)];
	}
	switch (parent.type) {
		case "Pattern": return [parent, "[]"];
		case "Assertion": {
			const assertionParent = parent.parent;
			if (parent.negate) return [assertionParent.type === "Quantifier" ? assertionParent : parent, ""];
			if (assertionParent.type === "Quantifier") {
				if (assertionParent.min === 0) return [assertionParent, ""];
				return removeAlternative(assertionParent.parent);
			}
			return removeAlternative(assertionParent);
		}
		case "CapturingGroup": return [parent, `${parent.raw.slice(0, alternative.start - parent.start)}[]${parent.raw.slice(alternative.end - parent.start)}`];
		case "Group": {
			const groupParent = parent.parent;
			if (groupParent.type === "Quantifier") {
				if (groupParent.min === 0) return [groupParent, ""];
				return removeAlternative(groupParent.parent);
			}
			return removeAlternative(groupParent);
		}
		default: return assertNever(parent);
	}
}
var no_useless_assertions_default = createRule("no-useless-assertions", {
	meta: {
		docs: {
			description: "disallow assertions that are known to always accept (or reject)",
			category: "Possible Errors",
			recommended: true
		},
		hasSuggestions: true,
		schema: [],
		messages: {
			alwaysRejectByChar: "{{assertion}} will always reject because it is {{followedOrPreceded}} by a character.",
			alwaysAcceptByChar: "{{assertion}} will always accept because it is never {{followedOrPreceded}} by a character.",
			alwaysRejectByNonLineTerminator: "{{assertion}} will always reject because it is {{followedOrPreceded}} by a non-line-terminator character.",
			alwaysAcceptByLineTerminator: "{{assertion}} will always accept because it is {{followedOrPreceded}} by a line-terminator character.",
			alwaysAcceptByLineTerminatorOrEdge: "{{assertion}} will always accept because it is {{followedOrPreceded}} by a line-terminator character or the {{startOrEnd}} of the input string.",
			alwaysAcceptOrRejectFollowedByWord: "{{assertion}} will always {{acceptOrReject}} because it is preceded by a non-word character and followed by a word character.",
			alwaysAcceptOrRejectFollowedByNonWord: "{{assertion}} will always {{acceptOrReject}} because it is preceded by a non-word character and followed by a non-word character.",
			alwaysAcceptOrRejectPrecededByWordFollowedByNonWord: "{{assertion}} will always {{acceptOrReject}} because it is preceded by a word character and followed by a non-word character.",
			alwaysAcceptOrRejectPrecededByWordFollowedByWord: "{{assertion}} will always {{acceptOrReject}} because it is preceded by a word character and followed by a word character.",
			alwaysForLookaround: "The {{kind}} {{assertion}} will always {{acceptOrReject}}.",
			alwaysForNegativeLookaround: "The negative {{kind}} {{assertion}} will always {{acceptOrReject}}.",
			acceptSuggestion: "Remove the assertion. (Replace with empty string.)",
			rejectSuggestion: "Remove branch of the assertion. (Replace with empty set.)"
		},
		type: "problem"
	},
	create(context) {
		function createVisitor({ node, flags, getRegexpLocation, fixReplaceNode }) {
			const reported = /* @__PURE__ */ new Set();
			function replaceWithEmptyString(assertion) {
				if (assertion.parent.type === "Quantifier") return fixReplaceNode(assertion.parent, "");
				return fixReplaceNode(assertion, "");
			}
			function replaceWithEmptySet(assertion) {
				if (assertion.parent.type === "Quantifier") {
					if (assertion.parent.min === 0) return fixReplaceNode(assertion.parent, "");
					const [element, replacement] = removeAlternative(assertion.parent.parent);
					return fixReplaceNode(element, replacement);
				}
				const [element, replacement] = removeAlternative(assertion.parent);
				return fixReplaceNode(element, replacement);
			}
			function report(assertion, messageId, data) {
				reported.add(assertion);
				const { acceptOrReject } = data;
				context.report({
					node,
					loc: getRegexpLocation(assertion),
					messageId,
					data: {
						assertion: mention(assertion),
						...data
					},
					suggest: [{
						messageId: `${acceptOrReject}Suggestion`,
						fix: acceptOrReject === "accept" ? replaceWithEmptyString(assertion) : replaceWithEmptySet(assertion)
					}]
				});
			}
			/**
			* Verify for `^` or `$`
			*/
			function verifyStartOrEnd(assertion, getFirstCharAfterFn) {
				const next = getFirstCharAfterFn(assertion, getMatchingDirectionFromAssertionKind(assertion.kind), flags);
				const followedOrPreceded = assertion.kind === "end" ? "followed" : "preceded";
				const lineTerminator = Chars.lineTerminator(flags);
				if (next.edge) {
					if (!flags.multiline) {
						if (next.char.isEmpty) report(assertion, "alwaysAcceptByChar", {
							followedOrPreceded,
							acceptOrReject: "accept"
						});
					} else if (next.char.isSubsetOf(lineTerminator)) report(assertion, "alwaysAcceptByLineTerminatorOrEdge", {
						followedOrPreceded,
						startOrEnd: assertion.kind,
						acceptOrReject: "accept"
					});
				} else if (!flags.multiline) report(assertion, "alwaysRejectByChar", {
					followedOrPreceded,
					acceptOrReject: "reject"
				});
				else if (next.char.isDisjointWith(lineTerminator)) report(assertion, "alwaysRejectByNonLineTerminator", {
					followedOrPreceded,
					acceptOrReject: "reject"
				});
				else if (next.char.isSubsetOf(lineTerminator)) report(assertion, "alwaysAcceptByLineTerminator", {
					followedOrPreceded,
					acceptOrReject: "accept"
				});
			}
			/**
			* Verify for `\b` or `\B`
			*/
			function verifyWordBoundary(assertion, getFirstCharAfterFn) {
				const word = Chars.word(flags);
				const next = getFirstCharAfterFn(assertion, "ltr", flags);
				const prev = getFirstCharAfterFn(assertion, "rtl", flags);
				const nextIsWord = next.char.isSubsetOf(word) && !next.edge;
				const prevIsWord = prev.char.isSubsetOf(word) && !prev.edge;
				const nextIsNonWord = next.char.isDisjointWith(word);
				const prevIsNonWord = prev.char.isDisjointWith(word);
				const accept = assertion.negate ? "reject" : "accept";
				const reject = assertion.negate ? "accept" : "reject";
				if (prevIsNonWord) {
					if (nextIsWord) report(assertion, "alwaysAcceptOrRejectFollowedByWord", { acceptOrReject: accept });
					if (nextIsNonWord) report(assertion, "alwaysAcceptOrRejectFollowedByNonWord", { acceptOrReject: reject });
				}
				if (prevIsWord) {
					if (nextIsNonWord) report(assertion, "alwaysAcceptOrRejectPrecededByWordFollowedByNonWord", { acceptOrReject: accept });
					if (nextIsWord) report(assertion, "alwaysAcceptOrRejectPrecededByWordFollowedByWord", { acceptOrReject: reject });
				}
			}
			/**
			* Verify for LookaroundAssertion
			*/
			function verifyLookaround(assertion, getFirstCharAfterFn) {
				if (isPotentiallyEmpty(assertion.alternatives, flags)) return;
				const direction = getMatchingDirectionFromAssertionKind(assertion.kind);
				const after = getFirstCharAfterFn(assertion, direction, flags);
				const firstOf = FirstConsumedChars.toLook(getFirstConsumedChar(assertion.alternatives, direction, flags));
				const accept = assertion.negate ? "reject" : "accept";
				const reject = assertion.negate ? "accept" : "reject";
				if (after.char.isDisjointWith(firstOf.char) && !(after.edge && firstOf.edge)) report(assertion, assertion.negate ? "alwaysForNegativeLookaround" : "alwaysForLookaround", {
					kind: assertion.kind,
					acceptOrReject: reject
				});
				const edgeSubset = firstOf.edge || !after.edge;
				if (firstOf.exact && edgeSubset && after.char.isSubsetOf(firstOf.char) && isSingleCharacterAssertion(assertion, getMatchingDirectionFromAssertionKind(assertion.kind), flags)) report(assertion, assertion.negate ? "alwaysForNegativeLookaround" : "alwaysForLookaround", {
					kind: assertion.kind,
					acceptOrReject: accept
				});
			}
			/**
			* Verify for Assertion
			*/
			function verifyAssertion(assertion, getFirstCharAfterFn) {
				switch (assertion.kind) {
					case "start":
					case "end":
						verifyStartOrEnd(assertion, getFirstCharAfterFn);
						break;
					case "word":
						verifyWordBoundary(assertion, getFirstCharAfterFn);
						break;
					case "lookahead":
					case "lookbehind":
						verifyLookaround(assertion, getFirstCharAfterFn);
						break;
					default: throw assertNever(assertion);
				}
			}
			const allAssertions = [];
			return {
				onAssertionEnter(assertion) {
					verifyAssertion(assertion, getFirstCharAfter);
					allAssertions.push(assertion);
				},
				onPatternLeave() {
					const reorderingGetFirstCharAfter = createReorderingGetFirstCharAfter(reported);
					for (const assertion of allAssertions) if (!reported.has(assertion)) verifyAssertion(assertion, reorderingGetFirstCharAfter);
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-useless-backreference.ts
/**
* Returns whether the list of ancestors from `from` to `to` contains a negated
* lookaround.
*/
function hasNegatedLookaroundInBetween(from, to) {
	for (let p = from.parent; p && p !== to; p = p.parent) if (p.type === "Assertion" && (p.kind === "lookahead" || p.kind === "lookbehind") && p.negate) return true;
	return false;
}
/**
* Returns the problem information specifying the reason why the backreference is
* useless.
*/
function getUselessProblem(backRef, flags) {
	const groups = [backRef.resolved].flat();
	const problems = [];
	for (const group of groups) {
		const messageId = getUselessMessageId(backRef, group, flags);
		if (!messageId) return null;
		problems.push({
			messageId,
			group
		});
	}
	if (problems.length === 0) return null;
	let problemsToReport;
	const problemsInSameDisjunction = problems.filter((problem) => problem.messageId !== "disjunctive");
	if (problemsInSameDisjunction.length) problemsToReport = problemsInSameDisjunction;
	else problemsToReport = problems;
	const [{ messageId, group }, ...other] = problemsToReport;
	let otherGroups = "";
	if (other.length === 1) otherGroups = " and another group";
	else if (other.length > 1) otherGroups = ` and other ${other.length} groups`;
	return {
		messageId,
		group,
		otherGroups
	};
}
/**
* Returns the message id specifying the reason why the backreference is
* useless.
*/
function getUselessMessageId(backRef, group, flags) {
	const closestAncestor = getClosestAncestor(backRef, group);
	if (closestAncestor === group) return "nested";
	else if (closestAncestor.type !== "Alternative") return "disjunctive";
	if (hasNegatedLookaroundInBetween(group, closestAncestor)) return "intoNegativeLookaround";
	const matchingDir = getMatchingDirection(closestAncestor);
	if (matchingDir === "ltr" && backRef.end <= group.start) return "forward";
	else if (matchingDir === "rtl" && group.end <= backRef.start) return "backward";
	if (isZeroLength(group, flags)) return "empty";
	return null;
}
var no_useless_backreference_default = createRule("no-useless-backreference", {
	meta: {
		docs: {
			description: "disallow useless backreferences in regular expressions",
			category: "Possible Errors",
			recommended: true
		},
		schema: [],
		messages: {
			nested: "Backreference {{ bref }} will be ignored. It references group {{ group }}{{ otherGroups }} from within that group.",
			forward: "Backreference {{ bref }} will be ignored. It references group {{ group }}{{ otherGroups }} which appears later in the pattern.",
			backward: "Backreference {{ bref }} will be ignored. It references group {{ group }}{{ otherGroups }} which appears before in the same lookbehind.",
			disjunctive: "Backreference {{ bref }} will be ignored. It references group {{ group }}{{ otherGroups }} which is in another alternative.",
			intoNegativeLookaround: "Backreference {{ bref }} will be ignored. It references group {{ group }}{{ otherGroups }} which is in a negative lookaround.",
			empty: "Backreference {{ bref }} will be ignored. It references group {{ group }}{{ otherGroups }} which always captures zero characters."
		},
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, flags, getRegexpLocation }) {
			return { onBackreferenceEnter(backRef) {
				const problem = getUselessProblem(backRef, flags);
				if (problem) context.report({
					node,
					loc: getRegexpLocation(backRef),
					messageId: problem.messageId,
					data: {
						bref: mention(backRef),
						group: mention(problem.group),
						otherGroups: problem.otherGroups
					}
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-useless-character-class.ts
const ESCAPES_OUTSIDE_CHARACTER_CLASS = /* @__PURE__ */ new Set("$()*+./?[{|");
const ESCAPES_OUTSIDE_CHARACTER_CLASS_WITH_U = new Set([...ESCAPES_OUTSIDE_CHARACTER_CLASS, "}"]);
var no_useless_character_class_default = createRule("no-useless-character-class", {
	meta: {
		docs: {
			description: "disallow character class with one character",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { ignores: {
				type: "array",
				items: {
					type: "string",
					minLength: 1
				},
				uniqueItems: true
			} },
			additionalProperties: false
		}],
		messages: {
			unexpectedCharacterClassWith: "Unexpected character class with one {{type}}. Can remove brackets{{additional}}.",
			unexpectedUnnecessaryNestingCharacterClass: "Unexpected unnecessary nesting character class. Can remove brackets."
		},
		type: "suggestion"
	},
	create(context) {
		const ignores = context.options[0]?.ignores ?? ["="];
		function createVisitor({ node, pattern, flags, fixReplaceNode, getRegexpLocation }) {
			const characterClassStack = [];
			return {
				onExpressionCharacterClassEnter(eccNode) {
					characterClassStack.push(eccNode);
				},
				onExpressionCharacterClassLeave() {
					characterClassStack.pop();
				},
				onCharacterClassEnter(ccNode) {
					characterClassStack.push(ccNode);
				},
				onCharacterClassLeave(ccNode) {
					characterClassStack.pop();
					if (ccNode.negate) return;
					let messageId, messageData;
					const unwrapped = ccNode.elements.map((_e, index) => {
						const element = ccNode.elements[index];
						return (index === 0 ? getEscapedFirstRawIfNeeded(element) : null) ?? (index === ccNode.elements.length - 1 ? getEscapedLastRawIfNeeded(element) : null) ?? element.raw;
					});
					if (ccNode.elements.length !== 1 && ccNode.parent.type === "CharacterClass") {
						messageId = "unexpectedUnnecessaryNestingCharacterClass";
						messageData = { type: "unnecessary nesting character class" };
						if (!ccNode.elements.length) {
							const nextElement = ccNode.parent.elements[ccNode.parent.elements.indexOf(ccNode) + 1];
							if (nextElement && isNeedEscapedForFirstElement(nextElement)) unwrapped.push("\\");
						}
					} else {
						if (ccNode.elements.length !== 1) return;
						const element = ccNode.elements[0];
						if (ignores.length > 0 && ignores.includes(element.raw)) return;
						if (element.type === "Character") {
							if (element.raw === "\\b") return;
							if (/^\\\d+$/u.test(element.raw) && !element.raw.startsWith("\\0")) return;
							if (ignores.length > 0 && ignores.includes(String.fromCodePoint(element.value))) return;
							if (!canUnwrapped(ccNode, element.raw)) return;
							messageData = { type: "character" };
						} else if (element.type === "CharacterClassRange") {
							if (element.min.value !== element.max.value) return;
							messageData = {
								type: "character class range",
								additional: " and range"
							};
							unwrapped[0] = getEscapedFirstRawIfNeeded(element.min) ?? getEscapedLastRawIfNeeded(element.min) ?? element.min.raw;
						} else if (element.type === "ClassStringDisjunction") {
							if (!characterClassStack.length) return;
							messageData = { type: "string literal" };
						} else if (element.type === "CharacterSet") messageData = { type: "character class escape" };
						else if (element.type === "CharacterClass" || element.type === "ExpressionCharacterClass") messageData = { type: "character class" };
						else return;
						messageId = "unexpectedCharacterClassWith";
					}
					context.report({
						node,
						loc: getRegexpLocation(ccNode),
						messageId,
						data: {
							type: messageData.type,
							additional: messageData.additional || ""
						},
						fix: fixReplaceNode(ccNode, unwrapped.join(""))
					});
					/**
					* Checks whether an escape is required if the given element is placed first
					* after character class replacement.
					*/
					function isNeedEscapedForFirstElement(element) {
						const char = element.type === "Character" ? element.raw : element.type === "CharacterClassRange" ? element.min.raw : null;
						if (char == null) return false;
						if (characterClassStack.length) {
							if (RESERVED_DOUBLE_PUNCTUATOR_CHARS.has(char) && pattern[ccNode.start - 1] === char) return true;
							return char === "^" && ccNode.parent.type === "CharacterClass" && ccNode.parent.elements[0] === ccNode;
						}
						return (flags.unicode ? ESCAPES_OUTSIDE_CHARACTER_CLASS_WITH_U : ESCAPES_OUTSIDE_CHARACTER_CLASS).has(char);
					}
					/**
					* Checks whether an escape is required if the given element is placed last
					* after character class replacement.
					*/
					function needEscapedForLastElement(element) {
						const char = element.type === "Character" ? element.raw : element.type === "CharacterClassRange" ? element.max.raw : null;
						if (char == null) return false;
						if (characterClassStack.length) return RESERVED_DOUBLE_PUNCTUATOR_CHARS.has(char) && pattern[ccNode.end] === char;
						return false;
					}
					/**
					* Returns the escaped raw text, if the given first element requires escaping.
					* Otherwise, returns null.
					*/
					function getEscapedFirstRawIfNeeded(firstElement) {
						if (isNeedEscapedForFirstElement(firstElement)) return `\\${firstElement.raw}`;
						return null;
					}
					/**
					* Returns the escaped raw text, if the given last element requires escaping.
					* Otherwise, returns null.
					*/
					function getEscapedLastRawIfNeeded(lastElement) {
						if (needEscapedForLastElement(lastElement)) {
							const lastRaw = lastElement.type === "Character" ? lastElement.raw : lastElement.type === "CharacterClassRange" ? lastElement.max.raw : "";
							return `${lastElement.raw.slice(0, -lastRaw.length)}\\${lastRaw}`;
						}
						return null;
					}
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-useless-dollar-replacements.ts
/**
* Extract `$` replacements
*/
function extractDollarReplacements(context, node) {
	return parseReplacements(context, node).filter((e) => e.type === "ReferenceElement");
}
var no_useless_dollar_replacements_default = createRule("no-useless-dollar-replacements", {
	meta: {
		docs: {
			description: "disallow useless `$` replacements in replacement string",
			category: "Possible Errors",
			recommended: true
		},
		schema: [],
		messages: {
			numberRef: "'${{ refText }}' replacement will insert '${{ refText }}' because there are less than {{ num }} capturing groups. Use '$$' if you want to escape '$'.",
			numberRefCapturingNotFound: "'${{ refText }}' replacement will insert '${{ refText }}' because capturing group is not found. Use '$$' if you want to escape '$'.",
			namedRef: "'$<{{ refText }}>' replacement will be ignored because the named capturing group is not found. Use '$$' if you want to escape '$'.",
			namedRefNamedCapturingNotFound: "'$<{{ refText }}>' replacement will insert '$<{{ refText }}>' because named capturing group is not found. Use '$$' if you want to escape '$'."
		},
		type: "suggestion"
	},
	create(context) {
		const typeTracer = createTypeTracker(context);
		const sourceCode = context.sourceCode;
		function verify(patternNode, replacement) {
			const captures = extractCaptures(patternNode);
			for (const dollarReplacement of extractDollarReplacements(context, replacement)) if (typeof dollarReplacement.ref === "number") {
				if (captures.count < dollarReplacement.ref) context.report({
					node: replacement,
					loc: {
						start: sourceCode.getLocFromIndex(dollarReplacement.range[0]),
						end: sourceCode.getLocFromIndex(dollarReplacement.range[1])
					},
					messageId: captures.count > 0 ? "numberRef" : "numberRefCapturingNotFound",
					data: {
						refText: dollarReplacement.refText,
						num: String(dollarReplacement.ref)
					}
				});
			} else if (!captures.names.has(dollarReplacement.ref)) context.report({
				node: replacement,
				loc: {
					start: sourceCode.getLocFromIndex(dollarReplacement.range[0]),
					end: sourceCode.getLocFromIndex(dollarReplacement.range[1])
				},
				messageId: captures.names.size > 0 ? "namedRef" : "namedRefNamedCapturingNotFound",
				data: { refText: dollarReplacement.refText }
			});
		}
		return { CallExpression(node) {
			if (!isKnownMethodCall(node, {
				replace: 2,
				replaceAll: 2
			})) return;
			const mem = node.callee;
			const replacementTextNode = node.arguments[1];
			if (replacementTextNode.type !== "Literal" || typeof replacementTextNode.value !== "string") return;
			const patternNode = getRegExpNodeFromExpression(node.arguments[0], context);
			if (!patternNode) return;
			if (!typeTracer.isString(mem.object)) return;
			verify(patternNode, replacementTextNode);
		} };
	}
});
//#endregion
//#region lib/rules/no-useless-escape.ts
const REGEX_CHAR_CLASS_ESCAPES = new Set([
	CP_BACK_SLASH,
	CP_CLOSING_BRACKET,
	CP_MINUS
]);
const REGEX_CLASS_SET_CHAR_CLASS_ESCAPE = new Set([
	CP_BACK_SLASH,
	CP_SLASH,
	CP_OPENING_BRACKET,
	CP_CLOSING_BRACKET,
	CP_OPENING_BRACE,
	CP_CLOSING_BRACE,
	CP_PIPE,
	CP_OPENING_PAREN,
	CP_CLOSING_PAREN,
	CP_MINUS
]);
const REGEX_ESCAPES = new Set([
	CP_BACK_SLASH,
	CP_SLASH,
	CP_CARET,
	CP_DOT,
	CP_DOLLAR,
	CP_STAR,
	CP_PLUS,
	CP_QUESTION,
	CP_OPENING_BRACKET,
	CP_CLOSING_BRACKET,
	CP_OPENING_BRACE,
	CP_CLOSING_BRACE,
	CP_PIPE,
	CP_OPENING_PAREN,
	CP_CLOSING_PAREN
]);
const POTENTIAL_ESCAPE_SEQUENCE = /* @__PURE__ */ new Set("uxkpP");
const POTENTIAL_ESCAPE_SEQUENCE_FOR_CHAR_CLASS = new Set([...POTENTIAL_ESCAPE_SEQUENCE, "q"]);
var no_useless_escape_default = createRule("no-useless-escape", {
	meta: {
		docs: {
			description: "disallow unnecessary escape characters in RegExp",
			category: "Stylistic Issues",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { unnecessary: "Unnecessary escape character: \\{{character}}." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, flags, pattern, getRegexpLocation, fixReplaceNode }) {
			function report(cNode, offset, character, fix) {
				context.report({
					node,
					loc: getRegexpLocation(cNode, [offset, offset + 1]),
					messageId: "unnecessary",
					data: { character },
					fix: fix ? fixReplaceNode(cNode, character) : null
				});
			}
			const characterClassStack = [];
			return {
				onCharacterClassEnter: (characterClassNode) => characterClassStack.unshift(characterClassNode),
				onCharacterClassLeave: () => characterClassStack.shift(),
				onExpressionCharacterClassEnter: (characterClassNode) => characterClassStack.unshift(characterClassNode),
				onExpressionCharacterClassLeave: () => characterClassStack.shift(),
				onCharacterEnter(cNode) {
					if (cNode.raw[0] === "\\") {
						const char = cNode.raw.slice(1);
						const escapedChar = String.fromCodePoint(cNode.value);
						if (char === escapedChar) {
							let allowedEscapes;
							if (characterClassStack.length) allowedEscapes = flags.unicodeSets ? REGEX_CLASS_SET_CHAR_CLASS_ESCAPE : REGEX_CHAR_CLASS_ESCAPES;
							else allowedEscapes = REGEX_ESCAPES;
							if (allowedEscapes.has(cNode.value)) return;
							if (characterClassStack.length) {
								const characterClassNode = characterClassStack[0];
								if (cNode.value === CP_CARET) {
									if (characterClassNode.start + 1 === cNode.start) return;
								}
								if (flags.unicodeSets) {
									if (RESERVED_DOUBLE_PUNCTUATOR_CP.has(cNode.value)) {
										if (pattern[cNode.end] === escapedChar) return;
										const prevIndex = cNode.start - 1;
										if (pattern[prevIndex] === escapedChar) {
											if (escapedChar !== "^") return;
											if (characterClassNode.start + 1 + (characterClassNode.negate ? 1 : 0) <= prevIndex) return;
										}
									}
								}
							}
							if (!canUnwrapped(cNode, char)) return;
							report(cNode, 0, char, !(characterClassStack.length ? POTENTIAL_ESCAPE_SEQUENCE_FOR_CHAR_CLASS : POTENTIAL_ESCAPE_SEQUENCE).has(char));
						}
					}
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-useless-flag.ts
var RegExpReference = class {
	regExpContext;
	get defineNode() {
		return this.regExpContext.regexpNode;
	}
	defineId;
	readNodes = /* @__PURE__ */ new Map();
	state = {
		usedNodes: /* @__PURE__ */ new Map(),
		track: true
	};
	constructor(regExpContext) {
		this.regExpContext = regExpContext;
	}
	addReadNode(node) {
		this.readNodes.set(node, {});
	}
	setDefineId(codePathId, loopNode) {
		this.defineId = {
			codePathId,
			loopNode
		};
	}
	markAsUsedInSearch(node) {
		const exprState = this.readNodes.get(node);
		if (exprState) exprState.marked = true;
		this.addUsedNode("search", node);
	}
	markAsUsedInSplit(node) {
		const exprState = this.readNodes.get(node);
		if (exprState) exprState.marked = true;
		this.addUsedNode("split", node);
	}
	markAsUsedInExec(node, codePathId, loopNode) {
		const exprState = this.readNodes.get(node);
		if (exprState) {
			exprState.marked = true;
			exprState.usedInExec = { id: {
				codePathId,
				loopNode
			} };
		}
		this.addUsedNode("exec", node);
	}
	markAsUsedInTest(node, codePathId, loopNode) {
		const exprState = this.readNodes.get(node);
		if (exprState) {
			exprState.marked = true;
			exprState.usedInTest = { id: {
				codePathId,
				loopNode
			} };
		}
		this.addUsedNode("test", node);
	}
	isUsed(kinds) {
		for (const kind of kinds) if (this.state.usedNodes.has(kind)) return true;
		return false;
	}
	isCannotTrack() {
		return !this.state.track;
	}
	markAsUsed(kind, exprNode) {
		this.addUsedNode(kind, exprNode);
	}
	markAsCannotTrack() {
		this.state.track = false;
	}
	getUsedNodes() {
		return this.state.usedNodes;
	}
	addUsedNode(kind, exprNode) {
		const list = this.state.usedNodes.get(kind);
		if (list) list.push(exprNode);
		else this.state.usedNodes.set(kind, [exprNode]);
	}
};
/**
* Returns a fixer that removes the given flag.
*/
function fixRemoveFlag({ flagsString, fixReplaceFlags }, flag) {
	if (flagsString) return fixReplaceFlags(flagsString.replace(flag, ""));
	return null;
}
/**
* Create visitor for verify unnecessary i flag
*/
function createUselessIgnoreCaseFlagVisitor(context) {
	return defineRegexpVisitor(context, { createVisitor(regExpContext) {
		const { flags, regexpNode, ownsFlags, getFlagLocation } = regExpContext;
		if (!flags.ignoreCase || !ownsFlags) return {};
		return { onPatternLeave(pattern) {
			if (!isCaseVariant(pattern, flags, false)) context.report({
				node: regexpNode,
				loc: getFlagLocation("i"),
				messageId: "uselessIgnoreCaseFlag",
				fix: fixRemoveFlag(regExpContext, "i")
			});
		} };
	} });
}
/**
* Create visitor for verify unnecessary m flag
*/
function createUselessMultilineFlagVisitor(context) {
	return defineRegexpVisitor(context, { createVisitor(regExpContext) {
		const { flags, regexpNode, ownsFlags, getFlagLocation } = regExpContext;
		if (!flags.multiline || !ownsFlags) return {};
		let unnecessary = true;
		return {
			onAssertionEnter(node) {
				if (node.kind === "start" || node.kind === "end") unnecessary = false;
			},
			onPatternLeave() {
				if (unnecessary) context.report({
					node: regexpNode,
					loc: getFlagLocation("m"),
					messageId: "uselessMultilineFlag",
					fix: fixRemoveFlag(regExpContext, "m")
				});
			}
		};
	} });
}
/**
* Create visitor for verify unnecessary s flag
*/
function createUselessDotAllFlagVisitor(context) {
	return defineRegexpVisitor(context, { createVisitor(regExpContext) {
		const { flags, regexpNode, ownsFlags, getFlagLocation } = regExpContext;
		if (!flags.dotAll || !ownsFlags) return {};
		let unnecessary = true;
		return {
			onCharacterSetEnter(node) {
				if (node.kind === "any") unnecessary = false;
			},
			onPatternLeave() {
				if (unnecessary) context.report({
					node: regexpNode,
					loc: getFlagLocation("s"),
					messageId: "uselessDotAllFlag",
					fix: fixRemoveFlag(regExpContext, "s")
				});
			}
		};
	} });
}
/**
* Create visitor for verify unnecessary g flag
*/
function createUselessGlobalFlagVisitor(context, strictTypes) {
	let ReportKind = /* @__PURE__ */ function(ReportKind) {
		ReportKind[ReportKind["usedOnlyInSplit"] = 0] = "usedOnlyInSplit";
		ReportKind[ReportKind["usedOnlyInSearch"] = 1] = "usedOnlyInSearch";
		ReportKind[ReportKind["usedOnlyOnceInExec"] = 2] = "usedOnlyOnceInExec";
		ReportKind[ReportKind["usedOnlyOnceInTest"] = 3] = "usedOnlyOnceInTest";
		ReportKind[ReportKind["unused"] = 4] = "unused";
		return ReportKind;
	}({});
	/**
	* Report for useless global flag
	*/
	function reportUselessGlobalFlag(regExpReference, data) {
		const { getFlagLocation } = regExpReference.regExpContext;
		const node = regExpReference.defineNode;
		context.report({
			node,
			loc: getFlagLocation("g"),
			messageId: data.kind === ReportKind.usedOnlyInSplit ? "uselessGlobalFlagForSplit" : data.kind === ReportKind.usedOnlyInSearch ? "uselessGlobalFlagForSearch" : data.kind === ReportKind.usedOnlyOnceInTest ? "uselessGlobalFlagForTest" : data.kind === ReportKind.usedOnlyOnceInExec ? "uselessGlobalFlagForExec" : "uselessGlobalFlag",
			fix: data.fixable ? fixRemoveFlag(regExpReference.regExpContext, "g") : null
		});
	}
	/**
	* Checks if it needs to be reported and returns the report data if it needs to be reported.
	*/
	function getReportData(regExpReference) {
		let countOfUsedInExecOrTest = 0;
		for (const readData of regExpReference.readNodes.values()) {
			if (!readData.marked) return null;
			const usedInExecOrTest = readData.usedInExec || readData.usedInTest;
			if (usedInExecOrTest) {
				if (!regExpReference.defineId) return null;
				if (regExpReference.defineId.codePathId === usedInExecOrTest.id.codePathId && regExpReference.defineId.loopNode === usedInExecOrTest.id.loopNode) {
					countOfUsedInExecOrTest++;
					if (countOfUsedInExecOrTest > 1) return null;
					continue;
				} else return null;
			}
		}
		return buildReportData(regExpReference);
	}
	function buildReportData(regExpReference) {
		const usedNodes = regExpReference.getUsedNodes();
		if (usedNodes.size === 1) {
			const [[method, nodes]] = usedNodes;
			const fixable = nodes.length === 1 && nodes.includes(regExpReference.defineNode);
			if (method === "split") return {
				kind: ReportKind.usedOnlyInSplit,
				fixable
			};
			if (method === "search") return {
				kind: ReportKind.usedOnlyInSearch,
				fixable
			};
			if (method === "exec" && nodes.length === 1) return {
				kind: ReportKind.usedOnlyOnceInExec,
				fixable
			};
			if (method === "test" && nodes.length === 1) return {
				kind: ReportKind.usedOnlyOnceInTest,
				fixable
			};
		}
		return { kind: ReportKind.unused };
	}
	return createRegExpReferenceExtractVisitor(context, {
		flag: "global",
		exit(regExpReferenceList) {
			for (const regExpReference of regExpReferenceList) {
				const report = getReportData(regExpReference);
				if (report != null) reportUselessGlobalFlag(regExpReference, report);
			}
		},
		isUsedShortCircuit(regExpReference) {
			return regExpReference.isUsed([
				"match",
				"matchAll",
				"replace",
				"replaceAll"
			]);
		},
		strictTypes
	});
}
/**
* Create visitor for verify unnecessary y flag
*/
function createUselessStickyFlagVisitor(context, strictTypes) {
	/**
	* Report for useless sticky flag
	*/
	function reportUselessStickyFlag(regExpReference, data) {
		const { getFlagLocation } = regExpReference.regExpContext;
		const node = regExpReference.defineNode;
		context.report({
			node,
			loc: getFlagLocation("y"),
			messageId: "uselessStickyFlag",
			fix: data.fixable ? fixRemoveFlag(regExpReference.regExpContext, "y") : null
		});
	}
	/**
	* Checks if it needs to be reported and returns the report data if it needs to be reported.
	*/
	function getReportData(regExpReference) {
		for (const readData of regExpReference.readNodes.values()) if (!readData.marked) return null;
		return buildReportData(regExpReference);
	}
	function buildReportData(regExpReference) {
		const usedNodes = regExpReference.getUsedNodes();
		if (usedNodes.size === 1) {
			const [[method, nodes]] = usedNodes;
			const fixable = nodes.length === 1 && nodes.includes(regExpReference.defineNode);
			if (method === "split") return { fixable };
		}
		return {};
	}
	return createRegExpReferenceExtractVisitor(context, {
		flag: "sticky",
		exit(regExpReferenceList) {
			for (const regExpReference of regExpReferenceList) {
				const report = getReportData(regExpReference);
				if (report != null) reportUselessStickyFlag(regExpReference, report);
			}
		},
		isUsedShortCircuit(regExpReference) {
			return regExpReference.isUsed([
				"search",
				"exec",
				"test",
				"match",
				"matchAll",
				"replace",
				"replaceAll"
			]);
		},
		strictTypes
	});
}
/**
* Create a visitor that extracts RegExpReference.
*/
function createRegExpReferenceExtractVisitor(context, { flag, exit, isUsedShortCircuit, strictTypes }) {
	const typeTracer = createTypeTracker(context);
	let stack = null;
	const regExpReferenceMap = /* @__PURE__ */ new Map();
	const regExpReferenceList = [];
	/** Verify for String.prototype.search() or String.prototype.split() */
	function verifyForSearchOrSplit(node, kind) {
		const regExpReference = regExpReferenceMap.get(node.arguments[0]);
		if (regExpReference == null || isUsedShortCircuit(regExpReference)) return;
		if (strictTypes ? !typeTracer.isString(node.callee.object) : !typeTracer.maybeString(node.callee.object)) {
			regExpReference.markAsCannotTrack();
			return;
		}
		if (kind === "search") regExpReference.markAsUsedInSearch(node.arguments[0]);
		else regExpReference.markAsUsedInSplit(node.arguments[0]);
	}
	/** Verify for RegExp.prototype.exec() or RegExp.prototype.test() */
	function verifyForExecOrTest(node, kind) {
		const regExpReference = regExpReferenceMap.get(node.callee.object);
		if (regExpReference == null || isUsedShortCircuit(regExpReference)) return;
		if (kind === "exec") regExpReference.markAsUsedInExec(node.callee.object, stack.codePathId, stack.loopStack[0]);
		else regExpReference.markAsUsedInTest(node.callee.object, stack.codePathId, stack.loopStack[0]);
	}
	return compositingVisitors(defineRegexpVisitor(context, { createVisitor(regExpContext) {
		const { flags, regexpNode } = regExpContext;
		if (flags[flag]) {
			const regExpReference = new RegExpReference(regExpContext);
			regExpReferenceList.push(regExpReference);
			regExpReferenceMap.set(regexpNode, regExpReference);
			for (const ref of extractExpressionReferences(regexpNode, context)) if (ref.type === "argument" || ref.type === "member") {
				regExpReferenceMap.set(ref.node, regExpReference);
				regExpReference.addReadNode(ref.node);
			} else regExpReference.markAsCannotTrack();
		}
		return {};
	} }), {
		"Program:exit"() {
			exit(regExpReferenceList.filter((regExpReference) => {
				if (!regExpReference.readNodes.size) return false;
				if (regExpReference.isCannotTrack()) return false;
				if (isUsedShortCircuit(regExpReference)) return false;
				return true;
			}));
		},
		onCodePathStart(codePath) {
			stack = {
				codePathId: codePath.id,
				upper: stack,
				loopStack: []
			};
		},
		onCodePathEnd() {
			stack = stack?.upper ?? null;
		},
		["WhileStatement, DoWhileStatement, ForStatement, ForInStatement, ForOfStatement, :matches(WhileStatement, DoWhileStatement, ForStatement, ForInStatement, ForOfStatement) > :statement"](node) {
			stack?.loopStack.unshift(node);
		},
		["WhileStatement, DoWhileStatement, ForStatement, ForInStatement, ForOfStatement, :matches(WhileStatement, DoWhileStatement, ForStatement, ForInStatement, ForOfStatement) > :statement:exit"]() {
			stack?.loopStack.shift();
		},
		"Literal, NewExpression, CallExpression:exit"(node) {
			if (!stack) return;
			const regExpReference = regExpReferenceMap.get(node);
			if (!regExpReference || regExpReference.defineNode !== node) return;
			regExpReference.setDefineId(stack.codePathId, stack.loopStack[0]);
		},
		"CallExpression:exit"(node) {
			if (!stack) return;
			if (!isKnownMethodCall(node, {
				search: 1,
				split: 1,
				test: 1,
				exec: 1,
				match: 1,
				matchAll: 1,
				replace: 2,
				replaceAll: 2
			})) return;
			if (node.callee.property.name === "search" || node.callee.property.name === "split") verifyForSearchOrSplit(node, node.callee.property.name);
			else if (node.callee.property.name === "test" || node.callee.property.name === "exec") verifyForExecOrTest(node, node.callee.property.name);
			else if (node.callee.property.name === "match" || node.callee.property.name === "matchAll" || node.callee.property.name === "replace" || node.callee.property.name === "replaceAll") regExpReferenceMap.get(node.arguments[0])?.markAsUsed(node.callee.property.name, node.arguments[0]);
		}
	});
}
/**
* Create visitor for verify unnecessary flags of owned RegExp literals
*/
function createOwnedRegExpFlagsVisitor(context) {
	const sourceCode = context.sourceCode;
	/** Remove the flags of the given literal */
	function removeFlags(node) {
		const newFlags = node.regex.flags.replace(/[^u]+/gu, "");
		if (newFlags === node.regex.flags) return;
		context.report({
			node,
			loc: getFlagsLocation(sourceCode, node, node),
			messageId: "uselessFlagsOwned",
			fix(fixer) {
				const range = getFlagsRange(node);
				return fixer.replaceTextRange(range, newFlags);
			}
		});
	}
	return defineRegexpVisitor(context, { createSourceVisitor(regExpContext) {
		const { patternSource, regexpNode } = regExpContext;
		if (patternSource.isStringValue()) patternSource.getOwnedRegExpLiterals().forEach(removeFlags);
		else if (regexpNode.arguments.length >= 2) {
			const ownedNode = patternSource.regexpValue?.ownedNode;
			if (ownedNode) removeFlags(ownedNode);
		}
		return {};
	} });
}
function parseOption$1(userOption) {
	const ignore = /* @__PURE__ */ new Set();
	let strictTypes = true;
	if (userOption) {
		for (const i of userOption.ignore ?? []) ignore.add(i);
		if (userOption.strictTypes != null) strictTypes = userOption.strictTypes;
	}
	return {
		ignore,
		strictTypes
	};
}
var no_useless_flag_default = createRule("no-useless-flag", {
	meta: {
		docs: {
			description: "disallow unnecessary regex flags",
			category: "Best Practices",
			recommended: true,
			default: "warn"
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: {
				ignore: {
					type: "array",
					items: { enum: [
						"i",
						"m",
						"s",
						"g",
						"y"
					] },
					uniqueItems: true
				},
				strictTypes: { type: "boolean" }
			},
			additionalProperties: false
		}],
		messages: {
			uselessIgnoreCaseFlag: "The 'i' flag is unnecessary because the pattern only contains case-invariant characters.",
			uselessMultilineFlag: "The 'm' flag is unnecessary because the pattern does not contain start (^) or end ($) assertions.",
			uselessDotAllFlag: "The 's' flag is unnecessary because the pattern does not contain dots (.).",
			uselessGlobalFlag: "The 'g' flag is unnecessary because the regex does not use global search.",
			uselessGlobalFlagForTest: "The 'g' flag is unnecessary because the regex is used only once in 'RegExp.prototype.test'.",
			uselessGlobalFlagForExec: "The 'g' flag is unnecessary because the regex is used only once in 'RegExp.prototype.exec'.",
			uselessGlobalFlagForSplit: "The 'g' flag is unnecessary because 'String.prototype.split' ignores the 'g' flag.",
			uselessGlobalFlagForSearch: "The 'g' flag is unnecessary because 'String.prototype.search' ignores the 'g' flag.",
			uselessStickyFlag: "The 'y' flag is unnecessary because 'String.prototype.split' ignores the 'y' flag.",
			uselessFlagsOwned: "The flags of this RegExp literal are useless because only the source of the regex is used."
		},
		type: "suggestion"
	},
	create(context) {
		const { ignore, strictTypes } = parseOption$1(context.options[0]);
		let visitor = {};
		if (!ignore.has("i")) visitor = compositingVisitors(visitor, createUselessIgnoreCaseFlagVisitor(context));
		if (!ignore.has("m")) visitor = compositingVisitors(visitor, createUselessMultilineFlagVisitor(context));
		if (!ignore.has("s")) visitor = compositingVisitors(visitor, createUselessDotAllFlagVisitor(context));
		if (!ignore.has("g")) visitor = compositingVisitors(visitor, createUselessGlobalFlagVisitor(context, strictTypes));
		if (!ignore.has("y")) visitor = compositingVisitors(visitor, createUselessStickyFlagVisitor(context, strictTypes));
		visitor = compositingVisitors(visitor, createOwnedRegExpFlagsVisitor(context));
		return visitor;
	}
});
//#endregion
//#region lib/rules/no-useless-lazy.ts
/**
* Returns a fix that makes the given quantifier greedy.
*/
function makeGreedy({ patternSource }, qNode) {
	return (fixer) => {
		if (qNode.greedy) return null;
		const range = patternSource.getReplaceRange({
			start: qNode.end - 1,
			end: qNode.end
		});
		if (!range) return null;
		return range.remove(fixer);
	};
}
/**
* Returns the source location of the lazy modifier of the given quantifier.
*/
function getLazyLoc({ getRegexpLocation }, qNode) {
	const offset = qNode.raw.length - 1;
	return getRegexpLocation(qNode, [offset, offset + 1]);
}
var no_useless_lazy_default = createRule("no-useless-lazy", {
	meta: {
		docs: {
			description: "disallow unnecessarily non-greedy quantifiers",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: {
			constant: "Unexpected non-greedy constant quantifier.",
			possessive: "Unexpected non-greedy constant quantifier. The quantifier is effectively possessive, so it doesn't matter whether it is greedy or not."
		},
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, flags } = regexpContext;
			return { onQuantifierEnter(qNode) {
				if (qNode.greedy) return;
				if (qNode.min === qNode.max) {
					context.report({
						node,
						loc: getLazyLoc(regexpContext, qNode),
						messageId: "constant",
						fix: makeGreedy(regexpContext, qNode)
					});
					return;
				}
				const matchingDir = getMatchingDirection(qNode);
				const firstChar = getFirstConsumedChar(qNode.element, matchingDir, flags);
				if (!firstChar.empty) {
					const after = getFirstCharAfter(qNode, matchingDir, flags);
					if (firstChar.char.isDisjointWith(after.char)) context.report({
						node,
						loc: getLazyLoc(regexpContext, qNode),
						messageId: "possessive",
						fix: makeGreedy(regexpContext, qNode)
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-useless-non-capturing-group.ts
/**
* Returns whether the given group is the top-level group of its pattern.
*
* A pattern with a top-level groups is of the form `/(?:...)/flags`.
*/
function isTopLevel(group) {
	const parent = group.parent;
	if (parent.type === "Alternative" && parent.elements.length === 1) {
		const parentParent = parent.parent;
		if (parentParent.type === "Pattern" && parentParent.alternatives.length === 1) return true;
	}
	return false;
}
var no_useless_non_capturing_group_default = createRule("no-useless-non-capturing-group", {
	meta: {
		docs: {
			description: "disallow unnecessary non-capturing group",
			category: "Stylistic Issues",
			recommended: true
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { allowTop: { anyOf: [{ type: "boolean" }, { enum: [
				"always",
				"never",
				"partial"
			] }] } },
			additionalProperties: false
		}],
		messages: { unexpected: "Unexpected unnecessary non-capturing group. This group can be removed without changing the behaviour of the regex." },
		type: "suggestion"
	},
	create(context) {
		const allowTop = context.options[0]?.allowTop === true ? "always" : context.options[0]?.allowTop === false ? "never" : context.options[0]?.allowTop ?? "partial";
		function createVisitor({ node, getRegexpLocation, fixReplaceNode, getUsageOfPattern }) {
			let isIgnored;
			if (allowTop === "always") isIgnored = isTopLevel;
			else if (allowTop === "partial") if (getUsageOfPattern() !== UsageOfPattern.whole) isIgnored = isTopLevel;
			else isIgnored = () => false;
			else isIgnored = () => false;
			return { onGroupEnter(gNode) {
				if (isIgnored(gNode)) return;
				if (gNode.alternatives.length === 1) {
					const alt = gNode.alternatives[0];
					if (alt.elements.length === 0) return;
					if (gNode.parent.type === "Quantifier" && (alt.elements.length > 1 || alt.elements[0].type === "Quantifier")) return;
					if (!canUnwrapped(gNode, alt.raw)) return;
				} else {
					const parent = gNode.parent;
					if (parent.type !== "Alternative") return;
					if (parent.elements.length !== 1) return;
				}
				context.report({
					node,
					loc: getRegexpLocation(gNode, [0, 3]),
					messageId: "unexpected",
					fix: fixReplaceNode(gNode, () => {
						if (allowTop === "never" && isTopLevel(gNode) && getUsageOfPattern() !== UsageOfPattern.whole) return null;
						return gNode.raw.slice(3, -1);
					})
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-useless-quantifier.ts
var no_useless_quantifier_default = createRule("no-useless-quantifier", {
	meta: {
		docs: {
			description: "disallow quantifiers that can be removed",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: {
			constOne: "Unexpected useless quantifier.",
			empty: "Unexpected useless quantifier. The quantified element doesn't consume or assert characters.",
			emptyQuestionMark: "Unexpected useless quantifier. The quantified element can already accept the empty string, so this quantifier is redundant.",
			zeroLength: "Unexpected useless quantifier. The quantified element doesn't consume characters.",
			remove: "Remove the '{{quant}}' quantifier."
		},
		type: "suggestion",
		hasSuggestions: true
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation, fixReplaceNode } = regexpContext;
			/**
			* Returns a fix that replaces the given quantifier with its
			* quantified element
			*/
			function fixRemoveQuant(qNode) {
				return fixReplaceNode(qNode, () => {
					const text = qNode.element.raw;
					return canUnwrapped(qNode, text) ? text : null;
				});
			}
			/**
			* Returns a suggestion that replaces the given quantifier with its
			* quantified element
			*/
			function suggestRemoveQuant(qNode) {
				return {
					messageId: "remove",
					data: { quant: qNode.raw.slice(qNode.element.end - qNode.start) },
					fix: fixReplaceNode(qNode, () => {
						const text = qNode.element.raw;
						return canUnwrapped(qNode, text) ? text : null;
					})
				};
			}
			return { onQuantifierEnter(qNode) {
				if (qNode.min === 1 && qNode.max === 1) {
					context.report({
						node,
						loc: getRegexpLocation(qNode),
						messageId: "constOne",
						fix: fixRemoveQuant(qNode)
					});
					return;
				}
				if (isEmpty(qNode.element, flags)) {
					context.report({
						node,
						loc: getRegexpLocation(qNode),
						messageId: "empty",
						suggest: [suggestRemoveQuant(qNode)]
					});
					return;
				}
				if (qNode.min === 0 && qNode.max === 1 && qNode.greedy && isPotentiallyEmpty(qNode.element, flags)) {
					context.report({
						node,
						loc: getRegexpLocation(qNode),
						messageId: "emptyQuestionMark",
						suggest: [suggestRemoveQuant(qNode)]
					});
					return;
				}
				if (qNode.min >= 1 && isZeroLength(qNode.element, flags)) context.report({
					node,
					loc: getRegexpLocation(qNode),
					messageId: "zeroLength",
					suggest: [suggestRemoveQuant(qNode)]
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-useless-range.ts
var no_useless_range_default = createRule("no-useless-range", {
	meta: {
		docs: {
			description: "disallow unnecessary character ranges",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { unexpected: "Unexpected unnecessary character ranges. The hyphen is unnecessary." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, fixReplaceNode, getRegexpLocation }) {
			return { onCharacterClassRangeEnter(ccrNode) {
				if (ccrNode.min.value !== ccrNode.max.value && ccrNode.min.value + 1 !== ccrNode.max.value) return;
				context.report({
					node,
					loc: getRegexpLocation(ccrNode),
					messageId: "unexpected",
					fix: fixReplaceNode(ccrNode, () => {
						const parent = ccrNode.parent;
						const rawBefore = parent.raw.slice(0, ccrNode.start - parent.start);
						const rawAfter = parent.raw.slice(ccrNode.end - parent.start);
						if (/\\(?:x[\dA-Fa-f]?|u[\dA-Fa-f]{0,3})?$/u.test(rawBefore)) return null;
						let text = ccrNode.min.raw;
						if (ccrNode.min.value < ccrNode.max.value) if (ccrNode.max.raw === "-") text += `\\-`;
						else text += `${ccrNode.max.raw}`;
						if (rawAfter[0] === "-") text += "\\";
						return text;
					})
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-useless-set-operand.ts
function getFlatElements(node) {
	if (node.type === "ClassStringDisjunction") return node.alternatives;
	if (node.type === "CharacterClass") {
		const nested = [];
		const addElement = (element) => {
			if (element.type === "ClassStringDisjunction") nested.push(...element.alternatives);
			else if (element.type === "CharacterClass") {
				if (!element.negate) nested.push(...element.elements);
				nested.push(element);
			} else nested.push(element);
		};
		node.elements.forEach(addElement);
		return nested;
	}
	return [];
}
function removeDescendant(root, e) {
	let { start, end } = e;
	if (e.type === "StringAlternative") if (e.parent.alternatives.length === 1) {
		e = e.parent;
		start = e.start;
		end = e.end;
	} else if (e.parent.alternatives.at(-1) === e) start--;
	else end++;
	return root.raw.slice(0, start - root.start) + root.raw.slice(end - root.start);
}
var no_useless_set_operand_default = createRule("no-useless-set-operand", {
	meta: {
		docs: {
			description: "disallow unnecessary elements in expression character classes",
			category: "Best Practices",
			recommended: true
		},
		schema: [],
		messages: {
			intersectionDisjoint: "'{{left}}' and '{{right}}' are disjoint, so the result of the intersection is always going to be the empty set.",
			intersectionSubset: "'{{sub}}' is a subset of '{{super}}', so the result of the intersection is always going to be '{{sub}}'.",
			intersectionRemove: "'{{expr}}' can be removed without changing the result of the intersection.",
			subtractionDisjoint: "'{{left}}' and '{{right}}' are disjoint, so the subtraction doesn't do anything.",
			subtractionSubset: "'{{left}}' is a subset of '{{right}}', so the result of the subtraction is always going to be the empty set.",
			subtractionRemove: "'{{expr}}' can be removed without changing the result of the subtraction."
		},
		fixable: "code",
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation, fixReplaceNode } = regexpContext;
			if (!flags.unicodeSets) return {};
			function fixRemoveExpression(expr) {
				if (expr.parent.type === "ExpressionCharacterClass") {
					const cc = expr.parent;
					return fixReplaceNode(cc, cc.negate ? "[^]" : "[]");
				}
				return fixReplaceNode(expr, "[]");
			}
			return {
				onClassIntersectionEnter(iNode) {
					const leftSet = toUnicodeSet(iNode.left, flags);
					const rightSet = toUnicodeSet(iNode.right, flags);
					if (leftSet.isDisjointWith(rightSet)) {
						context.report({
							node,
							loc: getRegexpLocation(iNode),
							messageId: "intersectionDisjoint",
							data: {
								left: iNode.left.raw,
								right: iNode.right.raw
							},
							fix: fixRemoveExpression(iNode)
						});
						return;
					}
					if (leftSet.isSubsetOf(rightSet)) {
						context.report({
							node,
							loc: getRegexpLocation(iNode),
							messageId: "intersectionSubset",
							data: {
								sub: iNode.left.raw,
								super: iNode.right.raw
							},
							fix: fixReplaceNode(iNode, iNode.left.raw)
						});
						return;
					}
					if (rightSet.isSubsetOf(leftSet)) {
						context.report({
							node,
							loc: getRegexpLocation(iNode),
							messageId: "intersectionSubset",
							data: {
								sub: iNode.right.raw,
								super: iNode.left.raw
							},
							fix: fixReplaceNode(iNode, iNode.right.raw)
						});
						return;
					}
					const toRemoveRight = getFlatElements(iNode.right).filter((e) => leftSet.isDisjointWith(toUnicodeSet(e, flags)));
					const toRemoveLeft = getFlatElements(iNode.left).filter((e) => rightSet.isDisjointWith(toUnicodeSet(e, flags)));
					for (const e of [...toRemoveRight, ...toRemoveLeft]) context.report({
						node,
						loc: getRegexpLocation(e),
						messageId: "subtractionRemove",
						data: { expr: e.raw },
						fix: fixReplaceNode(iNode, removeDescendant(iNode, e))
					});
				},
				onClassSubtractionEnter(sNode) {
					const leftSet = toUnicodeSet(sNode.left, flags);
					const rightSet = toUnicodeSet(sNode.right, flags);
					if (leftSet.isDisjointWith(rightSet)) {
						context.report({
							node,
							loc: getRegexpLocation(sNode),
							messageId: "subtractionDisjoint",
							data: {
								left: sNode.left.raw,
								right: sNode.right.raw
							},
							fix: fixReplaceNode(sNode, sNode.left.raw)
						});
						return;
					}
					if (leftSet.isSubsetOf(rightSet)) {
						context.report({
							node,
							loc: getRegexpLocation(sNode),
							messageId: "subtractionSubset",
							data: {
								left: sNode.left.raw,
								right: sNode.right.raw
							},
							fix: fixRemoveExpression(sNode)
						});
						return;
					}
					const toRemove = getFlatElements(sNode.right).filter((e) => leftSet.isDisjointWith(toUnicodeSet(e, flags)));
					for (const e of toRemove) context.report({
						node,
						loc: getRegexpLocation(e),
						messageId: "subtractionRemove",
						data: { expr: e.raw },
						fix: fixReplaceNode(sNode, removeDescendant(sNode, e))
					});
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-useless-string-literal.ts
var no_useless_string_literal_default = createRule("no-useless-string-literal", {
	meta: {
		docs: {
			description: "disallow string disjunction of single characters in `\\q{...}`",
			category: "Best Practices",
			recommended: true
		},
		schema: [],
		messages: { unexpected: "Unexpected string disjunction of single character." },
		type: "suggestion",
		fixable: "code"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, getRegexpLocation, fixReplaceNode, pattern } = regexpContext;
			return { onStringAlternativeEnter(saNode) {
				if (saNode.elements.length === 1) {
					const csdNode = saNode.parent;
					context.report({
						node,
						loc: getRegexpLocation(saNode),
						messageId: "unexpected",
						fix: fixReplaceNode(csdNode, () => {
							const alternativesText = csdNode.alternatives.filter((alt) => alt !== saNode).map((alt) => alt.raw).join("|");
							if (!alternativesText.length) return `${isNeedEscapeForAdjacentPreviousCharacter(csdNode, saNode) || isNeedEscapeForAdjacentNextCharacter(csdNode, saNode) ? "\\" : ""}${saNode.raw}`;
							if (csdNode.parent.type === "ClassIntersection" || csdNode.parent.type === "ClassSubtraction") {
								const escape = saNode.raw === "^" ? "\\" : "";
								return String.raw`[${escape}${saNode.raw}\q{${alternativesText}}]`;
							}
							const escape = isNeedEscapeForAdjacentPreviousCharacter(csdNode, saNode) ? "\\" : "";
							return String.raw`${escape}${saNode.raw}\q{${alternativesText}}`;
						})
					});
				}
			} };
			/**
			* Checks whether the given character requires escaping
			* when adjacent to the previous character.
			*/
			function isNeedEscapeForAdjacentPreviousCharacter(disjunction, character) {
				const char = character.raw;
				if (RESERVED_DOUBLE_PUNCTUATOR_CHARS.has(char) && pattern[disjunction.start - 1] === char) return true;
				return char === "^" && disjunction.parent.type === "CharacterClass" && disjunction.parent.start === disjunction.start - 1;
			}
			/**
			* Checks whether the given character requires escaping
			* when adjacent to the next character.
			*/
			function isNeedEscapeForAdjacentNextCharacter(disjunction, character) {
				const char = character.raw;
				return RESERVED_DOUBLE_PUNCTUATOR_CHARS.has(char) && pattern[disjunction.end] === char;
			}
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-useless-two-nums-quantifier.ts
var no_useless_two_nums_quantifier_default = createRule("no-useless-two-nums-quantifier", {
	meta: {
		docs: {
			description: "disallow unnecessary `{n,m}` quantifier",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { unexpected: "Unexpected quantifier '{{expr}}'." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, getRegexpLocation, fixReplaceQuant }) {
			return { onQuantifierEnter(qNode) {
				if (qNode.min === qNode.max) {
					const [startOffset, endOffset] = getQuantifierOffsets(qNode);
					const text = qNode.raw.slice(startOffset, endOffset);
					if (!/^\{\d+,\d+\}$/u.test(text)) return;
					context.report({
						node,
						loc: getRegexpLocation(qNode, [startOffset, endOffset]),
						messageId: "unexpected",
						data: { expr: text },
						fix: fixReplaceQuant(qNode, `{${qNode.min}}`)
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/no-zero-quantifier.ts
var no_zero_quantifier_default = createRule("no-zero-quantifier", {
	meta: {
		docs: {
			description: "disallow quantifiers with a maximum of zero",
			category: "Best Practices",
			recommended: true
		},
		schema: [],
		messages: {
			unexpected: "Unexpected zero quantifier. The quantifier and its quantified element can be removed without affecting the pattern.",
			withCapturingGroup: "Unexpected zero quantifier. The quantifier and its quantified element do not affecting the pattern. Try to remove the elements but be careful because it contains at least one capturing group.",
			remove: "Remove this zero quantifier."
		},
		type: "suggestion",
		hasSuggestions: true
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, getRegexpLocation, fixReplaceNode, patternAst } = regexpContext;
			return { onQuantifierEnter(qNode) {
				if (qNode.max === 0) if (hasSomeDescendant(qNode, (n) => n.type === "CapturingGroup")) context.report({
					node,
					loc: getRegexpLocation(qNode),
					messageId: "withCapturingGroup"
				});
				else {
					const suggest = [];
					if (patternAst.raw === qNode.raw) suggest.push({
						messageId: "remove",
						fix: fixReplaceNode(qNode, "(?:)")
					});
					else if (canUnwrapped(qNode, "")) suggest.push({
						messageId: "remove",
						fix: fixReplaceNode(qNode, "")
					});
					context.report({
						node,
						loc: getRegexpLocation(qNode),
						messageId: "unexpected",
						suggest
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/optimal-lookaround-quantifier.ts
/**
* Extract invalid quantifiers for lookarounds
*/
function* extractInvalidQuantifiers(alternatives, kind) {
	for (const { elements } of alternatives) if (elements.length > 0) {
		const last = elements[kind === "lookahead" ? elements.length - 1 : 0];
		switch (last.type) {
			case "Quantifier":
				if (last.min !== last.max) if (hasSomeDescendant(last.element, (d) => d.type === "CapturingGroup")) {} else yield last;
				break;
			case "Group":
				yield* extractInvalidQuantifiers(last.alternatives, kind);
				break;
			default: break;
		}
	}
}
const END_START_PHRASE = {
	lookahead: "end",
	lookbehind: "start"
};
var optimal_lookaround_quantifier_default = createRule("optimal-lookaround-quantifier", {
	meta: {
		docs: {
			description: "disallow the alternatives of lookarounds that end with a non-constant quantifier",
			category: "Best Practices",
			recommended: true,
			default: "warn"
		},
		schema: [],
		hasSuggestions: true,
		messages: {
			remove: "The quantified expression {{expr}} at the {{endOrStart}} of the expression tree should only be matched a constant number of times. The expression can be removed without affecting the lookaround.",
			replacedWith: "The quantified expression {{expr}} at the {{endOrStart}} of the expression tree should only be matched a constant number of times. The expression can be replaced with {{replacer}} without affecting the lookaround.",
			suggestRemove: "Remove the expression.",
			suggestReplace: "Replace the expression with {{replacer}}."
		},
		type: "problem"
	},
	create(context) {
		function createVisitor({ node, getRegexpLocation, fixReplaceNode }) {
			return { onAssertionEnter(aNode) {
				if (aNode.kind === "lookahead" || aNode.kind === "lookbehind") {
					const endOrStart = END_START_PHRASE[aNode.kind];
					const quantifiers = extractInvalidQuantifiers(aNode.alternatives, aNode.kind);
					for (const q of quantifiers) {
						const replacer = q.min === 0 ? "" : q.min === 1 ? `'${q.element.raw}' (no quantifier)` : `'${q.element.raw}{${q.min}}'`;
						context.report({
							node,
							loc: getRegexpLocation(q),
							messageId: q.min === 0 ? "remove" : "replacedWith",
							data: {
								expr: mention(q),
								endOrStart,
								replacer
							},
							suggest: [{
								messageId: q.min === 0 ? "suggestRemove" : "suggestReplace",
								data: { replacer },
								fix: fixReplaceNode(q, () => {
									if (q.min === 0) return "";
									else if (q.min === 1) return q.element.raw;
									return `${q.element.raw}{${q.min}}`;
								})
							}]
						});
					}
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/optimal-quantifier-concatenation.ts
const EMPTY_UTF16 = {
	char: Chars.empty({}),
	complete: false
};
const EMPTY_UNICODE = {
	char: Chars.empty({ unicode: true }),
	complete: false
};
/**
* If the given element is guaranteed to only consume a single character set,
* then this character set will be returned, `null` otherwise.
*/
function getSingleConsumedChar(element, flags) {
	const empty = flags.unicode || flags.unicodeSets ? EMPTY_UNICODE : EMPTY_UTF16;
	switch (element.type) {
		case "Alternative":
			if (element.elements.length === 1) return getSingleConsumedChar(element.elements[0], flags);
			return empty;
		case "Character":
		case "CharacterSet":
		case "CharacterClass":
		case "ExpressionCharacterClass": {
			const set = toUnicodeSet(element, flags);
			return {
				char: set.chars,
				complete: set.accept.isEmpty
			};
		}
		case "Group":
		case "CapturingGroup": {
			const results = element.alternatives.map((a) => getSingleConsumedChar(a, flags));
			return {
				char: empty.char.union(...results.map((r) => r.char)),
				complete: results.every((r) => r.complete)
			};
		}
		case "Assertion":
		case "Backreference":
		case "Quantifier": return empty;
		default: return assertNever(element);
	}
}
/**
* Returns the sum of the given quant and constant.
*/
function quantAddConst(quant, constant) {
	return {
		min: quant.min + constant,
		max: quant.max + constant,
		greedy: quant.greedy
	};
}
/**
* Returns the raw of the given quantifier.
*/
function quantize(element, quant) {
	if (quant.min === 0 && quant.max === 0) return "";
	if (quant.min === 1 && quant.max === 1) return element.raw;
	return element.raw + quantToString(quant);
}
/**
* Returns whether the given element is a group or character.
*/
function isGroupOrCharacter(element) {
	switch (element.type) {
		case "Group":
		case "CapturingGroup":
		case "Character":
		case "CharacterClass":
		case "CharacterSet":
		case "ExpressionCharacterClass": return true;
		case "Assertion":
		case "Backreference":
		case "Quantifier": return false;
		default: return assertNever(element);
	}
}
/**
* Returns the replacement for the two adjacent elements.
*/
function getQuantifiersReplacement(left, right, flags) {
	if (left.min === left.max || right.min === right.max) return null;
	if (left.greedy !== right.greedy) return null;
	const lSingle = getSingleConsumedChar(left.element, flags);
	const rSingle = getSingleConsumedChar(right.element, flags);
	const lPossibleChar = lSingle.complete ? lSingle.char : getConsumedChars(left.element, flags).chars;
	const rPossibleChar = rSingle.complete ? rSingle.char : getConsumedChars(right.element, flags).chars;
	const greedy = left.greedy;
	let lQuant, rQuant;
	if (lSingle.complete && rSingle.complete && lSingle.char.equals(rSingle.char)) {
		lQuant = {
			min: left.min + right.min,
			max: left.max + right.max,
			greedy
		};
		rQuant = {
			min: 0,
			max: 0,
			greedy
		};
	} else if (right.max === Infinity && rSingle.char.isSupersetOf(lPossibleChar)) {
		lQuant = {
			min: left.min,
			max: left.min,
			greedy
		};
		rQuant = right;
	} else if (left.max === Infinity && lSingle.char.isSupersetOf(rPossibleChar)) {
		lQuant = left;
		rQuant = {
			min: right.min,
			max: right.min,
			greedy
		};
	} else return null;
	const raw = quantize(left.element, lQuant) + quantize(right.element, rQuant);
	let messageId;
	if (lQuant.max === 0 && right.max === rQuant.max && right.min === rQuant.min) messageId = "removeLeft";
	else if (rQuant.max === 0 && left.max === lQuant.max && left.min === lQuant.min) messageId = "removeRight";
	else messageId = "replace";
	return {
		type: "Both",
		raw,
		messageId
	};
}
/**
* Tries to convert the given element into a repeated element.
*/
function asRepeatedElement(element) {
	if (element.type === "Quantifier") {
		if (element.min === element.max && element.min > 0 && isGroupOrCharacter(element.element)) return {
			type: "Repeated",
			element: element.element,
			min: element.min
		};
	} else if (isGroupOrCharacter(element)) return {
		type: "Repeated",
		element,
		min: 1
	};
	return null;
}
/**
* Returns the replacement for the two adjacent elements.
*/
function getQuantifierRepeatedElementReplacement(pair, flags) {
	const [left, right] = pair;
	const lSingle = getSingleConsumedChar(left.element, flags);
	if (!lSingle.complete) return null;
	const rSingle = getSingleConsumedChar(right.element, flags);
	if (!rSingle.complete) return null;
	if (!rSingle.char.equals(lSingle.char)) return null;
	let elementRaw, quant;
	if (left.type === "Quantifier") {
		elementRaw = left.element.raw;
		quant = quantAddConst(left, right.min);
	} else if (right.type === "Quantifier") {
		elementRaw = right.element.raw;
		quant = quantAddConst(right, left.min);
	} else throw new Error();
	return {
		type: "Both",
		messageId: "combine",
		raw: elementRaw + quantToString(quant)
	};
}
/**
* Returns a replacement for the nested quantifier.
*/
function getNestedReplacement(dominate, nested, flags) {
	if (dominate.greedy !== nested.greedy) return null;
	if (dominate.max < Infinity || nested.min === nested.max) return null;
	const single = getSingleConsumedChar(dominate.element, flags);
	if (single.char.isEmpty) return null;
	const nestedPossible = getConsumedChars(nested.element, flags);
	if (single.char.isSupersetOf(nestedPossible.chars)) {
		const { min } = nested;
		if (min === 0) return {
			type: "Nested",
			messageId: "nestedRemove",
			raw: "",
			nested,
			dominate
		};
		return {
			type: "Nested",
			messageId: "nestedReplace",
			raw: quantize(nested.element, {
				...nested,
				max: min
			}),
			nested,
			dominate
		};
	}
	return null;
}
/** Yields all quantifiers at the start/end of the given element. */
function* nestedQuantifiers(root, direction) {
	switch (root.type) {
		case "Alternative":
			if (root.elements.length > 0) {
				const index = direction === "start" ? 0 : root.elements.length - 1;
				yield* nestedQuantifiers(root.elements[index], direction);
			}
			break;
		case "CapturingGroup":
		case "Group":
			for (const a of root.alternatives) yield* nestedQuantifiers(a, direction);
			break;
		case "Quantifier":
			yield root;
			if (root.max === 1) yield* nestedQuantifiers(root.element, direction);
			break;
		default: break;
	}
}
/**
* Whether the computed replacement is to be ignored.
*/
function ignoreReplacement(left, right, result) {
	if (left.type === "Quantifier") {
		if (left.raw.length + right.raw.length <= result.raw.length && isGroupOrCharacter(right) && left.min === 0 && left.max === 1) return true;
	}
	if (right.type === "Quantifier") {
		if (left.raw.length + right.raw.length <= result.raw.length && isGroupOrCharacter(left) && right.min === 0 && right.max === 1) return true;
	}
	return false;
}
/**
* Returns the replacement for the two adjacent elements.
*/
function getReplacement(left, right, flags) {
	if (left.type === "Quantifier" && right.type === "Quantifier") {
		const result = getQuantifiersReplacement(left, right, flags);
		if (result && !ignoreReplacement(left, right, result)) return result;
	}
	if (left.type === "Quantifier") {
		const rightRep = asRepeatedElement(right);
		if (rightRep) {
			const result = getQuantifierRepeatedElementReplacement([left, rightRep], flags);
			if (result && !ignoreReplacement(left, right, result)) return result;
		}
	}
	if (right.type === "Quantifier") {
		const leftRep = asRepeatedElement(left);
		if (leftRep) {
			const result = getQuantifierRepeatedElementReplacement([leftRep, right], flags);
			if (result && !ignoreReplacement(left, right, result)) return result;
		}
	}
	if (left.type === "Quantifier" && left.max === Infinity) for (const nested of nestedQuantifiers(right, "start")) {
		const result = getNestedReplacement(left, nested, flags);
		if (result) return result;
	}
	if (right.type === "Quantifier" && right.max === Infinity) for (const nested of nestedQuantifiers(left, "end")) {
		const result = getNestedReplacement(right, nested, flags);
		if (result) return result;
	}
	return null;
}
/**
* Returns the combined location of two adjacent elements.
*/
function getLoc(left, right, { patternSource }) {
	return patternSource.getAstLocation({
		start: Math.min(left.start, right.start),
		end: Math.max(left.end, right.end)
	});
}
/**
* Returns a string representation of all capturing groups that the given
* element is inside of.
*
* This function is guaranteed to return the same value for 2 elements that are
* inside the same set of capturing groups.
*
* Note: The string itself is likely nonsensical.
*/
function getCapturingGroupStack(element) {
	let result = "";
	for (let p = element.parent; p.type !== "Pattern"; p = p.parent) if (p.type === "CapturingGroup") {
		const id = p.start;
		result += String.fromCodePoint(32 + id);
	}
	return result;
}
var CapturingGroupReporting = /* @__PURE__ */ function(CapturingGroupReporting) {
	CapturingGroupReporting["ignore"] = "ignore";
	CapturingGroupReporting["report"] = "report";
	return CapturingGroupReporting;
}(CapturingGroupReporting || {});
var optimal_quantifier_concatenation_default = createRule("optimal-quantifier-concatenation", {
	meta: {
		docs: {
			description: "require optimal quantifiers for concatenated quantifiers",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { capturingGroups: { enum: ["ignore", "report"] } },
			additionalProperties: false
		}],
		messages: {
			combine: "{{left}} and {{right}} can be combined into one quantifier {{fix}}.{{cap}}",
			removeLeft: "{{left}} can be removed because it is already included by {{right}}.{{cap}}",
			removeRight: "{{right}} can be removed because it is already included by {{left}}.{{cap}}",
			replace: "{{left}} and {{right}} can be replaced with {{fix}}.{{cap}}",
			nestedRemove: "{{nested}} can be removed because of {{dominate}}.{{cap}}",
			nestedReplace: "{{nested}} can be replaced with {{fix}} because of {{dominate}}.{{cap}}",
			removeQuant: "{{quant}} can be removed because it is already included by {{cause}}.{{cap}}",
			replaceQuant: "{{quant}} can be replaced with {{fix}} because of {{cause}}.{{cap}}"
		},
		type: "suggestion"
	},
	create(context) {
		const cgReporting = context.options[0]?.capturingGroups ?? CapturingGroupReporting.report;
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation, fixReplaceNode } = regexpContext;
			const parser = getParser(regexpContext);
			const simplifiedAlready = [];
			/** Returns whether the given element is included an element that was processed already. */
			function isSimplifiedAlready(element) {
				return simplifiedAlready.some((q) => {
					return hasSomeDescendant(q, element);
				});
			}
			return {
				onQuantifierEnter(quantifier) {
					const result = canSimplifyQuantifier(quantifier, flags, parser);
					if (!result.canSimplify) return;
					const quantStack = getCapturingGroupStack(quantifier);
					const crossesCapturingGroup = result.dependencies.some((e) => getCapturingGroupStack(e) !== quantStack);
					const removesCapturingGroup = quantifier.min === 0 && hasCapturingGroup(quantifier);
					const involvesCapturingGroup = removesCapturingGroup || crossesCapturingGroup;
					if (involvesCapturingGroup && cgReporting === CapturingGroupReporting.ignore) return;
					simplifiedAlready.push(quantifier, ...result.dependencies);
					const cause = joinEnglishList(result.dependencies.map((d) => mention(d)));
					const [replacement, fix] = fixSimplifyQuantifier(quantifier, result, regexpContext);
					if (quantifier.min === 0) {
						const cap = involvesCapturingGroup ? removesCapturingGroup ? " This cannot be fixed automatically because it removes a capturing group." : " This cannot be fixed automatically because it involves a capturing group." : "";
						context.report({
							node,
							loc: getRegexpLocation(quantifier),
							messageId: "removeQuant",
							data: {
								quant: mention(quantifier),
								cause,
								cap
							},
							fix: involvesCapturingGroup ? void 0 : fix
						});
					} else {
						const cap = involvesCapturingGroup ? " This cannot be fixed automatically because it involves a capturing group." : "";
						context.report({
							node,
							loc: getRegexpLocation(quantifier),
							messageId: "replaceQuant",
							data: {
								quant: mention(quantifier),
								fix: mention(replacement),
								cause,
								cap
							},
							fix: involvesCapturingGroup ? void 0 : fix
						});
					}
				},
				onAlternativeLeave(aNode) {
					for (let i = 0; i < aNode.elements.length - 1; i++) {
						const left = aNode.elements[i];
						const right = aNode.elements[i + 1];
						if (isSimplifiedAlready(left) || isSimplifiedAlready(right)) continue;
						const replacement = getReplacement(left, right, flags);
						if (!replacement) continue;
						const involvesCapturingGroup = hasCapturingGroup(left) || hasCapturingGroup(right);
						if (involvesCapturingGroup && cgReporting === CapturingGroupReporting.ignore) continue;
						const cap = involvesCapturingGroup ? " This cannot be fixed automatically because it might change or remove a capturing group." : "";
						if (replacement.type === "Both") context.report({
							node,
							loc: getLoc(left, right, regexpContext),
							messageId: replacement.messageId,
							data: {
								left: mention(left),
								right: mention(right),
								fix: mention(replacement.raw),
								cap
							},
							fix: fixReplaceNode(aNode, () => {
								if (involvesCapturingGroup) return null;
								const before = aNode.raw.slice(0, left.start - aNode.start);
								const after = aNode.raw.slice(right.end - aNode.start);
								return before + replacement.raw + after;
							})
						});
						else context.report({
							node,
							loc: getRegexpLocation(replacement.nested),
							messageId: replacement.messageId,
							data: {
								nested: mention(replacement.nested),
								dominate: mention(replacement.dominate),
								fix: mention(replacement.raw),
								cap
							},
							fix: fixReplaceNode(replacement.nested, () => {
								if (involvesCapturingGroup) return null;
								return replacement.raw;
							})
						});
					}
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-character-class.ts
/**
* Find the first index of an element that satisfies the given condition.
*/
function findIndex(arr, condFn) {
	return arr.findIndex(condFn);
}
/**
* Find the last index of an element that satisfies the given condition.
*/
function findLastIndex(arr, condFn) {
	for (let i = arr.length - 1; i >= 0; i--) if (condFn(arr[i], i)) return i;
	return -1;
}
/**
* Returns the string representation of the given character class elements in a character class.
*/
function elementsToCharacterClass(elements) {
	const parts = [];
	elements.forEach((e) => {
		switch (e.type) {
			case "Character":
				if (e.raw === "-") parts.push("\\-");
				else if (e.raw === "]") parts.push("\\]");
				else parts.push(e.raw);
				break;
			case "CharacterClassRange":
			case "CharacterSet":
			case "CharacterClass":
			case "ClassStringDisjunction":
			case "ExpressionCharacterClass":
				parts.push(e.raw);
				break;
			default: throw assertNever(e);
		}
	});
	if (parts.length > 0 && parts[0][0] === "^") parts[0] = `\\${parts[0]}`;
	for (let i = 1; i < parts.length; i++) {
		const prev = parts[i - 1];
		const curr = parts[i];
		const pChar = prev.slice(-1);
		const cChar = curr[0];
		if (RESERVED_DOUBLE_PUNCTUATOR_CHARS.has(cChar) && cChar === pChar && !prev.endsWith(`\\${pChar}`)) parts[i - 1] = `${prev.slice(0, -1)}\\${pChar}`;
	}
	return `[${parts.join("")}]`;
}
/**
* Given alternatives, this will return an array in which each alternative is categorized by whether it contains only a
* single character (that can be combined with other characters in a character class) or not.
*/
function categorizeRawAlts(alternatives, flags) {
	return alternatives.map((alternative) => {
		if (alternative.elements.length === 1) {
			const element = alternative.elements[0];
			if (element.type === "Character" || element.type === "CharacterClass" || element.type === "CharacterSet" || element.type === "ExpressionCharacterClass") {
				const set = toUnicodeSet(element, flags);
				if (set.accept.isEmpty) return {
					isCharacter: true,
					alternative,
					char: set.chars,
					element
				};
			}
		}
		return {
			isCharacter: false,
			alternative
		};
	});
}
/**
* Returns whether the given set contains a character class.
*/
function containsCharacterClass(alts) {
	for (const alt of alts) if (alt.isCharacter && alt.alternative.elements.length === 1) {
		const e = alt.alternative.elements[0];
		if (e.type === "CharacterClass" && !e.negate) return true;
	}
	return false;
}
/**
* Tries to convert the given element into character class elements.
*
* The returned array may be empty.
*/
function toCharacterClassElement(element) {
	switch (element.type) {
		case "Character": return [element];
		case "CharacterSet":
			if (element.kind === "any") return null;
			return [element];
		case "CharacterClass":
			if (element.negate) {
				if (element.unicodeSets) return [element];
				return null;
			}
			return element.elements;
		case "ExpressionCharacterClass": return [element];
		default: return assertNever(element);
	}
}
/**
* Parses the given raw alternatives.
*/
function parseRawAlts(alternatives, flags) {
	return alternatives.map((a) => {
		if (a.isCharacter) {
			const elements = toCharacterClassElement(a.element);
			if (elements) return {
				isCharacter: true,
				elements,
				char: a.char,
				raw: a.alternative.raw
			};
		}
		return {
			isCharacter: false,
			firstChar: getFirstConsumedChar(a.alternative, getMatchingDirection(a.alternative), flags),
			raw: a.alternative.raw
		};
	});
}
/**
* Tries to merge as many character alternatives as possible.
*/
function optimizeCharacterAlts(alternatives) {
	/**
	* The actual merge implementation.
	*/
	function merge(a, b) {
		const elements = [...a.elements, ...b.elements];
		return {
			isCharacter: true,
			char: a.char.union(b.char),
			elements,
			raw: elementsToCharacterClass(elements)
		};
	}
	for (let i = 0; i < alternatives.length - 1; i++) {
		let curr = alternatives[i];
		if (!curr.isCharacter) continue;
		/**
		* The union of all character sets a char alternative has to be disjoint with in order to be moved.
		*/
		let nonCharTotal = void 0;
		for (let j = i + 1; j < alternatives.length; j++) {
			const far = alternatives[j];
			if (far.isCharacter) if (nonCharTotal === void 0 || far.char.isDisjointWith(nonCharTotal)) {
				curr = merge(curr, far);
				alternatives.splice(j, 1);
				j--;
			} else break;
			else if (!far.firstChar.empty) {
				if (nonCharTotal === void 0) nonCharTotal = far.firstChar.char;
				else nonCharTotal = nonCharTotal.union(far.firstChar.char);
				if (nonCharTotal.isAll) break;
			} else break;
		}
		alternatives[i] = curr;
	}
}
/**
* Return whether all character alternatives are disjoint with each other.
*/
function findNonDisjointAlt(alternatives) {
	let total = void 0;
	for (const a of alternatives) if (a.isCharacter) if (total === void 0) total = a.char;
	else {
		if (!total.isDisjointWith(a.char)) return a;
		total = total.union(a.char);
	}
	return null;
}
/**
* Returns where the given alternative can accept any character.
*/
function totalIsAll(alternatives) {
	let total = void 0;
	for (const a of alternatives) if (a.isCharacter) if (total === void 0) total = a.char;
	else total = total.union(a.char);
	return total !== void 0 && total.isAll;
}
/**
* Returns the content prefix and suffix of the given parent node.
*/
function getParentPrefixAndSuffix(parent) {
	switch (parent.type) {
		case "Assertion": return [`(?${parent.kind === "lookahead" ? "" : "<"}${parent.negate ? "!" : "="}`, ")"];
		case "CapturingGroup":
			if (parent.name !== null) return [`(?<${parent.name}>`, ")"];
			return ["(", ")"];
		case "Group": return ["(?:", ")"];
		case "Pattern": return ["", ""];
		default: return assertNever(parent);
	}
}
/**
* Returns the minimum position.
*/
function minPos(a, b) {
	if (a.column < b.column) return a;
	else if (b.column < a.column) return b;
	return a.line < b.line ? a : b;
}
/**
* Returns the maximum position.
*/
function maxPos(a, b) {
	if (a.column > b.column) return a;
	else if (b.column > a.column) return b;
	return a.line > b.line ? a : b;
}
var prefer_character_class_default = createRule("prefer-character-class", {
	meta: {
		docs: {
			description: "enforce using character class",
			category: "Stylistic Issues",
			recommended: true
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { minAlternatives: {
				type: "integer",
				minimum: 2
			} },
			additionalProperties: false
		}],
		messages: { unexpected: "Unexpected the disjunction of single element alternatives. Use character class '[...]' instead." },
		type: "suggestion"
	},
	create(context) {
		const minCharacterAlternatives = context.options[0]?.minAlternatives ?? 3;
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation, fixReplaceNode } = regexpContext;
			/**
			* Replaces the alternatives of the given node with the given
			* new alternatives.
			*/
			function fixReplaceAlternatives(n, newAlternatives) {
				const [prefix, suffix] = getParentPrefixAndSuffix(n);
				return fixReplaceNode(n, prefix + newAlternatives + suffix);
			}
			/**
			* Returns the combined location of the locations of the given
			* elements.
			*/
			function unionRegexpLocations(elements) {
				let { start, end } = getRegexpLocation(elements[0]);
				for (let i = 1; i < elements.length; i++) {
					const other = getRegexpLocation(elements[1]);
					start = minPos(start, other.start);
					end = maxPos(end, other.end);
				}
				return {
					start,
					end
				};
			}
			function process(n) {
				if (n.alternatives.length < 2) return;
				const alts = categorizeRawAlts(n.alternatives, flags);
				const characterAltsCount = alts.filter((a) => a.isCharacter).length;
				if (characterAltsCount < 2) return;
				if (alts.every((a) => a.isCharacter) && totalIsAll(alts)) {
					context.report({
						node,
						loc: getRegexpLocation(n),
						messageId: "unexpected",
						fix: fixReplaceAlternatives(n, "[^]")
					});
					return;
				}
				const parsedAlts = parseRawAlts(alts, flags);
				if (characterAltsCount >= minCharacterAlternatives || containsCharacterClass(alts) || totalIsAll(alts) || findNonDisjointAlt(parsedAlts)) {
					optimizeCharacterAlts(parsedAlts);
					if (parsedAlts.length !== alts.length) {
						const firstChanged = findIndex(parsedAlts, (a, i) => a.raw !== n.alternatives[i].raw);
						const lastChanged = findLastIndex(parsedAlts, (a, i) => {
							const index = n.alternatives.length + i - parsedAlts.length;
							return a.raw !== n.alternatives[index].raw;
						});
						const changedNodes = [n.alternatives[firstChanged], n.alternatives[n.alternatives.length + lastChanged - parsedAlts.length]];
						context.report({
							node,
							loc: unionRegexpLocations(changedNodes),
							messageId: "unexpected",
							fix: fixReplaceAlternatives(n, parsedAlts.map((a) => a.raw).join("|"))
						});
					}
				}
			}
			return {
				onPatternEnter: process,
				onGroupEnter: process,
				onCapturingGroupEnter: process,
				onAssertionEnter(aNode) {
					if (aNode.kind === "lookahead" || aNode.kind === "lookbehind") process(aNode);
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-d.ts
/**
* Returns whether the given character class element is equivalent to `\d`.
*/
function isDigits(element) {
	return element.type === "CharacterSet" && element.kind === "digit" && !element.negate || element.type === "CharacterClassRange" && element.min.value === CP_DIGIT_ZERO && element.max.value === CP_DIGIT_NINE;
}
var prefer_d_default = createRule("prefer-d", {
	meta: {
		docs: {
			description: "enforce using `\\d`",
			category: "Stylistic Issues",
			recommended: true
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { insideCharacterClass: {
				type: "string",
				enum: [
					"ignore",
					"range",
					"d"
				]
			} },
			additionalProperties: false
		}],
		messages: { unexpected: "Unexpected {{type}} {{expr}}. Use '{{instead}}' instead." },
		type: "suggestion"
	},
	create(context) {
		const insideCharacterClass = context.options[0]?.insideCharacterClass ?? "ignore";
		function createVisitor({ node, flags, getRegexpLocation, fixReplaceNode }) {
			function verifyCharacterClass(ccNode) {
				const charSet = toUnicodeSet(ccNode, flags);
				let predefined = void 0;
				if (charSet.equals(Chars.digit(flags))) predefined = "\\d";
				else if (charSet.equals(Chars.digit(flags).negate())) predefined = "\\D";
				if (predefined) {
					context.report({
						node,
						loc: getRegexpLocation(ccNode),
						messageId: "unexpected",
						data: {
							type: "character class",
							expr: mention(ccNode),
							instead: predefined
						},
						fix: fixReplaceNode(ccNode, predefined)
					});
					return;
				}
				if (insideCharacterClass === "ignore" || ccNode.type !== "CharacterClass") return;
				const expected = insideCharacterClass === "d" ? "\\d" : "0-9";
				for (const e of ccNode.elements) if (isDigits(e) && e.raw !== expected) context.report({
					node,
					loc: getRegexpLocation(e),
					messageId: "unexpected",
					data: {
						type: e.type === "CharacterSet" ? "character set" : "character class range",
						expr: mention(e),
						instead: expected
					},
					fix: fixReplaceNode(e, expected)
				});
			}
			return {
				onCharacterClassEnter: verifyCharacterClass,
				onExpressionCharacterClassEnter: verifyCharacterClass
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-escape-replacement-dollar-char.ts
var prefer_escape_replacement_dollar_char_default = createRule("prefer-escape-replacement-dollar-char", {
	meta: {
		docs: {
			description: "enforces escape of replacement `$` character (`$$`).",
			category: "Best Practices",
			recommended: false
		},
		schema: [],
		messages: { unexpected: "Unexpected replacement `$` character without escaping. Use `$$` instead." },
		type: "suggestion"
	},
	create(context) {
		const typeTracer = createTypeTracker(context);
		const sourceCode = context.sourceCode;
		function verify(replacement) {
			for (const element of parseReplacements(context, replacement)) if (element.type === "CharacterElement" && element.value === "$") context.report({
				node: replacement,
				loc: {
					start: sourceCode.getLocFromIndex(element.range[0]),
					end: sourceCode.getLocFromIndex(element.range[1])
				},
				messageId: "unexpected"
			});
		}
		return { CallExpression(node) {
			if (!isKnownMethodCall(node, {
				replace: 2,
				replaceAll: 2
			})) return;
			const mem = node.callee;
			const replacementTextNode = node.arguments[1];
			if (replacementTextNode.type !== "Literal" || typeof replacementTextNode.value !== "string") return;
			if (!typeTracer.isRegExp(node.arguments[0])) return;
			if (!typeTracer.isString(mem.object)) return;
			verify(replacementTextNode);
		} };
	}
});
//#endregion
//#region lib/rules/prefer-lookaround.ts
/**
* Holds all replacement reference data.
*
* If the same RegExp instance is used for replacement in 2 places, the number of data in `list` is 2.
*/
var ReplaceReferencesList = class {
	list;
	/** Reference name at the starting position. */
	startRefName;
	/** Reference name at the ending position. */
	endRefName;
	/** All reference names except at the starting position. */
	otherThanStartRefNames;
	/** All reference names except at the starting position. */
	otherThanEndRefNames;
	constructor(list) {
		this.list = list;
		this.startRefName = list[0].startRef?.ref;
		this.endRefName = list[0].endRef?.ref;
		const otherThanStartRefNames = /* @__PURE__ */ new Set();
		const otherThanEndRefNames = /* @__PURE__ */ new Set();
		for (const { startRef, endRef, allRefs } of this.list) for (const ref of allRefs) {
			if (ref !== startRef) otherThanStartRefNames.add(ref.ref);
			if (ref !== endRef) otherThanEndRefNames.add(ref.ref);
		}
		this.otherThanStartRefNames = otherThanStartRefNames;
		this.otherThanEndRefNames = otherThanEndRefNames;
	}
	*[Symbol.iterator]() {
		yield* this.list;
	}
};
var SideEffect = /* @__PURE__ */ function(SideEffect) {
	SideEffect[SideEffect["startRef"] = 0] = "startRef";
	SideEffect[SideEffect["endRef"] = 1] = "endRef";
	return SideEffect;
}(SideEffect || {});
/**
* Gets the type of side effect when replacing the capture group for the given element.
*
* There are no side effects if the following conditions are met:
*
* - Some elements other than the start capturing group have disjoints to the start capturing group.
* - The last element and the start consume character have disjoint.
*/
function getSideEffectsWhenReplacingCapturingGroup(elements, start, end, { flags }) {
	const result = /* @__PURE__ */ new Set();
	if (start) {
		const { chars } = getConsumedChars(start, flags);
		if (!hasDisjoint(chars, elements.slice(1))) result.add(SideEffect.startRef);
		else {
			const last = elements[elements.length - 1];
			if (!FirstConsumedChars.toLook(getFirstConsumedCharPlusAfter(last, "rtl", flags)).char.isDisjointWith(chars)) result.add(SideEffect.startRef);
		}
	}
	if (end && flags.global) {
		const first = elements[0];
		if (first) {
			const { chars } = getConsumedChars(end, flags);
			if (!FirstConsumedChars.toLook(getFirstConsumedCharPlusAfter(first, "ltr", flags)).char.isDisjointWith(chars)) result.add(SideEffect.endRef);
		}
	}
	return result;
	/** Checks whether the given target element has disjoint in elements.  */
	function hasDisjoint(target, targetElements) {
		for (const element of targetElements) if (isConstantLength(element)) {
			const elementChars = getConsumedChars(element, flags);
			if (elementChars.chars.isEmpty) continue;
			if (elementChars.chars.isDisjointWith(target)) return true;
		} else return FirstConsumedChars.toLook(getFirstConsumedCharPlusAfter(element, "ltr", flags)).char.isDisjointWith(target);
		return false;
	}
	/** Checks whether the given element is constant length. */
	function isConstantLength(target) {
		const range = getLengthRange(target, flags);
		return range.min === range.max;
	}
}
/** Checks whether the given element is a capturing group of length 1 or greater. */
function isCapturingGroupAndNotZeroLength(element, flags) {
	return element.type === "CapturingGroup" && !isZeroLength(element, flags);
}
function parsePatternElements(node, flags) {
	if (node.alternatives.length > 1) return null;
	const elements = node.alternatives[0].elements;
	const leadingElements = [];
	let start = null;
	for (const element of elements) {
		if (isZeroLength(element, flags)) {
			leadingElements.push(element);
			continue;
		}
		if (isCapturingGroupAndNotZeroLength(element, flags)) {
			const capturingGroup = element;
			start = {
				leadingElements,
				capturingGroup,
				replacedAssertion: startElementsToLookbehindAssertionText(leadingElements, capturingGroup),
				range: {
					start: (leadingElements[0] || capturingGroup).start,
					end: capturingGroup.end
				}
			};
		}
		break;
	}
	let end = null;
	const trailingElements = [];
	for (const element of [...elements].reverse()) {
		if (isZeroLength(element, flags)) {
			trailingElements.unshift(element);
			continue;
		}
		if (isCapturingGroupAndNotZeroLength(element, flags)) {
			const capturingGroup = element;
			end = {
				capturingGroup,
				trailingElements,
				replacedAssertion: endElementsToLookaheadAssertionText(capturingGroup, trailingElements),
				range: {
					start: capturingGroup.start,
					end: (trailingElements[trailingElements.length - 1] || capturingGroup).end
				}
			};
		}
		break;
	}
	if (!start && !end) return null;
	if (start && end && start.capturingGroup === end.capturingGroup) return null;
	return {
		elements,
		start,
		end
	};
}
/** Convert end capturing group to lookahead assertion text. */
function endElementsToLookaheadAssertionText(capturingGroup, trailingElements) {
	const groupPattern = capturingGroup.alternatives.map((a) => a.raw).join("|");
	const trailing = leadingTrailingElementsToLookaroundAssertionPatternText(trailingElements, "lookahead");
	if (trailing && capturingGroup.alternatives.length !== 1) return `(?=(?:${groupPattern})${trailing})`;
	return `(?=${groupPattern}${trailing})`;
}
/** Convert start capturing group to lookbehind assertion text. */
function startElementsToLookbehindAssertionText(leadingElements, capturingGroup) {
	const leading = leadingTrailingElementsToLookaroundAssertionPatternText(leadingElements, "lookbehind");
	const groupPattern = capturingGroup.alternatives.map((a) => a.raw).join("|");
	if (leading && capturingGroup.alternatives.length !== 1) return `(?<=${leading}(?:${groupPattern}))`;
	return `(?<=${leading}${groupPattern})`;
}
/** Convert leading/trailing elements to lookaround assertion pattern text. */
function leadingTrailingElementsToLookaroundAssertionPatternText(leadingTrailingElements, lookaroundAssertionKind) {
	if (leadingTrailingElements.length === 1 && leadingTrailingElements[0].type === "Assertion") {
		const assertion = leadingTrailingElements[0];
		if (assertion.kind === lookaroundAssertionKind && !assertion.negate && assertion.alternatives.length === 1) return assertion.alternatives[0].raw;
	}
	return leadingTrailingElements.map((e) => e.raw).join("");
}
function parseOption(userOption) {
	return {
		lookbehind: userOption?.lookbehind ?? true,
		strictTypes: userOption?.strictTypes ?? true
	};
}
var prefer_lookaround_default = createRule("prefer-lookaround", {
	meta: {
		docs: {
			description: "prefer lookarounds over capturing group that do not replace",
			category: "Stylistic Issues",
			recommended: false
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: {
				lookbehind: { type: "boolean" },
				strictTypes: { type: "boolean" }
			},
			additionalProperties: false
		}],
		messages: {
			preferLookarounds: "These capturing groups can be replaced with lookaround assertions ({{expr1}} and {{expr2}}).",
			prefer: "This capturing group can be replaced with a {{kind}} ({{expr}})."
		},
		type: "suggestion"
	},
	create(context) {
		const { lookbehind, strictTypes } = parseOption(context.options[0]);
		const typeTracer = createTypeTracker(context);
		function createVisitor(regexpContext) {
			const { regexpNode, flags, patternAst } = regexpContext;
			const parsedElements = parsePatternElements(patternAst, flags);
			if (!parsedElements) return {};
			const replaceReferenceList = [];
			for (const ref of extractExpressionReferences(regexpNode, context)) if (ref.type === "argument") {
				if (!isKnownMethodCall(ref.callExpression, {
					replace: 2,
					replaceAll: 2
				})) return {};
				const replaceReference = getReplaceReferenceFromCallExpression(ref.callExpression);
				if (!replaceReference) return {};
				replaceReferenceList.push(replaceReference);
			} else if (ref.type === "member") {
				const parent = getParent(ref.memberExpression);
				if (parent?.type === "CallExpression" && isKnownMethodCall(parent, { test: 1 }) && !regexpContext.flags.global) continue;
				return {};
			} else return {};
			if (!replaceReferenceList.length) return {};
			const replaceReference = replaceReferenceList[0];
			if (replaceReferenceList.some((target) => target.startRef?.ref !== replaceReference.startRef?.ref || target.endRef?.ref !== replaceReference.endRef?.ref)) return {};
			return createVerifyVisitor(regexpContext, parsedElements, new ReplaceReferencesList(replaceReferenceList));
		}
		function getReplaceReferenceFromCallExpression(node) {
			if (strictTypes ? !typeTracer.isString(node.callee.object) : !typeTracer.maybeString(node.callee.object)) return null;
			const replacementNode = node.arguments[1];
			if (replacementNode.type === "Literal") return getReplaceReferenceFromLiteralReplacementArgument(replacementNode);
			return getReplaceReferenceFromNonLiteralReplacementArgument(replacementNode);
		}
		function getReplaceReferenceFromLiteralReplacementArgument(node) {
			if (typeof node.value !== "string") return null;
			const replacements = parseReplacements(context, node);
			let startRef = null;
			let endRef = null;
			const start = replacements[0];
			if (start?.type === "ReferenceElement") startRef = start;
			const end = replacements[replacements.length - 1];
			if (end?.type === "ReferenceElement") endRef = end;
			if (!startRef && !endRef) return null;
			return {
				startRef,
				endRef,
				allRefs: replacements.filter((e) => e.type === "ReferenceElement")
			};
		}
		function getReplaceReferenceFromNonLiteralReplacementArgument(node) {
			const evaluated = getStaticValue(context, node);
			if (!evaluated || typeof evaluated.value !== "string") return null;
			const refRegex = /\$(?<ref>[1-9]\d*|<(?<named>[^>]+)>)/gu;
			const allRefs = [];
			let startRef = null;
			let endRef = null;
			let re;
			while (re = refRegex.exec(evaluated.value)) {
				const ref = { ref: re.groups.named ? re.groups.named : Number(re.groups.ref) };
				if (re.index === 0) startRef = ref;
				if (refRegex.lastIndex === evaluated.value.length) endRef = ref;
				allRefs.push(ref);
			}
			if (!startRef && !endRef) return null;
			return {
				startRef,
				endRef,
				allRefs
			};
		}
		function createVerifyVisitor(regexpContext, parsedElements, replaceReferenceList) {
			const startRefState = {
				capturingGroups: [],
				capturingNum: -1
			};
			const endRefState = {
				capturingGroups: [],
				capturingNum: -1
			};
			let refNum = 0;
			return {
				onCapturingGroupEnter(cgNode) {
					refNum++;
					processForState(replaceReferenceList.startRefName, replaceReferenceList.otherThanStartRefNames, startRefState);
					processForState(replaceReferenceList.endRefName, replaceReferenceList.otherThanEndRefNames, endRefState);
					function processForState(refName, otherThanRefNames, state) {
						if (refName === refNum || refName === cgNode.name) {
							state.capturingGroups.push(cgNode);
							state.capturingNum = refNum;
							state.isUseOther ||= Boolean(otherThanRefNames.has(refNum) || cgNode.name && otherThanRefNames.has(cgNode.name));
						}
					}
				},
				onPatternLeave() {
					let reportStart = null;
					if (!startRefState.isUseOther && startRefState.capturingGroups.length === 1 && startRefState.capturingGroups[0] === parsedElements.start?.capturingGroup) reportStart = parsedElements.start;
					let reportEnd = null;
					if (!endRefState.isUseOther && endRefState.capturingGroups.length === 1 && endRefState.capturingGroups[0] === parsedElements.end?.capturingGroup) reportEnd = parsedElements.end;
					const sideEffects = getSideEffectsWhenReplacingCapturingGroup(parsedElements.elements, reportStart?.capturingGroup, reportEnd?.capturingGroup, regexpContext);
					if (sideEffects.has(SideEffect.startRef)) reportStart = null;
					if (sideEffects.has(SideEffect.endRef)) reportEnd = null;
					if (!lookbehind) reportStart = null;
					if (reportStart && reportEnd) {
						const fix = buildFixer(regexpContext, [reportStart, reportEnd], replaceReferenceList, (target) => {
							if (target.allRefs.some((ref) => ref !== target.startRef && ref !== target.endRef)) return null;
							return [target.startRef?.range, target.endRef?.range];
						});
						for (const report of [reportStart, reportEnd]) context.report({
							loc: regexpContext.getRegexpLocation(report.range),
							messageId: "preferLookarounds",
							data: {
								expr1: mention(reportStart.replacedAssertion),
								expr2: mention(reportEnd.replacedAssertion)
							},
							fix
						});
					} else if (reportStart) {
						const fix = buildFixer(regexpContext, [reportStart], replaceReferenceList, (target) => {
							if (target.allRefs.some((ref) => ref !== target.startRef)) return null;
							return [target.startRef?.range];
						});
						context.report({
							loc: regexpContext.getRegexpLocation(reportStart.range),
							messageId: "prefer",
							data: {
								kind: "lookbehind assertion",
								expr: mention(reportStart.replacedAssertion)
							},
							fix
						});
					} else if (reportEnd) {
						const fix = buildFixer(regexpContext, [reportEnd], replaceReferenceList, (target) => {
							if (target.allRefs.some((ref) => {
								if (ref === target.endRef || typeof ref.ref !== "number") return false;
								return endRefState.capturingNum <= ref.ref;
							})) return null;
							return [target.endRef?.range];
						});
						context.report({
							loc: regexpContext.getRegexpLocation(reportEnd.range),
							messageId: "prefer",
							data: {
								kind: "lookahead assertion",
								expr: mention(reportEnd.replacedAssertion)
							},
							fix
						});
					}
				}
			};
		}
		function buildFixer(regexpContext, replaceCapturingGroups, replaceReferenceList, getRemoveRanges) {
			const removeRanges = [];
			for (const replaceReference of replaceReferenceList) {
				const targetRemoveRanges = getRemoveRanges(replaceReference);
				if (!targetRemoveRanges) return null;
				for (const range of targetRemoveRanges) {
					if (!range) return null;
					removeRanges.push(range);
				}
			}
			const replaces = [];
			for (const { range, replacedAssertion } of replaceCapturingGroups) {
				const replaceRange = regexpContext.patternSource.getReplaceRange(range);
				if (!replaceRange) return null;
				replaces.push({
					replaceRange,
					replacedAssertion
				});
			}
			return (fixer) => {
				const list = [];
				for (const removeRange of removeRanges) list.push({
					offset: removeRange[0],
					fix: () => fixer.removeRange(removeRange)
				});
				for (const { replaceRange, replacedAssertion } of replaces) list.push({
					offset: replaceRange.range[0],
					fix: () => replaceRange.replace(fixer, replacedAssertion)
				});
				return list.sort((a, b) => a.offset - b.offset).map((item) => item.fix());
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-named-backreference.ts
var prefer_named_backreference_default = createRule("prefer-named-backreference", {
	meta: {
		docs: {
			description: "enforce using named backreferences",
			category: "Stylistic Issues",
			recommended: false
		},
		fixable: "code",
		schema: [],
		messages: { unexpected: "Unexpected unnamed backreference." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, fixReplaceNode, getRegexpLocation }) {
			return { onBackreferenceEnter(bNode) {
				if (!bNode.ambiguous && bNode.resolved.name && !bNode.raw.startsWith("\\k<")) context.report({
					node,
					loc: getRegexpLocation(bNode),
					messageId: "unexpected",
					fix: fixReplaceNode(bNode, `\\k<${bNode.resolved.name}>`)
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-named-capture-group.ts
var prefer_named_capture_group_default = createRule("prefer-named-capture-group", {
	meta: {
		docs: {
			description: "enforce using named capture groups",
			category: "Stylistic Issues",
			recommended: false
		},
		schema: [],
		messages: { required: "Capture group {{group}} should be converted to a named or non-capturing group." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, getRegexpLocation } = regexpContext;
			return { onCapturingGroupEnter(cgNode) {
				if (cgNode.name === null) context.report({
					node,
					loc: getRegexpLocation(cgNode),
					messageId: "required",
					data: { group: mention(cgNode) }
				});
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-named-replacement.ts
var prefer_named_replacement_default = createRule("prefer-named-replacement", {
	meta: {
		docs: {
			description: "enforce using named replacement",
			category: "Stylistic Issues",
			recommended: false
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { strictTypes: { type: "boolean" } },
			additionalProperties: false
		}],
		messages: { unexpected: "Unexpected indexed reference in replacement string." },
		type: "suggestion"
	},
	create(context) {
		const strictTypes = context.options[0]?.strictTypes ?? true;
		const sourceCode = context.sourceCode;
		function createVisitor(regexpContext) {
			const { node, getAllCapturingGroups, getCapturingGroupReferences } = regexpContext;
			const capturingGroups = getAllCapturingGroups();
			if (!capturingGroups.length) return {};
			for (const ref of getCapturingGroupReferences({ strictTypes })) if (ref.type === "ReplacementRef" && ref.kind === "index" && ref.range) {
				const cgNode = capturingGroups[ref.ref - 1];
				if (cgNode && cgNode.name) context.report({
					node,
					loc: {
						start: sourceCode.getLocFromIndex(ref.range[0]),
						end: sourceCode.getLocFromIndex(ref.range[1])
					},
					messageId: "unexpected",
					fix(fixer) {
						return fixer.replaceTextRange(ref.range, `$<${cgNode.name}>`);
					}
				});
			}
			return {};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-plus-quantifier.ts
var prefer_plus_quantifier_default = createRule("prefer-plus-quantifier", {
	meta: {
		docs: {
			description: "enforce using `+` quantifier",
			category: "Stylistic Issues",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { unexpected: "Unexpected quantifier '{{expr}}'. Use '+' instead." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, getRegexpLocation, fixReplaceQuant }) {
			return { onQuantifierEnter(qNode) {
				if (qNode.min === 1 && qNode.max === Infinity) {
					const [startOffset, endOffset] = getQuantifierOffsets(qNode);
					const text = qNode.raw.slice(startOffset, endOffset);
					if (text !== "+") context.report({
						node,
						loc: getRegexpLocation(qNode, [startOffset, endOffset]),
						messageId: "unexpected",
						data: { expr: text },
						fix: fixReplaceQuant(qNode, "+")
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-predefined-assertion.ts
/**
* If the lookaround only consists of a single character, character set, or
* character class, then this single character will be returned.
*/
function getCharacters(lookaround) {
	if (lookaround.alternatives.length === 1) {
		const alt = lookaround.alternatives[0];
		if (alt.elements.length === 1) {
			const first = alt.elements[0];
			if (first.type === "CharacterSet" || first.type === "CharacterClass" || first.type === "ExpressionCharacterClass") return first;
		}
	}
	return null;
}
var prefer_predefined_assertion_default = createRule("prefer-predefined-assertion", {
	meta: {
		docs: {
			description: "prefer predefined assertion over equivalent lookarounds",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { replace: "This lookaround assertion can be replaced with {{kind}} ('{{expr}}')." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation, fixReplaceNode } = regexpContext;
			const word = Chars.word(flags);
			const nonWord = Chars.word(flags).negate();
			/**
			* Tries to replace the given assertion with a word boundary
			* assertion
			*/
			function replaceWordAssertion(aNode, wordNegated) {
				const direction = getMatchingDirectionFromAssertionKind(aNode.kind);
				/**
				* Whether the lookaround is equivalent to (?!\w) / (?<!\w) or (?=\w) / (?<=\w)
				*/
				let lookaroundNegated = aNode.negate;
				if (wordNegated) if (!getFirstCharAfter(aNode, direction, flags).edge) lookaroundNegated = !lookaroundNegated;
				else return;
				const before = getFirstCharAfter(aNode, invertMatchingDirection(direction), flags);
				if (before.edge) return;
				let otherNegated;
				if (before.char.isSubsetOf(word)) otherNegated = false;
				else if (before.char.isSubsetOf(nonWord)) otherNegated = true;
				else return;
				let kind;
				let replacement;
				if (lookaroundNegated === otherNegated) {
					kind = "a negated word boundary assertion";
					replacement = "\\B";
				} else {
					kind = "a word boundary assertion";
					replacement = "\\b";
				}
				if (kind && replacement) context.report({
					node,
					loc: getRegexpLocation(aNode),
					messageId: "replace",
					data: {
						kind,
						expr: replacement
					},
					fix: fixReplaceNode(aNode, replacement)
				});
			}
			/**
			* Tries to replace the given assertion with a edge assertion
			*/
			function replaceEdgeAssertion(aNode, lineAssertion) {
				if (!aNode.negate) return;
				if (flags.multiline === lineAssertion) {
					const replacement = aNode.kind === "lookahead" ? "$" : "^";
					context.report({
						node,
						loc: getRegexpLocation(aNode),
						messageId: "replace",
						data: {
							kind: "an edge assertion",
							expr: replacement
						},
						fix: fixReplaceNode(aNode, replacement)
					});
				}
			}
			return { onAssertionEnter(aNode) {
				if (aNode.kind !== "lookahead" && aNode.kind !== "lookbehind") return;
				const chars = getCharacters(aNode);
				if (chars === null) return;
				if (chars.type === "CharacterSet") {
					if (chars.kind === "word") {
						replaceWordAssertion(aNode, chars.negate);
						return;
					}
					if (chars.kind === "any") {
						replaceEdgeAssertion(aNode, !flags.dotAll);
						return;
					}
				}
				const set = toUnicodeSet(chars, flags);
				if (!set.accept.isEmpty) return;
				const charSet = set.chars;
				if (charSet.isAll) replaceEdgeAssertion(aNode, false);
				else if (charSet.equals(word)) replaceWordAssertion(aNode, false);
				else if (charSet.equals(nonWord)) replaceWordAssertion(aNode, true);
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-quantifier.ts
var CharBuffer = class {
	target;
	elements;
	times;
	equalChar;
	allows;
	constructor(target, allows) {
		this.target = target;
		this.elements = [target];
		this.allows = allows;
		this.times = 1;
		if (target.type === "CharacterSet") if (target.kind === "any") this.equalChar = (e) => e.type === "CharacterSet" && e.kind === "any";
		else if (target.kind === "property") this.equalChar = (e) => e.type === "CharacterSet" && e.kind === "property" && e.key === target.key && e.value === target.value && e.negate === target.negate;
		else this.equalChar = (e) => e.type === "CharacterSet" && e.kind === target.kind && e.negate === target.negate;
		else this.equalChar = (e) => e.type === "Character" && e.value === target.value;
	}
	addElement(element) {
		this.elements.push(element);
		this.times += 1;
	}
	get bufferRawContents() {
		return this.elements.reduce((acc, element) => acc + element.raw, "");
	}
	isValid() {
		if (this.elements.length < 2) return true;
		if (this.allows.includes(this.bufferRawContents)) return true;
		let charKind = null;
		for (const element of this.elements) if (element.type === "Character") {
			if (charKind == null) if (isDigit(element.value)) charKind = "digit";
			else if (isLetter(element.value)) charKind = "letter";
			else if (isSymbol(element.value)) charKind = "symbol";
			else return false;
		} else return false;
		if (charKind === "digit" || charKind === "letter" && this.elements.length <= 2 || charKind === "symbol" && this.elements.length <= 3) return true;
		return false;
	}
	getQuantifier() {
		return quantToString({
			min: this.times,
			max: this.times
		});
	}
};
var prefer_quantifier_default = createRule("prefer-quantifier", {
	meta: {
		docs: {
			description: "enforce using quantifier",
			category: "Best Practices",
			recommended: false
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { allows: {
				type: "array",
				items: { type: "string" }
			} },
			additionalProperties: false
		}],
		messages: { unexpected: "Unexpected consecutive same {{type}}. Use '{{quantifier}}' instead." },
		type: "suggestion"
	},
	create(context) {
		const allows = context.options[0]?.allows ?? [];
		function createVisitor({ node, patternSource }) {
			return { onAlternativeEnter(aNode) {
				let charBuffer = null;
				for (const element of aNode.elements) if (element.type === "CharacterSet" || element.type === "Character") if (charBuffer && charBuffer.equalChar(element)) charBuffer.addElement(element);
				else {
					validateBuffer(charBuffer);
					charBuffer = new CharBuffer(element, allows);
				}
				else {
					validateBuffer(charBuffer);
					charBuffer = null;
				}
				validateBuffer(charBuffer);
				function validateBuffer(buffer) {
					if (!buffer || buffer.isValid()) return;
					const bufferRange = {
						start: buffer.elements[0].start,
						end: buffer.elements[buffer.elements.length - 1].end
					};
					context.report({
						node,
						loc: patternSource.getAstLocation(bufferRange),
						messageId: "unexpected",
						data: {
							type: buffer.target.type === "Character" ? "characters" : buffer.target.kind === "any" ? "any characters" : "character class escapes",
							quantifier: buffer.getQuantifier()
						},
						fix(fixer) {
							const range = patternSource.getReplaceRange(bufferRange);
							if (!range) return null;
							return range.replace(fixer, buffer.target.raw + buffer.getQuantifier());
						}
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-question-quantifier.ts
var prefer_question_quantifier_default = createRule("prefer-question-quantifier", {
	meta: {
		docs: {
			description: "enforce using `?` quantifier",
			category: "Stylistic Issues",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: {
			unexpected: "Unexpected quantifier '{{expr}}'. Use '?' instead.",
			unexpectedGroup: "Unexpected group {{expr}}. Use '{{instead}}' instead."
		},
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, getRegexpLocation, fixReplaceQuant, fixReplaceNode }) {
			return {
				onQuantifierEnter(qNode) {
					if (qNode.min === 0 && qNode.max === 1) {
						const [startOffset, endOffset] = getQuantifierOffsets(qNode);
						const text = qNode.raw.slice(startOffset, endOffset);
						if (text !== "?") context.report({
							node,
							loc: getRegexpLocation(qNode, [startOffset, endOffset]),
							messageId: "unexpected",
							data: { expr: text },
							fix: fixReplaceQuant(qNode, "?")
						});
					}
				},
				onGroupEnter(gNode) {
					if (!gNode.alternatives[gNode.alternatives.length - 1].elements.length) {
						const alternatives = gNode.alternatives.slice(0, -1);
						while (alternatives.length > 0) {
							if (!alternatives[alternatives.length - 1].elements.length) {
								alternatives.pop();
								continue;
							}
							break;
						}
						if (!alternatives.length) return;
						let reportNode = gNode;
						const instead = `(?:${alternatives.map((ne) => ne.raw).join("|")})?`;
						if (gNode.parent.type === "Quantifier") if (gNode.parent.greedy && gNode.parent.min === 0 && gNode.parent.max === 1) reportNode = gNode.parent;
						else return;
						context.report({
							node,
							loc: getRegexpLocation(reportNode),
							messageId: "unexpectedGroup",
							data: {
								expr: mention(reportNode),
								instead
							},
							fix: fixReplaceNode(reportNode, instead)
						});
					}
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-range.ts
var prefer_range_default = createRule("prefer-range", {
	meta: {
		docs: {
			description: "enforce using character class range",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { target: getAllowedCharValueSchema() },
			additionalProperties: false
		}],
		messages: { unexpected: "Unexpected multiple adjacent characters. Use {{range}} instead." },
		type: "suggestion"
	},
	create(context) {
		const allowedRanges = getAllowedCharRanges(context.options[0]?.target, context);
		const sourceCode = context.sourceCode;
		function createVisitor(regexpContext) {
			const { node, patternSource } = regexpContext;
			/** Get report location ranges */
			function getReportRanges(nodes) {
				const ranges = [];
				for (const reportNode of nodes) {
					const reportRange = patternSource.getReplaceRange(reportNode);
					if (!reportRange) return null;
					const range = ranges.find((r) => r.range[0] <= reportRange.range[1] && reportRange.range[0] <= r.range[1]);
					if (range) {
						range.range[0] = Math.min(range.range[0], reportRange.range[0]);
						range.range[1] = Math.max(range.range[1], reportRange.range[1]);
					} else ranges.push(reportRange);
				}
				return ranges;
			}
			return { onCharacterClassEnter(ccNode) {
				const groups = [];
				for (const element of ccNode.elements) {
					let data;
					if (element.type === "Character") if (inRange(allowedRanges, element.value)) data = {
						min: element,
						max: element
					};
					else continue;
					else if (element.type === "CharacterClassRange") if (inRange(allowedRanges, element.min.value, element.max.value)) data = {
						min: element.min,
						max: element.max
					};
					else continue;
					else continue;
					const group = groups.find((gp) => {
						if (!(gp.min.value - 1 <= data.max.value && data.min.value <= gp.max.value + 1)) return false;
						return inRange(allowedRanges, Math.min(gp.min.value, data.min.value), Math.max(gp.max.value, data.max.value));
					});
					if (group) {
						if (data.min.value < group.min.value) group.min = data.min;
						if (group.max.value < data.max.value) group.max = data.max;
						group.nodes.push(element);
					} else groups.push({
						...data,
						nodes: [element]
					});
				}
				for (const group of groups) if (group.max.value - group.min.value + 1 >= 4 && group.nodes.length > 1) {
					const newText = `${group.min.raw}-${group.max.raw}`;
					const ranges = getReportRanges(group.nodes);
					if (!ranges) {
						context.report({
							node,
							loc: node.loc,
							messageId: "unexpected",
							data: { range: mention(newText) }
						});
						continue;
					}
					for (const range of ranges) context.report({
						node,
						loc: range.getAstLocation(sourceCode),
						messageId: "unexpected",
						data: { range: mention(newText) },
						fix: (fixer) => {
							return ranges.map((r, index) => {
								if (index === 0) return r.replace(fixer, newText);
								return r.remove(fixer);
							});
						}
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-regexp-exec.ts
var prefer_regexp_exec_default = createRule("prefer-regexp-exec", {
	meta: {
		docs: {
			description: "enforce that `RegExp#exec` is used instead of `String#match` if no global flag is provided",
			category: "Best Practices",
			recommended: false
		},
		schema: [],
		messages: { disallow: "Use the `RegExp#exec()` method instead." },
		type: "suggestion"
	},
	create(context) {
		const typeTracer = createTypeTracker(context);
		return { CallExpression(node) {
			if (!isKnownMethodCall(node, { match: 1 })) return;
			const arg = node.arguments[0];
			const evaluated = getStaticValue(context, arg);
			if (evaluated && evaluated.value instanceof RegExp && evaluated.value.flags.includes("g")) return;
			if (!typeTracer.isString(node.callee.object)) return;
			context.report({
				node,
				messageId: "disallow"
			});
		} };
	}
});
//#endregion
//#region lib/rules/prefer-regexp-test.ts
var prefer_regexp_test_default = createRule("prefer-regexp-test", {
	meta: {
		docs: {
			description: "enforce that `RegExp#test` is used instead of `String#match` and `RegExp#exec`",
			category: "Best Practices",
			recommended: false
		},
		fixable: "code",
		schema: [],
		messages: { disallow: "Use the `RegExp#test()` method instead of `{{target}}`, if you need a boolean." },
		type: "suggestion"
	},
	create(context) {
		const sourceCode = context.sourceCode;
		const typeTracer = createTypeTracker(context);
		return { CallExpression(node) {
			if (!isKnownMethodCall(node, {
				match: 1,
				exec: 1
			})) return;
			if (!isUseBoolean(node)) return;
			if (node.callee.property.name === "match") {
				if (!typeTracer.isString(node.callee.object)) return;
				const arg = node.arguments[0];
				const evaluated = getStaticValue(context, arg);
				let argIsRegExp = true;
				if (evaluated && evaluated.value instanceof RegExp) {
					if (evaluated.value.flags.includes("g")) return;
				} else if (!typeTracer.isRegExp(arg)) argIsRegExp = false;
				const memberExpr = node.callee;
				context.report({
					node,
					messageId: "disallow",
					data: { target: "String#match" },
					fix(fixer) {
						if (!argIsRegExp) return null;
						if (node.arguments.length !== 1 || hasSideEffect(memberExpr, sourceCode) || hasSideEffect(node.arguments[0], sourceCode)) return null;
						const openParen = sourceCode.getTokenAfter(node.callee, isOpeningParenToken);
						const closeParen = sourceCode.getLastToken(node);
						const stringRange = memberExpr.object.range;
						const regexpRange = [openParen.range[1], closeParen.range[0]];
						const stringText = sourceCode.text.slice(...stringRange);
						const regexpText = sourceCode.text.slice(...regexpRange);
						const convertedComparison = node.parent.type === "BinaryExpression" && isComparisonToNull(node.parent) ? convertComparison(node.parent, sourceCode)(fixer) : [];
						return [
							fixer.replaceTextRange(stringRange, regexpText),
							fixer.replaceText(memberExpr.property, "test"),
							fixer.replaceTextRange(regexpRange, stringText),
							...convertedComparison
						];
					}
				});
			}
			if (node.callee.property.name === "exec") {
				if (!typeTracer.isRegExp(node.callee.object)) return;
				const execNode = node.callee.property;
				context.report({
					node: execNode,
					messageId: "disallow",
					data: { target: "RegExp#exec" },
					*fix(fixer) {
						yield fixer.replaceText(execNode, "test");
						if (node.parent.type === "BinaryExpression" && isComparisonToNull(node.parent)) yield* convertComparison(node.parent, sourceCode)(fixer);
					}
				});
			}
		} };
	}
});
/** Checks if the given node is use boolean. */
function isUseBoolean(node) {
	const parent = getParent(node);
	if (!parent) return false;
	if (parent.type === "UnaryExpression") return parent.operator === "!";
	if (parent.type === "CallExpression") return parent.callee.type === "Identifier" && parent.callee.name === "Boolean" && parent.arguments[0] === node;
	if (parent.type === "IfStatement" || parent.type === "ConditionalExpression" || parent.type === "WhileStatement" || parent.type === "DoWhileStatement" || parent.type === "ForStatement") return parent.test === node;
	if (parent.type === "BinaryExpression") return isComparisonToNull(parent);
	if (parent.type === "LogicalExpression") {
		if (parent.operator === "&&" || parent.operator === "||") return isUseBoolean(parent);
	}
	return false;
}
function isComparisonToNull(binary) {
	return (binary.operator === "===" || binary.operator === "!==") && binary.right.type === "Literal" && binary.right.value === null;
}
function convertComparison(comparison, sourceCode) {
	return function removeComparisonFixer(fixer) {
		const operator = sourceCode.getTokenBefore(comparison.right, ({ value }) => value === comparison.operator);
		const beforeOperator = sourceCode.getTokenBefore(operator, { includeComments: true });
		return [fixer.removeRange([beforeOperator.range[1], comparison.range[1]]), ...comparison.operator === "===" ? [fixer.insertTextBefore(comparison.left, "!")] : []];
	};
}
//#endregion
//#region lib/rules/prefer-result-array-groups.ts
var prefer_result_array_groups_default = createRule("prefer-result-array-groups", {
	meta: {
		docs: {
			description: "enforce using result array `groups`",
			category: "Stylistic Issues",
			recommended: false
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { strictTypes: { type: "boolean" } },
			additionalProperties: false
		}],
		messages: { unexpected: "Unexpected indexed access for the named capturing group '{{ name }}' from regexp result array." },
		type: "suggestion"
	},
	create(context) {
		const strictTypes = context.options[0]?.strictTypes ?? true;
		const sourceCode = context.sourceCode;
		function createVisitor(regexpContext) {
			const { getAllCapturingGroups, getCapturingGroupReferences } = regexpContext;
			const capturingGroups = getAllCapturingGroups();
			if (!capturingGroups.length) return {};
			for (const ref of getCapturingGroupReferences({ strictTypes })) if (ref.type === "ArrayRef" && ref.kind === "index" && ref.ref != null) {
				const cgNode = capturingGroups[ref.ref - 1];
				if (cgNode && cgNode.name) {
					const memberNode = ref.prop.type === "member" ? ref.prop.node : null;
					context.report({
						node: ref.prop.node,
						messageId: "unexpected",
						data: { name: cgNode.name },
						fix: memberNode && memberNode.computed ? (fixer) => {
							const tokens = sourceCode.getTokensBetween(memberNode.object, memberNode.property);
							let openingBracket = tokens.pop();
							while (openingBracket && !isOpeningBracketToken(openingBracket)) openingBracket = tokens.pop();
							if (!openingBracket) return null;
							const kind = getRegExpArrayTypeKind(memberNode.object);
							if (kind === "unknown") return null;
							const needNonNull = kind === "RegExpXArray";
							return fixer.replaceTextRange([openingBracket.range[0], memberNode.range[1]], `${memberNode.optional ? "" : "."}groups${needNonNull ? "!" : ""}.${cgNode.name}`);
						} : null
					});
				}
			}
			return {};
		}
		return defineRegexpVisitor(context, { createVisitor });
		/** Gets the type kind of the given node. */
		function getRegExpArrayTypeKind(node) {
			const { tsNodeMap, checker, usedTS, hasFullTypeInformation } = getTypeScriptTools(context);
			if (!usedTS) return null;
			if (!hasFullTypeInformation) return "unknown";
			const tsNode = tsNodeMap.get(node);
			const tsType = tsNode && checker?.getTypeAtLocation(tsNode) || null;
			if (!tsType) return "unknown";
			if (isAny(tsType)) return "any";
			if (isRegExpMatchArrayOrRegExpExecArray(tsType)) return "RegExpXArray";
			if (isUnionOrIntersection(tsType)) {
				if (tsType.types.every((t) => isRegExpMatchArrayOrRegExpExecArray(t) || isNull(t))) return "RegExpXArray";
			}
			return "unknown";
		}
		/** Checks whether given type is RegExpMatchArray or RegExpExecArray or not */
		function isRegExpMatchArrayOrRegExpExecArray(tsType) {
			if (isClassOrInterface(tsType)) {
				const name = tsType.symbol.escapedName;
				return name === "RegExpMatchArray" || name === "RegExpExecArray";
			}
			return false;
		}
	}
});
//#endregion
//#region lib/rules/prefer-set-operation.ts
function isCharElement(node) {
	return node.type === "Character" || node.type === "CharacterSet" || node.type === "CharacterClass" || node.type === "ExpressionCharacterClass";
}
function isCharLookaround(node) {
	return node.type === "Assertion" && (node.kind === "lookahead" || node.kind === "lookbehind") && node.alternatives.length === 1 && node.alternatives[0].elements.length === 1 && isCharElement(node.alternatives[0].elements[0]);
}
function escapeRaw$1(raw) {
	if (/^[&\-^]$/u.test(raw)) return `\\${raw}`;
	return raw;
}
var prefer_set_operation_default = createRule("prefer-set-operation", {
	meta: {
		docs: {
			description: "prefer character class set operations instead of lookarounds",
			category: "Best Practices",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { unexpected: "This lookaround can be combined with '{{char}}' using a set operation." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation, fixReplaceNode } = regexpContext;
			if (!flags.unicodeSets) return {};
			function tryApply(element, assertion, parent) {
				const assertElement = assertion.alternatives[0].elements[0];
				if (hasStrings(assertElement, flags)) return;
				context.report({
					node,
					loc: getRegexpLocation(assertion),
					messageId: "unexpected",
					data: { char: element.raw },
					fix: fixReplaceNode(parent, () => {
						const op = assertion.negate ? "--" : "&&";
						const replacement = `[${escapeRaw$1(element.raw)}${op}${escapeRaw$1(assertElement.raw)}]`;
						return parent.elements.map((e) => {
							if (e === assertion) return "";
							else if (e === element) return replacement;
							return e.raw;
						}).join("");
					})
				});
			}
			return { onAlternativeEnter(alternative) {
				const { elements } = alternative;
				for (let i = 1; i < elements.length; i++) {
					const a = elements[i - 1];
					const b = elements[i];
					if (isCharElement(a) && isCharLookaround(b) && b.kind === "lookbehind") tryApply(a, b, alternative);
					if (isCharLookaround(a) && a.kind === "lookahead" && isCharElement(b)) tryApply(b, a, alternative);
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-star-quantifier.ts
var prefer_star_quantifier_default = createRule("prefer-star-quantifier", {
	meta: {
		docs: {
			description: "enforce using `*` quantifier",
			category: "Stylistic Issues",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { unexpected: "Unexpected quantifier '{{expr}}'. Use '*' instead." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, getRegexpLocation, fixReplaceQuant }) {
			return { onQuantifierEnter(qNode) {
				if (qNode.min === 0 && qNode.max === Infinity) {
					const [startOffset, endOffset] = getQuantifierOffsets(qNode);
					const text = qNode.raw.slice(startOffset, endOffset);
					if (text !== "*") context.report({
						node,
						loc: getRegexpLocation(qNode, [startOffset, endOffset]),
						messageId: "unexpected",
						data: { expr: text },
						fix: fixReplaceQuant(qNode, "*")
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-unicode-codepoint-escapes.ts
var prefer_unicode_codepoint_escapes_default = createRule("prefer-unicode-codepoint-escapes", {
	meta: {
		docs: {
			description: "enforce use of unicode codepoint escapes",
			category: "Stylistic Issues",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { disallowSurrogatePair: "Use Unicode codepoint escapes instead of Unicode escapes using surrogate pairs." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation, fixReplaceNode } = regexpContext;
			if (!flags.unicode && !flags.unicodeSets) return {};
			return { onCharacterEnter(cNode) {
				if (cNode.value >= 65536) {
					if (/^(?:\\u[\dA-Fa-f]{4}){2}$/u.test(cNode.raw)) context.report({
						node,
						loc: getRegexpLocation(cNode),
						messageId: "disallowSurrogatePair",
						fix: fixReplaceNode(cNode, () => {
							let text = String.fromCodePoint(cNode.value).codePointAt(0).toString(16);
							if (/[A-F]/u.test(cNode.raw)) text = text.toUpperCase();
							return `\\u{${text}}`;
						})
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/prefer-w.ts
function isSmallLetterRange(node) {
	return node.type === "CharacterClassRange" && node.min.value === CP_SMALL_A && node.max.value === CP_SMALL_Z;
}
function isCapitalLetterRange(node) {
	return node.type === "CharacterClassRange" && node.min.value === CP_CAPITAL_A && node.max.value === CP_CAPITAL_Z;
}
function isDigitRangeOrSet(node) {
	return node.type === "CharacterClassRange" && node.min.value === CP_DIGIT_ZERO && node.max.value === CP_DIGIT_NINE || node.type === "CharacterSet" && node.kind === "digit" && !node.negate;
}
function isUnderscoreCharacter(node) {
	return node.type === "Character" && node.value === CP_LOW_LINE;
}
var prefer_w_default = createRule("prefer-w", {
	meta: {
		docs: {
			description: "enforce using `\\w`",
			category: "Stylistic Issues",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { unexpected: "Unexpected {{type}} {{expr}}. Use '{{instead}}' instead." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor({ node, flags, getRegexpLocation, fixReplaceNode, patternSource }) {
			return { onCharacterClassEnter(ccNode) {
				const charSet = toUnicodeSet(ccNode, flags);
				let predefined = void 0;
				const word = Chars.word(flags);
				if (charSet.equals(word)) predefined = "\\w";
				else if (charSet.equals(word.negate())) predefined = "\\W";
				if (predefined) {
					context.report({
						node,
						loc: getRegexpLocation(ccNode),
						messageId: "unexpected",
						data: {
							type: "character class",
							expr: mention(ccNode),
							instead: predefined
						},
						fix: fixReplaceNode(ccNode, predefined)
					});
					return;
				}
				const lowerAToZ = [];
				const capitalAToZ = [];
				const digit = [];
				const underscore = [];
				for (const element of ccNode.elements) if (isSmallLetterRange(element)) {
					lowerAToZ.push(element);
					if (flags.ignoreCase) capitalAToZ.push(element);
				} else if (isCapitalLetterRange(element)) {
					capitalAToZ.push(element);
					if (flags.ignoreCase) lowerAToZ.push(element);
				} else if (isDigitRangeOrSet(element)) digit.push(element);
				else if (isUnderscoreCharacter(element)) underscore.push(element);
				if (lowerAToZ.length && capitalAToZ.length && digit.length && underscore.length) {
					const unexpectedElements = [...new Set([
						...lowerAToZ,
						...capitalAToZ,
						...digit,
						...underscore
					])].sort((a, b) => a.start - b.start);
					context.report({
						node,
						loc: getRegexpLocation(ccNode),
						messageId: "unexpected",
						data: {
							type: "character class ranges",
							expr: `'[${unexpectedElements.map((e) => e.raw).join("")}]'`,
							instead: "\\w"
						},
						fix(fixer) {
							const fixes = [];
							for (const element of unexpectedElements) {
								const range = patternSource.getReplaceRange(element);
								if (!range) return null;
								if (fixes.length === 0) fixes.push(range.replace(fixer, "\\w"));
								else fixes.push(range.remove(fixer));
							}
							return fixes;
						}
					});
				}
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/require-unicode-regexp.ts
const UTF16_MAX = 65535;
/**
* Returns whether the given pattern is compatible with unicode-mode on a
* syntactical level. So means that:
*
* 1. The raw regex is syntactically valid with the u flag.
* 2. The regex is parsed the same way (*).
*
* (*) Unicode mode parses surrogates as one character while non-Unicode mode
* parses the pair as two separate code points. We will ignore this difference.
* We will also ignore the sematic differences between escape sequences and
* so on.
*
* @returns `false` or the parsed Unicode pattern
*/
function isSyntacticallyCompatible(pattern) {
	const INCOMPATIBLE = {};
	let uPattern;
	try {
		uPattern = new RegExpParser().parsePattern(pattern.raw, void 0, void 0, { unicode: true });
	} catch {
		return false;
	}
	try {
		visitRegExpAST(pattern, { onCharacterEnter(node) {
			if (/^\\(?![bfnrtv])[A-Za-z]$/u.test(node.raw)) throw INCOMPATIBLE;
		} });
		visitRegExpAST(uPattern, {
			onCharacterEnter(node) {
				if (node.value > UTF16_MAX && (node.parent.type === "CharacterClass" || node.parent.type === "CharacterClassRange")) throw INCOMPATIBLE;
			},
			onQuantifierEnter(node) {
				if (node.element.type === "Character" && node.element.value > UTF16_MAX) throw INCOMPATIBLE;
			}
		});
	} catch (error) {
		if (error === INCOMPATIBLE) return false;
		throw error;
	}
	return uPattern;
}
const HIGH_SURROGATES = {
	min: 55296,
	max: 56319
};
const LOW_SURROGATES = {
	min: 56320,
	max: 57343
};
const SURROGATES = {
	min: 55296,
	max: 57343
};
const ASTRAL = {
	min: 65536,
	max: 1114111
};
/** Returns whether the two given ranges are equal. */
function rangeEqual(a, b) {
	if (a.length !== b.length) return false;
	for (let i = 0; i < a.length; i++) {
		const x = a[i];
		const y = b[i];
		if (x.min !== y.min || x.max !== y.max) return false;
	}
	return true;
}
/** Whether the given element is character-like element. */
function isChar(node) {
	return node.type === "Character" || node.type === "CharacterClass" || node.type === "CharacterSet";
}
/**
* Whether the given char-like accepts the same characters with and without
* the u flag.
*/
function isCompatibleCharLike(char, flags, uFlags) {
	const cs = toUnicodeSet(char, flags);
	if (!cs.isDisjointWith(SURROGATES)) return false;
	const uCs = toUnicodeSet(char, uFlags);
	return rangeEqual(cs.chars.ranges, uCs.chars.ranges);
}
/**
* Whether the given quantifier accepts the same characters with and without
* the u flag.
*
* This will return `undefined` if the function cannot decide.
*/
function isCompatibleQuantifier(q, flags, uFlags) {
	if (!isChar(q.element)) return;
	if (isCompatibleCharLike(q.element, flags, uFlags)) return true;
	if (q.min > 1 || q.max !== Infinity) return;
	const cs = toUnicodeSet(q.element, flags);
	if (!cs.isSupersetOf(SURROGATES)) return false;
	const uCs = toUnicodeSet(q.element, uFlags);
	if (!uCs.isSupersetOf(SURROGATES) || !uCs.isSupersetOf(ASTRAL)) return false;
	if (!rangeEqual(cs.chars.ranges, uCs.without(ASTRAL).chars.ranges)) return false;
	if (!getFirstCharAfter(q, "rtl", flags).char.isDisjointWith(HIGH_SURROGATES)) return false;
	if (!getFirstCharAfter(q, "ltr", flags).char.isDisjointWith(LOW_SURROGATES)) return false;
	return true;
}
/**
* Returns whether the regex would keep its behaviour if the u flag were to be
* added.
*/
function isSemanticallyCompatible(regexpContext, uPattern) {
	const surrogatePositions = /* @__PURE__ */ new Set();
	visitRegExpAST(uPattern, { onCharacterEnter(node) {
		if (node.value > UTF16_MAX) for (let i = node.start; i < node.end; i++) surrogatePositions.add(i);
	} });
	const pattern = regexpContext.patternAst;
	const flags = regexpContext.flags;
	const uFlags = toCache({
		...flags,
		unicode: true
	});
	const skip = /* @__PURE__ */ new Set();
	return !hasSomeDescendant(pattern, (n) => {
		if (n.type === "Character" && surrogatePositions.has(n.start)) return false;
		if (n.type === "Assertion" && n.kind === "word" && flags.ignoreCase) return true;
		if (isChar(n)) return !isCompatibleCharLike(n, flags, uFlags);
		if (n.type === "Quantifier") {
			const result = isCompatibleQuantifier(n, flags, uFlags);
			if (result !== void 0) {
				skip.add(n);
				return !result;
			}
		}
		return false;
	}, (n) => {
		return n.type !== "CharacterClass" && !skip.has(n);
	});
}
/**
* Returns whether the regex would keep its behaviour if the u flag were to be
* added.
*/
function isCompatible$1(regexpContext) {
	const uPattern = isSyntacticallyCompatible(regexpContext.patternAst);
	if (!uPattern) return false;
	return isSemanticallyCompatible(regexpContext, uPattern);
}
var require_unicode_regexp_default = createRule("require-unicode-regexp", {
	meta: {
		docs: {
			description: "enforce the use of the `u` flag",
			category: "Best Practices",
			recommended: false
		},
		schema: [],
		fixable: "code",
		messages: { require: "Use the 'u' flag." },
		type: "suggestion"
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, flags, flagsString, getFlagsLocation, fixReplaceFlags } = regexpContext;
			if (flagsString === null) return {};
			if (!flags.unicode && !flags.unicodeSets) context.report({
				node,
				loc: getFlagsLocation(),
				messageId: "require",
				fix: fixReplaceFlags(() => {
					if (!isCompatible$1(regexpContext)) return null;
					return `${flagsString}u`;
				})
			});
			return {};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/require-unicode-sets-regexp.ts
/**
* Returns whether the regex would keep its behavior if the v flag were to be
* added.
*/
function isCompatible(regexpContext) {
	const INCOMPATIBLE = {};
	const { flags, patternAst, pattern } = regexpContext;
	try {
		const flagsWithV = {
			...flags,
			unicodeSets: true,
			unicode: false
		};
		visitRegExpAST(patternAst, { onCharacterClassEnter(node) {
			const us = toUnicodeSet(node, flags);
			const vus = toUnicodeSet({
				...node,
				unicodeSets: true
			}, flagsWithV);
			if (!us.equals(vus)) throw INCOMPATIBLE;
			if (RESERVED_DOUBLE_PUNCTUATOR_PATTERN.test(node.raw)) throw INCOMPATIBLE;
		} });
	} catch (error) {
		if (error === INCOMPATIBLE) return false;
		throw error;
	}
	try {
		new RegExpParser().parsePattern(pattern, void 0, void 0, { unicodeSets: true });
	} catch {
		return false;
	}
	return true;
}
var require_unicode_sets_regexp_default = createRule("require-unicode-sets-regexp", {
	meta: {
		docs: {
			description: "enforce the use of the `v` flag",
			category: "Best Practices",
			recommended: false
		},
		schema: [],
		fixable: "code",
		messages: { require: "Use the 'v' flag." },
		type: "suggestion"
	},
	create(context) {
		/**
		* Create visitor
		*/
		function createVisitor(regexpContext) {
			const { node, flags, flagsString, getFlagsLocation, fixReplaceFlags } = regexpContext;
			if (flagsString === null) return {};
			if (!flags.unicodeSets) context.report({
				node,
				loc: getFlagsLocation(),
				messageId: "require",
				fix: fixReplaceFlags(() => {
					if (!flags.unicode || !isCompatible(regexpContext)) return null;
					return `${flagsString.replace(/u/gu, "")}v`;
				})
			});
			return {};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/simplify-set-operations.ts
/** Checks whether the given character class is negatable. */
function isNegatableCharacterClassElement(node) {
	return node.type === "CharacterClass" || node.type === "ExpressionCharacterClass" || node.type === "CharacterSet" && (node.kind !== "property" || !node.strings);
}
/** Checks whether the given character class is negate. */
function isNegate(node) {
	return isNegatableCharacterClassElement(node) && node.negate;
}
/**
* Gets the text of a character class that negates the given character class.
*/
function getRawTextToNot(negateNode) {
	const raw = negateNode.raw;
	if (negateNode.type === "CharacterClass" || negateNode.type === "ExpressionCharacterClass") return `${raw[0]}${raw.slice(2)}`;
	const escapeChar = negateNode.raw[1].toLowerCase();
	return `${raw[0]}${escapeChar}${raw.slice(2)}`;
}
/** Collect the operands from the given intersection expression */
function collectIntersectionOperands(expression) {
	const operands = [];
	let operand = expression;
	while (operand.type === "ClassIntersection") {
		operands.unshift(operand.right);
		operand = operand.left;
	}
	operands.unshift(operand);
	return operands;
}
/** Gets the parsed result element. */
function getParsedElement(pattern, flags) {
	try {
		const ast = new RegExpParser().parsePattern(pattern, void 0, void 0, {
			unicode: flags.unicode,
			unicodeSets: flags.unicodeSets
		});
		if (ast.alternatives.length === 1) {
			if (ast.alternatives[0].elements.length === 1) {
				const element = ast.alternatives[0].elements[0];
				if (element.type !== "Assertion" && element.type !== "Quantifier" && element.type !== "CapturingGroup" && element.type !== "Group" && element.type !== "Backreference") return element;
			}
		}
	} catch {}
	return null;
}
var simplify_set_operations_default = createRule("simplify-set-operations", {
	meta: {
		docs: {
			description: "require simplify set operations",
			category: "Best Practices",
			recommended: true
		},
		schema: [],
		messages: {
			toNegationOfDisjunction: "This {{target}} can be converted to the negation of a disjunction using De Morgan's laws.",
			toNegationOfConjunction: "This character class can be converted to the negation of a conjunction using De Morgan's laws.",
			toSubtraction: "This expression can be converted to the subtraction.",
			toIntersection: "This expression can be converted to the intersection."
		},
		fixable: "code",
		type: "suggestion"
	},
	create(context) {
		/**
		* Create visitor
		*/
		function createVisitor(regexpContext) {
			const { node, flags, getRegexpLocation, fixReplaceNode } = regexpContext;
			if (!flags.unicodeSets) return {};
			return {
				onCharacterClassEnter(ccNode) {
					toNegationOfConjunction(ccNode);
				},
				onExpressionCharacterClassEnter(eccNode) {
					if (toNegationOfDisjunction(eccNode)) return;
					if (toSubtraction(eccNode)) return;
					verifyExpressions(eccNode);
				}
			};
			/**
			* Reports if the fixed pattern is compatible with the original pattern.
			* Returns true if reported.
			*/
			function reportWhenFixedIsCompatible({ reportNode, targetNode, messageId, data, fix }) {
				const us = toUnicodeSet(targetNode, flags);
				const fixedText = fix();
				const convertedElement = getParsedElement(fixedText, flags);
				if (!convertedElement) return false;
				const convertedUs = toUnicodeSet(convertedElement, flags);
				if (!us.equals(convertedUs)) return false;
				context.report({
					node,
					loc: getRegexpLocation(reportNode),
					messageId,
					data: data || {},
					fix: fixReplaceNode(targetNode, fixedText)
				});
				return true;
			}
			/** Verify for intersections and subtractions */
			function verifyExpressions(eccNode) {
				let operand = eccNode.expression;
				let right = null;
				while (operand.type === "ClassIntersection" || operand.type === "ClassSubtraction") {
					toIntersection(operand, right, eccNode);
					right = operand.right;
					operand = operand.left;
				}
			}
			/**
			* Checks the given character class and reports if it can be converted to the negation of a disjunction
			* using De Morgan's laws.
			* Returns true if reported.
			*
			* e.g.
			* - `[[^a]&&[^b]]` -> `[^ab]`
			* - `[^[^a]&&[^b]]` -> `[ab]`
			* - `[[^a]&&[^b]&&c]` -> `[[^ab]&&c]`
			*/
			function toNegationOfDisjunction(eccNode) {
				const expression = eccNode.expression;
				if (expression.type !== "ClassIntersection") return false;
				const operands = collectIntersectionOperands(expression);
				const negateOperands = [];
				const others = [];
				for (const e of operands) if (isNegate(e)) negateOperands.push(e);
				else others.push(e);
				const fixedOperands = negateOperands.map((negateOperand) => getRawTextToNot(negateOperand)).join("");
				if (negateOperands.length === operands.length) return reportWhenFixedIsCompatible({
					reportNode: eccNode,
					targetNode: eccNode,
					messageId: "toNegationOfDisjunction",
					data: { target: "character class" },
					fix: () => `[${eccNode.negate ? "" : "^"}${fixedOperands}]`
				});
				if (negateOperands.length < 2) return null;
				return reportWhenFixedIsCompatible({
					reportNode: negateOperands[negateOperands.length - 1].parent,
					targetNode: eccNode,
					messageId: "toNegationOfDisjunction",
					data: { target: "expression" },
					fix: () => {
						const operandTestList = [`[^${fixedOperands}]`, ...others.map((e) => e.raw)];
						return `[${eccNode.negate ? "^" : ""}${operandTestList.join("&&")}]`;
					}
				});
			}
			/**
			* Checks the given character class and reports if it can be converted to the negation of a conjunction
			* using De Morgan's laws.
			* Returns true if reported.
			*
			* e.g.
			* - `[[^a][^b]]` -> `[^a&&b]`
			*/
			function toNegationOfConjunction(ccNode) {
				if (ccNode.elements.length <= 1) return false;
				const elements = ccNode.elements;
				const negateElements = elements.filter(isNegate);
				if (negateElements.length !== elements.length) return false;
				return reportWhenFixedIsCompatible({
					reportNode: ccNode,
					targetNode: ccNode,
					messageId: "toNegationOfConjunction",
					fix: () => {
						const fixedElements = negateElements.map((negateElement) => getRawTextToNot(negateElement));
						return `[${ccNode.negate ? "" : "^"}${fixedElements.join("&&")}]`;
					}
				});
			}
			/**
			* Checks the given expression and reports whether it can be converted to subtraction by reducing its complement.
			* Returns true if reported.
			*
			* e.g.
			* - `[a&&[^b]]` -> `[a--b]`
			* - `[[^a]&&b]` -> `[b--a]`
			* - `[a&&[^b]&&c]` -> `[[a&&c]--b]`
			*/
			function toSubtraction(eccNode) {
				const expression = eccNode.expression;
				if (expression.type !== "ClassIntersection") return false;
				const operands = collectIntersectionOperands(expression);
				const negateOperand = operands.find(isNegate);
				if (!negateOperand) return false;
				return reportWhenFixedIsCompatible({
					reportNode: expression,
					targetNode: eccNode,
					messageId: "toSubtraction",
					fix() {
						const others = operands.filter((e) => e !== negateOperand);
						let fixedLeftText = others.map((e) => e.raw).join("&&");
						if (others.length >= 2) fixedLeftText = `[${fixedLeftText}]`;
						const fixedRightText = getRawTextToNot(negateOperand);
						return `[${eccNode.negate ? "^" : ""}${`${fixedLeftText}--${fixedRightText}`}]`;
					}
				});
			}
			/**
			* Checks the given expression and reports whether it can be converted to intersection by reducing its complement.
			* Returns true if reported.
			*
			* e.g.
			* - `[a--[^b]]` -> `[a&&b]`
			*/
			function toIntersection(expression, expressionRight, eccNode) {
				if (expression.type !== "ClassSubtraction") return false;
				const { left, right } = expression;
				if (!isNegate(right)) return false;
				return reportWhenFixedIsCompatible({
					reportNode: expression,
					targetNode: eccNode,
					messageId: "toIntersection",
					fix() {
						let fixedLeftText = left.raw;
						if (left.type === "ClassSubtraction") fixedLeftText = `[${fixedLeftText}]`;
						const fixedRightText = getRawTextToNot(right);
						let fixedText = `${fixedLeftText}&&${fixedRightText}`;
						if (expressionRight) fixedText = `[${fixedText}]`;
						const targetRaw = eccNode.raw;
						return `${targetRaw.slice(0, expression.start - eccNode.start)}${fixedText}${targetRaw.slice(expression.end - eccNode.start)}`;
					}
				});
			}
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/utils/lexicographically-smallest.ts
function findMin(array, compare) {
	if (array.length === 0) return;
	let min = array[0];
	for (let i = 1; i < array.length; i++) {
		const item = array[i];
		if (compare(item, min) < 0) min = item;
	}
	return min;
}
function compareWords$2(a, b) {
	const l = Math.min(a.length, b.length);
	for (let i = 0; i < l; i++) {
		const diff = a[i] - b[i];
		if (diff !== 0) return diff;
	}
	return a.length - b.length;
}
/**
* Returns the lexicographically smallest word in the given set or `undefined` if the set is empty.
*/
function getLexicographicallySmallest(set) {
	if (set.accept.isEmpty) return set.chars.isEmpty ? void 0 : [set.chars.ranges[0].min];
	return findMin(set.accept.wordSets.map((w) => w.map((c) => c.ranges[0].min)), compareWords$2);
}
/**
* Returns the lexicographically smallest word in the given set or `undefined` if the set is empty.
*/
function getLexicographicallySmallestInConcatenation(elements) {
	if (elements.length === 1) return getLexicographicallySmallest(elements[0]);
	let smallest = [];
	for (let i = elements.length - 1; i >= 0; i--) {
		const set = elements[i];
		if (set.isEmpty) return;
		else if (set.accept.isEmpty) smallest.unshift(set.chars.ranges[0].min);
		else {
			let words = [...set.chars.isEmpty ? [] : [[set.chars]], ...set.accept.wordSets].map((w) => w.map((c) => c.ranges[0].min));
			const seenLengths = /* @__PURE__ */ new Set();
			words = words.sort(compareWords$2).filter((w) => {
				if (seenLengths.has(w.length)) return false;
				seenLengths.add(w.length);
				return true;
			});
			smallest = findMin(words.map((w) => [...w, ...smallest]), compareWords$2);
		}
	}
	return smallest;
}
//#endregion
//#region lib/rules/sort-alternatives.ts
const cache = /* @__PURE__ */ new Map();
function getAllowedChars(flags) {
	assertValidFlags(flags);
	const cacheKey = (flags.ignoreCase ? "i" : "") + (flags.unicode ? "u" : "") + (flags.unicodeSets ? "v" : "");
	let result = cache.get(cacheKey);
	if (result === void 0) {
		result = {
			allowed: JS.createCharSet([
				{
					kind: "word",
					negate: false
				},
				{
					min: CP_SPACE,
					max: CP_SPACE
				},
				{
					min: CP_PLUS,
					max: CP_PLUS
				},
				{
					min: CP_MINUS,
					max: CP_MINUS
				},
				{
					min: CP_STAR,
					max: CP_STAR
				},
				{
					min: CP_SLASH,
					max: CP_SLASH
				},
				{
					min: CP_APOSTROPHE,
					max: CP_APOSTROPHE
				},
				{
					min: CP_QUESTION,
					max: CP_QUESTION
				}
			], flags),
			required: Chars.word(flags)
		};
		cache.set(cacheKey, result);
	}
	return result;
}
/**
* Returns whether the given element contains only literal characters and
* groups/other elements containing literal characters.
*/
function containsOnlyLiterals(element) {
	return !hasSomeDescendant(element, (d) => {
		return d.type === "Backreference" || d.type === "CharacterSet" || d.type === "Quantifier" && d.max === Infinity || d.type === "CharacterClass" && d.negate || d.type === "ExpressionCharacterClass" && d.negate;
	}, (d) => d.type !== "Assertion");
}
const lssCache = /* @__PURE__ */ new WeakMap();
/**
* A cached version of {@link approximateLexicographicallySmallest}.
*/
function cachedApproximateLexicographicallySmallest(alternative, parser, flags) {
	let cached = lssCache.get(alternative);
	if (cached === void 0) {
		cached = approximateLexicographicallySmallest(alternative, parser, flags);
		lssCache.set(alternative, cached);
	}
	return cached;
}
const LONGEST_PREFIX_OPTIONS = {
	includeAfter: true,
	onlyInside: true,
	looseGroups: true
};
/**
* Return an approximation of the lexicographically smallest string (LSS)
* accepted by the given alternative.
*
* If the LSS is defined for the given alternative and shorter than 1000
* characters, then the LSS will be returned. Otherwise, a prefix-based
* approximation will be returned.
*
* Assertions will be ignored when computing the LSS.
*
* Backreferences will be disabled when computing the LSS, but the prefix-based
* approximation will account for them.
*/
function approximateLexicographicallySmallest(alternative, parser, flags) {
	const lss = getLexicographicallySmallestFromAlternative(alternative, parser, flags);
	if (lss !== void 0) return lss;
	return getLexicographicallySmallestFromCharSets(getLongestPrefix(alternative, "ltr", flags, LONGEST_PREFIX_OPTIONS));
}
/**
* If defined, this will return the lexicographically smallest string accepted
* by the given alternative (ignoring assertions).
*/
function getLexicographicallySmallestFromAlternative(alternative, parser, flags) {
	if (alternative.type === "StringAlternative" || hasOnlyCharacters(alternative, flags)) {
		const smallest = [];
		for (const e of alternative.elements) {
			const cs = toUnicodeSet(e, flags).chars;
			if (cs.isEmpty) return void 0;
			smallest.push(cs.ranges[0].min);
		}
		return smallest;
	}
	if (isOnlyCharacterElements(alternative.elements)) return getLexicographicallySmallestInConcatenation(alternative.elements.map((e) => toUnicodeSet(e, flags)));
	try {
		const result = parser.parseElement(alternative, {
			assertions: "unknown",
			backreferences: "disable",
			maxBackreferenceWords: 4,
			maxNodes: 1e3
		});
		const expression = transform({ onConcatenation(concat) {
			concat.elements = concat.elements.filter((e) => e.type !== "Unknown");
		} }, result.expression);
		const nfa = NFA.fromRegex(expression, { maxCharacter: result.maxCharacter }, {}, new NFA.LimitedNodeFactory(1e3));
		return getLexicographicallySmallestFromNfa(nfa.initial, nfa.finals);
	} catch {
		return;
	}
}
/**
* Returns whether the given array of nodes contains only characters.
* But note that if the pattern has the v flag, the character class may contain strings.
*/
function isOnlyCharacterElements(nodes) {
	return nodes.every((e) => e.type === "Character" || e.type === "CharacterClass" || e.type === "CharacterSet" || e.type === "ExpressionCharacterClass");
}
/**
* Returns whether the given alternative has contains only characters.
* The v flag in the pattern does not contains the string.
*/
function hasOnlyCharacters(alternative, flags) {
	return isOnlyCharacterElements(alternative.elements) && alternative.elements.every((e) => !hasStrings(e, flags));
}
/**
* If defined, this will return the lexicographically smallest string accepted
* by the given NFA.
*/
function getLexicographicallySmallestFromNfa(initial, finals) {
	const smallest = [];
	let currentStates = [initial];
	const newStatesSet = /* @__PURE__ */ new Set();
	const MAX_LENGTH = 1e3;
	for (let i = 0; i < MAX_LENGTH; i++) {
		if (currentStates.some((n) => finals.has(n))) return smallest;
		let min = Infinity;
		for (const state of currentStates) state.out.forEach((charSet) => {
			if (!charSet.isEmpty) min = Math.min(min, charSet.ranges[0].min);
		});
		if (min === Infinity) return;
		smallest.push(min);
		const newStates = [];
		newStatesSet.clear();
		for (const state of currentStates) state.out.forEach((charSet, to) => {
			if (charSet.has(min) && !newStatesSet.has(to)) {
				newStates.push(to);
				newStatesSet.add(to);
			}
		});
		currentStates = newStates;
	}
}
/**
* If defined, this will return the lexicographically smallest string accepted
* by the given sequence of character sets.
*
* If any of the given character sets is empty, the current smallest will be
* returned.
*/
function getLexicographicallySmallestFromCharSets(word) {
	const result = [];
	for (const set of word) {
		if (set.isEmpty) break;
		result.push(set.ranges[0].min);
	}
	return result;
}
/**
* Compare two string independent of the current locale by byte order.
*/
function compareByteOrder(a, b) {
	if (a === b) return 0;
	return a < b ? -1 : 1;
}
/**
* Compare two char sets by byte order.
*/
function compareCharSets(a, b) {
	const aRanges = a.ranges;
	const bRanges = b.ranges;
	for (let i = 0; i < aRanges.length && i < bRanges.length; i++) {
		const aR = aRanges[i];
		const bR = bRanges[i];
		if (aR.min !== bR.min) return aR.min - bR.min;
		if (aR.max !== bR.max) if (aR.max < bR.max) return i + 1 < aRanges.length ? 1 : -1;
		else return i + 1 < bRanges.length ? -1 : 1;
	}
	return aRanges.length - bRanges.length;
}
/**
* Compare two strings of char sets by byte order.
*/
function compareCharSetStrings(a, b) {
	const l = Math.min(a.length, b.length);
	for (let i = 0; i < l; i++) {
		const diff = compareCharSets(a[i], b[i]);
		if (diff !== 0) return diff;
	}
	return a.length - b.length;
}
/**
* Compare two strings of char sets by byte order.
*/
function compareWords$1(a, b) {
	const l = Math.min(a.length, b.length);
	for (let i = 0; i < l; i++) {
		const aI = a[i];
		const bI = b[i];
		if (aI !== bI) return aI - bI;
	}
	return a.length - b.length;
}
/**
* Sorts the given alternatives.
*
* The comparison function implemented by this function has 3 parts:
*
* 1) Comparison based on the lexicographically smallest strings (LSS) accepted
*    by the alternatives.
* 2) Comparison based on the longest prefix of the alternatives.
* 3) Comparison based on the raw source code of the alternatives.
*
* For more information on why we use LSS-based comparison and how it works,
* see https://github.com/ota-meshi/eslint-plugin-regexp/pull/423.
*/
function sortAlternatives(alternatives, parser, flags) {
	alternatives.sort((a, b) => {
		const lssDiff = compareWords$1(cachedApproximateLexicographicallySmallest(a, parser, flags), cachedApproximateLexicographicallySmallest(b, parser, flags));
		if (lssDiff !== 0) return lssDiff;
		const prefixDiff = compareCharSetStrings(getLongestPrefix(a, "ltr", flags, LONGEST_PREFIX_OPTIONS), getLongestPrefix(b, "ltr", flags, LONGEST_PREFIX_OPTIONS));
		if (prefixDiff !== 0) return prefixDiff;
		if (flags.ignoreCase) return compareByteOrder(a.raw.toUpperCase(), b.raw.toUpperCase()) || compareByteOrder(a.raw, b.raw);
		return compareByteOrder(a.raw, b.raw);
	});
}
/**
* Sorts the given string alternatives.
*
* Sorting is done by comparing the lexicographically smallest strings (LSS).
*
* For more information on why we use LSS-based comparison and how it works,
* see https://github.com/ota-meshi/eslint-plugin-regexp/pull/423.
*/
function sortStringAlternatives(alternatives, parser, flags) {
	alternatives.sort((a, b) => {
		return compareWords$1(getLexicographicallySmallestFromAlternative(a, parser, flags), getLexicographicallySmallestFromAlternative(b, parser, flags));
	});
}
/**
* Returns whether the given string is a valid integer.
* @param str
* @returns
*/
function isIntegerString(str) {
	return /^(?:0|[1-9]\d*)$/u.test(str);
}
/**
* This tries to sort the given alternatives by assuming that all alternatives
* are a number.
*/
function trySortNumberAlternatives(alternatives) {
	const runs = getRuns(alternatives, (a) => isIntegerString(a.raw));
	for (const { startIndex, elements } of runs) {
		elements.sort((a, b) => {
			return Number(a.raw) - Number(b.raw);
		});
		alternatives.splice(startIndex, elements.length, ...elements);
	}
}
/**
* Returns the indexes of the first and last of original array that is changed
* when compared with the reordered one.
*/
function getReorderingBounds(original, reorder) {
	if (original.length !== reorder.length) return;
	const len = original.length;
	let first = 0;
	for (; first < len && original[first] === reorder[first]; first++);
	if (first === len) return;
	let last = len - 1;
	for (; last >= 0 && original[last] === reorder[last]; last--);
	return [first, last];
}
/**
* Returns an array of runs of elements that fulfill the given condition.
*/
function getRuns(iter, condFn) {
	const runs = [];
	let elements = [];
	let index = 0;
	for (const item of iter) {
		if (condFn(item)) elements.push(item);
		else if (elements.length > 0) {
			runs.push({
				startIndex: index - elements.length,
				elements
			});
			elements = [];
		}
		index++;
	}
	if (elements.length > 0) runs.push({
		startIndex: index - elements.length,
		elements
	});
	return runs;
}
var sort_alternatives_default = createRule("sort-alternatives", {
	meta: {
		docs: {
			description: "sort alternatives if order doesn't matter",
			category: "Best Practices",
			recommended: false
		},
		fixable: "code",
		schema: [],
		messages: { sort: "The {{alternatives}} can be sorted without affecting the regex." },
		type: "suggestion"
	},
	create(context) {
		const sliceMinLength = 3;
		function createVisitor(regexpContext) {
			const { node, getRegexpLocation, fixReplaceNode, flags } = regexpContext;
			const allowedChars = getAllowedChars(flags);
			const possibleCharsCache = /* @__PURE__ */ new Map();
			const parser = getParser(regexpContext);
			/** A cached version of getConsumedChars */
			function getPossibleChars(a) {
				let chars = possibleCharsCache.get(a);
				if (chars === void 0) chars = getConsumedChars(a, flags).chars;
				return chars;
			}
			/** Tries to sort the given alternatives. */
			function trySortRun(run) {
				const alternatives = run.elements;
				if (canReorder(alternatives, flags)) {
					sortAlternatives(alternatives, parser, flags);
					trySortNumberAlternatives(alternatives);
				} else if (!Chars.empty(flags).union(...alternatives.map(getPossibleChars)).isDisjointWith(Chars.digit(flags))) {
					const runs = getRuns(alternatives, (a) => isIntegerString(a.raw));
					for (const { startIndex: index, elements } of runs) if (elements.length > 1 && canReorder(elements, flags)) {
						trySortNumberAlternatives(elements);
						alternatives.splice(index, elements.length, ...elements);
					}
				}
				enforceSorted(run, "alternatives of this group");
			}
			/**
			* Creates a report if the sorted alternatives are different from
			* the unsorted ones.
			*/
			function enforceSorted(run, alternatives) {
				const sorted = run.elements;
				const parent = sorted[0].parent;
				const unsorted = parent.alternatives.slice(run.startIndex, run.startIndex + sorted.length);
				const bounds = getReorderingBounds(unsorted, sorted);
				if (!bounds) return;
				const loc = getRegexpLocation({
					start: unsorted[bounds[0]].start,
					end: unsorted[bounds[1]].end
				});
				context.report({
					node,
					loc,
					messageId: "sort",
					data: { alternatives },
					fix: fixReplaceNode(parent, () => {
						const prefix = parent.raw.slice(0, unsorted[0].start - parent.start);
						const suffix = parent.raw.slice(unsorted[unsorted.length - 1].end - parent.start);
						return prefix + sorted.map((a) => a.raw).join("|") + suffix;
					})
				});
			}
			function onParent(parent) {
				if (parent.alternatives.length < 2) return;
				const runs = getRuns(parent.alternatives, (a) => {
					if (!containsOnlyLiterals(a)) return false;
					const consumedChars = getPossibleChars(a);
					if (consumedChars.isEmpty) return false;
					if (!consumedChars.isSubsetOf(allowedChars.allowed)) return false;
					if (consumedChars.isDisjointWith(allowedChars.required)) return false;
					return true;
				});
				if (runs.length === 1 && runs[0].elements.length === parent.alternatives.length) trySortRun(runs[0]);
				else for (const run of runs) if (run.elements.length >= sliceMinLength && run.elements.length >= 2) trySortRun(run);
			}
			/** The handler for ClassStringDisjunction */
			function onClassStringDisjunction(parent) {
				if (parent.alternatives.length < 2) return;
				const alternatives = [...parent.alternatives];
				sortStringAlternatives(alternatives, parser, flags);
				trySortNumberAlternatives(alternatives);
				enforceSorted({
					startIndex: 0,
					elements: [...alternatives]
				}, "string alternatives");
			}
			return {
				onGroupEnter: onParent,
				onPatternEnter: onParent,
				onCapturingGroupEnter: onParent,
				onClassStringDisjunctionEnter: onClassStringDisjunction
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/sort-character-class-elements.ts
const DEFAULT_ORDER = [
	"\\s",
	"\\w",
	"\\d",
	"\\p",
	"*",
	"\\q",
	"[]"
];
/**
* Get kind of CharacterClassElement for given CharacterClassElement
*/
function getCharacterClassElementKind(node) {
	if (node.type === "CharacterSet") return node.kind === "word" ? "\\w" : node.kind === "digit" ? "\\d" : node.kind === "space" ? "\\s" : "\\p";
	if (node.type === "ClassStringDisjunction") return "\\q";
	if (node.type === "CharacterClass" || node.type === "ExpressionCharacterClass") return "[]";
	return "*";
}
/**
* Return the lexicographically smallest string accepted by the given element.
* If the class set is negate, the original value is used for calculation.
*/
function getLexicographicallySmallestFromElement(node, flags) {
	return getLexicographicallySmallest(node.type === "CharacterSet" && node.negate ? toUnicodeSet({
		...node,
		negate: false
	}, flags) : toUnicodeSet(node, flags)) || [];
}
/**
* Compare two strings of char sets by byte order.
*/
function compareWords(a, b) {
	const l = Math.min(a.length, b.length);
	for (let i = 0; i < l; i++) {
		const aI = a[i];
		const bI = b[i];
		if (aI !== bI) return aI - bI;
	}
	return a.length - b.length;
}
var sort_character_class_elements_default = createRule("sort-character-class-elements", {
	meta: {
		docs: {
			description: "enforces elements order in character class",
			category: "Stylistic Issues",
			recommended: false
		},
		fixable: "code",
		schema: [{
			type: "object",
			properties: { order: {
				type: "array",
				items: { enum: [
					"\\s",
					"\\w",
					"\\d",
					"\\p",
					"*",
					"\\q",
					"[]"
				] }
			} },
			additionalProperties: false
		}],
		messages: { sortElements: "Expected character class elements to be in ascending order. {{next}} should be before {{prev}}." },
		type: "layout"
	},
	create(context) {
		const orderOption = { "*": Infinity };
		(context.options[0]?.order ?? DEFAULT_ORDER).forEach((o, i) => {
			orderOption[o] = i + 1;
		});
		function createVisitor({ node, flags, getRegexpLocation, patternSource }) {
			return { onCharacterClassEnter(ccNode) {
				const prevList = [];
				for (const next of ccNode.elements) {
					if (prevList.length) {
						const prev = prevList[0];
						if (!isValidOrder(prev, next, flags)) {
							let moveTarget = prev;
							for (const p of prevList) if (isValidOrder(p, next, flags)) break;
							else moveTarget = p;
							context.report({
								node,
								loc: getRegexpLocation(next),
								messageId: "sortElements",
								data: {
									next: mention(next),
									prev: mention(moveTarget)
								},
								*fix(fixer) {
									const nextRange = patternSource.getReplaceRange(next);
									const targetRange = patternSource.getReplaceRange(moveTarget);
									if (!targetRange || !nextRange) return;
									yield targetRange.insertBefore(fixer, escapeRaw(next, moveTarget));
									yield nextRange.remove(fixer);
								}
							});
						}
					}
					prevList.unshift(next);
				}
			} };
		}
		/**
		* Check that the two given CharacterClassElements are in a valid order.
		*/
		function isValidOrder(prev, next, flags) {
			const prevKind = getCharacterClassElementKind(prev);
			const nextKind = getCharacterClassElementKind(next);
			const prevOrder = orderOption[prevKind] ?? orderOption["*"];
			const nextOrder = orderOption[nextKind] ?? orderOption["*"];
			if (prevOrder < nextOrder) return true;
			else if (prevOrder > nextOrder) return false;
			const prevOrderShortCircuit = DEFAULT_ORDER.indexOf(prevKind);
			const nextOrderShortCircuit = DEFAULT_ORDER.indexOf(nextKind);
			if (prevOrderShortCircuit < nextOrderShortCircuit) return true;
			else if (prevOrderShortCircuit > nextOrderShortCircuit) return false;
			if (prev.type === "CharacterSet" && prev.kind === "property" && next.type === "CharacterSet" && next.kind === "property") return isValidOrderForUnicodePropertyCharacterSet(prev, next);
			if (compareWords(getLexicographicallySmallestFromElement(prev, flags), getLexicographicallySmallestFromElement(next, flags)) <= 0) return true;
			return false;
		}
		/**
		* Check that the two given UnicodePropertyCharacterSet are in a valid order.
		*/
		function isValidOrderForUnicodePropertyCharacterSet(prev, next) {
			if (prev.key < next.key) return true;
			else if (prev.key > next.key) return false;
			if (prev.value) {
				if (next.value) {
					if (prev.value <= next.value) return true;
					return false;
				}
				return false;
			}
			return true;
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
/**
* get the escape text from the given CharacterClassElement.
*/
function escapeRaw(node, target) {
	let raw = node.raw;
	if (raw[0] === "-") {
		const elements = target.parent.elements;
		const prev = elements[elements.indexOf(target) - 1];
		if (prev && (prev.type === "Character" || prev.type === "CharacterSet")) raw = `\\${raw}`;
	} else if (raw[0] === "^") {
		if (target.parent.elements[0] === target) raw = `\\${raw}`;
	}
	if (target.raw[0] === "-") {
		if (node.type === "Character" || node.type === "CharacterSet") raw = `${raw}\\`;
	}
	return raw;
}
//#endregion
//#region lib/rules/sort-flags.ts
var sort_flags_default = createRule("sort-flags", {
	meta: {
		docs: {
			description: "require regex flags to be sorted",
			category: "Stylistic Issues",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: { sortFlags: "The flags '{{flags}}' should be in the order '{{sortedFlags}}'." },
		type: "suggestion"
	},
	create(context) {
		function sortFlags(flagsStr) {
			return [...flagsStr].sort((a, b) => a.codePointAt(0) - b.codePointAt(0)).join("");
		}
		function visit({ regexpNode, flagsString, ownsFlags, getFlagsLocation, fixReplaceFlags }) {
			if (flagsString && ownsFlags) {
				const sortedFlags = sortFlags(flagsString);
				if (flagsString !== sortedFlags) context.report({
					node: regexpNode,
					loc: getFlagsLocation(),
					messageId: "sortFlags",
					data: {
						flags: flagsString,
						sortedFlags
					},
					fix: fixReplaceFlags(sortedFlags, false)
				});
			}
		}
		return defineRegexpVisitor(context, {
			createVisitor(regexpContext) {
				visit(regexpContext);
				return {};
			},
			visitInvalid: visit,
			visitUnknown: visit
		});
	}
});
//#endregion
//#region lib/rules/strict.ts
const validator = new RegExpValidator({
	strict: true,
	ecmaVersion: 2020
});
/**
* Check syntax error in a given pattern.
* @returns The syntax error.
*/
function validateRegExpPattern(pattern, flags) {
	try {
		validator.validatePattern(pattern, void 0, void 0, flags);
		return null;
	} catch (err) {
		return err instanceof Error ? err.message : null;
	}
}
const CHARACTER_CLASS_SYNTAX_CHARACTERS = new Set("\\/()[]{}^$.|-+*?".split(""));
const SYNTAX_CHARACTERS = new Set("\\/()[]{}^$.|+*?".split(""));
var strict_default = createRule("strict", {
	meta: {
		docs: {
			description: "disallow not strictly valid regular expressions",
			category: "Possible Errors",
			recommended: true
		},
		fixable: "code",
		schema: [],
		messages: {
			invalidControlEscape: "Invalid or incomplete control escape sequence. Either use a valid control escape sequence or escaping the standalone backslash.",
			incompleteEscapeSequence: "Incomplete escape sequence {{expr}}. Either use a valid escape sequence or remove the useless escaping.",
			invalidPropertyEscape: "Invalid property escape sequence {{expr}}. Either use a valid property escape sequence or remove the useless escaping.",
			incompleteBackreference: "Incomplete backreference {{expr}}. Either use a valid backreference or remove the useless escaping.",
			unescapedSourceCharacter: "Unescaped source character {{expr}}.",
			octalEscape: "Invalid legacy octal escape sequence {{expr}}. Use a hexadecimal escape instead.",
			uselessEscape: "Useless identity escapes with non-syntax characters are forbidden.",
			invalidRange: "Invalid character class range. A character set cannot be the minimum or maximum of a character class range. Either escape the `-` or fix the character class range.",
			quantifiedAssertion: "Assertion are not allowed to be quantified directly.",
			regexMessage: "{{message}}.",
			hexEscapeSuggestion: "Replace the octal escape with a hexadecimal escape."
		},
		type: "suggestion",
		hasSuggestions: true
	},
	create(context) {
		function createVisitor(regexpContext) {
			const { node, flags, pattern, getRegexpLocation, fixReplaceNode } = regexpContext;
			if (flags.unicode || flags.unicodeSets) return {};
			let reported = false;
			let hasNamedBackreference = false;
			function report(messageId, element, fix) {
				reported = true;
				if (fix && typeof fix === "object") context.report({
					node,
					loc: getRegexpLocation(element),
					messageId,
					data: { expr: mention(element) },
					suggest: [{
						messageId: fix.messageId,
						fix: fixReplaceNode(element, fix.fix)
					}]
				});
				else context.report({
					node,
					loc: getRegexpLocation(element),
					messageId,
					data: { expr: mention(element) },
					fix: fix ? fixReplaceNode(element, fix) : null
				});
			}
			return {
				onCharacterEnter(cNode) {
					if (cNode.raw === "\\") {
						report("invalidControlEscape", cNode);
						return;
					}
					if (cNode.raw === "\\u" || cNode.raw === "\\x") {
						report("incompleteEscapeSequence", cNode);
						return;
					}
					if (cNode.raw === "\\p" || cNode.raw === "\\P") {
						report("invalidPropertyEscape", cNode);
						return;
					}
					if (cNode.value !== 0 && isOctalEscape(cNode.raw)) {
						report("octalEscape", cNode, {
							fix: `\\x${cNode.value.toString(16).padStart(2, "0")}`,
							messageId: "hexEscapeSuggestion"
						});
						return;
					}
					const insideCharClass = cNode.parent.type === "CharacterClass" || cNode.parent.type === "CharacterClassRange";
					if (!insideCharClass) {
						if (cNode.raw === "\\k") {
							report("incompleteBackreference", cNode);
							return;
						}
						if (cNode.raw === "{" || cNode.raw === "}" || cNode.raw === "]") {
							report("unescapedSourceCharacter", cNode, `\\${cNode.raw}`);
							return;
						}
					}
					if (isEscapeSequence(cNode.raw)) return;
					if (cNode.raw[0] === "\\") {
						const identity = cNode.raw.slice(1);
						const syntaxChars = insideCharClass ? CHARACTER_CLASS_SYNTAX_CHARACTERS : SYNTAX_CHARACTERS;
						if (cNode.value === identity.charCodeAt(0) && !syntaxChars.has(identity)) report("uselessEscape", cNode, identity);
					}
				},
				onCharacterClassEnter(ccNode) {
					for (let i = 0; i < ccNode.elements.length; i++) {
						const current = ccNode.elements[i];
						if (current.type === "CharacterSet") {
							const next = ccNode.elements[i + 1];
							const nextNext = ccNode.elements[i + 2];
							if (next && next.raw === "-" && nextNext) {
								report("invalidRange", current);
								return;
							}
							const prev = ccNode.elements[i - 1];
							const prevPrev = ccNode.elements[i - 2];
							if (prev && prev.raw === "-" && prevPrev && prevPrev.type !== "CharacterClassRange") {
								report("invalidRange", current);
								return;
							}
						}
					}
				},
				onQuantifierEnter(qNode) {
					if (qNode.element.type === "Assertion") report("quantifiedAssertion", qNode, `(?:${qNode.element.raw})${qNode.raw.slice(qNode.element.end - qNode.start)}`);
				},
				onBackreferenceEnter(bNode) {
					if (typeof bNode.ref === "string") hasNamedBackreference = true;
				},
				onPatternLeave() {
					if (hasNamedBackreference) return;
					if (!reported) {
						const message = validateRegExpPattern(pattern, flags);
						if (message) context.report({
							node,
							messageId: "regexMessage",
							data: { message }
						});
					}
				}
			};
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/unicode-escape.ts
var unicode_escape_default = createRule("unicode-escape", {
	meta: {
		docs: {
			description: "enforce consistent usage of unicode escape or unicode codepoint escape",
			category: "Stylistic Issues",
			recommended: false
		},
		fixable: "code",
		schema: [{ enum: ["unicodeCodePointEscape", "unicodeEscape"] }],
		messages: {
			expectedUnicodeCodePointEscape: "Expected unicode code point escape ('{{unicodeCodePointEscape}}'), but unicode escape ('{{unicodeEscape}}') is used.",
			expectedUnicodeEscape: "Expected unicode escape ('{{unicodeEscape}}'), but unicode code point escape ('{{unicodeCodePointEscape}}') is used."
		},
		type: "suggestion"
	},
	create(context) {
		const preferUnicodeCodePointEscape = context.options[0] !== "unicodeEscape";
		function verifyForUnicodeCodePointEscape({ node, getRegexpLocation, fixReplaceNode }, kind, cNode) {
			if (kind !== EscapeSequenceKind.unicode) return;
			const unicodeCodePointEscape = `\\u{${cNode.value.toString(16)}}`;
			context.report({
				node,
				loc: getRegexpLocation(cNode),
				messageId: "expectedUnicodeCodePointEscape",
				data: {
					unicodeCodePointEscape,
					unicodeEscape: cNode.raw
				},
				fix: fixReplaceNode(cNode, unicodeCodePointEscape)
			});
		}
		function verifyForUnicodeEscape({ node, getRegexpLocation, fixReplaceNode }, kind, cNode) {
			if (kind !== EscapeSequenceKind.unicodeCodePoint) return;
			const unicodeEscape = `\\u${cNode.value.toString(16).padStart(4, "0")}`;
			context.report({
				node,
				loc: getRegexpLocation(cNode),
				messageId: "expectedUnicodeEscape",
				data: {
					unicodeEscape,
					unicodeCodePointEscape: cNode.raw
				},
				fix: fixReplaceNode(cNode, unicodeEscape)
			});
		}
		const verify = preferUnicodeCodePointEscape ? verifyForUnicodeCodePointEscape : verifyForUnicodeEscape;
		function createVisitor(regexpContext) {
			const { flags } = regexpContext;
			if (!flags.unicode && !flags.unicodeSets) return {};
			return { onCharacterEnter(cNode) {
				if (cNode.value >= 65536) return;
				const kind = getEscapeSequenceKind(cNode.raw);
				if (!kind) return;
				verify(regexpContext, kind, cNode);
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/utils/unicode-alias.ts
var AliasMap = class {
	toShortMap;
	toLongMap;
	constructor({ shortToLong, otherToLong }) {
		const toShortMap = /* @__PURE__ */ new Map();
		const toLongMap = /* @__PURE__ */ new Map();
		for (const [short, long] of Object.entries(shortToLong)) {
			toShortMap.set(long, short);
			toLongMap.set(short, long);
		}
		for (const [other, long] of Object.entries(otherToLong)) {
			toLongMap.set(other, long);
			const short = toShortMap.get(long);
			if (!short) throw new Error(`No short key for ${long} with other key ${other}`);
			toShortMap.set(other, short);
		}
		this.toShortMap = toShortMap;
		this.toLongMap = toLongMap;
	}
	toShort(key) {
		return this.toShortMap.get(key) || key;
	}
	toLong(key) {
		return this.toLongMap.get(key) || key;
	}
};
const UNICODE_CATEGORY_ALIAS = new AliasMap({
	shortToLong: {
		gc: "General_Category",
		sc: "Script",
		scx: "Script_Extensions"
	},
	otherToLong: {}
});
const UNICODE_BINARY_PROPERTY_ALIAS = new AliasMap({
	shortToLong: {
		AHex: "ASCII_Hex_Digit",
		Alpha: "Alphabetic",
		Bidi_C: "Bidi_Control",
		Bidi_M: "Bidi_Mirrored",
		CE: "Composition_Exclusion",
		CI: "Case_Ignorable",
		Comp_Ex: "Full_Composition_Exclusion",
		CWCF: "Changes_When_Casefolded",
		CWCM: "Changes_When_Casemapped",
		CWKCF: "Changes_When_NFKC_Casefolded",
		CWL: "Changes_When_Lowercased",
		CWT: "Changes_When_Titlecased",
		CWU: "Changes_When_Uppercased",
		Dep: "Deprecated",
		DI: "Default_Ignorable_Code_Point",
		Dia: "Diacritic",
		EBase: "Emoji_Modifier_Base",
		EComp: "Emoji_Component",
		EMod: "Emoji_Modifier",
		EPres: "Emoji_Presentation",
		Ext: "Extender",
		ExtPict: "Extended_Pictographic",
		Gr_Base: "Grapheme_Base",
		Gr_Ext: "Grapheme_Extend",
		Gr_Link: "Grapheme_Link",
		Hex: "Hex_Digit",
		IDC: "ID_Continue",
		Ideo: "Ideographic",
		IDS: "ID_Start",
		IDSB: "IDS_Binary_Operator",
		IDST: "IDS_Trinary_Operator",
		IDSU: "IDS_Unary_Operator",
		Join_C: "Join_Control",
		LOE: "Logical_Order_Exception",
		Lower: "Lowercase",
		MCM: "Modifier_Combining_Mark",
		NChar: "Noncharacter_Code_Point",
		OAlpha: "Other_Alphabetic",
		ODI: "Other_Default_Ignorable_Code_Point",
		OGr_Ext: "Other_Grapheme_Extend",
		OIDC: "Other_ID_Continue",
		OIDS: "Other_ID_Start",
		OLower: "Other_Lowercase",
		OMath: "Other_Math",
		OUpper: "Other_Uppercase",
		Pat_Syn: "Pattern_Syntax",
		Pat_WS: "Pattern_White_Space",
		PCM: "Prepended_Concatenation_Mark",
		QMark: "Quotation_Mark",
		RI: "Regional_Indicator",
		SD: "Soft_Dotted",
		STerm: "Sentence_Terminal",
		Term: "Terminal_Punctuation",
		UIdeo: "Unified_Ideograph",
		Upper: "Uppercase",
		VS: "Variation_Selector",
		WSpace: "White_Space",
		XIDC: "XID_Continue",
		XIDS: "XID_Start",
		XO_NFC: "Expands_On_NFC",
		XO_NFD: "Expands_On_NFD",
		XO_NFKC: "Expands_On_NFKC",
		XO_NFKD: "Expands_On_NFKD"
	},
	otherToLong: { space: "White_Space" }
});
const UNICODE_GENERAL_CATEGORY_ALIAS = new AliasMap({
	shortToLong: {
		C: "Other",
		Cc: "Control",
		Cf: "Format",
		Cn: "Unassigned",
		Co: "Private_Use",
		Cs: "Surrogate",
		L: "Letter",
		LC: "Cased_Letter",
		Ll: "Lowercase_Letter",
		Lm: "Modifier_Letter",
		Lo: "Other_Letter",
		Lt: "Titlecase_Letter",
		Lu: "Uppercase_Letter",
		M: "Mark",
		Mc: "Spacing_Mark",
		Me: "Enclosing_Mark",
		Mn: "Nonspacing_Mark",
		N: "Number",
		Nd: "Decimal_Number",
		Nl: "Letter_Number",
		No: "Other_Number",
		P: "Punctuation",
		Pc: "Connector_Punctuation",
		Pd: "Dash_Punctuation",
		Pe: "Close_Punctuation",
		Pf: "Final_Punctuation",
		Pi: "Initial_Punctuation",
		Po: "Other_Punctuation",
		Ps: "Open_Punctuation",
		S: "Symbol",
		Sc: "Currency_Symbol",
		Sk: "Modifier_Symbol",
		Sm: "Math_Symbol",
		So: "Other_Symbol",
		Z: "Separator",
		Zl: "Line_Separator",
		Zp: "Paragraph_Separator",
		Zs: "Space_Separator"
	},
	otherToLong: {
		cntrl: "Control",
		Combining_Mark: "Mark",
		digit: "Decimal_Number",
		punct: "Punctuation"
	}
});
const UNICODE_SCRIPT_ALIAS = new AliasMap({
	shortToLong: {
		Adlm: "Adlam",
		Aghb: "Caucasian_Albanian",
		Arab: "Arabic",
		Armi: "Imperial_Aramaic",
		Armn: "Armenian",
		Avst: "Avestan",
		Bali: "Balinese",
		Bamu: "Bamum",
		Bass: "Bassa_Vah",
		Batk: "Batak",
		Beng: "Bengali",
		Berf: "Beria_Erfe",
		Bhks: "Bhaiksuki",
		Bopo: "Bopomofo",
		Brah: "Brahmi",
		Brai: "Braille",
		Bugi: "Buginese",
		Buhd: "Buhid",
		Cakm: "Chakma",
		Cans: "Canadian_Aboriginal",
		Cari: "Carian",
		Cher: "Cherokee",
		Chrs: "Chorasmian",
		Copt: "Coptic",
		Cpmn: "Cypro_Minoan",
		Cprt: "Cypriot",
		Cyrl: "Cyrillic",
		Deva: "Devanagari",
		Diak: "Dives_Akuru",
		Dogr: "Dogra",
		Dsrt: "Deseret",
		Dupl: "Duployan",
		Egyp: "Egyptian_Hieroglyphs",
		Elba: "Elbasan",
		Elym: "Elymaic",
		Ethi: "Ethiopic",
		Gara: "Garay",
		Geor: "Georgian",
		Glag: "Glagolitic",
		Gong: "Gunjala_Gondi",
		Gonm: "Masaram_Gondi",
		Goth: "Gothic",
		Gran: "Grantha",
		Grek: "Greek",
		Gujr: "Gujarati",
		Gukh: "Gurung_Khema",
		Guru: "Gurmukhi",
		Hang: "Hangul",
		Hani: "Han",
		Hano: "Hanunoo",
		Hatr: "Hatran",
		Hebr: "Hebrew",
		Hira: "Hiragana",
		Hluw: "Anatolian_Hieroglyphs",
		Hmng: "Pahawh_Hmong",
		Hmnp: "Nyiakeng_Puachue_Hmong",
		Hrkt: "Katakana_Or_Hiragana",
		Hung: "Old_Hungarian",
		Ital: "Old_Italic",
		Java: "Javanese",
		Kali: "Kayah_Li",
		Kana: "Katakana",
		Khar: "Kharoshthi",
		Khmr: "Khmer",
		Khoj: "Khojki",
		Kits: "Khitan_Small_Script",
		Knda: "Kannada",
		Krai: "Kirat_Rai",
		Kthi: "Kaithi",
		Lana: "Tai_Tham",
		Laoo: "Lao",
		Latn: "Latin",
		Lepc: "Lepcha",
		Limb: "Limbu",
		Lina: "Linear_A",
		Linb: "Linear_B",
		Lyci: "Lycian",
		Lydi: "Lydian",
		Mahj: "Mahajani",
		Maka: "Makasar",
		Mand: "Mandaic",
		Mani: "Manichaean",
		Marc: "Marchen",
		Medf: "Medefaidrin",
		Mend: "Mende_Kikakui",
		Merc: "Meroitic_Cursive",
		Mero: "Meroitic_Hieroglyphs",
		Mlym: "Malayalam",
		Mong: "Mongolian",
		Mroo: "Mro",
		Mtei: "Meetei_Mayek",
		Mult: "Multani",
		Mymr: "Myanmar",
		Nagm: "Nag_Mundari",
		Nand: "Nandinagari",
		Narb: "Old_North_Arabian",
		Nbat: "Nabataean",
		Nkoo: "Nko",
		Nshu: "Nushu",
		Ogam: "Ogham",
		Olck: "Ol_Chiki",
		Onao: "Ol_Onal",
		Orkh: "Old_Turkic",
		Orya: "Oriya",
		Osge: "Osage",
		Osma: "Osmanya",
		Ougr: "Old_Uyghur",
		Palm: "Palmyrene",
		Pauc: "Pau_Cin_Hau",
		Perm: "Old_Permic",
		Phag: "Phags_Pa",
		Phli: "Inscriptional_Pahlavi",
		Phlp: "Psalter_Pahlavi",
		Phnx: "Phoenician",
		Plrd: "Miao",
		Prti: "Inscriptional_Parthian",
		Rjng: "Rejang",
		Rohg: "Hanifi_Rohingya",
		Runr: "Runic",
		Samr: "Samaritan",
		Sarb: "Old_South_Arabian",
		Saur: "Saurashtra",
		Sgnw: "SignWriting",
		Shaw: "Shavian",
		Shrd: "Sharada",
		Sidd: "Siddham",
		Sidt: "Sidetic",
		Sind: "Khudawadi",
		Sinh: "Sinhala",
		Sogd: "Sogdian",
		Sogo: "Old_Sogdian",
		Sora: "Sora_Sompeng",
		Soyo: "Soyombo",
		Sund: "Sundanese",
		Sunu: "Sunuwar",
		Sylo: "Syloti_Nagri",
		Syrc: "Syriac",
		Tagb: "Tagbanwa",
		Takr: "Takri",
		Tale: "Tai_Le",
		Talu: "New_Tai_Lue",
		Taml: "Tamil",
		Tang: "Tangut",
		Tavt: "Tai_Viet",
		Tayo: "Tai_Yo",
		Telu: "Telugu",
		Tfng: "Tifinagh",
		Tglg: "Tagalog",
		Thaa: "Thaana",
		Tibt: "Tibetan",
		Tirh: "Tirhuta",
		Tnsa: "Tangsa",
		Todr: "Todhri",
		Tols: "Tolong_Siki",
		Tutg: "Tulu_Tigalari",
		Ugar: "Ugaritic",
		Vaii: "Vai",
		Vith: "Vithkuqi",
		Wara: "Warang_Citi",
		Wcho: "Wancho",
		Xpeo: "Old_Persian",
		Xsux: "Cuneiform",
		Yezi: "Yezidi",
		Yiii: "Yi",
		Zanb: "Zanabazar_Square",
		Zinh: "Inherited",
		Zyyy: "Common",
		Zzzz: "Unknown"
	},
	otherToLong: {
		Qaac: "Coptic",
		Qaai: "Inherited"
	}
});
//#endregion
//#region lib/rules/unicode-property.ts
function isGeneralCategory(key) {
	return UNICODE_CATEGORY_ALIAS.toShort(key) === "gc";
}
var unicode_property_default = createRule("unicode-property", {
	meta: {
		docs: {
			description: "enforce consistent naming of unicode properties",
			category: "Stylistic Issues",
			recommended: false
		},
		schema: [{
			type: "object",
			properties: {
				generalCategory: { enum: [
					"always",
					"never",
					"ignore"
				] },
				key: { enum: [
					"short",
					"long",
					"ignore"
				] },
				property: { anyOf: [{ enum: [
					"short",
					"long",
					"ignore"
				] }, {
					type: "object",
					properties: {
						binary: { enum: [
							"short",
							"long",
							"ignore"
						] },
						generalCategory: { enum: [
							"short",
							"long",
							"ignore"
						] },
						script: { enum: [
							"short",
							"long",
							"ignore"
						] }
					},
					additionalProperties: false
				}] }
			},
			additionalProperties: false
		}],
		messages: {
			unnecessaryGc: "Unnecessary '{{ gc }}=' in Unicode property.",
			missingGc: "Missing '{{ gc }}=' in Unicode property.",
			expectedKey: "Excepted {{ len }} key. Use '{{ key }}' instead.",
			expectedProperty: "Excepted {{ len }} {{ type }} property. Use '{{ prop }}' instead."
		},
		type: "suggestion",
		fixable: "code"
	},
	create(context) {
		const { generalCategory = "never", key: keyFormat = "ignore", property = {
			binary: "ignore",
			generalCategory: "ignore",
			script: "long"
		} } = context.options[0] || {};
		let defaultPropertyFormat = "long";
		if (typeof property === "string") defaultPropertyFormat = property;
		const { binary: binaryFormat = defaultPropertyFormat, generalCategory: generalCategoryFormat = defaultPropertyFormat, script: scriptFormat = defaultPropertyFormat } = typeof property === "string" ? {} : property;
		function createVisitor(regexpContext) {
			const { node, getRegexpLocation, fixReplaceNode } = regexpContext;
			function onUnicodeProperty(cs) {
				const keyValueSyntax = cs.raw.includes("=");
				function fixReplace(inner) {
					return fixReplaceNode(cs, `${cs.raw.slice(0, 2)}{${inner}}`);
				}
				function getKeyLocation() {
					const offset = 3;
					if (keyValueSyntax) return getRegexpLocation({
						start: cs.start + offset,
						end: cs.start + offset + cs.key.length
					});
					return getRegexpLocation({
						start: cs.start + offset,
						end: cs.end - 1
					});
				}
				function getValueLocation() {
					return getRegexpLocation({
						start: cs.end - 1 - (cs.value || cs.key).length,
						end: cs.end - 1
					});
				}
				const { key, value } = cs;
				if (value === null) {
					if (binaryFormat !== "ignore") {
						const expected = binaryFormat === "short" ? UNICODE_BINARY_PROPERTY_ALIAS.toShort(key) : UNICODE_BINARY_PROPERTY_ALIAS.toLong(key);
						if (key !== expected) context.report({
							node,
							loc: getKeyLocation(),
							messageId: "expectedProperty",
							data: {
								len: binaryFormat,
								type: "binary",
								prop: expected
							},
							fix: fixReplace(expected)
						});
					}
				} else {
					const isGC = isGeneralCategory(key);
					let handledKey = false;
					if (isGC) {
						if (keyValueSyntax && generalCategory === "never") {
							context.report({
								node,
								loc: getKeyLocation(),
								messageId: "unnecessaryGc",
								data: { gc: key },
								fix: fixReplace(value)
							});
							handledKey = true;
						}
						if (!keyValueSyntax && generalCategory === "always") {
							const missing = keyFormat === "long" ? "General_Category" : "gc";
							context.report({
								node,
								loc: getRegexpLocation(cs),
								messageId: "missingGc",
								data: { gc: missing },
								fix: fixReplace(`${missing}=${value}`)
							});
							handledKey = true;
						}
					}
					if (!handledKey && keyValueSyntax && keyFormat !== "ignore") {
						const expected = keyFormat === "short" ? UNICODE_CATEGORY_ALIAS.toShort(key) : UNICODE_CATEGORY_ALIAS.toLong(key);
						if (key !== expected) context.report({
							node,
							loc: getKeyLocation(),
							messageId: "expectedKey",
							data: {
								len: keyFormat,
								key: expected
							},
							fix: fixReplace(`${expected}=${value}`)
						});
					}
					const valueFormat = isGC ? generalCategoryFormat : scriptFormat;
					if (valueFormat !== "ignore") {
						const aliasMap = isGC ? UNICODE_GENERAL_CATEGORY_ALIAS : UNICODE_SCRIPT_ALIAS;
						const expected = valueFormat === "short" ? aliasMap.toShort(value) : aliasMap.toLong(value);
						if (value !== expected) {
							const prefix = keyValueSyntax ? `${key}=` : "";
							const type = isGC ? "General_Category" : "Script";
							context.report({
								node,
								loc: getValueLocation(),
								messageId: "expectedProperty",
								data: {
									len: valueFormat,
									type,
									prop: expected
								},
								fix: fixReplace(`${prefix}${expected}`)
							});
						}
					}
				}
			}
			return { onCharacterSetEnter(cs) {
				if (cs.kind === "property") onUnicodeProperty(cs);
			} };
		}
		return defineRegexpVisitor(context, { createVisitor });
	}
});
//#endregion
//#region lib/rules/use-ignore-case.ts
const ELEMENT_ORDER = {
	Character: 1,
	CharacterClassRange: 2,
	CharacterSet: 3,
	CharacterClass: 4,
	ExpressionCharacterClass: 5,
	ClassStringDisjunction: 6,
	StringAlternative: 7
};
/**
* Finds all character class elements that do not contribute to the whole.
*/
function findUseless(elements, getChars, other) {
	const get = cachedFn(getChars);
	const sortedElements = [...elements].reverse().sort((a, b) => ELEMENT_ORDER[a.type] - ELEMENT_ORDER[b.type]);
	const useless = /* @__PURE__ */ new Set();
	for (const e of sortedElements) {
		const cs = get(e);
		if (cs.isSubsetOf(other)) {
			useless.add(e);
			continue;
		}
		const otherElements = elements.filter((o) => o !== e && !useless.has(o));
		const total = other.union(...otherElements.map(get));
		if (cs.isSubsetOf(total)) {
			useless.add(e);
			continue;
		}
	}
	return useless;
}
/** Returns all elements not in the given set */
function without(iter, set) {
	const result = [];
	for (const item of iter) if (!set.has(item)) result.push(item);
	return result;
}
/**
* Removes all the given nodes from the given pattern.
*/
function removeAll(fixer, patternSource, nodes) {
	const sorted = CharSet.empty(Number.MAX_SAFE_INTEGER).union(nodes.map((n) => {
		let min = n.start;
		let max = n.end - 1;
		if (n.type === "StringAlternative") {
			const parent = n.parent;
			if (parent.alternatives.length === 1 || parent.alternatives.every((a) => nodes.includes(a))) {
				min = parent.start;
				max = parent.end - 1;
			} else if (parent.alternatives.at(0) === n) max++;
			else min--;
		}
		return {
			min,
			max
		};
	})).ranges.map(({ min, max }) => ({
		start: min,
		end: max + 1
	}));
	let pattern = patternSource.value;
	let removed = 0;
	for (const { start, end } of sorted) {
		pattern = pattern.slice(0, start - removed) + pattern.slice(end - removed);
		removed += end - start;
	}
	const range = patternSource.getReplaceRange({
		start: 0,
		end: patternSource.value.length
	});
	if (range) return range.replace(fixer, pattern);
	return null;
}
/**
* Adds the `i` flag to the given flags string.
*/
function getIgnoreCaseFlagsString(flags) {
	if (flags.includes("i")) return flags;
	for (let i = 0; i < flags.length; i++) if (flags[i] > "i") return `${flags.slice(0, i)}i${flags.slice(i)}`;
	return `${flags}i`;
}
//#endregion
//#region lib/all-rules.ts
const rules$3 = [
	confusing_quantifier_default,
	control_character_escape_default,
	grapheme_string_literal_default,
	hexadecimal_escape_default,
	letter_case_default,
	match_any_default,
	negation_default,
	no_contradiction_with_assertion_default,
	no_control_character_default,
	no_dupe_characters_character_class_default,
	no_dupe_disjunctions_default,
	no_empty_alternative_default,
	no_empty_capturing_group_default,
	no_empty_character_class_default,
	no_empty_group_default,
	no_empty_lookarounds_assertion_default,
	no_empty_string_literal_default,
	no_escape_backspace_default,
	no_extra_lookaround_assertions_default,
	no_invalid_regexp_default,
	no_invisible_character_default,
	no_lazy_ends_default,
	no_legacy_features_default,
	no_misleading_capturing_group_default,
	no_misleading_unicode_character_default,
	no_missing_g_flag_default,
	no_non_standard_flag_default,
	no_obscure_range_default,
	no_octal_default,
	no_optional_assertion_default,
	no_potentially_useless_backreference_default,
	no_standalone_backslash_default,
	no_super_linear_backtracking_default,
	no_super_linear_move_default,
	no_trivially_nested_assertion_default,
	no_trivially_nested_quantifier_default,
	no_unused_capturing_group_default,
	no_useless_assertions_default,
	no_useless_backreference_default,
	no_useless_character_class_default,
	no_useless_dollar_replacements_default,
	no_useless_escape_default,
	no_useless_flag_default,
	no_useless_lazy_default,
	no_useless_non_capturing_group_default,
	no_useless_quantifier_default,
	no_useless_range_default,
	no_useless_set_operand_default,
	no_useless_string_literal_default,
	no_useless_two_nums_quantifier_default,
	no_zero_quantifier_default,
	optimal_lookaround_quantifier_default,
	optimal_quantifier_concatenation_default,
	prefer_character_class_default,
	prefer_d_default,
	prefer_escape_replacement_dollar_char_default,
	prefer_lookaround_default,
	prefer_named_backreference_default,
	prefer_named_capture_group_default,
	prefer_named_replacement_default,
	prefer_plus_quantifier_default,
	prefer_predefined_assertion_default,
	prefer_quantifier_default,
	prefer_question_quantifier_default,
	prefer_range_default,
	prefer_regexp_exec_default,
	prefer_regexp_test_default,
	prefer_result_array_groups_default,
	prefer_set_operation_default,
	prefer_star_quantifier_default,
	prefer_unicode_codepoint_escapes_default,
	prefer_w_default,
	require_unicode_regexp_default,
	require_unicode_sets_regexp_default,
	simplify_set_operations_default,
	sort_alternatives_default,
	sort_character_class_elements_default,
	sort_flags_default,
	strict_default,
	unicode_escape_default,
	unicode_property_default,
	createRule("use-ignore-case", {
		meta: {
			docs: {
				description: "use the `i` flag if it simplifies the pattern",
				category: "Best Practices",
				recommended: true
			},
			fixable: "code",
			schema: [],
			messages: { unexpected: "The character class(es) {{ classes }} can be simplified using the `i` flag." },
			type: "suggestion"
		},
		create(context) {
			function createVisitor(regexpContext) {
				const { node, flags, ownsFlags, flagsString, patternAst, patternSource, getUsageOfPattern, getFlagsLocation, fixReplaceFlags } = regexpContext;
				if (!ownsFlags || flagsString === null) return {};
				if (flags.ignoreCase) return {};
				if (getUsageOfPattern() === UsageOfPattern.partial) return {};
				if (isCaseVariant(patternAst, flags)) return {};
				const uselessElements = [];
				const ccs = [];
				return {
					onCharacterClassEnter(ccNode) {
						const elements = ccNode.elements.flatMap((e) => {
							if (e.type === "ClassStringDisjunction") return e.alternatives;
							return [e];
						});
						const invariantElement = elements.filter((e) => !isCaseVariant(e, flags));
						if (invariantElement.length === elements.length) return;
						const invariant = JS.UnicodeSet.empty(Chars.maxChar(flags)).union(...invariantElement.map((e) => toUnicodeSet(e, flags)));
						let variantElements = without(elements, new Set(invariantElement));
						const alwaysUseless = findUseless(variantElements, (e) => toUnicodeSet(e, flags), invariant);
						variantElements = without(variantElements, alwaysUseless);
						const iFlags = getIgnoreCaseFlags(flags);
						const useless = findUseless(variantElements, (e) => toUnicodeSet(e, iFlags), invariant);
						uselessElements.push(...useless);
						ccs.push(ccNode);
					},
					onPatternLeave() {
						if (uselessElements.length === 0) return;
						context.report({
							node,
							loc: getFlagsLocation(),
							messageId: "unexpected",
							data: { classes: ccs.map((cc) => mention(cc)).join(", ") },
							fix(fixer) {
								const patternFix = removeAll(fixer, patternSource, uselessElements);
								if (!patternFix) return null;
								const flagsFix = fixReplaceFlags(getIgnoreCaseFlagsString(flagsString), false)(fixer);
								if (!flagsFix) return null;
								const fix = [patternFix];
								if (Array.isArray(flagsFix)) fix.push(...flagsFix);
								else fix.push(flagsFix);
								return fix;
							}
						});
					}
				};
			}
			return defineRegexpVisitor(context, { createVisitor });
		}
	})
];
//#endregion
//#region lib/configs/rules/recommended.ts
const rules$2 = {
	"no-control-regex": "error",
	"no-misleading-character-class": "error",
	"no-regex-spaces": "error",
	"prefer-regex-literals": "error",
	"no-invalid-regexp": "off",
	"no-useless-backreference": "off",
	"no-empty-character-class": "off",
	"regexp/confusing-quantifier": "warn",
	"regexp/control-character-escape": "error",
	"regexp/match-any": "error",
	"regexp/negation": "error",
	"regexp/no-contradiction-with-assertion": "error",
	"regexp/no-dupe-characters-character-class": "error",
	"regexp/no-dupe-disjunctions": "error",
	"regexp/no-empty-alternative": "warn",
	"regexp/no-empty-capturing-group": "error",
	"regexp/no-empty-character-class": "error",
	"regexp/no-empty-group": "error",
	"regexp/no-empty-lookarounds-assertion": "error",
	"regexp/no-empty-string-literal": "error",
	"regexp/no-escape-backspace": "error",
	"regexp/no-extra-lookaround-assertions": "error",
	"regexp/no-invalid-regexp": "error",
	"regexp/no-invisible-character": "error",
	"regexp/no-lazy-ends": "warn",
	"regexp/no-legacy-features": "error",
	"regexp/no-misleading-capturing-group": "error",
	"regexp/no-misleading-unicode-character": "error",
	"regexp/no-missing-g-flag": "error",
	"regexp/no-non-standard-flag": "error",
	"regexp/no-obscure-range": "error",
	"regexp/no-optional-assertion": "error",
	"regexp/no-potentially-useless-backreference": "warn",
	"regexp/no-super-linear-backtracking": "error",
	"regexp/no-trivially-nested-assertion": "error",
	"regexp/no-trivially-nested-quantifier": "error",
	"regexp/no-unused-capturing-group": "error",
	"regexp/no-useless-assertions": "error",
	"regexp/no-useless-backreference": "error",
	"regexp/no-useless-character-class": "error",
	"regexp/no-useless-dollar-replacements": "error",
	"regexp/no-useless-escape": "error",
	"regexp/no-useless-flag": "warn",
	"regexp/no-useless-lazy": "error",
	"regexp/no-useless-non-capturing-group": "error",
	"regexp/no-useless-quantifier": "error",
	"regexp/no-useless-range": "error",
	"regexp/no-useless-set-operand": "error",
	"regexp/no-useless-string-literal": "error",
	"regexp/no-useless-two-nums-quantifier": "error",
	"regexp/no-zero-quantifier": "error",
	"regexp/optimal-lookaround-quantifier": "warn",
	"regexp/optimal-quantifier-concatenation": "error",
	"regexp/prefer-character-class": "error",
	"regexp/prefer-d": "error",
	"regexp/prefer-plus-quantifier": "error",
	"regexp/prefer-predefined-assertion": "error",
	"regexp/prefer-question-quantifier": "error",
	"regexp/prefer-range": "error",
	"regexp/prefer-set-operation": "error",
	"regexp/prefer-star-quantifier": "error",
	"regexp/prefer-unicode-codepoint-escapes": "error",
	"regexp/prefer-w": "error",
	"regexp/simplify-set-operations": "error",
	"regexp/sort-flags": "error",
	"regexp/strict": "error",
	"regexp/use-ignore-case": "error"
};
//#endregion
//#region lib/configs/rules/all.ts
const all = {};
for (const rule of rules$3) all[rule.meta.docs.ruleId] = "error";
const rules$1 = {
	...all,
	...rules$2
};
//#endregion
//#region lib/configs/flat/all.ts
var all_exports = /* @__PURE__ */ __exportAll({
	plugins: () => plugins$1,
	rules: () => rules$1
});
const plugins$1 = { get regexp() {
	return regexp;
} };
//#endregion
//#region lib/configs/flat/recommended.ts
var recommended_exports = /* @__PURE__ */ __exportAll({
	plugins: () => plugins,
	rules: () => rules$2
});
const plugins = { get regexp() {
	return regexp;
} };
//#endregion
//#region lib/index.ts
const meta = {
	name: "eslint-plugin-regexp",
	version: "3.1.0"
};
const configs = {
	recommended: recommended_exports,
	all: all_exports,
	"flat/all": all_exports,
	"flat/recommended": recommended_exports
};
const rules = rules$3.reduce((obj, r) => {
	obj[r.meta.docs.ruleName] = r;
	return obj;
}, {});
const regexp = {
	configs,
	rules,
	meta
};
//#endregion
export { configs, regexp as default, meta, rules };
