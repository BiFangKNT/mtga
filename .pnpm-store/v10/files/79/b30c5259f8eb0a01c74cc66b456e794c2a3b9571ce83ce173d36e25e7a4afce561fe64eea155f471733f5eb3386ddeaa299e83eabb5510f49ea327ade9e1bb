import { RuleOptions } from "./rule-options.js";
import { ESLint, Linter, Rule } from "eslint";

//#region src/dts/configs.d.ts
declare const configs: {
  /**
   * The default recommended config in Flat Config Format
   */
  recommended: Linter.Config;
  /**
   * Enable all rules, in Flat Config Format
   */
  all: Linter.Config;
};
type Configs = typeof configs;
//#endregion
//#region src/dts/rules.d.ts
type RuleName<K extends string> = K extends `${string}/${infer Name}` ? RuleName<Name> : K;
type Rules = Required<{ [K in keyof RuleOptions as RuleName<K>]: Rule.RuleModule }>;
//#endregion
//#region src/dts/index.d.ts
declare const plugin: {
  rules: Rules;
  configs: ESLint.Plugin['configs'] & Configs;
};
//#endregion
export { type Configs, type RuleOptions, type Rules, plugin as default };