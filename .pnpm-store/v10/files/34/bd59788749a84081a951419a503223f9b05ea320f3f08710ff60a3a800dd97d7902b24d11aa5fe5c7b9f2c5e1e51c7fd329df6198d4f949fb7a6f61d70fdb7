/*!
 * vue-router v5.0.4
 * (c) 2026 Eduardo San Martin Morote
 * @license MIT
 */
import { a as DefineLoaderFn, b as trackRoute, c as UseDataLoaderResult, d as DataLoaderPlugin, f as DataLoaderPluginOptions, g as useIsDataLoading, h as reroute, i as DefineDataLoaderOptionsBase_LaxData, l as toLazyValue, m as SetupLoaderGuardOptions, n as DataLoaderEntryBase, o as UseDataLoader, p as NavigationResult$1, r as DefineDataLoaderOptionsBase_DefinedData, s as UseDataLoaderInternals, t as DataLoaderContextBase, u as ErrorDefault, v as getCurrentContext, x as withLoaderContext, y as setCurrentContext } from "../index-C3eYkdSl.js";
import { $ as MatcherQueryParamsValue, A as EXPERIMENTAL_RouterOptions, B as defineQueryParamParser, C as EXPERIMENTAL_RouteRecordNormalized_Group, D as EXPERIMENTAL_RouteRecord_Group, E as EXPERIMENTAL_RouteRecord_Base, F as createFixedResolver, G as MatcherParamsFormatted, H as PARAM_PARSER_BOOL, I as MatcherPatternQuery, J as MatcherPatternPath, K as MatcherPattern, L as MatcherPatternQueryParam, M as EXPERIMENTAL_Router_Base, N as experimental_createRouter, O as EXPERIMENTAL_RouteRecord_Matchable, P as normalizeRouteRecord, Q as MatcherQueryParams, R as defineParamParser, S as EXPERIMENTAL_RouteRecordNormalized, T as EXPERIMENTAL_RouteRecordRaw, V as PARAM_PARSER_INT, Vn as TypesConfig, W as EmptyParams, X as MatcherPatternPathDynamic_ParamOptions, Y as MatcherPatternPathDynamic, Z as MatcherPatternPathStatic, et as ParamParser, j as EXPERIMENTAL_RouterOptions_Base, jt as RouteLocationNormalizedLoaded, k as EXPERIMENTAL_Router, q as MatcherPatternHash, tn as RouteMap, w as EXPERIMENTAL_RouteRecordNormalized_Matchable, xn as RouteRecordRaw, z as definePathParamParser } from "../index-BzEKChPW.js";

//#region src/experimental/route-resolver/matchers/errors.d.ts
/**
 * Error throw when a matcher matches by regex but validation fails.
 *
 * @internal
 */
declare class MatchMiss extends Error {
  name: string;
}
/**
 * Helper to throw a {@link MatchMiss} error.
 * @param args - Arguments to pass to the `MatchMiss` constructor.
 *
 * @example
 * ```ts
 * miss()
 * // in a number param matcher
 * miss('Number must be finite')
 * ```
 */
declare const miss: (...args: ConstructorParameters<typeof MatchMiss>) => never;
//#endregion
//#region src/experimental/runtime.d.ts
/**
 * Helper to define page properties with file-based routing.
 * **Doesn't do anything**, used for types only.
 *
 * @param route - route information to be added to this page
 *
 * @internal
 */
declare const definePage: (route: DefinePage) => DefinePage;
/**
 * Merges route records.
 *
 * @internal
 *
 * @param main - main route record
 * @param routeRecords - route records to merge
 * @returns merged route record
 */
declare function _mergeRouteRecord(main: RouteRecordRaw, ...routeRecords: Partial<RouteRecordRaw>[]): RouteRecordRaw;
/**
 * Type to define a page. Can be augmented to add custom properties.
 */
