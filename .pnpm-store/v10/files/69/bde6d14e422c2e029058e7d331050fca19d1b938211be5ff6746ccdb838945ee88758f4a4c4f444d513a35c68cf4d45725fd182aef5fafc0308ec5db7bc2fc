/**
 * @param {string} str
 * @returns {string}
 */
const toCamelCase = (str) => {
  return str.toLowerCase().replaceAll(/^[a-z]/gv, (init) => {
    return init.toUpperCase();
  }).replaceAll(/_(?<wordInit>[a-z])/gv, (_, n1, o, s, {wordInit}) => {
    return wordInit.toUpperCase();
  });
};

export {toCamelCase};
