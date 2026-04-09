# impound

[![npm version][npm-version-src]][npm-version-href]
[![npm downloads][npm-downloads-src]][npm-downloads-href]
[![Github Actions][github-actions-src]][github-actions-href]
[![Codecov][codecov-src]][codecov-href]

> Build plugin to restrict import patterns in certain parts of your code-base.

This package is an [unplugin](https://unplugin.unjs.io/) which provides support for a wide range of bundlers.

## Usage

Install package:

```sh
# npm
npm install impound
```

```js
// rollup.config.js
import { dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { ImpoundPlugin } from 'impound'

export default {
  plugins: [
    ImpoundPlugin.rollup({
      cwd: dirname(fileURLToPath(import.meta.url)),
      include: [/src\/*/],
      patterns: [
        [/^node:.*/], // disallows all node imports
        ['@nuxt/kit', 'Importing from @nuxt/kit is not allowed in your src/ directory'], // custom error message
        [(id, importer) => id.endsWith('.server') && `Server-only import in ${importer}`] // functional pattern with importer context
      ]
    }),
  ],
}
```

### Import Tracing

Enable `trace: true` to get rich violation diagnostics with full import chains and code snippets. When enabled, errors are deferred to `buildEnd` so the complete module graph can be collected first.

```js
ImpoundPlugin.rollup({
  cwd: dirname(fileURLToPath(import.meta.url)),
  trace: true,
  patterns: [
    [/\.server$/, 'Server-only import', ['Use a server function instead', 'Move this import to a .server.ts file']]
  ]
})
```

Example output:

```text
Invalid import [importing `secret` from `middle.js`]

Trace:
  1. src/routes/index.tsx:2:34 (entry) (import "../features/auth/session")
  2. src/features/auth/session.ts

Code:
  1 | import { logger } from '../utils/logger'
  2 |
> 3 | import { getUsers } from '../db/queries.server'
    |                           ^
  4 |
  5 | export function loadAuth() {

Suggestions:
  - Use a server function instead
  - Move this import to a .server.ts file
```

## 💻 Development

- Clone this repository
- Enable [Corepack](https://github.com/nodejs/corepack) using `corepack enable`
- Install dependencies using `pnpm install`
- Run interactive tests using `pnpm dev`

## Acknowledgements

Some features in impound were inspired by [TanStack Start's import protection](https://tanstack.com/start/latest/docs/framework/react/guide/import-protection).

## License

Made with ❤️

Published under [MIT License](./LICENCE).

<!-- Badges -->

[npm-version-src]: https://npmx.dev/api/registry/badge/version/impound
[npm-version-href]: https://npmx.dev/package/impound
[npm-downloads-src]: https://npmx.dev/api/registry/badge/downloads/impound
[npm-downloads-href]: https://npm.chart.dev/impound
[github-actions-src]: https://img.shields.io/github/actions/workflow/status/unjs/impound/ci.yml?branch=main&style=flat-square
[github-actions-href]: https://github.com/unjs/impound/actions?query=workflow%3Aci
[codecov-src]: https://img.shields.io/codecov/c/gh/unjs/impound/main?style=flat-square
[codecov-href]: https://codecov.io/gh/unjs/impound
