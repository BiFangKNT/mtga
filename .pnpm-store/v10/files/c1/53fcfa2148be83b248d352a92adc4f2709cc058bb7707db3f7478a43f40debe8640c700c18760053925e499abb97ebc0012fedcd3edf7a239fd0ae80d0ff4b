import * as parserVue from 'vue-eslint-parser';
import pluginVue from 'eslint-plugin-vue';
import processorVueBlocks from 'eslint-processor-vue-blocks';
import { mergeProcessors } from 'eslint-merge-processors';
import { r as resolveOptions, a as removeUndefined } from '../shared/eslint-config.Bw-e4MbC.mjs';
import 'eslint-flat-config-utils';
import 'eslint-config-flat-gitignore';
import 'pathe';
import 'node:process';
import 'local-pkg';
import '@nuxt/eslint-plugin';
import '@eslint/js';
import 'globals';

const INLINE_ELEMENTS = ["a", "abbr", "audio", "b", "bdi", "bdo", "canvas", "cite", "code", "data", "del", "dfn", "em", "i", "iframe", "ins", "kbd", "label", "map", "mark", "noscript", "object", "output", "picture", "q", "ruby", "s", "samp", "small", "span", "strong", "sub", "sup", "svg", "time", "u", "var", "video"];
async function vue(options) {
  const resolved = resolveOptions(options);
  const hasTs = resolved.features.typescript !== false;
  const parser = hasTs ? await import('./typescript.mjs').then((mod) => mod.parserTs) : void 0;
  const {
    indent = 2,
    commaDangle = "always-multiline"
  } = typeof resolved.features.stylistic === "boolean" ? {} : resolved.features.stylistic;
  const configs = [
    {
      name: "nuxt/vue/setup",
      plugins: {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        vue: pluginVue
      },
      languageOptions: {
        parserOptions: {
          ecmaVersion: "latest",
          extraFileExtensions: [".vue"],
          parser,
          sourceType: "module",
          ecmaFeatures: {
            jsx: true
          }
        },
        // This allows Vue plugin to work with auto imports
        // https://github.com/vuejs/eslint-plugin-vue/pull/2422
        globals: {
          computed: "readonly",
          defineEmits: "readonly",
          defineExpose: "readonly",
          defineProps: "readonly",
          onMounted: "readonly",
          onUnmounted: "readonly",
          reactive: "readonly",
          ref: "readonly",
          shallowReactive: "readonly",
          shallowRef: "readonly",
          toRef: "readonly",
          toRefs: "readonly",
          watch: "readonly",
          watchEffect: "readonly"
        }
      }
    },
    {
      name: "nuxt/vue/rules",
      files: [
        "**/*.vue"
      ],
      languageOptions: {
        parser: parserVue
      },
      processor: options.features?.formatters ? mergeProcessors([
        pluginVue.processors[".vue"],
        processorVueBlocks({
          blocks: {
            styles: true
          }
        })
      ]) : pluginVue.processors[".vue"],
      rules: {
        ...pluginVue.configs.base.rules,
        ...pluginVue.configs["flat/essential"].map((c) => c.rules).reduce((acc, c) => ({ ...acc, ...c }), {}),
        ...pluginVue.configs["flat/strongly-recommended"].map((c) => c.rules).reduce((acc, c) => ({ ...acc, ...c }), {}),
        ...pluginVue.configs["flat/recommended"].map((c) => c.rules).reduce((acc, c) => ({ ...acc, ...c }), {}),
        "no-useless-assignment": "off",
        // Deprecated in favor of 'vue/block-order'
        "vue/component-tags-order": void 0,
        "vue/block-order": "warn",
        ...resolved.features.stylistic ? {
          "vue/array-bracket-spacing": ["error", "never"],
          "vue/arrow-spacing": ["error", { after: true, before: true }],
          "vue/block-spacing": ["error", "always"],
          "vue/block-tag-newline": [
            "error",
            {
              multiline: "always",
              singleline: "always"
            }
          ],
          "vue/brace-style": ["error", "stroustrup", { allowSingleLine: true }],
          "vue/html-indent": ["error", indent],
          "vue/html-quotes": ["error", "double"],
          "vue/comma-dangle": ["error", commaDangle],
          "vue/comma-spacing": ["error", { after: true, before: false }],
          "vue/comma-style": ["error", "last"],
          "vue/html-comment-content-spacing": [
            "error",
            "always",
            { exceptions: ["-"] }
          ],
          "vue/key-spacing": ["error", { afterColon: true, beforeColon: false }],
          "vue/keyword-spacing": ["error", { after: true, before: true }],
          "vue/object-curly-newline": "off",
          "vue/object-curly-spacing": ["error", "always"],
          "vue/object-property-newline": [
            "error",
            { allowAllPropertiesOnSameLine: true }
          ],
          "vue/one-component-per-file": "off",
          "vue/operator-linebreak": ["error", "before"],
          "vue/padding-line-between-blocks": ["error", "always"],
          "vue/quote-props": ["error", "consistent-as-needed"],
          "vue/require-default-prop": "off",
          "vue/space-in-parens": ["error", "never"],
          "vue/template-curly-spacing": "error",
          "vue/multiline-html-element-content-newline": ["error", {
            ignoreWhenEmpty: true,
            ignores: ["pre", "textarea", "router-link", "RouterLink", "nuxt-link", "NuxtLink", "u-link", "ULink", ...INLINE_ELEMENTS],
            allowEmptyLines: false
          }],
          "vue/singleline-html-element-content-newline": ["error", {
            ignoreWhenNoAttributes: true,
            ignoreWhenEmpty: true,
            ignores: ["pre", "textarea", "router-link", "RouterLink", "nuxt-link", "NuxtLink", "u-link", "ULink", ...INLINE_ELEMENTS],
            externalIgnores: []
          }]
        } : {
          // Disable Vue's default stylistic rules when stylistic is not enabled
          "vue/html-closing-bracket-newline": void 0,
          "vue/html-closing-bracket-spacing": void 0,
          "vue/html-indent": void 0,
          "vue/html-quotes": void 0,
          "vue/max-attributes-per-line": void 0,
          "vue/multiline-html-element-content-newline": void 0,
          "vue/mustache-interpolation-spacing": void 0,
          "vue/no-multi-spaces": void 0,
          "vue/no-spaces-around-equal-signs-in-attribute": void 0,
          "vue/singleline-html-element-content-newline": void 0
        }
      }
    }
  ];
  for (const config of configs) {
    if (config.rules)
      config.rules = removeUndefined(config.rules);
  }
  return configs;
}

export { vue as default };
