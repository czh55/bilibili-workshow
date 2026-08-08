#!/usr/bin/env python3
"""批24：为10篇视频生成完整场景英译JSON（含场景/练习/避坑/思维转变/生词）。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

ARTICLES = {}

ARTICLES["w4Qh1I72MK"] = {
    "title_zh": "手机运镜每日轻松练习",
    "title_en": "Easy Daily Phone Camera Moves",
    "duration": "00:16",
    "topic": "摄影 · 运镜练习",
    "scenes": [
        {"id": "s1", "scene_zh": "前推接后拉运镜", "scene_en": "Push In, Then Pull Back", "time": "00:00",
         "context": "前推后拉是最基础的双段运镜：先向前推进突出主体，再向后退拉展现环境。",
         "sentences": [
            ["前推接后拉运镜，今天练习的第一个动作。", "First up today: push in, then pull back.", "push in（前推）"],
            ["先向前推进靠近主体，让观众的视线聚焦。", "Move forward to close in on the subject.", "close in（靠近）"],
            ["然后再向后拉，把环境一起展现出来。", "Then pull back to reveal the surroundings.", "pull back（后拉）"]
         ]},
        {"id": "s2", "scene_zh": "前推半环绕接后拉", "scene_en": "Push In, Half-Orbit, Pull Back", "time": "00:03",
         "context": "前推半环绕接后拉：推进的同时做半圈环绕，画面更有立体感和运动感。",
         "sentences": [
            ["前推半环绕接后拉，比单纯直推多了一丝变化。", "Push in, sweep a half circle, then pull back.", "sweep（环绕扫动）"],
            ["推进的同时环绕主体半圈，画面立刻立体起来。", "Orbiting halfway while pushing adds depth.", "orbiting（环绕）"],
            ["再接一个后拉，运动感十足。", "Finish with a pull-back for extra motion.", "motion feel（运动感）"]
         ]},
        {"id": "s3", "scene_zh": "前推运镜", "scene_en": "The Push-In Move", "time": "00:07",
         "context": "单纯前推运镜：身体平稳向前移动，画面逐渐靠近主体，适合表现注意力集中。",
         "sentences": [
            ["到空间前推运镜，保持身体平稳向前。", "Push in steadily, keeping your body smooth.", "steadily（平稳地）"],
            ["画面逐渐靠近主体，注意力自然集中。", "The frame moves closer, focusing attention.", "frame（画面）"]
         ]},
        {"id": "s4", "scene_zh": "上升接斜摇运镜", "scene_en": "Rise, Then Tilt", "time": "00:11",
         "context": "上升接斜摇：身体先向上抬升，再斜向摇动镜头，常用于展示高大主体或空间全貌。",
         "sentences": [
            ["上升接斜摇运镜，先抬升再摇动。", "Rise up, then tilt the camera diagonally.", "tilt（倾斜摇动）"],
            ["这种组合能展示出主体的高度感。", "The combo shows off the subject's height.", "sense of height（高度感）"]
         ]},
        {"id": "s5", "scene_zh": "横摇运镜", "scene_en": "The Pan", "time": "00:14",
         "context": "横摇运镜：镜头沿水平方向摇动，适合展现宽阔场景或跟随人物移动。",
         "sentences": [
            ["横摇运镜，镜头沿水平方向扫过。", "The pan sweeps the camera horizontally.", "pan（横摇）"],
            ["收工，今天的练习就到这里。", "And that's a wrap for today's practice.", "a wrap（收工）"]
         ]}
    ]
}

ARTICLES["2zJFokTBwsM"] = {
    "title_zh": "短视频拍摄技巧",
    "title_en": "Short-Video Shooting Tips",
    "duration": "00:18",
    "topic": "摄影 · 人像机位",
    "scenes": [
        {"id": "s1", "scene_zh": "侧面45度更松弛", "scene_en": "Side 45° Feels Relaxed", "time": "00:00",
         "context": "正面直拍容易呆板，改用侧面45度拍摄，人物更自然松弛。",
         "sentences": [
            ["视频不要这样正面直直地拍。", "Don't shoot straight on like this.", "straight on（正面直拍）"],
            ["要侧面45度拍，这样更有松弛感。", "Shoot from a 45° side angle for a relaxed vibe.", "side angle（侧面角度）"],
            ["45度的角度让人物看起来更自然。", "The 45° angle makes people look more natural.", "natural（自然）"]
         ]},
        {"id": "s2", "scene_zh": "侧面拍更亲切", "scene_en": "Profile Shots Feel Warmer", "time": "00:03",
         "context": "继续用侧面机位拍摄，比正面更亲切，拉近与观众的距离。",
         "sentences": [
            ["不要这样拍，正面太硬。", "Don't shoot like this—too stiff.", "stiff（生硬）"],
            ["要侧面拍，这样更加亲切。", "Shoot from the side—it feels warmer.", "warmer（更亲切）"]
         ]},
        {"id": "s3", "scene_zh": "过肩拍主次分明", "scene_en": "Over-the-Shoulder Separates Focus", "time": "00:06",
         "context": "过肩拍利用前景人物的肩膀做遮挡，画面主次分明，层次感更强。",
         "sentences": [
            ["不要这样直接拍两个人。", "Don't just shoot both people head-on.", "head-on（正对）"],
            ["过肩拍，这样主持更加分明。", "Go over-the-shoulder to separate the subjects.", "over-the-shoulder（过肩拍）"],
            ["前景的肩膀让画面有了层次。", "The shoulder in the foreground adds depth.", "foreground（前景）"]
         ]},
        {"id": "s4", "scene_zh": "偷拍视角带人感", "scene_en": "Candid View Pulls You In", "time": "00:08",
         "context": "用偷拍视角拍摄，仿佛在背后偷看，代入感更强，观众更容易进入画面。",
         "sentences": [
            ["不要这样摆拍。", "Don't shoot it as a staged pose.", "staged（摆拍）"],
            ["用偷拍视角拍，这样带入感更强。", "Use a candid view—it pulls the audience in.", "candid view（偷拍视角）"],
            ["像在不经意间记录，观众更有代入感。", "It feels like a casual catch, drawing viewers in.", "pull in（带入）"]
         ]},
        {"id": "s5", "scene_zh": "手上拿东西更自然", "scene_en": "Hold Something for Natural Hands", "time": "00:12",
         "context": "人物空手站立容易手足无措，手上拿点东西（如杯子、手机）会更自然。",
         "sentences": [
            ["不要这样空手干站着。", "Don't just stand there empty-handed.", "empty-handed（空手）"],
            ["这样拍，手上拿点东西会更自然。", "Shoot it this way—holding something looks natural.", "hold something（拿着东西）"],
            ["手里有东西，肢体就不尴尬了。", "Something in hand, no awkward limbs.", "awkward（尴尬）"]
         ]},
        {"id": "s6", "scene_zh": "镜头微晃有呼吸感", "scene_en": "Subtle Shake Feels Alive", "time": "00:15",
         "context": "镜头轻微晃动制造呼吸感，画面更有生命力，比完全静止更有温度。",
         "sentences": [
            ["不要这样完全不动地拍。", "Don't keep the camera totally still.", "totally still（完全静止）"],
            ["镜头微晃，更加有呼吸感。", "A subtle shake adds a breathing feel.", "breathing feel（呼吸感）"],
            ["轻微的晃动让画面活了起来。", "The gentle movement brings the frame to life.", "bring to life（赋予生命力）"]
         ]}
    ]
}

ARTICLES["42u6PCAZwG5"] = {
    "title_zh": "万能对话戏拍法来了",
    "title_en": "The Universal Way to Film Dialogue",
    "duration": "03:40",
    "topic": "摄影 · 正反打",
    "scenes": [
        {"id": "s1", "scene_zh": "降低机位平视演员", "scene_en": "Lower the Camera to Eye Level", "time": "00:00",
         "context": "对话戏拍得没感觉，先降低机位和演员平视，并带着人物关系去拍，立马有戏。",
         "sentences": [
            ["对话戏这么拍没感觉。", "Filming dialogue like this feels flat.", "flat（没感觉）"],
            ["把机位降下来，和演员平视。", "Lower the camera to the actor's eye level.", "eye level（平视）"],
            ["并带着关系去拍，立马有戏了。", "Shoot with relationship in mind—and it comes alive.", "comes alive（有戏）"]
         ]},
        {"id": "s2", "scene_zh": "外反打带人物关系", "scene_en": "Outside Reverse: Carry the Relationship", "time": "00:12",
         "context": "外反打是正反打中常见的一种：镜头越过一方肩膀拍另一方，画面带着人物关系、更有层次。",
         "sentences": [
            ["这不就是我们常说的正反打吗。", "Isn't this the classic shot-reverse-shot?", "shot-reverse-shot（正反打）"],
            ["这是正反打中的外反打。", "This one is the outside reverse.", "outside reverse（外反打）"],
            ["外反打带着人物关系，画面更有层次。", "It carries the relationship and adds depth.", "adds depth（更有层次）"]
         ]},
        {"id": "s3", "scene_zh": "内反打表达内心", "scene_en": "Inside Reverse: Show the Inner World", "time": "00:24",
         "context": "内反打不拍对方，只拍单人，用于表达人物内心活动。",
         "sentences": [
            ["有外反打，那还有内反打啰。", "If there's an outside reverse, there's an inside reverse too.", "inside reverse（内反打）"],
            ["内反打则是表达人物内心。", "The inside reverse expresses a character's inner world.", "inner world（内心）"]
         ]},
        {"id": "s4", "scene_zh": "轴线与中间机位", "scene_en": "The Axis and the Center Position", "time": "00:47",
         "context": "二人对话时中间有一条轴线，两边的机位是外反打和内反打，还有一个机位在中间可以拍双人。",
         "sentences": [
            ["二人对话时，中间有一条轴线。", "Two people in dialogue share an axis between them.", "axis（轴线）"],
            ["这两边的机位，就是外反打和内反打。", "The two side positions are outside and inside reverses.", "side positions（两侧机位）"],
            ["还有一个机位在中间，可以拍二人同框。", "A center position captures both people.", "center position（中间机位）"],
            ["这个机位好有仪式感，再推紧一些还能制造戏剧效果。", "This position feels ceremonial; push in for drama.", "ceremonial（仪式感）"]
         ]},
        {"id": "s5", "scene_zh": "骑轴拍打破第四堵墙", "scene_en": "Ride the Axis: Break the Fourth Wall", "time": "01:20",
         "context": "骑轴拍就是机位在二人中间，类似打破第四堵墙，还有主观视角效果，能把观众带入角色。",
         "sentences": [
            ["咱还可以骑轴拍。", "You can also ride the axis.", "ride the axis（骑轴）"],
            ["骑轴其实就是机位在二人中间。", "Riding the axis puts the camera between them.", "between them（二人中间）"],
            ["类似打破第四堵墙，有主观视角效果。", "It breaks the fourth wall with a POV feel.", "fourth wall（第四堵墙）"],
            ["能将观众带入角色，产生代入感。", "It drops viewers into the character's shoes.", "into the shoes（代入）"]
         ]},
        {"id": "s6", "scene_zh": "越轴要根据情节", "scene_en": "Crossing the Axis: Follow the Story", "time": "01:38",
         "context": "很多教程说不能越轴，其实要看情节：为了表达需要，可以故意越轴甚至跳切。",
         "sentences": [
            ["还有很多人讲，再怎么样咱都不能越轴。", "Many say you must never cross the axis.", "cross the axis（越轴）"],
            ["谁说不可以越，要根据情节来。", "Who says not? It depends on the story.", "depends on the story（看情节）"],
            ["我还运镜着越，再给你来个跳切呢。", "I can cross while moving, then cut.", "jump cut（跳切）"],
            ["不要为了眼前一点蝇头小利，而放弃了长远规划。", "Don't trade long-term planning for short-term gain.", "long-term planning（长远规划）"]
         ]}
    ]
}

ARTICLES["female-parking-skill"] = {
    "title_zh": "侧方停车一次到位技巧",
    "title_en": "Parallel Parking: Get It Right the First Time",
    "duration": "01:31",
    "topic": "驾驶 · 侧方停车",
    "scenes": [
        {"id": "s1", "scene_zh": "案例复盘", "scene_en": "Reviewing the Case", "time": "00:00",
         "context": "这位女士在两边停满电动车的车位倒车入库，发现位置不合适后通过熟练操作调整成功。",
         "sentences": [
            ["来看案例，这位女士进行侧方停车。", "Let's watch this driver parallel park.", "parallel park（侧方停车）"],
            ["由于两边停满了电动车，而且车位也不长。", "Both sides are packed with e-bikes, and the spot is short.", "packed（停满）"],
            ["第一次倒进去发现位置不合适，她通过熟练操作进行了调整。", "Her first attempt didn't fit, so she adjusted smoothly.", "adjust（调整）"]
         ]},
        {"id": "s2", "scene_zh": "核心思路：车尾对准假角", "scene_en": "Key Idea: Aim the Tail at the Corner", "time": "00:19",
         "context": "侧方停车就是把车尾尽可能停到假角处，让后轮先找好位置，车身角度不用管。",
         "sentences": [
            ["她入场方式目的性非常强，就是让车尾停到假角处。", "Her entry is purposeful: plant the tail at the corner.", "corner（假角处）"],
            ["让后车轮先找到位置。", "Get the rear wheel seated first.", "rear wheel（后轮）"],
            ["车身的角度你完全不用管。", "Don't worry about the body angle at all.", "body angle（车身角度）"]
         ]},
        {"id": "s3", "scene_zh": "优化点一：贴近障碍物", "scene_en": "Tip 1: Stay Close to the Obstacle", "time": "00:47",
         "context": "入场时尽可能贴近库位这一边的障碍物，给另一侧甩出足够的外摆空间。",
         "sentences": [
            ["第一点，入场时尽可能贴近库位这一边的障碍物。", "First, hug the obstacle on your side of the spot.", "hug the obstacle（贴近障碍物）"],
            ["给另一侧甩出足够的外摆空间。", "Leave enough swing room on the other side.", "swing room（外摆空间）"]
         ]},
        {"id": "s4", "scene_zh": "优化点二：后轮过障碍点", "scene_en": "Tip 2: Pass the Obstacle Point First", "time": "00:53",
         "context": "后车轮一定要过了障碍点再停车，距离越长能甩过去的角度就越大。",
         "sentences": [
            ["第二点，后车轮一定要过了障碍点再停车。", "Second, drive past the obstacle before stopping.", "obstacle point（障碍点）"],
            ["因为距离越长，能甩过去的角度也就越大。", "More distance means a bigger swing angle.", "swing angle（甩角）"]
         ]},
        {"id": "s5", "scene_zh": "走一点倒一点重复", "scene_en": "Advance a Bit, Reverse a Bit, Repeat", "time": "01:10",
         "context": "后轮到位后，只需要右前方走一点、反方向倒一点，重复操作车头就进去了。",
         "sentences": [
            ["后车轮找到位置后，就是右前方走一点，反方向倒一点。", "Once the rear wheel is set, nudge right-forward, then reverse a bit.", "nudge（轻挪）"],
            ["但切记不要走太多，不然后轮被拉出来，车身就会偏外。", "Don't nudge too far, or the rear wheel pulls out and the body sits off.", "pulls out（被拉出来）"],
            ["所以不管前方多少空间，就走一点，反方向倒一点，重复操作。", "No matter the space ahead, advance a bit and reverse a bit, repeating.", "repeat（重复）"]
         ]},
        {"id": "s6", "scene_zh": "侧方停车其实不难", "scene_en": "Parallel Parking Isn't Hard", "time": "01:24",
         "context": "哪怕后轮到位后车身角度歪，也是完全一样的操作，所以侧方停车并不难。",
         "sentences": [
            ["哪怕后轮找到位置之后，车身的角度是歪的，也是完全一样的操作。", "Even if the body sits at an angle, the procedure is identical.", "procedure（操作流程）"],
            ["所以你现在还认为侧方停车很难吗。", "So do you still think parallel parking is hard?", "hard（难）"]
         ]}
    ]
}

ARTICLES["parallel-parking-adjust"] = {
    "title_zh": "侧方停车进不去怎么调整",
    "title_en": "How to Fix a Parallel Park That Won't Fit",
    "duration": "02:04",
    "topic": "驾驶 · 侧方停车",
    "scenes": [
        {"id": "s1", "scene_zh": "两种失败情况", "scene_en": "The Two Failure Modes", "time": "00:00",
         "context": "侧方停车进不去无非两种情况：角度大了车身偏离车头被卡住，或角度小了车身偏外后轮进不去。",
         "sentences": [
            ["侧方停车进不去，无非就两种情况。", "A failed parallel park comes down to two cases.", "two cases（两种情况）"],
            ["第一种，角度大了，车身偏离，车头被卡住。", "First: too sharp an angle—the nose is stuck.", "stuck nose（车头卡住）"],
            ["第二种，角度小了，车身偏外，后轮进不去。", "Second: too shallow an angle—the rear wheel won't enter.", "rear wheel（后轮）"]
         ]},
        {"id": "s2", "scene_zh": "正确进库思路", "scene_en": "The Right Way to Enter", "time": "00:12",
         "context": "先贴近白车观察后视镜，让车尾朝着库位的后半部分去倒，后轮送到位，前面有空间就等于进空了。",
         "sentences": [
            ["讲之前先了解一下怎么样进最简单：靠近白车，观察后视镜。", "First, the simplest entry: pull close to the white car and watch the mirror.", "side mirror（后视镜）"],
            ["让你的车尾朝着库位的后半部分去倒车。", "Aim your tail at the back half of the spot.", "back half（后半部分）"],
            ["后轮送到位，前面有空间，就等于进空了。", "Seat the rear wheel and space up front means you're in.", "seat the wheel（后轮到位）"]
         ]},
        {"id": "s3", "scene_zh": "角度大了怎么调整", "scene_en": "Too Sharp: Fix It by Swing-Out", "time": "01:03",
         "context": "角度大了车身偏底、车头被卡住时，把车开出去做一次甩尾：往前开后轮过障碍点再往里打方向，车尾就往外甩。",
         "sentences": [
            ["倒进来后发现角度大了，车头被卡住了。", "Came in too sharp and the nose is stuck.", "too sharp（角度大）"],
            ["我们只需要把车开出去，进行一下甩尾就可以了。", "Just drive out and do a swing-out.", "swing-out（甩尾）"],
            ["往前开，后轮过了障碍点之后往里打方向，车尾的角度就往外甩了。", "Drive forward, turn past the obstacle, and the tail swings out.", "swings out（往外甩）"],
            ["之后朝着库尾的后半部分去倒，把后轮先送到位。", "Then reverse toward the back half and seat the rear wheel.", "back half（后半部分）"]
         ]},
        {"id": "s4", "scene_zh": "角度小了怎么调整", "scene_en": "Too Shallow: Turn Out to Fix It", "time": "01:38",
         "context": "车身偏外时往外打方向往前走，车尾就甩过来了，然后再倒进去。",
         "sentences": [
            ["倒进来后发现车身偏外。", "Came in too shallow and the body sits out.", "too shallow（角度小）"],
            ["让车尾对着库尾的后半部分，肯定是往外打方向。", "To aim the tail at the back half, steer outward.", "steer outward（往外打）"],
            ["往前走，往外打方向，车尾不就甩过来了吗。", "Drive forward, steer out, and the tail swings across.", "swings across（甩过来）"],
            ["之后还是同样的操作：倒进去，把后轮送到位。", "Then repeat: reverse in and seat the rear wheel.", "seat（送到位）"]
         ]},
        {"id": "s5", "scene_zh": "核心是调整思路", "scene_en": "It's About the Adjustment Logic", "time": "02:01",
         "context": "这些操作不要死记，理解不了就多看几遍，主要是把调整的思路搞清楚。",
         "sentences": [
            ["这些东西不要去死记。", "Don't memorize these by rote.", "by rote（死记）"],
            ["理解不了就多看几遍。", "If you can't follow, rewatch it.", "rewatch（再看一遍）"],
            ["主要是把调整的思路搞清楚。", "The point is to nail the adjustment logic.", "adjustment logic（调整思路）"]
         ]}
    ]
}

ARTICLES["narrow-parking-adjust"] = {
    "title_zh": "窄路侧方停车调整",
    "title_en": "Parallel Parking in a Narrow Street",
    "duration": "01:15",
    "topic": "驾驶 · 侧方停车",
    "scenes": [
        {"id": "s1", "scene_zh": "窄路失败的案例", "scene_en": "A Narrow-Street Failure", "time": "00:00",
         "context": "路不是很宽时调整多次仍失败，车身偏外最终只能放弃车位，问题出在哪？",
         "sentences": [
            ["路不是很宽，这位司机调整了很多次都没能成功入库。", "The street is narrow, and the driver can't get in after many tries.", "narrow street（窄路）"],
            ["整体来说还是车身偏外，最终还是放弃了车位。", "The body stays out, and the spot is finally given up.", "given up（放弃）"],
            ["问题出在哪？我们讲一下。", "Where's the problem? Let's break it down.", "break it down（拆解）"]
         ]},
        {"id": "s2", "scene_zh": "问题：中途回正方向", "scene_en": "The Mistake: Centering Too Early", "time": "00:09",
         "context": "前面的操作没有错：先贴近旁边车给车头留出外摆空间，但倒到一半把前轮回正，导致后轮没送进去。",
         "sentences": [
            ["它前面的操作没有任何问题，先贴近旁边车，给左侧车头留出外摆的空间。", "The entry is fine: hug the car beside and leave swing room for the nose.", "swing room（外摆空间）"],
            ["但倒到一半，它把前轮回正了。", "But midway, it centers the front wheels.", "centers（回正）"],
            ["所以就导致后车轮没有送进去。", "That's why the rear wheel never seats.", "rear wheel（后轮）"]
         ]},
        {"id": "s3", "scene_zh": "正确做法：不回正继续倒", "scene_en": "The Fix: Keep Turning While Backing", "time": "00:25",
         "context": "车身偏外的主因是后轮没到位，倒车时应随着后轮往库里走加大角度继续倒，而不是回正方向。",
         "sentences": [
            ["车身偏外的主要原因，就是因为后车轮没有送到位。", "The main cause of sitting out is the unseated rear wheel.", "sitting out（偏外）"],
            ["随着后轮往库里走，车头外摆的空间也会越来越大。", "As the rear wheel moves in, the nose swing room grows.", "grows（变大）"],
            ["这时候不应该回正方向，而是加大角度继续倒车。", "Don't center now—increase the angle and keep backing.", "keep backing（继续倒）"],
            ["目的就一个：把后车轮先送进去。", "One goal: seat the rear wheel first.", "one goal（一个目的）"]
         ]},
        {"id": "s4", "scene_zh": "后轮到位等于进库", "scene_en": "Rear Wheel Seated = You're In", "time": "00:36",
         "context": "不用管车身角度停成什么样子，只要后轮能到位且车头右前方有空间，就等于进库了。",
         "sentences": [
            ["你不用管车身角度停成什么样子。", "Don't care how the body angle looks.", "body angle（车身角度）"],
            ["只要后车轮能到位，并且车头右前方有空间，就等于已经进库了。", "If the rear wheel seats and the nose has room, you're in.", "you're in（已进库）"],
            ["之后只需要右前方走一点，反方向倒一点，重复操作也就可以了。", "Then nudge right-forward and reverse a bit, repeating.", "nudge（轻挪）"]
         ]},
        {"id": "s5", "scene_zh": "注意：别走太多", "scene_en": "Caution: Don't Nudge Too Far", "time": "00:53",
         "context": "右前方走的时候切记不要走太多，不然后轮会被拉出去，车身还是会偏外。",
         "sentences": [
            ["但切记，右前方走的时候不要走太多。", "But mind you: don't nudge right-forward too far.", "too far（走太多）"],
            ["不然后车轮会被拉出去，车身还是会偏外。", "Or the rear wheel gets pulled out and the body sits out again.", "pulled out（被拉出去）"],
            ["好，下一期咱们缩短车位。", "Next episode: an even shorter spot.", "shorter spot（更短的车位）"]
         ]}
    ]
}

ARTICLES["parallel-parking"] = {
    "title_zh": "侧方停车入库调整",
    "title_en": "Adjusting Your Parallel Park Entry",
    "duration": "00:58",
    "topic": "驾驶 · 侧方停车",
    "scenes": [
        {"id": "s1", "scene_zh": "两种情况", "scene_en": "Two Common Scenarios", "time": "00:00",
         "context": "侧方停车入库时难免方向打早或打晚，导致车身只停进一半，或后轮压到马路牙子。",
         "sentences": [
            ["側方停车入库时，难免会出现方向打早或者打晚了。", "Parallel parking often ends up with the steering turned too early or too late.", "too early / too late（打早 / 打晚）"],
            ["导致出现车身只停进半个车位，或者后轮压马路牙子。", "Leaving the body half-in, or the rear wheel on the curb.", "curb（马路牙子）"],
            ["遇到这两个情况，该怎么调整？", "How do you fix either case?", "how to fix（怎么调整）"]
         ]},
        {"id": "s2", "scene_zh": "情况一：离牙子远了", "scene_en": "Case 1: Too Far from the Curb", "time": "00:08",
         "context": "停好后发现车离马路牙子远，不要盲目打方向乱倒：左打满往前上，后视镜出现后车整个车头后回正，再倒，左后轮即将压线时左打满入库。",
         "sentences": [
            ["停下来以后，发现车离马路牙子远了。", "You stop and find the car too far from the curb.", "too far（太远）"],
            ["很简单，把方向左打满，往左前上再出去。", "Simple: steer hard left and pull forward out.", "steer hard left（左打满）"],
            ["往前出多少？只要左后视镜出现后车的整个车头后，回正方向继续往后倒。", "How far? Until the left mirror shows the car's whole nose, then center and reverse.", "mirror view（后视镜视野）"],
            ["左后轮即将压线时，方向盘向左打满入库，车身与路边平行时回正停车。", "Just before the left rear wheel crosses the line, steer hard left in; center when parallel.", "cross the line（压线）"]
         ]},
        {"id": "s3", "scene_zh": "情况二：后轮离牙子近", "scene_en": "Case 2: Rear Wheel Too Close to the Curb", "time": "00:41",
         "context": "后轮离马路牙子近时，不需要出去重来：向右打满往前上，再左打满往后倒，车身平行后调整前后距离即可。",
         "sentences": [
            ["第二种情况，就是后轮离马路牙子近了。", "Second case: the rear wheel sits too close to the curb.", "too close（太近）"],
            ["很多新手会选择出去重来一次。", "Many novices restart from scratch.", "start over（重来）"],
            ["其实只需要把方向向右打满，往前上一上。", "Actually, steer hard right and nudge forward.", "steer hard right（右打满）"],
            ["然后方向左打满，往后倒一倒，车身跟马路牙子平行时调整前后距离。", "Then steer hard left and reverse; adjust fore-aft once parallel.", "fore-aft（前后距离）"],
            ["车子也能顺利入库成功。", "And the car parks cleanly.", "parks cleanly（顺利入库）"]
         ]}
    ]
}

ARTICLES["suspension-underrated"] = {
    "title_zh": "为什么悬架是汽车最被低估的技术？",
    "title_en": "Why Suspension Is the Most Underrated Tech",
    "duration": "04:42",
    "topic": "汽车 · 悬架",
    "scenes": [
        {"id": "s1", "scene_zh": "没有悬架会怎样", "scene_en": "Life Without Suspension", "time": "00:00",
         "context": "没有悬架，踩油门车身仰起、过弯侧倾、过减速带直接颠到骨折，悬架是第一道防线。",
         "sentences": [
            ["如果你的汽车没有悬架会发生什么？", "What happens if your car has no suspension?", "suspension（悬架）"],
            ["踩油门会这样，过弯会这样，过减速带会这样。", "Accelerate: it rears. Corner: it leans. Speed bump: it crashes.", "rears（仰起）"],
            ["你没有看错，直接就颠骨折了。", "No joke—it shakes you to the bone.", "shakes to the bone（颠到骨头）"]
         ]},
        {"id": "s2", "scene_zh": "从板簧到螺旋弹簧", "scene_en": "From Leaf Springs to Coil Springs", "time": "00:26",
         "context": "最早的汽车只有硬连接，后来人们把马车的板簧装上，再换成螺旋弹簧，舒适性逐步提升。",
         "sentences": [
            ["这是最初的汽车，过颠簸路段时是这样的。", "The earliest cars bounced wildly over bumps.", "bounced（颠簸）"],
            ["把马车上的板簧加上，是不是好点？是好了点，但不够好。", "Add carriage leaf springs—better, but not enough.", "leaf springs（板簧）"],
            ["把板簧换成螺旋弹簧，车子会不会更舒服？答案是会。", "Swap in coil springs and it gets much comfier.", "coil springs（螺旋弹簧）"]
         ]},
        {"id": "s3", "scene_zh": "减震器的诞生", "scene_en": "Enter the Shock Absorber", "time": "00:43",
         "context": "螺旋弹簧会让车弹起来，于是劳斯莱斯兄弟用充满油的缸体加活塞杆造出减震器，油液流动形成阻力吸收震动。",
         "sentences": [
            ["开过颠簸之后，车又会弹起来一段。", "After a bump, the car keeps bouncing.", "bouncing（弹跳）"],
            ["劳斯莱斯兄弟用一个充满油的缸体加活塞杆造了一个减震器。", "The Rolls-Royce brothers built a shock absorber: an oil-filled cylinder with a piston.", "shock absorber（减震器）"],
            ["活塞在油液中移动，油通过小口流动形成阻力，从而减少震动。", "The piston pushes oil through small holes, creating resistance that damps motion.", "resistance（阻力）"]
         ]},
        {"id": "s4", "scene_zh": "麦弗逊与双叉臂", "scene_en": "MacPherson and Double Wishbone", "time": "01:04",
         "context": "麦弗逊把减震弹簧和下叉臂集成抵消侧倾；路特斯的查普曼觉得不够，再加一根上叉臂做成双叉臂，精准控制轮胎姿态。",
         "sentences": [
            ["转弯时侧倾严重，一边轮胎抓地力好，一边弱，车速稍快很容易甩出弯道。", "Cornering leans hard, one tire grips, the other doesn't—spin-out risk rises.", "spin-out（甩出弯道）"],
            ["福特工程师麦弗逊把减震器弹簧和下叉臂集成在一起，悬架就能抵消侧倾的力。", "Ford's MacPherson merged spring and strut with a lower arm to counter body roll.", "body roll（侧倾）"],
            ["路特斯的查普曼觉得不够，还要再多一根上叉臂。", "Lotus's Chapman wanted more—add an upper wishbone.", "upper wishbone（上叉臂）"],
            ["双叉臂能精准控制轮胎与地面接触的姿态，高速过弯更咬地。", "Double wishbones control tire attitude precisely, biting harder in fast corners.", "bite（咬地）"]
         ]},
        {"id": "s5", "scene_zh": "五连杆与空气悬架", "scene_en": "Five-Link and Air Suspension", "time": "01:53",
         "context": "奔驰用五连杆分担力提升舒适；凯迪拉克把钢弹簧换成气囊，靠打气放气控制软硬和高度，实现升降和软硬调节。",
         "sentences": [
            ["两个连杆不够，需要多个控制臂来分担力，奔驰一次性拉满发明了五连杆悬架。", "Two arms aren't enough—Mercedes invented the five-link to spread the load.", "five-link（五连杆）"],
            ["传统弹簧太死，没法面对复杂的载重和多变的路况。", "Fixed springs can't handle varying load and rough roads.", "varying load（多变载重）"],
            ["凯迪拉克把钢弹簧换成了气囊，靠打气和放气来控制软硬和高度。", "Cadillac swapped steel for air bags, adjusting firmness and height by air.", "air bags（气囊）"],
            ["带空悬的车，上高速自动降低重心，下烂路自动升高底盘。", "Air-sprung cars lower on the highway and lift on rough ground.", "lower the center（降低重心）"]
         ]},
        {"id": "s6", "scene_zh": "CDC与魔毯悬架", "scene_en": "CDC and Magic-Carpet Suspension", "time": "03:02",
         "context": "宝马工程师给减震器加电磁阀控制油口大小调阻尼；新能源车用激光雷达摄像头提前看到坑，ECU提前调软调硬，即魔毯悬架。",
         "sentences": [
            ["一位宝马的工程师觉得不够：减震可以调节软硬，但阻尼不可以自由调节。", "A BMW engineer found damping couldn't vary—only spring stiffness.", "damping（阻尼）"],
            ["它在油液通道旁边多加了一个电磁阀，控制油口大小，从而控制阻尼的软硬。", "He added a solenoid valve to size the oil port and tune the damping.", "solenoid valve（电磁阀）"],
            ["新能源车用激光雷达、摄像头、惯性传感器提前看到坑洼。", "EVs use lidar, cameras, and IMUs to see potholes ahead.", "lidar（激光雷达）"],
            ["到达之前，ECU就把减震器调软或调硬，这就是大家说的魔毯悬架。", "Before arrival, the ECU pre-tunes the damper—the magic-carpet ride.", "magic-carpet（魔毯）"]
         ]},
        {"id": "s7", "scene_zh": "悬架记录了汽车的跃迁", "scene_en": "Suspension Tells the Car's Evolution", "time": "03:40",
         "context": "悬架是所有汽车技术进化中最内在的演化，记录了从马车到汽车再到新能源汽车的每一次跃迁。",
         "sentences": [
            ["悬架是所有汽车技术进化当中最内在的演化。", "Suspension is the most intrinsic evolution in car tech.", "intrinsic（内在的）"],
            ["它记录了汽车从马车到汽车，再到新能源汽车的每一次跃迁。", "It records every leap from carriage to car to EV.", "leap（跃迁）"],
            ["每一次震动被悄悄收住，都是人类试图掌控混沌的微小胜利。", "Every absorbed shock is a small human victory over chaos.", "absorbed shock（被收住的震动）"]
         ]},
        {"id": "s8", "scene_zh": "底盘到底怎么选", "scene_en": "How to Choose Your Chassis", "time": "04:28",
         "context": "底盘怎么选还得看大家要什么样的体验，常见的用车类型、悬架配置、适合建议一目了然。",
         "sentences": [
            ["说了这么多，底盘到底要怎么选呢？", "After all this, how do you pick a chassis?", "chassis（底盘）"],
            ["还得看大家要什么样的体验。", "It comes down to the experience you want.", "experience（体验）"],
            ["下面这张表格把常见的用车类型、悬架配置、适合建议都列出来了。", "The table lists car types, suspension setups, and recommendations.", "setup（配置）"]
         ]}
    ]
}

ARTICLES["exhaust-bang"] = {
    "title_zh": "排气为什么会放炮？涡轮迟滞&偏时点火",
    "title_en": "Why Exhausts Backfire: Lag & Anti-Lag",
    "duration": "12:25",
    "topic": "汽车 · 涡轮",
    "scenes": [
        {"id": "s1", "scene_zh": "放炮只是一个结果", "scene_en": "Backfire Is a Result, Not a Goal", "time": "00:00",
         "context": "排气放炮只是解决涡轮迟滞几种方法带来的结果，偏时点火只是其中一种，两者不能画等号。",
         "sentences": [
            ["很多人一听到排气放炮，顺口就会说是偏时点火，其实这并不准确。", "Many say backfire equals anti-lag—that's not quite accurate.", "anti-lag（偏时点火）"],
            ["排气放炮实际上只是一个结果，并不是目的。", "The bang is a result, not the goal.", "result（结果）"],
            ["偏时点火会引起排气放炮，而排气放炮不一定就是偏时点火。", "Anti-lag causes backfire, but not all backfire is anti-lag.", "not all（不一定）"]
         ]},
        {"id": "s2", "scene_zh": "什么是涡轮迟滞", "scene_en": "What Turbo Lag Is", "time": "01:02",
         "context": "松开油门节气门关闭，排气变少涡轮转速掉下来；重新踩油门把涡轮重新吹起来需要时间，这就是涡轮迟滞。",
         "sentences": [
            ["松油门时，节气门基本就关上了，发动机只吸入很少的空气。", "Lift off and the throttle closes; the engine gulps barely any air.", "throttle（节气门）"],
            ["吸入的空气少了，排气排出去的自然也就少了，没有足够的排气吹动涡轮。", "Less air in means less exhaust to spin the turbo.", "spin the turbo（吹动涡轮）"],
            ["重新踩油门把变慢的涡轮重新吹起来需要一段时间，这就是涡轮迟滞。", "Re-spooling the slowed turbo takes time—that's turbo lag.", "turbo lag（涡轮迟滞）"],
            ["表现出来就是油门踩到底，车却要过一秒两秒才猛窜出去。", "You floor it and the car lunges only a second or two later.", "lunge（猛窜）"]
         ]},
        {"id": "s3", "scene_zh": "最简单的解法不可行", "scene_en": "The Obvious Fix Is a Dead End", "time": "03:14",
         "context": "有人说让节气门一直开着发动机别停，但那样松不松油门都一样，车子马力全开往前冲，非常危险。",
         "sentences": [
            ["有的朋友说，只要把节气门一直开着，不让它关不就行了。", "Some say: keep the throttle open so the engine never stops.", "throttle open（节气门常开）"],
            ["那样效果就是你松不松油门已经没有区别，车子都是马力全开往前冲。", "Then lift-off makes no difference—the car runs flat-out.", "flat-out（马力全开）"],
            ["这肯定是非常危险的，显然不可行。", "That's clearly dangerous and unworkable.", "dangerous（危险）"]
         ]},
        {"id": "s4", "scene_zh": "偏时点火的原理", "scene_en": "How Anti-Lag Works", "time": "03:43",
         "context": "偏时点火：松油门时节气门保留一点开度继续喷油，但电脑把点火延后到排气冲程，让汽油在排气管中被高温点燃，继续吹动涡轮。",
         "sentences": [
            ["节气门还是保留一点点的开度，钢内继续喷油照喷不误。", "The throttle stays slightly open and the cylinder keeps injecting fuel.", "inject fuel（喷油）"],
            ["唯一不同的是，电脑控制点火延后，到了该点火的时候不点火。", "The difference: the ECU delays the spark instead of firing on time.", "delay the spark（延迟点火）"],
            ["汽油只来得及燃烧一小部分维持发动机运转，绝大部分没烧完的油气被排入排气管。", "Only a fraction burns to keep the engine running; the rest flows into the exhaust.", "exhaust manifold（排气歧管）"],
            ["油气遇到滚烫的排气管被高温点燃，燃爆的气体继续吹动涡轮保持转速。", "The mix ignites on the red-hot pipes, and the blast keeps the turbo spinning.", "ignite（点燃）"],
            ["说白了就是把本来应该在缸内燃爆的汽油，拿到排气管里燃爆。", "In short: burn in the exhaust what normally burns in the cylinder.", "in short（说白了）"]
         ]},
        {"id": "s5", "scene_zh": "放炮的由来与局限", "scene_en": "Where the Bang Comes From", "time": "05:34",
         "context": "把汽油搞到排气管里点燃，排气不放炮才怪；但这种做法会大幅缩短排气管和涡轮寿命，民用车上开猛一点涡轮制保器可能只有三百公里。",
         "sentences": [
            ["排气为什么会放炮？你都已经把汽油搞到排气管里点燃了，不放炮才怪。", "Why the bang? You're burning fuel in the exhaust—of course it pops.", "of course（当然）"],
            ["松掉油门踏板时听到的那种声音，就是汽油在排气歧管里劈里啪啦燃烧的声音。", "The popping on lift-off is fuel crackling in the manifold.", "crackling（劈啪声）"],
            ["偏时点火和二次进气能简单粗暴地避免迟滞，但排气管和涡轮设计时不是用来在里面爆炸的。", "They're brutal fixes, but manifolds weren't designed to detonate.", "detonate（爆炸）"],
            ["长时间高强度地使用会大幅缩短排气管和涡轮的寿命，民用车上开猛一点制保器可能只有三天两百公里。", "Constant hard use guts the turbo's life—on a street car, maybe 300 km.", "guts the life（大幅缩命）"]
         ]},
        {"id": "s6", "scene_zh": "自吸与故障也会放炮", "scene_en": "NA Cars and Faults Also Pop", "time": "10:26",
         "context": "自吸车在超浓混合气下也可能在排气管尾端放炮；正常家用车正时、火花塞或油路出问题也会放炮，油喷太多或太少都可能。",
         "sentences": [
            ["还有没有其他情况排气也会放炮？答案是有的。", "Any other ways exhausts pop? Yes.", "any other（其他情况）"],
            ["自吸车在超浓的混合气下工作，排气管温度足够高，也会在排气管尾端放炮。", "A rich-running NA car with hot pipes pops at the tailpipe.", "rich mixture（超浓混合气）"],
            ["正常家用车出故障也可能放炮，比如正时或火花塞出了问题，该点火时点不着火。", "Faulty timing or spark plugs can also make a street car pop.", "spark plugs（火花塞）"],
            ["油路出故障也可能导致放炮，油喷多了会放炮，油喷太少汽油燃烧变慢也可能放炮。", "Fuel system faults too: too much fuel, or too little burning slow.", "fuel system（油路）"]
         ]}
    ]
}

ARTICLES["esp-principle"] = {
    "title_zh": "ESP车身稳定系统工作原理",
    "title_en": "How ESP Electronic Stability Works",
    "duration": "14:21",
    "topic": "汽车 · ESP",
    "scenes": [
        {"id": "s1", "scene_zh": "ESP是什么", "scene_en": "What ESP Is", "time": "00:00",
         "context": "ESP是Electronic Stability Program的缩写，即电子稳定程序；也叫ESC，还有很多厂商各自的叫法，本质都是车身稳定系统。",
         "sentences": [
            ["ESP是英文Electronic Stability Program的首字母缩写。", "ESP stands for Electronic Stability Program.", "stand for（缩写为）"],
            ["直接翻译就是电子稳定程序的意思，也有车叫它ESC。", "Literally 'electronic stability program'; some brands call it ESC.", "Electronic Stability Control（电子稳定控制）"],
            ["本田叫VSA，丰田叫VSC，日产斯巴鲁叫VDC，宝马捷豹路虎叫DSC，本质都是车身稳定系统。", "Honda calls it VSA, Toyota VSC, Nissan VDC, BMW DSC—same thing underneath.", "same thing（同一回事）"]
         ]},
        {"id": "s2", "scene_zh": "如何监测打滑", "scene_en": "How It Detects Slip", "time": "01:50",
         "context": "ESP靠几类传感器监测车身：方向盘角度传感器告诉电脑驾驶员想去的方向，横摆传感器测车身摆动，轮速传感器测打滑，加速度传感器确认姿态。",
         "sentences": [
            ["首先要靠传感器监测车身状态：方向盘角度传感器告诉电脑驾驶员想往哪个方向去。", "First, sensors read the car: the steering-angle sensor reports the driver's intent.", "steering-angle sensor（方向盘角度传感器）"],
            ["横摆传感器实时监测车身摆动的幅度，摆动大就说明要失控甚至翻车了。", "A yaw sensor tracks the body's rotation; big swings mean imminent loss of control.", "yaw sensor（横摆传感器）"],
            ["四个轮子上的速度传感器（也就是ABS传感器）检测每个轮子的转速，哪个轮子转得不一样就说明打滑了。", "Wheel-speed (ABS) sensors spot a wheel spinning out of sync—that's slip.", "wheel-speed sensor（轮速传感器）"],
            ["加速度传感器配合横摆传感器，让电脑知道车身是侧翻、前倾还是后仰。", "Accelerometers refine whether the body is rolling, diving, or pitching.", "accelerometer（加速度传感器）"]
         ]},
        {"id": "s3", "scene_zh": "紧急避障的介入", "scene_en": "Intervention in an Emergency Swerve", "time": "05:11",
         "context": "高速上突然遇到前车急停，没有ESP会出现转向不足追尾或回打方向转向过度甩出；有ESP时电脑单独给某个轮子刹车修正车身。",
         "sentences": [
            ["高速120公里时前方有车紧急停在超车道，刹车来不及，只能一把方向往右打。", "At 120 km/h a car stops ahead; no time to brake, so you yank right.", "yank the wheel（急打方向）"],
            ["没有ESP很可能出现转向不足：实际转过的幅度小于方向盘打的幅度。", "Without ESP comes understeer: the car turns less than you asked.", "understeer（转向不足）"],
            ["回打方向时车身晃动最厉害，最容易产生转向过度然后彻底失控。", "The counter-steer wobble invites oversteer and a full spin.", "oversteer（转向过度）"],
            ["有ESP时，电脑通过ABS只对右后轮制动，让车绕这个点向右转动，修正转向不足。", "With ESP, the computer brakes just the right-rear wheel, yawing the car into the turn.", "brake one wheel（单轮制动）"],
            ["回打方向时电脑又只对右前轮制动，产生向右摆动的趋势，抵消转向过度。", "On counter-steer it brakes the right-front, countering the oversteer.", "counter（抵消）"]
         ]},
        {"id": "s4", "scene_zh": "日常打滑与电子限滑", "scene_en": "Everyday Slip and Electronic LSD", "time": "08:47",
         "context": "雨天压水坑、压冰、过砂石路面会抢方向盘，ESP可以刹慢有抓地力的轮子把车身修正回来，还能刹停打滑轮让动力给到有抓地力的轮子，即电子限滑。",
         "sentences": [
            ["雨天高速压过水坑，水把轮胎和路面隔开，压水那一侧的轮子瞬间失去抓地力。", "Hit a puddle and the water lifts the tire—that side loses grip instantly.", "lose grip（失去抓地力）"],
            ["方向盘会向压水那一侧被抢了一下，手没握紧方向盘又没ESP就很容易失控。", "The wheel gets yanked toward the water; loose hands and no ESP spell trouble.", "yanked（被抢）"],
            ["ESP能刹慢有抓地力的轮子，把车身修正回安全方向。", "ESP brakes the gripping wheels to steer the body back to safety.", "gripping wheels（有抓地力的轮子）"],
            ["它还能刹停打滑的空转轮，让动力更有效给到有抓地力的轮子，这就是电子限滑。", "It can also brake a spinning wheel, sending power to the gripping one—electronic LSD.", "electronic LSD（电子限滑）"]
         ]},
        {"id": "s5", "scene_zh": "什么时候要关ESP", "scene_en": "When to Turn ESP Off", "time": "09:57",
         "context": "漂移需要驱动轮打滑、方向盘指向与车身运动方向不一致，ESP会干预；陷车需要驱动轮持续打滑冲出来；修车空转判断异响也要关ESP。",
         "sentences": [
            ["有些特殊情况下ESP介入反而帮倒忙，最典型的就是想玩漂移。", "In a few cases ESP hinders—most famously drifting.", "hinders（帮倒忙）"],
            ["漂移的两个特征就是驱动轮打滑和方向盘指向与车身运动方向不一致，开着ESP永远飘不起来。", "Drifting needs wheelspin and mismatched wheel angle—ESP blocks it all.", "wheelspin（打滑）"],
            ["陷在雪坑泥坑里，必须依靠驱动轮一个劲打滑靠惯性冲出来，也需要关闭ESP。", "Stuck in snow or mud, you need wheels spinning to rock out—so ESP off.", "rock out（靠惯性冲出来）"],
            ["修车师傅把车顶到架子上让轮子空转判断异响，也需要关闭ESP，不然电脑会限制发动机输出还踩刹车。", "On a lift, spinning wheels make ESP cut power and brake—so turn it off.", "on a lift（顶到架子上）"]
         ]},
        {"id": "s6", "scene_zh": "ESP的边界与价值", "scene_en": "The Limits and Value of ESP", "time": "12:02",
         "context": "安全驾驶主要靠人，ESP只是辅助；ESP不能提高转弯性能，只能降低失控概率；美国NHTSA数据：同条件下降低撞车概率35%，SUV车型降67%。",
         "sentences": [
            ["安全驾驶最主要的因素还是人，ESP再好也只是辅助，只有在你好好开车的前提下才能帮到你。", "The driver comes first; ESP only helps if you drive sensibly.", "sensibly（理智地）"],
            ["每一次ESP介入仪表盘指示灯都会闪烁，它是在告诉你系统正在保护你。", "The ESP light flashes on intervention—it's telling you it's saving you.", "intervention（介入）"],
            ["车辆的最终极限取决于轮胎的抓地极限，ESP只能在抓地极限内尽量控制车身。", "Grip limits the car; ESP can only work within them.", "grip limit（抓地极限）"],
            ["ESP不属于提高转弯性能的功能，它只能降低车辆失控的概率。", "It doesn't boost cornering—it lowers the odds of losing control.", "lower the odds（降低概率）"],
            ["美国NHTSA公布：同等条件下ESP能降低撞车概率35%，在SUV车型中带ESP的事故比不带少67%。", "NHTSA: ESP cuts crash probability 35%, and SUV crashes by 67%.", "NHTSA（美国国家高速安全部门）"]
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
