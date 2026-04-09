"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getAsyncContext = getAsyncContext;
const config_js_1 = require("./config.js");
const tailwindcss_js_1 = require("./tailwindcss.js");
const tsconfig_js_1 = require("./tsconfig.js");
async function getAsyncContext({ configPath, cwd, tsconfigPath }) {
    const version = (0, tailwindcss_js_1.getTailwindcssVersion)();
    const { path: resolvedTailwindPath, warnings: tailwindConfigWarnings } = (0, config_js_1.getTailwindConfigPath)({ configPath, cwd, version });
    const { path: resolvedTSConfigPath, warnings: tsconfigWarnings } = (0, tsconfig_js_1.getTSConfigPath)({ configPath: tsconfigPath, cwd });
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