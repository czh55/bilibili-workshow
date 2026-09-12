#!/usr/bin/env node
/** Log 调色与色彩管理 · 讨论整理 · 理性分析 SVG */
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../../svg-auto-height.mjs';
import fs from 'node:fs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', '..', 'docs', 'log-color-grading-notes-理性分析.svg');
const SLUG = 'log-color-grading-notes';

const d = {
  title: 'Log 调色与色彩管理',
  tags: ['个人专栏', 'Log', 'LUT', '色彩管理', '白平衡', 'FCP'],
  duration: '讨论整理',
  perspective: '理性分析',
  url: `personal:${SLUG}`,
  summary:
    '九章把 Log 工作流拧成一条主线：先统一坐标系与基准，再用 LUT 做「罐头变换」，在标准显示空间交付；白平衡动中性轴、饱和调离轴距离，且必须分清 LUT 前/后工位。FCP 里用 Custom LUT 堆栈才能保住这条数学顺序。',
  timeline: [
    ['01 流程', '标准化 → 校正 → 匹配 → 风格化 → 输出适配'],
    ['02 LUT', '颜色变换的罐头：方便可分发，也可原生现做'],
    ['03 官方 LUT', '技术转换带审美；记录保持 Log，监看路径可烘焙'],
    ['04 显示空间', '色域×白点×传递函数×观看环境的行业契约'],
    ['05 高光损失', '709 压缩真实但可逆于母版；LUT 额外代价是精度'],
    ['06 手工/制作', '解眼前这题 vs 总结成对一切输入成立的公式'],
    ['07 中性轴', '白平衡=立轴（LUT 前）；饱和=调距（LUT 后）'],
    ['08 FCP 地图', '五层工具；Camera LUT 钉死最前 vs Custom 可排序'],
    ['09 色轮三轴', '轮盘动方向、滑块动距离、亮度动曝光'],
  ],
  map: [
    ['统一坐标系', 'IDT / 工作空间'],
    ['技术基准', '曝光·白平衡'],
    ['LUT / 渲染', '技术或创意'],
    ['显示契约', 'Rec.709 / HDR'],
  ],
  corrections: [
    'Log 不是单一格式，而是一族曲线+色域；不做输入变换，跨机匹配在错误坐标系里比坐标。',
    '「机内不生成」指的是记录路径保持 Log；监看路径上的 LUT/代理一直在发生。',
    '技术转换 LUT 的高光压缩多半是显示器上限所迫，母版仍在则损失在视图而非资产；真正额外罪过常是精度噪声。',
    '色轮「既能校白又能补饱和」不是矛盾：校白用轮盘（动轴），补饱和用滑块（动距）。',
    'Camera LUT 后做白平衡可行但有天花板：非线性后再全局 offset，阴影/高光易残留色偏。',
  ],
  cards: [
    {
      tone: '',
      title: '主线：数学先于口味',
      body: '标准化与校正处理的是坐标与真实亮度关系；匹配服务感知连续；风格化才是主观表达；输出把意图翻译到目标媒介物理特性。场景差异来自素材一致性、时间预算与交付目标，而不是另发明一套魔法步骤。',
      quote: '流程的标准部分处理数学，差异部分处理生产关系',
      relation: '机制：先统一语言与基准，再谈叙事染色。',
    },
    {
      tone: 'card-orange',
      title: 'LUT：罐头 vs 现做',
      body: 'LUT 是颜色变换的可分发封装。索尼官方 LUT 是「带官方审美的技术转换」。记录保存信息、呈现做出解释——两者越晚绑定，自由度越大；确定永不二次解释时才烘焙。',
      quote: '记录保存信息，呈现做出解释',
      relation: '边界：协作链吃得起「现做」就可用原生管理替代罐头。',
    },
    {
      tone: 'card-green',
      title: '中性轴框架：立轴与调距',
      body: '白平衡把本该中性的推回中性轴，宜在 LUT 前一次增益全段生效；饱和补偿不动物体色相归属，只改离轴距离，针对 LUT 色域压缩副作用，宜在 LUT 后对着示波器补。',
      quote: '动轴的，还是动距离的——意图定操作，示波器裁决',
      relation: '避坑：用降饱和洗色偏，只会得到「错误得比较安静」的灰片。',
    },
    {
      tone: 'card-purple',
      title: 'FCP：工具身份 vs 工位',
      body: '色轮始终是白平衡主力工具；理想工位在技术 LUT 之前。Camera LUT 钉死最前换便利；需要严格前后分工时，用 Custom LUT + 双份 Color Adjustments 搭堆栈（#1 立轴曝光，#2 饱和与口味）。',
      quote: '工具（what）与工位（where）正交',
      relation: '行动：检查器里把校正拖到 Custom LUT 上方。',
    },
    {
      tone: 'card-red',
      title: '色轮是三轴控制器',
      body: '轮盘=带方向的色向量（白平衡/染色）；饱和滑块=无方向径向缩放；亮度滑块=曝光。同一控件两次实例化可各取一根轴，不可拿错轴互顶。',
      quote: '白平衡用轮盘，饱和补偿用滑块',
      relation: '向量图检验：滑块径向呼吸、中心钉死；轮盘整体位移。',
    },
  ],
  boundary: [
    '讨论以 Log→Rec.709 SDR 与 FCP 统一调色面板为主；ACES/达芬奇节点细节未展开成手册。',
    '官方 LUT 审美因厂牌而异，不能当作唯一「正确」渲染。',
    '混合色温、大面积单色场景，自动白平衡常采错锚点，需遮罩分区。',
    'HDR/PQ 交付需另一套亮度映射，不可直接套用 SDR 口味结论。',
  ],
  pitfalls: [
    '跳过输入变换直接套创意 LUT，跨机颜色无法对话。',
    '在 Camera LUT 后狂拧全局 offset「修白」，阴影高光残留相反色偏。',
    '用饱和滑块当白平衡，或用轮盘当全局饱和补偿。',
    '把监看烘焙误当成记录烘焙，丢掉二次解释空间。',
    '手工只对眼前一镜取巧，导出成通用 LUT 后在其他镜头崩坏。',
  ],
  conclusion: {
    key: [
      '顺序：统一坐标系 → 立曝光与中性轴 →（可选）技术 LUT → 饱和/口味 → 输出契约',
      '几何：白平衡动轴，饱和动距，曝光动亮度分布',
      'FCP：要严格顺序就用 Custom LUT 堆栈，不要默认 Camera LUT 钉死',
    ],
    actions: [
      '为常用机内 Log 建「Custom LUT 前校正」效果堆栈模板',
      '白平衡时强制开 RGB Parade；补饱和时看 Vectorscope / Luma vs Sat',
      '交付前确认目标显示空间四要素（色域/白点/曲线/观看环境）',
      '母版保留 Log；只对确定不再重释的版本烘焙',
      '新场景先问：素材一致性、时间预算、交付目标——再裁剪 pipeline',
    ],
    shift:
      '以前：把 LUT 和色轮当成滤镜旋钮乱拧；现在：先问自己在动哪根几何轴、工位在变换前还是后，用示波器而不是感觉结案。',
  },
};

