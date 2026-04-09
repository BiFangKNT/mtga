import { t as FastURL } from "./_chunks/_url.mjs";
import { createReadStream } from "node:fs";
import { extname, join, resolve, sep } from "node:path";
import { readFile, stat } from "node:fs/promises";
import { FastResponse } from "srvx";
import { createBrotliCompress, createGzip } from "node:zlib";
//#region src/static.ts
const COMMON_MIME_TYPES = {
	".html": "text/html",
	".htm": "text/html",
	".css": "text/css",
	".js": "text/javascript",
	".mjs": "text/javascript",
	".json": "application/json",
	".txt": "text/plain",
	".xml": "application/xml",
	".gif": "image/gif",
	".ico": "image/vnd.microsoft.icon",
	".jpeg": "image/jpeg",
	".jpg": "image/jpeg",
	".png": "image/png",
	".svg": "image/svg+xml",
	".webp": "image/webp",
	".woff": "font/woff",
	".woff2": "font/woff2",
	".mp4": "video/mp4",
	".webm": "video/webm",
	".zip": "application/zip",
	".pdf": "application/pdf"
};
const serveStatic = (options) => {
	const dir = resolve(options.dir) + sep;
	const methods = new Set((options.methods || ["GET", "HEAD"]).map((m) => m.toUpperCase()));
	return async (req, next) => {
		if (!methods.has(req.method)) return next();
		const path = (req._url ??= new FastURL(req.url)).pathname.slice(1).replace(/\/$/, "");
		let paths;
		if (path === "") paths = ["index.html"];
		else if (extname(path) === "") paths = [`${path}.html`, `${path}/index.html`];
		else paths = [path];
		for (const path of paths) {
			const filePath = join(dir, path);
			if (!filePath.startsWith(dir)) continue;
			const fileStat = await stat(filePath).catch(() => null);
			if (fileStat?.isFile()) {
				const fileExt = extname(filePath);
				const headers = {
					"Content-Length": fileStat.size.toString(),
					"Content-Type": COMMON_MIME_TYPES[fileExt] || "application/octet-stream"
				};
				if (options.renderHTML && fileExt === ".html") return options.renderHTML({
					html: await readFile(filePath, "utf8"),
					filename: filePath,
					request: req
				});
				let stream = createReadStream(filePath);
				const acceptEncoding = req.headers.get("accept-encoding") || "";
				if (acceptEncoding.includes("br")) {
					headers["Content-Encoding"] = "br";
					delete headers["Content-Length"];
					headers["Vary"] = "Accept-Encoding";
					stream = stream.pipe(createBrotliCompress());
				} else if (acceptEncoding.includes("gzip")) {
					headers["Content-Encoding"] = "gzip";
					delete headers["Content-Length"];
					headers["Vary"] = "Accept-Encoding";
					stream = stream.pipe(createGzip());
				}
				return new FastResponse(stream, { headers });
			}
		}
		return next();
	};
};
//#endregion
export { serveStatic };
