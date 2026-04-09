function parseArgsStringToArgv(value, env, file) {
  const myRegexp = (
    // @ts-expect-error Bypass typescript validation
    // biome-ignore lint/complexity/noUselessEscapeInRegex: Bypass validation
    /([^\s'"]([^\s'"]*(['"])([^\3]*?)\3)+[^\s'"]*)|[^\s'"]+|(['"])([^\5]*?)\5/gi
  );
  const myString = value;
  const myArray = [];
  if (env) {
    myArray.push(env);
  }
  if (file) {
    myArray.push(file);
  }
  let match;
  do {
    match = myRegexp.exec(myString);
    if (match !== null) {
      myArray.push(firstString(match[1], match[6], match[0]));
    }
  } while (match !== null);
  return myArray;
}
function firstString(...args) {
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (typeof arg === "string") {
      return arg;
    }
  }
}
export {
  parseArgsStringToArgv as default,
  parseArgsStringToArgv
};
//# sourceMappingURL=argv.js.map