const CSS = `*{margin:0;padding:0;box-sizing:border-box}
body{font-family:"PingFang SC","Microsoft YaHei",sans-serif;background:linear-gradient(135deg,#f8fafc,#e2e8f0);padding:48px 60px;color:#1e293b}
.container{max-width:1200px;margin:0 auto}
h1{font-size:36px;font-weight:900;background:linear-gradient(135deg,#a4622d,#356e68);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:8px}
h2{font-size:26px;font-weight:700;color:#7c4920;margin:32px 0 16px;padding-bottom:8px;border-bottom:2px solid #e2e8f0}
h3{font-size:20px;font-weight:700;color:#334155;margin-bottom:12px}
p{font-size:16px;line-height:1.8;color:#475569;margin-bottom:10px}
ul,ol{padding-left:24px;margin:8px 0}
li{font-size:15px;line-height:1.8;color:#475569;margin-bottom:6px}
.tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600;margin-right:8px}
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #a4622d;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline h3{color:#7c4920;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#a4622d;min-width:110px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#fbf6ec,#f6e9db);border:2px solid #e0c6a8;border-radius:16px;padding:20px 28px;text-align:center;min-width:140px;font-weight:700;font-size:16px;color:#7c4920}
.node-green{background:linear-gradient(135deg,#edf2ee,#d1e7e0);border-color:#9fc0b8;color:#26524d}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3,.correction p{color:#92400e}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#7c4920;margin-bottom:16px;padding-left:16px;border-left:4px solid #a4622d}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #a4622d}
.card.card-green{border-left-color:#356e68}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#7c4920;margin-bottom:12px}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#edf2ee;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#26524d}
.conclusion{background:linear-gradient(135deg,#7c4920,#356e68);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#a4622d;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
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
  <div class="footer">双轨产物之二 · 理性分析 · 证据来自讨论整理全文</div>
</div>`;
}

const { svg, height } = await buildSvg({ css: CSS, body: buildBody(d), width: 1320 });
fs.writeFileSync(OUT, svg, 'utf8');
console.log('Generated', OUT, 'height', height);

const indexPath = path.join(DIR, '..', '..', 'docs', 'index.json');
const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
const url = `personal:${SLUG}`;
let entry = index.find((e) => e.url === url);
const today = new Date().toISOString().slice(0, 10);
if (!entry) {
  entry = {
    date: today,
    title: 'Log 调色与色彩管理',
    summary:
      '九章讨论整理：Log 流程五步、LUT 原理与官方转换、标准显示空间、高光损失、手工还原与制作、白平衡/饱和中性轴框架，以及 FCP 工具地图与色轮三轴。',
    tags: ['个人专栏', 'Log', 'LUT', '色彩管理', '白平衡', '饱和度', 'Final Cut Pro', '调色'],
    platform: 'personal',
    url,
    duration: '讨论整理',
    outputs: {
      html: `${SLUG}-图文实录.html`,
      svg: `${SLUG}-理性分析.svg`,
    },
    screenshot_count: 0,
    transcript_segments: 9,
    svg_height: height,
  };
  index.push(entry);
} else {
  entry.svg_height = height;
  entry.outputs = entry.outputs || {};
  entry.outputs.html = `${SLUG}-图文实录.html`;
  entry.outputs.svg = `${SLUG}-理性分析.svg`;
}
fs.writeFileSync(indexPath, JSON.stringify(index, null, 2) + '\n');
console.log('index updated, svg_height', height);
