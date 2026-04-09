import crypto from "node:crypto";
import path from "node:path";
import * as babel from "@babel/core";
import { types } from "@babel/core";
import jsx from "@vue/babel-plugin-jsx";
import { createFilter, normalizePath } from "vite";
import { exactRegex, makeIdFiltersToMatchWithQuery } from "@rolldown/pluginutils";

//#region src/index.ts
const ssrRegisterHelperId = "/__vue-jsx-ssr-register-helper";
const ssrRegisterHelperCode = `import { useSSRContext } from "vue"\nexport const ssrRegisterHelper = ${ssrRegisterHelper.toString()}`;
/**
* This function is serialized with toString() and evaluated as a virtual
* module during SSR
*/
function ssrRegisterHelper(comp, filename) {
	const setup = comp.setup;
	comp.setup = (props, ctx) => {
		const ssrContext = useSSRContext();
		(ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add(filename);
		if (setup) return setup(props, ctx);
	};
}
function vueJsxPlugin(options = {}) {
	let root = "";
	let needHmr = false;
	let needSourceMap = true;
	const { include = /\.[jt]sx$/, exclude, babelPlugins = [], defineComponentName = ["defineComponent"], tsPluginOptions = {}, tsTransform, ...babelPluginOptions } = options;
	const filter = createFilter(include, exclude);
	return {
		name: "vite:vue-jsx",
		config(config) {
			const parseDefine = (v) => {
				try {
					return typeof v === "string" ? JSON.parse(v) : v;
				} catch (err) {
					return v;
				}
			};
			const isRolldownVite = this && "rolldownVersion" in this.meta;
			return {
				[isRolldownVite ? "oxc" : "esbuild"]: tsTransform === "built-in" ? { exclude: /\.jsx?$/ } : { include: /\.ts$/ },
				define: {
					__VUE_OPTIONS_API__: parseDefine(config.define?.__VUE_OPTIONS_API__) ?? true,
					__VUE_PROD_DEVTOOLS__: parseDefine(config.define?.__VUE_PROD_DEVTOOLS__) ?? false,
					__VUE_PROD_HYDRATION_MISMATCH_DETAILS__: parseDefine(config.define?.__VUE_PROD_HYDRATION_MISMATCH_DETAILS__) ?? false
				},
				optimizeDeps: isRolldownVite ? { rolldownOptions: { transform: { jsx: "preserve" } } } : {}
			};
		},
		configResolved(config) {
			needHmr = config.command === "serve" && !config.isProduction;
			needSourceMap = config.command === "serve" || !!config.build.sourcemap;
			root = config.root;
		},
		resolveId: {
			filter: { id: exactRegex(ssrRegisterHelperId) },
			handler(id) {
				if (id === ssrRegisterHelperId) return id;
			}
		},
		load: {
			filter: { id: exactRegex(ssrRegisterHelperId) },
			handler(id) {
				if (id === ssrRegisterHelperId) return ssrRegisterHelperCode;
			}
		},
		transform: {
			order: tsTransform === "built-in" ? "pre" : void 0,
			filter: { id: {
				include: include ? makeIdFiltersToMatchWithQuery(include) : void 0,
				exclude: exclude ? makeIdFiltersToMatchWithQuery(exclude) : void 0
			} },
			async handler(code, id, opt) {
				const ssr = opt?.ssr === true;
				const [filepath] = id.split("?");
				if (filter(id) || filter(filepath)) {
					const plugins = [[jsx, babelPluginOptions], ...babelPlugins];
					if (id.endsWith(".tsx") || filepath.endsWith(".tsx")) if (tsTransform === "built-in") plugins.push([await import("@babel/plugin-syntax-typescript").then((r) => r.default), { isTSX: true }]);
					else plugins.push([await import("@babel/plugin-transform-typescript").then((r) => r.default), {
						...tsPluginOptions,
						isTSX: true,
						allowExtensions: true
					}]);
					if (!ssr && !needHmr) plugins.push(() => {
						return { visitor: { CallExpression: { enter(_path) {
							if (isDefineComponentCall(_path.node, defineComponentName)) {
								const callee = _path.node.callee;
								callee.name = `/* @__PURE__ */ ${callee.name}`;
							}
						} } } };
					});
					else plugins.push(() => {
						return { visitor: { ExportDefaultDeclaration: { enter(_path) {
							const unwrappedDeclaration = unwrapTypeAssertion(_path.node.declaration);
							if (isDefineComponentCall(unwrappedDeclaration, defineComponentName)) {
								const declaration = unwrappedDeclaration;
								const nodesPath = _path.replaceWithMultiple([types.variableDeclaration("const", [types.variableDeclarator(types.identifier("__default__"), types.callExpression(declaration.callee, declaration.arguments))]), types.exportDefaultDeclaration(types.identifier("__default__"))]);
								_path.scope.registerDeclaration(nodesPath[0]);
							}
						} } } };
					});
					const result = babel.transformSync(code, {
						babelrc: false,
						ast: true,
						plugins,
						sourceMaps: needSourceMap,
						sourceFileName: id,
						configFile: false
					});
					if (!ssr && !needHmr) {
						if (!result.code) return;
						return {
							code: result.code,
							map: result.map
						};
					}
					const declaredComponents = [];
					const hotComponents = [];
					for (const node of result.ast.program.body) {
						if (node.type === "VariableDeclaration") {
							const names = parseComponentDecls(node, defineComponentName);
							if (names.length) declaredComponents.push(...names);
						}
						if (node.type === "ExportNamedDeclaration") {
							if (node.declaration && node.declaration.type === "VariableDeclaration") hotComponents.push(...parseComponentDecls(node.declaration, defineComponentName).map((name) => ({
								local: name,
								exported: name,
								id: getHash(id + name)
							})));
							else if (node.specifiers.length) {
								for (const spec of node.specifiers) if (spec.type === "ExportSpecifier" && spec.exported.type === "Identifier") {
									if (declaredComponents.find((name) => name === spec.local.name)) hotComponents.push({
										local: spec.local.name,
										exported: spec.exported.name,
										id: getHash(id + spec.exported.name)
									});
								}
							}
						}
						if (node.type === "ExportDefaultDeclaration") {
							if (node.declaration.type === "Identifier") {
								const _name = node.declaration.name;
								if (declaredComponents.find((name) => name === _name)) hotComponents.push({
									local: _name,
									exported: "default",
									id: getHash(id + "default")
								});
							} else if (isDefineComponentCall(unwrapTypeAssertion(node.declaration), defineComponentName)) hotComponents.push({
								local: "__default__",
								exported: "default",
								id: getHash(id + "default")
							});
						}
					}
					if (hotComponents.length) {
						if (needHmr && !ssr && !/\?vue&type=script/.test(id)) {
							let code = result.code;
							let callbackCode = ``;
							for (const { local, exported, id } of hotComponents) {
								code += `\n${local}.__hmrId = "${id}"\n__VUE_HMR_RUNTIME__.createRecord("${id}", ${local})`;
								callbackCode += `\n__VUE_HMR_RUNTIME__.reload("${id}", __${exported})`;
							}
							const newCompNames = hotComponents.map((c) => `${c.exported}: __${c.exported}`).join(",");
							code += `\nimport.meta.hot.accept(({${newCompNames}}) => {${callbackCode}\n})`;
							result.code = code;
						}
						if (ssr) {
							const normalizedId = normalizePath(path.relative(root, id));
							let ssrInjectCode = `\nimport { ssrRegisterHelper } from "${ssrRegisterHelperId}"\nconst __moduleId = ${JSON.stringify(normalizedId)}`;
							for (const { local } of hotComponents) ssrInjectCode += `\nssrRegisterHelper(${local}, __moduleId)`;
							result.code += ssrInjectCode;
						}
					}
					if (!result.code) return;
					return {
						code: result.code,
						map: result.map
					};
				}
			}
		}
	};
}
function parseComponentDecls(node, fnNames) {
	const names = [];
	for (const decl of node.declarations) if (decl.id.type === "Identifier" && isDefineComponentCall(unwrapTypeAssertion(decl.init), fnNames)) names.push(decl.id.name);
	return names;
}
function isDefineComponentCall(node, names) {
	return node && node.type === "CallExpression" && node.callee.type === "Identifier" && names.includes(node.callee.name);
}
function unwrapTypeAssertion(node) {
	if (!node) return node;
	let current = node;
	while (current.type === "TSAsExpression" || current.type === "TSSatisfiesExpression" || current.type === "TSTypeAssertion") current = current.expression;
	return current;
}
function getHash(text) {
	return crypto.hash("sha256", text, "hex").substring(0, 8);
}
var src_default = vueJsxPlugin;
function vueJsxPluginCjs(options) {
	return vueJsxPlugin.call(this, options);
}
Object.assign(vueJsxPluginCjs, { default: vueJsxPluginCjs });

//#endregion
export { src_default as default, vueJsxPluginCjs as "module.exports" };