import { n as BaseComponent } from "./public_dir-C5bujZKB.js";
import { Header } from "./src/templates/header/main.js";
import { Layout } from "./src/templates/layout/main.js";
import "./helpers-B9BQYaS6.js";
import { ErrorInfo } from "./src/templates/error_info/main.js";
import { ErrorCause } from "./src/templates/error_cause/main.js";
import { ErrorStack } from "./src/templates/error_stack/main.js";
import { ErrorMetadata } from "./src/templates/error_metadata/main.js";
import { ErrorStackSource } from "./src/templates/error_stack_source/main.js";
import { parse } from "cookie-es";
import { ErrorParser } from "youch-core";
import { createScript, createStyleSheet } from "@poppinss/dumper/html";
var Metadata = class {
	#groups = {};
	#toArray(value) {
		return Array.isArray(value) ? value : [value];
	}
	group(name, sections) {
		this.#groups[name] = this.#groups[name] ?? {};
		Object.keys(sections).forEach((section) => {
			if (!this.#groups[name][section]) this.#groups[name][section] = sections[section];
			else {
				this.#groups[name][section] = this.#toArray(this.#groups[name][section]);
				this.#groups[name][section].push(...this.#toArray(sections[section]));
			}
		});
		return this;
	}
	toJSON() {
		return this.#groups;
	}
};
var Templates = class {
	#knownTemplates;
	#styles = new Map([["global", createStyleSheet()]]);
	#scripts = new Map([["global", createScript()]]);
	constructor(devMode) {
		this.devMode = devMode;
		this.#knownTemplates = {
			layout: new Layout(devMode),
			header: new Header(devMode),
			errorInfo: new ErrorInfo(devMode),
			errorStack: new ErrorStack(devMode),
			errorStackSource: new ErrorStackSource(devMode),
			errorCause: new ErrorCause(devMode),
			errorMetadata: new ErrorMetadata(devMode)
		};
	}
	#getStylesAndScripts(cspNonce) {
		let customInjectedStyles = "";
		let globalScript = "";
		const styles = [];
		const scripts = [];
		const cspNonceAttr = cspNonce ? ` nonce="${cspNonce}"` : "";
		this.#styles.forEach((bucket, name) => {
			if (name === "injected") customInjectedStyles = `<style id="${name}-styles"${cspNonceAttr}>${bucket}</style>`;
			else styles.push(`<style id="${name}-styles"${cspNonceAttr}>${bucket}</style>`);
		});
		this.#scripts.forEach((bucket, name) => {
			if (name === "global") globalScript = `<script id="${name}-script"${cspNonceAttr}>${bucket}<\/script>`;
			scripts.push(`<script id="${name}-script"${cspNonceAttr}>${bucket}<\/script>`);
		});
		return {
			styles: `${styles.join("\n")}\n${customInjectedStyles}`,
			scripts: scripts.join("\n"),
			globalScript
		};
	}
	async #collectStylesAndScripts(templateName) {
		if (!this.#styles.has(templateName)) {
			const styles = await this.#knownTemplates[templateName].getStyles();
			if (styles) this.#styles.set(templateName, styles);
		}
		if (!this.#scripts.has(templateName)) {
			const script = await this.#knownTemplates[templateName].getScript();
			if (script) this.#scripts.set(templateName, script);
		}
	}
	async #tmplToHTML(templateName, props) {
		const component = this.#knownTemplates[templateName];
		if (!component) throw new Error(`Invalid template "${templateName}"`);
		await this.#collectStylesAndScripts(templateName);
		return component.toHTML(props);
	}
	async #tmplToANSI(templateName, props) {
		const component = this.#knownTemplates[templateName];
		if (!component) throw new Error(`Invalid template "${templateName}"`);
		return component.toANSI(props);
	}
	use(templateName, component) {
		this.#knownTemplates[templateName] = component;
		return this;
	}
	injectStyles(cssFragment) {
		let injectedStyles = this.#styles.get("injected") ?? "";
		injectedStyles += `\n${cssFragment}`;
		this.#styles.set("injected", injectedStyles);
		return this;
	}
	async toHTML(props) {
		const html = await this.#tmplToHTML("layout", {
			title: props.title,
			ide: props.ide,
			cspNonce: props.cspNonce,
			children: async () => {
				return `${await this.#tmplToHTML("header", props)}${await this.#tmplToHTML("errorInfo", props)}${await this.#tmplToHTML("errorStack", {
					ide: process.env.EDITOR ?? "vscode",
					sourceCodeRenderer: (error, frame) => {
						return this.#tmplToHTML("errorStackSource", {
							error,
							frame,
							ide: props.ide,
							cspNonce: props.cspNonce
						});
					},
					...props
				})}${await this.#tmplToHTML("errorCause", props)}${await this.#tmplToHTML("errorMetadata", props)}`;
			}
		});
		const { globalScript, scripts, styles } = this.#getStylesAndScripts(props.cspNonce);
		return html.replace("<!-- STYLES -->", styles).replace("<!-- SCRIPTS -->", scripts).replace("<!-- GLOBAL SCRIPT -->", globalScript);
	}
	async toANSI(props) {
		return await this.#tmplToANSI("layout", {
			title: props.title,
			children: async () => {
				return `${await this.#tmplToANSI("header", {})}${await this.#tmplToANSI("errorInfo", props)}${await this.#tmplToANSI("errorStack", {
					ide: process.env.EDITOR ?? "vscode",
					sourceCodeRenderer: (error, frame) => {
						return this.#tmplToANSI("errorStackSource", {
							error,
							frame
						});
					},
					...props
				})}${await this.#tmplToANSI("errorCause", props)}${await this.#tmplToANSI("errorMetadata", props)}`;
			}
		});
	}
};
var Youch = class {
	#sourceLoader;
	#parsers = [];
	#transformers = [];
	templates = new Templates(false);
	metadata = new Metadata();
	#createErrorParser(options) {
		const errorParser = new ErrorParser(options);
		if (this.#sourceLoader) errorParser.defineSourceLoader(this.#sourceLoader);
		this.#parsers.forEach((parser) => errorParser.useParser(parser));
		this.#transformers.forEach((transformer) => errorParser.useTransformer(transformer));
		return errorParser;
	}
	#defineRequestMetadataGroup(request) {
		if (!request || Object.keys(request).length === 0) return;
		this.metadata.group("Request", {
			...request.url ? { url: {
				key: "URL",
				value: request.url
			} } : {},
			...request.method ? { method: {
				key: "Method",
				value: request.method
			} } : {},
			...request.headers ? { headers: Object.keys(request.headers).map((key) => {
				const value = request.headers[key];
				return {
					key,
					value: key === "cookie" ? { ...parse(value) } : value
				};
			}) } : {}
		});
	}
	defineSourceLoader(loader) {
		this.#sourceLoader = loader;
		return this;
	}
	useParser(parser) {
		this.#parsers.push(parser);
		return this;
	}
	useTransformer(transformer) {
		this.#transformers.push(transformer);
		return this;
	}
	async toJSON(error, options) {
		options = { ...options };
		return this.#createErrorParser({ offset: options.offset }).parse(error);
	}
	async toHTML(error, options) {
		options = { ...options };
		this.#defineRequestMetadataGroup(options.request);
		const parsedError = await this.#createErrorParser({ offset: options.offset }).parse(error);
		return this.templates.toHTML({
			title: options.title ?? "An error has occurred",
			ide: options.ide ?? process.env.IDE ?? "vscode",
			cspNonce: options.cspNonce,
			error: parsedError,
			metadata: this.metadata
		});
	}
	async toANSI(error, options) {
		options = { ...options };
		const parsedError = await this.#createErrorParser({ offset: options.offset }).parse(error);
		return this.templates.toANSI({
			title: "",
			error: parsedError,
			metadata: this.metadata
		});
	}
};
export { BaseComponent, Metadata, Youch };
