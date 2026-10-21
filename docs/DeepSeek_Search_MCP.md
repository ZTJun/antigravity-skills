# DeepSeek Search MCP 部署记录（Devin）

> 记录时间：2026-10-21 | 部署对象：DeepSeek 官方 Search/Fetch API → 本地 stdio MCP 封装
> 相关文档：`docs/AnySearch_MCP_Devin.md`（同模式部署案例）

## 1. 背景与决策

2026 年 DeepSeek 发布了官方 Search / Fetch **REST API**（不是 MCP）：

| API | 端点 | 说明 |
|-----|------|------|
| Search | `POST https://api.deepseek.com/v1/tools/search` | DeepSeek 自研搜索引擎，`query` 支持 `site:` / `-site:` / `la:zh` / `after:` / `before:` 运算符 |
| Fetch | `POST https://api.deepseek.com/v1/tools/fetch` | 抓单页 URL → 返回 Markdown |

- 官方文档：`https://api-docs.deepseek.com/guides/search`（中文 `/zh-cn/guides/web_search`）
- 认证：DeepSeek 主站 API key，Bearer，与 chat 模型调用同一把 key、同一个充值账户
- **官方没有 MCP server**；社区现存的 deepseek-mcp-server 包的是 chat API，与本需求不符 → 自行封装薄 stdio wrapper（~130 行，零第三方服务信任面）
- 与 AnySearch 互补：DeepSeek 自研引擎（中文源覆盖好）+ AnySearch 垂直域搜索（finance/academic/travel），可并行交叉验证

## 2. 架构

```
Devin MCP client --stdio--> uv run scripts/mcp/deepseek_search_mcp.py
                                │  (FastMCP, mcp<2 + httpx, PEP723 内联依赖)
                                ├─ 启动时 _load_env(): scripts/mcp/.env > env var
                                └─ HTTPS POST → api.deepseek.com/v1/tools/{search,fetch}
```

**关键设计：key 不进 MCP 配置。** `mcp_config.json` 里只有 `uv run <脚本>`，key 存脚本同目录的 `scripts/mcp/.env`（gitignored），后续改 MCP 配置不会接触密钥。加载逻辑镜像 `skills/anysearch-skill/scripts/anysearch_cli.py` 的 `_load_env()`（utf-8-sig、跳过注释空行、剥引号、`.env` 覆盖环境变量）。

## 3. 部署形态（实际生效配置）

`~/.config/devin/mcp_config.json`（用户级，与 anysearch 并列）：

```json
"deepseek-search": {
  "command": "uv",
  "args": ["run", "<repo 绝对路径>/scripts/mcp/deepseek_search_mcp.py"]
}
```

无 `env` 块 —— 这是刻意设计，密钥只在 `scripts/mcp/.env`：

```dotenv
DEEPSEEK_API_KEY=<key>   # 参考 scripts/mcp/.env.example
```

Key 查找优先级（与 anysearch 一致）：`scripts/mcp/.env` > 仓库根 `.env` > `DEEPSEEK_API_KEY` 环境变量。

## 4. 工具清单

| 工具 | 参数 | 说明 |
|------|------|------|
| `deepseek_search` | `query`, `count`(1-50, 默认10), `need_content`(默认false), `ori_question` | 网络搜索；`need_content=true` 会返回每个结果全文（很费 token） |
| `deepseek_fetch` | `url` | 抓网页转 Markdown |

错误时工具返回字符串错误信息（含 HTTP 状态码），无 key 时返回安装指引。

## 5. 部署 / 换 key 流程

```bash
# 首次装 key / 轮换
vim <repo>/scripts/mcp/.env        # DEEPSEEK_API_KEY=sk-xxx
# 或走 inbox：把 key 写到 ~/.config/devin/deepseek-api-key.inbox 第一行，
# 让 Devin 写入 .env 并把 inbox 移到 ~/.trash

# 冒烟测试（initialize + tools/list）
cd <repo>
printf '%s\n%s\n%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"0"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}' \
| timeout 60 uv run scripts/mcp/deepseek_search_mcp.py

# 期望最后行返回 ["deepseek_search", "deepseek_fetch"]
```

`tools/list` 通过 ≠ key 有效；真实验证要在新会话调一次 `deepseek_search`。

## 6. 注意事项

- **新会话生效**：Devin 只在会话启动时加载 MCP 配置
- **计费**：约 5 元/1000 次成功请求（按调用次数计，非 token；仍以 platform.deepseek.com 控制台为准）
- **`uv run` 首次冷启**要下载 `mcp`/`httpx` 依赖（~秒级），之后命中 uv 缓存即起
- **`mcp<2` 必须 pin**：mcp 2.x 把 FastMCP 改名 MCPServer 且 API 变了，升级前需改代码
- **`.env` 已被仓库 `.gitignore` 覆盖**（`*.env`/`.env`/`.env.*` 规则）；注意 `.env.example` 也因此不纳入 git，仅作本地模板
- **其他客户端**：Claude Code `~/.claude.json`、Codex `~/.codex/config.toml`、Gemini `~/.gemini/settings.json` 需要同样的 `command/args` 形式条目
