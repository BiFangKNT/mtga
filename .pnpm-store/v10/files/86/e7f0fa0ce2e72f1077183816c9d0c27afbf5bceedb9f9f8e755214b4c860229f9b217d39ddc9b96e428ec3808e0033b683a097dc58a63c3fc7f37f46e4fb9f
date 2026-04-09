"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const synckit_1 = require("synckit");
const context_js_1 = require("../async-utils/context.js");
const context_async_v4_js_1 = require("./context.async.v4.js");
const unregistered_classes_async_v4_js_1 = require("./unregistered-classes.async.v4.js");
(0, synckit_1.runAsWorker)(async ({ classes, configPath, cwd, tsconfigPath }) => {
    const { ctx, warnings } = await (0, context_js_1.getAsyncContext)({ configPath, cwd, tsconfigPath });
    const tailwindContext = await (0, context_async_v4_js_1.createTailwindContext)(ctx);
    const unregisteredClasses = (0, unregistered_classes_async_v4_js_1.getUnregisteredClasses)(tailwindContext, classes);
    return { unregisteredClasses, warnings: [...warnings] };
});
//# sourceMappingURL=unregistered-classes.async.worker.v4.js.map