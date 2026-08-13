# Archived 归档目录

本目录存放已归档的内容：低频使用但保留上游同步的技能、废弃包、历史文档。

## 归档清单

### skills/（13 个低频技能，保留上游同步）

| 类别 | 技能 |
|---|---|
| 发布类 | baoyu-post-to-wechat / baoyu-post-to-weibo / baoyu-post-to-x |
| 漫画配图 | baoyu-comic / baoyu-article-illustrator |
| 封面卡片 | baoyu-cover-image / baoyu-image-cards / baoyu-xhs-images |
| 图片压缩 | baoyu-compress-image |
| 心智建模 | bdi-mental-states |
| Obsidian | obsidian-cli / obsidian-markdown / obsidian-bases |

这些技能仍随 `skills_sources.json` 配置同步到 `archived/skills/`（`git pull` 或手动 `oah sync` 可更新），`~/.claude/skills` 符号链接保持可用。

### docs/backup/（旧版手册，2026-08-14 归档）

- Antigravity_Skills_Manual.en.md / Antigravity_Skills_Manual.zh-CN.md（约 960 行 × 2）
- 归档原因：已被 `docs/` 下新的 Skill/Agent/Command Guidelines 取代

### 顶层文档（2026-08-14 归档）

- CHANGELOG.md — 原仓库版本历史（本仓库修改已总结于根 README）
- CONTRIBUTING.md — 社区贡献指南（fork 仓库无需）
- CLAUDE.md / GEMINI.md — Claude / Gemini 编码行为规范（本机使用 OpenCode，读取 AGENTS.md 即可）

### science_skills_common（2026-08-14 归档）

- **来源仓库**：[google-deepmind/science-skills](https://github.com/google-deepmind/science-skills)
- **归档原因**：上游在后续版本中已删除该共享包，所有技能脚本的 HTTP 客户端已迁移到独立的 PyPI 包 [`polite-http`](https://pypi.org/project/polite-http/)（v0.1.0）。
- **替代方案**：新版脚本通过 PEP 723 内联依赖声明（脚本头部 `# /// script` 块），由 `uv run` 运行时自动从 PyPI 安装 `polite-http`，无需在本地维护共享目录。

#### 两者对比

| | science_skills_common（旧） | polite-http（新） |
|---|---|---|
| 形态 | 仓库内共享目录，本地路径依赖安装 | 独立 PyPI 包 |
| 安装方式 | `pyproject.toml` 中 `path = "../../science_skills_common"` | 脚本内联声明依赖，`uv run` 自动拉取 |
| 功能 | 限速（跨进程文件锁）、429/5xx 重试、指数退避 + jitter、Retry-After | 同左，另支持网络错误重试 |
| 额外特性 | X-Throttling-Control 主动背压（PubChem / NCBI 专用） | 更通用，无专有特性 |

#### 受影响技能（均已更新为上游最新版）

- literature_search_arxiv
- literature_search_europepmc
- literature_search_openalex
- pymol
- quickgo_database
- uv
- workflow_skill_creator

#### 归档操作记录

- `skills/science_skills_common/` → `archived/science_skills_common/`
- 删除 `~/.claude/skills/science_skills_common` 符号链接（原指向已移动目录，避免断链）
