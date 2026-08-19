# 视频（B 站 / 小红书）→ HTML + SVG 双轨自动化工作流

当 Cursor Automation 通过 Webhook 收到视频链接后，严格按本文档逐步骤执行。**先自动识别平台，再下载与双轨生成；一个视频必须同时产出两种互补内容，不得只生成其中一种。**

| 产物 | 视角 | 目标 |
|------|------|------|
| HTML 图文实录 | 轻松、纪实、按时间展开 | 保留原始内容、关键画面和完整转录，让读者像重看视频一样阅读 |
| SVG 理性分析 | 客观、结构化、跨章节重组 | 提炼论点、证据、关系、对比、适用边界和行动结论 |

HTML 不是 SVG 的加长版，SVG 也不是 HTML 的缩略图。二者共享同一份视频与转录证据，但承担不同阅读任务。

## 不可妥协的发布标准

### 简体中文

- 所有面向读者的编辑内容必须使用**简体中文**：标题、导语、章节标题、内容要点、图注、`index.json` 摘要、SVG 文案、标签与错误说明均包括在内。
- 图注的中文行是主文案；英文翻译行（`.cap-en`）只是朗读辅助，**不得替代中文图注**，也不得把整段正文替换为英文。
- 不得直接把繁体中文、粤语转写、英文 Whisper 片段或机械直译作为摘要、章节叙述或结论发布。原始转录是证据，可保留原语言；若在正文引用非简体中文原话，必须紧随简体中文释义。
- 生成后用 OpenCC（繁体转简体）或等效工具检查编辑文案；同时人工抽查标题、导语、每个章节标题和每张卡片。转换后仍须通读，避免把专有名词、术语或引用误改。

### 内容完整性与模型选择

- 不得使用低能力或“省钱”模型直接产出可发布的摘要、章节叙述或 SVG 分析。模型能力不足时，宁可保留草稿、标记待人工整理，也不得发布残缺内容、关键词拼贴、空泛套话或未完成句子。
- 编辑前必须完整读取转录 JSON 的全部非空 `segments`；不能只依据标题、前 30 秒、截图或截断的 `.txt` 文件写作。
- 优先参照已发布的优质样例 [`absurd-wuxia-cinematography-图文实录.html`](absurd-wuxia-cinematography-图文实录.html)：它以有信息量的导语、完整时间线章节、准确截图图注、可追溯引文和完整转录共同构成文章。新文章无需复制其措辞或视觉风格，但必须达到同等的叙事完整度。
- 禁止发布以下内容：`要点详解` 等泛化标题反复出现、仅罗列关键词、以 `...`/`…` 截断的摘要、无上下文的原文碎片、把“视频围绕相关技巧展开”等模板句当作内容。

### 完整版 / 增强版 HTML（内容极其丰富的视频）

当用户要求对既有文章“出非常完整的版本”“每个模特/每个演示都要有”时，适用下列增强版规则（与常规版互补，常规版规则仍全部有效）：

- **增强版不等于放宽标准**：图注仍必须中英对照（`.cap-bilingual`）+ 朗读音频（见「图注双语与朗读音频（强制）」），必须运行 `scripts/gen-caption-audio.py`（在增强前）与 `scripts/enhance-captions-html.py`（在增强后）。
- **截图数量可以突破 3–8 张常规上限**：增强版按知识点配图，可到 15–20 张甚至更多；每张仍须有准确 `alt` 和带时间戳的图注。文件名可用语义化命名（如 `pose-foot-circle.jpg`、`pose-squat-back.jpg`）而非强制 `shot-NN.jpg`，但要整篇统一。
- **“大屏幕/示例照片”时刻优先配图**：教学类视频常以“请看大屏幕”展示示例照片，这些时刻是最高价值的配图素材。用 `ffmpeg -ss` 精确定位大屏幕展示瞬间并抽取全尺寸帧；配图应选画面中照片/演示内容清晰、构图完整的帧。
- **中间帧与拼图是过程文件，不进仓库**：预览帧、密集抽帧、拼图网格（`_work/` 下所有产物）都只用于选图，不得提交；最终只提交精选后的 `docs/assets/{slug}/` 图片。
- **增强版发布后必须同步 `index.json`**：`screenshot_count` 更新为实际提交的截图数，`transcript_segments` 如有变化同步更新。
- **生成脚本保留规则**：增强版专用的构建脚本（如 `build-{slug}-html.py`）可保留在仓库根目录或 `scripts/`，但必须在文档或脚本注释中说明用途；若是一次性脚本，任务结束即清理（见 Step 11）。
- **figcaption 格式必须与全站统一**：图注一律写成 `<figcaption>[MM:SS] 中文图注</figcaption>` 的单时间戳形式，**不要**使用 `<span class="time-badge">[MM:SS]</span>[MM:SS] …` 的重复时间戳写法。否则 `extract-captions.py` / `gen-caption-audio.py` / `enhance-captions-html.py` 提取出的翻译 key 会带 `[MM:SS]` 前缀，无法命中 `translations.json` 的纯中文 key，导致图注无法增强。

### 小红书访问限流

- 对 `xiaohongshu.com`、`xhslink.cn`、`xhslink.com` 的**任何网络请求**（含短链解析、元数据读取、下载、重试）实行全局限流：两次请求的开始时间必须相隔至少 **60 秒**。
- 一个视频的元数据和下载必须合并为一次下载调用，禁止先探测、再分别请求音频和视频。不得使用 `HEAD`、额外探测或并发请求。默认使用新方式 `python3 scripts/xhs-fetch.py`（脚本内部已执行限流、短链展开、页面解析并产出 meta.json）；若新方式失效，可退回备选方式：执行 `node xhs-rate-limit.mjs` 后单次 `yt-dlp -f "best[height<=1080]/best"` 下载混合文件。
- 出现 403、412、429、网络错误或下载失败时，不得立即重试；每次重试同样等待至少 60 秒，最多 3 次。达到上限后记录失败并停止。
- 修复既有小红书文章时，优先且默认只使用仓库中已有的 HTML、截图、SVG 和本地转录；**不得**为润色、补全、转简体或重建摘要重新访问小红书。只有本地源文件确实缺失、且用户明确要求重新抓取时，才可按上述限流规则单独排队。
- **限流器锁文件死锁恢复（2026-08 b45 批次实战）**：`xhs-rate-limit.mjs` 用 `os.tmpdir()` 下的 `bilibili-workshop-xhs-last-request*` 状态/锁文件串行化请求。进程被中断（Ctrl-C、超时 kill、沙箱终止）会留下孤儿锁文件，导致后续请求被误判为“间隔不足”而无限等待。症状：脚本长时间停留在「等待 N 秒」不前进。恢复：先 `pkill -f xhs-fetch.py; pkill -f xhs-rate-limit`，再删除锁文件 `rm -f "$(node -e 'console.log(require("os").tmpdir())')"/bilibili-workshop-xhs-last-request*` 后重试。

