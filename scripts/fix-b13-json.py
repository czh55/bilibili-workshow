#!/usr/bin/env python3
"""批13：将简化场景JSON补全为 gen-scene-en.py 所需的完整结构。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "3lylv6dlQPz": {
        "duration": "0:57", "topic": "AIGC · AI提示词控光",
        "practice": [
            ["说光的方向", "Describe where the light enters the frame."],
            ["说光的比例", "Tell AI exactly which parts are bright and dark."],
            ["说光的色温", "Interweave cool and warm light for emotion."],
            ["说综合提示词", "Add direction, ratio, and temperature in one prompt."]
        ],
        "pitfalls": [
            ["Write only cinematic lighting.",
             "Specify the light direction and entry angle.",
             "影视灯光太笼统，AI不知道光从哪来。"],
            ["Let AI fill the frame bright.",
             "State exactly where's bright and where's dark.",
             "AI默认全亮，要明确光影比例才有对比。"],
            ["Ignore color temperature.",
             "Use cool-warm contrast for mood.",
             "色温是情绪，冷暖交错才不死板。"],
            ["Cram every effect into one prompt.",
             "Combine direction, ratio, and temperature coherently.",
             "方向+光比+色温组合，逻辑要连贯。"]
        ],
        "shifts": [
            ["说光线只会说 light",
             "用 light source（光源）、entry direction（进场方向）、shadow layout（阴影布局）"],
            ["说真实只会说 real",
             "用 contrast（对比）、dimensional（立体）、texture（质感）"],
            ["说情绪只会说 mood",
             "用 color temperature（色温）、morning mist（晨雾）、midday heat（正午曝晒）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：控制光线、影视灯光、光的来源、进场方向、阴影布局、立体、质感、画面打得很满、哪里亮哪里暗、光影比例、亮暗对比、色温、情绪、清晨的雾、曝晒的风、冷暖交错、死板、免费提示词等。"
    },
    "6pWwRV85enC": {
        "duration": "2:08", "topic": "剪辑 · 视频封面设计",
        "practice": [
            ["说封面主角", "Make yourself the most important element."],
            ["说抠图方法", "Trace the edge in Procreate or use Apple cutout."],
            ["说视觉重点", "Keep only one visual focus on the cover."],
            ["说手绘字体", "I hand-draw every font on the cover."]
        ],
        "pitfalls": [
            ["Cram the cover with many elements.",
             "Keep one and only one visual focus.",
             "多个重点画面平均，视觉会乱。"],
            ["Use the default photo as-is.",
             "Cut out yourself and add a stroke.",
             "把自己抠出来加描边，才有个性。"],
            ["Chase hot trends for clicks.",
             "Stay consistent with your own style.",
             "盲目追热点会丢掉风格。"],
            ["Expect good covers overnight.",
             "Build aesthetic accumulation with daily practice.",
             "审美需要大量积累和练习。"]
        ],
        "shifts": [
            ["说封面只会说 cover",
             "用 poster design（海报设计）、collage（拼贴）、the hero element（主角元素）"],
            ["说设计只会说 design",
             "用 hand-drawn（手绘）、stroke（描边）、visual focus（视觉重点）"],
            ["说风格只会说 style",
             "用 convey emotion（传递情绪）、aesthetic practice（审美练习）、life-based learning（生活化学习）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：视频封面、海报设计、拼贴元素、排列组合、封面主角、情绪、夸张字体、平静表情、发言工作、背景元素、Procreate、手绘描线、苹果相册抠图、拷贝粘贴、关背景图层、描边、视觉重点、放大显眼、手绘字体、追热门、保持风格、审美积累、生活化学习等。"
    },
    "1pFUeLG0aMs": {
        "duration": "0:21", "topic": "拍摄 · 电影感",
        "practice": [
            ["说构图基础", "Follow the rule of thirds and leading lines."],
            ["说光线运用", "Use natural light direction for depth."],
            ["说调色思路", "Lower saturation and unify the tone."],
            ["说快速捷径", "Add black bars at a 2.35:1 aspect ratio."]
        ],
        "pitfalls": [
            ["Think cinematic equals expensive gear.",
             "Phone plus good techniques works too.",
             "电影感不在设备，在拍法与处理。"],
            ["Grading without composing well.",
             "Fix composition before touching color.",
             "好的调色救不了差的构图。"],
            ["Boost saturation for vibrancy.",
             "Lower saturation and unify the tone.",
             "降低饱和度统一色调才有电影感。"],
            ["Shoot in automatic mode.",
             "Observe light and compose layers consciously.",
             "拍摄前观察光，构图分层，是基本功。"]
        ],
        "shifts": [
            ["说电影感只会说 cinematic",
             "用 rule of thirds（三分法）、leading lines（引导线）、negative space（留白）"],
            ["说后期只会说 edit",
             "用 unify the tone（统一色调）、teal-orange（青橙调）、film look（胶片感）"],
            ["说高级只会说 high-end",
             "用 2.35:1 aspect（宽银幕画幅）、composition（构图）、layering（层次）"]
        ],
        "footer": "转录基于图文实录完整口播（口播极短，场景依据图文实录画面与SVG分析重构）。已校正：电影感、昂贵设备、手机拍摄、构图、光线、调色、三分法、引导线、留白、层次、青橙调、胶片感、饱和度、对比度、2.35:1画幅比等。"
    },
    "98ndLERsqZR": {
        "duration": "0:24", "topic": "设计 · 打破平淡",
        "practice": [
            ["说线条分割", "Split a plain image with a line."],
            ["说打破排版", "Slash the stiff layout for rhythm."],
            ["说冲出边界", "Push one element past the frame."],
            ["说打破标题", "Break the title's arrangement to pop."]
        ],
        "pitfalls": [
            ["Fix flatness by adding more.",
             "Ask what you can break instead.",
             "想加东西时先问能不能打破什么。"],
            ["Keep every element safely inside.",
             "Let a key element cross the boundary.",
             "关键元素冲出边界才有张力。"],
            ["Use random flashy decoration.",
             "Split, slash, and offset with purpose.",
             "分割、错位要有设计目的。"],
            ["Replace elements without thought.",
             "Swap dull elements for deeper ones.",
             "替换元素要引入深度与层次。"]
        ],
        "shifts": [
            ["说平淡只会说 boring",
             "用 flat（平淡）、stiff（呆板）、no design flair（缺设计感）"],
            ["说改只会说 change",
             "用 split（分割）、slash（划一刀）、break the grid（打破网格）"],
            ["说好看只会说 nice",
             "用 rhythm（节奏感）、breathing room（呼吸感）、depth（层次感）"]
        ],
        "footer": "转录基于图文实录完整口播（口播极短，场景依据图文实录画面与SVG分析重构）。已校正：画面平、排版呆板、线条分割、划一刀、冲出边界、打破标题、替换元素、节奏感、呼吸感、层次感、堆砌代替打破等。"
    },
    "3GYt9BIvxNk": {
        "duration": "2:14", "topic": "摄影 · 闪光灯与常亮灯",
        "practice": [
            ["说灯的类型", "Flash and continuous light are different classes."],
            ["说亮度选择", "Match the lamp to the environment brightness."],
            ["说附件优势", "Flash powers big modifiers like softboxes."],
            ["说凝固画面", "Flash freezes motion for sharper shots."],
            ["说色温调节", "Flash can use gels, LED mixes warm and cool."]
        ],
        "pitfalls": [
            ["Use continuous light in bright sun.",
             "Only flash can beat outdoor sunlight.",
             "外景阳光只有闪光灯压得住。"],
            ["Expect continuous light to power big modifiers.",
             "Flash's output affords deep umbrellas and softboxes.",
             "附件吃光严重，常亮灯亮度不够。"],
            ["Give up on flash at the learning hurdle.",
             "Push past it—playing with light is the biggest joy.",
             "跨过门槛，玩灯是摄影最大乐趣。"],
            ["Think continuous is better for stepless color temp.",
             "Flash gets stepless color temp on a trigger too.",
             "闪光灯在引闪器上也能无极调色温。"]
        ],
        "shifts": [
            ["说灯只会说 lamp",
             "用 flash（闪光灯）、continuous light（长亮灯）、speedlight（机顶灯）"],
            ["说亮度只会说 bright",
             "用 output（输出）、10,000-watt equivalent（一万瓦当量）、match the environment（匹配环境）"],
            ["说效果只会说 good",
             "用 instant freeze（瞬间凝固）、sharper（更锐利）、modifiers（光效附件）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：两个级别、机顶灯、一万瓦以上长亮灯、秒杀、愈强则强愈弱则弱、数量级、夜景补光灯、室内阴天树影、外景阳光、所见即所得、视频唯一选择、大型深抛、柔光箱、亮度削减、瞬间凝固性、锐度质感、发虚、学习门槛、最大乐趣、无极调节色温、绿色纸、冷暖灯珠、引闪器无极调色温等。"
    },
    "AlTQGzzbzqu": {
        "duration": "1:48", "topic": "摄影 · 全域快门压光",
        "practice": [
            ["说压光原理", "Underexpose the background so flash is the hero."],
            ["说参数设置", "Drop ISO, raise shutter to the sync limit, stop down."],
            ["说哈苏玩法", "The global shutter syncs at 1/2000s."],
            ["说对比优势", "No power loss like HSS, no quality loss like ND."]
        ],
        "pitfalls": [
            ["Meter the flash like a steady light.",
             "Underexpose the background first, then add flash.",
             "先压背景曝光，闪光灯再补主体。"],
            ["Use HSS and accept the power loss.",
             "Use the global shutter for full-power high-speed sync.",
             "全域快门超高快门不损失功率。"],
            ["Rely on ND filters in the sun.",
             "Global shutter keeps quality and power together.",
             "ND损失画质，全域快门双兼顾。"],
            ["Expect the same on any camera.",
             "This experience comes from the global shutter.",
             "只有全域快门能兼顾功率与画质。"]
        ],
        "shifts": [
            ["说压光只会说 fill flash",
             "用 extreme fill-flash（极致压光）、underexpose the background（压低背景）、the hero（主角）"],
            ["说快门只会说 shutter",
             "用 global shutter（全域快门）、sync speed（同步速度）、1/2000s（同步速度）"],
            ["说对比只会说 compare",
             "用 HSS power loss（高速同步功率损失）、ND quality loss（滤镜画质损失）、both preserved（双双兼顾）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：机顶闪光灯、哈苏、全域快门、1/2000秒同步、极致压光、压低背景曝光、ISO最低、同步速度上限、收小光圈、背景欠曝、ETTL、高速同步、f8、曝光补偿、深蓝天空、黑背景、电影感、ND滤镜、画质功率兼顾等。"
    },
    "5BHRuqng9CC": {
        "duration": "1:30", "topic": "摄影 · 闪光灯ND镜",
        "practice": [
            ["说慢快门+ND原理", "At 1/250s the flash burst is fully recorded."],
            ["说参数组合", "Mount ND64, ISO 100, shutter 1/250, f/1.4."],
            ["说对比高速同步", "ND keeps full power while HSS attenuates."],
            ["说适用范围", "Great for portraits, can't freeze motion."]
        ],
        "pitfalls": [
            ["Think ND blocks flash.",
             "ND only dims ambient, flash-lit areas stay bright.",
             "ND只压环境光，不影响闪光范围。"],
            ["Use HSS and accept power loss.",
             "1/250s plus ND keeps full flash power.",
             "慢快门加ND不衰减功率。"],
            ["Freeze motion with ND.",
             "The limit is 1/250s; fast action needs HSS.",
             "凝固瞬间受限于250分之一秒。"],
            ["Skip ND in bright sun.",
             "ND keeps wide apertures usable at noon.",
             "正午大光圈靠ND实现。"]
        ],
        "shifts": [
            ["说滤镜只会说 filter",
             "用 ND filter（中灰滤镜）、dim ambient（压暗环境光）"],
            ["说同步只会说 sync",
             "用 flash duration（闪光持续时间）、1/250s（同步速度）、HSS（高速同步）"],
            ["说效果只会说 good",
             "用 full power（满功率）、bokeh（虚化）、freeze motion（凝固瞬间）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：快门250或更慢、中灰滤镜、不是高速同步、不损失功率、闪光持续时间、ND压暗环境光、正午户外、大光圈、ND64、ISO100、f1.4、TTL、深色调、高速同步衰减、凝固瞬间等。"
    },
    "9CKTFgwoqQU": {
        "duration": "2:12", "topic": "摄影 · 闪光灯人像",
        "practice": [
            ["说第一步机身", "Turn on manual, black out the ambient light."],
            ["说第二步闪光", "Set TTL and adjust flash compensation."],
            ["说第三步后期", "Raise contrast, fix white balance, polish skin."],
            ["说核心思路", "Black base first, flash second."]
        ],
        "pitfalls": [
            ["Let ambient light control exposure.",
             "Crush the background to black as a baseline.",
             "相机只负责环境光，先压黑。"],
            ["Judge exposure by the camera screen alone.",
             "Check the flash-lit subject with a test frame.",
             "闪光灯只负责照亮主体。"],
            ["Skip the gray-tone normalization.",
             "Raise contrast and polish in post.",
             "偏灰正常，后期三步出片。"],
            ["Fight the flash learning curve.",
             "This method has a very low bar.",
             "先黑底再闪光，门槛极低。"]
        ],
        "shifts": [
            ["说闪光灯只会说 flash",
             "用 TTL（自动测光）、flash compensation（闪光补偿）"],
            ["说曝光只会说 exposure",
             "用 crush the ambient（压环境光）、black base（黑底）、M mode（M档）"],
            ["说后期只会说 edit",
             "用 raise contrast（提对比）、white balance（白平衡）、polish skin tone（润肤色）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：最好上手、零基础、M档、快门1/200秒、ISO100、f4、白墙测光、黑色画面、TTL、闪光补偿、主体曝光、偏灰、提高对比度、暗部扎实、白平衡、润色肤色、先黑底再闪光、互不干扰、举一反三等。"
    },
    "p4aiaGi6Wf": {
        "duration": "2:02", "topic": "摄影 · 灯光亮度对比",
        "practice": [
            ["说实验设置", "Set both lights to the same wattage."],
            ["说结果差距", "Flash is orders of magnitude brighter."],
            ["说人眼错觉", "Eyes auto-adapt, the camera meters physics."],
            ["说选购建议", "Video picks continuous, photos pick flash."]
        ],
        "pitfalls": [
            ["Judge light by how bright it looks.",
             "Meter physical light, not the eye's adaptation.",
             "相机看物理光量，人眼会自动适应。"],
            ["Expect video lights to fit photography.",
             "Same wattage flash dwarfs continuous in stills.",
             "拍视频够亮的灯，拍照会明显偏暗。"],
            ["Compare wattage as if equal.",
             "Flash dumps energy instantly, LED radiates steadily.",
             "同瓦数有效光量差几个数量级。"],
            ["Buy a light without a use case.",
             "Know your use: WYSIWYG or freeze power.",
             "先想用途再买灯。"]
        ],
        "shifts": [
            ["说亮度只会说 bright",
             "用 wattage（瓦数）、effective light（有效光量）、orders of magnitude（数量级）"],
            ["说感觉只会说 feel",
             "用 auto-adapt（自动适应）、physical light（物理光量）"],
            ["说选择只会说 choose",
             "用 WYSIWYG（所见即所得）、freeze power（凝固力）、use case（用途）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：同瓦数、实验、闪光灯基准、ISO100、快门1/200秒、持续发光、测光逻辑、瞬间释放能量、持续均匀发光、数量级、人眼适应、物理光量、拍视频够亮、拍照片暗、用途、所见即所得、画质光效、适不适合等。"
    },
    "aesthetic-inspire-gallery-1": {
        "duration": "图集", "topic": "摄影 · 审美启发",
        "practice": [
            ["说四维拆图", "Read composition, light, tone, and mood."],
            ["说精读方法", "Break down ten photos deeply, not a hundred."],
            ["说刻意练习", "Write your observations every day."],
            ["说时间复利", "Thirty days of practice upgrades your eye."]
        ],
        "pitfalls": [
            ["Collect images without studying them.",
             "Read ten images deeply instead.",
             "收藏一百张不如精读十张。"],
            ["Look at photos only for liking.",
             "Break them into composition, light, tone, mood.",
             "用四维框架拆解，不是只看喜不喜欢。"],
            ["Expect taste to grow by osmosis.",
             "Write down your observations deliberately.",
             "写下观察，刻意练习才有效。"],
            ["Copy without understanding.",
             "Imitate after you can read the structure.",
             "先看懂结构，再模仿。"]
        ],
        "shifts": [
            ["说好看只会说 beautiful",
             "用 composition（构图）、leading lines（引导线）、negative space（留白）"],
            ["说光线只会说 light",
             "用 hard or soft（硬柔光）、light direction（光向）、shadow（阴影）"],
            ["说看照片只会说 look at",
             "用 break down（拆解）、four-dimension framework（四维框架）、visual intuition（审美直觉）"]
        ],
        "footer": "转录基于图文实录完整口播（图集无口播，场景依据图文实录画面与SVG分析重构）。已校正：审美启发、图片画廊、构图、光线、色调、情绪、引导线、留白、硬柔光、冷暖对比、统一色系、饱和度、精读、四维框架、审美直觉、三十天等。"
    }
}

for slug, extra in EXTRA.items():
    p = DATA / f"{slug}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    scenes_in = d["scenes"]

    full_scenes = []
    for i, s in enumerate(scenes_in, 1):
        title_cn = s.get("scene_zh", "")
        if len(title_cn) > 18:
            title_cn = title_cn[:18] + "…"
        title_en = s.get("scene_en", "")
        if len(title_en) > 42:
            title_en = title_en[:42] + "…"
        sentences = s["sentences"]
        speak = " ".join(t[1] for t in sentences)
        paraphrase = []
        seen = set()
        for t in sentences:
            note = t[2]
            parts = [x.strip() for x in re.split(r"[（(]/", note) if x.strip()]
            if parts:
                key = parts[0].rstrip("）)")
                if key not in seen and len(key) <= 24:
                    paraphrase.append([key, key])
                    seen.add(key)
        if not paraphrase:
            paraphrase.append([sentences[0][2], sentences[0][2]])
        full_scenes.append({
            "id": s["id"],
            "title_cn": title_cn,
            "title_en": title_en,
            "time": s.get("time", "00:00"),
            "context": s.get("context", ""),
            "sentences": sentences,
            "paraphrase": paraphrase[:2],
            "speak": speak,
        })

    total_sents = sum(len(s["sentences"]) for s in full_scenes)
    words = []
    for s in full_scenes:
        for t in s["sentences"]:
            for m in re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*", t[1]):
                n = m.lower()
                if len(n) >= 6 and n not in words:
                    words.append(n)
    words = words[:30]
    if len(words) < 20:
        words = words + ["sample", "learning", "camera", "light", "shadow", "frame", "shoot", "angle", "focus", "setting"][: 20 - len(words)]

    out = {
        "meta": {
            "slug": slug,
            "title": d["title_zh"],
            "title_en": d["title_en"],
            "duration": extra["duration"],
            "scenes": len(full_scenes),
            "sentences": total_sents,
            "date": "2026-08-08",
            "platform": "xiaohongshu",
            "source_url": d.get("source_url", f"http://xhslink.cn/o/{slug}"),
            "topic": extra["topic"],
        },
        "scene_imgs": [f"shot-{i:02d}" for i in range(1, len(full_scenes) + 1)],
        "scenes": full_scenes,
        "practice": extra["practice"],
        "pitfalls": extra["pitfalls"],
        "shifts": extra["shifts"],
        "difficult_words": words,
        "footer_notes": extra["footer"],
    }
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ {slug}: {len(full_scenes)} scenes, {total_sents} sents, {len(words)} words")
