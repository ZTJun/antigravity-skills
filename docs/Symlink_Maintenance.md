# 符号链接维护文档

> 本仓库 `skills/` 是技能的**单一数据源**。各 AI 编码客户端不复制技能文件，而是通过**符号链接**接入——改一处，处处生效。
> 本文档记录 `skills/` 当前链接到了哪些位置、各自的同步方式与注意事项。
> 路径统一用 `~` 表示用户主目录；`<repo>` 表示本仓库根目录。

## 链接目标一览

| 目标目录 | 客户端 | 数量 | 同步方式 | 说明 |
|---|---|---|---|---|
| `~/.claude/skills` | Claude Code（Devin/Windsurf 亦兼容读取） | 77 | 手动 / `oah enable -g -t claude` | 未链 `anysearch-skill`（见下文）；`claude-api` 为独立实体目录，不在本仓库 |
| `~/.agents/skills` | 通用目录（配套 AGENTS.md 约定） | 78 | 手动脚本（见下） | 全量链接 |
| `~/.config/opencode/skills` | opencode 全局 | 78 | 手动脚本 / `oah enable -g -t opencode` | oah target 约定即 `~/.config/opencode` |
| `~/.zcode/skills` | zcode | 73 | `zsh ~/.zcode/skills-sync.sh` | 有 SKIP 列表（见下） |
| `~/.gemini/config/plugins/customs/skills` | Gemini 自定义插件 | 35 | 手动 | **旧快照，未全量同步**，需要时可按通用脚本补齐 |

## 各目标的同步方法

### 通用脚本（~/.agents、opencode，或任意目录）

```bash
REPO=<repo>/skills
DEST=~/.agents/skills          # 或 ~/.config/opencode/skills
mkdir -p "$DEST"
for d in "$REPO"/*/; do
  name=$(basename "$d")
  ln -sfn "${d%/}" "$DEST/$name"
done
```

### zcode

```bash
zsh ~/.zcode/skills-sync.sh
```

- SKIP 列表：`docx pdf pptx xlsx skill-creator`——与 ZCode 官方插件同名，链接会覆盖插件版，刻意跳过回落到插件版。
- 新增技能后重跑脚本即可；**该脚本只增不删**，删除技能需手动清死链（见下）。

### ~/.claude/skills

- `anysearch-skill` **刻意不链接**：已改走 AnySearch 官方 MCP（Devin 用户级配置于 `~/.config/devin/mcp_config.json`，端点 `https://api.anysearch.com/mcp`，含 API key header）。其他客户端没有配 MCP，如需保留 skill 可自行补链。
- `claude-api` 是独立实体目录（非链接），独立于本仓库维护。

## 死链清理

`scripts/sync_skills.sh` 用 `rsync -a` **不带 `--delete`**——上游删除的技能不会自动消失，留下死链需要手动清：

```bash
# 列出死链
for d in ~/.claude/skills ~/.agents/skills ~/.config/opencode/skills ~/.zcode/skills ~/.gemini/config/plugins/customs/skills; do
  find "$d" -maxdepth 1 -type l ! -exec test -e {} \; -print 2>/dev/null
done

# 移入回收目录（不要直接 rm）
mv <死链路径> ~/.trash/
```

## 维护备忘

- 上游删除过的技能（本仓库已移除）：`baoyu-imagine`（被 `baoyu-image-gen` 取代）、`archived/skills/baoyu-image-cards`。2026-10-21 清理的一批历史孤儿文件在 `~/.trash/orphans-2026-10-21/` 有留底。
- `archived/skills/` 下的技能**不链接**到任何客户端。
- `~/.gemini/config/plugins/customs/skills` 目前是 35 个链接的旧快照；其中曾出现的 `anysearch-skill-main`、`bdi-mental-states` 死链已于 2026-10-21 清理。
- 仓库内 `.claude-plugin/`、`.codex-plugin/`、`.gemini/`、`agents/`、`commands/` 是分发用清单/插件定义，不是运行态链接，不在本文档范围。
