import * as t from "@babel/types";
import _template from "@babel/template";
import _syntaxJsx from "@babel/plugin-syntax-jsx";
import { addDefault, addNamed, addNamespace, isModule } from "@babel/helper-module-imports";
import ResolveType from "@vue/babel-plugin-resolve-type";
import { declare } from "@babel/helper-plugin-utils";
import { isHTMLTag, isSVGTag } from "@vue/shared";

//#region src/slotFlags.ts
var SlotFlags = /* @__PURE__ */ function(SlotFlags$1) {
	/**
	* Stable slots that only reference slot props or context state. The slot
	* can fully capture its own dependencies so when passed down the parent won't
	* need to force the child to update.
	*/
	SlotFlags$1[SlotFlags$1["STABLE"] = 1] = "STABLE";
	/**
	* Slots that reference scope variables (v-for or an outer slot prop), or
	* has conditional structure (v-if, v-for). The parent will need to force
	* the child to update because the slot does not fully capture its dependencies.
	*/
	SlotFlags$1[SlotFlags$1["DYNAMIC"] = 2] = "DYNAMIC";
	/**
	* `<slot/>` being forwarded into a child component. Whether the parent needs
	* to update the child is dependent on what kind of slots the parent itself
	* received. This has to be refined at runtime, when the child's vnode
	* is being created (in `normalizeChildren`)
	*/
	SlotFlags$1[SlotFlags$1["FORWARDED"] = 3] = "FORWARDED";
	return SlotFlags$1;
}(SlotFlags || {});
var slotFlags_default = SlotFlags;

