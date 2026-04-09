import { VueJSXPluginOptions } from "@vue/babel-plugin-jsx";
import { FilterPattern, Plugin } from "vite";

//#region src/types.d.ts
interface FilterOptions {
  include?: FilterPattern;
  exclude?: FilterPattern;
}
interface Options extends VueJSXPluginOptions, FilterOptions {
  babelPlugins?: any[];
  /** @default ['defineComponent'] */
  defineComponentName?: string[];
  tsPluginOptions?: any;
  /** @default 'babel' */
  tsTransform?: 'babel' | 'built-in';
}
//#endregion
//#region src/index.d.ts
declare function vueJsxPlugin(options?: Options): Plugin;
declare function vueJsxPluginCjs(this: unknown, options: Options): Plugin;
//#endregion
export { FilterOptions, Options, vueJsxPlugin as default, vueJsxPluginCjs as "module.exports" };