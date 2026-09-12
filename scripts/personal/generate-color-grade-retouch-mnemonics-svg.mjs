#!/usr/bin/env node
/** 调色20 + 修图20 口诀专题 · 理性分析 SVG */
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../../svg-auto-height.mjs';
import fs from 'node:fs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', '..', 'docs', 'color-grade-retouch-mnemonics-理性分析.svg');

const d = {
  title: '调色与修图双二十口诀',
  tags: ['调色', '修图', 'HSL', '人像', '风格化', '口诀'],
  duration: '截图专题',
  perspective: '理性分析',
  url: 'personal:color-grade-retouch-mnemonics',
  summary:
    '两套口诀分工：修图管「底座与排障」，调色管「叙事与风格」。共同刹车是人物优先、光影先于颜色、肤色找橙、背景让路；风格 RGB/百分比是起点，不是一键真理。',
  timeline: [
    ['调色·光影', '透气藏戏 / 亮柔暗实 / 光来色染 / 逆光藏补色 / 轮廓与情绪'],
    ['调色·情绪', '冷唇暖肤 / 背景压暗 / 同色切断杂色 / 色温情绪 / 撞色不撞明'],
    ['调色·细节', '橙黄肤色 / 冷眼神光 / 发色降艳 / 服装背景让路 / 磨皮加纹理'],
    ['调色·风格', '胶片青橙 / 日系 / 赛博品青 / 港风 / 法式灰粉'],
    ['调色·心法', '先光后色 / 脏查明度 / 暗部青灰 / 高光蓝品 / 人为主'],
    ['修图·基础', '先校后调 / 救高光提阴影 / 肤色公式 / 虚化背景 / S曲线'],
    ['修图·人像', '磨皮不磨骨 / 眼神 / 发丝径向 / 唇色 / 颈肩阴影'],
    ['修图·排障', '逆光脸 / 天空过曝 / 衣服抢眼 / 皮肤偏红 / 夜景噪点'],
    ['修图·心法', '先修心 / 少滑块 / 肤色找橙 / 背景让人 / 100%查细节'],
  ],
  map: [
    ['修图底座', '校色曝光'],
    ['人像精修', '骨皮眼神'],
    ['调色叙事', '光影情绪'],
    ['风格配方', '可微调'],
  ],
  corrections: [
    '标题「20口诀」下各类实际各列 5 条，两套合计约 55 条可执行句；按截图全文收录，不删减。',
    '修图系列原标 7 页，素材仅至 6/7，缺第 7 页。',
    '赛博/法式等 RGB 与 ±15/±20 为口诀起点，需按素材与软件色段微调。',
    '「先校色后调色」与「调色先调光」不冲突：校色=还原；调光=再叙事。',
  ],
  cards: [
    {
      tone: '',
      title: '核心命题：底座 → 叙事 → 风格',
      body: '先把曝光白平衡和人像可信度修好，再谈情绪色温与风格配方。跳过底座直接套 LUT/风格，最容易脏、假、抢戏。',
      quote: '先校色，后调色 / 调色先调光，无光不成色',
      relation: '两套口诀开篇同向，可当作强制顺序。',
    },
    {
      tone: 'card-orange',
      title: '人物优先的三条硬规则',
      body: '① 人为主、色彩为仆；② 背景永远让路（压暗/降饱和/虚化）；③ 肤色问题先查 HSL 橙色（修图称控制约 80%）。',
      quote: '人物为主，色彩为仆 / 背景服务于人 / 肤色不对，先找橙色',
      relation: '诊断顺序：人 → 背景 → 风格色。',
    },
    {
      tone: 'card-green',
      title: '光影比颜色更早',
      body: '高光透气、阴影藏戏；受光暖、背光冷；逆光控补色饱和。修图侧用径向/渐变/明暗分离落实同一逻辑。',
      quote: '光从哪来，色往哪染 / 侧光加暖，背光补冷',
      relation: '机制：染色服从光源方向，避免「满屏乱染」。',
    },
    {
      tone: 'card-purple',
      title: '风格配方是菜单不是圣旨',
      body: '胶片青橙、日系低对比、赛博品青、港风红黄、法式灰粉——记下比例后必须回看肤色与直方图。修图篇的五风格是短版速记。',
      quote: '胶片不胶，青橙配比 / 赛博朋克，品青二分',
      relation: '行动：每种风格保存「个人微调版」预设。',
    },
    {
      tone: 'card-red',
      title: '操作纪律：少动、多看、放大查',
      body: '每次调整停 3 秒看全局；磨皮后回 10% 纹理防塑料；100% 查皮肤发丝边缘。脏色先查明度统一，再提纯度。',
      quote: '少动滑块，多观察 / 瑕疵隐形，纹理救命 / 细节是魔鬼',
      relation: '避坑：连拉十个滑块再看整体。',
    },
  ],
  boundary: [
    '口诀来自社交图文笔记整理，非某一软件官方手册。',
    '人像审美因文化与客户要求而异；「高级感」非唯一目标。',
    '夜景降噪与阴影提亮存在画质权衡，需按输出尺寸取舍。',
    '缺修图第 7 页，若原文有收束页未纳入。',
  ],
  pitfalls: [
    '未校色就套赛博/港风，肤色发灰发品。',
    '磨皮磨掉骨相轮廓，五官发糊。',
    '撞色同时撞明度，画面刺眼。',
    '发色/衣服饱和过高抢脸。',
    '阴影狂提超 +50 再强降噪，夜景发糊。',
  ],
  conclusion: {
    key: [
      '顺序：校色曝光 → 人像可信 → 光影叙事 → 风格配方',
      '刹车：人物优先、肤色找橙、背景让路、少滑块多观察',
      '风格参数当起点，按直方图与肤色回修',
    ],
    actions: [
      '打印/收藏两套目录，按任务勾选（排障 vs 风格）',
      '为人像建「橙色肤色」默认起步：明度↑饱和↓微偏色相',
      '每风格各存一版个人预设并标注适用光比',
      '成片前强制 100% 检查皮肤发丝边缘',
      '逆光片固定流程：径向提脸 + 色温微暖 + 控暗部补色',
    ],
    shift:
      '以前：看到好看成片就乱堆滑块和滤镜；现在：先修底座再讲故事，用口诀当检查清单，风格只做最后一层。',
  },
};

