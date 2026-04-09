import { defineNuxtModule } from '@nuxt/kit';
import { isGlobalInstall } from '../dirs.mjs';

const e=globalThis.process?.env||Object.create(null),t=globalThis.process||{env:e},n=t!==void 0&&t.env&&t.env.NODE_ENV||void 0,r=[[`claude`,[`CLAUDECODE`,`CLAUDE_CODE`]],[`replit`,[`REPL_ID`]],[`gemini`,[`GEMINI_CLI`]],[`codex`,[`CODEX_SANDBOX`,`CODEX_THREAD_ID`]],[`opencode`,[`OPENCODE`]],[`pi`,[i(`PATH`,/\.pi[\\/]agent/)]],[`auggie`,[`AUGMENT_AGENT`]],[`goose`,[`GOOSE_PROVIDER`]],[`devin`,[i(`EDITOR`,/devin/)]],[`cursor`,[`CURSOR_AGENT`]],[`kiro`,[i(`TERM_PROGRAM`,/kiro/)]]];function i(t,n){return ()=>{let r=e[t];return r?n.test(r):false}}function a(){let t=e.AI_AGENT;if(t)return {name:t.toLowerCase()};for(let[t,n]of r)for(let r of n)if(typeof r==`string`?e[r]:r())return {name:t};return {}}const o=a();o.name;!!o.name;const l=[[`APPVEYOR`],[`AWS_AMPLIFY`,`AWS_APP_ID`,{ci:true}],[`AZURE_PIPELINES`,`SYSTEM_TEAMFOUNDATIONCOLLECTIONURI`],[`AZURE_STATIC`,`INPUT_AZURE_STATIC_WEB_APPS_API_TOKEN`],[`APPCIRCLE`,`AC_APPCIRCLE`],[`BAMBOO`,`bamboo_planKey`],[`BITBUCKET`,`BITBUCKET_COMMIT`],[`BITRISE`,`BITRISE_IO`],[`BUDDY`,`BUDDY_WORKSPACE_ID`],[`BUILDKITE`],[`CIRCLE`,`CIRCLECI`],[`CIRRUS`,`CIRRUS_CI`],[`CLOUDFLARE_PAGES`,`CF_PAGES`,{ci:true}],[`CLOUDFLARE_WORKERS`,`WORKERS_CI`,{ci:true}],[`GOOGLE_CLOUDRUN`,`K_SERVICE`],[`GOOGLE_CLOUDRUN_JOB`,`CLOUD_RUN_JOB`],[`CODEBUILD`,`CODEBUILD_BUILD_ARN`],[`CODEFRESH`,`CF_BUILD_ID`],[`DRONE`],[`DRONE`,`DRONE_BUILD_EVENT`],[`DSARI`],[`GITHUB_ACTIONS`],[`GITLAB`,`GITLAB_CI`],[`GITLAB`,`CI_MERGE_REQUEST_ID`],[`GOCD`,`GO_PIPELINE_LABEL`],[`LAYERCI`],[`JENKINS`,`JENKINS_URL`],[`HUDSON`,`HUDSON_URL`],[`MAGNUM`],[`NETLIFY`],[`NETLIFY`,`NETLIFY_LOCAL`,{ci:false}],[`NEVERCODE`],[`RENDER`],[`SAIL`,`SAILCI`],[`SEMAPHORE`],[`SCREWDRIVER`],[`SHIPPABLE`],[`SOLANO`,`TDDIUM`],[`STRIDER`],[`TEAMCITY`,`TEAMCITY_VERSION`],[`TRAVIS`],[`VERCEL`,`NOW_BUILDER`],[`VERCEL`,`VERCEL`,{ci:false}],[`VERCEL`,`VERCEL_ENV`,{ci:false}],[`APPCENTER`,`APPCENTER_BUILD_ID`],[`CODESANDBOX`,`CODESANDBOX_SSE`,{ci:false}],[`CODESANDBOX`,`CODESANDBOX_HOST`,{ci:false}],[`STACKBLITZ`],[`STORMKIT`],[`CLEAVR`],[`ZEABUR`],[`CODESPHERE`,`CODESPHERE_APP_ID`,{ci:true}],[`RAILWAY`,`RAILWAY_PROJECT_ID`],[`RAILWAY`,`RAILWAY_SERVICE_ID`],[`DENO-DEPLOY`,`DENO_DEPLOY`],[`DENO-DEPLOY`,`DENO_DEPLOYMENT_ID`],[`FIREBASE_APP_HOSTING`,`FIREBASE_APP_HOSTING`,{ci:true}]];function u(){for(let t of l)if(e[t[1]||t[0]])return {name:t[0].toLowerCase(),...t[2]};return e.SHELL===`/bin/jsh`&&t.versions?.webcontainer?{name:`stackblitz`,ci:false}:{name:``,ci:false}}const d=u(),f=d.name,p=t.platform||``,m=!!e.CI||d.ci!==false,h=!!t.stdout?.isTTY;!!e.DEBUG;const v=n===`test`||!!e.TEST;n===`production`||e.MODE===`production`;n===`dev`||n===`development`||e.MODE===`development`;!!e.MINIMAL||m||v||!h;const S=/^win/i.test(p);!e.NO_COLOR&&(!!e.FORCE_COLOR||(h||S)&&e.TERM!==`dumb`||m);const E=(t.versions?.node||``).replace(/^v/,``)||null;Number(E?.split(`.`)[0])||null;const O=!!t?.versions?.node,k=`Bun`in globalThis,A=`Deno`in globalThis,j=`fastly`in globalThis,M=`Netlify`in globalThis,N=`EdgeRuntime`in globalThis,P=globalThis.navigator?.userAgent===`Cloudflare-Workers`,F=[[M,`netlify`],[N,`edge-light`],[P,`workerd`],[j,`fastly`],[A,`deno`],[k,`bun`],[O,`node`]];function I(){let e=F.find(e=>e[0]);if(e)return {name:e[1]}}const L=I();L?.name||``;

