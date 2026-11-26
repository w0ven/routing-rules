# Built Rulesets Summary

| Ruleset | Type | Entries | Description |
|---|---:|---:|---|
| `claude-core` | `domain` | 25 | Claude 精简核心与内容域名（不含多站共用的第三方登录/监控域名） |
| `claude` | `domain` | 33 | Claude 全生态防串出口域名（核心 + 内容 + 登录第三方 + 监控统计 + d.aiip.si） |
| `claude-ip` | `ipcidr` | 2 | Anthropic 官方公布的 IPv4 / IPv6 网段兜底 |
| `chatgpt` | `domain` | 24 | ChatGPT / OpenAI / Sora 全量域名 |
| `gemini` | `domain` | 52 | Google Gemini / AI Studio / NotebookLM / Antigravity 域名 |
| `ai-other` | `domain` | 29 | 其他海外 AI 服务（Perplexity / xAI Grok / Meta AI / Cursor / OpenRouter / Midjourney 等） |
| `ai-all` | `domain` | 241 | 全部海外 AI 合集（Claude + ChatGPT + Gemini + 其他 AI + MetaCubeX category-ai-!cn） |
| `forum` | `domain` | 12 | 通用技术与主机社区论坛（固定出口减少 Cloudflare 验证） |
| `cn-direct-extra` | `domain` | 98 | 通用国内直连补充（抖音/字节国内 CDN + Steam 国内下载 CDN） |
| `game-epic` | `domain` | 30 | Epic Games（替代停更的 blackmatrix7 Epic.list） |
| `game-ea` | `domain` | 165 | EA Games（替代停更的 blackmatrix7 EA.list） |
| `game-blizzard` | `domain` | 25 | Blizzard（替代停更的 blackmatrix7 Blizzard.list） |
| `game-ubisoft` | `domain` | 31 | Ubisoft（替代停更的 blackmatrix7 UBI.list） |
| `game-playstation` | `domain` | 5 | PlayStation（替代停更的 blackmatrix7 PlayStation.list） |
| `game-nintendo` | `domain` | 124 | Nintendo（替代停更的 blackmatrix7 Nintendo.list） |
| `game-all` | `domain` | 380 | 六大海外游戏平台合集（Epic / EA / Blizzard / Ubisoft / PlayStation / Nintendo） |
| `nvidia` | `domain` | 66 | Nvidia（替代停更的 blackmatrix7 Nvidia.list） |
| `test-check` | `domain` | 22 | 通用 IP / 测速 / DNS 泄露检测域名（干净版，不含 challenges.cloudflare.com） |
| `block-adobe` | `domain` | 4 | Adobe 验证与遥测域名屏蔽 |
