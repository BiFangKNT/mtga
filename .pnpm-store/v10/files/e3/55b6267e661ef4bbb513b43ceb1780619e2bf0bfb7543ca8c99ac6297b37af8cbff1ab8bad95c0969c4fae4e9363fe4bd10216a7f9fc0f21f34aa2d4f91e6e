import { ConfigWithExtends } from '@eslint/config-helpers';
export { ConfigWithExtends } from '@eslint/config-helpers';
import { Linter, Rule, ESLint } from 'eslint';

/**
 * Alias to `Linter.Config`
 *
 * @deprecated
 */
interface FlatConfigItem extends Linter.Config {
}
/**
 * A type that can be awaited. Promise<T> or T.
 */
type Awaitable<T> = T | Promise<T>;
/**
 * A type that can be an array or a single item.
 */
type Arrayable<T> = T | T[];
/**
 * Default config names map. Used for type augmentation.
 *
 * @example
 * ```ts
 * declare module 'eslint-flat-config-utils' {
 *   interface DefaultConfigNamesMap {
 *     'my-custom-config': true
 *   }
 * }
 * ```
 */
interface DefaultConfigNamesMap {
}
interface Nothing {
}
/**
 * type StringLiteralUnion<'foo'> = 'foo' | string
 * This has auto completion whereas `'foo' | string` doesn't
 * Adapted from https://github.com/microsoft/TypeScript/issues/29729
 */
type StringLiteralUnion<T extends U, U = string> = T | (U & Nothing);
type FilterType<T, F> = T extends F ? T : never;
type NullableObject<T> = {
    [K in keyof T]?: T[K] | null | undefined;
};
type GetRuleRecordFromConfig<T> = T extends {
    rules?: infer R;
} ? R : Linter.RulesRecord;

declare const DEFAULT_PLUGIN_CONFLICTS_ERROR = "Different instances of plugin \"{{pluginName}}\" found in multiple configs: {{configNames}}. It's likely you misconfigured the merge of these configs.";
interface DisableFixesOptions {
    builtinRules?: Map<string, Rule.RuleModule> | (() => Awaitable<Map<string, Rule.RuleModule>>);
}
type PluginConflictsError<T extends Linter.Config = Linter.Config> = (pluginName: string, configs: T[]) => string;
/**
 * Awaitable array of ESLint flat configs or a composer object.
 */
type ResolvableFlatConfig<T extends object = ConfigWithExtends> = Awaitable<Arrayable<(T | false | undefined | null)>> | Awaitable<(ConfigWithExtends | false | undefined | null)[]> | Awaitable<(Linter.Config | false | undefined | null)[]> | FlatConfigComposer<any>;
/**
 * Create a chainable composer object that makes manipulating ESLint flat config easier.
 *
 * It extends Promise, so that you can directly await or export it to `eslint.config.mjs`
 *
 * ```ts
 * // eslint.config.mjs
 * import { composer } from 'eslint-flat-config-utils'
 *
 * export default composer(
 *   {
 *     plugins: {},
 *     rules: {},
 *   }
 *   // ...some configs, accepts same arguments as `concat`
 * )
 *   .append(
 *     // appends more configs at the end, accepts same arguments as `concat`
 *   )
 *   .prepend(
 *     // prepends more configs at the beginning, accepts same arguments as `concat`
 *   )
 *   .insertAfter(
 *     'config-name', // specify the name of the target config, or index
 *     // insert more configs after the target, accepts same arguments as `concat`
 *   )
 *   .renamePlugins({
 *     // rename plugins
 *     'old-name': 'new-name',
 *     // for example, rename `n` from `eslint-plugin-n` to more a explicit prefix `node`
 *     'n': 'node'
 *     // applies to all plugins and rules in the configs
 *   })
 *   .override(
 *     'config-name', // specify the name of the target config, or index
 *     {
 *       // merge with the target config
 *       rules: {
 *         'no-console': 'off'
 *       },
 *     }
 *   )
 *
 * // And you an directly return the composer object to `eslint.config.mjs`
 * ```
 */
declare function composer<T extends ConfigWithExtends = ConfigWithExtends, ConfigNames extends string = keyof DefaultConfigNamesMap>(...configs: ResolvableFlatConfig<ConfigWithExtends extends T ? T : ConfigWithExtends>[]): FlatConfigComposer<ConfigWithExtends extends T ? T : ConfigWithExtends, ConfigNames>;
/**
 * The underlying impolementation of `composer()`.
 */
