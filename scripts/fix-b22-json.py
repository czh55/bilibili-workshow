#!/usr/bin/env python3
"""批22：为简化场景JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "3DxsMYEvNHS": {
        "practice": [
            ["说双轴跟随", "Two-axis follow adds vertical motion to pan-follow."],
            ["说对角线原则", "Plan the start and end, then move diagonally."],
            ["说典型用法", "Top-to-bottom or bottom-to-top tilt, ending on the sky."],
            ["说运动变焦", "Switch joystick mode and use the follow-focus motor."]
        ],
        "pitfalls": [
            ["Move without a plan.",
             "Decide the start and end before you move.",
             "先想好起止再运镜。"],
            ["Only pan horizontally.",
             "Add vertical motion for richer shots.",
             "双轴要上下结合。"],
            ["End on an empty frame.",
             "Land on the sky or a building.",
             "以天空建筑收尾。"],
            ["Struggle with zoom mid-shot.",
             "Switch joystick mode and use the follow-focus motor.",
             "用摇杆模式变焦。"],
            ["Zoom by hand and shake.",
             "Let the gimbal control the zoom.",
             "让稳定器控制变焦。"]
        ],
        "shifts": [
            ["说运镜只会说 camera move",
             "用 two-axis follow（双轴跟随）、diagonal rule（对角线原则）、tilt shot（摇镜头）"],
            ["说变焦只会说 zoom",
             "用 follow-focus motor（跟焦电机）、joystick mode（摇杆模式）、focal length（焦段）"],
            ["说跟随只会说 follow",
             "用 pan-follow（平移跟随）、vertical movement（上下移动）、plan the route（规划路线）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：双轴跟随怎么拍记住对角线原则、双轴跟随模式在平移跟随的基础上加了上下的运动模式、稳定器不仅可以随着身体左右平移还可以配合上下方向进行移动、一般使用双轴跟随模式都是由上到下或者由下到上的摇镜头方式、最后带到天空或者建筑作为结尾、大家在运镜时提前想好画面的开头和结尾、比如我想从人物开始运镜最后落在樱花和天空结束、确定好大致路线后记住要往对角线方向运镜就OK了、在运镜过程中需要改变焦段、通过切换摇杆模式配合跟焦电机直接用稳定器快速控制镜头变焦等。"
    },
    "49c6PsYXRP": {
        "practice": [
            ["说锁定模式", "Lock mode keeps the gimbal facing forward."],
            ["说进入方式", "Press and hold the trigger to enter lock mode."],
            ["说适用场景", "Fixed routes and subjects moving on a fixed line."],
            ["说前景转场", "Pass foregrounds to design a transition."],
            ["说真稳算法", "The RS4's 4th-gen algorithm keeps static shots steady."]
        ],
        "pitfalls": [
            ["Hold the trigger too briefly.",
             "Press and hold to enter lock mode.",
             "要长按扳机键。"],
            ["Use lock mode for sweeping shots.",
             "It keeps the heading fixed for steady tracking.",
             "锁定模式锁定朝向。"],
            ["Ignore foregrounds.",
             "Pass them to build natural transitions.",
             "前景可做转场。"],
            ["Expect free tilting in lock mode.",
             "Lock mode freezes the camera's direction.",
             "锁定模式不跟身体。"],
            ["Forget fixed-route subjects.",
             "Lock mode is perfect for walking shots.",
             "固定线路用锁定。"]
        ],
        "shifts": [
            ["说稳定器只会说 gimbal",
             "用 lock mode（锁定模式）、trigger button（扳机键）、fixed route（固定线路）"],
            ["说拍摄只会说 shoot",
             "用 static shot（固定镜头）、track the subject（跟随主体）、transition（转场）"],
            ["说稳只会说 stable",
             "用 real-stability algorithm（真稳算法）、steady frame（稳定画面）、gimbal drift（云台偏移）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：为什么我们用稳定器拍摄时画面还是会移动呢、很多新手小白在拍摄人像或者商单短片的过程中总是觉得稳定器很复杂很难上手、锁定模式是大家拿到稳定器最容易上手也是最容易忽略的模式、比较常用于固定镜头或者拍摄人物在某一个方向固定的运动、长按扳机键进入锁定模式后稳定器不会跟随我们身体移动而是锁定在朝前的方向上、当我们按照固定线路拍摄时就可以打开锁定模式、比如人物在固定位置或者固定行径状态时、锁定模式下可以确保云台不会向其他方向偏移、从而拍出跟随人物走动的画面、也可以通过锁定模式运镜时经过不同的前景、把镜头设计成转场过度使用、RS4搭载了第四代真稳算法、优化了云台的控制、可以在我们拍摄固定镜头时做到尽可能的画面稳定等。"
    },
    "nXxooAxGnr": {
        "practice": [
            ["说慢门追随", "Slow the shutter and pan with the moving car."],
            ["说三大要素", "Low shutter, smooth focus tracking, same speed."],
            ["说推荐参数", "1/15s to 1/60s; slower is more dynamic."],
            ["说白天拍摄", "Use an ND filter when light is strong."],
            ["说练习路径", "Start at 1/60s and lower step by step."]
        ],
        "pitfalls": [
            ["Drop the shutter too fast.",
             "Start at 1/60s and lower it gradually.",
             "快门要逐步降。"],
            ["Pan at a different speed from the car.",
             "Match the subject's speed for a sharp body.",
             "与被摄体同速。"],
            ["Shoot handheld and shake.",
             "Use a tripod or gimbal.",
             "用三脚架或稳定器。"],
            ["Forget ND in daylight.",
             "Bright light needs an ND filter to slow the shutter.",
             "白天要ND滤镜。"],
            ["Expect blur from post effects.",
             "Dynamism comes from shutter and tracking, not filters.",
             "动感靠拍不靠后期。"]
        ],
        "shifts": [
            ["说拍车只会说 shoot a car",
             "用 slow-shutter panning（慢门追随）、speed lines（速度线）、pan along（跟随平移）"],
            ["说快门只会说 shutter speed",
             "用 drop the shutter（降低快门）、1/15s to 1/60s（推荐快门范围）、ND filter（ND滤镜）"],
            ["说稳定只会说 steady",
             "用 focus tracking（跟焦）、tripod support（三脚架辅助）、same speed（同速移动）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：如何把爱车拍动感、用慢门追随拍摄法把静态的车拍出动感、核心是把快门速度放慢跟随车辆移动拍摄、让背景产生动态模糊而车身保持清晰、营造速度感和张力、慢门追随法核心原理、降低快门速度如1/30s或更慢、在车辆移动的同时跟随平移相机、车身因相对静止而保持清晰、背景因相机移动而产生动态模糊形成速度线效果、三要素低快门速度加平滑跟焦加与被摄体同速移动、慢门拍摄需要练习跟焦的稳定性、手持容易抖动建议使用三脚架或稳定器辅助、快门太慢导致车身也模糊、跟焦不匀速导致画面抖动、光线太强时快门降不下来需要ND滤镜、推荐快门1/15s到1/60s越慢越动感但越难稳、保持与车同速、减少微抖动、白天也能用慢门、光线强时必备、练习从1/60s开始逐步降低快门速度、先用静止物体练习跟焦稳定性、白天拍摄备好ND滤镜来控制进光量、选择有背景细节的场景树木建筑模糊效果更明显、新手最常见的错误是快门速度突然降太低导致全画面模糊、另一个问题是跟焦不匀速在车辆经过正前方时需要最快转动、适用于汽车自行车跑步者等运动主体的动态拍摄、夜景暗光环境更容易使用慢门白天需要ND滤镜辅助、动感不是靠后期滤镜做出来的而是靠快门速度和跟焦技巧拍出来的等。"
    },
    "2HlhFpYqj6b": {
        "practice": [
            ["说动作引导", "Use an action as the trigger point for the cut."],
            ["说无感转场", "The best transition is one the audience never notices."],
            ["说三种转场", "Lens cover, match cut, and consistent motion."],
            ["说动作余量", "Keep 0.5s of action on each side of the cut."]
        ],
        "pitfalls": [
            ["Cover the lens incompletely.",
             "Block it fully or the seam shows.",
             "遮镜头要遮全。"],
            ["Mismatch the actions.",
             "Ending pose must equal the starting pose.",
             "动作要衔接。"],
            ["Cut on a still frame.",
             "Always cut during motion.",
             "永远在运动中切。"],
            ["Rely only on post effects.",
             "Plan the action while shooting.",
             "拍摄时就要规划。"],
            ["Expect complex effects.",
             "Simple action transitions are the best.",
             "简单转场最自然。"]
        ],
        "shifts": [
            ["说转场只会说 transition",
             "用 action-triggered cut（动作触发切换）、invisible transition（无感转场）"],
            ["说剪辑只会说 edit",
             "用 cut at max speed（最高速处切）、persistence of vision（视觉暂留）、match cut（动作匹配）"],
            ["说特效只会说 effect",
             "用 lens cover（遮镜头）、body movement（肢体动作）、momentum（动力感）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：如何用最简单的转场手法让视频画面变化不再生硬、用动作引导的方式完成流畅的场景过渡、转场视频的关键不是特效而是用动作作为切换的触发点、最好的转场是观众感觉不到的转场、用肢体动作和镜头运动隐藏剪辑点、设计转场动作拍摄时保留动作、剪辑时在动作最高速时切、观众的视觉暂留会填补剪辑痕迹、简单转场的黄金法则、遮镜头转场手或物体遮住镜头切从遮住物移开、动作匹配转场上一个镜头动作结束的姿势等于下一个镜头动作开始的姿势、运镜方向一致两个镜头的相机运动方向一致切镜时保持运动连续、关键在剪辑点前后各保留0.5秒的动作让过渡有动力感、遮镜头没遮全露出边缘确保完全遮黑、动作不匹配上一个镜头举右手下一个镜头举左手不自然、在静止画面中切显得生硬永远在运动中切、转场需要在拍摄时就规划好动作不能完全靠后期、适用于Vlog日常记录旅行视频中的场景切换、最好的转场是不让人注意到的转场、从我需要一个酷炫转场转变为我在动作中偷偷换场景等。"
    },
    "3wyVoWgGSZl": {
        "practice": [
            ["说掩体转场", "Walk past a cover and let it trigger the cut."],
            ["说核心原理", "The blocking moment is the most natural cut point."],
            ["说常见掩体", "Walls, pillars, passersby, doors, and door frames."],
            ["说行动清单", "Find covers, shoot through them, cut at the block."],
            ["说避坑要点", "Full cover, no see-through, similar brightness."]
        ],
        "pitfalls": [
            ["Pick a cover too small.",
             "It must fully block the lens for a few frames.",
             "掩体要够大遮全。"],
            ["Use see-through covers.",
             "They reveal the cut.",
             "别用半透明掩体。"],
            ["Switch to a much brighter scene.",
             "Keep brightness similar across the cut.",
             "前后光比别太大。"],
            ["Rely on post effects.",
             "This transition needs zero post work.",
             "零后期成本。"],
            ["Forget to hunt for covers.",
             "Make finding covers a shooting habit.",
             "养成找掩体的习惯。"]
        ],
        "shifts": [
            ["说转场只会说 transition",
             "用 natural cover（自然掩体）、trigger point（触发点）、blocking moment（遮挡瞬间）"],
            ["说旅行拍摄只会说 travel vlog",
             "用 city walk（城市漫步）、pass through（穿过）、zero post cost（零后期成本）"],
            ["说切换只会说 switch",
             "用 cut at the block（遮挡处切）、cross the door（过门切换）、orbit around（环绕）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：这大概是最简单的旅行vlog转场吧、利用自然的掩体墙壁柱子路人作为转场触发点、走过去画面自然切换、最简单也最有效的旅行转场技巧、找掩体墙壁柱子路人走过去遮挡镜头切换场景自然过渡、掩体转场的原理在旅行拍摄中利用环境中自然存在的掩体墙壁柱子路人车门、让主体走过去遮挡镜头、遮挡的瞬间就是最自然的转场点、后面接任何场景都不会突兀、这是所有转场技巧中实现成本最低但效果最自然的、不需要任何后期特效、只需要在拍摄时多走一步穿过某个物体、墙壁建筑适合老街城区靠近墙壁走过去镜头贴墙、柱子路灯围绕柱子转半圈转到新场景、路人跟随一个路人走过遮挡镜头、车门上下车时车门自然遮挡、门框出入口进门出门的瞬间切换场景、拍摄时主动寻找场景中的自然掩体、每到一个新场景先拍一个穿过掩体的过渡镜头、后期在掩体遮挡镜头的瞬间切场景、掩体要足够大能完全遮挡镜头至少两三帧全黑、不要找半透明的掩体树叶缝隙等会暴露切换痕迹、前后场景光比不要差太多否则转场会跳、适用于旅行Vlog城市漫步探店记录等有物理移动的拍摄场景、旅行Vlog不需要复杂的特效转场、掩体转场等于零后期成本、遮挡瞬间等于最自然的叙事断裂点、找掩体的习惯比任何转场教程都重要等。"
    },
    "ENv35ryYOb": {
        "practice": [
            ["说安全区", "The safe zone is where main footage lives."],
            ["说禁区", "The restricted zone is for scale gestures—add nothing."],
            ["说元素位置", "Eyes, title, and captions have their own spots."]
        ],
        "pitfalls": [
            ["Put key content at the edges.",
             "Keep it inside the safe zone.",
             "关键内容放安全区。"],
            ["Add elements to the restricted zone.",
             "It's reserved for zoom gestures.",
             "禁区别放元素。"],
            ["Cover captions with overlays.",
             "Place them in the safe bottom area.",
             "字幕放安全区下方。"],
            ["Place titles randomly.",
             "Titles have a designated spot.",
             "标题有固定位置。"],
            ["Ignore platform UI.",
             "Safe zones avoid platform overlays.",
             "安全区防UI遮挡。"]
        ],
        "shifts": [
            ["说排版只会说 layout",
             "用 safe zone（安全区）、restricted zone（禁区）、element placement（元素摆放）"],
            ["说遮挡只会说 cover",
             "用 platform UI（平台界面）、scale gestures（缩放操作）、overlay（叠加层）"],
            ["说画面只会说 frame",
             "用 main footage（主要画面）、key content（关键内容）、caption area（字幕区）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：这里是你的安全区、这是你的禁区、这里是你眼睛出现的地方、这里是标题要出现的位置、这里是字幕、安全区是常用画面、禁区用来放大缩小、千万不要在这里和这里添加任何东西等。"
    },
    "68f0a1lDCT6": {
        "practice": [
            ["说推", "Push with your body, not your hand."],
            ["说拉", "Pull back with your legs."],
            ["说摇", "Pan from your waist."],
            ["说移", "Slide with your whole body."],
            ["说升降", "Rise and crouch slowly with leg power."]
        ],
        "pitfalls": [
            ["Push with your arms only.",
             "Drive the push with your body.",
             "推用身体带动。"],
            ["Pull back with your hands.",
             "Step back with your legs.",
             "拉用腿后退。"],
            ["Pan by swinging your arms.",
             "Rotate your waist instead.",
             "摇要转腰。"],
            ["Slide with your arms.",
             "Move your whole body laterally.",
             "移要身体横移。"],
            ["Rise with your waist.",
             "Drive the rise with your legs.",
             "升降腿部发力。"]
        ],
        "shifts": [
            ["说运镜只会说 camera move",
             "用 body-driven push（身体带动推）、leg-driven pull（腿部后退拉）、waist pan（腰部横摇）"],
            ["说稳定只会说 steady",
             "用 lower your center（放低重心）、plant your feet（先落脚）、even speed（匀速）"],
            ["说拍摄只会说 shoot",
             "用 lateral slide（横移）、rise and fall（升降）、static shot（静态拍摄）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：推不是用手推而是用我们的身体带动我们的手去推、拉不是用手拉而是用我们的腿去拉、摇不是用手摇而是转动我们的腰部左右横摇、移不是这样移不是用我们的手臂去移而是控制好我们的身体左右水平横移、还有上下垂直移动的升降等。"
    },
    "1WsLXa0PqFw": {
        "practice": [
            ["说电影感三要素", "Wide aspect ratio, directional light, layered foreground."],
            ["说遮幅", "Add 2.35:1 letterboxing for the fastest cinematic feel."],
            ["说方向光", "Light from one side; let the other fall into shadow."],
            ["说前景景深", "Blur a foreground object; use a wide aperture."],
            ["说饱和度", "Drop saturation 10–20% for a calmer image."]
        ],
        "pitfalls": [
            ["Only add black bars.",
             "Light and composition carry the look too.",
             "黑边只是锦上添花。"],
            ["Use flat, even lighting.",
             "Make the light directional.",
             "光线要有方向。"],
            ["Let the foreground block the subject.",
             "Keep it under 15% of the frame.",
             "前景别挡主体。"],
            ["Desaturate too much.",
             "Stay around 10–15%, never over 20%.",
             "饱和度别降过头。"],
            ["Blame your equipment.",
             "Technique, not gear, creates the look.",
             "关键在技巧不在设备。"]
        ],
        "shifts": [
            ["说电影感只会说 cinematic",
             "用 letterboxing（遮幅）、directional light（方向光）、foreground blur（前景虚化）"],
            ["说调色只会说 color grade",
             "用 desaturation（降低饱和度）、calmer image（沉稳画面）、widescreen feel（宽银幕感）"],
            ["说构图只会说 composition",
             "用 layered depth（层次）、shallow depth of field（浅景深）、aspect ratio（画幅比）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：如何在23秒内掌握拍出电影感的几个核心技巧、从构图到光线普通人也能上手的电影感速成法、几个简单技巧可以让画面在几秒内产生电影般的质感、电影感不来自设备来自构图意识加光线选择加画面比例、改变画幅注意光线增加前景控制景深降低饱和度、电影感不需要昂贵的设备改变几个拍摄习惯就能让画面质变、最重要的三个要素宽画幅比2.35:1遮幅、有方向的光线、层次分明的前中后景、加黑边遮幅后期添加2.35:1黑边这是最快的电影感捷径、光线有方向避免全脸均匀光照让光线从一侧来脸的另一侧有阴影、前景虚化在镜头前放一个物体并虚化增加画面层次、降低饱和度适当降低色彩饱和度10到20%画面更沉稳、控制景深用大光圈让背景虚化突出主体、画幅比16:9全屏对2.35:1宽银幕后期加黑边遮幅、光线正面均匀打光对侧光加阴影光源放在人物一侧、层次平铺直叙对前景加中景加背景加前景虚化物体、色彩原始饱和度对降低10到20%饱和度后期调色调整、给视频添加2.35:1黑边遮幅、下次拍摄时把光源放在人物一侧、找一个物体放在镜头前10cm处虚化前景、后期把饱和度降低10到15%、只加黑边以为就是电影感忽略光线和构图、侧光太强烈一半脸全黑适当补充一点反光板或柔光、前景虚化物体太大挡住主体前景物体在画面边缘且占不超过15%、饱和度降太多画面变灰控制在降低10到15%不要超过20%、适用于Vlog短片个人创作等需要画面美感的视频、电影感风格不适合所有内容快节奏搞笑内容过度电影感反而违和、电影感等于宽画幅加侧光加前景层次加低饱和度加深景深、手机也能拍出电影感关键在技巧不在设备、从我缺一台好相机转变为我需要在拍摄时就为电影感做决策等。"
    },
    "4eJBwSSK5xU": {
        "practice": [
            ["说响指转场三要素", "Small action, clear sound, strong visual focus."],
            ["说操作流程", "Shoot two snap scenes; cut at the sound peak."],
            ["说一致性", "Keep direction, speed, and hand position identical."],
            ["说对齐剪辑点", "Zoom the waveform and nudge the cut 1–2 frames."],
            ["说替代动作", "Claps or stomps can replace the snap."]
        ],
        "pitfalls": [
            ["Mismatch the hand positions.",
             "Mark the position so both snaps match.",
             "手的位置要一致。"],
            ["Snap far from the mic.",
             "A clear sound is needed to find the cut.",
             "打响指靠近麦克风。"],
            ["Miss the sound peak.",
             "Zoom the waveform to align precisely.",
             "对准响指峰值。"],
            ["Forget the snap in scene B.",
             "Both scenes need the action.",
             "两个场景都要做动作。"],
            ["Use it for serious content.",
             "The snap is too showy for low-key videos.",
             "严肃内容慎用。"]
        ],
        "shifts": [
            ["说切镜只会说 cut",
             "用 sound-triggered cut（声音触发切换）、audio waveform（音频波形）、snap peak（响指峰值）"],
            ["说动作只会说 action",
             "用 hand position（手的位置）、visual focus（视觉焦点）、sound cue（声音提示）"],
            ["说转场只会说 transition",
             "用 match the move（动作一致）、nudge the cut（微调剪辑点）、frame-by-frame（逐帧）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：响指转场用最简单的动作触发场景切换、15秒学会最受欢迎的短视频转场之一、一个响指等于完美的转场触发点、动作清晰加声音鲜明加视觉焦点集中、响指转场之所以流行是因为动作小加声音明确加视觉冲击力强、拍摄响指动作在响指声峰值切镜下一个场景从动作中开始、动作小而清晰手指打响指、有听觉提示啪一声、视觉焦点集中所有人的注意力都在手上、在响指声的峰值点切镜观众的注意力被声音引导切换自然流畅、拍两个场景两个场景中都在做打响指的动作、剪辑时把剪辑点精确放在响指声的峰值啪的一瞬间、前一个镜头结束于响指后一个镜头从响指开始动作和声音形成连续、两个场景的响指动作方向速度手的位置要尽量一致否则会有跳跃感、拍摄时标记手的位置、放大音频波形找到响指的峰值点作为切换点、如果动作不够连贯微调剪辑点前移或后移一两帧、打响指时靠近麦克风、尝试延伸用拍手跺脚等其他有声音的动作替代响指、两个场景手的位置不一致跳跃感、响指声音不够清晰找不到剪辑点、剪辑点没对准响指峰值动作和声音不同步、后一个场景忘记做响指动作前后不连贯、适用于短视频转场Vlog场景切换服装造型变换展示、响指转场比较显眼不适合需要低调转场的严肃内容、从切就切了转变为用声音触发转场让观众的耳朵先感知变化等。"
    },
    "9pHFfApHJ7t": {
        "practice": [
            ["说真实与诗意", "Non-photographers record reality; photographers capture poetry."],
            ["说树干线条", "Treat a trunk as a bold line."],
            ["说布局关系", "One tree: line; two: relationship; many: order."],
            ["说调整角度", "Change angles to find new compositions."],
            ["说用心感受", "Poetic feel comes from feeling, not post."]
        ],
        "pitfalls": [
            ["Snap whatever you see.",
             "Look up and observe first.",
             "先观察再拍。"],
            ["Rely on post filters.",
             "Poetry comes from composition and feeling.",
             "诗意靠拍不靠修。"],
            ["Shoot everything at eye level.",
             "Try looking up for new lines.",
             "试着仰视找线条。"],
            ["Only shoot single trees.",
             "Two trees show relationship; many show order.",
             "多拍几棵树看秩序。"],
            ["Rush the moment.",
             "Slow down and feel the scene.",
             "放慢节奏去感受。"]
        ],
        "shifts": [
            ["说拍树只会说 shoot trees",
             "用 bold line（粗线条）、look up（仰视）、composition（构图）"],
            ["说诗意只会说 poetic",
             "用 capture poetry（拍出诗意）、mood（意境）、rhythm of order（秩序节奏）"],
            ["说手机摄影只会说 phone photo",
             "用 exposure slider（曝光调节）、zoom composition（变焦构图）、try new angles（多试角度）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：怎么把这片小树林拍出诗意感大片、不少人都是拿出手机就拍没啥问题就是真实、不懂摄影的人拍的是真实懂摄影的人拍的是诗意、我会走进小树林走到一棵树前仰视观察、把树干看成一根粗线条、通过变焦布局构图、根据上一期的知识点上拉小太阳、拍出不见春时花满树铁骨斗寒天、再调整角度再寻找树干的布局、拍出残枝蘸雪为洞笔满写云间带春意、再拍两棵树寻找两棵树的布局关系、再拍更多树的秩序关系、慢慢的感受双风过处万枝空、疏影横斜水清浅、东边日出西边雨别有风姿在画中、玩手机摄影你只关注我就足够了等。"
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
