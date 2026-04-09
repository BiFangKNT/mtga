interface FlatGitignoreOptions {
    /**
     * Name of the configuration.
     * @default 'gitignore'
     */
    name?: string;
    /**
     * Path to `.gitignore` files, or files with compatible formats like `.eslintignore`.
     * @default ['.gitignore'] // or findUpSync('.gitignore')
     */
    files?: string | string[];
    /**
     * Path to `.gitmodules` file.
     * @default ['.gitmodules'] // or findUpSync('.gitmodules')
     */
    filesGitModules?: string | string[];
    /**
     * Throw an error if gitignore file not found.
     * @default true
     */
    strict?: boolean;
    /**
     * Mark the current working directory as the root directory,
     * disable searching for `.gitignore` files in parent directories.
     *
     * This option is not effective when `files` is explicitly specified.
     * @default false
     */
    root?: boolean;
    /**
     * Current working directory.
     * Used to resolve relative paths.
     * @default process.cwd()
     */
    cwd?: string;
    /**
     * Also include recursive `.gitignore` files under `cwd`.
     *
     * This option is useful for monorepos or projects that keep
     * per-folder `.gitignore` files.
     *
     * Pass `{ skipDirs: ['name'] }` to skip directory names while
     * scanning recursively. `skipDirs` matches by directory name at
     * any depth (not by path), and is applied in addition to `.git`
     * and `node_modules`.
     * @default false
     */
    recursive?: boolean | {
        skipDirs: string[];
    };
}
interface FlatConfigItem {
    ignores: string[];
    name?: string;
}
declare function ignore(options?: FlatGitignoreOptions): FlatConfigItem;

export { ignore as default };
export type { FlatConfigItem, FlatGitignoreOptions };
