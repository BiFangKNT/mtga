import { n as BaseComponent, t as publicDirURL } from "../../../public_dir-C5bujZKB.js";
import { i as wordWrap, n as htmlEscape, t as colors } from "../../../helpers-B9BQYaS6.js";
const ERROR_ICON_SVG = `<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" width="24" height="24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 7v6m0 4.01.01-.011M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10Z"/></svg>`;
const HINT_ICON_SVG = `<svg xmlns="http://www.w3.org/2000/svg" aria-hidden="true" width="24" height="24" fill="none"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="m21 2-1 1M3 2l1 1m17 13-1-1M3 16l1-1m5 3h6m-5 3h4M12 3C8 3 5.952 4.95 6 8c.023 1.487.5 2.5 1.5 3.5S9 13 9 15h6c0-2 .5-2.5 1.5-3.5h0c1-1 1.477-2.013 1.5-3.5.048-3.05-2-5-6-5Z"/></svg>`;
const COPY_ICON_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"  stroke-linejoin="round"><path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M7 7m0 2.667a2.667 2.667 0 0 1 2.667 -2.667h8.666a2.667 2.667 0 0 1 2.667 2.667v8.666a2.667 2.667 0 0 1 -2.667 2.667h-8.666a2.667 2.667 0 0 1 -2.667 -2.667z" /><path d="M4.012 16.737a2.005 2.005 0 0 1 -1.012 -1.737v-10c0 -1.1 .9 -2 2 -2h10c.75 0 1.158 .385 1.5 1" /></svg>`;
function buildErrorWithStacktrace(error) {
	const cwd = process.cwd();
	const lines = [];
	lines.push(`${error.name}: ${error.message}`);
	if (error.hint) lines.push(`Hint: ${error.hint.replace(/(<([^>]+)>)/gi, "")}`);
	if (error.frames.length > 0) {
		lines.push("");
		lines.push("Stack trace:");
		for (const frame of error.frames) {
			const fileName = frame.fileName?.replace(`${cwd}/`, "") || "<anonymous>";
			const func = frame.functionName ? `at ${frame.functionName} ` : "at ";
			lines.push(`  ${func}(${fileName}:${frame.lineNumber}:${frame.columnNumber})`);
		}
	}
	return lines.join("\n");
}
function htmlAttributeEscape(value) {
	return value.replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/'/g, "&#x27;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
var ErrorInfo = class extends BaseComponent {
	cssFile = new URL("./error_info/style.css", publicDirURL);
	scriptFile = new URL("./error_info/script.js", publicDirURL);
	async toHTML(props) {
		const stacktraceText = buildErrorWithStacktrace(props.error);
		return `<section>
      <h4 id="error-name">${htmlEscape(props.error.name)}</h4>
      <h1 id="error-title">${htmlEscape(props.title)}</h1>
    </section>
    <section>
      <div class="card">
        <div class="card-body">
          <h2 id="error-message">
            <span>${ERROR_ICON_SVG}</span>
            <span>${htmlEscape(props.error.message)}</span>
            <button
              id="copy-error-btn"
              data-error-text="${htmlAttributeEscape(stacktraceText)}"
              onclick="copyErrorMessage(this)"
              title="Copy error with stack trace"
              aria-label="Copy error with stack trace to clipboard"
            >
              ${COPY_ICON_SVG}
            </button>
          </h2>
          ${props.error.hint ? `<div id="error-hint">
                <span>${HINT_ICON_SVG}</span>
                <span>${props.error.hint}</span>
              </div>` : ""}
        </div>
      </div>
    </section>`;
	}
	async toANSI(props) {
		return `${colors.red(`ℹ ${wordWrap(`${props.error.name}: ${props.error.message}`, {
			width: process.stdout.columns,
			indent: "  ",
			newLine: "\n",
			escape: (value) => value
		})}`)}${props.error.hint ? `\n\n${colors.blue("◉")} ${colors.dim().italic(wordWrap(props.error.hint.replace(/(<([^>]+)>)/gi, ""), {
			width: process.stdout.columns,
			indent: "  ",
			newLine: "\n",
			escape: (value) => value
		}))}` : ""}`;
	}
};
export { ErrorInfo };
