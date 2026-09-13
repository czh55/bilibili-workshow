#!/usr/bin/env node
/** B57 batch2：host-express-day2-logic + host-express-system-intro */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.join(ROOT, '..');
const DOCS = path.join(REPO, 'docs');

function esc(s) {
  return String(s ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function fmtTime(sec) {
  const s = Math.max(0, Math.floor(Number(sec) || 0));
  const m = Math.floor(s / 60);
  const r = s % 60;
  return `${String(m).padStart(2, '0')}:${String(r).padStart(2, '0')}`;
}

function durationZh(sec) {
  const s = Math.floor(Number(sec) || 0);
  if (s < 60) return `${s}秒`;
  const m = Math.floor(s / 60);
  const r = s % 60;
  return r ? `${m}分${r}秒` : `${m}分钟`;
}

function loadSegments(slug) {
  const j = JSON.parse(fs.readFileSync(path.join(REPO, `${slug}.json`), 'utf8'));
  return (j.segments || []).filter((x) => String(x.text || '').trim());
}

function rawAsr(text) {
  return String(text ?? '').trim();
}

const HTML_CSS = `*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}
.container{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}header{margin-bottom:40px}
header h1{font-size:28px;font-weight:800;color:#1c1917;margin:0 0 8px;line-height:1.4}
header .meta{font-size:14px;color:#78716c;margin-bottom:16px}header .meta span{margin-right:16px}
.original-link{display:inline-block;margin-top:8px;font-size:14px;color:#3b82f6;text-decoration:none;border:1px solid #3b82f6;padding:4px 14px;border-radius:8px}
.original-link:hover{background:#3b82f6;color:#fff}
.documentary{font-size:17px}
.documentary h2{font-size:22px;font-weight:700;color:#1c1917;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.summary-row{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}
.summary-row .time-marker{flex-shrink:0;margin-top:2px;font-size:14px;color:#b45309;font-weight:700;font-variant-numeric:tabular-nums;min-width:80px}
.summary-row strong{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}
.summary-row p{color:#57534e;margin:0;font-size:15px}
.takeaway-box{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}
.takeaway-box strong{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}
.takeaway-box p{color:#3b82f6;margin:0;font-size:15px}
.story-section{margin:48px 0}
.story-section h3{font-size:20px;font-weight:700;color:#1c1917;margin:28px 0 6px}
.story-section .section-time{font-size:14px;color:#b45309;font-weight:600;margin-bottom:12px;font-variant-numeric:tabular-nums}
.story-section p{color:#44403c;margin:0 0 12px;line-height:1.9}
img{display:block;max-width:100%;height:auto}
figure{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}
figcaption{padding:14px 18px;color:#57534e;font-size:14px;line-height:1.6}
.transcript-section{margin-top:64px}
.transcript-list{list-style:none;padding:0}
.transcript-row{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}
.transcript-row time{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700;font-size:14px}
.transcript-row p{margin:0;font-size:15px}
.transcript-collapsible{border:none;margin:0;padding:0}
.transcript-collapsible summary{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{display:none}
.transcript-collapsible summary::before{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}
.transcript-collapsible[open] summary::before{transform:rotate(90deg)}
.transcript-collapsible[open] summary{margin-bottom:16px}
.transcript-note{font-size:14px;color:#a8a29e;margin-bottom:16px}
@media(max-width:640px){.container{padding:28px 18px 56px}.transcript-row{grid-template-columns:56px 1fr;gap:10px}}`;

const SVG_CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#1e40af,#3b82f6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#1e40af;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul,ol{padding-left:24px;margin:8px 0}
li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline h3{color:#1e40af;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#3b82f6;min-width:100px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:16px 22px;text-align:center;min-width:130px;font-weight:700;font-size:14px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.node-red{background:linear-gradient(135deg,#fef2f2,#fee2e2);border-color:#fca5a5;color:#991b1b}
.arrow{font-size:20px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3,.correction p{color:#92400e}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:16px;padding-left:16px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #3b82f6}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .pitfall{background:#fef2f2;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#991b1b;border-left:4px solid #ef4444}
.card .action{background:#eff6ff;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#1e40af;border-left:4px solid #3b82f6}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;

function buildSvgBody(d) {
  const tags = (d.tags || [])
    .map((t, i) => `<span class="tag ${['tag-blue', 'tag-green', 'tag-orange', 'tag-purple', 'tag-red'][i % 5]}">${esc(t)}</span>`)
    .join('');
  const timeline = (d.timeline || [])
    .map(([t, x]) => `<div class="timeline-item"><span class="timeline-time">${esc(t)}</span><span class="timeline-text">${esc(x)}</span></div>`)
    .join('');
  const mapNodes = (d.map || [])
    .map((label, i) => {
      const cls = ['node', 'node-green', 'node-orange', 'node-red'][i % 4];
      const arrow = i < d.map.length - 1 ? '<span class="arrow">→</span>' : '';
      return `<div class="${cls}">${esc(label)}</div>${arrow}`;
    })
    .join('');
  const corrections = (d.corrections || []).map((c) => `<p>· ${esc(c)}</p>`).join('');
  const cards = (d.cards || [])
    .map((c) => {
      const tone = c.tone ? `card ${c.tone}` : 'card';
      const quote = c.quote ? `<div class="quote">${esc(c.quote)}</div>` : '';
      const pitfall = c.pitfall ? `<div class="pitfall">${esc(c.pitfall)}</div>` : '';
      const action = c.action ? `<div class="action">${esc(c.action)}</div>` : '';
      return `<div class="${tone}"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p>${quote}${pitfall}${action}</div>`;
    })
    .join('');
  const boundary = (d.boundary || []).map((b) => `<li>${esc(b)}</li>`).join('');
  const pitfalls = (d.pitfalls || []).map((p) => `<li>${esc(p)}</li>`).join('');
  const keyHtml = (d.conclusion?.key || []).map((k) => `<li>${esc(k)}</li>`).join('');
  const actionsHtml = (d.conclusion?.actions || []).map((a) => `<li>${esc(a)}</li>`).join('');
  const shift = d.conclusion?.shift || '';

  return `<div class="container root-wrap">
  <h1>${esc(d.title)}</h1>
  <div class="meta">${tags}<span class="tag tag-gray">${esc(d.duration)}</span><span class="tag tag-gray">理性分析</span></div>
  <a class="source-link" href="${esc(d.url)}">原视频</a>
  <div class="summary-line">${esc(d.summary)}</div>
  <div class="timeline"><h3>关键证据时间轴</h3>${timeline}</div>
  <div class="map"><h2>核心脉络</h2><div class="diagram">${mapNodes}</div></div>
  <div class="correction"><h3>常见误解与认知纠偏</h3>${corrections}</div>
  <div class="section"><h2 class="sec-title">观点拆解：在讲什么 → 为何重要 → 怎么用</h2>${cards}</div>
  <div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${boundary}</ul><h3>避坑</h3><ul>${pitfalls}</ul></div></div>
  <div class="conclusion"><h2>总结与行动</h2><h3>核心要点</h3><ul>${keyHtml}</ul><h3>行动清单</h3><ol>${actionsHtml}</ol><h3>关键认知转变</h3><p>${esc(shift)}</p></div>
  <div class="footer">双轨产物之二 · 理性分析 · 证据来自同一 Whisper 转录 · ${esc(d.duration)}</div>
</div>`;
}

function buildHtml(item, segs) {
  const summaryRows = item.structure
    .map(
      ([range, title, body]) =>
        `<div class="summary-row"><span class="time-marker">[${esc(range)}]</span><div><strong>${esc(title)}</strong><p>${esc(body)}</p></div></div>`,
    )
    .join('\n');
  const chapters = item.chapters
    .map((c) => {
      const figs = (c.figures || [])
        .map(
          (f) =>
            `<figure><img src="assets/${item.slug}/${f.file}" alt="${esc(f.alt)}" loading="lazy"><figcaption>[${esc(f.time)}] ${esc(f.cap)}</figcaption></figure>`,
        )
        .join('');
      const paras = (c.paras || []).map((p) => `<p>${esc(p)}</p>`).join('');
      return `<section class="story-section"><h3>${esc(c.title)}</h3><span class="section-time">[${esc(c.range)}]</span>${paras}${figs}</section>`;
    })
    .join('\n');
  const transcript = segs
    .map((s) => `<div class="transcript-row"><time>${fmtTime(s.start)}</time><p>${esc(rawAsr(s.text))}</p></div>`)
    .join('\n');

  return `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><meta name="description" content="${esc(item.description)}"><title>${esc(item.shortTitle || item.title)}｜图文实录</title><style>${HTML_CSS}</style></head><body><main class="container"><header><h1>${esc(item.title)}</h1><div class="meta"><span>来源：小红书</span><span>时长：${esc(item.duration)}</span></div><a class="original-link" href="${esc(item.url)}" target="_blank" rel="noopener">查看原视频</a></header><article class="documentary"><h2>内容要点</h2><p>${esc(item.lead)}</p><h3>知识结构</h3>
${summaryRows}
<div class="takeaway-box"><strong>核心口诀</strong><p>${esc(item.takeaway)}</p></div>
${chapters}
</article><section class="transcript-section" id="transcript"><details class="transcript-collapsible"><summary>详细文字转录（${segs.length}段）</summary><div class="transcript-body"><p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差。</p><div class="transcript-list">
${transcript}
</div></div></details></section></main><script>(function(){var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){d.setAttribute("open","")}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){a.addEventListener("click",open)});if(location.hash==="#transcript")open()})();</script></body></html>`;
}

const ITEMS = [
  {
    slug: 'host-express-day2-logic',
    title: '14天建立表达系统day2｜如何让表达更有逻辑性',
    shortTitle: '表达更有逻辑性',
    svgTitle: '逻辑词升级：三句结构的三条铁律',
    url: 'https://xhslink.cn/o/5GUSBV1WqG7',
    durationSec: 154.24,
    primary: 'workplace',
    description:
      '三句话框架写出来仍像流水账时，先修三大病：结果优先、一句一信息、补齐落点；再把「因为/我决定」换成「根源在于/应对策略」等逻辑词，不改结构也能更有逻辑感。',
    lead: '昨天一万多人收藏后，评论区大量作业已能写出「我今天怎么样→是因为怎么样→所以我决定」的框架，但句式一放到聊天和职场汇报就变啰嗦，甚至像小学生写作文。今天两项任务：先指出问题，再在原结构上轻微升级难度；结尾预告明天用 AI 陪练。作者归纳三大易错：①顺序颠倒——先铺堵车闹钟，最后才说迟到，听众听半天才知道发生了啥，铁律是第一句永远甩结果；②一句话塞一堆细碎信息，三句话变成三小段流水账，重点被淹没——每一句只承载一个核心信息；③最多人犯的是漏掉第三句，只陈述事实不给落点，别人听完只会问「所以你想表达什么」——第三句是灵魂，必须给到行动、感受或结论。升级招：不用加内容、不改结构，只换词——「因为」→「根源在于/这背后其实是/究其原因」，「我决定」→「我的应对策略是/目前我能做到的最优解释/接下来我的思路是」。示范把「上台发抖因为害羞所以多开口」改成带逻辑词的版本二，并复盘三条铁律；评论区打卡加了逻辑词的三句话，明天教如何训练 AI 免费帮自己建表达系统。',
    takeaway: '结果优先 + 一句一信息 + 必补第三句落点；「因为/我决定」换成「根源在于/应对策略」——结构不变，逻辑感立刻上来。',
    structure: [
      ['00:00→00:27', '反馈与今日任务', '框架写得出但像流水账；先纠错再升级，预告明天 AI。'],
      ['00:27→01:22', '三大易错', '顺序颠倒、塞碎信息、漏第三句；第三句是灵魂。'],
      ['01:22→02:05', '换词升级示范', '因为→根源在于；我决定→应对策略；版本二对照。'],
      ['02:05→02:34', '三条铁律与打卡', '结果优先、一句一核、补齐落点；明日 AI 陪练。'],
    ],
    chapters: [
      {
        range: '00:00 → 00:27',
        title: '框架有了，为什么还像写作文',
        paras: [
          '昨天视频破万收藏，作者逐条看了用三句话结构讲自己事儿的作业：绝大多数人框架都写出来了，但用得不够好。句式基本停在「我今天怎么样→是因为怎么样→所以我决定」——逻辑没错，一放进现实聊天、职场汇报就变回啰嗦，甚至有点小学生写作文的感觉。',
          '今天两个重点：先指出问题，再继续练结构感并略微提升难度；结尾预告明天 AI 内容。',
        ],
        figures: [
          {
            file: 'shot-01.jpg',
            time: '00:13',
            alt: '口播举手示意，字幕「所以我决定」',
            cap: '作业句式标本：停在「所以我决定」——框架对，现场一说就啰嗦',
          },
        ],
      },
      {
        range: '00:27 → 01:22',
        title: '三大病：颠倒、塞料、断尾',
        paras: [
          '问题一：顺序颠倒。开口先铺「路上堵车、闹钟没响」，最后才说「我迟到了」——听众听半天才知道发生了啥。铁律：三句话第一句永远甩结果，不要先讲一堆理由铺垫（这也有助于短视频开头留人）。',
          '问题二：一句话塞一堆细碎信息，三句话变成三小段流水账，无关细节全塞进去，看似分了三句，重点被淹没。所以每一句只承载一个核心信息，不堆砌细节（后面会练到具体化）。',
          '问题三（最多人犯）：漏掉第三句。只陈述事实、不给落点，只讲发生了什么、为什么发生，没有后续——别人听完就会问「所以你想表达什么」。第三句是整套结构的灵魂，必须给到行动、感受或结论。',
        ],
        figures: [
          {
            file: 'shot-02.jpg',
            time: '00:39',
            alt: '口播，字幕「才知道发生了啥」',
            cap: '反例代价：先铺理由后甩结果，听众听半天才明白发生了什么',
          },
          {
            file: 'shot-03.jpg',
            time: '01:10',
            alt: '口播，字幕「只讲发生了什么」',
            cap: '断尾病：只陈述事实不给落点，对方只能追问「你想表达什么」',
          },
        ],
      },
      {
        range: '01:22 → 02:05',
        title: '只换一个词：逻辑感升级',
        paras: [
          '问题都清楚后，今天难度只升半格：不用加内容、不用改结构，只换一个词。把「因为」换成「根源在于 / 这背后其实是 / 究其原因」；把「我决定」换成「我的应对策略是 / 目前我能做到的最优解释 / 接下来我的思路是」。这些强逻辑感替换词作者已整理好。',
          '对照练习（昨天版本→今天版本二）：「我一上台讲话就容易发抖，因为我从小就害羞，所以我要多在众人面前开口说话」→「……根源在于我从小就很害羞；接下来我的思路是多在众人面前开口说话」。结构仍是结果—原因—行动，但连接词一换，听感立刻像在做分析而不是作文填空。',
        ],
        figures: [
          {
            file: 'shot-04.jpg',
            time: '01:45',
            alt: '微笑举手示意一，讲解逻辑词替换',
            cap: '升级动作：不换结构，只把连接词换成「根源在于 / 应对策略」一类',
          },
        ],
      },
      {
        range: '02:05 → 02:34',
        title: '三条铁律 + 打卡与预告',
        paras: [
          '重点强调：不换新结构，依旧是结果、原因、行动，但要遵守三条铁律才算真正掌握——①结果优先，绝不把原因放开头；②每一句话只讲一个核心信息，砍掉无关碎碎念；③必须补齐第三句，给出落点，不要止于讲故事。',
          '作业：评论区说出加了逻辑词的三句话，讲讲今天发生的一件事。明天第三天教如何训练 AI，免费帮助自己建立表达系统；记得收藏评论。',
        ],
        figures: [
          {
            file: 'shot-05.jpg',
            time: '02:20',
            alt: '比三，字幕「第三必须补齐第三句」',
            cap: '铁律三：必须补齐第三句落点——行动/感受/结论，别只讲故事',
          },
        ],
      },
    ],
    svg: {
      tags: ['表达系统', '逻辑感', '三句话', '职场汇报', '主持人'],
      summary:
        '三句框架写得出仍像流水账时，先修三大病（结果优先、一句一信息、补齐落点），再把「因为/我决定」换成「根源在于/应对策略」——结构不变，逻辑感升级。',
      timeline: [
        ['00:00', '作业反馈：框架有、用不好'],
        ['00:20', '今日：纠错 + 难度微升'],
        ['00:30', '病1：顺序颠倒，先铺理由'],
        ['00:41', '铁律：第一句永远甩结果'],
        ['00:48', '病2：一句塞碎信息成流水账'],
        ['01:05', '病3：漏第三句，只讲发生了什么'],
        ['01:28', '只换词：因为→根源在于'],
        ['01:57', '示范版本二对照'],
        ['02:10', '三条铁律收束 + 打卡'],
      ],
      map: ['三句框架', '修三大病', '换逻辑词', '更有逻辑感'],
      corrections: [
        'ASR「写错文」→写作文；「二点」→第二点（问题二）。',
        '误解：写出「因为…所以我决定」=有逻辑。纠偏：顺序颠倒、塞料、断尾任一成立，现场仍像啰嗦作文。',
        '误解：要更有逻辑就得加内容或换结构。纠偏：本课只换连接词，结构仍是结果—原因—行动。',
        '第三句落点=行动/感受/结论，不是再堆一段故事。',
      ],
      cards: [
        {
          tone: 'card-orange',
          title: '为何框架对了还啰嗦',
          body: '句式停在「怎么样—因为—所以我决定」时，逻辑骨架有了，但缺结果优先与信息裁剪，一进职场汇报就变回小学生作文腔。',
          quote: '「逻辑没错，但是放到现实聊天、职场汇报里面很容易变回啰嗦」[00:14–00:18]',
          pitfall: '继续堆细节「证明自己有在想」，重点更淹。',
          action: '先检查三句顺序：结果是否在第一句？',
        },
        {
          tone: 'card-green',
          title: '三大病与铁律',
          body: '颠倒（先铺理由）、塞料（一句多核）、断尾（无落点）。对应铁律：结果优先、一句一信息、必须补齐第三句。',
          quote: '「第三句话是整套结构的灵魂，必须给到行动、感受或者结论」[01:15–01:20]',
          pitfall: '只讲发生了什么，等对方追问「你想表达什么」。',
          action: '写完三句后删掉所有不能单独成核的碎碎念。',
        },
        {
          title: '换词不换结构',
          body: '「因为」族换成「根源在于/这背后其实是/究其原因」；「我决定」族换成「应对策略/最优解释/接下来我的思路是」。同一事实，连接词决定听感是分析还是填空。',
          quote: '「不用加内容，不用改结构，只换一个词，让我们的表达就更有逻辑感」[01:24–01:29]',
          pitfall: '换了词却仍把原因放第一句。',
          action: '把昨天作业整段只改连接词，朗读对照。',
        },
        {
          tone: 'card-red',
          title: '打卡闭环',
          body: '评论区交「加了逻辑词的三句话」讲今天一件事；明日进入 AI 陪练，把结构安检外包给提示词。',
          quote: '「在评论区说出加了逻辑词的三句话，讲讲你今天发生的一件事」[02:22–02:28]',
          pitfall: '只收藏不交作业，铁律记不住。',
          action: '今日一事 → 结果/根源在于/应对策略 三句语音打卡。',
        },
      ],
      boundary: [
        '面向口语与职场短汇报，不替代正式公文或法律陈述规范。',
        '「只换词」是 day2 剂量；画面感/具体化在后续天数另练。',
        '逻辑词清单可自扩展，但不要为了炫词牺牲一句一核。',
      ],
      pitfalls: [
        '结果仍埋在第三句。',
        '换词后继续塞无关细节。',
        '第三句只抒情不给行动或结论。',
      ],
      conclusion: {
        key: [
          '框架写出≠会用：先修颠倒/塞料/断尾',
          '第一句甩结果，第三句给落点',
          '逻辑感可先靠连接词升级，不必加码内容',
        ],
        actions: [
          '挑今天一件事，按结果—根源在于—应对策略写三句',
          '朗读并删到每句只剩一个核',
          '评论区打卡，明日接 AI 安检',
        ],
        shift: '以前：有「因为所以」就觉得有逻辑；现在：结果优先 + 一句一核 + 落点齐全，再靠逻辑词把作文腔换成分析腔。',
      },
    },
    index: {
      summary:
        '三句框架仍像流水账时，先修结果优先、一句一信息、补齐落点；再把「因为/我决定」换成「根源在于/应对策略」，结构不变逻辑感升级。',
      tags: ['表达系统', '逻辑感', '三句话', '职场汇报', '口语训练'],
    },
  },
  {
    slug: 'host-express-system-intro',
    title: '主持人跟练｜14天建立表达系统',
    shortTitle: '14天表达系统开篇',
    svgTitle: '三句话定乾坤：14天表达系统开篇',
    url: 'https://xhslink.cn/o/9NbGTZOCn14',
    durationSec: 85.2,
    primary: 'workplace',
    description:
      '结巴、大脑空白或讲半天别人听不懂时，用14天表达系统入门：前三天练结构感，核心方法「三句话定乾坤」——结果、原因、行动；电梯撞领导迟到示范，结构性汇报不背锅只解决问题。',
    lead: '开场立人设：科班出身、一堆专业证书、省台干了十几年新闻主播，自称更懂普通人说话的痛点——一开口就结巴、大脑一下子空白，或讲了半天别人听不懂。承诺每天三分钟跟练：不需要卖课、不需要天赋，无偿带打卡，收藏即可开始。系统地图：前三天练结构感，四到七天练具体化，八到十天练观点，十一到十三天练即兴表达，最后一天复盘。第一阶段目标是把话说顺，核心方法叫「三句话定乾坤」：每天找一件亲身经历的事，强迫自己不说废话，只用三句话说清楚——一句结果、第二句原因、第三句影响（示范里落地为行动补救）。电梯撞领导迟到场景：别解释一堆堵车闹铃；示范句「领导我今天迟到了20分钟；主要是因为早上出门发现车胎没气处理了一下；我已经跟行政报备了，并且晚上会多留半小时把工作补上」——这叫结构性汇报，不背锅只解决问题。别嫌简单，要练到张嘴就是这个顺序；评论区用三句话讲今天一件小事，作者批作业。',
    takeaway: '三句话定乾坤：结果→原因→行动；练到张嘴就是这个顺序，汇报才像在解决问题而不是背锅。',
    structure: [
      ['00:00→00:26', '痛点与承诺', '结巴/空白/听不懂；每天三分钟无偿跟练。'],
      ['00:26→00:41', '14天地图', '结构→具体→观点→即兴→复盘；三句话定乾坤。'],
      ['00:41→01:15', '迟到示范', '结果—原因—报备补工；结构性汇报不背锅。'],
      ['01:15→01:25', '打卡作业', '练到张嘴就是顺序；评论区三句话批改。'],
    ],
    chapters: [
      {
        range: '00:00 → 00:26',
        title: '普通人说话的三个痛点',
        paras: [
          '作者以科班、证书与省台十几年新闻主播经历自荐：比一般博主更懂普通人说话的痛点——一开口就结巴、大脑一下子空白，或讲了半天别人听不懂。',
          '承诺：每天花三分钟跟练，不需要卖课、不需要天赋，会无偿带着打卡；收藏本视频即可开始。',
        ],
        figures: [
          {
            file: 'shot-01.jpg',
            time: '00:09',
            alt: '手持梳子麦克口播，字幕「我想我应该更懂」',
            cap: '立人设：省台主播视角，切入普通人结巴/空白/听不懂的痛点',
          },
          {
            file: 'shot-02.jpg',
            time: '00:25',
            alt: '口播，字幕「我们直接开始打卡吧」',
            cap: '入场门槛：收藏即可打卡，不卖课、不要天赋',
          },
        ],
      },
      {
        range: '00:26 → 00:41',
        title: '14天地图 + 三句话定乾坤',
        paras: [
          '系统分期：前三天练结构感，四到七天练具体化（口播「具体话」），八到十天练观点，十一到十三天练即兴表达，最后一天复盘。',
          '第一阶段结构感=把话说顺。核心方法「三句话定乾坤」：每天找一件亲身经历的事，强迫自己不说废话，只用三句话说清楚——一句结果、第二句原因、第三句影响（后文示范明确落到行动补救，与系列里的行动/落点同槽）。',
        ],
        figures: [
          {
            file: 'shot-03.jpg',
            time: '00:40',
            alt: '比三，字幕「三句话定乾坤」',
            cap: '核心方法亮相：三句话定乾坤——结果、原因、影响/行动',
          },
        ],
      },
      {
        range: '00:41 → 01:15',
        title: '电梯撞领导：结构性汇报',
        paras: [
          '情境：上班迟到，电梯里又碰到领导。此时不要解释一堆堵车、闹铃没响。示范：「领导我今天迟到了20分钟；主要是因为早上出门时发现车胎没气处理了一下；我已经跟行政报备了，并且晚上会多留半小时把工作补上。」',
          '作者点题：这叫结构性汇报——不背锅，只解决问题。三句话看起来简单，价值在于练到张嘴就是这个顺序。',
        ],
        figures: [
          {
            file: 'shot-04.jpg',
            time: '00:54',
            alt: '口播，字幕「比如今天我上班迟到了」，头顶上班贴纸',
            cap: '情境植入：迟到撞领导——先别堆堵车闹铃的借口',
          },
          {
            file: 'shot-05.jpg',
            time: '01:14',
            alt: '字幕「不背锅只解决问题」「解决问题」',
            cap: '示范收束：结构性汇报=不背锅，只给原因与补救行动',
          },
        ],
      },
      {
        range: '01:15 → 01:25',
        title: '评论区三句话打卡',
        paras: [
          '作业立刻落地：现在就在评论区，用三句话讲一讲今天发生的一件小事，作者来批作业。',
          '开篇不卖复杂技巧，只锁一个习惯：开口顺序=结果→原因→行动。',
        ],
        figures: [],
      },
    ],
    svg: {
      tags: ['表达系统', '三句话定乾坤', '结构感', '职场汇报', '跟练'],
      summary:
        '结巴、脑空白或讲不清时，用14天系统入门：前三天练结构感，「三句话定乾坤」按结果→原因→行动说清一事；迟到撞领导示范结构性汇报——不背锅只解决问题。',
      timeline: [
        ['00:00', '14天系统开场'],
        ['00:09', '痛点：结巴/空白/听不懂'],
        ['00:19', '每天三分钟无偿跟练'],
        ['00:26', '地图：结构→具体→观点→即兴'],
        ['00:39', '方法：三句话定乾坤'],
        ['00:54', '情境：迟到撞领导'],
        ['01:02', '示范三句：结果—车胎—报备补工'],
        ['01:12', '结构性汇报：不背锅只解决问题'],
        ['01:20', '评论区三句话打卡'],
      ],
      map: ['痛点开口', '14天地图', '三句话定乾坤', '结构性汇报'],
      corrections: [
        'ASR「一开口就接吧」→一开口就结巴；「不需要买客」→不需要卖课；「无常」→无偿；「革新方法」→核心方法。',
        '「第三句说影响」在示范中落地为行动补救（报备+加班补工），与系列「行动/落点」同槽，勿理解成再堆情绪影响描写。',
        '误解：汇报要先把委屈和客观原因讲完。纠偏：先甩结果，再一句原因，再给补救。',
        '误解：三句话太简单没必要练。纠偏：难在张嘴就是这个顺序，不是背定义。',
      ],
      cards: [
        {
          tone: 'card-orange',
          title: '为何需要系统',
          body: '痛点不是缺金句，而是开口失控：结巴、空白、或信息散乱让人听不懂。主播经验用来降低「这套对普通人是否管用」的疑虑。',
          quote: '「如果你也一开口就结巴，大脑会一下子空白，或者讲了半天别人听不懂」[00:11–00:17]',
          pitfall: '收藏一堆表达课却从不限时三句练习。',
          action: '设每日三分钟闹钟，只练结构不练辞藻。',
        },
        {
          tone: 'card-green',
          title: '14天分期',
          body: '结构感→具体化→观点→即兴→复盘。开篇只锁第一阶段：把话说顺，方法名「三句话定乾坤」。',
          quote: '「前三天练结构感……核心方法：三句话定乾坤」[00:26–00:41]',
          pitfall: '第一天就跳去练金句观点，结构仍乱。',
          action: '本周只交三句话作业，不追其他技巧。',
        },
        {
          title: '迟到示范的信息裁剪',
          body: '结果（迟到20分钟）→单一原因（车胎没气处理）→行动（报备+晚上补半小时）。砍掉堵车闹铃堆砌，听感从甩锅变成解决问题。',
          quote: '「你看这叫结构性汇报，不背锅只解决问题」[01:12–01:15]',
          pitfall: '第三句只道歉不给补救动作。',
          action: '把今天一件糗事改写成同样三槽。',
        },
        {
          tone: 'card-red',
          title: '练到自动化',
          body: '方法简单不是借口；目标是自动化顺序。评论区小事打卡形成外部监督。',
          quote: '「要练到张嘴就是这个顺序的程度」[01:18–01:20]',
          pitfall: '只会复述示范原文，换场景不会套。',
          action: '换通勤/会议/家务各写一版三句并打卡。',
        },
      ],
      boundary: [
        '开篇只建立结构习惯，不含画面感/观点深度/即兴完整课。',
        '职场示范侧重同步与补救，不覆盖所有危机公关场景。',
        '「不背锅」指表达策略，不鼓励隐瞒真实责任。',
      ],
      pitfalls: [
        '先道歉长篇铺垫再提结果。',
        '原因句塞进多个并列借口。',
        '第三句没有可执行补救。',
      ],
      conclusion: {
        key: [
          '开口乱=缺结构槽位，不是缺嘴皮',
          '结果→原因→行动，练到自动化',
          '结构性汇报：先同步事实与补救，少堆委屈',
        ],
        actions: [
          '收藏后立刻用三句话写今天一件小事',
          '检查：第一句是否结果、第三句是否行动',
          '连续三天打卡，再进入具体化阶段',
        ],
        shift: '以前：撞领导先解释一堆客观原因；现在：先报结果，再一句原因，再给报备与补救——像在解决问题。',
      },
    },
    index: {
      summary:
        '结巴或讲不清时，用「三句话定乾坤」按结果→原因→行动说清一事；迟到撞领导示范结构性汇报——不背锅只解决问题。',
      tags: ['表达系统', '三句话定乾坤', '结构感', '职场汇报', '口语训练'],
    },
  },
];

function upsertIndex(entry) {
  const indexPath = path.join(DOCS, 'index.json');
  const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
  const i = index.findIndex((e) => e.slug === entry.slug || e.url === entry.url);
  if (i >= 0) index[i] = { ...index[i], ...entry };
  else index.push(entry);
  fs.writeFileSync(indexPath, JSON.stringify(index, null, 2) + '\n');
}

const results = [];

for (const item of ITEMS) {
  const segs = loadSegments(item.slug);
  item.duration = durationZh(item.durationSec);

  const html = buildHtml(item, segs);
  const htmlPath = path.join(DOCS, `${item.slug}-图文实录.html`);
  fs.writeFileSync(htmlPath, html, 'utf8');

  const { svg, height } = await buildSvg({
    css: SVG_CSS,
    body: buildSvgBody({
      title: item.svgTitle,
      tags: item.svg.tags,
      duration: item.duration,
      url: item.url,
      summary: item.svg.summary,
      timeline: item.svg.timeline,
      map: item.svg.map,
      corrections: item.svg.corrections,
      cards: item.svg.cards,
      boundary: item.svg.boundary,
      pitfalls: item.svg.pitfalls,
      conclusion: item.svg.conclusion,
    }),
    width: 1320,
  });
  const svgPath = path.join(DOCS, `${item.slug}-理性分析.svg`);
  fs.writeFileSync(svgPath, svg, 'utf8');

  const entry = {
    date: '2026-09-13',
    title: item.title,
    summary: item.index.summary,
    tags: item.index.tags,
    platform: 'xiaohongshu',
    url: item.url,
    duration: item.duration,
    outputs: {
      html: `${item.slug}-图文实录.html`,
      svg: `${item.slug}-理性分析.svg`,
    },
    screenshot_count: 5,
    transcript_segments: segs.length,
    svg_height: height,
    slug: item.slug,
    primary: item.primary,
  };
  upsertIndex(entry);

  results.push({
    slug: item.slug,
    html: `docs/${item.slug}-图文实录.html`,
    svg: `docs/${item.slug}-理性分析.svg`,
    index: true,
    summary: item.index.summary,
    shots: 5,
    segments: segs.length,
    svg_height: height,
    duration: item.duration,
    primary: item.primary,
  });
  console.log('OK', item.slug, 'segs', segs.length, 'svg_height', height);
}

console.log(JSON.stringify(results, null, 2));
