import { isRef, toRefs as toRefs$1, customRef, toValue, onMounted, nextTick, watch, getCurrentInstance, getCurrentScope, onScopeDispose, shallowRef, computed, ref, unref, defineComponent, useModel, watchEffect, mergeModels, withDirectives, openBlock, createElementBlock, createCommentVNode, createElementVNode, withModifiers, vShow, reactive, useTemplateRef, normalizeClass, normalizeStyle, toDisplayString, Fragment, createVNode, defineCustomElement, createTextVNode } from 'vue';

const css = `*{box-sizing:border-box;border-style:solid;border-width:0;border-color:var(--un-default-border-color,#e5e7eb)}:before{box-sizing:border-box;border-style:solid;border-width:0;border-color:var(--un-default-border-color,#e5e7eb)}:after{box-sizing:border-box;border-style:solid;border-width:0;border-color:var(--un-default-border-color,#e5e7eb)}:before{--un-content:""}:after{--un-content:""}html{-webkit-text-size-adjust:100%;tab-size:4;font-feature-settings:normal;font-variation-settings:normal;-webkit-tap-highlight-color:transparent;font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Noto Sans,Ubuntu,Cantarell,Helvetica Neue,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;line-height:1.5}:host{-webkit-text-size-adjust:100%;tab-size:4;font-feature-settings:normal;font-variation-settings:normal;-webkit-tap-highlight-color:transparent;font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Noto Sans,Ubuntu,Cantarell,Helvetica Neue,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;line-height:1.5}body{line-height:inherit;margin:0}hr{height:0;color:inherit;border-top-width:1px}abbr:where([title]){text-decoration:underline dotted}h1,h2,h3,h4,h5,h6{font-size:inherit;font-weight:inherit}a{color:inherit;text-decoration:inherit}b,strong{font-weight:bolder}code,kbd,samp,pre{font-feature-settings:normal;font-variation-settings:normal;font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace;font-size:1em}small{font-size:80%}sub,sup{vertical-align:baseline;font-size:75%;line-height:0;position:relative}sub{bottom:-.25em}sup{top:-.5em}table{text-indent:0;border-color:inherit;border-collapse:collapse}button,input,optgroup,select,textarea{font-feature-settings:inherit;font-variation-settings:inherit;font-family:inherit;font-size:100%;font-weight:inherit;line-height:inherit;color:inherit;margin:0;padding:0}button,select{text-transform:none}button{-webkit-appearance:button;background-color:transparent;background-image:none}[type=button]{-webkit-appearance:button;background-color:transparent;background-image:none}[type=reset]{-webkit-appearance:button;background-color:transparent;background-image:none}[type=submit]{-webkit-appearance:button;background-color:transparent;background-image:none}:-moz-focusring{outline:auto}:-moz-ui-invalid{box-shadow:none}progress{vertical-align:baseline}::-webkit-inner-spin-button{height:auto}::-webkit-outer-spin-button{height:auto}[type=search]{-webkit-appearance:textfield;outline-offset:-2px}::-webkit-search-decoration{-webkit-appearance:none}::-webkit-file-upload-button{-webkit-appearance:button;font:inherit}summary{display:list-item}blockquote,dl,dd,h1,h2,h3,h4,h5,h6,hr,figure,p,pre{margin:0}fieldset{margin:0;padding:0}legend{padding:0}ol,ul,menu{margin:0;padding:0;list-style:none}dialog{padding:0}textarea{resize:vertical}input::placeholder{opacity:1;color:#9ca3af}textarea::placeholder{opacity:1;color:#9ca3af}button{cursor:pointer}[role=button]{cursor:pointer}:disabled{cursor:default}img,svg,video,canvas,audio,iframe,embed,object{vertical-align:middle;display:block}img,video{max-width:100%;height:auto}[hidden]:where(:not([hidden=until-found])){display:none}:root{--un-text-opacity:100%}@property --nuxt-devtools-inspect-border-angle{syntax:"<angle>";inherits:false;initial-value:90deg}.nuxt-devtools-inspect-running-border{filter:blur(10px);--nuxt-devtools-inspect-border-angle:0deg;background:conic-gradient(from var(--nuxt-devtools-inspect-border-angle), #00dc82, #00e6e8, #42e200, #0086e2, #00dc82) border-box;-webkit-mask:linear-gradient(#fff 0,#fff 0) padding-box,linear-gradient(#fff 0,#fff 0);-webkit-mask-composite:destination-out;transition:all .5s;animation:1s linear infinite color-rotate-background;mask-image:linear-gradient(#fff 0,#fff 0),linear-gradient(#fff 0,#fff 0);mask-position:0 0,0 0;mask-size:auto,auto;mask-repeat:repeat,repeat;mask-clip:padding-box,border-box;mask-origin:padding-box,border-box;mask-composite:exclude;mask-mode:match-source,match-source}.nuxt-devtools-inspect-neon{background-image:linear-gradient(90deg,#00dc82,#00e6e8,#42e200,#00dc82,#00e6e8,#42e200,#00dc82,#00e6e8,#42e200);background-position:0;background-size:400% 400%}.nuxt-devtools-inspect-neon.running{animation:3s linear infinite neon-background}@keyframes neon-background{0%{background-position:0%}50%{background-position:100%}to{background-position:0%}}.nuxt-devtools-frame{z-index:2147483645;-webkit-font-smoothing:antialiased;width:100%;height:100%;position:fixed}.nuxt-devtools-frame iframe{background:var(--nuxt-devtools-widget-bg);border:1px solid rgba(125,125,125,.2);-webkit-border-radius:10px;border-radius:10px;outline:none;width:100%;height:100%}.nuxt-devtools-resize-handle-horizontal{cursor:ns-resize;-webkit-border-radius:5px;border-radius:5px;height:10px;margin:-5px 0;position:absolute;left:6px;right:6px}.nuxt-devtools-resize-handle-vertical{cursor:ew-resize;-webkit-border-radius:5px;border-radius:5px;width:10px;margin:0 -5px;position:absolute;top:6px;bottom:0}.nuxt-devtools-resize-handle-corner{-webkit-border-radius:6px;border-radius:6px;width:14px;height:14px;margin:-6px;position:absolute}.nuxt-devtools-resize-handle:hover{background:rgba(125,125,125,.1)}#nuxt-devtools-anchor{z-index:2147483645;transform-origin:50%;box-sizing:border-box;width:0;font-family:Arial,Helvetica,sans-serif;position:fixed;transform:translate(-50%,-50%)rotate(0);font-size:15px!important}#nuxt-devtools-anchor *{box-sizing:border-box}#nuxt-devtools-anchor button{cursor:pointer;color:inherit;background:0 0;border:none;outline:none;margin:0;padding:0}#nuxt-devtools-anchor .nuxt-devtools-label{align-items:center;justify-items:center;gap:3px;padding:0 7px 0 8px;font-size:.8em;line-height:1em;display:flex}#nuxt-devtools-anchor .nuxt-devtools-label .nuxt-devtools-label-main{opacity:.8;white-space:nowrap}#nuxt-devtools-anchor .nuxt-devtools-label .nuxt-devtools-label-secondary{opacity:.5;white-space:nowrap;font-size:.8em;line-height:.6em}#nuxt-devtools-anchor .nuxt-devtools-nuxt-button{flex:none}#nuxt-devtools-anchor.nuxt-devtools-vertical .nuxt-devtools-nuxt-button{transform:rotate(-90deg)}#nuxt-devtools-anchor.nuxt-devtools-vertical .nuxt-devtools-label{flex-direction:column;gap:2px;padding:0 10px;transform:rotate(-90deg)}#nuxt-devtools-anchor .nuxt-devtools-panel{border:1px solid var(--nuxt-devtools-widget-border);background-color:var(--nuxt-devtools-widget-bg);backdrop-filter:blur(10px);height:30px;color:var(--nuxt-devtools-widget-fg);box-shadow:2px 2px 8px var(--nuxt-devtools-widget-shadow);user-select:none;touch-action:none;-webkit-border-radius:100px;border-radius:100px;justify-content:flex-start;align-items:center;gap:2px;max-width:150px;padding:2px 2px 2px 2.5px;transition:all .6s,max-width .6s,padding .5s,transform .4s,opacity .2s;display:flex;position:absolute;top:0;left:0;overflow:hidden;transform:translate(-50%,-50%)}#nuxt-devtools-anchor.nuxt-devtools-hide .nuxt-devtools-panel{max-width:32px;padding:2px 0}#nuxt-devtools-anchor.nuxt-devtools-vertical .nuxt-devtools-panel{box-shadow:2px -2px 8px var(--nuxt-devtools-widget-shadow);transform:translate(-50%,-50%)rotate(90deg)}#nuxt-devtools-anchor .nuxt-devtools-panel-content{transition:opacity .4s}#nuxt-devtools-anchor.nuxt-devtools-hide .nuxt-devtools-panel-content{opacity:0}#nuxt-devtools-anchor .nuxt-devtools-icon-button{opacity:.8;border-width:0;-webkit-border-radius:100%;border-radius:100%;justify-content:center;align-items:center;width:30px;height:30px;transition:opacity .2s ease-in-out;display:flex}#nuxt-devtools-anchor .nuxt-devtools-icon-button:hover{opacity:1}#nuxt-devtools-anchor:hover .nuxt-devtools-glowing{opacity:.6}#nuxt-devtools-anchor .nuxt-devtools-glowing{opacity:0;pointer-events:none;z-index:-1;filter:blur(60px);background-image:linear-gradient(45deg,#00dc82,#00dc82,#00dc82);-webkit-border-radius:9999px;border-radius:9999px;width:160px;height:160px;transition:all 1s;position:absolute;top:0;left:0;transform:translate(-50%,-50%)}@media print{#nuxt-devtools-anchor{display:none}}*{--un-rotate:0;--un-rotate-x:0;--un-rotate-y:0;--un-rotate-z:0;--un-scale-x:1;--un-scale-y:1;--un-scale-z:1;--un-skew-x:0;--un-skew-y:0;--un-translate-x:0;--un-translate-y:0;--un-translate-z:0;--un-pan-x: ;--un-pan-y: ;--un-pinch-zoom: ;--un-scroll-snap-strictness:proximity;--un-ordinal: ;--un-slashed-zero: ;--un-numeric-figure: ;--un-numeric-spacing: ;--un-numeric-fraction: ;--un-border-spacing-x:0;--un-border-spacing-y:0;--un-ring-offset-shadow:0 0 transparent;--un-ring-shadow:0 0 transparent;--un-shadow-inset: ;--un-shadow:0 0 transparent;--un-ring-inset: ;--un-ring-offset-width:0px;--un-ring-offset-color:#fff;--un-ring-width:0px;--un-ring-color:rgba(147,197,253,.5);--un-blur: ;--un-brightness: ;--un-contrast: ;--un-drop-shadow: ;--un-grayscale: ;--un-hue-rotate: ;--un-invert: ;--un-saturate: ;--un-sepia: ;--un-backdrop-blur: ;--un-backdrop-brightness: ;--un-backdrop-contrast: ;--un-backdrop-grayscale: ;--un-backdrop-hue-rotate: ;--un-backdrop-invert: ;--un-backdrop-opacity: ;--un-backdrop-saturate: ;--un-backdrop-sepia: }:before{--un-rotate:0;--un-rotate-x:0;--un-rotate-y:0;--un-rotate-z:0;--un-scale-x:1;--un-scale-y:1;--un-scale-z:1;--un-skew-x:0;--un-skew-y:0;--un-translate-x:0;--un-translate-y:0;--un-translate-z:0;--un-pan-x: ;--un-pan-y: ;--un-pinch-zoom: ;--un-scroll-snap-strictness:proximity;--un-ordinal: ;--un-slashed-zero: ;--un-numeric-figure: ;--un-numeric-spacing: ;--un-numeric-fraction: ;--un-border-spacing-x:0;--un-border-spacing-y:0;--un-ring-offset-shadow:0 0 transparent;--un-ring-shadow:0 0 transparent;--un-shadow-inset: ;--un-shadow:0 0 transparent;--un-ring-inset: ;--un-ring-offset-width:0px;--un-ring-offset-color:#fff;--un-ring-width:0px;--un-ring-color:rgba(147,197,253,.5);--un-blur: ;--un-brightness: ;--un-contrast: ;--un-drop-shadow: ;--un-grayscale: ;--un-hue-rotate: ;--un-invert: ;--un-saturate: ;--un-sepia: ;--un-backdrop-blur: ;--un-backdrop-brightness: ;--un-backdrop-contrast: ;--un-backdrop-grayscale: ;--un-backdrop-hue-rotate: ;--un-backdrop-invert: ;--un-backdrop-opacity: ;--un-backdrop-saturate: ;--un-backdrop-sepia: }:after{--un-rotate:0;--un-rotate-x:0;--un-rotate-y:0;--un-rotate-z:0;--un-scale-x:1;--un-scale-y:1;--un-scale-z:1;--un-skew-x:0;--un-skew-y:0;--un-translate-x:0;--un-translate-y:0;--un-translate-z:0;--un-pan-x: ;--un-pan-y: ;--un-pinch-zoom: ;--un-scroll-snap-strictness:proximity;--un-ordinal: ;--un-slashed-zero: ;--un-numeric-figure: ;--un-numeric-spacing: ;--un-numeric-fraction: ;--un-border-spacing-x:0;--un-border-spacing-y:0;--un-ring-offset-shadow:0 0 transparent;--un-ring-shadow:0 0 transparent;--un-shadow-inset: ;--un-shadow:0 0 transparent;--un-ring-inset: ;--un-ring-offset-width:0px;--un-ring-offset-color:#fff;--un-ring-width:0px;--un-ring-color:rgba(147,197,253,.5);--un-blur: ;--un-brightness: ;--un-contrast: ;--un-drop-shadow: ;--un-grayscale: ;--un-hue-rotate: ;--un-invert: ;--un-saturate: ;--un-sepia: ;--un-backdrop-blur: ;--un-backdrop-brightness: ;--un-backdrop-contrast: ;--un-backdrop-grayscale: ;--un-backdrop-hue-rotate: ;--un-backdrop-invert: ;--un-backdrop-opacity: ;--un-backdrop-saturate: ;--un-backdrop-sepia: }::backdrop{--un-rotate:0;--un-rotate-x:0;--un-rotate-y:0;--un-rotate-z:0;--un-scale-x:1;--un-scale-y:1;--un-scale-z:1;--un-skew-x:0;--un-skew-y:0;--un-translate-x:0;--un-translate-y:0;--un-translate-z:0;--un-pan-x: ;--un-pan-y: ;--un-pinch-zoom: ;--un-scroll-snap-strictness:proximity;--un-ordinal: ;--un-slashed-zero: ;--un-numeric-figure: ;--un-numeric-spacing: ;--un-numeric-fraction: ;--un-border-spacing-x:0;--un-border-spacing-y:0;--un-ring-offset-shadow:0 0 transparent;--un-ring-shadow:0 0 transparent;--un-shadow-inset: ;--un-shadow:0 0 transparent;--un-ring-inset: ;--un-ring-offset-width:0px;--un-ring-offset-color:#fff;--un-ring-width:0px;--un-ring-color:rgba(147,197,253,.5);--un-blur: ;--un-brightness: ;--un-contrast: ;--un-drop-shadow: ;--un-grayscale: ;--un-hue-rotate: ;--un-invert: ;--un-saturate: ;--un-sepia: ;--un-backdrop-blur: ;--un-backdrop-brightness: ;--un-backdrop-contrast: ;--un-backdrop-grayscale: ;--un-backdrop-hue-rotate: ;--un-backdrop-invert: ;--un-backdrop-opacity: ;--un-backdrop-saturate: ;--un-backdrop-sepia: }.i-ph-arrow-bend-left-up-duotone{--un-icon:url("data:image/svg+xml;utf8,%3Csvg viewBox='0 0 256 256' width='1em' height='1em' xmlns='http://www.w3.org/2000/svg' %3E%3Cg fill='currentColor'%3E%3Cpath d='M152 80H56l48-48Z' opacity='.2'/%3E%3Cpath d='M200 216a88.1 88.1 0 0 1-88-88V88h40a8 8 0 0 0 5.66-13.66l-48-48a8 8 0 0 0-11.32 0l-48 48A8 8 0 0 0 56 88h40v40a104.11 104.11 0 0 0 104 104a8 8 0 0 0 0-16M104 43.31L132.69 72H75.31Z'/%3E%3C/g%3E%3C/svg%3E");-webkit-mask:var(--un-icon) no-repeat;mask:var(--un-icon) no-repeat;color:inherit;background-color:currentColor;width:1em;height:1em;mask-size:100% 100%}.i-ph-arrow-up-right-light{--un-icon:url("data:image/svg+xml;utf8,%3Csvg viewBox='0 0 256 256' width='1em' height='1em' xmlns='http://www.w3.org/2000/svg' %3E%3Cpath fill='currentColor' d='M198 64v104a6 6 0 0 1-12 0V78.48L68.24 196.24a6 6 0 0 1-8.48-8.48L177.52 70H88a6 6 0 0 1 0-12h104a6 6 0 0 1 6 6'/%3E%3C/svg%3E");-webkit-mask:var(--un-icon) no-repeat;mask:var(--un-icon) no-repeat;color:inherit;background-color:currentColor;width:1em;height:1em;mask-size:100% 100%}.i-ph-check-circle-duotone{--un-icon:url("data:image/svg+xml;utf8,%3Csvg viewBox='0 0 256 256' width='1em' height='1em' xmlns='http://www.w3.org/2000/svg' %3E%3Cg fill='currentColor'%3E%3Cpath d='M224 128a96 96 0 1 1-96-96a96 96 0 0 1 96 96' opacity='.2'/%3E%3Cpath d='M173.66 98.34a8 8 0 0 1 0 11.32l-56 56a8 8 0 0 1-11.32 0l-24-24a8 8 0 0 1 11.32-11.32L112 148.69l50.34-50.35a8 8 0 0 1 11.32 0M232 128A104 104 0 1 1 128 24a104.11 104.11 0 0 1 104 104m-16 0a88 88 0 1 0-88 88a88.1 88.1 0 0 0 88-88'/%3E%3C/g%3E%3C/svg%3E");-webkit-mask:var(--un-icon) no-repeat;mask:var(--un-icon) no-repeat;color:inherit;background-color:currentColor;width:1em;height:1em;mask-size:100% 100%}.i-ph-copy-duotone{--un-icon:url("data:image/svg+xml;utf8,%3Csvg viewBox='0 0 256 256' width='1em' height='1em' xmlns='http://www.w3.org/2000/svg' %3E%3Cg fill='currentColor'%3E%3Cpath d='M216 40v128h-48V88H88V40Z' opacity='.2'/%3E%3Cpath d='M216 32H88a8 8 0 0 0-8 8v40H40a8 8 0 0 0-8 8v128a8 8 0 0 0 8 8h128a8 8 0 0 0 8-8v-40h40a8 8 0 0 0 8-8V40a8 8 0 0 0-8-8m-56 176H48V96h112Zm48-48h-32V88a8 8 0 0 0-8-8H96V48h112Z'/%3E%3C/g%3E%3C/svg%3E");-webkit-mask:var(--un-icon) no-repeat;mask:var(--un-icon) no-repeat;color:inherit;background-color:currentColor;width:1em;height:1em;mask-size:100% 100%}.i-ph-file-duotone{--un-icon:url("data:image/svg+xml;utf8,%3Csvg viewBox='0 0 256 256' width='1em' height='1em' xmlns='http://www.w3.org/2000/svg' %3E%3Cg fill='currentColor'%3E%3Cpath d='M208 88h-56V32Z' opacity='.2'/%3E%3Cpath d='m213.66 82.34l-56-56A8 8 0 0 0 152 24H56a16 16 0 0 0-16 16v176a16 16 0 0 0 16 16h144a16 16 0 0 0 16-16V88a8 8 0 0 0-2.34-5.66M160 51.31L188.69 80H160ZM200 216H56V40h88v48a8 8 0 0 0 8 8h48z'/%3E%3C/g%3E%3C/svg%3E");-webkit-mask:var(--un-icon) no-repeat;mask:var(--un-icon) no-repeat;color:inherit;background-color:currentColor;width:1em;height:1em;mask-size:100% 100%}.i-ph-tree-view-duotone{--un-icon:url("data:image/svg+xml;utf8,%3Csvg viewBox='0 0 256 256' width='1em' height='1em' xmlns='http://www.w3.org/2000/svg' %3E%3Cg fill='currentColor'%3E%3Cpath d='M104 32v32a8 8 0 0 1-8 8H64a8 8 0 0 1-8-8V32a8 8 0 0 1 8-8h32a8 8 0 0 1 8 8m104 64h-32a8 8 0 0 0-8 8v32a8 8 0 0 0 8 8h32a8 8 0 0 0 8-8v-32a8 8 0 0 0-8-8m0 88h-32a8 8 0 0 0-8 8v32a8 8 0 0 0 8 8h32a8 8 0 0 0 8-8v-32a8 8 0 0 0-8-8' opacity='.2'/%3E%3Cpath d='M176 152h32a16 16 0 0 0 16-16v-32a16 16 0 0 0-16-16h-32a16 16 0 0 0-16 16v8H88V80h8a16 16 0 0 0 16-16V32a16 16 0 0 0-16-16H64a16 16 0 0 0-16 16v32a16 16 0 0 0 16 16h8v112a24 24 0 0 0 24 24h64v8a16 16 0 0 0 16 16h32a16 16 0 0 0 16-16v-32a16 16 0 0 0-16-16h-32a16 16 0 0 0-16 16v8H96a8 8 0 0 1-8-8v-64h72v8a16 16 0 0 0 16 16M64 32h32v32H64Zm112 160h32v32h-32Zm0-88h32v32h-32Z'/%3E%3C/g%3E%3C/svg%3E");-webkit-mask:var(--un-icon) no-repeat;mask:var(--un-icon) no-repeat;color:inherit;background-color:currentColor;width:1em;height:1em;mask-size:100% 100%}.i-ph-x{--un-icon:url("data:image/svg+xml;utf8,%3Csvg viewBox='0 0 256 256' width='1em' height='1em' xmlns='http://www.w3.org/2000/svg' %3E%3Cpath fill='currentColor' d='M205.66 194.34a8 8 0 0 1-11.32 11.32L128 139.31l-66.34 66.35a8 8 0 0 1-11.32-11.32L116.69 128L50.34 61.66a8 8 0 0 1 11.32-11.32L128 116.69l66.34-66.35a8 8 0 0 1 11.32 11.32L139.31 128Z'/%3E%3C/svg%3E");-webkit-mask:var(--un-icon) no-repeat;mask:var(--un-icon) no-repeat;color:inherit;background-color:currentColor;width:1em;height:1em;mask-size:100% 100%}.container{width:100%}.border-base{--un-border-opacity:.13;border-color:rgba(136,136,136,var(--un-border-opacity))}.bg-glass{--un-backdrop-blur:blur(5px);backdrop-filter:var(--un-backdrop-blur) var(--un-backdrop-brightness) var(--un-backdrop-contrast) var(--un-backdrop-grayscale) var(--un-backdrop-hue-rotate) var(--un-backdrop-invert) var(--un-backdrop-opacity) var(--un-backdrop-saturate) var(--un-backdrop-sepia);background-color:rgba(255,255,255,.75)}.color-base{--un-text-opacity:1;color:rgba(38,38,38,var(--un-text-opacity))}.ring-base{--un-ring-opacity:.13;--un-ring-color:rgba(136,136,136,var(--un-ring-opacity))}@media (prefers-color-scheme:dark){.bg-glass{background-color:rgba(17,17,17,.75)}.color-base{--un-text-opacity:1;color:rgba(229,229,229,var(--un-text-opacity))}}@media (min-width:640px){.container{max-width:640px}}@media (min-width:768px){.container{max-width:768px}}@media (min-width:1024px){.container{max-width:1024px}}@media (min-width:1280px){.container{max-width:1280px}}@media (min-width:1536px){.container{max-width:1536px}}.pointer-events-none{pointer-events:none}.disabled\\:pointer-events-none:disabled{pointer-events:none}.absolute{position:absolute}.fixed{position:fixed}.relative{position:relative}.inset-0{top:0;bottom:0;left:0;right:0}.bottom-20px{bottom:20px}.right-20px{right:20px}.z-10{z-index:10}.z-9999999{z-index:9999999}.z-99999999{z-index:99999999}.grid{display:grid}.grid-cols-\\[max-content_1fr\\]{grid-template-columns:max-content 1fr}.ms:not(:is(:lang(ae),:lang(ar),:lang(arc),:lang(bcc),:lang(bqi),:lang(ckb),:lang(dv),:lang(fa),:lang(glk),:lang(he),:lang(ku),:lang(mzn),:lang(nqo),:lang(pnb),:lang(ps),:lang(sd),:lang(ug),:lang(ur),:lang(yi))){margin-left:1rem}.ms:is(:lang(ae),:lang(ar),:lang(arc),:lang(bcc),:lang(bqi),:lang(ckb),:lang(dv),:lang(fa),:lang(glk),:lang(he),:lang(ku),:lang(mzn),:lang(nqo),:lang(pnb),:lang(ps),:lang(sd),:lang(ug),:lang(ur),:lang(yi)){margin-right:1rem}.mt-2{margin-top:.5rem}.max-h-200px{max-height:200px}.max-w-500px{max-width:500px}.w-400px{width:400px}.flex{display:flex}.flex-auto{flex:auto}.flex-none{flex:none}.flex-col{flex-direction:column}.translate-y-0{--un-translate-y:0;transform:translateX(var(--un-translate-x)) translateY(var(--un-translate-y)) translateZ(var(--un-translate-z)) rotate(var(--un-rotate)) rotateX(var(--un-rotate-x)) rotateY(var(--un-rotate-y)) rotateZ(var(--un-rotate-z)) skewX(var(--un-skew-x)) skewY(var(--un-skew-y)) scaleX(var(--un-scale-x)) scaleY(var(--un-scale-y)) scaleZ(var(--un-scale-z))}.translate-y-10{--un-translate-y:2.5rem;transform:translateX(var(--un-translate-x)) translateY(var(--un-translate-y)) translateZ(var(--un-translate-z)) rotate(var(--un-rotate)) rotateX(var(--un-rotate-x)) rotateY(var(--un-rotate-y)) rotateZ(var(--un-rotate-z)) skewX(var(--un-skew-x)) skewY(var(--un-skew-y)) scaleX(var(--un-scale-x)) scaleY(var(--un-scale-y)) scaleZ(var(--un-scale-z))}.transform{transform:translateX(var(--un-translate-x)) translateY(var(--un-translate-y)) translateZ(var(--un-translate-z)) rotate(var(--un-rotate)) rotateX(var(--un-rotate-x)) rotateY(var(--un-rotate-y)) rotateZ(var(--un-rotate-z)) skewX(var(--un-skew-x)) skewY(var(--un-skew-y)) scaleX(var(--un-scale-x)) scaleY(var(--un-scale-y)) scaleZ(var(--un-scale-z))}.resize{resize:both}.items-center{align-items:center}.gap-2{gap:.5rem}.of-auto{overflow:auto}.of-hidden{overflow:hidden}.whitespace-pre-wrap{white-space:pre-wrap}.break-all{word-break:break-all}.border-1{border-width:1px}.border-1\\.5{border-width:1.5px}.border-transparent{border-color:transparent}.rounded{-webkit-border-radius:.25rem;border-radius:.25rem}.rounded-lg{-webkit-border-radius:.5rem;border-radius:.5rem}.bg-black{--un-bg-opacity:1;background-color:rgba(0,0,0,var(--un-bg-opacity))}.bg-op-20{--un-bg-opacity:.2}.p2{padding:.5rem}.p4{padding:1rem}.px{padding-left:1rem;padding-right:1rem}.px1{padding-left:.25rem;padding-right:.25rem}.py0\\.5{padding-top:.125rem;padding-bottom:.125rem}.text-lg{font-size:1.125rem;line-height:1.75rem}.text-sm{font-size:.875rem;line-height:1.25rem}.text-xl{font-size:1.25rem;line-height:1.75rem}.text-xs{font-size:.75rem;line-height:1rem}.text-green6{--un-text-opacity:1;color:rgba(22,163,74,var(--un-text-opacity))}.hover\\:text-green6:hover{--un-text-opacity:1;color:rgba(22,163,74,var(--un-text-opacity))}.font-semibold{font-weight:600}.font-mono{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace}.op0{opacity:0}.op100{opacity:1}.op50{opacity:.5}.hover\\:op100:hover{opacity:1}.disabled\\:op10\\!:disabled{opacity:.1!important}.shadow-lg{--un-shadow:var(--un-shadow-inset) 0 10px 15px -3px var(--un-shadow-color,rgba(0,0,0,.1)),var(--un-shadow-inset) 0 4px 6px -4px var(--un-shadow-color,rgba(0,0,0,.1));box-shadow:var(--un-ring-offset-shadow), var(--un-ring-shadow), var(--un-shadow)}.shadow-xl{--un-shadow:var(--un-shadow-inset) 0 20px 25px -5px var(--un-shadow-color,rgba(0,0,0,.1)),var(--un-shadow-inset) 0 8px 10px -6px var(--un-shadow-color,rgba(0,0,0,.1));box-shadow:var(--un-ring-offset-shadow), var(--un-ring-shadow), var(--un-shadow)}.ring-1{--un-ring-width:1px;--un-ring-offset-shadow:var(--un-ring-inset) 0 0 0 var(--un-ring-offset-width) var(--un-ring-offset-color);--un-ring-shadow:var(--un-ring-inset) 0 0 0 calc(var(--un-ring-width) + var(--un-ring-offset-width)) var(--un-ring-color);box-shadow:var(--un-ring-offset-shadow), var(--un-ring-shadow), var(--un-shadow)}.backdrop-blur{--un-backdrop-blur:blur(8px);backdrop-filter:var(--un-backdrop-blur) var(--un-backdrop-brightness) var(--un-backdrop-contrast) var(--un-backdrop-grayscale) var(--un-backdrop-hue-rotate) var(--un-backdrop-invert) var(--un-backdrop-opacity) var(--un-backdrop-saturate) var(--un-backdrop-sepia)}.transition-all{transition-property:all;transition-duration:.15s;transition-timing-function:cubic-bezier(.4,0,.2,1)}.transition-opacity{transition-property:opacity;transition-duration:.15s;transition-timing-function:cubic-bezier(.4,0,.2,1)}.duration-200{transition-duration:.2s}.duration-300{transition-duration:.3s}.transition-none{transition:none}`;

