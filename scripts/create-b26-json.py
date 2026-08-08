#!/usr/bin/env python3
"""批26：为10篇小红书视频生成完整场景英译JSON（跑步送髋/跑步折叠/咖啡拉花/核心收紧/游泳技巧）。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

ARTICLES = {}

ARTICLES["songkuan-4tips"] = {
    "title_zh": "4个小技巧轻松拿捏送髋",
    "title_en": "4 Tips to Nail Hip Drive While Running",
    "duration": "1:37",
    "topic": "运动 · 跑步",
    "scenes": [
        {"id": "s1", "scene_zh": "热身：靠墙弓步蹲激活臀部", "scene_en": "Warm-Up: Wall Lunge to Fire Up the Glutes", "time": "00:00",
         "context": "练送髋之前先激活臀肌：保持站姿，身体前倾不靠墙，一侧脚向后踩住墙，上半身向前趴30度，重心向下蹲再起来，做15次，让臀部先有感觉。",
         "sentences": [
            ["我练送髋啊，爷就没有点针对性的训练？", "I'm working on hip drive—surely there's a targeted drill.", "hip drive（送髋）"],
            ["保持你现在的站姿，身体往前别靠墙，一侧脚向后再踩住墙。", "Keep your stance, lean forward off the wall, step one foot back onto it.", "stance（站姿）"],
            ["上半身向前趴30度，重心向下蹲再起来，臀部有感觉没？", "Fold forward 30°, squat down and rise—feel it in your glutes?", "glutes（臀部肌肉）"],
            ["15次够了，然后踩住你后面的小椅子。", "15 reps is enough; now step onto the stool behind you.", "rep（次数）"]
         ]},
        {"id": "s2", "scene_zh": "起身瞬间抬对侧腿摆臂", "scene_en": "Rise and Drive the Opposite Knee", "time": "00:27",
         "context": "保持刚才蹲的动作，起来的瞬间把对侧腿抬起来、把手臂摆起来，带点爆发力。这是把臀部力量转化为跑步动作的第一步。",
         "sentences": [
            ["保持刚才蹲的动作，起来的瞬间把对侧腿抬起来。", "Keep the squat, and as you rise, drive the opposite knee up.", "drive the knee（抬腿）"],
            ["把手臂摆起来，带点爆发力，碰一下抬起来。", "Swing your arms with a bit of explosion—tap and lift.", "explosion（爆发力）"],
            ["有感觉没？有劲！", "Feel it? Yes—it's firing!", "firing（发力）"]
         ]},
        {"id": "s3", "scene_zh": "单腿支撑平衡与后展", "scene_en": "Single-Leg Balance and Extension", "time": "00:42",
         "context": "双手抬平或抱手，保持单侧腿支撑，抬腿落地。单腿支撑时抬到90度向后伸展到最远方，保持平衡。这个动作训练送髋时的核心稳定。",
         "sentences": [
            ["双手抬平抱手，保持单侧腿支撑，抬腿落地。", "Hold your hands out or clasp them, balance on one leg, lift and land.", "single-leg support（单腿支撑）"],
            ["单腿支撑的时候，抬到90度向后伸展到最远方，保持平衡。", "On one leg, raise the knee to 90° and extend back as far as you can.", "extend（伸展）"],
            ["做得不错，感觉做起来很稳。", "Nice work—feels really stable.", "stable（稳定的）"]
         ]},
        {"id": "s4", "scene_zh": "原地摆臂送髋", "scene_en": "In-Place Arm Swing With Hip Drive", "time": "00:55",
         "context": "原地腿伸开，摆臂的瞬间后侧髋关节向前带一下再回来，一次一次做。这是把送髋直接装进摆臂节奏里的关键动作。",
         "sentences": [
            ["原地腿伸开，摆臂的瞬间，后侧髋关节向前带一下。", "Stand tall, and at the moment you swing, drive the rear hip forward.", "rear hip（后侧髋）"],
            ["带一下再回来，再一次一次，带一下再回来。", "Drive forward and back—again and again.", "drive forward（向前带动）"],
            ["可以，核心要收紧，髋关节带一点，不要你快。", "Good. Keep your core tight and drive the hip slightly—don't rush.", "core（核心）"]
         ]},
        {"id": "s5", "scene_zh": "收尾感受：髋部燃起来了", "scene_en": "The Payoff: Hips Are Fired Up", "time": "01:14",
         "context": "练完这段对话强调臀部真的被练到，引出一个认知：跑得快的运动员并不是靠死肌肉，而是靠力量转化为跑步技术。",
         "sentences": [
            ["我现在练完，感觉髋都大了，冲爆我了。", "After this, my hips feel huge—they're burning.", "burning（燃烧感）"],
            ["见了运动员或者肌肉块大的，那都是世界级的。", "Athletes or big-muscle guys are all world-class.", "world-class（世界级）"],
            ["那跑得快的都是大肌肉吗？你看这转化，连动起来。", "Are all fast runners muscular? Look at the transfer—it all links up.", "transfer（转化）"]
         ]}
    ]
}

ARTICLES["running-hip-drive"] = {
    "title_zh": "不送髋=费腿费力｜会送髋=轻松提速",
    "title_en": "No Hip Drive = Heavy Legs; Hip Drive = Easy Speed",
    "duration": "44秒",
    "topic": "运动 · 跑步",
    "scenes": [
        {"id": "s1", "scene_zh": "不送髋的后果", "scene_en": "What Happens Without Hip Drive", "time": "00:00",
         "context": "跑步要送髋，不送髋会怎样？后腿趋髋、下坐、脚后跟先着地，身体向前侵入，会造成膝关节和髋关节的运动损伤。",
         "sentences": [
            ["跑步要送髋，不送髋会怎样？", "You need hip drive when running—what happens if you don't?", "hip drive（送髋）"],
            ["后腿趋髋下坐，脚后跟先着地。", "You sit back, load the rear hip, and heel-strike first.", "heel-strike（脚跟着地）"],
            ["身体向前侵入，会造成膝关节、髋关节的运动损伤。", "Forward collapse like this leads to knee and hip overuse injuries.", "overuse injury（运动损伤）"]
         ]},
        {"id": "s2", "scene_zh": "什么叫送髋", "scene_en": "What 'Sending the Hip' Means", "time": "00:12",
         "context": "跑动的时候什么叫送髋？跑的时候髋关节向前顶出去就叫送髋；不送髋就是髋没往前顶、腿在后面拖着。",
         "sentences": [
            ["跑动的时候什么叫送髋？", "What does hip drive actually mean while running?", "hip drive（送髋）"],
            ["跑的时候髋往前顶出去，这样就送髋。", "Drive the hip forward as you run—that's sending it.", "drive forward（向前顶）"],
            ["这样就没送髋，这样就是送髋。", "Like this—no drive. Like this—drive.", "no drive（没送髋）"]
         ]},
        {"id": "s3", "scene_zh": "落地瞬间的身体直线", "scene_en": "A Straight Line at Foot Strike", "time": "00:20",
         "context": "跑的时候整体前倾，脚向前摆动落地的一瞬间，脚、髋、头要在一条竖直直线上，这样才算标准的送髋落地。",
         "sentences": [
            ["跑的时候整体前倾。", "Lean your whole body forward as you run.", "lean forward（前倾）"],
            ["脚向前摆动落地的一瞬间，脚、髋、头要在一条竖直直线。", "At the moment of landing, foot, hip and head form one vertical line.", "vertical line（竖直直线）"],
            ["这样就送髋。", "That's hip drive.", "hip drive（送髋）"]
         ]},
        {"id": "s4", "scene_zh": "想象背后有人推你", "scene_en": "Imagine Someone Pushing You Forward", "time": "00:31",
         "context": "跑动的时候，时刻感觉好像有人用手推着你的背往前走，这个意象能让身体自然进入前倾+送髋的节奏。",
         "sentences": [
            ["跑动的时候，时刻感觉有人用手推着你的背往前走。", "As you run, always feel like someone's hand is pushing your back forward.", "push forward（向前推）"],
            ["这个感觉能帮你自然送髋。", "That cue naturally engages your hip drive.", "cue（提示意象）"]
         ]},
        {"id": "s5", "scene_zh": "送髋省力提速", "scene_en": "Hip Drive Saves Energy", "time": "00:41",
         "context": "结论：跑步送髋，跑出风速，省力一半。送髋让每一步都借到重心前移的势能，腿不再拖着跑。",
         "sentences": [
            ["跑步送髋，跑出风速，省力一半。", "Run with hip drive and you'll feel half as tired.", "half as tired（省力一半）"],
            ["髋往前送，腿就轻松了。", "Drive the hip forward and your legs lighten up.", "lighten up（变轻松）"]
         ]}
    ]
}

ARTICLES["running-leg-fold"] = {
    "title_zh": "跑步腿沉拖沓？先把折叠搞清楚",
    "title_en": "Legs Feel Heavy? Learn the Fold, Not the Kick",
    "duration": "2分56秒",
    "topic": "运动 · 跑步",
    "scenes": [
        {"id": "s1", "scene_zh": "腿沉的根源：折叠与后撩分不清", "scene_en": "Heavy Legs: Confusing Fold With Kick-Back", "time": "00:00",
         "context": "如果你跑步总觉得腿沉重拖沓，可能是把折叠和后撩搞不清楚。今天的主题就是讲二者的区别，以及如何轻松做到正确的折叠。",
         "sentences": [
            ["如果你跑步总觉得腿沉重拖沓，可能是折叠和后撩搞不清楚。", "If your legs feel heavy and dragging, you may be mixing up the fold and the kick-back.", "fold（折叠）"],
            ["今天讲一下二者的区别，以及如何轻松做到正确的折叠。", "Today: the difference, and how to fold easily and correctly.", "kick-back（后撩）"]
         ]},
        {"id": "s2", "scene_zh": "正确折叠 vs 错误后撩", "scene_en": "Correct Fold vs Wrong Kick-Back", "time": "00:16",
         "context": "正确的折叠一定是大腿和小腿在身体下方产生的折叠；错误的后撩则是大腿和小腿在臀部后方产生。位置一前一后，效果天差地别。",
         "sentences": [
            ["正确的折叠，一定是大腿和小腿在身体下方产生的折叠。", "A correct fold happens with your thigh and shin under your body.", "under your body（身体下方）"],
            ["错误的后撩，是大腿和小腿在臀部后方产生的。", "A wrong kick-back happens behind your hips.", "behind the hips（臀部后方）"],
            ["两者的区别是什么？我们分别来看。", "What's the difference? Let's break it down.", "break it down（拆解）"]
         ]},
        {"id": "s3", "scene_zh": "正确折叠的动力学", "scene_en": "The Dynamics of a Correct Fold", "time": "00:32",
         "context": "身体往前失去平衡时，大腿和小腿在身体下方折叠。折叠的瞬间脚落地，重心在脚的正上方，然后重心更快地过了脚，身体继续向前失去平衡。",
         "sentences": [
            ["当身体往前失去平衡的时候，大腿和小腿在身体下方产生折叠。", "As your body falls forward, your thigh and shin fold beneath it.", "lose balance（失去平衡）"],
            ["脚落地瞬间，重心在脚的正上方。", "At landing, your center of gravity is right above the foot.", "center of gravity（重心）"],
            ["然后重心还能更快地过了你的脚，身体又可以继续向前失去平衡。", "Then the weight passes the foot quickly and you keep falling forward.", "pass over（越过）"]
         ]},
        {"id": "s4", "scene_zh": "后撩的坏处", "scene_en": "Why Kick-Back Hurts", "time": "00:49",
         "context": "如果身体前倾失衡时直接去后撩，撩完之后由于惯性小腿会甩到重心前面，产生制动，重心还得再走到脚正上方才能离地，这会大大增加脚与地面接触时间。",
         "sentences": [
            ["如果直接去后撩，撩完之后由于惯性，小腿还会甩到重心前面。", "If you kick back instead, inertia flings your shin ahead of your center of gravity.", "inertia（惯性）"],
            ["这样就容易产生制动。", "That creates braking force.", "braking（制动）"],
            ["这会大大增加你脚与地面接触的时间，腿也更累。", "It greatly increases ground contact time and tires your legs.", "ground contact time（触地时间）"]
         ]},
        {"id": "s5", "scene_zh": "最大区别：大腿的位置", "scene_en": "The Key Difference: Where the Thigh Is", "time": "01:19",
         "context": "折叠时大腿在躯干前侧，重心能更快向前；后撩时大腿在身体后面，重心是前不去的，等大腿转到前面重心才能走，这大大拖慢重心向前移动的速度。",
         "sentences": [
            ["折叠的时候，膝盖和大腿在躯干的前侧。", "When you fold, your knee and thigh are in front of your trunk.", "trunk（躯干）"],
            ["大腿在前面，重心就能更快地向前。", "Thigh forward means your weight moves forward faster.", "weight forward（重心前移）"],
            ["后撩时大腿在后面，重心是前不去的，这大大拖慢你的速度。", "With a kick-back, your thigh trails behind and the weight can't move on—slowing you down.", "trail behind（拖在后面）"]
         ]},
        {"id": "s6", "scene_zh": "如何做到正确折叠：腘绳肌发力", "scene_en": "How to Fold: Fire the Hamstrings", "time": "01:54",
         "context": "要轻松做到正确折叠，记住跑步时大腿后侧腘绳肌发力要积极。脚落地瞬间腘绳肌发力，小腿会瞬间向上折叠，折叠就会做得非常好。",
         "sentences": [
            ["跑步的时候，大腿后侧腘绳肌发力要积极。", "Run with active hamstring drive on the back of your thigh.", "hamstring（腘绳肌）"],
            ["脚落地瞬间腘绳肌发力，小腿会瞬间向上折叠。", "The instant your foot lands, fire the hamstring and the shin folds up.", "fire（发力）"],
            ["这样你的折叠会做得非常好。", "That makes for a beautiful fold.", "fold（折叠）"]
         ]},
        {"id": "s7", "scene_zh": "腘绳肌不积极的后果", "scene_en": "Lazy Hamstrings, Dragging Legs", "time": "02:09",
         "context": "如果脚落地后腘绳肌半天不发力，就会去蹬地，小腿和大腿在后面拖着，大腿前不来，重心就不会往前走，跑动效率大大下降。",
         "sentences": [
            ["如果脚落地后腘绳肌半天不发力，可能就会出现蹬地。", "If the hamstring is slow to fire, you end up pushing off the ground.", "push off（蹬地）"],
            ["小腿和大腿在后面拖着，大腿就前不来。", "Your shin and thigh drag behind, so the thigh can't come forward.", "drag（拖）"],
            ["大腿前不来，重心就不会往前走，拖慢你向前跑的效率。", "No thigh forward means no weight forward—slower and tiring.", "efficiency（效率）"]
         ]},
        {"id": "s8", "scene_zh": "总结：腘绳肌越积极，折叠越顺", "scene_en": "Active Hamstrings = Easy Fold", "time": "02:36",
         "context": "如果你跑步时总觉得腿拖沓沉重、腿在后面半天回不来，可能就是腘绳肌发力不积极。腘绳肌发力越积极，越能形成正确的折叠，脚能更好地落到身体下方，跑起来也更轻松。",
         "sentences": [
            ["如果你跑步时总觉得腿拖沓沉重，可能就是腘绳肌发力不积极。", "Heavy, dragging legs usually mean lazy hamstrings.", "lazy（不积极）"],
            ["腘绳肌发力越积极，越能形成正确的折叠。", "The more active the hamstring, the better your fold.", "the more... the better（越……越）"],
            ["这样脚能更好地落到身体下方，跑起来也更轻松。", "Your foot lands under your body and running gets easier.", "land under（落在下方）"]
         ]}
    ]
}

ARTICLES["coffee-latte-art-swing"] = {
    "title_zh": "咖啡拉花摆动技巧！零基础保姆级练习教程",
    "title_en": "Latte Art Swing: A Zero-to-One Practice Guide",
    "duration": "2分02秒",
    "topic": "生活 · 咖啡",
    "scenes": [
        {"id": "s1", "scene_zh": "翻车90%不是奶泡问题", "scene_en": "90% of Failures Aren't the Milk", "time": "00:00",
         "context": "很多新手拉花翻车90%都不是奶泡问题，是摆动不会。波纹乱、宽窄不一，拉出来的纹路僵硬不清晰。核心原因是手腕发力导致摆动节奏乱。",
         "sentences": [
            ["很多新手拉花翻车90%都不是奶泡问题，是摆动不会。", "Nine in ten newbie latte-art fails come from the swing, not the milk.", "latte art（拉花）"],
            ["核心原因是手腕发力导致摆动节奏乱，摆动快慢频率不一致。", "The real culprit is wrist power breaking the swing rhythm and frequency.", "rhythm（节奏）"],
            ["今天拆解一套拉花摆动核心技巧，从0到1的练习流程。", "Today: a core swing technique, a step-by-step path from zero.", "step-by-step（一步步的）"]
         ]},
        {"id": "s2", "scene_zh": "正确摆动：手臂稳、手腕晃", "scene_en": "The Right Swing: Steady Arm, Wrist Rocks", "time": "00:24",
         "context": "拉花摆动不是整只手左右摇动，那样只是倒奶不是摆动。正确的摆动应该是手臂稳、手腕晃水流呈现S形。",
         "sentences": [
            ["拉花摆动不是整只手左右摇动，这样不是摆动只是倒奶。", "Swinging isn't shaking your whole hand side to side—that's just pouring.", "pour（倒奶）"],
            ["正确的摆动应该是手臂稳、手腕晃水流呈现S形。", "The correct swing keeps the arm steady while the wrist rocks the flow into an S.", "S-curve（S形）"]
         ]},
        {"id": "s3", "scene_zh": "握缸手法", "scene_en": "How to Grip the Pitcher", "time": "00:36",
         "context": "中指、无名指、小拇指放在奶缸把手上，手臂打开，手肘与肩关节齐平，进行左右摆动，靠后方三个手指进行摆动。",
         "sentences": [
            ["中指、无名指、小拇指放在奶缸把手上。", "Rest your middle, ring and pinky fingers on the pitcher handle.", "pitcher（奶缸）"],
            ["手臂打开，手肘与肩关节齐平，进行左右摆动。", "Open your arm, elbow level with your shoulder, and swing side to side.", "elbow（手肘）"],
            ["靠后方三个手指进行摆动，这是手腕的惯性运动。", "Swing with those three back fingers—it's an inertial wrist motion.", "inertial（惯性的）"]
         ]},
        {"id": "s4", "scene_zh": "发力越轻纹路越细腻", "scene_en": "Lighter Touch, Finer Pattern", "time": "00:45",
         "context": "摆动是手腕的惯性运动，发力越轻越放松，奶的纹路越细腻。紧张发力会让水流忽大忽小。",
         "sentences": [
            ["左右摆动是手腕的惯性运动。", "Side-to-side swinging is an inertial wrist motion.", "inertial（惯性的）"],
            ["发力越轻越放松，奶的纹路越细腻。", "The lighter and more relaxed you are, the finer the pattern.", "fine（细腻的）"]
         ]},
        {"id": "s5", "scene_zh": "第一天：玩水练动作", "scene_en": "Day 1: Practice With Water", "time": "00:54",
         "context": "零基础练习摆动先从玩水开始，只练动作：放水流呈现S形，每天三组每组一分钟，全程不抖，速度均匀幅度一致。",
         "sentences": [
            ["零基础练习摆动可以先从玩水开始，只练动作。", "Start from zero by swinging water, just to build the motion.", "build the motion（练动作）"],
            ["放水流呈现S形，每天三组每组一分钟，全程不抖。", "Pour an S-shaped stream, three sets of one minute a day, no shaking.", "set（一组）"],
            ["速度均匀，幅度一致。", "Steady speed, consistent width.", "consistent（一致的）"]
         ]},
        {"id": "s6", "scene_zh": "第二天：定点摆动", "scene_en": "Day 2: Stationary Swing", "time": "01:05",
         "context": "稳定之后第二天练习定点摆动：拿出空杯模拟拉花摆动手法，定点摆动就是只摆不退，观察水面的波纹，练出整齐平行、宽窄一致的纹路。",
         "sentences": [
            ["稳定之后，第二天练习定点摆动，拿出空杯模拟拉花摆动手法。", "Once steady, day two is the stationary swing—mime it over an empty cup.", "stationary（定点的）"],
            ["定点摆动就是只摆不退，观察水面的波纹。", "Swing in place without backing up, watching the ripples.", "ripple（波纹）"],
            ["练出整齐平行、宽窄一致的纹路，改掉忽大忽小、左右偏移的坏习惯。", "Aim for parallel, even lines—fix the uneven, drifting habit.", "drift（偏移）"]
         ]},
        {"id": "s7", "scene_zh": "第三天：摆动+后退", "scene_en": "Day 3: Swing and Retreat", "time": "01:21",
         "context": "学会稳定摆动后，第三天加上摆动加后退的动作。练习重点是摆动不停、后退不加速，全程节奏统一，前期用反复用水练习。",
         "sentences": [
            ["第三天可以加上摆动加后退的动作。", "Day three adds the swing-and-retreat motion.", "retreat（后退）"],
            ["练习的重点是摆动不停、后退不加速，全程节奏统一。", "The key: never stop swinging, never speed up the retreat—one steady tempo.", "tempo（节奏）"],
            ["前期可以用水反复练习，基础的拉花直接就能成型。", "Drill with water first, and basic latte art just takes shape.", "take shape（成型）"]
         ]},
        {"id": "s8", "scene_zh": "实战：压低出杯", "scene_en": "For Real: Low, Then Swing", "time": "01:37",
         "context": "掌握摆动技巧后，直接用牛奶和浓缩液实战。压低出杯后进行左右摆动，边摆边慢慢回杯，摆动流量均匀不要刻意发力，纹路就会非常清晰。",
         "sentences": [
            ["压低出杯后进行左右摆动。", "Pour low at the cup, then swing side to side.", "pour low（压低出杯）"],
            ["边摆边慢慢回杯，摆动流量均匀，不要刻意发力。", "Swing while slowly pulling back—keep the flow even, no forced power.", "pull back（回杯）"],
            ["这样纹路就会非常清晰。", "That gives you crisp, clean lines.", "crisp（清晰的）"]
         ]},
        {"id": "s9", "scene_zh": "成品：树叶拉花", "scene_en": "The Payoff: A Leaf Latte", "time": "01:52",
         "context": "摆动过程中加上后退的动作，摆动的宽幅、流量、频率要确保一致，这样你就得到了一杯好看的树叶拉花。",
         "sentences": [
            ["摆动的宽幅、流量、频率要确保一致。", "Keep the width, flow and frequency of your swing consistent.", "width（宽幅）"],
            ["这样你就得到了一杯好看的树叶拉花。", "And there it is—a beautiful leaf latte.", "leaf（树叶纹）"],
            ["你也学会了吗？", "Have you got it too?", "got it（学会了）"]
         ]}
    ]
}

ARTICLES["gaozhou-jueding-meichou"] = {
    "title_zh": "高肘决定美丑",
    "title_en": "High Elbow Decides Beauty",
    "duration": "13秒",
    "topic": "运动 · 游泳",
    "scenes": [
        {"id": "s1", "scene_zh": "标题定性：审美判断", "scene_en": "The Claim: Beauty, Not Just Technique", "time": "00:00",
         "context": "全片无口播，Whisper转录只有背景音乐的幻觉字幕，所有判断都来自画面文字条与动作对比。标题「高肘决定美丑」是创作者给出的审美评价，本质是主观立场。",
         "sentences": [
            ["「高肘决定美丑」是创作者给出的审美评价，本质是主观立场。", "'High elbow decides beauty' is the creator's aesthetic call—subjective at heart.", "aesthetic（审美的）"],
            ["视频用13秒分屏对照，把正确与错误示范浓缩成两条固定文字条。", "Thirteen seconds of split-screen distills right vs wrong into two fixed captions.", "split-screen（分屏）"],
            ["全片无口播，所有判断依据来自画面文字条、动作对比和截图。", "No narration—all evidence is on-screen captions, motion and stills.", "narration（口播）"]
         ]},
        {"id": "s2", "scene_zh": "正确：高肘移臂", "scene_en": "Correct: The High-Elbow Recovery", "time": "00:03",
         "context": "视频认定的正确做法：手臂划水结束准备移臂出水时，肘部先于手掌和小臂抬起，肘尖朝前方顶出；小臂保持放松、自然下垂；因为肘部先抬高、身体略微侧转，腋窝会随动作自然露出。",
         "sentences": [
            ["移臂出水时，肘部先于手掌和小臂抬起，肘尖朝前方顶出。", "Exiting the water, the elbow lifts before hand and forearm, pointing forward.", "recovery（移臂）"],
            ["小臂保持放松、自然下垂，不主动用力。", "The forearm stays relaxed and hangs naturally.", "forearm（小臂）"],
            ["因为肘部先抬高、身体略微侧转，腋窝会自然露出。", "With the elbow up and a slight roll, the armpit naturally shows.", "armpit（腋窝）"]
         ]},
        {"id": "s3", "scene_zh": "错误：举手移臂", "scene_en": "Wrong: The Hand-First Recovery", "time": "00:06",
         "context": "视频认定的错误做法：移臂时是手先主动抬起发力，肘部没有跟上抬高的节奏反而被压低，藏在身体一侧，腋窝看不见；小臂被举得很高很直，容易手掌拍水。",
         "sentences": [
            ["错误做法是手先主动抬起发力，肘部被压低藏起来。", "The wrong way lifts the hand first while the elbow drops and hides.", "hide（藏起来）"],
            ["小臂被举得很高很直，腋窝因此看不见。", "The forearm goes high and straight, so the armpit disappears.", "straight（笔直的）"],
            ["出水或回摆阶段容易出现手掌拍打水面的动作。", "This often ends in slapping the water with the palm.", "slap（拍打）"]
         ]},
        {"id": "s4", "scene_zh": "结论：把好看和有效分开", "scene_en": "Separate 'Looks' From 'Works'", "time": "00:09",
         "context": "这条视频只解决了「好看」的判断标准，效率和安全性没有数据支撑。练习时要分开验证：高肘移臂看起来协调美观，但技术效率需要参考更系统的资料。",
         "sentences": [
            ["把「好看」和「有效」分开验证。", "Verify 'looks good' and 'works well' separately.", "separately（分开地）"],
            ["这条视频只定义了美观的标准，没有给出速度或安全的数据。", "It only defines beauty—no speed or safety data.", "data（数据）"],
            ["练习时让肘部先于手掌离开水面，改变发力顺序。", "Practice lifting the elbow before the hand to change the firing order.", "firing order（发力顺序）"]
         ]},
        {"id": "s5", "scene_zh": "行动清单", "scene_en": "Action Steps", "time": "00:12",
         "context": "练习移臂时有意识让肘先离水；移臂过程中保持小臂放松；对镜或录像检查移臂时腋窝是否自然露出，作为肘部先动的直观参照；避免手掌主动拍水。",
         "sentences": [
            ["练习移臂时，有意识让肘部先于手掌离开水面。", "In practice, deliberately clear the elbow from the water before the hand.", "clear the water（出水）"],
            ["对着镜子或录像检查移臂时腋窝是否自然露出。", "Check in a mirror or video whether the armpit opens naturally.", "mirror（镜子）"],
            ["避免用手掌主动拍打水面，让手臂更顺滑地回到前伸位置。", "Avoid slapping; bring the arm back smoothly toward extension.", "extension（前伸）"]
         ]}
    ]
}

ARTICLES["hexin-shoujin-teaching"] = {
    "title_zh": "学不会收紧核心？一个视频教会你如何收紧核心",
    "title_en": "Can't Tighten Your Core? This Video Teaches You",
    "duration": "23秒",
    "topic": "运动 · 核心训练",
    "scenes": [
        {"id": "s1", "scene_zh": "反例：吸肚子不是收紧核心", "scene_en": "The Trap: Sucking In ≠ Tightening", "time": "00:00",
         "context": "这是吸肚子，核心是散的。从侧面看肋骨是打开外翻的——吸腹可能只是表层皮肤与腹直肌收缩，腹横肌与肋廓并未协同内收。",
         "sentences": [
            ["这是吸肚子，核心是散的。", "This is just sucking in—your core is loose.", "suck in（吸肚子）"],
            ["从侧面看，肋骨是打开外翻的。", "From the side, your ribs are flared outward.", "flared ribs（肋骨外翻）"],
            ["吸腹不等于核心收紧，深层稳定肌群没有参与。", "Sucking in isn't bracing—the deep stabilizers aren't engaged.", "stabilizer（稳定肌）"]
         ]},
        {"id": "s2", "scene_zh": "蜡烛吹气：建立肋廓内收", "scene_en": "Blow Out a Candle: Ribs In", "time": "00:06",
         "context": "假装前面有个蜡烛，对着蜡烛使劲吹，肋骨下缘向前向内收。这是呼吸驱动下的胸廓-腹压联动，比单纯憋气更接近功能性的核心激活。",
         "sentences": [
            ["假装前面有个蜡烛，对着蜡烛使劲吹。", "Pretend there's a candle—blow at it with force.", "candle（蜡烛）"],
            ["吹气让肋骨下缘向前向内收。", "Blowing pulls your lower ribs down and in.", "lower ribs（下肋）"],
            ["这是呼吸驱动的胸廓与腹压联动。", "It's breath-driven ribcage and abdominal pressure working together.", "abdominal pressure（腹压）"]
         ]},
        {"id": "s3", "scene_zh": "咳嗽两声：激活腹横肌", "scene_en": "Two Coughs: Wake the Transversus", "time": "00:11",
         "context": "连续咳嗽两声，唤醒腹横肌。咳嗽提供爆发式的腹压，用于找到收紧的感觉。",
         "sentences": [
            ["连续咳嗽两声，唤醒腹横肌。", "Cough twice in a row to wake up the transversus abdominis.", "transversus abdominis（腹横肌）"],
            ["咳嗽提供爆发式的腹压。", "A cough creates an explosive spike of abdominal pressure.", "explosive（爆发式的）"]
         ]},
        {"id": "s4", "scene_zh": "发嘶音：维持张力", "scene_en": "A Long 'Sss': Hold the Tension", "time": "00:15",
         "context": "继续发嘶的音，用持续的呼气阻力把腹压张力延长。咳嗽找到收紧感，嘶音保持住收紧感。",
         "sentences": [
            ["继续发嘶的音。", "Keep making the hissing 'sss' sound.", "hiss（嘶音）"],
            ["嘶音提供持续的呼气阻力，把张力延长。", "The hiss adds steady exhalation resistance to hold the tension.", "tension（张力）"]
         ]},
        {"id": "s5", "scene_zh": "验收：整个腰腹发硬", "scene_en": "The Check: A Hard Cylinder of a Trunk", "time": "00:18",
         "context": "用手触或自我感知，确认不是局部吸腹，而是腰腹区域整体发紧、变硬。这是完成标志，也是与开场反例的对照终点。",
         "sentences": [
            ["用手触摸腰腹，整个腰腹都是硬的。", "Touch your midsection—the whole waist should feel hard.", "midsection（腰腹）"],
            ["确认不是局部吸腹，而是整体发紧。", "Make sure it's global tightness, not a local suck-in.", "global（整体的）"],
            ["恭喜你学会收紧核心。", "Congrats—you've learned to brace your core.", "brace（收紧支撑）"]
         ]}
    ]
}

ARTICLES["ziyouyong-gunfan-jiqiao"] = {
    "title_zh": "教学合集｜自由泳滚翻技巧",
    "title_en": "Freestyle Tumble Turn in Five Beats",
    "duration": "11秒",
    "topic": "运动 · 游泳",
    "scenes": [
        {"id": "s1", "scene_zh": "第一拍：收臂贴紧", "scene_en": "Beat 1: Arms In, Streamlined", "time": "00:00",
         "context": "最后一把划水完成后，双臂迅速收拢贴在躯干两侧不再外划。这一动作减少水阻，为向前翻滚腾出旋转空间，是游进到转身的过渡信号。",
         "sentences": [
            ["最后一把划水完成后，双臂贴紧身体不动。", "After the final pull, pin both arms tight to your sides.", "pin（贴紧）"],
            ["收臂减少水阻，为翻滚腾出旋转空间。", "Arms in reduce drag and make room for the roll.", "drag（水阻）"],
            ["这是从游进到转身的过渡信号。", "It signals the shift from swimming to turning.", "transition（过渡）"]
         ]},
        {"id": "s2", "scene_zh": "第二拍：收下巴蜷体", "scene_en": "Beat 2: Tuck and Roll", "time": "00:02",
         "context": "三个连续的身体指令：手下摆、眼睛看脚尖、头去找膝盖。身体折叠成紧凑的球状，这是翻滚半径最小的关键姿势。",
         "sentences": [
            ["手下摆，眼睛看脚尖，头去找膝盖。", "Hands sweep down, eyes on your toes, head reaching for your knees.", "tuck（蜷体）"],
            ["身体折叠成紧凑的球状，翻滚半径最小。", "Fold into a tight ball for the smallest turning radius.", "turning radius（翻滚半径）"],
            ["这是关键姿势，头找膝盖让转动更快。", "Head-to-knee is the key for a faster spin.", "spin（转动）"]
         ]},
        {"id": "s3", "scene_zh": "第三拍：蓄力转身", "scene_en": "Beat 3: Load the Roll", "time": "00:05",
         "context": "身体从蜷曲球状开始向前下方翻滚旋转，翻滚动量在此刻积累，为触壁蹬出做准备。",
         "sentences": [
            ["身体从蜷曲球状开始向前下方翻滚。", "From the tucked ball, roll forward and downward.", "roll（翻滚）"],
            ["翻滚动量在此刻积累，为蹬壁做准备。", "Momentum builds here, readying the push-off.", "momentum（动量）"]
         ]},
        {"id": "s4", "scene_zh": "第四拍：腰背打直流线蹬出", "scene_en": "Beat 4: Straighten and Push Off", "time": "00:07",
         "context": "翻滚完成后身体迅速伸展：腰背绷直、双臂向前伸直夹紧在头部两侧，进入蹬壁前的流线型预备姿态。画面与口播都强调：不要转动躯干直接蹬出。",
         "sentences": [
            ["腰背打直，手伸直加紧在头部两侧。", "Straighten your back, arms extended and squeezed by your head.", "straighten（打直）"],
            ["注意这个时候不要转动躯干直接蹬出。", "Don't twist your trunk—push off straight away.", "push off（蹬壁）"],
            ["滑行时再转体，保持流线型获得最大距离。", "Rotate only while gliding to keep the streamline and gain distance.", "streamline（流线型）"]
         ]},
        {"id": "s5", "scene_zh": "关键认知：蹬壁≠立刻转体", "scene_en": "The Mindset Shift: Push Off Straight", "time": "00:09",
         "context": "全片最关键提醒：蹬壁时不要提前转躯干，保持流线型直接蹬出，滑行一段后再转体恢复划水。这一认知可能是这个11秒视频最有价值的单点提醒。",
         "sentences": [
            ["蹬壁时保持流线型直接滑行，不要提前转体。", "Push off streamlined and glide before you rotate.", "glide（滑行）"],
            ["滑行一段后再转体恢复划水。", "Rotate to resume swimming only after a moment of glide.", "resume（恢复）"],
            ["把「蹬壁=立刻转回游进方向」变成「蹬壁=流线滑行再转」。", "Change 'push off = turn now' into 'push off = glide, then turn'.", "mindset shift（认知转变）"]
         ]}
    ]
}

ARTICLES["ziyouyong-datui-cuowu"] = {
    "title_zh": "自由泳打腿最容易出现的错误",
    "title_en": "The Most Common Freestyle Kick Mistakes",
    "duration": "14秒",
    "topic": "运动 · 游泳",
    "scenes": [
        {"id": "s1", "scene_zh": "错误1：直腿打水", "scene_en": "Mistake 1: Stiff-Leg Kicking", "time": "00:00",
         "context": "视频用两条字幕指出两种相反的膝关节错误。错误1「直腿打水」：膝盖几乎不弯，大小腿像一根棍子整体摆动，膝关节僵直。",
         "sentences": [
            ["直腿打水：膝盖几乎不弯，大小腿像一根棍子整体摆动。", "Stiff-leg kicking: the knee barely bends and the leg swings like a rod.", "stiff（僵直的）"],
            ["膝关节僵直是打腿效率低的常见原因。", "A locked knee is a common cause of a weak kick.", "locked knee（僵直的膝盖）"]
         ]},
        {"id": "s2", "scene_zh": "错误2：锄头脚", "scene_en": "Mistake 2: The 'Hoe Foot'", "time": "00:04",
         "context": "错误2「锄头脚」：打腿时脚踝勾起背屈，没有用脚背打水，推水面从脚背变成了脚底，形似锄地的角度。",
         "sentences": [
            ["锄头脚：打腿时脚踝勾起，形似锄地的角度。", "The hoe foot: you point your ankle up, digging like a hoe.", "hoe（锄头）"],
            ["没有用脚背打水，推水面从脚背变成了脚底。", "You push with the sole instead of the top of the foot.", "sole（脚底）"]
         ]},
        {"id": "s3", "scene_zh": "错误3：小腿打水", "scene_en": "Mistake 3: Shin-Dominated Kicking", "time": "00:08",
         "context": "错误3「小腿打水」：膝盖弯曲过大，动作变成主要靠小腿发力，大腿没有带动小腿完成鞭状动作。与错误1方向相反，说明膝关节弯曲存在合适区间。",
         "sentences": [
            ["小腿打水：膝盖弯曲过大，主要靠小腿发力。", "Shin kicking: the knee bends too much and the shin does the work.", "shin（小腿）"],
            ["大腿没有带动小腿完成鞭状动作。", "The thigh isn't driving a whipping motion down the leg.", "whip（鞭状）"],
            ["错误1和错误3方向相反，说明膝关节弯曲有个合适区间。", "The two mistakes run opposite ways—knee bend has a sweet spot.", "sweet spot（合适区间）"]
         ]},
        {"id": "s4", "scene_zh": "错误4：幅度过大", "scene_en": "Mistake 4: Too Big a Range", "time": "00:11",
         "context": "错误4「打腿幅度过大」：打腿上下摆动时两腿分离距离过开，超出正常范围。幅度过大既费力又不经济。",
         "sentences": [
            ["打腿幅度过大：两腿分离太开，超出正常范围。", "Too big a range: the legs spread too wide.", "range（幅度）"],
            ["幅度过大既费力又不经济。", "Overkicking wastes energy.", "overkick（过度打腿）"]
         ]},
        {"id": "s5", "scene_zh": "总结：三维修正", "scene_en": "Fix in Three Dimensions", "time": "00:13",
         "context": "四个错误覆盖膝关节两极端、踝关节角度、动作幅度三个维度。行动：先自查膝关节更偏哪个极端，放松踝关节避免锄头脚，控制幅度在小范围摆动。",
         "sentences": [
            ["膝关节弯曲要适中，既不能打直也不能弯曲过大。", "Knee bend must be moderate—neither locked nor over-flexed.", "moderate（适中的）"],
            ["踝关节放松绷直，用脚背而不是脚底推水。", "Keep the ankle relaxed and pointed, pushing with the foot top.", "pointed（绷直的）"],
            ["逐项对照四条字幕自查，而不是笼统地多练。", "Check yourself against each caption instead of just 'kick more'.", "check against（对照检查）"]
         ]}
    ]
}

ARTICLES["aijiaolian-zhuanshen-duibi"] = {
    "title_zh": "游泳转身正确动作vs错误动作",
    "title_en": "Swimming Turn: Right vs Wrong",
    "duration": "30秒",
    "topic": "运动 · 游泳",
    "scenes": [
        {"id": "s1", "scene_zh": "分屏对比：真正的差距在哪", "scene_en": "Split Screen: Where the Gap Is", "time": "00:00",
         "context": "不要把这段视频理解成两人游泳速度天生不同。分屏显示两人在触壁前的划水阶段差异并不悬殊，真正拉开差距的关键帧出现在贴壁之后。",
         "sentences": [
            ["分屏画面显示两人在触壁前的划水阶段差异并不悬殊。", "The split screen shows little difference in their strokes before the wall.", "stroke（划水）"],
            ["真正拉开差距的关键帧出现在贴壁之后。", "The gap truly opens after they hit the wall.", "key frame（关键帧）"]
         ]},
        {"id": "s2", "scene_zh": "贴壁翻滚的紧凑度", "scene_en": "Tightness of the Tumble", "time": "00:05",
         "context": "快到池壁时两人几乎同时低头收腿向前翻滚，但✓泳者的身体折叠角度更小、翻滚半径更紧凑；✗泳者身体展开幅度更大，翻滚显得更松。",
         "sentences": [
            ["快到池壁时，两人几乎同时低头收腿、开始向前翻滚。", "At the wall, both drop their heads and tuck to roll forward.", "tuck（收腿）"],
            ["✓泳者的折叠角度更小，翻滚半径更紧凑。", "The ✓ swimmer folds tighter with a more compact radius.", "compact（紧凑的）"],
            ["✗泳者展开幅度更大，翻滚显得更松。", "The ✗ swimmer opens up more, looking loose.", "loose（松散的）"]
         ]},
        {"id": "s3", "scene_zh": "关键帧：蹬壁时机", "scene_en": "The Key Frame: Push-Off Timing", "time": "00:06",
         "context": "00:06.75是整段对比里差异最明显的时刻：✓泳者双脚已经蹬离池壁、身体伸展成流线型向前冲出；✗泳者此时仍处于收拢、脚还未完全离墙的翻滚阶段。",
         "sentences": [
            ["✓泳者已经蹬离池壁，伸展成流线型向前冲出。", "The ✓ swimmer is already pushing off and extending streamlined.", "extend（伸展）"],
            ["✗泳者此时还在收拢翻滚，脚还未离墙。", "The ✗ swimmer is still tucked and rolling.", "still tucked（仍在收拢）"],
            ["同一时间点上，两人的转身进度已经拉开。", "At the same instant, their turn progress has already diverged.", "diverged（拉开差距）"]
         ]},
        {"id": "s4", "scene_zh": "蹬壁后的流线滑行", "scene_en": "Glide After the Push-Off", "time": "00:07",
         "context": "蹬壁离墙后两人都进入水下流线型滑行，姿势本身都基本合格，但因为✓更早完成蹬壁，滑行位置持续领先✗约一个身位。",
         "sentences": [
            ["两人都进入水下流线型滑行，姿势基本合格。", "Both glide streamlined underwater with decent form.", "glide（滑行）"],
            ["因为✓更早完成蹬壁，滑行位置领先约一个身位。", "Pushing off earlier keeps ✓ about a body length ahead.", "body length（身位）"],
            ["转身效率的差距主要来自蹬壁时机，而非滑行姿势。", "The gap comes from push-off timing, not glide form.", "timing（时机）"]
         ]},
        {"id": "s5", "scene_zh": "行动清单", "scene_en": "Action Steps", "time": "00:20",
         "context": "贴壁前用力收膝抱团，练习更小的翻滚半径；用水下摄像或计时检查自己触壁瞬间双脚是否已经开始蹬伸；蹬壁后保持双臂前伸、身体绷直，把翻滚动量转化为前冲距离。",
         "sentences": [
            ["贴壁前用力收膝抱团，让翻滚半径更小、动作更紧凑。", "Before the wall, pull your knees in hard for a tighter roll.", "pull in（收拢）"],
            ["检查自己触壁瞬间双脚是否已经开始蹬伸。", "Check whether your feet are already driving at the touch.", "touch（触壁）"],
            ["蹬壁后保持流线型，把翻滚动量转化为前冲距离。", "Stay streamlined after the push to turn momentum into distance.", "turn into（转化为）"]
         ]}
    ]
}

ARTICLES["youyong-zhuanshen-duibi-2"] = {
    "title_zh": "你能看出这两种开放式游泳转身有什么不同",
    "title_en": "Spot the Difference in These Open Turns",
    "duration": "16秒",
    "topic": "运动 · 游泳",
    "scenes": [
        {"id": "s1", "scene_zh": "问题引入：两种转身有何不同", "scene_en": "Two Open Turns, One Difference", "time": "00:00",
         "context": "视频对比两种开放式转身。很多人以为转身速度差距来自蹬壁力量大小，但这段对比显示：两人蹬壁力度看起来相近，真正拉开差距的是转身各阶段之间的衔接速度。",
         "sentences": [
            ["你能看出这两种开放式游泳转身有什么不同吗？", "Can you spot the difference between these two open turns?", "open turn（开放式转身）"],
            ["转身速度差距不是来自蹬壁力量，而是动作衔接的速度。", "The gap comes from transition speed, not push-off strength.", "transition（衔接）"],
            ["尤其「从蜷体到流线展开」这一步的切换快慢。", "Especially how fast they switch from tuck to streamline.", "switch（切换）"]
         ]},
        {"id": "s2", "scene_zh": "什么是开放式转身", "scene_en": "What an Open Turn Is", "time": "00:05",
         "context": "开放式转身也叫触壁转身：游到池壁时单手或双手触壁，不做翻滚，头部始终露出水面完成转身动作，随后屈膝收腿、贴壁蹬出，再展开成流线型继续游进。",
         "sentences": [
            ["开放式转身：游到池壁时单手或双手触壁，不做翻滚。", "An open turn touches the wall with one or two hands, no flip.", "touch the wall（触壁）"],
            ["头部始终露出水面完成转身动作。", "The head stays above water through the turn.", "above water（露出水面）"],
            ["随后屈膝收腿、贴壁蹬出，再展开成流线型。", "Then bend, tuck, push off, and extend into a streamline.", "tuck（收腿）"]
         ]},
        {"id": "s3", "scene_zh": "差距环节：进与出的流线切换", "scene_en": "The Gap: Faster Streamlining In and Out", "time": "00:08",
         "context": "视频描述原文：「这位顶级游泳选手在进出转弯时都更快地进入流线，这让她保持了速度。」作者指出「进」（触壁蜷体）和「出」（蹬壁展开）两个阶段的流线切换是拉开差距的关键。",
         "sentences": [
            ["这位顶级选手在进出转弯时都更快地进入流线。", "This elite swimmer streamlines faster both into and out of the turn.", "elite（顶尖的）"],
            ["「进」和「出」两个阶段的流线切换拉开了差距。", "Streamlining at both entry and exit is where she gains.", "entry and exit（进与出）"],
            ["保持流线让她保住了速度。", "Holding the streamline lets her keep her speed.", "hold（保持）"]
         ]},
        {"id": "s4", "scene_zh": "初学者的两个慢点", "scene_en": "Where Beginners Lose Time", "time": "00:12",
         "context": "初学者在两个环节最容易慢半拍：一是触壁时机（手臂前伸拖延，没有第一时间触壁收腿）；二是蜷体到流线的切换（蹬壁后仍保持团身姿态，没有立刻伸展手臂拉长身体）。",
         "sentences": [
            ["初学者最容易慢半拍：触壁时机拖延。", "Beginners lose time first on a late touch.", "late touch（触壁晚）"],
            ["蜷体到流线的切换：蹬壁后没有立刻伸展手臂。", "They also stay tucked too long instead of reaching out.", "reach out（伸展）"],
            ["这两个慢点叠加，身位差距就出来了。", "Stacked together, the two slow points open up a gap.", "stack（叠加）"]
         ]},
        {"id": "s5", "scene_zh": "行动清单", "scene_en": "Action Steps", "time": "00:14",
         "context": "练习触壁反应：游到池壁前提前判断距离，减少手臂前伸的犹豫时间；专项练习蹬壁到展开的衔接，用陆地或扶壁蹬腿强化蹬壁后立刻伸展手臂的肌肉记忆；录制转身视频逐帧回放找慢点。",
         "sentences": [
            ["练习触壁反应：提前判断距离，减少犹豫。", "Practice the touch reaction—judge the distance early.", "judge the distance（判断距离）"],
            ["专项练习蹬壁到展开的衔接，强化肌肉记忆。", "Drill the push-off-to-extend link to build muscle memory.", "muscle memory（肌肉记忆）"],
            ["录制自己的转身视频逐帧回放，找出自己的慢点。", "Film your turn and review frame by frame to find your weak spot.", "frame by frame（逐帧）"]
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
