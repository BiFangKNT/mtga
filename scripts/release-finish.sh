#!/usr/bin/env bash

# scripts/release-finish.sh
# 用法：
#   ./scripts/release-finish.sh
#   ./scripts/release-finish.sh -v 2.0.0-beta.10
#   ./scripts/release-finish.sh -v 2.0.0-beta.10 -r origin -m tauri -d dev

set -euo pipefail

VERSION=""
REMOTE="origin"
MAIN_BRANCH="tauri"
DEV_BRANCH="dev"

fail() {
  local msg="${1:-未知错误}"
  local code="${2:-1}"
  echo "❌ ${msg}" >&2
  exit "${code}"
}

while getopts ":v:r:m:d:-:" opt; do
  case "${opt}" in
    v) VERSION="${OPTARG}" ;;
    r) REMOTE="${OPTARG}" ;;
    m) MAIN_BRANCH="${OPTARG}" ;;
    d) DEV_BRANCH="${OPTARG}" ;;
    -)
      case "${OPTARG}" in
        Version=*) VERSION="${OPTARG#*=}" ;;
        Remote=*) REMOTE="${OPTARG#*=}" ;;
        MainBranch=*) MAIN_BRANCH="${OPTARG#*=}" ;;
        DevBranch=*) DEV_BRANCH="${OPTARG#*=}" ;;
        *) fail "未知参数 --${OPTARG}" 2 ;;
      esac
      ;;
    :) fail "参数 -${OPTARG} 缺少值" 2 ;;
    \?) fail "未知参数 -${OPTARG}" 2 ;;
  esac
done
shift $((OPTIND - 1))

# 0) 确认在 git 仓库
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || fail "当前目录不是 git 仓库（git rev-parse 失败）" 2

# 1) 工作区必须干净（含 untracked）
status="$(git status --porcelain)" || fail "无法读取 git status" 3
if [[ -n "${status}" ]]; then
  echo "当前工作区不干净（git status --porcelain 有输出），请先 commit/stash/clean 后再运行：" >&2
  while IFS= read -r line; do
    [[ -n "${line}" ]] && echo "  ${line}" >&2
  done <<< "${status}"
  fail "中断：工作区不干净" 20
fi

# 2) 当前分支必须是 release/*
branch="$(git rev-parse --abbrev-ref HEAD | tr -d '\r\n')" || fail "无法获取当前分支名" 4
[[ -n "${branch}" ]] || fail "无法获取当前分支名" 4

[[ "${branch}" == release/* ]] || fail "当前分支不是 release/*（现在是 '${branch}'）。请切到 release/<版本> 分支再运行。" 10

cur_ver="${branch#release/}"
[[ -n "${cur_ver}" ]] || fail "分支名 '${branch}' 无法解析出版本号（预期形如 release/2.0.0-beta.10）" 11

# 3) Version 可选：没传则用分支名；传了必须与分支一致
if [[ -z "${VERSION}" ]]; then
  VERSION="${cur_ver}"
elif [[ "${VERSION}" != "${cur_ver}" ]]; then
  fail "你传入的 -v/-Version 是 '${VERSION}'，但当前分支是 '${branch}'（版本 '${cur_ver}'）。两者不一致，已中断。" 12
fi

# 预检查：本地/远程 tag 是否已存在（存在则中断）
# 约定：git-flow release finish <Version> 会创建 tag "v<Version>"
if [[ "${VERSION}" =~ ^[vV] ]]; then
  expected_tag="${VERSION}"
else
  expected_tag="v${VERSION}"
fi
expected_ref="refs/tags/${expected_tag}"

# 本地 tag 检查
if git show-ref --tags --verify --quiet "${expected_ref}"; then
  fail "本地已存在 tag：${expected_tag}（${expected_ref}）。请更换版本号或先删除该 tag 后再试。" 30
fi

# 远程 tag 检查（同时查轻量/附注 tag 的对象解引用）
if ! remote_hit="$(git ls-remote --tags "${REMOTE}" "${expected_ref}" "${expected_ref}^{}")"; then
  fail "无法查询远程 tag：git ls-remote --tags ${REMOTE} ...（请检查远程名/网络/权限）" 31
fi
if [[ -n "${remote_hit}" ]]; then
  fail "远程 '${REMOTE}' 已存在 tag：${expected_tag}。请更换版本号，或在远程删除该 tag 后再试。" 32
fi

echo "▶ 当前分支: ${branch}"
echo "▶ 将执行: git-flow release finish ${VERSION}"
echo "▶ 完成后推送: ${REMOTE} ${MAIN_BRANCH} ${DEV_BRANCH} + (HEAD tag if exists)"

# 4) 执行 finish
git-flow release finish "${VERSION}" || {
  code=$?
  fail "git-flow release finish 失败（exit=${code}）" "${code}"
}

# 5) 推送主分支/开发分支
git push "${REMOTE}" "${MAIN_BRANCH}" "${DEV_BRANCH}" || {
  code=$?
  fail "推送分支失败：git push ${REMOTE} ${MAIN_BRANCH} ${DEV_BRANCH}" "${code}"
}

# 6) 只推 HEAD 上的 tag
tag="$(git describe --tags --exact-match 2>/dev/null || true)"
tag="${tag//$'\r'/}"
tag="${tag//$'\n'/}"
if [[ -n "${tag}" ]]; then
  git push "${REMOTE}" "refs/tags/${tag}" || {
    code=$?
    fail "推送 tag 失败：git push ${REMOTE} refs/tags/${tag}" "${code}"
  }
  echo "✅ 已推送 tag: ${tag}"
else
  echo "ℹ️ HEAD 上没有 tag，跳过 tag push"
fi

echo "✅ 完成"
