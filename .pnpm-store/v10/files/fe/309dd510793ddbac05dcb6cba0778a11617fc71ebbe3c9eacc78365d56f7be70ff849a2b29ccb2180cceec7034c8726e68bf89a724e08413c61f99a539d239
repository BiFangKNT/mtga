import { createError } from "../composables/error.js";
function renderStubMessage(name) {
  throw createError({
    fatal: true,
    status: 500,
    statusText: `${name} is provided by @nuxt/image. Check your console to install it or run 'npx nuxt module add @nuxt/image'`
  });
}
export const NuxtImg = {
  setup: () => renderStubMessage("<NuxtImg>")
};
export const NuxtPicture = {
  setup: () => renderStubMessage("<NuxtPicture>")
};
