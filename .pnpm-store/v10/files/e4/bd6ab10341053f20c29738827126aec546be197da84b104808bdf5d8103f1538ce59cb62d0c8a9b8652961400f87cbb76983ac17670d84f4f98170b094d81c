/// <reference types="node" />
import * as _vue_devtools_kit0 from "@vue/devtools-kit";
import { AppRecord, CustomCommand, CustomTab, DevToolsV6PluginAPIHookKeys, DevToolsV6PluginAPIHookPayloads, OpenInEditorOptions, getRpcClient, getRpcServer, getViteRpcClient } from "@vue/devtools-kit";
import * as vue from "vue";
import { AllowedComponentProps, AnchorHTMLAttributes, App, Component as Component$1, ComponentCustomProps, ComponentPublicInstance, ComputedRef, DefineComponent, MaybeRef, Ref, ShallowRef, UnwrapRef, VNode, VNodeProps } from "vue";
import * as http from "node:http";
import { Agent, ClientRequest, ClientRequestArgs, OutgoingHttpHeaders } from "node:http";
import { Http2SecureServer } from "node:http2";
import * as fs from "node:fs";
import { EventEmitter } from "node:events";
import { Server as Server$1, ServerOptions as ServerOptions$1 } from "node:https";
import * as net from "node:net";
import { Duplex, DuplexOptions, Stream } from "node:stream";
import { SecureContextOptions } from "node:tls";
import { URL as URL$1 } from "node:url";
import { ZlibOptions } from "node:zlib";
import Lightningcss from "lightningcss";
import Less from "less";
import Stylus from "stylus";

//#region src/client.d.ts
declare function setDevToolsClientUrl(url: string): void;
declare function getDevToolsClientUrl(): any;
//#endregion
//#region ../../node_modules/.pnpm/vue-router@4.6.0_vue@3.5.22_typescript@5.9.3_/node_modules/vue-router/dist/router-CXzcRfJt.d.mts
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
declare function stringifyQuery(query: LocationQueryRaw | undefined): string; //#endregion
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
interface TypesConfig {} //#endregion
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
 * Convenience type to get the typed RouteMap or a generic one if not provided. It is extracted from the {@link TypesConfig} if it exists, it becomes {@link RouteMapGeneric} otherwise.
 */
type RouteMap = TypesConfig extends Record<'RouteNamedMap', infer RouteNamedMap> ? RouteNamedMap : RouteMapGeneric;
/**
 * Generic version of the `RouteMap`.
 */
type RouteMapGeneric = Record<string | symbol, RouteRecordInfoGeneric>; //#endregion
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
/**
 * @internal
 */
type _RouteRecordProps<Name extends keyof RouteMap = keyof RouteMap> = boolean | Record<string, any> | ((to: RouteLocationNormalized<Name>) => Record<string, any>); //#endregion
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
interface RouteLocationTyped<RouteMap extends RouteMapGeneric, Name extends keyof RouteMap> extends RouteLocationGeneric {
  name: Extract<Name, string | symbol>;
  params: RouteMap[Name]['params'];
}
/**
 * List of all possible {@link RouteLocation} indexed by the route name.
 * @internal
 */
type RouteLocationTypedList<RouteMap extends RouteMapGeneric = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationTyped<RouteMap, N> };
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
interface RouteLocationNormalizedTyped<RouteMap extends RouteMapGeneric = RouteMapGeneric, Name extends keyof RouteMap = keyof RouteMap> extends RouteLocationNormalizedGeneric {
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
type RouteLocationNormalizedTypedList<RouteMap extends RouteMapGeneric = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationNormalizedTyped<RouteMap, N> };
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
interface RouteLocationNormalizedLoadedTyped<RouteMap extends RouteMapGeneric = RouteMapGeneric, Name extends keyof RouteMap = keyof RouteMap> extends RouteLocationNormalizedLoadedGeneric {
  name: Extract<Name, string | symbol>;
  params: RouteMap[Name]['params'];
}
/**
 * List of all possible {@link RouteLocationNormalizedLoaded} indexed by the route name.
 * @internal
 */
type RouteLocationNormalizedLoadedTypedList<RouteMap extends RouteMapGeneric = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationNormalizedLoadedTyped<RouteMap, N> };
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
interface RouteLocationAsRelativeTyped<RouteMap extends RouteMapGeneric = RouteMapGeneric, Name extends keyof RouteMap = keyof RouteMap> extends RouteLocationAsRelativeGeneric {
  name?: Extract<Name, string | symbol>;
  params?: RouteMap[Name]['paramsRaw'];
}
/**
 * List of all possible {@link RouteLocationAsRelative} indexed by the route name.
 * @internal
 */
type RouteLocationAsRelativeTypedList<RouteMap extends RouteMapGeneric = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationAsRelativeTyped<RouteMap, N> };
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
interface RouteLocationAsPathTyped<RouteMap extends RouteMapGeneric = RouteMapGeneric, Name extends keyof RouteMap = keyof RouteMap> extends RouteLocationAsPathGeneric {
  path: _LiteralUnion<RouteMap[Name]['path']>;
}
/**
 * List of all possible {@link RouteLocationAsPath} indexed by the route name.
 * @internal
 */
type RouteLocationAsPathTypedList<RouteMap extends RouteMapGeneric = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationAsPathTyped<RouteMap, N> };
/**
 * Helper to generate a type safe version of the {@link RouteLocationAsString} type.
 */
type RouteLocationAsStringTyped<RouteMap extends RouteMapGeneric = RouteMapGeneric, Name extends keyof RouteMap = keyof RouteMap> = RouteMap[Name]['path'];
/**
 * List of all possible {@link RouteLocationAsString} indexed by the route name.
 * @internal
 */
type RouteLocationAsStringTypedList<RouteMap extends RouteMapGeneric = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationAsStringTyped<RouteMap, N> };
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
interface RouteLocationResolvedTyped<RouteMap extends RouteMapGeneric, Name extends keyof RouteMap> extends RouteLocationTyped<RouteMap, Name> {
  /**
   * Resolved `href` for the route location that will be set on the `<a href="...">`.
   */
  href: string;
}
/**
 * List of all possible {@link RouteLocationResolved} indexed by the route name.
 * @internal
 */
type RouteLocationResolvedTypedList<RouteMap extends RouteMapGeneric = RouteMapGeneric> = { [N in keyof RouteMap]: RouteLocationResolvedTyped<RouteMap, N> };
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
type RouteLocationRaw<Name extends keyof RouteMap = keyof RouteMap> = RouteMapGeneric extends RouteMap ? RouteLocationAsString | RouteLocationAsRelativeGeneric | RouteLocationAsPathGeneric : _LiteralUnion<RouteLocationAsStringTypedList<RouteMap>[Name], string> | RouteLocationAsRelativeTypedList<RouteMap>[Name] | RouteLocationAsPathTypedList<RouteMap>[Name]; //#endregion
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
  (this: T, to: RouteLocationNormalized, from: RouteLocationNormalizedLoaded, next: NavigationGuardNext): _Awaitable<NavigationGuardReturn>;
}
/**
 * Navigation Guard.
 */
interface NavigationGuard {
  (to: RouteLocationNormalized, from: RouteLocationNormalizedLoaded, next: NavigationGuardNext): _Awaitable<NavigationGuardReturn>;
}
/**
 * Navigation hook triggered after a navigation is settled.
 */
interface NavigationHookAfter {
  (to: RouteLocationNormalized, from: RouteLocationNormalizedLoaded, failure?: NavigationFailure | void): unknown;
}
/**
 * `next()` callback passed to navigation guards.
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
type NavigationGuardNextCallback = (vm: ComponentPublicInstance) => unknown; //#endregion
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
type RouteRecord = RouteRecordNormalized; //#endregion
//#region src/matcher/pathParserRanker.d.ts
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
type PathParserOptions = Pick<_PathParserOptions, 'end' | 'sensitive' | 'strict'>; //#endregion
//#region src/matcher/pathMatcher.d.ts
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
} //#endregion
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
} //#endregion
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
} //#endregion
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
type Awaitable<T> = T | PromiseLike<T>; //#endregion
//#region src/experimental/route-resolver/matchers/param-parsers/types.d.ts
/**
 * Defines a parser that can read a param from the url (string-based) and
 * transform it into a more complex type, or vice versa.
 *
 * @see MatcherPattern
 */
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
  beforeResolve(guard: NavigationGuardWithThis<undefined>): () => void;
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
//#endregion
//#region ../../node_modules/.pnpm/vue-router@4.6.0_vue@3.5.22_typescript@5.9.3_/node_modules/vue-router/dist/vue-router.d.mts
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
} //#endregion
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
}; //#endregion
//#region src/useApi.d.ts
/**
 * Returns the router instance. Equivalent to using `$router` inside
 * templates.
 */
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
} //#endregion
//#endregion
//#region src/rpc/global.d.ts
declare enum DevToolsMessagingEvents {
  INSPECTOR_TREE_UPDATED = "inspector-tree-updated",
  INSPECTOR_STATE_UPDATED = "inspector-state-updated",
  DEVTOOLS_STATE_UPDATED = "devtools-state-updated",
  ROUTER_INFO_UPDATED = "router-info-updated",
  TIMELINE_EVENT_UPDATED = "timeline-event-updated",
  INSPECTOR_UPDATED = "inspector-updated",
  ACTIVE_APP_UNMOUNTED = "active-app-updated",
  DESTROY_DEVTOOLS_CLIENT = "destroy-devtools-client",
  RELOAD_DEVTOOLS_CLIENT = "reload-devtools-client"
}
declare const functions: {
  on: (event: string, handler: Function) => void;
  off: (event: string, handler: Function) => void;
  once: (event: string, handler: Function) => void;
  emit: (event: string, ...args: any[]) => void;
  heartbeat: () => boolean;
  devtoolsState: () => {
    connected: boolean;
    clientConnected: boolean;
    vueVersion: string;
    tabs: _vue_devtools_kit0.CustomTab[];
    commands: _vue_devtools_kit0.CustomCommand[];
    vitePluginDetected: boolean;
    appRecords: {
      id: string;
      name: string;
      version: string | undefined;
      routerId: string | undefined;
      iframe: string | undefined;
    }[];
    activeAppRecordId: string;
    timelineLayersState: Record<string, boolean>;
  };
  getInspectorTree(payload: Pick<DevToolsV6PluginAPIHookPayloads[DevToolsV6PluginAPIHookKeys.GET_INSPECTOR_TREE], "inspectorId" | "filter">): Promise<string>;
  getInspectorState(payload: Pick<DevToolsV6PluginAPIHookPayloads[DevToolsV6PluginAPIHookKeys.GET_INSPECTOR_STATE], "inspectorId" | "nodeId">): Promise<string>;
  editInspectorState(payload: DevToolsV6PluginAPIHookPayloads[DevToolsV6PluginAPIHookKeys.EDIT_INSPECTOR_STATE]): Promise<void>;
  sendInspectorState(id: string): void;
  inspectComponentInspector(): Promise<string>;
  cancelInspectComponentInspector(): void;
  getComponentRenderCode(id: string): any;
  scrollToComponent(id: string): void;
  inspectDOM(id: string): void;
  getInspectorNodeActions(id: string): {
    icon: string;
    tooltip?: string;
    action: (nodeId: string) => void | Promise<void>;
  }[] | undefined;
  getInspectorActions(id: string): {
    icon: string;
    tooltip?: string;
    action: () => void | Promise<void>;
  }[] | undefined;
  updateTimelineLayersState(state: Record<string, boolean>): void;
  callInspectorNodeAction(inspectorId: string, actionIndex: number, nodeId: string): void;
  callInspectorAction(inspectorId: string, actionIndex: number): void;
  openInEditor(options: OpenInEditorOptions): void;
  checkVueInspectorDetected(): Promise<boolean>;
  enableVueInspector(): Promise<void>;
  toggleApp(id: string, options?: {
    inspectingComponent?: boolean;
  }): Promise<void>;
  updatePluginSettings(pluginId: string, key: string, value: string): void;
  getPluginSettings(pluginId: string): {
    options: Record<string, {
      label: string;
      description?: string;
    } & ({
      type: "boolean";
      defaultValue: boolean;
    } | {
      type: "choice";
      defaultValue: string | number;
      options: {
        value: string | number;
        label: string;
      }[];
      component?: "select" | "button-group";
    } | {
      type: "text";
      defaultValue: string;
    })> | null;
    values: any;
  };
  getRouterInfo(): _vue_devtools_kit0.RouterInfo;
  navigate(path: string): Promise<void | NavigationFailure | {} | undefined>;
  getMatchedRoutes(path: string): RouteRecordNormalized[];
  toggleClientConnected(state: boolean): void;
  getCustomInspector(): {
    id: string;
    label: string;
    logo: string;
    icon: string;
    packageName: string | undefined;
    homepage: string | undefined;
    pluginId: string;
  }[];
  getInspectorInfo(id: string): {
    id: string;
    label: string;
    logo: string | undefined;
    packageName: string | undefined;
    homepage: string | undefined;
    timelineLayers: {
      id: string;
      label: string;
      color: number;
    }[];
    treeFilterPlaceholder: string;
    stateFilterPlaceholder: string;
  } | undefined;
  highlighComponent(uid: string): Promise<any>;
  unhighlight(): Promise<any>;
  updateDevToolsClientDetected(params: Record<string, boolean>): void;
  initDevToolsServerListener(): void;
};
type RPCFunctions = typeof functions;
declare const rpc: {
  value: ReturnType<typeof getRpcClient<RPCFunctions>>;
  functions: ReturnType<typeof getRpcClient<RPCFunctions>>;
};
declare const rpcServer: {
  value: ReturnType<typeof getRpcServer<RPCFunctions>>;
  functions: ReturnType<typeof getRpcServer<RPCFunctions>>;
};
declare function onRpcConnected(callback: () => void): void;
declare function onRpcSeverReady(callback: () => void): void;
//#endregion
//#region ../../node_modules/.pnpm/vite@7.1.10_@types+node@24.7.2_jiti@2.5.1_sass-embedded@1.93.2_sass@1.93.2_terser@5.44.0_tsx@4.20.6_yaml@2.8.1/node_modules/vite/types/hmrPayload.d.ts
type HotPayload = ConnectedPayload | PingPayload | UpdatePayload | FullReloadPayload | CustomPayload | ErrorPayload | PrunePayload;
interface ConnectedPayload {
  type: 'connected';
}
interface PingPayload {
  type: 'ping';
}
interface UpdatePayload {
  type: 'update';
  updates: Update[];
}
interface Update {
  type: 'js-update' | 'css-update';
  path: string;
  acceptedPath: string;
  timestamp: number;
  /** @internal */
  explicitImportRequired?: boolean;
  /** @internal */
  isWithinCircularImport?: boolean;
  /** @internal */
  firstInvalidatedBy?: string;
  /** @internal */
  invalidates?: string[];
}
interface PrunePayload {
  type: 'prune';
  paths: string[];
}
interface FullReloadPayload {
  type: 'full-reload';
  path?: string;
  /** @internal */
  triggeredBy?: string;
}
interface CustomPayload {
  type: 'custom';
  event: string;
  data?: any;
}
interface ErrorPayload {
  type: 'error';
  err: {
    [name: string]: any;
    message: string;
    stack: string;
    id?: string;
    frame?: string;
    plugin?: string;
    pluginCode?: string;
    loc?: {
      file?: string;
      line: number;
      column: number;
    };
  };
}
//#endregion
//#region ../../node_modules/.pnpm/vite@7.1.10_@types+node@24.7.2_jiti@2.5.1_sass-embedded@1.93.2_sass@1.93.2_terser@5.44.0_tsx@4.20.6_yaml@2.8.1/node_modules/vite/dist/node/moduleRunnerTransport-BWUZBVLX.d.ts
//#region src/shared/invokeMethods.d.ts
interface FetchFunctionOptions {
  cached?: boolean;
  startOffset?: number;
}
type FetchResult = CachedFetchResult | ExternalFetchResult | ViteFetchResult;
interface CachedFetchResult {
  /**
   * If module cached in the runner, we can just confirm
   * it wasn't invalidated on the server side.
   */
  cache: true;
}
interface ExternalFetchResult {
  /**
   * The path to the externalized module starting with file://,
   * by default this will be imported via a dynamic "import"
   * instead of being transformed by vite and loaded with vite runner
   */
  externalize: string;
  /**
   * Type of the module. Will be used to determine if import statement is correct.
   * For example, if Vite needs to throw an error if variable is not actually exported
   */
  type: 'module' | 'commonjs' | 'builtin' | 'network';
}
interface ViteFetchResult {
  /**
   * Code that will be evaluated by vite runner
   * by default this will be wrapped in an async function
   */
  code: string;
  /**
   * File path of the module on disk.
   * This will be resolved as import.meta.url/filename
   * Will be equal to `null` for virtual modules
   */
  file: string | null;
  /**
   * Module ID in the server module graph.
   */
  id: string;
  /**
   * Module URL used in the import.
   */
  url: string;
  /**
   * Invalidate module on the client side.
   */
  invalidate: boolean;
}
//#endregion
//#region ../../node_modules/.pnpm/vite@7.1.10_@types+node@24.7.2_jiti@2.5.1_sass-embedded@1.93.2_sass@1.93.2_terser@5.44.0_tsx@4.20.6_yaml@2.8.1/node_modules/vite/types/customEvent.d.ts
interface CustomEventMap {
  'vite:beforeUpdate': UpdatePayload;
  'vite:afterUpdate': UpdatePayload;
  'vite:beforePrune': PrunePayload;
  'vite:beforeFullReload': FullReloadPayload;
  'vite:error': ErrorPayload;
  'vite:invalidate': InvalidatePayload;
  'vite:ws:connect': WebSocketConnectionPayload;
  'vite:ws:disconnect': WebSocketConnectionPayload;
}
interface WebSocketConnectionPayload {
  /**
   * @experimental
   * We expose this instance experimentally to see potential usage.
   * This might be removed in the future if we didn't find reasonable use cases.
   * If you find this useful, please open an issue with details so we can discuss and make it stable API.
   */
  // eslint-disable-next-line n/no-unsupported-features/node-builtins
  webSocket: WebSocket;
}
interface InvalidatePayload {
  path: string;
  message: string | undefined;
  firstInvalidatedBy: string;
}
/**
 * provides types for payloads of built-in Vite events
 */
