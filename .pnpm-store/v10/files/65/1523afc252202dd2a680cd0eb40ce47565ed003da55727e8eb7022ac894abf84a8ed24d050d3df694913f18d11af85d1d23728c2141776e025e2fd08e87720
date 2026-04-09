/**
 * @fileoverview Tailwind 4 `@import` rule parser
 * @see https://github.com/eslint/csstree/blob/1d74355c1960315bf55a33b0652d13f97ebb1ba2/lib/syntax/atrule/import.js.
 */
//-----------------------------------------------------------------------------
// Imports
//-----------------------------------------------------------------------------
import { tokenTypes } from "@eslint/css-tree";
//-----------------------------------------------------------------------------
// Type Definitions
//-----------------------------------------------------------------------------
/**
 * @import { ParserContext as BaseParserContext, ConsumerFunction, SyntaxConfig } from "@eslint/css-tree";
 */
/**
 * @typedef {'Raw' | 'Layer' | 'Condition' | 'Declaration' | 'String' | 'Identifier' | 'Url' | 'Function' | 'MediaQueryList'} ConsumerNames
 * @typedef {BaseParserContext & { [key in ConsumerNames]: ConsumerFunction }} ParserContext
 */
//-----------------------------------------------------------------------------
// Helpers
//-----------------------------------------------------------------------------
/**
 * @param {ConsumerFunction} parse
 * @param {ConsumerFunction=} fallback
 * @this {ParserContext}
 */
function parseWithFallback(parse, fallback) {
    return this.parseWithFallback(() => {
        try {
            return parse.call(this);
        }
        finally {
            this.skipSC();
            if (this.lookupNonWSType(0) !== tokenTypes.RightParenthesis) {
                // @ts-expect-error
                this.error();
            }
        }
    }, fallback || (() => this.Raw(null, true)));
}
const parseFunctions = {
    /**
     * @this {ParserContext}
     */
    layer() {
        this.skipSC();
        const children = this.createList();
        const node = parseWithFallback.call(this, this.Layer);
        if (node.type !== 'Raw' || node.value !== '') {
            children.push(node);
        }
        return children;
    },
    /**
     * @this {ParserContext}
     */
    supports() {
        this.skipSC();
        const children = this.createList();
        const node = parseWithFallback.call(this, this.Declaration, () => parseWithFallback.call(this, () => this.Condition('supports')));
        if (node.type !== 'Raw' || node.value !== '') {
            children.push(node);
        }
        return children;
    },
    /**
     * @this {ParserContext}
     */
    source() {
        this.skipSC();
        const children = this.createList();
        const node = parseWithFallback.call(this, this.String, () => parseWithFallback.call(this, this.Identifier));
        if (node.type !== 'Raw' || node.value !== '') {
            children.push(node);
        }
        return children;
    },
    /**
     * @this {ParserContext}
     */
    prefix() {
        this.skipSC();
        const children = this.createList();
        const node = parseWithFallback.call(this, this.Identifier);
        if (node.type !== 'Raw' || node.value !== '') {
            children.push(node);
        }
        return children;
    },
};
//-----------------------------------------------------------------------------
// Exports
//-----------------------------------------------------------------------------
export default {
    parse: {
        /**
         * @this {ParserContext}
         * @type {SyntaxConfig['atrule']['import']['parse']['prelude']}
         */
        // @ts-expect-error it doesn't like that we extend ParserContext
        prelude: function () {
            const children = this.createList();
            switch (this.tokenType) {
                case tokenTypes.String:
                    children.push(this.String());
                    break;
                case tokenTypes.Url:
                case tokenTypes.Function:
                    children.push(this.Url());
                    break;
                default:
                    // @ts-expect-error
                    this.error('String or url() is expected');
            }
            while (true) {
                this.skipSC();
                if (this.tokenType === tokenTypes.Function && (this.cmpStr(this.tokenStart, this.tokenEnd, 'source(') ||
                    this.cmpStr(this.tokenStart, this.tokenEnd, 'prefix(') ||
                    this.cmpStr(this.tokenStart, this.tokenEnd, 'layer('))) {
                    children.push(this.Function(null, parseFunctions));
                }
                else if (this.tokenType === tokenTypes.Ident &&
                    this.cmpStr(this.tokenStart, this.tokenEnd, 'layer')) {
                    children.push(this.Identifier());
                }
                else {
                    break;
                }
            }
            this.skipSC();
            if (this.tokenType === tokenTypes.Function &&
                this.cmpStr(this.tokenStart, this.tokenEnd, 'supports(')) {
                children.push(this.Function(null, parseFunctions));
            }
            if (this.lookupNonWSType(0) === tokenTypes.Ident ||
                this.lookupNonWSType(0) === tokenTypes.LeftParenthesis) {
                children.push(this.MediaQueryList());
            }
            return children;
        },
        block: null
    }
};
