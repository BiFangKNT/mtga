import { promises as fs } from "node:fs";
import path from "node:path";
import opn from "open";
import { version } from "./version.js";
import { createGzipSizeGetter, createBrotliSizeGetter } from "./compress.js";
import { ModuleMapper, replaceHashPlaceholders } from "./module-mapper.js";
import { addLinks, buildTree, mergeTrees } from "./data.js";
import { getSourcemapModules } from "./sourcemap.js";
import { renderTemplate } from "./render-template.js";
import { createFilter } from "../shared/create-filter.js";
const WARN_SOURCEMAP_DISABLED = "rollup output configuration missing sourcemap = true. You should add output.sourcemap = true or disable sourcemap in this plugin";
const WARN_SOURCEMAP_MISSING = (id) => `${id} missing source map`;
const WARN_JSON_DEPRECATED = 'Option `json` deprecated, please use template: "raw-data"';
const ERR_FILENAME_EMIT = "When using emitFile option, filename must not be path but a filename";
const defaultSizeGetter = () => Promise.resolve(0);
const chooseDefaultFileName = (opts) => {
    if (opts.filename)
        return opts.filename;
    if (opts.json || opts.template === "raw-data")
        return "stats.json";
    if (opts.template === "list")
        return "stats.yml";
    if (opts.template === "markdown")
        return "stats.md";
    return "stats.html";
};
export const visualizer = (opts = {}) => {
    return {
        name: "visualizer",
        async generateBundle(outputOptions, outputBundle) {
            opts = typeof opts === "function" ? opts(outputOptions) : opts;
            if ("json" in opts) {
                this.warn(WARN_JSON_DEPRECATED);
                if (opts.json)
                    opts.template = "raw-data";
            }
            const filename = opts.filename ?? chooseDefaultFileName(opts);
            const title = opts.title ?? "Rollup Visualizer";
            const open = !!opts.open;
            const openOptions = opts.openOptions ?? {};
            const template = opts.template ?? "treemap";
            const projectRoot = opts.projectRoot ?? process.cwd();
            const filter = createFilter(opts.include, opts.exclude);
            const gzipSizeRequested = !!opts.gzipSize;
            const brotliSizeRequested = !!opts.brotliSize;
            const gzipSize = gzipSizeRequested && !opts.sourcemap;
            const brotliSize = brotliSizeRequested && !opts.sourcemap;
            const gzipSizeGetter = gzipSize
                ? createGzipSizeGetter(typeof opts.gzipSize === "object" ? opts.gzipSize : {})
                : defaultSizeGetter;
            const brotliSizeGetter = brotliSize
                ? createBrotliSizeGetter(typeof opts.brotliSize === "object" ? opts.brotliSize : {})
                : defaultSizeGetter;
            const getModuleLengths = async ({ id, renderedLength, code, }, useRenderedLength = false) => {
                const isCodeEmpty = code == null || code == "";
                const result = {
                    id,
                    gzipLength: isCodeEmpty ? 0 : await gzipSizeGetter(code),
                    brotliLength: isCodeEmpty ? 0 : await brotliSizeGetter(code),
                    renderedLength: useRenderedLength
                        ? renderedLength
                        : isCodeEmpty
                            ? 0
                            : Buffer.byteLength(code, "utf-8"),
                };
                return result;
            };
            if (opts.sourcemap && !outputOptions.sourcemap) {
                this.warn(WARN_SOURCEMAP_DISABLED);
            }
            const roots = [];
            const mapper = new ModuleMapper(projectRoot);
            // collect trees
            for (const [bundleId, bundle] of Object.entries(outputBundle)) {
                if (bundle.type !== "chunk")
                    continue; //only chunks
                let tree;
                if (opts.sourcemap) {
                    if (!bundle.map) {
                        this.warn(WARN_SOURCEMAP_MISSING(bundleId));
                    }
                    const modules = await getSourcemapModules(bundleId, bundle, outputOptions.dir ??
                        (outputOptions.file && path.dirname(outputOptions.file)) ??
                        process.cwd());
                    const moduleRenderInfo = await Promise.all(Object.values(modules)
                        .filter(({ id }) => filter(bundleId, id))
                        .map(({ id, renderedLength, code }) => {
                        return getModuleLengths({ id, renderedLength, code: code.join("") }, true);
                    }));
                    tree = buildTree(bundleId, moduleRenderInfo, mapper);
                }
                else {
                    const modules = await Promise.all(Object.entries(bundle.modules)
                        .filter(([id]) => filter(bundleId, id))
                        .map(([id, { renderedLength, code }]) => getModuleLengths({ id, renderedLength, code }), false));
                    tree = buildTree(bundleId, modules, mapper);
                }
                if (tree.children.length === 0) {
                    const bundleSizes = await getModuleLengths({
                        id: bundleId,
                        renderedLength: bundle.code.length,
                        code: bundle.code,
                    }, false);
                    const facadeModuleId = bundle.facadeModuleId ?? `${bundleId}-unknown`;
                    const bundleUid = mapper.setNodePart(bundleId, facadeModuleId, bundleSizes);
                    mapper.setNodeMeta(facadeModuleId, { isEntry: true });
                    const leaf = { name: bundleId, uid: bundleUid };
                    roots.push(leaf);
                }
                else {
                    roots.push(tree);
                }
            }
            // after trees we process links (this is mostly for uids)
            for (const [, bundle] of Object.entries(outputBundle)) {
                if (bundle.type !== "chunk" || bundle.facadeModuleId == null)
                    continue; //only chunks
                addLinks(bundle.facadeModuleId, this.getModuleInfo.bind(this), mapper);
            }
            const tree = mergeTrees(roots);
            const data = {
                version,
                tree,
                nodeParts: mapper.getNodeParts(),
                nodeMetas: mapper.getNodeMetas(),
                env: {
                    rollup: this.meta.rollupVersion,
                },
                options: {
                    gzip: gzipSize,
                    brotli: brotliSize,
                    sourcemap: !!opts.sourcemap,
                },
            };
            const stringData = replaceHashPlaceholders(data);
            const fileContent = await renderTemplate(template, {
                title,
                data: stringData,
                reportConfig: {
                    sourcemap: !!opts.sourcemap,
                    outputSourcemap: !!outputOptions.sourcemap,
                    gzipSize: {
                        requested: gzipSizeRequested,
                        enabled: gzipSize,
                    },
                    brotliSize: {
                        requested: brotliSizeRequested,
                        enabled: brotliSize,
                    },
                    include: opts.include,
                    exclude: opts.exclude,
                },
            });
            if (opts.emitFile) {
                // Regex checks for filenames starting with `./`, `../`, `.\` or `..\`
                // to account for windows-style path separators
                if (path.isAbsolute(filename) || /^\.{1,2}[/\\]/.test(filename)) {
                    this.error(ERR_FILENAME_EMIT);
                }
                this.emitFile({
                    type: "asset",
                    fileName: filename,
                    source: fileContent,
                });
            }
            else {
                await fs.mkdir(path.dirname(filename), { recursive: true });
                await fs.writeFile(filename, fileContent);
                if (open) {
                    await opn(filename, openOptions);
                }
            }
        },
    };
};
export default visualizer;
