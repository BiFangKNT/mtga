import {type Get} from 'type-fest';

/**
Get the value of the property at the given path.

@param object - Object or array to get the `path` value.
@param path - Path of the property in the object, using `.` to separate each nested key. Use `\\.` if you have a `.` in the key. Array indices can be accessed using bracket notation (`'users[0].name'`) or dot notation (`'users.0.name'`). Both syntaxes are equivalent and will create arrays when setting values. Numeric strings in dot notation (like `'users.0.name'`) are automatically coerced to numbers. When using array paths, numeric strings are normalized to numbers for simplicity (treating `['users', '0']` the same as `['users', 0]`).
@param defaultValue - Default value.

@example
```
import {getProperty} from 'dot-prop';

getProperty({foo: {bar: 'unicorn'}}, 'foo.bar');
//=> 'unicorn'

getProperty({foo: {bar: 'a'}}, 'foo.notDefined.deep');
//=> undefined

getProperty({foo: {bar: 'a'}}, 'foo.notDefined.deep', 'default value');
//=> 'default value'

getProperty({foo: {'dot.dot': 'unicorn'}}, 'foo.dot\\.dot');
//=> 'unicorn'

getProperty({foo: [{bar: 'unicorn'}]}, 'foo[0].bar');
//=> 'unicorn'

getProperty({foo: [{bar: 'unicorn'}]}, 'foo.0.bar');
//=> 'unicorn'
```
*/
export function getProperty<ObjectType, PathType extends string, DefaultValue = undefined>(
	object: ObjectType,
	path: PathType | ReadonlyArray<string | number>,
	defaultValue?: DefaultValue
): ObjectType extends Record<string, unknown> | unknown[]
	? (unknown extends Get<ObjectType, PathType> ? DefaultValue : Get<ObjectType, PathType>)
	: DefaultValue extends undefined ? unknown : DefaultValue;

/**
Set the property at the given path to the given value.

@param object - Object or array to set the `path` value.
@param path - Path of the property in the object, using `.` to separate each nested key. Use `\\.` if you have a `.` in the key. Array indices can be accessed using bracket notation (`'users[0].name'`) or dot notation (`'users.0.name'`). Both syntaxes are equivalent and will create arrays when setting values. Numeric strings in dot notation (like `'users.0.name'`) are automatically coerced to numbers. When using array paths, numeric strings are normalized to numbers for simplicity (treating `['users', '0']` the same as `['users', 0]`).
@param value - Value to set at `path`.
@returns The object.

@example
```
import {setProperty} from 'dot-prop';

const object = {foo: {bar: 'a'}};
setProperty(object, 'foo.bar', 'b');
console.log(object);
//=> {foo: {bar: 'b'}}

const foo = setProperty({}, 'foo.bar', 'c');
console.log(foo);
//=> {foo: {bar: 'c'}}

setProperty(object, 'foo.baz', 'x');
console.log(object);
//=> {foo: {bar: 'b', baz: 'x'}}

setProperty(object, 'foo.biz[0]', 'a');
console.log(object);
//=> {foo: {bar: 'b', baz: 'x', biz: ['a']}}

setProperty(object, 'foo.items.0', 'first');
console.log(object);
//=> {foo: {bar: 'b', baz: 'x', biz: ['a'], items: ['first']}}
```
*/
export function setProperty<ObjectType extends (Record<string, any> | unknown[])>(
	object: ObjectType,
	path: string | ReadonlyArray<string | number>,
	value: unknown
): ObjectType;

/**
Check whether the property at the given path exists.

@param object - Object or array to test the `path` value.
@param path - Path of the property in the object, using `.` to separate each nested key. Use `\\.` if you have a `.` in the key. Array indices can be accessed using bracket notation (`'users[0].name'`) or dot notation (`'users.0.name'`). Both syntaxes are equivalent and will create arrays when setting values. Numeric strings in dot notation (like `'users.0.name'`) are automatically coerced to numbers. When using array paths, numeric strings are normalized to numbers for simplicity (treating `['users', '0']` the same as `['users', 0]`).

@example
```
import {hasProperty} from 'dot-prop';

hasProperty({foo: {bar: 'unicorn'}}, 'foo.bar');
//=> true
```
*/
export function hasProperty(object: Record<string, any> | unknown[] | undefined, path: string | ReadonlyArray<string | number>): boolean;

