import { NestedHooks, Hookable } from 'hookable';

type UseScriptStatus = 'awaitingLoad' | 'loading' | 'loaded' | 'error' | 'removed';
type UseScriptContext<T extends Record<symbol | string, any>> = ScriptInstance<T>;
/**
 * Either a string source for the script or full script properties.
 */
type UseScriptResolvedInput = Omit<ScriptWithoutEvents, 'src'> & {
    src: string;
} & DataKeys & MaybeEventFnHandlers<HttpEventAttributes> & SchemaAugmentations['script'];
type BaseScriptApi = Record<symbol | string, any>;
type HasDiscriminatedParameters<T> = T extends {
    (first: infer A, ...rest1: any[]): any;
    (first: infer B, ...rest2: any[]): any;
} ? A extends B ? B extends A ? false : true : true : false;
type HasDifferentParameterCounts<T> = T extends {
    (...args: infer A): any;
} & {
    (...args: infer B): any;
} ? A['length'] extends B['length'] ? B['length'] extends A['length'] ? false : true : true : false;
type IsOverloadedFunction<T> = HasDiscriminatedParameters<T> extends true ? true : HasDifferentParameterCounts<T> extends true ? true : false;
type AsVoidFunctions<T extends BaseScriptApi> = {
    [K in keyof T]: T[K] extends any[] ? T[K] : T[K] extends (...args: infer A) => any ? IsOverloadedFunction<T[K]> extends true ? T[K] : (...args: A) => void : T[K] extends Record<any, any> ? AsVoidFunctions<T[K]> : never;
};
type UseScriptInput = string | UseScriptResolvedInput;
type UseFunctionType<T, U> = T extends {
    use: infer V;
} ? V extends (...args: any) => any ? ReturnType<V> : U : U;
type WarmupStrategy = false | 'preload' | 'preconnect' | 'dns-prefetch';
interface ScriptInstance<T extends BaseScriptApi> {
    proxy: AsVoidFunctions<T>;
    instance?: T;
    id: string;
    status: Readonly<UseScriptStatus>;
    entry?: ActiveHeadEntry<any>;
    load: () => Promise<T>;
    warmup: (rel: WarmupStrategy) => ActiveHeadEntry<any>;
    remove: () => boolean;
    setupTriggerHandler: (trigger: UseScriptOptions['trigger']) => void;
    onLoaded: (fn: (instance: T) => void | Promise<void>, options?: EventHandlerOptions) => void;
    onError: (fn: (err?: Error) => void | Promise<void>, options?: EventHandlerOptions) => void;
    /**
     * @internal
     */
    _loadPromise: Promise<T | false>;
    /**
     * @internal
     */
    _warmupEl: any;
    /**
     * @internal
     */
    _triggerAbortController?: AbortController | null;
    /**
     * @internal
     */
    _triggerAbortControllers?: Set<AbortController>;
    /**
     * @internal
     */
    _triggerPromises?: Promise<void>[];
    /**
     * @internal
     */
    _cbs: {
        loaded: null | ((instance: T) => void | Promise<void>)[];
        error: null | ((err?: Error) => void | Promise<void>)[];
    };
}
interface EventHandlerOptions {
    /**
     * Used to dedupe the event, allowing you to have an event run only a single time.
     */
    key?: string;
}
type RecordingEntry = {
    type: 'get';
    key: string | symbol;
    args?: any[];
    value?: any;
} | {
    type: 'apply';
    key: string | symbol;
    args: any[];
};
interface UseScriptOptions<T extends BaseScriptApi = Record<string, any>> extends HeadEntryOptions {
    /**
     * Resolve the script instance from the window.
     */
    use?: () => T | undefined | null;
    /**
     * The trigger to load the script:
     * - `undefined` | `client` - (Default) Load the script on the client when this js is loaded.
     * - `manual` - Load the script manually by calling `$script.load()`, exists only on the client.
     * - `Promise` - Load the script when the promise resolves, exists only on the client.
     * - `Function` - Register a callback function to load the script, exists only on the client.
     * - `server` - Have the script injected on the server.
     */
    trigger?: 'client' | 'server' | 'manual' | Promise<boolean | void> | ((fn: any) => any) | null;
    /**
     * Add a preload or preconnect link tag before the script is loaded.
     */
    warmupStrategy?: WarmupStrategy;
    /**
     * Context to run events with. This is useful in Vue to attach the current instance context before
     * calling the event, allowing the event to be reactive.
     */
    eventContext?: any;
    /**
     * Called before the script is initialized. Will not be triggered when the script is already loaded. This means
     * this is guaranteed to be called only once, unless the script is removed and re-added.
     */
    beforeInit?: () => void;
}
type UseScriptReturn<T extends Record<symbol | string, any>> = UseScriptContext<UseFunctionType<UseScriptOptions<T>, T>>;

type Booleanable = boolean | 'false' | 'true' | '';
type Stringable = string | Booleanable | number;
type Arrayable<T> = T | Array<T>;
type Never<T> = {
    [P in keyof T]?: never;
};
type Falsy = false | null | undefined;
type ResolvableValue<T> = T | Falsy | (() => (T | Falsy));
type ResolvableProperties<T> = {
    [key in keyof T]?: ResolvableValue<T[key]>;
};
type ResolvableUnion<T> = T extends string | number | boolean ? ResolvableValue<T> : T extends object ? DeepResolvableProperties<T> : ResolvableValue<T>;
type DeepResolvableProperties<T> = {
    [K in keyof T]?: T[K] extends string | object ? T[K] extends string ? ResolvableUnion<T[K]> : T[K] extends object ? DeepResolvableProperties<T[K]> : ResolvableUnion<T[K]> : ResolvableUnion<T[K]>;
};

interface DataKeys {
    [key: `data-${string}`]: Stringable;
}

interface HttpEventAttributes {
    /**
     * Script to be run on abort
     */
    onabort?: string;
    /**
     * Script to be run when an error occurs when the file is being loaded
     */
    onerror?: string;
    /**
     * Script to be run when the file is loaded
     */
    onload?: string;
    /**
     * The progress event is fired periodically when a request receives more data.
     */
    onprogress?: string;
    /**
     * Script to be run just as the file begins to load before anything is actually loaded
     */
    onloadstart?: string;
}

interface Base {
    /**
     * The base URL to be used throughout the document for relative URLs. Absolute and relative URLs are allowed.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/base#attr-href
     */
    href?: string;
    /**
     * A keyword or author-defined name of the default browsing context to show the results of navigation from `<a>`,
     * `<area>`, or `<form>` elements without explicit target attributes.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/base#attr-target
     */
    target?: string;
}

interface GlobalAttributes {
    /**
     * Provides a hint for generating a keyboard shortcut for the current element. This attribute consists of a
     * space-separated list of characters. The browser should use the first one that exists on the computer keyboard layout.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/accesskey
     */
    accesskey?: string;
    /**
     * Controls whether and how text input is automatically capitalized as it is entered/edited by the user.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/autocapitalize
     */
    autocapitalize?: 'off' | 'none' | 'on' | 'sentences' | 'words' | 'characters';
    /**
     * Indicates that an element is to be focused on page load, or as soon as the `<dialog>` it is part of is displayed.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/autofocus
     */
    autofocus?: Booleanable;
    /**
     * A space-separated list of the classes of the element. Classes allows CSS and JavaScript to select and access
     * specific elements via the class selectors or functions like the method Document.getElementsByClassName().
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/class
     */
    class?: Stringable;
    /**
     * An enumerated attribute indicating if the element should be editable by the user.
     * If so, the browser modifies its widget to allow editing.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/contenteditable
     */
    contenteditable?: Booleanable;
    /**
     * An enumerated attribute indicating the directionality of the element's text.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/dir
     */
    dir?: 'ltr' | 'rtl' | 'auto';
    /**
     * An enumerated attribute indicating whether the element can be dragged, using the Drag and Drop API.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/draggable
     */
    draggable?: Booleanable;
    /**
     * Hints what action label (or icon) to present for the enter key on virtual keyboards.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/enterkeyhint
     */
    enterkeyhint?: string;
    /**
     * Used to transitively export shadow parts from a nested shadow tree into a containing light tree.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/exportparts
     */
    exportparts?: string;
    /**
     * A Boolean attribute indicates that the element is not yet, or is no longer, relevant.
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/hidden
     */
    hidden?: Booleanable;
    /**
     * The id global attribute defines a unique identifier (ID) which must be unique in the whole document.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/id
     */
    id?: string;
    /**
     * Provides a hint to browsers as to the type of virtual keyboard configuration to use when editing this element or its contents.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/inputmode
     */
    inputmode?: string;
    /**
     * Allows you to specify that a standard HTML element should behave like a registered custom built-in element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/is
     */
    is?: string;
    /**
     * The unique, global identifier of an item.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/itemid
     */
    itemid?: string;
    /**
     * Used to add properties to an item.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/itemprop
     */
    itemprop?: string;
    /**
     * Properties that are not descendants of an element with the itemscope attribute can be associated with the item using an itemref.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/itemref
     */
    itemref?: string;
    /**
     * itemscope (usually) works along with itemtype to specify that the HTML contained in a block is about a particular item.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/itemscope
     */
    itemscope?: string;
    /**
     * Specifies the URL of the vocabulary that will be used to define itemprops (item properties) in the data structure.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/itemtype
     */
    itemtype?: string;
    /**
     * Helps define the language of an element: the language that non-editable elements are in, or the language
     * that editable elements should be written in by the user.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/lang
     */
    lang?: string;
    /**
     * A cryptographic nonce ("number used once") which can be used by Content Security Policy to determine whether or not
     * a given fetch will be allowed to proceed.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/nonce
     */
    nonce?: string;
    /**
     * A space-separated list of the part names of the element. Part names allows CSS to select and style specific elements
     * in a shadow tree via the ::part pseudo-element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/part
     */
    part?: string;
    /**
     * Assigns a slot in a shadow DOM shadow tree to an element: An element with a slot attribute is assigned to the slot
     * created by the `<slot>` element whose name attribute's value matches that slot attribute's value.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/slot
     */
    slot?: string;
    /**
     * An enumerated attribute defines whether the element may be checked for spelling errors.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/spellcheck
     */
    spellcheck?: Booleanable;
    /**
     * Contains CSS styling declarations to be applied to the element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/style
     */
    style?: string;
    /**
     * An integer attribute indicating if the element can take input focus (is focusable),
     * if it should participate to sequential keyboard navigation, and if so, at what position.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/tabindex
     */
    tabindex?: number;
    /**
     * Contains a text representing advisory information related to the element it belongs to.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/title
     */
    title?: string;
    /**
     * An enumerated attribute that is used to specify whether an element's attribute values and the values of its
     * Text node children are to be translated when the page is localized, or whether to leave them unchanged.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/translate
     */
    translate?: 'yes' | 'no' | '';
}

