import { n as logger } from "./logger-B4ge7MhP.mjs";
import process from "node:process";
import { colors } from "consola/utils";

//#region ../nuxi/src/utils/env.ts
function overrideEnv(targetEnv) {
	const currentEnv = process.env.NODE_ENV;
	if (currentEnv && currentEnv !== targetEnv) logger.warn(`Changing ${colors.cyan("NODE_ENV")} from ${colors.cyan(currentEnv)} to ${colors.cyan(targetEnv)}, to avoid unintended behavior.`);
	process.env.NODE_ENV = targetEnv;
}

//#endregion
export { overrideEnv as t };