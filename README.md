# routing-rules

自维护的多端通用分流规则仓库：以 `MetaCubeX/meta-rules-dat` 作为活跃上游，叠加自维护的 AI 防串出口规则与常用业务补丁，由 GitHub Actions 每日自动构建并发布到 `release` 分支。

- **`main` 分支**：源补丁（`sources/`）、清单（`manifest.json`）与构建脚本（`scripts/build.py`）
- **`release` 分支**：自动编译产物（`mihomo/domain/*.mrs`、`mihomo/ip/*.mrs`、`mihomo/classical/*.list`、`surge/*.list`），仅在规则实际变化时提交
- **隐私边界**：本仓库仅收录公开通用规则，不包含任何个人自建服务、私有 Emby 或节点信息

## 产物目录与引用方式（jsDelivr）

基础前缀：
- jsDelivr（推荐国内/路由器直连）：`https://testingcf.jsdelivr.net/gh/w0ven/routing-rules@release/`
- GitHub Raw：`https://raw.githubusercontent.com/w0ven/routing-rules/release/`

| 规则集 | 类型 | Mihomo `.mrs` 路径 | Classical / Surge `.list` 路径 | 说明 |
|---|---|---|---|---|
| `claude` | domain | `mihomo/domain/claude.mrs` | `mihomo/classical/claude.list` | Claude 全生态（核心+内容+第三方登录+监控+`d.aiip.si`，classical 含 `datadog` 关键词与官方 IP） |
| `claude-core` | domain | `mihomo/domain/claude-core.mrs` | `mihomo/classical/claude-core.list` | Claude 精简核心（不含 `accounts.google.com`/`sentry.io`/`intercom.io`） |
| `claude-ip` | ipcidr | `mihomo/ip/claude-ip.mrs` | `mihomo/classical/claude-ip.list` | Anthropic 官方 IPv4/IPv6 段（`160.79.104.0/21`、`2607:6bc0::/32`） |
| `chatgpt` | domain | `mihomo/domain/chatgpt.mrs` | `mihomo/classical/chatgpt.list` | ChatGPT / OpenAI / Sora 全量域名 |
| `gemini` | domain | `mihomo/domain/gemini.mrs` | `mihomo/classical/gemini.list` | Gemini / AI Studio / NotebookLM / Antigravity |
| `ai-other` | domain | `mihomo/domain/ai-other.mrs` | `mihomo/classical/ai-other.list` | Perplexity / xAI Grok / Meta AI / Cursor / OpenRouter 等 |
| `ai-all` | domain | `mihomo/domain/ai-all.mrs` | `mihomo/classical/ai-all.list` | 上述全部 AI + `category-ai-!cn` 合集（适合单 AI 组客户端） |
| `forum` | domain | `mihomo/domain/forum.mrs` | `mihomo/classical/forum.list` | 通用技术与主机社区论坛 |
| `cn-direct-extra` | domain | `mihomo/domain/cn-direct-extra.mrs` | `mihomo/classical/cn-direct-extra.list` | 抖音/字节国内 CDN + Steam 国内下载 CDN |
| `game-all` | domain | `mihomo/domain/game-all.mrs` | `mihomo/classical/game-all.list` | Epic / EA / Blizzard / Ubisoft / PlayStation / Nintendo 合集（亦提供独立单平台 `.mrs`） |
| `nvidia` | domain | `mihomo/domain/nvidia.mrs` | `mihomo/classical/nvidia.list` | Nvidia 官网与驱动下载 |
| `test-check` | domain | `mihomo/domain/test-check.mrs` | `mihomo/classical/test-check.list` | 常用 IP / 测速 / DNS 泄露检测站（不含 `challenges.cloudflare.com`） |
| `block-adobe` | domain | `mihomo/domain/block-adobe.mrs` | `mihomo/classical/block-adobe.list` | Adobe 验证与遥测屏蔽 |

## Mihomo / OpenClash 推荐用法

配合 `rule-set:` 在 `dns.nameserver-policy` 中直接复用同一份 `.mrs`，规则更新后分流与 DNS 策略自动保持同步：

```yaml
dns:
  nameserver-policy:
    "rule-set:Claude / Domain":
      - https://1.1.1.1/dns-query#Claude
      - https://8.8.8.8/dns-query#Claude
    "rule-set:ChatGPT / Domain":
      - https://1.1.1.1/dns-query#ChatGPT
      - https://8.8.8.8/dns-query#ChatGPT

rules:
  - AND,((NETWORK,UDP),(DST-PORT,443),(OR,((RULE-SET,Claude / Domain),(RULE-SET,ChatGPT / Domain),(RULE-SET,Claude / IP)))),REJECT
  - AND,((IP-CIDR,1.1.1.1/32,no-resolve),(DST-PORT,443)),Claude
  - DOMAIN-KEYWORD,datadog,Claude
  - RULE-SET,Claude / Domain,Claude
  - RULE-SET,Claude / IP,Claude,no-resolve
  - RULE-SET,ChatGPT / Domain,ChatGPT
  - RULE-SET,Gemini / Domain,Gemini
  - RULE-SET,AI Other / Domain,Claude

rule-providers:
  Claude / Domain:
    type: http
    interval: 86400
    behavior: domain
    format: mrs
    url: "https://testingcf.jsdelivr.net/gh/w0ven/routing-rules@release/mihomo/domain/claude.mrs"
  Claude / IP:
    type: http
    interval: 86400
    behavior: ipcidr
    format: mrs
    url: "https://testingcf.jsdelivr.net/gh/w0ven/routing-rules@release/mihomo/ip/claude-ip.mrs"
  ChatGPT / Domain:
    type: http
    interval: 86400
    behavior: domain
    format: mrs
    url: "https://testingcf.jsdelivr.net/gh/w0ven/routing-rules@release/mihomo/domain/chatgpt.mrs"
```

## 日常维护

1. 新增或调整域名：直接编辑 `sources/` 下对应文件并提交到 `main`。
2. 排除上游误杀域名：写入 `sources/exclude/ai-all.exclude.txt`（或为任意规则集在 `manifest.json` 挂接 `excludes`）。
3. 推送到 `main` 后 GitHub Actions 会自动重新编译并更新 `release` 分支；无变动时每日北京时间 04:00 也会自动同步 `MetaCubeX` 上游。
