/**
 * @fileoverview The TailwindThemeKey node
 * @author Nicholas C. Zakas
 */
//-----------------------------------------------------------------------------
// Imports
//-----------------------------------------------------------------------------
import { tokenTypes } from "@eslint/css-tree";
//-----------------------------------------------------------------------------
// Type Definitions
//-----------------------------------------------------------------------------
/**
 * @import { NodeSyntaxConfig, TokenStream } from "@eslint/css-tree";
 */
/**
 * @import { CssNode, List, ParserContext, Recognizer, ReadSequenceFunction, CssNodeCommon } from "@eslint/css-tree";
 *
 * @typedef {Object} TailwindParserContextThemeKeyExtensions
 * @property {(recognizer: Recognizer) => CssNode} TailwindThemeKey - Parses the key of the theme function.
 * @property {() => CssNode} Operator - Parses the operator (slash).
 * @property {() => CssNode} Percentage - Parses a percentage value.
 * @property {() => CssNode} Identifier - Parses an identifier.
 * @property {(readSequence: ReadSequenceFunction, recognizer: Recognizer) => CssNode} Brackets - Parses a sequence of tokens within square brackets.
 * @property {() => CssNode} Number - Parses a number.
 * @property {(message: string) => void} error - Throws an error with the specified message.
 * @property {number} tokenStart - The starting index of the current token in the source string.
 *
 * @typedef {CssNodeCommon & { children: List<CssNode>}} TailwindThemeKeyNode
 *
 * @typedef {ParserContext & TailwindParserContextThemeKeyExtensions} TailwindParserThemeKeyContext
 */
//-----------------------------------------------------------------------------
// Helpers
//-----------------------------------------------------------------------------
const DOT = 46; // ASCII code for '.'
/**
 * Reads a sequence of tokens that represent a Tailwind theme() function argument.
 * @this {TailwindParserThemeKeyContext}
 * @param {Recognizer} recognizer - The recognizer instance used to parse tokens.
 * @returns {List<CssNode>} An array of CSS nodes representing the parsed theme function argument.
 */
function readKey(recognizer) {
    const children = this.createList();
    this.skipSC();
    children.push(this.Identifier());
    while (this.isDelim(DOT)) {
        children.push(this.Operator());
        // can be an identifier, a square bracket, or a number
        switch (this.tokenType) {
            case tokenTypes.Ident:
                children.push(this.Identifier());
                break;
            default:
                this.error("Expected identifier, square bracket, or number after '.' in theme function.");
        }
    }
    if (this.tokenType === tokenTypes.LeftSquareBracket) {
        children.push(this.Brackets(this.readSequence, recognizer));
    }
    /*
     * A bit weird here. CSS tokenization allows a number to begin with a dot,
     * so something like colors.gray.900 means that .900 is considered a number.
     * To account for that, we check if there is a number, and if so, if the first
     * character is a dot. If it is, we treat it as an operator.
     */
    if (this.tokenType === tokenTypes.Number) {
        // number can begin with a dot, so we need to check if the character is a dot
        if (this.source.charCodeAt(this.tokenStart) === DOT) {
            children.push({
                type: "Operator",
                loc: this.getLocation(this.tokenStart, this.tokenStart + 1),
                value: this.substrToCursor(this.tokenStart++)
            });
        }
        children.push(this.Number());
    }
    this.skipSC();
    return children;
}
//-----------------------------------------------------------------------------
// Exports
//-----------------------------------------------------------------------------
/**
 * Name of the Tailwind theme key node.
 * @type {string}
 */
export const name = "TailwindThemeKey";
/**
 * Structure of the Tailwind theme key node.
 * @type {NodeSyntaxConfig["structure"]}
 */
export const structure = {
    name: String,
    children: [[]]
};
/**
 * Parse method for Tailwind theme key node.
 * Handles Tailwind functions such as theme(colors.gray.900/75%) and theme(spacing[2.5]).
 * @this {TailwindParserThemeKeyContext}
 * @param {Recognizer} recognizer - The recognizer instance used to parse tokens.
 * @type {NodeSyntaxConfig<TailwindThemeKeyNode>["parse"]}
 */
export function parse(recognizer) {
    const start = this.tokenStart;
    const children = readKey.call(this, recognizer);
    return {
        type: name,
        loc: this.getLocation(start, this.tokenStart),
        children
    };
}
/**
 * Generate method for Tailwind theme key node.
 * @type {NodeSyntaxConfig<TailwindThemeKeyNode>["generate"]}
 */
export function generate(node) {
    // @ts-ignore -- need to fix later
    this.children(node);
}
