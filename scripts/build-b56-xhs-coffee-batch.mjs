#!/usr/bin/env node
/** B56：3 条小红书咖啡科普 → 图文实录 HTML + 理性分析 SVG + index.json */
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

function fixAsr(text) {
  return String(text)
    .replaceAll('纯厚度', '醇厚度')
    .replaceAll('红都拉斯', '洪都拉斯')
    .replaceAll('意识拼配', '意式拼配')
    .replaceAll('不耐并宠害', '不耐病虫害')
    .replaceAll('抗荡', '抗造')
    .replaceAll('比较嚼劲', '比较娇贵')
    .replaceAll('咖啡的含量', '咖啡因含量')
    .replaceAll('再说养殖', '再说种植')
    .replaceAll('海拔 维度', '海拔 纬度')
    .replaceAll('拼配不非', '拼配无非')
    .replaceAll('一倍带拐弯', '一倍多')
    .trim();
}

const HTML_CSS = `*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}
.container{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}header{margin-bottom:40px}
header h1{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}
.meta-row{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.meta-tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}
.tag-platform{background:#ff2442;color:#fff}.tag-duration{background:#f1f5f9;color:#64748b}.tag-topic{background:#dbeafe;color:#1e40af}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none}.source-link:hover{text-decoration:underline}
.toc{background:#fff;border-radius:16px;padding:20px 24px;margin-bottom:32px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.toc h3{font-size:16px;color:#1e40af;margin:0 0 12px}.toc a{display:block;color:#475569;font-size:14px;text-decoration:none;padding:4px 0;border-bottom:1px solid #f1f5f9}.toc a:hover{color:#3b82f6}
.documentary{font-size:17px}.story-section{margin:48px 0}
.story-section h2{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.story-section p{margin:0 0 14px;color:#44403c}
.time-marker{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}
img{display:block;max-width:100%;height:auto}figure{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}
figcaption{padding:14px 18px;color:#57534e;font-size:14px;line-height:1.7}
.transcript-section{margin-top:48px}
.transcript-note{font-size:14px;color:#78716c;margin-bottom:24px}.transcript-list{list-style:none;padding:0}
.transcript-row{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}
.transcript-row time{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}.transcript-row p{margin:0}
@media(max-width:640px){.container{padding:28px 18px 56px}header h1{font-size:24px}.transcript-row{grid-template-columns:56px 1fr;gap:10px}}
.transcript-collapsible{border:none;margin:0;padding:0}.transcript-collapsible summary{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{display:none}
.transcript-collapsible summary::before{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}
.transcript-collapsible[open] summary::before{transform:rotate(90deg)}.transcript-collapsible[open] summary{margin-bottom:16px}.transcript-collapsible .transcript-body{margin-top:0}
.summary-row{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}
.summary-row .time-marker{flex-shrink:0;margin-top:2px}
.summary-row strong{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}
.summary-row p{color:#57534e;margin:0;font-size:15px}
.takeaway-box{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}
.takeaway-box strong{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}
.takeaway-box p{color:#3b82f6;margin:0;font-size:15px}
.content-points h2{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.content-points h3{font-size:20px;font-weight:700;color:#1c1917;margin:22px 0 14px}`;

