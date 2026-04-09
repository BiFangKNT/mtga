import type { Warning } from "../types/async.js";
export interface AsyncContext {
    cwd: string;
    tailwindConfigPath: string;
    tsconfigPath: string | undefined;
    version: {
        major: number;
        minor: number;
        patch: number;
    };
}
export interface GetAsyncContextRequest {
    cwd: string;
    configPath?: string;
    tsconfigPath?: string;
}
export interface GetAsyncContextResponse {
    ctx: AsyncContext;
    warnings: (Warning | undefined)[];
}
export declare function getAsyncContext({ configPath, cwd, tsconfigPath }: GetAsyncContextRequest): Promise<GetAsyncContextResponse>;
//# sourceMappingURL=context.d.ts.map