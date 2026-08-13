# Archived 归档目录

本目录存放已被上游废弃、不再使用的技能副本，仅作历史存档。

## 归档清单

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
