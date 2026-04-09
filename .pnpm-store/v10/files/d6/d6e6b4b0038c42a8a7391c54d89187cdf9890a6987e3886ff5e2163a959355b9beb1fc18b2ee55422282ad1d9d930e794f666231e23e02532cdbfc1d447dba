import {stringify as prattStringify} from 'jsdoc-type-pratt-parser';

/* eslint-disable jsdoc/reject-function-type -- Different functions */
/** @type {Record<string, Function>} */
const stringifiers = {
  /* eslint-enable jsdoc/reject-function-type -- Different functions */
  JsdocBlock,

  /**
   * @param {import('./commentParserToESTree').JsdocDescriptionLine} node
   * @returns {string}
   */
  JsdocDescriptionLine ({
    initial, delimiter, postDelimiter, description
  }) {
    return `${initial}${delimiter}${postDelimiter}${description}`;
  },

  /**
   * @param {import('./commentParserToESTree').JsdocTypeLine} node
   * @returns {string}
   */
  JsdocTypeLine ({
    initial, delimiter, postDelimiter, rawType
  }) {
    return `${initial}${delimiter}${postDelimiter}${rawType}`;
  },

  /**
   * @param {import('./commentParserToESTree').JsdocInlineTag} node
   */
  JsdocInlineTag ({format, namepathOrURL, tag, text}) {
    return format === 'pipe'
      ? `{@${tag} ${namepathOrURL}|${text}}`
      : format === 'plain'
        ? `{@${tag} ${namepathOrURL}}`
        : format === 'prefix'
          ? `[${text}]{@${tag} ${namepathOrURL}}`
          // "space"
          : `{@${tag} ${namepathOrURL} ${text}}`;
  },

  JsdocTag
};

/**
 * @todo convert for use by escodegen (until may be patched to support
 *   custom entries?).
 * @param {import('./commentParserToESTree').JsdocBlock|
 *   import('./commentParserToESTree').JsdocDescriptionLine|
 *   import('./commentParserToESTree').JsdocTypeLine|
 *   import('./commentParserToESTree').JsdocTag|
 *   import('./commentParserToESTree').JsdocInlineTag|
 *   import('jsdoc-type-pratt-parser').RootResult
 * } node
 * @param {import('.').ESTreeToStringOptions} [opts]
 * @throws {Error}
 * @returns {string}
 */
function estreeToString (node, opts = {}) {
  if (Object.hasOwn(stringifiers, node.type)) {
    return stringifiers[
      /**
       * @type {import('./commentParserToESTree').JsdocBlock|
       *   import('./commentParserToESTree').JsdocDescriptionLine|
       *   import('./commentParserToESTree').JsdocTypeLine|
       *   import('./commentParserToESTree').JsdocTag}
       */
      (node).type
    ](
      node,
      opts
    );
  }

  // We use raw type instead but it is a key as other apps may wish to traverse
  if (node.type.startsWith('JsdocType')) {
    return opts.preferRawType
      ? ''
      : `{${prattStringify(
        /** @type {import('jsdoc-type-pratt-parser').RootResult} */ (
          node
        ),
        opts.jtppStringificationRules
      )}}`;
  }

  throw new Error(`Unhandled node type: ${node.type}`);
}

/**
 * @param {import('./commentParserToESTree').JsdocBlock} node
 * @param {import('.').ESTreeToStringOptions} opts
 * @returns {string}
 */
function JsdocBlock (node, opts) {
  const {delimiter, delimiterLineBreak, descriptionLines,
    initial, postDelimiter, preterminalLineBreak, tags, terminal} = node;

  const terminalPrepend = preterminalLineBreak !== ''
    ? `${preterminalLineBreak}${initial} `
    : '';

  let result = `${initial}${delimiter}${postDelimiter}${delimiterLineBreak}`;

  for (let i = 0; i < descriptionLines.length; i++) {
    result += estreeToString(descriptionLines[i]);

    if (i !== descriptionLines.length - 1 || tags.length) {
      result += '\n';
    }
  }

  for (let i = 0; i < tags.length; i++) {
    result += estreeToString(tags[i], opts);

    if (i !== tags.length - 1) {
      result += '\n';
    }
  }

  result += `${terminalPrepend}${terminal}`;

  return result;
}

/**
 * @param {import('./commentParserToESTree').JsdocTag} node
 * @param {import('.').ESTreeToStringOptions} opts
 * @returns {string}
 */
function JsdocTag (node, opts) {
  const {
    delimiter, descriptionLines, initial, name, parsedType, postDelimiter,
    postName, postTag, postType, tag, typeLines
  } = node;

  let result = `${initial}${delimiter}${postDelimiter}@${tag}${postTag}`;

  // Could do `rawType` but may have been changed; could also do
  //   `typeLines` but not as likely to be changed
  // parsedType
  // Comment this out later in favor of `parsedType`
  // We can't use raw `typeLines` as first argument has delimiter on it
  if (opts.preferRawType || !parsedType) {
    if (typeLines.length) {
      result += '{';

      for (let i = 0; i < typeLines.length; i++) {
        result += estreeToString(typeLines[i]);

        if (i !== typeLines.length - 1) {
          result += '\n';
        }
      }

      result += '}';
    }
    /* v8 ignore start */
  } else if (parsedType?.type.startsWith('JsdocType')) {
    result += `{${prattStringify(
      /** @type {import('jsdoc-type-pratt-parser').RootResult} */ (
        parsedType
      )
    )}}`;
    /* v8 ignore stop */
  }

  // Check if the name appears on a separate line from the tag/type
  // This is indicated by postTag and postType both being empty
  let nameLineOffset = 0;
  if (name && postTag === '' && postType === '') {
    // The name is on a separate line from the tag
    result += '\n';

    if (descriptionLines.length > 0) {
      const firstDescLine = descriptionLines[0];
      /* v8 ignore next 3 */
      if (firstDescLine.description === '' && firstDescLine.delimiter === '' &&
          firstDescLine.postDelimiter === '' && firstDescLine.initial === '') {
        // Empty first line, check if there's a second line with formatting
        if (descriptionLines.length > 1) {
          const nameLine = descriptionLines[1];
          result += `${
            nameLine.initial
          }${nameLine.delimiter}${
            nameLine.postDelimiter
          }${name}${postName}${
            nameLine.description
          }`;
          nameLineOffset = 2;
        } else {
          /* v8 ignore start */
          // Fallback: just add name (shouldn't normally happen)
          result += name + postName;
          nameLineOffset = 1;
          /* v8 ignore stop */
        }
      } else {
        /* v8 ignore start */
        // First description line has content, use it for the name line
        const nameLine = descriptionLines[0];
        result += `${nameLine.initial}${
          nameLine.delimiter
        }${nameLine.postDelimiter}${name}${postName}${nameLine.description}`;
        nameLineOffset = 1;
        /* v8 ignore stop */
      }
    } else {
      // No description lines, need to construct the name line
      // Use the same formatting as the tag line
      result += `${initial}${delimiter}${postDelimiter}${name}${postName}`;
    }
  } else {
    result += name ? `${postType}${name}${postName}` : postType;
  }

  for (let i = nameLineOffset; i < descriptionLines.length; i++) {
    const descriptionLine = descriptionLines[i];

    if (i > 0 || nameLineOffset > 0) {
      result += '\n';
    }

    result += estreeToString(descriptionLine);
  }

  return result;
}

export {estreeToString};