type InferCustomEventPayload<T extends string> = T extends keyof CustomEventMap ? CustomEventMap[T] : any;
//#endregion
//#region ../../node_modules/.pnpm/@types+estree@1.0.8/node_modules/@types/estree/index.d.ts
// This definition file follows a somewhat unusual format. ESTree allows
// runtime type checks based on the `type` parameter. In order to explain this
// to typescript we want to use discriminated union types:
// https://github.com/Microsoft/TypeScript/pull/9163
//
// For ESTree this is a bit tricky because the high level interfaces like
// Node or Function are pulling double duty. We want to pass common fields down
// to the interfaces that extend them (like Identifier or
// ArrowFunctionExpression), but you can't extend a type union or enforce
// common fields on them. So we've split the high level interfaces into two
// types, a base type which passes down inherited fields, and a type union of
// all types which extend the base type. Only the type union is exported, and
// the union is how other types refer to the collection of inheriting types.
//
// This makes the definitions file here somewhat more difficult to maintain,
// but it has the notable advantage of making ESTree much easier to use as
// an end user.
interface BaseNodeWithoutComments {
  // Every leaf interface that extends BaseNode must specify a type property.
  // The type property should be a string literal. For example, Identifier
  // has: `type: "Identifier"`
  type: string;
  loc?: SourceLocation | null | undefined;
  range?: [number, number] | undefined;
}
interface BaseNode extends BaseNodeWithoutComments {
  leadingComments?: Comment$1[] | undefined;
  trailingComments?: Comment$1[] | undefined;
}
interface NodeMap {
  AssignmentProperty: AssignmentProperty;
  CatchClause: CatchClause;
  Class: Class;
  ClassBody: ClassBody;
  Expression: Expression;
  Function: Function$1;
  Identifier: Identifier;
  Literal: Literal;
  MethodDefinition: MethodDefinition;
  ModuleDeclaration: ModuleDeclaration;
  ModuleSpecifier: ModuleSpecifier;
  Pattern: Pattern;
  PrivateIdentifier: PrivateIdentifier;
  Program: Program;
  Property: Property;
  PropertyDefinition: PropertyDefinition;
  SpreadElement: SpreadElement;
  Statement: Statement;
  Super: Super;
  SwitchCase: SwitchCase;
  TemplateElement: TemplateElement;
  VariableDeclarator: VariableDeclarator;
}
type Node$1 = NodeMap[keyof NodeMap];
interface Comment$1 extends BaseNodeWithoutComments {
  type: "Line" | "Block";
  value: string;
}
interface SourceLocation {
  source?: string | null | undefined;
  start: Position$1;
  end: Position$1;
}
interface Position$1 {
  /** >= 1 */
  line: number;
  /** >= 0 */
  column: number;
}
interface Program extends BaseNode {
  type: "Program";
  sourceType: "script" | "module";
  body: Array<Directive | Statement | ModuleDeclaration>;
  comments?: Comment$1[] | undefined;
}
interface Directive extends BaseNode {
  type: "ExpressionStatement";
  expression: Literal;
  directive: string;
}
interface BaseFunction extends BaseNode {
  params: Pattern[];
  generator?: boolean | undefined;
  async?: boolean | undefined; // The body is either BlockStatement or Expression because arrow functions
  // can have a body that's either. FunctionDeclarations and
  // FunctionExpressions have only BlockStatement bodies.
  body: BlockStatement | Expression;
}
type Function$1 = FunctionDeclaration | FunctionExpression | ArrowFunctionExpression;
type Statement = ExpressionStatement | BlockStatement | StaticBlock | EmptyStatement | DebuggerStatement | WithStatement | ReturnStatement | LabeledStatement | BreakStatement | ContinueStatement | IfStatement | SwitchStatement | ThrowStatement | TryStatement | WhileStatement | DoWhileStatement | ForStatement | ForInStatement | ForOfStatement | Declaration$1;
interface BaseStatement extends BaseNode {}
interface EmptyStatement extends BaseStatement {
  type: "EmptyStatement";
}
interface BlockStatement extends BaseStatement {
  type: "BlockStatement";
  body: Statement[];
  innerComments?: Comment$1[] | undefined;
}
interface StaticBlock extends Omit<BlockStatement, "type"> {
  type: "StaticBlock";
}
interface ExpressionStatement extends BaseStatement {
  type: "ExpressionStatement";
  expression: Expression;
}
interface IfStatement extends BaseStatement {
  type: "IfStatement";
  test: Expression;
  consequent: Statement;
  alternate?: Statement | null | undefined;
}
interface LabeledStatement extends BaseStatement {
  type: "LabeledStatement";
  label: Identifier;
  body: Statement;
}
interface BreakStatement extends BaseStatement {
  type: "BreakStatement";
  label?: Identifier | null | undefined;
}
interface ContinueStatement extends BaseStatement {
  type: "ContinueStatement";
  label?: Identifier | null | undefined;
}
interface WithStatement extends BaseStatement {
  type: "WithStatement";
  object: Expression;
  body: Statement;
}
interface SwitchStatement extends BaseStatement {
  type: "SwitchStatement";
  discriminant: Expression;
  cases: SwitchCase[];
}
interface ReturnStatement extends BaseStatement {
  type: "ReturnStatement";
  argument?: Expression | null | undefined;
}
interface ThrowStatement extends BaseStatement {
  type: "ThrowStatement";
  argument: Expression;
}
interface TryStatement extends BaseStatement {
  type: "TryStatement";
  block: BlockStatement;
  handler?: CatchClause | null | undefined;
  finalizer?: BlockStatement | null | undefined;
}
interface WhileStatement extends BaseStatement {
  type: "WhileStatement";
  test: Expression;
  body: Statement;
}
interface DoWhileStatement extends BaseStatement {
  type: "DoWhileStatement";
  body: Statement;
  test: Expression;
}
interface ForStatement extends BaseStatement {
  type: "ForStatement";
  init?: VariableDeclaration | Expression | null | undefined;
  test?: Expression | null | undefined;
  update?: Expression | null | undefined;
  body: Statement;
}
interface BaseForXStatement extends BaseStatement {
  left: VariableDeclaration | Pattern;
  right: Expression;
  body: Statement;
}
interface ForInStatement extends BaseForXStatement {
  type: "ForInStatement";
}
interface DebuggerStatement extends BaseStatement {
  type: "DebuggerStatement";
}
type Declaration$1 = FunctionDeclaration | VariableDeclaration | ClassDeclaration;
interface BaseDeclaration extends BaseStatement {}
interface MaybeNamedFunctionDeclaration extends BaseFunction, BaseDeclaration {
  type: "FunctionDeclaration";
  /** It is null when a function declaration is a part of the `export default function` statement */
  id: Identifier | null;
  body: BlockStatement;
}
interface FunctionDeclaration extends MaybeNamedFunctionDeclaration {
  id: Identifier;
}
interface VariableDeclaration extends BaseDeclaration {
  type: "VariableDeclaration";
  declarations: VariableDeclarator[];
  kind: "var" | "let" | "const" | "using" | "await using";
}
interface VariableDeclarator extends BaseNode {
  type: "VariableDeclarator";
  id: Pattern;
  init?: Expression | null | undefined;
}
interface ExpressionMap {
  ArrayExpression: ArrayExpression;
  ArrowFunctionExpression: ArrowFunctionExpression;
  AssignmentExpression: AssignmentExpression;
  AwaitExpression: AwaitExpression;
  BinaryExpression: BinaryExpression;
  CallExpression: CallExpression;
  ChainExpression: ChainExpression;
  ClassExpression: ClassExpression;
  ConditionalExpression: ConditionalExpression;
  FunctionExpression: FunctionExpression;
  Identifier: Identifier;
  ImportExpression: ImportExpression;
  Literal: Literal;
  LogicalExpression: LogicalExpression;
  MemberExpression: MemberExpression;
  MetaProperty: MetaProperty;
  NewExpression: NewExpression;
  ObjectExpression: ObjectExpression;
  SequenceExpression: SequenceExpression;
  TaggedTemplateExpression: TaggedTemplateExpression;
  TemplateLiteral: TemplateLiteral;
  ThisExpression: ThisExpression;
  UnaryExpression: UnaryExpression;
  UpdateExpression: UpdateExpression;
  YieldExpression: YieldExpression;
}
type Expression = ExpressionMap[keyof ExpressionMap];
interface BaseExpression extends BaseNode {}
type ChainElement = SimpleCallExpression | MemberExpression;
interface ChainExpression extends BaseExpression {
  type: "ChainExpression";
  expression: ChainElement;
}
interface ThisExpression extends BaseExpression {
  type: "ThisExpression";
}
interface ArrayExpression extends BaseExpression {
  type: "ArrayExpression";
  elements: Array<Expression | SpreadElement | null>;
}
interface ObjectExpression extends BaseExpression {
  type: "ObjectExpression";
  properties: Array<Property | SpreadElement>;
}
interface PrivateIdentifier extends BaseNode {
  type: "PrivateIdentifier";
  name: string;
}
interface Property extends BaseNode {
  type: "Property";
  key: Expression | PrivateIdentifier;
  value: Expression | Pattern; // Could be an AssignmentProperty
  kind: "init" | "get" | "set";
  method: boolean;
  shorthand: boolean;
  computed: boolean;
}
interface PropertyDefinition extends BaseNode {
  type: "PropertyDefinition";
  key: Expression | PrivateIdentifier;
  value?: Expression | null | undefined;
  computed: boolean;
  static: boolean;
}
interface FunctionExpression extends BaseFunction, BaseExpression {
  id?: Identifier | null | undefined;
  type: "FunctionExpression";
  body: BlockStatement;
}
interface SequenceExpression extends BaseExpression {
  type: "SequenceExpression";
  expressions: Expression[];
}
interface UnaryExpression extends BaseExpression {
  type: "UnaryExpression";
  operator: UnaryOperator;
  prefix: true;
  argument: Expression;
}
interface BinaryExpression extends BaseExpression {
  type: "BinaryExpression";
  operator: BinaryOperator;
  left: Expression | PrivateIdentifier;
  right: Expression;
}
interface AssignmentExpression extends BaseExpression {
  type: "AssignmentExpression";
  operator: AssignmentOperator;
  left: Pattern | MemberExpression;
  right: Expression;
}
interface UpdateExpression extends BaseExpression {
  type: "UpdateExpression";
  operator: UpdateOperator;
  argument: Expression;
  prefix: boolean;
}
interface LogicalExpression extends BaseExpression {
  type: "LogicalExpression";
  operator: LogicalOperator;
  left: Expression;
  right: Expression;
}
interface ConditionalExpression extends BaseExpression {
  type: "ConditionalExpression";
  test: Expression;
  alternate: Expression;
  consequent: Expression;
}
interface BaseCallExpression extends BaseExpression {
  callee: Expression | Super;
  arguments: Array<Expression | SpreadElement>;
}
type CallExpression = SimpleCallExpression | NewExpression;
interface SimpleCallExpression extends BaseCallExpression {
  type: "CallExpression";
  optional: boolean;
}
interface NewExpression extends BaseCallExpression {
  type: "NewExpression";
}
interface MemberExpression extends BaseExpression, BasePattern {
  type: "MemberExpression";
  object: Expression | Super;
  property: Expression | PrivateIdentifier;
  computed: boolean;
  optional: boolean;
}
type Pattern = Identifier | ObjectPattern | ArrayPattern | RestElement | AssignmentPattern | MemberExpression;
interface BasePattern extends BaseNode {}
interface SwitchCase extends BaseNode {
  type: "SwitchCase";
  test?: Expression | null | undefined;
  consequent: Statement[];
}
interface CatchClause extends BaseNode {
  type: "CatchClause";
  param: Pattern | null;
  body: BlockStatement;
}
interface Identifier extends BaseNode, BaseExpression, BasePattern {
  type: "Identifier";
  name: string;
}
type Literal = SimpleLiteral | RegExpLiteral | BigIntLiteral;
interface SimpleLiteral extends BaseNode, BaseExpression {
  type: "Literal";
  value: string | boolean | number | null;
  raw?: string | undefined;
}
interface RegExpLiteral extends BaseNode, BaseExpression {
  type: "Literal";
  value?: RegExp | null | undefined;
  regex: {
    pattern: string;
    flags: string;
  };
  raw?: string | undefined;
}
interface BigIntLiteral extends BaseNode, BaseExpression {
  type: "Literal";
  value?: bigint | null | undefined;
  bigint: string;
  raw?: string | undefined;
}
type UnaryOperator = "-" | "+" | "!" | "~" | "typeof" | "void" | "delete";
type BinaryOperator = "==" | "!=" | "===" | "!==" | "<" | "<=" | ">" | ">=" | "<<" | ">>" | ">>>" | "+" | "-" | "*" | "/" | "%" | "**" | "|" | "^" | "&" | "in" | "instanceof";
type LogicalOperator = "||" | "&&" | "??";
type AssignmentOperator = "=" | "+=" | "-=" | "*=" | "/=" | "%=" | "**=" | "<<=" | ">>=" | ">>>=" | "|=" | "^=" | "&=" | "||=" | "&&=" | "??=";
type UpdateOperator = "++" | "--";
interface ForOfStatement extends BaseForXStatement {
  type: "ForOfStatement";
  await: boolean;
}
interface Super extends BaseNode {
  type: "Super";
}
interface SpreadElement extends BaseNode {
  type: "SpreadElement";
  argument: Expression;
}
interface ArrowFunctionExpression extends BaseExpression, BaseFunction {
  type: "ArrowFunctionExpression";
  expression: boolean;
  body: BlockStatement | Expression;
}
interface YieldExpression extends BaseExpression {
  type: "YieldExpression";
  argument?: Expression | null | undefined;
  delegate: boolean;
}
interface TemplateLiteral extends BaseExpression {
  type: "TemplateLiteral";
  quasis: TemplateElement[];
  expressions: Expression[];
}
interface TaggedTemplateExpression extends BaseExpression {
  type: "TaggedTemplateExpression";
  tag: Expression;
  quasi: TemplateLiteral;
}
interface TemplateElement extends BaseNode {
  type: "TemplateElement";
  tail: boolean;
  value: {
    /** It is null when the template literal is tagged and the text has an invalid escape (e.g. - tag`\unicode and \u{55}`) */cooked?: string | null | undefined;
    raw: string;
  };
}
interface AssignmentProperty extends Property {
  value: Pattern;
  kind: "init";
  method: boolean; // false
}
interface ObjectPattern extends BasePattern {
  type: "ObjectPattern";
  properties: Array<AssignmentProperty | RestElement>;
}
interface ArrayPattern extends BasePattern {
  type: "ArrayPattern";
  elements: Array<Pattern | null>;
}
interface RestElement extends BasePattern {
  type: "RestElement";
  argument: Pattern;
}
interface AssignmentPattern extends BasePattern {
  type: "AssignmentPattern";
  left: Pattern;
  right: Expression;
}
type Class = ClassDeclaration | ClassExpression;
interface BaseClass extends BaseNode {
  superClass?: Expression | null | undefined;
  body: ClassBody;
}
interface ClassBody extends BaseNode {
  type: "ClassBody";
  body: Array<MethodDefinition | PropertyDefinition | StaticBlock>;
}
interface MethodDefinition extends BaseNode {
  type: "MethodDefinition";
  key: Expression | PrivateIdentifier;
  value: FunctionExpression;
  kind: "constructor" | "method" | "get" | "set";
  computed: boolean;
  static: boolean;
}
interface MaybeNamedClassDeclaration extends BaseClass, BaseDeclaration {
  type: "ClassDeclaration";
  /** It is null when a class declaration is a part of the `export default class` statement */
  id: Identifier | null;
}
interface ClassDeclaration extends MaybeNamedClassDeclaration {
  id: Identifier;
}
interface ClassExpression extends BaseClass, BaseExpression {
  type: "ClassExpression";
  id?: Identifier | null | undefined;
}
interface MetaProperty extends BaseExpression {
  type: "MetaProperty";
  meta: Identifier;
  property: Identifier;
}
type ModuleDeclaration = ImportDeclaration | ExportNamedDeclaration | ExportDefaultDeclaration | ExportAllDeclaration;
interface BaseModuleDeclaration extends BaseNode {}
type ModuleSpecifier = ImportSpecifier | ImportDefaultSpecifier | ImportNamespaceSpecifier | ExportSpecifier;
interface BaseModuleSpecifier extends BaseNode {
  local: Identifier;
}
interface ImportDeclaration extends BaseModuleDeclaration {
  type: "ImportDeclaration";
  specifiers: Array<ImportSpecifier | ImportDefaultSpecifier | ImportNamespaceSpecifier>;
  attributes: ImportAttribute[];
  source: Literal;
}
interface ImportSpecifier extends BaseModuleSpecifier {
  type: "ImportSpecifier";
  imported: Identifier | Literal;
}
interface ImportAttribute extends BaseNode {
  type: "ImportAttribute";
  key: Identifier | Literal;
  value: Literal;
}
interface ImportExpression extends BaseExpression {
  type: "ImportExpression";
  source: Expression;
  options?: Expression | null | undefined;
}
interface ImportDefaultSpecifier extends BaseModuleSpecifier {
  type: "ImportDefaultSpecifier";
}
interface ImportNamespaceSpecifier extends BaseModuleSpecifier {
  type: "ImportNamespaceSpecifier";
}
interface ExportNamedDeclaration extends BaseModuleDeclaration {
  type: "ExportNamedDeclaration";
  declaration?: Declaration$1 | null | undefined;
  specifiers: ExportSpecifier[];
  attributes: ImportAttribute[];
  source?: Literal | null | undefined;
}
interface ExportSpecifier extends Omit<BaseModuleSpecifier, "local"> {
  type: "ExportSpecifier";
  local: Identifier | Literal;
  exported: Identifier | Literal;
}
interface ExportDefaultDeclaration extends BaseModuleDeclaration {
  type: "ExportDefaultDeclaration";
  declaration: MaybeNamedFunctionDeclaration | MaybeNamedClassDeclaration | Expression;
}
interface ExportAllDeclaration extends BaseModuleDeclaration {
  type: "ExportAllDeclaration";
  exported: Identifier | Literal | null;
  attributes: ImportAttribute[];
  source: Literal;
}
interface AwaitExpression extends BaseExpression {
  type: "AwaitExpression";
  argument: Expression;
}
//#endregion
//#region ../../node_modules/.pnpm/rollup@4.50.1/node_modules/rollup/dist/rollup.d.ts
declare module 'estree' {
  export interface Decorator extends BaseNode {
    type: 'Decorator';
    expression: Expression;
  }
  interface PropertyDefinition {
    decorators: undefined[];
  }
  interface MethodDefinition {
    decorators: undefined[];
  }
  interface BaseClass {
    decorators: undefined[];
  }
}
// utils
type NullValue = null | undefined | void;
type MaybeArray<T> = T | T[];
type MaybePromise<T> = T | Promise<T>;
type PartialNull<T> = { [P in keyof T]: T[P] | null };
interface RollupError extends RollupLog {
  name?: string | undefined;
  stack?: string | undefined;
  watchFiles?: string[] | undefined;
}
interface RollupLog {
  binding?: string | undefined;
  cause?: unknown | undefined;
  code?: string | undefined;
  exporter?: string | undefined;
  frame?: string | undefined;
  hook?: string | undefined;
  id?: string | undefined;
  ids?: string[] | undefined;
  loc?: {
    column: number;
    file?: string | undefined;
    line: number;
  };
  message: string;
  meta?: any | undefined;
  names?: string[] | undefined;
  plugin?: string | undefined;
  pluginCode?: unknown | undefined;
  pos?: number | undefined;
  reexporter?: string | undefined;
  stack?: string | undefined;
  url?: string | undefined;
}
type LogLevel$2 = 'warn' | 'info' | 'debug';
type LogLevelOption = LogLevel$2 | 'silent';
type SourceMapSegment$1 = [number] | [number, number, number, number] | [number, number, number, number, number];
interface ExistingDecodedSourceMap {
  file?: string | undefined;
  readonly mappings: SourceMapSegment$1[][];
  names: string[];
  sourceRoot?: string | undefined;
  sources: string[];
  sourcesContent?: string[] | undefined;
  version: number;
  x_google_ignoreList?: number[] | undefined;
}
interface ExistingRawSourceMap {
  file?: string | undefined;
  mappings: string;
  names: string[];
  sourceRoot?: string | undefined;
  sources: string[];
  sourcesContent?: string[] | undefined;
  version: number;
  x_google_ignoreList?: number[] | undefined;
}
type DecodedSourceMapOrMissing = {
  missing: true;
  plugin: string;
} | (ExistingDecodedSourceMap & {
  missing?: false | undefined;
});
interface SourceMap$2 {
  file: string;
  mappings: string;
  names: string[];
  sources: string[];
  sourcesContent?: string[] | undefined;
  version: number;
  debugId?: string | undefined;
  toString(): string;
  toUrl(): string;
}
type SourceMapInput$1 = ExistingRawSourceMap | string | null | {
  mappings: '';
};
interface ModuleOptions {
  attributes: Record<string, string>;
  meta: CustomPluginOptions;
  moduleSideEffects: boolean | 'no-treeshake';
  syntheticNamedExports: boolean | string;
}
interface SourceDescription extends Partial<PartialNull<ModuleOptions>> {
  ast?: ProgramNode | undefined;
  code: string;
  map?: SourceMapInput$1 | undefined;
}
interface TransformModuleJSON {
  ast?: ProgramNode | undefined;
  code: string; // note if plugins use new this.cache to opt-out auto transform cache
  customTransformCache: boolean;
  originalCode: string;
  originalSourcemap: ExistingDecodedSourceMap | null;
  sourcemapChain: DecodedSourceMapOrMissing[];
  transformDependencies: string[];
}
interface ModuleJSON extends TransformModuleJSON, ModuleOptions {
  ast: ProgramNode;
  dependencies: string[];
  id: string;
  resolvedIds: ResolvedIdMap;
  transformFiles: EmittedFile[] | undefined;
}
interface PluginCache {
  delete(id: string): boolean;
  get<T = any>(id: string): T;
  has(id: string): boolean;
  set<T = any>(id: string, value: T): void;
}
type LoggingFunction = (log: RollupLog | string | (() => RollupLog | string)) => void;
interface MinimalPluginContext {
  debug: LoggingFunction;
  error: (error: RollupError | string) => never;
  info: LoggingFunction;
  meta: PluginContextMeta;
  warn: LoggingFunction;
}
interface EmittedAsset {
  fileName?: string | undefined;
  name?: string | undefined;
  needsCodeReference?: boolean | undefined;
  originalFileName?: string | null | undefined;
  source?: string | Uint8Array | undefined;
  type: 'asset';
}
interface EmittedChunk {
  fileName?: string | undefined;
  id: string;
  implicitlyLoadedAfterOneOf?: string[] | undefined;
  importer?: string | undefined;
  name?: string | undefined;
  preserveSignature?: PreserveEntrySignaturesOption | undefined;
  type: 'chunk';
}
interface EmittedPrebuiltChunk {
  code: string;
  exports?: string[] | undefined;
  fileName: string;
  map?: SourceMap$2 | undefined;
  sourcemapFileName?: string | undefined;
  type: 'prebuilt-chunk';
}
type EmittedFile = EmittedAsset | EmittedChunk | EmittedPrebuiltChunk;
type EmitFile = (emittedFile: EmittedFile) => string;
interface ModuleInfo$1 extends ModuleOptions {
  ast: ProgramNode | null;
  code: string | null;
  dynamicImporters: readonly string[];
  dynamicallyImportedIdResolutions: readonly ResolvedId[];
  dynamicallyImportedIds: readonly string[];
  exportedBindings: Record<string, string[]> | null;
  exports: string[] | null;
  hasDefaultExport: boolean | null;
  id: string;
  implicitlyLoadedAfterOneOf: readonly string[];
  implicitlyLoadedBefore: readonly string[];
  importedIdResolutions: readonly ResolvedId[];
  importedIds: readonly string[];
  importers: readonly string[];
  isEntry: boolean;
  isExternal: boolean;
  isIncluded: boolean | null;
}
type GetModuleInfo = (moduleId: string) => ModuleInfo$1 | null;
// eslint-disable-next-line @typescript-eslint/consistent-indexed-object-style -- this is an interface so that it can be extended by plugins
interface CustomPluginOptions {
  [plugin: string]: any;
}
type LoggingFunctionWithPosition = (log: RollupLog | string | (() => RollupLog | string), pos?: number | {
  column: number;
  line: number;
}) => void;
type ParseAst = (input: string, options?: {
  allowReturnOutsideFunction?: boolean;
  jsx?: boolean;
}) => ProgramNode;
// declare AbortSignal here for environments without DOM lib or @types/node
declare global {
  // eslint-disable-next-line @typescript-eslint/no-empty-object-type
  interface AbortSignal {}
}
interface PluginContext extends MinimalPluginContext {
  addWatchFile: (id: string) => void;
  cache: PluginCache;
  debug: LoggingFunction;
  emitFile: EmitFile;
  error: (error: RollupError | string) => never;
  fs: RollupFsModule;
  getFileName: (fileReferenceId: string) => string;
  getModuleIds: () => IterableIterator<string>;
  getModuleInfo: GetModuleInfo;
  getWatchFiles: () => string[];
  info: LoggingFunction;
  load: (options: {
    id: string;
    resolveDependencies?: boolean;
  } & Partial<PartialNull<ModuleOptions>>) => Promise<ModuleInfo$1>;
  parse: ParseAst;
  resolve: (source: string, importer?: string, options?: {
    attributes?: Record<string, string>;
    custom?: CustomPluginOptions;
    isEntry?: boolean;
    skipSelf?: boolean;
  }) => Promise<ResolvedId | null>;
  setAssetSource: (assetReferenceId: string, source: string | Uint8Array) => void;
  warn: LoggingFunction;
}
interface PluginContextMeta {
  rollupVersion: string;
  watchMode: boolean;
}
type StringOrRegExp = string | RegExp;
type StringFilter$1<Value = StringOrRegExp> = MaybeArray<Value> | {
  include?: MaybeArray<Value> | undefined;
  exclude?: MaybeArray<Value> | undefined;
};
interface HookFilter {
  id?: StringFilter$1 | undefined;
  code?: StringFilter$1 | undefined;
}
interface ResolvedId extends ModuleOptions {
  external: boolean | 'absolute';
  id: string;
  resolvedBy: string;
}
type ResolvedIdMap = Record<string, ResolvedId>;
interface PartialResolvedId extends Partial<PartialNull<ModuleOptions>> {
  external?: boolean | 'absolute' | 'relative' | undefined;
  id: string;
  resolvedBy?: string | undefined;
}
type ResolveIdResult = string | NullValue | false | PartialResolvedId;
type ResolveIdHook = (this: PluginContext, source: string, importer: string | undefined, options: {
  attributes: Record<string, string>;
  custom?: CustomPluginOptions;
  isEntry: boolean;
}) => ResolveIdResult;
type ShouldTransformCachedModuleHook = (this: PluginContext, options: {
  ast: ProgramNode;
  code: string;
  id: string;
  meta: CustomPluginOptions;
  moduleSideEffects: boolean | 'no-treeshake';
  resolvedSources: ResolvedIdMap;
  syntheticNamedExports: boolean | string;
}) => boolean | NullValue;
type IsExternal = (source: string, importer: string | undefined, isResolved: boolean) => boolean;
type HasModuleSideEffects = (id: string, external: boolean) => boolean;
type LoadResult = SourceDescription | string | NullValue;
type LoadHook = (this: PluginContext, id: string) => LoadResult;
interface TransformPluginContext extends PluginContext {
  debug: LoggingFunctionWithPosition;
  error: (error: RollupError | string, pos?: number | {
    column: number;
    line: number;
  }) => never;
  getCombinedSourcemap: () => SourceMap$2;
  info: LoggingFunctionWithPosition;
  warn: LoggingFunctionWithPosition;
}
type TransformResult$2 = string | NullValue | Partial<SourceDescription>;
type TransformHook = (this: TransformPluginContext, code: string, id: string) => TransformResult$2;
type ModuleParsedHook = (this: PluginContext, info: ModuleInfo$1) => void;
type RenderChunkHook = (this: PluginContext, code: string, chunk: RenderedChunk, options: NormalizedOutputOptions, meta: {
  chunks: Record<string, RenderedChunk>;
}) => {
  code: string;
  map?: SourceMapInput$1;
} | string | NullValue;
type ResolveDynamicImportHook = (this: PluginContext, specifier: string | AstNode, importer: string, options: {
  attributes: Record<string, string>;
}) => ResolveIdResult;
type ResolveImportMetaHook = (this: PluginContext, property: string | null, options: {
  chunkId: string;
  format: InternalModuleFormat;
  moduleId: string;
}) => string | NullValue;
type ResolveFileUrlHook = (this: PluginContext, options: {
  chunkId: string;
  fileName: string;
  format: InternalModuleFormat;
  moduleId: string;
  referenceId: string;
  relativePath: string;
}) => string | NullValue;
type AddonHookFunction = (this: PluginContext, chunk: RenderedChunk) => string | Promise<string>;
type AddonHook = string | AddonHookFunction;
type ChangeEvent = 'create' | 'update' | 'delete';
type WatchChangeHook = (this: PluginContext, id: string, change: {
  event: ChangeEvent;
}) => void;
type OutputBundle = Record<string, OutputAsset | OutputChunk>;
type PreRenderedChunkWithFileName = PreRenderedChunk & {
  fileName: string;
};
interface ImportedInternalChunk {
  type: 'internal';
  fileName: string;
  resolvedImportPath: string;
  chunk: PreRenderedChunk;
}
interface ImportedExternalChunk {
  type: 'external';
  fileName: string;
  resolvedImportPath: string;
}
type DynamicImportTargetChunk = ImportedInternalChunk | ImportedExternalChunk;
interface FunctionPluginHooks {
  augmentChunkHash: (this: PluginContext, chunk: RenderedChunk) => string | void;
  buildEnd: (this: PluginContext, error?: Error) => void;
  buildStart: (this: PluginContext, options: NormalizedInputOptions) => void;
  closeBundle: (this: PluginContext, error?: Error) => void;
  closeWatcher: (this: PluginContext) => void;
  generateBundle: (this: PluginContext, options: NormalizedOutputOptions, bundle: OutputBundle, isWrite: boolean) => void;
  load: LoadHook;
  moduleParsed: ModuleParsedHook;
  onLog: (this: MinimalPluginContext, level: LogLevel$2, log: RollupLog) => boolean | NullValue;
  options: (this: MinimalPluginContext, options: InputOptions) => InputOptions | NullValue;
  outputOptions: (this: PluginContext, options: OutputOptions) => OutputOptions | NullValue;
  renderChunk: RenderChunkHook;
  renderDynamicImport: (this: PluginContext, options: {
    customResolution: string | null;
    format: InternalModuleFormat;
    moduleId: string;
    targetModuleId: string | null;
    chunk: PreRenderedChunkWithFileName;
    targetChunk: PreRenderedChunkWithFileName | null;
    getTargetChunkImports: () => DynamicImportTargetChunk[] | null;
  }) => {
    left: string;
    right: string;
  } | NullValue;
  renderError: (this: PluginContext, error?: Error) => void;
  renderStart: (this: PluginContext, outputOptions: NormalizedOutputOptions, inputOptions: NormalizedInputOptions) => void;
  resolveDynamicImport: ResolveDynamicImportHook;
  resolveFileUrl: ResolveFileUrlHook;
  resolveId: ResolveIdHook;
  resolveImportMeta: ResolveImportMetaHook;
  shouldTransformCachedModule: ShouldTransformCachedModuleHook;
  transform: TransformHook;
  watchChange: WatchChangeHook;
  writeBundle: (this: PluginContext, options: NormalizedOutputOptions, bundle: OutputBundle) => void;
}
type OutputPluginHooks = 'augmentChunkHash' | 'generateBundle' | 'outputOptions' | 'renderChunk' | 'renderDynamicImport' | 'renderError' | 'renderStart' | 'resolveFileUrl' | 'resolveImportMeta' | 'writeBundle';
type SyncPluginHooks = 'augmentChunkHash' | 'onLog' | 'outputOptions' | 'renderDynamicImport' | 'resolveFileUrl' | 'resolveImportMeta';
type AsyncPluginHooks = Exclude<keyof FunctionPluginHooks, SyncPluginHooks>;
type FirstPluginHooks = 'load' | 'renderDynamicImport' | 'resolveDynamicImport' | 'resolveFileUrl' | 'resolveId' | 'resolveImportMeta' | 'shouldTransformCachedModule';
type SequentialPluginHooks = 'augmentChunkHash' | 'generateBundle' | 'onLog' | 'options' | 'outputOptions' | 'renderChunk' | 'transform';
type ParallelPluginHooks = Exclude<keyof FunctionPluginHooks | AddonHooks, FirstPluginHooks | SequentialPluginHooks>;
type AddonHooks = 'banner' | 'footer' | 'intro' | 'outro';
type MakeAsync<Function_> = Function_ extends ((this: infer This, ...parameters: infer Arguments) => infer Return) ? (this: This, ...parameters: Arguments) => Return | Promise<Return> : never; // eslint-disable-next-line @typescript-eslint/no-empty-object-type
type ObjectHook<T, O = {}> = T | ({
  handler: T;
  order?: 'pre' | 'post' | null;
} & O);
type HookFilterExtension<K extends keyof FunctionPluginHooks> = K extends 'transform' ? {
  filter?: HookFilter | undefined;
} : K extends 'load' ? {
  filter?: Pick<HookFilter, 'id'> | undefined;
} : K extends 'resolveId' ? {
  filter?: {
    id?: StringFilter$1<RegExp> | undefined;
  };
} | undefined : // eslint-disable-next-line @typescript-eslint/no-empty-object-type
{};
type PluginHooks = { [K in keyof FunctionPluginHooks]: ObjectHook<K extends AsyncPluginHooks ? MakeAsync<FunctionPluginHooks[K]> : FunctionPluginHooks[K], // eslint-disable-next-line @typescript-eslint/no-empty-object-type
HookFilterExtension<K> & (K extends ParallelPluginHooks ? {
  sequential?: boolean;
} : {})> };
interface OutputPlugin extends Partial<{ [K in OutputPluginHooks]: PluginHooks[K] }>, Partial<Record<AddonHooks, ObjectHook<AddonHook>>> {
  cacheKey?: string | undefined;
  name: string;
  version?: string | undefined;
}
interface Plugin$3<A = any> extends OutputPlugin, Partial<PluginHooks> {
  // for inter-plugin communication
  api?: A | undefined;
}
type JsxPreset = 'react' | 'react-jsx' | 'preserve' | 'preserve-react';
type NormalizedJsxOptions = NormalizedJsxPreserveOptions | NormalizedJsxClassicOptions | NormalizedJsxAutomaticOptions;
interface NormalizedJsxPreserveOptions {
  factory: string | null;
  fragment: string | null;
  importSource: string | null;
  mode: 'preserve';
}
interface NormalizedJsxClassicOptions {
  factory: string;
  fragment: string;
  importSource: string | null;
  mode: 'classic';
}
interface NormalizedJsxAutomaticOptions {
  factory: string;
  importSource: string | null;
  jsxImportSource: string;
  mode: 'automatic';
}
type JsxOptions = Partial<NormalizedJsxOptions> & {
  preset?: JsxPreset | undefined;
};
type TreeshakingPreset = 'smallest' | 'safest' | 'recommended';
interface NormalizedTreeshakingOptions {
  annotations: boolean;
  correctVarValueBeforeDeclaration: boolean;
  manualPureFunctions: readonly string[];
  moduleSideEffects: HasModuleSideEffects;
  propertyReadSideEffects: boolean | 'always';
  tryCatchDeoptimization: boolean;
  unknownGlobalSideEffects: boolean;
}
interface TreeshakingOptions extends Partial<Omit<NormalizedTreeshakingOptions, 'moduleSideEffects'>> {
  moduleSideEffects?: ModuleSideEffectsOption | undefined;
  preset?: TreeshakingPreset | undefined;
}
interface ManualChunkMeta {
  getModuleIds: () => IterableIterator<string>;
  getModuleInfo: GetModuleInfo;
}
type GetManualChunk = (id: string, meta: ManualChunkMeta) => string | NullValue;
type ExternalOption = (string | RegExp)[] | string | RegExp | ((source: string, importer: string | undefined, isResolved: boolean) => boolean | NullValue);
type GlobalsOption = Record<string, string> | ((name: string) => string);
type InputOption = string | string[] | Record<string, string>;
type ManualChunksOption = Record<string, string[]> | GetManualChunk;
type LogHandlerWithDefault = (level: LogLevel$2, log: RollupLog, defaultHandler: LogOrStringHandler) => void;
type LogOrStringHandler = (level: LogLevel$2 | 'error', log: RollupLog | string) => void;
type LogHandler = (level: LogLevel$2, log: RollupLog) => void;
type ModuleSideEffectsOption = boolean | 'no-external' | string[] | HasModuleSideEffects;
type PreserveEntrySignaturesOption = false | 'strict' | 'allow-extension' | 'exports-only';
type SourcemapPathTransformOption = (relativeSourcePath: string, sourcemapPath: string) => string;
type SourcemapIgnoreListOption = (relativeSourcePath: string, sourcemapPath: string) => boolean;
type InputPluginOption = MaybePromise<Plugin$3 | NullValue | false | InputPluginOption[]>;
interface InputOptions {
  cache?: boolean | RollupCache | undefined;
  context?: string | undefined;
  experimentalCacheExpiry?: number | undefined;
  experimentalLogSideEffects?: boolean | undefined;
  external?: ExternalOption | undefined;
  fs?: RollupFsModule | undefined;
  input?: InputOption | undefined;
  jsx?: false | JsxPreset | JsxOptions | undefined;
  logLevel?: LogLevelOption | undefined;
  makeAbsoluteExternalsRelative?: boolean | 'ifRelativeSource' | undefined;
  maxParallelFileOps?: number | undefined;
  moduleContext?: ((id: string) => string | NullValue) | Record<string, string> | undefined;
  onLog?: LogHandlerWithDefault | undefined;
  onwarn?: WarningHandlerWithDefault | undefined;
  perf?: boolean | undefined;
  plugins?: InputPluginOption | undefined;
  preserveEntrySignatures?: PreserveEntrySignaturesOption | undefined;
  preserveSymlinks?: boolean | undefined;
  shimMissingExports?: boolean | undefined;
  strictDeprecations?: boolean | undefined;
  treeshake?: boolean | TreeshakingPreset | TreeshakingOptions | undefined;
  watch?: WatcherOptions | false | undefined;
}
interface NormalizedInputOptions {
  cache: false | undefined | RollupCache;
  context: string;
  experimentalCacheExpiry: number;
  experimentalLogSideEffects: boolean;
  external: IsExternal;
  fs: RollupFsModule;
  input: string[] | Record<string, string>;
  jsx: false | NormalizedJsxOptions;
  logLevel: LogLevelOption;
  makeAbsoluteExternalsRelative: boolean | 'ifRelativeSource';
  maxParallelFileOps: number;
  moduleContext: (id: string) => string;
  onLog: LogHandler;
  perf: boolean;
  plugins: Plugin$3[];
  preserveEntrySignatures: PreserveEntrySignaturesOption;
  preserveSymlinks: boolean;
  shimMissingExports: boolean;
  strictDeprecations: boolean;
  treeshake: false | NormalizedTreeshakingOptions;
}
type InternalModuleFormat = 'amd' | 'cjs' | 'es' | 'iife' | 'system' | 'umd';
type ImportAttributesKey = 'with' | 'assert';
type ModuleFormat = InternalModuleFormat | 'commonjs' | 'esm' | 'module' | 'systemjs';
type GeneratedCodePreset = 'es5' | 'es2015';
interface NormalizedGeneratedCodeOptions {
  arrowFunctions: boolean;
  constBindings: boolean;
  objectShorthand: boolean;
  reservedNamesAsProps: boolean;
  symbols: boolean;
}
interface GeneratedCodeOptions extends Partial<NormalizedGeneratedCodeOptions> {
  preset?: GeneratedCodePreset | undefined;
}
type OptionsPaths = Record<string, string> | ((id: string) => string);
type InteropType = 'compat' | 'auto' | 'esModule' | 'default' | 'defaultOnly';
type GetInterop = (id: string | null) => InteropType;
type AmdOptions = ({
  autoId?: false | undefined;
  id: string;
} | {
  autoId: true;
  basePath?: string | undefined;
  id?: undefined | undefined;
} | {
  autoId?: false | undefined;
  id?: undefined | undefined;
}) & {
  define?: string | undefined;
  forceJsExtensionForImports?: boolean | undefined;
};
type NormalizedAmdOptions = ({
  autoId: false;
  id?: string | undefined;
} | {
  autoId: true;
  basePath: string;
}) & {
  define: string;
  forceJsExtensionForImports: boolean;
};
type AddonFunction = (chunk: RenderedChunk) => string | Promise<string>;
type OutputPluginOption = MaybePromise<OutputPlugin | NullValue | false | OutputPluginOption[]>;
type HashCharacters = 'base64' | 'base36' | 'hex';
interface OutputOptions {
  amd?: AmdOptions | undefined;
  assetFileNames?: string | ((chunkInfo: PreRenderedAsset) => string) | undefined;
  banner?: string | AddonFunction | undefined;
  chunkFileNames?: string | ((chunkInfo: PreRenderedChunk) => string) | undefined;
  compact?: boolean | undefined; // only required for bundle.write
  dir?: string | undefined;
  dynamicImportInCjs?: boolean | undefined;
  entryFileNames?: string | ((chunkInfo: PreRenderedChunk) => string) | undefined;
  esModule?: boolean | 'if-default-prop' | undefined;
  experimentalMinChunkSize?: number | undefined;
  exports?: 'default' | 'named' | 'none' | 'auto' | undefined;
  extend?: boolean | undefined;
  /** @deprecated Use "externalImportAttributes" instead. */
  externalImportAssertions?: boolean | undefined;
  externalImportAttributes?: boolean | undefined;
  externalLiveBindings?: boolean | undefined; // only required for bundle.write
  file?: string | undefined;
  footer?: string | AddonFunction | undefined;
  format?: ModuleFormat | undefined;
  freeze?: boolean | undefined;
  generatedCode?: GeneratedCodePreset | GeneratedCodeOptions | undefined;
  globals?: GlobalsOption | undefined;
  hashCharacters?: HashCharacters | undefined;
  hoistTransitiveImports?: boolean | undefined;
  importAttributesKey?: ImportAttributesKey | undefined;
  indent?: string | boolean | undefined;
  inlineDynamicImports?: boolean | undefined;
  interop?: InteropType | GetInterop | undefined;
  intro?: string | AddonFunction | undefined;
  manualChunks?: ManualChunksOption | undefined;
  minifyInternalExports?: boolean | undefined;
  name?: string | undefined;
  noConflict?: boolean | undefined;
  outro?: string | AddonFunction | undefined;
  paths?: OptionsPaths | undefined;
  plugins?: OutputPluginOption | undefined;
  preserveModules?: boolean | undefined;
  preserveModulesRoot?: string | undefined;
  reexportProtoFromExternal?: boolean | undefined;
  sanitizeFileName?: boolean | ((fileName: string) => string) | undefined;
  sourcemap?: boolean | 'inline' | 'hidden' | undefined;
  sourcemapBaseUrl?: string | undefined;
  sourcemapExcludeSources?: boolean | undefined;
  sourcemapFile?: string | undefined;
  sourcemapFileNames?: string | ((chunkInfo: PreRenderedChunk) => string) | undefined;
  sourcemapIgnoreList?: boolean | SourcemapIgnoreListOption | undefined;
  sourcemapPathTransform?: SourcemapPathTransformOption | undefined;
  sourcemapDebugIds?: boolean | undefined;
  strict?: boolean | undefined;
  systemNullSetters?: boolean | undefined;
  validate?: boolean | undefined;
  virtualDirname?: string | undefined;
}
interface NormalizedOutputOptions {
  amd: NormalizedAmdOptions;
  assetFileNames: string | ((chunkInfo: PreRenderedAsset) => string);
  banner: AddonFunction;
  chunkFileNames: string | ((chunkInfo: PreRenderedChunk) => string);
  compact: boolean;
  dir: string | undefined;
  dynamicImportInCjs: boolean;
  entryFileNames: string | ((chunkInfo: PreRenderedChunk) => string);
  esModule: boolean | 'if-default-prop';
  experimentalMinChunkSize: number;
  exports: 'default' | 'named' | 'none' | 'auto';
  extend: boolean;
  /** @deprecated Use "externalImportAttributes" instead. */
  externalImportAssertions: boolean;
  externalImportAttributes: boolean;
  externalLiveBindings: boolean;
  file: string | undefined;
  footer: AddonFunction;
  format: InternalModuleFormat;
  freeze: boolean;
  generatedCode: NormalizedGeneratedCodeOptions;
  globals: GlobalsOption;
  hashCharacters: HashCharacters;
  hoistTransitiveImports: boolean;
  importAttributesKey: ImportAttributesKey;
  indent: true | string;
  inlineDynamicImports: boolean;
  interop: GetInterop;
  intro: AddonFunction;
  manualChunks: ManualChunksOption;
  minifyInternalExports: boolean;
  name: string | undefined;
  noConflict: boolean;
  outro: AddonFunction;
  paths: OptionsPaths;
  plugins: OutputPlugin[];
  preserveModules: boolean;
  preserveModulesRoot: string | undefined;
  reexportProtoFromExternal: boolean;
  sanitizeFileName: (fileName: string) => string;
  sourcemap: boolean | 'inline' | 'hidden';
  sourcemapBaseUrl: string | undefined;
  sourcemapExcludeSources: boolean;
  sourcemapFile: string | undefined;
  sourcemapFileNames: string | ((chunkInfo: PreRenderedChunk) => string) | undefined;
  sourcemapIgnoreList: SourcemapIgnoreListOption;
  sourcemapPathTransform: SourcemapPathTransformOption | undefined;
  sourcemapDebugIds: boolean;
  strict: boolean;
  systemNullSetters: boolean;
  validate: boolean;
  virtualDirname: string;
}
type WarningHandlerWithDefault = (warning: RollupLog, defaultHandler: LoggingFunction) => void;
type SerializedTimings = Record<string, [number, number, number]>;
interface PreRenderedAsset {
  /** @deprecated Use "names" instead. */
  name: string | undefined;
  names: string[];
  /** @deprecated Use "originalFileNames" instead. */
  originalFileName: string | null;
  originalFileNames: string[];
  source: string | Uint8Array;
  type: 'asset';
}
interface OutputAsset extends PreRenderedAsset {
  fileName: string;
  needsCodeReference: boolean;
}
interface RenderedModule {
  readonly code: string | null;
  originalLength: number;
  removedExports: string[];
  renderedExports: string[];
  renderedLength: number;
}
interface PreRenderedChunk {
  exports: string[];
  facadeModuleId: string | null;
  isDynamicEntry: boolean;
  isEntry: boolean;
  isImplicitEntry: boolean;
  moduleIds: string[];
  name: string;
  type: 'chunk';
}
interface RenderedChunk extends PreRenderedChunk {
  dynamicImports: string[];
  fileName: string;
  implicitlyLoadedBefore: string[];
  importedBindings: Record<string, string[]>;
  imports: string[];
  modules: Record<string, RenderedModule>;
  referencedFiles: string[];
}
interface OutputChunk extends RenderedChunk {
  code: string;
  map: SourceMap$2 | null;
  sourcemapFileName: string | null;
  preliminaryFileName: string;
}
type SerializablePluginCache = Record<string, [number, any]>;
interface RollupCache {
  modules: ModuleJSON[];
  plugins?: Record<string, SerializablePluginCache>;
}
interface RollupOutput {
  output: [OutputChunk, ...(OutputChunk | OutputAsset)[]];
}
interface RollupBuild {
  cache: RollupCache | undefined;
  close: () => Promise<void>;
  closed: boolean;
  [Symbol.asyncDispose](): Promise<void>;
  generate: (outputOptions: OutputOptions) => Promise<RollupOutput>;
  getTimings?: (() => SerializedTimings) | undefined;
  watchFiles: string[];
  write: (options: OutputOptions) => Promise<RollupOutput>;
}
interface RollupOptions extends InputOptions {
  // This is included for compatibility with config files but ignored by rollup.rollup
  output?: OutputOptions | OutputOptions[] | undefined;
}
interface ChokidarOptions {
  alwaysStat?: boolean | undefined;
  atomic?: boolean | number | undefined;
  awaitWriteFinish?: {
    pollInterval?: number | undefined;
    stabilityThreshold?: number | undefined;
  } | boolean | undefined;
  binaryInterval?: number | undefined;
  cwd?: string | undefined;
  depth?: number | undefined;
  disableGlobbing?: boolean | undefined;
  followSymlinks?: boolean | undefined;
  ignoreInitial?: boolean | undefined;
  ignorePermissionErrors?: boolean | undefined;
  ignored?: any | undefined;
  interval?: number | undefined;
  persistent?: boolean | undefined;
  useFsEvents?: boolean | undefined;
  usePolling?: boolean | undefined;
}
interface WatcherOptions {
  allowInputInsideOutputPath?: boolean | undefined;
  buildDelay?: number | undefined;
  chokidar?: ChokidarOptions | undefined;
  clearScreen?: boolean | undefined;
  exclude?: string | RegExp | (string | RegExp)[] | undefined;
  include?: string | RegExp | (string | RegExp)[] | undefined;
  skipWrite?: boolean | undefined;
  onInvalidate?: ((id: string) => void) | undefined;
}
type AwaitedEventListener<T extends Record<string, (...parameters: any) => any>, K extends keyof T> = (...parameters: Parameters<T[K]>) => void | Promise<void>;
interface AwaitingEventEmitter<T extends Record<string, (...parameters: any) => any>> {
  close(): Promise<void>;
  emit<K extends keyof T>(event: K, ...parameters: Parameters<T[K]>): Promise<unknown>;
  /**
   * Removes an event listener.
   */
  off<K extends keyof T>(event: K, listener: AwaitedEventListener<T, K>): this;
  /**
   * Registers an event listener that will be awaited before Rollup continues.
   * All listeners will be awaited in parallel while rejections are tracked via
   * Promise.all.
   */
  on<K extends keyof T>(event: K, listener: AwaitedEventListener<T, K>): this;
  /**
   * Registers an event listener that will be awaited before Rollup continues.
   * All listeners will be awaited in parallel while rejections are tracked via
   * Promise.all.
   * Listeners are removed automatically when removeListenersForCurrentRun is
   * called, which happens automatically after each run.
   */
  onCurrentRun<K extends keyof T>(event: K, listener: (...parameters: Parameters<T[K]>) => Promise<ReturnType<T[K]>>): this;
  removeAllListeners(): this;
  removeListenersForCurrentRun(): this;
}
type RollupWatcherEvent = {
  code: 'START';
} | {
  code: 'BUNDLE_START';
  input?: InputOption | undefined;
  output: readonly string[];
} | {
  code: 'BUNDLE_END';
  duration: number;
  input?: InputOption | undefined;
  output: readonly string[];
  result: RollupBuild;
} | {
  code: 'END';
} | {
  code: 'ERROR';
  error: RollupError;
  result: RollupBuild | null;
};
type RollupWatcher = AwaitingEventEmitter<{
  change: (id: string, change: {
    event: ChangeEvent;
  }) => void;
  close: () => void;
  event: (event: RollupWatcherEvent) => void;
  restart: () => void;
}>;
interface AstNodeLocation {
  end: number;
  start: number;
}
type OmittedEstreeKeys = 'loc' | 'range' | 'leadingComments' | 'trailingComments' | 'innerComments' | 'comments';
type RollupAstNode<T> = Omit<T, OmittedEstreeKeys> & AstNodeLocation;
type ProgramNode = RollupAstNode<Program>;
type AstNode = RollupAstNode<Node$1>;
interface RollupFsModule {
  appendFile(path: string, data: string | Uint8Array, options?: {
    encoding?: BufferEncoding$1 | null;
    mode?: string | number;
    flag?: string | number;
  }): Promise<void>;
  copyFile(source: string, destination: string, mode?: string | number): Promise<void>;
  mkdir(path: string, options?: {
    recursive?: boolean;
    mode?: string | number;
  }): Promise<void>;
  mkdtemp(prefix: string): Promise<string>;
  readdir(path: string, options?: {
    withFileTypes?: false;
  }): Promise<string[]>;
  readdir(path: string, options?: {
    withFileTypes: true;
  }): Promise<RollupDirectoryEntry[]>;
  readFile(path: string, options?: {
    encoding?: null;
    flag?: string | number;
    signal?: AbortSignal;
  }): Promise<Uint8Array>;
  readFile(path: string, options?: {
    encoding: BufferEncoding$1;
    flag?: string | number;
    signal?: AbortSignal;
  }): Promise<string>;
  realpath(path: string): Promise<string>;
  rename(oldPath: string, newPath: string): Promise<void>;
  rmdir(path: string, options?: {
    recursive?: boolean;
  }): Promise<void>;
  stat(path: string): Promise<RollupFileStats>;
  lstat(path: string): Promise<RollupFileStats>;
  unlink(path: string): Promise<void>;
  writeFile(path: string, data: string | Uint8Array, options?: {
    encoding?: BufferEncoding$1 | null;
    mode?: string | number;
    flag?: string | number;
  }): Promise<void>;
}
type BufferEncoding$1 = 'ascii' | 'utf8' | 'utf16le' | 'ucs2' | 'base64' | 'base64url' | 'latin1' | 'binary' | 'hex';
interface RollupDirectoryEntry {
  isFile(): boolean;
  isDirectory(): boolean;
  isSymbolicLink(): boolean;
  name: string;
}
interface RollupFileStats {
  isFile(): boolean;
  isDirectory(): boolean;
  isSymbolicLink(): boolean;
  size: number;
  mtime: Date;
  ctime: Date;
  atime: Date;
  birthtime: Date;
}
//#endregion
//#region ../../node_modules/.pnpm/esbuild@0.25.9/node_modules/esbuild/lib/main.d.ts
type Platform = 'browser' | 'node' | 'neutral';
type Format = 'iife' | 'cjs' | 'esm';
type Loader = 'base64' | 'binary' | 'copy' | 'css' | 'dataurl' | 'default' | 'empty' | 'file' | 'js' | 'json' | 'jsx' | 'local-css' | 'text' | 'ts' | 'tsx';
type LogLevel$1 = 'verbose' | 'debug' | 'info' | 'warning' | 'error' | 'silent';
type Charset = 'ascii' | 'utf8';
type Drop = 'console' | 'debugger';
type AbsPaths = 'code' | 'log' | 'metafile';
interface CommonOptions {
  /** Documentation: https://esbuild.github.io/api/#sourcemap */
  sourcemap?: boolean | 'linked' | 'inline' | 'external' | 'both';
  /** Documentation: https://esbuild.github.io/api/#legal-comments */
  legalComments?: 'none' | 'inline' | 'eof' | 'linked' | 'external';
  /** Documentation: https://esbuild.github.io/api/#source-root */
  sourceRoot?: string;
  /** Documentation: https://esbuild.github.io/api/#sources-content */
  sourcesContent?: boolean;
  /** Documentation: https://esbuild.github.io/api/#format */
  format?: Format;
  /** Documentation: https://esbuild.github.io/api/#global-name */
  globalName?: string;
  /** Documentation: https://esbuild.github.io/api/#target */
  target?: string | string[];
  /** Documentation: https://esbuild.github.io/api/#supported */
  supported?: Record<string, boolean>;
  /** Documentation: https://esbuild.github.io/api/#platform */
  platform?: Platform;
  /** Documentation: https://esbuild.github.io/api/#mangle-props */
  mangleProps?: RegExp;
  /** Documentation: https://esbuild.github.io/api/#mangle-props */
  reserveProps?: RegExp;
  /** Documentation: https://esbuild.github.io/api/#mangle-props */
  mangleQuoted?: boolean;
  /** Documentation: https://esbuild.github.io/api/#mangle-props */
  mangleCache?: Record<string, string | false>;
  /** Documentation: https://esbuild.github.io/api/#drop */
  drop?: Drop[];
  /** Documentation: https://esbuild.github.io/api/#drop-labels */
  dropLabels?: string[];
  /** Documentation: https://esbuild.github.io/api/#minify */
  minify?: boolean;
  /** Documentation: https://esbuild.github.io/api/#minify */
  minifyWhitespace?: boolean;
  /** Documentation: https://esbuild.github.io/api/#minify */
  minifyIdentifiers?: boolean;
  /** Documentation: https://esbuild.github.io/api/#minify */
  minifySyntax?: boolean;
  /** Documentation: https://esbuild.github.io/api/#line-limit */
  lineLimit?: number;
  /** Documentation: https://esbuild.github.io/api/#charset */
  charset?: Charset;
  /** Documentation: https://esbuild.github.io/api/#tree-shaking */
  treeShaking?: boolean;
  /** Documentation: https://esbuild.github.io/api/#ignore-annotations */
  ignoreAnnotations?: boolean;
  /** Documentation: https://esbuild.github.io/api/#jsx */
  jsx?: 'transform' | 'preserve' | 'automatic';
  /** Documentation: https://esbuild.github.io/api/#jsx-factory */
  jsxFactory?: string;
  /** Documentation: https://esbuild.github.io/api/#jsx-fragment */
  jsxFragment?: string;
  /** Documentation: https://esbuild.github.io/api/#jsx-import-source */
  jsxImportSource?: string;
  /** Documentation: https://esbuild.github.io/api/#jsx-development */
  jsxDev?: boolean;
  /** Documentation: https://esbuild.github.io/api/#jsx-side-effects */
  jsxSideEffects?: boolean;
  /** Documentation: https://esbuild.github.io/api/#define */
  define?: {
    [key: string]: string;
  };
  /** Documentation: https://esbuild.github.io/api/#pure */
  pure?: string[];
  /** Documentation: https://esbuild.github.io/api/#keep-names */
  keepNames?: boolean;
  /** Documentation: https://esbuild.github.io/api/#abs-paths */
  absPaths?: AbsPaths[];
  /** Documentation: https://esbuild.github.io/api/#color */
  color?: boolean;
  /** Documentation: https://esbuild.github.io/api/#log-level */
  logLevel?: LogLevel$1;
  /** Documentation: https://esbuild.github.io/api/#log-limit */
  logLimit?: number;
  /** Documentation: https://esbuild.github.io/api/#log-override */
  logOverride?: Record<string, LogLevel$1>;
  /** Documentation: https://esbuild.github.io/api/#tsconfig-raw */
  tsconfigRaw?: string | TsconfigRaw;
}
interface TsconfigRaw {
  compilerOptions?: {
    alwaysStrict?: boolean;
    baseUrl?: string;
    experimentalDecorators?: boolean;
    importsNotUsedAsValues?: 'remove' | 'preserve' | 'error';
    jsx?: 'preserve' | 'react-native' | 'react' | 'react-jsx' | 'react-jsxdev';
    jsxFactory?: string;
    jsxFragmentFactory?: string;
    jsxImportSource?: string;
    paths?: Record<string, string[]>;
    preserveValueImports?: boolean;
    strict?: boolean;
    target?: string;
    useDefineForClassFields?: boolean;
    verbatimModuleSyntax?: boolean;
  };
}
interface BuildOptions$1 extends CommonOptions {
  /** Documentation: https://esbuild.github.io/api/#bundle */
  bundle?: boolean;
  /** Documentation: https://esbuild.github.io/api/#splitting */
  splitting?: boolean;
  /** Documentation: https://esbuild.github.io/api/#preserve-symlinks */
  preserveSymlinks?: boolean;
  /** Documentation: https://esbuild.github.io/api/#outfile */
  outfile?: string;
  /** Documentation: https://esbuild.github.io/api/#metafile */
  metafile?: boolean;
  /** Documentation: https://esbuild.github.io/api/#outdir */
  outdir?: string;
  /** Documentation: https://esbuild.github.io/api/#outbase */
  outbase?: string;
  /** Documentation: https://esbuild.github.io/api/#external */
  external?: string[];
  /** Documentation: https://esbuild.github.io/api/#packages */
  packages?: 'bundle' | 'external';
  /** Documentation: https://esbuild.github.io/api/#alias */
  alias?: Record<string, string>;
  /** Documentation: https://esbuild.github.io/api/#loader */
  loader?: {
    [ext: string]: Loader;
  };
  /** Documentation: https://esbuild.github.io/api/#resolve-extensions */
  resolveExtensions?: string[];
  /** Documentation: https://esbuild.github.io/api/#main-fields */
  mainFields?: string[];
  /** Documentation: https://esbuild.github.io/api/#conditions */
  conditions?: string[];
  /** Documentation: https://esbuild.github.io/api/#write */
  write?: boolean;
  /** Documentation: https://esbuild.github.io/api/#allow-overwrite */
  allowOverwrite?: boolean;
  /** Documentation: https://esbuild.github.io/api/#tsconfig */
  tsconfig?: string;
  /** Documentation: https://esbuild.github.io/api/#out-extension */
  outExtension?: {
    [ext: string]: string;
  };
  /** Documentation: https://esbuild.github.io/api/#public-path */
  publicPath?: string;
  /** Documentation: https://esbuild.github.io/api/#entry-names */
  entryNames?: string;
  /** Documentation: https://esbuild.github.io/api/#chunk-names */
  chunkNames?: string;
  /** Documentation: https://esbuild.github.io/api/#asset-names */
  assetNames?: string;
  /** Documentation: https://esbuild.github.io/api/#inject */
  inject?: string[];
  /** Documentation: https://esbuild.github.io/api/#banner */
  banner?: {
    [type: string]: string;
  };
  /** Documentation: https://esbuild.github.io/api/#footer */
  footer?: {
    [type: string]: string;
  };
  /** Documentation: https://esbuild.github.io/api/#entry-points */
  entryPoints?: (string | {
    in: string;
    out: string;
  })[] | Record<string, string>;
  /** Documentation: https://esbuild.github.io/api/#stdin */
  stdin?: StdinOptions;
  /** Documentation: https://esbuild.github.io/plugins/ */
  plugins?: Plugin$2[];
  /** Documentation: https://esbuild.github.io/api/#working-directory */
  absWorkingDir?: string;
  /** Documentation: https://esbuild.github.io/api/#node-paths */
  nodePaths?: string[]; // The "NODE_PATH" variable from Node.js
}
interface StdinOptions {
  contents: string | Uint8Array;
  resolveDir?: string;
  sourcefile?: string;
  loader?: Loader;
}
interface Message$1 {
  id: string;
  pluginName: string;
  text: string;
  location: Location | null;
  notes: Note[];
  /**
   * Optional user-specified data that is passed through unmodified. You can
   * use this to stash the original error, for example.
   */
  detail: any;
}
interface Note {
  text: string;
  location: Location | null;
}
interface Location {
  file: string;
  namespace: string;
  /** 1-based */
  line: number;
  /** 0-based, in bytes */
  column: number;
  /** in bytes */
  length: number;
  lineText: string;
  suggestion: string;
}
interface OutputFile {
  path: string;
  contents: Uint8Array;
  hash: string;
  /** "contents" as text (changes automatically with "contents") */
  readonly text: string;
}
interface BuildResult<ProvidedOptions extends BuildOptions$1 = BuildOptions$1> {
  errors: Message$1[];
  warnings: Message$1[];
  /** Only when "write: false" */
  outputFiles: OutputFile[] | (ProvidedOptions['write'] extends false ? never : undefined);
  /** Only when "metafile: true" */
  metafile: Metafile | (ProvidedOptions['metafile'] extends true ? never : undefined);
  /** Only when "mangleCache" is present */
  mangleCache: Record<string, string | false> | (ProvidedOptions['mangleCache'] extends Object ? never : undefined);
}
/** Documentation: https://esbuild.github.io/api/#serve-arguments */
interface ServeOptions {
  port?: number;
  host?: string;
  servedir?: string;
  keyfile?: string;
  certfile?: string;
  fallback?: string;
  cors?: CORSOptions;
  onRequest?: (args: ServeOnRequestArgs) => void;
}
/** Documentation: https://esbuild.github.io/api/#cors */
interface CORSOptions {
  origin?: string | string[];
}
interface ServeOnRequestArgs {
  remoteAddress: string;
  method: string;
  path: string;
  status: number;
  /** The time to generate the response, not to send it */
  timeInMS: number;
}
/** Documentation: https://esbuild.github.io/api/#serve-return-values */
interface ServeResult {
  port: number;
  hosts: string[];
}
interface TransformOptions$1 extends CommonOptions {
  /** Documentation: https://esbuild.github.io/api/#sourcefile */
  sourcefile?: string;
  /** Documentation: https://esbuild.github.io/api/#loader */
  loader?: Loader;
  /** Documentation: https://esbuild.github.io/api/#banner */
  banner?: string;
  /** Documentation: https://esbuild.github.io/api/#footer */
  footer?: string;
}
interface TransformResult$1<ProvidedOptions extends TransformOptions$1 = TransformOptions$1> {
  code: string;
  map: string;
  warnings: Message$1[];
  /** Only when "mangleCache" is present */
  mangleCache: Record<string, string | false> | (ProvidedOptions['mangleCache'] extends Object ? never : undefined);
  /** Only when "legalComments" is "external" */
  legalComments: string | (ProvidedOptions['legalComments'] extends 'external' ? never : undefined);
}
interface Plugin$2 {
  name: string;
  setup: (build: PluginBuild) => (void | Promise<void>);
}
interface PluginBuild {
  /** Documentation: https://esbuild.github.io/plugins/#build-options */
  initialOptions: BuildOptions$1;
  /** Documentation: https://esbuild.github.io/plugins/#resolve */
  resolve(path: string, options?: ResolveOptions$1): Promise<ResolveResult>;
  /** Documentation: https://esbuild.github.io/plugins/#on-start */
  onStart(callback: () => (OnStartResult | null | void | Promise<OnStartResult | null | void>)): void;
  /** Documentation: https://esbuild.github.io/plugins/#on-end */
  onEnd(callback: (result: BuildResult) => (OnEndResult | null | void | Promise<OnEndResult | null | void>)): void;
  /** Documentation: https://esbuild.github.io/plugins/#on-resolve */
  onResolve(options: OnResolveOptions, callback: (args: OnResolveArgs) => (OnResolveResult | null | undefined | Promise<OnResolveResult | null | undefined>)): void;
  /** Documentation: https://esbuild.github.io/plugins/#on-load */
  onLoad(options: OnLoadOptions, callback: (args: OnLoadArgs) => (OnLoadResult | null | undefined | Promise<OnLoadResult | null | undefined>)): void;
  /** Documentation: https://esbuild.github.io/plugins/#on-dispose */
  onDispose(callback: () => void): void; // This is a full copy of the esbuild library in case you need it
  esbuild: {
    context: typeof context;
    build: typeof build;
    buildSync: typeof buildSync;
    transform: typeof transform;
    transformSync: typeof transformSync;
    formatMessages: typeof formatMessages;
    formatMessagesSync: typeof formatMessagesSync;
    analyzeMetafile: typeof analyzeMetafile;
    analyzeMetafileSync: typeof analyzeMetafileSync;
    initialize: typeof initialize;
    version: typeof version;
  };
}
/** Documentation: https://esbuild.github.io/plugins/#resolve-options */
interface ResolveOptions$1 {
  pluginName?: string;
  importer?: string;
  namespace?: string;
  resolveDir?: string;
  kind?: ImportKind;
  pluginData?: any;
  with?: Record<string, string>;
}
/** Documentation: https://esbuild.github.io/plugins/#resolve-results */
interface ResolveResult {
  errors: Message$1[];
  warnings: Message$1[];
  path: string;
  external: boolean;
  sideEffects: boolean;
  namespace: string;
  suffix: string;
  pluginData: any;
}
interface OnStartResult {
  errors?: PartialMessage[];
  warnings?: PartialMessage[];
}
interface OnEndResult {
  errors?: PartialMessage[];
  warnings?: PartialMessage[];
}
/** Documentation: https://esbuild.github.io/plugins/#on-resolve-options */
interface OnResolveOptions {
  filter: RegExp;
  namespace?: string;
}
/** Documentation: https://esbuild.github.io/plugins/#on-resolve-arguments */
interface OnResolveArgs {
  path: string;
  importer: string;
  namespace: string;
  resolveDir: string;
  kind: ImportKind;
  pluginData: any;
  with: Record<string, string>;
}
type ImportKind = 'entry-point' // JS
| 'import-statement' | 'require-call' | 'dynamic-import' | 'require-resolve' // CSS
| 'import-rule' | 'composes-from' | 'url-token';
/** Documentation: https://esbuild.github.io/plugins/#on-resolve-results */
interface OnResolveResult {
  pluginName?: string;
  errors?: PartialMessage[];
  warnings?: PartialMessage[];
  path?: string;
  external?: boolean;
  sideEffects?: boolean;
  namespace?: string;
  suffix?: string;
  pluginData?: any;
  watchFiles?: string[];
  watchDirs?: string[];
}
/** Documentation: https://esbuild.github.io/plugins/#on-load-options */
interface OnLoadOptions {
  filter: RegExp;
  namespace?: string;
}
/** Documentation: https://esbuild.github.io/plugins/#on-load-arguments */
interface OnLoadArgs {
  path: string;
  namespace: string;
  suffix: string;
  pluginData: any;
  with: Record<string, string>;
}
/** Documentation: https://esbuild.github.io/plugins/#on-load-results */
interface OnLoadResult {
  pluginName?: string;
  errors?: PartialMessage[];
  warnings?: PartialMessage[];
  contents?: string | Uint8Array;
  resolveDir?: string;
  loader?: Loader;
  pluginData?: any;
  watchFiles?: string[];
  watchDirs?: string[];
}
interface PartialMessage {
  id?: string;
  pluginName?: string;
  text?: string;
  location?: Partial<Location> | null;
  notes?: PartialNote[];
  detail?: any;
}
interface PartialNote {
  text?: string;
  location?: Partial<Location> | null;
}
/** Documentation: https://esbuild.github.io/api/#metafile */
interface Metafile {
  inputs: {
    [path: string]: {
      bytes: number;
      imports: {
        path: string;
        kind: ImportKind;
        external?: boolean;
        original?: string;
        with?: Record<string, string>;
      }[];
      format?: 'cjs' | 'esm';
      with?: Record<string, string>;
    };
  };
  outputs: {
    [path: string]: {
      bytes: number;
      inputs: {
        [path: string]: {
          bytesInOutput: number;
        };
      };
      imports: {
        path: string;
        kind: ImportKind | 'file-loader';
        external?: boolean;
      }[];
      exports: string[];
      entryPoint?: string;
      cssBundle?: string;
    };
  };
}
interface FormatMessagesOptions {
  kind: 'error' | 'warning';
  color?: boolean;
  terminalWidth?: number;
}
interface AnalyzeMetafileOptions {
  color?: boolean;
  verbose?: boolean;
}
/** Documentation: https://esbuild.github.io/api/#watch-arguments */
interface WatchOptions$1 {
  delay?: number; // In milliseconds
}
interface BuildContext<ProvidedOptions extends BuildOptions$1 = BuildOptions$1> {
  /** Documentation: https://esbuild.github.io/api/#rebuild */
  rebuild(): Promise<BuildResult<ProvidedOptions>>;
  /** Documentation: https://esbuild.github.io/api/#watch */
  watch(options?: WatchOptions$1): Promise<void>;
  /** Documentation: https://esbuild.github.io/api/#serve */
  serve(options?: ServeOptions): Promise<ServeResult>;
  cancel(): Promise<void>;
  dispose(): Promise<void>;
}
// This is a TypeScript type-level function which replaces any keys in "In"
// that aren't in "Out" with "never". We use this to reject properties with
// typos in object literals. See: https://stackoverflow.com/questions/49580725
type SameShape<Out, In extends Out> = In & { [Key in Exclude<keyof In, keyof Out>]: never };
/**
 * This function invokes the "esbuild" command-line tool for you. It returns a
 * promise that either resolves with a "BuildResult" object or rejects with a
 * "BuildFailure" object.
 *
 * - Works in node: yes
 * - Works in browser: yes
 *
 * Documentation: https://esbuild.github.io/api/#build
 */
