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
type ExtractWildcards<TPath extends string, Count extends readonly unknown[] = []> = TPath extends `${string}**:${infer Rest}` ? Rest extends `${infer Param}/${infer Tail}` ? Param | ExtractWildcards<Tail, Count> : Rest : TPath extends `${string}*${infer Rest}` ? Rest extends `*` ? `_` : `${Count["length"]}` | ExtractWildcards<Rest, [...Count, unknown]> : TPath extends `${string}/${infer Rest}` ? ExtractWildcards<Rest, Count> : never;
type ExtractNamedParams<TPath extends string> = TPath extends `${infer _Start}:${infer Rest}` ? Rest extends `${infer Param}/${infer Tail}` ? Param | ExtractNamedParams<`/${Tail}`> : Rest extends `${infer Param}*${infer Tail}` ? Param | ExtractNamedParams<`/${Tail}`> : Rest : TPath extends `/${infer Rest}` ? ExtractNamedParams<Rest> : never;
type InferRouteParams<TPath extends string> = { [K in ExtractNamedParams<TPath> | ExtractWildcards<TPath>]: string };
/**
* Create a new router context.
*/
declare function createRouter<T = unknown>(): RouterContext<T>;
/**
* Add a route to the router context.
*/
declare function addRoute<T>(ctx: RouterContext<T>, method: string | undefined, path: string, data?: T): void;
/**
* Find a route by path.
*/
declare function findRoute<T = unknown>(ctx: RouterContext<T>, method: string | undefined, path: string, opts?: {
  params?: boolean;
  normalize?: boolean;
}): MatchedRoute<T> | undefined;
/**
* Remove a route from the router context.
*/
declare function removeRoute<T>(ctx: RouterContext<T>, method: string, path: string): void;
/**
* Find all route patterns that match the given path.
*/
declare function findAllRoutes<T>(ctx: RouterContext<T>, method: string | undefined, path: string, opts?: {
  params?: boolean;
  normalize?: boolean;
}): MatchedRoute<T>[];
declare function routeToRegExp(route?: string): RegExp;
declare const NullProtoObj: {
  new (): any;
};
export { type InferRouteParams, type MatchedRoute, NullProtoObj, type RouterContext, addRoute, createRouter, findAllRoutes, findRoute, removeRoute, routeToRegExp };