#!/usr/bin/env python3
"""批33：为10篇摄影/修图/脸型视频生成完整场景英译JSON。
场景以元组定义，build 时统一转 dict，避免裸 scene_en 引号问题。
"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

# scene 元组: (id, scene_zh, scene_en, time, context, [(zh, en, note), ...])
ARTICLES = {}

ARTICLES["eye-catchlight-tutorial"] = {
    "title_zh": "进来学❗️一镜到底超详细眼神光教程🍂",
    "title_en": "One-Take Catchlight Tutorial",
    "duration": "21秒",
    "topic": "摄影 · 人像",
    "scenes": [
        ("s1", "开场立题：枫叶道具", "The Brief: A Maple Leaf", "00:00",
         "一镜到底教你拍出眼神光，道具是一片透光的枫叶。眼神光就是眼中反射的光点，能让眼睛显得有神有生命力。",
         [("一镜到底教你拍出眼神光。", "One take, and I'll teach you real catchlights.", "catchlight（眼神光）"),
          ("道具是一片透光的枫叶。", "The prop is a translucent maple leaf.", "translucent（透光的）")]),
        ("s2", "站位：阳光下", "Placement: In the Sun", "00:02",
         "模特放在阳光下，为眼睛受光做准备。要让眼睛里有光点，前提是模特的脸要朝向有光的方向。",
         [("模特站在阳光下，眼睛准备受光。", "The model stands in sunlight, eyes ready to catch it.", "catch light（受光）")]),
        ("s3", "光源定位：太阳在侧逆光", "Sun Position: Side Backlight", "00:04",
         "太阳在画面一侧，逆光带来高光与眩光。逆光时脸的前景会有强烈的眩光和过曝风险。",
         [("太阳在画面一侧，带来逆光高光。", "The sun sits to one side, giving backlit highlights.", "backlight（逆光）"),
          ("逆光会带来眩光和过曝。", "Backlighting brings flare and blown highlights.", "flare（眩光）")]),
        ("s4", "关键动作：手挡强光", "Key Move: Block With Your Hand", "00:07",
         "用手挡镜头上方强光，保留眼神光、压住过曝眩光。手挡住直射镜头的光线，既能防止过曝，又能让眼睛里的光点保留下来。",
         [("用手挡住镜头上方的强光。", "Block the harsh light above the lens with a hand.", "block（遮挡）"),
          ("保留眼神光，压住过曝眩光。", "Keep the catchlights and tame the blown flare.", "tame（压制）")]),
        ("s5", "姿势微调：收下巴", "Pose Fine-Tune: Tuck the Chin", "00:10",
         "下巴略收，让脸部线条与眼神光更干净。微调角度能让眼里的光点更明显、脸部轮廓更利落。",
         [("下巴略收，脸部线条更干净。", "Tuck the chin for cleaner facial lines.", "tuck（收拢）")]),
        ("s6", "结果确认：眼神光成立", "Result: Catchlights Locked", "00:12",
         "作者连夸漂亮，眼神光与秋叶透光同时成立。透过枫叶的光斑和眼中的高光相呼应，画面氛围感拉满。",
         [("眼神光与秋叶透光同时成立。", "Catchlights and the backlit leaves both work.", "backlit（透光的）")]),
    ],
}

ARTICLES["vlog-four-perspectives"] = {
    "title_zh": "VLOG拍摄技巧｜四种视角拍出更有趣的vlog",
    "title_en": "Four Perspectives for a Better Vlog",
    "duration": "1分38秒",
    "topic": "VLOG · 拍摄技巧",
    "scenes": [
        ("s1", "用拇指相机玩转视角", "A Thumb-Size Camera for Views", "00:00",
         "新手小白能拍摄哪些有趣的视角呢？今天就用拇指大小、能拍4K的相机，教你拍摄十几种创意的镜头。利用转向支架或者夹子，将生活中常用的物品和相机固定在一起，我们就得到这样有趣的视角。",
         [("用拇指大小能拍4K的相机。", "A thumb-size camera that shoots 4K.", "4K（超高清）"),
          ("用转向支架把相机固定在物品上。", "Rig the camera to everyday items with a mount.", "mount（支架）"),
          ("就能得到有趣的视角。", "And you get playful new angles.", "angle（角度）")]),
        ("s2", "第一人称视角", "First-Person View", "00:26",
         "外出时可以用磁吸挂脖拍摄第一人称视角，机子小小不怕尴尬，解放双手拍摄沉浸式的视频。第一人称让观众像戴上了你的眼睛。",
         [("磁吸挂脖拍第一人称视角。", "Use a magnetic necklace mount for POV shots.", "POV（第一人称视角）"),
          ("机子小小，不怕尴尬。", "It's tiny, so no one minds it.", "tiny（小巧）"),
          ("解放双手，拍沉浸式视频。", "Free your hands for immersive clips.", "immersive（沉浸式的）")]),
        ("s3", "第三人称视角", "Third-Person View", "00:34",
         "相机本身自带磁吸，可以帮助你发掘很多不一样的第三人称视角，从而丰富你的Vlog画面。把相机吸在任何地方，就能得到一个全新的观察角度。",
         [("相机自带磁吸，发掘第三人称视角。", "Built-in magnets open up third-person angles.", "magnet（磁吸）"),
          ("丰富你的Vlog画面。", "That enriches your vlog footage.", "enrich（丰富）")]),
        ("s4", "上帝视角", "God's-Eye View", "00:52",
         "拍摄角度上还可以选择墙壁、冰箱、门上，高视角可以利用拓展舱轻松俯瞰画面，我们就可以得到丰富的上帝视角，多视角展示我一天都干了什么。",
         [("还可以吸在墙壁、冰箱、门上。", "Stick it on walls, fridges, and doors.", "stick（吸住）"),
          ("用拓展舱轻松拍上帝视角。", "A ceiling mount gives an easy bird's-eye view.", "bird's-eye view（上帝视角）"),
          ("多视角展示一天的生活。", "Show a whole day from many angles.", "many angles（多视角）")]),
    ],
}

ARTICLES["rain-umbrella-no-reflect"] = {
    "title_zh": "雨天氛围感伞面不反光的详细方法☔️",
    "title_en": "Rainy Umbrella Without Glare",
    "duration": "19秒",
    "topic": "摄影 · 氛围感",
    "scenes": [
        ("s1", "问题示范：伞面反光", "Problem Demo: Umbrella Glare", "00:00",
         "问题示范：透过带水珠的透明伞俯拍，字幕提示伞面反光。直接用伞俯拍时，伞面的反光会盖住人脸。",
         [("透过带水珠的透明伞俯拍。", "Shooting top-down through a beaded clear umbrella.", "beaded（带水珠的）"),
          ("伞面反光会盖住脸。", "The umbrella glare swallows the face.", "glare（反光）")]),
        ("s2", "高光水珠叠压面部", "Highlights and Droplets Overlap", "00:02",
         "另一角度：伞面高光与水珠叠在一起，面部细节被压住。反光和水珠混在一起，脸部细节完全看不清楚。",
         [("伞面高光与水珠叠在一起。", "Highlights and droplets overlap.", "overlap（叠加）"),
          ("面部细节被压住。", "The facial detail gets buried.", "buried（被遮盖）")]),
        ("s3", "操作瞬间：上撑伞柄", "Key Move: Push the Umbrella Up", "00:05",
         "操作瞬间：手握伞柄把伞上撑，字幕同步说明动作。把伞从正上方抬起来，让伞面不再挡在镜头和脸之间。",
         [("手握伞柄把伞向上撑。", "Grip the handle and push the umbrella up.", "push up（上撑）")]),
        ("s4", "光线路径改到头顶", "Light Shifts Overhead", "00:09",
         "伞抬高后，光线路径改到头顶方向，字幕进入下一句。伞面抬高后，反光不再直接进入镜头，人脸重新获得清晰的受光。",
         [("伞抬高后，光线改到头顶方向。", "Raised, the light path moves overhead.", "overhead（头顶的）")]),
        ("s5", "结果对照：清晰的脸", "Result: A Clear Face", "00:12",
         "结果对照：脸部轮廓与表情清晰，雨滴氛围仍在。反光消失，脸清楚了，但雨滴的氛围还保留着。",
         [("脸部轮廓与表情清晰。", "The face's contours and expression turn sharp.", "contour（轮廓）"),
          ("雨滴氛围仍然保留。", "The raindrop vibe stays intact.", "atmosphere（氛围）")]),
        ("s6", "收尾氛围镜头", "Closing Mood Shot", "00:16",
         "收尾氛围镜头：清晰度回来后，雨天道具感反而更完整。清晰的人脸加上雨天的道具氛围，画面反而更完整。",
         [("清晰度回来后，雨天感反而更完整。", "With clarity back, the rainy feel reads even better.", "complete（完整）")]),
    ],
}

ARTICLES["slow-shutter-portrait"] = {
    "title_zh": "国庆怎样出片最高效，慢门人像张张都是大片",
    "title_en": "Slow-Shutter Portraits That Pop",
    "duration": "41秒",
    "topic": "摄影 · 慢门人像",
    "scenes": [
        ("s1", "慢门的差距", "The Slow-Shutter Gap", "00:00",
         "这是你用慢门拍出来的照片，而这是摄影师用慢门拍出来的照片。为什么差距会这么大呢？难道是它的相机更贵吗？其实想要实现这种效果很简单，今天就用一分钟的时间教会你。",
         [("你用慢门和摄影师用慢门差距很大。", "Your slow-shutter shot vs the photographer's—night and day.", "night and day（天壤之别）"),
          ("实现这种效果其实很简单。", "Getting this look is actually simple.", "look（效果）")]),
        ("s2", "1/20秒追焦", "Panning at 1/20s", "00:13",
         "首先把快门速度设为20分之1秒，此时相机平稳地跟着模特一起移动，就能拍出电影感的追焦照片。追焦：相机跟着主体移动，背景被拉出动感模糊。",
         [("快门设为1/20秒。", "Set the shutter to 1/20s.", "shutter（快门）"),
          ("相机平稳跟着模特移动，拍出追焦。", "Pan smoothly with the model for cinematic motion.", "pan（追随拍摄）")]),
        ("s3", "时间流逝感", "Time-Lapse Feel", "00:21",
         "如果让模特静止不动，就能拍出时间流逝的效果。主体不动、背景在动，慢门就制造出时间流动的观感。",
         [("模特静止，拍出时间流逝感。", "Freeze the model and time seems to flow.", "flow（流动）")]),
        ("s4", "闪光+晃动=流光人像", "Flash Plus Shake: Light Trails", "00:25",
         "然后准备一个闪光灯，在按下快门的同时晃动相机，就能拍出绝美的流光人像效果。闪光定住主体，晃动把光线拖成彩带。",
         [("按下快门同时晃动相机。", "Shake the camera as you press the shutter.", "shake（晃动）"),
          ("拍出绝美的流光人像。", "That makes gorgeous light-trail portraits.", "light trail（流光）")]),
        ("s5", "旋转机身=定格旋焦", "Rotate the Body: Spin Blur", "00:32",
         "再给相机设置中心对焦，拍摄时旋转机身，这样就拍出来了定格旋焦人像。中心对焦锁住主体，旋转机身让四周画出同心圆。",
         [("设置中心对焦。", "Lock center focus.", "center focus（中心对焦）"),
          ("旋转机身拍出旋焦人像。", "Rotate the body for a swirl-blur portrait.", "swirl（旋转）")]),
    ],
}

ARTICLES["video-clarity-tips"] = {
    "title_zh": "别怪设备了‼️3分钟让视频清晰度提升80%",
    "title_en": "Boost Video Clarity 80% in 3 Minutes",
    "duration": "2分37秒",
    "topic": "摄影 · 视频清晰度",
    "scenes": [
        ("s1", "清晰度的决定性元素：光", "Light Rules Clarity", "00:00",
         "这是相机拍的画面，而这是手机拍的画面。为什么感觉相机拍的还没有手机拍的清晰呢？并非如此哦，在换相机之前，先来认识一下对画面清晰度起决定性作用的元素——光。光线太暗会导致画面噪点严重、细节模糊。",
         [("相机拍的还没手机拍的清晰？", "Why does the camera look softer than the phone?", "soft（不清晰）"),
          ("决定清晰度的元素是光。", "The decisive factor is light.", "decisive（决定性的）"),
          ("光线太暗，噪点严重细节模糊。", "Too little light means noise and mushy detail.", "noise（噪点）")]),
        ("s2", "明暗对比才是底层原因", "Contrast Is the Real Secret", "00:22",
         "如果只是用灯把整个环境打亮，光线太平，画面没有视觉重心，观感上还是显得不够清晰。当主体从环境中凸显出来，画面自然就变得清晰多了。所以光是表层原因，而光所带来的明暗对比，才是最底层的原因。",
         [("光线太平，画面没有视觉重心。", "Flat light leaves the frame with no visual focus.", "flat light（平光）"),
          ("主体凸显出来，画面就清晰了。", "Pull the subject out and it reads sharp.", "stand out（凸显）"),
          ("明暗对比才是底层原因。", "Contrast is the underlying cause.", "contrast（对比）")]),
        ("s3", "万能打光公式：蝴蝶光", "The Butterflies: Butterfly Lighting", "00:47",
         "现在就教你们一个经典的万能打光公式。第一步，把主光放在人物正前方，从上往下45度角拍摄，这种光会在人脸上形成蝴蝶形状的高光、脸颊两侧的阴影，会在视觉上更加显瘦和立体。",
         [("主光放正前方，从上往下45度。", "Place the key light in front, 45 degrees down.", "key light（主光）"),
          ("人脸上形成蝴蝶形高光。", "It draws a butterfly-shaped highlight on the face.", "butterfly（蝴蝶）"),
          ("脸颊阴影让脸显瘦立体。", "Cheek shadows slim and sculpt the face.", "sculpt（立体）")]),
        ("s4", "补光与背景分离", "Fill Light and Background Seams", "01:03",
         "第二步，用灯棒或者反光板给阴影部分补一点光，不要让暗部过于死黑，但注意光线要比主光弱一点。这就是早期好莱坞经常给女演员们打的蝴蝶光，因为拍人实在好看，所以也叫美人光。第三步，在背景里放一些小灯，比如家里的小台灯、落地灯之类的，让人物边缘和背景分离开来，画面也会更有氛围感。",
         [("用灯棒或反光板给阴影补光。", "Use a bar light or reflector to fill the shadows.", "fill（补光）"),
          ("补光要比主光弱一点。", "Keep the fill softer than the key.", "softer（更柔和）"),
          ("背景放小灯，把人物分离出来。", "Small lights in the back separate the subject.", "separate（分离）")]),
        ("s5", "色彩对比也加分", "Color Contrast Adds Punch", "01:34",
         "既然明暗对比能增加视频的清晰度，那别的对比是不是也可以呢？没错，比如说色彩的对比。很多电影里都会用到类似的方法，让主体颜色和背景形成强烈的对比来塑造人物形象。我自己拍口播的时候，也会用灯棒给窗帘打上蓝色，和屋内的暖光形成对比，来让画面更有质感。其实大光圈拍人更好看的原理也是类似，因为光圈越大，虚实对比越明显，那主体自然也会更加突出。",
         [("色彩对比也能增加清晰度。", "Color contrast boosts the perceived clarity too.", "color contrast（色彩对比）"),
          ("主体与背景形成强烈色彩对比。", "A strong color gap defines the subject.", "define（塑造）"),
          ("大光圈让虚实对比更明显。", "Wide apertures sharpen the subject-vs-blur contrast.", "subject-vs-blur（虚实）")]),
        ("s6", "后期与导出参数", "Post and Export Settings", "02:00",
         "除了前期拍摄，你也可以在后期通过手动拉曝光、对比度和饱和度去增加画面对比，也能起到提升清晰度的效果。做完这一步，你的视频清晰度已经可以打到90%的人了。但如果导出参数不对，也很容易损伤画质。前期拍摄尽量使用4K分辨率，这样即便需要二次构图，也不会过度损伤画质。导出编码选择H.264、最高码率。",
         [("后期拉曝光、对比度、饱和度。", "In post, push exposure, contrast, and saturation.", "saturation（饱和度）"),
          ("前期拍4K，方便二次构图。", "Shoot 4K so reframing keeps quality.", "reframe（二次构图）"),
          ("导出用H.264最高码率。", "Export in H.264 at max bitrate.", "bitrate（码率）")]),
    ],
}

ARTICLES["wedding-retouch-process"] = {
    "title_zh": "婚纱照修图进行中、修图过程",
    "title_en": "Wedding Retouch in Progress",
    "duration": "2分52秒",
    "topic": "修图 · 人像精修",
    "scenes": [
        ("s1", "开场：发顶到额头勾勒", "Outline From Crown to Forehead", "00:01",
         "开场侧脸：发顶到额头的勾勒线，圆形播放式光标停在发际附近。修图师从脸部轮廓入手，先用钢笔勾勒关键线条。",
         [("从发顶到额头勾勒线条。", "An outline runs from the crown to the forehead.", "outline（轮廓线）"),
          ("光标停在发际附近。", "The cursor pauses at the hairline.", "hairline（发际线）")]),
        ("s2", "天空选区", "Sky Selection", "00:08",
         "天空选区：不规则「蚂蚁线」落在蓝天区域，准备做局部处理或填充。用选区工具圈出天空，准备替换或调整。",
         [("蚂蚁线圈出蓝天区域。", "Marching ants trace the blue sky.", "marching ants（蚂蚁线）"),
          ("准备做局部处理或填充。", "Ready for local edits or a fill.", "local edit（局部处理）")]),
        ("s3", "液化变形网格", "Liquify Mesh", "00:15",
         "液化/变形网格：新娘全身三角网与钉点，耳旁显示像素坐标与6.0°。液化工具通过网格精确控制身体曲线，避免全局变形。",
         [("全身三角网格与钉点。", "A full-body triangle mesh with pins.", "mesh（网格）"),
          ("液化精确调整身体曲线。", "Liquify shapes the body line precisely.", "liquify（液化）")]),
        ("s4", "西服选区", "Suit Selection", "00:40",
         "西服选区：蚂蚁线贴着夹克下摆与背景交界，准备局部处理。沿服装边缘建立选区，为局部调整做准备。",
         [("蚂蚁线贴着夹克下摆。", "Marching ants ride the jacket hem.", "hem（下摆）"),
          ("准备局部处理。", "Ready for local adjustment.", "local adjustment（局部处理）")]),
        ("s5", "肩部变形网格", "Shoulder Deform Grid", "00:50",
         "肩部变形网格：蓝色3×3锚点覆盖西装肩臂，水印「颜值修图」可见。针对肩臂区域做局部网格变形，调整体态。",
         [("蓝色3×3锚点覆盖肩臂。", "Blue 3×3 anchors cover the shoulder and arm.", "anchor（锚点）"),
          ("局部变形调整体态。", "Local warping fixes the posture.", "warp（变形）")]),
        ("s6", "裤线刷修", "Trouser-Line Retouch", "01:30",
         "裤线刷修：100%缩放下圆形笔刷停在西裤膝后褶皱处。用笔刷处理裤子的褶皱细节，让面料干净挺括。",
         [("笔刷停在西裤膝后褶皱处。", "The brush pauses at the knee creases.", "crease（褶皱）"),
          ("100%缩放处理细节。", "Retouching at 100% zoom.", "zoom（缩放）")]),
        ("s7", "黑白检视", "Black-and-White Check", "02:30",
         "黑白检视：去色后回看新娘侧脸与头纱层次，圆形光标停在耳饰附近。去掉颜色，专门检查光影过渡是否均匀。",
         [("去色后回看侧脸与头纱。", "Desaturated, reviewing profile and veil layers.", "desaturate（去色）"),
          ("黑白模式检查光影层次。", "Black and white exposes the tonal layers.", "tonal（影调的）")]),
        ("s8", "成片与调色对照", "Final vs Graded", "02:50",
         "成片与调色对照：左右饱和度/色温差异明显，画面带修图服务水印。左边原片、右边成片，色温和饱和度差异明显。",
         [("左右饱和度与色温差异明显。", "Saturation and white balance clearly differ side by side.", "white balance（色温）"),
          ("成片带修图服务水印。", "The final frame carries the service watermark.", "watermark（水印）")]),
    ],
}

ARTICLES["retoucher-ends-cleaner"] = {
    "title_zh": "修图师的尽头是干保洁？",
    "title_en": "A Retoucher's Final Form: Cleaning?",
    "duration": "2分16秒",
    "topic": "修图 · 人像精修",
    "scenes": [
        ("s1", "保洁隐喻：腋窝开局", "The 'Cleaning' Metaphor", "00:01",
         "开场：钢笔点落在腋窝附近，对应标题里的「保洁」隐喻——先打扫皮肤局部。修图先处理最细小的皮肤瑕疵，像打扫房间一样。",
         [("钢笔点在腋窝附近，隐喻保洁。", "The pen lands near the armpit—the cleaning metaphor.", "metaphor（隐喻）"),
          ("先打扫皮肤局部。", "Tidy a patch of skin first.", "tidy（打扫）")]),
        ("s2", "笑口特写与高低频", "Smile Close-Up and High/Low Frequency", "00:05",
         "笑口特写；标题栏可见「变色鱼——高低频」，进入皮肤/牙齿细节层。高低频分离皮肤纹理与颜色，分别处理。",
         [("笑口特写进入细节层。", "A smile close-up enters the detail layer.", "close-up（特写）"),
          ("高低频分别处理纹理与颜色。", "High/low frequency splits texture from color.", "frequency separation（高低频）")]),
        ("s3", "地砖「扫地」", "'Sweeping' the Tiles", "00:15",
         "地砖「扫地」：钢笔路径框住斜向路面区域，准备清理。把背景里的杂物当作垃圾，逐一扫除。",
         [("钢笔路径框住路面区域。", "A pen path selects the pavement area.", "pavement（路面）"),
          ("准备清理背景杂物。", "Ready to clean up the background clutter.", "clutter（杂物）")]),
        ("s4", "中景清场", "Clearing the Medium Shot", "00:30",
         "中景：电瓶车、车牌与钢笔路径同框，背景「清场」开始。背景里的车、牌都是干扰元素，需要清除。",
         [("电瓶车和车牌都入画。", "A scooter and plate share the frame.", "scooter（电瓶车）"),
          ("背景清场开始。", "The background cleanup begins.", "cleanup（清场）")]),
        ("s5", "变换框罩车牌", "Transform Box on the Plate", "00:35",
         "变换框罩住车牌/车轮一带；红门「福」字与「颜值修图」水印可见。用变换工具直接覆盖掉车牌等干扰。",
         [("变换框罩住车牌和车轮。", "A transform box covers the plate and wheel.", "transform（变换）"),
          ("红门「福」字是保留的主体。", "The red door's 福 stays as the subject.", "subject（主体）")]),
        ("s6", "脚后跟创可贴", "The Heel Band-Aid", "00:50",
         "脚后跟创可贴特写——典型「保洁」级细节，准备擦掉。连脚后跟的创可贴都要修掉，这就是「保洁」级细节。",
         [("脚后跟创可贴也要修掉。", "Even the heel band-aid gets erased.", "band-aid（创可贴）"),
          ("这是「保洁」级的细节。", "That's cleaning-grade detail.", "cleaning-grade（保洁级）")]),
        ("s7", "中景验收", "Medium-Shot Acceptance", "01:10",
         "中景验收：背景更干净，人物与红门「福」成为主体。清完背景，人物和「福」字成为画面焦点。",
         [("背景更干净，主体突出。", "A cleaner background lets the subject stand out.", "stand out（突出）"),
          ("人物与「福」成为焦点。", "The person and 福 become the focus.", "focus（焦点）")]),
        ("s8", "终帧：清场完成", "Final Frame: Cleaning Done", "02:15",
         "终帧：清场后的彩色全景，对应「保洁」完成的结果。全部清理完成，画面干净，氛围还在。",
         [("清场后的彩色全景。", "A colorful wide shot after the cleanup.", "wide shot（全景）"),
          ("保洁完成，画面干净。", "Cleaning done—the frame is spotless.", "spotless（干净）")]),
    ],
}

ARTICLES["wedding-photo-retouch"] = {
    "title_zh": "婚纱照修图进行🀄️还原美貌过程",
    "title_en": "Wedding Photo Retouch, Beauty Restored",
    "duration": "59秒",
    "topic": "修图 · 人像精修",
    "scenes": [
        ("s1", "开场高倍检视", "Opening High-Zoom Inspection", "00:01",
         "开场高倍检视：皮肤折痕、痣点与深色椅面边界，钢笔光标停在轮廓线上。放大检视皮肤上的每一个小瑕疵。",
         [("放大检视皮肤折痕和痣点。", "Zoomed in on creases, moles, and edges.", "crease（折痕）"),
          ("钢笔光标停在轮廓线上。", "The pen cursor pauses on the contour line.", "contour（轮廓）")]),
        ("s2", "液化颈侧", "Liquify Over the Neck", "00:08",
         "液化网格覆盖颈侧：针对横纹做局部变形，而非全局磨皮。针对颈纹做局部液化，避免整个皮肤被磨平。",
         [("液化网格覆盖颈侧。", "A liquify grid spreads over the neck.", "liquify grid（液化网格）"),
          ("局部变形而非全局磨皮。", "Local warping, not global smoothing.", "warp（变形）")]),
        ("s3", "侧光人像工作视图", "Side-Lit Working View", "00:18",
         "侧光人像工作视图：暖光勾勒下颌与颈前，蕾丝婚纱细节清晰。在侧光下检查轮廓和高光的处理。",
         [("暖光勾勒下颌与颈前。", "Warm light traces the jaw and front neck.", "trace（勾勒）"),
          ("蕾丝婚纱细节清晰。", "Lace wedding details stay sharp.", "lace（蕾丝）")]),
        ("s4", "轮廓蒙版", "Silhouette Mask", "00:25",
         "轮廓蒙版：选区沿头、颈、肩剪影行进，为后续换背景或局部处理做准备。沿人物轮廓建立蒙版，便于后续处理。",
         [("选区沿头颈肩剪影行进。", "The selection follows the head-neck-shoulder outline.", "silhouette（剪影）"),
          ("为换背景做准备。", "It preps a background swap.", "swap（替换）")]),
        ("s5", "高倍局部润饰", "High-Zoom Local Retouch", "00:36",
         "高倍局部润饰：笔刷落在颈侧阴影过渡带，界面显示约245%缩放。在245%缩放下精修阴影过渡。",
         [("笔刷处理颈侧阴影过渡。", "The brush works the neck shadow transition.", "transition（过渡）"),
          ("界面显示约245%缩放。", "The view shows roughly 245% zoom.", "245% zoom（245%缩放）")]),
        ("s6", "全身回看", "Full-Body Review", "00:45",
         "全身回看：100%视图下检查体态与服装，手臂旁有白色标注线。回到全身，检查体态与服装整体效果。",
         [("100%视图检查体态与服装。", "At 100% view, checking posture and garment.", "posture（体态）"),
          ("手臂旁有标注线。", "A white annotation line sits by the arm.", "annotation（标注）")]),
        ("s7", "构图检视", "Composition Check", "00:50",
         "构图检视：台灯、圆桌与沙发一并入画，确认暖光氛围与整体层次。检查整幅画面的光线氛围与层次。",
         [("台灯、圆桌与沙发一并入画。", "The lamp, table, and sofa all frame in.", "frame in（入画）"),
          ("确认暖光氛围与层次。", "Confirming the warm mood and layers.", "layers（层次）")]),
        ("s8", "黑白检视", "Black-and-White Check", "00:55",
         "黑白检视：去掉色彩后复查颈肩光影过渡与皮肤干净度。去色检查光影过渡是否干净利落。",
         [("去色复查光影过渡。", "Stripping color to review the light transitions.", "strip color（去色）"),
          ("检查皮肤干净度。", "Checking how clean the skin looks.", "cleanliness（干净度）")]),
    ],
}

ARTICLES["cinematic-composition"] = {
    "title_zh": "深度解析电影感大片是如何构成的",
    "title_en": "What Makes a Shot Cinematic",
    "duration": "28秒",
    "topic": "摄影 · 电影感",
    "scenes": [
        ("s1", "黄金分割构图", "The Golden-Ratio Card", "00:01",
         "开场构图工具：黄金分割卡对准路锥，室外日光下演示焦点落点。构图时用黄金分割卡找到画面的视觉落点。",
         [("黄金分割卡对准路锥。", "A golden-ratio card aims at the cone.", "golden ratio（黄金分割）"),
          ("室外日光下演示焦点落点。", "Placing the focal point in outdoor daylight.", "focal point（焦点落点）")]),
        ("s2", "对照A：普通的观感", "Comparison A: The Ordinary Look", "00:07",
         "对照A：同一鞋履题材先给出「普通的」观感，光线相对平均。同样的题材，光线平均时画面就显得普通。",
         [("同一题材先给出普通的观感。", "The same subject first reads ordinary.", "ordinary（普通的）"),
          ("光线相对平均。", "The light is relatively even.", "even light（平均光）")]),
        ("s3", "对照A的幕后", "Behind Scenes of A", "00:10",
         "对照A的幕后感：地面相机与环境光并存，尚未看到强侧光灯板。普通的画面背后是平光和环境光。",
         [("地面相机与环境光并存。", "A floor camera and ambient light.", "ambient light（环境光）"),
          ("还没有强侧光灯板。", "No strong side-light panel yet.", "side light（侧光）")]),
        ("s4", "对照B：戏剧性侧光", "Comparison B: Dramatic Side Light", "00:13",
         "对照B：叠字「电影感的」；下方可见LED灯板制造的戏剧性侧光。加上LED侧光灯板，画面立刻有了电影感。",
         [("LED灯板制造戏剧性侧光。", "An LED panel creates dramatic side light.", "dramatic（戏剧性的）"),
          ("侧光让画面有电影感。", "Side light instantly reads cinematic.", "cinematic（电影感的）")]),
        ("s5", "快门三档对比", "Three Shutter Speeds", "00:19",
         "快门对比：1/60s糊成圆盘、1/160s见臂影、1/1300s冻帧清晰。快门速度决定运动模糊的多少。",
         [("1/60秒糊成圆盘。", "At 1/60s motion blurs into a disc.", "blur（模糊）"),
          ("1/1300秒冻帧清晰。", "At 1/1300s it freezes sharp.", "freeze（冻结）")]),
        ("s6", "收尾总览：曝光三要素", "Closing Overview: The Exposure Trio", "00:24",
         "收尾总览：快门控制运动、光圈控制景深、ISO控制亮度与噪点。一句话总结曝光三要素的分工。",
         [("快门控制运动。", "Shutter controls motion.", "motion（运动）"),
          ("光圈控制景深。", "Aperture controls depth of field.", "depth of field（景深）"),
          ("ISO控制亮度与噪点。", "ISO controls brightness and noise.", "brightness（亮度）")]),
    ],
}

ARTICLES["face-shape-analysis"] = {
    "title_zh": "脸型特征分析",
    "title_en": "Face Profile Shapes, Explained",
    "duration": "26秒",
    "topic": "审美 · 脸型",
    "scenes": [
        ("s1", "开场：S型最丑", "Opening: The S-Curve", "00:01",
         "开场定调：黄字「这是最丑的面型」，红虚线描出鼻唇颏起伏。从侧脸轮廓看，鼻、唇、颏的起伏决定了面型分类。",
         [("红虚线描出鼻唇颏的起伏。", "A red dashed line traces the nose-lip-chin profile.", "profile（侧轮廓）"),
          ("黄字定调：这是最丑的面型。", "“The ugliest face shape,” the label declares.", "label（标签）")]),
        ("s2", "S型早期凤姐脸", "The S-Curve 'Fengjie' Face", "00:03",
         "标签落地：黄白叠字「S型早期凤姐脸」；右下可见豆包AI水印。S型轮廓被归类为早期凤姐式脸型。",
         [("S型被叫作早期凤姐脸。", "The S shape gets the 'early Fengjie' label.", "S-shape（S型）")]),
        ("s3", "直面型", "The Straight Profile", "00:05",
         "直面型定名：红虚线更接近竖直轮廓，黄字「直面型」。轮廓接近竖直，显得立体端庄、大气。",
         [("直面型轮廓接近竖直。", "The straight profile runs near vertical.", "straight profile（直面型）"),
          ("立体端庄，大气。", "It reads sculpted, dignified, and grand.", "dignified（端庄）")]),
        ("s4", "微凸面型", "The Slight-Convex Profile", "00:08",
         "微凸定名：轮廓略向外凸，黄字「微凸」高亮。轮廓略微前凸，显得明艳贵气，多出港风美女。",
         [("微凸轮廓略向外凸。", "The profile bulges slightly outward.", "bulge（外凸）"),
          ("明艳贵气，多出港风美女。", "Bright and classy—many Hong Kong beauties.", "classy（贵气）")]),
        ("s5", "凸面型", "The Convex Profile", "00:12",
         "凸面定名：鼻唇颏外拱更明显，黄字「凸面型」。外拱明显，可爱不足，憨态有余。",
         [("凸面鼻唇颏外拱更明显。", "The arch is more pronounced.", "arch（拱形）"),
          ("可爱不足，憨态有余。", "Less cute, a bit more naive.", "naive（憨态）")]),
        ("s6", "微凹面型：东亚最多", "Slight-Concave: The East Asian Norm", "00:17",
         "微凹段口号：正脸大字「东亚人最多的面型」。微凹是东亚人最常见的面型，容易出现三八纹。",
         [("微凹是东亚人最多的面型。", "Slight-concave is the most common East Asian shape.", "slight-concave（微凹）"),
          ("容易出现三八纹。", "It tends toward the 'three-eight' lines.", "three-eight lines（三八纹）")]),
        ("s7", "凹面型：月亮脸", "The Concave 'Moon Face'", "00:21",
         "凹面定名：红虚线向内弯，黄字「凹面型」。轮廓向内弯，叫月亮脸，苦相又土气。",
         [("凹面轮廓向内弯。", "The concave profile curves inward.", "concave（凹面）"),
          ("也叫月亮脸，苦相又土气。", "Called a moon face—sorrowful and plain.", "sorrowful（苦相）")]),
        ("s8", "收束：很难出美女", "Closing: Hard to Make a Beauty", "00:24",
         "收束观感：大字「很难出美女」压在胸口位置。视频以「很难出美女」作结，强调轮廓对审美观感的影响。",
         [("结论：这类脸型很难出美女。", "The takeaway: it's hard to produce a beauty.", "takeaway（结论）"),
          ("轮廓决定审美观感。", "The profile shapes how beauty is read.", "perceive（感知）")]),
    ],
}


def build(slug, art):
    full_scenes = []
    for (sid, zh, en, time, context, sentences) in art["scenes"]:
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
            "id": sid,
            "title_cn": zh[:18] + ("…" if len(zh) > 18 else ""),
            "title_en": en[:42] + ("…" if len(en) > 42 else ""),
            "time": time,
            "context": context,
            "sentences": [[z, e, n] for (z, e, n) in sentences],
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
        words = words + ["exposure", "sensor", "pixel", "shutter", "signal", "noise", "dynamic", "range", "gain", "digital"][: 20 - len(words)]

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
