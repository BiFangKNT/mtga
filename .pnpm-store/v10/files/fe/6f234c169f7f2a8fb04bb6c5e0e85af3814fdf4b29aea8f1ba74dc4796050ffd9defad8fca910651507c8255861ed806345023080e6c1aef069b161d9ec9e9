import { ConfigEnv } from 'vite';
import { SharedConfig, ServeAndBuildChecker, BuildInCheckers, BuildCheckBin, ServeChecker } from './types.js';
import 'node:worker_threads';
import 'eslint';
import 'stylelint';
import './checkers/vls/initParams.js';
import 'vscode-languageserver/node';
import 'vscode-uri';

interface WorkerScriptOptions {
    absFilename: string;
    buildBin: BuildCheckBin;
    serverChecker: ServeChecker;
}
interface Script<T> {
    mainScript: () => (config: T & SharedConfig, env: ConfigEnv) => ServeAndBuildChecker;
    workerScript: () => void;
}
declare function createScript<T extends Partial<BuildInCheckers>>({ absFilename, buildBin, serverChecker, }: WorkerScriptOptions): Script<T>;

export { type Script, createScript };
