//#region rolldown:runtime
var __defProp = Object.defineProperty;
var __export = (all, symbols) => {
	let target = {};
	for (var name in all) {
		__defProp(target, name, {
			get: all[name],
			enumerable: true
		});
	}
	if (symbols) {
		__defProp(target, Symbol.toStringTag, { value: "Module" });
	}
	return target;
};

//#endregion
let node_fs_promises = require("node:fs/promises");
let pathe = require("pathe");
let tinyglobby = require("tinyglobby");

//#region src/event/server.ts
function createEventServer(info) {
	const path = (0, pathe.join)(info.project.getCurrentDirectory(), "dxup/events.md");
	async function write(key, data) {
		try {
			await (0, node_fs_promises.appendFile)(path, `\`\`\`json {${key}}\n${JSON.stringify(data, null, 2)}\n\`\`\`\n`);
		} catch {}
	}
	return { write };
}

//#endregion
//#region src/typescript/data.ts
const initialValue = {
	buildDir: "",
	publicDir: "",
	configFiles: [],
	layouts: {},
	middleware: {},
	nitroRoutes: {},
	typedPages: {},
	features: {
		components: true,
		importGlob: true,
		nitroRoutes: true,
		pageMeta: true,
		runtimeConfig: true,
		typedPages: true,
		unofficial: true
	}
};
const callbacks = {};
function createData(ts, info) {
	const path = (0, pathe.join)(info.languageServiceHost.getCurrentDirectory(), "dxup/data.json");
	const data = {};
	const updates = callbacks[path] ??= (ts.sys.watchFile?.(path, () => {
		const text$1 = ts.sys.readFile(path);
		for (const update of updates) update(text$1);
	}), []);
	updates.push((text$1) => {
		Object.assign(data, {
			...initialValue,
			...text$1 ? JSON.parse(text$1) : {}
		});
	});
	const text = ts.sys.readFile(path);
	updates.at(-1)(text);
	return data;
}

//#endregion
//#region src/typescript/utils.ts
function createModuleDefinition(ts, path) {
	return {
		fileName: path,
		textSpan: {
			start: 0,
			length: 0
		},
		kind: ts.ScriptElementKind.moduleElement,
		name: `"${path}"`,
		containerKind: ts.ScriptElementKind.unknown,
		containerName: ""
	};
}
function isVueVirtualCode(code) {
	return code?.languageId === "vue";
}
function withVirtualOffset(language, sourceScript, position, method) {
	const serviceScript = sourceScript.generated.languagePlugin.typescript?.getServiceScript(sourceScript.generated.root);
	if (!serviceScript) return;
	const map = language.maps.get(serviceScript.code, sourceScript);
	const leadingOffset = sourceScript.snapshot.getLength();
	const offset = 1145141919810;
	const mapping = {
		sourceOffsets: [offset],
		generatedOffsets: [position - leadingOffset],
		lengths: [0],
		data: {
			completion: true,
			navigation: true,
			semantic: true,
			verification: true
		}
	};
	const original = map.toGeneratedLocation;
	map.toGeneratedLocation = function* (sourceOffset, ...args) {
		if (sourceOffset === offset) yield [mapping.generatedOffsets[0], mapping];
		yield* original.call(this, sourceOffset, ...args);
	};
	try {
		return method(offset);
	} finally {
		map.toGeneratedLocation = original;
	}
}

//#endregion
//#region src/typescript/features/findReferences.ts
var findReferences_exports = /* @__PURE__ */ __export({ postprocess: () => postprocess$1 });
function postprocess$1(context, language, findReferences) {
	const { ts, info } = context;
	return (...args) => {
		const result = findReferences(...args);
		if (!result?.length) {
			const sourceScript = language.scripts.get(args[0].replaceAll("\\", "/"));
			const root = sourceScript?.generated?.root;
			if (!isVueVirtualCode(root)) return;
			const start = (root.sfc.template?.start ?? Infinity) + 1;
			if (args[1] < start || args[1] > start + 8) return;
			const sourceFile = info.languageService.getProgram().getSourceFile(args[0]);
			if (!sourceFile) return;
			for (const statement of sourceFile.statements) if (ts.isExportAssignment(statement)) return withVirtualOffset(language, sourceScript, statement.getChildAt(1).getStart(sourceFile), (position) => findReferences(args[0], position));
			return;
		}
		return result;
	};
}