declare function build<T extends BuildOptions$1>(options: SameShape<BuildOptions$1, T>): Promise<BuildResult<T>>;
/**
 * This is the advanced long-running form of "build" that supports additional
 * features such as watch mode and a local development server.
 *
 * - Works in node: yes
 * - Works in browser: no
 *
 * Documentation: https://esbuild.github.io/api/#build
 */
declare function context<T extends BuildOptions$1>(options: SameShape<BuildOptions$1, T>): Promise<BuildContext<T>>;
/**
 * This function transforms a single JavaScript file. It can be used to minify
 * JavaScript, convert TypeScript/JSX to JavaScript, or convert newer JavaScript
 * to older JavaScript. It returns a promise that is either resolved with a
 * "TransformResult" object or rejected with a "TransformFailure" object.
 *
 * - Works in node: yes
 * - Works in browser: yes
 *
 * Documentation: https://esbuild.github.io/api/#transform
 */
declare function transform<T extends TransformOptions$1>(input: string | Uint8Array, options?: SameShape<TransformOptions$1, T>): Promise<TransformResult$1<T>>;
/**
 * Converts log messages to formatted message strings suitable for printing in
 * the terminal. This allows you to reuse the built-in behavior of esbuild's
 * log message formatter. This is a batch-oriented API for efficiency.
 *
 * - Works in node: yes
 * - Works in browser: yes
 */
