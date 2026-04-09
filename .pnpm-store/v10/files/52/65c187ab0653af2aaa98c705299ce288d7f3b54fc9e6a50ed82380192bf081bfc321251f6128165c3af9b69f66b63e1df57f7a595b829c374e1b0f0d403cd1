/**
 * Parse options.
 */
interface CookieParseOptions {
  /**
   * Specifies a function that will be used to decode a [cookie-value](https://datatracker.ietf.org/doc/html/rfc6265#section-4.1.1).
   * Since the value of a cookie has a limited character set (and must be a simple string), this function can be used to decode
   * a previously-encoded cookie value into a JavaScript string.
   *
   * The default function is the global `decodeURIComponent`, wrapped in a `try..catch`. If an error
   * is thrown it will return the cookie's original value. If you provide your own encode/decode
   * scheme you must ensure errors are appropriately handled.
   *
   * @default decode
   */
  decode?: (str: string) => string | undefined;
  /**
   * Custom function to filter parsing specific keys.
   */
  filter?(key: string): boolean;
  /**
   * When enabled, duplicate cookie names will return an array of values
   * instead of only the first value.
   */
  allowMultiple?: boolean;
}
/**
 * Cookies object.
 */
type Cookies = Record<string, string | undefined>;
/**
 * Cookies object when `allowMultiple` is enabled.
 */
type MultiCookies = Record<string, string | string[] | undefined>;
/**
 * Stringify options.
 */
interface CookieStringifyOptions {
  /**
   * Specifies a function that will be used to encode a [cookie-value](https://datatracker.ietf.org/doc/html/rfc6265#section-4.1.1).
   * Since value of a cookie has a limited character set (and must be a simple string), this function can be used to encode
   * a value into a string suited for a cookie's value, and should mirror `decode` when parsing.
   *
   * @default encodeURIComponent
   */
  encode?: (str: string) => string;
  /**
   * Specifies a function that will be used to coerce non-string values to a string.
   *
   * @default JSON.stringify
   */
  stringify?: (value: unknown) => string;
}
/**
 * Set-Cookie object.
 */
interface SetCookie {
  /**
   * Specifies the name of the cookie.
   */
  name: string;
  /**
   * Specifies the string to be the value for the cookie.
   */
  value: string | undefined;
  /**
   * Specifies the `number` (in seconds) to be the value for the [`Max-Age` `Set-Cookie` attribute](https://tools.ietf.org/html/rfc6265#section-5.2.2).
   *
   * The [cookie storage model specification](https://tools.ietf.org/html/rfc6265#section-5.3) states that if both `expires` and
   * `maxAge` are set, then `maxAge` takes precedence, but it is possible not all clients by obey this,
   * so if both are set, they should point to the same date and time.
   */
  maxAge?: number;
  /**
   * Specifies the `Date` object to be the value for the [`Expires` `Set-Cookie` attribute](https://tools.ietf.org/html/rfc6265#section-5.2.1).
   * When no expiration is set, clients consider this a "non-persistent cookie" and delete it when the current session is over.
   *
   * The [cookie storage model specification](https://tools.ietf.org/html/rfc6265#section-5.3) states that if both `expires` and
   * `maxAge` are set, then `maxAge` takes precedence, but it is possible not all clients by obey this,
   * so if both are set, they should point to the same date and time.
   */
  expires?: Date;
  /**
   * Specifies the value for the [`Domain` `Set-Cookie` attribute](https://tools.ietf.org/html/rfc6265#section-5.2.3).
   * When no domain is set, clients consider the cookie to apply to the current domain only.
   */
  domain?: string;
  /**
   * Specifies the value for the [`Path` `Set-Cookie` attribute](https://tools.ietf.org/html/rfc6265#section-5.2.4).
   * When no path is set, the path is considered the ["default path"](https://tools.ietf.org/html/rfc6265#section-5.1.4).
   */
  path?: string;
  /**
   * Enables the [`HttpOnly` `Set-Cookie` attribute](https://tools.ietf.org/html/rfc6265#section-5.2.6).
   * When enabled, clients will not allow client-side JavaScript to see the cookie in `document.cookie`.
   */
  httpOnly?: boolean;
  /**
   * Enables the [`Secure` `Set-Cookie` attribute](https://tools.ietf.org/html/rfc6265#section-5.2.5).
   * When enabled, clients will only send the cookie back if the browser has an HTTPS connection.
   */
  secure?: boolean;
  /**
   * Enables the [`Partitioned` `Set-Cookie` attribute](https://tools.ietf.org/html/draft-cutler-httpbis-partitioned-cookies/).
   * When enabled, clients will only send the cookie back when the current domain _and_ top-level domain matches.
   *
   * This is an attribute that has not yet been fully standardized, and may change in the future.
   * This also means clients may ignore this attribute until they understand it. More information
   * about can be found in [the proposal](https://github.com/privacycg/CHIPS).
   */
  partitioned?: boolean;
  /**
   * Specifies the value for the [`Priority` `Set-Cookie` attribute](https://tools.ietf.org/html/draft-west-cookie-priority-00#section-4.1).
   *
   * - `'low'` will set the `Priority` attribute to `Low`.
   * - `'medium'` will set the `Priority` attribute to `Medium`, the default priority when not set.
   * - `'high'` will set the `Priority` attribute to `High`.
   *
   * More information about priority levels can be found in [the specification](https://tools.ietf.org/html/draft-west-cookie-priority-00#section-4.1).
   */
  priority?: "low" | "medium" | "high";
  /**
   * Specifies the value for the [`SameSite` `Set-Cookie` attribute](https://tools.ietf.org/html/draft-ietf-httpbis-rfc6265bis-09#section-5.4.7).
   *
   * - `true` will set the `SameSite` attribute to `Strict` for strict same site enforcement.
   * - `'lax'` will set the `SameSite` attribute to `Lax` for lax same site enforcement.
   * - `'none'` will set the `SameSite` attribute to `None` for an explicit cross-site cookie.
   * - `'strict'` will set the `SameSite` attribute to `Strict` for strict same site enforcement.
   *
   * More information about enforcement levels can be found in [the specification](https://tools.ietf.org/html/draft-ietf-httpbis-rfc6265bis-09#section-5.4.7).
   */
  sameSite?: boolean | "lax" | "strict" | "none";
}
/**
 * Backward compatibility serialize options.
 */
