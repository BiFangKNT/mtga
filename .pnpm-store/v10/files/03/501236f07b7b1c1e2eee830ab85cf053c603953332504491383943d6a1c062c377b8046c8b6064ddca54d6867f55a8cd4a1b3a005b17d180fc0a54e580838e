import type {
  JsdocObjectFieldResult,
  KeyValueResult,
  ObjectFieldResult,
  PropertyResult,
  TypeParameterResult,
  CallSignatureResult,
  ConstructorSignatureResult,
  MethodSignatureResult,
  IndexedAccessIndexResult,
  ComputedPropertyResult,
  ComputedMethodResult
} from './NonRootResult.js'

export interface Location {
  loc?: {
    end: {
      column: number,
      line: number,
    },
    start: {
      column: number,
      line: number
    }
  }
}

export interface Range {
  range?: [number, number]
}

export interface BaseNode extends Range, Location {}

/**
 * A parse result that corresponds to a valid type expression.
 */
export type RootResult =
  NameResult
  | InferResult
  | UnionResult
  | GenericResult
  | StringValueResult
  | NullResult
  | UndefinedResult
  | AnyResult
  | UnknownResult
  | FunctionResult
  | ObjectResult
  | NamePathResult
  | SymbolResult
  | TypeOfResult
  | KeyOfResult
  | ImportResult
  | TupleResult
  | SpecialNamePath
  | OptionalResult<RootResult>
  | NullableResult<RootResult>
  | NotNullableResult<RootResult>
  | VariadicResult<RootResult>
  | ParenthesisResult
  | IntersectionResult
  | NumberResult
  | PredicateResult
  | AssertsResult
  | ReadonlyArrayResult
  | AssertsPlainResult
  | ConditionalResult
  | TemplateLiteralResult

export type QuoteStyle = 'single' | 'double'

/**
 * `element` is optional.
 */
export interface OptionalResult<T extends RootResult> extends BaseNode {
  type: 'JsdocTypeOptional'
  element: T
  meta: {
    position: 'prefix' | 'suffix'
  }
}

/**
 * A nullable type.
 */
export interface NullableResult<T extends RootResult> extends BaseNode {
  type: 'JsdocTypeNullable'
  element: T
  meta: {
    position: 'prefix' | 'suffix'
  }
}

/**
 * A not nullable type.
 */
export interface NotNullableResult<T extends RootResult> extends BaseNode {
  type: 'JsdocTypeNotNullable'
  element: T
  meta: {
    position: 'prefix' | 'suffix'
  }
}

/**
 * A rest or spread parameter. It can either occur in `@param` tags or as last parameter of a function,
 * or it is a spread tuple or object type and can occur inside these. For any mode that is not `jsdoc` this can
 * only occur in position `'suffix'`.
 */
export interface VariadicResult<T extends RootResult> extends BaseNode {
  type: 'JsdocTypeVariadic'
  element?: T
  meta: {
    position: 'prefix' | 'suffix' | undefined
    squareBrackets: boolean
  }
}

/**
 * A type name.
 */
export interface NameResult extends BaseNode {
  type: 'JsdocTypeName'
  value: string
}

/**
 * A TypeScript `infer` type parameter within a generic argument list.
 * Represents the `infer X` construct when it appears as a generic argument
 * (e.g. `Map<any, infer V>`) or alongside other parameters.
 */
export interface InferResult extends BaseNode {
  type: 'JsdocTypeInfer'
  element: NameResult
}

/**
 * A type union.
 */
export interface UnionResult extends BaseNode {
  type: 'JsdocTypeUnion'
  elements: RootResult[]
  meta?: {
    spacing: string
  }
}

/**
 * A generic type. The property `left` is the generic type that has `elements` as type values for its type parameters.
 * Array types that are written as `Type[]` always have the name `Array` as the `left` type and `elements` will contain
 * only one element (in this case the name `Type`). To differentiate `Type[]` and `Array<Type>` there is the meta
 * property
 * `brackets`.
 */
export interface GenericResult extends BaseNode {
  type: 'JsdocTypeGeneric'
  left: RootResult
  elements: RootResult[]
  meta: {
    brackets: 'angle' | 'square'
    dot: boolean,
    elementSpacing?: string
  }
}

/**
 * A string value as a type.
 */
export interface StringValueResult extends BaseNode {
  type: 'JsdocTypeStringValue'
  value: string
  meta: {
    quote: QuoteStyle
  }
}

/**
 * The `null` type.
 */
export interface NullResult extends BaseNode {
  type: 'JsdocTypeNull'
}

/**
 * The `undefined` type.
 */
export interface UndefinedResult extends BaseNode {
  type: 'JsdocTypeUndefined'
}

/**
 * The `any` type, represented by `*` (`any` is parsed as a name).
 */
export interface AnyResult extends BaseNode {
  type: 'JsdocTypeAny'
}

/**
 * The unknown type, represented by `?` (`unknown` is parsed as a name).
 */
export interface UnknownResult extends BaseNode {
  type: 'JsdocTypeUnknown'
}

/**
 * A function type. Has `parameters` which can be named, if the grammar supports it. Some grammars only allow named
 * `this` and `new` parameters. Named parameters are returned as {@link KeyValueResult}s. It can have a `returnType`.
 * It can be a normal function type or an arrow, which is indicated by `arrow`. If `parenthesis` is false, it is any
 * kind of function without specified parameters or return type.
 */
