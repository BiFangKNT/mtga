import * as _nuxt_schema from '@nuxt/schema';
import { BirpcGroup } from 'birpc';
import { ExecaChildProcess } from 'execa';
import { M as ModuleCustomTab, N as NuxtDevtoolsInfo, S as SubprocessOptions, T as TerminalState } from './shared/devtools-kit.BE8MVpwl.cjs';
import 'vue';
import 'nuxt/schema';
import 'unimport';
import 'vue-router';
import 'nitropack';
import 'unstorage';
import 'vite';

/**
 * Hooks to extend a custom tab in devtools.
 *
 * Provide a function to pass a factory that can be updated dynamically.
 */
declare function addCustomTab(tab: ModuleCustomTab | (() => ModuleCustomTab | Promise<ModuleCustomTab>), nuxt?: _nuxt_schema.Nuxt): void;
/**
 * Retrigger update for custom tabs, `devtools:customTabs` will be called again.
 */
declare function refreshCustomTabs(nuxt?: _nuxt_schema.Nuxt): void | Promise<any>;
/**
 * Create a subprocess that handled by the DevTools.
 */
declare function startSubprocess(execaOptions: SubprocessOptions, tabOptions: TerminalState, nuxt?: _nuxt_schema.Nuxt): {
    getProcess: () => ExecaChildProcess<string>;
    terminate: () => void;
    restart: () => void;
    clear: () => void;
};
declare function extendServerRpc<ClientFunctions extends object = Record<string, unknown>, ServerFunctions extends object = Record<string, unknown>>(namespace: string, functions: ServerFunctions, nuxt?: _nuxt_schema.Nuxt): BirpcGroup<ClientFunctions, ServerFunctions>;
declare function onDevToolsInitialized(fn: (info: NuxtDevtoolsInfo) => void, nuxt?: _nuxt_schema.Nuxt): void;

export { addCustomTab, extendServerRpc, onDevToolsInitialized, refreshCustomTabs, startSubprocess };
