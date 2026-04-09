//#region src/deserialize.d.ts
/**
 * Returns a deserialized value from a serialized array of Records.
 * @param serialized a previously serialized value.
 */
declare function deserialize(serialized: any[]): any;
//#endregion
//#region src/json.d.ts
/**
 * Revive a previously stringified structured clone.
 * @param str previously stringified data as string.
 */
declare function parse<T = any>(str: string): T;
/**
 * Represent a structured clone value as string.
 * @param any some clone-able value to stringify.
 */
declare function stringify(any: any): string;
//#endregion
//#region src/serialize.d.ts
type SerializedRecord = [type: number | string, value?: any];
/**
 * Returns an array of serialized Records.
 */
declare function serialize(value: any, options?: {
  json?: boolean;
  lossy?: boolean;
}): SerializedRecord[];
//#endregion
//#region src/index.d.ts
/**
 * A pure implementation of the structured clone algorithm using serialize/deserialize.
 */
declare function structuredClone<T>(value: T, options?: {
  lossy?: boolean;
}): T;
//#endregion
export { deserialize, parse, serialize, stringify, structuredClone };