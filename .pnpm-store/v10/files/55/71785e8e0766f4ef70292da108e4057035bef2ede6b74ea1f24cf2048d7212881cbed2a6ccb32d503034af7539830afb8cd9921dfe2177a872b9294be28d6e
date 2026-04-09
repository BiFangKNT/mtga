//#region src/types.d.ts
type SyntaxElement = {
  range: [number, number];
};
type TokenFilter<E extends SyntaxElement, R extends E = E> = ((tokenOrComment: E) => tokenOrComment is R) | ((tokenOrComment: E) => boolean);
type CursorWithSkipOptionsWithoutFilter = number | {
  includeComments?: false;
  filter?: undefined;
  skip?: number;
};
type CursorWithSkipOptionsWithFilter<Token extends SyntaxElement, R extends Token = Token> = TokenFilter<Token, R> | {
  includeComments?: false;
  filter: TokenFilter<Token, R>;
  skip?: number;
};
type CursorWithSkipOptionsWithComment<Token extends SyntaxElement, Comment extends SyntaxElement, R extends Token | Comment = Token | Comment> = {
  includeComments: true;
  filter?: TokenFilter<Token | Comment, R>;
  skip?: number;
};
type CursorWithCountOptionsWithoutFilter = number | {
  includeComments?: false;
  filter?: undefined;
  count?: number;
};
type CursorWithCountOptionsWithFilter<Token extends SyntaxElement, R extends Token = Token> = TokenFilter<Token, R> | {
  includeComments?: false;
  filter: TokenFilter<Token, R>;
  count?: number;
};
type CursorWithCountOptionsWithComment<Token extends SyntaxElement, Comment extends SyntaxElement, R extends Token | Comment = Token | Comment> = {
  includeComments: true;
  filter?: TokenFilter<Token | Comment, R>;
  count?: number;
};
//#endregion
//#region src/token-store/token-store.d.ts
declare const PRIVATE: unique symbol;
declare class TokenStore<Node extends SyntaxElement, Token extends SyntaxElement, Comment extends SyntaxElement> {
  private readonly [PRIVATE];
  constructor(params: {
    tokens: (Token | Comment)[];
    isComment: (token: Token | Comment) => token is Comment;
  });
  /**
   * Gets all tokens, including comments.
   */
  getAllTokens(): (Token | Comment)[];
  /**
   * Gets all comments.
   */
  getAllComments(): Comment[];
  /**
   * Gets the first token of the given node.
   */
  getFirstToken(node: Node | Token): Token;
  /**
   * Gets the first token of the given node with simple options.
   */
  getFirstToken(node: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter): Token | null;
  /**
   * Gets the first token of the given node with options.
   */
  getFirstToken<R extends Token>(node: Node | Token | Comment, options: CursorWithSkipOptionsWithFilter<Token, R>): R | null;
  /**
   * Gets the first token of the given node with options.
   */
  getFirstToken<R extends Token | Comment>(node: Node | Token | Comment, options: CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Gets the first token of the given node with complex options.
   */
  getFirstToken<R extends Token | Comment>(node: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter | CursorWithSkipOptionsWithFilter<Token, R & Token> | CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Gets the first tokens of the given node.
   */
  getFirstTokens(node: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter): Token[];
  /**
   * Gets the first tokens of the given node.
   */
  getFirstTokens<R extends Token>(node: Node | Token | Comment, options: CursorWithCountOptionsWithFilter<Token, R>): R[];
  /**
   * Gets the first tokens of the given node with comment options.
   */
  getFirstTokens<R extends Token | Comment>(node: Node | Token | Comment, options: CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets the first tokens of the given node with complex options.
   */
  getFirstTokens<R extends Token | Comment>(node: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter | CursorWithCountOptionsWithFilter<Token, R & Token> | CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets the last token of the given node.
   */
  getLastToken(node: Node | Token): Token;
  /**
   * Gets the last token of the given node with options.
   */
  getLastToken(node: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter): Token | null;
  /**
   * Gets the last token of the given node with options.
   */
  getLastToken<R extends Token>(node: Node | Token | Comment, options: CursorWithSkipOptionsWithFilter<Token, R>): R | null;
  /**
   * Gets the last token of the given node with options.
   */
  getLastToken<R extends Token | Comment>(node: Node | Token | Comment, options: CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Gets the last token of the given node with complex options.
   */
  getLastToken<R extends Token | Comment>(node: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter | CursorWithSkipOptionsWithFilter<Token, R & Token> | CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Get the last tokens of the given node.
   */
  getLastTokens(node: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter): Token[];
  /**
   * Get the last tokens of the given node.
   */
  getLastTokens<R extends Token>(node: Node | Token | Comment, options: CursorWithCountOptionsWithFilter<Token, R>): R[];
  /**
   * Get the last tokens of the given node with comment options.
   */
  getLastTokens<R extends Token | Comment>(node: Node | Token | Comment, options: CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Get the last tokens of the given node with complex options.
   */
  getLastTokens<R extends Token | Comment>(node: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter | CursorWithCountOptionsWithFilter<Token, R & Token> | CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets the token that follows a given node or token.
   */
  getTokenAfter(node: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter): Token | null;
  /**
   * Gets the token that follows a given node or token.
   */
  getTokenAfter<R extends Token>(node: Node | Token | Comment, options?: CursorWithSkipOptionsWithFilter<Token, R>): R | null;
  /**
   * Gets the token that follows a given node or token with comment options.
   */
  getTokenAfter<R extends Token | Comment>(node: Node | Token | Comment, options: CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Gets the token that follows a given node or token with complex options.
   */
  getTokenAfter<R extends Token | Comment>(node: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter | CursorWithSkipOptionsWithFilter<Token, R & Token> | CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Gets the `count` tokens that follows a given node or token.
   */
  getTokensAfter(node: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter): Token[];
  /**
   * Gets the `count` tokens that follows a given node or token.
   */
  getTokensAfter<R extends Token>(node: Node | Token | Comment, options: CursorWithCountOptionsWithFilter<Token, R>): R[];
  /**
   * Gets the `count` tokens that follows a given node or token with comment options.
   */
  getTokensAfter<R extends Token | Comment>(node: Node | Token | Comment, options: CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets the `count` tokens that follows a given node or token with complex options.
   */
  getTokensAfter<R extends Token | Comment>(node: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter | CursorWithCountOptionsWithFilter<Token, R & Token> | CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets the token that precedes a given node or token.
   */
  getTokenBefore(node: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter): Token | null;
  /**
   * Gets the token that precedes a given node or token.
   */
  getTokenBefore<R extends Token>(node: Node | Token | Comment, options: CursorWithSkipOptionsWithFilter<Token, R>): R | null;
  /**
   * Gets the token that precedes a given node or token with comment options.
   */
  getTokenBefore<R extends Token | Comment>(node: Node | Token | Comment, options: CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Gets the token that precedes a given node or token with complex options.
   */
  getTokenBefore<R extends Token | Comment>(node: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter | CursorWithSkipOptionsWithFilter<Token, R & Token> | CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Gets the `count` tokens that precedes a given node or token.
   */
  getTokensBefore(node: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter): Token[];
  /**
   * Gets the `count` tokens that precedes a given node or token.
   */
  getTokensBefore<R extends Token>(node: Node | Token | Comment, options: CursorWithCountOptionsWithFilter<Token, R>): R[];
  /**
   * Gets the `count` tokens that precedes a given node or token with comment options.
   */
  getTokensBefore<R extends Token | Comment>(node: Node | Token | Comment, options: CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets the `count` tokens that precedes a given node or token with complex options.
   */
  getTokensBefore<R extends Token | Comment>(node: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter | CursorWithCountOptionsWithFilter<Token, R & Token> | CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets the first token between two non-overlapping nodes.
   */
  getFirstTokenBetween(left: Node | Token | Comment, right: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter): Token | null;
  /**
   * Gets the first token between two non-overlapping nodes.
   */
  getFirstTokenBetween<R extends Token>(left: Node | Token | Comment, right: Node | Token | Comment, options: CursorWithSkipOptionsWithFilter<Token, R>): R | null;
  /**
   * Gets the first token between two non-overlapping nodes with comment options.
   */
  getFirstTokenBetween<R extends Token | Comment>(left: Node | Token | Comment, right: Node | Token | Comment, options: CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Gets the first token between two non-overlapping nodes with complex options.
   */
  getFirstTokenBetween<R extends Token | Comment>(left: Node | Token | Comment, right: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter | CursorWithSkipOptionsWithFilter<Token, R & Token> | CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Gets the first tokens between two non-overlapping nodes.
   */
  getFirstTokensBetween(left: Node | Token | Comment, right: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter): Token[];
  /**
   * Gets the first tokens between two non-overlapping nodes.
   */
  getFirstTokensBetween<R extends Token>(left: Node | Token | Comment, right: Node | Token | Comment, options: CursorWithCountOptionsWithFilter<Token, R>): R[];
  /**
   * Gets the first tokens between two non-overlapping nodes with comment options.
   */
  getFirstTokensBetween<R extends Token | Comment>(left: Node | Token | Comment, right: Node | Token | Comment, options: CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets the first tokens between two non-overlapping nodes with complex options.
   */
  getFirstTokensBetween<R extends Token | Comment>(left: Node | Token | Comment, right: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter | CursorWithCountOptionsWithFilter<Token, R & Token> | CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets the last token between two non-overlapping nodes.
   */
  getLastTokenBetween(left: Node | Token | Comment, right: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter): Token | null;
  /**
   * Gets the last token between two non-overlapping nodes.
   */
  getLastTokenBetween<R extends Token>(left: Node | Token | Comment, right: Node | Token | Comment, options: CursorWithSkipOptionsWithFilter<Token, R>): R | null;
  /**
   * Gets the last token between two non-overlapping nodes with comment options.
   */
  getLastTokenBetween<R extends Token | Comment>(left: Node | Token | Comment, right: Node | Token | Comment, options: CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Gets the last token between two non-overlapping nodes with complex options.
   */
  getLastTokenBetween<R extends Token | Comment>(left: Node | Token | Comment, right: Node | Token | Comment, options?: CursorWithSkipOptionsWithoutFilter | CursorWithSkipOptionsWithFilter<Token, R & Token> | CursorWithSkipOptionsWithComment<Token, Comment, R>): R | null;
  /**
   * Gets the last tokens between two non-overlapping nodes.
   */
  getLastTokensBetween(left: Node | Token | Comment, right: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter): Token[];
  /**
   * Gets the last tokens between two non-overlapping nodes.
   */
  getLastTokensBetween<R extends Token>(left: Node | Token | Comment, right: Node | Token | Comment, options: CursorWithCountOptionsWithFilter<Token, R>): R[];
  /**
   * Gets the last tokens between two non-overlapping nodes with comment options.
   */
  getLastTokensBetween<R extends Token | Comment>(left: Node | Token | Comment, right: Node | Token | Comment, options: CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets the last tokens between two non-overlapping nodes with complex options.
   */
  getLastTokensBetween<R extends Token | Comment>(left: Node | Token | Comment, right: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter | CursorWithCountOptionsWithFilter<Token, R & Token> | CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets all tokens that are related to the given node.
   */
  getTokens(node: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter): Token[];
  /**
   * Gets all tokens that are related to the given node.
   */
  getTokens<R extends Token>(node: Node | Token | Comment, options?: CursorWithCountOptionsWithFilter<Token, R>): R[];
  /**
   * Gets all tokens that are related to the given node with comment options.
   */
  getTokens<R extends Token | Comment>(node: Node | Token | Comment, options: CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets all tokens that are related to the given node with complex options.
   */
  getTokens<R extends Token | Comment>(node: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter | CursorWithCountOptionsWithFilter<Token, R & Token> | CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets all of the tokens between two non-overlapping nodes.
   */
  getTokensBetween(left: Node | Token | Comment, right: Node | Token | Comment, options?: CursorWithCountOptionsWithoutFilter): Token[];
  /**
   * Gets all of the tokens between two non-overlapping nodes.
   */
  getTokensBetween<R extends Token>(left: Node | Token | Comment, right: Node | Token | Comment, options?: CursorWithCountOptionsWithFilter<Token, R>): R[];
  /**
   * Gets all of the tokens between two non-overlapping nodes with comment options.
   */
  getTokensBetween<R extends Token | Comment>(left: Node | Token | Comment, right: Node | Token | Comment, options: CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets all of the tokens between two non-overlapping nodes with complex options.
   */
  getTokensBetween<R extends Token | Comment>(left: Node | Token | Comment, right: Node | Token | Comment, paddingOrOptions?: CursorWithCountOptionsWithoutFilter | CursorWithCountOptionsWithFilter<Token, R & Token> | CursorWithCountOptionsWithComment<Token, Comment, R>): R[];
  /**
   * Gets all comment tokens inside the given node or token.
   */
  getCommentsInside(nodeOrToken: Node | Token | Comment): Comment[];
  /**
   * Gets all comment tokens directly before the given node or token.
   */
  getCommentsBefore(nodeOrToken: Node | Token | Comment): Comment[];
  /**
   * Gets all comment tokens directly after the given node or token.
   */
  getCommentsAfter(nodeOrToken: Node | Token | Comment): Comment[];
  /**
   * Checks if there are any comment tokens between two non-overlapping nodes.
   */
  commentsExistBetween(left: Node | Token | Comment, right: Node | Token | Comment): boolean;
  /**
   * Checks if there is whitespace between two non-overlapping nodes.
   */
  isSpaceBetween(left: Node | Token | Comment, right: Node | Token | Comment): boolean;
}
//#endregion
//#region src/index.d.ts
declare const meta: {
  name: string;
  version: string;
};
//#endregion
export { type CursorWithCountOptionsWithComment, type CursorWithCountOptionsWithFilter, type CursorWithCountOptionsWithoutFilter, type CursorWithSkipOptionsWithComment, type CursorWithSkipOptionsWithFilter, type CursorWithSkipOptionsWithoutFilter, type SyntaxElement, type TokenFilter, TokenStore, meta };