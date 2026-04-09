/*!
 * vue-router v5.0.4
 * (c) 2026 Eduardo San Martin Morote
 * @license MIT
 */
import { AllowedComponentProps, AnchorHTMLAttributes, App, Component as Component$1, ComponentCustomProps, ComponentPublicInstance, ComputedRef, DefineComponent, InjectionKey, MaybeRef, Ref, ShallowRef, UnwrapRef, VNode, VNodeProps } from "vue";

//#region src/config.d.ts
/**
 * Allows customizing existing types of the router that are used globally like `$router`, `<RouterLink>`, etc. **ONLY FOR INTERNAL USAGE**.
 *
 * - `$router` - the router instance
 * - `$route` - the current route location
 * - `beforeRouteEnter` - Page component option
 * - `beforeRouteUpdate` - Page component option
 * - `beforeRouteLeave` - Page component option
 * - `RouterLink` - RouterLink Component
 * - `RouterView` - RouterView Component
 *
 * @internal
 */
interface TypesConfig {}
//#endregion
//#region src/query.d.ts
/**
 * Possible values in normalized {@link LocationQuery}. `null` renders the query
 * param but without an `=`.
 *
 * @example
 * ```
 * ?isNull&isEmpty=&other=other
 * gives
 * `{ isNull: null, isEmpty: '', other: 'other' }`.
 * ```
 *
 * @internal
 */
type LocationQueryValue = string | null;
/**
 * Possible values when defining a query. `undefined` allows to remove a value.
 *
 * @internal
 */
type LocationQueryValueRaw = LocationQueryValue | number | undefined;
/**
 * Normalized query object that appears in {@link RouteLocationNormalized}
 *
 * @public
 */
type LocationQuery = Record<string, LocationQueryValue | LocationQueryValue[]>;
/**
 * Loose {@link LocationQuery} object that can be passed to functions like
 * {@link Router.push} and {@link Router.replace} or anywhere when creating a
 * {@link RouteLocationRaw}
 *
 * @public
 */
type LocationQueryRaw = Record<string | number, LocationQueryValueRaw | LocationQueryValueRaw[]>;
/**
 * Transforms a queryString into a {@link LocationQuery} object. Accept both, a
 * version with the leading `?` and without Should work as URLSearchParams

 * @internal
 *
 * @param search - search string to parse
 * @returns a query object
 */
declare function parseQuery(search: string): LocationQuery;
/**
 * Stringifies a {@link LocationQueryRaw} object. Like `URLSearchParams`, it
 * doesn't prepend a `?`
 *
 * @internal
 *
 * @param query - query object to stringify
 * @returns string version of the query without the leading `?`
 */
declare function stringifyQuery(query: LocationQueryRaw | undefined): string;
//#endregion
//#region src/matcher/types.d.ts
/**
 * Normalized version of a {@link RouteRecord | route record}.
 */
interface RouteRecordNormalized {
  /**
   * {@inheritDoc _RouteRecordBase.path}
   */
  path: _RouteRecordBase['path'];
  /**
   * {@inheritDoc _RouteRecordBase.redirect}
   */
  redirect: _RouteRecordBase['redirect'] | undefined;
  /**
   * {@inheritDoc _RouteRecordBase.name}
   */
  name: _RouteRecordBase['name'];
  /**
   * {@inheritDoc RouteRecordMultipleViews.components}
   */
  components: RouteRecordMultipleViews['components'] | null | undefined;
  /**
   * Contains the original modules for lazy loaded components.
   * @internal
   */
  mods: Record<string, unknown>;
  /**
   * Nested route records.
   */
  children: RouteRecordRaw[];
  /**
   * {@inheritDoc _RouteRecordBase.meta}
   */
  meta: Exclude<_RouteRecordBase['meta'], void>;
  /**
   * {@inheritDoc RouteRecordMultipleViews.props}
   */
  props: Record<string, _RouteRecordProps>;
  /**
   * Registered beforeEnter guards
   */
  beforeEnter: _RouteRecordBase['beforeEnter'];
  /**
   * Registered leave guards
   *
   * @internal
   */
  leaveGuards: Set<NavigationGuard>;
  /**
   * Registered update guards
   *
   * @internal
   */
  updateGuards: Set<NavigationGuard>;
  /**
   * Registered beforeRouteEnter callbacks passed to `next` or returned in guards
   *
   * @internal
   */
  enterCallbacks: Record<string, NavigationGuardNextCallback[]>;
  /**
   * Mounted route component instances
   * Having the instances on the record mean beforeRouteUpdate and
   * beforeRouteLeave guards can only be invoked with the latest mounted app
   * instance if there are multiple application instances rendering the same
   * view, basically duplicating the content on the page, which shouldn't happen
   * in practice. It will work if multiple apps are rendering different named
   * views.
   */
  instances: Record<string, ComponentPublicInstance | undefined | null>;
  /**
   * Defines if this record is the alias of another one. This property is
   * `undefined` if the record is the original one.
   */
  aliasOf: RouteRecordNormalized | undefined;
}
/**
 * {@inheritDoc RouteRecordNormalized}
 */
type RouteRecord = RouteRecordNormalized;
//#endregion
//#region src/matcher/pathParserRanker.d.ts
type PathParams = Record<string, string | string[]>;
/**
 * A param in a url like `/users/:id`
 */
interface PathParserParamKey {
  name: string;
  repeatable: boolean;
  optional: boolean;
}
interface PathParser {
  /**
   * The regexp used to match a url
   */
  re: RegExp;
  /**
   * The score of the parser
   */
  score: Array<number[]>;
  /**
   * Keys that appeared in the path
   */
  keys: PathParserParamKey[];
  /**
   * Parses a url and returns the matched params or null if it doesn't match. An
   * optional param that isn't preset will be an empty string. A repeatable
   * param will be an array if there is at least one value.
   *
   * @param path - url to parse
   * @returns a Params object, empty if there are no params. `null` if there is
   * no match
   */
  parse(path: string): PathParams | null;
  /**
   * Creates a string version of the url
   *
   * @param params - object of params
   * @returns a url
   */
  stringify(params: PathParams): string;
}
/**
 * @internal
 */
interface _PathParserOptions {
  /**
   * Makes the RegExp case-sensitive.
   *
   * @defaultValue `false`
   */
  sensitive?: boolean;
  /**
   * Whether to disallow a trailing slash or not.
   *
   * @defaultValue `false`
   */
  strict?: boolean;
  /**
   * Should the RegExp match from the beginning by prepending a `^` to it.
   * @internal
   *
   * @defaultValue `true`
   */
  start?: boolean;
  /**
   * Should the RegExp match until the end by appending a `$` to it.
   *
   * @deprecated this option will alsways be `true` in the future. Open a discussion in vuejs/router if you need this to be `false`
   *
   * @defaultValue `true`
   */
  end?: boolean;
}
type PathParserOptions = Pick<_PathParserOptions, 'end' | 'sensitive' | 'strict'>;
//#endregion
//#region src/matcher/pathMatcher.d.ts
interface RouteRecordMatcher extends PathParser {
  record: RouteRecord;
  parent: RouteRecordMatcher | undefined;
  children: RouteRecordMatcher[];
  alias: RouteRecordMatcher[];
}
//#endregion
//#region src/matcher/index.d.ts
/**
 * Internal RouterMatcher
 *
 * @internal
 */
interface RouterMatcher {
  addRoute: (record: RouteRecordRaw, parent?: RouteRecordMatcher) => () => void;
  removeRoute(matcher: RouteRecordMatcher): void;
  removeRoute(name: NonNullable<RouteRecordNameGeneric>): void;
  clearRoutes: () => void;
  getRoutes: () => RouteRecordMatcher[];
  getRecordMatcher: (name: NonNullable<RouteRecordNameGeneric>) => RouteRecordMatcher | undefined;
  /**
   * Resolves a location. Gives access to the route record that corresponds to the actual path as well as filling the corresponding params objects
   *
   * @param location - MatcherLocationRaw to resolve to a url
   * @param currentLocation - MatcherLocation of the current location
   */
  resolve: (location: MatcherLocationRaw, currentLocation: MatcherLocation) => MatcherLocation;
}
/**
 * Creates a Router Matcher.
 *
 * @internal
 * @param routes - array of initial routes
 * @param globalOptions - global route options
 */
declare function createRouterMatcher(routes: Readonly<RouteRecordRaw[]>, globalOptions: PathParserOptions): RouterMatcher;
//#endregion
//#region src/history/common.d.ts
type HistoryLocation = string;
/**
 * Allowed variables in HTML5 history state. Note that pushState clones the state
 * passed and does not accept everything: e.g.: it doesn't accept symbols, nor
 * functions as values. It also ignores Symbols as keys.
 *
 * @internal
 */
type HistoryStateValue = string | number | boolean | null | undefined | HistoryState | HistoryStateArray;
/**
 * Allowed HTML history.state
 */
interface HistoryState {
  [x: number]: HistoryStateValue;
  [x: string]: HistoryStateValue;
}
/**
 * Allowed arrays for history.state.
 *
 * @internal
 */
interface HistoryStateArray extends Array<HistoryStateValue> {}
declare enum NavigationType {
  pop = "pop",
  push = "push"
}
declare enum NavigationDirection {
  back = "back",
  forward = "forward",
  unknown = ""
}
interface NavigationInformation {
  type: NavigationType;
  direction: NavigationDirection;
  delta: number;
}
interface NavigationCallback {
  (to: HistoryLocation, from: HistoryLocation, information: NavigationInformation): void;
}
/**
 * Interface implemented by History implementations that can be passed to the
 * router as {@link Router.history}
 *
 * @alpha
 */
interface RouterHistory {
  /**
   * Base path that is prepended to every url. This allows hosting an SPA at a
   * sub-folder of a domain like `example.com/sub-folder` by having a `base` of
   * `/sub-folder`
   */
  readonly base: string;
  /**
   * Current History location
   */
  readonly location: HistoryLocation;
  /**
   * Current History state
   */
  readonly state: HistoryState;
  /**
   * Navigates to a location. In the case of an HTML5 History implementation,
   * this will call `history.pushState` to effectively change the URL.
   *
   * @param to - location to push
   * @param data - optional {@link HistoryState} to be associated with the
   * navigation entry
   */
  push(to: HistoryLocation, data?: HistoryState): void;
  /**
   * Same as {@link RouterHistory.push} but performs a `history.replaceState`
   * instead of `history.pushState`
   *
   * @param to - location to set
   * @param data - optional {@link HistoryState} to be associated with the
   * navigation entry
   */
  replace(to: HistoryLocation, data?: HistoryState): void;
  /**
   * Traverses history in a given direction.
   *
   * @example
   * ```js
   * myHistory.go(-1) // equivalent to window.history.back()
   * myHistory.go(1) // equivalent to window.history.forward()
   * ```
   *
   * @param delta - distance to travel. If delta is \< 0, it will go back,
   * if it's \> 0, it will go forward by that amount of entries.
   * @param triggerListeners - whether this should trigger listeners attached to
   * the history
   */
  go(delta: number, triggerListeners?: boolean): void;
  /**
   * Attach a listener to the History implementation that is triggered when the
   * navigation is triggered from outside (like the Browser back and forward
   * buttons) or when passing `true` to {@link RouterHistory.back} and
   * {@link RouterHistory.forward}
   *
   * @param callback - listener to attach
   * @returns a callback to remove the listener
   */
  listen(callback: NavigationCallback): () => void;
  /**
   * Generates the corresponding href to be used in an anchor tag.
   *
   * @param location - history location that should create an href
   */
  createHref(location: HistoryLocation): string;
  /**
   * Clears any event listener attached by the history implementation.
   */
  destroy(): void;
}
//#endregion
//#region src/types/index.d.ts
type Lazy<T> = () => Promise<T>;
/**
 * @internal
 */
