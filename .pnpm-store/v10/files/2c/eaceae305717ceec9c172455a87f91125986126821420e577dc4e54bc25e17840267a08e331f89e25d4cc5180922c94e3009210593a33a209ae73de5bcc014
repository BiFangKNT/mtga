"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.TSCONFIG_SCHEMA = exports.TAILWIND_CONFIG_SCHEMA = exports.ENTRYPOINT_SCHEMA = exports.TAG_SCHEMA = exports.VARIABLE_SCHEMA = exports.ATTRIBUTE_SCHEMA = exports.CALLEE_SCHEMA = void 0;
const rule_js_1 = require("../types/rule.js");
const STRING_MATCHER_SCHEMA = {
    additionalProperties: false,
    properties: {
        match: {
            description: "Matcher type that will be applied.",
            enum: [rule_js_1.MatcherType.String],
            type: "string"
        }
    },
    type: "object"
};
const OBJECT_KEY_MATCHER_SCHEMA = {
    additionalProperties: false,
    properties: {
        match: {
            description: "Matcher type that will be applied.",
            enum: [rule_js_1.MatcherType.ObjectKey],
            type: "string"
        },
        pathPattern: {
            description: "Regular expression that filters the object key and matches the content for further processing in a group.",
            type: "string"
        }
    },
    type: "object"
};
const OBJECT_VALUE_MATCHER_SCHEMA = {
    additionalProperties: false,
    properties: {
        match: {
            description: "Matcher type that will be applied.",
            enum: [rule_js_1.MatcherType.ObjectValue],
            type: "string"
        },
        pathPattern: {
            description: "Regular expression that filters the object value and matches the content for further processing in a group.",
            type: "string"
        }
    },
    type: "object"
};
const ATTRIBUTE_REGEX_CONFIG = {
    description: "List of regular expressions that matches string literals which should get linted.",
    items: [
        {
            description: "Regular expression that filters the attribute and matches the content for further processing in a group.",
            type: "string"
        },
        {
            description: "Regular expression that matches each string literal in a group.",
            type: "string"
        }
    ],
    type: "array"
};
const ATTRIBUTE_MATCHER_CONFIG = {
    description: "List of matchers that will automatically be matched.",
    items: [
        {
            description: "Attribute name for which children get linted if matched.",
            type: "string"
        },
        {
            description: "List of matchers that will be applied.",
            items: {
                anyOf: [
                    STRING_MATCHER_SCHEMA,
                    OBJECT_KEY_MATCHER_SCHEMA,
                    OBJECT_VALUE_MATCHER_SCHEMA
                ],
                type: "object"
            },
            type: "array"
        }
    ],
    type: "array"
};
const ATTRIBUTE_NAME_CONFIG = {
    description: "Attribute name that for which children get linted.",
    type: "string"
};
const CALLEE_REGEX_CONFIG = {
    description: "List of regular expressions that matches string literals which should get linted.",
    items: [
        {
            description: "Regular expression that filters the callee and matches the content for further processing in a group.",
            type: "string"
        },
        {
            description: "Regular expression that matches each string literal in a group.",
            type: "string"
        }
    ],
    type: "array"
};
const CALLEE_MATCHER_CONFIG = {
    description: "List of matchers that will automatically be matched.",
    items: [
        {
            description: "Callee name for which children get linted if matched.",
            type: "string"
        },
        {
            description: "List of matchers that will be applied.",
            items: {
                anyOf: [
                    STRING_MATCHER_SCHEMA,
                    OBJECT_KEY_MATCHER_SCHEMA,
                    OBJECT_VALUE_MATCHER_SCHEMA
                ],
                type: "object"
            },
            type: "array"
        }
    ],
    type: "array"
};
const CALLEE_NAME_CONFIG = {
    description: "Callee name for which children get linted.",
    type: "string"
};
const VARIABLE_REGEX_CONFIG = {
    description: "List of regular expressions that matches string literals which should get linted.",
    items: [
        {
            description: "Regular expression that filters the variable and matches the content for further processing in a group.",
            type: "string"
        },
        {
            description: "Regular expression that matches each string literal in a group.",
            type: "string"
        }
    ],
    type: "array"
};
const VARIABLE_MATCHER_CONFIG = {
    description: "List of matchers that will automatically be matched.",
    items: [
        {
            description: "Variable name for which children get linted if matched.",
            type: "string"
        },
        {
            description: "List of matchers that will be applied.",
            items: {
                anyOf: [
                    STRING_MATCHER_SCHEMA,
                    OBJECT_KEY_MATCHER_SCHEMA,
                    OBJECT_VALUE_MATCHER_SCHEMA
                ],
                type: "object"
            },
            type: "array"
        }
    ],
    type: "array"
};
const VARIABLE_NAME_CONFIG = {
    description: "Variable name for which children get linted.",
    type: "string"
};
const TAG_REGEX_CONFIG = {
    description: "List of regular expressions that matches string literals which should get linted.",
    items: [
        {
            description: "Regular expression that filters the template literal tags and matches the content for further processing in a group.",
            type: "string"
        },
        {
            description: "Regular expression that matches each string literal in a group.",
            type: "string"
        }
    ],
    type: "array"
};
const TAG_MATCHER_CONFIG = {
    description: "List of matchers that will automatically be matched.",
    items: [
        {
            description: "Template literal tag for which children get linted if matched.",
            type: "string"
        },
        {
            description: "List of matchers that will be applied.",
            items: {
                anyOf: [
                    STRING_MATCHER_SCHEMA,
                    OBJECT_KEY_MATCHER_SCHEMA,
                    OBJECT_VALUE_MATCHER_SCHEMA
                ],
                type: "object"
            },
            type: "array"
        }
    ],
    type: "array"
};
const TAG_NAME_CONFIG = {
    description: "Template literal tag that should get linted.",
    type: "string"
};
exports.CALLEE_SCHEMA = {
    callees: {
        description: "List of function names which arguments should get linted.",
        items: {
            anyOf: [
                CALLEE_REGEX_CONFIG,
                CALLEE_MATCHER_CONFIG,
                CALLEE_NAME_CONFIG
            ]
        },
        type: "array"
    }
};
exports.ATTRIBUTE_SCHEMA = {
    attributes: {
        description: "List of attribute names that should get linted.",
        items: {
            anyOf: [
                ATTRIBUTE_NAME_CONFIG,
                ATTRIBUTE_REGEX_CONFIG,
                ATTRIBUTE_MATCHER_CONFIG
            ]
        },
        type: "array"
    }
};
exports.VARIABLE_SCHEMA = {
    variables: {
        description: "List of variable names which values should get linted.",
        items: {
            anyOf: [
                VARIABLE_REGEX_CONFIG,
                VARIABLE_MATCHER_CONFIG,
                VARIABLE_NAME_CONFIG
            ]
        },
        type: "array"
    }
};
exports.TAG_SCHEMA = {
    tags: {
        description: "List of template literal tags that should get linted.",
        items: {
            anyOf: [
                TAG_REGEX_CONFIG,
                TAG_MATCHER_CONFIG,
                TAG_NAME_CONFIG
            ]
        },
        type: "array"
    }
};
exports.ENTRYPOINT_SCHEMA = {
    entryPoint: {
        description: "The path to the css entry point of the project. If not specified, the plugin will fall back to the default tailwind classes.",
        type: "string"
    }
};
exports.TAILWIND_CONFIG_SCHEMA = {
    tailwindConfig: {
        description: "The path to the tailwind config file. If not specified, the plugin will try to find it automatically or falls back to the default configuration.",
        type: "string"
    }
};
exports.TSCONFIG_SCHEMA = {
    tsconfig: {
        description: "The path to the tsconfig file. Is used to resolve path aliases in the tsconfig.",
        type: "string"
    }
};
//# sourceMappingURL=descriptions.js.map