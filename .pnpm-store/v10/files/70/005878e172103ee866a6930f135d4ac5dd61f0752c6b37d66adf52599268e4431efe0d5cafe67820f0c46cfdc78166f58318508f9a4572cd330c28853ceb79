import { b as ViteNodeServerOptions } from "./types-EZz9rsDw.mjs";

//#region src/cli.d.ts
interface CliOptions {
  "root"?: string;
  "script"?: boolean;
  "config"?: string;
  "mode"?: string;
  "watch"?: boolean;
  "inspect"?: boolean;
  "inspectAddr"?: string;
  "options"?: ViteNodeServerOptionsCLI;
  "version"?: boolean;
  "help"?: boolean;
  "--"?: string[];
}
type Optional<T> = T | undefined;
type ComputeViteNodeServerOptionsCLI<T extends Record<string, any>> = { [K in keyof T]: T[K] extends Optional<RegExp[]> ? string | string[] : T[K] extends Optional<(string | RegExp)[]> ? string | string[] : T[K] extends Optional<(string | RegExp)[] | true> ? string | string[] | true : T[K] extends Optional<Record<string, any>> ? ComputeViteNodeServerOptionsCLI<T[K]> : T[K] };
type ViteNodeServerOptionsCLI = ComputeViteNodeServerOptionsCLI<ViteNodeServerOptions>;
//#endregion
export { CliOptions, ViteNodeServerOptionsCLI };