import { runAsWorker } from "synckit";
import { getAsyncContext } from "../async-utils/context.js";
import { createTailwindContext } from "./context.async.v3.js";
import { getDissectedClasses } from "./dissect-classes.async.v3.js";
runAsWorker(async ({ classes, configPath, cwd, tsconfigPath }) => {
    const { ctx, warnings } = await getAsyncContext({ configPath, cwd, tsconfigPath });
    const context = await createTailwindContext(ctx);
    const dissectedClasses = getDissectedClasses(context, classes);
    return { dissectedClasses, warnings: [...warnings] };
});
//# sourceMappingURL=dissect-classes.async.worker.v3.js.map