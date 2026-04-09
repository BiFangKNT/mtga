import useColors from "@poppinss/colors";
const ANSI_REGEX = new RegExp([`[\\u001B\\u009B][[\\]()#;?]*(?:(?:(?:(?:;[-a-zA-Z\\d\\/#&.:=?%@~_]+)*|[a-zA-Z\\d]+(?:;[-a-zA-Z\\d\\/#&.:=?%@~_]*)*)?(?:\\u0007|\\u001B\\u005C|\\u009C))`, "(?:(?:\\d{1,4}(?:;\\d{0,4})*)?[\\dA-PR-TZcf-nq-uy=><~]))"].join("|"), "g");
function htmlEscape(value) {
	return value.replace(/&/g, "&amp;").replace(/\\"/g, "&bsol;&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
function wordWrap(value, options) {
	const width = options.width;
	const indent = options.indent;
	const newLine = `${options.newLine}${indent}`;
	if (!width) return options.escape ? options.escape(value) : htmlEscape(value);
	let regexString = ".{1," + width + "}";
	regexString += "([\\s​]+|$)|[^\\s​]+?([\\s​]+|$)";
	const re = new RegExp(regexString, "g");
	return (value.match(re) || []).map(function(line) {
		if (line.slice(-1) === "\n") line = line.slice(0, line.length - 1);
		return options.escape ? options.escape(line) : htmlEscape(line);
	}).join(newLine);
}
function stripAnsi(value) {
	return value.replace(ANSI_REGEX, "");
}
const colors = useColors.ansi();
export { wordWrap as i, htmlEscape as n, stripAnsi as r, colors as t };
