import { getTailwindcssVersion, TailwindcssVersion } from "../async-utils/tailwindcss.js";
import { createTailwindContext as createTailwindContextV3 } from "./context.async.v3.js";
import { createTailwindContext as createTailwindContextV4 } from "./context.async.v4.js";
export async function createTailwindContext(ctx) {
    const version = getTailwindcssVersion();
    if (version.major === TailwindcssVersion.V3) {
        return createTailwindContextV3(ctx);
    }
    else {
        return createTailwindContextV4(ctx);
    }
}
//# sourceMappingURL=context.async.js.map