#!/usr/bin/env python3
"""批14：将简化场景JSON补全为 gen-scene-en.py 所需的完整结构。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "7yKcnjpgewF": {
        "duration": "3:15", "topic": "美妆 · 遮瑕教程",
        "practice": [
            ["说遮瑕激活", "Rub the cream concealer until slightly tacky."],
            ["说眼下第一笔", "Start at the outer corner and work forward."],
            ["说色斑手法", "Dab vertically with an angled mushroom brush."],
            ["说结构瑕疵", "Cover tear troughs after foundation, not before."],
            ["说定妆提亮", "Pinch a velour puff corner and pat on matte highlighter."]
        ],
        "pitfalls": [
            ["Press the first dab on the inner corner.",
             "Start at the outer corner so the inner area stays thin.",
             "第一笔从眼尾起，眼头粉才薄。"],
            ["Cover all flaws before foundation.",
             "Color flaws first; structure flaws after foundation.",
             "泪沟法令纹等结构瑕疵要放在粉底之后。"],
            ["Dab concealer straight on without activating.",
             "Rub it tacky and spread thin on the hand first.",
             "膏状遮瑕不激活会卡纹卡粉。"],
            ["Skip under-eye setting.",
             "Matte highlighter on a velour puff brightens and sets.",
             "泪沟严重必须定妆，哑光高光二次提亮。"],
            ["Cover in one thick layer.",
             "Build deep troughs in thin layers.",
             "泪沟严重要少量多次叠加。"]
        ],
        "shifts": [
            ["说遮瑕只会说 concealer",
             "用 activate（激活）、tacky（微粘）、spread thin（摊薄）"],
            ["说手法只会说 apply",
             "用 outer corner first（眼尾起笔）、dab vertically（垂直点戳）、build thin layers（少量多次）"],
            ["说瑕疵只会说 flaw",
             "用 color-based（颜色型）、structure-based（结构型）、tear trough（泪沟）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：手指或刷子戳、卡纹卡粉、定妆回潮、三色双色遮瑕、膏状激活、手背摊薄、眼尾起笔、手指温度、斜角蘑菇刷、垂直戳、颜色型结构型瑕疵、泪沟法令纹嘴角凹陷、粉底液后遮、余粉融合、最亮遮瑕色、小粉扑捏起、原地垂直拍开、少量多次、植绒粉扑、哑光高光、二次提亮、定妆、鼻基底、嘴角安全位置、无破绽等。"
    },
    "7TnKPkcYuWu": {
        "duration": "0:32", "topic": "拍摄 · 方圆脸上镜",
        "practice": [
            ["说回头技巧", "The head turns while the shoulders stay."],
            ["说披发方式", "Sweep hair to one side, leaving strands down."],
            ["说低头眼神", "Tilt the crown and relax your eyes downward."],
            ["说坐姿遮挡", "Use a shawl to cover the arms, cross hands for the belly."]
        ],
        "pitfalls": [
            ["Turn head and shoulders together.",
             "Turn only the head; keep the shoulders still.",
             "回头要头回肩不回。"],
            ["Wear hair on both sides.",
             "Sweep it to one side to slim the face.",
             "两边披发会框大脸型。"],
            ["Look down with tense eyes.",
             "Tilt the crown and relax your gaze toward the ground.",
             "低头要放松眼神看地面。"],
            ["Leave arms bare in sitting shots.",
             "Cover arms with the shawl and cross hands for the belly.",
             "坐姿用披肩挡手臂、抱手挡肚。"]
        ],
        "shifts": [
            ["说动作只会说 pose",
             "用 three-quarter view（四分之三侧）、turn head only（头回肩不回）"],
            ["说发型只会说 hair",
             "用 one-side hair（单侧披发）、frame the face（框住脸型）、slim the face（修饰脸型）"],
            ["说遮丑只会说 hide",
             "用 cover the jawline（挡下颌角）、cover the arms（挡手臂）、hide the belly（挡小肚）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：回头肩膀不回、头顶往一边倒、脸型流畅、头发挡下颌角、眼神看镜头下方、头发放两边显脸大、撩在一侧、留一侧修饰脸型、四分之三侧、眉眼显凶、眼神放松看地面、坐姿手臂有肉、披肩挡手臂、抱手挡小肚子等。"
    },
    "7PkSwHyFU1j": {
        "duration": "0:47", "topic": "拍摄 · 眼神管理",
        "practice": [
            ["说侧面眼神", "Keep the head still; let the eyes find the phone."],
            ["说抬头眼神", "Chin up but eyeballs sit slightly lower."],
            ["说低头眼神", "Eyes look toward the floor direction."],
            ["说正面眼神", "Look left or right of the lens."]
        ],
        "pitfalls": [
            ["Show all sclera in profile shots.",
             "Keep the head still and roll your eyes toward the phone.",
             "侧脸时眼珠要转向手机。"],
            ["Roll your eyes when tilting up.",
             "Keep the chin up but the eyeballs lower.",
             "抬头时眼珠略低，避免翻白眼。"],
            ["Shut your eyes when looking down.",
             "Keep the head low and look toward the floor.",
             "低头时眼珠向地板延伸。"],
            ["Stare dead-center in front shots.",
             "Look slightly left or right of the lens.",
             "正面时眼珠偏离镜头中心更灵动。"]
        ],
        "shifts": [
            ["说眼神只会说 eyes",
             "用 eyeballs（眼珠）、sclera（眼白）、roll your eyes（翻白眼）"],
            ["说头位只会说 head",
             "用 chin up（抬头）、head low（低头）、keep the head still（头不动）"],
            ["说方向只会说 direction",
             "用 look toward the floor（向地板）、extend from forehead（从脑门延伸）、off-center（偏离中心）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：侧面全是眼白、头不动、眼珠找手机、抬头翻白眼、眼珠略低、脑门方向延伸、低头像闭眼、眼珠向地板延伸、正面像证件照、眼珠看镜头左边右边、眼神管理等。"
    },
    "9h3W1CZXUMP": {
        "duration": "0:30", "topic": "拍摄 · 眼神训练",
        "practice": [
            ["说恢复眼神", "Raise the brows, then relax."],
            ["说侧脸眼神", "Turn the eyeballs opposite to the face."],
            ["说左右相反", "Face right, eyes look left."]
        ],
        "pitfalls": [
            ["Shoot with tired, flat eyes.",
             "Raise the brows, then relax to find the spark.",
             "抬眉再放松，眼睛就有神。"],
            ["Turn face and eyes the same way.",
             "The eyeball turns opposite to the face.",
             "侧脸时眼珠转向与脸相反。"],
            ["Forget the opposite rule on every profile.",
             "Apply it every time you shoot a profile.",
             "每条侧脸都要用反向眼神。"]
        ],
        "shifts": [
            ["说无神只会说 tired",
             "用 lifeless（无神）、find the spark（找到有神的感觉）"],
            ["说方向只会说 direction",
             "用 opposite direction（相反方向）、face right eyes left（脸右眼左）"],
            ["说训练只会说 practice",
             "用 eye training（眼神训练）、eyebrow raise（抬眉）、relax（放松）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：眼睛无神、眉毛抬起来再放松、有神的感觉、侧脸、眼球转动方向和脸相反、脸往右边转眼睛往左边看、眼神无神等。"
    },
    "2mVLquX3nUL": {
        "duration": "0:56", "topic": "拍摄 · 嘴巴管理",
        "practice": [
            ["说微笑扬嘴角", "Lift the corners toward the apple cheeks."],
            ["说小声哈哈", "Say ha-ha quietly, not a big open mouth."],
            ["说放松微张", "Exhale with a hoo sound, then set the face."],
            ["说嘟嘴想象", "Imagine whistling or a whistle candy."]
        ],
        "pitfalls": [
            ["Smile with flat or drooping corners.",
             "Lift the corners toward the apple cheeks.",
             "嘴角平行或下垂都不好看。"],
            ["Say ha-ha with a huge mouth.",
             "Keep it small and quiet.",
             "小声发哈哈，嘴巴别咧太大。"],
            ["Tense the mouth when relaxing it.",
             "Exhale with a hoo sound to soften it.",
             "吐气能让嘴唇自然放松。"],
            ["Tense hard when pouting.",
             "Imagine whistling or a whistle candy.",
             "嘟嘴时想象吹口哨。"]
        ],
        "shifts": [
            ["说微笑只会说 smile",
             "用 corner lift（嘴角上扬）、apple cheeks（苹果肌）"],
            ["说放松只会说 relax",
             "用 exhale（吐气）、hoo sound（呼的声音）、part-open（微张）"],
            ["说嘴型只会说 mouth",
             "用 whistle candy（口哨糖）、pout（嘟嘴）、lip seam（唇缝）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：嘴角下垂平行、嘴角上扬、斜向苹果肌、发哈哈声音、小声、嘴巴咧太大、不笑时微张、吐气、发呼、脸部表情、嘴巴放松、嘟嘴、吹口哨、口哨糖、嘴巴管理等。"
    },
    "AbNgBncldTo": {
        "duration": "22秒", "topic": "拍摄 · 蹲姿出片",
        "practice": [
            ["说蹲姿核心", "Squat sideways to reveal the leg line."],
            ["说膝盖变化", "Vary one knee high, one low, or crossed."],
            ["说手部框架", "Rest a hand on the knee to form a triangle."],
            ["说万能模板", "Body at 45 degrees, hand on the high knee."]
        ],
        "pitfalls": [
            ["Squat facing the lens.",
             "Turn sideways to reveal the leg line.",
             "正面蹲暴露腿厚。"],
            ["Curl up like a ball.",
             "Keep the torso open and tall.",
             "缩成一团下巴贴膝像球。"],
            ["Keep both knees at the same height.",
             "Vary the knee heights for layers.",
             "双膝同高没层次。"],
            ["Squat in a short skirt.",
             "Avoid squatting poses in short skirts.",
             "短裙蹲姿容易走光。"]
        ],
        "shifts": [
            ["说蹲下只会说 squat",
             "用 side squat（侧身蹲）、knee height change（膝盖高度变化）"],
            ["说身材只会说 figure",
             "用 leg line（腿部线条）、vertical lines（纵向线条）、triangle frame（三角框架）"],
            ["说好看只会说 good",
             "用 layers（层次感）、extended（修长）、photogenic（上镜）"]
        ],
        "footer": "转录基于图文实录完整口播（口播仅水印，场景依据图文实录画面与SVG分析重构）。已校正：三个蹲姿、侧身蹲、膝盖高度变化、手的位置、正面蹲、缩成一团、下巴贴膝盖、腿厚、腿部侧面线条、一高一低、同高交叉、手搭膝盖、自然垂放、三角形框架、纵向线条延长、45度、万能蹲姿模板、街拍旅行、低角度、短裙走光等。"
    },
    "AtQNf9DLz1W": {
        "duration": "0:31", "topic": "拍摄 · 松弛感姿势",
        "practice": [
            ["说胳膊弯曲", "Bend the arms to avoid stiffness."],
            ["说手腕下垂", "Let the hands droop instead of cocking up."],
            ["说脖子歪头", "Tilt the head to avoid a formal look."],
            ["说膝盖屈曲", "Bend one knee when standing or sitting."]
        ],
        "pitfalls": [
            ["Keep arms perfectly straight.",
             "Bend them slightly for an effortless look.",
             "胳膊过直动作僵化。"],
            ["Cock wrists upward.",
             "Let the hands droop for a relaxed look.",
             "手腕下垂比上翘更放松。"],
            ["Hold the head bolt upright.",
             "Tilt the head slightly.",
             "头太正显得过于正式。"],
            ["Stand bolt upright.",
             "Bend one knee for an extended look.",
             "单腿屈膝更舒展。"]
        ],
        "shifts": [
            ["说僵硬只会说 stiff",
             "用 stiffen（僵化）、relaxed（松弛）、effortless（松弛感）"],
            ["说姿势只会说 pose",
             "用 bend the arms（弯胳膊）、droop the wrist（手腕下垂）、tilt the head（歪头）"],
            ["说自然只会说 natural",
             "用 extended（舒展）、formal（正式）、ID photo（证件照）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：松弛感、四件事、胳膊要弯、过直僵化、弯一点松弛、手腕要弯、上翘、下垂、放松、脖子要歪、头太正正式、歪一歪头、膝盖要弯、站太直、单腿屈膝、舒展、坐着也一样等。"
    },
    "9semVCvttLP": {
        "duration": "0:35", "topic": "拍摄 · 坐姿出片",
        "practice": [
            ["说膝盖侧放", "Angle the knee to the side when crossing legs."],
            ["说换腿交叉", "Cross the back leg over the front for slimness."],
            ["说拉长身段", "Lengthen the torso when legs look short."],
            ["说正面坐姿", "Extend the lower leg and turn the toes forward."]
        ],
        "pitfalls": [
            ["Cross legs front-over-back only.",
             "Cross the back leg over the front instead.",
             "前腿搭后腿显壮，后腿搭前腿显瘦。"],
            ["Let the legs look too short.",
             "Lengthen the torso to balance.",
             "腿显短就拉长身段。"],
            ["Face the lens with cramped legs.",
             "Extend the lower leg and turn the toes forward.",
             "正面坐姿伸出小腿脚尖转正。"],
            ["Use the same style for every vibe.",
             "Apart for Korean style, together for demure.",
             "韩系分开放，端庄就并拢。"]
        ],
        "shifts": [
            ["说坐姿只会说 sitting",
             "用 crossed-legs pose（二郎腿）、angle the knee（膝盖侧放）"],
            ["说腿型只会说 legs",
             "用 back leg over front（后腿搭前腿）、extend the lower leg（伸小腿）"],
            ["说风格只会说 style",
             "用 lazy vibe（慵懒感）、Korean style（韩系）、demure（端庄）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：二郎腿、膝盖侧过来放、前腿搭后腿、后腿搭前腿、瘦多了、腿短、身长一点、慵懒感、正面拍、小腿伸出来、脚尖转正、韩系分开放、端庄并拢、随便你选等。"
    },
    "AqvKM2fcdw5": {
        "duration": "1:06", "topic": "拍摄 · 表情控制",
        "practice": [
            ["说微张位置", "Part the lip seam, not the jaw."],
            ["说牙齿接触", "Let the teeth just touch, no hard biting."],
            ["说吹气开唇", "Blow once to push the closed lips open."],
            ["说修饰嘴角", "Use corner-lift strength to fix drooping corners."]
        ],
        "pitfalls": [
            ["Drop the jaw for a part-open mouth.",
             "Open the lip seam, keep the jaw still.",
             "微张张的是唇缝不是下颌。"],
            ["Bite the teeth together hard.",
             "Let them just touch.",
             "牙齿轻碰即可，别使劲咬。"],
            ["Let the mouth look stretched.",
             "Blow to part it and correct drooping corners.",
             "吹气开缝，微张要放松。"],
            ["Ignore drooping corners.",
             "Use the smile corner-lift to correct them.",
             "嘴角下挂要用嘴角力量修饰。"]
        ],
        "shifts": [
            ["说表情只会说 face",
             "用 part-open（微张）、lip seam（唇缝）、drooling（流口水）"],
            ["说嘴部只会说 mouth",
             "用 jaw sinks（下颌下沉）、teeth just touch（牙齿轻碰）、blow open（吹开）"],
            ["说放松只会说 relax",
             "用 loose and saggy（松垮）、corner-lift（嘴角力量）、relaxed（放松）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：微张、呆、下颌骨沉下来、流口水、松垮、张的不是下颌骨、嘴唇的缝分开、牙齿并在一起、别使劲咬、碰在一起、嘴唇闭拢、吹一口气、吹开、微弱的缝、嘴角下挂、嘴角力量、修饰、放松、拉开难看等。"
    },
    "nn40KSlwOw": {
        "duration": "3:22", "topic": "拍摄 · 上镜显瘦",
        "practice": [
            ["说挤压动作", "Keep arms off the body, never squeeze limbs."],
            ["说背部打开", "Open the back backward, settle, and hold."],
            ["说颈部提拉", "Lift the neck, ease forward, and settle back."],
            ["说模糊比例", "Blur the waistline with clothes or half-body shots."],
            ["说侧光显瘦", "Use side light in the soft late afternoon."],
            ["说90度法", "Full front or full side as the last resort."]
        ],
        "pitfalls": [
            ["Squeeze limbs against the body.",
             "Keep arms off the body for space.",
             "挤压肢体加剧肉感。"],
            ["Accept a thick back and round shoulders.",
             "Open the back backward and hold.",
             "背部打开回落，优化上镜状态。"],
            ["Ignore the neck line.",
             "Lift the neck to reduce the double chin.",
             "颈部视觉是显瘦核心。"],
            ["Reveal the waistline in full body.",
             "Blur the ratio with outfits or half-body framing.",
             "明确腰线暴露比例。"],
            ["Use flat frontal light.",
             "Learn side light with soft low sun.",
             "侧光阴影才显瘦。"],
            ["Forget posture is real.",
             "Fix actual posture scientifically.",
             "真有体态问题要科学改善。"]
        ],
        "shifts": [
            ["说显瘦只会说 slimmer",
             "用 fleshiness（肉感）、blur the ratio（模糊比例）、side light（侧光）"],
            ["说动作只会说 move",
             "用 open the back（背部打开）、lift the neck（提脖子）、90-degree rule（90度调整法）"],
            ["说照片只会说 photo",
             "用 on-camera presence（上镜状态）、half-body shot（半身）、weakens shadows（弱化阴影）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：上镜显胖、后期大力出奇迹、挤压肢体、加剧肉感、手臂离开身体、给出空间、轻盈、背厚肩圆笨重、背部向后打开、向下回落定住、体态问题科学改善、脖子肥大、双下巴、向上提起脖子、向前探出、回落、颈部视觉核心、模糊比例、一米五多、明确腰线、连衣裙、宽松衬衫、模糊腰线、拍半身、苹果型身材、肩膀脖子区域、冒出来的领子、翻领、围巾、厚重感、露脖子、顺着光扁平、侧光、下午太阳较低柔和、顺光逆光、脸上四肢阴影、90度调整法、正脸完全正、侧脸完全侧、保下限、向下调整、下巴下颚面往上走弱化阴影、往下走强化阴影、挤压脖子、显瘦、脸型调整、八个实用技巧、课程栏目、摄影师小李等。"
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
