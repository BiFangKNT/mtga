import { runAsWorker } from "synckit";
import { getAsyncContext } from "../async-utils/context.js";
import { createTailwindContext } from "./context.async.v3.js";
import { getUnregisteredClasses } from "./unregistered-classes.async.v3.js";
runAsWorker(async ({ classes, configPath, cwd, tsconfigPath }) => {
    const { ctx, warnings } = await getAsyncContext({ configPath, cwd, tsconfigPath });
    const context = await createTailwindContext(ctx);
    const unregisteredClasses = getUnregisteredClasses(context, classes);
    return { unregisteredClasses, warnings: [...warnings] };
});
//# sourceMappingURL=unregistered-classes.async.worker.v3.js.map