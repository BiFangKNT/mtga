import { fileURLToPath } from "node:url";
import fs from 'node:fs/promises';
import Module from "node:module";
import { main as asc } from "assemblyscript/asc";

const require = Module.createRequire(import.meta.url);
const wabt = await require("wabt")();

async function compile(name) {
  // https://www.assemblyscript.org/compiler.html#programmatic-usage
  const res = await asc([`${name}.asc.ts`, "-o", `${name}.wasm`], {});

  if (res.error) {
    console.log(`Compilation failed for ${name}:`, res.error);
    console.log(res.stderr.toString());
  } else {
    console.log(`Compiled: ${name}.wasm`);
    console.log(res.stdout.toString());
  }
}

async function compileWat(name) {
  const module = wabt.parseWat(`${name}.wat`, await fs.readFile(`${name}.wat`));
  module.resolveNames();
  const binaryOutput = module.toBinary({write_debug_names:true});
  const binaryBuffer = binaryOutput.buffer;
  await fs.writeFile(`${name}.wasm`, binaryBuffer);
}

process.chdir(fileURLToPath(new URL(".", import.meta.url)));

await compile("sum");
await compile("rand");
await compileWat("add-esmi");