//#endregion
//#region src/utils.ts
const FRAGMENT = "Fragment";
const KEEP_ALIVE = "KeepAlive";
/**
* create Identifier
* @param path NodePath
* @param state
* @param name string
* @returns MemberExpression
*/
const createIdentifier = (state, name) => state.get(name)();
/**
* Checks if string is describing a directive
* @param src string
*/
const isDirective = (src) => src.startsWith("v-") || src.startsWith("v") && src.length >= 2 && src[1] >= "A" && src[1] <= "Z";
/**
* Should transformed to slots
* @param tag string
* @returns boolean
*/
const shouldTransformedToSlots = (tag) => !(tag.match(RegExp(`^_?${FRAGMENT}\\d*$`)) || tag === KEEP_ALIVE);
/**
* Check if a Node is a component
*
* @param t
* @param path JSXOpeningElement
* @returns boolean
*/
const checkIsComponent = (path, state) => {
	const namePath = path.get("name");
	if (namePath.isJSXMemberExpression()) return shouldTransformedToSlots(namePath.node.property.name);
	const tag = namePath.node.name;
	return !state.opts.isCustomElement?.(tag) && shouldTransformedToSlots(tag) && !isHTMLTag(tag) && !isSVGTag(tag);
};
/**
* Transform JSXMemberExpression to MemberExpression
* @param path JSXMemberExpression
* @returns MemberExpression
*/
const transformJSXMemberExpression = (path) => {
	const objectPath = path.node.object;
	const propertyPath = path.node.property;
	const transformedObject = t.isJSXMemberExpression(objectPath) ? transformJSXMemberExpression(path.get("object")) : t.isJSXIdentifier(objectPath) ? t.identifier(objectPath.name) : t.nullLiteral();
	const transformedProperty = t.identifier(propertyPath.name);
	return t.memberExpression(transformedObject, transformedProperty);
};
/**
* Get tag (first attribute for h) from JSXOpeningElement
* @param path JSXElement
* @param state State
* @returns Identifier | StringLiteral | MemberExpression | CallExpression
*/
const getTag = (path, state) => {
	const namePath = path.get("openingElement").get("name");
	if (namePath.isJSXIdentifier()) {
		const { name } = namePath.node;
		if (!isHTMLTag(name) && !isSVGTag(name)) return name === FRAGMENT ? createIdentifier(state, FRAGMENT) : path.scope.hasBinding(name) ? t.identifier(name) : state.opts.isCustomElement?.(name) ? t.stringLiteral(name) : t.callExpression(createIdentifier(state, "resolveComponent"), [t.stringLiteral(name)]);
		return t.stringLiteral(name);
	}
	if (namePath.isJSXMemberExpression()) return transformJSXMemberExpression(namePath);
	throw new Error(`getTag: ${namePath.type} is not supported`);
};
const getJSXAttributeName = (path) => {
	const nameNode = path.node.name;
	if (t.isJSXIdentifier(nameNode)) return nameNode.name;
	return `${nameNode.namespace.name}:${nameNode.name.name}`;
};
/**
* Transform JSXText to StringLiteral
* @param path JSXText
* @returns StringLiteral | null
*/
const transformJSXText = (path) => {
	const str = transformText(path.node.value);
	return str !== "" ? t.stringLiteral(str) : null;
};
const transformText = (text) => {
	const lines = text.split(/\r\n|\n|\r/);
	let lastNonEmptyLine = 0;
	for (let i = 0; i < lines.length; i++) if (lines[i].match(/[^ \t]/)) lastNonEmptyLine = i;
	let str = "";
	for (let i = 0; i < lines.length; i++) {
		const line = lines[i];
		const isFirstLine = i === 0;
		const isLastLine = i === lines.length - 1;
		const isLastNonEmptyLine = i === lastNonEmptyLine;
		let trimmedLine = line.replace(/\t/g, " ");
		if (!isFirstLine) trimmedLine = trimmedLine.replace(/^[ ]+/, "");
		if (!isLastLine) trimmedLine = trimmedLine.replace(/[ ]+$/, "");
		if (trimmedLine) {
			if (!isLastNonEmptyLine) trimmedLine += " ";
			str += trimmedLine;
		}
	}
	return str;
};
/**
* Transform JSXExpressionContainer to Expression
* @param path JSXExpressionContainer
* @returns Expression
*/
const transformJSXExpressionContainer = (path) => path.get("expression").node;
/**
* Transform JSXSpreadChild
* @param path JSXSpreadChild
* @returns SpreadElement
*/
const transformJSXSpreadChild = (path) => t.spreadElement(path.get("expression").node);
const walksScope = (path, name, slotFlag) => {
	if (path.scope.hasBinding(name) && path.parentPath) {
		if (t.isJSXElement(path.parentPath.node)) path.parentPath.setData("slotFlag", slotFlag);
		walksScope(path.parentPath, name, slotFlag);
	}
};
const buildIIFE = (path, children) => {
	const { parentPath } = path;
	if (parentPath.isAssignmentExpression()) {
		const { left } = parentPath.node;
		if (t.isIdentifier(left)) return children.map((child) => {
			if (t.isIdentifier(child) && child.name === left.name) {
				const insertName = path.scope.generateUidIdentifier(child.name);
				parentPath.insertBefore(t.variableDeclaration("const", [t.variableDeclarator(insertName, t.callExpression(t.functionExpression(null, [], t.blockStatement([t.returnStatement(child)])), []))]));
				return insertName;
			}
			return child;
		});
	}
	return children;
};
const onRE = /^on[^a-z]/;
const isOn = (key) => onRE.test(key);
const mergeAsArray = (existing, incoming) => {
	if (t.isArrayExpression(existing.value)) existing.value.elements.push(incoming.value);
	else existing.value = t.arrayExpression([existing.value, incoming.value]);
};
const dedupeProperties = (properties = [], mergeProps) => {
	if (!mergeProps) return properties;
	const knownProps = /* @__PURE__ */ new Map();
	const deduped = [];
	properties.forEach((prop) => {
		if (t.isStringLiteral(prop.key)) {
			const { value: name } = prop.key;
			const existing = knownProps.get(name);
			if (existing) {
				if (name === "style" || name === "class" || name.startsWith("on")) mergeAsArray(existing, prop);
			} else {
				knownProps.set(name, prop);
				deduped.push(prop);
			}
		} else deduped.push(prop);
	});
	return deduped;
};
/**
*  Check if an attribute value is constant
* @param node
* @returns boolean
*/
const isConstant = (node) => {
	if (t.isIdentifier(node)) return node.name === "undefined";
	if (t.isArrayExpression(node)) {
		const { elements } = node;
		return elements.every((element) => element && isConstant(element));
	}
	if (t.isObjectExpression(node)) return node.properties.every((property) => isConstant(property.value));
	if (t.isTemplateLiteral(node) ? !node.expressions.length : t.isLiteral(node)) return true;
	return false;
};
const transformJSXSpreadAttribute = (nodePath, path, mergeProps, args) => {
	const argument = path.get("argument");
	const properties = t.isObjectExpression(argument.node) ? argument.node.properties : void 0;
	if (!properties) {
		if (argument.isIdentifier()) walksScope(nodePath, argument.node.name, slotFlags_default.DYNAMIC);
		args.push(mergeProps ? argument.node : t.spreadElement(argument.node));
	} else if (mergeProps) args.push(t.objectExpression(properties));
	else args.push(...properties);
};

