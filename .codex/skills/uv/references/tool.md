# uv tool

```bash
uv tool run ruff --version
uvx ruff --version
uv tool run --from ruff ruff check .
uv tool install ruff
uv tool list
```

用途：运行或安装由 Python 包提供的命令行工具。

选择策略：

- 一次性执行优先 `uv tool run`（或 `uvx`）。
- 需要长期复用才用 `uv tool install`。
- 工具命令缺依赖时可加 `--with <pkg>`。
