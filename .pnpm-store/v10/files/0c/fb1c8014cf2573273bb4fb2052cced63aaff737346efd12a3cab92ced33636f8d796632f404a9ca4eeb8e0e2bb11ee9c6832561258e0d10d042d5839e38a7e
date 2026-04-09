import { a as createRule } from "../utils.mjs";

//#region src/rules/newline-after-import/newline-after-import.ts
function isStaticRequire(node) {
	return node && node.callee && node.callee.type === "Identifier" && node.callee.name === "require" && node.arguments.length === 1 && node.arguments[0].type === "Literal" && typeof node.arguments[0].value === "string";
}
function containsNodeOrEqual(outerNode, innerNode) {
	return outerNode.range[0] <= innerNode.range[0] && outerNode.range[1] >= innerNode.range[1];
}
function getScopeBody(scope) {
	if (scope.block.type === "SwitchStatement") {
		console.log("SwitchStatement scopes not supported");
		return [];
	}
	const body = "body" in scope.block ? scope.block.body : null;
	if (body && "type" in body && body.type === "BlockStatement") return body.body;
	return Array.isArray(body) ? body : [];
}
function findNodeIndexInScopeBody(body, nodeToFind) {
	return body.findIndex((node) => containsNodeOrEqual(node, nodeToFind));
}
function getLineDifference(node, nextNode) {
	return nextNode.loc.start.line - node.loc.end.line;
}
function isClassWithDecorator(node) {
	return node.type === "ClassDeclaration" && !!node.decorators?.length;
}
function isExportDefaultClass(node) {
	return node.type === "ExportDefaultDeclaration" && node.declaration.type === "ClassDeclaration";
}
function isExportNameClass(node) {
	return node.type === "ExportNamedDeclaration" && node.declaration?.type === "ClassDeclaration";
}
var newline_after_import_default = createRule({
	name: "newline-after-import",
	meta: {
		type: "layout",
		docs: { description: "Enforce a newline after import statements." },
		fixable: "whitespace",
		schema: [{
			type: "object",
			properties: {
				count: {
					type: "integer",
					minimum: 1
				},
				exactCount: { type: "boolean" },
				considerComments: { type: "boolean" }
			},
			additionalProperties: false
		}],
		messages: { newline: "Expected {{count}} empty line{{lineSuffix}} after {{type}} statement not followed by another {{type}}." }
	},
	defaultOptions: [{
		count: 1,
		exactCount: false,
		considerComments: false
	}],
	create(context, [options]) {
		const { count = 1, exactCount = false, considerComments = false } = options || {};
		let level = 0;
		const requireCalls = [];
		function checkForNewLine(node, nextNode, type) {
			if (isExportDefaultClass(nextNode) || isExportNameClass(nextNode)) {
				const classNode = nextNode.declaration;
				if (isClassWithDecorator(classNode)) nextNode = classNode.decorators[0];
			} else if (isClassWithDecorator(nextNode)) nextNode = nextNode.decorators[0];
			const lineDifference = getLineDifference(node, nextNode);
			const EXPECTED_LINE_DIFFERENCE = count + 1;
			if (lineDifference < EXPECTED_LINE_DIFFERENCE || exactCount && lineDifference !== EXPECTED_LINE_DIFFERENCE) {
				let column = node.loc.start.column;
				if (node.loc.start.line !== node.loc.end.line) column = 0;
				context.report({
					loc: {
						line: node.loc.end.line,
						column
					},
					messageId: "newline",
					data: {
						count,
						lineSuffix: count > 1 ? "s" : "",
						type
					},
					fix: exactCount && EXPECTED_LINE_DIFFERENCE < lineDifference ? void 0 : (fixer) => fixer.insertTextAfter(node, "\n".repeat(EXPECTED_LINE_DIFFERENCE - lineDifference))
				});
			}
		}
		function commentAfterImport(node, nextComment, type) {
			const lineDifference = getLineDifference(node, nextComment);
			const EXPECTED_LINE_DIFFERENCE = count + 1;
			if (lineDifference < EXPECTED_LINE_DIFFERENCE) {
				let column = node.loc.start.column;
				if (node.loc.start.line !== node.loc.end.line) column = 0;
				context.report({
					loc: {
						line: node.loc.end.line,
						column
					},
					messageId: "newline",
					data: {
						count,
						lineSuffix: count > 1 ? "s" : "",
						type
					},
					fix: exactCount && EXPECTED_LINE_DIFFERENCE < lineDifference ? void 0 : (fixer) => fixer.insertTextAfter(node, "\n".repeat(EXPECTED_LINE_DIFFERENCE - lineDifference))
				});
			}
		}
		function incrementLevel() {
			level++;
		}
		function decrementLevel() {
			level--;
		}
		function checkImport(node) {
			const { parent } = node;
			if (!parent || !("body" in parent) || !parent.body) return;
			const root = parent;
			const nodePosition = root.body.indexOf(node);
			const nextNode = root.body[nodePosition + 1];
			const endLine = node.loc.end.line;
			let nextComment;
			if (root.comments !== void 0 && considerComments) nextComment = root.comments.find((o) => o.loc.start.line >= endLine && o.loc.start.line <= endLine + count + 1);
			if (node.type === "TSImportEqualsDeclaration" && node.isExport) return;
			if (nextComment) commentAfterImport(node, nextComment, "import");
			else if (nextNode && nextNode.type !== "ImportDeclaration" && (nextNode.type !== "TSImportEqualsDeclaration" || nextNode.isExport)) checkForNewLine(node, nextNode, "import");
		}
		return {
			"ImportDeclaration": checkImport,
			"TSImportEqualsDeclaration": checkImport,
			CallExpression(node) {
				if (isStaticRequire(node) && level === 0) requireCalls.push(node);
			},
			"Program:exit": function(node) {
				const scopeBody = getScopeBody(context.sourceCode.getScope(node));
				for (const [index, node] of requireCalls.entries()) {
					const nodePosition = findNodeIndexInScopeBody(scopeBody, node);
					const statementWithRequireCall = scopeBody[nodePosition];
					const nextStatement = scopeBody[nodePosition + 1];
					const nextRequireCall = requireCalls[index + 1];
					if (nextRequireCall && containsNodeOrEqual(statementWithRequireCall, nextRequireCall)) continue;
					if (nextStatement && (!nextRequireCall || !containsNodeOrEqual(nextStatement, nextRequireCall))) {
						let nextComment;
						if ("comments" in statementWithRequireCall.parent && statementWithRequireCall.parent.comments !== void 0 && considerComments) {
							const endLine = node.loc.end.line;
							nextComment = statementWithRequireCall.parent.comments.find((o) => o.loc.start.line >= endLine && o.loc.start.line <= endLine + count + 1);
						}
						if (nextComment && nextComment !== void 0) commentAfterImport(statementWithRequireCall, nextComment, "require");
						else checkForNewLine(statementWithRequireCall, nextStatement, "require");
					}
				}
			},
			"FunctionDeclaration": incrementLevel,
			"FunctionExpression": incrementLevel,
			"ArrowFunctionExpression": incrementLevel,
			"BlockStatement": incrementLevel,
			"ObjectExpression": incrementLevel,
			"Decorator": incrementLevel,
			"FunctionDeclaration:exit": decrementLevel,
			"FunctionExpression:exit": decrementLevel,
			"ArrowFunctionExpression:exit": decrementLevel,
			"BlockStatement:exit": decrementLevel,
			"ObjectExpression:exit": decrementLevel,
			"Decorator:exit": decrementLevel
		};
	}
});

//#endregion
export { newline_after_import_default as t };