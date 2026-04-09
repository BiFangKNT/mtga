import { SharedConfig } from '../types.js';
import 'node:worker_threads';
import 'eslint';
import 'stylelint';
import 'vite';
import '../checkers/vls/initParams.js';
import 'vscode-languageserver/node';
import 'vscode-uri';

declare const RUNTIME_CLIENT_RUNTIME_PATH = "/@vite-plugin-checker-runtime";
declare const RUNTIME_CLIENT_ENTRY_PATH = "/@vite-plugin-checker-runtime-entry";
declare const wrapVirtualPrefix: (id: `/${string}`) => `virtual:${string}`;
declare const composePreambleCode: ({ baseWithOrigin, overlayConfig, }: {
    baseWithOrigin: string;
    overlayConfig: SharedConfig["overlay"];
}) => string;
declare const WS_CHECKER_ERROR_EVENT = "vite-plugin-checker:error";
declare const WS_CHECKER_RECONNECT_EVENT = "vite-plugin-checker:reconnect";
declare const runtimeSourceFilePath: string;
declare const runtimeCode: string;

export { RUNTIME_CLIENT_ENTRY_PATH, RUNTIME_CLIENT_RUNTIME_PATH, WS_CHECKER_ERROR_EVENT, WS_CHECKER_RECONNECT_EVENT, composePreambleCode, runtimeCode, runtimeSourceFilePath, wrapVirtualPrefix };