//#endregion
//#region src/typescript/features/findRenameLocations.ts
var findRenameLocations_exports = /* @__PURE__ */ __export({ preprocess: () => preprocess$2 });
function preprocess$2(context, findRenameLocations) {
	const { data } = context;
	return (...args) => {
		return findRenameLocations(...args)?.filter((edit) => {
			return !edit.fileName.startsWith(data.buildDir);
		});
	};
}

//#endregion
//#region ../shared/src/index.ts
function* forEachTouchingNode(ts, sourceFile, position) {
	yield* binaryVisit(ts, sourceFile, sourceFile, position);
}
function* binaryVisit(ts, sourceFile, node, position) {
	const nodes = [];
	ts.forEachChild(node, (child) => {
		nodes.push(child);
	});
	let left = 0;
	let right = nodes.length - 1;
	while (left <= right) {
		const mid = Math.floor((left + right) / 2);
		const node$1 = nodes[mid];
		if (position > node$1.getEnd()) left = mid + 1;
		else if (position < node$1.getStart(sourceFile)) right = mid - 1;
		else {
			yield node$1;
			yield* binaryVisit(ts, sourceFile, node$1, position);
			return;
		}
	}
}
function isTextSpanWithin(node, textSpan, sourceFile) {
	return textSpan.start + textSpan.length <= node.getEnd() && textSpan.start >= node.getStart(sourceFile);
}

