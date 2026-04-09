const IS_ABSOLUTE_RE = /^[/\\](?![/\\])|^[/\\]{2}(?!\.)|^[a-z]:[/\\]/i;
const LINE_RE = /^\s+at (?:(?<function>[^)]+) \()?(?<source>[^)]+)\)?$/u;
const SOURCE_RE = /^(?<source>.+):(?<line>\d+):(?<column>\d+)$/u;
function captureRawStackTrace() {
  if (!Error.captureStackTrace) {
    return;
  }
  const stack = new Error();
  Error.captureStackTrace(stack);
  return stack.stack;
}
function captureStackTrace() {
  const stack = captureRawStackTrace();
  return stack ? parseRawStackTrace(stack) : [];
}
function parseRawStackTrace(stacktrace) {
  const trace = [];
  for (const line of stacktrace.split("\n")) {
    const parsed = LINE_RE.exec(line)?.groups;
    if (!parsed) {
      continue;
    }
    if (!parsed.source) {
      continue;
    }
    const parsedSource = SOURCE_RE.exec(parsed.source)?.groups;
    if (parsedSource) {
      Object.assign(parsed, parsedSource);
    }
    if (IS_ABSOLUTE_RE.test(parsed.source)) {
      parsed.source = `file://${parsed.source}`;
    }
    if (parsed.source === import.meta.url) {
      continue;
    }
    for (const key of ["line", "column"]) {
      if (parsed[key]) {
        parsed[key] = Number(parsed[key]);
      }
    }
    trace.push(parsed);
  }
  return trace;
}

export { captureRawStackTrace, captureStackTrace, parseRawStackTrace };
