import type { Warning } from "../types/async.js";
export type ConflictingClasses = {
    [className: string]: {
        [conflictingClassName: string]: {
            cssPropertyName: string;
            important: boolean;
            cssPropertyValue?: string;
        }[];
    };
};
export interface GetConflictingClassesRequest {
    classes: string[];
    configPath: string | undefined;
    cwd: string;
    tsconfigPath: string | undefined;
}
export type GetConflictingClassesResponse = {
    conflictingClasses: ConflictingClasses;
    warnings: (Warning | undefined)[];
};
export declare function createGetConflictingClasses(): (req: GetConflictingClassesRequest) => GetConflictingClassesResponse;
//# sourceMappingURL=conflicting-classes.d.ts.map