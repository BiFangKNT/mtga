//#region node_modules/.pnpm/es-toolkit@1.44.0/node_modules/es-toolkit/dist/predicate/isPrimitive.mjs
function isPrimitive(value) {
	return value == null || typeof value !== "object" && typeof value !== "function";
}

//#endregion
//#region node_modules/.pnpm/es-toolkit@1.44.0/node_modules/es-toolkit/dist/predicate/isTypedArray.mjs
function isTypedArray(x) {
	return ArrayBuffer.isView(x) && !(x instanceof DataView);
}

//#endregion
//#region node_modules/.pnpm/es-toolkit@1.44.0/node_modules/es-toolkit/dist/object/clone.mjs
function clone(obj) {
	if (isPrimitive(obj)) return obj;
	if (Array.isArray(obj) || isTypedArray(obj) || obj instanceof ArrayBuffer || typeof SharedArrayBuffer !== "undefined" && obj instanceof SharedArrayBuffer) return obj.slice(0);
	const prototype = Object.getPrototypeOf(obj);
	if (prototype == null) return Object.assign(Object.create(prototype), obj);
	const Constructor = prototype.constructor;
	if (obj instanceof Date || obj instanceof Map || obj instanceof Set) return new Constructor(obj);
	if (obj instanceof RegExp) {
		const newRegExp = new Constructor(obj);
		newRegExp.lastIndex = obj.lastIndex;
		return newRegExp;
	}
	if (obj instanceof DataView) return new Constructor(obj.buffer.slice(0));
	if (obj instanceof Error) {
		let newError;
		if (obj instanceof AggregateError) newError = new Constructor(obj.errors, obj.message, { cause: obj.cause });
		else newError = new Constructor(obj.message, { cause: obj.cause });
		newError.stack = obj.stack;
		Object.assign(newError, obj);
		return newError;
	}
	if (typeof File !== "undefined" && obj instanceof File) return new Constructor([obj], obj.name, {
		type: obj.type,
		lastModified: obj.lastModified
	});
	if (typeof obj === "object") {
		const newObject = Object.create(prototype);
		return Object.assign(newObject, obj);
	}
	return obj;
}

//#endregion
//#region node_modules/.pnpm/es-toolkit@1.44.0/node_modules/es-toolkit/dist/predicate/isPlainObject.mjs
function isPlainObject(value) {
	if (!value || typeof value !== "object") return false;
	const proto = Object.getPrototypeOf(value);
	if (!(proto === null || proto === Object.prototype || Object.getPrototypeOf(proto) === null)) return false;
	return Object.prototype.toString.call(value) === "[object Object]";
}

//#endregion
//#region node_modules/.pnpm/es-toolkit@1.44.0/node_modules/es-toolkit/dist/_internal/isUnsafeProperty.mjs
function isUnsafeProperty(key) {
	return key === "__proto__";
}

//#endregion
//#region node_modules/.pnpm/es-toolkit@1.44.0/node_modules/es-toolkit/dist/object/mergeWith.mjs
function mergeWith(target, source, merge) {
	const sourceKeys = Object.keys(source);
	for (let i = 0; i < sourceKeys.length; i++) {
		const key = sourceKeys[i];
		if (isUnsafeProperty(key)) continue;
		const sourceValue = source[key];
		const targetValue = target[key];
		const merged = merge(targetValue, sourceValue, key, target, source);
		if (merged !== void 0) target[key] = merged;
		else if (Array.isArray(sourceValue)) if (Array.isArray(targetValue)) target[key] = mergeWith(targetValue, sourceValue, merge);
		else target[key] = mergeWith([], sourceValue, merge);
		else if (isPlainObject(sourceValue)) if (isPlainObject(targetValue)) target[key] = mergeWith(targetValue, sourceValue, merge);
		else target[key] = mergeWith({}, sourceValue, merge);
		else if (targetValue === void 0 || sourceValue !== void 0) target[key] = sourceValue;
	}
	return target;
}

//#endregion
//#region node_modules/.pnpm/es-toolkit@1.44.0/node_modules/es-toolkit/dist/object/toMerged.mjs
function toMerged(target, source) {
	return mergeWith(clone(target), source, function mergeRecursively(targetValue, sourceValue) {
		if (Array.isArray(sourceValue)) if (Array.isArray(targetValue)) return mergeWith(clone(targetValue), sourceValue, mergeRecursively);
		else return mergeWith([], sourceValue, mergeRecursively);
		else if (isPlainObject(sourceValue)) if (isPlainObject(targetValue)) return mergeWith(clone(targetValue), sourceValue, mergeRecursively);
		else return mergeWith({}, sourceValue, mergeRecursively);
	});
}

//#endregion
export { isPlainObject as n, toMerged as t };