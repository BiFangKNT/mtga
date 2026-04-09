import { runAsWorker } from "synckit";
import { getAsyncContext } from "../async-utils/context.js";
import { createTailwindContext } from "./context.async.v4.js";
import { getUnregisteredClasses } from "./unregistered-classes.async.v4.js";
runAsWorker(async ({ classes, configPath, cwd, tsconfigPath }) => {
    const { ctx, warnings } = await getAsyncContext({ configPath, cwd, tsconfigPath });
    const tailwindContext = await createTailwindContext(ctx);
    const unregisteredClasses = getUnregisteredClasses(tailwindContext, classes);
    return { unregisteredClasses, warnings: [...warnings] };
});
//# sourceMappingURL=unregistered-classes.async.worker.v4.js.map