import { join as join$1, resolve as resolve$1, dirname as dirname$1 } from 'node:path';
import fs from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolvePath } from 'mlly';
import { join, dirname, relative, resolve } from 'pathe';
import { getPort } from 'get-port-please';
import { logger, createResolver } from '@nuxt/kit';
import { builtinModules } from 'node:module';
import { stringifyImports } from 'unimport';

function createAddonGlobals(nuxt) {
  let unimport;
  let nitroUnimport;
  nuxt.hook("imports:context", (context) => {
    unimport = context;
  });
  nuxt.hook("nitro:init", (nitro) => {
    nitroUnimport = nitro.unimport;
  });
  return {
    name: "nuxt:eslint:import-globals",
    async getConfigs() {
      const imports = [
        ...await unimport?.getImports() || [],
        ...await nitroUnimport?.getImports() || []
      ].sort((a, b) => 10 * a.from.localeCompare(b.from) + a.name.localeCompare(b.name));
      return {
        configs: [
          [
            "// Set globals from imports registry",
            "{",
            `  name: 'nuxt/import-globals',`,
            "  languageOptions: {",
            `    globals: Object.fromEntries(${JSON.stringify(imports.map((i) => i.as || i.name))}.map(i => [i, 'readonly'])),`,
            `  },`,
            "}"
          ].join("\n")
        ]
      };
    }
  };
}

async function setupDevToolsIntegration(options, nuxt) {
  const {
    enabled = "lazy",
    port
  } = (typeof options.config !== "boolean" ? options.config || {} : {}).devtools || {};
  if (enabled === false)
    return;
  let viewerProcess;
  let viewerPort;
  let viewerUrl;
  let started = false;
  async function start() {
    if (started)
      return;
    started = true;
    const { startSubprocess } = await import('@nuxt/devtools-kit');
    const inspectorBinPath = join(
      dirname(await resolvePath(
        "@eslint/config-inspector/package.json",
        { url: dirname(fileURLToPath(import.meta.url)) }
      )),
      "bin.mjs"
    );
    viewerPort = port || await getPort({
      portRange: [8123, 1e4],
      random: true
    });
    viewerProcess = startSubprocess(
      {
        command: "node",
        args: [inspectorBinPath, "--no-open"],
        cwd: nuxt.options.rootDir,
        env: {
          PORT: viewerPort.toString()
        }
      },
      {
        id: "eslint-config-inspector",
        name: "ESLint Config Viewer"
      },
      nuxt
    );
    nuxt.callHook("devtools:customTabs:refresh");
    const url = `http://localhost:${viewerPort}`;
    for (let i = 0; i < 100; i++) {
      if (await fetch(url).then((r) => r.ok).catch(() => false))
        break;
      await new Promise((resolve) => setTimeout(resolve, 500));
    }
    await new Promise((resolve) => setTimeout(resolve, 2e3));
    viewerUrl = url;
  }
  nuxt.hook("devtools:customTabs", (tabs) => {
    tabs.push({
      name: "eslint-config",
      title: "ESLint Config",
      icon: "https://raw.githubusercontent.com/eslint/config-inspector/refs/heads/main/public/favicon.svg",
      view: viewerUrl ? {
        type: "iframe",
        src: viewerUrl
      } : {
        type: "launch",
        description: "Start ESLint config inspector to analyze the local ESLint configs",
        actions: [
          {
            label: "Launch",
            pending: !!viewerProcess,
            handle: start
          }
        ]
      }
    });
  });
  if (enabled === true)
    start();
}

