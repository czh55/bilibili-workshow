#!/usr/bin/env node
/** B57：homemade-instant-coffee → 图文实录 HTML + 理性分析 SVG + index.json */
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
  slug: 'homemade-instant-coffee',
  title: '如何在家制作速溶咖啡',
  shortTitle: '如何在家制作速溶咖啡',
  svgTitle: '速溶为何不如现磨：干燥、冻干与增香三条工艺链',
  url: 'https://xhslink.cn/o/7HXJxpJzYjB',
  durationSec: 557,
  primary: 'coffee',
  description:
    '同豆对照喷雾干燥、三合一掩盖、冻干浓缩与蒸香回填：高温与升华都会散失香气；速溶输在风味、赢在方便。约9分18秒工艺实验全记录。',
  lead: '凌晨加班想喝拿铁：选豆、磨粉、机萃、兑奶——麻烦但香；撕开速溶三十秒搞定，却少了醇厚与果香。作者用同一批好豆进喷雾干燥机，结果喝到「这辈子最难喝」的粉末，再用 GC-MS 钉死：约 210℃ 热风让酯类、醛类等风味物面目全非。请教业内后走出「三合一」商业路径：罗布斯塔深烘 + 奶粉糖掩盖高温负面，便宜好喝但「气没了」。直接冻干意式浓缩略好仍散失；按外文工艺做「水煮→真空浓缩→压过共晶点砸成大颗粒→再冻干」，外观像工业冻干，香气问题依旧。最后从豆液蒸出香气、冷凝收集后喷回冻干粉，做出「罗氏速溶」——比裸冻干高那么一丢丢。收束：拼配太复杂先不讲；口味远逊现磨，但焦头烂额时那杯方便无法替代。',
  takeaway:
    '高温喷雾毁香 → 奶糖掩盖成三合一；冻干更保香但仍散失 → 工厂式浓缩+大颗粒也不够；保不住就增香回填。速溶输风味、赢方便。',
  structure: [
    ['00:00→00:45', '立题对照', '现磨拿铁全流程 vs 速溶一撕一倒；同豆能否做出一样好喝的速溶？'],
    ['00:45→01:40', '喷雾干燥翻车', '雾化+热风成粉，却无香难喝；210℃ 与 GC-MS 证实风味散失。'],
    ['01:40→02:40', '三合一商业解', '专家：加奶粉糖掩盖；换罗布斯塔深烘，像某四字品牌，气没了。'],
    ['02:40→03:20', '方便平行线', '手冲/挂耳也「方便」，香气与便利是否注定不相交？'],
    ['03:20→04:10', '直接冻干', '阿拉比卡意式浓缩升华干燥：有香又像没香，散失仍不小。'],
    ['04:10→05:50', '工厂工艺复刻', '水煮→旋蒸浓缩→超低温冻硬→砸 5mm→冻干大颗粒；外观像，味道仍旧。'],
    ['05:50→06:40', '成本顿悟', '香气难题以现有家用科技难解；火锅酱料对比「十元香气」。'],
    ['06:40→08:00', '蒸香回填', '油浴蒸气+冷凝/氮气/干冰收集，喷回冻干粉→罗氏速溶略高一点。'],
    ['08:00→09:18', '收束边界', '拼配未讲；口味远逊现磨，但方便仍值得留一杯。'],
  ],
  chapters: [
    {
      range: '00:00 → 00:45',
      title: '三十秒速溶 vs 一整套拿铁',
      paras: [
        '开场把两种提神路径并置：凌晨加班想喝咖啡，现磨路径是选豆、磨粉、机萃、兑奶，才能得到香浓拿铁——麻烦到「喝之前就不困了」；速溶则是一撕一倒一冲，约三十秒。作者承认速溶少了醇厚、果香与油润，但追问：为什么同样方便的粉末，就注定比不过现磨？',
        '先算账：一块约 69 元的豆子可做约 14 杯美式（约 4.9 元/杯），对照一袋约 0.8 元的速溶——豆子本身好得多。假设成立：若用同一批好豆做成速溶，味道是不是就能追平？于是搬来小型喷雾干燥机。',
      ],
      figures: [
        {
          file: 'shot-01.jpg',
          time: '00:30',
          alt: '杯中奶咖与咖啡豆，标题「如何在家里制造速溶咖啡」',
          cap: '立题封面：在家「制造」速溶——不是冲泡评测，而是工艺实验',
        },
      ],
    },
    {
      range: '00:45 → 01:40',
      title: '喷雾干燥：成熟技术，却喝到「亲妈都不认」',
      paras: [
        '工艺动作很清楚：把现做咖啡液在高压下雾化成微滴，再被热风干燥成细粉。作者说这是很成熟的技术，理论应接近现做——结果却是「这辈子最难喝」：几乎没有任何香味。',
        '查文献后指向风味散失：喷雾干燥机热风可高达约 210℃，酯类、醛类等风味物质发生复杂变化。GC-MS（转录作 GC Master）对照显示，高温后图谱「连亲妈都认不出来」。同豆、不同干燥路径，足以把一杯咖啡变成另一种东西。',
      ],
      figures: [],
    },
    {
      range: '01:40 → 02:40',
      title: '专家路线：三合一用奶糖「盖」住高温伤害',
      paras: [
        '作者戴上 Rokid / 乐奇 AI 眼镜导航去请教业内（曾总）。结论很直：纯粉路线很难好喝；可以加入奶粉和糖，大幅压低高温干燥带来的负面口感。豆种与烘焙也要改：把偏香的阿拉比卡换成口味更重的罗布斯塔，中烘换成深烘——直接喝会是浓重焦糊与苦后调；加奶粉加糖冲泡后，却出一种「很像拿铁、也像某四字品牌」的熟悉感。',
        '铝箔条包装后，这就是常见的三合一：便宜、味道过得去；坏处是罗布斯塔本就香气偏少，干制后再「气没了」。商业解法不是保香，而是用甜奶结构掩盖工艺损失。',
      ],
      figures: [
        {
          file: 'shot-02.jpg',
          time: '01:40',
          alt: '戴头盔调整 Rokid 智能眼镜',
          cap: '请教专家路上：乐奇 AI 眼镜导航/FOV 植入——剧情桥，也是设备口播',
        },
      ],
    },
    {
      range: '02:40 → 03:20',
      title: '香气与方便：平行线？先排除「泡粉当手冲」',
      paras: [
        '外行会问：磨完直接泡不就得了？叠滤纸冲掉渣呢？作者用「手冲麻烦得要死」「折简易滤网装粉」把挂耳/办公室冲泡点出来——这些确实更接近现磨风味，但仍要现场萃取，不是「粉末即饮」的速溶定义。问题收束成：香气与方便，是不是注定不能相交的平行线？答案：不一定——既然高温干燥毁香，就换冷冻干燥。',
      ],
      figures: [],
    },
    {
      range: '03:20 → 04:10',
      title: '第一次冻干：意式浓缩直接升华，香气仍暧昧',
      paras: [
        '作者用手磨处理香气宜人的阿拉比卡，萃意式浓缩后直接冷冻、冻干（水分固态升华）。理论上风味散失应小于热风喷雾。48 小时后得到松散冻干粉，外观不像传统大颗粒工业冻干；品饮感受是「有香又像没香、果香又像没多少」——头脑尖尖的暧昧。GC-MS 显示：比高温干燥好得多，但仍有不小散失。怀疑工艺不对，于是去查外文资料（再次用上眼镜实时翻译）。',
      ],
      figures: [
        {
          file: 'shot-03.jpg',
          time: '03:20',
          alt: '手摇磨豆，字幕「我直接用香气宜人的阿拉比卡」',
          cap: '冻干线起点：先用好豆做浓缩，再谈干燥保香',
        },
      ],
    },
    {
      range: '04:10 → 05:50',
      title: '工厂步骤家用复刻：浓缩、共晶点、大颗粒冻干',
      paras: [
        '外文工艺总结为：水煮咖啡 → 浓缩 → 冷冻 → 打碎成大颗粒 → 再冻干。家用执行：粉加水后间接加热、封闭锅口（减少香气逃逸），沸腾约 10 分钟过滤；液约 6°Brix，需真空低温浓缩到约 55°Brix 以上。没有工厂真空浓缩，改用旋转蒸发仪，漫长一夜把稀液收成黏糊「石油状」。',
        '普通冰箱冻不硬：浓缩物在共晶点附近呈沙沙软膏。解决办法是压过共晶点——扔进约 −60℃，数小时后成硬板砖，套袋砸成约 5mm 碎块立刻送冻干。再 48 小时，得到外观接近传统大颗粒的冻干咖啡：融化丝滑如陨石，但喝起来、闻起来仍像「之前那盘冻干」——形貌对了，香气难题没被外形解决。',
      ],
      figures: [
        {
          file: 'shot-04.jpg',
          time: '05:20',
          alt: '硅胶模里沙沙软膏状浓缩物',
          cap: '共晶点现场：浓缩咖啡在普通冷冻下仍是软膏，必须更深低温才能砸块',
        },
      ],
    },
    {
      range: '05:50 → 06:40',
      title: '水中捞月：成本账单与「十元酱料」的香',
      paras: [
        '算账时作者崩溃：同样一百多元预算能吃多少猪脚饭。暂时结论很丧：速溶损失香气，以人类目前科技（至少在家用实验边界内）无法完美解决。出门放松、火锅沾酱——对比「收马支付十元」也能有强烈香气——铺垫下一问：保不住香，能不能增香？',
      ],
      figures: [],
    },
    {
      range: '06:40 → 08:00',
      title: '蒸香回填：从豆里抽出香，再喷回速溶',
      paras: [
        '外加香味剂像作弊；但从咖啡液本身蒸出香气再加回速溶，作者认为不算。流程：油浴加热咖啡液，香气随水蒸气挥发，经长冷凝管收集；为提高收集率加氮气与减压（气压从约 7 MPa 降到 1 MPa 以下——操作翻车「居然爆了」），氮气经气体加热罐到约 40℃，再换更大冷凝管与冰水稳定系统。最终在旁路小管倒入干冰，融化后倒出浓缩香气物，用喷笔边喷边搅拌到冻干粉上，小袋包装——「现代蒸香工艺」的冻干速溶完成。',
        'GC-MS 显示：比未蒸香的冻干速溶「明显高了那么一丢丢」。作者戏称这就是「罗氏速溶」。',
      ],
      figures: [
        {
          file: 'shot-05.jpg',
          time: '07:30',
          alt: '工作室/冷凝管路仰拍，工业风顶棚',
          cap: '增香装置现场：冷凝、管路与工作室感——家用「邪修」收集香气',
        },
      ],
    },
    {
      range: '08:00 → 09:18',
      title: '拼配未讲完：口味输给现磨，方便仍留下',
      paras: [
        '作者坦白：本该很重要的拼配完全没展开，因为太复杂、自己也讲不清，留给以后。从口味与香气讲，速溶远比不上现磨；但它有不可替代的优点——方便，非常方便。即便商业咖啡已经普及，工作焦头烂额时仍会来上一杯。感谢观看，下期再见。',
      ],
      figures: [
        {
          file: 'shot-06.jpg',
          time: '08:40',
          alt: '作者与桌上多种速溶形态：小杯、条装、冻干粒与冰咖',
          cap: '收束台面：速溶有很多形态；核心取舍仍是风味 vs 即饮便利',
        },
      ],
    },
  ],
  svg: {
    tags: ['咖啡', '速溶', '喷雾干燥', '冻干', '蒸香', '三合一'],
    summary:
      '同豆实验证明：喷雾高温毁香、冻干仍散失、工厂大颗粒也救不回全部风味；三合一靠奶糖掩盖，蒸香回填只能「高一丢丢」。速溶输香气、赢方便。',
    timeline: [
      ['00:00', '现磨拿铁全流程 vs 速溶 30 秒'],
      ['00:31', '同豆假说：好豆做成速溶能否追平'],
      ['00:48', '喷雾干燥成粉 → 无香难喝'],
      ['01:20', '210℃ + GC-MS：风味面目全非'],
      ['01:50', '专家：奶粉糖掩盖；罗布斯塔深烘三合一'],
      ['03:16', '香气∥方便？切入冻干'],
      ['03:20', '阿拉比卡浓缩直接冻干，香气暧昧'],
      ['04:25', '水煮→旋蒸浓缩→过共晶点→砸块冻干'],
      ['05:50', '形貌像工业品，香气问题未解'],
      ['06:30', '暂判：保香难；对比火锅酱料之香'],
      ['06:40', '从豆蒸香回填 → 罗氏速溶略高'],
      ['08:30', '拼配未讲；方便仍值得留'],
    ],
    map: ['喷雾高温毁香', '三合一奶糖掩盖', '冻干仍散失', '蒸香回填补一丢丢'],
    corrections: [
      'ASR：喷雾干澡/干脏→喷雾干燥；纸类纯类→酯类醛类等；GC Master/GCMASK→GC-MS。',
      'ASR：易式→意式；深化→升华；风油→风味；共精点→共晶点；旋转蒸发液→旋转蒸发仪；6brex→6°Brix。',
      'ASR：树蓉→速溶；冷冰管→冷凝管；香气几斤→香气宜人；挂着→挂耳；香蕉的平行线→相交的平行线。',
      '误解：同豆做成速溶=同味道。纠偏：干燥路径会摧毁或散失大量挥发物。',
      '误解：冻干外观像工业品就等于香气到位。纠偏：形貌与香气是两件事。',
      '误解：速溶只有「难喝」一种结局。纠偏：三合一用结构掩盖；蒸香可小幅回补，但边界是方便品不是精品替代。',
    ],
    cards: [
      {
        tone: 'card-orange',
        title: '喷雾干燥：效率高，香气先死',
        body: '雾化+热风是成熟制粉技术，但约 210℃ 量级热风让挥发风味剧烈变化；同豆对照足够说明「工艺 > 豆子叙事」。',
        quote: '「喷雾干燥机高到210度的热风……高温让它变得连它亲妈都认不出来」[01:20–01:32]',
        pitfall: '用「豆子很贵」说服自己忽略干燥温度。',
        action: '看速溶配料与工艺宣传时，先问干燥方式，再问豆种故事。',
      },
      {
        tone: 'card-green',
        title: '三合一：商业解是掩盖，不是保香',
        body: '专家路径承认纯粉难喝，用奶粉糖降负面；罗布斯塔深烘提供浓重基底，冲出来像熟悉的四字品牌拿铁感——代价是香气几乎清零。',
        quote: '「加入奶粉和糖……气没了」[01:59–02:40]',
        pitfall: '把「好喝的三合一」误读成「保留了咖啡香气」。',
        action: '品三合一时分开评：甜奶结构 vs 咖啡本香，各打一维分数。',
      },
      {
        title: '冻干：更好，但仍不是零散失',
        body: '升华路径理论上更温和；直接冻浓缩、以及「浓缩→过共晶点→大颗粒」工厂复刻，都能改善或对齐外观，GC-MS 与口感仍显示明显散失。',
        quote: '「虽然比高温干燥好得多，但确实还有不小的散失率」[04:00–04:04]',
        pitfall: '看见大颗粒冻干就默认等于精品风味。',
        action: '对比「新鲜浓缩 / 冻干粉复溶」盲品，记录果香与余韵差。',
      },
      {
        tone: 'card-red',
        title: '保不住就增香：蒸香回填的上限',
        body: '从咖啡液蒸出香气再喷回冻干粉，GC-MS 只「高那么一丢丢」——诚实的上限声明。拼配更复杂，作者主动标为未覆盖。',
        quote: '「比直接冻干没做蒸香的速溶咖啡，明显的高了那么一丢丢」[07:54–08:00]',
        pitfall: '把家用蒸香实验当成可复现的工业品质保证。',
        action: '接受速溶品类目标：便利优先；要香气就回到现磨或挂耳现场萃。',
      },
    ],
    table: {
      title: '三条工艺链对照（视频内）',
      headers: ['路径', '核心动作', '结果一句话'],
      rows: [
        ['喷雾干燥', '雾化 + 高温热风', '成熟、快，香气几乎毁掉'],
        ['三合一', '罗豆深烘 + 奶粉糖', '便宜好喝，气没了'],
        ['冻干（直接/工厂式）', '升华；浓缩+大颗粒', '好于热风，仍显著散失'],
        ['蒸香回填', '冷凝收集香气喷回', '比裸冻干高一丢丢'],
      ],
    },
    boundary: [
      '这是创作者家用/小厨店设备实验，不是食品安全或工业参数手册。',
      '压力、温度、Brix、共晶点等口述为示意，机型与配方会偏移。',
      '未展开拼配；结论不覆盖「所有速溶品牌」的感官排序。',
      '设备口播（AI 眼镜）是叙事与赞助桥段，不改变工艺因果。',
    ],
    pitfalls: [
      '把「同豆」当成味道守恒——忽略干燥与浓缩过程的挥发损失。',
      '普通冷冻浓缩物不硬就硬砸——未过共晶点会得到软膏而非可冻干砖块。',
      '减压/氮气操作不当会炸管——视频已演示翻车。',
      '用外加香精自我安慰「恢复风味」——与片中「从豆提取再回填」不是同一伦理与风味逻辑。',
    ],
    conclusion: {
      key: [
        '干燥路径决定速溶上限，豆子叙事救不了高温喷雾',
        '三合一是掩盖策略；冻干更保香仍有散失',
        '蒸香回填只能小幅补偿；品类价值在方便不在追平现磨',
      ],
      actions: [
        '选速溶：分清喷雾粉 / 冻干粒 / 三合一，预期绑在「方便」而非「果香层次」',
        '要香气：优先现磨、挂耳或现场萃取，而不是加长速溶冲泡仪式',
        '看工艺视频：用 GC-MS/盲品思维问「损失了什么」，少被外形骗',
      ],
      shift:
        '以前：觉得速溶难吃是豆子差；现在：同豆也挡不住干燥与浓缩的香气税——方便是买到的功能，香气是缴掉的税。',
    },
  },
  index: {
    summary:
      '同豆做喷雾、三合一、冻干与蒸香回填：高温与升华都散失香气；速溶输风味、赢方便。约9分工艺实验全记录。',
    tags: ['速溶咖啡', '喷雾干燥', '冻干', '三合一', '咖啡工艺', '风味散失'],
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
