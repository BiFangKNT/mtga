import { Checker } from '../../Checker.js';
import { CreateDiagnostic } from '../../types.js';
import 'vite';
import '../../worker.js';
import 'node:worker_threads';
import 'eslint';
import 'stylelint';
import './initParams.js';
import 'vscode-languageserver/node';
import 'vscode-uri';

declare let createServeAndBuild: any;
declare const createDiagnostic: CreateDiagnostic<'vls'>;
declare class VlsChecker extends Checker<'vls'> {
    constructor();
    init(): void;
}

export { VlsChecker, createDiagnostic, createServeAndBuild };
