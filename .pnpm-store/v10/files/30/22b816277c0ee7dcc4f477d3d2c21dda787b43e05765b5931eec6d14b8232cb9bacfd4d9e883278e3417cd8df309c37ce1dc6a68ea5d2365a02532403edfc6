import { Plugin } from 'vite';
import { UserPluginConfig } from './types.js';
import 'node:worker_threads';
import 'eslint';
import 'stylelint';
import './checkers/vls/initParams.js';
import 'vscode-languageserver/node';
import 'vscode-uri';

declare function checker(userConfig: UserPluginConfig): Plugin;

export { checker, checker as default };
