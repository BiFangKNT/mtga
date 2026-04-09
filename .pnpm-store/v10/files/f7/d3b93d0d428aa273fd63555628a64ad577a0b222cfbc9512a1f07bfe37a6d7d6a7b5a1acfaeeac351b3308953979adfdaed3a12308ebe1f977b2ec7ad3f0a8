import type { Warning } from "../types/async.js";
export interface GetTailwindConfigRequest {
    configPath: string | undefined;
    cwd: string;
    version: {
        major: number;
        minor: number;
        patch: number;
    };
}
export interface GetTailwindConfigResponse {
    path: string;
    warnings: (Warning | undefined)[];
}
export declare const getTailwindConfigPath: ({ configPath, cwd, version }: GetTailwindConfigRequest) => GetTailwindConfigResponse;
//# sourceMappingURL=config.d.ts.map