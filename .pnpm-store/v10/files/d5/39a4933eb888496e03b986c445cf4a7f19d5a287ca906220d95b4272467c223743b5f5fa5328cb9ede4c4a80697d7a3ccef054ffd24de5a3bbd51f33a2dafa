# errx

[![npm version][npm-version-src]][npm-version-href]
[![npm downloads][npm-downloads-src]][npm-downloads-href]
[![Github Actions][github-actions-src]][github-actions-href]
[![Codecov][codecov-src]][codecov-href]

> Zero dependency library to capture and parse stack traces in Node, Bun, Deno and more.

## Usage

Install package:

```sh
# npm
npm install errx

# pnpm
pnpm install errx
```

```js
import { captureRawStackTrace, captureStackTrace, parseRawStackTrace } from 'errx'

// returns raw string stack trace
captureRawStackTrace()
// returns parsed stack trace
captureStackTrace()

console.log(captureStackTrace())
// [{
//   function: undefined,
//   source: 'file:///code/danielroe/errx/playground/index.js',
//   line: '5',
//   column: '13'
// }]
```

## 💻 Development

- Clone this repository
- Enable [Corepack](https://github.com/nodejs/corepack) using `corepack enable`
- Install dependencies using `pnpm install`
- Run interactive tests using `pnpm dev`

## License

Made with ❤️

Published under [MIT License](./LICENCE).

<!-- Badges -->

[npm-version-src]: https://img.shields.io/npm/v/errx?style=flat-square
[npm-version-href]: https://npmjs.com/package/errx
[npm-downloads-src]: https://img.shields.io/npm/dm/errx?style=flat-square
[npm-downloads-href]: https://npmjs.com/package/errx
[github-actions-src]: https://img.shields.io/github/workflow/status/danielroe/errx/ci/main?style=flat-square
[github-actions-href]: https://github.com/danielroe/errx/actions?query=workflow%3Aci
[codecov-src]: https://img.shields.io/codecov/c/gh/danielroe/errx/main?style=flat-square
[codecov-href]: https://codecov.io/gh/danielroe/errx
