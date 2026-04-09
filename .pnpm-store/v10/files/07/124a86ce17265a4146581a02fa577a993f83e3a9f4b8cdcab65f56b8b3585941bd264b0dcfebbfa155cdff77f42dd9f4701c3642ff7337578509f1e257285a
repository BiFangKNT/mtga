import { AST } from "yaml-eslint-parser";
import { IDirective, TextSourceCodeBase, TraversalStep } from "@eslint/plugin-kit";
import { CursorWithCountOptionsWithComment, CursorWithCountOptionsWithFilter, CursorWithCountOptionsWithoutFilter, CursorWithSkipOptionsWithComment, CursorWithSkipOptionsWithFilter, CursorWithSkipOptionsWithoutFilter } from "@ota-meshi/ast-token-store";
import * as _eslint_core0 from "@eslint/core";
import { File, FileProblem, Language, OkParseResult, ParseResult, RuleDefinition, RulesConfig } from "@eslint/core";
import { Linter, Scope } from "eslint";

//#region src/meta.d.ts
declare namespace meta_d_exports {
  export { name, version };
}
declare const name: string;
declare const version: string;
//#endregion
//#region src/language/yaml-source-code.d.ts
/**
 * YAML-specific syntax element type
 */
type YAMLSyntaxElement = AST.YAMLNode | AST.Token | AST.Comment;
type YAMLToken = AST.Token | AST.Comment;
/**
 * YAML Source Code Object
 */
