#!/usr/bin/env python3
"""makeup-class-prep → 场景英译学习卡（复用 language_paraphrase 的方式）。

产出：
- docs/audio/makeup-class-prep/{s1.mp3, s1-01.mp3, ..., practice-0.mp3, narration.mp3}
- docs/makeup-class-prep-场景英译.html

数据内嵌在 DATA 结构中；英文翻译/表达提示/paraphrase/练习/避坑/认知转变
为人工精修内容（ASR 专有名词已校正）。
"""
from __future__ import annotations

import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
AUDIO_DIR = DOCS / "audio" / "makeup-class-prep"
OUT_HTML = DOCS / "makeup-class-prep-场景英译.html"
IMG = "assets/makeup-class-prep"

ZH_VOICE = "zh-CN-XiaoxiaoNeural"
EN_VOICE = "en-US-JennyNeural"
MAX_CHUNK_LEN = 2000

META = {
    "slug": "makeup-class-prep",
    "title": "练妆日记 | 想上线下化妆课的姐妹先看看这",
    "title_en": "Makeup Prep Diary: Watch This Before Booking an In-Person Makeup Class",
    "duration": "27:45",
    "scenes": 10,
    "sentences": 36,
}

# 场景截图映射（7 张图注截图 → 10 个场景，部分复用）
SCENE_IMG = ["shot-01", "shot-02", "shot-02", "shot-02", "shot-03",
             "shot-03", "shot-04", "shot-05", "shot-06", "shot-07"]

