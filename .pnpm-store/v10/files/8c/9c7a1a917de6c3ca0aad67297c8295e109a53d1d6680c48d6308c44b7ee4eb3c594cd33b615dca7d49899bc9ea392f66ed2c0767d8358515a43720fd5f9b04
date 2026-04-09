"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.JSX_CONTAINER_TYPES_TO_INSERT_BRACES = exports.JSX_CONTAINER_TYPES_TO_REPLACE_QUOTES = void 0;
exports.getLiteralsByJSXAttribute = getLiteralsByJSXAttribute;
exports.getAttributesByJSXElement = getAttributesByJSXElement;
const es_js_1 = require("./es.js");
const matchers_js_1 = require("../utils/matchers.js");
const utils_js_1 = require("../utils/utils.js");
exports.JSX_CONTAINER_TYPES_TO_REPLACE_QUOTES = [
    ...es_js_1.ES_CONTAINER_TYPES_TO_REPLACE_QUOTES,
    "JSXAttribute",
    "JSXExpressionContainer"
];
exports.JSX_CONTAINER_TYPES_TO_INSERT_BRACES = [
    ...es_js_1.ES_CONTAINER_TYPES_TO_INSERT_BRACES,
    "JSXAttribute"
];
function getLiteralsByJSXAttribute(ctx, attribute, attributes) {
    const value = attribute.value;
    const literals = attributes.reduce((literals, attributes) => {
        if (!value) {
            return literals;
        }
        const name = getAttributeName(attribute);
        if (typeof name !== "string") {
            return literals;
        }
        if ((0, matchers_js_1.isAttributesName)(attributes)) {
            if (!(0, utils_js_1.matchesName)(attributes.toLowerCase(), name.toLowerCase())) {
                return literals;
            }
            literals.push(...getLiteralsByJSXAttributeValue(ctx, value));
        }
        else if ((0, matchers_js_1.isAttributesRegex)(attributes)) {
            literals.push(...(0, es_js_1.getLiteralsByESNodeAndRegex)(ctx, attribute, attributes));
        }
        else if ((0, matchers_js_1.isAttributesMatchers)(attributes)) {
            if (!(0, utils_js_1.matchesName)(attributes[0].toLowerCase(), name.toLowerCase())) {
                return literals;
            }
            literals.push(...(0, es_js_1.getLiteralsByESMatchers)(ctx, value, attributes[1]));
        }
        return literals;
    }, []);
    return (0, utils_js_1.deduplicateLiterals)(literals);
}
function getAttributesByJSXElement(ctx, node) {
    return node.attributes.reduce((acc, attribute) => {
        if (isJSXAttribute(attribute)) {
            acc.push(attribute);
        }
        return acc;
    }, []);
}
function getAttributeName(attribute) {
    if (attribute.name.type === "JSXIdentifier") {
        return attribute.name.name;
    }
    if (attribute.name.type === "JSXNamespacedName") {
        return `${attribute.name.namespace.name}:${attribute.name.name.name}`;
    }
}
function getLiteralsByJSXAttributeValue(ctx, value) {
    if (!value) {
        return [];
    }
    if ((0, es_js_1.isESSimpleStringLiteral)(value)) {
        const stringLiteral = getStringLiteralByJSXStringLiteral(ctx, value);
        if (stringLiteral) {
            return [stringLiteral];
        }
    }
    if (isJSXExpressionContainerWithESSimpleStringLiteral(value)) {
        const stringLiteral = getStringLiteralByJSXStringLiteral(ctx, value.expression);
        if (stringLiteral) {
            return [stringLiteral];
        }
    }
    if (isJSXExpressionContainerWithESTemplateLiteral(value)) {
        return getLiteralsByJSXTemplateLiteral(ctx, value.expression);
    }
    return [];
}
function getStringLiteralByJSXStringLiteral(ctx, node) {
    const literal = (0, es_js_1.getStringLiteralByESStringLiteral)(ctx, node);
    const multilineQuotes = getMultilineQuotes(node);
    if (!literal) {
        return;
    }
    return {
        ...literal,
        ...multilineQuotes
    };
}
function getLiteralsByJSXTemplateLiteral(ctx, node) {
    const literals = (0, es_js_1.getLiteralsByESTemplateLiteral)(ctx, node);
    return literals.map(literal => {
        if (!(0, es_js_1.hasESNodeParentExtension)(node)) {
            return literal;
        }
        const multilineQuotes = getMultilineQuotes(node);
        return {
            ...literal,
            ...multilineQuotes
        };
    });
}
function getMultilineQuotes(node) {
    const surroundingBraces = exports.JSX_CONTAINER_TYPES_TO_INSERT_BRACES.includes(node.parent.type);
    const multilineQuotes = exports.JSX_CONTAINER_TYPES_TO_REPLACE_QUOTES.includes(node.parent.type)
        ? ["`"]
        : [];
    return {
        multilineQuotes,
        surroundingBraces
    };
}
function isJSXExpressionContainerWithESSimpleStringLiteral(node) {
    return node.type === "JSXExpressionContainer" && "expression" in node &&
        (0, es_js_1.isESNode)(node.expression) &&
        (0, es_js_1.isESSimpleStringLiteral)(node.expression);
}
function isJSXExpressionContainerWithESTemplateLiteral(node) {
    return node.type === "JSXExpressionContainer" && "expression" in node &&
        (0, es_js_1.isESNode)(node.expression) &&
        (0, es_js_1.isESTemplateLiteral)(node.expression);
}
function isJSXAttribute(node) {
    return node.type === "JSXAttribute";
}
//# sourceMappingURL=jsx.js.map