//#endregion
//#region src/patchFlags.ts
let PatchFlags = /* @__PURE__ */ function(PatchFlags$1) {
	PatchFlags$1[PatchFlags$1["TEXT"] = 1] = "TEXT";
	PatchFlags$1[PatchFlags$1["CLASS"] = 2] = "CLASS";
	PatchFlags$1[PatchFlags$1["STYLE"] = 4] = "STYLE";
	PatchFlags$1[PatchFlags$1["PROPS"] = 8] = "PROPS";
	PatchFlags$1[PatchFlags$1["FULL_PROPS"] = 16] = "FULL_PROPS";
	PatchFlags$1[PatchFlags$1["HYDRATE_EVENTS"] = 32] = "HYDRATE_EVENTS";
	PatchFlags$1[PatchFlags$1["STABLE_FRAGMENT"] = 64] = "STABLE_FRAGMENT";
	PatchFlags$1[PatchFlags$1["KEYED_FRAGMENT"] = 128] = "KEYED_FRAGMENT";
	PatchFlags$1[PatchFlags$1["UNKEYED_FRAGMENT"] = 256] = "UNKEYED_FRAGMENT";
	PatchFlags$1[PatchFlags$1["NEED_PATCH"] = 512] = "NEED_PATCH";
	PatchFlags$1[PatchFlags$1["DYNAMIC_SLOTS"] = 1024] = "DYNAMIC_SLOTS";
	PatchFlags$1[PatchFlags$1["HOISTED"] = -1] = "HOISTED";
	PatchFlags$1[PatchFlags$1["BAIL"] = -2] = "BAIL";
	return PatchFlags$1;
}({});
const PatchFlagNames = {
	[PatchFlags.TEXT]: "TEXT",
	[PatchFlags.CLASS]: "CLASS",
	[PatchFlags.STYLE]: "STYLE",
	[PatchFlags.PROPS]: "PROPS",
	[PatchFlags.FULL_PROPS]: "FULL_PROPS",
	[PatchFlags.HYDRATE_EVENTS]: "HYDRATE_EVENTS",
	[PatchFlags.STABLE_FRAGMENT]: "STABLE_FRAGMENT",
	[PatchFlags.KEYED_FRAGMENT]: "KEYED_FRAGMENT",
	[PatchFlags.UNKEYED_FRAGMENT]: "UNKEYED_FRAGMENT",
	[PatchFlags.DYNAMIC_SLOTS]: "DYNAMIC_SLOTS",
	[PatchFlags.NEED_PATCH]: "NEED_PATCH",
	[PatchFlags.HOISTED]: "HOISTED",
	[PatchFlags.BAIL]: "BAIL"
};

