# mocked-exports

<!-- automd:badges codecov color=yellow -->

[![npm version](https://img.shields.io/npm/v/mocked-exports?color=yellow)](https://npmjs.com/package/mocked-exports)
[![npm downloads](https://img.shields.io/npm/dm/mocked-exports?color=yellow)](https://npm.chart.dev/mocked-exports)
[![codecov](https://img.shields.io/codecov/c/gh/unjs/mocked-exports?color=yellow)](https://codecov.io/gh/unjs/mocked-exports)

<!-- /automd -->

Simple mocks (extracted from [unjs/unenv](https://github.com/unjs/unenv.git)).

Main usage of `mocked-exports` is to use them as **bundler aliases** to mock specific modules you don't want to end-up into your bundle.

```js
// Exports a dynamic mock proxy function
const proxy = require("mocked-exports/proxy");
import proxy from "mocked-exports/proxy";
import proxy from "mocked-exports/proxy/foo/bar/baz";

// Exports a no-op frozen function
const noop = require("mocked-exports/noop");
import noop from "mocked-exports/noop";

// Exports an empty frozen object
const empty = require("mocked-exports/empty");
import empty from "mocked-exports/empty";
```

There are also extra variants of exports with `-mjs` or `-cjs` suffixes available if your mocking needs to force a specific format.

## Magic proxy

The `proxy` mock, is a nested deep proxy that tries to replace any dynamic nested access to an unknown object.

Examples: `proxy.foo.bar().xyz[1].then(() => {});`

For better debugging, you can use `proxy.__mock__('name')` to create a named instance.

## Development

<details>

<summary>local development</summary>

- Clone this repository
- Install latest LTS version of [Node.js](https://nodejs.org/en/)
- Enable [Corepack](https://github.com/nodejs/corepack) using `corepack enable`
- Install dependencies using `pnpm install`
- Run interactive tests using `pnpm dev`

</details>

## License

<!-- automd:contributors license=MIT -->

Published under the [MIT](https://github.com/unjs/mocked-exports/blob/main/LICENSE) license.
Made by [community](https://github.com/unjs/mocked-exports/graphs/contributors) 💛
<br><br>
<a href="https://github.com/unjs/mocked-exports/graphs/contributors">
<img src="https://contrib.rocks/image?repo=unjs/mocked-exports" />
</a>

<!-- /automd -->

<!-- automd:with-automd -->

---

_🤖 auto updated with [automd](https://automd.unjs.io)_

<!-- /automd -->
