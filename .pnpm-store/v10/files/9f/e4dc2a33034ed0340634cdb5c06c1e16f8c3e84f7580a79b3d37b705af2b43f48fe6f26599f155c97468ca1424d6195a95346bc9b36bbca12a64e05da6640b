class FileDiagnosticManager {
  diagnostics = [];
  /**
   * Initialize and reset the diagnostics array
   */
  initWith(diagnostics) {
    this.diagnostics = [...diagnostics];
  }
  getDiagnostics(fileName) {
    if (fileName) {
      return this.diagnostics.filter((f) => f.id === fileName);
    }
    return this.diagnostics;
  }
  updateByFileId(fileId, next) {
    this.diagnostics = this.diagnostics.filter((d) => d.id !== fileId);
    if (next == null ? void 0 : next.length) {
      this.diagnostics.push(...next);
    }
  }
}
export {
  FileDiagnosticManager
};
//# sourceMappingURL=FileDiagnosticManager.js.map