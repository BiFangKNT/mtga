export { v as vueTemplateAddon } from './shared/unimport.DMFRbr22.mjs';
import { U as UnimportOptions, a as Unimport, I as Import, b as InstallGlobalOptions, S as ScanDir, c as ScanDirExportsOptions, B as BuiltinPresetName, P as Preset, d as InlinePreset, T as ToExportsOptions, e as TypeDeclarationOptions, M as MagicStringResult } from './shared/unimport.DCeIjgcw.mjs';
export { s as Addon, o as AddonVueDirectivesOptions, A as AddonsOptions, D as DetectImportResult, i as ImportCommon, t as ImportInjectionResult, h as ImportName, q as InjectImportsOptions, m as InjectionUsageRecord, g as ModuleId, k as PackagePreset, p as PathFromResolver, j as PresetImport, r as Thenable, l as UnimportContext, n as UnimportMeta, f as builtinPresets } from './shared/unimport.DCeIjgcw.mjs';
import { StripLiteralOptions } from 'strip-literal';
import MagicString from 'magic-string';
import 'mlly';

declare let version: string;

declare function createUnimport(opts: Partial<UnimportOptions>): Unimport;

declare function installGlobalAutoImports(imports: Import[] | Unimport, options?: InstallGlobalOptions): Promise<any>;

declare function normalizeScanDirs(dirs: (string | ScanDir)[], options?: ScanDirExportsOptions): Required<ScanDir>[];
declare function scanFilesFromDir(dir: ScanDir | ScanDir[], options?: ScanDirExportsOptions): Promise<string[]>;
declare function scanDirExports(dirs: (string | ScanDir)[], options?: ScanDirExportsOptions): Promise<Import[]>;
declare function dedupeDtsExports(exports: Import[]): Import[];
declare function scanExports(filepath: string, includeTypes: boolean, seen?: Set<string>): Promise<Import[]>;

declare function resolvePreset(preset: Preset): Promise<Import[]>;
declare function resolveBuiltinPresets(presets: (BuiltinPresetName | Preset)[]): Promise<Import[]>;

declare const excludeRE: RegExp[];
declare const importAsRE: RegExp;
declare const separatorRE: RegExp;
/**
 *                                                                             |       |
 *                    destructing   case&ternary    non-call     inheritance   |  id   |
 *                         ↓             ↓             ↓             ↓         |       |
 */
declare const matchRE: RegExp;
declare function stripCommentsAndStrings(code: string, options?: StripLiteralOptions): string;

declare function defineUnimportPreset(preset: InlinePreset): InlinePreset;
declare function stringifyImports(imports: Import[], isCJS?: boolean): string;
declare function dedupeImports(imports: Import[], warn: (msg: string) => void): Import[];
declare function toExports(imports: Import[], fileDir?: string, includeType?: boolean, options?: ToExportsOptions): string;
declare function stripFileExtension(path: string): string;
declare function toTypeDeclarationItems(imports: Import[], options?: TypeDeclarationOptions): string[];
declare function toTypeDeclarationFile(imports: Import[], options?: TypeDeclarationOptions): string;
declare function toTypeReExports(imports: Import[], options?: TypeDeclarationOptions): string;
declare function getString(code: string | MagicString): string;
declare function getMagicString(code: string | MagicString): MagicString;
declare function addImportToCode(code: string | MagicString, imports: Import[], isCJS?: boolean, mergeExisting?: boolean, injectAtLast?: boolean, firstOccurrence?: number, onResolved?: (imports: Import[]) => void | Import[], onStringified?: (str: string, imports: Import[]) => void | string): MagicStringResult;
declare function normalizeImports(imports: Import[]): Import[];
declare function resolveIdAbsolute(id: string, parentId?: string): string;
/**
 * @deprecated renamed to `stringifyImports`
 */
declare const toImports: typeof stringifyImports;

export { BuiltinPresetName, Import, InlinePreset, InstallGlobalOptions, MagicStringResult, Preset, ScanDir, ScanDirExportsOptions, ToExportsOptions, TypeDeclarationOptions, Unimport, UnimportOptions, addImportToCode, createUnimport, dedupeDtsExports, dedupeImports, defineUnimportPreset, excludeRE, getMagicString, getString, importAsRE, installGlobalAutoImports, matchRE, normalizeImports, normalizeScanDirs, resolveBuiltinPresets, resolveIdAbsolute, resolvePreset, scanDirExports, scanExports, scanFilesFromDir, separatorRE, stringifyImports, stripCommentsAndStrings, stripFileExtension, toExports, toImports, toTypeDeclarationFile, toTypeDeclarationItems, toTypeReExports, version };