interface BodyEvents {
    /**
     * Script to be run after the document is printed
     */
    onafterprint?: string;
    /**
     * Script to be run before the document is printed
     */
    onbeforeprint?: string;
    /**
     * Script to be run when the document is about to be unloaded
     */
    onbeforeunload?: string;
    /**
     * Script to be run when an error occurs
     */
    onerror?: string;
    /**
     * Script to be run when there has been changes to the anchor part of the a URL
     */
    onhashchange?: string;
    /**
     * Fires after the page is finished loading
     */
    onload?: string;
    /**
     * Script to be run when the message is triggered
     */
    onmessage?: string;
    /**
     * Script to be run when the browser starts to work offline
     */
    onoffline?: string;
    /**
     * Script to be run when the browser starts to work online
     */
    ononline?: string;
    /**
     * Script to be run when a user navigates away from a page
     */
    onpagehide?: string;
    /**
     * Script to be run when a user navigates to a page
     */
    onpageshow?: string;
    /**
     * Script to be run when the window's history changes
     */
    onpopstate?: string;
    /**
     * Fires when the browser window is resized
     */
    onresize?: string;
    /**
     * Script to be run when a Web Storage area is updated
     */
    onstorage?: string;
    /**
     * Fires once a page has unloaded (or the browser window has been closed)
     */
    onunload?: string;
}
interface BodyAttributesWithoutEvents extends Pick<GlobalAttributes, 'class' | 'style' | 'id'> {
}

interface HtmlAttributes extends Pick<GlobalAttributes, 'lang' | 'dir' | 'translate' | 'class' | 'style' | 'id'> {
    /**
     * Open-graph protocol prefix.
     *
     * @see https://ogp.me/
     */
    prefix?: 'og: https://ogp.me/ns#' | (string & Record<never, never>);
    /**
     * XML namespace
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/SVG/Namespaces_Crash_Course
     */
    xmlns?: string;
    /**
     * Custom XML namespace
     *
     * @See https://developer.mozilla.org/en-US/docs/Web/SVG/Namespaces_Crash_Course
     */
    [key: `xmlns:${'og' | string}`]: string;
}

type ReferrerPolicy = '' | 'no-referrer' | 'no-referrer-when-downgrade' | 'origin' | 'origin-when-cross-origin' | 'same-origin' | 'strict-origin' | 'strict-origin-when-cross-origin' | 'unsafe-url';

/**
 * Represents the possible blocking tokens for an element.
 */
type BlockingToken = 'render';
/**
 * Represents the blocking attribute for an element.
 * The blocking attribute must have a value that is an unordered set of unique space-separated tokens,
 * each of which are possible blocking tokens.
 */
interface Blocking {
    /**
     * The blocking attribute indicates that certain operations should be blocked on the fetching of an external resource.
     * The value is an unordered set of unique space-separated tokens, each of which are possible blocking tokens.
     *
     * @example
     * blocking: "render"
     */
    blocking?: BlockingToken | string;
}

type LinkRelTypes = 'alternate' | 'author' | 'shortcut icon' | 'bookmark' | 'canonical' | 'dns-prefetch' | 'external' | 'help' | 'icon' | 'license' | 'manifest' | 'me' | 'modulepreload' | 'next' | 'nofollow' | 'noopener' | 'noreferrer' | 'opener' | 'pingback' | 'preconnect' | 'prefetch' | 'preload' | 'prerender' | 'prev' | 'search' | 'shortlink' | 'stylesheet' | 'tag' | 'apple-touch-icon' | 'apple-touch-startup-image';
interface LinkWithoutEvents extends Pick<GlobalAttributes, 'nonce' | 'id'>, Blocking {
    /**
     * This attribute is only used when rel="preload" or rel="prefetch" has been set on the `<link>` element.
     * It specifies the type of content being loaded by the `<link>`, which is necessary for request matching,
     * application of correct content security policy, and setting of correct Accept request header.
     * Furthermore, rel="preload" uses this as a signal for request prioritization.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-as
     */
    as?: 'audio' | 'document' | 'embed' | 'fetch' | 'font' | 'image' | 'object' | 'script' | 'style' | 'track' | 'video' | 'worker';
    /**
     * The color attribute is used with the mask-icon link type.
     * The attribute must only be specified on link elements that have a rel attribute
     * that contains the mask-icon keyword.
     * The value must be a string that matches the CSS `<color>` production,
     * defining a suggested color that user agents can use to customize the display
     * of the icon that the user sees when they pin your site.
     *
     * @see https://html.spec.whatwg.org/multipage/semantics.html#attr-link-color
     */
    color?: string;
    /**
     * This enumerated attribute indicates whether CORS must be used when fetching the resource.
     * CORS-enabled images can be reused in the `<canvas>` element without being tainted.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-crossorigin
     */
    crossorigin?: '' | 'anonymous' | 'use-credentials';
    /**
     * Provides a hint of the relative priority to use when fetching a preloaded resource.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-fetchpriority
     */
    fetchpriority?: 'high' | 'low' | 'auto';
    /**
     * This attribute specifies the URL of the linked resource. A URL can be absolute or relative.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-href
     */
    href?: string;
    /**
     * This attribute indicates the language of the linked resource. It is purely advisory.
     * Allowed values are specified by RFC 5646: Tags for Identifying Languages (also known as BCP 47).
     * Use this attribute only if the href attribute is present.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-hreflang
     */
    hreflang?: string;
    /**
     * For rel="preload" and as="image" only, the imagesizes attribute is a sizes attribute that indicates to preload
     * the appropriate resource used by an img element with corresponding values for its srcset and sizes attributes.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-imagesizes
     */
    imagesizes?: string;
    /**
     * For rel="preload" and as="image" only, the imagesrcset attribute is a sourceset attribute that indicates
     * to preload the appropriate resource used by an img element with corresponding values for its srcset and
     * sizes attributes.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-imagesrcset
     */
    imagesrcset?: string;
    /**
     * Contains inline metadata — a base64-encoded cryptographic hash of the resource (file)
     * you're telling the browser to fetch.
     * The browser can use this to verify that the fetched resource has been delivered free of unexpected manipulation.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-integrity
     */
    integrity?: string;
    /**
     * This attribute specifies the media that the linked resource applies to.
     * Its value must be a media type / media query.
     * This attribute is mainly useful when linking to external stylesheets —
     * it allows the user agent to pick the best adapted one for the device it runs on.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-integrity
     */
    media?: string;
    /**
     * Identifies a resource that might be required by the next navigation and that the user agent should retrieve it.
     * This allows the user agent to respond faster when the resource is requested in the future.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-prefetch
     */
    prefetch?: string;
    /**
     * A string indicating which referrer to use when fetching the resource.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-referrerpolicy
     */
    referrerpolicy?: ReferrerPolicy;
    /**
     * This attribute names a relationship of the linked document to the current document.
     * The attribute must be a space-separated list of link type values.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-rel
     */
    rel?: LinkRelTypes | (string & Record<never, never>);
    /**
     * This attribute defines the sizes of the icons for visual media contained in the resource.
     * It must be present only if the rel contains a value of icon or a non-standard type
     * such as Apple's apple-touch-icon.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-sizes
     */
    sizes?: 'any' | '16x16' | '32x32' | '64x64' | '180x180' | (string & Record<never, never>);
    /**
     * The title attribute has special semantics on the `<link>` element.
     * When used on a `<link rel="stylesheet">` it defines a default or an alternate stylesheet.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-title
     */
    title?: string;
    /**
     * This attribute is used to define the type of the content linked to.
     * The value of the attribute should be a MIME type such as text/html, text/css, and so on.
     * The common use of this attribute is to define the type of stylesheet being referenced (such as text/css),
     * but given that CSS is the only stylesheet language used on the web,
     * not only is it possible to omit the type attribute, but is actually now recommended practice.
     * It is also used on rel="preload" link types, to make sure the browser only downloads file types that it supports.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-type
     */
    type?: 'audio/aac' | 'application/x-abiword' | 'application/x-freearc' | 'image/avif' | 'video/x-msvideo' | 'application/vnd.amazon.ebook' | 'application/octet-stream' | 'image/bmp' | 'application/x-bzip' | 'application/x-bzip2' | 'application/x-cdf' | 'application/x-csh' | 'text/css' | 'text/csv' | 'application/msword' | 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' | 'application/vnd.ms-fontobject' | 'application/epub+zip' | 'application/gzip' | 'image/gif' | 'text/html' | 'image/vnd.microsoft.icon' | 'text/calendar' | 'application/java-archive' | 'image/jpeg' | 'text/javascript' | 'application/json' | 'application/ld+json' | 'audio/midi' | 'audio/x-midi' | 'audio/mpeg' | 'video/mp4' | 'video/mpeg' | 'application/vnd.apple.installer+xml' | 'application/vnd.oasis.opendocument.presentation' | 'application/vnd.oasis.opendocument.spreadsheet' | 'application/vnd.oasis.opendocument.text' | 'audio/ogg' | 'video/ogg' | 'application/ogg' | 'audio/opus' | 'font/otf' | 'image/png' | 'application/pdf' | 'application/x-httpd-php' | 'application/vnd.ms-powerpoint' | 'application/vnd.openxmlformats-officedocument.presentationml.presentation' | 'application/vnd.rar' | 'application/rtf' | 'application/x-sh' | 'image/svg+xml' | 'application/x-tar' | 'image/tiff' | 'video/mp2t' | 'font/ttf' | 'text/plain' | 'application/vnd.visio' | 'audio/wav' | 'audio/webm' | 'video/webm' | 'image/webp' | 'font/woff' | 'font/woff2' | 'application/xhtml+xml' | 'application/vnd.ms-excel' | 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' | 'text/xml' | 'application/atom+xml' | 'application/xml' | 'application/vnd.mozilla.xul+xml' | 'application/zip' | 'video/3gpp' | 'audio/3gpp' | 'video/3gpp2' | 'audio/3gpp2' | (string & Record<never, never>);
}

