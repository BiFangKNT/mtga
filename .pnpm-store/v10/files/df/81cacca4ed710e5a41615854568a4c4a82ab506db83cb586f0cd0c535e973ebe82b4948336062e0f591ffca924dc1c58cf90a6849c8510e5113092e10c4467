import { getTailwindConfigPath } from "./config.js";
import { getTailwindcssVersion } from "./tailwindcss.js";
import { getTSConfigPath } from "./tsconfig.js";
export async function getAsyncContext({ configPath, cwd, tsconfigPath }) {
    const version = getTailwindcssVersion();
    const { path: resolvedTailwindPath, warnings: tailwindConfigWarnings } = getTailwindConfigPath({ configPath, cwd, version });
    const { path: resolvedTSConfigPath, warnings: tsconfigWarnings } = getTSConfigPath({ configPath: tsconfigPath, cwd });
    return {
        ctx: {
            cwd,
            tailwindConfigPath: resolvedTailwindPath,
            tsconfigPath: resolvedTSConfigPath,
            version
        },
        warnings: [...tailwindConfigWarnings, ...tsconfigWarnings]
    };
}
//# sourceMappingURL=context.js.map