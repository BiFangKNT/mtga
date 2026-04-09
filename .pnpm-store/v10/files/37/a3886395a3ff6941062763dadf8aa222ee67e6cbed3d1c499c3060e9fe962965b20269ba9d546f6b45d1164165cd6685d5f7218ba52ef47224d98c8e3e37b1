import { runAsWorker } from "synckit";
import { getAsyncContext } from "../async-utils/context.js";
runAsWorker(async ({ configPath, cwd, tsconfigPath }) => {
    const { ctx, warnings } = await getAsyncContext({ configPath, cwd, tsconfigPath });
    const { getCustomComponentClasses } = await import(`./custom-component-classes.async.v${ctx.version.major}.js`);
    const customComponentClasses = await getCustomComponentClasses(ctx);
    return { customComponentClasses, warnings: [...warnings] };
});
//# sourceMappingURL=custom-component-classes.async.worker.js.map