SCENES = [
    {
        "id": "s1", "title_cn": "开场：别急着报名，先看完这条免费视频",
        "title_en": "Opening: Watch the Free Video Before You Enroll",
        "time": "00:00–00:40", "context": "博主劝姐妹们在花钱报线下化妆课之前，先用这条免费视频自己试试。语域：教程口播，东北口语（鼓球＝琢磨）。",
        "sentences": [
            ("如果咱想出去学化妆课的话，我觉得可以先不用去。",
             "If you're thinking about taking a makeup class, I'd say you can hold off for now.",
             "take a makeup class（上化妆课）；hold off（先缓一缓，比 wait 更口语）"),
            ("这条视频想讲清楚的，是化妆的基本原理和所有步骤的顺序。",
             "What this video wants to make clear are the basic principles of makeup and the order of every step.",
             "make clear（讲清楚）；the order of steps（步骤顺序）"),
            ("鼓球完发现结果满意，就不用去上课了；要是还差点事，再花钱上化妆课也不迟。",
             "Try it first — if you're happy with the result, skip the class; if it's still lacking, you can always pay for a class later.",
             "鼓球＝东北口语「琢磨/试试」，译成 try it first；it's still lacking（还差点事）"),
        ],
        "paraphrase": [
            ("别急着报名 → hold off for now / there's no rush to sign up", "hold off · no rush · sign up for"),
            ("试完结果满意 → happy with the result / satisfied with how it turns out", "happy with · how it turns out"),
            ("还差点事 → it's still lacking / it falls short / there's room to improve", "falls short · room to improve"),
        ],
        "speak": "If you're thinking about taking a makeup class, I'd say you can hold off for now. What this video wants to make clear are the basic principles of makeup and the order of every step. Try it first — if you're happy with the result, skip the class; if it's still lacking, you can always pay for a class later.",
    },
    {
        "id": "s2", "title_cn": "底妆前准备：毛发清理 + 皮肤清洁 + 去死皮",
        "title_en": "Prep: Facial Hair, Cleansing & Exfoliating",
        "time": "00:41–02:00", "context": "化妆第一步是清理面部毛发和油脂灰尘死皮，消除粉底和脸之间的「隔层」。语域：教程口播，步骤讲解。",
        "sentences": [
            ("首先化妆的第一步，就是把脸上的毛发清理一下。",
             "The very first step of makeup is clearing the facial hair.",
             "clear the facial hair（清理毛发），比 remove hair 更口语"),
            ("尤其小胡子这块，隔着毛上粉底会发青。",
             "Especially the upper-lip area — if you apply foundation over the hair, that patch turns bluish.",
             "upper-lip area（小胡子区域）；turns bluish（发青）"),
            ("顺着毛茬刮，别逆向刮伤自己。",
             "Shave along the grain — don't go against it and cut yourself.",
             "along the grain（顺着毛茬）；against the grain（逆向）"),
            ("拿化妆棉蘸化妆水，顺着皮肤纹路把油脂灰尘全擦下去。",
             "Take a cotton pad dipped in toner and wipe along the skin's texture to sweep away oil and dust.",
             "cotton pad dipped in toner（化妆棉蘸化妆水）；sweep away（擦下去）"),
            ("鼻翼两边死皮硬，就湿敷泡软再轻轻带下来。",
             "If the dead skin around your nostrils is tough, press on a wet pad to soften it, then gently sweep it off.",
             "dead skin（死皮）；soften（泡软）；sweep it off（带下来）"),
        ],
        "paraphrase": [
            ("顺着毛茬 → along the grain / with the direction the hair grows", "along the grain · direction the hair grows"),
            ("用化妆棉擦 → sweep it away with a cotton pad / wipe it off with toner", "cotton pad · sweep away"),
            ("把死皮泡软 → soften it with a wet compress / let it soak until soft", "wet compress · soak until soft"),
        ],
        "speak": "The very first step of makeup is clearing the facial hair. Especially the upper-lip area — if you apply foundation over the hair, that patch turns bluish. Shave along the grain, don't go against it and cut yourself. Take a cotton pad dipped in toner and wipe along the skin's texture to sweep away oil and dust. If the dead skin around your nostrils is tough, press on a wet pad to soften it, then gently sweep it off.",
    },
    {
        "id": "s3", "title_cn": "补水 + 锁水：两个动作分开做",
        "title_en": "Hydrate & Lock In: Two Separate Steps",
        "time": "02:00–03:17", "context": "喷雾、水、精华负责补水，面霜、乳液负责锁水。只补水不锁水，水一蒸发还是干、起皮。语域：教程口播，原理讲解。",
        "sentences": [
            ("水、喷雾、精华的作用都是补水，面霜或乳液的作用就是锁水。",
             "Water, mist, and essence hydrate; cream and lotion lock the moisture in.",
             "hydrate（补水）；lock in moisture（锁水）"),
            ("只补水不锁水，水一蒸发，脸还是干、起皮。",
             "If you only hydrate but don't lock it in, the water evaporates and your face ends up dry and flaky again.",
             "evaporate（蒸发）；dry and flaky（干、起皮）"),
            ("等完全吸收了，再来下一遍。",
             "Wait until it's fully absorbed before applying the next layer.",
             "fully absorbed（完全吸收）；next layer（下一遍）"),
        ],
        "paraphrase": [
            ("补水 → hydrate / replenish moisture / add moisture to the skin", "hydrate · replenish moisture"),
            ("锁水 → lock in the moisture / seal it in / trap the moisture", "lock in · seal it in"),
            ("起皮 → dry and flaky / peeling / getting scaly", "flaky · peeling"),
        ],
        "speak": "Water, mist, and essence hydrate; cream and lotion lock the moisture in. If you only hydrate but don't lock it in, the water evaporates and your face ends up dry and flaky again. Wait until it's fully absorbed before applying the next layer.",
    },
    {
        "id": "s4", "title_cn": "防晒：用「印」不用「搓」，基本不搓泥",
        "title_en": "Sunscreen: Press, Don't Rub — No Pilling",
        "time": "03:18–04:39", "context": "夏天防晒必不可少。选乳液压的防晒，用粉扑往脸上「印」，手法上最大程度避免手指搓脸，就不容易搓泥。语域：教程口播，手法教学。",
        "sentences": [
            ("夏天防晒必不可少。",
             "Sunscreen is non-negotiable in summer.",
             "non-negotiable（必不可少），比 must-have 更有力度"),
            ("上防晒不用怕搓泥，找乳液压的防晒，拿粉扑往脸上「印」。",
             "Don't worry about pilling — pick a lotion-textured sunscreen and press it on with a puff.",
             "pilling（搓泥）；lotion-textured（乳液压）；press on（印）"),
            ("你不搓，它上哪搓泥去。",
             "No rubbing, no pilling — simple as that.",
             "rubbing（搓）；no pilling（不搓泥）"),
            ("防晒上完别急着叠东西，等它成膜之后再上。",
             "After sunscreen, don't rush to layer anything on; wait for it to set into a film first.",
             "set into a film（成膜）；layer on（叠加）"),
        ],
        "paraphrase": [
            ("搓泥 → pilling / it rolls off / it balls up", "pilling · rolls off"),
            ("用印不用搓 → press it on instead of rubbing / dab, don't rub", "press on · dab, don't rub"),
            ("等成膜 → let it set into a film / wait for it to dry down", "set into a film · dry down"),
        ],
        "speak": "Sunscreen is non-negotiable in summer. Don't worry about pilling — pick a lotion-textured sunscreen and press it on with a puff. No rubbing, no pilling, simple as that. After sunscreen, don't rush to layer anything on; wait for it to set into a film first.",
    },
    {
        "id": "s5", "title_cn": "底妆前遮瑕：按颜色对号入座",
        "title_en": "Pre-Base Concealer: Match the Color",
        "time": "04:40–07:25", "context": "底妆前遮瑕按瑕疵颜色处理：发青发黄用紫色提亮，发红用绿色遮瑕液，黑眼圈用三文鱼色少量多次。语域：教程口播，校色原理。",
        "sentences": [
            ("发青的地方用紫色提亮，发黄也用紫色点，发红用绿色遮瑕液。",
             "Bluish areas get purple to brighten, yellowish areas get purple dots too, and red areas get a green corrector.",
             "bluish/yellowish/reddish（发青/发黄/发红）；green corrector（绿色遮瑕液）"),
            ("手法是刷子铺开 + 粉扑压实。",
             "The technique is brush to spread, then puff to press.",
             "brush to spread（刷子铺开）；puff to press（粉扑压实）"),
            ("黑眼圈别想着遮得完全看不出，正面看基本看不见就够了。",
             "Don't expect to hide dark circles completely — it's enough if they're basically invisible from the front.",
             "dark circles（黑眼圈）；basically invisible（基本看不见）"),
            ("用三文鱼色，每次蘸一点点，少量多次，基本不会卡粉。",
             "Use a salmon shade — pick up just a tiny bit each time, apply a little often, and it won't cake.",
             "salmon shade（三文鱼色）；cake（卡粉）"),
        ],
        "paraphrase": [
            ("按颜色校色 → color correct by shade / neutralize the tone", "color correct · neutralize"),
            ("少量多次 → apply a little, often / build it up in thin layers", "a little, often · thin layers"),
            ("卡粉 → cake / get cakey / look patchy", "cake · cakey"),
        ],
        "speak": "Bluish areas get purple to brighten, yellowish areas get purple dots too, and red areas get a green corrector. The technique is brush to spread, then puff to press. Don't expect to hide dark circles completely — it's enough if they're basically invisible from the front. Use a salmon shade, pick up just a tiny bit each time, apply a little often, and it won't cake.",
    },
    {
        "id": "s6", "title_cn": "粉底液 + 定妆喷雾：第一笔落面中，由内向外",
        "title_en": "Foundation & Setting Spray: Start at the Center",
        "time": "07:26–08:30", "context": "遮瑕后上一层定妆喷雾像双面胶，把遮瑕和粉底粘在一起。粉底第一笔落面中，由内向外过渡到外轮廓。语域：教程口播，手法讲解。",
        "sentences": [
            ("遮瑕完后来一层定妆喷雾，像双面胶一样，把遮瑕和粉底液粘住。",
             "After concealing, add a layer of setting spray — like double-sided tape, it sticks the concealer and foundation together.",
             "setting spray（定妆喷雾）；double-sided tape（双面胶）"),
            ("粉底液第一笔落在面中，这条线掌握着里脸和外脸的分界线。",
             "The first stroke of foundation lands on the mid-face; that line holds the boundary between your inner and outer face.",
             "mid-face（面中）；boundary（分界线）"),
            ("由内向外一点点过渡到外轮廓，外轮廓粉少一点反而更立体。",
             "Blend outward bit by bit toward the outer contour — less foundation there actually looks more sculpted.",
             "blend outward（向外过渡）；outer contour（外轮廓）；sculpted（立体）"),
        ],
        "paraphrase": [
            ("第一笔落面中 → start with the mid-face / begin at the center of the face", "mid-face · begin at the center"),
            ("由内向外 → blend outward / work from the center out", "blend outward · work from the center"),
            ("更立体 → more sculpted / more dimensional / better defined", "sculpted · dimensional"),
        ],
        "speak": "After concealing, add a layer of setting spray — like double-sided tape, it sticks the concealer and foundation together. The first stroke of foundation lands on the mid-face; that line holds the boundary between your inner and outer face. Blend outward bit by bit toward the outer contour — less foundation there actually looks more sculpted.",
    },
    {
        "id": "s7", "title_cn": "骨相三件套：提亮 + 修容 + 腮红",
        "title_en": "The Bone-Structure Trio: Highlight, Contour, Blush",
        "time": "08:30–13:19", "context": "提亮、修容、腮红三者一组，都是为了塑造脸上的骨相。提亮要比粉底明显白，鼻影要有层次，腮红衔接外圈阴影和里圈提亮。语域：教程口播，原理讲解。",
        "sentences": [
            ("提亮、修容、腮红这三个东西放一起，都是为了塑造脸上的骨相。",
             "Highlight, blush, and contour work as a set — all of them sculpt the face's bone structure.",
             "highlight/contour/blush（提亮/修容/腮红）；bone structure（骨相）；sculpt（塑造）"),
            ("提亮一定要比粉底肉眼可见地白很多才行。",
             "Your highlight has to be visibly much whiter than your foundation.",
             "visibly whiter（肉眼可见地更白）"),
            ("鼻影要有层次，不是一条均匀的黑，深的地方在鼻根两侧，其他地方都是过渡。",
             "The nose shadow needs layers — not one flat dark stripe. The deepest color sits at the sides of the nose root; everywhere else is a smooth transition.",
             "nose shadow（鼻影）；nose root（鼻根）；smooth transition（过渡）"),
            ("外圈修容是黑的、里圈提亮是白的，中间这块空档用腮红衔接起来。",
             "The outer contour is dark, the inner highlight is light, and blush bridges the empty band in between.",
             "bridges（衔接），动词比 connect 更形象"),
        ],
        "paraphrase": [
            ("塑造骨相 → sculpt the bone structure / build up the facial structure / add dimension to the face", "sculpt · add dimension"),
            ("鼻影有层次 → layered nose shadow / graduated shading", "layered · graduated"),
            ("腮红衔接 → blush bridges the gap / blush ties the two together", "bridges · ties together"),
        ],
        "speak": "Highlight, blush, and contour work as a set — all of them sculpt the face's bone structure. Your highlight has to be visibly much whiter than your foundation. The nose shadow needs layers, not one flat dark stripe. The deepest color sits at the sides of the nose root; everywhere else is a smooth transition. The outer contour is dark, the inner highlight is light, and blush bridges the empty band in between.",
    },
    {
        "id": "s8", "title_cn": "散粉定妆 + 眼妆：眼皮一定要定，眼线填睫毛根",
        "title_en": "Setting Powder & Eye Makeup: Set the Lids, Line the Roots",
        "time": "13:20–18:38", "context": "定妆喷雾成膜后上散粉，眼皮一定要定妆，否则眼线晕染快。眼影刷具要选对，眼线用刀锋刷填睫毛根。语域：教程口播，手法讲解。",
        "sentences": [
            ("眼皮上面一定要用小刷子沾粉好好定妆，不然画完眼线晕染得特别快。",
             "Always set your eyelids well with a small brush and powder — otherwise your eyeliner smudges in no time.",
             "set（定妆）；smudge（晕染）"),
            ("蓬松的刷子适合大面积铺色，边缘自然；扁刺刷适合小范围加深。",
             "A fluffy brush is great for large-area blending with a soft edge; a flat, firm brush is for small-area deepening.",
             "fluffy brush（蓬松刷）；blending（铺色）；deepening（加深）"),
            ("眼线用刀锋刷，笔尖在睫毛根一填，眼睛一下就有神了。",
             "Use an angled brush for liner — fill right into the lash line, and your eyes instantly come alive.",
             "angled brush（刀锋刷）；lash line（睫毛根）；come alive（有神）"),
        ],
        "paraphrase": [
            ("眼皮定妆 → set your eyelids / powder the lids first", "set the eyelids · powder the lids"),
            ("晕染 → smudge / smears / blends away", "smudge · smears"),
            ("有神 → come alive / look more defined / pop", "come alive · pop"),
        ],
        "speak": "Always set your eyelids well with a small brush and powder — otherwise your eyeliner smudges in no time. A fluffy brush is great for large-area blending with a soft edge; a flat, firm brush is for small-area deepening. Use an angled brush for liner — fill right into the lash line, and your eyes instantly come alive.",
    },
    {
        "id": "s9", "title_cn": "睫毛 + 眉毛：窗户与窗帘",
        "title_en": "Lashes & Brows: The Window and the Curtains",
        "time": "18:39–21:44", "context": "眼睛是心灵之窗，睫毛是窗帘。睫毛打底从根部往上刷，假睫毛新手推荐免胶款，眉毛颜色跟发色走。语域：教程口播，类比教学。",
        "sentences": [
            ("眼睛是心灵的窗户，睫毛就是心灵的窗帘。",
             "The eyes are the window to the soul, and the lashes are the curtains.",
             "window to the soul（心灵之窗）"),
            ("睫毛打底一定要从睫毛根往上刷，从根部撸上去才定型。",
             "Lash primer must be brushed from the root upward — that's what actually sets the curl.",
             "lash primer（睫毛打底）；from the root upward（从根部往上）"),
            ("假睫毛新手最推荐免胶款，夹在离睫毛根三分之一处。",
             "For beginners I'd recommend glue-free falsies — clamp them about one-third from your lash root.",
             "glue-free falsies（免胶款假睫毛）；lash root（睫毛根）"),
            ("眉毛的颜色跟发色走，先填眉毛底下皮的色。",
             "Match your brow color to your hair color, and fill in the skin beneath the brows first.",
             "match ... to（跟…走）；fill in（填色）"),
        ],
        "paraphrase": [
            ("心灵之窗 → the window to the soul / the eyes as windows", "window to the soul"),
            ("推荐免胶款 → recommend the glue-free kind / go with glue-free / skip the glue", "glue-free · skip the glue"),
            ("跟发色走 → match your hair color / follow your hair color", "match to · follow"),
        ],
        "speak": "The eyes are the window to the soul, and the lashes are the curtains. Lash primer must be brushed from the root upward — that's what actually sets the curl. For beginners I'd recommend glue-free falsies — clamp them about one-third from your lash root. Match your brow color to your hair color, and fill in the skin beneath the brows first.",
    },
    {
        "id": "s10", "title_cn": "二次加深 + 提亮层次 + 口红收官",
        "title_en": "Deepening, Highlight Layering & Lipstick Finale",
        "time": "21:45–27:45", "context": "化妆是层层渲染，不是一步到位。三种提亮像大圈套小圈再套迷你圈，唇线笔的作用就是嘴唇修容。语域：教程口播，收尾总结。",
        "sentences": [
            ("化妆不是一步到位，而是头一遍来一点、再加深一点，一层层渲染。",
             "Makeup isn't a one-shot deal — you apply a little first, deepen it, and render it layer by layer.",
             "one-shot（一步到位）；render layer by layer（层层渲染）"),
            ("三种提亮的关系就像大圈套小圈、再套迷你圈。",
             "The three highlights work like a big circle, a small circle inside it, and a mini circle inside that.",
             "大圈套小圈 → circles within circles，译成 a small circle inside it"),
            ("唇线笔的作用就是嘴唇修容，把明显的唇缘分界线模糊掉，有扩唇效果。",
             "A lip liner acts as lip contouring — blur the obvious lip boundary, and it creates a fuller-lip effect.",
             "lip liner（唇线笔）；blur（模糊）；fuller-lip effect（扩唇效果）"),
        ],
        "paraphrase": [
            ("一步到位 → a one-shot deal / all in one go / done in a single pass", "one-shot · in one go"),
            ("层层渲染 → render it layer by layer / build it up gradually / keep layering", "layer by layer · keep layering"),
            ("扩唇效果 → a fuller-lip effect / makes lips look fuller", "fuller-lip · look fuller"),
        ],
        "speak": "Makeup isn't a one-shot deal — you apply a little first, deepen it, and render it layer by layer. The three highlights work like a big circle, a small circle inside it, and a mini circle inside that. A lip liner acts as lip contouring — blur the obvious lip boundary, and it creates a fuller-lip effect.",
    },
]

