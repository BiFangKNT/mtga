import { s as EncodedSourceMap } from "./types-EZz9rsDw.mjs";
import { TransformResult } from "vite";

//#region src/source-map.d.ts
interface InstallSourceMapSupportOptions {
  getSourceMap: (source: string) => EncodedSourceMap | null | undefined;
}
declare function withInlineSourcemap(result: TransformResult, options: {
  root: string;
  filepath: string;
  noFirstLineMapping?: boolean;
}): TransformResult;
declare function extractSourceMap(code: string): EncodedSourceMap | null;
declare function installSourcemapsSupport(options: InstallSourceMapSupportOptions): void;
//#endregion
export { extractSourceMap, installSourcemapsSupport, withInlineSourcemap };