### 执行环境网络权限（沙箱限制，2026-08 b49 批次实战）

**凡是需要访问小红书/B 站/任意非白名单域名的命令，都必须显式请求 `full_network` 权限再执行；后台化（`block_until_ms: 0`）的命令尤其容易落入受限沙箱。** 沙箱默认只放行常见包管理域名（npm/pypi/github 等），对 `xiaohongshu.com`、`xhslink.cn` 的 `curl` 请求会被拦截或返回不完整页面。

- **典型症状**：`xhs-fetch.py` 报「页面中未找到 __INITIAL_STATE__」，反复重试 3 次仍失败，但用相同命令在前台手动执行却成功——这几乎可以确定是沙箱网络限制，而不是链接失效或小红书反爬。
- **正确做法**：下载类命令（`xhs-fetch.py`、`yt-dlp`、`curl` 抓页面、B 站 API）一律用 `required_permissions: ["full_network"]` 启动；批量下载脚本建议用 `block_until_ms: 0` 后台化 + `full_network` 权限，并用输出匹配（`=== 完成 cNN` / `全部下载流程结束`）监听进度。
- **快速自检**：失败后不要盲目重试。先手动跑一次确认链路：
  ```bash
  curl -s -L -A "$UA" -H "Referer: https://www.xiaohongshu.com/" \
    "https://xhslink.cn/o/xxxxxx" -o /tmp/xhs_test.html -w "HTTP:%{http_code} SIZE:%{size_download}\n"
  grep -c '__INITIAL_STATE__' /tmp/xhs_test.html   # ≥1 说明页面正常，问题在权限；0 则可能是限流/反爬
  ```
- 若确认是沙箱导致：重启命令时带 `full_network` 权限，已被跳过/失败的条目由下载脚本的「已下载跳过」逻辑自然续跑。
- 转录（Whisper）、抽帧（ffmpeg）、生成 HTML/SVG 等纯本地命令不需要额外权限，可在普通沙箱内执行。

```
Task Progress:
- [ ] 0. 自动识别平台（B 站 / 小红书）
- [ ] 1. 获取元数据并下载音频、视频（小红书用 `scripts/xhs-fetch.py`，见 Step 1）
- [ ] 2. 安装依赖（ffmpeg + openai-whisper，仅首次）
- [ ] 3. Whisper 转录（优先 `medium` 或更高质量模型，`--language Chinese`）
- [ ] 4. 基于同一转录进行双轨编辑
- [ ] 5. 从视频提取 HTML 所需关键截图
- [ ] 6. 生成 HTML 图文实录
- [ ] 7. 生成 SVG 理性分析
- [ ] 8. 双产物质量自检
- [ ] 9. 更新 docs/index.json
- [ ] 10. 在开发分支提交推送，并主动合并到 `main`
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

也支持小红书分享短链或笔记页：

```json
{
  "url": "http://xhslink.cn/o/xxxxxx",
  "date": "2026-07-26"
}
```

| 字段 | 必填 | 说明 |
|------|------|------|
| `url` | 是 | 视频链接；支持 `bilibili.com`、`b23.tv`、`xiaohongshu.com`、`xhslink.cn` |
| `date` | 否 | 展示日期，格式 `YYYY-MM-DD`；未提供时使用当天日期 |

字段缺失、为空或域名不符合约束时，记录错误并结束。下载前检查 `docs/index.json`，相同 `url` 已存在则结束，避免重复处理。

开始处理前先同步 `main`，再切换到开发分支。若 Automation 已指定开发分支，直接使用该分支；否则从 `main` 创建：

```bash
git checkout main
git pull origin main
git checkout -B "{dev-branch}"
```

`{dev-branch}` 命名建议：`cursor/{slug}` 或 Automation 下发的分支名。后续 Step 0–9 都在开发分支上完成，不要直接在 `main` 上开发。

---

## Step 0：自动识别平台

收到 `url` 后，必须先识别平台，再进入下载：

```bash
node detect-platform.mjs "{url}"
```

| `platform` | 匹配域名 | 说明 |
|------------|----------|------|
| `bilibili` | `bilibili.com`、`b23.tv` | B 站长链或短链 |
| `xiaohongshu` | `xiaohongshu.com`、`xhslink.cn`、`xhslink.com` | 小红书笔记页或分享短链 |

规则：

- 只看 hostname，不依赖人工标注
- 无法识别或不支持的域名：写入含 `"error": true` 的索引条目并结束
- 识别结果写入后续索引字段 `platform`（`bilibili` 或 `xiaohongshu`）
- 短链允许跳转；索引 `url` 仍保留 Webhook 原始输入，便于去重

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

### B 站下载

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

若网页 412，可回退公开 API（`x/web-interface/view` + `x/player/playurl?fnval=16`），优先低码率音频与 ≤1080p 视频的 `backupUrl`，并携带浏览器 User-Agent 与 B 站 Referer。

### 小红书下载

**主路径（推荐，2026-08 起）**：`yt-dlp` 的小红书提取器已因小红书页面改版失效（报 403 或 "No video formats found"），改用仓库内脚本 `scripts/xhs-fetch.py`，它负责短链展开、页面解析、提取视频直链、下载与抽音频，一次调用产出全部所需文件：

```bash
# 脚本内部已执行 xhs-rate-limit.mjs 限流；产出 {slug}.source.mp4 + {slug}.m4a + {slug}.meta.json
python3 scripts/xhs-fetch.py "{url}" "{slug}"
```

脚本工作原理与注意事项：

- 用 `curl -L` 展开短链并抓取笔记页（iPhone UA + `Referer: https://www.xiaohongshu.com/`）
- 解析页面 `window.__INITIAL_STATE__`：优先读新版路径 `noteData.data.noteData`，旧路径 `note.noteDetailMap` 作为兜底；JSON 解析失败时用 `yt_dlp.utils.js_to_json` 修复非标准 JSON
- 从 `video.media.stream.h264/h265` 中取第一个 `masterUrl` 作为视频直链，再 `curl` 下载（视频本体在 CDN，**下载视频不占限流额度**）
- `meta.json` 包含笔记 id / 标题 / 时长 / 作者 / master_url，可直接作为后续图文实录的元数据来源
- 需要 `curl` 和能 `import yt_dlp.utils` 的 Python 环境；若 `yt-dlp` 后续修复了提取器，可自行判断是否退回备选方式

**备选方式（yt-dlp 提取器恢复有效时，或新方式失效时退回）**：