PRACTICE = [
    ("想说服朋友别急着花钱报课", "Don't rush into a paid class — try the free tutorial first and see how it goes."),
    ("跟姐妹解释遮瑕要少量多次", "Build the concealer up in thin layers instead of one thick blob."),
    ("提醒眼皮一定要定妆", "Never skip setting your eyelids, or the liner will smudge in no time."),
    ("描述口红的大圈套小圈叠涂", "Layer a redder shade on the inner lip for that circles-within-circles effect."),
]

PITFALLS = [
    ("The dead skin is very hard.",
     "The dead skin around my nostrils is really tough.",
     "tough 比 hard 更贴合肤质描述，dead skin 是固定搭配（死皮）。"),
    ("Press the sunscreen on my face.",
     "Press the sunscreen into my face.",
     "press ... into 表示「按压进去」，比 on 更自然；on 有「按在表面」的歧义。"),
    ("My makeup is very dirty.",
     "My contour looks muddy.",
     "说妆容「脏」指修容不干净，用 muddy（脏浊）；very dirty 太笼统且不像化妆语境。"),
    ("I draw my eyeliner every day.",
     "I line my eyes every day.",
     "line 是化妆语境「画眼线」的地道动词，draw 偏绘画语境。"),
]

SHIFTS = [
    ("只会用 makeup 指代一切", "用 foundation / concealer / contour / liner / lash primer / setting spray 等精准名词"),
    ("说动作只会 apply", "按手法选词：press on（印）、dab（点）、sweep（扫）、blend（晕染）、fill in（填）、blur（模糊）"),
    ("说效果只会 good / bad", "用 sculpted（立体）、muddy（脏浊）、cakey（卡粉）、flaky（起皮）、smudged（晕染）、come alive（有神）"),
]