type RouteParamValue = string;
/**
 * @internal
 */
type RouteParamValueRaw = RouteParamValue | number | null | undefined;
type RouteParamsGeneric = Record<string, RouteParamValue | RouteParamValue[]>;
type RouteParamsRawGeneric = Record<string, RouteParamValueRaw | Exclude<RouteParamValueRaw, null | undefined>[]>;
/**
 * @internal
 */
interface RouteQueryAndHash {
  query?: LocationQueryRaw;
  hash?: string;
}
/**
 * @internal
 */
interface MatcherLocationAsPath {
  path: string;
}
/**
 * @internal
 */
interface MatcherLocationAsName {
  name: RouteRecordNameGeneric;
  /**
   * Ignored path property since we are dealing with a relative location. Only `undefined` is allowed.
   */
  path?: undefined;
  params?: RouteParamsGeneric;
}
/**
 * @internal
 */
interface MatcherLocationAsRelative {
  /**
   * Ignored path property since we are dealing with a relative location. Only `undefined` is allowed.
   */
  path?: undefined;
  params?: RouteParamsGeneric;
}
/**
 * @internal
 */
interface LocationAsRelativeRaw {
  name?: RouteRecordNameGeneric;
  /**
   * Ignored path property since we are dealing with a relative location. Only `undefined` is allowed.
   */
  path?: undefined;
  params?: RouteParamsRawGeneric;
}
/**
 * Common options for all navigation methods.
 */
interface RouteLocationOptions {
  /**
   * Replace the entry in the history instead of pushing a new entry
   */
  replace?: boolean;
  /**
   * Triggers the navigation even if the location is the same as the current one.
   * Note this will also add a new entry to the history unless `replace: true`
   * is passed.
   */
  force?: boolean;
  /**
   * State to save using the History API. This cannot contain any reactive
   * values and some primitives like Symbols are forbidden. More info at
   * https://developer.mozilla.org/en-US/docs/Web/API/History/state
   */
  state?: HistoryState;
}
/**
 * Route Location that can infer the necessary params based on the name.
 *
 * @internal
 */
interface RouteLocationNamedRaw extends RouteQueryAndHash, LocationAsRelativeRaw, RouteLocationOptions {}
/**
 * Route Location that can infer the possible paths.
 *
 * @internal
 */
interface RouteLocationPathRaw extends RouteQueryAndHash, MatcherLocationAsPath, RouteLocationOptions {}
interface RouteLocationMatched extends RouteRecordNormalized {
  components: Record<string, RouteComponent> | null | undefined;
}
/**
 * Base properties for a normalized route location.
 *
 * @internal
 */
interface _RouteLocationBase extends Pick<MatcherLocation, 'name' | 'path' | 'params' | 'meta'> {
  /**
   * The whole location including the `search` and `hash`. This string is
   * percentage encoded.
   */
  fullPath: string;
  /**
   * Object representation of the `search` property of the current location.
   */
  query: LocationQuery;
  /**
   * Hash of the current location. If present, starts with a `#`.
   */
  hash: string;
  /**
   * Contains the location we were initially trying to access before ending up
   * on the current location.
   */
  redirectedFrom: RouteLocation | undefined;
}
/**
 * Allowed Component in {@link RouteLocationMatched}
 */
type RouteComponent = Component$1 | DefineComponent;
/**
 * Allowed Component definitions in route records provided by the user
 */
type RawRouteComponent = RouteComponent | Lazy<RouteComponent>;
/**
 * Internal type for common properties among all kind of {@link RouteRecordRaw}.
 */
interface _RouteRecordBase extends PathParserOptions {
  /**
   * Path of the record. Should start with `/` unless the record is the child of
   * another record.
   *
   * @example `/users/:id` matches `/users/1` as well as `/users/posva`.
   */
  path: string;
  /**
   * Where to redirect if the route is directly matched. The redirection happens
   * before any navigation guard and triggers a new navigation with the new
   * target location.
   */
  redirect?: RouteRecordRedirectOption;
  /**
   * Aliases for the record. Allows defining extra paths that will behave like a
   * copy of the record. Allows having paths shorthands like `/users/:id` and
   * `/u/:id`. All `alias` and `path` values must share the same params.
   */
  alias?: string | string[];
  /**
   * Name for the route record. Must be unique.
   */
  name?: RouteRecordNameGeneric;
  /**
   * Before Enter guard specific to this record. Note `beforeEnter` has no
   * effect if the record has a `redirect` property.
   */
  beforeEnter?: NavigationGuardWithThis<undefined> | NavigationGuardWithThis<undefined>[];
  /**
   * Arbitrary data attached to the record.
   */
  meta?: RouteMeta;
  /**
   * Array of nested routes.
   */
  children?: RouteRecordRaw[];
  /**
   * Allow passing down params as props to the component rendered by `router-view`.
   */
  props?: _RouteRecordProps | Record<string, _RouteRecordProps>;
}
/**
 * Interface to type `meta` fields in route records.
 *
 * @example
 *
 * ```ts
 * // typings.d.ts or router.ts
 * import 'vue-router';
 *
 * declare module 'vue-router' {
 *   interface RouteMeta {
 *     requiresAuth?: boolean
 *   }
 * }
 * ```
 */
interface RouteMeta extends Record<PropertyKey, unknown> {}
/**
 * Route Record defining one single component with the `component` option.
 */
interface RouteRecordSingleView extends _RouteRecordBase {
  /**
   * Component to display when the URL matches this route.
   */
  component: RawRouteComponent;
  components?: never;
  children?: never;
  redirect?: never;
  /**
   * Allow passing down params as props to the component rendered by `router-view`.
   */
  props?: _RouteRecordProps;
}
/**
 * Route Record defining one single component with a nested view. Differently
 * from {@link RouteRecordSingleView}, this record has children and allows a
 * `redirect` option.
 */
interface RouteRecordSingleViewWithChildren extends _RouteRecordBase {
  /**
   * Component to display when the URL matches this route.
   */
  component?: RawRouteComponent | null | undefined;
  components?: never;
  children: RouteRecordRaw[];
  /**
   * Allow passing down params as props to the component rendered by `router-view`.
   */
  props?: _RouteRecordProps;
}
/**
 * Route Record defining multiple named components with the `components` option.
 */
interface RouteRecordMultipleViews extends _RouteRecordBase {
  /**
   * Components to display when the URL matches this route. Allow using named views.
   */
  components: Record<string, RawRouteComponent>;
  component?: never;
  children?: never;
  redirect?: never;
  /**
   * Allow passing down params as props to the component rendered by
   * `router-view`. Should be an object with the same keys as `components` or a
   * boolean to be applied to every component.
   */
  props?: Record<string, _RouteRecordProps> | boolean;
}
/**
 * Route Record defining multiple named components with the `components` option and children.
 */
interface RouteRecordMultipleViewsWithChildren extends _RouteRecordBase {
  /**
   * Components to display when the URL matches this route. Allow using named views.
   */
  components?: Record<string, RawRouteComponent> | null | undefined;
  component?: never;
  children: RouteRecordRaw[];
  /**
   * Allow passing down params as props to the component rendered by
   * `router-view`. Should be an object with the same keys as `components` or a
   * boolean to be applied to every component.
   */
  props?: Record<string, _RouteRecordProps> | boolean;
}
/**
 * Route Record that defines a redirect. Cannot have `component` or `components`
 * as it is never rendered.
 */
interface RouteRecordRedirect extends _RouteRecordBase {
  redirect: RouteRecordRedirectOption;
  component?: never;
  components?: never;
  props?: never;
}
type RouteRecordRaw = RouteRecordSingleView | RouteRecordSingleViewWithChildren | RouteRecordMultipleViews | RouteRecordMultipleViewsWithChildren | RouteRecordRedirect;
/**
 * Route location that can be passed to the matcher.
 */
type MatcherLocationRaw = MatcherLocationAsPath | MatcherLocationAsName | MatcherLocationAsRelative;
/**
 * Normalized/resolved Route location that returned by the matcher.
 */
interface MatcherLocation {
  /**
   * Name of the matched record
   */
  name: RouteRecordNameGeneric | null | undefined;
  /**
   * Percentage encoded pathname section of the URL.
   */
  path: string;
  /**
   * Object of decoded params extracted from the `path`.
   */
  params: RouteParamsGeneric;
  /**
   * Merged `meta` properties from all the matched route records.
   */
  meta: RouteMeta;
  /**
   * Array of {@link RouteRecord} containing components as they were
   * passed when adding records. It can also contain redirect records. This
   * can't be used directly
   */
  matched: RouteRecord[];
}
//#endregion
//#region src/typed-routes/route-map.d.ts
/**
 * Helper type to define a Typed `RouteRecord`
 * @see {@link RouteRecord}
 */
interface RouteRecordInfo<Name extends string | symbol = string, Path extends string = string, ParamsRaw extends RouteParamsRawGeneric = RouteParamsRawGeneric, Params extends RouteParamsGeneric = RouteParamsGeneric, ChildrenNames extends string | symbol = never> {
  name: Name;
  path: Path;
  paramsRaw: ParamsRaw;
  params: Params;
  childrenNames: ChildrenNames;
}
type RouteRecordInfoGeneric = RouteRecordInfo<string | symbol, string, RouteParamsRawGeneric, RouteParamsGeneric, string | symbol>;
/**
 * Convenience type to get the typed RouteMap or a generic one if not provided.
 * It is extracted from the {@link TypesConfig} if it exists, it becomes
 * {@link RouteMapGeneric} otherwise.
 */
type RouteMap = TypesConfig extends Record<'RouteNamedMap', infer RouteNamedMap> ? RouteNamedMap : RouteMapGeneric;
/**
 * Generic version of the `RouteMap`.
 */
type RouteMapGeneric = Record<string | symbol, RouteRecordInfoGeneric>;
//#endregion
//#region src/typed-routes/params.d.ts
/**
 * Utility type for raw and non raw params like :id+
 *
 */
type ParamValueOneOrMore<isRaw extends boolean> = [ParamValue<isRaw>, ...ParamValue<isRaw>[]];
/**
 * Utility type for raw and non raw params like :id*
 *
 */
type ParamValueZeroOrMore<isRaw extends boolean> = true extends isRaw ? ParamValue<isRaw>[] | undefined | null : ParamValue<isRaw>[] | undefined;
/**
 * Utility type for raw and non raw params like :id?
 *
 */
type ParamValueZeroOrOne<isRaw extends boolean> = true extends isRaw ? string | number | null | undefined : string;
/**
 * Utility type for raw and non raw params like :id
 *
 */
