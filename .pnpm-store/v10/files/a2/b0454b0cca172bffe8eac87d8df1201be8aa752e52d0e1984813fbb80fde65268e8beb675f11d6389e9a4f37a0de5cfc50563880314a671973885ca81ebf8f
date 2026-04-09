import type { ConflictingClasses } from "./conflicting-classes.js";
export declare function getConflictingClasses(context: any, classes: string[]): Promise<ConflictingClasses>;
export type StyleRule = {
    kind: "rule";
    nodes: AstNode[];
    selector: string;
};
export type AtRule = {
    kind: "at-rule";
    name: string;
    nodes: AstNode[];
    params: string;
};
export type Declaration = {
    important: boolean;
    kind: "declaration";
    property: string;
    value: string | undefined;
};
export type Comment = {
    kind: "comment";
    value: string;
};
export type Context = {
    context: Record<string, boolean | string>;
    kind: "context";
    nodes: AstNode[];
};
export type AtRoot = {
    kind: "at-root";
    nodes: AstNode[];
};
export type Rule = AtRule | StyleRule;
export type AstNode = AtRoot | AtRule | Comment | Context | Declaration | StyleRule;
//# sourceMappingURL=conflicting-classes.async.v4.d.ts.map