import { readFile } from "node:fs/promises";
var BaseComponent = class {
	#cachedStyles;
	#cachedScript;
	#inDevMode;
	scriptFile;
	cssFile;
	constructor(devMode) {
		this.#inDevMode = devMode;
	}
	async getStyles() {
		if (!this.cssFile) return null;
		if (this.#inDevMode) return await readFile(this.cssFile, "utf-8");
		this.#cachedStyles = this.#cachedStyles ?? await readFile(this.cssFile, "utf-8");
		return this.#cachedStyles;
	}
	async getScript() {
		if (!this.scriptFile) return null;
		if (this.#inDevMode) return await readFile(this.scriptFile, "utf-8");
		this.#cachedScript = this.#cachedScript ?? await readFile(this.scriptFile, "utf-8");
		return this.#cachedScript;
	}
};
const publicDirURL = new URL("./public/", import.meta.url);
export { BaseComponent as n, publicDirURL as t };
