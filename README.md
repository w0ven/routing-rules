# routing-rules

自维护的多端通用分流规则与 Surge 模块仓库：以 `MetaCubeX/meta-rules-dat` 作为活跃上游，叠加自维护的 AI 防串出口规则、Telegram DC 机房段、HTTPDNS 拦截模块与常用业务补丁，由 GitHub Actions 每日自动构建并发布到 `release` 分支。

- **在线导航与一键复制 / 安装页**：https://w0ven.github.io/routing-rules/
- **`main` 分支**：源补丁（`sources/`）、清单（`manifest.json`）、导航页（`site/`）与构建脚本（`scripts/build.py`）
- **`release` 分支**：自动编译产物（`mihomo/`、`surge/`、`catalog.json`、`index.html`），仅在规则或页面有实质变化时提交
- **隐私边界**：本仓库仅收录公开通用规则与零远端脚本模块，不包含任何个人自建服务、私有 Emby 或节点信息

## 引用地址前缀

- jsDelivr（推荐国内/路由器直连）：`https://testingcf.jsdelivr.net/gh/w0ven/routing-rules@release/`
- GitHub Raw：`https://raw.githubusercontent.com/w0ven/routing-rules/release/`

完整 47 组规则清单见 `release` 分支的 [`SUMMARY.md`](https://raw.githubusercontent.com/w0ven/routing-rules/release/SUMMARY.md) 或直接访问 [在线导航页](https://w0ven.github.io/routing-rules/)。

### 核心产物速查

| 分类 | Mihomo `.mrs` | Surge 推荐引用 | 说明 |
|---|---|---|---|
| **HTTPDNS 拦截模块** | `mihomo/domain/httpdns-block.mrs` | `surge/modules/httpdns-block.sgmodule`（或 `domain-set/httpdns-block.txt`） | 精准拦截国内 App HTTPDNS 解析域名与 IP 路径，零远端 JS |
| **Claude 全生态** | `mihomo/domain/claude.mrs` + `mihomo/ip/claude-ip.mrs` | `surge/claude.list` | 核心 + 内容 + 第三方登录 + 监控 + MCP + `d.aiip.si`（`.list` 含 `datadog` 与官方 IP） |
| **Claude 精简核** | `mihomo/domain/claude-core.mrs` | `surge/claude-core.list` | 不含 `accounts.google.com` / `sentry.io` / `intercom.io` |
| **ChatGPT / Gemini / Intelligence** | `chatgpt.mrs` / `gemini.mrs` / `intelligence.mrs` / `ai-all.mrs` | `surge/chatgpt.list`、`surge/domain-set/{gemini,intelligence}.txt` | OpenAI、Gemini/Antigravity、Apple Intelligence、Copilot、Cursor、Windsurf 等 |
| **Telegram DC 机房** | `mihomo/ip/telegram-dc{1,2-4,5}.mrs` | `surge/telegram-dc{1,2-4,5}.list` | 美东 DC1 (`AS59930`) / 欧洲 DC2-4 (`AS62041/AS211157`) / 新加坡 DC5 (`AS44907/AS62014`)，双端可用 |
| **常用服务与流媒体** | `mihomo/domain/<name>.mrs` | `surge/domain-set/<name>.txt`（含 IP 的用 `surge/<name>.list`） | `speedtest`、`apple-cn`、`apple`、`github`、`microsoft`、`telegram`、`twitter`、`discord`、`crypto`、`steam`、`game-all`、`gamer-with-steam`、`nvidia`、`youtube`、`netflix`、`disney`、`spotify`、`tiktok`、`bilibili`、`china-media`、`global-media`、`google` |
| **社区 / 国内直连 / 兜底** | `forum.mrs` / `cn-direct-extra.mrs` / `global.mrs` / `cn.mrs` | `surge/domain-set/{forum,cn-direct-extra,global,cn}.txt` | 社区论坛、抖音/字节+Steam CDN、非 CN 总集、CN 总集 |
