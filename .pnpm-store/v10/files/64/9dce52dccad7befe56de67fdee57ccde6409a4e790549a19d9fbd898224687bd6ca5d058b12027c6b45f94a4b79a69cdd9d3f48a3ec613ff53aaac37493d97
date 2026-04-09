import { addVitePlugin } from '@nuxt/kit';
import { resolve, join } from 'pathe';
import { readdir, lstat } from 'node:fs/promises';
import { createVitePluginInspect } from './vite-inspect.mjs';
import '@nuxt/devtools-kit';

async function getFolderSize(dir) {
  const dirents = await readdir(dir, {
    withFileTypes: true
  });
  if (dirents.length === 0)
    return 0;
  const files = [];
  const directorys = [];
  for (const dirent of dirents) {
    if (dirent.isFile()) {
      files.push(dirent);
      continue;
    }
    if (dirent.isDirectory())
      directorys.push(dirent);
  }
  const sizes = await Promise.all(
    [
      files.map(async (file) => {
        const path = resolve(dir, file.name);
        const { size } = await lstat(path);
        return size;
      }),
      directorys.map((directory) => {
        const path = resolve(dir, directory.name);
        return getFolderSize(path);
      })
    ].flat()
  );
  return sizes.reduce((total, size) => total += size, 0);
}

async function setup(nuxt, options) {
  if (options.viteInspect !== false) {
    addVitePlugin(
      await createVitePluginInspect({
        build: true,
        outputDir: join(nuxt.options.analyzeDir, ".vite-inspect")
      })
    );
  }
  nuxt.hook("build:analyze:done", async (meta) => {
    const _meta = meta;
    _meta.size = _meta.size || {};
    const dirs = [join(meta.buildDir, "dist/client"), meta.outDir];
    const [clientBundleSize, nitroBundleSize] = await Promise.all(dirs.map(getFolderSize));
    _meta.size.clientBundle = clientBundleSize;
    _meta.size.nitroBundle = nitroBundleSize;
  });
}

export { setup };
