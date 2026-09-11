#!/usr/bin/env node
/** 留晞印象派专题 · 理性分析 SVG：明度五律 / 九调 / 鲁昂时辰 / 看见四层 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../../svg-auto-height.mjs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', '..', 'docs', 'liuxi-monet-value-seeing-理性分析.svg');

const d = {
  title: '留晞看印象派：明度、九调与「看见」',
  tags: ['莫奈', '明度', '九调', '倒影', '鲁昂教堂', '观看'],
  duration: '截图专题',
  perspective: '理性分析',
  url: 'personal:liuxi-monet-value-seeing',
  summary:
    '同一认知链四段：倒影里重组明度关系（五律）→ 九调坐标（亮度×对比）→ 鲁昂教堂验证时辰同时改气氛/跨度/色相 → 进步=新的分层看见。核心不是复制倒置世界或建筑，而是光线进入画面后视觉关系被重新组织。',
  timeline: [
    ['倒影1-2', '不是镜像翻转；亮部进水被压低'],
    ['倒影3-4', '暗部可更深；真正压缩的是明度跨度'],
    ['倒影5', '保留结构关系；越远越松'],
    ['九调', '亮度管整体 / 对比管层次；横收窄、纵平移'],
    ['教堂①②', '明度先升后降；对比跟光线是否明确'],
    ['教堂③+特例', '冷→暖轨迹；阴天低长调=暗≠平'],
    ['看见', '观察→理解→感知→审美'],
  ],
  map: [
    ['调灰', '剥色相'],
    ['明度结构', '五律'],
    ['九调坐标', '定位'],
    ['时辰验证', '三变量'],
    ['分层看见', '内化'],
  ],
  corrections: [
    '素材为小红书图文截图整理，非艺术史论文；九调归类原文注明含主观性。',
    '鲁昂样本「近 30 幅」为作者统计口径；阴天低长调样本少，作待验证点。',
    '「水·三部曲」前两篇（颜色、笔触）不在本文件夹，仅第三篇明度收录完整。',
    'IMG_6026/6027 缺失；「隔两年再临摹」仅余一页原则卡。',
  ],
  cards: [
    {
      tone: '',
      title: '核心命题：重组关系，不复制数值',
      body: '倒影与时辰变化，本质都是进入画面后的视觉系统被重新组织：明度气氛、明暗跨度、冷暖轨迹一起动。',
      quote: '不是复制一个倒过来的世界，而是重新组织水面上的视觉关系',
      relation: '可验证：先问「明度结构还在吗」，再找颜色。',
    },
    {
      tone: 'card-orange',
      title: '倒影五律（压缩但不抹平结构）',
      body: '亮部压低；暗部不必抬；跨度收窄；关系保留；距离再削弱。反例（暗倒影可比本体更深）本身有教学价值。',
      quote: '水面不是一面完美的镜子',
      relation: '与笔触同构：保留结构、打破轮廓 / 保留关系、压缩跨度。',
    },
    {
      tone: 'card-green',
      title: '九调：两个旋钮',
      body: '高中低 = 整体能量；长中短 = 层次密度。横向：两端靠近、亮度位置不变；纵向：区间平移、对比宽度不变。',
      quote: '亮度管整体，对比管层次',
      relation: '画不出层次时先诊断：亮度错了，还是对比没拉开？',
    },
    {
      tone: 'card-purple',
      title: '鲁昂：时辰 = 三变量同动',
      body: '明度：中→高→中/低；对比：柔光收中间、明确光拉开；色相：蓝紫→金黄→粉橙暖棕。橙红仅日落出现。',
      quote: '真正改变的不是建筑本身',
      relation: '特例：低长调证明「暗≠平」，可留强光锚点。',
    },
    {
      tone: 'card-red',
      title: '看见四层',
      body: '观察看信息 → 理解看关系 → 感知进画面 → 审美见自己。手可练；看见需要时间。',
      quote: '同一个世界，我开始看见更多层次',
      relation: '印象派三原则对照：画关系/画光线/笔触是语言。',
    },
  ],
  boundary: [
    '个人临摹与观察笔记整理，不构成唯一正确的艺术史结论。',
    '灰度分析会损失色相信息，需与色彩发现交叉阅读。',
    '九调命名（高长调等）沿用色彩构成习惯用语。',
  ],
  pitfalls: [
    '倒影当完美镜像、亮暗对称翻转。',
    '以为压亮就必须抬暗，忽略可更深的暗倒影。',
    '只改颜色「越画越红」却不动明度与对比。',
    '把「暗」画成「平」，抹掉视觉锚点。',
    '只练手势、不升级观察模型。',
  ],
  conclusion: {
    key: [
      '倒影：压缩跨度、保留结构',
      '九调：亮度×对比两个旋钮',
      '时辰：明度气氛 + 对比清晰度 + 冷暖轨迹',
      '进步：分层看见，而非更多动作',
    ],
    actions: [
      '临摹前先把参考图调灰，标出暗/亮/灰层级',
      '用九宫给自己画面定位：整体能量与层次密度',
      '画远处：降纯度与对比、弱化边缘（空气感）',
      '画倒影：先检查明度结构是否还在',
      '同一题材隔一段时间再画，对照「看见」是否多了一层',
    ],
    shift:
      '以前：对颜色、翻倒影、练笔触；现在：先调灰看结构，用九调定位气氛与层次，再让看见从命名物体走到关系、感受与审美。',
  },
};

const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f0fdfa,#ecfeff);padding:48px 60px;color:#134e4a}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#0f766e,#14b8a6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#0f766e;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #ccfbf1}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul,ol{padding-left:24px;margin:8px 0}
li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#ccfbf1;color:#115e59}.tag-green{background:#d1fae5;color:#065f46}
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
.diagram{display:flex;align-items:center;justify-content:center;gap:16px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#f0fdfa,#ccfbf1);border:2px solid #5eead4;border-radius:16px;padding:18px 22px;text-align:center;min-width:120px;font-weight:700;font-size:15px;color:#0f766e}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:22px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3,.correction p{color:#92400e}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#0f766e;margin-bottom:16px;padding-left:16px;border-left:4px solid #14b8a6}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #14b8a6}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#0f766e;margin-bottom:12px}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdfa;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#115e59}
.conclusion{background:linear-gradient(135deg,#0f766e,#14b8a6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#0d9488;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f0fdfa,#ecfeff);padding:48px 60px;color:#134e4a}`;

function esc(s) {
  return String(s ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function buildBody(d) {
  const tags = (d.tags || [])
    .map((t, i) => `<span class="tag ${['tag-blue', 'tag-green', 'tag-orange', 'tag-purple', 'tag-red'][i % 5]}">${esc(t)}</span>`)
    .join('');
  const timeline = (d.timeline || [])
    .map(([t, x]) => `<div class="timeline-item"><span class="timeline-time">${esc(t)}</span><span class="timeline-text">${esc(x)}</span></div>`)
    .join('');
  const mapNodes = (d.map || [])
    .map(([label], i) => {
      const cls = ['node', 'node-green', 'node-orange', 'node', 'node-green'][i % 5];
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
  const keys = (d.conclusion?.key || []).map((k) => `<li>${esc(k)}</li>`).join('');
  const actions = (d.conclusion?.actions || []).map((a) => `<li>${esc(a)}</li>`).join('');

  return `<div class="root-wrap"><div class="container">
<h1>${esc(d.title)}</h1>
<div class="meta">${tags}<span class="tag tag-gray">${esc(d.duration)}</span><span class="tag tag-gray">${esc(d.perspective)}</span></div>
<a class="source-link" href="../${esc(d.url.replace('personal:', ''))}-图文实录.html">← 图文实录</a>
<div class="summary-line">${esc(d.summary)}</div>
<div class="timeline"><h3>阅读路径</h3>${timeline}</div>
<div class="map"><h2>认知链路</h2><div class="diagram">${mapNodes}</div></div>
<div class="correction"><h3>校正与边界</h3>${corrections}</div>
<div class="section"><div class="sec-title">结构化卡片</div>${cards}</div>
<div class="section"><div class="sec-title">适用边界</div><ul>${boundary}</ul></div>
<div class="section"><div class="sec-title">常见坑</div><ul>${pitfalls}</ul></div>
<div class="conclusion"><h2>行动结论</h2>
<h3>记住</h3><ul>${keys}</ul>
<h3>去做</h3><ul>${actions}</ul>
<h3>行为转变</h3><p>${esc(d.conclusion?.shift || '')}</p>
</div>
<div class="footer">personal · ${esc(d.url)} · 理性分析</div>
</div></div>`;
}

const { svg, height } = await buildSvg({ css: CSS, body: buildBody(d), width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated', OUT, 'height', height);
