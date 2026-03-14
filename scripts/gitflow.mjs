import { spawnSync } from "node:child_process";

const RELEASE_PREFIX = "release/";

function fail(message, code = 1) {
  console.error(`❌ ${message}`);
  process.exit(code);
}

function run(command, args, { capture = false, check = true } = {}) {
  const result = spawnSync(command, args, {
    shell: false,
    encoding: "utf8",
    stdio: capture ? ["ignore", "pipe", "pipe"] : "inherit",
  });

  if (result.error) {
    fail(`执行失败: ${command} ${args.join(" ")} (${result.error.message})`);
  }
  if (check && (result.status ?? 1) !== 0) {
    fail(`命令执行失败: ${command} ${args.join(" ")}`, result.status ?? 1);
  }
  return result;
}

function trimOutput(value) {
  return (value ?? "").replaceAll("\r", "").trim();
}

function assertGitRepo() {
  const result = run("git", ["rev-parse", "--is-inside-work-tree"], {
    capture: true,
    check: false,
  });
  if ((result.status ?? 1) !== 0) {
    fail("当前目录不是 git 仓库（git rev-parse 失败）", 2);
  }
}

function setupGitflow() {
  assertGitRepo();

  const keysResult = run("git", ["config", "--local", "--get-regexp", "^gitflow\\."], {
    capture: true,
    check: false,
  });

  if ((keysResult.status ?? 1) === 0) {
    const keys = Array.from(
      new Set(
        trimOutput(keysResult.stdout)
          .split("\n")
          .map((line) => line.trim())
          .filter(Boolean)
          .map((line) => line.split(/\s+/, 1)[0]),
      ),
    );
    for (const key of keys) {
      run("git", ["config", "--local", "--unset-all", key], { check: false });
    }
  }

  run("git-flow", [
    "init",
    "--preset=classic",
    "--defaults",
    "--main=tauri",
    "--develop=dev",
    "--no-create-branches",
  ]);

  run("git-flow", [
    "config",
    "add",
    "topic",
    "release",
    "tauri",
    "--starting-point=dev",
    "--tag=true",
  ]);

  console.log("✅ git-flow 配置完成");
}

function parseFinishArgs(argv) {
  const options = {
    version: "",
    remote: "origin",
    mainBranch: "tauri",
    devBranch: "dev",
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "-h" || arg === "--help") {
      printUsage();
      process.exit(0);
    }
    const next = argv[i + 1];
    if (arg === "-v" || arg === "--version" || arg === "--Version") {
      if (!next) fail(`参数 ${arg} 缺少值`, 2);
      options.version = next;
      i += 1;
      continue;
    }
    if (arg.startsWith("--version=") || arg.startsWith("--Version=")) {
      options.version = arg.split("=", 2)[1] ?? "";
      continue;
    }
    if (arg === "-r" || arg === "--remote" || arg === "--Remote") {
      if (!next) fail(`参数 ${arg} 缺少值`, 2);
      options.remote = next;
      i += 1;
      continue;
    }
    if (arg.startsWith("--remote=") || arg.startsWith("--Remote=")) {
      options.remote = arg.split("=", 2)[1] ?? "";
      continue;
    }
    if (arg === "-m" || arg === "--main-branch" || arg === "--MainBranch") {
      if (!next) fail(`参数 ${arg} 缺少值`, 2);
      options.mainBranch = next;
      i += 1;
      continue;
    }
    if (arg.startsWith("--main-branch=") || arg.startsWith("--MainBranch=")) {
      options.mainBranch = arg.split("=", 2)[1] ?? "";
      continue;
    }
    if (arg === "-d" || arg === "--dev-branch" || arg === "--DevBranch") {
      if (!next) fail(`参数 ${arg} 缺少值`, 2);
      options.devBranch = next;
      i += 1;
      continue;
    }
    if (arg.startsWith("--dev-branch=") || arg.startsWith("--DevBranch=")) {
      options.devBranch = arg.split("=", 2)[1] ?? "";
      continue;
    }
    fail(`未知参数 ${arg}`, 2);
  }

  return options;
}

