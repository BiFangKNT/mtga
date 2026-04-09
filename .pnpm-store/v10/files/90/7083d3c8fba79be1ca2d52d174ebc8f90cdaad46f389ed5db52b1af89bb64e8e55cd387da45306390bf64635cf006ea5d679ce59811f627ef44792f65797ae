import type { AllowedComponentProps, ComponentCustomProps, ComponentPublicInstance, KeepAliveProps, TransitionProps, VNode, VNodeProps } from 'vue';
import type { RouteLocationNormalizedLoaded, RouterViewProps } from 'vue-router';
import type { RouterViewSlotProps } from './utils.js';
export interface NuxtPageProps extends RouterViewProps {
    /**
     * Define global transitions for all pages rendered with the `NuxtPage` component.
     */
    transition?: boolean | TransitionProps;
    /**
     * Control state preservation of pages rendered with the `NuxtPage` component.
     */
    keepalive?: boolean | KeepAliveProps;
    /**
     * Control when the `NuxtPage` component is re-rendered.
     */
    pageKey?: string | ((route: RouteLocationNormalizedLoaded) => string);
}
declare const _default: {
    new (): {
        $props: AllowedComponentProps & ComponentCustomProps & VNodeProps & NuxtPageProps;
        $slots: {
            default?: (routeProps: RouterViewSlotProps) => VNode[];
        };
        /**
         * Reference to the page component instance
         */
        pageRef: Element | ComponentPublicInstance | null;
    };
};
export default _default;
