import { performance } from "node:perf_hooks";
import process from "node:process";
import { consola } from "consola";
import { viteNodeFetch, viteNodeOptions } from "#vite-node";
import runner from "#vite-node-runner";
//#region src/vite-node-entry.ts
let render;
var vite_node_entry_default = async (ssrContext) => {
	process.server = true;
	import.meta.server = true;
	const invalidates = await viteNodeFetch.getInvalidates();
	const updates = runner.moduleCache.invalidateDepTree(invalidates);
	const start = performance.now();
	render = updates.has(viteNodeOptions.entryPath) || !render ? (await runner.executeFile(viteNodeOptions.entryPath)).default : render;
	if (updates.size) {
		const time = Math.round((performance.now() - start) * 1e3) / 1e3;
		consola.success(`Vite server hmr ${updates.size} files`, time ? `in ${time}ms` : "");
	}
	return await render(ssrContext);
};
//#endregion
export { vite_node_entry_default as default };
