/**
 * Reads a sequence of tokens that represent a Tailwind theme() function argument.
 * @this {TailwindParserThemeContext}
 * @param {Recognizer} recognizer - The recognizer instance used to parse tokens.
 * @returns {List<CssNode>} An array of CSS nodes representing the parsed theme function argument.
 */
export default function _default(this: TailwindParserThemeContext, recognizer: Recognizer): List<CssNode>;
export type TailwindParserContextThemeExtensions = {
    /**
     * - Parses the key of the theme function.
     */
    TailwindThemeKey: (recognizer: Recognizer) => CssNode;
    /**
     * - Parses the operator (slash).
     */
    Operator: () => CssNode;
    /**
     * - Parses a percentage value.
     */
    Percentage: () => CssNode;
};
export type TailwindParserThemeContext = ParserContext & TailwindParserContextThemeExtensions;
import type { Recognizer } from "@eslint/css-tree";
import type { CssNode } from "@eslint/css-tree";
import type { List } from "@eslint/css-tree";
import type { ParserContext } from "@eslint/css-tree";
