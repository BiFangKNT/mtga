# @ota-meshi/ast-token-store

[![NPM version](https://img.shields.io/npm/v/@ota-meshi/ast-token-store.svg)](https://www.npmjs.com/package/@ota-meshi/ast-token-store)
[![NPM license](https://img.shields.io/npm/l/@ota-meshi/ast-token-store.svg)](https://github.com/ota-meshi/ast-token-store/blob/main/LICENSE)

A class library that provides an API similar to [ESLint's SourceCode#getFirstToken and related methods](https://eslint.org/docs/latest/extend/custom-rules#accessing-the-source-code) for any AST.

## Installation

```bash
npm install @ota-meshi/ast-token-store
```

## Requirements

- Node.js `^20.19.0 || ^22.13.0 || >=24`

## Usage

### Basic Example

The `TokenStore` class provides a way to query tokens from any AST that uses `range: [number, number]` to represent source locations.

```ts
import { TokenStore } from "@ota-meshi/ast-token-store";

// Define your TokenStore subclass (or use it directly)
const store = new TokenStore({
  // Provide all tokens and comments, sorted or unsorted
  tokens: [...ast.tokens, ...ast.comments],
  // A type guard to distinguish comments from regular tokens
  isComment: (token): token is Comment => token.type === "Comment",
});
```

### Constructor

```ts
new TokenStore<Node, Token, Comment>({
  tokens: (Token | Comment)[],
  isComment: (token: Token | Comment) => token is Comment,
})
```

- **`tokens`** — An array of all tokens and comments.
- **`isComment`** — A type guard function that returns `true` if a given token is a comment.

The class has three generic type parameters:

| Parameter | Description                                             |
| --------- | ------------------------------------------------------- |
| `Node`    | The AST node type (must have `range: [number, number]`) |
| `Token`   | The token type (must have `range: [number, number]`)    |
| `Comment` | The comment type (must have `range: [number, number]`)  |

### Methods

All methods accept options for filtering, skipping, counting, and including comments.

#### Single Token Methods

| Method                                        | Description                                            |
| --------------------------------------------- | ------------------------------------------------------ |
| `getFirstToken(node, options?)`               | Gets the first token of the given node                 |
| `getLastToken(node, options?)`                | Gets the last token of the given node                  |
| `getTokenAfter(node, options?)`               | Gets the token that follows the given node             |
| `getTokenBefore(node, options?)`              | Gets the token that precedes the given node            |
| `getFirstTokenBetween(left, right, options?)` | Gets the first token between two non-overlapping nodes |
| `getLastTokenBetween(left, right, options?)`  | Gets the last token between two non-overlapping nodes  |

#### Multiple Token Methods

| Method                                         | Description                                         |
| ---------------------------------------------- | --------------------------------------------------- |
| `getFirstTokens(node, options?)`               | Gets the first `count` tokens of the given node     |
| `getLastTokens(node, options?)`                | Gets the last `count` tokens of the given node      |
| `getTokensAfter(node, options?)`               | Gets the `count` tokens that follow the given node  |
| `getTokensBefore(node, options?)`              | Gets the `count` tokens that precede the given node |
| `getFirstTokensBetween(left, right, options?)` | Gets the first `count` tokens between two nodes     |
| `getLastTokensBetween(left, right, options?)`  | Gets the last `count` tokens between two nodes      |
| `getTokens(node, options?)`                    | Gets all tokens within the given node               |
| `getTokensBetween(left, right, options?)`      | Gets all tokens between two nodes                   |
| `getAllTokens()`                               | Gets all tokens including comments                  |

#### Comment Methods

| Method                              | Description                                                  |
| ----------------------------------- | ------------------------------------------------------------ |
| `getAllComments()`                  | Gets all comment tokens                                      |
| `getCommentsInside(nodeOrToken)`    | Gets all comment tokens inside the given node/token          |
| `getCommentsBefore(nodeOrToken)`    | Gets all comment tokens directly before the given node/token |
| `getCommentsAfter(nodeOrToken)`     | Gets all comment tokens directly after the given node/token  |
| `commentsExistBetween(left, right)` | Checks if any comments exist between two nodes               |

#### Spacing Methods

| Method                        | Description                                                     |
| ----------------------------- | --------------------------------------------------------------- |
| `isSpaceBetween(left, right)` | Checks if there is whitespace between two non-overlapping nodes |

### Options

Single token methods (`getFirstToken`, `getLastToken`, etc.) accept skip options:

```ts
// Skip N tokens
store.getFirstToken(node, { skip: 1 });
// Shorthand: pass a number directly
store.getFirstToken(node, 1);

// Filter tokens
store.getFirstToken(node, {
  filter: (token) => token.type === "Punctuator",
});

// Include comments in the search
store.getFirstToken(node, { includeComments: true });
```

Multiple token methods (`getFirstTokens`, `getTokensAfter`, etc.) accept count options:

```ts
// Get up to N tokens
store.getFirstTokens(node, { count: 3 });
// Shorthand: pass a number directly
store.getFirstTokens(node, 3);

// Filter and count
store.getTokensAfter(node, {
  filter: (token) => token.type === "Punctuator",
  count: 2,
});

// Include comments
store.getTokens(node, { includeComments: true });
```

## Attribution

This library aims for compatibility with ESLint's `SourceCode` token API and its method surface. The method design follows ideas described by ESLint, which is licensed under MIT. The implementation here is original and does not reuse ESLint code.

ESLint is distributed under the MIT License. See the ESLint repository for details: <https://github.com/eslint/eslint/blob/main/LICENSE>

## License

[MIT](./LICENSE)
