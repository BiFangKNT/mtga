import kleur from "kleur";
var Colors = class {
	black(text) {
		return this.transform("black", text);
	}
	red(text) {
		return this.transform("red", text);
	}
	green(text) {
		return this.transform("green", text);
	}
	yellow(text) {
		return this.transform("yellow", text);
	}
	blue(text) {
		return this.transform("blue", text);
	}
	magenta(text) {
		return this.transform("magenta", text);
	}
	cyan(text) {
		return this.transform("cyan", text);
	}
	white(text) {
		return this.transform("white", text);
	}
	gray(text) {
		return this.transform("gray", text);
	}
	grey(text) {
		return this.transform("grey", text);
	}
	bgBlack(text) {
		return this.transform("bgBlack", text);
	}
	bgRed(text) {
		return this.transform("bgRed", text);
	}
	bgGreen(text) {
		return this.transform("bgGreen", text);
	}
	bgYellow(text) {
		return this.transform("bgYellow", text);
	}
	bgBlue(text) {
		return this.transform("bgBlue", text);
	}
	bgMagenta(text) {
		return this.transform("bgMagenta", text);
	}
	bgCyan(text) {
		return this.transform("bgCyan", text);
	}
	bgWhite(text) {
		return this.transform("bgWhite", text);
	}
	reset(text) {
		return this.transform("reset", text);
	}
	bold(text) {
		return this.transform("bold", text);
	}
	dim(text) {
		return this.transform("dim", text);
	}
	italic(text) {
		return this.transform("italic", text);
	}
	underline(text) {
		return this.transform("underline", text);
	}
	inverse(text) {
		return this.transform("inverse", text);
	}
	hidden(text) {
		return this.transform("hidden", text);
	}
	strikethrough(text) {
		return this.transform("strikethrough", text);
	}
};
var Raw = class extends Colors {
	#transformations = [];
	#dispose(value, callback) {
		callback();
		return value;
	}
	transform(transformation, text) {
		this.#transformations.push(transformation);
		if (text !== void 0) {
			const transformations = this.#transformations.concat([text]).join("(");
			const closingWrapping = new Array(this.#transformations.length + 1).join(")");
			return this.#dispose(`${transformations}${closingWrapping}`, () => {
				this.#transformations = [];
			});
		}
		return this;
	}
};
var Kleur = class extends Colors {
	#chain;
	constructor() {
		super();
		kleur.enabled = true;
	}
	#dispose(value, callback) {
		callback();
		return value;
	}
	transform(transformation, text) {
		if (text !== void 0) {
			if (this.#chain) return this.#dispose(this.#chain[transformation](text), () => {
				this.#chain = void 0;
			});
			return kleur[transformation](text);
		}
		if (this.#chain) this.#chain = this.#chain[transformation]();
		else this.#chain = kleur[transformation]();
		return this;
	}
};
var Silent = class extends Colors {
	transform(_, text) {
		if (text !== void 0) return String(text);
		return this;
	}
};
var colors_default = {
	ansi() {
		return new Kleur();
	},
	silent() {
		return new Silent();
	},
	raw() {
		return new Raw();
	}
};
export { colors_default as default };
