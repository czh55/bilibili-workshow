#!/usr/bin/env node
/** 大厂应届选岗 + 阿里/小米面试专题 · 理性分析 SVG */
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { buildSvg } from '../../svg-auto-height.mjs';
import fs from 'node:fs';

const DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.join(DIR, '..', '..', 'docs', 'dachang-career-interview-playbook-理性分析.svg');

const d = {
  title: '大厂应届选岗与面试打法：阿里 / 小米对照',
  tags: ['校招', '选岗', '阿里', '小米', '面试'],
  duration: '截图专题',
  perspective: '理性分析',
  url: 'personal:dachang-career-interview-playbook',
  summary:
    '三条线合一：用性格特质选赛道（而非岗位虚名）；大厂面试按轮次换剧本——一面验真、二面 Owner、三面格局、四面闻味道；阿里偏客户第一与业务迁移，小米偏务实、人车家与发烧友/厚道。',
  timeline: [
    ['选岗1-2', '三类人 ↔ 岗位；警惕算法/策略产品/数据分析虚名'],
    ['选岗3-5', '研发要长期深耕；运营勿轻视；产品数据项目稳健'],
    ['选岗6-8', '实习底牌；AI/信创/AI运营赛道；简历按 JD 定制'],
    ['阿里1-2', '骨干验货 STAR；主管看 Owner 与业务规划'],
    ['阿里3-4', '总监看格局与价值观；HRG 闻味道'],
    ['小米1-4', '同构四轮 + 人车家 / 发烧友精神 / 厚道'],
    ['反问', '3-6 月优先价值；好 vs 出色；小米「和用户交朋友」'],
  ],
  map: [
    ['认清自己', '三类特质'],
    ['选赛道', '适配优先'],
    ['一面验真', 'STAR 扛追问'],
    ['二三四面', 'Owner→格局→味道'],
  ],
  corrections: [
    '素材为小红书聊天截图整理，非官方校招手册；战略表述（全球化/云/AI、人车家）以求职时官网为准。',
    '「皮实」按原文保留，释义为抗压、韧劲。',
    'HRG（政委）为阿里语境称呼；小米四面为 HR 匹配面。',
    '高红利赛道（AI/信创/AI运营）是截图观点，非投资建议。',
  ],
  cards: [
    {
      tone: '',
      title: '核心命题：适配 > 虚名；每轮换剧本',
      body: '选岗看性格与抗压，不看岗位名气；面试看面试官角色，不看背诵稿。',
      quote: '互联网岗位没有绝对的好坏，只有适配与否',
      relation: '可验证：原文收束句。',
    },
    {
      tone: 'card-orange',
      title: '三类人 → 三类岗',
      body: '技术钻研→研发算法测试；逻辑统筹→产品项目；外向落地→运营市场商务。专业对口次于特质匹配。',
      quote: '性格特质和岗位匹配度，远比专业对口更重要',
      relation: '行动：先自测再投。',
    },
    {
      tone: 'card-green',
      title: '一面：验货 / 扣细节',
      body: '阿里骨干与小米同事都在验经历真实性。STAR、数据、个人贡献、落地案例是共同解。',
      quote: '验货……经不起追问',
      relation: '差异：阿里强调快速解题；小米强调动手解决小问题与务实。',
    },
    {
      tone: 'card-purple',
      title: '二面：Owner / 业务思维',
      body: '主管面挂在执行层。要有「发现问题→推动落地」案例，以及领域基本认知。',
      quote: '缺乏 Owner 意识 / 产品感',
      relation: '硬件补供应链品控；软件补体验与数据驱动。',
    },
    {
      tone: 'card-red',
      title: '三面格局 + 四面味道',
      body: '三面挂在格局与价值观；四面挂在不稳定、不真实、不匹配。反问用来摸紧急需求与卓越标准，勿谈薪假。',
      quote: '终极闻味道 / 找同道中人',
      relation: '阿里：客户第一；小米：极致性价比、发烧友、厚道。',
    },
  ],
  boundary: [
    '个人经验分享整理，不构成录用承诺或薪资预测。',
    '大厂流程因 BG/年份而异，以实际面试安排为准。',
    '「普通本科难碰核心项目」是截图判断，个体差异大。',
  ],
  pitfalls: [
    '一份简历通投技术+产品+运营。',
    '四面用同一套项目故事不换角度。',
    '匹配面问薪资假期。',
    '只追算法岗名却耐不住长期打磨。',
    '轻视运营却又想快速出成果。',
  ],
  conclusion: {
    key: [
      '适配优先：三类人对应三类岗',
      '一面验真、二面 Owner、三面格局、四面味道',
      '反问问紧急价值与卓越差距',
    ],
    actions: [
      '写「适配/不碰」岗位清单各 3 个',
      '每目标岗一份定制简历',
      '1～2 个项目练到扛三层追问',
      '阿里补业务迁移；小米补人车家与文化共鸣',
      '尽早实习验证赛道',
    ],
    shift:
      '以前：追高大上岗名、一套话术打四轮；现在：按特质选赛道，按面试官角色换剧本，用反问确认需求与卓越标准。',
  },
};

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
.tag-blue{background:#dbeafe;color:#1e40af}.tag-green{background:#d1fae5;color:#065f46}
.tag-orange{background:#ffedd5;color:#9a3412}.tag-purple{background:#ede9fe;color:#6b21a8}
.tag-red{background:#fee2e2;color:#991b1b}.tag-gray{background:#f1f5f9;color:#64748b}
.meta{margin:12px 0 20px}
.summary-line{font-size:18px;line-height:1.7;color:#334155;padding:20px 24px;background:#fff;border-radius:12px;border-left:4px solid #3b82f6;margin-bottom:20px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline{background:#fff;border-radius:16px;padding:24px 28px;margin-bottom:24px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.timeline h3{color:#1e40af;margin-bottom:12px}
.timeline-item{display:flex;align-items:baseline;padding:8px 0;border-bottom:1px solid #f1f5f9}
.timeline-time{font-size:14px;font-weight:700;color:#3b82f6;min-width:90px;font-variant-numeric:tabular-nums}
.timeline-text{font-size:15px;color:#475569}
.map{background:#fff;border-radius:20px;padding:36px;margin-bottom:28px;box-shadow:0 4px 24px rgba(0,0,0,.06)}
.map h2{font-size:24px;margin-top:0;border-bottom:none;padding-bottom:0}
.diagram{display:flex;align-items:center;justify-content:center;gap:20px;flex-wrap:wrap;padding:20px 0}
.node{background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #93c5fd;border-radius:16px;padding:20px 28px;text-align:center;min-width:140px;font-weight:700;font-size:16px;color:#1e40af}
.node-green{background:linear-gradient(135deg,#ecfdf5,#d1fae5);border-color:#6ee7b7;color:#065f46}
.node-orange{background:linear-gradient(135deg,#fff7ed,#ffedd5);border-color:#fdba74;color:#9a3412}
.arrow{font-size:24px;color:#94a3b8}
.correction{background:linear-gradient(135deg,#fef3c7,#fef9c3);border-left:4px solid #f59e0b;padding:20px 24px;border-radius:12px;margin-bottom:24px}
.correction h3,.correction p{color:#92400e}
.section{margin-bottom:32px}
.sec-title{font-size:22px;font-weight:700;color:#1e40af;margin-bottom:16px;padding-left:16px;border-left:4px solid #3b82f6}
.card{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 4px 24px rgba(0,0,0,.06);border-left:5px solid #3b82f6}
.card.card-green{border-left-color:#10b981}.card.card-orange{border-left-color:#f59e0b}
.card.card-purple{border-left-color:#8b5cf6}.card.card-red{border-left-color:#ef4444}
.card h3{font-size:20px;font-weight:700;color:#1e40af;margin-bottom:12px}
.card .quote{background:#f8fafc;padding:12px 16px;border-radius:10px;margin:12px 0;font-size:15px;color:#64748b;border-left:4px solid #cbd5e1;font-style:italic}
.card .relation{background:#f0fdf4;padding:10px 14px;border-radius:10px;margin:8px 0;font-size:14px;color:#166534}
.conclusion{background:linear-gradient(135deg,#1e40af,#3b82f6);color:#fff;border-radius:20px;padding:36px;margin-top:32px}
.conclusion h2{font-size:26px;font-weight:800;margin-top:0;margin-bottom:16px;padding-bottom:8px;border-bottom:1px solid rgba(255,255,255,.2);color:#fff}
.conclusion h3{font-size:18px;font-weight:700;color:rgba(255,255,255,.9);margin:20px 0 10px}
.conclusion p,.conclusion li{color:rgba(255,255,255,.9);font-size:15px}
.footer{text-align:center;color:#94a3b8;font-size:13px;padding:32px 0 16px}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none;margin-bottom:24px;display:inline-block}
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
  <div class="timeline"><h3>关键证据时间轴</h3>${timeline}</div>
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

// update index svg_height
const indexPath = path.join(DIR, '..', '..', 'docs', 'index.json');
const index = JSON.parse(fs.readFileSync(indexPath, 'utf8'));
const entry = index.find((e) => e.url === 'personal:dachang-career-interview-playbook');
if (entry) {
  entry.svg_height = height;
  fs.writeFileSync(indexPath, JSON.stringify(index, null, 2) + '\n');
  console.log('updated svg_height', height);
}
