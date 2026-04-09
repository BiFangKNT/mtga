//#region src/cli/_utils.ts
const noColor = /* @__PURE__ */ (() => {
	const env = globalThis.process?.env ?? {};
	return env.NO_COLOR === "1" || env.TERM === "dumb";
})();
const _c = (c, r = 39) => (t) => noColor ? t : `\u001B[${c}m${t}\u001B[${r}m`;
const bold = /* @__PURE__ */ _c(1, 22);
const red = /* @__PURE__ */ _c(31);
const green = /* @__PURE__ */ _c(32);
const yellow = /* @__PURE__ */ _c(33);
const blue = /* @__PURE__ */ _c(34);
const magenta = /* @__PURE__ */ _c(35);
const cyan = /* @__PURE__ */ _c(36);
const gray = /* @__PURE__ */ _c(90);
const url = (title, url) => noColor ? `[${title}](${url})` : `\u001B]8;;${url}\u001B\\${title}\u001B]8;;\u001B\\`;
//#endregion
export { green as a, url as c, gray as i, yellow as l, bold as n, magenta as o, cyan as r, red as s, blue as t };
