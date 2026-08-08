#!/usr/bin/env python3
"""批20：将简化场景JSON补全为 gen-scene-en.py 所需的完整结构。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "2nIYM8mRzxo": {
        "duration": "6:08", "topic": "剪辑 · 画面联系",
        "practice": [
            ["说联系的定义", "Connections between shots make sequences feel comfortable."],
            ["说视觉焦点联系", "Pulling the eye to one spot creates a comfortable feel."],
            ["说动势联系", "Changing people, scenes, or outfits all rely on motion links."],
            ["说声音联系", "Sound effects and music can subtly bridge two shots."],
            ["说表达联系", "A tree followed by an axe triggers words in your mind."]
        ],
        "pitfalls": [
            ["Only chase visual comfort.",
             "Expressive connections can create new meaning.",
             "只追求视觉舒适不够。"],
            ["Think each shot stands alone.",
             "Shots connect through focus, motion, color, and sound.",
             "镜头之间需要联系。"],
            ["Force seamless links.",
             "Connections never need to be seamless.",
             "联系无需严丝合缝。"],
            ["Overthink the formulas.",
             "Tear them up once you understand the idea.",
             "公式理解后要撕碎。"],
            ["Shoot without saving clips.",
             "Today's clips may find their story years later.",
             "此刻片段未来有用。"]
        ],
        "shifts": [
            ["说转场只会说 transition",
             "用 connection（联系）、visual focus（视觉焦点）、action link（动作联系）"],
            ["说剪辑只会说 edit",
             "用 sound bridge（声音桥梁）、expressive link（表达联系）、seamless（严丝合缝）"],
            ["说创作只会说 create",
             "用 1+1>2（一加一大于二）、serve the story（服务故事）、your link with the world（与世界的联系）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：从浅到深理解视频创作、这个词就是联系、画面之间的联系、视觉焦点的联系、视线引向同一个地方、舒适的观感、第一眼注意的位置、动势、动作的联系、换人换场景换衣服、底层原理、颜色、相同的颜色、同一个色调、形状、声音的联系、尾音重叠、音效上产生微妙关联、音乐和画面之间的联系、慢动作、歌词和台词、思路的世界、新的表达、一棵树、纸、斧头、词汇产生、服务你的故事、1加1大于2、排列组合、表艺这一层、密密麻麻、撕碎、扔进垃圾桶、严丝合缝、振耳欲聋的缠绵、铸铁人像、若有若无的联系、约翰威尔逊、裸机540克、拍下你看到的、五年之后、完美联系的故事、90%靠你自己、你与世界的联系、尼康ZR、Red色彩、6K60帧、12bit色深、4英寸屏幕、原生ISO 6400、构图裁切、颜色联系、DAM、4K120帧、呼吸补偿等。"
    },
    "AUT0mrcxlP6": {
        "duration": "2:10", "topic": "剪辑 · 定格动画",
        "practice": [
            ["说五张照片", "Five photos are enough for a simple stop-motion."],
            ["说拍得越多越丝滑", "More frames mean smoother motion."],
            ["说标题动画", "Five frames can pop in your Vlog title."],
            ["说两帧抖动", "Two frames wiggled side to side look like talking."],
            ["说换表情", "Swap expressions to avoid the silly look."]
        ],
        "pitfalls": [
            ["Think stop-motion needs complex software.",
             "Five photos are enough to start.",
             "五张照片就能入门。"],
            ["Shoot once and toss the footage.",
             "Reusing footage saves huge effort.",
             "素材重复利用很香。"],
            ["Only cover the lens for transitions.",
             "Use shapes, textures, and backgrounds too.",
             "遮挡素材要多样。"],
            ["Keep one expression for the wiggle.",
             "Swapping expressions adds life.",
             "抖动时换表情更有趣。"],
            ["Forget music sync.",
             "Matching the beat makes it playful.",
             "卡点音乐更有趣。"]
        ],
        "shifts": [
            ["说动画只会说 animation",
             "用 stop-motion（定格动画）、frame-by-frame（逐帧）、squash（压扁）"],
            ["说拍摄只会说 shoot",
             "用 five photos（五张照片）、reuse footage（复用素材）、title pop-in（标题出现）"],
            ["说字幕只会说 subtitle",
             "用 wiggle to talk（抖动说话）、expression swap（换表情）、sync to the beat（卡点）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：定格动画、简单到爆炸、五张照片、压扁、拍得越多越丝滑、素材重复利用、千变万化、做标记、文字出场、Vlog标题出现、柔直展开、原理一样、背景动起来、放置文字、材质变化、更简单的方法、两张就够、左右抖两下、像在说话、换几个表情、Wake up、body to the beat、body to set you free等。"
    },
    "1jVfLpUmn0g": {
        "duration": "1:48", "topic": "Vlog · 不露脸技巧",
        "practice": [
            ["说分屏融合", "Split the screen so the top half fuses with your body."],
            ["说整体抠图", "Cut your whole body out to blend with the environment."],
            ["说面具遮挡", "A distinctive mask or object makes you memorable."],
            ["说背影脚步", "Shoot your back or footsteps for the whole film."],
            ["说露脸好处", "Only open faces keep memories vivid years later."]
        ],
        "pitfalls": [
            ["Avoid the face at any cost.",
             "AI can change faces, but hiding has its own perks.",
             "不露脸也有其好处。"],
            ["Let masks distract from content.",
             "Pick props that match your vlog's theme.",
             "遮挡物要贴合主题。"],
            ["Forget the memory value of showing up.",
             "Open faces make recollections vivid.",
             "露脸保留真实回忆。"],
            ["Rely only on post-production tricks.",
             "Backs and footsteps are classic alternatives.",
             "背影脚步同样经典。"],
            ["Regret the footage you hid.",
             "You'll only regret filming too little.",
             "只会遗憾拍得不够多。"]
        ],
        "shifts": [
            ["说露脸只会说 show face",
             "用 split screen（分屏）、cutout（抠图）、cover the face（遮挡脸部）"],
            ["说创意只会说 creative",
             "用 playful fusion（有趣融合）、theme-matched props（贴合主题道具）、part of the environment（环境的一部分）"],
            ["说回忆只会说 memory",
             "用 vivid memories（清晰回忆）、truest memories（最真实的回忆）、film more（拍更多）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：不想在视频里露脸、方法太多、分屏、上半部分、身体产生有趣的融合、放弃融合、整个身体抠出来、环境中的地面、做个转场、带上面具、面具足够特别、观众记住你、后期找个东西挡住脸、树叶车票落花、根据vlog主题变化、传统一点、转过身去、全片都拍背影、脚步、时代变了、AI千变万化、方法好处多到爆炸、暂缓容貌焦虑、画面更有创意、大方露脸的好处、可怜的一个、最真实的回忆、第一次吃到那个东西的反应、笑得这么傻、刚从高原回来、晒得够黑、动作浮夸表情很大、真年轻、很多年以后、硬盘不知去向、大大方方展出来的面孔、回忆清晰地浮现、不会懊悔、遗憾拍得不够多、拿起它、把镜头对向自己、大疆Pocket4P等。"
    },
    "8FNenLTO0N8": {
        "duration": "3:56", "topic": "器材 · Vivo X300 Ultra",
        "practice": [
            ["说长焦拼接", "A 400mm telephoto plus primes gives flexible framings."],
            ["说慢动作叙事", "4K120fps amplifies emotions and catches fleeting details."],
            ["说手机Log调色", "10-bit Log on a phone leaves headroom for grading."],
            ["说一键电影感", "A Film Look filter gives cinematic results instantly."],
            ["说两亿像素裁切", "200MP portraits crop into clean close-ups."]
        ],
        "pitfalls": [
            ["Think only cinema cameras grade in Log.",
             "This phone shoots 10-bit Log across all specs.",
             "手机也能拍Log。"],
            ["Miss fleeting travel moments.",
             "4K120fps slow motion catches them from your seat.",
             "慢动作捕捉瞬间。"],
            ["Assume you must learn color grading.",
             "A Film Look filter delivers cinematic tones instantly.",
             "不会调色也能出片。"],
            ["Forget flexible framing on a phone.",
             "Three primes plus long telephoto cover many framings.",
             "多焦段灵活构图。"],
            ["Crop losing quality.",
             "200MP lets you crop freely into sharp close-ups.",
             "高像素随意裁切。"]
        ],
        "shifts": [
            ["说长焦只会说 telephoto",
             "用 400mm zoom（400毫米长焦）、prime lenses（定焦镜头）、stitch shots（拼接画面）"],
            ["说慢动作只会说 slow motion",
             "用 4K120fps、amplify emotions（放大情绪）、fleeting details（转瞬即逝的细节）"],
            ["说调色只会说 color grade",
             "用 10-bit Log、Film Look filter（电影感滤镜）、grade on site（现场调色）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：旅行中千万要小心这样的椅子、精疲力尽、会偷手机的小偷、一部手机、再偷一下另一边、一根铁棒、三摄镜头、太强了、VIVO X300 Ultra、400毫米长焦、王炸组合、一目千里、三颗大师定焦镜头、不同景别、拼到一起、游远道径放大、旅行片头、那个人的望远镜、作弊呀、怎么要望远镜、为什么看起来都这么有故事感、因为慢、全焦段4K120帧、旅行中的情绪放大、增添诗意、转瞬即逝、来不及追赶的细节、坐在原地、一网打尽、这可是手机呀、颜色怎么可以、10bit Log、足够的空间、天气情绪场景、调出对应的风格、Vivo Pad 6 Pro、现场调给你看、手绘动画、直接电影感、郑重夏淮呀、film look滤镜的美丽、不会调色也可以原地出片、帮我拍张照、戴紧的全身的还有大脸的特写、傻了吧过不去了吧、人家要近的、两亿人像随意裁切、拉大变成特写、主体放在不同的位置、都很清晰、原地拍一张等于好几张、服了吗、什么拍法想学啊我教你等。"
    },
    "9RCFfD2gA37": {
        "duration": "4:58", "topic": "旅行 · 找灵感",
        "practice": [
            ["说第一件事", "Visit classic story settings with plenty of people."],
            ["说第二件事", "Watch strangers and weave stories about them."],
            ["说第三件事", "Ask young filmmakers what they do without inspiration."],
            ["说打破routine", "Routines need loosening to spark ideas."],
            ["说走出去", "Inspiration comes from hearing stories and new experiences."]
        ],
        "pitfalls": [
            ["Wait for inspiration at home.",
             "Go where stories happen and people gather.",
             "灵感来自现场。"],
            ["Record without observing.",
             "Weave stories about strangers in your head.",
             "观察路人编故事。"],
            ["Copy others' methods blindly.",
             "Ask creators—their answers vary wildly.",
             "创作者各有妙招。"],
            ["Keep an iron routine.",
             "Small breaks in routine loosen your life.",
             "固定生活要松动。"],
            ["Eat and scroll for ideas.",
             "Go out to hear stories and try new things.",
             "走出去才有灵感。"]
        ],
        "shifts": [
            ["说灵感只会说 inspiration",
             "用 story settings（故事场景）、observe strangers（观察路人）、break the routine（打破routine）"],
            ["说拍摄只会说 shoot",
             "用 weave a story（编故事）、ask creators（问创作者）、document real life（记录真实）"],
            ["说旅行只会说 travel",
             "用 people-watching（观察人群）、unexpected visits（突然造访）、new experiences（新鲜经历）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：洛杉矶、世界电影之都、空气充斥着灵感和故事、一个仓白的报告、完全不知道拍什么、一种折磨、灵感获取之难、三件事、故事发生的经典场景、人一定要够多、游乐场、塞兰摩尼卡、码头沙滩、日落时分、博物馆、有趣的人、驻足、疯狂观察路人、脑中给他们编一段故事、刚刚长出的双腿、迈进电影博物馆、大师所望、一对年长的美人鱼情侣、七十岁修炼成人、厌倦了牛腿的生活、截然不同的伴侣、更资深的牛仔、变色龙果实、自动穿上跟环境配色一样的衣服、大白沙斩、觉得自己过得很惨、海鸥、飞到美国了、数条吃、班里那个每天被欺负的疏灾同学、开始滑档、长得太像老牌导演、拍他紧张手抖、代码以奇怪的方式运行起来、时间机器、传送到这个时空、索尼最新65毫米电影摄影机、全新传感器、全画负的2.2倍、机身分体、Future Film Maker Wars、年轻、没有灵感的时候会做什么、一直在工作、一个很长的洗澡、肩膀变得很厉害、有点感情、更舒服、音乐绝对的、认识David Bowie、认识我的女朋友、打电话、女朋友Jack、同一家店吃早餐、没有开门、周而复始的生活被打破了、烧饼换成了油条、SFF颁奖晚宴、衣服很紧、年轻的电影人、掌声雷动、灯光变化、跳清了、图定、颁奖进寻常之外的场合、开始松动、突然造访八年未见的朋友、混进一场庆祝游行、夜里和一帮人、铁天圈店、吃东西怎么会有灵感、出去要听铁天圈讲故事、经历新鲜的事情等。"
    },
    "tNfxFSZ6zP": {
        "duration": "5:36", "topic": "拍摄 · 主体醒目",
        "practice": [
            ["说颜色对比", "Standout color against large blocks makes you pop."],
            ["说去色保留", "Keep only the subject's color for one mood."],
            ["说大色块标题", "Big color fields are great for title placement."],
            ["说引导线", "Ropes, roads, and tunnels all become leading lines."],
            ["说用光突出", "Place the subject in the frame's only lit zone."]
        ],
        "pitfalls": [
            ["Clutter the frame with many elements.",
             "Standout color on plain blocks pops best.",
             "元素多反而杂乱。"],
            ["Judge brightness by gut feeling.",
             "Use plain backgrounds and contrast.",
             "用色块对比出主体。"],
            ["Only use bokeh to stand out.",
             "Composition and light matter more.",
             "构图用光同样重要。"],
            ["Rely on gear over design.",
             "Skills beat gear in most cases.",
             "技巧胜过器材。"],
            ["Forget post-light boosting.",
             "A lamp or flashlight, boosted in post, focuses the eye.",
             "后期加强光源。"]
        ],
        "shifts": [
            ["说突出只会说 stand out",
             "用 visual focus（视觉焦点）、leading lines（引导线）、lit zone（被光照区域）"],
            ["说背景只会说 background",
             "用 color block（色块）、bokeh（虚化）、plain backdrop（简洁背景）"],
            ["说设备只会说 gear",
             "用 85mm F1.4、portrait lens（人像镜头）、skills over gear（技巧胜过器材）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：如何让自己在画面里看起来更醒目、这里很难、五子棋、第一次落下、首先是颜色、突出的颜色、大片色块的环境、第一颗黑紫落入棋局、元素过多的环境、衣服与背景的颜色搭配、以后期挑战、只保留主体的颜色、色彩来传递同一种情绪、大色块画面放置标题、标题的颜色、主体相近的、对比色、捷客镜头拍、虚化多漂亮、85毫米F1.4、新款、怎么变这么轻、不要打扰我继续下棋、小微调、构图也很重要、旗帆上横梳做横的线、引导线构图、引导线之歌、主题心目的关键、颜色道路是引导线、脑皮壳是引导线、随到当然是引导线、电影中会唱歌唱简、照片视频都独一朝吃便甜、主条放在引导线、尤其是他们的实现、对焦的好厉害、高速运动物体的追焦、全聚快门的机身、高速连拍也不跑交、引导线之歌又有什么关系、用捷客镜头拍、牢牢锁住主题、没怎么停电了、手电筒、还有光、人物站在画面中唯一被光照耀的区域、被焦点、被切割的阳光、摄影灯打出的巨光、一盏路灯、一只手电筒、后期把支出光加强、其他情况压暗、头灯、手机的灯、让自己成为光源、画面中的焦点、夜景也太好看了、大光圈让画面变得很干净、郊外光斑、免责声明、厉害的器材可以胜过所有精心设计的谬论、画面配色构图都是非常实用的技巧、大多数情况下都比器材更重要、前景深的特写镜头、相互配合的关系、拍东西亏根解体还是为了爽、新一代的G大师、F1.4镜头、摄影天才、焦段、杂断的元素、大光圈带来的前后景虚画、焦内锐利的画质、很有质感、拍东西的快乐有很多种、追求氛围、表达、好的器材、高素质的画面、影像可能有高低之分但快乐都是一样的、前一代在时间的验证下、新一代对焦更快、四压差更小、迅光过瘾空置更强、体积和重量都大不缩减、旅行拍摄轻松了很多、85毫米F1.42代、索尼的第20次大式镜头、原厂镜头超过75只、价位和焦段的选择非常丰富、原厂韩副厂、更好的画质、无视变的呼吸补偿、机身的高速连拍和对焦速度、A93、每秒一秒连拍、新手老手通用的超强人像镜头、波多头、下次再见等。"
    },
    "3EwpevjnXp1": {
        "duration": "4:44", "topic": "剪辑 · 黑场转场",
        "practice": [
            ["说黑场核心", "A brief blackout between scenes creates a smooth transition."],
            ["说生活遮挡", "Clothes, doors, and laptops naturally cover the lens."],
            ["说明灭画面", "Any light-on/light-off shot can bridge with black."],
            ["说转换节奏", "Blackout acts as a breath pause when changing music or mood."],
            ["说高潮前奏", "Darkness before dawn sets up an emotional climax."]
        ],
        "pitfalls": [
            ["Only use your hand to cover.",
             "Daily objects and actions make far richer covers.",
             "生活遮挡更丰富。"],
            ["Cover literally every time.",
             "Light-on/off shots also bridge naturally.",
             "明灭画面也能衔接。"],
            ["Forget blackout's rhythm role.",
             "It's a breath between chapters and music changes.",
             "黑场也是呼吸点。"],
            ["Cut straight to the climax.",
             "A moment of black builds anticipation.",
             "黑场铺垫高潮。"],
            ["Shoot covers without a theme.",
             "Match the cover to your story's tone.",
             "遮挡要贴合故事。"]
        ],
        "shifts": [
            ["说转场只会说 transition",
             "用 blackout transition（黑场转场）、cover the lens（遮镜头）、natural covers（自然遮挡）"],
            ["说节奏只会说 rhythm",
             "用 breath pause（呼吸暂停）、chapter close（章节结束）、music change（换音乐）"],
            ["说创意只会说 creative",
             "用 light on and off（明与灭）、anticipation（铺垫）、emotional climax（情绪高潮）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：在场景A把画面一遮、来到场景B再把手拿开、2017年、像第一次看到魔术一样找不到缝、经典到有点无趣、丝环核心、两个场景之间迷人而短暂的漆黑、vlog镜头设计的巧思、不只用手折、扔衣服、拍块地毁、开门关门、打仓眼、打开电脑、做椅子、自然地遮住进口、随意组合、黑场破统、比光是用手折的要丰富很多、拇指相机拍下来非常方便、第一层、遮住这个思维定势力、拓宽一下、明和灭感觉的画面、黑场自然间接、扔掉一些胶条、应该假然而止的地方、防水的相机、全部裸裂下来、告别转场没想法、另一大作用、思路同样重要的拍摄设备、英式的320COSS、黑色和白色、限定反正让我眼前一亮、功能还是一样的强、能吸的地方可以到处吸、浇到一瞻也很方便、太小了、只有拇指大小、4K的画质、拓展仓、遥控和监看、自然广角模式、人像滤镜、记录日常方便的不得了、黑场转换节奏、换音乐换情绪、结束一个章节、呼吸之间的暂停、音效、前一段情节办成的音乐一同结束、更常见的是作为高潮的叙事、黎明前的黑暗、烟花、自由的奔跑、评论去发一下、音乐开始升华、都来梦、小时候最喜欢的动画、朋友家看、角色扮演、不同意犯胖虎就关掉电视不让看、每一集每一部大电影都是胖虎、如今我不再是小胖虎、我变成了老胖虎、自己故事里的哆啦A梦、转场之上任意门、航拍之下的主情敌、水下的世界可以轻松看到、不用变小也可以去到各种地方、小小的拇指相机可以装下整个世界、那时候有人把这样的相机拿给我看、这就是说爱梦可代理泡出来的、很多东西都成真了真好等。"
    },
    "88iMVf1zdWf": {
        "duration": "3:52", "topic": "Vlog · 运动相机",
        "practice": [
            ["说Action特点", "Tiny size plus durability opens creative mount points."],
            ["说双面胶固定", "Double-sided tape mounts the camera to any object."],
            ["说5倍慢动作", "5x slow motion amplifies everyday moments."],
            ["说冰箱视角升级", "Fixed on objects, you get a truer dynamic POV."],
            ["说坚持的道理", "Make something crappy first, then improve it daily."]
        ],
        "pitfalls": [
            ["Shoot only the classic fridge angle.",
             "Mounting on objects gives dynamic POVs.",
             "双面胶让视角更活。"],
            ["Use only 2x or 4x slow motion.",
             "5x slow motion gives a stronger feel.",
             "5倍慢放更惊艳。"],
            ["Assume action cams are only for sports.",
             "They capture breakfast stories and daily life too.",
             "运动相机也能拍日常。"],
            ["Wait for a perfect start.",
             "Make something crappy first, then improve it.",
             "先做出烂东西再变好。"],
            ["Give up when things go wrong.",
             "Keep daily habits; they pay back someday.",
             "坚持日常终有回报。"]
        ],
        "shifts": [
            ["说相机只会说 camera",
             "用 action cam（运动相机）、cold tolerance（耐寒）、heat resistance（耐高温）"],
            ["说视角只会说 angle",
             "用 dynamic POV（动态视角）、double-sided tape（双面胶）、5x slow motion（5倍慢放）"],
            ["说坚持只会说 persist",
             "用 the first step（第一步）、daily habits（每日习惯）、pays you back（给你回报）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：回顾过去的这一年、去了很多地方、日本的最高峰、大高枷锁的山脉、fishing on the Black Sea、记录生活中的美好瞬间、升级版本、全新的DJI Action 5 Pro、如何用DJI Action 5拍摄Vlog、更好的电影感、防水、咔咔扛噪、小、创意的地方、感官刺激的视觉冲击、特别冷的地方滑雪、遇寒能力非常出众、放在煎鸡蛋的锅里面、抵抗高温的能力、Kafka早期准备早餐的小故事、经典的冰箱视觉、it is boring、双面胶、固定在想要拍摄的物体上面、真实并且是动态的物体视觉、the same method we could also apply to the coffee part、慢动作模式slow motion、不是两倍也不是四倍、5倍速慢放、Let's go、相机不可以直接放进锅里的、简易的道具、先给自己整点吃的吧、离职领了大礼包、注册了个小公司、自媒体粉丝突破了一万、签了EMCN、脚踝受大伤、在家躺了至少半个月不止、2024年对我来说真的很难评价、很多个第一次、有好的也有不好的难忘、同时又很宝贵、成长、一开始我也傻了故事、卖出第一步是最重要的、做出一坨像狗屎一样的东西、慢慢的把它变好、换做其他人应该也是可以的、不管发生什么事情都要坚持下去、坚持每天吃早餐、坚持每天运动、坚持每天学习个新的技能、坚持让自己变得更好、每一分钟每一秒都很重要、未来的某一天给你回报等。"
    },
    "4RbaI1bzrFp": {
        "duration": "37秒", "topic": "分镜 · 蒙太奇",
        "practice": [
            ["说蒙太奇定义", "Cutting related or unrelated shots together creates metaphor."],
            ["说关联核心", "Montage-style boards build visual or semantic links between shots."],
            ["说三种方式", "Similar composition, matching motion, and causal progression."],
            ["说分镜表", "Sketch what each shot conveys and its link to neighbors."],
            ["说适用范围", "Linking needs pre-production; it fits narrative shorts."]
        ],
        "pitfalls": [
            ["Think storyboarding means more angles.",
             "Without linking, extra angles are just multi-cam recording.",
             "多角度不等于分镜。"],
            ["Cut shots with no connection.",
             "Viewers feel jumps and fragmentation.",
             "无关联观众会割裂。"],
            ["Force unrelated links.",
             "A weak forced link is worse than none.",
             "强拉关联更差。"],
            ["Fix everything in post.",
             "Linking needs pre-production planning.",
             "关联靠前期规划。"],
            ["Ignore sound as a cut point.",
             "Sound can be a connecting edit point.",
             "声音也能做剪接点。"]
        ],
        "shifts": [
            ["说剪辑只会说 edit",
             "用 montage（蒙太奇）、storyboard（分镜）、cut point（切镜点）"],
            ["说关联只会说 link",
             "用 visual connection（视觉关联）、semantic connection（语义关联）、causal progression（因果递进）"],
            ["说叙事只会说 narrative",
             "用 viewer inference（观众脑补）、narrative engagement（参与叙事）、push the story（推动叙事）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：什么是蒙太奇、着急地开着车、时间很紧迫、接孩子放学、描述一个主题、相关或不相关的镜头放在一起、产生暗喻的作用、普通分镜只是展示不同画面、蒙太奇式分镜建立关联、视觉上的相似形状颜色动作、语义上的因果关系对比关系、观众自动脑补中间的故事、相似的构图颜色、动作方向一致、因果递进、参与感越强效果越好、新手认为分镜就是多切几个角度、多机位记录、每个镜头都在推动叙事、拍之前画一个简单的分镜表、传达什么信息和上下镜头的关联、练习视觉关联、形状颜色相似的物体、切镜的连接点、动作关联、从左跑出从右跑入、控制单镜头时长、超过几秒还没新信息观众走神、切镜没有信息增量、强拉关联比没有关联更差、信息密度低、忽略声音的关联作用、声音也可以成为剪接点、分镜关联需要前期规划、叙事类短视频短片创作、直播类单镜头长记录纯教程的一镜到底、好的分镜让观众主动脑补产生参与感等。"
    },
    "1pV3F53joY1": {
        "duration": "48秒", "topic": "剪辑 · 蒙太奇句式",
        "practice": [
            ["说句式定义", "A sentence turns montage theory into a reusable template."],
            ["说积累句式", "Cut fast between similar shots to build an impression."],
            ["说对比句式", "Alternate two contrasting sets to sharpen the theme."],
            ["说重复句式", "Repeat one action across scenes for rhythm and ritual."],
            ["说句式组合", "Mixing sentences works better than using only one."]
        ],
        "pitfalls": [
            ["Freeze on what to cut next.",
             "Sentences tell you exactly what to cut.",
             "句式让你知道下一刀。"],
            ["Use too many shots when accumulating.",
             "A few suffice for the effect.",
             "积累画面几个就够。"],
            ["Pick weak contrasts.",
             "Choose materials with clear opposition.",
             "反差要选明显素材。"],
            ["Cut repeat scenes off-beat.",
             "Sync the cut speed to the music.",
             "重复切速跟音乐。"],
            ["Apply one sentence rigidly.",
             "Sentences are tools, not formulas.",
             "句式是工具不是公式。"]
        ],
        "shifts": [
            ["说蒙太奇只会说 montage",
             "用 sentence（句式）、template（模板）、cut fast（快切）"],
            ["说情绪只会说 mood",
             "用 accumulation（积累）、contrast（对比）、repetition（重复）、progression（递进）"],
            ["说剪辑只会说 edit",
             "用 ritual and rhythm（仪式与节奏）、emotional burst（情绪爆发）、sync to music（跟音乐卡点）"]
        ],
        "footer": "分析基于理性分析SVG重构。已校正：不同的蒙泰奇句型、前进式句型、后退式句型、怀型句型、蒙太奇句式、蒙太奇一学就会、理论听懂了但拍的时候不知道该用什么句式、可复用的具体操作模板、多个相似画面快速切换建立印象、两组反差画面交替出现强化主题、学会了句式剪辑时就知道下一刀该切什么、快速切换多个相似画面、不同人喝咖啡、城市速写、情绪铺垫、今昔对比、贫富差距、同一类动作在不同场景重复出现、建立节奏和仪式感、画面从小到大、增强冲击力、高潮段落、情绪爆发、收集几个相似主题的短片段、快速切换在一起、对比内容刻意用对比句式、记录同一个动作在不同时间地点的重复、每天早上喝咖啡、画面太多几个画面足够、对比句式对比不够强烈、两组画面差异太小、选素材时就要注意反差、重复句式节奏不对、切换太快看不懂太慢没感觉、根据音乐节奏定切换速度、只用一种句式、多种句式结合效果最好、句式是工具不是公式、根据内容灵活调整不要生搬硬套、每种句式都有其最佳场景、短片创作情绪内容、单一场景的教程访谈视频新闻纪实类内容等。"
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
