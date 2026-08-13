# open-agent-hub（antigravity-skills）

> 本仓库为 **ZTJun/antigravity-skills**（fork 自 [guanyang/open-agent-hub](https://github.com/guanyang/antigravity-skills)），在原仓库基础上做了个性化精简与归档整理。

一个轻量、零依赖的 AI 编码助手能力管理仓库。通过一个命令，即可将**技能 (Skills)**、**专家角色 (Agents)** 与**快捷指令 (Commands)** 链接到你的项目工作区或全局配置目录（支持 Claude Code、Antigravity、Cursor、Codex 等）。

---

## 📂 目录结构

```
.
├── skills/             # ★ 模块化技能库（78 个活跃技能）
├── archived/           # ★ 归档区（仍保留上游同步）
│   ├── skills/         #   13 个低频技能（发布/漫画/封面/Obsidian 等）
│   ├── docs/           #   旧版手册备份（中英双版）
│   ├── CHANGELOG.md    #   原仓库版本历史
│   ├── CONTRIBUTING.md #   贡献指南
│   ├── CLAUDE.md       #   Claude 行为规范（本机使用 OpenCode）
│   ├── GEMINI.md       #   Gemini 行为规范（本机使用 OpenCode）
│   └── science_skills_common/  # 已废弃共享包（上游已迁移至 polite-http）
├── agents/             # 专家 Agent 系统提示词 (agent-*.md)
├── commands/           # Slash Commands (*.md)
├── docs/               # 技术指南（Skill / Agent / Command Guidelines）
├── scripts/            # CLI 管理脚本 (hub.js) + 上游同步 (sync_skills.sh)
├── spec/               # 技能格式规范 (Specification.md)
├── template/           # 新技能开发模板
├── .githooks/          # post-merge：pull 后自动同步上游技能
├── AGENTS.md           # LLM 编码行为规范（项目级，OpenCode 读取）
├── SECURITY.md         # 安全策略
├── LICENSE             # MIT 开源协议
├── package.json        # CLI 配置与 npm 注册
├── skills_index.json   # 技能元数据全局索引
├── skills_sources.json # 上游技能数据源配置（12 个源）
└── README.md           # 中文主文档（本文件）
```

---

## 🔧 本仓库的个性化修改

以下为 fork 后相对原仓库的改动：

### 归档整理（archived/）
- **低频技能归档**（13 个，仍随上游同步到 `archived/skills/`）：`baoyu-post-to-wechat/-weibo/-x`（发布类）、`baoyu-comic`、`baoyu-article-illustrator`（漫画配图）、`baoyu-cover-image`、`baoyu-image-cards`、`baoyu-xhs-images`（封面卡片）、`baoyu-compress-image`、`bdi-mental-states`、`obsidian-cli/-markdown/-bases`
- **文档归档**：旧版双语文档、CHANGELOG、CONTRIBUTING、CLAUDE.md、GEMINI.md、废弃共享包 `science_skills_common`（本机使用 OpenCode，读取 AGENTS.md 即可）
- `claude-api` 已移出仓库，独立存放于 `~/.claude/skills/claude-api`（不再随本仓库同步）

### 技能精简
- **remotion 细分技能**（12 个）已迁出至独立工作区 `~/Documents/Projects/remotion/`，本仓库仅保留 `remotion` 主技能
- **science-skills 精简集**：仅保留 `literature_search_arxiv`、`literature_search_openalex`、`uv`、`pymol`、`workflow_skill_creator`（完整 38 技能见 `~/Documents/Projects/biomedic-search/`）
- **新增上游追踪**：`OfficeCli`（iOfficeAI/OfficeCLI）、`anysearch-skill`（anysearch-ai/anysearch-skill）、`science-skills`（google-deepmind/science-skills）
- **上游来源修正**：`advanced-evaluation`、`context-*`、`memory-systems` 等实际来自 context-engineering 源（原误归 superpowers）

### 自动同步
- `.githooks/post-merge`：`git pull` 后自动同步 **officecli / science-skills / anysearch** 三个源，有变更自动提交

---

## 🧩 技能分类速览（78 个活跃技能）

| 类别 | 数量 | 示例 |
|---|---|---|
| 文档办公 | 5 | docx / pptx / xlsx / pdf / OfficeCli |
| 设计创作 | 8 | canvas-design / theme-factory / ui-ux-pro-max |
| Agent 流程（superpowers） | 14 | brainstorming / TDD / debugging |
| 上下文工程（context-engineering） | 16 | context-* / evaluation / memory-systems |
| 内容创作（baoyu） | 14 | translate / image-gen / diagram / wechat-summary |
| 科学文献（science-skills） | 5 | literature_search_arxiv / openalex / uv / pymol / workflow_skill_creator |
| 其他 | 16 | anysearch / notebooklm / react-* / supabase / defuddle / json-canvas / remotion |

---

## 🚀 快速开始

### 方式一：`skills` CLI（仅技能）

```bash
npx skills@latest add ZTJun/antigravity-skills
```

### 方式二：克隆并使用内置 `oah` CLI（技能 + Agents + Commands）

```bash
git clone https://github.com/ZTJun/antigravity-skills.git ~/antigravity-skills
cd ~/antigravity-skills && npm link
```

常用命令：

```bash
oah list                          # 列出所有 Skills / Agents / Commands
oah status                        # 查看当前项目链接状态
oah enable <skill-name>           # 启用指定技能（链接到 .claude/）
oah enable                        # 启用全部（默认）
oah enable --target=all           # 启用全部目标环境
oah enable --global               # 全局启用
oah disable                       # 禁用全部
```

CLI 选项：`-p/--project`（项目级，默认）、`-g/--global`（全局）、`-t/--target <name>`（目标环境：claude/antigravity/gemini/codex/cursor/trae/opencode/kiro）、`--path <dir>`（自定义目录）、`--skills/--agents/--commands`（按类型过滤）

---

## 🔄 上游同步

技能库来自多个开源社区，可随时拉取上游更新：

```bash
# 同步所有配置的源
oah sync

# 同步指定源
oah sync science-skills

# 或直接调用脚本
bash scripts/sync_skills.sh <source-name>
```

已配置的上游源（`skills_sources.json`）：

| 源 | 上游仓库 | 同步目标 |
|---|---|---|
| anthropics-skills | anthropics/skills | skills/（16 个） |
| superpowers | obra/superpowers | skills/（14 个） |
| context-engineering | muratcankoylan/Agent-Skills-for-Context-Engineering | skills/（16 个）+ archived（1） |
| baoyu-skills | JimLiu/baoyu-skills | skills/（14 个）+ archived/skills（9 个） |
| obsidian-skills | kepano/obsidian-skills | skills/（2 个）+ archived/skills（3 个） |
| science-skills | google-deepmind/science-skills | skills/（5 个） |
| officecli | iOfficeAI/OfficeCLI | skills/OfficeCli |
| anysearch | anysearch-ai/anysearch-skill | skills/anysearch-skill |
| notebooklm / planning-with-files / vercel-labs / supabase / remotion | 各自上游 | skills/ |

---

## 🛡️ 安全

漏洞报告请参见 [SECURITY.md](SECURITY.md)。

## 📄 许可证

本项目基于 [MIT License](LICENSE)。归档技能与文档保留各自上游许可证。
