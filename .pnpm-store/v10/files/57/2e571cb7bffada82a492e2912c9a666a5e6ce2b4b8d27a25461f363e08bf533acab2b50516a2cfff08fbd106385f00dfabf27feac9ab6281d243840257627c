//#region src/types.d.ts
type ArgType = "boolean" | "string" | "enum" | "positional" | undefined;
type _ArgDef<T extends ArgType, VT extends boolean | number | string> = {
  type?: T;
  description?: string;
  valueHint?: string;
  alias?: string | string[];
  default?: VT;
  required?: boolean;
  options?: string[];
};
type BooleanArgDef = Omit<_ArgDef<"boolean", boolean>, "options"> & {
  negativeDescription?: string;
};
type StringArgDef = Omit<_ArgDef<"string", string>, "options">;
type EnumArgDef = _ArgDef<"enum", string>;
type PositionalArgDef = Omit<_ArgDef<"positional", string>, "alias" | "options">;
type ArgDef = BooleanArgDef | StringArgDef | PositionalArgDef | EnumArgDef;
type ArgsDef = Record<string, ArgDef>;
type Arg = ArgDef & {
  name: string;
  alias: string[];
};
type ResolveParsedArgType<T extends ArgDef, VT> = T extends {
  default?: any;
  required?: boolean;
} ? T["default"] extends NonNullable<VT> ? VT : T["required"] extends true ? VT : VT | undefined : VT | undefined;
type ParsedPositionalArg<T extends ArgDef> = T extends {
  type: "positional";
} ? ResolveParsedArgType<T, string> : never;
type ParsedStringArg<T extends ArgDef> = T extends {
  type: "string";
} ? ResolveParsedArgType<T, string> : never;
type ParsedBooleanArg<T extends ArgDef> = T extends {
  type: "boolean";
} ? ResolveParsedArgType<T, boolean> : never;
type ParsedEnumArg<T extends ArgDef> = T extends {
  type: "enum";
  options: infer U;
} ? U extends Array<any> ? ResolveParsedArgType<T, U[number]> : never : never;
type RawArgs = {
  _: string[];
};
type ParsedArg<T extends ArgDef> = T["type"] extends "positional" ? ParsedPositionalArg<T> : T["type"] extends "boolean" ? ParsedBooleanArg<T> : T["type"] extends "string" ? ParsedStringArg<T> : T["type"] extends "enum" ? ParsedEnumArg<T> : never;
type ParsedArgs<T extends ArgsDef = ArgsDef> = RawArgs & { [K in keyof T]: ParsedArg<T[K]> } & { [K in keyof T as T[K] extends {
  alias: string;
} ? T[K]["alias"] : never]: ParsedArg<T[K]> } & { [K in keyof T as T[K] extends {
  alias: string[];
} ? T[K]["alias"][number] : never]: ParsedArg<T[K]> } & Record<string, string | number | boolean | string[]>;
interface CommandMeta {
  name?: string;
  version?: string;
  description?: string;
  hidden?: boolean;
}
type SubCommandsDef = Record<string, Resolvable<CommandDef<any>>>;
type CommandDef<T extends ArgsDef = ArgsDef> = {
  meta?: Resolvable<CommandMeta>;
  args?: Resolvable<T>;
  subCommands?: Resolvable<SubCommandsDef>;
  setup?: (context: CommandContext<T>) => any | Promise<any>;
  cleanup?: (context: CommandContext<T>) => any | Promise<any>;
  run?: (context: CommandContext<T>) => any | Promise<any>;
};
type CommandContext<T extends ArgsDef = ArgsDef> = {
  rawArgs: string[];
  args: ParsedArgs<T>;
  cmd: CommandDef<T>;
  subCommand?: CommandDef<T>;
  data?: any;
};
type Awaitable<T> = () => T | Promise<T>;
type Resolvable<T> = T | Promise<T> | (() => T) | (() => Promise<T>);
//#endregion
//#region src/command.d.ts
declare function defineCommand<const T extends ArgsDef = ArgsDef>(def: CommandDef<T>): CommandDef<T>;
interface RunCommandOptions {
  rawArgs: string[];
  data?: any;
  showUsage?: boolean;
}
declare function runCommand<T extends ArgsDef = ArgsDef>(cmd: CommandDef<T>, opts: RunCommandOptions): Promise<{
  result: unknown;
}>;
//#endregion
//#region src/usage.d.ts
declare function showUsage<T extends ArgsDef = ArgsDef>(cmd: CommandDef<T>, parent?: CommandDef<T>): Promise<void>;
declare function renderUsage<T extends ArgsDef = ArgsDef>(cmd: CommandDef<T>, parent?: CommandDef<T>): Promise<string>;
//#endregion
//#region src/main.d.ts
interface RunMainOptions {
  rawArgs?: string[];
  showUsage?: typeof showUsage;
}
declare function runMain<T extends ArgsDef = ArgsDef>(cmd: CommandDef<T>, opts?: RunMainOptions): Promise<void>;
declare function createMain<T extends ArgsDef = ArgsDef>(cmd: CommandDef<T>): (opts?: RunMainOptions) => Promise<void>;
//#endregion
//#region src/args.d.ts
declare function parseArgs<T extends ArgsDef = ArgsDef>(rawArgs: string[], argsDef: ArgsDef): ParsedArgs<T>;
//#endregion
export { Arg, ArgDef, ArgType, ArgsDef, Awaitable, BooleanArgDef, CommandContext, CommandDef, CommandMeta, EnumArgDef, ParsedArgs, PositionalArgDef, Resolvable, type RunCommandOptions, type RunMainOptions, StringArgDef, SubCommandsDef, _ArgDef, createMain, defineCommand, parseArgs, renderUsage, runCommand, runMain, showUsage };