import { n as themeColor } from "./ascii-AoH-yOf6.mjs";
import process from "node:process";
import { colors } from "consola/utils";
import { box } from "@clack/prompts";
import { join, relative } from "pathe";
import { mkdirSync, writeFileSync } from "node:fs";

//#region ../nuxi/src/utils/profile.ts
const RELATIVE_PATH_RE = /^(?![^.]{1,2}\/)/;
let session;
let profileCount = 0;
async function startCpuProfile() {
	const cli = globalThis.__nuxt_cli__;
	if (cli?.cpuProfileSession) {
		session = cli.cpuProfileSession;
		delete cli.cpuProfileSession;
		return;
	}
	session = new (await (import("node:inspector"))).Session();
	session.connect();
	try {
		await new Promise((res, rej) => {
			session.post("Profiler.enable", (err) => {
				if (err) return rej(err);
				session.post("Profiler.start", (err) => {
					if (err) return rej(err);
					res();
				});
			});
		});
	} catch (err) {
		session.disconnect();
		session = void 0;
		throw err;
	}
}
async function stopCpuProfile(outDir, command) {
	if (!session) return;
	const s = session;
	session = void 0;
	const count = profileCount++;
	const outPath = join(outDir, `nuxt-${command}${count ? `-${count}` : ""}.cpuprofile`);
	const relativeOutPath = relative(process.cwd(), outPath).replace(RELATIVE_PATH_RE, "./");
	try {
		await new Promise((resolve, reject) => {
			s.post("Profiler.stop", (err, params) => {
				if (err) return reject(err);
				if (!params?.profile) return resolve(params);
				try {
					mkdirSync(outDir, { recursive: true });
					writeFileSync(outPath, JSON.stringify(params.profile));
					box(`\n${[`CPU profile written to ${colors.cyan(relativeOutPath)}.`, `Open it in a CPU profile viewer like your IDE, or ${colors.cyan("https://discoveryjs.github.io/cpupro")}.`].map((step) => ` › ${step}`).join("\n")}\n`, "", {
						contentAlign: "left",
						titleAlign: "left",
						width: "auto",
						titlePadding: 2,
						contentPadding: 2,
						rounded: true,
						withGuide: false,
						formatBorder: (text) => `${themeColor + text}\x1B[0m`
					});
				} catch {}
				resolve(params);
			});
		});
	} finally {
		s.disconnect();
	}
}

//#endregion
export { stopCpuProfile as n, startCpuProfile as t };