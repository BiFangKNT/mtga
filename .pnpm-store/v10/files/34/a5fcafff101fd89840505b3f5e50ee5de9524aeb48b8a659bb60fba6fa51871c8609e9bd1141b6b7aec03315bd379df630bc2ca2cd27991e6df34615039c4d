import { a as createRule, i as isCommaToken, r as getValue } from "../utils.mjs";

//#region src/rules/consistent-type-specifier-style/consistent-type-specifier-style.ts
function getImportText(node, sourceCode, specifiers) {
	const sourceString = sourceCode.getText(node.source);
	if (specifiers.length === 0) return "";
	return `import type {${specifiers.map((s) => {
		const importedName = getValue(s.imported);
		if (importedName === s.local.name) return importedName;
		return `${importedName} as ${s.local.name}`;
	}).join(", ")}} from ${sourceString};`;
}
var consistent_type_specifier_style_default = createRule({
	name: "consistent-type-specifier-style",
	meta: {
		type: "suggestion",
		docs: { description: "Enforce or ban the use of inline type-only markers for named imports." },
		fixable: "code",
		schema: [{
			type: "string",
			enum: [
				"top-level",
				"inline",
				"prefer-top-level"
			],
			default: "top-level"
		}],
		messages: {
			inline: "Prefer using inline {{kind}} specifiers instead of a top-level {{kind}}-only import.",
			topLevel: "Prefer using a top-level {{kind}}-only import instead of inline {{kind}} specifiers."
		}
	},
	defaultOptions: ["top-level"],
	create(context, [options]) {
		const { sourceCode } = context;
		if (options === "inline") return { ImportDeclaration(node) {
			if (node.importKind === "value" || node.importKind == null) return;
			if (node.specifiers.length === 0 || node.specifiers.length === 1 && (node.specifiers[0].type === "ImportDefaultSpecifier" || node.specifiers[0].type === "ImportNamespaceSpecifier")) return;
			context.report({
				node,
				messageId: "inline",
				data: { kind: node.importKind },
				fix(fixer) {
					const kindToken = sourceCode.getFirstToken(node, { skip: 1 });
					return [kindToken ? fixer.remove(kindToken) : [], node.specifiers.map((specifier) => fixer.insertTextBefore(specifier, `${node.importKind} `))].flat();
				}
			});
		} };
		return { ImportDeclaration(node) {
			if (node.importKind === "type" || node.specifiers.length === 0 || node.specifiers.length === 1 && (node.specifiers[0].type === "ImportDefaultSpecifier" || node.specifiers[0].type === "ImportNamespaceSpecifier")) return;
			const typeSpecifiers = [];
			const valueSpecifiers = [];
			let defaultSpecifier = null;
			for (const specifier of node.specifiers) {
				if (specifier.type === "ImportDefaultSpecifier") {
					defaultSpecifier = specifier;
					continue;
				}
				if (!("importKind" in specifier)) continue;
				if (specifier.importKind === "type") typeSpecifiers.push(specifier);
				else if (specifier.importKind === "value" || specifier.importKind == null) valueSpecifiers.push(specifier);
			}
			const typeImport = getImportText(node, sourceCode, typeSpecifiers);
			if (typeSpecifiers.length === node.specifiers.length) context.report({
				node,
				messageId: "topLevel",
				data: { kind: "type" },
				fix(fixer) {
					return fixer.replaceText(node, typeImport);
				}
			});
			else if (options === "top-level") for (const specifier of typeSpecifiers) context.report({
				node: specifier,
				messageId: "topLevel",
				data: { kind: specifier.importKind },
				fix(fixer) {
					const fixes = [];
					if (valueSpecifiers.length > 0) {
						for (const specifier of typeSpecifiers) {
							const token = sourceCode.getTokenAfter(specifier);
							if (token && isCommaToken(token)) fixes.push(fixer.remove(token));
							fixes.push(fixer.remove(specifier));
						}
						const maybeComma = sourceCode.getTokenAfter(valueSpecifiers.at(-1));
						if (isCommaToken(maybeComma)) fixes.push(fixer.remove(maybeComma));
					} else if (defaultSpecifier) {
						const comma = sourceCode.getTokenAfter(defaultSpecifier, isCommaToken);
						const closingBrace = sourceCode.getTokenAfter(node.specifiers.at(-1), (token) => token.type === "Punctuator" && token.value === "}");
						fixes.push(fixer.removeRange([comma.range[0], closingBrace.range[1]]));
					}
					return [...fixes, fixer.insertTextAfter(node, `\n${typeImport}`)];
				}
			});
		} };
	}
});

//#endregion
export { consistent_type_specifier_style_default as t };