type MetaNames = 'apple-itunes-app' | 'apple-mobile-web-app-capable' | 'apple-mobile-web-app-status-bar-style' | 'apple-mobile-web-app-title' | 'application-name' | 'author' | 'charset' | 'color-scheme' | 'content-security-policy' | 'content-type' | 'creator' | 'default-style' | 'description' | 'fb:app_id' | 'format-detection' | 'generator' | 'google-site-verification' | 'google' | 'googlebot' | 'keywords' | 'mobile-web-app-capable' | 'msapplication-Config' | 'msapplication-TileColor' | 'msapplication-TileImage' | 'publisher' | 'rating' | 'referrer' | 'refresh' | 'robots' | 'theme-color' | 'twitter:app:id:googleplay' | 'twitter:app:id:ipad' | 'twitter:app:id:iphone' | 'twitter:app:name:googleplay' | 'twitter:app:name:ipad' | 'twitter:app:name:iphone' | 'twitter:app:url:googleplay' | 'twitter:app:url:ipad' | 'twitter:app:url:iphone' | 'twitter:card' | 'twitter:creator:id' | 'twitter:creator' | 'twitter:data:1' | 'twitter:data:2' | 'twitter:description' | 'twitter:image:alt' | 'twitter:image' | 'twitter:label:1' | 'twitter:label:2' | 'twitter:player:height' | 'twitter:player:stream' | 'twitter:player:width' | 'twitter:player' | 'twitter:site:id' | 'twitter:site' | 'twitter:title' | 'viewport' | 'x-ua-compatible';
type MetaProperties = 'article:author' | 'article:expiration_time' | 'article:modified_time' | 'article:published_time' | 'article:section' | 'article:tag' | 'book:author' | 'book:isbn' | 'book:release_data' | 'book:tag' | 'fb:app:id' | 'og:audio:secure_url' | 'og:audio:type' | 'og:audio:url' | 'og:description' | 'og:determiner' | 'og:image:height' | 'og:image:secure_url' | 'og:image:type' | 'og:image:url' | 'og:image:width' | 'og:image' | 'og:locale:alternate' | 'og:locale' | 'og:site:name' | 'og:title' | 'og:type' | 'og:url' | 'og:video:height' | 'og:video:secure_url' | 'og:video:type' | 'og:video:url' | 'og:video:width' | 'og:video' | 'profile:first_name' | 'profile:gender' | 'profile:last_name' | 'profile:username';
interface Meta extends Pick<GlobalAttributes, 'id'> {
    /**
     * This attribute declares the document's character encoding.
     * If the attribute is present, its value must be an ASCII case-insensitive match for the string "utf-8",
     * because UTF-8 is the only valid encoding for HTML5 documents.
     * `<meta>` elements which declare a character encoding must be located entirely within the first 1024 bytes
     * of the document.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta#attr-charset
     */
    charset?: 'utf-8' | (string & Record<never, never>);
    /**
     * This attribute contains the value for the http-equiv or name attribute, depending on which is used.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta#attr-content
     */
    content?: Stringable;
    /**
     * Defines a pragma directive. The attribute is named http-equiv(alent) because all the allowed values are names of
     * particular HTTP headers.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta#attr-http-equiv
     */
    ['http-equiv']?: 'content-security-policy' | 'content-type' | 'default-style' | 'x-ua-compatible' | 'refresh' | 'accept-ch' | (string & Record<never, never>);
    /**
     * The name and content attributes can be used together to provide document metadata in terms of name-value pairs,
     * with the name attribute giving the metadata name, and the content attribute giving the value.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta#attr-name
     */
    name?: MetaNames | (string & Record<never, never>);
    /**
     * The property attribute is used to define a property associated with the content attribute.
     *
     * Mainly used for og and twitter meta tags.
     */
    property?: MetaProperties | (string & Record<never, never>);
    /**
     * A valid media query list that can be included to set the media the `theme-color` metadata applies to.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name/theme-color
     */
    media?: '(prefers-color-scheme: light)' | '(prefers-color-scheme: dark)' | (string & Record<never, never>);
}