declare class YAMLSourceCode extends TextSourceCodeBase<{
  LangOptions: Record<never, never>;
  RootNode: AST.YAMLProgram;
  SyntaxElementWithLoc: YAMLSyntaxElement;
  ConfigNode: AST.Comment;
}> {
  #private;
  readonly hasBOM: boolean;
  readonly parserServices: {
    isYAML?: boolean;
    parseError?: unknown;
  };
  readonly visitorKeys: Record<string, string[]>;
  private readonly tokenStore;
  /**
   * Creates a new instance.
   */
  constructor(config: {
    text: string;
    ast: AST.YAMLProgram;
    hasBOM: boolean;
    parserServices: {
      isYAML: boolean;
      parseError?: unknown;
    };
    visitorKeys?: Record<string, string[]> | null | undefined;
  });
  traverse(): Iterable<TraversalStep>;
  /**
   * Gets all tokens and comments.
   */
  get tokensAndComments(): YAMLToken[];
  getLines(): string[];
  getAllComments(): AST.Comment[];
  /**
   * Returns an array of all inline configuration nodes found in the source code.
   * This includes eslint-disable, eslint-enable, eslint-disable-line,
   * eslint-disable-next-line, and eslint (for inline config) comments.
   */
  getInlineConfigNodes(): AST.Comment[];
  /**
   * Returns directives that enable or disable rules along with any problems
   * encountered while parsing the directives.
   */
  getDisableDirectives(): {
    directives: IDirective[];
    problems: FileProblem[];
  };
  /**
   * Returns inline rule configurations along with any problems
   * encountered while parsing the configurations.
   */
  applyInlineConfig(): {
    configs: {
      config: {
        rules: RulesConfig;
      };
      loc: AST.SourceLocation;
    }[];
    problems: FileProblem[];
  };
  getNodeByRangeIndex(index: number): AST.YAMLNode | null;
  /**
   * Gets the first token of the given node.
   */
  getFirstToken(node: YAMLSyntaxElement): AST.Token;
  /**
   * Gets the first token of the given node with options.
   */
  getFirstToken(node: YAMLSyntaxElement, options: CursorWithSkipOptionsWithoutFilter): AST.Token | null;
  /**
   * Gets the first token of the given node with filter options.
   */
  getFirstToken<R extends AST.Token>(node: YAMLSyntaxElement, options: CursorWithSkipOptionsWithFilter<AST.Token, R>): R | null;
  /**
   * Gets the first token of the given node with comment options.
   */
  getFirstToken<R extends AST.Token | AST.Comment>(node: YAMLSyntaxElement, options: CursorWithSkipOptionsWithComment<AST.Token, AST.Comment, R>): R | null;
  /**
   * Gets the first tokens of the given node.
   */
  getFirstTokens(node: YAMLSyntaxElement, options?: CursorWithCountOptionsWithoutFilter): AST.Token[];
  /**
   * Gets the first tokens of the given node with filter options.
   */
  getFirstTokens<R extends AST.Token>(node: YAMLSyntaxElement, options: CursorWithCountOptionsWithFilter<AST.Token, R>): R[];
  /**
   * Gets the first tokens of the given node with comment options.
   */
  getFirstTokens<R extends AST.Token | AST.Comment>(node: YAMLSyntaxElement, options: CursorWithCountOptionsWithComment<AST.Token, AST.Comment, R>): R[];
  /**
   * Gets the last token of the given node.
   */
  getLastToken(node: YAMLSyntaxElement): AST.Token;
  /**
   * Gets the last token of the given node with options.
   */
  getLastToken(node: YAMLSyntaxElement, options: CursorWithSkipOptionsWithoutFilter): AST.Token | null;
  /**
   * Gets the last token of the given node with filter options.
   */
  getLastToken<R extends AST.Token>(node: YAMLSyntaxElement, options: CursorWithSkipOptionsWithFilter<AST.Token, R>): R | null;
  /**
   * Gets the last token of the given node with comment options.
   */
  getLastToken<R extends AST.Token | AST.Comment>(node: YAMLSyntaxElement, options: CursorWithSkipOptionsWithComment<AST.Token, AST.Comment, R>): R | null;
  /**
   * Get the last tokens of the given node.
   */
  getLastTokens(node: YAMLSyntaxElement, options?: CursorWithCountOptionsWithoutFilter): AST.Token[];
  /**
   * Get the last tokens of the given node with filter options.
   */
  getLastTokens<R extends AST.Token>(node: YAMLSyntaxElement, options: CursorWithCountOptionsWithFilter<AST.Token, R>): R[];
  /**
   * Get the last tokens of the given node with comment options.
   */
  getLastTokens<R extends AST.Token | AST.Comment>(node: YAMLSyntaxElement, options: CursorWithCountOptionsWithComment<AST.Token, AST.Comment, R>): R[];
  /**
   * Gets the token that precedes a given node or token.
   */
  getTokenBefore(node: YAMLSyntaxElement, options?: CursorWithSkipOptionsWithoutFilter): AST.Token | null;
  /**
   * Gets the token that precedes a given node or token with filter options.
   */
  getTokenBefore<R extends AST.Token>(node: YAMLSyntaxElement, options: CursorWithSkipOptionsWithFilter<AST.Token, R>): R | null;
  /**
   * Gets the token that precedes a given node or token with comment options.
   */
  getTokenBefore<R extends AST.Token | AST.Comment>(node: YAMLSyntaxElement, options: CursorWithSkipOptionsWithComment<AST.Token, AST.Comment, R>): R | null;
  /**
   * Gets the `count` tokens that precedes a given node or token.
   */
  getTokensBefore(node: YAMLSyntaxElement, options?: CursorWithCountOptionsWithoutFilter): AST.Token[];
  /**
   * Gets the `count` tokens that precedes a given node or token with filter options.
   */
  getTokensBefore<R extends AST.Token>(node: YAMLSyntaxElement, options: CursorWithCountOptionsWithFilter<AST.Token, R>): R[];
  /**
   * Gets the `count` tokens that precedes a given node or token with comment options.
   */
  getTokensBefore<R extends AST.Token | AST.Comment>(node: YAMLSyntaxElement, options: CursorWithCountOptionsWithComment<AST.Token, AST.Comment, R>): R[];
  /**
   * Gets the token that follows a given node or token.
   */
  getTokenAfter(node: YAMLSyntaxElement, options?: CursorWithSkipOptionsWithoutFilter): AST.Token | null;
  /**
   * Gets the token that follows a given node or token with filter options.
   */
  getTokenAfter<R extends AST.Token>(node: YAMLSyntaxElement, options: CursorWithSkipOptionsWithFilter<AST.Token, R>): R | null;
  /**
   * Gets the token that follows a given node or token with comment options.
   */
  getTokenAfter<R extends AST.Token | AST.Comment>(node: YAMLSyntaxElement, options: CursorWithSkipOptionsWithComment<AST.Token, AST.Comment, R>): R | null;
  /**
   * Gets the `count` tokens that follows a given node or token.
   */
  getTokensAfter(node: YAMLSyntaxElement, options?: CursorWithCountOptionsWithoutFilter): AST.Token[];
  /**
   * Gets the `count` tokens that follows a given node or token with filter options.
   */
  getTokensAfter<R extends AST.Token>(node: YAMLSyntaxElement, options: CursorWithCountOptionsWithFilter<AST.Token, R>): R[];
  /**
   * Gets the `count` tokens that follows a given node or token with comment options.
   */
  getTokensAfter<R extends AST.Token | AST.Comment>(node: YAMLSyntaxElement, options: CursorWithCountOptionsWithComment<AST.Token, AST.Comment, R>): R[];
  /**
   * Gets the first token between two non-overlapping nodes.
   */
  getFirstTokenBetween(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options?: CursorWithSkipOptionsWithoutFilter): AST.Token | null;
  /**
   * Gets the first token between two non-overlapping nodes with filter options.
   */
  getFirstTokenBetween<R extends AST.Token>(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options: CursorWithSkipOptionsWithFilter<AST.Token, R>): R | null;
  /**
   * Gets the first token between two non-overlapping nodes with comment options.
   */
  getFirstTokenBetween<R extends AST.Token | AST.Comment>(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options: CursorWithSkipOptionsWithComment<AST.Token, AST.Comment, R>): R | null;
  /**
   * Gets the first tokens between two non-overlapping nodes.
   */
  getFirstTokensBetween(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options?: CursorWithCountOptionsWithoutFilter): AST.Token[];
  /**
   * Gets the first tokens between two non-overlapping nodes with filter options.
   */
  getFirstTokensBetween<R extends AST.Token>(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options: CursorWithCountOptionsWithFilter<AST.Token, R>): R[];
  /**
   * Gets the first tokens between two non-overlapping nodes with comment options.
   */
  getFirstTokensBetween<R extends AST.Token | AST.Comment>(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options: CursorWithCountOptionsWithComment<AST.Token, AST.Comment, R>): R[];
  /**
   * Gets the last token between two non-overlapping nodes.
   */
  getLastTokenBetween(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options?: CursorWithSkipOptionsWithoutFilter): AST.Token | null;
  /**
   * Gets the last token between two non-overlapping nodes with filter options.
   */
  getLastTokenBetween<R extends AST.Token>(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options: CursorWithSkipOptionsWithFilter<AST.Token, R>): R | null;
  /**
   * Gets the last token between two non-overlapping nodes with comment options.
   */
  getLastTokenBetween<R extends AST.Token | AST.Comment>(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options: CursorWithSkipOptionsWithComment<AST.Token, AST.Comment, R>): R | null;
  /**
   * Gets the last tokens between two non-overlapping nodes.
   */
  getLastTokensBetween(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options?: CursorWithCountOptionsWithoutFilter): AST.Token[];
  /**
   * Gets the last tokens between two non-overlapping nodes with filter options.
   */
  getLastTokensBetween<R extends AST.Token>(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options: CursorWithCountOptionsWithFilter<AST.Token, R>): R[];
  /**
   * Gets the last tokens between two non-overlapping nodes with comment options.
   */
  getLastTokensBetween<R extends AST.Token | AST.Comment>(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options: CursorWithCountOptionsWithComment<AST.Token, AST.Comment, R>): R[];
  /**
   * Gets all tokens that are related to the given node.
   */
  getTokens(node: YAMLSyntaxElement, options?: CursorWithCountOptionsWithoutFilter): AST.Token[];
  /**
   * Gets all tokens that are related to the given node with filter options.
   */
  getTokens<R extends AST.Token>(node: YAMLSyntaxElement, options: CursorWithCountOptionsWithFilter<AST.Token, R>): R[];
  /**
   * Gets all tokens that are related to the given node with comment options.
   */
  getTokens<R extends AST.Token | AST.Comment>(node: YAMLSyntaxElement, options: CursorWithCountOptionsWithComment<AST.Token, AST.Comment, R>): R[];
  /**
   * Gets all of the tokens between two non-overlapping nodes.
   */
  getTokensBetween(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options?: CursorWithCountOptionsWithoutFilter): AST.Token[];
  /**
   * Gets all of the tokens between two non-overlapping nodes with filter options.
   */
  getTokensBetween<R extends AST.Token>(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options: CursorWithCountOptionsWithFilter<AST.Token, R>): R[];
  /**
   * Gets all of the tokens between two non-overlapping nodes with comment options.
   */
  getTokensBetween<R extends AST.Token | AST.Comment>(left: YAMLSyntaxElement, right: YAMLSyntaxElement, options: CursorWithCountOptionsWithComment<AST.Token, AST.Comment, R>): R[];
  getCommentsInside(nodeOrToken: YAMLSyntaxElement): AST.Comment[];
  getCommentsBefore(nodeOrToken: YAMLSyntaxElement): AST.Comment[];
  getCommentsAfter(nodeOrToken: YAMLSyntaxElement): AST.Comment[];
  commentsExistBetween(first: YAMLSyntaxElement, second: YAMLSyntaxElement): boolean;
  isSpaceBetween(first: AST.Token | AST.Comment, second: AST.Token | AST.Comment): boolean;
  /**
   * Compatibility for ESLint's SourceCode API
   * @deprecated YAML does not have scopes
   */
  getScope(node?: AST.YAMLNode): Scope.Scope | null;
  /**
   * Compatibility for ESLint's SourceCode API
   * @deprecated YAML does not have scopes
   */
  get scopeManager(): Scope.ScopeManager | null;
  /**
   * Compatibility for ESLint's SourceCode API
   * @deprecated
   */
  isSpaceBetweenTokens(first: YAMLToken, second: YAMLToken): boolean;
  private _getChildren;
}
//#endregion
//#region src/language/yaml-language.d.ts
/**
 * Language options for YAML
 */
