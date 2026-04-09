interface CacheItem {
    date: Date;
    value: any;
}
export declare function invalidateByModifiedDate(cache: CacheItem, path: string | undefined): boolean;
export declare function withCache<Result>(key: string, path: string | undefined, callback: () => Result, invalidate?: (cache: CacheItem, path: string | undefined) => boolean): Result;
export declare function withCache<Result>(key: string, path: string | undefined, callback: () => Promise<Result>, invalidate?: (cache: CacheItem, path: string | undefined) => boolean): Promise<Result>;
export {};
//# sourceMappingURL=cache.d.ts.map