# bilibili-workshop

B 站视频 → Whisper 完整转录 → HTML 图文实录 + SVG 理性分析 → GitHub Pages。

每个视频从两个互补角度呈现：

- **HTML 图文实录**：按时间展开原始内容，包含关键截图和完整转录，阅读轻松、偏纪实
- **SVG 理性分析**：用关系图、卡片、对比表和行动清单重组观点，强调客观证据与适用边界

## 结构

```
bilibili-workshop/
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
curl -X POST "<webhook-url>" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.bilibili.com/video/BVxxx","date":"2026-07-24"}'
```

## 依赖

- `yt-dlp`
- `ffmpeg`
- `openai-whisper`
- Node.js（生成 HTML 与 SVG）

详见 `docs/WORKFLOW.md`。
