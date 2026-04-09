//#region ../shared/types.d.ts
interface PackageManifest {
  name: string;
  distTags: Record<string, string> & {
    latest: string;
  };
  versionsMeta: Record<string, PackageVersionMeta>;
  timeCreated: string;
  timeModified: string;
  lastSynced: number;
}
type Engines = Partial<Record<string, string>>;
interface PackageVersionMeta {
  time?: string;
  engines?: Engines;
  deprecated?: string;
  provenance?: 'trustedPublisher' | boolean;
  integrity?: string;
}
interface PackageVersionsInfo extends Pick<PackageManifest, 'name' | 'distTags' | 'lastSynced'> {
  versions: string[];
  specifier: string;
  time: {
    created: string;
    modified: string;
  } & Record<string, string>;
}
interface PackageVersionsInfoWithMetadata extends PackageManifest {
  specifier: string;
}
interface PackageError {
  status: number;
  name: string;
  error: string;
}
type MaybeError<T> = T | PackageError;
interface PackageManifestError extends PackageError {
  lastSynced: number;
}
interface ResolvedPackageVersion {
  name: string;
  version: string | null;
  specifier: string;
  publishedAt: string | null;
  lastSynced: number;
}
interface ResolvedPackageVersionWithMetadata extends ResolvedPackageVersion, PackageVersionMeta {}
//#endregion
//#region src/types.d.ts
interface RetryOptions {
  /**
   * The number of times to retry the operation.
   *
   * @default 5
   */
  retries?: number;
  /**
   * The exponential factor to use.
   *
   * @default 2
   */
  factor?: number;
  /**
   * The number of milliseconds before starting the first retry.
   *
   * Set this to `0` to retry immediately with no delay.
   *
   * @default 1000
   */
  minTimeout?: number;
  /**
   * The maximum number of milliseconds between two retries.
   *
   * @default Infinity
   */
  maxTimeout?: number;
  /**
   * Randomizes the timeouts by multiplying with a factor between 1 and 2.
   *
   * @default false
   */
  randomize?: boolean;
}
interface FetchOptions<Throw extends boolean = true> {
  /**
   * API endpoint for fetching package versions
   *
   * @default 'https://npm.antfu.dev/'
   */
  apiEndpoint?: string;
  /**
   * Fetch function
   *
   * @default [globalThis.fetch](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API)
   */
  fetch?: typeof fetch;
  /**
   * Should throw error or return error object
   *
   * @default true
   */
  throw?: Throw;
}
interface GetVersionsOptions<Metadata extends boolean = false, Throw extends boolean = true> extends FetchOptions<Throw> {
  /**
   * By pass cache and get the latest data
   *
   * @default false
   */
  force?: boolean;
  /**
   * Include all versions that are newer than the specified version
   *
   * @default false
   */
  loose?: boolean;
  /**
   * Includes metadata, this will change the return type
   *
   * @default false
   */
  metadata?: Metadata;
  /**
   * Only return versions published after this ISO date-time
   *
   * @default undefined
   */
  after?: string;
  /**
   * Retry options for the built-in retry mechanism
   *
   * Can be:
   * - `RetryOptions` object for fine-grained control
   * - `number` for simple retry count (uses defaults for other options)
   * - `false` to disable retries
   */
  retry?: RetryOptions | number | false;
}
interface GetLatestVersionOptions<Metadata extends boolean = false, Throw extends boolean = true> extends FetchOptions<Throw> {
  /**
   * By pass cache and get the latest data
   *
   * @default false
   */
  force?: boolean;
  /**
   * Includes metadata
   *
   * @default false
   */
  metadata?: Metadata;
  /**
   * Retry options for the built-in retry mechanism
   *
   * Can be:
   * - `RetryOptions` object for fine-grained control
   * - `number` for simple retry count (uses defaults for other options)
   * - `false` to disable retries
   */
  retry?: RetryOptions | number | false;
}
type InferGetVersionsResult<Metadata, Throw> = Metadata extends true ? Throw extends true ? PackageVersionsInfoWithMetadata : MaybeError<PackageVersionsInfoWithMetadata> : Throw extends true ? PackageVersionsInfo : MaybeError<PackageVersionsInfo>;
type InferGetLatestVersionResult<Metadata, Throw> = Metadata extends true ? Throw extends true ? ResolvedPackageVersionWithMetadata : MaybeError<ResolvedPackageVersionWithMetadata> : Throw extends true ? ResolvedPackageVersion : MaybeError<ResolvedPackageVersion>;
//#endregion
//#region src/api.d.ts
declare const defaultOptions: {
  /**
   * API endpoint for fetching package versions
   *
   * @default 'https://npm.antfu.dev/'
   */
  apiEndpoint: string;
};
declare function getLatestVersionBatch<Metadata extends boolean = false, Throw extends boolean = true>(packages: string[], options?: GetLatestVersionOptions<Metadata, Throw>): Promise<InferGetLatestVersionResult<Metadata, Throw>[]>;
declare function getLatestVersion<Metadata extends boolean = false, Throw extends boolean = true>(name: string, options?: GetLatestVersionOptions<Metadata, Throw>): Promise<InferGetLatestVersionResult<Metadata, Throw>>;
declare function getVersionsBatch<Metadata extends boolean = false, Throw extends boolean = true>(packages: string[], options?: GetVersionsOptions<Metadata, Throw>): Promise<InferGetVersionsResult<Metadata, Throw>[]>;
declare function getVersions<Metadata extends boolean = false, Throw extends boolean = true>(name: string, options?: GetVersionsOptions<Metadata, Throw>): Promise<InferGetVersionsResult<Metadata, Throw>>;
//#endregion
//#region src/helpers.d.ts
declare const NPM_REGISTRY = "https://registry.npmjs.org/";
/**
 * Lightweight replacement of `npm-registry-fetch` function `pickRegistry`'
 *
 * @param scope - scope of package, get from 'npm-package-arg'
 * @param npmConfigs - npm configs, read from `.npmrc` file
 * @param defaultRegistry - default registry, default to 'https://registry.npmjs.org/'
 */
declare function pickRegistry(scope: string | null | undefined, npmConfigs: Record<string, unknown>, defaultRegistry?: string): string;
//#endregion
export { Engines, FetchOptions, GetLatestVersionOptions, GetVersionsOptions, InferGetLatestVersionResult, InferGetVersionsResult, MaybeError, NPM_REGISTRY, PackageError, PackageManifest, PackageManifestError, PackageVersionMeta, PackageVersionsInfo, PackageVersionsInfoWithMetadata, ResolvedPackageVersion, ResolvedPackageVersionWithMetadata, RetryOptions, defaultOptions, getLatestVersion, getLatestVersionBatch, getVersions, getVersionsBatch, pickRegistry };