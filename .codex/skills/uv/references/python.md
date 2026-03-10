# uv python

```bash
uv python list
uv python install 3.12
uv python find 3.12
uv python pin 3.12
uv python pin --show-version
```

用途：管理解释器安装并把项目 Python 版本固定到 `.python-version`。

说明：

- `uv python pin <version>` 会写入 `.python-version`。
- `uv python pin`（不带参数）用于查看当前 pin 状态（若不存在会报错）。
- 需要严格使用 uv 管理的解释器时，可搭配 `--managed-python`。
