import { composer } from 'eslint-flat-config-utils';
import gitignore from 'eslint-config-flat-gitignore';
import { join } from 'pathe';
import process from 'node:process';
import { isPackageExists } from 'local-pkg';
import nuxtPlugin from '@nuxt/eslint-plugin';
import pluginESLint from '@eslint/js';
import globals from 'globals';

const GLOB_EXTS = "{js,ts,jsx,tsx,vue}";

const parserPlain = {
  meta: {
    name: "parser-plain"
  },
  parseForESLint: (code) => ({
    ast: {
      body: [],
      comments: [],
      loc: { end: code.length, start: 0 },
      range: [0, code.length],
      tokens: [],
      type: "Program"
    },
    scopeManager: null,
    services: { isPlain: true },
    visitorKeys: {
      Program: []
    }
  })
};
async function ensurePackages(packages) {
  if (process.env.CI || !process.stdout.isTTY)
    return;
  const nonExistingPackages = packages.filter((i) => i && !isPackageExists(i));
  if (nonExistingPackages.length === 0)
    return;
  const p = await import('@clack/prompts');
  const result = await p.confirm({
    message: `${nonExistingPackages.length === 1 ? "Package is" : "Packages are"} required for this config: ${nonExistingPackages.join(", ")}. Do you want to install them?`
  });
  if (result)
    await import('@antfu/install-pkg').then((i) => i.installPackage(nonExistingPackages, { dev: true }));
}
async function interopDefault(m) {
  const resolved = await m;
  return resolved.default || resolved;
}
function removeUndefined(obj) {
  return Object.fromEntries(Object.entries(obj).filter(([, value]) => value !== void 0));
}
function resolveOptions(config) {
  if ("__resolved" in config) {
    return config;
  }
  const dirs = {
    ...config.dirs
  };
  dirs.root ||= [".", "./app"];
  dirs.src ||= dirs.root;
  dirs.pages ||= dirs.src.map((src) => `${src}/pages`);
  dirs.layouts ||= dirs.src.map((src) => `${src}/layouts`);
  dirs.components ||= dirs.src.map((src) => `${src}/components`);
  dirs.composables ||= dirs.src.map((src) => `${src}/composables`);
  dirs.plugins ||= dirs.src.map((src) => `${src}/plugins`);
  dirs.modules ||= dirs.src.map((src) => `${src}/modules`);
  dirs.middleware ||= dirs.src.map((src) => `${src}/middleware`);
  dirs.servers ||= dirs.src.map((src) => `${src}/servers`);
  dirs.componentsPrefixed ||= [];
  const resolved = {
    features: {
      standalone: true,
      stylistic: false,
      typescript: isPackageExists("typescript"),
      tooling: false,
      formatters: false,
      nuxt: {},
      import: {},
      ...config.features
    },
    dirs
  };
  Object.defineProperty(resolved, "__resolved", { value: true, enumerable: false });
  return resolved;
}

function disables(options) {
  const resolved = resolveOptions(options);
  const dirs = resolved.dirs;
  const nestedGlobPattern = `**/*.${GLOB_EXTS}`;
  const fileRoutes = [.../* @__PURE__ */ new Set([
    // These files must have one-word names as they have a special meaning in Nuxt.
    ...dirs.src.flatMap((layersDir) => [
      join(layersDir, `app.${GLOB_EXTS}`),
      join(layersDir, `error.${GLOB_EXTS}`)
    ]) || [],
    // Layouts and pages are not used directly by users so they can have one-word names.
    ...dirs.layouts.map((layoutsDir) => join(layoutsDir, nestedGlobPattern)) || [],
    ...dirs.pages.map((pagesDir) => join(pagesDir, nestedGlobPattern)) || [],
    // These files should have multiple words in their names as they are within subdirectories.
    ...dirs.components.map((componentsDir) => join(componentsDir, "*", nestedGlobPattern)) || [],
    // Prefixed components can have one-word names in file
    ...dirs.componentsPrefixed.map((componentsDir) => join(componentsDir, nestedGlobPattern)) || []
  ])].sort();
  const configs = [];
  if (fileRoutes.length) {
    configs.push({
      name: "nuxt/disables/routes",
      files: fileRoutes,
      rules: {
        "vue/multi-word-component-names": "off"
      }
    });
  }
  return configs;
}