```bash
# 请求前必须手动过限流器，保证与上一条小红书网络请求相隔至少 60 秒
node xhs-rate-limit.mjs
yt-dlp -f "best[height<=1080]/best" -o "{slug}.source.%(ext)s" "{url}"
ffmpeg -i "{slug}.source.{实际扩展名}" -vn -acodec aac -b:a 128k "{slug}.m4a"
```

注意：

- 主路径脚本已内置限流；若改用备选方式，上述节流器必须在每一次小红书重试前执行；不得并发处理多个小红书 URL。
- 小红书常只有整段 MP4，没有独立 bestaudio；只从已下载的本地混合文件抽出 m4a，不再发起第二个下载请求。
- 备选方式中，短链需允许跟随跳转；保留完整 `xsec_token` 等分享参数
- 作者名可能缺失，可用 uploader id 或笔记文案补全元数据，不得虚构
- 若任务是修复既有文章，严禁调用本小节；只处理仓库中的本地文件

临时网络、403、412 或 429 错误最多重试 3 次；每次尝试之间至少间隔 60 秒。后续命令使用磁盘上的真实文件名，不假定扩展名。

---

## Step 2：安装依赖

仅首次运行需要：

```bash
command -v ffmpeg >/dev/null || brew install ffmpeg
python3 -c "import whisper" 2>/dev/null || pip3 install --user openai-whisper
```

确认 `ffmpeg`、`ffprobe`、`whisper`、`node`、`curl`、`detect-platform.mjs` 和 `xhs-rate-limit.mjs` 均可执行；确认 `python3` 已安装且环境内有 `yt-dlp`（`scripts/xhs-fetch.py` 依赖其 `yt_dlp.utils.js_to_json` 解析小红书非标准 JSON）。

---

## Step 3：Whisper 转录

```bash
# 可用时优先使用 medium 或更高质量模型；不得为节省成本降级为
# 无法可靠输出中文转录的模型。
whisper "{音频文件}" --model medium --language Chinese --output_dir .
```

产物为 `{slug}.txt`、`{slug}.srt`、`{slug}.vtt`、`{slug}.tsv` 和 `{slug}.json`。

必须保留 JSON 中所有非空 `segments` 及其起止时间。听不清的内容标记为 `[听不清]`，不得凭空补写。HTML 逐段呈现完整转录；SVG 的每个主要结论必须能回溯到这些分段。

效率与特殊情况：

- **超长视频（>30 分钟）**：medium 模型转录耗时很长。转录开始后即可在后台并行执行 Step 5 的预览抽帧与拼图审阅（低分辨率抽帧不依赖转录结果），不要空等转录。如需加速，可对音频切片分段转录后再按时间戳合并，但不得遗漏任何时间段。
- **视觉型短视频（<30 秒或非空 `segments` ≤3）**：转录结果可能很短甚至为空，属正常现象。这类视频以画面事实、对比演示和图注重建为主要内容来源，不要为了凑章节而臆造口播；时长档与处理方式见「视频时长分档」表。

---

## Step 4：基于同一转录进行双轨编辑

完整阅读 `{slug}.txt` 和 `{slug}.json` 后，分别准备两套内容。不得先写一份摘要，再机械复制到两个格式中。编辑前先建立覆盖表：为每个主题记录对应的起止时间、证据分段、人物/操作、画面和结论；覆盖表未覆盖全部有效转录区间前，不得开始写最终稿。

### 强制中间产物：让低能力模型只能做可验证工作

低能力模型可以协助转录切分、繁简转换、候选术语收集和 HTML 机械检查，但**不得直接生成可发布的正文、标题、摘要、术语结论或图注**。无论使用何种模型，生成正文前必须落盘并人工/高能力模型复核下列结构化中间产物：

1. **证据表 `evidence-{slug}.json`**：每个章节的时间范围、对应原始 segment 编号、可核验原话、可见操作/画面、不能确定的内容。所有非空转录区间必须恰好归入一个章节或被明确标为配乐、无口播或听不清。
2. **术语表 `terms-{slug}.json`**：`原始转录`、`候选校正`、`证据来源（画面/上下文/无法确认）`、`采用与否`。没有画面或上下文佐证的候选校正必须保留为“无法确认”，禁止写入正文。
3. **截图映射 `shots-{slug}.json`**：每张已提交截图的文件名、视频时间、画面事实描述、对应章节。图注只允许使用这份映射中的事实；“相关画面”“操作画面”“示意图”等泛化图注视为不合格。**`time` 字段必须为合法 `MM:SS`（秒 00–59），禁止 `00:70` 这类秒数越界值**（2026-08 b45 批次出现 23 处此类非法时间，直接污染 HTML 图注徽章）；从 Whisper/`ffmpeg` 拿到的原始秒数必须先转成 `M:SS` 并进位，再写入 JSON。
4. **发布摘要草案**：必须由证据表中的章节结论组合而成；禁止取第一句转录、关键词拼接或截断文本作为摘要。

生成器必须先验证这些 JSON 可解析、章节时间无空洞、截图文件存在，才可写 HTML/SVG。若任何中间产物缺失，任务只能产出草稿并标记待复核，不能写入 `index.json` 的成功条目。

### 视频时长分档（章节/字符/配图的建议基准）

不同长度视频的产出体量差异极大。下表按时长给出一档**建议基准**，用于评估章节数、编辑字符量、配图数是否与视频体量相称。**数字是建议而非硬性门禁**：最终以实际内容详实程度为准，宗旨是**尽可能详细**——内容已经充分（如长视频章节少但每章叙述充分、配图精确覆盖全部知识点）时不因数字不达标而返工；反之，即使数字达标，若正文空泛、覆盖不全，仍须补充。

| 时长档 | 判定 | HTML 章节数 | 简体中文编辑字符 | 配图数 | 特别处理 |
|--------|------|------------|-----------------|--------|----------|
| 视觉型短视频 | <30 秒，或非空 `segments` ≤3 | ≥1（画面驱动） | ≥200 | 1–3 | 内容以画面事实 + 图注重建为主；SVG 合并为 2–3 模块 |
| 普通短视频 | 30–90 秒 | ≥2 | ≥400 | 2–4 | — |
| 短中视频 | 90 秒–5 分钟 | ≥3 | ≥800 | 3–6 | — |
| 中视频 | 5–10 分钟 | ≥4 | ≥800 | 6–8 | — |
| 长视频 | 10–30 分钟 | ≥6 | ≥1500 | 8–12 | — |
| 超长视频 | >30 分钟 | ≥8 | ≥2500 | 12–20 | 走「完整版 / 增强版」流程（见上文）；转写期间后台并行抽帧 |

判定要点：