type ParamValue<isRaw extends boolean> = true extends isRaw ? string | number : string;
/**
 * Generate a type safe params for a route location. Requires the name of the route to be passed as a generic.
 * @see {@link RouteParamsGeneric}
 */
type RouteParams<Name extends keyof RouteMap = keyof RouteMap> = RouteMap[Name]['params'];
/**
 * Generate a type safe raw params for a route location. Requires the name of the route to be passed as a generic.
 * @see {@link RouteParamsRaw}
 */
type RouteParamsRaw<Name extends keyof RouteMap = keyof RouteMap> = RouteMap[Name]['paramsRaw'];
//#endregion
//#region src/types/utils.d.ts
/**
 * Creates a union type that still allows autocompletion for strings.
 * @internal
 */
type _LiteralUnion<LiteralType, BaseType extends string = string> = LiteralType | (BaseType & Record<never, never>);
/**
 * Maybe a promise maybe not
 * @internal
 */
type _Awaitable<T> = T | PromiseLike<T>;
/**
 * @internal
 */
type Simplify<T> = { [K in keyof T]: T[K] } & {};
//#endregion
//#region src/typed-routes/route-records.d.ts
/**
 * @internal
 */
type RouteRecordRedirectOption = RouteLocationRaw | ((to: RouteLocation, from: RouteLocationNormalizedLoaded) => RouteLocationRaw);
/**
 * Generic version of {@link RouteRecordName}.
 */
type RouteRecordNameGeneric = string | symbol | undefined;
/**
 * Possible values for a route record **after normalization**
 *
 * NOTE: since `RouteRecordName` is a type, it evaluates too early and it's often the generic version {@link RouteRecordNameGeneric}. If you need a typed version of all of the names of routes, use {@link RouteMap | `keyof RouteMap`}
 */
type RouteRecordName = RouteMapGeneric extends RouteMap ? RouteRecordNameGeneric : keyof RouteMap;
/**
 * @internal
 */
type _RouteRecordProps<Name extends keyof RouteMap = keyof RouteMap> = boolean | Record<string, any> | ((to: RouteLocationNormalized<Name>) => Record<string, any>);
//#endregion
//#region src/typed-routes/route-location.d.ts
/**
 * Generic version of {@link RouteLocation}. It is used when no {@link RouteMap} is provided.
 */
interface RouteLocationGeneric extends _RouteLocationBase, RouteLocationOptions {
  /**
   * Array of {@link RouteRecord} containing components as they were
   * passed when adding records. It can also contain redirect records. This
   * can't be used directly. **This property is non-enumerable**.
   */
  matched: RouteRecord[];
}
/**
 * Helper to generate a type safe version of the {@link RouteLocation} type.
 */
interface RouteLocationTyped<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric }, Name extends keyof RouteMap> extends RouteLocationGeneric {
  name: Extract<Name, string | symbol>;
  params: RouteMap[Name]['params'];
}
/**
 * List of all possible {@link RouteLocation} indexed by the route name.
 * @internal
 */
type RouteLocationTypedList<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationTyped<RouteMap, N> };
/**
 * Generic version of {@link RouteLocationNormalized} that is used when no {@link RouteMap} is provided.
 */
interface RouteLocationNormalizedGeneric extends _RouteLocationBase {
  name: RouteRecordNameGeneric;
  /**
   * Array of {@link RouteRecordNormalized}
   */
  matched: RouteRecordNormalized[];
}
/**
 * Helper to generate a type safe version of the {@link RouteLocationNormalized} type.
 */
interface RouteLocationNormalizedTyped<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric, Name extends keyof RouteMap = keyof RouteMap> extends RouteLocationNormalizedGeneric {
  name: Extract<Name, string | symbol>;
  params: RouteMap[Name]['params'];
  /**
   * Array of {@link RouteRecordNormalized}
   */
  matched: RouteRecordNormalized[];
}
/**
 * List of all possible {@link RouteLocationNormalized} indexed by the route name.
 * @internal
 */
type RouteLocationNormalizedTypedList<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationNormalizedTyped<RouteMap, N> };
/**
 * Generic version of {@link RouteLocationNormalizedLoaded} that is used when no {@link RouteMap} is provided.
 */
interface RouteLocationNormalizedLoadedGeneric extends RouteLocationNormalizedGeneric {
  /**
   * Array of {@link RouteLocationMatched} containing only plain components (any
   * lazy-loaded components have been loaded and were replaced inside the
   * `components` object) so it can be directly used to display routes. It
   * cannot contain redirect records either. **This property is non-enumerable**.
   */
  matched: RouteLocationMatched[];
}
/**
 * Helper to generate a type safe version of the {@link RouteLocationNormalizedLoaded} type.
 */
interface RouteLocationNormalizedLoadedTyped<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric, Name extends keyof RouteMap = keyof RouteMap> extends RouteLocationNormalizedLoadedGeneric {
  name: Extract<Name, string | symbol>;
  params: RouteMap[Name]['params'];
}
/**
 * List of all possible {@link RouteLocationNormalizedLoaded} indexed by the route name.
 * @internal
 */
type RouteLocationNormalizedLoadedTypedList<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationNormalizedLoadedTyped<RouteMap, N> };
/**
 * Generic version of {@link RouteLocationAsRelative}. It is used when no {@link RouteMap} is provided.
 */
interface RouteLocationAsRelativeGeneric extends RouteQueryAndHash, RouteLocationOptions {
  name?: RouteRecordNameGeneric;
  params?: RouteParamsRawGeneric;
  /**
   * A relative path to the current location. This property should be removed
   */
  path?: undefined;
}
/**
 * Helper to generate a type safe version of the {@link RouteLocationAsRelative} type.
 */
interface RouteLocationAsRelativeTyped<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric, Name extends keyof RouteMap = keyof RouteMap> extends RouteLocationAsRelativeGeneric {
  name?: Extract<Name, string | symbol>;
  params?: RouteMap[Name]['paramsRaw'];
}
/**
 * List of all possible {@link RouteLocationAsRelative} indexed by the route name.
 * @internal
 */
type RouteLocationAsRelativeTypedList<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationAsRelativeTyped<RouteMap, N> };
/**
 * Generic version of {@link RouteLocationAsPath}. It is used when no {@link RouteMap} is provided.
 */
interface RouteLocationAsPathGeneric extends RouteQueryAndHash, RouteLocationOptions {
  /**
   * Percentage encoded pathname section of the URL.
   */
  path: string;
}
/**
 * Helper to generate a type safe version of the {@link RouteLocationAsPath} type.
 */
interface RouteLocationAsPathTyped<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric, Name extends keyof RouteMap = keyof RouteMap> extends RouteLocationAsPathGeneric {
  path: _LiteralUnion<RouteMap[Name]['path']>;
}
/**
 * List of all possible {@link RouteLocationAsPath} indexed by the route name.
 * @internal
 */
type RouteLocationAsPathTypedList<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationAsPathTyped<RouteMap, N> };
/**
 * Helper to generate a type safe version of the {@link RouteLocationAsString} type.
 */
type RouteLocationAsStringTyped<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric, Name extends keyof RouteMap = keyof RouteMap> = RouteMap[Name]['path'];
/**
 * List of all possible {@link RouteLocationAsString} indexed by the route name.
 * @internal
 */
type RouteLocationAsStringTypedList<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationAsStringTyped<RouteMap, N> };
/**
 * Generic version of {@link RouteLocationResolved}. It is used when no {@link RouteMap} is provided.
 */
interface RouteLocationResolvedGeneric extends RouteLocationGeneric {
  /**
   * Resolved `href` for the route location that will be set on the `<a href="...">`.
   */
  href: string;
}
/**
 * Helper to generate a type safe version of the {@link RouteLocationResolved} type.
 */
interface RouteLocationResolvedTyped<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric }, Name extends keyof RouteMap> extends RouteLocationTyped<RouteMap, Name> {
  /**
   * Resolved `href` for the route location that will be set on the `<a href="...">`.
   */
  href: string;
}
/**
 * List of all possible {@link RouteLocationResolved} indexed by the route name.
 * @internal
 */
type RouteLocationResolvedTypedList<RouteMap extends { [K in keyof RouteMap]: RouteRecordInfoGeneric } = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationResolvedTyped<RouteMap, N> };
/**
 * Type safe versions of types that are exposed by vue-router. We have to use a generic check to allow for names to be `undefined` when no `RouteMap` is provided.
 */
/**
 * {@link RouteLocationRaw} resolved using the matcher
 */
type RouteLocation<Name extends keyof RouteMap = keyof RouteMap> = RouteMapGeneric extends RouteMap ? RouteLocationGeneric : RouteLocationTypedList<RouteMap>[Name];
/**
 * Similar to {@link RouteLocation} but its
 * {@link RouteLocationNormalizedTyped.matched | `matched` property} cannot contain redirect records
 */
type RouteLocationNormalized<Name extends keyof RouteMap = keyof RouteMap> = RouteMapGeneric extends RouteMap ? RouteLocationNormalizedGeneric : RouteLocationNormalizedTypedList<RouteMap>[Name];
/**
 * Similar to {@link RouteLocationNormalized} but its `components` do not contain any function to lazy load components.
 * In other words, it's ready to be rendered by `<RouterView>`.
 */
type RouteLocationNormalizedLoaded<Name extends keyof RouteMap = keyof RouteMap> = RouteMapGeneric extends RouteMap ? RouteLocationNormalizedLoadedGeneric : RouteLocationNormalizedLoadedTypedList<RouteMap>[Name];
/**
 * Route location relative to the current location. It accepts other properties than `path` like `params`, `query` and
 * `hash` to conveniently change them.
 */
type RouteLocationAsRelative<Name extends keyof RouteMap = keyof RouteMap> = RouteMapGeneric extends RouteMap ? RouteLocationAsRelativeGeneric : RouteLocationAsRelativeTypedList<RouteMap>[Name];
/**
 * Route location resolved with {@link Router | `router.resolve()`}.
 */
type RouteLocationResolved<Name extends keyof RouteMap = keyof RouteMap> = RouteMapGeneric extends RouteMap ? RouteLocationResolvedGeneric : RouteLocationResolvedTypedList<RouteMap>[Name];
/**
 * Same as {@link RouteLocationAsPath} but as a string literal.
 */
type RouteLocationAsString<Name extends keyof RouteMap = keyof RouteMap> = RouteMapGeneric extends RouteMap ? string : _LiteralUnion<RouteLocationAsStringTypedList<RouteMap>[Name], string>;
/**
 * Route location as an object with a `path` property.
 */
type RouteLocationAsPath<Name extends keyof RouteMap = keyof RouteMap> = RouteMapGeneric extends RouteMap ? RouteLocationAsPathGeneric : RouteLocationAsPathTypedList<RouteMap>[Name];
/**
 * Route location that can be passed to `router.push()` and other user-facing APIs.
 */
type RouteLocationRaw<Name extends keyof RouteMap = keyof RouteMap> = RouteMapGeneric extends RouteMap ? RouteLocationAsString | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric : _LiteralUnion<RouteLocationAsStringTypedList<RouteMap>[Name], string> | RouteLocationAsRelativeTypedList<RouteMap>[Name] | RouteLocationAsPathTypedList<RouteMap>[Name];
//#endregion
//#region src/errors.d.ts
/**
 * Flags so we can combine them when checking for multiple errors. This is the internal version of
 * {@link NavigationFailureType}.
 *
 * @internal
 */
