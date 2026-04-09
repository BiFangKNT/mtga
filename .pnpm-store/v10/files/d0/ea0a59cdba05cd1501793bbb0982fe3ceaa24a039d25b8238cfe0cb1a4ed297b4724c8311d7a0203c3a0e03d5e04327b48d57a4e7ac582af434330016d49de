import { computed, customRef, effectScope, getCurrentInstance, getCurrentScope, hasInjectionContext, inject, isReactive, isRef, markRaw, nextTick, onMounted, onScopeDispose, reactive, readonly, ref, shallowRef, toRaw, toRef, toRefs, toValue, unref, watch, watchEffect } from "./runtime-core.esm-bundler-Cyv4obHQ.js";
/**
* setActivePinia must be called to handle SSR at the top of functions like
* `fetch`, `setup`, `serverPrefetch` and others
*/
let activePinia;
/**
* Sets or unsets the active pinia. Used in SSR and internally when calling
* actions and getters
*
* @param pinia - Pinia instance
*/
const setActivePinia = (pinia) => activePinia = pinia;
const piniaSymbol = Symbol();
function isPlainObject(o) {
	return o && typeof o === "object" && Object.prototype.toString.call(o) === "[object Object]" && typeof o.toJSON !== "function";
}
/**
* Possible types for SubscriptionCallback
*/
var MutationType;
(function(MutationType$1) {
	/**
	* Direct mutation of the state:
	*
	* - `store.name = 'new name'`
	* - `store.$state.name = 'new name'`
	* - `store.list.push('new item')`
	*/
	MutationType$1["direct"] = "direct";
	/**
	* Mutated the state with `$patch` and an object
	*
	* - `store.$patch({ name: 'newName' })`
	*/
	MutationType$1["patchObject"] = "patch object";
	/**
	* Mutated the state with `$patch` and a function
	*
	* - `store.$patch(state => state.name = 'newName')`
	*/
	MutationType$1["patchFunction"] = "patch function";
})(MutationType || (MutationType = {}));
const IS_CLIENT = typeof window !== "undefined";
const _global$1 = /* @__PURE__ */ (() => typeof window === "object" && window.window === window ? window : typeof self === "object" && self.self === self ? self : typeof global === "object" && global.global === global ? global : typeof globalThis === "object" ? globalThis : { HTMLElement: null })();
function bom(blob, { autoBom = false } = {}) {
	if (autoBom && /^\s*(?:text\/\S*|application\/xml|\S*\/\S*\+xml)\s*;.*charset\s*=\s*utf-8/i.test(blob.type)) return new Blob([String.fromCharCode(65279), blob], { type: blob.type });
	return blob;
}
function download(url, name, opts) {
	const xhr = new XMLHttpRequest();
	xhr.open("GET", url);
	xhr.responseType = "blob";
	xhr.onload = function() {
		saveAs(xhr.response, name, opts);
	};
	xhr.onerror = function() {
		console.error("could not download file");
	};
	xhr.send();
}
function corsEnabled(url) {
	const xhr = new XMLHttpRequest();
	xhr.open("HEAD", url, false);
	try {
		xhr.send();
	} catch (e) {}
	return xhr.status >= 200 && xhr.status <= 299;
}
function click(node) {
	try {
		node.dispatchEvent(new MouseEvent("click"));
	} catch (e) {
		const evt = new MouseEvent("click", {
			bubbles: true,
			cancelable: true,
			view: window,
			detail: 0,
			screenX: 80,
			screenY: 20,
			clientX: 80,
			clientY: 20,
			ctrlKey: false,
			altKey: false,
			shiftKey: false,
			metaKey: false,
			button: 0,
			relatedTarget: null
		});
		node.dispatchEvent(evt);
	}
}
const _navigator = typeof navigator === "object" ? navigator : { userAgent: "" };
const isMacOSWebView = /* @__PURE__ */ (() => /Macintosh/.test(_navigator.userAgent) && /AppleWebKit/.test(_navigator.userAgent) && !/Safari/.test(_navigator.userAgent))();
const saveAs = !IS_CLIENT ? () => {} : typeof HTMLAnchorElement !== "undefined" && "download" in HTMLAnchorElement.prototype && !isMacOSWebView ? downloadSaveAs : "msSaveOrOpenBlob" in _navigator ? msSaveAs : fileSaverSaveAs;
function downloadSaveAs(blob, name = "download", opts) {
	const a = document.createElement("a");
	a.download = name;
	a.rel = "noopener";
	if (typeof blob === "string") {
		a.href = blob;
		if (a.origin !== location.origin) if (corsEnabled(a.href)) download(blob, name, opts);
		else {
			a.target = "_blank";
			click(a);
		}
		else click(a);
	} else {
		a.href = URL.createObjectURL(blob);
		setTimeout(function() {
			URL.revokeObjectURL(a.href);
		}, 4e4);
		setTimeout(function() {
			click(a);
		}, 0);
	}
}
function msSaveAs(blob, name = "download", opts) {
	if (typeof blob === "string") if (corsEnabled(blob)) download(blob, name, opts);
	else {
		const a = document.createElement("a");
		a.href = blob;
		a.target = "_blank";
		setTimeout(function() {
			click(a);
		});
	}
	else navigator.msSaveOrOpenBlob(bom(blob, opts), name);
}
function fileSaverSaveAs(blob, name, opts, popup) {
	popup = popup || open("", "_blank");
	if (popup) popup.document.title = popup.document.body.innerText = "downloading...";
	if (typeof blob === "string") return download(blob, name, opts);
	const force = blob.type === "application/octet-stream";
	const isSafari = /constructor/i.test(String(_global$1.HTMLElement)) || "safari" in _global$1;
	const isChromeIOS = /CriOS\/[\d]+/.test(navigator.userAgent);
	if ((isChromeIOS || force && isSafari || isMacOSWebView) && typeof FileReader !== "undefined") {
		const reader = new FileReader();
		reader.onloadend = function() {
			let url = reader.result;
			if (typeof url !== "string") {
				popup = null;
				throw new Error("Wrong reader.result type");
			}
			url = isChromeIOS ? url : url.replace(/^data:[^;]*;/, "data:attachment/file;");
			if (popup) popup.location.href = url;
			else location.assign(url);
			popup = null;
		};
		reader.readAsDataURL(blob);
	} else {
		const url = URL.createObjectURL(blob);
		if (popup) popup.location.assign(url);
		else location.href = url;
		popup = null;
		setTimeout(function() {
			URL.revokeObjectURL(url);
		}, 4e4);
	}
}
const { assign: assign$1 } = Object;
/**
* Creates a Pinia instance to be used by the application
*/
function createPinia() {
	const scope = effectScope(true);
	const state = scope.run(() => ref({}));
	let _p = [];
	let toBeInstalled = [];
	const pinia = markRaw({
		install(app) {
			setActivePinia(pinia);
			pinia._a = app;
			app.provide(piniaSymbol, pinia);
			app.config.globalProperties.$pinia = pinia;
			toBeInstalled.forEach((plugin) => _p.push(plugin));
			toBeInstalled = [];
		},
		use(plugin) {
			if (!this._a) toBeInstalled.push(plugin);
			else _p.push(plugin);
			return this;
		},
		_p,
		_a: null,
		_e: scope,
		_s: new Map(),
		state
	});
	return pinia;
}
const noop$1 = () => {};
function addSubscription(subscriptions, callback, detached, onCleanup = noop$1) {
	subscriptions.push(callback);
	const removeSubscription = () => {
		const idx = subscriptions.indexOf(callback);
		if (idx > -1) {
			subscriptions.splice(idx, 1);
			onCleanup();
		}
	};
	if (!detached && getCurrentScope()) onScopeDispose(removeSubscription);
	return removeSubscription;
}
function triggerSubscriptions(subscriptions, ...args) {
	subscriptions.slice().forEach((callback) => {
		callback(...args);
	});
}
const fallbackRunWithContext = (fn) => fn();
/**
* Marks a function as an action for `$onAction`
* @internal
*/
const ACTION_MARKER = Symbol();
/**
* Action name symbol. Allows to add a name to an action after defining it
* @internal
*/
const ACTION_NAME = Symbol();
function mergeReactiveObjects(target, patchToApply) {
	if (target instanceof Map && patchToApply instanceof Map) patchToApply.forEach((value, key) => target.set(key, value));
	else if (target instanceof Set && patchToApply instanceof Set) patchToApply.forEach(target.add, target);
	for (const key in patchToApply) {
		if (!patchToApply.hasOwnProperty(key)) continue;
		const subPatch = patchToApply[key];
		const targetValue = target[key];
		if (isPlainObject(targetValue) && isPlainObject(subPatch) && target.hasOwnProperty(key) && !isRef(subPatch) && !isReactive(subPatch)) target[key] = mergeReactiveObjects(targetValue, subPatch);
		else target[key] = subPatch;
	}
	return target;
}
const skipHydrateSymbol = Symbol();
/**
* Returns whether a value should be hydrated
*
* @param obj - target variable
* @returns true if `obj` should be hydrated
*/
function shouldHydrate(obj) {
	return !isPlainObject(obj) || !Object.prototype.hasOwnProperty.call(obj, skipHydrateSymbol);
}
const { assign } = Object;
function isComputed(o) {
	return !!(isRef(o) && o.effect);
}
function createOptionsStore(id, options, pinia, hot$1) {
	const { state, actions, getters } = options;
	const initialState = pinia.state.value[id];
	let store;
	function setup() {
		if (!initialState && true) pinia.state.value[id] = state ? state() : {};
		const localState = toRefs(pinia.state.value[id]);
		return assign(localState, actions, Object.keys(getters || {}).reduce((computedGetters, name) => {
			computedGetters[name] = markRaw(computed(() => {
				setActivePinia(pinia);
				const store$1 = pinia._s.get(id);
				return getters[name].call(store$1, store$1);
			}));
			return computedGetters;
		}, {}));
	}
	store = createSetupStore(id, setup, options, pinia, hot$1, true);
	return store;
}
function createSetupStore($id, setup, options = {}, pinia, hot$1, isOptionsStore) {
	let scope;
	const optionsForPlugin = assign({ actions: {} }, options);
	const $subscribeOptions = { deep: true };
	let isListening;
	let isSyncListening;
	let subscriptions = [];
	let actionSubscriptions = [];
	let debuggerEvents;
	const initialState = pinia.state.value[$id];
	if (!isOptionsStore && !initialState && true) pinia.state.value[$id] = {};
	const hotState = ref({});
	let activeListener;
	function $patch(partialStateOrMutator) {
		let subscriptionMutation;
		isListening = isSyncListening = false;
		if (typeof partialStateOrMutator === "function") {
			partialStateOrMutator(pinia.state.value[$id]);
			subscriptionMutation = {
				type: MutationType.patchFunction,
				storeId: $id,
				events: debuggerEvents
			};
		} else {
			mergeReactiveObjects(pinia.state.value[$id], partialStateOrMutator);
			subscriptionMutation = {
				type: MutationType.patchObject,
				payload: partialStateOrMutator,
				storeId: $id,
				events: debuggerEvents
			};
		}
		const myListenerId = activeListener = Symbol();
		nextTick().then(() => {
			if (activeListener === myListenerId) isListening = true;
		});
		isSyncListening = true;
		triggerSubscriptions(subscriptions, subscriptionMutation, pinia.state.value[$id]);
	}
	const $reset = isOptionsStore ? function $reset$1() {
		const { state } = options;
		const newState = state ? state() : {};
		this.$patch(($state) => {
			assign($state, newState);
		});
	} : noop$1;
	function $dispose() {
		scope.stop();
		subscriptions = [];
		actionSubscriptions = [];
		pinia._s.delete($id);
	}
	/**
	* Helper that wraps function so it can be tracked with $onAction
	* @param fn - action to wrap
	* @param name - name of the action
	*/
	const action = (fn, name = "") => {
		if (ACTION_MARKER in fn) {
			fn[ACTION_NAME] = name;
			return fn;
		}
		const wrappedAction = function() {
			setActivePinia(pinia);
			const args = Array.from(arguments);
			const afterCallbackList = [];
			const onErrorCallbackList = [];
			function after(callback) {
				afterCallbackList.push(callback);
			}
			function onError(callback) {
				onErrorCallbackList.push(callback);
			}
			triggerSubscriptions(actionSubscriptions, {
				args,
				name: wrappedAction[ACTION_NAME],
				store,
				after,
				onError
			});
			let ret;
			try {
				ret = fn.apply(this && this.$id === $id ? this : store, args);
			} catch (error) {
				triggerSubscriptions(onErrorCallbackList, error);
				throw error;
			}
			if (ret instanceof Promise) return ret.then((value) => {
				triggerSubscriptions(afterCallbackList, value);
				return value;
			}).catch((error) => {
				triggerSubscriptions(onErrorCallbackList, error);
				return Promise.reject(error);
			});
			triggerSubscriptions(afterCallbackList, ret);
			return ret;
		};
		wrappedAction[ACTION_MARKER] = true;
		wrappedAction[ACTION_NAME] = name;
		return wrappedAction;
	};
	const _hmrPayload = /* @__PURE__ */ markRaw({
		actions: {},
		getters: {},
		state: [],
		hotState
	});
	const partialStore = {
		_p: pinia,
		$id,
		$onAction: addSubscription.bind(null, actionSubscriptions),
		$patch,
		$reset,
		$subscribe(callback, options$1 = {}) {
			const removeSubscription = addSubscription(subscriptions, callback, options$1.detached, () => stopWatcher());
			const stopWatcher = scope.run(() => watch(() => pinia.state.value[$id], (state) => {
				if (options$1.flush === "sync" ? isSyncListening : isListening) callback({
					storeId: $id,
					type: MutationType.direct,
					events: debuggerEvents
				}, state);
			}, assign({}, $subscribeOptions, options$1)));
			return removeSubscription;
		},
		$dispose
	};
	const store = reactive(partialStore);
	pinia._s.set($id, store);
	const runWithContext = pinia._a && pinia._a.runWithContext || fallbackRunWithContext;
	const setupStore = runWithContext(() => pinia._e.run(() => (scope = effectScope()).run(() => setup({ action }))));
	for (const key in setupStore) {
		const prop = setupStore[key];
		if (isRef(prop) && !isComputed(prop) || isReactive(prop)) {
			if (!isOptionsStore) {
				if (initialState && shouldHydrate(prop)) if (isRef(prop)) prop.value = initialState[key];
				else mergeReactiveObjects(prop, initialState[key]);
				pinia.state.value[$id][key] = prop;
			}
		} else if (typeof prop === "function") {
			const actionValue = action(prop, key);
			setupStore[key] = actionValue;
			optionsForPlugin.actions[key] = prop;
		}
	}
	assign(store, setupStore);
	assign(toRaw(store), setupStore);
	Object.defineProperty(store, "$state", {
		get: () => pinia.state.value[$id],
		set: (state) => {
			$patch(($state) => {
				assign($state, state);
			});
		}
	});
	pinia._p.forEach((extender) => {
		assign(store, scope.run(() => extender({
			store,
			app: pinia._a,
			pinia,
			options: optionsForPlugin
		})));
	});
	if (initialState && isOptionsStore && options.hydrate) options.hydrate(store.$state, initialState);
	isListening = true;
	isSyncListening = true;
	return store;
}
/*! #__NO_SIDE_EFFECTS__ */
function defineStore(id, setup, setupOptions) {
	let options;
	const isSetupStore = typeof setup === "function";
	options = isSetupStore ? setupOptions : setup;
	function useStore(pinia, hot$1) {
		const hasContext = hasInjectionContext();
		pinia = pinia || (hasContext ? inject(piniaSymbol, null) : null);
		if (pinia) setActivePinia(pinia);
		pinia = activePinia;
		if (!pinia._s.has(id)) if (isSetupStore) createSetupStore(id, setup, options, pinia);
		else createOptionsStore(id, options, pinia);
		const store = pinia._s.get(id);
		return store;
	}
	useStore.$id = id;
	return useStore;
}
const scriptRel = "modulepreload";
const assetsURL = function(dep, importerUrl) {
	return new URL(dep, importerUrl).href;
};
const seen = {};
const __vitePreload = function preload(baseModule, deps, importerUrl) {
	let promise = Promise.resolve();
	if (deps && deps.length > 0) {
		const links = document.getElementsByTagName("link");
		const cspNonceMeta = document.querySelector("meta[property=csp-nonce]");
		const cspNonce = cspNonceMeta?.nonce || cspNonceMeta?.getAttribute("nonce");
		promise = Promise.allSettled(deps.map((dep) => {
			dep = assetsURL(dep, importerUrl);
			if (dep in seen) return;
			seen[dep] = true;
			const isCss = dep.endsWith(".css");
			const cssSelector = isCss ? "[rel=\"stylesheet\"]" : "";
			const isBaseRelative = !!importerUrl;
			if (isBaseRelative) for (let i = links.length - 1; i >= 0; i--) {
				const link2 = links[i];
				if (link2.href === dep && (!isCss || link2.rel === "stylesheet")) return;
			}
			else if (document.querySelector(`link[href="${dep}"]${cssSelector}`)) return;
			const link = document.createElement("link");
			link.rel = isCss ? "stylesheet" : scriptRel;
			if (!isCss) link.as = "script";
			link.crossOrigin = "";
			link.href = dep;
			if (cspNonce) link.setAttribute("nonce", cspNonce);
			document.head.appendChild(link);
			if (isCss) return new Promise((res, rej) => {
				link.addEventListener("load", res);
				link.addEventListener("error", () => rej(new Error(`Unable to preload CSS for ${dep}`)));
			});
		}));
	}
	function handlePreloadError(err) {
		const e = new Event("vite:preloadError", { cancelable: true });
		e.payload = err;
		window.dispatchEvent(e);
		if (!e.defaultPrevented) throw err;
	}
	return promise.then((res) => {
		for (const item of res || []) {
			if (item.status !== "rejected") continue;
			handlePreloadError(item.reason);
		}
		return baseModule().catch(handlePreloadError);
	});
};
function tryOnScopeDispose(fn) {
	if (getCurrentScope()) {
		onScopeDispose(fn);
		return true;
	}
	return false;
}
/* @__NO_SIDE_EFFECTS__ */
function createEventHook() {
	const fns = /* @__PURE__ */ new Set();
	const off = (fn) => {
		fns.delete(fn);
	};
	const clear = () => {
		fns.clear();
	};
	const on = (fn) => {
		fns.add(fn);
		const offFn = () => off(fn);
		tryOnScopeDispose(offFn);
		return { off: offFn };
	};
	const trigger = (...args) => {
		return Promise.all(Array.from(fns).map((fn) => fn(...args)));
	};
	return {
		on,
		off,
		trigger,
		clear
	};
}
const localProvidedStateMap = /* @__PURE__ */ new WeakMap();
const injectLocal = /* @__NO_SIDE_EFFECTS__ */ (...args) => {
	var _a;
	const key = args[0];
	const instance = (_a = getCurrentInstance()) == null ? void 0 : _a.proxy;
	if (instance == null && !hasInjectionContext()) throw new Error("injectLocal must be called in setup");
	if (instance && localProvidedStateMap.has(instance) && key in localProvidedStateMap.get(instance)) return localProvidedStateMap.get(instance)[key];
	return inject(...args);
};
const isClient = typeof window !== "undefined" && typeof document !== "undefined";
const isWorker = typeof WorkerGlobalScope !== "undefined" && globalThis instanceof WorkerGlobalScope;
const toString = Object.prototype.toString;
const isObject = (val) => toString.call(val) === "[object Object]";
const noop = () => {};
function toRef$1(...args) {
	if (args.length !== 1) return toRef(...args);
	const r = args[0];
	return typeof r === "function" ? readonly(customRef(() => ({
		get: r,
		set: noop
	}))) : ref(r);
}
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
const bypassFilter = (invoke) => {
	return invoke();
};
function pausableFilter(extendFilter = bypassFilter, options = {}) {
	const { initialState = "active" } = options;
	const isActive = toRef$1(initialState === "active");
	function pause() {
		isActive.value = false;
	}
	function resume() {
		isActive.value = true;
	}
	const eventFilter = (...args) => {
		if (isActive.value) extendFilter(...args);
	};
	return {
		isActive: readonly(isActive),
		pause,
		resume,
		eventFilter
	};
}
function pxValue(px) {
	return px.endsWith("rem") ? Number.parseFloat(px) * 16 : Number.parseFloat(px);
}
function toArray(value) {
	return Array.isArray(value) ? value : [value];
}
function cacheStringFunction(fn) {
	const cache = /* @__PURE__ */ Object.create(null);
	return (str) => {
		const hit = cache[str];
		return hit || (cache[str] = fn(str));
	};
}
const hyphenateRE = /\B([A-Z])/g;
const hyphenate = cacheStringFunction((str) => str.replace(hyphenateRE, "-$1").toLowerCase());
const camelizeRE = /-(\w)/g;
const camelize = cacheStringFunction((str) => {
	return str.replace(camelizeRE, (_, c) => c ? c.toUpperCase() : "");
});
function getLifeCycleTarget(target) {
	return target || getCurrentInstance();
}
function watchWithFilter(source, cb, options = {}) {
	const { eventFilter = bypassFilter,...watchOptions } = options;
	return watch(source, createFilterWrapper(eventFilter, cb), watchOptions);
}
function watchPausable(source, cb, options = {}) {
	const { eventFilter: filter, initialState = "active",...watchOptions } = options;
	const { eventFilter, pause, resume, isActive } = pausableFilter(filter, { initialState });
	const stop = watchWithFilter(source, cb, {
		...watchOptions,
		eventFilter
	});
	return {
		stop,
		pause,
		resume,
		isActive
	};
}
function tryOnMounted(fn, sync = true, target) {
	const instance = getLifeCycleTarget(target);
	if (instance) onMounted(fn, target);
	else if (sync) fn();
	else nextTick(fn);
}
/* @__NO_SIDE_EFFECTS__ */
function useToggle(initialValue = false, options = {}) {
	const { truthyValue = true, falsyValue = false } = options;
	const valueIsRef = isRef(initialValue);
	const _value = shallowRef(initialValue);
	function toggle(value) {
		if (arguments.length) {
			_value.value = value;
			return _value.value;
		} else {
			const truthy = toValue(truthyValue);
			_value.value = _value.value === truthy ? toValue(falsyValue) : truthy;
			return _value.value;
		}
	}
	if (valueIsRef) return toggle;
	else return [_value, toggle];
}
function watchImmediate(source, cb, options) {
	return watch(source, cb, {
		...options,
		immediate: true
	});
}
const defaultWindow = isClient ? window : void 0;
const defaultDocument = isClient ? window.document : void 0;
const defaultNavigator = isClient ? window.navigator : void 0;
const defaultLocation = isClient ? window.location : void 0;
function unrefElement(elRef) {
	var _a;
	const plain = toValue(elRef);
	return (_a = plain == null ? void 0 : plain.$el) != null ? _a : plain;
}
function useEventListener(...args) {
	const cleanups = [];
	const cleanup = () => {
		cleanups.forEach((fn) => fn());
		cleanups.length = 0;
	};
	const register = (el, event, listener, options) => {
		el.addEventListener(event, listener, options);
		return () => el.removeEventListener(event, listener, options);
	};
	const firstParamTargets = computed(() => {
		const test = toArray(toValue(args[0])).filter((e) => e != null);
		return test.every((e) => typeof e !== "string") ? test : void 0;
	});
	const stopWatch = watchImmediate(() => {
		var _a, _b;
		return [
			(_b = (_a = firstParamTargets.value) == null ? void 0 : _a.map((e) => unrefElement(e))) != null ? _b : [defaultWindow].filter((e) => e != null),
			toArray(toValue(firstParamTargets.value ? args[1] : args[0])),
			toArray(unref(firstParamTargets.value ? args[2] : args[1])),
			toValue(firstParamTargets.value ? args[3] : args[2])
		];
	}, ([raw_targets, raw_events, raw_listeners, raw_options]) => {
		cleanup();
		if (!(raw_targets == null ? void 0 : raw_targets.length) || !(raw_events == null ? void 0 : raw_events.length) || !(raw_listeners == null ? void 0 : raw_listeners.length)) return;
		const optionsClone = isObject(raw_options) ? { ...raw_options } : raw_options;
		cleanups.push(...raw_targets.flatMap((el) => raw_events.flatMap((event) => raw_listeners.map((listener) => register(el, event, listener, optionsClone)))));
	}, { flush: "post" });
	const stop = () => {
		stopWatch();
		cleanup();
	};
	tryOnScopeDispose(cleanup);
	return stop;
}
/* @__NO_SIDE_EFFECTS__ */
function useMounted() {
	const isMounted = shallowRef(false);
	const instance = getCurrentInstance();
	if (instance) onMounted(() => {
		isMounted.value = true;
	}, instance);
	return isMounted;
}
/* @__NO_SIDE_EFFECTS__ */
function useSupported(callback) {
	const isMounted = /* @__PURE__ */ useMounted();
	return computed(() => {
		isMounted.value;
		return Boolean(callback());
	});
}
const ssrWidthSymbol = Symbol("vueuse-ssr-width");
/* @__NO_SIDE_EFFECTS__ */
function useSSRWidth() {
	const ssrWidth = hasInjectionContext() ? /* @__PURE__ */ injectLocal(ssrWidthSymbol, null) : null;
	return typeof ssrWidth === "number" ? ssrWidth : void 0;
}
function useMediaQuery(query, options = {}) {
	const { window: window$1 = defaultWindow, ssrWidth = /* @__PURE__ */ useSSRWidth() } = options;
	const isSupported = /* @__PURE__ */ useSupported(() => window$1 && "matchMedia" in window$1 && typeof window$1.matchMedia === "function");
	const ssrSupport = shallowRef(typeof ssrWidth === "number");
	const mediaQuery = shallowRef();
	const matches = shallowRef(false);
	const handler = (event) => {
		matches.value = event.matches;
	};
	watchEffect(() => {
		if (ssrSupport.value) {
			ssrSupport.value = !isSupported.value;
			const queryStrings = toValue(query).split(",");
			matches.value = queryStrings.some((queryString) => {
				const not = queryString.includes("not all");
				const minWidth = queryString.match(/\(\s*min-width:\s*(-?\d+(?:\.\d*)?[a-z]+\s*)\)/);
				const maxWidth = queryString.match(/\(\s*max-width:\s*(-?\d+(?:\.\d*)?[a-z]+\s*)\)/);
				let res = Boolean(minWidth || maxWidth);
				if (minWidth && res) res = ssrWidth >= pxValue(minWidth[1]);
				if (maxWidth && res) res = ssrWidth <= pxValue(maxWidth[1]);
				return not ? !res : res;
			});
			return;
		}
		if (!isSupported.value) return;
		mediaQuery.value = window$1.matchMedia(toValue(query));
		matches.value = mediaQuery.value.matches;
	});
	useEventListener(mediaQuery, "change", handler, { passive: true });
	return computed(() => matches.value);
}
const _global = typeof globalThis !== "undefined" ? globalThis : typeof window !== "undefined" ? window : typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : {};
const globalKey = "__vueuse_ssr_handlers__";
const handlers = /* @__PURE__ */ getHandlers();
function getHandlers() {
	if (!(globalKey in _global)) _global[globalKey] = _global[globalKey] || {};
	return _global[globalKey];
}
function getSSRHandler(key, fallback) {
	return handlers[key] || fallback;
}
/* @__NO_SIDE_EFFECTS__ */
function usePreferredDark(options) {
	return useMediaQuery("(prefers-color-scheme: dark)", options);
}
function guessSerializerType(rawInit) {
	return rawInit == null ? "any" : rawInit instanceof Set ? "set" : rawInit instanceof Map ? "map" : rawInit instanceof Date ? "date" : typeof rawInit === "boolean" ? "boolean" : typeof rawInit === "string" ? "string" : typeof rawInit === "object" ? "object" : !Number.isNaN(rawInit) ? "number" : "any";
}
const StorageSerializers = {
	boolean: {
		read: (v) => v === "true",
		write: (v) => String(v)
	},
	object: {
		read: (v) => JSON.parse(v),
		write: (v) => JSON.stringify(v)
	},
	number: {
		read: (v) => Number.parseFloat(v),
		write: (v) => String(v)
	},
	any: {
		read: (v) => v,
		write: (v) => String(v)
	},
	string: {
		read: (v) => v,
		write: (v) => String(v)
	},
	map: {
		read: (v) => new Map(JSON.parse(v)),
		write: (v) => JSON.stringify(Array.from(v.entries()))
	},
	set: {
		read: (v) => new Set(JSON.parse(v)),
		write: (v) => JSON.stringify(Array.from(v))
	},
	date: {
		read: (v) => new Date(v),
		write: (v) => v.toISOString()
	}
};
const customStorageEventName = "vueuse-storage";
function useStorage(key, defaults, storage, options = {}) {
	var _a;
	const { flush = "pre", deep = true, listenToStorageChanges = true, writeDefaults = true, mergeDefaults = false, shallow, window: window$1 = defaultWindow, eventFilter, onError = (e) => {
		console.error(e);
	}, initOnMounted } = options;
	const data = (shallow ? shallowRef : ref)(typeof defaults === "function" ? defaults() : defaults);
	const keyComputed = computed(() => toValue(key));
	if (!storage) try {
		storage = getSSRHandler("getDefaultStorage", () => {
			var _a2;
			return (_a2 = defaultWindow) == null ? void 0 : _a2.localStorage;
		})();
	} catch (e) {
		onError(e);
	}
	if (!storage) return data;
	const rawInit = toValue(defaults);
	const type = guessSerializerType(rawInit);
	const serializer = (_a = options.serializer) != null ? _a : StorageSerializers[type];
	const { pause: pauseWatch, resume: resumeWatch } = watchPausable(data, (newValue) => write(newValue), {
		flush,
		deep,
		eventFilter
	});
	watch(keyComputed, () => update(), { flush });
	let firstMounted = false;
	const onStorageEvent = (ev) => {
		if (initOnMounted && !firstMounted) return;
		update(ev);
	};
	const onStorageCustomEvent = (ev) => {
		if (initOnMounted && !firstMounted) return;
		updateFromCustomEvent(ev);
	};
	if (window$1 && listenToStorageChanges) if (storage instanceof Storage) useEventListener(window$1, "storage", onStorageEvent, { passive: true });
	else useEventListener(window$1, customStorageEventName, onStorageCustomEvent);
	if (initOnMounted) tryOnMounted(() => {
		firstMounted = true;
		update();
	});
	else update();
	function dispatchWriteEvent(oldValue, newValue) {
		if (window$1) {
			const payload = {
				key: keyComputed.value,
				oldValue,
				newValue,
				storageArea: storage
			};
			window$1.dispatchEvent(storage instanceof Storage ? new StorageEvent("storage", payload) : new CustomEvent(customStorageEventName, { detail: payload }));
		}
	}
	function write(v) {
		try {
			const oldValue = storage.getItem(keyComputed.value);
			if (v == null) {
				dispatchWriteEvent(oldValue, null);
				storage.removeItem(keyComputed.value);
			} else {
				const serialized = serializer.write(v);
				if (oldValue !== serialized) {
					storage.setItem(keyComputed.value, serialized);
					dispatchWriteEvent(oldValue, serialized);
				}
			}
		} catch (e) {
			onError(e);
		}
	}
	function read(event) {
		const rawValue = event ? event.newValue : storage.getItem(keyComputed.value);
		if (rawValue == null) {
			if (writeDefaults && rawInit != null) storage.setItem(keyComputed.value, serializer.write(rawInit));
			return rawInit;
		} else if (!event && mergeDefaults) {
			const value = serializer.read(rawValue);
			if (typeof mergeDefaults === "function") return mergeDefaults(value, rawInit);
			else if (type === "object" && !Array.isArray(value)) return {
				...rawInit,
				...value
			};
			return value;
		} else if (typeof rawValue !== "string") return rawValue;
		else return serializer.read(rawValue);
	}
	function update(event) {
		if (event && event.storageArea !== storage) return;
		if (event && event.key == null) {
			data.value = rawInit;
			return;
		}
		if (event && event.key !== keyComputed.value) return;
		pauseWatch();
		try {
			const serializedData = serializer.write(data.value);
			if (event === void 0 || (event == null ? void 0 : event.newValue) !== serializedData) data.value = read(event);
		} catch (e) {
			onError(e);
		} finally {
			if (event) nextTick(resumeWatch);
			else resumeWatch();
		}
	}
	function updateFromCustomEvent(event) {
		update(event.detail);
	}
	return data;
}
const CSS_DISABLE_TRANS = "*,*::before,*::after{-webkit-transition:none!important;-moz-transition:none!important;-o-transition:none!important;-ms-transition:none!important;transition:none!important}";
function useColorMode(options = {}) {
	const { selector = "html", attribute = "class", initialValue = "auto", window: window$1 = defaultWindow, storage, storageKey = "vueuse-color-scheme", listenToStorageChanges = true, storageRef, emitAuto, disableTransition = true } = options;
	const modes = {
		auto: "",
		light: "light",
		dark: "dark",
		...options.modes || {}
	};
	const preferredDark = /* @__PURE__ */ usePreferredDark({ window: window$1 });
	const system = computed(() => preferredDark.value ? "dark" : "light");
	const store = storageRef || (storageKey == null ? toRef$1(initialValue) : useStorage(storageKey, initialValue, storage, {
		window: window$1,
		listenToStorageChanges
	}));
	const state = computed(() => store.value === "auto" ? system.value : store.value);
	const updateHTMLAttrs = getSSRHandler("updateHTMLAttrs", (selector2, attribute2, value) => {
		const el = typeof selector2 === "string" ? window$1 == null ? void 0 : window$1.document.querySelector(selector2) : unrefElement(selector2);
		if (!el) return;
		const classesToAdd = /* @__PURE__ */ new Set();
		const classesToRemove = /* @__PURE__ */ new Set();
		let attributeToChange = null;
		if (attribute2 === "class") {
			const current = value.split(/\s/g);
			Object.values(modes).flatMap((i) => (i || "").split(/\s/g)).filter(Boolean).forEach((v) => {
				if (current.includes(v)) classesToAdd.add(v);
				else classesToRemove.add(v);
			});
		} else attributeToChange = {
			key: attribute2,
			value
		};
		if (classesToAdd.size === 0 && classesToRemove.size === 0 && attributeToChange === null) return;
		let style;
		if (disableTransition) {
			style = window$1.document.createElement("style");
			style.appendChild(document.createTextNode(CSS_DISABLE_TRANS));
			window$1.document.head.appendChild(style);
		}
		for (const c of classesToAdd) el.classList.add(c);
		for (const c of classesToRemove) el.classList.remove(c);
		if (attributeToChange) el.setAttribute(attributeToChange.key, attributeToChange.value);
		if (disableTransition) {
			window$1.getComputedStyle(style).opacity;
			document.head.removeChild(style);
		}
	});
	function defaultOnChanged(mode) {
		var _a;
		updateHTMLAttrs(selector, attribute, (_a = modes[mode]) != null ? _a : mode);
	}
	function onChanged(mode) {
		if (options.onChanged) options.onChanged(mode, defaultOnChanged);
		else defaultOnChanged(mode);
	}
	watch(state, onChanged, {
		flush: "post",
		immediate: true
	});
	tryOnMounted(() => onChanged(state.value));
	const auto = computed({
		get() {
			return emitAuto ? store.value : state.value;
		},
		set(v) {
			store.value = v;
		}
	});
	return Object.assign(auto, {
		store,
		system,
		state
	});
}
function useDark(options = {}) {
	const { valueDark = "dark", valueLight = "" } = options;
	const mode = useColorMode({
		...options,
		onChanged: (mode2, defaultHandler) => {
			var _a;
			if (options.onChanged) (_a = options.onChanged) == null || _a.call(options, mode2 === "dark", defaultHandler, mode2);
			else defaultHandler(mode2);
		},
		modes: {
			dark: valueDark,
			light: valueLight
		}
	});
	const system = computed(() => mode.system.value);
	const isDark$1 = computed({
		get() {
			return mode.value === "dark";
		},
		set(v) {
			const modeVal = v ? "dark" : "light";
			if (system.value === modeVal) mode.value = "auto";
			else mode.value = modeVal;
		}
	});
	return isDark$1;
}
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
	const targets = computed(() => {
		const _targets = toValue(target);
		return Array.isArray(_targets) ? _targets.map((el) => unrefElement(el)) : [unrefElement(_targets)];
	});
	const stopWatch = watch(targets, (els) => {
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
function useElementSize(target, initialSize = {
	width: 0,
	height: 0
}, options = {}) {
	const { window: window$1 = defaultWindow, box = "content-box" } = options;
	const isSVG = computed(() => {
		var _a, _b;
		return (_b = (_a = unrefElement(target)) == null ? void 0 : _a.namespaceURI) == null ? void 0 : _b.includes("svg");
	});
	const width = shallowRef(initialSize.width);
	const height = shallowRef(initialSize.height);
	const { stop: stop1 } = useResizeObserver(target, ([entry]) => {
		const boxSize = box === "border-box" ? entry.borderBoxSize : box === "content-box" ? entry.contentBoxSize : entry.devicePixelContentBoxSize;
		if (window$1 && isSVG.value) {
			const $elem = unrefElement(target);
			if ($elem) {
				const rect = $elem.getBoundingClientRect();
				width.value = rect.width;
				height.value = rect.height;
			}
		} else if (boxSize) {
			const formatBoxSize = toArray(boxSize);
			width.value = formatBoxSize.reduce((acc, { inlineSize }) => acc + inlineSize, 0);
			height.value = formatBoxSize.reduce((acc, { blockSize }) => acc + blockSize, 0);
		} else {
			width.value = entry.contentRect.width;
			height.value = entry.contentRect.height;
		}
	}, options);
	tryOnMounted(() => {
		const ele = unrefElement(target);
		if (ele) {
			width.value = "offsetWidth" in ele ? ele.offsetWidth : initialSize.width;
			height.value = "offsetHeight" in ele ? ele.offsetHeight : initialSize.height;
		}
	});
	const stop2 = watch(() => unrefElement(target), (ele) => {
		width.value = ele ? initialSize.width : 0;
		height.value = ele ? initialSize.height : 0;
	});
	function stop() {
		stop1();
		stop2();
	}
	return {
		width,
		height,
		stop
	};
}
function useLocalStorage(key, initialValue, options = {}) {
	const { window: window$1 = defaultWindow } = options;
	return useStorage(key, initialValue, window$1 == null ? void 0 : window$1.localStorage, options);
}
const DEFAULT_UNITS = [
	{
		max: 6e4,
		value: 1e3,
		name: "second"
	},
	{
		max: 276e4,
		value: 6e4,
		name: "minute"
	},
	{
		max: 72e6,
		value: 36e5,
		name: "hour"
	},
	{
		max: 5184e5,
		value: 864e5,
		name: "day"
	},
	{
		max: 24192e5,
		value: 6048e5,
		name: "week"
	},
	{
		max: 28512e6,
		value: 2592e6,
		name: "month"
	},
	{
		max: Number.POSITIVE_INFINITY,
		value: 31536e6,
		name: "year"
	}
];
function useVirtualList(list, options) {
	const { containerStyle, wrapperProps, scrollTo, calculateRange, currentList, containerRef } = "itemHeight" in options ? useVerticalVirtualList(options, list) : useHorizontalVirtualList(options, list);
	return {
		list: currentList,
		scrollTo,
		containerProps: {
			ref: containerRef,
			onScroll: () => {
				calculateRange();
			},
			style: containerStyle
		},
		wrapperProps
	};
}
function useVirtualListResources(list) {
	const containerRef = shallowRef(null);
	const size = useElementSize(containerRef);
	const currentList = ref([]);
	const source = shallowRef(list);
	const state = ref({
		start: 0,
		end: 10
	});
	return {
		state,
		source,
		currentList,
		size,
		containerRef
	};
}
function createGetViewCapacity(state, source, itemSize) {
	return (containerSize) => {
		if (typeof itemSize === "number") return Math.ceil(containerSize / itemSize);
		const { start = 0 } = state.value;
		let sum = 0;
		let capacity = 0;
		for (let i = start; i < source.value.length; i++) {
			const size = itemSize(i);
			sum += size;
			capacity = i;
			if (sum > containerSize) break;
		}
		return capacity - start;
	};
}
function createGetOffset(source, itemSize) {
	return (scrollDirection) => {
		if (typeof itemSize === "number") return Math.floor(scrollDirection / itemSize) + 1;
		let sum = 0;
		let offset = 0;
		for (let i = 0; i < source.value.length; i++) {
			const size = itemSize(i);
			sum += size;
			if (sum >= scrollDirection) {
				offset = i;
				break;
			}
		}
		return offset + 1;
	};
}
function createCalculateRange(type, overscan, getOffset, getViewCapacity, { containerRef, state, currentList, source }) {
	return () => {
		const element = containerRef.value;
		if (element) {
			const offset = getOffset(type === "vertical" ? element.scrollTop : element.scrollLeft);
			const viewCapacity = getViewCapacity(type === "vertical" ? element.clientHeight : element.clientWidth);
			const from = offset - overscan;
			const to = offset + viewCapacity + overscan;
			state.value = {
				start: from < 0 ? 0 : from,
				end: to > source.value.length ? source.value.length : to
			};
			currentList.value = source.value.slice(state.value.start, state.value.end).map((ele, index) => ({
				data: ele,
				index: index + state.value.start
			}));
		}
	};
}
function createGetDistance(itemSize, source) {
	return (index) => {
		if (typeof itemSize === "number") {
			const size2 = index * itemSize;
			return size2;
		}
		const size = source.value.slice(0, index).reduce((sum, _, i) => sum + itemSize(i), 0);
		return size;
	};
}
function useWatchForSizes(size, list, containerRef, calculateRange) {
	watch([
		size.width,
		size.height,
		() => toValue(list),
		containerRef
	], () => {
		calculateRange();
	});
}
function createComputedTotalSize(itemSize, source) {
	return computed(() => {
		if (typeof itemSize === "number") return source.value.length * itemSize;
		return source.value.reduce((sum, _, index) => sum + itemSize(index), 0);
	});
}
const scrollToDictionaryForElementScrollKey = {
	horizontal: "scrollLeft",
	vertical: "scrollTop"
};
function createScrollTo(type, calculateRange, getDistance, containerRef) {
	return (index) => {
		if (containerRef.value) {
			containerRef.value[scrollToDictionaryForElementScrollKey[type]] = getDistance(index);
			calculateRange();
		}
	};
}
function useHorizontalVirtualList(options, list) {
	const resources = useVirtualListResources(list);
	const { state, source, currentList, size, containerRef } = resources;
	const containerStyle = { overflowX: "auto" };
	const { itemWidth, overscan = 5 } = options;
	const getViewCapacity = createGetViewCapacity(state, source, itemWidth);
	const getOffset = createGetOffset(source, itemWidth);
	const calculateRange = createCalculateRange("horizontal", overscan, getOffset, getViewCapacity, resources);
	const getDistanceLeft = createGetDistance(itemWidth, source);
	const offsetLeft = computed(() => getDistanceLeft(state.value.start));
	const totalWidth = createComputedTotalSize(itemWidth, source);
	useWatchForSizes(size, list, containerRef, calculateRange);
	const scrollTo = createScrollTo("horizontal", calculateRange, getDistanceLeft, containerRef);
	const wrapperProps = computed(() => {
		return { style: {
			height: "100%",
			width: `${totalWidth.value - offsetLeft.value}px`,
			marginLeft: `${offsetLeft.value}px`,
			display: "flex"
		} };
	});
	return {
		scrollTo,
		calculateRange,
		wrapperProps,
		containerStyle,
		currentList,
		containerRef
	};
}
function useVerticalVirtualList(options, list) {
	const resources = useVirtualListResources(list);
	const { state, source, currentList, size, containerRef } = resources;
	const containerStyle = { overflowY: "auto" };
	const { itemHeight, overscan = 5 } = options;
	const getViewCapacity = createGetViewCapacity(state, source, itemHeight);
	const getOffset = createGetOffset(source, itemHeight);
	const calculateRange = createCalculateRange("vertical", overscan, getOffset, getViewCapacity, resources);
	const getDistanceTop = createGetDistance(itemHeight, source);
	const offsetTop = computed(() => getDistanceTop(state.value.start));
	const totalHeight = createComputedTotalSize(itemHeight, source);
	useWatchForSizes(size, list, containerRef, calculateRange);
	const scrollTo = createScrollTo("vertical", calculateRange, getDistanceTop, containerRef);
	const wrapperProps = computed(() => {
		return { style: {
			width: "100%",
			height: `${totalHeight.value - offsetTop.value}px`,
			marginTop: `${offsetTop.value}px`
		} };
	});
	return {
		calculateRange,
		scrollTo,
		containerStyle,
		wrapperProps,
		currentList,
		containerRef
	};
}
const isDark = useDark();
const toggleDark = /* @__PURE__ */ useToggle(isDark);
const TYPE_REQUEST = "q";
const TYPE_RESPONSE = "s";
const DEFAULT_TIMEOUT = 6e4;
function defaultSerialize(i) {
	return i;
}
const defaultDeserialize = defaultSerialize;
const { clearTimeout: clearTimeout$1, setTimeout: setTimeout$1 } = globalThis;
const random = Math.random.bind(Math);
function createBirpc(functions, options) {
	const { post, on, off = () => {}, eventNames = [], serialize = defaultSerialize, deserialize = defaultDeserialize, resolver, bind = "rpc", timeout = DEFAULT_TIMEOUT } = options;
	const rpcPromiseMap = /* @__PURE__ */ new Map();
	let _promise;
	let closed = false;
	const rpc$1 = new Proxy({}, { get(_, method) {
		if (method === "$functions") return functions;
		if (method === "$close") return close;
		if (method === "$closed") return closed;
		if (method === "then" && !eventNames.includes("then") && !("then" in functions)) return void 0;
		const sendEvent = (...args) => {
			post(serialize({
				m: method,
				a: args,
				t: TYPE_REQUEST
			}));
		};
		if (eventNames.includes(method)) {
			sendEvent.asEvent = sendEvent;
			return sendEvent;
		}
		const sendCall = async (...args) => {
			if (closed) throw new Error(`[birpc] rpc is closed, cannot call "${method}"`);
			if (_promise) try {
				await _promise;
			} finally {
				_promise = void 0;
			}
			return new Promise((resolve, reject) => {
				const id = nanoid();
				let timeoutId;
				if (timeout >= 0) {
					timeoutId = setTimeout$1(() => {
						try {
							const handleResult = options.onTimeoutError?.(method, args);
							if (handleResult !== true) throw new Error(`[birpc] timeout on calling "${method}"`);
						} catch (e) {
							reject(e);
						}
						rpcPromiseMap.delete(id);
					}, timeout);
					if (typeof timeoutId === "object") timeoutId = timeoutId.unref?.();
				}
				rpcPromiseMap.set(id, {
					resolve,
					reject,
					timeoutId,
					method
				});
				post(serialize({
					m: method,
					a: args,
					i: id,
					t: "q"
				}));
			});
		};
		sendCall.asEvent = sendEvent;
		return sendCall;
	} });
	function close(error) {
		closed = true;
		rpcPromiseMap.forEach(({ reject, method }) => {
			reject(error || new Error(`[birpc] rpc is closed, cannot call "${method}"`));
		});
		rpcPromiseMap.clear();
		off(onMessage);
	}
	async function onMessage(data, ...extra) {
		let msg;
		try {
			msg = deserialize(data);
		} catch (e) {
			if (options.onGeneralError?.(e) !== true) throw e;
			return;
		}
		if (msg.t === TYPE_REQUEST) {
			const { m: method, a: args } = msg;
			let result, error;
			const fn = resolver ? resolver(method, functions[method]) : functions[method];
			if (!fn) error = new Error(`[birpc] function "${method}" not found`);
			else try {
				result = await fn.apply(bind === "rpc" ? rpc$1 : functions, args);
			} catch (e) {
				error = e;
			}
			if (msg.i) {
				if (error && options.onError) options.onError(error, method, args);
				if (error && options.onFunctionError) {
					if (options.onFunctionError(error, method, args) === true) return;
				}
				if (!error) try {
					post(serialize({
						t: TYPE_RESPONSE,
						i: msg.i,
						r: result
					}), ...extra);
					return;
				} catch (e) {
					error = e;
					if (options.onGeneralError?.(e, method, args) !== true) throw e;
				}
				try {
					post(serialize({
						t: TYPE_RESPONSE,
						i: msg.i,
						e: error
					}), ...extra);
				} catch (e) {
					if (options.onGeneralError?.(e, method, args) !== true) throw e;
				}
			}
		} else {
			const { i: ack, r: result, e: error } = msg;
			const promise = rpcPromiseMap.get(ack);
			if (promise) {
				clearTimeout$1(promise.timeoutId);
				if (error) promise.reject(error);
				else promise.resolve(result);
			}
			rpcPromiseMap.delete(ack);
		}
	}
	_promise = on(onMessage);
	return rpc$1;
}
const urlAlphabet = "useandom-26T198340PX75pxJACKVERYMINDBUSHWOLF_GQZbfghjklqvwyzrict";
function nanoid(size = 21) {
	let id = "";
	let i = size;
	while (i--) id += urlAlphabet[random() * 64 | 0];
	return id;
}
function createRPCClient(name, hot$1, functions = {}, options = {}) {
	const event = `${name}:rpc`;
	const promise = Promise.resolve(hot$1).then((r) => {
		if (!r) console.warn("[vite-hot-client] Received undefined hot context, RPC calls are ignored");
		return r;
	});
	return createBirpc(functions, {
		...options,
		on: async (fn) => {
			(await promise)?.on(event, fn);
		},
		post: async (data) => {
			(await promise)?.send(event, data);
		}
	});
}
async function getViteClient(base = "/", warning = true) {
	try {
		const url = `${base}@vite/client`;
		const res = await fetch(url);
		const text = await res.text();
		if (text.startsWith("<") || !res.headers.get("content-type")?.includes("javascript")) throw new Error("Not javascript");
		return await import(
			/* @vite-ignore */
			url
);
	} catch {
		if (warning) console.error(`[vite-hot-client] Failed to import "${base}@vite/client"`);
	}
	return void 0;
}
async function createHotContext(path = "/____", base = "/") {
	const viteClient = await getViteClient(base);
	return viteClient?.createHotContext(path);
}
const dataCache = new Map();
function fetchJson(url) {
	if (!dataCache.has(url)) dataCache.set(url, fetch(url).then((r) => r.json()));
	return dataCache.get(url);
}
function createStaticRpcClient() {
	async function getModuleTransformInfo(query, id) {
		const { hash } = await __vitePreload(async () => {
			const { hash: hash$1 } = await import("./dist-Dp-WpU5V.js");
			return { hash: hash$1 };
		}, [], import.meta.url);
		return fetchJson(`./reports/${query.vite}-${query.env}/transforms/${hash(id)}.json`);
	}
	return {
		getMetadata: () => fetchJson("./reports/metadata.json"),
		getModulesList: (query) => fetchJson(`./reports/${query.vite}-${query.env}/modules.json`),
		getPluginMetrics: (query) => fetchJson(`./reports/${query.vite}-${query.env}/metric-plugins.json`),
		getModuleTransformInfo,
		resolveId: (query, id) => getModuleTransformInfo(query, id).then((r) => r.resolvedId),
		onModuleUpdated: async () => void 0,
		getServerMetrics: async () => ({})
	};
}
const onModuleUpdated = /* @__PURE__ */ createEventHook();
const isStaticMode = document.body.getAttribute("data-vite-inspect-mode") === "BUILD";
const hot = createHotContext("/___", `${location.pathname.split("/__inspect")[0] || ""}/`.replace(/\/\//g, "/"));
const rpc = isStaticMode ? createStaticRpcClient() : createRPCClient("vite-plugin-inspect", hot, { async onModuleUpdated() {
	onModuleUpdated.trigger();
} });
function guessMode(code) {
	if (code.trimStart().startsWith("<")) return "htmlmixed";
	if (code.match(/^import\s/)) return "javascript";
	if (code.match(/^[.#].+\{/)) return "css";
	return "javascript";
}
function inspectSourcemaps({ code, sourcemaps }) {
	console.info("sourcemaps", JSON.stringify(sourcemaps, null, 2));
	const serialized = serializeForSourcemapsVisualizer(code, sourcemaps);
	window.open(`https://evanw.github.io/source-map-visualization#${serialized}`, "_blank");
}
function safeJsonParse(str) {
	try {
		return JSON.parse(str);
	} catch {
		console.error("Failed to parse JSON", str);
		return null;
	}
}
function serializeForSourcemapsVisualizer(code, map) {
	const encoder = new TextEncoder();
	const codeArray = encoder.encode(code);
	const mapArray = encoder.encode(map);
	const codeLengthArray = encoder.encode(codeArray.length.toString());
	const mapLengthArray = encoder.encode(mapArray.length.toString());
	const combinedArray = new Uint8Array(codeLengthArray.length + 1 + codeArray.length + mapLengthArray.length + 1 + mapArray.length);
	combinedArray.set(codeLengthArray);
	combinedArray.set([0], codeLengthArray.length);
	combinedArray.set(codeArray, codeLengthArray.length + 1);
	combinedArray.set(mapLengthArray, codeLengthArray.length + 1 + codeArray.length);
	combinedArray.set([0], codeLengthArray.length + 1 + codeArray.length + mapLengthArray.length);
	combinedArray.set(mapArray, codeLengthArray.length + 1 + codeArray.length + mapLengthArray.length + 1);
	let binary = "";
	const len = combinedArray.byteLength;
	for (let i = 0; i < len; i++) binary += String.fromCharCode(combinedArray[i]);
	return btoa(binary);
}
const usePayloadStore = defineStore("payload", () => {
	const isLoading = ref(false);
	const metadata = shallowRef({ instances: [] });
	const query = useLocalStorage("vite-inspect-v1-query", {
		vite: "",
		env: ""
	}, { mergeDefaults: true });
	const modules = shallowRef([]);
	const queryCache = new Map();
	async function init() {
		metadata.value = await rpc.getMetadata();
		if (!metadata.value.instances.some((i) => i.vite === query.value.vite)) query.value.vite = metadata.value.instances[0].vite;
		if (!metadata.value.instances.some((i) => i.vite === query.value.vite && i.environments.includes(query.value.env))) {
			const instance$1 = metadata.value.instances.find((i) => i.vite === query.value.vite);
			if (instance$1) query.value.env = instance$1.environments[0] || "client";
			else query.value.env = metadata.value.instances[0].environments[0] || "client";
		}
		await doQuery();
		watch(query, async () => {
			await doQuery();
		}, { deep: true });
		onModuleUpdated.on(() => refetch());
	}
	async function doQuery() {
		const key = `${query.value.vite}-${query.value.env}`;
		if (!queryCache.has(key)) queryCache.set(key, rpc.getModulesList(query.value));
		isLoading.value = true;
		modules.value = [];
		try {
			modules.value = Object.freeze(await queryCache.get(key));
		} finally {
			isLoading.value = false;
		}
	}
	async function refetch(force = false) {
		queryCache.clear();
		if (force) metadata.value = await rpc.getMetadata();
		await doQuery();
	}
	const instance = computed(() => metadata.value.instances.find((i) => i.vite === query.value.vite));
	const root = computed(() => instance.value.root);
	return {
		init,
		metadata,
		query,
		modules,
		instance,
		root,
		isLoading,
		isStatic: isStaticMode,
		refetch
	};
});
export { __vitePreload, createHotContext, createPinia, defineStore, guessMode, inspectSourcemaps, isDark, isStaticMode, onModuleUpdated, rpc, safeJsonParse, toggleDark, tryOnScopeDispose, useLocalStorage, usePayloadStore, useVirtualList };
