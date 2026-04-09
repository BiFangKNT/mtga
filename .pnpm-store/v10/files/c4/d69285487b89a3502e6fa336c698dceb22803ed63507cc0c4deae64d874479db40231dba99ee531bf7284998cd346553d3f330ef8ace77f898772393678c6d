interface Preview {
    enabled: boolean;
    state: Record<any, unknown>;
    _initialized?: boolean;
}
/**
 * Options for configuring preview mode.
 */
interface PreviewModeOptions<S> {
    /**
     * A function that determines whether preview mode should be enabled based on the current state.
     * @param {Record<any, unknown>} state - The state of the preview.
     * @returns {boolean} A boolean indicating whether the preview mode is enabled.
     */
    shouldEnable?: (state: Preview['state']) => boolean;
    /**
     * A function that retrieves the current state.
     * The `getState` function will append returned values to current state, so be careful not to accidentally overwrite important state.
     * @param {Record<any, unknown>} state - The preview state.
     * @returns {Record<any, unknown>} The preview state.
     */
    getState?: (state: Preview['state']) => S;
    /**
     * A function to be called when the preview mode is enabled.
     */
    onEnable?: () => void;
    /**
     * A function to be called when the preview mode is disabled.
     */
    onDisable?: () => void;
}
type EnteredState = Record<any, unknown> | null | undefined | void;
/** @since 3.11.0 */
export declare function usePreviewMode<S extends EnteredState>(options?: PreviewModeOptions<S>): {
    enabled: import("vue").Ref<boolean, boolean>;
    state: S extends void ? Preview["state"] : (NonNullable<S> & Preview["state"]);
};
export {};
