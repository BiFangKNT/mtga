//#region src/tools/parser.d.ts
type ParsedWasmModule = {
  id?: string;
  imports: ModuleImport[];
  exports: ModuleExport[];
};
type ModuleImport = {
  module: string;
  name: string;
  returnType?: string;
  params?: {
    id?: string;
    type: string;
  }[];
};
type ModuleExport = {
  name: string;
  id: string | number;
  type: "Func" | "Memory";
};
type ParseResult = {
  modules: ParsedWasmModule[];
};
declare function parseWasm(source: Buffer | ArrayBuffer, opts?: {
  name?: string;
}): ParseResult;
//#endregion
export { ModuleExport, ModuleImport, ParseResult, ParsedWasmModule, parseWasm };