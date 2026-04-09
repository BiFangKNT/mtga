interface RouterContext<T = unknown> {
  root: Node<T>;
  static: Record<string, Node<T> | undefined>;
}
type ParamsIndexMap = Array<[Index: number, name: string | RegExp, optional: boolean]>;
type MethodData<T = unknown> = {
  data: T;
  paramsMap?: ParamsIndexMap;
  paramsRegexp: RegExp[];
};
interface Node<T = unknown> {
  key: string;
  static?: Record<string, Node<T>>;
  param?: Node<T>;
  wildcard?: Node<T>;
  hasRegexParam?: boolean;
  methods?: Record<string, MethodData<T>[] | undefined>;
}
type MatchedRoute<T = unknown> = {
  data: T;
  params?: Record<string, string>;
};
interface RouterCompilerOptions<T = any> {
  matchAll?: boolean;
  normalize?: boolean;
  serialize?: (data: T) => string;
}
/**
* Compiles the router instance into a faster route-matching function.
*
* **IMPORTANT:** `compileRouter` requires eval support with `new Function()` in the runtime for JIT compilation.
*
* @example
* import { createRouter, addRoute } from "rou3";
* import { compileRouter } from "rou3/compiler";
* const router = createRouter();
* // [add some routes]
* const findRoute = compileRouter(router);
* const matchAll = compileRouter(router, { matchAll: true });
* findRoute("GET", "/path/foo/bar");
*
* @param router - The router context to compile.
*/
declare function compileRouter<T, O extends RouterCompilerOptions<T> = RouterCompilerOptions<T>>(router: RouterContext<T>, opts?: O): (method: string, path: string) => O["matchAll"] extends true ? MatchedRoute<T>[] : MatchedRoute<T> | undefined;
/**
* Compile the router instance into a compact runnable code.
*
* **IMPORTANT:** Route data must be serializable to JSON (i.e., no functions or classes) or implement the `toJSON()` method to render custom code or you can pass custom `serialize` function in options.
*
* @example
* import { createRouter, addRoute } from "rou3";
* import { compileRouterToString } from "rou3/compiler";
* const router = createRouter();
* // [add some routes with serializable data]
* const compilerCode = compileRouterToString(router, "findRoute");
* // "const findRoute=(m, p) => {}"
*/
declare function compileRouterToString(router: RouterContext, functionName?: string, opts?: RouterCompilerOptions): string;
export { RouterCompilerOptions, compileRouter, compileRouterToString };