declare const enum ErrorTypes {
  MATCHER_NOT_FOUND = 1,
  NAVIGATION_GUARD_REDIRECT = 2,
  NAVIGATION_ABORTED = 4,
  NAVIGATION_CANCELLED = 8,
  NAVIGATION_DUPLICATED = 16
}
/**
 * Enumeration with all possible types for navigation failures. Can be passed to
 * {@link isNavigationFailure} to check for specific failures.
 */
declare enum NavigationFailureType {
  /**
   * An aborted navigation is a navigation that failed because a navigation
   * guard returned `false` or called `next(false)`
   */
  aborted = 4,
  /**
   * A cancelled navigation is a navigation that failed because a more recent
   * navigation finished started (not necessarily finished).
   */
  cancelled = 8,
  /**
   * A duplicated navigation is a navigation that failed because it was
   * initiated while already being at the exact same location.
   */
  duplicated = 16
}
/**
 * Extended Error that contains extra information regarding a failed navigation.
 */
interface NavigationFailure extends Error {
  /**
   * Type of the navigation. One of {@link NavigationFailureType}
   */
  type: ErrorTypes.NAVIGATION_CANCELLED | ErrorTypes.NAVIGATION_ABORTED | ErrorTypes.NAVIGATION_DUPLICATED;
  /**
   * Route location we were navigating from
   */
  from: RouteLocationNormalized;
  /**
   * Route location we were navigating to
   */
  to: RouteLocationNormalized;
}
/**
 * Internal error used to detect a redirection.
 *
 * @internal
 */
interface NavigationRedirectError extends Omit<NavigationFailure, 'to' | 'type'> {
  type: ErrorTypes.NAVIGATION_GUARD_REDIRECT;
  to: RouteLocationRaw;
}
/**
 * Check if an object is a {@link NavigationFailure}.
 *
 * @param error - possible {@link NavigationFailure}
 * @param type - optional types to check for
 *
 * @example
 * ```js
 * import { isNavigationFailure, NavigationFailureType } from 'vue-router'
 *
 * router.afterEach((to, from, failure) => {
 *   // Any kind of navigation failure
 *   if (isNavigationFailure(failure)) {
 *     // ...
 *   }
 *   // Only duplicated navigations
 *   if (isNavigationFailure(failure, NavigationFailureType.duplicated)) {
 *     // ...
 *   }
 *   // Aborted or canceled navigations
 *   if (isNavigationFailure(failure, NavigationFailureType.aborted | NavigationFailureType.cancelled )) {
 *     // ...
 *   }
 * })
 * ```
 */
declare function isNavigationFailure(error: any, type?: ErrorTypes.NAVIGATION_GUARD_REDIRECT): error is NavigationRedirectError;
declare function isNavigationFailure(error: any, type?: ErrorTypes | NavigationFailureType): error is NavigationFailure;
/**
 * Internal type to define an ErrorHandler
 *
 * @param error - error thrown
 * @param to - location we were navigating to when the error happened
 * @param from - location we were navigating from when the error happened
 * @internal
 */
interface _ErrorListener {
  (error: any, to: RouteLocationNormalized, from: RouteLocationNormalizedLoaded): any;
}
//#endregion
//#region src/typed-routes/navigation-guards.d.ts
/**
 * Return types for a Navigation Guard. Based on `TypesConfig`
 *
 * @see {@link TypesConfig}
 */
type NavigationGuardReturn = void | Error | boolean | RouteLocationRaw;
/**
 * Navigation Guard with a type parameter for `this`.
 * @see {@link TypesConfig}
 */
interface NavigationGuardWithThis<T> {
  (this: T, to: RouteLocationNormalized, from: RouteLocationNormalizedLoaded,
  /**
   * @deprecated Return a value from the guard instead of calling `next(value)`.
   * The callback will be removed in a future version of Vue Router.
   */

  next: NavigationGuardNext): _Awaitable<NavigationGuardReturn>;
}
/**
 * In `router.beforeResolve((to) => {})`, the `to` is typed as `RouteLocationNormalizedLoaded`, not
 * `RouteLocationNormalized` like in `router.beforeEach()`. In practice it doesn't change much as users do not rely on
 * the difference between them but if we update the type in vue-router, we will have to update this type too.
 * @internal
 */
interface _NavigationGuardResolved {
  (this: undefined, to: RouteLocationNormalizedLoaded, from: RouteLocationNormalizedLoaded,
  /**
   * @deprecated Return a value from the guard instead of calling `next(value)`.
   * The callback will be removed in a future version of Vue Router.
   */

  next: NavigationGuardNext): _Awaitable<NavigationGuardReturn>;
}
/**
 * Navigation Guard.
 */
interface NavigationGuard {
  (to: RouteLocationNormalized, from: RouteLocationNormalizedLoaded,
  /**
   * @deprecated Return a value from the guard instead of calling `next(value)`.
   * The callback will be removed in a future version of Vue Router.
   */

  next: NavigationGuardNext): _Awaitable<NavigationGuardReturn>;
}
/**
 * Navigation hook triggered after a navigation is settled.
 */
interface NavigationHookAfter {
  (to: RouteLocationNormalizedLoaded, from: RouteLocationNormalizedLoaded, failure?: NavigationFailure | void): unknown;
}
/**
 * Callback passed to navigation guards to continue or abort the navigation.
 *
 * @deprecated Prefer returning a value from the guard instead of calling
 * `next(value)`. The callback will be removed in a future version of Vue Router.
 */
interface NavigationGuardNext {
  (): void;
  (error: Error): void;
  (location: RouteLocationRaw): void;
  (valid: boolean | undefined): void;
  (cb: NavigationGuardNextCallback): void;
}
/**
 * Callback that can be passed to `next()` in `beforeRouteEnter()` guards.
 */
type NavigationGuardNextCallback = (vm: ComponentPublicInstance) => unknown;
//#endregion
//#region src/history/html5.d.ts
/**
 * Creates an HTML5 history. Most common history for single page applications.
 *
 * @param base -
 */
declare function createWebHistory(base?: string): RouterHistory;
//#endregion
//#region src/history/memory.d.ts
/**
 * Creates an in-memory based history. The main purpose of this history is to handle SSR. It starts in a special location that is nowhere.
 * It's up to the user to replace that location with the starter location by either calling `router.push` or `router.replace`.
 *
 * @param base - Base applied to all urls, defaults to '/'
 * @returns a history object that can be passed to the router constructor
 */
declare function createMemoryHistory(base?: string): RouterHistory;
//#endregion
//#region src/history/hash.d.ts
/**
 * Creates a hash history. Useful for web applications with no host (e.g. `file://`) or when configuring a server to
 * handle any URL is not possible.
 *
 * @param base - optional base to provide. Defaults to `location.pathname + location.search` If there is a `<base>` tag
 * in the `head`, its value will be ignored in favor of this parameter **but note it affects all the history.pushState()
 * calls**, meaning that if you use a `<base>` tag, it's `href` value **has to match this parameter** (ignoring anything
 * after the `#`).
 *
 * @example
 * ```js
 * // at https://example.com/folder
 * createWebHashHistory() // gives a url of `https://example.com/folder#`
 * createWebHashHistory('/folder/') // gives a url of `https://example.com/folder/#`
 * // if the `#` is provided in the base, it won't be added by `createWebHashHistory`
 * createWebHashHistory('/folder/#/app/') // gives a url of `https://example.com/folder/#/app/`
 * // you should avoid doing this because it changes the original url and breaks copying urls
 * createWebHashHistory('/other-folder/') // gives a url of `https://example.com/other-folder/#`
 *
 * // at file:///usr/etc/folder/index.html
 * // for locations with no `host`, the base is ignored
 * createWebHashHistory('/iAmIgnored') // gives a url of `file:///usr/etc/folder/index.html#`
 * ```
 */
declare function createWebHashHistory(base?: string): RouterHistory;
//#endregion
//#region src/scrollBehavior.d.ts
/**
 * Scroll position similar to
 * {@link https://developer.mozilla.org/en-US/docs/Web/API/ScrollToOptions | `ScrollToOptions`}.
 * Note that not all browsers support `behavior`.
 */
type ScrollPositionCoordinates = {
  behavior?: ScrollOptions['behavior'];
  left?: number;
  top?: number;
};
/**
 * Internal normalized version of {@link ScrollPositionCoordinates} that always
 * has `left` and `top` coordinates. Must be a type to be assignable to HistoryStateValue.
 *
 * @internal
 */
type _ScrollPositionNormalized = {
  behavior?: ScrollOptions['behavior'];
  left: number;
  top: number;
};
/**
 * Type of the `scrollBehavior` option that can be passed to `createRouter`.
 */
interface RouterScrollBehavior {
  /**
   * @param to - Route location where we are navigating to
   * @param from - Route location where we are navigating from
   * @param savedPosition - saved position if it exists, `null` otherwise
   */
  (to: RouteLocationNormalized, from: RouteLocationNormalizedLoaded, savedPosition: _ScrollPositionNormalized | null): Awaitable<ScrollPosition | false | void>;
}
interface ScrollPositionElement extends ScrollToOptions {
  /**
   * A valid CSS selector. Note some characters must be escaped in id selectors (https://mathiasbynens.be/notes/css-escapes).
   * @example
   * Here are a few examples:
   *
   * - `.title`
   * - `.content:first-child`
   * - `#marker`
   * - `#marker\~with\~symbols`
   * - `#marker.with.dot`: selects `class="with dot" id="marker"`, not `id="marker.with.dot"`
   *
   */
  el: string | Element;
}
type ScrollPosition = ScrollPositionCoordinates | ScrollPositionElement;
type Awaitable<T> = T | PromiseLike<T>;
//#endregion
//#region src/experimental/route-resolver/matchers/param-parsers/types.d.ts
/**
 * Defines a parser that can read a param from the url (string-based) and
 * transform it into a more complex type, or vice versa.
 *
 * @see MatcherPattern
 */
interface ParamParser<TParam = MatcherQueryParamsValue, TUrlParam = MatcherQueryParamsValue, TParamRaw = TParam> {
  get?: (value: NoInfer<TUrlParam>) => TParam;
  set?: (value: TParamRaw) => TUrlParam;
}
//#endregion
//#region src/experimental/route-resolver/matchers/matcher-pattern.d.ts
/**
 * Base interface for matcher patterns that extract params from a URL.
 *
 * @template TIn - type of the input value to match against the pattern
 * @template TParams - type of the output value after matching
 * @template TParamsRaw - type of the input value to build the input from
 *
 * In the case of the `path`, the `TIn` is a `string`, but in the case of the
 * query, it's the object of query params. `TParamsRaw` allows for a more permissive
 * type when building the value, for example allowing numbers and strings like
 * the old params.
 *
 * @internal this is the base interface for all matcher patterns, it shouldn't
 * be used directly
 */
