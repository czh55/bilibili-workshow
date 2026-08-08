#!/usr/bin/env python3
"""批12：将简化场景JSON补全为 gen-scene-en.py 所需的完整结构。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "6zovAUiqTnQ": {
        "duration": "3:11", "topic": "剪辑 · iPhone调色APP",
        "practice": [
            ["说灰片来源", "We forgot to select LUT burn-in when shooting."],
            ["说VN的操作", "Open the Filters tab to grade Apple Log fast."],
            ["说LUT微调", "Tune exposure and saturation on the current LUT."],
            ["说导入LUT", "Tap Add in Filters and choose From Files."]
        ],
        "pitfalls": [
            ["Shoot without picking a LUT setting.",
             "Choose LUT burn-in while shooting, or grade later.",
             "忘选LUT烧录会得到灰片，需要第三方APP补救。"],
            ["Grade flat clips directly in the album.",
             "Use a third-party app like VN to grade gray footage.",
             "相册无法加载LUT，必须用第三方APP。"],
            ["Adjust the whole LUT only.",
             "Fine-tune exposure, saturation, and per-color hue.",
             "LUT基础上还能逐项微调参数。"],
            ["Store LUTs anywhere unclear.",
             "Keep LUTs in a folder like the Blackmagic Camera app.",
             "LUT要放在明确目录，导入时从文件添加。"]
        ],
        "shifts": [
            ["说调色只会说 color",
             "用 LUT（查色表）、flat gray（灰片）、grade（调色）"],
            ["说滤镜只会说 filter",
             "用 Filters tab（滤镜面板）、preset（预设）、anime style（动漫风）"],
            ["说调整只会说 change",
             "用 exposure（曝光）、per-color hue（单色色相）、white balance（色温）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：Blackmagic Camera、LUT烧录、灰片格式、VN Video Editor、Apple Log、动漫风、调整面板、曝光/饱和度/色温、从文件添加、人像晨调、Resolve Fusion等。"
    },
    "2t22wB8H3m4": {
        "duration": "33秒", "topic": "剪辑 · 字体配色",
        "practice": [
            ["说颜色对比", "Red on my head pops; black would look flat."],
            ["说互补色", "Yellow on blue looks beautiful."],
            ["说踩雷的救法", "Use white and desaturate the text color."]
        ],
        "pitfalls": [
            ["Use any text color you like.",
             "Choose a color that contrasts with the background.",
             "字体颜色要与背景形成对比，否则不酷。"],
            ["Pick gray for a safe look.",
             "Pick a complementary color like yellow on blue.",
             "黑灰一般般，互补色才出彩。"],
            ["Stick to a loud color on busy frames.",
             "Use white and desaturate when color ruins the frame.",
             "画面复杂时白色加降饱和最稳。"]
        ],
        "shifts": [
            ["说字体只会说 font",
             "用 text color（文字颜色）、color contrast（颜色对比）、complementary（互补色）"],
            ["说好看只会说 nice",
             "用 pops（出彩）、premium（高级）、flat（平庸）"],
            ["说调整只会说 change",
             "用 desaturate（降饱和）、neutralize（中和）、pairing（搭配）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：红色文字、颜色对比、黄色在蓝色上、黑色灰色一般、文字颜色毁画面、白色、降饱和、完美搭配等。"
    },
    "8Atb7PlOMpX": {
        "duration": "1:08", "topic": "拍摄 · 竖屏构图",
        "practice": [
            ["说竖持手机比例", "Seventy-five percent hold their phone vertically."],
            ["说字幕位置", "Keep subtitles above the progress bar line."],
            ["说互动区遮挡", "Likes, comments, and shares cover the bottom."],
            ["说眼睛位置", "Your eyes should stay in the golden zone."]
        ],
        "pitfalls": [
            ["Design for landscape viewing.",
             "Design for the 75% who hold their phone vertically.",
             "75%竖持手机，内容要适配竖屏。"],
            ["Place subtitles near the bottom edge.",
             "Keep subtitles above the progress-bar line.",
             "字幕会被进度条和点赞栏遮住。"],
            ["Put your face anywhere in the frame.",
             "Keep your eyes in the golden zone from any angle.",
             "眼睛始终保持在黄金区域。"],
            ["Ignore platform UI overlays.",
             "Leave room for likes, comments, and shares.",
             "预留互动按钮区域，避免遮挡。"]
        ],
        "shifts": [
            ["说构图只会说 compose",
             "用 golden zone（黄金区）、critical area（关键区域）、safe line（安全线）"],
            ["说字幕只会说 caption",
             "用 subtitle placement（字幕位置）、stay above the line（在线之上）"],
            ["说数据只会说 data",
             "用 75% vertically（75%竖持）、cover up（遮挡）、keep watching（看不停）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：关键区域、75%竖持手机、字幕位置、进度条、点赞栏、点赞留言分享区、眼睛黄金区、看个不停等。"
    },
    "4Jj42V65B6U": {
        "duration": "1:15", "topic": "拍摄 · 镜头语言",
        "practice": [
            ["说荷兰角", "The Dutch tilt adds imbalance and tension."],
            ["说仰拍效果", "Low angle makes the subject look powerful."],
            ["说过肩镜头", "The over-the-shoulder shot immerses the viewer."],
            ["说超特写", "Extreme close-up turns detail into the hero."]
        ],
        "pitfalls": [
            ["Tilt the camera randomly for effect.",
             "Use the Dutch tilt to create tension and imbalance.",
             "荷兰角是为紧张感服务，不是随便倾斜。"],
            ["Shoot everything at eye level.",
             "Use low and high angles to control power and mood.",
             "仰俯拍分别传达强势与柔和。"],
            ["Show only the subject.",
             "Use over-the-shoulder shots for immersion.",
             "过肩镜头让观众瞬间代入。"],
            ["Zoom out for everything.",
             "Use extreme close-ups to highlight key moments.",
             "超特写把细节变成主角。"]
        ],
        "shifts": [
            ["说镜头只会说 shot",
             "用 Dutch tilt（荷兰角）、low/high angle（仰俯拍）、over-the-shoulder（过肩）"],
            ["说情绪只会说 mood",
             "用 tension（紧张感）、helplessness（无力感）、intimacy（亲密感）"],
            ["说讲故事只会说 tell",
             "用 cinematic（故事感）、carry emotion（传达情绪）、key moment（关键瞬间）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：荷兰式倾斜角度、失衡感紧张感、仰拍强势、俯拍柔和、焦虑感无力感、过肩镜头、超特写、关键瞬间、故事感等。"
    },
    "AeIri1iYpGs": {
        "duration": "1:12", "topic": "拍摄 · 剪辑注意力",
        "practice": [
            ["说剪辑匹配", "Keep the subject in the same place across the cut."],
            ["说无痕剪切", "The cut becomes nearly invisible."],
            ["说三分构图", "Place the subject on a grid focal point."],
            ["说引导视线", "Good composition steers the viewer's gaze."]
        ],
        "pitfalls": [
            ["Cut to a completely new position.",
             "Keep the subject in the same place so eyes don't search.",
             "主体位置一致，剪切才无痕。"],
            ["Center everything in the frame.",
             "Place the subject on a grid focal point.",
             "主体放网格焦点，构图才有呼吸。"],
            ["Pack the frame edge to edge.",
             "Use the rule of thirds for balance and beauty.",
             "三分构图带来平衡美感。"]
        ],
        "shifts": [
            ["说剪辑只会说 cut",
             "用 match on cut（剪辑匹配）、nearly invisible（几乎无痕）"],
            ["说构图只会说 compose",
             "用 rule of thirds（三分法）、grid lines（网格线）、focal point（焦点）"],
            ["说吸引只会说 attract",
             "用 steer the gaze（引导视线）、grab attention（抓住注意力）、balance and beauty（平衡美感）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：抓住观众注意力、剪切匹配、同一位置、几乎察觉不到、网格线、焦点、三分构图、引导视线、平衡美感、照片视频通用等。"
    },
    "5pOlmvU8vTS": {
        "duration": "1:05", "topic": "拍摄 · 度假Vlog",
        "practice": [
            ["说开场结构", "Wide shot of you walking in, then a tight shot."],
            ["说稳定运镜", "Keep the movement silky and stable."],
            ["说对角线构图", "Shoot the pool moment on a diagonal."],
            ["说前后景层次", "Place yourself between foreground and background."]
        ],
        "pitfalls": [
            ["Start with a close-up.",
             "Start with a wide shot, then a tight shot.",
             "度假Vlog开场用远景走进来再切近景。"],
            ["Wave the camera around.",
             "Keep movement silky and stable.",
             "运镜要丝滑稳定。"],
            ["Shoot everything head-on.",
             "Use a diagonal for the pool moment.",
             "泳池享受过程用对角线构图。"],
            ["Stay far from the lens.",
             "Place yourself between foreground and background.",
             "前后景之间才有层次。"],
            ["Skip the details.",
             "Shoot some detail shots to finish.",
             "细节镜头让画面更丰富。"]
        ],
        "shifts": [
            ["说拍视频只会说 record",
             "用 wide shot（远景）、tight shot（近景）、detail shots（细节镜头）"],
            ["说运镜只会说 move",
             "用 silky and stable（丝滑稳定）、diagonal（对角线）、foreground（前景）"],
            ["说好看只会说 beautiful",
             "用 depth（层次）、cinematic（电影感）、relaxing moment（享受时刻）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：泳池拍自己、远景、表情近景、展示景色、丝滑稳定、对角线、前后景层次、细节镜头等。"
    },
    "3EBy7VLengn": {
        "duration": "1:17", "topic": "剪辑 · 画质清晰",
        "practice": [
            ["说帧率一致", "Shoot, edit, and export at the same frame rate."],
            ["说导出1080的原因", "It loads faster and the algorithm prefers it."],
            ["说比特率误区", "Bitrate isn't quality; heavy files get compressed harder."]
        ],
        "pitfalls": [
            ["Shoot 30fps, edit 25fps, export 24fps.",
             "Keep one frame rate across shoot, edit, and export.",
             "帧率不一致画面会坏掉卡顿。"],
            ["Export 4K for best quality.",
             "Export 1080p—it loads faster and the algorithm likes it.",
             "1080P加载快，平台更喜欢。"],
            ["Raise the bitrate for clarity.",
             "Bitrate isn't quality; the platform compresses heavy files harder.",
             "高比特率不是画质，反而被压得更狠。"],
            ["Chase specs for premium feel.",
             "Comfortable light and natural rhythm matter more.",
             "光线舒服节奏自然，简单即高级。"]
        ],
        "shifts": [
            ["说清晰只会说 clear",
             "用 crisp（清晰）、consistent frame rate（帧率一致）、playback（播放）"],
            ["说导出只会说 export",
             "用 load faster（加载快）、algorithm（算法）、juddery（卡顿）"],
            ["说画质只会说 quality",
             "用 bitrate（比特率）、compress harder（压得更狠）、premium（高级）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：4K25帧、1080P 25帧、30/25/24帧不一致、画面坏掉卡顿、加载快、平台算法、比特率不是画质、压得更狠、光线舒服节奏自然等。"
    },
    "3eUM3lUb9kV": {
        "duration": "2:09", "topic": "剪辑 · 声画联动",
        "practice": [
            ["说画面主导", "The sound follows the on-screen actions."],
            ["说动作声音", "Turn up the background music after the action."],
            ["说音乐主导", "Cut the image to the music's rhythm."],
            ["说跳切变速", "Use speed changes and jump cuts to match."]
        ],
        "pitfalls": [
            ["Keep background music constant.",
             "Turn the music up after a start-or-end action.",
             "动作瞬间让声音变化，细节才出彩。"],
            ["Edit without listening to the beat.",
             "Cut the frame to the music's rhythm.",
             "卡点剪辑要顺着音乐节奏。"],
            ["Cut frames without logic.",
             "Keep story logic, then use speed or jump cuts.",
             "跳切变速要以前后画面有逻辑为前提。"],
            ["Overdo flashy effects.",
             "Use subtle, thoughtful sound-frame sync.",
             "含蓄的高级感优于花里胡哨的炫技。"]
        ],
        "shifts": [
            ["说剪辑只会说 edit",
             "用 sound-frame sync（声画联动）、beat-sync（卡点）、jump cut（跳切）"],
            ["说音乐只会说 music",
             "用 rhythm（节奏）、background music（背景音）、turn it up（调大）"],
            ["说高级只会说 fancy",
             "用 subtle premium（含蓄高级）、clever touch（巧思）、shine（出彩）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：声画联动、画面主导、开始或结束动作、戴耳机/开门/拉链/液化气旋钮、背景音调大、音乐主导、卡点视频、变速、跳切、含蓄高级感等。"
    },
    "ADA626B7s2f": {
        "duration": "27秒", "topic": "剪辑 · 无缝衔接",
        "practice": [
            ["说动作瞬间切画", "Cut right at the moment of the action."],
            ["说保持说话", "Keep talking while you switch the shot."],
            ["说过渡规则", "Transitions should follow comfortable rules."]
        ],
        "pitfalls": [
            ["Cut mid-sentence with no reason.",
             "Cut at the action moment while continuing to talk.",
             "在动作瞬间切画，说话不断。"],
            ["Keep one static shot the whole time.",
             "Change the shot to keep it engaging.",
             "别忘了切换镜头。"],
            ["Use flashy random transitions.",
             "Follow simple, comfortable transition rules.",
             "过渡要遵循简单舒服的规则。"]
        ],
        "shifts": [
            ["说剪辑只会说 cut",
             "用 cutaway（切画）、seamless（无缝）、transition（过渡）"],
            ["说自然只会说 natural",
             "用 at the moment of action（动作瞬间）、keep talking（持续说话）"],
            ["说舒服只会说 comfortable",
             "用 comfortable rules（舒服的规则）、engaging（吸引人）、premium（高级感）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：动作瞬间紧切画面、继续说话、切换镜头、过渡规则、下集预告等。"
    },
    "5hnZliYYqQP": {
        "duration": "1:24", "topic": "美妆 · 卧蚕画法",
        "practice": [
            ["说画卧蚕方法", "Draw a line under the eye and highlight above."],
            ["说阴影面换线", "Swap the dark line for a soft shadow plane."],
            ["说上下加深", "Deepen the lash root and lower-lid triangle."],
            ["说高光点缀", "Brighten a small front-top area and let it fade."]
        ],
        "pitfalls": [
            ["Draw one hard line under the eye.",
             "Use a soft shadow plane with a blended fade.",
             "卧蚕从阴影线进阶到阴影面更自然。"],
            ["Use strong color all along.",
             "Fade the color as it goes outward.",
             "越靠外颜色越淡。"],
            ["Treat aegyo-sal as a sticker.",
             "Connect it with the lash root and lower-lid triangle.",
             "上下加深让卧蚕与眼睛连成一体。"],
            ["Add a big highlight blob.",
             "Brighten a small area and fade by the middle.",
             "高光小面积点缀、中间自然过渡。"],
            ["Skip the setting step.",
             "Layer matte highlighter so it lasts longer.",
             "哑光高光叠加更持久。"]
        ],
        "shifts": [
            ["说卧蚕只会说 eyebag line",
             "用 aegyo-sal（卧蚕）、shadow plane（阴影面）、lash root（睫毛根部）"],
            ["说画法只会说 draw",
             "用 blend（晕染）、tap off excess（擦余粉）、fade outward（向外渐淡）"],
            ["说效果只会说 pretty",
             "用 dimensional（立体）、harmonious（和谐）、natural born look（妈生感）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：眼下画线上方提亮、深色阴影线换浅色阴影面、小刷子、擦余粉、晕染、越靠外越淡、鼻影上下加深、睫毛根部、下睑三角区、眼尾空缺、球体高光、前端上方提亮、哑光高光叠加、妈生感卧蚕等。"
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