- 时长以 Step 1 的 `yt-dlp --print duration_string`（B 站）或 `meta.json` 中的 `duration`（小红书，由 `xhs-fetch.py` 产出）为准；`segments ≤3` 指 Whisper 转录后非空分段数不超过 3。
- 与表格冲突时以内容详实度优先：教程/科普类建议按「章节数」列取高值（如 10–30 分钟教程参考 ≥6 章），但章节可合并叙述、按实际内容划分，不必为凑数字拆分。
- 视觉型短视频（8–30 秒的动图、对比、卡点、纯画面无口播）转录结果可能为空，属正常现象，不作为质量缺陷；其内容来源是画面事实与图注，而非臆造口播。
- 表格中的配图数为常规区间，增强版可突破上限（见「完整版 / 增强版 HTML」）；源资产缺失时允许少于下限，但必须在正文写明「本地截图缺失」。

### 生成后反模板门禁

在提交前对每篇文章运行以下失败即阻断的检查；不要用“已生成页面”代替检查：

- 正文不得包含 `summary-row`、`要点详解`、`核心主题：` 等批量模板残留。
- 章节标题不得使用“核心内容”“操作演示”“相关技巧”“进阶设置与优化”等泛化标题；标题必须包含视频中的对象、方法或判断。
- 每个 `figure` 必须有存在的本地图片、具体 `alt` 和含时间的图注；截图数量参考「视频时长分档」表，但以是否覆盖全部知识点为准，不得因缺图注、坏图等原因遗留残图。源资产缺失时允许少于该档参考值，并必须在正文写明「本地截图缺失」。
- 检测到英文句、繁体字、`...`/`…`、占位标题 `XiaoHongShu video #`、连续乱码词或未完成句时，阻断发布并进入术语复核。
- HTML 的章节数与编辑字符量参考「视频时长分档」表（如视觉型短视频 ≥1 章/200 字、短中视频 ≥3 章/800 字、长视频 ≥6 章/1500 字、超长视频 ≥8 章/2500 字）；数字不达标时先按实际内容判断是否详实，**硬性底线**是：正文不得由转录拼接构成、必须覆盖完整视频时段、没有模板空话和未完成句。
- 所有专业性、安全性或产品参数结论必须标明来源层级：视频演示、视频作者观点、或可核验画面；无法验证的数字、法规、寿命和性能承诺必须删除或标为未核实。

### A. HTML 图文实录：按视频发生顺序展开

写作语气自然、轻松、偏纪实，保留视频的推进感：

1. **内容要点（提炼总结，严禁逐段罗列）**：阅读全部转录后，用简体中文将视频内容归纳为一段开场导语 + 按主题分组的要点列表。每组必须包含：
   - 主题标签（如"原理说明""操作步骤""避坑提醒"等，而非原文关键词拼接）
   - 该主题涉及的起止时间范围
   - 用自然语言概括的核心信息（选最具代表性的 1-2 句原话或归纳表述）
   
   **硬约束：不得**把 Whisper segments 逐条罗列为内容要点。如果转录有 100 段，内容要点最多 8 个主题组，每组一段概括，不是 100 行时间标记。内容要点和"详细文字转录"的功能必须明确分离——前者是归纳，后者是原文逐段存档。
2. **开场背景**：UP 主为什么谈这个主题，当时面对什么场景；没有证据时明确写“视频未交代”，不得补写。
3. **章节实录**：按时间顺序讲清每一段发生了什么。每个章节均须包含时间范围、描述性小标题、至少一段完整叙述；有可见操作、界面、动作、产品或前后对比时，必须写明其变化与作用，而非只说“展示了画面”。
4. **人物与语气**：区分说话人；争议观点明确标注为个人立场
5. **关键画面**：把界面、产品、图表、操作或对比截图放在对应叙述旁
6. **完整转录**：页面末尾逐段呈现全部非空 Whisper segments 和时间戳

HTML 可以解释必要背景，但不应把叙事切碎成大量分析卡片。它回答的是：“视频具体说了什么、展示了什么、前后如何发展？”章节数量参考「视频时长分档」表（视觉型短视频至少 1 个画面驱动章节，普通短视频至少 2 个，90 秒及以上至少 3 个，超长视频至少 8 个），但按实际内容划分，不必为凑数字拆分章节。若素材确实只有一个连续操作，按操作阶段拆分，并在文中说明没有明显段落切换。

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

SVG 的模块数量同样参考「视频时长分档」表：视觉型短视频（<30 秒或 `segments` ≤3）允许合并为 2–3 个模块（如「核心对比 + 关键结论」），避免空泛；长视频（>10 分钟）观点卡片建议不少于 4 张；超长视频（>30 分钟）建议至少覆盖 5 个分析主题。核心命题、行动清单与避坑总结对任何长度都是必需模块，不得因短视频而省略。

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

- 配图数量参考「视频时长分档」表（视觉型短视频 1–3 张、普通短视频 2–4 张、长视频 8–12 张、超长视频 12–20 张），每张对应一个内容节点，最终以是否覆盖全部知识点为准；增强版可突破上限，见「完整版 / 增强版 HTML」
- 静态或纯音频视频至少保留 1 张代表画面，并在图注说明画面长期不变
- 文件按顺序命名为 `shot-01.jpg`、`shot-02.jpg`……
- 检查黑屏、模糊、转场和字幕遮挡，必要时前后微调 0.5-2 秒
- 使用本地相对路径，不引用平台远程图片，不嵌入 base64
- 每张图必须有准确 `alt` 和带时间戳的 `figcaption`

### 提取与选图建议

- **预览 → 抽帧 → 拼图 → 精选**：先抽低分辨率全片预览帧，再用拼图（`ffmpeg` `hstack`/`vstack`）批量审阅，确认画面内容后，再对选定时刻提取全尺寸帧。避免反复单帧读取浪费时间。
- **“大屏幕/示例照片”时刻优先**：教学类视频的“请看大屏幕”瞬间是最高价值配图素材，应精确定位并抽取全尺寸帧。
- **中间产物一律放 `_work/`**：预览帧、密集抽帧、拼图网格等过程文件统一放在仓库根目录 `_work/`（已被 `.gitignore` 忽略，不会误提交）。最终只把精选后的图片复制进 `docs/assets/{slug}/`。
- **增强版配图可突破 8 张上限**：完整版/增强版文章按知识点配图，可到 15–20 张甚至更多，文件名可用语义化命名（`pose-squat-back.jpg` 等），但仍须逐张有准确 `alt` 和带时间戳图注。

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
      <details class="transcript-collapsible">
        <summary>详细文字转录</summary>
        <div class="transcript-body">
          <p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差。</p>
          <ol class="transcript-list">${transcript}</ol>
        </div>
      </details>
    </section>
  </main>
  <script>(function(){var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){d.setAttribute("open","")}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){a.addEventListener("click",open)});if(location.hash==="#transcript")open()})();</script>