export interface FunctionResult extends BaseNode {
  type: 'JsdocTypeFunction'
  parameters: Array<RootResult | KeyValueResult>
  returnType?: RootResult
  constructor: boolean
  arrow: boolean
  parenthesis: boolean
  typeParameters?: TypeParameterResult[]
  meta?: {
    parameterSpacing: string
    typeParameterSpacing: string
    preReturnMarkerSpacing: string
    postReturnMarkerSpacing: string
    postGenericSpacing?: string
  }
}

/**
 * An object type. Contains entries which can be {@link KeyValueResult}s or {@link NameResult}s. In most grammars the
 * keys need to be {@link NameResult}s. In some grammars it possible that an entry is only a {@link RootResult} or a
 * {@link NumberResult} without a key. The separator is `'comma'` by default.
 */
export interface ObjectResult extends BaseNode {
  type: 'JsdocTypeObject'
  elements: Array<ObjectFieldResult | JsdocObjectFieldResult | CallSignatureResult | ConstructorSignatureResult | MethodSignatureResult | ComputedPropertyResult | ComputedMethodResult>
  meta: {
    bracketSpacing?: string,
    separator: 'comma' | 'semicolon' | 'linebreak' | 'comma-and-linebreak' | 'semicolon-and-linebreak' | undefined
    separatorForSingleObjectField?: boolean
    trailingPunctuation?: boolean
    propertyIndent?: string
  }
}

export type SpecialNamePathType = 'module' | 'event' | 'external'

/**
 * A module type. Often this is a `left` type of {@link NamePathResult}.
 */
export interface SpecialNamePath<Type extends SpecialNamePathType = SpecialNamePathType> extends BaseNode {
  type: 'JsdocTypeSpecialNamePath'
  value: string
  specialType: Type
  meta: {
    quote: QuoteStyle | undefined
  }
}

/**
 * A name path type. This can be a property path separated by `.` or an inner or static member (`~`, `#`).
 */
export interface NamePathResult extends BaseNode {
  type: 'JsdocTypeNamePath'
  left: RootResult
  right: PropertyResult | SpecialNamePath<'event'> | IndexedAccessIndexResult
  pathType: 'inner' | 'instance' | 'property' | 'property-brackets'
}

/**
 * A symbol type. Only available in `jsdoc` mode.
 */
export interface SymbolResult extends BaseNode {
  type: 'JsdocTypeSymbol'
  value: string
  element?: NumberResult | NameResult | VariadicResult<NameResult>
}

/**
 * A typeof type. The `element` normally should be a name.
 */
export interface TypeOfResult extends BaseNode {
  type: 'JsdocTypeTypeof'
  element: RootResult
}

/**
 * A keyof type. The `element` normally should be a name.
 */
export interface KeyOfResult extends BaseNode {
  type: 'JsdocTypeKeyof'
  element: RootResult
}

/**
 * An import type. The `element` is {@link StringValueResult} representing the path. Often the `left` side of an
 * {@link NamePathResult}.
 */
export interface ImportResult extends BaseNode {
  type: 'JsdocTypeImport'
  element: StringValueResult
}

/**
 * A tuple type containing multiple `elements`.
 */
export interface TupleResult extends BaseNode {
  type: 'JsdocTypeTuple'
  elements: RootResult[] | KeyValueResult[],
  meta?: {
    elementSpacing: string
  }
}

/**
 * A type enclosed in parenthesis. Often {@link UnionResult}s ot {@link IntersectionResult}s.
 */
export interface ParenthesisResult extends BaseNode {
  type: 'JsdocTypeParenthesis'
  element: RootResult
}

/**
 * An intersection type.
 */
export interface IntersectionResult extends BaseNode {
  type: 'JsdocTypeIntersection'
  elements: RootResult[]
}

/**
 * A number. Can be the key of an {@link ObjectResult} entry or the parameter of a {@link SymbolResult}.
 * Is a {@link NonRootResult}.
 */
export interface NumberResult extends BaseNode {
  type: 'JsdocTypeNumber'
  value: number
}

/**
 * A typescript predicate. Is used in return annotations like this: `@return {x is string}`.
 */
export interface PredicateResult extends BaseNode {
  type: 'JsdocTypePredicate'
  left: NameResult
  right: RootResult
}

/**
 * An asserts result. Is used like this: `@return {asserts foo is Bar}`
 */
export interface AssertsResult extends BaseNode {
  type: 'JsdocTypeAsserts'
  left: NameResult
  right: RootResult
}

/**
 * A TypeScript readonly modifier. Is used like this: `readonly string[]`.
 */
export interface ReadonlyArrayResult extends BaseNode {
  type: 'JsdocTypeReadonlyArray'
  element: RootResult
}

/**
 * An asserts result without `is`. Is used like this: `@return {asserts foo}`
 */
export interface AssertsPlainResult extends BaseNode {
  type: 'JsdocTypeAssertsPlain'
  element: NameResult
}

/**
 * A TypeScript conditional. Is used like this: `A extends B ? C : D`.
 */
export interface ConditionalResult extends BaseNode {
  type: 'JsdocTypeConditional'
  checksType: RootResult
  extendsType: RootResult
  trueType: RootResult
  falseType: RootResult
}

/**
 * A TypeScript template literal. Is used like: `\`someText${someType}\``
 */
export interface TemplateLiteralResult extends BaseNode {
  type: 'JsdocTypeTemplateLiteral'
  literals: string[],
  interpolations: RootResult[]
}
