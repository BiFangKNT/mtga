import { a5 as RawInput, R as ResolvableHead, az as ResolvableValue, aA as ResolvableProperties, ag as LinkWithoutEvents, ab as DataKeys, K as SchemaAugmentations, Q as UnheadMeta, ai as ScriptWithoutEvents, O as UnheadHtmlAttributes, N as UnheadBodyAttributesWithoutEvents } from './unhead.DKj0fe9v.js';

type Base = RawInput<'base'>;
type HtmlAttributes = RawInput<'htmlAttrs'>;
type Noscript = RawInput<'noscript'>;
type Style = RawInput<'style'>;
type Meta = RawInput<'meta'>;
type Script = RawInput<'script'>;
type Link = RawInput<'link'>;
type BodyAttributes = RawInput<'bodyAttrs'>;

type SafeBodyAttr = ResolvableProperties<Pick<UnheadBodyAttributesWithoutEvents, 'id' | 'class' | 'style'> & DataKeys & SchemaAugmentations['bodyAttrs']>;
type SafeHtmlAttr = ResolvableProperties<Pick<UnheadHtmlAttributes, 'id' | 'class' | 'style' | 'lang' | 'dir'> & DataKeys & SchemaAugmentations['htmlAttrs']>;
type SafeMeta = ResolvableProperties<Pick<UnheadMeta, 'id' | 'name' | 'property' | 'charset' | 'content' | 'media'> & DataKeys & SchemaAugmentations['meta']>;
type SafeLink = ResolvableProperties<Pick<LinkWithoutEvents, 'id' | 'color' | 'crossorigin' | 'fetchpriority' | 'href' | 'hreflang' | 'imagesrcset' | 'imagesizes' | 'integrity' | 'media' | 'referrerpolicy' | 'rel' | 'sizes' | 'type'> & DataKeys & SchemaAugmentations['link']>;
type SafeScript = ResolvableProperties<Pick<ScriptWithoutEvents, 'id' | 'type' | 'nonce' | 'blocking'> & DataKeys & SchemaAugmentations['script']>;
type SafeNoscript = ResolvableProperties<Pick<Noscript, 'id'> & DataKeys & Omit<SchemaAugmentations['noscript'], 'innerHTML'>>;
type SafeStyle = ResolvableProperties<Pick<Style, 'id' | 'media' | 'nonce' | 'title' | 'blocking'> & DataKeys & Omit<SchemaAugmentations['style'], 'innerHTML'>>;
interface HeadSafe extends Pick<ResolvableHead, 'title' | 'titleTemplate' | 'templateParams'> {
    /**
     * The `<link>` HTML element specifies relationships between the current document and an external resource.
     * This element is most commonly used to link to stylesheets, but is also used to establish site icons
     * (both "favicon" style icons and icons for the home screen and apps on mobile devices) among other things.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-as
     */
    link?: ResolvableValue<ResolvableValue<SafeLink[]>>;
    /**
     * The `<meta>` element represents metadata that cannot be expressed in other HTML elements, like `<link>` or `<script>`.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta
     */
    meta?: ResolvableValue<ResolvableValue<SafeMeta>[]>;
    /**
     * The `<style>` HTML element contains style information for a document, or part of a document.
     * It contains CSS, which is applied to the contents of the document containing the `<style>` element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style
     */
    style?: ResolvableValue<ResolvableValue<(SafeStyle | string)>[]>;
    /**
     * The `<script>` HTML element is used to embed executable code or data; this is typically used to embed or refer to JavaScript code.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script
     */
    script?: ResolvableValue<ResolvableValue<(SafeScript | string)>[]>;
    /**
     * The `<noscript>` HTML element defines a section of HTML to be inserted if a script type on the page is unsupported
     * or if scripting is currently turned off in the browser.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/noscript
     */
    noscript?: ResolvableValue<ResolvableValue<(SafeNoscript | string)>[]>;
    /**
     * Attributes for the `<html>` HTML element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/html
     */
    htmlAttrs?: ResolvableValue<SafeHtmlAttr>;
    /**
     * Attributes for the `<body>` HTML element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/body
     */
    bodyAttrs?: ResolvableValue<SafeBodyAttr>;
}

export type { Base as B, HeadSafe as H, Link as L, Meta as M, Noscript as N, SafeBodyAttr as S, SafeHtmlAttr as a, SafeMeta as b, SafeLink as c, SafeScript as d, SafeNoscript as e, SafeStyle as f, HtmlAttributes as g, Style as h, Script as i, BodyAttributes as j };