interface MetaFlatArticle {
    /**
     * Writers of the article.
     * @example ['https://example.com/some.html', 'https://example.com/one.html']
     */
    articleAuthor?: string[];
    /**
     * When the article is out of date after.
     * @example '1970-01-01T00:00:00.000Z'
     */
    articleExpirationTime?: string;
    /**
     * When the article was last changed.
     * @example '1970-01-01T00:00:00.000Z'
     */
    articleModifiedTime?: string;
    /**
     * When the article was first published.
     * @example '1970-01-01T00:00:00.000Z'
     */
    articlePublishedTime?: string;
    /**
     * A high-level section name.
     * @example 'Technology'
     */
    articleSection?: string;
    /**
     * Tag words associated with this article.
     * @example ['Apple', 'Steve Jobs']
     */
    articleTag?: string[];
}
interface MetaFlatBook {
    /**
     * Who wrote this book.
     * @example ['https://example.com/some.html', 'https://example.com/one.html']
     */
    bookAuthor?: string[];
    /**
     * The ISBN.
     * @example '978-3-16-148410-0'
     */
    bookIsbn?: string;
    /**
     * The date the book was released.
     * @example '1970-01-01T00:00:00.000Z'
     */
    bookReleaseDate?: string;
    /**
     * Tag words associated with this book.
     * @example ['Apple', 'Steve Jobs']
     */
    bookTag?: string[];
}
interface MetaFlatProfile {
    /**
     * A name normally given to an individual by a parent or self-chosen.
     */
    profileFirstName?: string;
    /**
     * Their gender.
     */
    profileGender?: 'male' | 'female' | string;
    /**
     * A name inherited from a family or marriage and by which the individual is commonly known.
     */
    profileLastName?: string;
    /**
     * A short unique string to identify them.
     */
    profileUsername?: string;
}
interface MetaFlat extends MetaFlatArticle, MetaFlatBook, MetaFlatProfile {
    /**
     * This attribute declares the document's character encoding.
     * If the attribute is present, its value must be an ASCII case-insensitive match for the string "utf-8",
     * because UTF-8 is the only valid encoding for HTML5 documents.
     * `<meta>` elements which declare a character encoding must be located entirely within the first 1024 bytes
     * of the document.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta#attr-charset
     */
    charset?: 'utf-8' | (string & Record<never, never>);
    /**
     * Use this tag to provide a short description of the page.
     * In some situations, this description is used in the snippet shown in search results.
     *
     * @see https://developers.google.com/search/docs/advanced/appearance/snippet#meta-descriptions
     */
    description?: string;
    /**
     * Specifies one or more color schemes with which the document is compatible.
     * The browser will use this information in tandem with the user's browser or device settings to determine what colors
     * to use for everything from background and foregrounds to form controls and scrollbars.
     * The primary use for `<meta name="color-scheme">` is to indicate compatibility with—and order of preference
     * for—light and dark color modes.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name#normal
     */
    colorScheme?: 'normal' | 'light dark' | 'dark light' | 'only light' | (string & Record<never, never>);
    /**
     * The name of the application running in the web page.
     *
     * Uses:
     * - When adding the page to the home screen.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name
     */
    applicationName?: string;
    /**
     * The name of the document's author.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name
     */
    author?: string;
    /**
     * The name of the creator of the document, such as an organization or institution.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name#other_metadata_names
     */
    creator?: string;
    /**
     * The name of the document's publisher.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name#other_metadata_names
     */
    publisher?: string;
    /**
     * The identifier of the software that generated the page.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name#standard_metadata_names_defined_in_the_html_specification
     */
    generator?: string;
    /**
     * Controls the HTTP Referer header of requests sent from the document.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name#standard_metadata_names_defined_in_the_html_specification
     */
    referrer?: ReferrerPolicy;
    /**
     * This tag tells the browser how to render a page on a mobile device.
     * Presence of this tag indicates to Google that the page is mobile friendly.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name#standard_metadata_names_defined_in_other_specifications
     */
    viewport?: 'width=device-width, initial-scale=1.0' | string | Partial<{
        /**
         * Defines the pixel width of the viewport that you want the web site to be rendered at.
         */
        width?: number | string | 'device-width';
        /**
         * Defines the height of the viewport. Not used by any browser.
         */
        height?: number | string | 'device-height';
        /**
         * Defines the ratio between the device width
         * (device-width in portrait mode or device-height in landscape mode) and the viewport size.
         *
         * @minimum 0
         * @maximum 10
         */
        initialScale?: '1.0' | number | (string & Record<never, never>);
        /**
         * Defines the maximum amount to zoom in.
         * It must be greater or equal to the minimum-scale or the behavior is undefined.
         * Browser settings can ignore this rule and iOS10+ ignores it by default.
         *
         * @minimum 0
         * @maximum 10
         */
        maximumScale?: number | string;
        /**
         * Defines the minimum zoom level. It must be smaller or equal to the maximum-scale or the behavior is undefined.
         * Browser settings can ignore this rule and iOS10+ ignores it by default.
         *
         * @minimum 0
         * @maximum 10
         */
        minimumScale?: number | string;
        /**
         * If set to no, the user is unable to zoom in the webpage.
         * The default is yes. Browser settings can ignore this rule, and iOS10+ ignores it by default.
         */
        userScalable?: 'yes' | 'no';
        /**
         * The auto value doesn't affect the initial layout viewport, and the whole web page is viewable.
         *
         * The contain value means that the viewport is scaled to fit the largest rectangle inscribed within the display.
         *
         * The cover value means that the viewport is scaled to fill the device display.
         * It is highly recommended to make use of the safe area inset variables to ensure that important content
         * doesn't end up outside the display.
         */
        viewportFit?: 'auto' | 'contain' | 'cover';
    }>;
    /**
     * Control the behavior of search engine crawling and indexing.
     *
     * @see https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
     */
    robots?: 'noindex, nofollow' | 'index, follow' | string | Partial<{
        /**
         * Allow search engines to index this page.
         *
         * Note: This is not officially supported by Google but is used widely.
         */
        index?: Booleanable;
        /**
         * Allow search engines to follow links on this page.
         *
         * Note: This is not officially supported by Google but is used widely.
         */
        follow?: Booleanable;
        /**
         * There are no restrictions for indexing or serving.
         * This directive is the default value and has no effect if explicitly listed.
         */
        all?: Booleanable;
        /**
         * Do not show this page, media, or resource in search results.
         * If you don't specify this directive, the page, media, or resource may be indexed and shown in search results.
         */
        noindex?: Booleanable;
        /**
         * Do not follow the links on this page.
         * If you don't specify this directive, Google may use the links on the page to discover those linked pages.
         */
        nofollow?: Booleanable;
        /**
         * Equivalent to noindex, nofollow.
         */
        none?: Booleanable;
        /**
         * Do not show a cached link in search results.
         * If you don't specify this directive,
         * Google may generate a cached page and users may access it through the search results.
         */
        noarchive?: Booleanable;
        /**
         * Do not show a sitelinks search box in the search results for this page.
         * If you don't specify this directive, Google may generate a search box specific to your site in search results,
         * along with other direct links to your site.
         */
        nositelinkssearchbox?: Booleanable;
        /**
         *
         * Do not show a text snippet or video preview in the search results for this page.
         * A static image thumbnail (if available) may still be visible, when it results in a better user experience.
         */
        nosnippet?: Booleanable;
        /**
         * Google is allowed to index the content of a page if it's embedded in another
         * page through iframes or similar HTML tags, in spite of a noindex directive.
         *
         * indexifembedded only has an effect if it's accompanied by noindex.
         */
        indexifembedded?: Booleanable;
        /**
         * Use a maximum of [number] characters as a textual snippet for this search result.
         */
        maxSnippet?: number | string;
        /**
         * Set the maximum size of an image preview for this page in a search results.
         */
        maxImagePreview?: 'none' | 'standard' | 'large';
        /**
         * Use a maximum of [number] seconds as a video snippet for videos on this page in search results.
         */
        maxVideoPreview?: number | string;
        /**
         * Don't offer translation of this page in search results.
         */
        notranslate?: Booleanable;
        /**
         * Do not show this page in search results after the specified date/time.
         */
        unavailable_after?: string;
        /**
         * Do not index images on this page.
         */
        noimageindex?: Booleanable;
    }>;
    /**
     * Special meta tag for controlling Google's indexing behavior.
     *
     * @see https://developers.google.com/search/docs/crawling-indexing/special-tags
     */
    google?: 
    /**
     * When users search for your site, Google Search results sometimes display a search box specific to your site,
     * along with other direct links to your site. This tag tells Google not to show the sitelinks search box.
     */
    'nositelinkssearchbox'
    /**
     * Prevents various Google text-to-speech services from reading aloud web pages using text-to-speech (TTS).
     */
     | 'nopagereadaloud';
    /**
     * Control how Google indexing works specifically for the googlebot crawler.
     *
     * @see https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
     */
    googlebot?: 
    /**
     * When Google recognizes that the contents of a page aren't in the language that the user likely wants to read,
     * Google may provide a translated title link and snippet in search results.
     */
    'notranslate' | 'noimageindex' | 'noarchive' | 'nosnippet' | 'max-snippet' | 'max-image-preview' | 'max-video-preview';
    /**
     * Control how Google indexing works specifically for the googlebot-news crawler.
     *
     * @see https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag
     */
    googlebotNews?: 'noindex' | 'nosnippet' | 'notranslate' | 'noimageindex';
    /**
     * You can use this tag on the top-level page of your site to verify ownership for Search Console.
     *
     * @see https://developers.google.com/search/docs/crawling-indexing/special-tags
     */
    googleSiteVerification?: string;
    /**
     * Labels a page as containing adult content, to signal that it be filtered by SafeSearch results
     * .
     * @see https://developers.google.com/search/docs/advanced/guidelines/safesearch
     */
    rating?: 'adult';
    /**
     * The canonical URL for your page.
     *
     * This should be the undecorated URL, without session variables, user identifying parameters, or counters.
     * Likes and Shares for this URL will aggregate at this URL.
     *
     * For example?: mobile domain URLs should point to the desktop version of the URL as the canonical URL to aggregate
     * Likes and Shares across different versions of the page.
     *
     * @see https://ogp.me/#metadata
     */
    ogUrl?: string;
    /**
     * The title of your page without any branding such as your site name.
     *
     * @see https://ogp.me/#metadata
     */
    ogTitle?: string;
    /**
     * A brief description of the content, usually between 2 and 4 sentences.
     *
     * @see https://ogp.me/#optional
     */
    ogDescription?: string;
    /**
     * The type of media of your content. This tag impacts how your content shows up in Feed. If you don't specify a type,
     * the default is website.
     * Each URL should be a single object, so multiple og:type values are not possible.
     *
     * @see https://ogp.me/#metadata
     */
    ogType?: 'website' | 'article' | 'book' | 'profile' | 'music.song' | 'music.album' | 'music.playlist' | 'music.radio_status' | 'video.movie' | 'video.episode' | 'video.tv_show' | 'video.other';
    /**
     * The locale of the resource. Defaults to en_US.
     *
     * @see https://ogp.me/#optional
     */
    ogLocale?: string;
    /**
     * An array of other locales this page is available in.
     *
     * @see https://ogp.me/#optional
     */
    ogLocaleAlternate?: Arrayable<string>;
    /**
     * The word that appears before this object's title in a sentence.
     * An enum of (a, an, the, "", auto).
     * If auto is chosen, the consumer of your data should choose between "a" or "an".
     * Default is "" (blank).
     *
     * @see https://ogp.me/#optional
     */
    ogDeterminer?: 'a' | 'an' | 'the' | '' | 'auto';
    /**
     * If your object is part of a larger website, the name which should be displayed for the overall site. e.g., "IMDb".
     *
     * @see https://ogp.me/#optional
     */
    ogSiteName?: string;
    /**
     * The URL for the video. If you want the video to play in-line in Feed, you should use the https:// URL if possible.
     *
     * @see https://ogp.me/#type_video
     */
    ogVideo?: string | Arrayable<{
        /**
         * Equivalent to og:video
         */
        url?: string;
        /**
         *
         * Secure URL for the video. Include this even if you set the secure URL in og:video.
         */
        secureUrl?: string;
        /**
         * MIME type of the video.
         */
        type?: 'application/x-shockwave-flash' | 'video/mp4';
        /**
         * Width of video in pixels. This property is required for videos.
         */
        width?: string | number;
        /**
         * Height of video in pixels. This property is required for videos.
         */
        height?: string | number;
        /**
         * A text description of the video.
         */
        alt?: string;
    }>;
    /**
     * Equivalent to og:video
     *
     * @see https://ogp.me/#type_video
     */
    ogVideoUrl?: string;
    /**
     *
     * Secure URL for the video. Include this even if you set the secure URL in og:video.
     *
     * @see https://ogp.me/#type_video
     */
    ogVideoSecureUrl?: string;
    /**
     * MIME type of the video.
     *
     * @see https://ogp.me/#type_video
     */
    ogVideoType?: 'application/x-shockwave-flash' | 'video/mp4';
    /**
     * Width of video in pixels. This property is required for videos.
     *
     * @see https://ogp.me/#type_video
     */
    ogVideoWidth?: string | number;
    /**
     * Height of video in pixels. This property is required for videos.
     *
     * @see https://ogp.me/#type_video
     */
    ogVideoHeight?: string | number;
    /**
     * A text description of the video.
     *
     * @see https://ogp.me/#type_video
     */
    ogVideoAlt?: string;
    /**
     * The URL of the image that appears when someone shares the content.
     *
     * @see https://developers.facebook.com/docs/sharing/webmasters#images
     */
    ogImage?: string | Arrayable<{
        /**
         * Equivalent to og:image
         */
        url?: string;
        /**
         *
         * https:// URL for the image
         */
        secureUrl?: string;
        /**
         * MIME type of the image.
         */
        type?: 'image/jpeg' | 'image/gif' | 'image/png';
        /**
         * Width of image in pixels. Specify height and width for your image to ensure that the image loads properly the first time it's shared.
         */
        width?: '1200' | string | number;
        /**
         * Height of image in pixels. Specify height and width for your image to ensure that the image loads properly the first time it's shared.
         */
        height?: '630' | string | number;
        /**
         * A description of what is in the image (not a caption). If the page specifies an og:image, it should specify og:image:alt.
         */
        alt?: string;
    }>;
    /**
     * Equivalent to og:image
     *
     * @see https://developers.facebook.com/docs/sharing/webmasters#images
     */
    ogImageUrl?: string;
    /**
     *
     * https:// URL for the image
     *
     * @see https://developers.facebook.com/docs/sharing/webmasters#images
     */
    ogImageSecureUrl?: string;
    /**
     * MIME type of the image.
     *
     * @see https://developers.facebook.com/docs/sharing/webmasters#images
     */
    ogImageType?: 'image/jpeg' | 'image/gif' | 'image/png';
    /**
     * Width of image in pixels. Specify height and width for your image to ensure that the image loads properly the first time it's shared.
     *
     * @see https://developers.facebook.com/docs/sharing/webmasters#images
     */
    ogImageWidth?: '1200' | string | number;
    /**
     * Height of image in pixels. Specify height and width for your image to ensure that the image loads properly the first time it's shared.
     *
     * @see https://developers.facebook.com/docs/sharing/webmasters#images
     */
    ogImageHeight?: '630' | string | number;
    /**
     * A description of what is in the image (not a caption). If the page specifies an og:image, it should specify og:image:alt.
     *
     * @see https://developers.facebook.com/docs/sharing/webmasters#images
     */
    ogImageAlt?: string;
    /**
     * The URL for an audio file to accompany this object.
     *
     * @see https://ogp.me/#optional
     */
    ogAudio?: string | Arrayable<{
        /**
         * Equivalent to og:audio
         */
        url?: string;
        /**
         * Secure URL for the audio. Include this even if you set the secure URL in og:audio.
         */
        secureUrl?: string;
        /**
         * MIME type of the audio.
         */
        type?: 'audio/mpeg' | 'audio/ogg' | 'audio/wav';
    }>;
    /**
     * Equivalent to og:audio
     *
     * @see https://ogp.me/#optional
     */
    ogAudioUrl?: string;
    /**
     * Secure URL for the audio. Include this even if you set the secure URL in og:audio.
     *
     * @see https://ogp.me/#optional
     */
    ogAudioSecureUrl?: string;
    /**
     * MIME type of the audio.
     *
     * @see https://ogp.me/#optional
     */
    ogAudioType?: 'audio/mpeg' | 'audio/ogg' | 'audio/wav';
    /**
     * Your Facebook app ID.
     *
     * In order to use Facebook Insights you must add the app ID to your page.
     * Insights lets you view analytics for traffic to your site from Facebook. Find the app ID in your App Dashboard.
     *
     * @see https://developers.facebook.com/docs/sharing/webmasters#basic
     */
    fbAppId?: string | number;
    /**
     * The card type
     *
     * Used with all cards
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards
     */
    twitterCard?: 'summary' | 'summary_large_image' | 'app' | 'player';
    /**
     * Title of content (max 70 characters)
     *
     * Used with summary, summary_large_image, player cards
     *
     * Same as `og:title`
     *
     * @maxLength 70
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards
     */
    twitterTitle?: string;
    /**
     * Description of content (maximum 200 characters)
     *
     * Used with summary, summary_large_image, player cards.
     *
     * Same as `og:description`
     *
     * @maxLength 200
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards
     */
    twitterDescription?: string;
    /**
     * URL of image to use in the card.
     * Images must be less than 5MB in size.
     * JPG, PNG, WEBP and GIF formats are supported.
     * Only the first frame of an animated GIF will be used. SVG is not supported.
     *
     * Used with summary, summary_large_image, player cards
     *
     * Same as `og:image`.
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards
     */
    twitterImage?: string | Arrayable<{
        /**
         * Equivalent to twitter:image
         */
        url?: string;
        /**
         * MIME type of the image.
         * @deprecated Twitter removed this property from their card specification.
         */
        type?: 'image/jpeg' | 'image/gif' | 'image/png';
        /**
         * Width of image in pixels. Specify height and width for your image to ensure that the image loads properly the first time it's shared.
         * @deprecated Twitter removed this property from their card specification.
         */
        width?: '1200' | string | number;
        /**
         * Height of image in pixels. Specify height and width for your image to ensure that the image loads properly the first time it's shared.
         * @deprecated Twitter removed this property from their card specification.
         */
        height?: '630' | string | number;
        /**
         * A description of what is in the image (not a caption). If the page specifies an og:image, it should specify og:image:alt.
         */
        alt?: string;
    }>;
    /**
     * The width of the image in pixels.
     *
     * Note: This is not officially documented.
     *
     * Same as `og:image:width`
     *
     * @deprecated Twitter removed this property from their card specification.
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards
     */
    twitterImageWidth?: string | number;
    /**
     * The height of the image in pixels.
     *
     * Note: This is not officially documented.
     *
     * Same as `og:image:height`
     *
     * @deprecated Twitter removed this property from their card specification.
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards
     */
    twitterImageHeight?: string | number;
    /**
     * The type of the image.
     *
     * Note: This is not officially documented.
     *
     * Same as `og:image:type`
     *
     * @deprecated Twitter removed this property from their card specification.
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards
     */
    twitterImageType?: 'image/jpeg' | 'image/gif' | 'image/png';
    /**
     * A text description of the image conveying the essential nature of an image to users who are visually impaired.
     * Maximum 420 characters.
     *
     * Used with summary, summary_large_image, player cards
     *
     * Same as `og:image:alt`.
     *
     * @maxLength 420
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards
     */
    twitterImageAlt?: string;
    /**
     * The @username of website. Either twitter:site or twitter:site:id is required.
     *
     * Used with summary, summary_large_image, app, player cards
     *
     * @example @harlan_zw
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterSite?: string;
    /**
     * Same as twitter:site, but the user’s Twitter ID. Either twitter:site or twitter:site:id is required.
     *
     * Used with summary, summary_large_image, player cards
     *
     * @example 1296047337022742529
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterSiteId?: string | number;
    /**
     * The @username who created the pages content.
     *
     * Used with summary_large_image cards
     *
     * @example harlan_zw
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterCreator?: string;
    /**
     * Twitter user ID of content creator
     *
     * Used with summary, summary_large_image cards
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterCreatorId?: string | number;
    /**
     * HTTPS URL of player iframe
     *
     * Used with player card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterPlayer?: string;
    /**
     *
     * Width of iframe in pixels
     *
     * Used with player card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterPlayerWidth?: string | number;
    /**
     * Height of iframe in pixels
     *
     * Used with player card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterPlayerHeight?: string | number;
    /**
     * URL to raw video or audio stream
     *
     * Used with player card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterPlayerStream?: string;
    /**
     * Name of your iPhone app
     *
     * Used with app card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterAppNameIphone?: string;
    /**
     * Your app ID in the iTunes App Store
     *
     * Used with app card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterAppIdIphone?: string;
    /**
     * Your app’s custom URL scheme (you must include ”://” after your scheme name)
     *
     * Used with app card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterAppUrlIphone?: string;
    /**
     * Name of your iPad optimized app
     *
     * Used with app card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterAppNameIpad?: string;
    /**
     * Your app ID in the iTunes App Store
     *
     * Used with app card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterAppIdIpad?: string;
    /**
     * Your app’s custom URL scheme
     *
     * Used with app card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterAppUrlIpad?: string;
    /**
     * Name of your Android app
     *
     * Used with app card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterAppNameGoogleplay?: string;
    /**
     * Your app ID in the Google Play Store
     *
     * Used with app card
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterAppIdGoogleplay?: string;
    /**
     * Your app’s custom URL scheme
     *
     * @see https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/markup
     */
    twitterAppUrlGoogleplay?: string;
    /**
     * Top customizable data field, can be a relatively short string (ie “$3.99”)
     *
     * Used by Slack.
     *
     * @see https://api.slack.com/reference/messaging/link-unfurling#classic_unfurl
     */
    twitterData1?: string;
    /**
     * Customizable label or units for the information in twitter:data1 (best practice?: use all caps)
     *
     * Used by Slack.
     *
     * @see https://api.slack.com/reference/messaging/link-unfurling#classic_unfurl
     */
    twitterLabel1?: string;
    /**
     * Bottom customizable data field, can be a relatively short string (ie “Seattle, WA”)
     *
     * Used by Slack.
     *
     * @see https://api.slack.com/reference/messaging/link-unfurling#classic_unfurl
     */
    twitterData2?: string;
    /**
     * Customizable label or units for the information in twitter:data2 (best practice?: use all caps)
     *
     * Used by Slack.
     *
     * @see https://api.slack.com/reference/messaging/link-unfurling#classic_unfurl
     */
    twitterLabel2?: string;
    /**
     * Indicates a suggested color that user agents should use to customize the display of the page or
     * of the surrounding user interface.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta/name
     * @example `#4285f4` or `{ color?: '#4285f4', media?: '(prefers-color-scheme?: dark)'}`
     */
    themeColor?: string | Arrayable<{
        /**
         * A valid CSS color value that matches the value used for the `theme-color` CSS property.
         *
         * @example `#4285f4`
         */
        content?: string;
        /**
         * A valid media query that defines when the value should be used.
         *
         * @example `(prefers-color-scheme?: dark)`
         */
        media?: '(prefers-color-scheme?: dark)' | '(prefers-color-scheme?: light)' | string;
    }>;
    /**
     * Sets whether a web application runs in full-screen mode.
     */
    mobileWebAppCapable?: 'yes';
    /**
     * Sets whether a web application runs in full-screen mode.
     *
     * @see https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariHTMLRef/Articles/MetaTags.html
     */
    appleMobileWebAppCapable?: 'yes';
    /**
     * Sets the style of the status bar for a web application.
     *
     * @see https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariHTMLRef/Articles/MetaTags.html
     */
    appleMobileWebAppStatusBarStyle?: 'default' | 'black' | 'black-translucent';
    /**
     * Make the app title different from the page title.
     */
    appleMobileWebAppTitle?: string;
    /**
     * Promoting Apps with Smart App Banners
     *
     * @see https://developer.apple.com/documentation/webkit/promoting_apps_with_smart_app_banners
     */
    appleItunesApp?: string | {
        /**
         * Your app’s unique identifier.
         */
        appId?: string;
        /**
         * A URL that provides context to your native app.
         */
        appArgument?: string;
    };
    /**
     * Enables or disables automatic detection of possible phone numbers in a webpage in Safari on iOS.
     *
     * @see https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariHTMLRef/Articles/MetaTags.html
     */
    formatDetection?: 'telephone=no';
    /**
     * Tile image for windows.
     *
     * @see https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/dn320426(v=vs.85)
     */
    msapplicationTileImage?: string;
    /**
     * Tile colour for windows
     *
     * @see https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/dn320426(v=vs.85)
     */
    msapplicationTileColor?: string;
    /**
     * URL of a config for windows tile.
     *
     * @see https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/platform-apis/dn320426(v=vs.85)
     */
    msapplicationConfig?: string;
    contentSecurityPolicy?: string | Partial<{
        childSrc?: string;
        connectSrc?: string;
        defaultSrc?: string;
        fontSrc?: string;
        imgSrc?: string;
        manifestSrc?: string;
        mediaSrc?: string;
        objectSrc?: string;
        prefetchSrc?: string;
        scriptSrc?: string;
        scriptSrcElem?: string;
        scriptSrcAttr?: string;
        styleSrc?: string;
        styleSrcElem?: string;
        styleSrcAttr?: string;
        workerSrc?: string;
        baseUri?: string;
        sandbox?: string;
        formAction?: string;
        frameAncestors?: string;
        reportUri?: string;
        reportTo?: string;
        requireSriFor?: string;
        requireTrustedTypesFor?: string;
        trustedTypes?: string;
        upgradeInsecureRequests?: string;
    }>;
    contentType?: 'text/html; charset=utf-8';
    defaultStyle?: string;
    xUaCompatible?: 'IE=edge';
    refresh?: string | {
        seconds?: number | string;
        url?: string;
    };
    /**
     * A comma-separated list of keywords - relevant to the page (Legacy tag used to tell search engines what the page is about).
     * @deprecated the "keywords" metatag is no longer used.
     * @see https://web.dev/learn/html/metadata/#keywords
     */
    keywords?: string;
}

