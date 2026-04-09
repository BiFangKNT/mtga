import { a as createRule } from "../utils.mjs";

//#region src/rules/no-mutable-exports/no-mutable-exports.ts
var no_mutable_exports_default = createRule({
	name: "no-mutable-exports",
	meta: {
		type: "suggestion",
		docs: { description: "Forbid the use of mutable exports with `var` or `let`." },
		schema: [],
		messages: { noMutable: "Exporting mutable '{{kind}}' binding, use 'const' instead." }
	},
	defaultOptions: [],
	create(context) {
		function checkDeclaration(node) {
			if ("kind" in node && (node.kind === "var" || node.kind === "let")) context.report({
				node,
				messageId: "noMutable",
				data: { kind: node.kind }
			});
		}
		function checkDeclarationsInScope({ variables }, name) {
			for (const variable of variables) if (variable.name === name) {
				for (const def of variable.defs) if (def.type === "Variable" && def.parent) checkDeclaration(def.parent);
			}
		}
		return {
			ExportDefaultDeclaration(node) {
				const scope = context.sourceCode.getScope(node);
				if ("name" in node.declaration) checkDeclarationsInScope(scope, node.declaration.name);
			},
			ExportNamedDeclaration(node) {
				const scope = context.sourceCode.getScope(node);
				if (node.declaration) checkDeclaration(node.declaration);
				else if (!node.source) for (const specifier of node.specifiers) checkDeclarationsInScope(scope, specifier.local.name);
			}
		};
	}
});

//#endregion
export { no_mutable_exports_default as t };