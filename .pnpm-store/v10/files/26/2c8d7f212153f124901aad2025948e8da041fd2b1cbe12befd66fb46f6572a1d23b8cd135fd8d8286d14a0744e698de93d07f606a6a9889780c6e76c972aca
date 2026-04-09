import type { Warning } from "../types/async.js";
export type ClassOrder = [className: string, order: bigint | null][];
export interface GetClassOrderRequest {
    classes: string[];
    configPath: string | undefined;
    cwd: string;
    tsconfigPath: string | undefined;
}
export type GetClassOrderResponse = {
    classOrder: ClassOrder;
    warnings: (Warning | undefined)[];
};
export declare function createGetClassOrder(): (req: GetClassOrderRequest) => GetClassOrderResponse;
//# sourceMappingURL=class-order.d.ts.map