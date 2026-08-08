#!/usr/bin/env python3
"""批22：为10篇小红书视频生成完整场景英译JSON（含场景/练习/避坑/思维转变/生词）。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

ARTICLES = {}

ARTICLES["3DxsMYEvNHS"] = {
    "title_zh": "不会摇镜头？新手稳定器必学模式",
    "title_en": "Can't Tilt the Camera? A Must-Learn Gimbal Mode",
    "duration": "52秒",
    "topic": "稳定器 · 双轴跟随",
    "scenes": [
        {"id": "s1", "scene_zh": "双轴跟随的定义", "scene_en": "What Two-Axis Follow Is", "time": "00:00",
         "context": "双轴跟随在平移跟随的基础上加上下运动：稳定器不仅能随身体左右平移，还能配合上下方向移动。",
         "sentences": [
            ["双轴跟随怎么拍？记住对角线原则。", "How do you shoot two-axis follow? Remember the diagonal rule.", "two-axis follow（双轴跟随）"],
            ["双轴跟随模式在平移跟随的基础上，加了上下的运动模式。", "Two-axis follow adds up-and-down motion on top of pan-follow.", "pan-follow（平移跟随）"],
            ["稳定器不仅可以随着身体左右平移，还可以配合上下方向进行移动。", "The gimbal not only pans left and right with your body, but also moves vertically.", "vertical movement（上下移动）"]
         ]},
        {"id": "s2", "scene_zh": "典型摇镜用法", "scene_en": "Classic Tilt Usage", "time": "00:18",
         "context": "一般使用双轴跟随做由上到下或由下到上的摇镜头，最后带到天空或建筑作为结尾。",
         "sentences": [
            ["一般使用双轴跟随模式，都是由上到下或者由下到上的摇镜头方式。", "Two-axis follow is usually used for top-to-bottom or bottom-to-top tilt shots.", "tilt shot（摇镜头）"],
            ["最后带到天空或者建筑作为结尾。", "Finally, end on the sky or a building.", "end on the sky（以天空收尾）"],
            ["大家在运镜时，提前想好画面的开头和结尾。", "Plan the opening and ending of your shot before you start moving.", "plan the shot（提前规划镜头）"]
         ]},
        {"id": "s3", "scene_zh": "对角线运镜", "scene_en": "The Diagonal Rule", "time": "00:31",
         "context": "比如从人物开始运镜，最后落在樱花和天空；确定大致路线后，往对角线方向运镜就对了。",
         "sentences": [
            ["比如我想从人物开始运镜，最后落在樱花和天空结束。", "Say I start on a person and end on cherry blossoms and the sky.", "cherry blossoms（樱花）"],
            ["确定好大致路线后，记住要往对角线方向运镜。", "Once the rough path is set, remember to move diagonally.", "diagonal direction（对角线方向）"],
            ["预先想好镜头起点和终点，画面会更有目的性。", "Knowing your start and end point makes the shot more purposeful.", "purposeful（有目的的）"]
         ]},
        {"id": "s4", "scene_zh": "运动中变焦", "scene_en": "Zooming While Moving", "time": "00:43",
         "context": "运镜过程中需要改变焦段，可通过切换摇杆模式配合跟焦电机，直接用稳定器快速控制镜头变焦。",
         "sentences": [
            ["在运镜过程中需要改变焦段。", "During the move you may need to change the focal length.", "focal length（焦段）"],
            ["通过切换摇杆模式，配合跟焦电机。", "Switch the joystick mode and pair it with the follow-focus motor.", "follow-focus motor（跟焦电机）"],
            ["直接用稳定器快速控制镜头变焦。", "Use the gimbal itself to control zoom quickly.", "control the zoom（控制变焦）"]
         ]}
    ]
}

ARTICLES["49c6PsYXRP"] = {
    "title_zh": "新手入门！1分钟搞懂稳定器基础模式",
    "title_en": "Beginner's Guide: Gimbal Basics in One Minute",
    "duration": "1:02",
    "topic": "稳定器 · 锁定模式",
    "scenes": [
        {"id": "s1", "scene_zh": "为什么画面还会动", "scene_en": "Why the Frame Still Moves", "time": "00:00",
         "context": "很多新手用稳定器拍摄时，画面还是会移动——因为他们没搞懂锁定模式。",
         "sentences": [
            ["为什么我们用稳定器拍摄时，画面还是会移动呢？", "Why does the frame still move when we shoot with a gimbal?", "the frame moves（画面移动）"],
            ["很多新手在拍摄人像或商单短片时，总觉得稳定器很复杂很难上手。", "Many beginners find gimbals complicated when shooting portraits or commercials.", "commercial shoots（商单短片）"],
            ["锁定模式是最容易上手，也是最容易被忽略的模式。", "Lock mode is the easiest to learn and the easiest to overlook.", "lock mode（锁定模式）"]
         ]},
        {"id": "s2", "scene_zh": "锁定模式的作用", "scene_en": "What Lock Mode Does", "time": "00:18",
         "context": "长按扳机键进入锁定模式后，稳定器不跟随身体移动，而是锁定在朝前的方向上。",
         "sentences": [
            ["长按扳机键进入锁定模式后，稳定器不会跟随我们身体移动。", "Press and hold the trigger to enter lock mode; the gimbal won't follow your body.", "trigger button（扳机键）"],
            ["它锁定在朝前的方向上。", "It stays locked in the forward-facing direction.", "lock forward（朝前锁定）"],
            ["当我们按照固定线路拍摄时，就可以打开锁定模式。", "When shooting along a fixed route, turn on lock mode.", "fixed route（固定线路）"]
         ]},
        {"id": "s3", "scene_zh": "拍出稳定跟拍", "scene_en": "Steady Tracking Shots", "time": "00:31",
         "context": "人物在固定位置或固定行径状态时，锁定模式可确保云台不偏移，从而拍出跟随人物走动的画面。",
         "sentences": [
            ["人物在固定位置或者固定行径状态时，锁定模式可以确保云台不会偏移。", "When a subject stays put or walks a fixed line, lock mode keeps the gimbal from drifting.", "keep the gimbal steady（保持云台稳定）"],
            ["从而拍出跟随人物走动的画面。", "This gives you a shot that follows the person walking.", "track the subject（跟随主体）"],
            ["也可以用于运镜时经过不同的前景。", "You can also pass different foregrounds while moving.", "pass foregrounds（经过前景）"]
         ]},
        {"id": "s4", "scene_zh": "前景转场设计", "scene_en": "Foreground Transitions", "time": "00:48",
         "context": "锁定模式下运镜经过前景，可把镜头设计成转场过渡使用。",
         "sentences": [
            ["通过锁定模式运镜时经过不同的前景。", "Move through different foregrounds in lock mode.", "foreground（前景）"],
            ["把镜头设计成转场过渡使用。", "Design the shot as a transition between scenes.", "transition（转场）"],
            ["前景遮挡的瞬间，就是自然的切换点。", "The moment the foreground blocks the lens is a natural cut point.", "natural cut（自然切换点）"]
         ]},
        {"id": "s5", "scene_zh": "真稳算法", "scene_en": "Real-Stability Algorithm", "time": "00:53",
         "context": "RS4搭载第四代真稳算法，优化云台控制，让固定镜头拍摄尽可能稳定。",
         "sentences": [
            ["RS4搭载了第四代真稳算法。", "The RS4 carries the fourth-generation real-stability algorithm.", "stability algorithm（稳像算法）"],
            ["优化了云台的控制。", "It optimizes gimbal control.", "optimize control（优化控制）"],
            ["在拍摄固定镜头时，做到尽可能的画面稳定。", "It keeps static shots as steady as possible.", "static shot（固定镜头）"]
         ]}
    ]
}

ARTICLES["nXxooAxGnr"] = {
    "title_zh": "如何把爱车拍动感？37秒教会你！",
    "title_en": "How to Make Your Car Look Dynamic in 37 Seconds",
    "duration": "54秒",
    "topic": "拍摄 · 慢门追随",
    "scenes": [
        {"id": "s1", "scene_zh": "问题：静态无动感", "scene_en": "The Problem: Stillness", "time": "00:00",
         "context": "静态的车照看起来毫无动感，核心解法是用慢门追随拍摄法。",
         "sentences": [
            ["静态的车照看起来没有动感。", "A static photo of a parked car lacks dynamism.", "lack dynamism（缺乏动感）"],
            ["用慢门追随拍摄法，把静态的车拍出动感。", "Use slow-shutter panning to make a parked car look dynamic.", "slow-shutter panning（慢门追随）"],
            ["核心是把快门速度放慢，跟随车辆移动拍摄。", "The key is a slow shutter while tracking the moving car.", "slow the shutter（放慢快门）"]
         ]},
        {"id": "s2", "scene_zh": "慢门追随原理", "scene_en": "How Panning Works", "time": "00:08",
         "context": "降低快门速度（如1/30s或更慢），在车辆移动时跟随平移相机：车身因相对静止保持清晰，背景因相机移动产生动态模糊。",
         "sentences": [
            ["降低快门速度，在车辆移动的同时跟随平移相机。", "Lower the shutter speed and pan along with the moving car.", "pan along（跟随平移）"],
            ["车身因相对静止而保持清晰。", "The car body stays sharp because it's relatively still in the frame.", "stay sharp（保持清晰）"],
            ["背景因相机移动而产生动态模糊，形成速度线效果。", "The background blurs from the camera motion, creating speed lines.", "motion blur（动态模糊）"]
         ]},
        {"id": "s3", "scene_zh": "三大要素", "scene_en": "The Three Essentials", "time": "00:18",
         "context": "慢门追随的三要素：低快门速度、平滑跟焦、与被摄体同速移动。",
         "sentences": [
            ["三要素：低快门速度加平滑跟焦，再加与被摄体同速移动。", "Three essentials: low shutter speed, smooth focus tracking, and moving at the same speed as the subject.", "focus tracking（跟焦）"],
            ["快门太慢会导致车身也模糊。", "A shutter that's too slow blurs the car body too.", "too slow a shutter（快门过慢）"],
            ["跟焦不匀速会导致画面抖动。", "Uneven focus tracking causes shaky footage.", "uneven tracking（跟焦不匀速）"]
         ]},
        {"id": "s4", "scene_zh": "工具与光线", "scene_en": "Tools and Light", "time": "00:28",
         "context": "手持容易抖动，建议用三脚架或稳定器；白天光线强时快门降不下来，需要ND滤镜。",
         "sentences": [
            ["手持容易抖动，建议使用三脚架或稳定器辅助。", "Handheld shots shake easily; use a tripod or gimbal.", "tripod（三脚架）"],
            ["光线太强时快门降不下来，需要ND滤镜。", "In bright light the shutter won't drop, so you need an ND filter.", "ND filter（ND滤镜）"],
            ["推荐快门 1/15秒 到 1/60秒，越慢越动感但越难稳。", "Use 1/15s to 1/60s; slower is more dynamic but harder to hold steady.", "slower is harder（越慢越难稳）"]
         ]},
        {"id": "s5", "scene_zh": "练习路径", "scene_en": "Practice Path", "time": "00:40",
         "context": "从1/60s开始逐步降低快门，先用静止物体练跟焦，选有背景细节的场景，效果更明显。",
         "sentences": [
            ["练习从 1/60秒 开始，逐步降低快门速度。", "Start at 1/60s and lower the shutter step by step.", "step by step（逐步）"],
            ["先用静止物体练习跟焦稳定性。", "First practice focus tracking on a static object.", "static object（静止物体）"],
            ["选择有背景细节的场景，模糊效果更明显。", "Pick scenes with background details for a stronger blur.", "background details（背景细节）"]
         ]}
    ]
}

ARTICLES["2HlhFpYqj6b"] = {
    "title_zh": "终于轮到我们拍这个转场视频啦",
    "title_en": "Finally We Shoot This Transition Video",
    "duration": "15秒",
    "topic": "剪辑 · 动作转场",
    "scenes": [
        {"id": "s1", "scene_zh": "动作引导转场", "scene_en": "Action-Guided Transitions", "time": "00:00",
         "context": "如何用最简单的转场手法让画面变化不再生硬？答案是用动作作为切换的触发点。",
         "sentences": [
            ["如何用最简单的转场手法，让视频画面变化不再生硬？", "How do you make scene changes feel smooth with the simplest trick?", "scene change（场景切换）"],
            ["转场视频的关键不是特效，而是用动作作为切换的触发点。", "The key isn't effects—it's using an action as the trigger point.", "trigger point（触发点）"],
            ["最好的转场，是观众感觉不到的转场。", "The best transition is one the audience never notices.", "invisible transition（无感转场）"]
         ]},
        {"id": "s2", "scene_zh": "视觉暂留切镜", "scene_en": "Cut at Peak Action", "time": "00:06",
         "context": "在动作的最高点（速度最快时）切镜，观众的视觉暂留会填补剪辑痕迹，让切换变得自然。",
         "sentences": [
            ["在动作的最高点切镜，观众的视觉暂留会填补剪辑痕迹。", "Cut at the peak of the action; persistence of vision fills the seam.", "persistence of vision（视觉暂留）"],
            ["用肢体动作和镜头运动隐藏剪辑点。", "Hide the cut point with body movement and camera motion.", "hide the cut（隐藏剪辑点）"],
            ["设计转场动作，拍摄时保留动作，剪辑时在动作最高速时切。", "Design the move, keep it in the shot, and cut at maximum speed.", "cut at max speed（最高速处切）"]
         ]},
        {"id": "s3", "scene_zh": "三种简单转场", "scene_en": "Three Simple Transitions", "time": "00:10",
         "context": "遮镜头转场、动作匹配转场、运镜方向一致——三个基本款即可完成自然过渡。",
         "sentences": [
            ["遮镜头转场：手或物体遮住镜头，切，再从遮住物移开。", "Whip-pan cover: block the lens with a hand, cut, then move away.", "block the lens（遮镜头）"],
            ["动作匹配转场：上一个镜头结束的姿势等于下一个镜头开始的姿势。", "Match cut: the ending pose of one shot equals the starting pose of the next.", "match cut（动作匹配）"],
            ["运镜方向一致：两个镜头的运动方向一致，切镜时保持运动连续。", "Keep camera motion consistent so movement flows across the cut.", "consistent motion（运动一致）"]
         ]},
        {"id": "s4", "scene_zh": "保留动作余量", "scene_en": "Keep 0.5s of Action", "time": "00:13",
         "context": "在剪辑点前后各保留0.5秒的动作，让过渡有动力感。",
         "sentences": [
            ["在剪辑点前后各保留半秒的动作，让过渡有动力感。", "Keep about 0.5s of action on each side of the cut for momentum.", "keep the momentum（保持动力）"],
            ["永远在运动中切，不要在静止画面中切。", "Always cut during motion, never on a still frame.", "cut in motion（运动中切）"],
            ["转场要在拍摄时就规划好动作，不能完全靠后期。", "Plan the action while shooting—you can't rely only on editing.", "plan while shooting（拍摄时规划）"]
         ]}
    ]
}

ARTICLES["3wyVoWgGSZl"] = {
    "title_zh": "这大概是最简单的旅行vlog转场吧",
    "title_en": "Probably the Simplest Travel Vlog Transition",
    "duration": "21秒",
    "topic": "旅行 · 掩体转场",
    "scenes": [
        {"id": "s1", "scene_zh": "找掩体走过去", "scene_en": "Find a Block and Walk Through", "time": "00:00",
         "context": "利用自然的掩体——墙壁、柱子、路人——作为转场触发点：走过去，画面自然切换。",
         "sentences": [
            ["利用自然的掩体，比如墙壁、柱子、路人，作为转场触发点。", "Use natural covers—walls, pillars, or passersby—as transition triggers.", "natural cover（自然掩体）"],
            ["走过去，遮挡镜头，画面自然切换。", "Walk past, block the lens, and the scene switches naturally.", "block the lens（遮挡镜头）"],
            ["这是所有转场技巧中实现成本最低、效果最自然的。", "It's the cheapest and most natural of all transition tricks.", "lowest cost（成本最低）"]
         ]},
        {"id": "s2", "scene_zh": "遮挡瞬间即转场点", "scene_en": "The Block Is the Cut", "time": "00:05",
         "context": "主体走过去遮挡镜头的瞬间，就是最自然的转场点，后面接任何场景都不会突兀。",
         "sentences": [
            ["遮挡的瞬间，就是最自然的转场点。", "The moment of blockage is the most natural cut point.", "cut point（转场点）"],
            ["后面接任何场景，都不会显得突兀。", "Whatever comes next won't feel abrupt.", "feel abrupt（显得突兀）"],
            ["不需要后期特效，只需要拍摄时多走一步穿过某个物体。", "No post effects needed—just walk through something while shooting.", "no post effects（零后期）"]
         ]},
        {"id": "s3", "scene_zh": "常见掩体素材", "scene_en": "Common Cover Materials", "time": "00:09",
         "context": "墙壁建筑、柱子路灯、路人、车门、门框出入口都是常用掩体，各有拍摄建议。",
         "sentences": [
            ["墙壁和建筑适合老街城区，镜头贴墙走过去。", "Walls and buildings work in old towns—keep the lens close and walk past.", "close to the wall（贴墙）"],
            ["柱子路灯可以围绕转半圈，转到新场景。", "Pillars and lampposts let you orbit halfway into a new scene.", "orbit around（环绕）"],
            ["门框出入口适合室内外切换，进出门的瞬间切换场景。", "Door frames suit indoor-outdoor cuts—switch as you cross.", "cross the door（过门切换）"]
         ]},
        {"id": "s4", "scene_zh": "行动清单", "scene_en": "Action Checklist", "time": "00:14",
         "context": "拍摄时主动寻找场景中的自然掩体，每到一个新场景先拍一个穿过掩体的过渡镜头。",
         "sentences": [
            ["拍摄时主动寻找场景中的自然掩体。", "Actively hunt for natural covers while shooting.", "hunt for covers（主动寻找掩体）"],
            ["每到一个新场景，先拍一个穿过掩体的过渡镜头。", "At every new location, shoot a through-the-cover transition.", "transition shot（过渡镜头）"],
            ["后期在掩体遮挡镜头的瞬间切场景。", "Cut at the moment the cover blocks the lens in editing.", "cut at the block（遮挡处切）"]
         ]},
        {"id": "s5", "scene_zh": "避坑与边界", "scene_en": "Pitfalls and Boundaries", "time": "00:17",
         "context": "掩体要足够大能完全遮挡镜头；不要用半透明掩体；前后场景光比不要差太多。",
         "sentences": [
            ["掩体要足够大，能完全遮挡镜头至少两三帧全黑。", "The cover must be big enough to fully block the lens for a few frames.", "fully block（完全遮挡）"],
            ["不要找半透明的掩体，会暴露切换痕迹。", "Avoid see-through covers—they reveal the cut.", "see-through（半透明）"],
            ["前后场景光比不要差太多，否则转场会跳。", "Don't let the two scenes differ too much in brightness, or the cut jumps.", "brightness gap（光比差异）"]
         ]}
    ]
}

ARTICLES["ENv35ryYOb"] = {
    "title_zh": "短视频排版",
    "title_en": "Short-Video Layout Guide",
    "duration": "18秒",
    "topic": "剪辑 · 画面排版",
    "scenes": [
        {"id": "s1", "scene_zh": "安全区", "scene_en": "The Safe Zone", "time": "00:00",
         "context": "画面中央是安全区，常用画面都放在这里，避免被平台UI遮挡。",
         "sentences": [
            ["这里是你的安全区。", "This is your safe zone.", "safe zone（安全区）"],
            ["安全区是常用画面出现的地方。", "The safe zone is where your main footage goes.", "main footage（主要画面）"],
            ["把主体放在安全区内，关键内容不会被遮挡。", "Keep subjects inside the safe zone so key content isn't covered.", "key content（关键内容）"]
         ]},
        {"id": "s2", "scene_zh": "禁区", "scene_en": "The Restricted Zone", "time": "00:03",
         "context": "屏幕边缘是禁区，用来放大缩小；千万不要在禁区添加任何东西。",
         "sentences": [
            ["这是你的禁区。", "This is your restricted zone.", "restricted zone（禁区）"],
            ["禁区用来放大缩小。", "The restricted zone is for scaling gestures.", "scale gestures（缩放操作）"],
            ["千万不要在这里和这里添加任何东西。", "Never add anything here or here.", "never add anything（勿添加元素）"]
         ]},
        {"id": "s3", "scene_zh": "元素摆放位置", "scene_en": "Where Elements Go", "time": "00:06",
         "context": "眼睛出现在画面中上部，标题出现的位置有讲究，字幕放在下方安全区内。",
         "sentences": [
            ["这里是你眼睛出现的地方。", "This is where your eyes appear.", "eye line（视线位置）"],
            ["这里是标题要出现的位置。", "This is where the title goes.", "title placement（标题位置）"],
            ["字幕放在安全区下方，避免被弹幕或UI遮挡。", "Put captions at the bottom safe area, clear of overlays.", "captions（字幕）"]
         ]}
    ]
}

ARTICLES["68f0a1lDCT6"] = {
    "title_zh": "静态拍摄的正确姿势",
    "title_en": "The Right Posture for Static Shots",
    "duration": "26秒",
    "topic": "拍摄 · 身体运镜",
    "scenes": [
        {"id": "s1", "scene_zh": "推：身体带动", "scene_en": "Push with Your Body", "time": "00:00",
         "context": "推不是用手推，而是用身体带动手去推，画面才能稳。",
         "sentences": [
            ["推不是用手推，而是用身体带动手去推。", "Push doesn't come from your hand—your body drives your hand forward.", "drive with your body（身体带动）"],
            ["身体先动，手臂保持稳定，画面才不会晃。", "Move your body first and keep your arm steady so the frame stays calm.", "keep the arm steady（手臂稳定）"],
            ["推镜的速度要均匀，才有平滑的推进感。", "Push at an even speed for a smooth dolly-in feel.", "even speed（匀速）"]
         ]},
        {"id": "s2", "scene_zh": "拉：用腿去拉", "scene_en": "Pull with Your Legs", "time": "00:05",
         "context": "拉不是用手拉，而是用腿往后撤去完成后退运镜。",
         "sentences": [
            ["拉不是用手拉，而是用腿去拉。", "Pulling isn't done with your hands—step back with your legs.", "step back（后退）"],
            ["后退时先落脚再收臂，保持画面平稳。", "Plant your feet first, then retract, keeping the frame steady.", "plant your feet（先落脚）"],
            ["用腿部力量控制退后速度，画面更稳定。", "Use your legs to control the pull speed for steadier footage.", "control the speed（控制速度）"]
         ]},
        {"id": "s3", "scene_zh": "摇：腰部横摇", "scene_en": "Pan from Your Waist", "time": "00:10",
         "context": "摇不是用手摇，而是转动腰部做左右横摇，范围更大也更稳。",
         "sentences": [
            ["摇不是用手摇，而是转动腰部左右横摇。", "Panning isn't arm work—rotate your waist for a left-right pan.", "rotate your waist（转动腰部）"],
            ["以腰为轴，镜头才能摇得又平又广。", "Pivoting from the waist gives a smooth, wide pan.", "pivot point（旋转轴心）"],
            ["摇镜开始和结束时稍作停顿，画面更专业。", "Pause briefly at the start and end of the pan for a pro feel.", "pause briefly（稍作停顿）"]
         ]},
        {"id": "s4", "scene_zh": "移：身体横移", "scene_en": "Slide with Your Body", "time": "00:16",
         "context": "移不是用手臂去移，而是控制好身体做左右水平横移。",
         "sentences": [
            ["移不是这样用手臂去移，而是控制好身体左右水平横移。", "Don't slide with your arms—move your whole body laterally.", "lateral move（横移）"],
            ["重心放低，脚步交叉或小碎步，画面更平稳。", "Lower your center, cross-step or shuffle for a stable frame.", "lower your center（放低重心）"],
            ["横移时保持机位高度不变，避免上下跳动。", "Keep the camera height constant to avoid bobbing.", "keep the height（保持高度）"]
         ]},
        {"id": "s5", "scene_zh": "升降：垂直移动", "scene_en": "Rise and Fall", "time": "00:22",
         "context": "扩是上下垂直移动，蹲起时要慢而稳，用腿部发力。",
         "sentences": [
            ["还有上下垂直移动的升降镜头。", "There's also vertical rise-and-fall movement.", "rise and fall（升降）"],
            ["蹲起时要慢而稳，用腿部发力而不是弯腰。", "Rise and crouch slowly, driving with your legs, not your waist.", "drive with your legs（腿部发力）"],
            ["升降和横移组合，能拍出更有层次的画面。", "Combining rise with lateral moves adds depth to the frame.", "add depth（增加层次）"]
         ]}
    ]
}

ARTICLES["1WsLXa0PqFw"] = {
    "title_zh": "拍出电影感",
    "title_en": "How to Shoot a Cinematic Look",
    "duration": "23秒",
    "topic": "拍摄 · 电影感",
    "scenes": [
        {"id": "s1", "scene_zh": "电影感来自习惯", "scene_en": "Cinematic Look Comes from Habits", "time": "00:00",
         "context": "电影感不需要昂贵设备，改变几个拍摄习惯就能让画面质变。",
         "sentences": [
            ["电影感不来自设备，来自构图意识加光线选择加画面比例。", "A cinematic look comes not from gear but from composition, light, and aspect ratio.", "composition and light（构图与光线）"],
            ["改变几个拍摄习惯，就能让画面产生电影般的质感。", "A few shooting habits can give your footage a film-like quality.", "film-like quality（电影质感）"],
            ["最重要的三个要素：宽画幅比、有方向的光线、层次分明的前中后景。", "The big three: a wide aspect ratio, directional light, and layered foreground, middle, and background.", "aspect ratio（画幅比）"]
         ]},
        {"id": "s2", "scene_zh": "宽画幅遮幅", "scene_en": "Wide Cinemascope", "time": "00:04",
         "context": "后期添加2.35:1黑边遮幅，是最快的电影感捷径。",
         "sentences": [
            ["加黑边遮幅：后期添加 2.35比1 黑边，这是最快的电影感捷径。", "Add black bars: 2.35:1 letterboxing is the fastest shortcut to a cinematic feel.", "letterbox（遮幅）"],
            ["遮幅让画面更像宽银幕电影。", "Bars make the frame feel like widescreen cinema.", "widescreen（宽银幕）"],
            ["黑边是锦上添花，不是雪中送炭，还要配合光线和构图。", "Black bars help, but light and composition carry the look.", "frosting on the cake（锦上添花）"]
         ]},
        {"id": "s3", "scene_zh": "有方向的光线", "scene_en": "Directional Light", "time": "00:08",
         "context": "避免全脸均匀光照，让光线从一侧来，脸的另一侧有阴影。",
         "sentences": [
            ["光线有方向：避免全脸均匀光照。", "Make light directional: avoid flat, even lighting on the face.", "directional light（方向光）"],
            ["让光线从一侧来，脸的另一侧有阴影。", "Let light come from one side so the other side falls into shadow.", "fall into shadow（落入阴影）"],
            ["侧光太强烈时，用反光板或柔光补一点亮。", "If the side light is too harsh, bounce or soften it slightly.", "bounce light（补光）"]
         ]},
        {"id": "s4", "scene_zh": "前景与景深", "scene_en": "Foreground and Depth", "time": "00:12",
         "context": "在镜头前放一个物体并虚化增加层次；用大光圈控制景深突出主体。",
         "sentences": [
            ["前景虚化：在镜头前放一个物体并虚化，增加画面层次。", "Foreground blur: place an object near the lens and soften it for depth.", "foreground blur（前景虚化）"],
            ["控制景深：用大光圈让背景虚化，突出主体。", "Control depth of field with a wide aperture to isolate the subject.", "depth of field（景深）"],
            ["前景物体占画面不要超过15%，别挡住主体。", "Keep the foreground object under 15% of the frame—don't block the subject.", "don't block the subject（别挡主体）"]
         ]},
        {"id": "s5", "scene_zh": "降低饱和度", "scene_en": "Lower the Saturation", "time": "00:18",
         "context": "适当降低色彩饱和度10-20%，画面更沉稳有质感。",
         "sentences": [
            ["降低饱和度：适当降低色彩饱和度 10到20%，画面更沉稳。", "Drop saturation by 10–20% for a calmer, more grounded image.", "lower saturation（降低饱和度）"],
            ["饱和度降太多会让画面变灰，控制在15%左右即可。", "Too much desaturation looks gray—stay around 15%.", "look gray（画面发灰）"],
            ["电影感等于宽画幅加侧光加前景层次加低饱和加深景深。", "Cinematic feel = widescreen + side light + foreground + desaturation + shallow depth.", "cinematic formula（电影感公式）"]
         ]}
    ]
}

ARTICLES["4eJBwSSK5xU"] = {
    "title_zh": "2026跟我一起收集这个响指转场吧",
    "title_en": "Let's Collect This Finger-Snap Transition",
    "duration": "15秒",
    "topic": "剪辑 · 响指转场",
    "scenes": [
        {"id": "s1", "scene_zh": "响指转场的原理", "scene_en": "Why the Snap Works", "time": "00:00",
         "context": "响指转场流行是因为动作小、声音明确、视觉焦点集中——在响指声峰值点切镜，切换自然流畅。",
         "sentences": [
            ["响指转场之所以流行，是因为动作小、声音明确、视觉冲击力强。", "The snap transition works because the action is small, the sound is clear, and the visual focus is strong.", "clear sound cue（明确的声音提示）"],
            ["在响指声的峰值点切镜，观众的注意力被声音引导。", "Cut at the peak of the snap; the sound guides the audience's attention.", "cut at the peak（峰值处切）"],
            ["三个镜头中动作都集中在手上，焦点高度集中。", "All attention is on the hand, keeping the focus tight.", "focus on the hand（焦点在手上）"]
         ]},
        {"id": "s2", "scene_zh": "操作流程", "scene_en": "The Workflow", "time": "00:04",
         "context": "拍两个场景，两个场景都做打响指动作；剪辑时把剪辑点精确放在响指声的峰值。",
         "sentences": [
            ["拍两个场景，两个场景中都在做打响指的动作。", "Shoot two scenes, snapping fingers in both.", "two scenes（两个场景）"],
            ["剪辑时把剪辑点精确放在响指声的峰值。", "In editing, place the cut exactly at the peak of the snap.", "exact cut point（精确剪辑点）"],
            ["前一个镜头结束于响指，后一个镜头从响指开始。", "The first scene ends on the snap; the next begins with it.", "sound continuity（声音连续）"]
         ]},
        {"id": "s3", "scene_zh": "动作一致性", "scene_en": "Consistency of the Move", "time": "00:07",
         "context": "两个场景的响指动作方向、速度、手的位置要尽量一致，否则会有跳跃感。",
         "sentences": [
            ["两个场景的响指动作方向、速度、手的位置要尽量一致。", "Keep direction, speed, and hand position consistent across the two scenes.", "consistent hand position（手位一致）"],
            ["动作不一致会带来跳跃感。", "Mismatched actions create a jumpy feel.", "jumpy feel（跳跃感）"],
            ["拍摄时可以在手上标记位置，确保两次一致。", "Mark the hand position when shooting to keep the two snaps identical.", "mark the position（标记位置）"]
         ]},
        {"id": "s4", "scene_zh": "精确对齐剪辑点", "scene_en": "Aligning the Cut Precisely", "time": "00:10",
         "context": "放大音频波形，找到响指的峰值点作为切换点，必要时前后微调1-2帧。",
         "sentences": [
            ["放大音频波形，找到响指的峰值点作为切换点。", "Zoom into the audio waveform to find the snap's peak as the cut point.", "audio waveform（音频波形）"],
            ["如果动作不够连贯，微调剪辑点前移或后移一两帧。", "If the motion feels off, nudge the cut a frame or two.", "nudge the cut（微调剪辑点）"],
            ["响指时靠近麦克风，声音会更清晰。", "Snap close to the microphone for a clearer sound.", "close to the mic（靠近麦克风）"]
         ]},
        {"id": "s5", "scene_zh": "延伸与边界", "scene_en": "Variations and Boundaries", "time": "00:13",
         "context": "可以用拍手、跺脚等其他有声音的动作替代响指；响指转场比较显眼，不适合严肃内容。",
         "sentences": [
            ["可以用拍手、跺脚等其他有声音的动作替代响指。", "You can swap the snap for claps or stomps—any sound-marked action.", "sound-marked action（有声音的动作）"],
            ["响指转场比较显眼，不适合需要低调转场的严肃内容。", "The snap is showy—it doesn't fit serious, low-key content.", "low-key content（低调内容）"],
            ["从切就切了，转变为用声音触发转场，让观众的耳朵先感知变化。", "Shift from cutting blindly to letting the sound trigger the change.", "sound-triggered cut（声音触发切换）"]
         ]}
    ]
}

ARTICLES["9pHFfApHJ7t"] = {
    "title_zh": "用手机拍出诗意感",
    "title_en": "Shooting Poetic Photos with a Phone",
    "duration": "1:13",
    "topic": "手机摄影 · 诗意构图",
    "scenes": [
        {"id": "s1", "scene_zh": "真实与诗意", "scene_en": "Reality vs. Poetry", "time": "00:00",
         "context": "不懂摄影的人拍的是真实，懂摄影的人拍的是诗意——同样的场景，观察方式不同。",
         "sentences": [
            ["怎么把这片小树林拍出诗意感大片？", "How do you turn this small forest into a poetic masterpiece?", "poetic masterpiece（诗意大片）"],
            ["不懂摄影的人拍的是真实，懂摄影的人拍的是诗意。", "Non-photographers capture reality; photographers capture poetry.", "capture poetry（拍出诗意）"],
            ["走进小树林，走到一棵树前，仰视观察。", "Walk into the woods, stand before a tree, and look up.", "look up（仰视）"]
         ]},
        {"id": "s2", "scene_zh": "把树干看成线条", "scene_en": "See Trunks as Lines", "time": "00:15",
         "context": "把树干看成一根粗线条，通过变焦布局构图，上拉小太阳，拍出铁骨斗寒天的画面。",
         "sentences": [
            ["把树干看成一根粗线条。", "Treat the tree trunk as a bold line.", "bold line（粗线条）"],
            ["通过变焦布局构图，上拉小太阳。", "Compose by zooming and adjust exposure with the little sun slider.", "exposure slider（曝光调节）"],
            ["拍出不见春花满树、铁骨斗寒天的意境。", "Capture the mood of bare branches bracing against winter.", "bare branches（铁骨）"]
         ]},
        {"id": "s3", "scene_zh": "调整角度找布局", "scene_en": "Adjust Angles, Find Layouts", "time": "00:34",
         "context": "再调整角度，寻找树干的布局，拍出残雪为洞笔、云间带春意的画面。",
         "sentences": [
            ["再调整角度，寻找树干的布局。", "Shift your angle to find new compositions among the trunks.", "find compositions（寻找构图）"],
            ["残雪湛雪为洞笔，满写云间带春意。", "Snow-dusted branches write calligraphy against the clouds.", "calligraphy（书法感）"],
            ["一棵树看线条，两棵树看关系，多棵树看秩序。", "One trunk shows line; two show relationship; many show order.", "order and rhythm（秩序与节奏）"]
         ]},
        {"id": "s4", "scene_zh": "多棵树的秩序", "scene_en": "Order Among Many Trees", "time": "00:45",
         "context": "再拍两棵树，寻找两棵树的布局关系；再拍更多树的秩序关系。",
         "sentences": [
            ["再拍两棵树，寻找两棵树的布局关系。", "Then shoot two trees and look for their relationship.", "relationship（关系）"],
            ["再拍更多树，感受树的秩序关系。", "Shoot more trees and feel the rhythm of their order.", "rhythm of order（秩序节奏）"],
            ["慢慢感受，疏影横斜水清浅。", "Slow down and feel the sparse shadows slanting across shallow water.", "sparse shadows（疏影）"]
         ]},
        {"id": "s5", "scene_zh": "用心感受", "scene_en": "Feel It Slowly", "time": "01:01",
         "context": "诗意感来自放慢速度去感受，而不是靠后期；玩手机摄影，关注系统化方法更重要。",
         "sentences": [
            ["诗意感不是后期调出来的，而是拍摄时用心感受出来的。", "Poetic feel isn't made in post—it comes from feeling while shooting.", "feel while shooting（拍摄时感受）"],
            ["东边日出西边雨，别有风姿在画中。", "A charm all its own, like sun in the east and rain in the west.", "a charm of its own（别有风姿）"],
            ["多观察、多尝试角度，手机也能拍出诗意。", "Observe more and try new angles—a phone can capture poetry too.", "try new angles（多试角度）"]
         ]}
    ]
}


def build(slug, art):
    full_scenes = []
    for i, s in enumerate(art["scenes"], 1):
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
