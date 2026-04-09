import { a as createRule } from "../utils.mjs";

//#region src/rules/first/first.ts
function getImportValue(node) {
	return node.type === "ImportDeclaration" ? node.source.value : "moduleReference" in node && "expression" in node.moduleReference && "value" in node.moduleReference.expression && node.moduleReference.expression.value;
}
function isPossibleDirective(node) {
	return node.type === "ExpressionStatement" && node.expression.type === "Literal" && typeof node.expression.value === "string";
}
var first_default = createRule({
	name: "first",
	meta: {
		type: "suggestion",
		docs: { description: "Ensure all imports appear before other statements." },
		fixable: "code",
		schema: [{
			type: "string",
			enum: ["absolute-first", "disable-absolute-first"]
		}],
		messages: {
			absolute: "Absolute imports should come before relative imports.",
			order: "Import in body of module; reorder to top."
		}
	},
	defaultOptions: [],
	create(context, options) {
		return { Program(n) {
			const body = n.body;
			if (!body?.length) return;
			const absoluteFirst = options[0] === "absolute-first";
			const { sourceCode } = context;
			const originSourceCode = sourceCode.getText();
			let nonImportCount = 0;
			let anyExpressions = false;
			let anyRelative = false;
			let lastLegalImp = null;
			const errorInfos = [];
			let shouldSort = true;
			let lastSortNodesIndex = 0;
			for (const [index, node] of body.entries()) {
				if (!anyExpressions && isPossibleDirective(node)) continue;
				anyExpressions = true;
				if (node.type === "ImportDeclaration" || node.type === "TSImportEqualsDeclaration") {
					if (absoluteFirst) {
						const importValue = getImportValue(node);
						if (typeof importValue === "string" && /^\./.test(importValue)) anyRelative = true;
						else if (anyRelative) context.report({
							node: node.type === "ImportDeclaration" ? node.source : node.moduleReference,
							messageId: "absolute"
						});
					}
					if (nonImportCount > 0) {
						/** @see https://eslint.org/docs/next/use/migrate-to-9.0.0#-removed-multiple-context-methods */
						for (const variable of sourceCode.getDeclaredVariables(node)) {
							if (!shouldSort) break;
							for (const reference of variable.references) if (reference.identifier.range[0] < node.range[1]) {
								shouldSort = false;
								break;
							}
						}
						if (shouldSort) lastSortNodesIndex = errorInfos.length;
						errorInfos.push({
							node,
							range: [body[index - 1].range[1], node.range[1]]
						});
					} else lastLegalImp = node;
				} else nonImportCount++;
			}
			if (errorInfos.length === 0) return;
			for (const [index, { node }] of errorInfos.entries()) {
				let fix;
				if (index < lastSortNodesIndex) fix = (fixer) => fixer.insertTextAfter(node, "");
				else if (index === lastSortNodesIndex) {
					const sortNodes = errorInfos.slice(0, lastSortNodesIndex + 1);
					fix = (fixer) => {
						const removeFixers = sortNodes.map(({ range }) => fixer.removeRange(range));
						const range = [0, removeFixers.at(-1).range[1]];
						let insertSourceCode = sortNodes.map(({ range }) => {
							const nodeSourceCode = originSourceCode.slice(...range);
							if (/\S/.test(nodeSourceCode[0])) return `\n${nodeSourceCode}`;
							return nodeSourceCode;
						}).join("");
						let replaceSourceCode = "";
						if (!lastLegalImp) insertSourceCode = insertSourceCode.trim() + insertSourceCode.match(/^(\s+)/)[0];
						const fixers = [lastLegalImp ? fixer.insertTextAfter(lastLegalImp, insertSourceCode) : fixer.insertTextBefore(body[0], insertSourceCode), ...removeFixers];
						for (const [i, computedFixer] of fixers.entries()) replaceSourceCode += originSourceCode.slice(fixers[i - 1] ? fixers[i - 1].range[1] : 0, computedFixer.range[0]) + computedFixer.text;
						return fixer.replaceTextRange(range, replaceSourceCode);
					};
				}
				context.report({
					node,
					messageId: "order",
					fix
				});
			}
		} };
	}
});

//#endregion
export { first_default as t };