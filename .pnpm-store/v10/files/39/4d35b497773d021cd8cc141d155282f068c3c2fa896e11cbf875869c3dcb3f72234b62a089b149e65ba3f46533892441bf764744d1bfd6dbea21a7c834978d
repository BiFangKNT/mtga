"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.getDissectedClasses = getDissectedClasses;
const utils = __importStar(require("tailwindcss/lib/util/splitAtTopLevelOnly.js"));
const escape_js_1 = require("../async-utils/escape.js");
const prefix_async_v3_js_1 = require("./prefix.async.v3.js");
function getDissectedClasses(context, classes) {
    const prefix = (0, prefix_async_v3_js_1.getPrefix)(context);
    const separator = context.tailwindConfig.separator ?? ":";
    return classes.map(className => {
        const splitChunks = utils.splitAtTopLevelOnly?.(className, separator) ?? utils.default?.splitAtTopLevelOnly?.(className, separator);
        const variants = splitChunks.slice(0, -1);
        let base = className
            .replace(new RegExp(`^${(0, escape_js_1.escapeForRegex)(variants.join(separator) + separator)}`), "")
            .replace(new RegExp(`^${(0, escape_js_1.escapeForRegex)(prefix)}`), "");
        const isNegative = base.startsWith("-");
        base = base.replace(/^-/, "");
        const isImportantAtStart = base.startsWith("!");
        base = base.replace(/^!/, "");
        const isImportantAtEnd = base.endsWith("!");
        base = base.replace(/!$/, "");
        return {
            base,
            className,
            important: [isImportantAtStart, isImportantAtEnd],
            negative: isNegative,
            prefix,
            separator,
            variants
        };
    });
}
//# sourceMappingURL=dissect-classes.async.v3.js.map