//#endregion
//#region tryOnScopeDispose/index.ts
/**
* Call onScopeDispose() if it's inside an effect scope lifecycle, if not, do nothing
*
* @param fn
*/
function tryOnScopeDispose(fn, failSilently) {
	if (getCurrentScope()) {
		onScopeDispose(fn, failSilently);
		return true;
	}
	return false;
}

//#endregion
//#region utils/is.ts
const isClient = typeof window !== "undefined" && typeof document !== "undefined";
typeof WorkerGlobalScope !== "undefined" && globalThis instanceof WorkerGlobalScope;
const notNullish = (val) => val != null;
const toString = Object.prototype.toString;
const isObject = (val) => toString.call(val) === "[object Object]";
const noop = () => {};

//#endregion
//#region utils/filters.ts
/**
* @internal
*/
function createFilterWrapper(filter, fn) {
	function wrapper(...args) {
		return new Promise((resolve, reject) => {
			Promise.resolve(filter(() => fn.apply(this, args), {
				fn,
				thisArg: this,
				args
			})).then(resolve).catch(reject);
		});
	}
	return wrapper;
}
/**
* Create an EventFilter that debounce the events
*/
function debounceFilter(ms, options = {}) {
	let timer;
	let maxTimer;
	let lastRejector = noop;
	const _clearTimeout = (timer$1) => {
		clearTimeout(timer$1);
		lastRejector();
		lastRejector = noop;
	};
	let lastInvoker;
	const filter = (invoke$1) => {
		const duration = toValue(ms);
		const maxDuration = toValue(options.maxWait);
		if (timer) _clearTimeout(timer);
		if (duration <= 0 || maxDuration !== void 0 && maxDuration <= 0) {
			if (maxTimer) {
				_clearTimeout(maxTimer);
				maxTimer = void 0;
			}
			return Promise.resolve(invoke$1());
		}
		return new Promise((resolve, reject) => {
			lastRejector = options.rejectOnCancel ? reject : resolve;
			lastInvoker = invoke$1;
			if (maxDuration && !maxTimer) maxTimer = setTimeout(() => {
				if (timer) _clearTimeout(timer);
				maxTimer = void 0;
				resolve(lastInvoker());
			}, maxDuration);
			timer = setTimeout(() => {
				if (maxTimer) _clearTimeout(maxTimer);
				maxTimer = void 0;
				resolve(invoke$1());
			}, duration);
		});
	};
	return filter;
}
function toArray(value) {
	return Array.isArray(value) ? value : [value];
}

