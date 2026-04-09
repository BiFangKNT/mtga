# 📍 unrouting

[![npm version][npm-version-src]][npm-version-href]
[![npm downloads][npm-downloads-src]][npm-downloads-href]
[![bundle][bundle-src]][bundle-href]
[![Codecov][codecov-src]][codecov-href]
[![License][license-src]][license-href]
[![JSDocs][jsdocs-src]][jsdocs-href]

> Universal filesystem routing

`unrouting` parses file paths into a route tree and emits route definitions for any framework router. It handles nested routes, dynamic params, catchalls, optional segments, route groups, layer merging, and more – as a standalone, framework-agnostic library.

## Status

In active development. The core pipeline (parse, tree, emit) is functional and used by Nuxt.

- [x] Generic route parsing covering major filesystem routing patterns
  - [x] [Nuxt](https://github.com/nuxt/nuxt) / [unplugin-vue-router](https://github.com/posva/unplugin-vue-router)
  - [ ] [SvelteKit](https://kit.svelte.dev/docs/routing)
  - [ ] [Next.js](https://nextjs.org/docs/app/building-your-application/routing)
- [x] Route tree with nesting, layer merging, group transparency
- [x] Layer priority (multiple roots with configurable file precedence)
- [x] Incremental tree updates (`addFile`/`removeFile` for dev server HMR)
- [x] Pluggable route name generation
- [x] Route ordering by segment priority (static > dynamic > optional > catchall)
- [x] Named view support (`@viewName` convention)
- [x] Mode variant support (`.client`, `.server`, configurable)
- [x] Duplicate route name detection
- [x] Emit to framework routers
  - [x] [`vue-router`](https://router.vuejs.org/) (nested routes, names, files, children, meta, components, modes)
  - [x] [rou3](http://github.com/h3js/rou3)/[Nitro](https://nitro.unjs.io/)
  - [x] RegExp patterns
  - [ ] [SolidStart](https://start.solidjs.com/core-concepts/routing)
  - [ ] [SvelteKit](https://kit.svelte.dev/docs/routing)

## Install

```sh
# npm
npm install unrouting

# pnpm
pnpm install unrouting
```

## Usage

The library has a three-phase pipeline: **parse** file paths into tokens, **build** a route tree, and **emit** to a target format. For most use cases you only need two function calls.

### Quick start

```js
import { buildTree, toVueRouter4 } from 'unrouting'

const tree = buildTree([
  'pages/index.vue',
  'pages/about.vue',
  'pages/users/[id].vue',
  'pages/users.vue',
  'pages/[...slug].vue',
], { roots: ['pages/'] })

const routes = toVueRouter4(tree)
// [
//   { name: 'index', path: '/', file: 'pages/index.vue', children: [] },
//   { name: 'about', path: '/about', file: 'pages/about.vue', children: [] },
//   { name: 'users', path: '/users', file: 'pages/users.vue', children: [
//     { name: 'users-id', path: ':id()', file: 'pages/users/[id].vue', children: [] },
//   ]},
//   { name: 'slug', path: '/:slug(.*)*', file: 'pages/[...slug].vue', children: [] },
// ]
```

### Nuxt-like usage with layers

```js
import { buildTree, toVueRouter4 } from 'unrouting'

// Files from app + layer directories with priority
const tree = buildTree([
  { path: 'pages/index.vue', priority: 0 }, // app layer (wins on collision)
  { path: 'pages/dashboard.vue', priority: 0 },
  { path: 'pages/dashboard/settings.vue', priority: 0 },
  { path: 'layer/pages/dashboard/analytics.vue', priority: 1 }, // extending layer
  { path: 'layer/pages/index.vue', priority: 1 }, // overridden by app layer
], {
  roots: ['pages/', 'layer/pages/'],
  extensions: ['.vue'],
  modes: ['client', 'server'],
  warn: msg => console.warn(msg),
})

const routes = toVueRouter4(tree, {
  onDuplicateRouteName: (name, file, existingFile) => {
    console.warn(`Duplicate route name "${name}": ${file} and ${existingFile}`)
  },
})
```

### Emitting to different formats

All emitters accept a `RouteTree`:

```js
import { buildTree, toRegExp, toRou3, toVueRouter4 } from 'unrouting'

const tree = buildTree(['users/[id]/posts/[slug].vue'])

// Vue Router 4 – nested routes with names, files, children
const vueRoutes = toVueRouter4(tree)
// [{ name: 'users-id-posts-slug', path: '/users/:id()/posts/:slug()', file: '...', children: [] }]

// rou3/Nitro – flat route patterns
const rou3Routes = toRou3(tree)
// [{ path: '/users/:id/posts/:slug', file: '...' }]

// RegExp – matcher patterns with named groups
const regexpRoutes = toRegExp(tree)
// [{ pattern: /^\/users\/(?<id>[^/]+)\/posts\/(?<slug>[^/]+)\/?$/, keys: ['id', 'slug'], file: '...' }]
```

### Incremental updates (dev server)

The route tree is mutable. Instead of rebuilding everything when a file changes, use `addFile` and `removeFile` to update the tree in place – avoiding the cost of re-parsing all files and reconstructing the tree from scratch on every change.

```js
import { addFile, buildTree, removeFile, toVueRouter4 } from 'unrouting'

const opts = { roots: ['pages/'], extensions: ['.vue'] }

// Build once at startup
const tree = buildTree(initialFiles, opts)
let routes = toVueRouter4(tree)

// On file add/remove (e.g., from a watcher callback)
addFile(tree, 'pages/new-page.vue', opts)
routes = toVueRouter4(tree)

removeFile(tree, 'pages/old-page.vue')
routes = toVueRouter4(tree)

// Rename = remove + add
removeFile(tree, 'pages/old-name.vue')
addFile(tree, 'pages/new-name.vue', opts)
routes = toVueRouter4(tree)
```

`addFile` supports the same `InputFile` format as `buildTree` for layer priority:

```js
addFile(tree, { path: 'layer/pages/about.vue', priority: 1 }, opts)
```

### Standalone parsing and segment conversion

If you don't need the full tree pipeline – e.g., you already have resolved routes and only need to convert individual path segments or strings to Vue Router syntax – you can use the parse + convert functions directly:

```js
import { parsePath, parseSegment, toVueRouterPath, toVueRouterSegment } from 'unrouting'

// Parse a full file path
const [result] = parsePath(['users/[id]/profile.vue'])
// {
//   file: 'users/[id]/profile.vue',
//   segments: [
//     [{ type: 'static', value: 'users' }],
//     [{ type: 'dynamic', value: 'id' }],
//     [{ type: 'static', value: 'profile' }],
//   ],
// }

// Convert parsed segments to a Vue Router path
toVueRouterPath(result.segments) // => '/users/:id()/profile'

// Parse and convert a single segment (e.g., i18n per-locale route path)
const tokens = parseSegment('[...slug]')
// [{ type: 'catchall', value: 'slug' }]
toVueRouterSegment(tokens) // => ':slug(.*)*'
```

## Supported patterns

| Pattern | Example | Description |
|---|---|---|
| Static | `about.vue` | Static route segment |
| Index | `index.vue` | Index page (maps to `/`) |
| Dynamic | `[slug].vue` | Required parameter |
| Optional | `[[slug]].vue` | Optional parameter |
| Catchall | `[...slug].vue` | Catch-all (zero or more segments) |
| Repeatable | `[slug]+.vue` | One or more segments |
| Optional repeatable | `[[slug]]+.vue` | Zero or more segments |
| Group | `(admin)/dashboard.vue` | Route group (transparent to path, stored in meta) |
| Mixed | `prefix-[slug]-suffix.vue` | Static and dynamic in one segment |
| Nested | `parent.vue` + `parent/child.vue` | Parent layout with child routes |
| Named views | `index@sidebar.vue` | Vue Router named view slots |
| Modes | `page.client.vue` | Mode variants (configurable suffixes) |

## API

### `buildTree(input, options?)`

Build a route tree from file paths. Accepts raw strings, `InputFile[]` (with priority), or pre-parsed `ParsedPath[]`.

```ts
function buildTree(
  input: string[] | InputFile[] | ParsedPath[],
  options?: BuildTreeOptions
): RouteTree

interface InputFile {
  path: string
  /** Lower number = higher priority. Default: 0 */
  priority?: number
}
```

**Options** (extends `ParsePathOptions`):

| Option | Type | Description |
|---|---|---|
| `roots` | `string[]` | Root paths to strip (e.g., `['pages/', 'layer/pages/']`) |
| `extensions` | `string[]` | File extensions to strip (default: strip all) |
| `modes` | `string[]` | Mode suffixes to detect (e.g., `['client', 'server']`) |
| `warn` | `(msg: string) => void` | Warning callback for invalid characters in dynamic params |
| `duplicateStrategy` | `'first-wins' \| 'last-wins' \| 'error'` | How to handle duplicate paths (default: `'first-wins'`) |

When files from different layers collide at the same tree position, the file with the lowest `priority` number wins regardless of insertion order.

### `addFile(tree, filePath, options?)`

Add a single file to an existing route tree in place. Parses the file and inserts it, avoiding a full rebuild. Accepts a plain string or `InputFile` with priority.

```ts
function addFile(
  tree: RouteTree,
  filePath: string | InputFile,
  options?: BuildTreeOptions
): void
```

### `removeFile(tree, filePath)`

Remove a file from an existing route tree by its original file path. Prunes empty structural nodes left behind. Returns `true` if the file was found and removed.

```ts
function removeFile(tree: RouteTree, filePath: string): boolean
```

### `toVueRouter4(tree, options?)`

Emit Vue Router 4 route definitions from a tree. Handles nested routes, names, index promotion, structural collapse, groups, catchall optimisation, route ordering, named views, and mode variants.

```ts
function toVueRouter4(tree: RouteTree, options?: VueRouterEmitOptions): VueRoute[]

interface VueRoute {
  name?: string
  path: string
  file?: string
  /** Named view components. Only present when multiple views exist. */
  components?: Record<string, string>
  /** Mode variants. Only present when mode files exist. */
  modes?: string[]
  children: VueRoute[]
  meta?: Record<string, unknown>
}

interface VueRouterEmitOptions {
  /** Custom name generator. Receives raw `/`-separated name, returns final name. */
  getRouteName?: (rawName: string) => string
  /** Called when two routes produce the same name. */
  onDuplicateRouteName?: (name: string, file: string, existingFile: string) => void
}
```

Routes are sorted by segment priority within each level: static segments first, then dynamic, optional, and catchall last.

### `toRou3(tree)`

Emit rou3/Nitro route patterns from a tree.

```ts
function toRou3(tree: RouteTree): Rou3Route[]

interface Rou3Route {
  path: string
  file: string
}
```

### `toRegExp(tree)`

Emit RegExp matchers from a tree.

```ts
function toRegExp(tree: RouteTree): RegExpRoute[]

interface RegExpRoute {
  pattern: RegExp
  keys: string[]
  file: string
}
```

### `toVueRouterSegment(tokens, options?)`

Convert a single parsed segment (an array of tokens returned by `parseSegment`) into a Vue Router 4 path segment string. Useful for modules that already have resolved routes and only need segment-level path conversion (e.g., `@nuxtjs/i18n` converting per-locale custom paths).

```ts
function toVueRouterSegment(
  tokens: ParsedPathSegmentToken[],
  options?: ToVueRouterSegmentOptions
): string

interface ToVueRouterSegmentOptions {
  /**
   * Whether non-index segments follow this one.
   * When true, catchall uses ([^/]*)*; when false (default), uses (.*)*
   */
  hasSucceeding?: boolean
}
```

```js
import { parseSegment, toVueRouterSegment } from 'unrouting'

toVueRouterSegment(parseSegment('[id]')) // => ':id()'
toVueRouterSegment(parseSegment('[[opt]]')) // => ':opt?'
toVueRouterSegment(parseSegment('[...slug]')) // => ':slug(.*)*'
toVueRouterSegment(parseSegment('prefix-[slug]')) // => 'prefix-:slug()'

// i18n use case – parse a custom locale path segment
const tokens = parseSegment('[foo]_[bar]:[...buz]_buz_[[qux]]')
const path = `/${toVueRouterSegment(tokens)}`
// => '/:foo()_:bar()\::buz(.*)*_buz_:qux?'
```

### `toVueRouterPath(segments)`

Convert an array of parsed path segments into a full Vue Router 4 path string. Automatically determines `hasSucceeding` per segment so that mid-path catchalls use the restrictive `([^/]*)*` pattern and terminal catchalls use `(.*)*`.

```ts
function toVueRouterPath(segments: ParsedPathSegment[]): string
```

```js
import { parsePath, toVueRouterPath } from 'unrouting'

toVueRouterPath(parsePath(['users/[id]/posts.vue'])[0].segments)
// => '/users/:id()/posts'

toVueRouterPath(parsePath(['[...slug]/suffix.vue'])[0].segments)
// => '/:slug([^/]*)*/suffix'  (mid-path catchall auto-detected)

toVueRouterPath(parsePath(['prefix/[...slug].vue'])[0].segments)
// => '/prefix/:slug(.*)*'     (terminal catchall)
```

### `parsePath(filePaths, options?)`

Parse file paths into segments. Standalone – does not build a tree.

```ts
function parsePath(filePaths: string[], options?: ParsePathOptions): ParsedPath[]

interface ParsedPath {
  file: string
  segments: ParsedPathSegment[]
  meta?: { modes?: string[], name?: string }
}
```

### `compileParsePath(options?)`

Pre-compile parsing options into a reusable function. Useful in hot paths (e.g., dev server file watchers) where `parsePath` would otherwise reconstruct the same regexes on every call.

```ts
function compileParsePath(options?: ParsePathOptions): CompiledParsePath

interface CompiledParsePath {
  (filePaths: string[]): ParsedPath[]
}
```

Returns a callable with the same signature as `parsePath` (minus the options argument). The regexes for root stripping, extension matching, and mode detection are built once at compile time.

```js
import { addFile, buildTree, compileParsePath, toVueRouter4 } from 'unrouting'

const opts = { roots: ['pages/'], modes: ['client', 'server'] }

// Compile once at startup
const parse = compileParsePath(opts)
const tree = buildTree(initialFiles, opts)

// In a file watcher callback — no regex re-compilation
addFile(tree, 'pages/new-page.vue', parse)
const routes = toVueRouter4(tree)
```

The compiled function can be passed directly to `addFile` as the options argument:

```js
// These are equivalent, but the compiled version avoids re-building regexes:
addFile(tree, file, parse) // pre-compiled (fast)
addFile(tree, file, opts) // raw options (re-compiles each call)
```

### `parseSegment(segment, absolutePath?, warn?)`

Parse a single filesystem segment into typed tokens. Useful for modules that need to parse custom paths (e.g., i18n locale-specific routes).

```ts
function parseSegment(
  segment: string,
  absolutePath?: string,
  warn?: (message: string) => void
): ParsedPathSegmentToken[]

// Token types: 'static' | 'dynamic' | 'optional' | 'catchall' |
//              'repeatable' | 'optional-repeatable' | 'group'
```

### `walkTree(tree, visitor)`

Walk all nodes depth-first.

```ts
function walkTree(
  tree: RouteTree,
  visitor: (node: RouteNode, depth: number, parent: RouteNode | null) => void
): void
```

### `isPageNode(node)`

Check if a node has files attached (page node vs structural node).

```ts
function isPageNode(node: RouteNode): boolean
```

## How nesting works

The tree distinguishes between **page nodes** (have files) and **structural nodes** (directory-only, no files):

- **Page nodes** create nesting boundaries – children get relative paths
- **Structural nodes** collapse – their path segment is prepended to descendants

```text
parent.vue + parent/child.vue
  → { path: '/parent', children: [{ path: 'child' }] }

parent/child.vue  (no parent.vue)
  → { path: '/parent/child' }  (structural 'parent' collapses)
```

`index.vue` promotes a structural directory into a page node:

```text
users/index.vue + users/[id].vue
  → { path: '/users', file: 'users/index.vue', children: [{ path: ':id()' }] }
```

Route groups `(name)` are transparent – they don't affect paths or nesting, but are stored in `meta.groups`.

## Development

- Clone this repository
- Enable [Corepack](https://github.com/nodejs/corepack) using `corepack enable`
- Install dependencies using `pnpm install`
- Run interactive tests using `pnpm dev`

## License

Made with ❤️

Published under [MIT License](./LICENCE).

<!-- Badges -->

[npm-version-src]: https://npmx.dev/api/registry/badge/version/unrouting
[npm-version-href]: https://npmx.dev/package/unrouting
[npm-downloads-src]: https://npmx.dev/api/registry/badge/downloads/unrouting
[npm-downloads-href]: https://npmx.dev/package/unrouting
[codecov-src]: https://img.shields.io/codecov/c/gh/unjs/unrouting/main?style=flat&colorA=18181B&colorB=F0DB4F
[codecov-href]: https://codecov.io/gh/unjs/unrouting
[bundle-src]: https://img.shields.io/bundlephobia/minzip/unrouting?style=flat&colorA=18181B&colorB=F0DB4F
[bundle-href]: https://bundlephobia.com/result?p=unrouting
[license-src]: https://img.shields.io/github/license/unjs/unrouting.svg?style=flat&colorA=18181B&colorB=F0DB4F
[license-href]: https://github.com/unjs/unrouting/blob/main/LICENSE
[jsdocs-src]: https://img.shields.io/badge/jsDocs.io-reference-18181B?style=flat&colorA=18181B&colorB=F0DB4F
[jsdocs-href]: https://www.jsdocs.io/package/unrouting
