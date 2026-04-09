import { NormalizedDiagnostic } from './logger.js';
import '@babel/code-frame';
import './types.js';
import 'node:worker_threads';
import 'eslint';
import 'stylelint';
import 'vite';
import './checkers/vls/initParams.js';
import 'vscode-languageserver/node';
import 'vscode-uri';
import 'typescript';
import 'vscode-languageclient/node';

declare class FileDiagnosticManager {
    diagnostics: NormalizedDiagnostic[];
    /**
     * Initialize and reset the diagnostics array
     */
    initWith(diagnostics: NormalizedDiagnostic[]): void;
    getDiagnostics(fileName?: string): NormalizedDiagnostic[];
    updateByFileId(fileId: string, next: NormalizedDiagnostic[] | null): void;
}

export { FileDiagnosticManager };