# 硬词表：化妆主题 ≥20
DIFFICULT_WORDS = [
    "non-negotiable", "lotion-textured", "concealer", "foundation", "sunscreen",
    "highlight", "contour", "bluish", "yellowish", "visibly", "sculpted",
    "dimensional", "transition", "boundary", "mid-face", "eyeliner", "eyelid",
    "eyelashes", "mascara", "primer", "smudge", "smudges", "flaky", "pilling",
    "double-sided", "absorbed", "evaporates", "sponge", "blending", "deepening",
]


def estimate_duration(char_count: int) -> str:
    minutes = char_count / 280
    low = max(1, int(minutes))
    high = max(low, int(minutes + 0.99))
    if low == high:
        return f"约 {low} 分钟"
    return f"约 {low} 到 {high} 分钟"


def build_narration_script(meta: dict, scenes: list[dict]) -> str:
    parts: list[str] = []
    total = len(scenes)
    parts.append(
        f"欢迎收听场景英译语音讲解。今天我们要学习的视频是「{meta['title']}」，"
        f"英文副标题：{meta['title_en']}。"
        f"视频总长{meta['duration']}，共分为{total}个场景、{meta['sentences']}句核心英文表达。"
        f"好，我们开始。"
    )
    for i, scene in enumerate(scenes, 1):
        cn = scene["title_cn"]
        en = scene["title_en"]
        time = scene["time"]
        parts.append(
            f"第{i}个场景，{cn}，{en}。时间范围{time}。请听场景完整英文："
        )
        parts.append(scene["speak"])
        if i < total:
            parts.append("好，进入下一个场景。")
    parts.append("下面是今日可练环节，请听完中文意图后尝试说出英文。")
    practice_prompts = [
        "第一题：想说服朋友别急着花钱报课。",
        "第二题：跟姐妹解释遮瑕要少量多次。",
        "第三题：提醒眼皮一定要定妆。",
        "第四题：描述口红的大圈套小圈叠涂。",
    ]
    for i, (prompt, english) in enumerate(zip(practice_prompts, PRACTICE)):
        parts.append(prompt)
        parts.append(english[1] if isinstance(english, tuple) else english)
    parts.append(
        "讲解完毕。建议回到网页查看完整逐句中英对照与表达提示，跟着朗读按钮反复练习。祝学习顺利！"
    )
    return "\n\n".join(p.strip() for p in parts if p.strip())


def split_text(text: str, max_len: int = MAX_CHUNK_LEN) -> list[str]:
    if len(text) <= max_len:
        return [text]
    chunks: list[str] = []
    current = ""
    for para in text.split("\n\n"):
        if len(para) > max_len:
            if current:
                chunks.append(current.strip())
                current = ""
            for i in range(0, len(para), max_len):
                chunks.append(para[i : i + max_len])
            continue
        candidate = f"{current}\n\n{para}".strip() if current else para
        if len(candidate) <= max_len:
            current = candidate
        else:
            if current:
                chunks.append(current.strip())
            current = para
    if current:
        chunks.append(current.strip())
    return chunks


async def _synthesize_chunk(text: str, output: Path, voice: str) -> None:
    import edge_tts
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(output))


def _concat_mp3(files: list[Path], output: Path) -> None:
    list_file = output.parent / f".concat_{output.stem}.txt"
    try:
        with open(list_file, "w", encoding="utf-8") as f:
            for p in files:
                f.write(f"file '{p.resolve()}'\n")
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
             "-c", "copy", str(output)],
            check=True, capture_output=True,
        )
    finally:
        if list_file.exists():
            list_file.unlink()


async def synthesize_speech(text: str, output_path: Path, voice: str) -> bool:
    chunks = split_text(text)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if len(chunks) == 1:
        await _synthesize_chunk(chunks[0], output_path, voice)
        return output_path.exists()
    temp_files: list[Path] = []
    try:
        for i, chunk in enumerate(chunks):
            tmp = output_path.parent / f".tmp_{output_path.stem}_{i}.mp3"
            await _synthesize_chunk(chunk, tmp, voice)
            temp_files.append(tmp)
        _concat_mp3(temp_files, output_path)
        return output_path.exists()
    finally:
        for f in temp_files:
            if f.exists():
                f.unlink()


