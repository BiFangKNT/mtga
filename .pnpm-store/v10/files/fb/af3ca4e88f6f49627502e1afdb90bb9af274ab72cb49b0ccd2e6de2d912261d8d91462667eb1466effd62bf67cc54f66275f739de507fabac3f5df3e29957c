import { FileDiagnosticManager } from '../../FileDiagnosticManager.js';
import { ResolvedOptions } from './options.js';
import { DisplayTarget } from './types.js';
import '../../logger.js';
import '@babel/code-frame';
import '../../types.js';
import 'node:worker_threads';
import 'eslint';
import 'stylelint';
import 'vite';
import '../vls/initParams.js';
import 'vscode-languageserver/node';
import 'vscode-uri';
import 'typescript';
import 'vscode-languageclient/node';

declare function setupDevServer(root: string, options: ResolvedOptions, manager: FileDiagnosticManager, displayTargets: Set<DisplayTarget>): Promise<void>;

export { setupDevServer };
