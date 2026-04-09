const isObject = value => {
	const type = typeof value;
	return value !== null && (type === 'object' || type === 'function');
};

// Optimized empty check without creating an array.
const isEmptyObject = value => {
	if (!isObject(value)) {
		return false;
	}

	for (const key in value) {
		if (Object.hasOwn(value, key)) {
			return false;
		}
	}

	return true;
};

const disallowedKeys = new Set([
	'__proto__',
	'prototype',
	'constructor',
]);

// Maximum allowed array index to prevent DoS via memory exhaustion.
const MAX_ARRAY_INDEX = 1_000_000;

// Optimized digit check without Set overhead.
const isDigit = character => character >= '0' && character <= '9';

// Check if a segment should be coerced to a number.
function shouldCoerceToNumber(segment) {
	// Only coerce valid non-negative integers without leading zeros.
	if (segment === '0') {
		return true;
	}

	if (/^[1-9]\d*$/.test(segment)) {
		const parsedNumber = Number.parseInt(segment, 10);
		// Check within safe integer range and under MAX_ARRAY_INDEX to prevent DoS.
		return parsedNumber <= Number.MAX_SAFE_INTEGER && parsedNumber <= MAX_ARRAY_INDEX;
	}

	return false;
}

// Helper to process a path segment (eliminates duplication).
function processSegment(segment, parts) {
	if (disallowedKeys.has(segment)) {
		return false; // Signal to return empty array.
	}

	if (segment && shouldCoerceToNumber(segment)) {
		parts.push(Number.parseInt(segment, 10));
	} else {
		parts.push(segment);
	}

	return true;
}

export function parsePath(path) { // eslint-disable-line complexity
	if (typeof path !== 'string') {
		throw new TypeError(`Expected a string, got ${typeof path}`);
	}

	const parts = [];
	let currentSegment = '';
	let currentPart = 'start';
	let isEscaping = false;
	let position = 0;

	for (const character of path) {
		position++;

		// Handle escaping.
		if (isEscaping) {
			currentSegment += character;
			isEscaping = false;
			continue;
		}

		// Handle escape character.
		if (character === '\\') {
			if (currentPart === 'index') {
				throw new Error(`Invalid character '${character}' in an index at position ${position}`);
			}

			if (currentPart === 'indexEnd') {
				throw new Error(`Invalid character '${character}' after an index at position ${position}`);
			}

			isEscaping = true;
			currentPart = currentPart === 'start' ? 'property' : currentPart;
			continue;
		}

		switch (character) {
			case '.': {
				if (currentPart === 'index') {
					throw new Error(`Invalid character '${character}' in an index at position ${position}`);
				}

				if (currentPart === 'indexEnd') {
					currentPart = 'property';
					break;
				}

				if (!processSegment(currentSegment, parts)) {
					return [];
				}

				currentSegment = '';
				currentPart = 'property';
				break;
			}

			case '[': {
				if (currentPart === 'index') {
					throw new Error(`Invalid character '${character}' in an index at position ${position}`);
				}

				if (currentPart === 'indexEnd') {
					currentPart = 'index';
					break;
				}

				if (currentPart === 'property' || currentPart === 'start') {
					// Only push if we have content OR if we're in 'property' mode (not 'start')
					if ((currentSegment || currentPart === 'property') && !processSegment(currentSegment, parts)) {
						return [];
					}

					currentSegment = '';
				}

				currentPart = 'index';
				break;
			}

			case ']': {
				if (currentPart === 'index') {
					if (currentSegment === '') {
						// Empty brackets - backtrack and treat as literal
						const lastSegment = parts.pop() || '';
						currentSegment = lastSegment + '[]';
						currentPart = 'property';
					} else {
						// Index must be digits only (enforced by default case)
						const parsedNumber = Number.parseInt(currentSegment, 10);
						const isValidInteger = !Number.isNaN(parsedNumber)
							&& Number.isFinite(parsedNumber)
							&& parsedNumber >= 0
							&& parsedNumber <= Number.MAX_SAFE_INTEGER
							&& parsedNumber <= MAX_ARRAY_INDEX
							&& currentSegment === String(parsedNumber);

						if (isValidInteger) {
							parts.push(parsedNumber);
						} else {
							// Keep as string if not a valid integer representation or exceeds MAX_ARRAY_INDEX
							parts.push(currentSegment);
						}

						currentSegment = '';
						currentPart = 'indexEnd';
					}

					break;
				}

				if (currentPart === 'indexEnd') {
					throw new Error(`Invalid character '${character}' after an index at position ${position}`);
				}

				// In property context, treat ] as literal character
				currentSegment += character;
				break;
			}

			default: {
				if (currentPart === 'index' && !isDigit(character)) {
					throw new Error(`Invalid character '${character}' in an index at position ${position}`);
				}

				if (currentPart === 'indexEnd') {
					throw new Error(`Invalid character '${character}' after an index at position ${position}`);
				}

				if (currentPart === 'start') {
					currentPart = 'property';
				}

				currentSegment += character;
			}
		}
	}

	// Handle unfinished escaping (trailing backslash)
	if (isEscaping) {
		currentSegment += '\\';
	}

	// Handle end of path
	switch (currentPart) {
		case 'property': {
			if (!processSegment(currentSegment, parts)) {
				return [];
			}

			break;
		}

		case 'index': {
			throw new Error('Index was not closed');
		}

		case 'start': {
			parts.push('');
			break;
		}
		// No default
	}

	return parts;
}

