import { ParserOptions } from '@apidevtools/json-schema-ref-parser';
import { JSONSchema4 } from 'json-schema';

interface JSONSchema extends JSONSchema4 {
    /**
     * schema extension to support numeric enums
     */
    tsEnumNames?: string[];
    /**
     * schema extension to support custom types
     */
    tsType?: string;
    /**
     * property exists at least in https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.9.3
     */
    deprecated?: boolean;
}
declare const Parent: unique symbol;
interface LinkedJSONSchema extends JSONSchema {
    /**
     * A reference to this schema's parent node, for convenience.
     * `null` when this is the root schema.
     */
    [Parent]: LinkedJSONSchema | null;
    additionalItems?: boolean | LinkedJSONSchema;
    additionalProperties?: boolean | LinkedJSONSchema;
    items?: LinkedJSONSchema | LinkedJSONSchema[];
    definitions?: {
        [k: string]: LinkedJSONSchema;
    };
    properties?: {
        [k: string]: LinkedJSONSchema;
    };
    patternProperties?: {
        [k: string]: LinkedJSONSchema;
    };
    dependencies?: {
        [k: string]: LinkedJSONSchema | string[];
    };
    allOf?: LinkedJSONSchema[];
    anyOf?: LinkedJSONSchema[];
    oneOf?: LinkedJSONSchema[];
    not?: LinkedJSONSchema;
}
interface NormalizedJSONSchema extends LinkedJSONSchema {
    additionalItems?: boolean | NormalizedJSONSchema;
    additionalProperties: boolean | NormalizedJSONSchema;
    extends?: string[];
    items?: NormalizedJSONSchema | NormalizedJSONSchema[];
    $defs?: {
        [k: string]: NormalizedJSONSchema;
    };
    properties?: {
        [k: string]: NormalizedJSONSchema;
    };
    patternProperties?: {
        [k: string]: NormalizedJSONSchema;
    };
    dependencies?: {
        [k: string]: NormalizedJSONSchema | string[];
    };
    allOf?: NormalizedJSONSchema[];
    anyOf?: NormalizedJSONSchema[];
    oneOf?: NormalizedJSONSchema[];
    not?: NormalizedJSONSchema;
    required: string[];
    definitions: never;
    id: never;
}
interface EnumJSONSchema extends NormalizedJSONSchema {
    enum: any[];
}
interface NamedEnumJSONSchema extends NormalizedJSONSchema {
    tsEnumNames: string[];
}
interface CustomTypeJSONSchema extends NormalizedJSONSchema {
    tsType: string;
}

declare function isSafeIdentifier(string: string): boolean;
/**
 * Convert a string that might contain spaces or special characters to one that
 * can safely be used as a TypeScript interface or enum name.
 */
declare function toSafeIdentifier(string: string): string;
declare function normalizeIdentifier(string: string): Capitalize<string>;

interface Options {
    /**
     * [$RefParser](https://github.com/BigstickCarpet/json-schema-ref-parser) Options, used when resolving `$ref`s
     */
    $refOptions: ParserOptions;
    /**
     * Default value for additionalProperties, when it is not explicitly set.
     */
    additionalProperties: boolean;
    /**
     * Root directory for resolving [`$ref`](https://tools.ietf.org/id/draft-pbryan-zyp-json-ref-03.html)s.
     */
    cwd: string;
    /**
     * Declare external schemas referenced via `$ref`?
     */
    declareExternallyReferenced: boolean;
    /**
     * Prepend enums with [`const`](https://www.typescriptlang.org/docs/handbook/enums.html#computed-and-constant-members)?
     */
    enableConstEnums: boolean;
    /**
     * Ignore maxItems and minItems for `array` types, preventing tuples being generated.
     */
    ignoreMinAndMaxItems: boolean;
    /**
     * Maximum number of unioned tuples to emit when representing bounded-size array types,
     * before falling back to emitting unbounded arrays. Increase this to improve precision
     * of emitted types, decrease it to improve performance, or set it to `-1` to ignore
     * `minItems` and `maxItems`.
     */
    maxItems: number;
    /**
     * Append all index signatures with `| undefined` so that they are strictly typed.
     *
     * This is required to be compatible with `strictNullChecks`.
     */
    strictIndexSignatures: boolean;
    /**
     * Generate code for `definitions` that aren't referenced by the schema?
     */
    unreachableDefinitions: boolean;
    /**
     * Generate unknown type instead of any
     */
    unknownAny: boolean;
    /**
     * Custom function to provide a type name for a given schema
     */
    customName?: (schema: JSONSchema, keyNameFromDefinition: string | undefined) => string;
}
declare const DEFAULT_OPTIONS: Options;
declare function compile(schema: JSONSchema4, name: string, options?: Partial<Options>): Promise<string>;
declare class ValidationError extends Error {
}

export { DEFAULT_OPTIONS, ValidationError, compile, isSafeIdentifier, normalizeIdentifier, toSafeIdentifier };
export type { CustomTypeJSONSchema, EnumJSONSchema, JSONSchema, NamedEnumJSONSchema, Options };
