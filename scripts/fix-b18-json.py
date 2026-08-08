#!/usr/bin/env python3
"""批18：将简化场景JSON补全为 gen-scene-en.py 所需的完整结构。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "2QXYFGfsfgf": {
        "duration": "3:48", "topic": "摄影 · 电影感曝光",
        "practice": [
            ["说快门为什么不能调", "The 180-degree rule sets the shutter for the cinematic feel."],
            ["说人眼帧率", "The eye's frame rate is dynamic, not fixed at 24fps."],
            ["说视觉暂留", "Photoreceptor signals persist 1/10 to 1/15 of a second."],
            ["说24帧标准", "24fps came from the sound era, not the eye's limit."],
            ["说180度原理", "A 180-degree opening gives the natural motion blur."]
        ],
        "pitfalls": [
            ["Think the eye sees at 24fps.",
             "The eye's frame rate is dynamic and continuous.",
             "人眼帧率不是24帧。"],
            ["Blame the screen for judder.",
             "Too-sharp frames break the motion illusion.",
             "画面过清晰会露馅。"],
            ["Treat the 180-degree rule as physics.",
             "It's a human convention from film history—breakable.",
             "180度是人定规矩。"],
            ["Forget why 24fps exists.",
             "It was chosen to fit sound and stable playback.",
             "24帧是声音时代的妥协。"],
            ["Confuse exposure time with sharpness alone.",
             "Longer shutter means more motion blur, softer frames.",
             "曝光时长决定模糊度。"]
        ],
        "shifts": [
            ["说快门只会说 shutter",
             "用 180-degree rule（180度原则）、shutter angle（快门角度）、1/48s"],
            ["说帧率只会说 fps",
             "用 persistence of vision（视觉暂留）、motion blur（动态模糊）、visual imprint（视觉烙印）"],
            ["说电影感只会说 cinematic",
             "用 the industry's legacy（工业遗产）、natural blur（自然模糊）、frame rate reciprocal（帧率倒数）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：出于艺术的考量、感光度、光圈、快门、180度原则、电影感、拍照片、画面太暗、减慢快门、立竿见影、拍视频、犯了大忌、48分之1秒、帧率24帧、24张图片、连贯动感的错觉、人眼的帧率、动态的、持续的、恒定帧率的机制、注意力和生命机能、电竞选手、144Hz、240Hz、显示器高刷、生病、醉酒、王家卫电影、常曝光降格、拖影、光线通过晶体、视网膜、感光细胞、化学信号、10分之1到15分之1秒、视觉暂留、动态模糊、重叠、小实验、昏暗、举起手臂、挥舞、拖影、手电筒、开到最亮、拖影长了很多、更强刺激、恢复敏感度、判断进入视线的物体、从哪个方向来、往哪个方向去、狩猎、躲避危险、标准帧率、默片时期、16帧每秒、同声机、兼容声音画面、24帧每秒、极限帧率、最低帧率、过于清晰、单独的图片、大范围的运动、打消错觉、24P、水平摇镜、一卡一卡、圆盘、镂空、遮挡、更换下一帧胶片、缝隙越小、曝光时长越短、画面越锐利、动态模糊越小、180度镂空角度、自然的动态模糊、快门角度原则、打破、战争动作片、高度危险、肾上腺素爆发、身体机能提升、看得更快更广、注意力更集中、模拟战争现场感、爆款慢门、帧率的两倍分之一、工业历史的遗产、100多年、视觉烙印、本能认为、电影感、推翻替代、该遵守的还是得遵守等。"
    },
    "8rLKlpNhDvi": {
        "duration": "2:34", "topic": "摄影 · 景深叙事",
        "practice": [
            ["说光圈代价", "Adjusting aperture ignores its cost: depth of field."],
            ["说浅景深问题", "Shallow DOF limits the actors' room to perform."],
            ["说跟焦员噩梦", "Film focuses by hand, so shallow DOF tortures the puller."],
            ["说小屏幕变化", "Small screens make bokeh harder to appreciate."],
            ["说设计联动", "Aperture is designed with set, lights, and blocking."]
        ],
        "pitfalls": [
            ["Open the aperture for exposure freedom.",
             "Film is an art of restraint, not technique.",
             "电影是蓄势的艺术。"],
            ["Keep both actors on the same plane.",
             "Deepen DOF to give both more room to perform.",
             "提高景深给表演空间。"],
            ["Rely on autofocus for film.",
             "Focus pulls are done by hand and steer attention.",
             "电影靠手动跟焦。"],
            ["Judge bokeh on a phone screen.",
             "Small screens raise the difficulty of showing bokeh.",
             "小屏难呈现虚化。"],
            ["Set aperture only for exposure.",
             "It's an artistic tool linked to the whole scene design.",
             "光圈是艺术蓄势工具。"]
        ],
        "shifts": [
            ["说光圈只会说 aperture",
             "用 depth of field（景深）、bokeh（虚化）、art of restraint（蓄势的艺术）"],
            ["说对焦只会说 autofocus",
             "用 focus puller（跟焦员）、hand focus（手动跟焦）、assist not replace（辅助而非替代）"],
            ["说叙事只会说 story",
             "用 story cues（剧情线索）、foreground and background（前后景）、T2.8 is already large（T2.8已算大）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：曝光三要素过时了吗、ISO不能调、光圈快门总能调了吧、很抱歉、不可以、打开光圈画面提亮、收起光圈画面变暗、最灵活的曝光掌控、苦口婆心、大光圈牛头、蓄势的艺术、技术的艺术、代价、景深、光圈越大景深越浅、剧情表达、两个人物、胶平面、稍微动一点点、虚焦、提高景深、表演区域、自动对焦、跟焦都是活人手动完成、焦点的推拉、调动观众的注意力、蓄势表达、准确性的重要级别、跟焦员的噩梦、T2.8、非常大的光圈、好莱坞、自动跟焦的方案、大将、LIDER跟焦器、辅助跟焦员、代替跟焦员、内容消费的中端、手机和平板、屏幕越来越小、背景虚化、呈现难度、大萤幕、猛猛开光圈、虚化的背景、陶醉、光圈全开拍到底、景深来展示剧情线索、前景和背景、展示剧情的重要位置、主体清晰、前后景、去得一塌糊涂、信息量大大降低、导演摄影美书灯光、设计前后景、远近都有戏、公民凯恩、超景深的摄影手法、巨大的表演区域、前后景都能安排演员同时表演、超大功率的照明、满足导演对画面的追求、经典、超浅的景深、折磨跟焦员、光圈布光和减光、不只是技术工具、艺术蓄势工具、分镜策划、场地道具灯光演员走位摄影走位、大机器运作中的一环、画面太暗加灯光、画面太亮加ND、小范围的改动、导演预想中的效果、大光圈是七彩矮、拍电影为啥需要更较远等。"
    },
    "AsOqxrPuu7s": {
        "duration": "2:51", "topic": "摄影 · 感光度原理",
        "practice": [
            ["说电影只认一个ISO", "Film uses only one sensitivity: ISO 800."],
            ["说换卷代价", "Swapping film mid-shoot breaks the schedule and logging."],
            ["说胶片是艺术工具", "Film ASA and color temp were artistic, not exposure, tools."],
            ["说原生感光度", "Native ISO is the setting with max dynamic range."],
            ["说800黄金标准", "800 is the practical sweet spot all brands chose."]
        ],
        "pitfalls": [
            ["Trust dozens of ISO stops for film.",
             "The film industry locks one sensitivity: ISO 800.",
             "电影工业只有ISO800。"],
            ["Swap film rolls for bad light.",
             "Adjust exposure, ND, or push/pull in processing instead.",
             "换卷代价高不如调光。"],
            ["Treat ISO as a pure exposure tool.",
             "It was an artistic grain tool in the film era.",
             "ASA是艺术工具。"],
            ["Push past native ISO casually.",
             "Other settings are simulated digital gain.",
             "非原生感光度是数字增益。"],
            ["Ignore the gold-standard habit.",
             "ARRI, Red, Sony, Nikon, Canon all chose 800.",
             "各厂默契选800。"]
        ],
        "shifts": [
            ["说感光度只会说 ISO",
             "用 native ISO（原生感光度）、gold standard（黄金标准）、digital gain（数字增益）"],
            ["说换卷只会说 change film",
             "用 push and pull（推充减冲）、ND filter（减光片）、log and archive（记录归档）"],
            ["说胶片只会说 film",
             "用 ASA grain（感光度颗粒）、artistic tool（艺术工具）、dual-native ISO（双原生ISO）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：光圈快门ISO为何过时了、拍立德、手机原相机摄影师、三座曝光基石、2026年、照片视频双修、摄影圣经、悄悄过时、ISO已经失效、视频拍摄成为内容生产的主力、界限越来越模糊、专业的电影人、曝光三要素、一二十个ISO档位、电影工业、感光度只有一个、ISO800、胶片年代、不同的感光度、挂上摄影机就无法更换、很简单、牵扯出的问题太多、胶片是无法回看的、打乱拍摄的进度表、严谨的记录、归档管理工作、中途换下未用完的胶卷、不被浪费、稍有疏忽、后期冲印流程、不可逆转的事故、现场拍摄、光线不对、换一盘胶卷、调整曝光、增加减光片、后期破充减充、翻江倒海的动作、保险的多、ASA和色温、艺术表现工具、曝光工具、颗粒感、不同题材、情节氛围、色温同理、数码相机、随意更换、很省事、不调ISO、原生感光度、模拟出来的、数字增益、胶卷破充和减充、动态范围最大、画质最好的挡位、画质最优秀的毛片、不会碰感光度、R来摄影机的原生ISO就是800、甜点挡位、黄金标准、白天加一片ND、晚上也不需要过分曝光、Red索尼尼康加能、默契选择、不遵守这套法则、故意提高感光度、高噪点、自媒体行业卷到飞起、追求最好的画质、默默遵守、双原生、三原生ISO、满血的画质表现、多帧合成技术、风起云涌、随意可调的感光度、调快门光圈不就解决了吗、下一期再见等。"
    },
    "6geWXgB6tVj": {
        "duration": "1:29", "topic": "摄影 · 布光理论",
        "practice": [
            ["说反平方率", "Light attenuation is geometric: brightness = 1/n²."],
            ["说思想实验", "A near lamp lights one spot; the sun lights everyone."],
            ["说曝光不均原因", "A source too close makes faces fall off unevenly."],
            ["说口播背景分离", "Move the source close to separate the background."],
            ["说适用范围", "The inverse-square law fails under specific conditions."]
        ],
        "pitfalls": [
            ["Assume light fades linearly.",
             "Attenuation is geometric, not linear.",
             "光衰减不是线性的。"],
            ["Keep sources far from subjects.",
             "Close sources make background falloff stronger.",
             "光源远近决定衰减。"],
            ["Blame the actors for uneven exposure.",
             "A source too close causes the light gap between faces.",
             "光源太近导致曝光差。"],
            ["Pull the source away to separate the background.",
             "Bring it closer to isolate the background.",
             "分离背景要靠近光源。"],
            ["Apply the inverse-square law everywhere.",
             "It fails under specific conditions.",
             "反平方率有失效条件。"]
        ],
        "shifts": [
            ["说光衰减只会说 fade",
             "用 inverse-square law（反平方率）、geometric（几何式）、not linear（非线性）"],
            ["说曝光只会说 exposure",
             "用 uneven exposure（曝光不均）、sharp falloff（急促衰减）、light-dark contrast（明暗反差）"],
            ["说背景只会说 background",
             "用 background separation（背景分离）、subject-background gap（人物背景差）、the law can fail（定律会失效）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：光行走了一倍的距离、强度应当减弱一半、传播衰减倍率、不是线性的、几何式的、思想实验、80楼、小帅、一盏灯、小美、1楼、半点照明作用、太阳、超级无敌远、亮度几乎一致、反平方率、n的平方分之一、距离增加一倍、四分之一、增加两倍、九分之一、曝光影响、一盏灯打两个人物、面部曝光刚刚好、曝光不足、光源离演员们太近了、光衰减得太急促、明暗反差越大、应用场景、拍摄口播、光源离人物越近、背景的亮度衰减越大、光源拉远、亮度差逐渐缩小、背景分离的效果、照亮人物的同时、光源不要过分影响背景、尽可能往人物靠近、不完全适用于所有情况、特定条件下失效、以后我们聊光志、感谢收看这篇新闻摄影、我是老队、下次再见等。"
    },
    "35b62Bbn98": {
        "duration": "11:57", "topic": "器材 · iPhone电影机",
        "practice": [
            ["说iPhone定位", "The 15 Pro is the first phone I'd treat as a cinema camera."],
            ["说算法依赖", "Phone hardware peaked; smart algorithms are the answer."],
            ["说Apple Log", "It's a low-contrast curve retaining maximum dynamic range."],
            ["说面团比喻", "Log is kneaded dough—versatile, unlike finished noodles."],
            ["说Blackmagic Cam", "BMD's free app gives 100% manual cinema control."]
        ],
        "pitfalls": [
            ["Expect a bigger sensor to go mainstream.",
             "Phone size is locked by function and usage.",
             "大传感器难成主流。"],
            ["Trust Smart HDR for video.",
             "Uncontrollable exposure kills the cinematic feel.",
             "智能HDR扼杀电影感。"],
            ["Treat Apple Log as a software trick.",
             "It needs dedicated Log hardware.",
             "Apple Log靠硬件。"],
            ["Buy a cinema camera for travel.",
             "Phones reach farther, harder destinations.",
             "手机能去更远的地方。"],
            ["Stabilize at night with IBIS.",
             "Physical stabilization avoids ghost jitter.",
             "夜间防抖用物理方案。"]
        ],
        "shifts": [
            ["说灰片只会说 log",
             "用 Apple Log、rec709 restore LUT（还原LUT）、dynamic range（动态范围）"],
            ["说手机拍摄只会说 shoot phone",
             "用 dedicated hardware（专用硬件）、rolling shutter（果冻效应）、physical stabilization（物理防抖）"],
            ["说设备只会说 device",
             "用 pocket cinema camera（口袋电影机）、backup phone（备用手机）、all-in-one tool（集成工具）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：iPhone 15 Pro、第一台真正可以当作电影机对待的手机、严肃创作的工具、iPhone 6s、4K影像、辩论桌、品牌还是用户、智能手机近10年市场增长、数码相机的份额、分割得有多惨烈、照片工具、主流微单的水平、视频、跟随急速排档到北美、生产力工具、比较全面的认知、传感器1英寸时代、硬件层面摸到了天花板、3.4%传感器、主流、屏幕大小、功能定位使用场景、牢牢框死、物理卡下来、更大的传感器需要更大的镜头、小米12S Ultra、外接镜头的方案、为相机附加了手机功能、强劲拍照性能的手机、比较原始的状态、讨喜的画面、硬件逐渐同质化、算法调教和AI训练、智能算法才是当下手机的解决方案、毫不克制的锐化和饱和度、涂抹感、苹果2017年推出智能HDR、锁死了曝光、智能调节画面局部的曝光、更多的细节、拍照片非常棒、对于视频、不可控的曝光等于扼杀掉电影感、一眼能辨别那些手机拍的素材、Apple Lock、2023年里程碑、苹果的灰片、松下V Lock、索尼S Lock、大疆D Lock、色彩对比度曲线、保留最多的色彩和明暗信息、对比度和保护度非常低、电影工业的逻辑、重新调整对比度保护度、还原成现实中的一面、最小程度的锐化、最大程度的保留动态范围、Gero Undone、ISO1250、动态范围接近惊人的14档、GH6、不到14档、指数709识并素材、一碗方便面、原始绒号文件、面粉、Lock素材、刚获好的面团、方便面饺子、夏威夷部落披萨、回炉改造成、为难它了、未经身家工的食材、不油腻且抑郁健康、色彩信息、色彩匹配、简单的软件调教、专制处理Lock的硬件、软件更新、早期iPhone、高感、1600 ISO的素材完全可用、24匹快门50分之1秒、夜间场景、滚动快门、Eric Fossum博士、像素大小、像素越大或者景容越大、电荷转信号的读取速度、传感器总体面积增大、导体总长度、读取速度下降、越小的传感器滚动快门越细微、CND的测试、5.3秒左右、读取速度、iPhone比iPhone RLX 3mm更加优秀、逼近机械快门、机械快门也是滚动快门、更自然的画面采集、后期防抖更加容易、过度锐化过度饱和过度降噪、智能HDR算法介入、三个镜头的画质都出奇的好、差一步、苹果自带的相机APP、手动模式都没有、严肃的视频拍摄、几乎是不可用的、95%的苹果用户、拍电影、只有5%的用户能看懂、脏活、大善人黑魔法、Black Magic Cam、纯电影机逻辑的免费操作系统、100%的手动操作、帧率曝光补偿白平衡、快门速度手动对焦、监看LUT、HEVC录制格式、苹果PORES、非常高质量的格式、体积过于庞大、184G的容量、20分钟的PORES素材、至上是可笑的、HEVC或者PORESLT记录、高强度连拍三天、容量焦虑、潜力并没有被黑魔法完全炸干、可进步的方向、Apple-Law下的OpenGate 4B3、4B3的协议苹果是开放了的、ProMovie、4B3全开选项、暂时无法使用Apple-Law、BNK上无法设置快门低过视频帧率、王家卫的万门效果、长曝光的星空掩饰、开放协议、电影级的标准、高动态多帧率低果凍高录制规格、正正住在里库里的电影机、Action按键设置为BNK的快捷键、口袋电影机的BNPCC、更进一步、一点不便宜、专业伪单搭配一个变焦镜头、价格还是达得有来有回的、集成了通讯剪辑和宣发功能、直播中毕竟的一环、主力生产工具、续航可以伸过市面上所有伪单、无法更换电池、充电宝的加持、先天的优势、机身小巧、更小的脚架、稳定器滤镜器材包、数台备用即时、运输成本几乎可忽略不计、海关的质问、遥远且极端饿溜的环境、北极圈之旅、滑雪潜水攀岩飞行、先天防水、影视器材的重量和体积、与素材量乘反比、徒步10公里、器材过重、6公里就些菜了、更远更难的目的地、特殊的机位角度、大屏幕构图、秒杀一切运动相机、三个胶段、安装个吐笼、画里胡哨、实用的、扩展分享、一扩版屏幕、一夜间取代电影机、慎重小心拍摄画续机、纪录片、排成电影、画质过瘾、传统相机的必要性搭得降低、说服穷人摄影码iPhone、最正当且正义的理由、阴伤、无法获得前景深、电影模式、西兰的状态、严肃创作完全不可用、给它时间能够赶上来、精力花在构图上、最被忽略的阴伤、鬼影、点光源直射镜头、手机属特别严重、鬼影和防抖加起来可以回掉一个好镜头、夜间、打开防抖、画面稳定了、镜头内的鬼影就会出卖你、跳来跳去、后期解决这些鬼影、大部分情况是不奏效的、唯一的解决方法、舍弃机身防抖、采用物理防抖、样片、大量使用脚架拍摄的镜头、消除鬼影跳动、稳定器滑鬼都有类似的功效、大屏幕取景很爽、监看有时是个大问题、低级位养拍、高级位腐拍、场恶梦、无法监看构图和焦点、操作参数、AirPlay投屏功能、索尼、手机vlog专用的监视器、大善人来开发、Apple lock十分强大、709还原LUT却很垃圾、Fanok自带的LUT还原、红色溢出相当严重、松下vlog的还原LUT、套在苹果LUT的素材上、效果竟初期的好、调整的色彩和对比度、最终得到的结果、非常满意、直接下载来试试、1.3分之1英寸传感器、T1.8的光圈、3倍长焦和13毫米广角、2024年的手机海洋、旗舰水平、稳坐了影像的第一把交易、继续遥遥领线、积极可危、后者、5年前对比手机的拍照性能、肉眼可见最优秀的、当年的遥遥领线早已不复存在、国产品牌王斯利卷硬件、主传1200万相处的传感器、小小的OP手机、依应传传感器的光学虚化、一点点小震撼、苹果今年推出Applelog、拉盖于友商的差距、OPLog花卫Log、VivoLog Vlog、重新回到硬件的比拼、双浅往长焦、按在地上抹擦、国产品牌能紧追更上、白宝箱、继续伸喊我们、欢迎收看时机成人摄影、我是罗翠、下集再见、点赞订阅转发打赏等。"
    },
    "90myESzS4uC": {
        "duration": "1:43", "topic": "器材 · 标准镜头",
        "practice": [
            ["说50毫米原因", "50mm balances optical quality, size, cost, and difficulty."],
            ["说套头历史", "Kits bundled 45-58mm standards to pull in consumers."],
            ["说非人眼视角", "50mm isn't the eye's view—easily debunked."],
            ["说人体工学", "We view paintings at 30-60 degrees; 50mm sees 46 degrees."],
            ["说标准演化", "It's history plus ergonomics and aesthetics combined."]
        ],
        "pitfalls": [
            ["Think 50mm is the eye's focal length.",
             "Our vision is wider than 50mm.",
             "50毫米不是人眼视角。"],
            ["Judge a lens by sharpness alone.",
             "Extreme lengths are hard to make sharp and fast.",
             "极端焦段难做牛头。"],
            ["Ignore why kits bundled 50mm.",
             "It was cheap and easy for great results.",
             "50毫米曾是爆款套头。"],
            ["Forget the 30-60 degree habit.",
             "It matches the eye's comfortable info zone.",
             "30-60度是舒适视野。"],
            ["Treat 46 degrees as coincidence.",
             "It's close to the 43mm film diagonal.",
             "46度接近胶片对角线。"]
        ],
        "shifts": [
            ["说镜头只会说 lens",
             "用 standard focal length（标准焦段）、kit lens（套头）、neutral perspective（中性透视）"],
            ["说视角只会说 angle",
             "用 46 degrees（46度）、30-60 degrees（30-60度）、human ergonomics（人体工学）"],
            ["说标准只会说 standard",
             "用 industrial history（工业历史）、the bestseller（爆款产品）、evolution（演化）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：50毫米、标准镜头、光学性能体积成本制造难度、最好的平衡、爆款产品、越极端的焦段、成像优秀且大光权的镜头越困难、早期焦片、套机捆绑标准焦段、45 50 55 58毫米、平排、便宜、容易上手出片、跌入摄影坑、第一台批量销售的35毫米相机、莱卡一、50毫米F3.5、套头搭配、制作变焦镜头技术、24-55、24-70、数码时代、50毫米定焦、套头销售、人眼视野、很容易批摇、50毫米拍的、视野比50毫米宽多了、运动相机的视角、近似人眼视角的理论、不是完全无道理、一幅画座前、调整离画幅的距离、画幅边缘、视角线、30-60度、人眼十字变色的视野范围、获取信息的密集区域、46度、35毫米胶卷的对角线、43毫米、整数的50毫米接近、最自然或中性的通知效果、早期工业能力、营销环境的历史原因、人体工学和审美、逐渐演化出来的概念、镜头的秘密、感谢收看、下期再见等。"
    },
    "5gYf1yxejcN": {
        "duration": "1:54", "topic": "摄影 · 曝光档位",
        "practice": [
            ["说一档定义", "One stop doubles or halves the light."],
            ["说两档倍率", "Two stops means four times, not twice."],
            ["说光圈倍率", "Aperture stops multiply by 1.4 due to circular area."],
            ["说STOP词源", "Stops come from Waterhouse insert apertures."],
            ["说ND单位", "ND2X/4X/8X and 0.3/0.6/0.9 map to 1/2/3 stops."]
        ],
        "pitfalls": [
            ["Think one stop equals a fixed amount.",
             "It's a doubling or halving of light.",
             "一档是倍增或减半。"],
            ["Add stops linearly.",
             "Two stops is four times the light.",
             "两档是四倍曝光。"],
            ["Expect aperture to follow integers.",
             "It uses the 1.4 factor from circular area.",
             "光圈倍率是1.4。"],
            ["Forget where 'stop' came from.",
             "It's from Waterhouse insert apertures.",
             "STOP源自插片光孔。"],
            ["Mix ND multiplier and density units.",
             "2X/4X/8X equals 0.3/0.6/0.9 equals 1/2/3 stops.",
             "ND单位别搞混。"]
        ],
        "shifts": [
            ["说曝光只会说 exposure",
             "用 one stop（一档）、EV value（EV值）、double or halve（加倍减半）"],
            ["说光圈只会说 aperture",
             "用 circular area（圆形面积）、1.4 factor（1.4倍率）、open a stop（开一档）"],
            ["说减光只会说 ND",
             "用 Waterhouse Stops（插片光孔）、reduction multiplier（减光倍率）、optical density（光密度）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：一档曝光、过曝一档、什么意思、怎么来的、stop、EV值、加减EV、增加一倍的亮度、减少一档、减一半的亮度、200%的E秒、100%的E秒、延长至、增加一档曝光、ISO100增加至一倍的ISO200、除以二、加两档、两倍乘以两倍等于四倍曝光、光圈有点点狡猾、圆形面积、1.4、F4出于1.4等于2.8、F4到F2.8、开一档光圈、F4乘以1.4等于5.6、F4到5.6、减少一档、收益档光圈、显著的规律、每个档位上的数字、上上档位的两倍、源于光圈、望远镜、减低入光的装置、光圈刚被发明、把镜头整体拆散、换上不同尺寸的光孔、19世纪50年代、John Waterhouse约翰水方先生、插片式光孔、提升换光圈的效率、WaterhouseStops、阻止了光的进入、ND镜、档标准、单位名称有所不同、ND2X ND4X ND8X、减光倍率、0.3 0.6 0.9、光密度、1档2档3档、单位对照、很明了、感谢收看这期视频、我是老粹、下期见等。"
    },
    "5fpZMfHJIGB": {
        "duration": "4:34", "topic": "摄影 · 逻辑光源",
        "practice": [
            ["说台灯角色", "A lamp is a movable, controllable practical light."],
            ["说库布里克蜡烛", "Barry Lyndon used special candles as the key light."],
            ["说逻辑光源", "Adding an explained source makes rim light logical."],
            ["说光位设计", "Logical light can be anything lit, not just a lamp."],
            ["说台灯高度优势", "Lamps sit at the ideal middle height for re-lighting."]
        ],
        "pitfalls": [
            ["Count lamps as mere decoration.",
             "They're cheat-level practical lighting tools.",
             "台灯是布光作弊技巧。"],
            ["Leave rim light unexplained.",
             "Add a logical source to justify it.",
             "轮廓光需要逻辑光源。"],
            ["Assume logical light must self-emit.",
             "Anything lit can serve as logical light.",
             "逻辑光不必自发。"],
            ["Tie lighting to one lamp type.",
             "Range hoods and other sources work too.",
             "油烟机灯同样可用。"],
            ["Let logical sources blow out.",
             "They need very fine brightness control.",
             "逻辑光源易过曝要精细调。"]
        ],
        "shifts": [
            ["说台灯只会说 lamp",
             "用 practical light（实景光源）、logical light（逻辑光源）、fill the light（补光）"],
            ["说布光只会说 lighting",
             "用 three-point lighting（三点布光）、rim light（轮廓光）、light-dark sandwich（三明治布光）"],
            ["说画面只会说 shot",
             "用 point of interest（兴趣点）、information drop（信息量）、visual depth（画面层次）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：一个两个三个四个五个六个七个、房间里真的需要这么多台灯、富人家庭、装修富力堂皇、普通人家庭、杂业有这么多盏台灯、电影里到处都是台灯、什么作用、笼统一点的回答、电影不光作弊极的技巧、移动可控的光源、合理出现在画面里、石井光源、什么地方缺光、放一盏台灯、物件和人物补光、创造兴趣点、地面散落的台灯、演员面部的主光来源、斯坦利库布里克、暴力美学、Barry Lyndon、室内晚宴的场景、拒绝放置人造光源、仅靠蜡烛作为主光、提高亮度、定做了特种蜡烛、竹星是一般蜡烛的三倍、燃烧速度也是三倍、颗灯月同款的蔡司50毫米、T10.7超大光圈镜头、ASA200的胶卷、电影史上一次艺术与技术结合的状惠、好莱坞中外台灯的全部原因、合理解释光从哪来、杀手剪、三点是曝光、每一个镜头里、逻辑的支撑、典型的三点式、主光从窗外来、辅光是空间里慢慢射回来的光、轮廓光作为唯一的卵色光源、没能解释清楚、显得没那么自然、加入一盏台灯、轮廓光立马就合理了、放置的角度、不能参与照亮演员的轮廓、对画面的帮助是显著的、未光标明来源的技法、增添逻辑光源、为何必须是台灯、换成油烟机的灯、完整光位、轮廓光、反光板给割开、避免污染、轮廓的逻辑光源、窗外还有一盏灯、亮度只开到了1%、演员的面光、四盏灯、逻辑很直观、逻辑光甚至不必是一个自发光源、被照亮的任何东西、窗外打到窗帘上的光、一道逻辑光、不参与演员面部的照明、围照街道的光、空穴来风的面光、逻辑支撑、铺了一层底子光、更显著的例子、没有一个直接为演员的发丝和轮廓提供逻辑的光源、太远了、角度严重不符、整个区域很关键、被暖色的光照亮、暗示画外还有一盏或者多盏光源、逻辑才能成立、动态连续的、前后镜头只要出现过逻辑光源、被观众记住、下一个画面角度不能再带到光源、逻辑依然通顺、台灯大放一彩、高度正好落在房间布高也不低的中间位置、不知多展台灯、拍摄机位怎么变动、方便快捷、重新补上面光浮光和轮廓光、并补破坏逻辑、逻辑光源需要出现在画面里、很容易过报、亮度调节的挡位需要非常精细、专门为台灯设计的补光灯泡、神流的NoLED-C7R、手机APP、无级调节亮度色温、RGB变色、灵活实时掌控多个逻辑光源、E27标准罗口设计、接入试电、什么时候会没电、平视的镜头、占多数、养世和腐蚀的构图、时代背景、设计其他形态的逻辑光源、星星点点的光源那么多、制造小光区、增加场景里的细节和反差、明暗明暗的三明治不光、画面有层次、拂起逻辑光源、不可或缺的使命、感谢粉丝们的认识、我是老崔、下期再见等。"
    },
    "4IALaRM1Q4Y": {
        "duration": "9:05", "topic": "摄影 · 曝光三要素",
        "practice": [
            ["说视频时代变化", "Video made the exposure triangle quietly outdated."],
            ["说ISO固定800", "Film locks one sensitivity: ISO 800, the gold standard."],
            ["说光圈代价", "Aperture changes ignore the cost of depth of field."],
            ["说跟焦艺术", "Hand focus pulls steer attention; shallow DOF tortures the puller."],
            ["说180度快门", "The shutter is set by the 180-degree rule per frame rate."]
        ],
        "pitfalls": [
            ["Adjust the three factors freely for video.",
             "Film locks ISO, aperture, and shutter for art.",
             "电影里三要素不可乱调。"],
            ["Swap film rolls for bad light.",
             "Adjust exposure, ND, or push/pull instead.",
             "换卷不如调光。"],
            ["Open the aperture for exposure.",
             "Shallow DOF hurts acting space and story.",
             "大光圈牺牲景深。"],
            ["Rely on autofocus for film.",
             "Focus is pulled by hand, aided not replaced.",
             "跟焦员不可替代。"],
            ["Slow the shutter when dark in video.",
             "The 180-degree rule fixes the shutter.",
             "视频调快门犯大忌。"]
        ],
        "shifts": [
            ["说曝光只会说 exposure",
             "用 exposure triangle（曝光三要素）、gold standard（黄金标准）、180-degree rule（180度原则）"],
            ["说景深只会说 depth of field",
             "用 acting space（表演区域）、focus puller（跟焦员）、artistic restraint（蓄势表达）"],
            ["说电影感只会说 cinematic",
             "用 persistence of vision（视觉暂留）、shutter angle（快门角度）、industrial legacy（工业遗产）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：光圈快门ISO为何过时了、拍立德、手机原相机摄影师、三座曝光基石、2026年、照片视频双修、摄影圣经、悄悄过时、拍视频不用曝光三要素、视频拍摄成为内容生产的主力、界限越来越模糊、专业的电影人、一二十个ISO档位、电影工业、感光度只有一个、ISO800、胶片年代、不同的感光度、挂上摄影机就无法更换、更换其实也很简单、牵扯出的问题太多、胶片是无法回看的、打乱拍摄的进度表、严谨的记录、归档管理工作、中途换下未用完的胶卷、不被浪费、稍有疏忽、后期冲印流程、不可逆转的事故、现场拍摄、光线不对、换一盘胶卷、调整曝光、增加减光片、后期破充减充、翻江倒海的动作、保险的多、ASA和色温、艺术表现工具、曝光工具、颗粒感、不同题材、情节氛围、色温同理、随意更换、很省事、不调ISO、原生感光度、模拟出来的、数字增益、推充和减冲、动态范围最大、画质最好的挡位、画质最优秀的毛片、不会碰感光度、R来摄影机的原生ISO就是800、甜点挡位、黄金标准、白天加一片ND、晚上也不需要过分曝光、Red索尼尼康加能、默契选择、不遵守这套法则、故意提高感光度、高噪点、自媒体行业卷到飞起、追求最好的画质、默默遵守、双原生、三原生ISO、满血的画质表现、多帧合成技术、风起云涌、随意可调的感光度、憋了很久了、调快门光圈不就解决了吗、很抱歉、也不可以的、打开光圈画面提亮、收起光圈画面变暗、最灵活的曝光掌控、苦口婆心、大光圈牛头、蓄势的艺术、技术的艺术、调节光圈往往忽略了很重要的代价、景深、光圈越大景深越浅、剧情表达、景深太重要了、两个人物在画面里、胶平面、稍微动一点点、虚焦、提高景深、表演区域、自动对焦、跟焦都是活人手动完成、焦点的推拉、调动观众的注意力、蓄势表达、准确性、景深太浅、跟焦员的噩梦、T2.8、非常大的光圈、好莱坞、自动跟焦的方案、大将、拉达跟焦器、辅助跟焦员、代替跟焦员、内容消费的中端、手机和平板、屏幕越来越小、背景虚化、呈现难度、大萤幕、猛猛开光圈、虚化的背景、陶醉、光圈全开拍到底、景深来展示剧情线索、前景和背景、剧情的重要位置、主体清晰、前后景虚得一塌糊涂、信息量大大降低、导演摄影美书灯光、设计前后景、远近都有戏、公民凯恩、超景深、巨大的表演区域、前后景同时表演、超大功率的照明、满足导演对画面的追求、经典、超前的景深、折磨更较远、光圈布光和解光、艺术蓄视工具、分镜策划、场地道具灯光演员走位摄影走位、大机器运作中的一环、画面太暗加灯光、画面太亮加ND、小范围的改动、导演预想中的效果、出于艺术的考量、为何快门也不能调、180度原则、为了电影感、拍照片、画面太暗、减慢快门、立竿见影、拍视频、调节快门犯了大忌、48分之1秒、24帧、24张图片、连贯动感的错觉、人眼的帧率也是24帧、错误的、动态的、持续的、横定帧率的机制、注意力和生命机能、电竞选手、144Hz、240Hz、高刷、生病、醉酒、王家卫电影、常曝光降格、拖影、光线通过晶体、视网膜、感光细薄、化学信号、10分之1到15分之1秒、视觉战流、动态模糊、重叠、小实验、昏暗点、举起手臂、挥舞、拖影、手电筒、开到最亮、拖影长了很多、更强刺激、恢复敏感度、视网膜时间更长、判断进入视线的物体、从哪个方向来、往哪个方向去、物理世界里运动、狩猎、躲避危险、动态模糊的原理、标准帧率、默片时期、16帧每秒、同声机、兼容声音画面、稳定播放、24帧每秒、极限帧率、最低帧率、过于清晰、觉察到、单独的图片、大范围的运动、打消错觉、24匹、正确运动模糊的水平摇进画面、一卡一卡、180度又是个啥意思、圆盘、镂空的地方、曝光的时长、遮挡的地方、更换下针胶片、缝隙越小、曝光时长越短、画面越锐利、动态模糊越小、180度的镂空角度、自然的动态模糊、现代摄影机快门结构、已经完全改变、快门角度原则、人定下的规矩、可以打破、战争动作片、高度危险、圣上线速爆发、身体技能提升、看得更快更广、注意力更集中、提高快门速度、模拟战争现场感、王家卫的爆款漫门、48分之1秒、不同针对下、统一用180度原则、公式是针对的2倍分之1、工业历史的遗产、100多年、人类文明GTG、视觉烙印、本能认为、电影感、推翻替代、不好说、该遵守的还是得遵守、感受看这期春摄影、我是老翠、下期再见等。"
    },
    "2BtKsAgGSeO": {
        "duration": "2:50", "topic": "Vlog · 旅行剪辑",
        "practice": [
            ["说旅行素材逻辑", "A trip is made of separate events to film."],
            ["说1+3模板", "One talking shot plus wide, action, and state shots."],
            ["说镜头数量", "One minute of rich video needs 25-30 shots."],
            ["说AI配音", "Clone your voice or record your own narration."],
            ["说一键混剪", "Auto-edit assembles and is ready to upload."]
        ],
        "pitfalls": [
            ["Shoot aimless clips with no template.",
             "Use the 1+3 template per event.",
             "没模板素材难用。"],
            ["Film only talking or only scenery.",
             "Wide, action, and emotion cover the story.",
             "叙事需要三类镜头。"],
            ["Under-shoot a one-minute vlog.",
             "Aim for 25-30 shots per minute.",
             "一分钟要25-30个镜头。"],
            ["Narrate yourself when in a rush.",
             "Import the script and use your cloned voice.",
             "赶时间用克隆配音。"],
            ["Edit frame by frame manually.",
             "Auto-edit assembles fast and uploads immediately.",
             "一键混剪立即上传。"]
        ],
        "shifts": [
            ["说素材只会说 footage",
             "用 1+3 template（1+3模板）、separate events（独立事件）、shot count（镜头数）"],
            ["说镜头只会说 shot",
             "用 establishing wide（远景）、action shot（动作镜头）、emotional state（情绪状态）"],
            ["说剪辑只会说 edit",
             "用 voice clone（克隆声音）、auto-edit（一键混剪）、script import（脚本导入）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：放下出来玩、手机里面塞了一堆的素材、想减、如何下手、零碎的素材、快速组装、高质量又流量、旅行vlog、发朋友圈很有面子、搭小红书一言能成为报款、同家的方法、揣兜里、千万别弄丢了、先说拍摄、多个单独事件组成、朋友去吃当地的夜市小吃、打卡某某景点、一起去泡汤、每一个事件、1加3的模板、积累素材、1就是首先你要拍一个对着镜头说话的画面、跟朋友们约了一只泡汤的活动、3是一起在vlog灭万能的敘事镜头、三类镜头、园景、动作和容状态、拍一个来泡汤的环境里面的一个园景、手拿食物的动作、我跟朋友说话、面部表情的情绪状态、夜市的环境里面、夜市的园景、拿食物或者吃食物的动作型的画面、情绪、画面里的人当然也可以是说话的、进入一个新的场景、一个新的事件、1加3的模板去积累你的拍摄素材、记住一个数字、1分钟的视频、画面丰富一点、大概需要25到30个镜头、心里面有数、素材积累得差不多、后期险阶、导入清险阶软件、选择配音的方式、非常着急、最快的就是把脚本直接导入进去、克隆了一个我自己的声音、这个国庆假期我打算不出北京、找了几个在北京的好朋友一起沉浸市聚会、非常相似、直接用你克隆的声音、配音、自己读出来更加自然、点击这个录音、录音的感受、比较一下、配音搞进去、点击这个混减、很快能给你混减出来、减的这个效果、不用赶高铁、不用激进区、不用出眼门、把城市玩出新鞋样的感觉、国庆最期待的打开方式、非常不错、非常快速地制作出你的旅行blog、立即上传、blog制作得更大惊良、主页、实习万人看过的万能blog公事、非常非常详细、新粉、脚本的干货、主页播过课、点击关注等。"
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