//#endregion
//#region src/typescript/features/getDefinitionAndBoundSpan.ts
var getDefinitionAndBoundSpan_exports = /* @__PURE__ */ __export({
	postprocess: () => postprocess,
	preprocess: () => preprocess$1
});
const fetchFunctions = new Set([
	"$fetch",
	"useFetch",
	"useLazyFetch"
]);
const pageMetaKeys = new Set(["layout", "middleware"]);
function postprocess(context, language, getDefinitionAndBoundSpan) {
	const { ts } = context;
	return (...args) => {
		const result = getDefinitionAndBoundSpan(...args);
		if (!result?.definitions?.length) {
			const root = language.scripts.get(args[0].replaceAll("\\", "/"))?.generated?.root;
			if (!isVueVirtualCode(root)) return result;
			const textSpan = {
				start: (root.sfc.template?.start ?? Infinity) + 1,
				length: 8
			};
			if (args[1] >= textSpan.start && args[1] <= textSpan.start + textSpan.length) return {
				textSpan,
				definitions: [{
					fileName: args[0],
					textSpan,
					kind: ts.ScriptElementKind.memberVariableElement,
					name: "default",
					containerKind: ts.ScriptElementKind.unknown,
					containerName: args[0]
				}]
			};
			return result;
		}
		return result;
	};
}
function preprocess$1(context, getDefinitionAndBoundSpan) {
	const { ts, info, data } = context;
	return (...args) => {
		const result = getDefinitionAndBoundSpan(...args);
		if (!result) {
			const program$1 = info.languageService.getProgram();
			const sourceFile = program$1.getSourceFile(args[0]);
			if (!sourceFile) return;
			const checker = program$1.getTypeChecker();
			let result$1;
			for (const node of forEachTouchingNode(ts, sourceFile, args[1])) {
				if (data.features.importGlob) result$1 ??= visitImportGlob(ts, info, sourceFile, node, args[1]);
				if (data.features.nitroRoutes) result$1 ??= visitNitroRoutes(ts, data, checker, sourceFile, node, args[1]);
				if (data.features.pageMeta) result$1 ??= visitPageMeta(ts, data, sourceFile, node, args[1]);
				if (data.features.typedPages) result$1 ??= visitTypedPages(ts, data, checker, sourceFile, node, args[1]);
			}
			if (result$1) return result$1;
		}
		if (!result?.definitions?.length) return result;
		const program = info.languageService.getProgram();
		const definitions = new Set(result.definitions);
		for (const definition of result.definitions) {
			const sourceFile = program.getSourceFile(definition.fileName);
			if (!sourceFile) continue;
			let result$1;
			if (data.features.runtimeConfig && definition.fileName.endsWith("runtime-config.d.ts")) result$1 = visitRuntimeConfig(context, sourceFile, definition);
			if (result$1?.length) {
				for (const definition$1 of result$1) definitions.add(definition$1);
				definitions.delete(definition);
			}
		}
		return {
			definitions: [...definitions],
			textSpan: result.textSpan
		};
	};
}
function visitImportGlob(ts, info, sourceFile, node, position) {
	if (!ts.isCallExpression(node) || !node.arguments.length) return;
	const firstArg = node.arguments[0];
	const start = firstArg.getStart(sourceFile);
	const end = firstArg.getEnd();
	if (position < start || position > end) return;
	let pattern;
	const callText = node.expression.getText(sourceFile);
	if (callText === "import" && ts.isTemplateExpression(firstArg)) pattern = [firstArg.head.text, ...firstArg.templateSpans.map((span) => span.literal.text)].join("*");
	else if (callText === "import.meta.glob" && ts.isStringLiteral(firstArg)) pattern = firstArg.text;
	if (pattern === void 0) return;
	const resolved = ts.resolveModuleName(pattern, sourceFile.fileName, info.languageServiceHost.getCompilationSettings(), {
		fileExists: () => true,
		readFile: () => ""
	});
	if (!resolved?.resolvedModule) return;
	const extension = (0, pathe.extname)(pattern);
	const arbitrary = `.d${extension}.ts`;
	pattern = resolved.resolvedModule.resolvedFileName;
	if (resolved.resolvedModule.extension === arbitrary) pattern = pattern.slice(0, -arbitrary.length) + extension;
	const fileNames = (0, tinyglobby.globSync)(pattern, { absolute: true });
	return {
		textSpan: {
			start,
			length: end - start
		},
		definitions: fileNames.map((fileName) => createModuleDefinition(ts, fileName))
	};
}
function visitNitroRoutes(ts, data, checker, sourceFile, node, position) {
	if (!ts.isCallExpression(node) || !ts.isIdentifier(node.expression) || !fetchFunctions.has(node.expression.text) || !node.arguments.length || !ts.isStringLiteralLike(node.arguments[0])) return;
	const firstArg = node.arguments[0];
	const start = firstArg.getStart(sourceFile);
	const end = firstArg.getEnd();
	if (position < start || position > end) return;
	const resolvedSignature = checker.getResolvedSignature(node);
	if (!resolvedSignature) return;
	const typeArguments = checker.getTypeArgumentsForResolvedSignature(resolvedSignature);
	let routeType;
	let methodType;
	if (node.expression.text === "$fetch") {
		routeType = typeArguments?.[1];
		const symbol = typeArguments?.[2].getProperty("method");
		methodType = symbol ? checker.getTypeOfSymbol(symbol) : void 0;
	} else {
		routeType = typeArguments?.[2];
		methodType = typeArguments?.[3];
	}
	const paths = [];
	if (routeType?.isStringLiteral()) {
		const alternatives = data.nitroRoutes[routeType.value] ?? {};
		const methods = [];
		for (const type of methodType?.isUnion() ? methodType.types : [methodType]) if (type?.isStringLiteral()) methods.push(type.value);
		for (const method of methods.length ? methods : Object.keys(alternatives)) {
			const path = alternatives[method];
			if (path !== void 0) paths.push(path);
		}
	}
	if (!paths.length && firstArg.text.startsWith("/")) {
		const fallback = (0, pathe.join)(data.publicDir, firstArg.text);
		if (ts.sys.fileExists(fallback)) paths.push(fallback);
	}
	return {
		textSpan: {
			start,
			length: end - start
		},
		definitions: paths.map((path) => createModuleDefinition(ts, path))
	};
}
function visitPageMeta(ts, data, sourceFile, node, position) {
	if (!ts.isPropertyAssignment(node) || !ts.isIdentifier(node.name) || !pageMetaKeys.has(node.name.text) || !ts.isCallExpression(node.parent.parent) || !ts.isIdentifier(node.parent.parent.expression) || node.parent.parent.expression.text !== "definePageMeta") return;
	switch (node.name.text) {
		case "layout": {
			if (!ts.isStringLiteralLike(node.initializer)) return;
			const start = node.initializer.getStart(sourceFile);
			const end = node.initializer.getEnd();
			if (position < start || position > end) return;
			const path = data.layouts[node.initializer.text];
			if (path === void 0) return;
			return {
				textSpan: {
					start,
					length: end - start
				},
				definitions: [createModuleDefinition(ts, path)]
			};
		}
		case "middleware": {
			const literals = ts.isStringLiteralLike(node.initializer) ? [node.initializer] : ts.isArrayLiteralExpression(node.initializer) ? node.initializer.elements.filter(ts.isStringLiteralLike) : [];
			for (const literal of literals) {
				const start = literal.getStart(sourceFile);
				const end = literal.getEnd();
				if (position < start || position > end) continue;
				const path = data.middleware[literal.text];
				if (path === void 0) continue;
				return {
					textSpan: {
						start,
						length: end - start
					},
					definitions: [createModuleDefinition(ts, path)]
				};
			}
			break;
		}
	}
}
function visitTypedPages(ts, data, checker, sourceFile, node, position) {
	if (!ts.isPropertyAssignment(node) || !ts.isIdentifier(node.name) || node.name.text !== "name" || !ts.isStringLiteralLike(node.initializer)) return;
	const start = node.initializer.getStart(sourceFile);
	const end = node.initializer.getEnd();
	if (position < start || position > end) return;
	const contextualType = checker.getContextualType(node.parent)?.getNonNullableType();
	if (contextualType?.aliasSymbol?.name !== "RouteLocationRaw" && (!contextualType?.isUnion() || contextualType.types.every((type) => type.symbol?.name !== "RouteLocationAsPathTyped"))) return;
	const path = data.typedPages[node.initializer.text];
	if (path === void 0) return;
	return {
		textSpan: {
			start,
			length: end - start
		},
		definitions: [createModuleDefinition(ts, path)]
	};
}
function visitRuntimeConfig(context, sourceFile, definition) {
	const { ts } = context;
	let definitions = [];
	const path = [];
	for (const node of forEachTouchingNode(ts, sourceFile, definition.textSpan.start)) {
		let key;
		if (ts.isInterfaceDeclaration(node) && ts.isIdentifier(node.name)) key = node.name.text;
		else if (ts.isPropertySignature(node) && ts.isIdentifier(node.name)) {
			key = node.name.text;
			if (isTextSpanWithin(node.name, definition.textSpan, sourceFile)) {
				path.push(key);
				definitions = [...forwardRuntimeConfig(context, definition, path)];
				break;
			}
		}
		if (key !== void 0) path.push(key);
	}
	return definitions;
}
function* forwardRuntimeConfig(context, definition, path) {
	const { ts, info, data } = context;
	switch (path[0]) {
		case "SharedRuntimeConfig":
			path.shift();
			break;
		case "SharedPublicRuntimeConfig":
			path[0] = "public";
			break;
		default: return;
	}
	const configFile = data.configFiles[0];
	if (configFile === void 0) return;
	const { configFileName } = info.project.projectService.openClientFile(configFile);
	if (configFileName === void 0) return;
	const nodeProject = info.project.projectService.findProject(configFileName);
	if (!nodeProject) return;
	const nodeProgram = nodeProject.getLanguageService().getProgram();
	if (!nodeProgram) return;
	const checker = nodeProgram.getTypeChecker();
	for (const configFile$1 of data.configFiles) {
		const sourceFile = nodeProgram.getSourceFile(configFile$1);
		if (!sourceFile) continue;
		outer: for (const node of sourceFile.statements) {
			if (!ts.isExportAssignment(node) || !ts.isCallExpression(node.expression) || !node.expression.arguments.length) continue;
			const arg = node.expression.arguments[0];
			let currentSymbol;
			let currentType = checker.getTypeAtLocation(arg);
			for (const key of ["runtimeConfig", ...path]) {
				const symbol = currentType.getProperties().find((s) => s.name === key);
				if (!symbol) break outer;
				currentSymbol = symbol;
				currentType = checker.getTypeOfSymbol(symbol);
			}
			for (const decl of currentSymbol?.declarations ?? []) {
				const sourceFile$1 = decl.getSourceFile();
				const contextSpan = {
					start: decl.getStart(sourceFile$1),
					length: decl.getWidth(sourceFile$1)
				};
				let textSpan = contextSpan;
				if (ts.isPropertyAssignment(decl) || ts.isPropertySignature(decl)) textSpan = {
					start: decl.name.getStart(sourceFile$1),
					length: decl.name.getWidth(sourceFile$1)
				};
				yield {
					...definition,
					fileName: sourceFile$1.fileName,
					textSpan,
					contextSpan
				};
			}
		}
	}
}

