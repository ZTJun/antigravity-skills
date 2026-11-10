# open-agent-hub（antigravity-skills）

> 本仓库为 **ZTJun/antigravity-skills**（fork 自 [guanyang/open-agent-hub](https://github.com/guanyang/antigravity-skills)），在原仓库基础上做了个性化精简与归档整理。

一个轻量、零依赖的 AI 编码助手能力管理仓库。通过一个命令，即可将**技能 (Skills)**、**专家角色 (Agents)** 与**快捷指令 (Commands)** 链接到你的项目工作区或全局配置目录（支持 Claude Code、Antigravity、Cursor、Codex 等）。

---

## 📂 目录结构

```
.
├── skills/             # ★ 模块化技能库（79 个活跃技能）
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
├── AGENTS.md           # LLM 编码行为规范（仅本地使用，不同步远程）
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
- **低频技能归档**（17 个，仍随上游同步到 `archived/skills/`）：`baoyu-post-to-wechat/-weibo/-x`（发布类）、`baoyu-comic`、`baoyu-article-illustrator`（漫画配图）、`baoyu-cover-image`、`baoyu-image-cards`、`baoyu-xhs-images`（封面卡片）、`baoyu-compress-image`、`bdi-mental-states`、`obsidian-cli/-markdown/-bases`、`docx`/`pptx`/`xlsx`/`pdf`（anthropic 办公四件套，已由 minimax-*/pdfkit-py 平替，不再同步）
- **文档归档**：旧版双语文档、CHANGELOG、CONTRIBUTING、CLAUDE.md、GEMINI.md
- `claude-api` 已移出仓库，独立存放，不再随本仓库同步

### 技能精简
- **remotion 细分技能**（12 个）已迁出至独立工作区，本仓库仅保留 `remotion` 主技能
- **science-skills 精简集**：仅保留 `literature_search_arxiv`、`literature_search_openalex`、`uv`、`pymol`、`workflow_skill_creator`
- **新增上游追踪**：`OfficeCli`（iOfficeAI/OfficeCLI）、`anysearch-skill`（anysearch-ai/anysearch-skill）、`science-skills`（google-deepmind/science-skills）
- **上游来源修正**：`advanced-evaluation`、`context-*`、`memory-systems` 等实际来自 context-engineering 源

### 自动同步
- `.githooks/post-merge`：`git pull` 后自动同步 **officecli / science-skills / anysearch** 三个源，有变更自动提交

---

## 🧩 技能分类速览（79 个活跃技能）

| 类别 | 数量 | 示例 |
|---|---|---|
| 文档办公 | 5 | OfficeCli / minimax-docx / minimax-xlsx / pptx-generator / pdfkit-py |
| 设计创作 | 8 | canvas-design / theme-factory / ui-ux-pro-max |
| Agent 流程（superpowers） | 14 | brainstorming / TDD / debugging |
| 上下文工程（context-engineering） | 16 | context-* / evaluation / memory-systems |
| 内容创作（baoyu） | 14 | translate / image-gen / diagram / wechat-summary |
| 科学文献（science-skills） | 5 | literature_search_arxiv / openalex / uv / pymol / workflow_skill_creator |
| 其他 | 17 | anysearch / notebooklm / react-* / supabase / defuddle / json-canvas / remotion / lieflat-less-ai-tone |

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
| minimax-docx / minimax-xlsx / pptx-generator / pdfkit-py | SeaWork-Labs | skills/ |
| lieflat-less-ai-tone | larashero3-dotcom | skills/ |

---

## 📝 备选工具备忘（未安装）

以下项目调研后暂未纳入技能库，仅作备选记录（workaround）。

### ruin-everything（浏览器自动化 MCP）

本地共享 Chrome 运行时，通过 CDP（`127.0.0.1:9222`）+ stdio MCP 暴露浏览器工具（`ruin_browser`、`ruin_auto_register` 等）。主打求职网站（Greenhouse/Ashby/Workday/飞书招聘）与学术机构 SSO（IEEE/ACM/Springer 经大学登录）适配器。

```json
{
  "mcpServers": {
    "ruin-everything": {
      "command": "uvx",
      "args": ["--isolated", "--refresh", "--from", "ruin-everything[mcp]", "ruin-mcp"],
      "env": { "RUIN_AUTO_UPDATE": "0" }
    }
  }
}
```

风险与限制：

- `~/.ruin/identity.json` 明文存储账号密码
- 读取 macOS 短信数据库抓取验证码（需授权 Messages）
- 内置滑块/拼图验证码绕过，存在平台 ToS 风险
- 与 Playwright MCP 功能重叠；早期项目，star 数少
- `uvx --refresh` 每次启动拉取最新代码，建议锁定版本

结论：仅当需要"持久化共享 Chrome profile + 求职/学术专用适配器"时再启用；纯浏览器自动化用 Playwright MCP 即可。

### Agent-Reach（站点访问聚合 CLI，未装）

"让 Agent 够得上登录态互联网"的聚合壳：每个渠道 = 上游工具有序列表（opencli / bili-cli / yt-dlp / Jina Reader / Exa / boss-agent-cli）。**小红书渠道 = 直接调 `opencli xiaohongshu search|note|comments`**，Agent-Reach 只提供专用浏览器、cookie 复制与错误码归一化。

风险：

- 作者可信度存疑；夹带 CloakBrowser 闭源浏览器二进制（非 MIT）
- OpenCLI Bridge 扩展会复制主 Chrome 站点 cookie 到专用浏览器（不装扩展即可掐断该链路）
- ⚠️ PyPI 上的 `agent-reach` 是冒名包，安装只认 GitHub Releases zip（`uv tool install .../agent-reach.zip`）

隔离方案（如日后要装）：`sandbox-exec` deny-list 包装 CLI（挡 Keychains/Chrome profile/.ssh/.aws/短信库/Mail/IM 容器/`.env` 等），不装 Chrome 扩展改用 `agent-reach login` 在专用浏览器登小号，锁 release 版本。容器/独立 macOS 用户方案会废掉 login GUI 渠道。

结论：**不装**。与 AnySearch 重合度低但非刚需；需要小红书搜索时直接用 OpenCLI。

### OpenCLI（jackwener，CLI+daemon，未装）

与 `wx-cli` 同作者（31k star，Apache-2.0），"把任意网站变成 CLI"：npm 包 + Browser Bridge Chrome 扩展 + 懒启动本地 daemon（`localhost:19825`）+ 官方 agent skills（`npx skills add jackwener/opencli`）。100+ 站点内置适配器（小红书 `search/note/comments` 等 15 个命令），输出统一 `{ok, data}` JSON；另有通用 `opencli browser` 原语。

评估：

- 扩展声明纯 localhost、无遥测、cookie 按域名按需读取不离开 Chrome（PRIVACY.md；npm 包本体不在声明范围）
- ⚠️ 含写命令（`publish`/`like`/`comment`/`follow`/`reply-dm`），误用或恶意适配器可借登录态发帖
- daemon 监听 localhost:19825，本机其他进程理论上可驱动

安装路径（未执行）：`npm i -g @jackwener/opencli`（需 Node ≥20.18.1）→ Chrome Web Store 装扩展 → `opencli doctor`。建议把扩展装在**专用 Chrome Profile + 小号**——profile 本身就是隔离边界。官方另有 OpenCLIApp 桌面版（托盘 UI + 托管更新）。

结论：**暂不装**，但它是日后做"登录态站点访问"（小红书等）的首选实现，优先级高于 Agent-Reach。

### veraPDF（PDF/A 合规校验 CLI，未装）

ISO 19005（PDF/A）与 PDF/UA（ISO 14289）校验的参考实现（EU 资助、Open Preservation Foundation 维护），政府/图书馆归档场景事实标准。`brew install verapdf` 即可。

用途：校验欧盟/政府归档公文是否真正符合 PDF/A，或转换后验证产出合规。

结论：**暂不装**——pdfkit-py 已覆盖日常 PDF 处理（PyMuPDF + OCR + 表单）；仅当需要 ISO 19005 合规验证时再启用。

---

## 🛡️ 安全

漏洞报告请参见 [SECURITY.md](SECURITY.md)。

## 📄 许可证

本项目基于 [MIT License](LICENSE)。归档技能与文档保留各自上游许可证。
