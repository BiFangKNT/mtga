import { r as resolveOptions } from '../shared/eslint-config.Bw-e4MbC.mjs';
import 'eslint-flat-config-utils';
import 'eslint-config-flat-gitignore';
import 'pathe';
import 'node:process';
import 'local-pkg';
import '@nuxt/eslint-plugin';
import '@eslint/js';
import 'globals';

async function imports(options) {
  const resolved = resolveOptions(options);
  if (resolved.features.import === false) {
    return [];
  }
  const importOptions = resolved.features.import === true ? {} : resolved.features.import || {};
  const plugin = importOptions.package === "eslint-plugin-import-lite" ? (await import('eslint-plugin-import-lite')).default : (await import('eslint-plugin-import-x')).default;
  return [
    {
      name: "nuxt/import/rules",
      plugins: {
        import: plugin
      },
      rules: {
        ...importOptions.package === "eslint-plugin-import-lite" ? {
          "import/consistent-type-specifier-style": ["error", "top-level"]
        } : {},
        "import/first": "error",
        "import/no-duplicates": "error",
        "import/no-mutable-exports": "error",
        "import/no-named-default": "error",
        ...resolved.features.stylistic ? {
          "import/newline-after-import": ["error", { count: 1 }]
        } : {}
      }
    }
  ];
}

export { imports as default };
