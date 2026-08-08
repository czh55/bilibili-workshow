#!/usr/bin/env python3
"""批26：为简化场景JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "songkuan-4tips": {
        "practice": [
            ["说送髋训练第一步", "Step one: lean off the wall and squat to fire the glutes."],
            ["说起身抬腿", "As you rise, drive the opposite knee and swing your arms."],
            ["说单腿支撑", "Balance on one leg, raise the knee to 90° and extend back."],
            ["说原地摆臂送髋", "At the moment of the swing, drive the rear hip forward."],
            ["说收尾感受", "My hips are burning—that's the glutes finally working."]
        ],
        "pitfalls": [
            ["Skipping the glute warm-up.",
             "Hip drive needs activated glutes first—15 wall lunges first.",
             "送髋要先激活臀肌。"],
            ["Swinging your whole body instead of the hip.",
             "Only the rear hip drives forward with the arm swing.",
             "只有后侧髋向前带。"],
            ["Rushing the movement.",
             "The coach repeats: keep it slow and controlled.",
             "不要快，要控制节奏。"],
            ["Forgetting core tension.",
             "Core tight + hip drive is the pairing that transfers power.",
             "核心收紧+髋带动。"],
            ["Thinking big muscles mean fast running.",
             "Speed comes from transferring strength, not just muscle size.",
             "快慢靠力量转化。" ]
        ],
        "shifts": [
            ["说跑步训练只说 run",
             "用 hip drive（送髋）、glute activation（臀肌激活）、single-leg support（单腿支撑）"],
            ["说力量只提 strength",
             "用 transfer（转化）、explosion（爆发力）、fire up（激活）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：练送髋先做靠墙弓步蹲激活臀部、踩住小椅子的变式、起身瞬间抬对侧腿摆臂、单腿支撑抬到90度向后伸展保持平衡、原地摆臂时后侧髋关节向前带一下、核心收紧髋关节带一点不要快、练完臀部燃烧感明显、跑得快的运动员靠力量转化而非死肌肉等。"
    },
    "running-hip-drive": {
        "practice": [
            ["说不送髋的后果", "Without hip drive, you sit back, heel-strike and risk knee injuries."],
            ["说什么是送髋", "Drive the hip forward as you run—that's sending the hip."],
            ["说落地瞬间", "At landing, foot, hip and head form one vertical line."],
            ["说背后有人推的意象", "Feel like someone's hand is pushing your back forward."],
            ["说送髋的效果", "Run with hip drive and you feel half as tired."]
        ],
        "pitfalls": [
            ["Sitting back into the hip.",
             "That loads the rear hip and heel-strikes—a recipe for injury.",
             "后腿趋髋下坐是错的。"],
            ["Pumping only the legs.",
             "Hip drive plus a forward lean is the whole picture.",
             "送髋要配合整体前倾。"],
            ["Overthinking the cue.",
             "The 'hand pushing your back' image does the work for you.",
             "想象有人推你往前走。"],
            ["Forgetting the vertical line at landing.",
             "Foot, hip and head aligned keeps the chain efficient.",
             "落地瞬间三点成一线。" ]
        ],
        "shifts": [
            ["说跑步只讲腿",
             "用 hip drive（送髋）、forward lean（前倾）、vertical line（竖直直线）"],
            ["说省力只说 save energy",
             "用 feel half as tired（省力一半）、lighten up（变轻松）"]
        ],
        "footer": "转录基于图文实录口播（繁体字幕）。已校正：不送髋会造成后腿趋髋下坐、脚后跟先着地、身体向前侵入导致膝髋关节运动损伤、跑动时髋关节向前顶出去就是送髋、整体前倾落地瞬间脚髋头在一条竖直直线、时刻想象有人用手推着背往前走、跑步送髋跑出风速省力一半等。"
    },
    "running-leg-fold": {
        "practice": [
            ["说正确折叠的位置", "The correct fold happens with thigh and shin under your body."],
            ["说错误后撩的位置", "A wrong kick-back happens behind your hips."],
            ["说折叠的动力学", "Your weight lands above the foot, then passes it quickly."],
            ["说后撩的坏处", "Kick-back flings the shin forward and creates braking."],
            ["说大腿位置的区别", "Thigh forward moves your weight forward; trailing thigh stalls it."],
            ["说腘绳肌的作用", "Fire the hamstring the instant your foot lands to fold the shin."]
        ],
        "pitfalls": [
            ["Confusing fold with kick-back.",
             "Fold happens under the body; kick-back happens behind it.",
             "折叠在身体下方，后撩在臀部后方。"],
            ["Letting the shin fling forward.",
             "Inertia carries the shin past your center and brakes you.",
             "小腿甩到重心前面会产生制动。"],
            ["Leaving the thigh behind.",
             "A trailing thigh means the weight can't move forward.",
             "大腿在后面重心前不去。"],
            ["Waiting to fire the hamstring.",
             "A late hamstring makes you push off and drag your legs.",
             "腘绳肌发力不及时会拖腿。"],
            ["Kicking back to feel fast.",
             "It adds ground contact time and makes you heavier, not faster.",
             "后撩会增加触地时间。" ]
        ],
        "shifts": [
            ["说跑步腿累只说 legs tired",
             "用 fold（折叠）、kick-back（后撩）、ground contact time（触地时间）"],
            ["说后腿力量只说 hamstrings",
             "用 fire the hamstring（腘绳肌发力）、trail behind（拖在后面）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：跑步腿沉拖沓通常是折叠与后撩分不清、正确折叠是大腿小腿在身体下方产生、错误后撩是在臀部后方产生、身体前倾失衡时折叠能让重心更快过脚、后撩会因惯性把小腿甩到重心前面产生制动并增加触地时间、折叠时大腿在躯干前侧而折叠时大腿在前重心更快向前、做到正确折叠靠腘绳肌发力积极让小腿瞬间向上折叠、腘绳肌发力不积极会蹬地拖腿、腘绳肌越积极折叠越好脚落身体下方跑得更轻松等。"
    },
    "coffee-latte-art-swing": {
        "practice": [
            ["说翻车的真正原因", "90% of latte art fails come from the swing, not the milk."],
            ["说正确摆动", "Keep the arm steady and rock the wrist into an S-curve."],
            ["说握缸手法", "Three back fingers on the handle, elbow level with your shoulder."],
            ["说发力要点", "The lighter and more relaxed, the finer the pattern."],
            ["说三天练习计划", "Day one water S-curves, day two stationary swing, day three retreat."],
            ["说实战收尾", "Pour low, swing, and slowly pull back for a crisp leaf."]
        ],
        "pitfalls": [
            ["Blaming the milk first.",
             "90% of failures are the swing, not the milk froth.",
             "翻车90%是摆动不是奶泡。"],
            ["Shaking the whole hand.",
             "That's just pouring unevenly—the wrist should do the rocking.",
             "整只手摇不是摆动。"],
            ["Forcing power into the swing.",
             "Lighter and more relaxed gives finer, clearer lines.",
             "发力越轻纹路越细腻。"],
            ["Retreating too fast on day three.",
             "Never speed up the retreat; keep one steady tempo.",
             "后退不加速，全程节奏统一。"],
            ["Ignoring consistent width and frequency.",
             "Uneven width and speed make the leaf pattern messy.",
             "宽幅频率不一致纹路会乱。" ]
        ],
        "shifts": [
            ["说拉花失败只说 milk",
             "用 swing（摆动）、froth（奶泡）、rhythm（节奏）"],
            ["说练习只说 practice",
             "用 stationary swing（定点摆动）、retreat（后退）、S-curve（S形水流）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：新手拉花翻车90%是摆动不会而非奶泡问题、核心原因是手腕发力导致摆动节奏乱、正确摆动是手臂稳手腕晃水流呈现S形、中指无名指小拇指放奶缸把手上手肘与肩齐平靠后方三指摆动、摆动是手腕惯性运动发力越轻纹路越细腻、第一天玩水练S形每天三组每组一分钟不抖、第二天空杯定点摆动只摆不退观察波纹、第三天摆动加后退摆动不停后退不加速、实战压低出杯边摆边回杯流量均匀不刻意发力、摆动宽幅流量频率一致得到树叶拉花等。"
    },
    "gaozhou-jueding-meichou": {
        "practice": [
            ["说高肘移臂的正确做法", "The elbow clears the water first, pointing forward, forearm relaxed."],
            ["说举手移臂的错误做法", "The hand leads, the elbow drops and the armpit disappears."],
            ["说腋窝参照信号", "A visible armpit at recovery signals the elbow-led motion."],
            ["说如何练习", "Lift the elbow before the hand and keep the forearm relaxed."],
            ["说审美与技术的边界", "This video defines 'looks good', not 'works fast'."]
        ],
        "pitfalls": [
            ["Reducing recovery to 'get the hand forward'.",
             "It's an ordered chain: elbow first, relaxed forearm follows.",
             "移臂是顺序动作，肘先动。"],
            ["Treating 'beauty' as a speed result.",
             "The verdict is aesthetic, with no speed or safety data.",
             "「美丑」是审美判断不是技术指标。"],
            ["Lifting the hand first.",
             "That hides the elbow, raises the forearm and ends in hand slaps.",
             "手先抬会藏肘并导致拍水。"],
            ["Forcing the forearm up.",
             "The forearm should stay relaxed and hang naturally.",
             "小臂要放松自然下垂。" ],
            ["Slapping the water to finish the recovery.",
             "Aim for a smooth path close to the body back to extension.",
             "避免手掌拍水。" ]
        ],
        "shifts": [
            ["说移臂只说 move your arm",
             "用 recovery（移臂）、high elbow（高肘）、armpit（腋窝）"],
            ["说判断只说 right or wrong",
             "用 aesthetic judgment（审美判断）、subjective（主观的）、verifiable（可验证的）"]
        ],
        "footer": "转录来自图文实录与理性分析SVG。本片无口播，Whisper仅识别到背景配乐的幻觉字幕，内容重建自画面文字条与动作对比：高肘移臂为视频认定的正确做法（肘尖前顶、小臂放松、腋窝可见）、举手移臂为错误做法（手掌先抬、小臂高举、藏腋窝）、13秒分屏对照、标题「高肘决定美丑」是审美评价而非客观技术结论、练习时让肘先离水保持小臂放松对镜检查腋窝、避免手掌拍水、把好看与有效分开验证等。"
    },
    "hexin-shoujin-teaching": {
        "practice": [
            ["说吸肚子的问题", "Sucking in leaves your ribs flared and the core loose."],
            ["说蜡烛吹气", "Blow at an imaginary candle to pull the lower ribs in."],
            ["说咳嗽激活", "Cough twice to fire the transversus abdominis."],
            ["说嘶音维持", "Hiss with steady resistance to hold the tension."],
            ["说验收标准", "The whole midsection should feel hard, not just the surface."]
        ],
        "pitfalls": [
            ["Equating sucked-in belly with a braced core.",
             "Flared ribs prove the deep stabilizers aren't engaged.",
             "吸肚子不等于收紧核心。"],
            ["Holding your breath to brace.",
             "Breath-driven bracing is closer to real functional activation.",
             "呼吸驱动比憋气更接近功能性激活。"],
            ["Only flattening the surface.",
             "Acceptance requires the entire waist to feel hard.",
             "验收是腰腹整体发硬。"],
            ["Expecting this to replace strength training.",
             "This is an entry-level feel calibration, not a program.",
             "这只是入门体感校准。" ],
            ["Ignoring the rib-flare check.",
             "Check in a side mirror to see if the ribs still flare.",
             "对镜侧身看肋骨是否外翻。" ]
        ],
        "shifts": [
            ["说收紧核心只说 suck in",
             "用 brace（收紧支撑）、rib flare（肋骨外翻）、abdominal pressure（腹压）"],
            ["说核心训练只提器械",
             "用 breath cue（呼吸意象）、transversus abdominis（腹横肌）、stabilizer（稳定肌）"]
        ],
        "footer": "转录基于图文实录口播（繁体字幕）与理性分析SVG。已校正：吸肚子核心是散的且肋骨外翻、有效核心收紧应让肋廓内收建立腹压、蜡烛吹气引导肋骨向前向内收、连续咳嗽两声唤醒腹横肌、发嘶音用持续呼气阻力维持张力、用手触摸确认腰腹整体变硬、核心收紧是三维桶状稳定而非二维肚脐位移、该方法适合入门体感校准不能替代系统力量训练等。"
    },
    "ziyouyong-gunfan-jiqiao": {
        "practice": [
            ["说第一拍收臂", "After the final pull, pin both arms tight to your sides."],
            ["说第二拍蜷体", "Hands sweep down, eyes on your toes, head reaching for your knees."],
            ["说第三拍蓄力", "Roll forward and downward, loading momentum for the push."],
            ["说第四拍蹬壁", "Straighten your back, arms squeezed, and push off straight."],
            ["说关键提醒", "Don't twist your trunk—push off streamlined and rotate while gliding."]
        ],
        "pitfalls": [
            ["Rotating the trunk at the push-off.",
             "Push off streamlined; rotate only during the glide.",
             "蹬壁时不要提前转躯干。"],
            ["Keeping arms wide during the roll.",
             "Pinned arms reduce drag and give room to rotate.",
             "收臂贴紧减少水阻。"],
            ["Forgetting the tuck cue.",
             "Head-to-knee is the tightest, fastest rolling shape.",
             "头找膝盖是翻滚半径最小的姿势。"],
            ["Trying the tight roll before you can flip safely.",
             "Practice in shallow water or with a coach first.",
             "初学者先分步练习翻滚再衔接蹬壁。" ],
            ["Reading '不要转动膝盖' literally.",
             "Whisper misheard 躯干 (trunk) as 膝盖 (knee) — it's the trunk.",
             "字幕「膝盖」是「躯干」的误识。" ]
        ],
        "shifts": [
            ["说转身只说 turn",
             "用 tumble turn（翻滚转身）、tuck（蜷体）、streamline（流线型）"],
            ["说蹬壁只说 push off",
             "用 five-beat sequence（五拍口诀）、delayed rotation（延迟转体）"]
        ],
        "footer": "转录基于图文实录口播与理性分析SVG。已校正：自由泳滚翻五拍为收臂贴紧、收下巴蜷体（手下摆眼睛看脚尖头去找膝盖）、蓄力转身、腰背打直蹬壁、流线滑行再转体、全片最关键提醒是蹬壁时不要转动躯干直接蹬出滑行时再转、Whisper将「躯干」误识为「膝盖」、内容标注来源于国外网站非原创教学、视频仅11秒无分步练习方法、初学者建议浅水区或教练陪同下分步练习等。"
    },
    "ziyouyong-datui-cuowu": {
        "practice": [
            ["说直腿打水错误", "Stiff-leg kicking swings the leg like a rod with a locked knee."],
            ["说锄头脚错误", "The hoe foot digs with the sole instead of the foot top."],
            ["说小腿打水错误", "Shin kicking over-bends the knee and drops the whipping motion."],
            ["说幅度过大的错误", "Too big a range spreads the legs wide and wastes energy."],
            ["说正确做法", "Moderate knee bend, relaxed pointed ankle, small hip-driven range."]
        ],
        "pitfalls": [
            ["Assuming one 'right' kick.",
             "The two knee mistakes are opposites—there's a sweet spot.",
             "打腿错误不是单一标准。"],
            ["Chasing big splashes.",
             "Large amplitude is listed as its own mistake.",
             "幅度过大大水花本身是错误。"],
            ["Expecting a correct demo in the video.",
             "All four clips are wrong demos; correct form must be inferred.",
             "全片都是错误示范，正确做法需反推。"],
            ["Sucking the ankle up into a hoe foot.",
             "Keep the ankle relaxed and pointed, pushing with the foot top.",
             "脚踝放松绷直用脚背推水。"],
            ["Kicking from the knee only.",
             "The kick should be hip-driven with a whipping chain.",
             "打腿应由髋部发起、大腿带动小腿。" ]
        ],
        "shifts": [
            ["说打腿只说 kick",
             "用 stiff-leg kick（直腿打水）、hoe foot（锄头脚）、whip（鞭状）"],
            ["说用力只说 work hard",
             "用 amplitude（幅度）、sweet spot（合适区间）、economy（经济性）"]
        ],
        "footer": "转录来自图文实录与理性分析SVG。本片无口播，音轨为背景音乐，内容重建自四条字幕（直腿打水/锄头脚/小腿打水/打腿幅度过大）：四个错误覆盖膝关节两极端与踝关节、动作幅度三个维度、直腿打水与小腿打水方向相反说明膝关节弯曲有合适区间、锄头脚是没有用脚背打水、打腿幅度过大两腿分离太开既费力又不经济、全片四段画面全部是错误示范没有正确动作对照、正确做法需反推：髋部发起大腿带动小腿鞭状打水、膝盖适度自然弯曲、脚踝放松下垂等。"
    },
    "aijiaolian-zhuanshen-duibi": {
        "practice": [
            ["说转身差距在哪", "The gap opens after the wall—in tuck tightness and push-off timing."],
            ["说贴壁翻滚紧凑度", "Fold tighter and roll with a smaller radius like the ✓ swimmer."],
            ["说关键帧", "At the same instant, ✓ is pushing off while ✗ is still tucked."],
            ["说蹬壁后的滑行", "Stay streamlined after the push to turn momentum into distance."],
            ["说行动要点", "Pull knees in hard, check your feet at touch, glide long."]
        ],
        "pitfalls": [
            ["Blaming swim speed for the turn gap.",
             "Their strokes are similar—the wall is where it diverges.",
             "差距在贴壁之后。"],
            ["Turning loosely at the wall.",
             "A compact, tight roll is the faster shape.",
             "翻滚要紧凑不能松。"],
            ["Pushing off late.",
             "The same instant shows ✓ pushing off while ✗ still rolls.",
             "蹬壁时机是关键帧。"],
            ["Neglecting the glide.",
             "Both glide fine—timing, not glide form, decides the gap.",
             "滑行姿势不是差距来源。" ],
            ["Copying the tight roll before mastering the flip.",
             "Practicing an aggressive tuck too early can cause choking.",
             "初学者先分步练翻滚再衔接蹬壁。" ]
        ],
        "shifts": [
            ["说转身快慢只说 swim fast",
             "用 tumble turn（翻滚转身）、tuck tightness（翻滚紧凑度）、push-off timing（蹬壁时机）"],
            ["说滑行只说 glide",
             "用 streamline（流线型）、body length（身位）、momentum（动量）"]
        ],
        "footer": "转录来自图文实录与理性分析SVG。本片无口播讲解，30秒分屏对比，内容重建自画面：两人划水阶段差异不大、真正拉开差距的关键帧在贴壁之后、✓泳者翻滚更紧凑折叠角度更小、00:06.75是关键帧此时✓已蹬壁伸展而✗仍在收拢翻滚、蹬壁后两人流线型滑行姿势接近说明差距来自蹬壁时机而非滑行姿势、✓因更早蹬壁持续领先约一个身位、行动为贴壁前用力收膝抱团、检查触壁瞬间双脚是否已开始蹬伸、蹬壁后保持双臂前伸身体绷直、视频未说明✗错误成因也没有纠正训练动作等。"
    },
    "youyong-zhuanshen-duibi-2": {
        "practice": [
            ["说转身差距的根源", "The gap is transition speed, not push-off strength."],
            ["说开放式转身的定义", "An open turn touches the wall with hands, head above water, no flip."],
            ["说进出流线的关键", "The elite swimmer streamlines faster into and out of the turn."],
            ["说初学者的慢点", "Beginners lag on the late touch and slow tuck-to-streamline switch."],
            ["说行动要点", "Judge distance early, drill the push-off link, and review your turn on film."]
        ],
        "pitfalls": [
            ["Blaming the push-off power.",
             "Both swimmers push off similarly—transitions decide the race.",
             "差距来自衔接不是蹬壁力量。"],
            ["Treating both turns as flip turns.",
             "These are open, head-above-water turns, not tumble turns.",
             "这是触壁转身不是翻滚转身。"],
            ["Staying tucked after the push.",
             "Reach out into the streamline immediately.",
             "蹬壁后要立刻伸展手臂。"],
            ["Dawdling on the approach.",
             "Judge the distance early to touch on time.",
             "提前判断距离减少触壁拖延。"],
            ["Generalizing from one comparison.",
             "The sample is one pair; 'pro/beginner' labels are the author's.",
             "样本量为1，标签是作者给定。" ]
        ],
        "shifts": [
            ["说转身慢只说 weak legs",
             "用 open turn（开放式转身）、transition speed（衔接速度）、tuck-to-streamline（蜷体到流线）"],
            ["说差距只说 gap",
             "用 late touch（触壁晚）、muscle memory（肌肉记忆）、frame by frame（逐帧）"]
        ],
        "footer": "转录来自图文实录与理性分析SVG。本片无口播，内容重建自笔记文案与画面：两种开放式转身对比、差距根源是触壁蜷体蹬壁流线展开四步之间的衔接时间差而非蹬壁力量、作者文案指顶级选手进出转弯都更快进入流线从而保持速度、开放式转身是单手或双手触壁头部始终露出水面不做翻滚、初学者的两个慢点是触壁时机拖延与蜷体到流线切换慢、蹬壁后立刻展开流线是本片差距最明显的环节、行动为提前判断距离减少犹豫、用陆地或扶壁蹬腿强化蹬壁后伸展的肌肉记忆、录视频逐帧回放找慢点、样本量为1次对比且高手初学者标签为视频给定等。"
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
