import { a as createRule } from "../utils.mjs";

//#region src/rules/exports-last/exports-last.ts
function isNonExportStatement({ type }) {
	return type !== "ExportDefaultDeclaration" && type !== "ExportNamedDeclaration" && type !== "ExportAllDeclaration";
}
var exports_last_default = createRule({
	name: "exports-last",
	meta: {
		type: "suggestion",
		docs: { description: "Ensure all exports appear after other statements." },
		schema: [],
		messages: { end: "Export statements should appear at the end of the file" }
	},
	defaultOptions: [],
	create(context) {
		return { Program({ body }) {
			const lastNonExportStatementIndex = body.findLastIndex(isNonExportStatement);
			if (lastNonExportStatementIndex !== -1) {
				for (const node of body.slice(0, lastNonExportStatementIndex)) if (!isNonExportStatement(node)) context.report({
					node,
					messageId: "end"
				});
			}
		} };
	}
});

//#endregion
export { exports_last_default as t };