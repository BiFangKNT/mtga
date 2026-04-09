import * as rules from "tailwindcss/lib/lib/generateRules.js";
export function getUnregisteredClasses(context, classes) {
    return classes
        .filter(className => {
        const generated = rules.generateRules?.([className], context) ?? rules.default?.generateRules?.([className], context);
        return generated.length === 0;
    });
}
//# sourceMappingURL=unregistered-classes.async.v3.js.map