//#endregion
//#region utils/vue.ts
function getLifeCycleTarget(target) {
	return getCurrentInstance();
}

//#endregion
//#region useDebounceFn/index.ts
/**
* Debounce execution of a function.
*
* @see https://vueuse.org/useDebounceFn
* @param  fn          A function to be executed after delay milliseconds debounced.
* @param  ms          A zero-or-greater delay in milliseconds. For event callbacks, values around 100 or 250 (or even higher) are most useful.
* @param  options     Options
*
* @return A new, debounce, function.
*
* @__NO_SIDE_EFFECTS__
*/
function useDebounceFn(fn, ms = 200, options = {}) {
	return createFilterWrapper(debounceFilter(ms, options), fn);
}

//#endregion
//#region toRefs/index.ts
/**
* Extended `toRefs` that also accepts refs of an object.
*
* @see https://vueuse.org/toRefs
* @param objectRef A ref or normal object or array.
* @param options Options
*/
function toRefs(objectRef, options = {}) {
	if (!isRef(objectRef)) return toRefs$1(objectRef);
	const result = Array.isArray(objectRef.value) ? Array.from({ length: objectRef.value.length }) : {};
	for (const key in objectRef.value) result[key] = customRef(() => ({
		get() {
			return objectRef.value[key];
		},
		set(v) {
			var _toValue;
			if ((_toValue = toValue(options.replaceRef)) !== null && _toValue !== void 0 ? _toValue : true) if (Array.isArray(objectRef.value)) {
				const copy = [...objectRef.value];
				copy[key] = v;
				objectRef.value = copy;
			} else {
				const newObject = {
					...objectRef.value,
					[key]: v
				};
				Object.setPrototypeOf(newObject, Object.getPrototypeOf(objectRef.value));
				objectRef.value = newObject;
			}
			else objectRef.value[key] = v;
		}
	}));
	return result;
}

//#endregion
//#region tryOnMounted/index.ts
/**
* Call onMounted() if it's inside a component lifecycle, if not, just call the function
*
* @param fn
* @param sync if set to false, it will run in the nextTick() of Vue
* @param target
*/
function tryOnMounted(fn, sync = true, target) {
	if (getLifeCycleTarget()) onMounted(fn, target);
	else if (sync) fn();
	else nextTick(fn);
}

//#endregion
//#region watchImmediate/index.ts
/**
* Shorthand for watching value with {immediate: true}
*
* @see https://vueuse.org/watchImmediate
*/
function watchImmediate(source, cb, options) {
	return watch(source, cb, {
		...options,
		immediate: true
	});
}

//#endregion
//#region _configurable.ts
const defaultWindow = isClient ? window : void 0;

//#endregion
//#region unrefElement/index.ts
/**
* Get the dom element of a ref of element or Vue component instance
*
* @param elRef
*/
function unrefElement(elRef) {
	var _$el;
	const plain = toValue(elRef);
	return (_$el = plain === null || plain === void 0 ? void 0 : plain.$el) !== null && _$el !== void 0 ? _$el : plain;
}

