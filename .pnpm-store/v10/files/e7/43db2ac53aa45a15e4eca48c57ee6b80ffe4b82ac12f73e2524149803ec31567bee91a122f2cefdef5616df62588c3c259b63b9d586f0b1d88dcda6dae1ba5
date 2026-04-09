import * as unplugin from "unplugin";

//#region src/index.d.ts
interface ImpoundTraceStep {
  /** The file path in this step of the import chain. */
  file: string;
  /** The import specifier used (if not entry). */
  import?: string;
  /** Line number of the import statement (1-indexed, if available). */
  line?: number;
  /** Column number of the import statement (0-indexed, if available). */
  column?: number;
}
interface ImpoundSnippet {
  /** Formatted code snippet with line numbers, `>` marker, and `^` caret. */
  text: string;
  /** The line number of the offending import (1-indexed). */
  line: number;
  /** The column number of the offending import (0-indexed). */
  column: number;
}
interface ImpoundViolationInfo {
  /** The resolved import specifier that was denied. */
  id: string;
  /** The file that contains the denied import. */
  importer: string;
  /** The formatted error message. */
  message: string;
  /** Import chain from entry to violation (when trace is enabled). */
  trace?: ImpoundTraceStep[];
  /** Source code snippet around the offending import (when trace is enabled). */
  snippet?: ImpoundSnippet;
}
interface ImpoundMatcherOptions {
  /** An array of patterns of importers to apply the import protection rules to. */
  include?: Array<string | RegExp>;
  /** An array of patterns of importers where the import protection rules explicitly do not apply. */
  exclude?: Array<string | RegExp>;
  /** Whether to throw an error or not. if set to `false`, an error will be logged to console instead. */
  error?: boolean;
  /**
   * Controls whether duplicate warnings are logged when `error` is `false`.
   * - `'once'` (default): each unique violation is logged only once.
   * - `'always'`: every violation is logged, even if repeated.
   *
   * This has no effect when `error` is `true` (the default), since the build fails on the first violation.
   */
  warn?: 'once' | 'always';
  /**
   * Callback invoked on every violation. Receives the violation details.
   * Return `false` to allow the import and suppress the default error/warning.
   */
  onViolation?: (info: ImpoundViolationInfo) => boolean | void;
  /**
   * An array of patterns matching resolved import targets that should be excluded from pattern checks.
   * Useful for skipping false positives from third-party packages, e.g. node_modules.
   */
  excludeFiles?: Array<string | RegExp>;
  /** An array of patterns to prevent being imported, along with an optional warning and suggestions to display.  */
  patterns: [importPattern: string | RegExp | ((id: string, importer: string) => boolean | string), warning?: string, suggestions?: string[]][];
}
interface ImpoundSharedOptions {
  cwd?: string;
  /**
   * Enable import tracing and code snippets in violation reports.
   * Violations are reported eagerly with best-effort trace enrichment
   * from the module graph collected so far.
   */
  trace?: boolean;
  /**
   * Maximum depth for import traces. Only used when `trace` is `true`.
   * @default 20
   */
  maxTraceDepth?: number;
}
type ImpoundOptions = (ImpoundSharedOptions & ImpoundMatcherOptions) | (ImpoundSharedOptions & {
  matchers: ImpoundMatcherOptions[];
});
declare const ImpoundPlugin: unplugin.UnpluginInstance<ImpoundOptions, boolean>;
//#endregion
export { ImpoundMatcherOptions, ImpoundOptions, ImpoundPlugin, ImpoundSharedOptions, ImpoundSnippet, ImpoundTraceStep, ImpoundViolationInfo };