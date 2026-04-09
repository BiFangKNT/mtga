# dot-prop

> Get, set, or delete a property from a nested object using a dot path

## Install

```sh
npm install dot-prop
```

## Usage

```js
import {getProperty, setProperty, hasProperty, deleteProperty} from 'dot-prop';

// Getter
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

// Setter
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

// Has
hasProperty({foo: {bar: 'unicorn'}}, 'foo.bar');
//=> true

// Deleter
const object = {foo: {bar: 'a'}};
deleteProperty(object, 'foo.bar');
console.log(object);
//=> {foo: {}}

object.foo.bar = {x: 'y', y: 'x'};
deleteProperty(object, 'foo.bar.x');
console.log(object);
//=> {foo: {bar: {y: 'x'}}}
```

### Array paths

For improved performance and interoperability with other libraries, you can also pass paths as arrays instead of strings. This avoids the overhead of parsing string paths.

```js
import {getProperty, setProperty} from 'dot-prop';

const object = {
	users: [
		{name: 'Alice', role: 'admin'},
		{name: 'Bob', role: 'user'}
	]
};

// Using array paths - no parsing overhead
getProperty(object, ['users', 0, 'name']);
//=> 'Alice'

setProperty(object, ['users', 1, 'role'], 'moderator');
console.log(object.users[1].role);
//=> 'moderator'

// Useful for interoperability with libraries that return paths as arrays
const pathFromOtherLib = ['users', 0, 'profile', 'settings'];
setProperty(object, pathFromOtherLib, {theme: 'dark'});
```

Array paths:
- Avoid the parse/stringify cycle when you already have path segments
- Work with all functions: `getProperty`, `setProperty`, `hasProperty`, `deleteProperty`
- Numeric strings are automatically normalized to numbers for simplicity

## API

### getProperty(object, path, defaultValue?)

Get the value of the property at the given path.

Returns the value if any.

### setProperty(object, path, value)

Set the property at the given path to the given value.

Returns the object.

### hasProperty(object, path)

Check whether the property at the given path exists.

Returns a boolean.

### deleteProperty(object, path)

Delete the property at the given path.

Returns a boolean of whether the property existed before being deleted.

### escapePath(path)

Escape special characters in a path. Useful for sanitizing user input.

```js
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

### parsePath(path)

Parse a dot path into an array of path segments.

Returns an array of path segments where numbers represent array indices and strings represent object keys.

```js
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

### stringifyPath(pathSegments, options?)

Convert an array of path segments back into a path string.

Returns a string path that can be used with other dot-prop functions.

```js
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

#### pathSegments

Type: `Array<string | number>`

Array of path segments where numbers represent array indices and strings represent object keys.

#### options

Type: `object`

##### preferDotForIndices

Type: `boolean`\
Default: `false`

When `true`, numeric indices will use dot notation instead of bracket notation when not the first segment.

### deepKeys(object)

Returns an array of every path. Non-empty plain objects and arrays are deeply recursed and are not themselves included.

This can be useful to help flatten an object for an API that only accepts key-value pairs or for a tagged template literal.

```js
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

Sparse arrays are supported. In general, [avoid using sparse arrays](https://github.com/sindresorhus/dot-prop/issues/109#issuecomment-1614819869).

#### object

Type: `object | array`

Object or array to get, set, or delete the `path` value.

You are allowed to pass in `undefined` as the object to the `get` and `has` functions.

#### path

Type: `string | Array<string | number>`

Path of the property in the object.

**String paths**: Use `.` to separate each nested key. Use `\\.` if you have a `.` in the key. Array indices can be accessed using bracket notation (like `'users[0].name'`) or dot notation (like `'users.0.name'`). Both syntaxes are equivalent and will create arrays when setting values. Numeric strings in dot notation (like `'users.0.name'`) are automatically coerced to numbers.

**Array paths**: Pass an array of path segments for better performance and interoperability. Numbers create arrays (like `['users', 0, 'name']`). Numeric strings are normalized to numbers for simplicity. No parsing overhead.

The following path components are invalid and results in `undefined` being returned: `__proto__`, `prototype`, `constructor`.

#### value

Type: `unknown`

Value to set at `path`.

#### defaultValue

Type: `unknown`

Default value.

### unflatten(object)

Convert an object with dot paths into a nested object.

Uses the same path rules and escaping as the rest of the API.

```js
import {unflatten} from 'dot-prop';

const flat = {
	'unicorn.name': 'Rainbow Dash',
	'unicorn.color': '🦄',
	'unicorn.treasures[0]': 'sparkles',
	'unicorn.treasures[1]': 'glitter',
};

unflatten(flat);
/*
{
	unicorn: {
		name: 'Rainbow Dash',
		color: '🦄',
		treasures: ['sparkles', 'glitter']
	}
}
*/
```
