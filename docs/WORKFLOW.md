# B 站视频 → SVG 自动化工作流

当 Cursor Automation 通过 Webhook 收到 B 站视频链接后，严格按本文档逐步骤执行。**不要跳过或合并任何步骤。**

```
Task Progress:
- [ ] 1. yt-dlp 下载音频（m4a 格式）
- [ ] 2. 安装依赖（ffmpeg + openai-whisper，仅首次）
- [ ] 3. Whisper 转录（--model small --language Chinese）
- [ ] 4. 读取转录稿并深度总结
- [ ] 5. 生成 SVG（Node .mjs + svg-auto-height.mjs）
- [ ] 6. 质量自检
- [ ] 7. 更新 docs/index.json
- [ ] 8. Git 提交并推送到 main（**必须**，Pages 才能展示）
- [ ] 9. 清理临时文件
```

---

## 入口

Webhook payload 格式：

```json
{
  "url": "https://www.bilibili.com/video/BVxxx",
  "date": "2026-07-24"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `url` | 是 | B 站视频链接（bilibili.com 或 b23.tv 短链接） |
| `date` | 否 | 前端展示日期，格式 `YYYY-MM-DD`；**未提供时使用当天日期** |

从 payload 中提取 `url` 字段。若缺失，记录错误并结束。

`date` 字段用于 Step 7 写入 `index.json`，首页按此日期分组展示。

---

## Step 1：yt-dlp 下载音频

```bash
cd ~/Projects/bilibili-workshop
yt-dlp -f "bestaudio[ext=m4a]/bestaudio/best" -o "{slug}.%(ext)s" "{url}"
```

- `{slug}`：从视频标题提取英文/拼音关键词，≤30 字符，不含空格和特殊字符
- 示例：`leica-dlux8`、`fuji-x100-compare`
- 若下载失败（网络错误、403 等），重试最多 3 次

同时用 `yt-dlp --print title --print duration_string` 提取标题与时长，供后续写入 `index.json`。

---

## Step 2：安装依赖

仅首次运行需要，已安装则跳过：

```bash
which ffmpeg || brew install ffmpeg
python3 -c "import whisper" 2>/dev/null || pip3 install --user openai-whisper
export PATH="$PATH:/Users/chenzhiheng/Library/Python/3.9/bin:/opt/homebrew/bin"
```

---

## Step 3：Whisper 转录

```bash
export PATH="$PATH:/Users/chenzhiheng/Library/Python/3.9/bin:/opt/homebrew/bin"
cd ~/Projects/bilibili-workshop
whisper {slug}.m4a --model small --language Chinese --output_dir .
```

**模型选择**：

| 模型 | 中文质量 | 速度 | 适用 |
|------|---------|------|------|
| tiny | 一般 | 极快 | 快速预览 |
| **small** | 较好 | 中等 | **默认** |
| medium | 很好 | 慢 | 高质量需求 |

转录产物：`{slug}.txt` `{slug}.srt` `{slug}.vtt` `{slug}.json`。

---

## Step 4：读取转录稿并深度总结

读取 `{slug}.txt` 转录稿全文，按以下规则分析。

### 必须包含

1. **不罗列名词**：每张卡片回答「在讲什么 → 关键理解 → 与其他概念关系 → 怎么用 → 原文依据」
2. **行动清单**：可立刻执行的 3-5 件事
3. **避坑总结**：原文提到的陷阱/误区/不要做的事
4. **对比分析**：多概念/产品并列时做横向对比表
5. **方法边界**：每种方法/观点的适用上下限

### 视频特有处理

- **标注时间戳关键节点**（Outline 章节）：如 `[01:23] 开始介绍 D-Lux 8 优点`
- **UP 主观点**用 `.speaker` / `.card-purple` 标注
- **保留有争议的结论**，标注立场
- **提取关键金句**：用 `.quote` 样式框标注

---

## Step 5：生成 SVG

在仓库根目录创建 `generate-{slug}.mjs` 脚本。**必须使用 `svg-auto-height.mjs` 的 `buildSvg` 函数。**

### 脚本模板

```javascript
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { buildSvg } from './svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'docs', '{slug}-总结.svg');

const CSS = `/* 见下方完整 CSS */`;

const body = `<!-- 见下方 body 区模板 -->`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height, 'px');
```

### body 区模板

```html
<div class="container">

<h1>{视频标题}</h1>
<div class="meta">
  <span class="tag tag-blue">B站视频</span>
  <span class="tag tag-purple">{主题标签}</span>
  <span class="tag tag-orange">{时长}</span>
</div>
<div class="summary-line">{一句话概括}</div>

<div class="timeline">
  <h3>关键时间轴</h3>
  <div class="timeline-item">
    <span class="timeline-time">00:00</span>
    <span class="timeline-text">开场介绍</span>
  </div>
</div>

<div class="map">
  <h2>核心脉络</h2>
  <div class="diagram"><!-- 节点+箭头 --></div>
</div>

<div class="correction">
  <h3>⚠ 常见误解 / 认知纠偏</h3>
  <p>{纠偏内容}</p>
</div>

<div class="section">
  <h2 class="sec-title">{章节标题}</h2>
  <div class="card">...</div>
  <div class="card card-orange">⚠ 避坑</div>
  <div class="card card-purple">UP 主观点</div>
</div>

<div class="card">
  <h3>观点对比</h3>
  <table>...</table>
