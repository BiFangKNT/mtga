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
    return this.Raw(this.consumeUntilSemicolonIncluded, true);
}

function isElementSelectorStart() {
    if (this.tokenType !== types.Ident) {
        return false;
    }

    const nextTokenType = this.lookupTypeNonSC(1);

    // If next token is a left curly bracket, it's definitely a selector (e.g., "div { ... }")
    if (nextTokenType === types.LeftCurlyBracket) {
        return true;
    }

    // If next token is semicolon, comma, or closing brace, it's definitely a declaration
    if (nextTokenType === types.Semicolon || nextTokenType === types.Comma || nextTokenType === types.RightCurlyBracket) {
        return false;
    }

    // Special handling for colon case - could be pseudo-class/pseudo-element or property
    if (nextTokenType === types.Colon) {
        // Look ahead further to see what follows the colon
        const afterColonType = this.lookupTypeNonSC(2);

        // If after colon there's an identifier (pseudo-class/pseudo-element name),
        // check what comes after that
        if (afterColonType === types.Ident) {
            const afterPseudoType = this.lookupTypeNonSC(3);
            // If it's followed by {, it's definitely a selector (e.g., "div:hover { ... }")
            if (afterPseudoType === types.LeftCurlyBracket) {
                return true;
            }
            // Otherwise, it's a property (e.g., "transition: opacity 1s")
            return false;
        }
        // If after colon there's not an identifier, it's a property
        return false;
    }

    // For other token types (dimensions, numbers, strings, etc.), assume it's a declaration
    // This handles cases like multi-value properties
    return false;
}

function isSelectorStart() {
    return this.tokenType === types.Delim && selectorStarts.has(this.source.charCodeAt(this.tokenStart)) ||
        this.tokenType === types.Hash || this.tokenType === types.LeftSquareBracket ||
        this.tokenType === types.Colon || isElementSelectorStart.call(this);
}

const name = 'DeclarationList';
const structure = {
    children: [[
        'Declaration',
        'Atrule',
        'Rule'
    ]]
};

function parse() {
    const children = this.createList();

    while (!this.eof) {
        switch (this.tokenType) {
            case types.WhiteSpace:
            case types.Comment:
            case types.Semicolon:
                this.next();
                break;

            case types.AtKeyword:
                children.push(this.parseWithFallback(this.Atrule.bind(this, true), consumeRaw));
                break;

            default:
                if (isSelectorStart.call(this))  {
                    children.push(this.parseWithFallback(this.Rule, consumeRaw));
                } else {
                    children.push(this.parseWithFallback(this.Declaration, consumeRaw));
                }
        }
    }

    return {
        type: 'DeclarationList',
        loc: this.getLocationFromList(children),
        children
    };
}

function generate(node) {
    this.children(node, prev => {
        if (prev.type === 'Declaration') {
            this.token(types.Semicolon, ';');
        }
    });
}

exports.generate = generate;
exports.name = name;
exports.parse = parse;
exports.structure = structure;
