import { Worker } from 'node:worker_threads';
import { ESLint } from 'eslint';
import * as Stylelint from 'stylelint';
import { ConfigEnv, ErrorPayload } from 'vite';
import { VlsOptions } from './checkers/vls/initParams.js';
import 'vscode-languageserver/node';
import 'vscode-uri';

interface TsConfigOptions {
    /**
     * path to tsconfig.json file
     */
    tsconfigPath: string;
    /**
     * path to typescript package
     */
    typescriptPath: string;
    /**
     * root path of cwd
     */
    root: string;
    /**
     * root path of cwd
     */
    buildMode: boolean;
}
/**
 * TypeScript checker configuration
 * @default true
 */
type TscConfig = 
/**
 * - set to `true` to enable type checking with default configuration
 * - set to `false` to disable type checking, you can also remove `config.typescript` directly
 */
boolean | Partial<TsConfigOptions>;
/** vue-tsc checker configuration */
type VueTscConfig = 
/**
 * - set to `true` to enable type checking with default configuration
 * - set to `false` to disable type checking, you can also remove `config.vueTsc` directly
 */
boolean | Partial<TsConfigOptions>;
/** vls checker configuration */
type VlsConfig = boolean | DeepPartial<VlsOptions>;
/** ESLint checker configuration */
type EslintConfig = false | {
    /**
     * Configure path to watch files
     */
    watchPath?: string | string[];
    /**
     * lintCommand will be executed at build mode, and will also be used as
     * default config for dev mode when options.eslint.dev.eslint is nullable.
     */
    lintCommand: string;
    /**
     * @default false
     */
    useFlatConfig?: boolean;
    dev?: Partial<{
        /** You can override the options of translated from lintCommand. */
        overrideConfig: ESLint.Options;
        /** which level of the diagnostic will be emitted from plugin */
        logLevel: ('error' | 'warning')[];
    }>;
};
/** Stylelint checker configuration */
type StylelintConfig = false | {
    /**
     * Configure path to watch files
     */
    watchPath?: string | string[];
    /**
     * lintCommand will be executed at build mode, and will also be used as
     * default config for dev mode when options.stylelint.dev.stylelint is nullable.
     */
    lintCommand: string;
    dev?: Partial<{
        /** You can override the options of translated from lintCommand. */
        overrideConfig: Stylelint.LinterOptions;
        /** which level of the diagnostic will be emitted from plugin */
        logLevel: ('error' | 'warning')[];
    }>;
};
type BiomeCommand = 'lint' | 'check' | 'format' | 'ci';
/** Biome checker configuration */
type BiomeConfig = boolean | {
    /**
     * Command will be used in dev and build mode, will be override
     * if `dev.command` or `build.command` is set their mode.
     */
    command?: BiomeCommand;
    /**
     * Flags of the command, will be override if `dev.flags`
     * or `build.command` is set their mode.
     * */
    flags?: string;
    /**
     * Configure path to watch files
     */
    watchPath?: string | string[];
    dev?: Partial<{
        /** Command will be used in dev mode */
        command: BiomeCommand;
        /** Flags of the command */
        flags?: string;
        /** Which level of the diagnostic will be emitted from plugin */
        logLevel: ('error' | 'warning' | 'info')[];
    }>;
    build?: Partial<{
        /** Command will be used in build mode */
        command: BiomeCommand;
        /** Flags of the command */
        flags?: string;
    }>;
};
type OxlintConfig = boolean | {
    /**
     * `lintCommand` will be executed at build mode.
     */
    lintCommand: string;
    /**
     * Configure path to watch files
     */
    watchPath?: string | string[];
    dev?: Partial<{
        /** Specifies which level of the diagnostic will be emitted from the plugin */
        logLevel: ('error' | 'warning')[];
    }>;
};
declare enum DiagnosticLevel {
    Warning = 0,
    Error = 1,
    Suggestion = 2,
    Message = 3
}
type ErrorPayloadErr = ErrorPayload['err'];
interface DiagnosticToRuntime extends ErrorPayloadErr {
    checkerId: string;
    level?: DiagnosticLevel;
}
interface ClientDiagnosticPayload {
    event: 'vite-plugin-checker:error';
    data: {
        checkerId: string;
        diagnostics: DiagnosticToRuntime[];
    };
}
interface ClientReconnectPayload {
    event: 'vite-plugin-checker:reconnect';
    data: ClientDiagnosticPayload[];
}
type ClientPayload = ClientDiagnosticPayload | ClientReconnectPayload;
/** checkers shared configuration */
interface SharedConfig {
    /**
     * Show overlay on UI view when there are errors or warnings in dev mode.
     * - Set `true` to show overlay
     * - Set `false` to disable overlay
     * - Set with a object to customize overlay
     *
     * @defaultValue `true`
     */
    overlay: boolean | {
        /**
         * Set this true if you want the overlay to default to being open if
         * errors/warnings are found
         * @defaultValue `true`
         */
        initialIsOpen?: boolean | 'error';
        /**
         * The position of the vite-plugin-checker badge to open and close
         * the diagnostics panel
         * @default `bl`
         */
        position?: 'tl' | 'tr' | 'bl' | 'br';
        /**
         * Use this to add extra style string to the badge button, the string format is
         * [HTML element's style property](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style)
         * For example, if you want to hide the badge,
         * you can pass `display: none;` to the badgeStyle property
         * @default no default value
         */
        badgeStyle?: string;
        /**
         * Use this to add extra style string to the diagnostic panel, the string format is
         * [HTML element's style property](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/style)
         * For example, if you want to change the opacity of the panel,
         * you can pass `opacity: 0.8;` to the panelStyle property
         * @default no default value
         */
        panelStyle?: string;
    };
    /**
     * stdout in terminal which starts the Vite server in dev mode.
     * - Set `true` to enable
     * - Set `false` to disable
     *
     * @defaultValue `true`
     */
    terminal: boolean;
    /**
     * Enable checking in build mode
     * @defaultValue `true`
     */
    enableBuild: boolean;
    /**
     * Configure root directory of checkers
     * @defaultValue no default value
     */
    root?: string;
}
interface BuildInCheckers {
    typescript: TscConfig;
    vueTsc: VueTscConfig;
    vls: VlsConfig;
    eslint: EslintConfig;
    stylelint: StylelintConfig;
    biome: BiomeConfig;
    oxlint: OxlintConfig;
}
type BuildInCheckerNames = keyof BuildInCheckers;
type PluginConfig = SharedConfig & BuildInCheckers;
/** Userland plugin configuration */
type UserPluginConfig = Partial<PluginConfig>;
declare enum ACTION_TYPES {
    config = "config",
    configureServer = "configureServer",
    overlayError = "overlayError",
    console = "console",
    unref = "unref"
}
interface AbstractAction {
    type: string;
    payload: unknown;
}
interface OverlayErrorAction extends AbstractAction {
    type: ACTION_TYPES.overlayError;
    /**
     * send `ClientPayload` to raise error overlay
     * send `null` to clear overlay for current checker
     */
    payload: ClientPayload;
}
interface ConfigAction extends AbstractAction {
    type: ACTION_TYPES.config;
    payload: ConfigActionPayload;
}
interface ConfigureServerAction extends AbstractAction {
    type: ACTION_TYPES.configureServer;
    payload: {
        root: string;
    };
}
interface ConsoleAction extends AbstractAction {
    type: ACTION_TYPES.console;
    level: 'info' | 'warn' | 'error';
    payload: string;
}
interface UnrefAction extends AbstractAction {
    type: ACTION_TYPES.unref;
}
interface ConfigActionPayload {
    enableOverlay: boolean;
    enableTerminal: boolean;
    env: ConfigEnv;
}
type Action = ConfigAction | ConfigureServerAction | ConsoleAction | OverlayErrorAction | UnrefAction;
type BuildCheckBin = BuildCheckBinStr | BuildCheckBinFn;
type BuildCheckBinStr = [string, ReadonlyArray<string>];
type BuildCheckBinFn = (config: UserPluginConfig) => [string, ReadonlyArray<string>];
interface ConfigureServeChecker {
    worker: Worker;
    config: (config: ConfigAction['payload']) => void;
    configureServer: (serverConfig: ConfigureServerAction['payload']) => void;
}
interface ServeAndBuildChecker {
    serve: ConfigureServeChecker;
    build: {
        buildBin: BuildCheckBin;
        buildFile?: string;
    };
}
/**
 * create serve & build checker
 */
