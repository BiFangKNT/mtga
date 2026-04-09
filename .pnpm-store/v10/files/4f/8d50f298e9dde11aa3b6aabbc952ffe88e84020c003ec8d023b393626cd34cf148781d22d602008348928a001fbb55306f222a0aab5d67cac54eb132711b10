import { defineNuxtModule, addVitePlugin } from '@nuxt/kit';
import { P as PluginInspect } from './shared/vite-plugin-inspect.BzUKaD4x.mjs';
import 'node:process';
import 'ansis';
import 'perfect-debounce';
import 'sirv';
import 'vite-dev-rpc';
import './dirs.mjs';
import 'node:path';
import 'node:url';
import 'node:fs/promises';
import 'ohash';
import 'node:buffer';
import 'unplugin-utils';
import 'debug';
import 'error-stack-parser-es';
import 'node:http';

const nuxt = defineNuxtModule({
  meta: {
    name: "vite-plugin-inspect",
    configKey: "inspect"
  },
  setup(options) {
    addVitePlugin(() => PluginInspect(options));
  }
});

export { nuxt as default };