interface MatcherPattern<TIn = string, TParams extends MatcherParamsFormatted = MatcherParamsFormatted, TParamsRaw extends MatcherParamsFormatted = TParams> {
  /**
   * Matches a serialized params value against the pattern.
   *
   * @param value - params value to parse
   * @throws {MatchMiss} if the value doesn't match
   * @returns parsed params object
   */
  match(value: TIn): TParams;
  /**
   * Build a serializable value from parsed params. Should apply encoding if the
   * returned value is a string (e.g path and hash should be encoded but query
   * shouldn't).
   *
   * @param value - params value to parse
   * @returns serialized params value
   */
  build(params: TParamsRaw): TIn;
}
/**
 * Handles the `path` part of a URL. It can transform a path string into an
 * object of params and vice versa.
 */
interface MatcherPatternPath<TParams extends MatcherParamsFormatted = MatcherParamsFormatted, // | null // | undefined // | void // so it might be a bit more convenient
TParamsRaw extends MatcherParamsFormatted = TParams> extends MatcherPattern<string, TParams, TParamsRaw> {}
/**
 * Allows matching a static path.
 *
 * @example
 * ```ts
 * const matcher = new MatcherPatternPathStatic('/team')
 * matcher.match('/team') // {}
 * matcher.match('/team/123') // throws MatchMiss
 * matcher.build() // '/team'
 * ```
 */
declare class MatcherPatternPathStatic implements MatcherPatternPath<EmptyParams> {
  readonly path: string;
  /**
   * lowercase version of the path to match against.
   * This is used to make the matching case insensitive.
   */
  private pathi;
  constructor(path: string);
  match(path: string): EmptyParams;
  build(): string;
}
/**
 * Options for param parsers in {@link MatcherPatternPathDynamic}.
 */
type MatcherPatternPathDynamic_ParamOptions<TUrlParam extends string | string[] | null = string | string[] | null, TParam = string | string[] | null, TParamRaw = TParam> = readonly [
/**
 * Param parser to use for this param.
 */
parser?: ParamParser<TParam, TUrlParam, TParamRaw>,
/**
 * Is tha param a repeatable param and should be converted to an array
 */
repeatable?: boolean,
/**
 * Can this parameter be omitted or empty (for repeatable params, an empty array).
 */
optional?: boolean];
/**
 * Helper type to extract the params from the options object.
 *
 * @internal
 */
type ExtractParamTypeFromOptions<TParamsOptions> = { [K in keyof TParamsOptions]: TParamsOptions[K] extends MatcherPatternPathDynamic_ParamOptions<any, infer TParam, any> ? TParam : never };
/**
 * Helper type to extract the raw params from the options object.
 *
 * @internal
 */
type ExtractLocationParamTypeFromOptions<TParamsOptions> = { [K in keyof TParamsOptions]: TParamsOptions[K] extends MatcherPatternPathDynamic_ParamOptions<any, any, infer TParamRaw> ? TParamRaw : never };
/**
 * Handles the `path` part of a URL with dynamic parameters.
 */
declare class MatcherPatternPathDynamic<TParamsOptions> implements MatcherPatternPath<ExtractParamTypeFromOptions<TParamsOptions>, ExtractLocationParamTypeFromOptions<TParamsOptions>> {
  readonly re: RegExp;
  readonly params: TParamsOptions & Record<string, MatcherPatternPathDynamic_ParamOptions<any, any>>;
  readonly pathParts: Array<string | number | Array<string | number>>;
  readonly trailingSlash: boolean | null;
  /**
   * Cached keys of the {@link params} object.
   */
  private paramsKeys;
  /**
   * Creates a new dynamic path matcher.
   *
   * @param re - regex to match the path against
   * @param params - object of param parsers as {@link MatcherPatternPathDynamic_ParamOptions}
   * @param pathParts - array of path parts, where strings are static parts, 1 are regular params, and 0 are splat params (not encode slash)
   * @param trailingSlash - whether the path should end with a trailing slash, null means "do not care" (for trailing splat params)
   */
  constructor(re: RegExp, params: TParamsOptions & Record<string, MatcherPatternPathDynamic_ParamOptions<any, any>>, pathParts: Array<string | number | Array<string | number>>, trailingSlash?: boolean | null);
  match(path: string): Simplify<ExtractParamTypeFromOptions<TParamsOptions>>;
  build(params: Simplify<ExtractLocationParamTypeFromOptions<TParamsOptions>>): string;
}
/**
 * Handles the `hash` part of a URL. It can transform a hash string into an
 * object of params and vice versa.
 */
interface MatcherPatternHash<TParams extends MatcherParamsFormatted = MatcherParamsFormatted> extends MatcherPattern<string, TParams> {}
/**
 * Generic object of params that can be passed to a matcher.
 */
type MatcherParamsFormatted = Record<string, unknown>;
/**
 * Empty object in TS.
 */
type EmptyParams = Record<PropertyKey, never>;
/**
 * Possible values for query params in a matcher.
 */
type MatcherQueryParamsValue = string | null | undefined | Array<string | null>;
type MatcherQueryParams = Record<string, MatcherQueryParamsValue>;
//#endregion
//#region src/location.d.ts
/**
 * Location object returned by {@link `parseURL`}.
 * @internal
 */
interface LocationNormalized {
  path: string;
  fullPath: string;
  hash: string;
  query: LocationQuery;
}
/**
 * Initial route location where the router is. Can be used in navigation guards
 * to differentiate the initial navigation.
 *
 * @example
 * ```js
 * import { START_LOCATION } from 'vue-router'
 *
 * router.beforeEach((to, from) => {
 *   if (from === START_LOCATION) {
 *     // initial navigation
 *   }
 * })
 * ```
 */
declare const START_LOCATION_NORMALIZED: RouteLocationNormalizedLoaded;
//#endregion
//#region src/experimental/route-resolver/resolver-abstract.d.ts
/**
 * Allowed types for a matcher name.
 */
type RecordName = string | symbol;
/**
 * Manage and resolve routes. Also handles the encoding, decoding, parsing and
 * serialization of params, query, and hash.
 *
 * - `TMatcherRecordRaw` represents the raw record type passed to {@link addMatcher}.
 * - `TMatcherRecord` represents the normalized record type returned by {@link getRoutes}.
 */
interface EXPERIMENTAL_Resolver_Base<TRecord> {
  /**
   * Resolves an absolute location (like `/path/to/somewhere`).
   *
   * @param absoluteLocation - The absolute location to resolve.
   * @param currentLocation - This value is ignored and should not be passed if the location is absolute.
   */
  resolve(absoluteLocation: `/${string}`, currentLocation?: undefined): ResolverLocationResolved<TRecord>;
  /**
   * Resolves a string location relative to another location. A relative
   * location can be `./same-folder`, `../parent-folder`, `same-folder`, or
   * even `?page=2`.
   */
  resolve(relativeLocation: string, currentLocation: ResolverLocationResolved<TRecord>): ResolverLocationResolved<TRecord>;
  /**
   * Resolves a location by its name. Any required params or query must be
   * passed in the `options` argument.
   */
  resolve(location: ResolverLocationAsNamed, currentLocation?: undefined): ResolverLocationResolved<TRecord>;
  /**
   * Resolves a location by its absolute path (starts with `/`). Any required query must be passed.
   *
   * @param location - The location to resolve.
   */
  resolve(location: ResolverLocationAsPathAbsolute, currentLocation?: undefined): ResolverLocationResolved<TRecord>;
  resolve(location: ResolverLocationAsPathRelative, currentLocation: ResolverLocationResolved<TRecord>): ResolverLocationResolved<TRecord>;
  /**
   * Resolves a location relative to another location. It reuses existing
   * properties in the `currentLocation` like `params`, `query`, and `hash`.
   */
  resolve(relativeLocation: ResolverLocationAsRelative, currentLocation: ResolverLocationResolved<TRecord>): ResolverLocationResolved<TRecord>;
  /**
   * Get a list of all resolver route records.
   */
  getRoutes(): TRecord[];
  /**
   * Get a resolver record by its name.
   * Previously named `getRecordMatcher()`
   */
  getRoute(name: RecordName): TRecord | undefined;
}
/**
 * Returned location object by {@link EXPERIMENTAL_Resolver_Base['resolve']}.
 * It contains the resolved name, params, query, hash, and matched records.
 */
interface ResolverLocationResolved<TMatched> extends LocationNormalized {
  /**
   * Name of the route record. A symbol if no name is provided.
   */
  name: RecordName;
  /**
   * Parsed params. Already decoded and formatted.
   */
  params: MatcherParamsFormatted;
  /**
   * Chain of route records that lead to the matched one. The last record is
   * the the one that matched the location. Each previous record is the parent
   * of the next one.
   */
  matched: TMatched[];
}
/**
 * Location object that can be passed to {@link
 * EXPERIMENTAL_Resolver_Base['resolve']} and is recognized as a `name`.
 *
 * @example
 * ```ts
 * resolver.resolve({ name: 'user', params: { id: 123 } })
 * resolver.resolve({ name: 'user-search', params: {}, query: { page: 2 } })
 * ```
 */
interface ResolverLocationAsNamed {
  name: RecordName;
  params: MatcherParamsFormatted;
  query?: LocationQueryRaw;
  hash?: string;
  /**
   * @deprecated This is ignored when `name` is provided
   */
  path?: undefined;
}
/**
 * Location object that can be passed to {@link EXPERIMENTAL_Resolver_Base['resolve']}
 * and is recognized as a relative path.
 *
 * @example
 * ```ts
 * resolver.resolve({ path: './123' }, currentLocation)
 * resolver.resolve({ path: '..' }, currentLocation)
 * ```
 */
interface ResolverLocationAsPathRelative {
  path: string;
  query?: LocationQueryRaw;
  hash?: string;
  /**
   * @deprecated This is ignored when `path` is provided
   */
  name?: undefined;
  /**
   * @deprecated This is ignored when `path` (instead of `name`) is provided
   */
  params?: undefined;
}
/**
 * Location object that can be passed to {@link EXPERIMENTAL_Resolver_Base['resolve']}
 * and is recognized as an absolute path.
 *
 * @example
 * ```ts
 * resolver.resolve({ path: '/team/123' })
 * ```
 */
interface ResolverLocationAsPathAbsolute extends ResolverLocationAsPathRelative {
  path: `/${string}`;
}
/**
 * Relative location object that can be passed to {@link EXPERIMENTAL_Resolver_Base['resolve']}
 * and is recognized as a relative location, copying the `params`, `query`, and
 * `hash` if not provided.
 *
 * @example
 * ```ts
 * resolver.resolve({ params: { id: 123 } }, currentLocation)
 * resolver.resolve({ hash: '#bottom' }, currentLocation)
 * ```
 */
interface ResolverLocationAsRelative {
  params?: MatcherParamsFormatted;
  query?: LocationQueryRaw;
  hash?: string;
  /**
   * @deprecated This location is relative to the next parameter. This `name` will be ignored.
   */
  name?: undefined;
  /**
   * @deprecated This location is relative to the next parameter. This `path` will be ignored.
   */
  path?: undefined;
}
//#endregion
//#region src/experimental/route-resolver/matchers/param-parsers/booleans.d.ts
/**
 * Native Param parser for booleans.
 *
 * @internal
 */
