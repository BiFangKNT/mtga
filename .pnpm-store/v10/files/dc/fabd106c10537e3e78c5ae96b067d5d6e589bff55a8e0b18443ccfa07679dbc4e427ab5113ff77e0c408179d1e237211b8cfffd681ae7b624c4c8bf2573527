export function parse(this: ParserContext, ...args: Array<unknown>): TailwindThemeKeyNode;
export function generate(this: ParserContext, node: TailwindThemeKeyNode): void;
/**
 * Name of the Tailwind theme key node.
 * @type {string}
 */
export const name: string;
/**
 * Structure of the Tailwind theme key node.
 * @type {NodeSyntaxConfig["structure"]}
 */
export const structure: NodeSyntaxConfig["structure"];
export type TailwindParserContextThemeKeyExtensions = {
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
    /**
     * - Parses an identifier.
     */
    Identifier: () => CssNode;
    /**
     * - Parses a sequence of tokens within square brackets.
     */
    Brackets: (readSequence: ReadSequenceFunction, recognizer: Recognizer) => CssNode;
    /**
     * - Parses a number.
     */
    Number: () => CssNode;
    /**
     * - Throws an error with the specified message.
     */
    error: (message: string) => void;
    /**
     * - The starting index of the current token in the source string.
     */
    tokenStart: number;
};
export type TailwindThemeKeyNode = CssNodeCommon & {
    children: List<CssNode>;
};
export type TailwindParserThemeKeyContext = ParserContext & TailwindParserContextThemeKeyExtensions;
import type { ParserContext } from "@eslint/css-tree";
import type { NodeSyntaxConfig } from "@eslint/css-tree";
import type { Recognizer } from "@eslint/css-tree";
import type { CssNode } from "@eslint/css-tree";
import type { ReadSequenceFunction } from "@eslint/css-tree";
import type { CssNodeCommon } from "@eslint/css-tree";
import type { List } from "@eslint/css-tree";
