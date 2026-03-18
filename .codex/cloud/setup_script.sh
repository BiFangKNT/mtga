#!/usr/bin/env bash
set -euo pipefail

export SHELL=bash

CACHE_ROOT="$HOME/.cache/codex"
STATE_DIR="$CACHE_ROOT/state"
PYEMBED_CACHE_ROOT="$CACHE_ROOT/pyembed"
mkdir -p "$STATE_DIR" "$PYEMBED_CACHE_ROOT" ~/.codex

# GH_TOKEN 不在脚本里硬编码。
# 需要 agent 也能使用时，请在 Codex 环境里配置为 Environment Variable。

cat > ~/.codex/AGENTS.md <<'EOF'
永远使用中文

### 已安装

- ast-grep (别名 sg)
- rg
- dust
- gh
- jq
- uv

### shell调用限制

进行代码搜索或批量替换时必须优先使用`ast-grep`而不是`rg`
EOF

# ---- pnpm：安装后仅为当前 setup shell 补 PATH ----
curl -fsSL https://get.pnpm.io/install.sh | sh -
export PNPM_HOME="/root/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"

pnpm add -g @ast-grep/cli
pnpm approve-builds -g --all

# ---- fnm / node：安装后仅为当前 setup shell 生效 ----
curl -fsSL https://fnm.vercel.app/install | bash
export FNM_PATH="/root/.local/share/fnm"
export PATH="$FNM_PATH:$PATH"
eval "$(fnm env --shell bash)"

fnm install
fnm use

# ---- 系统工具 ----
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y universe
sudo apt-get update
sudo apt-get install -y jq ripgrep gh
curl -sSfL https://raw.githubusercontent.com/bootandy/dust/refs/heads/master/install.sh | sh

# ---- uv：安装后仅为当前 setup shell 补 PATH ----
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# ---- 项目依赖（这些会随 setup 结果一起进入容器缓存）----
pnpm install --frozen-lockfile
uv sync --project python-src --frozen

# ---- 记录 lockfile 指纹，供 maintenance 判断是否需要补装 ----
if [ -f pnpm-lock.yaml ]; then
  sha256sum pnpm-lock.yaml > "$STATE_DIR/pnpm-lock.sha256"
fi

if [ -f python-src/uv.lock ]; then
  sha256sum python-src/uv.lock > "$STATE_DIR/uv-lock.sha256"
fi

# ---- 下载并缓存 python-build-standalone 到仓库外，避免分支切换干扰 ----
PYEMBED_LINK="src-tauri/pyembed"

ASSET_JSON=$(
  gh api /repos/astral-sh/python-build-standalone/releases/latest \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    --jq '.assets[]
      | select(.name | test("cpython-3\\.13\\..*\\+.*-x86_64-unknown-linux-gnu-install_only_stripped\\.tar\\.gz"))
      | [.name, .browser_download_url]
      | @tsv' \
    | head -n 1
)

if [ -z "$ASSET_JSON" ]; then
  echo "未找到匹配的 python-build-standalone 产物"
  exit 1
fi

ASSET_NAME="$(printf '%s\n' "$ASSET_JSON" | cut -f1)"
ASSET_URL="$(printf '%s\n' "$ASSET_JSON" | cut -f2)"
ASSET_DIR_NAME="${ASSET_NAME%.tar.gz}"
PYEMBED_TARGET="$PYEMBED_CACHE_ROOT/$ASSET_DIR_NAME"

if [ ! -f "$PYEMBED_TARGET/.ready" ]; then
  rm -rf "$PYEMBED_TARGET"
  mkdir -p "$PYEMBED_TARGET"
  curl -L "$ASSET_URL" -o /tmp/python-standalone.tar.gz
  tar -xzf /tmp/python-standalone.tar.gz -C "$PYEMBED_TARGET"
  touch "$PYEMBED_TARGET/.ready"
fi

printf '%s\n' "$PYEMBED_TARGET" > "$STATE_DIR/pyembed-target"

rm -rf "$PYEMBED_LINK"
ln -sfn "$PYEMBED_TARGET" "$PYEMBED_LINK"