</body>
</html>`;

fs.writeFileSync(OUT, html, 'utf8');
console.log('Generated:', OUT, 'segments:', segments.length);
```

### HTML 页面结构

```html
<main class="container">
  <header><!-- 标题、元数据、纪实导语、原视频链接 --></header>
  <article class="documentary">
    <!-- 内容要点：提炼总结，不是逐段转录！ -->
    <h2>内容要点</h2>
    <p>{开场导语：一句话概括视频类型和核心主题}</p>
    <h3>知识结构</h3>
    <div class="summary-row">
      <span class="time-marker">[MM:SS→MM:SS]</span>
      <div>
        <strong>{主题标签，如「原理说明」「操作步骤」}</strong>
        <p>{用自然语言概括的核心信息，选 1-2 句最具代表性的话}</p>
      </div>
    </div>
    <!-- 重复最多 8 个 summary-row -->
    <div class="takeaway-box">
      <strong>总结</strong>
      <p>{核心结论或要点（一两句话）}</p>
    </div>

    <section class="story-section"><!-- 按时间推进的详细叙述 --></section>
    <figure>
      <img src="assets/{slug}/shot-01.jpg" alt="{准确描述}" loading="lazy">
      <figcaption class="cap-bilingual">
        <div class="cap-zh">[01:23] {画面内容及上下文}</div>
        <div class="cap-en">
          <button class="cap-speak" data-audio="audio/{图注md5前12位}.mp3" type="button" aria-label="Play English audio">🔊</button>
          <span>{图注英文翻译}</span>
        </div>
        <audio class="cap-audio" src="audio/{图注md5前12位}.mp3" preload="none"></audio>
      </figcaption>
    </figure>
  </article>
  <section class="transcript-section" id="transcript">
    <details class="transcript-collapsible">
      <summary>详细文字转录</summary>
      <div class="transcript-body">
        <p class="transcript-note">…</p>
        <ol class="transcript-list">…</ol>
      </div>
    </details>
  </section>
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
.cap-bilingual .cap-zh{font-size:14px;line-height:1.7}.cap-bilingual .cap-zh .time-badge{font-weight:700;color:#b45309;margin-right:6px}.cap-bilingual .cap-en{display:flex;align-items:flex-start;gap:10px;margin-top:8px;padding-top:8px;border-top:1px dashed #e7e5e4;color:#0f766e;font-size:14px;line-height:1.7}.cap-speak{flex:none;width:34px;height:34px;border:none;border-radius:50%;background:#0f766e;color:#fff;font-size:14px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;transition:transform .15s,background .2s}.cap-speak:hover{background:#115e59;transform:scale(1.08)}.cap-speak.playing{background:#b45309;animation:capPulse 1s infinite}@keyframes capPulse{0%,100%{opacity:1}50%{opacity:.55}}
.transcript-list{list-style:none;padding:0}
.transcript-row{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}
.transcript-row time{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}
.transcript-row p{margin:0}
.transcript-collapsible{border:none;margin:0;padding:0}
.transcript-collapsible summary{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{display:none}
.transcript-collapsible summary::before{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}
.transcript-collapsible[open] summary::before{transform:rotate(90deg)}
.transcript-collapsible[open] summary{margin-bottom:16px}
.transcript-collapsible .transcript-body{margin-top:0}
.summary-row{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}
.summary-row .time-marker{flex-shrink:0;margin-top:2px}
.summary-row strong{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}
.summary-row p{color:#57534e;margin:0;font-size:15px}
.takeaway-box{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}
.takeaway-box strong{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}
.takeaway-box p{color:#3b82f6;margin:0;font-size:15px}
h3{font-size:20px;font-weight:700;color:#1c1917;margin:28px 0 14px}
@media(max-width:640px){
  .container{padding:28px 18px 56px}
  .transcript-row{grid-template-columns:56px 1fr;gap:10px}
}
```

运行：

```bash
node "generate-{slug}-html.mjs"
```

### 图注双语与朗读音频（强制）

每个 `figcaption` 必须是中英对照结构（见上方 HTML 页面结构），中文图注为主文案，英文行为其翻译，并配 🔊 朗读按钮播放英文。这是发布标准，不允许生成只有中文的单语图注。

翻译与音频按全站共享资产处理：

- **翻译表 `translations.json`**：`{中文图注: 英文翻译}`，按图注文本精确匹配，跨视频复用。新图注先查表：命中直接复用，未命中翻译后追加进表。
- **音频 `docs/audio/{md5(中文图注)[:12]}.mp3`**：用 `edge-tts`（`en-US-JennyNeural`）按英文翻译合成，按图注哈希命名实现全局去重；同一图注的多个视频共用一份音频。
- **增强脚本**（幂等、可全量重跑）：
  - `scripts/extract-captions.py`：从全部 HTML 提取图注，重建 `caption-extract.json` 翻译清单
  - `scripts/gen-caption-audio.py`：读取 `translations.json`，对缺音频的图注用 edge-tts 批量生成，已存在则跳过（可续跑）
  - `scripts/enhance-captions-html.py`：把 HTML 中的单语 `figcaption` 重写为中英对照，并注入 `cap-en-style` 样式与 `cap-en-script` 播放脚本

**全量扫描副作用（2026-08 b45 批次实战）**：三个脚本都按 `docs/*-图文实录.html` 全量扫描，`enhance-captions-html.py` 会把缺少增强块的旧文章（其他批次）也注入样式与脚本，产生无关 git diff（b45 批次一次误改 14 个 b42 旧文件，需逐个还原）。批处理运行后必须用 `git status` 核对并还原无关改动（`git checkout -- <无关文件>`）；只处理单篇时可临时给脚本加 slug 白名单过滤。

**执行顺序（不可颠倒）**：`gen-caption-audio.py` 用 `<figcaption>` 正则匹配单语图注，无法识别已增强的 `class="cap-bilingual"`。因此必须**先在未增强 HTML 上运行 `gen-caption-audio.py` 生成音频，再运行 `enhance-captions-html.py` 增强图注**。若顺序颠倒导致音频缺失，先重新生成 HTML（或还原未增强版本），再按正确顺序执行。

页面底部还需注入图注播放脚本（与转录展开脚本并存于 `</body>` 前）：

