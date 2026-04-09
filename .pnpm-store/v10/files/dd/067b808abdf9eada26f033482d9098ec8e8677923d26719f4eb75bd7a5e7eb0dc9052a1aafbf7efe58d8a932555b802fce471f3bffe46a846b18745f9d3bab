import process from 'node:process';
import { walk } from 'estree-walker';
import { resolveModulePath } from 'exsolve';
import MagicString from 'magic-string';
import { relative, dirname, isAbsolute } from 'pathe';
import { SourceMapConsumer } from 'source-map-js';

const functions = [
  "h",
  "_createElementVNode",
  "_createElementBlock",
  "_createBlock",
  "_createVNode",
  "_createStaticVNode"
];
const testRe = new RegExp(`\\b(?:${functions.join("|")})\\(`);
function VueTracer(options) {
  let {
    enabled = "dev",
    resolveRecordEntryPath = true,
    viteDevtools = false
  } = options || {};
  if (enabled === false)
    return;
  const pathRecordDist = resolveModulePath("vite-plugin-vue-tracer/client/record", { from: import.meta.url });
  const getRecordPath = (id) => {
    if (!resolveRecordEntryPath)
      return "vite-plugin-vue-tracer/client/record";
    let related = relative(dirname(id), pathRecordDist);
    if (!related.startsWith("./") && !isAbsolute(related))
      related = `./${related}`;
    return related;
  };
  return {
    name: "vite-plugin-vue-tracer",
    enforce: "post",
    configResolved(config) {
      if (enabled === "dev")
        enabled = config.command === "serve";
      else if (enabled === "prod")
        enabled = config.command === "build";
    },
    transform(code, id) {
      if (!enabled)
        return;
      if (this.environment.name !== "client")
        return;
      if (!code.includes("_sfc_render("))
        return;
      if (!testRe.test(code))
        return;
      if (code.includes("_tracer("))
        return;
      function offsetToPos(index) {
        const lines = code.slice(0, index).split("\n");
        return {
          line: lines.length,
          column: lines.at(-1).length
        };
      }
      const map = this.getCombinedSourcemap();
      const consumer = new SourceMapConsumer(map);
      const s = new MagicString(code);
      const ast = this.parse(code);
      let hit = false;
      walk(ast, {
        enter(node) {
          if (node.type !== "CallExpression" || node.callee.type !== "Identifier")
            return;
          if (!functions.includes(node.callee.name))
            return;
          const { start, end } = node;
          const pos = offsetToPos(start);
          const original = consumer.originalPositionFor(pos);
          if (original.source === null)
            return;
          hit = true;
          s.appendLeft(start, `_tracer(${original.line},${original.column},`);
          s.appendRight(end, `)`);
        }
      });
      if (!hit)
        return;
      const related = relative(process.cwd(), id);
      s.prepend(`import { recordPosition as _tracerRecordPosition } from ${JSON.stringify(getRecordPath(id))}
`);
      s.append(`
function _tracer(line, column, vnode) { return _tracerRecordPosition(${JSON.stringify(related)}, line, column, vnode) }
`);
      return {
        code: s.toString(),
        map: s.generateMap({ hires: true })
      };
    },
    // Vite DevTools integration
    ...viteDevtools ? {
      devtools: {
        setup(ctx) {
          ctx.docks.register({
            id: "vue-tracer",
            title: "Vue Tracer",
            icon: "ph:crosshair-simple-duotone",
            type: "action",
            action: {
              importFrom: "vite-plugin-vue-tracer/client/vite-devtools",
              importName: "default"
            }
          });
        }
      }
    } : {}
  };
}

export { VueTracer, VueTracer as default };
