#!/usr/bin/env node
/** B57：homemade-americano-guide → 图文实录 HTML + 理性分析 SVG + index.json */
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
  slug: 'homemade-americano-guide',
  title: '如何制作一杯好喝的美式咖啡？',
  shortTitle: '如何制作一杯好喝的美式咖啡',
  svgTitle: '理想美式方法论：基底→稀释→水温→冰美式模板',
  url: 'https://xhslink.cn/o/6EwQTplFPYE',
  durationSec: 788,
  primary: 'coffee',
  description:
    '乔治队长咖啡教室第二课：美式不是「浓缩加水」这么简单。从滤网脂肪与风味持久、萃取率/浓度，到粉液比与萃取时间、1:5–1:7稀释盲品、先水后浓缩、高水温混合，再到冰美式动态浓度公式。约13分8秒理想美式方法论全记录。',
  lead: '美式听起来只是浓缩加水，却牵涉加水量、浓缩与水的比例、水温、浓缩的萃取率与浓度、以及你开始喝时的杯温。作者先用 Crema 与激光笔对照美式与手冲：金属滤网让更多脂肪通过，口感更圆润、风味更耐放。再钉死两个基底概念——萃取率管平衡，浓度管感官强度——并按烘焙深度给出粉液比与 25–32 秒萃取时间窗口。随后用同一 36g 浓缩做 1:5 / 1:6 / 1:7 稀释对比，给出浅/中/深烘的个人稀释建议；实测多数豆子「先水后浓缩」更饱满；较高水温混合后冷却对比，高水温一侧更扎实。收束到冰美式：它是快饮、动态稀释饮料，提供浅烘与深烘两套冰+水模板，目标是 25–30 分钟内浓度仍约 ≥1.2%。',
  takeaway:
    '先做出好喝浓缩（烘焙对应粉液比 + 时间判磨）→ 再按口味选稀释比 → 先水后浓缩 + 偏高水温 → 冰美式用「冰+水」模板扛动态融化。',
  structure: [
    ['00:00→00:49', '立题：宝藏日常饮', '美式表面简单，实际覆盖比例、水温、萃取与饮用时机；作者视为宝藏咖啡。'],
    ['00:49→02:33', '辨认实验', 'Crema 易被骗；激光穿透手冲却难穿透美式——金属滤网保留更多脂肪，口感与风味持久度更强。'],
    ['02:33→04:09', '萃取率与浓度', '萃取率决定平衡（酸/糖/大分子）；浓度决定感官强度；无绝对参数，按豆子找方案。'],
    ['04:09→05:24', '浓缩粉液比', '深烘约1:1.8–1.9、中深约1:1.9–2.0、浅烘约1:2.0–2.2；越深越不宜拉大粉液比。'],
    ['05:24→06:15', '研磨与时间', '高压体系下研磨主要决定萃取时间；家用/店用建议约25–32秒落入酸甜平衡区。'],
    ['06:15→08:06', '稀释盲品', '同36g浓缩做1:5/1:6/1:7；浅烘偏浓稀释、深烘可更稀；最终以个人偏好为准。'],
    ['08:06→08:47', '加料顺序', '大量测试：多数豆子先水后浓缩，醇厚度与风味饱满度更高（机制未完全解释）。'],
    ['08:47→10:53', '水温钥匙', '不同加水温度冷却到同温后仍可差很多；倾向较高水温混合；同时提醒勿过烫伤食道。'],
    ['10:53→12:53', '冰美式公式', '冰美式是动态浓度饮料；浅烘120冰+120水、深烘120冰+140水再加浓缩，保25–30分钟浓度约≥1.2%。'],
    ['12:53→13:08', '收束', '概括性方法论：搭好框架，在家复现理想美式。'],
  ],
  chapters: [
    {
      range: '00:00 → 00:49',
      title: '第二课开场：一杯日常，却是多变量系统',
      paras: [
        '彭志阳（乔治队长）开场：咖啡教室第二课主题是「如何制作一杯好喝的美式」。它听起来像浓缩加水，却牵涉加多少水、浓缩与水的比例、水温几度、基底浓缩的萃取率与浓度，以及你大概到多少杯温才开始喝——每个因素都在改体验。',
        '作者坦言美式不起眼、非常日常，却是他的宝藏咖啡、最爱之一。立题完成：不是教你「倒水」，而是把理想美式拆成可调的方法论框架。',
      ],
      figures: [
        {
          file: 'shot-01.jpg',
          time: '00:38',
          alt: '乔治队长坐在咖啡教室台前开场讲解',
          cap: '立题现场：日常美式被重新定义为多变量系统，而不只是「浓缩加水」',
        },
      ],
    },
    {
      range: '00:49 → 02:33',
      title: '哪杯是美式：Crema 会被骗，激光不会',
      paras: [
        '趣味实验：两杯咖啡，多数人会凭表面 Crema 指认美式。作者用勺子抹掉 Crema 后，肉眼几乎难辨美式与手冲。真正的判别来自激光电筒：手冲液体能轻易被穿透，美式则难以穿透。',
        '原因指向滤材：浓缩机的金属滤网（滤杯/滤材系统）允许部分脂肪通过，而纸滤手冲会挡下更多油脂。结果是美式口腔触觉更圆润顺滑，风味持久度也略高——外卖手冲放二十分钟可能已明显走味，美式放四十分钟、五十分钟仍能保住一些风味。这段把「美式是什么」从外观叙事拉回物理与感官。',
      ],
      figures: [
        {
          file: 'shot-02.jpg',
          time: '02:00',
          alt: '两杯分享壶并置，讲解金属滤网与脂肪通过',
          cap: '对照实验现场：脂肪通过金属过滤系统——美式更圆润、更耐放的物理线索',
        },
      ],
    },
    {
      range: '02:33 → 04:09',
      title: '先钉死两个词：萃取率管平衡，浓度管强度',
      paras: [
        '进入美式细节前，先补两个会直接影响 Espresso（浓缩基底）质量的概念。萃取率：所用咖啡豆中有百分之多少可溶物质进入杯中——你在控制平衡感，决定有机酸、糖类与更大分子物质的比例，也就决定基底「喝起来像什么」。',
        '浓度更直观：已萃出的可溶物占整杯液体的百分比（例如 1% 浓度即液体里约有 1% 来自咖啡可溶物）。浓度决定酸、风味、香气、甜、苦等各项感官的强度。没有绝对正确值：烘焙度、风土、品种带来的酸甜比例不同，必须具体问题具体分析，按豆子找最合适方案。好喝美式离不开好喝浓缩原液——原液对了，稀释才有机会对。',
      ],
      figures: [
        {
          file: 'shot-03.jpg',
          time: '03:58',
          alt: '讲解不同豆子酸甜比例不同，需具体分析',
          cap: '概念桥段：酸与甜的比例因豆而异——拒绝「一套参数打天下」',
        },
      ],
    },
    {
      range: '04:09 → 05:24',
      title: '家用速调公式：烘焙越深，粉液比越收',
      paras: [
        '作者给出便于在家快速调整的粉液比参考：深烘约 1:1.8–1:1.9；中深烘约 1:1.9–1:2.0；浅烘约 1:2.0–1:2.2。有趣现象：烘焙越深，建议粉液比反而越小——因为深烘更容易萃取，粉液比拉太大容易把苦味与粗糙口感一起带出来。',
        '强调这不是绝对值：烘焙机、膨胀率、处理法都会偏移，公式只给方向。有了粉液比，下一环是研磨度。',
      ],
      figures: [],
    },
    {
      range: '05:24 → 06:15',
      title: '研磨度：高压体系里，用时间当仪表盘',
      paras: [
        '在浓缩的高温高压系统中，研磨度大部分决定萃取时间。靠肉眼或抹粉很难找到合适研磨——建议用萃取时间判断研磨是否合适。家用或咖啡店场景，作者建议把萃取时间控制在约 25–32 秒：这个窗口更容易得到酸甜平衡、负面较少的浓缩。',
        '至此，理想美式的「基底层」搭好：按烘焙选粉液比，用时间校准研磨，先保证原液好喝。',
      ],
      figures: [],
    },
    {
      range: '06:15 → 08:06',
      title: '稀释对照：1:5 浓郁带苦，1:7 空淡，中间找心仪点',
      paras: [
        '三杯同起点：都是 36g 浓缩，分别按浓缩:水 = 1:5、1:6、1:7 加水。1:5 味道浓郁，前段香甜与焦糖化调性很靠前，但尾韵苦味偏强偏长；1:6 酸甜略弱，尾韵苦不再那么突兀；1:7 则显空、强度不够，焦糖甜香气与酸质都模糊，像一杯淡淡的咖啡。',
        '设计原则：萃取完成后用不同比例找自己最喜欢的点。若要建议——浅烘作者习惯约 1:5–1:5.5，中烘约 1:5.5–1:6，深烘约 1:6–1:7；但仍完全可以按个人喜好设定。',
      ],
      figures: [
        {
          file: 'shot-04.jpg',
          time: '06:40',
          alt: '三杯美式标注 1:5、1:6、1:7 浓缩与水比例对照',
          cap: '稀释盲品台：同一浓缩基底，比例一变，浓郁、平衡与空淡立刻分层',
        },
      ],
    },
    {
      range: '08:06 → 08:47',
      title: '先水还是先浓缩：多数豆子，先水更饱满',
      paras: [
        '网络常争：先在杯里加水再注入浓缩，还是先挤浓缩再加水？作者基于大量测试与日常工作观察：无论深烘还是浅烘，多数豆子都是先水后浓缩时，醇厚度、风味持久度与饱满度明显更高。具体机制作者也不完全清楚——「离谱又现实」——但作为可执行规则足够清晰。',
      ],
      figures: [],
    },
    {
      range: '08:47 → 10:53',
      title: '水温是钥匙：高温混合更扎实，但别烫着喝',
      paras: [
        '另一发现：杯中加入不同温度的水，再冷却到相同饮用温度，喝起来仍可天壤之别。较高水温有机会让浓缩液里更多物质更充分溶解，风味更多、扎实度与醇厚度更好一点；作者坦承没有仪器论证微观变化，但按日常经验建议用相对较高水温与浓缩混合。',
        '现场对比：约 85℃ 热水一侧（中深烘黑猫拼配）呈现扎实甜感、圆润口感与较长余韵，仍带一点果酸；低温稀释一侧入口强烈但余韵短。健康提醒：不要迷信「咖啡要趁热喝」——食道是「一块生肉」，过烫对食道健康并不友好。热美式方法论到此收束，下一问是冰美式。',
      ],
      figures: [
        {
          file: 'shot-05.jpg',
          time: '09:20',
          alt: '鹅颈壶注水，杯口温度计显示水温读数',
          cap: '水温实验：加水温度不同、冷却到同温后仍可差很多——混合温度是被低估的变量',
        },
      ],
    },
    {
      range: '10:53 → 12:53',
      title: '冰美式：快饮 + 动态浓度，用冰水模板扛融化',
      paras: [
        '冰美式比热美式更复杂：冰块量、水量、浓缩与融化中冰块的叠加，会让浓度持续变化。作者把热美式看作长饮、冰美式看作快饮——冰块融化速度、形状、室内外/打包/车内等环境温度都会改浓度。',
        '两套基础模板：浅烘可用 120g 冰块 + 120g 水再加浓缩；深烘建议 120g 冰块 + 140g 水再加浓缩并搅拌均匀。此时浓度可能约 1.45% 左右——听起来偏浓，正因为冰美式是动态饮料，折中方案要确保约 25–30 分钟内仍能维持约 1.2% 以上浓度。这是片中「非常好用」的公式收束。',
      ],
      figures: [
        {
          file: 'shot-06.jpg',
          time: '11:40',
          alt: '透明杯中的冰美式，讲解冰块融化速度影响浓度',
          cap: '冰美式现场：融化速度、环境温度让浓度一直在变——所以要预留「偏浓一点」的起点',
        },
      ],
    },
    {
      range: '12:53 → 13:08',
      title: '收束：把框架带走，在家复现理想美式',
      paras: [
        '今天用概括性、总结性的方式给出可带走的方法论，分享作者心中理想的美式咖啡。期待你在家也能做出一杯好喝的美式——先搭框架，再按豆子微调。',
      ],
      figures: [],
    },
  ],
  svg: {
    tags: ['美式咖啡', '浓缩', '稀释比', '水温', '冰美式', '萃取'],
    summary:
      '理想美式=好喝浓缩基底×合适稀释×先水后浓缩×偏高水温；冰美式再用冰+水模板对抗动态融化，保一段时间内浓度不垮。',
    timeline: [
      ['00:00', '立题：美式多变量，宝藏日常饮'],
      ['00:49', 'Crema 可骗眼；激光辨美式 vs 手冲'],
      ['01:48', '金属滤网保留脂肪 → 更圆润、更耐放'],
      ['02:33', '萃取率=平衡；浓度=强度'],
      ['04:09', '按烘焙给粉液比：越深越收'],
      ['05:24', '研磨用时间判：约25–32秒'],
      ['06:15', '36g浓缩 × 1:5/1:6/1:7 稀释盲品'],
      ['07:44', '浅/中/深烘个人稀释建议区间'],
      ['08:06', '多数豆子：先水后浓缩更饱满'],
      ['08:47', '水温钥匙：高温混合后冷却仍更扎实'],
      ['10:37', '健康边界：别过烫喝'],
      ['10:53', '冰美式=快饮+动态浓度'],
      ['11:56', '浅烘120冰+120水；深烘120冰+140水'],
      ['12:47', '目标：25–30分钟内浓度约≥1.2%'],
    ],
    map: ['好喝浓缩基底', '选稀释比', '先水后浓缩', '偏高水温', '冰美式模板'],
    corrections: [
      'ASR：carima→Crema；绿杯/绿彩→滤杯/滤材（金属滤网）；美食→美式。',
      'ASR：深红/浅红/中风→深烘/浅烘/中烘；终身烘→中深烘；语韵/鱼韵→余韵。',
      'ASR：抹敷→模糊；扭扣→纽扣；应用跟体验→饮用与体验（语境）。',
      '误解：美式=随便加水。纠偏：比例、水温、加料顺序与基底萃取共同决定体验。',
      '误解：靠 Crema 辨美式。纠偏：抹掉 Crema 后肉眼难辨；脂肪/浊度差异更本质。',
      '误解：冰美式可以套用热美式静态比例。纠偏：冰块融化使浓度持续下降，起点要预留余量。',
    ],
    cards: [
      {
        tone: 'card-orange',
        title: '金属滤网：脂肪留下的口感税与红利',
        body: '美式与纸滤手冲的关键差异之一是过滤介质。金属滤网放过更多脂肪，带来更圆润的口感与更长的风味保持——也解释了为何「看起来像」不等于「喝起来像」。',
        quote: '「它可以允许部分的脂肪通过我们的过滤系统……口腔触觉更加的圆润顺滑」[01:57–02:10]',
        pitfall: '用表面 Crema 当唯一判别标准。',
        action: '对比同豆美式与手冲时，除风味外记录「放置 20/40 分钟后」的衰减差。',
      },
      {
        title: '萃取率与浓度：先分清再调参',
        body: '萃取率管物质组成与平衡；浓度管强度。美式好喝的前提是浓缩原液在这两维上对豆子合适——再谈加水。',
        quote: '「控制好一杯咖啡的萃取率……是在控制一个咖啡的平衡感」「浓度……决定的是咖啡各项感官的一个强度」[02:56–03:36]',
        pitfall: '只改水量却不先问原液是否过萃/欠萃。',
        action: '调美式前先固定粉液比与时间窗口，再单独扫稀释比。',
      },
      {
        tone: 'card-green',
        title: '粉液比随烘焙收放 + 时间判磨',
        body: '深烘更易萃，粉液比宜收；浅烘可略放。研磨在高压体系里主要映射为时间——约 25–32 秒是作者给的家用/店用可执行窗口。',
        quote: '「随着我们的烘焙度的变深……粉液比反而会变小」「萃取时间控制在25秒到32秒左右」[04:47–06:07]',
        pitfall: '深烘仍强行拉大粉液比，把苦与粗糙一起萃出。',
        action: '换豆时先按烘焙深度选粉液比区间，再用秒表校准研磨。',
      },
      {
        tone: 'card-orange',
        title: '稀释比是偏好旋钮，不是道德审判',
        body: '同浓缩下 1:5 浓郁易显苦、1:7 易空淡；浅烘作者偏浓稀释、深烘可更稀。建议是起点，心仪点靠自己喝出来。',
        quote: '「浅烘……1比5到1比5.5……深烘……1比6到1比7」[07:44–07:58]',
        pitfall: '把网红固定比例当成唯一正确答案。',
        action: '一次做三杯 1:5/1:6/1:7，只改水，盲记偏好。',
      },
      {
        title: '顺序与水温：两个被低估的杠杆',
        body: '实测多数豆子先水后浓缩更饱满；较高水温混合再冷却到同温，仍可能更扎实。机制未完全仪器化，但可复现。',
        quote: '「先把水放在杯子里面然后再加入浓缩……都会明显的高于先加浓缩再加水」[08:28–08:41]',
        pitfall: '加水温度很低却指望冷却后仍有同样醇厚。',
        action: '固定比例做「先水/先浓缩」与「高/低水温」各一对，冷却到同温再比。',
      },
      {
        tone: 'card-red',
        title: '冰美式：动态系统，用模板预留浓度',
        body: '冰块融化让浓度持续变。浅烘 120冰+120水、深烘 120冰+140水再加浓缩，是为了在约半小时内仍维持可用浓度（约 ≥1.2%），而不是追求倒出来瞬间的「标准热美式口感」。',
        quote: '「至少可以确保你的咖啡在25到30分钟以内……维持在一个1.2以上左右浓度」[12:42–12:50]',
        pitfall: '冰美式按热美式静态比例直接套，越喝越稀。',
        action: '出门带走时按模板偏浓起杯，并记录你真实饮用时长对应的口感拐点。',
      },
    ],
    table: {
      title: '理想美式参数速查（视频内建议）',
      headers: ['环节', '浅烘倾向', '深烘倾向', '备注'],
      rows: [
        ['浓缩粉液比', '约 1:2.0–2.2', '约 1:1.8–1.9', '中深约 1:1.9–2.0；非绝对值'],
        ['萃取时间', '约 25–32 秒', '约 25–32 秒', '用时间判研磨是否合适'],
        ['稀释（浓缩:水）', '约 1:5–5.5', '约 1:6–7', '中烘约 1:5.5–6；按偏好调'],
        ['加料顺序', '先水后浓缩', '先水后浓缩', '多数豆子更饱满'],
        ['混合水温', '相对较高', '相对较高', '冷却到同温后再评；勿过烫饮用'],
        ['冰美式模板', '120冰+120水+浓缩', '120冰+140水+浓缩', '目标约半小时内浓度仍可用'],
      ],
    },
    boundary: [
      '个人工作室/咖啡教室经验总结，不是实验室标定的唯一真值。',
      '粉液比、稀释比、冰水克数为起点区间，机型、水质、豆子新鲜度会偏移。',
      '「先水后浓缩更饱满」「高水温更扎实」以作者测试与体感为主，未提供仪器级机制证明。',
      '冰美式浓度百分比为口述示意，需结合你自己的称重与折射计习惯校准。',
      '健康提醒仅作常识提示，不构成医疗建议。',
    ],
    pitfalls: [
      '基底浓缩已经过萃/欠萃，却只在美式水量上死磕。',
      '深烘仍用过大粉液比，把苦与粗糙一并放大。',
      '冰美式忽略融化动态，倒杯瞬间好喝、十分钟后稀掉却怪豆子。',
      '迷信必须趁热灌下——烫伤风险与风味评价应分开处理。',
      '把 Crema 厚薄当成质量总分，忽略脂肪与稀释后的真实平衡。',
    ],
    conclusion: {
      key: [
        '美式是系统工程：基底萃取 × 稀释 × 顺序 × 水温（× 冰块动态）',
        '先用烘焙对应粉液比 + 时间窗口做出好喝浓缩，再谈加水',
        '冰美式要用模板预留浓度，而不是套热美式静态比例',
      ],
      actions: [
        '换豆：按深/中/浅选粉液比，把萃取钉在约 25–32 秒',
        '热美式：固定浓缩克数扫 1:5–1:7，默认先水后浓缩 + 偏高水温',
        '冰美式：按浅/深烘套 120冰+(120或140)水模板，按饮用时长微调',
      ],
      shift:
        '以前：美式=浓缩随便兑热水；现在：先把浓缩做成对的基底，再把稀释、顺序、水温（和冰块）当成可调旋钮——框架比运气稳。',
    },
  },
  index: {
    summary:
      '理想美式：先做好浓缩基底，再调稀释、先水后浓缩与水温；冰美式用冰水模板扛动态浓度。约13分方法论。',
    tags: ['美式咖啡', '浓缩咖啡', '稀释比例', '水温', '冰美式', '萃取率'],
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
  screenshot_count: 6,
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
  shots: 6,
  segments: segs.length,
  svg_height: height,
  duration: ITEM.duration,
  primary: ITEM.primary,
};
console.log('OK', ITEM.slug, 'segs', segs.length, 'svg_height', height);
console.log(JSON.stringify(result, null, 2));
