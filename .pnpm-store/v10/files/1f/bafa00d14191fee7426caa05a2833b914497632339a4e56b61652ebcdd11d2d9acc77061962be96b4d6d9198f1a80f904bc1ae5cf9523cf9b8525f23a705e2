import type { AsyncComponentLoader, Component, ComponentPublicInstance, DefineComponent } from 'vue';
type LazyHydrationComponent<T extends Component, Props> = T & DefineComponent<Props, {}, {}, {}, {}, {}, {}, {
    hydrated: () => void;
}>;
export declare function defineLazyHydrationComponent<T extends Component = {
    new (): ComponentPublicInstance;
}>(strategy: 'visible', source: AsyncComponentLoader<T>): LazyHydrationComponent<T, {
    hydrateOnVisible?: IntersectionObserverInit | true;
}>;
export declare function defineLazyHydrationComponent<T extends Component = {
    new (): ComponentPublicInstance;
}>(strategy: 'idle', source: AsyncComponentLoader<T>): LazyHydrationComponent<T, {
    hydrateOnIdle?: number | true;
}>;
export declare function defineLazyHydrationComponent<T extends Component = {
    new (): ComponentPublicInstance;
}>(strategy: 'interaction', source: AsyncComponentLoader<T>): LazyHydrationComponent<T, {
    hydrateOnInteraction?: keyof HTMLElementEventMap | Array<keyof HTMLElementEventMap>;
}>;
export declare function defineLazyHydrationComponent<T extends Component = {
    new (): ComponentPublicInstance;
}>(strategy: 'mediaQuery', source: AsyncComponentLoader<T>): LazyHydrationComponent<T, {
    hydrateOnMediaQuery: string;
}>;
export declare function defineLazyHydrationComponent<T extends Component = {
    new (): ComponentPublicInstance;
}>(strategy: 'if', source: AsyncComponentLoader<T>): LazyHydrationComponent<T, {
    hydrateWhen: boolean;
}>;
export declare function defineLazyHydrationComponent<T extends Component = {
    new (): ComponentPublicInstance;
}>(strategy: 'time', source: AsyncComponentLoader<T>): LazyHydrationComponent<T, {
    hydrateAfter: number | true;
}>;
export declare function defineLazyHydrationComponent<T extends Component = {
    new (): ComponentPublicInstance;
}>(strategy: 'never', source: AsyncComponentLoader<T>): LazyHydrationComponent<T, {
    hydrateNever?: true;
}>;
export {};
