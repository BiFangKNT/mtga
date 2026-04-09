import { n as BaseComponent, t as publicDirURL } from "../../../public_dir-C5bujZKB.js";
import { r as stripAnsi, t as colors } from "../../../helpers-B9BQYaS6.js";
import { extname } from "node:path";
import { highlightText } from "@speed-highlight/core";
import { highlightText as highlightText$1 } from "@speed-highlight/core/terminal";
const GUTTER = "┃";
const POINTER = "❯";
const LANGS_MAP = {
	".tsx": "ts",
	".jsx": "js",
	".js": "js",
	".ts": "ts",
	".css": "css",
	".json": "json",
	".html": "html",
	".astro": "ts",
	".vue": "ts"
};
var ErrorStackSource = class extends BaseComponent {
	cssFile = new URL("./error_stack_source/style.css", publicDirURL);
	async toHTML(props) {
		const frame = props.frame;
		if (frame.type === "native" || !frame.source || !frame.fileName) return "";
		const language = LANGS_MAP[extname(frame.fileName)] ?? "plain";
		const highlight = `<div class="line-highlight" style="margin-top: ${`${frame.source.findIndex((chunk) => {
			return chunk.lineNumber === frame.lineNumber;
		}) * 24}px`}"></div>`;
		let code = await highlightText(frame.source.map((chunk) => chunk.chunk).join("\n"), language, true);
		code = code.replace("<div class=\"shj-numbers\">", `<div class="shj-numbers" style="counter-set: line ${frame.source[0].lineNumber - 1}">`);
		return `<pre><code class="shj-lang-js">${highlight}${code}</code></pre>`;
	}
	async toANSI(props) {
		const frame = props.frame;
		if (frame.type === "native" || !frame.source || !frame.fileName) return "";
		const language = LANGS_MAP[extname(frame.fileName)] ?? "plain";
		const largestLineNumber = Math.max(...frame.source.map(({ lineNumber }) => lineNumber));
		const lineNumberCols = String(largestLineNumber).length;
		return `\n\n${(await highlightText$1(frame.source.map(({ chunk }) => chunk).join("\n"), language)).split("\n").map((line, index) => {
			const lineNumber = frame.source[index].lineNumber;
			const alignedLineNumber = String(lineNumber).padStart(lineNumberCols, " ");
			if (lineNumber === props.frame.lineNumber) return ` ${colors.bgRed(`${POINTER} ${alignedLineNumber} ${GUTTER}  ${stripAnsi(line)}`)}`;
			return `   ${colors.dim(alignedLineNumber)} ${colors.dim(GUTTER)}  ${line}`;
		}).join("\n")}\n`;
	}
};
export { ErrorStackSource };
