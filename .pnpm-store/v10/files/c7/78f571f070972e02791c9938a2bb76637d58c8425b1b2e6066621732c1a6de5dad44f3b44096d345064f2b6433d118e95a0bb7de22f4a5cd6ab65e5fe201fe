import jsdocPlugin from 'eslint-plugin-jsdoc';
import { G as GLOB_SRC, a as GLOB_VUE } from '../shared/eslint-config.CUi9znUC.mjs';
import { r as resolveOptions } from '../shared/eslint-config.Bw-e4MbC.mjs';
import 'eslint-flat-config-utils';
import 'eslint-config-flat-gitignore';
import 'pathe';
import 'node:process';
import 'local-pkg';
import '@nuxt/eslint-plugin';
import '@eslint/js';
import 'globals';

function jsdoc(options = {}) {
  const resolved = resolveOptions(options);
  return [
    {
      name: "nuxt/tooling/jsdoc",
      files: [GLOB_SRC, GLOB_VUE],
      plugins: {
        jsdoc: jsdocPlugin
      },
      rules: {
        "jsdoc/check-access": "warn",
        "jsdoc/check-param-names": "warn",
        "jsdoc/check-property-names": "warn",
        "jsdoc/check-types": "warn",
        "jsdoc/empty-tags": "warn",
        "jsdoc/implements-on-classes": "warn",
        "jsdoc/no-defaults": "warn",
        "jsdoc/no-multi-asterisks": "warn",
        "jsdoc/require-param-name": "warn",
        "jsdoc/require-property": "warn",
        "jsdoc/require-property-description": "warn",
        "jsdoc/require-property-name": "warn",
        "jsdoc/require-returns-check": "warn",
        "jsdoc/require-returns-description": "warn",
        "jsdoc/require-yields-check": "warn",
        ...resolved.features.stylistic ? {
          "jsdoc/check-alignment": "warn",
          "jsdoc/multiline-blocks": "warn"
        } : {}
      }
    }
  ];
}

export { jsdoc as default };
