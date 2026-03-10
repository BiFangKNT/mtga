# uv sync / uv lock

```bash
uv lock --check
uv sync --check
uv sync
uv sync --locked
uv sync --frozen
```

用途：维护 `uv.lock` 与 `.venv` 的一致性。

关键行为：

- `uv sync` 在 `.venv` 不存在时会创建环境。
- `uv sync` 默认执行精确同步，会移除多余包（可用 `--inexact` 放宽）。
- `uv lock --check` 只检查锁文件是否最新，不写入。
- `--locked`：要求锁文件保持不变，不满足即失败。
- `--frozen`：不更新锁文件直接运行/同步。
