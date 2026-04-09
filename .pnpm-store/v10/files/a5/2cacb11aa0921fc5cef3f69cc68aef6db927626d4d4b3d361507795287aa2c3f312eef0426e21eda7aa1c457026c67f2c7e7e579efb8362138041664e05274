<img align="right" width="111" height="111" alt="CSSTree logo" src="assets/csstree-logo-rounded.svg" />

# CSSTree (ESLint Fork)

CSSTree is a tool set for CSS: [fast](https://github.com/postcss/benchmark) detailed parser (CSS → AST), walker (AST traversal), generator (AST → CSS) and lexer (validation and matching) based on specs and browser implementations. The main goal is to be efficient and W3C spec compliant, with focus on CSS analyzing and source-to-source transforming tasks.

## Features

- **Detailed parsing with an adjustable level of detail**

  By default CSSTree parses CSS as detailed as possible, i.e. each single logical part is representing with its own AST node (see [AST format](docs/ast.md) for all possible node types). The parsing detail level can be changed through [parser options](docs/parsing.md#parsesource-options), for example, you can disable parsing of selectors or declaration values for component parts.

- **Tolerant to errors by design**

  Parser behaves as [spec says](https://www.w3.org/TR/css-syntax-3/#error-handling): "When errors occur in CSS, the parser attempts to recover gracefully, throwing away only the minimum amount of content before returning to parsing as normal". The only thing the parser departs from the specification is that it doesn't throw away bad content, but wraps it in a special node type (`Raw`) that allows processing it later.

- **Fast and efficient**

  CSSTree is created with focus on performance and effective memory consumption. Therefore it's [one of the fastest CSS parsers](https://github.com/postcss/benchmark) at the moment.

- **Syntax validation**

  The built-in lexer can test CSS against syntaxes defined by W3C. CSSTree uses [mdn/data](https://github.com/mdn/data/) as a basis for lexer's dictionaries and extends it with vendor specific and legacy syntaxes. Lexer can only check the declaration values and at-rules currently, but this feature will be extended to other parts of the CSS in the future.

## Projects using CSSTree

- [Svelte](https://github.com/sveltejs/svelte) – Cybernetically enhanced web apps
- [SVGO](https://github.com/svg/svgo) – Node.js tool for optimizing SVG files
- [CSSO](https://github.com/css/csso) – CSS minifier with structural optimizations
- [NativeScript](https://github.com/NativeScript/NativeScript) – NativeScript empowers you to access native APIs from JavaScript directly
- [react-native-svg](https://github.com/react-native-svg/react-native-svg) – SVG library for React Native, React Native Web, and plain React web projects
- [penthouse](https://github.com/pocketjoso/penthouse) – Critical Path CSS Generator
- [Bit](https://github.com/teambit/bit) – Bit is the platform for collaborating on components
- and more...

## Documentation

- [AST format](docs/ast.md)
- [Parsing CSS → AST](docs/parsing.md)
  - [parse(source[, options])](docs/parsing.md#parsesource-options)
- [Serialization AST → CSS](docs/generate.md)
  - [generate(ast[, options])](docs/generate.md#generateast-options)
- [AST traversal](docs/traversal.md)
  - [walk(ast, options)](docs/traversal.md#walkast-options)
  - [find(ast, fn)](docs/traversal.md#findast-fn)
  - [findLast(ast, fn)](docs/traversal.md#findlastast-fn)
  - [findAll(ast, fn)](docs/traversal.md#findallast-fn)
- [Util functions](docs/utils.md)
  - Value encoding & decoding
    - [property(name)](docs/utils.md#propertyname)
    - [keyword(name)](docs/utils.md#keywordname)
    - [ident](docs/utils.md#ident)
    - [string](docs/utils.md#string)
    - [url](docs/utils.md#url)
  - [List class](docs/list.md)
  - AST transforming
    - [clone(ast)](docs/utils.md#cloneast)
    - [fromPlainObject(object)](docs/utils.md#fromplainobjectobject)
    - [toPlainObject(ast)](docs/utils.md#toplainobjectast)
- [Value Definition Syntax](docs/definition-syntax.md)
  - [parse(source)](docs/definition-syntax.md#parsesource)
  - [walk(node, options, context)](docs/definition-syntax.md#walknode-options-context)
  - [generate(node, options)](docs/definition-syntax.md#generatenode-options)
  - [AST format](docs/definition-syntax.md#ast-format)

## Tools

* [AST Explorer](https://astexplorer.net/#/gist/244e2fb4da940df52bf0f4b94277db44/e79aff44611020b22cfd9708f3a99ce09b7d67a8) – explore CSSTree AST format with zero setup
* [CSS syntax reference](https://csstree.github.io/docs/syntax.html)
* [CSS syntax validator](https://csstree.github.io/docs/validator.html)

## Related projects

* [csstree-validator](https://github.com/csstree/validator) – NPM package to validate CSS
* [stylelint-csstree-validator](https://github.com/csstree/stylelint-validator) – plugin for stylelint to validate CSS
* [Grunt plugin](https://github.com/sergejmueller/grunt-csstree-validator)
* [Gulp plugin](https://github.com/csstree/gulp-csstree)
* [Sublime plugin](https://github.com/csstree/SublimeLinter-contrib-csstree)
* [VS Code plugin](https://github.com/csstree/vscode-plugin)
* [Atom plugin](https://github.com/csstree/atom-plugin)

## Usage

Install with npm:

```
npm install @eslint/css-tree
```

Basic usage:

```js
import * as csstree from '@eslint/css-tree';

// parse CSS to AST
const ast = csstree.parse('.example { world: "!" }');

// traverse AST and modify it
csstree.walk(ast, (node) => {
    if (node.type === 'ClassSelector' && node.name === 'example') {
        node.name = 'hello';
    }
});

// generate CSS from AST
console.log(csstree.generate(ast));
// .hello{world:"!"}
```

Syntax matching:

```js
// parse CSS to AST as a declaration value
const ast = csstree.parse('red 1px solid', { context: 'value' });

// match to syntax of `border` property
const matchResult = csstree.lexer.matchProperty('border', ast);

// check first value node is a <color>
console.log(matchResult.isType(ast.children.first, 'color'));
// true

// get a type list matched to a node
console.log(matchResult.getTrace(ast.children.first));
// [ { type: 'Property', name: 'border' },
//   { type: 'Type', name: 'color' },
//   { type: 'Type', name: 'named-color' },
//   { type: 'Keyword', name: 'red' } ]
```

### Exports

Is it possible to import just a needed part of library like a parser or a walker. That's might useful for loading time or bundle size optimisations.

```js
import * as tokenizer from '@eslint/css-tree/tokenizer';
import * as parser from '@eslint/css-tree/parser';
import * as walker from '@eslint/css-tree/walker';
import * as lexer from '@eslint/css-tree/lexer';
import * as definitionSyntax from '@eslint/css-tree/definition-syntax';
import * as data from '@eslint/css-tree/definition-syntax-data';
import * as dataPatch from '@eslint/css-tree/definition-syntax-data-patch';
import * as utils from '@eslint/css-tree/utils';
```

### Using in a browser

Bundles are available for use in a browser:

- `dist/csstree.js` – minified IIFE with `csstree` as global
```html
<script src="node_modules/@eslint/css-tree/dist/csstree.js"></script>
<script>
  csstree.parse('.example { color: green }');
</script>
```

- `dist/csstree.esm.js` – minified ES module
```html
<script type="module">
  import { parse } from 'node_modules/@eslint/css-tree/dist/csstree.esm.js'
  parse('.example { color: green }');
</script>
```

One of CDN services like `unpkg` or `jsDelivr` can be used. By default (for short path) a ESM version is exposing. For IIFE version a full path to a bundle should be specified:

```html
<!-- ESM -->
<script type="module">
  import * as csstree from 'https://cdn.jsdelivr.net/npm/@eslint/css-tree';
  import * as csstree from 'https://unpkg.com/@eslint/css-tree';
</script>

<!-- IIFE with an export to global -->
<script src="https://cdn.jsdelivr.net/npm/@eslint/css-tree/dist/csstree.js"></script>
<script src="https://unpkg.com/@eslint/css-tree/dist/csstree.js"></script>
```

## Top level API

![API map](https://cdn.rawgit.com/eslint/csstree/aaf327e/docs/api-map.svg)

## License

MIT

## Branch Setup and Development

* `main` - the default branch for new development in the fork repo
* `upstream` - kept in sync with `csstree/csstree`

When merging in changes from `csstree/csstree`, sync `upstream` in the GitHub UI (if possible). Then send a pull request to `main` to work through any merge conflicts.

<!-- NOTE: This section is autogenerated. Do not manually edit.-->
<!--sponsorsstart-->

## Sponsors

The following companies, organizations, and individuals support ESLint's ongoing maintenance and development. [Become a Sponsor](https://eslint.org/donate)
to get your logo on our READMEs and [website](https://eslint.org/sponsors).

<h3>Platinum Sponsors</h3>
<p><a href="https://automattic.com"><img src="https://images.opencollective.com/automattic/d0ef3e1/logo.png" alt="Automattic" height="128"></a> <a href="https://www.airbnb.com/"><img src="https://images.opencollective.com/airbnb/d327d66/logo.png" alt="Airbnb" height="128"></a></p><h3>Gold Sponsors</h3>
<p><a href="https://qlty.sh/"><img src="https://images.opencollective.com/qltysh/33d157d/logo.png" alt="Qlty Software" height="96"></a> <a href="https://shopify.engineering/"><img src="https://avatars.githubusercontent.com/u/8085" alt="Shopify" height="96"></a></p><h3>Silver Sponsors</h3>
<p><a href="https://vite.dev/"><img src="https://images.opencollective.com/vite/e6d15e1/logo.png" alt="Vite" height="64"></a> <a href="https://liftoff.io/"><img src="https://images.opencollective.com/liftoff/2d6c3b6/logo.png" alt="Liftoff" height="64"></a> <a href="https://americanexpress.io"><img src="https://avatars.githubusercontent.com/u/3853301" alt="American Express" height="64"></a> <a href="https://stackblitz.com"><img src="https://avatars.githubusercontent.com/u/28635252" alt="StackBlitz" height="64"></a></p><h3>Bronze Sponsors</h3>
<p><a href="https://cybozu.co.jp/"><img src="https://images.opencollective.com/cybozu/933e46d/logo.png" alt="Cybozu" height="32"></a> <a href="https://syntax.fm"><img src="https://github.com/syntaxfm.png" alt="Syntax" height="32"></a> <a href="https://www.n-ix.com/"><img src="https://images.opencollective.com/n-ix-ltd/575a7a5/logo.png" alt="N-iX Ltd" height="32"></a> <a href="https://icons8.com/"><img src="https://images.opencollective.com/icons8/7fa1641/logo.png" alt="Icons8" height="32"></a> <a href="https://discord.com"><img src="https://images.opencollective.com/discordapp/f9645d9/logo.png" alt="Discord" height="32"></a> <a href="https://www.gitbook.com"><img src="https://avatars.githubusercontent.com/u/7111340" alt="GitBook" height="32"></a> <a href="https://nx.dev"><img src="https://avatars.githubusercontent.com/u/23692104" alt="Nx" height="32"></a> <a href="https://opensource.mercedes-benz.com/"><img src="https://avatars.githubusercontent.com/u/34240465" alt="Mercedes-Benz Group" height="32"></a> <a href="https://herocoders.com"><img src="https://avatars.githubusercontent.com/u/37549774" alt="HeroCoders" height="32"></a> <a href="https://www.lambdatest.com"><img src="https://avatars.githubusercontent.com/u/171592363" alt="LambdaTest" height="32"></a></p>
<h3>Technology Sponsors</h3>
Technology sponsors allow us to use their products and services for free as part of a contribution to the open source ecosystem and our work.
<p><a href="https://netlify.com"><img src="https://raw.githubusercontent.com/eslint/eslint.org/main/src/assets/images/techsponsors/netlify-icon.svg" alt="Netlify" height="32"></a> <a href="https://algolia.com"><img src="https://raw.githubusercontent.com/eslint/eslint.org/main/src/assets/images/techsponsors/algolia-icon.svg" alt="Algolia" height="32"></a> <a href="https://1password.com"><img src="https://raw.githubusercontent.com/eslint/eslint.org/main/src/assets/images/techsponsors/1password-icon.svg" alt="1Password" height="32"></a></p>
<!--sponsorsend-->
