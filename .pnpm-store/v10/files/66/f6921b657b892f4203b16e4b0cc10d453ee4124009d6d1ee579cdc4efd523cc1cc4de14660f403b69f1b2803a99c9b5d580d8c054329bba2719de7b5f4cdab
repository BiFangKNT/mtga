import type { Ref } from 'vue';
export type AnnouncerPoliteness = 'assertive' | 'polite' | 'off';
export type NuxtAnnouncerOpts = {
    /** @default 'polite' */
    politeness?: AnnouncerPoliteness;
};
export type NuxtAnnouncer = {
    message: Ref<string>;
    politeness: Ref<AnnouncerPoliteness>;
    set: (message: string, politeness?: AnnouncerPoliteness) => void;
    polite: (message: string) => void;
    assertive: (message: string) => void;
    _cleanup: () => void;
};
/**
 * Composable for announcing messages to screen readers
 * @since 3.17.0
 * @example
 * const { polite, assertive } = useAnnouncer()
 * polite('Item saved successfully')
 * assertive('Error: Form is invalid')
 */
export declare function useAnnouncer(opts?: NuxtAnnouncerOpts): Omit<NuxtAnnouncer, '_cleanup'>;
