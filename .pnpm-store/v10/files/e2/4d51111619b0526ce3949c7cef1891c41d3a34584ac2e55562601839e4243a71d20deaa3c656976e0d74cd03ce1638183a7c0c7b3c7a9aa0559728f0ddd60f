import { t as consistent_type_specifier_style_default } from "./rules/consistent-type-specifier-style.mjs";
import { t as exports_last_default } from "./rules/exports-last.mjs";
import { t as first_default } from "./rules/first.mjs";
import { t as newline_after_import_default } from "./rules/newline-after-import.mjs";
import { t as no_default_export_default } from "./rules/no-default-export.mjs";
import { t as no_duplicates_default } from "./rules/no-duplicates.mjs";
import { t as no_mutable_exports_default } from "./rules/no-mutable-exports.mjs";
import { t as no_named_default_default } from "./rules/no-named-default.mjs";
import { t as prefer_default_export_default } from "./rules/prefer-default-export.mjs";

//#region src/rules/index.ts
const rules = {
	"consistent-type-specifier-style": consistent_type_specifier_style_default,
	"exports-last": exports_last_default,
	"first": first_default,
	"newline-after-import": newline_after_import_default,
	"no-default-export": no_default_export_default,
	"no-duplicates": no_duplicates_default,
	"no-mutable-exports": no_mutable_exports_default,
	"no-named-default": no_named_default_default,
	"prefer-default-export": prefer_default_export_default
};

//#endregion
//#region src/index.ts
const pluginName = "import-lite";
function generateConfig(name, filter = () => true) {
	const ruleMeta = Object.entries(rules).filter(([ruleName, rule]) => !rule.meta?.deprecated && filter(ruleName, rule));
	return {
		name: `${pluginName}/${name}`,
		plugins: { [pluginName]: {
			name: pluginName,
			rules
		} },
		rules: Object.fromEntries(ruleMeta.map(([ruleName]) => [`${pluginName}/${ruleName}`, "error"]))
	};
}
var src_default = {
	rules,
	configs: {
		recommended: generateConfig("recommended", (_, rule) => !!rule.meta?.docs?.recommended),
		all: generateConfig("all")
	}
};

//#endregion
export { src_default as default, pluginName };