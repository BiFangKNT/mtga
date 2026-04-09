import type { Rule } from "eslint";
export declare enum MatcherType {
    /** Matches all object keys that are strings. */
    ObjectKey = "objectKeys",
    /** Matches all object values that are strings. */
    ObjectValue = "objectValues",
    /** Matches all strings  that are not matched by another matcher. */
    String = "strings"
}
export type StringMatcher = {
    match: MatcherType.String;
};
export type ObjectKeyMatcher = {
    match: MatcherType.ObjectKey;
    pathPattern?: Regex;
};
export type ObjectValueMatcher = {
    match: MatcherType.ObjectValue;
    pathPattern?: Regex;
};
export type MatcherFunction<Node> = (node: unknown) => node is Node;
export type MatcherFunctions<Node> = MatcherFunction<Node>[];
export type Matcher = ObjectKeyMatcher | ObjectValueMatcher | StringMatcher;
export type Regex = string;
export type CalleeName = string;
export type CalleeMatchers = [callee: CalleeName, matchers: Matcher[]];
export type CalleeRegex = [containerRegex: Regex, literalRegex: Regex];
export type Callees = (CalleeMatchers | CalleeName | CalleeRegex)[];
export type CalleeOption = {
    callees: Callees;
};
export type VariableName = string;
export type VariableMatchers = [variable: VariableName, matchers: Matcher[]];
export type VariableRegex = [variableNameRegex: Regex, literalRegex: Regex];
export type Variables = (VariableMatchers | VariableName | VariableRegex)[];
export type VariableOption = {
    variables: Variables;
};
export type TagName = string;
export type TagMatchers = [tag: TagName, matchers: Matcher[]];
export type TagRegex = [tagRegex: Regex, literalRegex: Regex];
export type Tags = (TagMatchers | TagName | TagRegex)[];
export type TagOption = {
    tags: Tags;
};
export type AttributeName = string;
export type AttributeMatchers = [attribute: AttributeName, matchers: Matcher[]];
export type AttributeRegex = [attributeRegex: Regex, literalRegex: Regex];
export type Attributes = (AttributeMatchers | AttributeName | AttributeRegex)[];
export type AttributeOption = {
    attributes: Attributes;
};
export type NameConfig = AttributeName | CalleeName | VariableName;
export type RegexConfig = AttributeRegex | CalleeRegex | VariableRegex;
export type MatchersConfig = AttributeMatchers | CalleeMatchers | VariableMatchers;
export interface ESLintRule<Options extends [any] = [any]> {
    name: string;
    rule: Rule.RuleModule;
    options?: Options;
    settings?: Rule.RuleContext["settings"];
}
//# sourceMappingURL=rule.d.ts.map