async def generate_scene_mp3(scene: dict) -> bool:
    out = AUDIO_DIR / f"{scene['id']}.mp3"
    if out.exists():
        print(f"  (skip) scene {scene['id']}")
        return True
    ok = await synthesize_speech(scene["speak"], out, EN_VOICE)
    print(f"  {'✓' if ok else '✗'} scene {scene['id']}")
    return ok


async def generate_sentence_mp3(scene_id: str, idx: int, text: str) -> bool:
    out = AUDIO_DIR / f"{scene_id}-{idx:02d}.mp3"
    if out.exists():
        return True
    return await synthesize_speech(text, out, EN_VOICE)


async def generate_practice_mp3(idx: int, text: str) -> bool:
    out = AUDIO_DIR / f"practice-{idx}.mp3"
    if out.exists():
        print(f"  (skip) practice-{idx}")
        return True
    ok = await synthesize_speech(text, out, EN_VOICE)
    print(f"  {'✓' if ok else '✗'} practice-{idx}")
    return ok


async def generate_narration() -> bool:
    script = build_narration_script(META, SCENES)
    out_mp3 = AUDIO_DIR / "narration.mp3"
    out_txt = AUDIO_DIR / "narration.txt"
    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    if out_mp3.exists():
        print("  (skip) narration.mp3")
    else:
        ok = await synthesize_speech(script, out_mp3, ZH_VOICE)
        if not ok:
            print("  ✗ FAIL narration.mp3")
            return False
        print("  ✓ narration.mp3")
    out_txt.write_text(script, encoding="utf-8")
    print(f"  ✓ narration.txt ({len(script)} 字)")
    return True