//#endregion
//#region useEventListener/index.ts
function useEventListener(...args) {
	const register = (el, event, listener, options) => {
		el.addEventListener(event, listener, options);
		return () => el.removeEventListener(event, listener, options);
	};
	const firstParamTargets = computed(() => {
		const test = toArray(toValue(args[0])).filter((e) => e != null);
		return test.every((e) => typeof e !== "string") ? test : void 0;
	});
	return watchImmediate(() => {
		var _firstParamTargets$va, _firstParamTargets$va2;
		return [
			(_firstParamTargets$va = (_firstParamTargets$va2 = firstParamTargets.value) === null || _firstParamTargets$va2 === void 0 ? void 0 : _firstParamTargets$va2.map((e) => unrefElement(e))) !== null && _firstParamTargets$va !== void 0 ? _firstParamTargets$va : [defaultWindow].filter((e) => e != null),
			toArray(toValue(firstParamTargets.value ? args[1] : args[0])),
			toArray(unref(firstParamTargets.value ? args[2] : args[1])),
			toValue(firstParamTargets.value ? args[3] : args[2])
		];
	}, ([raw_targets, raw_events, raw_listeners, raw_options], _, onCleanup) => {
		if (!(raw_targets === null || raw_targets === void 0 ? void 0 : raw_targets.length) || !(raw_events === null || raw_events === void 0 ? void 0 : raw_events.length) || !(raw_listeners === null || raw_listeners === void 0 ? void 0 : raw_listeners.length)) return;
		const optionsClone = isObject(raw_options) ? { ...raw_options } : raw_options;
		const cleanups = raw_targets.flatMap((el) => raw_events.flatMap((event) => raw_listeners.map((listener) => register(el, event, listener, optionsClone))));
		onCleanup(() => {
			cleanups.forEach((fn) => fn());
		});
	}, { flush: "post" });
}
function onClickOutside(target, handler, options = {}) {
	const { window: window$1 = defaultWindow, ignore = [], capture = true, detectIframe = false, controls = false } = options;
	if (!window$1) return controls ? {
		stop: noop,
		cancel: noop,
		trigger: noop
	} : noop;
	let shouldListen = true;
	const shouldIgnore = (event) => {
		return toValue(ignore).some((target$1) => {
			if (typeof target$1 === "string") return Array.from(window$1.document.querySelectorAll(target$1)).some((el) => el === event.target || event.composedPath().includes(el));
			else {
				const el = unrefElement(target$1);
				return el && (event.target === el || event.composedPath().includes(el));
			}
		});
	};
	/**
	* Determines if the given target has multiple root elements.
	* Referenced from: https://github.com/vuejs/test-utils/blob/ccb460be55f9f6be05ab708500a41ec8adf6f4bc/src/vue-wrapper.ts#L21
	*/
	function hasMultipleRoots(target$1) {
		const vm = toValue(target$1);
		return vm && vm.$.subTree.shapeFlag === 16;
	}
	function checkMultipleRoots(target$1, event) {
		const vm = toValue(target$1);
		const children = vm.$.subTree && vm.$.subTree.children;
		if (children == null || !Array.isArray(children)) return false;
		return children.some((child) => child.el === event.target || event.composedPath().includes(child.el));
	}
	const listener = (event) => {
		const el = unrefElement(target);
		if (event.target == null) return;
		if (!(el instanceof Element) && hasMultipleRoots(target) && checkMultipleRoots(target, event)) return;
		if (!el || el === event.target || event.composedPath().includes(el)) return;
		if ("detail" in event && event.detail === 0) shouldListen = !shouldIgnore(event);
		if (!shouldListen) {
			shouldListen = true;
			return;
		}
		handler(event);
	};
	let isProcessingClick = false;
	const cleanup = [
		useEventListener(window$1, "click", (event) => {
			if (!isProcessingClick) {
				isProcessingClick = true;
				setTimeout(() => {
					isProcessingClick = false;
				}, 0);
				listener(event);
			}
		}, {
			passive: true,
			capture
		}),
		useEventListener(window$1, "pointerdown", (e) => {
			const el = unrefElement(target);
			shouldListen = !shouldIgnore(e) && !!(el && !e.composedPath().includes(el));
		}, { passive: true }),
		detectIframe && useEventListener(window$1, "blur", (event) => {
			setTimeout(() => {
				var _window$document$acti;
				const el = unrefElement(target);
				if (((_window$document$acti = window$1.document.activeElement) === null || _window$document$acti === void 0 ? void 0 : _window$document$acti.tagName) === "IFRAME" && !(el === null || el === void 0 ? void 0 : el.contains(window$1.document.activeElement))) handler(event);
			}, 0);
		}, { passive: true })
	].filter(Boolean);
	const stop = () => cleanup.forEach((fn) => fn());
	if (controls) return {
		stop,
		cancel: () => {
			shouldListen = false;
		},
		trigger: (event) => {
			shouldListen = true;
			listener(event);
			shouldListen = false;
		}
	};
	return stop;
}

//#endregion
//#region useMounted/index.ts
/**
* Mounted state in ref.
*
* @see https://vueuse.org/useMounted
*
* @__NO_SIDE_EFFECTS__
*/
function useMounted() {
	const isMounted = shallowRef(false);
	const instance = getCurrentInstance();
	if (instance) onMounted(() => {
		isMounted.value = true;
	}, instance);
	return isMounted;
}

//#endregion
//#region useSupported/index.ts
/* @__NO_SIDE_EFFECTS__ */
function useSupported(callback) {
	const isMounted = useMounted();
	return computed(() => {
		isMounted.value;
		return Boolean(callback());
	});
}

//#endregion
//#region useMutationObserver/index.ts
/**
* Watch for changes being made to the DOM tree.
*
* @see https://vueuse.org/useMutationObserver
* @see https://developer.mozilla.org/en-US/docs/Web/API/MutationObserver MutationObserver MDN
* @param target
* @param callback
* @param options
*/
function useMutationObserver(target, callback, options = {}) {
	const { window: window$1 = defaultWindow,...mutationOptions } = options;
	let observer;
	const isSupported = /* @__PURE__ */ useSupported(() => window$1 && "MutationObserver" in window$1);
	const cleanup = () => {
		if (observer) {
			observer.disconnect();
			observer = void 0;
		}
	};
	const stopWatch = watch(computed(() => {
		const items = toArray(toValue(target)).map(unrefElement).filter(notNullish);
		return new Set(items);
	}), (newTargets) => {
		cleanup();
		if (isSupported.value && newTargets.size) {
			observer = new MutationObserver(callback);
			newTargets.forEach((el) => observer.observe(el, mutationOptions));
		}
	}, {
		immediate: true,
		flush: "post"
	});
	const takeRecords = () => {
		return observer === null || observer === void 0 ? void 0 : observer.takeRecords();
	};
	const stop = () => {
		stopWatch();
		cleanup();
	};
	tryOnScopeDispose(stop);
	return {
		isSupported,
		stop,
		takeRecords
	};
}

//#endregion
//#region useCssVar/index.ts
/**
* Manipulate CSS variables.
*
* @see https://vueuse.org/useCssVar
* @param prop
* @param target
* @param options
*/
function useCssVar(prop, target, options = {}) {
	const { window: window$1 = defaultWindow, initialValue, observe = false } = options;
	const variable = shallowRef(initialValue);
	const elRef = computed(() => {
		var _window$document;
		return unrefElement(target) || (window$1 === null || window$1 === void 0 || (_window$document = window$1.document) === null || _window$document === void 0 ? void 0 : _window$document.documentElement);
	});
	function updateCssVar() {
		const key = toValue(prop);
		const el = toValue(elRef);
		if (el && window$1 && key) {
			var _window$getComputedSt;
			variable.value = ((_window$getComputedSt = window$1.getComputedStyle(el).getPropertyValue(key)) === null || _window$getComputedSt === void 0 ? void 0 : _window$getComputedSt.trim()) || variable.value || initialValue;
		}
	}
	if (observe) useMutationObserver(elRef, updateCssVar, {
		attributeFilter: ["style", "class"],
		window: window$1
	});
	watch([elRef, () => toValue(prop)], (_, old) => {
		if (old[0] && old[1]) old[0].style.removeProperty(old[1]);
		updateCssVar();
	}, { immediate: true });
	watch([variable, elRef], ([val, el]) => {
		const raw_prop = toValue(prop);
		if ((el === null || el === void 0 ? void 0 : el.style) && raw_prop) if (val == null) el.style.removeProperty(raw_prop);
		else el.style.setProperty(raw_prop, val);
	}, { immediate: true });
	return variable;
}

//#endregion
//#region useDraggable/index.ts
const defaultScrollConfig = {
	speed: 2,
	margin: 30,
	direction: "both"
};
function clampContainerScroll(container) {
	if (container.scrollLeft > container.scrollWidth - container.clientWidth) container.scrollLeft = Math.max(0, container.scrollWidth - container.clientWidth);
	if (container.scrollTop > container.scrollHeight - container.clientHeight) container.scrollTop = Math.max(0, container.scrollHeight - container.clientHeight);
}
/**
* Make elements draggable.
*
* @see https://vueuse.org/useDraggable
* @param target
* @param options
*/
function useDraggable(target, options = {}) {
	var _toValue, _toValue2, _toValue3, _scrollConfig$directi;
	const { pointerTypes, preventDefault: preventDefault$1, stopPropagation, exact, onMove, onEnd, onStart, initialValue, axis = "both", draggingElement = defaultWindow, containerElement, handle: draggingHandle = target, buttons = [0], restrictInView, autoScroll = false } = options;
	const position = ref((_toValue = toValue(initialValue)) !== null && _toValue !== void 0 ? _toValue : {
		x: 0,
		y: 0
	});
	const pressedDelta = ref();
	const filterEvent = (e) => {
		if (pointerTypes) return pointerTypes.includes(e.pointerType);
		return true;
	};
	const handleEvent = (e) => {
		if (toValue(preventDefault$1)) e.preventDefault();
		if (toValue(stopPropagation)) e.stopPropagation();
	};
	const scrollConfig = toValue(autoScroll);
	const scrollSettings = typeof scrollConfig === "object" ? {
		speed: (_toValue2 = toValue(scrollConfig.speed)) !== null && _toValue2 !== void 0 ? _toValue2 : defaultScrollConfig.speed,
		margin: (_toValue3 = toValue(scrollConfig.margin)) !== null && _toValue3 !== void 0 ? _toValue3 : defaultScrollConfig.margin,
		direction: (_scrollConfig$directi = scrollConfig.direction) !== null && _scrollConfig$directi !== void 0 ? _scrollConfig$directi : defaultScrollConfig.direction
	} : defaultScrollConfig;
	const getScrollAxisValues = (value) => typeof value === "number" ? [value, value] : [value.x, value.y];
	const handleAutoScroll = (container, targetRect, position$1) => {
		const { clientWidth, clientHeight, scrollLeft, scrollTop, scrollWidth, scrollHeight } = container;
		const [marginX, marginY] = getScrollAxisValues(scrollSettings.margin);
		const [speedX, speedY] = getScrollAxisValues(scrollSettings.speed);
		let deltaX = 0;
		let deltaY = 0;
		if (scrollSettings.direction === "x" || scrollSettings.direction === "both") {
			if (position$1.x < marginX && scrollLeft > 0) deltaX = -speedX;
			else if (position$1.x + targetRect.width > clientWidth - marginX && scrollLeft < scrollWidth - clientWidth) deltaX = speedX;
		}
		if (scrollSettings.direction === "y" || scrollSettings.direction === "both") {
			if (position$1.y < marginY && scrollTop > 0) deltaY = -speedY;
			else if (position$1.y + targetRect.height > clientHeight - marginY && scrollTop < scrollHeight - clientHeight) deltaY = speedY;
		}
		if (deltaX || deltaY) container.scrollBy({
			left: deltaX,
			top: deltaY,
			behavior: "auto"
		});
	};
	let autoScrollInterval = null;
	const startAutoScroll = () => {
		const container = toValue(containerElement);
		if (container && !autoScrollInterval) autoScrollInterval = setInterval(() => {
			const targetRect = toValue(target).getBoundingClientRect();
			const { x, y } = position.value;
			const relativePosition = {
				x: x - container.scrollLeft,
				y: y - container.scrollTop
			};
			if (relativePosition.x >= 0 && relativePosition.y >= 0) {
				handleAutoScroll(container, targetRect, relativePosition);
				relativePosition.x += container.scrollLeft;
				relativePosition.y += container.scrollTop;
				position.value = relativePosition;
			}
		}, 1e3 / 60);
	};
	const stopAutoScroll = () => {
		if (autoScrollInterval) {
			clearInterval(autoScrollInterval);
			autoScrollInterval = null;
		}
	};
	const isPointerNearEdge = (pointer, container, margin, targetRect) => {
		const [marginX, marginY] = typeof margin === "number" ? [margin, margin] : [margin.x, margin.y];
		const { clientWidth, clientHeight } = container;
		return pointer.x < marginX || pointer.x + targetRect.width > clientWidth - marginX || pointer.y < marginY || pointer.y + targetRect.height > clientHeight - marginY;
	};
	const checkAutoScroll = () => {
		if (toValue(options.disabled) || !pressedDelta.value) return;
		const container = toValue(containerElement);
		if (!container) return;
		const targetRect = toValue(target).getBoundingClientRect();
		const { x, y } = position.value;
		if (isPointerNearEdge({
			x: x - container.scrollLeft,
			y: y - container.scrollTop
		}, container, scrollSettings.margin, targetRect)) startAutoScroll();
		else stopAutoScroll();
	};
	if (toValue(autoScroll)) watch(position, checkAutoScroll);
	const start = (e) => {
		var _container$getBoundin;
		if (!toValue(buttons).includes(e.button)) return;
		if (toValue(options.disabled) || !filterEvent(e)) return;
		if (toValue(exact) && e.target !== toValue(target)) return;
		const container = toValue(containerElement);
		const containerRect = container === null || container === void 0 || (_container$getBoundin = container.getBoundingClientRect) === null || _container$getBoundin === void 0 ? void 0 : _container$getBoundin.call(container);
		const targetRect = toValue(target).getBoundingClientRect();
		const pos = {
			x: e.clientX - (container ? targetRect.left - containerRect.left + (autoScroll ? 0 : container.scrollLeft) : targetRect.left),
			y: e.clientY - (container ? targetRect.top - containerRect.top + (autoScroll ? 0 : container.scrollTop) : targetRect.top)
		};
		if ((onStart === null || onStart === void 0 ? void 0 : onStart(pos, e)) === false) return;
		pressedDelta.value = pos;
		handleEvent(e);
	};
	const move = (e) => {
		if (toValue(options.disabled) || !filterEvent(e)) return;
		if (!pressedDelta.value) return;
		const container = toValue(containerElement);
		if (container instanceof HTMLElement) clampContainerScroll(container);
		const targetRect = toValue(target).getBoundingClientRect();
		let { x, y } = position.value;
		if (axis === "x" || axis === "both") {
			x = e.clientX - pressedDelta.value.x;
			if (container) x = Math.min(Math.max(0, x), container.scrollWidth - targetRect.width);
		}
		if (axis === "y" || axis === "both") {
			y = e.clientY - pressedDelta.value.y;
			if (container) y = Math.min(Math.max(0, y), container.scrollHeight - targetRect.height);
		}
		if (toValue(autoScroll) && container) {
			if (autoScrollInterval === null) handleAutoScroll(container, targetRect, {
				x,
				y
			});
			x += container.scrollLeft;
			y += container.scrollTop;
		}
		if (container && (restrictInView || autoScroll)) {
			if (axis !== "y") {
				const relativeX = x - container.scrollLeft;
				if (relativeX < 0) x = container.scrollLeft;
				else if (relativeX > container.clientWidth - targetRect.width) x = container.clientWidth - targetRect.width + container.scrollLeft;
			}
			if (axis !== "x") {
				const relativeY = y - container.scrollTop;
				if (relativeY < 0) y = container.scrollTop;
				else if (relativeY > container.clientHeight - targetRect.height) y = container.clientHeight - targetRect.height + container.scrollTop;
			}
		}
		position.value = {
			x,
			y
		};
		onMove === null || onMove === void 0 || onMove(position.value, e);
		handleEvent(e);
	};
	const end = (e) => {
		if (toValue(options.disabled) || !filterEvent(e)) return;
		if (!pressedDelta.value) return;
		pressedDelta.value = void 0;
		if (autoScroll) stopAutoScroll();
		onEnd === null || onEnd === void 0 || onEnd(position.value, e);
		handleEvent(e);
	};
	if (isClient) {
		const config = () => {
			var _options$capture;
			return {
				capture: (_options$capture = options.capture) !== null && _options$capture !== void 0 ? _options$capture : true,
				passive: !toValue(preventDefault$1)
			};
		};
		useEventListener(draggingHandle, "pointerdown", start, config);
		useEventListener(draggingElement, "pointermove", move, config);
		useEventListener(draggingElement, "pointerup", end, config);
	}
	return {
		...toRefs(position),
		position,
		isDragging: computed(() => !!pressedDelta.value),
		style: computed(() => `
      left: ${position.value.x}px;
      top: ${position.value.y}px;
      ${autoScroll ? "text-wrap: nowrap;" : ""}
    `)
	};
}

