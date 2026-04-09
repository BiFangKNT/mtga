declare namespace _default {
    namespace parse {
        let prelude: SyntaxConfig["atrule"]["import"]["parse"]["prelude"];
        let block: null;
    }
}
export default _default;
export type ConsumerNames = "Raw" | "Layer" | "Condition" | "Declaration" | "String" | "Identifier" | "Url" | "Function" | "MediaQueryList";
export type ParserContext = BaseParserContext & { [key in ConsumerNames]: ConsumerFunction; };
import type { SyntaxConfig } from "@eslint/css-tree";
import type { ParserContext as BaseParserContext } from "@eslint/css-tree";
import type { ConsumerFunction } from "@eslint/css-tree";