declare function formatMessages(messages: PartialMessage[], options: FormatMessagesOptions): Promise<string[]>;
/**
 * Pretty-prints an analysis of the metafile JSON to a string. This is just for
 * convenience to be able to match esbuild's pretty-printing exactly. If you want
 * to customize it, you can just inspect the data in the metafile yourself.
 *
 * - Works in node: yes
 * - Works in browser: yes
 *
 * Documentation: https://esbuild.github.io/api/#analyze
 */
declare function analyzeMetafile(metafile: Metafile | string, options?: AnalyzeMetafileOptions): Promise<string>;
/**
 * A synchronous version of "build".
 *
 * - Works in node: yes
 * - Works in browser: no
 *
 * Documentation: https://esbuild.github.io/api/#build
 */
declare function buildSync<T extends BuildOptions$1>(options: SameShape<BuildOptions$1, T>): BuildResult<T>;
/**
 * A synchronous version of "transform".
 *
 * - Works in node: yes
 * - Works in browser: no
 *
 * Documentation: https://esbuild.github.io/api/#transform
 */
declare function transformSync<T extends TransformOptions$1>(input: string | Uint8Array, options?: SameShape<TransformOptions$1, T>): TransformResult$1<T>;
/**
 * A synchronous version of "formatMessages".
 *
 * - Works in node: yes
 * - Works in browser: no
 */
declare function formatMessagesSync(messages: PartialMessage[], options: FormatMessagesOptions): string[];
/**
 * A synchronous version of "analyzeMetafile".
 *
 * - Works in node: yes
 * - Works in browser: no
 *
 * Documentation: https://esbuild.github.io/api/#analyze
 */
declare function analyzeMetafileSync(metafile: Metafile | string, options?: AnalyzeMetafileOptions): string;
/**
 * This configures the browser-based version of esbuild. It is necessary to
 * call this first and wait for the returned promise to be resolved before
 * making other API calls when using esbuild in the browser.
 *
 * - Works in node: yes
 * - Works in browser: yes ("options" is required)
 *
 * Documentation: https://esbuild.github.io/api/#browser
 */
declare function initialize(options: InitializeOptions): Promise<void>;
interface InitializeOptions {
  /**
   * The URL of the "esbuild.wasm" file. This must be provided when running
   * esbuild in the browser.
   */
  wasmURL?: string | URL;
  /**
   * The result of calling "new WebAssembly.Module(buffer)" where "buffer"
   * is a typed array or ArrayBuffer containing the binary code of the
   * "esbuild.wasm" file.
   *
   * You can use this as an alternative to "wasmURL" for environments where it's
   * not possible to download the WebAssembly module.
   */
  wasmModule?: WebAssembly.Module;
  /**
   * By default esbuild runs the WebAssembly-based browser API in a web worker
   * to avoid blocking the UI thread. This can be disabled by setting "worker"
   * to false.
   */
  worker?: boolean;
}
declare let version: string;
// Note: These declarations exist to avoid type errors when you omit "dom" from
// "lib" in your "tsconfig.json" file. TypeScript confusingly declares the
// global "WebAssembly" type in "lib.dom.d.ts" even though it has nothing to do
// with the browser DOM and is present in many non-browser JavaScript runtimes
// (e.g. node and deno). Declaring it here allows esbuild's API to be used in
// these scenarios.
//
// There's an open issue about getting this problem corrected (although these
// declarations will need to remain even if this is fixed for backward
// compatibility with older TypeScript versions):
//
//   https://github.com/microsoft/TypeScript-DOM-lib-generator/issues/826
//
declare global {
  namespace WebAssembly {
    interface Module {}
  }
  interface URL {}
}
//#endregion
//#region ../../node_modules/.pnpm/@jridgewell+trace-mapping@0.3.31/node_modules/@jridgewell/trace-mapping/types/sourcemap-segment.d.mts
type GeneratedColumn = number;
type SourcesIndex = number;
type SourceLine = number;
type SourceColumn = number;
type NamesIndex = number;
type SourceMapSegment = [GeneratedColumn] | [GeneratedColumn, SourcesIndex, SourceLine, SourceColumn] | [GeneratedColumn, SourcesIndex, SourceLine, SourceColumn, NamesIndex];
//#endregion
//#region ../../node_modules/.pnpm/@jridgewell+trace-mapping@0.3.31/node_modules/@jridgewell/trace-mapping/types/types.d.mts
interface SourceMapV3 {
  file?: string | null;
  names: string[];
  sourceRoot?: string;
  sources: (string | null)[];
  sourcesContent?: (string | null)[];
  version: 3;
  ignoreList?: number[];
}
interface EncodedSourceMap extends SourceMapV3 {
  mappings: string;
}
interface DecodedSourceMap extends SourceMapV3 {
  mappings: SourceMapSegment[][];
}
interface Section {
  offset: {
    line: number;
    column: number;
  };
  map: EncodedSourceMap | DecodedSourceMap | SectionedSourceMap;
}
interface SectionedSourceMap {
  file?: string | null;
  sections: Section[];
  version: 3;
}
type XInput = {
  x_google_ignoreList?: SourceMapV3['ignoreList'];
};
type EncodedSourceMapXInput = EncodedSourceMap & XInput;
type DecodedSourceMapXInput = DecodedSourceMap & XInput;
type SectionedSourceMapXInput = Omit<SectionedSourceMap, 'sections'> & {
  sections: SectionXInput[];
};
type SectionXInput = Omit<Section, 'map'> & {
  map: SectionedSourceMapInput;
};
type SourceMapInput = string | EncodedSourceMapXInput | DecodedSourceMapXInput | TraceMap;
type SectionedSourceMapInput = SourceMapInput | SectionedSourceMapXInput;
declare abstract class SourceMap$1 {
  version: SourceMapV3['version'];
  file: SourceMapV3['file'];
  names: SourceMapV3['names'];
  sourceRoot: SourceMapV3['sourceRoot'];
  sources: SourceMapV3['sources'];
  sourcesContent: SourceMapV3['sourcesContent'];
  resolvedSources: SourceMapV3['sources'];
  ignoreList: SourceMapV3['ignoreList'];
}
type Ro<T> = T extends Array<infer V> ? V[] | Readonly<V[]> | RoArray<V> | Readonly<RoArray<V>> : T extends object ? T | Readonly<T> | RoObject<T> | Readonly<RoObject<T>> : T;
type RoArray<T> = Ro<T>[];
type RoObject<T> = { [K in keyof T]: T[K] | Ro<T[K]> };
//#endregion
//#region ../../node_modules/.pnpm/@jridgewell+trace-mapping@0.3.31/node_modules/@jridgewell/trace-mapping/types/trace-mapping.d.mts
declare class TraceMap implements SourceMap$1 {
  version: SourceMapV3['version'];
  file: SourceMapV3['file'];
  names: SourceMapV3['names'];
  sourceRoot: SourceMapV3['sourceRoot'];
  sources: SourceMapV3['sources'];
  sourcesContent: SourceMapV3['sourcesContent'];
  ignoreList: SourceMapV3['ignoreList'];
  resolvedSources: string[];
  private _encoded;
  private _decoded;
  private _decodedMemo;
  private _bySources;
  private _bySourceMemos;
  constructor(map: Ro<SourceMapInput>, mapUrl?: string | null);
}
//#endregion
//#region ../../node_modules/.pnpm/terser@5.44.0/node_modules/terser/tools/terser.d.ts
type ECMA = 5 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020;
type ConsoleProperty = keyof typeof console;
type DropConsoleOption = boolean | ConsoleProperty[];
interface ParseOptions {
  bare_returns?: boolean;
  /** @deprecated legacy option. Currently, all supported EcmaScript is valid to parse. */
  ecma?: ECMA;
  html5_comments?: boolean;
  shebang?: boolean;
}
interface CompressOptions {
  arguments?: boolean;
  arrows?: boolean;
  booleans_as_integers?: boolean;
  booleans?: boolean;
  collapse_vars?: boolean;
  comparisons?: boolean;
  computed_props?: boolean;
  conditionals?: boolean;
  dead_code?: boolean;
  defaults?: boolean;
  directives?: boolean;
  drop_console?: DropConsoleOption;
  drop_debugger?: boolean;
  ecma?: ECMA;
  evaluate?: boolean;
  expression?: boolean;
  global_defs?: object;
  hoist_funs?: boolean;
  hoist_props?: boolean;
  hoist_vars?: boolean;
  ie8?: boolean;
  if_return?: boolean;
  inline?: boolean | InlineFunctions;
  join_vars?: boolean;
  keep_classnames?: boolean | RegExp;
  keep_fargs?: boolean;
  keep_fnames?: boolean | RegExp;
  keep_infinity?: boolean;
  lhs_constants?: boolean;
  loops?: boolean;
  module?: boolean;
  negate_iife?: boolean;
  passes?: number;
  properties?: boolean;
  pure_funcs?: string[];
  pure_new?: boolean;
  pure_getters?: boolean | 'strict';
  reduce_funcs?: boolean;
  reduce_vars?: boolean;
  sequences?: boolean | number;
  side_effects?: boolean;
  switches?: boolean;
  toplevel?: boolean;
  top_retain?: null | string | string[] | RegExp;
  typeofs?: boolean;
  unsafe_arrows?: boolean;
  unsafe?: boolean;
  unsafe_comps?: boolean;
  unsafe_Function?: boolean;
  unsafe_math?: boolean;
  unsafe_symbols?: boolean;
  unsafe_methods?: boolean;
  unsafe_proto?: boolean;
  unsafe_regexp?: boolean;
  unsafe_undefined?: boolean;
  unused?: boolean;
}
declare enum InlineFunctions {
  Disabled = 0,
  SimpleFunctions = 1,
  WithArguments = 2,
  WithArgumentsAndVariables = 3
}
interface MangleOptions {
  eval?: boolean;
  keep_classnames?: boolean | RegExp;
  keep_fnames?: boolean | RegExp;
  module?: boolean;
  nth_identifier?: SimpleIdentifierMangler | WeightedIdentifierMangler;
  properties?: boolean | ManglePropertiesOptions;
  reserved?: string[];
  safari10?: boolean;
  toplevel?: boolean;
}
/**
 * An identifier mangler for which the output is invariant with respect to the source code.
 */
interface SimpleIdentifierMangler {
  /**
   * Obtains the nth most favored (usually shortest) identifier to rename a variable to.
   * The mangler will increment n and retry until the return value is not in use in scope, and is not a reserved word.
   * This function is expected to be stable; Evaluating get(n) === get(n) should always return true.
   * @param n The ordinal of the identifier.
   */
  get(n: number): string;
}
/**
 * An identifier mangler that leverages character frequency analysis to determine identifier precedence.
 */
interface WeightedIdentifierMangler extends SimpleIdentifierMangler {
  /**
   * Modifies the internal weighting of the input characters by the specified delta.
   * Will be invoked on the entire printed AST, and then deduct mangleable identifiers.
   * @param chars The characters to modify the weighting of.
   * @param delta The numeric weight to add to the characters.
   */
  consider(chars: string, delta: number): number;
  /**
   * Resets character weights.
   */
  reset(): void;
  /**
   * Sorts identifiers by character frequency, in preparation for calls to get(n).
   */
  sort(): void;
}
interface ManglePropertiesOptions {
  builtins?: boolean;
  debug?: boolean;
  keep_quoted?: boolean | 'strict';
  nth_identifier?: SimpleIdentifierMangler | WeightedIdentifierMangler;
  regex?: RegExp | string;
  reserved?: string[];
}
interface FormatOptions {
  ascii_only?: boolean;
  /** @deprecated Not implemented anymore */
  beautify?: boolean;
  braces?: boolean;
  comments?: boolean | 'all' | 'some' | RegExp | ((node: any, comment: {
    value: string;
    type: 'comment1' | 'comment2' | 'comment3' | 'comment4';
    pos: number;
    line: number;
    col: number;
  }) => boolean);
  ecma?: ECMA;
  ie8?: boolean;
  keep_numbers?: boolean;
  indent_level?: number;
  indent_start?: number;
  inline_script?: boolean;
  keep_quoted_props?: boolean;
  max_line_len?: number | false;
  preamble?: string;
  preserve_annotations?: boolean;
  quote_keys?: boolean;
  quote_style?: OutputQuoteStyle;
  safari10?: boolean;
  semicolons?: boolean;
  shebang?: boolean;
  shorthand?: boolean;
  source_map?: SourceMapOptions$1;
  webkit?: boolean;
  width?: number;
  wrap_iife?: boolean;
  wrap_func_args?: boolean;
}
declare enum OutputQuoteStyle {
  PreferDouble = 0,
  AlwaysSingle = 1,
  AlwaysDouble = 2,
  AlwaysOriginal = 3
}
interface MinifyOptions {
  compress?: boolean | CompressOptions;
  ecma?: ECMA;
  enclose?: boolean | string;
  ie8?: boolean;
  keep_classnames?: boolean | RegExp;
  keep_fnames?: boolean | RegExp;
  mangle?: boolean | MangleOptions;
  module?: boolean;
  nameCache?: object;
  format?: FormatOptions;
  /** @deprecated */
  output?: FormatOptions;
  parse?: ParseOptions;
  safari10?: boolean;
  sourceMap?: boolean | SourceMapOptions$1;
  toplevel?: boolean;
}
interface SourceMapOptions$1 {
  /** Source map object, 'inline' or source map file content */
  content?: SectionedSourceMapInput | string;
  includeSources?: boolean;
  filename?: string;
  root?: string;
  asObject?: boolean;
  url?: string | 'inline';
}
//#endregion
//#region ../../node_modules/.pnpm/vite@7.1.10_@types+node@24.7.2_jiti@2.5.1_sass-embedded@1.93.2_sass@1.93.2_terser@5.44.0_tsx@4.20.6_yaml@2.8.1/node_modules/vite/types/internal/terserOptions.d.ts
/* eslint-enable @typescript-eslint/ban-ts-comment */
type TerserMinifyOptions = MinifyOptions;
//#endregion
//#region ../../node_modules/.pnpm/vite@7.1.10_@types+node@24.7.2_jiti@2.5.1_sass-embedded@1.93.2_sass@1.93.2_terser@5.44.0_tsx@4.20.6_yaml@2.8.1/node_modules/vite/types/internal/lightningcssOptions.d.ts
/* eslint-enable @typescript-eslint/ban-ts-comment */
type LightningCSSOptions = Omit<Lightningcss.BundleAsyncOptions<Lightningcss.CustomAtRules>, 'filename' | 'resolver' | 'minify' | 'sourceMap' | 'analyzeDependencies' // properties not overridden by Vite, but does not make sense to set by end users
| 'inputSourceMap' | 'projectRoot'>;
//#endregion
//#region ../../node_modules/.pnpm/vite@7.1.10_@types+node@24.7.2_jiti@2.5.1_sass-embedded@1.93.2_sass@1.93.2_terser@5.44.0_tsx@4.20.6_yaml@2.8.1/node_modules/vite/types/internal/cssPreprocessorOptions.d.ts
/* eslint-enable @typescript-eslint/ban-ts-comment */
// https://github.com/type-challenges/type-challenges/issues/29285
type IsAny<T> = boolean extends (T extends never ? true : false) ? true : false;
type DartSassStringOptionsAsync = DartSass.StringOptions<'async'>;
type SassEmbeddedStringOptionsAsync = SassEmbedded.StringOptions<'async'>;
type SassStringOptionsAsync = IsAny<SassEmbeddedStringOptionsAsync> extends false ? SassEmbeddedStringOptionsAsync : DartSassStringOptionsAsync;
type SassModernPreprocessBaseOptions = Omit<SassStringOptionsAsync, 'url' | 'sourceMap'>;
type LessPreprocessorBaseOptions = Omit<Less.Options, 'sourceMap' | 'filename'>;
type StylusPreprocessorBaseOptions = Omit<Stylus.RenderOptions, 'filename'> & {
  define?: Record<string, any>;
};
declare global {
  // LESS' types somewhat references this which doesn't make sense in Node,
  // so we have to shim it
  // eslint-disable-next-line @typescript-eslint/no-empty-object-type
  interface HTMLLinkElement {}
}
//#endregion
//#region ../../node_modules/.pnpm/vite@7.1.10_@types+node@24.7.2_jiti@2.5.1_sass-embedded@1.93.2_sass@1.93.2_terser@5.44.0_tsx@4.20.6_yaml@2.8.1/node_modules/vite/types/importGlob.d.ts
/**
 * Declare Worker in case DOM is not added to the tsconfig lib causing
 * Worker interface is not defined. For developers with DOM lib added,
 * the Worker interface will be merged correctly.
 */
declare global {
  // eslint-disable-next-line @typescript-eslint/no-empty-object-type
  interface Worker {}
}
//#endregion
//#region ../../node_modules/.pnpm/vite@7.1.10_@types+node@24.7.2_jiti@2.5.1_sass-embedded@1.93.2_sass@1.93.2_terser@5.44.0_tsx@4.20.6_yaml@2.8.1/node_modules/vite/types/metadata.d.ts
interface ChunkMetadata {
  importedAssets: Set<string>;
  importedCss: Set<string>;
}
interface CustomPluginOptionsVite {
  /**
   * If this is a CSS Rollup module, you can scope to its importer's exports
   * so that if those exports are treeshaken away, the CSS module will also
   * be treeshaken.
   *
   * The "importerId" must import the CSS Rollup module statically.
   *
   * Example config if the CSS id is `/src/App.vue?vue&type=style&lang.css`:
   * ```js
   * cssScopeTo: ['/src/App.vue', 'default']
   * ```
   */
  cssScopeTo?: readonly [importerId: string, exportName: string | undefined];
  /** @deprecated no-op since Vite 6.1 */
  lang?: string;
}
declare module 'rollup' {
  export interface RenderedChunk {
    viteMetadata?: ChunkMetadata;
  }
  export interface CustomPluginOptions {
    vite?: CustomPluginOptionsVite;
  }
}
//#endregion
//#region ../../node_modules/.pnpm/vite@7.1.10_@types+node@24.7.2_jiti@2.5.1_sass-embedded@1.93.2_sass@1.93.2_terser@5.44.0_tsx@4.20.6_yaml@2.8.1/node_modules/vite/dist/node/index.d.ts
//#region rolldown:runtime
//#endregion
//#region src/types/alias.d.ts
interface Alias {
  find: string | RegExp;
  replacement: string;
  /**
   * Instructs the plugin to use an alternative resolving algorithm,
   * rather than the Rollup's resolver.
   * @default null
   */
  customResolver?: ResolverFunction | ResolverObject | null;
}
type MapToFunction<T> = T extends Function ? T : never;
type ResolverFunction = MapToFunction<PluginHooks['resolveId']>;
interface ResolverObject {
  buildStart?: PluginHooks['buildStart'];
  resolveId: ResolverFunction;
}
/**
 * Specifies an `Object`, or an `Array` of `Object`,
 * which defines aliases used to replace values in `import` or `require` statements.
 * With either format, the order of the entries is important,
 * in that the first defined rules are applied first.
 *
 * This is passed to \@rollup/plugin-alias as the "entries" field
 * https://github.com/rollup/plugins/tree/master/packages/alias#entries
 */
