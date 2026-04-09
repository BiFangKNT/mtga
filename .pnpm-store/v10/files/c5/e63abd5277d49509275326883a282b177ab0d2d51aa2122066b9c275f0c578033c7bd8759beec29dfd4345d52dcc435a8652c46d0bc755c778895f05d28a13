import { n as BaseComponent, t as publicDirURL } from "../../../public_dir-C5bujZKB.js";
import { n as htmlEscape, t as colors } from "../../../helpers-B9BQYaS6.js";
import { dump, themes } from "@poppinss/dumper/html";
import { dump as dump$1 } from "@poppinss/dumper/console";
const CHEVIRON = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" width="24" height="24" stroke-width="2">
  <path d="M6 9l6 6l6 -6"></path>
</svg>`;
const EDITORS = {
	textmate: "txmt://open?url=file://%f&line=%l",
	macvim: "mvim://open?url=file://%f&line=%l",
	emacs: "emacs://open?url=file://%f&line=%l",
	sublime: "subl://open?url=file://%f&line=%l",
	phpstorm: "phpstorm://open?file=%f&line=%l",
	atom: "atom://core/open/file?filename=%f&line=%l",
	vscode: "vscode://file/%f:%l"
};
var ErrorStack = class extends BaseComponent {
	cssFile = new URL("./error_stack/style.css", publicDirURL);
	scriptFile = new URL("./error_stack/script.js", publicDirURL);
	#getRelativeFileName(filePath) {
		return filePath.replace(`${process.cwd()}/`, "");
	}
	#getFirstExpandedFrameIndex(frames) {
		let expandAtIndex = frames.findIndex((frame) => frame.type === "app");
		if (expandAtIndex === -1) expandAtIndex = frames.findIndex((frame) => frame.type === "module");
		return expandAtIndex;
	}
	#getEditorLink(ide, frame) {
		const editorURL = EDITORS[ide] || ide;
		if (!editorURL || frame.type === "native") return { text: this.#getRelativeFileName(frame.fileName) };
		return {
			href: editorURL.replace("%f", frame.fileName).replace("%l", String(frame.lineNumber)),
			text: this.#getRelativeFileName(frame.fileName)
		};
	}
	#renderFrameLocation(frame, ide) {
		const { text, href } = this.#getEditorLink(ide, frame);
		const fileName = `<a${href ? ` href="${href}"` : ""} class="stack-frame-filepath" title="${text}">
      ${htmlEscape(text)}
    </a>`;
		const functionName = frame.functionName ? `<span>in <code title="${frame.functionName}">
        ${htmlEscape(frame.functionName)}
      </code></span>` : "";
		const loc = `<span>at line <code>${frame.lineNumber}:${frame.columnNumber}</code></span>`;
		if (frame.type !== "native" && frame.source) return `<button class="stack-frame-location">
        ${fileName} ${functionName} ${loc}
      </button>`;
		return `<div class="stack-frame-location">
      ${fileName} ${functionName} ${loc}
    </div>`;
	}
	async #renderStackFrame(frame, index, expandAtIndex, props) {
		const label = frame.type === "app" ? "<span class=\"frame-label\">In App</span>" : "";
		const expandedClass = expandAtIndex === index ? " expanded" : "";
		const toggleButton = frame.type !== "native" && frame.source ? `<button class="stack-frame-toggle-indicator">${CHEVIRON}</button>` : "";
		return `<li class="stack-frame stack-frame-${frame.type}${expandedClass}">
      <div class="stack-frame-contents">
        ${this.#renderFrameLocation(frame, props.ide)}
        <div class="stack-frame-extras">
          ${label}
          ${toggleButton}
        </div>
      </div>
      <div class="stack-frame-source">
        ${await props.sourceCodeRenderer(props.error, frame)}
      </div>
    </li>`;
	}
	async #printStackFrame(frame, index, expandAtIndex, props) {
		const loc = `${this.#getRelativeFileName(frame.fileName)}:${frame.lineNumber}:${frame.columnNumber}`;
		if (index === expandAtIndex) {
			const functionName = frame.functionName ? `at ${frame.functionName} ` : "";
			const codeSnippet = await props.sourceCodeRenderer(props.error, frame);
			return ` ⁃ ${functionName}${colors.yellow(`(${loc})`)}${codeSnippet}`;
		}
		if (frame.type === "native") {
			const functionName = frame.functionName ? `at ${colors.italic(frame.functionName)} ` : "";
			return colors.dim(` ⁃ ${functionName}(${colors.italic(loc)})`);
		}
		return ` ⁃ ${frame.functionName ? `at ${frame.functionName} ` : ""}${colors.yellow(`(${loc})`)}`;
	}
	async toHTML(props) {
		return `<section>
      <div class="card">
        <div class="card-heading">
          <div>
            <h3 class="card-title">
              Stack Trace
            </h3>
          </div>
        </div>
        <div class="card-body">
          <div id="stack-frames-wrapper">
            <div id="stack-frames-header">
              <div id="all-frames-toggle-wrapper">
                <label id="all-frames-toggle">
                  <input type="checkbox" />
                  <span> View All Frames </span>
                </label>
              </div>

              <div>
                <div class="toggle-switch">
                  <button id="formatted-frames-toggle" class="active"> Pretty </button>
                  <button id="raw-frames-toggle"> Raw </button>
                </div>
              </div>
            </div>

            <div id="stack-frames-body">
              <div id="stack-frames-formatted" class="visible">
                <ul id="stack-frames">
                  ${(await Promise.all(props.error.frames.map((frame, index) => {
			return this.#renderStackFrame(frame, index, this.#getFirstExpandedFrameIndex(props.error.frames), props);
		}))).join("\n")}
                </ul>
              </div>
              <div id="stack-frames-raw">
                ${dump(props.error.raw, {
			styles: themes.cssVariables,
			expand: true,
			cspNonce: props.cspNonce,
			inspectObjectPrototype: false,
			inspectStaticMembers: false,
			inspectArrayPrototype: false
		})}
              </div>
            </div>
          <div>
        </div>
      </div>
    </section>`;
	}
	async toANSI(props) {
		const displayRaw = process.env.YOUCH_RAW;
		if (displayRaw) {
			const depth = Number.isNaN(Number(displayRaw)) ? 2 : Number(displayRaw);
			return `\n\n${colors.red("[RAW]")}\n${dump$1(props.error.raw, {
				depth,
				inspectObjectPrototype: false,
				inspectStaticMembers: false,
				inspectArrayPrototype: false
			})}`;
		}
		const frames = await Promise.all(props.error.frames.map((frame, index) => {
			return this.#printStackFrame(frame, index, this.#getFirstExpandedFrameIndex(props.error.frames), props);
		}));
		if (frames.length) return `\n\n${frames.join("\n")}`;
		return "";
	}
};
export { ErrorStack };
