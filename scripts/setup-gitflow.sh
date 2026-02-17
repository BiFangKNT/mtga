#!/usr/bin/env bash

# 1) 可选：清掉旧 gitflow.*（相当于 reset）
set -euo pipefail

while IFS= read -r key; do
  [[ -z "${key}" ]] && continue
  git config --local --unset-all "${key}" || true
done < <(git config --local --get-regexp '^gitflow\.' 2>/dev/null | awk '{print $1}' | sort -u || true)

# 2) 重新 init（不创建分支）
git-flow init --preset=classic --defaults --main=tauri --develop=dev --no-create-branches

# 3) release finish 默认打 tag
git-flow config add topic release tauri --starting-point=dev --tag=true
