# bilibili-workshop

B 站视频 → Whisper 完整转录 → 结构化总结 + 关键截图 → HTML 阅读页 → GitHub Pages。

## 结构

```
bilibili-workshop/
├── docs/
│   ├── WORKFLOW.md       # Automation 执行规范（权威）
│   ├── index.html        # GitHub Pages 首页
│   ├── index.json        # 总结条目索引
│   ├── assets/<slug>/    # 视频关键画面
│   └── *-总结.html       # 总结、截图与完整转录
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
- Node.js（生成独立 HTML 页面）

详见 `docs/WORKFLOW.md`。
