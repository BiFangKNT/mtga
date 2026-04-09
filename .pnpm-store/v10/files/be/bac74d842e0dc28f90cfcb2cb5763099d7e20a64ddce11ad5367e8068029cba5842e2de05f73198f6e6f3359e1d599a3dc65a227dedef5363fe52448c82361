import type { SyncFinder, AsyncFinder } from "./finders";
import { FzfResultItem, Token } from "./types";
export declare function basicMatch<U>(this: SyncFinder<ReadonlyArray<U>>, query: string): FzfResultItem<U>[];
export declare function extendedMatch<U>(this: SyncFinder<ReadonlyArray<U>>, query: string): FzfResultItem<U>[];
export declare function asyncBasicMatch<U>(this: AsyncFinder<ReadonlyArray<U>>, query: string, token: Token): Promise<FzfResultItem<U>[]>;
export declare function asyncExtendedMatch<U>(this: AsyncFinder<ReadonlyArray<U>>, query: string, token: Token): Promise<FzfResultItem<U>[]>;
