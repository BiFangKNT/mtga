import { ES_CONTAINER_TYPES_TO_INSERT_BRACES, ES_CONTAINER_TYPES_TO_REPLACE_QUOTES, getLiteralsByESMatchers, getLiteralsByESNodeAndRegex, getLiteralsByESTemplateLiteral, getStringLiteralByESStringLiteral, hasESNodeParentExtension, isESNode, isESSimpleStringLiteral, isESTemplateLiteral } from "./es.js";
import { isAttributesMatchers, isAttributesName, isAttributesRegex } from "../utils/matchers.js";
import { deduplicateLiterals, matchesName } from "../utils/utils.js";
export const JSX_CONTAINER_TYPES_TO_REPLACE_QUOTES = [
    ...ES_CONTAINER_TYPES_TO_REPLACE_QUOTES,
    "JSXAttribute",
    "JSXExpressionContainer"
];
export const JSX_CONTAINER_TYPES_TO_INSERT_BRACES = [
    ...ES_CONTAINER_TYPES_TO_INSERT_BRACES,
    "JSXAttribute"
];
export function getLiteralsByJSXAttribute(ctx, attribute, attributes) {
    const value = attribute.value;
    const literals = attributes.reduce((literals, attributes) => {
        if (!value) {
            return literals;
        }
        const name = getAttributeName(attribute);
        if (typeof name !== "string") {
            return literals;
        }
        if (isAttributesName(attributes)) {
            if (!matchesName(attributes.toLowerCase(), name.toLowerCase())) {
                return literals;
            }
            literals.push(...getLiteralsByJSXAttributeValue(ctx, value));
        }
        else if (isAttributesRegex(attributes)) {
            literals.push(...getLiteralsByESNodeAndRegex(ctx, attribute, attributes));
        }
        else if (isAttributesMatchers(attributes)) {
            if (!matchesName(attributes[0].toLowerCase(), name.toLowerCase())) {
                return literals;
            }
            literals.push(...getLiteralsByESMatchers(ctx, value, attributes[1]));
        }
        return literals;
    }, []);
    return deduplicateLiterals(literals);
}
export function getAttributesByJSXElement(ctx, node) {
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
    if (isESSimpleStringLiteral(value)) {
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
    const literal = getStringLiteralByESStringLiteral(ctx, node);
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
    const literals = getLiteralsByESTemplateLiteral(ctx, node);
    return literals.map(literal => {
        if (!hasESNodeParentExtension(node)) {
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
    const surroundingBraces = JSX_CONTAINER_TYPES_TO_INSERT_BRACES.includes(node.parent.type);
    const multilineQuotes = JSX_CONTAINER_TYPES_TO_REPLACE_QUOTES.includes(node.parent.type)
        ? ["`"]
        : [];
    return {
        multilineQuotes,
        surroundingBraces
    };
}
function isJSXExpressionContainerWithESSimpleStringLiteral(node) {
    return node.type === "JSXExpressionContainer" && "expression" in node &&
        isESNode(node.expression) &&
        isESSimpleStringLiteral(node.expression);
}
function isJSXExpressionContainerWithESTemplateLiteral(node) {
    return node.type === "JSXExpressionContainer" && "expression" in node &&
        isESNode(node.expression) &&
        isESTemplateLiteral(node.expression);
}
function isJSXAttribute(node) {
    return node.type === "JSXAttribute";
}
//# sourceMappingURL=jsx.js.map