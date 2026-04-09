import process from "node:process";
import { colors } from "consola/utils";
import { stripVTControlCharacters } from "node:util";

//#region ../nuxi/src/utils/formatting.ts
const AT_MENTION_RE = /\b@([^, ]+)/g;
const BACKTICK_RE = /`([^`]*)`/g;
function getStringWidth(str) {
	const stripped = stripVTControlCharacters(str);
	let width = 0;
	for (const char of stripped) {
		const code = char.codePointAt(0);
		if (!code) continue;
		if (code >= 65024 && code <= 65039) continue;
		if (code >= 127744 && code <= 129535 || code >= 128512 && code <= 128591 || code >= 128640 && code <= 128767 || code >= 9728 && code <= 9983 || code >= 9984 && code <= 10175 || code >= 129280 && code <= 129535 || code >= 129648 && code <= 129791) width += 2;
		else width += 1;
	}
	return width;
}
function formatInfoBox(infoObj) {
	let firstColumnLength = 0;
	let ansiFirstColumnLength = 0;
	const entries = Object.entries(infoObj).map(([label, val]) => {
		if (label.length > firstColumnLength) {
			ansiFirstColumnLength = colors.bold(colors.whiteBright(label)).length + 6;
			firstColumnLength = label.length + 6;
		}
		return [label, val || "-"];
	});
	const terminalWidth = Math.max(process.stdout.columns || 80, firstColumnLength) - 8;
	let boxStr = "";
	for (const [label, value] of entries) {
		const formattedValue = value.replace(AT_MENTION_RE, (_, r) => colors.gray(` ${r}`)).replace(BACKTICK_RE, (_, r) => r);
		boxStr += `${colors.bold(colors.whiteBright(label))}`.padEnd(ansiFirstColumnLength);
		let boxRowLength = firstColumnLength;
		const words = formattedValue.split(" ");
		let currentLine = "";
		for (const word of words) {
			const wordLength = getStringWidth(word);
			const spaceLength = currentLine ? 1 : 0;
			if (boxRowLength + wordLength + spaceLength > terminalWidth) {
				if (currentLine) boxStr += colors.cyan(currentLine);
				boxStr += `\n${" ".repeat(firstColumnLength)}`;
				currentLine = word;
				boxRowLength = firstColumnLength + wordLength;
			} else {
				currentLine += (currentLine ? " " : "") + word;
				boxRowLength += wordLength + spaceLength;
			}
		}
		if (currentLine) boxStr += colors.cyan(currentLine);
		boxStr += "\n";
	}
	return boxStr;
}

//#endregion
export { formatInfoBox as t };