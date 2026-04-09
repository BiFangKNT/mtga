import { addTemplate, defineNuxtModule, useNitro } from "@nuxt/kit";
import { Buffer } from "node:buffer";
import EventEmitter from "node:events";
import { mkdir, open, readFile, writeFile } from "node:fs/promises";
import { watch } from "chokidar";
import { dirname, join } from "pathe";

//#region package.json
var name = "@dxup/nuxt";

//#endregion
//#region src/event/client.ts
const responseRE = /^```json \{(?<key>.*)\}\n(?<value>[\s\S]*?)\n```$/;
async function createEventClient(nuxt) {
	const path = join(nuxt.options.buildDir, "dxup/events.md");
	await mkdir(dirname(path), { recursive: true });
	await writeFile(path, "");
	const fd = await open(path, "r");
	const watcher = watch(path, { ignoreInitial: true });
	nuxt.hook("close", async () => {
		await fd.close();
		await watcher.close();
	});
	const client = new EventEmitter();
	let offset = 0;
	watcher.on("change", async (path$1, stats) => {
		if (!stats || stats.size <= offset) return;
		const pos = offset;
		offset = stats.size;
		const buffer = Buffer.alloc(offset - pos);
		await fd.read(buffer, 0, buffer.length, pos);
		const match = buffer.toString("utf-8").trim().match(responseRE);
		if (match) {
			const { key, value } = match.groups;
			client.emit(key, JSON.parse(value));
		}
	});
	return client;
}

//#endregion
//#region src/module/events.ts
const uppercaseRE = /[A-Z]/;
async function onComponentsRename(nuxt, { fileName, references }) {
	const component = Object.values(nuxt.apps).flatMap((app) => app.components).find((c) => c.filePath === fileName);
	if (!component) return;
	const tasks = Object.entries(references).map(async ([fileName$1, references$1]) => {
		const code = await readFile(fileName$1, "utf-8");
		const chunks = [];
		let offset = 0;
		for (const { textSpan, lazy } of references$1) {
			const start = textSpan.start;
			const end = start + textSpan.length;
			const oldName = code.slice(start, end);
			const newName = uppercaseRE.test(oldName) ? lazy ? "Lazy" + component.pascalName : component.pascalName : lazy ? "lazy-" + component.kebabName : component.kebabName;
			chunks.push(code.slice(offset, start), newName);
			offset = end;
		}
		chunks.push(code.slice(offset));
		await writeFile(fileName$1, chunks.join(""));
	});
	await Promise.all(tasks);
}

//#endregion
//#region src/module/index.ts
var module_default = defineNuxtModule().with({
	meta: {
		name,
		configKey: "dxup"
	},
	defaults: { features: {
		components: true,
		importGlob: true,
		nitroRoutes: true,
		pageMeta: true,
		runtimeConfig: true,
		typedPages: true,
		unimport: true,
		unofficial: true
	} },
	async setup(options, nuxt) {
		const pluginsTs = [{ name: "@dxup/nuxt" }];
		if (options.features?.unimport) pluginsTs.unshift({ name: "@dxup/unimport" });
		append(pluginsTs, nuxt.options, "typescript", "tsConfig", "compilerOptions");
		append(pluginsTs, nuxt.options.nitro, "typescript", "tsConfig", "compilerOptions");
		append(pluginsTs, nuxt.options, "typescript", "sharedTsConfig", "compilerOptions");
		append(pluginsTs, nuxt.options, "typescript", "nodeTsConfig", "compilerOptions");
		addTemplate({
			filename: "dxup/data.json",
			write: true,
			getContents({ nuxt: nuxt$1, app }) {
				const layouts = Object.fromEntries(Object.values(app.layouts).map((item) => [item.name, item.file]));
				const middleware = app.middleware.reduce((acc, item) => {
					if (!item.global) acc[item.name] = item.path;
					return acc;
				}, {});
				const nitroRoutes = useNitro().scannedHandlers.reduce((acc, item) => {
					if (item.route && item.method) (acc[item.route] ??= {})[item.method] = item.handler;
					return acc;
				}, {});
				const typedPages = app.pages?.reduce(function reducer(acc, page) {
					if (page.name && page.file) acc[page.name] = page.file;
					if (page.children) for (const child of page.children) reducer(acc, child);
					return acc;
				}, {});
				const data = {
					buildDir: nuxt$1.options.buildDir,
					publicDir: nuxt$1.options.dir.public,
					configFiles: [...nuxt$1.options._nuxtConfigFiles, ...nuxt$1.options._layers.map((layer) => layer._configFile).filter(Boolean)],
					layouts,
					middleware,
					nitroRoutes,
					typedPages,
					features: options.features
				};
				return JSON.stringify(data, null, 2);
			}
		});
		if (nuxt.options.dev) (await createEventClient(nuxt)).on("components:rename", (data) => onComponentsRename(nuxt, data));
	}
});
function append(plugins, target, ...keys) {
	for (const key of keys) target = target[key] ??= {};
	(target.plugins ??= []).push(...plugins);
}

//#endregion
export { module_default as default };