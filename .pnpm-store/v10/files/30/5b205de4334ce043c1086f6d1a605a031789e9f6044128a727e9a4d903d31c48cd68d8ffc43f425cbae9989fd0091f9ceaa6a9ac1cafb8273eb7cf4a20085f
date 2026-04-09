import { parse } from '@vue/compiler-sfc';

class TextWrapper {
  constructor(text) {
    this.text = text;
    this.lines = text.split("\n");
    this.lines.forEach((_, index) => {
      if (index !== this.lines.length - 1)
        this.lines[index] += "\n";
    });
    this.linesLength = this.lines.map((line) => line.length);
  }
  lines;
  linesLength;
  getLineColumn(index) {
    let line = 0;
    while (index >= this.linesLength[line]) {
      index -= this.linesLength[line];
      line++;
    }
    return {
      line: line + 1,
      column: index
    };
  }
  getIndex(line, column) {
    return this.linesLength.slice(0, line - 1).reduce((a, b) => a + b, 0) + column;
  }
}
const cache = /* @__PURE__ */ new Map();
function processor(options = {}) {
  return {
    meta: {
      name: "eslint-processor-vue-blocks"
    },
    supportsAutofix: true,
    preprocess(text, filename) {
      const { descriptor } = parse(text, {
        filename,
        pad: false
      });
      const defaultLanguage = {
        style: "css",
        template: "html",
        script: "js",
        i18n: "json",
        ...options.defaultLanguage
      };
      const wrapper = new TextWrapper(text);
      const blocks = [];
      function pushBlock(block) {
        const lang = block.lang || defaultLanguage[block.type] || block.type;
        let startOffset = wrapper.getIndex(block.loc.start.line, block.loc.start.column);
        let content = block.content;
        content = content.replace(/^(\s*)/g, (match) => {
          startOffset += match.length;
          return "";
        });
        blocks.push({
          text: content,
          filename: `${block.type}.${lang}`,
          wrapper,
          startOffset
        });
      }
      if (options.blocks?.styles)
        descriptor.styles.forEach((style) => pushBlock(style));
      if (options.blocks?.customBlocks) {
        descriptor.customBlocks.forEach((block) => {
          if (Array.isArray(options.blocks?.customBlocks) && !options.blocks?.customBlocks.includes(block.type))
            return;
          pushBlock(block);
        });
      }
      if (options.blocks?.template && descriptor.template)
        pushBlock(descriptor.template);
      if (options.blocks?.script && descriptor.script)
        pushBlock(descriptor.script);
      if (options.blocks?.scriptSetup && descriptor.scriptSetup)
        pushBlock(descriptor.scriptSetup);
      cache.set(filename, blocks);
      return blocks;
    },
    postprocess(messages, filename) {
      const blocks = cache.get(filename);
      cache.delete(filename);
      return messages.flatMap((blockMessages, index) => {
        const block = blocks[index];
        const startOffset = block.startOffset;
        const localLineColumn = new TextWrapper(block.text);
        function rewriteMessage(message) {
          const start = block.wrapper.getLineColumn(
            startOffset + localLineColumn.getIndex(message.line, message.column)
          );
          const end = block.wrapper.getLineColumn(
            startOffset + localLineColumn.getIndex(message.endLine, message.endColumn)
          );
          return {
            ...message,
            line: start.line,
            column: start.column,
            endLine: end.line,
            endColumn: end.column,
            fix: message.fix && {
              ...message.fix,
              range: message.fix.range.map((i) => i + startOffset - 1)
            }
          };
        }
        return blockMessages.map((message) => rewriteMessage(message));
      });
    }
  };
}

export { processor as default };