function normalizePath(path) {
	if (typeof path === 'string') {
		return parsePath(path);
	}

	if (Array.isArray(path)) {
		const normalized = [];

		for (const [index, segment] of path.entries()) {
			// Type validation.
			if (typeof segment !== 'string' && typeof segment !== 'number') {
				throw new TypeError(`Expected a string or number for path segment at index ${index}, got ${typeof segment}`);
			}

			// Validate numbers are finite (reject NaN, Infinity, -Infinity).
			if (typeof segment === 'number' && !Number.isFinite(segment)) {
				throw new TypeError(`Path segment at index ${index} must be a finite number, got ${segment}`);
			}

			// Check for disallowed keys.
			if (disallowedKeys.has(segment)) {
				return [];
			}

			// Normalize numeric strings to numbers for simplicity.
			// This treats ['items', '0'] the same as ['items', 0].
			if (typeof segment === 'string' && shouldCoerceToNumber(segment)) {
				normalized.push(Number.parseInt(segment, 10));
			} else {
				normalized.push(segment);
			}
		}

		return normalized;
	}

	return [];
}

export function getProperty(object, path, value) {
	if (!isObject(object) || (typeof path !== 'string' && !Array.isArray(path))) {
		return value === undefined ? object : value;
	}

	const pathArray = normalizePath(path);
	if (pathArray.length === 0) {
		return value;
	}

	for (let index = 0; index < pathArray.length; index++) {
		const key = pathArray[index];
		object = object[key];

		if (object === undefined || object === null) {
			// Return default value if we hit undefined/null before the end of the path.
			// This ensures get({foo: null}, 'foo.bar') returns the default value, not null.
			if (index !== pathArray.length - 1) {
				return value;
			}

			break;
		}
	}

	return object === undefined ? value : object;
}

export function setProperty(object, path, value) {
	if (!isObject(object) || (typeof path !== 'string' && !Array.isArray(path))) {
		return object;
	}

	const root = object;
	const pathArray = normalizePath(path);

	if (pathArray.length === 0) {
		return object;
	}

	for (let index = 0; index < pathArray.length; index++) {
		const key = pathArray[index];

		if (index === pathArray.length - 1) {
			object[key] = value;
		} else if (!isObject(object[key])) {
			const nextKey = pathArray[index + 1];
			// Create arrays for numeric indices, objects for string keys
			const shouldCreateArray = typeof nextKey === 'number';
			object[key] = shouldCreateArray ? [] : {};
		}

		object = object[key];
	}

	return root;
}

