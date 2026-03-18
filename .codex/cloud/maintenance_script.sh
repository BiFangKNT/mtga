#!/usr/bin/env bash
set -euo pipefail

CACHE_ROOT="$HOME/.cache/codex"
STATE_DIR="$CACHE_ROOT/state"

# ---- 仅让当前 maintenance shell 立刻可用，不做持久化 ----
export PNPM_HOME="/root/.local/share/pnpm"
export PATH="$PNPM_HOME:$PATH"

export FNM_PATH="/root/.local/share/fnm"
export PATH="$FNM_PATH:$PATH"

export PATH="$HOME/.local/bin:$PATH"

if command -v fnm >/dev/null 2>&1; then
  eval "$(fnm env --shell bash)"
  if ! fnm use >/dev/null 2>&1; then
    fnm install
    fnm use
  fi
fi

# ---- 恢复 pyembed 映射：缓存恢复后会 checkout 当前分支，这一步负责重新挂回 repo 内路径 ----
PYEMBED_LINK="src-tauri/pyembed"
if [ -f "$STATE_DIR/pyembed-target" ]; then
  PYEMBED_TARGET="$(cat "$STATE_DIR/pyembed-target")"
  if [ -d "$PYEMBED_TARGET" ]; then
    rm -rf "$PYEMBED_LINK"
    ln -sfn "$PYEMBED_TARGET" "$PYEMBED_LINK"
  fi
fi

# ---- 只有 lock 变了才补 pnpm 依赖 ----
if [ -f pnpm-lock.yaml ]; then
  tmp_pnpm="$(mktemp)"
  sha256sum pnpm-lock.yaml > "$tmp_pnpm"

  if [ ! -f "$STATE_DIR/pnpm-lock.sha256" ] || ! cmp -s "$tmp_pnpm" "$STATE_DIR/pnpm-lock.sha256"; then
    pnpm install --frozen-lockfile
    mv "$tmp_pnpm" "$STATE_DIR/pnpm-lock.sha256"
  else
    rm -f "$tmp_pnpm"
  fi
fi

# ---- 只有 uv.lock 变了才补 Python 依赖 ----
if [ -f python-src/uv.lock ]; then
  tmp_uv="$(mktemp)"
  sha256sum python-src/uv.lock > "$tmp_uv"

  if [ ! -f "$STATE_DIR/uv-lock.sha256" ] || ! cmp -s "$tmp_uv" "$STATE_DIR/uv-lock.sha256"; then
    uv sync --project python-src --frozen
    mv "$tmp_uv" "$STATE_DIR/uv-lock.sha256"
  else
    rm -f "$tmp_uv"
  fi
fi