declare const PARAM_PARSER_BOOL: {
  get: (value: NoInfer<MatcherQueryParamsValue>) => boolean | boolean[] | undefined;
  set: (value: boolean | boolean[] | null | undefined) => string | string[] | null | undefined;
};
//#endregion
//#region src/experimental/route-resolver/matchers/param-parsers/integers.d.ts
/**
 * Native Param parser for integers.
 *
 * @internal
 */
declare const PARAM_PARSER_INT: {
  get: (value: NoInfer<MatcherQueryParamsValue>) => number | number[] | null;
  set: (value: number | number[] | null) => string | string[] | null;
};
//#endregion
//#region src/experimental/route-resolver/matchers/param-parsers/index.d.ts
/**
 * Defines a path param parser.
 *
 * @param parser - the parser to define. Will be returned as is.
 *
 * @see {@link defineQueryParamParser}
 * @see {@link defineParamParser}
 */
/*! #__NO_SIDE_EFFECTS__ */
declare function definePathParamParser<TParam, TUrlParam extends string | string[] | null, TParamRaw>(parser: Required<ParamParser<TParam, TUrlParam, TParamRaw>>): Required<ParamParser<TParam, TUrlParam, TParamRaw>>;
/**
 * Defines a query param parser. Note that query params can also be used as
 * path param parsers.
 *
 * @param parser - the parser to define. Will be returned as is.
 *
 * @see {@link definePathParamParser}
 * @see {@link defineParamParser}
 */
/*! #__NO_SIDE_EFFECTS__ */
declare function defineQueryParamParser<TParam, TParamRaw = TParam>(parser: Required<ParamParser<TParam, MatcherQueryParamsValue, TParamRaw>>): Required<ParamParser<TParam, MatcherQueryParamsValue, TParamRaw>>;
/**
 * Alias for {@link defineQueryParamParser}. Implementing a param parser like this
 * works for path, query, and hash params.
 *
 * @see {@link defineQueryParamParser}
 * @see {@link definePathParamParser}
 */
declare const defineParamParser: typeof defineQueryParamParser;
//#endregion
//#region src/experimental/route-resolver/matchers/matcher-pattern-query.d.ts
/**
 * Handles the `query` part of a URL. It can transform a query object into an
 * object of params and vice versa.
 */
interface MatcherPatternQuery<TParams extends MatcherParamsFormatted = MatcherParamsFormatted> extends MatcherPattern<MatcherQueryParams, TParams> {}
/**
 * Matcher for a specific query parameter. It will read and write the parameter
 */
declare class MatcherPatternQueryParam<T, ParamName extends string> implements MatcherPatternQuery<Record<ParamName, T>> {
  private paramName;
  private queryKey;
  private format;
  private parser;
  private defaultValue?;
  private required?;
  constructor(paramName: ParamName, queryKey: string, format: 'value' | 'array', parser?: ParamParser<T>, defaultValue?: ((() => T) | T) | undefined, required?: boolean | undefined);
  match(query: MatcherQueryParams): Record<ParamName, T>;
  build(params: Record<ParamName, T>): MatcherQueryParams;
}
//#endregion
//#region src/experimental/route-resolver/resolver-fixed.d.ts
/**
 * Base interface for a resolver record that can be extended.
 */
interface EXPERIMENTAL_ResolverRecord_Base {
  /**
   * Name of the matcher. Unique across all matchers. If missing, this record
   * cannot be matched. This is useful for grouping records.
   */
  name?: RecordName;
  /**
   * {@link MatcherPattern} for the path section of the URI.
   */
  path?: MatcherPatternPath;
  /**
   * {@link MatcherPattern} for the query section of the URI.
   */
  query?: MatcherPatternQuery[];
  /**
   * {@link MatcherPattern} for the hash section of the URI.
   */
  hash?: MatcherPatternHash;
  /**
   * Parent record. The parent can be a group or a matchable record.
   * It will be included in the `matched` array of a resolved location.
   */
  parent?: EXPERIMENTAL_ResolverRecord_Base | null;
  /**
   * If this record is an alias of another record, this points to the original
   * record. Alias records are not added to the name map and resolve to the
   * original record's name.
   */
  aliasOf?: EXPERIMENTAL_ResolverRecord_Base | null;
}
/**
 * A group can contain other useful properties like `meta` defined by the router.
 */
interface EXPERIMENTAL_ResolverRecord_Group extends EXPERIMENTAL_ResolverRecord_Base {
  /**
   * A group route cannot be matched directly and cannot be named.
   */
  name?: undefined;
  /**
   * A group route can **only** match the `query`.
   */
  path?: undefined;
  /**
   * A group route can **only** match the `query`.
   */
  hash?: undefined;
}
/**
 * A matchable record is a record that can be matched by a path, query or hash
 * and will resolve to a location.
 */
interface EXPERIMENTAL_ResolverRecord_Matchable extends EXPERIMENTAL_ResolverRecord_Base {
  name: RecordName;
  path: MatcherPatternPath;
}
/**
 * @alias EXPERIMENTAL_Resolver_Base
 */
interface EXPERIMENTAL_ResolverFixed<TRecord> extends EXPERIMENTAL_Resolver_Base<TRecord> {}
/**
 * Creates a fixed resolver that must have all records defined at creation
 * time.
 *
 * @template TRecord - extended type of the records
 * @param {TRecord[]} records - Ordered array of records that will be used to resolve routes
 * @returns a resolver that can be passed to the router
 */
declare function createFixedResolver<TRecord extends EXPERIMENTAL_ResolverRecord_Matchable>(records: TRecord[]): EXPERIMENTAL_ResolverFixed<TRecord>;
//#endregion
//#region src/experimental/router.d.ts
/**
 * Options to initialize a {@link Router} instance.
 */
interface EXPERIMENTAL_RouterOptions_Base extends PathParserOptions {
  /**
   * History implementation used by the router. Most web applications should use
   * `createWebHistory` but it requires the server to be properly configured.
   * You can also use a _hash_ based history with `createWebHashHistory` that
   * does not require any configuration on the server but isn't handled at all
   * by search engines and does poorly on SEO.
   *
   * @example
   * ```js
   * createRouter({
   *   history: createWebHistory(),
   *   // other options...
   * })
   * ```
   */
  history: RouterHistory;
  /**
   * Function to control scrolling when navigating between pages. Can return a
   * Promise to delay scrolling.
   *
   * @see {@link RouterScrollBehavior}.
   *
   * @example
   * ```js
   * function scrollBehavior(to, from, savedPosition) {
   *   // `to` and `from` are both route locations
   *   // `savedPosition` can be null if there isn't one
   * }
   * ```
   */
  scrollBehavior?: RouterScrollBehavior;
  /**
   * Custom implementation to parse a query. See its counterpart,
   * {@link EXPERIMENTAL_RouterOptions_Base.stringifyQuery}.
   *
   * @example
   * Let's say you want to use the [qs package](https://github.com/ljharb/qs)
   * to parse queries, you can provide both `parseQuery` and `stringifyQuery`:
   * ```js
   * import qs from 'qs'
   *
   * createRouter({
   *   // other options...
   *   parseQuery: qs.parse,
   *   stringifyQuery: qs.stringify,
   * })
   * ```
   */
  parseQuery?: typeof parseQuery;
  /**
   * Custom implementation to stringify a query object. Should not prepend a leading `?`.
   * {@link parseQuery} counterpart to handle query parsing.
   */
  stringifyQuery?: typeof stringifyQuery;
  /**
   * Default class applied to active {@link RouterLink}. If none is provided,
   * `router-link-active` will be applied.
   */
  linkActiveClass?: string;
  /**
   * Default class applied to exact active {@link RouterLink}. If none is provided,
   * `router-link-exact-active` will be applied.
   */
  linkExactActiveClass?: string;
}
/**
 * Internal type for common properties among all kind of {@link RouteRecordRaw}.
 */
interface EXPERIMENTAL_RouteRecord_Base extends EXPERIMENTAL_ResolverRecord_Base {
  /**
   * Where to redirect if the route is directly matched. The redirection happens
   * before any navigation guard and triggers a new navigation with the new
   * target location.
   */
  redirect?: RouteRecordRedirectOption;
  /**
   * Before Enter guard specific to this record. Note `beforeEnter` has no
   * effect if the record has a `redirect` property.
   */
  /**
   * Arbitrary data attached to the record.
   */
  meta?: RouteMeta;
  /**
   * Components to display when the URL matches this route. Allow using named views.
   */
  components?: Record<string, RawRouteComponent>;
  /**
   * Parent of this component if any
   */
  parent?: EXPERIMENTAL_RouteRecordNormalized | null;
  /**
   * References another record if this record is an alias of it.
   */
  aliasOf?: EXPERIMENTAL_RouteRecordNormalized | null;
}
interface EXPERIMENTAL_RouteRecord_Redirect extends Omit<EXPERIMENTAL_RouteRecord_Base, 'name' | 'path'>, Omit<EXPERIMENTAL_ResolverRecord_Matchable, 'parent' | 'aliasOf'> {
  components?: Record<string, RawRouteComponent>;
  redirect: RouteRecordRedirectOption;
}
interface EXPERIMENTAL_RouteRecord_Group extends Omit<EXPERIMENTAL_RouteRecord_Base, 'name' | 'path' | 'query' | 'hash'>, Omit<EXPERIMENTAL_ResolverRecord_Group, 'parent' | 'aliasOf'> {
  components?: Record<string, RawRouteComponent>;
}
interface EXPERIMENTAL_RouteRecord_Components extends Omit<EXPERIMENTAL_RouteRecord_Base, 'name' | 'path'>, Omit<EXPERIMENTAL_ResolverRecord_Matchable, 'parent' | 'aliasOf'> {
  components: Record<string, RawRouteComponent>;
  redirect?: never;
}
type EXPERIMENTAL_RouteRecord_Matchable = EXPERIMENTAL_RouteRecord_Components | EXPERIMENTAL_RouteRecord_Redirect;
type EXPERIMENTAL_RouteRecordRaw = EXPERIMENTAL_RouteRecord_Matchable | EXPERIMENTAL_RouteRecord_Group;
interface EXPERIMENTAL_RouteRecordNormalized_Base {
  /**
   * Contains the original modules for lazy loaded components.
   *
   * @internal
   */
  mods: Record<string, unknown>;
  props: Record<string, _RouteRecordProps>;
  /**
   * Registered leave guards
   *
   * @internal
   */
  leaveGuards: Set<NavigationGuard>;
  /**
   * Registered update guards
   *
   * @internal
   */
  updateGuards: Set<NavigationGuard>;
  instances: Record<string, unknown>;
}
interface EXPERIMENTAL_RouteRecordNormalized_Group extends EXPERIMENTAL_RouteRecordNormalized_Base, EXPERIMENTAL_RouteRecord_Group {
  meta: RouteMeta;
}
interface EXPERIMENTAL_RouteRecordNormalized_Redirect extends EXPERIMENTAL_RouteRecordNormalized_Base, EXPERIMENTAL_RouteRecord_Redirect {
  meta: RouteMeta;
}
interface EXPERIMENTAL_RouteRecordNormalized_Components extends EXPERIMENTAL_RouteRecordNormalized_Base, EXPERIMENTAL_RouteRecord_Components {
  meta: RouteMeta;
}
type EXPERIMENTAL_RouteRecordNormalized_Matchable = EXPERIMENTAL_RouteRecordNormalized_Components | EXPERIMENTAL_RouteRecordNormalized_Redirect;
type EXPERIMENTAL_RouteRecordNormalized = EXPERIMENTAL_RouteRecordNormalized_Matchable | EXPERIMENTAL_RouteRecordNormalized_Group;
declare function normalizeRouteRecord(record: EXPERIMENTAL_RouteRecord_Group): EXPERIMENTAL_RouteRecordNormalized_Group;
declare function normalizeRouteRecord(record: EXPERIMENTAL_RouteRecord_Matchable): EXPERIMENTAL_RouteRecordNormalized_Matchable;
/**
 * Options to initialize an experimental {@link EXPERIMENTAL_Router} instance.
 * @experimental
 */