interface Noscript {
    /**
     * This attribute defines the unique ID.
     */
    id?: string;
    /**
     * The class global attribute is a space-separated list of the case-sensitive classes of the element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/class
     */
    class?: string;
    /**
     * The style global attribute contains CSS styling declarations to be applied to the element.
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/style
     */
    style?: string;
}

interface ScriptWithoutEvents extends Pick<GlobalAttributes, 'nonce' | 'id'>, Blocking {
    /**
     * For classic scripts, if the async attribute is present,
     * then the classic script will be fetched in parallel to parsing and evaluated as soon as it is available.
     *
     * For module scripts,
     * if the async attribute is present then the scripts and all their dependencies will be executed in the defer queue,
     * therefore they will get fetched in parallel to parsing and evaluated as soon as they are available.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-async
     */
    async?: Booleanable;
    /**
     * Normal script elements pass minimal information to the window.onerror
     * for scripts which do not pass the standard CORS checks.
     * To allow error logging for sites which use a separate domain for static media, use this attribute.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-crossorigin
     */
    crossorigin?: '' | 'anonymous' | 'use-credentials';
    /**
     * This Boolean attribute is set to indicate to a browser that the script is meant to be executed after the document
     * has been parsed, but before firing DOMContentLoaded.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-defer
     */
    defer?: Booleanable;
    /**
     * Provides a hint of the relative priority to use when fetching an external script.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-fetchpriority
     */
    fetchpriority?: 'high' | 'low' | 'auto';
    /**
     * This attribute contains inline metadata that a user agent can use to verify
     * that a fetched resource has been delivered free of unexpected manipulation.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-integrity
     */
    integrity?: string;
    /**
     * This Boolean attribute is set to indicate that the script should not be executed in browsers
     * that support ES modules — in effect,
     * this can be used to serve fallback scripts to older browsers that do not support modular JavaScript code.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-nomodule
     */
    nomodule?: Booleanable;
    /**
     * Indicates which referrer to send when fetching the script, or resources fetched by the script.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-referrerpolicy
     */
    referrerpolicy?: ReferrerPolicy;
    /**
     * This attribute specifies the URI of an external script;
     * this can be used as an alternative to embedding a script directly within a document.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-src
     */
    src?: string;
    /**
     * This attribute indicates the type of script represented.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script#attr-type
     */
    type?: '' | 'text/javascript' | 'module' | 'application/json' | 'application/ld+json' | 'speculationrules' | (string & Record<never, never>);
    /**
     * A custom element name
     *
     * Used by the AMP specification.
     *
     * @see https://amp.dev/documentation/guides-and-tutorials/learn/spec/amphtml/#custom-elements
     */
    ['custom-element']?: 'amp-story' | 'amp-carousel' | 'amp-ad' | (string & Record<never, never>);
}

