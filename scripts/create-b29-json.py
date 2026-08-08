#!/usr/bin/env python3
"""批29：为10篇小红书游泳技术视频生成完整场景英译JSON。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

ARTICLES = {}

ARTICLES["ziyouyong-qingsong-changyou"] = {
    "title_zh": "自由泳如何才能游得轻松、距离游得长一些",
    "title_en": "How to Swim Freestyle Effortlessly and Long",
    "duration": "1分29秒",
    "topic": "游泳 · 自由泳",
    "scenes": [
        {"id": "s1", "scene_zh": "第一步：检查你的腿", "scene_en": "Step 1: Check Your Legs", "time": "00:07",
         "context": "粉丝朋友问自由泳怎么样才能游得轻松一点、时间和距离都长一点。第一步可以先看看自己游的时候腿是沉在水下还是飘在水上。腿的位置决定了水阻大小。",
         "sentences": [
            ["游的时候，腿是沉在水下还是飘在水上？", "Is your leg sinking below or floating on the water?", "sink（下沉）"],
            ["第一步，先检查自己打腿的位置。", "Step one: check where your kick sits.", "kick（打腿）"],
            ["腿的位置直接决定了阻力大小。", "Leg position directly sets your drag.", "drag（水阻）"]
         ]},
        {"id": "s2", "scene_zh": "第二步：划手要拉长", "scene_en": "Step 2: Lengthen the Pull", "time": "00:24",
         "context": "除了打腿就是划手。手臂的行程要足够长：行程太短会游出狗刨式；太软的行程会让你划得非常吃力，消耗过多的氧气，可能到25米、50米就游不动了。怎么做长行程？要注意前伸的动作。",
         "sentences": [
            ["手臂的行程要足够长，行程太短就是狗刨式。", "Your stroke must be long enough—too short means dog-paddling.", "stroke（划水行程）"],
            ["太软的行程会让你划得非常吃力。", "A floppy pull wears you out fast.", "floppy（软塌的）"],
            ["游到25米、50米就没劲了，是做长前伸的关键。", "Gassing out at 25 or 50 meters means your extension is short.", "extension（前伸）"]
         ]},
        {"id": "s3", "scene_zh": "第三步：侧身换气", "scene_en": "Step 3: Breathe Sideways", "time": "00:57",
         "context": "最后一步做好换气动作。很多同学自由泳换气就跟救命一样，上半身抬太高，下半身就会掉下去，整个人是往下潜的。自由泳的换气是侧面呼吸：转体侧头，而不是抬头。",
         "sentences": [
            ["很多同学换气像救命，上半身抬太高。", "Many swimmers gasp and lift their chest too high.", "gasp（大口喘气）"],
            ["上半身太高，下半身就会掉下去。", "Raise the chest and your legs sink.", "sink（下沉）"],
            ["自由泳换气是侧面呼吸，不是抬头。", "Freestyle breathing is sideways, never face-up.", "sideways breathing（侧向换气）"]
         ]}
    ]
}

ARTICLES["ziyouyong-tisu-tips"] = {
    "title_zh": "有效提高自由泳提速的小技巧",
    "title_en": "Small Tricks to Speed Up Freestyle",
    "duration": "53秒",
    "topic": "游泳 · 自由泳",
    "scenes": [
        {"id": "s1", "scene_zh": "转胯提高效率", "scene_en": "Hip Rotation Lifts Efficiency", "time": "00:00",
         "context": "听说自由泳要转胯才好？那必须是。转胯自由泳更好更轻松。第一，提高效率：通过转胯手滑得更长，这样每一次划水都推得更远。",
         "sentences": [
            ["听说自由泳要转胯才好？那必须是。", "Heard that freestyle needs hip rotation? Absolutely.", "hip rotation（转胯）"],
            ["通过转胯，手能划得更长。", "Rotating the hips lets your arm pull longer.", "pull longer（划得更长）"],
            ["每一次划水都推得更远，效率更高。", "Every stroke pushes farther—more efficient.", "efficient（高效）"]
         ]},
        {"id": "s2", "scene_zh": "减少水阻", "scene_en": "Less Water Resistance", "time": "00:11",
         "context": "第二，减少水阻：手前伸时转胯，身体拉得更长了，侧身前进，肩膀出水，更具流线型。转胯让身体在水中的投影面积变小。",
         "sentences": [
            ["手前伸时转胯，身体就拉得更长了。", "Rotate as your hand extends and the body lengthens.", "lengthen（拉长）"],
            ["侧身前进，肩膀出水，更具流线型。", "Swim sideways with the shoulder up—more streamlined.", "streamlined（流线型）"],
            ["身体变长变薄，水阻自然变小。", "A longer, thinner body cuts through with less drag.", "drag（水阻）"]
         ]},
        {"id": "s3", "scene_zh": "呼吸更轻松", "scene_en": "Easier Breathing", "time": "00:19",
         "context": "第三，呼吸更容易：胯转动带动头转动，头更容易转出水面呼吸。转胯是让头部自然滚转出水面，不需要费力抬头。",
         "sentences": [
            ["胯转带动头转，头更容易出水面。", "Hip rotation rolls the head out for a breath.", "roll out（滚转出水）"],
            ["不需要费力抬头，换气更轻松。", "No straining to lift—breathing gets easy.", "strain（费力）"]
         ]},
        {"id": "s4", "scene_zh": "转胯的要点", "scene_en": "The Key to Rotating", "time": "00:31",
         "context": "但转胯的要点可不是故意去扭你的胯。就像你够高东西、猴子摘桃，是不是就自然转胯了？这个时候利用身体的合力去推水，这胯不转都不行。所以自由泳转胯不是扭扭屁股就好，不要为了转胯而转胯。",
         "sentences": [
            ["转胯的要点不是故意去扭胯。", "The key is not deliberately twisting your hips.", "deliberately（刻意）"],
            ["像够高东西、猴子摘桃，自然就转胯了。", "Like reaching high to pick fruit—the hip turns on its own.", "reach high（够高）"],
            ["利用身体合力推水，胯不转都不行。", "Push with your whole body and rotation is automatic.", "whole-body push（全身发力）"],
            ["不要为了转胯而转胯。", "Never rotate just for the sake of rotating.", "for the sake of（为了…而）"]
         ]}
    ]
}

ARTICLES["mosike-dieyong-huanqi"] = {
    "title_zh": "莫斯科游泳教学：蝶泳手臂与换气问题",
    "title_en": "Moscow Swim Lesson: Butterfly Arms and Breathing",
    "duration": "1分11秒",
    "topic": "游泳 · 蝶泳",
    "scenes": [
        {"id": "s1", "scene_zh": "反面案例：错误的手臂与呼吸", "scene_en": "The Wrong Way: Arms and Breathing", "time": "00:01",
         "context": "开场展示反面案例：错误的手臂与呼吸，配俄语感叹词「ФУ!」（不行/糟糕）。教练指出常见的蝶泳错误示范。",
         "sentences": [
            ["开场是反面案例：错误的手臂与呼吸。", "The opening is a counter-example: wrong arms and breathing.", "counter-example（反面案例）"],
            ["配俄语感叹词「ФУ!」，表示不行、糟糕。", "It comes with the Russian exclamation “ФУ!”—no, ugh.", "exclamation（感叹词）"]
         ]},
        {"id": "s2", "scene_zh": "岸上模拟：推水发力", "scene_en": "On-Deck Drill: Pull Power", "time": "00:06",
         "context": "教练带学员做岸上模拟：推水发力练习。通过陆上动作感受蝶泳推水的发力方式，再带入水中。",
         "sentences": [
            ["先在岸上模拟，练习推水发力。", "First simulate on deck: the pulling-power drill.", "simulate（模拟）"],
            ["找到发力感，再带入水中。", "Find the power feel, then take it into the water.", "power feel（发力感）"]
         ]},
        {"id": "s3", "scene_zh": "换气瞬间：推水同步打腿", "scene_en": "The Breath Moment: Sync Kick With Pull", "time": "00:15",
         "context": "水中实拍换气瞬间，字幕提示「注意推水同步打腿」。蝶泳换气要配合推水和打腿的节奏，形成整体动作。",
         "sentences": [
            ["换气瞬间要同步打腿。", "At the breath, sync the kick with the pull.", "sync（同步）"],
            ["推水和打腿形成整体节奏。", "The pull and kick become one rhythm.", "rhythm（节奏）"]
         ]},
        {"id": "s4", "scene_zh": "正确换气姿态", "scene_en": "Correct Breathing Posture", "time": "00:27",
         "context": "岸上模拟正确换气姿态，字幕「推水换气保持颈肩背在一条线上」。换气时身体要像钢板一样整体转动，而不是抬头。",
         "sentences": [
            ["推水换气时，颈肩背保持一条线。", "During the pull and breath, keep neck, shoulders and back in one line.", "in one line（一条线）"],
            ["像钢板一样整体转动，不要抬头。", "Rotate as one plank—never lift the chin.", "plank（钢板）"]
         ]},
        {"id": "s5", "scene_zh": "发力技巧：数字「3」", "scene_en": "Power Trick: The “3”", "time": "00:36",
         "context": "岸上模拟发力技巧，教练比出数字「3」，强调推水发力的时机与力度，让换气前的最后一推更有力。",
         "sentences": [
            ["教练比出数字「3」，强调发力时机。", "The coach holds up “3” to cue the power timing.", "cue（提示）"],
            ["最后一推要有力，帮助身体出水。", "The final push must be strong to lift the body out.", "lift out（带出水面）"]
         ]},
        {"id": "s6", "scene_zh": "保持身体平直推进", "scene_en": "Stay Flat and Drive Forward", "time": "00:46",
         "context": "水中实拍叠加岸上示范，字幕「保持身体平直向前推进」。身体不要上下起伏太大，保持平直向前。",
         "sentences": [
            ["保持身体平直，向前推进。", "Keep the body flat and drive forward.", "drive forward（向前推进）"],
            ["减少上下起伏，保存体力。", "Less bobbing saves your energy.", "bob（起伏）"]
         ]},
        {"id": "s7", "scene_zh": "移臂方式：数字「4」", "scene_en": "Recovery Style: The “4”", "time": "00:51",
         "context": "岸上模拟移臂方式，教练比出数字「4」，强调移臂要屈肘、低平，避免甩臂过直造成肩部疲劳。",
         "sentences": [
            ["移臂方式也有讲究，比出数字「4」。", "Even the recovery has a cue—the “4”.", "recovery（移臂）"],
            ["屈肘低平移臂，避免肩部疲劳。", "Bend the elbow and stay low to spare your shoulders.", "spare（省着用）"]
         ]},
        {"id": "s8", "scene_zh": "屈肘移臂更有利", "scene_en": "Bent Elbow Wins the Recovery", "time": "00:57",
         "context": "字幕「肘部弯曲更有利移臂」。屈肘移臂让手更贴近水面滑行，减小空气阻力与肩膀负担，是蝶泳高效移臂的关键。",
         "sentences": [
            ["肘部弯曲更有利于移臂。", "Bending the elbow helps the recovery.", "bent elbow（屈肘）"],
            ["手贴近水面滑行，肩部负担更小。", "Sliding low keeps the load off your shoulder.", "shoulder load（肩部负担）"]
         ]}
    ]
}

ARTICLES["youyong-zhuanshen-duibi"] = {
    "title_zh": "自由泳转身对比：错误 vs 正确",
    "title_en": "Freestyle Flip Turn: Wrong vs Right",
    "duration": "8秒",
    "topic": "游泳 · 转身",
    "scenes": [
        {"id": "s1", "scene_zh": "分屏定调", "scene_en": "Split Screen Setup", "time": "00:00",
         "context": "分屏对比：上格红叉（问题动作）、下格绿勾（正确示范），两位泳者同步冲向池壁。错误组团身偏松，正确组团身紧凑。",
         "sentences": [
            ["上格红叉是问题动作，下格绿勾是正确示范。", "Top: red cross for the flawed turn; bottom: green check for the model.", "flawed（有缺陷的）"],
            ["两位泳者同步冲向池壁。", "Both swimmers sprint toward the wall in sync.", "in sync（同步）"]
         ]},
        {"id": "s2", "scene_zh": "冲刺阶段：差异未显", "scene_en": "Sprint Phase: No Gap Yet", "time": "00:01",
         "context": "冲刺阶段两组动作同步性很高，差异尚未显现。这时候还看不出对错，关键在于团身阶段。",
         "sentences": [
            ["冲刺阶段，两组动作高度同步。", "In the sprint phase, both groups move in sync.", "sprint（冲刺）"],
            ["差异还没显现，关键在团身。", "No gap yet—the tuck decides everything.", "tuck（团身）"]
         ]},
        {"id": "s3", "scene_zh": "团身瞬间：松 vs 紧", "scene_en": "The Tuck: Loose vs Tight", "time": "00:03",
         "context": "团身瞬间：上格更立、更松、离墙更远；下格更贴、更紧凑。正确做法是膝盖收向胸口、全身缩成一团，越紧凑滚翻越快。",
         "sentences": [
            ["上格更立更松、离墙更远。", "The top is more upright, looser and farther from the wall.", "upright（竖直）"],
            ["下格更贴、更紧凑。", "The bottom hugs closer and tighter.", "compact（紧凑）"],
            ["团身越紧，滚翻越快。", "A tighter tuck spins you faster.", "spin（滚翻）"]
         ]},
        {"id": "s4", "scene_zh": "翻滚中段：保持紧凑", "scene_en": "Mid-Flip: Stay Compact", "time": "00:04",
         "context": "翻滚中段：上格团身持续偏松，下格持续保持紧凑。松散的团身会让身体在滚翻中展开，损失角速度。",
         "sentences": [
            ["上格持续偏松，滚翻变慢。", "The loose tuck keeps the flip slow.", "loose tuck（松散团身）"],
            ["下格全程紧凑，速度不掉。", "The bottom stays compact and fast throughout.", "throughout（全程）"]
         ]},
        {"id": "s5", "scene_zh": "蹬壁对比", "scene_en": "The Push-Off", "time": "00:06",
         "context": "蹬壁对比：上格蹬得更早、离墙更远；下格贴墙更久才出发。正确做法是等双脚贴稳墙再发力，蹬得更远更扎实。",
         "sentences": [
            ["上格蹬得早、离墙远，力量浪费。", "The top pushes early and far from the wall—wasted power.", "wasted（浪费的）"],
            ["下格贴墙更久，蹬得更扎实。", "The bottom hugs the wall longer for a solid push.", "solid push（扎实蹬壁）"]
         ]}
    ]
}

ARTICLES["chigun-zhuanjian-lianxi"] = {
    "title_zh": "仰泳·自由泳陆上持棍转肩练习",
    "title_en": "On-Land Shoulder Rotation Drill With a Pole",
    "duration": "9秒",
    "topic": "游泳 · 陆上训练",
    "scenes": [
        {"id": "s1", "scene_zh": "开场分屏", "scene_en": "Split Screen Opening", "time": "00:00",
         "context": "开场分屏：上格仰泳持棍高举，下格自由泳持棍前伸。用一根棍在陆上模拟水中划臂轨迹，强化转肩与移臂路径。",
         "sentences": [
            ["上格仰泳持棍高举，下格自由泳持棍前伸。", "Top: pole raised for backstroke. Bottom: pole extended for freestyle.", "backstroke（仰泳）"],
            ["陆上持棍，模拟水中划臂轨迹。", "On land, the pole maps your underwater arm path.", "map（模拟）"]
         ]},
        {"id": "s2", "scene_zh": "仰泳过程帧：棍身一字", "scene_en": "Backstroke Mid-Frame: Pole Flat", "time": "00:04",
         "context": "仰泳组过程帧：棍身放平呈「一字」，途经肩线中段。仰泳转肩时棍要贴近肩线水平移动。",
         "sentences": [
            ["棍身放平呈一字，途经肩线中段。", "The pole lies flat, passing the mid-shoulder line.", "shoulder line（肩线）"],
            ["仰泳转肩，棍贴近肩线水平移动。", "Backstroke rotation keeps the pole level at the shoulder.", "level（水平）"]
         ]},
        {"id": "s3", "scene_zh": "仰泳顶点帧：高举贴墙", "scene_en": "Backstroke Apex: High Against the Wall", "time": "00:07",
         "context": "仰泳组顶点帧：棍端高举贴墙，弧线回到起始位置，准备下一次循环。完成一个完整的高举移臂回环。",
         "sentences": [
            ["棍端高举贴墙，再弧线回到起点。", "The pole's end reaches up against the wall, then arcs back.", "arc（弧线）"],
            ["完成一次完整的移臂回环。", "One full recovery loop complete.", "loop（回环）"]
         ]},
        {"id": "s4", "scene_zh": "自由泳过程帧：前伸下探", "scene_en": "Freestyle Mid-Frame: Reach Down", "time": "00:01",
         "context": "自由泳组过程帧：俯身前倾，棍身前伸下探，模拟入水抓水。自由泳强调前伸和抓水，转肩带动棍前探。",
         "sentences": [
            ["俯身前倾，棍身前伸下探。", "Lean forward, the pole reaching down.", "reach down（下探）"],
            ["模拟入水后的抓水动作。", "This mimics the entry and catch.", "catch（抓水）"]
         ]},
        {"id": "s5", "scene_zh": "自由泳过程帧：高肘移臂", "scene_en": "Freestyle Mid-Frame: High Elbow", "time": "00:06",
         "context": "自由泳组过程帧：棍身后摆、肘部抬高，模拟高肘出水与移臂。高肘移臂减少肩部压力、保持流线。",
         "sentences": [
            ["棍身后摆、肘部抬高。", "The pole sweeps back with the elbow raised.", "sweep（摆动）"],
            ["模拟高肘出水与移臂。", "This simulates the high-elbow exit and recovery.", "high-elbow（高肘）"]
         ]},
        {"id": "s6", "scene_zh": "循环闭合", "scene_en": "Both Loops Close", "time": "00:08",
         "context": "循环末尾：上格再次高举回到起点，下格同步上摆过肩，两条弧线各自闭环。仰泳与自由泳的转肩练习循环完成。",
         "sentences": [
            ["上格高举回起点，下格上摆过肩。", "Top raises back to start; bottom swings past the shoulder.", "swing past（摆过）"],
            ["两条弧线各自闭环，循环完成。", "Each arc closes its own loop.", "close the loop（闭环）"]
         ]}
    ]
}

ARTICLES["qimeng-jibengong-shangxian"] = {
    "title_zh": "启蒙和基本功才能决定上限",
    "title_en": "Fundamentals Set Your Ceiling",
    "duration": "2分34秒",
    "topic": "游泳 · 打腿",
    "scenes": [
        {"id": "s1", "scene_zh": "鞭状腿：上下但不是抬腿", "scene_en": "Whip Kick: Up-Down, Not Lifting", "time": "00:00",
         "context": "这条视频是针对之前鞭状腿复位视频的宝宝的延展。第一点，鞭状腿的自由泳虽然也是上下上下，但是是没有所谓的抬腿的动作。即便自由泳腿的主体方向是上下上下，但不是抬腿，更不是直抬腿。",
         "sentences": [
            ["鞭状腿自由泳虽然也是上下上下。", "Whip-kick freestyle still goes up-down, up-down.", "whip kick（鞭状腿）"],
            ["但是没有所谓的抬腿动作。", "But there's no such thing as a lift.", "lift（抬腿）"],
            ["不是抬腿，更不是直抬腿。", "Not lifting—and definitely not straight-leg lifting.", "straight-leg（直腿）"]
         ]},
        {"id": "s2", "scene_zh": "直抬腿=直棍腿道", "scene_en": "Straight Lifts Become “Straight-Stick” Kicking", "time": "00:20",
         "context": "直抬腿直上直下，那就是直棍腿道。教练指出这主要是商业产物，是某些速成班的训练方式。想学自由泳并成为游泳爱好者，想游得舒展，速成班几乎不可能，因为自由泳需要量的堆积。",
         "sentences": [
            ["直抬腿直上直下，就是直棍腿道。", "Straight up-down lifts are “straight-stick” kicking.", "straight-stick（直棍）"],
            ["这主要是商业产物，速成班的套路。", "It's mostly a commercial product—a crash-course gimmick.", "commercial product（商业产物）"],
            ["想游得舒展，速成班几乎不可能。", "Swimming relaxed? A crash course almost never delivers.", "crash course（速成班）"],
            ["自由泳需要量的堆积。", "Freestyle demands accumulated volume.", "volume（量）"]
         ]},
        {"id": "s3", "scene_zh": "自由泳腿不在陆上练", "scene_en": "Freestyle Kicking Isn't Learned on Land", "time": "00:34",
         "context": "自由泳腿本身就没有在陆地上练的，只有会的人才能做出来。在陆地上做出来自由泳打腿的人，都是已经会打自由泳腿的人。",
         "sentences": [
            ["自由泳腿没有在陆地上练的。", "Freestyle kicking isn't practiced on land.", "on land（陆上）"],
            ["只有会的人才能做出来。", "Only those who can swim it can demonstrate it.", "demonstrate（演示）"]
         ]},
        {"id": "s4", "scene_zh": "发力方式不同，无法过渡", "scene_en": "Different Mechanics: No Transition", "time": "00:57",
         "context": "从直棍腿过渡到鞭状腿完全是瞎扯淡。发力方式不同，怎么过渡？鞭状腿没有抬腿，抬腿是要屁股往上；鞭状腿是小腹肌肉展开，这个动作就是打腿动作。",
         "sentences": [
            ["从直棍腿过渡到鞭状腿是瞎扯。", "Transitioning from straight-stick to whip kick is nonsense.", "nonsense（瞎扯）"],
            ["两者发力方式完全不同。", "The two use completely different mechanics.", "mechanics（发力机制）"],
            ["鞭状腿没有抬腿，是展开小腹发力。", "The whip kick expands the lower abs—that's the kick.", "expand（展开）"]
         ]},
        {"id": "s5", "scene_zh": "打腿看起来轻松，练起来不轻松", "scene_en": "Looks Easy, Feels Hard", "time": "01:36",
         "context": "自用打腿看起来很轻松，你练的时候一点也不轻松，这个是要量则时间的积累。所谓轻松打自用腿，那是展现出来的发力方式轻松，但是从不会到会是需要一个过程的。",
         "sentences": [
            ["打腿看起来轻松，练起来一点也不轻松。", "It looks easy but training it is anything but.", "anything but（一点都不）"],
            ["需要量的积累和时间的沉淀。", "It takes volume and time to build.", "build（积累）"],
            ["从不会到会，需要一个过程。", "From unable to able is a process.", "process（过程）"]
         ]},
        {"id": "s6", "scene_zh": "鞭状腿才能起频率", "scene_en": "Only Whip Kicks Reach High Tempo", "time": "02:08",
         "context": "鞭状腿才能起频率。直棍腿害了多少成年业余爱好者和游泳队的孩子。鞭状腿能起频率，全程没有快进，直棍腿整条腿往上抬很累。",
         "sentences": [
            ["只有鞭状腿才能起频率。", "Only the whip kick can hit high tempo.", "tempo（频率）"],
            ["直棍腿害了多少游泳爱好者。", "Straight-stick kicking has hurt countless swimmers.", "countless（无数的）"],
            ["直棍腿整条腿往上抬，很累。", "Lifting the whole leg up-down is exhausting.", "exhausting（累人的）"]
         ]}
    ]
}

ARTICLES["hexin-shoujin-fangfa"] = {
    "title_zh": "核心收紧不是吸肚子！3个正确收紧核心方法",
    "title_en": "Brace Your Core, Don't Suck In—3 Methods",
    "duration": "1分45秒",
    "topic": "运动 · 核心训练",
    "scenes": [
        {"id": "s1", "scene_zh": "核心肌群包括什么", "scene_en": "What the Core Includes", "time": "00:13",
         "context": "先明确什么是核心肌群。很多宝子以为肚子就是一个核心，不对，它只是核心的一部分。核心肌群包括腹部、背部以及骨盆。这些核心肌群收紧之后就会如铜墙铁壁般，在运动的时候防止受伤，并且保持好的体型体态。",
         "sentences": [
            ["核心肌群不只是肚子。", "The core is more than your belly.", "core（核心）"],
            ["它包括腹部、背部以及骨盆。", "It includes the abs, back and pelvis.", "pelvis（骨盆）"],
            ["收紧后如铜墙铁壁，防止受伤。", "Bracing turns it into an iron wall against injury.", "brace（收紧）"]
         ]},
        {"id": "s2", "scene_zh": "核心收紧 vs 吸肚子", "scene_en": "Bracing vs Sucking In", "time": "00:32",
         "context": "要搞清楚核心收紧和吸肚子的区别。吸肚子是吸气，肚子瘪下去，但是全是软的；而核心收紧是像被击打一样一锤一圈，是可以抵挡住的。这就是为什么运动的时候要收紧核心。",
         "sentences": [
            ["吸肚子是吸气，肚子瘪下去但全软。", "Sucking in deflates the belly but stays soft.", "suck in（吸肚子）"],
            ["核心收紧像一锤一圈，能抵挡住。", "Bracing can take a punch—it holds.", "take a punch（扛住一拳）"],
            ["这就是运动时收紧核心的原因。", "That's why you brace during exercise.", "brace（绷紧）"]
         ]},
        {"id": "s3", "scene_zh": "保护脊柱与腰椎", "scene_en": "Protecting the Spine", "time": "00:54",
         "context": "这些肌群一起发力的状态，可以保护我们的脊柱、腰椎以及其他各个关节，避免运动受伤。核心是身体的力量传导中枢。",
         "sentences": [
            ["肌群一起发力，保护脊柱和腰椎。", "Firing together, they shield the spine and lower back.", "shield（保护）"],
            ["避免各个关节运动受伤。", "They prevent joint injuries during sport.", "joint（关节）"]
         ]},
        {"id": "s4", "scene_zh": "技巧一：上大号", "scene_en": "Trick 1: The Bathroom Grunt", "time": "01:08",
         "context": "第一个技巧：上大号。已经在拉屎有点干，出来往外站住。你看，收紧了。这个生活场景天然会让你启动腹部深层肌群。",
         "sentences": [
            ["上大号时会自然收紧核心。", "Straining on the toilet naturally braces your core.", "strain（用力）"],
            ["你看，这就是收紧了。", "See? That's a braced core.", "braced（收紧的）"]
         ]},
        {"id": "s5", "scene_zh": "技巧二：吹蜡烛", "scene_en": "Trick 2: Blow Out the Candle", "time": "00:18",
         "context": "第二个技巧：过生日的时候咱们都得吹蜡烛。感受一下，又收紧了。吹蜡烛的呼气方式会启动腹横肌，让腰腹一圈都收紧。",
         "sentences": [
            ["过生日吹蜡烛，感受一下。", "Birthday candles—feel it.", "candle（蜡烛）"],
            ["吹蜡烛的呼气，自然收紧腰腹。", "Blowing engages the transverse abs and tightens the waist.", "transverse abs（腹横肌）"]
         ]},
        {"id": "s6", "scene_zh": "技巧三：笑出腹肌", "scene_en": "Trick 3: Laugh Your Abs Out", "time": "00:25",
         "context": "第三招：笑出腹肌。哈哈哈，感受一下，特别紧。这个招真有用，笑出腹肌那是真的。大声笑的腹压与核心收紧的腹压机制一致。",
         "sentences": [
            ["大笑时，肚子特别紧。", "Laughing hard makes the belly feel tight.", "tight（紧）"],
            ["笑出腹肌是真的，这招真有用。", "Laughing your abs out is real—it works.", "work（有效）"],
            ["大声笑的腹压，和核心收紧机制一致。", "Laughing builds the same intra-abdominal pressure.", "intra-abdominal pressure（腹压）"]
         ]}
    ]
}

ARTICLES["dieyong-huashou-jiaoxue"] = {
    "title_zh": "蝶泳划手教学",
    "title_en": "Butterfly Pull Lesson",
    "duration": "16秒",
    "topic": "游泳 · 蝶泳",
    "scenes": [
        {"id": "s1", "scene_zh": "流线型前伸", "scene_en": "Streamlined Extension", "time": "00:00",
         "context": "开场：流线型前伸 + 标题「蝶泳划手教学」。双手前伸呈流线型，身体拉平，准备开始划手动作。",
         "sentences": [
            ["开场先做好流线型前伸。", "Open with a streamlined forward extension.", "streamlined（流线型）"],
            ["双手前伸，身体拉平。", "Arms stretched forward, body flat.", "stretch（前伸）"]
         ]},
        {"id": "s2", "scene_zh": "划手四段：划手→抱水→推水→小拇指出水", "scene_en": "Four Phases: Reach, Catch, Pull, Pinky-Out", "time": "00:02",
         "context": "四段标签齐出：划手 → 抱水 → 推水 → 小拇指出水。蝶泳划水路径的完整四步，每一步都要做到位。",
         "sentences": [
            ["蝶泳划手分四段：划手、抱水、推水、小拇指出水。", "The butterfly pull has four phases: reach, catch, pull, pinky-first exit.", "phase（阶段）"],
            ["四步连贯，划水路径完整。", "Four steps make a complete pull path.", "complete path（完整路径）"]
         ]},
        {"id": "s3", "scene_zh": "推水末端：小拇指出水", "scene_en": "End of the Pull: Pinky Exits", "time": "00:03",
         "context": "推水末端：小拇指侧出水，准备移臂。推水最后阶段向侧后推，小拇指先出水面，顺势移臂向前。",
         "sentences": [
            ["推水末端，小拇指侧出水。", "At the end of the pull, the pinky side exits the water.", "pinky side（小拇指侧）"],
            ["出水后顺势准备移臂。", "Exit, then flow into the recovery.", "flow into（顺势进入）"]
         ]},
        {"id": "s4", "scene_zh": "入水关键：大拇指先入水", "scene_en": "Entry Key: Thumbs First", "time": "00:05",
         "context": "入水关键点：大拇指先入水，双手重回前伸。移臂回前时大拇指领先切入水中，双手重新回到前伸的流线型。",
         "sentences": [
            ["入水时大拇指先入水。", "Enter the water thumbs first.", "thumbs first（拇指先入）"],
            ["双手重回前伸，回到流线型。", "Hands return to the full forward extension.", "return（回到）"]
         ]},
        {"id": "s5", "scene_zh": "身体提示：压胸提臀", "scene_en": "Body Cue: Chest Down, Hips Up", "time": "00:06",
         "context": "身体提示：压胸（下）+ 提臀（上）配合手部推进。蝶泳不是光靠手臂，身体波浪配合压胸提臀，让推进更高效。",
         "sentences": [
            ["压胸向下，配合手部推进。", "Press the chest down to drive the pull.", "press down（下压）"],
            ["提臀向上，形成身体波浪。", "Lift the hips up for the body wave.", "body wave（身体波浪）"],
            ["手和身体配合，推进更高效。", "Hands and body together make the drive efficient.", "drive（推进）"]
         ]},
        {"id": "s6", "scene_zh": "路径复述", "scene_en": "Path Restated", "time": "00:08",
         "context": "路径复述：同一套黄字标签再次对齐虚线轨迹。反复确认划水路径，让肌肉记住正确的轨迹。",
         "sentences": [
            ["黄字标签再次对齐虚线轨迹。", "The same yellow labels align with the dashed trajectory.", "trajectory（轨迹）"],
            ["反复确认，让肌肉记住路径。", "Repeat to burn the path into muscle memory.", "muscle memory（肌肉记忆）"]
         ]},
        {"id": "s7", "scene_zh": "恢复阶段：指向拇指入水", "scene_en": "Recovery: Aim for the Thumb Entry", "time": "00:11",
         "context": "恢复阶段：移臂轨迹指向大拇指入水。空中移臂要低平放松，轨迹终点明确指向下一次的大拇指入水点。",
         "sentences": [
            ["移臂轨迹指向大拇指入水点。", "The recovery path aims at the thumb entry point.", "aim（指向）"],
            ["空中移臂低平放松。", "Keep the aerial recovery low and relaxed.", "aerial recovery（空中移臂）"]
         ]},
        {"id": "s8", "scene_zh": "收尾：身体与划手同拍", "scene_en": "Wrap-Up: Body and Pull in Time", "time": "00:12",
         "context": "收尾再强调身体：压胸 + 提臀与划手同拍。身体波浪和手臂划水必须严格同拍，这是蝶泳节奏的核心。",
         "sentences": [
            ["压胸提臀要和划手同拍。", "Chest press and hip lift must sync with the pull.", "in time（同拍）"],
            ["节奏对了，蝶泳才顺。", "The right rhythm makes the butterfly flow.", "flow（顺畅）"]
         ]}
    ]
}

ARTICLES["dietui-jiebie-juepigu"] = {
    "title_zh": "新手轻松解锁蝶腿，告别“撅屁股”",
    "title_en": "Unlock the Dolphin Kick Without the “Butt-Up”",
    "duration": "1分03秒",
    "topic": "游泳 · 蝶泳",
    "scenes": [
        {"id": "s1", "scene_zh": "误区：蝶腿=撅屁股", "scene_en": "The Myth: Dolphin Kick = Butt-Up", "time": "00:00",
         "context": "很多姐妹练出发蝶腿，总容易陷入一个误区，以为蝶腿就是撅屁股。结果练出来动作又僵又不雅，速度也提不上来。上次教出发蝶腿，就发现全程靠下半身硬甩，上半身完全不动，这样可不行。",
         "sentences": [
            ["以为蝶腿就是撅屁股，是个误区。", "Thinking the dolphin kick is a butt-up is a myth.", "myth（误区）"],
            ["结果动作又僵又不雅，速度也上不去。", "The result is stiff, ugly and slow.", "stiff（僵硬的）"],
            ["靠下半身硬甩、上半身不动，不行。", "Hard-throwing the legs with a frozen torso won't do.", "frozen torso（僵住的上半身）"]
         ]},
        {"id": "s2", "scene_zh": "关键：全身波动的发力", "scene_en": "The Key: Whole-Body Wave", "time": "00:16",
         "context": "想让蝶腿又好看又快，关键在于全身配合的波动感。记住，手不是摆设，它负责导向：不管是向上调整，还是向下前游，都要靠手来辅助控制方向。",
         "sentences": [
            ["关键在于全身配合的波动感。", "The key is a coordinated whole-body wave.", "whole-body wave（全身波动）"],
            ["手不是摆设，它负责导向。", "The hands aren't decoration—they steer.", "steer（导向）"],
            ["向上调整、向下前游，都靠手辅助控方向。", "Rising or diving forward, the hands guide you.", "guide（引导）"]
         ]},
        {"id": "s3", "scene_zh": "发力顺序：胸→肚子→甩腿", "scene_en": "The Order: Chest, Belly, Then Kick", "time": "00:27",
         "context": "真正的发力顺序很简单：首先从肩胸开始，主动把胸往前顶出去；胸顶完之后再顺势顶肚子；最后一步才是自然的甩腿。",
         "sentences": [
            ["从肩胸开始，主动把胸往前顶。", "Start at the chest and push it forward actively.", "push forward（前顶）"],
            ["顶完胸，再顺势顶肚子。", "After the chest, follow through with the belly.", "follow through（顺势）"],
            ["最后一步才是自然甩腿。", "The natural leg flick comes last.", "leg flick（甩腿）"]
         ]},
        {"id": "s4", "scene_zh": "节奏：顶胸-顶肚-甩腿循环", "scene_en": "The Cycle: Chest-Belly-Kick", "time": "00:39",
         "context": "腿打完之后立刻衔接下一轮，重复顶胸、顶屁股甩腿的节奏。这里我需要出水向上，如果前游就保持垂直向前就好。",
         "sentences": [
            ["腿打完立刻衔接下一轮。", "Finish the kick and flow straight into the next round.", "flow into（衔接）"],
            ["重复顶胸、顶肚、甩腿的节奏。", "Repeat chest, belly, kick.", "repeat（重复）"],
            ["出水向上，或前游保持垂直向前。", "Rise up, or dive forward staying perpendicular.", "perpendicular（垂直）"]
         ]},
        {"id": "s5", "scene_zh": "告别撅屁股", "scene_en": "Say Goodbye to the Butt-Up", "time": "00:47",
         "context": "千万别再只靠屁股用力上下甩腿了，这样上半身会一直僵着，完全没有美感。只要解锁了这种全身波动的蝶腿技巧，下次水下拍摄你也能轻松拍出美美的美人鱼视频，动作又丝滑又出片。",
         "sentences": [
            ["别只靠屁股上下甩腿，上半身会僵。", "Stop kicking from the hips alone—the torso stiffens.", "stiffen（变僵）"],
            ["解锁全身波动，动作又丝滑又出片。", "Unlock the whole-body wave for silky, photogenic moves.", "silky（丝滑的）"],
            ["下次水下拍摄，你也能拍出美人鱼视频。", "Next underwater shoot, you'll nail the mermaid video.", "mermaid video（美人鱼视频）"]
         ]}
    ]
}

ARTICLES["ziyouyong-datui-zoushui"] = {
    "title_zh": "自由泳打腿走水的原理",
    "title_en": "The Physics of Freestyle Kicking",
    "duration": "53秒",
    "topic": "游泳 · 打腿",
    "scenes": [
        {"id": "s1", "scene_zh": "错误示范：垂直切水", "scene_en": "The Wrong Way: Vertical Cutting", "time": "00:00",
         "context": "自由泳打腿什么时候失效？黄色模型（错误）：脚尖向下，垂直切过水面。这会阻碍向后的推进力，还制造阻力。",
         "sentences": [
            ["黄色模型中，脚尖向下垂直切水。", "In the yellow model, the toes point down and cut through vertically.", "cut through（切过）"],
            ["这会阻碍推进并制造阻力。", "This blocks backward thrust and creates drag.", "thrust（推进力）"],
            ["打腿失效，游得又慢又累。", "The kick fails—slow and tiring.", "fail（失效）"]
         ]},
        {"id": "s2", "scene_zh": "正确示范：脚面引导水流", "scene_en": "The Right Way: Guide the Water", "time": "00:08",
         "context": "绿色模型（正确）：用脚背向下推水、脚底向上推水，有效引导水流。让脚有效引导水的流动，把水推向身后。",
         "sentences": [
            ["用脚背向下推水、脚底向上推水。", "Use the instep to push down and the sole to push up.", "instep（脚背）"],
            ["脚有效引导水流，产生推进。", "The feet guide the flow and generate propulsion.", "propulsion（推进）"]
         ]},
        {"id": "s3", "scene_zh": "收膝盖的坏处", "scene_en": "Why Pulling Knees Up Hurts", "time": "00:17",
         "context": "把膝盖向胸口收，不仅制造阻力，还可能产生错误方向的推力。收膝打腿等于把自己向后推。",
         "sentences": [
            ["收膝盖向胸，制造阻力。", "Pulling the knees to the chest creates drag.", "drag（阻力）"],
            ["还可能产生错误方向的推力。", "It can even push you the wrong way.", "wrong way（错误方向）"]
         ]},
        {"id": "s4", "scene_zh": "脚底垂直刺水", "scene_en": "Sole-First Stabbing", "time": "00:22",
         "context": "用脚底强踢、垂直刺穿水面，无法产生有效推进。错误的击水角度让力量浪费在上下方向，而不是向后。",
         "sentences": [
            ["脚底强踢垂直刺水。", "Strong kicks with the sole pierce the water abruptly.", "pierce（刺穿）"],
            ["力量浪费在上下，无法有效推进。", "Power wasted up-down—no real propulsion.", "wasted（浪费）"]
         ]},
        {"id": "s5", "scene_zh": "微弯膝引导水流", "scene_en": "Soft Knees Guide the Flow", "time": "00:27",
         "context": "绿色模型微弯膝盖控制方向，水从膝盖到脚趾逐渐引导，然后向后推。鞭状的柔和弯曲让水沿着腿逐渐加速向后。",
         "sentences": [
            ["微弯膝盖，控制打腿方向。", "Slightly bend the knees to control the kick's direction.", "slightly bend（微弯）"],
            ["水从膝盖到脚趾逐渐引导，再向后推。", "Water is guided from knee to toes, then pushed back.", "guide（引导）"]
         ]},
        {"id": "s6", "scene_zh": "僵硬 vs 放松", "scene_en": "Stiff vs Relaxed", "time": "00:34",
         "context": "错误技术中膝踝僵硬，没有振荡，因此没有向后的推力，手臂扫水但腿只是下压放松。绿色模型中膝踝放松，腿像旗帜飘动般波浪运动，沿整条腿产生推力。",
         "sentences": [
            ["膝踝僵硬，没有振荡就没有推力。", "Stiff knees and ankles mean no oscillation and no thrust.", "oscillation（振荡）"],
            ["绿色模型膝踝放松，腿像旗帜飘动。", "Relaxed joints make the leg wave like a flag.", "flag（旗帜）"],
            ["沿整条腿产生推力。", "Thrust builds along the entire leg.", "entire leg（整条腿）"]
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
        words = words + ["stroke", "rotation", "streamline", "breathe", "glide", "rhythm", "kick", "shoulder", "posture", "balance"][: 20 - len(words)]

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