</div>

<div class="conclusion">
  <h2>总结与行动</h2>
  <h3>核心要点</h3>
  <ul>...</ul>
  <h3>行动清单</h3>
  <ol>...</ol>
  <h3>关键认知转变</h3>
  <p>以前认为…… 现在理解了……</p>
</div>

</div>
```

### 完整 CSS（必须使用）

```css
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#1e40af;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul,ol{padding-left:24px;margin:8px 0}
li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}
.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}
.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}
.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.timeline h3{color:#1e40af;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#3b82f6;min-width:70px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,0.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:20px 28px;text-align:center;min-width:160px;font-weight:700;font-size:16px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3{color:#92400e;margin-bottom:8px}
.correction p{color:#92400e;font-size:15px}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:16px;padding-left:16px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,0.06);border-left:5px solid #3b82f6}
.card.card-green{border-left-color:#10b981}
.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}
.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
.card .highlight{background:#fef3c7;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#92400e;border-left:4px solid #f59e0b}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#166534}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#991b1b;border-left:4px solid #ef4444}
.card .action{background:#eff6ff;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#1e40af;border-left:4px solid #3b82f6}
.card .insight{background:#eff6ff;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#1e40af;border-left:4px solid #3b82f6}
.speaker{display:inline-block;font-size:13px;font-weight:600;padding:2px 10px;border-radius:12px;margin-right:8px}
.speaker-host{background:#dbeafe;color:#1e40af}
.speaker-guest{background:#ede9fe;color:#6b21a8}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:700;color:#1e40af;border-bottom:2px solid #cbd5e1}
td{padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
tr:nth-child(even) td{background:#fafbfc}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,0.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,0.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,0.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
.key-data{display:inline-block;background:#1e40af;color:#fff;padding:2px 8px;border-radius:4px;font-size:13px;font-weight:700;margin-right:4px}
```

### 运行

```bash
node generate-{slug}.mjs
```

**Node 路径**：优先 `/Applications/Cursor.app/Contents/Resources/app/resources/helpers/node`。

### XML 避坑

- HTML 注释中禁止连续双连字符 `--`
- 文本中裸 `<` 必须转义为 `&lt;`
- `buildSvg` 已内置 `fixSvgXml()` 修复 `&` 和 `<br/>`

---

## Step 6：质量自检

- [ ] 每张卡片能回答「在讲什么、关键理解、怎么用」
- [ ] 至少包含 1 处落地建议（可执行的操作步骤）
- [ ] 至少包含 1 处避坑总结（不该做什么）
- [ ] 涉及多产品/方法时有选型/决策表
- [ ] 每个结论都说明了适用边界
- [ ] 文首有核心脉络关系图
- [ ] 结论区有三段式（总结 + 行动清单 + 认知转变）
- [ ] 有视频时间轴关键节点
- [ ] SVG 高度正常、XML 无错配标签

---

## Step 7：更新 index.json

读取 `docs/index.json`，将新总结追加到数组开头。

```json
{
  "date": "YYYY-MM-DD",
  "filename": "slug-总结.svg",
  "title": "视频标题",
  "summary": "一句话摘要，≤120字",
  "tags": ["数码", "相机"],
  "url": "https://www.bilibili.com/video/BVxxx",
  "duration": "5分40秒",
  "svg_height": 9560
}
```

**字段说明**：
- `date`：优先 Webhook payload 的 `date`；未提供则用当天日期
- `filename`：SVG 文件名（在 docs/ 目录下）
- `title`：视频标题
- `summary`：摘要（120 字内）
- `tags`：标签数组（2-4 个）
- `url`：原始 B 站链接
- `duration`：视频时长
- `svg_height`：SVG 高度像素值

若失败，记录失败项（含 `"error": true` 与 `error_message`）。

---

## Step 8：Git 提交与推送到 main（**必须**）

> **此步骤不可跳过。** GitHub Pages 从 `main` 分支的 `docs/` 目录部署。

```bash
git add docs/
git commit -m "bilibili: summarize {视频标题}"
git checkout main
git pull origin main
git push -u origin main
```

**要求：**
- 最终变更**必须**出现在 `origin/main` 上
- 禁止仅推送到 feature 分支就结束
- 推送前确认 `docs/index.json` 与 `docs/{slug}-总结.svg` 均已纳入提交

若 push 失败（冲突），先 `git pull --rebase origin main` 再 push。

---

## Step 9：清理

```bash
rm generate-{slug}.mjs
# 可选：rm {slug}.m4a
```

---

## 产出文件清单

| 文件 | 说明 |
|------|------|
| `{slug}.m4a` | 原始音频 |
| `{slug}.txt` | 纯文本转录稿 |
| `{slug}.srt` | SRT 字幕 |
| `{slug}.vtt` | WebVTT 字幕 |
| `{slug}.json` | Whisper JSON |
| `docs/{slug}-总结.svg` | 内容总结长图 |

---

## 约束

- 仅处理 B 站（bilibili.com / b23.tv）链接
- 不修改非 `docs/` 目录的文件（`generate-{slug}.mjs` 除外，用完删除）
- 不修改 `.gitignore`
- 每个 URL 只处理一次（检查 `index.json` 中是否已存在相同 `url`）
- 严禁使用 `rsvg-convert` 或 Inkscape 渲染 SVG
- **必须将产出推送到 `main` 分支**，否则 GitHub Pages 无法展示
