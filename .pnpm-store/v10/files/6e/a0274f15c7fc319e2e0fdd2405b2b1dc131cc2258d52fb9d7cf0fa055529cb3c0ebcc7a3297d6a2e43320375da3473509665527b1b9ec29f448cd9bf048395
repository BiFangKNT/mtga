import { Fragment, computed, createBaseVNode, createBlock, createCommentVNode, createElementBlock, createVNode, defineComponent, h, normalizeClass, normalizeStyle, openBlock, renderList, renderSlot, resolveDynamicComponent, toDisplayString, unref, withCtx } from "./runtime-core.esm-bundler-Cyv4obHQ.js";
import { isDark, toggleDark, usePayloadStore } from "./payload-BX9lTMvN.js";
import { __plugin_vue_export_helper_default } from "./_plugin-vue_export-helper-DfavQbjy.js";
const _sfc_main = {};
const _hoisted_1$4 = { class: "h-[calc(100vh-55px)]" };
function _sfc_render(_ctx, _cache) {
	return openBlock(), createElementBlock("div", _hoisted_1$4, [renderSlot(_ctx.$slots, "default")]);
}
var Container_default = /* @__PURE__ */ __plugin_vue_export_helper_default(_sfc_main, [["render", _sfc_render]]);
/**
* Predefined color map for matching the branding
*
* Accpet a 6-digit hex color string or a hue number
* Hue numbers are preferred because they will adapt better contrast in light/dark mode
*
* Hue numbers reference:
* - 0: red
* - 30: orange
* - 60: yellow
* - 120: green
* - 180: cyan
* - 240: blue
* - 270: purple
*/
const predefinedColorMap = {
	error: 0,
	client: 60,
	bailout: -1,
	ssr: 270,
	vite: 250,
	vite1: 240,
	vite2: 120,
	virtual: 140
};
function getHashColorFromString(name, opacity = 1) {
	if (predefinedColorMap[name]) return getHsla(predefinedColorMap[name], opacity);
	let hash = 0;
	for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
	const hue = hash % 360;
	return getHsla(hue, opacity);
}
function getHsla(hue, opacity = 1) {
	const saturation = hue === -1 ? 0 : isDark.value ? 50 : 100;
	const lightness = isDark.value ? 60 : 20;
	return `hsla(${hue}, ${saturation}%, ${lightness}%, ${opacity})`;
}
function getPluginColor(name, opacity = 1) {
	if (predefinedColorMap[name]) {
		const color = predefinedColorMap[name];
		if (typeof color === "number") return getHsla(color, opacity);
		else {
			if (opacity === 1) return color;
			const opacityHex = Math.floor(opacity * 255).toString(16).padStart(2, "0");
			return color + opacityHex;
		}
	}
	return getHashColorFromString(name, opacity);
}
var PluginName_vue_vue_type_script_setup_true_lang_default = /* @__PURE__ */ defineComponent({
	__name: "PluginName",
	props: {
		name: {},
		compact: { type: Boolean },
		colored: { type: Boolean },
		hide: { type: Boolean }
	},
	setup(__props) {
		const props = __props;
		const startsGeneric = [
			"__load__",
			"vite-plugin-",
			"vite-",
			"rollup-plugin-",
			"rollup-",
			"unplugin-"
		];
		const startCompact = [...startsGeneric, "vite:"];
		function render() {
			const starts = props.compact ? startCompact : startsGeneric;
			for (const s of starts) if (props.name.startsWith(s)) {
				if (props.compact) return h("span", props.name.slice(s.length));
				return h("span", [h("span", { class: "op50" }, s), h("span", props.name.slice(s.length))]);
			}
			const parts = props.name.split(":");
			if (parts.length > 1) return h("span", [h("span", { style: { color: getHashColorFromString(parts[0]) } }, `${parts[0]}:`), h("span", parts.slice(1).join(":"))]);
			return h("span", props.name);
		}
		return (_ctx, _cache) => {
			return openBlock(), createBlock(resolveDynamicComponent(render));
		};
	}
});
var PluginName_default = PluginName_vue_vue_type_script_setup_true_lang_default;
const _hoisted_1$3 = ["textContent"];
var Badge_vue_vue_type_script_setup_true_lang_default = /* @__PURE__ */ defineComponent({
	__name: "Badge",
	props: {
		text: {},
		color: {
			type: [Boolean, Number],
			default: true
		},
		as: {},
		size: {}
	},
	setup(__props) {
		const props = __props;
		const style = computed(() => {
			if (!props.text || props.color === false) return {};
			return {
				color: typeof props.color === "number" ? getHsla(props.color) : getHashColorFromString(props.text),
				background: typeof props.color === "number" ? getHsla(props.color, .1) : getHashColorFromString(props.text, .1)
			};
		});
		const sizeClasses = computed(() => {
			switch (props.size || "sm") {
				case "sm": return "px-1.5 text-11px leading-1.6em";
			}
			return "";
		});
		return (_ctx, _cache) => {
			return openBlock(), createBlock(resolveDynamicComponent(_ctx.as || "span"), {
				"ws-nowrap": "",
				rounded: "",
				class: normalizeClass(unref(sizeClasses)),
				style: normalizeStyle(unref(style))
			}, {
				default: withCtx(() => [renderSlot(_ctx.$slots, "default", {}, () => [createBaseVNode("span", { textContent: toDisplayString(props.text) }, null, 8, _hoisted_1$3)])]),
				_: 3
			}, 8, ["class", "style"]);
		};
	}
});
var Badge_default = Badge_vue_vue_type_script_setup_true_lang_default;
const _hoisted_1$2 = {
	"h-54px": "",
	flex: "~ none gap-2",
	border: "b main",
	"pl-4": "",
	"pr-4": "",
	"font-light": "",
	"children:my-auto": ""
};
var NavBar_vue_vue_type_script_setup_true_lang_default = /* @__PURE__ */ defineComponent({
	__name: "NavBar",
	setup(__props) {
		const payload = usePayloadStore();
		return (_ctx, _cache) => {
			return openBlock(), createElementBlock("nav", _hoisted_1$2, [renderSlot(_ctx.$slots, "default"), renderSlot(_ctx.$slots, "actions", {}, () => [!unref(payload).metadata.embedded ? (openBlock(), createElementBlock(Fragment, { key: 0 }, [
				_cache[2] || (_cache[2] = createBaseVNode("div", {
					mx1: "",
					"h-full": "",
					"w-0": "",
					border: "r main"
				}, null, -1)),
				_cache[3] || (_cache[3] = createBaseVNode("a", {
					"icon-btn": "",
					"text-lg": "",
					href: "https://github.com/antfu/vite-plugin-inspect",
					target: "_blank"
				}, [createBaseVNode("div", { "i-carbon-logo-github": "" })], -1)),
				createBaseVNode("button", {
					class: "icon-btn text-lg",
					title: "Toggle Dark Mode",
					onClick: _cache[0] || (_cache[0] = ($event) => unref(toggleDark)())
				}, [..._cache[1] || (_cache[1] = [createBaseVNode("span", {
					"i-carbon-sun": "",
					"dark:i-carbon-moon": ""
				}, null, -1)])])
			], 64)) : createCommentVNode("", true)])]);
		};
	}
});
var NavBar_default = NavBar_vue_vue_type_script_setup_true_lang_default;
const _hoisted_1$1 = {
	flex: "~ gap-1 items-center",
	border: "~ subtle rounded",
	"bg-subtle": "",
	p1: ""
};
var SegmentControl_vue_vue_type_script_setup_true_lang_default = /* @__PURE__ */ defineComponent({
	__name: "SegmentControl",
	props: {
		options: {},
		modelValue: {}
	},
	emits: ["update:modelValue"],
	setup(__props) {
		return (_ctx, _cache) => {
			const _component_Badge = Badge_default;
			return openBlock(), createElementBlock("div", _hoisted_1$1, [(openBlock(true), createElementBlock(Fragment, null, renderList(_ctx.options, (option) => {
				return openBlock(), createBlock(_component_Badge, {
					key: option.value,
					class: normalizeClass(["px-2 py-1 text-xs font-mono", option.value === _ctx.modelValue ? "" : "op50"]),
					color: option.value === _ctx.modelValue,
					"aria-pressed": option.value === _ctx.modelValue,
					size: "none",
					text: option.label,
					as: "button",
					onClick: ($event) => _ctx.$emit("update:modelValue", option.value)
				}, null, 8, [
					"class",
					"color",
					"aria-pressed",
					"text",
					"onClick"
				]);
			}), 128))]);
		};
	}
});
var SegmentControl_default = SegmentControl_vue_vue_type_script_setup_true_lang_default;
const _hoisted_1 = { flex: "~ gap-2" };
var QuerySelector_vue_vue_type_script_setup_true_lang_default = /* @__PURE__ */ defineComponent({
	__name: "QuerySelector",
	setup(__props) {
		const payload = usePayloadStore();
		return (_ctx, _cache) => {
			const _component_SegmentControl = SegmentControl_default;
			return openBlock(), createElementBlock("div", _hoisted_1, [unref(payload).metadata.instances.length > 1 ? (openBlock(), createBlock(_component_SegmentControl, {
				key: 0,
				modelValue: unref(payload).query.vite,
				"onUpdate:modelValue": _cache[0] || (_cache[0] = ($event) => unref(payload).query.vite = $event),
				options: unref(payload).metadata.instances.map((i) => ({
					label: i.vite,
					value: i.vite
				}))
			}, null, 8, ["modelValue", "options"])) : createCommentVNode("", true), createVNode(_component_SegmentControl, {
				modelValue: unref(payload).query.env,
				"onUpdate:modelValue": _cache[1] || (_cache[1] = ($event) => unref(payload).query.env = $event),
				options: unref(payload).instance.environments.map((i) => ({
					label: i,
					value: i
				}))
			}, null, 8, ["modelValue", "options"])]);
		};
	}
});
var QuerySelector_default = QuerySelector_vue_vue_type_script_setup_true_lang_default;
export { Badge_default, Container_default, NavBar_default, PluginName_default, QuerySelector_default, SegmentControl_default, getPluginColor };
