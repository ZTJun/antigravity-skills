# 技能生命周期与检视流程

> 本仓库 `skills/` 是技能的**单一数据源**，各客户端通过符号链接接入（见 [Symlink_Maintenance.md](Symlink_Maintenance.md)）。
> 本文档记录新增 / 归档（退休）/ 删除技能的完整流程，以及如何检视仓库与链接状态。
> 路径约定：`<repo>` 表示本仓库根目录，`~` 表示用户主目录。

---

## 新增技能

### 来自上游仓库（推荐）

1. **拷贝 payload**：浅克隆上游，把技能目录复制为 `<repo>/skills/<name>/`。`name` 必须与 SKILL.md 的 `name` 字段一致（spec/Specification.md）。
   ```bash
   git clone --depth 1 <repo_url> /tmp/x
   rsync -a --exclude '.DS_Store' /tmp/x/<path-to-payload>/ <repo>/skills/<name>/
   ```
2. **登记来源**：在 `skills_sources.json` 追加条目，之后 `bash scripts/sync_skills.sh <name>`（或 `oah sync <name>`）可拉取更新：
   ```json
   {
     "name": "<name>",
     "repo_url": "https://github.com/<org>/<repo>.git",
     "branch": "main",
     "copy_rules": [{ "source": "<payload-path>", "dest": "skills/<name>", "exclude": [".DS_Store"] }]
   }
   ```
   - `source` 相对上游仓库根；单技能仓库用 `"."`。
   - `exclude` 常见项：`.git`、`.github`、`.gitignore`、`.DS_Store`。
3. **重建索引**：`python3 scripts/update_skills_index.py`（扫描 `skills/` 生成 `skills_index.json`；支持 YAML 块标量 description）。
4. **更新 README**：技能计数、分类表数量、上游源表。
5. **补链**：`ln -s <repo>/skills/<name> ~/.agents/skills/<name>`（其他目标目录见符号链接文档）。
6. **验证**：name 与目录名一致、无 `.DS_Store`/本地路径泄漏、SKILL.md frontmatter 完整。

### 本地原创

用 `template/` 目录起步，格式遵循 `spec/Specification.md`，然后走上面 3–6 步（无需登记 sources）。

## 归档（退休）技能

不删除、移入 `archived/skills/`——不建链接、不进索引，可随时复活：

```bash
cd <repo>
git mv skills/<name> archived/skills/<name>
```

配套动作：

1. **摘除 sources**：若来自上游，从 `skills_sources.json` 对应 `include` 列表移除（或删整个条目）——否则下次 sync 会拉回。
2. **摘除链接**：把 `~/.agents/skills/<name>` 等目录中的符号链接 `mv` 到 `~/.trash/`（不要 `rm`）。
3. 重建索引 + 更新 README（计数、分类、归档清单）。

> 注意：sync 是 `rsync -a` **不带 `--delete`**，上游删除不会自动清本地，但摘了 include 后技能只会停在原地，需要时手动归档。

## 删除技能

优先归档。确需删除：`mv` 到 `~/.trash/`（勿直接 `rm`），然后摘 sources、重建索引、清链接、更新 README。

## 检视仓库与链接

```bash
# 活跃技能数（应与 index、README 计数一致）
ls <repo>/skills | wc -l
python3 -c "import json; print(len(json.load(open('<repo>/skills_index.json'))))"

# 死链扫描（所有链接目标）
for d in ~/.agents/skills ~/.claude/skills ~/.config/opencode/skills ~/.zcode/skills; do
  find "$d" -maxdepth 1 -type l ! -exec test -e {} \; -print 2>/dev/null
done

# 全量补链（幂等，可重复跑）
for d in <repo>/skills/*/; do
  name=$(basename "$d"); ln -sfn "$(cd "$d" && pwd)" ~/.agents/skills/"$name"
done
```

死链 `mv` 到 `~/.trash/`。`archived/skills/` 下不链接任何客户端。

## 常见坑

- **目录名 ≠ name 字段**：skill 不会被识别。
- **Finder 副本污染**：手动复制目录会产生 `xxx 2.md` / `xxx 2/` 副本，提交前 `find skills -name '* 2*'` 清一遍。
- **重复触发**：同功能 skill 并存会争夺触发（如新旧两套 office skill），保留一套、其余归档。
- **JIT 依赖**：skill 首次调用可能跑 setup（下载运行时/字体），装 skill 时注意其 setup 脚本行为。

## 已知初始化问题（2026-11-10 验证）

- **pdfkit-py `setup.sh`**：`_find_python` 取 PATH 第一个 `python3`——若解析到 uv 托管的 Python（`~/.local/bin/python3`），`venv` 会因缺 ensurepip 失败。修复：`PATH="/opt/homebrew/bin:$PATH" bash scripts/setup.sh`。homebrew Python 3.15 可正常建 venv。
- **minimax-docx 验证测试**：CLI 目标框架 net8.0，仅装 .NET 10 时 `dotnet run` 报框架缺失。修复：`DOTNET_ROLL_FORWARD=LatestMajor`（或装 .NET 8 运行时）。已验证 `create` 可正常产 docx。
- **minimax-xlsx**：无独立运行时，`uv run --with pandas --with openpyxl` 即可。
- **pptx-generator**：需 `pptxgenjs`（npm 全局）+ `markitdown`（`uv run --with markitdown`）。
- **minimax-docx `triggers` 字段**：上游 SKILL.md 把 `triggers` 误用为关键词列表，但 Devin 只认 `user`/`model` 枚举——非法值导致技能完全不可见。本地已删除该字段；**上游 sync 会回灌**，若技能消失请重新移除（或推动上游修复）。
