import type { Storage } from "unstorage";
export declare const payloadCache: Storage | null;
export declare const islandCache: Storage | null;
export declare const islandPropCache: Storage | null;
export declare const sharedPrerenderPromises: Map<string, Promise<any>> | null;
interface SharedPrerenderCache {
	get<T = unknown>(key: string): Promise<T> | undefined;
	set<T>(key: string, value: Promise<T>): Promise<void>;
}
export declare const sharedPrerenderCache: SharedPrerenderCache | null;
export {};
