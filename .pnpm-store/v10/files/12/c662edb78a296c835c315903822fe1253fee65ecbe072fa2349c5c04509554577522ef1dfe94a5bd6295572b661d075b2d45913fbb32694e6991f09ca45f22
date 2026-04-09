import { n as BaseComponent, t as publicDirURL } from "../../../public_dir-C5bujZKB.js";
var Layout = class extends BaseComponent {
	cssFile = new URL("./layout/style.css", publicDirURL);
	scriptFile = new URL("./layout/script.js", publicDirURL);
	async toHTML(props) {
		return `<!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>${props.title}</title>
        <!-- STYLES -->
        <!-- GLOBAL SCRIPT -->
      </head>
      <body>
        <div id="layout">
          ${await props.children()}
        </div>
        <!-- SCRIPTS -->
      </body>
    </html>`;
	}
	async toANSI(props) {
		return `\n${await props.children()}\n`;
	}
};
export { Layout };
