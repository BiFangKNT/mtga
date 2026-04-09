import { CommandDef } from "citty";

//#region src/main.d.ts
declare const main: CommandDef<any>;
//#endregion
//#region src/run.d.ts
declare function runMain(): Promise<void>;
declare function runCommand(name: string, argv?: string[], data?: {
  overrides?: Record<string, any>;
}): Promise<{
  result: unknown;
}>;
//#endregion
export { main, runCommand, runMain };