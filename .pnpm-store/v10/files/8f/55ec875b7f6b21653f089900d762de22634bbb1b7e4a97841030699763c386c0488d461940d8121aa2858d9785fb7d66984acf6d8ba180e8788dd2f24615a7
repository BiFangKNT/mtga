import * as vite from 'vite';
import { BuildInCheckerNames, CreateDiagnostic, ServeAndBuildChecker, BuildInCheckers } from './types.js';
import { Script } from './worker.js';
import 'node:worker_threads';
import 'eslint';
import 'stylelint';
import './checkers/vls/initParams.js';
import 'vscode-languageserver/node';
import 'vscode-uri';

interface CheckerMeta<T extends BuildInCheckerNames> {
    name: T;
    absFilePath: string;
    createDiagnostic: CreateDiagnostic<T>;
    build: ServeAndBuildChecker['build'];
    script?: Script<any>;
}
declare abstract class Checker<T extends BuildInCheckerNames> implements CheckerMeta<T> {
    static logger: ((...v: string[]) => unknown)[];
    static log(...args: any[]): void;
    name: T;
    absFilePath: string;
    createDiagnostic: CreateDiagnostic<T>;
    build: ServeAndBuildChecker['build'];
    script?: Script<any>;
    constructor({ name, absFilePath, createDiagnostic, build, }: CheckerMeta<T>);
    prepare(): Script<Pick<BuildInCheckers, T>>;
    initMainThread(): ((config: any, env: vite.ConfigEnv) => ServeAndBuildChecker) | undefined;
    initWorkerThread(): void;
}

export { Checker };
