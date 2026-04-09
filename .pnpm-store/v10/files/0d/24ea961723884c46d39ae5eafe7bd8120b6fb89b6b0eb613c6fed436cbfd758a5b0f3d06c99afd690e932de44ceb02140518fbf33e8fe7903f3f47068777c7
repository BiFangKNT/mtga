import type { KeyValueResult, NonRootResult } from './NonRootResult.js';
import type { RootResult, BaseNode } from './RootResult.js';
export type IntermediateResult = NonRootResult | ParameterList | ReadonlyProperty;
export interface ParameterList extends BaseNode {
    type: 'JsdocTypeParameterList';
    elements: Array<KeyValueResult | RootResult>;
}
export interface ReadonlyProperty extends BaseNode {
    type: 'JsdocTypeReadonlyProperty';
    element: IntermediateResult;
}
