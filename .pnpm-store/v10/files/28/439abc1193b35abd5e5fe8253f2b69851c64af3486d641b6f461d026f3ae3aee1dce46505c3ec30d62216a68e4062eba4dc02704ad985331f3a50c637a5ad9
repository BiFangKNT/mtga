import { ServeAndBuildChecker } from '../../types.js';
import * as vite from 'vite';
import { Checker } from '../../Checker.js';
import 'node:worker_threads';
import 'eslint';
import 'stylelint';
import '../vls/initParams.js';
import 'vscode-languageserver/node';
import 'vscode-uri';
import '../../worker.js';

declare class OxlintChecker extends Checker<'oxlint'> {
    constructor();
}
declare const createServeAndBuild: ((config: any, env: vite.ConfigEnv) => ServeAndBuildChecker) | undefined;

export { OxlintChecker, createServeAndBuild };
