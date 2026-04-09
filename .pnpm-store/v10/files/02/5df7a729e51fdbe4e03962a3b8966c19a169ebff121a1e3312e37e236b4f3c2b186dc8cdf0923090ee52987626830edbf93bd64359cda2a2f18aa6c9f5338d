import { UseScriptOptions as UseScriptOptions$1, ScriptInstance, UseScriptStatus, UseFunctionType } from 'unhead/scripts';
export { AsVoidFunctions, EventHandlerOptions, RecordingEntry, ScriptInstance, UseFunctionType, UseScriptResolvedInput, UseScriptStatus, WarmupStrategy, createSpyProxy, resolveScriptKey } from 'unhead/scripts';
import { ScriptWithoutEvents, DataKeys, SchemaAugmentations, HeadEntryOptions } from 'unhead/types';
import { Ref } from 'vue';
import { o as ResolvableProperties, V as VueHeadClient } from './shared/vue.DoxLTFJk.js';

interface VueScriptInstance<T extends Record<symbol | string, any>> extends Omit<ScriptInstance<T>, 'status'> {
    status: Ref<UseScriptStatus>;
}
type UseScriptInput = string | (ResolvableProperties<Omit<ScriptWithoutEvents & DataKeys & SchemaAugmentations['script'], 'src'>> & {
    src: string;
});
interface UseScriptOptions<T extends Record<symbol | string, any> = Record<string, any>> extends Omit<HeadEntryOptions, 'head'>, Pick<UseScriptOptions$1<T>, 'use' | 'eventContext' | 'beforeInit'> {
    /**
     * The trigger to load the script:
     * - `undefined` | `client` - (Default) Load the script on the client when this js is loaded.
     * - `manual` - Load the script manually by calling `$script.load()`, exists only on the client.
     * - `Promise` - Load the script when the promise resolves, exists only on the client.
     * - `Function` - Register a callback function to load the script, exists only on the client.
     * - `server` - Have the script injected on the server.
     * - `Ref<boolean>` - Load the script when the ref becomes true.
     * - `() => boolean` - Getter function, load the script when return value becomes true.
     */
    trigger?: UseScriptOptions$1['trigger'] | Ref<boolean> | (() => boolean);
    /**
     * Unhead instance.
     */
    head?: VueHeadClient<any>;
}
type UseScriptContext<T extends Record<symbol | string, any>> = VueScriptInstance<T>;
type UseScriptReturn<T extends Record<symbol | string, any>> = UseScriptContext<UseFunctionType<UseScriptOptions<T>, T>>;
declare function useScript<T extends Record<symbol | string, any> = Record<symbol | string, any>>(_input: UseScriptInput, _options?: UseScriptOptions<T>): UseScriptReturn<T>;

export { useScript };
export type { UseScriptContext, UseScriptInput, UseScriptOptions, UseScriptReturn, VueScriptInstance };
