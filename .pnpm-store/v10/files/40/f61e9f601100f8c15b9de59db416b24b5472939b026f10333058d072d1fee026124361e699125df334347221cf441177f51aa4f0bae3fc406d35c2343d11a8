"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.invalidateByModifiedDate = invalidateByModifiedDate;
exports.withCache = withCache;
const node_process_1 = require("node:process");
const fs_js_1 = require("./fs.js");
const CACHE = new Map();
function invalidateByModifiedDate(cache, path) {
    if (!path) {
        return true;
    }
    const modified = (0, fs_js_1.getModifiedDate)(path);
    return modified > cache.date;
}
function withCache(key, path, callback, invalidate = invalidateByModifiedDate) {
    const cacheKey = `${key}-${path}`;
    const cached = CACHE.get(cacheKey);
    if (node_process_1.env.NODE_ENV !== "test" && cached && !invalidate(cached, path)) {
        return cached.value;
    }
    const value = callback();
    if (value instanceof Promise) {
        return value.then(resolvedValue => {
            CACHE.set(cacheKey, { date: new Date(), value: resolvedValue });
            return resolvedValue;
        });
    }
    else {
        CACHE.set(cacheKey, { date: new Date(), value });
        return value;
    }
}
//# sourceMappingURL=cache.js.map