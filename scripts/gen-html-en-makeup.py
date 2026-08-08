#!/usr/bin/env python3
"""生成 makeup-class-prep 的英文版图文实录页面。

复用中文版的截图、图注音频、双语图注结构与完整转录区（转录保留原语言作为证据），
将标题、导航、章节正文、引文、列表翻译为英文，输出独立文件
docs/makeup-class-prep-图文实录-en.html。
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "docs" / "makeup-class-prep-图文实录.html"
OUT = ROOT / "docs" / "makeup-class-prep-图文实录-en.html"

# ---- 提取转录区（原样保留，证据区不翻译）----
src_html = SRC.read_text(encoding="utf-8")
transcript_m = re.search(r'<section class="transcript-section" id="transcript">.*?</section>', src_html, re.S)
transcript_section = transcript_m.group(0) if transcript_m else ""
# 转录区 summary 标题翻成英文
transcript_section = transcript_section.replace(
    "完整转录（861段）", "Full Transcript (861 segments)"
)
transcript_section = transcript_section.replace(
    "以下文本由 Whisper medium 模型自动转录，可能存在少量识别误差，已尽可能修正。",
    "Below is the raw Whisper transcription in its original language; captions and narration above are translated into English.",
)

CSS = """*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:-apple-system,"Segoe UI","Helvetica Neue",Arial,"PingFang SC",sans-serif;line-height:1.8;color:#292524;background:#fafaf9}
.container{width:min(960px,100%);margin:0 auto;padding:48px 32px 80px}header{margin-bottom:40px}
header h1{font-size:32px;font-weight:900;color:#1c1917;margin:0 0 12px;line-height:1.3}
.meta-row{display:flex;gap:16px;flex-wrap:wrap;align-items:center;margin-bottom:16px}
.meta-tag{display:inline-block;padding:4px 14px;border-radius:20px;font-size:13px;font-weight:600}
.tag-platform{background:#ff2442;color:#fff}.tag-duration{background:#f1f5f9;color:#64748b}.tag-topic{background:#dbeafe;color:#1e40af}
.source-link{color:#3b82f6;font-size:14px;text-decoration:none}.source-link:hover{text-decoration:underline}
.lang-switch{display:inline-block;margin-left:16px;font-size:13px;font-weight:700}
.toc{background:#fff;border-radius:16px;padding:20px 24px;margin-bottom:32px;box-shadow:0 2px 12px rgba(0,0,0,.04)}
.toc h3{font-size:16px;color:#1e40af;margin:0 0 12px}.toc a{display:block;color:#475569;font-size:14px;text-decoration:none;padding:4px 0;border-bottom:1px solid #f1f5f9}.toc a:hover{color:#3b82f6}
.documentary{font-size:17px}.story-section{margin:48px 0}
.story-section h2{font-size:24px;font-weight:700;color:#1c1917;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.story-section p{margin:0 0 14px;color:#44403c}
.time-marker{display:inline-block;padding:2px 8px;background:#fef3c7;border-radius:6px;font-size:13px;font-weight:700;color:#b45309;margin-right:6px;font-variant-numeric:tabular-nums}
.quote-block{background:#f0fdf4;border-left:4px solid #10b981;padding:12px 16px;border-radius:8px;margin:14px 0;font-size:15px;color:#166534;font-style:italic}
.story-section ul,.story-section ol{padding-left:22px;margin:0 0 14px}.story-section li{margin:0 0 8px;color:#44403c}
img{display:block;max-width:100%;height:auto}figure{margin:28px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(41,37,36,.1)}
figcaption{padding:14px 18px;color:#57534e;font-size:14px}figcaption .time-badge{font-weight:700;color:#b45309;margin-right:6px}
.transcript-section{margin-top:48px}.transcript-section h2{font-size:24px;font-weight:700;color:#1c1917}
.transcript-note{font-size:14px;color:#78716c;margin-bottom:24px}.transcript-list{list-style:none;padding:0}
.transcript-row{display:grid;grid-template-columns:72px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid #e7e5e4}
.transcript-row time{font-variant-numeric:tabular-nums;color:#b45309;font-weight:700}.transcript-row p{margin:0}
@media(max-width:640px){.container{padding:28px 18px 56px}header h1{font-size:24px}.transcript-row{grid-template-columns:56px 1fr;gap:10px}}
.transcript-collapsible{border:none;margin:0;padding:0}.transcript-collapsible summary{display:flex;align-items:center;gap:10px;cursor:pointer;list-style:none;user-select:none;font-size:24px;font-weight:700;color:#1c1917;margin:0;padding-bottom:8px;border-bottom:2px solid #e7e5e4}
.transcript-collapsible summary::-webkit-details-marker,.transcript-collapsible summary::marker{display:none}
.transcript-collapsible summary::before{content:"▶";font-size:12px;color:#b45309;transition:transform .2s;flex-shrink:0}
.transcript-collapsible[open] summary::before{transform:rotate(90deg)}.transcript-collapsible[open] summary{margin-bottom:16px}.transcript-collapsible .transcript-body{margin-top:0}
.cap-bilingual{padding:14px 18px}.cap-bilingual .cap-zh{color:#57534e;font-size:14px;line-height:1.7}.cap-bilingual .cap-zh .time-badge{font-weight:700;color:#b45309;margin-right:6px}.cap-bilingual .cap-en{display:flex;align-items:flex-start;gap:10px;margin-top:8px;padding-top:8px;border-top:1px dashed #e7e5e4;color:#0f766e;font-size:14px;line-height:1.7}.cap-speak{flex:none;width:34px;height:34px;border:none;border-radius:50%;background:#0f766e;color:#fff;font-size:14px;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;transition:transform .15s,background .2s}.cap-speak:hover{background:#115e59;transform:scale(1.08)}.cap-speak.playing{background:#b45309;animation:capPulse 1s infinite}@keyframes capPulse{0%,100%{opacity:1}50%{opacity:.55}}"""

# ---- 图注双语块（复用中文版已有的，保证音频路径一致）----
CAPTION_FIGS = re.findall(r"<figure>.*?</figure>", src_html, re.S)
fig_by_shot = {}
for fig in CAPTION_FIGS:
    shot_m = re.search(r"shot-0\d\.jpg", fig)
    if shot_m:
        fig_by_shot[shot_m.group(0).replace(".jpg", "")] = fig

def fig(shot: str) -> str:
    return fig_by_shot.get(shot, "")

# ---- 章节正文 ----
SECTIONS = [
    (
        "intro",
        "Opening: Don't rush to enroll — watch this video first",
        f"""<p><span class='time-marker'>00:00</span>If you're thinking about signing up for a makeup class, I'd say you can hold off for now. What this video wants to make clear are the basic principles of makeup and the order of every single step.</p>
<p><span class='time-marker'>00:18</span>First, "chew over" this free video: if you're happy with the results, you don't need the class; if something's still missing, you can still go pay for a class later — no rush.</p>
{fig('shot-01')}
<div class="quote-block">Once you've chewed it over and found the result genuinely satisfying, you don't need to take the makeup class.</div>""",
    ),
    (
        "prep",
        "Pre-base prep: hair cleanup + skin cleansing + exfoliation",
        f"""<p><span class='time-marker'>00:41</span>The first step of makeup is clearing the facial hair. Especially the upper-lip area: if you apply foundation over the hair, that patch turns bluish. Shave along the grain — don't shave against it and cut yourself.</p>
<p><span class='time-marker'>01:06</span>Once the hair is handled, take a cotton pad (or cotton sheet) dipped in toner and wipe along the skin's texture to remove stubble, excess oil, and dust. This is the skin cleanse before base makeup; its purpose is to eliminate the "barrier" between the foundation and your skin.</p>
<p><span class='time-marker'>01:40</span>If the dead skin around your nostrils is especially tough, soak a cotton pad in a little water and leave it on to soften it, then gently sweep it off; if you don't feel much dead skin, skip the compress.</p>
{fig('shot-02')}
<ul><li>Shave the upper-lip hair along the grain → avoid a bluish patch under foundation</li><li>Wipe with a toner-soaked cotton pad along the skin's texture → remove the oil / dust / dead-skin barrier</li><li>Tough nose-wing dead skin → soften with a wet compress, then lift it off</li></ul>""",
    ),
    (
        "hydrate",
        "Hydrate + lock in moisture: two separate steps",
        """<p><span class='time-marker'>02:00</span>After cleansing, apply hydrating mist, pat it in, and wait until it's fully absorbed before the next layer. On rough spots like the nose, rub in small circles to work the water in. In summer the mist is usually enough — your skin should feel slightly soft to the touch.</p>
<p><span class='time-marker'>02:32</span>If you're misting plenty and the makeup still flakes, the problem is usually the missing "lock-in" step: water, mist, and essence hydrate, while creams and lotions lock moisture in. Hydrate without locking, and once the water evaporates your face is dry and peeling again.</p>
<div class="quote-block">Hydrate only, don't lock it in, and no matter how many layers you pile on, your face is still dry and peeling.</div>
<ul><li>Hydrate: mist / water / essence</li><li>Lock in: cream / lotion (especially crucial in autumn-winter or for dry skin)</li></ul>""",
    ),
    (
        "sunscreen",
        'Sunscreen: "press" instead of "rub" — barely any pilling',
        """<p><span class='time-marker'>03:18</span>Sunscreen is a must in summer. Before the puff touches your face, dab it once to pick up any lint; run the puff under water once, then use a sponge to dab sunscreen onto your face — don't worry, the sponge won't eat the sunscreen.</p>
<p><span class='time-marker'>04:10</span>No need to fear pilling: pick a lotion-textured sunscreen and press it on with the puff — pilling is rare. Because this technique keeps your fingers from rubbing the face at all — no rubbing, no pilling.</p>
<p><span class='time-marker'>04:34</span>After sunscreen, don't rush to layer anything on; wait for it to form a film. You can fan it with a small fan.</p>
<ol><li>Pick a lotion-textured sunscreen</li><li>Press it on with a puff / sponge</li><li>Wait for the film to set before the next step</li></ol>""",
    ),
    (
        "conceal",
        "Pre-base concealer: match by color",
        f"""<p><span class='time-marker'>04:40</span>Pre-base concealing is handled by the blemish's color: bluish areas get purple to brighten, yellowish areas also get purple dots, and reddish areas get a green concealer to take care of large red zones.</p>
<p><span class='time-marker'>05:00</span>The technique is brush to spread + puff to press: a dab on the brush tip, spread evenly, then press with the puff — nothing like pros ending up thick here and thin there. What's left uneven on your face? The dark circles.</p>
<p><span class='time-marker'>05:51</span>Don't expect to hide dark circles completely — that's nearly impossible. It's enough that they're basically invisible from the front. Use a salmon shade; each time pick up just a tiny bit on the brush, apply a little often, and it basically won't cake.</p>
{fig('shot-03')}
<ul><li>Bluish / yellowish → purple to brighten</li><li>Reddish → green concealer</li><li>Dark circles → salmon shade, apply a little often, no caking</li></ul>""",
    ),
    (
        "foundation",
        "Foundation: first stroke on the mid-face, blend outward",
        """<p><span class='time-marker'>07:26</span>After concealing, add a layer of setting spray: it locks the concealer in place. Like double-sided tape, one side sticks down the concealer while the other side grips the foundation about to go on. Once it dries into a film, apply the foundation.</p>
<p><span class='time-marker'>07:39</span>The first stroke of foundation lands on the mid-face; this line holds the boundary between the inner and outer face. After applying, tap inward with a small brush or puff so all the foundation lands on the mid-face first — the area the face most needs evened out — then transition outward a little at a time.</p>
<p><span class='time-marker'>08:12</span>The outer contour is where you normally contour; having less product there or it looking a bit darker is fine — it actually reads more sculpted. A thin layer of foundation and the skin tone is right.</p>
<div class="quote-block">Less foundation on the outer contour actually looks more sculpted, because that's where contouring is supposed to do its work.</div>
<ul><li>First stroke on the mid-face → establishes the inner / outer face boundary</li><li>Tap from inside out → thin, natural transition at the outer contour</li><li>Bridge concealer and foundation with a layer of setting spray</li></ul>""",
    ),
    (
        "bones",
        "Bone-structure trio: highlight + contour + blush",
        f"""<p><span class='time-marker'>08:30</span>Once the foundation is on, highlight, blush, and contour work as a set — all of them sculpt the face's bone structure.</p>
<p><span class='time-marker'>08:34</span>Highlight not showing up? Most likely it hasn't separated enough from the foundation — your highlight has to be visibly much whiter than the foundation. Does it look like it's floating on the skin? Mix a little of the foundation you just used into the highlight and it'll sit more naturally.</p>
<p><span class='time-marker'>08:58</span>Highlight placement: mid-face, corners of the mouth, chin, nose bridge, brow bone, under the eyes. Highlighting under the eyes keeps tear troughs from looking so dark and makes the area look fuller.</p>
<p><span class='time-marker'>10:01</span>Contour: whatever sticks out most from the front, shade down from there. The nose shadow needs layers — not one uniform dark stripe: the deepest color sits at the sides of the nose root, everywhere else is a transition that tucks inward — don't go too hard.</p>
<p><span class='time-marker'>11:36</span>A little shadow under the lips makes them look poutier and more defined; shade the jaw-to-neck line and the jawline appears.</p>
<p><span class='time-marker'>12:06</span>Blush does two jobs: it brightens your complexion, and it's also contouring. The outer contour is dark, the inner highlight is light — blush bridges that empty band in between. A dab of blush under and along the nose works like shadow to make the nose look taller.</p>
{fig('shot-04')}
<ul><li>Highlight: must be visibly whiter than the foundation; mix in foundation if it won't sit well</li><li>Contour: nose shadow needs layers — deep → transition → tuck in</li><li>Blush: bridges outer shadow and inner highlight; lip color and blush in the same family</li></ul>""",
    ),
    (
        "powder",
        "Powder setting: never skip the eyelids",
        """<p><span class='time-marker'>13:20</span>After highlight, blush, and contour, one more layer of setting spray: it sets everything just applied, while the spray's water melts the powdery look. While the film dries, sort out the logic — concealer and foundation unify the skin tone; highlight, blush, and contour sculpt the bone structure.</p>
<p><span class='time-marker'>14:02</span>Once the setting spray films over, apply setting powder to the spots that get oily or shiny. You can powder the whole face, or keep a local glow.</p>
<p><span class='time-marker'>14:14</span>Always set the eyelids well with a small brush and powder — otherwise your eyeliner smudges fast no matter what product you use.</p>
<div class="quote-block">Skip setting the eyelids and the eyeliner smudges quickly, whatever product you use.</div>""",
    ),
    (
        "eyes",
        "Eye makeup: pick the right brushes + fill the lash line",
        f"""<p><span class='time-marker'>14:30</span>Eye shadow brushes matter: a fluffy brush suits large-area blending — the color comes out natural with a soft, blurred edge; a flat, firm brush suits small-area deepening with a harder edge. Sweep the dark shade along the outer corner and the lash line, dust a little under the lower lid, and the eye's shape looks more dimensional.</p>
<p><span class='time-marker'>16:02</span>For eyeliner use an angled brush, ideally on a small pen handle. Lift the eyelid and fill the brush tip into the lash line. Beginners don't need to flip the lid — just fill the lash root bit by bit with a small brush; it looks far less intimidating. The moment the liner's done, the eyes suddenly come alive.</p>
{fig('shot-05')}
<ul><li>Fluffy brush → large-area blending, natural edges</li><li>Flat firm brush → small-area deepening (outer corner, lash line)</li><li>Eyeliner: lift the lid with the pen handle, fill the lash root</li></ul>""",
    ),
    (
        "lash",
        "Lashes + brows: the window and the curtain",
        f"""<p><span class='time-marker'>18:39</span>The eyes are the window to the soul; lashes are the curtains. Curling: line the bottom edge of the curler with the upper-lid rim, clamp, tilt the eye slightly upward, squeeze, and lift — the lashes are curled.</p>
<p><span class='time-marker'>19:12</span>After curling, apply a lash primer — think of it as the lash "setting gel" that keeps them standing longer. The primer must be brushed from the root upward; stroke from the root to set. After the primer, mascara, also from the root.</p>
<p><span class='time-marker'>19:55</span>Want to wear falsies? For beginners, the glue-free type is easiest — no glue to apply. Clamp them about one-third from the lash root, curve the whole lash toward you, and stick them onto your real lash roots. Falsies are the icing on the cake for a beginner look — nice to have, fine without.</p>
<p><span class='time-marker'>20:25</span>Brows: first sweep the foundation off the brows with a brush, or brow powder will cake. Match the brow powder to your hair color and fill the skin under the brows first; dip the brow mascara wand into the tube before applying — it tints the hairs, not the skin. For daily makeup that's enough; if you want more definition, use a brow pencil along the middle line of the brow — the brow's framework.</p>
{fig('shot-06')}
<ul><li>Curler: rim against the upper lid → tilt up → squeeze → lift</li><li>Lash primer + mascara: always brush from the root upward</li><li>Falsies: glue-free type, clamp 1/3 from the lash root</li></ul>""",
    ),
    (
        "second",
        "Second pass: makeup is layered rendering, not one-shot",
        """<p><span class='time-marker'>21:45</span>After the brows, redo a round of contour and blush: the powder earlier "ate" the shine and color, so you need deeper shades to re-deepen locally.</p>
<p><span class='time-marker'>22:21</span>Contour too dark? Mix a little setting powder into the contour — it both absorbs color and sets it. If you always think your contour looks dirty, try two contour shades: a light one blended over a large area, a dark one deepened locally — the depth shows up right away.</p>
<p><span class='time-marker'>23:11</span>The blush touch-up must match the first round's tone — whatever shade you used then, keep using it; a slight difference is okay, but don't switch from warm to purple tones. Just a tiny bit of powder is enough.</p>
<div class="quote-block">Makeup isn't done in one swoop — first a little here, then deepen a little more, layer by layer of rendering.</div>""",
    ),
    (
        "highlight",
        "Highlight layering: big circle in small circle, then a mini circle",
        """<p><span class='time-marker'>24:00</span>Highlight powders have rules. The natural-white type suits large areas: mid-face, forehead, chin. The dead-white type only suits small single-point highlights — never apply it over a large area, or it looks like you applied nothing.</p>
<p><span class='time-marker'>24:50</span>Pearl highlight: on top of the large and small highlight areas, dot two tiny spots — like the nose tip — so it catches a natural sheen.</p>
<p><span class='time-marker'>25:20</span>The three highlights relate like a big circle inside a small circle, then a mini circle: natural white makes the big circle, dead white the small circle, pearl the mini circle — dotted locally, the highlighting gets its layers.</p>
<ul><li>Natural white → large areas: mid-face, forehead, chin</li><li>Dead white → small single points only, not large areas</li><li>Pearl → mini circle: glow points like the nose tip</li></ul>""",
    ),
    (
        "lip",
        "Lipstick finale: lip liner = lip contouring",
        f"""<p><span class='time-marker'>25:43</span>Time for lipstick. A lip liner acts as lip contouring: first wipe the wax coat off the pencil with a piece of paper — otherwise it won't deposit color. It's ideal for thin upper lips — it blurs the obvious lip boundary so you can't tell where the upper lip starts, creating a lip-enlarging effect. Run it over the lower lip and the lip looks poutier.</p>
<p><span class='time-marker'>26:35</span>Filled the whole lip and still no color, like you're sick? Grab a shade a bit redder than it, and don't cover the whole lip — just the inner part, almost. Big circle wrapping a small circle, and the color appears. That's the whole look done.</p>
{fig('shot-07')}
<div class="quote-block">Lipstick has no color? Layer a redder shade on the inner lip: big circle wrapping a small circle, and the color's there.</div>""",
    ),
]

# ---- 组装页面 ----
toc_links = "\n".join(
    f'<a href="#{sid}">{title}</a>' for sid, title, _ in SECTIONS
)
toc_links += '\n<a href="#transcript">Full transcript</a>'

body_sections = "\n".join(
    f'<section class="story-section" id="{sid}"><h2>{title}</h2>{body}</section>'
    for sid, title, body in SECTIONS
)

html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="Before booking an in-person makeup class, watch this 27-minute guide: hair cleanup, skin cleansing, sunscreen, color-correcting concealer, foundation, the bone-structure trio, eye makeup, and lipstick.">
<title>Makeup Prep Diary | Watch This Before Booking an In-Person Makeup Class</title>
<style>{CSS}</style>
</head>
<body><main class="container">
<header><h1>Makeup Prep Diary | Watch This Before Booking an In-Person Makeup Class</h1>
<div class="meta-row"><span class="meta-tag tag-platform">Xiaohongshu</span><span class="meta-tag tag-duration">27:45</span><span class="meta-tag tag-topic">Makeup tutorial / Beginner makeup / Base techniques</span></div>
<a class="source-link" href="http://xhslink.cn/o/9TtjHs4NiCD" target="_blank" rel="noopener">→ Original video</a>
<a class="source-link lang-switch" href="makeup-class-prep-图文实录.html" hreflang="zh">中文版</a></header>
<nav class="toc"><h3>On this page</h3>
{toc_links}</nav>
<article class="documentary">
{body_sections}
</article>
{transcript_section}
</main><script id="cap-en-script">
(function(){{
  function stopOthers(except){{
    document.querySelectorAll('.cap-audio').forEach(function(a){{
      if(a!==except){{a.pause();a.currentTime=0;}}
    }});
    document.querySelectorAll('.cap-speak.playing').forEach(function(b){{
      if(!except||b.dataset.audio!==except.dataset.audio){{b.classList.remove('playing');}}
    }});
  }}
  document.addEventListener('click',function(e){{
    var btn=e.target.closest('.cap-speak');
    if(!btn)return;
    var cap=btn.closest('.cap-bilingual');
    if(!cap)return;
    var au=cap.querySelector('.cap-audio');
    if(!au)return;
    if(au.paused){{
      stopOthers(au);
      btn.classList.add('playing');
      au.play();
    }}else{{
      au.pause();au.currentTime=0;btn.classList.remove('playing');
    }}
  }});
  ['pause','ended'].forEach(function(ev){{
    document.addEventListener(ev,function(e){{
      if(e.target.classList&&e.target.classList.contains('cap-audio')){{
        var cap=e.target.closest('.cap-bilingual');
        if(cap){{var b=cap.querySelector('.cap-speak');if(b)b.classList.remove('playing');}}
      }}
    }},true);
  }});
}})();
</script>
<script id="transcript-open-script">(function(){{var d=document.querySelector(".transcript-collapsible");if(!d)return;function o(){{d.setAttribute("open","")}}document.querySelectorAll('a[href="#transcript"]').forEach(function(a){{a.addEventListener("click",o)}});if(location.hash==="#transcript")o()}})();</script></body></html>"""

OUT.write_text(html, encoding="utf-8")
print(f"generated: {OUT.name} ({len(html)} bytes)")
