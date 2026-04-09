export function defineKeyedFunctionFactory(factory) {
  const placeholder = function() {
    if (import.meta.dev) {
      throw new Error(
        `[nuxt:compiler] \`${factory.name}\` is a compiler macro that is only usable inside the directories scanned by the Nuxt compiler as an exported function and imported statically. Learn more: \`https://nuxt.com/docs/guide/going-further/compiler\``
      );
    }
    throw new Error(`[nuxt] \`${factory.name}\` is a compiler macro and cannot be called at runtime.`);
  };
  return Object.defineProperty(placeholder, "__nuxt_factory", {
    enumerable: false,
    get: () => factory.factory
  });
}
