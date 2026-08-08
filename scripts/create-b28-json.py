#!/usr/bin/env python3
"""批28：为10篇小红书视频生成完整场景英译JSON（旅行转场/运镜/相机噪点）。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

ARTICLES = {}

ARTICLES["travel-10-transitions"] = {
    "title_zh": "1分钟学会10种旅行神级转场！",
    "title_en": "10 Pro Travel Transitions in 1 Minute",
    "duration": "1分22秒",
    "topic": "摄影 · 运镜转场",
    "scenes": [
        {"id": "s1", "scene_zh": "动作匹配转场：无脑但精髓", "scene_en": "Action-Match Cut: Dumb-Simple Yet Core", "time": "00:00",
         "context": "出门旅行无论如何都要先拍一个的走路转场。只要会拍这个就搞懂了动作匹配的精髓：在想拍的每个场景里做相同的动作，把它们串联起来，剪辑时仔细把左右角的动作连接好。",
         "sentences": [
            ["走路转场是旅行中最无脑的处理方法。", "A walking match cut is the most brainless travel trick.", "match cut（动作匹配）"],
            ["在每个场景里做相同动作，再串联起来。", "Repeat the same move in every scene, then stitch them together.", "stitch（串联）"],
            ["剪辑时把左右角的动作连接好，画面会特别丝滑。", "Match the action at the edit point and it flows beautifully.", "edit point（剪辑点）"]
         ]},
        {"id": "s2", "scene_zh": "转身回头转场", "scene_en": "The Turn-and-Look-Back Cut", "time": "00:19",
         "context": "霸道总裁爱上我之转身回头：拍摄人物往前走时转过头的瞬间，把不同画面拼起来。可以在此基础上利用视觉逻辑转场：第一个镜头拍人物擦肩而过，第二个镜头拍另一个人物往前走转身回头，就像是和初恋擦肩而过的样子，非常有宿命感。",
         "sentences": [
            ["拍摄人物往前走时转过来的那一瞬间，拼起不同画面。", "Film the moment they turn while walking, then join different shots.", "turn（转身）"],
            ["第一个镜头拍人物擦肩而过，第二个镜头拍转身回头。", "Shot one: someone brushes past. Shot two: another turns back.", "brush past（擦肩而过）"],
            ["就像和初恋擦肩而过，非常宿命感。", "It reads like passing your first love—pure destiny.", "destiny（宿命感）"]
         ]},
        {"id": "s3", "scene_zh": "躺平转场", "scene_en": "The Lie-Down Transition", "time": "00:42",
         "context": "用视觉逻辑做更有创意的办法：躺平转场。如果不小心迟到了，就可以一秒钟从酒店转场到下一个地点的床上。细节在于躺下方向与下一个镜头的运动方向完全一致。",
         "sentences": [
            ["不小心迟到了，就可以一秒钟从酒店转场到异地。", "Running late? Cut from the hotel bed to anywhere in one second.", "cut（转场）"],
            ["躺下方向和下一个镜头的运动方向完全一致。", "The fall direction matches the next shot's motion.", "motion direction（运动方向）"],
            ["只要动作连续，大脑就来不及反应。", "As long as the motion flows, your brain fills in the gap.", "fill in（脑补）"]
         ]},
        {"id": "s4", "scene_zh": "室内外同构图转场", "scene_en": "Indoor-Outdoor Match Transition", "time": "00:55",
         "context": "只要转个身就可以从室内直接转到室外，因为两个画面的动作和构图完全一致。这种丝滑感类似电影中的蒙太奇：即使前后镜头完全不同，只要画面带有相似的情绪、相似的运镜或动作，都可以骗过大脑。",
         "sentences": [
            ["转个身就能从室内转到室外，因为构图和动作完全一致。", "A turn takes you indoors to outdoors when composition and motion match.", "composition（构图）"],
            ["这有点像是电影里的蒙太奇。", "It's close to montage in film.", "montage（蒙太奇）"],
            ["只要画面有相似的情绪或动作，就能骗过大脑丝滑转场。", "Similar mood or motion in different shots fools the brain into a smooth cut.", "smooth cut（丝滑转场）"]
         ]}
    ]
}

ARTICLES["travel-7-camera-moves"] = {
    "title_zh": "120秒学会7种旅拍神级运镜",
    "title_en": "7 Pro Travel Camera Moves in 120 Seconds",
    "duration": "2分31秒",
    "topic": "摄影 · 运镜",
    "scenes": [
        {"id": "s1", "scene_zh": "自拍拉远：意外感", "scene_en": "Pull-Back Selfie: The Surprise", "time": "00:00",
         "context": "自拍时突然把镜头拉远，配合人物回头瞬间向后运镜，会获得绝美效果并自然创造意外的感觉。秘诀就是让人物用手扶着镜头往前走，在它回头的一瞬间向后运镜。",
         "sentences": [
            ["自拍的时候突然把镜头拉远。", "Pull the lens back suddenly while self-shooting.", "pull back（拉远）"],
            ["让人物扶着镜头往前走，回头瞬间向后运镜。", "Have them push the lens as they walk; when they turn, glide backward.", "glide（滑动运镜）"],
            ["这样会获得绝美效果，还自然带出意外的感觉。", "It looks stunning and naturally adds surprise.", "surprise（意外感）"]
         ]},
        {"id": "s2", "scene_zh": "遮挡物无缝转场", "scene_en": "Obstacle Transition: Seamless", "time": "00:24",
         "context": "找一个合适的遮挡物：第一个画面遮挡物作为结尾，第二个画面从遮挡物出来开始运镜，创造出丝滑的无缝转场。可以拿旧电话或老板的电脑当道具。",
         "sentences": [
            ["第一个画面遮挡物作为结尾，第二个画面从遮挡物出来。", "End shot one on an obstacle; start shot two emerging from it.", "obstacle（遮挡物）"],
            ["这样就会创造出丝滑的无缝转场。", "That gives you a seamless, silky transition.", "seamless（无缝的）"],
            ["拿旧电话或老板的电脑当道具就行。", "Props can be an old phone or your boss's laptop.", "prop（道具）"]
         ]},
        {"id": "s3", "scene_zh": "站着不动：希区柯克变焦", "scene_en": "Standing Still: Hitchcock Zoom", "time": "00:48",
         "context": "有没有种站着不动就可以出片的方法？那就是希区柯克式变焦：让人物站着不动，通过改变镜头与人物之间的距离，创造像时间凝固般的经典画面。",
         "sentences": [
            ["站着不动怎么出片？就是希区柯克式变焦。", "Can't move? That's the Hitchcock dolly zoom.", "dolly zoom（希区柯克变焦）"],
            ["通过改变镜头和人物的距离，创造时间凝固的感觉。", "Changing the camera-subject distance freezes time.", "freeze time（时间凝固）"]
         ]},
        {"id": "s4", "scene_zh": "环绕运镜", "scene_en": "The Orbit Around", "time": "00:52",
         "context": "流笔版的片中转场：让一个人物站在画面中间，每次都绕着它转一圈拍摄，再把小片段拼接。运镜小tips：拍摄时提前打开三分线，每次把人物放在正中间，保证构图一致。",
         "sentences": [
            ["让人物站在画面中间，每次绕着它转一圈拍摄。", "Keep the subject centered and orbit a full circle each time.", "orbit（环绕）"],
            ["把拍好的小片段拼接起来就可以了。", "Stitch the small clips together.", "clip（片段）"],
            ["提前打开三分线，人物放正中间，保证构图一致。", "Turn on the rule of thirds and center the subject for consistent framing.", "rule of thirds（三分线）"]
         ]},
        {"id": "s5", "scene_zh": "设备与稳定性", "scene_en": "Gear and Stability", "time": "01:49",
         "context": "旅拍常用设备是微单加稳定器，比较常用的是索尼ZV-E1和DJI RS4系列。拍摄运镜转场时搭配稳定器保证画面稳定，RS4的追踪模块可以用于第三视角拍摄。",
         "sentences": [
            ["一般就是微单加上稳定器。", "Usually a mirrorless camera plus a gimbal.", "gimbal（稳定器）"],
            ["常用设备是索尼ZV-E1，拍摄效果绝了。", "The Sony ZV-E1 is a go-to and looks amazing.", "go-to（常用款）"],
            ["运镜转场都搭配稳定器保证画面稳定。", "Pair every move with a gimbal for stability.", "stability（稳定性）"]
         ]}
    ]
}

ARTICLES["yunjing-rs4mini-tips"] = {
    "title_zh": "不会运镜？普通人拍好视频只差这一步！",
    "title_en": "Can't Do Camera Moves? One Step Away",
    "duration": "2分31秒",
    "topic": "摄影 · 运镜",
    "scenes": [
        {"id": "s1", "scene_zh": "第一步：先拍风景再出人物", "scene_en": "Step 1: Scene First, Subject Second", "time": "00:00",
         "context": "固定机位拍多了没意思。用最简单的运镜让画面丰富起来：先推运镜拍景色，然后让人物出场，或把镜头向后拉先拍到环境再带出人物。用这个思路特别适合放在视频开场或结尾，非常有电影感。",
         "sentences": [
            ["把相机固定住按下快门，拍多了就没意思了。", "Locked-off shots get boring fast.", "locked-off（固定机位）"],
            ["先推运镜拍景色，然后让人物出场。", "Push in on the scenery, then reveal the subject.", "push in（前推）"],
            ["这个思路放在开场或结尾，非常有电影感。", "It works great as an opening or closer—very cinematic.", "cinematic（电影感）"]
         ]},
        {"id": "s2", "scene_zh": "第二步：环绕镜头", "scene_en": "Step 2: The Orbit Shot", "time": "00:46",
         "context": "出门旅游一定要拍一个环绕镜头：让人物靠在某个地方，从全景环绕拍摄到近景。细节：人物注视的方向可以跟摄影师一起移动，这样拍起来就很自然。",
         "sentences": [
            ["让人物靠在某处，从全景环绕拍到近景。", "Have them lean somewhere and orbit from wide to close.", "orbit（环绕）"],
            ["人物注视方向跟着摄影师一起移动，拍出来很自然。", "Let their gaze follow the camera for a natural look.", "gaze（注视方向）"]
         ]},
        {"id": "s3", "scene_zh": "格莱美运镜：转身反向运镜", "scene_en": "The Grammy Move: Turn and Counter-Move", "time": "00:57",
         "context": "用环绕的方法给拍摄格莱美运镜，这个运镜每年都会火。秘诀就是当人物转身的时候，镜头需要朝相反的方向向人物运镜，一个画面就创造出一种张力，非常有氛围感。",
         "sentences": [
            ["格莱美运镜每年都会火，谁拍谁火。", "The Grammy move goes viral every year.", "viral（走红）"],
            ["人物转身的时候，镜头朝相反方向运镜。", "As the subject turns, glide the camera the opposite way.", "opposite direction（相反方向）"],
            ["一个画面就创造出张力，非常有氛围感。", "One shot creates tension and atmosphere.", "tension（张力）"]
         ]},
        {"id": "s4", "scene_zh": "第三步：组合运镜", "scene_en": "Step 3: Combine the Basics", "time": "00:14",
         "context": "运镜不要太老实。所有运镜都建立在推拉摇移四种移动之上，在这个基础上做小组合：比如最喜欢的万物皆可摇镜头，用下摇加前推运镜从天空拍到人物，或者先跟随人物再上摇把目光从人物转移到景色。",
         "sentences": [
            ["所有运镜都建立在推拉摇移四种移动之上。", "Every move builds on push, pull, pan and tilt.", "pan and tilt（摇与移）"],
            ["下摇加前推，就能从天空拍到人物。", "Tilt down and push in to go from sky to subject.", "tilt down（下摇）"],
            ["先跟随人物再上摇，把目光从人物转移到景色。", "Follow the subject, then tilt up to move the eye to the scenery.", "transfer the eye（转移目光）"]
         ]},
        {"id": "s5", "scene_zh": "一个人自拍：智能追踪", "scene_en": "Solo Shooting: Smart Tracking", "time": "01:38",
         "context": "一个人去自拍可以把稳定器当成可以自动摇镜头的三脚架。RS4 mini的智能追踪模块只要比个手势就能锁定人物自动环绕运镜，人物在十米之内都能保持追踪，一个人也能拍出跟拍效果。",
         "sentences": [
            ["一个人自拍，把稳定器当成自动摇镜头的三脚架。", "Solo? Turn the gimbal into an auto-panning tripod.", "auto-panning（自动摇镜头）"],
            ["比个手势就能锁定人物，自动环绕运镜。", "A simple gesture locks the subject and auto-orbits.", "gesture（手势）"],
            ["人物在十米之内都能保持追踪。", "Tracking holds within ten meters.", "tracking（追踪）"]
         ]},
        {"id": "s6", "scene_zh": "设备参数与收尾", "scene_en": "Specs and Wrap-Up", "time": "02:16",
         "context": "RS4 mini裸机890克、承重2000克，主流的微单搭配24-70 F2.8都没问题，还有自动轴锁。新手旅拍运镜可以无脑去卷它。",
         "sentences": [
            ["裸机890克，承重2000克。", "890 grams bare, 2000 grams payload.", "payload（承重）"],
            ["主流微单搭配24-70 F2.8都没问题。", "Mainstream mirrorless with a 24-70 f/2.8 is no problem.", "mirrorless（微单）"],
            ["新手旅拍运镜可以无脑选它。", "Beginners can blindly pick it for travel moves.", "blindly pick（无脑选）"]
         ]}
    ]
}

ARTICLES["pocket4p-4-transitions"] = {
    "title_zh": "榨干口袋电影机！OP4P必学的4个神级转场",
    "title_en": "4 God-Tier Transitions for the Pocket 4P",
    "duration": "3分50秒",
    "topic": "摄影 · 运镜转场",
    "scenes": [
        {"id": "s1", "scene_zh": "第一种：下班转场", "scene_en": "1. The Off-Work Transition", "time": "00:26",
         "context": "Pocket 4P整机仅230克，轻松装进口袋，自带专业稳定器级别的丝滑云台。下班转场：在公司楼下拿一份绝密文件，用20mm广角镜头等人物跑过来向后运镜，文件飞过来时顺势遮住镜头达到黑场效果。",
         "sentences": [
            ["整机仅230克，轻松穿进口袋。", "At just 230 grams it slips right into your pocket.", "pocketable（便携的）"],
            ["用20毫米广角，等人跑过来就向后运镜。", "Shoot wide at 20mm, let them run in, then dolly back.", "dolly back（向后运镜）"],
            ["文件飞过来时顺势遮住镜头，达到黑场效果。", "As the file flies past, cover the lens for a blackout.", "blackout（黑场）"]
         ]},
        {"id": "s2", "scene_zh": "60mm中焦的压缩感", "scene_en": "The 60mm Compression", "time": "00:51",
         "context": "重点在第二个画面拍出绝美氛围感：换60mm中焦镜头。相比20mm广角，60mm带来明显的空间压缩感，用它拍人就像拍微单，是拍出好看人像的关键。站位上先与人物平行，用包包或头发遮住镜头，人物向前走时顺势转到身后继续跟随。",
         "sentences": [
            ["60毫米中焦带来明显的空间压缩感。", "60mm gives obvious spatial compression.", "spatial compression（空间压缩感）"],
            ["用它拍人，直接给你一种拍微单的感觉。", "Shooting people with it feels like a full-frame mirrorless.", "full-frame（全画幅）"],
            ["先与人物平行，用包包遮住镜头再转到身后。", "Start parallel, block with the bag, then swing behind.", "swing behind（转到身后）"]
         ]},
        {"id": "s3", "scene_zh": "第二种：敲击转场", "scene_en": "2. The Knock Transition", "time": "00:24",
         "context": "敲击转场把三个画面组合在一起，灵魂是中间那个超广角画面。换上超广角镜头配件，焦距从20mm变成16mm。第一个画面从天空摇下来，然后敲击镜头；拍第二个画面时设置4K/240帧，人物敲击镜头后迅速后退扔出文件，再摸镜头让画面变黑；第三个画面换到最终场景。",
         "sentences": [
            ["敲击转场要三个画面组合，灵魂是超广角那一帧。", "The knock cut needs three shots, and the ultra-wide one is the soul.", "knock（敲击）"],
            ["换上配件焦距从20变成16毫米。", "With the accessory the focal length drops from 20 to 16mm.", "focal length（焦距）"],
            ["第二画面设置4K/240帧，敲完迅速后退。", "Shoot the middle at 4K/240fps and step back fast.", "slow motion（慢动作）"]
         ]},
        {"id": "s4", "scene_zh": "第三种：摔倒转场", "scene_en": "3. The Fall Transition", "time": "00:17",
         "context": "摔倒转场太有活人感。把云台设置成PV模式，机头跟手随意摇摆。第一个画面运镜到旁边的东西上，第二个画面是重头戏：提前打开P4P的低感光盖，记录17档动态范围，相当于电影机的后期调色空间，非常适合拍氛围感大光比画面。",
         "sentences": [
            ["把云台设置成PV模式，机头跟你随意摇摆。", "Set the gimbal to PV mode so the head sways with your hand.", "PV mode（PV模式）"],
            ["提前打开低感光盖，记录17档动态范围。", "Open the low-light cover early for 17 stops of dynamic range.", "dynamic range（动态范围）"],
            ["相当于电影机的后期调色空间，适合拍氛围感。", "It's like a cinema camera's grading headroom—great for mood.", "grading（调色）"]
         ]},
        {"id": "s5", "scene_zh": "第四种：相似动作转场", "scene_en": "4. The Match-Action Cut", "time": "00:03",
         "context": "非常简单的相似动作转场：用60mm中焦，向后运镜的同时能涡轮化，等待回头看你手的瞬间转到下一个画面，然后继续向前走。",
         "sentences": [
            ["用60毫米中焦，向后运镜的同时能涡轮化。", "Use the 60mm and zoom in while dollying back.", "dolly-zoom（涡轮变焦）"],
            ["等待回头看你手的瞬间，转到下一个画面。", "Wait for the turn and cut to the next shot.", "turn（回头）"]
         ]},
        {"id": "s6", "scene_zh": "P4P的小心得", "scene_en": "Little Takeaways on the 4P", "time": "03:18",
         "context": "心得分享：它有双摄，从3倍变成12倍变焦，这种画面特别适合放综艺Vlog。还有一个小配件，不仅自拍可以构图，别人给你拍时还可以检查角度好不好看，女生肯定人手一个。",
         "sentences": [
            ["双摄从3倍变成12倍变焦，适合综艺Vlog。", "Dual lenses give 3x to 12x zoom—great for variety vlogs.", "variety vlog（综艺Vlog）"],
            ["小配件不仅能自拍构图，还能检查别人给你拍的构图。", "The tiny accessory helps frame selfies and check shots of you.", "check the frame（检查构图）"],
            ["以后我们经常带着它出门。", "We'll be taking it out a lot from now on.", "take it out（带出门）"]
         ]}
    ]
}

ARTICLES["travel-transition-4tips"] = {
    "title_zh": "运镜+转场❗4个组合技巧让旅拍轻松出片！",
    "title_en": "4 Camera-Move + Transition Combos for Travel",
    "duration": "2分59秒",
    "topic": "摄影 · 运镜转场",
    "scenes": [
        {"id": "s1", "scene_zh": "第一种：人为制造擦肩而过", "scene_en": "1. Fake the Brush-Past", "time": "00:18",
         "context": "人为制造出一切擦肩而过：先前推镜头慢慢靠近人物，快到人物肩膀时旋转运镜，下一个画面从肩膀转过来，把镜头向后拉就好了。",
         "sentences": [
            ["先前推镜头，慢慢靠近人物。", "Push in slowly toward the person.", "push in（前推）"],
            ["快到肩膀时旋转运镜，下一个画面从肩膀转过来。", "Rotate near the shoulder, then cut to turning from behind it.", "rotate（旋转）"],
            ["把镜头向后拉就好了。", "Then just pull the shot back.", "pull back（后拉）"]
         ]},
        {"id": "s2", "scene_zh": "第二种：躺平转场", "scene_en": "2. The Lie-Down Cut", "time": "00:30",
         "context": "躺平转场反差越大越惊艳。第一个画面躺下时镜头顺势拍到旁边的遮挡物（摄影背包），再从遮挡物开始向相同方向继续运镜。记住：风景越美就越好拍，非常有氛围感。",
         "sentences": [
            ["躺平转场，反差越大就越惊艳。", "The lie-down cut gets better with bigger contrast.", "contrast（反差）"],
            ["躺下时顺势拍到旁边的遮挡物。", "As you lie down, let the shot land on a blocking prop.", "blocking prop（遮挡物）"],
            ["从遮挡物开始，向相同方向继续运镜。", "Start from the prop and keep moving the same way.", "same direction（同方向）"]
         ]},
        {"id": "s3", "scene_zh": "第三种：走路转场", "scene_en": "3. The Walking Cut", "time": "00:59",
         "context": "最被大家低估的是走路转场，真的非常简单，随便拍一拍都能出片。运镜时需要保持人物在画面中间，可以打开相机里的三分线辅助构图，只需要不同场景拍摄朋友走路的视频，再把它们剪辑接起来。",
         "sentences": [
            ["走路转场非常简单，随便拍都能出片。", "The walking cut is simple and always works.", "walking cut（走路转场）"],
            ["保持人物在画面中间，打开三分线辅助构图。", "Center the subject and use the rule of thirds.", "rule of thirds（三分线）"],
            ["不同场景拍走路视频，再剪辑接起来。", "Film walking in different scenes and join them.", "join（拼接）"]
         ]},
        {"id": "s4", "scene_zh": "第四种：相似动作转场", "scene_en": "4. The Match-Action Cut", "time": "01:18",
         "context": "拍完走路转场后顺便拍一个相似动作转场：第一个画面随意地敲入架腿，然后用同样的构图做相似的动作，一个相似动作的转场就出来了。如果想更松弛，也不用追求动作贴合，只要画面之间有相似性就都可以转场。",
         "sentences": [
            ["第一个画面随意地敲入架腿，再用同样构图做相似动作。", "Kick casually in shot one, then repeat a similar move in the same framing.", "similar move（相似动作）"],
            ["一个相似动作的转场就这样出来了。", "And just like that you have a match-action cut.", "match-action（相似动作）"],
            ["只要画面之间有相似性，就都可以转场。", "Any visual similarity can carry a transition.", "similarity（相似性）"]
         ]},
        {"id": "s5", "scene_zh": "设备小分享", "scene_en": "Gear Notes", "time": "01:35",
         "context": "设备小分享：口袋机拍第三视角，主力机型是索尼ZV-E1，配24mm和24-70两颗镜头。智能追踪模块可以吸在稳定器上追踪自己，升级后还能追踪物体，滑动屏幕即可触发追踪；电动踢弧配件可以直接在踢弧操作稳定器，别的稳定器都没有。",
         "sentences": [
            ["主力机型是索尼ZV-E1，配24毫米和24-70两颗镜头。", "The main body is the Sony ZV-E1 with 24mm and 24-70 lenses.", "main body（主力机型）"],
            ["智能追踪模块吸在稳定器上，就能追踪自己。", "The tracking module attaches to the gimbal to track yourself.", "tracking module（追踪模块）"],
            ["电动踢弧配件，可以不用手操作稳定器。", "The powered handle controls the gimbal hands-free.", "hands-free（免手操作）"]
         ]}
    ]
}

ARTICLES["action-cam-vlog-5-tips"] = {
    "title_zh": "运动相机正确打开方式！5个技巧拍出有趣vlog",
    "title_en": "5 Tricks to Make Your Action-Cam Vlog Fun",
    "duration": "2分08秒",
    "topic": "摄影 · Vlog",
    "scenes": [
        {"id": "s1", "scene_zh": "磁吸第一人称视角", "scene_en": "Magnetic First-Person Views", "time": "00:07",
         "context": "用运动相机的磁吸功能拍出神奇的第一视角：在笔杆上粘贴细铁石就能拍一只笔的第一视角；同理磁吸在菜刀上拍菜刀的第一人称视角。比较晃的话记得双手扶住。",
         "sentences": [
            ["在笔杆上粘两块细铁石，就能拍笔的第一视角。", "Tape magnets to a pen and film its first-person view.", "first-person view（第一视角）"],
            ["同理磁吸在菜刀上，拍菜刀的第一人称视角。", "Stick it on a knife for a knife's-eye view.", "knife's-eye view（菜刀视角）"],
            ["如果比较晃的话，记得双手扶住。", "If it gets shaky, hold it with both hands.", "shaky（晃动）"]
         ]},
        {"id": "s2", "scene_zh": "第三人称的新奇视角", "scene_en": "Third-Person Surprises", "time": "00:28",
         "context": "拍Vlog也要第三人称视角的素材：把相机放在平时放不到的地方带来新奇感，比如放在门上来拍过场画面，吸附在油烟机附近拍做饭视角，零下20度也能埋进雪地里让观众体验雪的视角。",
         "sentences": [
            ["把相机放在平时放不到的地方，带来新奇感。", "Place the camera where it can't normally go for novelty.", "novelty（新奇感）"],
            ["放在门上来拍过场画面。", "Mount it on the door for a transition shot.", "transition shot（过场画面）"],
            ["零下20度也能埋进雪地里，让观众体验雪的视角。", "Even at -20°C you can bury it in snow for a snow's view.", "snow's view（雪的视角）"]
         ]},
        {"id": "s3", "scene_zh": "慢动作与防抖运镜", "scene_en": "Slow Motion and Stabilized Moves", "time": "00:48",
         "context": "用慢动作模式拍出有趣的画面：让切好的蔬菜缓缓落下，或放在水里洗蓝莓。运动相机这么防抖，当然要拿来运镜：把相机固定在遥控小车上，输入遇到障碍物停止的指令，一个人也能拍推拉等镜头；后期用关键帧放大可得到希区柯克变焦效果。",
         "sentences": [
            ["用慢动作模式，让切好的蔬菜缓缓落下。", "Use slow motion and let chopped veggies fall slowly.", "slow motion（慢动作）"],
            ["把相机固定在遥控小车上，一个人也能拍推拉镜头。", "Mount it on an RC car to shoot push-pull solo.", "RC car（遥控小车）"],
            ["后期用关键帧放大，得到希区柯克变焦效果。", "Scale up with keyframes in post for a dolly-zoom look.", "keyframe（关键帧）"]
         ]},
        {"id": "s4", "scene_zh": "人物跟随与防抖等级", "scene_en": "Subject Tracking and Stabilization", "time": "01:14",
         "context": "利用人物跟随功能一个人也能运镜，在家演绎人物在房间里纠结不定、来回踱步的场景。",
         "sentences": [
            ["利用人物跟随功能，一个人也能进行运镜。", "With subject tracking, one person can do dynamic moves.", "subject tracking（人物跟随）"],
            ["在家演绎人物纠结不定、来回踱步的场景。", "Recreate a pacing, conflicted scene at home.", "pace（踱步）"]
         ]},
        {"id": "s5", "scene_zh": "调色：Vlog模式与HDR", "scene_en": "Color: Vlog Mode and HDR", "time": "01:24",
         "context": "X5 Pro配备Vlog模式，色彩调整空间更大。对比背光环境原片与调色：Vlog模式确实在调色时更容易展现高光和暗部细节。不会调色想直出就用HDR 10-bit功能；用Vlog模式调色前需先色彩还原，最简单的方式是在DJI Mimo app里点色彩还原按键。",
         "sentences": [
            ["Vlog模式确实让色彩调整空间更大一些。", "Vlog mode gives you much more color-grading room.", "color grading（调色）"],
            ["调色时更容易展现高光和暗部的细节。", "It reveals highlight and shadow detail when grading.", "highlight（高光）"],
            ["用Vlog模式调色前，先做色彩还原。", "Before grading Vlog footage, do a color restore.", "color restore（色彩还原）"]
         ]}
    ]
}

ARTICLES["vlog-panorama-8-tricks"] = {
    "title_zh": "如何把日常vlog变有趣？8个全景创意玩法！",
    "title_en": "8 Panorama Tricks for Fun Daily Vlogs",
    "duration": "2分47秒",
    "topic": "摄影 · Vlog",
    "scenes": [
        {"id": "s1", "scene_zh": "特写引入人物", "scene_en": "Open With a Close-Up, Then Reveal", "time": "00:00",
         "context": "拍不出有趣Vlog是因为没有结合日常生活。先用一个特写吸引观众，再伴随物品移动引出人物。拍摄时选择全景视频，后期在DJI Mimo app手动调整视角，或直接用智能追踪让它自动完成运镜。",
         "sentences": [
            ["先用一个特写吸引观众，再伴随物品移动引出人物。", "Open on a close-up, then follow an object to reveal the person.", "close-up（特写）"],
            ["拍摄时选择全景视频。", "Shoot in panorama mode.", "panorama（全景）"],
            ["后期在App里手动调整视角，或用智能追踪自动运镜。", "Adjust the view in the app, or let smart tracking do the moves.", "smart tracking（智能追踪）"]
         ]},
        {"id": "s2", "scene_zh": "极光脚制造反差", "scene_en": "Extreme Close-Up for Contrast", "time": "00:19",
         "context": "想强调某样事物时，将它凑近相机用极光脚拍摄制造反差感。前一秒展现的信息密度越高，越能突出凑近的物品。",
         "sentences": [
            ["想强调某物时，凑近相机拍摄制造反差感。", "To emphasize something, bring it close for contrast.", "close for contrast（凑近反差）"],
            ["前一秒信息密度越高，越能突出凑近的物品。", "The denser the first shot, the more the close-up pops.", "pop（突出）"]
         ]},
        {"id": "s3", "scene_zh": "镜子与水流场景", "scene_en": "Mirrors and Water Flow", "time": "00:29",
         "context": "利用相机的全景视角拍摄镜子相关场景，不仅能后期帮助运镜，还不用担心拍到相机。洗水果时把相机夹在水流和水果中间，可以拍出非常新奇的效果。",
         "sentences": [
            ["用全景视角拍镜子场景，不用担心拍到相机。", "Use the full view for mirror scenes without catching the camera.", "mirror scene（镜子场景）"],
            ["把相机夹在水流和水果中间，拍出新奇效果。", "Wedged between the stream and fruit, it looks fresh.", "fresh look（新奇效果）"]
         ]},
        {"id": "s4", "scene_zh": "冰箱场景两种思路", "scene_en": "Two Fridge Ideas", "time": "00:40",
         "context": "冰箱场景有两种思路：一种用物品跟踪引导到人物；另一种通过开门的光亮切换到人物特写，最后用广角收尾。无论哪种都只要拍摄一次，这就是全景相机的优势。",
         "sentences": [
            ["冰箱场景：用物品跟踪引导到人物。", "Fridge idea one: track an object into the person.", "track（跟踪）"],
            ["或用开门的光亮切换人物特写，广角收尾。", "Or cut to a close-up through the door's light and end wide.", "door light（开门光亮）"],
            ["无论哪种思路，都只要拍摄一次。", "Either way, you only shoot it once.", "shoot once（一次拍完）"]
         ]},
        {"id": "s5", "scene_zh": "先环境后人物", "scene_en": "Environment First, Person Later", "time": "00:53",
         "context": "全景还能实现先环境后人物的有趣运镜。记得固定好三脚架，最好在无风的环境下进行。遇上有风或条件不允许架支架时，也可以手持拍摄：保持机身和隐形自拍杆在一条线上，杆子就会自动消失。",
         "sentences": [
            ["全景还能实现先环境后人物的运镜。", "Panorama lets you do environment-first reveals.", "reveal（引出）"],
            ["最好在无风环境下，固定好三脚架。", "Fix the tripod and shoot in windless conditions.", "tripod（三脚架）"],
            ["手持时保持机身和隐形自拍杆一条线，杆子自动消失。", "Align the body and invisible selfie stick and the stick vanishes.", "invisible stick（隐形杆）"]
         ]},
        {"id": "s6", "scene_zh": "超级夜景与单镜头模式", "scene_en": "Super Night and Single-Lens Mode", "time": "01:12",
         "context": "夜晚拍摄记得用超级夜景模式。想更随意地介绍环境和人物可以用单镜头模式，直接切换前后置镜头就能完成，切换时完全不会中断语音，也能达到先环境后人物的出场方式。",
         "sentences": [
            ["夜晚拍摄记得用超级夜景模式。", "Remember super-night mode for night shots.", "super night（超级夜景）"],
            ["单镜头模式直接切换前后置，不会中断语音。", "Single-lens mode flips front/back without cutting your voice.", "single-lens（单镜头）"],
            ["也能达到先环境后人物的出场方式。", "It also gives the environment-first reveal.", "reveal（出场方式）"]
         ]},
        {"id": "s7", "scene_zh": "第三人称甩镜转场", "scene_en": "The Third-Person Whip Transition", "time": "01:44",
         "context": "第三人称视角的转场现在一个人也能轻松拍出来：相机固定不动，开始录制一段全景视频，通过后期编辑让前后两段视频的运动方向一致。打开DJI Mimo app点击取景，模拟手持相机的动感；下一个视频顺着同样的方向甩进来，在剪辑软件一拼接就搞定了。",
         "sentences": [
            ["相机固定不动，录制一段全景视频。", "Lock the camera and record one panorama.", "lock（固定）"],
            ["后期让前后两段视频的运动方向一致。", "In post, match the motion direction of both clips.", "match motion（运动一致）"],
            ["顺着同样方向甩进来，一拼接就搞定。", "Whip in the same direction and join them in the editor.", "whip（甩镜）"]
         ]}
    ]
}

ARTICLES["cinematic-vlog-tips"] = {
    "title_zh": "如何拍出电影感vlog？节奏+质感的6个小tips",
    "title_en": "6 Tips for a Cinematic Vlog: Rhythm + Texture",
    "duration": "1分45秒",
    "topic": "摄影 · Vlog",
    "scenes": [
        {"id": "s1", "scene_zh": "法宝一：节奏——快切", "scene_en": "Weapon 1: Rhythm via Quick Cuts", "time": "00:00",
         "context": "拍出吸引人的Vlog有两个法宝：节奏和质感。加快节奏最爱用快切：在长镜头之间插入补充细节的短镜头，比如在街上四处张望后快速切换细节，再回归到自己。",
         "sentences": [
            ["两个法宝：节奏和质感。", "Two weapons: rhythm and texture.", "rhythm（节奏）"],
            ["在长镜头之间插入补充细节的短镜头。", "Insert short detail shots between longer takes.", "insert（插入）"],
            ["快速小切换后，再回归到自己。", "Quick detail cutaways, then back to the subject.", "cutaway（插镜）"]
         ]},
        {"id": "s2", "scene_zh": "丝滑运镜与防抖", "scene_en": "Smooth Moves and Stabilization", "time": "00:19",
         "context": "速度感的体现离不开丝滑的运镜。为了稳定性用运动相机并把防抖模式开到最大，这样单手操作也完全没问题。",
         "sentences": [
            ["速度感离不开丝滑的运镜。", "Speed reads through silky camera moves.", "camera move（运镜）"],
            ["把防抖模式开到最大，单手操作也没问题。", "Max out stabilization and shoot one-handed.", "stabilization（防抖）"]
         ]},
        {"id": "s3", "scene_zh": "延时拍摄与跳切", "scene_en": "Time-Lapse and Jump Cuts", "time": "00:29",
         "context": "日常出行怕画面太无聊，就用延时拍摄搭配跳切剪辑。剪辑时删掉中间片段，让节奏更紧凑，就是跳切。除此之外还喜欢用关键帧让画面慢慢放大，配上字幕画面更有深度。",
         "sentences": [
            ["怕画面无聊，就用延时拍摄搭配跳切。", "Bored shots? Pair a time-lapse with jump cuts.", "time-lapse（延时拍摄）"],
            ["剪辑时删掉中间片段，让节奏更紧凑。", "Delete the middle frames to tighten the rhythm.", "jump cut（跳切）"],
            ["用关键帧让画面慢慢放大，配上字幕更有深度。", "Slowly zoom with keyframes and add captions for depth.", "keyframe（关键帧）"]
         ]},
        {"id": "s4", "scene_zh": "移动延时与画质色调", "scene_en": "Hyper-Lapse, Quality, and Tones", "time": "00:48",
         "context": "在超市或马路拍摄试试移动延时，可以让单一的长镜不再单调、加快节奏。提升质感的话画质和色调最重要：运动相机最高能拍8K，自带滤镜库，选莱卡自然拍城市场景特别有电影感；画质越高后期分镜放大到150%、200%也不影响观感。",
         "sentences": [
            ["试试移动延时，让单一长镜不再单调。", "Try a hyper-lapse so one long shot stops feeling flat.", "hyper-lapse（移动延时）"],
            ["最高能拍8K，还自带滤镜库。", "It shoots up to 8K with built-in LUTs.", "LUT（滤镜库）"],
            ["放大到150%、200%也不影响观感。", "You can crop 150-200% without losing quality.", "crop（裁切）"]
         ]},
        {"id": "s5", "scene_zh": "陌生化处理", "scene_en": "Making It Strange", "time": "00:12",
         "context": "透过玻璃拍摄能营造陌生感，很适合上帝视角叙事；这里还结合了跳切表现时光流逝。也可以利用水来做陌生化处理，能拍出特殊的光影。",
         "sentences": [
            ["透过玻璃拍摄能营造陌生感。", "Shooting through glass creates defamiliarization.", "defamiliarization（陌生化）"],
            ["结合跳切表现时光流逝。", "Pair it with jump cuts to show time passing.", "time passing（时光流逝）"],
            ["利用水拍出特殊的光影。", "Use water for special light and shadow.", "water（水）"]
         ]},
        {"id": "s6", "scene_zh": "伪装成蓝莓的相机", "scene_en": "The Camera Disguised as a Blueberry", "time": "01:28",
         "context": "如果相机够小巧，就把它塞进盒子里伪装成一颗蓝莓，然后让它静静地躺在水底，借助蓝莓的自由落体完成一个梦幻的转场。",
         "sentences": [
            ["相机够小巧，就塞进盒子里伪装成蓝莓。", "If it's tiny, hide it in a box and disguise it as a blueberry.", "disguise（伪装）"],
            ["让它静静地躺在水底。", "Let it rest quietly at the bottom.", "rest（静躺）"],
            ["借助蓝莓的自由落体，完成梦幻转场。", "Use the berry's fall for a dreamy transition.", "free fall（自由落体）"]
         ]}
    ]
}

ARTICLES["high-iso-less-noise"] = {
    "title_zh": "高ISO噪点少？",
    "title_en": "Does High ISO Really Mean More Noise?",
    "duration": "3分09秒",
    "topic": "摄影 · 相机知识",
    "scenes": [
        {"id": "s1", "scene_zh": "高ISO与噪点的直觉", "scene_en": "The Intuition About High ISO", "time": "00:00",
         "context": "说到高ISO，很多人的印象就是造点多，从结果导向来看这非常正确。但这里容易忽略一个问题：怎么比较？暗光下噪声高是因为进光量不足，导致有效信号减少。",
         "sentences": [
            ["说到高ISO，很多人的印象就是噪点多。", "High ISO has a bad rap for more noise.", "ISO（感光度）"],
            ["从结果导向看，这非常正确。", "By results, that's absolutely right.", "results-oriented（结果导向）"],
            ["暗光下噪声高，是因为进光量不足、有效信号减少。", "Noise rises in low light because less light means less signal.", "effective signal（有效信号）"]
         ]},
        {"id": "s2", "scene_zh": "等亮度对比：高ISO反而更好", "scene_en": "Same Brightness: High ISO Wins", "time": "00:20",
         "context": "如果只是高低ISO画面直接对比，结果显而易见。但把低ISO拍摄的画面后期提亮到相同水平时发现：噪声表现竟然差别不大，甚至高ISO画面还要稍微好一点。",
         "sentences": [
            ["直接对比高低ISO，结果显而易见。", "A direct ISO comparison seems obvious.", "direct comparison（直接对比）"],
            ["把低ISO画面后期提亮到相同水平，噪声差别不大。", "Brighten the low-ISO shot to match and noise is about the same.", "brighten（提亮）"],
            ["甚至高ISO画面还要稍微好一点。", "The high-ISO shot is even slightly cleaner.", "slightly cleaner（略干净）"]
         ]},
        {"id": "s3", "scene_zh": "为什么：电压放大4倍", "scene_en": "Why: 4x Voltage Gain", "time": "00:35",
         "context": "当进光量确定时，散粒噪声与前端读出噪声的信噪比也就确定了。相比基准ISO 100，用ISO 400可以让电压直接放大4倍，ADC接收更高的电压摆幅，信号的量化精度更高，还能压制PGA与ADC之间的后端读出噪声。",
         "sentences": [
            ["进光量确定时，散粒噪声与前端读出噪声的信噪比也就确定了。", "With light fixed, the shot-noise to read-noise ratio is set.", "shot noise（散粒噪声）"],
            ["用ISO 400可以让电压直接放大4倍。", "At ISO 400 the voltage is amplified 4x.", "amplify（放大）"],
            ["还能压制PGA与ADC之间的后端读出噪声。", "It also suppresses back-end read noise.", "back-end read noise（后端读出噪声）"]
         ]},
        {"id": "s4", "scene_zh": "高ISO画面噪声反而更少", "scene_en": "High ISO Ends Up With Less Noise", "time": "00:57",
         "context": "从ISO 400画面看确实比ISO 100噪声更多，因为散粒噪声和前端读出噪声都放大了4倍。但把ISO 100提亮到相同水平时，会把散粒噪声、前端读出噪声和后端读出噪声都放大4倍。在同一亮度水平对比，高ISO画面的噪声反而比低ISO的少一点，少的正是后端读出噪声。",
         "sentences": [
            ["ISO 400的画面比ISO 100的噪声更多。", "ISO 400 looks noisier than ISO 100 at first glance.", "noisier（更噪）"],
            ["但提亮ISO 100时，三类噪声都被放大了4倍。", "But brightening ISO 100 amplifies all three noise types 4x.", "amplify（放大）"],
            ["同一亮度下，高ISO反而噪声更少。", "At equal brightness, high ISO is actually quieter.", "quieter（更安静）"]
         ]},
        {"id": "s5", "scene_zh": "ISO不变性与取舍", "scene_en": "ISO Invariance and Trade-Offs", "time": "01:36",
         "context": "暗光环境是不是就可以无脑提高ISO了？那倒也不是。现阶段很多相机对读出噪声的抑制都很优秀，后端读出噪声占比更小，高ISO收益并不明显，这就是常说的ISO不变性。实际应用中还要考虑动态范围，需要根据创作环境与意图做取舍。",
         "sentences": [
            ["暗光环境下可以无脑提高ISO吗？那倒也不是。", "Can you blindly crank ISO in low light? Not quite.", "blindly crank（无脑提高）"],
            ["相机对读出噪声抑制优秀，高ISO收益不明显，就是ISO不变性。", "Strong read-noise control makes high ISO pointless—that's ISO invariance.", "ISO invariance（ISO不变性）"],
            ["还要考虑动态范围，根据创作意图做取舍。", "Mind dynamic range and choose by intent.", "dynamic range（动态范围）"]
         ]},
        {"id": "s6", "scene_zh": "结论：掌控平衡", "scene_en": "The Lesson: Master Balance", "time": "02:12",
         "context": "光线不足只想提亮画面拍清主体、对动态范围没要求，就可以大胆提升ISO，既能拍到合适亮度还能赚一点信噪比。光比较大想保留高光细节就用基准ISO保证动态范围。ISO高低没有绝对的好坏，真正要掌控的是平衡：曝光、景深、动态模糊、信噪比、动态范围。",
         "sentences": [
            ["只想提亮画面拍清主体，就可以大胆提升ISO。", "If you just need brightness on the subject, raise ISO boldly.", "boldly（大胆地）"],
            ["光比较大想保留高光细节，就用基准ISO。", "High-contrast scenes wanting highlight detail call for base ISO.", "base ISO（基准ISO）"],
            ["ISO没有绝对好坏，真正要掌控的是平衡。", "ISO isn't good or bad—what matters is balance.", "balance（平衡）"]
         ]}
    ]
}

ARTICLES["image-noise-snr"] = {
    "title_zh": "画面为什么有噪点？",
    "title_en": "Why Does Your Image Have Noise?",
    "duration": "2分25秒",
    "topic": "摄影 · 相机知识",
    "scenes": [
        {"id": "s1", "scene_zh": "噪点的本质", "scene_en": "What Noise Is", "time": "00:00",
         "context": "画面中烦人的噪点在电子信号处理领域被称为噪声。噪声的出现是因为信号在采集、传输、转换和量化过程中都存在一定误差，无法完全规避。这些误差导致像素不能精确显示原本的亮度和色度值，造成像素之间波动、过度不均。",
         "sentences": [
            ["画面中烦人的噪点，在信号处理领域叫噪声。", "Those annoying specks are called noise in signal processing.", "noise（噪声）"],
            ["信号在采集、传输、转换和量化中都有误差。", "Every stage—capture, transfer, convert, quantize—adds error.", "quantize（量化）"],
            ["误差导致像素之间的亮度色度波动。", "Errors make pixels fluctuate in brightness and color.", "fluctuate（波动）"]
         ]},
        {"id": "s2", "scene_zh": "噪声的类型", "scene_en": "Types of Noise", "time": "00:27",
         "context": "噪声的类型有很多：传感器内硅基材料因热激发形成的自由电子汇聚成暗电流；制造公差导致的像素个体光敏差异引发非均匀性噪声。但大部分噪声在日常拍摄中影响都很小，存在感较强的是散粒噪声和读出噪声。",
         "sentences": [
            ["热激发的自由电子汇聚成暗电流。", "Thermally excited electrons pool into dark current.", "dark current（暗电流）"],
            ["制造公差导致像素个体光敏差异。", "Manufacturing tolerances make pixels differ in sensitivity.", "tolerance（公差）"],
            ["日常影响大的主要是散粒噪声和读出噪声。", "The big two in practice are shot noise and read noise.", "shot noise（散粒噪声）"]
         ]},
        {"id": "s3", "scene_zh": "散粒噪声", "scene_en": "Shot Noise Explained", "time": "00:49",
         "context": "理想情况下每个像素接受相同数量的光子，但现实中光子传播离散随机波动，导致每个像素在相同时间内接受的光子数量并不完全一致，由此引发的误差就是散粒噪声。暗光环境光子很少，微小误差在信号中占比很高，信噪比低、画质下降。",
         "sentences": [
            ["光子的传播离散随机，每个像素接到的光子数不完全一致。", "Photons arrive randomly, so pixels catch uneven numbers of them.", "photon（光子）"],
            ["由此引发的误差就是散粒噪声。", "That fluctuation is shot noise.", "shot noise（散粒噪声）"],
            ["暗光下光子少，信噪比低，画质下降。", "Few photons in the dark mean a low SNR and worse quality.", "signal-to-noise ratio（信噪比）"]
         ]},
        {"id": "s4", "scene_zh": "提升信噪比：向右曝光", "scene_en": "Raise SNR: Expose to the Right", "time": "01:19",
         "context": "随着光子数量增加，散粒噪声也增加，但有效信号的增加比率更大，信噪比显著提升。所以提升信噪比的最优点是在不过曝的前提下增加进光量，这也是为什么要向右曝光的根本原因。",
         "sentences": [
            ["光子增多时，信号增加比率大于噪声。", "More photons grow the signal faster than the noise.", "signal grows faster（信号增加更快）"],
            ["信噪比显著提升，画质更好。", "SNR rises sharply and quality improves.", "SNR（信噪比）"],
            ["提升信噪比最优点：不过曝的前提下增加进光量。", "The best SNR boost is more light without clipping.", "without clipping（不过曝）"],
            ["这就是为什么向右曝光。", "That's exactly why you expose to the right.", "expose to the right（向右曝光）"]
         ]},
        {"id": "s5", "scene_zh": "前端与后端读出噪声", "scene_en": "Front-End and Back-End Read Noise", "time": "01:36",
         "context": "信号在读出链路各环节都会引入噪声。浮动扩散节点和源极跟随器的噪声相对固定，与信号强弱和曝光时长无关，是制约动态范围下限的关键因素。提高ISO时TG对电压信号进行模拟放大，同步放大前端读出噪声；PGA和ADC本身引发的噪声不随ISO改变，叫后端读出噪声。",
         "sentences": [
            ["浮动扩散节点和源极跟随器的噪声相对固定。", "Floating diffusion and source-follower noise is fairly fixed.", "floating diffusion（浮动扩散）"],
            ["提高ISO会同步放大前端读出噪声。", "Raising ISO amplifies front-end read noise too.", "front-end read noise（前端读出噪声）"],
            ["PGA和ADC的噪声不随ISO改变，叫后端读出噪声。", "PGA/ADC noise is ISO-independent—that's back-end read noise.", "back-end（后端）"]
         ]},
        {"id": "s6", "scene_zh": "信噪比的意义", "scene_en": "What SNR Means", "time": "02:07",
         "context": "不管什么类型的噪声都没人喜欢，我们想要的是纯净的信号也就是光。把它们放在一起就有了信噪比，这个比值越高表示有效信号越强，画面纯净观感舒适；反之画质粗糙观感下降。",
         "sentences": [
            ["我们想要的只是纯净的信号，也就是光。", "All we want is clean signal—the light itself.", "clean signal（纯净信号）"],
            ["信噪比越高，有效信号越强。", "A higher SNR means stronger signal.", "stronger（更强）"],
            ["画面纯净观感舒适，反之画质粗糙。", "Clean images feel great; low SNR looks rough.", "rough（粗糙）"]
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
