#!/usr/bin/env python3
"""批27：为10篇小红书视频生成完整场景英译JSON（游泳技巧/跑步技术）。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

ARTICLES = {}

ARTICLES["ziyouyong-gaozhou-baoshui"] = {
    "title_zh": "自由泳高肘抱水，看完让你更走水",
    "title_en": "Freestyle High-Elbow Catch That Moves You Forward",
    "duration": "16秒",
    "topic": "运动 · 游泳",
    "scenes": [
        {"id": "s1", "scene_zh": "抱水不要抱90度", "scene_en": "Don't Catch at 90 Degrees", "time": "00:00",
         "context": "自由泳抱水不要抱90度，否则肩关节会疼。正确动作是送肩前伸，往斜下方抱水。",
         "sentences": [
            ["抱水不要抱90度，会导致肩关节会疼。", "Don't catch the water at 90 degrees—it hurts your shoulder.", "catch（抱水）"],
            ["正确动作是送肩前伸，往斜下方抱水。", "The correct move is to lead with the shoulder and reach forward.", "lead with the shoulder（送肩）"],
            ["往斜下方抱，肩关节才不会痛。", "Catch diagonally downward to spare your shoulder.", "diagonally（斜向地）"]
         ]},
        {"id": "s2", "scene_zh": "抱水时不要过中线", "scene_en": "Don't Cross the Centerline", "time": "00:07",
         "context": "抱水时手不要过身体中线，推水时转肩、送肩前伸。手保持在肩宽范围内，才能保持身体平衡与划水效率。",
         "sentences": [
            ["抱水时不要过中线。", "Don't let your hand cross the centerline.", "centerline（中线）"],
            ["推水时转肩、送肩前伸。", "Rotate the shoulder as you push and lead it forward.", "rotate（转动）"],
            ["两边肩转换交替起来，这才是正确的自由泳抱水。", "Alternate the shoulders side to side—that's the right freestyle catch.", "alternate（交替）"]
         ]}
    ]
}

ARTICLES["ziyouyong-kaiwu-5moments"] = {
    "title_zh": "自由泳突然开悟的五个瞬间",
    "title_en": "Five 'Aha' Moments in Freestyle",
    "duration": "1分05秒",
    "topic": "运动 · 游泳",
    "scenes": [
        {"id": "s1", "scene_zh": "一：重心前移，身体平直", "scene_en": "1. Weight Forward, Body Flat", "time": "00:00",
         "context": "当发现手入水后往前下方伸一点时，身体会自然上浮，形成平直的流线型，滑手打腿都很轻松。这是自由泳开悟的第一个瞬间。",
         "sentences": [
            ["手入水后往前下方伸一点，身体会自然上浮。", "Reach slightly forward and down after entry, and the body naturally floats up.", "body floats up（身体上浮）"],
            ["平直的流线型，滑手打腿都很轻松。", "A flat streamline makes the stroke and kick feel easy.", "streamline（流线型）"]
         ]},
        {"id": "s2", "scene_zh": "二：转体带动滑手", "scene_en": "2. Body Roll Drives the Pull", "time": "00:14",
         "context": "再怎么用力滑手，也不如把身体转起来。手抓住水后被身体转动带着走，滑得轻松游得快。",
         "sentences": [
            ["再用力滑手，也不如把身体转起来。", "No matter how hard you pull, rolling the body does more.", "roll（转体）"],
            ["手抓住水后，被身体转动带着走。", "Once the hand catches, the body rotation carries it.", "carry（带着走）"],
            ["滑得轻松，游得快。", "Easier pull, faster swimming.", "easier（更轻松的）"]
         ]},
        {"id": "s3", "scene_zh": "三：高肘抱水", "scene_en": "3. The High-Elbow Catch", "time": "00:27",
         "context": "手入水后不是立刻发力往下压，而是大臂内侧固定住、屈轴小臂下滑抱住水，第一次感觉到推水推着往前走。",
         "sentences": [
            ["手入水后不是立刻发力往下压。", "After entry, don't press down immediately.", "press down（下压）"],
            ["大臂内侧固定住，屈轴小臂下滑抱住水。", "Anchor the upper arm and let the bent forearm sink to catch.", "anchor（固定）"],
            ["第一次感觉到推水推着你往前走。", "For the first time you feel the water pushing you forward.", "push forward（向前推进）"]
         ]},
        {"id": "s4", "scene_zh": "四：换气轻松", "scene_en": "4. Effortless Breathing", "time": "00:40",
         "context": "学会了转头不抬头，头随着身体的转动很自然地转出水面换气，节奏稳定、吸气足。",
         "sentences": [
            ["你学会了转头不抬头。", "You learn to turn your head, not lift it.", "turn the head（转头）"],
            ["头随着身体的转动，自然转出水面换气。", "The head follows the body roll and surfaces to breathe naturally.", "surface（露出水面）"],
            ["节奏稳定，吸气足。", "Steady rhythm, full breath.", "rhythm（节奏）"]
         ]},
        {"id": "s5", "scene_zh": "五：不用拼命打腿", "scene_en": "5. No More Desperate Kicking", "time": "00:51",
         "context": "当你发现打腿是为了维持身体平衡和流线型的时候，随着身体滚动有节奏地打腿，反而游得更轻松更平稳。",
         "sentences": [
            ["打腿是为了维持身体平衡和流线型。", "Kicking exists to keep balance and the streamline.", "balance（平衡）"],
            ["随着身体的滚动，有节奏地打腿。", "Kick in rhythm with the body roll.", "in rhythm（有节奏地）"],
            ["反而游得更轻松、更平稳。", "It actually makes you smoother and more relaxed.", "smoother（更平稳的）"]
         ]}
    ]
}

ARTICLES["dieyong-baoshui"] = {
    "title_zh": "蝶泳抱水",
    "title_en": "Butterfly Catch: Angles and Symmetry",
    "duration": "22秒",
    "topic": "运动 · 游泳",
    "scenes": [
        {"id": "s1", "scene_zh": "多视角看蝶泳抱水", "scene_en": "Catch It From Multiple Angles", "time": "00:00",
         "context": "本片没有口播，靠多个视角的蝶泳抱水角度讲解：侧视给肘角与入水角，前视给对称与肩肘空间，绿勾段再把片段连成过程。缺任一视角，都容易把局部角度记成全部答案。",
         "sentences": [
            ["本片无口播，用多个视角讲蝶泳抱水。", "No narration—the butterfly catch is shown from several angles.", "multiple angles（多视角）"],
            ["侧视看肘角与入水角，前视看对称与肩肘空间。", "Side view shows elbow and entry angles; front view shows symmetry and space.", "side view（侧视）"],
            ["缺任一视角，容易把局部角度当成全部答案。", "Missing one angle, you mistake a local detail for the whole answer.", "local（局部的）"]
         ]},
        {"id": "s2", "scene_zh": "45°入水前伸", "scene_en": "Entry and Reach at ~45°", "time": "00:03",
         "context": "开场侧视在手部旁叠斜线与「45°」，把难以口头描述的入水相对角度变成可视标尺。",
         "sentences": [
            ["画面标注手部入水前伸角度约45°。", "The graphic marks the entry-reach angle at about 45°.", "entry angle（入水角）"],
            ["把难以描述的角度变成可视标尺。", "It turns an unspoken angle into a visible ruler.", "ruler（标尺）"]
         ]},
        {"id": "s3", "scene_zh": "90°高肘抱水", "scene_en": "High-Elbow Catch at 90°", "time": "00:06",
         "context": "抱水瞬间肘关节被白线标出「90°」，把「高肘」从感觉词落成关节角度。",
         "sentences": [
            ["抱水瞬间，肘关节被标成90°。", "At the catch, the elbow is marked at 90 degrees.", "elbow angle（肘角）"],
            ["把「高肘」从感觉词落成关节角度。", "It turns 'high elbow' from a feeling into an angle.", "high elbow（高肘）"]
         ]},
        {"id": "s4", "scene_zh": "前视检查对称", "scene_en": "Front View: Check Symmetry", "time": "00:10",
         "context": "前视用左右竖线、肩肘圆点与下垂参考线，检查双手是否同步、手臂相对竖直方向如何张开。",
         "sentences": [
            ["前视检查双手是否同步。", "The front view checks whether both hands stay in sync.", "in sync（同步）"],
            ["用参考线看手臂相对竖直方向如何张开。", "Reference lines show how the arms open from vertical.", "reference line（参考线）"]
         ]},
        {"id": "s5", "scene_zh": "绿勾串起完整手部路径", "scene_en": "The Green Check Links the Full Path", "time": "00:14",
         "context": "约00:14起出现绿勾与「蝶泳手部动作」，随后侧视连续展示由前伸转入外展划水，把静帧角度连回完整路径。",
         "sentences": [
            ["绿勾标注「蝶泳手部动作」，把静帧连成过程。", "The green check names the butterfly hand motion, linking the stills.", "still frame（静帧）"],
            ["由前伸转入外展划水，连续展示。", "It flows from the reach into the outward sweep.", "outward sweep（外展划水）"]
         ]},
        {"id": "s6", "scene_zh": "方法与边界", "scene_en": "Method and Limits", "time": "00:18",
         "context": "关键认知：从「凭感觉划手」转向「用水下角度与多机位关系理解抱水」。数字是观察锚点，完整手部路径才是目标；口播听不清时以叠字为准，有争议请教练复核。",
         "sentences": [
            ["从凭感觉划手，转向用水下角度理解抱水。", "Shift from feeling the pull to reading it through underwater angles.", "underwater（水下）"],
            ["数字是观察锚点，完整手部路径才是目标。", "The numbers are anchors; the full hand path is the goal.", "anchor（锚点）"],
            ["口播听不清时，以画面标注为准。", "When narration is unclear, trust the on-screen marks.", "on-screen marks（画面标注）"]
         ]}
    ]
}

ARTICLES["rushui-diezhou-chain"] = {
    "title_zh": "入水跌肘【导致】前伸沉肘【导致】抱水溜肘",
    "title_en": "Dropped Elbow at Entry → Sunk Reach → Slipped Catch",
    "duration": "3分05秒",
    "topic": "运动 · 游泳",
    "scenes": [
        {"id": "s1", "scene_zh": "跌肘的连锁反应", "scene_en": "The Dropped-Elbow Chain", "time": "00:00",
         "context": "自由泳的跌肘，十个成人八个肘先入水。入水时能听到啪啪的拍水声；减阻是不可能的，还会导致接下来前伸沉肘，基本上就和高肘抱水说再见了。",
         "sentences": [
            ["自由泳的跌肘，十个成人八个肘先入水。", "In freestyle, eight of ten adults drop the elbow at entry.", "dropped elbow（跌肘）"],
            ["自己都能听到每一次入水的啪啪声。", "You can hear the slap with every entry.", "slap（拍水声）"],
            ["减阻是不可能减阻的，还会导致前伸沉肘。", "No drag reduction—it just leads to a sinking reach.", "sinking reach（前伸沉肘）"]
         ]},
        {"id": "s2", "scene_zh": "跌肘的根源是掉肩", "scene_en": "The Root Cause: Dropping the Shoulder", "time": "00:28",
         "context": "很多人入水时肘先掉下去，根源都是肩先掉了下去。正确的动作是在移臂入水时，肩膀都是在水面上的；手入水后，随着前伸的动作，肩膀才会随着转下去。",
         "sentences": [
            ["跌肘的罪恶之源是掉肩。", "The root of the dropped elbow is the dropped shoulder.", "root cause（根源）"],
            ["正确动作是移臂入水时，肩膀在水面上。", "Correctly, the shoulder stays above water at entry.", "above water（水面上）"],
            ["手入水后，随着前伸肩膀才转下去。", "Only as the hand enters and reaches does the shoulder follow.", "follow（跟随）"]
         ]},
        {"id": "s3", "scene_zh": "正确的入水顺序", "scene_en": "The Right Entry Order", "time": "00:49",
         "context": "正确的入水顺序是手、肘、肩。但跌肘的朋友手还没入水，肩膀就已经先入水掉到水里了；肩都入水了，连接肩的大臂就会入水，大臂入水了，自然肘也就先入水了。",
         "sentences": [
            ["正确的顺序是：手、肘、肩。", "The correct order is: hand, elbow, shoulder.", "sequence（顺序）"],
            ["跌肘的朋友手还没入水，肩膀已经先入水了。", "Elbow-droppers send the shoulder in before the hand.", "send in（先入水）"],
            ["肩入水带动大臂入水，肘自然也就先入水了。", "Shoulder down drags the upper arm, and the elbow follows first.", "drag（拖带）"]
         ]},
        {"id": "s4", "scene_zh": "肩撑住等于肘撑住", "scene_en": "Hold the Shoulder, Hold the Elbow", "time": "01:27",
         "context": "在一臂入水的过程中，肩一定要撑住。手不粘水，肩膀都应该是在水面上撑着的，不能提早往下掉；随着前伸手入水、肘入水、最后才是肩膀入水。肩撑住了就等于肘撑住了。",
         "sentences": [
            ["移臂入水时，肩一定要撑住。", "Through the entry, the shoulder must stay supported.", "supported（撑住）"],
            ["手不粘水，肩膀都应该在水面上撑着。", "Before the hand touches water, the shoulder rides high.", "ride high（撑在水面）"],
            ["肩撑住了，就等于肘撑住了。", "Hold the shoulder, and you hold the elbow.", "hold（撑住）"]
         ]},
        {"id": "s5", "scene_zh": "第二个因素：手入水姿态", "scene_en": "Factor Two: Hand Entry Angle", "time": "01:33",
         "context": "除了肩的问题，还有一个因素导致很多新手跌肘：手入水的姿态。肩膀柔韧性一般的成年人用平插入水，就很容易跌肘；建议采用斜插入水，手掌手腕稍微向外侧转一点，肘就撑起来了。",
         "sentences": [
            ["手入水时是斜插还是平插？", "Do you enter flat or at an angle?", "enter（入水）"],
            ["柔韧性一般的成年人平插入水，很容易跌肘。", "Less flexible adults often drop the elbow with a flat entry.", "flexible（柔韧性好的）"],
            ["斜插入水，手掌手腕稍微向外侧转一点，肘就撑起来了。", "Enter angled with the wrist rotated out and the elbow lifts.", "rotate outward（向外转）"]
         ]},
        {"id": "s6", "scene_zh": "总结两个细节", "scene_en": "Summary: Two Details", "time": "02:21",
         "context": "想要不跌肘：第一，入水时肩不要往下掉、要撑住，肩撑住就等于肘撑住，肩掉就等于肘掉；第二，建议新手采用斜插方式入水，手稍微向外侧倾斜一点，更容易把肘架住，平插更容易肘部掉下来。",
         "sentences": [
            ["入水时肩要撑住，肩掉就等于肘掉。", "Support the shoulder at entry—shoulder down means elbow down.", "shoulder down（肩下沉）"],
            ["新手建议用斜插的方式入水。", "New swimmers should enter at an angle.", "angled entry（斜插入水）"],
            ["手向外侧倾斜一点，更容易把肘架住。", "A slight outward tilt helps prop the elbow up.", "prop up（架住）"]
         ]}
    ]
}

ARTICLES["ziyouyong-huashou-baoshui"] = {
    "title_zh": "自由泳划手抱水纠正",
    "title_en": "Fixing Your Freestyle Pull and Catch",
    "duration": "17秒",
    "topic": "运动 · 游泳",
    "scenes": [
        {"id": "s1", "scene_zh": "误解：弯肘不等于抱水正确", "scene_en": "Bent Elbow ≠ Correct Catch", "time": "00:00",
         "context": "视频在弯肘姿态上仍打红叉并写「大臂无内旋」——弯肘只是外形，内旋才是驱动抱水的关键转动。",
         "sentences": [
            ["弯肘只是外形，不一定等于抱水正确。", "A bent elbow is just the look—it doesn't mean the catch is right.", "bent elbow（弯肘）"],
            ["红叉标注的是「大臂无内旋」。", "The red X marks 'no internal rotation of the upper arm'.", "internal rotation（内旋）"],
            ["内旋才是驱动抱水的关键转动。", "Internal rotation is what actually drives the catch.", "drive（驱动）"]
         ]},
        {"id": "s2", "scene_zh": "正确链条：内旋+外展+前伸", "scene_en": "The Correct Chain: Rotate, Spread, Reach", "time": "00:04",
         "context": "正确的驱动链条分三步：大臂转向内旋 → 肩胛骨向外展 → 肩膀前伸叠加大臂内旋，形成高肘抱水。",
         "sentences": [
            ["大臂转向内旋。", "Rotate the upper arm inward.", "rotate inward（内旋）"],
            ["肩胛骨向外展。", "Spread the shoulder blade outward.", "shoulder blade（肩胛骨）"],
            ["肩膀前伸叠加大臂内旋，形成高肘抱水。", "Reach forward on top of the rotation to form a high-elbow catch.", "high-elbow catch（高肘抱水）"]
         ]},
        {"id": "s3", "scene_zh": "体感口诀：想象抱住一颗球", "scene_en": "The Cue: Hug a Ball", "time": "00:10",
         "context": "用足球图示把正确空间压成一句可执行口令：想象抱住一颗球。肘腕与胸口之间留出球的空隙。",
         "sentences": [
            ["想象抱住一颗球。", "Imagine hugging a ball.", "hug（抱住）"],
            ["肘腕与胸口之间留出球的空隙。", "Leave a ball's space between your elbow, wrist and chest.", "space（空隙）"],
            ["每次划手前默念「抱球」自检。", "Whisper 'hug the ball' before every pull to self-check.", "self-check（自检）"]
         ]},
        {"id": "s4", "scene_zh": "方法与边界", "scene_en": "Method and Limits", "time": "00:14",
         "context": "关键认知：从「看起来弯肘了就算抱水」转向「以内旋驱动触水面，用抱球感锁定空间」。本片是17秒跪姿示意，不含水中阻力、呼吸侧转与全身配合；肩伤或医嘱限制者不应照搬幅度。",
         "sentences": [
            ["从「看起来弯肘」转向「以内旋驱动触水面」。", "Shift from 'looks bent' to 'drive the surface with rotation'.", "drive the surface（驱动触水面）"],
            ["17秒跪姿示意，不含水中阻力与全身配合。", "A 17-second kneeling demo—no water resistance or full-body timing.", "kneeling（跪姿）"],
            ["肩伤或医嘱限制者，不应照搬动作幅度。", "Those with shoulder injuries shouldn't copy the full range.", "shoulder injury（肩伤）"]
         ]}
    ]
}

ARTICLES["hexin-buwen-cuowu-zhuan"] = {
    "title_zh": "你的【核心不稳】是因为错误的转",
    "title_en": "Your 'Unstable Core' Is a Wrong Rotation",
    "duration": "2分38秒",
    "topic": "运动 · 游泳",
    "scenes": [
        {"id": "s1", "scene_zh": "游泳时核心像荡秋千", "scene_en": "Core Swinging Like a Hammock", "time": "00:00",
         "context": "很多人游自由泳的时候，核心的部分就像在水里荡秋千，左摇右摆扭来扭去，专业术语叫核心不稳。问题出在哪里？核心力量差吗？不，问题出在转体游而非转肩游。",
         "sentences": [
            ["很多人游自由泳时，核心像在水里荡秋千。", "Many swimmers' cores swing like a hammock in the water.", "hammock（荡秋千）"],
            ["专业术语叫核心不稳。", "The technical term is core instability.", "instability（不稳）"],
            ["问题不是核心力量差，而是转体游而非转肩游。", "It's not weak core strength—it's rolling the body instead of the shoulders.", "body roll（转体）"]
         ]},
        {"id": "s2", "scene_zh": "每次滑手都翻面", "scene_en": "Flipping the Body Every Stroke", "time": "00:24",
         "context": "如果游的时候脑子里想的是滑手转左边、滑手转右边，随着每一次的滑手动作，身体就像左右翻面。因为你主观想转动身体时，发力点在核心，核心又发力又做动作，还想维持稳定几乎不可能。",
         "sentences": [
            ["脑子里想滑手转左、滑手转右，身体就跟着翻面。", "Thinking 'pull left, pull right' makes your body flip side to side.", "flip（翻面）"],
            ["想转动身体时，发力点就在核心。", "When you drive the turn from the core, the core is the engine.", "engine（发力点）"],
            ["用核心发力又用核心做动作，还要维持稳定，几乎不可能。", "Powering and moving with the core while keeping it stable is nearly impossible.", "keep stable（维持稳定）"]
         ]},
        {"id": "s3", "scene_zh": "正确的转动：转肩带着身体转", "scene_en": "The Right Roll: Shoulders Lead", "time": "01:21",
         "context": "自由泳正确的转动并不是去翻身体转体，而是转肩带着身体转：随着每一次的前伸推水，让肩膀转动滚动起来，身体跟随着肩膀的转动去转动，主力军是肩膀的联动。",
         "sentences": [
            ["正确的转动是转肩带着身体转。", "The right roll starts from the shoulder and carries the body.", "carry the body（带动身体）"],
            ["随着每一次前伸推水，让肩膀滚动起来。", "Each reach-and-push sets the shoulder rolling.", "reach-and-push（前伸推水）"],
            ["主力军是肩膀的联动。", "The lead actor is the linked shoulders.", "linked（联动的）"]
         ]},
        {"id": "s4", "scene_zh": "水中练习：肩带宽而非宽带肩", "scene_en": "Drill: Shoulder Leads, Hip Follows", "time": "01:42",
         "context": "在水中先趴平，手臂一前一后，前伸手开始向前伸，胳膊带着肩膀转动，肩膀带着身体侧倾。多做几次就能感受到自由泳究竟是如何转动的：是肩带宽，而不是髋先转带着肩去拧。",
         "sentences": [
            ["水中趴平，手臂一前一后。", "Lie flat in the water with arms front and back.", "lie flat（趴平）"],
            ["胳膊带着肩膀转，肩膀带着身体侧倾。", "The arm turns the shoulder, and the shoulder tilts the body.", "tilt（侧倾）"],
            ["是肩带宽，而不是髋先转带着肩去拧。", "The shoulder band leads—not the hip twisting the shoulder.", "shoulder band（肩带）"]
         ]},
        {"id": "s5", "scene_zh": "核心拉长收紧，不塌不扭", "scene_en": "Core Lengthened, Not Twisted", "time": "02:04",
         "context": "此时你的核心是拉长收紧的，不塌不扭，连贯起来自然核心也就不会出现荡秋千的情况了。重点总结：转肩游而非转体游，肩带宽而不是宽带肩。",
         "sentences": [
            ["此时核心拉长收紧，不塌不扭。", "Your core is now lengthened and braced—no sag, no twist.", "brace（收紧）"],
            ["连贯起来，核心就不会荡秋千了。", "Chained together, the core stops swinging.", "chain（连贯）"],
            ["转肩游而非转体游，肩带宽而不是宽带肩。", "Roll the shoulders, not the body—shoulders lead, hips follow.", "hips follow（髋跟随）"]
         ]}
    ]
}

ARTICLES["zilv-1348-days"] = {
    "title_zh": "自律第1348天",
    "title_en": "Self-Discipline, Day 1,348",
    "duration": "8分13秒",
    "topic": "运动 · 跑步",
    "scenes": [
        {"id": "s1", "scene_zh": "街头搭话：指出跑姿问题", "scene_en": "Street Encounter: The Form Check", "time": "00:00",
         "context": "跑者在公园遇到一位小哥哥，直话直说指出问题：脚后跟落地偏多、上身没收紧、仰着头，这样跑很累还可能受伤。真诚交流后对方同意接受指导。",
         "sentences": [
            ["前面小哥哥跑姿不对，咱们交流一下。", "That runner's form is off—let's have a chat.", "form（跑姿）"],
            ["你脚后跟落地偏多，上身没有收紧，还仰着头。", "You heel-strike too much, your torso is loose, and you look up.", "heel-strike（脚后跟落地）"],
            ["这样跑很累，我可以教你一种轻松还不受伤的跑法。", "That's tiring—let me teach you an easy, injury-free way.", "injury-free（不受伤的）"]
         ]},
        {"id": "s2", "scene_zh": "最大问题：脚后跟落地", "scene_en": "The Biggest Issue: Heel-Striking", "time": "01:01",
         "context": "你的最大问题是脚后跟落地，再加上步频又低，跑久了膝盖百分之百会受伤。脚后跟落地是因为上身没有收紧，包括小腹腹部。",
         "sentences": [
            ["你的最大问题是脚后跟落地。", "Your biggest problem is landing on your heels.", "biggest problem（最大问题）"],
            ["再加上步频低，跑久膝盖一定会受伤。", "Add a low cadence and your knees will suffer over time.", "cadence（步频）"],
            ["脚后跟落地是因为上身没有收紧。", "Heel-striking comes from a loose upper body.", "loose upper body（上身未收紧）"]
         ]},
        {"id": "s3", "scene_zh": "收紧腹部，降低步幅", "scene_en": "Brace the Belly, Shrink the Stride", "time": "01:26",
         "context": "让跑者按一下腹部确认收紧，然后把步幅再降低一点，你会感觉跑得更轻松一点。现在的步频才160，要提到180以上才不会受伤。",
         "sentences": [
            ["腹部收紧，步幅再降低一点。", "Brace the belly and take smaller steps.", "brace（收紧）"],
            ["步频才160，要提到180以上。", "Your cadence is 160—get it above 180.", "cadence（步频）"],
            ["180以上才不会受伤，感觉更轻松。", "Above 180 spares the joints and feels easier.", "spare the joints（保护关节）"]
         ]},
        {"id": "s4", "scene_zh": "练小碎步找全脚掌落地", "scene_en": "Shuffle Steps to Find the Full-Foot Landing", "time": "02:00",
         "context": "步子小一点，小碎步，不要点脚尖，不要用前脚掌落地，用整个脚落地。练习时张开手臂找平衡，像机器人一样直上直下走。",
         "sentences": [
            ["步子小一点，小碎步。", "Take smaller steps—a light shuffle.", "shuffle（小碎步）"],
            ["不要点脚尖，用整个脚落地。", "Don't tiptoe—land with the whole foot.", "whole foot（全脚掌）"],
            ["张开手臂找平衡，直上直下像机器人。", "Open your arms for balance and step up-down like a robot.", "like a robot（像机器人）"]
         ]},
        {"id": "s5", "scene_zh": "摆臂：前后送不是往下敲", "scene_en": "Arms Swing Front-Back, Not Punching Down", "time": "04:09",
         "context": "摆臂不是往下敲，而是手肘固定、前后送，弯曲小于90度。翘手、往下敲都是错的，摆臂前后送才省力。",
         "sentences": [
            ["摆臂不是往下敲，而是固定手肘前后送。", "Don't punch downward—fix the elbow and swing front and back.", "punch（敲）"],
            ["手臂弯曲小于90度。", "Bend the arm under 90 degrees.", "under 90 degrees（小于90度）"],
            ["前后送才省力。", "Front-back swinging saves energy.", "save energy（省力）"]
         ]},
        {"id": "s6", "scene_zh": "头部与核心要点", "scene_en": "Head and Core Cues", "time": "05:08",
         "context": "提醒吸气挺胸、头看斜下方不要扬头、脖子收起来、步子小着、上身稳住。慢跑时头微微往下看，一疲劳头就容易上扬。",
         "sentences": [
            ["吸气挺胸，头看斜下方不要扬头。", "Breathe in, chest up, eyes down—don't lift your chin.", "eyes down（向下看）"],
            ["脖子收起来，步子小着，上身稳住。", "Tuck the neck, keep steps short, hold the torso steady.", "hold steady（稳住）"],
            ["一疲劳，头就往上扬了。", "Get tired and the head creeps up.", "creep up（悄悄上扬）"]
         ]},
        {"id": "s7", "scene_zh": "收尾：步频提升的成果", "scene_en": "The Payoff: Cadence Is Up", "time": "07:55",
         "context": "练了一会儿，步频从160提到166、接近180，保持住越来越好。教练肯定成果后离开，留下一句鼓励。",
         "sentences": [
            ["练了一会儿，步频上来了。", "After some drills, your cadence is climbing.", "climb（上升）"],
            ["保持住，越来越好。", "Hold it—you're getting better and better.", "better and better（越来越好）"],
            ["那我就走了，不打扰了，拜拜。", "I'll leave you to it—bye!", "leave you to it（不打扰）"]
         ]}
    ]
}

ARTICLES["dabu-liuxing-songkuan"] = {
    "title_zh": "这大步流星的感觉谁懂呀",
    "title_en": "That Long-Stride Feeling Nobody Gets",
    "duration": "41秒",
    "topic": "运动 · 跑步",
    "scenes": [
        {"id": "s1", "scene_zh": "大步流星的真相：送髋", "scene_en": "The Truth: Hip Drive, Not Stride Length", "time": "00:00",
         "context": "大步流星的感觉不是步子迈多大，而是髋能不能把身体送出去。标题体感来自后蹬把人送出，而不是伸腿够远；口播听不清，内容重建自画面大字与笔记。",
         "sentences": [
            ["大步流星的真相不是步子迈多大，而是送髋。", "The real secret isn't stride length—it's hip drive.", "hip drive（送髋）"],
            ["体感来自后蹬把人送出，而不是伸腿够远。", "The feeling comes from the push-off sending you, not reaching far.", "push-off（后蹬）"],
            ["口播听不清，内容以画面大字与笔记为准。", "Narration is unclear—trust the captions and notes.", "captions（字幕）"]
         ]},
        {"id": "s2", "scene_zh": "能力前提：髋活+臀驱动力+核心稳定", "scene_en": "The Prerequisites: Mobility, Drive, Stability", "time": "00:05",
         "context": "笔记明确写：没有髋活动度、臀驱动力、核心稳定，「很难做得出来」。动作是入口，不是充分条件；送髋是综合能力，不是单个花样动作。",
         "sentences": [
            ["没有髋活动度、臀驱动力和核心稳定，很难做得出来。", "Without hip mobility, glute drive and core stability, it's very hard.", "mobility（活动度）"],
            ["动作是入口，不是充分条件。", "The drills are an entry, not a guarantee.", "entry（入口）"],
            ["送髋是综合能力，不是单个花样动作。", "Hip drive is a compound ability, not one flashy move.", "compound ability（综合能力）"]
         ]},
        {"id": "s3", "scene_zh": "五项动作之一二：摆腿", "scene_en": "Drills 1-2: Swing Legs", "time": "00:10",
         "context": "正摆腿：扶栏站立，大幅度正向摆腿，左右脚各20次，优先打开髋关节矢状面活动度。俯卧交叉摆腿：在俯撑支撑下做交叉摆腿，把髋活动放进核心必须在线的情境，先锁肋骨骨盆中立再摆腿。",
         "sentences": [
            ["正摆腿：扶栏站立，大幅度正向摆腿，每侧20次。", "Forward leg swings: hold the rail, swing big, 20 per side.", "leg swing（摆腿）"],
            ["打开髋关节矢状面的活动度。", "It opens hip mobility in the sagittal plane.", "sagittal plane（矢状面）"],
            ["俯卧交叉摆腿：核心必须在线。", "Prone cross-swings demand an engaged core.", "prone（俯卧）"]
         ]},
        {"id": "s4", "scene_zh": "动作三：交叉踢腿", "scene_en": "Drill 3: Cross Kicks", "time": "00:15",
         "context": "站立位交叉踢摆，左右脚各20次，在站立平衡条件下继续刺激髋的交叉/旋转相关控制，衔接后面的跑步动作。支撑腿微屈、落地轻。",
         "sentences": [
            ["站立位交叉踢腿，每侧20次。", "Cross kicks from standing, 20 per side.", "cross kick（交叉踢腿）"],
            ["在平衡条件下刺激髋的交叉控制。", "It trains cross-control of the hip while balancing.", "cross-control（交叉控制）"],
            ["支撑腿微屈，落地轻。", "Keep the stance leg soft and land lightly.", "soft（微屈的）"]
         ]},
        {"id": "s5", "scene_zh": "动作四：快速后蹬跑", "scene_en": "Drill 4: Quick Push-Off Runs", "time": "00:20",
         "context": "短距离强调后蹬的跑步练习，约20米。这是大步流星体感的关键转化点：把前面的髋活变成后腿把身体送出去的推进。关注后腿蹬直与髋前送，而不是刻意伸小腿够远。",
         "sentences": [
            ["快速后蹬跑：约20米，强调后蹬。", "Quick push-off runs: about 20 meters, all about the drive.", "push-off run（后蹬跑）"],
            ["这是把髋活变成推进的关键转化点。", "It converts hip mobility into propulsion.", "propulsion（推进）"],
            ["关注后腿蹬直与髋前送，不刻意伸小腿。", "Drive the leg straight and hip forward—don't reach with the shin.", "reach with the shin（伸小腿）"]
         ]},
        {"id": "s6", "scene_zh": "动作五：弓箭步行走", "scene_en": "Drill 5: Walking Lunges", "time": "00:30",
         "context": "慢速、大步幅的弓箭步向前走，用可控速度巩固髋前送与步幅，让「大步」有支撑结构和平衡，而不仅是冲刺瞬间的感觉。",
         "sentences": [
            ["弓箭步行走：慢速、大步幅向前。", "Walking lunges: slow, long strides forward.", "walking lunge（弓箭步走）"],
            ["用可控速度巩固髋前送与步幅。", "Consolidate hip drive and stride at a controlled pace.", "consolidate（巩固）"],
            ["让大步有支撑结构，而不是冲刺瞬间的感觉。", "Give the long stride structure, not just a sprint feeling.", "structure（结构）"]
         ]},
        {"id": "s7", "scene_zh": "方法与边界", "scene_en": "Method and Limits", "time": "00:38",
         "context": "训练日志不要只记「做了正摆腿」，要记髋活动幅度、后蹬是否更干脆、核心是否塌。五项动作服务同一目标的不同侧面；适合作为跟练入口，实际效果取决于能力前提是否补齐。",
         "sentences": [
            ["训练日志记髋活动幅度、后蹬是否干脆。", "Log hip range, push-off crispness, and core integrity.", "log（记录）"],
            ["五项动作服务同一目标的不同侧面。", "Five drills serve different sides of one goal.", "sides（侧面）"],
            ["效果取决于能力前提是否补齐。", "Results hinge on closing the prerequisite gaps.", "prerequisite（前提）"]
         ]}
    ]
}

ARTICLES["paobu-zhengque-luodi"] = {
    "title_zh": "新手跑者必须要知道跑步如何正确落地",
    "title_en": "How Beginners Should Land While Running",
    "duration": "48秒",
    "topic": "运动 · 跑步",
    "scenes": [
        {"id": "s1", "scene_zh": "脚后跟先落地是刹车", "scene_en": "Heel-First Is Braking", "time": "00:00",
         "context": "脚后跟先入地干嘛？刹车！每跑一步再刹车一次。先用脚后跟跳一跳感受：脚后跟没有减震功能、没有弹性。",
         "sentences": [
            ["脚后跟先入地是刹车，每跑一步再刹车一次。", "Heel-first landing is braking—every step a brake.", "braking（刹车）"],
            ["用脚后跟跳一跳，没有减震功能。", "Hop on your heels—no shock absorption.", "shock absorption（减震）"],
            ["脚后跟没有弹性。", "Your heels have no spring.", "spring（弹性）"]
         ]},
        {"id": "s2", "scene_zh": "用前脚掌跳一跳", "scene_en": "Now Hop on Your Forefeet", "time": "00:14",
         "context": "教练到底哪里先着地？答案是全脚掌着地——整个脚掌着地，也就是鞋底和地面平行，小腿垂直地面，才有可能做到全脚掌落地。",
         "sentences": [
            ["到底是脚后跟、前脚掌还是哪里先着地？", "Heel, forefoot, or what?", "forefoot（前脚掌）"],
            ["我们是全脚掌着地，鞋底和地面平行。", "We land with the whole foot—sole parallel to the ground.", "whole foot（全脚掌）"],
            ["小腿垂直地面，才有可能全脚掌落地。", "With the shin vertical, a full-foot landing becomes possible.", "vertical（垂直的）"]
         ]},
        {"id": "s3", "scene_zh": "落地瞬间的支撑点", "scene_en": "The Support Point at Landing", "time": "00:33",
         "context": "落地的一瞬间，把身体的体重都移动到前脚掌做支撑。站直时重心在脚后跟上，向前移动时重心在前脚掌上，落的每一步都要落到有效的支撑点。",
         "sentences": [
            ["落地瞬间，把体重移动到前脚掌做支撑。", "At landing, shift your weight onto the forefoot for support.", "shift weight（转移体重）"],
            ["站直时重心在脚后跟，前移时重心在前脚掌。", "Standing, the center sits on the heel; moving, it sits on the forefoot.", "center of gravity（重心）"],
            ["每一步都要落到有效的支撑点。", "Every step must hit an effective support point.", "support point（支撑点）"]
         ]}
    ]
}

ARTICLES["running-form-errors"] = {
    "title_zh": "常见错误跑姿调整！让正确姿态刻在肌肉记忆",
    "title_en": "Fix Common Run Form, Engrave the Right Posture",
    "duration": "17秒",
    "topic": "运动 · 跑步",
    "scenes": [
        {"id": "s1", "scene_zh": "纠正动作不等于比赛跑姿", "scene_en": "Drills Aren't Race Form", "time": "00:00",
         "context": "「背手跑」是训练钻，用来逼出直立躯干与屈髋，不是要求正式跑时一直背手。口播不可辨，可核验结论来自画面大字、红叉/绿勾与笔记文案，三者一致。",
         "sentences": [
            ["纠正动作不等于比赛跑姿。", "Correction drills aren't race form.", "drill（训练钻）"],
            ["「背手跑」用来逼出直立躯干与屈髋。", "'Hands-behind running' forces an upright trunk and hip flexion.", "upright trunk（直立躯干）"],
            ["口播不可辨，结论来自画面标注与笔记。", "Narration is unclear—conclusions come from captions and notes.", "conclusions（结论）"]
         ]},
        {"id": "s2", "scene_zh": "错误一：趴着跑", "scene_en": "Mistake 1: Hunching", "time": "00:03",
         "context": "把过度前倾、躯干趴下去的跑法标为「趴着跑」。纠正方法是背手跑：双手背于身后继续跑，逼出直立躯干与屈髋。",
         "sentences": [
            ["趴着跑：过度前倾，躯干趴下去。", "Hunching: over-leaning with the trunk folded down.", "over-lean（过度前倾）"],
            ["纠正：背手跑，双手背于身后。", "Fix it with hands-behind running.", "hands-behind（背手）"],
            ["背手跑逼出直立躯干。", "It forces your trunk upright.", "force（逼出）"]
         ]},
        {"id": "s3", "scene_zh": "错误二：伸腿跑", "scene_en": "Mistake 2: Reaching", "time": "00:06",
         "context": "「伸腿跑」拆成两个可观察故障点：小腿抢到身前、后脚跟落地。压力大、刹车制动是作者对姿态后果的解释性判断；纠正方法是提拉抬腿，用向上提拉替代向前甩小腿。",
         "sentences": [
            ["伸腿跑：小腿抢到身前、后脚跟落地。", "Reaching: the shin lunges forward and the heel slams.", "reach（伸腿）"],
            ["这增加膝踝压力，并产生刹车制动。", "It loads the knees and ankles and brakes you.", "load（施压）"],
            ["纠正：提拉抬腿，用向上提拉替代向前甩小腿。", "Fix it by lifting—pull up instead of flinging the shin.", "lift（提拉）"]
         ]},
        {"id": "s4", "scene_zh": "目标姿态三要素", "scene_en": "The Three-Point Target", "time": "00:10",
         "context": "结尾把标准压成三条：上体垂直、屈髋抬腿、脚踝稳定。恢复摆臂后用三要素清单复检，而不是追求更大步幅。",
         "sentences": [
            ["目标姿态三要素：上体垂直、屈髋抬腿、脚踝稳定。", "Target posture: upright torso, hip-flexed lift, stable ankles.", "target posture（目标姿态）"],
            ["恢复摆臂后，用三要素清单复检。", "After normal arm swing, recheck with the three-point list.", "recheck（复检）"],
            ["不要盲目追求更大步幅。", "Don't chase a bigger stride.", "bigger stride（更大步幅）"]
         ]},
        {"id": "s5", "scene_zh": "行动清单与边界", "scene_en": "Action Steps and Limits", "time": "00:14",
         "context": "侧向录10-20秒慢跑对照是否趴躯干或小腿抢前；趴着跑就做背手跑钻，伸腿跑就做提拉抬腿钻；已有膝踝伤痛或平衡障碍者不宜盲目加大纠正钻强度；背手跑不适合作长时间主训练。",
         "sentences": [
            ["侧向录像10-20秒，对照两个错误。", "Film yourself from the side for 10-20 seconds to check.", "film（录像）"],
            ["趴着跑做背手跑，伸腿跑做提拉抬腿。", "Hunching? Hands-behind. Reaching? Lift drills.", "match（对应）"],
            ["有膝踝伤痛者不宜加大钻强度。", "Those with joint pain shouldn't push the drills harder.", "joint pain（关节痛）"]
         ]}
    ]
}


def build(slug, art):
    full_scenes = []
    for s in art["scenes"]:
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
            "title_cn": s["scene_zh"][:18] + ("…" if len(s["scene_zh"]) > 18 else ""),
            "title_en": s["scene_en"][:42] + ("…" if len(s["scene_en"]) > 42 else ""),
            "time": s["time"],
            "context": s["context"],
            "sentences": sentences,
            "paraphrase": paraphrase[:2],
            "speak": speak,
        })

    total_sents = sum(len(sc["sentences"]) for sc in full_scenes)
    words = []
    for sc in full_scenes:
        for t in sc["sentences"]:
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
            "title": art["title_zh"],
            "title_en": art["title_en"],
            "duration": art["duration"],
            "scenes": len(full_scenes),
            "sentences": total_sents,
            "date": "2026-08-08",
            "platform": "xiaohongshu",
            "source_url": f"http://xhslink.cn/o/{slug}",
            "topic": art["topic"],
        },
        "scene_imgs": [f"shot-{i:02d}" for i in range(1, len(full_scenes) + 1)],
        "scenes": full_scenes,
        "practice": art.get("practice", []),
        "pitfalls": art.get("pitfalls", []),
        "shifts": art.get("shifts", []),
        "difficult_words": words,
        "footer_notes": art.get("footer", ""),
    }
    p = DATA / f"{slug}.json"
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ {slug}: {len(full_scenes)} scenes, {total_sents} sents, {len(words)} words")


for slug, art in ARTICLES.items():
    build(slug, art)
print("完成")