interface ServeChecker<T extends BuildInCheckerNames = any> {
    createDiagnostic: CreateDiagnostic<T>;
}
interface CheckerDiagnostic {
    config: (options: ConfigActionPayload) => unknown;
    configureServer: (options: {
        root: string;
    }) => unknown;
}
type CreateDiagnostic<T extends BuildInCheckerNames = any> = (config: Pick<BuildInCheckers, T> & SharedConfig) => CheckerDiagnostic;
type DeepPartial<T> = {
    [P in keyof T]?: DeepPartial<T[P]>;
};

export { ACTION_TYPES, type Action, type BiomeConfig, type BuildCheckBin, type BuildCheckBinFn, type BuildCheckBinStr, type BuildInCheckerNames, type BuildInCheckers, type CheckerDiagnostic, type ClientDiagnosticPayload, type ClientPayload, type ClientReconnectPayload, type ConfigAction, type ConfigureServeChecker, type ConfigureServerAction, type ConsoleAction, type CreateDiagnostic, type DeepPartial, DiagnosticLevel, type DiagnosticToRuntime, type EslintConfig, type OverlayErrorAction, type OxlintConfig, type PluginConfig, type ServeAndBuildChecker, type ServeChecker, type SharedConfig, type StylelintConfig, type TscConfig, type UnrefAction, type UserPluginConfig, type VlsConfig, type VueTscConfig };
