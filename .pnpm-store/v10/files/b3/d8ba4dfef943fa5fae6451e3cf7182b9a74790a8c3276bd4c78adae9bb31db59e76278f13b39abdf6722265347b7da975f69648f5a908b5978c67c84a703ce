import {type Options as LocatePathOptions} from 'locate-path';

/**
Return this in a `matcher` function to stop the search and force `findUp` to immediately return `undefined`.
*/
export const findUpStop: unique symbol;

export type Match = string | typeof findUpStop | undefined;

export type Options = {
	/**
	A directory path where the search halts if no matches are found before reaching this point.

	Default: Root directory
	*/
	readonly stopAt?: string;

	/**
	The type of path to match.

	@default 'file'
	*/
	readonly type?: 'file' | 'directory' | 'both';

	/**
	The number of matches to limit the search to.

	@default Infinity

	Only available for `findUpMultiple` and `findUpMultipleSync`.
	*/
	readonly limit?: number;
} & Omit<LocatePathOptions, 'type'>;

/**
Find a file or directory by walking up parent directories.

@param name - The name of the file or directory to find. Can be an array of names to search for multiple files.
@returns The first path found (by respecting the order of names) or `undefined` if none could be found.

@example
```
// /
// └── Users
//     └── sindresorhus
//         ├── unicorn.png
//         └── foo
//             └── bar
//                 ├── baz
//                 └── example.js

// example.js
import {findUp} from 'find-up';

console.log(await findUp('unicorn.png'));
//=> '/Users/sindresorhus/unicorn.png'

console.log(await findUp(['rainbow.png', 'unicorn.png']));
//=> '/Users/sindresorhus/unicorn.png'
```
*/
export function findUp(name: string | readonly string[], options?: Options): Promise<string | undefined>;

/**
Find a file or directory by walking up parent directories.

@param matcher - Called for each directory in the search. Return a path or `findUpStop` to stop the search.
@returns The path or `undefined` if it could not be found.

@example
```
import path from 'node:path';
import {pathExists} from 'path-exists';
import {findUp} from 'find-up';

console.log(await findUp(async directory => {
	const hasUnicorn = await pathExists(path.join(directory, 'unicorn.png'));
	return hasUnicorn && directory;
}, {type: 'directory'}));
//=> '/Users/sindresorhus'
```
*/
export function findUp(matcher: (directory: string) => (Match | Promise<Match>), options?: Options): Promise<string | undefined>;

/**
Synchronously find a file or directory by walking up parent directories.

@param name - The name of the file or directory to find. Can be an array of names to search for multiple files.
@returns The first path found (by respecting the order of names) or `undefined` if none could be found.

@example
```
// /
// └── Users
//     └── sindresorhus
//         ├── unicorn.png
//         └── foo
//             └── bar
//                 ├── baz
//                 └── example.js

// example.js
import {findUpSync} from 'find-up';

console.log(findUpSync('unicorn.png'));
//=> '/Users/sindresorhus/unicorn.png'

console.log(findUpSync(['rainbow.png', 'unicorn.png']));
//=> '/Users/sindresorhus/unicorn.png'
```
*/
export function findUpSync(name: string | readonly string[], options?: Options): string | undefined;

/**
Synchronously find a file or directory by walking up parent directories.

@param matcher - Called for each directory in the search. Return a path or `findUpStop` to stop the search.
@returns The path or `undefined` if it could not be found.

@example
```
import path from 'node:path';
import {pathExistsSync} from 'path-exists';
import {findUpSync} from 'find-up';

console.log(findUpSync(directory => {
	const hasUnicorn = pathExistsSync(path.join(directory, 'unicorn.png'));
	return hasUnicorn && directory;
}, {type: 'directory'}));
//=> '/Users/sindresorhus'
```
*/
export function findUpSync(matcher: (directory: string) => Match, options?: Options): string | undefined;

/**
Find files or directories by walking up parent directories.

@param name - The name of the file or directory to find. Can be an array of names to search for multiple files.
@returns An array of all paths found (by respecting the order of names) or an empty array if none could be found.

@example
```
// /
// └── Users
//     └── sindresorhus
//         ├── unicorn.png
//         └── foo
//             ├── unicorn.png
//             └── bar
//                 ├── baz
//                 └── example.js

// example.js
import {findUpMultiple} from 'find-up';

console.log(await findUpMultiple('unicorn.png'));
//=> ['/Users/sindresorhus/foo/unicorn.png', '/Users/sindresorhus/unicorn.png']

console.log(await findUpMultiple(['rainbow.png', 'unicorn.png']));
//=> ['/Users/sindresorhus/foo/unicorn.png', '/Users/sindresorhus/unicorn.png']
```
*/
export function findUpMultiple(name: string | readonly string[], options?: Options): Promise<string[]>;

