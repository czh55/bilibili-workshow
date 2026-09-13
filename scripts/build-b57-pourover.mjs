#!/usr/bin/env node
/** B57：pour-over-fundamentals → 图文实录 HTML + 理性分析 SVG + index.json */
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

/** 转录区保留 ASR 原样；正文另走纠错表述 */
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
.summary-row .time-marker{flex-shrink:0;margin-top:2px;font-size:14px;color:#b45309;font-weight:700;font-variant-numeric:tabular-nums;min-width:88px}
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
  const table = d.table
    ? `<div class="section"><h2 class="sec-title">${esc(d.table.title)}</h2><div class="card"><table><thead><tr>${d.table.headers
        .map((h) => `<th>${esc(h)}</th>`)
        .join('')}</tr></thead><tbody>${d.table.rows
        .map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`)
        .join('')}</tbody></table></div></div>`
    : '';
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
  <div class="section"><h2 class="sec-title">观点拆解：在讲什么 → 为何重要 → 怎么用 → 原文依据</h2>${cards}</div>
  ${table}
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

const ITEM = {
  slug: 'pour-over-fundamentals',
  title: '手冲咖啡底层逻辑 一条视频讲清楚',
  shortTitle: '手冲咖啡底层逻辑',
  svgTitle: '手冲底层逻辑：滤杯极限下水时间优先，再定浓度、粉水比与注水次数',
  url: 'https://xhslink.cn/o/7h7ZbQWpbpY',
  durationSec: 1144,
  primary: 'coffee',
  description:
    '手冲咖啡底层逻辑：水温 90–96℃、研磨与香气、否定闷蒸伪命题、滤杯极限下水时间、浓度与粉水比、注水次数与手法边界。约19分4秒全片。',
  lead:
    '作者用约十三年经验，把「手冲方法」拆成可验证的底层逻辑：水温不必迷信某个精确度数（常压下约 90–96℃，100℃ 因气化萃取力反而差）；研磨越粗香气越具象，香气不足先调粗；闷蒸排二氧化碳无法被感官或仪器验完，整段冲煮都在排气，故闷蒸是伪命题；滤杯真正要问的是「极限下水时间」（如 V60 约 1 分 10 秒）——超过则易苦；风味描述是行业沟通语言，对消费者先谈酸甜苦平衡；浓度（作者偏好约 1.1–1.3）排第二重要，用注水次数在极限时间内调节；粉水比按个人口味（示意 1:13–1:15），不是固定口令。片尾用巴拿马翡翠庄园示意推演完整方案：96℃、比杯测研磨略粗、V60、四次注水、1:14→15g×210g≈每次约 65g，并强调对绝大多数人手法几乎无用。',
  takeaway:
    '先问滤杯极限下水时间 → 在时限内用注水次数调浓度（约 1.1–1.3）→ 粉水比按口味 → 研磨比杯测略粗保香气；水温 90–96℃，不必闷蒸，别迷信三段式表象与画圈手法。',
  structure: [
    ['00:00→01:42', '立题与水温', '水温不那么重要；90–96℃；100℃ 气化萃取力差；地域气压会变。'],
    ['01:42→02:44', '研磨与香气', '同牌同刻度仍不同；越粗香气越具象；香气不足调粗。'],
    ['02:44→03:57', '闷蒸是伪命题', 'CO₂ 何时排净无法验证；整段冲煮都在排气。'],
    ['03:57→05:47', '滤杯极限下水时间', '问商家给数据；决定豆适配与冲煮节奏。'],
    ['05:47→07:18', '香气/味觉分工', '香气看研磨；酸甜苦看时间与杯测。'],
    ['07:18→08:55', '风味是行业语言', '风味描述给从业者，不是消费者教育话术。'],
    ['08:55→09:56', '浓度第二重要', '金杯语境；作者喜好约 1.1–1.3，可按口味调。'],
    ['09:56→12:24', 'V60 案例推演', '浅烘好豆 96℃；1′10″ 时限；段数不重要，超时必苦。'],
    ['12:24→14:12', '酸甜苦与注水次数', '先酸再甜再苦；次数提浓度；V60 常三次表象。'],
    ['14:12→15:33', '研磨与挑磨', '比杯测研磨略粗；问厂家杯测度并用筛网验。'],
    ['15:33→17:35', '粉水比与完整方案', '1:13–1:15 按口味；15g×1:14=210g÷4≈65g。'],
    ['17:35→19:04', '手法边界与收束', '90% 人不需要手法；逻辑终极大纲，欢迎讨论。'],
  ],
  chapters: [
    {
      range: '00:00 → 01:42',
      title: '立题：水温并不像你以为的那么重要',
      paras: [
        '开场：作者称花了约十三年、二十多万学费，今天讲「全网很少人教」的手冲底层逻辑——学会之后，手冲只会越做越好。白板列出七条主线：水温、研磨度、闷蒸、滤杯、时间、风味、浓度。',
        '第一点反直觉：水温一点都不重要——不是完全不管，而是别被「必须 92 还是 93」绑架。常说手冲约 90–96℃；100℃ 可不可以？不可以。水到沸点会气化，分子更想逃离壶口，而不是把可溶物带出来。日式深烘「咕噜开水」冲却不苦，正因 100℃ 萃取能力反而低。浅烘可略高、深烘略低，但仍落在约 90–96℃；同是 92℃，四川盆地与江苏因大气压不同，萃取能力也不一样。所以水温「知道区间」即可，不必神化。',
      ],
      figures: [
        {
          file: 'shot-01.jpg',
          time: '00:58',
          alt: '白板列出水温等七项，字幕「烧的咕噜咕噜烧开了」',
          cap: '水温段：用「开水咕噜」引出 100℃ 气化与萃取力下降的物理直觉',
        },
      ],
    },
    {
      range: '01:42 → 02:44',
      title: '研磨度：只跟香气有关，越粗越具象',
      paras: [
        '「粗砂糖」说法对，但要自己试。更关键的纠偏：同一品牌、同一天生产的磨豆机，刻度都拧到 1–2–3，粉的粗细仍可能不一样——像双胞胎也不会完全相同。',
        '研磨度记住只跟香气有关：越粗，香气越具象；越细，香气越没有。磨成面粉级，再好的豆也只剩木质纤维的木头味。香气不足或不具象时，答案是调粗，不是越调越细。',
      ],
      figures: [],
    },
    {
      range: '02:44 → 03:57',
      title: '闷蒸：伪命题——你无法知道 CO₂ 何时排净',
      paras: [
        '作者断言：世界上做手冲没有闷蒸，闷蒸是伪命题。常见说法是闷蒸排二氧化碳；但他追问：用眼睛、鼻子还是嘴巴告诉你排干净了？注 30g、40g、60g 就能排净吗？没有仪器可验；昨天、今天、后天闷蒸也不可能一样。',
        '整段冲煮都在给粉能量、都在排气——只要最终排干净即可，不必迷信某一注水量的「闷蒸仪式」。网上三段式、四六法、一刀流等，等底层逻辑讲完自然明白：它们是表象，不是唯一真理。世界上没有唯一正确的冲煮方法；只教方法、不教逻辑的人，可以不听。',
      ],
      figures: [
        {
          file: 'shot-02.jpg',
          time: '03:00',
          alt: '指向玻璃滤杯，字幕「你注入30克的水」',
          cap: '反诘闷蒸：注多少水算「排净」？感官与仪器都给不出终点',
        },
      ],
    },
    {
      range: '03:57 → 05:47',
      title: '滤杯第一重要：要的是极限下水时间',
      paras: [
        '滤杯形态千奇百怪：单孔、三孔、扇形、折纸、V60……买滤杯只记一点：它是过滤器。问商家一个科学问题——极限下水时间：同样放 15g 粉、注 200g 水，水完全滴滤完要多久？有的 1′10″、1′20″，有的 3 分钟，有的 45 秒。有了这个参数，才知道杯适合什么样的豆。',
        '别只听「下水快/慢」叙事，要准确数据；像买车要知道时速上限。拿到极限下水时间后，按这个时钟来萃取，一刀流、三刀流都会了——因为段数是你对时间的切分方式，核心约束是滤杯时钟。',
      ],
      figures: [
        {
          file: 'shot-03.jpg',
          time: '06:00',
          alt: '白板划掉闷蒸，桌上多款滤杯，字幕「那杯手冲咖啡有没有风味」',
          cap: '白板纠偏：闷蒸「不需要」；滤杯箭头指向「极限下水时间」',
        },
      ],
    },
    {
      range: '05:47 → 07:18',
      title: '风味二元：香气看研磨，味觉看时间',
      paras: [
        '咖啡风味大致拆成香气与味觉（酸甜苦）。豆的香气只跟研磨度有关——所以「这杯有没有风味」跟你怎么冲手法几乎无关，先跟研磨有关。接下来力气应集中在味觉：酸、甜、苦何时出来。',
        '你可以杯测自己的豆：第几秒酸完、甜完、苦完（示意 20s / 45s / 1′20″）。滤杯给的是「极限萃取时间」像汽车时速；你自己找酸甜苦像开车技术——同样的车，技术不同，酸甜苦节奏也不同。酸甜苦要自己找；极限下水时间必须由滤杯/商家给出。',
      ],
      figures: [],
    },
    {
      range: '07:18 → 08:55',
      title: '风味描述：行业第三语言，不是消费者必修课',
      paras: [
        '作者郑重声明：凡是动辄对消费者灌风味词的人，在耍流氓——不是说行业撒谎，而是沟通对象错了。类比修咖啡机：用户只需知道加热管坏了、换好能用；买配件才需要型号与材质。',
        '风味是行业内沟通语言：同样训练过的感官，可以说柠檬酸值、白花香、佛手柑尾韵。对消费者说这些，本质是想证明豆好、好卖价钱；把消费者当十年咖啡师来「教育」是错位。风味由研磨度决定；风味语言留给行业。',
      ],
      figures: [
        {
          file: 'shot-04.jpg',
          time: '08:59',
          alt: '指向白板「风味」圈注，字幕「刚才讲的这个」',
          cap: '滤杯极限下水时间第一重要；下一节进入浓度',
        },
      ],
    },
    {
      range: '08:55 → 09:56',
      title: '浓度：第二重要，可按口味调',
      paras: [
        '一杯好不好喝，浓度很重要——不是个人随口一说，而是大量实验调查得到的参考（金杯标准语境）。作者个人喜欢的手冲浓度约在 1.1–1.3：入口觉得浓度合适，像炒番茄蛋加多少糖——按口味定。',
        '地区与人有平均标准，但浓一点淡一点可以自己调。浓度排第二重要（滤杯极限时间第一）。至此基础逻辑铺完，进入完整案例。',
      ],
      figures: [],
    },
    {
      range: '09:56 → 12:24',
      title: '案例：V60 × 浅烘好豆，96℃ 与 1′10″ 铁律',
      paras: [
        '示意：V60 + 巴拿马翡翠庄园级浅烘好豆（生豆很贵）。水温选 96℃——要榨干、不留遗憾；100℃ 才是气化临界，96℃ 在常温常压下萃取力强的区间。不需要闷蒸。',
        'V60 极限下水时间作者直接给：约 1 分 10 秒。粉水接触超过 1′10″，这杯必定偏苦。冲三次都落在 1′10″ 叫三段；冲一次叫一段；冲五次叫五段——段数不重要，你爱冲几段冲几段；但每一次注水到滴尽，都不能超过 1′10″。冲煮时间跟滤杯有关，不是自己随便定。',
      ],
      figures: [
        {
          file: 'shot-05.jpg',
          time: '12:01',
          alt: '讲解酸甜苦平衡，字幕「我们在喝一个咖啡的时候」',
          cap: '好喝抓酸甜苦平衡：先酸再甜再苦的抛物线，苦提供余韵',
        },
      ],
    },
    {
      range: '12:24 → 14:12',
      title: '酸甜苦抛物线，与用注水次数调节浓度',
      paras: [
        '好豆贵，往往因甜味物质含量高，酸是复合酸而非单一尖酸。冲完酸与甜仍要一点苦——没有苦就像没有回韵、「绕梁三日」。整体曲线：先酸再甜再苦，酸甜苦平衡才好喝；南北方舌头有差异，但你只需知道「好喝」即可，不必强迫对齐标签风味。',
        '浓度按极限萃取时间来调：同一粉床，注一次滴尽再注第二次，第二次更浓——粉里还有物质可萃。注得越多越浓，但也有极限；浓度仍要落在约 1.1–1.3。V60 按极限时间注水，正常极限大约三次——市面上很多人做三次注水，只学到表象，没说清「三次来自极限时间」。好豆可耐萃，作者会注四次把豆榨干。',
      ],
      figures: [],
    },
    {
      range: '14:12 → 15:33',
      title: '研磨怎么找：比杯测研磨度粗一丢丢；用筛网验磨',
      paras: [
        '难点是研磨度。买专业磨豆机，问品牌方「杯测研磨度是多少」——不用深究杯测用途，记住手冲（尤其 V60）比杯测研磨再粗一丢丢；只能粗不能更细去追香气。',
        '挑磨：问杯测研磨度 → 买约 25 元杯测筛网 → 按厂家给的度筛一下，对就留、不对就扔。不用先纠结材质话术。作者自嘲像在揭行业底——那就揭。',
      ],
      figures: [
        {
          file: 'shot-06.jpg',
          time: '15:01',
          alt: '按压磨豆机风箱排粉，字幕「你看一台磨豆机好不好」',
          cap: '挑磨标准：问杯测研磨度 + 筛网验证，比听材质故事更硬',
        },
      ],
    },
    {
      range: '15:33 → 17:35',
      title: '拼出完整方案：粉水比是「适量的盐」',
      paras: [
        '方案汇总：好豆 → 96℃；研磨 ≥ 杯测研磨（厂家给数字，略大或等于即可）；V60 极限约 1′10″；好豆注四次；风味不谈标签，浓度约 1.1–1.3（口述偶作 1.1–1.5）。浓度≈粉水比：巴拿马示意 1:14 / 1:15 / 极限 1:13 都可以——按口味，偏重 1:13、偏轻 1:15。',
        '凡不问你口味就甩一个固定粉水比的人，学的是表象。像炒菜「适量盐」=符合自己口味。作者个人用 1:14：15g 粉 ×14 = 210g 水，分 4 次 ≈ 每次 65g。水温、水量、次数齐了——还需要手法吗？',
      ],
      figures: [
        {
          file: 'shot-07.jpg',
          time: '16:58',
          alt: '白板酸甜苦圈注，字幕「这个适量等于什么」',
          cap: '粉水比＝适量盐：符合自己口味，不是别人甩来的固定口令',
        },
      ],
    },
    {
      range: '17:35 → 19:04',
      title: '手法对 90% 的人没用；逻辑才是终极',
      paras: [
        '对手冲小白乃至约 90% 爱好者：画圈、椭圆、定点注水几乎没有作用。世界冠军才需要用手法应对现场环境与豆况。滤杯发明者并没有规定你必须某种手法——他想传达的是：用我的杯，按极限时间直接注水（示意四次、每次约 65g）就能好喝。',
        '作者说：我没有教你「手法」，但我告诉你这杯该怎么冲。凡给数据却不问地理/感官/浓厚度的人，是在耍流氓——这叫逻辑。初中物理化学翻一遍就能自验。这套逻辑对他是「终极」大纲，还有更高级内容可讲两三个小时；有不同意见欢迎评论区讨论。',
      ],
      figures: [
        {
          file: 'shot-08.jpg',
          time: '18:20',
          alt: '指向 V60 套装，字幕「冲的很好喝了」',
          cap: '收束：按极限时间与粉水比注水，不必天天研究画圈手法',
        },
      ],
    },
  ],
  svg: {
    tags: ['手冲', '滤杯', '极限下水时间', '研磨', '浓度', '粉水比'],
    summary:
      '滤杯极限下水时间第一，浓度第二；研磨保香气（比杯测略粗），水温 90–96℃，否定闷蒸与手法迷信；用注水次数与粉水比按口味拼方案。',
    timeline: [
      ['00:00', '立题：手冲底层逻辑'],
      ['00:14', '水温：知道 90–96℃ 即可'],
      ['00:37', '100℃ 气化 → 萃取力反而差'],
      ['01:42', '研磨：越粗香气越具象'],
      ['02:44', '闷蒸是伪命题'],
      ['03:57', '滤杯：问极限下水时间'],
      ['05:47', '香气看研磨；味觉看时间'],
      ['07:18', '风味是行业语言'],
      ['08:55', '浓度第二重要 ≈1.1–1.3'],
      ['09:56', 'V60 案例：96℃ + 1′10″'],
      ['11:09', '段数不重要，超时必苦'],
      ['12:24', '酸甜苦抛物线'],
      ['12:44', '注水次数调节浓度'],
      ['14:12', '研磨比杯测略粗；筛网验磨'],
      ['15:33', '拼方案：粉水比按口味'],
      ['17:06', '15g×1:14=210g÷4≈65g'],
      ['17:35', '90% 人不需要手法'],
      ['18:27', '逻辑终极大纲；欢迎讨论'],
    ],
    map: ['极限下水时间', '浓度/注水次数', '研磨保香气', '粉水比按口味'],
    corrections: [
      'ASR：手熟→手冲；绿杯→滤杯；盐没度/颜柏斗→研磨度；催/催取→萃取；温蒸/闷争→闷蒸；杯侧→杯测。',
      'ASR：二氧化氮→二氧化碳（脱气语境）；班达玛→巴拿马；Guesa/桂香→瑰夏（Geisha）示意。',
      '误解：必须精确到某度水温。纠偏：常压约 90–96℃；100℃ 因气化萃取力差。',
      '误解：闷蒸是必备步骤。纠偏：无法验证 CO₂ 排净点；整段冲煮都在排气。',
      '误解：三段式/手法决定一切。纠偏：核心是滤杯时钟与浓度；段数与画圈对多数人几乎无用。',
      '误解：对消费者必须讲风味词。纠偏：风味是行业语言；先抓酸甜苦平衡。',
      '误解：存在唯一正确粉水比。纠偏：粉水比≈适量盐，按口味在约 1:13–1:15 自调。',
    ],
    cards: [
      {
        tone: 'card-orange',
        title: '第一优先：滤杯极限下水时间',
        body: '买滤杯不问「快慢故事」，要 15g/200g 滴尽秒数。V60 示意约 1′10″；超过此时限粉水接触过长 → 易苦。段数只是把总时间切开的方式。',
        quote: '「每一次注水到水滴干净，不能超过1分10秒」[11:09–11:12]',
        pitfall: '只抄三段注水，不看滤杯时钟。',
        action: '向商家或自测写下你的滤杯极限下水时间，贴在手冲台。',
      },
      {
        tone: 'card-green',
        title: '研磨管香气：比杯测粗一丢丢',
        body: '香气具象度随研磨变粗而上升；磨太细只剩木头味。手冲问厂家杯测研磨度，再略粗；用筛网验证磨机是否诚实。',
        quote: '「你的研磨度越粗，你的香气它更加的具象」[02:12–02:14]',
        pitfall: '香气不足却越调越细。',
        action: '香气不够 → 先调粗；换磨先问杯测度并筛一次。',
      },
      {
        title: '浓度第二：注水次数 × 粉水比',
        body: '在极限时间内，多注一次通常更浓。V60 常三次是表象；好豆可四次榨干。粉水比 1:13–1:15 按口味，浓度落在约 1.1–1.3。',
        quote: '「三次注水是根据极限时间来的」[13:36–13:39]',
        pitfall: '不问口味就死记某个粉水比。',
        action: '先定滤杯时钟 → 选注水次数调浓淡 → 再用 1:14 左右微调。',
      },
      {
        tone: 'card-red',
        title: '删掉伪步骤：闷蒸与手法迷信',
        body: '闷蒸无法证明排气终点；整段都在排气。对约 90% 人，画圈/定点几乎无增益；冠军才用手法应对现场变量。滤杯发明逻辑是按参数注水，不是天天研究手法。',
        quote: '「闷蒸是一个伪命题」「手法没有任何用」[02:49][17:42]',
        pitfall: '把仪式感步骤当成科学终点。',
        action: '方案写清：水温区间、研磨相对杯测、极限时间、次数、粉水比；手法保持简单稳定即可。',
      },
    ],
    table: {
      title: '片中 V60 × 好豆示意方案',
      headers: ['变量', '作者示意', '逻辑'],
      rows: [
        ['水温', '96℃（好豆浅烘）', '90–96℃ 区间；榨干但不碰 100℃ 气化'],
        ['闷蒸', '不需要', '无法验证排净点；全程都在排气'],
        ['滤杯时钟', 'V60 ≈ 1′10″', '每次注水至滴尽不超过此时限'],
        ['研磨', '≥ 杯测研磨度', '略粗保香气；筛网验磨'],
        ['注水次数', '好豆可 4 次', '次数↑ → 浓度↑；常人三次是表象'],
        ['粉水比', '个人 1:14（15g→210g）', '按口味 1:13–1:15；每次≈65g'],
        ['手法', '多数人几乎无用', '稳定注水优先于画圈神话'],
      ],
    },
    boundary: [
      '极限下水时间、1′10″、1.1–1.3、1:14 等为口述示意，滤杯、海拔、豆况会变，需自测校准。',
      '「风味不对消费者说」是沟通策略主张，不否定风味轮在专业训练中的价值。',
      '否定闷蒸针对「无法验证的仪式」；若你的流程把首注当作稳定浸润，仍可用逻辑自洽的方式保留。',
      '手法无用论针对业余与多数爱好者；竞赛与极端条件另当别论。',
    ],
    pitfalls: [
      '迷信网上固定粉水比与三段式，不先问滤杯极限时间。',
      '香气不足却越磨越细，把木质味当风味。',
      '超时萃取却怪豆子或手法，忽略滤杯时钟。',
      '买磨不验证杯测研磨度，只听材质故事。',
      '把风味形容词灌给未训练感官的饮用者，替代酸甜苦平衡。',
    ],
    conclusion: {
      key: [
        '滤杯极限下水时间 > 浓度 > 其他口头参数',
        '研磨保香气（比杯测略粗）；水温落在 90–96℃',
        '粉水比与注水次数按口味调；别被闷蒸与手法绑架',
      ],
      actions: [
        '测/问清你常用滤杯的极限下水时间，并写进冲煮卡',
        '问磨厂杯测研磨度，手冲略粗，用筛网验一次',
        '用同一豆试 3 次 vs 4 次注水，在时限内找浓度甜点，再定个人粉水比',
      ],
      shift:
        '以前：抄三段式、纠结画圈与闷蒸秒数；现在：先钉死滤杯时钟与浓度，再用研磨保香气、用粉水比对齐口味——方法可以自由，逻辑不能空。',
    },
  },
  index: {
    summary:
      '手冲底层逻辑：先钉滤杯极限下水时间，再以注水次数与粉水比调浓度；研磨比杯测略粗保香气，水温90–96℃，破除闷蒸与手法迷信。约19分钟。',
    tags: ['手冲咖啡', '滤杯', '研磨度', '粉水比', '萃取', 'V60'],
  },
};

function upsertIndex(entry) {
  const indexPath = path.join(DOCS, 'index.json');
  const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
  const i = index.findIndex((e) => e.slug === entry.slug || e.url === entry.url);
  if (i >= 0) index[i] = { ...index[i], ...entry };
  else index.push(entry);
  fs.writeFileSync(indexPath, JSON.stringify(index, null, 2) + '\n');
}

const segs = loadSegments(ITEM.slug);
ITEM.duration = durationZh(ITEM.durationSec);

const html = buildHtml(ITEM, segs);
const htmlPath = path.join(DOCS, `${ITEM.slug}-图文实录.html`);
fs.writeFileSync(htmlPath, html, 'utf8');

const { svg, height } = await buildSvg({
  css: SVG_CSS,
  body: buildSvgBody({
    title: ITEM.svgTitle,
    tags: ITEM.svg.tags,
    duration: ITEM.duration,
    url: ITEM.url,
    summary: ITEM.svg.summary,
    timeline: ITEM.svg.timeline,
    map: ITEM.svg.map,
    corrections: ITEM.svg.corrections,
    cards: ITEM.svg.cards,
    table: ITEM.svg.table,
    boundary: ITEM.svg.boundary,
    pitfalls: ITEM.svg.pitfalls,
    conclusion: ITEM.svg.conclusion,
  }),
  width: 1320,
});
const svgPath = path.join(DOCS, `${ITEM.slug}-理性分析.svg`);
fs.writeFileSync(svgPath, svg, 'utf8');

const summary = ITEM.index.summary;
if ([...summary].length > 120) {
  console.warn('summary too long', [...summary].length);
}

const entry = {
  date: '2026-09-13',
  title: ITEM.title,
  summary,
  tags: ITEM.index.tags,
  platform: 'xiaohongshu',
  url: ITEM.url,
  duration: ITEM.duration,
  outputs: {
    html: `${ITEM.slug}-图文实录.html`,
    svg: `${ITEM.slug}-理性分析.svg`,
  },
  screenshot_count: 8,
  transcript_segments: segs.length,
  svg_height: height,
  slug: ITEM.slug,
  primary: ITEM.primary,
};
upsertIndex(entry);

const result = {
  slug: ITEM.slug,
  html: `docs/${ITEM.slug}-图文实录.html`,
  svg: `docs/${ITEM.slug}-理性分析.svg`,
  index: true,
  summary,
  shots: 8,
  segments: segs.length,
  svg_height: height,
  duration: ITEM.duration,
  primary: ITEM.primary,
};
console.log('OK', ITEM.slug, 'segs', segs.length, 'svg_height', height);
console.log(JSON.stringify(result, null, 2));
