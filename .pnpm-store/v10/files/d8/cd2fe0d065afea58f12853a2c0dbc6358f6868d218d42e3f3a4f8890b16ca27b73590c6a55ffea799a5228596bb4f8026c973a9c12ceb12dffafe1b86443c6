import { getResponseStatus, getResponseStatusText } from "h3";
import devalue from "@nuxt/devalue";
import { stringify, uneval } from "devalue";
// @ts-expect-error virtual file
import { appId, multiApp } from "#internal/nuxt.config.mjs";
// @ts-expect-error virtual file
import { NUXT_JSON_PAYLOADS, NUXT_NO_SSR } from "#internal/nuxt/nitro-config.mjs";
export function renderPayloadResponse(ssrContext) {
	return {
		body: NUXT_JSON_PAYLOADS ? encodeForwardSlashes(stringify(splitPayload(ssrContext).payload, ssrContext["~payloadReducers"])) : `export default ${devalue(splitPayload(ssrContext).payload)}`,
		statusCode: getResponseStatus(ssrContext.event),
		statusMessage: getResponseStatusText(ssrContext.event),
		headers: {
			"content-type": NUXT_JSON_PAYLOADS ? "application/json;charset=utf-8" : "text/javascript;charset=utf-8",
			"x-powered-by": "Nuxt"
		}
	};
}
export function renderPayloadJsonScript(opts) {
	const contents = opts.data ? encodeForwardSlashes(stringify(opts.data, opts.ssrContext["~payloadReducers"])) : "";
	const payload = {
		"type": "application/json",
		"innerHTML": contents,
		"data-nuxt-data": appId,
		"data-ssr": !(NUXT_NO_SSR || opts.ssrContext.noSSR)
	};
	if (!multiApp) {
		payload.id = "__NUXT_DATA__";
	}
	if (opts.src) {
		payload["data-src"] = opts.src;
	}
	const config = uneval(opts.ssrContext.config);
	return [payload, { innerHTML: multiApp ? `window.__NUXT__=window.__NUXT__||{};window.__NUXT__[${JSON.stringify(appId)}]={config:${config}}` : `window.__NUXT__={};window.__NUXT__.config=${config}` }];
}
/**
* Encode forward slashes as unicode escape sequences to prevent
* Google from treating them as internal links and trying to crawl them.
* @see https://github.com/nuxt/nuxt/issues/24175
*/
function encodeForwardSlashes(str) {
	return str.replaceAll("/", "\\u002F");
}
/**
* Escape a string for safe interpolation inside a double-quoted JavaScript string literal.
* Prevents XSS when user-controlled URLs are embedded in inline `<script>` tags.
*/
function escapeJsString(str) {
	return str.replaceAll("\\", "\\\\").replaceAll("\"", "\\\"").replaceAll("\n", "\\n").replaceAll("\r", "\\r").replaceAll("/", "\\u002F").replaceAll("<", "\\u003C");
}
export function renderPayloadScript(opts) {
	opts.data.config = opts.ssrContext.config;
	const nuxtData = devalue(opts.data);
	if (opts.src) {
		// Escape the URL to prevent XSS when interpolated into a JS string literal
		const escapedSrc = escapeJsString(opts.src);
		const singleAppPayload = `import p from "${escapedSrc}";window.__NUXT__={...p,...(${nuxtData})}`;
		const multiAppPayload = `import p from "${escapedSrc}";window.__NUXT__=window.__NUXT__||{};window.__NUXT__[${JSON.stringify(appId)}]={...p,...(${nuxtData})}`;
		return [{
			type: "module",
			innerHTML: multiApp ? multiAppPayload : singleAppPayload
		}];
	}
	const singleAppPayload = `window.__NUXT__=${nuxtData}`;
	const multiAppPayload = `window.__NUXT__=window.__NUXT__||{};window.__NUXT__[${JSON.stringify(appId)}]=${nuxtData}`;
	return [{ innerHTML: multiApp ? multiAppPayload : singleAppPayload }];
}
export function splitPayload(ssrContext) {
	const { data, prerenderedAt, ...initial } = ssrContext.payload;
	return {
		initial: {
			...initial,
			prerenderedAt
		},
		payload: {
			data,
			prerenderedAt
		}
	};
}
