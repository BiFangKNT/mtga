import { n as isPlainObject, t as toMerged } from "./vender.mjs";

//#region src/utils/index.ts
function createRule({ name, create, defaultOptions = [], meta }) {
	return {
		create: ((context) => {
			const optionsCount = Math.max(context.options.length, defaultOptions.length);
			return create(context, Array.from({ length: optionsCount }, (_, i) => {
				if (isPlainObject(context.options[i]) && isPlainObject(defaultOptions[i])) return toMerged(defaultOptions[i], context.options[i]);
				return context.options[i] ?? defaultOptions[i];
			}));
		}),
		defaultOptions,
		meta: {
			...meta,
			docs: {
				...meta.docs,
				url: `https://github.com/9romise/eslint-plugin-import-lite/blob/main/src/rules/${name}/README.md`
			}
		}
	};
}

//#endregion
//#region src/utils/ast.ts
function isCommaToken(token) {
	return token.type === "Punctuator" && token.value === ",";
}
function getValue(node) {
	switch (node.type) {
		case "Identifier": return node.name;
		case "Literal": return node.value;
		default: throw new Error(`Unsupported node type: ${node.type}`);
	}
}

//#endregion
//#region src/utils/compat.ts
function sourceType(context) {
	if ("sourceType" in context.parserOptions) return context.parserOptions.sourceType;
	if ("languageOptions" in context && context.languageOptions) return context.languageOptions.sourceType;
}

//#endregion
//#region src/utils/resolve.ts
function resolve(path) {
	return path;
}

//#endregion
export { createRule as a, isCommaToken as i, sourceType as n, getValue as r, resolve as t };