const SVG_CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#0f766e,#14b8a6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#0f766e;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul,ol{padding-left:24px;margin:8px 0}
li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #14b8a6;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline h3{color:#0f766e;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#0d9488;min-width:100px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#f0fdfa,#ccfbf1);border:2px solid #5eead4;border-radius:16px;padding:20px 28px;text-align:center;min-width:140px;font-weight:700;font-size:16px;color:#0f766e}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3,.correction p{color:#92400e}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#0f766e;margin-bottom:16px;padding-left:16px;border-left:4px solid #14b8a6}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #14b8a6}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#0f766e;margin-bottom:12px}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#166534}
.conclusion{background:linear-gradient(135deg,#0f766e,#14b8a6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#0d9488;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;

function buildSvgBody(d) {
  const tags = (d.tags || [])
    .map((t, i) => `<span class="tag ${['tag-blue', 'tag-green', 'tag-orange', 'tag-purple', 'tag-red'][i % 5]}">${esc(t)}</span>`)
    .join('');
  const timeline = (d.timeline || [])
    .map(([t, x]) => `<div class="timeline-item"><span class="timeline-time">${esc(t)}</span><span class="timeline-text">${esc(x)}</span></div>`)
    .join('');
  const mapNodes = (d.map || [])
    .map(([label], i) => {
      const cls = ['node', 'node-green', 'node-orange', 'node'][i % 4];
      const arrow = i < d.map.length - 1 ? '<span class="arrow">→</span>' : '';
      return `<div class="${cls}">${esc(label)}</div>${arrow}`;
    })
    .join('');
  const corrections = (d.corrections || []).map((c) => `<p>· ${esc(c)}</p>`).join('');
  const cards = (d.cards || [])
    .map((c) => {
      const tone = c.tone ? ` card ${c.tone}` : ' card';
      return `<div class="${tone.trim()}"><h3>${esc(c.title)}</h3><p>${esc(c.body)}</p><div class="quote">${esc(c.quote)}</div><div class="relation">${esc(c.relation)}</div></div>`;
    })
    .join('');
  const boundary = (d.boundary || []).map((b) => `<li>${esc(b)}</li>`).join('');
  const pitfalls = (d.pitfalls || []).map((p) => `<li>${esc(p)}</li>`).join('');
  const keyHtml = (d.conclusion?.key || []).map((k) => `<li>${esc(k)}</li>`).join('');
  const actionsHtml = (d.conclusion?.actions || []).map((a) => `<li>${esc(a)}</li>`).join('');
  const shift = d.conclusion?.shift || '';

  return `<div class="container root-wrap">
  <h1>${esc(d.title)}</h1>
  <div class="meta">${tags}<span class="tag tag-gray">${esc(d.duration)}</span><span class="tag tag-gray">${esc(d.perspective)}</span></div>
  <a class="source-link" href="${esc(d.url)}">${esc(d.url)}</a>
  <div class="summary-line">${esc(d.summary)}</div>
  <div class="timeline"><h3>结构时间轴</h3>${timeline}</div>
  <div class="map"><h2>核心脉络</h2><div class="diagram">${mapNodes}</div></div>
  <div class="correction"><h3>常见误解与认知纠偏</h3>${corrections}</div>
  <div class="section"><h2 class="sec-title">观点拆解</h2>${cards}</div>
  <div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${boundary}</ul><h3>避坑</h3><ul>${pitfalls}</ul></div></div>
  <div class="conclusion"><h2>总结与行动</h2><h3>核心要点</h3><ul>${keyHtml}</ul><h3>行动清单</h3><ol>${actionsHtml}</ol><h3>关键认知转变</h3><p>${esc(shift)}</p></div>
  <div class="footer">双轨产物之二 · 理性分析 · 证据来自 Whisper 转录与视频截图</div>
</div>`;
}

function buildHtml(item, segs) {
  const toc = item.chapters
    .map((c, i) => `<a href="#ch${i + 1}">${esc(c.nav)}</a>`)
    .join('');
  const summaryRows = item.structure
    .map(
      ([range, title, body]) =>
        `<div class="summary-row"><span class="time-marker">[${esc(range)}]</span><div><strong>${esc(title)}</strong><p>${esc(body)}</p></div></div>`,
    )
    .join('\n');
  const chapters = item.chapters
    .map((c, i) => {
      const figs = (c.figures || [])
        .map(
          (f) =>
            `<figure><img src="assets/${item.slug}/${f.file}" alt="${esc(f.alt)}" loading="lazy"><figcaption>[${esc(f.time)}] ${esc(f.cap)}</figcaption></figure>`,
        )
        .join('');
      const paras = (c.paras || []).map((p) => `<p>${esc(p)}</p>`).join('');
      return `<section class="story-section" id="ch${i + 1}"><h2><span class="time-marker">${esc(c.range)}</span>${esc(c.title)}</h2>${paras}${figs}</section>`;
    })
    .join('\n');
  const transcript = segs
    .map((s) => `<div class="transcript-row"><time>${fmtTime(s.start)}</time><p>${esc(fixAsr(s.text))}</p></div>`)
    .join('\n');

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="${esc(item.description)}">
<title>${esc(item.title)}｜图文实录</title>
<style>${HTML_CSS}</style>
</head>
<body><main class="container">
<header><h1>${esc(item.title)}</h1>
<div class="meta-row"><span class="meta-tag tag-platform">小红书</span><span class="meta-tag tag-duration">${esc(item.duration)}</span><span class="meta-tag tag-topic">${esc(item.topic)}</span></div>
<a class="source-link" href="${esc(item.url)}" target="_blank" rel="noopener">→ 原视频链接</a></header>
<nav class="toc"><h3>内容导航</h3>
${toc}<a href="#transcript">完整转录</a></nav>
<article class="documentary"><div class="content-points"><h2>内容要点</h2><p>${esc(item.lead)}</p><h3>知识结构</h3>
${summaryRows}
<div class="takeaway-box"><strong>总结</strong><p>${esc(item.takeaway)}</p></div></div>
${chapters}
<section class="transcript-section" id="transcript"><details class="transcript-collapsible"><summary>完整转录（${segs.length}段）</summary>
<div class="transcript-body"><p class="transcript-note">以下文本由 Whisper medium 模型自动转录，可能存在少量识别误差，已尽可能修正明显 ASR 错字。</p>
<div class="transcript-list">
${transcript}
</div></div></details></section>
</article>
</main>
<script>(function(){var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){d.setAttribute("open","")}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){a.addEventListener("click",open)});if(location.hash==="#transcript")open()})();</script>
</body></html>
`;
}

const ITEMS = [
  {
    slug: 'coffee-bean-oil-myth',
    title: '卖豆的人天天讲油脂？别被智商税',
    url: 'https://xhslink.cn/o/41kZeQUP6oQ',
    durationSec: 44.4,
    topic: '精品咖啡 油脂神话 crema 浓缩萃取 认知纠偏',
    description:
      '卖豆话术常把浓缩表面泡沫当「油脂」卖点；视频用快进消泡演示：表面主要是二氧化碳与咖啡液混合泡沫，真正油脂只有零星一点，并类比花生油解释种子本就含油。',
    lead: '作者嘲讽卖豆视频「看油脂、看萃取状态」的话术，用快进消泡把真相钉死：表面那层很快消退的东西，主要是萃取时咖啡粉排出的二氧化碳、少量其他气体、咖啡液与零星油脂形成的混合泡沫——不是卖家口中的「满杯油脂」。浓缩里确实有油脂（像花生一样种子都有），但那不是上面的泡沫；把泡沫当油脂指标，是在拿智商摩擦。',
    takeaway:
      '看浓缩：先分清「会消退的泡沫」与「液面里真正的油脂」。泡沫消退变深是正常物理过程，不能当豆质或新鲜度的神话指标；油脂有，但含量与话术不成正比。',
    structure: [
      ['00:00→00:11', '话术开场', '卖豆人拍「看油脂看萃取」；作者快进演示泡沫很快就消。'],
      ['00:11→00:25', '泡沫成分', '点破「哪有那么多油脂」：成分是 CO₂ + 少量气体 + 咖啡液 + 零星油脂的混合泡沫。'],
      ['00:25→00:36', '晃杯残留', '晃一下剩顽固泡沫与一丢丢油脂；泡沫消退后颜色变深。'],
      ['00:36→00:44', '真正油脂', '浓缩有油脂≠上面泡沫；油脂像花生油一样种子本有；话术=智商税。'],
    ],
    chapters: [
      {
        nav: '话术开场：看油脂不如看泡沫会消',
        range: '00:00-00:11',
        title: '话术开场：看油脂不如看泡沫会消',
        paras: [
          '开场直接点名卖咖啡豆的人拍视频「看着油脂、看着萃取状态」，语气嘲讽这类表演式品鉴。作者说今天快进看这到底是啥——画面里浓缩表面那层厚厚的金棕色泡沫，用不了多久就消了。',
          '第一刀落在直觉上：咖啡豆哪有那么多油脂？观众若只听卖家口播，很容易把「厚 crema/泡沫」误当成「油多＝豆好」。',
        ],
        figures: [
          {
            file: 'shot-01.jpg',
            time: '00:04',
            alt: '玻璃量杯中新鲜浓缩，表面厚厚金棕色泡沫，字幕嘲讽看油脂话术',
            cap: '玻璃量杯里厚厚金棕色表面层，字幕吐槽卖豆「看油脂」话术的开场',
          },
          {
            file: 'shot-02.jpg',
            time: '00:09',
            alt: '快进消泡后表面层明显变薄，说明泡沫不持久',
            cap: '快进消泡对照：用不了多久表面泡沫就消退，质疑「满杯油脂」叙事',
          },
        ],
      },
      {
        nav: '成分拆解：CO₂混合泡沫不是「油脂」',
        range: '00:11-00:25',
        title: '成分拆解：CO₂混合泡沫不是「油脂」',
        paras: [
          '作者不知道「哪个 RB 开始传的」——这层被叫成油脂的东西，其实是萃取过程中咖啡粉排出的二氧化碳，加上一丢丢其他气体、咖啡液，以及零星点点的咖啡油脂，共同产生的混合泡沫。',
          '关键词是「混合泡沫」和「零星点点」：承认有极少量油脂，但主体不是油；把主体叫成油脂，才是营销夸大。',
        ],
        figures: [
          {
            file: 'shot-03.jpg',
            time: '00:21',
            alt: '侧拍浓缩分层，字幕提到咖啡液，对应混合泡沫成分解说',
            cap: '侧拍浓缩深浅分层，口播拆解泡沫里还有咖啡液与气体，不只是油',
          },
        ],
      },
      {
        nav: '晃杯残留与真正油脂',
        range: '00:25-00:44',
        title: '晃杯残留与真正油脂',
        paras: [
          '等不及就晃一下：剩下顽固泡沫和一丢丢油脂；随着泡沫消退，颜色也变深。画面俯拍把「顽固泡沫」钉在字幕上，让观众看到消退后剩下的东西很少。',
          '收束三句：浓缩里面是有油脂的，但它并不是上面的泡沫；咖啡油脂和花生里的油脂一样，所有种子都有油脂；说白了，这类话术就是拿智商在地上摩擦。',
        ],
        figures: [
          {
            file: 'shot-04.jpg',
            time: '00:26',
            alt: '俯拍晃杯后表面残留，字幕「剩下这些顽固泡沫和一丢丢油脂」',
            cap: '俯拍晃杯后：字幕钉死「顽固泡沫和一丢丢油脂」，泡沫主体≠油',
          },
          {
            file: 'shot-05.jpg',
            time: '00:36',
            alt: '俯拍浓缩表面中央破洞见深色液面，字幕「咖啡油脂」',
            cap: '泡沫消退见深色液面，字幕标「咖啡油脂」——点明真正油脂在液里而非厚泡沫',
          },
        ],
      },
    ],
    svg: {
      tags: ['咖啡', '油脂', 'crema', '浓缩', '认知纠偏'],
      summary:
        '卖豆话术把浓缩表面泡沫当「油脂」卖点；证据显示那层会快消的是以 CO₂ 为主的混合泡沫，真正油脂只有零星一点，种子含油本属常态，泡沫厚度不是智商税式质量指标。',
      timeline: [
        ['00:00-00:11', '嘲讽「看油脂」话术，快进证明泡沫会消'],
        ['00:11-00:25', '拆解：CO₂+气体+咖啡液+零星油脂＝混合泡沫'],
        ['00:25-00:36', '晃杯：顽固泡沫+一丢丢油脂；消退变深'],
        ['00:36-00:44', '有油脂≠上面泡沫；类比花生；结论智商税'],
      ],
      map: [
        ['话术泡沫', '混合泡沫'],
        ['CO₂为主', '零星油脂'],
        ['种子含油', '别当指标'],
      ],
      corrections: [
        '表面厚厚金棕色层 ≠「咖啡豆油脂很多」；主体是萃取排气形成的泡沫。',
        '浓缩确实含油脂，但口播明确「并不是上面的泡沫」。',
        '「所有种子都有油脂」说明含油是常态，不能单独证明豆好/新鲜。',
        '泡沫消退后颜色变深是正常过程，不等于「油被偷走了」或豆质崩了。',
      ],
      cards: [
        {
          tone: '',
          title: '核心命题：分清泡沫与油脂',
          body: '营销把 crema/泡沫视觉当油脂含量表演；物理上泡沫是气体裹挟液体与微量油的混合物，消退快、不稳定，不适合当选豆硬指标。',
          quote: '咖啡豆哪有那么多油脂 / 这就是混合泡沫',
          relation: '诊断顺序：先问「会不会消」→再问「剩多少」→再谈油脂。',
        },
        {
          tone: 'card-orange',
          title: '证据链：快进消泡 + 晃杯残留',
          body: '快进看泡沫消掉；晃一下只剩顽固泡沫与一丢丢油脂。两步把「满杯油脂」叙事压成「微量残留」。',
          quote: '剩下这些顽固泡沫和一丢丢油脂',
          relation: '可复现实验：萃取后静置/晃杯对照拍一段即可自证。',
        },
        {
          tone: 'card-green',
          title: '真正油脂：有，但不是那层',
          body: '作者承认浓缩有油脂，并用花生类比——种子普遍含油。重点从「有没有油」转到「油在哪、话术夸大到什么程度」。',
          quote: '浓缩里面是有油脂的，但它并不是上面的泡沫',
          relation: '纠偏：承认事实中的真部分，拆掉夸大部分。',
        },
        {
          tone: 'card-red',
          title: '行动建议：换指标',
          body: '选豆更该看烘焙日期、产地处理、冲煮配方与杯测风味，而不是卖家特写里泡沫有多厚。',
          quote: '说白了它就是拿你智商在地上摩擦',
          relation: '避坑：别被「油脂感」三个字绑架购买决策。',
        },
      ],
      boundary: [
        '短视频科普语气犀利，非实验室油脂定量分析。',
        '深烘豆表面油光（焙烤渗油）与浓缩 crema 泡沫是不同现象，勿混为一谈。',
        '新鲜豆排气多可能泡沫更明显，但仍不等于「油脂多＝好」。',
      ],
      pitfalls: [
        '把 crema 厚度当新鲜度/豆质唯一指标。',
        '听卖家「看油脂」话术不下单前自己静置观察。',
        '把「有油脂」听成「全是油脂」。',
      ],
      conclusion: {
        key: [
          '表面泡沫≈CO₂混合泡沫，会消退',
          '真正油脂有但量少，且不是泡沫本身',
          '种子含油常态 ≠ 营销卖点',
        ],
        actions: [
          '买豆前忽略「油脂特写」，要烘焙日期与冲煮建议',
          '回家萃取后静置 30–60 秒观察泡沫是否消退',
          '杯测风味与配方复现，比泡沫颜值优先',
        ],
        shift:
          '以前：看见厚泡沫就觉得豆油、豆好；现在：先分泡沫与油脂，把视觉表演从决策变量里删掉。',
      },
    },
    index: {
      summary:
        '卖豆「看油脂」多半在演泡沫：浓缩表面主要是 CO₂ 混合泡沫，真正油脂只有零星；种子含油是常态，别把泡沫厚度当选豆智商税指标。',
      tags: ['咖啡', '油脂', 'crema', '浓缩', '认知纠偏', '选豆'],
      skills: ['选豆'],
    },
  },
  {
    slug: 'blend-vs-single-origin',
    title: '拼配豆or单品豆',
    url: 'https://xhslink.cn/o/4bBnhgGAYAe',
    durationSec: 75.56,
    topic: '精品咖啡 拼配豆 单品豆 醇厚度 阿拉比卡 罗布斯塔',
    description:
      '用豆子外观差异演示什么是拼配：多品种（可含罗布斯塔）互补风味与醇厚度；澄清并非所有拼配都要加罗布斯塔；单品豆=单一品种不加别的，并幽默暗示「好东西谁舍得乱拼」。',
    lead: '作者先亮出一款颜色、外形不一致的拼配豆，再拆成多个阿拉比卡分支品种加一款罗布斯塔「拌在一起」的定义。接着用优缺点对照解释为什么拼：花果香好但醇厚度不够、坚果香好仍缺醇厚度，中庸罗布斯塔补醇厚度，四者刚合适。随后紧急纠偏——举例而已，不是所有拼配都要加罗布斯塔，也有三种阿拉比卡拼配；拼配无非为了丰富层次或表现更多风味。最后用洪都拉斯单品豆定义「自己一个品种、没加别的」，并以玩笑收尾。',
    takeaway:
      '拼配=多豆互补（常见目标：风味层次 + 醇厚度）；单品=单一品种不混。罗布斯塔是可选工具不是拼配必选项；「好单品不乱拼」是价值判断，不是科学禁令。',
    structure: [
      ['00:00→00:21', '定义拼配', '外观不一的豆子混在一起；多支阿拉比卡 + 罗布斯塔示例。'],
      ['00:21→00:49', '为何拼配', '香气好缺醇厚度 → 用罗布斯塔补醇厚度，四豆平衡。'],
      ['00:49→01:03', '纠偏', '非必须加罗布斯塔；也可纯阿拉比卡拼；目的=层次/风味。'],
      ['01:03→01:15', '单品定义', '洪都拉斯单品=单一品种；玩笑「好东西谁舍得加别的」。'],
    ],
    chapters: [
      {
        nav: '什么是拼配：外观不一拌在一起',
        range: '00:00-00:21',
        title: '什么是拼配：外观不一拌在一起',
        paras: [
          '开场提问：拼配豆和单品豆都是啥意思、又为啥拼配。镜头给出一款拼配豆——颜色不一样、长得也不一样，用肉眼差异先建立「混合」直觉。',
          '打比方依次指认：阿拉比卡分支品种一、二、三，再加一种罗布斯塔，把它们拌在一起，就成了一款拼配豆。',
        ],
        figures: [
          {
            file: 'shot-01.jpg',
            time: '00:09',
            alt: '大理石面上标注阿拉比卡某品种一的豆堆，字幕「打个比方」',
            cap: '俯拍豆堆标注「阿拉比卡（某品种一）」，开始举例拆解拼配组成',
          },
        ],
      },
      {
        nav: '为什么拼：香气与醇厚度互补',
        range: '00:21-00:49',
        title: '为什么拼：香气与醇厚度互补',
        paras: [
          '好好的豆为啥拼？两款花香果香很好但醇厚度不够；另一款坚果味浓郁、咖啡香气好，仍缺一点醇厚度。',
          '一款比较中庸的罗布斯塔登场：风味不够丰富，但带来的醇厚度正好均衡上面三个豆的缺点。四个拌在一起——风味有了、醇厚度有了；单拿一个都会觉得缺点什么，拼在一起刚刚好。',
        ],
        figures: [
          {
            file: 'shot-02.jpg',
            time: '00:21',
            alt: '深浅两堆豆子对照，字幕「为啥拼在一起」',
            cap: '深浅两堆豆对照提问「为啥拼在一起」，切入优缺点互补逻辑',
          },
          {
            file: 'shot-03.jpg',
            time: '00:34',
            alt: '四堆豆子优缺点标注，底部罗布斯塔框出，字幕「风味不够丰富」',
            cap: '四堆豆优缺点对照：前排香气好但醇厚度低，框出的罗布斯塔补醇厚度',
          },
        ],
      },
      {
        nav: '纠偏与单品：不是必须加罗豆',
        range: '00:49-01:15',
        title: '纠偏与单品：不是必须加罗豆',
        paras: [
          '紧急澄清：只是举例，可不是所有拼配豆都要加罗布斯塔；也有三种阿拉比卡拼在一起的豆子。拼配无非两种原因：一是丰富层次，二是表现更好、更多的风味。',
          '镜头给出洪都拉斯单品豆：自己一个品种、没加别的，这就叫单品豆。收尾玩笑「好东西谁舍得加别的乱七八糟」——价值暗示大于技术定义，并自嘲别骂我。',
        ],
        figures: [
          {
            file: 'shot-04.jpg',
            time: '00:48',
            alt: '深色豆堆，字幕「你可别误会啊」提醒举例非通则',
            cap: '字幕「你可别误会啊」——强调罗布斯塔入拼只是举例不是通则',
          },
          {
            file: 'shot-05.jpg',
            time: '01:02',
            alt: '均匀豆堆，字幕「这种就是来自洪都拉斯的」单品示例',
            cap: '均匀单堆豆：字幕点出洪都拉斯来源，示范「单一品种」的单品豆',
          },
        ],
      },
    ],
    svg: {
      tags: ['咖啡', '拼配豆', '单品豆', '醇厚度', '阿拉比卡', '罗布斯塔'],
      summary:
        '拼配是多品种互补（常见补醇厚度与层次）；罗布斯塔可选不是必选项；单品=单一品种不加别的。选豆先问目标是平衡配方还是风味表达，再决定拼或单。',
      timeline: [
        ['00:00-00:21', '外观不一→多品种拌和=拼配定义'],
        ['00:21-00:49', '香气好缺醇厚度→罗豆补醇厚度举例'],
        ['00:49-01:03', '纠偏：可不加罗豆；目的=层次/风味'],
        ['01:03-01:15', '洪都拉斯单品定义；价值玩笑收尾'],
      ],
      map: [
        ['多豆混合', '优缺互补'],
        ['醇厚度工具', '罗豆可选'],
        ['单品表达', '目标选型'],
      ],
      corrections: [
        '拼配 ≠ 一定加罗布斯塔；视频明确有纯阿拉比卡拼配。',
        '罗布斯塔在举例里扮演「补醇厚度」工具，不是「低级豆」标签本身。',
        '单品「好东西不乱拼」是价值修辞，技术上精品拼配也很常见。',
        '「颜色长得不一样」是入门观察线索，深烘/浅烘同品种也可能色差。',
      ],
      cards: [
        {
          tone: '',
          title: '定义：拼配 vs 单品',
          body: '拼配=多个品种/批次拌在一起；单品=自己一个品种、没加别的。先把名词钉死，再谈为什么拼。',
          quote: '把它们拌在一起，这就成了一款拼配豆 / 这就叫单品豆了',
          relation: '买豆看包装：Blend / Single Origin 对应这两类。',
        },
        {
          tone: 'card-orange',
          title: '机制：互补缺陷',
          body: '花果香、坚果香好的豆可能醇厚度不够；中庸罗布斯塔风味不丰富但醇厚度能托底。拼配是配方工程，不是随便搅和。',
          quote: '风味有了，醇厚度有了……拼在一起呢就刚刚好了',
          relation: '问自己：缺的是香气层次还是口感厚度？',
        },
        {
          tone: 'card-green',
          title: '目的只有两类',
          body: '口播收成：丰富层次；表现更好、更多风味。其他营销词（神秘配方）都要回到这两类可验证目标。',
          quote: '拼配无非就是两种原因：一是丰富层次，二是表现更好更多的风味',
          relation: '行动：让店家说明拼配要解决的具体缺陷。',
        },
        {
          tone: 'card-purple',
          title: '边界：举例≠处方',
          body: '作者连说「你可别误会」——四豆模型是教学脚手架。实战比例、是否加罗豆、烘焙曲线都要另案设计。',
          quote: '我就是举例说明而已',
          relation: '别把视频配方当唯一正确拼法。',
        },
      ],
      boundary: [
        '短视频举例未给出具体拼配比例与烘焙度。',
        '「洪都拉斯」在此作单品产地示例，不代表该国只有单品。',
        '商业意式拼配还要考虑油脂、crema、奶咖耐受等，超出本片范围。',
      ],
      pitfalls: [
        '以为拼配必须加罗布斯塔。',
        '觉得单品一定优于拼配（或反过来）。',
        '只看豆子外观色差就断定好坏。',
      ],
      conclusion: {
        key: [
          '拼配=互补配方；单品=单一表达',
          '罗布斯塔是可选醇厚度工具',
          '选型服从目标：平衡 vs 风味个性',
        ],
        actions: [
          '买豆先写目标：奶咖稳定 / 手冲风味 / 浓缩底韵',
          '问清拼配组成与是否含罗布斯塔及大致比例',
          '单品与拼配各冲一壶对照醇厚度与香气',
        ],
        shift:
          '以前：纠结「拼配低端、单品高端」；现在：按缺陷互补看拼配，按风味纯度看单品。',
      },
    },
    index: {
      summary:
        '拼配是多品种互补（常补醇厚度与层次），罗布斯塔可选非必须；单品=单一品种。按目标选平衡配方或风味表达，莫神话单品。',
      tags: ['咖啡', '拼配豆', '单品豆', '醇厚度', '阿拉比卡', '罗布斯塔'],
      skills: ['选豆'],
    },
  },
  {
    slug: 'coffee-bean-varieties',
    title: '不同品种咖啡豆的区别',
    url: 'https://xhslink.cn/o/5APTJtXX0eM',
    durationSec: 106.36,
    topic: '精品咖啡 阿拉比卡 罗布斯塔 利比瑞卡 咖啡因 种植',
    description:
      '三大品种先排除市面少见的利比瑞卡；对照阿拉比卡与罗布斯塔的中缝曲直、体型、咖啡因、风味、种植难度；强调平均对比，高品质罗布斯塔可胜过低品质阿拉比卡，并预告意式拼配用途。',
    lead: '承接「三大品种」话题：先排除细长像瓜子的利比瑞卡（市面不常见）。重点对比阿拉比卡与罗布斯塔——中缝弯/直、体型长/短饱满；罗布斯塔咖啡因更高（有的约高一倍），过高也不好；风味上阿拉比卡花果香更丰富、酸甜苦更复合，罗布斯塔香气少偏苦；种植上阿拉比卡娇贵、要海拔气候且不耐病虫害，罗布斯塔抗造好种。总结后强调凡事没有绝对：高品质罗布斯塔可比低品质阿拉比卡好很多，只是平均对比；罗布斯塔常与阿拉比卡按比例混作意式拼配，下集再说。',
    takeaway:
      '认豆先看中缝与体型，再记咖啡因/风味/种植三条平均差异；品种标签不能代替品质等级——好罗豆可以打过差阿豆。',
    structure: [
      ['00:00→00:15', '排除利比瑞卡', '三大品种里利比瑞卡市面少见，先放下。'],
      ['00:15→00:26', '外观', '阿豆中缝弯、体型偏长；罗豆中缝直、偏短饱满。'],
      ['00:26→00:51', '咖啡因与风味', '罗豆咖啡因更高；阿豆风味更复合，罗豆偏苦。'],
      ['00:51→01:24', '种植与总结', '阿豆娇贵金贵；罗豆抗造；平均对比+品质例外。'],
      ['01:24→01:46', '用途预告', '罗豆常入意式拼配，下集讲为什么拼。'],
    ],
    chapters: [
      {
        nav: '三大品种：先放下利比瑞卡',
        range: '00:00-00:15',
        title: '三大品种：先放下利比瑞卡',
        paras: [
          '「上次咱不是说咖啡豆有这三大品种吗？今天咱就说它们有啥区别。」先排除细长、像瓜子式的利比瑞卡——知道有这个品种就行，市面上不常见，于是把镜头留给剩下俩。',
        ],
        figures: [
          {
            file: 'shot-01.jpg',
            time: '00:11',
            alt: '三颗豆横排对比阿拉比卡、罗布斯塔、利比瑞卡，字幕市面不常见',
            cap: '三品种并排：右侧尖长利比瑞卡，字幕「市面上不常见」故先排除',
          },
        ],
      },
      {
        nav: '外观与咖啡因',
        range: '00:15-00:38',
        title: '外观与咖啡因',
        paras: [
          '外观看中间这条线：阿拉比卡是弯的，罗布斯塔是直的；阿拉比卡多数体型偏长，罗布斯塔多数短一点、饱满一点。',
          '再说咖啡因含量：罗布斯塔要高出阿拉比卡很多，甚至有些要高出一倍。咖啡因由肝脏代谢，太高也不是好事——把「含量高」从卖点改写成需要节制的变量。',
        ],
        figures: [
          {
            file: 'shot-02.jpg',
            time: '00:31',
            alt: '阿拉比卡1.1%-1.7%与罗布斯塔2%-4%咖啡因对比图',
            cap: '画面标注咖啡因区间：阿拉比卡约1.1%–1.7%，罗布斯塔约2%–4%，可高出一倍',
          },
        ],
      },
      {
        nav: '风味、种植与品质例外',
        range: '00:38-01:46',
        title: '风味、种植与品质例外',
        paras: [
          '风味：阿拉比卡花果香更丰富，酸甜苦更复合；罗布斯塔香气较少、风味比较苦。种植：阿拉比卡娇贵，对产地、海拔、纬度、气候要求高且不耐病虫害；罗布斯塔抗造，环境海拔要求小很多——作者开玩笑说可能咖啡因太高虫子都不敢吃。',
          '不好种植的就会金贵一些。总结后立刻刹车：凡事没有绝对，高品质罗布斯塔也要比低品质阿拉比卡好很多，这只是平均对比。罗布斯塔多数风味一般，但仍有作用，比如与阿拉比卡按比例混合成意式拼配——为什么拼，下集再说。',
        ],
        figures: [
          {
            file: 'shot-03.jpg',
            time: '00:51',
            alt: '阿豆与罗豆外观对照，字幕转入「再说种植」',
            cap: '弯缝长豆 vs 直缝圆豆对照后，字幕转入种植条件差异',
          },
          {
            file: 'shot-04.jpg',
            time: '01:08',
            alt: '金元宝与银元宝隐喻阿豆更金贵，字幕不好种植更金贵',
            cap: '金银元宝隐喻：难种的阿拉比卡更「金贵」，对应种植门槛',
          },
          {
            file: 'shot-05.jpg',
            time: '01:26',
            alt: '拟人总结卡强调高品质罗布斯塔可优于低品质阿拉比卡',
            cap: '拟人总结卡：平均画像之外，字幕强调高品质罗豆可打过低品质阿豆',
          },
        ],
      },
    ],
    svg: {
      tags: ['咖啡', '阿拉比卡', '罗布斯塔', '利比瑞卡', '咖啡因', '选豆'],
      summary:
        '三大品种先搁置少见利比瑞卡；阿豆弯缝偏长、风味复合、种植娇贵；罗豆直缝偏圆、咖啡因更高偏苦、抗造好种。记住这是平均像，品质等级可以翻转品种刻板印象。',
      timeline: [
        ['00:00-00:15', '排除市面少见的利比瑞卡'],
        ['00:15-00:26', '中缝弯/直 + 体型长/短'],
        ['00:26-00:51', '咖啡因与风味平均差异'],
        ['00:51-01:24', '种植难度、金贵感与品质例外'],
        ['01:24-01:46', '罗豆入意式拼配用途预告'],
      ],
      map: [
        ['外观识别', '成分风味'],
        ['种植门槛', '平均画像'],
        ['品质例外', '拼配用途'],
      ],
      corrections: [
        '「阿拉比卡一定更好」不成立：视频强调高品质罗布斯塔可胜过低品质阿拉比卡。',
        '咖啡因更高不是单纯优点；口播提醒肝脏代谢、太高不好。',
        '利比瑞卡不是不存在，只是国内零售少见，勿当成「只有两种豆」。',
        '画面咖啡因百分比是科普示意区间，具体批次仍以检测/庄园数据为准。',
      ],
      cards: [
        {
          tone: '',
          title: '识别：中缝与体型',
          body: '阿拉比卡中缝弯、多数偏长；罗布斯塔中缝直、多数短而饱满。这是入门肉眼线索，不是实验室鉴定。',
          quote: '阿拉比卡是弯的，罗布斯塔是直的',
          relation: '买生豆/熟豆时可先做形态分类再谈风味。',
        },
        {
          tone: 'card-orange',
          title: '咖啡因：数量与代价',
          body: '罗布斯塔咖啡因显著更高（示意可到约两倍）。含量高带来提神与抗虫叙事，也带来「太高不好」的健康提醒。',
          quote: '甚至有些要高出一倍 / 咖啡因太高也不是一件好事',
          relation: '选豆时把咖啡因当约束条件，不当唯一卖点。',
        },
        {
          tone: 'card-green',
          title: '风味与种植的平均画像',
          body: '阿豆：花果香、酸甜苦复合、种植要求高故金贵。罗豆：香气少偏苦、好种抗造。这是统计意义的「多数」，方便建框架。',
          quote: '不好种植的肯定就会金贵一些了',
          relation: '框架用于快速分类，细节靠杯测修正。',
        },
        {
          tone: 'card-red',
          title: '例外与下一步：拼配',
          body: '品质可以翻转品种偏见；罗布斯塔在意式拼配里常按比例混入——机制留到下集（与本批拼配篇互证）。',
          quote: '高品质的罗布斯塔也要比低品质的阿拉比卡要好很多',
          relation: '决策：先看批次品质，再看品种标签。',
        },
      ],
      boundary: [
        '未展开利比瑞卡风味与产区细节。',
        '未给具体杯测分数或庄园案例。',
        '「意式拼配」只预告，比例与烘焙不在本片。',
      ],
      pitfalls: [
        '只认阿拉比卡牌子，无视烘焙与瑕疵豆。',
        '把罗布斯塔一律打成「坏豆」。',
        '用咖啡因高低替代风味判断。',
      ],
      conclusion: {
        key: [
          '先排除少见利比瑞卡，聚焦阿/罗对照',
          '外观→咖啡因→风味→种植 四层平均差异',
          '品质例外优先于品种刻板印象',
        ],
        actions: [
          '练一眼：弯缝长豆 vs 直缝圆豆',
          '买豆同时看品种与烘焙日期/处理法',
          '对「纯阿豆」宣传追问批次与瑕疵率',
          '若喝意式，了解拼配是否含罗豆及目的',
        ],
        shift:
          '以前：阿拉比卡=好、罗布斯塔=差；现在：先看平均画像，再用品质等级允许翻转，并理解罗豆在拼配中的功能位。',
      },
    },
    index: {
      summary:
        '阿豆弯缝风味复合但娇贵，罗豆直缝咖啡因高偏苦却抗造；利比瑞卡市面少见。平均对比之外，高品质罗豆可胜过低品质阿豆。',
      tags: ['咖啡', '阿拉比卡', '罗布斯塔', '利比瑞卡', '咖啡因', '选豆'],
      skills: ['选豆'],
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

  const svgData = {
    title: item.title,
    tags: item.svg.tags,
    duration: item.duration,
    perspective: '理性分析',
    url: item.url,
    summary: item.svg.summary,
    timeline: item.svg.timeline,
    map: item.svg.map,
    corrections: item.svg.corrections,
    cards: item.svg.cards,
    boundary: item.svg.boundary,
    pitfalls: item.svg.pitfalls,
    conclusion: item.svg.conclusion,
  };
  const { svg, height } = await buildSvg({ css: SVG_CSS, body: buildSvgBody(svgData), width: 1320 });
  const svgPath = path.join(DOCS, `${item.slug}-理性分析.svg`);
  fs.writeFileSync(svgPath, svg, 'utf8');

  const summary = item.index.summary;
  if ([...summary].length > 120) {
    console.warn('summary too long', item.slug, [...summary].length);
  }

  const entry = {
    date: '2026-09-12',
    title: item.title,
    summary,
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
    primary: 'coffee',
    skills: item.index.skills,
  };
  upsertIndex(entry);

  results.push({ slug: item.slug, htmlPath, svgPath, height, summary, segs: segs.length, duration: item.duration });
  console.log('OK', item.slug, 'segs', segs.length, 'svg_height', height, 'duration', item.duration);
}

console.log(JSON.stringify(results, null, 2));
