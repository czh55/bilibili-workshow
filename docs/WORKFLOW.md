# B 站视频 → HTML + SVG 双轨自动化工作流

当 Cursor Automation 通过 Webhook 收到 B 站视频链接后，严格按本文档逐步骤执行。**一个视频必须同时产出两种互补内容，不得只生成其中一种。**

| 产物 | 视角 | 目标 |
|------|------|------|
| HTML 图文实录 | 轻松、纪实、按时间展开 | 保留原始内容、关键画面和完整转录，让读者像重看视频一样阅读 |
| SVG 理性分析 | 客观、结构化、跨章节重组 | 提炼论点、证据、关系、对比、适用边界和行动结论 |

HTML 不是 SVG 的加长版，SVG 也不是 HTML 的缩略图。二者共享同一份视频与转录证据，但承担不同阅读任务。

```
Task Progress:
- [ ] 1. yt-dlp 获取元数据并下载音频、视频
- [ ] 2. 安装依赖（ffmpeg + openai-whisper，仅首次）
- [ ] 3. Whisper 转录（--model small --language Chinese）
- [ ] 4. 基于同一转录进行双轨编辑
- [ ] 5. 从视频提取 HTML 所需关键截图
- [ ] 6. 生成 HTML 图文实录
- [ ] 7. 生成 SVG 理性分析
- [ ] 8. 双产物质量自检
- [ ] 9. 更新 docs/index.json
- [ ] 10. Git 提交并推送
- [ ] 11. 清理临时文件
```

---

## 入口

Webhook payload：

```json
{
  "url": "https://www.bilibili.com/video/BVxxx",
  "date": "2026-07-24"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `url` | 是 | B 站链接，仅允许 `bilibili.com` 或 `b23.tv` |
| `date` | 否 | 展示日期，格式 `YYYY-MM-DD`；未提供时使用当天日期 |

字段缺失、为空或域名不符合约束时，记录错误并结束。下载前检查 `docs/index.json`，相同 `url` 已存在则结束，避免重复处理。

---

## Step 1：获取元数据并下载音频、视频

```bash
cd ~/Projects/bilibili-workshop
yt-dlp --print title --print duration_string --print id "{url}"
```

根据标题生成 `{slug}`：

- 提取英文或核心关键词拼音，≤30 字符
- 只允许小写字母、数字和连字符
- 若冲突则追加数字后缀

下载 Whisper 音频：

```bash
yt-dlp -f "bestaudio[ext=m4a]/bestaudio/best" \
  -o "{slug}.%(ext)s" "{url}"
```

下载 1080p 以内的视频画面用于截图：

```bash
yt-dlp -f "bestvideo[height<=1080][ext=mp4]/bestvideo[height<=1080]/best[height<=1080]" \
  -o "{slug}.source.%(ext)s" "{url}"
