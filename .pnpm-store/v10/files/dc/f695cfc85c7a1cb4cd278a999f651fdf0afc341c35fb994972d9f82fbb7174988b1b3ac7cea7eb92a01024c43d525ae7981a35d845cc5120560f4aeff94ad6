import { defineNuxtPlugin } from "../nuxt.js";
import { onNuxtReady } from "../composables/ready.js";
import { useRouter } from "../composables/router.js";
export default defineNuxtPlugin(() => {
  const router = useRouter();
  onNuxtReady(() => {
    router.beforeResolve(async () => {
      await new Promise((resolve) => {
        setTimeout(resolve, 100);
        requestAnimationFrame(() => {
          setTimeout(resolve, 0);
        });
      });
    });
  });
});
