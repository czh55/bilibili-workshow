#!/usr/bin/env node
/** B57 batch1：piano-fingertip-catch + host-speak-visual-sense + host-express-day3-ai */
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

/** 转录区保留 ASR 原样；正文引用另走纠错 */
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
    slug: 'piano-fingertip-catch',
    title: '第13集｜一个动作让你弹出更专业的感觉',
    shortTitle: '钢琴指尖抓住',
    url: 'https://xhslink.cn/o/AuZje16MzUF',
    durationSec: 220.72,
    primary: 'other',
    description:
      '钢琴强奏「出不来力」或「响却吵」时，先送大臂再让力流动，最后用指尖瞬间抓住立住；对照拍苍蝇式砸键，旋律更透亮、可与左手伴奏分离。',
    lead: '作者对比「用指尖 / 不用指尖」的听感，点出穿音教授课上的提壶灌顶：弹强时明明使劲，却要么力量出不来，要么响得吵、闹。前提是大臂往前送、不耸肩；力要流动，不能拍苍蝇式砸死。精髓是送完后指尖瞬间抓住、立住——音更透亮不死，旋律也更清晰，左手触键则像章鱼一样摸、三关节主动而不必过度勾尖。',
    takeaway: '先送大臂 → 力流动 → 指尖瞬间抓住立住；砸下去不动=拍苍蝇，响≠专业。',
    structure: [
      ['00:00→00:41', '问题立题', '强音使劲却出不来，或响却吵；提壶灌顶点在「抓指尖」。'],
      ['00:41→01:16', '前提：大臂送', '不耸肩、往前推琴；站起试 Ring Drops，先让手臂出来。'],
      ['01:16→02:23', '精髓：指尖抓住', '力流动 + 送完瞬间抓住立住；对照不抓=吵且死。'],
      ['02:23→03:41', '旋律与左手', '指尖让旋律清晰；左手章鱼摸触、三关节主动。'],
    ],
    chapters: [
      {
        range: '00:00 → 00:41',
        title: '响≠专业：问题出在「抓指尖」',
        paras: [
          '开场先让人听「用指尖和不用指尖」的区别。作者说这是昨天听穿音教授讲课时被提壶灌顶的一点：弹强时觉得已经很使劲，力量却出不来；或者已经弹得很响，老师仍说「你好吵啊，有点闹」。',
          '精髓落在「抓指尖那么一下」。读书时老师也讲过：前提是大臂要送，不能怂肩，大臂与身体往前送，感觉在往前推钢琴——这一步没做到，后面都白练。',
        ],
        figures: [
          {
            file: 'shot-01.jpg',
            time: '00:20',
            alt: '钢琴前讲解，字幕「你弹的好吵啊有点闹」',
            cap: '立题：响却被说吵闹——问题不在音量，而在触键方式',
          },
        ],
      },
      {
        range: '00:41 → 01:16',
        title: '先送大臂：站起来练 Ring Drops',
        paras: [
          '若大臂还没送出去，先尝试站起来，用曲目片段（口播 Ring Drops）把前面几个音「送出来」，感觉整个手臂往下走。',
          '做到这一步之后，若仍觉得吵、音很死僵在那里，就要进入下一层：不是再砸重一点，而是让力流动起来。',
        ],
        figures: [
          {
            file: 'shot-02.jpg',
            time: '00:55',
            alt: '侧身示范触键，字幕「你就要出来」',
            cap: '站姿/送臂示范：前面几个音要把力量「送出来」',
          },
        ],
      },
      {
        range: '01:16 → 02:23',
        title: '拍苍蝇 vs 指尖抓住',
        paras: [
          '「啪一下下去不动」就像拍苍蝇——声音大但死。一定要让力流动；完成流动后再加上精髓：指尖立住，送完瞬间抓住，音就感觉立起来了。',
          '对照听：不抓住会很吵、虽然也很大；加上指尖不仅更透亮，而且不死，听感多了一层「立住」的坚实。本段演示刻意只弹抓住的强音，不做别的音乐处理。',
        ],
        figures: [
          {
            file: 'shot-03.jpg',
            time: '01:35',
            alt: '讲解中，字幕「再加上那个精髓」',
            cap: '切入精髓：在送臂与力流动之上，加上指尖抓住',
          },
          {
            file: 'shot-04.jpg',
            time: '02:20',
            alt: '侧拍触键，屏幕提示只演示指尖抓住的强音',
            cap: '对照演示：只用指尖抓住的强音，听透亮与「不死」',
          },
        ],
      },
      {
        range: '02:23 → 03:41',
        title: '旋律清晰 + 左手像章鱼',
        paras: [
          '用上指尖后，旋律更清晰，能和左手伴奏区别开。左手触键也要变：去摸，像章鱼一样——不必把指尖勾得特别厉害，但三关节非常主动、立起来。',
          '收束：不论弹强时的「抓住」，还是单旋律的「指尖往回勾一下」，都要去试——一定要把指尖勾出去。',
        ],
        figures: [
          {
            file: 'shot-05.jpg',
            time: '03:10',
            alt: '侧拍触键，字幕「去摸像章鱼一样」',
            cap: '左手比喻：像章鱼去摸，三关节主动，不必过度勾尖',
          },
        ],
      },
    ],
    svg: {
      tags: ['钢琴', '指尖', '触键', '强音', '演奏技巧'],
      summary:
        '强音「出不来」或「响却吵」，多半缺大臂输送与指尖瞬间抓住；力流动代替拍苍蝇式砸键，音才透亮立住，旋律才能与伴奏分离。',
      timeline: [
        ['00:00', '对比用/不用指尖的听感'],
        ['00:08', '立题：使劲却无力，或响却吵闹'],
        ['00:24', '精髓预告：抓指尖'],
        ['00:30', '前提：大臂送、不耸肩、推琴'],
        ['01:16', '反例：拍苍蝇式砸死'],
        ['01:31', '力流动 + 指尖立住抓住'],
        ['02:05', '对照：抓住更透亮不死'],
        ['02:53', '左手章鱼摸触、三关节主动'],
      ],
      map: ['问题：响或无力', '前提：大臂送', '力要流动', '指尖抓住立住'],
      corrections: [
        'ASR「提胡冠典」→提壶灌顶；「筋髓」→精髓；「触件」→触键。',
        '误解：音量更大=更专业。纠偏：拍苍蝇式砸键会吵、会死。',
        '误解：只会勾指尖就够。纠偏：先送大臂，再谈抓住。',
        '左手不是把指尖勾死，而是三关节主动、像章鱼去摸。',
      ],
      cards: [
        {
          tone: 'card-orange',
          title: '诊断：响≠专业',
          body: '两种失败态：力量出不来，或已经很响仍被说吵闹。共同指向触键缺少「抓住」与力的流动。',
          quote: '「为什么力量还是出不来……老师为什么总说你弹得好吵啊有点闹」[00:12–00:21]',
          pitfall: '继续加力砸键，只会更吵更死。',
          action: '先录音对照：同一乐句「砸死」vs「抓住」，听透亮与余音。',
        },
        {
          tone: 'card-green',
          title: '前提：大臂送出去',
          body: '指尖技巧建立在大臂与身体往前送之上；耸肩、手臂不参与，后面抓住无效。',
          quote: '「大臂身体是要往前送，感觉在往前推钢琴」[00:33–00:38]',
          pitfall: '只练手指、忽略站起送臂的检查动作。',
          action: '站立慢练短句，确认肩放松、手臂重量能送进琴键。',
        },
        {
          title: '精髓：瞬间抓住立住',
          body: '力先流动，送完后指尖立住抓住；对照不抓=大而吵、僵死。抓住后强音更透亮，旋律也更清晰。',
          quote: '「送完之后，瞬间给它抓住……不仅会更透亮，而且它没有那么死」[01:37–02:11]',
          pitfall: '「啪一下下去不动」——拍苍蝇。',
          action: '单音练习：送→流→抓，听「立起来」的一刻。',
        },
        {
          tone: 'card-red',
          title: '左手：章鱼摸触',
          body: '伴奏层不必过度勾尖，但三关节要主动立起，才能让右手旋律浮出来。',
          quote: '「去摸像章鱼一样……三关节是非常主动的」[03:07–03:16]',
          pitfall: '左右手同一套「死勾」，层次糊成一团。',
          action: '分手练：右手抓尖立旋律，左手轻摸控伴奏。',
        },
      ],
      boundary: [
        '短视频聚焦强音与指尖抓住，不含完整踏板/踏板层次与音色配色。',
        '曲目片段口播作演示载体，动作原则可迁移，不必拘泥曲名。',
        '不同琴键阻力与坐姿会影响「送」的幅度，需按自己的琴校准。',
      ],
      pitfalls: [
        '把「专业感」理解成一味弹响。',
        '跳过大臂输送，直接猛练勾指。',
        '左手过度勾尖，压死伴奏空间。',
      ],
      conclusion: {
        key: [
          '强音问题先分：出不来 vs 响却吵',
          '顺序：大臂送 → 力流动 → 指尖抓住',
          '左手摸触分层，右手抓住立旋律',
        ],
        actions: [
          '选一小句强音，录三段：砸死 / 只送臂 / 送+抓住',
          '站立检查耸肩，再坐回慢速抓住',
          '分手练章鱼左手 + 抓住右手，再合手听层次',
        ],
        shift: '以前：响=有力=专业；现在：力要送、要流、要被指尖接住，专业感来自立住与透亮，而不是音量。',
      },
    },
    index: {
      summary:
        '强音出不来或响却吵：先送大臂让力流动，再指尖瞬间抓住立住；告别拍苍蝇式砸键，旋律才透亮可分层。',
      tags: ['钢琴', '指尖', '触键', '强音', '演奏技巧'],
    },
  },
  {
    slug: 'host-speak-visual-sense',
    title: '主持人手把手跟练🎤4天练出说话的“画面感”',
    shortTitle: '说话的画面感',
    url: 'https://xhslink.cn/o/AKsu46fhtFo',
    durationSec: 106.16,
    primary: 'workplace',
    description:
      '说话干巴、对方只回「哦对」时，用五感钩子法每次只挑两个感官细节，把经历说成可放映的画面；示例从「风很大」改到风雨砸树、广告牌抖，再到泡面咕嘟香辣。',
    lead: '开场点破：你说话别人总记不住，对方只会「哦对」然后就没有然后了。四天只练一件事——具体化，让听者脑子里自动放电影。前三天练结构把话说顺之后，仍可能干巴巴。作者从出镜记者经验出发：别说「风真的很大」，要说风雨倾斜砸过来、行道树树冠压得往一边塌、广告牌铁皮哗哗抖得像要撕开。方法叫「五感钩子法」：视听嗅味触里随便挑两个加进话里，多了像作文，两个刚刚好。用「周末煮泡面」改写示范，并布置三天打卡作业。',
    takeaway: '五感里挑两个钩子，把抽象形容词换成可看见/听见/闻到的细节——画面感就来了。',
    structure: [
      ['00:00→00:19', '问题与目标', '记不住、只回哦对；四天练具体化，让对方脑内放电影。'],
      ['00:19→00:35', '记者反例', '别说风很大；风雨砸、树冠塌、广告牌抖——立刻有画面。'],
      ['00:35→00:55', '五感钩子法', '视听嗅味触任选两个；多了像作文，两个刚好。'],
      ['00:55→01:46', '泡面示范与作业', '错误「没干嘛」→感官改写；三天小事打卡 C4。'],
    ],
    chapters: [
      {
        range: '00:00 → 00:19',
        title: '从「哦对」到脑子放电影',
        paras: [
          '痛点很具体：说完对方记不住，只能回「哦对」，话题断掉。今天起四天只练具体化——让听你说话的人脑子里自动放电影，注意力不自觉被吸引。',
          '承接前三天结构练习：话已经不乱套，但还干巴巴。下一刀切在「画面感」。',
        ],
        figures: [
          {
            file: 'shot-01.jpg',
            time: '00:08',
            alt: '车内口播，字幕「让听你说话的人」',
            cap: '立目标：让听者注意力被吸住，脑子里开始「放电影」',
          },
        ],
      },
      {
        range: '00:19 → 00:35',
        title: '出镜记者：别说「风很大」',
        paras: [
          '作者入行从出镜记者做起，写过几千条稿。上台别跟观众说「风风风真的很大」——要说风雨倾斜砸过来，行道树树冠压得往一边塌，广告牌铁皮哗哗抖得像要撕开：是不是马上有画面感？',
          '差异不在形容词强度，而在把抽象「大」换成可见的动作与物体状态。',
        ],
        figures: [
          {
            file: 'shot-02.jpg',
            time: '00:29',
            alt: '暴雨出镜记者指着积水路段，字幕「行道树树冠」',
            cap: '画面证据：用树冠压塌等细节替代「风很大」',
          },
        ],
      },
      {
        range: '00:35 → 00:55',
        title: '五感钩子法：只挑两个',
        paras: [
          '作者把用了十几年的受用方法叫「五感钩子法」：你看到什么颜色形状动作、听到什么声音、闻到什么、尝到什么味道、触摸到什么质感——五个里面随便挑两个，加到要说的话里。',
          '多了会像写作文；两个刚刚好。这是剂量控制，不是感官越多越好。',
        ],
        figures: [
          {
            file: 'shot-03.jpg',
            time: '00:48',
            alt: '车内讲解举手示意，字幕「随便挑两个就行」',
            cap: '方法剂量：五感任选两个，够用且不像作文',
          },
        ],
      },
      {
        range: '00:55 → 01:46',
        title: '泡面改写 + 三天打卡',
        paras: [
          '练习题：周一同事问周末干嘛了。错误版「没干嘛，就在家待着」——话题终结。调整版：周末在家煮了锅泡面，水咕嘟咕嘟冒泡，面饼放进去筷子一搅都散开，客厅都是香辣味，蹲在茶几旁稀溜稀溜吃，连汤喝干净。一样的事，多了两个感官，对方脑子立刻有画面。',
          '作业：接下来三天，每天找一件小事（吃饭、通勤、排队、开会），用五感钩子法描述并录下来自己听；评论区打卡格式 C4 + 今天用五感描述的一件事，最好语音，作者批作业。',
        ],
        figures: [
          {
            file: 'shot-04.jpg',
            time: '01:09',
            alt: '车内煮泡面加香菜，字幕「筷子一搅」',
            cap: '示范素材：咕嘟冒泡、筷子一搅、香辣味——感官钩子落地',
          },
          {
            file: 'shot-05.jpg',
            time: '01:32',
            alt: '车内总结，调色盘图形，字幕「你的话变得有色彩了」',
            cap: '收束：按法练习后，话会「有色彩」',
          },
        ],
      },
    ],
    svg: {
      tags: ['表达', '画面感', '五感钩子', '具体化', '主持人'],
      summary:
        '说话干巴、对方只回「哦对」时，用五感钩子法每次只嵌两个感官细节，把「风很大」「没干嘛」改成可放映的动作与气味画面。',
      timeline: [
        ['00:00', '痛点：说完只剩「哦对」'],
        ['00:05', '四天目标：具体化→脑内电影'],
        ['00:23', '反例改写：风很大→风雨砸/树冠塌'],
        ['00:37', '提出五感钩子法'],
        ['00:48', '剂量：五感里挑两个'],
        ['01:00', '错误版：没干嘛就在家'],
        ['01:04', '泡面感官改写示范'],
        ['01:23', '三天小事录音打卡'],
      ],
      map: ['抽象形容词', '挑两个感官', '嵌进经历', '对方脑内放电影'],
      corrections: [
        'ASR「授意」→受用；「行道术的术官」→行道树树冠；「五感勾字」→五感钩子；「一脚」→一搅；「不买客」→不卖课。',
        '误解：细节越多越好。纠偏：多了像作文，两个刚刚好。',
        '误解：画面感=堆华丽辞藻。纠偏：换成可见可听可闻的具体动作与物件状态。',
      ],
      cards: [
        {
          tone: 'card-orange',
          title: '为何对方记不住',
          body: '结构顺了仍干巴时，信息缺少可被想象的锚点，对话只能礼貌结束。',
          quote: '「对方只能回你哦对，然后就没有然后了」[00:02–00:05]',
          pitfall: '继续加观点、不加画面，话题照样死。',
          action: '下次闲聊先问自己：听的人脑中能「看见」哪一帧？',
        },
        {
          tone: 'card-green',
          title: '五感钩子法',
          body: '视、听、嗅、味、触五选二，嵌进原话。记者台风例子证明：同一天气，具体物件状态秒出画面。',
          quote: '「这五个里面随便挑两个就行……多了呢会像写作文」[00:48–00:53]',
          pitfall: '五个全堆上去，像在写作文。',
          action: '随身备一张五感清单，开口前只圈两个。',
        },
        {
          title: '泡面对照实验',
          body: '「没干嘛」vs 咕嘟冒泡、筷子一搅、香辣味、稀溜吃完汤——同一事实，感官密度决定可记性。',
          quote: '「一样的事，多了两个感官，对方脑子一下子就有画面了」[01:18–01:21]',
          pitfall: '示范听完不练，仍用空形容词应付同事。',
          action: '把今天通勤/午饭按两感官改写并录音回放。',
        },
        {
          tone: 'card-red',
          title: '三天闭环',
          body: '小事即可：吃饭、通勤、排队、开会；描述→录音→自听→打卡。闭环比一次灵感重要。',
          quote: '「每天找一件你经历的小事……用五感钩子法描述一遍，录下来自己听一遍」[01:24–01:32]',
          pitfall: '只在评论区打字不录音，听不出自己的干巴处。',
          action: '连续三天语音打卡，格式按口播 C4 + 事件。',
        },
      ],
      boundary: [
        '面向日常口语与出镜叙述，不替代新闻事实核查规范。',
        '「两个感官」是入门剂量，专业稿件可按体裁调整密度。',
        '前三天结构练习是前置，本片默认话已不太乱套。',
      ],
      pitfalls: [
        '用更狠的形容词代替具体细节。',
        '感官堆砌导致像作文、不像说话。',
        '只看示范不录音回放。',
      ],
      conclusion: {
        key: [
          '画面感=可感知细节，不是辞藻升级',
          '五感钩子：每次只嵌两个',
          '小事反复练，比背例句有效',
        ],
        actions: [
          '列出今天三件小事，各改写一版两感官描述',
          '录音回放，删掉所有「很/非常+抽象词」',
          '按 C4 格式打卡三天，强制闭环',
        ],
        shift: '以前：把事情概括成标签（没干嘛、风很大）；现在：用两个感官钩子让对方脑内自动播片。',
      },
    },
    index: {
      summary:
        '干巴对话只剩「哦对」时，用五感钩子法每次嵌两个感官细节，把「风很大」「没干嘛」改成可放映的画面描述。',
      tags: ['表达', '画面感', '五感钩子', '具体化', '口语训练'],
    },
  },
  {
    slug: 'host-express-day3-ai',
    title: '主持人14天建立表达系统3️⃣AI指令带你跟练',
    shortTitle: '三句定乾坤·AI陪练',
    url: 'https://xhslink.cn/o/4KwKxppQWJ',
    durationSec: 156.6,
    primary: 'workplace',
    description:
      '讲话总被问「你到底想表达什么」时，用结果→原因→行动的「三句定乾坤」做结构安检；把固定提示词交给 AI 当陪练，追问逃避与矛盾并重组三句话。',
    lead: '开场痛点：讲话常被问「所以你到底想表达什么／我没听懂」。不是不会说话，是缺一个帮你做结构安检的人。14 天表达系统里，作者以省台十几年主播经历说明：提词器坏、活动突发时，必须边说边过「核心结论是什么—为什么—然后呢」——这叫「三句定乾坤」，靠练不靠天分。普通人没有主持压力，就让 AI 当陪练：设定表达教练身份，只追问三件事，抓逃避模糊矛盾，答完后用结果—原因—行动重组。现场用「三小时无效会」演示，从情绪吐槽被逼到结论、归因到自己、落到可执行行动；强调关键不是 AI 多聪明，而是给自己设了表达安检。',
    takeaway: '结果→原因→行动三句定乾坤；把提示词扔进任意 AI，让它追问并重组——你缺的是安检员，不是口才天赋。',
    structure: [
      ['00:00→00:36', '立题与三句定乾坤', '缺结构安检；结论—为什么—然后呢；AI 可当陪练。'],
      ['00:36→01:02', '提示词演示', '表达教练身份；只追问三事；重组三句话。'],
      ['01:02→02:10', '无效会议跟练', '情绪→结论→自我归因→可执行行动；AI 指出矛盾。'],
      ['02:10→02:37', '安检本质与预告', '关键是表达安检；明日进入具体化阶段。'],
    ],
    chapters: [
      {
        range: '00:00 → 00:36',
        title: '你缺的是结构安检，不是口才',
        paras: [
          '常被追问「你到底想表达什么」「我没听懂」——作者判断：不是不会说话，是缺一个帮你做结构安检的人。14 天建立表达系统，会无偿带跟练。',
          '省台十几年新闻主播经验：直播提词器坏、大型活动突发救场时，必须一边说一边快速过：这段话核心结论是什么、为什么、然后呢。这就是「三句定乾坤」，能力是练出来的。普通人没有主持压力怎么练？让 AI 当你的陪练，提示词放到最后。',
        ],
        figures: [
          {
            file: 'shot-01.jpg',
            time: '00:14',
            alt: '口播持话筒，字幕「经常遇到直播的时候」',
            cap: '情境：直播突发时脑子里仍要过结论—原因—行动',
          },
        ],
      },
      {
        range: '00:36 → 01:02',
        title: 'AI 提示词：表达教练只追问三事',
        paras: [
          '示范指令：请你以表达教练身份，用结果、原因、行动的三句话结构对我训练；核心只追问——你到底想说什么、为什么这么说、然后呢；若回答逃避、模糊或前后矛盾就直接指出；答完后把内容用结果—原因—行动重组给他看；先从「你到底想说什么」开始。',
          '整段可原封不动复制到豆包或任意 AI，关键是角色与追问边界写死。',
        ],
        figures: [
          {
            file: 'shot-02.jpg',
            time: '00:40',
            alt: '展示手机 AI 界面，字幕「以一位表达教练的身份」',
            cap: '设定身份：AI = 表达教练，不是闲聊搭子',
          },
        ],
      },
      {
        range: '01:02 → 02:10',
        title: '跟练：三小时会如何变成三句话',
        paras: [
          '用户版：「今天特别不爽，开了巨长的会，三小时全聊早定过的事，没结论，下周还要开。」AI 指出只说了情绪与过程，逼问核心结果——落到「浪费一上午，原计划工作全没动」。',
          '第二问为什么：承认没提前跟领导确认议程、跑题时没拉回。AI 抓矛盾：前面吐槽会议无意义，现在又认自己没动作——要分清是指责会议无效，还是自己应对不足；选定后者。第三问行动：会前 24 小时发议程确认；跑题超 10 分钟主动喊停回归。最后 AI 重组三句，完成安检。',
        ],
        figures: [
          {
            file: 'shot-03.jpg',
            time: '01:09',
            alt: '对手机说话，字幕「最后什么结论也没有」',
            cap: '原始吐槽：情绪+过程，缺可传递的结论',
          },
          {
            file: 'shot-04.jpg',
            time: '01:44',
            alt: '展示 AI 通话界面，字幕「下次开会前」',
            cap: '落到行动：会前确认议程、跑题超时就拉回',
          },
        ],
      },
      {
        range: '02:10 → 02:37',
        title: '安检本质 + 明日具体化',
        paras: [
          '发生了什么？不是 AI 多聪明，是给自己设置了一个表达安检。从「我觉得」到「结果是」，中间只差一个追问你的人——好好利用 AI。',
          '预告第四天进入重点第二阶段：具体化，让大脑空白或说不出话时，用细节把话说活，让听的人脑子里有画面。提示词卡片可复制到任意 AI。',
        ],
        figures: [
          {
            file: 'shot-05.jpg',
            time: '02:18',
            alt: '屏幕展示完整表达教练提示词卡片',
            cap: '可复制提示词：结果→原因→行动追问 + 矛盾点破 + 三句重组',
          },
        ],
      },
    ],
    svg: {
      tags: ['表达系统', '三句定乾坤', 'AI陪练', '结构安检', '职场沟通'],
      summary:
        '被问「你到底想说什么」时，用结果→原因→行动做结构安检；把固定提示词交给 AI 追问逃避与矛盾并重组三句，缺的是安检员不是口才。',
      timeline: [
        ['00:00', '痛点：你到底想表达什么'],
        ['00:05', '诊断：缺结构安检'],
        ['00:22', '三句定乾坤：结论—为什么—然后呢'],
        ['00:32', '方案：AI 当陪练'],
        ['00:38', '提示词：教练身份+只追三问'],
        ['01:03', '案例：无效会议情绪版'],
        ['01:20', '逼出结果与自我归因'],
        ['01:56', '重组三句完成安检'],
        ['02:12', '本质：安检不是 AI 聪明'],
      ],
      map: ['情绪吐槽', 'AI 三问追打', '结果原因行动', '可复制安检'],
      corrections: [
        'ASR「三具定乾坤」→三句定乾坤；「无常」→无偿；「提词系」→提词器；「志祥」→指责；「表达安全」→表达安检；「说火」→说活。',
        '误解：我不会说话。纠偏：缺的是结构安检闭环。',
        '误解：靠 AI 替我生成漂亮稿。纠偏：AI 职责是追问与重组，话仍是你的。',
        '误解：吐槽外部就等于表达完成。纠偏：要落到自己可执行的行动。',
      ],
      cards: [
        {
          tone: 'card-orange',
          title: '三句定乾坤',
          body: '高压出场同款内核：核心结论是什么、为什么、然后呢。把瞬时空转成可执行结构。',
          quote: '「接下来这段话的核心结论是什么、为什么、然后呢——这就是三句定乾坤」[00:22–00:27]',
          pitfall: '只发泄情绪与过程，没有结论句。',
          action: '任何抱怨先强制写成三句再开口。',
        },
        {
          tone: 'card-green',
          title: 'AI 提示词设计',
          body: '身份=表达教练；只追三问；抓逃避模糊矛盾；答完用结果—原因—行动重组。边界写死，模型才不会跑去安慰或闲聊。',
          quote: '「如果我的回答里有逃避、模糊或者前后矛盾，直接指出来」[00:50–00:54]',
          pitfall: '提示词太软，AI 变成情绪树洞。',
          action: '把片尾卡片原文粘贴进常用 AI，收藏为「表达安检」。',
        },
        {
          title: '案例：无效会议如何过安检',
          body: '从「不爽开会」被逼到结果（浪费上午/工作未动），再分清外部吐槽 vs 自己应对不足，最后给出 24 小时议程与跑题超时干预。',
          quote: '「不是 AI 多聪明，是我给自己设置了一个表达安检」[02:12–02:16]',
          pitfall: '停在指责会议，不认领自己可改的动作。',
          action: '用同一提示词复盘本周一次低效会，产出三句话。',
        },
        {
          tone: 'card-red',
          title: '系统位置：结构之后是具体化',
          body: '本集解决「说清」；预告下一阶段用细节把话说活、让对方有画面——与画面感训练衔接。',
          quote: '「从我觉得到结果是，中间只差一个追问你的人」[02:20–02:22]',
          pitfall: '结构通了就停，表达仍抽象无画面。',
          action: '安检通过后，再给结果句补两个感官细节。',
        },
      ],
      boundary: [
        '示范用通用大模型对话，效果依赖你是否诚实回答追问。',
        '三句结构适合作结论表达与工作同步，不覆盖所有叙事体裁。',
        'AI 指出矛盾不等于事实真相，最终判断仍在你。',
      ],
      pitfalls: [
        '把 AI 当代写，跳过被追问的不适感。',
        '归因永远甩给外部，行动句空洞。',
        '提示词每次即兴改写，丢失「只追三问」约束。',
      ],
      conclusion: {
        key: [
          '表达问题常是缺安检，不是缺嘴皮',
          '结果→原因→行动可练、可迁移',
          'AI 的价值是强制追问与重组',
        ],
        actions: [
          '收藏片中提示词，今日用它复盘一件不爽事',
          '输出必须是三句话，禁止超长情绪铺陈',
          '明日衔接具体化：给结论句加感官细节',
        ],
        shift: '以前：一肚子情绪却说不清；现在：先过三句安检，再决定要不要展开故事。',
      },
    },
    index: {
      summary:
        '被问「你到底想说什么」时，用结果→原因→行动做结构安检；把固定提示词交给 AI 追问矛盾并重组三句，缺的是安检不是口才。',
      tags: ['表达系统', '三句定乾坤', 'AI陪练', '结构安检', '职场沟通'],
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
      title: item.svg.tags.includes('钢琴')
        ? '指尖抓住：强音从「吵」到「立住」'
        : item.slug === 'host-speak-visual-sense'
          ? '五感钩子：两笔细节换画面感'
          : '三句定乾坤：AI 当你的表达安检',
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
