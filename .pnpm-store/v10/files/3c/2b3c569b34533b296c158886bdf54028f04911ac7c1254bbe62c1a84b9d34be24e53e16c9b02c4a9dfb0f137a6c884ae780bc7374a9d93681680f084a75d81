import * as unplugin from 'unplugin';
import { HookFilter } from 'unplugin';
import { TransformerOptions } from './transform.mjs';
import 'magic-string';

interface UnctxPluginOptions extends TransformerOptions {
    /** Plugin Hook Filter for the transform hook
     * @see https://unplugin.unjs.io/guide/#filters
     */
    transformFilter?: HookFilter;
    /** Function to determine whether a file should be transformed. If possible, use `transformFilter` instead for better performance.  */
    transformInclude?: (id: string) => boolean;
}
declare const unctxPlugin: unplugin.UnpluginInstance<UnctxPluginOptions, boolean>;

export { unctxPlugin };
export type { UnctxPluginOptions };