async function initRootESLintConfig(nuxt, generateConfigPath) {
  const { findUp } = await import('find-up');
  const hasFlatConfig = await findUp(
    [
      "eslint.config.js",
      "eslint.config.mjs",
      "eslint.config.cjs",
      "eslint.config.ts",
      "eslint.config.mts",
      "eslint.config.cts"
    ],
    {
      cwd: nuxt.options.rootDir
    }
  );
  if (hasFlatConfig)
    return;
  const targetPath = join(nuxt.options.rootDir, "eslint.config.mjs");
  let relativeDistPath = relative(nuxt.options.rootDir, generateConfigPath);
  if (!relativeDistPath.startsWith("./") && !relativeDistPath.startsWith("../"))
    relativeDistPath = "./" + relativeDistPath;
  await fs.writeFile(
    targetPath,
    [
      "// @ts-check",
      `import withNuxt from '${relativeDistPath}'`,
      "",
      "export default withNuxt(",
      "  // Your custom configs here",
      ")",
      ""
    ].join("\n"),
    "utf-8"
  );
  logger.success(`ESLint config file created at ${targetPath}`);
  logger.info(`If you have .eslintrc or .eslintignore files, you might want to migrate them to the new config file`);
}

function getDirs(nuxt, options) {
  const rootDir = typeof options.config === "object" && options.config.rootDir || nuxt.options.rootDir;
  const dirs = {
    pages: [],
    composables: [],
    components: [],
    componentsPrefixed: [],
    layouts: [],
    plugins: [],
    middleware: [],
    modules: [],
    servers: [],
    root: [],
    src: []
  };
  for (const layer of nuxt.options._layers) {
    const r = (t) => relative(rootDir, resolve(layer.config.srcDir, t.replace(/^~[/\\]/, "")));
    dirs.src.push(r(""));
    dirs.pages.push(r(nuxt.options.dir.pages || "pages"));
    dirs.layouts.push(r(nuxt.options.dir.layouts || "layouts"));
    dirs.plugins.push(r(nuxt.options.dir.plugins || "plugins"));
    dirs.middleware.push(r(nuxt.options.dir.middleware || "middleware"));
    dirs.modules.push(r(nuxt.options.dir.modules || "modules"));
    dirs.composables.push(r("composables"));
    dirs.composables.push(r("utils"));
    for (const dir of layer.config.imports?.dirs ?? []) {
      if (dir)
        dirs.composables.push(r(dir));
    }
    if (layer.config.components && layer.config.components !== true) {
      const options2 = Array.isArray(layer.config.components) ? { dirs: layer.config.components } : layer.config.components;
      for (const dir of options2.dirs || []) {
        if (typeof dir === "string")
          dirs.components.push(r(dir));
        else if (dir && "path" in dir && typeof dir.path === "string") {
          dirs.components.push(r(dir.path));
          if (dir.prefix)
            dirs.componentsPrefixed.push(r(dir.path));
        }
      }
    } else {
      dirs.components.push(r("components"));
    }
  }
  return dirs;
}