const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#6d28d9,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#6d28d9;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul,ol{padding-left:24px;margin:8px 0}
li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #7c3aed;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline h3{color:#6d28d9;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#7c3aed;min-width:100px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#f5f3ff,#ede9fe);border:2px solid #c4b5fd;border-radius:16px;padding:20px 28px;text-align:center;min-width:140px;font-weight:700;font-size:16px;color:#6d28d9}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3,.correction p{color:#92400e}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#6d28d9;margin-bottom:16px;padding-left:16px;border-left:4px solid #7c3aed}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #7c3aed}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#6d28d9;margin-bottom:12px}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#166534}
.conclusion{background:linear-gradient(135deg,#6d28d9,#7c3aed);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#7c3aed;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
.root-wrap{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}`;

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
  <a class="source-link" href="#">${esc(d.url)}</a>
  <div class="summary-line">${esc(d.summary)}</div>
  <div class="timeline"><h3>结构时间轴</h3>${timeline}</div>
  <div class="map"><h2>核心脉络</h2><div class="diagram">${mapNodes}</div></div>
  <div class="correction"><h3>常见误解与认知纠偏</h3>${corrections}</div>
  <div class="section"><h2 class="sec-title">观点拆解</h2>${cards}</div>
  <div class="section"><h2 class="sec-title">方法边界与避坑</h2><div class="card card-red"><h3>适用边界</h3><ul>${boundary}</ul><h3>避坑</h3><ul>${pitfalls}</ul></div></div>
  <div class="conclusion"><h2>总结与行动</h2><h3>核心要点</h3><ul>${keyHtml}</ul><h3>行动清单</h3><ol>${actionsHtml}</ol><h3>关键认知转变</h3><p>${esc(shift)}</p></div>
  <div class="footer">双轨产物之二 · 理性分析 · 证据来自截图全文整理</div>
</div>`;
}

const { svg, height } = await buildSvg({ css: CSS, body: buildBody(d), width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated', OUT, 'height', height);

const indexPath = path.join(DIR, '..', '..', 'docs', 'index.json');
const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
let entry = index.find((e) => e.url === 'personal:color-grade-retouch-mnemonics');
if (!entry) {
  entry = JSON.parse(fs.readFileSync(path.join(DIR, '_tmp_mnemonics_index.json'), 'utf8'));
  index.push(entry);
}
entry.svg_height = height;
fs.writeFileSync(indexPath, JSON.stringify(index, null, 2) + '\n');
console.log('index updated, svg_height', height);
