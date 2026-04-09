import type { Warning } from "../types/async.js";
export type UnregisteredClass = string;
export interface GetUnregisteredClassesRequest {
    classes: string[];
    configPath: string | undefined;
    cwd: string;
    tsconfigPath: string | undefined;
}
export type GetUnregisteredClassesResponse = {
    unregisteredClasses: UnregisteredClass[];
    warnings: (Warning | undefined)[];
};
export declare function createGetUnregisteredClasses(): (req: GetUnregisteredClassesRequest) => GetUnregisteredClassesResponse;
//# sourceMappingURL=unregistered-classes.d.ts.map