const WS_EVENT_NAME = "nuxt:devtools:rpc";
const isSandboxed = f === "stackblitz" || f === "codesandbox";
const defaultOptions = {
  enabled: void 0,
  // determine multiple conditions
  componentInspector: true,
  viteInspect: true,
  vscode: {
    enabled: true,
    startOnBoot: false,
    port: 3080,
    reuseExistingServer: true
  },
  disableAuthorization: isSandboxed
};
const defaultTabOptions = {
  behavior: {
    telemetry: null,
    openInEditor: void 0
  },
  ui: {
    componentsView: "list",
    componentsGraphShowNodeModules: false,
    componentsGraphShowGlobalComponents: true,
    componentsGraphShowPages: false,
    componentsGraphShowLayouts: false,
    componentsGraphShowWorkspace: true,
    interactionCloseOnOutsideClick: false,
    showExperimentalFeatures: false,
    showHelpButtons: true,
    showPanel: true,
    scale: 1,
    minimizePanelInactive: 5e3,
    hiddenTabs: [],
    pinnedTabs: [],
    hiddenTabCategories: [],
    sidebarExpanded: false,
    sidebarScrollable: false
  },
  serverRoutes: {
    selectedRoute: null,
    view: "tree",
    inputDefaults: {
      query: [],
      body: [],
      headers: []
    },
    sendFrom: "app"
  },
  serverTasks: {
    enabled: false,
    selectedTask: null,
    view: "list",
    inputDefaults: {
      query: [],
      body: [],
      headers: [{ active: true, key: "Content-Type", value: "application/json", type: "string" }]
    }
  },
  assets: {
    view: "grid"
  }
};
const defaultAllowedExtensions = [
  "png",
  "jpg",
  "jpeg",
  "gif",
  "svg",
  "webp",
  "ico",
  "mp4",
  "ogg",
  "mp3",
  "wav",
  "mov",
  "mkv",
  "mpg",
  "txt",
  "ttf",
  "woff",
  "woff2",
  "eot",
  "json",
  "js",
  "jsx",
  "ts",
  "tsx",
  "md",
  "mdx",
  "vue",
  "webm"
];

const module$1 = defineNuxtModule({
  meta: {
    name: "@nuxt/devtools",
    configKey: "devtools"
  },
  defaults: defaultOptions,
  setup(options, nuxt) {
    if (process.env.VITEST || process.env.TEST)
      return;
    if (typeof options === "boolean")
      options = { enabled: options };
    if (options.enabled === false)
      return;
    if (isGlobalInstall()) {
      const globalOptions = nuxt.options.devtoolsGlobal || {};
      if (options.enabled !== true && !globalOptions.projects?.includes(nuxt.options.rootDir))
        return;
    }
    return import('../chunks/module-main.mjs').then(function (n) { return n.m; }).then(({ enableModule }) => enableModule(options, nuxt));
  }
});

export { WS_EVENT_NAME as W, defaultTabOptions as a, defaultAllowedExtensions as d, module$1 as m };
