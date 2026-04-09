import { AlgoFn } from "./algo";
import { Rune } from "./runes";
import { FzfResultItem, BaseOptions, SyncOptions, AsyncOptions, Tiebreaker, Token, Selector } from "./types";
export type ArrayElement<ArrayType extends readonly unknown[]> = ArrayType extends readonly (infer ElementType)[] ? ElementType : never;
type SortAttrs<U> = {
    sort?: true;
    tiebreakers?: Tiebreaker<U>[];
} | {
    sort: false;
};
type BaseOptsToUse<U> = Omit<Partial<BaseOptions<U>>, "sort" | "tiebreakers"> & SortAttrs<U>;
type BaseOptionsTuple<U> = U extends string ? [options?: BaseOptsToUse<U>] : [options: BaseOptsToUse<U> & {
    selector: Selector<U>;
}];
export declare abstract class BaseFinder<L extends ReadonlyArray<any>> {
    runesList: Rune[][];
    items: L;
    readonly opts: BaseOptions<ArrayElement<L>>;
    algoFn: AlgoFn;
    constructor(list: L, ...optionsTuple: BaseOptionsTuple<ArrayElement<L>>);
}
export type SyncOptsToUse<U> = BaseOptsToUse<U> & Partial<Pick<SyncOptions<U>, "match">>;
export type SyncOptionsTuple<U> = U extends string ? [options?: SyncOptsToUse<U>] : [options: SyncOptsToUse<U> & {
    selector: Selector<U>;
}];
export declare class SyncFinder<L extends ReadonlyArray<any>> extends BaseFinder<L> {
    readonly opts: SyncOptions<ArrayElement<L>>;
    constructor(list: L, ...optionsTuple: SyncOptionsTuple<ArrayElement<L>>);
    find(query: string): FzfResultItem<ArrayElement<L>>[];
}
export type AsyncOptsToUse<U> = BaseOptsToUse<U> & Partial<Pick<AsyncOptions<U>, "match">>;
export type AsyncOptionsTuple<U> = U extends string ? [options?: AsyncOptsToUse<U>] : [options: AsyncOptsToUse<U> & {
    selector: Selector<U>;
}];
export declare class AsyncFinder<L extends ReadonlyArray<any>> extends BaseFinder<L> {
    readonly opts: AsyncOptions<ArrayElement<L>>;
    token: Token;
    constructor(list: L, ...optionsTuple: AsyncOptionsTuple<ArrayElement<L>>);
    find(query: string): Promise<FzfResultItem<ArrayElement<L>>[]>;
}
export {};
