import { t as cwdArgs } from "./_shared-BsGoKfo3.mjs";
import { n as logger } from "./logger-B4ge7MhP.mjs";
import "./kit-DUlGqV3Z.mjs";
import { t as getNuxtVersion } from "./versions-Bg99eDSc.mjs";
import { t as formatInfoBox } from "./formatting-BVTBOej7.mjs";
import { n as fetchModules, t as checkNuxtCompatibility } from "./_utils-Co1L4CHe.mjs";
import { defineCommand } from "citty";
import { colors } from "consola/utils";
import { box } from "@clack/prompts";
import { kebabCase, upperFirst } from "scule";
import Fuse from "fuse.js";

//#region ../nuxi/src/commands/module/search.ts
const DASH_RE = /-/g;
const { format: formatNumber } = Intl.NumberFormat("en-GB", {
	notation: "compact",
	maximumFractionDigits: 1
});
var search_default = defineCommand({
	meta: {
		name: "search",
		description: "Search in Nuxt modules"
	},
	args: {
		...cwdArgs,
		query: {
			type: "positional",
			description: "keywords to search for",
			required: true
		},
		nuxtVersion: {
			type: "string",
			description: "Filter by Nuxt version and list compatible modules only (auto detected by default)",
			required: false,
			valueHint: "2|3"
		}
	},
	async setup(ctx) {
		const nuxtVersion = await getNuxtVersion(ctx.args.cwd);
		return findModuleByKeywords(ctx.args._.join(" "), nuxtVersion);
	}
});
async function findModuleByKeywords(query, nuxtVersion) {
	const results = new Fuse((await fetchModules()).filter((m) => checkNuxtCompatibility(m, nuxtVersion)), {
		threshold: .1,
		keys: [
			{
				name: "name",
				weight: 1
			},
			{
				name: "npm",
				weight: 1
			},
			{
				name: "repo",
				weight: 1
			},
			{
				name: "tags",
				weight: 1
			},
			{
				name: "category",
				weight: 1
			},
			{
				name: "description",
				weight: .5
			},
			{
				name: "maintainers.name",
				weight: .5
			},
			{
				name: "maintainers.github",
				weight: .5
			}
		]
	}).search(query).map((result) => {
		const res = {
			name: result.item.name,
			package: result.item.npm,
			homepage: colors.cyan(result.item.website),
			compatibility: `nuxt: ${result.item.compatibility?.nuxt || "*"}`,
			repository: result.item.github,
			description: result.item.description,
			install: `npx nuxt add ${result.item.name}`,
			stars: colors.yellow(formatNumber(result.item.stats.stars)),
			monthlyDownloads: colors.yellow(formatNumber(result.item.stats.downloads))
		};
		if (result.item.github === result.item.website) delete res.homepage;
		if (result.item.name === result.item.npm) delete res.packageName;
		return res;
	});
	if (!results.length) {
		logger.info(`No Nuxt modules found matching query ${colors.magenta(query)} for Nuxt ${colors.cyan(nuxtVersion)}`);
		return;
	}
	logger.success(`Found ${results.length} Nuxt ${results.length > 1 ? "modules" : "module"} matching ${colors.cyan(query)} ${nuxtVersion ? `for Nuxt ${colors.cyan(nuxtVersion)}` : ""}:\n`);
	for (const foundModule of results) {
		const formattedModule = {};
		for (const [key, val] of Object.entries(foundModule)) {
			const label = upperFirst(kebabCase(key)).replace(DASH_RE, " ");
			formattedModule[label] = val;
		}
		const title = formattedModule.Name || formattedModule.Package;
		delete formattedModule.Name;
		box(`\n${formatInfoBox(formattedModule)}`, ` ${title} `, {
			contentAlign: "left",
			titleAlign: "left",
			width: "auto",
			titlePadding: 2,
			contentPadding: 2,
			rounded: true
		});
	}
}

//#endregion
export { search_default as default };