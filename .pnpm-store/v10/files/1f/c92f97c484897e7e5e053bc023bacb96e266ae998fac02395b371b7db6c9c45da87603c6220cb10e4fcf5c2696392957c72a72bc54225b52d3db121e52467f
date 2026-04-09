import type { Ref } from 'vue';
export type LoadingIndicatorOpts = {
    /** @default 2000 */
    duration: number;
    /** @default 200 */
    throttle: number;
    /** @default 500 */
    hideDelay: number;
    /** @default 400 */
    resetDelay: number;
    /**
     * You can provide a custom function to customize the progress estimation,
     * which is a function that receives the duration of the loading bar (above)
     * and the elapsed time. It should return a value between 0 and 100.
     */
    estimatedProgress?: (duration: number, elapsed: number) => number;
};
export type LoadingIndicator = {
    _cleanup: () => void;
    progress: Ref<number>;
    isLoading: Ref<boolean>;
    error: Ref<boolean>;
    start: (opts?: {
        force?: boolean;
    }) => void;
    set: (value: number, opts?: {
        force?: boolean;
    }) => void;
    finish: (opts?: {
        force?: boolean;
        error?: boolean;
    }) => void;
    clear: () => void;
};
/**
 * composable to handle the loading state of the page
 * @since 3.9.0
 */
export declare function useLoadingIndicator(opts?: Partial<LoadingIndicatorOpts>): Omit<LoadingIndicator, '_cleanup'>;
