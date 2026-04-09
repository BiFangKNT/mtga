"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.createTailwindContext = void 0;
const promises_1 = require("node:fs/promises");
const node_path_1 = require("node:path");
const node_url_1 = require("node:url");
const jiti_1 = require("jiti");
const postcss_1 = __importDefault(require("postcss"));
const postcss_import_1 = __importDefault(require("postcss-import"));
const cache_js_1 = require("../async-utils/cache.js");
const module_js_1 = require("../async-utils/module.js");
const platform_js_1 = require("../async-utils/platform.js");
const resolvers_js_1 = require("../async-utils/resolvers.js");
const createTailwindContext = async (ctx) => (0, cache_js_1.withCache)("tailwind-context", ctx.tailwindConfigPath, async () => {
    const jiti = (0, jiti_1.createJiti)(getCurrentFilename(), {
        fsCache: false,
        moduleCache: false
    });
    const importBasePath = (0, node_path_1.dirname)(ctx.tailwindConfigPath);
    const tailwindPath = (0, resolvers_js_1.resolveJs)(ctx, "tailwindcss", importBasePath);
    if (!tailwindPath) {
        throw new Error("Could not find Tailwind CSS");
    }
    const tailwindUrl = (0, platform_js_1.isWindows)() && (0, module_js_1.isESModule)() ? (0, node_url_1.pathToFileURL)(tailwindPath).toString() : tailwindPath;
    // eslint-disable-next-line eslint-plugin-typescript/naming-convention
    const { __unstable__loadDesignSystem } = await Promise.resolve(`${tailwindUrl}`).then(s => __importStar(require(s)));
    let css = await (0, promises_1.readFile)(ctx.tailwindConfigPath, "utf-8");
    // Determine if the v4 API supports resolving `@import`
    let supportsImports = false;
    try {
        await __unstable__loadDesignSystem('@import "./empty";', {
            loadStylesheet: async () => {
                supportsImports = true;
                return {
                    base: importBasePath,
                    content: ""
                };
            }
        });
    }
    catch { }
    if (!supportsImports) {
        const resolveImports = (0, postcss_1.default)([(0, postcss_import_1.default)()]);
        const result = await resolveImports.process(css, { from: ctx.tailwindConfigPath });
        css = result.css;
    }
    // Load the design system and set up a compatible context object that is
    // usable by the rest of the plugin
    const design = await __unstable__loadDesignSystem(css, {
        base: importBasePath,
        loadModule: createLoader(ctx, jiti, {
            filepath: ctx.tailwindConfigPath,
            legacy: false,
            onError: (id, err, resourceType) => {
                console.error(`Unable to load ${resourceType}: ${id}`, err);
                if (resourceType === "config") {
                    return {};
                }
                else if (resourceType === "plugin") {
                    return () => { };
                }
            }
        }),
        loadStylesheet: async (id, base) => {
            try {
                const resolved = (0, resolvers_js_1.resolveCss)(ctx, id, base);
                return {
                    base: (0, node_path_1.dirname)(resolved),
                    content: await (0, promises_1.readFile)(resolved, "utf-8")
                };
            }
            catch {
                return {
                    base: "",
                    content: ""
                };
            }
        }
    });
    return design;
});
exports.createTailwindContext = createTailwindContext;
function createLoader(ctx, jiti, { filepath, legacy, onError }) {
    const cacheKey = `${+Date.now()}`;
    async function loadFile(id, base, resourceType) {
        try {
            const resolved = (0, resolvers_js_1.resolveJs)(ctx, id, base);
            const url = (0, node_url_1.pathToFileURL)(resolved);
            url.searchParams.append("t", cacheKey);
            return await jiti.import(url.href, { default: true });
        }
        catch (err) {
            return onError(id, err, resourceType);
        }
    }
    if (legacy) {
        const baseDir = (0, node_path_1.dirname)(filepath);
        return async (id) => loadFile(id, baseDir, "module");
    }
    return async (id, base, resourceType) => {
        return {
            base,
            module: await loadFile(id, base, resourceType)
        };
    };
}
function getCurrentFilename() {
    // eslint-disable-next-line eslint-plugin-typescript/prefer-ts-expect-error
    // @ts-ignore - `import.meta` doesn't exist in CommonJS -> will be transformed in build step
    return __filename;
}
//# sourceMappingURL=context.async.v4.js.map