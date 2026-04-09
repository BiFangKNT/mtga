import { ServerMiddleware } from "./types.mjs";

//#region src/static.d.ts
interface ServeStaticOptions {
  /**
  * The directory to serve static files from.
  */
  dir: string;
  /**
  * The HTTP methods to allow for serving static files.
  */
  methods?: string[];
  /**
  * A function to modify the HTML content before serving it.
  */
  renderHTML?: (ctx: {
    request: Request;
    html: string;
    filename: string;
  }) => Response | Promise<Response>;
}
declare const serveStatic: (options: ServeStaticOptions) => ServerMiddleware;
//#endregion
export { ServeStaticOptions, serveStatic };