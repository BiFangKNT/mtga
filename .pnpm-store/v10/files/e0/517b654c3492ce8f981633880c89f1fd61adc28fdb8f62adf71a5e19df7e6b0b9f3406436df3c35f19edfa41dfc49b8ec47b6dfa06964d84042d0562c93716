import { createUnplugin } from 'unplugin';
import { createTransformer } from './transform.mjs';
import 'acorn';
import 'magic-string';
import 'estree-walker';

const unctxPlugin = createUnplugin(
  (options = {}) => {
    const transformer = createTransformer(options);
    return {
      name: "unctx:transform",
      enforce: "post",
      transformInclude: options.transformInclude,
      transform: {
        filter: options.transformFilter ?? transformer.filter,
        handler(code, id) {
          const result = transformer.transform(code);
          if (result) {
            return {
              code: result.code,
              map: result.magicString.generateMap({
                source: id,
                includeContent: true
              })
            };
          }
        }
      }
    };
  }
);

export { unctxPlugin };