//#endregion
//#region src/parseDirectives.ts
/**
* Get JSX element type
*
* @param path Path<JSXOpeningElement>
*/
const getType = (path) => {
	const typePath = path.get("attributes").find((attribute) => {
		if (!attribute.isJSXAttribute()) return false;
		return attribute.get("name").isJSXIdentifier() && attribute.get("name").node.name === "type";
	});
	return typePath ? typePath.get("value").node : null;
};
const parseModifiers = (value) => t.isArrayExpression(value) ? value.elements.map((el) => t.isStringLiteral(el) ? el.value : "").filter(Boolean) : [];
const parseDirectives = (params) => {
	const { path, value, state, tag, isComponent } = params;
	const args = [];
	const vals = [];
	const modifiersSet = [];
	let directiveName;
	let directiveArgument;
	let directiveModifiers;
	if ("namespace" in path.node.name) {
		[directiveName, directiveArgument] = params.name.split(":");
		directiveName = path.node.name.namespace.name;
		directiveArgument = path.node.name.name.name;
		directiveModifiers = directiveArgument.split("_").slice(1);
	} else {
		const underscoreModifiers = params.name.split("_");
		directiveName = underscoreModifiers.shift() || "";
		directiveModifiers = underscoreModifiers;
	}
	directiveName = directiveName.replace(/^v/, "").replace(/^-/, "").replace(/^\S/, (s) => s.toLowerCase());
	if (directiveArgument) args.push(t.stringLiteral(directiveArgument.split("_")[0]));
	const isVModels = directiveName === "models";
	const isVModel = directiveName === "model";
	if (isVModel && !path.get("value").isJSXExpressionContainer()) throw new Error("You have to use JSX Expression inside your v-model");
	if (isVModels && !isComponent) throw new Error("v-models can only use in custom components");
	const shouldResolve = ![
		"html",
		"text",
		"model",
		"slots",
		"models"
	].includes(directiveName) || isVModel && !isComponent;
	let modifiers = directiveModifiers;
	if (t.isArrayExpression(value)) (isVModels ? value.elements : [value]).forEach((element) => {
		if (isVModels && !t.isArrayExpression(element)) throw new Error("You should pass a Two-dimensional Arrays to v-models");
		const { elements } = element;
		const [first, second, third] = elements;
		if (second && !t.isArrayExpression(second) && !t.isSpreadElement(second)) {
			args.push(second);
			modifiers = parseModifiers(third);
		} else if (t.isArrayExpression(second)) {
			if (!shouldResolve) args.push(t.nullLiteral());
			modifiers = parseModifiers(second);
		} else if (!shouldResolve) args.push(t.nullLiteral());
		modifiersSet.push(new Set(modifiers));
		vals.push(first);
	});
	else if (isVModel && !shouldResolve) {
		args.push(t.nullLiteral());
		modifiersSet.push(new Set(directiveModifiers));
	} else modifiersSet.push(new Set(directiveModifiers));
	return {
		directiveName,
		modifiers: modifiersSet,
		values: vals.length ? vals : [value],
		args,
		directive: shouldResolve ? [
			resolveDirective(path, state, tag, directiveName),
			vals[0] || value,
			modifiersSet[0]?.size ? args[0] || t.unaryExpression("void", t.numericLiteral(0), true) : args[0],
			!!modifiersSet[0]?.size && t.objectExpression([...modifiersSet[0]].map((modifier) => t.objectProperty(t.identifier(modifier), t.booleanLiteral(true))))
		].filter(Boolean) : void 0
	};
};
const resolveDirective = (path, state, tag, directiveName) => {
	if (directiveName === "show") return createIdentifier(state, "vShow");
	if (directiveName === "model") {
		let modelToUse;
		const type = getType(path.parentPath);
		switch (tag.value) {
			case "select":
				modelToUse = createIdentifier(state, "vModelSelect");
				break;
			case "textarea":
				modelToUse = createIdentifier(state, "vModelText");
				break;
			default: if (t.isStringLiteral(type) || !type) switch (type?.value) {
				case "checkbox":
					modelToUse = createIdentifier(state, "vModelCheckbox");
					break;
				case "radio":
					modelToUse = createIdentifier(state, "vModelRadio");
					break;
				default: modelToUse = createIdentifier(state, "vModelText");
			}
			else modelToUse = createIdentifier(state, "vModelDynamic");
		}
		return modelToUse;
	}
	const referenceName = "v" + directiveName[0].toUpperCase() + directiveName.slice(1);
	if (path.scope.references[referenceName]) return t.identifier(referenceName);
	return t.callExpression(createIdentifier(state, "resolveDirective"), [t.stringLiteral(directiveName)]);
};
var parseDirectives_default = parseDirectives;