def build_html() -> str:
    # --- Hero ---
    hero = f"""<header class="hero">
    <div class="hero-inner">
      <div class="hero-flex">
        <img class="hero-cover" src="{IMG}/shot-01.jpg" alt="{META['title']} 封面" loading="lazy">
        <div class="hero-text">
          <p class="eyebrow">Scene English · 化妆教程</p>
          <h1>{META['title']}</h1>
          <p class="hero-en">{META['title_en']}</p>
          <div class="hero-meta"><span class="chip">2026-08-07</span><span class="chip">小红书</span><span class="chip">{META['duration']}</span><span class="chip">{META['scenes']} 个场景</span><span class="chip">点下划线单词听发音</span><a class="source-link" href="http://xhslink.cn/o/9TtjHs4NiCD" target="_blank" rel="noopener">查看原视频 ↗</a><a class="source-link lang-switch" href="makeup-class-prep-图文实录.html" hreflang="zh" style="margin-left:12px;font-size:.8rem">中文图文实录版 ↗</a></div>
        </div>
      </div>
      <div class="toolbar"><label for="speech-rate">朗读速度</label><select id="speech-rate"><option value="0.85">慢速 0.85×</option><option value="1" selected>正常 1×</option><option value="1.15">快速 1.15×</option></select><button id="stop-speech" class="stop-btn" type="button">■ 停止朗读</button><span id="speech-status" class="speech-status" role="status" aria-live="polite"></span></div>
      <div class="narration-player"><p class="audio-label">🎧 语音讲解</p><button class="speak-btn" type="button" data-audio="audio/makeup-class-prep/narration.mp3" aria-label="播放语音讲解"><span aria-hidden="true">▶</span><span>播放语音讲解</span></button></div>
    </div>
  </header>"""

    # --- 场景地图 ---
    map_links = []
    for i, s in enumerate(SCENES, 1):
        map_links.append(
            f'<a class="map-link" href="#{s["id"]}"><span class="map-id">S{i}</span>'
            f'<span><b>{s["title_cn"]}</b><small>{s["time"]} · {s["title_en"]}</small></span></a>'
        )
    sidebar = (
        '<aside class="sidebar" aria-label="场景地图"><div class="sidebar-box">'
        f'<h2>场景地图 · SCENE MAP</h2><nav class="map-nav">{"".join(map_links)}</nav></div></aside>'
    )

    # --- 场景卡片 ---
    cards = []
    for i, s in enumerate(SCENES, 1):
        img_name = SCENE_IMG[i - 1]
        sentences_html = []
        for j, (zh, en, note) in enumerate(s["sentences"], 1):
            sentences_html.append(
                f'<article class="sentence"><div class="sentence-no">{j:02d}</div>'
                '<div class="bilingual">'
                '<div class="lang-block zh-block"><span class="lang-tag">中文</span>'
                f'<p>{zh}</p></div>'
                '<div class="lang-block en-block"><div class="en-head"><span class="lang-tag">EN</span>'
                f'<button class="speak-btn compact" type="button" data-audio="audio/makeup-class-prep/{s["id"]}-{j:02d}.mp3" aria-label="朗读本句">'
                '<span aria-hidden="true">▶</span><span>朗读本句</span></button></div>'
                f'<p class="english">{en}</p></div></div>'
                f'<p class="note"><span>表达提示</span>{note}</p></article>'
            )
        para_items = "".join(
            f'<li><p>{p}</p><div class="chunks">{c}</div></li>'
            for p, c in s["paraphrase"]
        )
        cards.append(
            f'<section class="scene-card" id="{s["id"]}" data-scene>'
            '<div class="scene-topline"><div>'
            f'<span class="scene-id">S{i}</span><span class="time">{s["time"]}</span></div>'
            f'<button class="speak-btn scene-speak" type="button" data-audio="audio/makeup-class-prep/{s["id"]}.mp3" aria-label="朗读整个场景">'
            '<span aria-hidden="true">▶</span><span>朗读整个场景</span></button></div>'
            f'<img class="scene-frame" src="{IMG}/{img_name}.jpg" alt="{s["title_cn"]} 场景截图" loading="lazy">'
            f'<h2>{s["title_cn"]}</h2>'
            f'<p class="scene-title-en">{s["title_en"]}</p>'
            f'<p class="context"><b>情境</b>{s["context"]}</p>'
            f'<div class="sentence-list">{"".join(sentences_html)}</div>'
            f'<details class="paraphrase"><summary>Paraphrase &amp; Chunks <span>{len(s["paraphrase"])} 组表达</span></summary>'
            f'<ol>{para_items}</ol></details>'
            "</section>"
        )

    # --- 今日可练 ---
    practice_items = "".join(
        f'<article><p>{zh}</p><div class="practice-en">{en} '
        f'<button class="speak-btn icon-only" type="button" data-audio="audio/makeup-class-prep/practice-{i}.mp3" aria-label="朗读练习句">'
        '<span aria-hidden="true">▶</span><span>朗读练习句</span></button></div></article>'
        for i, (zh, en) in enumerate(PRACTICE)
    )
    practice_section = (
        '<section class="study-section" id="practice"><h2 class="section-heading">今日可练 <small>PRACTICE TODAY</small></h2>'
        f'<div class="study-grid">{practice_items}</div></section>'
    )

    # --- 避坑 ---
    pit_items = "".join(
        f'<article><div class="wrong">✕ {wrong}</div><div class="right">✓ {right}</div><p>{why}</p></article>'
        for wrong, right, why in PITFALLS
    )
    pitfalls_section = (
        '<section class="study-section pitfalls" id="pitfalls"><h2 class="section-heading">避坑 <small>PITFALLS</small></h2>'
        f'<div class="study-grid">{pit_items}</div></section>'
    )

    # --- 认知转变 ---
    shift_items = "".join(
        f'<article><span>{a}</span><b aria-hidden="true">→</b><strong>{b}</strong></article>'
        for a, b in SHIFTS
    )
    shifts_section = (
        '<section class="study-section shifts" id="mindset"><h2 class="section-heading">认知转变 <small>MINDSET SHIFTS</small></h2>'
        f'<div class="study-grid">{shift_items}</div></section>'
    )

    footer = (
        "<footer>ASR 专有名词已按语境校正（鼓球→琢磨/试试、小胡子→上唇、睫毛根→lash line、刀锋刷→angled brush 等）"
        " · 场景/句子朗读使用 edge-tts 神经网络语音 · 单词发音使用浏览器 Web Speech API</footer>"
    )

    difficult_words = ", ".join(repr(w) for w in DIFFICULT_WORDS)

    js = f"""(() => {{
    let activeAudio = null;
    let activeBtn = null;
    const status = document.getElementById('speech-status');
    const stopBtn = document.getElementById('stop-speech');
    const rateSel = document.getElementById('speech-rate');
    const reset = () => {{ if (activeAudio) {{ activeAudio.pause(); activeAudio = null; }} activeBtn?.classList.remove('playing'); activeBtn = null; stopBtn.classList.remove('visible'); status.textContent = ''; }};
    const playAudio = (url, btn) => {{ reset(); const a = new Audio(url); a.playbackRate = Number(rateSel.value); activeAudio = a; activeBtn = btn; btn.classList.add('playing'); stopBtn.classList.add('visible'); status.textContent = btn.classList.contains('scene-speak') ? '正在朗读整个场景…' : btn.classList.contains('speak-btn') && btn.dataset.audio.includes('narration') ? '正在播放语音讲解…' : '正在朗读…'; a.onended = () => {{ if (activeAudio === a) reset(); }}; a.onerror = () => {{ status.textContent = '音频加载失败'; if (activeAudio === a) reset(); }}; a.play().catch(() => {{ status.textContent = '播放失败'; if (activeAudio === a) reset(); }}); }};
    document.addEventListener('click', e => {{ const btn = e.target.closest('[data-audio]'); if (!btn) return; e.preventDefault(); if (btn === activeBtn && activeAudio) {{ reset(); return; }} playAudio(btn.dataset.audio, btn); }});
    stopBtn.addEventListener('click', reset);
    const synth = window.speechSynthesis;
    const getEnglishVoice = () => {{ const v = synth.getVoices(); return v.find(x => /^en-(US|GB)/i.test(x.lang)) || v.find(x => /^en/i.test(x.lang)) || null; }};
    const difficultWords = new Set([{difficult_words}]);
    const shouldPronounce = w => {{ const n = w.toLowerCase().replace(/^[^a-z]+|[^a-z]+$/g,''); return n.replace(/[^a-z]/g,'').length >= 8 || difficultWords.has(n); }};
    const mark = root => {{ const w = document.createTreeWalker(root, NodeFilter.SHOW_TEXT); const ns = []; while (w.nextNode()) ns.push(w.currentNode); ns.forEach(n => {{ if (n.parentElement?.closest('button,script,style')) return; let m,l=0,ch=false; const fg = document.createDocumentFragment(); const re = /[A-Za-z]+(?:[-'’][A-Za-z]+)*/g; while ((m = re.exec(n.nodeValue))) {{ if (!shouldPronounce(m[0])) continue; ch=true; fg.append(n.nodeValue.slice(l,m.index)); const b=document.createElement('button');b.type='button';b.className='pronounce-word';b.dataset.speak=m[0];b.setAttribute('aria-label','朗读单词 '+m[0]);b.title='点击听 '+m[0]+' 发音';b.textContent=m[0];fg.append(b);l=m.index+m[0].length;}} if(!ch)return;fg.append(n.nodeValue.slice(l));n.replaceWith(fg);}}); }};
    document.querySelectorAll('.english,.scene-title-en,.paraphrase li p,.chunks,.practice-en,.wrong,.right').forEach(mark);
    document.addEventListener('click', e => {{ const wb = e.target.closest('.pronounce-word'); if (!wb) return; e.preventDefault(); if (!synth) return; synth.cancel(); if (activeAudio) {{ activeAudio.pause(); activeAudio = null; }} activeBtn?.classList.remove('playing'); activeBtn=wb; wb.classList.add('playing'); const u=new SpeechSynthesisUtterance(wb.dataset.speak);u.lang='en-US';u.rate=0.88;const v=getEnglishVoice();if(v)u.voice=v;u.onend=()=>{{activeBtn?.classList.remove('playing');activeBtn=null;}};u.onerror=()=>{{activeBtn?.classList.remove('playing');activeBtn=null;}};synth.speak(u); }});
  }})();"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <meta name="description" content="{META['title']}视频场景英译学习卡" />
  <title>{META['title']}｜场景英译</title>
  <style>{CSS}</style>
</head>
<body>
  {hero}
  <main class="page">
    {sidebar}
    <div class="content">
      {"".join(cards)}
      {practice_section}
      {pitfalls_section}
      {shifts_section}
      {footer}
    </div>
  </main>
  <script>{js}</script>
</body>
</html>"""
    return html