declare class FlatConfigComposer<T extends object = ConfigWithExtends, ConfigNames extends string = keyof DefaultConfigNamesMap> extends Promise<Linter.Config[]> {
    private _operations;
    private _operationsOverrides;
    private _operationsResolved;
    private _renames;
    private _pluginsConflictsError;
    constructor(...configs: ResolvableFlatConfig<T>[]);
    /**
     * Set plugin renames, like `n` -> `node`, `import-x` -> `import`, etc.
     *
     * This will runs after all config items are resolved. Applies to `plugins` and `rules`.
     */
    renamePlugins(renames: Record<string, string>): this;
    /**
     * Append configs to the end of the current configs array.
     */
    append(...items: ResolvableFlatConfig<T>[]): this;
    /**
     * Prepend configs to the beginning of the current configs array.
     */
    prepend(...items: ResolvableFlatConfig<T>[]): this;
    /**
     * Insert configs before a specific config.
     */
    insertBefore(nameOrIndex: StringLiteralUnion<ConfigNames, string | number>, ...items: ResolvableFlatConfig<T>[]): this;
    /**
     * Insert configs after a specific config.
     */
    insertAfter(nameOrIndex: StringLiteralUnion<ConfigNames, string | number>, ...items: ResolvableFlatConfig<T>[]): this;
    /**
     * Provide overrides to a specific config.
     *
     * It will be merged with the original config, or provide a custom function to replace the config entirely.
     */
    override(nameOrIndex: StringLiteralUnion<ConfigNames, string | number>, config: T | ((config: T) => Awaitable<T>)): this;
    /**
     * Provide overrides to multiple configs as an object map.
     *
     * Same as calling `override` multiple times.
     */
    overrides(overrides: Partial<Record<StringLiteralUnion<ConfigNames, string | number>, T | ((config: T) => Awaitable<T>)>>): this;
    /**
     * Override rules and it's options in **all configs**.
     *
     * Pass `null` as the value to remove the rule.
     *
     * @example
     * ```ts
     * composer
     *   .overrideRules({
     *      'no-console': 'off',
     *      'no-unused-vars': ['error', { vars: 'all', args: 'after-used' }],
     *      // remove the rule from all configs
     *      'no-undef': null,
     *   })
     * ```
     */
    overrideRules(rules: NullableObject<GetRuleRecordFromConfig<T>>): this;
    /**
     * Remove rules from **all configs**.
     *
     * @example
     * ```ts
     * composer
     *  .removeRules(
     *    'no-console',
     *    'no-unused-vars'
     *  )
     * ```
     */
    removeRules(...rules: StringLiteralUnion<FilterType<keyof GetRuleRecordFromConfig<T>, string>, string>[]): this;
    /**
     * Remove plugins by name and all the rules referenced by them.
     *
     * @example
     * ```ts
     * composer
     *   .removePlugins(
     *     'node'
     *   )
     * ```
     *
     * The `plugins: { node }` and `rules: { 'node/xxx': 'error' }` will be removed from all configs.
     */
    removePlugins(...names: string[]): this;
    /**
     * Remove a specific config by name or index.
     */
    remove(nameOrIndex: ConfigNames | string | number): this;
    /**
     * Replace a specific config by name or index.
     *
     * The original config will be removed and replaced with the new one.
     */
    replace(nameOrIndex: StringLiteralUnion<ConfigNames, string | number>, ...items: ResolvableFlatConfig<T>[]): this;
    /**
     * Hijack into plugins to disable fixes for specific rules.
     *
     * Note this mutates the plugin object, use with caution.
     *
     * @example
     * ```ts
     * const config = await composer(...)
     *  .disableRulesFix([
     *    'unused-imports/no-unused-imports',
     *    'vitest/no-only-tests'
     *  ])
     * ```
     */
    disableRulesFix(ruleIds: string[], options?: DisableFixesOptions): this;
    /**
     * Set a custom warning message for plugins conflicts.
     *
     * The error message can be a string or a function that returns a string.
     *
     * Error message accepts template strings:
     * - `{{pluginName}}`: the name of the plugin that has conflicts
     * - `{{configName1}}`: the name of the first config that uses the plugin
     * - `{{configName2}}`: the name of the second config that uses the plugin
     * - `{{configNames}}`: a list of config names that uses the plugin
     *
     * When only one argument is provided, it will be used as the default error message.
     */
    setPluginConflictsError(warning?: string | PluginConflictsError): this;
    setPluginConflictsError(pluginName: string, warning: string | PluginConflictsError): this;
    private _verifyPluginsConflicts;
    /**
     * Hook when all configs are resolved but before returning the final configs.
     *
     * You can modify the final configs here.
     */
    onResolved(callback: (configs: T[]) => Awaitable<T[] | void>): this;
    /**
     * Clone the composer object.
     */
    clone(): FlatConfigComposer<T>;
    /**
     * Resolve the pipeline and return the final configs.
     *
     * This returns a promise. Calling `.then()` has the same effect.
     */
    toConfigs(): Promise<Linter.Config[]>;
    then<T>(onFulfilled: (value: Linter.Config[]) => T, onRejected?: (reason: any) => any): Promise<Awaited<T>>;
    catch(onRejected: (reason: any) => any): Promise<any>;
    finally(onFinally: () => void): Promise<Linter.Config[]>;
}
/**
 * @deprecated Renamed to `composer`.
 */
