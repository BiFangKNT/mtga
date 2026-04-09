import { a as green, i as gray, n as bold, s as red } from "./_utils.mjs";
//#region src/_middleware.ts
function wrapFetch(server) {
	const fetchHandler = server.options.fetch;
	const middleware = server.options.middleware || [];
	return middleware.length === 0 ? fetchHandler : (request) => callMiddleware(request, fetchHandler, middleware, 0);
}
function callMiddleware(request, fetchHandler, middleware, index) {
	if (index === middleware.length) return fetchHandler(request);
	return middleware[index](request, () => callMiddleware(request, fetchHandler, middleware, index + 1));
}
//#endregion
//#region src/_plugins.ts
const errorPlugin = (server) => {
	const errorHandler = server.options.error;
	if (!errorHandler) return;
	server.options.middleware.unshift((_req, next) => {
		try {
			const res = next();
			return res instanceof Promise ? res.catch((error) => errorHandler(error)) : res;
		} catch (error) {
			return errorHandler(error);
		}
	});
};
const gracefulShutdownPlugin = (server) => {
	const config = server.options?.gracefulShutdown;
	if (!globalThis.process?.on || config === false || config === void 0 && (process.env.CI || process.env.TEST)) return;
	const gracefulTimeout = config === true || !config?.gracefulTimeout ? Number.parseInt(process.env.SERVER_SHUTDOWN_TIMEOUT || "") || 5 : config.gracefulTimeout;
	let isClosing = false;
	let isClosed = false;
	const w = server.options.silent ? () => {} : process.stderr.write.bind(process.stderr);
	const forceClose = async () => {
		if (isClosed) return;
		w(red("\x1B[2K\rForcibly closing connections...\n"));
		isClosed = true;
		await server.close(true);
	};
	const shutdown = async () => {
		if (isClosing || isClosed) return;
		setTimeout(() => {
			globalThis.process.once("SIGINT", forceClose);
		}, 100);
		isClosing = true;
		const closePromise = server.close();
		for (let remaining = gracefulTimeout; remaining > 0; remaining--) {
			w(gray(`\rStopping server gracefully (${remaining}s)... Press ${bold("Ctrl+C")} again to force close.`));
			if (await Promise.race([closePromise.then(() => true), new Promise((r) => setTimeout(() => r(false), 1e3))])) {
				w("\x1B[2K\r" + green("Server closed successfully.\n"));
				isClosed = true;
				return;
			}
		}
		w("\x1B[2K\rGraceful shutdown timed out.\n");
		await forceClose();
	};
	for (const sig of ["SIGINT", "SIGTERM"]) globalThis.process.on(sig, shutdown);
};
//#endregion
export { gracefulShutdownPlugin as n, wrapFetch as r, errorPlugin as t };
