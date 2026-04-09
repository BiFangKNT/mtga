import { addVitePlugin } from '@nuxt/kit';
import { VueTracer } from 'vite-plugin-vue-tracer';

function setup({ nuxt, options }) {
  if (!nuxt.options.dev || nuxt.options.test)
    return;
  if (!options.componentInspector)
    return;
  const plugin = VueTracer();
  if (plugin)
    addVitePlugin(plugin);
}

export { setup };
