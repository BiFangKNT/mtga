import { S as SerializableHead } from './shared/unhead.DKj0fe9v.js';
import 'hookable';

declare const TagIdMap: {
    readonly html: 0;
    readonly head: 1;
    readonly title: 4;
    readonly meta: 5;
    readonly body: 44;
    readonly script: 52;
    readonly style: 53;
    readonly link: 54;
    readonly base: 56;
};
interface PreparedHtmlTemplate {
    html: string;
    input: SerializableHead;
}
interface PreparedHtmlTemplateWithIndexes {
    html: string;
    input: SerializableHead;
    indexes: {
        htmlTagStart: number;
        htmlTagEnd: number;
        headTagEnd: number;
        bodyTagStart: number;
        bodyTagEnd: number;
        bodyCloseTagStart: number;
    };
}
/**
 * Parse HTML attributes string into key-value object
 */
declare function parseAttributes(attrStr: string): Record<string, string>;
/**
 * Parse HTML to find tag indexes without extracting head elements
 * Used for transformHtmlTemplateRaw where we don't want to extract existing head content
 */
declare function parseHtmlForIndexes(html: string): PreparedHtmlTemplateWithIndexes;
declare function parseHtmlForUnheadExtraction(html: string): PreparedHtmlTemplateWithIndexes;
/**
 * Optimized HTML construction function that uses indexes instead of string.replace()
 * This avoids searching through the entire HTML
 */
declare function applyHeadToHtml(template: PreparedHtmlTemplateWithIndexes, headHtml: {
    htmlAttrs: string;
    headTags: string;
    bodyAttrs: string;
    bodyTagsOpen?: string;
    bodyTags: string;
}): string;

export { TagIdMap, applyHeadToHtml, parseAttributes, parseHtmlForIndexes, parseHtmlForUnheadExtraction };
export type { PreparedHtmlTemplate, PreparedHtmlTemplateWithIndexes };
