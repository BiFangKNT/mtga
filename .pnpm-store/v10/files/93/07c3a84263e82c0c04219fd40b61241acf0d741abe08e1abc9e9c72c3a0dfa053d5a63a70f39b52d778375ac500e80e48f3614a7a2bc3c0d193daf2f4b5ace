const KEY_IGNORE = "data-v-inspector-ignore";
const KEY_GLOBAL = "__vue_tracer__";
let _store = globalThis[KEY_GLOBAL];
if (!_store) {
  _store = {
    hasData: false,
    vnodeToPos: /* @__PURE__ */ new WeakMap(),
    fileToVNode: /* @__PURE__ */ new Map(),
    posToVNode: /* @__PURE__ */ new Map()
  };
  Object.defineProperty(globalThis, KEY_GLOBAL, {
    value: _store,
    configurable: true,
    enumerable: false
  });
}
function getInternalStore() {
  return _store;
}
function recordPosition(source, line, column, node) {
  if (!node || typeof node === "string" || typeof node === "number")
    return node;
  if (!_store.hasData)
    _store.hasData = true;
  const props = node.props ||= {};
  _store.vnodeToPos.set(props, [source, line, column]);
  if (!_store.fileToVNode.has(source))
    _store.fileToVNode.set(source, /* @__PURE__ */ new WeakSet());
  _store.fileToVNode.get(source).add(props);
  if (!_store.posToVNode.has(source))
    _store.posToVNode.set(source, /* @__PURE__ */ new Map());
  const lineMap = _store.posToVNode.get(source);
  if (!lineMap.has(line))
    lineMap.set(line, /* @__PURE__ */ new Map());
  const columnMap = lineMap.get(line);
  if (!columnMap.has(column))
    columnMap.set(column, /* @__PURE__ */ new WeakSet());
  columnMap.get(column).add(props);
  return node;
}
function getPositionFromVNode(node) {
  const props = node?.props;
  if (props)
    return _store.vnodeToPos.get(props);
}
class ElementTraceInfo {
  pos;
  vnode;
  el;
  constructor(pos, el, vnode) {
    this.vnode = vnode;
    this.pos = pos;
    this.el = el;
  }
  get filepath() {
    return this.pos[0];
  }
  get fullpath() {
    let path = this.pos[0];
    if (this.pos[1]) {
      path += `:${this.pos[1]}`;
      if (this.pos[2])
        path += `:${this.pos[2]}`;
    }
    return path;
  }
  get rect() {
    return this.el?.getBoundingClientRect();
  }
  getElementsSameFile() {
    const pos = this.pos;
    const fileVNodeSet = _store.fileToVNode.get(pos[0]);
    if (!fileVNodeSet)
      return;
    const sameFile = fileVNodeSet ? Array.from(document.querySelectorAll("*")).filter((e) => e !== this.el && e.__vnode?.props && fileVNodeSet.has(e.__vnode?.props)) : [];
    return sameFile;
  }
  getParent() {
    const parentVNode = this.vnode?.parent;
    const parentEl = this.el?.parentElement;
    return findTraceFromVNode(parentVNode) ?? findTraceFromElement(parentEl);
  }
  getElementsSamePosition() {
    if (typeof this.vnode?.type !== "string")
      return;
    const pos = this.pos;
    const posVNodeSet = _store.posToVNode.get(pos[0])?.get(pos[1])?.get(pos[2]);
    if (!posVNodeSet)
      return;
    const samePos = posVNodeSet ? Array.from(document.querySelectorAll(this.vnode.type)).filter((e) => e !== this.el && e.__vnode?.props && posVNodeSet.has(e.__vnode?.props)) : [];
    return samePos;
  }
}
function findTraceFromElement(el) {
  if (!el)
    return;
  const vnode = el.__vnode;
  return findTraceFromVNode(vnode, el);
}
function findTraceFromVNode(vnode, el) {
  if (!vnode)
    return;
  const pos = getPositionFromVNode(vnode);
  if (!pos)
    return;
  return new ElementTraceInfo(pos, el ?? vnode?.el ?? void 0, vnode);
}
function findTraceAtPointer(e) {
  let elements = document.elementsFromPoint(e.x, e.y);
  const ignoreIndex = elements.findIndex((node) => node?.hasAttribute?.(KEY_IGNORE));
  if (ignoreIndex !== -1)
    elements = elements.slice(ignoreIndex);
  for (const el of elements) {
    const match = findTraceFromElement(el);
    if (match)
      return match;
  }
}
function hasData() {
  return _store.hasData;
}

export { ElementTraceInfo, findTraceAtPointer, findTraceFromElement, findTraceFromVNode, getInternalStore, hasData, recordPosition };
