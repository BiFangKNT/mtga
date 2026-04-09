function getInitParams(workspaceUri) {
  const defaultVLSConfig = getDefaultVLSConfig();
  defaultVLSConfig.vetur.validation = {
    template: true,
    style: true,
    script: true,
    interpolation: true,
    templateProps: true
  };
  defaultVLSConfig.vetur.experimental = {
    templateInterpolationService: true
  };
  const init = {
    rootPath: workspaceUri.fsPath,
    rootUri: workspaceUri.toString(),
    processId: process.pid,
    capabilities: {},
    initializationOptions: {
      config: defaultVLSConfig
    }
  };
  return init;
}
function getDefaultVLSConfig() {
  return {
    vetur: {
      ignoreProjectWarning: false,
      useWorkspaceDependencies: false,
      validation: {
        template: true,
        templateProps: true,
        interpolation: true,
        style: true,
        script: true
      },
      completion: {
        autoImport: false,
        tagCasing: "initial",
        scaffoldSnippetSources: {
          workspace: "\u{1F4BC}",
          user: "\u{1F5D2}\uFE0F",
          vetur: "\u270C"
        }
      },
      grammar: {
        customBlocks: {}
      },
      format: {
        enable: true,
        options: {
          tabSize: 2,
          useTabs: false
        },
        defaultFormatter: {},
        defaultFormatterOptions: {},
        scriptInitialIndent: false,
        styleInitialIndent: false
      },
      languageFeatures: {
        codeActions: true,
        updateImportOnFileMove: true,
        semanticTokens: true
      },
      trace: {
        server: "off"
      },
      dev: {
        vlsPath: "",
        vlsPort: -1,
        logLevel: "INFO"
      },
      experimental: {
        templateInterpolationService: false
      }
    },
    css: {},
    html: {
      suggest: {}
    },
    javascript: {
      format: {}
    },
    typescript: {
      tsdk: null,
      format: {}
    },
    emmet: {},
    stylusSupremacy: {}
  };
}
export {
  getDefaultVLSConfig,
  getInitParams
};
//# sourceMappingURL=initParams.js.map