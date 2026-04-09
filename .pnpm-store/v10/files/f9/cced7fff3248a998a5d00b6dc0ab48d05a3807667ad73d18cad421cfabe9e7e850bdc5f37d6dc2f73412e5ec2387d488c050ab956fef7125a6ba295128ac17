import { isPackageExists } from 'local-pkg';
import { e as ensurePackages, i as interopDefault, p as parserPlain } from '../shared/eslint-config.Bw-e4MbC.mjs';
import { b as GLOB_CSS, c as GLOB_POSTCSS, d as GLOB_SCSS, e as GLOB_LESS, f as GLOB_HTML, g as GLOB_XML, h as GLOB_SVG, i as GLOB_MARKDOWN, j as GLOB_GRAPHQL } from '../shared/eslint-config.CUi9znUC.mjs';
import 'eslint-flat-config-utils';
import 'eslint-config-flat-gitignore';
import 'pathe';
import 'node:process';
import '@nuxt/eslint-plugin';
import '@eslint/js';
import 'globals';

function mergePrettierOptions(options, overrides = {}) {
  return {
    ...options,
    ...overrides,
    plugins: [
      ...overrides.plugins || [],
      ...options.plugins || []
    ]
  };
}
async function formatters(options = {}, stylistic) {
  if (!options)
    return [];
  if (options === true) {
    const isPrettierPluginXmlInScope = isPackageExists("@prettier/plugin-xml");
    options = {
      css: true,
      graphql: true,
      html: true,
      // Markdown is disabled by default as many Nuxt projects use MDC with @nuxt/content,
      // where Prettier doesn't fully understand.
      markdown: false,
      svg: isPrettierPluginXmlInScope,
      xml: isPrettierPluginXmlInScope
    };
  }
  await ensurePackages([
    "eslint-plugin-format",
    options.xml || options.svg ? "@prettier/plugin-xml" : void 0
  ]);
  const {
    indent,
    quotes,
    semi
  } = {
    indent: 2,
    quotes: "single",
    semi: false,
    ...stylistic
  };
  const prettierOptions = Object.assign(
    {
      endOfLine: "auto",
      printWidth: 120,
      semi,
      singleQuote: quotes === "single",
      tabWidth: typeof indent === "number" ? indent : 2,
      trailingComma: "all",
      useTabs: indent === "tab"
    },
    options.prettierOptions || {}
  );
  const prettierXmlOptions = {
    xmlQuoteAttributes: "double",
    xmlSelfClosingSpace: true,
    xmlSortAttributesByKey: false,
    xmlWhitespaceSensitivity: "ignore"
  };
  const dprintOptions = Object.assign(
    {
      indentWidth: typeof indent === "number" ? indent : 2,
      quoteStyle: quotes === "single" ? "preferSingle" : "preferDouble",
      useTabs: indent === "tab"
    },
    options.dprintOptions || {}
  );
  const pluginFormat = await interopDefault(import('eslint-plugin-format'));
  const configs = [
    {
      name: "nuxt/formatter/setup",
      plugins: {
        format: pluginFormat
      }
    }
  ];
  if (options.css) {
    configs.push(
      {
        files: [GLOB_CSS, GLOB_POSTCSS],
        languageOptions: {
          parser: parserPlain
        },
        name: "nuxt/formatter/css",
        rules: {
          "format/prettier": [
            "error",
            mergePrettierOptions(prettierOptions, {
              parser: "css"
            })
          ]
        }
      },
      {
        files: [GLOB_SCSS],
        languageOptions: {
          parser: parserPlain
        },
        name: "nuxt/formatter/scss",
        rules: {
          "format/prettier": [
            "error",
            mergePrettierOptions(prettierOptions, {
              parser: "scss"
            })
          ]
        }
      },
      {
        files: [GLOB_LESS],
        languageOptions: {
          parser: parserPlain
        },
        name: "nuxt/formatter/less",
        rules: {
          "format/prettier": [
            "error",
            mergePrettierOptions(prettierOptions, {
              parser: "less"
            })
          ]
        }
      }
    );
  }
  if (options.html) {
    configs.push({
      files: [GLOB_HTML],
      languageOptions: {
        parser: parserPlain
      },
      name: "nuxt/formatter/html",
      rules: {
        "format/prettier": [
          "error",
          mergePrettierOptions(prettierOptions, {
            parser: "html"
          })
        ]
      }
    });
  }
  if (options.xml) {
    configs.push({
      files: [GLOB_XML],
      languageOptions: {
        parser: parserPlain
      },
      name: "nuxt/formatter/xml",
      rules: {
        "format/prettier": [
          "error",
          mergePrettierOptions({ ...prettierXmlOptions, ...prettierOptions }, {
            parser: "xml",
            plugins: [
              "@prettier/plugin-xml"
            ]
          })
        ]
      }
    });
  }
  if (options.svg) {
    configs.push({
      files: [GLOB_SVG],
      languageOptions: {
        parser: parserPlain
      },
      name: "nuxt/formatter/svg",
      rules: {
        "format/prettier": [
          "error",
          mergePrettierOptions({ ...prettierXmlOptions, ...prettierOptions }, {
            parser: "xml",
            plugins: [
              "@prettier/plugin-xml"
            ]
          })
        ]
      }
    });
  }
  if (options.markdown) {
    const formater = options.markdown === true ? "prettier" : options.markdown;
    configs.push({
      files: [GLOB_MARKDOWN],
      languageOptions: {
        parser: parserPlain
      },
      name: "nuxt/formatter/markdown",
      rules: {
        [`format/${formater}`]: [
          "error",
          formater === "prettier" ? mergePrettierOptions(prettierOptions, {
            embeddedLanguageFormatting: "off",
            parser: "markdown"
          }) : {
            ...dprintOptions,
            language: "markdown"
          }
        ]
      }
    });
  }
  if (options.graphql) {
    configs.push({
      files: [GLOB_GRAPHQL],
      languageOptions: {
        parser: parserPlain
      },
      name: "nuxt/formatter/graphql",
      rules: {
        "format/prettier": [
          "error",
          mergePrettierOptions(prettierOptions, {
            parser: "graphql"
          })
        ]
      }
    });
  }
  return configs;
}

export { formatters };
