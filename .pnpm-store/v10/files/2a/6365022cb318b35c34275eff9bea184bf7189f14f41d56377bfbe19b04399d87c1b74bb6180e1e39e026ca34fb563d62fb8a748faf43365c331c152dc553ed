import { n as HeadPluginInput, U as Unhead, m as HeadPluginOptions } from './shared/unhead.DKj0fe9v.mjs';
import 'hookable';

declare const AliasSortingPlugin: HeadPluginInput;

interface CanonicalPluginOptions {
    canonicalHost?: string;
    customResolver?: (url: string) => string;
}
/**
 * CanonicalPlugin resolves paths in tags that require a canonical host to be set.
 *
 *  - Resolves paths in meta tags like `og:image` and `twitter:image`.
 *  - Resolves paths in the `og:url` meta tag.
 *  - Resolves paths in the `link` tag with the `rel="canonical"` attribute.
 * @example
 * const plugin = CanonicalPlugin({
 *   canonicalHost: 'https://example.com',
 *   customResolver: (path) => `/custom${path}`,
 * });
 *
 * // This plugin will resolve URLs in meta tags like:
 * // <meta property="og:image" content="/image.jpg">
 * // to:
 * // <meta property="og:image" content="https://example.com/image.jpg">
 */
declare function CanonicalPlugin(options: CanonicalPluginOptions): ((head: Unhead) => HeadPluginOptions & {
    key: string;
});

declare function defineHeadPlugin(plugin: HeadPluginInput): HeadPluginInput;

declare const DeprecationsPlugin: HeadPluginInput;

declare const FlatMetaPlugin: HeadPluginInput;

interface InferSeoMetaPluginOptions {
    /**
     * Transform the og title.
     *
     * @param title
     */
    ogTitle?: ((title?: string) => string);
    /**
     * Transform the og description.
     *
     * @param description
     */
    ogDescription?: ((description?: string) => string);
    /**
     * The twitter card to use.
     *
     * @default 'summary_large_image'
     */
    twitterCard?: false | 'summary' | 'summary_large_image' | 'app' | 'player';
}
declare function InferSeoMetaPlugin(options?: InferSeoMetaPluginOptions): HeadPluginInput;

declare const PromisesPlugin: HeadPluginInput;

declare const SafeInputPlugin: HeadPluginInput;

declare const TemplateParamsPlugin: HeadPluginInput;

export { AliasSortingPlugin, CanonicalPlugin, DeprecationsPlugin, FlatMetaPlugin, InferSeoMetaPlugin, PromisesPlugin, SafeInputPlugin, TemplateParamsPlugin, defineHeadPlugin };