export function deleteProperty(object, path) {
	if (!isObject(object) || (typeof path !== 'string' && !Array.isArray(path))) {
		return false;
	}

	const pathArray = normalizePath(path);

	if (pathArray.length === 0) {
		return false;
	}

	for (let index = 0; index < pathArray.length; index++) {
		const key = pathArray[index];

		if (index === pathArray.length - 1) {
			const existed = Object.hasOwn(object, key);
			if (!existed) {
				return false;
			}

			delete object[key];
			return true;
		}

		object = object[key];

		if (!isObject(object)) {
			return false;
		}
	}
}

export function hasProperty(object, path) {
	if (!isObject(object) || (typeof path !== 'string' && !Array.isArray(path))) {
		return false;
	}

	const pathArray = normalizePath(path);
	if (pathArray.length === 0) {
		return false;
	}

	for (const key of pathArray) {
		if (!isObject(object) || !(key in object)) {
			return false;
		}

		object = object[key];
	}

	return true;
}

export function escapePath(path) {
	if (typeof path !== 'string') {
		throw new TypeError(`Expected a string, got ${typeof path}`);
	}

	// Escape special characters in one pass
	return path.replaceAll(/[\\.[]/g, String.raw`\$&`);
}

function normalizeEntries(value) {
	const entries = Object.entries(value);
	if (Array.isArray(value)) {
		return entries.map(([key, entryValue]) => {
			// Use shouldCoerceToNumber for consistency with parsePath
			const normalizedKey = shouldCoerceToNumber(key)
				? Number.parseInt(key, 10)
				: key;
			return [normalizedKey, entryValue];
		});
	}

	return entries;
}

export function stringifyPath(pathSegments, options = {}) {
	if (!Array.isArray(pathSegments)) {
		throw new TypeError(`Expected an array, got ${typeof pathSegments}`);
	}

	const {preferDotForIndices = false} = options;
	const parts = [];

	for (const [index, segment] of pathSegments.entries()) {
		// Validate segment types at runtime
		if (typeof segment !== 'string' && typeof segment !== 'number') {
			throw new TypeError(`Expected a string or number for path segment at index ${index}, got ${typeof segment}`);
		}

		if (typeof segment === 'number') {
			// Handle numeric indices
			if (!Number.isInteger(segment) || segment < 0) {
				// Non-integer or negative numbers are treated as string keys
				const escaped = escapePath(String(segment));
				parts.push(index === 0 ? escaped : `.${escaped}`);
			} else if (preferDotForIndices && index > 0) {
				parts.push(`.${segment}`);
			} else {
				parts.push(`[${segment}]`);
			}
		} else if (typeof segment === 'string') {
			if (segment === '') {
				// Empty string handling
				if (index === 0) {
					// Start with empty string, no prefix needed
				} else {
					parts.push('.');
				}
			} else if (shouldCoerceToNumber(segment)) {
				// Numeric strings are normalized to numbers
				const numericValue = Number.parseInt(segment, 10);
				if (preferDotForIndices && index > 0) {
					parts.push(`.${numericValue}`);
				} else {
					parts.push(`[${numericValue}]`);
				}
			} else {
				// Regular strings use dot notation
				const escaped = escapePath(segment);
				parts.push(index === 0 ? escaped : `.${escaped}`);
			}
		}
	}

	return parts.join('');
}

function * deepKeysIterator(object, currentPath = [], ancestors = new Set()) {
	if (!isObject(object) || isEmptyObject(object)) {
		if (currentPath.length > 0) {
			yield stringifyPath(currentPath);
		}

		return;
	}

	// Check if this object is already in the current path (circular reference)
	if (ancestors.has(object)) {
		return;
	}

	// Add to ancestors, recurse, then remove (backtrack)
	ancestors.add(object);

	// Reuse currentPath array by push/pop instead of creating new arrays
	for (const [key, value] of normalizeEntries(object)) {
		currentPath.push(key);
		yield * deepKeysIterator(value, currentPath, ancestors);
		currentPath.pop();
	}

	ancestors.delete(object);
}

export function deepKeys(object) {
	return [...deepKeysIterator(object)];
}

export function unflatten(object) {
	const result = {};
	if (!isObject(object)) {
		return result;
	}

	for (const [path, value] of Object.entries(object)) {
		setProperty(result, path, value);
	}

	return result;
}
