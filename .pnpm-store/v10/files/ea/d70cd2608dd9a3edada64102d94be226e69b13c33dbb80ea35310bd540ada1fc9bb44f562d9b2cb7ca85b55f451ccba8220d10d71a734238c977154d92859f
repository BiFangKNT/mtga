import { defineComponent, h } from "vue";
import { parseQuery } from "vue-router";
import { resolve } from "pathe";
import { devRootDir } from "#build/nuxt.config.mjs";
export default (url) => defineComponent({
  name: "NuxtTestComponentWrapper",
  inheritAttrs: false,
  async setup(props, { attrs }) {
    const query = parseQuery(new URL(url, "http://localhost").search);
    let urlProps = {};
    if (query.props) {
      try {
        const parsedProps = JSON.parse(query.props);
        if (parsedProps && typeof parsedProps === "object") {
          urlProps = parsedProps;
        }
      } catch {
      }
    }
    const path = resolve(query.path);
    if (!path.startsWith(devRootDir)) {
      throw new Error(`[nuxt] Cannot access path outside of project root directory: \`${path}\`.`);
    }
    const comp = await import(
      /* @vite-ignore */
      path
    ).then((r) => r.default);
    return () => [
      h("div", "Component Test Wrapper for " + path),
      h("div", { id: "nuxt-component-root" }, [
        h(comp, { ...attrs, ...props, ...urlProps })
      ])
    ];
  }
});