interface Style extends Pick<GlobalAttributes, 'nonce' | 'id'>, Blocking {
    /**
     * This attribute defines which media the style should be applied to.
     * Its value is a media query, which defaults to all if the attribute is missing.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style#attr-media
     */
    media?: string;
    /**
     * A cryptographic nonce (number used once) used to allow inline styles in a style-src Content-Security-Policy.
     * The server must generate a unique nonce value each time it transmits a policy.
     * It is critical to provide a nonce that cannot be guessed as bypassing a resource's policy is otherwise trivial.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style#attr-nonce
     */
    nonce?: string;
    /**
     * This attribute specifies alternative style sheet sets.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style#attr-title
     */
    title?: string;
}

interface DeprecatedResolvesDuplicates {
    /**
     * @deprecated You should avoid using keys to dedupe meta as they are automatically deduped.
     * If you need to change the meta tag rendered use tagPriority.
     */
    key?: string;
    /**
     * @deprecated Remove
     */
    tagDuplicateStrategy?: 'replace' | 'merge';
}
interface SchemaAugmentations {
    title: TagPriority;
    titleTemplate: TagPriority;
    base: ResolvesDuplicates & TagPriority;
    htmlAttrs: ResolvesDuplicates & TagPriority;
    bodyAttrs: ResolvesDuplicates & TagPriority;
    link: TagPriority & TagPosition & ResolvesDuplicates & ProcessesTemplateParams;
    meta: TagPriority & DeprecatedResolvesDuplicates & ProcessesTemplateParams;
    style: TagPriority & TagPosition & InnerContent & ResolvesDuplicates & ProcessesTemplateParams;
    script: TagPriority & TagPosition & InnerContent & ResolvesDuplicates & ProcessesTemplateParams;
    noscript: TagPriority & TagPosition & InnerContent & ResolvesDuplicates & ProcessesTemplateParams;
}
type MaybeArray<T> = T | T[];
interface UnheadBodyAttributesWithoutEvents extends Omit<BodyAttributesWithoutEvents, 'class' | 'style'> {
    /**
     * The class global attribute is a space-separated list of the case-sensitive classes of the element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/class
     */
    class?: MaybeArray<ResolvableValue<Stringable>> | Record<string, ResolvableValue<boolean>>;
    /**
     * The style attribute contains CSS styling declarations to be applied to the element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/style
     */
    style?: MaybeArray<ResolvableValue<Stringable>> | Record<string, ResolvableValue<Stringable>>;
}
interface UnheadHtmlAttributes extends Omit<HtmlAttributes, 'class' | 'style'> {
    /**
     * The class global attribute is a space-separated list of the case-sensitive classes of the element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/class
     */
    class?: MaybeArray<ResolvableValue<Stringable>> | Record<string, ResolvableValue<boolean>>;
    /**
     * The style attribute contains CSS styling declarations to be applied to the element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/style
     */
    style?: MaybeArray<ResolvableValue<Stringable>> | Record<string, ResolvableValue<Stringable>>;
}
interface UnheadMeta extends Omit<Meta, 'content'> {
    /**
     * This attribute contains the value for the http-equiv, name or property attribute, depending on which is used.
     *
     * You can provide an array of values to create multiple tags sharing the same name, property or http-equiv.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta#attr-content
     */
    content?: MaybeArray<Stringable> | null;
}
type MaybeEventFnHandlers<T> = {
    [key in keyof T]?: T[key] | ((e: Event) => void);
};
type ResolvableTitle = ResolvableValue<Stringable> | ResolvableProperties<({
    textContent: string;
} & SchemaAugmentations['title'])>;
type ResolvableTitleTemplate = string | ((title?: string) => string | null) | null | ({
    textContent: string | ((title?: string) => string | null);
} & SchemaAugmentations['titleTemplate']);
type ResolvableBase = ResolvableProperties<Base & SchemaAugmentations['base']>;
type ResolvableLink = ResolvableProperties<LinkWithoutEvents & DataKeys & SchemaAugmentations['link']> & MaybeEventFnHandlers<HttpEventAttributes>;
type ResolvableMeta = ResolvableProperties<UnheadMeta & DataKeys & SchemaAugmentations['meta']>;
type ResolvableStyle = ResolvableProperties<Style & DataKeys & SchemaAugmentations['style']> | string;
type ResolvableScript = ResolvableProperties<ScriptWithoutEvents & DataKeys & SchemaAugmentations['script']> & MaybeEventFnHandlers<HttpEventAttributes> | string;
type ResolvableNoscript = ResolvableProperties<Noscript & DataKeys & SchemaAugmentations['noscript']> | string;
type ResolvableHtmlAttributes = ResolvableProperties<UnheadHtmlAttributes & DataKeys & SchemaAugmentations['htmlAttrs']>;
type ResolvableBodyAttributes = ResolvableProperties<UnheadBodyAttributesWithoutEvents & DataKeys & SchemaAugmentations['bodyAttrs']> & MaybeEventFnHandlers<BodyEvents>;
type ResolvableTemplateParams = {
    separator?: '|' | '-' | '·' | string;
} & Record<string, null | string | Record<string, string>>;
interface ResolvableHead {
    /**
     * The `<title>` HTML element defines the document's title that is shown in a browser's title bar or a page's tab.
     * It only contains text; tags within the element are ignored.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title
     */
    title?: ResolvableTitle;
    /**
     * The `<base>` HTML element specifies the base URL to use for all relative URLs in a document.
     * There can be only one <base> element in a document.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/base
     */
    base?: ResolvableValue<ResolvableBase>;
    /**
     * The `<link>` HTML element specifies relationships between the current document and an external resource.
     * This element is most commonly used to link to stylesheets, but is also used to establish site icons
     * (both "favicon" style icons and icons for the home screen and apps on mobile devices) among other things.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#attr-as
     */
    link?: ResolvableValue<ResolvableValue<ResolvableLink>[]>;
    /**
     * The `<meta>` element represents metadata that cannot be expressed in other HTML elements, like `<link>` or `<script>`.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/meta
     */
    meta?: ResolvableValue<ResolvableValue<ResolvableMeta>[]>;
    /**
     * The `<style>` HTML element contains style information for a document, or part of a document.
     * It contains CSS, which is applied to the contents of the document containing the `<style>` element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/style
     */
    style?: ResolvableValue<ResolvableValue<(ResolvableStyle)>[]>;
    /**
     * The `<script>` HTML element is used to embed executable code or data; this is typically used to embed or refer to JavaScript code.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script
     */
    script?: ResolvableValue<ResolvableValue<(ResolvableScript)>[]>;
    /**
     * The `<noscript>` HTML element defines a section of HTML to be inserted if a script type on the page is unsupported
     * or if scripting is currently turned off in the browser.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/noscript
     */
    noscript?: ResolvableValue<ResolvableValue<(ResolvableNoscript)>[]>;
    /**
     * Attributes for the `<html>` HTML element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/html
     */
    htmlAttrs?: ResolvableValue<ResolvableHtmlAttributes>;
    /**
     * Attributes for the `<body>` HTML element.
     *
     * @see https://developer.mozilla.org/en-US/docs/Web/HTML/Element/body
     */
    bodyAttrs?: ResolvableValue<ResolvableBodyAttributes>;
    /**
     * Generate the title from a template.
     *
     * Should include a `%s` placeholder for the title, for example `%s - My Site`.
     */
    titleTemplate?: ResolvableTitleTemplate;
    /**
     * Variables used to substitute in the title and meta content.
     */
    templateParams?: ResolvableTemplateParams;
}
interface SerializableHead {
    title?: string;
    titleTemplate?: string;
    base?: Base & DataKeys & SchemaAugmentations['base'];
    templateParams?: Record<string, any>;
    link?: (LinkWithoutEvents & DataKeys & HttpEventAttributes & SchemaAugmentations['link'])[];
    meta?: (Meta & DataKeys & SchemaAugmentations['meta'])[];
    style?: (Style & DataKeys & SchemaAugmentations['style'])[];
    script?: (ScriptWithoutEvents & DataKeys & HttpEventAttributes & SchemaAugmentations['script'])[];
    noscript?: (Noscript & DataKeys & SchemaAugmentations['noscript'])[];
    htmlAttrs?: HtmlAttributes & DataKeys & SchemaAugmentations['htmlAttrs'];
    bodyAttrs?: BodyAttributesWithoutEvents & DataKeys & BodyEvents & SchemaAugmentations['bodyAttrs'];
}
type RawInput<K extends keyof SerializableHead> = Required<SerializableHead>[K] extends Array<infer T> ? T : Required<SerializableHead>[K];
/**
 * @deprecated Use SerializableResolvedHead
 */