//#endregion
//#region useResizeObserver/index.ts
/**
* Reports changes to the dimensions of an Element's content or the border-box
*
* @see https://vueuse.org/useResizeObserver
* @param target
* @param callback
* @param options
*/
function useResizeObserver(target, callback, options = {}) {
	const { window: window$1 = defaultWindow,...observerOptions } = options;
	let observer;
	const isSupported = /* @__PURE__ */ useSupported(() => window$1 && "ResizeObserver" in window$1);
	const cleanup = () => {
		if (observer) {
			observer.disconnect();
			observer = void 0;
		}
	};
	const stopWatch = watch(computed(() => {
		const _targets = toValue(target);
		return Array.isArray(_targets) ? _targets.map((el) => unrefElement(el)) : [unrefElement(_targets)];
	}), (els) => {
		cleanup();
		if (isSupported.value && window$1) {
			observer = new ResizeObserver(callback);
			for (const _el of els) if (_el) observer.observe(_el, observerOptions);
		}
	}, {
		immediate: true,
		flush: "post"
	});
	const stop = () => {
		cleanup();
		stopWatch();
	};
	tryOnScopeDispose(stop);
	return {
		isSupported,
		stop
	};
}

//#endregion
//#region useElementBounding/index.ts
/**
* Reactive bounding box of an HTML element.
*
* @see https://vueuse.org/useElementBounding
* @param target
*/
function useElementBounding(target, options = {}) {
	const { reset = true, windowResize = true, windowScroll = true, immediate = true, updateTiming = "sync" } = options;
	const height = shallowRef(0);
	const bottom = shallowRef(0);
	const left = shallowRef(0);
	const right = shallowRef(0);
	const top = shallowRef(0);
	const width = shallowRef(0);
	const x = shallowRef(0);
	const y = shallowRef(0);
	function recalculate() {
		const el = unrefElement(target);
		if (!el) {
			if (reset) {
				height.value = 0;
				bottom.value = 0;
				left.value = 0;
				right.value = 0;
				top.value = 0;
				width.value = 0;
				x.value = 0;
				y.value = 0;
			}
			return;
		}
		const rect = el.getBoundingClientRect();
		height.value = rect.height;
		bottom.value = rect.bottom;
		left.value = rect.left;
		right.value = rect.right;
		top.value = rect.top;
		width.value = rect.width;
		x.value = rect.x;
		y.value = rect.y;
	}
	function update() {
		if (updateTiming === "sync") recalculate();
		else if (updateTiming === "next-frame") requestAnimationFrame(() => recalculate());
	}
	useResizeObserver(target, update);
	watch(() => unrefElement(target), (ele) => !ele && update());
	useMutationObserver(target, update, { attributeFilter: ["style", "class"] });
	if (windowScroll) useEventListener("scroll", update, {
		capture: true,
		passive: true
	});
	if (windowResize) useEventListener("resize", update, { passive: true });
	tryOnMounted(() => {
		if (immediate) update();
	});
	return {
		height,
		bottom,
		left,
		right,
		top,
		width,
		x,
		y,
		update
	};
}

//#endregion
//#region useScreenSafeArea/index.ts
const topVarName = "--vueuse-safe-area-top";
const rightVarName = "--vueuse-safe-area-right";
const bottomVarName = "--vueuse-safe-area-bottom";
const leftVarName = "--vueuse-safe-area-left";
/**
* Reactive `env(safe-area-inset-*)`
*
* @see https://vueuse.org/useScreenSafeArea
*/
function useScreenSafeArea() {
	const top = shallowRef("");
	const right = shallowRef("");
	const bottom = shallowRef("");
	const left = shallowRef("");
	if (isClient) {
		const topCssVar = useCssVar(topVarName);
		const rightCssVar = useCssVar(rightVarName);
		const bottomCssVar = useCssVar(bottomVarName);
		const leftCssVar = useCssVar(leftVarName);
		topCssVar.value = "env(safe-area-inset-top, 0px)";
		rightCssVar.value = "env(safe-area-inset-right, 0px)";
		bottomCssVar.value = "env(safe-area-inset-bottom, 0px)";
		leftCssVar.value = "env(safe-area-inset-left, 0px)";
		tryOnMounted(update);
		useEventListener("resize", useDebounceFn(update), { passive: true });
	}
	function update() {
		top.value = getValue(topVarName);
		right.value = getValue(rightVarName);
		bottom.value = getValue(bottomVarName);
		left.value = getValue(leftVarName);
	}
	return {
		top,
		right,
		bottom,
		left,
		update
	};
}
function getValue(position) {
	return getComputedStyle(document.documentElement).getPropertyValue(position);
}

const PANEL_MIN = 20;
const PANEL_MAX = 100;
const _sfc_main$2 = /* @__PURE__ */ defineComponent({
  __name: "NuxtDevtoolsFrameBox",
  props: /* @__PURE__ */ mergeModels({
    client: { type: Object, required: true },
    isDragging: { type: Boolean, required: true },
    state: { type: Object, required: true }
  }, {
    "popupWindow": { type: null },
    "popupWindowModifiers": {}
  }),
  emits: ["update:popupWindow"],
  setup(__props, { expose: __expose }) {
    __expose();
    const props = __props;
    const popupWindow = useModel(__props, "popupWindow");
    const {
      state
    } = toRefs(props);
    const container = ref();
    const isResizing = ref(false);
    watchEffect(() => {
      if (!container.value)
        return;
      if (state.value.open) {
        const iframe = props.client.getIframe();
        if (!iframe)
          return;
        iframe.style.pointerEvents = isResizing.value || props.isDragging || props.client.inspector?.isEnabled.value ? "none" : "auto";
        if (!popupWindow.value) {
          if ([...container.value.children].every((el) => el !== iframe))
            container.value.appendChild(iframe);
        }
      }
    });
    useEventListener(window, "keydown", (e) => {
      if (e.key === "Escape" && props.client.inspector?.isEnabled.value) {
        e.preventDefault();
        props.client.inspector?.disable();
        props.client.devtools.close();
      }
    });
    useEventListener(window, "mousedown", (e) => {
      if (!state.value.closeOnOutsideClick)
        return;
      if (popupWindow.value)
        return;
      if (!state.value.open || isResizing.value || props.client.inspector?.isEnabled.value)
        return;
      const matched = e.composedPath().find((_el) => {
        const el = _el;
        return [...el.classList || []].some((c) => c.startsWith("nuxt-devtools-")) || el.tagName?.toLowerCase() === "iframe";
      });
      if (!matched)
        state.value.open = false;
    });
    function handleResize(e) {
      if (!isResizing.value || !state.value.open)
        return;
      const iframe = props.client.getIframe();
      if (!iframe)
        return;
      const box = iframe.getBoundingClientRect();
      let widthPx, heightPx;
      if (isResizing.value.right) {
        widthPx = Math.abs(e instanceof MouseEvent ? e.clientX : (e.touches[0]?.clientX || 0) - (box?.left || 0));
        state.value.width = Math.min(PANEL_MAX, Math.max(PANEL_MIN, widthPx / window.innerWidth * 100));
      } else if (isResizing.value.left) {
        widthPx = Math.abs((box?.right || 0) - (e instanceof MouseEvent ? e.clientX : e.touches[0]?.clientX || 0));
        state.value.width = Math.min(PANEL_MAX, Math.max(PANEL_MIN, widthPx / window.innerWidth * 100));
      }
      if (isResizing.value.top) {
        heightPx = Math.abs((box?.bottom || 0) - (e instanceof MouseEvent ? e.clientY : e.touches[0]?.clientY || 0));
        state.value.height = Math.min(PANEL_MAX, Math.max(PANEL_MIN, heightPx / window.innerHeight * 100));
      } else if (isResizing.value.bottom) {
        heightPx = Math.abs(e instanceof MouseEvent ? e.clientY : (e.touches[0]?.clientY || 0) - (box?.top || 0));
        state.value.height = Math.min(PANEL_MAX, Math.max(PANEL_MIN, heightPx / window.innerHeight * 100));
      }
    }
    useEventListener(window, "mousemove", handleResize);
    useEventListener(window, "touchmove", handleResize);
    useEventListener(window, "mouseup", () => isResizing.value = false);
    useEventListener(window, "touchend", () => isResizing.value = false);
    useEventListener(window, "mouseleave", () => isResizing.value = false);
    const __returned__ = { props, PANEL_MIN, PANEL_MAX, popupWindow, state, container, isResizing, handleResize };
    Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
    return __returned__;
  }
});

const _export_sfc = (sfc, props) => {
  const target = sfc.__vccOpts || sfc;
  for (const [key, val] of props) {
    target[key] = val;
  }
  return target;
};

