"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createTailwindContext = createTailwindContext;
const tailwindcss_js_1 = require("../async-utils/tailwindcss.js");
const context_async_v3_js_1 = require("./context.async.v3.js");
const context_async_v4_js_1 = require("./context.async.v4.js");
async function createTailwindContext(ctx) {
    const version = (0, tailwindcss_js_1.getTailwindcssVersion)();
    if (version.major === 3 /* TailwindcssVersion.V3 */) {
        return (0, context_async_v3_js_1.createTailwindContext)(ctx);
    }
    else {
        return (0, context_async_v4_js_1.createTailwindContext)(ctx);
    }
}
//# sourceMappingURL=context.async.js.map