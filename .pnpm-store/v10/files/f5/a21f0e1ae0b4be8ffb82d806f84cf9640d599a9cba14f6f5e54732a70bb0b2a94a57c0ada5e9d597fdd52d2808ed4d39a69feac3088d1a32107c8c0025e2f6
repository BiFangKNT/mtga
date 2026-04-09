import { Fragment, computed, createBaseVNode, createBlock, createCommentVNode, createElementBlock, createTextVNode, createVNode, defineComponent, guardReactiveProps, h, mergeProps, nextTick, normalizeClass, normalizeProps, normalizeStyle, openBlock, popScopeId, pushScopeId, ref, renderList, renderSlot, resolveComponent, toDisplayString, toRef, unref, withCtx, withDirectives, withScopeId } from "./runtime-core.esm-bundler-Cyv4obHQ.js";
import { createApp, useRoute, withKeys } from "./vue-router-BxYGFXy-.js";
import { isDark, usePayloadStore, useVirtualList } from "./payload-BX9lTMvN.js";
import { Badge_default, PluginName_default, getPluginColor } from "./QuerySelector-iLRAQoow.js";
import { DurationDisplay_default, NumberWithUnit_default, useOptionsStore } from "./options-D_MMddT_.js";
var ByteSizeDisplay_vue_vue_type_script_setup_true_lang_default = /* @__PURE__ */ defineComponent({
	__name: "ByteSizeDisplay",
	props: { bytes: {} },
	setup(__props) {
		const props = __props;
		function byteToHumanReadable(byte) {
			if (byte < 1024) return [byte, "B"];
			if (byte < 1024 * 1024) return [(byte / 1024).toFixed(2), "KB"];
			if (byte < 1024 * 1024 * 1024) return [(byte / 1024 / 1024).toFixed(2), "MB"];
			return [(byte / 1024 / 1024 / 1024).toFixed(2), "GB"];
		}
		const readable = computed(() => byteToHumanReadable(props.bytes));
		return (_ctx, _cache) => {
			const _component_NumberWithUnit = NumberWithUnit_default;
			return openBlock(), createBlock(_component_NumberWithUnit, {
				number: unref(readable)[0],
				unit: unref(readable)[1]
			}, null, 8, ["number", "unit"]);
		};
	}
});
var ByteSizeDisplay_default = ByteSizeDisplay_vue_vue_type_script_setup_true_lang_default;
var FileIcon_vue_vue_type_script_setup_true_lang_default = /* @__PURE__ */ defineComponent({
	__name: "FileIcon",
	props: { filename: {} },
	setup(__props) {
		const props = __props;
		const map = {
			angular: "i-catppuccin-angular",
			vue: "i-catppuccin-vue",
			js: "i-catppuccin-javascript",
			mjs: "i-catppuccin-javascript",
			cjs: "i-catppuccin-javascript",
			ts: "i-catppuccin-typescript",
			mts: "i-catppuccin-typescript",
			cts: "i-catppuccin-typescript",
			md: "i-catppuccin-markdown",
			markdown: "i-catppuccin-markdown",
			mdx: "i-catppuccin-mdx",
			jsx: "i-catppuccin-javascript-react",
			tsx: "i-catppuccin-typescript-react",
			svelte: "i-catppuccin-svelte",
			html: "i-catppuccin-html",
			css: "i-catppuccin-css",
			scss: "i-catppuccin-css",
			less: "i-catppuccin-less",
			json: "i-catppuccin-json",
			yaml: "i-catppuccin-yaml",
			toml: "i-catppuccin-toml",
			svg: "i-catppuccin-svg"
		};
		const icon = computed(() => {
			let file = props.filename;
			file = file.replace(/(\?|&)v=[^&]*/, "$1").replace(/\?$/, "");
			if (file.match(/[\\/]node_modules[\\/]/)) return "i-catppuccin-folder-node-open";
			let ext = (file.split(".").pop() || "").toLowerCase();
			let icon$1 = map[ext];
			if (icon$1) return icon$1;
			ext = ext.split("?")[0];
			icon$1 = map[ext];
			if (icon$1) return icon$1;
			return "i-catppuccin-file";
		});
		return (_ctx, _cache) => {
			return openBlock(), createElementBlock("div", {
				"flex-none": "",
				class: normalizeClass([unref(icon), unref(isDark) ? "" : "brightness-60 hue-rotate-180 invert-100 saturate-200"])
			}, null, 2);
		};
	}
});
var FileIcon_default = FileIcon_vue_vue_type_script_setup_true_lang_default;
/**
* Custom positioning reference element.
* @see https://floating-ui.com/docs/virtual-elements
*/
const sides = [
	"top",
	"right",
	"bottom",
	"left"
];
const alignments = ["start", "end"];
const placements = /* @__PURE__ */ sides.reduce((acc, side) => acc.concat(side, side + "-" + alignments[0], side + "-" + alignments[1]), []);
const min = Math.min;
const max = Math.max;
const oppositeSideMap = {
	left: "right",
	right: "left",
	bottom: "top",
	top: "bottom"
};
const oppositeAlignmentMap = {
	start: "end",
	end: "start"
};
function clamp(start, value, end) {
	return max(start, min(value, end));
}
function evaluate(value, param) {
	return typeof value === "function" ? value(param) : value;
}
function getSide(placement) {
	return placement.split("-")[0];
}
function getAlignment(placement) {
	return placement.split("-")[1];
}
function getOppositeAxis(axis) {
	return axis === "x" ? "y" : "x";
}
function getAxisLength(axis) {
	return axis === "y" ? "height" : "width";
}
function getSideAxis(placement) {
	return ["top", "bottom"].includes(getSide(placement)) ? "y" : "x";
}
function getAlignmentAxis(placement) {
	return getOppositeAxis(getSideAxis(placement));
}
function getAlignmentSides(placement, rects, rtl) {
	if (rtl === void 0) rtl = false;
	const alignment = getAlignment(placement);
	const alignmentAxis = getAlignmentAxis(placement);
	const length = getAxisLength(alignmentAxis);
	let mainAlignmentSide = alignmentAxis === "x" ? alignment === (rtl ? "end" : "start") ? "right" : "left" : alignment === "start" ? "bottom" : "top";
	if (rects.reference[length] > rects.floating[length]) mainAlignmentSide = getOppositePlacement(mainAlignmentSide);
	return [mainAlignmentSide, getOppositePlacement(mainAlignmentSide)];
}
function getExpandedPlacements(placement) {
	const oppositePlacement = getOppositePlacement(placement);
	return [
		getOppositeAlignmentPlacement(placement),
		oppositePlacement,
		getOppositeAlignmentPlacement(oppositePlacement)
	];
}
function getOppositeAlignmentPlacement(placement) {
	return placement.replace(/start|end/g, (alignment) => oppositeAlignmentMap[alignment]);
}
function getSideList(side, isStart, rtl) {
	const lr = ["left", "right"];
	const rl = ["right", "left"];
	const tb = ["top", "bottom"];
	const bt$1 = ["bottom", "top"];
	switch (side) {
		case "top":
		case "bottom":
			if (rtl) return isStart ? rl : lr;
			return isStart ? lr : rl;
		case "left":
		case "right": return isStart ? tb : bt$1;
		default: return [];
	}
}
function getOppositeAxisPlacements(placement, flipAlignment, direction, rtl) {
	const alignment = getAlignment(placement);
	let list = getSideList(getSide(placement), direction === "start", rtl);
	if (alignment) {
		list = list.map((side) => side + "-" + alignment);
		if (flipAlignment) list = list.concat(list.map(getOppositeAlignmentPlacement));
	}
	return list;
}
function getOppositePlacement(placement) {
	return placement.replace(/left|right|bottom|top/g, (side) => oppositeSideMap[side]);
}
function expandPaddingObject(padding) {
	return {
		top: 0,
		right: 0,
		bottom: 0,
		left: 0,
		...padding
	};
}
function getPaddingObject(padding) {
	return typeof padding !== "number" ? expandPaddingObject(padding) : {
		top: padding,
		right: padding,
		bottom: padding,
		left: padding
	};
}
function rectToClientRect(rect) {
	const { x: x$2, y: y$2, width, height } = rect;
	return {
		width,
		height,
		top: y$2,
		left: x$2,
		right: x$2 + width,
		bottom: y$2 + height,
		x: x$2,
		y: y$2
	};
}
function computeCoordsFromPlacement(_ref, placement, rtl) {
	let { reference, floating } = _ref;
	const sideAxis = getSideAxis(placement);
	const alignmentAxis = getAlignmentAxis(placement);
	const alignLength = getAxisLength(alignmentAxis);
	const side = getSide(placement);
	const isVertical = sideAxis === "y";
	const commonX = reference.x + reference.width / 2 - floating.width / 2;
	const commonY = reference.y + reference.height / 2 - floating.height / 2;
	const commonAlign = reference[alignLength] / 2 - floating[alignLength] / 2;
	let coords;
	switch (side) {
		case "top":
			coords = {
				x: commonX,
				y: reference.y - floating.height
			};
			break;
		case "bottom":
			coords = {
				x: commonX,
				y: reference.y + reference.height
			};
			break;
		case "right":
			coords = {
				x: reference.x + reference.width,
				y: commonY
			};
			break;
		case "left":
			coords = {
				x: reference.x - floating.width,
				y: commonY
			};
			break;
		default: coords = {
			x: reference.x,
			y: reference.y
		};
	}
	switch (getAlignment(placement)) {
		case "start":
			coords[alignmentAxis] -= commonAlign * (rtl && isVertical ? -1 : 1);
			break;
		case "end":
			coords[alignmentAxis] += commonAlign * (rtl && isVertical ? -1 : 1);
			break;
	}
	return coords;
}
/**
* Computes the `x` and `y` coordinates that will place the floating element
* next to a given reference element.
*
* This export does not have any `platform` interface logic. You will need to
* write one for the platform you are using Floating UI with.
*/
const computePosition = async (reference, floating, config) => {
	const { placement = "bottom", strategy = "absolute", middleware = [], platform } = config;
	const validMiddleware = middleware.filter(Boolean);
	const rtl = await (platform.isRTL == null ? void 0 : platform.isRTL(floating));
	let rects = await platform.getElementRects({
		reference,
		floating,
		strategy
	});
	let { x: x$2, y: y$2 } = computeCoordsFromPlacement(rects, placement, rtl);
	let statefulPlacement = placement;
	let middlewareData = {};
	let resetCount = 0;
	for (let i$1 = 0; i$1 < validMiddleware.length; i$1++) {
		const { name, fn } = validMiddleware[i$1];
		const { x: nextX, y: nextY, data, reset } = await fn({
			x: x$2,
			y: y$2,
			initialPlacement: placement,
			placement: statefulPlacement,
			strategy,
			middlewareData,
			rects,
			platform,
			elements: {
				reference,
				floating
			}
		});
		x$2 = nextX != null ? nextX : x$2;
		y$2 = nextY != null ? nextY : y$2;
		middlewareData = {
			...middlewareData,
			[name]: {
				...middlewareData[name],
				...data
			}
		};
		if (reset && resetCount <= 50) {
			resetCount++;
			if (typeof reset === "object") {
				if (reset.placement) statefulPlacement = reset.placement;
				if (reset.rects) rects = reset.rects === true ? await platform.getElementRects({
					reference,
					floating,
					strategy
				}) : reset.rects;
				({x: x$2, y: y$2} = computeCoordsFromPlacement(rects, statefulPlacement, rtl));
			}
			i$1 = -1;
		}
	}
	return {
		x: x$2,
		y: y$2,
		placement: statefulPlacement,
		strategy,
		middlewareData
	};
};
/**
* Resolves with an object of overflow side offsets that determine how much the
* element is overflowing a given clipping boundary on each side.
* - positive = overflowing the boundary by that number of pixels
* - negative = how many pixels left before it will overflow
* - 0 = lies flush with the boundary
* @see https://floating-ui.com/docs/detectOverflow
*/
async function detectOverflow(state, options) {
	var _await$platform$isEle;
	if (options === void 0) options = {};
	const { x: x$2, y: y$2, platform, rects, elements, strategy } = state;
	const { boundary = "clippingAncestors", rootBoundary = "viewport", elementContext = "floating", altBoundary = false, padding = 0 } = evaluate(options, state);
	const paddingObject = getPaddingObject(padding);
	const altContext = elementContext === "floating" ? "reference" : "floating";
	const element = elements[altBoundary ? altContext : elementContext];
	const clippingClientRect = rectToClientRect(await platform.getClippingRect({
		element: ((_await$platform$isEle = await (platform.isElement == null ? void 0 : platform.isElement(element))) != null ? _await$platform$isEle : true) ? element : element.contextElement || await (platform.getDocumentElement == null ? void 0 : platform.getDocumentElement(elements.floating)),
		boundary,
		rootBoundary,
		strategy
	}));
	const rect = elementContext === "floating" ? {
		x: x$2,
		y: y$2,
		width: rects.floating.width,
		height: rects.floating.height
	} : rects.reference;
	const offsetParent = await (platform.getOffsetParent == null ? void 0 : platform.getOffsetParent(elements.floating));
	const offsetScale = await (platform.isElement == null ? void 0 : platform.isElement(offsetParent)) ? await (platform.getScale == null ? void 0 : platform.getScale(offsetParent)) || {
		x: 1,
		y: 1
	} : {
		x: 1,
		y: 1
	};
	const elementClientRect = rectToClientRect(platform.convertOffsetParentRelativeRectToViewportRelativeRect ? await platform.convertOffsetParentRelativeRectToViewportRelativeRect({
		elements,
		rect,
		offsetParent,
		strategy
	}) : rect);
	return {
		top: (clippingClientRect.top - elementClientRect.top + paddingObject.top) / offsetScale.y,
		bottom: (elementClientRect.bottom - clippingClientRect.bottom + paddingObject.bottom) / offsetScale.y,
		left: (clippingClientRect.left - elementClientRect.left + paddingObject.left) / offsetScale.x,
		right: (elementClientRect.right - clippingClientRect.right + paddingObject.right) / offsetScale.x
	};
}
/**
* Provides data to position an inner element of the floating element so that it
* appears centered to the reference element.
* @see https://floating-ui.com/docs/arrow
*/
const arrow = (options) => ({
	name: "arrow",
	options,
	async fn(state) {
		const { x: x$2, y: y$2, placement, rects, platform, elements, middlewareData } = state;
		const { element, padding = 0 } = evaluate(options, state) || {};
		if (element == null) return {};
		const paddingObject = getPaddingObject(padding);
		const coords = {
			x: x$2,
			y: y$2
		};
		const axis = getAlignmentAxis(placement);
		const length = getAxisLength(axis);
		const arrowDimensions = await platform.getDimensions(element);
		const isYAxis = axis === "y";
		const minProp = isYAxis ? "top" : "left";
		const maxProp = isYAxis ? "bottom" : "right";
		const clientProp = isYAxis ? "clientHeight" : "clientWidth";
		const endDiff = rects.reference[length] + rects.reference[axis] - coords[axis] - rects.floating[length];
		const startDiff = coords[axis] - rects.reference[axis];
		const arrowOffsetParent = await (platform.getOffsetParent == null ? void 0 : platform.getOffsetParent(element));
		let clientSize = arrowOffsetParent ? arrowOffsetParent[clientProp] : 0;
		if (!clientSize || !await (platform.isElement == null ? void 0 : platform.isElement(arrowOffsetParent))) clientSize = elements.floating[clientProp] || rects.floating[length];
		const centerToReference = endDiff / 2 - startDiff / 2;
		const largestPossiblePadding = clientSize / 2 - arrowDimensions[length] / 2 - 1;
		const minPadding = min(paddingObject[minProp], largestPossiblePadding);
		const maxPadding = min(paddingObject[maxProp], largestPossiblePadding);
		const min$1 = minPadding;
		const max$1 = clientSize - arrowDimensions[length] - maxPadding;
		const center = clientSize / 2 - arrowDimensions[length] / 2 + centerToReference;
		const offset$1 = clamp(min$1, center, max$1);
		const shouldAddOffset = !middlewareData.arrow && getAlignment(placement) != null && center !== offset$1 && rects.reference[length] / 2 - (center < min$1 ? minPadding : maxPadding) - arrowDimensions[length] / 2 < 0;
		const alignmentOffset = shouldAddOffset ? center < min$1 ? center - min$1 : center - max$1 : 0;
		return {
			[axis]: coords[axis] + alignmentOffset,
			data: {
				[axis]: offset$1,
				centerOffset: center - offset$1 - alignmentOffset,
				...shouldAddOffset && { alignmentOffset }
			},
			reset: shouldAddOffset
		};
	}
});
function getPlacementList(alignment, autoAlignment, allowedPlacements) {
	const allowedPlacementsSortedByAlignment = alignment ? [...allowedPlacements.filter((placement) => getAlignment(placement) === alignment), ...allowedPlacements.filter((placement) => getAlignment(placement) !== alignment)] : allowedPlacements.filter((placement) => getSide(placement) === placement);
	return allowedPlacementsSortedByAlignment.filter((placement) => {
		if (alignment) return getAlignment(placement) === alignment || (autoAlignment ? getOppositeAlignmentPlacement(placement) !== placement : false);
		return true;
	});
}
/**
* Optimizes the visibility of the floating element by choosing the placement
* that has the most space available automatically, without needing to specify a
* preferred placement. Alternative to `flip`.
* @see https://floating-ui.com/docs/autoPlacement
*/
const autoPlacement = function(options) {
	if (options === void 0) options = {};
	return {
		name: "autoPlacement",
		options,
		async fn(state) {
			var _middlewareData$autoP, _middlewareData$autoP2, _placementsThatFitOnE;
			const { rects, middlewareData, placement, platform, elements } = state;
			const { crossAxis = false, alignment, allowedPlacements = placements, autoAlignment = true,...detectOverflowOptions } = evaluate(options, state);
			const placements$1 = alignment !== void 0 || allowedPlacements === placements ? getPlacementList(alignment || null, autoAlignment, allowedPlacements) : allowedPlacements;
			const overflow = await detectOverflow(state, detectOverflowOptions);
			const currentIndex = ((_middlewareData$autoP = middlewareData.autoPlacement) == null ? void 0 : _middlewareData$autoP.index) || 0;
			const currentPlacement = placements$1[currentIndex];
			if (currentPlacement == null) return {};
			const alignmentSides = getAlignmentSides(currentPlacement, rects, await (platform.isRTL == null ? void 0 : platform.isRTL(elements.floating)));
			if (placement !== currentPlacement) return { reset: { placement: placements$1[0] } };
			const currentOverflows = [
				overflow[getSide(currentPlacement)],
				overflow[alignmentSides[0]],
				overflow[alignmentSides[1]]
			];
			const allOverflows = [...((_middlewareData$autoP2 = middlewareData.autoPlacement) == null ? void 0 : _middlewareData$autoP2.overflows) || [], {
				placement: currentPlacement,
				overflows: currentOverflows
			}];
			const nextPlacement = placements$1[currentIndex + 1];
			if (nextPlacement) return {
				data: {
					index: currentIndex + 1,
					overflows: allOverflows
				},
				reset: { placement: nextPlacement }
			};
			const placementsSortedByMostSpace = allOverflows.map((d$2) => {
				const alignment$1 = getAlignment(d$2.placement);
				return [
					d$2.placement,
					alignment$1 && crossAxis ? d$2.overflows.slice(0, 2).reduce((acc, v$1) => acc + v$1, 0) : d$2.overflows[0],
					d$2.overflows
				];
			}).sort((a$1, b$2) => a$1[1] - b$2[1]);
			const placementsThatFitOnEachSide = placementsSortedByMostSpace.filter((d$2) => d$2[2].slice(
				0,
				// Aligned placements should not check their opposite crossAxis
				// side.
				getAlignment(d$2[0]) ? 2 : 3
).every((v$1) => v$1 <= 0));
			const resetPlacement = ((_placementsThatFitOnE = placementsThatFitOnEachSide[0]) == null ? void 0 : _placementsThatFitOnE[0]) || placementsSortedByMostSpace[0][0];
			if (resetPlacement !== placement) return {
				data: {
					index: currentIndex + 1,
					overflows: allOverflows
				},
				reset: { placement: resetPlacement }
			};
			return {};
		}
	};
};
/**
* Optimizes the visibility of the floating element by flipping the `placement`
* in order to keep it in view when the preferred placement(s) will overflow the
* clipping boundary. Alternative to `autoPlacement`.
* @see https://floating-ui.com/docs/flip
*/
const flip = function(options) {
	if (options === void 0) options = {};
	return {
		name: "flip",
		options,
		async fn(state) {
			var _middlewareData$arrow, _middlewareData$flip;
			const { placement, middlewareData, rects, initialPlacement, platform, elements } = state;
			const { mainAxis: checkMainAxis = true, crossAxis: checkCrossAxis = true, fallbackPlacements: specifiedFallbackPlacements, fallbackStrategy = "bestFit", fallbackAxisSideDirection = "none", flipAlignment = true,...detectOverflowOptions } = evaluate(options, state);
			if ((_middlewareData$arrow = middlewareData.arrow) != null && _middlewareData$arrow.alignmentOffset) return {};
			const side = getSide(placement);
			const initialSideAxis = getSideAxis(initialPlacement);
			const isBasePlacement = getSide(initialPlacement) === initialPlacement;
			const rtl = await (platform.isRTL == null ? void 0 : platform.isRTL(elements.floating));
			const fallbackPlacements = specifiedFallbackPlacements || (isBasePlacement || !flipAlignment ? [getOppositePlacement(initialPlacement)] : getExpandedPlacements(initialPlacement));
			const hasFallbackAxisSideDirection = fallbackAxisSideDirection !== "none";
			if (!specifiedFallbackPlacements && hasFallbackAxisSideDirection) fallbackPlacements.push(...getOppositeAxisPlacements(initialPlacement, flipAlignment, fallbackAxisSideDirection, rtl));
			const placements$1 = [initialPlacement, ...fallbackPlacements];
			const overflow = await detectOverflow(state, detectOverflowOptions);
			const overflows = [];
			let overflowsData = ((_middlewareData$flip = middlewareData.flip) == null ? void 0 : _middlewareData$flip.overflows) || [];
			if (checkMainAxis) overflows.push(overflow[side]);
			if (checkCrossAxis) {
				const sides$1 = getAlignmentSides(placement, rects, rtl);
				overflows.push(overflow[sides$1[0]], overflow[sides$1[1]]);
			}
			overflowsData = [...overflowsData, {
				placement,
				overflows
			}];
			if (!overflows.every((side$1) => side$1 <= 0)) {
				var _middlewareData$flip2, _overflowsData$filter;
				const nextIndex = (((_middlewareData$flip2 = middlewareData.flip) == null ? void 0 : _middlewareData$flip2.index) || 0) + 1;
				const nextPlacement = placements$1[nextIndex];
				if (nextPlacement) return {
					data: {
						index: nextIndex,
						overflows: overflowsData
					},
					reset: { placement: nextPlacement }
				};
				let resetPlacement = (_overflowsData$filter = overflowsData.filter((d$2) => d$2.overflows[0] <= 0).sort((a$1, b$2) => a$1.overflows[1] - b$2.overflows[1])[0]) == null ? void 0 : _overflowsData$filter.placement;
				if (!resetPlacement) switch (fallbackStrategy) {
					case "bestFit": {
						var _overflowsData$filter2;
						const placement$1 = (_overflowsData$filter2 = overflowsData.filter((d$2) => {
							if (hasFallbackAxisSideDirection) {
								const currentSideAxis = getSideAxis(d$2.placement);
								return currentSideAxis === initialSideAxis || currentSideAxis === "y";
							}
							return true;
						}).map((d$2) => [d$2.placement, d$2.overflows.filter((overflow$1) => overflow$1 > 0).reduce((acc, overflow$1) => acc + overflow$1, 0)]).sort((a$1, b$2) => a$1[1] - b$2[1])[0]) == null ? void 0 : _overflowsData$filter2[0];
						if (placement$1) resetPlacement = placement$1;
						break;
					}
					case "initialPlacement":
						resetPlacement = initialPlacement;
						break;
				}
				if (placement !== resetPlacement) return { reset: { placement: resetPlacement } };
			}
			return {};
		}
	};
};
async function convertValueToCoords(state, options) {
	const { placement, platform, elements } = state;
	const rtl = await (platform.isRTL == null ? void 0 : platform.isRTL(elements.floating));
	const side = getSide(placement);
	const alignment = getAlignment(placement);
	const isVertical = getSideAxis(placement) === "y";
	const mainAxisMulti = ["left", "top"].includes(side) ? -1 : 1;
	const crossAxisMulti = rtl && isVertical ? -1 : 1;
	const rawValue = evaluate(options, state);
	let { mainAxis, crossAxis, alignmentAxis } = typeof rawValue === "number" ? {
		mainAxis: rawValue,
		crossAxis: 0,
		alignmentAxis: null
	} : {
		mainAxis: rawValue.mainAxis || 0,
		crossAxis: rawValue.crossAxis || 0,
		alignmentAxis: rawValue.alignmentAxis
	};
	if (alignment && typeof alignmentAxis === "number") crossAxis = alignment === "end" ? alignmentAxis * -1 : alignmentAxis;
	return isVertical ? {
		x: crossAxis * crossAxisMulti,
		y: mainAxis * mainAxisMulti
	} : {
		x: mainAxis * mainAxisMulti,
		y: crossAxis * crossAxisMulti
	};
}
/**
* Modifies the placement by translating the floating element along the
* specified axes.
* A number (shorthand for `mainAxis` or distance), or an axes configuration
* object may be passed.
* @see https://floating-ui.com/docs/offset
*/
const offset = function(options) {
	if (options === void 0) options = 0;
	return {
		name: "offset",
		options,
		async fn(state) {
			var _middlewareData$offse, _middlewareData$arrow;
			const { x: x$2, y: y$2, placement, middlewareData } = state;
			const diffCoords = await convertValueToCoords(state, options);
			if (placement === ((_middlewareData$offse = middlewareData.offset) == null ? void 0 : _middlewareData$offse.placement) && (_middlewareData$arrow = middlewareData.arrow) != null && _middlewareData$arrow.alignmentOffset) return {};
			return {
				x: x$2 + diffCoords.x,
				y: y$2 + diffCoords.y,
				data: {
					...diffCoords,
					placement
				}
			};
		}
	};
};
/**
* Optimizes the visibility of the floating element by shifting it in order to
* keep it in view when it will overflow the clipping boundary.
* @see https://floating-ui.com/docs/shift
*/
const shift = function(options) {
	if (options === void 0) options = {};
	return {
		name: "shift",
		options,
		async fn(state) {
			const { x: x$2, y: y$2, placement } = state;
			const { mainAxis: checkMainAxis = true, crossAxis: checkCrossAxis = false, limiter = { fn: (_ref) => {
				let { x: x$3, y: y$3 } = _ref;
				return {
					x: x$3,
					y: y$3
				};
			} },...detectOverflowOptions } = evaluate(options, state);
			const coords = {
				x: x$2,
				y: y$2
			};
			const overflow = await detectOverflow(state, detectOverflowOptions);
			const crossAxis = getSideAxis(getSide(placement));
			const mainAxis = getOppositeAxis(crossAxis);
			let mainAxisCoord = coords[mainAxis];
			let crossAxisCoord = coords[crossAxis];
			if (checkMainAxis) {
				const minSide = mainAxis === "y" ? "top" : "left";
				const maxSide = mainAxis === "y" ? "bottom" : "right";
				const min$1 = mainAxisCoord + overflow[minSide];
				const max$1 = mainAxisCoord - overflow[maxSide];
				mainAxisCoord = clamp(min$1, mainAxisCoord, max$1);
			}
			if (checkCrossAxis) {
				const minSide = crossAxis === "y" ? "top" : "left";
				const maxSide = crossAxis === "y" ? "bottom" : "right";
				const min$1 = crossAxisCoord + overflow[minSide];
				const max$1 = crossAxisCoord - overflow[maxSide];
				crossAxisCoord = clamp(min$1, crossAxisCoord, max$1);
			}
			const limitedCoords = limiter.fn({
				...state,
				[mainAxis]: mainAxisCoord,
				[crossAxis]: crossAxisCoord
			});
			return {
				...limitedCoords,
				data: {
					x: limitedCoords.x - x$2,
					y: limitedCoords.y - y$2,
					enabled: {
						[mainAxis]: checkMainAxis,
						[crossAxis]: checkCrossAxis
					}
				}
			};
		}
	};
};
/**
* Provides data that allows you to change the size of the floating element —
* for instance, prevent it from overflowing the clipping boundary or match the
* width of the reference element.
* @see https://floating-ui.com/docs/size
*/
const size = function(options) {
	if (options === void 0) options = {};
	return {
		name: "size",
		options,
		async fn(state) {
			var _state$middlewareData, _state$middlewareData2;
			const { placement, rects, platform, elements } = state;
			const { apply = () => {},...detectOverflowOptions } = evaluate(options, state);
			const overflow = await detectOverflow(state, detectOverflowOptions);
			const side = getSide(placement);
			const alignment = getAlignment(placement);
			const isYAxis = getSideAxis(placement) === "y";
			const { width, height } = rects.floating;
			let heightSide;
			let widthSide;
			if (side === "top" || side === "bottom") {
				heightSide = side;
				widthSide = alignment === (await (platform.isRTL == null ? void 0 : platform.isRTL(elements.floating)) ? "start" : "end") ? "left" : "right";
			} else {
				widthSide = side;
				heightSide = alignment === "end" ? "top" : "bottom";
			}
			const maximumClippingHeight = height - overflow.top - overflow.bottom;
			const maximumClippingWidth = width - overflow.left - overflow.right;
			const overflowAvailableHeight = min(height - overflow[heightSide], maximumClippingHeight);
			const overflowAvailableWidth = min(width - overflow[widthSide], maximumClippingWidth);
			const noShift = !state.middlewareData.shift;
			let availableHeight = overflowAvailableHeight;
			let availableWidth = overflowAvailableWidth;
			if ((_state$middlewareData = state.middlewareData.shift) != null && _state$middlewareData.enabled.x) availableWidth = maximumClippingWidth;
			if ((_state$middlewareData2 = state.middlewareData.shift) != null && _state$middlewareData2.enabled.y) availableHeight = maximumClippingHeight;
			if (noShift && !alignment) {
				const xMin = max(overflow.left, 0);
				const xMax = max(overflow.right, 0);
				const yMin = max(overflow.top, 0);
				const yMax = max(overflow.bottom, 0);
				if (isYAxis) availableWidth = width - 2 * (xMin !== 0 || xMax !== 0 ? xMin + xMax : max(overflow.left, overflow.right));
				else availableHeight = height - 2 * (yMin !== 0 || yMax !== 0 ? yMin + yMax : max(overflow.top, overflow.bottom));
			}
			await apply({
				...state,
				availableWidth,
				availableHeight
			});
			const nextDimensions = await platform.getDimensions(elements.floating);
			if (width !== nextDimensions.width || height !== nextDimensions.height) return { reset: { rects: true } };
			return {};
		}
	};
};
function n$1(t) {
	var e;
	return (null == (e = t.ownerDocument) ? void 0 : e.defaultView) || window;
}
function o(t) {
	return n$1(t).getComputedStyle(t);
}
const i = Math.min, r = Math.max, l = Math.round;
function c$1(t) {
	const e = o(t);
	let n$2 = parseFloat(e.width), i$1 = parseFloat(e.height);
	const r$1 = t.offsetWidth, c$2 = t.offsetHeight, s$1 = l(n$2) !== r$1 || l(i$1) !== c$2;
	return s$1 && (n$2 = r$1, i$1 = c$2), {
		width: n$2,
		height: i$1,
		fallback: s$1
	};
}
function s(t) {
	return h$2(t) ? (t.nodeName || "").toLowerCase() : "";
}
let f;
function u() {
	if (f) return f;
	const t = navigator.userAgentData;
	return t && Array.isArray(t.brands) ? (f = t.brands.map((t$1) => t$1.brand + "/" + t$1.version).join(" "), f) : navigator.userAgent;
}
function a(t) {
	return t instanceof n$1(t).HTMLElement;
}
function d$1(t) {
	return t instanceof n$1(t).Element;
}
function h$2(t) {
	return t instanceof n$1(t).Node;
}
function p(t) {
	if ("undefined" == typeof ShadowRoot) return !1;
	return t instanceof n$1(t).ShadowRoot || t instanceof ShadowRoot;
}
function g$1(t) {
	const { overflow: e, overflowX: n$2, overflowY: i$1, display: r$1 } = o(t);
	return /auto|scroll|overlay|hidden|clip/.test(e + i$1 + n$2) && !["inline", "contents"].includes(r$1);
}
function m$1(t) {
	return [
		"table",
		"td",
		"th"
	].includes(s(t));
}
function y$1(t) {
	const e = /firefox/i.test(u()), n$2 = o(t), i$1 = n$2.backdropFilter || n$2.WebkitBackdropFilter;
	return "none" !== n$2.transform || "none" !== n$2.perspective || !!i$1 && "none" !== i$1 || e && "filter" === n$2.willChange || e && !!n$2.filter && "none" !== n$2.filter || ["transform", "perspective"].some((t$1) => n$2.willChange.includes(t$1)) || [
		"paint",
		"layout",
		"strict",
		"content"
	].some((t$1) => {
		const e$1 = n$2.contain;
		return null != e$1 && e$1.includes(t$1);
	});
}
function x$1() {
	return !/^((?!chrome|android).)*safari/i.test(u());
}
function w(t) {
	return [
		"html",
		"body",
		"#document"
	].includes(s(t));
}
function v(t) {
	return d$1(t) ? t : t.contextElement;
}
const b$1 = {
	x: 1,
	y: 1
};
function L(t) {
	const e = v(t);
	if (!a(e)) return b$1;
	const n$2 = e.getBoundingClientRect(), { width: o$1, height: i$1, fallback: r$1 } = c$1(e);
	let s$1 = (r$1 ? l(n$2.width) : n$2.width) / o$1, f$1 = (r$1 ? l(n$2.height) : n$2.height) / i$1;
	return s$1 && Number.isFinite(s$1) || (s$1 = 1), f$1 && Number.isFinite(f$1) || (f$1 = 1), {
		x: s$1,
		y: f$1
	};
}
function E$1(t, e, o$1, i$1) {
	var r$1, l$1;
	void 0 === e && (e = !1), void 0 === o$1 && (o$1 = !1);
	const c$2 = t.getBoundingClientRect(), s$1 = v(t);
	let f$1 = b$1;
	e && (i$1 ? d$1(i$1) && (f$1 = L(i$1)) : f$1 = L(t));
	const u$1 = s$1 ? n$1(s$1) : window, a$1 = !x$1() && o$1;
	let h$3 = (c$2.left + (a$1 && (null == (r$1 = u$1.visualViewport) ? void 0 : r$1.offsetLeft) || 0)) / f$1.x, p$1 = (c$2.top + (a$1 && (null == (l$1 = u$1.visualViewport) ? void 0 : l$1.offsetTop) || 0)) / f$1.y, g$2 = c$2.width / f$1.x, m$2 = c$2.height / f$1.y;
	if (s$1) {
		const t$1 = n$1(s$1), e$1 = i$1 && d$1(i$1) ? n$1(i$1) : i$1;
		let o$2 = t$1.frameElement;
		for (; o$2 && i$1 && e$1 !== t$1;) {
			const t$2 = L(o$2), e$2 = o$2.getBoundingClientRect(), i$2 = getComputedStyle(o$2);
			e$2.x += (o$2.clientLeft + parseFloat(i$2.paddingLeft)) * t$2.x, e$2.y += (o$2.clientTop + parseFloat(i$2.paddingTop)) * t$2.y, h$3 *= t$2.x, p$1 *= t$2.y, g$2 *= t$2.x, m$2 *= t$2.y, h$3 += e$2.x, p$1 += e$2.y, o$2 = n$1(o$2).frameElement;
		}
	}
	return {
		width: g$2,
		height: m$2,
		top: p$1,
		right: h$3 + g$2,
		bottom: p$1 + m$2,
		left: h$3,
		x: h$3,
		y: p$1
	};
}
function R(t) {
	return ((h$2(t) ? t.ownerDocument : t.document) || window.document).documentElement;
}
function T(t) {
	return d$1(t) ? {
		scrollLeft: t.scrollLeft,
		scrollTop: t.scrollTop
	} : {
		scrollLeft: t.pageXOffset,
		scrollTop: t.pageYOffset
	};
}
function C$1(t) {
	return E$1(R(t)).left + T(t).scrollLeft;
}
function F(t) {
	if ("html" === s(t)) return t;
	const e = t.assignedSlot || t.parentNode || p(t) && t.host || R(t);
	return p(e) ? e.host : e;
}
function W(t) {
	const e = F(t);
	return w(e) ? e.ownerDocument.body : a(e) && g$1(e) ? e : W(e);
}
function D(t, e) {
	var o$1;
	void 0 === e && (e = []);
	const i$1 = W(t), r$1 = i$1 === (null == (o$1 = t.ownerDocument) ? void 0 : o$1.body), l$1 = n$1(i$1);
	return r$1 ? e.concat(l$1, l$1.visualViewport || [], g$1(i$1) ? i$1 : []) : e.concat(i$1, D(i$1));
}
function S$1(e, i$1, l$1) {
	return "viewport" === i$1 ? rectToClientRect(function(t, e$1) {
		const o$1 = n$1(t), i$2 = R(t), r$1 = o$1.visualViewport;
		let l$2 = i$2.clientWidth, c$2 = i$2.clientHeight, s$1 = 0, f$1 = 0;
		if (r$1) {
			l$2 = r$1.width, c$2 = r$1.height;
			const t$1 = x$1();
			(t$1 || !t$1 && "fixed" === e$1) && (s$1 = r$1.offsetLeft, f$1 = r$1.offsetTop);
		}
		return {
			width: l$2,
			height: c$2,
			x: s$1,
			y: f$1
		};
	}(e, l$1)) : d$1(i$1) ? rectToClientRect(function(t, e$1) {
		const n$2 = E$1(t, !0, "fixed" === e$1), o$1 = n$2.top + t.clientTop, i$2 = n$2.left + t.clientLeft, r$1 = a(t) ? L(t) : {
			x: 1,
			y: 1
		};
		return {
			width: t.clientWidth * r$1.x,
			height: t.clientHeight * r$1.y,
			x: i$2 * r$1.x,
			y: o$1 * r$1.y
		};
	}(i$1, l$1)) : rectToClientRect(function(t) {
		const e$1 = R(t), n$2 = T(t), i$2 = t.ownerDocument.body, l$2 = r(e$1.scrollWidth, e$1.clientWidth, i$2.scrollWidth, i$2.clientWidth), c$2 = r(e$1.scrollHeight, e$1.clientHeight, i$2.scrollHeight, i$2.clientHeight);
		let s$1 = -n$2.scrollLeft + C$1(t);
		const f$1 = -n$2.scrollTop;
		return "rtl" === o(i$2).direction && (s$1 += r(e$1.clientWidth, i$2.clientWidth) - l$2), {
			width: l$2,
			height: c$2,
			x: s$1,
			y: f$1
		};
	}(R(e)));
}
function A(t) {
	return a(t) && "fixed" !== o(t).position ? t.offsetParent : null;
}
function H$1(t) {
	const e = n$1(t);
	let i$1 = A(t);
	for (; i$1 && m$1(i$1) && "static" === o(i$1).position;) i$1 = A(i$1);
	return i$1 && ("html" === s(i$1) || "body" === s(i$1) && "static" === o(i$1).position && !y$1(i$1)) ? e : i$1 || function(t$1) {
		let e$1 = F(t$1);
		for (; a(e$1) && !w(e$1);) {
			if (y$1(e$1)) return e$1;
			e$1 = F(e$1);
		}
		return null;
	}(t) || e;
}
function O(t, e, n$2) {
	const o$1 = a(e), i$1 = R(e), r$1 = E$1(t, !0, "fixed" === n$2, e);
	let l$1 = {
		scrollLeft: 0,
		scrollTop: 0
	};
	const c$2 = {
		x: 0,
		y: 0
	};
	if (o$1 || !o$1 && "fixed" !== n$2) if (("body" !== s(e) || g$1(i$1)) && (l$1 = T(e)), a(e)) {
		const t$1 = E$1(e, !0);
		c$2.x = t$1.x + e.clientLeft, c$2.y = t$1.y + e.clientTop;
	} else i$1 && (c$2.x = C$1(i$1));
	return {
		x: r$1.left + l$1.scrollLeft - c$2.x,
		y: r$1.top + l$1.scrollTop - c$2.y,
		width: r$1.width,
		height: r$1.height
	};
}
const P = {
	getClippingRect: function(t) {
		let { element: e, boundary: n$2, rootBoundary: l$1, strategy: c$2 } = t;
		const f$1 = "clippingAncestors" === n$2 ? function(t$1, e$1) {
			const n$3 = e$1.get(t$1);
			if (n$3) return n$3;
			let i$1 = D(t$1).filter((t$2) => d$1(t$2) && "body" !== s(t$2)), r$1 = null;
			const l$2 = "fixed" === o(t$1).position;
			let c$3 = l$2 ? F(t$1) : t$1;
			for (; d$1(c$3) && !w(c$3);) {
				const t$2 = o(c$3), e$2 = y$1(c$3);
				(l$2 ? e$2 || r$1 : e$2 || "static" !== t$2.position || !r$1 || !["absolute", "fixed"].includes(r$1.position)) ? r$1 = t$2 : i$1 = i$1.filter((t$3) => t$3 !== c$3), c$3 = F(c$3);
			}
			return e$1.set(t$1, i$1), i$1;
		}(e, this._c) : [].concat(n$2), u$1 = [...f$1, l$1], a$1 = u$1[0], h$3 = u$1.reduce((t$1, n$3) => {
			const o$1 = S$1(e, n$3, c$2);
			return t$1.top = r(o$1.top, t$1.top), t$1.right = i(o$1.right, t$1.right), t$1.bottom = i(o$1.bottom, t$1.bottom), t$1.left = r(o$1.left, t$1.left), t$1;
		}, S$1(e, a$1, c$2));
		return {
			width: h$3.right - h$3.left,
			height: h$3.bottom - h$3.top,
			x: h$3.left,
			y: h$3.top
		};
	},
	convertOffsetParentRelativeRectToViewportRelativeRect: function(t) {
		let { rect: e, offsetParent: n$2, strategy: o$1 } = t;
		const i$1 = a(n$2), r$1 = R(n$2);
		if (n$2 === r$1) return e;
		let l$1 = {
			scrollLeft: 0,
			scrollTop: 0
		}, c$2 = {
			x: 1,
			y: 1
		};
		const f$1 = {
			x: 0,
			y: 0
		};
		if ((i$1 || !i$1 && "fixed" !== o$1) && (("body" !== s(n$2) || g$1(r$1)) && (l$1 = T(n$2)), a(n$2))) {
			const t$1 = E$1(n$2);
			c$2 = L(n$2), f$1.x = t$1.x + n$2.clientLeft, f$1.y = t$1.y + n$2.clientTop;
		}
		return {
			width: e.width * c$2.x,
			height: e.height * c$2.y,
			x: e.x * c$2.x - l$1.scrollLeft * c$2.x + f$1.x,
			y: e.y * c$2.y - l$1.scrollTop * c$2.y + f$1.y
		};
	},
	isElement: d$1,
	getDimensions: function(t) {
		return a(t) ? c$1(t) : t.getBoundingClientRect();
	},
	getOffsetParent: H$1,
	getDocumentElement: R,
	getScale: L,
	async getElementRects(t) {
		let { reference: e, floating: n$2, strategy: o$1 } = t;
		const i$1 = this.getOffsetParent || H$1, r$1 = this.getDimensions;
		return {
			reference: O(e, await i$1(n$2), o$1),
			floating: {
				x: 0,
				y: 0,
				...await r$1(n$2)
			}
		};
	},
	getClientRects: (t) => Array.from(t.getClientRects()),
	isRTL: (t) => "rtl" === o(t).direction
};
const B$1 = (t, n$2, o$1) => {
	const i$1 = new Map(), r$1 = {
		platform: P,
		...o$1
	}, l$1 = {
		...r$1.platform,
		_c: i$1
	};
	return computePosition(t, n$2, {
		...r$1,
		platform: l$1
	});
};
const h$1 = {
	disabled: !1,
	distance: 5,
	skidding: 0,
	container: "body",
	boundary: void 0,
	instantMove: !1,
	disposeTimeout: 150,
	popperTriggers: [],
	strategy: "absolute",
	preventOverflow: !0,
	flip: !0,
	shift: !0,
	overflowPadding: 0,
	arrowPadding: 0,
	arrowOverflow: !0,
	autoHideOnMousedown: !1,
	themes: {
		tooltip: {
			placement: "top",
			triggers: [
				"hover",
				"focus",
				"touch"
			],
			hideTriggers: (e) => [...e, "click"],
			delay: {
				show: 200,
				hide: 0
			},
			handleResize: !1,
			html: !1,
			loadingContent: "..."
		},
		dropdown: {
			placement: "bottom",
			triggers: ["click"],
			delay: 0,
			handleResize: !0,
			autoHide: !0
		},
		menu: {
			$extend: "dropdown",
			triggers: ["hover", "focus"],
			popperTriggers: ["hover"],
			delay: {
				show: 0,
				hide: 400
			}
		}
	}
};
function S(e, t) {
	let o$1 = h$1.themes[e] || {}, i$1;
	do
		i$1 = o$1[t], typeof i$1 > "u" ? o$1.$extend ? o$1 = h$1.themes[o$1.$extend] || {} : (o$1 = null, i$1 = h$1[t]) : o$1 = null;
	while (o$1);
	return i$1;
}
function Ze(e) {
	const t = [e];
	let o$1 = h$1.themes[e] || {};
	do
		o$1.$extend && !o$1.$resetCss ? (t.push(o$1.$extend), o$1 = h$1.themes[o$1.$extend] || {}) : o$1 = null;
	while (o$1);
	return t.map((i$1) => `v-popper--theme-${i$1}`);
}
function re(e) {
	const t = [e];
	let o$1 = h$1.themes[e] || {};
	do
		o$1.$extend ? (t.push(o$1.$extend), o$1 = h$1.themes[o$1.$extend] || {}) : o$1 = null;
	while (o$1);
	return t;
}
let $ = !1;
if (typeof window < "u") {
	$ = !1;
	try {
		const e = Object.defineProperty({}, "passive", { get() {
			$ = !0;
		} });
		window.addEventListener("test", null, e);
	} catch {}
}
let _e = !1;
typeof window < "u" && typeof navigator < "u" && (_e = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream);
const Te = [
	"auto",
	"top",
	"bottom",
	"left",
	"right"
].reduce((e, t) => e.concat([
	t,
	`${t}-start`,
	`${t}-end`
]), []), pe = {
	hover: "mouseenter",
	focus: "focus",
	click: "click",
	touch: "touchstart",
	pointer: "pointerdown"
}, ae = {
	hover: "mouseleave",
	focus: "blur",
	click: "click",
	touch: "touchend",
	pointer: "pointerup"
};
function de(e, t) {
	const o$1 = e.indexOf(t);
	o$1 !== -1 && e.splice(o$1, 1);
}
function G() {
	return new Promise((e) => requestAnimationFrame(() => {
		requestAnimationFrame(e);
	}));
}
const d = [];
let g = null;
const le = {};
function he(e) {
	let t = le[e];
	return t || (t = le[e] = []), t;
}
let Y = function() {};
typeof window < "u" && (Y = window.Element);
function n(e) {
	return function(t) {
		return S(t.theme, e);
	};
}
const q = "__floating-vue__popper", Q = () => defineComponent({
	name: "VPopper",
	provide() {
		return { [q]: { parentPopper: this } };
	},
	inject: { [q]: { default: null } },
	props: {
		theme: {
			type: String,
			required: !0
		},
		targetNodes: {
			type: Function,
			required: !0
		},
		referenceNode: {
			type: Function,
			default: null
		},
		popperNode: {
			type: Function,
			required: !0
		},
		shown: {
			type: Boolean,
			default: !1
		},
		showGroup: {
			type: String,
			default: null
		},
		ariaId: { default: null },
		disabled: {
			type: Boolean,
			default: n("disabled")
		},
		positioningDisabled: {
			type: Boolean,
			default: n("positioningDisabled")
		},
		placement: {
			type: String,
			default: n("placement"),
			validator: (e) => Te.includes(e)
		},
		delay: {
			type: [
				String,
				Number,
				Object
			],
			default: n("delay")
		},
		distance: {
			type: [Number, String],
			default: n("distance")
		},
		skidding: {
			type: [Number, String],
			default: n("skidding")
		},
		triggers: {
			type: Array,
			default: n("triggers")
		},
		showTriggers: {
			type: [Array, Function],
			default: n("showTriggers")
		},
		hideTriggers: {
			type: [Array, Function],
			default: n("hideTriggers")
		},
		popperTriggers: {
			type: Array,
			default: n("popperTriggers")
		},
		popperShowTriggers: {
			type: [Array, Function],
			default: n("popperShowTriggers")
		},
		popperHideTriggers: {
			type: [Array, Function],
			default: n("popperHideTriggers")
		},
		container: {
			type: [
				String,
				Object,
				Y,
				Boolean
			],
			default: n("container")
		},
		boundary: {
			type: [String, Y],
			default: n("boundary")
		},
		strategy: {
			type: String,
			validator: (e) => ["absolute", "fixed"].includes(e),
			default: n("strategy")
		},
		autoHide: {
			type: [Boolean, Function],
			default: n("autoHide")
		},
		handleResize: {
			type: Boolean,
			default: n("handleResize")
		},
		instantMove: {
			type: Boolean,
			default: n("instantMove")
		},
		eagerMount: {
			type: Boolean,
			default: n("eagerMount")
		},
		popperClass: {
			type: [
				String,
				Array,
				Object
			],
			default: n("popperClass")
		},
		computeTransformOrigin: {
			type: Boolean,
			default: n("computeTransformOrigin")
		},
		autoMinSize: {
			type: Boolean,
			default: n("autoMinSize")
		},
		autoSize: {
			type: [Boolean, String],
			default: n("autoSize")
		},
		autoMaxSize: {
			type: Boolean,
			default: n("autoMaxSize")
		},
		autoBoundaryMaxSize: {
			type: Boolean,
			default: n("autoBoundaryMaxSize")
		},
		preventOverflow: {
			type: Boolean,
			default: n("preventOverflow")
		},
		overflowPadding: {
			type: [Number, String],
			default: n("overflowPadding")
		},
		arrowPadding: {
			type: [Number, String],
			default: n("arrowPadding")
		},
		arrowOverflow: {
			type: Boolean,
			default: n("arrowOverflow")
		},
		flip: {
			type: Boolean,
			default: n("flip")
		},
		shift: {
			type: Boolean,
			default: n("shift")
		},
		shiftCrossAxis: {
			type: Boolean,
			default: n("shiftCrossAxis")
		},
		noAutoFocus: {
			type: Boolean,
			default: n("noAutoFocus")
		},
		disposeTimeout: {
			type: Number,
			default: n("disposeTimeout")
		}
	},
	emits: {
		show: () => !0,
		hide: () => !0,
		"update:shown": (e) => !0,
		"apply-show": () => !0,
		"apply-hide": () => !0,
		"close-group": () => !0,
		"close-directive": () => !0,
		"auto-hide": () => !0,
		resize: () => !0
	},
	data() {
		return {
			isShown: !1,
			isMounted: !1,
			skipTransition: !1,
			classes: {
				showFrom: !1,
				showTo: !1,
				hideFrom: !1,
				hideTo: !0
			},
			result: {
				x: 0,
				y: 0,
				placement: "",
				strategy: this.strategy,
				arrow: {
					x: 0,
					y: 0,
					centerOffset: 0
				},
				transformOrigin: null
			},
			randomId: `popper_${[Math.random(), Date.now()].map((e) => e.toString(36).substring(2, 10)).join("_")}`,
			shownChildren: /* @__PURE__ */ new Set(),
			lastAutoHide: !0,
			pendingHide: !1,
			containsGlobalTarget: !1,
			isDisposed: !0,
			mouseDownContains: !1
		};
	},
	computed: {
		popperId() {
			return this.ariaId != null ? this.ariaId : this.randomId;
		},
		shouldMountContent() {
			return this.eagerMount || this.isMounted;
		},
		slotData() {
			return {
				popperId: this.popperId,
				isShown: this.isShown,
				shouldMountContent: this.shouldMountContent,
				skipTransition: this.skipTransition,
				autoHide: typeof this.autoHide == "function" ? this.lastAutoHide : this.autoHide,
				show: this.show,
				hide: this.hide,
				handleResize: this.handleResize,
				onResize: this.onResize,
				classes: {
					...this.classes,
					popperClass: this.popperClass
				},
				result: this.positioningDisabled ? null : this.result,
				attrs: this.$attrs
			};
		},
		parentPopper() {
			var e;
			return (e = this[q]) == null ? void 0 : e.parentPopper;
		},
		hasPopperShowTriggerHover() {
			var e, t;
			return ((e = this.popperTriggers) == null ? void 0 : e.includes("hover")) || ((t = this.popperShowTriggers) == null ? void 0 : t.includes("hover"));
		}
	},
	watch: {
		shown: "$_autoShowHide",
		disabled(e) {
			e ? this.dispose() : this.init();
		},
		async container() {
			this.isShown && (this.$_ensureTeleport(), await this.$_computePosition());
		},
		triggers: {
			handler: "$_refreshListeners",
			deep: !0
		},
		positioningDisabled: "$_refreshListeners",
		...[
			"placement",
			"distance",
			"skidding",
			"boundary",
			"strategy",
			"overflowPadding",
			"arrowPadding",
			"preventOverflow",
			"shift",
			"shiftCrossAxis",
			"flip"
		].reduce((e, t) => (e[t] = "$_computePosition", e), {})
	},
	created() {
		this.autoMinSize && console.warn("[floating-vue] `autoMinSize` option is deprecated. Use `autoSize=\"min\"` instead."), this.autoMaxSize && console.warn("[floating-vue] `autoMaxSize` option is deprecated. Use `autoBoundaryMaxSize` instead.");
	},
	mounted() {
		this.init(), this.$_detachPopperNode();
	},
	activated() {
		this.$_autoShowHide();
	},
	deactivated() {
		this.hide();
	},
	beforeUnmount() {
		this.dispose();
	},
	methods: {
		show({ event: e = null, skipDelay: t = !1, force: o$1 = !1 } = {}) {
			var i$1, s$1;
			(i$1 = this.parentPopper) != null && i$1.lockedChild && this.parentPopper.lockedChild !== this || (this.pendingHide = !1, (o$1 || !this.disabled) && (((s$1 = this.parentPopper) == null ? void 0 : s$1.lockedChild) === this && (this.parentPopper.lockedChild = null), this.$_scheduleShow(e, t), this.$emit("show"), this.$_showFrameLocked = !0, requestAnimationFrame(() => {
				this.$_showFrameLocked = !1;
			})), this.$emit("update:shown", !0));
		},
		hide({ event: e = null, skipDelay: t = !1 } = {}) {
			var o$1;
			if (!this.$_hideInProgress) {
				if (this.shownChildren.size > 0) {
					this.pendingHide = !0;
					return;
				}
				if (this.hasPopperShowTriggerHover && this.$_isAimingPopper()) {
					this.parentPopper && (this.parentPopper.lockedChild = this, clearTimeout(this.parentPopper.lockedChildTimer), this.parentPopper.lockedChildTimer = setTimeout(() => {
						this.parentPopper.lockedChild === this && (this.parentPopper.lockedChild.hide({ skipDelay: t }), this.parentPopper.lockedChild = null);
					}, 1e3));
					return;
				}
				((o$1 = this.parentPopper) == null ? void 0 : o$1.lockedChild) === this && (this.parentPopper.lockedChild = null), this.pendingHide = !1, this.$_scheduleHide(e, t), this.$emit("hide"), this.$emit("update:shown", !1);
			}
		},
		init() {
			var e;
			this.isDisposed && (this.isDisposed = !1, this.isMounted = !1, this.$_events = [], this.$_preventShow = !1, this.$_referenceNode = ((e = this.referenceNode) == null ? void 0 : e.call(this)) ?? this.$el, this.$_targetNodes = this.targetNodes().filter((t) => t.nodeType === t.ELEMENT_NODE), this.$_popperNode = this.popperNode(), this.$_innerNode = this.$_popperNode.querySelector(".v-popper__inner"), this.$_arrowNode = this.$_popperNode.querySelector(".v-popper__arrow-container"), this.$_swapTargetAttrs("title", "data-original-title"), this.$_detachPopperNode(), this.triggers.length && this.$_addEventListeners(), this.shown && this.show());
		},
		dispose() {
			this.isDisposed || (this.isDisposed = !0, this.$_removeEventListeners(), this.hide({ skipDelay: !0 }), this.$_detachPopperNode(), this.isMounted = !1, this.isShown = !1, this.$_updateParentShownChildren(!1), this.$_swapTargetAttrs("data-original-title", "title"));
		},
		async onResize() {
			this.isShown && (await this.$_computePosition(), this.$emit("resize"));
		},
		async $_computePosition() {
			if (this.isDisposed || this.positioningDisabled) return;
			const e = {
				strategy: this.strategy,
				middleware: []
			};
			(this.distance || this.skidding) && e.middleware.push(offset({
				mainAxis: this.distance,
				crossAxis: this.skidding
			}));
			const t = this.placement.startsWith("auto");
			if (t ? e.middleware.push(autoPlacement({ alignment: this.placement.split("-")[1] ?? "" })) : e.placement = this.placement, this.preventOverflow && (this.shift && e.middleware.push(shift({
				padding: this.overflowPadding,
				boundary: this.boundary,
				crossAxis: this.shiftCrossAxis
			})), !t && this.flip && e.middleware.push(flip({
				padding: this.overflowPadding,
				boundary: this.boundary
			}))), e.middleware.push(arrow({
				element: this.$_arrowNode,
				padding: this.arrowPadding
			})), this.arrowOverflow && e.middleware.push({
				name: "arrowOverflow",
				fn: ({ placement: i$1, rects: s$1, middlewareData: r$1 }) => {
					let p$1;
					const { centerOffset: a$1 } = r$1.arrow;
					return i$1.startsWith("top") || i$1.startsWith("bottom") ? p$1 = Math.abs(a$1) > s$1.reference.width / 2 : p$1 = Math.abs(a$1) > s$1.reference.height / 2, { data: { overflow: p$1 } };
				}
			}), this.autoMinSize || this.autoSize) {
				const i$1 = this.autoSize ? this.autoSize : this.autoMinSize ? "min" : null;
				e.middleware.push({
					name: "autoSize",
					fn: ({ rects: s$1, placement: r$1, middlewareData: p$1 }) => {
						var u$1;
						if ((u$1 = p$1.autoSize) != null && u$1.skip) return {};
						let a$1, l$1;
						return r$1.startsWith("top") || r$1.startsWith("bottom") ? a$1 = s$1.reference.width : l$1 = s$1.reference.height, this.$_innerNode.style[i$1 === "min" ? "minWidth" : i$1 === "max" ? "maxWidth" : "width"] = a$1 != null ? `${a$1}px` : null, this.$_innerNode.style[i$1 === "min" ? "minHeight" : i$1 === "max" ? "maxHeight" : "height"] = l$1 != null ? `${l$1}px` : null, {
							data: { skip: !0 },
							reset: { rects: !0 }
						};
					}
				});
			}
			(this.autoMaxSize || this.autoBoundaryMaxSize) && (this.$_innerNode.style.maxWidth = null, this.$_innerNode.style.maxHeight = null, e.middleware.push(size({
				boundary: this.boundary,
				padding: this.overflowPadding,
				apply: ({ availableWidth: i$1, availableHeight: s$1 }) => {
					this.$_innerNode.style.maxWidth = i$1 != null ? `${i$1}px` : null, this.$_innerNode.style.maxHeight = s$1 != null ? `${s$1}px` : null;
				}
			})));
			const o$1 = await B$1(this.$_referenceNode, this.$_popperNode, e);
			Object.assign(this.result, {
				x: o$1.x,
				y: o$1.y,
				placement: o$1.placement,
				strategy: o$1.strategy,
				arrow: {
					...o$1.middlewareData.arrow,
					...o$1.middlewareData.arrowOverflow
				}
			});
		},
		$_scheduleShow(e, t = !1) {
			if (this.$_updateParentShownChildren(!0), this.$_hideInProgress = !1, clearTimeout(this.$_scheduleTimer), g && this.instantMove && g.instantMove && g !== this.parentPopper) {
				g.$_applyHide(!0), this.$_applyShow(!0);
				return;
			}
			t ? this.$_applyShow() : this.$_scheduleTimer = setTimeout(this.$_applyShow.bind(this), this.$_computeDelay("show"));
		},
		$_scheduleHide(e, t = !1) {
			if (this.shownChildren.size > 0) {
				this.pendingHide = !0;
				return;
			}
			this.$_updateParentShownChildren(!1), this.$_hideInProgress = !0, clearTimeout(this.$_scheduleTimer), this.isShown && (g = this), t ? this.$_applyHide() : this.$_scheduleTimer = setTimeout(this.$_applyHide.bind(this), this.$_computeDelay("hide"));
		},
		$_computeDelay(e) {
			const t = this.delay;
			return parseInt(t && t[e] || t || 0);
		},
		async $_applyShow(e = !1) {
			clearTimeout(this.$_disposeTimer), clearTimeout(this.$_scheduleTimer), this.skipTransition = e, !this.isShown && (this.$_ensureTeleport(), await G(), await this.$_computePosition(), await this.$_applyShowEffect(), this.positioningDisabled || this.$_registerEventListeners([...D(this.$_referenceNode), ...D(this.$_popperNode)], "scroll", () => {
				this.$_computePosition();
			}));
		},
		async $_applyShowEffect() {
			if (this.$_hideInProgress) return;
			if (this.computeTransformOrigin) {
				const t = this.$_referenceNode.getBoundingClientRect(), o$1 = this.$_popperNode.querySelector(".v-popper__wrapper"), i$1 = o$1.parentNode.getBoundingClientRect(), s$1 = t.x + t.width / 2 - (i$1.left + o$1.offsetLeft), r$1 = t.y + t.height / 2 - (i$1.top + o$1.offsetTop);
				this.result.transformOrigin = `${s$1}px ${r$1}px`;
			}
			this.isShown = !0, this.$_applyAttrsToTarget({
				"aria-describedby": this.popperId,
				"data-popper-shown": ""
			});
			const e = this.showGroup;
			if (e) {
				let t;
				for (let o$1 = 0; o$1 < d.length; o$1++) t = d[o$1], t.showGroup !== e && (t.hide(), t.$emit("close-group"));
			}
			d.push(this), document.body.classList.add("v-popper--some-open");
			for (const t of re(this.theme)) he(t).push(this), document.body.classList.add(`v-popper--some-open--${t}`);
			this.$emit("apply-show"), this.classes.showFrom = !0, this.classes.showTo = !1, this.classes.hideFrom = !1, this.classes.hideTo = !1, await G(), this.classes.showFrom = !1, this.classes.showTo = !0, this.noAutoFocus || this.$_popperNode.focus();
		},
		async $_applyHide(e = !1) {
			if (this.shownChildren.size > 0) {
				this.pendingHide = !0, this.$_hideInProgress = !1;
				return;
			}
			if (clearTimeout(this.$_scheduleTimer), !this.isShown) return;
			this.skipTransition = e, de(d, this), d.length === 0 && document.body.classList.remove("v-popper--some-open");
			for (const o$1 of re(this.theme)) {
				const i$1 = he(o$1);
				de(i$1, this), i$1.length === 0 && document.body.classList.remove(`v-popper--some-open--${o$1}`);
			}
			g === this && (g = null), this.isShown = !1, this.$_applyAttrsToTarget({
				"aria-describedby": void 0,
				"data-popper-shown": void 0
			}), clearTimeout(this.$_disposeTimer);
			const t = this.disposeTimeout;
			t !== null && (this.$_disposeTimer = setTimeout(() => {
				this.$_popperNode && (this.$_detachPopperNode(), this.isMounted = !1);
			}, t)), this.$_removeEventListeners("scroll"), this.$emit("apply-hide"), this.classes.showFrom = !1, this.classes.showTo = !1, this.classes.hideFrom = !0, this.classes.hideTo = !1, await G(), this.classes.hideFrom = !1, this.classes.hideTo = !0;
		},
		$_autoShowHide() {
			this.shown ? this.show() : this.hide();
		},
		$_ensureTeleport() {
			if (this.isDisposed) return;
			let e = this.container;
			if (typeof e == "string" ? e = window.document.querySelector(e) : e === !1 && (e = this.$_targetNodes[0].parentNode), !e) throw new Error("No container for popover: " + this.container);
			e.appendChild(this.$_popperNode), this.isMounted = !0;
		},
		$_addEventListeners() {
			const e = (o$1) => {
				this.isShown && !this.$_hideInProgress || (o$1.usedByTooltip = !0, !this.$_preventShow && this.show({ event: o$1 }));
			};
			this.$_registerTriggerListeners(this.$_targetNodes, pe, this.triggers, this.showTriggers, e), this.$_registerTriggerListeners([this.$_popperNode], pe, this.popperTriggers, this.popperShowTriggers, e);
			const t = (o$1) => {
				o$1.usedByTooltip || this.hide({ event: o$1 });
			};
			this.$_registerTriggerListeners(this.$_targetNodes, ae, this.triggers, this.hideTriggers, t), this.$_registerTriggerListeners([this.$_popperNode], ae, this.popperTriggers, this.popperHideTriggers, t);
		},
		$_registerEventListeners(e, t, o$1) {
			this.$_events.push({
				targetNodes: e,
				eventType: t,
				handler: o$1
			}), e.forEach((i$1) => i$1.addEventListener(t, o$1, $ ? { passive: !0 } : void 0));
		},
		$_registerTriggerListeners(e, t, o$1, i$1, s$1) {
			let r$1 = o$1;
			i$1 != null && (r$1 = typeof i$1 == "function" ? i$1(r$1) : i$1), r$1.forEach((p$1) => {
				const a$1 = t[p$1];
				a$1 && this.$_registerEventListeners(e, a$1, s$1);
			});
		},
		$_removeEventListeners(e) {
			const t = [];
			this.$_events.forEach((o$1) => {
				const { targetNodes: i$1, eventType: s$1, handler: r$1 } = o$1;
				!e || e === s$1 ? i$1.forEach((p$1) => p$1.removeEventListener(s$1, r$1)) : t.push(o$1);
			}), this.$_events = t;
		},
		$_refreshListeners() {
			this.isDisposed || (this.$_removeEventListeners(), this.$_addEventListeners());
		},
		$_handleGlobalClose(e, t = !1) {
			this.$_showFrameLocked || (this.hide({ event: e }), e.closePopover ? this.$emit("close-directive") : this.$emit("auto-hide"), t && (this.$_preventShow = !0, setTimeout(() => {
				this.$_preventShow = !1;
			}, 300)));
		},
		$_detachPopperNode() {
			this.$_popperNode.parentNode && this.$_popperNode.parentNode.removeChild(this.$_popperNode);
		},
		$_swapTargetAttrs(e, t) {
			for (const o$1 of this.$_targetNodes) {
				const i$1 = o$1.getAttribute(e);
				i$1 && (o$1.removeAttribute(e), o$1.setAttribute(t, i$1));
			}
		},
		$_applyAttrsToTarget(e) {
			for (const t of this.$_targetNodes) for (const o$1 in e) {
				const i$1 = e[o$1];
				i$1 == null ? t.removeAttribute(o$1) : t.setAttribute(o$1, i$1);
			}
		},
		$_updateParentShownChildren(e) {
			let t = this.parentPopper;
			for (; t;) e ? t.shownChildren.add(this.randomId) : (t.shownChildren.delete(this.randomId), t.pendingHide && t.hide()), t = t.parentPopper;
		},
		$_isAimingPopper() {
			const e = this.$_referenceNode.getBoundingClientRect();
			if (y >= e.left && y <= e.right && _ >= e.top && _ <= e.bottom) {
				const t = this.$_popperNode.getBoundingClientRect(), o$1 = y - c, i$1 = _ - m, r$1 = t.left + t.width / 2 - c + (t.top + t.height / 2) - m + t.width + t.height, p$1 = c + o$1 * r$1, a$1 = m + i$1 * r$1;
				return C(c, m, p$1, a$1, t.left, t.top, t.left, t.bottom) || C(c, m, p$1, a$1, t.left, t.top, t.right, t.top) || C(c, m, p$1, a$1, t.right, t.top, t.right, t.bottom) || C(c, m, p$1, a$1, t.left, t.bottom, t.right, t.bottom);
			}
			return !1;
		}
	},
	render() {
		return this.$slots.default(this.slotData);
	}
});
if (typeof document < "u" && typeof window < "u") {
	if (_e) {
		const e = $ ? {
			passive: !0,
			capture: !0
		} : !0;
		document.addEventListener("touchstart", (t) => ue(t, !0), e), document.addEventListener("touchend", (t) => fe(t, !0), e);
	} else window.addEventListener("mousedown", (e) => ue(e, !1), !0), window.addEventListener("click", (e) => fe(e, !1), !0);
	window.addEventListener("resize", tt);
}
function ue(e, t) {
	if (h$1.autoHideOnMousedown) Pe(e, t);
	else for (let o$1 = 0; o$1 < d.length; o$1++) {
		const i$1 = d[o$1];
		try {
			i$1.mouseDownContains = i$1.popperNode().contains(e.target);
		} catch {}
	}
}
function fe(e, t) {
	h$1.autoHideOnMousedown || Pe(e, t);
}
function Pe(e, t) {
	const o$1 = {};
	for (let i$1 = d.length - 1; i$1 >= 0; i$1--) {
		const s$1 = d[i$1];
		try {
			const r$1 = s$1.containsGlobalTarget = s$1.mouseDownContains || s$1.popperNode().contains(e.target);
			s$1.pendingHide = !1, requestAnimationFrame(() => {
				if (s$1.pendingHide = !1, !o$1[s$1.randomId] && ce(s$1, r$1, e)) {
					if (s$1.$_handleGlobalClose(e, t), !e.closeAllPopover && e.closePopover && r$1) {
						let a$1 = s$1.parentPopper;
						for (; a$1;) o$1[a$1.randomId] = !0, a$1 = a$1.parentPopper;
						return;
					}
					let p$1 = s$1.parentPopper;
					for (; p$1 && ce(p$1, p$1.containsGlobalTarget, e);) {
						p$1.$_handleGlobalClose(e, t);
						p$1 = p$1.parentPopper;
					}
				}
			});
		} catch {}
	}
}
function ce(e, t, o$1) {
	return o$1.closeAllPopover || o$1.closePopover && t || et(e, o$1) && !t;
}
function et(e, t) {
	if (typeof e.autoHide == "function") {
		const o$1 = e.autoHide(t);
		return e.lastAutoHide = o$1, o$1;
	}
	return e.autoHide;
}
function tt() {
	for (let e = 0; e < d.length; e++) d[e].$_computePosition();
}
let c = 0, m = 0, y = 0, _ = 0;
typeof window < "u" && window.addEventListener("mousemove", (e) => {
	c = y, m = _, y = e.clientX, _ = e.clientY;
}, $ ? { passive: !0 } : void 0);
function C(e, t, o$1, i$1, s$1, r$1, p$1, a$1) {
	const l$1 = ((p$1 - s$1) * (t - r$1) - (a$1 - r$1) * (e - s$1)) / ((a$1 - r$1) * (o$1 - e) - (p$1 - s$1) * (i$1 - t)), u$1 = ((o$1 - e) * (t - r$1) - (i$1 - t) * (e - s$1)) / ((a$1 - r$1) * (o$1 - e) - (p$1 - s$1) * (i$1 - t));
	return l$1 >= 0 && l$1 <= 1 && u$1 >= 0 && u$1 <= 1;
}
const ot = { extends: Q() }, B = (e, t) => {
	const o$1 = e.__vccOpts || e;
	for (const [i$1, s$1] of t) o$1[i$1] = s$1;
	return o$1;
};
function it(e, t, o$1, i$1, s$1, r$1) {
	return openBlock(), createElementBlock("div", {
		ref: "reference",
		class: normalizeClass(["v-popper", { "v-popper--shown": e.slotData.isShown }])
	}, [renderSlot(e.$slots, "default", normalizeProps(guardReactiveProps(e.slotData)))], 2);
}
const st = /* @__PURE__ */ B(ot, [["render", it]]);
function nt() {
	var e = window.navigator.userAgent, t = e.indexOf("MSIE ");
	if (t > 0) return parseInt(e.substring(t + 5, e.indexOf(".", t)), 10);
	var o$1 = e.indexOf("Trident/");
	if (o$1 > 0) {
		var i$1 = e.indexOf("rv:");
		return parseInt(e.substring(i$1 + 3, e.indexOf(".", i$1)), 10);
	}
	var s$1 = e.indexOf("Edge/");
	return s$1 > 0 ? parseInt(e.substring(s$1 + 5, e.indexOf(".", s$1)), 10) : -1;
}
let z;
function X() {
	X.init || (X.init = !0, z = nt() !== -1);
}
var E = {
	name: "ResizeObserver",
	props: {
		emitOnMount: {
			type: Boolean,
			default: !1
		},
		ignoreWidth: {
			type: Boolean,
			default: !1
		},
		ignoreHeight: {
			type: Boolean,
			default: !1
		}
	},
	emits: ["notify"],
	mounted() {
		X(), nextTick(() => {
			this._w = this.$el.offsetWidth, this._h = this.$el.offsetHeight, this.emitOnMount && this.emitSize();
		});
		const e = document.createElement("object");
		this._resizeObject = e, e.setAttribute("aria-hidden", "true"), e.setAttribute("tabindex", -1), e.onload = this.addResizeHandlers, e.type = "text/html", z && this.$el.appendChild(e), e.data = "about:blank", z || this.$el.appendChild(e);
	},
	beforeUnmount() {
		this.removeResizeHandlers();
	},
	methods: {
		compareAndNotify() {
			(!this.ignoreWidth && this._w !== this.$el.offsetWidth || !this.ignoreHeight && this._h !== this.$el.offsetHeight) && (this._w = this.$el.offsetWidth, this._h = this.$el.offsetHeight, this.emitSize());
		},
		emitSize() {
			this.$emit("notify", {
				width: this._w,
				height: this._h
			});
		},
		addResizeHandlers() {
			this._resizeObject.contentDocument.defaultView.addEventListener("resize", this.compareAndNotify), this.compareAndNotify();
		},
		removeResizeHandlers() {
			this._resizeObject && this._resizeObject.onload && (!z && this._resizeObject.contentDocument && this._resizeObject.contentDocument.defaultView.removeEventListener("resize", this.compareAndNotify), this.$el.removeChild(this._resizeObject), this._resizeObject.onload = null, this._resizeObject = null);
		}
	}
};
const rt = /* @__PURE__ */ withScopeId("data-v-b329ee4c");
pushScopeId("data-v-b329ee4c");
const pt = {
	class: "resize-observer",
	tabindex: "-1"
};
popScopeId();
const at = /* @__PURE__ */ rt((e, t, o$1, i$1, s$1, r$1) => (openBlock(), createBlock("div", pt)));
E.render = at;
E.__scopeId = "data-v-b329ee4c";
E.__file = "src/components/ResizeObserver.vue";
const Z = (e = "theme") => ({ computed: { themeClass() {
	return Ze(this[e]);
} } }), dt = defineComponent({
	name: "VPopperContent",
	components: { ResizeObserver: E },
	mixins: [Z()],
	props: {
		popperId: String,
		theme: String,
		shown: Boolean,
		mounted: Boolean,
		skipTransition: Boolean,
		autoHide: Boolean,
		handleResize: Boolean,
		classes: Object,
		result: Object
	},
	emits: ["hide", "resize"],
	methods: { toPx(e) {
		return e != null && !isNaN(e) ? `${e}px` : null;
	} }
}), lt = [
	"id",
	"aria-hidden",
	"tabindex",
	"data-popper-placement"
], ht = {
	ref: "inner",
	class: "v-popper__inner"
}, ut = /* @__PURE__ */ createBaseVNode("div", { class: "v-popper__arrow-outer" }, null, -1), ft = /* @__PURE__ */ createBaseVNode("div", { class: "v-popper__arrow-inner" }, null, -1), ct = [ut, ft];
function mt(e, t, o$1, i$1, s$1, r$1) {
	const p$1 = resolveComponent("ResizeObserver");
	return openBlock(), createElementBlock("div", {
		id: e.popperId,
		ref: "popover",
		class: normalizeClass(["v-popper__popper", [
			e.themeClass,
			e.classes.popperClass,
			{
				"v-popper__popper--shown": e.shown,
				"v-popper__popper--hidden": !e.shown,
				"v-popper__popper--show-from": e.classes.showFrom,
				"v-popper__popper--show-to": e.classes.showTo,
				"v-popper__popper--hide-from": e.classes.hideFrom,
				"v-popper__popper--hide-to": e.classes.hideTo,
				"v-popper__popper--skip-transition": e.skipTransition,
				"v-popper__popper--arrow-overflow": e.result && e.result.arrow.overflow,
				"v-popper__popper--no-positioning": !e.result
			}
		]]),
		style: normalizeStyle(e.result ? {
			position: e.result.strategy,
			transform: `translate3d(${Math.round(e.result.x)}px,${Math.round(e.result.y)}px,0)`
		} : void 0),
		"aria-hidden": e.shown ? "false" : "true",
		tabindex: e.autoHide ? 0 : void 0,
		"data-popper-placement": e.result ? e.result.placement : void 0,
		onKeyup: t[2] || (t[2] = withKeys((a$1) => e.autoHide && e.$emit("hide"), ["esc"]))
	}, [createBaseVNode("div", {
		class: "v-popper__backdrop",
		onClick: t[0] || (t[0] = (a$1) => e.autoHide && e.$emit("hide"))
	}), createBaseVNode("div", {
		class: "v-popper__wrapper",
		style: normalizeStyle(e.result ? { transformOrigin: e.result.transformOrigin } : void 0)
	}, [createBaseVNode("div", ht, [e.mounted ? (openBlock(), createElementBlock(Fragment, { key: 0 }, [createBaseVNode("div", null, [renderSlot(e.$slots, "default")]), e.handleResize ? (openBlock(), createBlock(p$1, {
		key: 0,
		onNotify: t[1] || (t[1] = (a$1) => e.$emit("resize", a$1))
	})) : createCommentVNode("", !0)], 64)) : createCommentVNode("", !0)], 512), createBaseVNode("div", {
		ref: "arrow",
		class: "v-popper__arrow-container",
		style: normalizeStyle(e.result ? {
			left: e.toPx(e.result.arrow.x),
			top: e.toPx(e.result.arrow.y)
		} : void 0)
	}, ct, 4)], 4)], 46, lt);
}
const ee = /* @__PURE__ */ B(dt, [["render", mt]]), te = { methods: {
	show(...e) {
		return this.$refs.popper.show(...e);
	},
	hide(...e) {
		return this.$refs.popper.hide(...e);
	},
	dispose(...e) {
		return this.$refs.popper.dispose(...e);
	},
	onResize(...e) {
		return this.$refs.popper.onResize(...e);
	}
} };
let K = function() {};
typeof window < "u" && (K = window.Element);
const gt = defineComponent({
	name: "VPopperWrapper",
	components: {
		Popper: st,
		PopperContent: ee
	},
	mixins: [te, Z("finalTheme")],
	props: {
		theme: {
			type: String,
			default: null
		},
		referenceNode: {
			type: Function,
			default: null
		},
		shown: {
			type: Boolean,
			default: !1
		},
		showGroup: {
			type: String,
			default: null
		},
		ariaId: { default: null },
		disabled: {
			type: Boolean,
			default: void 0
		},
		positioningDisabled: {
			type: Boolean,
			default: void 0
		},
		placement: {
			type: String,
			default: void 0
		},
		delay: {
			type: [
				String,
				Number,
				Object
			],
			default: void 0
		},
		distance: {
			type: [Number, String],
			default: void 0
		},
		skidding: {
			type: [Number, String],
			default: void 0
		},
		triggers: {
			type: Array,
			default: void 0
		},
		showTriggers: {
			type: [Array, Function],
			default: void 0
		},
		hideTriggers: {
			type: [Array, Function],
			default: void 0
		},
		popperTriggers: {
			type: Array,
			default: void 0
		},
		popperShowTriggers: {
			type: [Array, Function],
			default: void 0
		},
		popperHideTriggers: {
			type: [Array, Function],
			default: void 0
		},
		container: {
			type: [
				String,
				Object,
				K,
				Boolean
			],
			default: void 0
		},
		boundary: {
			type: [String, K],
			default: void 0
		},
		strategy: {
			type: String,
			default: void 0
		},
		autoHide: {
			type: [Boolean, Function],
			default: void 0
		},
		handleResize: {
			type: Boolean,
			default: void 0
		},
		instantMove: {
			type: Boolean,
			default: void 0
		},
		eagerMount: {
			type: Boolean,
			default: void 0
		},
		popperClass: {
			type: [
				String,
				Array,
				Object
			],
			default: void 0
		},
		computeTransformOrigin: {
			type: Boolean,
			default: void 0
		},
		autoMinSize: {
			type: Boolean,
			default: void 0
		},
		autoSize: {
			type: [Boolean, String],
			default: void 0
		},
		autoMaxSize: {
			type: Boolean,
			default: void 0
		},
		autoBoundaryMaxSize: {
			type: Boolean,
			default: void 0
		},
		preventOverflow: {
			type: Boolean,
			default: void 0
		},
		overflowPadding: {
			type: [Number, String],
			default: void 0
		},
		arrowPadding: {
			type: [Number, String],
			default: void 0
		},
		arrowOverflow: {
			type: Boolean,
			default: void 0
		},
		flip: {
			type: Boolean,
			default: void 0
		},
		shift: {
			type: Boolean,
			default: void 0
		},
		shiftCrossAxis: {
			type: Boolean,
			default: void 0
		},
		noAutoFocus: {
			type: Boolean,
			default: void 0
		},
		disposeTimeout: {
			type: Number,
			default: void 0
		}
	},
	emits: {
		show: () => !0,
		hide: () => !0,
		"update:shown": (e) => !0,
		"apply-show": () => !0,
		"apply-hide": () => !0,
		"close-group": () => !0,
		"close-directive": () => !0,
		"auto-hide": () => !0,
		resize: () => !0
	},
	computed: { finalTheme() {
		return this.theme ?? this.$options.vPopperTheme;
	} },
	methods: { getTargetNodes() {
		return Array.from(this.$el.children).filter((e) => e !== this.$refs.popperContent.$el);
	} }
});
function wt(e, t, o$1, i$1, s$1, r$1) {
	const p$1 = resolveComponent("PopperContent"), a$1 = resolveComponent("Popper");
	return openBlock(), createBlock(a$1, mergeProps({ ref: "popper" }, e.$props, {
		theme: e.finalTheme,
		"target-nodes": e.getTargetNodes,
		"popper-node": () => e.$refs.popperContent.$el,
		class: [e.themeClass],
		onShow: t[0] || (t[0] = () => e.$emit("show")),
		onHide: t[1] || (t[1] = () => e.$emit("hide")),
		"onUpdate:shown": t[2] || (t[2] = (l$1) => e.$emit("update:shown", l$1)),
		onApplyShow: t[3] || (t[3] = () => e.$emit("apply-show")),
		onApplyHide: t[4] || (t[4] = () => e.$emit("apply-hide")),
		onCloseGroup: t[5] || (t[5] = () => e.$emit("close-group")),
		onCloseDirective: t[6] || (t[6] = () => e.$emit("close-directive")),
		onAutoHide: t[7] || (t[7] = () => e.$emit("auto-hide")),
		onResize: t[8] || (t[8] = () => e.$emit("resize"))
	}), {
		default: withCtx(({ popperId: l$1, isShown: u$1, shouldMountContent: L$1, skipTransition: D$1, autoHide: I, show: F$1, hide: v$1, handleResize: R$1, onResize: j, classes: V, result: Ee }) => [renderSlot(e.$slots, "default", {
			shown: u$1,
			show: F$1,
			hide: v$1
		}), createVNode(p$1, {
			ref: "popperContent",
			"popper-id": l$1,
			theme: e.finalTheme,
			shown: u$1,
			mounted: L$1,
			"skip-transition": D$1,
			"auto-hide": I,
			"handle-resize": R$1,
			classes: V,
			result: Ee,
			onHide: v$1,
			onResize: j
		}, {
			default: withCtx(() => [renderSlot(e.$slots, "popper", {
				shown: u$1,
				hide: v$1
			})]),
			_: 2
		}, 1032, [
			"popper-id",
			"theme",
			"shown",
			"mounted",
			"skip-transition",
			"auto-hide",
			"handle-resize",
			"classes",
			"result",
			"onHide",
			"onResize"
		])]),
		_: 3
	}, 16, [
		"theme",
		"target-nodes",
		"popper-node",
		"class"
	]);
}
const k = /* @__PURE__ */ B(gt, [["render", wt]]), Se = {
	...k,
	name: "VDropdown",
	vPopperTheme: "dropdown"
}, be = {
	...k,
	name: "VMenu",
	vPopperTheme: "menu"
}, Ce = {
	...k,
	name: "VTooltip",
	vPopperTheme: "tooltip"
}, $t = defineComponent({
	name: "VTooltipDirective",
	components: {
		Popper: Q(),
		PopperContent: ee
	},
	mixins: [te],
	inheritAttrs: !1,
	props: {
		theme: {
			type: String,
			default: "tooltip"
		},
		html: {
			type: Boolean,
			default: (e) => S(e.theme, "html")
		},
		content: {
			type: [
				String,
				Number,
				Function
			],
			default: null
		},
		loadingContent: {
			type: String,
			default: (e) => S(e.theme, "loadingContent")
		},
		targetNodes: {
			type: Function,
			required: !0
		}
	},
	data() {
		return { asyncContent: null };
	},
	computed: {
		isContentAsync() {
			return typeof this.content == "function";
		},
		loading() {
			return this.isContentAsync && this.asyncContent == null;
		},
		finalContent() {
			return this.isContentAsync ? this.loading ? this.loadingContent : this.asyncContent : this.content;
		}
	},
	watch: {
		content: {
			handler() {
				this.fetchContent(!0);
			},
			immediate: !0
		},
		async finalContent() {
			await this.$nextTick(), this.$refs.popper.onResize();
		}
	},
	created() {
		this.$_fetchId = 0;
	},
	methods: {
		fetchContent(e) {
			if (typeof this.content == "function" && this.$_isShown && (e || !this.$_loading && this.asyncContent == null)) {
				this.asyncContent = null, this.$_loading = !0;
				const t = ++this.$_fetchId, o$1 = this.content(this);
				o$1.then ? o$1.then((i$1) => this.onResult(t, i$1)) : this.onResult(t, o$1);
			}
		},
		onResult(e, t) {
			e === this.$_fetchId && (this.$_loading = !1, this.asyncContent = t);
		},
		onShow() {
			this.$_isShown = !0, this.fetchContent();
		},
		onHide() {
			this.$_isShown = !1;
		}
	}
}), vt = ["innerHTML"], yt = ["textContent"];
function _t(e, t, o$1, i$1, s$1, r$1) {
	const p$1 = resolveComponent("PopperContent"), a$1 = resolveComponent("Popper");
	return openBlock(), createBlock(a$1, mergeProps({ ref: "popper" }, e.$attrs, {
		theme: e.theme,
		"target-nodes": e.targetNodes,
		"popper-node": () => e.$refs.popperContent.$el,
		onApplyShow: e.onShow,
		onApplyHide: e.onHide
	}), {
		default: withCtx(({ popperId: l$1, isShown: u$1, shouldMountContent: L$1, skipTransition: D$1, autoHide: I, hide: F$1, handleResize: v$1, onResize: R$1, classes: j, result: V }) => [createVNode(p$1, {
			ref: "popperContent",
			class: normalizeClass({ "v-popper--tooltip-loading": e.loading }),
			"popper-id": l$1,
			theme: e.theme,
			shown: u$1,
			mounted: L$1,
			"skip-transition": D$1,
			"auto-hide": I,
			"handle-resize": v$1,
			classes: j,
			result: V,
			onHide: F$1,
			onResize: R$1
		}, {
			default: withCtx(() => [e.html ? (openBlock(), createElementBlock("div", {
				key: 0,
				innerHTML: e.finalContent
			}, null, 8, vt)) : (openBlock(), createElementBlock("div", {
				key: 1,
				textContent: toDisplayString(e.finalContent)
			}, null, 8, yt))]),
			_: 2
		}, 1032, [
			"class",
			"popper-id",
			"theme",
			"shown",
			"mounted",
			"skip-transition",
			"auto-hide",
			"handle-resize",
			"classes",
			"result",
			"onHide",
			"onResize"
		])]),
		_: 1
	}, 16, [
		"theme",
		"target-nodes",
		"popper-node",
		"onApplyShow",
		"onApplyHide"
	]);
}
const ze = /* @__PURE__ */ B($t, [["render", _t]]), Ae = "v-popper--has-tooltip";
function Tt(e, t) {
	let o$1 = e.placement;
	if (!o$1 && t) for (const i$1 of Te) t[i$1] && (o$1 = i$1);
	return o$1 || (o$1 = S(e.theme || "tooltip", "placement")), o$1;
}
function Ne(e, t, o$1) {
	let i$1;
	const s$1 = typeof t;
	return s$1 === "string" ? i$1 = { content: t } : t && s$1 === "object" ? i$1 = t : i$1 = { content: !1 }, i$1.placement = Tt(i$1, o$1), i$1.targetNodes = () => [e], i$1.referenceNode = () => e, i$1;
}
let x, b, Pt = 0;
function St() {
	if (x) return;
	b = ref([]), x = createApp({
		name: "VTooltipDirectiveApp",
		setup() {
			return { directives: b };
		},
		render() {
			return this.directives.map((t) => h(ze, {
				...t.options,
				shown: t.shown || t.options.shown,
				key: t.id
			}));
		},
		devtools: { hide: !0 }
	});
	const e = document.createElement("div");
	document.body.appendChild(e), x.mount(e);
}
function bt(e, t, o$1) {
	St();
	const i$1 = ref(Ne(e, t, o$1)), s$1 = ref(!1), r$1 = {
		id: Pt++,
		options: i$1,
		shown: s$1
	};
	return b.value.push(r$1), e.classList && e.classList.add(Ae), e.$_popper = {
		options: i$1,
		item: r$1,
		show() {
			s$1.value = !0;
		},
		hide() {
			s$1.value = !1;
		}
	};
}
function He(e) {
	if (e.$_popper) {
		const t = b.value.indexOf(e.$_popper.item);
		t !== -1 && b.value.splice(t, 1), delete e.$_popper, delete e.$_popperOldShown, delete e.$_popperMountTarget;
	}
	e.classList && e.classList.remove(Ae);
}
function me(e, { value: t, modifiers: o$1 }) {
	const i$1 = Ne(e, t, o$1);
	if (!i$1.content || S(i$1.theme || "tooltip", "disabled")) He(e);
	else {
		let s$1;
		e.$_popper ? (s$1 = e.$_popper, s$1.options.value = i$1) : s$1 = bt(e, t, o$1), typeof t.shown < "u" && t.shown !== e.$_popperOldShown && (e.$_popperOldShown = t.shown, t.shown ? s$1.show() : s$1.hide());
	}
}
const oe = {
	beforeMount: me,
	updated: me,
	beforeUnmount(e) {
		He(e);
	}
};
function ge(e) {
	e.addEventListener("mousedown", H), e.addEventListener("click", H), e.addEventListener("touchstart", Oe, $ ? { passive: !0 } : !1);
}
function we(e) {
	e.removeEventListener("mousedown", H), e.removeEventListener("click", H), e.removeEventListener("touchstart", Oe), e.removeEventListener("touchend", Me), e.removeEventListener("touchcancel", Be);
}
function H(e) {
	const t = e.currentTarget;
	e.closePopover = !t.$_vclosepopover_touch, e.closeAllPopover = t.$_closePopoverModifiers && !!t.$_closePopoverModifiers.all;
}
function Oe(e) {
	if (e.changedTouches.length === 1) {
		const t = e.currentTarget;
		t.$_vclosepopover_touch = !0;
		const o$1 = e.changedTouches[0];
		t.$_vclosepopover_touchPoint = o$1, t.addEventListener("touchend", Me), t.addEventListener("touchcancel", Be);
	}
}
function Me(e) {
	const t = e.currentTarget;
	if (t.$_vclosepopover_touch = !1, e.changedTouches.length === 1) {
		const o$1 = e.changedTouches[0], i$1 = t.$_vclosepopover_touchPoint;
		e.closePopover = Math.abs(o$1.screenY - i$1.screenY) < 20 && Math.abs(o$1.screenX - i$1.screenX) < 20, e.closeAllPopover = t.$_closePopoverModifiers && !!t.$_closePopoverModifiers.all;
	}
}
function Be(e) {
	const t = e.currentTarget;
	t.$_vclosepopover_touch = !1;
}
const ie = {
	beforeMount(e, { value: t, modifiers: o$1 }) {
		e.$_closePopoverModifiers = o$1, (typeof t > "u" || t) && ge(e);
	},
	updated(e, { value: t, oldValue: o$1, modifiers: i$1 }) {
		e.$_closePopoverModifiers = i$1, t !== o$1 && (typeof t > "u" || t ? ge(e) : we(e));
	},
	beforeUnmount(e) {
		we(e);
	}
}, Ht = h$1, Ot = oe, Mt = oe, Bt = ie, Et = ie, kt = Se, Lt = be, Dt = Q, It = ee, Ft = te, Rt = k, jt = Z, Vt = Ce, Wt = ze;
const _DRIVE_LETTER_START_RE = /^[A-Za-z]:\//;
function normalizeWindowsPath(input = "") {
	if (!input) return input;
	return input.replace(/\\/g, "/").replace(_DRIVE_LETTER_START_RE, (r$1) => r$1.toUpperCase());
}
const _IS_ABSOLUTE_RE = /^[/\\](?![/\\])|^[/\\]{2}(?!\.)|^[A-Za-z]:[/\\]/;
const _ROOT_FOLDER_RE = /^\/([A-Za-z]:)?$/;
function cwd() {
	if (typeof process !== "undefined" && typeof process.cwd === "function") return process.cwd().replace(/\\/g, "/");
	return "/";
}
const resolve = function(...arguments_) {
	arguments_ = arguments_.map((argument) => normalizeWindowsPath(argument));
	let resolvedPath = "";
	let resolvedAbsolute = false;
	for (let index = arguments_.length - 1; index >= -1 && !resolvedAbsolute; index--) {
		const path = index >= 0 ? arguments_[index] : cwd();
		if (!path || path.length === 0) continue;
		resolvedPath = `${path}/${resolvedPath}`;
		resolvedAbsolute = isAbsolute(path);
	}
	resolvedPath = normalizeString(resolvedPath, !resolvedAbsolute);
	if (resolvedAbsolute && !isAbsolute(resolvedPath)) return `/${resolvedPath}`;
	return resolvedPath.length > 0 ? resolvedPath : ".";
};
function normalizeString(path, allowAboveRoot) {
	let res = "";
	let lastSegmentLength = 0;
	let lastSlash = -1;
	let dots = 0;
	let char = null;
	for (let index = 0; index <= path.length; ++index) {
		if (index < path.length) char = path[index];
		else if (char === "/") break;
		else char = "/";
		if (char === "/") {
			if (lastSlash === index - 1 || dots === 1);
			else if (dots === 2) {
				if (res.length < 2 || lastSegmentLength !== 2 || res[res.length - 1] !== "." || res[res.length - 2] !== ".") {
					if (res.length > 2) {
						const lastSlashIndex = res.lastIndexOf("/");
						if (lastSlashIndex === -1) {
							res = "";
							lastSegmentLength = 0;
						} else {
							res = res.slice(0, lastSlashIndex);
							lastSegmentLength = res.length - 1 - res.lastIndexOf("/");
						}
						lastSlash = index;
						dots = 0;
						continue;
					} else if (res.length > 0) {
						res = "";
						lastSegmentLength = 0;
						lastSlash = index;
						dots = 0;
						continue;
					}
				}
				if (allowAboveRoot) {
					res += res.length > 0 ? "/.." : "..";
					lastSegmentLength = 2;
				}
			} else {
				if (res.length > 0) res += `/${path.slice(lastSlash + 1, index)}`;
				else res = path.slice(lastSlash + 1, index);
				lastSegmentLength = index - lastSlash - 1;
			}
			lastSlash = index;
			dots = 0;
		} else if (char === "." && dots !== -1) ++dots;
		else dots = -1;
	}
	return res;
}
const isAbsolute = function(p$1) {
	return _IS_ABSOLUTE_RE.test(p$1);
};
const relative = function(from, to) {
	const _from = resolve(from).replace(_ROOT_FOLDER_RE, "$1").split("/");
	const _to = resolve(to).replace(_ROOT_FOLDER_RE, "$1").split("/");
	if (_to[0][1] === ":" && _from[0][1] === ":" && _from[0] !== _to[0]) return _to.join("/");
	const _fromCopy = [..._from];
	for (const segment of _fromCopy) {
		if (_to[0] !== segment) break;
		_from.shift();
		_to.shift();
	}
	return [..._from.map(() => ".."), ..._to].join("/");
};
var ModuleId_vue_vue_type_script_setup_true_lang_default = /* @__PURE__ */ defineComponent({
	__name: "ModuleId",
	props: {
		id: {},
		badges: { type: Boolean },
		icon: {
			type: Boolean,
			default: true
		},
		module: { type: Boolean }
	},
	setup(__props) {
		const props = __props;
		const payload = usePayloadStore();
		const mod = computed(() => payload.modules.find((i$1) => i$1.id === props.id));
		const isVirtual = computed(() => mod.value?.virtual);
		const relativePath = computed(() => {
			if (!props.id) return "";
			let relate = relative(payload.root, props.id);
			if (!relate.startsWith(".")) relate = `./${relate}`;
			if (relate.startsWith("./")) return relate;
			if (relate.match(/^(?:\.\.\/){1,3}[^.]/)) return relate;
			return props.id;
		});
		const HighlightedPath = defineComponent({ render() {
			const parts = relativePath.value.split(/([/?&:])/g);
			let type = "start";
			const classes = parts.map(() => []);
			const nodes = parts.map((part) => {
				return h("span", { class: "" }, part);
			});
			parts.forEach((part, index) => {
				const _class = classes[index];
				if (part === "?") type = "query";
				if (type === "start") {
					if (part.match(/^\.+$/)) _class.push("op50");
					else if (part === "/") _class.push("op50");
					else if (part !== "/") type = "path";
				}
				if (type === "path") {
					if (part === "/" || part === "node_modules" || part.match(/^\.\w/)) _class.push("op75");
					if (part === ".pnpm") {
						classes[index + 2]?.push("op50");
						if (nodes[index + 2]) nodes[index + 2].children = "…";
					}
					if (part === ":") {
						if (nodes[index - 1]) {
							nodes[index - 1].props ||= {};
							nodes[index - 1].props.style ||= {};
							nodes[index - 1].props.style.color = getPluginColor(parts[index - 1]);
						}
						_class.push("op50");
					}
				}
				if (type === "query") if (part === "?" || part === "&") _class.push("text-orange-5 dark:text-orange-4");
				else _class.push("text-orange-9 dark:text-orange-2");
			});
			nodes.forEach((node, index) => {
				if (node.props) node.props.class = classes[index].join(" ");
			});
			return nodes;
		} });
		const gridStyles = computed(() => {
			if (!props.module) return "";
			const gridColumns = [];
			if (props.icon) gridColumns.push("min-content");
			if (props.module) gridColumns.push("minmax(0,1fr)");
			else gridColumns.push("100%");
			if (isVirtual.value) gridColumns.push("min-content");
			return `grid-template-columns: ${gridColumns.join(" ")};`;
		});
		const containerClass = computed(() => {
			return props.module ? "grid grid-rows-1 items-center gap-1" : "flex items-center";
		});
		return (_ctx, _cache) => {
			const _component_FileIcon = FileIcon_default;
			const _component_Badge = Badge_default;
			return _ctx.id ? withDirectives((openBlock(), createElementBlock("div", {
				key: 0,
				"my-auto": "",
				"text-sm": "",
				"font-mono": "",
				class: normalizeClass(containerClass.value),
				style: normalizeStyle(gridStyles.value)
			}, [
				_ctx.icon ? (openBlock(), createBlock(_component_FileIcon, {
					key: 0,
					filename: _ctx.id,
					"mr1.5": ""
				}, null, 8, ["filename"])) : createCommentVNode("", true),
				createBaseVNode("span", { class: normalizeClass({
					"overflow-hidden": _ctx.module,
					"text-truncate": _ctx.module
				}) }, [createVNode(unref(HighlightedPath))], 2),
				renderSlot(_ctx.$slots, "default"),
				isVirtual.value ? (openBlock(), createBlock(_component_Badge, {
					key: 1,
					class: "ml1",
					text: "virtual"
				})) : createCommentVNode("", true)
			], 6)), [[
				unref(Mt),
				{
					content: props.id,
					triggers: ["hover", "focus"],
					disabled: !_ctx.module
				},
				void 0,
				{ "bottom-start": true }
			]]) : createCommentVNode("", true);
		};
	}
});
var ModuleId_default = ModuleId_vue_vue_type_script_setup_true_lang_default;
const _hoisted_1 = {
	key: 0,
	class: "h-full"
};
const _hoisted_2 = {
	key: 0,
	"px-6": "",
	"py-4": "",
	italic: "",
	op50: ""
};
const _hoisted_3 = { key: 0 };
const _hoisted_4 = { key: 1 };
const _hoisted_5 = {
	key: 0,
	flex: "~ gap-1",
	"text-xs": ""
};
const _hoisted_6 = {
	flex: "~ auto gap-1",
	"of-hidden": ""
};
const _hoisted_7 = {
	key: 0,
	op20: ""
};
const _hoisted_8 = {
	"ws-nowrap": "",
	op50: ""
};
const _hoisted_9 = ["title"];
const _hoisted_10 = { flex: "~ none gap-1 wrap justify-end" };
var ModuleList_vue_vue_type_script_setup_true_lang_default = /* @__PURE__ */ defineComponent({
	__name: "ModuleList",
	props: { modules: {} },
	setup(__props) {
		const props = __props;
		const options = useOptionsStore();
		const payload = usePayloadStore();
		const route = useRoute();
		const { list, containerProps, wrapperProps } = useVirtualList(toRef(props, "modules"), { itemHeight: options.view.listMode === "detailed" ? 53 : 37 });
		return (_ctx, _cache) => {
			const _component_ModuleId = ModuleId_default;
			const _component_PluginName = PluginName_default;
			const _component_ByteSizeDisplay = ByteSizeDisplay_default;
			const _component_DurationDisplay = DurationDisplay_default;
			const _component_RouterLink = resolveComponent("RouterLink");
			return _ctx.modules ? (openBlock(), createElementBlock("div", _hoisted_1, [!_ctx.modules.length ? (openBlock(), createElementBlock("div", _hoisted_2, [unref(options).search.text ? (openBlock(), createElementBlock("div", _hoisted_3, " No search result ")) : (openBlock(), createElementBlock("div", _hoisted_4, [..._cache[0] || (_cache[0] = [
				createTextVNode(" No module recorded yet, visit ", -1),
				createBaseVNode("a", {
					href: "/",
					target: "_blank"
				}, "your app", -1),
				createTextVNode(" first and then refresh this page. ", -1)
			])]))])) : (openBlock(), createElementBlock("div", mergeProps({ key: 1 }, unref(containerProps), { class: "h-full" }), [createBaseVNode("div", normalizeProps(guardReactiveProps(unref(wrapperProps))), [(openBlock(true), createElementBlock(Fragment, null, renderList(unref(list), (m$2) => {
				return openBlock(), createBlock(_component_RouterLink, {
					key: `${unref(payload).query.vite}-${unref(payload).query.env}-${m$2.data.id}`,
					class: "block border-b border-main px-3 py-2 text-left text-sm font-mono hover:bg-active",
					to: {
						path: "/module",
						query: {
							...unref(route).query,
							id: m$2.data.id
						}
					}
				}, {
					default: withCtx(() => [createVNode(_component_ModuleId, {
						id: m$2.data.id,
						badges: "",
						"ws-nowrap": ""
					}, null, 8, ["id"]), unref(options).view.listMode === "detailed" ? (openBlock(), createElementBlock("div", _hoisted_5, [createBaseVNode("div", _hoisted_6, [(openBlock(true), createElementBlock(Fragment, null, renderList(m$2.data.plugins.slice(1).filter((plugin) => plugin.transform !== void 0), (i$1, idx) => {
						return openBlock(), createElementBlock(Fragment, { key: i$1 }, [idx !== 0 ? (openBlock(), createElementBlock("span", _hoisted_7, "|")) : createCommentVNode("", true), createBaseVNode("span", _hoisted_8, [createVNode(_component_PluginName, {
							name: i$1.name,
							compact: true
						}, null, 8, ["name"])])], 64);
					}), 128)), m$2.data.invokeCount > 2 ? (openBlock(), createElementBlock(Fragment, { key: 0 }, [_cache[1] || (_cache[1] = createBaseVNode("span", { op40: "" }, "·", -1)), createBaseVNode("span", {
						"text-green": "",
						title: `Transform invoked ${m$2.data.invokeCount} times`
					}, "x" + toDisplayString(m$2.data.invokeCount), 9, _hoisted_9)], 64)) : createCommentVNode("", true)]), createBaseVNode("div", _hoisted_10, [m$2.data.sourceSize && m$2.data.distSize ? (openBlock(), createElementBlock(Fragment, { key: 0 }, [
						createVNode(_component_ByteSizeDisplay, {
							op75: "",
							bytes: m$2.data.sourceSize
						}, null, 8, ["bytes"]),
						_cache[2] || (_cache[2] = createBaseVNode("span", {
							"i-carbon-arrow-right": "",
							op50: ""
						}, null, -1)),
						createVNode(_component_ByteSizeDisplay, {
							class: normalizeClass(m$2.data.distSize > m$2.data.sourceSize ? "status-yellow" : "status-green"),
							bytes: m$2.data.distSize
						}, null, 8, ["class", "bytes"]),
						_cache[3] || (_cache[3] = createBaseVNode("span", { op40: "" }, "|", -1))
					], 64)) : createCommentVNode("", true), createBaseVNode("span", null, [createVNode(_component_DurationDisplay, { duration: m$2.data.totalTime }, null, 8, ["duration"])])])])) : createCommentVNode("", true)]),
					_: 2
				}, 1032, ["to"]);
			}), 128))], 16)], 16))])) : createCommentVNode("", true);
		};
	}
});
var ModuleList_default = ModuleList_vue_vue_type_script_setup_true_lang_default;
export { ModuleId_default, ModuleList_default, kt };
