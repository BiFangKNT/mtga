import { Plugin } from 'vite';
import { StackFrame } from 'error-stack-parser-es';
import { V as ViteInspectOptions } from './shared/vite-plugin-inspect.CtoQ7j4S.mjs';
export { F as FilterPattern } from './shared/vite-plugin-inspect.CtoQ7j4S.mjs';

interface TransformInfo {
    name: string;
    result?: string;
    start: number;
    end: number;
    order?: string;
    sourcemaps?: any;
    error?: ParsedError;
}
interface ParsedError {
    message: string;
    stack: StackFrame[];
    raw?: any;
}
interface ModuleInfo {
    id: string;
    plugins: {
        name: string;
        transform?: number;
        resolveId?: number;
    }[];
    deps: string[];
    importers: string[];
    virtual: boolean;
    totalTime: number;
    invokeCount: number;
    sourceSize: number;
    distSize: number;
}
type ModulesList = ModuleInfo[];
interface ModuleTransformInfo {
    resolvedId: string;
    transforms: TransformInfo[];
}
interface PluginMetricInfo {
    name: string;
    enforce?: string;
    transform: {
        invokeCount: number;
        totalTime: number;
    };
    resolveId: {
        invokeCount: number;
        totalTime: number;
    };
}
interface ServerMetrics {
    middleware?: Record<string, {
        name: string;
        self: number;
        total: number;
    }[]>;
}
interface SerializedPlugin {
    name: string;
    enforce?: string;
    resolveId: string;
    load: string;
    transform: string;
    generateBundle: string;
    handleHotUpdate: string;
    api: string;
}
interface InstanceInfo {
    root: string;
    /**
     * Vite instance ID
     */
    vite: string;
    /**
     * Environment names
     */
    environments: string[];
    /**
     * Plugins
     */
    plugins: SerializedPlugin[];
    /**
     * Environment plugins, the index of the plugin in the `plugins` array
     */
    environmentPlugins: Record<string, number[]>;
}
interface Metadata {
    instances: InstanceInfo[];
    embedded?: boolean;
}
interface RpcFunctions {
    getMetadata: () => Promise<Metadata>;
    getModulesList: (query: QueryEnv) => Promise<ModulesList>;
    getModuleTransformInfo: (query: QueryEnv, id: string, clear?: boolean) => Promise<ModuleTransformInfo>;
    getPluginMetrics: (query: QueryEnv) => Promise<PluginMetricInfo[]>;
    getServerMetrics: (query: QueryEnv) => Promise<ServerMetrics>;
    resolveId: (query: QueryEnv, id: string) => Promise<string>;
    onModuleUpdated: () => Promise<void>;
}
interface QueryEnv {
    /**
     * Vite instance ID
     */
    vite: string;
    /**
     * Environment name
     */
    env: string;
}

interface ViteInspectAPI {
    rpc: RpcFunctions;
}
declare function PluginInspect(options?: ViteInspectOptions): Plugin;

export { ViteInspectOptions, PluginInspect as default };
export type { ViteInspectAPI };
