/**
 * @fileoverview Tailwind 3 Custom Syntax for CSSTree.
 * @author Nicholas C. Zakas
 */
//-----------------------------------------------------------------------------
// Imports
//-----------------------------------------------------------------------------
import defaultSyntax from "@eslint/css-tree/definition-syntax-data";
import * as TailwindThemeKey from "./node/tailwind-theme-key.js";
import * as TailwindUtilityClass from "./node/tailwind-class.js";
import tailwindApply from "./atrule/tailwind-apply.js";
import theme from "./scope/theme.js";
import { themeTypes } from "./types/theme-types.js";
//-----------------------------------------------------------------------------
// Type Definitions
//-----------------------------------------------------------------------------
/**
 * @typedef {import("@eslint/css-tree").NodeSyntaxConfig} NodeSyntaxConfig
 * @import { SyntaxConfig } from "@eslint/css-tree"
 */
/** @type {Partial<SyntaxConfig>} */
export const tailwind3 = {
    atrule: {
        apply: tailwindApply,
    },
    atrules: {
        apply: {
            prelude: "<tw-apply-ident>+",
        },
        tailwind: {
            prelude: "base | components | utilities | variants",
        },
        config: {
            prelude: "<string>",
        }
    },
    types: {
        "length-percentage": `${defaultSyntax.types["length-percentage"]} | <tw-theme-spacing>`,
        "color": `${defaultSyntax.types.color} | <tw-theme-color>`,
        "tw-apply-ident": "<ident> | [ <ident> ':' <ident> ]",
        ...themeTypes
    },
    node: {
        TailwindThemeKey,
        TailwindUtilityClass
    },
    scope: {
        Value: {
            theme
        }
    }
};