//#endregion
//#region src/transform-vue-jsx.ts
const xlinkRE = /^xlink([A-Z])/;
const getJSXAttributeValue = (path, state) => {
	const valuePath = path.get("value");
	if (valuePath.isJSXElement()) return transformJSXElement(valuePath, state);
	if (valuePath.isStringLiteral()) return t.stringLiteral(transformText(valuePath.node.value));
	if (valuePath.isJSXExpressionContainer()) return transformJSXExpressionContainer(valuePath);
	return null;
};
const buildProps = (path, state) => {
	const tag = getTag(path, state);
	const isComponent = checkIsComponent(path.get("openingElement"), state);
	const props = path.get("openingElement").get("attributes");
	const directives = [];
	const dynamicPropNames = /* @__PURE__ */ new Set();
	let slots = null;
	let patchFlag = 0;
	if (props.length === 0) return {
		tag,
		isComponent,
		slots,
		props: t.nullLiteral(),
		directives,
		patchFlag,
		dynamicPropNames
	};
	let properties = [];
	let hasRef = false;
	let hasClassBinding = false;
	let hasStyleBinding = false;
	let hasHydrationEventBinding = false;
	let hasDynamicKeys = false;
	const mergeArgs = [];
	const { mergeProps = true } = state.opts;
	props.forEach((prop) => {
		if (prop.isJSXAttribute()) {
			let name = getJSXAttributeName(prop);
			const attributeValue = getJSXAttributeValue(prop, state);
			if (!isConstant(attributeValue) || name === "ref") {
				if (!isComponent && isOn(name) && name.toLowerCase() !== "onclick" && name !== "onUpdate:modelValue") hasHydrationEventBinding = true;
				if (name === "ref") hasRef = true;
				else if (name === "class" && !isComponent) hasClassBinding = true;
				else if (name === "style" && !isComponent) hasStyleBinding = true;
				else if (name !== "key" && !isDirective(name) && name !== "on") dynamicPropNames.add(name);
			}
			if (state.opts.transformOn && (name === "on" || name === "nativeOn")) {
				if (!state.get("transformOn")) state.set("transformOn", addDefault(path, "@vue/babel-helper-vue-transform-on", { nameHint: "_transformOn" }));
				mergeArgs.push(t.callExpression(state.get("transformOn"), [attributeValue || t.booleanLiteral(true)]));
				return;
			}
			if (isDirective(name)) {
				const { directive, modifiers, values, args, directiveName } = parseDirectives_default({
					tag,
					isComponent,
					name,
					path: prop,
					state,
					value: attributeValue
				});
				if (directiveName === "slots") {
					slots = attributeValue;
					return;
				}
				if (directive) directives.push(t.arrayExpression(directive));
				else if (directiveName === "html") {
					properties.push(t.objectProperty(t.stringLiteral("innerHTML"), values[0]));
					dynamicPropNames.add("innerHTML");
				} else if (directiveName === "text") {
					properties.push(t.objectProperty(t.stringLiteral("textContent"), values[0]));
					dynamicPropNames.add("textContent");
				}
				if (["models", "model"].includes(directiveName)) values.forEach((value, index) => {
					const propName = args[index];
					const isDynamic = propName && !t.isStringLiteral(propName) && !t.isNullLiteral(propName);
					if (!directive) {
						properties.push(t.objectProperty(t.isNullLiteral(propName) ? t.stringLiteral("modelValue") : propName, value, isDynamic));
						if (!isDynamic) dynamicPropNames.add(propName?.value || "modelValue");
						if (modifiers[index]?.size) properties.push(t.objectProperty(isDynamic ? t.binaryExpression("+", propName, t.stringLiteral("Modifiers")) : t.stringLiteral(`${propName?.value || "model"}Modifiers`), t.objectExpression([...modifiers[index]].map((modifier) => t.objectProperty(t.stringLiteral(modifier), t.booleanLiteral(true)))), isDynamic));
					}
					const updateName = isDynamic ? t.binaryExpression("+", t.stringLiteral("onUpdate:"), propName) : t.stringLiteral(`onUpdate:${propName?.value || "modelValue"}`);
					properties.push(t.objectProperty(updateName, t.arrowFunctionExpression([t.identifier("$event")], t.assignmentExpression("=", value, t.identifier("$event"))), isDynamic));
					if (!isDynamic) dynamicPropNames.add(updateName.value);
					else hasDynamicKeys = true;
				});
			} else {
				if (name.match(xlinkRE)) name = name.replace(xlinkRE, (_, firstCharacter) => `xlink:${firstCharacter.toLowerCase()}`);
				properties.push(t.objectProperty(t.stringLiteral(name), attributeValue || t.booleanLiteral(true)));
			}
		} else {
			if (properties.length && mergeProps) {
				mergeArgs.push(t.objectExpression(dedupeProperties(properties, mergeProps)));
				properties = [];
			}
			hasDynamicKeys = true;
			transformJSXSpreadAttribute(path, prop, mergeProps, mergeProps ? mergeArgs : properties);
		}
	});
	if (hasDynamicKeys) patchFlag |= PatchFlags.FULL_PROPS;
	else {
		if (hasClassBinding) patchFlag |= PatchFlags.CLASS;
		if (hasStyleBinding) patchFlag |= PatchFlags.STYLE;
		if (dynamicPropNames.size) patchFlag |= PatchFlags.PROPS;
		if (hasHydrationEventBinding) patchFlag |= PatchFlags.HYDRATE_EVENTS;
	}
	if ((patchFlag === 0 || patchFlag === PatchFlags.HYDRATE_EVENTS) && (hasRef || directives.length > 0)) patchFlag |= PatchFlags.NEED_PATCH;
	let propsExpression = t.nullLiteral();
	if (mergeArgs.length) {
		if (properties.length) mergeArgs.push(t.objectExpression(dedupeProperties(properties, mergeProps)));
		if (mergeArgs.length > 1) propsExpression = t.callExpression(createIdentifier(state, "mergeProps"), mergeArgs);
		else propsExpression = mergeArgs[0];
	} else if (properties.length) if (properties.length === 1 && t.isSpreadElement(properties[0])) propsExpression = properties[0].argument;
	else propsExpression = t.objectExpression(dedupeProperties(properties, mergeProps));
	return {
		tag,
		props: propsExpression,
		isComponent,
		slots,
		directives,
		patchFlag,
		dynamicPropNames
	};
};
/**
* Get children from Array of JSX children
* @param paths Array<JSXText | JSXExpressionContainer  | JSXElement | JSXFragment>
* @returns Array<Expression | SpreadElement>
*/
const getChildren = (paths, state) => paths.map((path) => {
	if (path.isJSXText()) {
		const transformedText = transformJSXText(path);
		if (transformedText) return t.callExpression(createIdentifier(state, "createTextVNode"), [transformedText]);
		return transformedText;
	}
	if (path.isJSXExpressionContainer()) {
		const expression = transformJSXExpressionContainer(path);
		if (t.isIdentifier(expression)) {
			const { name } = expression;
			const { referencePaths = [] } = path.scope.getBinding(name) || {};
			referencePaths.forEach((referencePath) => {
				walksScope(referencePath, name, slotFlags_default.DYNAMIC);
			});
		}
		return expression;
	}
	if (path.isJSXSpreadChild()) return transformJSXSpreadChild(path);
	if (path.isCallExpression()) return path.node;
	if (path.isJSXElement()) return transformJSXElement(path, state);
	throw new Error(`getChildren: ${path.type} is not supported`);
}).filter(((value) => value != null && !t.isJSXEmptyExpression(value)));
const transformJSXElement = (path, state) => {
	const children = getChildren(path.get("children"), state);
	const { tag, props, isComponent, directives, patchFlag, dynamicPropNames, slots } = buildProps(path, state);
	const { optimize = false } = state.opts;
	if (directives.length && directives.some((d) => d.elements?.[0]?.type === "CallExpression" && d.elements[0].callee.type === "Identifier" && d.elements[0].callee.name === "_resolveDirective")) {
		let currentPath = path;
		while (currentPath.parentPath?.isJSXElement()) {
			currentPath = currentPath.parentPath;
			currentPath.setData("slotFlag", 0);
		}
	}
	const slotFlag = path.getData("slotFlag") ?? slotFlags_default.STABLE;
	const optimizeSlots = optimize && slotFlag !== 0;
	let VNodeChild;
	if (children.length > 1 || slots) VNodeChild = isComponent ? children.length ? t.objectExpression([
		!!children.length && t.objectProperty(t.identifier("default"), t.arrowFunctionExpression([], t.arrayExpression(buildIIFE(path, children)))),
		...slots ? t.isObjectExpression(slots) ? slots.properties : [t.spreadElement(slots)] : [],
		optimizeSlots && t.objectProperty(t.identifier("_"), t.numericLiteral(slotFlag))
	].filter(Boolean)) : slots : t.arrayExpression(children);
	else if (children.length === 1) {
		const { enableObjectSlots = true } = state.opts;
		const child = children[0];
		const objectExpression = t.objectExpression([t.objectProperty(t.identifier("default"), t.arrowFunctionExpression([], t.arrayExpression(buildIIFE(path, [child])))), optimizeSlots && t.objectProperty(t.identifier("_"), t.numericLiteral(slotFlag))].filter(Boolean));
		if (t.isIdentifier(child) && isComponent) VNodeChild = enableObjectSlots ? t.conditionalExpression(t.callExpression(state.get("@vue/babel-plugin-jsx/runtimeIsSlot")(), [child]), child, objectExpression) : objectExpression;
		else if (t.isCallExpression(child) && child.loc && isComponent) if (enableObjectSlots) {
			const { scope } = path;
			const slotId = scope.generateUidIdentifier("slot");
			if (scope) scope.push({
				id: slotId,
				kind: "let"
			});
			const alternate = t.objectExpression([t.objectProperty(t.identifier("default"), t.arrowFunctionExpression([], t.arrayExpression(buildIIFE(path, [slotId])))), optimizeSlots && t.objectProperty(t.identifier("_"), t.numericLiteral(slotFlag))].filter(Boolean));
			const assignment = t.assignmentExpression("=", slotId, child);
			const condition = t.callExpression(state.get("@vue/babel-plugin-jsx/runtimeIsSlot")(), [assignment]);
			VNodeChild = t.conditionalExpression(condition, slotId, alternate);
		} else VNodeChild = objectExpression;
		else if (t.isFunctionExpression(child) || t.isArrowFunctionExpression(child)) VNodeChild = t.objectExpression([t.objectProperty(t.identifier("default"), child)]);
		else if (t.isObjectExpression(child)) VNodeChild = t.objectExpression([...child.properties, optimizeSlots && t.objectProperty(t.identifier("_"), t.numericLiteral(slotFlag))].filter(Boolean));
		else VNodeChild = isComponent ? t.objectExpression([t.objectProperty(t.identifier("default"), t.arrowFunctionExpression([], t.arrayExpression([child])))]) : t.arrayExpression([child]);
	}
	const createVNode = t.callExpression(createIdentifier(state, "createVNode"), [
		tag,
		props,
		VNodeChild || t.nullLiteral(),
		!!patchFlag && optimize && t.numericLiteral(patchFlag),
		!!dynamicPropNames.size && optimize && t.arrayExpression([...dynamicPropNames.keys()].map((name) => t.stringLiteral(name)))
	].filter(Boolean));
	if (!directives.length) return createVNode;
	return t.callExpression(createIdentifier(state, "withDirectives"), [createVNode, t.arrayExpression(directives)]);
};
const visitor$1 = { JSXElement: { exit(path, state) {
	path.replaceWith(transformJSXElement(path, state));
} } };
var transform_vue_jsx_default = visitor$1;

