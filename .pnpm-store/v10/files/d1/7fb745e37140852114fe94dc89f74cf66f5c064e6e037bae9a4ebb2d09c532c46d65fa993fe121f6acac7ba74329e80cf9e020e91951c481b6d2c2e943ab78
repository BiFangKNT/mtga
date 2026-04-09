import process from "node:process";
import { consola } from "consola";
import { viteNodeFetch, viteNodeOptions } from "#vite-node";
import { ViteNodeRunner } from "vite-node/client";
//#region src/vite-node-runner.ts
const runner = createRunner();
function createRunner() {
	return new ViteNodeRunner({
		root: viteNodeOptions.root,
		base: viteNodeOptions.base,
		resolveId(id, importer) {
			return viteNodeFetch.resolveId(id, importer);
		},
		fetchModule(id) {
			id = id.replace(/\/\//g, "/");
			return viteNodeFetch.fetchModule(id).catch((err) => {
				const errorData = err?.data?.data;
				if (!errorData) throw err;
				let _err;
				try {
					const { message, stack } = formatViteError(errorData, id);
					_err = {
						statusText: "Vite Error",
						message,
						stack
					};
				} catch (formatError) {
					consola.warn("Internal nuxt error while formatting vite-node error. Please report this!", formatError);
					const message = `[vite-node] [TransformError] ${errorData?.message || "-"}`;
					consola.error(message, errorData);
					throw {
						statusText: "Vite Error",
						message,
						stack: `${message}\nat ${id}\n` + (errorData?.stack || "")
					};
				}
				throw _err;
			});
		}
	});
}
function formatViteError(errorData, id) {
	const errorCode = errorData.name || errorData.reasonCode || errorData.code;
	const frame = errorData.frame || errorData.source || errorData.pluginCode;
	const getLocId = (locObj = {}) => locObj.file || locObj.id || locObj.url || id || "";
	const getLocPos = (locObj = {}) => locObj.line ? `${locObj.line}:${locObj.column || 0}` : "";
	const locId = getLocId(errorData.loc) || getLocId(errorData.location) || getLocId(errorData.input) || getLocId(errorData);
	const locPos = getLocPos(errorData.loc) || getLocPos(errorData.location) || getLocPos(errorData.input) || getLocPos(errorData);
	const loc = locId.replace(process.cwd(), ".") + (locPos ? `:${locPos}` : "");
	const message = [
		"[vite-node]",
		errorData.plugin && `[plugin:${errorData.plugin}]`,
		errorCode && `[${errorCode}]`,
		loc,
		errorData.reason && `: ${errorData.reason}`,
		frame && `<br><pre>${frame.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")}</pre><br>`
	].filter(Boolean).join(" ");
	return {
		message,
		stack: [
			message,
			`at ${loc}`,
			errorData.stack
		].filter(Boolean).join("\n")
	};
}
//#endregion
export { runner as default };
