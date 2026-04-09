import { DocumentOptions } from "yaml";
import { VisitorKeys as VisitorKeys$1 } from "eslint-visitor-keys";
import { SourceCode } from "eslint";

//#region src/utils.d.ts
type YAMLVersion = NonNullable<DocumentOptions["version"]>;
type YAMLContentValue = string | number | boolean | null | YAMLContentValue[] | YAMLMappingValue;
type YAMLMappingValue = {
  [key: string]: YAMLContentValue;
  [key: number]: YAMLContentValue;
};
declare function getStaticYAMLValue(node: YAMLMapping | YAMLPair): YAMLMappingValue;
declare function getStaticYAMLValue(node: YAMLSequence): YAMLContentValue[];
declare function getStaticYAMLValue(node: YAMLScalar): string | number | boolean | null;
declare function getStaticYAMLValue(node: YAMLAlias | YAMLProgram | YAMLDocument | YAMLContent | YAMLPair | YAMLWithMeta): YAMLContentValue;
declare namespace ast_d_exports {
  export { Comment, Locations, Position, Range, SourceLocation, Token, YAMLAlias, YAMLAnchor, YAMLBlockFoldedScalar, YAMLBlockLiteralScalar, YAMLBlockMapping, YAMLBlockSequence, YAMLContent, YAMLDirective, YAMLDirectiveForTAG, YAMLDirectiveForUnknown, YAMLDirectiveForYAML, YAMLDocument, YAMLDoubleQuotedScalar, YAMLFlowMapping, YAMLFlowSequence, YAMLMapping, YAMLNode, YAMLPair, YAMLPlainScalar, YAMLProgram, YAMLScalar, YAMLSequence, YAMLSingleQuotedScalar, YAMLTag, YAMLWithMeta };
}
type Range = [number, number];
interface Locations {
  loc: SourceLocation;
  range: Range;
}
interface BaseYAMLNode extends Locations {
  type: string;
}
interface SourceLocation {
  start: Position;
  end: Position;
}
interface Token extends BaseYAMLNode {
  type: "Directive" | "Marker" | "Punctuator" | "Identifier" | "String" | "Boolean" | "Numeric" | "Null" | "BlockLiteral" | "BlockFolded";
  value: string;
}
interface Comment extends BaseYAMLNode {
  type: "Line" | "Block";
  value: string;
}
interface Position {
  /** >= 1 */
  line: number;
  /** >= 0 */
  column: number;
}
type YAMLNode = YAMLProgram | YAMLDocument | YAMLDirective | YAMLContent | YAMLPair | YAMLWithMeta | YAMLAnchor | YAMLTag;
interface YAMLProgram extends BaseYAMLNode {
  type: "Program";
  body: YAMLDocument[];
  sourceType: "module";
  comments: Comment[];
  tokens: Token[];
  parent: null;
}
interface YAMLDocument extends BaseYAMLNode {
  type: "YAMLDocument";
  directives: YAMLDirective[];
  content: YAMLContent | YAMLWithMeta | null;
  parent: YAMLProgram;
  anchors: {
    [key: string]: YAMLAnchor[];
  };
  version: YAMLVersion;
}
interface BaseYAMLDirective extends BaseYAMLNode {
  type: "YAMLDirective";
  value: string;
  kind: "YAML" | "TAG" | null;
  parent: YAMLDocument;
}
interface YAMLDirectiveForYAML extends BaseYAMLDirective {
  kind: "YAML";
  version: string;
}
interface YAMLDirectiveForTAG extends BaseYAMLDirective {
  kind: "TAG";
  handle: string;
  prefix: string;
}
interface YAMLDirectiveForUnknown extends BaseYAMLDirective {
  kind: null;
}
type YAMLDirective = YAMLDirectiveForYAML | YAMLDirectiveForTAG | YAMLDirectiveForUnknown;
interface YAMLWithMeta extends BaseYAMLNode {
  type: "YAMLWithMeta";
  anchor: YAMLAnchor | null;
  tag: YAMLTag | null;
  value: Exclude<YAMLContent, YAMLAlias> | null;
  parent: YAMLDocument | YAMLPair | YAMLSequence;
}
interface YAMLAnchor extends BaseYAMLNode {
  type: "YAMLAnchor";
  name: string;
  parent: YAMLWithMeta;
}
interface YAMLTag extends BaseYAMLNode {
  type: "YAMLTag";
  tag: string;
  raw: string;
  parent: YAMLWithMeta;
}
interface BaseYAMLContentNode extends BaseYAMLNode {
  parent: YAMLDocument | YAMLPair | YAMLSequence | YAMLWithMeta;
}
type YAMLContent = YAMLMapping | YAMLSequence | YAMLScalar | YAMLAlias;
type YAMLMapping = YAMLBlockMapping | YAMLFlowMapping;
interface YAMLBlockMapping extends BaseYAMLContentNode {
  type: "YAMLMapping";
  style: "block";
  pairs: YAMLPair[];
}
interface YAMLFlowMapping extends BaseYAMLContentNode {
  type: "YAMLMapping";
  style: "flow";
  pairs: YAMLPair[];
}
interface YAMLPair extends BaseYAMLNode {
  type: "YAMLPair";
  key: YAMLContent | YAMLWithMeta | null;
  value: YAMLContent | YAMLWithMeta | null;
  parent: YAMLMapping;
}
type YAMLSequence = YAMLBlockSequence | YAMLFlowSequence;
interface YAMLBlockSequence extends BaseYAMLContentNode {
  type: "YAMLSequence";
  style: "block";
  entries: (YAMLContent | YAMLWithMeta | null)[];
}
interface YAMLFlowSequence extends BaseYAMLContentNode {
  type: "YAMLSequence";
  style: "flow";
  entries: (YAMLContent | YAMLWithMeta)[];
}
type YAMLScalar = YAMLPlainScalar | YAMLDoubleQuotedScalar | YAMLSingleQuotedScalar | YAMLBlockLiteralScalar | YAMLBlockFoldedScalar;
interface YAMLPlainScalar extends BaseYAMLContentNode {
  type: "YAMLScalar";
  style: "plain";
  strValue: string;
  value: string | number | boolean | null;
  raw: string;
}
interface YAMLDoubleQuotedScalar extends BaseYAMLContentNode {
  type: "YAMLScalar";
  style: "double-quoted";
  strValue: string;
  value: string;
  raw: string;
}
interface YAMLSingleQuotedScalar extends BaseYAMLContentNode {
  type: "YAMLScalar";
  style: "single-quoted";
  strValue: string;
  value: string;
  raw: string;
}
interface YAMLBlockLiteralScalar extends BaseYAMLContentNode {
  type: "YAMLScalar";
  style: "literal";
  chomping: "clip" | "keep" | "strip";
  indent: null | number;
  value: string;
}
interface YAMLBlockFoldedScalar extends BaseYAMLContentNode {
  type: "YAMLScalar";
  style: "folded";
  chomping: "clip" | "keep" | "strip";
  indent: null | number;
  value: string;
}
interface YAMLAlias extends BaseYAMLContentNode {
  type: "YAMLAlias";
  name: string;
}
//#endregion
//#region src/parser.d.ts
/**
 * Parse YAML source code
 */
