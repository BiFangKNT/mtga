# structured-clone-es

[![npm version][npm-version-src]][npm-version-href]
[![npm downloads][npm-downloads-src]][npm-downloads-href]
[![bundle][bundle-src]][bundle-href]
[![JSDocs][jsdocs-src]][jsdocs-href]
[![License][license-src]][license-href]

An env-agnostic serializer and deserializer with recursion ability and types beyond JSON, based on the [HTML structured clone algorithm](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm).

Ported from [`@ungap/structured-clone`](https://github.com/ungap/structured-clone) by [Andrea Giammarchi](https://github.com/WebReflection), with TypeScript support and modern ESM packaging.

> [!NOTE]
> If you are targeting modern environments, the native [`structuredClone()`](https://developer.mozilla.org/en-US/docs/Web/API/structuredClone) is available in all major browsers and Node.js 17+. Use it directly for better performance.
>
> The main value of this package is the **`serialize` / `deserialize`** and **`stringify` / `parse`** utilities, which allow you to convert complex and recursive objects into JSON-safe representations — useful for sending structured data across processes or over the network (e.g. client-server RPC communication).
>
> Used by [Nuxt DevTools](https://github.com/nuxt/devtools), [Vite DevTools](https://github.com/nicepkg/vite-plugin-devtools), [Node Modules Inspector](https://github.com/nicepkg/node-modules-inspector), [ESLint Config Inspector](https://github.com/eslint/config-inspector), and more.

## Install

```bash
npm i structured-clone-es
```

## Usage

### Serialize / Deserialize

The result of `serialize` can be safely stringified as JSON, even if the original data contains recursive references, `BigInt` values, typed arrays, and so on.

```ts
import { deserialize, serialize } from 'structured-clone-es'

// serialize any value into a JSON-compatible array of records
const serialized = serialize({ any: 'serializable' })

// reconstruct the original object
const deserialized = deserialize(serialized)
```

### Stringify / Parse

A convenience wrapper that combines `serialize` + `JSON.stringify` and `JSON.parse` + `deserialize`:

```ts
import { parse, stringify } from 'structured-clone-es'

const str = stringify({ any: 'serializable' })
const obj = parse(str)
```

### structuredClone

A pure `structuredClone` implementation is also exported. It always uses the serialize/deserialize path without relying on the runtime's native `structuredClone`.

```ts
import { structuredClone } from 'structured-clone-es'

const cloned = structuredClone({ any: 'serializable' })
```

If you need polyfill `globalThis.structuredClone`, you can attach it manually:

```ts
import { structuredClone } from 'structured-clone-es'

if (!('structuredClone' in globalThis)) {
  globalThis.structuredClone = structuredClone
}
```

## Supported Types

- Primitives: `string`, `number`, `boolean`, `null`, `undefined`, `BigInt`
- Collections: `Array`, `Object`, `Map`, `Set`
- Typed Arrays: `Uint8Array`, `Uint16Array`, `Uint32Array`, `Int8Array`, `Int16Array`, `Int32Array`, `ArrayBuffer`, `DataView`
- `Date`, `RegExp`, `Error`
- Boxed primitives: `Boolean`, `Number`, `String`
- Circular / recursive references

See the [MDN documentation](https://developer.mozilla.org/en-US/docs/Web/API/Web_Workers_API/Structured_clone_algorithm#supported_types) for the full structured clone algorithm spec. Note that browser-specific types (Blob, File, ImageBitmap, etc.) are not supported by this library.

## Lossy Mode

By default, `serialize` throws on incompatible types like `function` or `symbol`. Use the `lossy` option to silently replace them with `null` instead:

```ts
import { structuredClone } from 'structured-clone-es'

const cloned = structuredClone(
  {
    method() { /* ignored */ },
    special: Symbol('also ignored'),
  },
  { lossy: true },
)
```

### JSON Mode

The `json` option implies `lossy` and additionally checks for `toJSON()` methods on objects:

```ts
import { structuredClone } from 'structured-clone-es'

const cloned = structuredClone(
  {
    date: {
      toJSON() {
        return '2024-01-01'
      },
    },
  },
  { json: true },
)
```

The `stringify` / `parse` exports use both `json` and `lossy` by default.

## Credits

This project is a TypeScript port of [`@ungap/structured-clone`](https://github.com/ungap/structured-clone), originally created by [Andrea Giammarchi](https://github.com/WebReflection) under the ISC license.

## License

[ISC](./LICENSE.md)

<!-- Badges -->

[npm-version-src]: https://img.shields.io/npm/v/structured-clone-es?style=flat&colorA=080f12&colorB=1fa669
[npm-version-href]: https://npmjs.com/package/structured-clone-es
[npm-downloads-src]: https://img.shields.io/npm/dm/structured-clone-es?style=flat&colorA=080f12&colorB=1fa669
[npm-downloads-href]: https://npmjs.com/package/structured-clone-es
[bundle-src]: https://img.shields.io/bundlephobia/minzip/structured-clone-es?style=flat&colorA=080f12&colorB=1fa669&label=minzip
[bundle-href]: https://bundlephobia.com/result?p=structured-clone-es
[license-src]: https://img.shields.io/github/license/antfu-collective/structured-clone-es.svg?style=flat&colorA=080f12&colorB=1fa669
[license-href]: https://github.com/antfu-collective/structured-clone-es/blob/main/LICENSE
[jsdocs-src]: https://img.shields.io/badge/jsdocs-reference-080f12?style=flat&colorA=080f12&colorB=1fa669
[jsdocs-href]: https://www.jsdocs.io/package/structured-clone-es
