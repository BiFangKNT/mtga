import { ArgumentHandler, OptionHandler } from "./index.mjs";

//#region src/shared.d.ts
interface CompletionConfig {
  subCommands?: Record<string, CompletionConfig>;
  options?: Record<string, OptionHandler>;
  args?: Record<string, ArgumentHandler>;
}
//#endregion
export { CompletionConfig as t };