const _hoisted_1$2 = {
	ref: "container",
	class: "nuxt-devtools-frame"
};
function _sfc_render$2(_ctx, _cache, $props, $setup, $data, $options) {
	return withDirectives((openBlock(), createElementBlock(
		"div",
		_hoisted_1$2,
		[
			createCommentVNode(" Handlers "),
			withDirectives(createElementVNode(
				"div",
				{
					class: "nuxt-devtools-resize-handle nuxt-devtools-resize-handle-horizontal",
					style: { top: 0 },
					onMousedown: _cache[0] || (_cache[0] = withModifiers(($event) => $setup.isResizing = { top: true }, ["prevent"])),
					onTouchstartPassive: _cache[1] || (_cache[1] = () => $setup.isResizing = { top: true })
				},
				null,
				544
				/* NEED_HYDRATION, NEED_PATCH */
			), [[vShow, $setup.state.position !== "top"]]),
			withDirectives(createElementVNode(
				"div",
				{
					class: "nuxt-devtools-resize-handle nuxt-devtools-resize-handle-horizontal",
					style: { bottom: 0 },
					onMousedown: _cache[2] || (_cache[2] = withModifiers(() => $setup.isResizing = { bottom: true }, ["prevent"])),
					onTouchstartPassive: _cache[3] || (_cache[3] = () => $setup.isResizing = { bottom: true })
				},
				null,
				544
				/* NEED_HYDRATION, NEED_PATCH */
			), [[vShow, $setup.state.position !== "bottom"]]),
			withDirectives(createElementVNode(
				"div",
				{
					class: "nuxt-devtools-resize-handle nuxt-devtools-resize-handle-vertical",
					style: { left: 0 },
					onMousedown: _cache[4] || (_cache[4] = withModifiers(() => $setup.isResizing = { left: true }, ["prevent"])),
					onTouchstartPassive: _cache[5] || (_cache[5] = () => $setup.isResizing = { left: true })
				},
				null,
				544
				/* NEED_HYDRATION, NEED_PATCH */
			), [[vShow, $setup.state.position !== "left"]]),
			withDirectives(createElementVNode(
				"div",
				{
					class: "nuxt-devtools-resize-handle nuxt-devtools-resize-handle-vertical",
					style: { right: 0 },
					onMousedown: _cache[6] || (_cache[6] = withModifiers(() => $setup.isResizing = { right: true }, ["prevent"])),
					onTouchstartPassive: _cache[7] || (_cache[7] = () => $setup.isResizing = { right: true })
				},
				null,
				544
				/* NEED_HYDRATION, NEED_PATCH */
			), [[vShow, $setup.state.position !== "right"]]),
			withDirectives(createElementVNode(
				"div",
				{
					class: "nuxt-devtools-resize-handle nuxt-devtools-resize-handle-corner",
					style: {
						top: 0,
						left: 0,
						cursor: "nwse-resize"
					},
					onMousedown: _cache[8] || (_cache[8] = withModifiers(() => $setup.isResizing = {
						top: true,
						left: true
					}, ["prevent"])),
					onTouchstartPassive: _cache[9] || (_cache[9] = () => $setup.isResizing = {
						top: true,
						left: true
					})
				},
				null,
				544
				/* NEED_HYDRATION, NEED_PATCH */
			), [[vShow, $setup.state.position !== "top" && $setup.state.position !== "left"]]),
			withDirectives(createElementVNode(
				"div",
				{
					class: "nuxt-devtools-resize-handle nuxt-devtools-resize-handle-corner",
					style: {
						top: 0,
						right: 0,
						cursor: "nesw-resize"
					},
					onMousedown: _cache[10] || (_cache[10] = withModifiers(() => $setup.isResizing = {
						top: true,
						right: true
					}, ["prevent"])),
					onTouchstartPassive: _cache[11] || (_cache[11] = () => $setup.isResizing = {
						top: true,
						right: true
					})
				},
				null,
				544
				/* NEED_HYDRATION, NEED_PATCH */
			), [[vShow, $setup.state.position !== "top" && $setup.state.position !== "right"]]),
			withDirectives(createElementVNode(
				"div",
				{
					class: "nuxt-devtools-resize-handle nuxt-devtools-resize-handle-corner",
					style: {
						bottom: 0,
						left: 0,
						cursor: "nesw-resize"
					},
					onMousedown: _cache[12] || (_cache[12] = withModifiers(() => $setup.isResizing = {
						bottom: true,
						left: true
					}, ["prevent"])),
					onTouchstartPassive: _cache[13] || (_cache[13] = () => $setup.isResizing = {
						bottom: true,
						left: true
					})
				},
				null,
				544
				/* NEED_HYDRATION, NEED_PATCH */
			), [[vShow, $setup.state.position !== "bottom" && $setup.state.position !== "left"]]),
			withDirectives(createElementVNode(
				"div",
				{
					class: "nuxt-devtools-resize-handle nuxt-devtools-resize-handle-corner",
					style: {
						bottom: 0,
						right: 0,
						cursor: "nwse-resize"
					},
					onMousedown: _cache[14] || (_cache[14] = withModifiers(() => $setup.isResizing = {
						bottom: true,
						right: true
					}, ["prevent"])),
					onTouchstartPassive: _cache[15] || (_cache[15] = () => $setup.isResizing = {
						bottom: true,
						right: true
					})
				},
				null,
				544
				/* NEED_HYDRATION, NEED_PATCH */
			), [[vShow, $setup.state.position !== "bottom" && $setup.state.position !== "right"]])
		],
		512
		/* NEED_PATCH */
	)), [[vShow, $setup.state.open && !$props.client.inspector?.isEnabled.value && !$setup.popupWindow]]);
}
const FrameBox = /* @__PURE__ */ _export_sfc(_sfc_main$2, [["render", _sfc_render$2], ["__file", "/home/runner/work/devtools/devtools/packages/devtools/src/webcomponents/components/NuxtDevtoolsFrameBox.vue"]]);

const SNAP_THRESHOLD = 2;
const _sfc_main$1 = /* @__PURE__ */ defineComponent({
  __name: "NuxtDevtoolsFrame",
  props: {
    client: { type: Object, required: true },
    settings: { type: Object, required: true },
    state: { type: Object, required: true }
  },
  setup(__props, { expose: __expose }) {
    __expose();
    const props = __props;
    const {
      state,
      settings
    } = toRefs(props);
    function millisecondToHumanreadable(ms) {
      if (ms < 1e3)
        return [+ms.toFixed(0), "ms"];
      if (ms < 1e3 * 60)
        return [+(ms / 1e3).toFixed(1), "s"];
      if (ms < 1e3 * 60 * 60)
        return [+(ms / 1e3 / 60).toFixed(1), "min"];
      return [+(ms / 1e3 / 60 / 60).toFixed(1), "hour"];
    }
    const panelMargins = reactive({
      left: 10,
      top: 10,
      right: 10,
      bottom: 10
    });
    const safeArea = useScreenSafeArea();
    const isSafari = navigator.userAgent.includes("Safari") && !navigator.userAgent.includes("Chrome");
    function toNumber(value) {
      const num = +value;
      if (Number.isNaN(num))
        return 0;
      return num;
    }
    watchEffect(() => {
      panelMargins.left = toNumber(safeArea.left.value) + 10;
      panelMargins.top = toNumber(safeArea.top.value) + 10;
      panelMargins.right = toNumber(safeArea.right.value) + 10;
      panelMargins.bottom = toNumber(safeArea.bottom.value) + 10;
    });
    const vars = computed(() => {
      const dark = props.client.app.colorMode.value === "dark";
      return {
        "--nuxt-devtools-widget-bg": dark ? "#111" : "#ffffff",
        "--nuxt-devtools-widget-fg": dark ? "#F5F5F5" : "#111",
        "--nuxt-devtools-widget-border": dark ? "#3336" : "#efefef",
        "--nuxt-devtools-widget-shadow": dark ? "rgba(0,0,0,0.3)" : "rgba(128,128,128,0.1)"
      };
    });
    const frameBox = useTemplateRef("frameBox");
    const panelEl = useTemplateRef("panelEl");
    const anchorEl = useTemplateRef("anchorEl");
    const windowSize = reactive({
      width: window.innerWidth,
      height: window.innerHeight
    });
    const isDragging = ref(false);
    const draggingOffset = reactive({ x: 0, y: 0 });
    const mousePosition = reactive({ x: 0, y: 0 });
    function onPointerDown(e) {
      if (!panelEl.value)
        return;
      isDragging.value = true;
      const { left, top, width, height } = panelEl.value.getBoundingClientRect();
      draggingOffset.x = e.clientX - left - width / 2;
      draggingOffset.y = e.clientY - top - height / 2;
    }
    onMounted(() => {
      windowSize.width = window.innerWidth;
      windowSize.height = window.innerHeight;
      useEventListener(window, "resize", () => {
        windowSize.width = window.innerWidth;
        windowSize.height = window.innerHeight;
      });
      useEventListener(window, "pointermove", (e) => {
        if (!isDragging.value)
          return;
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        const x = e.clientX - draggingOffset.x;
        const y = e.clientY - draggingOffset.y;
        if (Number.isNaN(x) || Number.isNaN(y))
          return;
        mousePosition.x = x;
        mousePosition.y = y;
        const deg = Math.atan2(y - centerY, x - centerX);
        const HORIZONTAL_MARGIN = 70;
        const TL = Math.atan2(0 - centerY + HORIZONTAL_MARGIN, 0 - centerX);
        const TR = Math.atan2(0 - centerY + HORIZONTAL_MARGIN, window.innerWidth - centerX);
        const BL = Math.atan2(window.innerHeight - HORIZONTAL_MARGIN - centerY, 0 - centerX);
        const BR = Math.atan2(window.innerHeight - HORIZONTAL_MARGIN - centerY, window.innerWidth - centerX);
        state.value.position = deg >= TL && deg <= TR ? "top" : deg >= TR && deg <= BR ? "right" : deg >= BR && deg <= BL ? "bottom" : "left";
        state.value.left = snapToPoints(x / window.innerWidth * 100);
        state.value.top = snapToPoints(y / window.innerHeight * 100);
      });
      useEventListener(window, "pointerup", () => {
        isDragging.value = false;
      });
      useEventListener(window, "pointerleave", () => {
        isDragging.value = false;
      });
    });
    function snapToPoints(value) {
      if (value < 5)
        return 0;
      if (value > 95)
        return 100;
      if (Math.abs(value - 50) < SNAP_THRESHOLD)
        return 50;
      return value;
    }
    function clamp(value, min, max) {
      return Math.min(Math.max(value, min), max);
    }
    const isHovering = ref(false);
    const isVertical = computed(() => state.value.position === "left" || state.value.position === "right");
    const anchorPos = computed(() => {
      const halfWidth = (panelEl.value?.clientWidth || 0) / 2;
      const halfHeight = (panelEl.value?.clientHeight || 0) / 2;
      const left = state.value.left * windowSize.width / 100;
      const top = state.value.top * windowSize.height / 100;
      switch (state.value.position) {
        case "top":
          return {
            left: clamp(left, halfWidth + panelMargins.left, windowSize.width - halfWidth - panelMargins.right),
            top: panelMargins.top + halfHeight
          };
        case "right":
          return {
            left: windowSize.width - panelMargins.right - halfHeight,
            top: clamp(top, halfWidth + panelMargins.top, windowSize.height - halfWidth - panelMargins.bottom)
          };
        case "left":
          return {
            left: panelMargins.left + halfHeight,
            top: clamp(top, halfWidth + panelMargins.top, windowSize.height - halfWidth - panelMargins.bottom)
          };
        case "bottom":
        default:
          return {
            left: clamp(left, halfWidth + panelMargins.left, windowSize.width - halfWidth - panelMargins.right),
            top: windowSize.height - panelMargins.bottom - halfHeight
          };
      }
    });
    let _timer = null;
    function bringUp() {
      isHovering.value = true;
      if (state.value.minimizePanelInactive < 0)
        return;
      if (_timer)
        clearTimeout(_timer);
      _timer = setTimeout(() => {
        isHovering.value = false;
      }, +state.value.minimizePanelInactive || 0);
    }
    const isHidden = computed(() => {
      if (state.value.open)
        return false;
      if (settings.value.ui.showPanel === true)
        return false;
      if (settings.value.ui.showPanel === false)
        return true;
      return false;
    });
    const isMinimized = computed(() => {
      if (state.value.minimizePanelInactive < 0)
        return false;
      if (state.value.minimizePanelInactive === 0)
        return true;
      const isTouchDevice = "ontouchstart" in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0;
      return !isDragging.value && !state.value.open && !isHovering.value && !isTouchDevice && state.value.minimizePanelInactive;
    });
    const anchorStyle = computed(() => {
      return {
        left: `${anchorPos.value.left}px`,
        top: `${anchorPos.value.top}px`,
        pointerEvents: isHidden.value ? "none" : "auto"
      };
    });
    const panelStyle = computed(() => {
      const style = {
        transform: isVertical.value ? `translate(${isMinimized.value ? `calc(-50% ${state.value.position === "right" ? "+" : "-"} 15px)` : "-50%"}, -50%) rotate(90deg)` : `translate(-50%, ${isMinimized.value ? `calc(-50% ${state.value.position === "top" ? "-" : "+"} 15px)` : "-50%"})`
      };
      if (isHidden.value) {
        style.opacity = 0;
        style.pointerEvents = "none";
      }
      if (isMinimized.value) {
        switch (state.value.position) {
          case "top":
          case "right":
            style.borderTopLeftRadius = "0";
            style.borderTopRightRadius = "0";
            break;
          case "bottom":
          case "left":
            style.borderBottomLeftRadius = "0";
            style.borderBottomRightRadius = "0";
            break;
        }
      }
      if (isDragging.value)
        style.transition = "none !important";
      return style;
    });
    const { width: frameWidth, height: frameHeight } = useElementBounding(frameBox);
    const popupWindow = ref(null);
    const iframeStyle = computed(() => {
      mousePosition.x, mousePosition.y;
      const halfHeight = (panelEl.value?.clientHeight || 0) / 2;
      const frameMargin = {
        left: panelMargins.left + halfHeight,
        top: panelMargins.top + halfHeight,
        right: panelMargins.right + halfHeight,
        bottom: panelMargins.bottom + halfHeight
      };
      const marginHorizontal = frameMargin.left + frameMargin.right;
      const marginVertical = frameMargin.top + frameMargin.bottom;
      const maxWidth = windowSize.width - marginHorizontal;
      const maxHeight = windowSize.height - marginVertical;
      const style = {
        position: "fixed",
        zIndex: -1,
        pointerEvents: isDragging.value || !state.value.open || props.client.inspector?.isEnabled.value ? "none" : "auto",
        width: `min(${state.value.width}vw, calc(100vw - ${marginHorizontal}px))`,
        height: `min(${state.value.height}vh, calc(100vh - ${marginVertical}px))`
      };
      const anchor = anchorPos.value;
      const width = Math.min(maxWidth, state.value.width * windowSize.width / 100);
      const height = Math.min(maxHeight, state.value.height * windowSize.height / 100);
      const anchorX = anchor?.left || 0;
      const anchorY = anchor?.top || 0;
      switch (state.value.position) {
        case "top":
        case "bottom":
          style.left = `${-frameWidth.value / 2}px`;
          style.transform = "translate(0, 0)";
          if (anchorX - frameMargin.left < width / 2)
            style.left = `${width / 2 - anchorX + frameMargin.left - frameWidth.value / 2}px`;
          else if (windowSize.width - anchorX - frameMargin.right < width / 2)
            style.left = `${windowSize.width - anchorX - width / 2 - frameMargin.right - frameWidth.value / 2}px`;
          break;
        case "right":
        case "left":
          style.top = `${-frameHeight.value / 2}px`;
          style.transform = "translate(0, 0)";
          if (anchorY - frameMargin.top < height / 2)
            style.top = `${height / 2 - anchorY + frameMargin.top - frameHeight.value / 2}px`;
          else if (windowSize.height - anchorY - frameMargin.bottom < height / 2)
            style.top = `${windowSize.height - anchorY - height / 2 - frameMargin.bottom - frameHeight.value / 2}px`;
          break;
      }
      switch (state.value.position) {
        case "top":
          style.top = 0;
          break;
        case "right":
          style.right = 0;
          break;
        case "left":
          style.left = 0;
          break;
        case "bottom":
        default:
          style.bottom = 0;
          break;
      }
      if (props.client.inspector?.isEnabled.value) {
        style.opacity = 0;
      }
      return style;
    });
    const time = computed(() => {
      let type = "";
      const metric = props.client.metrics.loading();
      let time2 = -1;
      if (metric.pageEnd && metric.pageStart) {
        time2 = metric.pageEnd - metric.pageStart;
        type = "Page";
      } else if (metric.appLoad && metric.appInit) {
        time2 = metric.appLoad - metric.appInit;
        type = "App";
      }
      bringUp();
      if (time2 < 0)
        return [type, "", "-"];
      return [type, ...millisecondToHumanreadable(time2)];
    });
    function toggleInspector() {
      const isDevToolsOpen = state.value.open;
      if (!isDevToolsOpen)
        props.client.devtools.open();
      props.client.inspector?.enable();
      if (!isDevToolsOpen) {
        setTimeout(() => {
          props.client.devtools.close();
        }, 500);
      }
    }
    onMounted(() => {
      bringUp();
    });
    const __returned__ = { props, state, settings, millisecondToHumanreadable, panelMargins, safeArea, isSafari, toNumber, SNAP_THRESHOLD, vars, frameBox, panelEl, anchorEl, windowSize, isDragging, draggingOffset, mousePosition, onPointerDown, snapToPoints, clamp, isHovering, isVertical, anchorPos, get _timer() {
      return _timer;
    }, set _timer(v) {
      _timer = v;
    }, bringUp, isHidden, isMinimized, anchorStyle, panelStyle, frameWidth, frameHeight, popupWindow, iframeStyle, time, toggleInspector, FrameBox };
    Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
    return __returned__;
  }
});

