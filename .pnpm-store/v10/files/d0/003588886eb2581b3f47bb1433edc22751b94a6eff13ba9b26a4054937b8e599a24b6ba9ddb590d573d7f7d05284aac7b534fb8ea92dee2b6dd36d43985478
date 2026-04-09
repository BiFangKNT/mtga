'use strict';

var fs = require('node:fs');
var path = require('node:path');

/**
 * @fileoverview Functions to fix up rules to provide missing methods on the `context` and `sourceCode` objects.
 * @author Nicholas C. Zakas
 */

//-----------------------------------------------------------------------------
// Types
//-----------------------------------------------------------------------------

/** @typedef {import("@eslint/core").Plugin} FixupPluginDefinition */
/** @typedef {import("@eslint/core").RuleDefinition} FixupRuleDefinition */
/** @typedef {FixupRuleDefinition["create"]} FixupLegacyRuleDefinition */
/** @typedef {import("@eslint/core").ConfigObject} FixupConfig */
/** @typedef {Array<FixupConfig>} FixupConfigArray */

//-----------------------------------------------------------------------------
// Data
//-----------------------------------------------------------------------------

/**
 * The removed methods from the `context` object that need to be added back.
 * The keys are the name of the method on the `context` object and the values
 * are the name of the method on the `sourceCode` object.
 * @type {Map<string, string>}
 */
const removedMethodNames = new Map([
	["getSource", "getText"],
	["getSourceLines", "getLines"],
	["getAllComments", "getAllComments"],
	["getDeclaredVariables", "getDeclaredVariables"],
	["getNodeByRangeIndex", "getNodeByRangeIndex"],
	["getCommentsBefore", "getCommentsBefore"],
	["getCommentsAfter", "getCommentsAfter"],
	["getCommentsInside", "getCommentsInside"],
	["getJSDocComment", "getJSDocComment"],
	["getFirstToken", "getFirstToken"],
	["getFirstTokens", "getFirstTokens"],
	["getLastToken", "getLastToken"],
	["getLastTokens", "getLastTokens"],
	["getTokenAfter", "getTokenAfter"],
	["getTokenBefore", "getTokenBefore"],
	["getTokenByRangeStart", "getTokenByRangeStart"],
	["getTokens", "getTokens"],
	["getTokensAfter", "getTokensAfter"],
	["getTokensBefore", "getTokensBefore"],
	["getTokensBetween", "getTokensBetween"],
]);

/**
 * Tracks the original rule definition and the fixed-up rule definition.
 * @type {WeakMap<FixupRuleDefinition|FixupLegacyRuleDefinition,FixupRuleDefinition>}
 */
const fixedUpRuleReplacements = new WeakMap();

/**
 * Tracks all of the fixed up rule definitions so we don't duplicate effort.
 * @type {WeakSet<FixupRuleDefinition>}
 */
const fixedUpRules = new WeakSet();

/**
 * Tracks the original plugin definition and the fixed-up plugin definition.
 * @type {WeakMap<FixupPluginDefinition,FixupPluginDefinition>}
 */
const fixedUpPluginReplacements = new WeakMap();

/**
 * Tracks all of the fixed up plugin definitions so we don't duplicate effort.
 * @type {WeakSet<FixupPluginDefinition>}
 */
const fixedUpPlugins = new WeakSet();

//-----------------------------------------------------------------------------
// Helpers
//-----------------------------------------------------------------------------

/**
 * Determines if two nodes or tokens overlap.
 * @param {object} first The first node or token to check.
 * @param {object} second The second node or token to check.
 * @returns {boolean} True if the two nodes or tokens overlap.
 */
function nodesOrTokensOverlap(first, second) {
	return (
		(first.range[0] <= second.range[0] &&
			first.range[1] >= second.range[0]) ||
		(second.range[0] <= first.range[0] && second.range[1] >= first.range[0])
	);
}

/**
 * Checks whether a node is an export declaration.
 * @param {object} node An AST node.
 * @returns {boolean} True if the node is an export declaration.
 */
function looksLikeExport(node) {
	return (
		node.type === "ExportDefaultDeclaration" ||
		node.type === "ExportNamedDeclaration"
	);
}

/**
 * Checks for the presence of a JSDoc comment for the given node and returns it.
 * @param {object} node The AST node to get the comment for.
 * @param {object} sourceCode A SourceCode instance to get comments.
 * @returns {object|null} The Block comment token containing the JSDoc comment
 *      for the given node or null if not found.
 */
