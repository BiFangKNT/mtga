# Tailwind CSSTree

by [Nicholas C. Zakas](https://humanwhocodes.com)

If you find this useful, please consider supporting my work with a [donation](https://humanwhocodes.com/donate).

## Description

Tailwind custom syntax in CSSTree format. 

## Installation

```shell
npm install @humanwhocodes/tailwind-csstree
```

## Usage

This package exports the following objects:

- `tailwind3` - CSSTree syntax extensions for Tailwind 3 syntax
- `tailwind4` - CSSTree syntax extensions for Tailwind 4 syntax

You can import them like this:

```js
import { tailwind3, tailwind4 } from "tailwind-csstree";
```

### Use with ESLint CSS Plugin

To use this package with the [ESLint CSS plugin](https://github.com/eslint/css), use `languageOptions.customSyntax` to specify the Tailwind version you'd like to use in your `eslint.config.js` file:

```js
// eslint.config.js
import { defineConfig } from "eslint/config";
import css from "@eslint/css";
import { tailwind4 } from "tailwind-csstree";

export default defineConfig([
	{
		files: ["**/*.css"],
		plugins: {
			css,
		},
		language: "css/css",
		languageOptions: {
			customSyntax: tailwind4,
		},
		rules: {
			"css/no-empty-blocks": "error",
		},
	},
]);
```

**Note:** Not all ESLint CSS plugin rules will work with Tailwind syntax. That's something I'm actively working on.

### Use with CSSTree directly

If you're using [CSSTree](https://github.com/eslint/css-tree) directly, you 

```js
import { fork } from "@eslint/css-tree";
import { tailwind4 } from "tailwind-csstree";

const {
    parse,
    toPlainObject
} = fork(tailwind4);

const result = parse("@config 'tailwind.config.js'");
console.log(toPlainObject(result));
```

## License

Copyright 2025 Nicholas C. Zakas

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
