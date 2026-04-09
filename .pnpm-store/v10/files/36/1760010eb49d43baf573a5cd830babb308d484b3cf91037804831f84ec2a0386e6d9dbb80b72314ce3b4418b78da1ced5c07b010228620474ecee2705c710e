import { env } from "node:process";
import { TsRunner } from "synckit";
export function getWorkerOptions() {
    if (env.NODE_ENV === "test") {
        return {
            tsRunner: TsRunner.TsNode
        };
    }
}
//# sourceMappingURL=worker.js.map