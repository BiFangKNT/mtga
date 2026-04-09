import { n as logger } from "./logger-B4ge7MhP.mjs";
import { n as getPkgJSON, r as getPkgVersion } from "./versions-Bg99eDSc.mjs";
import { colors } from "consola/utils";

//#region ../nuxi/src/utils/banner.ts
function getBuilder(cwd, builder) {
	switch (builder) {
		case "rspack":
		case "@nuxt/rspack-builder": return {
			name: "Rspack",
			version: getPkgVersion(cwd, "@rspack/core")
		};
		case "webpack":
		case "@nuxt/webpack-builder": return {
			name: "Webpack",
			version: getPkgVersion(cwd, "webpack")
		};
		default: {
			const pkgJSON = getPkgJSON(cwd, "vite");
			return {
				name: pkgJSON.name.includes("rolldown") ? "Rolldown-Vite" : "Vite",
				version: pkgJSON.version
			};
		}
	}
}
function showVersionsFromConfig(cwd, config) {
	const { bold, gray, green } = colors;
	const nuxtVersion = getPkgVersion(cwd, "nuxt") || getPkgVersion(cwd, "nuxt-nightly") || getPkgVersion(cwd, "nuxt3") || getPkgVersion(cwd, "nuxt-edge");
	const nitroVersion = getPkgVersion(cwd, "nitropack") || getPkgVersion(cwd, "nitro") || getPkgVersion(cwd, "nitropack-nightly") || getPkgVersion(cwd, "nitropack-edge");
	const builder = getBuilder(cwd, config.builder);
	const vueVersion = getPkgVersion(cwd, "vue") || null;
	logger.info(green(`Nuxt ${bold(nuxtVersion)}`) + gray(" (with ") + (nitroVersion ? gray(`Nitro ${bold(nitroVersion)}`) : "") + gray(`, ${builder.name} ${bold(builder.version)}`) + (vueVersion ? gray(` and Vue ${bold(vueVersion)}`) : "") + gray(")"));
}
async function showVersions(cwd, kit, dotenv) {
	return showVersionsFromConfig(cwd, await kit.loadNuxtConfig({
		cwd,
		dotenv: dotenv ? {
			cwd,
			fileName: dotenv
		} : void 0
	}));
}

//#endregion
export { showVersions as n, showVersionsFromConfig as r, getBuilder as t };