const r = createResolver(import.meta.url);
async function generateESLintConfig(options, nuxt, addons) {
  const importLines = [];
  const configItems = [];
  const config = {
    standalone: true,
    ...typeof options.config !== "boolean" ? options.config || {} : {}
  };
  let {
    configFile = join$1(nuxt.options.buildDir, "eslint.config.mjs")
  } = config;
  configFile = resolve$1(nuxt.options.rootDir, configFile);
  const configDir = dirname$1(configFile);
  importLines.push(
    {
      from: "eslint-typegen",
      name: "default",
      as: "typegen"
    },
    {
      from: "@nuxt/eslint-config/flat",
      name: "createConfigForNuxt"
    },
    {
      from: "@nuxt/eslint-config/flat",
      name: "defineFlatConfigs"
    },
    {
      from: "@nuxt/eslint-config/flat",
      name: "resolveOptions"
    },
    {
      from: "url",
      name: "fileURLToPath"
    }
  );
  const dirs = getDirs(nuxt, options) || {};
  for (const addon of addons) {
    const resolved = await addon.getConfigs();
    if (resolved?.imports)
      importLines.push(...resolved.imports);
    if (resolved?.configs)
      configItems.push(...resolved.configs);
  }
  function relativeWithDot(path) {
    const r2 = relative(configDir, path);
    return r2.startsWith(".") ? r2 : "./" + r2;
  }
  const imports = await Promise.all(importLines.map(async (line) => {
    return {
      ...line,
      from: builtinModules.includes(line.from) ? line.from.replace(/^(node:)?/, "node:") : line.from.match(/^\w+:/) ? line.from : relativeWithDot(await r.resolvePath(line.from))
    };
  }));
  const code = [
    "// ESLint config generated by Nuxt",
    '/// <reference path="./eslint-typegen.d.ts" />',
    "/* eslint-disable */",
    "// @ts-nocheck",
    "",
    stringifyImports(imports, false),
    "",
    "const r = (...args) => fileURLToPath(new URL(...args, import.meta.url))",
    "",
    "export { defineFlatConfigs }",
    "",
    `export const options = resolveOptions({`,
    `  features: ${JSON.stringify(config, null, 2)},`,
    `  dirs: {`,
    ...Object.entries(dirs).map(([key, value]) => {
      return `    ${key}: [${value.map(
        (v) => key === "root" ? `r(${JSON.stringify(relativeWithDot(v))})` : JSON.stringify(v)
      ).join(", ")}],`;
    }),
    `}`,
    `})`,
    "",
    `export const configs = createConfigForNuxt(options)`,
    ...configItems.length ? [
      "",
      `configs.append(`,
      configItems.join(",\n\n"),
      `)`,
      ""
    ] : [],
    "export function withNuxt(...customs) {",
    "  return configs",
    "    .clone()",
    "    .append(...customs)",
    '    .onResolved(configs => typegen(configs, { dtsPath: r("./eslint-typegen.d.ts"), augmentFlatConfigUtils: true }))',
    "}",
    "",
    "export default withNuxt"
  ].join("\n");
  const [
    pathToFlatConfigUtils,
    pathToESLintConfigFlat
  ] = await Promise.all([
    r.resolvePath("eslint-flat-config-utils").then((r2) => relativeWithDot(r2)),
    r.resolvePath("@nuxt/eslint-config/flat").then((r2) => relativeWithDot(r2))
  ]);
  const codeDts = [
    "import type { FlatConfigComposer } from " + JSON.stringify(pathToFlatConfigUtils),
    "import { defineFlatConfigs } from " + JSON.stringify(pathToESLintConfigFlat),
    "import type { NuxtESLintConfigOptionsResolved } from " + JSON.stringify(pathToESLintConfigFlat),
    "",
    "declare const configs: FlatConfigComposer",
    "declare const options: NuxtESLintConfigOptionsResolved",
    "declare const withNuxt: typeof defineFlatConfigs",
    "export default withNuxt",
    "export { withNuxt, defineFlatConfigs, configs, options }"
  ].join("\n");
  return {
    code,
    codeDts,
    configFile
  };
}

async function setupConfigGen(options, nuxt) {
  const {
    autoInit = true
  } = typeof options.config !== "boolean" ? options.config || {} : {};
  const defaultAddons = [
    createAddonGlobals(nuxt)
  ];
  nuxt.hook("prepare:types", ({ declarations, nodeReferences }) => {
    declarations.push('/// <reference path="./eslint-typegen.d.ts" />');
    if (nodeReferences)
      nodeReferences.push({ path: join$1(nuxt.options.buildDir, "eslint-typegen.d.ts") });
  });
  let _configFile = void 0;
  async function writeConfigFile() {
    const addons = [
      ...defaultAddons
    ];
    await nuxt.callHook("eslint:config:addons", addons);
    const { code, codeDts, configFile } = await generateESLintConfig(options, nuxt, addons);
    await fs.mkdir(dirname$1(configFile), { recursive: true });
    await fs.writeFile(configFile, code, "utf-8");
    await fs.writeFile(configFile.replace(/\.mjs$/, ".d.mts"), codeDts, "utf-8");
    _configFile = configFile;
  }
  setupDevToolsIntegration(options, nuxt);
  await writeConfigFile();
  nuxt.hook("builder:generateApp", async () => {
    await writeConfigFile();
  });
  if (autoInit) {
    await initRootESLintConfig(nuxt, _configFile);
  }
}

export { setupConfigGen };
