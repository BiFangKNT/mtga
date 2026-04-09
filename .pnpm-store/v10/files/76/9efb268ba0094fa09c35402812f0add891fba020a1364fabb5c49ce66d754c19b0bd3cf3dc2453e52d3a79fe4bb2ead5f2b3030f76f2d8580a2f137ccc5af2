import { addPluginTemplate, resolvePath } from '@nuxt/kit';
import { join } from 'pathe';
import { runtimeDir } from '../dirs.mjs';
import 'node:path';
import 'node:url';
import 'is-installed-globally';

async function setup({ nuxt }) {
  if (!nuxt.options.dev || nuxt.options.test)
    return;
  addPluginTemplate({
    name: "vue-devtools-client",
    mode: "client",
    order: -1e3,
    src: await resolvePath(join(runtimeDir, "vue-devtools-client"))
  });
}

export { setup };
