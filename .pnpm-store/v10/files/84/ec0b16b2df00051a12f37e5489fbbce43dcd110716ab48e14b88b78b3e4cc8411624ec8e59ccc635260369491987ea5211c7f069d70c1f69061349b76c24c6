import {
    WhiteSpace,
    Comment,
    Delim,
    Semicolon,
    Hash,
    Colon,
    Ident,
    AtKeyword,
    LeftSquareBracket,
    LeftCurlyBracket,
    RightCurlyBracket
} from '../../tokenizer/index.js';

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
    if (this.tokenType === Semicolon) {
        return consumeRawDeclaration.call(this, this.tokenIndex);
    }

    const node = this.parseWithFallback(this.Declaration, consumeRawDeclaration);

    if (this.tokenType === Semicolon) {
        this.next();
    }

    return node;
}

function isElementSelectorStart() {
    if (this.tokenType !== Ident) {
        return false;
    }

    const nextTokenType = this.lookupTypeNonSC(1);

    if (nextTokenType !== Colon && nextTokenType !== Semicolon && nextTokenType !== RightCurlyBracket) {
        return true;
    }

    return false;
}

function isSelectorStart() {
    // Check for Delim tokens that might be selector starts
    if (this.tokenType === Delim && selectorStarts.has(this.source.charCodeAt(this.tokenStart))) {
        const code = this.source.charCodeAt(this.tokenStart);

        // Special case: browser hack prefixes (*, +, &) followed immediately by an ident
        // (no whitespace) are declarations, not selectors. Examples: *zoom: 1; +width: 100px; &prop: value;
        if (code === STAR || code === PLUSSIGN || code === AMPERSAND) {
            const nextToken = this.lookupType(1);
            const nextTokenNonSC = this.lookupTypeNonSC(1);

            // If next token is Ident and there's no whitespace between, it's a declaration
            if (nextToken === Ident && nextTokenNonSC === Ident) {
                return false;
            }
        }
        return true;
    }

    // Hash can be either a Hash token (#id selector) or Delim(#) + Ident (browser hack)
    // When it's a Hash token, it's a selector. When it's Delim, check if followed by Ident without whitespace
    if (this.tokenType === Hash) {
        return true;
    }

    return this.tokenType === LeftSquareBracket ||
        this.tokenType === Colon || isElementSelectorStart.call(this);
}

export const name = 'Block';
export const walkContext = 'block';
export const structure = {
    children: [[
        'Atrule',
        'Rule',
        'Declaration'
    ]]
};

export function parse(isStyleBlock, { allowNestedRules = false } = {}) {
    const start = this.tokenStart;
    let children = this.createList();

    this.eat(LeftCurlyBracket);

    scan:
    while (!this.eof) {
        switch (this.tokenType) {
            case RightCurlyBracket:
                break scan;

            case WhiteSpace:
            case Comment:
                this.next();
                break;

            case AtKeyword:
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
        this.eat(RightCurlyBracket);
    }

    return {
        type: 'Block',
        loc: this.getLocation(start, this.tokenStart),
        children
    };
}

export function generate(node) {
    this.token(LeftCurlyBracket, '{');
    this.children(node, prev => {
        if (prev.type === 'Declaration') {
            this.token(Semicolon, ';');
        }
    });
    this.token(RightCurlyBracket, '}');
}
