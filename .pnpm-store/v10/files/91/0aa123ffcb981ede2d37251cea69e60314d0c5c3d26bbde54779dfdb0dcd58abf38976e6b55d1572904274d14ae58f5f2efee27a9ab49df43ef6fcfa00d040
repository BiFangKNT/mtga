# 🌳 rou3

<!-- automd:badges codecov bundlejs -->

[![npm version](https://img.shields.io/npm/v/rou3)](https://npmjs.com/package/rou3)
[![npm downloads](https://img.shields.io/npm/dm/rou3)](https://npm.chart.dev/rou3)
[![bundle size](https://img.shields.io/bundlejs/size/rou3)](https://bundlejs.com/?q=rou3)
[![codecov](https://img.shields.io/codecov/c/gh/h3js/rou3)](https://codecov.io/gh/h3js/rou3)

<!-- /automd -->

Lightweight and fast router for JavaScript.

## Usage

**Install:**

```sh
# ✨ Auto-detect
npx nypm install rou3
```

**Import:**

<!-- automd:jsimport cdn src="./src/index.ts"-->

**ESM** (Node.js, Bun, Deno)

```js
import {
  createRouter,
  addRoute,
  findRoute,
  removeRoute,
  findAllRoutes,
  routeToRegExp,
  NullProtoObj,
} from "rou3";
```

**CDN** (Deno and Browsers)

```js
import {
  createRouter,
  addRoute,
  findRoute,
  removeRoute,
  findAllRoutes,
  routeToRegExp,
  NullProtoObj,
} from "https://esm.sh/rou3";
```

<!-- /automd -->

**Create a router instance and insert routes:**

```js
import { createRouter, addRoute } from "rou3";

const router = createRouter(/* options */);

addRoute(router, "GET", "/path", { payload: "this path" });
addRoute(router, "POST", "/path/:name", { payload: "named route" });
addRoute(router, "GET", "/path/foo/**", { payload: "wildcard route" });
addRoute(router, "GET", "/path/foo/**:name", {
  payload: "named wildcard route",
});
```

**Match route to access matched data:**

```js
// Returns { payload: 'this path' }
findRoute(router, "GET", "/path");

// Returns { payload: 'named route', params: { name: 'fooval' } }
findRoute(router, "POST", "/path/fooval");

// Returns { payload: 'wildcard route' }
findRoute(router, "GET", "/path/foo/bar/baz");

// Returns undefined (no route matched for/)
findRoute(router, "GET", "/");
```

> [!IMPORTANT]
> Paths should **always begin with `/`**.

> [!IMPORTANT]
> Method should **always be UPPERCASE**.

> [!TIP]
> If you need to register a pattern containing literal `:` or `*`, you can escape them with `\\`. For example, `/static\\:path/\\*\\*` matches only the static `/static:path/**` route.

## Route Patterns

rou3 supports [URLPattern](https://developer.mozilla.org/en-US/docs/Web/API/URL_Pattern_API)-compatible syntax.

| Pattern                     | Example Match                      | Params                                               |
| --------------------------- | ---------------------------------- | ---------------------------------------------------- |
| `/path/to/resource`         | `/path/to/resource`                | `{}`                                                 |
| `/users/:name`              | `/users/foo`                       | `{ name: "foo" }`                                    |
| `/path/**`                  | `/path/foo/bar`                    | `{}`                                                 |
| `/path/**:rest`             | `/path/foo/bar`                    | `{ rest: "foo/bar" }`                                |
| `/files/*.png`              | `/files/icon.png`                  | `{ "0": "icon" }`                                    |
| `/files/file-*-*.png`       | `/files/file-a-b.png`              | `{ "0": "a", "1": "b" }`                             |
| `/users/:id(\\d+)`          | `/users/123`                       | `{ id: "123" }`                                      |
| `/files/:ext(png\|jpg)`     | `/files/png`                       | `{ ext: "png" }`                                     |
| `/path/(\\d+)`              | `/path/123`                        | `{ "0": "123" }`                                     |
| `/users/:id?`               | `/users` or `/users/123`           | `{}` or `{ id: "123" }`                              |
| `/files/:path+`             | `/files/a/b/c`                     | `{ path: "a/b/c" }`                                  |
| `/files/:path*`             | `/files` or `/files/a/b`           | `{}` or `{ path: "a/b" }`                            |
| `/book{s}?`                 | `/book` or `/books`                | `{}`                                                 |
| `/blog/:id(\\d+){-:title}?` | `/blog/123` or `/blog/123-my-post` | `{ id: "123" }` or `{ id: "123", title: "my-post" }` |

- **Named params** (`:name`) match a single segment.
- **Single-segment wildcards** (`*`) capture unnamed params (`0`, `1`, ...) and can be used as full or mid-segment tokens (for example `/*` or `/*.png`).
- **Wildcards** (`**`) match zero or more segments. Use `**:name` to capture.
- **Regex constraints** (`:name(regex)`) restrict matching. Constrained and unconstrained params can coexist on the same node (constrained checked first).
- **Unnamed groups** (`(regex)`) capture into auto-indexed keys `0`, `1`, etc.
- **Modifiers:** `:name?` (optional), `:name+` (one or more), `:name*` (zero or more). Can combine with regex: `:id(\d+)?`.
- **Non-capturing groups** (`{...}`): supported with inline (`/foo{bar}`) and optional (`/foo{bar}?`) forms.
- **Current limitation:** repeating non-capturing groups (`{...}+`, `{...}*`) are supported only within a single segment (no `/` inside the group body).
- **Backslash escaping** (`\`): escape special characters like `:`, `*`, `(`, `)`, `{`, `}` with a backslash (e.g., `/static\:path` matches literal `/static:path`).

### Differences from URLPattern

rou3 aims for URLPattern-compatible syntax but has intentional differences due to its radix-tree design:

| Feature                       | URLPattern                         | rou3                                                          |
| ----------------------------- | ---------------------------------- | ------------------------------------------------------------- |
| `*` (single star)             | Greedy catch-all `(.*)` across `/` | Single-segment unnamed param `([^/]*)`                        |
| `**` (double star)            | Literal `**`                       | Catch-all wildcard (zero or more segments)                    |
| `(.*)` in segment             | Greedy match across `/`            | Segment-scoped (does not cross `/`)                           |
| `{...}+` / `{...}*` groups    | Cross-segment group repetition     | Only supported within a single segment (no `/` in group body) |
| Path normalization (`.`/`..`) | Resolves `.`/`..` in input paths   | Not done by default (opt-in with `{ normalize: true }`)       |
| Case sensitivity              | Can be case-insensitive            | Always case-sensitive                                         |
| Non-`/`-prefixed paths        | Supported                          | Paths must start with `/`                                     |
| Unicode param names           | Supports Unicode identifiers       | Params use `\w` (ASCII word chars only)                       |
| Percent-encoding              | Normalizes `%xx` sequences         | Does not decode percent-encoded input                         |

### Path normalization

By default, `findRoute` and `findAllRoutes` do **not** resolve `.`/`..` segments in input paths. If your input paths may contain relative segments, enable normalization:

```js
findRoute(router, "GET", "/foo/bar/../baz", { normalize: true });
// Matches "/foo/baz"

findAllRoutes(router, "GET", "/foo/./bar", { normalize: true });
// Matches "/foo/bar"
```

The compiled router also supports this via the `normalize` option:

```js
const match = compileRouter(router, { normalize: true });
match("GET", "/foo/bar/../baz"); // Matches "/foo/baz"
```

## Compiler

<!-- automd:jsdocs src="./src/compiler.ts" -->

### `compileRouter(router, opts?)`

Compiles the router instance into a faster route-matching function.

**IMPORTANT:** `compileRouter` requires eval support with `new Function()` in the runtime for JIT compilation.

**Example:**

```ts
import { createRouter, addRoute } from "rou3";
import { compileRouter } from "rou3/compiler";
const router = createRouter();
// [add some routes]
const findRoute = compileRouter(router);
const matchAll = compileRouter(router, { matchAll: true });
findRoute("GET", "/path/foo/bar");
```

### `compileRouterToString(router, functionName?, opts?)`

Compile the router instance into a compact runnable code.

**IMPORTANT:** Route data must be serializable to JSON (i.e., no functions or classes) or implement the `toJSON()` method to render custom code or you can pass custom `serialize` function in options.

**Example:**

```ts
import { createRouter, addRoute } from "rou3";
import { compileRouterToString } from "rou3/compiler";
const router = createRouter();
// [add some routes with serializable data]
const compilerCode = compileRouterToString(router, "findRoute");
// "const findRoute=(m, p) => {}"
```

<!--/automd -->

## License

<!-- automd:contributors license=MIT author="pi0" -->

Published under the [MIT](https://github.com/h3js/rou3/blob/main/LICENSE) license.
Made by [@pi0](https://github.com/pi0) and [community](https://github.com/h3js/rou3/graphs/contributors) 💛
<br><br>
<a href="https://github.com/h3js/rou3/graphs/contributors">
<img src="https://contrib.rocks/image?repo=h3js/rou3" />
</a>

<!-- /automd -->

<!-- automd:with-automd -->

---

_🤖 auto updated with [automd](https://automd.unjs.io)_

<!-- /automd -->
