#!/usr/bin/env python3
"""批27：为简化场景JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "ziyouyong-gaozhou-baoshui": {
        "practice": [
            ["说不抱90度", "Don't catch the water at 90 degrees—it hurts your shoulder."],
            ["说正确抱水", "Lead with the shoulder, reach forward, catch diagonally."],
            ["说不过中线", "Keep the hand inside the centerline and rotate the shoulder."],
            ["说肩的交替", "Alternate the shoulders side to side in the catch."]
        ],
        "pitfalls": [
            ["Catching at 90 degrees.",
             "It strains the shoulder joint.",
             "抱90度会让肩关节疼。"],
            ["Reaching across the centerline.",
             "Keep the hand inside the shoulder line for balance.",
             "手不要过身体中线。"],
            ["Pressing down at entry.",
             "Lead with the shoulder and catch diagonally instead.",
             "入水后不要立刻下压。"],
            ["Forgetting the shoulder roll.",
             "Rotate the shoulder as you push and lead it forward.",
             "推水时转肩送肩前伸。" ]
        ],
        "shifts": [
            ["说抱水只说 catch",
             "用 catch the water（抱水）、lead with the shoulder（送肩）、centerline（中线）"],
            ["说肩膀只说 shoulder",
             "用 rotate（转动）、alternate（交替）、diagonally（斜向地）"]
        ],
        "footer": "转录基于图文实录完整口播（繁体字幕）。已校正：抱水不要抱90度会导致肩关节疼、正确动作是送肩前伸往斜下方抱水、抱水时不要过身体中线、推水时转肩送肩前伸、两边肩转换交替才是正确的自由泳抱水等。"
    },
    "ziyouyong-kaiwu-5moments": {
        "practice": [
            ["说重心前移", "Reach slightly forward and down, and the body floats up."],
            ["说转体带动滑手", "No matter how hard you pull, rolling the body does more."],
            ["说高肘抱水", "Anchor the upper arm and let the bent forearm sink to catch."],
            ["说转头换气", "Turn the head with the body roll to breathe naturally."],
            ["说打腿的意义", "Kick to keep balance and the streamline, in rhythm with the roll."]
        ],
        "pitfalls": [
            ["Pressing down right after entry.",
             "Anchor the upper arm and sink the bent forearm to catch.",
             "入水后不要立刻下压。"],
            ["Pulling with arms only.",
             "The body roll carries the pulling hand.",
             "转体带着手走。"],
            ["Lifting the head to breathe.",
             "Turn the head with the roll—don't lift it.",
             "转头不抬头。"],
            ["Kicking desperately for speed.",
             "Kick for balance and streamline, in rhythm with the roll.",
             "打腿是为了平衡和流线。" ]
        ],
        "shifts": [
            ["说划水只说 pull",
             "用 body roll（转体）、catch（抱水）、anchor（固定）"],
            ["说换气只说 breathe",
             "用 turn the head（转头）、surface（露出水面）、rhythm（节奏）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：自由泳突然开悟的五个瞬间、一重心前移身体平直（手入水后往前下方伸一点身体自然上浮）、二转体带动滑手（再用力滑手不如转体手被转动带着走）、三高肘抱水（大臂内侧固定屈轴小臂下滑抱水第一次感觉推水推着走）、四换气轻松（转头不抬头随身体转动自然换气节奏稳定）、五不用拼命打腿（打腿是维持平衡和流线随身体滚动有节奏打腿反而更轻松平稳）等。"
    },
    "dieyong-baoshui": {
        "practice": [
            ["说多视角的重要性", "Side view shows angles; front view shows symmetry—use both."],
            ["说45度入水", "The entry and reach angle is marked at about 45°."],
            ["说90度高肘", "The catch holds the elbow at about 90°."],
            ["说前视对称检查", "Check that both hands stay in sync in the front view."],
            ["说绿勾路径", "The green check links the still angles into the full hand path."]
        ],
        "pitfalls": [
            ["Trusting one angle only.",
             "Side and front views carry different information.",
             "只看一个视角会把局部当全部。"],
            ["Taking 45°/90° as hard rules.",
             "They're visual anchors, not competition rules.",
             "数字是观察锚点不是竞赛规则。"],
            ["Drilling only the middle frame.",
             "Watch entry → catch → outward sweep as one path.",
             "要连起来看完整手部路径。"],
            ["Copying the angles with shoulder issues.",
             "Youth and rehab swimmers may need more conservative angles.",
             "青少年或康复期需更保守的肘角。" ],
            ["Trusting unclear narration.",
             "Rely on the on-screen marks; verify disputes with a coach.",
             "口播听不清时以画面标注为准。" ]
        ],
        "shifts": [
            ["说划水只说 feel the pull",
             "用 underwater angles（水下角度）、entry angle（入水角）、elbow angle（肘角）"],
            ["说判断只说 right",
             "用 visual anchor（观察锚点）、in sync（同步）、sweep（外划）"]
        ],
        "footer": "转录来自图文实录与理性分析SVG。本片无口播，内容重建自画面叠字与笔记：多视角看蝶泳抱水（侧视给45°入水前伸角与90°高肘抱水角、前视检查左右手同步对称、绿勾段把静帧连成蝶泳手部动作完整路径）、口播听不清以叠字为准、数字是观察锚点而非竞赛规则、青少年或伤后康复需更保守肘角、22秒无法覆盖呼吸波浪腿部配合等。"
    },
    "rushui-diezhou-chain": {
        "practice": [
            ["说跌肘的连锁反应", "Dropped elbow at entry leads to a sinking reach and a slipped catch."],
            ["说根源是掉肩", "The root cause is the shoulder dropping before the hand enters."],
            ["说正确入水顺序", "The correct order is hand, elbow, shoulder."],
            ["说肩撑住的意义", "Hold the shoulder at entry, and you hold the elbow too."],
            ["说斜插入水", "Enter at an angle with the wrist rotated out to prop the elbow."]
        ],
        "pitfalls": [
            ["Entering with the elbow first.",
             "Eight of ten adults drop the elbow—check your shoulder height.",
             "十个成人八个肘先入水。"],
            ["Dropping the shoulder at entry.",
             "The shoulder must ride high until the hand touches water.",
             "入水时肩先掉是根源。"],
            ["Using a flat entry.",
             "Angled entry with a turned-out wrist props the elbow up.",
             "平插入水容易跌肘。"],
            ["Ignoring the entry order.",
             "Hand → elbow → shoulder; never shoulder first.",
             "正确顺序是手肘肩。" ],
            ["Blaming the elbow alone.",
             "Shoulder down means elbow down—fix the shoulder first.",
             "肩掉就等于肘掉。" ]
        ],
        "shifts": [
            ["说入水只说 enter",
             "用 dropped elbow（跌肘）、sinking reach（前伸沉肘）、slipped catch（抱水溜肘）"],
            ["说肩只说 shoulder",
             "用 ride high（撑在水面）、support（撑住）、follow（跟随）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：自由泳跌肘十个成人八个肘先入水、入水有啪啪声、减阻不可能还会导致前伸沉肘、跌肘罪恶之源是掉肩、正确动作移臂入水时肩膀在水面上、手入水后随前伸肩膀才转下去、正确顺序是手肘肩、跌肘者手未入水肩已先入水、肩入水带动大臂入水大臂入水肘先入水、移臂入水过程肩一定要撑住、肩撑住等于肘撑住、第二个因素是手入水姿态、柔韧性一般成年人平插容易跌肘、建议斜插入水手掌手腕向外侧转一点肘就撑起来、平插更容易肘部掉下来等。"
    },
    "ziyouyong-huashou-baoshui": {
        "practice": [
            ["说弯肘的误区", "A bent elbow is just the look—internal rotation drives the catch."],
            ["说正确链条", "Rotate the upper arm inward, spread the blade, reach forward."],
            ["说抱球口诀", "Imagine hugging a ball—leave its space by your chest."],
            ["说自检方法", "Whisper 'hug the ball' before every pull to self-check."]
        ],
        "pitfalls": [
            ["Thinking a bent elbow is enough.",
             "The red X marks 'no internal rotation' even with the bend.",
             "弯肘只是外形，内旋才是关键。"],
            ["Rotating without spreading the blade.",
             "The chain is rotation → blade spread → reach.",
             "正确链条是内旋+外展+前伸。"],
            ["Copying the drill with shoulder pain.",
             "A 17-second kneeling demo isn't for everyone.",
             "肩伤者不应照搬幅度。"],
            ["Trying to change everything at once.",
             "Migrate the shape and feel first; speed comes later.",
             "先迁移形状与体感，别一次改全部。" ]
        ],
        "shifts": [
            ["说抱水只说 bend the elbow",
             "用 internal rotation（内旋）、shoulder blade（肩胛骨）、high-elbow catch（高肘抱水）"],
            ["说感受只说 feel",
             "用 hug a ball（抱球）、self-check（自检）、muscle memory（肌肉记忆）"]
        ],
        "footer": "转录来自图文实录与理性分析SVG。本片无口播（17秒跪姿示意），内容重建自画面标注：弯肘姿态上仍打红叉并写大臂无内旋、弯肘只是外形内旋才是驱动抱水的关键转动、正确链条为大臂内旋到肩胛外展到肩膀前伸叠加形成高肘抱水、体感口诀是想象抱住一颗球肘腕与胸口留出球的空隙、本片不含水中阻力呼吸侧转与全身配合、肩伤或医嘱限制者不应照搬幅度、口播不可辨力学效果为教学推断非实测等。"
    },
    "hexin-buwen-cuowu-zhuan": {
        "practice": [
            ["说核心不稳的表现", "Swimming with the core swinging like a hammock is core instability."],
            ["说错误根源", "The problem is body-rolling instead of shoulder-rolling."],
            ["说正确转动", "Roll the shoulders first and let the body follow."],
            ["说水中练习", "Lie flat, reach, and let the arm turn the shoulder, the shoulder tilt the body."],
            ["说核心状态", "The core stays lengthened and braced—no sag, no twist."]
        ],
        "pitfalls": [
            ["Blaming weak core strength.",
             "The real cause is rolling the body, not the shoulders.",
             "不是核心差，是转体游而非转肩游。"],
            ["Thinking 'pull left, pull right'.",
             "That flips the body and destabilizes the core.",
             "滑手转左转右会让身体翻面。"],
            ["Powering the roll from the core.",
             "An engine core can't also stay stable.",
             "用核心发力又想核心稳定几乎不可能。"],
            ["Twisting the hip to turn the shoulder.",
             "The shoulder band leads—the hip follows.",
             "是肩带宽，不是髋带肩。" ]
        ],
        "shifts": [
            ["说核心只说 core strength",
             "用 core instability（核心不稳）、brace（收紧）、lengthen（拉长）"],
            ["说转动只说 rotate",
             "用 body roll（转体）、shoulder roll（转肩）、shoulder band（肩带）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：游自由泳时核心像在水里荡秋千叫核心不稳、问题不是核心力量差而是转体游而非转肩游、主观转体时发力点在核心导致核心又发力又做动作无法稳定、正确转动是转肩带着身体转、每一次前伸推水让肩膀滚动起来身体跟随、主力军是肩膀联动、水中练习趴平手臂一前一后前伸手向前伸胳膊带肩转肩带身体侧倾、是肩带宽而不是髋先转带肩拧、核心拉长收紧不塌不扭就不会荡秋千、重点转肩游而非转体游肩带宽而不是宽带肩等。"
    },
    "zilv-1348-days": {
        "practice": [
            ["说指出跑姿问题", "You heel-strike too much, your torso is loose, and you look up."],
            ["说最大的问题", "Heel-striking plus a low cadence will hurt your knees over time."],
            ["说提升步频", "Your cadence is 160—get it above 180."],
            ["说小碎步落地", "Take small shuffle steps and land with the whole foot."],
            ["说摆臂", "Fix the elbow and swing front and back, bending under 90°."],
            ["说头部要点", "Breathe in, chest up, eyes down—don't lift your chin."]
        ],
        "pitfalls": [
            ["Heel-striking every step.",
             "It's braking with every step and loads the knees.",
             "脚后跟落地多，膝盖会受伤。"],
            ["Running with a loose torso.",
             "Brace the belly to stabilize the upper body.",
             "上身没收紧是脚后跟落地的原因。"],
            ["Leaving cadence at 160.",
             "Get it above 180 to spare the joints.",
             "步频160太低，要180以上。"],
            ["Punching the arms down when swinging.",
             "Fix the elbow and swing front and back.",
             "摆臂要前后送不是往下敲。" ],
            ["Letting the head creep up when tired.",
             "Keep your eyes down and the neck tucked.",
             "疲劳时头容易上扬，要往下看。" ]
        ],
        "shifts": [
            ["说跑姿只说 posture",
             "用 form（跑姿）、cadence（步频）、heel-strike（脚后跟落地）"],
            ["说指导只说 coach",
             "用 brace the belly（收紧腹部）、shuffle steps（小碎步）、streamline（流线型）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：街头教练主动指出跑姿问题（脚后跟落地偏多、上身没收紧、仰着头）、最大问题是脚后跟落地加上步频低跑久膝盖会受伤、脚后跟落地源于上身未收紧包括小腹、步频从160要提到180以上、练小碎步找全脚掌落地不要点脚尖、张开手臂找平衡像机器人直上直下走、摆臂不是往下敲而是固定手肘前后送弯曲小于90度、吸气挺胸头看斜下方不要扬头、一疲劳头就上扬、练后步频从160升到166接近180、保持住越来越好等。"
    },
    "dabu-liuxing-songkuan": {
        "practice": [
            ["说大步流星的真相", "It's hip drive, not stride length, that sends you forward."],
            ["说能力前提", "You need hip mobility, glute drive and core stability."],
            ["说正摆腿", "Hold the rail and swing big, 20 per side."],
            ["说后蹬跑", "Push off hard for 20 meters, driving the leg and hip forward."],
            ["说弓箭步走", "Walk slowly with long strides to consolidate hip drive."]
        ],
        "pitfalls": [
            ["Swinging the shin far forward.",
             "The feeling comes from the push-off, not reaching far.",
             "大步流星的体感来自后蹬不是伸腿。"],
            ["Expecting instant hip drive from one drill.",
             "Without mobility, drive and stability it's very hard.",
             "没有髋活臀驱动力核心稳定很难做出来。"],
            ["Treating drills as the whole program.",
             "The drills are an entry—track mobility and push-off quality.",
             "动作是入口，要记录能力指标。"],
            ["Swinging out of control.",
             "Controlled big arcs over wild flailing.",
             "以可控大弧度为主。" ],
            ["Losing the core during cross-swings.",
             "Lock the ribs and pelvis first.",
             "交叉摆腿时核心必须在线。" ]
        ],
        "shifts": [
            ["说步幅只说 stride length",
             "用 hip drive（送髋）、push-off（后蹬）、propulsion（推进）"],
            ["说训练只说 drill",
             "用 leg swing（摆腿）、cross kick（交叉踢腿）、walking lunge（弓箭步走）"]
        ],
        "footer": "转录来自图文实录与理性分析SVG。本片口播听不清，内容重建自画面大字、动作示范与笔记：大步流星体感来自后蹬把人送出而非伸腿够远、笔记写没有髋活臀驱动力核心稳定很难做得出来、送髋是综合能力不是单个花样动作、五项跟练为正摆腿（每侧20次）、俯卧交叉摆腿、交叉踢腿（每侧20次）、快速后蹬跑（20米）、弓箭步行走、训练日志记髋活动幅度后蹬是否干脆核心是否塌、动作是入口实际效果取决于能力前提是否补齐等。"
    },
    "paobu-zhengque-luodi": {
        "practice": [
            ["说脚后跟落地的坏处", "Heel-first landing is braking—no shock absorption."],
            ["说哪里先着地", "We land with the whole foot, sole parallel to the ground."],
            ["说小腿垂直", "With the shin vertical, a full-foot landing is possible."],
            ["说落地支撑", "Shift weight onto the forefoot and hit an effective support point."]
        ],
        "pitfalls": [
            ["Heel-striking every step.",
             "It's braking with no shock absorption.",
             "脚后跟先落地就是刹车。"],
            ["Landing on the forefoot only.",
             "The answer is the whole foot, sole parallel.",
             "答案是全脚掌着地。"],
            ["Bending the shin at landing.",
             "Keep the shin vertical for a full-foot landing.",
             "小腿要垂直地面。"],
            ["Carrying weight on the heel while moving.",
             "Moving weight sits on the forefoot, standing it's on the heel.",
             "前移时重心在前脚掌。" ]
        ],
        "shifts": [
            ["说落地只说 landing",
             "用 whole-foot landing（全脚掌落地）、forefoot（前脚掌）、shin vertical（小腿垂直）"],
            ["说支撑只说 support",
             "用 support point（支撑点）、center of gravity（重心）、shift weight（转移体重）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：脚后跟先入地是刹车每跑一步再刹车一次、脚后跟没有减震功能没有弹性、答案是全脚掌着地鞋底与地面平行小腿垂直地面才有可能、落地瞬间把体重都移动到前脚掌做支撑、站直时重心在脚后跟上、向前移动时重心在前脚掌上、落的每一步都要落到有效的支撑点等。"
    },
    "running-form-errors": {
        "practice": [
            ["说背手跑的性质", "Hands-behind running is a drill to force an upright trunk."],
            ["说错误一趴着跑", "Hunching means over-leaning with the trunk folded down."],
            ["说错误二伸腿跑", "Reaching flings the shin forward and slams the heel."],
            ["说目标三要素", "Upright torso, hip-flexed lift, stable ankles."],
            ["说行动清单", "Film yourself, match the drill, and recheck with three points."]
        ],
        "pitfalls": [
            ["Treating drills as race form.",
             "Hands-behind is a drill, not your everyday running posture.",
             "背手跑是训练钻不是比赛跑姿。"],
            ["Chasing a bigger stride.",
             "Bigger steps often mean reaching and braking.",
             "步幅越大不等于越快。"],
            ["Hunching forward to go fast.",
             "It over-leans the trunk; fix with hands-behind drills.",
             "过度前倾是错误一。"],
            ["Flailing the shin forward.",
             "Lift the leg up instead of flinging the shin.",
             "提拉抬腿替代向前甩小腿。" ],
            ["Pushing drills with joint pain.",
             "Those with knee/ankle pain shouldn't increase drill intensity.",
             "有膝踝伤痛者不宜加大钻强度。" ]
        ],
        "shifts": [
            ["说跑姿只说 posture",
             "用 hunching（趴着跑）、reaching（伸腿跑）、hands-behind（背手跑）"],
            ["说纠正只说 fix",
             "用 muscle memory（肌肉记忆）、drill（训练钻）、three-point target（三要素）"]
        ],
        "footer": "转录来自图文实录与理性分析SVG。本片口播不可辨，内容重建自画面大字、红叉绿勾与笔记：背手跑是训练钻用来逼出直立躯干与屈髋不是正式跑姿、错误一是趴着跑（过度前倾躯干趴下去）纠正为背手跑、错误二是伸腿跑（小腿抢到身前、后脚跟落地、膝踝压力大刹车制动）纠正为提拉抬腿、目标姿态三要素为上体垂直屈髋抬腿脚踝稳定、行动为侧向录10-20秒慢跑对照、按错误类型选钻、恢复摆臂后用三要素复检、有膝踝伤痛或平衡障碍者不宜盲目加大纠正钻强度等。"
    }
}

for slug, extra in EXTRA.items():
    p = DATA / f"{slug}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["practice"] = extra["practice"]
    d["pitfalls"] = extra["pitfalls"]
    d["shifts"] = extra["shifts"]
    d["footer_notes"] = extra["footer"]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ {slug}: practice={len(d['practice'])} pitfalls={len(d['pitfalls'])} shifts={len(d['shifts'])}")
print("完成")
