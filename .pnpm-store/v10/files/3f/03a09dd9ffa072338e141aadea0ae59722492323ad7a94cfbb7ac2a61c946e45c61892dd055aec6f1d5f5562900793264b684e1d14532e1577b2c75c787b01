# eslint-typegen

[![npm version][npm-version-src]][npm-version-href]
[![npm downloads][npm-downloads-src]][npm-downloads-href]
[![bundle][bundle-src]][bundle-href]
[![JSDocs][jsdocs-src]][jsdocs-href]
[![License][license-src]][license-href]

Generate types from ESLint rule schemas automatically, with auto-completion and type-checking for rule options.

![](https://github.com/antfu/eslint-typegen/assets/11247099/642ffdc0-c662-4f3b-9237-16d776be1c3e)

> Btw, if you are using [`@antfu/eslint-config`](https://github.com/antfu/eslint-config), you may NOT need to setup this, as the types for rules [are already shipped with the package](https://github.com/antfu/eslint-config/blob/95963ac345d27cd06a4eeb5ebc16e1848cb2fd81/scripts/typegen.ts#L29-L33).

## Usage

```bash
npm i eslint-typegen
```

In your `eslint.config.mjs`, wrap the export with `typegen` function:

```ts
// @ts-check
/// <reference path="./eslint-typegen.d.ts" />
import typegen from 'eslint-typegen'

export default typegen(
  [
    // ...your normal eslint flat config
  ]
)
```

Run ESLint once, an `eslint-typegen.d.ts` file will be generated to augment ESLint's `Linter.RulesRecord` types, to provide you with auto-completion and type-checking for your ESLint rules configuration based on the ESLint plugins you are using.

> It will caluclate the hash of the plugins meta from your flat config, and only regenerate the types when they changes. If you want to force regenerate the types, you can delete the `eslint-typegen.d.ts` file and run ESLint again.

## Low-level API

You can find low-level APIs in the `eslint-typegen/core` modules.

```ts
import fs from 'node:fs/promises'
import pluginTs from '@typescript-eslint/eslint-plugin'
import pluginN from 'eslint-plugin-n'
import { pluginsToRulesDTS } from 'eslint-typegen/core'

const dts = await pluginsToRulesDTS({
  '@typescript-eslint': pluginTs,
  'n': pluginN,
})

await fs.writeFile('eslint-typegen.d.ts', dts)
```

This can be useful if you want to have more control over the generation process, or even bundle the types with your config package. For example, [here](https://github.com/antfu/eslint-config/blob/95963ac345d27cd06a4eeb5ebc16e1848cb2fd81/scripts/typegen.ts#L29-L33) is how [`@antfu/eslint-config`](https://github.com/antfu/eslint-config) does.

## How it works

Thanks to that [ESLint requires rules to provide the JSONSchema for options](https://eslint.org/docs/latest/extend/custom-rules#options-schemas), we could leverage that to generate types with [`json-schema-to-typescript`](https://github.com/bcherny/json-schema-to-typescript). With the new flat config allowing you to execute the code with fully resolved configs, we managed to sneak in the type generation process on the fly.

## Credits

The initial idea comes from [@Shinigami92](https://github.com/Shinigami92) via his work on [`eslint-define-config`](https://github.com/eslint-types/eslint-define-config), thanks to him!

## Sponsors

<p align="center">
  <a href="https://cdn.jsdelivr.net/gh/antfu/static/sponsors.svg">
    <img src='https://cdn.jsdelivr.net/gh/antfu/static/sponsors.svg'/>
  </a>
</p>

## License

[MIT](./LICENSE) License © 2023-PRESENT [Anthony Fu](https://github.com/antfu)

<!-- Badges -->

[npm-version-src]: https://img.shields.io/npm/v/eslint-typegen?style=flat&colorA=080f12&colorB=1fa669
[npm-version-href]: https://npmjs.com/package/eslint-typegen
[npm-downloads-src]: https://img.shields.io/npm/dm/eslint-typegen?style=flat&colorA=080f12&colorB=1fa669
[npm-downloads-href]: https://npmjs.com/package/eslint-typegen
[bundle-src]: https://img.shields.io/bundlephobia/minzip/eslint-typegen?style=flat&colorA=080f12&colorB=1fa669&label=minzip
[bundle-href]: https://bundlephobia.com/result?p=eslint-typegen
[license-src]: https://img.shields.io/github/license/antfu/eslint-typegen.svg?style=flat&colorA=080f12&colorB=1fa669
[license-href]: https://github.com/antfu/eslint-typegen/blob/main/LICENSE
[jsdocs-src]: https://img.shields.io/badge/jsdocs-reference-080f12?style=flat&colorA=080f12&colorB=1fa669
[jsdocs-href]: https://www.jsdocs.io/package/eslint-typegen