function findJSDocComment(node, sourceCode) {
	const tokenBefore = sourceCode.getTokenBefore(node, {
		includeComments: true,
	});

	if (
		tokenBefore &&
		tokenBefore.type === "Block" &&
		tokenBefore.value.charAt(0) === "*" &&
		node.loc.start.line - tokenBefore.loc.end.line <= 1
	) {
		return tokenBefore;
	}

	return null;
}

//-----------------------------------------------------------------------------
// Exports
//-----------------------------------------------------------------------------

/**
 * Takes the given rule and creates a new rule with the `create()` method wrapped
 * to provide missing methods on the `context` and `sourceCode` objects.
 * @param {FixupRuleDefinition|FixupLegacyRuleDefinition} ruleDefinition The rule to fix up.
 * @returns {FixupRuleDefinition} The fixed-up rule.
 */
function fixupRule(ruleDefinition) {
	// first check if we've already fixed up this rule
	if (fixedUpRuleReplacements.has(ruleDefinition)) {
		return fixedUpRuleReplacements.get(ruleDefinition);
	}

	const isLegacyRule = typeof ruleDefinition === "function";

	// check to see if this rule definition has already been fixed up
	if (!isLegacyRule && fixedUpRules.has(ruleDefinition)) {
		return ruleDefinition;
	}

	const originalCreate = isLegacyRule
		? ruleDefinition
		: ruleDefinition.create.bind(ruleDefinition);

	function ruleCreate(context) {
		const sourceCode = context.sourceCode;

		// No need to create old methods for ESLint < 9
		if ("getScope" in context) {
			return originalCreate(context);
		}

		let eslintVersion = 9;
		if (!("getCwd" in context)) {
			eslintVersion = 10;
		}

		let compatSourceCode = sourceCode;
		if (eslintVersion >= 10) {
			compatSourceCode = Object.assign(Object.create(sourceCode), {
				getTokenOrCommentBefore(node, skip) {
					return sourceCode.getTokenBefore(node, {
						includeComments: true,
						skip,
					});
				},
				getTokenOrCommentAfter(node, skip) {
					return sourceCode.getTokenAfter(node, {
						includeComments: true,
						skip,
					});
				},
				isSpaceBetweenTokens(first, second) {
					if (nodesOrTokensOverlap(first, second)) {
						return false;
					}

					const [startingNodeOrToken, endingNodeOrToken] =
						first.range[1] <= second.range[0]
							? [first, second]
							: [second, first];
					const firstToken =
						sourceCode.getLastToken(startingNodeOrToken) ||
						startingNodeOrToken;
					const finalToken =
						sourceCode.getFirstToken(endingNodeOrToken) ||
						endingNodeOrToken;
					let currentToken = firstToken;

					while (currentToken !== finalToken) {
						const nextToken = sourceCode.getTokenAfter(
							currentToken,
							{
								includeComments: true,
							},
						);

						if (
							currentToken.range[1] !== nextToken.range[0] ||
							(nextToken !== finalToken &&
								nextToken.type === "JSXText" &&
								/\s/u.test(nextToken.value))
						) {
							return true;
						}

						currentToken = nextToken;
					}

					return false;
				},
				getJSDocComment(node) {
					let parent = node.parent;

					switch (node.type) {
						case "ClassDeclaration":
						case "FunctionDeclaration":
							return findJSDocComment(
								looksLikeExport(parent) ? parent : node,
								sourceCode,
							);

						case "ClassExpression":
							return findJSDocComment(parent.parent, sourceCode);

						case "ArrowFunctionExpression":
						case "FunctionExpression":
							if (
								parent.type !== "CallExpression" &&
								parent.type !== "NewExpression"
							) {
								while (
									!sourceCode.getCommentsBefore(parent)
										.length &&
									!/Function/u.test(parent.type) &&
									parent.type !== "MethodDefinition" &&
									parent.type !== "Property"
								) {
									parent = parent.parent;

									if (!parent) {
										break;
									}
								}

								if (
									parent &&
									parent.type !== "FunctionDeclaration" &&
									parent.type !== "Program"
								) {
									return findJSDocComment(parent, sourceCode);
								}
							}

							return findJSDocComment(node, sourceCode);

						default:
							return null;
					}
				},
			});

			Object.freeze(compatSourceCode);
		}

		let currentNode = compatSourceCode.ast;

		const compatContext = Object.assign(Object.create(context), {
			parserServices: compatSourceCode.parserServices,

			/*
			 * The following methods rely on the current node in the traversal,
			 * so we need to add them manually.
			 */
			getScope() {
				return compatSourceCode.getScope(currentNode);
			},

			getAncestors() {
				return compatSourceCode.getAncestors(currentNode);
			},

			markVariableAsUsed(variable) {
				compatSourceCode.markVariableAsUsed(variable, currentNode);
			},
		});

		if (eslintVersion >= 10) {
			Object.assign(compatContext, {
				parserOptions: compatContext.languageOptions.parserOptions,

				getCwd() {
					return compatContext.cwd;
				},

				getFilename() {
					return compatContext.filename;
				},

				getPhysicalFilename() {
					return compatContext.physicalFilename;
				},

				getSourceCode() {
					return compatSourceCode;
				},
			});

			Object.defineProperty(compatContext, "sourceCode", {
				enumerable: true,
				value: compatSourceCode,
			});
		}

		// add passthrough methods
		for (const [
			contextMethodName,
			sourceCodeMethodName,
		] of removedMethodNames) {
			compatContext[contextMethodName] =
				compatSourceCode[sourceCodeMethodName].bind(compatSourceCode);
		}

		// freeze just like the original context
		Object.freeze(compatContext);

		/*
		 * Create the visitor object using the original create() method.
		 * This is necessary to ensure that the visitor object is created
		 * with the correct context.
		 */
		const visitor = originalCreate(compatContext);

		/*
		 * Wrap each method in the visitor object to update the currentNode
		 * before calling the original method. This is necessary because the
		 * methods like `getScope()` need to know the current node.
		 */
		for (const [methodName, method] of Object.entries(visitor)) {
			/*
			 * Node is the second argument to most code path methods,
			 * and the third argument for onCodePathSegmentLoop.
			 */
			if (methodName.startsWith("on")) {
				// eslint-disable-next-line no-loop-func -- intentionally updating shared `currentNode` variable
				visitor[methodName] = (...args) => {
					currentNode =
						args[methodName === "onCodePathSegmentLoop" ? 2 : 1];

					return method.call(visitor, ...args);
				};

				continue;
			}

			// eslint-disable-next-line no-loop-func -- intentionally updating shared `currentNode` variable
			visitor[methodName] = (...args) => {
				currentNode = args[0];

				return method.call(visitor, ...args);
			};
		}

		return visitor;
	}

	const newRuleDefinition = {
		...(isLegacyRule ? undefined : ruleDefinition),
		create: ruleCreate,
	};

	// copy `schema` property of function-style rule or top-level `schema` property of object-style rule into `meta` object
	// @ts-ignore -- top-level `schema` property was not officially supported for object-style rules so it doesn't exist in types
	const { schema } = ruleDefinition;
	if (schema) {
		if (!newRuleDefinition.meta) {
			newRuleDefinition.meta = { schema };
		} else {
			newRuleDefinition.meta = {
				...newRuleDefinition.meta,
				// top-level `schema` had precedence over `meta.schema` so it's okay to overwrite `meta.schema` if it exists
				schema,
			};
		}
	}

	// cache the fixed up rule
	fixedUpRuleReplacements.set(ruleDefinition, newRuleDefinition);
	fixedUpRules.add(newRuleDefinition);

	return newRuleDefinition;
}

