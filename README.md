# bilibili-workshop

B 站视频 → Whisper 转录 → 结构化总结 → SVG 长图 → GitHub Pages。

## 结构

```
bilibili-workshop/
├── svg-auto-height.mjs   # SVG 自动测高
├── docs/
│   ├── WORKFLOW.md       # Automation 执行规范（权威）
│   ├── index.html        # GitHub Pages 首页
│   ├── index.json        # 总结条目索引
│   └── *-总结.svg        # 产出长图
└── .gitignore
```

## Webhook

```bash
curl -X POST "<webhook-url>" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.bilibili.com/video/BVxxx","date":"2026-07-24"}'
```

## 依赖

- `yt-dlp`
- `ffmpeg`
- `openai-whisper`
- Node.js（运行 `generate-*.mjs`）

详见 `docs/WORKFLOW.md`。
