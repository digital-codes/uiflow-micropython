# AGENTS.md

本目录只负责维护 `uiflow2-coder` skill：生成/同步 skill 的 `docs`、`SKILL.md` 内嵌索引和辅助描述文件。

## 目标

- 源头：`D:\git\uiflow_micropython\docs\source` 和 `D:\git\uiflow_micropython\m5stack\libs`。
- 本地 skill 副本：`D:\git\uiflow_micropython\tools\knowledge-base\uiflow2-coder`。
- 实际生效 skill：`C:\Users\15515\.agents\skills\uiflow2-coder`。
- 不再保留独立的 `tools\knowledge-base\uiflow2-docs` 中间产物；脚本用临时目录生成后直接同步到 skill。

## 标准更新流程

在仓库根目录运行：

```powershell
python tools\knowledge-base\sync_uiflow2_skill.py
```

`sync_uiflow2_skill.py` 会：

1. 先把系统里的 `uiflow2-coder` skill 复制到本目录的 `uiflow2-coder` 副本。
2. 在临时目录中从 `docs\source` 生成最新 Markdown。
3. 批量同步到系统 skill 和本地副本的 `docs` 目录。
4. 生成 skill 根目录的紧凑 `file_tree.txt`。
5. 刷新 `SKILL.md` 内的 `BEGIN_DOC_TREE` / `END_DOC_TREE` 紧凑索引。

如需使用已有生成目录，可显式指定：

```powershell
python tools\knowledge-base\sync_uiflow2_skill.py --source-docs C:\path\to\docs
```

## 维护规则

- 不要手动编辑 skill 的 `docs` 目录；要改内容，优先改 `docs\source` 或转换脚本。
- `index.rst` 会转换为 `_overview.md`；skill 使用时要求先读 `_overview.md`，再读具体 API 文档。
- `SKILL.md` 内嵌索引统一省略 `.md` 后缀，例如 `unit/env` 表示 `docs/unit/env.md`。
- `file_tree.txt` 保留在 skill 根目录，只作为外部工具、人工 diff 和脚本验证的冗余索引。
- 缺失 class 的注释必须使用仓库相对路径，不要写入 `D:\...` 或 `/tmp/...` 这类本机绝对路径。
- 生成的 Markdown 要去掉尾随空白、多余 EOF 空行，并保持 UTF-8。

## 验证清单

```powershell
python -m py_compile tools\knowledge-base\rst2md_en.py tools\knowledge-base\generate_tree.py tools\knowledge-base\sync_uiflow2_skill.py
git diff --check -- tools\knowledge-base
python -X utf8 C:\Users\15515\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\Users\15515\.agents\skills\uiflow2-coder
python -X utf8 C:\Users\15515\.codex\skills\.system\skill-creator\scripts\quick_validate.py tools\knowledge-base\uiflow2-coder
```

还要用 Python 检查：

- 所有 `.md` 可用 `encoding="utf-8"` 解码。
- 没有 `U+FFFD` replacement character。
- skill 文档中没有本机绝对路径残留。
- 系统 skill 和本地副本内容一致。

## Windows 编码注意

- 写中文文件优先用 `apply_patch` 或明确 UTF-8 的 Python 脚本。
- 不要用 PowerShell here-string/stdin 管道写大段中文到文件。
- 写完中文文件后用 Python 读取原始字节，确认 UTF-8 可解码且没有异常 `?` 或 `U+FFFD`。