```html
<script id="cap-en-script">
(function(){
  function stopOthers(except){
    document.querySelectorAll('.cap-audio').forEach(function(a){if(a!==except){a.pause();a.currentTime=0;}});
    document.querySelectorAll('.cap-speak.playing').forEach(function(b){if(!except||b.dataset.audio!==except.dataset.audio){b.classList.remove('playing');}});
  }
  document.addEventListener('click',function(e){
    var btn=e.target.closest('.cap-speak');
    if(!btn)return;
    var cap=btn.closest('.cap-bilingual');
    if(!cap)return;
    var au=cap.querySelector('.cap-audio');
    if(!au)return;
    if(au.paused){stopOthers(au);btn.classList.add('playing');au.play();}
    else{au.pause();au.currentTime=0;btn.classList.remove('playing');}
  });
  ['pause','ended'].forEach(function(ev){
    document.addEventListener(ev,function(e){
      if(e.target.classList&&e.target.classList.contains('cap-audio')){
        var cap=e.target.closest('.cap-bilingual');
        if(cap){var b=cap.querySelector('.cap-speak');if(b)b.classList.remove('playing');}
      }
    },true);
  });
})();
</script>
```

发布注意：

- 默认用 `python3 scripts/enhance-captions-html.py` 对已生成 HTML 做后处理，保证图注双语结构统一，不必手写。
- `docs/audio/` 与 `translations.json` 必须随文章一起提交（`.gitignore` 已放行 `docs/audio/*.mp3`、`docs/audio/{slug}/*.mp3` 与 `translations.json`）；不提交则 GitHub Pages 上无法播放朗读。
- 转录区必须使用 `<details class="transcript-collapsible">` 且**默认不带 `open` 属性**（折叠），由导航点击或 `#transcript` 锚点展开；防止整页转录平铺。

---

## Step 6.5：可选产出「场景英译」英文学习卡（`html_en`）

当用户对简单英文翻译版不满意、或明确要求按 `language_paraphrase` 方式学习时，可额外产出 `docs/{slug}-场景英译.html` 作为 `outputs.html_en`，覆盖（或替代）旧的纯翻译英文页。参考实现：`docs/makeup-class-prep-场景英译.html` 与生成脚本 `scripts/gen-scene-en-makeup.py`。

页面为交互式场景英译学习卡，必须包含：

1. **Hero 头部**：封面图 + 中文标题 + 英文副标题 + meta chips（日期/平台/时长/场景数/单词点读提示）+ 朗读速度选择 + 停止朗读 + 中文语音讲解按钮（`data-audio` 指向 `audio/{slug}/narration.mp3`）
2. **侧边栏场景地图**：每个场景有编号徽章、中文标题、时间范围和英文标题，可点击跳转
3. **场景卡片**（4–12 个，按口播/步骤/活动切分）：
   - 顶部 S 编号 + 时间范围 + 「朗读整个场景」按钮
   - 场景截图（复用 `docs/assets/{slug}/shot-XX.jpg` 或按需抽帧）
   - 中文场景标题 + 英文场景标题
   - 情境说明 `context`（谁在哪、要完成什么 + 语域标注）
   - 逐句中英对照：中文原文（ASR 已校正）→ 地道英文 + 每句「朗读本句」按钮 + **必填表达提示**（`<p class="note">`：关键词 → 英文对照 + 语境说明）
   - `Paraphrase & Chunks` 可折叠：每组「中文意图 → 英文替换说法」+ chunk 拆解，每场景 ≥2 组
4. **今日可练**：4 个口头替换练习（中文意图 + 英文例句 + 朗读按钮）
5. **避坑**：4 组 `✕ 直译腔 → ✓ 地道说法 + 解释`
6. **认知转变**：3 组「以前 → 新」三列对照
7. **单词点读**：英文长词（≥8 字母）与硬词表自动标记为下划线可点按钮，用 Web Speech API 发音；硬词表按主题定制 ≥20 词
8. **页脚**标注「ASR 专有名词已按语境校正 · 场景/句子朗读使用 edge-tts · 单词发音使用浏览器 Web Speech API」

音频统一用 `edge-tts` 预生成到 `docs/audio/{slug}/`：

| 文件 | 语音 | 用途 |
|------|------|------|
| `narration.mp3` + `narration.txt` | `zh-CN-XiaoxiaoNeural` | 中文讲解旁白 |
| `s{N}.mp3` | `en-US-JennyNeural` | 「朗读整个场景」 |
| `s{N}-{idx:02d}.mp3` | 同上 | 逐句朗读 |
| `practice-{idx}.mp3` | 同上 | 练习句朗读 |
| `manifest.json` | — | 音频清单 |

**禁止静态 `<audio>` 元素**：统一用 `data-audio` 按钮 + JS `new Audio()` 按需加载，避免整文件预加载卡死页面。

编辑约束：

- 中文原文必须基于已校正转录，不得凭空编造；ASR 同音错字（如「鼓球→琢磨」）在页脚注明
- 英文翻译为地道口语，不是逐字直译；主目标是从视频里学「场景式英文表达」，不是视频内容总结
- 删除被替换的旧英文页（如 `*-图文实录-en.html`），并更新 `index.json` 的 `outputs.html_en`，中文图文实录页的英文链接同步指向新页
- 更新 `index.json` 时建议增加 `"html_en_type": "scene-english"` 便于前端识别

### 批量场景英译流水线（10 篇一批）

一次处理多篇时，固定按以下 5 步推进，每步都是独立脚本、幂等可续跑：

1. **提取转录**（不重新下载/转写，避免限流）：从已发布的中文图文实录页提取带时间戳文本，作为场景切分的证据源：

   ```bash
   python3 scripts/html-transcript-to-text.py {slug} > /tmp/bXX/{slug}.txt
   ```

   同时对照 `docs/index.json` 取 URL、时长、`docs/assets/{slug}/` 的截图文件数。
2. **建 JSON**：编写一次性脚本 `scripts/create-bXX-json.py`，生成 `scripts/scene-data/{slug}.json`。scene 结构与 Step 6.5 定义一致（含 `sentences` 三元组、`paraphrase`、`speak` 等）。
3. **补全**：编写一次性脚本 `scripts/fix-bXX-json.py` 为 JSON 填充 `practice`（4 组）、`pitfalls`（4 组）、`shifts`（3 组）、`difficult_words`（≥20）、`footer_notes`。
4. **生成音频 + HTML**：

   ```bash
   python3 scripts/gen-scene-en.py --slug={slug}      # 音频 + HTML
   python3 scripts/validate-scene-json.py {slug}      # JSON 语法兜底校验
   ```

5. **链接 + 索引**：`python3 scripts/link-scene-en.py {slug1} {slug2} ...`，自动给中文图文实录页注入 `English Version` 链接，并写入 `index.json` 的 `outputs.html_en` 与 `outputs.html_en_type: "scene-english"`。

批量硬约束（443 篇执行中验证的经验）：

