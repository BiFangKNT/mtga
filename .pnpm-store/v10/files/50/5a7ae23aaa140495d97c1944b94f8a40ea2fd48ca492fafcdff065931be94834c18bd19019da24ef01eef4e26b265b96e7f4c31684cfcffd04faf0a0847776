//#region src/parse.d.ts
interface ParsePathOptions {
  /**
   * File extensions to strip. If omitted, all extensions are stripped.
   */
  extensions?: string[];
  postfix?: string;
  /** Warn about invalid characters in dynamic parameters. */
  warn?: (message: string) => void;
  /**
   * Mode suffixes to detect (e.g. `['client', 'server']`).
   * Detected as `.mode` before the file extension.
   */
  modes?: string[];
  /** Root paths to strip from file paths. Longest match wins. */
  roots?: string[];
}
type SegmentType = 'static' | 'dynamic' | 'optional' | 'catchall' | 'group' | 'repeatable' | 'optional-repeatable';
interface ParsedPathSegmentToken {
  type: SegmentType;
  value: string;
}
type ParsedPathSegment = ParsedPathSegmentToken[];
interface ParsedPath {
  /** Original file path before processing. */
  file: string;
  segments: ParsedPathSegment[];
  meta?: {
    /** Detected modes (e.g. `['client', 'vapor']`). */modes?: string[]; /** Named view from `@name` suffix. */
    name?: string;
  };
}
declare function parsePath(filePaths: string[], options?: ParsePathOptions): ParsedPath[];
/**
 * Pre-compile parsing options for repeated calls.
 *
 * Returns a callable that has the same signature as `parsePath` (minus options)
 * but reuses pre-built regexes and mode lists, avoiding re-compilation on each
 * invocation.
 *
 * @example
 * const parse = compileParsePath({ roots: ['pages/'], modes: ['client', 'server'] })
 * const result = parse(['pages/index.vue'])
 */
interface CompiledParsePath {
  (filePaths: string[]): ParsedPath[];
  /**
   * @internal
   */
  '~compiled': true;
}
declare function compileParsePath(options?: ParsePathOptions): CompiledParsePath;
declare function parseSegment(segment: string, absolutePath?: string, warn?: (message: string) => void): ParsedPathSegmentToken[];
//#endregion
//#region src/tree.d.ts
interface RouteNodeFile {
  /** Original file path (before root stripping / extension removal) */
  'path': string;
  /** Relative path reconstructed from parsed segments (for sorting) */
  'relativePath': string;
  /** Named view slot (`'default'` unless `@name` suffix was used) */
  'viewName': string;
  /** Mode variants (e.g. `['client']`, `['server']`) */
  'modes'?: string[];
  /** Route group names from transparent group segments */
  'groups': string[];
  /** Original parsed segments (including groups) */
  'originalSegments': ParsedPathSegment[];
  /** Layer priority — lower number wins. @default 0 */
  'priority': number;
  /**
   * Precomputed key for duplicate detection
   * @internal
   */
  '~dedupeKey'?: string;
}
/**
 * A node in the route tree.
 *
 * "Page nodes" have files; "structural nodes" don't.
 * Page nodes create nesting boundaries; structural nodes collapse into children.
 */
interface RouteNode {
  rawSegment: string;
  segment: ParsedPathSegment;
  /** Attached files. Empty = structural node. */
  files: RouteNodeFile[];
  children: Map<string, RouteNode>;
  parent: RouteNode | null;
}
/** Input file with optional layer priority. */
interface InputFile {
  path: string;
  /** Layer priority — lower number wins. @default 0 */
  priority?: number;
}
interface BuildTreeOptions extends ParsePathOptions {
  /**
   * How to resolve duplicate files at the same tree position.
   *
   * - `'first-wins'` — keep existing unless the new file has strictly lower
   *   priority number. Equal priority keeps the first.
   * - `'last-wins'` — always replace with the later file.
   * - `'error'` — throw on duplicates.
   *
   * @default 'first-wins'
   */
  duplicateStrategy?: 'first-wins' | 'last-wins' | 'error';
}
interface RouteTree {
  'root': RouteNode;
  /**
   * Whether the tree has been modified since the last converter output.
   * Set to `true` by `addFile` / `removeFile` / `buildTree`.
   * Converters (e.g. `toVueRouter4`) can set this to `false` after caching.
   * @internal
   */
  '~dirty': boolean;
  /**
   * Index from file path to the node that contains it.
   * Enables O(1) lookup for `removeFile`.
   * @internal
   */
  '~fileIndex': Map<string, RouteNode>;
}
/**
 * Build a route tree from file paths.
 *
 * Accepts `string[]`, `InputFile[]`, or `ParsedPath[]`.
 * On collision, the file with the lowest priority number wins.
 */
declare function buildTree(input: string[] | InputFile[] | ParsedPath[], options?: BuildTreeOptions): RouteTree;
/**
 * Add a single file to an existing route tree.
 *
 * Parses the file path and inserts it into the tree in-place, avoiding a full
 * rebuild. Useful for dev-server HMR when a file is added or renamed.
 *
 * The `options` parameter accepts either raw `BuildTreeOptions` or a
 * pre-compiled `CompiledParsePath` (from `compileParsePath()`) for faster
 * repeated calls.
 */
declare function addFile(tree: RouteTree, filePath: string | InputFile, options?: BuildTreeOptions | CompiledParsePath): void;
/**
 * Remove a file from an existing route tree by its original file path.
 *
 * Prunes empty structural nodes left behind. Returns `true` if the file was
 * found and removed.
 */