/**
Find files or directories by walking up parent directories.

@param matcher - Called for each directory in the search. Return a path or `findUpStop` to stop the search.
@returns An array of all paths found or an empty array if none could be found.

@example
```
import path from 'node:path';
import {pathExists} from 'path-exists';
import {findUpMultiple} from 'find-up';

console.log(await findUpMultiple(async directory => {
	const hasUnicorn = await pathExists(path.join(directory, 'unicorn.png'));
	return hasUnicorn && directory;
}, {type: 'directory'}));
//=> ['/Users/sindresorhus/foo', '/Users/sindresorhus']
```
*/
export function findUpMultiple(matcher: (directory: string) => (Match | Promise<Match>), options?: Options): Promise<string[]>;

/**
Synchronously find files or directories by walking up parent directories.

@param name - The name of the file or directory to find. Can be an array of names to search for multiple files.
@returns An array of all paths found (by respecting the order of names) or an empty array if none could be found.

@example
```
// /
// └── Users
//     └── sindresorhus
//         ├── unicorn.png
//         └── foo
//             ├── unicorn.png
//             └── bar
//                 ├── baz
//                 └── example.js

// example.js
import {findUpMultipleSync} from 'find-up';

console.log(findUpMultipleSync('unicorn.png'));
//=> ['/Users/sindresorhus/foo/unicorn.png', '/Users/sindresorhus/unicorn.png']

console.log(findUpMultipleSync(['rainbow.png', 'unicorn.png']));
//=> ['/Users/sindresorhus/foo/unicorn.png', '/Users/sindresorhus/unicorn.png']
```
*/
export function findUpMultipleSync(name: string | readonly string[], options?: Options): string[];

/**
Synchronously find files or directories by walking up parent directories.

@param matcher - Called for each directory in the search. Return a path or `findUpStop` to stop the search.
@returns An array of all paths found or an empty array if none could be found.

@example
```
import path from 'node:path';
import {pathExistsSync} from 'path-exists';
import {findUpMultipleSync} from 'find-up';

console.log(findUpMultipleSync(directory => {
	const hasUnicorn = pathExistsSync(path.join(directory, 'unicorn.png'));
	return hasUnicorn && directory;
}, {type: 'directory'}));
//=> ['/Users/sindresorhus/foo', '/Users/sindresorhus']
```
*/
export function findUpMultipleSync(matcher: (directory: string) => Match, options?: Options): string[];

/**
Options for `findDown` and `findDownSync`.
*/
export type FindDownOptions = {
	/**
	The directory to start from.

	@default process.cwd()
	*/
	readonly cwd?: URL | string;

	/**
	Maximum number of directory levels to traverse below `cwd`.

	@default 1
	*/
	readonly depth?: number;

	/**
	The type of path to match.

	@default 'file'
	*/
	readonly type?: 'file' | 'directory' | 'both';

	/**
	Allow symbolic links to match if they point to the chosen path type.

	@default true
	*/
	readonly allowSymlinks?: boolean;

	/**
	Search strategy to use:
	- `'breadth'`: Breadth-first search, finds shallower matches first.
	- `'depth'`: Depth-first search, fully explores each branch before moving to the next.

	@default 'breadth'
	*/
	readonly strategy?: 'breadth' | 'depth';
};

/**
Find a file or directory by walking down descendant directories from `cwd`.

@param name - The name of the file or directory to find. Can be an array of names to search for multiple files.
@returns The path or `undefined` if it could not be found.

@example
```
import {findUp, findDown} from 'find-up';

// Find the nearest parent directory that contains a specific file
// in its direct children (useful for monorepo roots)
console.log(await findUp(async directory => {
	return findDown('example.js', {cwd: directory, depth: 1});
}));
//=> '/Users/sindresorhus/foo'
```
*/
export function findDown(name: string | readonly string[], options?: FindDownOptions): Promise<string | undefined>;

/**
Synchronously find a file or directory by walking down descendant directories from `cwd`.

@param name - The name of the file or directory to find. Can be an array of names to search for multiple files.
@returns The path or `undefined` if it could not be found.

@example
```
import {findUpSync, findDownSync} from 'find-up';

// Find the nearest parent directory that contains a specific file
// in its direct children (useful for monorepo roots)
console.log(findUpSync(async directory => {
	return findDownSync('example.js', {cwd: directory, depth: 1});
}));
//=> '/Users/sindresorhus/foo'
```

*/
export function findDownSync(name: string | readonly string[], options?: FindDownOptions): string | undefined;
