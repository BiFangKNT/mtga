import type { QuoteStyle, RootResult, NameResult, BaseNode } from './RootResult.js';
import type { Node } from 'estree';
/**
 * A parse sub result that might not be a valid type expression on its own.
 */
export type NonRootResult = RootResult | PropertyResult | ObjectFieldResult | JsdocObjectFieldResult | KeyValueResult | MappedTypeResult | IndexSignatureResult | TypeParameterResult | CallSignatureResult | ConstructorSignatureResult | MethodSignatureResult | IndexedAccessIndexResult | ComputedPropertyResult | ComputedMethodResult;
export interface ObjectFieldResult extends BaseNode {
    type: 'JsdocTypeObjectField';
    key: string | MappedTypeResult | IndexSignatureResult | ComputedPropertyResult | ComputedMethodResult;
    right: RootResult | undefined;
    optional: boolean;
    readonly: boolean;
    meta: {
        quote: QuoteStyle | undefined;
        postColonSpacing?: string;
        postKeySpacing?: string;
        postOptionalSpacing?: string;
    };
}
export interface JsdocObjectFieldResult extends BaseNode {
    type: 'JsdocTypeJsdocObjectField';
    left: RootResult;
    right: RootResult;
}
export interface PropertyResult extends BaseNode {
    type: 'JsdocTypeProperty';
    value: string;
    meta: {
        quote: QuoteStyle | undefined;
    };
}
/**
 * A key value pair represented by a `:`. Can occur as a named parameter of a {@link FunctionResult} or as an entry for
 * an {@link TupleResult}. Is a {@link NonRootResult}.
 */
export interface KeyValueResult extends BaseNode {
    type: 'JsdocTypeKeyValue';
    key: string;
    right: RootResult | undefined;
    optional: boolean;
    variadic: boolean;
    meta?: {
        postKeySpacing: string;
        postOptionalSpacing: string;
        postVariadicSpacing: string;
        postColonSpacing: string;
    };
}
export interface IndexSignatureResult extends BaseNode {
    type: 'JsdocTypeIndexSignature';
    key: string;
    right: RootResult;
}
export interface MappedTypeResult extends BaseNode {
    type: 'JsdocTypeMappedType';
    key: string;
    right: RootResult;
}
export interface TypeParameterResult extends BaseNode {
    type: 'JsdocTypeTypeParameter';
    defaultValue?: RootResult;
    name: NameResult;
    constraint?: RootResult;
    meta?: {
        defaultValueSpacing: string;
    };
}
export interface CallSignatureResult extends BaseNode {
    type: 'JsdocTypeCallSignature';
    parameters: Array<RootResult | KeyValueResult>;
    returnType: RootResult;
    typeParameters?: TypeParameterResult[];
    meta?: {
        parameterSpacing: string;
        typeParameterSpacing: string;
        postGenericSpacing: string;
        preReturnMarkerSpacing?: string;
        postReturnMarkerSpacing?: string;
    };
}
export interface ConstructorSignatureResult extends BaseNode {
    type: 'JsdocTypeConstructorSignature';
    parameters: Array<RootResult | KeyValueResult>;
    returnType: RootResult;
    typeParameters?: TypeParameterResult[];
    meta?: {
        parameterSpacing: string;
        typeParameterSpacing: string;
        postNewSpacing: string;
        postGenericSpacing: string;
        preReturnMarkerSpacing?: string;
        postReturnMarkerSpacing?: string;
    };
}
export interface MethodSignatureResult extends BaseNode {
    type: 'JsdocTypeMethodSignature';
    name: string;
    meta: {
        quote: QuoteStyle | undefined;
        parameterSpacing?: string;
        typeParameterSpacing?: string;
        postMethodNameSpacing?: string;
        postGenericSpacing?: string;
        preReturnMarkerSpacing?: string;
        postReturnMarkerSpacing?: string;
    };
    parameters: Array<RootResult | KeyValueResult>;
    returnType: RootResult;
    typeParameters?: TypeParameterResult[];
}
export interface IndexedAccessIndexResult extends BaseNode {
    type: 'JsdocTypeIndexedAccessIndex';
    right: RootResult;
}
export interface ComputedPropertyResult extends BaseNode {
    type: 'JsdocTypeComputedProperty';
    value: RootResult | Node;
}
export interface ComputedMethodResult extends BaseNode {
    type: 'JsdocTypeComputedMethod';
    value: RootResult | Node;
    optional: boolean;
    parameters: Array<RootResult | KeyValueResult>;
    returnType: RootResult;
    typeParameters?: TypeParameterResult[];
    meta?: {
        parameterSpacing: string;
        typeParameterSpacing: string;
        postGenericSpacing: string;
        preReturnMarkerSpacing?: string;
        postReturnMarkerSpacing?: string;
    };
}
