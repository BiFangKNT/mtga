import { t as installDependencies } from "./_chunks/libs/nypm.mjs";
import { Readable } from "node:stream";

//#region src/types.d.ts
interface GitInfo {
  provider: "github" | "gitlab" | "bitbucket" | "sourcehut";
  repo: string;
  subdir: string;
  ref: string;
}
type TarOutput = Readable | ReadableStream<Uint8Array>;
interface TemplateInfo {
  name: string;
  tar: string | ((options?: {
    auth?: string;
  }) => TarOutput | Promise<TarOutput>);
  version?: string;
  subdir?: string;
  url?: string;
  defaultDir?: string;
  headers?: Record<string, string | undefined>;
  source?: never;
  dir?: never;
  [key: string]: any;
}
type TemplateProvider = (input: string, options: {
  auth?: string;
}) => TemplateInfo | Promise<TemplateInfo> | null;
//#endregion
//#region src/giget.d.ts
type InstallOptions = Parameters<typeof installDependencies>[0];
interface DownloadTemplateOptions {
  provider?: string;
  force?: boolean;
  forceClean?: boolean;
  offline?: boolean;
  preferOffline?: boolean;
  providers?: Record<string, TemplateProvider>;
  dir?: string;
  registry?: false | string;
  cwd?: string;
  auth?: string;
  install?: boolean | InstallOptions;
  silent?: boolean;
}
type DownloadTemplateResult = Omit<TemplateInfo, "dir" | "source"> & {
  dir: string;
  source: string;
};
declare function downloadTemplate(input: string, options?: DownloadTemplateOptions): Promise<DownloadTemplateResult>;
//#endregion
//#region src/registry.d.ts
declare const registryProvider: (registryEndpoint?: string, options?: {
  auth?: string;
}) => TemplateProvider;
//#endregion
//#region src/_utils.d.ts
declare function startShell(cwd: string): void;
//#endregion
export { DownloadTemplateOptions, DownloadTemplateResult, GitInfo, TarOutput, TemplateInfo, TemplateProvider, downloadTemplate, registryProvider, startShell };