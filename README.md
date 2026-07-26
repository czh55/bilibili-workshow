# bilibili-workshop

B 站 / 小红书视频 → Whisper 完整转录 → HTML 图文实录 + SVG 理性分析 → GitHub Pages。

Webhook 收到链接后先自动识别平台，再按同一套双轨流程生成：

- **HTML 图文实录**：按时间展开原始内容，包含关键截图和完整转录，阅读轻松、偏纪实
- **SVG 理性分析**：用关系图、卡片、对比表和行动清单重组观点，强调客观证据与适用边界

## 结构

```
bilibili-workshop/
├── detect-platform.mjs   # 自动识别 B 站 / 小红书
├── svg-auto-height.mjs   # SVG 自动测高与 XML 修复
├── docs/
│   ├── WORKFLOW.md       # Automation 执行规范（权威）
│   ├── index.html        # GitHub Pages 首页
│   ├── index.json        # 总结条目索引
│   ├── assets/<slug>/    # 视频关键画面
│   ├── *-图文实录.html   # 纪实叙述、截图与完整转录
│   └── *-理性分析.svg    # 客观结构化分析长图
└── .gitignore
```

## Webhook

```bash
# B 站
curl -X POST "<webhook-url>" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.bilibili.com/video/BVxxx","date":"2026-07-24"}'

# 小红书
curl -X POST "<webhook-url>" \
  -H "Content-Type: application/json" \
  -d '{"url":"http://xhslink.cn/o/xxxxxx","date":"2026-07-26"}'
```

平台识别：

```bash
node detect-platform.mjs "https://b23.tv/xxxx"
node detect-platform.mjs "http://xhslink.cn/o/xxxx"
```

## 依赖

- `yt-dlp`
- `ffmpeg`
- `openai-whisper`
- Node.js（生成 HTML 与 SVG、平台识别）

详见 `docs/WORKFLOW.md`。