declare function parseYAML(code: string, options?: any): YAMLProgram;
//#endregion
//#region src/traverse.d.ts
interface Visitor<N> {
  visitorKeys?: VisitorKeys$1;
  enterNode(node: N, parent: N | null): void;
  leaveNode(node: N, parent: N | null): void;
}
declare function traverseNodes(node: YAMLNode, visitor: Visitor<YAMLNode>): void;
//#endregion
//#region src/errors.d.ts
/**
 * YAML parse errors.
 */
declare class ParseError extends SyntaxError {
  index: number;
  lineNumber: number;
  column: number;
  /**
   * Initialize this ParseError instance.
   * @param message The error message.
   * @param offset The offset number of this error.
   * @param line The line number of this error.
   * @param column The column number of this error.
   */
  constructor(message: string, offset: number, line: number, column: number);
}
declare namespace meta_d_exports {
  export { name, version };
}
declare const name: "yaml-eslint-parser";
declare const version: "2.0.0";
//#endregion
//#region src/index.d.ts
declare const VisitorKeys: SourceCode.VisitorKeys;
/**
 * Parse source code
 */
declare function parseForESLint(code: string, options?: any): {
  ast: YAMLProgram;
  visitorKeys: SourceCode.VisitorKeys;
  services: {
    isYAML: boolean;
  };
};
//#endregion
export { type ast_d_exports as AST, ParseError, VisitorKeys, getStaticYAMLValue, meta_d_exports as meta, name, parseForESLint, parseYAML, traverseNodes };