declare const pipe: typeof composer;
/**
 * @deprecated Renamed to `FlatConfigComposer`.
 */
declare class FlatConfigPipeline<T extends object = Linter.Config, ConfigNames extends string = string> extends FlatConfigComposer<T, ConfigNames> {
}

/**
 * Concat multiple flat configs into a single flat config array.
 *
 * It also resolves promises and flattens the result.
 *
 * @example
 *
 * ```ts
 * import { concat } from 'eslint-flat-config-utils'
 * import eslint from '@eslint/js'
 * import stylistic from '@stylistic/eslint-plugin'
 *
 * export default concat(
 *   eslint,
 *   stylistic.configs.customize(),
 *   { rules: { 'no-console': 'off' } },
 *   // ...
 * )
 * ```
 */
declare function concat<T extends Linter.Config = Linter.Config>(...configs: Awaitable<T | T[]>[]): Promise<T[]>;

/**
 * A function that returns the config as-is, useful for providing type hints.
 */
declare function defineFlatConfig<T extends Linter.Config = Linter.Config>(config: T): T;

/**
 * Extend another flat configs and rename globs paths.
 *
 * @example
 * ```ts
 * import { extend } from 'eslint-flat-config-utils'
 *
 * export default [
 *   ...await extend(
 *     // configs to extend
 *     import('./other-configs/eslint.config.js').then(m => m.default),
 *     // relative directory path
 *     'other-configs/',
 *   ),
 * ]
 * ```
 */
declare function extend(configs: Awaitable<Linter.Config[]>, relativePath: string): Promise<Linter.Config[]>;

/**
 * Replace a rule in a plugin with given factory.
 */
declare function hijackPluginRule(plugin: ESLint.Plugin, name: string, factory: (rule: Rule.RuleModule) => Rule.RuleModule): ESLint.Plugin;
/**
 * Hijack into a rule's `context.report` to disable fixes.
 */
declare function disableRuleFixes(rule: Rule.RuleModule): Rule.RuleModule;

/**
 * Merge multiple flat configs into a single flat config.
 *
 * Note there is no guarantee that the result works the same as the original configs.
 */
declare function mergeConfigs<T extends Linter.Config = Linter.Config>(...configs: T[]): T;

declare function parseRuleId(ruleId: string): {
    plugin: string | null;
    rule: string;
};

/**
 * Rename plugin prefixes in a rule object.
 * Accepts a map of prefixes to rename.
 *
 * @example
 * ```ts
 * import { renamePluginsInRules } from 'eslint-flat-config-utils'
 *
 * export default [{
 *   rules: renamePluginsInRules(
 *     {
 *       '@typescript-eslint/indent': 'error'
 *     },
 *     { '@typescript-eslint': 'ts' }
 *   )
 * }]
 * ```
 */
declare function renamePluginsInRules(rules: Record<string, any>, map: Record<string, string>): Record<string, any>;
/**
 * Rename plugin names a flat configs array
 *
 * @example
 * ```ts
 * import { renamePluginsInConfigs } from 'eslint-flat-config-utils'
 * import someConfigs from './some-configs'
 *
 * export default renamePluginsInConfigs(someConfigs, {
 *   '@typescript-eslint': 'ts',
 *   'import-x': 'import',
 * })
 * ```
 */
declare function renamePluginsInConfigs<T extends Linter.Config = Linter.Config>(configs: T[], map: Record<string, string>): T[];

export { DEFAULT_PLUGIN_CONFLICTS_ERROR, FlatConfigComposer, FlatConfigPipeline, composer, concat, defineFlatConfig, disableRuleFixes, extend, hijackPluginRule, mergeConfigs, parseRuleId, pipe, renamePluginsInConfigs, renamePluginsInRules };
export type { Arrayable, Awaitable, DefaultConfigNamesMap, DisableFixesOptions, FilterType, FlatConfigItem, GetRuleRecordFromConfig, NullableObject, PluginConflictsError, ResolvableFlatConfig, StringLiteralUnion };