//#endregion
//#region src/typescript/features/getEditsForFileRename.ts
var getEditsForFileRename_exports = /* @__PURE__ */ __export({ preprocess: () => preprocess });
function preprocess(context, getEditsForFileRename) {
	const { ts, info, data, server } = context;
	return (...args) => {
		const result = getEditsForFileRename(...args);
		if (!result?.length) return result;
		if (data.features.components) {
			const languageService = info.project.getLanguageService();
			const program = languageService.getProgram();
			const references = {};
			for (const { fileName, textChanges } of result) {
				if (!fileName.endsWith("components.d.ts")) continue;
				const sourceFile = program.getSourceFile(fileName);
				if (!sourceFile) continue;
				for (const { span } of textChanges) for (const node of forEachTouchingNode(ts, sourceFile, span.start)) {
					if (!ts.isPropertySignature(node) && !ts.isVariableDeclaration(node)) continue;
					const position = node.name.getStart(sourceFile);
					const res = languageService.getReferencesAtPosition(fileName, position)?.filter((entry) => !entry.fileName.startsWith(data.buildDir))?.sort((a, b) => a.textSpan.start - b.textSpan.start);
					const lazy = node.type && ts.isTypeReferenceNode(node.type) && ts.isIdentifier(node.type.typeName) && node.type.typeName.text === "LazyComponent";
					for (const { fileName: fileName$1, textSpan } of res ?? []) (references[fileName$1] ??= []).push({
						textSpan,
						lazy: lazy || void 0
					});
					break;
				}
			}
			if (Object.keys(references).length) server.write("components:rename", {
				fileName: args[1],
				references
			});
		}
		return result.filter((change) => {
			return !change.fileName.startsWith(data.buildDir);
		});
	};
}

