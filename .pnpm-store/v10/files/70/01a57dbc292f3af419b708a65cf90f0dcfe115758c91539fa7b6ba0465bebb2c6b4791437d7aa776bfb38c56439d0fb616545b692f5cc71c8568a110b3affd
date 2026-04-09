import { FlatConfigsToRulesOptions } from "./core.mjs";
import { Linter } from "eslint";

//#region src/index.d.ts
interface TypeGenOptions extends FlatConfigsToRulesOptions {
  /**
   * Include core rules in the generated types.
   *
   * @default true
   */
  includeCoreRules?: boolean;
  /**
   * Path to the generated types file.
   */
  dtsPath?: string;
}
/**
 * Wrap with resolved flat configs to generates types for rules.
 */
declare function typegen(configs: Promise<Linter.Config[]> | Linter.Config[], options?: TypeGenOptions): Promise<Linter.Config[]>;
//#endregion
export { TypeGenOptions, typegen as default };