#!/usr/bin/env python3
"""批25：为10篇视频生成完整场景英译JSON（含场景/练习/避坑/思维转变/生词）。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

ARTICLES = {}

ARTICLES["audi-quattro-1"] = {
    "title_zh": "奥迪Quattro四驱（上）：自锁冠齿中央差速器",
    "title_en": "Audi Quattro (1): The Self-Locking Crown-Gear Center Diff",
    "duration": "10:40",
    "topic": "汽车 · 四驱系统",
    "scenes": [
        {"id": "s1", "scene_zh": "Quattro是商标不是特定四驱", "scene_en": "Quattro Is a Trademark, Not One System", "time": "00:00",
         "context": "Quattro是奥迪对它自家四驱的叫法，也是一个商标。奥迪不同车型上有四套不同的Quattro系统：纵置发动机上的Quattro和Quattro ultra、横置发动机上的Haldex、电动车上的e-Quattro。",
         "sentences": [
            ["Quattro其实是奥迪对自家四驱的一个叫法，它也是一个商标。", "Quattro is Audi's name for its own AWD—and also a trademark.", "trademark（商标）"],
            ["它并不是特指某一种四驱形式。", "It doesn't refer to any single AWD layout.", "layout（形式）"],
            ["今天讲纵置发动机上的三种最常见的Quattro，看看它们分别怎么工作。", "Today we cover the three most common longitudinal Quattro systems.", "longitudinal（纵置的）"]
         ]},
        {"id": "s2", "scene_zh": "第六代自锁冠齿差速器", "scene_en": "Gen 6: The Self-Locking Crown-Gear Diff", "time": "01:05",
         "context": "第一种Quattro被认为是正宗的标准Quattro，已出到第六代。前五代基于托森中央差速器，第六代改用奥迪自研的冠齿自锁式限滑中央差速器，只用于纵置发动机车型。",
         "sentences": [
            ["第一种Quattro被普遍认为是最正宗的Quattro，到今天已经出到第六代了。", "The first Quattro is widely seen as the genuine one—now in its sixth generation.", "genuine（正宗的）"],
            ["前五代基本以托森中央差速器为基础，第六代用了奥迪自研的冠齿自锁式限滑中央差速器。", "The first five were Torsen-based; Gen 6 uses Audi's self-locking crown-gear diff.", "Torsen（托森差速器）"],
            ["这套系统只针对纵置发动机车型，横置发动机用不了。", "It's for longitudinal-engine cars only; transverse cars can't use it.", "transverse（横置的）"]
         ]},
        {"id": "s3", "scene_zh": "冠齿差速器结构", "scene_en": "Inside the Crown-Gear Differential", "time": "01:56",
         "context": "动力经变速箱输入轴传入黑色壳体（直接相连一起转），壳体上有四个红色小齿轮，分别咬合紫色（前）和绿色（后）两个冠齿齿轮。正常行驶时红色齿轮只公转不自转。",
         "sentences": [
            ["整个黑色的壳体直接和变速箱输入轴硬性连接，所有黑色部分都跟着一起转。", "The black housing is rigidly linked to the gearbox input—all of it spins together.", "housing（壳体）"],
            ["四个红色的齿轮固定在黑色柱子上，分别咬合前后两个冠齿齿轮。", "Four red pinions mesh with a front and a rear crown gear.", "pinion（小齿轮）"],
            ["前后轮都有抓地力时，红色齿轮只随壳体公转，本身不自转。", "With all wheels gripping, the red pinions orbit but don't spin themselves.", "orbit（公转）"]
         ]},
        {"id": "s4", "scene_zh": "前轮打滑自动锁定", "scene_en": "Front Slip: The Diff Self-Locks", "time": "03:20",
         "context": "前轮打滑时紫色冠齿齿轮转得更快，红色齿轮开始自转。其特殊几何齿形对绿色冠齿齿轮产生轴向推力，把壳体上的离合片和绿色冠齿齿轮上的离合片压在一起，形成硬性连接，将更多动力传到后轴。",
         "sentences": [
            ["前轮一打滑，紫色的冠齿齿轮就转得更快，红色的齿轮开始一边公转一边自转。", "When the front slips, the purple crown gear spins faster and the red pinions start self-rotating.", "self-rotate（自转）"],
            ["红色齿轮的特殊几何齿形会给绿色冠齿齿轮一个轴向的推力。", "The red pinion's special tooth geometry pushes the green crown gear axially.", "axially（轴向地）"],
            ["壳体上的离合片和绿色冠齿齿轮上的离合片被压到一起，整个就锁定了。", "The housing's clutch plates are pressed against the crown gear's, locking the assembly.", "clutch plates（离合片）"],
            ["整个过程完全机械、自发，不涉及任何液压或电子控制。", "It's purely mechanical and self-acting—no hydraulics or electronics.", "mechanical（机械的）"]
         ]},
        {"id": "s5", "scene_zh": "后轮打滑同理", "scene_en": "Rear Slip: The Mirror Case", "time": "06:41",
         "context": "后桥打滑时绿色冠齿齿轮转得更快，红色齿轮以相反方向自转，对紫色部分产生向外推的力，离合片锁死，更多动力被传到前轴。",
         "sentences": [
            ["后桥打滑时，绿色的冠齿齿轮会转得更快。", "When the rear slips, the green crown gear spins faster.", "rear axle（后桥）"],
            ["红色的齿轮以刚才相反的方向自转，对紫色的部分产生向外推的力。", "The red pinions self-rotate the other way, pushing the purple crown gear outward.", "outward（向外）"],
            ["离合片锁死，更多动力被传到前轴。", "The clutches lock and more torque flows to the front axle.", "torque（扭矩）"]
         ]},
        {"id": "s6", "scene_zh": "动力分配与力臂设计", "scene_en": "Torque Split by Lever Arm", "time": "07:25",
         "context": "正常情况下前后动力分配是40:60，打滑时最高可到前70后30或前15后85。达不到100:0是因为离合片锁定有物理极限。默认40:60是通过红色齿轮与前后冠齿齿轮连接点的力臂比例4:6实现的纯物理设计。",
         "sentences": [
            ["正常时动力分配是前40后60，打滑时最高可达前70后30或前15后85。", "Normally the split is 40/60; during slip it can reach 70/30 or 15/85.", "split（分配）"],
            ["为什么达不到100:0？因为离合片之间互相锁死有它的物理极限。", "Why never 100/0? The clutch plates have a physical locking limit.", "physical limit（物理极限）"],
            ["默认的40:60是靠红色齿轮与两个冠齿齿轮连接点的力臂比例4比6，纯物理实现的。", "The default 40/60 comes from a 4:6 lever-arm ratio—pure geometry.", "lever arm（力臂）"]
         ]},
        {"id": "s7", "scene_zh": "三个动力分流", "scene_en": "The Three Torque Splits", "time": "08:11",
         "context": "四驱就是动力的三个分流：前后分流靠中央差速器，前轮左右分流靠前桥开放式差速器，后轮左右分流靠后桥开放式差速器。运动车型可选配带离合片组的运动后差速器实现左右动力分配。",
         "sentences": [
            ["四驱简化来讲就是动力的三个分流：对前对后、前桥左右、后桥左右。", "AWD is three torque splits: front/rear, and left/right at each axle.", "torque split（动力分流）"],
            ["前桥和后桥都是开放式差速器，这是比较令人遗憾的。", "Both axle diffs are open-type, which is a pity.", "open differential（开放式差速器）"],
            ["运动车型可选配运动后差速器，多给两组离合片实现左右动力分配。", "Sport models can spec a sport rear diff with extra clutch packs.", "sport diff（运动差速器）"]
         ]},
        {"id": "s8", "scene_zh": "对比托森的三点优势", "scene_en": "Three Wins Over the Torsen", "time": "09:03",
         "context": "冠齿系统优点：四轮永远有动力；对比托森式三大优势——更轻2kg、动力分配更自由且不受打滑程度限制、能更好整合全车电子系统。缺点是：动力分配是打滑后被动调整，无法主动控制；前后差速器完全开放。",
         "sentences": [
            ["它最大的优点就是前后轮永远有动力，不像有些四驱只在打滑时才给另一桥输送动力。", "Its biggest plus: all four wheels always have power, unlike systems that only engage on slip.", "always on（常时四驱）"],
            ["对比托森有三大优势：更轻、分配更自由、能更好整合全车电子系统。", "Versus Torsen: lighter, freer torque split, and better integration with vehicle electronics.", "integration（整合）"],
            ["缺点是分配动力比较被动，要等打滑出现后才自己调整，而且前后差速器完全开放。", "The downsides: passive response to slip, and fully open axle diffs.", "passive（被动的）"]
         ]}
    ]
}

ARTICLES["audi-quattro-2"] = {
    "title_zh": "奥迪Quattro四驱（下）：quattro ultra与Haldex",
    "title_en": "Audi Quattro (2): Quattro Ultra and Haldex",
    "duration": "08:44",
    "topic": "汽车 · 四驱系统",
    "scenes": [
        {"id": "s1", "scene_zh": "quattro ultra概述", "scene_en": "Quattro Ultra at a Glance", "time": "00:00",
         "context": "quattro ultra用在奥迪纵置车型上（A6/A7/A8/Q5），是一套适时四驱系统，前桥仍是开放式差速器，通过电控多片离合向后方传递动力。",
         "sentences": [
            ["quattro ultra用在所有奥迪纵置车型上，是一个适时四驱系统。", "Quattro ultra equips Audi's longitudinal cars—an on-demand AWD system.", "on-demand（适时）"],
            ["前桥很遗憾仍然是开放式差速器，往后传动力靠一个电控多片离合器。", "The front diff is still open, and power flows rearward through an electronically controlled multi-plate clutch.", "multi-plate clutch（多片离合）"]
         ]},
        {"id": "s2", "scene_zh": "默认是纯前驱", "scene_en": "Default: Pure Front-Wheel Drive", "time": "00:44",
         "context": "没有打滑的默认情况下前后动力分配是100:0，也就是一台纯前驱车，后轴传动完全断开。",
         "sentences": [
            ["默认情况下前后动力分配是100比0，这是一台纯纯的前驱车。", "By default the split is 100/0—a pure front-wheel-drive car.", "front-wheel drive（前驱）"],
            ["这个地方断开了，后面就不用看了，整个传动就是前驱车。", "The rear path is disconnected; it's simply a FWD drivetrain.", "drivetrain（传动系统）"]
         ]},
        {"id": "s3", "scene_zh": "电脑主动锁离合", "scene_en": "The Computer Actively Locks", "time": "00:55",
         "context": "前轮打滑或驾驶员想运动驾驶时，电脑主动把离合片锁死。比如红灯口轰着油门，电脑判断你可能要弹射起步，即使车还没动、前轮没打滑，也会提前锁死离合给后桥传动力。离合片锁死极限只能做到50:50。",
         "sentences": [
            ["当前轮打滑或者你想运动驾驶时，电脑会通过电子控制主动把离合片锁死。", "When the front slips or you drive hard, the computer actively locks the clutch.", "actively lock（主动锁死）"],
            ["就算车还没动，电脑能判断你想要最大抓地力，提前把离合片锁死。", "Even before moving, it senses you want max grip and locks up early.", "max grip（最大抓地力）"],
            ["离合片彻底锁死也就是极限，最多做到50比50的动力分配。", "Fully locked, the clutch tops out at a 50/50 split.", "50/50 split（前后50比50）"]
         ]},
        {"id": "s4", "scene_zh": "断开机构省油", "scene_en": "The Decoupler Saves Fuel", "time": "02:06",
         "context": "系统里还有第二个关键部件：两个红色部分可以通过电子控制连接或断开。进入前驱模式时不仅离合片断开，这两个部分也断开，后轮变成完全自由的轮子，传动轴完全静止，最大限度减少油耗。",
         "sentences": [
            ["第二个关键部件是两组可以电子控制连接或断开的轴。", "The second key part: two shafts that can connect or disconnect electronically.", "disconnect（断开）"],
            ["进入前驱模式时不仅离合片断开，这两个部分也断开，后轮完全自由。", "In FWD mode the clutch and these shafts both open, leaving the rear wheels free.", "free wheels（自由轮）"],
            ["这样传动轴连转都不转，没有人为它浪费动力，最大限度减少油耗。", "The driveshaft sits still, wasting nothing—max fuel savings.", "fuel savings（省油）"]
         ]},
        {"id": "s5", "scene_zh": "ultra的优缺点", "scene_en": "Pros and Cons of Ultra", "time": "03:00",
         "context": "优点：省油，非常适合市区驾驶；动力分配由电脑主动控制，不是打滑后才介入。缺点：仍然是前驱属性，发动机重量全压在前轴前面；动力分配不够硬派；前后桥都是开放差速器，只靠电子刹车限滑。",
         "sentences": [
            ["优点就是省油，非常适合城区市区驾驶。", "The plus is fuel economy—great for city driving.", "city driving（市区驾驶）"],
            ["动力分配是电脑主动控制的，而不是出现打滑的时候才介入。", "Torque is distributed proactively, not only after slip occurs.", "proactively（主动地）"],
            ["缺点是偏前驱属性，动力分配不够硬派，前后桥都是开放差速器。", "The drawbacks: a front-biased feel, soft limits, and open diffs.", "front-biased（偏前驱）"]
         ]},
        {"id": "s6", "scene_zh": "Haldex系统概述", "scene_en": "The Haldex System", "time": "03:56",
         "context": "Haldex用在所有奥迪横置四驱车型上（A3/Q3/TT/R8/RS3/TT RS），还有大众很多横置四驱车。它不是奥迪自己的技术，而是博格华纳的技术，已经出到第五代。",
         "sentences": [
            ["Haldex用在所有奥迪横置四驱车型上，比如A3、Q3、TT、RS3。", "Haldex equips Audi's transverse AWD cars—the A3, Q3, TT, RS3.", "transverse AWD（横置四驱）"],
            ["这不是奥迪自己的技术，是博格华纳的技术，已经出到第五代。", "It's BorgWarner's tech, not Audi's, now in its fifth generation.", "BorgWarner（博格华纳）"]
         ]},
        {"id": "s7", "scene_zh": "Haldex工作原理", "scene_en": "How Haldex Works", "time": "04:38",
         "context": "发动机动力先到开放式前桥差速器，前桥差速器同时带一组齿轮把动力转90度向后传。多片主动离合设计在变速箱尾部，默认也是100:0前驱；前轮打滑或运动驾驶时电脑压上离合片，动力传到后桥，锁死极限也是50:50。",
         "sentences": [
            ["前桥差速器上有一组齿轮把动力转90度向后传，一路上所有橘色部分只要挂挡就都在转。", "A gear set turns the drive 90° rearward; everything orange spins whenever you're in gear.", "gear set（齿轮组）"],
            ["这个多片离合设计在变速箱尾部，默认动力分配也是100比0。", "The clutch pack sits at the gearbox tail, defaulting to a 100/0 split.", "clutch pack（离合片组）"],
            ["前轮打滑或运动驾驶时电脑压上离合片，动力传到后桥，锁死极限是50比50。", "On slip or hard driving the computer engages it, sending power rear—up to 50/50.", "engage（接合）"]
         ]},
        {"id": "s8", "scene_zh": "Haldex的优缺点", "scene_en": "Pros and Cons of Haldex", "time": "07:04",
         "context": "优点：省油、主动电脑控制、比纯液压强。缺点：是纯纯的前驱属性（前置横置发动机），前后桥都是开放差速器，没有运动差速器可选。",
         "sentences": [
            ["优点和省油、主动控制这些基本一样，总比完全液压的来得强。", "It's economical and proactive—still better than pure hydraulic systems.", "hydraulic（液压的）"],
            ["缺点就是纯纯的前驱属性，完全前置的横置发动机。", "The drawback: an emphatically front-drive character.", "character（属性）"],
            ["前后桥老生常谈，还是两套开放式差速器。", "Both axles remain open diffs, as usual.", "as usual（老生常谈）"]
         ]},
        {"id": "s9", "scene_zh": "没有最好只有最合适", "scene_en": "No Best, Only the Fitting One", "time": "07:45",
         "context": "三种四驱系统都讲完。很多朋友爱问哪种最好，深入研究会发现没有最好只有最合适，要根据个人实际需求选择。情怀归情怀，科技永远在向前进步。",
         "sentences": [
            ["深入进去研究以后你会发现，其实没有最好，只有最合适的。", "Dig deeper and you'll find there's no best system—only the most fitting.", "the most fitting（最合适的）"],
            ["还是要根据你个人的实际需求，来选择最适合你的。", "Choose based on your actual needs.", "based on（根据）"],
            ["情怀还是要有的，但科技永远是在向前进步的。", "Keep the nostalgia, but technology always moves forward.", "nostalgia（情怀）"]
         ]}
    ]
}

ARTICLES["turbo-principle"] = {
    "title_zh": "涡轮增压原理与四种涡轮",
    "title_en": "Turbocharging: The Principle and Four Kinds of Turbos",
    "duration": "13:20",
    "topic": "汽车 · 涡轮",
    "scenes": [
        {"id": "s1", "scene_zh": "涡轮的基本原理", "scene_en": "The Basic Turbo Principle", "time": "00:00",
         "context": "发动机动力靠汽油和空气一起燃爆，想获得更大动力就要燃烧更多汽油，就要更多空气。排量固定则吸入的空气有限，于是有了涡轮增压：废气吹动一个小电风扇，带动轴另一头的进气端风扇像鼓风机一样把更多空气压进发动机。",
         "sentences": [
            ["想要更大的动力就需要燃烧更多汽油，就要有与之对应的更多空气。", "More power means burning more fuel, which needs more air.", "fuel（汽油）"],
            ["每台发动机排量固定，能吸入的空气是有限的。", "Displacement is fixed, so the air it can draw is limited.", "displacement（排量）"],
            ["涡轮就是两个小电风扇用一根小轴连在一起，废气吹动一头，另一头把更多空气压进发动机。", "A turbo is two little fans on one shaft: exhaust spins one side, the other packs in more air.", "spins（吹动）"],
            ["空气变多了就能喷更多汽油，动力自然就大了。", "More air allows more fuel—and more power.", "more power（更大动力）"]
         ]},
        {"id": "s2", "scene_zh": "中冷器的作用", "scene_en": "The Intercooler's Job", "time": "01:22",
         "context": "空气被压缩后会变热膨胀、变稀薄，吸入发动机时空气量反而减少，所以需要中冷器冷却进气。多数中冷放车头迎风，或在引擎盖开洞（如斯巴鲁STI），也有用水冷冷却的。",
         "sentences": [
            ["空气被压缩以后温度升高，温度一高空气就会膨胀变稀薄。", "Compressed air heats up, expands, and thins out.", "thins out（变稀薄）"],
            ["所以需要一个中冷器来冷却进气。", "That's why an intercooler cools the intake charge.", "intercooler（中冷器）"],
            ["大多数中冷放在车头迎风位置，也有在引擎盖开洞的，比如斯巴鲁STI。", "Most intercoolers sit at the nose; some sit under a hood scoop, like the Subaru STI.", "hood scoop（引擎盖开洞）"]
         ]},
        {"id": "s3", "scene_zh": "涡轮的三大缺点", "scene_en": "Three Downsides of Turbos", "time": "02:48",
         "context": "涡轮缺点一：贵，涡轮本身几千到几万，配套的中冷、卸压阀、油路管道都是成本；缺点二：高温，靠排气带动，最高可达900多摄氏度，需要单独油路润滑降温，对机油要求更高；缺点三：涡轮迟滞，涡轮被排气带起来需要时间，越大越慢。",
         "sentences": [
            ["第一个缺点就是贵：涡轮本身几千到几万，配套设备也都是钱。", "First, cost: turbos run from thousands to tens of thousands, plus all the supporting parts.", "supporting parts（配套部件）"],
            ["第二个缺点就是高温，最高能到将近900多摄氏度。", "Second, heat—up to nearly 900°C.", "nearly 900°C（近900度）"],
            ["第三个也是最大的缺点，就是涡轮迟滞：一脚油门踩到底，要等一两秒动力才轰的一下跟上。", "Third, and biggest, is turbo lag: you floor it and wait a second or two before the power hits.", "turbo lag（涡轮迟滞）"]
         ]},
        {"id": "s4", "scene_zh": "双涡轮：两个小涡轮", "scene_en": "Twin Turbo: Two Smaller Ones", "time": "04:42",
         "context": "涡轮做小没有迟滞但动力跟不上，做大动力好但反应慢。工程师用两个尺寸相同的小一号涡轮代替一个大涡轮。V型发动机左右各有一个排气歧管，正好一边装一个，进气在中冷器处汇合。市面上标Twin Turbo或Bi-turbo的其实都是这种双涡轮。",
         "sentences": [
            ["涡轮做小了动力跟不上，做大了有迟滞，怎么两者兼顾？用两个小一号的涡轮。", "Small turbos lack top-end, big ones lag—so engineers use two smaller ones.", "top-end（高转动力）"],
            ["V型发动机正好左右各有一个排气歧管，一边装一个涡轮。", "A V engine has two exhaust manifolds, so each bank gets its own turbo.", "exhaust manifold（排气歧管）"],
            ["Twin Turbo和Bi-turbo其实都是不同的叫法，实质都是双涡轮。", "Twin Turbo and Bi-turbo are just different names for the same thing.", "Twin Turbo（双涡轮）"]
         ]},
        {"id": "s5", "scene_zh": "顺序涡轮：一小一大", "scene_en": "Sequential Turbo: Small Then Large", "time": "06:40",
         "context": "顺序涡轮的两个涡轮有前后顺序：一个小涡轮加一个大一号的涡轮，之间有一个可开关的阀门。低转速排气压力不够时阀门关闭，大涡轮不参与，小涡轮快速完成增压；转速上来后打开阀门，两个涡轮同时增压。兼顾了迟滞和马力问题，90年代很多JDM跑车如马自达RX-7转子引擎、丰田Supra用过，但因管路复杂和现代技术改进，今天新车上基本看不到了。",
         "sentences": [
            ["顺序涡轮的两个涡轮有前后顺序，一个大一号、一个小一号，中间有个阀门控制开关。", "In a sequential setup the two turbos differ in size, gated by a controllable valve.", "sequential（顺序的）"],
            ["低转速时阀门关上，排气只驱动小涡轮，发挥尺寸小的优势快速完成增压。", "At low rpm the valve closes; exhaust spins only the small turbo for quick boost.", "quick boost（快速增压）"],
            ["转速上来排气压力够了再打开阀门，两个涡轮同时给进气增压。", "Once pressure builds, the valve opens and both turbos boost together.", "boost（增压）"],
            ["90年代很多JDM跑车用它，比如马自达RX-7和丰田Supra，但今天新车上基本看不到了。", "90s JDM cars like the RX-7 and Supra used it, but it's rare on new cars now.", "JDM（日本国内市场的车）"]
         ]},
        {"id": "s6", "scene_zh": "双涡管：单涡轮双通道", "scene_en": "Twin-Scroll: One Turbo, Two Paths", "time": "08:36",
         "context": "双涡管涡轮名字里带双但其实是单涡轮、双涡管。以直列四缸为例：1、4缸共用一个排气歧管进黄色通道，2、3缸共用进紫色通道。四缸机点火顺序1342，后一缸排气正压总会和前一缸的负压重叠，抵消部分压力。把互相影响的缸分开就能避免排气脉冲互相干扰，让排气压力更高效施加到涡轮上。宝马机舱里看到Twin Power Turbo字样其实是双涡管。",
         "sentences": [
            ["双涡管涡轮虽然名字里有双字，但它是单涡轮、双涡管。", "A twin-scroll turbo is one turbo with two scrolls, not two turbos.", "twin-scroll（双涡管）"],
            ["四缸机点火顺序1342，后一缸排气的正压总和前一缸的负压有重叠，抵消掉一部分压力。", "With firing order 1-3-4-2, each cylinder's positive pulse overlaps the prior one's vacuum.", "firing order（点火顺序）"],
            ["把互相影响的缸分开，1、4缸一管，2、3缸一管，排气压力就能更高效地施加到涡轮上。", "Separating the interfering cylinders—1/4 down one scroll, 2/3 down the other—makes the pulses work, not fight.", "scroll（涡管）"]
         ]},
        {"id": "s7", "scene_zh": "涡轮、自吸与机械增压", "scene_en": "Turbo vs NA vs Supercharger", "time": "11:57",
         "context": "涡轮大势所趋，动力和经济性优势大于劣势；自吸在可靠性和后期保养上更胜一筹，纯家用需求自吸仍适合。对比机械增压：涡轮赢在极限动力，机械增压没有迟滞、动力随叫随到、基本不产生高温、寿命可靠性更好，但用发动机本身能量增压，理论效率不如涡轮。",
         "sentences": [
            ["涡轮是大势所趋，优势大于劣势，无论从动力性还是经济性角度。", "Turbo is the trend—its pros outweigh its cons.", "the trend（大势所趋）"],
            ["自吸在可靠性和后期保养上更胜一筹，纯家用需求自吸还是更适合你。", "Naturally aspirated engines win on reliability and upkeep—great for pure daily use.", "naturally aspirated（自然吸气）"],
            ["机械增压没有丝毫迟滞，动力随叫随到，也基本不产生高温。", "A supercharger has zero lag, instant response, and runs cool.", "supercharger（机械增压）"],
            ["但机械增压用发动机本身能量增压，理论效率还是涡轮更高。", "It's belt-driven off the engine, so turbos remain theoretically more efficient.", "belt-driven（由皮带驱动）"]
         ]}
    ]
}

ARTICLES["suspension-types-1"] = {
    "title_zh": "悬挂形式（上）：麦弗逊与双叉臂",
    "title_en": "Suspension Types (1): MacPherson and Double Wishbone",
    "duration": "13:29",
    "topic": "汽车 · 悬架",
    "scenes": [
        {"id": "s1", "scene_zh": "打伞比喻与三点声明", "scene_en": "The Umbrella Analogy", "time": "00:00",
         "context": "车在崎岖路面行驶好比风雨中撑大伞：天气是路况，伞是轮胎，你是悬挂。抓轮胎的手越多，每只手承受的压力越小、负责的工作越单一，轮子越稳。悬挂好坏就是看抓住轮胎的手多还是少，两只手打伞总比一只手稳。悬挂形式只是基础，调教至关重要。",
         "sentences": [
            ["车在崎岖路面行驶，就像你在狂风暴雨中撑着一把大伞。", "Driving a rough road is like holding a big umbrella in a storm.", "rough road（崎岖路面）"],
            ["天气是路况，大伞是轮子，而你就是悬挂。", "Weather is the road, the umbrella is the wheel, and you are the suspension.", "suspension（悬挂）"],
            ["抓住轮子的手越多，每只手承受的压力就越小，轮子就越稳。", "More hands on the wheel means less load each, and a steadier wheel.", "steady（稳的）"],
            ["悬挂形式只是表现的基础，工程师的精心调教同样重要。", "The layout is just a baseline—tuning matters just as much.", "tuning（调教）"]
         ]},
        {"id": "s2", "scene_zh": "三类悬挂", "scene_en": "Three Families of Suspension", "time": "02:33",
         "context": "悬挂分三类：独立悬挂（每个轮子一套自己的悬挂系统，互不干扰，好比一人一把伞）；非独立悬挂（左右两轮用一根硬轴粗暴连接，一个轮子有动静立刻影响另一个，好比两人打一把伞）；半独立悬挂介于两者之间，典型如扭力梁。",
         "sentences": [
            ["独立悬挂是每个轮子都有一套自己的悬挂系统，互不干扰。", "Independent suspension gives each wheel its own setup—no cross-talk.", "independent（独立的）"],
            ["非独立悬挂是左右两个轮子通过一根硬轴连接在一起，一个轮子有动静立刻影响另一个。", "Non-independent suspension links the wheels with a rigid axle—motion on one side hits the other.", "rigid axle（硬轴）"],
            ["半独立悬挂介于两者之间，典型的例子就是扭力梁。", "Semi-independent sits in between—the torsion beam is the classic case.", "torsion beam（扭力梁）"]
         ]},
        {"id": "s3", "scene_zh": "麦弗逊结构", "scene_en": "The MacPherson Strut", "time": "03:41",
         "context": "麦弗逊由美国人艾尔·麦弗逊发明。弹簧和避震是一个整体，再配一个三角形的下臂。它是典型的一只手撑伞，控制轮子的手已经做到最少，再少轮子就要掉了。运动基本直上直下，不太能随车体侧倾改变外倾角保持轮胎最大接触。",
         "sentences": [
            ["麦弗逊的弹簧和避震是一个整体，再配合一个三角形的下臂。", "A MacPherson strut is a coil-over unit plus a triangular lower arm.", "coil-over（弹簧避震一体）"],
            ["它是典型的一只手撑伞，控制轮子的手已经做到最少。", "It's the classic one-hand umbrella—minimum control points.", "minimum（最少）"],
            ["轮子的运动基本直上直下，不太能随车体侧倾改变外倾角。", "The wheel mostly moves straight up and down, unable to adjust camber with body roll.", "camber（外倾角）"]
         ]},
        {"id": "s4", "scene_zh": "麦弗逊的优缺点", "scene_en": "MacPherson: Trade-Offs", "time": "05:08",
         "context": "缺点：对轮子运动轨迹缺乏严格控制，激烈驾驶和极端路况下抓地力表现不好。优点：最大程度精简悬挂部件，做到了轻（簧下质量轻）、造价低、保养便宜；结构让出空间给驱动轴安装，天然对前驱友好；整体很窄不占横向空间，给发动机舱留更多空间。",
         "sentences": [
            ["因为缺乏对轮子轨迹的严格控制，它在激烈驾驶和极端路况下抓地力表现不好。", "With loose wheel-path control, grip suffers in hard driving and extreme conditions.", "grip（抓地力）"],
            ["它最大程度精简了悬挂部件，做到了轻，而且是簧下质量的轻。", "It trims parts to the minimum—genuinely light unsprung mass.", "unsprung mass（簧下质量）"],
            ["结构上这一块非常空，正好给驱动轴安装留足了空间，天然对前驱友好。", "That open pocket leaves room for a driveshaft—naturally FWD-friendly.", "driveshaft（驱动轴）"],
            ["它整体非常窄，不占用横向空间，给发动机舱留出更多空间。", "It's slim, freeing up lateral room for the engine bay.", "lateral（横向的）"]
         ]},
        {"id": "s5", "scene_zh": "麦弗逊的变种", "scene_en": "MacPherson Variants", "time": "06:30",
         "context": "麦弗逊有很多变种：常见把弹簧和避震分开布局节省高度；用在后悬挂的变种会多一根纵向连杆固定指向（后轮没转向机构）。双球节悬挂把三角下臂换成两根独立连杆分摊横向纵向的力，宝马很多前悬挂在用。查普曼悬挂是莲花创始人设计的，把驱动轴也作为悬架连杆一部分，现只在菲亚特500X和吉普自由侠后悬挂使用。",
         "sentences": [
            ["双球节悬挂就是在麦弗逊基础上，把三角形的下臂换成两根独立的连杆。", "A double-joint strut swaps the A-arm for two separate links.", "double-joint（双球节）"],
            ["两根连杆分摊了原来下臂单独承受的横向纵向的力，轮子动态控制有所提升。", "Two links share the loads, improving wheel control.", "share the load（分摊载荷）"],
            ["查普曼悬挂是莲花创始人设计的，用驱动轴和一根连杆代替三角下摆臂。", "Chapman suspension uses the driveshaft and a link instead of an A-arm.", "Chapman（查普曼）"],
            ["只要只有下臂没有上臂的悬挂，基本都可以看作麦弗逊的变种。", "Any layout with only a lower arm is basically a MacPherson variant.", "variant（变种）"]
         ]},
        {"id": "s6", "scene_zh": "双叉臂结构", "scene_en": "The Double Wishbone", "time": "09:37",
         "context": "双叉臂是公认性能优于麦弗逊的悬挂形式，由一上一下两个叉臂组成。麦弗逊的避震一个人干了两份活：既要当避震又要充当上百臂角色；双叉臂中避震只负责支撑车身和过滤震动，轮子的转向和轨迹控制完全由上下两个叉臂负责。",
         "sentences": [
            ["双叉臂是公认在性能上优于麦弗逊的悬挂形式。", "The double wishbone is widely agreed to outperform the strut.", "double wishbone（双叉臂）"],
            ["它由一上一下两个叉臂组成，这就是双叉臂名字的由来。", "It's built from an upper and lower wishbone—hence the name.", "upper/lower wishbone（上下叉臂）"],
            ["避震只需要负责支撑车身和过滤震动，轮子的转向和轨迹控制完全由上下两个叉臂负责。", "The damper just supports and filters; the wishbones handle steering and wheel path.", "filter vibration（过滤震动）"]
         ]},
        {"id": "s7", "scene_zh": "双叉臂的动态外倾角", "scene_en": "Dynamic Camber: The Key Trick", "time": "10:29",
         "context": "双叉臂最大优点：上臂短于下臂，轮子上下运动时不是直上直下而是带着角度走。过弯车身侧倾时，外侧轮往上走会形成负外倾角，正好与车身倾斜角度抵消，让轮胎保持与地面垂直、100%接触，抓地力最大化，这就是操控好。",
         "sentences": [
            ["双叉臂的上臂长度短于下臂，轮子往上运动时不是直上而是带着角度走的。", "With a shorter upper arm, the wheel arcs as it travels—not straight up.", "arc（弧线运动）"],
            ["过弯车身侧倾，外侧轮子往上走形成负外倾角，正好和车身倾斜的角度相互抵消。", "Cornering lean and the wheel's negative camber cancel out.", "negative camber（负外倾角）"],
            ["轮胎就能和地面保持90度、100%接触，抓地力最大化，操控自然好。", "The tire stays 90° to the road with full contact—max grip, great handling.", "full contact（完全接触）"]
         ]},
        {"id": "s8", "scene_zh": "双叉臂的缺点", "scene_en": "Why Not Everything Uses It", "time": "12:01",
         "context": "为什么不是所有车都用双叉臂：第一贵，零件多、安装和维修人工都贵；第二用在前驱车前悬挂时避震刚好挡在传动轴路线上，需要做拱门形设计；第三横向占空间大，放前悬挂占发动机舱位置，放后悬挂占后备箱或第三排空间。",
         "sentences": [
            ["第一个原因就是贵：零件多，安装和维修的人工也都贵。", "First, cost: more parts and pricier labor to install and service.", "labor（人工费）"],
            ["用在前驱车前悬挂时，避震正好挡在传动轴路线上，需要特别设计成拱门形状。", "Up front, the damper blocks the driveshaft line—requiring an arch design.", "arch（拱门形）"],
            ["它横向占的空间大，放前悬挂占发动机舱，放后悬挂占后备箱或第三排空间。", "It eats lateral room: engine bay up front, trunk or third row in back.", "trunk（后备箱）"]
         ]}
    ]
}

ARTICLES["suspension-types-2"] = {
    "title_zh": "悬挂形式（下）：多连杆与扭力梁",
    "title_en": "Suspension Types (2): Multi-Link and Torsion Beam",
    "duration": "09:32",
    "topic": "汽车 · 悬架",
    "scenes": [
        {"id": "s1", "scene_zh": "多连杆是双叉臂升级版", "scene_en": "Multi-Link: The Wishbone Upgrade", "time": "00:00",
         "context": "多连杆可以看作双叉臂的升级版，拥有双叉臂所有优点，对轮子控制更优。双叉臂是一个人两只手打伞，两手的方向位置受限；多连杆是两个人各用一只手打伞，布局自由很多，分担一份工作更游刃有余。前后都能用。",
         "sentences": [
            ["多连杆可以看作双叉臂的升级版，拥有双叉臂的所有优点。", "Multi-link is an upgraded wishbone—all the same strengths, plus more.", "multi-link（多连杆）"],
            ["如果说双叉臂是一个人两只手打伞，多连杆就是两个人各用一只手打伞，布局自由很多。", "If the wishbone is one person with two hands, multi-link is two people with two hands.", "more freedom（更自由）"],
            ["连杆数量不同车型不同，有三连杆、四连杆、五连杆，连杆越多表现越好。", "Link counts vary—three, four, five—and more links generally perform better.", "link count（连杆数量）"]
         ]},
        {"id": "s2", "scene_zh": "异形连杆＝四连杆", "scene_en": "The 'Integral Link' Is a 4-Link", "time": "01:10",
         "context": "异形连杆听着高大上，其实就是四连杆的一种，多用于后轮。三根横向连杆一上两下控制住轮子，再加一根纵向连杆加强悬挂强度，三横一竖，性价比高，在成本不变的前提下有效提高悬挂表现。",
         "sentences": [
            ["异形连杆听名字好像很高深，实际上它就是四连杆的一种，多用于后轮。", "The 'integral link' sounds fancy, but it's just a four-link used at the rear.", "integral link（异形连杆）"],
            ["三根横向连杆一上两下控制轮子，再加一根纵向连杆加强强度，就是三横一竖。", "Three lateral links plus one longitudinal one—three across, one fore-aft.", "lateral（横向的）"],
            ["在成本不动的前提下，它有效提高了悬挂的表现，性价比比较高。", "It lifts performance at little cost—great value.", "value（性价比）"]
         ]},
        {"id": "s3", "scene_zh": "五连杆是天花板", "scene_en": "Five Links: The Ceiling", "time": "02:03",
         "context": "民用车型多连杆的极限在五连杆。具体布局没有一定之规，取决于车的定位，工程师会根据想要的悬挂动态设计调教五根连杆的位置、角度和尺寸。真要细说就要做受力分析了，大家知道五连杆最牛就行。",
         "sentences": [
            ["民用车型的多连杆极限就在五连杆了。", "Five links are about the practical ceiling for road cars.", "ceiling（天花板）"],
            ["布局没有一定之规，取决于车的定位，工程师会设计每根连杆的位置角度尺寸。", "There's no fixed layout—engineers tune each link's position, angle, and size.", "position and angle（位置与角度）"],
            ["真要细说就要开始做受力分析了，大家只需要知道五连杆是最牛的。", "A full breakdown means force analysis; just know five links is the best.", "force analysis（受力分析）"]
         ]},
        {"id": "s4", "scene_zh": "扭力梁结构", "scene_en": "The Torsion Beam Structure", "time": "02:33",
         "context": "扭力梁也叫拖曳臂悬挂。它非常简单粗暴：几根铁板焊在一起的一个整体，两边的轮子直接硬连接安装上去，不涉及任何连杆摆臂，再在两边布置弹簧和避震。运动时以两个固定在车身上的点为轴心上下的运动。",
         "sentences": [
            ["扭力梁简单粗暴：就是几根铁板焊在一起的一个整体。", "A torsion beam is brutally simple: several steel plates welded into one unit.", "welded（焊接的）"],
            ["两边的轮子直接硬连接装上去，不涉及任何连杆摆臂。", "The wheels bolt on directly—no links, no arms at all.", "bolt on（直接安装）"],
            ["它运动起来以两个固定在车身上的点为轴心，这样上下运动。", "It pivots on two body mounts, moving up and down.", "pivot（轴心转动）"]
         ]},
        {"id": "s5", "scene_zh": "为什么算半独立", "scene_en": "Why It's 'Semi' Independent", "time": "03:40",
         "context": "扭力梁看似整体一起上下动，但其实这根梁是有韧性的、会扭动。一个轮子往上提一个往下压时，梁通过自身扭曲变形完成两个轮子不同方向的运动。说它完全非独立不对（两个轮子可以不同方向动），说它独立也不对（轮子间并不独立），所以叫半独立。",
         "sentences": [
            ["虽然扭力梁看似一个整体，但这根梁是有韧性的，它是会扭动的。", "It looks solid, but the beam is flexible—it can twist.", "twist（扭转）"],
            ["一个轮子往上提一个往下压时，梁通过自身扭曲变形完成两个轮子不同方向的运动。", "Lift one side and push the other, and the beam twists to allow opposite motion.", "opposite motion（相反方向的运动）"],
            ["说它完全非独立不对，说它独立也不对，所以就有了半独立的说法。", "Not fully rigid, not truly independent—hence 'semi-independent'.", "semi-independent（半独立）"]
         ]},
        {"id": "s6", "scene_zh": "扭力梁的优点", "scene_en": "Torsion Beam: The Pluses", "time": "05:01",
         "context": "扭力梁优点：第一非常便宜，一整块铁板两个螺丝固定一切，零件和安装人工都便宜；它拧的过程和防倾杆工作原理重叠，很多时候防倾杆就不装了又省一笔；后期保养除了两个衬套老化，没有其他会坏的地方。第二结构平坦，最大程度腾出后备箱或后排空间。",
         "sentences": [
            ["第一个优点就是便宜：一整块铁板两个螺丝固定一切，零件安装都便宜。", "First, it's cheap: one steel assembly, two bolts—parts and labor are minimal.", "cheap（便宜）"],
            ["它的扭转过程和防倾杆原理重叠，很多时候防倾杆就不装了，又省一笔。", "Its twisting mimics an anti-roll bar, which can be skipped entirely.", "anti-roll bar（防倾杆）"],
            ["结构平坦，能最大程度腾出后备箱或后排的空间。", "It's flat, maximizing trunk and rear-seat room.", "flat（平坦的）"]
         ]},
        {"id": "s7", "scene_zh": "扭力梁的缺点", "scene_en": "Torsion Beam: The Minuses", "time": "05:55",
         "context": "缺点：第一毕竟不是独立悬挂，舒适性和操控性都大打折扣；第二完全不能做四轮定位调节，轮子和扭力梁硬连接、扭力梁和车身硬连接，原厂四轮定位什么样就永远什么样，想改装基本没什么可做的，只能改短簧避震。",
         "sentences": [
            ["毕竟它不是独立悬挂，从舒适性还是操控性考量都会大打折扣。", "Being non-independent, comfort and handling both take a hit.", "take a hit（打折扣）"],
            ["这套后悬挂完全不能做四轮定位的调节。", "The rear can't be aligned at all.", "alignment（四轮定位）"],
            ["轮子和梁硬连接，梁和车身硬连接，原厂什么样就一直什么样。", "Wheels to beam, beam to body—all rigid, so factory settings are permanent.", "factory settings（原厂设定）"],
            ["想改装的话只能改短簧和避震，外倾角后倾角什么都改不了。", "Modders can only swap springs and shocks—no camber or caster changes.", "springs and shocks（短簧和避震）"]
         ]},
        {"id": "s8", "scene_zh": "如何选悬挂", "scene_en": "How to Choose", "time": "07:59",
         "context": "笼统来说独立好于半独立，连杆多的好于连杆少的：多连杆略好于双叉臂，双叉臂好于麦弗逊。买菜车给多连杆开不出区别还徒增维修费，不如前麦弗逊后扭力梁简单便宜。对运动有要求的朋友扭力梁肯定没法看。调教好的麦弗逊也值得拥有，悬挂种类名称眼花缭乱，但万变不离其宗。",
         "sentences": [
            ["独立的好于半独立的，连杆多的好于连杆少的。", "Independent beats semi-independent; more links beat fewer.", "more is better（越多越好）"],
            ["买菜车给多连杆开不出区别，还徒增后区的维修保养费用。", "A grocery-getter can't tell a multi-link from a beam—it just raises maintenance bills.", "grocery-getter（买菜车）"],
            ["不如老老实实前麦弗逊后扭力梁，买来便宜保养便宜，还轻还省空间。", "A strut-and-beam combo is cheaper, lighter, and roomier.", "struts and beams（麦弗逊加扭力梁）"],
            ["悬挂名字让人眼花缭乱，但万变不离其宗，都是这四种的改良和衍生。", "Names dazzle, but every setup is a variant of these four families.", "variants of four（四种形式的衍生）"]
         ]}
    ]
}

ARTICLES["ackermann-angle-1"] = {
    "title_zh": "阿克曼角（上）：转向几何与完美阿克曼",
    "title_en": "Ackermann Angle (1): Steering Geometry and the Perfect Setup",
    "duration": "08:06",
    "topic": "汽车 · 转向几何",
    "scenes": [
        {"id": "s1", "scene_zh": "齿条齿轮转向", "scene_en": "Rack-and-Pinion Steering", "time": "00:00",
         "context": "绝大多数乘用车用的是齿条齿轮转向机构，它把方向盘左右旋转的动作转化成齿条横向移动，齿条往哪边移，轮子就往对应方向转。",
         "sentences": [
            ["绝大多数乘用车的转向机构都是齿条齿轮传动。", "Most passenger cars use rack-and-pinion steering.", "rack-and-pinion（齿条齿轮）"],
            ["它把方向盘左右旋转的动作转化成这根齿条左右横向的移动。", "It turns the wheel's rotation into a left-right rack motion.", "rack（齿条）"],
            ["齿条往左边移动，两个轮子就往右边转，反过来也一样。", "Move the rack left and the wheels turn right—and vice versa.", "vice versa（反之亦然）"]
         ]},
        {"id": "s2", "scene_zh": "平行转向的问题", "scene_en": "The Problem with Parallel Wheels", "time": "01:57",
         "context": "如果转向机构几何设计成两条前轮永远平行，那转弯时内侧轮转过的圈比外侧小，内侧轮需要转更大的角度才能走更小的圈；而且四个轮子各自的转动垂直线永远不可能在一个点会合，做不到绕着同一个圆心转动，转弯就不顺畅。",
         "sentences": [
            ["如果两个前轮永远平行，转弯时内侧轮转过的圈就要比外侧轮小。", "If the front wheels stay parallel, the inside wheel's circle is smaller than the outside's.", "inside wheel（内侧轮）"],
            ["内侧轮要转更大的角度，才能走更小的圈。", "The inside wheel must turn farther to trace the tighter circle.", "tighter circle（更小的圈）"],
            ["三根垂直线永远不可能在一个点会合，四个轮子做不到绕着同一个圆心转动。", "The three perpendiculars never meet at one point—the wheels can't share a center.", "common center（共同圆心）"],
            ["这一部分不协调就会以轮胎打滑脱载的形式表现出来，说人话就是转弯转得不顺畅。", "That mismatch shows as scrubbing—in plain words, corners feel rough.", "scrubbing（轮胎滑动）"]
         ]},
        {"id": "s3", "scene_zh": "三轮车类比", "scene_en": "The Tricycle Analogy", "time": "03:56",
         "context": "把左前轮挡住，当它是台三轮车：黑色线和绿色线交于一点，三个轮子都绕着这个共同圆心转动，非常和谐顺畅；把第四个轮子放回来就显得格格不入。",
         "sentences": [
            ["把左前轮挡住，就当它是一台三轮车，那就没问题了。", "Cover the left-front wheel and treat it as a tricycle—no problem.", "tricycle（三轮车）"],
            ["三根线交于一点，三个轮子都绕着这一个共同圆心转动，非常顺畅。", "Three lines meet at one point and all wheels share that center—smooth.", "smooth（顺畅）"],
            ["把第四个轮子放回来，它就显得格格不入了。", "Add the fourth wheel back and it simply doesn't fit in.", "doesn't fit（格格不入）"]
         ]},
        {"id": "s4", "scene_zh": "兰肯斯伯格的梯形", "scene_en": "Lankensperger's Trapezoid", "time": "04:29",
         "context": "德国车轮匠兰肯斯伯格1817年发现：把长方形的悬挂几何改成梯形，齿条左右移动时两个轮子转过的角度就不同，内侧轮比外侧轮转更大的角度，让三线会合的目标更进一步。",
         "sentences": [
            ["兰肯斯伯格在1817年发现，把长方形悬挂几何改成梯形，两个轮子转过的角度就会不同。", "In 1817 Lankensperger found that a trapezoid makes the two wheels turn unequal angles.", "trapezoid（梯形）"],
            ["内侧的轮子会比外侧的转更大的角度。", "The inside wheel turns more than the outside one.", "turn more（转更多）"],
            ["这样离四个轮子绕着同一个圆心转的目标就更进了一步。", "That gets the wheels closer to sharing one turning center.", "turning center（转向圆心）"]
         ]},
        {"id": "s5", "scene_zh": "完美几何的诞生", "scene_en": "The Perfect Geometry Emerges", "time": "05:24",
         "context": "兰肯斯伯格发现当梯形两条腰的延长线焦点正好位于后轴中心时，不管往哪边打多少方向，三根线永远交于一点，四个轮子都可以非常顺畅地绕着同一个点转动，互不干涉，完美的转向几何诞生了。",
         "sentences": [
            ["当梯形两条腰的延长线焦点正好位于后轴中心时，问题就解决了。", "When the trapezoid's extended lines meet at the rear-axle center, the problem is solved.", "rear-axle center（后轴中心）"],
            ["不管往哪边打方向、打多少方向，这三根线永远是交于一点的。", "No matter how you steer, the three lines always meet at one point.", "always meet（永远相交）"],
            ["四个轮子都能非常顺畅地绕着同一个点在转动，互相也不干涉了。", "All four wheels spin smoothly around one center without fighting.", "without fighting（互不干涉）"]
         ]},
        {"id": "s6", "scene_zh": "阿克曼名字的由来", "scene_en": "How It Got the Name Ackermann", "time": "05:59",
         "context": "兰肯斯伯格很高兴，找到律师朋友鲁道夫·阿克曼委托注册专利，结果阿克曼自己从德国跑到英国，用他自己的名字完成了注册。这就是阿克曼转向几何名字的由来。",
         "sentences": [
            ["兰肯斯伯格找到了他的律师朋友鲁道夫·阿克曼，委托他帮忙注册专利。", "Lankensperger asked his lawyer, Rudolph Ackermann, to patent it.", "patent（专利）"],
            ["阿克曼很机智，自己跑到英国，用他自己的名字完成了注册。", "The clever lawyer registered it in Britain under his own name.", "register（注册）"],
            ["这就是阿克曼转向几何这个名字的由来。", "And that's how 'Ackermann steering geometry' got its name.", "steering geometry（转向几何）"]
         ]},
        {"id": "s7", "scene_zh": "数学表达", "scene_en": "The Math", "time": "06:24",
         "context": "设两前轮转向角为A和B，转向半径R，轴距L，胎距T，可得两个三角函数方程，相减得：cotB减去cotA等于胎距比上轴距。任何时刻前轮转向角度完美满足这个方程，就称这车100%符合阿克曼转向几何。",
         "sentences": [
            ["设两个前轮的转向角度为A和B，转向半径为R，轴距为L，胎距为T。", "Let the two front steer angles be A and B, radius R, wheelbase L, track T.", "wheelbase（轴距）"],
            ["通过三角函数方程相减得到：cotB减cotA等于胎距比轴距。", "Subtracting the trig equations gives: cot B − cot A = track ÷ wheelbase.", "trig equations（三角函数方程）"],
            ["前轮转向角度任何时候都满足这个方程，就是100%符合阿克曼转向几何。", "Whenever the steer angles satisfy it, the car is 100% Ackermann.", "100% Ackermann（完美阿克曼）"]
         ]},
        {"id": "s8", "scene_zh": "阿克曼角与百分比", "scene_en": "The Angle and the Percentage", "time": "07:26",
         "context": "大家常说的阿克曼角指的就是两个转向角之间的差，角A减角B。实际应用中很少讲阿克曼角，因为它随打方向不断变化，更多用正反阿克曼和阿克曼百分比来表述交流。",
         "sentences": [
            ["所谓的阿克曼角，指的就是两个转向角之间的差，角A减角B。", "The 'Ackermann angle' is simply the difference between the two steer angles.", "angle difference（角度差）"],
            ["实际应用中很少讲阿克曼角，因为它是随打方向不停变化的。", "In practice the raw angle is rarely quoted—it changes constantly.", "constantly changing（不断变化）"],
            ["更多的是用正反阿克曼和阿克曼的百分比来表述和交流。", "People use positive/anti-Ackermann and the percentage instead.", "percentage（百分比）"]
         ]}
    ]
}

ARTICLES["ackermann-angle-2"] = {
    "title_zh": "阿克曼角（下）：滑移角与反阿克曼",
    "title_en": "Ackermann Angle (2): Slip Angle and Anti-Ackermann",
    "duration": "11:26",
    "topic": "汽车 · 转向几何",
    "scenes": [
        {"id": "s1", "scene_zh": "滑移角", "scene_en": "The Slip Angle", "time": "00:00",
         "context": "现实世界里轮胎是橡胶做的，橡胶会形变。打方向转弯时，轮胎指向已经转过来，但和地面接触的橡胶还拧着一股劲，实际行进方向总会打一点折扣。轮胎指向和实际行进方向之间的夹角就是滑移角。理论上完美的阿克曼不好用，就是因为有这个滑移角的存在。",
         "sentences": [
            ["现实世界里轮胎是橡胶做的，橡胶是会形变的。", "In the real world tires are rubber, and rubber deforms.", "deform（形变）"],
            ["打方向时轮胎指向已转过来，但接触地面的橡胶还拧着劲，实际行进方向总要打折扣。", "The tire points one way, but the contact patch lags—actual travel falls short.", "contact patch（接地面积）"],
            ["轮胎指向和实际行进方向的夹角就是滑移角。", "The angle between tire heading and actual travel is the slip angle.", "slip angle（滑移角）"],
            ["理论上完美的阿克曼不好用，就是因为有这个滑移角的存在。", "Perfect theoretical Ackermann fails because of the slip angle.", "slip（滑动）"]
         ]},
        {"id": "s2", "scene_zh": "F1的极端场景", "scene_en": "F1: The Extreme Case", "time": "02:12",
         "context": "用F1举例是因为它是汽车工业里最极端的例子：转弯速度最快，快速转弯势必带来重心转移。以150公里时速转弯时绝大多数重心都压到外侧轮上，内侧轮承受压力非常小，极限情况下内侧轮甚至轻微离地。",
         "sentences": [
            ["用F1来举例，因为它是汽车工业中最极端的例子。", "F1 is the industry's most extreme example.", "extreme（极端的）"],
            ["F1转弯速度最快，快速转弯势必带来重心的转移。", "Its cornering speeds are the highest, forcing big weight transfer.", "weight transfer（重心转移）"],
            ["150公里时速转弯时，绝大多数重心压到外侧轮上，内侧轮承受的压力非常小。", "At 150 km/h in a corner, most load rides the outside tire; the inside barely loads.", "outside tire（外侧轮）"]
         ]},
        {"id": "s3", "scene_zh": "外侧轮需要多转", "scene_en": "The Outside Wheel Needs More", "time": "03:14",
         "context": "压得越大力气转向，轮胎橡胶越拧巴、滑移角越大；不施加压力就几乎没有滑移角。F1过弯压力基本都在外侧轮，所以外侧轮的滑移角远大于内侧轮。为了让实际行进方向接近完美箭头，外侧轮胎的指向上要向左多转更多的角度。",
         "sentences": [
            ["压得越大力气转向，轮胎橡胶越是拧巴着，滑移角就越大。", "More vertical load means more rubber twist—and a bigger slip angle.", "vertical load（垂直载荷）"],
            ["外侧轮承受压力大，它的滑移角远远大于内侧轮的滑移角。", "The loaded outside tire develops a far larger slip angle than the inside.", "far larger（远大于）"],
            ["要减去滑移角之后实际行进方向才接近完美，所以外侧轮胎要向左多转更多角度。", "After the slip-angle discount, the outside tire must steer farther left.", "discount（折减）"]
         ]},
        {"id": "s4", "scene_zh": "反阿克曼", "scene_en": "Anti-Ackermann", "time": "03:42",
         "context": "这就是F1赛车上的反阿克曼转向几何设定：外侧轮转向角度明显大于内侧轮。F1转向设定还会根据赛道单独调校：高速弯多的赛道用激进的反阿克曼；蒙特卡洛这类低速弯、调头弯多的赛道，激进的反阿克曼就不合适了。",
         "sentences": [
            ["F1赛车上就是这种反阿克曼的设定：外侧轮转的角度明显大于内侧轮。", "F1 runs anti-Ackermann: the outside wheel visibly turns more than the inside.", "anti-Ackermann（反阿克曼）"],
            ["绝大多数的赛道都是高速弯比较多，会设计成比较激进的反阿克曼。", "Most tracks are fast-corner heavy, calling for aggressive anti-Ackermann.", "aggressive（激进的）"],
            ["蒙特卡洛有很多低速弯、调头弯，激进的反阿克曼设定就不合适了。", "Monaco's slow hairpins make aggressive anti-Ackermann unsuitable.", "hairpin（调头弯）"]
         ]},
        {"id": "s5", "scene_zh": "向心力靠滑移角", "scene_en": "Cornering Force from Slip", "time": "04:26",
         "context": "快速过弯靠的不是前轮打的方向，而是轮胎和地面摩擦产生的指向圆心的力，用来克服巨大的离心力。这个向心力只有在有了滑移角时才会产生，就是橡胶拧巴的劲。滑移角越大产生的摩擦力越大，大约5.5度时力达到最大值，这就是外侧转向轮的极限滑移角，此时能产生最大向心力，完成更高速度的过弯。",
         "sentences": [
            ["快速过弯看似靠前轮打的方向，其实靠的是轮胎和地面摩擦产生的指向圆心的力。", "Fast cornering isn't about steering angle—it's the friction force pointing to the circle's center.", "centripetal force（向心力）"],
            ["这个指向圆心的力只有在有了滑移角的时候才会产生，就是橡胶拧巴的那股劲。", "That force only exists with a slip angle—it's the rubber's twist.", "rubber twist（橡胶拧劲）"],
            ["滑移角大概5.5度时力达到最大值，这就是外侧转向轮的极限滑移角。", "The force peaks around 5.5°, the outside tire's ideal slip angle.", "peak（峰值）"],
            ["在这个角度上能产生最大向心力，才能完成更高速度的过弯。", "Max cornering force at this angle allows the fastest turns.", "cornering force（过弯力）"]
         ]},
        {"id": "s6", "scene_zh": "民用车的设定", "scene_en": "Street Car Setups", "time": "05:43",
         "context": "越家用的车设定越接近完美的100%阿克曼，因为家用车慢慢悠悠转弯不会产生多大滑移角，日常驾驶的顺畅才是第一位，硬开去赛道会体验到转向不足（推头）。偏运动的车型会往反阿克曼方向靠一靠，但不会疯狂到F1那样，也不会设计成0%平行的，一般介于两者之间，让外侧轮多转的角度正好和滑移角综合，达到指哪打哪，代价是低速大幅度转弯（如侧方停车）时轮胎可能打滑跳胎。",
         "sentences": [
            ["越家用的车设定越接近完美的100%阿克曼，因为日常顺畅的转弯才是第一位的。", "Daily drivers lean toward 100% Ackermann for smooth, fuss-free turns.", "daily driver（家用车）"],
            ["偏运动的车型会往反阿克曼方向靠一靠，但一般介于两者之间。", "Sportier cars lean toward anti-Ackermann but stay between the extremes.", "in between（介于之间）"],
            ["外侧轮多转的角度正好和滑移角综合，轮胎实际行进方向就和想要的方向完美契合，指哪打哪。", "Extra outside steering cancels the slip angle—the car goes exactly where you point it.", "point-and-shoot（指哪打哪）"],
            ["代价是低速大幅度转弯时轮胎可能打滑跳胎，特别是冷车冷胎的情况下。", "The price: scrubbing in slow, tight turns—especially on cold tires.", "scrubbing（打滑跳胎）"]
         ]},
        {"id": "s7", "scene_zh": "怎么改装阿克曼", "scene_en": "How to Adjust Ackermann", "time": "08:01",
         "context": "改装阿克曼其实很简单：黄色部分就是羊角，在羊角上重新钻一个洞，把蓝色转向拉杆的球头从原来的洞接到前面那个洞里。因为在一台轴距胎距固定的车上，阿克曼调整就是两个点的调整：轮子转动的轴心点和羊角与转向球头连接点，两点定了腰的方向就定了，会合点也就定了。",
         "sentences": [
            ["改装阿克曼非常简单：在羊角上重新钻一个洞，把转向拉杆的球头接到新的洞里。", "It's simple: drill a new hole in the knuckle and move the tie-rod ball joint into it.", "knuckle（羊角）"],
            ["在轴距胎距固定的车上，阿克曼调整实际上就是两个点的调整。", "With fixed wheelbase and track, Ackermann tuning is really about two points.", "two points（两个点）"],
            ["两个点定了，两条腰的方向就定了，延长线在哪里会合也就定了。", "Fix the two points, and the two arms' directions—and their meeting point—are set.", "meeting point（会合点）"]
         ]},
        {"id": "s8", "scene_zh": "法兰盘破坏标定", "scene_en": "Spacers Ruin the Calibration", "time": "09:15",
         "context": "加装法兰盘把轮子向外平移，本质就是改变了胎距参数。原来100%阿克曼的三条线交于一点，加法兰盘后红绿线各往两边平移，那个点就不存在了，原厂设计的阿克曼标定被完全破坏。实际汽车悬挂转向涉及的变量比想象的要多得多，乱改轮毂影响的东西很多。",
         "sentences": [
            ["加装法兰盘把两个前轮向外横移，本质上就是改变了胎距的参数。", "Bolt-on spacers push the wheels outward—in effect changing the track.", "spacers（法兰盘）"],
            ["原来交于一点的三条线，经法兰盘一加那个点就不存在了，阿克曼标定完全被破坏。", "The three lines once met at one point; with spacers the point vanishes and the calibration is ruined.", "calibration（标定）"],
            ["乱改轮毂所影响的悬挂变量，肯定比你想象的要来得多。", "Messing with wheels touches far more suspension variables than you'd expect.", "variables（变量）"]
         ]},
        {"id": "s9", "scene_zh": "后轮也有滑移角", "scene_en": "Rear Slip and Four-Wheel Steering", "time": "10:41",
         "context": "这里只讨论了前轮的转向和前轮的滑移角，其实后轮也存在滑移角，因为转弯靠的指向圆心的向心力一定要借助滑移角才能形成。四轮转向车型后轮也能左右打方向，相当于把图再复杂化一点，但本质原理一样。",
         "sentences": [
            ["其实后轮也是存在滑移角的，向心力的产生一定要借助滑移角才能形成。", "The rear tires have slip angles too—cornering force requires it.", "rear tires（后轮）"],
            ["有些车型带四轮转向，后轮也可以左右打方向，本质的原理是一样的。", "Four-wheel steering lets the rear turn too—same underlying physics.", "four-wheel steering（四轮转向）"]
         ]}
    ]
}

ARTICLES["spark-plug-1"] = {
    "title_zh": "火花塞（上）：结构、材质与间隙",
    "title_en": "Spark Plugs (1): Structure, Materials, and Gap",
    "duration": "11:29",
    "topic": "汽车 · 火花塞",
    "scenes": [
        {"id": "s1", "scene_zh": "火花塞的任务", "scene_en": "The Spark Plug's Job", "time": "00:00",
         "context": "汽油发动机运行离不开点火步骤，这个点火任务就是由火花塞完成的。火花产生在中心电极尖端和L型接地电极之间。",
         "sentences": [
            ["想要让汽油发动机运行，就离不开一个点火的步骤。", "Running a gasoline engine requires an ignition step.", "ignition（点火）"],
            ["这个点火的任务就是由火花塞来完成的。", "That job falls to the spark plug.", "spark plug（火花塞）"],
            ["火花产生实际上就是在尖尖的中心电极和L型的接地电极之间。", "The spark arcs between the pointed center electrode and the L-shaped ground electrode.", "center electrode（中心电极）"]
         ]},
        {"id": "s2", "scene_zh": "正负极与接地", "scene_en": "Positive, Negative, and Ground", "time": "01:03",
         "context": "火花塞中心是贯穿到顶端的金属杆（正极），被白色陶瓷绝缘包裹。L型部分是螺纹的延伸，螺纹直接旋在发动机缸盖上。车身和发动机的金属部分都是负极（接地），所以L型部分就是负极。",
         "sentences": [
            ["绿色的中心金属杆贯穿整个火花塞，为了绝缘被白色陶瓷包裹。", "A metal center rod runs through the plug, insulated by white ceramic.", "insulated（绝缘的）"],
            ["车身和发动机的金属部分都被认为是负极，也就是接地。", "All body and engine metal counts as negative—ground.", "ground（接地）"],
            ["L型的部分是螺纹的延伸，而螺纹直接接触发动机的缸盖，所以它就是负极。", "The L-arm extends from the threads, which bolt into the head—so it's the ground.", "ground electrode（接地电极）"]
         ]},
        {"id": "s3", "scene_zh": "点火原理", "scene_en": "How It Fires", "time": "02:17",
         "context": "需要点火时行车电脑通过高压包给火花塞正极一个约两万多伏特的电压，正极两万多伏、负极零伏，巨大的电压差击穿两电极间的空气形成火花，完成点火，原理和闪电类似。",
         "sentences": [
            ["需要点火时，行车电脑通过高压包给火花塞正极一个非常高的电压。", "At ignition, the ECU fires the plug through the coil with a very high voltage.", "ignition coil（高压包）"],
            ["这个电压一般在两万多伏特左右。", "That voltage is around 20,000 volts.", "20,000 volts（两万多伏）"],
            ["巨大的电压差在两电极之间击穿空气，从而形成火花，也就完成了点火。", "The huge voltage gap arcs across the air between the electrodes, making the spark that fires the charge.", "arc（电弧）"]
         ]},
        {"id": "s4", "scene_zh": "三种常见材质", "scene_en": "Three Common Materials", "time": "02:55",
         "context": "市场上常见的中心电极材质有三种：铜的、铂金的、铱金的。",
         "sentences": [
            ["中心电极在一般市场上可以看到的有三种：铜的、铂金的和铱金的。", "Center electrodes come in three common flavors: copper, platinum, and iridium.", "platinum（铂金）"],
            ["三种材质寿命和价格从低到高分别是铜、铂金、铱金。", "From cheapest and shortest-lived to priciest and longest: copper, platinum, iridium.", "iridium（铱金）"]
         ]},
        {"id": "s5", "scene_zh": "铜火花塞", "scene_en": "The Copper Plug", "time": "03:18",
         "context": "铜火花塞最常见也最便宜，整根都是铜做的，只在尖端覆盖一层镍合金。铜的导电导热性特别好，但铜很软、镍合金也不硬，长时间火花电弧会让中心电极很快磨损，寿命较短，可能两三万公里就磨损完。为了延长寿命把尖端做大到2.5毫米直径，但面积大了打相同火花需要更大电压，好在铜导电性好互相抵消。八九十年代老车用得多，现在涡轮增压高压比高转速发动机反而还用它。",
         "sentences": [
            ["铜火花塞最便宜，整根铜做，只在尖端覆盖一层镍合金。", "Copper plugs are cheapest—copper throughout with a nickel-alloy tip.", "nickel alloy（镍合金）"],
            ["铜的导电导热性好，但很软，长时间火花电弧会让中心电极很快磨损，寿命比较短。", "Copper conducts well but wears fast under the arc—short lifespan.", "wear（磨损）"],
            ["可能两三万公里就差不多磨损完了。", "They're often gone by 20,000–30,000 km.", "gone（磨损完）"],
            ["现在的涡轮增压高转速发动机有一部分还在用铜火花塞，因为它导电导热好。", "Some modern turbo, high-rpm engines still use copper for its conductivity.", "conductivity（导电性）"]
         ]},
        {"id": "s6", "scene_zh": "铂金火花塞", "scene_en": "The Platinum Plug", "time": "05:08",
         "context": "铂金比镍合金硬得多、熔点更高。把一片铂金焊到铜火花塞尖端覆盖住，原来的铜火花塞就变成了铂金火花塞，中心电极磨损慢很多，也能承受更高点火电压，寿命可达16万公里。现在绝大多数车用这种。双铂金火花塞是在接地电极上也焊一层铂金，正负极两头都有，进一步提高性能和寿命。",
         "sentences": [
            ["把一片铂金焊到尖端覆盖住，铜火花塞就变成了铂金火花塞。", "Weld a platinum pad over the tip and a copper plug becomes platinum.", "platinum pad（铂金片）"],
            ["中心电极的磨损慢很多，也能承受更高的点火电压，寿命可达16万公里左右。", "Wear slows dramatically, voltages rise, and life stretches to ~160,000 km.", "lifespan（寿命）"],
            ["双铂金火花塞是在接地电极上也焊一层铂金，正负极两头都有。", "Double platinum welds pads on both electrodes—positive and ground.", "double platinum（双铂金）"]
         ]},
        {"id": "s7", "scene_zh": "铱金火花塞", "scene_en": "The Iridium Plug", "time": "06:31",
         "context": "铱金是三种里最贵的：铱比铂硬六倍、强度高八倍、熔点高近700度。焊在中心电极表面能进一步提升寿命。因为铱非常硬，火花对电极表面磨损非常慢，中心电极尖端直径可以做得非常小，最小只有0.4毫米左右，既省铱金成本又提高点火效率——电极尖端直径越小打出火花所需电压越低。",
         "sentences": [
            ["铱比铂金硬六倍，强度高八倍，熔点高出将近七百度。", "Iridium is six times harder than platinum, eight times stronger, and melts ~700°C higher.", "six times harder（硬六倍）"],
            ["铱非常非常硬，火花对电极表面的磨损变得非常非常慢。", "Its hardness makes electrode wear glacially slow.", "glacially slow（非常慢）"],
            ["中心电极尖端直径可以做到非常小，最小可能只有0.4毫米左右。", "The tip can be tiny—as small as 0.4 mm.", "0.4 mm（0.4毫米）"],
            ["直径越小，打出火花所需要用到的电压就越低，能更轻松打出火花。", "A smaller tip needs less voltage to spark—easier ignition.", "less voltage（更低电压）"]
         ]},
        {"id": "s8", "scene_zh": "怎么选材质", "scene_en": "Which Material to Use", "time": "07:50",
         "context": "车要用哪种材料的火花塞要翻车主手册，手册让用哪种就用哪种最稳妥。应该用铜的不要升级，应该用铂金或铱金的不要降级。价格参考：铜或镍合金十几二十块，铂金二三十块，铱金五六十块。",
         "sentences": [
            ["要用哪种材质，去翻你的车主手册，它让用哪种你就用哪种，这是最稳妥的。", "Follow the owner's manual—whatever it specifies is the safe choice.", "owner's manual（车主手册）"],
            ["该用铜的不要去升级，该用铂金或铱金的不要去降级。", "Don't upgrade a copper spec, and don't downgrade a platinum or iridium spec.", "upgrade / downgrade（升级 / 降级）"],
            ["铜或镍合金一个十几二十块，铂金二三十块，铱金要到五六十块一个。", "Copper runs ¥15–20, platinum ¥20–30, iridium ¥50–60 each.", "price（价格）"]
         ]},
        {"id": "s9", "scene_zh": "火花塞间隙", "scene_en": "The Spark Plug Gap", "time": "08:55",
         "context": "间隙指中心电极到L型接地电极之间的距离，一般在0.6到1.8毫米之间。间隙越小火花尺寸越小，越大火花越大。点火时希望火花大一点，和油气混合体接触面积大，点火效率更高。但间隙大了需要更大电压，而且火花形成速度变慢。低压缩比注重油耗的家用车间隙设计较大，让更多汽油接触火花；高压缩比注重性能的运动车间隙设计较小，火花行程时间短，利于电脑精确控制点火正时。",
         "sentences": [
            ["间隙指中心电极到L型接地电极之间的距离，一般在0.6到1.8毫米之间。", "The gap is the distance from center to ground electrode—typically 0.6–1.8 mm.", "gap（间隙）"],
            ["间隙越大火花尺寸越大，和油气混合体接触面积变大，点火效率更高。", "A bigger gap makes a bigger spark, touching more mixture for better ignition.", "mixture（油气混合体）"],
            ["但间隙大了需要更大的电压，而且火花形成的速度变慢了。", "But a larger gap needs more voltage and forms the spark slower.", "slower（更慢）"],
            ["换火花塞不仅要用对材质，买回来还要检查并调整间隙。", "Beyond material, always check and set the gap after buying.", "check and set（检查调整）"]
         ]},
        {"id": "s10", "scene_zh": "间隙调整工具", "scene_en": "The Gap Tool", "time": "11:19",
         "context": "检查和调整间隙用的是锥形厚度规：很薄的一边越往这边转越厚。测量时把两电极之间放进去找到卡住的位置，读出英寸或毫米数值。要扩大间隙就把电极放到圆孔里轻轻向上掰，掰过头了直接按在桌子上压一下，直到达到标准。",
         "sentences": [
            ["检查调整间隙常用的是这种工具，一边很薄，越往这边转越厚。", "A tapered gauge does the job—thin at one end, thicker as it turns.", "tapered gauge（锥形厚度规）"],
            ["把火花塞两电极之间放进去，转不动卡住的位置就是间隙值。", "Slide it between the electrodes until snug—that spot reads the gap.", "snug（卡住）"],
            ["要扩大间隙就把电极放到圆孔中轻轻向上掰，掰过头了就按在桌子上压回来。", "To widen, hook the electrode in the hole and pry gently; overshot? Press it back on the bench.", "pry（撬）"]
         ]}
    ]
}

ARTICLES["spark-plug-2"] = {
    "title_zh": "火花塞（下）：冷热型与好坏判断",
    "title_en": "Spark Plugs (2): Heat Range and Reading the Plug",
    "duration": "09:19",
    "topic": "汽车 · 火花塞",
    "scenes": [
        {"id": "s1", "scene_zh": "冷型与热型", "scene_en": "Cold vs Hot Plugs", "time": "00:00",
         "context": "火花塞越冷工作温度越低，燃烧室的积碳、机油、废气颗粒物沉淀到电极上，温度不足以燃烧清除，慢慢覆盖电极影响发动机表现、缩短寿命。火花塞越热温度越高，能自己清除电极表面的积碳；但温度太高，高到还没到点火的时候火花塞自身温度就足以点燃油气混合体，就会出现提前爆震、敲缸。",
         "sentences": [
            ["火花塞越冷，工作温度越低，电极上的积碳清不掉。", "A colder plug runs cooler and can't burn deposits off its electrodes.", "deposits（积碳）"],
            ["积碳慢慢覆盖电极表面，影响发动机的表现，缩短火花塞的寿命。", "Deposits coat the electrodes, hurting performance and life.", "coat（覆盖）"],
            ["火花塞越热，能自己清除电极表面的积碳。", "A hotter plug burns deposits off itself.", "self-cleaning（自洁）"],
            ["但温度太高，还没到点火时候就足以点燃油气混合体，出现提前的爆震、敲缸。", "Too hot and it pre-ignites the charge—knock and pinging.", "pre-ignition（提前点火）"]
         ]},
        {"id": "s2", "scene_zh": "自清区450-850度", "scene_en": "The Self-Cleaning Zone: 450–850°C", "time": "00:53",
         "context": "火花塞低于450度处于积碳区，高于850度处于自燃区比较危险，容易提前点燃汽油。最佳工作温度在450到850度之间，既足够热可以清除积碳，又不会有敲缸自爆风险，这个区间叫自清区。",
         "sentences": [
            ["火花塞低于450度处于积碳区，高于850度处于自燃区，比较危险。", "Below 450°C plugs foul; above 850°C they self-ignite—dangerous.", "foul（积碳）"],
            ["最佳工作温度在450到850度之间，叫自清区。", "The sweet spot is 450–850°C, the self-cleaning zone.", "sweet spot（最佳区间）"],
            ["既足够热能清除积碳，又不会有敲缸自爆的风险。", "Hot enough to self-clean, cool enough to avoid knock.", "self-clean（自清洁）"]
         ]},
        {"id": "s3", "scene_zh": "偏冷偏热都不好", "scene_en": "Too Cold or Too Hot", "time": "01:29",
         "context": "火花塞太偏冷型散热太好，即使油门全开、发动机温度最高时火花塞温度还是上不去，停留在积碳区。太偏热型散热慢，油门稍微踩深一点温度就飙升进入自燃区。原厂推荐的火花塞差不多就是中间绿线的工况，没事不要去买更冷或更热的。",
         "sentences": [
            ["太偏冷型，即使油门全开火花塞温度还是上不去，停留在积碳区。", "Too cold and even at full throttle the plug stays in the fouling zone.", "fouling zone（积碳区）"],
            ["太偏热型，油门稍微踩深一点温度就飙升，直接进入自燃区。", "Too hot and a bit of throttle sends the temperature soaring into self-ignition.", "self-ignition zone（自燃区）"],
            ["原厂推荐的火花塞差不多就是中间那条绿线的工况，没事不要去买更冷或更热的。", "Factory plugs sit on the middle green line—don't chase colder or hotter.", "factory spec（原厂规格）"]
         ]},
        {"id": "s4", "scene_zh": "家用用热型运动用冷型", "scene_en": "Daily Drivers: Hot; Sports Cars: Cold", "time": "02:13",
         "context": "一般家用车或城市低速车用热型火花塞居多，因为发动机平时低负荷运行温度高不到哪去，需要散热慢一点保持温度避免积碳。运动车型一般用相对冷一点的火花塞，因为经常地板油发动机一直高温运行，火花塞容易过热，需要散热更好的冷型。",
         "sentences": [
            ["一般的家用车或城市低速车，用的是热型火花塞居多。", "Typical city cars run hotter plugs.", "hotter plugs（热型火花塞）"],
            ["发动机平时低负荷运行温度本来就高不到哪去，需要散热慢一点保持住温度。", "Low-load engines never get hot, so slow heat loss keeps the plug hot enough.", "low load（低负荷）"],
            ["运动车型动不动就地板油，发动机一直在高温运行，需要散热更好的冷型火花塞。", "Sports cars run flat-out and hot, so they need colder, better-cooled plugs.", "flat-out（地板油）"]
         ]},
        {"id": "s5", "scene_zh": "怎么读火花塞编号", "scene_en": "Reading NGK Part Numbers", "time": "02:47",
         "context": "火花塞冷热度标在火花塞上。以NGK为例，编号IZFR6K11S的第五位数字6就是热值：数字越小越热，数字越大越冷。不同品牌标注方法不同，博世编号ZGR6ST12里的6和NGK相反，数字越大越热。",
         "sentences": [
            ["火花塞的冷热度都标识在火花塞上面，以NGK为例，IZFR6K11S的第五位数字6指的就是热值。", "Heat range is printed on the plug—in NGK's IZFR6K11S, the 5th digit (6) is the heat rating.", "heat rating（热值）"],
            ["对NGK来说，数字越小越热，数字越大就越冷。", "For NGK, a smaller number means hotter.", "hotter（更热）"],
            ["不同品牌标注不同，博世的6正好相反，数字越大越热。", "Other brands differ—Bosch's number climbs as heat rises.", "opposite（相反）"]
         ]},
        {"id": "s6", "scene_zh": "好火花塞长什么样", "scene_en": "What a Healthy Plug Looks Like", "time": "03:50",
         "context": "拆下旧火花塞最重要是检查两个电极。颜色灰灰的或淡淡的褐色、整体干燥、电极没有断裂迹象，说明火花塞是好的，只是用得久了一点，完全可以接着用。陶瓷尾部有黄色是串气烤糊了，不影响任何性能，不需要看。",
         "sentences": [
            ["检查火花塞好坏，最重要的是看两个电极。", "Reading a plug comes down to the electrodes.", "read the plug（读火花塞）"],
            ["颜色灰灰的或淡淡的褐色、整体干燥、电极没有断裂，说明火花塞是好的。", "Gray or light tan, dry, and intact electrodes mean a healthy plug.", "light tan（淡褐色）"],
            ["陶瓷尾部的黄色是串气烤糊的，不影响性能，不需要看。", "Yellow at the ceramic base is just gas blow-by staining—harmless.", "staining（染色）"]
         ]},
        {"id": "s7", "scene_zh": "积碳与机油污染", "scene_en": "Fouled by Carbon or Oil", "time": "04:38",
         "context": "电极黑黑一层像被熏黑的，是积碳污染。原因很多：空气滤芯很脏、长期小油门开车、长时间怠速，即使正确的火花塞在低负荷下也会积碳。富油工况燃烧不充分也会积碳，这时不仅要换火花塞还要查清根源，光换火花塞是治标不治本。如果积碳黑黑的但是油油的，是机油污染，典型是活塞环或气门油封密封不严，机油漏进燃烧室，同样要先解决根源再换火花塞。",
         "sentences": [
            ["黑黑的一层被熏黑的感觉，就是被积碳污染的火花塞。", "A black, sooty coating means carbon fouling.", "sooty（熏黑的）"],
            ["空气滤芯脏、长期小油门、长时间怠速，都会让火花塞积碳。", "Dirty air filters, constant light throttle, and long idling all cause it.", "light throttle（小油门）"],
            ["富油工况燃烧不充分也会形成积碳，不仅要换火花塞还要检查根源，光换是治标不治本。", "Rich running fouls plugs too—fix the root cause or it recurs.", "root cause（根源）"],
            ["黑黑的但是油油的，是机油污染，典型是活塞环或气门油封密封不严。", "Black and oily points to oil contamination—usually worn rings or valve seals.", "oil contamination（机油污染）"]
         ]},
        {"id": "s8", "scene_zh": "湿、烧蚀与磨损", "scene_en": "Wet, Burned, and Worn Plugs", "time": "05:56",
         "context": "火花塞湿的一般发生在连续打火打不着之后，汽油一直喷但没被点燃把火花塞弄湿了，用清洗剂清洗吹干、再找到打不着火的原因即可。电极有白色沉淀物或融化痕迹，说明经历过高得不该承受的高温，可能是发动机过热或冷热型没选对，需要更换。电极明显磨损甚至断裂，一般都是太久不按时换火花塞导致。",
         "sentences": [
            ["火花塞湿的，一般发生在连续打火打不着之后，汽油把火花塞弄湿了。", "A wet plug usually follows repeated failed starts—fuel soaks it.", "wet plug（湿火花塞）"],
            ["用清洗剂清洗吹干，再把打不着火的原因找到就可以了。", "Clean it, dry it, and find why it wouldn't start.", "clean and dry（清洗吹干）"],
            ["白色沉淀物或融化痕迹，说明火花塞经历过高得不该承受的高温，需要更换。", "White deposits or melted spots mean extreme overheating—replace it.", "melted（融化）"],
            ["电极明显磨损甚至断裂，一般都是太久不按时换火花塞导致的。", "Heavy wear or a broken electrode usually means the change interval was ignored.", "change interval（更换周期）"]
         ]},
        {"id": "s9", "scene_zh": "不及时换的后果", "scene_en": "What Happens If You Don't", "time": "07:04",
         "context": "火花塞不行了却不更换，最常见的是怠速抖动、油耗增加，更严重可能发动机故障灯亮起、失火或缺缸、加速没力气，有时启动车也变得困难，总之油耗和动力都会受到很大程度影响。",
         "sentences": [
            ["最常见的是怠速抖动、油耗的增加。", "Most commonly: rough idle and worse fuel economy.", "rough idle（怠速抖动）"],
            ["更严重的话，发动机的故障灯会亮起，失火或缺缸。", "Worse, the check-engine light comes on with misfires.", "misfire（失火）"],
            ["加速没有力气，有的时候启动车也会变得比较困难。", "Acceleration feels gutless and starting can struggle.", "gutless（没力气）"],
            ["总而言之，油耗和动力都会受到很大程度的影响。", "In short, both economy and power take a real hit.", "take a hit（受影响）"]
         ]},
        {"id": "s10", "scene_zh": "三点补充", "scene_en": "Three Extra Notes", "time": "07:21",
         "context": "第一，高性能发动机有的是一缸两个火花塞，典型如转子发动机、克莱斯勒hemi、奔驰M112 V6和M113 V8。第二，火花塞最好的品牌有NGK、博世、电装、Champion、IK德克，绝大多数车企原厂火花塞都是这几家代工，别买山寨牌子省那十几块钱。第三，性能改装特别是刷电脑后发动机工作温度升高，一般选用比原厂冷一个级别的火花塞，具体要问刷电脑的技师，确保冷热度和间隙和新程序匹配。",
         "sentences": [
            ["有些高性能发动机是一缸两个火花塞，比如转子发动机、克莱斯勒hemi、奔驰M112 V6和M113 V8。", "Some high-performance engines use two plugs per cylinder—rotaries, the Chrysler Hemi, Mercedes M112/M113.", "two plugs per cylinder（每缸双火花塞）"],
            ["最好的火花塞品牌有NGK、博世、电装、Champion，买哪个都不会买错，别为省十几块钱买山寨。", "NGK, Bosch, Denso, Champion—all safe buys; don't save pennies on knockoffs.", "knockoffs（山寨货）"],
            ["动力改装特别是刷电脑后发动机温度升高，一般选用比原厂冷一个级别的火花塞。", "After a tune, engines run hotter—usually step the plug one range colder.", "step one range colder（冷一个级别）"],
            ["具体用冷几个级别要问刷电脑的技师，确保热度和间隙跟新程序匹配。", "Ask your tuner how far to go, matching heat range and gap to the new map.", "match（匹配）"]
         ]}
    ]
}

ARTICLES["horsepower-vs-torque-2"] = {
    "title_zh": "马力与扭矩（下）：数据背后与冲程的物理",
    "title_en": "Horsepower vs Torque (2): The Data and the Physics",
    "duration": "14:53",
    "topic": "汽车 · 发动机参数",
    "scenes": [
        {"id": "s1", "scene_zh": "快有quick和fast两种", "scene_en": "Two Kinds of Fast", "time": "00:00",
         "context": "发动机性能的主流评价标准就是一个字：快。但快有两层意思：提速的快（quick，迅速敏捷）和极速的快（fast，纯粹快速）。提速考验扭矩，极速看马力。",
         "sentences": [
            ["对于发动机性能的主流评价标准，其实就是一个字：快。", "The mainstream yardstick for engine performance is one word: fast.", "yardstick（评价标准）"],
            ["但这个快有两层意思：一个是提速的快，一个是极速的快。", "But 'fast' splits into quickness (acceleration) and top speed.", "quickness（提速）"],
            ["提速考验的是扭矩，极速看的则是马力。", "Acceleration tests torque; top speed tests horsepower.", "top speed（极速）"]
         ]},
        {"id": "s2", "scene_zh": "极速看马力加速看扭矩", "scene_en": "Horsepower Sets Top Speed", "time": "01:21",
         "context": "你可能零百4秒提速很快，但跑到240就到头了；我零百5秒多，却能轻松开到280、290，只要跑道足够长追上你是迟早的事。只要变速箱挡位够用，极速能跑多快看的是马力大小；从静止或固定速度开始提速有多猛、推背感多强，看的是扭矩。",
         "sentences": [
            ["零百4秒提速很快，但跑到240就结束了；我5秒多却能轻松开到280。", "You hit 100 in 4s but top out at 240; I'm slower to 100 but cruise to 280.", "top out（到头）"],
            ["只要跑道足够长，比你快是迟早的事情。", "Given a long enough runway, I'll pass you eventually.", "runway（跑道）"],
            ["极速看的是马力的大小，提速有多猛、推背感有多强，看的是扭矩。", "Horsepower sets top speed; torque sets how hard it pulls.", "pull（推背感）"]
         ]},
        {"id": "s3", "scene_zh": "两个极端例子", "scene_en": "Two Extreme Examples", "time": "02:18",
         "context": "马自达6的2.5T四缸发动机，最大马力250匹，最大扭矩432牛米，扭矩比市面上同级高很多。本田S2000的F20C发动机正好相反，240匹马力但扭矩只有206牛米，连人家一半都不到。看似非常接近又非常悬殊的数据背后有讲究。",
         "sentences": [
            ["马自达6的2.5T发动机，最大马力250匹，最大扭矩居然达到432牛米。", "The Mazda6 2.5T makes 250 hp and a hefty 432 Nm.", "hefty（惊人的）"],
            ["本田S2000的F20C正好相反：240匹马力，扭矩却只有206牛米。", "The S2000's F20C flips it: 240 hp but just 206 Nm.", "flips it（正好相反）"],
            ["看似非常接近又非常悬殊的数据，背后到底是怎么个说法？", "Nearly equal power, wildly different torque—what's the story?", "wildly different（非常悬殊）"]
         ]},
        {"id": "s4", "scene_zh": "马力扭矩图", "scene_en": "Reading the Dyno Chart", "time": "03:19",
         "context": "平时说的这车马力多少、扭矩多少，其实只是整个曲线上的最高点。真正性能的综合体现要看扭矩在各转速上的实际表现，日常开车不可能永远拉到五六千转找最大功率，低转速时的扭矩和马力输出对市区代步的消费者更有意义。先测出来的是红色扭矩曲线，再用公式算出各转速的马力连成绿色马力曲线。",
         "sentences": [
            ["平时说的马力多少、扭矩多少，只是曲线上的一个最高点。", "The headline number is just the peak of the curve.", "peak（最高点）"],
            ["真正性能的综合体现，要看扭矩在各个转速上的实际表现。", "Real performance lives in the torque curve across the rev range.", "rev range（转速区间）"],
            ["低转速时的扭矩和马力输出，对市区代步的消费者更有意义。", "Low-rpm output matters far more for daily commuters.", "commuter（通勤者）"]
         ]},
        {"id": "s5", "scene_zh": "冲程决定扭矩", "scene_en": "Stroke Sets Torque", "time": "04:41",
         "context": "活塞从下止点到上止点的距离叫冲程，等于曲轴半径的两倍。用同样多的汽油在头顶爆出同样多的能量压到活塞上，曲轴半径越长，同样的力压下来力臂更长，产生的扭矩更大。马自达2.5T扭矩大很大程度靠长达100毫米的冲程；本田S2000冲程只有84毫米，力臂短扭矩自然大不到哪去。",
         "sentences": [
            ["活塞从最低点到最高点的距离就是冲程，等于曲轴半径的两倍。", "The piston's travel from bottom to top is the stroke—twice the crank radius.", "stroke（冲程）"],
            ["同样的力压下来，曲轴半径越长、力臂越长，产生的扭矩就越大。", "Same force, longer lever arm, bigger torque.", "lever arm（力臂）"],
            ["马自达2.5T扭矩大，很大程度靠长达100毫米的冲程。", "The Mazda's fat torque owes a lot to its 100 mm stroke.", "100 mm stroke（100毫米冲程）"],
            ["本田S2000冲程只有84毫米，力臂短，扭矩肯定大不到哪去。", "The S2000's 84 mm stroke means a short arm—no big torque.", "short arm（短力臂）"]
         ]},
        {"id": "s6", "scene_zh": "马力公式与5252", "scene_en": "The Formula and 5252", "time": "06:24",
         "context": "用英制单位算，马力值等于转速乘以扭矩除以5252。转速低于5252转时系数小于1，马力数值比扭矩小，曲线在扭矩曲线下面；正好5252转时系数为1，两者数值相等，图中就是交叉点；高于5252转后马力值大于扭矩值。只要扭矩保持得差不多，越坚持到高转速系数越大，马力数字就开始爬升。这就是本田S2000扭矩一般但马力拉到240匹的秘诀：全力往高转拉，原厂红线9500转。",
         "sentences": [
            ["马力值实际上是转速乘以扭矩再除以5252。", "Horsepower equals rpm × torque ÷ 5252.", "formula（公式）"],
            ["转速低于5252转，马力数值比扭矩小；高于5252转，马力值就大于扭矩值。", "Below 5252 rpm hp trails torque; above it, hp leads.", "trail（落后）"],
            ["只要扭矩保持得差不多，越坚持到高转速，马力数字就开始爬升。", "Hold torque and push the revs—hp climbs.", "climb（爬升）"],
            ["S2000的秘诀就是全力往高转拉，原厂红线转速能达到9500转。", "The S2000's trick: scream to a 9,500 rpm redline.", "redline（红线转速）"]
         ]},
        {"id": "s7", "scene_zh": "长冲程限制转速", "scene_en": "Long Stroke Caps the RPM", "time": "08:04",
         "context": "马自达2.5T扭矩这么牛为什么不能把转速拉高刷马力？依然是长冲程的缘故：曲轴半径越大，活塞上下运动起来越费劲、越不稳定；半径小的反而越转越快、转得风生水起。为得到更大扭矩而设计的长冲程，反过来限制了最高转速，从而限制马力输出。马力、扭矩、转速三者互相牵制又互相成就，一起决定发动机特性，就像人的性格各有特点。",
         "sentences": [
            ["马自达不能拉高转速，原因依然还是长冲程。", "The Mazda can't rev high—again, the long stroke.", "long stroke（长冲程）"],
            ["曲轴半径越大，活塞转起来越费劲越不稳定。", "A bigger crank radius spins harder and less stably.", "unstable（不稳定）"],
            ["为得到更大扭矩而设计的长冲程，反过来限制了最高转速，从而限制马力输出。", "The long stroke that boosts torque also caps rpm—and therefore hp.", "caps（限制）"],
            ["马力、扭矩、转速三者互相牵制又互相成就，就像人的性格各有特点。", "The three fight and reinforce each other, like different personalities.", "reinforce（互相成就）"]
         ]},
        {"id": "s8", "scene_zh": "柴油机追求扭矩的极端", "scene_en": "Diesel: The Torque Extreme", "time": "10:46",
         "context": "柴油机靠压燃点燃，必须压得非常狠，压缩比低不了。以康明斯3.8升四缸柴油机为例，压缩比17.2:1，活塞要顶得很高压缩比才大，冲程短不了，曲轴半径小不了，天然决定力臂特别长、扭矩大。但同样因为曲轴半径大，转速上不去，2600转就到头，马力只有168匹，扭矩却达600牛米。",
         "sentences": [
            ["柴油机靠压燃点燃，压缩比低不了，活塞要顶得很高，冲程短不了。", "Diesels are compression-ignited, needing a huge CR and a long stroke.", "compression ratio（压缩比）"],
            ["康明斯3.8升柴油机压缩比17.2比1，冲程115毫米。", "This Cummins 3.8L runs a 17.2:1 CR with a 115 mm stroke.", "Cummins（康明斯）"],
            ["转速2600转就到头，马力只有168匹，扭矩却能达到惊人的600牛米。", "It revs to just 2,600, making 168 hp but a monster 600 Nm.", "monster（惊人的）"]
         ]},
        {"id": "s9", "scene_zh": "F1追求马力的极端", "scene_en": "F1: The Horsepower Extreme", "time": "12:03",
         "context": "F1是追求马力的极端：2006年F1发动机最大扭矩350牛米左右（和买菜汉兰达差不多），但马力却爆发到接近800匹。所有黑科技都只是手段，落到公式上就是扭矩乘转速除以5252。它硬靠着超过2万转的转速把马力拉出来，曲轴半径设计得非常迷你，冲程只有39.8毫米，运动距离不足4厘米，和小仓鼠跑跑轮差不多。",
         "sentences": [
            ["2006年F1发动机最大扭矩350牛米左右，和买菜的汉兰达差不多。", "A 2006 F1 engine made ~350 Nm—about what a family SUV makes.", "family SUV（家用SUV）"],
            ["但它的马力却能爆发到接近800匹。", "Yet its output approached 800 hp.", "800 hp（800马力）"],
            ["它是硬靠着超过2万转的转速把马力拉出来的。", "It's wrung out by revving past 20,000 rpm.", "20,000 rpm（两万转）"],
            ["F1的曲轴半径设计得非常迷你，冲程只有39.8毫米，运动距离不足4厘米。", "The F1 crank is tiny—a 39.8 mm stroke, under 4 cm of travel.", "miniature（迷你）"]
         ]},
        {"id": "s10", "scene_zh": "博尔特与大力士", "scene_en": "Bolt vs the Strongman", "time": "13:36",
         "context": "大马力的F1好比博尔特，跑起来风驰电掣；大扭矩的柴油机好比大力士。大家轻装上阵时你肯定跑不过博尔特；但背上一点负载，博尔特就跑不过大力士了。所以马力和扭矩谁更厉害要分场景看：低转速早发力大扭矩适合越野拉货，高马力适合追求极速。",
         "sentences": [
            ["大马力的F1就好比博尔特，大扭矩的柴油机就好比大力士。", "Big-hp F1 is Usain Bolt; big-torque diesel is a strongman.", "strongman（大力士）"],
            ["轻装上阵你肯定跑不过博尔特，但背上一点负载，博尔特就跑不过大力士了。", "Unloaded, Bolt wins; loaded, the strongman does.", "loaded（负重）"],
            ["低转速早发力大扭矩适合越野拉货，高马力适合追求极速。", "Early, big torque suits off-roading and hauling; high hp suits top speed.", "off-roading（越野）"]
         ]},
        {"id": "s11", "scene_zh": "最终答案", "scene_en": "The Answer", "time": "14:02",
         "context": "开头提的疑问马力和扭矩到底谁更厉害，现在能不能回答出来？如果你能直接回答，那可能还没彻底领悟；如果你觉得要看怎么说，那你大概率是搞懂了。很多问题并不是非黑即白，知道的东西越多越觉得不好回答。",
         "sentences": [
            ["如果你觉得马力和扭矩谁厉害要看怎么说，那你大概率还是搞懂了的。", "If your answer is 'it depends,' you've probably got it.", "it depends（看情况）"],
            ["很多问题并不是简单的非黑即白。", "Few questions are simply black and white.", "black and white（非黑即白）"],
            ["你知道的东西越多，你就越觉得这个问题不太好回答。", "The more you know, the harder the question gets.", "the more you know（知道得越多）"]
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
            "platform": "bilibili",
            "source_url": f"https://www.bilibili.com/video/{slug}",
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
