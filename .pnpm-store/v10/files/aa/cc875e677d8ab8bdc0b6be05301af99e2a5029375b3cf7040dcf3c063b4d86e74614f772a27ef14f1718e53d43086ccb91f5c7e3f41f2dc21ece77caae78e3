import { satisfies } from "semver";
import { $fetch } from "ofetch";
import { parseINI } from "confbox";

//#region ../nuxi/src/commands/module/_utils.ts
async function fetchModules() {
	const { modules } = await $fetch(`https://api.nuxt.com/modules?version=all`);
	return modules;
}
function checkNuxtCompatibility(module, nuxtVersion) {
	if (!module.compatibility?.nuxt) return true;
	return satisfies(nuxtVersion, module.compatibility.nuxt, { includePrerelease: true });
}
function getRegistryFromContent(content, scope) {
	try {
		const npmConfig = parseINI(content);
		if (scope) {
			const scopeKey = `${scope}:registry`;
			if (npmConfig[scopeKey]) return npmConfig[scopeKey].trim();
		}
		if (npmConfig.registry) return npmConfig.registry.trim();
		return null;
	} catch {
		return null;
	}
}

//#endregion
export { fetchModules as n, getRegistryFromContent as r, checkNuxtCompatibility as t };