import { runAsWorker } from "synckit";
import { getAsyncContext } from "../async-utils/context.js";
import { getClassOrder } from "./class-order.async.v4.js";
import { createTailwindContext } from "./context.async.v4.js";
runAsWorker(async ({ classes, configPath, cwd, tsconfigPath }) => {
    const { ctx, warnings } = await getAsyncContext({ configPath, cwd, tsconfigPath });
    const context = await createTailwindContext(ctx);
    const classOrder = getClassOrder(context, classes);
    return { classOrder, warnings: [...warnings] };
});
//# sourceMappingURL=class-order.async.worker.v4.js.map