function finishRelease(argv) {
  assertGitRepo();
  const options = parseFinishArgs(argv);

  const statusResult = run("git", ["status", "--porcelain"], { capture: true, check: false });
  if ((statusResult.status ?? 1) !== 0) {
    fail("无法读取 git status", 3);
  }
  const dirty = trimOutput(statusResult.stdout);
  if (dirty) {
    console.error(
      "当前工作区不干净（git status --porcelain 有输出），请先 commit/stash/clean 后再运行：",
    );
    for (const line of dirty.split("\n")) {
      if (line.trim()) console.error(`  ${line}`);
    }
    fail("中断：工作区不干净", 20);
  }

  const branchResult = run("git", ["rev-parse", "--abbrev-ref", "HEAD"], {
    capture: true,
    check: false,
  });
  const branch = trimOutput(branchResult.stdout);
  if ((branchResult.status ?? 1) !== 0 || !branch) {
    fail("无法获取当前分支名", 4);
  }
  if (!branch.startsWith(RELEASE_PREFIX)) {
    fail(`当前分支不是 release/*（现在是 '${branch}'）。请切到 release/<版本> 分支再运行。`, 10);
  }

  const currentVersion = branch.slice(RELEASE_PREFIX.length);
  if (!currentVersion) {
    fail(`分支名 '${branch}' 无法解析出版本号（预期形如 release/2.0.0-beta.10）`, 11);
  }

  const version = options.version || currentVersion;
  if (options.version && options.version !== currentVersion) {
    fail(
      `你传入的 -v/-Version 是 '${options.version}'，但当前分支是 '${branch}'（版本 '${currentVersion}'）。两者不一致，已中断。`,
      12,
    );
  }

  const expectedTag = /^[vV]/.test(version) ? version : `v${version}`;
  const expectedRef = `refs/tags/${expectedTag}`;

  const localTagResult = run("git", ["show-ref", "--tags", "--verify", "--quiet", expectedRef], {
    check: false,
  });
  const localTagStatus = localTagResult.status ?? 1;
  if (localTagStatus === 0) {
    fail(
      `本地已存在 tag：${expectedTag}（${expectedRef}）。请更换版本号或先删除该 tag 后再试。`,
      30,
    );
  }
  if (localTagStatus !== 1) {
    fail(`本地 tag 检查失败：git show-ref --tags --verify --quiet ${expectedRef}`, 30);
  }

  const remoteTagResult = run(
    "git",
    ["ls-remote", "--tags", options.remote, expectedRef, `${expectedRef}^{}`],
    { capture: true, check: false },
  );
  if ((remoteTagResult.status ?? 1) !== 0) {
    fail(
      `无法查询远程 tag：git ls-remote --tags ${options.remote} ...（请检查远程名/网络/权限）`,
      31,
    );
  }
  if (trimOutput(remoteTagResult.stdout)) {
    fail(
      `远程 '${options.remote}' 已存在 tag：${expectedTag}。请更换版本号，或在远程删除该 tag 后再试。`,
      32,
    );
  }

  console.log(`▶ 当前分支: ${branch}`);
  console.log(`▶ 将执行: git-flow release finish ${version}`);
  console.log(
    `▶ 完成后推送: ${options.remote} ${options.mainBranch} ${options.devBranch} + (HEAD tag if exists)`,
  );

  const finishResult = run("git-flow", ["release", "finish", version], { check: false });
  if ((finishResult.status ?? 1) !== 0) {
    const code = finishResult.status ?? 1;
    fail(`git-flow release finish 失败（exit=${code}）`, code);
  }

  const pushBranchesResult = run(
    "git",
    ["push", options.remote, options.mainBranch, options.devBranch],
    { check: false },
  );
  if ((pushBranchesResult.status ?? 1) !== 0) {
    const code = pushBranchesResult.status ?? 1;
    fail(
      `推送分支失败：git push ${options.remote} ${options.mainBranch} ${options.devBranch}`,
      code,
    );
  }

  const tagResult = run("git", ["describe", "--tags", "--exact-match"], {
    capture: true,
    check: false,
  });
  const headTag = trimOutput(tagResult.stdout);
  if (headTag) {
    const pushTagResult = run("git", ["push", options.remote, `refs/tags/${headTag}`], {
      check: false,
    });
    if ((pushTagResult.status ?? 1) !== 0) {
      const code = pushTagResult.status ?? 1;
      fail(`推送 tag 失败：git push ${options.remote} refs/tags/${headTag}`, code);
    }
    console.log(`✅ 已推送 tag: ${headTag}`);
  } else {
    console.log("ℹ️ HEAD 上没有 tag，跳过 tag push");
  }

  const checkoutDevResult = run("git", ["checkout", options.devBranch], { check: false });
  if ((checkoutDevResult.status ?? 1) !== 0) {
    const code = checkoutDevResult.status ?? 1;
    fail(`切回开发分支失败：git checkout ${options.devBranch}`, code);
  }
  console.log(`✅ 已切回分支: ${options.devBranch}`);

  console.log("✅ 完成");
}

function syncBranches() {
  assertGitRepo();

  const statusResult = run("git", ["status", "--porcelain"], { capture: true, check: false });
  if ((statusResult.status ?? 1) !== 0) {
    fail("无法读取 git status", 3);
  }
  const dirty = trimOutput(statusResult.stdout);
  if (dirty) {
    console.error(
      "当前工作区不干净（git status --porcelain 有输出），请先 commit/stash/clean 后再运行：",
    );
    for (const line of dirty.split("\n")) {
      if (line.trim()) console.error(`  ${line}`);
    }
    fail("中断：工作区不干净", 20);
  }

  const branches = ["dev", "tauri"];
  for (const branch of branches) {
    const checkoutResult = run("git", ["checkout", branch], { check: false });
    if ((checkoutResult.status ?? 1) !== 0) {
      const code = checkoutResult.status ?? 1;
      fail(`切换分支失败：git checkout ${branch}`, code);
    }
    console.log(`▶ 已切换分支: ${branch}`);

    const pullResult = run("git", ["pull"], { check: false });
    if ((pullResult.status ?? 1) !== 0) {
      const code = pullResult.status ?? 1;
      fail(`拉取分支失败：git pull (${branch})`, code);
    }
    console.log(`✅ 已拉取分支: ${branch}`);
  }

  const checkoutDevResult = run("git", ["checkout", "dev"], { check: false });
  if ((checkoutDevResult.status ?? 1) !== 0) {
    const code = checkoutDevResult.status ?? 1;
    fail("切回开发分支失败：git checkout dev", code);
  }
  console.log("✅ 已切回分支: dev");
}

function printUsage() {
  console.log("用法:");
  console.log("  node ./scripts/gitflow.mjs setup");
  console.log("  node ./scripts/gitflow.mjs finish [-v version] [-r remote] [-m main] [-d dev]");
  console.log("  node ./scripts/gitflow.mjs sync");
}

const [command, ...args] = process.argv.slice(2);

if (!command || command === "-h" || command === "--help") {
  printUsage();
  process.exit(0);
}

if (command === "setup") {
  setupGitflow();
  process.exit(0);
}

if (command === "finish") {
  finishRelease(args);
  process.exit(0);
}

if (command === "sync") {
  syncBranches();
  process.exit(0);
}

fail(`未知子命令 ${command}`, 2);
