import { Options } from "json-schema-to-typescript-lite";
import { ESLint, Linter, Rule } from "eslint";

//#region src/core.d.ts
interface RulesTypeGenOptions {
  /**
   * Insert type imports for the generated types.
   *
   * @default true
   */
  includeTypeImports?: boolean;
  /**
   * Include comments to disable ESLint and Prettier.
   *
   * @default true
   */
  includeIgnoreComments?: boolean;
  /**
   * Augment the interface to ESLint's `Linter.RulesRecord`.
   *
   * @default true
   */
  includeAugmentation?: boolean;
  /**
   * Augment the `DefaultConfigNamesMap` interface for `eslint-flat-config-utils`
   * For auto-completion of config names etc.
   *
   * @see https://github.com/antfu/eslint-flat-config-utils
   * @default false
   */
  augmentFlatConfigUtils?: boolean;
  /**
   * The name of the exported type.
   *
   * @default 'RuleOptions'
   */
  exportTypeName?: string;
  /**
   * Options for json-schema-to-typescript
   */
  compileOptions?: Partial<Options>;
}
interface FlatConfigsToPluginsOptions {
  filterConfig?: (config: Linter.Config) => boolean;
  filterPlugin?: (name: string, plugin: ESLint.Plugin) => boolean;
}
interface FlatConfigsToRulesOptions extends RulesTypeGenOptions, FlatConfigsToPluginsOptions {}
declare function flatConfigsToPlugins(configs: Linter.Config[], options?: FlatConfigsToPluginsOptions): Promise<Record<string, ESLint.Plugin>>;
/**
 * Generate types for rules from an array of ESLint configurations.
 */
declare function flatConfigsToRulesDTS(configs: Linter.Config[], options?: FlatConfigsToRulesOptions): Promise<string>;
/**
 * Generate types for rule from an object of ESLint plugins.
 */
declare function pluginsToRulesDTS(plugins: Record<string, ESLint.Plugin>, options?: RulesTypeGenOptions & {
  configNames?: string[];
}): Promise<string>;
declare function compileRule(ruleName: string, rule: Rule.RuleModule, compileOptions?: Partial<Options>): Promise<{
  name: string;
  jsdoc: string[];
  typeName: string;
  typeDeclarations: string[];
}>;
//#endregion
export { FlatConfigsToPluginsOptions, FlatConfigsToRulesOptions, RulesTypeGenOptions, compileRule, flatConfigsToPlugins, flatConfigsToRulesDTS, pluginsToRulesDTS };