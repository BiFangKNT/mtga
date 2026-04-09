export default {
    parse: {
        prelude() {
            return this.createSingleNodeList(
                this.MediaQueryList()
            );
        },
        block(nested = false, { allowNestedRules = false } = {}) {
            return this.Block(nested, { allowNestedRules });
        }
    }
};