- **场景数必须 ≤ 该视频截图数**：`scene_imgs` 与 `scenes` 等长，复用 `docs/assets/{slug}/` 的截图。截图不够时压缩场景（合并相邻内容），不得复用同一张图。
- **转录太短或纯歌词/配乐时，用图文实录页的 `figcaption`（图注）重建场景**，而不是臆造口播；页脚注明「ASR 专有名词已按语境校正」。
- `shifts` 必须为二元组 `["以前", "新"]`，`paraphrase` 必须为二元组 `["中文意图", "英文替换说法"]`，`sentences` 为 `["中文", "英文", "提示"]` 三元组——三者长度不符都会让 `gen-scene-en.py` 解包失败（2026-08 b45 批次 4 篇因 `paraphrase` 混入第三元素而中断）。
- **批量生成前先全量校验，再逐篇生成**：逐篇跑 `validate-scene-json.py` 会留下“前一篇崩了导致后续没跑”的静默缺口。批量时先对全部 `scripts/scene-data/{slug}.json` 连续校验（无报错才进入生成），再逐篇 `gen-scene-en.py --slug={slug}`，最后用「每篇三类产物齐全 + HTML 内音频/图片引用存在」的脚本兜底检查。
- 音频按 `docs/audio/{slug}/` 组织（`narration.mp3` + `s{N}.mp3` + `s{N}-{idx:02d}.mp3` + `practice-{idx}.mp3` + `manifest.json`），`gen-scene-en.py` 已存在则跳过、可续跑。

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
- [ ] 标题、导语、内容要点、章节叙述、图注和正文编辑文案均为简体中文；原始外语/繁体引文紧随简体中文释义
- [ ] 所有非空 Whisper segments 均按原顺序和时间戳出现
- [ ] **「内容要点」是真正的提炼总结**，不是逐段时间标记堆砌：长视频按 ≤8 个主题分组并标注时间范围，短视频为单段概括
- [ ] 内容要点、章节和截图共同覆盖完整视频时段；不得遗漏结尾结论、关键转折、演示结果或前后对比
- [ ] 每个章节有具体标题、时间范围和完整叙述；不存在关键词拼贴、模板空话、未完成句、`...`/`…` 截断或重复的泛化标题
- [ ] 内容主要按视频时间顺序展开，语气自然，不写成分析卡片堆叠
- [ ] 截图数量参考「视频时长分档」表并与内容相称，每张都有准确 alt 和时间戳图注；知识章节必须有对应配图，不因数字而取舍
- [ ] 所有图注时间徽章均为合法 `MM:SS`（秒 00–59），不存在 `00:70` 这类越界值（可对 `shots-*.json` 的 `time` 批量校验）
- [ ] 每个图注都是中英对照（`.cap-bilingual`）：中文图注 + 英文翻译行 + 🔊 朗读按钮
- [ ] 每个朗读按钮的 `data-audio` 都对应 `docs/audio/` 下真实存在且已提交的 MP3；`translations.json` 已更新并提交
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
- [ ] `index.json` 摘要为简体中文、≤120 字、语义完整且不含 HTML 实体、转录碎片或截断省略号

### 批次完整性（多篇一起处理时）

- [ ] 批次内每篇三类产物齐全：`{slug}-图文实录.html`、`{slug}-理性分析.svg`、`{slug}-场景英译.html`（若产出 `html_en`）；用脚本核对，不要只数文件个数
- [ ] 每篇的 HTML 图注音频引用、场景英译的音频/图片引用都在 `docs/` 下真实存在且已加入提交
- [ ] `enhance-captions-html.py` / `gen-caption-audio.py` 全量运行造成的无关批次改动已还原，`git status` 中只包含本批次产物与 `WORKFLOW.md` 等预期文件

### 修复既有文章

修复质量问题时，按以下顺序执行，且全过程不访问小红书：

1. 从仓库现有 HTML、SVG、`docs/assets/` 和本地 Whisper JSON/转录中收集证据；缺少原始转录时，只能依据已提交文件，不能臆测。
2. 先将编辑文案转为简体中文，再按完整转录重写导语、章节、图注、内容要点和 `index.json` 摘要；原始转录本身保持为证据，不可伪造。
3. 以 `absurd-wuxia-cinematography-图文实录.html` 为质量参照，逐篇检查覆盖范围、叙事连续性和截图对应关系。
4. 修复 HTML 标签与样式后，实际检查生成页面，确认 `<article>`、`<section class="transcript-section">`、图片与所有闭合标签结构正确。
5. 只有用户明确要求且本地证据无法修复时，才将该 URL 加入小红书重新抓取队列；队列必须通过 `xhs-rate-limit.mjs` 串行执行。

### 增强版替换既有文章（“出完整版”）

当用户要求替换既有 HTML 为“非常完整”的版本时，在既有文章基础上执行，注意：

1. **本地素材优先，不重新抓取**：复用本地视频文件（如 `{slug}.source.mp4`）、已有 `docs/assets/` 截图和本地转录 JSON；若本地视频缺失，才考虑按限流规则单独重新下载。
2. **新图注必须走完整双语流程**：新增截图后，把每条新图注中文追加进 `translations.json`，然后**先 `gen-caption-audio.py` 再 `enhance-captions-html.py`**（顺序不可颠倒，见「图注双语与朗读音频」）。
3. **替换后同步 `index.json`**：更新 `screenshot_count`、`transcript_segments` 等字段，保持索引与产物一致。
4. **保留/清理生成脚本**：若使用可复用的构建脚本，保留并注明用途；一次性脚本在任务完成后清理（见 Step 11）。
5. **替换后可删除被覆盖的旧图注翻译**：若旧版本图注被全部替换且不再被任何 HTML 引用，可从 `translations.json` 移除对应 key（可选，避免表膨胀）。

---

## Step 9：更新 index.json

一个视频只写一条记录，两个入口放在 `outputs` 中：

```json
{
  "date": "YYYY-MM-DD",
  "title": "视频标题",
  "summary": "一句话摘要，≤120字",
  "tags": ["影视", "视听分析"],
  "platform": "bilibili",
  "url": "https://www.bilibili.com/video/BVxxx",
  "duration": "5分40秒",
  "outputs": {
    "html": "slug-图文实录.html",
    "svg": "slug-理性分析.svg",
    "html_en": "slug-场景英译.html",
    "html_en_type": "scene-english"
  },
  "screenshot_count": 5,
  "transcript_segments": 86,
  "svg_height": 9560
}
```

- `platform`：`bilibili` 或 `xiaohongshu`，由 Step 0 自动识别写入
- `outputs.html`：轻松纪实、含截图与完整转录的 HTML
- `outputs.svg`：客观结构化分析 SVG
- `outputs.html_en`：可选，场景英译学习卡页面（`{slug}-场景英译.html`）
- `outputs.html_en_type`：`"scene-english"`，供前端识别英文学习卡类型
- `screenshot_count`：实际提交的截图数
- `transcript_segments`：HTML 呈现的非空 Whisper 分段数
- `svg_height`：`buildSvg()` 返回的最终高度

