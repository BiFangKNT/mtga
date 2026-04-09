import { NormalizedDiagnostic } from '../../logger.js';
import { CreateDiagnostic } from '../../types.js';
import { DisplayTarget } from './types.js';
import '@babel/code-frame';
import 'eslint';
import 'stylelint';
import 'typescript';
import 'vscode-languageclient/node';
import 'node:worker_threads';
import 'vite';
import '../vls/initParams.js';
import 'vscode-languageserver/node';
import 'vscode-uri';

declare const createDiagnostic: CreateDiagnostic<'oxlint'>;
declare function dispatchDiagnostics(diagnostics: NormalizedDiagnostic[], targets: Set<DisplayTarget>): void;

export { createDiagnostic, dispatchDiagnostics };
