"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildClass = buildClass;
const tailwindcss_js_1 = require("../async-utils/tailwindcss.js");
function buildClass({ base, important, negative, prefix, separator, variants }) {
    const { major } = (0, tailwindcss_js_1.getTailwindcssVersion)();
    const importantAtStart = important[0] && "!";
    const importantAtEnd = important[1] && "!";
    const negativePrefix = negative && "-";
    if (major >= 4 /* TailwindcssVersion.V4 */) {
        return [
            prefix,
            ...variants,
            [importantAtStart, negativePrefix, base, importantAtEnd].filter(Boolean).join("")
        ].filter(Boolean).join(separator);
    }
    else {
        return [
            ...variants,
            [importantAtStart, prefix, negativePrefix, base, importantAtEnd].filter(Boolean).join("")
        ].filter(Boolean).join(separator);
    }
}
//# sourceMappingURL=class.js.map