**增强/替换既有文章后必须同步索引**：若只是增强或替换某个既有条目（如新增大量截图），必须同步更新该条目的 `screenshot_count`（以及变化了的 `transcript_segments`、`svg_height` 等字段），保持索引与实际产物一致；不要只更新 HTML 而留下过期的元数据。

首页必须在同一卡片中展示“图文实录”和“理性分析”两个入口。失败时写入含 `"error": true` 和 `error_message` 的条目；缺少任一产物均视为失败。

---

## Step 10：在开发分支提交推送，并主动合并到 `main`

**开发在开发分支，发布在 `main`。** 收到 Webhook 后，先同步 `main` 并切换到开发分支；Step 0–9 的提交与推送都在开发分支完成。任务结束前，必须主动把开发分支合并进 `main` 并推送 `origin/main`。禁止只推送到开发分支就结束。

开始前确认当前分支：

```bash
git checkout main
git pull origin main
git checkout "{dev-branch}"
```

提交前确认以下文件已生成：

- `docs/{slug}-图文实录.html`
- `docs/{slug}-理性分析.svg`
- `docs/assets/{slug}/shot-*.jpg`
- `docs/audio/`（本视频图注对应的 MP3，哈希命名，可复用已有文件）
- `docs/audio/{slug}/`（若产出场景英译页：`narration.mp3` + `s{N}.mp3` + `s{N}-{idx}.mp3` + `practice-{idx}.mp3` + `manifest.json`）
- `translations.json`（若新增图注翻译）
- `docs/{slug}-场景英译.html`（若产出 `html_en`）
- `docs/index.json`

`_work/` 目录（抽帧、预览、拼图等过程文件）已被 `.gitignore` 忽略，不得 `git add -A` 全量暂存后再手动排除；只暂存上述产物文件。

先在开发分支提交并推送：

```bash
git add "docs/{slug}-图文实录.html" "docs/{slug}-理性分析.svg" \
  "docs/assets/{slug}" "docs/audio" translations.json docs/index.json
git commit -m "content: add dual-view summary for {视频标题}"
git pull --rebase origin main
git push -u origin "{dev-branch}"
```

然后主动合并到 `main` 并推送：

```bash
git checkout main
git pull origin main
git merge "{dev-branch}"
git push -u origin main
```

**最终发布目标是 `origin/main`。** 所有 webhook/trigger 完成后，变更必须已经出现在 `main` 上；GitHub Pages 从 `main` 的 `docs/` 部署。开发分支可以保留，也可以后续清理，但不得以“已推送到开发分支”代替合并。

网络失败按 4、8、16、32 秒退避重试。`git pull --rebase origin main` 或 `git merge` 出现冲突时，解决冲突、重新自检后再继续推送。若已创建 Pull Request，可在合并到 `main` 后关闭。

### Git 推送网络故障处理（高频，443 篇实战经验）

默认 `git push` 遇到 `Empty reply from server`、`HTTP 408`、`Couldn't connect to github.com port 443`、`Connection reset` 时，**普通退避重试往往无效**，按以下顺序处理：

1. **确认是否其实已推送成功**：408 后显示 `Everything up-to-date` 可能是误导（服务端已接收但响应超时）。用远端 HEAD 对比本地：

   ```bash
   git ls-remote origin main
   git rev-parse HEAD   # 两侧相同即已推送成功，无需重复操作
   ```

2. **批量测试 GitHub 可达 IP**：国内网络环境下常只有部分 IP 通，逐个探测（返回 `200` 即可达，`000` 不通）：

   ```bash
   for ip in 20.205.243.166 140.82.114.3 140.82.113.3 140.82.121.3 140.82.112.3; do
     echo -n "$ip "; curl -sk -o /dev/null -w "%{http_code}\n" --resolve github.com:443:$ip https://github.com/ 2>/dev/null
   done
   ```

3. **强制走可达 IP 推送**（IP 随网络波动需多次尝试）：

   ```bash
   git -c http.curloptResolve="github.com:443:20.205.243.166" \
       -c http.postBuffer=524288000 \
       -c http.version=HTTP/1.1 \
       push origin main
   ```

   - 命中可达 IP 后把该 IP 固化到当前仓库，减少后续失败：

     ```bash
     git config http.curloptResolve "github.com:443:20.205.243.166"
     git config http.version HTTP/1.1
     git config http.postBuffer 524288000
     ```

   - 大提交（每批含多张截图 + 音频）建议同时设 `http.lowSpeedLimit=1000`、`http.lowSpeedTime=300`，避免慢速被判超时。
4. 推送失败的重试间隔远大于网络退避（可达 1–3 分钟以上），且每次重试都换用 curl 探测到的最新可达 IP；不要对着同一失效 IP 反复重试。

---

## Step 11：清理

```bash
rm "generate-{slug}-html.mjs" "generate-{slug}-svg.mjs"
rm -f "{音频文件}" "{视频文件}"
```

转录中间文件可按调试需要保留，但不提交到仓库。

临时工作目录统一放 `_work/`（`.gitignore` 已忽略）；任务结束后建议清空 `_work/` 下的抽帧、预览、拼图产物，避免占用磁盘。可复用的构建脚本（如 `build-{slug}-html.py`）可保留在仓库根目录或 `scripts/` 并注明用途；一次性脚本必须清理。

---

## 约束

- 仅处理 `bilibili.com`、`b23.tv`、`xiaohongshu.com`、`xhslink.cn`；必须先用 `detect-platform.mjs` 识别平台
- 每个 URL 只处理一次，一个索引条目对应两个产物
- 小红书请求必须在每次网络访问前执行仓库根目录的 `xhs-rate-limit.mjs`，并保持至少 60 秒间隔；修复既有文章默认不得访问小红书
- HTML 必须包含本地关键截图、完整时间戳转录、图注英文翻译与朗读音频；转录默认折叠（`<details>` 不带 `open`），图注为中英对照（`.cap-bilingual`）
- 图注翻译写入 `translations.json`，朗读音频写入 `docs/audio/`（按图注哈希去重；场景英译音频按 `docs/audio/{slug}/` 组织）；二者为发布必需资产，必须随文章提交，`.gitignore` 已放行
- SVG 必须使用 `svg-auto-height.mjs` 和原有分析视觉框架
- 所有面向读者的编辑文案必须为简体中文，且不得包含截断内容、关键词拼贴或模板套话
- 不使用 `rsvg-convert` 或 Inkscape 渲染 SVG
- 自动化产出只写入 `docs/`；临时生成脚本除外
- 必须在开发分支完成开发与提交，并在任务结束前主动合并到 `main`；禁止只推送到开发分支就结束；Pages 从 `main` 的 `docs/` 部署