/**
 * Takes the given plugin and creates a new plugin with all of the rules wrapped
 * to provide missing methods on the `context` and `sourceCode` objects.
 * @param {FixupPluginDefinition} plugin The plugin to fix up.
 * @returns {FixupPluginDefinition} The fixed-up plugin.
 */
function fixupPluginRules(plugin) {
	// first check if we've already fixed up this plugin
	if (fixedUpPluginReplacements.has(plugin)) {
		return fixedUpPluginReplacements.get(plugin);
	}

	/*
	 * If the plugin has already been fixed up, or if the plugin
	 * doesn't have any rules, we can just return it.
	 */
	if (fixedUpPlugins.has(plugin) || !plugin.rules) {
		return plugin;
	}

	const newPlugin = {
		...plugin,
		rules: Object.fromEntries(
			Object.entries(plugin.rules).map(([ruleId, ruleDefinition]) => [
				ruleId,
				fixupRule(ruleDefinition),
			]),
		),
	};

	// cache the fixed up plugin
	fixedUpPluginReplacements.set(plugin, newPlugin);
	fixedUpPlugins.add(newPlugin);

	return newPlugin;
}

/**
 * Takes the given configuration and creates a new configuration with all of the
 * rules wrapped to provide missing methods on the `context` and `sourceCode` objects.
 * @param {FixupConfigArray|FixupConfig} config The configuration to fix up.
 * @returns {FixupConfigArray} The fixed-up configuration.
 */
