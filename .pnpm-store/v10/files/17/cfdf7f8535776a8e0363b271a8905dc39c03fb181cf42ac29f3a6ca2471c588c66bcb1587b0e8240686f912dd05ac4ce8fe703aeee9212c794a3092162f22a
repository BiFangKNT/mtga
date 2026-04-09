'use strict';

const index = require('../tokenizer/index.cjs');

const FUNCTION_TYPE = 'function';

/**
 * Gets the tokenizer function from the configuration object or returns the default tokenizer
 *
 * @param config Configuration object
 * @returns Corresponding tokenizer function
 */
function getTokenizer(config) {
    if (config && typeof config.tokenize === FUNCTION_TYPE) {
        return config.tokenize;
    }

    // Fallback to the default tokenizer
    return index.tokenize;
}

exports.getTokenizer = getTokenizer;
