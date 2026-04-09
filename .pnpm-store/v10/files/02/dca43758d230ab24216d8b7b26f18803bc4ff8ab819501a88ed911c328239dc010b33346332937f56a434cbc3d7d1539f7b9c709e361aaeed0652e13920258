"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createRuleListener = createRuleListener;
const angular_js_1 = require("../parsers/angular.js");
const es_js_1 = require("../parsers/es.js");
const html_js_1 = require("../parsers/html.js");
const jsx_js_1 = require("../parsers/jsx.js");
const svelte_js_1 = require("../parsers/svelte.js");
const vue_js_1 = require("../parsers/vue.js");
const tailwindcss_js_1 = require("../async-utils/tailwindcss.js");
const warn_js_1 = require("./warn.js");
function createRuleListener(ctx, initialize, getOptions, lintLiterals) {
    if (!(0, tailwindcss_js_1.isTailwindcssInstalled)()) {
        (0, warn_js_1.warnOnce)(`Tailwind CSS is not installed. Disabling rule ${ctx.id}.`);
        return {};
    }
    initialize();
    const { attributes, callees, tags, variables } = getOptions(ctx);
    const callExpression = {
        CallExpression(node) {
            const callExpressionNode = node;
            const literals = (0, es_js_1.getLiteralsByESCallExpression)(ctx, callExpressionNode, callees);
            lintLiterals(ctx, literals);
        }
    };
    const variableDeclarators = {
        VariableDeclarator(node) {
            const variableDeclaratorNode = node;
            const literals = (0, es_js_1.getLiteralsByESVariableDeclarator)(ctx, variableDeclaratorNode, variables);
            lintLiterals(ctx, literals);
        }
    };
    const taggedTemplateExpression = {
        TaggedTemplateExpression(node) {
            const taggedTemplateExpressionNode = node;
            const literals = (0, es_js_1.getLiteralsByTaggedTemplateExpression)(ctx, taggedTemplateExpressionNode, tags);
            lintLiterals(ctx, literals);
        }
    };
    const jsx = {
        JSXOpeningElement(node) {
            const jsxNode = node;
            const jsxAttributes = (0, jsx_js_1.getAttributesByJSXElement)(ctx, jsxNode);
            for (const jsxAttribute of jsxAttributes) {
                const attributeValue = jsxAttribute.value;
                if (!attributeValue) {
                    continue;
                }
                const literals = (0, jsx_js_1.getLiteralsByJSXAttribute)(ctx, jsxAttribute, attributes);
                lintLiterals(ctx, literals);
            }
        }
    };
    const svelte = {
        SvelteStartTag(node) {
            const svelteNode = node;
            const svelteAttributes = (0, svelte_js_1.getAttributesBySvelteTag)(ctx, svelteNode);
            for (const svelteAttribute of svelteAttributes) {
                const attributeName = svelteAttribute.key.name;
                if (typeof attributeName !== "string") {
                    continue;
                }
                const literals = (0, svelte_js_1.getLiteralsBySvelteAttribute)(ctx, svelteAttribute, attributes);
                lintLiterals(ctx, literals);
            }
        }
    };
    const vue = {
        VStartTag(node) {
            const vueNode = node;
            const vueAttributes = (0, vue_js_1.getAttributesByVueStartTag)(ctx, vueNode);
            for (const attribute of vueAttributes) {
                const literals = (0, vue_js_1.getLiteralsByVueAttribute)(ctx, attribute, attributes);
                lintLiterals(ctx, literals);
            }
        }
    };
    const html = {
        Tag(node) {
            const htmlTagNode = node;
            const htmlAttributes = (0, html_js_1.getAttributesByHTMLTag)(ctx, htmlTagNode);
            for (const htmlAttribute of htmlAttributes) {
                const literals = (0, html_js_1.getLiteralsByHTMLAttribute)(ctx, htmlAttribute, attributes);
                lintLiterals(ctx, literals);
            }
        }
    };
    const angular = {
        Element(node) {
            const angularElementNode = node;
            const angularAttributes = (0, angular_js_1.getAttributesByAngularElement)(ctx, angularElementNode);
            for (const angularAttribute of angularAttributes) {
                const literals = (0, angular_js_1.getLiteralsByAngularAttribute)(ctx, angularAttribute, attributes);
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