```

临时网络或 403 错误最多重试 3 次。后续命令使用磁盘上的真实文件名，不假定扩展名。

---

## Step 2：安装依赖

仅首次运行需要：

```bash
command -v ffmpeg >/dev/null || brew install ffmpeg
python3 -c "import whisper" 2>/dev/null || pip3 install --user openai-whisper
```

确认 `yt-dlp`、`ffmpeg`、`ffprobe`、`whisper` 和 `node` 均可执行。

---

## Step 3：Whisper 转录

```bash
whisper "{音频文件}" --model small --language Chinese --output_dir .
```

产物为 `{slug}.txt`、`{slug}.srt`、`{slug}.vtt`、`{slug}.tsv` 和 `{slug}.json`。

必须保留 JSON 中所有非空 `segments` 及其起止时间。听不清的内容标记为 `[听不清]`，不得凭空补写。HTML 逐段呈现完整转录；SVG 的每个主要结论必须能回溯到这些分段。

---

## Step 4：基于同一转录进行双轨编辑

完整阅读 `{slug}.txt` 和 `{slug}.json` 后，分别准备两套内容。不得先写一份摘要，再机械复制到两个格式中。

### A. HTML 图文实录：按视频发生顺序展开

写作语气自然、轻松、偏纪实，保留视频的推进感：

1. **开场背景**：UP 主为什么谈这个主题，当时面对什么场景
2. **章节实录**：按时间顺序讲清每一段发生了什么
3. **人物与语气**：区分说话人；争议观点明确标注为个人立场
4. **关键画面**：把界面、产品、图表、操作或对比截图放在对应叙述旁
5. **完整转录**：页面末尾逐段呈现全部非空 Whisper segments 和时间戳

HTML 可以解释必要背景，但不应把叙事切碎成大量分析卡片。它回答的是：“视频具体说了什么、展示了什么、前后如何发展？”

### B. SVG 理性分析：跨时间重组观点

打散原视频顺序，按概念和论证关系重新组织：

1. **核心命题**：视频真正试图回答的问题
2. **核心脉络图**：问题、判断、证据、结论之间的关系
3. **观点卡片**：每张回答「在讲什么 → 关键理解 → 怎么用 → 原文依据」
4. **行动清单**：3-5 项可以立即执行的操作
5. **避坑总结**：陷阱、误区和不要做的事
6. **横向对比**：多产品、方法或观点并列时必须做表格
7. **方法边界**：说明结论适用条件、上限、反例和例外
8. **立场分层**：明确区分可验证事实、UP 主观点和基于原文的推断

SVG 应信息密度高、措辞克制，不把 UP 主的主观判断写成客观事实。它回答的是：“这些内容之间是什么关系，证据是否支撑结论，读者应如何决策？”

### 共同证据规则

- 两个产物都标注关键时间戳
- 关键原话必须忠于转录，用 `.quote` 标注
- 有争议的结论保留原立场并说明证据强弱
- 不补充视频未表达的事实；必要的外部背景必须明确标为“补充资料”
- 同一个结论在 HTML 与 SVG 中不得互相矛盾

---

## Step 5：提取 HTML 关键截图

截图用于补充文字难以表达的界面、产品细节、图表、操作步骤和前后对比，不用于装饰。

```bash
mkdir -p "docs/assets/{slug}"
ffmpeg -ss "HH:MM:SS.mmm" -i "{视频文件}" -frames:v 1 \
  -vf "scale='min(1280,iw)':-2" -q:v 2 \
  "docs/assets/{slug}/shot-01.jpg"
```

要求：

- 一般视频 3-8 张，每张对应一个内容节点
- 静态或纯音频视频至少保留 1 张代表画面，并在图注说明画面长期不变
- 文件按顺序命名为 `shot-01.jpg`、`shot-02.jpg`……
- 检查黑屏、模糊、转场和字幕遮挡，必要时前后微调 0.5-2 秒
- 使用本地相对路径，不引用 B 站远程图片，不嵌入 base64
- 每张图必须有准确 `alt` 和带时间戳的 `figcaption`

---

## Step 6：生成 HTML 图文实录

创建临时脚本 `generate-{slug}-html.mjs`，输出 `docs/{slug}-图文实录.html`。页面必须独立、响应式，不依赖远程 CSS、JavaScript 或字体。

### 转录渲染骨架

```javascript
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'docs', '{slug}-图文实录.html');
const whisper = JSON.parse(fs.readFileSync(path.join(DIR, '{slug}.json'), 'utf8'));