type Head = SerializableHead;
/**
 * @deprecated Use SerializableResolvedHead
 */
type ResolvedHead = SerializableHead;
type UseSeoMetaInput = DeepResolvableProperties<MetaFlat> & {
    title?: ResolvableTitle;
    titleTemplate?: ResolvableTitleTemplate;
};
type UseHeadInput = ResolvableHead | SerializableHead;
type MetaFlatInput = MetaFlat;

/**
 * @deprecated No longer used
 */
type MergeHead = Record<string, any>;

interface ResolvesDuplicates {
    /**
     * By default, tags which share the same unique key `name`, `property` are de-duped. To allow duplicates
     * to be made you can provide a unique key for each entry.
     */
    key?: string;
    /**
     * The strategy to use when a duplicate tag is encountered.
     *
     * - `replace` - Replace the existing tag with the new tag
     * - `merge` - Merge the existing tag with the new tag
     *
     * @default 'replace' (some tags will default to 'merge', such as htmlAttr)
     */
    tagDuplicateStrategy?: 'replace' | 'merge';
}
type ValidTagPositions = 'head' | 'bodyClose' | 'bodyOpen';
interface TagPosition {
    /**
     * Specify where to render the tag.
     *
     * @default 'head'
     */
    tagPosition?: ValidTagPositions;
}
type InnerContentVal = string | Record<string, any>;
interface InnerContent {
    /**
     * Text content of the tag.
     *
     * Warning: This is not safe for XSS. Do not use this with user input, use `textContent` instead.
     */
    innerHTML?: InnerContentVal;
    /**
     * Sets the textContent of an element. Safer for XSS.
     */
    textContent?: InnerContentVal;
}
interface TagPriority {
    /**
     * The priority for rendering the tag, without this all tags are rendered as they are registered
     * (besides some special tags).
     *
     * The following special tags have default priorities:
     * -2 `<meta charset ...>`
     * -1 `<base>`
     * 0 `<meta http-equiv="content-security-policy" ...>`
     *
     * All other tags have a default priority of 10: `<meta>`, `<script>`, `<link>`, `<style>`, etc
     */
    tagPriority?: number | 'critical' | 'high' | 'low' | `before:${string}` | `after:${string}`;
}
type TagUserProperties = ResolvableProperties<TagPriority & TagPosition & InnerContent & ResolvesDuplicates & ProcessesTemplateParams>;
type TagKey = keyof ResolvableHead;
type TemplateParams = {
    separator?: '|' | '-' | '·' | string;
} & Record<string, null | string | Record<string, string>>;
interface ProcessesTemplateParams {
    processTemplateParams?: boolean;
}
interface HasTemplateParams {
    templateParams?: TemplateParams;
}
interface HeadTag extends TagPriority, TagPosition, ResolvesDuplicates, HasTemplateParams {
    tag: TagKey;
    props: Record<string, string>;
    processTemplateParams?: boolean;
    innerHTML?: string;
    textContent?: string;
    /**
     * @internal
     */
    _w?: number;
    /**
     * @internal
     */
    _p?: number;
    /**
     * @internal
     */
    _d?: string;
    /**
     * @internal
     */
    _h?: string;
    /**
     * @internal
     */
    mode?: RuntimeMode;
}
type HeadTagKeys = (keyof HeadTag)[];

type HookResult = Promise<void> | void;
interface SSRHeadPayload {
    headTags: string;
    bodyTags: string;
    bodyTagsOpen: string;
    htmlAttrs: string;
    bodyAttrs: string;
}
interface RenderSSRHeadOptions {
    omitLineBreaks?: boolean;
    resolvedTags?: HeadTag[];
}
interface EntryResolveCtx<T> {
    tags: HeadTag[];
    entries: HeadEntry<T>[];
}
interface DomRenderTagContext {
    id: string;
    $el: Element;
    shouldRender: boolean;
    tag: HeadTag;
    entry?: HeadEntry<any>;
    markSideEffect: (key: string, fn: () => void) => void;
}
interface DomBeforeRenderCtx extends ShouldRenderContext {
    /**
     * @deprecated will always be empty, prefer other hooks
     */
    tags: DomRenderTagContext[];
}
interface ShouldRenderContext {
    shouldRender: boolean;
}
interface SSRRenderContext {
    tags: HeadTag[];
    html: SSRHeadPayload;
}
interface TagResolveContext {
    tagMap: Map<string, HeadTag>;
    tags: HeadTag[];
}
interface HeadHooks {
    /**
     * @deprecated use Unhead options to setup instead
     */
    'init': (ctx: Unhead<any>) => HookResult;
    'entries:updated': (ctx: Unhead<any>) => HookResult;
    'entries:resolve': (ctx: EntryResolveCtx<any>) => HookResult;
    'entries:normalize': (ctx: {
        tags: HeadTag[];
        entry: HeadEntry<any>;
    }) => HookResult;
    'tag:normalise': (ctx: {
        tag: HeadTag;
        entry: HeadEntry<any>;
        resolvedOptions: CreateClientHeadOptions;
    }) => HookResult;
    'tags:beforeResolve': (ctx: TagResolveContext) => HookResult;
    'tags:resolve': (ctx: TagResolveContext) => HookResult;
    'tags:afterResolve': (ctx: TagResolveContext) => HookResult;
    'dom:beforeRender': (ctx: DomBeforeRenderCtx) => HookResult;
    'dom:renderTag': (ctx: DomRenderTagContext, document: Document, track: any) => HookResult;
    'dom:rendered': (ctx: {
        renders: DomRenderTagContext[];
    }) => HookResult;
    'ssr:beforeRender': (ctx: ShouldRenderContext) => HookResult;
    'ssr:render': (ctx: {
        tags: HeadTag[];
    }) => HookResult;
    'ssr:rendered': (ctx: SSRRenderContext) => HookResult;
    'script:updated': (ctx: {
        script: ScriptInstance<any>;
    }) => void | Promise<void>;
}