interface EXPERIMENTAL_RouterOptions extends EXPERIMENTAL_RouterOptions_Base {
  /**
   * Matcher to use to resolve routes.
   *
   * @experimental
   */
  resolver: EXPERIMENTAL_ResolverFixed<EXPERIMENTAL_RouteRecordNormalized_Matchable>;
}
/**
 * Router base instance.
 *
 * @experimental This version is not stable, it's meant to replace {@link Router} in the future.
 */
interface EXPERIMENTAL_Router_Base<TRecord> {
  /**
   * Current {@link RouteLocationNormalized}
   */
  readonly currentRoute: ShallowRef<RouteLocationNormalizedLoaded>;
  /**
   * Allows turning off the listening of history events. This is a low level api for micro-frontend.
   */
  listening: boolean;
  /**
   * Checks if a route with a given name exists
   *
   * @param name - Name of the route to check
   */
  hasRoute(name: NonNullable<RouteRecordNameGeneric>): boolean;
  /**
   * Get a full list of all the {@link RouteRecord | route records}.
   */
  getRoutes(): TRecord[];
  /**
   * Returns the {@link RouteLocation | normalized version} of a
   * {@link RouteLocationRaw | route location}. Also includes an `href` property
   * that includes any existing `base`. By default, the `currentLocation` used is
   * `router.currentRoute` and should only be overridden in advanced use cases.
   *
   * @param to - Raw route location to resolve
   * @param currentLocation - Optional current location to resolve against
   */
  resolve<Name extends keyof RouteMap = keyof RouteMap>(to: RouteLocationAsRelativeTyped<RouteMap, Name>, currentLocation?: RouteLocationNormalizedLoaded): RouteLocationResolved<Name>;
  resolve(to: RouteLocationAsString | RouteLocationAsRelative | RouteLocationAsPath, currentLocation?: RouteLocationNormalizedLoaded): RouteLocationResolved;
  /**
   * Programmatically navigate to a new URL by pushing an entry in the history
   * stack.
   *
   * @param to - Route location to navigate to
   */
  push(to: RouteLocationRaw): Promise<NavigationFailure | void | undefined>;
  /**
   * Programmatically navigate to a new URL by replacing the current entry in
   * the history stack.
   *
   * @param to - Route location to navigate to
   */
  replace(to: RouteLocationRaw): Promise<NavigationFailure | void | undefined>;
  /**
   * Go back in history if possible by calling `history.back()`. Equivalent to
   * `router.go(-1)`.
   */
  back(): void;
  /**
   * Go forward in history if possible by calling `history.forward()`.
   * Equivalent to `router.go(1)`.
   */
  forward(): void;
  /**
   * Allows you to move forward or backward through the history. Calls
   * `history.go()`.
   *
   * @param delta - The position in the history to which you want to move,
   * relative to the current page
   */
  go(delta: number): void;
  /**
   * Add a navigation guard that executes before any navigation. Returns a
   * function that removes the registered guard.
   *
   * @param guard - navigation guard to add
   */
  beforeEach(guard: NavigationGuardWithThis<undefined>): () => void;
  /**
   * Add a navigation guard that executes before navigation is about to be
   * resolved. At this state all component have been fetched and other
   * navigation guards have been successful. Returns a function that removes the
   * registered guard.
   *
   * @param guard - navigation guard to add
   * @returns a function that removes the registered guard
   *
   * @example
   * ```js
   * router.beforeResolve(to => {
   *   if (to.meta.requiresAuth && !isAuthenticated) return false
   * })
   * ```
   *
   */
  beforeResolve(guard: _NavigationGuardResolved): () => void;
  /**
   * Add a navigation hook that is executed after every navigation. Returns a
   * function that removes the registered hook.
   *
   * @param guard - navigation hook to add
   * @returns a function that removes the registered hook
   *
   * @example
   * ```js
   * router.afterEach((to, from, failure) => {
   *   if (isNavigationFailure(failure)) {
   *     console.log('failed navigation', failure)
   *   }
   * })
   * ```
   */
  afterEach(guard: NavigationHookAfter): () => void;
  /**
   * Adds an error handler that is called every time a non caught error happens
   * during navigation. This includes errors thrown synchronously and
   * asynchronously, errors returned or passed to `next` in any navigation
   * guard, and errors occurred when trying to resolve an async component that
   * is required to render a route.
   *
   * @param handler - error handler to register
   */
  onError(handler: _ErrorListener): () => void;
  /**
   * Returns a Promise that resolves when the router has completed the initial
   * navigation, which means it has resolved all async enter hooks and async
   * components that are associated with the initial route. If the initial
   * navigation already happened, the promise resolves immediately.
   *
   * This is useful in server-side rendering to ensure consistent output on both
   * the server and the client. Note that on server side, you need to manually
   * push the initial location while on client side, the router automatically
   * picks it up from the URL.
   */
  isReady(): Promise<void>;
  /**
   * Called automatically by `app.use(router)`. Should not be called manually by
   * the user. This will trigger the initial navigation when on client side.
   *
   * @internal
   * @param app - Application that uses the router
   */
  install(app: App): void;
}
interface EXPERIMENTAL_Router extends EXPERIMENTAL_Router_Base<EXPERIMENTAL_RouteRecordNormalized_Matchable> {
  /**
   * Original options object passed to create the Router
   */
  readonly options: EXPERIMENTAL_RouterOptions;
  /**
   * Dev only method to replace the resolver used by the router. Used during HMR
   *
   * @param newResolver - new resolver to use
   *
   * @internal
   */
  _hmrReplaceResolver?: (newResolver: EXPERIMENTAL_ResolverFixed<EXPERIMENTAL_RouteRecordNormalized_Matchable>) => void;
}
/**
 * Creates an experimental Router that allows passing a resolver instead of a
 * routes array. This router does not have `addRoute()` and `removeRoute()`
 * methods and is meant to be used with file-based routing thanks to
 * vue-router/vite or vue-router/unplugin resolver generation in
 * `'vue-router/auto-resolver'`.
 *
 * @param options - Options to initialize the router
 */
declare function experimental_createRouter(options: EXPERIMENTAL_RouterOptions): EXPERIMENTAL_Router;
//#endregion
//#region src/router.d.ts
/**
 * Options to initialize a {@link Router} instance.
 */
interface RouterOptions extends EXPERIMENTAL_RouterOptions_Base {
  /**
   * Initial list of routes that should be added to the router.
   */
  routes: Readonly<RouteRecordRaw[]>;
}
/**
 * Router instance.
 */
interface Router extends EXPERIMENTAL_Router_Base<RouteRecordNormalized> {
  /**
   * Original options object passed to create the Router
   */
  readonly options: RouterOptions;
  /**
   * Add a new {@link RouteRecordRaw | route record} as the child of an existing route.
   *
   * @param parentName - Parent Route Record where `route` should be appended at
   * @param route - Route Record to add
   */
  addRoute(parentName: NonNullable<RouteRecordNameGeneric>, route: RouteRecordRaw): () => void;
  /**
   * Add a new {@link RouteRecordRaw | route record} to the router.
   *
   * @param route - Route Record to add
   */
  addRoute(route: RouteRecordRaw): () => void;
  /**
   * Remove an existing route by its name.
   *
   * @param name - Name of the route to remove
   */
  removeRoute(name: NonNullable<RouteRecordNameGeneric>): void;
  /**
   * Delete all routes from the router.
   */
  clearRoutes(): void;
}
/**
 * Creates a Router instance that can be used by a Vue app.
 *
 * @param options - {@link RouterOptions}
 */
declare function createRouter(options: RouterOptions): Router;
//#endregion
//#region src/injectionSymbols.d.ts
/**
 * RouteRecord being rendered by the closest ancestor Router View. Used for
 * `onBeforeRouteUpdate` and `onBeforeRouteLeave`. rvlm stands for Router View
 * Location Matched
 *
 * @internal
 */
declare const matchedRouteKey: InjectionKey<ComputedRef<RouteRecordNormalized | undefined>>;
/**
 * Allows overriding the router view depth to control which component in
 * `matched` is rendered. rvd stands for Router View Depth
 *
 * @internal
 */
declare const viewDepthKey: InjectionKey<Ref<number> | number>;
/**
 * Allows overriding the router instance returned by `useRouter` in tests. r
 * stands for router
 *
 * @internal
 */
declare const routerKey: InjectionKey<Router>;
/**
 * Allows overriding the current route returned by `useRoute` in tests. rl
 * stands for route location
 *
 * @internal
 */
declare const routeLocationKey: InjectionKey<RouteLocationNormalizedLoaded>;
/**
 * Allows overriding the current route used by router-view. Internally this is
 * used when the `route` prop is passed.
 *
 * @internal
 */
declare const routerViewLocationKey: InjectionKey<Ref<RouteLocationNormalizedLoaded>>;
//#endregion
//#region src/navigationGuards.d.ts
/**
 * Add a navigation guard that triggers whenever the component for the current
 * location is about to be left. Similar to {@link beforeRouteLeave} but can be
 * used in any component. The guard is removed when the component is unmounted.
 *
 * @param leaveGuard - {@link NavigationGuard}
 */
declare function onBeforeRouteLeave(leaveGuard: NavigationGuard): void;
/**
 * Add a navigation guard that triggers whenever the current location is about
 * to be updated. Similar to {@link beforeRouteUpdate} but can be used in any
 * component. The guard is removed when the component is unmounted.
 *
 * @param updateGuard - {@link NavigationGuard}
 */
declare function onBeforeRouteUpdate(updateGuard: NavigationGuard): void;
/**
 * Ensures a route is loaded, so it can be passed as o prop to `<RouterView>`.
 *
 * @param route - resolved route to load
 */
declare function loadRouteLocation(route: RouteLocation | RouteLocationNormalized): Promise<RouteLocationNormalizedLoaded>;
//#endregion
//#region src/RouterLink.d.ts
interface RouterLinkOptions {
  /**
   * Route Location the link should navigate to when clicked on.
   */
  to: RouteLocationRaw;
  /**
   * Calls `router.replace` instead of `router.push`.
   */
  replace?: boolean;
}
interface RouterLinkProps extends RouterLinkOptions {
  /**
   * Whether RouterLink should not wrap its content in an `a` tag. Useful when
   * using `v-slot` to create a custom RouterLink
   */
  custom?: boolean;
  /**
   * Class to apply when the link is active
   */
  activeClass?: string;
  /**
   * Class to apply when the link is exact active
   */
  exactActiveClass?: string;
  /**
   * Value passed to the attribute `aria-current` when the link is exact active.
   *
   * @defaultValue `'page'`
   */
  ariaCurrentValue?: 'page' | 'step' | 'location' | 'date' | 'time' | 'true' | 'false';
  /**
   * Pass the returned promise of `router.push()` to `document.startViewTransition()` if supported.
   */
  viewTransition?: boolean;
}
/**
 * Options passed to {@link useLink}.
 */
