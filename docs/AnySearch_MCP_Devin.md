# AnySearch MCP 在 Devin 的部署记录

> 记录 AnySearch 接入 Devin 的方式演进与维护要点，以后改动有据可查。
> 初版：2026-10-21（远程 HTTP 直连）；**2026-10-21 晚改为本地 stdio wrapper**。路径统一用 `~` 表示用户主目录。

## 背景与决策

- 原先 AnySearch 以 skill 形式接入（`skills/anysearch-skill` → `~/.claude/skills`）。其 CLI 每次激活都要先找 `runtime.conf` 读 Runtime/Command，在其他项目里还要先定位 skill 目录，稳定浪费一轮交互。
- 第一阶段曾直连官方远程 MCP（`https://api.anysearch.com/mcp`，Streamable HTTP + Bearer）。**发现其 `tools/list` 下发的工具描述极度臃肿**——数千 token 的 sub_domain 决策流、GEO 向硬规则常驻上下文。
- 远程 server 的工具描述**无法在客户端覆盖**，因此第二阶段改为**本地 stdio wrapper**：`scripts/mcp/anysearch_mcp.py` 重新声明同名工具但用精简 docstring，转发到与 skill CLI 相同的 REST 端点（`POST /v1/search`、`GET /v1/sub-domains`、`POST /v1/extract`）。
- 顺带收益：API key 从 `mcp_config.json` 挪进 `scripts/mcp/.env`（gitignored），改 MCP 配置不再接触密钥。

## 部署形态（当前生效）

- 配置文件：`~/.config/devin/mcp_config.json`（Devin **用户级**），条目不包含任何密钥：

```json
"anysearch": {
  "command": "uv",
  "args": ["run", "<repo 绝对路径>/scripts/mcp/anysearch_mcp.py"]
}
```

- 传输：stdio（本地 `uv run` 拉起）；wrapper 内部走 HTTPS 调 `api.anysearch.com/v1/*`
- 密钥：`scripts/mcp/.env` 中 `ANYSEARCH_API_KEY=`；查找优先级 `.env` > 环境变量，**无 key 则匿名模式**（低限流），与上游一致
- 依赖：`mcp>=1.10,<2` + `httpx[socks]`，PEP 723 内联声明，uv 自动解析
- 生效时机：**新开会话才加载** MCP 配置

## 工具清单（精简描述版）

| 工具 | 说明 |
|------|------|
| `anysearch_search` | query + 可选 tag/params/zone/language/max_results；垂直查询先用 get_sub_domains 取 tag |
| `anysearch_get_sub_domains` | 列 1-5 个 domain 的 sub_domain、描述、必需参数 |
| `anysearch_batch_search` | 1-5 个独立查询并行（asyncio.gather） |
| `anysearch_extract` | URL → 清洗正文，输出带 untrusted-content 警示头 |

关键语义保留：结构化/垂直查询（ticker、专利、DOI、酒店等）必须先用 `get_sub_domains` 拿合法 `tag`（`<domain>.<sub_domain>`）和 `params`，不允许瞎猜 tag——这是原版描述里唯一值得保留的硬规则。

## 维护操作

```bash
# 冒烟测试（initialize + tools/list + 真实调用）
cd <repo> && (printf '%s\n%s\n%s\n' \
  '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"t","version":"0"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
  '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"anysearch_search","arguments":{"query":"test","max_results":3}}}' \
; sleep 20) | timeout 40 uv run scripts/mcp/anysearch_mcp.py

# 换 key：编辑 scripts/mcp/.env 里的 ANYSEARCH_API_KEY
# 停用：mcp_config.json 条目加 "disabled": true
```

注意：stdio 冒烟测试时 **stdin 不能提前 EOF**——上面用 `sleep` 挂住 stdin，否则服务端可能在响应写出前就退出。

## 注意事项

- 免费 key：https://anysearch.com/console/api-keys
- `X-Anysearch-Client: antigravity-mcp/1.0`（自建标识，官方原版是 `mcp/1.0.0`/`skill/3.1.1`）
- `scripts/mcp/.env` 被仓库 `.gitignore` 的 `*.env` 规则覆盖，不提交；`.env.example` 同理仅作本地模板
- 仓库内 `skills/anysearch-skill/` 仍在（含过期旧 key 的 `.env`）——若回链 skill 记得换 key；skill 上游更新与本 wrapper 解耦
- `mcp<2` 是硬约束（2.x API 大改），升级依赖前先改代码
- 官方远程 MCP（`api.anysearch.com/mcp`）仍可用，若上游哪天精简了工具描述可直接切回 HTTP 条目
- 其他客户端要接同款：`~/.claude.json`、`~/.codex/config.toml`、`~/.gemini/settings.json` 用相同 `command/args` 形式条目
