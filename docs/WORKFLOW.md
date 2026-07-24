# B 站视频 → HTML 自动化工作流

当 Cursor Automation 通过 Webhook 收到 B 站视频链接后，严格按本文档逐步骤执行。**不要跳过或合并任何步骤。**

```
Task Progress:
- [ ] 1. yt-dlp 获取元数据并下载音频、视频
- [ ] 2. 安装依赖（ffmpeg + openai-whisper，仅首次）
- [ ] 3. Whisper 转录（--model small --language Chinese）
- [ ] 4. 读取完整转录并深度总结
- [ ] 5. 从视频提取关键截图
- [ ] 6. 生成包含完整转录与截图的 HTML
- [ ] 7. 质量自检
- [ ] 8. 更新 docs/index.json
- [ ] 9. Git 提交并推送
- [ ] 10. 清理临时文件
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
| `url` | 是 | B 站视频链接（`bilibili.com` 或 `b23.tv`） |
| `date` | 否 | 前端展示日期，格式 `YYYY-MM-DD`；未提供时使用当天日期 |

从 payload 中提取 `url`。字段缺失、为空或域名不符合约束时，记录错误并结束。开始下载前检查 `docs/index.json`，相同 `url` 已存在则直接结束，避免重复处理。

---

## Step 1：获取元数据并下载音频、视频

先获取标题、时长和视频 ID，再按标题生成 `{slug}`：

```bash
cd ~/Projects/bilibili-workshop
yt-dlp --print title --print duration_string --print id "{url}"
```

`{slug}` 规则：

- 从标题提取英文或核心关键词拼音，≤30 字符
- 只允许小写字母、数字和连字符
- 若名称冲突，追加数字后缀

下载用于 Whisper 的最佳音频：

```bash
yt-dlp -f "bestaudio[ext=m4a]/bestaudio/best" \
  -o "{slug}.%(ext)s" "{url}"
```

下载用于截图的视频画面；无需音轨，限制到 1080p 以内：

```bash
yt-dlp -f "bestvideo[height<=1080][ext=mp4]/bestvideo[height<=1080]/best[height<=1080]" \
  -o "{slug}.source.%(ext)s" "{url}"
```

任一下载因网络、403 等临时错误失败时，最多重试 3 次。实际扩展名可能不是 `m4a` 或 `mp4`，后续命令必须使用磁盘上的真实文件名。

---

## Step 2：安装依赖

仅首次运行需要，已安装则跳过：

```bash
command -v ffmpeg >/dev/null || brew install ffmpeg
python3 -c "import whisper" 2>/dev/null || pip3 install --user openai-whisper
```

确保 `yt-dlp`、`ffmpeg`、`ffprobe`、`whisper` 和 `node` 均可执行。

---

## Step 3：Whisper 转录

```bash
cd ~/Projects/bilibili-workshop
whisper "{音频文件}" --model small --language Chinese --output_dir .
```

转录产物为 `{slug}.txt`、`{slug}.srt`、`{slug}.vtt`、`{slug}.tsv` 和 `{slug}.json`。后续必须读取 JSON 中的 `segments`，因为 HTML 的详细转录区需要逐段时间戳。

不得用摘要替代转录。每个非空 segment 都必须出现在最终 HTML 中，保持原顺序和对应时间；听不清的内容标记为 `[听不清]`，不得凭空补写。

---

## Step 4：读取完整转录并深度总结

读取 `{slug}.txt` 全文，并结合 `{slug}.json` 的时间分段分析。

### 总结必须包含

1. **核心脉络**：说明内容如何从问题推进到观点和结论
2. **主题拆解**：每节回答「在讲什么 → 关键理解 → 怎么用 → 原文依据」
3. **行动清单**：3-5 项可立即执行的具体操作
4. **避坑总结**：原文提到的陷阱、误区或不要做的事
5. **对比分析**：涉及多概念、产品或方法时提供横向对比表
6. **方法边界**：说明每种观点的适用条件、上限和例外

### 视频特有处理

- 标注关键节点时间戳，例如 `[01:23] 开始介绍 D-Lux 8 优点`
- UP 主观点用 `.speaker` 或 `.card-purple` 标注
- 有争议的结论保留原立场，不包装成客观事实
- 关键原话放入 `.quote`，并标注对应时间
- 从总结中列出 3-8 个候选截图时间点，说明每张图要佐证的内容

### 总结与转录的边界

- 总结区允许提炼和重组，但必须能回溯到时间戳
- 转录区必须完整，不删除重复、口语或与总结无关的段落
- 可修正明显标点，但不得悄悄改写说话人的意思

---

## Step 5：提取关键截图

截图用于补充无法仅靠文字表达的界面、产品细节、图表、操作步骤或前后对比，不得只截 UP 主头像、转场、黑帧或模糊画面。

创建资源目录：

```bash
mkdir -p "docs/assets/{slug}"
```

按 Step 4 选定的时间点逐张提取：

```bash
ffmpeg -ss "HH:MM:SS.mmm" -i "{视频文件}" -frames:v 1 \
  -vf "scale='min(1280,iw)':-2" -q:v 2 \
  "docs/assets/{slug}/shot-01.jpg"
