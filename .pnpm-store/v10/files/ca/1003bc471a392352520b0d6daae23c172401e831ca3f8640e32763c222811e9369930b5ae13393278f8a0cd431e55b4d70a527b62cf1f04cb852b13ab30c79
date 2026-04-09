import os from "node:os";
import { codeFrameColumns } from "@babel/code-frame";
function createFrame(source, location) {
  return codeFrameColumns(source, location, {
    // worker tty did not fork parent process stdout, let's make a workaround
    forceColor: true
  }).split("\n").map((line) => `  ${line}`).join(os.EOL);
}
function tsLikeLocToBabelLoc(tsLoc) {
  return {
    start: { line: tsLoc.start.line + 1, column: tsLoc.start.character + 1 },
    end: { line: tsLoc.end.line + 1, column: tsLoc.end.character + 1 }
  };
}
function lineColLocToBabelLoc(d) {
  return {
    start: { line: d.line, column: d.column },
    end: { line: d.endLine || 0, column: d.endColumn }
  };
}
function offsetRangeToBabelLocation(source, offset, length) {
  const defaultPos = { line: 1, column: 1 };
  if (!source || source.length === 0) {
    return { start: { ...defaultPos }, end: { ...defaultPos } };
  }
  const startIndex = offset;
  const endIndex = offset + length;
  let line = 1;
  let column = 1;
  let start = null;
  for (let i = 0; i < endIndex; i++) {
    if (i === startIndex) {
      start = { line, column };
    }
    if (source[i] === "\n") {
      line++;
      column = 1;
    } else {
      column++;
    }
  }
  start ?? (start = { line, column });
  const end = { line, column };
  return { start, end };
}
export {
  createFrame,
  lineColLocToBabelLoc,
  offsetRangeToBabelLocation,
  tsLikeLocToBabelLoc
};
//# sourceMappingURL=codeFrame.js.map