#!/usr/bin/env node
/** B57：espresso-machine-grind-dial → 图文实录 HTML + 理性分析 SVG + index.json */
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
  slug: 'espresso-machine-grind-dial',
  title: '13分钟教会你咖啡机调磨 小白也能变高手',
  shortTitle: '13分钟教会你咖啡机调磨',
  svgTitle: '意式调磨：先钉死 18g/30s/36g，再谈粗细、区间与酸苦平衡',
  url: 'https://xhslink.cn/o/2D4CZQoofgP',
  durationSec: 747,
  primary: 'coffee',
  description:
    '意式调磨底层逻辑：先定 18g 粉 / 30s / 36g 液，再按流速调粗细；洗磨、压粉、放水、可接受区间与酸苦平衡。约12分27秒实操全记录。',
  lead: '网上标准未必直接套用你的机与豆——要先学会底层逻辑。作者把调磨拆成两段：先不管好不好喝，钉死目标「18 克粉、30 秒、萃取 36 克液」，在同一台磨豆机与咖啡机上反复洗磨、称粉、布粉、压粉、放水、上粉，用流速判断偏细还是偏粗；再用「大约每差 5 秒调一格」把刻度从太细（35 秒几乎不出液、43 秒才 38 克）推到偏粗（22 秒已 41 克），落在约 1.7–2.0 的区间，最后一把约 28 秒近目标。随后才谈风味：浓缩喝的是酸苦平衡与回甘，油脂主要是视觉；理想值之外给出家用/门店可接受区间（粉 18–19g、时 25–30s、液 30–36g）。收束：天气气压与换豆才需要重调；咖啡师是豆—磨—机之间的连接器，今天只是皮毛。',
  takeaway:
    '先钉死 18g/30s/36g → 流速慢/无油脂=太细调粗，太快=调细；每约 5 秒一格；再谈酸苦平衡。理想值难天天中，落在可接受区间就算调磨成功。',
  structure: [
    ['00:00→00:30', '立题与目标', '意式最难；先定 18g/30s/36g，调完再评判好喝。'],
    ['00:30→01:10', '洗磨必做', '少倒豆磨净丢弃：清掉刀盘旧粉，意式就是费粉。'],
    ['01:10→02:00', '盲测第一把', '填满粉碗先萃：35s 几乎不出液、无油脂 → 太细。'],
    ['02:00→02:50', '调粗与四变量', '刻度 1.2→1.8；粉/液/时固定后，第四变量是刻度盘。'],
    ['02:50→04:00', '称粉与压粉', '动作一致；压平压实即可，力道比不过机端约 9 bar。'],
    ['04:00→04:40', '第二把与换算', '43s/38g 仍细；差 13s≈3 个 5 秒 → 调到约 2。'],
    ['04:40→06:00', '放水上粉与第三把', 'E61 冲煮头放水降温；流速变快、油脂变好 → 再调细。'],
    ['06:00→08:10', '区间与理想值', '1.7–2.0；28s 近成；理想值 vs 25–30s/30–36g 可接受区间。'],
    ['08:10→09:55', '风味与回甘', '酸苦平衡优先；油脂次要；清水演示回甘。'],
    ['09:55→11:00', '门店定量与豆子边界', '高杯量靠定量；区间内约六七成豆好喝。'],
    ['11:00→12:27', '天气与连接器', '换豆/气压变才重调；咖啡师连接豆磨机。'],
  ],
  chapters: [
    {
      range: '00:00 → 00:30',
      title: '先定目标，再谈好喝',
      paras: [
        '开场声明：约 13 分钟讲清意式咖啡机调磨，小白也能上手。意式是做咖啡里最难的一块——不是网上所有标准、视频都能直接套到你的机与豆上，你要先掌握基础逻辑。',
        '条目一：先给自己定目标。作者要求的目标是 18 克咖啡粉、30 秒时间、萃取 36 克咖啡液。此刻不要管好不好喝：给你一台磨豆机、一台咖啡机，就按这个目标调；调完之后再评判风味，再做微调。',
      ],
      figures: [],
    },
    {
      range: '00:30 → 01:10',
      title: '洗磨：看起来浪费，其实是清刀盘',
      paras: [
        '实操从磨豆机开始：打开豆仓开关，先少倒一点豆子，把粉磨完。这点粉直接不要——很浪费，但意式就是这么浪费。这一步叫洗磨：你不知道刀盘里之前磨过什么豆、放了多久；只有用新粉把旧粉「洗掉」，后续刻度判断才干净。',
        '洗磨完成后正式倒豆。第一轮可以先不管精确重量：粉碗按 18 克规格，先磨到大概铺平、填满即可，按作者方法走，避免一开始就被称重吓退。',
      ],
      figures: [
        {
          file: 'shot-01.jpg',
          time: '00:44',
          alt: '拍打豆仓把咖啡粉磨完，字幕「然后把整个的咖啡粉磨完」',
          cap: '洗磨现场：少倒豆、磨净、丢弃——清掉刀盘残留，再进入正式称粉',
        },
      ],
    },
    {
      range: '01:10 → 02:00',
      title: '第一把盲萃：太细的现场证据',
      paras: [
        '直接上机萃取。细节一：一边流一边不流，往往是机器没放平。关掉时已约 35 秒，只出极少咖啡液，且几乎看不到油脂；流速慢、无油脂，说明研磨太细——水难穿过粉层。',
        '诊断清楚后调粗：刚才约 1.2，先调到 1.6，再定到 1.8。调完还要把机内细粉再洗磨一遍，否则新旧研磨度混在一起，下一把仍会骗人。',
      ],
      figures: [
        {
          file: 'shot-02.jpg',
          time: '02:00',
          alt: '双手转动磨豆机刻度环，字幕「那我们把它磨粗一点」',
          cap: '粗细判断：粉太细 → 水难过粉层 → 调粗一丢丢（示意 1.2→1.8）',
        },
      ],
    },
    {
      range: '02:00 → 02:50',
      title: '四个变量：粉、液、时，最后钉死刻度',
      paras: [
        '正式定目标：18 克粉、萃 36 克液、30 秒。粉量、液量、时间都固定后，第四个要固定的变量就是磨豆机刻度盘——先找到能复现的刻度，细节才可谈。',
        '称粉时深烘豆可能偏轻偏重（示意到过 20 克），作者强调：先别管中烘深烘浅烘叙事，按方法把粉量调回约 18 克；操作动作全程保持一致。',
      ],
      figures: [],
    },
    {
      range: '02:50 → 04:00',
      title: '布粉、压粉：目的是压平压实，不是比力气',
      paras: [
        '布粉器放上铺匀，再用粉锤压粉。常见纠结是「使多大劲」：有人轻轻压、有人按重量压。作者指出：萃取时机器端提供约 9 bar 的稳定压力，换算到粉碗表面相当于约 250 公斤量级的力——你压粉再大力也比不过机端。压粉唯一目的是压平压实，不要在小劲大劲上自我较劲。',
        '怎么确保压平？练。标准动作提示：手柄轴线与手臂成一线，压粉唇垂直下压。上机前冲煮头放水约三秒即可。',
      ],
      figures: [],
    },
    {
      range: '04:00 → 04:40',
      title: '第二把仍细：用「每 5 秒一格」粗调',
      paras: [
        '机器仍可能不平。结果：43 秒才萃出约 38 克——相对 30 秒目标偏慢，粉仍太细，刀盘间距偏小。这把废掉后继续调粗。',
        '简易换算：43−30=13 秒，大约每差 5 秒调粗一格 → 约 3 格。从约 1.7–1.8 调到 2 再多一丢丢。仍要短时放粉洗磨（约 2–3 秒），再称到约 18.4→拨回 18 克；每一杯都要过秤。布粉、粉锤压粉、再放水。',
      ],
      figures: [
        {
          file: 'shot-03.jpg',
          time: '03:59',
          alt: '冲煮头下秤与奶缸，字幕「这机器还是不平」',
          cap: '第二把计时称重现场：机器不平会影响双侧出液，先排除再读流速',
        },
      ],
    },
    {
      range: '04:40 → 06:00',
      title: '为何放水、如何上粉，以及第三把偏粗',
      paras: [
        '细节：有的机不需要每次放水；这台冲煮头为 E61（ASR 作 161），有利于水温稳定，但久不萃时头部会过热，放一点水是为降温。上粉：意式把手双耳多数约 45° 平着推入、卡住再拧紧。',
        '第三把流速明显变快、前十秒油脂也好看——想要油脂，往往要把粉磨得相对粗一些。两次有效微调后，这台磨×这台机×这豆的区间落在约 1.7–2.0。但 22 秒已萃约 41 克，流速过快（粉太粗）→ 再调细到约 1.9。提醒：这一切不是为「这一杯好喝」，而是为找到刻度——这才叫调磨。意式费粉，所以店里与认真在家做的人常买公斤装。',
      ],
      figures: [
        {
          file: 'shot-04.jpg',
          time: '05:57',
          alt: '目标 18g/30s/36g 对照现在 22s/41g（粉太粗）',
          cap: '第三把诊断：相对目标过快过满 → 粉太粗，刻度再细一丢丢',
        },
      ],
    },
    {
      range: '06:00 → 08:10',
      title: '近成功、理想值与可接受区间',
      paras: [
        '再调细再萃：约 28 秒、约 41 克液——差两秒，几乎成了。作者坦白：下一次即使刻度与动作看似不变，参数仍可能漂——拼配豆比例、压粉力度都无法绝对复现。所谓「30 秒萃 18 克粉得 36 克液」是理想值；开店一天可能只有一两把完美中靶，下一把又偏。',
        '因此给出可接受区间：时间约 25–30 秒，粉约 18–19 克，液约 30–36 克——落在区间就算调磨成功，不必迷信每一次都刚好 30/36。',
      ],
      figures: [
        {
          file: 'shot-05.jpg',
          time: '07:52',
          alt: '理想值 18g/30s/36g 与参考区间对照讲解',
          cap: '理想值 vs 参考区间：调磨成功看区间，不看每一把是否完美中靶',
        },
      ],
    },
    {
      range: '08:10 → 09:55',
      title: '好喝是什么：酸苦平衡，油脂其次',
      paras: [
        '下一问：这杯到底好不好喝？表面油脂好看，但喝到的是酸涩与来得慢的微苦。作者主张：喝浓缩主要是喝酸苦平衡，不是追复杂风味叙事；油脂在意式里最不重要，多半是视觉好看。',
        '现场品饮：酸甜苦较平衡；甜往往难直接感知。倒清水漱口后觉得「水甜、有回甘」——不是水加了糖，而是酸苦刺激下降后舌头对甜的相对感知上来。门店目标：酸与苦平衡，并把酸苦的「距离」拉长；极甜豆子很贵，生意要算成本。',
      ],
      figures: [],
    },
    {
      range: '09:55 → 11:00',
      title: '门店不靠每杯电子秤，家用仍可用秤学',
      paras: [
        '日产两三百甚至四百杯时，不可能每杯都像教学那样反复称重计时。意式机常有定量功能；家里杯量少，仍可按称重方法学，但调一次磨很费粉——所以要学底层逻辑，而不是只抄一个网上刻度。',
        '区间里仍可能遇到不好喝的豆：作者经验约六七成日常豆在这套目标下会过得去；极差拼配与极贵豆是两端例外。对开店能买到的日常豆，这套数值已够用。',
      ],
      figures: [
        {
          file: 'shot-06.jpg',
          time: '09:58',
          alt: '讲师竖拇指，字幕「比如说每天出杯」',
          cap: '出品现实：高杯量靠定量与稳定手感；家用低频可继续用秤练',
        },
      ],
    },
    {
      range: '11:00 → 12:27',
      title: '何时重调：天气气压、换豆；咖啡师是连接器',
      paras: [
        '总结：意式难，早上常要调磨。两类触发：天气变化、换豆子。连续晴天温湿度气压近似，可能四五天甚至一周才调一次；刮风下雨大气压改变时，机内约 9 bar 相对外界的压差变了，萃取就会变，通常要调。',
        '咖啡师最难的不是「把某一杯吹得天花乱坠」，而是任意豆、任意磨、任意机之间承担连接：豆→磨成粉→机端萃取，中间全是人。今天只是底层皮毛；后续还有感官训练与操作一致性。做一两年的人都会这些——关键是先会这套逻辑。',
      ],
      figures: [
        {
          file: 'shot-07.jpg',
          time: '11:25',
          alt: '讲解机端约 9 bar 压力与萃取关系',
          cap: '气压与 9 bar：外界压强一变，同样机压下的萃取表现也会跟着变',
        },
      ],
    },
  ],
  svg: {
    tags: ['意式', '调磨', '研磨度', '18g/30s/36g', '酸苦平衡', '洗磨'],
    summary:
      '先钉死 18g 粉 / 30s / 36g 液，用流速判粗细并按约每 5 秒一格微调；找到刻度区间后再谈酸苦平衡。理想值难天天中，落在可接受区间即算成功。',
    timeline: [
      ['00:00', '立题：意式调磨底层逻辑'],
      ['00:16', '目标：18g / 30s / 36g，先别管好喝'],
      ['00:53', '洗磨：清刀盘旧粉，接受费粉'],
      ['01:45', '第一把：35s 几乎不出液 → 太细'],
      ['02:00', '调粗 1.2→1.8，再洗磨'],
      ['02:16', '四变量：粉、液、时、刻度'],
      ['03:00', '压粉：压平压实；机端约 9 bar'],
      ['04:03', '第二把：43s/38g 仍细；每 5 秒一格'],
      ['05:04', 'E61 放水降温；45° 上粉'],
      ['05:57', '第三把：22s/41g 太粗 → 调细至 ~1.9'],
      ['06:56', '近成功：~28s；理想值 vs 可接受区间'],
      ['08:13', '风味：酸苦平衡；油脂次要'],
      ['08:54', '清水回甘演示'],
      ['09:55', '门店定量；家用秤练'],
      ['10:57', '换豆/天气才重调；咖啡师是连接器'],
    ],
    map: ['钉死目标参数', '流速判粗细', '洗磨+微调刻度', '区间内谈酸苦'],
    corrections: [
      'ASR：意识/一式/一时→意式；洗墨/调墨→洗磨/调磨；催取/催→萃取。',
      'ASR：9%的压力→约 9 bar；高盘间距→刀盘间距；161冲煮头→E61 冲煮头。',
      'ASR：粉锤鸭粉→粉锤压粉；咖啡盐→咖啡液；纵长→已经。',
      '误解：网上标准刻度可直接抄。纠偏：先学 18g/30s/36g 逻辑，再落在你的机与豆上。',
      '误解：调磨是为立刻好喝。纠偏：先找可复现刻度，再评判风味与微调。',
      '误解：油脂厚=好喝。纠偏：意式优先酸苦平衡；油脂多为视觉。',
      '误解：必须每把刚好 30s/36g。纠偏：理想值之外有 25–30s / 30–36g 等可接受区间。',
    ],
    cards: [
      {
        tone: 'card-orange',
        title: '目标先于风味：18g / 30s / 36g',
        body: '调磨第一阶段故意不谈好喝，把粉量、时间、液重钉死，让研磨度成为可调的第四变量。没有共同坐标系，就无法判断粗细。',
        quote: '「你不要管好不好喝……这么调完之后，我们再来评判这杯咖啡好不好喝」[00:22–00:29]',
        pitfall: '一上来就凭口感乱拧刻度，无法复盘。',
        action: '换豆或换机时先写死粉/时/液目标，再只动研磨度。',
      },
      {
        tone: 'card-green',
        title: '流速读粗细：慢无油=细，太快=粗',
        body: '35s 几乎不出液、无油脂→太细；43s/38g→仍细；22s/41g→太粗。油脂在「偏粗」时往往更好看，但那是副现象，主判据仍是时间与液重。',
        quote: '「流速又慢又没有油脂……太细了对吧」[01:50–01:58]',
        pitfall: '只看油脂好坏，忽略称重计时。',
        action: '每把记录：刻度、粉重、时间、液重、出脂观感。',
      },
      {
        title: '换算与洗磨：每约 5 秒一格，改刻度必清粉',
        body: '时间差÷约 5 秒≈格数，用于粗调；改刻度后务必洗磨，否则刀盘残留会污染下一把判断。费粉是方法成本，不是失误。',
        quote: '「大概每5秒调粗一个格」[04:25–04:27]',
        pitfall: '调了刻度却不洗磨，新旧粉混磨。',
        action: '改刻度→短时排粉→再正式称 18g。',
      },
      {
        tone: 'card-red',
        title: '理想值难中靶：用区间验收调磨',
        body: '拼配比例与手法无法绝对复现，完美 30/36 是理想值。可接受：粉 18–19g、时 25–30s、液 30–36g。风味上抓酸苦平衡与回甘，别被油脂绑架。',
        quote: '「这个叫做理想值……我们只需要萃到25秒到30秒……约30到36克就可以了」[07:37–08:02]',
        pitfall: '差两秒就全盘否定，或为追油脂把粉磨得过粗失酸苦结构。',
        action: '先进入区间，再微调；品饮问酸苦是否平衡、苦是否来得过猛。',
      },
    ],
    table: {
      title: '片中几把萃取对照（示意）',
      headers: ['阶段', '观察', '判断', '动作'],
      rows: [
        ['盲测第一把', '≈35s 几乎无液、无油脂', '太细', '调粗 1.2→1.8 + 洗磨'],
        ['第二把', '43s / ≈38g', '仍细', '差 13s≈3 格 → 调至约 2'],
        ['第三把', '22s / ≈41g', '太粗', '调细至约 1.9'],
        ['近成功', '≈28s / ≈41g', '接近理想', '落入区间即可验收'],
        ['验收区间', '18–19g / 25–30s / 30–36g', '调磨成功', '再谈风味微调'],
      ],
    },
    boundary: [
      '刻度数字绑定该磨豆机与该豆，不能直接抄到你家机型。',
      '9 bar、E61、250kg 等为口述示意，机型与粉碗直径会变。',
      '教学强调费粉洗磨；家用低频可接受，但成本与豆耗需自担。',
      '风味结论偏门店拼配生意逻辑，不覆盖所有浅烘精品叙事。',
    ],
    pitfalls: [
      '不洗磨就改刻度，残留粉让流速判断失真。',
      '机器不平导致单边出液，误判研磨度。',
      '压粉比力气或追求「标准公斤数」，忽略压平压实。',
      '把理想值当唯一合格线，忽略可接受区间与变量漂移。',
      '只追油脂厚度，忽略酸苦平衡。',
    ],
    conclusion: {
      key: [
        '调磨先坐标系（粉/时/液），后刻度',
        '流速与液重判粗细；改刻度必洗磨',
        '理想值难天天中，区间验收；好喝看酸苦平衡',
      ],
      actions: [
        '写下你的目标参数与可接受区间，贴在磨豆机旁',
        '练固定布粉压粉与放水上粉动作，减少人为噪音',
        '换豆或天气气压大变时重走洗磨→试萃→微调闭环',
      ],
      shift:
        '以前：到处抄「某磨第几格」；现在：先钉死 18g/30s/36g，用流速自己找到区间，再谈这杯酸不酸、苦是否拖泥带水。',
    },
  },
  index: {
    summary:
      '意式调磨：先钉死18g/30s/36g，用流速判粗细并洗磨微调；落入可接受区间后再谈酸苦平衡。约12分半实操。',
    tags: ['意式咖啡', '调磨', '研磨度', '浓缩', '酸苦平衡', '咖啡机'],
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
  screenshot_count: 7,
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
  shots: 7,
  segments: segs.length,
  svg_height: height,
  duration: ITEM.duration,
  primary: ITEM.primary,
};
console.log('OK', ITEM.slug, 'segs', segs.length, 'svg_height', height);
console.log(JSON.stringify(result, null, 2));
