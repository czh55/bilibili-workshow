#!/usr/bin/env python3
"""批17：将简化场景JSON补全为 gen-scene-en.py 所需的完整结构。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "1cpgeBe2kdb": {
        "duration": "3:34", "topic": "随笔 · 生活感悟",
        "practice": [
            ["说冰淇淋象征", "The unopened matcha tub is a vessel of hope."],
            ["说课文共鸣", "The Last Leaf places hope on the ivy vine."],
            ["说自我安慰", "At least I still have a matcha tub."],
            ["说守护希望", "I feared losing the ability to comfort myself."],
            ["说恢复正常", "Life isn't normal, but I should make it so."]
        ],
        "pitfalls": [
            ["Treat comfort objects as everlasting.",
             "Hope is a vessel, not an eternal stash.",
             "寄托不是永远保留。"],
            ["Wait for perfect conditions to enjoy.",
             "Under normal circumstances you'd have done it already.",
             "正常情况早该去做。"],
            ["Hold onto the past instead of moving on.",
             "Plant new leaves rather than guarding old ones.",
             "与其守着过去不如种新树。"],
            ["Let comfort become avoidance.",
             "Use the comfort to step toward recovery.",
             "自我安慰不能变成逃避。"],
            ["Measure life by one standard of perfection.",
             "The standard of perfection keeps changing.",
             "完美的标准一直在变。"]
        ],
        "shifts": [
            ["说舍不得只会说 reluctant",
             "用 the last leaf（最后一片叶子）、vessel of hope（希望的寄托）、self-comfort（自我安慰）"],
            ["说等待只会说 wait",
             "用 unopened for 45 days（未开封45天）、hold on a little longer（再忍一忍）"],
            ["说恢复只会说 recover",
             "用 make it normal（让它恢复正常）、plant a new tree（种一棵新树）、grow new leaves（长新叶子）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：冰淇淋、未开封、45天、超过五分钟、全家、冰柜、各个口味、抹茶味、超爱、高中、暑假、一周吃光、三桶家庭装、最大桶、左手前胸冰凉、后脖颈凉硬邦邦、一口接着一口、最后一片叶子、课文、青年画家琼西、肺炎、卧床不起、窗外常春藤树、天气越来越冷、病情严重、藤叶凋谢、生命的希望、寄托、寒风、始终挂着、信念、痊愈、老画家贝尔曼、病死了、对抗自然的奇迹、冷雨夜、连夜画在墙上、肺炎夺走生命、最伟大的画作、故事后半段、树叶对琼西、希望的寄托、不要嘲笑、最后一罐、先留着、今晚吃掉、很久买不到、只剩两根、再忍一忍、森林的味道、快用完了、对剩就对了、每天读五页、解封正好读完、至少我还有一罐抹茶冰淇淋、几十天、自我安慰、完成一天的工作、作息混乱、半夜睡不着、沮丧的消息、没有吃掉、情绪低落、吃掉了这罐、生活没有恢复正常、该让它恢复正常、规律锻炼、阳台晒太阳、遛狗邻居、打招呼、出不了门、想之后拍什么、植物越长越好、发芽土豆、治愈、种植一棵新树、长一些叶子、心情低落、很多事情还在变好、更有力量、正常情况下早该吃掉它等。"
    },
    "9BibVUw3BZJ": {
        "duration": "4:26", "topic": "Vlog · 分屏技巧",
        "practice": [
            ["说分屏用处", "Match montage, transition, or eye-catching stroke."],
            ["说对比分屏", "Same composition, different reality and imagination."],
            ["说双向奔赴", "Two people, same framing, both walking."],
            ["说合而为一", "Let the split screens merge after they meet."],
            ["说动作框架", "Doors, windows, zippers frame the split naturally."]
        ],
        "pitfalls": [
            ["Shoot flat single-frame scenes.",
             "Split-screen creates similarity and contrast.",
             "分屏制造相似与反差。"],
            ["Use identical frames with no story.",
             "Change the scene and people, keep the composition.",
             "分屏要有变化与情节。"],
            ["Split screens that don't interact.",
             "Form one complete composition across spaces.",
             "分屏两块要形成整体构图。"],
            ["Force the split entrance.",
             "Let a door, window, or zipper frame it naturally.",
             "分屏进场要自然。"],
            ["Overuse identical transitions.",
             "Match the split to your story's mood.",
             "分屏要贴合情节。"]
        ],
        "shifts": [
            ["说分屏只会说 split screen",
             "用 matching montage（同频蒙太奇）、merge into one（合而为一）、comic panels（多格漫画）"],
            ["说对比只会说 contrast",
             "用 similarity and contrast（相似与反差）、imagination and reality（想象与现实）"],
            ["说构图只会说 composition",
             "用 same composition（同构图）、natural entrance（自然进场）、frame formed by action（动作框架）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：打喷嚏、上班路车流、切、讨作、视频主题、做视频、简单、画面建立确定、分屏、拥有姓名、辅助情节、同频猛太期、有趣的转场、Vlog中、眼前一亮、偷学电影碎片、分评用法、1916年、俄国电影、黑桃皇后、对比想象与现实、93年之后、和莎莫的500天、更精致、更令人心碎、常见的一种、构图、场景、营造相似性、表演道具区别、营造反差、趣味性、场景变化、人物不同、一男一女、构图相同、两个人都在赶路、经典、双向奔赴、滑轨、手超稳、情爱磁场、碰面之后、顺滑合而为一、何同学、多格漫画时分评、Vlog的开头、不错的选择、平凡的一天、爬起床、出门上班、突然反应过来、被踩了、怎么搬、分评的乐趣、完整构图、不同空间的场景、发生互动、混减广告片、打电话、一零后、恶趣味、电影里经常出现、相对保守的年代、男女角色、躺在不同的床上、打情骂俏、亲密又不至于鹿骨、腐拍设备、愿意配合的女朋友、细节、进场上画在心思、开冰箱门、门或者窗、拉链、小道具、动作形成的框架、自然进场、千变万化、历史悠久、经久不衰、接近的桥段、回来了、葡萄头、下期再见、拜拜等。"
    },
    "8csxJOVnmZX": {
        "duration": "4:57", "topic": "Vlog · 百搭技巧",
        "practice": [
            ["说技巧特点", "Simple, no fatigue, yet clever."],
            ["说定格感受", "Freeze interrupts emotion—use it in reverse."],
            ["说定格玩法", "Freeze with motion blur for artistic frames."],
            ["说快变焦", "Low shutter + quick zoom gives retro humor."],
            ["说拍摄前提", "Wide-range zoom lens, or keyframe in post."]
        ],
        "pitfalls": [
            ["Chase flashy effects.",
             "Simple tricks are the versatile basics.",
             "酷炫特效反而易疲劳。"],
            ["Let freezing break your flow unintentionally.",
             "Freeze on purpose at the artistic instant.",
             "定格要刻意用在艺术瞬间。"],
            ["Act out every action scene.",
             "Freeze the most dynamic frame instead.",
             "动作场面演出来太假。"],
            ["Zoom without a wide-range lens.",
             "Keyframe the scale in post if you lack one.",
             "没有变焦就后期打关键帧。"],
            ["Ignore shutter speed with quick zoom.",
             "Low shutter gives the retro wuxia feel.",
             "快变焦要配合低快门。"]
        ],
        "shifts": [
            ["说技巧只会说 trick",
             "用 versatile basics（百搭单品）、wardrobe basics（牛仔裤白球鞋）"],
            ["说定格只会说 freeze",
             "用 freeze frame（定格）、motion blur（运动模糊）、compress time（压缩时间）"],
            ["说变焦只会说 zoom",
             "用 quick zoom（快速变焦）、old wuxia feel（老武侠感）、keyframe the scale（关键帧缩放）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：视频创作技巧、非常简单、酷炫的特效、复杂显眼、审美疲劳、各种各样的视频、巧妙出现、会做视频、牛仔裤、白球鞋、百搭单位、网络没有问题、卡住了、定格的效果、剪辑软件一键、第一个百搭技巧、回味、难受、连贯的动作被停住、情绪被打断、注意定格画面信息、逆向思维、加以利用、相台甚欢、你平常看视频三连吗、从不三连、拍视频、原则、倾灭的笑了、杯子喝了一口、装喜结精品、一瞬间定格、比连关起来更有艺术性、电影里常见、图B、演出来很假、动作场面、买新镜头、脚趾狂抠、定格请出来、有点尬、比动态画面、只取定格帧、忽略表演、分镜、原地摩擦、运动模糊擦出来、最有动感的一帧、氛围感拍照、随便一截自然、定格画面快切、压缩时间的猛太棋、罗拉快跑、擦肩而过、定格照片快切、路人命运、使用场景很多、开头出标题、结尾情绪抽离、众生相、每期视频用到、第二个百搭技巧、不明显、增加趣味、博主、随意拉一下胶段、吸引注意力、动态丰富、快门速度调低、老武侠偏的感觉、老电影、坤廷、伟三德森、强调信息、放大表情、复古和一点幽默、运动模糊、冲击力动感、配合音效、连续动作、不到25岁、改变、前提、焦段叉子比较大的变焦镜头、2470、叉子够用、后期缩放打关键帧、实拍的质感、两个百搭技巧、结合、营造有趣画面、快乐系列花絮、喷包等。"
    },
    "9cNPz8Gd2nm": {
        "duration": "4:34", "topic": "Vlog · 手写文字动画",
        "practice": [
            ["说设备要求", "iPad with Apple Pencil and paid app Procreate."],
            ["说画布设置", "Match canvas size to your video resolution."],
            ["说描字技巧", "Write, trace into blocky hollow letters, fill color."],
            ["说动画导出", "Three traced layers × 3 = nine-frame animated GIF."],
            ["说PR抖动", "Turbulent Displace + Posterize Time for jitter."]
        ],
        "pitfalls": [
            ["Draw animation frame by frame.",
             "Trace three slightly different versions of the word.",
             "逐帧画太累，描三遍更高效。"],
            ["Trace too neatly.",
             "Trace rougher for a stronger shaking feel.",
             "描得太整齐抖动感弱。"],
            ["Forget the transparent background.",
             "Export animated GIF for transparency.",
             "导出动画GIF才有透明底。"],
            ["Pick Posterize instead of Posterize Time.",
             "Choose Posterize Time and change 24 to 6 or 9.",
             "要选色调分离时间而非色调分离。"],
            ["Stick to one method only.",
             "Combine turbulence displacement and paper tracing.",
             "多种方法可自由组合。"]
        ],
        "shifts": [
            ["说动画只会说 animation",
             "用 hand-drawn text（手写动画文字）、animation assist（动画协助）、transparent GIF（透明GIF）"],
            ["说描字只会说 trace",
             "用 blocky hollow letters（方块空心字）、rough strokes（粗糙笔迹）、shake effect（抖抖感）"],
            ["说后期只会说 post",
             "用 turbulent displace（湍流置换）、posterize time（色调分离时间）、blend mode（混合模式）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：手绘动画文字、省略开场白、详细教程、第一种方法、设备要求、Apple Pencil、iPad、付费软件Procreate、替代方法、新建画布、尺寸、视频一样、1080P、1920x1080、小扳手、画布、动画协助打开、截图、参考、新建图层、写字、干油墨、琢磨分类、手写风格字体、打出来再描、方块感觉字体、正常字、顺着笔画、方块感觉空心字、填色、手写字图片、动态、新建两个图层、描一遍、三个笔迹不同图层、故意粗糙、抖动感、复制两次、按顺序排列、每秒九帧、图刚好一秒、方便、九个图层、全部关闭、分享、导出动画、动画GIF、透明底、传到电脑、放到视频上面、动画不够长、多复制几段、拼到一起、任何剪辑软件、描两遍太麻烦、关闭其他图层、导出PNG、放到视频、PR完成、搜索囤流置换、施加完整图片、数量改成10、演化、打关键帧、猛拉大、疯狂抽出、嵌套、色调分离时间、不要选色调分离、24改成6或9、6帧或9帧、逐帧抖动、对比两种方法、右边感觉更好、没有iPad、解决方案、麻烦、白纸、马克笔、笔触粗一点、先写一遍、方块字、贴在窗户上、屏幕上、盖上另一张白纸、描一遍、再来一张纸、三张纸分别拍下来、黑色的字、三张照片、导进解决软件、调整位置、持续时长、每张三张左右、多复制几组、守卫相连、形成动画、嵌烫、对比度拉高、黑白分明、背景渐进纯白、混合模式、变暗、透明底黑色文字动画、变亮、镂空效果、有意思、其他颜色、导进PS、抠出来、控制软件、三张扣好的PNG、变成动画、油系统工具改颜色、直接在PS改颜色、繁琐、接近于Procreate、只写一遍、抠出来、团流之换、色调分离时间、抖动效果、现成的字体、普通的字体、三种形状接近的手写字体、同样的方法、文字动画的制作方法、简单美料的干活视频、帮到指导你、波头、下次再见、拜拜等。"
    },
    "4UPILbObSx0": {
        "duration": "4:01", "topic": "Vlog · 慢门慢动作",
        "practice": [
            ["说慢门原理", "Long shutter records motion trails in one frame."],
            ["说静态主体", "Tripod still, crowd flows into trails."],
            ["说镜头运动", "Orbit the subject with grid lines holding center."],
            ["说慢动作原理", "High fps captured, low fps playback."],
            ["说情绪放大", "Slow motion magnifies emotion and details."]
        ],
        "pitfalls": [
            ["Shoot at normal shutter for emotion shots.",
             "Low the shutter to create trails and stutter.",
             "情绪画面要调慢快门。"],
            ["Let the whole frame blur chaotically.",
             "Keep the subject still with a tripod.",
             "三脚架让主体保持静止。"],
            ["Hand-hold an orbiting shot.",
             "Use grid lines to hold the subject center.",
             "环绕拍摄借助参考线固定。"],
            ["Shoot slow motion at the same frame rate.",
             "Capture high fps and play back low.",
             "慢动作要高拍低放。"],
            ["Use slow motion for complex fights.",
             "Use it to show subtle, telling details.",
             "慢动作拍细微动作更有戏。"]
        ],
        "shifts": [
            ["说快门只会说 shutter",
             "用 motion trails（拖影）、slow shutter（慢门）、below frame rate（低于帧率）"],
            ["说慢动作只会说 slow motion",
             "用 high fps low playback（高拍低放）、subtle movements（细微动作）、magnify emotion（放大情绪）"],
            ["说拍摄只会说 shoot",
             "用 tripod still（三脚架静止）、grid lines（参考线）、orbit the subject（绕主体旋转）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：寻常画面之外、笨拙缓慢、从慢入手、电影中、运动部分、拖印、慌乱迷离、慢速快门、枯燥知识、快门速度、开合一次、运动轨迹、15分之一秒、拍卧、美妙拖印、展现理论知识、分母小于拍摄真律、抽真、30帧、快门速度、一团乱、相对静止、三角架、人流之中、马路对面、孤独感、镜头运动、政策跟、绕的人旋转、参考线、固定位置、慌乱迷失感、怪力怪气、快门速度调慢、惊喜、慢动作、电影中十分常见、高帧数画面低帧数播放、30帧拍60帧、0.5倍、120帧、0.25倍、240帧、计判器、体现动作细节、枪杖、打戏、复杂的动作设计、细微的动作、挠了三次头发、抹了七次鼻子、吞了十三次口水、撒谎、放大情绪、修饰演技、长速播放、显得我很蠢、回头的时候、突然想起那句话、生命不过是一次闪电、慢门和慢动作、使用场景、还有很多、这一视频就展现了、最基础、比较适合用在blog里、集合用法等。"
    },
    "4OG5dpQBBrr": {
        "duration": "3:43", "topic": "器材 · 入门相机",
        "practice": [
            ["说新手需求", "First camera shouldn't be too imposing."],
            ["说直出对焦", "Direct output presets and autofocus are key."],
            ["说视频便携", "Palm-sized body with big battery and good controls."],
            ["说挂机头", "Kit lens covers common focal lengths with stabilization."],
            ["说预算现实", "7000 yuan means smart compromises."]
        ],
        "pitfalls": [
            ["Buy a pro cinema camera as a first body.",
             "Pick something not too imposing for a beginner.",
             "第一台别买存在感太强的。"],
            ["Ignore direct output for novices.",
             "Pretty built-in presets are a must-have.",
             "新手不会调色，直出很重要。"],
            ["Assume manual-focus skills.",
             "Strong autofocus is essential.",
             "新手依赖自动对焦。"],
            ["Overlook battery and size.",
             "One charge should last 600+ shots.",
             "续航和体积要兼顾。"],
            ["Plan expensive accessories.",
             "Kit lens and built-in mic must work well.",
             "配件预算有限，挂机头要好用。"]
        ],
        "shifts": [
            ["说相机只会说 camera",
             "用 first camera（第一台相机）、palm-sized body（巴掌大机身）、kit lens（挂机头）"],
            ["说新手只会说 beginner",
             "用 direct output（直出）、autofocus（自动对焦）、built-in presets（直出滤镜）"],
            ["说预算只会说 budget",
             "用 7000 yuan（7000预算）、smart compromises（合理取舍）、not too imposing（不强存在感）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：六年前、书桌旁、不到二十岁、接触影像创作、韦三的《三在水中生活》、第一台相机、过去的我、未来的特拉、视频创作为生、拍摄等于干活、生活的全部、全部机序、功能发达、新闻强劲、电影机、武装到牙齿、狠狠推、规划我的人生、写小说、会画、科学家、记录探索、新城大海、政府广播、天際的点点瞬间、相机只是点缀、人生的全部、旷野、鬼、谈恋爱、没钱了、坦白、空门的亲戚、18岁以后、牙碎钱、7000块钱、从心审视、相同的特點、新手选相机、注意什么、太强的存在感、人设、文藝青年、事項大哥、顶望在记忆卡里、丢面子、不出贩版、外观轮廓、vlog对话、花时间、剪輯、拍照、发奇怪的朋友圈、前期主要用途、调参数、首動追焦、不能拍小的真兇故事、圈来女生、直出和对焦、重要的关键词、分隔多遍、自带多种多样、简单方便好看、直出率竟是必选项、一天一个想法、视频参数、框、轨道、突然爱上拍摄、塞进、八爪上的机身、电池、一大块、撑过600多张、期待更多拍摄、新手操控、不愿打工的大学生、有钱换进后、配套的挂机头、麦克风式配件、两个方式、好用、挂机头不敢成功的焦段、滴滴感、自带麦、智囊、无比合适、递到20岁的自己、没告诉他、唱响、征服世界、第一次出国、再等五年、很快会分手、卡、硬盘、隔世化、学电影、电影学院旁听、一疊口、探索处处碰壁、宿舍剪视频、最大的爱好、一点他猜对了、第一台相机拍很多东西、不对、ZV-12代、2024年7月发布、带回六年前等。"
    },
    "AC66zAROk0E": {
        "duration": "5:33", "topic": "Vlog · 分身创意",
        "practice": [
            ["说手持甩镜", "Whip the lens both ways, stitch the blur."],
            ["说全景相机", "360 camera shoots front and back positions."],
            ["说后期运镜", "Post panning keeps each shot's motion identical."],
            ["说合体分屏", "Keyframe the merge, switch angles, auto split."],
            ["说慢动作抽离", "Slow-mo one clone to strengthen detachment."]
        ],
        "pitfalls": [
            ["Rely on a free shooting friend.",
             "Use a 360 camera to shoot alone.",
             "别依赖随时有空的朋友。"],
            ["Hand-hold multiple clone passes.",
             "Post panning keeps the motion identical.",
             "后期运镜保证运动一致。"],
            ["Dodge the past self on camera.",
             "Meet your past choices in a split screen.",
             "拍摄相遇过去自己的画面。"],
            ["Keep all clones at normal speed.",
             "Slow-mo one clone for the detached feel.",
             "慢动作一个分身更有抽离感。"],
            ["Fear overused tricks.",
             "Shift angles to see them anew.",
             "用烂的技巧换个角度又是新的。"]
        ],
        "shifts": [
            ["说分身只会说 clone",
             "用 self-dialogue（自我对话）、outsider view（局外人视角）、meet the past（与过去碰面）"],
            ["说运镜只会说 pan",
             "用 post panning（后期运镜）、identical motion（运动一致）、whip-pan（甩镜）"],
            ["说设备只会说 device",
             "用 360 camera（全景相机）、auto split-screen（自动分屏）、high-frame-rate slow motion（升格慢动作）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：没灵感、被用烂的技巧、重获新生、分身自我对话、新玩法、创意、第一种方法、非常简单、手持自拍、镜头往另一个自己出现的方向甩、方好位置、朋友按刚才方向、甩一遍、两张运动模糊的地方、拼在一起、会拍摄随时有空的朋友、很难满足、独自拍摄、全景相机、直接拍到前后两个位置、固定机位拍两遍、后期剪辑做摇镜头、摇的地方拼起来、同样的意思、组织、后期控制运镜、非常重要、保证每段画面运动完全一致、运镜快慢、角度、掌控之中、加再多的分身、理论上不会失误、每种情绪、不同的自己围成一圈、展现内心世界、桥段、vlog一定有了啥、第二种方法、语言描述、例子、躲避过去的自己、无论怎么逃避、跟过去的选择碰面、以前有分享过、电动滑轨、麻烦、Insta420X4、全景相机、类似效果、不需要额外器材、固定机位拍、一边保留一半、找到最终合体的地方、关键针、倒退几秒、分辨跳上左右两个角度、把这一半拍出来、自动变成分屏、很实用的场景、局外人一样讨看自己、其中一个自己变成慢动作、加强抽离感、全部打进来、彻底崩溃、圣格慢动作、陌生感、全景画面的圣格、4K100帧、5.7K60帧、喜欢这种画面、并不新鲜的分身、两期视频、刚开始做视频、第一个技巧、哇有两个我、激动、很难这样激动、分身慢门升格定格动画、新东西、用烂的技巧、变换角度、重新激动起来、Insta360X4、记录生活、不同的角度、日常生活记录、全景画面、保护错过、统一瞬间的每一个角度、8K、更清晰、后期空间、挑选素材、AI找出高光片段、正常的运动相机、自然廣角模式、即便不那么明显、更拍模式、镜头保护照、游戏提升、轻松实现创意拍摄、打动我的优势、一个人拍摄非常复杂、转盘电动滑轨、麻烦的器材、手机操作、手势开拍、一遍成功、效率高、小行星、模仿无人机、移动延时、使用的东西、别的设备、拍不了、操作复杂、全景素材覆盖更多信息、创意空间讲故事、唯一的缺点、账号和app里的教练作势、太详细、创意玩法、AI一间长篇的功能、没有挑战性、全部内容、分享创意和设备、帮助你有影像本来自己的故事、布鲁头、下次再见、拜拜等。"
    },
    "9HPFVvqQ6g9": {
        "duration": "4:21", "topic": "随笔 · 少年愿望",
        "practice": [
            ["说完美计划", "At 11 I listed a dozen-plus perfect-life items."],
            ["说计划落地", "Kangding, Gugu village, a Cadillac SRX."],
            ["说细节复刻", "Scarf for snow, radar-less reversing, snacks, songs."],
            ["说理想火锅", "One bite made him decide to marry her."],
            ["说标准在变", "The perfect standard itself keeps changing."]
        ],
        "pitfalls": [
            ["Chase the imagined perfect life.",
             "The standard of perfection keeps changing.",
             "完美的标准一直在变。"],
            ["Treat childhood plans as promises.",
             "They were dreams, not contracts.",
             "少年计划不是契约。"],
            ["Blame the present for not matching the past.",
             "Feelings now were never imagined then.",
             "当下的感受过去无从设想。"],
            ["Force every detail to replay.",
             "Even exact details may not bring perfection.",
             "细节全对上也不一定完美。"],
            ["Forget the metaphor in memories.",
             "The black lump's taste arrives with time.",
             "隐喻需要时间才能尝到。"]
        ],
        "shifts": [
            ["说计划只会说 plan",
             "用 the perfect-life list（完美计划）、the plan's outline（计划梗概）、childhood dream（少年愿望）"],
            ["说细节只会说 detail",
             "用 scarf for the snow（围巾看雪山）、radar-less reversing（倒车不看雷达）、spicy snacks（辣骨头）"],
            ["说感悟只会说 reflection",
             "用 the standard changes（标准在变）、taste the metaphor（尝到隐喻）、perfect standard（完美标准）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：十一岁、十几项、完美的生活方式、泡面、老坛酸菜、生日、麦当劳、午后、幽默大师、高了高、这么难喝、中不似少年油、清淡、大多数都实现了、一点都没有觉得完美、一项还没有完成、最丰满的计划、确切的目的地、对世界的想象、古早旅游网站、攻略、一篇、远处雪山的路、康定古龙村、遥远的地名、计划里、一辆模糊的车、隔壁、很酷的大叔、两条拉不拉多、顺路送我上学、坐车不是骑狗、前脸印象、凌厉、凯迪拉克SRX、开始凯迪拉克去康定、梗开、老SRX很少见、今年最新的XD5、完美的延续、计划主题、上夫嫁去、学嫁照、细节、帽尾巾看雪山、运气不太好、倒车史像这样、扒着副驾驶座位、探头、倒车不看雷达、常驻俩人标志、后背装满零食、辣骨头、乌宝长到一块五、快爆了、车里听、老人鱼海、不在意这个想法、视频土、11岁的时候评位可以、真的要睡车里、严格按照计划之行、晚安、住了酒店、细节一模一样、过去的想象、完美的我、世界奇妙物语、理想的火锅、男主合数、完美的火锅吃法、很酷、列下计划、最后、女友杀之、火锅吃法、完美标准差距太大、准备放弃求婚、妈妈端上一坨黑黑的东西、吃了一口、共度余生、隐喻什么、百思不得结、此刻强到了她、彩虹、纠结过去想象的完美生活、满足现在的自己、忽略、完美的标准、一直在变化、现在所经历的感受和风险、过去从没设想过的、生活最有名的一天、少女、另一种人、康定、凯迪拉克、雪山等。"
    },
    "7Kf60za3hgq": {
        "duration": "3:00", "topic": "拍摄 · 合影哲学",
        "practice": [
            ["说合影重要", "Group photos are vital social rituals."],
            ["说角度生动", "Another angle beats eye level."],
            ["说经验口诀", "Condense experience into mantras."],
            ["说拍的本质", "We capture story moments and vitality."],
            ["说磁吸自拍", "A magnetic case lets you join the frame."]
        ],
        "pitfalls": [
            ["Keep every group photo at eye level.",
             "Try another angle for more life.",
             "合影别总平视。"],
            ["Squeeze everyone into a line.",
             "Stagger and layer with mantras.",
             "前后错落比站一排好。"],
            ["Pose everyone stiffly.",
             "Move and bring vitality to the frame.",
             "合影需要动起来。"],
            ["Always be the one behind the camera.",
             "A magnetic case lets you appear too.",
             "别总在镜头后面。"],
            ["Forget what the photo preserves.",
             "Partings, emotions, and bonds live in it.",
             "合影定格聚散羁绊。"]
        ],
        "shifts": [
            ["说合影只会说 group photo",
             "用 social ritual（社交仪式）、window to the past（回看过去的窗口）、frozen at zero（定格为零）"],
            ["说拍照只会说 shoot",
             "用 another angle（另一个角度）、vitality（生命力）、story moments（故事瞬间）"],
            ["说设备只会说 device",
             "用 magnetic phone case（磁吸手机壳）、camera spot（机位）、any angle holds（任意角度停住）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：合影、人类社交活动、至关重要、退到多远、野生路人、使用工具、支架手机、换个角度、平视、更生动、排队领队、必经症、前后错误、两吨两战、三滴一缸、经验总结成口诀、文艺复兴运动、专辑封面、影视作品、急许领感、进化持续发生、向高处、想拍合影、拍什么、哲学、故事的瞬间、值得纪念的时刻、好起来动起来、需要生命力、包含了太多东西、去了哪儿、那时候那么瘦、还联系吗、聚散、情绪、羁绊、定格、倒数到零的那一刻、几年、自拍一场、唯一回看过去自己的窗口、帮大家拍为借口、逃避出境、没这个机会、磁吸手机壳、太方便、随时随地一放、任意角度停住、高处低处任意悬挂、磁吸、变身影机、不用麻烦路人、少一个人、值得记录的时刻、一部手机、加一块磁吸手机壳、心情舒畅、不喜欢合影、不多头目、下次再见等。"
    },
    "4XpXg2bHaz4": {
        "duration": "5:24", "topic": "Vlog · 新手进阶",
        "practice": [
            ["说转场取舍", "Be comfortable, or deliberate enough to serve the story."],
            ["说光线时间", "Wait for near-sunset to shoot."],
            ["说必须稳的画面", "Info-heavy wide one-shots need a gimbal."],
            ["说画面节奏", "Sparse shots flash, highlight-rich shots stay."],
            ["说新挑战", "Add one new challenge per video."]
        ],
        "pitfalls": [
            ["Copy trendy turn-head transitions.",
             "Make the transition comfortable or story-driven.",
             "刻意转场不适合新手。"],
            ["Film in flat noon light.",
             "Wait for near-sunset hours.",
             "选对时间光线就好看。"],
            ["Hand-hold wide one-shots.",
             "Use a gimbal for must-be-steady shots.",
             "一镜到底必须稳。"],
            ["Cut highlight-rich shots too short.",
             "Let the audience actually see them.",
             "亮点多的画面要放慢。"],
            ["Repeat the same skills forever.",
             "Add one new challenge each video.",
             "每期尝试一个新东西。"],
            ["Let repetition kill your passion.",
             "Protect passion as you stack progress.",
             "别让重复毁掉热情。"]
        ],
        "shifts": [
            ["说转场只会说 transition",
             "用 forced transitions（刻意转场）、scratch through a boot（隔靴搔痒）、contrast or link（反差或衔接）"],
            ["说光线只会说 light",
             "用 near-sunset hours（快夕阳时分）、right time（选对时间）、flat noon light（正午平光）"],
            ["说节奏只会说 rhythm",
             "用 sparse shots（稀疏画面）、highlight-rich scenes（亮点多的画面）、one new challenge（一个新挑战）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：刚开始拍视频、做Vlog、五件事、一口气全告诉我、定做一面景气、感谢他、第一件事、不要搞太刻意又没意思的转场、模仿别人、没说一句话、突然转着头、换一个机位、非常不适合我、镜头面前说话放不开、脑子里一直想着、这句话说完要转头、更加不自然、非常刻意、提醒观众、换了个场景换了个机位、两个场景之间没有联系也没有设计、隔着靴子脑痒、好像很努力、有点没劲、新手、换场景说话、让自己舒服一点、不用看镜头、不用太刻意的动作、一直在说话、接得上头、细节一点、慢慢往前推、跟着你动、稳定器、AI追踪自动跟随、换场景和机位变得更刻意、刻意到跟你的情节有关、主题、不在乎别人的看法、开机头、居下换你的表达、前一个机位、裸体的疯狂原始人、下一个机位、穿衣服的动作、狭窄的衣柜、广阔的海边、要么反差、要么闲间、换场景、变得有意思、边走边自拍、不适合自己的转场动作、舒服一些、第二件事、完全不注意光线、新手车灯光、要求太高、多做一步、等到快夕阳的时候再拍、相同的场景、没有完全不同的摄影技术、选对的时间都好看、第三件事、有的画面是必须要稳的、澎湖拉山、一路北上隔离、沿路、可惜的灯、信息又多、运动范围又大、一镜到底、手指拍、不用稳定器、一顿一顿、非常出息、必须要稳、拉出来揭示环境、环绕展示情绪、好不容易设计、因为不稳、味道不对、很可惜、第四件事、画面也有节奏、愿意跟你说实话的人、好几个、想要观众注意的地方、毫无反应、画面放得太短、稀稀少的画面、脚步特写、推向眼神、跟拍单一物品、快速地闪过、一群人众生白态、亮点很多、需要慢慢看、一晃而过、观众没看出来、白态、第五件事、每次增加一个新挑战、不光动画、稳定器运进、简单的致净、每一条片子尝试一个新东西、个人最受益的一点、两个关键词、进步和热情、一条一条视频堆穿、想练新的技能、下一条片子就是最好的时机、持续拍下去的关键因素、热情、最难保护的、千万别让重复毁掉它、做视频这件事上线太高了、爱他的原因、从零到一、每个细节多花一点心思、手机本零七品类、最典型的、从零到一的器材、刚入门、可接受的运算、比较专业的拍摄流程、浩瀚M7手机稳定器、两个喜欢的亮点、强大的AI跟拍、不需要连任何APP、比一个手势、牢牢锁住你、划个框、跟着物体、AI模块、RGB不光灯、拍视频直播、自定义轨迹、轨迹重复、非常实用、分身、轨迹延时、创意画面、控制器参数调整、功能选择、简单直观、许下来远程控制、监看画面、一个人拍摄很方便、M7电机、任何角度、不会卡住、强重很强、补光、麦克风、续航很强、反向充电、创意不受限制、手机拍视频或直播、好用的器材、重要的补件、走弯路很难了、快去拍吧、很期待等。"
    }
}

for slug, extra in EXTRA.items():
    p = DATA / f"{slug}.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    scenes_in = d["scenes"]

    full_scenes = []
    for i, s in enumerate(scenes_in, 1):
        title_cn = s.get("scene_zh", "")
        if len(title_cn) > 18:
            title_cn = title_cn[:18] + "…"
        title_en = s.get("scene_en", "")
        if len(title_en) > 42:
            title_en = title_en[:42] + "…"
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
            "title_cn": title_cn,
            "title_en": title_en,
            "time": s.get("time", "00:00"),
            "context": s.get("context", ""),
            "sentences": sentences,
            "paraphrase": paraphrase[:2],
            "speak": speak,
        })

    total_sents = sum(len(s["sentences"]) for s in full_scenes)
    words = []
    for s in full_scenes:
        for t in s["sentences"]:
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
            "title": d["title_zh"],
            "title_en": d["title_en"],
            "duration": extra["duration"],
            "scenes": len(full_scenes),
            "sentences": total_sents,
            "date": "2026-08-08",
            "platform": "xiaohongshu",
            "source_url": d.get("source_url", f"http://xhslink.cn/o/{slug}"),
            "topic": extra["topic"],
        },
        "scene_imgs": [f"shot-{i:02d}" for i in range(1, len(full_scenes) + 1)],
        "scenes": full_scenes,
        "practice": extra["practice"],
        "pitfalls": extra["pitfalls"],
        "shifts": extra["shifts"],
        "difficult_words": words,
        "footer_notes": extra["footer"],
    }
    p.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ {slug}: {len(full_scenes)} scenes, {total_sents} sents, {len(words)} words")
