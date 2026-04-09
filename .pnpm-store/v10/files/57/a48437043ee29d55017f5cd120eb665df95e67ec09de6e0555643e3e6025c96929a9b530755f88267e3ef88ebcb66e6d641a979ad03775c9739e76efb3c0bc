import type { Warning } from "../types/async.js";
export type Prefix = string;
export type Suffix = string;
export interface GetPrefixRequest {
    configPath: string | undefined;
    cwd: string;
    tsconfigPath: string | undefined;
}
export interface GetPrefixResponse {
    prefix: Prefix;
    suffix: Suffix;
    warnings: (Warning | undefined)[];
}
export declare function createGetPrefix(): (req: GetPrefixRequest) => GetPrefixResponse;
//# sourceMappingURL=prefix.d.ts.map