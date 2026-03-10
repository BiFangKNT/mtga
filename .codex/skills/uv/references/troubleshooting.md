# Troubleshooting

## 常见错误与修复

`ModuleNotFoundError: No module named 'yaml'`

```bash
uv run --with pyyaml path/to/script.py
```

`--locked` 失败（锁文件过期）

```bash
uv lock
uv sync
```

目录中没有项目却执行了项目命令

```bash
uv run --no-project script.py
```

Windows 上 Python 读取文件报编码错误（如 `gbk` 解码失败）

```powershell
$env:PYTHONUTF8='1'
uv run --with pyyaml path\to\script.py
```

## 诊断顺序

1. 先看版本与帮助：`uv --version`、`uv <subcommand> --help`。
2. 再看锁与环境：`uv lock --check`、`uv sync --check`。
3. 最后执行变更命令，并记录实际改动文件。
