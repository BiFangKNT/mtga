import { shallowRef } from "vue";
import { useObjectStorage } from "./utils.js";
export const popupWindow = shallowRef(null);
export const state = useObjectStorage("nuxt-devtools-frame-state", {
  width: 80,
  height: 60,
  top: 0,
  left: 50,
  open: false,
  route: "/",
  position: "bottom",
  closeOnOutsideClick: false,
  minimizePanelInactive: 5e3
}, false);
