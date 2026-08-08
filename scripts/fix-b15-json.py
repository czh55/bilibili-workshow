#!/usr/bin/env python3
"""批15：将简化场景JSON补全为 gen-scene-en.py 所需的完整结构。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "3yKrD9TujJh": {
        "duration": "3:59", "topic": "美妆 · 眼妆教程",
        "practice": [
            ["说圆眼三线", "Make the three lines round and curved."],
            ["说圆眼卧蚕", "Smile to find the aegyo-sal center and blend a half-circle."],
            ["说长眼打底", "Start with a parallelogram and pull to the brow tail."],
            ["说长眼卧蚕", "Deepen the aegyo-sal flat, then turn up at the corner."],
            ["说提亮区别", "C-shape for round eyes, sharp corner for long."]
        ],
        "pitfalls": [
            ["Use straight shadow lines for round eyes.",
             "Round all three lines—brow, lid, and aegyo-sal.",
             "圆眼三条线都要圆弧状。"],
            ["Fill the whole inner lash line.",
             "Fill only the center segment for a rounder iris.",
             "圆眼只填内眼线中段。"],
            ["Draw long eyes with curved lines.",
             "Use a parallelogram, straighter and longer lines.",
             "长眼线条要偏直偏长。"],
            ["Keep both outer corners closed.",
             "Leave a small gap at the outer eye for breathability.",
             "长眼上下眼尾留空隙更透气。"],
            ["Use the same highlight for both eye types.",
             "C-shape shortens the mid-face; sharp corner extends it.",
             "圆眼C字提亮，长眼锐角提亮。"]
        ],
        "shifts": [
            ["说眼妆只会说 eye makeup",
             "用 three lines（三条线）、aegyo-sal（卧蚕）、parallelogram（平行四边形）"],
            ["说眼型只会说 eye shape",
             "用 rounded lines（圆弧线条）、straight and long（直而长）、pull to the brow tail（拉到眉尾）"],
            ["说美瞳只会说 contacts",
             "用 pupil-widening（扩瞳）、light contacts（浅色美瞳）、swept-back lashes（斜飞睫毛）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：圆眼长眼、三条线、眉毛上眼形卧蚕、半圆打底、下眼睑、灰色系、睫毛根部、双眼皮上方、眼尾眉尾连线、晕染下眼尾、深色加深、外扩、平拖、深灰、卧蚕中间、最低点、半圆状、比眼珠长一点、淡色提亮、眼角画圆、立体感、竖直款睫毛、纵向拉长、下拉眼睑、眼线胶笔、内眼角、短翘、扩瞳、深色、圆眉、染眉膏、团状腮红、平行四边形、平直、横向晕染、平拉、眉尾、锐角、眼下痣、空隙、透气感、斜飞款、黑色眼线、加强化尖、浅色系、减少黑眼珠存在感、延长感、锐利眉形、眉峰、毛流、斜线型腮红、线性腮红、提拉、C字提亮、中庭、锐角提亮、狗狗眼、清冷、贵气等。"
    },
    "8ZBcGy1luZk": {
        "duration": "5:08", "topic": "拍摄 · 素人上镜",
        "practice": [
            ["说显重原因", "A heavy body or a big frame looks stocky."],
            ["说穿搭收缩", "Deep colors shrink mass; a skirt beats pants for pear shapes."],
            ["说肢体舒展", "Keep limbs extended, never squeeze your flesh."],
            ["说配件选择", "Skip small props; pick a larger bag."],
            ["说光线放开", "An even face can handle high contrast."]
        ],
        "pitfalls": [
            ["Hide or squeeze your flesh.",
             "Keep limbs extended—squeezing makes you look bigger.",
             "收缩挤压显胖，肢体要舒展。"],
            ["Wear tight, flimsy fabrics.",
             "Keep some ease; the fabric shouldn't cling.",
             "面料软塌贴身上会暴露体量。"],
            ["Chase agile poses with a big frame.",
             "Favor relatively static poses.",
             "大体格做灵动动作会不协调。"],
            ["Use small props as size references.",
             "Pick larger accessories and simple backgrounds.",
             "小配件变参照物显笨拙。"],
            ["Force yourself into the thin template.",
             "Fix weaknesses, amplify strengths, keep character.",
             "套模板努力会越走越累。"]
        ],
        "shifts": [
            ["说显壮只会说 bulky",
             "用 heavy on camera（显重感）、big frame（大体格）、stocky（墩实）"],
            ["说穿搭只会说 outfit",
             "用 deep colors（深色系）、shrink mass（量感收缩）、keep some ease（保持宽松）"],
            ["说拍摄只会说 shoot",
             "用 static poses（静态动作）、size reference（参照物）、high contrast（大光比）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：素人拍照计划、威尼、上镜状态、笨重、不靠妆造不做爆改、还原自然瞬间、显重感、体型偏胖、体格很大、肢体不轻盈、身高1米78、体重150斤、超大体格、坠肉、灵动摆姿、压力、五官淡、身高臂展、梨形身材、下肢、上肢、长度优势、线条感、面部平整、凹陷、痘坑、法令纹、扛住光线、穿搭、颜色款式、牛仔色连衣裙、深色系、量感收缩、板型、裙子比裤子、适合理型身材、收腰设计、面料软塌、贴在身上、宽松、无袖、大臂后背、厚重、削肩设计、肩膀线条、坠肉、藏起来、收缩挤压、挤作一团、上镜更显胖、肢体舒展、弯曲、体格较大、灵动感、走动转身、不协调、静态动作、比例展示、小件、咖啡杯、参照物、笨拙、大一点的包、拍照背景、身心比例、狭窄室内咖啡店、室外场景、简化背景、构图、收、呆板、面部平整、光线放开、大光比、表情幅度大、不走形、简单底妆、气色优先、改造、眉毛走势低频、眉眼不精神、纹的、修图、眉型、眉骨立体、上镜模板、要瘦要娇小要灵动可爱、背道而驰、越走越累、停下来、少羡慕他人、多欣赏自己、特征、目标、长处和短板、修饰短板、放大长处、保留特点、根本秘诀、芝莉玉、盛世小礼等。"
    },
    "7X4ik8CNxin": {
        "duration": "0:30", "topic": "拍摄 · 眼神管理",
        "practice": [
            ["说看镜头有神", "Slightly engage the brows to open the look."],
            ["说45度夹角", "Keep the eye-to-lens angle within 45 degrees."],
            ["说反向看", "Face right and look left; face left and look right."],
            ["说抬头低头", "Tilt up and lower your gaze; tilt down and raise it."]
        ],
        "pitfalls": [
            ["Let the face go fully relaxed.",
             "Slightly engage the brows for a bright look.",
             "脸部完全放松会无神。"],
            ["Let too much sclera show.",
             "Keep the eye-to-lens angle within 45 degrees.",
             "视线夹角要控制。"],
            ["Turn eyes the same way as the face.",
             "Look opposite the face turn.",
             "脸右转看左，脸左转看右。"],
            ["Bare your teeth when smiling.",
             "Imagine crescent-moon eyes for a real smile.",
             "呲牙咧嘴显假，月牙眼才真。"]
        ],
        "shifts": [
            ["说眼神只会说 eyes",
             "用 lifeless（无神）、engage the brows（眉毛发力）、sclera（眼白）"],
            ["说角度只会说 angle",
             "用 45-degree angle（45度夹角）、opposite gaze（反向看）"],
            ["说微笑只会说 smile",
             "用 baring teeth（呲牙咧嘴）、crescent-moon eyes（月牙眼）、genuine（真实）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：看镜头、脸部完全放松、无神、眉毛稍微用力、舒展、不看镜头、眼白过多、视线夹角、不超过45度、脸右转左看、脸左转右看、抬头垂眸、低头抬眼、呲牙咧嘴显假、小月牙、真实、显假等。"
    },
    "4BI6ke4cPWy": {
        "duration": "0:09", "topic": "拍摄 · 身材焦虑",
        "practice": [
            ["说焦虑根源", "Anxiety comes from the thin-only belief."],
            ["说打破偏见", "The same outfit works on many body types."],
            ["说匹配身材", "Right cut, angle, and light outshine wrong clothes."],
            ["说认知转变", "Stop judging by one standard."]
        ],
        "pitfalls": [
            ["Chase the single perfect body standard.",
             "Break the bias with visual contrast.",
             "单一标准是焦虑源头。"],
            ["Think thin is required to be beautiful.",
             "Outfits and angles can match any body.",
             "不是只有瘦才好看。"],
            ["Blame your body for unflattering photos.",
             "Match the outfit, angle, and light to your body.",
             "问题在于匹配而非身材。"],
            ["Judge yourself by one standard.",
             "Stop the single standard and find your look.",
             "停止单一标准评价。"]
        ],
        "shifts": [
            ["说身材只会说 body",
             "用 body types（身材类型）、pear-shaped（梨形）、thin-only myth（瘦才美的偏见）"],
            ["说焦虑只会说 anxiety",
             "用 the bias（偏见）、the single standard（单一标准）"],
            ["说拍照只会说 shoot",
             "用 match your body（匹配身材）、outshine（好看得多）、mindset shift（认知转变）"]
        ],
        "footer": "转录基于图文实录完整口播（口播仅水印，场景依据图文实录画面与SVG分析重构）。已校正：随机缓解身材焦虑、同一套衣服、不同身材、很好看、不够瘦、以为只有瘦才好看、社交媒体、单一标准、完美范例、偏见、最简单对比、打破、照片好不好看、身材完美度、穿搭角度光线、匹配、梨形身材、穿对版型、选对角度、用好光线、比瘦子好看、认知转变、不敢上镜、停止单一标准、一直可以好看等。"
    },
    "6zub7SCxChc": {
        "duration": "4:16", "topic": "美妆 · 修容教程",
        "practice": [
            ["说修容脏因", "Shadowing the wrong places or a heavy hand."],
            ["说鼻影形状", "Tip is an eight and U; root is a flipped eight."],
            ["说眼窝轮廓", "Sculpt the socket with light matte eyeshadow."],
            ["说面颊转折", "Find the light-dark transition zone, not the front face."],
            ["说提亮逻辑", "Keep shadows still and only boost highlights."]
        ],
        "pitfalls": [
            ["Put shadow where no shadow exists.",
             "Only contour structural shadow zones.",
             "不该有阴影的地方上阴影会显脏。"],
            ["Draw two straight nose lines.",
             "Use the eight-U-flipped-eight shape language.",
             "鼻影直线条显脏显假。"],
            ["Contour the front face for width.",
             "Find the side-front transition zone.",
             "面颊修容要找转折区域。"],
            ["Rely on shadow alone.",
             "Boost highlights instead of darkening shadows.",
             "阴影控制不好就靠提亮。"],
            ["Chase 100% flatness.",
             "Keep a natural fold—too flat looks fake.",
             "追求过平反而僵硬。"]
        ],
        "shifts": [
            ["说修容只会说 contour",
             "用 shape language（形状语言）、transition zone（转折区域）、shadow structure（阴影结构）"],
            ["说鼻子只会说 nose",
             "用 inverted eight（倒八）、the U curve（U弧度）、bridge root（山根）"],
            ["说立体只会说 dimensional",
             "用 restore dimension（还原立体度）、sculpt the socket（塑造眼窝）、shade-narrowing blush（收缩色腮红）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：折叠、修容、新手、脸脏、画错位置、阴影结构、用量、下手太重、助教老师、光影变化、形状、粉底液、立体、扁钝、覆盖阴影结构、大白脸、淡妆、还原立体度、调整比例、修饰五官脸形、骨骼突出、修鼻子、鼻骨轮廓、凹凸、直线条、显脏显假、鼻头八、U、山根倒八、鼻梁开口菱形、男模特、连到眉头、女生连眉毛三分之一、小tips、U弧度越大越长、弧度越平越短、膏状、晕染、妈生骨骼感、侧面不显脏、修眼部、眼妆公式、平行四边形、眼头、眉毛三分之一、眉尾、卧蚕最低点、浅色小肿色、眼影盘、深邃立体、修面颊、脸宽脸方、颧骨、正面显脏、侧面没效果、正侧面转折区域、明暗关系、正面面对光源、转折线、45度、内收、两条线中间区域、视觉宽窄、打光方式、过渡区域、收缩色腮红、范围、瞳孔外边缘、侧面区域少量阴影、下颌角、贴着骨头加深、余粉向上带过、提亮、对比度、阴影更黑、高光更亮、立体、显脏、阴影不变、高光更亮、少量阴影、加强高光、修容效果、哑光高光、眉骨、鼻子更挺、苹果肌饱满、下巴更翘、练习、浓淡、脸形、学自行车、担心摔跤、大白脸、更美的一面等。"
    },
    "3Y2zr39lj0x": {
        "duration": "3:57", "topic": "美妆 · 遮法令纹",
        "practice": [
            ["说法令纹原理", "Lift the dropped highlight plane, not just the line."],
            ["说45度找凹面", "Tilt 45 degrees so side light reveals the hollow."],
            ["说薄层手法", "Blend on the hand and build in thin layers."],
            ["说压凸面", "Use shade-narrowing blush in a C, not shadow."],
            ["说重建苹果肌", "Rebuild the peak with brightening blush on a velour puff."]
        ],
        "pitfalls": [
            ["Cover the wrong area.",
             "Tilt 45 degrees and find the actual hollow.",
             "范围不对等于没遮。"],
            ["Pile on a thick blob.",
             "Blend thin on the hand, build in layers.",
             "厚涂卡粉像补丁。"],
            ["Brighten the whole area at once.",
             "Keep the brightening precise and thin.",
             "越拍越大等于没提亮。"],
            ["Shadow the front face.",
             "Use shade-narrowing blush in a C instead.",
             "正脸上阴影会脏。"],
            ["Chase 100% flatness.",
             "Keep a natural fold—total flatness looks fake.",
             "过平像假人。"]
        ],
        "shifts": [
            ["说法令纹只会说 nasolabial",
             "用 fold（法令纹）、hollow（凹面）、backlit plane（背光面）"],
            ["说手法只会说 apply",
             "用 flat brush（扁头刷）、blend on the hand（手背晕染）、thin layers（少量多次）"],
            ["说改善只会说 fix",
             "用 shade-narrowing blush（收缩色腮红）、brightening blush（膨胀色腮红）、velour puff（植绒粉扑）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：有纹没纹、年轻10岁、范围不对、厚厚一坨、卡鼻翼、补丁、平整自然、原理、手法、工具、凹凸结合、立体结构、助教老师、相比较、面中最膨、苹果肌、最突点、年龄流失、往下掉、堆积鼻翼、阴影更深、光线照上去、背光面、黑色、显老、黑黑的法令纹、提亮、高光面上移、饱满真实、三步、阴影凹面提亮、白色凸面压暗、最突点上移、复位苹果机、实操、头侧45度、半侧面、凹面、亮一号、遮瑕膏、遮瑕液、扁头遮瑕刷、扁面沾取、手背晕一晕、精准上到阴影区、粉更薄、区域更精准、一次性、大量粉、越拍越大、亮面暗面全部提亮、迷你粉扑、对折、折面、拍晕、余粉、少量多次、折两次、透明散粉、压反光、90%、百分之百平整、面中完全平、僵硬、假人、下坠凸面、压暗、正脸区域、直接上阴影、脸脏、变成暗面、让它平、没那么凸出、收缩色腮红、凸起区域、画C、日常画法、苹果肌凸点、重塑、瞳孔正下方、鼻梁中段交叉、小三角形、哑光高光、膨胀色腮红、植绒小粉扑、显色、自然隐藏、饱满、视觉向上、年轻、结构性凹陷、化妆改善、不可能完全消失、顶光、侧面光源、大部分光源、该遮还得遮、评论区留言等。"
    },
    "4nLI268uSVP": {
        "duration": "1:38", "topic": "拍摄 · 上镜角度",
        "practice": [
            ["说死亡角度", "Chin up too high, chin down, eye-roll, brow lines."],
            ["说20度微抬", "Lift the chin just 20 degrees for an even face."],
            ["说45度侧脸", "Keep the side turn within 45 degrees."],
            ["说平视眼神", "Gaze level with the face's turning angle."]
        ],
        "pitfalls": [
            ["Lift the chin too high.",
             "A tiny 20-degree lift keeps the face even.",
             "抬太高脸平显大。"],
            ["Turn the face far from the lens.",
             "Keep the side turn within 45 degrees.",
             "侧脸夹角要控制在45度内。"],
            ["Look opposite the camera in profile.",
             "Gaze level with the face's angle.",
             "侧脸反向看眼白过多。"],
            ["Swing angles in big movements.",
             "Make slight adjustments only.",
             "角度要微微周转。"]
        ],
        "shifts": [
            ["说角度只会说 angle",
             "用 dead angles（死亡角度）、20-degree lift（微抬20度）、within 45 degrees（45度内）"],
            ["说脸只会说 face",
             "用 even face（面部平整）、double chin（双下巴）、forehead lines（抬头纹）"],
            ["说眼神只会说 gaze",
             "用 level gaze（平视）、too much sclera（眼白过多）、slight adjustment（微微周转）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：人类拍照死亡角度、不要抬高、低头双下巴、翻白眼、抬头纹、脸移太侧、再侧、不对、下巴抬高20度、微抬、面部平整、抬过高、不立体、皮肤很大、脸很平、低头微低20度、侧面微侧、45度以内、眼睛看镜头、脸侧、很难受、45度角30度15度、微微移中、微微抬、侧面、眼睛、反方向、眼白过多、平视过去、微抬平视微低、歪头看向镜头、歪太多、控制好、微微周转、大幅度周转等。"
    },
    "5En77lJeUP": {
        "duration": "5:35", "topic": "拍摄 · 眼神引导",
        "practice": [
            ["说眼神重要性", "A storytelling gaze is the finishing stroke."],
            ["说套近乎", "Warm up the model to let real emotion flow."],
            ["说定剧本", "Give the model a story to know what to express."],
            ["说常理动作", "Smoking means looking away; keep the gaze natural."],
            ["说空洞根源", "Dull eyes mean no story was communicated."]
        ],
        "pitfalls": [
            ["Tell the model to look and snap.",
             "Give a story so the model knows what to express.",
             "无剧本拍摄造成呆板。"],
            ["Retouch a dull gaze.",
             "Direct emotion—eyes can't be fixed in post.",
             "眼神修图修不出来。"],
            ["Shoot only the outer beauty.",
             "Capture the inner mood and expression too.",
             "形神兼备才是优秀人像。"],
            ["Skip the ice-breaking.",
             "Befriend the model so they open up.",
             "套近乎让真实情绪流露。"],
            ["Force the model to face the lens.",
             "Let natural actions guide the gaze, like smoking looking away.",
             "按常理引导眼神才有力。"]
        ],
        "shifts": [
            ["说眼神只会说 eyes",
             "用 storytelling gaze（有故事的眼神）、window to the soul（心灵窗户）、the finishing stroke（点睛之笔）"],
            ["说引导只会说 guide",
             "用 break the ice（套近乎）、set a script（定剧本）、capture candidly（抓拍）"],
            ["说呆板只会说 dull",
             "用 empty gaze（眼神空洞）、uncommunicated story（没沟通好故事）、photographer's failure（摄影师问题）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：眼神呆滞、不知道看哪里、感情尴尬、模特、眼睛里有星星、自然灵动、人像摄影、眼睛是心灵的窗户、升华、有故事的眼神、画龙点睛之笔、形神兼备、外在、内在情绪神态、好看的皮囊千篇一律、有趣的灵魂万里挑一、修图整容、修不出来、小技巧、套近乎、面如呆板、面如死灰、眼神无光、朋友面前舒服、随意展示情绪性格、陌生人拘谨、做朋友做交流、镜头面前表现、真实情绪流露、眼神越来越有戏、好的演员、眼神有神有故事、专业靠这个吃饭、剧本、角色状态、有内容、知道自己要表现什么、善于引导、定一个剧本、特定的环境、抓拍、呆板眼神、沟通好情绪故事、紧张、两眼无光、抽烟怎么拍、常理、看镜头干嘛、往旁边一飘、不看镜头、有力、有故事、笑、眼神同样有故事、找角度、港风、任何一个有故事的眼神、呆板眼神配合、情绪状态、要看什么、摄影说看个镜头、没什么剧情、要表现的东西、摄影师的问题、很好的引导、不看镜头感觉也在、往下看特别有感觉、故事性、眼大无神、引导故事、特定的环境、思考一下就有眼神、看叶子没什么意义、眼拍大、往上看、小小的眼神同样有力、照片感觉上来了、眼神引导特别重要等。"
    },
    "6svbxkZZGM8": {
        "duration": "3:46", "topic": "拍摄 · 摆姿逻辑",
        "practice": [
            ["说坐姿三场景", "Chair, steps, ground—follow high to low."],
            ["说台阶显腿长", "One leg forward, one back lengthens the legs."],
            ["说蹲姿看膝", "Side squat, keyed on knee height changes."],
            ["说手部逻辑", "Props to hold, or work from head to toe."],
            ["说拍摄策划", "Plan pose references before every shoot."]
        ],
        "pitfalls": [
            ["Memorize poses one by one.",
             "Learn the underlying logic instead.",
             "死记动作不如懂逻辑。"],
            ["Squat facing the lens.",
             "Always squat sideways.",
             "蹲姿要侧身蹲。"],
            ["Squeeze arms into the body.",
             "Hold a prop or work head to toe.",
             "手有道具拿道具，无道具摸到脚。"],
            ["Pose without a plan.",
             "Give clients a pose reference set.",
             "拍摄前策划姿势参考。"],
            ["Force agile moves on the ground.",
             "Most step poses transfer to the ground.",
             "台阶姿势可通用到地面。"]
        ],
        "shifts": [
            ["说姿势只会说 pose",
             "用 high to low（从高到低）、side squat（侧身蹲）、knee height change（膝盖高度变化）"],
            ["说手只会说 hands",
             "用 head to toe（从头摸到脚）、prop（道具）、gestures（手势）"],
            ["说拍摄只会说 shoot",
             "用 pose reference（姿势参考）、shoot plan（拍摄策划）、mind map（思维导图）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：摄影师、摆姿、动作、十几二十种、不重样、偷偷背、现场查、摆姿背后的逻辑、记不住动作、被记法困住、十大干货、思维导图、坐姿、三个场景、椅子台阶地上、从高到低、两腿张开、并拢、翘二郎腿、放在凳子上、侧着翘、两只腿放凳子上、台阶、一前一后、腿比较长、手搭膝盖、双腿交叉、二郎腿、身体侧坐、浪漫、坐在地上、双腿并拢、盘腿、交叉、一前一后、蹲姿、侧身蹲、膝盖高度变化、同一高度、不同高度、经典侧身蹲、跪姿、视觉冲击力、辣妹风格、单腿跪、双腿跪、躺姿趴姿、居家草坪、躺地板、躺草坪、趴床上、趴草丛、手怎么放、有道具拿道具、草帽墨镜包包咖啡杯、从头摸到脚、摸额头、挡太阳、抓头发、手势、比OK、手张开、比耶、出拳、比心、托下巴、摸鼻子、摸耳朵、摸嘴巴、脸旁边比、上半身、歪头打招呼、插腰、两个手打开、抱胸、下半身、插兜、提裙子、垂下来、30种摆姿、记不住、技巧、策划、姿势参考方案、看图纠正、效率更高、收藏慢慢看、评论区、弯路等。"
    },
    "9ehOfiSMJLL": {
        "duration": "1:01", "topic": "拍摄 · 眼神力量",
        "practice": [
            ["说瞪眼误区", "Straining your lids makes the gaze emptier."],
            ["说穿针引线", "Thread a needle and feel the attention converge."],
            ["说专注一点", "Focus on one point to bring the penetration."],
            ["说眼神发力", "Engagement, not eye-straining."]
        ],
        "pitfalls": [
            ["Widen your eyes for power.",
             "The more you open, the emptier it gets.",
             "越睁大越没内容。"],
            ["Strain your eyelids.",
             "Power comes from focus, not the lids.",
             "眼皮用力眼神没劲。"],
            ["Force power on demand.",
             "Concentrate on a single point instead.",
             "专注一点才有穿透感。"],
            ["Equate power with staring.",
             "It's gaze engagement, like threading a needle.",
             "眼神发力不是瞪眼。"]
        ],
        "shifts": [
            ["说力量只会说 power",
             "用 penetration（穿透力）、gaze engagement（眼神发力）"],
            ["说眼神只会说 eyes",
             "用 lifeless（没力量感）、converge on a point（汇聚一点）"],
            ["说体验只会说 feel",
             "用 thread the needle（穿针引线）、focus on one point（专注一点）、the feeling（这感觉）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：眼睛没力量感、摄影师提醒、眼睛有劲一点、有力量一点、我有力了吗、有劲了吧、越挣大越没内容、力量感、穿透力、眼皮、使了多少劲、穿针引线、针、线塞进去、注意力、眼神、汇聚、空气中的点、认真看针、冲、眼神的发力、瞪眼皮、专注地看一个点、穿透感等。"
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
