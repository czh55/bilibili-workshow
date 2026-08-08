#!/usr/bin/env python3
"""批16：将简化场景JSON补全为 gen-scene-en.py 所需的完整结构。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "4IbwyqRz82t": {
        "duration": "3:07", "topic": "摄影 · 家庭引导",
        "practice": [
            ["说引导痛点", "Clients go stiff and fake-smile when directed."],
            ["说故事引导法", "Guide them into a story scene, not a pose."],
            ["说拍摄剧本", "Learn the family's small real-life details first."],
            ["说高光捕捉", "Move your position and record, don't re-pose."],
            ["说情境替代", "Turn commands into games and situations."]
        ],
        "pitfalls": [
            ["Shout 'smile!' and snap.",
             "Direct with a story scene, not commands.",
             "喊看镜头笑只会换来假笑。"],
            ["Force emotional recall on families.",
             "Use small daily details like cartoons and games.",
             "强行回忆情绪反而尴尬。"],
            ["Re-pose the moment once it's real.",
             "Move your position and record instead.",
             "真实的瞬间无需打断重摆。"],
            ["Give action commands to shy clients.",
             "Give situational states or games.",
             "动作指令换情境与游戏。"],
            ["Pull clients into perfect poses.",
             "Return them to their real state and forget the lens.",
             "完美姿势不如真实状态。"]
        ],
        "shifts": [
            ["说引导只会说 directing",
             "用 story scene（故事场景）、shooting script（拍摄剧本）、storyteller（故事讲述者）"],
            ["说拍照只会说 shoot",
             "用 capture highlight emotions（捕捉高光情绪）、observe（观察）、amplify real emotion（放大真实情绪）"],
            ["说家庭只会说 family",
             "用 real emotional threads（真实情绪线索）、family documentary（家庭纪实）、accept（接纳）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：越引导越尴尬、动作僵硬、尴尬假笑、技术不行、引导方式、最关键的一环、家庭纪实、摆姿势按快门、故事场景、摄像机、小片场、快门机器、故事讲述者、故事引导法、进入情境、体验一个瞬间、三点、家庭剧本、拍摄前开始、这个家的故事、孩子喜欢什么、特别经历、真实情感线索、调查文券、朋友圈、第一次抱宝宝、强行进入情绪、动画、小游戏、读到烂掉的绘本、互动方式、更自然更真实、生活瞬间、高光情绪、被观察出来、显示器、微小波动、靠在妈妈肩上、抚摸头、温柔、摆不出来、沙发聊天、爸爸什么都没说、嘴角上扬、不用打断、不用重新摆拍、移动机位、记录、放大真实的情绪、制造表情、动作指令、情境状态、演情绪、玩游戏、挤成馅饼、家里最可爱的人、吃一颗糖、自然地进入角色、故事里的家人、最好的引导、完美姿势、真实状态、忘记镜头、应该怎么拍、陪伴、接纳、突然想笑、鼻酸、抱得很紧、真实保存、柔软的记忆、最幸福的事情等。"
    },
    "4v3XB1avzP9": {
        "duration": "1:04", "topic": "摄影 · 透视畸变",
        "practice": [
            ["说透视与畸变", "Stretch is distortion; near objects get bigger by perspective."],
            ["说低机位问题", "Sitting low with wide angle enlarges feet, thickens legs."],
            ["说升高机位", "Stand up and lean back to change the perspective."],
            ["说拍长腿", "Raise the camera to lengthen legs without thickening them."],
            ["说熟练练功", "The skill is practice—shoot more."]
        ],
        "pitfalls": [
            ["Confuse distortion and perspective.",
             "Stretch is distortion; bigness is perspective.",
             "畸变与透视别混淆。"],
            ["Shoot from a low seat for long legs.",
             "Raising the camera height changes the perspective.",
             "低机位拍长腿反而显粗。"],
            ["Blame the lens for thick legs.",
             "It's the perspective relationship with camera height.",
             "腿粗脸大是透视关系。"],
            ["Skip practice after learning theory.",
             "Practice shooting until it's muscle memory.",
             "听懂后要练成熟练功。"]
        ],
        "shifts": [
            ["说畸变只会说 distortion",
             "用 stretch（拉长）、perspective（透视）、camera height（机位）"],
            ["说效果只会说 effect",
             "用 near and far（近大远小）、proportion（比例）、look longer（显得更长）"],
            ["说学习只会说 learn",
             "用 muscle memory（熟练功）、practice more（多练）、what I use（我用的东西）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：后仰、低机位、广角、离你最近、腿离得近、脚大腿粗、偏广角、被拉长、脸发泡、脚显大、腿显粗、畸变、透视、腿变长不变粗、脸瘦一点、坐地上、坐椅子上、站起来、往后仰、机位高起来、离镜头近、变远、腿长的同时不粗、畸变关系、比他本人看起来长、透视没控制好、熟练功、多拍、故弄玄虚、我用的、比你熟、多练等。"
    },
    "4yMlXbFTohR": {
        "duration": "0:52", "topic": "拍摄 · 对镜自拍",
        "practice": [
            ["说对镜要点", "1x zoom, step out a leg, hand on hip."],
            ["说挡脸技巧", "Cover the face when not wearing makeup."],
            ["说领口扭身", "Grab the collar and twist for a better shoulder line."],
            ["说借力伸腿", "Lean on something to stretch the legs farther."],
            ["说开膝搭框", "Open the knee on the phone side and hold the frame."]
        ],
        "pitfalls": [
            ["Use ultra-wide for mirror selfies.",
             "Switch to 1x zoom for a premium look.",
             "对镜拍用1倍焦段更高级。"],
            ["Show the bare face when no makeup.",
             "Cover the face with a hand.",
             "没化妆用手挡脸。"],
            ["Keep both legs closed.",
             "Open the knee or cross the legs.",
             "腿要开膝或交叉。"],
            ["Forget the shoulder line.",
             "Grab the collar or twist to shape the shoulders.",
             "抓领口扭身让肩线更好看。"],
            ["Hold the frame stiffly.",
             "Open the near knee and hold the door frame casually.",
             "搭门框时膝盖向侧面打开。"]
        ],
        "shifts": [
            ["说对镜拍只会说 mirror selfie",
             "用 1x zoom（一倍焦段）、hip hand（插腰）、collar grab（抓领口）"],
            ["说腿形只会说 leg shape",
             "用 step out（跨步）、cross the legs（交叉腿）、open the knee（打开膝盖）"],
            ["说比例只会说 proportion",
             "用 stretch farther（伸更远）、twist the body（扭身）、standard but safe（常规不出错）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：手机镜头一倍、对镜拍、高级、腿横着跨出去、肩膀距离、反手拨开衣服、插腰、凑近、没化妆、手挡脸、腿放前面、抓领口、上肩好看、扭身子、比例、撑着自己、腿伸得更远、穿裤子、膝盖打开、腿形、搭膝盖上、太刻意、扭胯、勾脚尖、更随意、胳膊打开、手机那边的膝盖、侧面打开、搭门框、趁脖子、很常规、不会出错等。"
    },
    "7JVAIoBNa1p": {
        "duration": "1:07", "topic": "拍摄 · 手部松弛感",
        "practice": [
            ["说支撑力", "The hand must have support—you control it."],
            ["说重量感", "The hand is a hanging weight under gravity."],
            ["说反重力", "An anti-gravity hand reads as tense."],
            ["说上行支撑", "Upward arms need support."],
            ["说下行放松", "Below the line, the wrist stays fully relaxed."]
        ],
        "pitfalls": [
            ["Force a supportive pose that looks stiff.",
             "Support alone isn't good—check the pose.",
             "光有支撑力并不好看。"],
            ["Hold the hand against gravity.",
             "Let it hang with a downward weightiness.",
             "反重力显得没放松。"],
            ["Keep the wrist tensed below the line.",
             "Fully relax the wrist in downward states.",
             "下行状态手腕要完全放松。"],
            ["Hold the bag stiffly.",
             "Let it hang naturally by your side.",
             "拿包要自然垂放。"],
            ["Ignore what hands read to viewers.",
             "Relaxed hands communicate relaxation.",
             "手的状态就是松弛的信号。"]
        ],
        "shifts": [
            ["说手只会说 hands",
             "用 hanging weight（悬挂重物）、weightiness（重量感）、support（支撑力）"],
            ["说紧张只会说 tense",
             "用 anti-gravity（反重力）、straining（使劲）、not relaxed（没放松）"],
            ["说摆姿只会说 pose",
             "用 below the parallel line（平行线以下）、downward state（下行状态）、relaxed wrist（放松手腕）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：松弛感、手咋摆、支撑力、控制它、好看、悬挂重物、挂在这儿、重量、重力、方向向下、反重力、常规认知、向下的重量感、没放松、使劲儿、小臂、向上的时候、支撑力、平行线以下、下行状态、手腕处、完全放松、长裙子、拿包、拿在手里、靠在身边、更好看等。"
    },
    "4MzhX0yzVfn": {
        "duration": "2:33", "topic": "拍摄 · 表情管理",
        "practice": [
            ["说大笑第一招", "Cover the nose tip with the index finger."],
            ["说下眼睑发力", "Squeeze the lower eyelid like doing aegyo-sal."],
            ["说替代手法", "Close eyes and scrunch the nose instead."],
            ["说头发氛围", "Lean the body and let the hair float."],
            ["说自然笑法", "Do something silly to trigger a real laugh."]
        ],
        "pitfalls": [
            ["Smile with a stiff, empty look.",
             "Weaken the mouth and engage the eyes.",
             "嘴僵眼空没感染力。"],
            ["Cover the nose too high.",
             "Keep the fingertip just two to three centimeters past the nose.",
             "挡鼻别挡太高。"],
            ["Open the eyes wide and round.",
             "Squeeze the lower eyelid into a curve.",
             "瞪圆眼反而感染力全无。"],
            ["Stand straight with hair stuck to the body.",
             "Lean and let the hair float for a joyful feel.",
             "直挺头发贴身难有氛围。"],
            ["Force a perfect smile on demand.",
             "Trigger a genuine laugh with silly actions.",
             "刻意笑不如诱发真笑。"]
        ],
        "shifts": [
            ["说笑只会说 smile",
             "用 natural smile（妈生感笑容）、big-smile cheat code（大笑作弊法）、live-in smile（活人感）"],
            ["说眼睛只会说 eyes",
             "用 lower eyelid contraction（下眼睑收缩）、aegyo-sal squeeze（卧蚕挤压）、crescent eyes（弯弯眼睛）"],
            ["说感染力只会说 appeal",
             "用 infectious（有感染力）、vibe（氛围感）、letting go（放任自己）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：超有感染力、妈生感笑容、普通人、表情管理、老师、看不下去了、抢页子、大笑作弊法、零基础学员、新手友好、教一步学一步、上课、奸笑不好看、挡起来、翘起食指、盖住鼻头、指尖超过鼻头、两三公分、笑得再狰狞再尴尬、挡在里面、看不到、别挡太高、弱化嘴巴、视觉中心、转移到眼睛、瞪得大大圆圆、眼睛很大很漂亮、感染力全无、下眼睑的收缩力、化卧蚕、被挤压、眼睛一弯、浓浓的笑意、透出来、学不来、下眼睑用力、闭起来、用力皱鼻子、五官挤成一团、感染力绝对无敌、大笑氛围感博主、用这招、氛围不够、头发来凑、极度开心、前仰后合、东倒西歪、头发甩来甩去、倾斜状态、直立状态、头发悬空、紧紧贴在身上、视觉上、传递给镜头、强烈的快乐情绪、感染力瞬间拉满、头发凌乱、活人感的关键、笑不自然、让笑自然发生、尴尬到不行、沙雕的行为、尴尬的舞蹈、坚持到30秒、崩不住、自己跟自己聊天、念叨搞笑的离谱的台词、挡着嘴巴、放任自己发疯、出片才是一道理等。"
    },
    "AWilXq57Cxe": {
        "duration": "0:51", "topic": "拍摄 · 剪刀手姿势",
        "practice": [
            ["说站姿公式", "Raise the hand, tilt the head, cover the mouth, cross legs."],
            ["说手部变化", "Two hands forward, lean, then slant again."],
            ["说腿内八", "Turn legs inward, hook a foot, keep thighs apart."],
            ["说坐姿公式", "Sit with legs crossed, put the peace sign down."],
            ["说地面公式", "One leg down, one leaning, hand on leg, bend waist."]
        ],
        "pitfalls": [
            ["Flash a plain peace sign.",
             "Add height, head tilt, mouth cover, and crossed legs.",
             "普通剪刀手太土。"],
            ["Hold both hands the same way.",
             "Lean forward, then slant them differently.",
             "两手动作要有变化。"],
            ["Keep the legs closed and stiff.",
             "Turn inward, hook a foot, open the thighs.",
             "腿要内八勾脚开大腿。"],
            ["Keep the peace sign while sitting.",
             "Put the hand down and cross the legs.",
             "坐姿放下剪刀手。"],
            ["Sit stiffly on the ground.",
             "Lean one leg over and bend the waist.",
             "地面要搭腿弯腰。"]
        ],
        "shifts": [
            ["说剪刀手只会说 peace sign",
             "用 de-cringe（去土味）、raise the hand high（举高）、formulas（公式）"],
            ["说站姿只会说 standing",
             "用 cross the legs（交叉腿）、inward legs（内八）、hook a foot（勾脚）"],
            ["说坐姿只会说 sitting",
             "用 legs crossed（盘腿）、lean over（靠过去）、bend the waist（弯腰）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：剪刀手、普通人、太普通、举高、歪头、挡嘴、交叉腿、两只手、往前放、微靠、斜着放、腿先内八、勾个脚、大腿分开、坐着、腿盘起来、跨过去、剪刀手放下、撑手、歪个头、坐在地上、一条腿放下面、另一条腿靠过去、手搭腿上、弯个腰、搞定、先学四个、太多记不住等。"
    },
    "onQfTgVIDF": {
        "duration": "0:55", "topic": "拍摄 · 视觉重量",
        "practice": [
            ["说视觉重量", "Body parts with volume carry visual weight."],
            ["说中心位", "Standing straight puts weight at the center."],
            ["说倾斜重量", "Lifting one side tilts the whole weight."],
            ["说砝码加对侧", "Add the gesture on the opposite side."],
            ["说平衡舒服", "Visual balance is what feels comfortable."]
        ],
        "pitfalls": [
            ["Let the pose tilt uncomfortably.",
             "Seek visual balance in every pose.",
             "倾斜过重看着难受。"],
            ["Add the gesture on the tilting side.",
             "Counterbalance on the opposite side.",
             "砝码要加在倾斜反方向。"],
            ["Overdo one gesture in a straight line.",
             "A single peace sign can throw you off-balance.",
             "剪刀手加错边失衡。"],
            ["Ignore the weight direction.",
             "Every volume points a weight direction.",
             "无视身体重量方向。"],
            ["Balance through hard stiffness.",
             "Balance through counter-actions, not tension.",
             "靠动作平衡而非僵硬。"]
        ],
        "shifts": [
            ["说摆姿只会说 pose",
             "用 visual weight（视觉重量）、counterweight（砝码）、balance（平衡）"],
            ["说身体只会说 body",
             "用 volume（体积）、center position（中心位）、tilt（倾斜）"],
            ["说动作只会说 move",
             "用 opposite direction（反方向）、pull the look back（往回拉）、female poses（女性动作）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：视觉重量感、摆姿更上镜、身体的每一个部分、有体积、重量的存在、站直、中心位、腰弯、哪边重、翘起来、重量非常斜、往这边倾斜、视觉上追求平衡、舒服、不能偏得很难受、手部动作、砝码、加在这边、视觉上舒服、整个人更往这边去、交叉腿、女性动作、身体往这边斜、加剪刀手、一条线、冲到那边去、不如这边加效果好、视觉上面往回拉、反方向去做动作等。"
    },
    "2KZdBWgvYi6": {
        "duration": "0:47", "topic": "拍摄 · 手势技巧",
        "practice": [
            ["说核心口诀", "Frame when you can, cover when you can."],
            ["说框架手势", "A classic gesture with built-in framing."],
            ["说遮挡手势", "A classic gesture with covering width."],
            ["说两个位置", "Frame or cover the eyes and the mouth."],
            ["说举一反三", "Quiz yourself on how you'd shoot someone."]
        ],
        "pitfalls": [
            ["Memorize gestures without logic.",
             "Learn the frame-or-cover rule.",
             "只记手势不懂逻辑。"],
            ["Frame where there's no frame.",
             "Only frame or cover the eyes and mouth.",
             "框挡只对眼睛嘴巴。"],
            ["Cover everything with the hand.",
             "Frame with one gesture, cover with another.",
             "遮挡宽度和框架结构要分清。"],
            ["Stop at the demo.",
             "Apply the rule to any subject.",
             "学完要举一反三。"]
        ],
        "shifts": [
            ["说拍照只会说 shoot",
             "用 frame（框）、cover（挡）、two positions（两个位置）"],
            ["说手势只会说 gesture",
             "用 framing structure（框架结构）、covering width（遮挡宽度）"],
            ["说学习只会说 learn",
             "用 the mantra（口诀）、demo（示范）、quiz（考考你）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：超简单的拍照方法、能框就框、能挡则挡、伸出右手、经典拍照手势、自带框架结构、不具备遮挡宽度、具备遮挡宽度、框架结构不够、有框架的去框、能遮挡的去挡、框哪儿挡哪儿、两个位置、眼睛、嘴巴、示范给你看、学会了、考考你、如果是他、怎么拍等。"
    },
    "35OmCyKrgwL": {
        "duration": "1:09", "topic": "拍摄 · 男生姿势",
        "practice": [
            ["说站姿要点", "Hand in pocket, one leg out, toe pointing."],
            ["说挑肩细节", "Lift one shoulder just a little."],
            ["说拿饮品", "Pinch the cup, not the whole hand, raise the elbow."],
            ["说坐姿要点", "Spread legs, feet together, one hand on cheek."],
            ["说走路姿势", "Weight centered, pace back and forth."]
        ],
        "pitfalls": [
            ["Face the lens rigidly with arms down.",
             "Relax, pocket the hand, extend a leg.",
             "僵硬站立不插袋。"],
            ["Grip the cup with the whole hand.",
             "Pinch it and raise the elbow.",
             "整个手抓杯显笨重。"],
            ["Sit with legs squeezed together.",
             "Spread the legs but keep the feet together.",
             "坐姿夹腿不自然。"],
            ["Actually walk for the shot.",
             "Pretend to walk, pacing in place.",
             "走路姿势要假装走。"],
            ["Keep hands dangling.",
             "Use pocket, collar, and head-scratch moves.",
             "手要插兜领口挠头。"]
        ],
        "shifts": [
            ["说姿势只会说 pose",
             "用 beginner guide（入门教学）、standing/sitting/walking（站坐走）"],
            ["说手只会说 hands",
             "用 pocket（插兜）、pinched hold（捏取）、elbow up（抬肘）"],
            ["说细节只会说 detail",
             "用 toe pointing（脚点地）、lift a shoulder（挑肩）、feet together（脚并拢）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：评论区、男生拍照姿势、站坐走、入门级教学、准备好了、第一步、放松、手插进口袋、伸出一条腿、脚插点地、挑起一点点肩膀、爱喝饮料吗、拿着、不要整个拿着、纸缚拿、手肘抬起来、喝一会、坐下、腿分开、脚并拢、一只手撑脸、一只手搭腿、看镜头还是看旁边、都可以、好了走吧、假装地走、重心放在两腿中间、前后来回地走、插兜、领口、挠头、男生、学会了吗等。"
    },
    "69r5cR6sEpk": {
        "duration": "1:09", "topic": "拍摄 · 摆姿纠错",
        "practice": [
            ["说正面改侧", "Try a profile or head tilt instead of front-facing."],
            ["说松胯挑肩", "Loosen the hips and lift the opposite shoulder."],
            ["说上身胖正面", "Arms back, chest forward, face the front."],
            ["说比例拉伸", "Legs forward, body back for better proportions."],
            ["说生命力动作", "Bend down and kick the leg up."]
        ],
        "pitfalls": [
            ["Face the lens straight on every time.",
             "Try a profile or tilted head now and then.",
             "永远正面看镜头。"],
            ["Go puffed and rigid at the shutter.",
             "Loosen the hips and lift the opposite shoulder.",
             "一拍照就发胀僵硬。"],
            ["Side-shoot a fuller upper body.",
             "Arms back, chest forward, face front.",
             "上身胖拍侧面反显壮。"],
            ["Pose tall for poor proportions.",
             "Extend legs forward, pull the body back.",
             "比例不好别摆舒展姿势。"],
            ["Stay stiff when aiming for vitality.",
             "Bend and kick the leg up.",
             "想拍生命力却僵硬。"]
        ],
        "shifts": [
            ["说错误姿势只会说 wrong pose",
             "用 front-facing（正面）、stiff（僵硬）、puffed（发胀）"],
            ["说修正只会说 fix",
             "用 profile（侧脸）、loosen the hips（松胯）、opposite shoulder（对侧肩）"],
            ["说比例只会说 proportion",
             "用 near bigger far smaller（近大远小）、legs forward（腿前伸）、body back（身后拉）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：拍照为什么不好看、看镜头、正面看镜头、侧脸、歪头、生动了一点点、发胀、胯松一松、对角的肩膀挑一挑、身体有层次、好看很多、上身胖、非得拍侧面吗、胳膊向后方、胸腔转过来、人正一点、不见嫌瘦、动作舒缠、比例不好、拍全身、腿往前伸、身体往后拉、近大加远小、上镜好比例、想拍生命力、贼僵硬、弯腰、再弯腰、腿踢起来、生命力的诀窍、还早着呢等。"
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
