import type { Warning } from "../types/async.js";
export interface GetDissectedClassRequest {
    classes: string[];
    configPath: string | undefined;
    cwd: string;
    tsconfigPath: string | undefined;
}
export interface DissectedClass {
    base: string;
    className: string;
    important: [start: boolean, end: boolean];
    negative: boolean;
    prefix: string;
    separator: string;
    variants: string[];
}
export type GetDissectedClassResponse = {
    dissectedClasses: DissectedClass[];
    warnings: (Warning | undefined)[];
};
export declare function createGetDissectedClasses(): (req: GetDissectedClassRequest) => GetDissectedClassResponse;
//# sourceMappingURL=dissect-classes.d.ts.map