type AliasOptions = readonly Alias[] | {
  [find: string]: string;
}; //#endregion
//#region src/types/anymatch.d.ts
type AnymatchFn = (testString: string) => boolean;
type AnymatchPattern = string | RegExp | AnymatchFn;
type AnymatchMatcher = AnymatchPattern | AnymatchPattern[]; //#endregion
//#region src/types/chokidar.d.ts
declare class FSWatcher extends EventEmitter implements fs.FSWatcher {
  options: WatchOptions;
  /**
   * Constructs a new FSWatcher instance with optional WatchOptions parameter.
   */
  constructor(options?: WatchOptions);
  /**
   * When called, requests that the Node.js event loop not exit so long as the fs.FSWatcher is active.
   * Calling watcher.ref() multiple times will have no effect.
   */
  ref(): this;
  /**
   * When called, the active fs.FSWatcher object will not require the Node.js event loop to remain active.
   * If there is no other activity keeping the event loop running, the process may exit before the fs.FSWatcher object's callback is invoked.
   * Calling watcher.unref() multiple times will have no effect.
   */
  unref(): this;
  /**
   * Add files, directories, or glob patterns for tracking. Takes an array of strings or just one
   * string.
   */
  add(paths: string | ReadonlyArray<string>): this;
  /**
   * Stop watching files, directories, or glob patterns. Takes an array of strings or just one
   * string.
   */
  unwatch(paths: string | ReadonlyArray<string>): this;
  /**
   * Returns an object representing all the paths on the file system being watched by this
   * `FSWatcher` instance. The object's keys are all the directories (using absolute paths unless
   * the `cwd` option was used), and the values are arrays of the names of the items contained in
   * each directory.
   */
  getWatched(): {
    [directory: string]: string[];
  };
  /**
   * Removes all listeners from watched files.
   */
  close(): Promise<void>;
  on(event: 'add' | 'addDir' | 'change', listener: (path: string, stats?: fs.Stats) => void): this;
  on(event: 'all', listener: (eventName: 'add' | 'addDir' | 'change' | 'unlink' | 'unlinkDir', path: string, stats?: fs.Stats) => void): this;
  /**
   * Error occurred
   */
  on(event: 'error', listener: (error: Error) => void): this;
  /**
   * Exposes the native Node `fs.FSWatcher events`
   */
  on(event: 'raw', listener: (eventName: string, path: string, details: any) => void): this;
  /**
   * Fires when the initial scan is complete
   */
  on(event: 'ready', listener: () => void): this;
  on(event: 'unlink' | 'unlinkDir', listener: (path: string) => void): this;
  on(event: string, listener: (...args: any[]) => void): this;
}
interface WatchOptions {
  /**
   * Indicates whether the process should continue to run as long as files are being watched. If
   * set to `false` when using `fsevents` to watch, no more events will be emitted after `ready`,
   * even if the process continues to run.
   */
  persistent?: boolean;
  /**
   * ([anymatch](https://github.com/micromatch/anymatch)-compatible definition) Defines files/paths to
   * be ignored. The whole relative or absolute path is tested, not just filename. If a function
   * with two arguments is provided, it gets called twice per path - once with a single argument
   * (the path), second time with two arguments (the path and the
   * [`fs.Stats`](https://nodejs.org/api/fs.html#fs_class_fs_stats) object of that path).
   */
  ignored?: AnymatchMatcher;
  /**
   * If set to `false` then `add`/`addDir` events are also emitted for matching paths while
   * instantiating the watching as chokidar discovers these file paths (before the `ready` event).
   */
  ignoreInitial?: boolean;
  /**
   * When `false`, only the symlinks themselves will be watched for changes instead of following
   * the link references and bubbling events through the link's path.
   */
  followSymlinks?: boolean;
  /**
   * The base directory from which watch `paths` are to be derived. Paths emitted with events will
   * be relative to this.
   */
  cwd?: string;
  /**
   * If set to true then the strings passed to .watch() and .add() are treated as literal path
   * names, even if they look like globs.
   *
   * @default false
   */
  disableGlobbing?: boolean;
  /**
   * Whether to use fs.watchFile (backed by polling), or fs.watch. If polling leads to high CPU
   * utilization, consider setting this to `false`. It is typically necessary to **set this to
   * `true` to successfully watch files over a network**, and it may be necessary to successfully
   * watch files in other non-standard situations. Setting to `true` explicitly on OS X overrides
   * the `useFsEvents` default.
   */
  usePolling?: boolean;
  /**
   * Whether to use the `fsevents` watching interface if available. When set to `true` explicitly
   * and `fsevents` is available this supersedes the `usePolling` setting. When set to `false` on
   * OS X, `usePolling: true` becomes the default.
   */
  useFsEvents?: boolean;
  /**
   * If relying upon the [`fs.Stats`](https://nodejs.org/api/fs.html#fs_class_fs_stats) object that
   * may get passed with `add`, `addDir`, and `change` events, set this to `true` to ensure it is
   * provided even in cases where it wasn't already available from the underlying watch events.
   */
  alwaysStat?: boolean;
  /**
   * If set, limits how many levels of subdirectories will be traversed.
   */
  depth?: number;
  /**
   * Interval of file system polling.
   */
  interval?: number;
  /**
   * Interval of file system polling for binary files. ([see list of binary extensions](https://gi
   * thub.com/sindresorhus/binary-extensions/blob/master/binary-extensions.json))
   */
  binaryInterval?: number;
  /**
   *  Indicates whether to watch files that don't have read permissions if possible. If watching
   *  fails due to `EPERM` or `EACCES` with this set to `true`, the errors will be suppressed
   *  silently.
   */
  ignorePermissionErrors?: boolean;
  /**
   * `true` if `useFsEvents` and `usePolling` are `false`. Automatically filters out artifacts
   * that occur when using editors that use "atomic writes" instead of writing directly to the
   * source file. If a file is re-added within 100 ms of being deleted, Chokidar emits a `change`
   * event rather than `unlink` then `add`. If the default of 100 ms does not work well for you,
   * you can override it by setting `atomic` to a custom value, in milliseconds.
   */
  atomic?: boolean | number;
  /**
   * can be set to an object in order to adjust timing params:
   */
  awaitWriteFinish?: AwaitWriteFinishOptions | boolean;
}
interface AwaitWriteFinishOptions {
  /**
   * Amount of time in milliseconds for a file size to remain constant before emitting its event.
   */
  stabilityThreshold?: number;
  /**
   * File size polling interval.
   */
  pollInterval?: number;
} //#endregion
//#region src/types/connect.d.ts
declare namespace Connect {
  export type ServerHandle = HandleFunction | http.Server;
  export class IncomingMessage extends http.IncomingMessage {
    originalUrl?: http.IncomingMessage['url'] | undefined;
  }
  export type NextFunction = (err?: any) => void;
  export type SimpleHandleFunction = (req: IncomingMessage, res: http.ServerResponse) => void;
  export type NextHandleFunction = (req: IncomingMessage, res: http.ServerResponse, next: NextFunction) => void;
  export type ErrorHandleFunction = (err: any, req: IncomingMessage, res: http.ServerResponse, next: NextFunction) => void;
  export type HandleFunction = SimpleHandleFunction | NextHandleFunction | ErrorHandleFunction;
  export interface ServerStackItem {
    route: string;
    handle: ServerHandle;
  }
  export interface Server extends NodeJS.EventEmitter {
    (req: http.IncomingMessage, res: http.ServerResponse, next?: Function): void;
    route: string;
    stack: ServerStackItem[];
    /**
     * Utilize the given middleware `handle` to the given `route`,
     * defaulting to _/_. This "route" is the mount-point for the
     * middleware, when given a value other than _/_ the middleware
     * is only effective when that segment is present in the request's
     * pathname.
     *
     * For example if we were to mount a function at _/admin_, it would
     * be invoked on _/admin_, and _/admin/settings_, however it would
     * not be invoked for _/_, or _/posts_.
     */
    use(fn: NextHandleFunction): Server;
    use(fn: HandleFunction): Server;
    use(route: string, fn: NextHandleFunction): Server;
    use(route: string, fn: HandleFunction): Server;
    /**
     * Handle server requests, punting them down
     * the middleware stack.
     */
    handle(req: http.IncomingMessage, res: http.ServerResponse, next: Function): void;
    /**
     * Listen for connections.
     *
     * This method takes the same arguments
     * as node's `http.Server#listen()`.
     *
     * HTTP and HTTPS:
     *
     * If you run your application both as HTTP
     * and HTTPS you may wrap them individually,
     * since your Connect "server" is really just
     * a JavaScript `Function`.
     *
     *      var connect = require('connect')
     *        , http = require('http')
     *        , https = require('https');
     *
     *      var app = connect();
     *
     *      http.createServer(app).listen(80);
     *      https.createServer(options, app).listen(443);
     */
    listen(port: number, hostname?: string, backlog?: number, callback?: Function): http.Server;
    listen(port: number, hostname?: string, callback?: Function): http.Server;
    listen(path: string, callback?: Function): http.Server;
    listen(handle: any, listeningListener?: Function): http.Server;
  }
} //#endregion
//#region ../../node_modules/.pnpm/http-proxy-3@1.22.0/node_modules/http-proxy-3/dist/lib/http-proxy/index.d.ts
interface ProxyTargetDetailed {
  host: string;
  port: number;
  protocol?: string;
  hostname?: string;
  socketPath?: string;
  key?: string;
  passphrase?: string;
  pfx?: Buffer | string;
  cert?: string;
  ca?: string;
  ciphers?: string;
  secureProtocol?: string;
}
type ProxyType = "ws" | "web";
type ProxyTarget = ProxyTargetUrl | ProxyTargetDetailed;
type ProxyTargetUrl = URL | string | {
  port: number;
  host: string;
  protocol?: string;
};
type NormalizeProxyTarget<T extends ProxyTargetUrl> = Exclude<T, string> | URL;
interface ServerOptions$3 {
  /** URL string to be parsed with the url module. */
  target?: ProxyTarget;
  /** URL string to be parsed with the url module or a URL object. */
  forward?: ProxyTargetUrl;
  /** Object to be passed to http(s).request. */
  agent?: any;
  /** Object to be passed to https.createServer(). */
  ssl?: any;
  /** If you want to proxy websockets. */
  ws?: boolean;
  /** Adds x- forward headers. */
  xfwd?: boolean;
  /** Verify SSL certificate. */
  secure?: boolean;
  /** Explicitly specify if we are proxying to another proxy. */
  toProxy?: boolean;
  /** Specify whether you want to prepend the target's path to the proxy path. */
  prependPath?: boolean;
  /** Specify whether you want to ignore the proxy path of the incoming request. */
  ignorePath?: boolean;
  /** Local interface string to bind for outgoing connections. */
  localAddress?: string;
  /** Changes the origin of the host header to the target URL. */
  changeOrigin?: boolean;
  /** specify whether you want to keep letter case of response header key */
  preserveHeaderKeyCase?: boolean;
  /** Basic authentication i.e. 'user:password' to compute an Authorization header. */
  auth?: string;
  /** Rewrites the location hostname on (301 / 302 / 307 / 308) redirects, Default: null. */
  hostRewrite?: string;
  /** Rewrites the location host/ port on (301 / 302 / 307 / 308) redirects based on requested host/ port.Default: false. */
  autoRewrite?: boolean;
  /** Rewrites the location protocol on (301 / 302 / 307 / 308) redirects to 'http' or 'https'.Default: null. */
  protocolRewrite?: string;
  /** rewrites domain of set-cookie headers. */
  cookieDomainRewrite?: false | string | {
    [oldDomain: string]: string;
  };
  /** rewrites path of set-cookie headers. Default: false */
  cookiePathRewrite?: false | string | {
    [oldPath: string]: string;
  };
  /** object with extra headers to be added to target requests. */
  headers?: {
    [header: string]: string | string[] | undefined;
  };
  /** Timeout (in milliseconds) when proxy receives no response from target. Default: 120000 (2 minutes) */
  proxyTimeout?: number;
  /** Timeout (in milliseconds) for incoming requests */
  timeout?: number;
  /** Specify whether you want to follow redirects. Default: false */
  followRedirects?: boolean;
  /** If set to true, none of the webOutgoing passes are called and it's your responsibility to appropriately return the response by listening and acting on the proxyRes event */
  selfHandleResponse?: boolean;
  /** Buffer */
  buffer?: Stream;
  /** Explicitly set the method type of the ProxyReq */
  method?: string;
  /**
   * Optionally override the trusted CA certificates.
   * This is passed to https.request.
   */
  ca?: string;
}
interface NormalizedServerOptions extends ServerOptions$3 {
  target?: NormalizeProxyTarget<ProxyTarget>;
  forward?: NormalizeProxyTarget<ProxyTargetUrl>;
}
type ErrorCallback<TIncomingMessage extends typeof http.IncomingMessage = typeof http.IncomingMessage, TServerResponse extends typeof http.ServerResponse = typeof http.ServerResponse, TError = Error> = (err: TError, req: InstanceType<TIncomingMessage>, res: InstanceType<TServerResponse> | net.Socket, target?: ProxyTargetUrl) => void;
type ProxyServerEventMap<TIncomingMessage extends typeof http.IncomingMessage = typeof http.IncomingMessage, TServerResponse extends typeof http.ServerResponse = typeof http.ServerResponse, TError = Error> = {
  error: Parameters<ErrorCallback<TIncomingMessage, TServerResponse, TError>>;
  start: [req: InstanceType<TIncomingMessage>, res: InstanceType<TServerResponse>, target: ProxyTargetUrl];
  open: [socket: net.Socket];
  proxyReq: [proxyReq: http.ClientRequest, req: InstanceType<TIncomingMessage>, res: InstanceType<TServerResponse>, options: ServerOptions$3, socket: net.Socket];
  proxyRes: [proxyRes: InstanceType<TIncomingMessage>, req: InstanceType<TIncomingMessage>, res: InstanceType<TServerResponse>];
  proxyReqWs: [proxyReq: http.ClientRequest, req: InstanceType<TIncomingMessage>, socket: net.Socket, options: ServerOptions$3, head: any];
  econnreset: [err: Error, req: InstanceType<TIncomingMessage>, res: InstanceType<TServerResponse>, target: ProxyTargetUrl];
  end: [req: InstanceType<TIncomingMessage>, res: InstanceType<TServerResponse>, proxyRes: InstanceType<TIncomingMessage>];
  close: [proxyRes: InstanceType<TIncomingMessage>, proxySocket: net.Socket, proxyHead: any];
};
type ProxyMethodArgs<TIncomingMessage extends typeof http.IncomingMessage = typeof http.IncomingMessage, TServerResponse extends typeof http.ServerResponse = typeof http.ServerResponse, TError = Error> = {
  ws: [req: InstanceType<TIncomingMessage>, socket: any, head: any, ...args: [options?: ServerOptions$3, callback?: ErrorCallback<TIncomingMessage, TServerResponse, TError>] | [callback?: ErrorCallback<TIncomingMessage, TServerResponse, TError>]];
  web: [req: InstanceType<TIncomingMessage>, res: InstanceType<TServerResponse>, ...args: [options: ServerOptions$3, callback?: ErrorCallback<TIncomingMessage, TServerResponse, TError>] | [callback?: ErrorCallback<TIncomingMessage, TServerResponse, TError>]];
};
type PassFunctions<TIncomingMessage extends typeof http.IncomingMessage = typeof http.IncomingMessage, TServerResponse extends typeof http.ServerResponse = typeof http.ServerResponse, TError = Error> = {
  ws: (req: InstanceType<TIncomingMessage>, socket: net.Socket, options: NormalizedServerOptions, head: Buffer | undefined, server: ProxyServer<TIncomingMessage, TServerResponse, TError>, cb?: ErrorCallback<TIncomingMessage, TServerResponse, TError>) => unknown;
  web: (req: InstanceType<TIncomingMessage>, res: InstanceType<TServerResponse>, options: NormalizedServerOptions, head: Buffer | undefined, server: ProxyServer<TIncomingMessage, TServerResponse, TError>, cb?: ErrorCallback<TIncomingMessage, TServerResponse, TError>) => unknown;
};
declare class ProxyServer<TIncomingMessage extends typeof http.IncomingMessage = typeof http.IncomingMessage, TServerResponse extends typeof http.ServerResponse = typeof http.ServerResponse, TError = Error> extends EventEmitter<ProxyServerEventMap<TIncomingMessage, TServerResponse, TError>> {
  /**
   * Used for proxying WS(S) requests
   * @param req - Client request.
   * @param socket - Client socket.
   * @param head - Client head.
   * @param options - Additional options.
   */
  readonly ws: (...args: ProxyMethodArgs<TIncomingMessage, TServerResponse, TError>["ws"]) => void;
  /**
   * Used for proxying regular HTTP(S) requests
   * @param req - Client request.
   * @param res - Client response.
   * @param options - Additional options.
   */
  readonly web: (...args: ProxyMethodArgs<TIncomingMessage, TServerResponse, TError>["web"]) => void;
  private options;
  private webPasses;
  private wsPasses;
  private _server?;
  /**
   * Creates the proxy server with specified options.
   * @param options - Config object passed to the proxy
   */
  constructor(options?: ServerOptions$3);
  /**
   * Creates the proxy server with specified options.
   * @param options Config object passed to the proxy
   * @returns Proxy object with handlers for `ws` and `web` requests
   */
  static createProxyServer<TIncomingMessage extends typeof http.IncomingMessage, TServerResponse extends typeof http.ServerResponse, TError = Error>(options?: ServerOptions$3): ProxyServer<TIncomingMessage, TServerResponse, TError>;
  /**
   * Creates the proxy server with specified options.
   * @param options Config object passed to the proxy
   * @returns Proxy object with handlers for `ws` and `web` requests
   */
  static createServer<TIncomingMessage extends typeof http.IncomingMessage, TServerResponse extends typeof http.ServerResponse, TError = Error>(options?: ServerOptions$3): ProxyServer<TIncomingMessage, TServerResponse, TError>;
  /**
   * Creates the proxy server with specified options.
   * @param options Config object passed to the proxy
   * @returns Proxy object with handlers for `ws` and `web` requests
   */
  static createProxy<TIncomingMessage extends typeof http.IncomingMessage, TServerResponse extends typeof http.ServerResponse, TError = Error>(options?: ServerOptions$3): ProxyServer<TIncomingMessage, TServerResponse, TError>;
  createRightProxy: <PT extends ProxyType>(type: PT) => Function;
  onError: (err: TError) => void;
  /**
   * A function that wraps the object in a webserver, for your convenience
   * @param port - Port to listen on
   * @param hostname - The hostname to listen on
   */
  listen: (port: number, hostname?: string) => this;
  address: () => string | net.AddressInfo | null | undefined;
  /**
   * A function that closes the inner webserver and stops listening on given port
   */
  close: (cb?: Function) => void;
  before: <PT extends ProxyType>(type: PT, passName: string, cb: PassFunctions<TIncomingMessage, TServerResponse, TError>[PT]) => void;
  after: <PT extends ProxyType>(type: PT, passName: string, cb: PassFunctions<TIncomingMessage, TServerResponse, TError>[PT]) => void;
} //#endregion
//#region ../../node_modules/.pnpm/http-proxy-3@1.22.0/node_modules/http-proxy-3/dist/lib/http-proxy/passes/ws-incoming.d.ts
//#endregion
//#region src/node/server/middlewares/proxy.d.ts
interface ProxyOptions extends ServerOptions$3 {
  /**
   * rewrite path
   */
  rewrite?: (path: string) => string;
  /**
   * configure the proxy server (e.g. listen to events)
   */
  configure?: (proxy: ProxyServer, options: ProxyOptions) => void;
  /**
   * webpack-dev-server style bypass function
   */
  bypass?: (req: http.IncomingMessage, /** undefined for WebSocket upgrade requests */

  res: http.ServerResponse | undefined, options: ProxyOptions) => void | null | undefined | false | string | Promise<void | null | undefined | boolean | string>;
  /**
   * rewrite the Origin header of a WebSocket request to match the target
   *
   * **Exercise caution as rewriting the Origin can leave the proxying open to [CSRF attacks](https://owasp.org/www-community/attacks/csrf).**
   */
  rewriteWsOrigin?: boolean | undefined;
} //#endregion
//#region src/node/logger.d.ts
type LogType = 'error' | 'warn' | 'info';
type LogLevel = LogType | 'silent';
interface Logger {
  info(msg: string, options?: LogOptions): void;
  warn(msg: string, options?: LogOptions): void;
  warnOnce(msg: string, options?: LogOptions): void;
  error(msg: string, options?: LogErrorOptions): void;
  clearScreen(type: LogType): void;
  hasErrorLogged(error: Error | RollupError): boolean;
  hasWarned: boolean;
}
interface LogOptions {
  clear?: boolean;
  timestamp?: boolean;
  environment?: string;
}
interface LogErrorOptions extends LogOptions {
  error?: Error | RollupError | null;
}
//#endregion
//#region src/node/http.d.ts
interface CommonServerOptions {
  /**
   * Specify server port. Note if the port is already being used, Vite will
   * automatically try the next available port so this may not be the actual
   * port the server ends up listening on.
   */
  port?: number;
  /**
   * If enabled, vite will exit if specified port is already in use
   */
  strictPort?: boolean;
  /**
   * Specify which IP addresses the server should listen on.
   * Set to 0.0.0.0 to listen on all addresses, including LAN and public addresses.
   */
  host?: string | boolean;
  /**
   * The hostnames that Vite is allowed to respond to.
   * `localhost` and subdomains under `.localhost` and all IP addresses are allowed by default.
   * When using HTTPS, this check is skipped.
   *
   * If a string starts with `.`, it will allow that hostname without the `.` and all subdomains under the hostname.
   * For example, `.example.com` will allow `example.com`, `foo.example.com`, and `foo.bar.example.com`.
   *
   * If set to `true`, the server is allowed to respond to requests for any hosts.
   * This is not recommended as it will be vulnerable to DNS rebinding attacks.
   */
  allowedHosts?: string[] | true;
  /**
   * Enable TLS + HTTP/2.
   * Note: this downgrades to TLS only when the proxy option is also used.
   */
  https?: ServerOptions$1;
  /**
   * Open browser window on startup
   */
  open?: boolean | string;
  /**
   * Configure custom proxy rules for the dev server. Expects an object
   * of `{ key: options }` pairs.
   * Uses [`http-proxy-3`](https://github.com/sagemathinc/http-proxy-3).
   * Full options [here](https://github.com/sagemathinc/http-proxy-3#options).
   *
   * Example `vite.config.js`:
   * ``` js
   * module.exports = {
   *   proxy: {
   *     // string shorthand: /foo -> http://localhost:4567/foo
   *     '/foo': 'http://localhost:4567',
   *     // with options
   *     '/api': {
   *       target: 'http://jsonplaceholder.typicode.com',
   *       changeOrigin: true,
   *       rewrite: path => path.replace(/^\/api/, '')
   *     }
   *   }
   * }
   * ```
   */
  proxy?: Record<string, string | ProxyOptions>;
  /**
   * Configure CORS for the dev server.
   * Uses https://github.com/expressjs/cors.
   *
   * When enabling this option, **we recommend setting a specific value
   * rather than `true`** to avoid exposing the source code to untrusted origins.
   *
   * Set to `true` to allow all methods from any origin, or configure separately
   * using an object.
   *
   * @default false
   */
  cors?: CorsOptions | boolean;
  /**
   * Specify server response headers.
   */
  headers?: OutgoingHttpHeaders;
}
/**
 * https://github.com/expressjs/cors#configuration-options
 */
interface CorsOptions {
  /**
   * Configures the Access-Control-Allow-Origin CORS header.
   *
   * **We recommend setting a specific value rather than
   * `true`** to avoid exposing the source code to untrusted origins.
   */
  origin?: CorsOrigin | ((origin: string | undefined, cb: (err: Error, origins: CorsOrigin) => void) => void);
  methods?: string | string[];
  allowedHeaders?: string | string[];
  exposedHeaders?: string | string[];
  credentials?: boolean;
  maxAge?: number;
  preflightContinue?: boolean;
  optionsSuccessStatus?: number;
}
type CorsOrigin = boolean | string | RegExp | (string | RegExp)[]; //#endregion
//#region src/node/typeUtils.d.ts
type RequiredExceptFor<T, K extends keyof T> = Pick<T, K> & Required<Omit<T, K>>; //#endregion
//#region src/node/preview.d.ts
interface PreviewOptions extends CommonServerOptions {}
interface ResolvedPreviewOptions extends RequiredExceptFor<PreviewOptions, 'host' | 'https' | 'proxy'> {}
interface PreviewServer {
  /**
   * The resolved vite config object
   */
  config: ResolvedConfig;
  /**
   * Stop the server.
   */
  close(): Promise<void>;
  /**
   * A connect app instance.
   * - Can be used to attach custom middlewares to the preview server.
   * - Can also be used as the handler function of a custom http server
   *   or as a middleware in any connect-style Node.js frameworks
   *
   * https://github.com/senchalabs/connect#use-middleware
   */
  middlewares: Connect.Server;
  /**
   * native Node http server instance
   */
  httpServer: HttpServer;
  /**
   * The resolved urls Vite prints on the CLI (URL-encoded). Returns `null`
   * if the server is not listening on any port.
   */
  resolvedUrls: ResolvedServerUrls | null;
  /**
   * Print server urls
   */
  printUrls(): void;
  /**
   * Bind CLI shortcuts
   */
  bindCLIShortcuts(options?: BindCLIShortcutsOptions<PreviewServer>): void;
}
type PreviewServerHook = (this: MinimalPluginContextWithoutEnvironment, server: PreviewServer) => (() => void) | void | Promise<(() => void) | void>;
/**
 * Starts the Vite server in preview mode, to simulate a production deployment
 */
//#endregion
//#region src/node/shortcuts.d.ts
type BindCLIShortcutsOptions<Server = ViteDevServer | PreviewServer> = {
  /**
   * Print a one-line shortcuts "help" hint to the terminal
   */
  print?: boolean;
  /**
   * Custom shortcuts to run when a key is pressed. These shortcuts take priority
   * over the default shortcuts if they have the same keys (except the `h` key).
   * To disable a default shortcut, define the same key but with `action: undefined`.
   */
  customShortcuts?: CLIShortcut<Server>[];
};
type CLIShortcut<Server = ViteDevServer | PreviewServer> = {
  key: string;
  description: string;
  action?(server: Server): void | Promise<void>;
}; //#endregion
//#region src/node/baseEnvironment.d.ts
declare class PartialEnvironment {
  name: string;
  getTopLevelConfig(): ResolvedConfig;
  config: ResolvedConfig & ResolvedEnvironmentOptions;
  logger: Logger;
  constructor(name: string, topLevelConfig: ResolvedConfig, options?: ResolvedEnvironmentOptions);
}
declare class BaseEnvironment extends PartialEnvironment {
  get plugins(): readonly Plugin$1[];
  constructor(name: string, config: ResolvedConfig, options?: ResolvedEnvironmentOptions);
}
/**
 * This class discourages users from inversely checking the `mode`
 * to determine the type of environment, e.g.
 *
 * ```js
 * const isDev = environment.mode !== 'build' // bad
 * const isDev = environment.mode === 'dev'   // good
 * ```
 *
 * You should also not check against `"unknown"` specifically. It's
 * a placeholder for more possible environment types.
 */
declare class UnknownEnvironment extends BaseEnvironment {
  mode: "unknown";
} //#endregion
//#region src/node/optimizer/scan.d.ts
//#endregion
//#region src/node/optimizer/index.d.ts
type ExportsData = {
  hasModuleSyntax: boolean;
  exports: readonly string[];
  jsxLoader?: boolean;
};
interface DepsOptimizer {
  init: () => Promise<void>;
  metadata: DepOptimizationMetadata;
  scanProcessing?: Promise<void>;
  registerMissingImport: (id: string, resolved: string) => OptimizedDepInfo;
  run: () => void;
  isOptimizedDepFile: (id: string) => boolean;
  isOptimizedDepUrl: (url: string) => boolean;
  getOptimizedDepId: (depInfo: OptimizedDepInfo) => string;
  close: () => Promise<void>;
  options: DepOptimizationOptions;
}
interface DepOptimizationConfig {
  /**
   * Force optimize listed dependencies (must be resolvable import paths,
   * cannot be globs).
   */
  include?: string[];
  /**
   * Do not optimize these dependencies (must be resolvable import paths,
   * cannot be globs).
   */
  exclude?: string[];
  /**
   * Forces ESM interop when importing these dependencies. Some legacy
   * packages advertise themselves as ESM but use `require` internally
   * @experimental
   */
  needsInterop?: string[];
  /**
   * Options to pass to esbuild during the dep scanning and optimization
   *
   * Certain options are omitted since changing them would not be compatible
   * with Vite's dep optimization.
   *
   * - `external` is also omitted, use Vite's `optimizeDeps.exclude` option
   * - `plugins` are merged with Vite's dep plugin
   *
   * https://esbuild.github.io/api
   */
  esbuildOptions?: Omit<BuildOptions$1, 'bundle' | 'entryPoints' | 'external' | 'write' | 'watch' | 'outdir' | 'outfile' | 'outbase' | 'outExtension' | 'metafile'>;
  /**
   * List of file extensions that can be optimized. A corresponding esbuild
   * plugin must exist to handle the specific extension.
   *
   * By default, Vite can optimize `.mjs`, `.js`, `.ts`, and `.mts` files. This option
   * allows specifying additional extensions.
   *
   * @experimental
   */
  extensions?: string[];
  /**
   * Deps optimization during build was removed in Vite 5.1. This option is
   * now redundant and will be removed in a future version. Switch to using
   * `optimizeDeps.noDiscovery` and an empty or undefined `optimizeDeps.include`.
   * true or 'dev' disables the optimizer, false or 'build' leaves it enabled.
   * @default 'build'
   * @deprecated
   * @experimental
   */
  disabled?: boolean | 'build' | 'dev';
  /**
   * Automatic dependency discovery. When `noDiscovery` is true, only dependencies
   * listed in `include` will be optimized. The scanner isn't run for cold start
   * in this case. CJS-only dependencies must be present in `include` during dev.
   * @default false
   */
  noDiscovery?: boolean;
  /**
   * When enabled, it will hold the first optimized deps results until all static
   * imports are crawled on cold start. This avoids the need for full-page reloads
   * when new dependencies are discovered and they trigger the generation of new
   * common chunks. If all dependencies are found by the scanner plus the explicitly
   * defined ones in `include`, it is better to disable this option to let the
   * browser process more requests in parallel.
   * @default true
   * @experimental
   */
  holdUntilCrawlEnd?: boolean;
}
type DepOptimizationOptions = DepOptimizationConfig & {
  /**
   * By default, Vite will crawl your `index.html` to detect dependencies that
   * need to be pre-bundled. If `build.rollupOptions.input` is specified, Vite
   * will crawl those entry points instead.
   *
   * If neither of these fit your needs, you can specify custom entries using
   * this option - the value should be a tinyglobby pattern or array of patterns
   * (https://github.com/SuperchupuDev/tinyglobby) that are relative from
   * vite project root. This will overwrite default entries inference.
   */
  entries?: string | string[];
  /**
   * Force dep pre-optimization regardless of whether deps have changed.
   * @experimental
   */
  force?: boolean;
};
interface OptimizedDepInfo {
  id: string;
  file: string;
  src?: string;
  needsInterop?: boolean;
  browserHash?: string;
  fileHash?: string;
  /**
   * During optimization, ids can still be resolved to their final location
   * but the bundles may not yet be saved to disk
   */
  processing?: Promise<void>;
  /**
   * ExportData cache, discovered deps will parse the src entry to get exports
   * data used both to define if interop is needed and when pre-bundling
   */
  exportsData?: Promise<ExportsData>;
}
interface DepOptimizationMetadata {
  /**
   * The main hash is determined by user config and dependency lockfiles.
   * This is checked on server startup to avoid unnecessary re-bundles.
   */
  hash: string;
  /**
   * This hash is determined by dependency lockfiles.
   * This is checked on server startup to avoid unnecessary re-bundles.
   */
  lockfileHash: string;
  /**
   * This hash is determined by user config.
   * This is checked on server startup to avoid unnecessary re-bundles.
   */
  configHash: string;
  /**
   * The browser hash is determined by the main hash plus additional dependencies
   * discovered at runtime. This is used to invalidate browser requests to
   * optimized deps.
   */
  browserHash: string;
  /**
   * Metadata for each already optimized dependency
   */
  optimized: Record<string, OptimizedDepInfo>;
  /**
   * Metadata for non-entry optimized chunks and dynamic imports
   */
  chunks: Record<string, OptimizedDepInfo>;
  /**
   * Metadata for each newly discovered dependency after processing
   */
  discovered: Record<string, OptimizedDepInfo>;
  /**
   * OptimizedDepInfo list
   */
  depInfoList: OptimizedDepInfo[];
}
/**
 * Scan and optimize dependencies within a project.
 * Used by Vite CLI when running `vite optimize`.
 *
 * @deprecated the optimization process runs automatically and does not need to be called
 */
