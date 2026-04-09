import { NormalizedDiagnostic } from '../../logger.js';
import { DiagnosticLevel } from '../../types.js';
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

declare function mapSeverity(s: string): DiagnosticLevel;
declare function getOxlintCommand(command: string): string[];
declare function runOxlint(command: string, cwd: string): Promise<NormalizedDiagnostic[]>;

export { getOxlintCommand, mapSeverity, runOxlint };
