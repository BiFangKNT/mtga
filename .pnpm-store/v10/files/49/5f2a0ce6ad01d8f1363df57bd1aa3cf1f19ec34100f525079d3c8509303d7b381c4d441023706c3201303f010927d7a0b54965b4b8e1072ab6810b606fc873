import defaultConfig from "tailwindcss/defaultConfig.js";
import * as setupContextUtils from "tailwindcss/lib/lib/setupContextUtils.js";
import loadConfig from "tailwindcss/loadConfig.js";
import resolveConfig from "tailwindcss/resolveConfig.js";
import { withCache } from "../async-utils/cache.js";
export const createTailwindContext = async (ctx) => withCache("tailwind-context", ctx.tailwindConfigPath, async () => {
    const tailwindConfig = loadTailwindConfig(ctx.tailwindConfigPath);
    return setupContextUtils.createContext?.(tailwindConfig) ?? setupContextUtils.default?.createContext?.(tailwindConfig);
});
function loadTailwindConfig(path) {
    const config = path === "default"
        ? defaultConfig
        : loadConfig(path);
    return resolveConfig(config);
}
//# sourceMappingURL=context.async.v3.js.map