import * as magicast0 from "magicast";

//#region src/update.d.ts
/**
 * @experimental Update a config file or create a new one.
 */
declare function updateConfig(opts: UpdateConfigOptions): Promise<UpdateConfigResult>;
interface UpdateConfigResult {
  configFile?: string;
  created?: boolean;
}
type MaybePromise<T> = T | Promise<T>;
type MagicAstOptions = Exclude<Parameters<(typeof magicast0)["parseModule"]>[1], undefined>;
interface UpdateConfigOptions {
  /**
   * Current working directory
   */
  cwd: string;
  /**
   * Config file name
   */
  configFile: string;
  /**
   * Extension used for new config file.
   */
  createExtension?: string;
  /**
   * Magicast options
   */
  magicast?: MagicAstOptions;
  /**
   * Update function.
   */
  onUpdate?: (config: any) => MaybePromise<void>;
  /**
   * Handle default config creation.
   *
   * Tip: you can use this option as a hook to prompt users about config creation.
   *
   * Context object:
   *  - path: determined full path to the config file
   *
   * Returns types:
   *  - string: custom config template
   *  - true: write the template
   *  - false: abort the operation
   */
  onCreate?: (ctx: {
    configFile: string;
  }) => MaybePromise<string | boolean>;
}
//#endregion
export { UpdateConfigOptions, UpdateConfigResult, updateConfig };