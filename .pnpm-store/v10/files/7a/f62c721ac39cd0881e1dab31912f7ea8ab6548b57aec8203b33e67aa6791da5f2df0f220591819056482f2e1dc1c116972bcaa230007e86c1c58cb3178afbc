import { existsSync } from 'node:fs';
import fsp from 'node:fs/promises';
import { hostname } from 'node:os';
import { resolve } from 'node:path';
import { startSubprocess } from '@nuxt/devtools-kit';
import { logger } from '@nuxt/kit';
import { execa } from 'execa';
import { checkPort, getPort } from 'get-port-please';
import which from 'which';
import { L as LOG_PREFIX } from './module-main.mjs';
import 'consola/utils';
import 'pathe';
import 'sirv';
import 'vite';
import '../shared/devtools.CT6XRG-F.mjs';
import '../dirs.mjs';
import 'node:url';
import 'is-installed-globally';
import 'ohash';
import 'birpc';
import 'structured-clone-es';
import 'simple-git';
import 'tinyglobby';
import 'image-meta';
import 'perfect-debounce';
import 'destr';
import '../../dist/runtime/shared/hooks.js';
import 'node:process';
import 'node:module';
import 'pkg-types';
import 'node:assert';
import 'node:v8';
import 'node:util';
import 'local-pkg';
import 'magicast';
import 'magicast/helpers';
import 'nypm';
import 'semver';
import 'unstorage';

const codeBinaryOptions = {
  "ms-code-cli": {
    codeBinary: "code",
    launchArg: "serve-web",
    licenseTermsArg: "--accept-server-license-terms",
    connectionTokenArg: "--without-connection-token"
  },
  "ms-code-server": {
    codeBinary: "code-server",
    launchArg: "serve-local",
    licenseTermsArg: "--accept-server-license-terms",
    connectionTokenArg: "--without-connection-token"
  },
  "coder-code-server": {
    codeBinary: "code-server",
    launchArg: "serve-local",
    licenseTermsArg: "",
    connectionTokenArg: ""
  }
};
async function setup({ nuxt, options, openInEditorHooks, rpc }) {
  const vsOptions = options?.vscode || {};
  const codeServer = vsOptions?.codeServer || "ms-code-server";
  const { codeBinary, launchArg, licenseTermsArg, connectionTokenArg } = codeBinaryOptions[codeServer];
  const installed = !!await which(codeBinary).catch(() => null);
  let port = vsOptions?.port || 3080;
  let url = `http://localhost:${port}`;
  const host = vsOptions?.host ? `--host=${vsOptions.host}` : "--host=127.0.0.1";
  let loaded = false;
  let promise = null;
  const mode = vsOptions?.mode || "local-serve";
  const computerHostName = vsOptions.tunnel?.name || hostname().split(".").join("");
  const root = nuxt.options.rootDir;
  const vscodeServerControllerFile = resolve(root, ".vscode", ".server-controller-port.log");
  openInEditorHooks.push(async (file) => {
    if (!existsSync(vscodeServerControllerFile))
      return false;
    try {
      const { port: port2 } = JSON.parse(await fsp.readFile(vscodeServerControllerFile, "utf-8"));
      const url2 = `http://localhost:${port2}/open?path=${encodeURIComponent(`${root}/${file}`)}`;
      await fetch(url2);
      rpc.broadcast.navigateTo("/modules/custom-builtin-vscode");
      return true;
    } catch (e) {
      console.debug(`Failed to open file "${file}" in VS Code Server`);
      console.debug(e);
      return false;
    }
  });
  async function startCodeServer() {
    if (existsSync(vscodeServerControllerFile))
      await fsp.rm(vscodeServerControllerFile, { force: true });
    if (vsOptions?.reuseExistingServer && !await checkPort(port)) {
      loaded = true;
      url = `http://localhost:${port}/?folder=${encodeURIComponent(root)}`;
      logger.info(LOG_PREFIX, `Existing VS Code Server found at port ${port}...`);
      return;
    }
    port = await getPort({ port });
    url = `http://localhost:${port}/?folder=${encodeURIComponent(root)}`;
    logger.info(LOG_PREFIX, `Starting VS Code Server at ${url} ...`);
    execa(codeBinary, [
      "--install-extension",
      "antfu.vscode-server-controller"
    ], { stderr: "inherit", stdout: "ignore", reject: false });
    startSubprocess(
      {
        command: codeBinary,
        args: [
          launchArg,
          licenseTermsArg,
          connectionTokenArg,
          `--port=${port}`,
          host
        ]
      },
      {
        id: "devtools:vscode",
        name: "VS Code Server",
        icon: "logos-visual-studio-code"
      },
      nuxt
    );
    for (let i = 0; i < 100; i++) {
      if (await fetch(url).then((r) => r.ok).catch(() => false))
        break;
      await new Promise((resolve2) => setTimeout(resolve2, 500));
    }
    await new Promise((resolve2) => setTimeout(resolve2, 2e3));
    loaded = true;
  }
  async function startCodeTunnel() {
    const { stdout: currentDir } = await execa("pwd");
    url = `https://vscode.dev/tunnel/${computerHostName}${currentDir}`;
    logger.info(LOG_PREFIX, `Starting VS Code tunnel at ${url} ...`);
    const command = execa("code", [
      "tunnel",
      "--accept-server-license-terms",
      "--name",
      `${computerHostName}`
    ]);
    command.stderr?.pipe(process.stderr);
    command.stdout?.pipe(process.stdout);
    nuxt.hook("close", () => {
      command.kill();
    });
    for (let i = 0; i < 100; i++) {
      if (await fetch(url).then((r) => r.ok).catch(() => false))
        break;
      await new Promise((resolve2) => setTimeout(resolve2, 500));
    }
    await new Promise((resolve2) => setTimeout(resolve2, 2e3));
    loaded = true;
  }
  async function start() {
    if (mode === "tunnel")
      await startCodeTunnel();
    else
      await startCodeServer();
  }
  nuxt.hook("devtools:customTabs", (tabs) => {
    tabs.push({
      name: "builtin-vscode",
      title: "VS Code",
      icon: "bxl-visual-studio",
      category: "modules",
      requireAuth: true,
      view: !installed && !(vsOptions?.mode === "tunnel") ? {
        type: "launch",
        title: "Install VS Code Server",
        description: `It seems you don't have code-server installed.

Learn more about it with <a href="https://code.visualstudio.com/blogs/2022/07/07/vscode-server" target="_blank">this guide</a>.
Once installed, restart Nuxt and visit this tab again.`,
        actions: []
      } : !loaded ? {
        type: "launch",
        description: "Launch VS Code right in the devtools!",
        actions: [{
          label: promise ? "Starting..." : "Launch",
          pending: !!promise,
          handle: () => {
            promise = promise || start();
            return promise;
          }
        }]
      } : {
        type: "iframe",
        src: url
      }
    });
  });
  if (vsOptions?.startOnBoot)
    promise = promise || start();
}

export { setup };
