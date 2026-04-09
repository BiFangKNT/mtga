/**
 * @fileoverview Tailwind 3 @apply rule parser
 * @author Nicholas C. Zakas
 */
//-----------------------------------------------------------------------------
// Imports
//-----------------------------------------------------------------------------
import { tokenTypes } from "@eslint/css-tree";
//-----------------------------------------------------------------------------
// Type Definitions
//-----------------------------------------------------------------------------
/**
 * @import { ParserContext, ConsumerFunction } from "@eslint/css-tree";
 *
 */
//-----------------------------------------------------------------------------
// Exports
//-----------------------------------------------------------------------------
export default {
    parse: {
        /**
         * @this {ParserContext}
         */
        prelude: function () {
            const children = this.createList();
            while (this.tokenType === tokenTypes.Ident) {
                if (this.lookupType(1) === tokenTypes.Colon) {
                    children.push(/** @type {ConsumerFunction} */ (this.TailwindUtilityClass)());
                }
                else {
                    children.push(/** @type {ConsumerFunction} */ (this.Identifier)());
                }
                this.skipSC();
            }
            return children;
        },
        block: null
    }
};
