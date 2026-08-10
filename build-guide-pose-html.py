#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从转录文本生成 guide-pose-model 完整版图文实录 HTML。"""
import re, html

TRANS = "/Users/chenzhiheng/Projects/bilibili-workshop/_work/gpm-transcript.txt"
OUT = "/Users/chenzhiheng/Projects/bilibili-workshop/docs/guide-pose-model-图文实录.html"

CSS = """*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;font-family:"PingFang SC","Microsoft YaHei",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}
a{color:#9a3412;text-underline-offset:3px}
.container{width:min(1000px,100%);margin:0 auto;padding:48px 32px 80px}
header{margin-bottom:40px}
header h1{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}
.meta-row{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.meta-tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}
.tag-platform{background:#ff2442;color:#fff}
.tag-duration{background:#f1f5f9;color:#64748b}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none}
h2{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
h3{font-size:20px;font-weight:700;color:#1c1917;margin:28px 0 14px}
h4{font-size:17px;font-weight:700;color:#44403c;margin:22px 0 10px}
p{margin:0 0 14px;color:#44403c}
ul{margin:0 0 14px;padding-left:22px;color:#44403c}
li{margin-bottom:6px}
strong{color:#1c1917}
.time-marker{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}
img{display:block;max-width:100%;height:auto}
figure{margin:24px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}
figcaption{padding:12px 18px;color:#57534e;font-size:14px}
figcaption .time-badge{font-weight:700;color:#b45309;margin-right:6px}
.story-section{margin:48px 0;padding:28px 28px 8px;background:#fff;border-radius:20px;box-shadow:0 4px 24px rgba(41,37,36,.06)}
.story-section>h3{margin-top:0;font-size:23px;color:#9a3412;display:flex;align-items:center;gap:12px}
.story-section>h3 .sec-num{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;border-radius:12px;background:#9a3412;color:#fff;font-size:18px;flex-shrink:0}
.tip-box{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:14px 18px;margin:16px 0}
.tip-box strong{color:#1e40af}
.tip-box p{color:#1d4ed8;margin:4px 0 0}
.warn-box{background:#fef2f2;border-left:4px solid #ef4444;border-radius:12px;padding:14px 18px;margin:16px 0}
.warn-box strong{color:#b91c1c}
.warn-box p{color:#dc2626;margin:4px 0 0}
.formula-box{background:#fefce8;border-left:4px solid #ca8a04;border-radius:12px;padding:14px 18px;margin:16px 0}
.formula-box strong{color:#a16207}
.formula-box p{color:#a16207;margin:4px 0 0}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:16px 0}
.two-col figure{margin:0}
.summary-row{display:flex;gap:12px;padding:16px 20px;background:#fff;border-radius:12px;margin-bottom:12px;box-shadow:0 2px 12px rgba(0,0,0,.04);align-items:flex-start}
.summary-row .time-marker{flex-shrink:0;margin-top:2px}
.summary-row strong{display:block;font-size:16px;color:#1c1917;margin-bottom:4px}
.summary-row p{color:#57534e;margin:0;font-size:15px}
.takeaway-box{background:#eff6ff;border-left:4px solid #3b82f6;border-radius:12px;padding:16px 20px;margin-top:20px}
.takeaway-box strong{display:block;font-size:16px;color:#1e40af;margin-bottom:6px}
.takeaway-box p{color:#3b82f6;margin:0;font-size:15px}
.toc{background:#fff;border-radius:16px;padding:20px 24px;box-shadow:0 4px 20px rgba(41,37,36,.06);margin-bottom:40px}
.toc h3{margin-top:0}
.toc a{display:block;padding:6px 0;text-decoration:none;color:#57534e;font-size:15px;border-bottom:1px dashed #e7e5e4}
.toc a:hover{color:#9a3412}
@media(max-width:640px){.container{padding:28px 18px 56px}header h1{font-size:24px}.two-col{grid-template-columns:1fr}.story-section{padding:20px 16px 4px}.transcript-row{grid-template-columns:56px 1fr;gap:10px}}
.transcript-section{margin-top:48px}
.transcript-note{font-size:14px;color:#78716c;margin-bottom:24px}
.transcript-list{list-style:none;padding:0}
.transcript-row{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}
.transcript-row time{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}
.transcript-row p{margin:0}
.transcript-collapsible{border:none;margin:0;padding:0}.transcript-collapsible summary{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{display:none}.transcript-collapsible summary::before{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}.transcript-collapsible[open] summary::before{transform:rotate(90deg)}.transcript-collapsible[open] summary{margin-bottom:16px}.transcript-collapsible .transcript-body{margin-top:0}"""

