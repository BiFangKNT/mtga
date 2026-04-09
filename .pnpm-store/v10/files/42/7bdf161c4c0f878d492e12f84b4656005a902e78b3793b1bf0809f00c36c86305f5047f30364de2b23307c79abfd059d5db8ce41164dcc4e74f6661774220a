import { H as HeadSafe } from './shared/unhead.MXxTEjru.mjs';
import { U as Unhead, R as ResolvableHead, s as HeadEntryOptions, p as ActiveHeadEntry, a8 as UseSeoMetaInput, C as CreateHeadOptions } from './shared/unhead.DKj0fe9v.mjs';
export { u as useScript } from './shared/unhead.D1Xv45s3.mjs';
import 'hookable';

declare function useHead<T extends Unhead<any>, I = ResolvableHead>(unhead: T, input?: ResolvableHead, options?: HeadEntryOptions): ActiveHeadEntry<I>;
declare function useHeadSafe<T extends Unhead<any>>(unhead: T, input?: HeadSafe, options?: HeadEntryOptions): ActiveHeadEntry<HeadSafe>;
declare function useSeoMeta<T extends Unhead<any>>(unhead: T, input?: UseSeoMetaInput, options?: HeadEntryOptions): ActiveHeadEntry<UseSeoMetaInput>;
/**
 * @deprecated use `useHead` instead. Advanced use cases should tree shake using import.meta.* if statements.
 */
declare function useServerHead<T extends Unhead<any>>(unhead: T, input?: Parameters<T['push']>[0], options?: Omit<HeadEntryOptions, 'mode'>): ReturnType<T['push']>;
/**
 * @deprecated use `useHeadSafe` instead. Advanced use cases should tree shake using import.meta.* if statements.
 */
declare function useServerHeadSafe<T extends Unhead<any>>(unhead: T, input?: HeadSafe, options?: Omit<HeadEntryOptions, 'mode'>): ActiveHeadEntry<HeadSafe>;
/**
 * @deprecated use `useSeoMeta` instead. Advanced use cases should tree shake using import.meta.* if statements.
 */
declare function useServerSeoMeta<T extends Unhead<any>>(unhead: T, input?: UseSeoMetaInput, options?: Omit<HeadEntryOptions, 'mode'>): ActiveHeadEntry<UseSeoMetaInput>;

/**
 * @deprecated use `createUnhead` instead
 */
declare function createHeadCore<T = ResolvableHead>(resolvedOptions?: CreateHeadOptions): Unhead<T>;
/**
 * Creates a core instance of unhead. Does not provide a global ctx for composables to work
 * and does not register DOM plugins.
 */
declare function createUnhead<T = ResolvableHead>(resolvedOptions?: CreateHeadOptions): Unhead<T>;

export { createHeadCore, createUnhead, useHead, useHeadSafe, useSeoMeta, useServerHead, useServerHeadSafe, useServerSeoMeta };
