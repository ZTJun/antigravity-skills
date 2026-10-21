# AnySearch MCP 在 Devin 的部署记录

> 记录 AnySearch 从 skill 切换到官方 MCP server 的部署方式与维护要点，以后改动有据可查。
> 部署日期：2026-10-21。路径统一用 `~` 表示用户主目录。

## 背景与决策

- 原先 AnySearch 以 skill 形式接入（`skills/anysearch-skill` → `~/.claude/skills`）。其 CLI 每次激活都要先找 `runtime.conf` 读 Runtime/Command，在其他项目里还要先定位 skill 目录，稳定浪费一轮交互。
- 官方 MCP server 与 skill **同源**：skill 的 CLI 本质就是向 `https://api.anysearch.com/mcp` 发 JSON-RPC `tools/call`，两者能力完全一致（`search` / `batch_search` / `get_sub_domains` / `extract`）。
- 决策：**只在 Devin 用户级装 MCP**，其他客户端未配 MCP，如需保留可重新链接 skill。

## 部署形态

- 配置文件：`~/.config/devin/mcp_config.json`（Devin **用户级**，v3000.3 起 MCP 配置独立成文件，旧版在主 `config.json` 的 `mcpServers` 里会自动迁移）
- 传输：Streamable HTTP，远程托管，**无本地安装包**
- 配置内容（key 值已略去）：

```json
{
  "mcpServers": {
    "anysearch": {
      "url": "https://api.anysearch.com/mcp",
      "headers": {
        "Authorization": "Bearer <ANYSEARCH_API_KEY>",
        "X-Anysearch-Client": "mcp/1.0.0"
      }
    }
  }
}
```

- API key **明文存在用户级配置文件里**（该文件不进 git，与 `~/.claude.json` 信任级别相同）。`headers` 是否支持 `${env:VAR}`/`${file:path}` 引用未验证，故采用明文写入。
- 生效时机：**新开会话才加载** MCP 配置，改动后需重启会话。

## 当时的部署流程（可复现）

1. 在 `mcp_config.json` 的 `mcpServers` 加 `anysearch` 条目（先无 key，匿名即可连通）
2. key 通过 inbox 流程注入：用户把 key 写入 `~/.config/devin/anysearch-api-key.inbox` 第一行，再由脚本用 `jq` 写进 `headers.Authorization`（key 不经过对话），inbox 清空后移入 `~/.trash`
3. 验证：`tools/list` + `tools/call get_sub_domains` 带 Bearer 返回真实数据（见下）
4. 摘除 `~/.claude/skills/anysearch-skill` 符号链接 → `~/.trash`（仓库源文件保留）

## 维护操作

```bash
# 匿名连通性测试（无需 key）
curl -sS -X POST https://api.anysearch.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list"}'

# 换 key：直接改 mcp_config.json 里 headers.Authorization 即可；inbox 流程可复用
# 停用：条目加 "disabled": true；删除：整条移除
# 若装了 devin CLI 也可用: devin mcp list / disable / remove（注意本机 devin 不在 PATH）
```

## 注意事项

- **匿名可用但限流低**；免费 key 在 https://anysearch.com/console/api-keys 申请
- `X-Anysearch-Client: mcp/1.0.0` 是官方建议的标识头，保留
- 仓库内 `skills/anysearch-skill/` 仍在（含 `.env` 旧 key 已过期、`runtime.conf` 指向本仓库路径）——若哪天回链 skill，记得换 `.env` 里的 key
- 上游 skill 更新与本 MCP 部署解耦：`sync_skills.sh` 照常同步 anysearch 源，互不影响
- 官方仓库：`anysearch-ai/anysearch-mcp-server`（Apache 2.0）；mcp.so / Glama / Smithery 有收录
- 其他客户端要接 MCP：`~/.claude.json`（Claude Code）、`~/.codex/config.toml`、`~/.gemini/settings.json` 均支持同类 HTTP server 配置，key 处理方式相同
