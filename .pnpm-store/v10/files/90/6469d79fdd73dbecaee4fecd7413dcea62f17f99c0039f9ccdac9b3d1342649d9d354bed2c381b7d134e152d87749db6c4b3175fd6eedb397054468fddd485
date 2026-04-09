"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const synckit_1 = require("synckit");
const context_js_1 = require("../async-utils/context.js");
const conflicting_classes_async_v4_js_1 = require("./conflicting-classes.async.v4.js");
const context_async_v4_js_1 = require("./context.async.v4.js");
(0, synckit_1.runAsWorker)(async ({ classes, configPath, cwd, tsconfigPath }) => {
    const { ctx, warnings } = await (0, context_js_1.getAsyncContext)({ configPath, cwd, tsconfigPath });
    const context = await (0, context_async_v4_js_1.createTailwindContext)(ctx);
    const conflictingClasses = await (0, conflicting_classes_async_v4_js_1.getConflictingClasses)(context, classes);
    return { conflictingClasses, warnings: [...warnings] };
});
//# sourceMappingURL=conflicting-classes.async.worker.v4.js.map