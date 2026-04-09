# find-up

> Find a file or directory by walking up parent directories or down descendant directories

## Install

```sh
npm install find-up
```

## Usage

```
/
└── Users
    └── sindresorhus
        ├── unicorn.png
        └── foo
            └── bar
                ├── baz
                └── example.js
```

`example.js`

```js
import path from 'node:path';
import {pathExists} from 'path-exists';
import {findUp, findDown} from 'find-up';

console.log(await findUp('unicorn.png'));
//=> '/Users/sindresorhus/unicorn.png'

console.log(await findUp(['rainbow.png', 'unicorn.png']));
//=> '/Users/sindresorhus/unicorn.png'

console.log(await findUp(async directory => {
	const hasUnicorn = await pathExists(path.join(directory, 'unicorn.png'));
	return hasUnicorn && directory;
}, {type: 'directory'}));
//=> '/Users/sindresorhus'

// Find .git (could be a file or directory, common in submodules)
console.log(await findUp('.git', {type: 'both'}));
//=> '/Users/sindresorhus/.git'
```

## API

### findUp(name, options?)
### findUp(matcher, options?)

Returns a `Promise` for either the path or `undefined` if it could not be found.

### findUp([...name], options?)

Returns a `Promise` for either the first path found (by respecting the order of names) or `undefined` if none could be found.

### findUpMultiple(name, options?)
### findUpMultiple(matcher, options?)

Returns a `Promise` for either an array of all paths found or an empty array if none could be found.

**Note:** You can limit the number of matches by setting the `limit` option.

### findUpMultiple([...name], options?)

Returns a `Promise` for either an array of all paths found (by respecting the order of names) or an empty array if none could be found.

**Note:** You can limit the number of matches by setting the `limit` option.

### findUpSync(name, options?)
### findUpSync(matcher, options?)

Returns a path or `undefined` if it could not be found.

### findUpSync([...name], options?)

Returns the first path found (by respecting the order of names) or `undefined` if none could be found.

### findUpMultipleSync(name, options?)
### findUpMultipleSync(matcher, options?)

Returns an array of all paths found or an empty array if none could be found.

### findUpMultipleSync([...name], options?)

Returns an array of all paths found (by respecting the order of names) or an empty array if none could be found.

**Note:** You can limit the number of matches by setting the `limit` option.

### findDown(name, options?)
### findDown([...name], options?)

Find a file or directory by walking down descendant directories from `cwd`.

Returns a `Promise` for either the path or `undefined` if it could not be found.

```js
import {findUp, findDown} from 'find-up';

// Find the nearest parent directory that contains a specific file
// in its direct children (useful for monorepo roots)
console.log(await findUp(async directory => {
	return findDown('example.js', {cwd: directory, depth: 1});
}));
//=> '/Users/sindresorhus/foo'
```

### findDownSync(name, options?)
### findDownSync([...name], options?)

Synchronous version of `findDown`.

Returns the path or `undefined` if it could not be found.

#### name

Type: `string`

The name of the file or directory to find. Can be an array of names to search for multiple files.

#### matcher

Type: `Function`

Called for each directory in the search. Return a path or `findUpStop` to stop the search. Useful if you want to match files with certain patterns, set of permissions, or other advanced use-cases.

#### options

Type: `object`

##### cwd

Type: `URL | string`\
Default: `process.cwd()`

The directory to start from.

##### type

Type: `string`\
Default: `'file'`\
Values: `'file' | 'directory' | 'both'`

The type of path to match.

##### allowSymlinks

Type: `boolean`\
Default: `true`

Allow symbolic links to match if they point to the chosen path type.

##### stopAt

*Only for `findUp` functions*

Type: `URL | string`\
Default: Root directory

A directory path where the search halts if no matches are found before reaching this point.

##### limit

*Only for `findUpMultiple` and `findUpMultipleSync`*

Type: `number`\
Default: `Infinity`

The maximum number of matches to return. Useful for limiting results when searching for multiple files.

### findUpStop

A [`Symbol`](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Symbol) that can be returned by a `matcher` function to stop the search and cause `findUp` to immediately return `undefined`. Useful as a performance optimization in case the current working directory is deeply nested in the filesystem.

```js
import path from 'node:path';
import {findUp, findUpStop} from 'find-up';

await findUp(directory => {
	// Stop searching if we've reached a 'work' directory
	if (path.basename(directory) === 'work') {
		return findUpStop;
	}

	// Look for package.json in this directory
	return 'package.json';
});
```

### findDown options

Type: `object`

##### cwd

Type: `URL | string`\
Default: `process.cwd()`

The directory to start from.

##### depth

Type: `number`\
Default: `1`

Maximum number of directory levels to traverse below `cwd`.

##### type

Type: `string`\
Default: `'file'`\
Values: `'file' | 'directory' | 'both'`

The type of path to match.

##### allowSymlinks

Type: `boolean`\
Default: `true`

Allow symbolic links to match if they point to the chosen path type.

##### strategy

Type: `string`\
Default: `'breadth'`\
Values: `'breadth' | 'depth'`

Search strategy to use:
- `'breadth'`: Breadth-first search, finds shallower matches first.
- `'depth'`: Depth-first search, fully explores each branch before moving to the next.

## Related

- [find-up-cli](https://github.com/sindresorhus/find-up-cli) - CLI for this module
- [package-up](https://github.com/sindresorhus/package-up) - Find the closest package.json file
- [package-directory](https://github.com/sindresorhus/package-directory) - Find the root directory of an npm package
- [resolve-from](https://github.com/sindresorhus/resolve-from) - Resolve the path of a module like `require.resolve()` but from a given path
