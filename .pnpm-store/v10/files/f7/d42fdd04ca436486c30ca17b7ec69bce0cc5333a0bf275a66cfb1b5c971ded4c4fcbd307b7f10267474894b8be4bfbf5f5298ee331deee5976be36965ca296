import process from "node:process";
import { defu } from "defu";
import { join, relative, resolve } from "pathe";
import { isDebug, isDevelopment, isTest } from "std-env";
import { existsSync } from "node:fs";
import { readdir } from "node:fs/promises";
import { randomUUID } from "node:crypto";
import { findWorkspaceDir } from "pkg-types";
import { escapeHtml } from "@vue/shared";
//#region src/utils/definition.ts
function defineResolvers(config) {
	return config;
}
//#endregion
//#region src/config/adhoc.ts
var adhoc_default = defineResolvers({
	components: { $resolve: (val) => {
		if (Array.isArray(val)) return { dirs: val };
		if (val === false) return { dirs: [] };
		return {
			dirs: [{
				path: "~/components/global",
				global: true
			}, "~/components"],
			...typeof val === "object" ? val : {}
		};
	} },
	imports: {
		global: false,
		scan: true,
		dirs: []
	},
	pages: void 0,
	telemetry: void 0,
	devtools: {}
});
//#endregion
//#region src/config/app.ts
var app_default = defineResolvers({
	vue: {
		transformAssetUrls: {
			video: ["src", "poster"],
			source: ["src"],
			img: ["src"],
			image: ["xlink:href", "href"],
			use: ["xlink:href", "href"]
		},
		compilerOptions: {},
		runtimeCompiler: { $resolve: (val) => {
			return typeof val === "boolean" ? val : false;
		} },
		propsDestructure: true,
		config: {}
	},
	app: {
		baseURL: { $resolve: (val) => {
			if (typeof val === "string") return val;
			return process.env.NUXT_APP_BASE_URL || "/";
		} },
		buildAssetsDir: { $resolve: (val) => {
			if (typeof val === "string") return val;
			return process.env.NUXT_APP_BUILD_ASSETS_DIR || "/_nuxt/";
		} },
		cdnURL: { $resolve: async (val, get) => {
			if (await get("dev")) return "";
			return process.env.NUXT_APP_CDN_URL || (typeof val === "string" ? val : "");
		} },
		head: { $resolve: (_val) => {
			const resolved = defu(_val && typeof _val === "object" ? _val : {}, {
				meta: [],
				link: [],
				style: [],
				script: [],
				noscript: []
			});
			if (!resolved.meta.find((m) => m?.charset)?.charset) resolved.meta.unshift({ charset: resolved.charset || "utf-8" });
			if (!resolved.meta.find((m) => m?.name === "viewport")?.content) resolved.meta.unshift({
				name: "viewport",
				content: resolved.viewport || "width=device-width, initial-scale=1"
			});
			resolved.meta = resolved.meta.filter(Boolean);
			resolved.link = resolved.link.filter(Boolean);
			resolved.style = resolved.style.filter(Boolean);
			resolved.script = resolved.script.filter(Boolean);
			resolved.noscript = resolved.noscript.filter(Boolean);
			return resolved;
		} },
		layoutTransition: false,
		pageTransition: false,
		viewTransition: { $resolve: async (val, get) => {
			const isEnabled = val === "always" || typeof val === "boolean";
			const hasEnabled = val && typeof val === "object" && "enabled" in val;
			const hasTypes = val && typeof val === "object" && "types" in val;
			const appOptions = {
				enabled: isEnabled ? val : hasEnabled ? val.enabled : void 0,
				types: hasTypes ? val.types : void 0
			};
			if (appOptions.enabled !== void 0 && appOptions.types !== void 0) return appOptions;
			const _configOptions = await get("experimental").then((e) => e.viewTransition) ?? { enabled: false };
			const configOptions = typeof _configOptions === "object" ? _configOptions : { enabled: _configOptions };
			return {
				enabled: appOptions.enabled ?? configOptions.enabled,
				types: appOptions.types ?? configOptions.types
			};
		} },
		keepalive: false,
		rootId: { $resolve: (val) => val === false ? false : val && typeof val === "string" ? val : "__nuxt" },
		rootTag: { $resolve: (val) => val && typeof val === "string" ? val : "div" },
		rootAttrs: { $resolve: async (val, get) => {
			const rootId = await get("app.rootId");
			return {
				id: rootId === false ? void 0 : rootId || "__nuxt",
				...typeof val === "object" ? val : {}
			};
		} },
		teleportTag: { $resolve: (val) => val && typeof val === "string" ? val : "div" },
		teleportId: { $resolve: (val) => val === false ? false : val && typeof val === "string" ? val : "teleports" },
		teleportAttrs: { $resolve: async (val, get) => {
			const teleportId = await get("app.teleportId");
			return {
				id: teleportId === false ? void 0 : teleportId || "teleports",
				...typeof val === "object" ? val : {}
			};
		} },
		spaLoaderTag: { $resolve: (val) => val && typeof val === "string" ? val : "div" },
		spaLoaderAttrs: { id: "__nuxt-loader" }
	},
	spaLoadingTemplate: { $resolve: async (val, get) => {
		if (typeof val === "string") return resolve(await get("srcDir"), val);
		if (typeof val === "boolean") return val;
		return null;
	} },
	plugins: [],
	css: { $resolve: (val) => {
		if (!Array.isArray(val)) return [];
		const css = [];
		for (const item of val) if (typeof item === "string") css.push(item);
		return css;
	} },
	unhead: {
		legacy: false,
		renderSSRHeadOptions: { $resolve: (val) => ({
			omitLineBreaks: true,
			...typeof val === "object" ? val : {}
		}) }
	}
});
//#endregion
//#region src/config/build.ts
var build_default = defineResolvers({
	builder: { $resolve: (val) => {
		if (val && typeof val === "object" && "bundle" in val) return val;
		const map = {
			rspack: "@nuxt/rspack-builder",
			vite: "@nuxt/vite-builder",
			webpack: "@nuxt/webpack-builder"
		};
		if (typeof val === "string" && val in map) return map[val];
		return map.vite;
	} },
	sourcemap: { $resolve: async (val, get) => {
		if (typeof val === "boolean") return {
			server: val,
			client: val
		};
		return {
			server: true,
			client: await get("dev"),
			...typeof val === "object" ? val : {}
		};
	} },
	logLevel: { $resolve: (val) => {
		if (val && typeof val === "string" && ![
			"silent",
			"info",
			"verbose"
		].includes(val)) console.warn(`Invalid \`logLevel\` option: \`${val}\`. Must be one of: \`silent\`, \`info\`, \`verbose\`.`);
		return val && typeof val === "string" ? val : isTest ? "silent" : "info";
	} },
	build: {
		transpile: { $resolve: (val) => {
			const transpile = [];
			if (Array.isArray(val)) for (const pattern of val) {
				if (!pattern) continue;
				if (typeof pattern === "string" || typeof pattern === "function" || pattern instanceof RegExp) transpile.push(pattern);
			}
			return transpile;
		} },
		templates: [],
		analyze: { $resolve: async (val, get) => {
			const [rootDir, analyzeDir] = await Promise.all([get("rootDir"), get("analyzeDir")]);
			return {
				template: "treemap",
				projectRoot: rootDir,
				filename: join(analyzeDir, "{name}.html"),
				...typeof val === "boolean" ? { enabled: val } : typeof val === "object" ? val : {}
			};
		} }
	},
	optimization: {
		keyedComposables: { $resolve: (val) => [
			{
				name: "callOnce",
				argumentLength: 3,
				source: "#app/composables/once"
			},
			{
				name: "defineNuxtComponent",
				argumentLength: 2,
				source: "#app/composables/component"
			},
			{
				name: "useState",
				argumentLength: 2,
				source: "#app/composables/state"
			},
			{
				name: "useFetch",
				argumentLength: 3,
				source: "#app/composables/fetch"
			},
			{
				name: "useAsyncData",
				argumentLength: 3,
				source: "#app/composables/asyncData"
			},
			{
				name: "useLazyAsyncData",
				argumentLength: 3,
				source: "#app/composables/asyncData"
			},
			{
				name: "useLazyFetch",
				argumentLength: 3,
				source: "#app/composables/fetch"
			},
			...Array.isArray(val) ? val : []
		].filter(Boolean) },
		keyedComposableFactories: { $resolve: (val) => [
			{
				name: "createUseFetch",
				source: "#app/composables/fetch",
				argumentLength: 3
			},
			{
				name: "createUseAsyncData",
				source: "#app/composables/asyncData",
				argumentLength: 3
			},
			...Array.isArray(val) ? val : []
		].filter(Boolean) },
		treeShake: { composables: {
			server: { $resolve: async (val, get) => defu(typeof val === "object" ? val || {} : {}, await get("dev") ? {} : {
				"vue": [
					"onMounted",
					"onUpdated",
					"onUnmounted",
					"onBeforeMount",
					"onBeforeUpdate",
					"onBeforeUnmount",
					"onRenderTracked",
					"onRenderTriggered",
					"onActivated",
					"onDeactivated"
				],
				"#app": ["definePayloadReviver", "definePageMeta"]
			}) },
			client: { $resolve: async (val, get) => defu(typeof val === "object" ? val || {} : {}, await get("dev") ? {} : {
				"vue": [
					"onRenderTracked",
					"onRenderTriggered",
					"onServerPrefetch"
				],
				"#app": [
					"definePayloadReducer",
					"definePageMeta",
					"onPrehydrate"
				]
			}) }
		} },
		asyncTransforms: {
			asyncFunctions: ["defineNuxtPlugin", "defineNuxtRouteMiddleware"],
			objectDefinitions: {
				defineNuxtComponent: ["asyncData", "setup"],
				defineNuxtPlugin: ["setup"],
				definePageMeta: ["middleware", "validate"]
			}
		}
	}
});
//#endregion
//#region src/config/common.ts
var common_default = defineResolvers({
	extends: void 0,
	compatibilityDate: void 0,
	theme: void 0,
	rootDir: { $resolve: (val) => typeof val === "string" ? resolve(val) : process.cwd() },
	workspaceDir: { $resolve: async (val, get) => {
		const rootDir = await get("rootDir");
		return val && typeof val === "string" ? resolve(rootDir, val) : findWorkspaceDir(rootDir, {
			gitConfig: "closest",
			try: true
		}).catch(() => rootDir);
	} },
	srcDir: { $resolve: async (val, get) => {
		if (val && typeof val === "string") return resolve(await get("rootDir"), val);
		const rootDir = await get("rootDir");
		const srcDir = resolve(rootDir, "app");
		if (!existsSync(srcDir)) return rootDir;
		const srcDirFiles = /* @__PURE__ */ new Set();
		const files = await readdir(srcDir).catch(() => []);
		for (const file of files) if (file !== "spa-loading-template.html" && !file.startsWith("router.options")) srcDirFiles.add(file);
		if (srcDirFiles.size === 0) {
			for (const file of ["app.vue", "App.vue"]) if (existsSync(resolve(rootDir, file))) return rootDir;
			const dirs = await Promise.all([
				"assets",
				"layouts",
				"middleware",
				"pages",
				"plugins"
			].map((key) => get(`dir.${key}`)));
			for (const dir of dirs) if (existsSync(resolve(rootDir, dir))) return rootDir;
		}
		return srcDir;
	} },
	serverDir: { $resolve: async (val, get) => {
		return resolve(await get("rootDir"), val && typeof val === "string" ? val : "server");
	} },
	buildDir: { $resolve: async (val, get) => {
		return resolve(await get("rootDir"), val && typeof val === "string" ? val : ".nuxt");
	} },
	appId: { $resolve: (val) => val && typeof val === "string" ? val : "nuxt-app" },
	buildId: { $resolve: async (val, get) => {
		if (typeof val === "string") return val;
		const [isDev, isTest] = await Promise.all([get("dev"), get("test")]);
		return isDev ? "dev" : isTest ? "test" : randomUUID();
	} },
	modulesDir: {
		$default: ["node_modules"],
		$resolve: async (val, get) => {
			const rootDir = await get("rootDir");
			const modulesDir = new Set([resolve(rootDir, "node_modules")]);
			if (Array.isArray(val)) {
				for (const dir of val) if (dir && typeof dir === "string") modulesDir.add(resolve(rootDir, dir));
			}
			return [...modulesDir];
		}
	},
	analyzeDir: { $resolve: async (val, get) => val && typeof val === "string" ? resolve(await get("rootDir"), val) : resolve(await get("buildDir"), "analyze") },
	dev: { $resolve: (val) => typeof val === "boolean" ? val : Boolean(isDevelopment) },
	test: { $resolve: (val) => typeof val === "boolean" ? val : Boolean(isTest) },
	debug: { $resolve: (val) => {
		val ??= isDebug;
		if (val === true) return {
			templates: true,
			modules: true,
			watchers: true,
			hooks: {
				client: true,
				server: true
			},
			nitro: true,
			router: true,
			hydration: true,
			perf: process.env.NUXT_DEBUG_PERF === "quiet" ? "quiet" : true
		};
		if (val && typeof val === "object") {
			if (process.env.NUXT_DEBUG_PERF) val.perf = process.env.NUXT_DEBUG_PERF === "quiet" ? "quiet" : true;
			return val;
		}
		if (process.env.NUXT_DEBUG_PERF) return { perf: process.env.NUXT_DEBUG_PERF === "quiet" ? "quiet" : true };
		return false;
	} },
	ssr: { $resolve: (val) => typeof val === "boolean" ? val : true },
	modules: { $resolve: (val) => {
		const modules = [];
		if (Array.isArray(val)) for (const mod of val) {
			if (!mod) continue;
			if (typeof mod === "string" || typeof mod === "function" || Array.isArray(mod) && mod[0]) modules.push(mod);
		}
		return modules;
	} },
	dir: {
		app: { $resolve: async (val, get) => {
			const [srcDir, rootDir] = await Promise.all([get("srcDir"), get("rootDir")]);
			return resolve(await get("srcDir"), val && typeof val === "string" ? val : srcDir === rootDir ? "app" : ".");
		} },
		assets: "assets",
		layouts: "layouts",
		middleware: "middleware",
		modules: { $resolve: async (val, get) => {
			return resolve(await get("rootDir"), val && typeof val === "string" ? val : "modules");
		} },
		pages: "pages",
		plugins: "plugins",
		shared: { $resolve: (val) => {
			return val && typeof val === "string" ? val : "shared";
		} },
		public: { $resolve: async (val, get) => {
			return resolve(await get("rootDir"), val && typeof val === "string" ? val : "public");
		} }
	},
	extensions: { $resolve: (val) => {
		const extensions = [
			".js",
			".jsx",
			".mjs",
			".ts",
			".tsx",
			".vue"
		];
		if (Array.isArray(val)) {
			for (const item of val) if (item && typeof item === "string") extensions.push(item);
		}
		return extensions;
	} },
	alias: { $resolve: async (val, get) => {
		const [srcDir, rootDir, buildDir, sharedDir, serverDir] = await Promise.all([
			get("srcDir"),
			get("rootDir"),
			get("buildDir"),
			get("dir.shared"),
			get("serverDir")
		]);
		const srcWithTrailingSlash = withTrailingSlash(srcDir);
		const rootWithTrailingSlash = withTrailingSlash(rootDir);
		return {
			"~": srcWithTrailingSlash,
			"@": srcWithTrailingSlash,
			"~~": rootWithTrailingSlash,
			"@@": rootWithTrailingSlash,
			"#shared": withTrailingSlash(resolve(rootDir, sharedDir)),
			"#server": withTrailingSlash(serverDir),
			"#build": withTrailingSlash(buildDir),
			"#internal/nuxt/paths": resolve(buildDir, "paths.mjs"),
			...typeof val === "object" ? val : {}
		};
	} },
	ignoreOptions: void 0,
	ignorePrefix: { $resolve: (val) => val && typeof val === "string" ? val : "-" },
	ignore: { $resolve: async (val, get) => {
		const [rootDir, ignorePrefix, analyzeDir, buildDir] = await Promise.all([
			get("rootDir"),
			get("ignorePrefix"),
			get("analyzeDir"),
			get("buildDir")
		]);
		const ignore = new Set([
			"**/*.stories.{js,cts,mts,ts,jsx,tsx}",
			"**/*.{spec,test}.{js,cts,mts,ts,jsx,tsx}",
			"**/*.d.{cts,mts,ts}",
			"**/*.d.vue.{cts,mts,ts}",
			"**/.{pnpm-store,vercel,netlify,output,git,cache,data,direnv}",
			"/vendor",
			"**/node-compile-cache",
			"**/test-results",
			"**/*.sock",
			relative(rootDir, analyzeDir),
			relative(rootDir, buildDir)
		]);
		if (ignorePrefix) ignore.add(`**/${ignorePrefix}*.*`);
		if (Array.isArray(val)) {
			for (const pattern of val) if (pattern) ignore.add(pattern);
		}
		return [...ignore];
	} },
	watch: { $resolve: (val) => {
		if (Array.isArray(val)) return val.filter((b) => typeof b === "string" || b instanceof RegExp);
		return [];
	} },
	watchers: {
		rewatchOnRawEvents: void 0,
		webpack: { aggregateTimeout: 1e3 },
		chokidar: {
			ignoreInitial: true,
			ignorePermissionErrors: true
		}
	},
	hooks: void 0,
	runtimeConfig: { $resolve: async (_val, get) => {
		const val = _val && typeof _val === "object" ? _val : {};
		const [app, buildId] = await Promise.all([get("app"), get("buildId")]);
		provideFallbackValues(val);
		return defu(val, {
			public: {},
			app: {
				buildId,
				baseURL: app.baseURL,
				buildAssetsDir: app.buildAssetsDir,
				cdnURL: app.cdnURL
			}
		});
	} },
	appConfig: { nuxt: {} },
	$schema: {}
});
function provideFallbackValues(obj) {
	for (const key in obj) if (typeof obj[key] === "undefined" || obj[key] === null) obj[key] = "";
	else if (typeof obj[key] === "object") provideFallbackValues(obj[key]);
}
function withTrailingSlash(str) {
	return str.replace(/\/?$/, "/");
}
//#endregion
//#region ../ui-templates/dist/templates/loading.ts
const _messages = {
	"appName": "Nuxt",
	"loading": "Loading",
	"version": "4.0"
};
const template = (messages) => {
	messages = {
		..._messages,
		...messages
	};
	return "<!DOCTYPE html><html lang=\"en\"><head><title>" + escapeHtml(messages.loading) + " | " + escapeHtml(messages.appName) + "</title><meta charset=\"utf-8\"><meta content=\"width=device-width,initial-scale=1.0,minimum-scale=1.0\" name=\"viewport\"><style>.nuxt-loader-bar{background:#00dc82;bottom:0;height:3px;left:0;position:fixed;right:0}.triangle-loading{position:absolute}.triangle-loading>path{animation:nuxt-loading-move 3s linear infinite;fill:none;stroke-dasharray:128;stroke-dashoffset:128;stroke-linecap:round;stroke-linejoin:round;stroke-width:4px}.nuxt-logo:hover .triangle-loading>path{animation-play-state:paused}@keyframes nuxt-loading-move{to{stroke-dashoffset:-128}}@media (prefers-color-scheme:dark){body,html{color:#fff;color-scheme:dark}}*,:after,:before{border-color:var(--un-default-border-color,#e5e7eb);border-style:solid;border-width:0;box-sizing:border-box}:after,:before{--un-content:\"\"}html{line-height:1.5;-webkit-text-size-adjust:100%;font-family:ui-sans-serif,system-ui,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji;font-feature-settings:normal;font-variation-settings:normal;-moz-tab-size:4;tab-size:4;-webkit-tap-highlight-color:transparent}body{line-height:inherit;margin:0}a{color:inherit;text-decoration:inherit}svg{display:block;vertical-align:middle}*,:after,:before{--un-rotate:0;--un-rotate-x:0;--un-rotate-y:0;--un-rotate-z:0;--un-scale-x:1;--un-scale-y:1;--un-scale-z:1;--un-skew-x:0;--un-skew-y:0;--un-translate-x:0;--un-translate-y:0;--un-translate-z:0;--un-pan-x: ;--un-pan-y: ;--un-pinch-zoom: ;--un-scroll-snap-strictness:proximity;--un-ordinal: ;--un-slashed-zero: ;--un-numeric-figure: ;--un-numeric-spacing: ;--un-numeric-fraction: ;--un-border-spacing-x:0;--un-border-spacing-y:0;--un-ring-offset-shadow:0 0 transparent;--un-ring-shadow:0 0 transparent;--un-shadow-inset: ;--un-shadow:0 0 transparent;--un-ring-inset: ;--un-ring-offset-width:0px;--un-ring-offset-color:#fff;--un-ring-width:0px;--un-ring-color:rgba(147,197,253,.5);--un-blur: ;--un-brightness: ;--un-contrast: ;--un-drop-shadow: ;--un-grayscale: ;--un-hue-rotate: ;--un-invert: ;--un-saturate: ;--un-sepia: ;--un-backdrop-blur: ;--un-backdrop-brightness: ;--un-backdrop-contrast: ;--un-backdrop-grayscale: ;--un-backdrop-hue-rotate: ;--un-backdrop-invert: ;--un-backdrop-opacity: ;--un-backdrop-saturate: ;--un-backdrop-sepia: }.relative{position:relative}.inline-block{display:inline-block}.min-h-screen{min-height:100vh}.flex{display:flex}.flex-col{flex-direction:column}.items-end{align-items:flex-end}.items-center{align-items:center}.justify-center{justify-content:center}.gap-4{gap:1rem}.overflow-hidden{overflow:hidden}.border{border-width:1px}.border-\\[\\#00DC42\\]\\/50{border-color:#00dc4280}.group:hover .group-hover\\:border-\\[\\#00DC42\\]{--un-border-opacity:1;border-color:rgb(0 220 66/var(--un-border-opacity))}.rounded{border-radius:.25rem}.bg-\\[\\#00DC42\\]\\/10{background-color:#00dc421a}.bg-white{--un-bg-opacity:1;background-color:rgb(255 255 255/var(--un-bg-opacity))}.group:hover .group-hover\\:bg-\\[\\#00DC42\\]\\/15{background-color:#00dc4226}.px-2\\.5{padding-left:.625rem;padding-right:.625rem}.py-1\\.5{padding-bottom:.375rem;padding-top:.375rem}.text-center{text-align:center}.text-\\[16px\\]{font-size:16px}.group:hover .group-hover\\:text-\\[\\#00DC82\\],.text-\\[\\#00DC82\\]{--un-text-opacity:1;color:rgb(0 220 130/var(--un-text-opacity))}.text-\\[\\#00DC82\\]\\/80{color:#00dc82cc}.group:hover .group-hover\\:text-\\[\\#020420\\],.text-\\[\\#020420\\]{--un-text-opacity:1;color:rgb(2 4 32/var(--un-text-opacity))}.text-\\[\\#020420\\]\\/80{color:#020420cc}.font-semibold{font-weight:600}.leading-none{line-height:1}.font-mono{font-family:ui-monospace,SFMono-Regular,Menlo,Monaco,Consolas,Liberation Mono,Courier New,monospace}.font-sans{font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica Neue,Arial,Noto Sans,sans-serif,Apple Color Emoji,Segoe UI Emoji,Segoe UI Symbol,Noto Color Emoji}.antialiased{-webkit-font-smoothing:antialiased;-moz-osx-font-smoothing:grayscale}@media(prefers-color-scheme:dark){.dark\\:bg-\\[\\#020420\\]{--un-bg-opacity:1;background-color:rgb(2 4 32/var(--un-bg-opacity))}.dark\\:text-gray-200{--un-text-opacity:1;color:rgb(224 224 224/var(--un-text-opacity))}.dark\\:text-white,.group:hover .dark\\:group-hover\\:text-white{--un-text-opacity:1;color:rgb(255 255 255/var(--un-text-opacity))}}</style><script>!function(){const e=document.createElement(\"link\").relList;if(!(e&&e.supports&&e.supports(\"modulepreload\"))){for(const e of document.querySelectorAll('link[rel=\"modulepreload\"]'))r(e);new MutationObserver(e=>{for(const o of e)if(\"childList\"===o.type)for(const e of o.addedNodes)\"LINK\"===e.tagName&&\"modulepreload\"===e.rel&&r(e)}).observe(document,{childList:!0,subtree:!0})}function r(e){if(e.ep)return;e.ep=!0;const r=function(e){const r={};return e.integrity&&(r.integrity=e.integrity),e.referrerPolicy&&(r.referrerPolicy=e.referrerPolicy),\"use-credentials\"===e.crossOrigin?r.credentials=\"include\":\"anonymous\"===e.crossOrigin?r.credentials=\"omit\":r.credentials=\"same-origin\",r}(e);fetch(e.href,r)}}();<\/script></head><body class=\"antialiased bg-white dark:bg-[#020420] dark:text-white flex flex-col font-sans items-center justify-center min-h-screen overflow-hidden relative text-[#020420] text-center\"><a href=\"https://nuxt.com/?utm_source=nuxt-loading-screen\" target=\"_blank\" rel=\"noopener\" class=\"flex gap-4 group items-end nuxt-logo\" id=\"nuxtImg\"><div class=\"relative\"><svg xmlns=\"http://www.w3.org/2000/svg\" width=\"80\" fill=\"none\" class=\"group-hover:text-[#00DC82] text-[#00DC82]/80 triangle-loading\" viewBox=\"0 0 37 25\"><path stroke=\"currentColor\" d=\"M24.236 22.006h10.742L25.563 5.822l-8.979 14.31a4 4 0 0 1-3.388 1.874H2.978l11.631-20 5.897 10.567\"/></svg> <svg xmlns=\"http://www.w3.org/2000/svg\" width=\"214\" height=\"53\" fill=\"none\" class=\"dark:group-hover:text-white dark:text-gray-200 group-hover:text-[#020420] text-[#020420]/80\" viewBox=\"0 0 800 200\"><path fill=\"currentColor\" d=\"M377 200a4 4 0 0 0 4-4v-93s5.244 8.286 15 25l38.707 66.961c1.789 3.119 5.084 5.039 8.649 5.039H470V50h-27a4 4 0 0 0-4 4v94l-17-30-36.588-62.98c-1.792-3.108-5.081-5.02-8.639-5.02H350v150zm299.203-56.143L710.551 92h-25.73a9.97 9.97 0 0 0-8.333 4.522L660.757 120.5l-15.731-23.978A9.97 9.97 0 0 0 636.693 92h-25.527l34.348 51.643L608.524 200h24.966a9.97 9.97 0 0 0 8.29-4.458l19.18-28.756 18.981 28.72a9.97 9.97 0 0 0 8.313 4.494h24.736zM724.598 92h19.714V60.071h28.251V92H800v24.857h-27.437V159.5c0 10.5 5.284 15.429 14.43 15.429H800V200h-16.869c-23.576 0-38.819-14.143-38.819-39.214v-43.929h-19.714zM590 92h-15c-3.489 0-6.218.145-8.5 2.523-2.282 2.246-2.5 3.63-2.5 7.066v52.486c0 8.058-.376 12.962-4 16.925-3.624 3.831-8.619 5-16 5-7.247 0-12.376-1.169-16-5-3.624-3.963-4-8.867-4-16.925v-52.486c0-3.435-.218-4.82-2.5-7.066C519.218 92.145 516.489 92 513 92h-15v62.422q0 21.006 11.676 33.292C517.594 195.905 529.103 200 544 200s26.204-4.095 34.123-12.286Q590 175.428 590 154.422z\"/></svg></div> <span class=\"bg-[#00DC42]/10 border border-[#00DC42]/50 font-mono font-semibold group-hover:bg-[#00DC42]/15 group-hover:border-[#00DC42] inline-block leading-none px-2.5 py-1.5 rounded text-[#00DC82] text-[16px]\">4.4.2</span> </a><div class=\"nuxt-loader-bar\"></div><script>if(void 0===window.fetch)setTimeout(()=>window.location.reload(),200);else{const o=async()=>{try{if(!(await window.fetch(window.location.href).then(o=>o.text())).includes(\"__NUXT_LOADING__\"))return window.location.reload()}catch{}setTimeout(o,200)};o()}<\/script><script>const prefersReducedMotion=window.matchMedia(\"(prefers-reduced-motion: reduce)\").matches;function whatHemisphere(){let e=new Date;if(null==e.getTimezoneOffset)return null;e=e.getFullYear();let t=-new Date(e,0,1,0,0,0,0).getTimezoneOffset()- -new Date(e,6,1,0,0,0,0).getTimezoneOffset();return t<0?\"N\":t>0?\"S\":null}const months={N:[10,11,0],S:[4,5,6]},hemisphere=whatHemisphere();if(hemisphere&&months[hemisphere].includes((new Date).getMonth())&&!prefersReducedMotion){let e=\"false\"!==localStorage.getItem(\"nuxt-snow\"),t=null,n=[],r=Date.now();const i=25e-5,a=1.25,o={current:0,maxCurrent:4,force:.1,target:.1,min:.1,max:.4,easing:.01},s=(e,t)=>(e%t+t)%t,d=document.createElement(\"button\");d.id=\"snow-toggle\",d.style=\"position:fixed;bottom:16px;right:16px;z-index:100;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:8px;padding:8px 12px;cursor:pointer;font-size:20px;\",document.body.appendChild(d);const h=document.createElement(\"canvas\");h.id=\"snow-canvas\",h.style=\"position:fixed;inset:0;z-index:-10;pointer-events:none;opacity:0;transition:opacity 0.5s;filter:blur(4px);\",document.body.appendChild(h);const l=h.getContext(\"2d\");function resize(){h.width=window.innerWidth,h.height=window.innerHeight,n=Array.from({length:Math.floor(h.width*h.height*i)},()=>({x:Math.random()*h.width,y:Math.random()*h.height,vx:1+Math.random(),vy:1+Math.random(),vsin:10*Math.random(),rangle:2*Math.random()*Math.PI,rsin:10*Math.random(),color:`rgba(255,255,255,${.1+.15*Math.random()})`,size:5*Math.random()*4*(h.height/1e3)}))}function draw(){l.clearRect(0,0,h.width,h.height);const e=Date.now(),i=e-r;r=e,o.force+=(o.target-o.force)*o.easing,o.current=Math.max(-o.maxCurrent,Math.min(o.current+o.force*i*.05,o.maxCurrent)),Math.random()>.995&&(o.target=(o.min+Math.random()*(o.max-o.min))*(Math.random()>.5?-1:1));const d=.2*i;n.forEach(e=>{e.x=s(e.x+d+o.current*e.vx,h.width),e.y=s(e.y+d*e.vy*a,h.height),e.x+=Math.sin(d*e.vsin)*e.rsin*.5,e.rangle+=.01*d,l.fillStyle=e.color,l.beginPath(),l.ellipse(e.x,e.y,e.size,.66*e.size,e.rangle,0,2*Math.PI),l.fill()}),t=requestAnimationFrame(draw)}function update(){d.innerHTML=e?\"☀️\":\"❄️\",d.title=e?\"Disable snow\":\"Enable snow\",e?(resize(),window.addEventListener(\"resize\",resize),h.style.opacity=1,r=Date.now(),draw()):(t&&cancelAnimationFrame(t),t=null,window.removeEventListener(\"resize\",resize),h.style.opacity=0)}d.onclick=()=>{e=!e,localStorage.setItem(\"nuxt-snow\",e),update()},update()}<\/script></body></html>";
};
//#endregion
//#region src/config/dev.ts
var dev_default = defineResolvers({ devServer: {
	https: false,
	port: Number(process.env.NUXT_PORT || process.env.NITRO_PORT || process.env.PORT || 3e3),
	host: process.env.NUXT_HOST || process.env.NITRO_HOST || process.env.HOST || void 0,
	url: "http://localhost:3000",
	loadingTemplate: template,
	cors: { origin: [/^https?:\/\/(?:(?:[^:]+\.)?localhost|127\.0\.0\.1|\[::1\])(?::\d+)?$/] }
} });
//#endregion
//#region src/config/esbuild.ts
var esbuild_default = defineResolvers({ esbuild: { options: {
	target: { $resolve: async (val, get) => {
		if (typeof val === "string") return val;
		const builder = await get("builder");
		if (!builder || builder === "vite" || builder === "@nuxt/vite-builder") return "esnext";
		if (await get("experimental").then((r) => r?.decorators === true)) return "es2024";
		return "esnext";
	} },
	jsxFactory: "h",
	jsxFragment: "Fragment",
	tsconfigRaw: { $resolve: async (_val, get) => {
		const val = typeof _val === "string" ? JSON.parse(_val) : _val && typeof _val === "object" ? _val : {};
		if (!await get("experimental").then((r) => r?.decorators === true)) return val;
		return defu({ compilerOptions: { experimentalDecorators: false } }, val);
	} }
} } });
//#endregion
//#region src/config/oxc.ts
var oxc_default = defineResolvers({ oxc: { transform: { options: {
	target: "esnext",
	jsxFactory: "h",
	jsxFragment: "Fragment"
} } } });
//#endregion
//#region src/config/experimental.ts
var experimental_default = defineResolvers({
	future: {
		compatibilityVersion: { $resolve: (val) => typeof val === "number" ? val : 4 },
		multiApp: false,
		typescriptBundlerResolution: { async $resolve(val, get) {
			val = typeof val === "boolean" ? val : await get("experimental").then((e) => e?.typescriptBundlerResolution);
			if (typeof val === "boolean") return val;
			const setting = await get("typescript.tsConfig").then((r) => r?.compilerOptions?.moduleResolution);
			if (setting) return setting.toLowerCase() === "bundler";
			return true;
		} }
	},
	features: {
		inlineStyles: { async $resolve(_val, get) {
			const val = typeof _val === "boolean" || typeof _val === "function" ? _val : await get("experimental").then((e) => e?.inlineSSRStyles);
			if (val === false || await get("dev") || await get("ssr") === false) return false;
			return val ?? ((id) => !!id && id.includes(".vue"));
		} },
		devLogs: { async $resolve(val, get) {
			if (typeof val === "boolean" || val === "silent") return val;
			const [isDev, isTest] = await Promise.all([get("dev"), get("test")]);
			return isDev && !isTest;
		} },
		noScripts: { async $resolve(val, get) {
			const isValidLiteral = (val) => {
				return typeof val === "string" && ["production", "all"].includes(val);
			};
			return val === true ? "production" : val === false || isValidLiteral(val) ? val : await get("experimental").then((e) => e?.noScripts && "production") ?? false;
		} }
	},
	experimental: {
		runtimeBaseURL: false,
		decorators: false,
		asyncEntry: { $resolve: (val) => typeof val === "boolean" ? val : false },
		externalVue: true,
		serverAppConfig: true,
		emitRouteChunkError: { $resolve: (val) => {
			if (val === true) return "manual";
			if (val === "reload") return "automatic";
			if (val === false) return false;
			if (typeof val === "string" && new Set([
				"manual",
				"automatic",
				"automatic-immediate"
			]).has(val)) return val;
			return "automatic";
		} },
		templateRouteInjection: true,
		restoreState: false,
		renderJsonPayloads: true,
		noVueServer: false,
		payloadExtraction: { $resolve: async (val, get) => {
			if (await get("ssr") === false) return false;
			if (val === "client" || typeof val === "boolean") return val;
			return await get("future.compatibilityVersion") >= 5 ? "client" : true;
		} },
		clientFallback: false,
		crossOriginPrefetch: false,
		viewTransition: false,
		writeEarlyHints: false,
		componentIslands: { $resolve: (val) => {
			if (val === "local+remote") return { remoteIsland: true };
			if (val === "local") return true;
			return val ?? "auto";
		} },
		localLayerAliases: true,
		typedPages: false,
		appManifest: true,
		checkOutdatedBuildInterval: 1e3 * 60 * 60,
		watcher: { $resolve: async (val, get) => {
			if (typeof val === "string" && new Set([
				"chokidar",
				"parcel",
				"chokidar-granular"
			]).has(val)) return val;
			const [srcDir, rootDir] = await Promise.all([get("srcDir"), get("rootDir")]);
			if (srcDir === rootDir) return "chokidar-granular";
			return "chokidar";
		} },
		asyncContext: false,
		headNext: true,
		inlineRouteRules: false,
		scanPageMeta: { $resolve(val) {
			return typeof val === "boolean" || val === "after-resolve" ? val : "after-resolve";
		} },
		extraPageMetaExtractionKeys: [],
		sharedPrerenderData: { $resolve(val) {
			return typeof val === "boolean" ? val : true;
		} },
		cookieStore: true,
		defaults: {
			nuxtLink: {
				componentName: "NuxtLink",
				prefetch: true,
				prefetchOn: { visibility: true }
			},
			useAsyncData: { deep: false },
			useState: { resetOnClear: { $resolve: async (val, get) => {
				return typeof val === "boolean" ? val : await get("future.compatibilityVersion") >= 5;
			} } },
			useFetch: {}
		},
		clientNodeCompat: false,
		navigationRepaint: true,
		buildCache: false,
		normalizeComponentNames: { $resolve: (val) => {
			return typeof val === "boolean" ? val : true;
		} },
		normalizePageNames: { $resolve: async (val, get) => {
			return typeof val === "boolean" ? val : await get("future.compatibilityVersion") >= 5;
		} },
		spaLoadingTemplateLocation: { $resolve: (val) => {
			return typeof val === "string" && new Set(["body", "within"]).has(val) ? val : "body";
		} },
		browserDevtoolsTiming: { $resolve: (val, get) => typeof val === "boolean" ? val : get("dev") },
		chromeDevtoolsProjectSettings: true,
		debugModuleMutation: { $resolve: async (val, get) => {
			return typeof val === "boolean" ? val : Boolean(await get("debug"));
		} },
		lazyHydration: { $resolve: (val) => {
			return typeof val === "boolean" ? val : true;
		} },
		templateImportResolution: true,
		purgeCachedData: { $resolve: (val) => {
			return typeof val === "boolean" ? val : true;
		} },
		granularCachedData: { $resolve: (val) => {
			return typeof val === "boolean" ? val : true;
		} },
		alwaysRunFetchOnKeyChange: { $resolve: (val) => {
			return typeof val === "boolean" ? val : false;
		} },
		parseErrorData: { $resolve: (val) => {
			return typeof val === "boolean" ? val : true;
		} },
		enforceModuleCompatibility: false,
		pendingWhenIdle: { $resolve: (val) => {
			return typeof val === "boolean" ? val : false;
		} },
		entryImportMap: true,
		extractAsyncDataHandlers: { $resolve: (val) => {
			return typeof val === "boolean" ? val : false;
		} },
		viteEnvironmentApi: { $resolve: async (val, get) => {
			return typeof val === "boolean" ? val : await get("future.compatibilityVersion") >= 5;
		} },
		nitroAutoImports: { $resolve: async (val, get) => {
			return typeof val === "boolean" ? val : await get("future.compatibilityVersion") < 5;
		} },
		asyncCallHook: { $resolve: async (val, get) => {
			return typeof val === "boolean" ? val : await get("future.compatibilityVersion") < 5;
		} }
	}
});
//#endregion
//#region src/config/generate.ts
var generate_default = defineResolvers({ generate: {
	routes: [],
	exclude: []
} });
//#endregion
//#region src/config/internal.ts
var internal_default = defineResolvers({
	_majorVersion: 4,
	_legacyGenerate: false,
	_start: false,
	_build: false,
	_generate: false,
	_prepare: false,
	_cli: false,
	_requiredModules: {},
	_loadOptions: void 0,
	_nuxtConfigFile: void 0,
	_nuxtConfigFiles: [],
	appDir: "",
	_installedModules: [],
	_modules: []
});
//#endregion
//#region src/config/nitro.ts
var nitro_default = defineResolvers({
	server: { builder: { $resolve: (val) => {
		if (typeof val === "string") return val;
		if (val && typeof val === "object" && "bundle" in val) return val;
		return "@nuxt/nitro-server";
	} } },
	nitro: {
		runtimeConfig: { $resolve: async (val, get) => {
			const runtimeConfig = await get("runtimeConfig");
			return {
				...runtimeConfig,
				app: {
					...runtimeConfig.app,
					baseURL: runtimeConfig.app.baseURL.startsWith("./") ? runtimeConfig.app.baseURL.slice(1) : runtimeConfig.app.baseURL
				},
				nitro: {
					envPrefix: "NUXT_",
					...runtimeConfig.nitro
				}
			};
		} },
		routeRules: { $resolve: async (val, get) => {
			return {
				...await get("routeRules"),
				...val && typeof val === "object" ? val : {}
			};
		} }
	},
	routeRules: {},
	serverHandlers: [],
	devServerHandlers: []
});
//#endregion
//#region src/config/postcss.ts
const ensureItemIsLast = (item) => (arr) => {
	const index = arr.indexOf(item);
	if (index !== -1) {
		arr.splice(index, 1);
		arr.push(item);
	}
	return arr;
};
const orderPresets = {
	cssnanoLast: ensureItemIsLast("cssnano"),
	autoprefixerLast: ensureItemIsLast("autoprefixer"),
	autoprefixerAndCssnanoLast(names) {
		return orderPresets.cssnanoLast(orderPresets.autoprefixerLast(names));
	}
};
var postcss_default = defineResolvers({ postcss: {
	order: { $resolve: (val) => {
		if (typeof val === "string") {
			if (!(val in orderPresets)) throw new Error(`[nuxt] Unknown PostCSS order preset: ${val}`);
			return orderPresets[val];
		}
		if (typeof val === "function") return val;
		if (Array.isArray(val)) return val;
		return orderPresets.autoprefixerAndCssnanoLast;
	} },
	plugins: {
		autoprefixer: {},
		cssnano: { $resolve: async (val, get) => {
			if (val || val === false) return val;
			if (await get("dev")) return false;
			return {};
		} }
	}
} });
//#endregion
//#region src/config/router.ts
var router_default = defineResolvers({ router: { options: {
	hashMode: false,
	scrollBehaviorType: "auto"
} } });
//#endregion
//#region src/config/typescript.ts
var typescript_default = defineResolvers({ typescript: {
	strict: true,
	builder: { $resolve: (val) => {
		if (typeof val === "string" && new Set([
			"vite",
			"webpack",
			"rspack",
			"shared"
		]).has(val)) return val;
		if (val === false) return false;
		return null;
	} },
	hoist: { $resolve: (val) => {
		const defaults = [
			"@unhead/vue",
			"@nuxt/devtools",
			"vue",
			"@vue/runtime-core",
			"@vue/compiler-sfc",
			"vue-router",
			"vue-router/auto-routes",
			"@nuxt/schema",
			"nuxt"
		];
		return val === false ? [] : Array.isArray(val) ? val.concat(defaults) : defaults;
	} },
	includeWorkspace: false,
	typeCheck: false,
	tsConfig: {},
	shim: false
} });
//#endregion
//#region src/config/vite.ts
var vite_default = defineResolvers({ vite: {
	root: { $resolve: (val, get) => typeof val === "string" ? val : get("srcDir") },
	mode: { $resolve: async (val, get) => typeof val === "string" ? val : await get("dev") ? "development" : "production" },
	define: { $resolve: async (_val, get) => {
		const [isDev, isDebug] = await Promise.all([get("dev"), get("debug")]);
		return {
			"__VUE_PROD_HYDRATION_MISMATCH_DETAILS__": Boolean(isDebug && (isDebug === true || isDebug.hydration)),
			"process.dev": isDev,
			"import.meta.dev": isDev,
			"process.test": isTest,
			"import.meta.test": isTest,
			..._val && typeof _val === "object" ? _val : {}
		};
	} },
	resolve: { extensions: [
		".mjs",
		".js",
		".ts",
		".jsx",
		".tsx",
		".json",
		".vue"
	] },
	publicDir: { $resolve: (val) => {
		if (val) console.warn("Directly configuring the `vite.publicDir` option is not supported. Instead, set `dir.public`. You can read more in `https://nuxt.com/docs/4.x/api/nuxt-config#public`.");
		return false;
	} },
	vue: {
		isProduction: { $resolve: async (val, get) => typeof val === "boolean" ? val : !await get("dev") },
		template: {
			compilerOptions: { $resolve: async (val, get) => val ?? (await get("vue")).compilerOptions },
			transformAssetUrls: { $resolve: async (val, get) => val ?? (await get("vue")).transformAssetUrls }
		},
		script: { hoistStatic: { $resolve: async (val, get) => typeof val === "boolean" ? val : (await get("vue")).compilerOptions?.hoistStatic } },
		features: { propsDestructure: { $resolve: async (val, get) => {
			if (typeof val === "boolean") return val;
			const vueOptions = await get("vue") || {};
			return Boolean(vueOptions.script?.propsDestructure ?? vueOptions.propsDestructure);
		} } }
	},
	vueJsx: { $resolve: async (val, get) => {
		return {
			isCustomElement: (await get("vue")).compilerOptions?.isCustomElement,
			...typeof val === "object" ? val : {}
		};
	} },
	optimizeDeps: {
		esbuildOptions: { $resolve: async (val, get) => defu(val && typeof val === "object" ? val : {}, await get("esbuild.options")) },
		exclude: { $resolve: (val) => [...Array.isArray(val) ? val : [], "vue-demi"] }
	},
	esbuild: { $resolve: async (val, get) => {
		return defu(val && typeof val === "object" ? val : {}, await get("esbuild.options"));
	} },
	clearScreen: true,
	build: {
		assetsDir: { $resolve: async (val, get) => typeof val === "string" ? val : (await get("app")).buildAssetsDir?.replace(/^\/+/, "") },
		emptyOutDir: false
	},
	server: { fs: { allow: { $resolve: async (val, get) => {
		const [buildDir, srcDir, rootDir, workspaceDir] = await Promise.all([
			get("buildDir"),
			get("srcDir"),
			get("rootDir"),
			get("workspaceDir")
		]);
		return [...new Set([
			buildDir,
			srcDir,
			rootDir,
			workspaceDir,
			...Array.isArray(val) ? val : []
		])];
	} } } },
	cacheDir: { $resolve: async (val, get) => typeof val === "string" ? val : resolve(await get("rootDir"), "node_modules/.cache/vite") }
} });
//#endregion
//#region src/config/webpack.ts
var webpack_default = defineResolvers({ webpack: {
	analyze: { $resolve: async (val, get) => {
		return defu(typeof val === "boolean" ? { enabled: val } : val && typeof val === "object" ? val : {}, await get("build.analyze"));
	} },
	profile: process.argv.includes("--profile"),
	extractCSS: true,
	cssSourceMap: { $resolve: (val, get) => typeof val === "boolean" ? val : get("dev") },
	serverURLPolyfill: "url",
	filenames: {
		app: ({ isDev }) => isDev ? "[name].js" : "[contenthash:7].js",
		chunk: ({ isDev }) => isDev ? "[name].js" : "[contenthash:7].js",
		css: ({ isDev }) => isDev ? "[name].css" : "css/[contenthash:7].css",
		img: ({ isDev }) => isDev ? "[path][name].[ext]" : "img/[name].[contenthash:7].[ext]",
		font: ({ isDev }) => isDev ? "[path][name].[ext]" : "fonts/[name].[contenthash:7].[ext]",
		video: ({ isDev }) => isDev ? "[path][name].[ext]" : "videos/[name].[contenthash:7].[ext]"
	},
	loaders: {
		$resolve: async (val, get) => {
			const loaders = val && typeof val === "object" ? val : {};
			for (const name of [
				"css",
				"cssModules",
				"less",
				"sass",
				"scss",
				"stylus",
				"vueStyle"
			]) {
				const loader = loaders[name];
				if (loader && loader.sourceMap === void 0) loader.sourceMap = Boolean(await get("build.cssSourceMap"));
			}
			return loaders;
		},
		esbuild: { $resolve: async (val, get) => {
			return defu(val && typeof val === "object" ? val : {}, await get("esbuild.options"));
		} },
		file: {
			esModule: false,
			limit: 1e3
		},
		fontUrl: {
			esModule: false,
			limit: 1e3
		},
		imgUrl: {
			esModule: false,
			limit: 1e3
		},
		pugPlain: {},
		vue: {
			transformAssetUrls: { $resolve: async (val, get) => val ?? await get("vue.transformAssetUrls") },
			compilerOptions: { $resolve: async (val, get) => val ?? await get("vue.compilerOptions") },
			propsDestructure: { $resolve: async (val, get) => Boolean(val ?? await get("vue.propsDestructure")) }
		},
		css: {
			importLoaders: 0,
			url: { filter: (url, _resourcePath) => url[0] !== "/" },
			esModule: false
		},
		cssModules: {
			importLoaders: 0,
			url: { filter: (url, _resourcePath) => url[0] !== "/" },
			esModule: false,
			modules: { localIdentName: "[local]_[hash:base64:5]" }
		},
		less: {},
		sass: { sassOptions: { indentedSyntax: true } },
		scss: {},
		stylus: {},
		vueStyle: {}
	},
	plugins: [],
	aggressiveCodeRemoval: false,
	optimizeCSS: { $resolve: async (val, get) => {
		if (val === false || val && typeof val === "object") return val;
		return await get("build.extractCSS") ? {} : false;
	} },
	optimization: {
		runtimeChunk: "single",
		minimize: { $resolve: async (val, get) => typeof val === "boolean" ? val : !await get("dev") },
		minimizer: void 0,
		splitChunks: {
			chunks: "all",
			automaticNameDelimiter: "/",
			cacheGroups: {}
		}
	},
	postcss: { postcssOptions: { plugins: { $resolve: (val, get) => val && typeof val === "object" ? val : get("postcss.plugins") } } },
	devMiddleware: { stats: "none" },
	hotMiddleware: {},
	friendlyErrors: true,
	warningIgnoreFilters: [],
	experiments: {}
} });
//#endregion
//#region src/config/index.ts
var config_default = {
	...adhoc_default,
	...app_default,
	...build_default,
	...common_default,
	...dev_default,
	...experimental_default,
	...generate_default,
	...internal_default,
	...nitro_default,
	...postcss_default,
	...router_default,
	...typescript_default,
	...esbuild_default,
	...oxc_default,
	...vite_default,
	...webpack_default
};
//#endregion
export { config_default as NuxtConfigSchema };
