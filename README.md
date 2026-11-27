# routing-rules

自维护的多端通用分流规则仓库：以 `MetaCubeX/meta-rules-dat` 作为活跃上游，叠加自维护的 AI 防串出口规则与常用业务补丁，由 GitHub Actions 每日自动构建并发布到 `release` 分支，**一份源码同时产出 Mihomo (`.mrs`) 与 Surge / Shadowrocket / Loon (`DOMAIN-SET` + `RULE-SET`)**。

- **`main` 分支**：源补丁（`sources/`）、清单（`manifest.json`）与构建脚本（`scripts/build.py`）
- **`release` 分支**：自动编译产物，仅在规则实际变化时提交
  - `mihomo/domain/*.mrs`、`mihomo/ip/*.mrs`：Mihomo / OpenClash 二进制规则集
  - `mihomo/classical/*.list`：Clash Classical 规则集
  - `surge/*.list`：Surge / Shadowrocket / Loon 标准 `RULE-SET`（`claude`、`telegram`、`netflix`、`google` 已自动合并官方 IP 段；`claude` 另含 `DOMAIN-KEYWORD,datadog`）
  - `surge/domain-set/*.txt`：Surge 原生高速 `DOMAIN-SET`（O(1) 哈希匹配，尤其适合 `cn.txt`、`global.txt` 等大列表）
- **隐私边界**：本仓库仅收录公开通用规则，不包含任何个人自建服务、私有 Emby 或节点信息

## 引用地址前缀

- jsDelivr（推荐国内/路由器直连）：`https://testingcf.jsdelivr.net/gh/w0ven/routing-rules@release/`
- GitHub Raw：`https://raw.githubusercontent.com/w0ven/routing-rules/release/`

完整 43 组规则清单与条目统计见 `release` 分支的 [`SUMMARY.md`](https://raw.githubusercontent.com/w0ven/routing-rules/release/SUMMARY.md)。

### 核心分类速查

| 分类 | Mihomo `.mrs` | Surge `RULE-SET` / `DOMAIN-SET` | 说明 |
|---|---|---|---|
| Claude 全生态 | `mihomo/domain/claude.mrs` + `mihomo/ip/claude-ip.mrs` | `surge/claude.list` | 核心 + 内容 + 第三方登录 + 监控 + MCP + `d.aiip.si`（`.list` 含 `datadog` 与官方 IP） |
| Claude 精简核 | `mihomo/domain/claude-core.mrs` | `surge/claude-core.list` | 不含 `accounts.google.com` / `sentry.io` / `intercom.io` |
| ChatGPT | `mihomo/domain/chatgpt.mrs` | `surge/domain-set/chatgpt.txt` / `surge/chatgpt.list` | OpenAI / ChatGPT / Sora / LiveKit / Arkose / Azure 静态资源 |
| Gemini | `mihomo/domain/gemini.mrs` | `surge/domain-set/gemini.txt` | Gemini / AI Studio / NotebookLM / Antigravity |
| Intelligence / 其他 AI | `mihomo/domain/intelligence.mrs` / `ai-other.mrs` | `surge/domain-set/intelligence.txt` | Apple Intelligence + Perplexity / Grok / Copilot / Cursor / Windsurf / Groq / Suno / HuggingFace |
| 全部海外 AI 合集 | `mihomo/domain/ai-all.mrs` | `surge/ai-all.list` | 上述全部 AI + `category-ai-!cn` |
| 常用服务与流媒体 | `mihomo/domain/<name>.mrs` | `surge/domain-set/<name>.txt`（含 IP 的用 `surge/<name>.list`） | `speedtest`、`apple-cn`、`apple`、`github`、`microsoft`、`telegram`、`twitter`、`discord`、`crypto`、`steam`、`game-all`、`gamer-with-steam`、`nvidia`、`youtube`、`netflix`、`disney`、`spotify`、`tiktok`、`bilibili`、`china-media`、`global-media`、`google` |
| 社区 / 国内直连 / 兜底 | `forum.mrs` / `cn-direct-extra.mrs` / `global.mrs` / `cn.mrs` | `surge/domain-set/{forum,cn-direct-extra,global,cn}.txt` | 社区论坛、抖音/字节+Steam CDN、非 CN 总集、CN 总集 |

## 日常维护

1. 新增或调整域名：编辑 `sources/` 下对应文件并提交到 `main`。
2. 排除上游误杀域名：写入 `sources/exclude/ai-all.exclude.txt`（或在 `manifest.json` 挂接 `excludes`）。
3. 推送 `main` 或每日北京时间 04:00 由 GitHub Actions 自动构建并同步到 `release` 分支。