interface RenderDomHeadOptions {
    /**
     * Document to use for rendering. Allows stubbing for testing.
     */
    document?: Document;
}
interface DomPluginOptions extends RenderDomHeadOptions {
    render: ((head: Unhead<any>) => void);
}

/**
 * Side effects are mapped with a key and their cleanup function.
 *
 * For example, `meta:data-h-4h46h465`: () => { document.querySelector('meta[data-h-4h46h465]').remove() }
 */
type SideEffectsRecord = Record<string, () => void>;
type RuntimeMode = 'server' | 'client';
interface HeadEntry<Input> {
    /**
     * User provided input for the entry.
     */
    input: Input;
    options?: {
        /**
         * The mode that the entry should be used in.
         *
         * @internal
         */
        mode?: RuntimeMode;
        /**
         * Default tag position.
         *
         * @internal
         */
        tagPosition?: TagPosition['tagPosition'];
        /**
         * Default tag priority.
         *
         * @internal
         */
        tagPriority?: TagPriority['tagPriority'];
        /**
         * Default tag duplicate strategy.
         *
         * @internal
         */
        tagDuplicateStrategy?: HeadTag['tagDuplicateStrategy'];
        /**
         * @internal
         */
        _safe?: boolean;
    };
    /**
     * Head entry index
     *
     * @internal
     */
    _i: number;
    /**
     * Resolved tags
     *
     * @internal
     */
    _tags?: HeadTag[];
    /**
     * @internal
     */
    _promisesProcessed?: boolean;
}
type HeadPluginOptions = Omit<CreateHeadOptions, 'plugins'>;
type HeadPluginInput = (HeadPluginOptions & {
    key: string;
}) | ((head: Unhead) => HeadPluginOptions & {
    key: string;
});
type HeadPlugin = HeadPluginOptions & {
    key: string;
};
/**
 * An active head entry provides an API to manipulate it.
 */
interface ActiveHeadEntry<Input> {
    /**
     * Updates the entry with new input.
     *
     * Will first clear any side effects for previous input.
     */
    patch: (input: Input) => void;
    /**
     * Dispose the entry, removing it from the active head.
     *
     * Will queue side effects for removal.
     */
    dispose: () => void;
    /**
     * @internal
     */
    _poll: (rm?: boolean) => void;
}
type PropResolver = (key?: string, value?: any, tag?: HeadTag) => any;
interface CreateHeadOptions {
    document?: Document;
    plugins?: HeadPluginInput[];
    hooks?: NestedHooks<HeadHooks>;
    /**
     * Initial head input that should be added.
     *
     * Any tags here are added with low priority.
     */
    init?: (ResolvableHead | undefined | false)[];
    /**
     * Disable the Capo.js tag sorting algorithm.
     *
     * This is added to make the v1 -> v2 migration easier allowing users to opt-out of the new sorting algorithm.
     */
    disableCapoSorting?: boolean;
    /**
     * Prop resolvers for tags.
     */
    propResolvers?: PropResolver[];
}
interface CreateServerHeadOptions extends CreateHeadOptions {
    /**
     * Should default important tags be skipped.
     *
     * Adds the following tags with low priority:
     * - <html lang="en">
     * - <meta charset="utf-8">
     * - <meta name="viewport" content="width=device-width, initial-scale=1">
     */
    disableDefaults?: boolean;
}
interface CreateClientHeadOptions extends CreateHeadOptions {
    /**
     * Options to pass to the DomPlugin.
     */
    domOptions?: DomPluginOptions;
}
interface HeadEntryOptions extends TagPosition, TagPriority, ProcessesTemplateParams, ResolvesDuplicates {
    /**
     * @deprecated Tree shaking should now be handled using import.meta.* if statements.
     */
    mode?: RuntimeMode;
    head?: Unhead;
    /**
     * @internal
     */
    _safe?: boolean;
    /**
     * @internal
     */
    _index?: number;
}
interface Unhead<Input = ResolvableHead> {
    /**
     * Registered plugins.
     */
    plugins: Map<string, HeadPlugin>;
    /**
     * The head entries.
     */
    entries: Map<number, HeadEntry<Input>>;
    /**
     * The active head entries.
     *
     * @deprecated Use entries instead.
     */
    headEntries: () => HeadEntry<Input>[];
    /**
     * Create a new head entry.
     */
    push: (entry: Input, options?: HeadEntryOptions) => ActiveHeadEntry<Input>;
    /**
     * Resolve tags from head entries.
     */
    resolveTags: () => Promise<HeadTag[]>;
    /**
     * Invalidate all entries and re-queue them for normalization.
     */
    invalidate: () => void;
    /**
     * Exposed hooks for easier extension.
     */
    hooks: Hookable<HeadHooks>;
    /**
     * Resolved options
     */
    resolvedOptions: CreateHeadOptions;
    /**
     * Use a head plugin, loads the plugins hooks.
     */
    use: (plugin: HeadPluginInput) => void;
    /**
     * Is it a server-side render context.
     */
    ssr: boolean;
    /**
     * @internal
     */
    _dom?: DomState;
    /**
     * @internal
     */
    _domUpdatePromise?: Promise<void>;
    /**
     * @internal
     */
    dirty: boolean;
    /**
     * @internal
     */
    _scripts?: Record<string, any>;
    /**
     * @internal
     */
    _templateParams?: TemplateParams;
    /**
     * @internal
     */
    _separator?: string;
    /**
     * @internal
     */
    _entryCount: number;
    /**
     * @internal
     */
    _title?: string;
    /**
     * @internal
     */
    _titleTemplate?: string;
    /**
     * @internal
     */
    _ssrPayload?: ResolvableHead;
}
interface DomState {
    title: string;
    pendingSideEffects: SideEffectsRecord;
    sideEffects: SideEffectsRecord;
    elMap: Map<string, Element | Element[]>;
}

export type { ResolvableStyle as $, AsVoidFunctions as A, Booleanable as B, CreateHeadOptions as C, DomState as D, EventHandlerOptions as E, SSRRenderContext as F, HeadHooks as G, HeadEntry as H, RenderDomHeadOptions as I, DomPluginOptions as J, SchemaAugmentations as K, MaybeArray as L, MetaFlatInput as M, UnheadBodyAttributesWithoutEvents as N, UnheadHtmlAttributes as O, PropResolver as P, UnheadMeta as Q, ResolvableHead as R, SerializableHead as S, MaybeEventFnHandlers as T, Unhead as U, ResolvableTitle as V, WarmupStrategy as W, ResolvableTitleTemplate as X, ResolvableBase as Y, ResolvableLink as Z, ResolvableMeta as _, UseScriptInput as a, ResolvableScript as a0, ResolvableNoscript as a1, ResolvableHtmlAttributes as a2, ResolvableBodyAttributes as a3, ResolvableTemplateParams as a4, RawInput as a5, Head as a6, ResolvedHead as a7, UseSeoMetaInput as a8, UseHeadInput as a9, ResolvableProperties as aA, ResolvableUnion as aB, DeepResolvableProperties as aC, MergeHead as aa, DataKeys as ab, HttpEventAttributes as ac, GlobalAttributes as ad, BodyAttributesWithoutEvents as ae, BodyEvents as af, LinkWithoutEvents as ag, MetaFlat as ah, ScriptWithoutEvents as ai, ResolvesDuplicates as aj, ValidTagPositions as ak, TagPosition as al, InnerContentVal as am, InnerContent as an, TagPriority as ao, TagUserProperties as ap, TagKey as aq, TemplateParams as ar, ProcessesTemplateParams as as, HasTemplateParams as at, HeadTag as au, HeadTagKeys as av, Stringable as aw, Arrayable as ax, Never as ay, ResolvableValue as az, UseScriptOptions as b, UseScriptReturn as c, UseScriptResolvedInput as d, ReferrerPolicy as e, UseScriptStatus as f, UseScriptContext as g, UseFunctionType as h, ScriptInstance as i, RecordingEntry as j, SideEffectsRecord as k, RuntimeMode as l, HeadPluginOptions as m, HeadPluginInput as n, HeadPlugin as o, ActiveHeadEntry as p, CreateServerHeadOptions as q, CreateClientHeadOptions as r, HeadEntryOptions as s, HookResult as t, SSRHeadPayload as u, RenderSSRHeadOptions as v, EntryResolveCtx as w, DomRenderTagContext as x, DomBeforeRenderCtx as y, ShouldRenderContext as z };
