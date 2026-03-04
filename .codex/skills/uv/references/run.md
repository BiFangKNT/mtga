# uv run

```bash
uv run python -c "print('ok')"
uv run -m pytest -q
uv run --with httpx==0.26.0 python -c "import httpx; print(httpx.__version__)"
uv run --no-project script.py
uv run --python 3.12 -- python
```

用途：在项目环境或指定环境中运行命令/脚本，并支持临时依赖。

关键规则：

- 所有 `uv` 选项写在命令前。
- 需要可读性时用 `--` 分隔 `uv` 参数和目标命令。
- 项目自动发现不符合预期时，显式加 `--no-project`。
- 需要锁文件不被改动时用 `--locked`；需要跳过锁文件更新检查时用 `--frozen`。
