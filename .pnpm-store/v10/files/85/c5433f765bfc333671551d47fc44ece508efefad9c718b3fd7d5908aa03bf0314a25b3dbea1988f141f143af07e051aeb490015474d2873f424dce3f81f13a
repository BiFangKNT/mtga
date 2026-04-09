import { Linter } from "eslint";

//#region src/dts/rule-options.d.ts
interface RuleOptions {
  /**
   * Enforce or ban the use of inline type-only markers for named imports.
   * @see https://github.com/9romise/eslint-plugin-import-lite/blob/main/src/rules/consistent-type-specifier-style/README.md
   */
  'import-lite/consistent-type-specifier-style'?: Linter.RuleEntry<ImportLiteConsistentTypeSpecifierStyle>;
  /**
   * Ensure all exports appear after other statements.
   * @see https://github.com/9romise/eslint-plugin-import-lite/blob/main/src/rules/exports-last/README.md
   */
  'import-lite/exports-last'?: Linter.RuleEntry<[]>;
  /**
   * Ensure all imports appear before other statements.
   * @see https://github.com/9romise/eslint-plugin-import-lite/blob/main/src/rules/first/README.md
   */
  'import-lite/first'?: Linter.RuleEntry<ImportLiteFirst>;
  /**
   * Enforce a newline after import statements.
   * @see https://github.com/9romise/eslint-plugin-import-lite/blob/main/src/rules/newline-after-import/README.md
   */
  'import-lite/newline-after-import'?: Linter.RuleEntry<ImportLiteNewlineAfterImport>;
  /**
   * Forbid default exports.
   * @see https://github.com/9romise/eslint-plugin-import-lite/blob/main/src/rules/no-default-export/README.md
   */
  'import-lite/no-default-export'?: Linter.RuleEntry<[]>;
  /**
   * Forbid repeated import of the same module in multiple places.
   * @see https://github.com/9romise/eslint-plugin-import-lite/blob/main/src/rules/no-duplicates/README.md
   */
  'import-lite/no-duplicates'?: Linter.RuleEntry<ImportLiteNoDuplicates>;
  /**
   * Forbid the use of mutable exports with `var` or `let`.
   * @see https://github.com/9romise/eslint-plugin-import-lite/blob/main/src/rules/no-mutable-exports/README.md
   */
  'import-lite/no-mutable-exports'?: Linter.RuleEntry<[]>;
  /**
   * Forbid named default exports.
   * @see https://github.com/9romise/eslint-plugin-import-lite/blob/main/src/rules/no-named-default/README.md
   */
  'import-lite/no-named-default'?: Linter.RuleEntry<[]>;
  /**
   * Prefer a default export if module exports a single name or multiple names.
   * @see https://github.com/9romise/eslint-plugin-import-lite/blob/main/src/rules/prefer-default-export/README.md
   */
  'import-lite/prefer-default-export'?: Linter.RuleEntry<ImportLitePreferDefaultExport>;
}
/* ======= Declarations ======= */
// ----- import-lite/consistent-type-specifier-style -----
type ImportLiteConsistentTypeSpecifierStyle = [] | [("top-level" | "inline" | "prefer-top-level")]; // ----- import-lite/first -----
type ImportLiteFirst = [] | [("absolute-first" | "disable-absolute-first")]; // ----- import-lite/newline-after-import -----
type ImportLiteNewlineAfterImport = [] | [{
  count?: number;
  exactCount?: boolean;
  considerComments?: boolean;
}]; // ----- import-lite/no-duplicates -----
type ImportLiteNoDuplicates = [] | [{
  "prefer-inline"?: boolean;
}]; // ----- import-lite/prefer-default-export -----
type ImportLitePreferDefaultExport = [] | [{
  target?: ("single" | "any");
}];
//#endregion
export { RuleOptions };