CSS = """:root {
  --teal-950:#073f42; --teal-800:#0d686c; --teal-700:#0f7c80; --teal-600:#14919b;
  --mint-100:#dff4ec; --mint-50:#f0faf6; --ink:#183536; --muted:#607879;
  --line:#d7e8e2; --paper:#fff; --amber:#a85d08; --shadow:0 12px 32px rgba(7,63,66,.08);
}
* { box-sizing:border-box; }
html { scroll-behavior:smooth; scroll-padding-top:24px; }
body { margin:0; color:var(--ink); background:#edf7f2; font-family:Inter,"PingFang SC","Noto Sans SC","Microsoft YaHei",system-ui,sans-serif; line-height:1.65; }
button, select { font:inherit; }
a { color:inherit; }
.hero { color:#fff; background:radial-gradient(circle at 85% 10%,rgba(129,230,196,.24),transparent 30%),linear-gradient(125deg,#073f42,#0d7377 56%,#14919b); }
.hero-inner { width:min(1440px,100%); margin:auto; padding:48px clamp(20px,5vw,72px) 42px; }
.hero-flex { display:flex; gap:clamp(18px,3vw,40px); align-items:flex-start; }
.hero-cover { width:min(240px,42vw); height:auto; max-height:320px; object-fit:contain; object-position:center; border-radius:16px; border:1px solid rgba(255,255,255,.28); box-shadow:0 18px 44px rgba(0,0,0,.32); flex-shrink:0; }
.hero-text { min-width:0; flex:1; }
.eyebrow { margin:0 0 12px; font-size:.78rem; font-weight:800; letter-spacing:.14em; text-transform:uppercase; opacity:.8; }
h1 { max-width:1020px; margin:0; font-size:clamp(1.8rem,3.8vw,3.2rem); line-height:1.13; letter-spacing:-.04em; }
.hero-en { margin:12px 0 24px; font-size:clamp(1rem,2vw,1.3rem); opacity:.82; }
.hero-meta { display:flex; flex-wrap:wrap; gap:9px; align-items:center; }
.chip { border:1px solid rgba(255,255,255,.28); border-radius:99px; padding:5px 11px; font-size:.82rem; background:rgba(255,255,255,.08); }
.source-link { font-weight:750; text-decoration:none; border-bottom:1px solid rgba(255,255,255,.5); }
.toolbar { display:flex; flex-wrap:wrap; gap:10px; align-items:center; margin-top:24px; }
.toolbar label { font-size:.82rem; opacity:.82; }
.toolbar select { color:#fff; background:#0a5d61; border:1px solid rgba(255,255,255,.3); border-radius:8px; padding:7px 9px; }
.stop-btn { display:none; color:#fff; background:#8c3b2a; border:0; border-radius:8px; padding:8px 12px; cursor:pointer; }
.stop-btn.visible { display:inline-flex; }
.speech-status { min-height:1.4em; font-size:.82rem; opacity:.88; }
.narration-player { margin-top:18px; padding:16px 18px; background:rgba(255,255,255,.1); border-radius:12px; border:1px solid rgba(255,255,255,.15); }
.audio-label { color:rgba(255,255,255,.88); font-size:.82rem; font-weight:700; margin:0 0 8px; }
.page { width:min(1440px,100%); margin:auto; padding:28px clamp(16px,3vw,44px) 64px; display:grid; grid-template-columns:minmax(230px,280px) minmax(0,1fr); gap:30px; align-items:start; }
.sidebar { position:sticky; top:20px; min-width:0; }
.sidebar-box { background:rgba(255,255,255,.8); border:1px solid var(--line); border-radius:16px; padding:17px; box-shadow:var(--shadow); backdrop-filter:blur(12px); }
.sidebar h2 { margin:0 0 13px; font-size:.9rem; letter-spacing:.08em; color:var(--teal-800); }
.map-link { display:grid; grid-template-columns:34px minmax(0,1fr); gap:9px; padding:10px 6px; text-decoration:none; border-top:1px solid var(--line); }
.map-link:hover b { color:var(--teal-700); }
.map-id { width:30px; height:30px; display:grid; place-items:center; border-radius:9px; color:#fff; background:var(--teal-700); font-size:.72rem; font-weight:800; }
.map-link b { display:block; font-size:.78rem; line-height:1.4; }
.map-link small { display:block; color:var(--muted); font-size:.67rem; line-height:1.4; margin-top:2px; overflow-wrap:anywhere; }
.content { min-width:0; }
.scene-card { background:var(--paper); border:1px solid var(--line); border-radius:20px; padding:clamp(20px,3vw,34px); margin-bottom:24px; box-shadow:var(--shadow); overflow:hidden; }
.scene-frame { display:block; width:100%; max-height:480px; object-fit:contain; object-position:center; background:rgba(7,63,66,.04); border-radius:14px; margin:16px 0 4px; border:1px solid var(--line); box-shadow:0 10px 28px rgba(7,63,66,.1); }
.scene-topline { display:flex; justify-content:space-between; gap:16px; align-items:center; }
.scene-id { display:inline-grid; place-items:center; min-width:42px; height:30px; padding:0 10px; color:#fff; background:var(--teal-700); border-radius:8px; font-size:.78rem; font-weight:850; }
.time { margin-left:10px; color:var(--muted); font-size:.82rem; font-variant-numeric:tabular-nums; }
.scene-card h2 { margin:18px 0 2px; font-size:clamp(1.35rem,2.4vw,2rem); line-height:1.25; color:var(--teal-950); }
.scene-title-en { margin:0 0 18px; color:var(--teal-600); font-weight:700; font-size:.98rem; }
.context { margin:0 0 20px; padding:12px 15px; color:#496566; background:var(--mint-50); border-left:3px solid var(--teal-600); border-radius:0 10px 10px 0; font-size:.88rem; }
.context b { margin-right:10px; color:var(--teal-800); }
.sentence-list { display:grid; gap:12px; }
.sentence { position:relative; display:grid; grid-template-columns:38px minmax(0,1fr); gap:12px; padding:16px; border:1px solid #e2ece8; border-radius:14px; background:#fcfefd; min-width:0; }
.sentence-no { color:var(--teal-600); font-size:.76rem; font-weight:850; font-variant-numeric:tabular-nums; padding-top:4px; }
.bilingual { min-width:0; display:grid; grid-template-columns:minmax(0,1fr) minmax(0,1fr); gap:clamp(14px,2vw,28px); }
.lang-block { min-width:0; }
.lang-block p { margin:5px 0 0; overflow-wrap:anywhere; }
.en-block { padding-left:clamp(14px,2vw,28px); border-left:1px solid var(--line); }
.en-block p { color:#0b5c60; font-weight:650; }
.lang-tag { display:inline-block; color:var(--muted); font-size:.66rem; font-weight:850; letter-spacing:.12em; }
.en-head { display:flex; justify-content:space-between; gap:10px; align-items:center; min-height:30px; }
.note { grid-column:2; margin:1px 0 0; color:#708182; font-size:.78rem; }
.note span { margin-right:7px; color:var(--amber); font-weight:750; }
.speak-btn { display:inline-flex; align-items:center; gap:7px; border:1px solid #b8d9d1; border-radius:9px; padding:7px 11px; color:var(--teal-800); background:#f5fbf8; cursor:pointer; white-space:nowrap; font-size:.78rem; font-weight:750; transition:.15s ease; }
.speak-btn:hover { color:#fff; background:var(--teal-700); border-color:var(--teal-700); transform:translateY(-1px); }
.speak-btn.playing { color:#fff; background:var(--teal-700); border-color:var(--teal-700); }
.speak-btn.compact { padding:4px 8px; font-size:.7rem; }
.speak-btn.icon-only { padding:3px 7px; margin-left:6px; }
.speak-btn.icon-only span:last-child { display:none; }
.pronounce-word { display:inline; margin:0; padding:0 2px; color:inherit; background:rgba(20,145,155,.08); border:0; border-bottom:1px dashed var(--teal-600); border-radius:3px; font:inherit; font-weight:inherit; line-height:inherit; cursor:pointer; }
.pronounce-word:hover, .pronounce-word:focus { color:var(--teal-950); background:#cceee4; border-bottom-style:solid; outline:3px solid rgba(20,145,155,.42); outline-offset:2px; }
.pronounce-word.playing { color:#fff; background:var(--teal-700); border-bottom-color:var(--teal-700); }
.paraphrase { margin-top:18px; border-top:1px solid var(--line); }
.paraphrase summary { padding:16px 0 3px; color:var(--teal-800); cursor:pointer; font-weight:800; }
.paraphrase summary span { color:var(--muted); font-size:.75rem; font-weight:500; margin-left:8px; }
.paraphrase ol { margin:12px 0 0; padding-left:22px; }
.paraphrase li { padding:7px 0 9px 5px; }
.paraphrase li p { margin:0; font-size:.9rem; font-weight:650; }
.chunks { margin-top:4px; color:var(--teal-700); font-size:.78rem; }
.study-section { margin:38px 0 0; }
.section-heading { display:flex; align-items:baseline; gap:10px; margin:0 0 15px; color:var(--teal-950); font-size:1.35rem; }
.section-heading small { color:var(--teal-600); font-size:.78rem; letter-spacing:.05em; }
.study-grid { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:14px; }
.study-grid article { padding:17px; background:#fff; border:1px solid var(--line); border-radius:14px; box-shadow:0 6px 18px rgba(7,63,66,.05); min-width:0; }
.study-grid p { margin:0; }
.practice-en { margin-top:9px; color:var(--teal-700); font-weight:650; overflow-wrap:anywhere; }
.wrong { color:#a24831; text-decoration:line-through; overflow-wrap:anywhere; }
.right { color:var(--teal-700); font-weight:750; margin:5px 0; overflow-wrap:anywhere; }
.pitfalls p { color:var(--muted); font-size:.82rem; }
.shifts article { display:grid; grid-template-columns:minmax(0,1fr) auto minmax(0,1.5fr); gap:12px; align-items:center; }
.shifts b { color:var(--teal-600); font-size:1.2rem; }
.shifts strong { color:var(--teal-800); }
footer { margin-top:38px; color:var(--muted); font-size:.78rem; text-align:center; }
@media (max-width:900px) { .page { grid-template-columns:1fr; } .sidebar { position:static; } .sidebar-box { overflow-x:auto; padding:12px; } .sidebar h2 { padding-left:5px; } .map-nav { display:flex; width:max-content; gap:8px; } .map-link { width:220px; border:1px solid var(--line); border-radius:10px; padding:8px; } .bilingual { grid-template-columns:1fr; } .en-block { padding:12px 0 0; border-left:0; border-top:1px dashed var(--line); } }
@media (max-width:620px) { .hero-inner { padding-top:32px; } .hero-flex { flex-direction:column; align-items:center; } .hero-cover { width:100%; max-width:360px; } .hero-text { text-align:center; } .page { padding-inline:10px; gap:18px; } .scene-card { border-radius:14px; padding:17px 13px; } .scene-topline { align-items:flex-start; } .scene-speak span:last-child { display:none; } .sentence { grid-template-columns:26px minmax(0,1fr); padding:13px 10px; gap:6px; } .note { grid-column:2; } .study-grid { grid-template-columns:1fr; } .shifts article { grid-template-columns:1fr; gap:5px; } .shifts b { transform:rotate(90deg); justify-self:start; } }
@media (prefers-reduced-motion:reduce) { html { scroll-behavior:auto; } .speak-btn { transition:none; } }"""