# ---- 读取转录 ----
rows = []
with open(TRANS, encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        m = re.match(r"\[(\d{2}:\d{2})\]\s*(.*)", line)
        if m:
            rows.append((m.group(1), html.escape(m.group(2))))

transcript_items = "\n".join(
    f'<li class="transcript-row"><time>{t}</time><p>{txt}</p></li>' for t, txt in rows
)

# ---- 构建正文 ----
parts = []
parts.append('<!DOCTYPE html>')
parts.append('<html lang="zh-CN">')
parts.append('<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">')
parts.append('<meta name="description" content="43 分钟人像美姿系统课完整图文实录：站姿（自下而上原则、画圈圈六点位脚法、固定手/功能手、双手美姿）、坐姿（135°与漏半鞋）、蹲姿（平行蹲/后方重心腿蹲/前方腿重心蹲）、靠姿（只靠一个部位）、道具应用（不要急慢慢来）。每个模特的动作和关键要领全收录。">')
parts.append(f'<title>如何引导摆姿摆姿呢？一个视频教会你。｜完整图文实录</title>')
parts.append(f'<style>{CSS}</style>')
parts.append('</head><body><main class="container">')

# Header
parts.append('''<header><h1>如何引导摆姿摆姿呢？一个视频教会你。</h1>
<div class="meta-row"><span class="meta-tag tag-platform">小红书</span>
<span class="meta-tag tag-duration">43分钟</span></div>
<a class="source-link" href="http://xhslink.cn/o/4J6bjUXtIsl" target="_blank" rel="noopener">原视频链接</a>
<a class="source-link" href="guide-pose-model-场景英译.html" hreflang="en">English Version</a></header>''')

# TOC
parts.append('''<nav class="toc"><h3>目录</h3>
<a href="#sec1">一、站姿篇：一个原则 + 三个关键点</a>
<a href="#sec2">二、坐姿篇：两个「确定」</a>
<a href="#sec3">三、蹲姿篇：三种蹲法 + 通用手法</a>
<a href="#sec4">四、靠姿篇：只允许一个部位靠</a>
<a href="#sec5">五、道具篇：不要急，慢慢来</a>
<a href="#transcript">六、完整文字转录</a></nav>''')

# 内容要点
parts.append('<article><h2>内容要点</h2>')
parts.append('<p>一支 43 分钟的人像美姿深度教学。吴老师把「引导模特摆姿」拆成一套可复制的底层逻辑：<strong>站姿</strong>（自下而上的原则、画圈圈六点位脚法、固定手/功能手、双手美姿）、<strong>坐姿</strong>（135° 脚角 + 前后脚错开漏半鞋）、<strong>蹲姿</strong>（避免正面蹲、平行蹲/后方重心腿蹲/前方腿重心蹲三种蹲法）、<strong>靠姿</strong>（只允许一个部位靠：手/肩/臀/脚）、<strong>道具</strong>（不要急慢慢来，墨镜背包由下往上）。</p>')
parts.append('<p>贯穿全片的一句话：<strong>「美姿小变化，机位构图大变化」</strong>——模特只要做细微调整，摄影师通过横竖构图、高低机位、正侧面和远近景别把画面做丰富。</p>')

parts.append('<div class="summary-row"><span class="time-marker">[00:00→02:00]</span><div><strong>站姿总原则</strong><p>引导从脚开始：自下而上，先站好站稳再做手部头部动作；站姿拆成脚、手、头三个关键部分。</p></div></div>')
parts.append('<div class="summary-row"><span class="time-marker">[02:03→06:52]</span><div><strong>脚法：画圈圈原则</strong><p>确定一个重心脚，另一只脚围绕它画圈圈，六个点位形成六种经典脚法。</p></div></div>')
parts.append('<div class="summary-row"><span class="time-marker">[06:56→14:05]</span><div><strong>单手美姿</strong><p>固定手（135° 垂放不动）+ 功能手（自上而下各种抓），配合机位构图大变化。</p></div></div>')
parts.append('<div class="summary-row"><span class="time-marker">[14:07→17:46]</span><div><strong>双手美姿</strong><p>双手抱胸八字起式、双手插腰错开高低手，再演化为固定手/功能手的变化。</p></div></div>')
parts.append('<div class="summary-row"><span class="time-marker">[17:52→24:33]</span><div><strong>坐姿</strong><p>两个确定：脚 135°（太直太弯都显腿短腿粗）+ 前后脚错开、后方脚漏半鞋（前方脚伸长线条流畅）。</p></div></div>')
parts.append('<div class="summary-row"><span class="time-marker">[24:36→32:53]</span><div><strong>蹲姿</strong><p>避免正面蹲，45° 侧方位；三种蹲法：平行蹲、后方重心腿蹲、前方腿重心蹲；手法通用 + 看天看地看镜头。</p></div></div>')
parts.append('<div class="summary-row"><span class="time-marker">[33:01→38:02]</span><div><strong>靠姿</strong><p>核心：只允许身体一个部位靠（手/肩/臀/脚），人跟靠的物体远一点点。</p></div></div>')
parts.append('<div class="summary-row"><span class="time-marker">[38:06→42:26]</span><div><strong>道具</strong><p>不要急慢慢来：墨镜垂下→腹部→锁骨→嘴→眼睛→头顶；背包同理，配合角度构图变化。</p></div></div>')
parts.append('<div class="takeaway-box"><strong>总结</strong><p>美姿引导的底层逻辑：① 自下而上，先站稳；② 确定重心脚，另一脚画圈圈；③ 固定手不动、功能手各种抓；④ 美姿小变化、机位构图大变化；⑤ 坐姿定 135°、靠姿只靠一个部位、道具慢慢来。</p></div>')

# ============ 章节 1 站姿 ============
parts.append('''<section class="story-section" id="sec1"><span class="time-marker">00:16 - 17:46</span><h3><span class="sec-num">一</span>站姿篇</h3>
<p>站姿的引导，吴老师先给出一套总纲：<strong>一个原则 + 三个关键点</strong>。记下来，这就是拍好站姿的关键。</p>

<h4>一个原则：自下而上</h4>
<p>很多同学模仿网图直接让模特「插一下腰、扭一下胯、头倒一下、屁股提一点」，最后才提脚——结果模特站不稳，还会被怪「不会摆 pose」。</p>
<div class="formula-box"><strong>正确顺序</strong><p>先让模特站好站稳（脚），再做手部动作，最后做头部动作。跳跃性、奔跑性的除外。</p></div>
<p>站姿因此拆成三个关键部分，分开练习就能轻松掌握：<strong>① 脚部调整（脚法）　② 手部调整（手法）　③ 头部</strong>。</p>''')

parts.append('''<h4>脚法：十秒钟六个经典脚法（画圈圈原则）</h4>
<p>模特不会摆 pose 时，不要否定她，而是告诉她：<strong>确定一个重心脚，另一只脚围绕重心脚「画圈圈」</strong>。只要在画圈圈的时候注意六个点位，就能得到六种经典脚法。</p>
<figure><img src="assets/guide-pose-model/pose-foot-circle.jpg" alt="画圈圈脚法原则" loading="lazy"><figcaption><span class="time-badge">[02:25]</span>[02:25] 画圈圈原则：一只脚站稳，另一只脚画圈圈</figcaption></figure>
<table style="width:100%;border-collapse:collapse;margin:16px 0 4px;font-size:14px"><thead><tr><th style="text-align:left;padding:8px 10px;background:#f5f5f4;border:1px solid #e7e5e4">点位</th><th style="text-align:left;padding:8px 10px;background:#f5f5f4;border:1px solid #e7e5e4">动作</th><th style="text-align:left;padding:8px 10px;background:#f5f5f4;border:1px solid #e7e5e4">气质关键词</th></tr></thead><tbody>
<tr><td style="padding:8px 10px;border:1px solid #e7e5e4;font-weight:700">点位一</td><td style="padding:8px 10px;border:1px solid #e7e5e4">右脚放正前方一点点，脚尖稍微斜一点</td><td style="padding:8px 10px;border:1px solid #e7e5e4">经典脚法一</td></tr>
<tr><td style="padding:8px 10px;border:1px solid #e7e5e4;font-weight:700">点位二</td><td style="padding:8px 10px;border:1px solid #e7e5e4">裸到侧方一点点，膝盖微微打开、抬起来一点</td><td style="padding:8px 10px;border:1px solid #e7e5e4">洒脱</td></tr>
<tr><td style="padding:8px 10px;border:1px solid #e7e5e4;font-weight:700">点位三</td><td style="padding:8px 10px;border:1px solid #e7e5e4">把脚往回收，收到左脚脚后跟位置，膝盖并拢</td><td style="padding:8px 10px;border:1px solid #e7e5e4">内敛优雅（最常见）</td></tr>
<tr><td style="padding:8px 10px;border:1px solid #e7e5e4;font-weight:700">点位四</td><td style="padding:8px 10px;border:1px solid #e7e5e4">把脚藏在脚后跟位置，膝盖微微打开</td><td style="padding:8px 10px;border:1px solid #e7e5e4">三角形稳定构图、有结构感</td></tr>
<tr><td style="padding:8px 10px;border:1px solid #e7e5e4;font-weight:700">点位五</td><td style="padding:8px 10px;border:1px solid #e7e5e4">脚往回再收一点点，抬起来一下</td><td style="padding:8px 10px;border:1px solid #e7e5e4">洒脱飘逸</td></tr>
<tr><td style="padding:8px 10px;border:1px solid #e7e5e4;font-weight:700">点位六</td><td style="padding:8px 10px;border:1px solid #e7e5e4">把脚从后面绕回来，放在前面</td><td style="padding:8px 10px;border:1px solid #e7e5e4">达克宁广告经典美姿</td></tr>
</tbody></table>
<p>画圈圈可以引导模特按<strong>前面 → 侧面 → 正侧 → 后方 → 后侧 → 前侧</strong>的顺序移动，配合现场照片就能轻松上手。</p>
<figure><img src="assets/guide-pose-model/pose-foot-six.jpg" alt="六个脚法点位展示" loading="lazy"><figcaption><span class="time-badge">[05:15]</span>[05:15] 六个脚法点位的实拍参考：脚位一到脚位六</figcaption></figure>
<div class="tip-box"><strong>引导话术</strong><p>拍几张后让她「自动换一下点位二、点位三」。做对就夸，做错就提醒后再鼓励——她会慢慢放开，觉得「我的摄影师跟别人不一样」。</p></div>''')

parts.append('''<h4>手法：单手美姿（固定手 + 功能手）</h4>
<p>网上流传的「眼睛疼、鼻子疼、嘴巴疼、下巴疼」各种疼、各种抓，都有用，但可以更有逻辑地架构美姿框架。</p>
<div class="warn-box"><strong>划分布局</strong><p>不引导时，女生会两手自然垂下或抓在一起，都不是特别好。要分成两个手：<strong>一个固定手</strong>（保持不变）+ <strong>一个功能手</strong>（去各种抓）。</p></div>
<figure><img src="assets/guide-pose-model/pose-hand-fixed.jpg" alt="固定手与功能手划分" loading="lazy"><figcaption><span class="time-badge">[08:01]</span>[08:01] 单手美姿：固定手 + 功能手</figcaption></figure>
<p><strong>固定手标准姿态</strong>：手微微弯曲大概 <strong>135°</strong> 垂下来，手背微微转侧，手臂不要夹太紧、微微打开——手线条更好，避免呆板。后续所有动作中，这个手保持不变。</p>
<p><strong>功能手：自上而下各种抓</strong>，按顺序引导：</p>
<ul>
<li><strong>挡太阳</strong>——有花抓花、没花抓草、实在不行挡太阳（由高的地方抓起）</li>
<li><strong>抓头发</strong>　→　<strong>揉眼睛</strong>　→　<strong>揉鼻子</strong>　→　<strong>咬嘴巴</strong>　→　<strong>放下巴</strong>　→　<strong>放胸口</strong>　→　<strong>两手交叉</strong></li>
</ul>
<figure><img src="assets/guide-pose-model/pose-hand-grab.jpg" alt="功能手各种抓" loading="lazy"><figcaption><span class="time-badge">[09:37]</span>[09:37] 功能手自上而下：挡太阳→抓头发→揉眼睛→揉鼻子→咬嘴巴→放下巴→放胸口→交叉</figcaption></figure>
<div class="formula-box"><strong>核心心法</strong><p>「美姿小变化，机位构图大变化」——不要一张照片一个大变、考验素人模特，而是让模特做小小变化，摄影师去改变构图、机位、景别，让画面更丰富。</p></div>
<p><strong>摄影师的变化清单</strong>：横竖构图交替（抓空气竖构图→摸头发横构图→揉鼻子横构图→放胸口竖构图…）、高低机位（特写稍高机位、全身稍低机位）、远近距离、模特的正面和侧面。</p>''')

parts.append('''<h4>双手美姿：标准起式 + 关联变化</h4>
<p>先确定几个双手美姿的标准起式，不要「大动干戈」拉着手机找图片给模特看。依然遵循美姿小变化原则。</p>
<p><strong>起式一：双手抱胸</strong>——两个手呈一个<strong>八字</strong>抱在胸口，手腕压一下，手背稍微转侧，就是基本美姿；脚法用点位移动脚法即可。</p>
<figure><img src="assets/guide-pose-model/pose-hand-dual.jpg" alt="双手美姿抱胸八字" loading="lazy"><figcaption><span class="time-badge">[16:40]</span>[16:40] 双手美姿：抱胸八字起式 + 功能手变化</figcaption></figure>
<p><strong>拍完起式后</strong>：确定一个手为固定手保持不变，另一只手为功能手——抓头发、揉眼睛、揉鼻子、放嘴巴、放下巴，这就是「关联变化」。</p>
<p><strong>起式二：双手插腰</strong>——重点是一个手<strong>高一点点</strong>、一个手<strong>低一点点</strong>错开，两个手一样高就像吵架；错开高低手后头微微倒一下就是美姿。拍完同样进入固定手/功能手的变化（抓头发、揉下巴、摸耳朵）。</p>
<p>模特小小的变化，你大大的变化（横竖构图、高低机位、正面侧面），光线、构图、情绪就都出来了。</p>''')
parts.append('</section>')

# ============ 章节 2 坐姿 ============
parts.append('''<section class="story-section" id="sec2"><span class="time-marker">17:52 - 24:33</span><h3><span class="sec-num">二</span>坐姿篇</h3>
<p>坐姿的底层逻辑：<strong>两个确定</strong>。</p>

<h4>确定一：脚的角度 = 135°</h4>
<p>侧坐时如果不会引导，模特为防走光会把两脚<strong>伸得很直</strong>（像竹竿）或<strong>弯得很厉害</strong>（肉挤成一坨），两种都显腿短腿粗。正确做法：引导模特坐下时，把脚大概调整到 <strong>135°</strong>，刚刚好。</p>

<h4>确定二：视觉美学 = 前后脚错开 + 漏半鞋</h4>
<p>两脚并得太拢的 135° 也不好。要<strong>前后脚错开</strong>：靠近镜头的是前方脚，远离镜头的是后方脚。<strong>把后方脚往回收，收到漏半个鞋子出来</strong>——这是干货。</p>
<figure><img src="assets/guide-pose-model/pose-sit-angle.jpg" alt="坐姿135度与漏半鞋" loading="lazy"><figcaption><span class="time-badge">[20:08]</span>[20:08] 坐姿：135° + 前方脚伸长、后方脚漏半鞋</figcaption></figure>
<ul>
<li><strong>为什么漏后方脚、而不是前方脚？</strong> 前方脚漏出来画面会有两个鞋子，且前方脚往回收会显腿短；让镜头前面的脚往前伸、线条第一感觉更长。</li>
<li><strong>为什么只漏半个鞋子？</strong> 收得太多就是完整两个鞋子，显得累赘冗余；半个鞋既保留前方脚流畅性，又避免两个鞋同时出现的冗余感。</li>
</ul>
<div class="tip-box"><strong>吴老师提醒</strong><p>拍情绪片时这些小细节可以放掉，但「先立规矩」——一板一眼学好，之后张弛有度地放，才是你的拿捏尺度。</p></div>

<h4>坐姿手法：和站姿完全一样</h4>
<p>脚法做好后，手法跟站姿里面的手法相同：先做一个起式（两手自然垂下、手指交叉、抬头看天），拍完不要大动，确定<strong>固定手</strong>与<strong>功能手</strong>。</p>
<figure><img src="assets/guide-pose-model/pose-sit-hand.jpg" alt="坐姿手法" loading="lazy"><figcaption><span class="time-badge">[22:44]</span>[22:44] 坐姿手法：前方手固定，后方手自上而下抓</figcaption></figure>
<p>坐姿前方手（左手）作固定手自然垂下，后方手作功能手由上往下抓：有花抓花、没花抓草、挡太阳、抓头发、抓下巴，再往下<strong>抓大臂、抓小臂、两手高低搭</strong>——一个手抓下来就拍了三张美姿。</p>
<div class="formula-box"><strong>总结</strong><p>坐姿侧坐：一确定脚法（135°、一脚前一脚后），二确定手法（固定手 + 功能手），配合高低机位、远近景别、正侧面角度实现美姿细微变化。</p></div>''')
parts.append('</section>')

# ============ 章节 3 蹲姿 ============
parts.append('''<section class="story-section" id="sec3"><span class="time-marker">24:36 - 32:53</span><h3><span class="sec-num">三</span>蹲姿篇</h3>
<p>蹲姿用好了有<strong>松弛感</strong>，没用好就拍出「熊猫蹲」或「上厕所」的感觉。</p>

<h4>基本逻辑：避免正面蹲，45° 侧方位</h4>
<p>正面蹲容易显得<strong>头大、臃肿、呆板</strong>（偶尔拍萌萌哒、撒娇可以来几张）。大部分情况调整为<strong>45° 侧方位</strong>——身体转侧一点点，腿部线条、手部线条、脸部侧面都会更好看，脸型更好，你就成功了一小半。</p>

<h4>三种蹲法</h4>
<p><strong>蹲法一：平行蹲</strong>——两脚并拢直接蹲下去。</p>
<figure><img src="assets/guide-pose-model/pose-squat-parallel.jpg" alt="平行蹲" loading="lazy"><figcaption><span class="time-badge">[27:01]</span>[27:01] 平行蹲：两脚并拢 + 提气头朝上</figcaption></figure>
<ul>
<li><strong>脚法</strong>：两脚并拢，直接蹲下。</li>
<li><strong>核心关键</strong>：<strong>提气、头朝上</strong>——想象头去撞天花板、头顶天花板的感觉，避免驼背弯腰，身形比例更好。</li>
<li><strong>手法</strong>：先两手并拢交叉或垂下，然后前方手为固定手不变，后方手各种抓：抓嘴巴、摸头发、抓后面的头发、抓大臂、抓小臂。</li>
</ul>

<p><strong>蹲法二：后方重心腿蹲</strong>——一个脚高一个脚低，后方腿蹲地支撑身体。</p>
<figure><img src="assets/guide-pose-model/pose-squat-back.jpg" alt="后方重心腿蹲" loading="lazy"><figcaption><span class="time-badge">[28:30]</span>[28:30] 后方重心腿蹲：后方腿支撑，前方腿往前伸约 110°</figcaption></figure>
<ul>
<li><strong>脚法</strong>：后方腿直接蹲地作为重心；<strong>前方腿尽量往前伸</strong>（大概 110°），腿部线条更修长，前方形成三角区域更稳健好看。关键点：前方腿要往前伸，不要勾着里面，勾着显腿短。</li>
<li><strong>手法</strong>：两手合拢放一起也可；再一个手固定、一个手功能：抓大臂、撩头发、挡太阳。</li>
</ul>

<p><strong>蹲法三：前方腿重心蹲</strong>——前方脚着地，重点调整后方腿。</p>
<figure><img src="assets/guide-pose-model/pose-squat-front.jpg" alt="前方腿重心蹲" loading="lazy"><figcaption><span class="time-badge">[29:24]</span>[29:24] 前方腿重心蹲：前方脚着地，后方腿往前伸约 110°</figcaption></figure>
<ul>
<li><strong>脚法</strong>：前方腿着地后，后方腿不要弯得特别厉害，把脚往前伸一点点（约 110°）——熟悉的配方前后对调，线条就流畅。</li>
<li><strong>手法</strong>：一个手顺势搭着，另一个手反手插腰、抓小臂、撑下巴。</li>
</ul>

<h4>通用手法：画圈圈抓（站坐蹲躺趴靠都适用）</h4>
<p>无论站姿坐姿蹲姿躺姿趴姿靠姿，手法是<strong>通用型</strong>的：确定一个固定手 + 一个功能手，功能手各种抓，可以<strong>画圈圈抓、由上往下抓</strong>。</p>
<figure><img src="assets/guide-pose-model/pose-hand-circle.jpg" alt="通用手法画圈圈抓" loading="lazy"><figcaption><span class="time-badge">[30:29]</span>[30:29] 通用手法：固定手不变，功能手画圈圈自上而下抓</figcaption></figure>
<p>固定手全程不变，功能手依次：脱下巴 → 撩头发 → 摸头顶 → 撩后脑勺头发（画一个圈圈过去）→ 摸肩膀 → 摸大臂 → 摸小臂 → 双手高低搭，变化非常多。</p>

<h4>附加小技巧：头部三变化</h4>
<div class="tip-box"><strong>看天 / 看地 / 看镜头</strong><p>不要张张看镜头：抬头看天拍几张 → 低头看地拍几张 → 偏头（头歪一下、倒头偏头）看镜头。站姿坐姿都适用，画面更丰富。</p></div>''')
parts.append('</section>')

# ============ 章节 4 靠姿 ============
parts.append('''<section class="story-section" id="sec4"><span class="time-marker">33:01 - 38:02</span><h3><span class="sec-num">四</span>靠姿篇</h3>
<div class="formula-box"><strong>核心要点</strong><p>只允许身体<strong>一个部位</strong>去靠（墙 / 电线杆），不要多处靠。</p></div>
<figure><img src="assets/guide-pose-model/pose-lean-wrong.jpg" alt="靠姿错误案例" loading="lazy"><figcaption><span class="time-badge">[33:19]</span>[33:19] 反面教材：头、肩、手三个部位同时靠墙，人像电线杆没有曲线</figcaption></figure>
<p>错误示范：头靠墙 + 肩靠墙 + 手贴墙（三个部位靠），人身体像电线杆，没有曲线和流畅性。<strong>记住：只让身体的一个部位去靠</strong>。通常分四种：</p>

<p><strong>① 手去靠墙</strong>——反手搭靠墙，或把手直接支撑搭在墙上。</p>
<figure><img src="assets/guide-pose-model/pose-lean-hand.jpg" alt="手靠墙" loading="lazy"><figcaption><span class="time-badge">[34:08]</span>[34:08] 手靠墙：反手搭或直接支撑</figcaption></figure>
<ul>
<li><strong>温馨提示</strong>：人跟靠的物体<strong>隔远一点点</strong>，更好引导美姿。</li>
<li><strong>脚法</strong>：用六脚法里的<strong>点位一</strong>。</li>
<li><strong>手法</strong>：两手抓在一起，或一个固定手 + 一个功能手：撩头发、放下巴、搭头顶挡太阳、拉眼镜、拿帽子。</li>
</ul>

<p><strong>② 肩膀靠墙</strong>——身体与物体远一点，侧面用肩膀靠。</p>
<figure><img src="assets/guide-pose-model/pose-lean-shoulder.jpg" alt="肩膀靠墙" loading="lazy"><figcaption><span class="time-badge">[35:10]</span>[35:10] 肩膀靠墙：侧面用肩靠，头尽量不靠</figcaption></figure>
<ul>
<li>肩膀靠了之后<strong>头尽量不要靠</strong>，更不要头跟臀部一起靠。</li>
<li><strong>脚法</strong>：仍用点位一，侧面版点位一。</li>
<li><strong>手法</strong>：双手抱胸起式，再确定固定手/功能手抓头发、揉眼睛、挡太阳；一手上、一手抱肚子等。</li>
</ul>

<p><strong>③ 臀部靠墙</strong>——身体尽量的分开一点点，上半身往前压一点点，线条感更好。</p>
<figure><img src="assets/guide-pose-model/pose-lean-hip.jpg" alt="臀部靠墙" loading="lazy"><figcaption><span class="time-badge">[36:10]</span>[36:10] 臀部靠墙：上半身往前压，线条感更好</figcaption></figure>
<ul>
<li><strong>手法</strong>：一个手抱着手臂位置，后方手为功能手摸头发、放嘴巴。</li>
<li><strong>脚法</strong>：可以踮起来，或六脚法里任意一个。</li>
<li>配合高低构图、横竖构图、正侧面变化。</li>
</ul>

<p><strong>④ 脚去靠墙（单脚靠墙）</strong>——特别适合洒脱一点的拍法。</p>
<figure><img src="assets/guide-pose-model/pose-lean-foot.jpg" alt="单脚靠墙" loading="lazy"><figcaption><span class="time-badge">[37:10]</span>[37:10] 单脚靠墙：脚勾起来，洒脱感</figcaption></figure>
<ul>
<li>人跟墙<strong>远一点点</strong>，把一个脚勾起来靠在墙上。</li>
<li><strong>手法</strong>：两手抱在一起，或一个手去抓。</li>
<li>可以拍<strong>背面、侧面、回头</strong>的单脚靠墙，非常好看。</li>
</ul>
<div class="formula-box"><strong>靠姿两大要点</strong><p>① 只允许身体一个部位靠：手 / 肩 / 臀 / 脚；② 人跟靠的物体远一点点，不要挨太近，更好舒展开做美姿。</p></div>''')
parts.append('</section>')

# ============ 章节 5 道具 ============
parts.append('''<section class="story-section" id="sec5"><span class="time-marker">38:06 - 42:26</span><h3><span class="sec-num">五</span>道具篇</h3>
<p>新手阶段不会摆美姿，常准备道具让模特拉着，缓解尴尬；也可以在场景里随机选匹配元素做道具。</p>
<div class="formula-box"><strong>核心关键</strong><p>不要急，慢慢来。拿到道具不要马上戴上去「咔嚓咔嚓」拍两张就没得拍了。</p></div>

<h4>墨镜：由下往上慢慢来</h4>
<p>拉着墨镜时<strong>不要急着戴</strong>，由下往上一步步放：</p>
<figure><img src="assets/guide-pose-model/pose-prop-sunglasses.jpg" alt="墨镜道具由下往上" loading="lazy"><figcaption><span class="time-badge">[39:27]</span>[39:27] 墨镜道具：垂下 → 腹部 → 锁骨 → 嘴 → 眼睛 → 头顶</figcaption></figure>
<ol>
<li>手拉墨镜自然<strong>垂下去</strong>（放这个位置）</li>
<li>慢慢拉高一点点，放<strong>腹部</strong></li>
<li>再放<strong>锁骨</strong></li>
<li>再放<strong>嘴巴</strong></li>
<li>再放<strong>眼睛</strong></li>
<li>最后<strong>戴在头顶</strong></li>
</ol>
<p>这样一个道具就能拍出一整套连贯的美姿，而不是一戴一拍就结束。</p>

<h4>背包：同样的逻辑</h4>
<figure><img src="assets/guide-pose-model/pose-prop-bag.jpg" alt="背包道具" loading="lazy"><figcaption><span class="time-badge">[40:10]</span>[40:10] 背包道具：垂下 → 放上一点 → 腹部 → 侧面 → 肩</figcaption></figure>
<p>拉了包之后：先自然垂下去拍一下 → 放上一点位置 → 放腹部 → 放侧面 → 放肩部，画面就丰富起来。</p>

<h4>摄影师的变化空间</h4>
<p>记住「美姿小变化、机位构图大变化」：同一个美姿下，摄影师可以<strong>找不同角度</strong>——正面拍完拍侧面、侧面拍完拍背面；让模特转侧一点拍偏背影、手搭下来墨镜放下抬头往上看；再改变<strong>高低机位、横竖构图</strong>，画面就灵动丰富。</p>
<div class="tip-box"><strong>吴老师的教学观</strong><p>没有花里胡哨的高审美要求，只是接地气地讲清逻辑和核心要点，再拍给你看。把这套当作你的<strong>底层逻辑和下限</strong>，理解后再教模特，有了基本功再去尝试松弛感、生命力的照片。</p></div>''')
parts.append('</section>')

parts.append('</article>')

# 转录
parts.append('''<section class="transcript-section" id="transcript"><details class="transcript-collapsible"><summary>详细文字转录</summary><div class="transcript-body">
<p class="transcript-note">以下内容按 Whisper 原始分段完整呈现，可能包含识别误差。</p>
<ol class="transcript-list">''')
parts.append(transcript_items)
parts.append('</ol>')
parts.append('</div></details></section>')
parts.append('</main><script>(function(){var d=document.querySelector(".transcript-collapsible");if(!d)return;function open(){d.setAttribute("open","")}document.querySelectorAll(\'a[href="#transcript"]\').forEach(function(a){a.addEventListener("click",open)});if(location.hash==="#transcript")open()})();</script></body></html>')

html_out = "\n".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html_out)

print(f"OK {len(html_out)} chars, {len(rows)} transcript rows")