```

截图要求：

- 一般视频提取 3-8 张；每张必须对应一个关键观点
- 静态画面或纯音频视频至少保留 1 张代表画面，并在图注中说明画面长期不变
- 文件按内容顺序命名为 `shot-01.jpg`、`shot-02.jpg`……
- 打开并检查每张图，若黑屏、模糊、字幕遮挡重点或处于转场，前后微调 0.5-2 秒重新截取
- 不使用 B 站远程图片地址，不将图片转为 base64；图片必须随 HTML 一起提交

---

## Step 6：生成 HTML

在仓库根目录临时创建 `generate-{slug}.mjs`，输出 `docs/{slug}-总结.html`。HTML 必须是独立、可直接打开的响应式页面，不依赖构建工具或远程 CSS/JavaScript。

### 脚本骨架

```javascript
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, 'docs', '{slug}-总结.html');
const whisper = JSON.parse(
  fs.readFileSync(path.join(DIR, '{slug}.json'), 'utf8')
);

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

const CSS = `/* 使用下方样式规范，并包含响应式规则 */`;
const summaryBody = `<!-- 深度总结、时间轴、卡片、对比表、截图与结论 -->`;

const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{一句话摘要}">
  <title>{视频标题}｜视频总结</title>
  <style>${CSS}</style>
</head>
<body>
  <main class="container">
    ${summaryBody}
    <section class="section transcript-section" id="transcript">
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

### 页面结构

```html
<main class="container">
  <header><!-- 标题、标签、一句话摘要、原视频链接 --></header>
  <nav class="toc"><!-- 总结、截图、详细转录的页内链接 --></nav>
  <section class="timeline"><!-- 关键时间轴 --></section>
  <section class="map"><!-- 核心脉络 --></section>
  <section class="section"><!-- 主题卡片、观点、避坑、对比 --></section>
  <section class="visual-evidence">
    <h2>关键画面</h2>
    <figure>
      <img src="assets/{slug}/shot-01.jpg"
           alt="{准确描述画面中的关键信息}"
           loading="lazy">
      <figcaption>[01:23] {画面内容及其支持的观点}</figcaption>
    </figure>
  </section>
  <section class="conclusion"><!-- 核心要点、行动清单、认知转变 --></section>
  <section class="transcript-section" id="transcript"><!-- 全部分段 --></section>
</main>
```

### 样式规范

沿用原有卡片语义，并增加 HTML 阅读所需样式：

- `.card`：通用概念；`.card-purple`：UP 主观点
- `.card-orange`：避坑；`.card-green`：正面经验；`.card-red`：严重问题
- `.quote`：原话；`.speaker`：说话人；`.conclusion`：三段式结论
- `.visual-evidence`、`figure`、`figcaption`：截图与带时间戳图注
- `.transcript-list`、`.transcript-row`：完整转录

必须包含以下基础规则，其余视觉样式可参考首页：

```css
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.75;color:#1e293b;background:#f8fafc}
.container{width:min(1120px,100%);margin:0 auto;padding:48px 32px 80px}
img{display:block;max-width:100%;height:auto}
figure{margin:24px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(15,23,42,.08)}
figcaption{padding:14px 18px;color:#475569}
.transcript-list{list-style:none;padding:0}
.transcript-row{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e2e8f0}
.transcript-row time{font-variant-numeric:tabular-nums;color:#2563eb;font-weight:700}
.transcript-row p{margin:0}
@media(max-width:640px){
  .container{padding:28px 18px 56px}
  .transcript-row{grid-template-columns:56px 1fr;gap:10px}
}
```

### 安全与可访问性

