# Introduction

[eslint-plugin-yml](https://www.npmjs.com/package/eslint-plugin-yml) is ESLint plugin provides linting rules for [YAML].

[![NPM license](https://img.shields.io/npm/l/eslint-plugin-yml.svg)](https://www.npmjs.com/package/eslint-plugin-yml)
[![NPM version](https://img.shields.io/npm/v/eslint-plugin-yml.svg)](https://www.npmjs.com/package/eslint-plugin-yml)
[![NPM downloads](https://img.shields.io/badge/dynamic/json.svg?label=downloads&colorB=green&suffix=/day&query=$.downloads&uri=https://api.npmjs.org//downloads/point/last-day/eslint-plugin-yml&maxAge=3600)](http://www.npmtrends.com/eslint-plugin-yml)
[![NPM downloads](https://img.shields.io/npm/dw/eslint-plugin-yml.svg)](http://www.npmtrends.com/eslint-plugin-yml)
[![NPM downloads](https://img.shields.io/npm/dm/eslint-plugin-yml.svg)](http://www.npmtrends.com/eslint-plugin-yml)
[![NPM downloads](https://img.shields.io/npm/dy/eslint-plugin-yml.svg)](http://www.npmtrends.com/eslint-plugin-yml)
[![NPM downloads](https://img.shields.io/npm/dt/eslint-plugin-yml.svg)](http://www.npmtrends.com/eslint-plugin-yml)
[![Build Status](https://github.com/ota-meshi/eslint-plugin-yml/actions/workflows/NodeCI.yml/badge.svg)](https://github.com/ota-meshi/eslint-plugin-yml/actions/workflows/NodeCI.yml)
[![Coverage Status](https://coveralls.io/repos/github/ota-meshi/eslint-plugin-yml/badge.svg?branch=master)](https://coveralls.io/github/ota-meshi/eslint-plugin-yml?branch=master)

## :name_badge: Features

This ESLint plugin provides linting rules for [YAML].

- You can use ESLint to lint [YAML].
- You can find out the problem with your [YAML] files.
- You can apply consistent code styles to your [YAML] files.
- Supports [Vue SFC](https://vue-loader.vuejs.org/spec.html) custom blocks such as `<i18n lang="yaml">`.  
  Requirements `vue-eslint-parser` v7.3.0 and above.
- Supports ESLint directives. e.g. `# eslint-disable-next-line`
- You can check your code in real-time using the ESLint editor integrations.

You can check on the [Online DEMO](https://ota-meshi.github.io/eslint-plugin-yml/playground/).

## :question: How is it different from other YAML plugins?

### Plugins that do not use AST

e.g. [eslint-plugin-yaml](https://www.npmjs.com/package/eslint-plugin-yaml)

These plugins use the processor to parse and return the results independently, without providing the ESLint engine with AST and source code text.

Plugins don't provide AST, so you can't use directive comments (e.g. `# eslint-disable`).  
Plugins don't provide source code text, so you can't use it with plugins and rules that use text (e.g. [eslint-plugin-prettier](https://github.com/prettier/eslint-plugin-prettier), [eol-last](https://eslint.org/docs/rules/eol-last)).

**eslint-plugin-yml** works by providing AST and source code text to ESLint.

<!--DOCS_IGNORE_START-->

## :book: Documentation

See [documents](https://ota-meshi.github.io/eslint-plugin-yml/).

## :cd: Installation

```bash
npm install --save-dev eslint eslint-plugin-yml
```

> **Requirements**
>
> - ESLint v9.38.0 and above
> - Node.js v20.19.0 or higher (in the 20.x line), v22.13.0 or higher (in the 22.x line), or v24.0.0 and above

<!--DOCS_IGNORE_END-->

## :book: Usage

<!--USAGE_SECTION_START-->
<!--USAGE_GUIDE_START-->

### Configuration

Use `eslint.config.js` file to configure rules. See also: <https://eslint.org/docs/latest/use/configure/configuration-files-new>.

Example **eslint.config.js**:

```js
import eslintPluginYml from 'eslint-plugin-yml';
export default [
  // add more generic rule sets here, such as:
  // js.configs.recommended,
  ...eslintPluginYml.configs.recommended,
  {
    rules: {
      // override/add rules settings here, such as:
    // 'yml/rule-name': 'error'
    }
  }
];
```

This plugin provides configs:

- `*.configs.base` ... Configuration to enable correct YAML parsing.
- `*.configs.recommended` ... Above, plus rules to prevent errors or unintended behavior.
- `*.configs.standard` ... Above, plus rules to enforce the common stylistic conventions.
- `*.configs.prettier` ... Turn off rules that may conflict with [Prettier](https://prettier.io/).

See [the rule list](https://ota-meshi.github.io/eslint-plugin-yml/rules/) to get the `rules` that this plugin provides.

**Note:** The `*.configs['flat/*']` configs are still available for backward compatibility, but it is recommended to use the new config names without the `flat/` prefix.

#### Parser Configuration

If you have specified a parser, you need to configure a parser for `.yaml`.

For example, if you are using the `"@babel/eslint-parser"`, configure it as follows:

```js
import eslintPluginYml from 'eslint-plugin-yml';
import babelParser from '@babel/eslint-parser';

export default [
  ...eslintPluginYml.configs.standard,
  {
    files: ['**/*.js'],
    languageOptions: {
      parser: babelParser,
    },
  },
  // YAML files are already configured by the plugin
];
```

#### Parser Options

The following parser options for `yaml-eslint-parser` are available by specifying them in [parserOptions](https://eslint.org/docs/latest/user-guide/configuring/language-options#specifying-parser-options) in the ESLint configuration file.

```js
import eslintPluginYml from 'eslint-plugin-yml';

export default [
  ...eslintPluginYml.configs.recommended,
  {
    files: ['**/*.yaml', '**/*.yml'],
    languageOptions: {
      parserOptions: {
        defaultYAMLVersion: '1.2',
      },
    },
  },
];
```

See also [https://github.com/ota-meshi/yaml-eslint-parser#readme](https://github.com/ota-meshi/yaml-eslint-parser#readme).

### Running ESLint from the command line

With ESLint v9 and flat config, ESLint automatically lints all files matched by your config. You typically don't need the `--ext` option anymore.

Examples:

```bash
eslint .
eslint "src/**/*.{js,yaml,yml}"
```

#### Languages

This plugin provides the following language identifiers for use in ESLint configurations:

- `yml/yaml` ... YAML files

For example, to apply settings specifically to YAML files, you can use the `language` field in your ESLint configuration:

```js
import eslintPluginYml from 'eslint-plugin-yml';
export default [
  {
    files: ["*.yaml", "*.yml", "**/*.yaml", "**/*.yml"],
    plugins: {
      yml: eslintPluginYml,
    },
    language: "yml/yaml",
  }
]
```

The configuration above is included in the shareable configs provided by this plugin, so using `configs` is generally recommended.

See also <https://eslint.org/docs/latest/use/configure/plugins#specify-a-language>

## :computer: Editor Integrations

### Visual Studio Code

Use the [dbaeumer.vscode-eslint](https://marketplace.visualstudio.com/items?itemName=dbaeumer.vscode-eslint) extension that Microsoft provides officially.

You have to configure the `eslint.validate` option of the extension to check `.yaml` files, because the extension targets only `*.js` or `*.jsx` files by default.

Example **.vscode/settings.json**:

```json
{
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "yaml",
    "github-actions-workflow" // for GitHub Actions workflow files
  ]
}
```

### JetBrains WebStorm IDEs

In any of the JetBrains IDEs you can [configure the linting scope](https://www.jetbrains.com/help/webstorm/eslint.html#ws_eslint_configure_scope).
Following the steps in their help document, you can add YAML files to the scope like so:

1. Open the **Settings/Preferences** dialog, go to **Languages and Frameworks** | **JavaScript** | **Code Quality Tools** | **ESLint**, and select **Automatic ESLint configuration** or **Manual ESLint configuration**.
2. In the **Run for files** field, update the pattern that defines the set of files to be linted to include YAML files as well:

```
{**/*,*}.{js,ts,jsx,tsx,html,vue,yaml,yml}
                                 ^^^^ ^^^
```

<!--USAGE_GUIDE_END-->
<!--USAGE_SECTION_END-->

## :white_check_mark: Rules

<!--RULES_SECTION_START-->

The `--fix` option on the [command line](https://eslint.org/docs/user-guide/command-line-interface#fixing-problems) automatically fixes problems reported by rules which have a wrench :wrench: below.  
The rules with the following star :star: are included in the config.

<!--RULES_TABLE_START-->

### YAML Rules

| Rule ID | Description | Fixable | RECOMMENDED | STANDARD |
|:--------|:------------|:-------:|:-----------:|:--------:|
| [yml/block-mapping-colon-indicator-newline](https://ota-meshi.github.io/eslint-plugin-yml/rules/block-mapping-colon-indicator-newline.html) | enforce consistent line breaks after `:` indicator | :wrench: |  | :star: |
| [yml/block-mapping-question-indicator-newline](https://ota-meshi.github.io/eslint-plugin-yml/rules/block-mapping-question-indicator-newline.html) | enforce consistent line breaks after `?` indicator | :wrench: |  | :star: |
| [yml/block-mapping](https://ota-meshi.github.io/eslint-plugin-yml/rules/block-mapping.html) | require or disallow block style mappings. | :wrench: |  | :star: |
| [yml/block-sequence-hyphen-indicator-newline](https://ota-meshi.github.io/eslint-plugin-yml/rules/block-sequence-hyphen-indicator-newline.html) | enforce consistent line breaks after `-` indicator | :wrench: |  | :star: |
| [yml/block-sequence](https://ota-meshi.github.io/eslint-plugin-yml/rules/block-sequence.html) | require or disallow block style sequences. | :wrench: |  | :star: |
| [yml/file-extension](https://ota-meshi.github.io/eslint-plugin-yml/rules/file-extension.html) | enforce YAML file extension |  |  |  |
| [yml/indent](https://ota-meshi.github.io/eslint-plugin-yml/rules/indent.html) | enforce consistent indentation | :wrench: |  | :star: |
| [yml/key-name-casing](https://ota-meshi.github.io/eslint-plugin-yml/rules/key-name-casing.html) | enforce naming convention to key names |  |  |  |
| [yml/no-empty-document](https://ota-meshi.github.io/eslint-plugin-yml/rules/no-empty-document.html) | disallow empty document |  | :star: | :star: |
| [yml/no-empty-key](https://ota-meshi.github.io/eslint-plugin-yml/rules/no-empty-key.html) | disallow empty mapping keys |  | :star: | :star: |
| [yml/no-empty-mapping-value](https://ota-meshi.github.io/eslint-plugin-yml/rules/no-empty-mapping-value.html) | disallow empty mapping values |  | :star: | :star: |
| [yml/no-empty-sequence-entry](https://ota-meshi.github.io/eslint-plugin-yml/rules/no-empty-sequence-entry.html) | disallow empty sequence entries |  | :star: | :star: |
| [yml/no-tab-indent](https://ota-meshi.github.io/eslint-plugin-yml/rules/no-tab-indent.html) | disallow tabs for indentation. |  | :star: | :star: |
| [yml/no-trailing-zeros](https://ota-meshi.github.io/eslint-plugin-yml/rules/no-trailing-zeros.html) | disallow trailing zeros for floats | :wrench: |  | :star: |
| [yml/plain-scalar](https://ota-meshi.github.io/eslint-plugin-yml/rules/plain-scalar.html) | require or disallow plain style scalar. | :wrench: |  | :star: |
| [yml/quotes](https://ota-meshi.github.io/eslint-plugin-yml/rules/quotes.html) | enforce the consistent use of either double, or single quotes | :wrench: |  | :star: |
| [yml/require-string-key](https://ota-meshi.github.io/eslint-plugin-yml/rules/require-string-key.html) | disallow mapping keys other than strings |  |  |  |
| [yml/sort-keys](https://ota-meshi.github.io/eslint-plugin-yml/rules/sort-keys.html) | require mapping keys to be sorted | :wrench: |  |  |
| [yml/sort-sequence-values](https://ota-meshi.github.io/eslint-plugin-yml/rules/sort-sequence-values.html) | require sequence values to be sorted | :wrench: |  |  |
| [yml/vue-custom-block/no-parsing-error](https://ota-meshi.github.io/eslint-plugin-yml/rules/vue-custom-block/no-parsing-error.html) | disallow parsing errors in Vue custom blocks |  | :star: | :star: |

### Extension Rules

| Rule ID | Description | Fixable | RECOMMENDED | STANDARD |
|:--------|:------------|:-------:|:-----------:|:--------:|
| [yml/flow-mapping-curly-newline](https://ota-meshi.github.io/eslint-plugin-yml/rules/flow-mapping-curly-newline.html) | enforce consistent line breaks inside braces | :wrench: |  | :star: |
| [yml/flow-mapping-curly-spacing](https://ota-meshi.github.io/eslint-plugin-yml/rules/flow-mapping-curly-spacing.html) | enforce consistent spacing inside braces | :wrench: |  | :star: |
| [yml/flow-sequence-bracket-newline](https://ota-meshi.github.io/eslint-plugin-yml/rules/flow-sequence-bracket-newline.html) | enforce linebreaks after opening and before closing flow sequence brackets | :wrench: |  | :star: |
| [yml/flow-sequence-bracket-spacing](https://ota-meshi.github.io/eslint-plugin-yml/rules/flow-sequence-bracket-spacing.html) | enforce consistent spacing inside flow sequence brackets | :wrench: |  | :star: |
| [yml/key-spacing](https://ota-meshi.github.io/eslint-plugin-yml/rules/key-spacing.html) | enforce consistent spacing between keys and values in mapping pairs | :wrench: |  | :star: |
| [yml/no-irregular-whitespace](https://ota-meshi.github.io/eslint-plugin-yml/rules/no-irregular-whitespace.html) | disallow irregular whitespace |  | :star: | :star: |
| [yml/no-multiple-empty-lines](https://ota-meshi.github.io/eslint-plugin-yml/rules/no-multiple-empty-lines.html) | disallow multiple empty lines | :wrench: |  | :star: |
| [yml/spaced-comment](https://ota-meshi.github.io/eslint-plugin-yml/rules/spaced-comment.html) | enforce consistent spacing after the `#` in a comment | :wrench: |  | :star: |

<!--RULES_TABLE_END-->
<!--RULES_SECTION_END-->

## :rocket: To Do More Verification

### Verify using JSON Schema

You can verify using JSON Schema by checking and installing [eslint-plugin-json-schema-validator].

### Verify the [Vue I18n] message resource files

You can verify the message files by checking and installing [@intlify/eslint-plugin-vue-i18n].

<!--DOCS_IGNORE_START-->

## :traffic_light: Semantic Versioning Policy

**eslint-plugin-yml** follows [Semantic Versioning](http://semver.org/) and [ESLint's Semantic Versioning Policy](https://github.com/eslint/eslint#semantic-versioning-policy).

## :beers: Contributing

Welcome contributing!

Please use GitHub's Issues/PRs.

### Development Tools

- `npm test` runs tests and measures coverage.
- `npm run update` runs in order to update readme and recommended configuration.

### Working With Rules

This plugin uses [yaml-eslint-parser](https://github.com/ota-meshi/yaml-eslint-parser) for the parser. Check [here](https://ota-meshi.github.io/yaml-eslint-parser/) to find out about AST.

<!--DOCS_IGNORE_END-->

## :couple: Related Packages

- [eslint-plugin-jsonc](https://github.com/ota-meshi/eslint-plugin-jsonc) ... ESLint plugin for JSON, JSON with comments (JSONC) and JSON5.
- [eslint-plugin-toml](https://github.com/ota-meshi/eslint-plugin-toml) ... ESLint plugin for TOML.
- [eslint-plugin-json-schema-validator](https://github.com/ota-meshi/eslint-plugin-json-schema-validator) ... ESLint plugin that validates data using JSON Schema Validator.
- [jsonc-eslint-parser](https://github.com/ota-meshi/jsonc-eslint-parser) ... JSON, JSONC and JSON5 parser for use with ESLint plugins.
- [yaml-eslint-parser](https://github.com/ota-meshi/yaml-eslint-parser) ... YAML parser for use with ESLint plugins.
- [toml-eslint-parser](https://github.com/ota-meshi/toml-eslint-parser) ... TOML parser for use with ESLint plugins.

## :lock: License

See the [LICENSE](LICENSE) file for license rights and limitations (MIT).

[yaml]: https://yaml.org/
[eslint-plugin-json-schema-validator]: https://github.com/ota-meshi/eslint-plugin-json-schema-validator
[@intlify/eslint-plugin-vue-i18n]: https://github.com/intlify/eslint-plugin-vue-i18n
[vue i18n]: https://github.com/intlify/vue-i18n-next
