'use strict';

const types = require('../../tokenizer/types.cjs');

const AMPERSAND = 0x0026;       // U+0026 AMPERSAND (&)
const DOT = 0x002E;             // U+002E FULL STOP (.)
const STAR = 0x002A;            // U+002A ASTERISK (*);
const PLUSSIGN = 0x002B;        // U+002B PLUS SIGN (+)
const GREATERTHANSIGN = 0x003E; // U+003E GREATER-THAN SIGN (>)
const TILDE = 0x007E;           // U+007E TILDE (~)

const selectorStarts = new Set([
    AMPERSAND,
    DOT,
    STAR,
    PLUSSIGN,
    GREATERTHANSIGN,
    TILDE
]);

function consumeRaw() {
    return this.Raw(null, true);
}
function consumeRule() {
    return this.parseWithFallback(this.Rule, consumeRaw);
}
function consumeRawDeclaration() {
    return this.Raw(this.consumeUntilSemicolonIncluded, true);
}
function consumeDeclaration() {
    if (this.tokenType === types.Semicolon) {
        return consumeRawDeclaration.call(this, this.tokenIndex);
    }

    const node = this.parseWithFallback(this.Declaration, consumeRawDeclaration);

    if (this.tokenType === types.Semicolon) {
        this.next();
    }

    return node;
}

function isElementSelectorStart() {
    if (this.tokenType !== types.Ident) {
        return false;
    }

    const nextTokenType = this.lookupTypeNonSC(1);

    if (nextTokenType !== types.Colon && nextTokenType !== types.Semicolon && nextTokenType !== types.RightCurlyBracket) {
        return true;
    }

    return false;
}

function isSelectorStart() {
    // Check for Delim tokens that might be selector starts
    if (this.tokenType === types.Delim && selectorStarts.has(this.source.charCodeAt(this.tokenStart))) {
        const code = this.source.charCodeAt(this.tokenStart);

        // Special case: browser hack prefixes (*, +, &) followed immediately by an ident
        // (no whitespace) are declarations, not selectors. Examples: *zoom: 1; +width: 100px; &prop: value;
        if (code === STAR || code === PLUSSIGN || code === AMPERSAND) {
            const nextToken = this.lookupType(1);
            const nextTokenNonSC = this.lookupTypeNonSC(1);

            // If next token is Ident and there's no whitespace between, it's a declaration
            if (nextToken === types.Ident && nextTokenNonSC === types.Ident) {
                return false;
            }
        }
        return true;
    }

    // Hash can be either a Hash token (#id selector) or Delim(#) + Ident (browser hack)
    // When it's a Hash token, it's a selector. When it's Delim, check if followed by Ident without whitespace
    if (this.tokenType === types.Hash) {
        return true;
    }

    return this.tokenType === types.LeftSquareBracket ||
        this.tokenType === types.Colon || isElementSelectorStart.call(this);
}

const name = 'Block';
const walkContext = 'block';
const structure = {
    children: [[
        'Atrule',
        'Rule',
        'Declaration'
    ]]
};

function parse(isStyleBlock, { allowNestedRules = false } = {}) {
    const start = this.tokenStart;
    let children = this.createList();

    this.eat(types.LeftCurlyBracket);

    scan:
    while (!this.eof) {
        switch (this.tokenType) {
            case types.RightCurlyBracket:
                break scan;

            case types.WhiteSpace:
            case types.Comment:
                this.next();
                break;

            case types.AtKeyword:
                children.push(this.parseWithFallback(this.Atrule.bind(this, isStyleBlock, { allowNestedRules }), consumeRaw));
                break;

            default:
                if (isStyleBlock) {

                    if (allowNestedRules && isSelectorStart.call(this)) {
                        children.push(consumeRule.call(this));
                    } else {
                        children.push(consumeDeclaration.call(this));
                    }

                } else {
                    children.push(consumeRule.call(this));
                }
        }
    }

    if (!this.eof) {
        this.eat(types.RightCurlyBracket);
    }

    return {
        type: 'Block',
        loc: this.getLocation(start, this.tokenStart),
        children
    };
}

function generate(node) {
    this.token(types.LeftCurlyBracket, '{');
    this.children(node, prev => {
        if (prev.type === 'Declaration') {
            this.token(types.Semicolon, ';');
        }
    });
    this.token(types.RightCurlyBracket, '}');
}

exports.generate = generate;
exports.name = name;
exports.parse = parse;
exports.structure = structure;
exports.walkContext = walkContext;
