import { au as HeadTag, Q as UnheadMeta, ah as MetaFlat, R as ResolvableHead, P as PropResolver, U as Unhead, ar as TemplateParams } from './shared/unhead.DKj0fe9v.mjs';
import 'hookable';

declare const SelfClosingTags: Set<string>;
declare const DupeableTags: Set<string>;
declare const TagsWithInnerContent: Set<string>;
declare const HasElementTags: Set<string>;
declare const ValidHeadTags: Set<string>;
declare const UniqueTags: Set<string>;
declare const TagConfigKeys: Set<string>;
declare const ScriptNetworkEvents: Set<string>;
declare const UsesMergeStrategy: Set<string>;
declare const MetaTagsArrayable: Set<string>;

declare function isMetaArrayDupeKey(v: string): boolean;
declare function dedupeKey<T extends HeadTag>(tag: T): string | undefined;
declare function hashTag(tag: HeadTag): string;

declare function resolveMetaKeyType(key: string): keyof UnheadMeta;
declare function resolveMetaKeyValue(key: string): string;
declare function resolvePackedMetaObjectValue(value: string, key: string): string;
declare function unpackMeta<T extends MetaFlat>(input: T): Required<ResolvableHead>['meta'];

declare function normalizeProps(tag: HeadTag, input: Record<string, any>): HeadTag;
declare function normalizeEntryToTags(input: any, propResolvers: PropResolver[]): HeadTag[];

declare const sortTags: (a: HeadTag, b: HeadTag) => number;
declare function tagWeight<T extends HeadTag>(head: Unhead<any>, tag: T): number;

declare function processTemplateParams(s: string, p: TemplateParams, sep?: string, isJson?: boolean): string;

declare function walkResolver(val: any, resolve?: PropResolver, key?: string): any;

export { DupeableTags, HasElementTags, MetaTagsArrayable, ScriptNetworkEvents, SelfClosingTags, TagConfigKeys, TagsWithInnerContent, UniqueTags, UsesMergeStrategy, ValidHeadTags, dedupeKey, hashTag, isMetaArrayDupeKey, normalizeEntryToTags, normalizeProps, processTemplateParams, resolveMetaKeyType, resolveMetaKeyValue, resolvePackedMetaObjectValue, sortTags, tagWeight, unpackMeta, walkResolver };
