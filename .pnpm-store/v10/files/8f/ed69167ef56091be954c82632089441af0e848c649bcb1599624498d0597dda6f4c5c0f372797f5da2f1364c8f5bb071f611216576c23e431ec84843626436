import { getRequestURL } from "@nuxt/nitro-server/h3";
import { useRequestEvent } from "./ssr.js";
export function useRequestURL(opts) {
  if (import.meta.server) {
    return getRequestURL(useRequestEvent(), opts);
  }
  return new URL(globalThis.location.href);
}
