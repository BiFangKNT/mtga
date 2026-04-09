# vite-plugin-vue-tracer

[![npm version][npm-version-src]][npm-version-href]
[![npm downloads][npm-downloads-src]][npm-downloads-href]
[![bundle][bundle-src]][bundle-href]
[![JSDocs][jsdocs-src]][jsdocs-href]
[![License][license-src]][license-href]

Tracer for the source code of elements and vdoms in Vue SFC.

This is a designed to be a replacement of [`vite-plugin-vue-inspector`](https://www.npmjs.com/package/vite-plugin-vue-inspector) with a new approach, that utilize Vite's internal source map to resolve the source location, without injecting data-attributes to the DOM.

This plugin is also designed to be more modular, where you can use it as a standalone inspector plugin, or as a headless APIs to build your own inspector.

## Usage

```bash
npm i -D vite-plugin-vue-tracer
```

```ts
import { defineConfig } from 'vite'
import { VueTracer } from 'vite-plugin-vue-tracer'

export default defineConfig({
  plugins: [
    VueTracer(),
  ],
})
```

In the your entry file, add the following code:

```ts
// Only apply in development
if (import.meta.hot) {
  import('vite-plugin-vue-tracer/client/overlay').then(({ events, state }) => {
    // Enables the overlay
    state.isEnabled = true

    events.on('hover', (info) => {
      // ...
    })

    events.on('click', (info) => {
      // ...
      openInEditor(info.fullpath) // 'src/app.vue:10:1'
      state.isEnabled = false
    })
  })
}
```

Of if you want headless APIs, import `vite-plugin-vue-tracer/client/record` instead.

```ts
if (import.meta.hot) {
  import('vite-plugin-vue-tracer/client/record')
    .then(({
      hasData,
      findTraceFromElement,
      findraceFromVNode,
      findTraceAtPointer,
    }) => {
      const el = document.querySelector('.foo')
      const trace = findTraceFromElement(el)
      if (trace) {
        console.log(trace)
      }
    })
}
```

## References

### Exports

- `vite-plugin-vue-tracer` - The Vite plugin entry, should be used in `vite.config.ts`
- `vite-plugin-vue-tracer/client/record` - The client entry for recording the trace data, this will be automatically injected into each component by the plugin. You don't normally need to import this.
- `vite-plugin-vue-tracer/client/listener` - The client entry for adding event listeners to the DOM and listening to the mouse events. It expose a ref `isEnabled` to control if the listeners are active. A `events` object is exposed for listening to those events. This entry is purely headless, does not come with any UI or styling.
- `vite-plugin-vue-tracer/client/overlay` - The builtin overlay UI for easier to use. A reactive `state` object is exposed to control the overlay's state. If you want to build your own UI, you can use the `listener` entry instead.

## Sponsors

<p align="center">
  <a href="https://cdn.jsdelivr.net/gh/antfu/static/sponsors.svg">
    <img src='https://cdn.jsdelivr.net/gh/antfu/static/sponsors.svg' alt='Sponsors' />
  </a>
</p>

## License

[MIT](./LICENSE) License © [Anthony Fu](https://github.com/antfu)

<!-- Badges -->

[npm-version-src]: https://img.shields.io/npm/v/vite-plugin-vue-tracer?style=flat&colorA=080f12&colorB=1fa669
[npm-version-href]: https://npmjs.com/package/vite-plugin-vue-tracer
[npm-downloads-src]: https://img.shields.io/npm/dm/vite-plugin-vue-tracer?style=flat&colorA=080f12&colorB=1fa669
[npm-downloads-href]: https://npmjs.com/package/vite-plugin-vue-tracer
[bundle-src]: https://img.shields.io/bundlephobia/minzip/vite-plugin-vue-tracer?style=flat&colorA=080f12&colorB=1fa669&label=minzip
[bundle-href]: https://bundlephobia.com/result?p=vite-plugin-vue-tracer
[license-src]: https://img.shields.io/github/license/antfu/vite-plugin-vue-tracer.svg?style=flat&colorA=080f12&colorB=1fa669
[license-href]: https://github.com/antfu/vite-plugin-vue-tracer/blob/main/LICENSE
[jsdocs-src]: https://img.shields.io/badge/jsdocs-reference-080f12?style=flat&colorA=080f12&colorB=1fa669
[jsdocs-href]: https://www.jsdocs.io/package/vite-plugin-vue-tracer
