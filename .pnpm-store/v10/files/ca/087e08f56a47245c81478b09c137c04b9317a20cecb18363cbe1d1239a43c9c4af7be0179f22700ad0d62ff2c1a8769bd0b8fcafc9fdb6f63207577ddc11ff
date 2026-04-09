# eslint-merge-processors

[![npm version][npm-version-src]][npm-version-href]
[![npm downloads][npm-downloads-src]][npm-downloads-href]
[![bundle][bundle-src]][bundle-href]
[![JSDocs][jsdocs-src]][jsdocs-href]
[![License][license-src]][license-href]

Merge multiple ESLint processors to behave like one

## Install

```bash
npm i eslint-merge-processors
```

```js
import { mergeProcessors } from 'eslint-merge-processors'

const processor = mergeProcessors([
  processorA,
  processorB,
  // ...
])
```

## Examples

### Markdown

Lint `.md` files with `eslint-plugin-markdown`.

By default, `eslint-plugin-markdown`'s processor will create a virtual file for each code snippet in the markdown file, **but not the original `.md` file itself**. This means the original `.md` file will not be linted.

With this package, along with the `processorPassThrough` processor, you can now fix that:

```ts
import {
  mergeProcessors,
  processorPassThrough
} from 'eslint-merge-processors'
import markdown from 'eslint-plugin-markdown'

// ESlint Flat config
export default [
  {
    files: ['**/*.md'],
    plugins: {
      markdown
    },
    processor: mergeProcessors([
      // This allow the original `.md` file to be linted
      processorPassThrough,
      // The markdown processor
      markdown.processors.markdown,
      // other processors if needed
    ])
  }
]
```

## Sponsors

<p align="center">
  <a href="https://cdn.jsdelivr.net/gh/antfu/static/sponsors.svg">
    <img src='https://cdn.jsdelivr.net/gh/antfu/static/sponsors.svg'/>
  </a>
</p>

## License

[MIT](./LICENSE) License © 2023-PRESENT [Anthony Fu](https://github.com/antfu)

<!-- Badges -->

[npm-version-src]: https://img.shields.io/npm/v/eslint-merge-processors?style=flat&colorA=080f12&colorB=1fa669
[npm-version-href]: https://npmjs.com/package/eslint-merge-processors
[npm-downloads-src]: https://img.shields.io/npm/dm/eslint-merge-processors?style=flat&colorA=080f12&colorB=1fa669
[npm-downloads-href]: https://npmjs.com/package/eslint-merge-processors
[bundle-src]: https://img.shields.io/bundlephobia/minzip/eslint-merge-processors?style=flat&colorA=080f12&colorB=1fa669&label=minzip
[bundle-href]: https://bundlephobia.com/result?p=eslint-merge-processors
[license-src]: https://img.shields.io/github/license/antfu/eslint-merge-processors.svg?style=flat&colorA=080f12&colorB=1fa669
[license-href]: https://github.com/antfu/eslint-merge-processors/blob/main/LICENSE
[jsdocs-src]: https://img.shields.io/badge/jsdocs-reference-080f12?style=flat&colorA=080f12&colorB=1fa669
[jsdocs-href]: https://www.jsdocs.io/package/eslint-merge-processors
