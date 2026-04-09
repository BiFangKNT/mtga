import path from "node:path";
import { SourceMapConsumer } from "source-map";
const getBytesPerFileUsingSourceMap = (bundleId, code, map, dir) => {
    const modules = {};
    let line = 1;
    let column = 0;
    const codeChars = [...code];
    for (let i = 0; i < codeChars.length; i++, column++) {
        const { source } = map.originalPositionFor({
            line,
            column,
        });
        if (source != null) {
            const id = path.resolve(path.dirname(path.join(dir, bundleId)), source);
            const char = codeChars[i];
            modules[id] = modules[id] || { id, renderedLength: 0, code: [] };
            modules[id].renderedLength += Buffer.byteLength(char);
            modules[id].code.push(char);
        }
        if (code[i] === "\n") {
            line += 1;
            column = -1;
        }
    }
    return modules;
};
export const getSourcemapModules = (id, outputChunk, dir) => {
    if (outputChunk.map == null) {
        return Promise.resolve({});
    }
    return SourceMapConsumer.with(outputChunk.map, null, (map) => {
        return getBytesPerFileUsingSourceMap(id, outputChunk.code, map, dir);
    });
};
