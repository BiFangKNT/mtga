import * as _nuxt_schema from '@nuxt/schema';
import { Import } from 'unimport';
import { ESLintPluginOptions } from 'vite-plugin-eslint2';
import { Options } from 'eslint-webpack-plugin';
import { NuxtESLintFeaturesOptions } from '@nuxt/eslint-config/flat';

declare module '@nuxt/schema' {
    interface NuxtHooks {
        /**
         * Called before generating ESLint config, can be used to custom ESLint config integrations
         */
        'eslint:config:addons': (addons: ESLintConfigGenAddon[]) => void;
    }
}
interface ConfigGenOptions extends NuxtESLintFeaturesOptions {
    /**
     * File path to the generated ESLint config
     *
     * @default '.nuxt/eslint.config.mjs'
     */
    configFile?: string;
    /**
     * Create `eslint.config.mjs` file automatically if not exists
     *
     * @default true
     */
    autoInit?: boolean;
    /**
     * Override rootDir for the generated ESLint config
     * If you generate ESLint config from a different directory, you can set this option
     *
     * @default nuxt.options.rootDir
     */
    rootDir?: string;
    /**
     * Options for DevTools integration
     */
    devtools?: {
        /**
         * Enable ESLint config inspector in DevTools
         *
         * @default 'lazy'
         */
        enabled?: boolean | 'lazy';
        /**
         * Port for the ESLint config inspector
         */
        port?: number;
    };
}
interface CheckerOptions {
    /**
     * Use ESLint cache to improve performance
     *
     * @default true
     */
    cache?: boolean;
    /**
     * ESLint config type
     *
     * Default to `flat` unless env `ESLINT_USE_FLAT_CONFIG` is set to `false`
     *
     * @default 'flat'
     */
    configType?: 'flat' | 'eslintrc';
    /**
     * Files to include for linting
     */
    include?: string[];
    /**
     * Files to exclude from linting
     */
    exclude?: string[];
    /**
     * ESLint formatter for the output
     *
     * @see https://eslint.org/docs/user-guide/formatters/
     */
    formatter?: string;
    /**
     * Path to the ESLint module
     *
     * @default 'eslint' or 'eslint/use-at-your-own-risk' based on configType
     */
    eslintPath?: string;
    /**
     * Lint on start
     *
     * @default true
     */
    lintOnStart?: boolean;
    /**
     * The warnings found will printed
     *
     * @default true
     */
    emitWarning?: boolean;
    /**
     * The errors found will printed
     *
     * @default true
     */
    emitError?: boolean;
    /**
     * Run ESLint fix
     * @default false
     */
    fix?: boolean;
    /**
     * Vite specific options
     */
    vite?: ESLintPluginOptions;
    /**
     * Webpack specific options
     *
     * @see https://www.npmjs.com/package/eslint-webpack-plugin
     */
    webpack?: Options;
}
interface ModuleOptions {
    /**
     * Options for ESLint flat config generation (.nuxt/eslint.config.mjs)
     */
    config?: ConfigGenOptions | boolean;
    /**
     * Enable ESLint checker align with dev server or build process
     * Not enabled by default
     *
     * @default false
     */
    checker?: CheckerOptions | boolean;
}
interface ESLintConfigGenAddonResult {
    /**
     * Imports statements to add to the generated ESLint config
     */
    imports?: Import[];
    /**
     * Flat config items, should be stringified lines
     */
    configs?: string[];
}
type Awaitable<T> = T | Promise<T>;
type ESLintConfigGenAddon = {
    name: string;
    getConfigs: () => Awaitable<ESLintConfigGenAddonResult | undefined>;
};

declare const _default: _nuxt_schema.NuxtModule<ModuleOptions, ModuleOptions, false>;

export { _default as default };
export type { Awaitable, CheckerOptions, ConfigGenOptions, ESLintConfigGenAddon, ESLintConfigGenAddonResult, ModuleOptions };