//#endregion
//#region src/node/server/transformRequest.d.ts
interface TransformResult {
  code: string;
  map: SourceMap$2 | {
    mappings: '';
  } | null;
  ssr?: boolean;
  etag?: string;
  deps?: string[];
  dynamicDeps?: string[];
}
interface TransformOptions {
  /**
   * @deprecated inferred from environment
   */
  ssr?: boolean;
}
//#endregion
//#region src/node/server/moduleGraph.d.ts
declare class EnvironmentModuleNode {
  environment: string;
  /**
   * Public served url path, starts with /
   */
  url: string;
  /**
   * Resolved file system path + query
   */
  id: string | null;
  file: string | null;
  type: 'js' | 'css' | 'asset';
  info?: ModuleInfo$1;
  meta?: Record<string, any>;
  importers: Set<EnvironmentModuleNode>;
  importedModules: Set<EnvironmentModuleNode>;
  acceptedHmrDeps: Set<EnvironmentModuleNode>;
  acceptedHmrExports: Set<string> | null;
  importedBindings: Map<string, Set<string>> | null;
  isSelfAccepting?: boolean;
  transformResult: TransformResult | null;
  ssrModule: Record<string, any> | null;
  ssrError: Error | null;
  lastHMRTimestamp: number;
  lastInvalidationTimestamp: number;
  /**
   * @param setIsSelfAccepting - set `false` to set `isSelfAccepting` later. e.g. #7870
   */
  constructor(url: string, environment: string, setIsSelfAccepting?: boolean);
}
type ResolvedUrl = [url: string, resolvedId: string, meta: object | null | undefined];
declare class EnvironmentModuleGraph {
  environment: string;
  urlToModuleMap: Map<string, EnvironmentModuleNode>;
  idToModuleMap: Map<string, EnvironmentModuleNode>;
  etagToModuleMap: Map<string, EnvironmentModuleNode>;
  fileToModulesMap: Map<string, Set<EnvironmentModuleNode>>;
  constructor(environment: string, resolveId: (url: string) => Promise<PartialResolvedId | null>);
  getModuleByUrl(rawUrl: string): Promise<EnvironmentModuleNode | undefined>;
  getModuleById(id: string): EnvironmentModuleNode | undefined;
  getModulesByFile(file: string): Set<EnvironmentModuleNode> | undefined;
  onFileChange(file: string): void;
  onFileDelete(file: string): void;
  invalidateModule(mod: EnvironmentModuleNode, seen?: Set<EnvironmentModuleNode>, timestamp?: number, isHmr?: boolean): void;
  invalidateAll(): void;
  /**
   * Update the module graph based on a module's updated imports information
   * If there are dependencies that no longer have any importers, they are
   * returned as a Set.
   *
   * @param staticImportedUrls Subset of `importedModules` where they're statically imported in code.
   *   This is only used for soft invalidations so `undefined` is fine but may cause more runtime processing.
   */
  updateModuleInfo(mod: EnvironmentModuleNode, importedModules: Set<string | EnvironmentModuleNode>, importedBindings: Map<string, Set<string>> | null, acceptedModules: Set<string | EnvironmentModuleNode>, acceptedExports: Set<string> | null, isSelfAccepting: boolean): Promise<Set<EnvironmentModuleNode> | undefined>;
  ensureEntryFromUrl(rawUrl: string, setIsSelfAccepting?: boolean): Promise<EnvironmentModuleNode>;
  createFileOnlyEntry(file: string): EnvironmentModuleNode;
  resolveUrl(url: string): Promise<ResolvedUrl>;
  updateModuleTransformResult(mod: EnvironmentModuleNode, result: TransformResult | null): void;
  getModuleByEtag(etag: string): EnvironmentModuleNode | undefined;
} //#endregion
//#region src/node/server/mixedModuleGraph.d.ts
declare class ModuleNode {
  _moduleGraph: ModuleGraph;
  _clientModule: EnvironmentModuleNode | undefined;
  _ssrModule: EnvironmentModuleNode | undefined;
  constructor(moduleGraph: ModuleGraph, clientModule?: EnvironmentModuleNode, ssrModule?: EnvironmentModuleNode);
  _get<T extends keyof EnvironmentModuleNode>(prop: T): EnvironmentModuleNode[T];
  _set<T extends keyof EnvironmentModuleNode>(prop: T, value: EnvironmentModuleNode[T]): void;
  _wrapModuleSet(prop: ModuleSetNames, module: EnvironmentModuleNode | undefined): Set<ModuleNode>;
  _getModuleSetUnion(prop: 'importedModules' | 'importers'): Set<ModuleNode>;
  _getModuleInfoUnion(prop: 'info'): ModuleInfo$1 | undefined;
  _getModuleObjectUnion(prop: 'meta'): Record<string, any> | undefined;
  get url(): string;
  set url(value: string);
  get id(): string | null;
  set id(value: string | null);
  get file(): string | null;
  set file(value: string | null);
  get type(): 'js' | 'css' | 'asset';
  get info(): ModuleInfo$1 | undefined;
  get meta(): Record<string, any> | undefined;
  get importers(): Set<ModuleNode>;
  get clientImportedModules(): Set<ModuleNode>;
  get ssrImportedModules(): Set<ModuleNode>;
  get importedModules(): Set<ModuleNode>;
  get acceptedHmrDeps(): Set<ModuleNode>;
  get acceptedHmrExports(): Set<string> | null;
  get importedBindings(): Map<string, Set<string>> | null;
  get isSelfAccepting(): boolean | undefined;
  get transformResult(): TransformResult | null;
  set transformResult(value: TransformResult | null);
  get ssrTransformResult(): TransformResult | null;
  set ssrTransformResult(value: TransformResult | null);
  get ssrModule(): Record<string, any> | null;
  get ssrError(): Error | null;
  get lastHMRTimestamp(): number;
  set lastHMRTimestamp(value: number);
  get lastInvalidationTimestamp(): number;
  get invalidationState(): TransformResult | 'HARD_INVALIDATED' | undefined;
  get ssrInvalidationState(): TransformResult | 'HARD_INVALIDATED' | undefined;
}
declare class ModuleGraph {
  urlToModuleMap: Map<string, ModuleNode>;
  idToModuleMap: Map<string, ModuleNode>;
  etagToModuleMap: Map<string, ModuleNode>;
  fileToModulesMap: Map<string, Set<ModuleNode>>;
  private moduleNodeCache;
  constructor(moduleGraphs: {
    client: () => EnvironmentModuleGraph;
    ssr: () => EnvironmentModuleGraph;
  });
  getModuleById(id: string): ModuleNode | undefined;
  getModuleByUrl(url: string, _ssr?: boolean): Promise<ModuleNode | undefined>;
  getModulesByFile(file: string): Set<ModuleNode> | undefined;
  onFileChange(file: string): void;
  onFileDelete(file: string): void;
  invalidateModule(mod: ModuleNode, seen?: Set<ModuleNode>, timestamp?: number, isHmr?: boolean): void;
  invalidateAll(): void;
  ensureEntryFromUrl(rawUrl: string, ssr?: boolean, setIsSelfAccepting?: boolean): Promise<ModuleNode>;
  createFileOnlyEntry(file: string): ModuleNode;
  resolveUrl(url: string, ssr?: boolean): Promise<ResolvedUrl>;
  updateModuleTransformResult(mod: ModuleNode, result: TransformResult | null, ssr?: boolean): void;
  getModuleByEtag(etag: string): ModuleNode | undefined;
  getBackwardCompatibleBrowserModuleNode(clientModule: EnvironmentModuleNode): ModuleNode;
  getBackwardCompatibleServerModuleNode(ssrModule: EnvironmentModuleNode): ModuleNode;
  getBackwardCompatibleModuleNode(mod: EnvironmentModuleNode): ModuleNode;
  getBackwardCompatibleModuleNodeDual(clientModule?: EnvironmentModuleNode, ssrModule?: EnvironmentModuleNode): ModuleNode;
}
type ModuleSetNames = 'acceptedHmrDeps' | 'importedModules'; //#endregion
//#region src/node/server/hmr.d.ts
interface HmrOptions {
  protocol?: string;
  host?: string;
  port?: number;
  clientPort?: number;
  path?: string;
  timeout?: number;
  overlay?: boolean;
  server?: HttpServer;
}
interface HotUpdateOptions {
  type: 'create' | 'update' | 'delete';
  file: string;
  timestamp: number;
  modules: Array<EnvironmentModuleNode>;
  read: () => string | Promise<string>;
  server: ViteDevServer;
}
interface HmrContext {
  file: string;
  timestamp: number;
  modules: Array<ModuleNode>;
  read: () => string | Promise<string>;
  server: ViteDevServer;
}
interface HotChannelClient {
  send(payload: HotPayload): void;
}
type HotChannelListener<T extends string = string> = (data: InferCustomEventPayload<T>, client: HotChannelClient) => void;
interface HotChannel<Api = any> {
  /**
   * Broadcast events to all clients
   */
  send?(payload: HotPayload): void;
  /**
   * Handle custom event emitted by `import.meta.hot.send`
   */
  on?<T extends string>(event: T, listener: HotChannelListener<T>): void;
  on?(event: 'connection', listener: () => void): void;
  /**
   * Unregister event listener
   */
  off?(event: string, listener: Function): void;
  /**
   * Start listening for messages
   */
  listen?(): void;
  /**
   * Disconnect all clients, called when server is closed or restarted.
   */
  close?(): Promise<unknown> | void;
  api?: Api;
}
interface NormalizedHotChannelClient {
  /**
   * Send event to the client
   */
  send(payload: HotPayload): void;
  /**
   * Send custom event
   */
  send(event: string, payload?: CustomPayload['data']): void;
}
interface NormalizedHotChannel<Api = any> {
  /**
   * Broadcast events to all clients
   */
  send(payload: HotPayload): void;
  /**
   * Send custom event
   */
  send<T extends string>(event: T, payload?: InferCustomEventPayload<T>): void;
  /**
   * Handle custom event emitted by `import.meta.hot.send`
   */
  on<T extends string>(event: T, listener: (data: InferCustomEventPayload<T>, client: NormalizedHotChannelClient) => void): void;
  on(event: 'connection', listener: () => void): void;
  /**
   * Unregister event listener
   */
  off(event: string, listener: Function): void;
  handleInvoke(payload: HotPayload): Promise<{
    result: any;
  } | {
    error: any;
  }>;
  /**
   * Start listening for messages
   */
  listen(): void;
  /**
   * Disconnect all clients, called when server is closed or restarted.
   */
  close(): Promise<unknown> | void;
  api?: Api;
}
//#endregion
//#region src/types/ws.d.ts
// WebSocket socket.
declare class WebSocket$1 extends EventEmitter {
  /** The connection is not yet open. */
  static readonly CONNECTING: 0;
  /** The connection is open and ready to communicate. */
  static readonly OPEN: 1;
  /** The connection is in the process of closing. */
  static readonly CLOSING: 2;
  /** The connection is closed. */
  static readonly CLOSED: 3;
  binaryType: 'nodebuffer' | 'arraybuffer' | 'fragments';
  readonly bufferedAmount: number;
  readonly extensions: string;
  /** Indicates whether the websocket is paused */
  readonly isPaused: boolean;
  readonly protocol: string;
  /** The current state of the connection */
  readonly readyState: typeof WebSocket$1.CONNECTING | typeof WebSocket$1.OPEN | typeof WebSocket$1.CLOSING | typeof WebSocket$1.CLOSED;
  readonly url: string;
  /** The connection is not yet open. */
  readonly CONNECTING: 0;
  /** The connection is open and ready to communicate. */
  readonly OPEN: 1;
  /** The connection is in the process of closing. */
  readonly CLOSING: 2;
  /** The connection is closed. */
  readonly CLOSED: 3;
  onopen: ((event: WebSocket$1.Event) => void) | null;
  onerror: ((event: WebSocket$1.ErrorEvent) => void) | null;
  onclose: ((event: WebSocket$1.CloseEvent) => void) | null;
  onmessage: ((event: WebSocket$1.MessageEvent) => void) | null;
  constructor(address: null);
  constructor(address: string | URL$1, options?: WebSocket$1.ClientOptions | ClientRequestArgs);
  constructor(address: string | URL$1, protocols?: string | string[], options?: WebSocket$1.ClientOptions | ClientRequestArgs);
  close(code?: number, data?: string | Buffer): void;
  ping(data?: any, mask?: boolean, cb?: (err: Error) => void): void;
  pong(data?: any, mask?: boolean, cb?: (err: Error) => void): void;
  send(data: any, cb?: (err?: Error) => void): void;
  send(data: any, options: {
    mask?: boolean | undefined;
    binary?: boolean | undefined;
    compress?: boolean | undefined;
    fin?: boolean | undefined;
  }, cb?: (err?: Error) => void): void;
  terminate(): void;
  /**
   * Pause the websocket causing it to stop emitting events. Some events can still be
   * emitted after this is called, until all buffered data is consumed. This method
   * is a noop if the ready state is `CONNECTING` or `CLOSED`.
   */
  pause(): void;
  /**
   * Make a paused socket resume emitting events. This method is a noop if the ready
   * state is `CONNECTING` or `CLOSED`.
   */
  resume(): void; // HTML5 WebSocket events
  addEventListener(method: 'message', cb: (event: WebSocket$1.MessageEvent) => void, options?: WebSocket$1.EventListenerOptions): void;
  addEventListener(method: 'close', cb: (event: WebSocket$1.CloseEvent) => void, options?: WebSocket$1.EventListenerOptions): void;
  addEventListener(method: 'error', cb: (event: WebSocket$1.ErrorEvent) => void, options?: WebSocket$1.EventListenerOptions): void;
  addEventListener(method: 'open', cb: (event: WebSocket$1.Event) => void, options?: WebSocket$1.EventListenerOptions): void;
  removeEventListener(method: 'message', cb: (event: WebSocket$1.MessageEvent) => void): void;
  removeEventListener(method: 'close', cb: (event: WebSocket$1.CloseEvent) => void): void;
  removeEventListener(method: 'error', cb: (event: WebSocket$1.ErrorEvent) => void): void;
  removeEventListener(method: 'open', cb: (event: WebSocket$1.Event) => void): void; // Events
  on(event: 'close', listener: (this: WebSocket$1, code: number, reason: Buffer) => void): this;
  on(event: 'error', listener: (this: WebSocket$1, err: Error) => void): this;
  on(event: 'upgrade', listener: (this: WebSocket$1, request: http.IncomingMessage) => void): this;
  on(event: 'message', listener: (this: WebSocket$1, data: WebSocket$1.RawData, isBinary: boolean) => void): this;
  on(event: 'open', listener: (this: WebSocket$1) => void): this;
  on(event: 'ping' | 'pong', listener: (this: WebSocket$1, data: Buffer) => void): this;
  on(event: 'unexpected-response', listener: (this: WebSocket$1, request: ClientRequest, response: http.IncomingMessage) => void): this;
  on(event: string | symbol, listener: (this: WebSocket$1, ...args: any[]) => void): this;
  once(event: 'close', listener: (this: WebSocket$1, code: number, reason: Buffer) => void): this;
  once(event: 'error', listener: (this: WebSocket$1, err: Error) => void): this;
  once(event: 'upgrade', listener: (this: WebSocket$1, request: http.IncomingMessage) => void): this;
  once(event: 'message', listener: (this: WebSocket$1, data: WebSocket$1.RawData, isBinary: boolean) => void): this;
  once(event: 'open', listener: (this: WebSocket$1) => void): this;
  once(event: 'ping' | 'pong', listener: (this: WebSocket$1, data: Buffer) => void): this;
  once(event: 'unexpected-response', listener: (this: WebSocket$1, request: ClientRequest, response: http.IncomingMessage) => void): this;
  once(event: string | symbol, listener: (this: WebSocket$1, ...args: any[]) => void): this;
  off(event: 'close', listener: (this: WebSocket$1, code: number, reason: Buffer) => void): this;
  off(event: 'error', listener: (this: WebSocket$1, err: Error) => void): this;
  off(event: 'upgrade', listener: (this: WebSocket$1, request: http.IncomingMessage) => void): this;
  off(event: 'message', listener: (this: WebSocket$1, data: WebSocket$1.RawData, isBinary: boolean) => void): this;
  off(event: 'open', listener: (this: WebSocket$1) => void): this;
  off(event: 'ping' | 'pong', listener: (this: WebSocket$1, data: Buffer) => void): this;
  off(event: 'unexpected-response', listener: (this: WebSocket$1, request: ClientRequest, response: http.IncomingMessage) => void): this;
  off(event: string | symbol, listener: (this: WebSocket$1, ...args: any[]) => void): this;
  addListener(event: 'close', listener: (code: number, reason: Buffer) => void): this;
  addListener(event: 'error', listener: (err: Error) => void): this;
  addListener(event: 'upgrade', listener: (request: http.IncomingMessage) => void): this;
  addListener(event: 'message', listener: (data: WebSocket$1.RawData, isBinary: boolean) => void): this;
  addListener(event: 'open', listener: () => void): this;
  addListener(event: 'ping' | 'pong', listener: (data: Buffer) => void): this;
  addListener(event: 'unexpected-response', listener: (request: ClientRequest, response: http.IncomingMessage) => void): this;
  addListener(event: string | symbol, listener: (...args: any[]) => void): this;
  removeListener(event: 'close', listener: (code: number, reason: Buffer) => void): this;
  removeListener(event: 'error', listener: (err: Error) => void): this;
  removeListener(event: 'upgrade', listener: (request: http.IncomingMessage) => void): this;
  removeListener(event: 'message', listener: (data: WebSocket$1.RawData, isBinary: boolean) => void): this;
  removeListener(event: 'open', listener: () => void): this;
  removeListener(event: 'ping' | 'pong', listener: (data: Buffer) => void): this;
  removeListener(event: 'unexpected-response', listener: (request: ClientRequest, response: http.IncomingMessage) => void): this;
  removeListener(event: string | symbol, listener: (...args: any[]) => void): this;
}
declare const WebSocketAlias: typeof WebSocket$1;
interface WebSocketAlias extends WebSocket$1 {}
declare namespace WebSocket$1 {
  /**
   * Data represents the raw message payload received over the WebSocket.
   */
  type RawData = Buffer | ArrayBuffer | Buffer[];
  /**
   * Data represents the message payload received over the WebSocket.
   */
  type Data = string | Buffer | ArrayBuffer | Buffer[];
  /**
   * CertMeta represents the accepted types for certificate & key data.
   */
  type CertMeta = string | string[] | Buffer | Buffer[];
  /**
   * VerifyClientCallbackSync is a synchronous callback used to inspect the
   * incoming message. The return value (boolean) of the function determines
   * whether or not to accept the handshake.
   */
  type VerifyClientCallbackSync = (info: {
    origin: string;
    secure: boolean;
    req: http.IncomingMessage;
  }) => boolean;
  /**
   * VerifyClientCallbackAsync is an asynchronous callback used to inspect the
   * incoming message. The return value (boolean) of the function determines
   * whether or not to accept the handshake.
   */
  type VerifyClientCallbackAsync = (info: {
    origin: string;
    secure: boolean;
    req: http.IncomingMessage;
  }, callback: (res: boolean, code?: number, message?: string, headers?: OutgoingHttpHeaders) => void) => void;
  interface ClientOptions extends SecureContextOptions {
    protocol?: string | undefined;
    followRedirects?: boolean | undefined;
    generateMask?(mask: Buffer): void;
    handshakeTimeout?: number | undefined;
    maxRedirects?: number | undefined;
    perMessageDeflate?: boolean | PerMessageDeflateOptions | undefined;
    localAddress?: string | undefined;
    protocolVersion?: number | undefined;
    headers?: {
      [key: string]: string;
    } | undefined;
    origin?: string | undefined;
    agent?: Agent | undefined;
    host?: string | undefined;
    family?: number | undefined;
    checkServerIdentity?(servername: string, cert: CertMeta): boolean;
    rejectUnauthorized?: boolean | undefined;
    maxPayload?: number | undefined;
    skipUTF8Validation?: boolean | undefined;
  }
  interface PerMessageDeflateOptions {
    serverNoContextTakeover?: boolean | undefined;
    clientNoContextTakeover?: boolean | undefined;
    serverMaxWindowBits?: number | undefined;
    clientMaxWindowBits?: number | undefined;
    zlibDeflateOptions?: {
      flush?: number | undefined;
      finishFlush?: number | undefined;
      chunkSize?: number | undefined;
      windowBits?: number | undefined;
      level?: number | undefined;
      memLevel?: number | undefined;
      strategy?: number | undefined;
      dictionary?: Buffer | Buffer[] | DataView | undefined;
      info?: boolean | undefined;
    } | undefined;
    zlibInflateOptions?: ZlibOptions | undefined;
    threshold?: number | undefined;
    concurrencyLimit?: number | undefined;
  }
  interface Event {
    type: string;
    target: WebSocket$1;
  }
  interface ErrorEvent {
    error: any;
    message: string;
    type: string;
    target: WebSocket$1;
  }
  interface CloseEvent {
    wasClean: boolean;
    code: number;
    reason: string;
    type: string;
    target: WebSocket$1;
  }
  interface MessageEvent {
    data: Data;
    type: string;
    target: WebSocket$1;
  }
  interface EventListenerOptions {
    once?: boolean | undefined;
  }
  interface ServerOptions {
    host?: string | undefined;
    port?: number | undefined;
    backlog?: number | undefined;
    server?: http.Server | Server$1 | undefined;
    verifyClient?: VerifyClientCallbackAsync | VerifyClientCallbackSync | undefined;
    handleProtocols?: (protocols: Set<string>, request: http.IncomingMessage) => string | false;
    path?: string | undefined;
    noServer?: boolean | undefined;
    clientTracking?: boolean | undefined;
    perMessageDeflate?: boolean | PerMessageDeflateOptions | undefined;
    maxPayload?: number | undefined;
    skipUTF8Validation?: boolean | undefined;
    WebSocket?: typeof WebSocket$1.WebSocket | undefined;
  }
  interface AddressInfo {
    address: string;
    family: string;
    port: number;
  } // WebSocket Server
  class Server<T extends WebSocket$1 = WebSocket$1> extends EventEmitter {
    options: ServerOptions;
    path: string;
    clients: Set<T>;
    constructor(options?: ServerOptions, callback?: () => void);
    address(): AddressInfo | string;
    close(cb?: (err?: Error) => void): void;
    handleUpgrade(request: http.IncomingMessage, socket: Duplex, upgradeHead: Buffer, callback: (client: T, request: http.IncomingMessage) => void): void;
    shouldHandle(request: http.IncomingMessage): boolean | Promise<boolean>; // Events
    on(event: 'connection', cb: (this: Server<T>, socket: T, request: http.IncomingMessage) => void): this;
    on(event: 'error', cb: (this: Server<T>, error: Error) => void): this;
    on(event: 'headers', cb: (this: Server<T>, headers: string[], request: http.IncomingMessage) => void): this;
    on(event: 'close' | 'listening', cb: (this: Server<T>) => void): this;
    on(event: string | symbol, listener: (this: Server<T>, ...args: any[]) => void): this;
    once(event: 'connection', cb: (this: Server<T>, socket: T, request: http.IncomingMessage) => void): this;
    once(event: 'error', cb: (this: Server<T>, error: Error) => void): this;
    once(event: 'headers', cb: (this: Server<T>, headers: string[], request: http.IncomingMessage) => void): this;
    once(event: 'close' | 'listening', cb: (this: Server<T>) => void): this;
    once(event: string | symbol, listener: (this: Server<T>, ...args: any[]) => void): this;
    off(event: 'connection', cb: (this: Server<T>, socket: T, request: http.IncomingMessage) => void): this;
    off(event: 'error', cb: (this: Server<T>, error: Error) => void): this;
    off(event: 'headers', cb: (this: Server<T>, headers: string[], request: http.IncomingMessage) => void): this;
    off(event: 'close' | 'listening', cb: (this: Server<T>) => void): this;
    off(event: string | symbol, listener: (this: Server<T>, ...args: any[]) => void): this;
    addListener(event: 'connection', cb: (client: T, request: http.IncomingMessage) => void): this;
    addListener(event: 'error', cb: (err: Error) => void): this;
    addListener(event: 'headers', cb: (headers: string[], request: http.IncomingMessage) => void): this;
    addListener(event: 'close' | 'listening', cb: () => void): this;
    addListener(event: string | symbol, listener: (...args: any[]) => void): this;
    removeListener(event: 'connection', cb: (client: T) => void): this;
    removeListener(event: 'error', cb: (err: Error) => void): this;
    removeListener(event: 'headers', cb: (headers: string[], request: http.IncomingMessage) => void): this;
    removeListener(event: 'close' | 'listening', cb: () => void): this;
    removeListener(event: string | symbol, listener: (...args: any[]) => void): this;
  }
  const WebSocketServer: typeof Server;
  interface WebSocketServer extends Server {}
  const WebSocket: typeof WebSocketAlias;
  interface WebSocket extends WebSocketAlias {} // WebSocket stream
  function createWebSocketStream(websocket: WebSocket$1, options?: DuplexOptions): Duplex;
} // export = WebSocket
//#endregion
//#region src/node/server/ws.d.ts
type WebSocketCustomListener<T> = (data: T, client: WebSocketClient, invoke?: 'send' | `send:${string}`) => void;
declare const isWebSocketServer: unique symbol;
interface WebSocketServer extends NormalizedHotChannel {
  /**
   * Handle custom event emitted by `import.meta.hot.send`
   */
  on: WebSocket$1.Server['on'] & {
    <T extends string>(event: T, listener: WebSocketCustomListener<InferCustomEventPayload<T>>): void;
  };
  /**
   * Unregister event listener.
   */
  off: WebSocket$1.Server['off'] & {
    (event: string, listener: Function): void;
  };
  /**
   * Listen on port and host
   */
  listen(): void;
  /**
   * Disconnect all clients and terminate the server.
   */
  close(): Promise<void>;
  [isWebSocketServer]: true;
  /**
   * Get all connected clients.
   */
  clients: Set<WebSocketClient>;
}
interface WebSocketClient extends NormalizedHotChannelClient {
  /**
   * The raw WebSocket instance
   * @advanced
   */
  socket: WebSocket$1;
} //#endregion
//#region src/node/server/environment.d.ts
interface DevEnvironmentContext {
  hot: boolean;
  transport?: HotChannel | WebSocketServer;
  options?: EnvironmentOptions;
  remoteRunner?: {
    inlineSourceMap?: boolean;
  };
  depsOptimizer?: DepsOptimizer;
}
declare class DevEnvironment extends BaseEnvironment {
  mode: "dev";
  moduleGraph: EnvironmentModuleGraph;
  depsOptimizer?: DepsOptimizer;
  get pluginContainer(): EnvironmentPluginContainer<DevEnvironment>;
  /**
   * Hot channel for this environment. If not provided or disabled,
   * it will be a noop channel that does nothing.
   *
   * @example
   * environment.hot.send({ type: 'full-reload' })
   */
  hot: NormalizedHotChannel;
  constructor(name: string, config: ResolvedConfig, context: DevEnvironmentContext);
  init(options?: {
    watcher?: FSWatcher;
    /**
     * the previous instance used for the environment with the same name
     *
     * when using, the consumer should check if it's an instance generated from the same class or factory function
     */
    previousInstance?: DevEnvironment;
  }): Promise<void>;
  /**
   * When the dev server is restarted, the methods are called in the following order:
   * - new instance `init`
   * - previous instance `close`
   * - new instance `listen`
   */
  listen(server: ViteDevServer): Promise<void>;
  fetchModule(id: string, importer?: string, options?: FetchFunctionOptions): Promise<FetchResult>;
  reloadModule(module: EnvironmentModuleNode): Promise<void>;
  transformRequest(url: string): Promise<TransformResult | null>;
  warmupRequest(url: string): Promise<void>;
  close(): Promise<void>;
  /**
   * Calling `await environment.waitForRequestsIdle(id)` will wait until all static imports
   * are processed after the first transformRequest call. If called from a load or transform
   * plugin hook, the id needs to be passed as a parameter to avoid deadlocks.
   * Calling this function after the first static imports section of the module graph has been
   * processed will resolve immediately.
   * @experimental
   */
  waitForRequestsIdle(ignoredId?: string): Promise<void>;
} //#endregion
//#region src/types/commonjs.d.ts
interface RollupCommonJSOptions {
  /**
   * A minimatch pattern, or array of patterns, which specifies the files in
   * the build the plugin should operate on. By default, all files with
   * extension `".cjs"` or those in `extensions` are included, but you can
   * narrow this list by only including specific files. These files will be
   * analyzed and transpiled if either the analysis does not find ES module
   * specific statements or `transformMixedEsModules` is `true`.
   * @default undefined
   */
  include?: string | RegExp | readonly (string | RegExp)[];
  /**
   * A minimatch pattern, or array of patterns, which specifies the files in
   * the build the plugin should _ignore_. By default, all files with
   * extensions other than those in `extensions` or `".cjs"` are ignored, but you
   * can exclude additional files. See also the `include` option.
   * @default undefined
   */
  exclude?: string | RegExp | readonly (string | RegExp)[];
  /**
   * For extensionless imports, search for extensions other than .js in the
   * order specified. Note that you need to make sure that non-JavaScript files
   * are transpiled by another plugin first.
   * @default [ '.js' ]
   */
  extensions?: ReadonlyArray<string>;
  /**
   * If true then uses of `global` won't be dealt with by this plugin
   * @default false
   */
  ignoreGlobal?: boolean;
  /**
   * If false, skips source map generation for CommonJS modules. This will
   * improve performance.
   * @default true
   */
  sourceMap?: boolean;
  /**
   * Some `require` calls cannot be resolved statically to be translated to
   * imports.
   * When this option is set to `false`, the generated code will either
   * directly throw an error when such a call is encountered or, when
   * `dynamicRequireTargets` is used, when such a call cannot be resolved with a
   * configured dynamic require target.
   * Setting this option to `true` will instead leave the `require` call in the
   * code or use it as a fallback for `dynamicRequireTargets`.
   * @default false
   */
  ignoreDynamicRequires?: boolean;
  /**
   * Instructs the plugin whether to enable mixed module transformations. This
   * is useful in scenarios with modules that contain a mix of ES `import`
   * statements and CommonJS `require` expressions. Set to `true` if `require`
   * calls should be transformed to imports in mixed modules, or `false` if the
   * `require` expressions should survive the transformation. The latter can be
   * important if the code contains environment detection, or you are coding
   * for an environment with special treatment for `require` calls such as
   * ElectronJS. See also the `ignore` option.
   * @default false
   */
  transformMixedEsModules?: boolean;
  /**
   * By default, this plugin will try to hoist `require` statements as imports
   * to the top of each file. While this works well for many code bases and
   * allows for very efficient ESM output, it does not perfectly capture
   * CommonJS semantics as the order of side effects like log statements may
   * change. But it is especially problematic when there are circular `require`
   * calls between CommonJS modules as those often rely on the lazy execution of
   * nested `require` calls.
   *
   * Setting this option to `true` will wrap all CommonJS files in functions
   * which are executed when they are required for the first time, preserving
   * NodeJS semantics. Note that this can have an impact on the size and
   * performance of the generated code.
   *
   * The default value of `"auto"` will only wrap CommonJS files when they are
   * part of a CommonJS dependency cycle, e.g. an index file that is required by
   * many of its dependencies. All other CommonJS files are hoisted. This is the
   * recommended setting for most code bases.
   *
   * `false` will entirely prevent wrapping and hoist all files. This may still
   * work depending on the nature of cyclic dependencies but will often cause
   * problems.
   *
   * You can also provide a minimatch pattern, or array of patterns, to only
   * specify a subset of files which should be wrapped in functions for proper
   * `require` semantics.
   *
   * `"debug"` works like `"auto"` but after bundling, it will display a warning
   * containing a list of ids that have been wrapped which can be used as
   * minimatch pattern for fine-tuning.
   * @default "auto"
   */
  strictRequires?: boolean | string | RegExp | readonly (string | RegExp)[];
  /**
   * Sometimes you have to leave require statements unconverted. Pass an array
   * containing the IDs or a `id => boolean` function.
   * @default []
   */
  ignore?: ReadonlyArray<string> | ((id: string) => boolean);
  /**
   * In most cases, where `require` calls are inside a `try-catch` clause,
   * they should be left unconverted as it requires an optional dependency
   * that may or may not be installed beside the rolled up package.
   * Due to the conversion of `require` to a static `import` - the call is
   * hoisted to the top of the file, outside the `try-catch` clause.
   *
   * - `true`: Default. All `require` calls inside a `try` will be left unconverted.
   * - `false`: All `require` calls inside a `try` will be converted as if the
   *   `try-catch` clause is not there.
   * - `remove`: Remove all `require` calls from inside any `try` block.
   * - `string[]`: Pass an array containing the IDs to left unconverted.
   * - `((id: string) => boolean|'remove')`: Pass a function that controls
   *   individual IDs.
   *
   * @default true
   */
  ignoreTryCatch?: boolean | 'remove' | ReadonlyArray<string> | ((id: string) => boolean | 'remove');
  /**
   * Controls how to render imports from external dependencies. By default,
   * this plugin assumes that all external dependencies are CommonJS. This
   * means they are rendered as default imports to be compatible with e.g.
   * NodeJS where ES modules can only import a default export from a CommonJS
   * dependency.
   *
   * If you set `esmExternals` to `true`, this plugin assumes that all
   * external dependencies are ES modules and respect the
   * `requireReturnsDefault` option. If that option is not set, they will be
   * rendered as namespace imports.
   *
   * You can also supply an array of ids to be treated as ES modules, or a
   * function that will be passed each external id to determine whether it is
   * an ES module.
   * @default false
   */
  esmExternals?: boolean | ReadonlyArray<string> | ((id: string) => boolean);
  /**
   * Controls what is returned when requiring an ES module from a CommonJS file.
   * When using the `esmExternals` option, this will also apply to external
   * modules. By default, this plugin will render those imports as namespace
   * imports i.e.
   *
   * ```js
   * // input
   * const foo = require('foo');
   *
   * // output
   * import * as foo from 'foo';
   * ```
   *
   * However, there are some situations where this may not be desired.
   * For these situations, you can change Rollup's behaviour either globally or
   * per module. To change it globally, set the `requireReturnsDefault` option
   * to one of the following values:
   *
   * - `false`: This is the default, requiring an ES module returns its
   *   namespace. This is the only option that will also add a marker
   *   `__esModule: true` to the namespace to support interop patterns in
   *   CommonJS modules that are transpiled ES modules.
   * - `"namespace"`: Like `false`, requiring an ES module returns its
   *   namespace, but the plugin does not add the `__esModule` marker and thus
   *   creates more efficient code. For external dependencies when using
   *   `esmExternals: true`, no additional interop code is generated.
   * - `"auto"`: This is complementary to how `output.exports: "auto"` works in
   *   Rollup: If a module has a default export and no named exports, requiring
   *   that module returns the default export. In all other cases, the namespace
   *   is returned. For external dependencies when using `esmExternals: true`, a
   *   corresponding interop helper is added.
   * - `"preferred"`: If a module has a default export, requiring that module
   *   always returns the default export, no matter whether additional named
   *   exports exist. This is similar to how previous versions of this plugin
   *   worked. Again for external dependencies when using `esmExternals: true`,
   *   an interop helper is added.
   * - `true`: This will always try to return the default export on require
   *   without checking if it actually exists. This can throw at build time if
   *   there is no default export. This is how external dependencies are handled
   *   when `esmExternals` is not used. The advantage over the other options is
   *   that, like `false`, this does not add an interop helper for external
   *   dependencies, keeping the code lean.
   *
   * To change this for individual modules, you can supply a function for
   * `requireReturnsDefault` instead. This function will then be called once for
   * each required ES module or external dependency with the corresponding id
   * and allows you to return different values for different modules.
   * @default false
   */
  requireReturnsDefault?: boolean | 'auto' | 'preferred' | 'namespace' | ((id: string) => boolean | 'auto' | 'preferred' | 'namespace');
  /**
   * @default "auto"
   */
  defaultIsModuleExports?: boolean | 'auto' | ((id: string) => boolean | 'auto');
  /**
   * Some modules contain dynamic `require` calls, or require modules that
   * contain circular dependencies, which are not handled well by static
   * imports. Including those modules as `dynamicRequireTargets` will simulate a
   * CommonJS (NodeJS-like) environment for them with support for dynamic
   * dependencies. It also enables `strictRequires` for those modules.
   *
   * Note: In extreme cases, this feature may result in some paths being
   * rendered as absolute in the final bundle. The plugin tries to avoid
   * exposing paths from the local machine, but if you are `dynamicRequirePaths`
   * with paths that are far away from your project's folder, that may require
   * replacing strings like `"/Users/John/Desktop/foo-project/"` -\> `"/"`.
   */
  dynamicRequireTargets?: string | ReadonlyArray<string>;
  /**
   * To avoid long paths when using the `dynamicRequireTargets` option, you can use this option to specify a directory
   * that is a common parent for all files that use dynamic require statements. Using a directory higher up such as `/`
   * may lead to unnecessarily long paths in the generated code and may expose directory names on your machine like your
   * home directory name. By default, it uses the current working directory.
   */
  dynamicRequireRoot?: string;
} //#endregion
//#region src/types/dynamicImportVars.d.ts
interface RollupDynamicImportVarsOptions {
  /**
   * Files to include in this plugin (default all).
   * @default []
   */
  include?: string | RegExp | (string | RegExp)[];
  /**
   * Files to exclude in this plugin (default none).
   * @default []
   */
  exclude?: string | RegExp | (string | RegExp)[];
  /**
   * By default, the plugin quits the build process when it encounters an error. If you set this option to true, it will throw a warning instead and leave the code untouched.
   * @default false
   */
  warnOnError?: boolean;
} //#endregion
//#region src/node/plugins/terser.d.ts
interface TerserOptions extends TerserMinifyOptions {
  /**
   * Vite-specific option to specify the max number of workers to spawn
   * when minifying files with terser.
   *
   * @default number of CPUs minus 1
   */
  maxWorkers?: number;
} //#endregion
//#region src/node/plugins/resolve.d.ts
interface EnvironmentResolveOptions {
  /**
   * @default ['browser', 'module', 'jsnext:main', 'jsnext']
   */
  mainFields?: string[];
  conditions?: string[];
  externalConditions?: string[];
  /**
   * @default ['.mjs', '.js', '.mts', '.ts', '.jsx', '.tsx', '.json']
   */
  extensions?: string[];
  dedupe?: string[];
  /**
   * Prevent listed dependencies from being externalized and will get bundled in build.
   * Only works in server environments for now. Previously this was `ssr.noExternal`.
   * @experimental
   */
  noExternal?: string | RegExp | (string | RegExp)[] | true;
  /**
   * Externalize the given dependencies and their transitive dependencies.
   * Only works in server environments for now. Previously this was `ssr.external`.
   * @experimental
   */
  external?: string[] | true;
  /**
   * Array of strings or regular expressions that indicate what modules are builtin for the environment.
   */
  builtins?: (string | RegExp)[];
}
interface ResolveOptions extends EnvironmentResolveOptions {
  /**
   * @default false
   */
  preserveSymlinks?: boolean;
}
interface ResolvePluginOptions {
  root: string;
  isBuild: boolean;
  isProduction: boolean;
  packageCache?: PackageCache;
  /**
   * src code mode also attempts the following:
   * - resolving /xxx as URLs
   * - resolving bare imports from optimized deps
   */
  asSrc?: boolean;
  tryIndex?: boolean;
  tryPrefix?: string;
  preferRelative?: boolean;
  isRequire?: boolean;
  scan?: boolean;
}
interface InternalResolveOptions extends Required<ResolveOptions>, ResolvePluginOptions {} //#endregion
//#region src/node/packages.d.ts
/** Cache for package.json resolution and package.json contents */
type PackageCache = Map<string, PackageData>;
interface PackageData {
  dir: string;
  hasSideEffects: (id: string) => boolean | 'no-treeshake' | null;
  setResolvedCache: (key: string, entry: string, options: InternalResolveOptions) => void;
  getResolvedCache: (key: string, options: InternalResolveOptions) => string | undefined;
  data: {
    [field: string]: any;
    name: string;
    type: string;
    version: string;
    main: string;
    module: string;
    browser: string | Record<string, string | false>;
    exports: string | Record<string, any> | string[];
    imports: Record<string, any>;
    dependencies: Record<string, string>;
  };
} //#endregion
//#region src/node/build.d.ts
interface BuildEnvironmentOptions {
  /**
   * Compatibility transform target. The transform is performed with esbuild
   * and the lowest supported target is es2015. Note this only handles
   * syntax transformation and does not cover polyfills
   *
   * Default: 'baseline-widely-available' - transpile targeting browsers that
   * are included in the Baseline Widely Available on 2025-05-01.
   * (Chrome 107+, Edge 107+, Firefox 104+, Safari 16+).
   *
   * Another special value is 'esnext' - which only performs minimal transpiling
   * (for minification compat).
   *
   * For custom targets, see https://esbuild.github.io/api/#target and
   * https://esbuild.github.io/content-types/#javascript for more details.
   * @default 'baseline-widely-available'
   */
  target?: 'baseline-widely-available' | TransformOptions$1['target'] | false;
  /**
   * whether to inject module preload polyfill.
   * Note: does not apply to library mode.
   * @default true
   * @deprecated use `modulePreload.polyfill` instead
   */
  polyfillModulePreload?: boolean;
  /**
   * Configure module preload
   * Note: does not apply to library mode.
   * @default true
   */
  modulePreload?: boolean | ModulePreloadOptions;
  /**
   * Directory relative from `root` where build output will be placed. If the
   * directory exists, it will be removed before the build.
   * @default 'dist'
   */
  outDir?: string;
  /**
   * Directory relative from `outDir` where the built js/css/image assets will
   * be placed.
   * @default 'assets'
   */
  assetsDir?: string;
  /**
   * Static asset files smaller than this number (in bytes) will be inlined as
   * base64 strings. If a callback is passed, a boolean can be returned to opt-in
   * or opt-out of inlining. If nothing is returned the default logic applies.
   *
   * Default limit is `4096` (4 KiB). Set to `0` to disable.
   * @default 4096
   */
  assetsInlineLimit?: number | ((filePath: string, content: Buffer) => boolean | undefined);
  /**
   * Whether to code-split CSS. When enabled, CSS in async chunks will be
   * inlined as strings in the chunk and inserted via dynamically created
   * style tags when the chunk is loaded.
   * @default true
   */
  cssCodeSplit?: boolean;
  /**
   * An optional separate target for CSS minification.
   * As esbuild only supports configuring targets to mainstream
   * browsers, users may need this option when they are targeting
   * a niche browser that comes with most modern JavaScript features
   * but has poor CSS support, e.g. Android WeChat WebView, which
   * doesn't support the #RGBA syntax.
   * @default target
   */
  cssTarget?: TransformOptions$1['target'] | false;
  /**
   * Override CSS minification specifically instead of defaulting to `build.minify`,
   * so you can configure minification for JS and CSS separately.
   * @default 'esbuild'
   */
  cssMinify?: boolean | 'esbuild' | 'lightningcss';
  /**
   * If `true`, a separate sourcemap file will be created. If 'inline', the
   * sourcemap will be appended to the resulting output file as data URI.
   * 'hidden' works like `true` except that the corresponding sourcemap
   * comments in the bundled files are suppressed.
   * @default false
   */
  sourcemap?: boolean | 'inline' | 'hidden';
  /**
   * Set to `false` to disable minification, or specify the minifier to use.
   * Available options are 'terser' or 'esbuild'.
   * @default 'esbuild'
   */
  minify?: boolean | 'terser' | 'esbuild';
  /**
   * Options for terser
   * https://terser.org/docs/api-reference#minify-options
   *
   * In addition, you can also pass a `maxWorkers: number` option to specify the
   * max number of workers to spawn. Defaults to the number of CPUs minus 1.
   */
  terserOptions?: TerserOptions;
  /**
   * Will be merged with internal rollup options.
   * https://rollupjs.org/configuration-options/
   */
  rollupOptions?: RollupOptions;
  /**
   * Options to pass on to `@rollup/plugin-commonjs`
   */
  commonjsOptions?: RollupCommonJSOptions;
  /**
   * Options to pass on to `@rollup/plugin-dynamic-import-vars`
   */
  dynamicImportVarsOptions?: RollupDynamicImportVarsOptions;
  /**
   * Whether to write bundle to disk
   * @default true
   */
  write?: boolean;
  /**
   * Empty outDir on write.
   * @default true when outDir is a sub directory of project root
   */
  emptyOutDir?: boolean | null;
  /**
   * Copy the public directory to outDir on write.
   * @default true
   */
  copyPublicDir?: boolean;
  /**
   * Whether to emit a .vite/manifest.json in the output dir to map hash-less filenames
   * to their hashed versions. Useful when you want to generate your own HTML
   * instead of using the one generated by Vite.
   *
   * Example:
   *
   * ```json
   * {
   *   "main.js": {
   *     "file": "main.68fe3fad.js",
   *     "css": "main.e6b63442.css",
   *     "imports": [...],
   *     "dynamicImports": [...]
   *   }
   * }
   * ```
   * @default false
   */
  manifest?: boolean | string;
  /**
   * Build in library mode. The value should be the global name of the lib in
   * UMD mode. This will produce esm + cjs + umd bundle formats with default
   * configurations that are suitable for distributing libraries.
   * @default false
   */
  lib?: LibraryOptions | false;
  /**
   * Produce SSR oriented build. Note this requires specifying SSR entry via
   * `rollupOptions.input`.
   * @default false
   */
  ssr?: boolean | string;
  /**
   * Generate SSR manifest for determining style links and asset preload
   * directives in production.
   * @default false
   */
  ssrManifest?: boolean | string;
  /**
   * Emit assets during SSR.
   * @default false
   */
  ssrEmitAssets?: boolean;
  /**
   * Emit assets during build. Frameworks can set environments.ssr.build.emitAssets
   * By default, it is true for the client and false for other environments.
   */
  emitAssets?: boolean;
  /**
   * Set to false to disable reporting compressed chunk sizes.
   * Can slightly improve build speed.
   * @default true
   */
  reportCompressedSize?: boolean;
  /**
   * Adjust chunk size warning limit (in kB).
   * @default 500
   */
  chunkSizeWarningLimit?: number;
  /**
   * Rollup watch options
   * https://rollupjs.org/configuration-options/#watch
   * @default null
   */
  watch?: WatcherOptions | null;
  /**
   * create the Build Environment instance
   */
  createEnvironment?: (name: string, config: ResolvedConfig) => Promise<BuildEnvironment> | BuildEnvironment;
}
type BuildOptions = BuildEnvironmentOptions;
interface LibraryOptions {
  /**
   * Path of library entry
   */
  entry: InputOption;
  /**
   * The name of the exposed global variable. Required when the `formats` option includes
   * `umd` or `iife`
   */
  name?: string;
  /**
   * Output bundle formats
   * @default ['es', 'umd']
   */
  formats?: LibraryFormats[];
  /**
   * The name of the package file output. The default file name is the name option
   * of the project package.json. It can also be defined as a function taking the
   * format as an argument.
   */
  fileName?: string | ((format: ModuleFormat, entryName: string) => string);
  /**
   * The name of the CSS file output if the library imports CSS. Defaults to the
   * same value as `build.lib.fileName` if it's set a string, otherwise it falls
   * back to the name option of the project package.json.
   */
  cssFileName?: string;
}
type LibraryFormats = 'es' | 'cjs' | 'umd' | 'iife' | 'system';
interface ModulePreloadOptions {
  /**
   * Whether to inject a module preload polyfill.
   * Note: does not apply to library mode.
   * @default true
   */
  polyfill?: boolean;
  /**
   * Resolve the list of dependencies to preload for a given dynamic import
   * @experimental
   */
  resolveDependencies?: ResolveModulePreloadDependenciesFn;
}
interface ResolvedModulePreloadOptions {
  polyfill: boolean;
  resolveDependencies?: ResolveModulePreloadDependenciesFn;
}
type ResolveModulePreloadDependenciesFn = (filename: string, deps: string[], context: {
  hostId: string;
  hostType: 'html' | 'js';
}) => string[];
interface ResolvedBuildEnvironmentOptions extends Required<Omit<BuildEnvironmentOptions, 'polyfillModulePreload'>> {
  modulePreload: false | ResolvedModulePreloadOptions;
}
interface ResolvedBuildOptions extends Required<Omit<BuildOptions, 'polyfillModulePreload'>> {
  modulePreload: false | ResolvedModulePreloadOptions;
}
/**
 * Bundles a single environment for production.
 * Returns a Promise containing the build result.
 */
