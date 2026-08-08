#!/usr/bin/env python3
"""批11：将简化场景JSON补全为 gen-scene-en.py 所需的完整结构。"""
import json, re, unicodedata
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

# 每篇的额外信息：duration、topic、practice、pitfalls、shifts、footer
EXTRA = {
    "6SQ7dHdz9jn": {
        "duration": "7:22", "topic": "摄影 · 分区曝光",
        "practice": [
            ["说分区曝光的相机设置", "Link spot metering to the focus point."],
            ["说窗户的曝光", "Set the window to plus one for detail without blowout."],
            ["说后期的蒙版合成", "Auto-align the images and mask in each zone."],
            ["说暗部提亮的技巧", "Brush the shadows in layers at fifty percent opacity."]
        ],
        "pitfalls": [
            ["Use multi-metering in strong backlight.",
             "Use spot metering linked to the focus point.",
             "大逆光下多重测光会暗部不足高光过曝，要点测光。"],
            ["Set every zone to zero exposure.",
             "Set each zone to the exposure it needs, like plus one for the window.",
             "每个区域要按「白加黑减」独立曝光，不是统一归零。"],
            ["Paint the mask at full opacity.",
             "Drop the mask opacity and brush in layers.",
             "满透明度直接擦反差太大，要降到50%分层擦拭。"],
            ["Lift every dark area to full brightness.",
             "Keep some shadow for realism.",
             "暗部不必全部刷亮，要保留真实的光比氛围。"]
        ],
        "shifts": [
            ["说测光只会说 exposure",
             "用 spot metering（点测光）、focus-point linked（对焦点联动）、zone exposure（分区曝光）"],
            ["说后期只会说 merge",
             "用 auto-align（自动对齐）、mask（蒙版）、layer by layer（分层擦拭）"],
            ["说亮度只会说 bright / dark",
             "用 blowout（过曝）、white level（白色阶）、luminance mask（亮度蒙版）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：点测光、对焦点联动、白加黑减、正一/负0.3、自动对齐、蒙版、透明度70/50/30、亮度蒙版、白色阶、曲线、白平衡等。"
    },
    "3z4vfB7cxH5": {
        "duration": "3:10", "topic": "摄影 · 布光原理",
        "practice": [
            ["说蝴蝶光的别名", "Butterfly light is also called Paramount light."],
            ["说正确打法", "Aim the beauty dish center at the bridge of the nose."],
            ["说蝴蝶的来源", "The muscle under the eye faces the dish directly."],
            ["说真正目的", "The goal is dimension, not a butterfly shape."]
        ],
        "pitfalls": [
            ["Hunt for the butterfly shadow under the nose.",
             "Learn the motive behind the lighting.",
             "找结果不如找动机，蝴蝶只是副产品。"],
            ["Raise the light until the butterfly appears.",
             "Keep the dish at forehead height and arm's reach.",
             "强行找蝴蝶会让脸变成骷髅脸，正确参数是额头高、一臂距。"],
            ["Say Asian faces don't suit butterfly light.",
             "The myth fails: forcing the butterfly ruins beauty.",
             "亚洲人不适合蝴蝶光是对「找蝴蝶」逻辑的误读。"],
            ["Judge the light by the triangle shape only.",
             "Judge it by dimension and three-dimensionality.",
             "判断标准是立体感而不是某个形状。"]
        ],
        "shifts": [
            ["说布光只会说 light",
             "用 beauty dish（雷达罩）、light ring（亮环）、falloff（衰减）"],
            ["说目的只会说 look",
             "用 motive（动机）、dimension（立体感）、byproduct（副产品）"],
            ["说面部只会说 face",
             "用 orbicularis muscle（口轮匝肌）、eyebrow bone（眉弓骨）、cheekbone（颧骨）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：派拉蒙光、雷达罩、反射板、日全食亮环、口轮匝肌、眉弓骨、颧骨、立体感、骷髅脸、亚洲人不适合蝴蝶光的破除等。"
    },
    "AL6IHBBwa6r": {
        "duration": "2:25", "topic": "剪辑 · 口播接单复盘",
        "practice": [
            ["说收到新单", "A new unboxing ad came in for 800 yuan."],
            ["说素材分类", "The footage splits into A-roll and two B-rolls."],
            ["说反馈修改", "The hero shade needs more time on screen."],
            ["说商用字体", "All fonts are commercially licensed."]
        ],
        "pitfalls": [
            ["Ignore the brand's materials.",
             "Study the brand materials and match the client's style.",
             "品牌方的补充信息都要消化，视频要贴合单主风格。"],
            ["Mix every shade evenly.",
             "Give the hero shade more screen time.",
             "主推色要加长，其他色分四屏展示。"],
            ["Use any font you like.",
             "Use commercially licensed fonts.",
             "规避版权，字体必须可商用。"]
        ],
        "shifts": [
            ["说接单只会说 get a job",
             "用 talking-head ad（口播广告）、full-line review（全系列测评）、client（单主）"],
            ["说剪辑只会说 edit",
             "用 rough cut（粗剪）、fine cut（精剪）、packaging（包装）"],
            ["说反馈只会说 feedback",
             "用 hero shade（主推色）、4-panel layout（四屏展示）、review pass（审片）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：加薪、PR、开箱口播800元、A roll/B roll、色号编号、粗剪、4屏展示、商用字体、包装、交付周期等。"
    },
    "91f9xpJbOMH": {
        "duration": "1:52", "topic": "剪辑 · Vlog效率",
        "practice": [
            ["说传统做法", "Lay all clips on the timeline in order."],
            ["说遇到的问题", "I keep losing track of where I am."],
            ["说新思路", "Sort the footage into two categories."],
            ["说邪门方法", "Lay a placeholder clip across the whole audio."]
        ],
        "pitfalls": [
            ["Drop every clip first, then sort.",
             "Sort into main-subject and support first.",
             "先分类再铺轨，而不是铺满再找。"],
            ["Stretch one long timeline and hunt for clips.",
             "Build the main-subject spine, add support on demand.",
             "主体镜头先行，补充镜头按需加入。"],
            ["Match footage to script without a plan.",
             "Cut the audio first, then swap in footage per sentence.",
             "以录音为骨架，一句一句替换素材。"]
        ],
        "shifts": [
            ["说剪辑只会说 cut",
             "用 rough cut（粗剪）、placeholder clip（打底素材）、swap in（替换）"],
            ["说素材只会说 footage",
             "用 main-subject shots（主体镜头）、support shots（补充镜头）、empty scenes（空景）"],
            ["说效率只会说 fast",
             "用 twice the result with half the effort（事半功倍）、know your footage（熟悉素材）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：vlog接单、铺素材、听文案、主体人物类/其他类、空景、补充镜头、邪门方法、素材打底、切段替换、事半功倍等。"
    },
    "8JbaT2D24UD": {
        "duration": "3:11", "topic": "剪辑 · 关键帧教学",
        "practice": [
            ["说关键帧的本质", "It creates gradual change between two keyframes."],
            ["说变大变小的做法", "Add a keyframe, then pinch outward to zoom."],
            ["说声音变化", "Drop the volume to zero on the first beat."],
            ["说蒙版转场", "A linear mask makes a background-change transition."]
        ],
        "pitfalls": [
            ["Expect a sudden jump between keyframes.",
             "Keyframes create gradual change, not jumps.",
             "关键帧是渐变不是突变。"],
            ["Move the timeline without adding a keyframe.",
             "Add a start keyframe before moving the timeline.",
             "先打起始关键帧再移动时间轴。"],
            ["Zoom the whole frame for an effect.",
             "Pinch on the frame after the start keyframe.",
             "双指放大画面会自动生成关键帧。"],
            ["Keep the music loud while speaking.",
             "Drop the music when you start talking.",
             "讲话或重点信息时音乐要降低。"]
        ],
        "shifts": [
            ["说动画只会说 animate",
             "用 keyframe（关键帧）、gradual change（渐变）、auto-form（自动形成）"],
            ["说效果只会说 effect",
             "用 opacity（不透明度）、auto beat-drop（自动踩点）、mask（蒙版）"],
            ["说转场只会说 transition",
             "用 linear mask（线性蒙版）、mirror mask（镜面蒙版）、fade out（淡出）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：关键帧、渐变变化、变大变小、不透明度、贴纸移动、文字变色、自动踩点、音量起伏、线性蒙版、镜面蒙版、圆形矩形蒙版等。"
    },
    "1R1UjgiLfff": {
        "duration": "11:07", "topic": "器材 · 稳定器教学",
        "practice": [
            ["说三轴名称", "The gimbal has tilt, roll, and pan axes."],
            ["说俯仰轴平衡", "If the lens tips forward, move the arm back."],
            ["说激活步骤", "Connect in the app with password 12345678."],
            ["说折叠收纳", "Half-fold needs no rebalancing for quick moves."]
        ],
        "pitfalls": [
            ["Skip balancing before shooting.",
             "Balance all three axes first.",
             "三轴都要调平，否则画面会抖。"],
            ["Force the plate if it won't align.",
             "Flip the plate 180 degrees to align.",
             "快装板对不上就翻转180度。"],
            ["Balance only the tilt axis.",
             "Balance tilt, roll, and pan.",
             "俯仰、横滚、平移三轴都要平衡。"],
            ["Fold full when changing scenes quickly.",
             "Use half-fold for quick scene changes.",
             "快速转场用半折叠，不用重新调平。"]
        ],
        "shifts": [
            ["说稳定器只会说 stabilizer",
             "用 tilt/roll/pan axes（俯仰/横滚/平移轴）、axis lock（轴锁）、latch（搬扣）"],
            ["说调平只会说 adjust",
             "用 center of gravity（重心）、horizontal balance（水平平衡）、vertical balance（垂直平衡）"],
            ["说收纳只会说 fold",
             "用 half-fold（半折叠）、full-fold（全折叠）、quick-release plate（快装板）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：RS 3 mini、包装清单、5V 2A、上层/下层快装板、俯仰/横滚/平移轴、轴锁、搬扣、重心判断、激活、DJI Ruin App、12345678、DJI Care 30天、半折叠/全折叠等。"
    },
    "AjVetKVyu7J": {
        "duration": "1:06", "topic": "剪辑 · 蒙版调色",
        "practice": [
            ["说分析光影", "Analyze the light and shadow first."],
            ["说复制视频", "Duplicate the clip onto a picture-in-picture track."],
            ["说蒙版选区", "Use a mask to outline the area to grade."],
            ["说左右分区", "Make the left cool and dark, the right warm and bright."]
        ],
        "pitfalls": [
            ["Grade the whole frame at once.",
             "Mask one area and grade it alone.",
             "先分析光影再分区蒙版调色。"],
            ["Use a hard mask edge.",
             "Add feathering for natural transitions.",
             "蒙版边缘要带羽化过渡才自然。"],
            ["Grade both sides the same.",
             "Make the left cooler and the right warmer.",
             "左右冷暖明暗对比是本视频的核心。"],
            ["Skip the cinematic effects.",
             "Add glow and vignette for a film look.",
             "最后加梦幻灰光和暗角增加电影感。"]
        ],
        "shifts": [
            ["说调色只会说 color",
             "用 light-shadow relationship（光影关系）、cool vs warm（冷暖）、mask（蒙版）"],
            ["说选区只会说 select",
             "用 outline（圈出）、feathering（羽化）、picture-in-picture（画中画）"],
            ["说特效只会说 filter",
             "用 dreamy glow（梦幻灰光）、vignette（暗角）、cinematic（电影感）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：蒙版光影感调色、画中画、对齐主轨、蒙版形状、羽化、冷暗左半、暖亮右半、梦幻灰光、暗角、电影感等。"
    },
    "3n3p9zsXLp2": {
        "duration": "1:05", "topic": "剪辑 · 调色新手",
        "practice": [
            ["说参数的作用", "Brightness lifts the whole image."],
            ["说冷白皮技巧", "Lower the orange hue and saturation, then raise brightness."],
            ["说果蔬调色", "Match each color to the produce in the frame."],
            ["说色温收尾", "Use cool white balance for a clean, fair look."]
        ],
        "pitfalls": [
            ["Raise contrast for a bright look.",
             "Lower contrast for a creamier look.",
             "奶油风要降对比度，不是加对比度。"],
            ["Adjust orange brightness before hue.",
             "Lower orange hue and saturation first, then brightness.",
             "橙色先降色调饱和度再提亮度。"],
            ["Skip highlights and shadows.",
             "Tune highlights and shadows for dimension.",
             "高光和阴影让画面更立体。"],
            ["Use warm white balance.",
             "Use cool white balance.",
             "清透白皙要选冷色调。"]
        ],
        "shifts": [
            ["说调色只会说 adjust",
             "用 brightness（亮度）、contrast（对比度）、saturation（饱和度）、clarity（清晰度）"],
            ["说皮肤只会说 skin",
             "用 HSL（色相饱和度明度）、cool fair tone（冷白皮）、orange hue（橙色色相）"],
            ["说成品只会说 good",
             "用 creamy（奶油风）、clean and fair（清透白皙）、dimensional（立体）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：亮度/对比度/饱和度/光感/锐化/清晰度、HSL、橙色降色调降饱和度、果蔬颜色、高光阴影、色温冷色调、冷白皮等。"
    },
    "2Ow3D1F2k7V": {
        "duration": "2:47", "topic": "拍摄 · 手机Vlog",
        "practice": [
            ["说四种镜头", "Shoot wide, close-up, full-body, and action shots."],
            ["说空镜要点", "Keep things moving inside the frame."],
            ["说追踪拍摄", "Let the gimbal track the person 360 degrees."],
            ["说近景配合", "Fill half the frame and keep doing your thing."]
        ],
        "pitfalls": [
            ["Shoot everything without a plan.",
             "Record four kinds of shots per scene.",
             "每个场景只拍四种画面，避免素材爆炸。"],
            ["Hold the camera still for wide shots.",
             "Keep things moving inside the frame.",
             "空镜要让物体动起来才有重点。"],
            ["Chase the person with your hands.",
             "Let the gimbal's tracking keep them centered.",
             "用稳定器追踪，人始终在画面中心。"],
            ["Show only the environment.",
             "Add person and close-up shots for focus.",
             "近景和人物让视觉焦点更明确。"]
        ],
        "shifts": [
            ["说拍摄只会说 record",
             "用 four shots per scene（每场景四镜头）、wide shot（空镜）、close-up（特写）"],
            ["说运镜只会说 move",
             "用 slow pan（慢横移）、rise and lower（升降）、fixed shot（固定镜头）"],
            ["说成片只会说 video",
             "用 cinematic feel（电影感）、immersion（沉浸感）、mix and match（随机组合）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：无Log素材、四种画面（场景空镜/物品特写/人物全景/人物近景）、固定拍摄、移动拍摄、Flow2 Pro、智能美学构图、副屏遥控、随机组合、电影感等。"
    }
}

# 简化JSON读取 + 补全
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
        # paraphrase: 从句子 note 提取关键词
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
            "time": s.get("time", f"00:00"),
            "context": s.get("context", ""),
            "sentences": sentences,
            "paraphrase": paraphrase[:2],
            "speak": speak,
        })

    total_sents = sum(len(s["sentences"]) for s in full_scenes)
    # difficult_words: 从所有英文提取长词
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
