# Built Rulesets Summary

| Ruleset | Type | Entries | Extra Rules (List) | Description |
|---|---:|---:|---:|---|
| `claude-core` | `domain` | 32 | 0 | Claude 精简核心与内容域名（不含多站共用的第三方登录/监控域名） |
| `claude` | `domain` | 41 | 3 | Claude 全生态防串出口域名（核心 + 内容 + 登录第三方 + 监控统计 + MCP + d.aiip.si；list 版含 datadog 与官方 IP） |
| `claude-ip` | `ipcidr` | 2 | 0 | Anthropic 官方公布的 IPv4 / IPv6 网段兜底 |
| `chatgpt` | `domain` | 27 | 0 | ChatGPT / OpenAI / Sora / LiveKit / Arkose / Azure 静态资源全量域名 |
| `gemini` | `domain` | 52 | 0 | Google Gemini / AI Studio / NotebookLM / Antigravity 域名 |
| `apple-intelligence` | `domain` | 6 | 0 | Apple Intelligence 专用域名（不含普通 iCloud） |
| `ai-other` | `domain` | 54 | 0 | 其他海外 AI 服务（Perplexity / xAI Grok / Meta AI / Copilot / Cursor / Windsurf / Groq / Suno / HuggingFace 等） |
| `intelligence` | `domain` | 60 | 0 | Apple Intelligence + 其他海外 AI 合集（适配 Surge Intelligence 策略组） |
| `ai-all` | `domain` | 260 | 3 | 全部海外 AI 合集（Claude + ChatGPT + Gemini + Intelligence + MetaCubeX category-ai-!cn） |
| `speedtest` | `domain` | 20 | 0 | Ookla Speedtest 测速域名 |
| `apple-cn` | `domain` | 165 | 0 | Apple 国内直连服务域名 |
| `apple` | `domain` | 1666 | 0 | Apple 全部服务域名 |
| `github` | `domain` | 66 | 0 | GitHub 全量域名 |
| `microsoft` | `domain` | 758 | 0 | Microsoft 全量域名 |
| `telegram` | `domain` | 21 | 12 | Telegram 全量域名（list 版含官方 IP 段） |
| `twitter` | `domain` | 28 | 0 | X / Twitter 全量域名 |
| `discord` | `domain` | 28 | 0 | Discord 全量域名 |
| `crypto` | `domain` | 71 | 0 | 主流加密货币交易所（OKX / Binance / Bybit） |
| `google` | `domain` | 1079 | 6915 | Google 全家桶域名（list 版含 Google IP 段） |
| `youtube` | `domain` | 178 | 0 | YouTube 全量域名 |
| `netflix` | `domain` | 24 | 122 | Netflix 全量域名（list 版含官方 IP 段） |
| `disney` | `domain` | 224 | 0 | Disney+ 全量域名 |
| `spotify` | `domain` | 28 | 0 | Spotify 全量域名 |
| `tiktok` | `domain` | 40 | 0 | TikTok 国际版全量域名 |
| `bilibili` | `domain` | 53 | 0 | BiliBili 全量域名 |
| `china-media` | `domain` | 461 | 0 | 中国大陆主流流媒体域名 |
| `global-media` | `domain` | 2163 | 0 | 国际流媒体与娱乐服务合集 |
| `steam` | `domain` | 61 | 0 | Steam 平台域名 |
| `game-epic` | `domain` | 30 | 0 | Epic Games |
| `game-ea` | `domain` | 165 | 0 | EA Games |
| `game-blizzard` | `domain` | 25 | 0 | Blizzard |
| `game-ubisoft` | `domain` | 31 | 0 | Ubisoft |
| `game-playstation` | `domain` | 5 | 0 | PlayStation |
| `game-nintendo` | `domain` | 124 | 0 | Nintendo |
| `game-all` | `domain` | 380 | 0 | 六大海外游戏平台合集（Epic / EA / Blizzard / Ubisoft / PlayStation / Nintendo） |
| `gamer-with-steam` | `domain` | 441 | 0 | Steam + 六大海外游戏平台合集（适配 Surge Gamer 策略组） |
| `nvidia` | `domain` | 66 | 0 | Nvidia 全量域名 |
| `telegram-dc1` | `ipcidr` | 3 | 1 | Telegram DC1 / DC3 美东机房（AS59930 官方 IP 段；list 版附带 IP-ASN） |
| `telegram-dc2-4` | `ipcidr` | 11 | 2 | Telegram DC2 / DC4 欧洲机房（AS62041 / AS211157 官方 IP 段；list 版附带 IP-ASN） |
| `telegram-dc5` | `ipcidr` | 6 | 2 | Telegram DC5 新加坡机房（AS44907 / AS62014 官方 IP 段；list 版附带 IP-ASN） |
| `forum` | `domain` | 12 | 0 | 通用技术与主机社区论坛（固定出口减少 Cloudflare 验证） |
| `cn-direct-extra` | `domain` | 98 | 0 | 通用国内直连补充（抖音/字节国内 CDN + Steam 国内下载 CDN） |
| `httpdns-block` | `domain` | 67 | 0 | 国内 App HTTPDNS 解析域名拦截（Mihomo/Surge 通用，不含普通业务域） |
| `test-check` | `domain` | 22 | 0 | 通用 IP / 测速 / DNS 泄露检测域名（干净版，不含 challenges.cloudflare.com） |
| `block-adobe` | `domain` | 4 | 0 | Adobe 验证与遥测域名屏蔽 |
| `global` | `domain` | 27244 | 0 | 非中国大陆通用代理域名总集（MetaCubeX geolocation-!cn，Surge 建议使用 DOMAIN-SET） |
| `cn` | `domain` | 110177 | 0 | 中国大陆直连域名总集（MetaCubeX cn，Surge 建议使用 DOMAIN-SET） |
