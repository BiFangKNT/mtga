import { R as ResolvableHead, q as CreateServerHeadOptions, U as Unhead, v as RenderSSRHeadOptions, au as HeadTag } from './shared/unhead.DKj0fe9v.mjs';
export { u as SSRHeadPayload } from './shared/unhead.DKj0fe9v.mjs';
import { PreparedHtmlTemplate } from './parser.mjs';
import 'hookable';

declare function createHead<T = ResolvableHead>(options?: CreateServerHeadOptions): Unhead<T>;

declare function renderSSRHead(head: Unhead<any>, options?: RenderSSRHeadOptions): Promise<{
    headTags: string;
    bodyTags: string;
    bodyTagsOpen: string;
    htmlAttrs: string;
    bodyAttrs: string;
}>;

/**
 * Transform an HTML template string by extracting any head tags and attributes from it, pushing them to Unhead,
 * and injecting the resulting head tags back into the HTML.
 * Uses optimized parsing and index-based HTML construction for best performance.
 */
declare function transformHtmlTemplate(head: Unhead<any>, html: string, options?: RenderSSRHeadOptions): Promise<string>;
/**
 * Transform an HTML template string by injecting head tags managed by Unhead.
 *
 * The differs to `transformHtmlTemplate` in that it does not extract and push any head input from the HTML, resulting
 * in much more performant execution if you don't need that feature.
 *
 * However, this also means that any head tags or attributes already present in the HTML may be duplicated or
 * ordered incorrectly, so use with caution.
 */
declare function transformHtmlTemplateRaw(head: Unhead<any>, html: string, options?: RenderSSRHeadOptions): Promise<string>;

/**
 * @deprecated use `parseHtmlForUnheadExtraction` from `unhead/parser` instead
 * @param html
 */
declare function extractUnheadInputFromHtml(html: string): PreparedHtmlTemplate;

declare function propsToString(props: Record<string, any>): string;

declare function ssrRenderTags<T extends HeadTag>(tags: T[], options?: RenderSSRHeadOptions): {
    headTags: string;
    bodyTags: string;
    bodyTagsOpen: string;
    htmlAttrs: string;
    bodyAttrs: string;
};

declare function escapeHtml(str: string): string;
declare function tagToString<T extends HeadTag>(tag: T): string;

export { CreateServerHeadOptions, Unhead, createHead, escapeHtml, extractUnheadInputFromHtml, propsToString, renderSSRHead, ssrRenderTags, tagToString, transformHtmlTemplate, transformHtmlTemplateRaw };
