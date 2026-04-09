export async function getConflictingClasses(context, classes) {
    var _a;
    const conflicts = {};
    const classRules = classes.reduce((classRules, className) => ({
        ...classRules,
        [className]: context.parseCandidate(className).reduce((classRules, candidate) => {
            const [rule] = context.compileAstNodes(candidate);
            return {
                ...classRules,
                ...getRuleContext(rule?.node?.nodes)
            };
        }, {})
    }), {});
    for (const className in classRules) {
        otherClassLoop: for (const otherClassName in classRules) {
            if (className === otherClassName) {
                continue otherClassLoop;
            }
            const classRule = classRules[className];
            const otherClassRule = classRules[otherClassName];
            const paths = Object.keys(classRule);
            const otherPaths = Object.keys(otherClassRule);
            if (paths.length !== otherPaths.length) {
                continue otherClassLoop;
            }
            for (const path of paths) {
                for (const otherPath of otherPaths) {
                    if (path !== otherPath) {
                        continue otherClassLoop;
                    }
                    if (classRule[path].length !== otherClassRule[otherPath].length) {
                        continue otherClassLoop;
                    }
                    for (const classRuleProperty of classRule[path]) {
                        if (!otherClassRule[otherPath].find(otherProp => {
                            return otherProp.cssPropertyName === classRuleProperty.cssPropertyName;
                        })) {
                            continue otherClassLoop;
                        }
                    }
                    for (const otherClassRuleProperty of otherClassRule[otherPath]) {
                        conflicts[className] ?? (conflicts[className] = {});
                        (_a = conflicts[className])[otherClassName] ?? (_a[otherClassName] = []);
                        conflicts[className][otherClassName].push(otherClassRuleProperty);
                    }
                }
            }
        }
    }
    return conflicts;
}
function getRuleContext(nodes) {
    const context = {};
    if (!nodes) {
        return context;
    }
    const checkNested = (nodes, context, path = "") => {
        for (const node of nodes.filter(node => !!node)) {
            if (node.kind === "declaration") {
                context[path] ?? (context[path] = []);
                if (node.value === undefined) {
                    continue;
                }
                context[path].push({
                    cssPropertyName: node.property,
                    cssPropertyValue: node.value,
                    important: node.important
                });
                continue;
            }
            if (node.kind === "rule") {
                return void checkNested(node.nodes, context, path + node.selector);
            }
            if (node.kind === "at-rule") {
                return void checkNested(node.nodes, context, path + node.name + node.params);
            }
        }
    };
    checkNested(nodes, context);
    return context;
}
//# sourceMappingURL=conflicting-classes.async.v4.js.map