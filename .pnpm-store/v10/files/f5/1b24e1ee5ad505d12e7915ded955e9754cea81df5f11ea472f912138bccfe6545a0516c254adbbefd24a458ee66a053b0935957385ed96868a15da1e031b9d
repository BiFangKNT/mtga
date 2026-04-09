import * as _nuxt_schema from '@nuxt/schema';
import { Nuxt } from '@nuxt/schema';

interface TelemetryOptions {
    debug: boolean;
    endpoint: string;
    seed: string;
    consent?: number;
    enabled: boolean;
}
interface Context {
    nuxt: Nuxt;
    cli: string;
    seed: string;
    projectHash: string;
    projectSession: string;
    nuxtVersion: string;
    nuxtMajorVersion: number;
    isEdge: boolean;
    nodeVersion: string;
    os: string;
    git?: {
        url: string;
    };
    environment: string | null;
    packageManager: string;
    concent: number;
}
interface Event {
    name: string;
    [key: string]: any;
}
type EventFactoryResult<T> = Promise<T> | T | Promise<T>[] | T[];
type EventFactory<T extends Event> = (context: Context, payload: any) => EventFactoryResult<T>;

declare class Telemetry {
    nuxt: Nuxt;
    options: Required<TelemetryOptions>;
    storage: any;
    _contextPromise?: Promise<Context>;
    events: Promise<EventFactoryResult<any>>[];
    eventFactories: Record<string, EventFactory<any>>;
    constructor(nuxt: Nuxt, options: Required<TelemetryOptions>);
    getContext(): Promise<Context>;
    createEvent(name: string, payload?: object): undefined | Promise<any>;
    _invokeEvent(name: string, eventFactory: EventFactory<any>, payload?: object): Promise<any>;
    getPublicContext(): Promise<Record<string, any>>;
    sendEvents(debug?: boolean): Promise<void>;
}

type ModuleOptions = TelemetryOptions;
interface ModuleHooks {
    'telemetry:setup': (telemetry: Telemetry) => void;
}
declare const _default: _nuxt_schema.NuxtModule<TelemetryOptions, TelemetryOptions, false>;

export { _default as default };
export type { ModuleHooks, ModuleOptions };
