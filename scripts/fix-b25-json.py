#!/usr/bin/env python3
"""批25：为简化场景JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "audi-quattro-1": {
        "practice": [
            ["说冠齿差速器", "The crown-gear diff locks mechanically when one axle slips."],
            ["说前轮打滑", "The purple crown gear speeds up and red pinions self-rotate."],
            ["说后轮打滑", "The green crown gear speeds up and the pinions push it outward."],
            ["说动力分配", "Default 40/60; during slip it can reach 70/30 or 15/85."],
            ["说三个分流", "Center diff splits front/rear; open diffs split left/right."],
            ["说托森对比", "Lighter, freer torque split, better electronics integration."]
        ],
        "pitfalls": [
            ["Treat Quattro as one system.",
             "It's a trademark covering four different AWD layouts.",
             "Quattro是商标不是一种四驱。"],
            ["Expect the diff to lock 100/0.",
             "Clutch plates have a physical locking limit.",
             "离合片有物理锁定极限。"],
            ["Think the split is electronically controlled.",
             "Gen 6 locks purely mechanically, reacting to slip.",
             "自锁是纯机械反应。"],
            ["Ignore the open axle diffs.",
             "Both axles are open unless you spec the sport rear diff.",
             "前后都是开放式差速器。"],
            ["Forget it reacts passively.",
             "Power shifts only after slip appears, not proactively.",
             "分配是被动的。"]
        ],
        "shifts": [
            ["说差速器只说 differential",
             "用 crown-gear diff（冠齿差速器）、Torsen（托森）、sport diff（运动差速器）"],
            ["说打滑只说 slip",
             "用 self-lock（自锁）、self-rotate（自转）、orbit（公转）、axially（轴向）"],
            ["说动力只说 power",
             "用 torque split（动力分流）、lever arm（力臂）、clutch plates（离合片）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：奥迪Quattro是商标而非特定四驱、纵置发动机上有Quattro和Quattro ultra、横置发动机上有Haldex、电动车上有e-Quattro、第一种Quattro已出到第六代、前五代基于托森中央差速器、第六代用奥迪自研冠齿自锁式限滑中央差速器、只针对纵置发动机车型、A4/A5/A8/Q7/Q8/RS5在用、四驱即动力的三个分流、黑色壳体与变速箱输入轴硬连接、四个红色小齿轮咬合前后两个冠齿齿轮、正常时红色齿轮只公转不自转、前轮打滑紫色冠齿齿轮转更快、红色齿轮自转产生轴向推力、离合片被压到一起形成硬性连接、动力更多传到后轴、整个过程纯机械自发无液压电子控制、后桥打滑绿色冠齿齿轮转更快、红色齿轮反方向自转、动力更多传到前轴、正常分配前40后60、打滑时可达前70后30或前15后85、离合片锁定有物理极限、默认40比60靠力臂比例4比6纯物理实现、前后都是开放式差速器、运动车型可选配运动后差速器、冠齿系统四轮永远有动力、对比托森三大优势更轻2千克分配更自由能更好整合电子系统、缺点是分配被动且前后差速器开放等。"
    },
    "audi-quattro-2": {
        "practice": [
            ["说ultra默认前驱", "Quattro ultra defaults to a 100/0 front-drive split."],
            ["说电脑锁离合", "The computer locks the clutch before slip, sensing intent."],
            ["说断开机构", "Decoupling shafts stop the driveshaft to save fuel."],
            ["说Haldex", "BorgWarner's clutch pack sits at the gearbox tail."],
            ["说极限50比50", "Fully locked, either system tops out at 50/50."],
            ["说怎么选", "Choose by need—economy, driving style, and platform."]
        ],
        "pitfalls": [
            ["Assume ultra is always AWD.",
             "It's on-demand: pure FWD until the computer locks in.",
             "ultra默认是前驱。"],
            ["Think ultra and Haldex are the same.",
             "Ultra fits longitudinal cars; Haldex fits transverse ones.",
             "纵置用ultra横置用Haldex。"],
            ["Expect a sport rear diff on Haldex cars.",
             "There's no sport diff option on these systems.",
             "Haldex没有运动后差速器。"],
            ["Forget the decoupler's fuel savings.",
             "A truly idle driveshaft wastes nothing.",
             "断开传动轴省油。"],
            ["Buy 'the best' AWD blindly.",
             "There's no best—only the fitting system for your use.",
             "没有最好只有最合适。"]
        ],
        "shifts": [
            ["说四驱只说 AWD",
             "用 on-demand（适时四驱）、multi-plate clutch（多片离合）、decoupler（断开机构）"],
            ["说动力分配只说 split",
             "用 proactively（主动地）、engage（接合）、lock the clutch（锁离合）"],
            ["说省油只说 fuel economy",
             "用 fuel savings（省油）、disconnected（断开）、driveshaft（传动轴）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：quattro ultra用在所有奥迪纵置车型上是适时四驱、A6/A7/A8/Q5在用、前桥仍是开放式差速器、往后传动力靠电控多片离合器、默认前后100比0是纯前驱、前轮打滑或想运动驾驶时电脑主动锁死离合片、等红灯轰油门电脑判断想弹射起步提前锁死、离合片极限只能50比50、电子刹车限滑默认都有、关键部件有多片主动电控离合片和两组可电子控制连接断开的轴、进入前驱模式时离合片和轴都断开后轮完全自由、传动轴连转都不转最大限度减少油耗、优点是省油适合市区驾驶、动力分配电脑主动控制不是打滑才介入、缺点是偏前驱属性动力分配不够硬派前后都是开放差速器、Haldex用在横置四驱车型上A3/Q3/TT/R8/RS3/TT RS、是博格华纳的技术已到第五代、发动机动力到开放式前桥差速器、一组齿轮把动力转90度向后传、多片离合设计在变速箱尾部、默认也是100比0、打滑或运动驾驶时电脑压上离合片动力传到后桥、锁死极限50比50、后桥是开放差速器没有运动差速器可选、优点是省油主动控制比纯液压强、缺点是纯纯前驱属性前后桥开放差速器、深入研究会发现没有最好只有最合适、情怀归情怀科技永远在向前进步等。"
    },
    "turbo-principle": {
        "practice": [
            ["说涡轮原理", "Exhaust spins one fan, the other packs more air in."],
            ["说中冷器", "Cooling the compressed air keeps its density up."],
            ["说三大缺点", "Cost, extreme heat, and turbo lag."],
            ["说双涡轮", "Two smaller turbos beat one big one on response."],
            ["说顺序涡轮", "A valve lets the small turbo boost first, then both work."],
            ["说双涡管", "Separate scrolls stop exhaust pulses from fighting."]
        ],
        "pitfalls": [
            ["Think a bigger turbo is always better.",
             "Bigger spools slower—more lag.",
             "涡轮越大迟滞越大。"],
            ["Skip the intercooler.",
             "Hot, thinned air reduces what actually reaches the engine.",
             "压缩空气会变热变稀。"],
            ["Blame the turbo for high running costs alone.",
             "Supporting parts, oiling, and plumbing all add up.",
             "配套部件都是成本。"],
            ["Confuse twin-scroll with twin turbo.",
             "Twin-scroll is one turbo with two paths.",
             "双涡管不是双涡轮。"],
            ["Forget anti-lag tech exists.",
             "Modern engines manage lag well today.",
             "现代技术已很好控制迟滞。"]
        ],
        "shifts": [
            ["说涡轮只说 turbo",
             "用 spool up（起压）、turbo lag（涡轮迟滞）、boost（增压）"],
            ["说结构只说 structure",
             "用 twin-scroll（双涡管）、sequential（顺序涡轮）、intercooler（中冷器）"],
            ["说对比只说 compare",
             "用 naturally aspirated（自然吸气）、supercharger（机械增压）、efficiency（效率）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：发动机动力靠汽油和空气燃爆、想要更大动力就要更多空气、排量固定吸入空气有限、于是有了涡轮增压、废气先吹到涡轮的小电风扇上、带动轴另一头进气端风扇像鼓风机一样把更多空气压进发动机、空气变多就能喷更多汽油动力自然大了、中冷器用来冷却进气、空气压缩后变热膨胀变稀薄、吸入量反而减少、大多数中冷放车头迎风或引擎盖开洞如斯巴鲁STI、也有水冷、涡轮缺点一是贵几千到几万配套设备也都是钱、二是高温最高近900多度需要单独油路润滑降温对机油要求更高、三是涡轮迟滞一脚油门踩到底要等一两秒动力才跟上、双涡轮用两个小一号涡轮代替一个大涡轮、V型发动机左右排气歧管各装一个、Twin Turbo和Bi-turbo都是双涡轮、V型双涡轮实际是这一侧排气涡轮给另一侧进气服务、顺序涡轮一个小涡轮加一个大一号涡轮之间有阀门、低转速关阀门只驱动小涡轮快速增压、转速上来打开阀门两涡轮同时增压、兼顾迟滞和马力、马自达RX-7和丰田Supra用过、因管路复杂现代技术改进今天新车上基本看不到、双涡管涡轮是单涡轮双涡管、直列四缸1、4缸共用一管2、3缸共用一管、四缸机点火顺序1342、后一缸排气正压和前一缸负压重叠抵消压力、把互相影响的缸分开排气压力更高效施加到涡轮、宝马Twin Power Turbo其实是双涡管、涡轮大势所趋优势大于劣势、自吸可靠性后期保养更胜一筹、机械增压没迟滞动力随叫随到基本不产生高温、但用发动机本身能量增压理论效率不如涡轮等。"
    },
    "suspension-types-1": {
        "practice": [
            ["说打伞比喻", "More hands on the wheel means a steadier ride."],
            ["说三类悬挂", "Independent, non-independent, and semi-independent."],
            ["说麦弗逊", "Coil-over plus a triangular lower arm—one-hand control."],
            ["说双叉臂", "Two wishbones let the wheel arc and hold camber."],
            ["说动态外倾角", "The wheel's negative camber cancels body lean."],
            ["说选型", "Struts save space and cost; wishbones grip better."]
        ],
        "pitfalls": [
            ["Judge suspension by name alone.",
             "Names are marketing—look at the arms.",
             "别被名字忽悠。"],
            ["Think more parts always mean better.",
             "Tuning matters as much as the layout.",
             "形式只是基础调教重要。"],
            ["Expect a strut to hold camber.",
             "It moves straight up and down—grip drops in hard corners.",
             "麦弗逊直上直下。"],
            ["Assume all cars can use double wishbones.",
             "Cost, driveshaft clearance, and space block it.",
             "双叉臂贵且占空间。"],
            ["Ignore unsprung mass.",
             "Lighter is genuinely better where it counts.",
             "簧下质量轻很重要。"]
        ],
        "shifts": [
            ["说悬挂只说 suspension",
             "用 MacPherson strut（麦弗逊）、double wishbone（双叉臂）、lower arm（下臂）"],
            ["说控制只说 control",
             "用 wheel path（轮迹）、camber（外倾角）、grip（抓地力）"],
            ["说结构只说 structure",
             "用 unsprung mass（簧下质量）、coil-over（弹簧避震一体）、A-arm（三角臂）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：悬挂形式千千万不同厂商叫不同名字、名字更像文字游戏异形连杆无非三横一竖的连杆布局、悬挂形式只是表现基础调教至关重要、车在崎岖路面好比风雨中撑大伞、天气是路况大伞是轮子你是悬挂、抓住轮子的手越多每只手压力越小轮子越稳、两只手打伞比一只手稳、悬挂分三类独立非独立半独立、独立悬挂每个轮子一套互不干扰、非独立悬挂左右轮一根硬轴连接、半独立介于两者之间典型如扭力梁、麦弗逊由美国人艾尔麦弗逊发明、弹簧避震一体配三角下臂、典型一只手撑伞控制轮子的手最少、运动基本直上直下不太能改变外倾角、极限驾驶操控性相对没那么好、优点是精简部件做到轻是簧下质量轻、造价低保养维护便宜、结构让出空间给驱动轴天然对前驱友好、整体很窄不占横向空间、双球节悬挂把三角下臂换成两根独立连杆、查普曼悬挂是莲花创始人设计用驱动轴和一根连杆代替三角下摆臂、现在只有菲亚特500X和吉普自由侠后悬挂用、双叉臂公认性能优于麦弗逊、由一上一下两个叉臂组成、麦弗逊避震一人干双叉臂两人的活、双叉臂避震只负责支撑和过滤震动转向轨迹由叉臂负责、上臂短于下臂轮子往上运动带角度走、过弯车身侧倾外侧轮负外倾角与车身倾斜抵消、轮胎保持90度100%接触抓地力最大化、为什么不是所有车都用双叉臂因为贵零件多人工贵、前悬挂避震挡传动轴需拱门设计、横向占空间大放前占发动机舱放后占后备箱等。"
    },
    "suspension-types-2": {
        "practice": [
            ["说多连杆", "Multi-link is the wishbone's upgrade—two people, two hands."],
            ["说异形连杆", "Three lateral links plus one longitudinal—the integral link."],
            ["说扭力梁结构", "One welded beam, wheels bolted on, body mounts as pivots."],
            ["说半独立原因", "The beam twists, letting the wheels move opposite ways."],
            ["说扭力梁优点", "Cheap, flat, roomy, and skips the anti-roll bar."],
            ["说怎么选", "Match the layout to your driving, not the spec sheet."]
        ],
        "pitfalls": [
            ["Assume more links always help a daily driver.",
             "You won't feel the difference, but you'll pay to maintain it.",
             "买菜车多连杆开不出区别。"],
            ["Call a torsion beam independent.",
             "It's semi—the wheels still share a beam.",
             "扭力梁是半独立。"],
            ["Expect alignment on a torsion beam.",
             "It's rigid end to end—factory settings are permanent.",
             "扭力梁不能四轮定位。"],
            ["Overlook the anti-roll bar savings.",
             "The beam's twist already does that job.",
             "扭力梁自带防倾功能。"],
            ["Buy by suspension name alone.",
             "Every layout is a variant of four families.",
             "万变不离其宗。"]
        ],
        "shifts": [
            ["说连杆只说 link",
             "用 multi-link（多连杆）、integral link（异形连杆）、four-link（四连杆）"],
            ["说扭力梁只说 torsion beam",
             "用 twist（扭转）、welded（焊接的）、pivot（轴心转动）"],
            ["说结论只说 conclusion",
             "用 more is better（越多越好）、fits your need（合你需求）、tuning（调教）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：多连杆是双叉臂升级版拥有双叉臂所有优点、对轮子控制优于双叉臂、双叉臂是一个人两只手打伞多连杆是两个人各用一只手打伞布局自由很多、多连杆前后都能用、连杆数量三连杆四连杆五连杆都有、连杆越多表现越好、异形连杆是四连杆的一种多用于后轮、三根横向连杆一上两下加一根纵向连杆就是三横一竖、成本不变前提下有效提高悬挂表现性价比高、民用车型多连杆极限在五连杆、布局没有一定之规取决于车定位、工程师设计调教五根连杆位置角度尺寸、扭力梁也叫拖曳臂、几根铁板焊在一起的整体、两边的轮子直接硬连接不涉及连杆摆臂、以两个固定在车身上的点为轴心上下运动、这根梁有韧性会扭动、一个轮子提一个轮子压时梁通过自身扭曲完成两个轮子不同方向运动、说完全非独立不对说独立也不对所以叫半独立、优点非常便宜一块铁板两个螺丝固定、扭转过程与防倾杆原理重叠防倾杆就不装了又省一笔、后期保养除两个衬套没有会坏的地方、结构平坦腾出后备箱后排空间、缺点不是独立悬挂舒适操控大打折扣、完全不能做四轮定位调节、轮子和梁硬连接梁和车身硬连接原厂什么样就永远什么样、改装只能改短簧避震外倾角后倾角都改不了、独立好于半独立连杆多好于连杆少、多连杆略好于双叉臂双叉臂好于麦弗逊、买菜车前麦弗逊后扭力粮简简单单、对运动有要求扭力梁肯定没法看、调教好的麦弗逊也值得拥有、万变不离其宗都是四种的改良衍生等。"
    },
    "ackermann-angle-1": {
        "practice": [
            ["说转向机构", "Rack-and-pinion turns wheel rotation into rack motion."],
            ["说平行转向问题", "Parallel wheels can't share one turning center."],
            ["说梯形几何", "A trapezoid makes the inside wheel steer more."],
            ["说完美几何", "Trapezoid lines meeting at the rear axle = perfect steering."],
            ["说数学表达", "cot B − cot A equals track over wheelbase."],
            ["说阿克曼角", "It's the difference between the two steer angles."]
        ],
        "pitfalls": [
            ["Think parallel front wheels are fine.",
             "They can't turn around one center—the car scrubs.",
             "平行转向转不顺畅。"],
            ["Expect perfect Ackermann to be universally used.",
             "Real tires deform, so real cars tune away from it.",
             "完美阿克曼只在黑板。"],
            ["Confuse the angle with the geometry.",
             "The percentage and anti-Ackermann matter more in practice.",
             "实际更多用百分比表述。"],
            ["Forget who invented it.",
             "The lawyer Ackermann registered Lankensperger's idea in his own name.",
             "名字来自抢注专利的律师。"],
            ["Ignore the trig relation.",
             "cotB−cotA=track/wheelbase defines 100% Ackermann.",
             "记住cot差等于胎距比轴距。"]
        ],
        "shifts": [
            ["说转向只说 steering",
             "用 rack-and-pinion（齿条齿轮）、steering geometry（转向几何）、steer angle（转向角）"],
            ["说几何只说 geometry",
             "用 trapezoid（梯形）、turning center（转向圆心）、perpendicular（垂直线）"],
            ["说比例只说 ratio",
             "用 wheelbase（轴距）、track（胎距）、percentage（百分比）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：绝大多数乘用车用齿条齿轮转向、把方向盘旋转转化为齿条横向移动、齿条往左移轮子往右转、如果转向几何设计成两前轮永远平行、转弯时内侧轮转过的圈比外侧小、内侧轮要转更大角度走更小的圈、三根垂直线永远不可能在一个点会合、四个轮子做不到绕同一圆心转动、就会以轮胎打滑脱载形式表现、说人话就是转弯转得不顺畅、挡住左前轮当它是三轮车就和谐顺畅、放回来就格格不入、德国车轮匠兰肯斯伯格1817年发现把长方形悬挂几何改成梯形、内侧轮比外侧转更大角度、当梯形两条腰延长线焦点正好位于后轴中心、不管打多少方向三根线永远交于一点、四个轮子顺畅绕同一个点转动、完美的转向几何诞生、兰肯斯伯格委托律师鲁道夫阿克曼注册专利、阿克曼自己跑到英国用自己名字注册、这就是阿克曼转向几何名字由来、设两前轮转向角A和B半径R轴距L胎距T、得两个三角函数方程相减得cotB减cotA等于胎距比轴距、任何时候满足此方程就称100%符合阿克曼转向几何、常说的阿克曼角指两个转向角之差角A减角B、实际应用很少讲阿克曼角因为它随打方向不断变化、更多用正反阿克曼和阿克曼百分比表述交流等。"
    },
    "ackermann-angle-2": {
        "practice": [
            ["说滑移角", "Rubber deforms, so actual travel lags the tire's heading."],
            ["说重心转移", "Fast corners pile load on the outside tire."],
            ["说反阿克曼", "The outside wheel steers more to beat its own slip."],
            ["说向心力", "Cornering force peaks at a ~5.5° slip angle."],
            ["说民用设定", "Daily drivers stay near 100%; sporty cars lean anti."],
            ["说改阿克曼", "It's two points on the knuckle—drill and move."]
        ],
        "pitfalls": [
            ["Ignore the slip angle.",
             "Perfect theory Ackermann fails because of tire deformation.",
             "滑移角让完美阿克曼失效。"],
            ["Assume F1 uses the same setup everywhere.",
             "Slow-corner tracks like Monaco need a milder setup.",
             "赛道不同调校不同。"],
            ["Add spacers and expect calibration to hold.",
             "Spacers change the track—breaking the geometry.",
             "法兰盘破坏标定。"],
            ["Think four-wheel steering changes the physics.",
             "It only adds complexity; the principle is the same.",
             "四轮转向原理相同。"],
            ["Overlook cold-tire scrubbing.",
             "Anti-Ackermann costs grip in slow turns on cold tires.",
             "低速冷胎会跳胎。"]
        ],
        "shifts": [
            ["说轮胎只说 tire",
             "用 slip angle（滑移角）、deform（形变）、contact patch（接地面积）"],
            ["说设定只说 setup",
             "用 anti-Ackermann（反阿克曼）、100% Ackermann（完美阿克曼）、aggressive（激进的）"],
            ["说改装只说 modify",
             "用 knuckle（羊角）、spacers（法兰盘）、ball joint（球头）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：现实世界轮胎是橡胶做的会形变、打方向时轮胎指向已转过但接触地面橡胶还拧着劲、实际行进方向打折扣、轮胎指向和实际行进方向夹角就是滑移角、完美阿克曼不好用就是因为滑移角存在、用F1举例因为是最极端例子、150公里时速转弯绝大多数重心压到外侧轮、内侧轮压力非常小极限时轻微离地、压得越大力气转向橡胶越拧巴滑移角越大、不施加压力几乎没有滑移角、外侧轮滑移角远大于内侧轮、所以外侧轮胎指向上要向左多转更多角度、减去滑移角后实际行进方向才接近完美箭头、F1赛车就是反阿克曼设定外侧轮转向角度明显大于内侧轮、F1转向设定根据赛道单独调校、高速弯多设计激进反阿克曼、蒙特卡洛低速弯调头弯多就不合适、快速过弯靠轮胎和地面摩擦产生的指向圆心的力克服离心力、这个力只有有了滑移角才产生就是橡胶拧巴的劲、滑移角大概5.5度时力达到最大值、这是外侧转向轮的极限滑移角能产生最大向心力、越家用的车设定越接近完美100%阿克曼、家用车慢慢悠悠转弯不需要多大滑移角对抗离心力、日常驾驶顺畅第一、硬开去赛道会体验到转向不足推头、偏运动的车型往反阿克曼方向靠一靠但不会像F1那么疯狂也不会设计成0%平行、介于两者之间、外侧轮多转角度正好和滑移角综合、轮胎实际行进方向和想要方向完美契合指哪打哪、代价是低速大幅度转弯如侧方停车时轮胎打滑跳胎特别是冷车冷胎、改装阿克曼很简单在羊角上重新钻一个洞把转向拉杆球头接过去、在一台轴距胎距固定的车上阿克曼调整就是两个点的调整、加装法兰盘改变胎距参数整个方程不成立、原厂阿克曼标定被完全破坏、乱改轮毂影响的东西比想象的多得多、后轮也存在滑移角、四轮转向本质原理一样等。"
    },
    "spark-plug-1": {
        "practice": [
            ["说火花塞任务", "The plug sparks the charge between two electrodes."],
            ["说正负极", "Center rod is positive; the L-arm is grounded through the head."],
            ["说点火原理", "~20,000 volts arc the gap and fire the mixture."],
            ["说三种材质", "Copper, platinum, and iridium—cost and life in that order."],
            ["说间隙", "0.6–1.8 mm; bigger spark needs more voltage and time."],
            ["说怎么换", "Follow the manual and always check the gap."]
        ],
        "pitfalls": [
            ["Upgrade or downgrade materials freely.",
             "Copper specs stay copper; iridium specs stay iridium.",
             "该用什么就用什么。"],
            ["Pick a spark plug by price.",
             "Cheap copper in a modern coil car wears out in days.",
             "高压包配铜塞磨损极快。"],
            ["Ignore the gap.",
             "It affects spark size, voltage, and timing.",
             "间隙影响点火效率。"],
            ["Buy knockoff brands to save a few yuan.",
             "OEM plugs come from NGK, Bosch, Denso, Champion.",
             "正品大牌更稳。"],
            ["Skip the manual.",
             "It specifies material, gap, and change interval.",
             "一切都以手册为准。"]
        ],
        "shifts": [
            ["说点火只说 ignition",
             "用 spark plug（火花塞）、ignition coil（高压包）、arc（电弧）"],
            ["说材质只说 material",
             "用 nickel alloy（镍合金）、platinum（铂金）、iridium（铱金）"],
            ["说参数只说 spec",
             "用 gap（间隙）、heat rating（热值）、firing voltage（点火电压）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：汽油发动机运行离不开点火步骤、点火任务由火花塞完成、火花产生在尖尖的中心电极和L型接地电极之间、绿色中心金属杆贯穿火花塞被白色陶瓷绝缘包裹、L型部分是螺纹的延伸、螺纹直接安装在发动机缸盖上、车身和发动机金属部分都是负极接地、所以L型就是负极、需要点火时行车电脑通过高压包给正极两万多伏特电压、正极两万多伏负极零伏、巨大电压差击穿空气形成火花完成点火、原理和闪电类似、中心电极常见三种材质铜铂金铱金、铜火花塞最便宜整根铜做尖端覆盖镍合金、导电导热好但铜软镍合金也不硬磨损快寿命短两三万公里就磨损完、为延长寿命把尖端做到2.5毫米直径、面积大了要更大电压好在铜导电性好互相抵消、八九十年代老车分电器低点火电压用得比较多、现在涡轮增压高转速发动机反而还用铜的、该用铜的不要升级用铂金铱金的不要降级、铂金比镍合金硬得多熔点更高、把一片铂金焊到尖端铜火花塞变铂金火花塞、磨损慢很多能承受更高点火电压寿命16万公里、现在绝大多数车用铂金、双铂金火花塞在接地电极上也焊一层铂金、铱金最贵铱比铂硬六倍强度高八倍熔点高近七百度、焊在中心电极表面进一步提升寿命、铱非常硬火花对电极表面磨损非常慢、中心电极尖端直径可做到最小0.4毫米、直径越小打出火花所需电压越低点火效率越高、用哪种材料翻车主手册、铜或镍合金十几二十块铂金二三十块铱金五六十块、间隙指中心电极到L型接地电极距离一般在0.6到1.8毫米、间隙越小火花越小越大火花越大、间隙大需要更大电压且火花形成速度变慢、低压缩比注重油耗的家用车间隙设计较大、高压缩比注重性能的运动车间隙设计较小利于精确控制点火正时、调整间隙用锥形厚度规、扩大间隙电极放圆孔轻轻向上掰、掰过头按在桌上压回来等。"
    },
    "spark-plug-2": {
        "practice": [
            ["说冷热型", "Colder plugs foul; hotter plugs can pre-ignite."],
            ["说自清区", "450–850°C: hot enough to self-clean, cool enough to be safe."],
            ["说怎么选冷热", "City cars run hot plugs; sports cars run cold ones."],
            ["说读编号", "NGK's 5th digit is heat range—smaller means hotter."],
            ["说判断好坏", "Gray, dry, intact electrodes mean a healthy plug."],
            ["说三点补充", "Twin-plug engines, real brands, and colder after tuning."]
        ],
        "pitfalls": [
            ["Judge a plug by its ceramic stains.",
             "Yellow stains are harmless blow-by.",
             "陶瓷发黄不影响性能。"],
            ["Replace a fouled plug without fixing the cause.",
             "Carbon, oil, or fuel faults will just refoul it.",
             "先治根源再换塞。"],
            ["Pick a hotter or colder plug for fun.",
             "Factory heat range is chosen for your engine's load.",
             "别随便换冷热。"],
            ["Delay replacement past the interval.",
             "Expect rough idle, misfires, and gutless acceleration.",
             "逾期不换怠速抖动力差。"],
            ["Tune without stepping the plug colder.",
             "A hotter engine needs a colder plug to avoid pre-ignition.",
             "刷电脑后要冷一级。"]
        ],
        "shifts": [
            ["说温度只说 temperature",
             "用 heat rating（热值）、fouling zone（积碳区）、pre-ignition（提前点火）"],
            ["说检查只说 check",
             "用 read the plug（读火花塞）、sooty（熏黑）、oil contamination（机油污染）"],
            ["说后果只说 result",
             "用 misfire（失火）、rough idle（怠速抖动）、step colder（冷一级）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：火花塞越冷工作温度越低燃烧室积碳机油废气颗粒物沉淀电极上、温度不足以燃烧清除慢慢覆盖电极影响表现缩短寿命、越热温度越高能自己清除电极表面积碳、但温度太高还没到点火时候就足以点燃油气混合体、出现提前爆震敲缸、火花塞低于450度处于积碳区高于850度处于自燃区危险、最佳工作温度450到850度之间叫自清区、既足够热清除积碳又没敲缸自爆风险、太偏冷散热太好油门全开温度上不去停留积碳区、太偏热散热慢油门踩深温度飙升进自燃区、原厂推荐差不多是绿线工况没事别买更冷更热、一般家用车或城市低速车用热型居多、发动机平时低负荷运行温度高不到哪去需要散热慢保持温度、运动车型经常地板油发动机一直高温需要散热更好的冷型、冷热度标在火花塞上、NGK的IZFR6K11S第五位数字6是热值数字越小越热越大越冷、博世ZGR6ST12里的6和NGK相反数字越大越热、拆下旧火花塞最重要检查两个电极、颜色灰灰或淡淡褐色整体干燥电极没断裂就是好的、陶瓷尾部黄色是串气烤糊不影响性能、黑黑一层被熏黑是被积碳污染、空气滤芯脏长期小油门长时间怠速都会导致、富油工况燃烧不充分也积碳、不仅要换火花塞还要查根源光换是治标不治本、黑黑但油油的是机油污染、典型是活塞环或气门油封密封不严机油漏进燃烧室、湿的一般是连续打火打不着汽油把火花塞弄湿、用清洗剂清洗吹干再找到打不着火的原因、白色沉淀物或融化痕迹说明经历高温可能发动机过热或冷热型没选对需要更换、明显磨损甚至断裂一般太久不按时换导致、火花塞不行了却不换最常见怠速抖动油耗增加、严重故障灯亮失火缺缸加速没力气启动困难、高性能发动机有的一个缸两个火花塞如转子发动机克莱斯勒hemi奔驰M112V6和M113V8、最好品牌NGK博士电装Champion绝大多数车企原厂都是这几家代工、别买山寨牌子省十几块钱、性能改装特别是刷电脑后发动机温度升高一般选用比原厂冷一个级别的火花塞、具体要问刷电脑的技师确保冷热度和间隙和新程序匹配等。"
    },
    "horsepower-vs-torque-2": {
        "practice": [
            ["说quick和fast", "Quickness tests torque; top speed tests horsepower."],
            ["说极速与加速", "Horsepower sets the top speed; torque sets the pull."],
            ["说两个极端", "Mazda6 2.5T: big torque. S2000: big revs."],
            ["说冲程", "A longer stroke means a longer lever—more torque."],
            ["说5252", "Below it hp trails torque; above it, hp leads."],
            ["说怎么选", "Match torque for hauling, horsepower for speed."]
        ],
        "pitfalls": [
            ["Compare only peak numbers.",
             "The curve shape matters more than the peak.",
             "峰值不代表一切。"],
            ["Think torque can't coexist with high rpm.",
             "Long strokes cap revs; short strokes trade torque for rpm.",
             "冲程决定转速上限。"],
            ["Assume diesel can't be powerful.",
             "It trades revs for torque—perfect for hauling.",
             "柴油机扭矩为王。"],
            ["Believe F1's power comes from magic.",
             "It's just torque × rpm ÷ 5252 at 20,000 rpm.",
             "F1马力靠转速硬拉。"],
            ["Ask which is 'better' without context.",
             "It depends on the load and the use.",
             "要看怎么说。"]
        ],
        "shifts": [
            ["说快只说 fast",
             "用 quickness（提速）、top speed（极速）、push you back（推背感）"],
            ["说数据只说 number",
             "用 peak（峰值）、torque curve（扭矩曲线）、dyno（马力机）"],
            ["说结构只说 structure",
             "用 stroke（冲程）、crank radius（曲轴半径）、redline（红线转速）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：发动机性能主流评价标准就是一个字快、快有两层意思提速的快和极速的快、一个quick一个fast、提速考验扭矩极速看马力、可能零百4秒提速很快但跑到240就结束、我5秒多却能轻松开到280290只要跑道足够长追上你是迟早的事、只要变速箱挡位够用极速看马力、提速多猛推背感多强看扭矩、大多数同级别民用发动机马力差不多扭矩也差不多、但就是有发动机高扭矩低马力、马自达6的2.5T四缸发动机最大马力250匹最大扭矩432牛米、本田S2000的F20C典型高马力低扭矩240匹马力扭矩只有206牛米连一半都没有、平时说的马力多少扭矩多少只是曲线上的最高点、真正性能综合体现看扭矩在各个转速的实际表现、低转速扭矩马力对市区代步更有意义、先测出红色扭矩曲线再用公式算出各转速马力连成绿色马力曲线、活塞从下止点到上止点距离叫冲程等于曲轴半径两倍、同样多的能量压到活塞上曲轴半径长力臂长扭矩大、马自达2.5T靠100毫米冲程、S2000冲程84毫米力臂短扭矩大不到哪去、英制单位马力等于转速乘扭矩除以5252、低于5252转马力数值比扭矩小曲线在下面、正好5252转系数1两者相等、高于5252转马力值大于扭矩值、只要扭矩保持差不多越坚持高转速马力爬升、这就是S2000扭矩一般马力240匹的秘诀全力往高转拉原厂红线9500转、马自达2.5T红线只有6000转、长冲程曲轴半径大转起来费劲不稳定、为更大扭矩设计的长冲程反过来限制最高转速从而限制马力、马力扭矩转速三者互相牵制又互相成就像人的性格、低转速早发力大扭矩适合越野拉货1500转2000转轻松爬坡拉货、柴油机靠压燃点燃压缩比低不了、康明斯3.8升柴油机压缩比17.2比1冲程115毫米、曲轴半径大转速拉不上去2600转到头、马力168匹扭矩600牛米、柴油机是追求扭矩的极端、F1是追求马力的极端、2006年F1发动机最大扭矩350牛米和汉兰达差不多但马力接近800匹、硬靠超过2万转转速拉出来、曲轴半径设计迷你冲程39.8毫米运动距离不足4厘米像小仓鼠跑跑轮、大马力F1好比博尔特大扭矩柴油机好比大力士、轻装上阵跑不过博尔特背上负载博尔特跑不过大力士、如果你觉得要看怎么说那你大概率是搞懂了、知道的东西越多越觉得这个问题不太好回答等。"
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
