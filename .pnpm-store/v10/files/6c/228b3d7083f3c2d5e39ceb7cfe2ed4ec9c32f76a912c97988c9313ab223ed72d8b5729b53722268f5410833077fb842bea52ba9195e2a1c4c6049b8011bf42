import { EnvironmentOptions } from "vite";
import { ViteConfig } from "nuxt/schema";
import { NuxtBuilder } from "@nuxt/schema";

//#region src/vite.d.ts
declare const bundle: NuxtBuilder["bundle"];
//#endregion
//#region src/index.d.ts
declare module "nuxt/schema" {
  interface ViteOptions extends ViteConfig {
    $client?: EnvironmentOptions;
    $server?: EnvironmentOptions;
    viteNode?: {
      maxRetryAttempts?: number; /** in milliseconds */
      baseRetryDelay?: number; /** in milliseconds */
      maxRetryDelay?: number; /** in milliseconds */
      requestTimeout?: number;
    };
  }
}
//#endregion
export { bundle };