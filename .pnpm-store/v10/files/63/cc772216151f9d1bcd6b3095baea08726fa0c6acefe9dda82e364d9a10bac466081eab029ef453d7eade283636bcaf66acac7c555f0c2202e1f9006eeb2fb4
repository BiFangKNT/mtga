"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const synckit_1 = require("synckit");
const context_js_1 = require("../async-utils/context.js");
const context_async_v3_js_1 = require("./context.async.v3.js");
const prefix_async_v3_js_1 = require("./prefix.async.v3.js");
(0, synckit_1.runAsWorker)(async ({ configPath, cwd, tsconfigPath }) => {
    const { ctx, warnings } = await (0, context_js_1.getAsyncContext)({ configPath, cwd, tsconfigPath });
    const context = await (0, context_async_v3_js_1.createTailwindContext)(ctx);
    const prefix = (0, prefix_async_v3_js_1.getPrefix)(context);
    const suffix = (0, prefix_async_v3_js_1.getSuffix)(context);
    return { prefix, suffix, warnings: [...warnings] };
});
//# sourceMappingURL=prefix.async.worker.v3.js.map