/**
Delete the property at the given path.

@param object - Object or array to delete the `path` value.
@param path - Path of the property in the object, using `.` to separate each nested key. Use `\\.` if you have a `.` in the key. Array indices can be accessed using bracket notation (`'users[0].name'`) or dot notation (`'users.0.name'`). Both syntaxes are equivalent and will create arrays when setting values. Numeric strings in dot notation (like `'users.0.name'`) are automatically coerced to numbers. When using array paths, numeric strings are normalized to numbers for simplicity (treating `['users', '0']` the same as `['users', 0]`).
@returns A boolean of whether the property existed before being deleted.

@example
```
import {deleteProperty} from 'dot-prop';

const object = {foo: {bar: 'a'}};
deleteProperty(object, 'foo.bar');
console.log(object);
//=> {foo: {}}

object.foo.bar = {x: 'y', y: 'x'};
deleteProperty(object, 'foo.bar.x');
console.log(object);
//=> {foo: {bar: {y: 'x'}}}
```
*/
export function deleteProperty(object: Record<string, any> | unknown[], path: string | ReadonlyArray<string | number>): boolean;

/**
Escape special characters in a path. Useful for sanitizing user input.

@param path - The dot path to sanitize.

@example
```
import {getProperty, escapePath} from 'dot-prop';

const object = {
	foo: {
		bar: '👸🏻 You found me Mario!',
	},
	'foo.bar' : '🍄 The princess is in another castle!',
};
const escapedPath = escapePath('foo.bar');

console.log(getProperty(object, escapedPath));
//=> '🍄 The princess is in another castle!'
```
*/
export function escapePath(path: string): string;

/**
Parse a dot path into an array of path segments.

@param path - Path to parse. Use `\\.` if you have a `.` in the key. Array indices can be accessed using bracket notation (`'users[0].name'`) or dot notation (`'users.0.name'`). Both syntaxes are equivalent. Numeric strings in dot notation (like `'users.0.name'`) are automatically coerced to numbers.
@returns An array of path segments where numbers represent array indices and strings represent object keys.

@example
```
import {parsePath} from 'dot-prop';

parsePath('foo.bar');
//=> ['foo', 'bar']

parsePath('foo[0].bar');
//=> ['foo', 0, 'bar']

parsePath('foo.0.bar');
//=> ['foo', 0, 'bar']

parsePath('foo\\.bar');
//=> ['foo.bar']

// Use case: Iterate over path segments to build up a nested object
const path = 'users[0].profile.settings.theme';
const segments = parsePath(path);
//=> ['users', 0, 'profile', 'settings', 'theme']
```
*/
export function parsePath(path: string): Array<string | number>;

/**
Convert an array of path segments back into a path string.

@param pathSegments - Array of path segments where numbers represent array indices and strings represent object keys.
@param options - Options for stringifying the path.

@example
```
import {stringifyPath} from 'dot-prop';

stringifyPath(['foo', 'bar']);
//=> 'foo.bar'

stringifyPath(['foo', 0, 'bar']);
//=> 'foo[0].bar'

stringifyPath(['foo', '0', 'bar']);
//=> 'foo[0].bar'

// With preferDotForIndices option
stringifyPath(['foo', 0, 'bar'], {preferDotForIndices: true});
//=> 'foo.0.bar'
```
*/
export function stringifyPath(pathSegments: ReadonlyArray<string | number>, options?: {preferDotForIndices?: boolean}): string;

/**
Returns an array of every path. Non-empty plain objects and arrays are deeply recursed and are not themselves included.

This can be useful to help flatten an object for an API that only accepts key-value pairs or for a tagged template literal.

@param object - The object to iterate through.

@example
```
import {getProperty, deepKeys} from 'dot-prop';

const user = {
	name: {
		first: 'Richie',
		last: 'Bendall',
	},
	activeTasks: [],
	currentProject: null
};

for (const property of deepKeys(user)) {
	console.log(`${property}: ${getProperty(user, property)}`);
	//=> name.first: Richie
	//=> name.last: Bendall
	//=> activeTasks: []
	//=> currentProject: null
}
```
*/
export function deepKeys(object: unknown): string[];

/**
Convert an object with dot paths into a nested object.

Uses the same path rules and escaping as the rest of the API.

@param object - A plain object mapping paths to values.
@returns A new nested object.

@example
```
import {unflatten} from 'dot-prop';

const flat = {
	'unicorn.name': 'Rainbow Dash',
	'unicorn.color': '🦄',
	'unicorn.treasures[0]': 'sparkles',
	'unicorn.treasures[1]': 'glitter',
};

unflatten(flat);
//=> {
//=> 	unicorn: {
//=> 		name: 'Rainbow Dash',
//=> 		color: '🦄',
//=> 		treasures: ['sparkles', 'glitter']
//=> 	}
//=> }
```
*/
export function unflatten(object: Record<string, unknown>): Record<string, unknown>;
