"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const synckit_1 = require("synckit");
const context_js_1 = require("../async-utils/context.js");
const context_async_v3_js_1 = require("./context.async.v3.js");
const dissect_classes_async_v3_js_1 = require("./dissect-classes.async.v3.js");
(0, synckit_1.runAsWorker)(async ({ classes, configPath, cwd, tsconfigPath }) => {
    const { ctx, warnings } = await (0, context_js_1.getAsyncContext)({ configPath, cwd, tsconfigPath });
    const context = await (0, context_async_v3_js_1.createTailwindContext)(ctx);
    const dissectedClasses = (0, dissect_classes_async_v3_js_1.getDissectedClasses)(context, classes);
    return { dissectedClasses, warnings: [...warnings] };
});
//# sourceMappingURL=dissect-classes.async.worker.v3.js.map