def generate_manifest() -> dict:
    return {
        "slug": META["slug"],
        "scenes": len(SCENES),
        "sentences": sum(len(s["sentences"]) for s in SCENES),
        "scene_audio": [f"audio/{META['slug']}/{s['id']}.mp3" for s in SCENES],
        "sentence_audio": {
            f"{s['id']}-{i+1:02d}": f"audio/{META['slug']}/{s['id']}-{i+1:02d}.mp3"
            for s in SCENES for i in range(len(s["sentences"]))
        },
        "practice_audio": [f"audio/{META['slug']}/practice-{i}.mp3" for i in range(len(PRACTICE))],
        "narration": f"audio/{META['slug']}/narration.mp3",
    }


def main() -> None:
    from argparse import ArgumentParser
    parser = ArgumentParser(description="makeup-class-prep 场景英译学习卡")
    parser.add_argument("--audio-only", action="store_true", help="仅生成音频")
    parser.add_argument("--html-only", action="store_true", help="仅生成 HTML")
    args = parser.parse_args()

    if not args.html_only:
        total_sents = sum(len(s["sentences"]) for s in SCENES)
        print(f"📢 生成英文音频：{len(SCENES)} 场景 + {total_sents} 句 + {len(PRACTICE)} 练习")

        async def run_all() -> tuple[list[bool], list[bool], list[bool], bool]:
            scene_tasks = [generate_scene_mp3(s) for s in SCENES]
            sent_tasks = [
                generate_sentence_mp3(s["id"], i + 1, text)
                for s in SCENES for i, (_, text, _) in enumerate(s["sentences"])
            ]
            practice_tasks = [
                generate_practice_mp3(i, text) for i, (_, text) in enumerate(PRACTICE)
            ]
            scene_results = await asyncio.gather(*scene_tasks)
            sent_results = await asyncio.gather(*sent_tasks)
            practice_results = await asyncio.gather(*practice_tasks)
            narration_ok = await generate_narration()
            return scene_results, sent_results, practice_results, narration_ok

        scene_results, sent_results, practice_results, narration_ok = asyncio.run(run_all())
        print(f"  场景 {sum(scene_results)}/{len(SCENES)} | 逐句 {sum(sent_results)}/{total_sents} | 练习 {sum(practice_results)}/{len(PRACTICE)} | 旁白 {'✓' if narration_ok else '✗'}")
        manifest = generate_manifest()
        (AUDIO_DIR / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"  ✓ manifest.json")

    if not args.audio_only:
        html = build_html()
        OUT_HTML.write_text(html, encoding="utf-8")
        print(f"  ✓ HTML: {OUT_HTML.name} ({len(html)} bytes)")

    print("✓ 完成")


if __name__ == "__main__":
    main()