//#endregion
//#region src/sugar-fragment.ts
const transformFragment = (path, Fragment) => {
	const children = path.get("children") || [];
	return t.jsxElement(t.jsxOpeningElement(Fragment, []), t.jsxClosingElement(Fragment), children.map(({ node }) => node), false);
};
const visitor = { JSXFragment: { enter(path, state) {
	const fragmentCallee = createIdentifier(state, FRAGMENT);
	path.replaceWith(transformFragment(path, t.isIdentifier(fragmentCallee) ? t.jsxIdentifier(fragmentCallee.name) : t.jsxMemberExpression(t.jsxIdentifier(fragmentCallee.object.name), t.jsxIdentifier(fragmentCallee.property.name))));
} } };
var sugar_fragment_default = visitor;

//#endregion
//#region src/index.ts
const hasJSX = (parentPath) => {
	let fileHasJSX = false;
	parentPath.traverse({
		JSXElement(path) {
			fileHasJSX = true;
			path.stop();
		},
		JSXFragment(path) {
			fileHasJSX = true;
			path.stop();
		}
	});
	return fileHasJSX;
};
const JSX_ANNOTATION_REGEX = /\*?\s*@jsx\s+([^\s]+)/;
/* @__NO_SIDE_EFFECTS__ */
function interopDefault(m) {
	return m.default || m;
}
const syntaxJsx = /* @__PURE__ */ interopDefault(_syntaxJsx);
const template = /* @__PURE__ */ interopDefault(_template);
const plugin = declare((api, opt, dirname) => {
	const { types } = api;
	let resolveType;
	if (opt.resolveType) {
		if (typeof opt.resolveType === "boolean") opt.resolveType = {};
		resolveType = ResolveType(api, opt.resolveType, dirname);
	}
	return {
		...resolveType || {},
		name: "babel-plugin-jsx",
		inherits: /* @__PURE__ */ interopDefault(syntaxJsx),
		visitor: {
			...resolveType?.visitor,
			...transform_vue_jsx_default,
			...sugar_fragment_default,
			Program: { enter(path, state) {
				if (hasJSX(path)) {
					const importNames = [
						"createVNode",
						"Fragment",
						"resolveComponent",
						"withDirectives",
						"vShow",
						"vModelSelect",
						"vModelText",
						"vModelCheckbox",
						"vModelRadio",
						"vModelText",
						"vModelDynamic",
						"resolveDirective",
						"mergeProps",
						"createTextVNode",
						"isVNode"
					];
					if (isModule(path)) {
						const importMap = {};
						importNames.forEach((name) => {
							state.set(name, () => {
								if (importMap[name]) return types.cloneNode(importMap[name]);
								const identifier = addNamed(path, name, "vue", { ensureLiveReference: true });
								importMap[name] = identifier;
								return identifier;
							});
						});
						const { enableObjectSlots = true } = state.opts;
						if (enableObjectSlots) state.set("@vue/babel-plugin-jsx/runtimeIsSlot", () => {
							if (importMap.runtimeIsSlot) return importMap.runtimeIsSlot;
							const { name: isVNodeName } = state.get("isVNode")();
							const isSlot = path.scope.generateUidIdentifier("isSlot");
							const ast = template.ast`
                    function ${isSlot.name}(s) {
                      return typeof s === 'function' || (Object.prototype.toString.call(s) === '[object Object]' && !${isVNodeName}(s));
                    }
                  `;
							const lastImport = path.get("body").filter((p) => p.isImportDeclaration()).pop();
							if (lastImport) lastImport.insertAfter(ast);
							importMap.runtimeIsSlot = isSlot;
							return isSlot;
						});
					} else {
						let sourceName;
						importNames.forEach((name) => {
							state.set(name, () => {
								if (!sourceName) sourceName = addNamespace(path, "vue", { ensureLiveReference: true });
								return t.memberExpression(sourceName, t.identifier(name));
							});
						});
						const helpers = {};
						const { enableObjectSlots = true } = state.opts;
						if (enableObjectSlots) state.set("@vue/babel-plugin-jsx/runtimeIsSlot", () => {
							if (helpers.runtimeIsSlot) return helpers.runtimeIsSlot;
							const isSlot = path.scope.generateUidIdentifier("isSlot");
							const { object: objectName } = state.get("isVNode")();
							const ast = template.ast`
                    function ${isSlot.name}(s) {
                      return typeof s === 'function' || (Object.prototype.toString.call(s) === '[object Object]' && !${objectName.name}.isVNode(s));
                    }
                  `;
							const lastImport = path.get("body").filter((p) => p.isVariableDeclaration() && p.node.declarations.some((d) => d.id?.name === sourceName.name)).pop();
							if (lastImport) lastImport.insertAfter(ast);
							return isSlot;
						});
					}
					const { opts: { pragma = "" }, file } = state;
					if (pragma) state.set("createVNode", () => t.identifier(pragma));
					if (file.ast.comments) for (const comment of file.ast.comments) {
						const jsxMatches = JSX_ANNOTATION_REGEX.exec(comment.value);
						if (jsxMatches) state.set("createVNode", () => t.identifier(jsxMatches[1]));
					}
				}
			} }
		}
	};
});
var src_default = plugin;

//#endregion
export { src_default as default, plugin as "module.exports" };