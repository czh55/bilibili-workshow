import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../svg-auto-height.mjs';
import { DATA } from './b49_svg_data.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', 'docs');

const CSS = `*{margin:0;padding:0;box-sizing:border-box}
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
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;

function esc(s) {
  return String(s ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function buildBody(d) {
  const tags = (d.tags || []).map((t, i) => `<span class="tag ${['tag-blue','tag-green','tag-orange','tag-purple','tag-red','tag-gray'][i % 6]}">${esc(t)}</span>`).join('');
  const timeline = (d.timeline || []).map(([t, x]) => `<div class="timeline-item"><span class="timeline-time">${esc(t)}</span><span class="timeline-text">${esc(x)}</span></div>`).join('');
  const mapNodes = (d.map || []).map(([label, x], i) => {
    const cls = ['node', 'node-green', 'node-orange', 'node-blue'][i % 4];
    const arrow = i < (d.map.length - 1) ? '<span class="arrow">→</span>' : '';
    return `<div class="${cls}">${esc(label)}<br>${esc(x)}</div>${arrow}`;
  }).join('');
  const corrections = (d.corrections || []).map((c) => `<p>${esc(c)}</p>`).join('');
  const cards = (d.cards || []).map((c) => `
    <div class="card ${c.tone || ''}">
      <h3>${esc(c.title)}</h3>
      <p>${esc(c.body)}</p>
      ${c.quote ? `<div class="quote">${esc(c.quote)}</div>` : ''}
      ${c.relation ? `<div class="relation">${esc(c.relation)}</div>` : ''}
    </div>`).join('');
  const thead = `<tr>${(d.table.head || []).map((h) => `<th>${esc(h)}</th>`).join('')}</tr>`;
  const tbody = (d.table.rows || []).map((r) => `<tr>${r.map((c) => `<td>${esc(c)}</td>`).join('')}</tr>`).join('');
  const boundary = (d.boundary || []).map((b) => `<li>${esc(b)}</li>`).join('');
  const pitfalls = (d.pitfalls || []).map((p) => `<div class="pitfall">${esc(p)}</div>`).join('');
  const key = (d.conclusion.key || []).map((k) => `<li>${esc(k)}</li>`).join('');
  const actions = (d.conclusion.actions || []).map((a) => `<li>${esc(a)}</li>`).join('');

  return `<div class="container root-wrap">
  <h1>${esc(d.title)}</h1>
  <div class="meta">${tags}<span class="tag tag-gray">时长 ${esc(d.duration)}</span><span class="tag tag-gray">${esc(d.perspective)}</span></div>
  <a class="source-link" href="${esc(d.url)}">原视频</a>
  <div class="summary-line">${esc(d.summary)}</div>

  <div class="timeline"><h3>关键证据时间轴</h3>${timeline}</div>

  <div class="map"><h2>核心脉络</h2><div class="diagram">${mapNodes}</div></div>

  <div class="correction"><h3>常见误解与认知纠偏</h3>${corrections}</div>

  <div class="section"><h2 class="sec-title">观点拆解：在讲什么 → 关键理解 → 怎么用 → 原文依据</h2>${cards}</div>

  <div class="section"><h2 class="sec-title">${esc(d.table.title)}</h2><div class="card"><table><thead>${thead}</thead><tbody>${tbody}</tbody></table></div></div>

  <div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${boundary}</ul>${pitfalls}</div></div>

  <div class="conclusion"><h2>总结与行动</h2><h3>核心要点</h3><ul>${key}</ul><h3>行动清单</h3><ol>${actions}</ol><h3>关键认知转变</h3><p>${esc(d.conclusion.shift)}</p></div>

  <div class="footer">双轨产物之二 · 理性分析 · 证据来自同一 Whisper 转录 · ${esc(d.footer_duration)}</div>
</div>`;
}

const slugs = process.argv.slice(2);
const targets = slugs.length ? slugs : Object.keys(DATA);
for (const slug of targets) {
  if (!DATA[slug]) { console.log(`skip: ${slug} (no data)`); continue; }
  const d = DATA[slug];
  const { svg, height } = await buildSvg({ css: CSS, body: buildBody(d), width: 1320 });
  const out = path.join(OUT, `${slug}-理性分析.svg`);
  fs.writeFileSync(out, svg, 'utf8');
  console.log(`Generated: ${out} height: ${height}`);
}