- 从视频元数据、转录或 payload 插入的纯文本必须经过 `escapeHtml`
- 每张截图必须提供描述信息的 `alt`，图注必须包含时间戳
- 页面必须有且仅有一个 `h1`，标题层级不得跳级
- 不加载远程脚本、跟踪代码或第三方字体
- 不设置固定页面高度；由浏览器自然滚动

运行：

```bash
node "generate-{slug}.mjs"
```

---

## Step 7：质量自检

- [ ] HTML 包含完整的 `<!DOCTYPE html>`、`lang="zh-CN"` 和 viewport
- [ ] Whisper JSON 中每个非空 segment 都出现在详细转录区，顺序与时间戳一致
- [ ] 每张总结卡片能回答「在讲什么、关键理解、怎么用、原文依据」
- [ ] 至少有 1 处行动清单和 1 处避坑总结
- [ ] 涉及多产品或方法时有对比表
- [ ] 每个结论都说明适用边界
- [ ] 文首有核心脉络和关键时间轴
- [ ] 结论区包含「总结 + 行动清单 + 认知转变」
- [ ] 一般视频有 3-8 张有效截图；每张图片存在、可打开、带准确 alt 和时间戳图注
- [ ] 桌面端和 375px 宽度下均无横向溢出，表格可横向滚动
- [ ] 所有本地图片链接、页内锚点和原视频链接有效

可用浏览器打开产出文件进行最终人工检查；禁止只检查源码后直接发布。

---

## Step 8：更新 index.json

读取 `docs/index.json`，将新条目插入数组开头：

```json
{
  "date": "YYYY-MM-DD",
  "filename": "slug-总结.html",
  "format": "html",
  "title": "视频标题",
  "summary": "一句话摘要，≤120字",
  "tags": ["数码", "相机"],
  "url": "https://www.bilibili.com/video/BVxxx",
  "duration": "5分40秒",
  "screenshot_count": 5,
  "transcript_segments": 86
}
```

字段要求：

- `date`：优先使用 payload 的 `date`，否则使用当天日期
- `filename`：位于 `docs/` 的 HTML 文件名
- `format`：固定为 `html`
- `summary`：不超过 120 个汉字
- `tags`：根据内容提取 2-4 个
- `screenshot_count`：实际提交的截图数
- `transcript_segments`：HTML 中实际呈现的非空 Whisper 分段数

失败时写入包含 `"error": true` 和 `error_message` 的失败条目，不写虚假的成功数据。

---

## Step 9：Git 提交与推送

GitHub Pages 从目标发布分支的 `docs/` 目录部署。提交前确认以下文件均已纳入：

- `docs/{slug}-总结.html`
- `docs/assets/{slug}/shot-*.jpg`
- `docs/index.json`

```bash
git add "docs/{slug}-总结.html" "docs/assets/{slug}" docs/index.json
git commit -m "bilibili: summarize {视频标题} as HTML"
git push -u origin "{目标分支}"
```

若推送因网络问题失败，按 4、8、16、32 秒退避重试。若因冲突失败，拉取目标分支并 rebase，解决冲突、重新自检后再推送。

---

## Step 10：清理

确认 HTML、截图和索引已提交后，删除生成脚本与本地大文件：

```bash
rm "generate-{slug}.mjs"
rm -f "{音频文件}" "{视频文件}"
```

转录中间文件可按调试需要保留；它们不提交到仓库，因为完整分段已经嵌入 HTML。

---

## 文件清单

### 发布文件

| 文件 | 说明 |
|------|------|
| `docs/{slug}-总结.html` | 深度总结、关键截图和完整转录页面 |
| `docs/assets/{slug}/shot-*.jpg` | 关键画面截图 |
| `docs/index.json` | Pages 内容索引 |

### 临时文件

| 文件 | 说明 |
|------|------|
| `{slug}.m4a` 或其他音频格式 | Whisper 输入 |
| `{slug}.source.*` | 截图用视频 |
| `{slug}.txt/.srt/.vtt/.tsv/.json` | Whisper 转录产物 |
| `generate-{slug}.mjs` | 一次性 HTML 生成脚本 |

---

## 约束

- 仅处理 `bilibili.com` 或 `b23.tv` 链接
- 每个 URL 只处理一次
- 新内容只发布为 HTML，不生成 SVG、Canvas 长图或图片化全文
- 完整转录必须直接出现在 HTML 中，不能只提供下载链接
- 截图只能来自所处理的视频，并作为本地资源提交
- 除临时生成脚本外，自动化产出只写入 `docs/`
