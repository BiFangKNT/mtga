import { getAttributesByAngularElement, getLiteralsByAngularAttribute } from "../parsers/angular.js";
import { getLiteralsByESCallExpression, getLiteralsByESVariableDeclarator, getLiteralsByTaggedTemplateExpression } from "../parsers/es.js";
import { getAttributesByHTMLTag, getLiteralsByHTMLAttribute } from "../parsers/html.js";
import { getAttributesByJSXElement, getLiteralsByJSXAttribute } from "../parsers/jsx.js";
import { getAttributesBySvelteTag, getLiteralsBySvelteAttribute } from "../parsers/svelte.js";
import { getAttributesByVueStartTag, getLiteralsByVueAttribute } from "../parsers/vue.js";
import { isTailwindcssInstalled } from "../async-utils/tailwindcss.js";
import { warnOnce } from "./warn.js";
export function createRuleListener(ctx, initialize, getOptions, lintLiterals) {
    if (!isTailwindcssInstalled()) {
        warnOnce(`Tailwind CSS is not installed. Disabling rule ${ctx.id}.`);
        return {};
    }
    initialize();
    const { attributes, callees, tags, variables } = getOptions(ctx);
    const callExpression = {
        CallExpression(node) {
            const callExpressionNode = node;
            const literals = getLiteralsByESCallExpression(ctx, callExpressionNode, callees);
            lintLiterals(ctx, literals);
        }
    };
    const variableDeclarators = {
        VariableDeclarator(node) {
            const variableDeclaratorNode = node;
            const literals = getLiteralsByESVariableDeclarator(ctx, variableDeclaratorNode, variables);
            lintLiterals(ctx, literals);
        }
    };
    const taggedTemplateExpression = {
        TaggedTemplateExpression(node) {
            const taggedTemplateExpressionNode = node;
            const literals = getLiteralsByTaggedTemplateExpression(ctx, taggedTemplateExpressionNode, tags);
            lintLiterals(ctx, literals);
        }
    };
    const jsx = {
        JSXOpeningElement(node) {
            const jsxNode = node;
            const jsxAttributes = getAttributesByJSXElement(ctx, jsxNode);
            for (const jsxAttribute of jsxAttributes) {
                const attributeValue = jsxAttribute.value;
                if (!attributeValue) {
                    continue;
                }
                const literals = getLiteralsByJSXAttribute(ctx, jsxAttribute, attributes);
                lintLiterals(ctx, literals);
            }
        }
    };
    const svelte = {
        SvelteStartTag(node) {
            const svelteNode = node;
            const svelteAttributes = getAttributesBySvelteTag(ctx, svelteNode);
            for (const svelteAttribute of svelteAttributes) {
                const attributeName = svelteAttribute.key.name;
                if (typeof attributeName !== "string") {
                    continue;
                }
                const literals = getLiteralsBySvelteAttribute(ctx, svelteAttribute, attributes);
                lintLiterals(ctx, literals);
            }
        }
    };
    const vue = {
        VStartTag(node) {
            const vueNode = node;
            const vueAttributes = getAttributesByVueStartTag(ctx, vueNode);
            for (const attribute of vueAttributes) {
                const literals = getLiteralsByVueAttribute(ctx, attribute, attributes);
                lintLiterals(ctx, literals);
            }
        }
    };
    const html = {
        Tag(node) {
            const htmlTagNode = node;
            const htmlAttributes = getAttributesByHTMLTag(ctx, htmlTagNode);
            for (const htmlAttribute of htmlAttributes) {
                const literals = getLiteralsByHTMLAttribute(ctx, htmlAttribute, attributes);
                lintLiterals(ctx, literals);
            }
        }
    };
    const angular = {
        Element(node) {
            const angularElementNode = node;
            const angularAttributes = getAttributesByAngularElement(ctx, angularElementNode);
            for (const angularAttribute of angularAttributes) {
                const literals = getLiteralsByAngularAttribute(ctx, angularAttribute, attributes);
                lintLiterals(ctx, literals);
            }
        }
    };
    // Vue
    if (typeof ctx.sourceCode.parserServices?.defineTemplateBodyVisitor === "function") {
        return {
            // script tag
            ...callExpression,
            ...variableDeclarators,
            ...taggedTemplateExpression,
            // bound classes
            ...ctx.sourceCode.parserServices.defineTemplateBodyVisitor({
                ...callExpression,
                ...vue
            })
        };
    }
    return {
        ...callExpression,
        ...variableDeclarators,
        ...taggedTemplateExpression,
        ...jsx,
        ...svelte,
        ...vue,
        ...html,
        ...angular
    };
}
//# sourceMappingURL=rule.js.map