interface DefinePage extends Partial<Omit<RouteRecordRaw, 'children' | 'components' | 'component' | 'name'>> {
  /**
   * A route name. If not provided, the name will be generated based on the file path.
   * Can be set to `false` to remove the name from types.
   */
  name?: string | false;
  /**
   * Custom parameters for the route. Requires `experimental.paramParsers` enabled.
   *
   * @experimental
   */
  params?: {
    path?: Record<string, ParamParserType>;
    /**
     * Parameters extracted from the query.
     */
    query?: Record<string, DefinePageQueryParamOptions | ParamParserType>;
  };
}
type ParamParserType_Native = 'int' | 'bool';
type ParamParserType = (TypesConfig extends Record<'ParamParsers', infer ParamParsers> ? ParamParsers : never) | ParamParserType_Native;
/**
 * Configures how to extract a route param from a specific query parameter.
 */
interface DefinePageQueryParamOptions<T = unknown> {
  /**
   * The type of the query parameter. Allowed values are native param parsers
   * and any parser in the {@link https://uvr.esm.is/TODO | params folder }. If
   * not provided, the value will kept as is.
   */
  parser?: ParamParserType;
  /**
   * Default value if the query parameter is missing or if the match fails
   * (e.g. a invalid number is passed to the int param parser). If not provided
   * and the param is not required, the route will match with undefined.
   */
  default?: (() => T) | T;
  /**
   * How to format the query parameter value.
   *
   * - 'value' - keep the first value only and pass that to parser
   * - 'array' - keep all values (even one or none) as an array and pass that to parser
   *
   * @default 'value'
   */
  format?: 'value' | 'array';
  /**
   * Whether this query parameter is required. If true and the parameter is
   * missing (and no default is provided), the route will not match.
   *
   * @default false
   */
  required?: boolean;
}
//#endregion
//#region src/experimental/data-loaders/defineLoader.d.ts
/**
 * Creates a data loader composable that can be exported by pages to attach the data loading to a route. In this version `data` is always defined.
 *
 * @param name - name of the route
 * @param loader - function that returns a promise with the data
 * @param options - options to configure the data loader
 */
declare function defineBasicLoader<Name extends keyof RouteMap, Data>(name: Name, loader: DefineLoaderFn<Data, DataLoaderContext, RouteLocationNormalizedLoaded<Name>>, options?: DefineDataLoaderOptions_DefinedData): UseDataLoaderBasic_DefinedData<Data>;
/**
 * Creates a data loader composable that can be exported by pages to attach the data loading to a route. In this version, `data` can be `undefined`.
 *
 * @param name - name of the route
 * @param loader - function that returns a promise with the data
 * @param options - options to configure the data loader
 */
declare function defineBasicLoader<Name extends keyof RouteMap, Data>(name: Name, loader: DefineLoaderFn<Data, DataLoaderContext, RouteLocationNormalizedLoaded<Name>>, options: DefineDataLoaderOptions_LaxData): UseDataLoaderBasic_LaxData<Data>;
/**
 * Creates a data loader composable that can be exported by pages to attach the data loading to a route. In this version `data` is always defined.
 *
 * @param loader - function that returns a promise with the data
 * @param options - options to configure the data loader
 */
declare function defineBasicLoader<Data>(loader: DefineLoaderFn<Data, DataLoaderContext, RouteLocationNormalizedLoaded>, options?: DefineDataLoaderOptions_DefinedData): UseDataLoaderBasic_DefinedData<Data>;
/**
 * Creates a data loader composable that can be exported by pages to attach the data loading to a route. In this version, `data` can be `undefined`.
 *
 * @param loader - function that returns a promise with the data
 * @param options - options to configure the data loader
 */
declare function defineBasicLoader<Data>(loader: DefineLoaderFn<Data, DataLoaderContext, RouteLocationNormalizedLoaded>, options: DefineDataLoaderOptions_LaxData): UseDataLoaderBasic_LaxData<Data>;
interface DefineDataLoaderOptions_LaxData extends DefineDataLoaderOptionsBase_LaxData {
  /**
   * Key to use for SSR state. This will be used to read the initial data from `initialData`'s object.
   */
  key?: string;
}
interface DefineDataLoaderOptions_DefinedData extends DefineDataLoaderOptionsBase_DefinedData {
  key?: string;
}
/**
 * @deprecated use {@link DefineDataLoaderOptions_LaxData} instead
 */
