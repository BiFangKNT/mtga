import type { HookCallback } from 'hookable';
import type { RuntimeNuxtHooks } from '../nuxt.js';
/**
 * Registers a runtime hook in a Nuxt application and ensures it is properly disposed of when the scope is destroyed.
 * @param name - The name of the hook to register.
 * @param fn - The callback function to be executed when the hook is triggered.
 * @since 3.14.0
 */
export declare function useRuntimeHook<THookName extends keyof RuntimeNuxtHooks>(name: THookName, fn: RuntimeNuxtHooks[THookName] extends HookCallback ? RuntimeNuxtHooks[THookName] : never): void;
