const UNNAMED_GROUP_PREFIX = "__rou3_unnamed_";
/**
* Compiles the router instance into a faster route-matching function.
*
* **IMPORTANT:** `compileRouter` requires eval support with `new Function()` in the runtime for JIT compilation.
*
* @example
* import { createRouter, addRoute } from "rou3";
* import { compileRouter } from "rou3/compiler";
* const router = createRouter();
* // [add some routes]
* const findRoute = compileRouter(router);
* const matchAll = compileRouter(router, { matchAll: true });
* findRoute("GET", "/path/foo/bar");
*
* @param router - The router context to compile.
*/
function compileRouter(router, opts) {
	const ctx = {
		opts: opts || {},
		router,
		data: []
	};
	const compiled = compileRouteMatch(ctx);
	return new Function(...ctx.data.map((_, i) => `$${i}`), `return(m,p)=>{${compiled}}`)(...ctx.data);
}
/**
* Compile the router instance into a compact runnable code.
*
* **IMPORTANT:** Route data must be serializable to JSON (i.e., no functions or classes) or implement the `toJSON()` method to render custom code or you can pass custom `serialize` function in options.
*
* @example
* import { createRouter, addRoute } from "rou3";
* import { compileRouterToString } from "rou3/compiler";
* const router = createRouter();
* // [add some routes with serializable data]
* const compilerCode = compileRouterToString(router, "findRoute");
* // "const findRoute=(m, p) => {}"
*/
function compileRouterToString(router, functionName, opts) {
	const ctx = {
		opts: opts || {},
		router,
		data: [],
		compileToString: true
	};
	let compiled = `(m,p)=>{${compileRouteMatch(ctx)}}`;
	if (ctx.data.length > 0) compiled = `/* @__PURE__ */ (() => { ${`const ${ctx.data.map((v, i) => `$${i}=${v}`).join(",")};`}; return ${compiled}})()`;
	return functionName ? `const ${functionName}=${compiled};` : compiled;
}
function compileRouteMatch(ctx) {
	let code = "";
	{
		let hasIf = false;
		for (const key in ctx.router.static) {
			const node = ctx.router.static[key];
			if (node?.methods) {
				code += `${hasIf ? "else " : ""}if(p===${JSON.stringify(key.replace(/\/$/, "") || "/")}){${compileMethodMatch(ctx, node.methods, [], -1)}}`;
				hasIf = true;
			}
		}
	}
	const match = compileNode(ctx, ctx.router.root, [], 1);
	if (match) code += `let s=p.split("/"),l=s.length;${match}`;
	if (!code) return ctx.opts?.matchAll ? `return [];` : "";
	const normalizeHelper = code.includes("_normalizeGroups(") ? `const _prefix=${JSON.stringify(UNNAMED_GROUP_PREFIX)},_prefixLen=15;const _normalizeGroups=(g)=>{if(!g)return g;for(const k in g){if(k.startsWith(_prefix)){g[k.slice(_prefixLen)]=g[k];delete g[k]}}return g;};` : "";
	const normalizePathHelper = ctx.opts?.normalize ? `if(p.includes("/.")){let _r=[];for(let _v of p.split("/")){if(_v===".")continue;_v===".."&&_r.length>1?_r.pop():_r.push(_v)}p=_r.join("/")||"/"}` : "";
	return `${ctx.opts?.matchAll ? `let r=[];` : ""}${normalizeHelper}${normalizePathHelper}if(p.charCodeAt(p.length-1)===47)p=p.slice(0,-1)||"/";${code}${ctx.opts?.matchAll ? "return r;" : ""}`;
}
function compileMethodMatch(ctx, methods, params, currentIdx) {
	let code = "";
	for (const key in methods) {
		const matchers = methods[key];
		if (matchers && matchers.length > 0) {
			if (key !== "") code += `if(m==="${key}")${matchers.length > 1 ? "{" : ""}`;
			const _matchers = matchers.map((m) => compileFinalMatch(ctx, m, currentIdx, params)).sort((a, b) => b.weight - a.weight);
			for (const matcher of _matchers) code += matcher.code;
			if (key !== "") code += matchers.length > 1 ? "}" : "";
		}
	}
	return code;
}
function compileFinalMatch(ctx, data, currentIdx, params) {
	let ret = `{data:${serializeData(ctx, data.data)}`;
	const conditions = [];
	const { paramsMap, paramsRegexp } = data;
	if (paramsMap && paramsMap.length > 0) {
		if (!paramsMap[paramsMap.length - 1][2] && currentIdx !== -1) conditions.push(`l>${currentIdx}`);
		for (let i = 0; i < paramsRegexp.length; i++) {
			const regexp = paramsRegexp[i];
			if (!regexp) continue;
			conditions.push(`${regexp.toString()}.test(s[${i + 1}])`);
		}
		ret += ",params:{";
		for (let i = 0; i < paramsMap.length; i++) {
			const map = paramsMap[i];
			ret += typeof map[1] === "string" ? `${JSON.stringify(map[1])}:${params[i]},` : `..._normalizeGroups((${map[1].toString()}.exec(${params[i]}))?.groups),`;
		}
		ret += "}";
	}
	return {
		code: (conditions.length > 0 ? `if(${conditions.join("&&")})` : "") + (ctx.opts?.matchAll ? `r.unshift(${ret}});` : `return ${ret}};`),
		weight: conditions.length
	};
}
function compileNode(ctx, node, params, currentIdx) {
	const hasLastOptionalParam = node.key === "*";
	let code = "", hasIf = false;
	if (node.methods && params.length > 0) {
		const match = compileMethodMatch(ctx, node.methods, params, hasLastOptionalParam ? currentIdx - 1 : -1);
		if (match) {
			code += `if(l===${currentIdx}${hasLastOptionalParam ? `||l===${currentIdx - 1}` : ""}){${match}}`;
			hasIf = true;
		}
	}
	if (node.static) {
		let staticCode = "";
		const notNeedBoundCheck = hasIf;
		for (const key in node.static) {
			const match = compileNode(ctx, node.static[key], params, currentIdx + 1);
			if (match) {
				staticCode += `${hasIf ? "else " : ""}if(s[${currentIdx}]===${JSON.stringify(key)}){${match}}`;
				hasIf = true;
			}
		}
		if (staticCode) code += notNeedBoundCheck ? staticCode : `if(l>${currentIdx}){${staticCode}}`;
	}
	if (node.param) code += compileNode(ctx, node.param, params.concat(`s[${currentIdx}]`), currentIdx + 1);
	if (node.wildcard) {
		const { wildcard } = node;
		if (wildcard.static || wildcard.param || wildcard.wildcard) throw new Error("Compiler mode does not support patterns after wildcard");
		if (wildcard.methods) code += compileMethodMatch(ctx, wildcard.methods, params.concat(`s.slice(${currentIdx}).join('/')`), currentIdx);
	}
	return code;
}
function serializeData(ctx, value) {
	if (ctx.compileToString) if (ctx.opts?.serialize) value = ctx.opts.serialize(value);
	else if (typeof value?.toJSON === "function") value = value.toJSON();
	else value = JSON.stringify(value);
	let index = ctx.data.indexOf(value);
	if (index === -1) {
		ctx.data.push(value);
		index = ctx.data.length - 1;
	}
	return `$${index}`;
}
export { compileRouter, compileRouterToString };