const _hoisted_1$1 = {
	viewBox: "0 0 324 324",
	fill: "none",
	xmlns: "http://www.w3.org/2000/svg",
	style: {
		"margin-top": "-1px",
		"height": "1.2em",
		"width": "1.2em"
	}
};
const _hoisted_2$1 = ["title"];
const _hoisted_3$1 = { class: "nuxt-devtools-label-main" };
const _hoisted_4$1 = { class: "nuxt-devtools-label-secondary" };
function _sfc_render$1(_ctx, _cache, $props, $setup, $data, $options) {
	return openBlock(), createElementBlock(
		"div",
		{
			id: "nuxt-devtools-anchor",
			ref: "anchorEl",
			style: normalizeStyle([$setup.anchorStyle, $setup.vars]),
			class: normalizeClass({
				"nuxt-devtools-vertical": $setup.isVertical,
				"nuxt-devtools-hide": $setup.isMinimized
			}),
			onMousemove: $setup.bringUp
		},
		[
			!$setup.isSafari ? (openBlock(), createElementBlock(
				"div",
				{
					key: 0,
					class: "nuxt-devtools-glowing",
					style: normalizeStyle($setup.isDragging ? "opacity: 0.6 !important" : "")
				},
				null,
				4
				/* STYLE */
			)) : createCommentVNode("v-if", true),
			createElementVNode(
				"div",
				{
					ref: "panelEl",
					class: "nuxt-devtools-panel",
					style: normalizeStyle($setup.panelStyle),
					onPointerdown: $setup.onPointerDown
				},
				[
					createElementVNode(
						"button",
						{
							class: "nuxt-devtools-icon-button nuxt-devtools-nuxt-button",
							title: "Toggle Nuxt DevTools",
							style: normalizeStyle($setup.state.open ? "" : "filter:saturate(0)"),
							onClick: _cache[0] || (_cache[0] = ($event) => $props.client.devtools.toggle())
						},
						[(openBlock(), createElementBlock("svg", _hoisted_1$1, [..._cache[2] || (_cache[2] = [createElementVNode(
							"path",
							{
								d: "M181.767 270H302.211C306.037 270 309.795 269.003 313.108 267.107C316.421 265.211 319.172 262.484 321.084 259.2C322.996 255.915 324.002 252.19 324 248.399C323.998 244.607 322.989 240.883 321.074 237.601L240.187 98.7439C238.275 95.4607 235.525 92.7342 232.213 90.8385C228.901 88.9429 225.143 87.9449 221.318 87.9449C217.494 87.9449 213.736 88.9429 210.424 90.8385C207.112 92.7342 204.361 95.4607 202.449 98.7439L181.767 134.272L141.329 64.7975C139.416 61.5145 136.664 58.7884 133.351 56.8931C130.038 54.9978 126.28 54 122.454 54C118.629 54 114.871 54.9978 111.558 56.8931C108.245 58.7884 105.493 61.5145 103.58 64.7975L2.92554 237.601C1.01067 240.883 0.00166657 244.607 2.06272e-06 248.399C-0.00166244 252.19 1.00407 255.915 2.91605 259.2C4.82803 262.484 7.57884 265.211 10.8918 267.107C14.2047 269.003 17.963 270 21.7886 270H97.3936C127.349 270 149.44 256.959 164.641 231.517L201.546 168.172L221.313 134.272L280.637 236.1H201.546L181.767 270ZM96.1611 236.065L43.3984 236.054L122.49 100.291L161.953 168.172L135.531 213.543C125.436 230.051 113.968 236.065 96.1611 236.065Z",
								fill: "#00DC82"
							},
							null,
							-1
							/* CACHED */
						)])]))],
						4
						/* STYLE */
					),
					_cache[5] || (_cache[5] = createElementVNode(
						"div",
						{
							style: {
								"border-left": "1px solid #8883",
								"width": "1px",
								"height": "10px"
							},
							class: "nuxt-devtools-panel-content"
						},
						null,
						-1
						/* CACHED */
					)),
					createElementVNode("div", {
						class: "nuxt-devtools-panel-content nuxt-devtools-label",
						title: `${$setup.time[0]} load time`
					}, [createElementVNode(
						"div",
						_hoisted_3$1,
						toDisplayString($setup.time[1]),
						1
						/* TEXT */
					), createElementVNode(
						"span",
						_hoisted_4$1,
						toDisplayString($setup.time[2]),
						1
						/* TEXT */
					)], 8, _hoisted_2$1),
					$props.client.inspector?.isAvailable ? (openBlock(), createElementBlock(
						Fragment,
						{ key: 0 },
						[_cache[4] || (_cache[4] = createElementVNode(
							"div",
							{
								style: {
									"border-left": "1px solid #8883",
									"width": "1px",
									"height": "10px"
								},
								class: "nuxt-devtools-panel-content"
							},
							null,
							-1
							/* CACHED */
						)), createElementVNode("button", {
							class: "nuxt-devtools-icon-button nuxt-devtools-panel-content",
							title: "Toggle Component Inspector",
							onClick: withModifiers($setup.toggleInspector, ["prevent", "stop"])
						}, [(openBlock(), createElementBlock(
							"svg",
							{
								xmlns: "http://www.w3.org/2000/svg",
								style: normalizeStyle([{
									"height": "1.2em",
									"width": "1.2em",
									"opacity": "0.5"
								}, $props.client.inspector.isEnabled.value ? "opacity:1;color:#00dc82" : ""]),
								viewBox: "0 0 24 24"
							},
							[..._cache[3] || (_cache[3] = [createElementVNode(
								"g",
								{
									fill: "none",
									stroke: "currentColor",
									"stroke-linecap": "round",
									"stroke-linejoin": "round",
									"stroke-width": "2"
								},
								[createElementVNode("circle", {
									cx: "12",
									cy: "12",
									r: ".5",
									fill: "currentColor"
								}), createElementVNode("path", { d: "M5 12a7 7 0 1 0 14 0a7 7 0 1 0-14 0m7-9v2m-9 7h2m7 7v2m7-9h2" })],
								-1
								/* CACHED */
							)])],
							4
							/* STYLE */
						))])],
						64
						/* STABLE_FRAGMENT */
					)) : createCommentVNode("v-if", true)
				],
				36
				/* STYLE, NEED_HYDRATION */
			),
			createElementVNode(
				"div",
				{
					ref: "frameBox",
					style: normalizeStyle($setup.iframeStyle)
				},
				[createVNode($setup["FrameBox"], {
					"popup-window": $setup.popupWindow,
					"onUpdate:popupWindow": _cache[1] || (_cache[1] = ($event) => $setup.popupWindow = $event),
					state: $setup.state,
					client: $props.client,
					"is-dragging": $setup.isDragging
				}, null, 8, [
					"popup-window",
					"state",
					"client",
					"is-dragging"
				])],
				4
				/* STYLE */
			)
		],
		38
		/* CLASS, STYLE, NEED_HYDRATION */
	);
}
const Component$1 = /* @__PURE__ */ _export_sfc(_sfc_main$1, [["render", _sfc_render$1], ["__file", "/home/runner/work/devtools/devtools/packages/devtools/src/webcomponents/components/NuxtDevtoolsFrame.vue"]]);

const NuxtDevtoolsFrame = defineCustomElement(
  Component$1,
  {
    shadowRoot: true,
    styles: [css]
  }
);
customElements.define("nuxt-devtools-frame", NuxtDevtoolsFrame);