declare function removeFile(tree: RouteTree, filePath: string): boolean;
/** Walk the tree depth-first, calling `visitor` for each non-root node. */
declare function walkTree(tree: RouteTree, visitor: (node: RouteNode, depth: number, parent: RouteNode | null) => void): void;
/** True if the node has files attached (is a "page node"). */
declare function isPageNode(node: RouteNode): boolean;
//#endregion
//#region src/converters.d.ts
/**
 * Maps an `attrs` record to typed optional properties on the route.
 *
 * Each key becomes an optional property whose value is a single literal
 * from the array. The attr is only set when exactly one mode matches.
 *
 * @example
 * type R = InferAttrs<{ mode: ['client', 'server'] }>
 * // { mode?: 'client' | 'server' }
 */
type InferAttrs<T extends Record<string, string[]>> = { [K in keyof T]?: T[K][number] };
type VueRoute<Attrs extends Record<string, string[]> = {}> = {
  name?: string;
  path: string;
  file?: string; /** Named view files keyed by view name. Only present when named views exist. */
  components?: Record<string, string>;
  modes?: string[];
  children: VueRoute<Attrs>[];
  meta?: Record<string, unknown>;
} & ([keyof Attrs] extends [never] ? {
  [key: string]: unknown;
} : InferAttrs<Attrs>);
interface VueRouterEmitOptions<Attrs extends Record<string, string[]> = {}> {
  /**
   * Custom route name generator.
   * Receives `/`-separated name (e.g. `'users/id'`), returns final name.
   * Default: Nuxt-style — strip trailing `/index`, replace `/` with `-`.
   */
  getRouteName?: (rawName: string) => string;
  /** Called when two routes resolve to the same generated name. */
  onDuplicateRouteName?: (name: string, file: string, existingFile: string) => void;
  /**
   * Collapse modes into single-value attributes.
   *
   * Each key becomes a typed top-level property on the route. When a route has
   * exactly one matching mode the attribute is set to that value string; when
   * none or multiple modes match, the attribute is omitted and the raw `modes`
   * array is emitted instead.
   *
   * The return type of `toVueRouter4` infers typed properties from the attrs
   * definition so that, e.g., `attrs: { mode: ['client', 'server'] }` produces
   * routes with `mode?: 'client' | 'server'`.
   *
   * @example
   * // Input: route has modes: ['server']
   * toVueRouter4(tree, { attrs: { mode: ['client', 'server'] } })
   * // Output: { ..., mode: 'server' }  (no `modes` property)
   *
   * @example
   * // Custom method-based routing
   * toVueRouter4(tree, { attrs: { method: ['get', 'post'] } })
   * // For a route with modes: ['get'] → { ..., method: 'get' }
   */
  attrs?: Attrs;
}
interface Rou3Route {
  path: string;
  file: string;
}
interface RegExpRoute {
  pattern: RegExp;
  keys: string[];
  file: string;
}
/**
 * Convert a route tree to Vue Router 4 route definitions.
 *
 * Results are cached on the tree and deep-cloned on return, so mutations
 * to the returned array do not affect the cache. The cache is automatically
 * invalidated when `addFile` / `removeFile` mark the tree as dirty.
 */
declare function toVueRouter4<const Attrs extends Record<string, string[]> = never>(tree: RouteTree, options?: VueRouterEmitOptions<[Attrs] extends [never] ? {} : Attrs>): VueRoute<[Attrs] extends [never] ? {} : Attrs>[];
declare function toRou3(tree: RouteTree): Rou3Route[];
declare function toRegExp(tree: RouteTree): RegExpRoute[];
interface ToVueRouterSegmentOptions {
  /**
   * Whether there are non-index segments following this one.
   * When `true`, catchall tokens use `([^/]*)*` (restrictive);
   * when `false` (default), they use `(.*)*` (permissive).
   */
  hasSucceeding?: boolean;
}
/**
 * Convert a single parsed segment (an array of tokens returned by
 * `parseSegment`) into a Vue Router 4 path segment string.
 *
 * @example
 * const tokens = parseSegment('[id]')
 * toVueRouterSegment(tokens) // => ':id()'
 */
declare function toVueRouterSegment(tokens: ParsedPathSegmentToken[], options?: ToVueRouterSegmentOptions): string;
/**
 * Convert an array of parsed path segments into a full Vue Router 4 path
 * string. Automatically determines `hasSucceeding` for each segment so that
 * mid-path catchalls use the restrictive `([^/]*)*` pattern.
 *
 * @example
 * const parsed = parsePath(['users/[id].vue'])[0]
 * toVueRouterPath(parsed.segments) // => '/users/:id()'
 */
declare function toVueRouterPath(segments: ParsedPathSegment[]): string;
//#endregion
export { type BuildTreeOptions, type CompiledParsePath, type InferAttrs, type InputFile, type ParsePathOptions, type ParsedPath, type ParsedPathSegment, type ParsedPathSegmentToken, type RegExpRoute, type Rou3Route, type RouteNode, type RouteNodeFile, type RouteTree, type SegmentType, type ToVueRouterSegmentOptions, type VueRoute, type VueRouterEmitOptions, addFile, buildTree, compileParsePath, isPageNode, parsePath, parseSegment, removeFile, toRegExp, toRou3, toVueRouter4, toVueRouterPath, toVueRouterSegment, walkTree };