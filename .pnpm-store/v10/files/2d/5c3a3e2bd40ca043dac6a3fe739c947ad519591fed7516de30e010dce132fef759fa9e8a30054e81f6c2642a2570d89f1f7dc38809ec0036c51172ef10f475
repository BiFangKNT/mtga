import { defineEventHandler, getRequestHeader } from "h3";
const handler = defineEventHandler((event) => {
	if (getRequestHeader(event, "x-nuxt-no-ssr")) {
		event.context.nuxt ||= {};
		event.context.nuxt.noSSR = true;
	}
});
export default handler;
