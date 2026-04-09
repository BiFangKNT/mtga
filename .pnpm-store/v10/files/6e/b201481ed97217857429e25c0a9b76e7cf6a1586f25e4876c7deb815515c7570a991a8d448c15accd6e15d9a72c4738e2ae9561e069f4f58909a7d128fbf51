function createDebug(namespace) {
	return Object.assign((...args) => {
		const env = globalThis.process?.env.DEBUG;
		if (!env || env !== "*" && !env.startsWith(namespace)) return;
		console.debug(...args);
	}, {
		color: "#000000",
		diff: 0,
		enabled: true,
		log: console.debug.bind(console),
		namespace,
		destroy: () => false,
		extend: (ns, _del) => createDebug(namespace + ns)
	});
}
const debug = Object.assign(createDebug, {
	coerce: (val) => val,
	disable: () => "",
	enable: (_namespaces) => {},
	enabled: (_namespaces) => true,
	formatArgs(args) {
		args[0] = `${this.namespace} ${args[0]}`;
	},
	log: console.debug.bind(console),
	selectColor: (_namespace) => 0,
	humanize: (num) => `${num}ms`,
	inspectOpts: {},
	names: [],
	skips: [],
	formatters: {}
});
export const coerce = debug.coerce;
export const disable = debug.disable;
export const enable = debug.enable;
export const enabled = debug.enabled;
export const formatArgs = debug.formatArgs;
export const log = debug.log;
export const selectColor = debug.selectColor;
export const humanize = debug.humanize;
export const names = debug.names;
export const skips = debug.skips;
export const formatters = debug.formatters;
export default debug;
