import { runAsWorker } from "synckit";
import { getAsyncContext } from "../async-utils/context.js";
import { createTailwindContext } from "./context.async.v3.js";
import { getPrefix, getSuffix } from "./prefix.async.v3.js";
runAsWorker(async ({ configPath, cwd, tsconfigPath }) => {
    const { ctx, warnings } = await getAsyncContext({ configPath, cwd, tsconfigPath });
    const context = await createTailwindContext(ctx);
    const prefix = getPrefix(context);
    const suffix = getSuffix(context);
    return { prefix, suffix, warnings: [...warnings] };
});
//# sourceMappingURL=prefix.async.worker.v3.js.map