type YAMLLanguageOptions = {
  parserOptions?: {
    defaultYAMLVersion?: "1.1" | "1.2";
  };
};
/**
 * The YAML language implementation for ESLint.
 */
declare class YAMLLanguage implements Language<{
  LangOptions: YAMLLanguageOptions;
  Code: YAMLSourceCode;
  RootNode: AST.YAMLProgram;
  Node: AST.YAMLNode;
}> {
  /**
   * The type of file to read.
   */
  fileType: "text";
  /**
   * The line number at which the parser starts counting.
   */
  lineStart: 1;
  /**
   * The column number at which the parser starts counting.
   */
  columnStart: 0;
  /**
   * The name of the key that holds the type of the node.
   */
  nodeTypeKey: "type";
  /**
   * Validates the language options.
   */
  validateLanguageOptions(_languageOptions: YAMLLanguageOptions): void;
  normalizeLanguageOptions(languageOptions: YAMLLanguageOptions): YAMLLanguageOptions;
  /**
   * Parses the given file into an AST.
   */
  parse(file: File, context: {
    languageOptions?: YAMLLanguageOptions;
  }): ParseResult<AST.YAMLProgram>;
  /**
   * Creates a new SourceCode object for the given file and parse result.
   */
  createSourceCode(file: File, parseResult: OkParseResult<AST.YAMLProgram>): YAMLSourceCode;
}
//#endregion
//#region src/index.d.ts
declare const configs: {
  base: Linter.Config[];
  recommended: Linter.Config[];
  standard: Linter.Config[];
  prettier: Linter.Config[];
  "flat/base": Linter.Config[];
  "flat/recommended": Linter.Config[];
  "flat/standard": Linter.Config[];
  "flat/prettier": Linter.Config[];
};
declare const rules: Record<string, RuleDefinition>;
declare const languages: {
  yaml: YAMLLanguage;
};
declare const _default: {
  meta: typeof meta_d_exports;
  configs: {
    base: Linter.Config[];
    recommended: Linter.Config[];
    standard: Linter.Config[];
    prettier: Linter.Config[];
    "flat/base": Linter.Config[];
    "flat/recommended": Linter.Config[];
    "flat/standard": Linter.Config[];
    "flat/prettier": Linter.Config[];
  };
  rules: Record<string, RuleDefinition<_eslint_core0.RuleDefinitionTypeOptions>>;
  languages: {
    yaml: YAMLLanguage;
  };
};
//#endregion
export { type YAMLLanguageOptions, type YAMLSourceCode, configs, _default as default, languages, meta_d_exports as meta, rules };