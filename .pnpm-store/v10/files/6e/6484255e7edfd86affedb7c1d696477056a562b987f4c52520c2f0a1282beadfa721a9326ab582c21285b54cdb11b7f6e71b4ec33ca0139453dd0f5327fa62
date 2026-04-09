# λ srvx

<!-- automd:badges color=yellow packagephobia -->

[![npm version](https://img.shields.io/npm/v/srvx?color=yellow)](https://npmjs.com/package/srvx)
[![npm downloads](https://img.shields.io/npm/dm/srvx?color=yellow)](https://npm.chart.dev/srvx)
[![install size](https://badgen.net/packagephobia/install/srvx?color=yellow)](https://packagephobia.com/result?p=srvx)

<!-- /automd -->

Universal Server based on web standards. Works with [Deno](https://deno.com/), [Bun](https://bun.sh/) and [Node.js](https://nodejs.org/en).

- ✅ Zero dependency
- ✅ Full featured CLI with watcher, error handler, serve static and logger
- ✅ Seamless runtime integration with same API ([handler](https://srvx.h3.dev/guide/handler) and [instance](https://srvx.h3.dev/guide/server)).
- ✅ [Node.js compatibility](https://srvx.h3.dev/guide/node) with a [**close to native performance**](https://github.com/h3js/srvx/tree/main/test/bench-node).
- ✅ Zero overhead [Deno](https://deno.com/) and [Bun](https://bun.sh/) support.

## Quick start

```js
export default {
  fetch(req: Request) {
    return Response.json({ hello: "world!" });
  },
};
```

Then, run the server using your favorite runtime:

```bash
# Node.js
$ npx srvx       # npm
$ pnpx srvx      # pnpm
$ yarn dlx srvx  # yarn

# Deno
$ deno -A npm:srvx

# Bun
$ bunx --bun srvx
```

You can also use `srvx fetch` to directly call your server handler without starting a server:

```bash
$ npx srvx fetch /api/users
```

See [CLI documentation](https://srvx.h3.dev/guide/cli) for more options.

👉 **Visit the 📖 [Documentation](https://srvx.h3.dev/) to learn more.**

## Contribution

- Clone this repository
- Install the latest LTS version of [Node.js](https://nodejs.org/en/)
- Enable [Corepack](https://github.com/nodejs/corepack) using `corepack enable`
- Install dependencies using `pnpm install`
- **Prepare stub mode using `pnpm build --stub`**
- Run interactive tests using `pnpm dev`

## License

<!-- automd:contributors author=pi0 license=MIT -->

Published under the [MIT](https://github.com/h3js/srvx/blob/main/LICENSE) license.
Made by [@pi0](https://github.com/pi0) and [community](https://github.com/h3js/srvx/graphs/contributors) 💛
<br><br>
<a href="https://github.com/h3js/srvx/graphs/contributors">
<img src="https://contrib.rocks/image?repo=h3js/srvx" />
</a>

<!-- /automd -->

<!-- automd:with-automd -->

---

_🤖 auto updated with [automd](https://automd.unjs.io)_

<!-- /automd -->
