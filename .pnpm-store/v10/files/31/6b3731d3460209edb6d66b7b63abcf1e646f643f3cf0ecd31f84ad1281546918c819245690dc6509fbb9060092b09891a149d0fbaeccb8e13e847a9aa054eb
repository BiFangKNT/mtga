export { b as builtinPresets, c as createUnimport, e as dedupeDtsExports, n as normalizeScanDirs, r as resolveBuiltinPresets, a as resolvePreset, d as scanDirExports, f as scanExports, s as scanFilesFromDir, v as version } from './shared/unimport.Bpe8Rcsr.mjs';
export { R as RE_EXCLUDE, b as RE_IMPORT_AS, d as RE_MATCH, c as RE_SEPARATOR, r as addImportToCode, j as dedupeImports, g as defineUnimportPreset, e as excludeRE, q as getMagicString, p as getString, i as importAsRE, m as matchRE, u as normalizeImports, w as resolveIdAbsolute, f as separatorRE, h as stringifyImports, s as stripCommentsAndStrings, k as stripFileExtension, t as toExports, x as toImports, n as toTypeDeclarationFile, l as toTypeDeclarationItems, o as toTypeReExports, a as vueTemplateAddon } from './shared/unimport.BCoAHNhG.mjs';
import 'mlly';
import 'node:fs';
import 'node:fs/promises';
import 'node:process';
import 'node:url';
import 'pathe';
import 'picomatch';
import 'scule';
import 'tinyglobby';
import 'node:os';
import 'pkg-types';
import 'local-pkg';
import 'node:path';
import 'magic-string';
import 'strip-literal';

async function installGlobalAutoImports(imports, options = {}) {
  const {
    globalObject = globalThis,
    overrides = false
  } = options;
  imports = Array.isArray(imports) ? imports : await imports.getImports();
  await Promise.all(
    imports.map(async (i) => {
      if (i.disabled || i.type)
        return;
      const as = i.as || i.name;
      if (overrides || !(as in globalObject)) {
        const module = await import(i.from);
        globalObject[as] = module[i.name];
      }
    })
  );
  return globalObject;
}

export { installGlobalAutoImports };
