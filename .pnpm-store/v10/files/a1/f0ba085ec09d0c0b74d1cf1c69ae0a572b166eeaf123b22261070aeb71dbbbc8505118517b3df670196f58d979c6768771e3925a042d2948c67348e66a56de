import type { Ref } from 'vue';
export type Politeness = 'assertive' | 'polite' | 'off';
export type NuxtRouteAnnouncerOpts = {
    /** @default 'polite' */
    politeness?: Politeness;
};
export type RouteAnnouncer = {
    message: Ref<string>;
    politeness: Ref<Politeness>;
    set: (message: string, politeness?: Politeness) => void;
    polite: (message: string) => void;
    assertive: (message: string) => void;
    _cleanup: () => void;
};
/**
 * composable to handle the route announcer
 * @since 3.12.0
 */
export declare function useRouteAnnouncer(opts?: NuxtRouteAnnouncerOpts): Omit<RouteAnnouncer, '_cleanup'>;
