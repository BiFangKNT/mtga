/**
 * @fileoverview The theme() function parser for Tailwind CSS.
 * @author Nicholas C. Zakas
 */
//-----------------------------------------------------------------------------
// Type Definitions
//-----------------------------------------------------------------------------
/**
 * @import { CssNode, List, ParserContext, Recognizer } from "@eslint/css-tree";
 *
 * @typedef {Object} TailwindParserContextThemeExtensions
 * @property {(recognizer: Recognizer) => CssNode} TailwindThemeKey - Parses the key of the theme function.
 * @property {() => CssNode} Operator - Parses the operator (slash).
 * @property {() => CssNode} Percentage - Parses a percentage value.
 *
 * @typedef {ParserContext & TailwindParserContextThemeExtensions} TailwindParserThemeContext
 */
//-----------------------------------------------------------------------------
// Helpers
//-----------------------------------------------------------------------------
const SLASH = 47; // ASCII code for '/'
//-----------------------------------------------------------------------------
// Exports
//-----------------------------------------------------------------------------
/**
 * Reads a sequence of tokens that represent a Tailwind theme() function argument.
 * @this {TailwindParserThemeContext}
 * @param {Recognizer} recognizer - The recognizer instance used to parse tokens.
 * @returns {List<CssNode>} An array of CSS nodes representing the parsed theme function argument.
 */
export default function (recognizer) {
    const children = this.createList();
    // parse key first
    children.push(this.TailwindThemeKey(recognizer));
    // the next token could be a / followed by a percentage
    if (this.isDelim(SLASH)) {
        children.push(this.Operator());
        this.skipSC();
        children.push(this.Percentage());
        this.skipSC();
    }
    return children;
}
;
