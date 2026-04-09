import { Plugin } from 'vite';

interface VueTracerOptions {
    /**
     * Enable this plugin or not, or only enable in certain environment.
     *
     * @default 'dev'
     */
    enabled?: boolean | 'dev' | 'prod';
    /**
     * Resolve the record entry path to relative path.
     * Normally, it should be true.
     *
     * @default true
     */
    resolveRecordEntryPath?: boolean;
    /**
     * Enable Vite DevTools integration.
     *
     * @default false
     */
    viteDevtools?: boolean;
}
declare function VueTracer(options?: VueTracerOptions): Plugin | undefined;

export { VueTracer, VueTracer as default };
