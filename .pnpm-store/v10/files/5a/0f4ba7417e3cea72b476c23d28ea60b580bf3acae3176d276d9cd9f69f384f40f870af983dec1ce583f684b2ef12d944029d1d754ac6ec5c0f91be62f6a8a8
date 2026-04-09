import invariant from "tiny-invariant";
import { isInVitestEntryThread, isMainThread } from "./utils.js";
import { createScript } from "./worker.js";
if (!(isMainThread || isInVitestEntryThread)) {
  process.stdout.isTTY = true;
}
class Checker {
  static logger = [];
  static log(...args) {
    for (const fn of Checker.logger) {
      fn(...args);
    }
  }
  name;
  absFilePath;
  createDiagnostic;
  build;
  script;
  constructor({
    name,
    absFilePath,
    createDiagnostic,
    build
  }) {
    this.name = name;
    this.absFilePath = absFilePath;
    this.build = build;
    this.createDiagnostic = createDiagnostic;
    this.build = build;
  }
  prepare() {
    const script = createScript({
      absFilename: this.absFilePath,
      buildBin: this.build.buildBin,
      serverChecker: { createDiagnostic: this.createDiagnostic }
    });
    this.script = script;
    return script;
  }
  initMainThread() {
    invariant(
      this.script,
      `script should be created in 'prepare', but got ${this.script}`
    );
    if (isMainThread || isInVitestEntryThread) {
      const createServeAndBuild = this.script.mainScript();
      return createServeAndBuild;
    }
    return;
  }
  initWorkerThread() {
    invariant(
      this.script,
      `script should be created in 'prepare', but got ${this.script}`
    );
    if (!(isMainThread || isInVitestEntryThread)) {
      this.script.workerScript();
    }
  }
}
export {
  Checker
};
//# sourceMappingURL=Checker.js.map