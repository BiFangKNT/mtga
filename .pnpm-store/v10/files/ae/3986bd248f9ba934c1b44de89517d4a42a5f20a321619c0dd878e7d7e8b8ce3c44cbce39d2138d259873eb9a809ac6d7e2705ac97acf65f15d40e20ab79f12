import { a as createRule, r as getValue } from "../utils.mjs";

//#region src/rules/prefer-default-export/prefer-default-export.ts
var prefer_default_export_default = createRule({
	name: "prefer-default-export",
	meta: {
		type: "suggestion",
		docs: { description: "Prefer a default export if module exports a single name or multiple names." },
		schema: [{
			type: "object",
			properties: { target: {
				type: "string",
				enum: ["single", "any"],
				default: "single"
			} },
			additionalProperties: false
		}],
		messages: {
			single: "Prefer default export on a file with single export.",
			any: "Prefer default export to be present on every file that has export."
		}
	},
	defaultOptions: [{ target: "single" }],
	create(context, [options]) {
		let specifierExportCount = 0;
		let hasDefaultExport = false;
		let hasStarExport = false;
		let hasTypeExport = false;
		let namedExportNode;
		const { target } = options;
		function captureDeclaration(identifierOrPattern) {
			if (identifierOrPattern?.type === "ObjectPattern") for (const property of identifierOrPattern.properties) captureDeclaration(property.value);
			else if (identifierOrPattern?.type === "ArrayPattern") for (const el of identifierOrPattern.elements) captureDeclaration(el);
			else specifierExportCount++;
		}
		return {
			ExportDefaultSpecifier() {
				hasDefaultExport = true;
			},
			ExportSpecifier(node) {
				if (getValue(node.exported) === "default") hasDefaultExport = true;
				else {
					specifierExportCount++;
					namedExportNode = node;
				}
			},
			ExportNamedDeclaration(node) {
				if (!node.declaration) return;
				const { type } = node.declaration;
				if (type === "TSTypeAliasDeclaration" || type === "TSInterfaceDeclaration") {
					specifierExportCount++;
					hasTypeExport = true;
					return;
				}
				if ("declarations" in node.declaration && node.declaration.declarations) for (const declaration of node.declaration.declarations) captureDeclaration(declaration.id);
				else specifierExportCount++;
				namedExportNode = node;
			},
			ExportDefaultDeclaration() {
				hasDefaultExport = true;
			},
			ExportAllDeclaration() {
				hasStarExport = true;
			},
			"Program:exit": function() {
				if (hasDefaultExport || hasStarExport || hasTypeExport) return;
				if (target === "single" && specifierExportCount === 1) context.report({
					node: namedExportNode,
					messageId: "single"
				});
				else if (target === "any" && specifierExportCount > 0) context.report({
					node: namedExportNode,
					messageId: "any"
				});
			}
		};
	}
});

//#endregion
export { prefer_default_export_default as t };