type RenderBuiltAssetUrl = (filename: string, type: {
  type: 'asset' | 'public';
  hostId: string;
  hostType: 'js' | 'css' | 'html';
  ssr: boolean;
}) => string | {
  relative?: boolean;
  runtime?: string;
} | undefined;
declare class BuildEnvironment extends BaseEnvironment {
  mode: "build";
  isBuilt: boolean;
  constructor(name: string, config: ResolvedConfig, setup?: {
    options?: EnvironmentOptions;
  });
  init(): Promise<void>;
}
interface ViteBuilder {
  environments: Record<string, BuildEnvironment>;
  config: ResolvedConfig;
  buildApp(): Promise<void>;
  build(environment: BuildEnvironment): Promise<RollupOutput | RollupOutput[] | RollupWatcher>;
}
interface BuilderOptions {
  /**
   * Whether to share the config instance among environments to align with the behavior of dev server.
   *
   * @default false
   * @experimental
   */
  sharedConfigBuild?: boolean;
  /**
   * Whether to share the plugin instances among environments to align with the behavior of dev server.
   *
   * @default false
   * @experimental
   */
  sharedPlugins?: boolean;
  buildApp?: (builder: ViteBuilder) => Promise<void>;
}
type ResolvedBuilderOptions = Required<BuilderOptions>;
/**
 * Creates a ViteBuilder to orchestrate building multiple environments.
 * @experimental
 */
type BuildAppHook = (this: MinimalPluginContextWithoutEnvironment, builder: ViteBuilder) => Promise<void>; //#endregion
//#region src/node/environment.d.ts
type Environment = DevEnvironment | BuildEnvironment | UnknownEnvironment;
/**
 * Creates a function that hides the complexities of a WeakMap with an initial value
 * to implement object metadata. Used by plugins to implement cross hooks per
 * environment metadata
 *
 * @experimental
 */
//#endregion
//#region src/node/server/pluginContainer.d.ts
type SkipInformation = {
  id: string;
  importer: string | undefined;
  plugin: Plugin$1;
  called?: boolean;
};
declare class EnvironmentPluginContainer<Env extends Environment = Environment> {
  environment: Env;
  plugins: readonly Plugin$1[];
  watcher?: FSWatcher | undefined;
  private _pluginContextMap;
  private _resolvedRollupOptions?;
  private _processesing;
  private _seenResolves;
  private _moduleNodeToLoadAddedImports;
  getSortedPluginHooks: PluginHookUtils['getSortedPluginHooks'];
  getSortedPlugins: PluginHookUtils['getSortedPlugins'];
  moduleGraph: EnvironmentModuleGraph | undefined;
  watchFiles: Set<string>;
  minimalContext: MinimalPluginContext$1<Env>;
  private _started;
  private _buildStartPromise;
  private _closed;
  private _updateModuleLoadAddedImports;
  private _getAddedImports;
  getModuleInfo(id: string): ModuleInfo$1 | null;
  private handleHookPromise;
  get options(): InputOptions;
  resolveRollupOptions(): Promise<InputOptions>;
  private _getPluginContext;
  private hookParallel;
  buildStart(_options?: InputOptions): Promise<void>;
  resolveId(rawId: string, importer?: string | undefined, options?: {
    attributes?: Record<string, string>;
    custom?: CustomPluginOptions; /** @deprecated use `skipCalls` instead */
    skip?: Set<Plugin$1>;
    skipCalls?: readonly SkipInformation[];
    isEntry?: boolean;
  }): Promise<PartialResolvedId | null>;
  load(id: string): Promise<LoadResult | null>;
  transform(code: string, id: string, options?: {
    inMap?: SourceDescription['map'];
  }): Promise<{
    code: string;
    map: SourceMap$2 | {
      mappings: '';
    } | null;
  }>;
  watchChange(id: string, change: {
    event: 'create' | 'update' | 'delete';
  }): Promise<void>;
  close(): Promise<void>;
}
declare class BasicMinimalPluginContext<Meta = PluginContextMeta> {
  meta: Meta;
  private _logger;
  constructor(meta: Meta, _logger: Logger);
  debug(rawLog: string | RollupLog | (() => string | RollupLog)): void;
  info(rawLog: string | RollupLog | (() => string | RollupLog)): void;
  warn(rawLog: string | RollupLog | (() => string | RollupLog)): void;
  error(e: string | RollupError): never;
  private _normalizeRawLog;
}
declare class MinimalPluginContext$1<T extends Environment = Environment> extends BasicMinimalPluginContext implements MinimalPluginContext {
  environment: T;
  constructor(meta: PluginContextMeta, environment: T);
}
declare class PluginContainer {
  private environments;
  constructor(environments: Record<string, Environment>);
  private _getEnvironment;
  private _getPluginContainer;
  getModuleInfo(id: string): ModuleInfo$1 | null;
  get options(): InputOptions;
  buildStart(_options?: InputOptions): Promise<void>;
  watchChange(id: string, change: {
    event: 'create' | 'update' | 'delete';
  }): Promise<void>;
  resolveId(rawId: string, importer?: string, options?: {
    attributes?: Record<string, string>;
    custom?: CustomPluginOptions; /** @deprecated use `skipCalls` instead */
    skip?: Set<Plugin$1>;
    skipCalls?: readonly SkipInformation[];
    ssr?: boolean;
    isEntry?: boolean;
  }): Promise<PartialResolvedId | null>;
  load(id: string, options?: {
    ssr?: boolean;
  }): Promise<LoadResult | null>;
  transform(code: string, id: string, options?: {
    ssr?: boolean;
    environment?: Environment;
    inMap?: SourceDescription['map'];
  }): Promise<{
    code: string;
    map: SourceMap$2 | {
      mappings: '';
    } | null;
  }>;
  close(): Promise<void>;
}
/**
 * server.pluginContainer compatibility
 *
 * The default environment is in buildStart, buildEnd, watchChange, and closeBundle hooks,
 * which are called once for all environments, or when no environment is passed in other hooks.
 * The ssrEnvironment is needed for backward compatibility when the ssr flag is passed without
 * an environment. The defaultEnvironment in the main pluginContainer in the server should be
 * the client environment for backward compatibility.
 **/
//#endregion
//#region src/node/server/index.d.ts
interface ServerOptions$1$1 extends CommonServerOptions {
  /**
   * Configure HMR-specific options (port, host, path & protocol)
   */
  hmr?: HmrOptions | boolean;
  /**
   * Do not start the websocket connection.
   * @experimental
   */
  ws?: false;
  /**
   * Warm-up files to transform and cache the results in advance. This improves the
   * initial page load during server starts and prevents transform waterfalls.
   */
  warmup?: {
    /**
     * The files to be transformed and used on the client-side. Supports glob patterns.
     */
    clientFiles?: string[];
    /**
     * The files to be transformed and used in SSR. Supports glob patterns.
     */
    ssrFiles?: string[];
  };
  /**
   * chokidar watch options or null to disable FS watching
   * https://github.com/paulmillr/chokidar/tree/3.6.0#api
   */
  watch?: WatchOptions | null;
  /**
   * Create Vite dev server to be used as a middleware in an existing server
   * @default false
   */
  middlewareMode?: boolean | {
    /**
     * Parent server instance to attach to
     *
     * This is needed to proxy WebSocket connections to the parent server.
     */
    server: HttpServer;
  };
  /**
   * Options for files served via '/\@fs/'.
   */
  fs?: FileSystemServeOptions;
  /**
   * Origin for the generated asset URLs.
   *
   * @example `http://127.0.0.1:8080`
   */
  origin?: string;
  /**
   * Pre-transform known direct imports
   * @default true
   */
  preTransformRequests?: boolean;
  /**
   * Whether or not to ignore-list source files in the dev server sourcemap, used to populate
   * the [`x_google_ignoreList` source map extension](https://developer.chrome.com/blog/devtools-better-angular-debugging/#the-x_google_ignorelist-source-map-extension).
   *
   * By default, it excludes all paths containing `node_modules`. You can pass `false` to
   * disable this behavior, or, for full control, a function that takes the source path and
   * sourcemap path and returns whether to ignore the source path.
   */
  sourcemapIgnoreList?: false | ((sourcePath: string, sourcemapPath: string) => boolean);
  /**
   * Backward compatibility. The buildStart and buildEnd hooks were called only once for all
   * environments. This option enables per-environment buildStart and buildEnd hooks.
   * @default false
   * @experimental
   */
  perEnvironmentStartEndDuringDev?: boolean;
  /**
   * Run HMR tasks, by default the HMR propagation is done in parallel for all environments
   * @experimental
   */
  hotUpdateEnvironments?: (server: ViteDevServer, hmr: (environment: DevEnvironment) => Promise<void>) => Promise<void>;
}
interface ResolvedServerOptions extends Omit<RequiredExceptFor<ServerOptions$1$1, 'host' | 'https' | 'proxy' | 'hmr' | 'ws' | 'watch' | 'origin' | 'hotUpdateEnvironments'>, 'fs' | 'middlewareMode' | 'sourcemapIgnoreList'> {
  fs: Required<FileSystemServeOptions>;
  middlewareMode: NonNullable<ServerOptions$1$1['middlewareMode']>;
  sourcemapIgnoreList: Exclude<ServerOptions$1$1['sourcemapIgnoreList'], false | undefined>;
}
interface FileSystemServeOptions {
  /**
   * Strictly restrict file accessing outside of allowing paths.
   *
   * Set to `false` to disable the warning
   *
   * @default true
   */
  strict?: boolean;
  /**
   * Restrict accessing files outside the allowed directories.
   *
   * Accepts absolute path or a path relative to project root.
   * Will try to search up for workspace root by default.
   */
  allow?: string[];
  /**
   * Restrict accessing files that matches the patterns.
   *
   * This will have higher priority than `allow`.
   * picomatch patterns are supported.
   *
   * @default ['.env', '.env.*', '*.{crt,pem}', '**\/.git/**']
   */
  deny?: string[];
}
type ServerHook = (this: MinimalPluginContextWithoutEnvironment, server: ViteDevServer) => (() => void) | void | Promise<(() => void) | void>;
type HttpServer = http.Server | Http2SecureServer;
interface ViteDevServer {
  /**
   * The resolved vite config object
   */
  config: ResolvedConfig;
  /**
   * A connect app instance.
   * - Can be used to attach custom middlewares to the dev server.
   * - Can also be used as the handler function of a custom http server
   *   or as a middleware in any connect-style Node.js frameworks
   *
   * https://github.com/senchalabs/connect#use-middleware
   */
  middlewares: Connect.Server;
  /**
   * native Node http server instance
   * will be null in middleware mode
   */
  httpServer: HttpServer | null;
  /**
   * Chokidar watcher instance. If `config.server.watch` is set to `null`,
   * it will not watch any files and calling `add` or `unwatch` will have no effect.
   * https://github.com/paulmillr/chokidar/tree/3.6.0#api
   */
  watcher: FSWatcher;
  /**
   * WebSocket server with `send(payload)` method
   */
  ws: WebSocketServer;
  /**
   * An alias to `server.environments.client.hot`.
   * If you want to interact with all environments, loop over `server.environments`.
   */
  hot: NormalizedHotChannel;
  /**
   * Rollup plugin container that can run plugin hooks on a given file
   */
  pluginContainer: PluginContainer;
  /**
   * Module execution environments attached to the Vite server.
   */
  environments: Record<'client' | 'ssr' | (string & {}), DevEnvironment>;
  /**
   * Module graph that tracks the import relationships, url to file mapping
   * and hmr state.
   */
  moduleGraph: ModuleGraph;
  /**
   * The resolved urls Vite prints on the CLI (URL-encoded). Returns `null`
   * in middleware mode or if the server is not listening on any port.
   */
  resolvedUrls: ResolvedServerUrls | null;
  /**
   * Programmatically resolve, load and transform a URL and get the result
   * without going through the http request pipeline.
   */
  transformRequest(url: string, options?: TransformOptions): Promise<TransformResult | null>;
  /**
   * Same as `transformRequest` but only warm up the URLs so the next request
   * will already be cached. The function will never throw as it handles and
   * reports errors internally.
   */
  warmupRequest(url: string, options?: TransformOptions): Promise<void>;
  /**
   * Apply vite built-in HTML transforms and any plugin HTML transforms.
   */
  transformIndexHtml(url: string, html: string, originalUrl?: string): Promise<string>;
  /**
   * Transform module code into SSR format.
   */
  ssrTransform(code: string, inMap: SourceMap$2 | {
    mappings: '';
  } | null, url: string, originalCode?: string): Promise<TransformResult | null>;
  /**
   * Load a given URL as an instantiated module for SSR.
   */
  ssrLoadModule(url: string, opts?: {
    fixStacktrace?: boolean;
  }): Promise<Record<string, any>>;
  /**
   * Returns a fixed version of the given stack
   */
  ssrRewriteStacktrace(stack: string): string;
  /**
   * Mutates the given SSR error by rewriting the stacktrace
   */
  ssrFixStacktrace(e: Error): void;
  /**
   * Triggers HMR for a module in the module graph. You can use the `server.moduleGraph`
   * API to retrieve the module to be reloaded. If `hmr` is false, this is a no-op.
   */
  reloadModule(module: ModuleNode): Promise<void>;
  /**
   * Start the server.
   */
  listen(port?: number, isRestart?: boolean): Promise<ViteDevServer>;
  /**
   * Stop the server.
   */
  close(): Promise<void>;
  /**
   * Print server urls
   */
  printUrls(): void;
  /**
   * Bind CLI shortcuts
   */
  bindCLIShortcuts(options?: BindCLIShortcutsOptions<ViteDevServer>): void;
  /**
   * Restart the server.
   *
   * @param forceOptimize - force the optimizer to re-bundle, same as --force cli flag
   */
  restart(forceOptimize?: boolean): Promise<void>;
  /**
   * Open browser
   */
  openBrowser(): void;
  /**
   * Calling `await server.waitForRequestsIdle(id)` will wait until all static imports
   * are processed. If called from a load or transform plugin hook, the id needs to be
   * passed as a parameter to avoid deadlocks. Calling this function after the first
   * static imports section of the module graph has been processed will resolve immediately.
   */
  waitForRequestsIdle: (ignoredId?: string) => Promise<void>;
}
interface ResolvedServerUrls {
  local: string[];
  network: string[];
}
//#endregion
//#region src/node/plugins/html.d.ts
interface HtmlTagDescriptor {
  tag: string;
  attrs?: Record<string, string | boolean | undefined>;
  children?: string | HtmlTagDescriptor[];
  /**
   * default: 'head-prepend'
   */
  injectTo?: 'head' | 'body' | 'head-prepend' | 'body-prepend';
}
type IndexHtmlTransformResult = string | HtmlTagDescriptor[] | {
  html: string;
  tags: HtmlTagDescriptor[];
};
interface IndexHtmlTransformContext {
  /**
   * public path when served
   */
  path: string;
  /**
   * filename on disk
   */
  filename: string;
  server?: ViteDevServer;
  bundle?: OutputBundle;
  chunk?: OutputChunk;
  originalUrl?: string;
}
type IndexHtmlTransformHook = (this: MinimalPluginContextWithoutEnvironment, html: string, ctx: IndexHtmlTransformContext) => IndexHtmlTransformResult | void | Promise<IndexHtmlTransformResult | void>;
type IndexHtmlTransform = IndexHtmlTransformHook | {
  order?: 'pre' | 'post' | null;
  handler: IndexHtmlTransformHook;
}; //#endregion
//#region src/node/plugins/pluginFilter.d.ts
type StringFilter<Value = string | RegExp> = Value | Array<Value> | {
  include?: Value | Array<Value>;
  exclude?: Value | Array<Value>;
}; //#endregion
//#region src/node/plugin.d.ts
/**
 * Vite plugins extends the Rollup plugin interface with a few extra
 * vite-specific options. A valid vite plugin is also a valid Rollup plugin.
 * On the contrary, a Rollup plugin may or may NOT be a valid vite universal
 * plugin, since some Rollup features do not make sense in an unbundled
 * dev server context. That said, as long as a rollup plugin doesn't have strong
 * coupling between its bundle phase and output phase hooks then it should
 * just work (that means, most of them).
 *
 * By default, the plugins are run during both serve and build. When a plugin
 * is applied during serve, it will only run **non output plugin hooks** (see
 * rollup type definition of {@link rollup#PluginHooks}). You can think of the
 * dev server as only running `const bundle = rollup.rollup()` but never calling
 * `bundle.generate()`.
 *
 * A plugin that expects to have different behavior depending on serve/build can
 * export a factory function that receives the command being run via options.
 *
 * If a plugin should be applied only for server or build, a function format
 * config file can be used to conditional determine the plugins to use.
 *
 * The current environment can be accessed from the context for the all non-global
 * hooks (it is not available in config, configResolved, configureServer, etc).
 * It can be a dev, build, or scan environment.
 * Plugins can use this.environment.mode === 'dev' to guard for dev specific APIs.
 */
interface PluginContextExtension {
  /**
   * Vite-specific environment instance
   */
  environment: Environment;
}
interface PluginContextMetaExtension {
  viteVersion: string;
}
interface ConfigPluginContext extends Omit<MinimalPluginContext, 'meta' | 'environment'> {
  meta: Omit<PluginContextMeta, 'watchMode'>;
}
interface MinimalPluginContextWithoutEnvironment extends Omit<MinimalPluginContext, 'environment'> {}
declare module 'rollup' {
  interface MinimalPluginContext extends PluginContextExtension {}
  interface PluginContextMeta extends PluginContextMetaExtension {}
}
/**
 * There are two types of plugins in Vite. App plugins and environment plugins.
 * Environment Plugins are defined by a constructor function that will be called
 * once per each environment allowing users to have completely different plugins
 * for each of them. The constructor gets the resolved environment after the server
 * and builder has already been created simplifying config access and cache
 * management for for environment specific plugins.
 * Environment Plugins are closer to regular rollup plugins. They can't define
 * app level hooks (like config, configResolved, configureServer, etc).
 */