function nuxt(options) {
  const resolved = resolveOptions(options);
  const dirs = resolved.dirs;
  const fileSingleRoot = [
    ...dirs.layouts?.map((layoutsDir) => join(layoutsDir, `**/*.${GLOB_EXTS}`)) || [],
    ...dirs.pages?.map((pagesDir) => join(pagesDir, `**/*.${GLOB_EXTS}`)) || [],
    ...dirs.components?.map((componentsDir) => join(componentsDir, `**/*.server.${GLOB_EXTS}`)) || []
  ].sort();
  const {
    sortConfigKeys = !!options.features?.stylistic
  } = options.features?.nuxt || {};
  const configs = [];
  configs.push({
    name: "nuxt/setup",
    plugins: {
      nuxt: nuxtPlugin
    },
    languageOptions: {
      globals: {
        // Nuxt's runtime globals
        $fetch: "readonly"
      }
    }
  });
  if (fileSingleRoot.length)
    configs.push({
      name: "nuxt/vue/single-root",
      files: fileSingleRoot,
      rules: {
        "vue/no-multiple-template-root": "error"
      }
    });
  configs.push({
    name: "nuxt/rules",
    rules: {
      "nuxt/prefer-import-meta": "error"
    }
  });
  const filePages = [
    ...dirs.pages?.map((pagesDir) => join(pagesDir, `**/*.${GLOB_EXTS}`)) || []
  ].sort();
  if (filePages.length) {
    configs.push({
      name: "nuxt/pages",
      files: filePages,
      rules: {
        "nuxt/no-page-meta-runtime-values": "error"
      }
    });
  }
  configs.push({
    name: "nuxt/nuxt-config",
    files: [
      "**/.config/nuxt.?([cm])[jt]s?(x)",
      "**/nuxt.config.?([cm])[jt]s?(x)"
    ],
    rules: {
      "nuxt/no-nuxt-config-test-key": "error"
    }
  });
  if (sortConfigKeys) {
    configs.push({
      name: "nuxt/sort-config",
      files: [
        "**/.config/nuxt.?([cm])[jt]s?(x)",
        "**/nuxt.config.?([cm])[jt]s?(x)"
      ],
      rules: {
        "nuxt/nuxt-config-keys-order": "error"
      }
    });
  }
  return configs;
}

function ignores() {
  return [
    {
      ignores: [
        "**/dist",
        "**/node_modules",
        "**/.nuxt",
        "**/.output",
        "**/.vercel",
        "**/.netlify",
        "**/public"
      ]
    }
  ];
}

function javascript() {
  return [
    {
      ...pluginESLint.configs.recommended,
      name: "nuxt/javascript",
      languageOptions: {
        ecmaVersion: 2022,
        parserOptions: {
          ecmaFeatures: {
            jsx: true
          },
          ecmaVersion: 2022,
          sourceType: "module"
        },
        sourceType: "module",
        globals: {
          ...globals.browser,
          ...globals.es2021,
          ...globals.node,
          document: "readonly",
          navigator: "readonly",
          window: "readonly",
          // This is technically not a global function, but it's a common practice in nuxt.config.ts,
          // we include it here to avoid false positives.
          defineNuxtConfig: "readonly"
        }
      },
      linterOptions: {
        reportUnusedDisableDirectives: true
      }
    }
  ];
}

function defineFlatConfigs(...configs) {
  return composer(...configs);
}
function createConfigForNuxt(options = {}, ...userConfigs) {
  const c = composer();
  const resolved = resolveOptions(options);
  if (resolved.features.standalone !== false) {
    c.append(
      gitignore({ strict: false }),
      ignores(),
      javascript(),
      // Make these imports async, as they are optional and imports plugins
      resolved.features.typescript !== false ? import('../chunks/typescript.mjs').then((m) => m.default(resolved)) : void 0,
      import('../chunks/vue.mjs').then((m) => m.default(resolved)),
      import('../chunks/import.mjs').then((m) => m.default(resolved))
    );
  }
  c.append(
    nuxt(resolved)
  );
  if (resolved.features.tooling) {
    const toolingOptions = typeof resolved.features.tooling === "boolean" ? {} : resolved.features.tooling;
    c.append(
      toolingOptions.jsdoc !== false && import('../chunks/jsdoc.mjs').then((m) => m.default(resolved)),
      toolingOptions.unicorn !== false && import('../chunks/unicorn.mjs').then((m) => m.default()),
      toolingOptions.regexp !== false && import('../chunks/regexp.mjs').then((m) => m.default())
    );
  }
  const stylisticOptions = typeof resolved.features.stylistic === "boolean" ? {} : resolved.features.stylistic;
  if (resolved.features.stylistic) {
    c.append(
      import('../chunks/stylistic.mjs').then((m) => m.default(stylisticOptions))
    );
  }
  if (resolved.features.formatters) {
    c.append(
      import('../chunks/formatters.mjs').then((m) => m.formatters(resolved.features.formatters, stylisticOptions))
    );
  }
  c.append(
    disables(resolved)
  );
  if (userConfigs.length > 0) {
    c.append(...userConfigs);
  }
  c.setPluginConflictsError().setPluginConflictsError("import", [
    'Different instances of plugin "{{pluginName}}" found in multiple configs:',
    "{{configNames}}.",
    "You might forget to set `standalone: false`.",
    "Please refer to https://eslint.nuxt.com/packages/module#custom-config-presets.",
    ""
  ].join("\n"));
  return c;
}

export { removeUndefined as a, createConfigForNuxt as c, defineFlatConfigs as d, ensurePackages as e, interopDefault as i, parserPlain as p, resolveOptions as r };