//#endregion
//#region src/typescript/index.ts
const plugin = (module$1) => {
	const { typescript: ts } = module$1;
	return { create(info) {
		const data = createData(ts, info);
		const context = {
			ts,
			info,
			data,
			server: createEventServer(info)
		};
		queueMicrotask(() => {
			context.language = info.project.__vue__?.language;
			if (!context.language || !data.features.unofficial) return;
			const languageService = info.project.getLanguageService();
			const methods = {};
			for (const [key, method] of [["findReferences", findReferences_exports], ["getDefinitionAndBoundSpan", getDefinitionAndBoundSpan_exports]]) {
				const original = languageService[key];
				methods[key] = method.postprocess(context, context.language, original);
			}
			info.project["languageService"] = new Proxy(languageService, {
				get(target, p, receiver) {
					return methods[p] ?? Reflect.get(target, p, receiver);
				},
				set(...args) {
					return Reflect.set(...args);
				}
			});
		});
		for (const [key, method] of [
			["findRenameLocations", findRenameLocations_exports],
			["getDefinitionAndBoundSpan", getDefinitionAndBoundSpan_exports],
			["getEditsForFileRename", getEditsForFileRename_exports]
		]) {
			const original = info.languageService[key];
			info.languageService[key] = method.preprocess(context, original);
		}
		return info.languageService;
	} };
};
var typescript_default = plugin;

//#endregion
module.exports = typescript_default;