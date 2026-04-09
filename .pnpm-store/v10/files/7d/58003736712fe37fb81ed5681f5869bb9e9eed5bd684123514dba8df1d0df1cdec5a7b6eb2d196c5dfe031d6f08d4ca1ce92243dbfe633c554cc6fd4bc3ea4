export function parse(this: ParserContext, ...args: Array<unknown>): TailwindUtilityClassNode;
export function generate(this: ParserContext, node: TailwindUtilityClassNode): void;
/**
 * @import { NodeSyntaxConfig } from "@eslint/css-tree";
 */
/**
 * @import { CssNode, CssNodeCommon, ParserContext, Recognizer, Identifier } from "@eslint/css-tree";
 *
 * @typedef {Object} TailwindParserContextApplyExtensions
 * @property {(recognizer: Recognizer) => CssNode} TailwindThemeKey - Parses the key of the theme function.
 * @property {() => CssNode} TailwindUtilityClass - Parses a Tailwind utility class.
 * @property {() => Identifier} Identifier - Parses an identifier.
 *
 * @typedef {CssNodeCommon & { name: Identifier, variant: Identifier | null }} TailwindUtilityClassNode
 *
 * @typedef {ParserContext & TailwindParserContextApplyExtensions} TailwindParserApplyContext
 */
/**
 * Name of the Tailwind utility class node.
 * @type {string}
 */
export const name: string;
/**
 * Structure of the Tailwind theme key node.
 * @type {NodeSyntaxConfig["structure"]}
 */
export const structure: NodeSyntaxConfig["structure"];
export type TailwindParserContextApplyExtensions = {
    /**
     * - Parses the key of the theme function.
     */
    TailwindThemeKey: (recognizer: Recognizer) => CssNode;
    /**
     * - Parses a Tailwind utility class.
     */
    TailwindUtilityClass: () => CssNode;
    /**
     * - Parses an identifier.
     */
    Identifier: () => Identifier;
};
export type TailwindUtilityClassNode = CssNodeCommon & {
    name: Identifier;
    variant: Identifier | null;
};
export type TailwindParserApplyContext = ParserContext & TailwindParserContextApplyExtensions;
import type { ParserContext } from "@eslint/css-tree";
import type { NodeSyntaxConfig } from "@eslint/css-tree";
import type { Recognizer } from "@eslint/css-tree";
import type { CssNode } from "@eslint/css-tree";
import type { Identifier } from "@eslint/css-tree";
import type { CssNodeCommon } from "@eslint/css-tree";
