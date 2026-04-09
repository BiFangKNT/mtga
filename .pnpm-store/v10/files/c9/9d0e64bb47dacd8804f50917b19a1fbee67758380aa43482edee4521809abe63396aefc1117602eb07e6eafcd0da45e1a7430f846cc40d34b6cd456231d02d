import { reactive, watchEffect } from 'vue';
import { isEnabled, events, lastMatchedElement } from './listeners.mjs';
export { ElementTraceInfo, findTraceAtPointer, findTraceFromElement, findTraceFromVNode, getInternalStore, hasData, recordPosition } from './record.mjs';

const state = reactive({
  isEnabled,
  isVisible: false,
  isFocused: false,
  isAnimated: true,
  sub: {}
});
const ANIMATE_DURATION = "0.15s";
const PADDING_FOCUSED = 10;
function createOverlay() {
  const overlay = document.createElement("div");
  overlay.id = "vue-tracer-overlay";
  Object.assign(overlay.style, {
    position: "fixed",
    top: "0",
    left: "0",
    bottom: "0",
    right: "0",
    zIndex: "999999",
    pointerEvents: "none",
    opacity: "0"
  });
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  Object.assign(svg.style, {
    position: "fixed",
    top: "0",
    left: "0",
    bottom: "0",
    pointerEvents: "none",
    right: "0"
  });
  svg.setAttribute("width", "100%");
  svg.setAttribute("height", "100%");
  const mainText = document.createElement("div");
  Object.assign(mainText.style, {
    position: "fixed",
    top: "0",
    left: "0",
    transition: `all ${ANIMATE_DURATION}`,
    backgroundColor: "#197",
    color: "#fff",
    borderBottomLeftRadius: "4px",
    borderBottomRightRadius: "4px",
    padding: "1px 4px",
    pointerEvents: "none",
    fontSize: "10px",
    fontFamily: "monospace",
    display: "flex",
    gap: "0.25rem",
    boxShadow: "0 0 2px rgba(0,0,0,0.2)"
  });
  const mainTextTag = document.createElement("div");
  const mainTextPath = document.createElement("div");
  Object.assign(mainTextPath.style, {
    opacity: "0.75",
    fontSize: "9px"
  });
  mainText.appendChild(mainTextTag);
  mainText.appendChild(mainTextPath);
  const mainRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  mainRect.setAttribute("fill", "#1972");
  mainRect.setAttribute("stroke", "#197");
  mainRect.setAttribute("rx", "4");
  mainRect.setAttribute("ry", "4");
  overlay.appendChild(svg);
  overlay.appendChild(mainText);
  svg.appendChild(mainRect);
  document.body.appendChild(overlay);
  watchEffect(() => {
    overlay.style.transition = state.isAnimated ? `all ${ANIMATE_DURATION}` : "none";
    mainText.style.transition = state.isAnimated ? `all ${ANIMATE_DURATION}` : "none";
    mainRect.style.transition = state.isAnimated ? `all ${ANIMATE_DURATION}` : "none";
    overlay.style.opacity = state.isVisible ? "1" : "0";
  });
  watchEffect(() => {
    if (state.main && state.main.rect) {
      const rect = state.main.rect;
      mainRect.style.opacity = "1";
      if (state.isFocused) {
        mainRect.setAttribute("rx", "8");
        mainRect.setAttribute("ry", "8");
        mainRect.setAttribute("x", String(rect.left - PADDING_FOCUSED));
        mainRect.setAttribute("y", String(rect.top - PADDING_FOCUSED));
        mainRect.setAttribute("width", String(rect.width + PADDING_FOCUSED * 2));
        mainRect.setAttribute("height", String(rect.height + PADDING_FOCUSED * 2));
        mainRect.style.filter = "blur(1px)";
      } else {
        mainRect.setAttribute("rx", "4");
        mainRect.setAttribute("ry", "4");
        mainRect.setAttribute("x", String(rect.left));
        mainRect.setAttribute("y", String(rect.top));
        mainRect.setAttribute("width", String(rect.width));
        mainRect.setAttribute("height", String(rect.height));
        mainRect.style.filter = "";
      }
      mainRect.style.fill = state.isFocused ? "transparent" : "#1972";
      mainText.style.opacity = state.isFocused ? "0" : "1";
      mainTextTag.textContent = "";
      let tagName = "";
      if (state.main?.vnode?.type) {
        if (typeof state.main?.vnode?.type === "string")
          tagName = state.main.vnode.type;
        else
          tagName = state.main.vnode.type.name;
      }
      mainTextTag.textContent = tagName ? `<${tagName}>` : "";
      mainTextPath.textContent = `${state.main.pos[0]}:${state.main.pos[1]}:${state.main.pos[2]}`;
      Object.assign(mainText.style, {
        left: `${rect.left + 3}px`,
        top: `${rect.top + rect.height - 1}px`
      });
    } else {
      mainText.style.opacity = "0";
      mainRect.style.opacity = "0";
    }
  });
  const subMap = /* @__PURE__ */ new Map();
  watchEffect(() => {
    const toRemove = new Set(subMap.keys());
    for (const { id, rect } of state.sub.rects || []) {
      toRemove.delete(id);
      let cover = subMap.get(id);
      if (!cover) {
        cover = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        cover.setAttribute("fill", "#8482");
        cover.setAttribute("stroke", "#848");
        cover.setAttribute("rx", "4");
        cover.setAttribute("ry", "4");
        svg.appendChild(cover);
        subMap.set(id, cover);
      }
      cover.style.transition = state.isAnimated ? `all ${ANIMATE_DURATION}` : "none";
      cover.setAttribute("x", String(rect.left));
      cover.setAttribute("y", String(rect.top));
      cover.setAttribute("width", String(rect.width));
      cover.setAttribute("height", String(rect.height));
      cover.style.opacity = "1";
    }
    for (const id of toRemove) {
      const cover = subMap.get(id);
      if (cover) {
        cover.style.opacity = "0";
        setTimeout(() => cover.remove(), 300);
        subMap.delete(id);
      }
    }
  });
}
const elementId = /* @__PURE__ */ new WeakMap();
function getElementId(el) {
  let id = elementId.get(el);
  if (!id) {
    id = Math.random().toString(16).slice(2);
    elementId.set(el, id);
  }
  return id;
}
function update(result) {
  if (!result) {
    state.isVisible = false;
    state.sub.rects = void 0;
    state.main = void 0;
    return;
  }
  state.isVisible = true;
  state.main = result;
  const samePos = result.getElementsSamePosition();
  state.sub.rects = samePos?.map((el) => ({
    id: getElementId(el),
    rect: el.getBoundingClientRect()
  }));
}
function init() {
  createOverlay();
  events.on("hover", (result) => {
    update(result);
  });
  document.addEventListener("scroll", () => {
    if (state.isVisible)
      update(lastMatchedElement.value);
  });
  window.addEventListener("resize", () => {
    if (state.isVisible)
      update(lastMatchedElement.value);
  });
}
init();

export { events, isEnabled, lastMatchedElement, state };
