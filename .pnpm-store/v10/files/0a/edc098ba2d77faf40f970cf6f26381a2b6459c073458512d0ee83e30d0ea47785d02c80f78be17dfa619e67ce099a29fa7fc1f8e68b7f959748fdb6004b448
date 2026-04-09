import { EmptyTask } from './task';
import { OptionFlags, Options, StringTask } from '../types';
import { SimpleGit } from '../../../typings';
export type CloneOptions = Options & OptionFlags<'--bare' | '--dissociate' | '--mirror' | '--no-checkout' | '--no-remote-submodules' | '--no-shallow-submodules' | '--no-single-branch' | '--no-tags' | '--remote-submodules' | '--single-branch' | '--shallow-submodules' | '--verbose'> & OptionFlags<'--depth' | '-j' | '--jobs', number> & OptionFlags<'--branch' | '--origin' | '--recurse-submodules' | '--separate-git-dir' | '--shallow-exclude' | '--shallow-since' | '--template', string>;
type CloneTaskBuilder = (repo: string | undefined, directory: string | undefined, customArgs: string[]) => StringTask<string> | EmptyTask;
export declare const cloneTask: CloneTaskBuilder;
export declare const cloneMirrorTask: CloneTaskBuilder;
export default function (): Pick<SimpleGit, 'clone' | 'mirror'>;
export {};