const PANEL_WIDTH = 400;
const PANEL_HEIGHT = 300;
const PANEL_MARGIN = 30;
const _sfc_main = /* @__PURE__ */ defineComponent({
  ...{
    inheritAttrs: false
  },
  __name: "NuxtDevtoolsInspectPanel",
  props: {
    props: { type: Object, required: true }
  },
  emits: ["close", "selectParent", "openInEditor"],
  setup(__props, { expose: __expose, emit: __emit }) {
    __expose();
    const emit = __emit;
    const WHITESPACE_RE = /\s+/;
    const FILE_EXT_RE = /\.\w+$/;
    const showToast = ref(false);
    const toastContent = ref("");
    let toastTimer;
    const initX = ref(0);
    const initY = ref(0);
    const el = useTemplateRef("el");
    const draggingEl = useTemplateRef("draggingEl");
    const { x, y, style: panelStyle, isDragging } = useDraggable(el, {
      initialValue: {
        x: initX.value,
        y: initY.value
      },
      preventDefault: true,
      stopPropagation: true,
      handle: draggingEl
    });
    const rect = computed(() => __props.props.matched?.rect || __props.props.matched?.el?.getBoundingClientRect());
    watch(
      () => rect.value,
      (rect2) => {
        if (!rect2)
          return;
        const preferredX = rect2.left;
        const preferredY = rect2.bottom + PANEL_MARGIN / 2;
        const fitsBelow = preferredY + PANEL_HEIGHT + PANEL_MARGIN < window.innerHeight;
        initX.value = Math.max(PANEL_MARGIN, Math.min(preferredX, window.innerWidth - PANEL_WIDTH - PANEL_MARGIN));
        initY.value = fitsBelow ? Math.max(PANEL_MARGIN, preferredY) : Math.max(PANEL_MARGIN, rect2.top - PANEL_HEIGHT - PANEL_MARGIN / 2);
        x.value = initX.value;
        y.value = initY.value;
      }
    );
    const hasMoved = computed(() => x.value !== initX.value || y.value !== initY.value);
    onClickOutside(el, () => {
      nextTick(() => {
        if (!__props.props.matched)
          return;
        if (hasMoved.value)
          return;
        close();
      });
    });
    function close() {
      emit("close");
    }
    async function selectParent() {
      emit("selectParent");
    }
    async function openInEditor() {
      if (!__props.props.matched)
        return;
      const file = `${__props.props.matched.pos[0]}:${__props.props.matched.pos[1]}:${__props.props.matched.pos[2]}`;
      emit("openInEditor", file);
    }
    function generateUniqueSelector(element) {
      if (!element)
        return "";
      const path = [];
      let current = element;
      while (current && current !== document.body) {
        let selector = current.tagName.toLowerCase();
        if (current.id) {
          selector += `#${CSS.escape(current.id)}`;
          path.unshift(selector);
          break;
        }
        if (current.className && typeof current.className === "string") {
          const classes = current.className.trim().split(WHITESPACE_RE).filter(Boolean);
          if (classes.length > 0)
            selector += `.${classes.map((c) => CSS.escape(c)).join(".")}`;
        }
        const parent = current.parentElement;
        if (parent) {
          const siblings = [...parent.children].filter(
            (child) => child.tagName === current.tagName
          );
          if (siblings.length > 1) {
            const index = siblings.indexOf(current) + 1;
            selector += `:nth-of-type(${index})`;
          }
        }
        path.unshift(selector);
        current = current.parentElement;
      }
      if (path.length > 6)
        return "";
      return path.join(" > ");
    }
    function buildComponentTree() {
      if (!__props.props.matched)
        return "";
      const components = [];
      let current = __props.props.matched;
      while (current) {
        let componentName = "Unknown";
        if (current.vnode) {
          const vnode = current.vnode;
          if (vnode.type) {
            if (typeof vnode.type === "string") {
              componentName = vnode.type;
            } else if (typeof vnode.type === "object") {
              const typeObj = vnode.type;
              componentName = typeObj.name || typeObj.__name || typeObj.__file?.split("/").pop()?.replace(FILE_EXT_RE, "") || "AnonymousComponent";
            } else if (typeof vnode.type === "function") {
              componentName = vnode.type.name || "FunctionalComponent";
            }
          }
        }
        components.unshift(componentName);
        try {
          current = current.getParent();
        } catch {
          break;
        }
      }
      return components.join(" > ");
    }
    async function copyAgentInfo() {
      if (!rect.value || !__props.props.matched)
        return;
      try {
        const pageUrl = window.location.href;
        const viewport = `${window.innerWidth}x${window.innerHeight}`;
        const selectedText = window.getSelection()?.toString()?.trim();
        const filepath = __props.props.matched.pos[0];
        const line = __props.props.matched.pos[1];
        const column = __props.props.matched.pos[2];
        const fileLocation = `${filepath}:${line}:${column}`;
        const selector = generateUniqueSelector(__props.props.matched.el);
        const componentTree = buildComponentTree();
        const info = [
          `Page URL: ${pageUrl}`,
          `Viewport: ${viewport}`,
          selectedText ? `Selected Text: ${selectedText}` : null,
          selector ? `Selector: ${selector}` : null,
          componentTree ? `Component Tree: ${componentTree}` : null,
          `File: ${fileLocation}`
        ].filter(Boolean).join("\n");
        await navigator.clipboard.writeText(info);
        toastContent.value = info;
        showToast.value = true;
        if (toastTimer)
          clearTimeout(toastTimer);
        toastTimer = setTimeout(() => {
          showToast.value = false;
        }, 6e3);
      } catch (error) {
        console.error("Failed to copy agent info:", error);
      }
    }
    const __returned__ = { emit, WHITESPACE_RE, FILE_EXT_RE, PANEL_WIDTH, PANEL_HEIGHT, PANEL_MARGIN, showToast, toastContent, get toastTimer() {
      return toastTimer;
    }, set toastTimer(v) {
      toastTimer = v;
    }, initX, initY, el, draggingEl, x, y, panelStyle, isDragging, rect, hasMoved, close, selectParent, openInEditor, generateUniqueSelector, buildComponentTree, copyAgentInfo };
    Object.defineProperty(__returned__, "__isScriptSetup", { enumerable: false, value: true });
    return __returned__;
  }
});

const _hoisted_1 = {
	ref: "draggingEl",
	class: "flex flex-col gap-2 of-hidden p2"
};
const _hoisted_2 = { class: "flex items-center gap-2" };
const _hoisted_3 = { class: "grid grid-cols-[max-content_1fr] items-center gap-2" };
const _hoisted_4 = {
	class: "break-all text-xs font-mono",
	title: "File location"
};
const _hoisted_5 = {
	class: "break-all text-xs font-mono",
	title: "Component Tree"
};
const _hoisted_6 = { class: "mt-2 max-h-200px of-auto whitespace-pre-wrap rounded bg-black bg-op-20 p2 text-xs font-mono" };
function _sfc_render(_ctx, _cache, $props, $setup, $data, $options) {
	return openBlock(), createElementBlock(
		Fragment,
		null,
		[
			$setup.rect && $props.props.matched ? (openBlock(), createElementBlock(
				"div",
				{
					key: 0,
					ref: "el",
					class: normalizeClass(["fixed relative z-9999999 w-400px flex flex-col of-hidden rounded-lg bg-glass text-sm color-base shadow-lg ring-1 ring-base backdrop-blur duration-200", [$setup.isDragging ? "transition-none" : "transition-opacity", $props.props.matched ? "op100" : "op0 pointer-events-none"]]),
					style: normalizeStyle($setup.panelStyle)
				},
				[createCommentVNode(" <div\n      class=\"pointer-events-none absolute inset-0 z-10 transition-opacity duration-300\"\n    >\n      <div class=\"nuxt-devtools-inspect-running-border pointer-events-none absolute inset-0 z-10 border-1.5 border-transparent rounded-lg\" />\n    </div> "), createElementVNode(
					"div",
					_hoisted_1,
					[createElementVNode("div", _hoisted_2, [
						$props.props.hasParent ? (openBlock(), createElementBlock("button", {
							key: 0,
							title: "Go to parent",
							class: "flex items-center border-1 border-base rounded px1 py0.5 text-sm font-mono op50 disabled:pointer-events-none hover:text-green6 hover:op100 disabled:op10!",
							onClick: $setup.selectParent
						}, [..._cache[0] || (_cache[0] = [createElementVNode(
							"div",
							{ class: "i-ph-arrow-bend-left-up-duotone text-lg" },
							null,
							-1
							/* CACHED */
						), createTextVNode(
							" Parent ",
							-1
							/* CACHED */
						)])])) : createCommentVNode("v-if", true),
						createElementVNode("button", {
							title: "Open in editor",
							class: "flex items-center border-1 border-base rounded px1 py0.5 text-sm font-mono op50 hover:text-green6 hover:op100",
							onClick: $setup.openInEditor
						}, [..._cache[1] || (_cache[1] = [createElementVNode(
							"div",
							{ class: "i-ph-arrow-up-right-light text-lg" },
							null,
							-1
							/* CACHED */
						), createTextVNode(
							" Open ",
							-1
							/* CACHED */
						)])]),
						createElementVNode("button", {
							title: "Copy infos for agents",
							class: "flex items-center border-1 border-base rounded px1 py0.5 text-sm font-mono op50 hover:text-green6 hover:op100",
							onClick: $setup.copyAgentInfo
						}, [..._cache[2] || (_cache[2] = [createElementVNode(
							"div",
							{ class: "i-ph-copy-duotone text-lg" },
							null,
							-1
							/* CACHED */
						), createTextVNode(
							" Info ",
							-1
							/* CACHED */
						)])]),
						_cache[4] || (_cache[4] = createElementVNode(
							"div",
							{ class: "flex-auto" },
							null,
							-1
							/* CACHED */
						)),
						createElementVNode("button", {
							title: "Close",
							class: "flex-none op50 hover:op100",
							onClick: $setup.close
						}, [..._cache[3] || (_cache[3] = [createElementVNode(
							"div",
							{ class: "i-ph-x text-lg" },
							null,
							-1
							/* CACHED */
						)])])
					]), createElementVNode("div", _hoisted_3, [
						createCommentVNode(" File "),
						_cache[5] || (_cache[5] = createElementVNode(
							"div",
							{
								class: "i-ph-file-duotone flex-none text-lg op50",
								title: "File"
							},
							null,
							-1
							/* CACHED */
						)),
						createElementVNode(
							"span",
							_hoisted_4,
							toDisplayString($props.props.matched.pos[0]) + ":" + toDisplayString($props.props.matched.pos[1]) + ":" + toDisplayString($props.props.matched.pos[2]),
							1
							/* TEXT */
						),
						createCommentVNode(" Component Tree "),
						_cache[6] || (_cache[6] = createElementVNode(
							"div",
							{
								class: "i-ph-tree-view-duotone flex-none text-lg op50",
								title: "Component Tree"
							},
							null,
							-1
							/* CACHED */
						)),
						createElementVNode(
							"span",
							_hoisted_5,
							toDisplayString($setup.buildComponentTree()),
							1
							/* TEXT */
						)
					])],
					512
					/* NEED_PATCH */
				)],
				6
				/* CLASS, STYLE */
			)) : createCommentVNode("v-if", true),
			createCommentVNode(" Toast notification "),
			withDirectives(createElementVNode(
				"div",
				{ class: normalizeClass(["fixed bottom-20px right-20px z-99999999 max-w-500px flex flex-col gap-2 rounded-lg bg-glass p4 text-sm color-base shadow-xl ring-1 ring-base backdrop-blur transition-all duration-300", $setup.showToast ? "translate-y-0 op100" : "translate-y-10 op0"]) },
				[_cache[7] || (_cache[7] = createElementVNode(
					"div",
					{ class: "flex items-center gap-2" },
					[createElementVNode("div", { class: "i-ph-check-circle-duotone text-xl text-green6" }), createElementVNode("span", { class: "font-semibold" }, "Infos for agents copied to clipboard")],
					-1
					/* CACHED */
				)), createElementVNode(
					"pre",
					_hoisted_6,
					toDisplayString($setup.toastContent),
					1
					/* TEXT */
				)],
				2
				/* CLASS */
			), [[vShow, $setup.showToast]])
		],
		64
		/* STABLE_FRAGMENT */
	);
}
const Component = /* @__PURE__ */ _export_sfc(_sfc_main, [["render", _sfc_render], ["__file", "/home/runner/work/devtools/devtools/packages/devtools/src/webcomponents/components/NuxtDevtoolsInspectPanel.vue"]]);

const NuxtDevtoolsInspectPanel = defineCustomElement(
  Component,
  {
    shadowRoot: true,
    styles: [css]
  }
);
customElements.define("nuxt-devtools-inspect-panel", NuxtDevtoolsInspectPanel);

export { NuxtDevtoolsFrame, NuxtDevtoolsInspectPanel };
