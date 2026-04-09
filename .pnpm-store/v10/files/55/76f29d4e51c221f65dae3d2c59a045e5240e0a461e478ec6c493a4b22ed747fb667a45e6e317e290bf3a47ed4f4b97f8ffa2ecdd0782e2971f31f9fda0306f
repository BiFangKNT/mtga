# eslint-processor-vue-blocks

[![npm version][npm-version-src]][npm-version-href]
[![npm downloads][npm-downloads-src]][npm-downloads-href]
[![bundle][bundle-src]][bundle-href]
[![JSDocs][jsdocs-src]][jsdocs-href]
[![License][license-src]][license-href]

Create virtual files in ESLint for each Vue SFC block, so that you can lint them individually.

## Install

```bash
npm i -D eslint-processor-vue-blocks eslint-merge-processors
```

## Usage

In ESLint flat config:

```js
// eslint.config.js
import { mergeProcessors } from 'eslint-merge-processors'
import pluginVue from 'eslint-plugin-vue'
import processorVueBlocks from 'eslint-processor-vue-blocks'

export default [
  {
    files: ['*/*.vue'],
    plugins: {
      vue: pluginVue,
    },
    // `eslint-plugin-vue` will set a default processor for `.vue` files
    // we use `eslint-merge-processors` to extend it
    processor: mergeProcessors([
      pluginVue.processors['.vue'],
      processorVueBlocks({
        blocks: {
          styles: true,
          customBlocks: true,
          // Usually it's not recommended to lint <script> and <template>
          // As eslint-plugin-vue already provides the support
          script: false,
          template: false,
        }
      }),
    ]),
    rules: {
      // ...
    }
  },
  {
    files: ['**/*.css'],
    // ... now you can lint CSS files as well as the <style> blocks in Vue SFCs
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

[npm-version-src]: https://img.shields.io/npm/v/eslint-processor-vue-blocks?style=flat&colorA=080f12&colorB=1fa669
[npm-version-href]: https://npmjs.com/package/eslint-processor-vue-blocks
[npm-downloads-src]: https://img.shields.io/npm/dm/eslint-processor-vue-blocks?style=flat&colorA=080f12&colorB=1fa669
[npm-downloads-href]: https://npmjs.com/package/eslint-processor-vue-blocks
[bundle-src]: https://img.shields.io/bundlephobia/minzip/eslint-processor-vue-blocks?style=flat&colorA=080f12&colorB=1fa669&label=minzip
[bundle-href]: https://bundlephobia.com/result?p=eslint-processor-vue-blocks
[license-src]: https://img.shields.io/github/license/antfu/eslint-processor-vue-blocks.svg?style=flat&colorA=080f12&colorB=1fa669
[license-href]: https://github.com/antfu/eslint-processor-vue-blocks/blob/main/LICENSE
[jsdocs-src]: https://img.shields.io/badge/jsdocs-reference-080f12?style=flat&colorA=080f12&colorB=1fa669
[jsdocs-href]: https://www.jsdocs.io/package/eslint-processor-vue-blocks
