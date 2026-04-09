//#region src/t.d.ts
declare const ShellCompDirective: {
  ShellCompDirectiveError: number;
  ShellCompDirectiveNoSpace: number;
  ShellCompDirectiveNoFileComp: number;
  ShellCompDirectiveFilterFileExt: number;
  ShellCompDirectiveFilterDirs: number;
  ShellCompDirectiveKeepOrder: number;
  shellCompDirectiveMaxValue: number;
  ShellCompDirectiveDefault: number;
};
type OptionsMap = Map<string, Option>;
type Complete = (value: string, description: string) => void;
type OptionHandler = (this: Option, complete: Complete, options: OptionsMap) => void;
interface Completion {
  description?: string;
  value: string;
}
type ArgumentHandler = (this: Argument, complete: Complete, options: OptionsMap) => void;
declare class Argument {
  name: string;
  variadic: boolean;
  command: Command;
  handler?: ArgumentHandler;
  constructor(command: Command, name: string, handler?: ArgumentHandler, variadic?: boolean);
}
declare class Option {
  value: string;
  description: string;
  command: Command;
  handler?: OptionHandler;
  alias?: string;
  isBoolean?: boolean;
  constructor(command: Command, value: string, description: string, handler?: OptionHandler, alias?: string, isBoolean?: boolean);
}
declare class Command {
  value: string;
  description: string;
  options: Map<string, Option>;
  arguments: Map<string, Argument>;
  parent?: Command;
  constructor(value: string, description: string);
  option(value: string, description: string, handlerOrAlias?: OptionHandler | string, alias?: string): Command;
  argument(name: string, handler?: ArgumentHandler, variadic?: boolean): this;
}
declare class RootCommand extends Command {
  commands: Map<string, Command>;
  completions: Completion[];
  directive: number;
  constructor();
  command(value: string, description: string): Command;
  private stripOptions;
  private matchCommand;
  private shouldCompleteFlags;
  private shouldCompleteCommands;
  private handleFlagCompletion;
  private findOption;
  private handleCommandCompletion;
  private handlePositionalCompletion;
  private complete;
  parse(args: string[]): void;
  setup(name: string, executable: string, shell: string): void;
}
declare const t: RootCommand;
declare function script(shell: string, name: string, executable: string): void;
//#endregion
export { Argument, ArgumentHandler, Command, Complete, Completion, Option, OptionHandler, OptionsMap, RootCommand, ShellCompDirective, t as default, script };