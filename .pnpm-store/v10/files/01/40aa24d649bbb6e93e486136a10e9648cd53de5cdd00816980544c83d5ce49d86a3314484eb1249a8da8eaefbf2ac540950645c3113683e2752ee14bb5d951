import type { ActiveHeadEntry, UseHeadInput, UseHeadOptions, UseHeadSafeInput, UseSeoMetaInput, VueHeadClient } from '@unhead/vue/types';
import type { NuxtApp } from '#app/nuxt';
/**
 * Injects the head client from the Nuxt context or Vue inject.
 */
export declare function injectHead(nuxtApp?: NuxtApp): VueHeadClient;
interface NuxtUseHeadOptions extends UseHeadOptions {
    nuxt?: NuxtApp;
}
export declare function useHead(input: UseHeadInput, options?: NuxtUseHeadOptions): ActiveHeadEntry<UseHeadInput>;
export declare function useHeadSafe(input: UseHeadSafeInput, options?: NuxtUseHeadOptions): ActiveHeadEntry<UseHeadSafeInput>;
export declare function useSeoMeta(input: UseSeoMetaInput, options?: NuxtUseHeadOptions): ActiveHeadEntry<UseSeoMetaInput>;
/**
 * @deprecated Use `useHead` instead and wrap with `if (import.meta.server)`
 */
export declare function useServerHead(input: UseHeadInput, options?: NuxtUseHeadOptions): ActiveHeadEntry<UseHeadInput>;
/**
 * @deprecated Use `useHeadSafe` instead and wrap with `if (import.meta.server)`
 */
export declare function useServerHeadSafe(input: UseHeadSafeInput, options?: NuxtUseHeadOptions): ActiveHeadEntry<UseHeadSafeInput>;
/**
 * @deprecated Use `useSeoMeta` instead and wrap with `if (import.meta.server)`
 */
export declare function useServerSeoMeta(input: UseSeoMetaInput, options?: NuxtUseHeadOptions): ActiveHeadEntry<UseSeoMetaInput>;
export {};
