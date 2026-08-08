#!/usr/bin/env python3
"""批21：将简化场景JSON补全为 gen-scene-en.py 所需的完整结构。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "2QUDGBzVGD3": {
        "duration": "33秒", "topic": "分镜 · 人物出场",
        "practice": [
            ["说出场定位", "The first seconds decide who the character is."],
            ["说五种出场", "Low angle, back reveal, eye close-up, scene emergence, signature action."],
            ["说视觉层级", "Protagonists shot low, supporting roles at eye level."],
            ["说避坑", "Don't use high angle on heroes or eye level on villains."],
            ["说环境出场", "Let the character emerge from the scene, not say hi to the camera."]
        ],
        "pitfalls": [
            ["Let every character enter the same way.",
             "Different entrances build distinction.",
             "出场方式要有区分度。"],
            ["Reveal everything at once.",
             "Backs, eyes, and scenes build suspense.",
             "先藏后露造悬念。"],
            ["Shoot heroes from above.",
             "High angles make protagonists look weak.",
             "主角慎用俯拍。"],
            ["Linger on the back too long.",
             "Turn to the face before viewers get bored.",
             "背影不要太长。"],
            ["Pick an entrance without character keywords.",
             "Define keywords first, then match the entrance.",
             "先定人物关键词。"]
        ],
        "shifts": [
            ["说出场只会说 entrance",
             "用 character positioning（人物定位）、first impression（第一印象）、visual hierarchy（视觉层级）"],
            ["说分镜只会说 storyboard",
             "用 narrative tool（叙事工具）、environment entrance（环境出场）、signature action（标志性动作）"],
            ["说悬念只会说 suspense",
             "用 layer-by-layer reveal（层层揭示）、mystery（神秘感）、back-to-face（背影转正面）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：人物出场设计、分镜设计中最关键的环节、短短几秒建立人物形象和观众期待、出场方式决定第一印象和情绪期待、黄金几秒、潜意识中完成定位、主角还是配角、好人还是反派、强大还是脆弱、不是来自台词而是来自出场镜头的设计、角度运动光线景别、五种经典出场方式、从下往上拍高大强势威严、先拍背影再转正面制造悬念和期待、眼睛特写再给全貌层层揭示、环境铺垫出场人物从环境中浮现融入叙事、标志性动作出场直接建立性格、所有人物的出场方式都一样、站着走进画面或坐着开始说话、从暗处走出来和从亮处走出来感受截然不同、根据人物定位设计出场是你的叙事工具、不要在主角出场时用俯拍显得弱小、不要在反派出场时用平拍不够压迫感、低角度向上拍摄威严强势大人物、神秘期待故事感重要人物揭晓、细腻层层揭示有深度的人物、融入感自然、性格鲜明记忆点强有个性的人物、先想好这个人物的关键词再选择匹配的出场方式、练习局部出场先拍手部特写再拉远露出全貌、尝试用环境出场代替直接对着镜头说大家好、主角用仰拍配角用平拍、利用镜头角度建立视觉层级、背影时间太长观众等得不耐烦、背影不超过几秒就转正面、出场和人物性格不匹配、娘娘腔角色用仰拍、叙事类视频短片人物介绍、出场方式要和整体视频风格一致、不需要区分人物的纯教程类视频、多人物群像需要更复杂的设计、设计人物的第一个镜头就是在叙事等。"
    },
    "71VnuCZA45g": {
        "duration": "28秒", "topic": "分镜 · 电影感构图",
        "practice": [
            ["说构图先行", "Cinematic feel comes from composition, not grading."],
            ["说四个核心", "Shot size, leading lines, foreground, negative space."],
            ["说一拍三景别", "Shoot at least three shot sizes of one scene."],
            ["说引导线终点", "Place the subject at the end of the leading line."],
            ["说留白呼吸", "Leave one side open for breathing room."]
        ],
        "pitfalls": [
            ["Rely only on color grading.",
             "Composition creates structural beauty grading can't.",
             "构图先于调色。"],
            ["Use one shot size everywhere.",
             "Shoot three sizes so post has options.",
             "景别要有层次。"],
            ["Let leading lines exit the frame.",
             "Point them at the subject.",
             "引导线指向主体。"],
            ["Keep the foreground too sharp.",
             "Soft blur keeps the subject the star.",
             "前景要适度虚化。"],
            ["Cram the frame with objects.",
             "Negative space serves the composition.",
             "留白服务构图。"]
        ],
        "shifts": [
            ["说电影感只会说 cinematic",
             "用 shot size（景别）、leading lines（引导线）、negative space（留白）"],
            ["说调色只会说 color grade",
             "用 structural beauty（结构性美感）、composition first（构图先行）、layers（层次）"],
            ["说拍摄只会说 shoot",
             "用 three sizes per scene（一拍三景别）、foreground blur（前景虚化）、art of subtraction（减法艺术）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：电影感构图、用几个简单的分镜构图技巧、让普通画面立刻具有电影感、不是靠后期调色而是靠拍摄时的构图意识、景别选择、善用引导线、电影感不只在后期调色、拍摄构图已经决定了、结构性美感、先学构图再谈调色、远景定氛围全景定关系中景定动作近景定情绪特写定细节、光影线条将观众视线引向主体、在前景放置虚化的物体树叶手臂、增加空间深度、给画面呼吸的空间不要在人物周围塞满东西、信息量递进、叙事性分镜、户外建筑场景、空间深度感、室内自然场景、人物偏一侧另一侧留空、呼吸感电影感、情绪对话场景、同一个场景至少拍三个景别远景特写、后期选择最好的、在拍摄环境里寻找引导线道路栏杆光影、让人物站在引导线的终点、每次拍摄找一个可以当前景的物体树叶杯子、放在镜头边缘制造层次、练习留白构图、所有镜头用同一个景别、至少拍三个景别让后期有选择、引导线把人引出画面、引导线应该指向主体而非画面外、前景太清晰抢了主体的风头、前景应该适度虚化、人物太小看不清、留白服务于构图而非为了留白而留白、短片人物拍摄等需要画面美感的视频、构图是工具不是教条、故意打破规则反而有惊喜、极限运动构图空间有限、新闻抓拍来不及构图、构图是做减法的艺术、不是把所有东西都放进画面、一拍三景别、加前景层次、后期调色解决一切、拍摄时就为电影感构图等。"
    },
    "APfchcnBYcv": {
        "duration": "1:08", "topic": "Vlog · 单人拍摄",
        "practice": [
            ["说单人难点", "The hard part is not knowing what to film, not technique."],
            ["说预设机位", "Preset angles at bedside, sink, and kitchen."],
            ["说前一晚准备", "Place cameras and write the script the night before."],
            ["说光线方向", "Window light, not overhead; mirror adds layers."],
            ["说紧凑节奏", "Keep the morning vlog to a few minutes."]
        ],
        "pitfalls": [
            ["Improvise what to shoot after waking.",
             "Write the script the night before.",
             "醒来才想拍什么就晚了。"],
            ["Run around adjusting positions.",
             "Preset each angle and shoot in order.",
             "机位要预设好。"],
            ["Use overhead light.",
             "Window light flatters morning shots.",
             "光线要来自窗户。"],
            ["Film a long rambling vlog.",
             "Keep the edit tight and short.",
             "节奏紧凑勿拖沓。"],
            ["Only think about gear.",
             "A phone and tripod work for zero cost.",
             "手机支架零成本。"]
        ],
        "shifts": [
            ["说机位只会说 camera angle",
             "用 preset angles（预设机位）、solo shooting（单人拍摄）、fixed position（固定机位）"],
            ["说脚本只会说 script",
             "用 the night before（前一晚）、shoot in order（按顺序拍摄）、follow the script（按图索骥）"],
            ["说视频只会说 vlog",
             "用 morning routine（起床日常）、first-person immersion（第一人称沉浸感）、tight edit（紧凑剪辑）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：一个简短的起床Vlog拍摄示范、全景相机或Nano、布置个人机位、脚本化拍摄、单人拍摄的核心思路、一个人如何拍自己醒来、预设多个机位床头洗手台厨房、按脚本时间线顺序拍摄、不需要来回跑调机位、后期紧凑剪辑省去废话直给重点、关键是提前设想每个环节的画面、前一晚就放好相机、可以放在任何你平时不敢放相机的地方、获得第一人称沉浸感、床头预设好角度、早上醒来直接按录制、光线要从窗户过来不要顶光、洗手台正面利用镜子反射增加画面层次、多用特写拍食物、给一个回头看家的镜头收尾、前一晚想好第二天起床后的几个拍摄环节、每个环节预设一个固定机位或手持方案、后期节奏要紧凑、起床Vlog的理想时长、观众耐心有限、光线是关键早上光线不好画面会很暗淡、适用于生活类日常记录极简风格、需要能预设机位的小型设备、手机加支架是零成本替代方案、脚本是单人拍摄的基础、一个人拍自己最难的不是技术而是不知道拍什么、花几分钟在前一晚写好脚本、第二天按图索骥、素材组织效率提升、前晚写脚本第二天高效拍摄等。"
    },
    "7ttCfEFkxco": {
        "duration": "2:51", "topic": "拍摄 · 导演技法",
        "practice": [
            ["说景别表达", "Medium shot shows actions; waist-up emphasizes the person."],
            ["说角度态度", "Low angle projects power; high angle diminishes it."],
            ["说运镜关系", "Pan connects people; tracking heightens risk."],
            ["说升格降格", "High-speed adds detail; low-speed blurs into light streaks."],
            ["说技术服务艺术", "Effects serve the director's imagination."]
        ],
        "pitfalls": [
            ["Shoot every subject at eye level.",
             "Angles express power, weakness, or judgment.",
             "角度传递态度。"],
            ["Cut without spatial logic.",
             "Pans, pushes, and tracks structure relationships.",
             "运镜表达关系。"],
            ["Ignore speed effects.",
             "High-speed adds detail; low-speed makes streaks.",
             "升格降格都是语言。"],
            ["Let effects lead the art.",
             "Technology should serve art.",
             "让技术服务艺术。"],
            ["Overlook lighting and music.",
             "They express mood and direct the image.",
             "灯光配乐表达情绪。"]
        ],
        "shifts": [
            ["说镜头只会说 shot",
             "用 shot size（景别）、ground-level angle（贴地角度）、bird's-eye view（鸟瞰）"],
            ["说运镜只会说 camera move",
             "用 pan（摇）、push-in（推）、tracking shot（跟拍）、rising shot（上升）"],
            ["说效果只会说 effect",
             "用 high-speed filming（升格）、low-speed filming（降格）、light streaks（流光效果）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：传警、人物的整顶、中拳紧膝上、适合表达人物的动作以及周遭的关系、中紧腰上、利于强调人物本身的叙事、紧紧减少减少注意力分散、写出乎人与面目情绪、贴地角度看不到人物的整顶、贴地角度看不到我是谁、要的就是这种神秘感、两拍镜头彰显主体的力量、五拍镜头削弱被拍摄者的力量、鸟看镜头彰显出审判感、摇建立不同人物之间的联系、换个时间换个地点完成空间的过渡、推展示更多的细节、拉扩大画面信息量让场景更具张力、跟踪镜头强调风险感、仿佛置身场景之中、让观众沉浸和陷入场景、深格通过拉长细致时间增加了细节的颗粒度、转瞬即逝却又不可错过、降格可以制造强烈的模糊和流光效果、墨镜王的惯用技巧、灯光色彩可以表达人物情绪也可以渲染氛围、配乐是画面的导演、万物皆有值得的配乐、特效实现导演天马行空的想象、让技术服务艺术、跑的特效已被观众发现、中人皆可创作的时代、你觉得什么是道理等。"
    },
    "3yV726SaVeI": {
        "duration": "11秒", "topic": "拍摄 · 视角升维",
        "practice": [
            ["说高级感来源", "Premium feel comes from the angle, not the gear."],
            ["说默认视角陷阱", "Standing height is the default—and most boring—view."],
            ["说非日常视角", "Any view viewers don't see daily feels premium."],
            ["说演示的力量", "Showing the difference beats telling how."],
            ["说立刻行动", "Shoot one scene at several angles and compare."]
        ],
        "pitfalls": [
            ["Blame your equipment.",
             "Premium frames differ by one angle.",
             "高级感与设备无关。"],
            ["Stay at standing height.",
             "Crouch, raise, or move for freshness.",
             "别站身高位置拍。"],
            ["Add extreme angles everywhere.",
             "Even a little shift out of default works.",
             "一点点偏移就够。"],
            ["Explain instead of showing.",
             "Demonstration outweighs explanation.",
             "示范胜过解释。"],
            ["Over-complicate for effect.",
             "Simple non-default angles feel premium.",
             "简单偏移即高级。"]
        ],
        "shifts": [
            ["说拍摄只会说 shoot",
             "用 non-everyday angle（非日常视角）、standing height（身高位置）、visual contrast（视觉对比）"],
            ["说高级感只会说 premium",
             "用 the angle you choose（你选的视角）、a fresh feel（新鲜感）、a different view（不同体验）"],
            ["说教学只会说 teach",
             "用 demonstration（演示）、show the difference（展示差距）、visual comparison（画面对比）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：视频这么拍又简单又高级、日常画面升维指南、极短的时间演示如何用简单的拍摄手法让普通场景呈现出高级感、角度运动和构图的新鲜组合、开场即展示对比效果、同样的场景不同的拍摄方式带来截然不同的视觉质感、高级感不来自设备升级而来自视角和运镜方式的变化、换一个角度、普通人拍视频最常见的陷阱是站在自己的身高位置平拍、人眼默认视角也是最平淡无奇的视角、蹲下来举高移动起来、同样的场景瞬间产生新鲜感、不是设备的问题、离开默认的观看位置、高级感的本质是非日常视角、观众每天看到的世界都是平视的、任何一个不同的视觉体验他就觉得高级了、每一个镜头必须有一个明确的角度、低角度鸟瞰快速推进透过某个前景物体拍、秒的极简教学最大的信息密度是示范不是解说、只用画面对比前后效果传达信息几乎不需要语言解释、演示的力量远超解释、我给你看区别有多大、极短内容的有效性靠的是视觉对比的直接冲击、不是语言的完整度、平视固定拍摄视觉新鲜感低、人眼日常就是这个角度、高观众看到了平时看不到的画面、简单的稳定性控制即可、低蹲举走、用手机拍同一个场景用几种角度、平视低角度手机贴地高度角度穿过某个物体前景、对比四段画面感受不同视角带来的叙事感差异、下一次拍视频时强制自己每个镜头都不站在自己的身高位置拍、不要为了高级感而过度复杂化、关键是从默认视角中走出来哪怕只是一点点、适用场景产品展示旅行记录生活碎片、固定内容的标准化录制如课程视频的固定机位、需要画面一致性作为信息基准、高级画面和普通画面的差距往往只差一个不站在自己身高位置上拍、今天拍你的咖啡窗边试试从来没试过的角度、对比之后选出最让你惊喜的一个角度记住它、这将成为你的视觉风格的一部分、我的设备不够好所以拍不高级、高级感来自你为自己和观众选择了一个看世界的新角度等。"
    },
    "6q4PNxI9gMY": {
        "duration": "16秒", "topic": "拍摄 · 机位语言",
        "practice": [
            ["说机位即态度", "Every camera position carries a narrative attitude."],
            ["说8个机位", "Eye level equals; low angle empowers; high angle weakens."],
            ["说背后跟拍", "Back tracking brings immersion and the unknown."],
            ["说顶拍展示", "Top-down is the god's-eye view."],
            ["说叙事动机", "Every position change needs a narrative reason."]
        ],
        "pitfalls": [
            ["Shoot everything at eye level.",
             "Mix low, high, and level angles.",
             "全平视最平淡。"],
            ["Overdo the low angle.",
             "Extreme tilt can distort the subject.",
             "仰拍角度别太夸张。"],
            ["Use high angle unintentionally.",
             "Unless you mean fragile, avoid it.",
             "俯拍暗示弱小。"],
            ["Cut positions without reason.",
             "Every switch needs narrative motivation.",
             "机位切换要有理由。"],
            ["Forget the observer stance.",
             "Side eye-level suits documentary records.",
             "侧面适合纪实。"]
        ],
        "shifts": [
            ["说机位只会说 camera position",
             "用 narrative stance（叙事立场）、eye level（平视）、god's-eye view（上帝视角）"],
            ["说角度只会说 angle",
             "用 low angle（低角度）、high angle（高角度）、over-the-shoulder（过肩镜头）"],
            ["说拍摄只会说 shoot",
             "用 back tracking（背后跟拍）、top-down（顶拍）、three positions（三种机位）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：16秒学会8个拍摄机位、从高角度到低角度从正面到侧面、不同机位带来的视觉语言完全不同、8种视觉语言、高角度脆弱低角度强大、机位选择就是用镜头说话、每个角度都在传递一种态度、理解每个机位的视觉语言、在拍摄中有意识地选择、镜头的语法、机位不仅仅是相机架在哪里的问题、它决定了观众和画面主体的关系、高角度让观众俯视主体主体显得脆弱渺小、低角度让观众仰视主体主体显得强大重要、平视让观众平等看待主体、正面平视最常用建立平等关系、正面仰拍主体强大威严、正面俯拍主体脆弱渺小、侧面平视观察者视角、背后跟拍代入感未知感、过肩镜头对话感亲密感人物对话互动、低角度特写强调细节和质感产品展示美食、顶拍上帝视角全貌展示开箱全景展示、8个机位的本质是8种叙事立场、你站在什么位置拍就是在告诉观众你该怎么看这个人、与眼睛同高平等客观、仰视崇拜主角亮相英雄感、俯视审视弱势角色失败感、旁观观察纪录纪实、代入悬念、对话亲密、同一个场景用至少几个不同机位拍摄对比画面的感觉差异、拍摄人物时尝试仰拍感受画面气质的变化、加入一段背后跟拍用三脚架或朋友帮忙增加代入感、食物时尝试鸟瞰机位垂直上方拍摄增加视觉多样性、所有镜头都是平视、有意识地混合高低三种角度、仰拍角度太大、俯拍时人物显得很矮、如果不是故意表达脆弱渺小慎用俯拍、机位变化太频繁观众晕头转向、每切换机位要有叙事理由、所有视频拍摄场景无论用什么设备机位的选择逻辑一样、机位的切换需要有叙事动机不是无意义地切来切去、固定机位的直播虽可调整但切换频率有限、一拍三机位、加入背后跟拍、练习鸟瞰机位、随便找个角度拍、这个机位在表达什么叙事立场等。"
    },
    "Ai0ipBFpPCn": {
        "duration": "1:24", "topic": "创作 · 模仿入门",
        "practice": [
            ["说模仿起点", "Imitation is a common starting point in video creation."],
            ["说临摹类比", "Like copying calligraphy, study masters' editing."],
            ["说非抄袭", "Imitation absorbs techniques and adds your creativity."],
            ["说巨人肩膀", "Great creators draw from the classics."],
            ["说超越飞跃", "The goal is to surpass those you learned from."]
        ],
        "pitfalls": [
            ["Go straight for a blockbuster.",
             "Start by studying masters' techniques.",
             "一上来拍大片太难。"],
            ["Confuse imitation with plagiarism.",
             "Absorb techniques, then add creativity.",
             "模仿并非抄袭。"],
            ["Copy without discovering yourself.",
             "Find what you like and excel at.",
             "模仿中发现自己。"],
            ["Stay at imitation forever.",
             "The goal is original creation.",
             "模仿只是起点。"],
            ["Call imitation laziness.",
             "It lays a solid creative foundation.",
             "模仿是打地基。"]
        ],
        "shifts": [
            ["说模仿只会说 copy",
             "用 imitation（模仿）、copying calligraphy（临摹）、absorb techniques（吸收技法）"],
            ["说创作只会说 create",
             "用 your own creativity（个人创意）、distinctive style（独特风格）、original creator（原创者）"],
            ["说学习只会说 learn",
             "用 stand on giants' shoulders（站在巨人肩上）、surpass others（超越他人）、solid foundation（坚实地基）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：很多人都在问为什么我的成长速度会这么快、答案早就在我的视频中表现出来、视频创作中模仿是非常常见的起点、模仿的过程让我们在最短的时间内掌握构图节奏剪辑配乐等核心技巧、就像写字画画都是从淋膜开始的、学习视频剪辑也一样、一上来就拍大片难度极高、不如静下心来研究一些大神的剪辑手法、模仿并非抄袭、而是在吸收技法后加上个人的创意、在这个过程中可能就会慢慢发现自己尤其喜欢哪些内容、擅长哪种表现手法、也会渐渐形成与众不同的创作风格和视角、这本质上是模仿到创作的过渡、也需要在模仿中保持理性的思考、很多伟大的创作者都是从模仿开始的、他们站在巨人的肩膀上、从经典中汲取灵感和经验、才逐渐提炼出独属于自己的风格、但是模仿只能是起点、最终目标是成为独具特色的原创者、实现从学习他人到超越他人的飞跃、模仿并不是偷懒、而是在为自己的创意之路打好坚实的地基、或许下一位成功的视频创作者说不定就正在练习模仿着你等。"
    },
    "7gH9YeB2RYT": {
        "duration": "2:15", "topic": "拍摄 · 电影运镜",
        "practice": [
            ["说前推加摇", "Push-in plus upward tilt makes one dynamic shot."],
            ["说横移层次", "Lateral moves need a foreground for layers."],
            ["说环绕稳定", "Half-crouch walk keeps orbits steady."],
            ["说慢推情绪", "Slow push-ins heighten sad or thinking moments."],
            ["说上升揭示", "A slow rise reveals hidden content."]
        ],
        "pitfalls": [
            ["Combine moves without purpose.",
             "Push plus tilt gives one dynamic frame.",
             "复合运镜更动感。"],
            ["Shoot lateral moves without foreground.",
             "Foreground adds the layers.",
             "横移要有前景。"],
            ["Walk upright during orbits.",
             "Half-crouch keeps the frame steady.",
             "半蹲环绕更稳。"],
            ["Push fast for emotional scenes.",
             "Slow push-ins heighten emotion.",
             "情绪用慢推。"],
            ["Rise without a reveal.",
             "Slow rises mask and reveal content.",
             "上升用于揭示。"]
        ],
        "shifts": [
            ["说运镜只会说 camera move",
             "用 push-in（前推）、lateral move（横移）、orbit shot（环绕）、rising shot（上升）"],
            ["说稳定器只会说 gimbal",
             "用 joystick（摇杆）、extension rod（延长杆）、half-crouch walk（半蹲前进）"],
            ["说情绪只会说 mood",
             "用 heighten emotion（增强情绪）、reveal hidden content（揭露隐藏画面）、focus shift（焦点转换）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：今天我会用手机和云台教大家几种电影中常见的运镜方式、第一个是前推加上摇镜头、拿着稳定器向前走的过程中同时用手指往上推动摇杆、一个镜头中包含了前推和向上摇的两个镜头运动、画面整体会变得十分动感、大疆Osmo Mobile 6、第二个是横移镜头、利用稳定器自带的延长杆翻转云台进行拍摄、一定要注意配合上前景才能产生有层次的画面、横移镜头在电影中经常会出现、跟随人物进行左右之间的移动、第三个是环绕镜头、围绕主体进行拍摄、脚步其实是半蹲前进的状态、半蹲的前进能够给到我们更稳定的画面、云台始终围绕着主体进行拍摄、看看电影中是如何运用这些镜头的、第四个是前推镜头、前推镜头非常简单但是用法却非常多、快速的向前推进、缓慢的向前推进、人物伤感或者思考的时刻、导演都会用缓慢前推去进行人物情绪的增强、第五个是上升镜头、使用稳定器的技巧、完全蹲下然后运用脚和身体同时往上提升、画面出来更加的平稳、缓慢的镜头上升一般在电影中用作画面遮罩、揭露隐藏画面、揭露了一只鸽子在雕塑头上搞事情、这个运镜也可以用作人物行动的跟随、最后一个镜头是横移焦点转换镜头、通过横移的镜头运动在两个视觉焦点之间进行切换、焦点在这个陶瓷人脸上、通过横移把焦点切换到后面的雕塑上等。"
    },
    "7dCNCLVzS4n": {
        "duration": "1:05", "topic": "器材 · 稳定器模式",
        "practice": [
            ["说平移跟随", "PF mode only pans left and right."],
            ["说刷锅环绕", "Orbit moves use PF, mostly for environment."],
            ["说长焦配合", "Pair PF orbits with telephoto for compression."],
            ["说与锁定对比", "PF shows more environment than lock mode."],
            ["说模式选择", "Moving action uses lock; surroundings use PF."]
        ],
        "pitfalls": [
            ["Confuse PF with lock mode.",
             "PF pans; lock freezes the camera's heading.",
             "PF只平移。"],
            ["Use PF for fast action.",
             "Lock mode suits moving subjects.",
             "运动状态用锁定。"],
            ["Expect PF to compress space.",
             "Add a telephoto lens for compression.",
             "压缩感靠长焦。"],
            ["Use one mode for everything.",
             "Choose by what the frame must show.",
             "按目的选模式。"],
            ["Forget PF for environment reveals.",
             "It's the go-to for surroundings.",
             "交代环境选PF。"]
        ],
        "shifts": [
            ["说模式只会说 mode",
             "用 pan-follow（平移跟随）、lock mode（锁定模式）、orbit move（环绕运镜）"],
            ["说运镜只会说 move",
             "用 establish surroundings（交代环境）、fixed-point lateral（定点横向运镜）、pan around（刷锅）"],
            ["说镜头只会说 lens",
             "用 telephoto（长焦）、spatial compression（空间压缩）、70-200mm（70-200镜头）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：看完这期视频教你分清稳定器两大模式、又是你们的瑞角、平移跟随是大家最常用到的稳定器模式、在这个模式下稳定器只会进行左右方向的平移移动、使用最多的场景就是环绕运镜也就是我们熟知的刷锅、不管是小范围的轻微环绕还是环绕主体的整体运镜都可以用到PF的平移跟随模式、这样的运镜更多的起到交代周围环境的作用、展现出人物所在的场景内容、如果想要突出人物主体的环绕运镜也可以搭配长焦镜头进行拍摄、空间的压缩感会更强、我用的70-200镜头加上机身大概不到2000克、一天的拍摄下来承重也完全没问题、和之前提到的锁定模式不同、平移跟随模式拍摄出来的效果更多的是一个定点的横向运镜、比起锁定模式可以展示更多的环境内容、如果画面是运动状态的展示就用锁定模式、如果画面重点是周围环境的展示就选平移跟随模式等。"
    },
    "7qP7vTOCiiJ": {
        "duration": "50秒", "topic": "器材 · 全域跟随",
        "practice": [
            ["说全域跟随", "All three axes follow; great for creative shots."],
            ["说360度旋转", "You can switch to a manual 360-degree mode."],
            ["说加长轴臂", "The extended tilt arm frees filter mounting."],
            ["说练习步骤", "Master lock and PF first, then widen the range."],
            ["说画面上限", "Fluency in all-axis sets your footage's ceiling."]
        ],
        "pitfalls": [
            ["Jump straight into all-axis mode.",
             "Master lock and pan-follow first.",
             "先掌握基础模式。"],
            ["Start with big movements.",
             "Practice small ranges, then expand.",
             "从小范围练起。"],
            ["Ignore your footing.",
             "Big moves need stable steps and balance.",
             "大幅运动注意平衡。"],
            ["Only use the simplest modes.",
             "All-axis mode unlocks your ceiling.",
             "全域跟随决定上限。"],
            ["Mount filters that hit the axis.",
             "The extended arm solves that.",
             "加长轴臂解决滤镜。"]
        ],
        "shifts": [
            ["说稳定器只会说 gimbal",
             "用 all-axis follow（全域跟随）、pan-follow（平移跟随）、lock mode（锁定模式）"],
            ["说运动只会说 move",
             "用 360-degree rotation（360度旋转）、slow-shutter shot（慢门镜头）、tension and impact（张力冲击力）"],
            ["说学习只会说 learn",
             "用 start small（小范围练习）、zero-lag settings（零延迟设置）、the ceiling of your footage（画面上限）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：稳定器全域跟随模式三轴联动进阶、新手最头疼但效果最出彩的模式、三轴同时跟随运动、更大范围多角度360度旋转的运动、最适合拍摄慢门镜头创作类画面、配合云台零延迟设置画面极具张力和冲击力、加长了俯仰轴臂解决了装滤镜后碰到横滚轴的问题、全域跟随是稳定器使用最少的模式但恰恰是最能出片最具创作潜力的模式、从少到多锁定到全域自由度递增上手难度递增、平移三轴同时跟随、可手动切换为360度旋转自定义模式、稳定器可以更大幅度多角度运动、零延迟设置张力冲击力、新手最头疼但最值得学、先掌握锁定和平移跟随再尝试全域跟随、极致张力画面、全域模式下安装滤镜不再受限、先小范围练习再逐步扩大运动幅度、不要一上来就用全域跟随、全域模式下运动幅度大注意脚步稳定和身体平衡、滤镜后可能碰到横滚轴已解决此问题、适用场景创作类慢门镜头旋转视角特效需要画面冲击力的场景、新手日常跟拍需要稳定构图的固定线路拍摄、进阶标志能熟练使用全域跟随意味着你已经真正掌握了稳定器、全域跟随是你用得最少但最值得练习的模式、它决定了你画面的上限等。"
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
