#!/usr/bin/env node
/**
 * b56：espresso-types-explained / study-habit-three-steps / tulip-wiggle-valid-invalid
 * 生成图文实录 HTML + 理性分析 SVG，并 upsert docs/index.json
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.join(DIR, '..');
const DOCS = path.join(ROOT, 'docs');

function esc(s) {
  return String(s ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function fmt(t) {
  const s = Math.max(0, Math.floor(Number(t) || 0));
  return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
}

function loadWhisper(slug) {
  const j = JSON.parse(fs.readFileSync(path.join(ROOT, `${slug}.json`), 'utf8'));
  return (j.segments || []).filter((seg) => String(seg.text || '').trim());
}

function transcriptHtml(segs) {
  return segs
    .map(
      (seg) =>
        `<div class="transcript-row"><time>${fmt(seg.start)}</time><p>${esc(String(seg.text).trim())}</p></div>`,
    )
    .join('\n');
}

const CSS_HTML = `*{box-sizing:border-box}html{scroll-behavior:smooth}
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

const CSS_SVG = `*{margin:0;padding:0;box-sizing:border-box}
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
.timeline-time{font-size:14px;font-weight:700;color:#3b82f6;min-width:70px;font-variant-numeric:tabular-nums}
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

function buildHtmlDoc(d, segs) {
  const summaryRows = d.summary_rows
    .map(
      ([tr, label, txt]) =>
        `<div class="summary-row"><span class="time-marker">[${esc(tr)}]</span><div><strong>${esc(label)}</strong><p>${esc(txt)}</p></div></div>`,
    )
    .join('');
  const chapters = d.chapters
    .map((ch) => {
      const figs = (ch.figures || [])
        .map(
          (f) =>
            `<figure><img src="assets/${d.slug}/${f.file}" alt="${esc(f.alt)}" loading="lazy"><figcaption>[${esc(f.cap_time)}] ${esc(f.caption)}</figcaption></figure>`,
        )
        .join('');
      const paras = (ch.paras || []).map((p) => `<p>${esc(p)}</p>`).join('');
      return `<section class="story-section"><h3>${esc(ch.title)}</h3><span class="section-time">[${esc(ch.time)}]</span>${paras}${figs}</section>`;
    })
    .join('');
  return `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><meta name="description" content="${esc(d.description)}"><title>${esc(d.title)}｜图文实录</title><style>${CSS_HTML}</style></head><body><main class="container"><header><h1>${esc(d.title)}</h1><div class="meta"><span>来源：小红书</span><span>时长：${esc(d.duration)}</span></div><a class="original-link" href="${esc(d.url)}" target="_blank" rel="noopener">查看原视频</a></header><article class="documentary"><h2>内容要点</h2><p>${esc(d.lead)}</p><h3>知识结构</h3>${summaryRows}<div class="takeaway-box"><strong>核心口诀</strong><p>${esc(d.takeaway)}</p></div>${chapters}</article><section class="transcript-section" id="transcript"><details class="transcript-collapsible"><summary>详细文字转录（${segs.length}段）</summary><div class="transcript-body"><p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差。</p><div class="transcript-list">${transcriptHtml(segs)}</div></div></details></section></main><script>(function(){var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){d.setAttribute("open","")}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){a.addEventListener("click",open)});if(location.hash==="#transcript")open()})();</script></body></html>\n`;
}

function buildSvgBody(d) {
  const tags = (d.tags || [])
    .map((t, i) => `<span class="tag ${['tag-blue', 'tag-green', 'tag-orange', 'tag-purple', 'tag-red', 'tag-gray'][i % 6]}">${esc(t)}</span>`)
    .join('');
  const timeline = (d.timeline || [])
    .map(([t, x]) => `<div class="timeline-item"><span class="timeline-time">${esc(t)}</span><span class="timeline-text">${esc(x)}</span></div>`)
    .join('');
  const mapNodes = (d.map || [])
    .map(([label, x], i) => {
      const cls = ['node', 'node-green', 'node-orange', 'node-red'][i % 4];
      const arrow = i < d.map.length - 1 ? '<span class="arrow">→</span>' : '';
      return `<div class="${cls}">${esc(label)}<br/>${esc(x)}</div>${arrow}`;
    })
    .join('');
  const corrections = (d.corrections || []).map((c) => `<p>${esc(c)}</p>`).join('');
  const cards = (d.cards || [])
    .map(
      (c) => `<div class="card ${c.tone || ''}"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p>${
        c.quote ? `<div class="quote">${esc(c.quote)}</div>` : ''
      }${c.pitfall ? `<div class="pitfall">${esc(c.pitfall)}</div>` : ''}${
        c.action ? `<div class="action">${esc(c.action)}</div>` : ''
      }</div>`,
    )
    .join('');
  let tableBlock = '';
  if (d.table?.head) {
    const thead = `<tr>${d.table.head.map((h) => `<th>${esc(h)}</th>`).join('')}</tr>`;
    const tbody = d.table.rows.map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`).join('');
    tableBlock = `<div class="section"><h2 class="sec-title">${esc(d.table.title || '横向对比')}</h2><div class="card"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div></div>`;
  }
  const boundary = (d.boundary || []).map((b) => `<li>${esc(b)}</li>`).join('');
  const pitfalls = (d.pitfalls || []).map((p) => `<div class="pitfall">${esc(p)}</div>`).join('');
  const keyHtml = (d.conclusion?.key || []).map((k) => `<li>${esc(k)}</li>`).join('');
  const actionsHtml = (d.conclusion?.actions || []).map((a) => `<li>${esc(a)}</li>`).join('');
  return `<div class="container root-wrap">
  <h1>${esc(d.svg_title || d.title)}</h1>
  <div class="meta">${tags}<span class="tag tag-gray">时长 ${esc(d.duration)}</span><span class="tag tag-gray">理性分析</span></div>
  <a class="source-link" href="${esc(d.url)}">原视频</a>
  <div class="summary-line">${esc(d.summary)}</div>
  <div class="timeline"><h3>关键证据时间轴</h3>${timeline}</div>
  <div class="map"><h2>核心脉络</h2><div class="diagram">${mapNodes}</div></div>
  <div class="correction"><h3>常见误解与认知纠偏</h3>${corrections}</div>
  <div class="section"><h2 class="sec-title">观点拆解：在讲什么 → 关键理解 → 怎么用 → 原文依据</h2>${cards}</div>
  ${tableBlock}
  <div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${boundary}</ul>${pitfalls}</div></div>
  <div class="conclusion"><h2>总结与行动</h2><h3>核心要点</h3><ul>${keyHtml}</ul><h3>行动清单</h3><ol>${actionsHtml}</ol><h3>关键认知转变</h3><p>${esc(d.conclusion?.shift || '')}</p></div>
  <div class="footer">双轨产物之二 · 理性分析 · 证据来自同一 Whisper 转录 · ${esc(d.duration)}</div>
</div>`;
}

const ITEMS = {
  'espresso-types-explained': {
    slug: 'espresso-types-explained',
    title: '浓缩咖啡有哪些？',
    svg_title: '浓缩≠只有 Espresso：三种萃取对照',
    url: 'https://xhslink.cn/o/32Grn8RIzTy',
    duration: '50秒',
    primary: 'coffee',
    tags: ['咖啡', '浓缩', 'Espresso', 'Ristretto', 'Lungo'],
    description:
      '澄清「Espresso=浓缩」的常见误解：同粉量不同萃取时间得到不同液重，对应 Espresso / Ristretto / Lungo，口感差异大；咖啡店多用 Espresso 作基底。',
    lead:
      '很多人把 espresso 直接等同于「浓缩」。视频先肯定这个直觉，再纠偏：espresso 只是浓缩咖啡的一种。同用 18 克咖啡粉，用不同萃取时间与液重，可以得到 Espresso（约 22–35 秒、36 克）、Ristretto（约 15–18 秒、18 克）、Lungo（约 45–60 秒、54 克）——三者都是浓缩，但口感差别很大。店里常用 espresso 作基底，所以大众只熟悉它；最后用「泰迪是狗，但不是所有狗都叫泰迪」收束概念边界。',
    takeaway: 'Espresso 是浓缩，但浓缩不一定是 Espresso——同粉量、不同时间与液重，得到不同浓缩。',
    summary_rows: [
      ['00:00→00:10', '概念纠偏', '说 espresso 是浓缩「对，但不完全对」——它只是浓缩的一种。'],
      ['00:10→00:29', '三组参数', '同 18g 粉：Espresso 22–35s/36g；Ristretto 15–18s/18g；Lungo 45–60s/54g。'],
      ['00:29→00:40', '为何只知 Espresso', '店内多用 espresso 作基底，所以大众只了解它；屏幕给出基本数据。'],
      ['00:40→00:50', '比喻收束', '泰迪是狗，但不是所有狗都叫泰迪——浓缩同理。'],
    ],
    chapters: [
      {
        title: '对，但不完全对：Espresso 只是浓缩的一种',
        time: '00:00 → 00:10',
        paras: [
          '开场先给出画面里正在萃取的浓缩，再点破常识：有人叫它 espresso，于是默认 espresso=浓缩。「对，但不完全对」——espresso 只是浓缩咖啡的一种，今天要讲还有哪些。',
        ],
        figures: [
          {
            file: 'shot-01.jpg',
            alt: '机头萃取中，字幕「对但不完全对」',
            cap_time: '00:05',
            caption: '机头双嘴出液，字幕钉住「对但不完全对」——直觉可半对',
          },
        ],
      },
      {
        title: '同粉量三组配方：Espresso / Ristretto / Lungo',
        time: '00:10 → 00:29',
        paras: [
          '统一粉量 18 克：Espresso 约 22–35 秒萃出约 36 克液，是大家最熟悉的那杯；Ristretto 约 15–18 秒、约 18 克液（转录误作 Rosgretto）；Lungo 约 45–60 秒、约 54 克液（转录误作 Lango）。相同粉重、不同时间与液重，得到三份都叫浓缩、口感却差很多的咖啡。',
        ],
        figures: [
          {
            file: 'shot-02.jpg',
            alt: 'Espresso 36g 与 22-35 秒标注',
            cap_time: '00:15',
            caption: 'Espresso：22–35 秒萃取约 36 克咖啡液',
          },
          {
            file: 'shot-03.jpg',
            alt: '三列对照：Ristretto / Espresso / Lungo',
            cap_time: '00:23',
            caption: '同粉量三列对照：18g / 36g / 54g 液重与时间区间',
          },
        ],
      },
      {
        title: '为何大众只认识 Espresso，以及泰迪比喻',
        time: '00:29 → 00:50',
        paras: [
          '一般咖啡馆用 espresso 作基底，所以大部分人只了解到它的存在；屏幕上的基本数据可自行对照。收束给中心思想：你可以打比方说「泰迪是狗，但不是所有狗都叫泰迪」——espresso 是浓缩，浓缩却不一定是 espresso。',
        ],
        figures: [
          {
            file: 'shot-04.jpg',
            alt: '三列口感与适用饮品表',
            cap_time: '00:34',
            caption: '屏幕数据：比例、时间、咖啡因与适用饮品一览',
          },
          {
            file: 'shot-05.jpg',
            alt: '字幕「给你打个比方」',
            cap_time: '00:41',
            caption: '收束比喻：泰迪是狗，但不是所有狗都叫泰迪',
          },
        ],
      },
    ],
    // SVG fields
    summary:
      '同 18g 粉、不同萃取时间与液重，得到 Espresso / Ristretto / Lungo 三种浓缩；大众只熟悉 Espresso，是因为店内多拿它做基底，不等于浓缩只有这一种。',
    timeline: [
      ['00:00', '立题：espresso 叫浓缩「对但不完全对」'],
      ['00:10', '统一 18g 粉，给出三组时间与液重'],
      ['00:15', 'Espresso：22–35s → 36g'],
      ['00:17', 'Ristretto：15–18s → 18g'],
      ['00:20', 'Lungo：45–60s → 54g'],
      ['00:31', '店内多用 espresso 作基底，故大众只知它'],
      ['00:42', '比喻：泰迪是狗 ≠ 所有狗都叫泰迪'],
    ],
    map: [
      ['同粉量 18g', '控制变量'],
      ['改时间/液重', '得到三种浓缩'],
      ['Espresso 最常见', '因作基底'],
      ['概念边界', '浓缩 ⊃ Espresso'],
    ],
    corrections: [
      '误解：听到 espresso 就等于「浓缩咖啡」的全部。纠偏：它是浓缩家族里的一种配方参数。',
      '误解：液重更大就一定「更浓」。纠偏：Lungo 时间更长、液重更大，口感往往更苦、风味更淡（屏幕标注）。',
      'ASR 纠偏：Rosgretto→Ristretto，Lango→Lungo。',
    ],
    cards: [
      {
        title: '控制变量：同粉量才谈「种类」',
        body: '视频反复强调「相同重量的咖啡粉」。种类差异来自萃取时间与目标液重，而不是再换一包豆子。',
        quote: '「相同重量的咖啡粉，不同时间萃取不同重量的咖啡液，我们得到不同的三份都是浓缩咖啡」[00:22–00:29]',
        tone: 'card-green',
      },
      {
        title: '三组可记参数',
        body: 'Espresso≈22–35s/36g；Ristretto≈15–18s/18g；Lungo≈45–60s/54g。屏幕另给比例、咖啡因与适用饮品，可当作入门对照表。',
        quote: '「22–35秒萃取36克……15–18秒……45–60秒萃取54克」[00:12–00:22]',
        action: '练习时先锁粉量，只改停表液重，对比一口酸苦与厚度。',
      },
      {
        title: '为何你只听过 Espresso',
        body: '不是市场只有一种浓缩，而是门店出品链默认用它打奶咖基底，曝光最高。',
        quote: '「一般咖啡馆都是 espresso 作为咖啡基底来使用，所以大部分人只了解到 espresso 的存在而已」[00:31–00:37]',
        pitfall: '别把「常见」当成「唯一合法定义」。',
        tone: 'card-orange',
      },
    ],
    table: {
      title: '三种浓缩（视频给定粉量下）',
      head: ['类型', '时间', '液重', '一句话'],
      rows: [
        ['Espresso', '22–35s', '≈36g', '最常见基底'],
        ['Ristretto', '15–18s', '≈18g', '更短更少液'],
        ['Lungo', '45–60s', '≈54g', '更长更多液'],
      ],
    },
    boundary: [
      '参数是教学示意，不同机型/研磨/粉碗会偏移，需按实际校准。',
      '「浓缩家族」此处按意式高压萃取讨论，不含手冲浓郁感。',
    ],
    pitfalls: [
      '只背名字不锁粉量，对比无效。',
      '把 Lungo 当「更浓」点单，可能得到更稀更苦的一杯。',
    ],
    conclusion: {
      key: [
        'Espresso ⊂ 浓缩，不是全等。',
        '同粉量下，时间与液重决定种类与口感。',
        '门店习惯解释「知名度」，不解释「定义边界」。',
      ],
      actions: [
        '用同一粉量拉三杯，只改目标液重，盲品记录。',
        '点单时问清「Ristretto / Espresso / Lungo」或比例，而不是只说「来杯浓缩」。',
      ],
      shift: '从「名字=品类」转向「粉量固定下的时间–液重配方族」。',
    },
  },

  'study-habit-three-steps': {
    slug: 'study-habit-three-steps',
    title: '从现在开始养成好习惯！每一步都很关键',
    svg_title: '五步学习闭环：对准「不会」',
    url: 'https://xhslink.cn/o/53Oq6q9mHU2',
    duration: '17秒',
    primary: 'other',
    tags: ['学习', '习惯', '方法'],
    description:
      '短视频给出高校学习法的五步闭环：预习找不会、上课解决不会、做题检验不会、复习死磕不会、改错消灭不会——关键不是比聪明，而是把「不会」走完闭环。',
    lead:
      '画面标题强调「告诉孩子学习一定记住这 5 步，每一步形成闭环」。口播把五步钉在同一目标词「不会」上：预习找出不会、上课解决不会、做题检验不会、复习死磕（此刻）不会、改错消灭不会。这是「语会闭环」的高校学习法——重点不是比谁疏通得快，而是把不会走完闭环，学明白。',
    takeaway: '学习习惯的核心不是「多花时间」，而是每一步都对准「不会」，形成找→解→检→磕→灭的闭环。',
    summary_rows: [
      ['00:00→00:04', '预习 / 上课', '预习找出不会；上课解决不会。'],
      ['00:04→00:08', '做题 / 复习', '做题检验不会；复习死磕此刻不会。'],
      ['00:08→00:13', '改错与闭环', '改错消灭不会；五步构成语会闭环。'],
      ['00:13→00:17', '心态纠偏', '不是比你更「聪明疏通」，会学习就明白了。'],
    ],
    chapters: [
      {
        title: '五步都对准同一个词：不会',
        time: '00:00 → 00:10',
        paras: [
          '口播一口气排开：预习是找出不会的，上课是解决不会的，做题是检验不会的，复习是此刻不会的，改错是消灭不会的。屏幕同步打出对应字幕，把习惯拆成可执行的五步，而不是空泛「好好学」。',
        ],
        figures: [
          {
            file: 'shot-01.jpg',
            alt: '字幕：预习是找出不会的',
            cap_time: '00:02',
            caption: '预习是找出不会的——闭环入口',
          },
          {
            file: 'shot-02.jpg',
            alt: '字幕：做题是检验不会的',
            cap_time: '00:05',
            caption: '做题是检验不会的——用题目验证缺口',
          },
          {
            file: 'shot-03.jpg',
            alt: '字幕：复习是死磕不会的',
            cap_time: '00:07',
            caption: '复习是死磕不会的——对准残留缺口',
          },
        ],
      },
      {
        title: '闭环与心态：会学习，而不是比聪明',
        time: '00:10 → 00:17',
        paras: [
          '口播总结：这是语会闭环的高校学习法。屏幕文案写「每一步形成闭环，真正学懂学透」；结尾强调别人不是比你更聪明（画面字幕），会学习就明白了——方法感强过天赋叙事。',
        ],
        figures: [
          {
            file: 'shot-04.jpg',
            alt: '字幕：这是五步闭环的',
            cap_time: '00:11',
            caption: '收束：这是五步闭环的高校学习法',
          },
          {
            file: 'shot-05.jpg',
            alt: '字幕：别人不是比你聪明',
            cap_time: '00:14',
            caption: '心态纠偏：别人不是比你聪明，关键是会学习',
          },
        ],
      },
    ],
    summary:
      '把学习拆成五步闭环，每一步都服务于「不会」：找、解、检、磕、灭；习惯养成的关键是闭环，而不是天赋比较。',
    timeline: [
      ['00:00', '再强调一遍：进入五步'],
      ['00:01', '预习＝找出不会'],
      ['00:03', '上课＝解决不会'],
      ['00:04', '做题＝检验不会'],
      ['00:06', '复习＝死磕此刻不会'],
      ['00:08', '改错＝消灭不会'],
      ['00:10', '五步＝语会闭环的高校学习法'],
      ['00:13', '不是比聪明，会学习就明白'],
    ],
    map: [
      ['预习', '找不会'],
      ['上课', '解不会'],
      ['做题', '检不会'],
      ['复习', '磕不会'],
      ['改错', '灭不会'],
    ],
    corrections: [
      '误解：标题像「三步」，内容实为五步闭环——以口播与画面「5 步」为准。',
      '误解：复习=再看一遍笔记。纠偏：口播是「死磕此刻不会」。',
      '误解：成绩差是因为不够聪明。纠偏：画面强调「别人不是比你聪明」。',
    ],
    cards: [
      {
        title: '同一动词链：不会',
        body: '五步共用宾语「不会」，保证习惯动作始终对准缺口，而不是表演「学了很久」。',
        quote: '「预习是找出不会的……改错是消灭不会的」[00:01–00:10]',
        tone: 'card-green',
      },
      {
        title: '闭环比单点努力更重要',
        body: '只预习不改错，缺口会回流；只做题不复习，检验结果无法沉淀。标题「每一步都很关键」指的是链上每环。',
        quote: '「这是语会闭环的高校学习法」[00:10–00:13]',
        action: '每天用五格清单勾选：找/解/检/磕/灭，缺一格就补。',
      },
      {
        title: '方法叙事压过天赋叙事',
        body: '短视频用「会学习明白了」收束，把习惯归因从智商转向流程。',
        quote: '画面字幕：「别人不是比你聪明」[约 00:14]',
        tone: 'card-orange',
      },
    ],
    table: {
      title: '五步与「不会」的关系',
      head: ['步骤', '动作', '对「不会」做什么'],
      rows: [
        ['预习', '找', '暴露缺口'],
        ['上课', '解', '当场处理'],
        ['做题', '检', '验证是否真会'],
        ['复习', '磕', '盯残留'],
        ['改错', '灭', '关闭缺口'],
      ],
    },
    boundary: [
      '口播面向学习习惯，尤其学龄/高校场景；职场技能需自行映射。',
      '17 秒只给骨架，具体预习怎么找、错题怎么归档需另补。',
    ],
    pitfalls: [
      '把五步做成打卡表演，不问「今天消灭了哪条不会」。',
      '跳过改错，导致「检验」结果无法闭环。',
    ],
    conclusion: {
      key: [
        '习惯=对准「不会」的五步闭环。',
        '每一步换动词，但宾语不变。',
        '方法感优先于聪明叙事。',
      ],
      actions: [
        '今晚只做一件事：把错题本里的一条「不会」走完改错。',
        '预习时强制写下 3 个「不会」问题再去听课。',
      ],
      shift: '从「我要努力学习」转向「我要闭环处理不会」。',
    },
  },

  'tulip-wiggle-valid-invalid': {
    slug: 'tulip-wiggle-valid-invalid',
    title: '郁金香拉花有效摆动和无效摆动',
    svg_title: '压纹郁金香：有效摆动 vs 无效摆动',
    url: 'https://xhslink.cn/o/4M3PrjZbfhv',
    duration: '1分4秒',
    primary: 'coffee',
    skills: ['拉花'],
    tags: ['咖啡', '拉花', '郁金香', '摆动', '压纹'],
    description:
      '诊断压纹郁金香「摆很多层却不清晰、底部偏厚」：那是无效摆动。有效摆动要求流量别太小，且每一摆都向前推进，让每条纹路可追溯，从而用更少奶泡做出同样效果，并留奶给后段。',
    lead:
      '主题是压纹郁金香的有效摆动与无效摆动。很多人为了层数多，原地猛摆：第二段却摆不清晰，完成后底部很厚、纹路也不清楚——这就是无效摆动。改善要点：流量不要太小；每一摆都向前推进，而不是原地摆很多下再往前推。这样做能用更少奶泡做出同样效果，也把更多奶泡留给后段制作；有效摆动的判据是每一下纹路都能找到那条线的根源。',
    takeaway: '有效摆动=流量够 + 每摆向前推；无效摆动=原地狂摆，层多但纹不清、底厚。',
    summary_rows: [
      ['00:00→00:25', '无效摆动症状', '喜摆很多层→后段不清晰→底厚、纹路不清。'],
      ['00:26→00:42', '改法两要点', '流量别太小；每一下摆动都往前推进，非原地狂摆。'],
      ['00:42→01:04', '有效判据', '更少奶泡同效果、后段更有奶；每条纹路可追溯根源。'],
    ],
    chapters: [
      {
        title: '无效摆动：层很多，但底厚纹不清',
        time: '00:00 → 00:26',
        paras: [
          '开场提问有效/无效摆动是什么。很多人做郁金香时喜欢摆很多层，第二段又觉得摆不清晰；做完发现底部非常厚、纹路也不清楚——口播点名：这就是无效摆动。',
        ],
        figures: [
          {
            file: 'shot-01.jpg',
            alt: '标题：压纹郁金香有效/无效摆动',
            cap_time: '00:08',
            caption: '立题：压纹郁金香的有效摆动与无效摆动',
          },
          {
            file: 'shot-02.jpg',
            alt: '反例标注「底很厚」',
            cap_time: '00:18',
            caption: '无效结果：底部很厚，纹路不清晰',
          },
        ],
      },
      {
        title: '有效摆动：流量够，且每摆向前推',
        time: '00:26 → 01:04',
        paras: [
          '改善方法：做压纹郁金香时流量一定不要太小；然后每一摆都要往前推进，并不是在原地摆很多下再往前推。这样能用更少奶泡做出同样效果，也能把更多奶泡留给后段。有效摆动的可见判据：每一下纹路都能找到那条线的根源。学会了就去评论区交作业。',
        ],
        figures: [
          {
            file: 'shot-03.jpg',
            alt: '演示压纹郁金香倒奶',
            cap_time: '00:32',
            caption: '操作提醒：流量不要太小',
          },
          {
            file: 'shot-04.jpg',
            alt: '细密压纹层在成形',
            cap_time: '00:44',
            caption: '每摆向前推：更少奶泡做出同样层次',
          },
          {
            file: 'shot-05.jpg',
            alt: '标注「有效摆动」',
            cap_time: '00:55',
            caption: '有效判据：每一下纹路都能追溯到那条线',
          },
        ],
      },
    ],
    summary:
      '无效摆动是原地狂摆：层多但底厚、纹不清；有效摆动要求流量足够，且每一摆都向前推进，让纹路可追溯，并省奶给后段。',
    timeline: [
      ['00:00', '立题：有效 vs 无效摆动'],
      ['00:06', '常见：喜欢摆很多层'],
      ['00:11', '第二段摆不清晰'],
      ['00:14', '结果：底很厚、纹路不清＝无效'],
      ['00:28', '改法：流量不要太小'],
      ['00:34', '每一摆都往前推进'],
      ['00:38', '不是原地摆很多下再往前'],
      ['00:42', '更少奶泡同效果 + 后段更有奶'],
      ['00:52', '有效＝每条纹路找得到根源'],
    ],
    map: [
      ['无效', '原地狂摆'],
      ['症状', '底厚纹糊'],
      ['有效', '摆+前推'],
      ['收益', '省奶可追溯'],
    ],
    corrections: [
      '误解：摆动次数越多越好。纠偏：无效摆动就是「很多下却没在纹路上体现」。',
      '误解：先原地摆够层数再往前推。纠偏：每一摆都要带前推。',
      'ASR：鸦纹→压纹（与画面标题一致）。',
    ],
    cards: [
      {
        title: '无效摆动的可观察结果',
        body: '层数看起来很多，但完成后底部厚、纹路不清——流量堆在原地，没有水平推进。',
        quote: '「这种郁金香的底会非常的厚，纹路又没有很清晰，这也就是我们所说的无效摆动」[00:14–00:25]',
        pitfall: '用「层数」当唯一 KPI，忽略清晰度与底部厚度。',
        tone: 'card-red',
      },
      {
        title: '有效摆动的两个硬条件',
        body: '① 流量不要太小；② 每一摆都向前推进，而不是定点狂摆后再平移。',
        quote: '「流量一定要保证不要太小，然后每一下摆动都要往前推进，并不是在原地摆很多下然后再往前推进」[00:31–00:41]',
        action: '练习时数「摆一下、推一点」，禁止定点连摆超过两下。',
        tone: 'card-green',
      },
      {
        title: '为什么有效摆动更省奶、后段更自由',
        body: '每一下都在纹路上留下可辨线迹，单位奶泡信息密度更高，于是可用更少奶泡达到同样视觉，并把余量留给后段收尾。',
        quote: '「用更少的奶泡做出同样的效果……用更多的奶泡在后段的制作当中」[00:42–00:51]',
      },
    ],
    table: {
      title: '有效 vs 无效',
      head: ['对比', '无效摆动', '有效摆动'],
      rows: [
        ['缸嘴路径', '原地多摆再推', '每摆都前推'],
        ['视觉', '底厚、纹糊', '纹路可追溯'],
        ['奶泡预算', '前段耗尽', '省奶留给后段'],
        ['判据', '层数多', '每一下都在纹路上'],
      ],
    },
    boundary: [
      '针对压纹郁金香的摆动段；融合高度、奶泡质地另题。',
      '「流量不要太小」需结合杯型与奶缸嘴，避免冲破 crema。',
    ],
    pitfalls: [
      '流量过小导致纹路写不进去，再怎么摆也是无效。',
      '只练摆幅不练前推，重复无效习惯。',
    ],
    conclusion: {
      key: [
        '无效=摆很多但纹路不体现。',
        '有效=流量够 + 每摆前推。',
        '目标是可追溯纹路与奶泡预算，不只是层数。',
      ],
      actions: [
        '下一杯刻意减少摆次，强制每摆前移 3–5mm。',
        '拍俯视图，检查是否每条线都能追到注入点。',
      ],
      shift: '从「多摆几下」转向「每一摆都在纹路上记账」。',
    },
  },
};

async function main() {
  const heights = {};
  for (const slug of Object.keys(ITEMS)) {
    const d = ITEMS[slug];
    const segs = loadWhisper(slug);

    const html = buildHtmlDoc(d, segs);
    const htmlPath = path.join(DOCS, `${slug}-图文实录.html`);
    fs.writeFileSync(htmlPath, html, 'utf8');
    console.log('HTML', htmlPath, 'segs', segs.length);

    const { svg, height } = await buildSvg({ css: CSS_SVG, body: buildSvgBody(d), width: 1320 });
    const svgPath = path.join(DOCS, `${slug}-理性分析.svg`);
    fs.writeFileSync(svgPath, svg, 'utf8');
    heights[slug] = height;
    console.log('SVG', svgPath, 'height', height);
  }

  // upsert index.json — re-read immediately before write
  const indexPath = path.join(DOCS, 'index.json');
  const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
  const bySlug = new Map(index.map((e, i) => [e.slug, i]));

  for (const slug of Object.keys(ITEMS)) {
    const d = ITEMS[slug];
    const segs = loadWhisper(slug);
    const entry = {
      date: '2026-09-12',
      title: d.title,
      summary: d.summary,
      tags: d.tags,
      platform: 'xiaohongshu',
      url: d.url,
      duration: d.duration,
      outputs: {
        html: `${slug}-图文实录.html`,
        svg: `${slug}-理性分析.svg`,
      },
      screenshot_count: 5,
      transcript_segments: segs.length,
      svg_height: heights[slug],
      slug,
      primary: d.primary,
    };
    if (d.skills) entry.skills = d.skills;

    if (bySlug.has(slug)) {
      index[bySlug.get(slug)] = { ...index[bySlug.get(slug)], ...entry };
      console.log('index update', slug);
    } else {
      index.push(entry);
      console.log('index append', slug);
    }
  }

  fs.writeFileSync(indexPath, JSON.stringify(index, null, 2) + '\n', 'utf8');
  console.log('index.json total', index.length);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