function fixupConfigRules(config) {
	const configs = Array.isArray(config) ? config : [config];

	return configs.map(configItem => {
		if (!configItem.plugins) {
			return configItem;
		}

		const newPlugins = Object.fromEntries(
			Object.entries(configItem.plugins).map(([pluginName, plugin]) => [
				pluginName,
				fixupPluginRules(plugin),
			]),
		);

		return {
			...configItem,
			plugins: newPlugins,
		};
	});
}

/**
 * @fileoverview Ignore file utilities for the compat package.
 * @author Nicholas C. Zakas
 */


//-----------------------------------------------------------------------------
// Types
//-----------------------------------------------------------------------------

/** @typedef {import("@eslint/core").ConfigObject} FlatConfig */

//-----------------------------------------------------------------------------
// Exports
//-----------------------------------------------------------------------------

/**
 * Converts an ESLint ignore pattern to a minimatch pattern.
 * @param {string} pattern The .eslintignore or .gitignore pattern to convert.
 * @returns {string} The converted pattern.
 */
function convertIgnorePatternToMinimatch(pattern) {
	const isNegated = pattern.startsWith("!");
	const negatedPrefix = isNegated ? "!" : "";
	const patternToTest = (isNegated ? pattern.slice(1) : pattern).trimEnd();

	// special cases
	if (["", "**", "/**", "**/"].includes(patternToTest)) {
		return `${negatedPrefix}${patternToTest}`;
	}

	const firstIndexOfSlash = patternToTest.indexOf("/");

	const matchEverywherePrefix =
		firstIndexOfSlash < 0 || firstIndexOfSlash === patternToTest.length - 1
			? "**/"
			: "";

	const patternWithoutLeadingSlash =
		firstIndexOfSlash === 0 ? patternToTest.slice(1) : patternToTest;

	/*
	 * Escape `{` and `(` because in gitignore patterns they are just
	 * literal characters without any specific syntactic meaning,
	 * while in minimatch patterns they can form brace expansion or extglob syntax.
	 *
	 * For example, gitignore pattern `src/{a,b}.js` ignores file `src/{a,b}.js`.
	 * But, the same minimatch pattern `src/{a,b}.js` ignores files `src/a.js` and `src/b.js`.
	 * Minimatch pattern `src/\{a,b}.js` is equivalent to gitignore pattern `src/{a,b}.js`.
	 */
	const escapedPatternWithoutLeadingSlash =
		patternWithoutLeadingSlash.replaceAll(
			// eslint-disable-next-line regexp/no-empty-lookarounds-assertion -- False positive
			/(?=((?:\\.|[^{(])*))\1([{(])/guy,
			"$1\\$2",
		);

	const matchInsideSuffix = patternToTest.endsWith("/**") ? "/*" : "";

	return `${negatedPrefix}${matchEverywherePrefix}${escapedPatternWithoutLeadingSlash}${matchInsideSuffix}`;
}

/**
 * Reads an ignore file and returns an object with the ignore patterns.
 * @param {string} ignoreFilePath The absolute path to the ignore file.
 * @param {string} [name] The name of the ignore file config.
 * @returns {FlatConfig} An object with an `ignores` property that is an array of ignore patterns.
 * @throws {Error} If the ignore file path is not an absolute path.
 */
function includeIgnoreFile(ignoreFilePath, name) {
	if (!path.isAbsolute(ignoreFilePath)) {
		throw new Error("The ignore file location must be an absolute path.");
	}

	const ignoreFile = fs.readFileSync(ignoreFilePath, "utf8");
	const lines = ignoreFile.split(/\r?\n/u);

	return {
		name: name || "Imported .gitignore patterns",
		ignores: lines
			.map(line => line.trim())
			.filter(line => line && !line.startsWith("#"))
			.map(convertIgnorePatternToMinimatch),
	};
}

exports.convertIgnorePatternToMinimatch = convertIgnorePatternToMinimatch;
exports.fixupConfigRules = fixupConfigRules;
exports.fixupPluginRules = fixupPluginRules;
exports.fixupRule = fixupRule;
exports.includeIgnoreFile = includeIgnoreFile;