type CookieSerializeOptions = CookieStringifyOptions & Omit<SetCookie, "name" | "value">;
/**
 * Parse a `Cookie` header string into an object.
 *
 * The object has cookie names as keys and decoded values as values.
 * First occurrence wins for duplicate names unless `allowMultiple` is set.
 *
 * @param str - The `Cookie` header string to parse.
 * @param options - Parsing options (`decode`, `filter`, `allowMultiple`).
 * @returns A prototype-less object of cookie name-value pairs.
 */
declare function parse(str: string, options: CookieParseOptions & {
  allowMultiple: true;
}): MultiCookies;
declare function parse(str: string, options?: CookieParseOptions): Cookies;
/**
 * Stringify a cookies object into an HTTP `Cookie` header string.
 *
 * @param cookie - An object of cookie name-value pairs.
 * @param options - Stringify options (`encode`).
 * @returns A `Cookie` header string (e.g. `"foo=bar; baz=qux"`).
 */
declare function stringifyCookie(cookie: Cookies, options?: CookieStringifyOptions): string;
/**
 * Serialize a cookie into a `Set-Cookie` header string.
 *
 * Accepts either a name-value pair with options or a `SetCookie` object.
 * Non-string values are coerced to strings. Validates name, value, domain,
 * and path against RFC 6265bis.
 *
 * @example
 * ```js
 * serialize("foo", "bar", { httpOnly: true });
 * // => "foo=bar; HttpOnly"
 *
 * serialize({ name: "foo", value: "bar", secure: true });
 * // => "foo=bar; Secure"
 * ```
 */
declare function serialize(cookie: SetCookie, options?: CookieStringifyOptions): string;
declare function serialize(name: string, val: unknown, options?: CookieSerializeOptions): string;
interface SetCookieParseOptions {
  /**
   * Custom decode function to use on cookie values.
   *
   * By default, `decodeURIComponent` is used.
   *
   * **Note:** If decoding fails, the original (undecoded) value will be used
   */
  decode?: false | ((value: string) => string);
}
interface SetCookie$1 {
  /**
   * Cookie name
   */
  name: string;
  /**
   * Cookie value
   */
  value: string;
  /**
   * Cookie path
   */
  path?: string | undefined;
  /**
   * Absolute expiration date for the cookie
   */
  expires?: Date | undefined;
  /**
   * Relative max age of the cookie in seconds from when the client receives it (integer or undefined)
   *
   * Note: when using with express's res.cookie() method, multiply maxAge by 1000 to convert to milliseconds
   */
  maxAge?: number | undefined;
  /**
   * Domain for the cookie,
   * May begin with "." to indicate the named domain or any subdomain of it
   */
  domain?: string | undefined;
  /**
   * Indicates that this cookie should only be sent over HTTPs
   */
  secure?: boolean | undefined;
  /**
   * Indicates that this cookie should not be accessible to client-side JavaScript
   */
  httpOnly?: boolean | undefined;
  /**
   * Indicates a cookie ought not to be sent along with cross-site requests
   */
  sameSite?: true | false | "lax" | "strict" | "none" | undefined;
  /**
   * Indicates that the cookie should be stored using partitioned storage
   *
   * See https://developer.mozilla.org/en-US/docs/Web/Privacy/Privacy_sandbox/Partitioned_cookies
   */
  partitioned?: boolean | undefined;
  /**
   * Indicates the priority of the cookie
   *
   * See https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie#prioritylow_medium_high
   */
  priority?: "low" | "medium" | "high" | undefined;
  [key: string]: unknown;
}
/**
 * Parse a [`Set-Cookie`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie) header string into an object.
 *
 * Returns `undefined` for cookies with forbidden names (prototype pollution protection)
 * or when both name and value are empty (RFC 6265bis sec 5.7).
 *
 * @param str - The `Set-Cookie` header string to parse.
 * @param options - Parsing options (`decode`).
 * @returns A `SetCookie` object with all parsed attributes, or `undefined`.
 */
declare function parseSetCookie(str: string, options?: SetCookieParseOptions): SetCookie$1 | undefined;
/**
 * Split comma-joined `Set-Cookie` header strings into individual cookie strings.
 *
 * Correctly handles commas within cookie attributes like `Expires` dates
 * by checking for `=` after a comma to determine if it's a cookie separator.
 *
 * @param cookiesString - A comma-joined `Set-Cookie` string or array of strings.
 * @returns An array of individual `Set-Cookie` strings.
 *
 * @see https://tools.ietf.org/html/rfc2616#section-4.2
 */
declare function splitSetCookieString(cookiesString: string | string[]): string[];
export { type CookieParseOptions, type CookieSerializeOptions, type CookieStringifyOptions, type Cookies, type MultiCookies, type SetCookie, type SetCookieParseOptions, parse, parse as parseCookie, parseSetCookie, serialize, serialize as serializeCookie, splitSetCookieString, stringifyCookie };