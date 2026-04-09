Object.defineProperty(exports, Symbol.toStringTag, { value: "Module" });
let _vue_devtools_shared = require("@vue/devtools-shared");
let _vue_devtools_kit = require("@vue/devtools-kit");
let vue = require("vue");
//#region src/client.ts
function setDevToolsClientUrl(url) {
	_vue_devtools_shared.target.__VUE_DEVTOOLS_CLIENT_URL__ = url;
}
function getDevToolsClientUrl() {
	return _vue_devtools_shared.target.__VUE_DEVTOOLS_CLIENT_URL__ ?? (() => {
		if (_vue_devtools_shared.isBrowser) {
			const devtoolsMeta = document.querySelector("meta[name=__VUE_DEVTOOLS_CLIENT_URL__]");
			if (devtoolsMeta) return devtoolsMeta.getAttribute("content");
		}
		return "";
	})();
}
//#endregion
//#region ../../node_modules/.pnpm/hookable@5.5.3/node_modules/hookable/dist/index.mjs
function flatHooks(configHooks, hooks = {}, parentName) {
	for (const key in configHooks) {
		const subHook = configHooks[key];
		const name = parentName ? `${parentName}:${key}` : key;
		if (typeof subHook === "object" && subHook !== null) flatHooks(subHook, hooks, name);
		else if (typeof subHook === "function") hooks[name] = subHook;
	}
	return hooks;
}
const defaultTask = { run: (function_) => function_() };
const _createTask = () => defaultTask;
const createTask = typeof console.createTask !== "undefined" ? console.createTask : _createTask;
function serialTaskCaller(hooks, args) {
	const task = createTask(args.shift());
	return hooks.reduce((promise, hookFunction) => promise.then(() => task.run(() => hookFunction(...args))), Promise.resolve());
}
function parallelTaskCaller(hooks, args) {
	const task = createTask(args.shift());
	return Promise.all(hooks.map((hook) => task.run(() => hook(...args))));
}
function callEachWith(callbacks, arg0) {
	for (const callback of [...callbacks]) callback(arg0);
}
var Hookable = class {
	constructor() {
		this._hooks = {};
		this._before = void 0;
		this._after = void 0;
		this._deprecatedMessages = void 0;
		this._deprecatedHooks = {};
		this.hook = this.hook.bind(this);
		this.callHook = this.callHook.bind(this);
		this.callHookWith = this.callHookWith.bind(this);
	}
	hook(name, function_, options = {}) {
		if (!name || typeof function_ !== "function") return () => {};
		const originalName = name;
		let dep;
		while (this._deprecatedHooks[name]) {
			dep = this._deprecatedHooks[name];
			name = dep.to;
		}
		if (dep && !options.allowDeprecated) {
			let message = dep.message;
			if (!message) message = `${originalName} hook has been deprecated` + (dep.to ? `, please use ${dep.to}` : "");
			if (!this._deprecatedMessages) this._deprecatedMessages = /* @__PURE__ */ new Set();
			if (!this._deprecatedMessages.has(message)) {
				console.warn(message);
				this._deprecatedMessages.add(message);
			}
		}
		if (!function_.name) try {
			Object.defineProperty(function_, "name", {
				get: () => "_" + name.replace(/\W+/g, "_") + "_hook_cb",
				configurable: true
			});
		} catch {}
		this._hooks[name] = this._hooks[name] || [];
		this._hooks[name].push(function_);
		return () => {
			if (function_) {
				this.removeHook(name, function_);
				function_ = void 0;
			}
		};
	}
	hookOnce(name, function_) {
		let _unreg;
		let _function = (...arguments_) => {
			if (typeof _unreg === "function") _unreg();
			_unreg = void 0;
			_function = void 0;
			return function_(...arguments_);
		};
		_unreg = this.hook(name, _function);
		return _unreg;
	}
	removeHook(name, function_) {
		if (this._hooks[name]) {
			const index = this._hooks[name].indexOf(function_);
			if (index !== -1) this._hooks[name].splice(index, 1);
			if (this._hooks[name].length === 0) delete this._hooks[name];
		}
	}
	deprecateHook(name, deprecated) {
		this._deprecatedHooks[name] = typeof deprecated === "string" ? { to: deprecated } : deprecated;
		const _hooks = this._hooks[name] || [];
		delete this._hooks[name];
		for (const hook of _hooks) this.hook(name, hook);
	}
	deprecateHooks(deprecatedHooks) {
		Object.assign(this._deprecatedHooks, deprecatedHooks);
		for (const name in deprecatedHooks) this.deprecateHook(name, deprecatedHooks[name]);
	}
	addHooks(configHooks) {
		const hooks = flatHooks(configHooks);
		const removeFns = Object.keys(hooks).map((key) => this.hook(key, hooks[key]));
		return () => {
			for (const unreg of removeFns.splice(0, removeFns.length)) unreg();
		};
	}
	removeHooks(configHooks) {
		const hooks = flatHooks(configHooks);
		for (const key in hooks) this.removeHook(key, hooks[key]);
	}
	removeAllHooks() {
		for (const key in this._hooks) delete this._hooks[key];
	}
	callHook(name, ...arguments_) {
		arguments_.unshift(name);
		return this.callHookWith(serialTaskCaller, name, ...arguments_);
	}
	callHookParallel(name, ...arguments_) {
		arguments_.unshift(name);
		return this.callHookWith(parallelTaskCaller, name, ...arguments_);
	}
	callHookWith(caller, name, ...arguments_) {
		const event = this._before || this._after ? {
			name,
			args: arguments_,
			context: {}
		} : void 0;
		if (this._before) callEachWith(this._before, event);
		const result = caller(name in this._hooks ? [...this._hooks[name]] : [], arguments_);
		if (result instanceof Promise) return result.finally(() => {
			if (this._after && event) callEachWith(this._after, event);
		});
		if (this._after && event) callEachWith(this._after, event);
		return result;
	}
	beforeEach(function_) {
		this._before = this._before || [];
		this._before.push(function_);
		return () => {
			if (this._before !== void 0) {
				const index = this._before.indexOf(function_);
				if (index !== -1) this._before.splice(index, 1);
			}
		};
	}
	afterEach(function_) {
		this._after = this._after || [];
		this._after.push(function_);
		return () => {
			if (this._after !== void 0) {
				const index = this._after.indexOf(function_);
				if (index !== -1) this._after.splice(index, 1);
			}
		};
	}
};
function createHooks() {
	return new Hookable();
}
//#endregion
//#region src/rpc/global.ts
const hooks$1 = createHooks();
let DevToolsMessagingEvents = /* @__PURE__ */ function(DevToolsMessagingEvents) {
	DevToolsMessagingEvents["INSPECTOR_TREE_UPDATED"] = "inspector-tree-updated";
	DevToolsMessagingEvents["INSPECTOR_STATE_UPDATED"] = "inspector-state-updated";
	DevToolsMessagingEvents["DEVTOOLS_STATE_UPDATED"] = "devtools-state-updated";
	DevToolsMessagingEvents["ROUTER_INFO_UPDATED"] = "router-info-updated";
	DevToolsMessagingEvents["TIMELINE_EVENT_UPDATED"] = "timeline-event-updated";
	DevToolsMessagingEvents["INSPECTOR_UPDATED"] = "inspector-updated";
	DevToolsMessagingEvents["ACTIVE_APP_UNMOUNTED"] = "active-app-updated";
	DevToolsMessagingEvents["DESTROY_DEVTOOLS_CLIENT"] = "destroy-devtools-client";
	DevToolsMessagingEvents["RELOAD_DEVTOOLS_CLIENT"] = "reload-devtools-client";
	return DevToolsMessagingEvents;
}({});
function getDevToolsState() {
	const state = _vue_devtools_kit.devtools.ctx.state;
	return {
		connected: state.connected,
		clientConnected: true,
		vueVersion: state?.activeAppRecord?.version || "",
		tabs: state.tabs,
		commands: state.commands,
		vitePluginDetected: state.vitePluginDetected,
		appRecords: state.appRecords.map((item) => ({
			id: item.id,
			name: item.name,
			version: item.version,
			routerId: item.routerId,
			iframe: item.iframe
		})),
		activeAppRecordId: state.activeAppRecordId,
		timelineLayersState: state.timelineLayersState
	};
}
const functions = {
	on: (event, handler) => {
		hooks$1.hook(event, handler);
	},
	off: (event, handler) => {
		hooks$1.removeHook(event, handler);
	},
	once: (event, handler) => {
		hooks$1.hookOnce(event, handler);
	},
	emit: (event, ...args) => {
		hooks$1.callHook(event, ...args);
	},
	heartbeat: () => {
		return true;
	},
	devtoolsState: () => {
		return getDevToolsState();
	},
	async getInspectorTree(payload) {
		return (0, _vue_devtools_kit.stringify)(await _vue_devtools_kit.devtools.ctx.api.getInspectorTree(payload));
	},
	async getInspectorState(payload) {
		const inspector = (0, _vue_devtools_kit.getInspector)(payload.inspectorId);
		if (inspector) inspector.selectedNodeId = payload.nodeId;
		return (0, _vue_devtools_kit.stringify)(await _vue_devtools_kit.devtools.ctx.api.getInspectorState(payload));
	},
	async editInspectorState(payload) {
		return await _vue_devtools_kit.devtools.ctx.api.editInspectorState(payload);
	},
	sendInspectorState(id) {
		return _vue_devtools_kit.devtools.ctx.api.sendInspectorState(id);
	},
	inspectComponentInspector() {
		return _vue_devtools_kit.devtools.ctx.api.inspectComponentInspector();
	},
	cancelInspectComponentInspector() {
		return _vue_devtools_kit.devtools.ctx.api.cancelInspectComponentInspector();
	},
	getComponentRenderCode(id) {
		return _vue_devtools_kit.devtools.ctx.api.getComponentRenderCode(id);
	},
	scrollToComponent(id) {
		return _vue_devtools_kit.devtools.ctx.api.scrollToComponent(id);
	},
	inspectDOM(id) {
		return _vue_devtools_kit.devtools.ctx.api.inspectDOM(id);
	},
	getInspectorNodeActions(id) {
		return (0, _vue_devtools_kit.getInspectorNodeActions)(id);
	},
	getInspectorActions(id) {
		return (0, _vue_devtools_kit.getInspectorActions)(id);
	},
	updateTimelineLayersState(state) {
		return (0, _vue_devtools_kit.updateTimelineLayersState)(state);
	},
	callInspectorNodeAction(inspectorId, actionIndex, nodeId) {
		const nodeActions = (0, _vue_devtools_kit.getInspectorNodeActions)(inspectorId);
		if (nodeActions?.length) nodeActions[actionIndex].action?.(nodeId);
	},
	callInspectorAction(inspectorId, actionIndex) {
		const actions = (0, _vue_devtools_kit.getInspectorActions)(inspectorId);
		if (actions?.length) actions[actionIndex].action?.();
	},
	openInEditor(options) {
		return _vue_devtools_kit.devtools.ctx.api.openInEditor(options);
	},
	async checkVueInspectorDetected() {
		return !!await _vue_devtools_kit.devtools.ctx.api.getVueInspector();
	},
	async enableVueInspector() {
		const inspector = await _vue_devtools_kit.devtools?.api?.getVueInspector?.();
		if (inspector) await inspector.enable();
	},
	async toggleApp(id, options) {
		return _vue_devtools_kit.devtools.ctx.api.toggleApp(id, options);
	},
	updatePluginSettings(pluginId, key, value) {
		return _vue_devtools_kit.devtools.ctx.api.updatePluginSettings(pluginId, key, value);
	},
	getPluginSettings(pluginId) {
		return _vue_devtools_kit.devtools.ctx.api.getPluginSettings(pluginId);
	},
	getRouterInfo() {
		return _vue_devtools_kit.devtoolsRouterInfo;
	},
	navigate(path) {
		return _vue_devtools_kit.devtoolsRouter.value?.push(path).catch(() => ({}));
	},
	getMatchedRoutes(path) {
		const c = console.warn;
		console.warn = () => {};
		const matched = _vue_devtools_kit.devtoolsRouter.value?.resolve?.({ path: path || "/" }).matched ?? [];
		console.warn = c;
		return matched;
	},
	toggleClientConnected(state) {
		(0, _vue_devtools_kit.toggleClientConnected)(state);
	},
	getCustomInspector() {
		return (0, _vue_devtools_kit.getActiveInspectors)();
	},
	getInspectorInfo(id) {
		return (0, _vue_devtools_kit.getInspectorInfo)(id);
	},
	highlighComponent(uid) {
		return _vue_devtools_kit.devtools.ctx.hooks.callHook(_vue_devtools_kit.DevToolsContextHookKeys.COMPONENT_HIGHLIGHT, { uid });
	},
	unhighlight() {
		return _vue_devtools_kit.devtools.ctx.hooks.callHook(_vue_devtools_kit.DevToolsContextHookKeys.COMPONENT_UNHIGHLIGHT);
	},
	updateDevToolsClientDetected(params) {
		(0, _vue_devtools_kit.updateDevToolsClientDetected)(params);
	},
	initDevToolsServerListener() {
		const broadcast = (0, _vue_devtools_kit.getRpcServer)().broadcast;
		_vue_devtools_kit.devtools.ctx.hooks.hook(_vue_devtools_kit.DevToolsMessagingHookKeys.SEND_INSPECTOR_TREE_TO_CLIENT, (payload) => {
			broadcast.emit(DevToolsMessagingEvents.INSPECTOR_TREE_UPDATED, (0, _vue_devtools_kit.stringify)(payload));
		});
		_vue_devtools_kit.devtools.ctx.hooks.hook(_vue_devtools_kit.DevToolsMessagingHookKeys.SEND_INSPECTOR_STATE_TO_CLIENT, (payload) => {
			broadcast.emit(DevToolsMessagingEvents.INSPECTOR_STATE_UPDATED, (0, _vue_devtools_kit.stringify)(payload));
		});
		_vue_devtools_kit.devtools.ctx.hooks.hook(_vue_devtools_kit.DevToolsMessagingHookKeys.DEVTOOLS_STATE_UPDATED, () => {
			broadcast.emit(DevToolsMessagingEvents.DEVTOOLS_STATE_UPDATED, getDevToolsState());
		});
		_vue_devtools_kit.devtools.ctx.hooks.hook(_vue_devtools_kit.DevToolsMessagingHookKeys.ROUTER_INFO_UPDATED, ({ state }) => {
			broadcast.emit(DevToolsMessagingEvents.ROUTER_INFO_UPDATED, state);
		});
		_vue_devtools_kit.devtools.ctx.hooks.hook(_vue_devtools_kit.DevToolsMessagingHookKeys.SEND_TIMELINE_EVENT_TO_CLIENT, (payload) => {
			broadcast.emit(DevToolsMessagingEvents.TIMELINE_EVENT_UPDATED, (0, _vue_devtools_kit.stringify)(payload));
		});
		_vue_devtools_kit.devtools.ctx.hooks.hook(_vue_devtools_kit.DevToolsMessagingHookKeys.SEND_INSPECTOR_TO_CLIENT, (payload) => {
			broadcast.emit(DevToolsMessagingEvents.INSPECTOR_UPDATED, payload);
		});
		_vue_devtools_kit.devtools.ctx.hooks.hook(_vue_devtools_kit.DevToolsMessagingHookKeys.SEND_ACTIVE_APP_UNMOUNTED_TO_CLIENT, () => {
			broadcast.emit(DevToolsMessagingEvents.ACTIVE_APP_UNMOUNTED);
		});
	}
};
const rpc = new Proxy({
	value: {},
	functions: {}
}, { get(target, property) {
	const _rpc = (0, _vue_devtools_kit.getRpcClient)();
	if (property === "value") return _rpc;
	else if (property === "functions") return _rpc.$functions;
} });
const rpcServer = new Proxy({
	value: {},
	functions: {}
}, { get(target, property) {
	const _rpc = (0, _vue_devtools_kit.getRpcServer)();
	if (property === "value") return _rpc;
	else if (property === "functions") return _rpc.functions;
} });
function onRpcConnected(callback) {
	let timer = null;
	let retryCount = 0;
	function heartbeat() {
		rpc.value?.heartbeat?.().then(() => {
			callback();
			clearTimeout(timer);
		}).catch(() => {});
	}
	timer = setInterval(() => {
		if (retryCount >= 30) clearTimeout(timer);
		retryCount++;
		heartbeat();
	}, retryCount * 200 + 200);
	heartbeat();
}
function onRpcSeverReady(callback) {
	let timer = null;
	const timeout = 120;
	function heartbeat() {
		if (rpcServer.value.clients.length > 0) {
			callback();
			clearTimeout(timer);
		}
	}
	timer = setInterval(() => {
		heartbeat();
	}, timeout);
}
//#endregion
//#region src/rpc/vite.ts
const hooks = createHooks();
const viteRpcFunctions = {
	on: (event, handler) => {
		hooks.hook(event, handler);
	},
	off: (event, handler) => {
		hooks.removeHook(event, handler);
	},
	once: (event, handler) => {
		hooks.hookOnce(event, handler);
	},
	emit: (event, ...args) => {
		hooks.callHook(event, ...args);
	},
	heartbeat: () => {
		return true;
	}
};
const viteRpc = new Proxy({
	value: {},
	functions: {}
}, { get(target, property) {
	const _rpc = (0, _vue_devtools_kit.getViteRpcClient)();
	if (property === "value") return _rpc;
	else if (property === "functions") return _rpc?.$functions;
} });
function onViteRpcConnected(callback) {
	let timer = null;
	function heartbeat() {
		viteRpc.value?.heartbeat?.().then(() => {
			clearTimeout(timer);
			callback();
		}).catch(() => ({}));
		timer = setTimeout(() => {
			heartbeat();
		}, 80);
	}
	heartbeat();
}
function createViteClientRpc() {
	(0, _vue_devtools_kit.createRpcClient)(viteRpcFunctions, { preset: "vite" });
}
function createViteServerRpc(functions) {
	(0, _vue_devtools_kit.createRpcServer)(functions, { preset: "vite" });
}
//#endregion
//#region src/vue-plugin/devtools-state.ts
const VueDevToolsStateSymbol = Symbol.for("__VueDevToolsStateSymbol__");
function VueDevToolsVuePlugin() {
	return { install(app) {
		const state = createDevToolsStateContext();
		state.getDevToolsState();
		app.provide(VueDevToolsStateSymbol, state);
		app.config.globalProperties.$getDevToolsState = state.getDevToolsState;
		app.config.globalProperties.$disconnectDevToolsClient = () => {
			state.clientConnected.value = false;
			state.connected.value = false;
		};
	} };
}
function createDevToolsStateContext() {
	const connected = (0, vue.ref)(false);
	const clientConnected = (0, vue.ref)(false);
	const vueVersion = (0, vue.ref)("");
	const tabs = (0, vue.ref)([]);
	const commands = (0, vue.ref)([]);
	const vitePluginDetected = (0, vue.ref)(false);
	const appRecords = (0, vue.ref)([]);
	const activeAppRecordId = (0, vue.ref)("");
	const timelineLayersState = (0, vue.ref)({});
	function updateState(data) {
		connected.value = data.connected;
		clientConnected.value = data.clientConnected;
		vueVersion.value = data.vueVersion || "";
		tabs.value = data.tabs;
		commands.value = data.commands;
		vitePluginDetected.value = data.vitePluginDetected;
		appRecords.value = data.appRecords;
		activeAppRecordId.value = data.activeAppRecordId;
		timelineLayersState.value = data.timelineLayersState;
	}
	function getDevToolsState() {
		onRpcConnected(() => {
			rpc.value.devtoolsState().then((data) => {
				updateState(data);
			});
			rpc.functions.off(DevToolsMessagingEvents.DEVTOOLS_STATE_UPDATED, updateState);
			rpc.functions.on(DevToolsMessagingEvents.DEVTOOLS_STATE_UPDATED, updateState);
		});
	}
	return {
		getDevToolsState,
		connected,
		clientConnected,
		vueVersion,
		tabs,
		commands,
		vitePluginDetected,
		appRecords,
		activeAppRecordId,
		timelineLayersState
	};
}
function useDevToolsState() {
	return (0, vue.inject)(VueDevToolsStateSymbol);
}
const fns = [];
function onDevToolsConnected(fn) {
	const { connected, clientConnected } = useDevToolsState();
	fns.push(fn);
	(0, vue.onUnmounted)(() => {
		fns.splice(fns.indexOf(fn), 1);
	});
	const devtoolsReady = (0, vue.computed)(() => clientConnected.value && connected.value);
	if (devtoolsReady.value) fn();
	else {
		const stop = (0, vue.watch)(devtoolsReady, (v) => {
			if (v) {
				fn();
				stop();
			}
		});
	}
	return () => {
		fns.splice(fns.indexOf(fn), 1);
	};
}
function refreshCurrentPageData() {
	fns.forEach((fn) => fn());
}
//#endregion
exports.DevToolsMessagingEvents = DevToolsMessagingEvents;
exports.VueDevToolsVuePlugin = VueDevToolsVuePlugin;
exports.createDevToolsStateContext = createDevToolsStateContext;
exports.createViteClientRpc = createViteClientRpc;
exports.createViteServerRpc = createViteServerRpc;
exports.functions = functions;
exports.getDevToolsClientUrl = getDevToolsClientUrl;
exports.onDevToolsConnected = onDevToolsConnected;
exports.onRpcConnected = onRpcConnected;
exports.onRpcSeverReady = onRpcSeverReady;
exports.onViteRpcConnected = onViteRpcConnected;
exports.refreshCurrentPageData = refreshCurrentPageData;
exports.rpc = rpc;
exports.rpcServer = rpcServer;
exports.setDevToolsClientUrl = setDevToolsClientUrl;
exports.useDevToolsState = useDevToolsState;
exports.viteRpc = viteRpc;
exports.viteRpcFunctions = viteRpcFunctions;
