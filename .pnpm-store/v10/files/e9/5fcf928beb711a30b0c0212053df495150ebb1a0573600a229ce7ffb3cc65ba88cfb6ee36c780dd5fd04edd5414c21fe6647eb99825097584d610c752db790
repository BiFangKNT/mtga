const entry = import.meta.server ? (ctx) => import("#app/entry").then((m) => m.default(ctx)) : () => import("#app/entry").then((m) => m.default);
if (import.meta.client) {
  entry();
}
export default entry;