function escapeHtml(value) {
  return String(value ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function timestamp(seconds) {
  const total = Math.max(0, Math.floor(Number(seconds) || 0));
  const hours = Math.floor(total / 3600);
  const minutes = Math.floor((total % 3600) / 60);
  const secs = total % 60;
  return hours
    ? `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`
    : `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
}

const segments = (whisper.segments || []).filter(
  segment => String(segment.text || '').trim()
);

const transcript = segments.map((segment, index) => `
  <li class="transcript-row" id="transcript-${index + 1}">
    <time datetime="PT${Math.floor(segment.start || 0)}S">${timestamp(segment.start)}</time>
    <p>${escapeHtml(segment.text.trim())}</p>
  </li>
`).join('');

const CSS = `/* 完整页面样式 */`;
const documentaryBody = `<!-- 按时间展开的图文实录 -->`;

const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{一句话纪实摘要}">
  <title>{视频标题}｜图文实录</title>
  <style>${CSS}</style>
</head>
<body>
  <main class="container">
    ${documentaryBody}
    <section class="transcript-section" id="transcript">
      <h2>详细文字转录</h2>
      <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差。</p>
      <ol class="transcript-list">${transcript}</ol>
    </section>
  </main>
</body>
</html>`;

fs.writeFileSync(OUT, html, 'utf8');
console.log('Generated:', OUT, 'segments:', segments.length);
```

### HTML 页面结构

```html
<main class="container">
  <header><!-- 标题、元数据、纪实导语、原视频链接 --></header>
  <nav class="toc"><!-- 时间章节、关键画面、完整转录 --></nav>
  <article class="documentary">
    <section class="story-section"><!-- 按时间推进的叙述 --></section>
    <figure>
      <img src="assets/{slug}/shot-01.jpg" alt="{准确描述}" loading="lazy">
      <figcaption>[01:23] {画面内容及上下文}</figcaption>
    </figure>
  </article>
  <section class="transcript-section"><!-- 全部分段 --></section>
</main>
```

### HTML 基础样式

```css
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}
.container{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}
.documentary{font-size:17px}
.story-section{margin:48px 0}
img{display:block;max-width:100%;height:auto}
figure{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}
figcaption{padding:14px 18px;color:#57534e}
.transcript-list{list-style:none;padding:0}
.transcript-row{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}
.transcript-row time{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}
.transcript-row p{margin:0}
@media(max-width:640px){
  .container{padding:28px 18px 56px}
  .transcript-row{grid-template-columns:56px 1fr;gap:10px}
}
```

运行：

```bash
node "generate-{slug}-html.mjs"
```

---

## Step 7：生成 SVG 理性分析

创建临时脚本 `generate-{slug}-svg.mjs`，必须调用仓库中的 `svg-auto-height.mjs`，输出 `docs/{slug}-理性分析.svg`。

### SVG 脚本骨架

```javascript
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from './svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'docs', '{slug}-理性分析.svg');
const CSS = `/* 使用下方完整 SVG CSS */`;
const body = `<!-- 使用下方分析框架 -->`;

const { svg, height } = await buildSvg({ css: CSS, body, width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated:', OUT, 'height:', height);
```

### SVG 分析框架

```html
<div class="container">
  <h1>{视频标题}</h1>
  <div class="meta"><!-- 标签、时长、分析视角 --></div>
  <div class="summary-line">{一句话核心判断}</div>
  <div class="timeline"><!-- 关键证据时间轴 --></div>

  <div class="map">
    <h2>核心脉络</h2>
    <div class="diagram"><!-- 问题 → 证据 → 判断 → 行动 --></div>
  </div>

  <div class="correction"><!-- 常见误解与认知纠偏 --></div>

  <div class="section">
    <h2 class="sec-title">{分析主题}</h2>
    <div class="card"><!-- 通用概念与证据 --></div>
    <div class="card card-purple"><!-- UP 主观点，明确立场 --></div>
    <div class="card card-orange"><!-- 风险和避坑 --></div>
  </div>

  <div class="card"><table><!-- 横向比较与选择条件 --></table></div>

  <div class="conclusion">
    <h2>总结与行动</h2>
    <h3>核心要点</h3>
    <h3>行动清单</h3>
    <h3>关键认知转变</h3>
  </div>
</div>
```

### 完整 SVG CSS

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
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline h3{color:#1e40af;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#3b82f6;min-width:70px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:20px 28px;text-align:center;min-width:160px;font-weight:700;font-size:16px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3,.correction p{color:#92400e}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:16px;padding-left:16px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #3b82f6}
.card.card-green{border-left-color:#10b981}
.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}
.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card .highlight{background:#fef3c7;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#92400e;border-left:4px solid #f59e0b}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#166534}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#991b1b;border-left:4px solid #ef4444}
.card .action,.card .insight{background:#eff6ff;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#1e40af;border-left:4px solid #3b82f6}
.speaker{display:inline-block;font-size:13px;font-weight:600;padding:2px 10px;border-radius:12px;margin-right:8px}
.speaker-host{background:#dbeafe;color:#1e40af}
.speaker-guest{background:#ede9fe;color:#6b21a8}
table{width:100%;border-collapse:collapse;margin:16px 0;font-size:15px}
th{background:#f1f5f9;padding:12px 16px;text-align:left;font-weight:700;color:#1e40af;border-bottom:2px solid #cbd5e1}
td{padding:12px 16px;border-bottom:1px solid #e2e8f0;color:#475569;vertical-align:top}
tr:nth-child(even) td{background:#fafbfc}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
.key-data{display:inline-block;background:#1e40af;color:#fff;padding:2px 8px;border-radius:4px;font-size:13px;font-weight:700;margin-right:4px}
```

运行：

```bash
node "generate-{slug}-svg.mjs"
```

XML 注意事项：

- HTML 注释中禁止连续双连字符
- 文本中的裸 `<` 必须写为 `&lt;`
- `buildSvg()` 会修复裸 `&` 和 `<br/>`，但生成后仍需 XML 解析检查

---

## Step 8：双产物质量自检

### HTML 图文实录

- [ ] 包含 `<!DOCTYPE html>`、`lang="zh-CN"` 和 viewport
- [ ] 所有非空 Whisper segments 均按原顺序和时间戳出现
- [ ] 内容主要按视频时间顺序展开，语气自然，不写成分析卡片堆叠
- [ ] 一般视频有 3-8 张有效截图，每张都有准确 alt 和时间戳图注
- [ ] 桌面端与 375px 宽度均无横向溢出
- [ ] 所有图片、页内锚点和原视频链接有效

### SVG 理性分析

- [ ] 每张卡片说明内容、理解、用法和原文依据
- [ ] 有核心脉络图、关键证据时间轴、行动清单与避坑总结
- [ ] 多产品或方法并列时有对比表
- [ ] 每个结论说明适用边界，并区分事实、观点和推断
- [ ] 结论区包含核心要点、行动清单和认知转变
- [ ] SVG 高度正常，可通过 XML 解析，无错配标签和内容截断

### 成对一致性

- [ ] 两个产物标题、视频来源、时长和关键事实一致
- [ ] HTML 保留过程，SVG 重组关系，二者没有大段机械重复
- [ ] 同一观点没有相互矛盾的归因、数字或结论
- [ ] 两个文件均生成成功后，才写入成功的索引条目

---

## Step 9：更新 index.json

一个视频只写一条记录，两个入口放在 `outputs` 中：

```json
{
  "date": "YYYY-MM-DD",
  "title": "视频标题",
  "summary": "一句话摘要，≤120字",
  "tags": ["数码", "相机"],
  "url": "https://www.bilibili.com/video/BVxxx",
  "duration": "5分40秒",
  "outputs": {
    "html": "slug-图文实录.html",
    "svg": "slug-理性分析.svg"
  },
  "screenshot_count": 5,
  "transcript_segments": 86,
  "svg_height": 9560
}
```

- `outputs.html`：轻松纪实、含截图与完整转录的 HTML
- `outputs.svg`：客观结构化分析 SVG
- `screenshot_count`：实际提交的截图数
- `transcript_segments`：HTML 呈现的非空 Whisper 分段数
- `svg_height`：`buildSvg()` 返回的最终高度

首页必须在同一卡片中展示“图文实录”和“理性分析”两个入口。失败时写入含 `"error": true` 和 `error_message` 的条目；缺少任一产物均视为失败。

---

## Step 10：Git 提交与推送

提交前确认：

- `docs/{slug}-图文实录.html`
- `docs/{slug}-理性分析.svg`
- `docs/assets/{slug}/shot-*.jpg`
- `docs/index.json`

```bash
git add "docs/{slug}-图文实录.html" "docs/{slug}-理性分析.svg" \
  "docs/assets/{slug}" docs/index.json
git commit -m "bilibili: add dual-view summary for {视频标题}"
git push -u origin "{目标分支}"
```

网络失败按 4、8、16、32 秒退避重试；冲突时 rebase、解决冲突并重新自检。

---

## Step 11：清理

```bash
rm "generate-{slug}-html.mjs" "generate-{slug}-svg.mjs"
rm -f "{音频文件}" "{视频文件}"
```

转录中间文件可按调试需要保留，但不提交到仓库。

---

## 约束

- 仅处理 `bilibili.com` 或 `b23.tv`
- 每个 URL 只处理一次，一个索引条目对应两个产物
- HTML 必须包含本地关键截图和完整时间戳转录
- SVG 必须使用 `svg-auto-height.mjs` 和原有分析视觉框架
- 不使用 `rsvg-convert` 或 Inkscape 渲染 SVG
- 自动化产出只写入 `docs/`；临时生成脚本除外
