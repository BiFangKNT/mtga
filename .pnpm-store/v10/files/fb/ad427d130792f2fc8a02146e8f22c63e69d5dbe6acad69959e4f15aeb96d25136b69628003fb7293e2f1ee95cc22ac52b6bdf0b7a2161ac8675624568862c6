'use strict';

const types = require('../../tokenizer/types.cjs');

const ASTERISK = 0x002A;     // U+002A ASTERISK (*)
const VERTICALLINE = 0x007C; // U+007C VERTICAL LINE (|)

function eatIdentifierOrAsterisk() {
    if (this.tokenType !== types.Ident &&
        this.isDelim(ASTERISK) === false) {
        this.error('Identifier or asterisk is expected');
    }

    // Check if asterisk is followed immediately by an ident (no whitespace)
    // This is invalid in selectors (e.g., "*foo" should error, "* foo" or "*:hover" is ok)
    if (this.isDelim(ASTERISK)) {
        const currentTokenEnd = this.tokenStart + 1; // asterisk is 1 char
        this.next();

        // If next token is an ident and starts immediately after asterisk, it's an error
        if (this.tokenType === types.Ident && this.tokenStart === currentTokenEnd) {
            this.error('Whitespace is required between universal selector and type selector');
        }

        return;
    }

    this.next();
}

const name = 'TypeSelector';
const structure = {
    name: String
};

// ident
// ident|ident
// ident|*
// *
// *|ident
// *|*
// |ident
// |*
function parse() {
    const start = this.tokenStart;

    if (this.isDelim(VERTICALLINE)) {
        this.next();
        eatIdentifierOrAsterisk.call(this);
    } else {
        eatIdentifierOrAsterisk.call(this);

        if (this.isDelim(VERTICALLINE)) {
            this.next();
            eatIdentifierOrAsterisk.call(this);
        }
    }

    return {
        type: 'TypeSelector',
        loc: this.getLocation(start, this.tokenStart),
        name: this.substrToCursor(start)
    };
}

function generate(node) {
    this.tokenize(node.name);
}

exports.generate = generate;
exports.name = name;
exports.parse = parse;
exports.structure = structure;