interface UseLinkOptions<Name extends keyof RouteMap = keyof RouteMap> {
  to: MaybeRef<RouteLocationAsString | RouteLocationAsRelativeTyped<RouteMap, Name> | RouteLocationAsPath | RouteLocationRaw>;
  replace?: MaybeRef<boolean | undefined>;
  /**
   * Pass the returned promise of `router.push()` to `document.startViewTransition()` if supported.
   */
  viewTransition?: boolean;
}
/**
 * Return type of {@link useLink}.
 * @internal
 */
interface UseLinkReturn<Name extends keyof RouteMap = keyof RouteMap> {
  route: ComputedRef<RouteLocationResolved<Name>>;
  href: ComputedRef<string>;
  isActive: ComputedRef<boolean>;
  isExactActive: ComputedRef<boolean>;
  navigate(e?: MouseEvent): Promise<void | NavigationFailure>;
}
/**
 * Returns the internal behavior of a {@link RouterLink} without the rendering part.
 *
 * @param props - a `to` location and an optional `replace` flag
 */
declare function useLink<Name extends keyof RouteMap = keyof RouteMap>(props: UseLinkOptions<Name>): UseLinkReturn<Name>;
/**
 * Component to render a link that triggers a navigation on click.
 */
declare const RouterLink: _RouterLinkI;
/**
 * @internal
 */
type _RouterLinkPropsTypedBase = AllowedComponentProps & ComponentCustomProps & VNodeProps & RouterLinkProps;
/**
 * @internal
 */
type RouterLinkPropsTyped<Custom extends boolean | undefined> = Custom extends true ? _RouterLinkPropsTypedBase & {
  custom: true;
} : _RouterLinkPropsTypedBase & {
  custom?: false | undefined;
} & Omit<AnchorHTMLAttributes, 'href'>;
/**
 * Typed version of the `RouterLink` component. Its generic defaults to the typed router, so it can be inferred
 * automatically for JSX.
 *
 * @internal
 */
interface _RouterLinkI {
  new <Custom extends boolean | undefined = boolean | undefined>(): {
    $props: RouterLinkPropsTyped<Custom>;
    $slots: {
      default?: ({
        route,
        href,
        isActive,
        isExactActive,
        navigate
      }: UnwrapRef<UseLinkReturn>) => VNode[];
    };
  };
  /**
   * Access to `useLink()` without depending on using vue-router
   *
   * @internal
   */
  useLink: typeof useLink;
}
//#endregion
//#region src/RouterView.d.ts
interface RouterViewProps {
  name?: string;
  route?: RouteLocationNormalized;
}
/**
 * Component to display the current route the user is at.
 */
declare const RouterView: {
  new (): {
    $props: AllowedComponentProps & ComponentCustomProps & VNodeProps & RouterViewProps;
    $slots: {
      default?: ({
        Component,
        route
      }: {
        Component: VNode;
        route: RouteLocationNormalizedLoaded;
      }) => VNode[];
    };
  };
};
//#endregion
//#region src/useApi.d.ts
/**
 * Returns the router instance. Equivalent to using `$router` inside
 * templates.
 */
declare function useRouter(): Router;
/**
 * Returns the current route location. Equivalent to using `$route` inside
 * templates.
 */
declare function useRoute<Name extends keyof RouteMap = keyof RouteMap>(_name?: Name): RouteLocationNormalizedLoaded<Name | RouteMap[Name]["childrenNames"]>;
//#endregion
//#region src/index.d.ts
declare module 'vue' {
  interface ComponentCustomOptions {
    /**
     * Guard called when the router is navigating to the route that is rendering
     * this component from a different route. Differently from `beforeRouteUpdate`
     * and `beforeRouteLeave`, `beforeRouteEnter` does not have access to the
     * component instance through `this` because it triggers before the component
     * is even mounted.
     *
     * @param to - RouteLocationRaw we are navigating to
     * @param from - RouteLocationRaw we are navigating from
     * @param next - function to validate, cancel or modify (by redirecting) the
     * navigation
     */
    beforeRouteEnter?: TypesConfig extends Record<'beforeRouteEnter', infer T> ? T : NavigationGuardWithThis<undefined>;
    /**
     * Guard called whenever the route that renders this component has changed, but
     * it is reused for the new route. This allows you to guard for changes in
     * params, the query or the hash.
     *
     * @param to - RouteLocationRaw we are navigating to
     * @param from - RouteLocationRaw we are navigating from
     * @param next - function to validate, cancel or modify (by redirecting) the
     * navigation
     */
    beforeRouteUpdate?: TypesConfig extends Record<'beforeRouteUpdate', infer T> ? T : NavigationGuard;
    /**
     * Guard called when the router is navigating away from the current route that
     * is rendering this component.
     *
     * @param to - RouteLocationRaw we are navigating to
     * @param from - RouteLocationRaw we are navigating from
     * @param next - function to validate, cancel or modify (by redirecting) the
     * navigation
     */
    beforeRouteLeave?: TypesConfig extends Record<'beforeRouteLeave', infer T> ? T : NavigationGuard;
  }
  interface ComponentCustomProperties {
    /**
     * Normalized current location. See {@link RouteLocationNormalizedLoaded}.
     */
    $route: TypesConfig extends Record<'$route', infer T> ? T : RouteLocationNormalizedLoaded;
    /**
     * {@link Router} instance used by the application.
     */
    $router: TypesConfig extends Record<'$router', infer T> ? T : Router;
  }
  interface GlobalComponents {
    RouterView: TypesConfig extends Record<'RouterView', infer T> ? T : typeof RouterView;
    RouterLink: TypesConfig extends Record<'RouterLink', infer T> ? T : typeof RouterLink;
  }
}
//#endregion
export { MatcherQueryParamsValue as $, RouteParams as $t, EXPERIMENTAL_RouterOptions as A, createRouterMatcher as An, RouteLocationNormalizedGeneric as At, defineQueryParamParser as B, stringifyQuery as Bn, RouteLocationResolvedTyped as Bt, EXPERIMENTAL_RouteRecordNormalized_Group as C, RouteRecordSingleView as Cn, RouteLocationAsRelativeTyped as Ct, EXPERIMENTAL_RouteRecord_Group as D, HistoryState as Dn, RouteLocationAsStringTypedList as Dt, EXPERIMENTAL_RouteRecord_Base as E, _RouteRecordBase as En, RouteLocationAsStringTyped as Et, createFixedResolver as F, LocationQuery as Fn, RouteLocationNormalizedTyped as Ft, MatcherParamsFormatted as G, RouteRecordNameGeneric as Gt, PARAM_PARSER_BOOL as H, RouteLocationTyped as Ht, MatcherPatternQuery as I, LocationQueryRaw as In, RouteLocationNormalizedTypedList as It, MatcherPatternPath as J, _Awaitable as Jt, MatcherPattern as K, RouteRecordRedirectOption as Kt, MatcherPatternQueryParam as L, LocationQueryValue as Ln, RouteLocationRaw as Lt, EXPERIMENTAL_Router_Base as M, _PathParserOptions as Mn, RouteLocationNormalizedLoadedGeneric as Mt, experimental_createRouter as N, RouteRecord as Nn, RouteLocationNormalizedLoadedTyped as Nt, EXPERIMENTAL_RouteRecord_Matchable as O, RouterHistory as On, RouteLocationGeneric as Ot, normalizeRouteRecord as P, RouteRecordNormalized as Pn, RouteLocationNormalizedLoadedTypedList as Pt, MatcherQueryParams as Q, ParamValueZeroOrOne as Qt, defineParamParser as R, LocationQueryValueRaw as Rn, RouteLocationResolved as Rt, EXPERIMENTAL_RouteRecordNormalized as S, RouteRecordRedirect as Sn, RouteLocationAsRelativeGeneric as St, EXPERIMENTAL_RouteRecordRaw as T, _RouteLocationBase as Tn, RouteLocationAsString as Tt, START_LOCATION_NORMALIZED as U, RouteLocationTypedList as Ut, PARAM_PARSER_INT as V, TypesConfig as Vn, RouteLocationResolvedTypedList as Vt, EmptyParams as W, RouteRecordName as Wt, MatcherPatternPathDynamic_ParamOptions as X, ParamValueOneOrMore as Xt, MatcherPatternPathDynamic as Y, ParamValue as Yt, MatcherPatternPathStatic as Z, ParamValueZeroOrMore as Zt, routerViewLocationKey as _, RouteParamsRawGeneric as _n, RouteLocationAsPath as _t, RouterLink as a, LocationAsRelativeRaw as an, NavigationGuard as at, RouterOptions as b, RouteRecordMultipleViewsWithChildren as bn, RouteLocationAsPathTypedList as bt, UseLinkReturn as c, RouteComponent as cn, NavigationGuardReturn as ct, loadRouteLocation as d, RouteLocationOptions as dn, ErrorTypes as dt, RouteParamsRaw as en, ParamParser as et, onBeforeRouteLeave as f, RouteLocationPathRaw as fn, NavigationFailure as ft, routerKey as g, RouteParamsGeneric as gn, RouteLocation as gt, routeLocationKey as h, RouteParamValueRaw as hn, isNavigationFailure as ht, RouterViewProps as i, RouteRecordInfoGeneric as in, createWebHistory as it, EXPERIMENTAL_RouterOptions_Base as j, PathParserOptions as jn, RouteLocationNormalizedLoaded as jt, EXPERIMENTAL_Router as k, RouterMatcher as kn, RouteLocationNormalized as kt, _RouterLinkI as l, RouteLocationMatched as ln, NavigationGuardWithThis as lt, matchedRouteKey as m, RouteParamValue as mn, NavigationRedirectError as mt, useRouter as n, RouteMapGeneric as nn, createWebHashHistory as nt, RouterLinkProps as o, MatcherLocation as on, NavigationGuardNext as ot, onBeforeRouteUpdate as p, RouteMeta as pn, NavigationFailureType as pt, MatcherPatternHash as q, _RouteRecordProps as qt, RouterView as r, RouteRecordInfo as rn, createMemoryHistory as rt, UseLinkOptions as s, MatcherLocationAsPath as sn, NavigationGuardNextCallback as st, useRoute as t, RouteMap as tn, RouterScrollBehavior as tt, useLink as u, RouteLocationNamedRaw as un, NavigationHookAfter as ut, viewDepthKey as v, RouteQueryAndHash as vn, RouteLocationAsPathGeneric as vt, EXPERIMENTAL_RouteRecordNormalized_Matchable as w, RouteRecordSingleViewWithChildren as wn, RouteLocationAsRelativeTypedList as wt, createRouter as x, RouteRecordRaw as xn, RouteLocationAsRelative as xt, Router as y, RouteRecordMultipleViews as yn, RouteLocationAsPathTyped as yt, definePathParamParser as z, parseQuery as zn, RouteLocationResolvedGeneric as zt };