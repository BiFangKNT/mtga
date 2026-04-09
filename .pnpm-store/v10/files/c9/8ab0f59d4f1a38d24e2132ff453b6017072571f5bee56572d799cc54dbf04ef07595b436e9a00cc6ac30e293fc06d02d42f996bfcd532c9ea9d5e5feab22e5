import { runAsWorker } from "synckit";
import { getAsyncContext } from "../async-utils/context.js";
import { getConflictingClasses } from "./conflicting-classes.async.v4.js";
import { createTailwindContext } from "./context.async.v4.js";
runAsWorker(async ({ classes, configPath, cwd, tsconfigPath }) => {
    const { ctx, warnings } = await getAsyncContext({ configPath, cwd, tsconfigPath });
    const context = await createTailwindContext(ctx);
    const conflictingClasses = await getConflictingClasses(context, classes);
    return { conflictingClasses, warnings: [...warnings] };
});
//# sourceMappingURL=conflicting-classes.async.worker.v4.js.map