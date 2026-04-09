import fs from 'node:fs';
import path, { join, resolve, relative, dirname } from 'node:path';
import process from 'node:process';
import { convertIgnorePatternToMinimatch } from '@eslint/compat';
import 'node:fs/promises';
import { fileURLToPath } from 'node:url';

function toArray(array) {
  array = array ?? [];
  return Array.isArray(array) ? array : [array];
}

const toPath = urlOrPath => urlOrPath instanceof URL ? fileURLToPath(urlOrPath) : urlOrPath;

function findUpSync(name, {
	cwd = process.cwd(),
	type = 'file',
	stopAt,
} = {}) {
	let directory = path.resolve(toPath(cwd) ?? '');
	const {root} = path.parse(directory);
	stopAt = path.resolve(directory, toPath(stopAt) ?? root);
	const isAbsoluteName = path.isAbsolute(name);

	while (directory) {
		const filePath = isAbsoluteName ? name : path.join(directory, name);

		try {
			const stats = fs.statSync(filePath, {throwIfNoEntry: false});
			if ((type === 'file' && stats?.isFile()) || (type === 'directory' && stats?.isDirectory())) {
				return filePath;
			}
		} catch {}

		if (directory === stopAt || directory === root) {
			break;
		}

		directory = path.dirname(directory);
	}
}

const GITIGNORE = ".gitignore";
const GITMODULES = ".gitmodules";
const RE_NEWLINE = /\r?\n/u;
const RE_PARENT_PATH = /^(?:\.\.\/)+$/;
const RE_PATH_SEP = /[/\\]/;
const RE_SUBMODULE_PATH = /path\s*=\s*(.+)/u;
function ignore(options = {}) {
  const ignores = [];
  const {
    cwd = process.cwd(),
    root = false,
    recursive = false,
    files: _files = root ? GITIGNORE : findUpSync(GITIGNORE, { cwd }) || [],
    filesGitModules: _filesGitModules = root ? fs.existsSync(join(cwd, GITMODULES)) ? GITMODULES : [] : findUpSync(GITMODULES, { cwd }) || [],
    strict = true
  } = options;
  const files = new Set(toArray(_files).map((file) => resolve(cwd, file)));
  if (recursive) {
    const additionalIgnoreDirs = typeof recursive === "boolean" ? [] : recursive.skipDirs;
    for (const file of findNestedFiles(cwd, GITIGNORE, additionalIgnoreDirs))
      files.add(file);
  }
  const filesList = [...files];
  const filesGitModules = toArray(_filesGitModules).map((file) => resolve(cwd, file));
  for (const file of filesList) {
    let content = "";
    try {
      content = fs.readFileSync(file, "utf8");
    } catch (error) {
      if (strict)
        throw error;
      continue;
    }
    const relativePath = relative(cwd, dirname(file)).replaceAll("\\", "/");
    const globs = content.split(RE_NEWLINE).filter((line) => line && !line.startsWith("#")).map((line) => convertIgnorePatternToMinimatch(line)).map((glob) => relativeMinimatch(glob, relativePath, cwd)).filter((glob) => glob !== null);
    ignores.push(...globs);
  }
  for (const file of filesGitModules) {
    let content = "";
    try {
      content = fs.readFileSync(file, "utf8");
    } catch (error) {
      if (strict)
        throw error;
      continue;
    }
    const dirs = parseGitSubmodules(content);
    ignores.push(...dirs.map((dir) => `${dir}/**`));
  }
  if (strict && filesList.length === 0)
    throw new Error("No .gitignore file found");
  return {
    name: options.name || "gitignore",
    ignores
  };
}
function findNestedFiles(cwd, fileName, additionalIgnoreDirs) {
  const files = [];
  const directoriesToSkip = /* @__PURE__ */ new Set([".git", "node_modules", ...additionalIgnoreDirs]);
  const queue = [cwd];
  while (queue.length) {
    const directory = queue.shift();
    const entries = fs.readdirSync(directory, { withFileTypes: true });
    for (const entry of entries) {
      const absolutePath = join(directory, entry.name);
      if (entry.isFile() && entry.name === fileName)
        files.push(absolutePath);
      if (entry.isDirectory() && !directoriesToSkip.has(entry.name))
        queue.push(absolutePath);
    }
  }
  return files;
}
function relativeMinimatch(pattern, relativePath, cwd) {
  if (["", ".", "/"].includes(relativePath))
    return pattern;
  const negated = pattern.startsWith("!") ? "!" : "";
  let cleanPattern = negated ? pattern.slice(1) : pattern;
  if (!relativePath.endsWith("/"))
    relativePath = `${relativePath}/`;
  const isParent = relativePath.startsWith("..");
  if (!isParent)
    return `${negated}${relativePath}${cleanPattern}`;
  if (!RE_PARENT_PATH.test(relativePath))
    throw new Error("The ignore file location should be either a parent or child directory");
  if (cleanPattern.startsWith("**"))
    return pattern;
  const parents = relative(resolve(cwd, relativePath), cwd).split(RE_PATH_SEP);
  while (parents.length && cleanPattern.startsWith(`${parents[0]}/`)) {
    cleanPattern = cleanPattern.slice(parents[0].length + 1);
    parents.shift();
  }
  if (cleanPattern.startsWith("**"))
    return `${negated}${cleanPattern}`;
  if (parents.length === 0)
    return `${negated}${cleanPattern}`;
  return null;
}
function parseGitSubmodules(content) {
  return content.split(RE_NEWLINE).map((line) => RE_SUBMODULE_PATH.exec(line)).filter((match) => match !== null).map((match) => match[1].trim());
}

export { ignore as default };
