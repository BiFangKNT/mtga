import { defineNuxtModule } from '@nuxt/kit';

const module$1 = defineNuxtModule({
  meta: {
    name: "@nuxt/eslint",
    configKey: "eslint"
  },
  defaults: {
    config: true,
    checker: false
  },
  async setup(options, nuxt) {
    if (options.config) {
      await import('./chunks/index.mjs').then(({ setupConfigGen }) => setupConfigGen(options, nuxt));
    }
    if (options.checker) {
      if (nuxt.options.dev) {
        await import('./chunks/checker.mjs').then(({ setupESLintChecker }) => {
          setupESLintChecker(options, nuxt);
        });
      }
    }
  }
});

export { module$1 as default };