interface Plugin$1<A = any> extends Plugin$3<A> {
  /**
   * Perform custom handling of HMR updates.
   * The handler receives an options containing changed filename, timestamp, a
   * list of modules affected by the file change, and the dev server instance.
   *
   * - The hook can return a filtered list of modules to narrow down the update.
   *   e.g. for a Vue SFC, we can narrow down the part to update by comparing
   *   the descriptors.
   *
   * - The hook can also return an empty array and then perform custom updates
   *   by sending a custom hmr payload via environment.hot.send().
   *
   * - If the hook doesn't return a value, the hmr update will be performed as
   *   normal.
   */
  hotUpdate?: ObjectHook<(this: MinimalPluginContext & {
    environment: DevEnvironment;
  }, options: HotUpdateOptions) => Array<EnvironmentModuleNode> | void | Promise<Array<EnvironmentModuleNode> | void>>;
  /**
   * extend hooks with ssr flag
   */
  resolveId?: ObjectHook<(this: PluginContext, source: string, importer: string | undefined, options: {
    attributes: Record<string, string>;
    custom?: CustomPluginOptions;
    ssr?: boolean;
    isEntry: boolean;
  }) => Promise<ResolveIdResult> | ResolveIdResult, {
    filter?: {
      id?: StringFilter<RegExp>;
    };
  }>;
  load?: ObjectHook<(this: PluginContext, id: string, options?: {
    ssr?: boolean;
  }) => Promise<LoadResult> | LoadResult, {
    filter?: {
      id?: StringFilter;
    };
  }>;
  transform?: ObjectHook<(this: TransformPluginContext, code: string, id: string, options?: {
    ssr?: boolean;
  }) => Promise<TransformResult$2> | TransformResult$2, {
    filter?: {
      id?: StringFilter;
      code?: StringFilter;
    };
  }>;
  /**
   * Opt-in this plugin into the shared plugins pipeline.
   * For backward-compatibility, plugins are re-recreated for each environment
   * during `vite build --app`
   * We have an opt-in per plugin, and a general `builder.sharedPlugins`
   * In a future major, we'll flip the default to be shared by default
   * @experimental
   */
  sharedDuringBuild?: boolean;
  /**
   * Opt-in this plugin into per-environment buildStart and buildEnd during dev.
   * For backward-compatibility, the buildStart hook is called only once during
   * dev, for the client environment. Plugins can opt-in to be called
   * per-environment, aligning with the build hook behavior.
   * @experimental
   */
  perEnvironmentStartEndDuringDev?: boolean;
  /**
   * Enforce plugin invocation tier similar to webpack loaders. Hooks ordering
   * is still subject to the `order` property in the hook object.
   *
   * Plugin invocation order:
   * - alias resolution
   * - `enforce: 'pre'` plugins
   * - vite core plugins
   * - normal plugins
   * - vite build plugins
   * - `enforce: 'post'` plugins
   * - vite build post plugins
   */
  enforce?: 'pre' | 'post';
  /**
   * Apply the plugin only for serve or build, or on certain conditions.
   */
  apply?: 'serve' | 'build' | ((this: void, config: UserConfig, env: ConfigEnv) => boolean);
  /**
   * Define environments where this plugin should be active
   * By default, the plugin is active in all environments
   * @experimental
   */
  applyToEnvironment?: (environment: PartialEnvironment) => boolean | Promise<boolean> | PluginOption;
  /**
   * Modify vite config before it's resolved. The hook can either mutate the
   * passed-in config directly, or return a partial config object that will be
   * deeply merged into existing config.
   *
   * Note: User plugins are resolved before running this hook so injecting other
   * plugins inside  the `config` hook will have no effect.
   */
  config?: ObjectHook<(this: ConfigPluginContext, config: UserConfig, env: ConfigEnv) => Omit<UserConfig, 'plugins'> | null | void | Promise<Omit<UserConfig, 'plugins'> | null | void>>;
  /**
   * Modify environment configs before it's resolved. The hook can either mutate the
   * passed-in environment config directly, or return a partial config object that will be
   * deeply merged into existing config.
   * This hook is called for each environment with a partially resolved environment config
   * that already accounts for the default environment config values set at the root level.
   * If plugins need to modify the config of a given environment, they should do it in this
   * hook instead of the config hook. Leaving the config hook only for modifying the root
   * default environment config.
   */
  configEnvironment?: ObjectHook<(this: ConfigPluginContext, name: string, config: EnvironmentOptions, env: ConfigEnv & {
    /**
     * Whether this environment is SSR environment and `ssr.target` is set to `'webworker'`.
     * Only intended to be used for backward compatibility.
     */
    isSsrTargetWebworker?: boolean;
  }) => EnvironmentOptions | null | void | Promise<EnvironmentOptions | null | void>>;
  /**
   * Use this hook to read and store the final resolved vite config.
   */
  configResolved?: ObjectHook<(this: MinimalPluginContextWithoutEnvironment, config: ResolvedConfig) => void | Promise<void>>;
  /**
   * Configure the vite server. The hook receives the {@link ViteDevServer}
   * instance. This can also be used to store a reference to the server
   * for use in other hooks.
   *
   * The hooks will be called before internal middlewares are applied. A hook
   * can return a post hook that will be called after internal middlewares
   * are applied. Hook can be async functions and will be called in series.
   */
  configureServer?: ObjectHook<ServerHook>;
  /**
   * Configure the preview server. The hook receives the {@link PreviewServer}
   * instance. This can also be used to store a reference to the server
   * for use in other hooks.
   *
   * The hooks are called before other middlewares are applied. A hook can
   * return a post hook that will be called after other middlewares are
   * applied. Hooks can be async functions and will be called in series.
   */
  configurePreviewServer?: ObjectHook<PreviewServerHook>;
  /**
   * Transform index.html.
   * The hook receives the following arguments:
   *
   * - html: string
   * - ctx: IndexHtmlTransformContext, which contains:
   *    - path: public path when served
   *    - filename: filename on disk
   *    - server?: ViteDevServer (only present during serve)
   *    - bundle?: rollup.OutputBundle (only present during build)
   *    - chunk?: rollup.OutputChunk
   *    - originalUrl?: string
   *
   * It can either return a transformed string, or a list of html tag
   * descriptors that will be injected into the `<head>` or `<body>`.
   *
   * By default the transform is applied **after** vite's internal html
   * transform. If you need to apply the transform before vite, use an object:
   * `{ order: 'pre', handler: hook }`
   */
  transformIndexHtml?: IndexHtmlTransform;
  /**
   * Build Environments
   *
   * @experimental
   */
  buildApp?: ObjectHook<BuildAppHook>;
  /**
   * Perform custom handling of HMR updates.
   * The handler receives a context containing changed filename, timestamp, a
   * list of modules affected by the file change, and the dev server instance.
   *
   * - The hook can return a filtered list of modules to narrow down the update.
   *   e.g. for a Vue SFC, we can narrow down the part to update by comparing
   *   the descriptors.
   *
   * - The hook can also return an empty array and then perform custom updates
   *   by sending a custom hmr payload via server.ws.send().
   *
   * - If the hook doesn't return a value, the hmr update will be performed as
   *   normal.
   */
  handleHotUpdate?: ObjectHook<(this: MinimalPluginContextWithoutEnvironment, ctx: HmrContext) => Array<ModuleNode> | void | Promise<Array<ModuleNode> | void>>;
}
type HookHandler<T> = T extends ObjectHook<infer H> ? H : T;
type PluginWithRequiredHook<K extends keyof Plugin$1> = Plugin$1 & { [P in K]: NonNullable<Plugin$1[P]> };
type Thenable<T> = T | Promise<T>;
type FalsyPlugin = false | null | undefined;
type PluginOption = Thenable<Plugin$1 | FalsyPlugin | PluginOption[]>;
/**
 * @experimental
 */
//#endregion
//#region src/node/plugins/css.d.ts
interface CSSOptions {
  /**
   * Using lightningcss is an experimental option to handle CSS modules,
   * assets and imports via Lightning CSS. It requires to install it as a
   * peer dependency.
   *
   * @default 'postcss'
   * @experimental
   */
  transformer?: 'postcss' | 'lightningcss';
  /**
   * https://github.com/css-modules/postcss-modules
   */
  modules?: CSSModulesOptions | false;
  /**
   * Options for preprocessors.
   *
   * In addition to options specific to each processors, Vite supports `additionalData` option.
   * The `additionalData` option can be used to inject extra code for each style content.
   */
  preprocessorOptions?: {
    scss?: SassPreprocessorOptions;
    sass?: SassPreprocessorOptions;
    less?: LessPreprocessorOptions;
    styl?: StylusPreprocessorOptions;
    stylus?: StylusPreprocessorOptions;
  };
  /**
   * If this option is set, preprocessors will run in workers when possible.
   * `true` means the number of CPUs minus 1.
   *
   * @default true
   */
  preprocessorMaxWorkers?: number | true;
  postcss?: string | (ProcessOptions & {
    plugins?: AcceptedPlugin[];
  });
  /**
   * Enables css sourcemaps during dev
   * @default false
   * @experimental
   */
  devSourcemap?: boolean;
  /**
   * @experimental
   */
  lightningcss?: LightningCSSOptions;
}
interface CSSModulesOptions {
  getJSON?: (cssFileName: string, json: Record<string, string>, outputFileName: string) => void;
  scopeBehaviour?: 'global' | 'local';
  globalModulePaths?: RegExp[];
  exportGlobals?: boolean;
  generateScopedName?: string | ((name: string, filename: string, css: string) => string);
  hashPrefix?: string;
  /**
   * default: undefined
   */
  localsConvention?: 'camelCase' | 'camelCaseOnly' | 'dashes' | 'dashesOnly' | ((originalClassName: string, generatedClassName: string, inputFile: string) => string);
}
type ResolvedCSSOptions = Omit<CSSOptions, 'lightningcss'> & Required<Pick<CSSOptions, 'transformer' | 'devSourcemap'>> & {
  lightningcss?: LightningCSSOptions;
};
type PreprocessorAdditionalDataResult = string | {
  content: string;
  map?: ExistingRawSourceMap;
};
type PreprocessorAdditionalData = string | ((source: string, filename: string) => PreprocessorAdditionalDataResult | Promise<PreprocessorAdditionalDataResult>);
type SassPreprocessorOptions = {
  additionalData?: PreprocessorAdditionalData;
} & SassModernPreprocessBaseOptions;
type LessPreprocessorOptions = {
  additionalData?: PreprocessorAdditionalData;
} & LessPreprocessorBaseOptions;
type StylusPreprocessorOptions = {
  additionalData?: PreprocessorAdditionalData;
} & StylusPreprocessorBaseOptions; //#endregion
//#region src/node/plugins/esbuild.d.ts
interface ESBuildOptions extends TransformOptions$1 {
  include?: string | RegExp | ReadonlyArray<string | RegExp>;
  exclude?: string | RegExp | ReadonlyArray<string | RegExp>;
  jsxInject?: string;
  /**
   * This option is not respected. Use `build.minify` instead.
   */
  minify?: never;
}
//#endregion
//#region src/node/plugins/json.d.ts
interface JsonOptions {
  /**
   * Generate a named export for every property of the JSON object
   * @default true
   */
  namedExports?: boolean;
  /**
   * Generate performant output as JSON.parse("stringified").
   *
   * When set to 'auto', the data will be stringified only if the data is bigger than 10kB.
   * @default 'auto'
   */
  stringify?: boolean | 'auto';
} //#endregion
//#region src/node/ssr/index.d.ts
type SSRTarget = 'node' | 'webworker';
type SsrDepOptimizationConfig = DepOptimizationConfig;
interface SSROptions {
  noExternal?: string | RegExp | (string | RegExp)[] | true;
  external?: string[] | true;
  /**
   * Define the target for the ssr build. The browser field in package.json
   * is ignored for node but used if webworker is the target
   * This option will be removed in a future major version
   * @default 'node'
   */
  target?: SSRTarget;
  /**
   * Control over which dependencies are optimized during SSR and esbuild options
   * During build:
   *   no external CJS dependencies are optimized by default
   * During dev:
   *   explicit no external CJS dependencies are optimized by default
   * @experimental
   */
  optimizeDeps?: SsrDepOptimizationConfig;
  resolve?: {
    /**
     * Conditions that are used in the plugin pipeline. The default value is the root config's `resolve.conditions`.
     *
     * Use this to override the default ssr conditions for the ssr build.
     *
     * @default rootConfig.resolve.conditions
     */
    conditions?: string[];
    /**
     * Conditions that are used during ssr import (including `ssrLoadModule`) of externalized dependencies.
     *
     * @default ['node', 'module-sync']
     */
    externalConditions?: string[];
    mainFields?: string[];
  };
}
interface ResolvedSSROptions extends SSROptions {
  target: SSRTarget;
  optimizeDeps: SsrDepOptimizationConfig;
} //#endregion
//#region src/node/config.d.ts
interface ConfigEnv {
  /**
   * 'serve': during dev (`vite` command)
   * 'build': when building for production (`vite build` command)
   */
  command: 'build' | 'serve';
  mode: string;
  isSsrBuild?: boolean;
  isPreview?: boolean;
}
/**
 * spa: include SPA fallback middleware and configure sirv with `single: true` in preview
 *
 * mpa: only include non-SPA HTML middlewares
 *
 * custom: don't include HTML middlewares
 */
type AppType = 'spa' | 'mpa' | 'custom';
interface CreateDevEnvironmentContext {
  ws: WebSocketServer;
}
interface DevEnvironmentOptions {
  /**
   * Files to be pre-transformed. Supports glob patterns.
   */
  warmup?: string[];
  /**
   * Pre-transform known direct imports
   * defaults to true for the client environment, false for the rest
   */
  preTransformRequests?: boolean;
  /**
   * Enables sourcemaps during dev
   * @default { js: true }
   * @experimental
   */
  sourcemap?: boolean | {
    js?: boolean;
    css?: boolean;
  };
  /**
   * Whether or not to ignore-list source files in the dev server sourcemap, used to populate
   * the [`x_google_ignoreList` source map extension](https://developer.chrome.com/blog/devtools-better-angular-debugging/#the-x_google_ignorelist-source-map-extension).
   *
   * By default, it excludes all paths containing `node_modules`. You can pass `false` to
   * disable this behavior, or, for full control, a function that takes the source path and
   * sourcemap path and returns whether to ignore the source path.
   */
  sourcemapIgnoreList?: false | ((sourcePath: string, sourcemapPath: string) => boolean);
  /**
   * create the Dev Environment instance
   */
  createEnvironment?: (name: string, config: ResolvedConfig, context: CreateDevEnvironmentContext) => Promise<DevEnvironment> | DevEnvironment;
  /**
   * For environments that support a full-reload, like the client, we can short-circuit when
   * restarting the server throwing early to stop processing current files. We avoided this for
   * SSR requests. Maybe this is no longer needed.
   * @experimental
   */
  recoverable?: boolean;
  /**
   * For environments associated with a module runner.
   * By default, it is false for the client environment and true for non-client environments.
   * This option can also be used instead of the removed config.experimental.skipSsrTransform.
   */
  moduleRunnerTransform?: boolean;
}
type ResolvedDevEnvironmentOptions = Omit<Required<DevEnvironmentOptions>, 'sourcemapIgnoreList'> & {
  sourcemapIgnoreList: Exclude<DevEnvironmentOptions['sourcemapIgnoreList'], false | undefined>;
};
type AllResolveOptions = ResolveOptions & {
  alias?: AliasOptions;
};
interface SharedEnvironmentOptions {
  /**
   * Define global variable replacements.
   * Entries will be defined on `window` during dev and replaced during build.
   */
  define?: Record<string, any>;
  /**
   * Configure resolver
   */
  resolve?: EnvironmentResolveOptions;
  /**
   * Define if this environment is used for Server-Side Rendering
   * @default 'server' if it isn't the client environment
   */
  consumer?: 'client' | 'server';
  /**
   * If true, `process.env` referenced in code will be preserved as-is and evaluated in runtime.
   * Otherwise, it is statically replaced as an empty object.
   */
  keepProcessEnv?: boolean;
  /**
   * Optimize deps config
   */
  optimizeDeps?: DepOptimizationOptions;
}
interface EnvironmentOptions extends SharedEnvironmentOptions {
  /**
   * Dev specific options
   */
  dev?: DevEnvironmentOptions;
  /**
   * Build specific options
   */
  build?: BuildEnvironmentOptions;
}
type ResolvedResolveOptions = Required<ResolveOptions>;
type ResolvedEnvironmentOptions = {
  define?: Record<string, any>;
  resolve: ResolvedResolveOptions;
  consumer: 'client' | 'server';
  keepProcessEnv?: boolean;
  optimizeDeps: DepOptimizationOptions;
  dev: ResolvedDevEnvironmentOptions;
  build: ResolvedBuildEnvironmentOptions;
  plugins: readonly Plugin$1[];
};
type DefaultEnvironmentOptions = Omit<EnvironmentOptions, 'consumer' | 'resolve' | 'keepProcessEnv'> & {
  resolve?: AllResolveOptions;
};
interface UserConfig extends DefaultEnvironmentOptions {
  /**
   * Project root directory. Can be an absolute path, or a path relative from
   * the location of the config file itself.
   * @default process.cwd()
   */
  root?: string;
  /**
   * Base public path when served in development or production.
   * @default '/'
   */
  base?: string;
  /**
   * Directory to serve as plain static assets. Files in this directory are
   * served and copied to build dist dir as-is without transform. The value
   * can be either an absolute file system path or a path relative to project root.
   *
   * Set to `false` or an empty string to disable copied static assets to build dist dir.
   * @default 'public'
   */
  publicDir?: string | false;
  /**
   * Directory to save cache files. Files in this directory are pre-bundled
   * deps or some other cache files that generated by vite, which can improve
   * the performance. You can use `--force` flag or manually delete the directory
   * to regenerate the cache files. The value can be either an absolute file
   * system path or a path relative to project root.
   * Default to `.vite` when no `package.json` is detected.
   * @default 'node_modules/.vite'
   */
  cacheDir?: string;
  /**
   * Explicitly set a mode to run in. This will override the default mode for
   * each command, and can be overridden by the command line --mode option.
   */
  mode?: string;
  /**
   * Array of vite plugins to use.
   */
  plugins?: PluginOption[];
  /**
   * HTML related options
   */
  html?: HTMLOptions;
  /**
   * CSS related options (preprocessors and CSS modules)
   */
  css?: CSSOptions;
  /**
   * JSON loading options
   */
  json?: JsonOptions;
  /**
   * Transform options to pass to esbuild.
   * Or set to `false` to disable esbuild.
   */
  esbuild?: ESBuildOptions | false;
  /**
   * Specify additional picomatch patterns to be treated as static assets.
   */
  assetsInclude?: string | RegExp | (string | RegExp)[];
  /**
   * Builder specific options
   * @experimental
   */
  builder?: BuilderOptions;
  /**
   * Server specific options, e.g. host, port, https...
   */
  server?: ServerOptions$1$1;
  /**
   * Preview specific options, e.g. host, port, https...
   */
  preview?: PreviewOptions;
  /**
   * Experimental features
   *
   * Features under this field could change in the future and might NOT follow semver.
   * Please be careful and always pin Vite's version when using them.
   * @experimental
   */
  experimental?: ExperimentalOptions;
  /**
   * Options to opt-in to future behavior
   */
  future?: FutureOptions | 'warn';
  /**
   * Legacy options
   *
   * Features under this field only follow semver for patches, they could be removed in a
   * future minor version. Please always pin Vite's version to a minor when using them.
   */
  legacy?: LegacyOptions;
  /**
   * Log level.
   * @default 'info'
   */
  logLevel?: LogLevel;
  /**
   * Custom logger.
   */
  customLogger?: Logger;
  /**
   * @default true
   */
  clearScreen?: boolean;
  /**
   * Environment files directory. Can be an absolute path, or a path relative from
   * root.
   * @default root
   */
  envDir?: string | false;
  /**
   * Env variables starts with `envPrefix` will be exposed to your client source code via import.meta.env.
   * @default 'VITE_'
   */
  envPrefix?: string | string[];
  /**
   * Worker bundle options
   */
  worker?: {
    /**
     * Output format for worker bundle
     * @default 'iife'
     */
    format?: 'es' | 'iife';
    /**
     * Vite plugins that apply to worker bundle. The plugins returned by this function
     * should be new instances every time it is called, because they are used for each
     * rollup worker bundling process.
     */
    plugins?: () => PluginOption[];
    /**
     * Rollup options to build worker bundle
     */
    rollupOptions?: Omit<RollupOptions, 'plugins' | 'input' | 'onwarn' | 'preserveEntrySignatures'>;
  };
  /**
   * Dep optimization options
   */
  optimizeDeps?: DepOptimizationOptions;
  /**
   * SSR specific options
   * We could make SSROptions be a EnvironmentOptions if we can abstract
   * external/noExternal for environments in general.
   */
  ssr?: SSROptions;
  /**
   * Environment overrides
   */
  environments?: Record<string, EnvironmentOptions>;
  /**
   * Whether your application is a Single Page Application (SPA),
   * a Multi-Page Application (MPA), or Custom Application (SSR
   * and frameworks with custom HTML handling)
   * @default 'spa'
   */
  appType?: AppType;
}
interface HTMLOptions {
  /**
   * A nonce value placeholder that will be used when generating script/style tags.
   *
   * Make sure that this placeholder will be replaced with a unique value for each request by the server.
   */
  cspNonce?: string;
}
interface FutureOptions {
  removePluginHookHandleHotUpdate?: 'warn';
  removePluginHookSsrArgument?: 'warn';
  removeServerModuleGraph?: 'warn';
  removeServerReloadModule?: 'warn';
  removeServerPluginContainer?: 'warn';
  removeServerHot?: 'warn';
  removeServerTransformRequest?: 'warn';
  removeServerWarmupRequest?: 'warn';
  removeSsrLoadModule?: 'warn';
}
interface ExperimentalOptions {
  /**
   * Append fake `&lang.(ext)` when queries are specified, to preserve the file extension for following plugins to process.
   *
   * @experimental
   * @default false
   */
  importGlobRestoreExtension?: boolean;
  /**
   * Allow finegrain control over assets and public files paths
   *
   * @experimental
   */
  renderBuiltUrl?: RenderBuiltAssetUrl;
  /**
   * Enables support of HMR partial accept via `import.meta.hot.acceptExports`.
   *
   * @experimental
   * @default false
   */
  hmrPartialAccept?: boolean;
}
interface LegacyOptions {
  /**
   * In Vite 6.0.8 and below, WebSocket server was able to connect from any web pages. However,
   * that could be exploited by a malicious web page.
   *
   * In Vite 6.0.9+, the WebSocket server now requires a token to connect from a web page.
   * But this may break some plugins and frameworks that connects to the WebSocket server
   * on their own. Enabling this option will make Vite skip the token check.
   *
   * **We do not recommend enabling this option unless you are sure that you are fine with
   * that security weakness.**
   */
  skipWebSocketTokenCheck?: boolean;
}
interface ResolvedWorkerOptions {
  format: 'es' | 'iife';
  plugins: (bundleChain: string[]) => Promise<ResolvedConfig>;
  rollupOptions: RollupOptions;
}
interface InlineConfig extends UserConfig {
  configFile?: string | false;
  /** @experimental */
  configLoader?: 'bundle' | 'runner' | 'native';
  /** @deprecated */
  envFile?: false;
  forceOptimizeDeps?: boolean;
}
interface ResolvedConfig extends Readonly<Omit<UserConfig, 'plugins' | 'css' | 'json' | 'assetsInclude' | 'optimizeDeps' | 'worker' | 'build' | 'dev' | 'environments' | 'experimental' | 'future' | 'server' | 'preview'> & {
  configFile: string | undefined;
  configFileDependencies: string[];
  inlineConfig: InlineConfig;
  root: string;
  base: string;
  publicDir: string;
  cacheDir: string;
  command: 'build' | 'serve';
  mode: string;
  isWorker: boolean;
  isProduction: boolean;
  envDir: string | false;
  env: Record<string, any>;
  resolve: Required<ResolveOptions> & {
    alias: Alias[];
  };
  plugins: readonly Plugin$1[];
  css: ResolvedCSSOptions;
  json: Required<JsonOptions>;
  esbuild: ESBuildOptions | false;
  server: ResolvedServerOptions;
  dev: ResolvedDevEnvironmentOptions; /** @experimental */
  builder: ResolvedBuilderOptions | undefined;
  build: ResolvedBuildOptions;
  preview: ResolvedPreviewOptions;
  ssr: ResolvedSSROptions;
  assetsInclude: (file: string) => boolean;
  logger: Logger;
  /**
   * Create an internal resolver to be used in special scenarios, e.g.
   * optimizer & handling css `@imports`.
   *
   * This API is deprecated. It only works for the client and ssr
   * environments. The `aliasOnly` option is also not being used anymore.
   * Plugins should move to `createIdResolver(environment.config)` instead.
   *
   * @deprecated Use `createIdResolver` from `vite` instead.
   */
  createResolver: (options?: Partial<InternalResolveOptions>) => ResolveFn;
  optimizeDeps: DepOptimizationOptions;
  worker: ResolvedWorkerOptions;
  appType: AppType;
  experimental: RequiredExceptFor<ExperimentalOptions, 'renderBuiltUrl'>;
  future: FutureOptions | undefined;
  environments: Record<string, ResolvedEnvironmentOptions>;
  /**
   * The token to connect to the WebSocket server from browsers.
   *
   * We recommend using `import.meta.hot` rather than connecting
   * to the WebSocket server directly.
   * If you have a usecase that requires connecting to the WebSocket
   * server, please create an issue so that we can discuss.
   *
   * @deprecated
   */
  webSocketToken: string;
} & PluginHookUtils> {}
interface PluginHookUtils {
  getSortedPlugins: <K extends keyof Plugin$1>(hookName: K) => PluginWithRequiredHook<K>[];
  getSortedPluginHooks: <K extends keyof Plugin$1>(hookName: K) => NonNullable<HookHandler<Plugin$1[K]>>[];
}
type ResolveFn = (id: string, importer?: string, aliasOnly?: boolean, ssr?: boolean) => Promise<string | undefined>;
//#endregion
//#region src/rpc/types.d.ts
type AssetType = 'image' | 'font' | 'video' | 'audio' | 'text' | 'json' | 'wasm' | 'other';
interface AssetInfo {
  path: string;
  type: AssetType;
  publicPath: string;
  relativePath: string;
  filePath: string;
  size: number;
  mtime: number;
}
interface ImageMeta {
  width: number;
  height: number;
  orientation?: number;
  type?: string;
  mimeType?: string;
}
type AssetImporter = Pick<ModuleNode, 'url' | 'id'>;
interface AssetEntry {
  path: string;
  content: string;
  encoding?: BufferEncoding;
  override?: boolean;
}
interface CodeSnippet {
  code: string;
  lang: string;
  name: string;
  docs?: string;
}
interface ModuleInfo {
  id: string;
  plugins: {
    name: string;
    transform?: number;
    resolveId?: number;
  }[];
  deps: string[];
  virtual: boolean;
}
//#endregion
//#region src/rpc/vite.d.ts
declare const viteRpcFunctions: {
  on: (event: string, handler: Function) => void;
  off: (event: string, handler: Function) => void;
  once: (event: string, handler: Function) => void;
  emit: (event: string, ...args: any[]) => void;
  heartbeat: () => boolean;
};
type ViteRPCFunctions = typeof viteRpcFunctions & {
  getStaticAssets: () => Promise<AssetInfo[]>;
  getAssetImporters: (url: string) => Promise<AssetImporter[]>;
  getImageMeta: (filepath: string) => Promise<ImageMeta>;
  getTextAssetContent: (filepath: string, limit?: number) => Promise<string>;
  getRoot: () => Promise<string>;
  getGraphModules: () => Promise<ModuleInfo[]>;
};
declare const viteRpc: {
  value: ReturnType<typeof getViteRpcClient<ViteRPCFunctions>>;
  functions: ReturnType<typeof getViteRpcClient<ViteRPCFunctions>>;
};
declare function onViteRpcConnected(callback: () => void): void;
declare function createViteClientRpc(): void;
declare function createViteServerRpc(functions: Record<string, any>): void;
//#endregion
//#region src/vue-plugin/devtools-state.d.ts
interface DevToolsState {
  connected: boolean;
  clientConnected: boolean;
  vueVersion: string;
  tabs: CustomTab[];
  commands: CustomCommand[];
  vitePluginDetected: boolean;
  appRecords: AppRecord[];
  activeAppRecordId: string;
  timelineLayersState: Record<string, boolean>;
}
type DevToolsRefState = { [P in keyof DevToolsState]: Ref<DevToolsState[P]> };
declare function VueDevToolsVuePlugin(): {
  install(app: App): void;
};
declare function createDevToolsStateContext(): {
  getDevToolsState: () => void;
  connected: Ref<boolean, boolean>;
  clientConnected: Ref<boolean, boolean>;
  vueVersion: Ref<string, string>;
  tabs: Ref<{
    name: string;
    icon?: string | undefined;
    title: string;
    view: {
      type: "iframe";
      src: string;
      persistent?: boolean | undefined;
    } | {
      type: "vnode";
      vnode: vue.VNode;
    } | {
      type: "sfc";
      sfc: string;
    };
    category?: ("app" | "pinned" | "modules" | "advanced") | undefined;
  }[], CustomTab[] | {
    name: string;
    icon?: string | undefined;
    title: string;
    view: {
      type: "iframe";
      src: string;
      persistent?: boolean | undefined;
    } | {
      type: "vnode";
      vnode: vue.VNode;
    } | {
      type: "sfc";
      sfc: string;
    };
    category?: ("app" | "pinned" | "modules" | "advanced") | undefined;
  }[]>;
  commands: Ref<{
    id: string;
    title: string;
    description?: string | undefined;
    order?: number | undefined;
    icon?: string | undefined;
    action?: {
      type: "url";
      src: string;
    } | undefined;
    children?: {
      icon?: string | undefined;
      title: string;
      id: string;
      description?: string | undefined;
      order?: number | undefined;
      action?: {
        type: "url";
        src: string;
      } | undefined;
    }[] | undefined;
  }[], CustomCommand[] | {
    id: string;
    title: string;
    description?: string | undefined;
    order?: number | undefined;
    icon?: string | undefined;
    action?: {
      type: "url";
      src: string;
    } | undefined;
    children?: {
      icon?: string | undefined;
      title: string;
      id: string;
      description?: string | undefined;
      order?: number | undefined;
      action?: {
        type: "url";
        src: string;
      } | undefined;
    }[] | undefined;
  }[]>;
  vitePluginDetected: Ref<boolean, boolean>;
  appRecords: Ref<{
    id: string;
    name: string;
    app?: _vue_devtools_kit0.App;
    version?: string | undefined;
    types?: Record<string, string | symbol> | undefined;
    instanceMap: Map<string, any> & Omit<Map<string, any>, keyof Map<any, any>>;
    perfGroupIds: Map<string, {
      groupId: number;
      time: number;
    }> & Omit<Map<string, {
      groupId: number;
      time: number;
    }>, keyof Map<any, any>>;
    rootInstance: _vue_devtools_kit0.VueAppInstance;
    routerId?: string | undefined;
    iframe?: string | undefined;
  }[], AppRecord[] | {
    id: string;
    name: string;
    app?: _vue_devtools_kit0.App;
    version?: string | undefined;
    types?: Record<string, string | symbol> | undefined;
    instanceMap: Map<string, any> & Omit<Map<string, any>, keyof Map<any, any>>;
    perfGroupIds: Map<string, {
      groupId: number;
      time: number;
    }> & Omit<Map<string, {
      groupId: number;
      time: number;
    }>, keyof Map<any, any>>;
    rootInstance: _vue_devtools_kit0.VueAppInstance;
    routerId?: string | undefined;
    iframe?: string | undefined;
  }[]>;
  activeAppRecordId: Ref<string, string>;
  timelineLayersState: Ref<Record<string, boolean>, Record<string, boolean>>;
};
declare function useDevToolsState(): DevToolsRefState;
declare function onDevToolsConnected(fn: () => void): () => void;
declare function refreshCurrentPageData(): void;
//#endregion
export { AssetEntry, AssetImporter, AssetInfo, AssetType, CodeSnippet, DevToolsMessagingEvents, ImageMeta, ModuleInfo, RPCFunctions, ViteRPCFunctions, VueDevToolsVuePlugin, createDevToolsStateContext, createViteClientRpc, createViteServerRpc, functions, getDevToolsClientUrl, onDevToolsConnected, onRpcConnected, onRpcSeverReady, onViteRpcConnected, refreshCurrentPageData, rpc, rpcServer, setDevToolsClientUrl, useDevToolsState, viteRpc, viteRpcFunctions };