type DefineDataLoaderOptions = DefineDataLoaderOptions_LaxData;
interface DataLoaderContext extends DataLoaderContextBase {}
/**
 * Symbol used to store the data in the router so it can be retrieved after the initial navigation.
 * @internal
 */
declare const SERVER_INITIAL_DATA_KEY: unique symbol;
/**
 * Initial data generated on server and consumed on client.
 * @internal
 */
declare const INITIAL_DATA_KEY: unique symbol;
declare module '../../router' {
  interface Router {
    /**
     * Gives access to the initial state during rendering. Should be set to `false` once it's consumed.
     * @internal
     */
    [SERVER_INITIAL_DATA_KEY]?: Record<string, unknown> | false;
    [INITIAL_DATA_KEY]?: Record<string, unknown> | false;
  }
}
interface UseDataLoaderBasic_LaxData<Data> extends UseDataLoader<Data | undefined, ErrorDefault> {}
/**
 * @deprecated use {@link UseDataLoaderBasic_LaxData} instead
 */
type UseDataLoaderBasic<Data> = UseDataLoaderBasic_LaxData<Data>;
interface UseDataLoaderBasic_DefinedData<Data> extends UseDataLoader<Data, ErrorDefault> {}
interface DataLoaderBasicEntry<TData, TError = unknown, TDataInitial extends TData | undefined = TData | undefined> extends DataLoaderEntryBase<TData, TError, TDataInitial> {}
//#endregion
//#region src/experimental/index.d.ts
/**
 * @deprecated Use {@link reroute} instead.
 */
declare class NavigationResult extends NavigationResult$1 {
  constructor(...args: ConstructorParameters<typeof NavigationResult$1>);
}
//#endregion
export { type DataLoaderBasicEntry, type DataLoaderContext, type DataLoaderContextBase, type DataLoaderEntryBase, DataLoaderPlugin, type DataLoaderPluginOptions, type DefineDataLoaderOptions, type DefineDataLoaderOptionsBase_DefinedData, type DefineDataLoaderOptionsBase_LaxData, type DefineDataLoaderOptions_DefinedData, type DefineDataLoaderOptions_LaxData, type DefineLoaderFn, type DefinePage, type DefinePageQueryParamOptions, type EXPERIMENTAL_RouteRecordNormalized, type EXPERIMENTAL_RouteRecordNormalized_Group, type EXPERIMENTAL_RouteRecordNormalized_Matchable, type EXPERIMENTAL_RouteRecordRaw, type EXPERIMENTAL_RouteRecord_Base, type EXPERIMENTAL_RouteRecord_Group, type EXPERIMENTAL_RouteRecord_Matchable, type EXPERIMENTAL_Router, type EXPERIMENTAL_RouterOptions, type EXPERIMENTAL_RouterOptions_Base, type EXPERIMENTAL_Router_Base, type EmptyParams, type ErrorDefault, type MatcherParamsFormatted, type MatcherPattern, type MatcherPatternHash, type MatcherPatternPath, MatcherPatternPathDynamic, type MatcherPatternPathDynamic_ParamOptions, MatcherPatternPathStatic, type MatcherPatternQuery, MatcherPatternQueryParam, type MatcherQueryParams, type MatcherQueryParamsValue, NavigationResult, PARAM_PARSER_BOOL, PARAM_PARSER_INT, type ParamParser, type ParamParserType, type ParamParserType_Native, type SetupLoaderGuardOptions, type UseDataLoader, type UseDataLoaderBasic, type UseDataLoaderBasic_DefinedData, type UseDataLoaderBasic_LaxData, type UseDataLoaderInternals, type UseDataLoaderResult, MatchMiss as _MatchMiss, NavigationResult$1 as _NavigationResult, _mergeRouteRecord, createFixedResolver, defineBasicLoader, definePage, defineParamParser, definePathParamParser, defineQueryParamParser, experimental_createRouter, getCurrentContext, miss, normalizeRouteRecord, reroute, setCurrentContext, toLazyValue, trackRoute, useIsDataLoading, withLoaderContext };