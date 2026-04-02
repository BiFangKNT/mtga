# scripts 目录说明

此目录用于仓库维护流程脚本，不面向普通最终用户。

## 前置依赖

- Node.js 版本需满足仓库要求（见根目录 `package.json` 的 `engines.node`）。
- 已安装 `pnpm`。
- 使用 `gitflow.mjs` 时需安装 [git-flow-next](https://github.com/gittower/git-flow-next) 且 `git-flow` 在 `PATH` 中可用。
- 使用 `ci-gate.mjs` 的 `py` 目标时需安装 `uv`。
- 使用 `rs-check.mjs` 时需安装 Rust 工具链（`cargo`）。

## 当前脚本清单

- `ci-gate.mjs`
  - 统一质量检查入口，支持目标：`app`、`py`、`rs`、`all`。
  - `app`：执行 `postinstall`、`prettier --check`、`eslint`、`vue-tsc`。
  - `py`：在 `python-src` 下执行 `uv run pyright` 与 `uv run ruff check .`。
  - `rs`：调用 `node ./scripts/rs-check.mjs gate`。
- `gitflow.mjs`
  - `setup`：清理本地 `gitflow.*` 配置，重新 `git-flow init`，并配置 release 默认打 tag。
  - `finish`：在 `release/<version>` 分支执行发布收尾，包含工作区、版本、tag 冲突检查，完成后推送分支与 tag，并切回开发分支。
  - `finish` 参数：
    - `-v, --version`（兼容 `--Version`）
    - `-r, --remote`（兼容 `--Remote`）
    - `-m, --main-branch`（兼容 `--MainBranch`）
    - `-d, --dev-branch`（兼容 `--DevBranch`）
- `prettier-check-locations.mjs`
  - 定位 Prettier 不一致位置，按 `file:line:column: message` 输出，便于编辑器问题匹配器跳转。
- `prune-pyembed.mjs`
  - 裁剪 `src-tauri/pyembed/python` 内确定无运行时用途的内容。
  - 当前会清理：`pip`、CLI 包装脚本、`ensurepip`、`idlelib`、`tkinter/tcl`、`turtledemo`、`__pycache__`、`.pyc/.pyo`、以及 `modules/resources/openssl`。
  - 支持 `--dry-run` 仅预览待删除项，不写入文件。
- `rs-check.mjs`
  - Rust 检查入口，模式：`dev`（默认）与 `gate`。
  - `dev`：要求本地 pyembed Python 存在，并设置 `PYO3_PYTHON` 后执行 `cargo fmt` + `cargo check -p mtga-tauri`。
  - `gate`：执行 `cargo fmt --check` + `cargo check -p mtga-tauri`，并准备 `src-tauri/pyembed/python` 目录。

## package.json 对应入口

- `pnpm gate -- <app|py|rs|all>`
- `pnpm app:gate`
- `pnpm py:gate`
- `pnpm rs:gate`
- `pnpm rs:check`
- `pnpm pyembed:prune`
- `pnpm pyembed:prune:dry-run`
- `pnpm gitflow:setup`
- `pnpm release:push`
- `pnpm release:push -- -v 2.0.0-beta.10 -r origin -m tauri -d dev`

## 本地 Tauri 打包

- `pnpm tauri:bundle:win`
- `pnpm tauri:bundle:mac`

以上本地 bundle 脚本会先执行 `pnpm pyembed:prune`，再进入 Tauri 构建；CI 使用的 `*:ci` 脚本当前不受影响。
