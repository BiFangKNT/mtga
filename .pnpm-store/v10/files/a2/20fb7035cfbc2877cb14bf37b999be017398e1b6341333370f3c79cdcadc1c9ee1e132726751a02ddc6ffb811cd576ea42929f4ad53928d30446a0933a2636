# image-meta

[![npm version][npm-version-src]][npm-version-href]
[![npm downloads][npm-downloads-src]][npm-downloads-href]
[![bundle][bundle-src]][bundle-href]
[![Codecov][codecov-src]][codecov-href]

Detect image type and size using pure javascript.

## Usage

Install package:

```sh
# npm
npm install image-meta

# yarn
yarn add image-meta

# pnpm
pnpm install image-meta

# bun
bun install image-meta
```

```ts
import { imageMeta } from "image-meta";

const data = await fetch(url).then((res) => res.buffer());

// Meta contains { type, width?, height?, orientation? }
const meta = imageMeta(data);
```

**Note:** `imageMeta` throws an error if either data is not a `Buffer`/`Uint8Array`, or data is invalid or type cannot be determined. You should wrap it into a `try/catch` statement to handle errors.

## Development

- Clone this repository
- Install the latest LTS version of [Node.js](https://nodejs.org/en/)
- Enable [Corepack](https://github.com/nodejs/corepack) using `corepack enable`
- Install dependencies using `pnpm install`
- Run interactive tests using `pnpm dev`

## License

Made with 💛

🔀 Based on [image-size](https://github.com/image-size/image-size) by [Aditya Yadav](https://github.com/netroy) and [contributors](https://github.com/image-size/image-size/graphs/contributors).

Published under [MIT License](./LICENSE).

<!-- Badges -->

[npm-version-src]: https://img.shields.io/npm/v/image-meta?style=flat&colorA=18181B&colorB=F0DB4F
[npm-version-href]: https://npmjs.com/package/image-meta
[npm-downloads-src]: https://img.shields.io/npm/dm/image-meta?style=flat&colorA=18181B&colorB=F0DB4F
[npm-downloads-href]: https://npmjs.com/package/image-meta
[codecov-src]: https://img.shields.io/codecov/c/gh/unjs/image-meta/main?style=flat&colorA=18181B&colorB=F0DB4F
[codecov-href]: https://codecov.io/gh/unjs/image-meta
[bundle-src]: https://img.shields.io/bundlephobia/minzip/image-meta?style=flat&colorA=18181B&colorB=F0DB4F
[bundle-href]: https://bundlephobia.com/result?p=image-meta
