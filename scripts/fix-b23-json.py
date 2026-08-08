#!/usr/bin/env python3
"""批23：为简化场景JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "at-transmission-1": {
        "practice": [
            ["说变速根本", "Two gears of different sizes change speed and force."],
            ["说齿比定义", "Gear ratio is driven teeth divided by driving teeth."],
            ["说低档高挡", "Low gear: small drives big; high gear: big drives small."],
            ["说换挡时机", "Cruise high, downshift to overtake."],
            ["说行星齿轮", "Sun, planets, carrier, and ring—hold one, drive one."],
            ["说倒挡原理", "Hold the carrier and the ring reverses."]
        ],
        "pitfalls": [
            ["Think high gear means more force.",
             "High gears trade force for speed.",
             "高档位是速度快力小。"],
            ["Confuse bike and car gearing.",
             "Cars: low gear is small-driving-big, opposite of bikes.",
             "汽车档位与自行车相反。"],
            ["Rev forever in first gear.",
             "High revs destroy an engine fast.",
             "一档别长期高转。"],
            ["Ignore gear ratios.",
             "Ratio = speed drop = torque boost.",
             "齿比是变速变矩的核心。"],
            ["Judge a transmission by gear count alone.",
             "Complexity adds ratios, not new principles.",
             "档位多不代表原理变。"]
        ],
        "shifts": [
            ["说变速箱只会说 gearbox",
             "用 drive ratio（传动比）、gear ratio（齿比）、torque multiplication（扭矩放大）"],
            ["说换挡只会说 shift",
             "用 downshift（降档）、overtake（超车）、launch feel（起步推背感）"],
            ["说行星齿轮只会说 planetary gear",
             "用 sun gear（太阳齿轮）、planet carrier（行星架）、outer ring（外齿圈）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：AT自动变速箱怎么传动、用克莱斯勒4E T1四速自动变速箱举例、看明白简单的九速十速也能想象、齿比和行星齿轮是大篇幅重点、变速的根就是两个尺寸不同的齿轮、小齿轮带大齿轮转速减小力气变大、大齿轮带小齿轮速度变大力气变小、山地自行车高档位小带大踩得轻松车速慢、低档位大带小踩得吃力提速快、齿比传动比就是从动轮和驱动轮的尺寸比值、齿轮尺寸和齿数挂钩所以也叫齿比、20个齿对10个齿齿比2比1、力放大两倍速度减小两倍、上坡挂高档位车速慢但腿省力、想迅速提速换低档位、自行车变速为了救活人的感受、发动机不会累给汽油就源源不断输出动力、汽车的变档机构为了救活车轮的感受、一档齿比3.5比1左右力放大3.5倍、二档2比1左右、越往高档驱动齿轮越大被驱动齿轮越小、高速巡航用高档位超车降档、手动变速箱一对外齿轮负责一个档位、AT用更巧妙占体积更小的行星齿轮、太阳齿轮居中行星齿轮绕转、行星架架起行星齿轮外齿圈包裹、行星齿轮组主要看三个部件、任意一个固定住剩下两个转动一个另一个就被驱动、按住太阳轮转行星架行星轮自转带动外齿圈、按住行星架转太阳轮行星轮原地自转带动外齿圈反转、反转拿来做倒挡、输入端永远在转动输出端连接车轮、发动机动力通过曲轴经过液力变矩器传递到红色输入轴等。"
    },
    "at-transmission-2": {
        "practice": [
            ["说整体结构", "Two planetary sets plus five clutches."],
            ["说一档", "Sun drives carrier, ring locked—lowest speed, most force."],
            ["说三档", "Both clutches engage—the whole set spins as one, 1:1."],
            ["说倒挡", "Carrier locked, sun drives ring in reverse."],
            ["说空挡P挡", "Clutch stands ready; Park adds a pawl."]
        ],
        "pitfalls": [
            ["Think one clutch per gear.",
             "Clutches switch which parts are input or locked.",
             "离合切换传动路径。"],
            ["Expect all gears to feel the same.",
             "Each gear changes which part is held and driven.",
             "每个档位路径不同。"],
            ["Forget the lock-up clutches.",
             "They hold parts still to change the ratio.",
             "锁止离合固定部件。"],
            ["Assume more gears mean new physics.",
             "More gears just add more planetary sets.",
             "更多档位更多齿轮组。"],
            ["Skip Park's parking pawl.",
             "It stops the car rolling on slopes.",
             "P挡有驻车锁止。"]
        ],
        "shifts": [
            ["说档位只会说 gear",
             "用 power path（传动路径）、input clutch（输入离合）、lock-up clutch（锁止离合）"],
            ["说行星齿轮只会说 planetary",
             "用 Simpson gearset（辛普森齿轮组）、Ravigneaux gearset（拉维尼奥齿轮组）、shared carrier（共用行星架）"],
            ["说传动只会说 drive",
             "用 1:1 ratio（1比1传动比）、reverse output（反向输出）、compact structure（紧凑结构）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：4E T1四速自动变速箱结构、一前一后两组行星齿轮组和五组离合片、输入端的离合决定谁输入、锁止离合把蓝轴上的部件锁死、一档低档位离合和低倒档离合咬合、后太阳轮变输入端外齿圈锁住行星架输出、最小带最大速度最小发力最大、二档松低倒档锁二四档、前太阳轮锁住外齿圈加入驱动行星架转速更快、三档锁定离合全撤两组输入离合同时锁上、行星齿轮被夹在中间无法自转整个组一体旋转1比1传动比、四档只和档位离合连接锁二四档离合、前太阳轮锁死前行星架驱动前外齿圈大带中速度放大、倒档连接倒档离合锁低倒档、前行星架锁住太阳轮驱动、行星架不动太阳轮顺时针行星轮逆时针带动外齿圈反转、输入输出方向相反、空挡和P挡一样一组离合待命咬合、P挡后方多一个防溜车锁止机构、8速9速10速无非用更多行星齿轮组、辛普森两组共用行星架、拉维尼奥两组共用一个太阳齿轮、原理的根依然是行星齿轮组本身等。"
    },
    "manual-transmission-1": {
        "practice": [
            ["说变速箱目的", "Change speed to match the engine's narrow rev range."],
            ["说齿比", "Ratio = driven teeth ÷ driving teeth = speed drop = torque boost."],
            ["说一档", "3.643 ratio—slow wheels, huge launch force."],
            ["说一死一活", "Each pair has one fixed and one loose gear."],
            ["说同步器", "Sleeve and hub lock loose gears to the shaft."],
            ["说同步原理", "Cone friction syncs speeds before the sleeve locks."]
        ],
        "pitfalls": [
            ["Think one gear pair does all work.",
             "Six pairs mesh on two shafts in a complementary layout.",
             "齿轮互补排列。"],
            ["Shift without syncing.",
             "Mismatched speeds shatter gears.",
             "转速不同会打齿。"],
            ["Rev the engine forever in first gear.",
             "Engine revs high while wheels crawl—fine only briefly.",
             "一档只用于起步。"],
            ["Ignore the reverse layout.",
             "Each gear pair keeps one free gear to avoid lockup.",
             "一死一活防卡死。"],
            ["Forget the cone's oil-wiping job.",
             "It clears the oil film before friction sync.",
             "锥面先刮油膜。"]
        ],
        "shifts": [
            ["说齿轮只会说 gear",
             "用 tooth count（齿数）、contact point（接触点）、gear pair（齿轮组）"],
            ["说换挡只会说 shift",
             "用 synchronizer（同步器）、sleeve and hub（结合套与花键毂）、cone friction（锥面摩擦）"],
            ["说动力只会说 power",
             "用 drive gear（驱动齿轮）、driven gear（从动齿轮）、spinning in place（空转）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：2018本田思域Si六速手动变速箱、切开壳体再组装回去展示换挡内部样子、变速箱主打变速改变速度、小齿轮带大齿轮速度降低、大齿轮带小齿轮速度变大、发动机正常转速区间1000到6000转、不变速直接连轮子车速有限、一档齿比3.643被驱动齿轮是驱动齿轮3.643倍、接触点一个齿带一个齿以相同线速度推进、小齿轮转3.643圈大齿轮才转一圈、转速降低3.643倍、一档3000转到轮子274-1647转、一档踩油门转速声嘶力竭车速才20多、一档不仅变速还变矩、100牛米小齿轮半径一米作用100牛、大齿轮半径3.643米乘100牛得364.3牛米、扭矩放大3.643倍、齿比是从动轮主动轮半径比周长比齿数比、起步用齿比最大一档、二档到六档驱动齿轮越来越大被驱动越来越小、齿比一路减小速度越来越高扭矩越来越小、超车降档用大扭矩快速提速、6组齿轮装两根轴、输入轴一二档定死三四五六活动、输出轴一二档活动三四五六定死互补、动力路线发动机带动输入轴、固定的齿轮带动输出轴活动的齿轮空转、动力止于空转齿轮、用几档就把那档位活动的齿轮定死、同步器以结合套和花键毂为中心两侧对称滑块卡环同步环、结合套套在花键毂外滑动锁死左右档位齿轮、花键毂里圈和轴卡死、结合套外侧和档位齿轮小斜齿套上、轴卡花键毂花键毂卡结合套结合套卡档位齿轮、换挡前空转二档齿轮1442转输出轴823转、直接锁死会把齿轮打掉、同步环锥面切润滑油膜靠摩擦同步转速、转速同步结合套再划过去锁死换挡顺畅等。"
    },
    "manual-transmission-2": {
        "practice": [
            ["说拨叉", "Forks slide the synchronizers to pick gears."],
            ["说挡杆对应", "Side-to-side picks a fork; up-down engages the gear."],
            ["说先同步再锁死", "Sync speeds first, then lock the gear."],
            ["说尾牙", "The final drive reduces speed one last time."],
            ["说改装尾牙", "Bigger ratio boosts torque everywhere but cuts top speed."],
            ["说倒挡", "No synchro, straight-cut teeth, must stop first."]
        ],
        "pitfalls": [
            ["Select reverse while moving.",
             "Without a synchro it grinds immediately.",
             "倒挡必须停稳挂。"],
            ["Assume the final drive is optional.",
             "Without it, gear ratios can't fit the shafts.",
             "尾牙是最后一道减速。"],
            ["Fit a huge final drive to a powerful engine.",
             "It just spins the tires—a waste.",
             "大尾牙配强动力会打滑。"],
            ["Expect the loose gear to stay still.",
             "The fixed gear on the other shaft spins it anyway.",
             "空转齿轮仍被带着转。"],
            ["Shift without letting the cone sync first.",
             "Speed mismatch grinds the gears.",
             "先同步再咬合。"]
        ],
        "shifts": [
            ["说换挡只会说 shift",
             "用 shift fork（拨叉）、sleeve slides（结合套滑动）、cone ring（同步环）"],
            ["说减速只会说 reduce",
             "用 final drive（主减速器）、tail tooth（尾牙）、final ratio（中传比）"],
            ["说改装只会说 modify",
             "用 upgrade the ratio（改装齿比）、trade speed for punch（以速换力）、tire slip（轮胎打滑）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：拨叉很像插板负责左右拨动同步器、分别卡在各自结合套上总共有三个、空挡时所有拨叉都在同步器最中间位置、没有档位齿轮被锁死所有齿轮空转、挡杆铁块在凹槽里来回游动在三个拨叉之间待命、往上推挂一档拨叉背往这边顶同步器和一档齿轮结合、往下推挂二档、停留中间推三档四档、装回去后两个连杆机构通过缆线连着、切开壳体窗口装上小摇柄模拟发动机输入、推进五档五档齿轮被同步器定死动力传到输出轴、六档齿轮被输入轴固定齿轮带着空转转速不同、换六档结合套先把同步环压上去锥面摩擦快速把速度带下来、先同步再彻底锁上、尾牙学名主减速器、最早汽车纵置后驱尾牙在两个后轮中间所以叫尾牙、主减速器说明作用靠它减速、发动机动力经过档位后转速过快扭矩太小、一档到六档齿比都太小、保持较小齿比最后再过尾牙中传比4.105、转速再减4.105倍扭矩再增4.105倍、一档3000转除3.643再除4.105轮上201转23540R28轮胎每小时24公里、扭矩200牛米翻3.643再翻4.105到轮上2991牛米除半径0.32米驱动力9340牛、二档351转42公里1708牛米、改装尾牙从4.105改4.5所有档位扭矩提高车速同比减小、尾牙太大一档用不上轮胎直接打滑、改大尾牙针对发动机动力小的车、动力超大的车要改小尾牙防止打滑、倒挡单独小轴齿轮一直和输入轴啮合、没有同步器直接卡死所以要停稳挂、直齿设计噪音大倒车有嗡嗡声等。"
    },
    "engine-cooling": {
        "practice": [
            ["说冷却部件", "Water pump, thermostat, radiator, fan, expansion tank."],
            ["说大小循环", "Small loop warms the engine; big loop cools it."],
            ["说节温器", "Its opening switches between loops."],
            ["说副水箱", "Expansion tank stores and returns coolant."],
            ["说暖风水箱", "Coolant routed through a heater core becomes cabin heat."],
            ["说故障诊断", "Cold top hose = thermostat; both hot = fan."]
        ],
        "pitfalls": [
            ["Check coolant only at the main tank.",
             "Look at the expansion tank, which has the marks.",
             "常规检查看副水箱。"],
            ["Blast the heater at cold start.",
             "It steals the little heat the engine just made.",
             "冷启动开暖气拖慢热机。"],
            ["Ignore the thermostat.",
             "Stuck closed and the engine overheats in the small loop.",
             "节温器卡死会过热。"],
            ["Blame the fan in winter.",
             "Cold air cools the radiator even without it.",
             "冬天风扇坏了影响小。"],
            ["Mix up the two temperature sensors.",
             "One reads engine heat; one reads radiator-out coolant.",
             "两个水温传感器别搞混。"]
        ],
        "shifts": [
            ["说冷却只会说 cool down",
             "用 small loop（小循环）、big loop（大循环）、thermostat opening（节温器开度）"],
            ["说故障只会说 problem",
             "用 stuck closed（卡死关闭）、forced cooling（强制冷却）、overheat（过热）"],
            ["说检查只会说 check",
             "用 expansion tank（膨胀水箱）、coolant level（冷却液液位）、temp sensor（水温传感器）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：冷却系统怎样运行、哪些部分故障以什么形式表现、发动机前端固定水泵、液轮在发动机内部滑轮在外部、由曲轴皮带带动是循环动力来源、节温器通过温度控制开关的法门、决定大循环还是小循环、冷却水箱在车头、上下两根粗水管滚烫冷却液从上面进下面回、车开起来撞风给冷却液降温、堵车没风温度传感器命令风扇启动强制撞风、副水箱膨胀水箱高温膨胀引流一部分储存、熄火降温收缩吸回、主水箱液位永远满副水箱液位随温度浮动、常规检查看副水箱有最高最低液位标识、冷启动只有水泵运行内部循环小循环、一点水很快烧到80多度、节温器打开进入大循环、水箱通过撞风降温堵车就开风扇、水温传感器不止一个车内仪表盘读的是发动机钢体上的传感器、水箱下方传感器检测冷却完的水温、大循环保证不高温小循环保证不低温、最佳工作温度80到90度、节温器一关只要烧缸里一点水比烧整个系统快得多、暖风水箱从冷却系统接两根小管子、加鼓风机一吹车内暖气就这么来、冬天刚启动没暖气越开最大来得越慢、刚烧起来的热量被吹跑热机更慢、故障案例一水温120度上水管不烫手节温器卡在关闭位置、保持小循环大循环走不了肯定过热、案例二上水管下水管都烫手风扇问题、风扇坏了或信号没给过来、冬天风扇坏了外界温度足够低不需要帮忙等。"
    },
    "clutch-principle": {
        "practice": [
            ["说离合含义", "Disengage separates engine and gearbox; engage joins them."],
            ["说三大件", "Flywheel, clutch disc, pressure plate."],
            ["说膜片弹簧", "Depress the center to tilt the plate back and disengage."],
            ["说半联动", "Partial engagement eases the car into motion."],
            ["说踩离合异响", "Pilot bearing rubs when speeds differ."]
        ],
        "pitfalls": [
            ["Hold the clutch on hills.",
             "Use the handbrake—riding the clutch wears it out.",
             "坡道别用离合驻车。"],
            ["Dump the clutch at launch.",
             "Half engagement avoids a violent jerk.",
             "起步要半联动。"],
            ["Shift while the clutch grinds.",
             "Ease off power before changing gears.",
             "换挡先松劲。"],
            ["Ignore clutch-pedal whine.",
             "It points to a worn pilot bearing.",
             "嗡嗡响查定位轴承。"],
            ["Think clutch wear is normal forever.",
             "Proper use and handbrake habits extend its life.",
             "正确使用延长寿命。"]
        ],
        "shifts": [
            ["说离合器只会说 clutch",
             "用 disengage（分离）、engage（结合）、half engagement（半联动）"],
            ["说零件只会说 part",
             "用 flywheel（飞轮）、pressure plate（压盘）、diaphragm spring（膜片弹簧）"],
            ["说故障只会说 fault",
             "用 pilot bearing（定位轴承）、relative motion（相对运动）、wear out（磨损）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：离合器工作原理和常见故障、离是把发动机和变速箱分离合是结合、骑山地车换挡脚上松一下劲、不松劲换挡听到链条齿轮磨损声、灰色飞轮黄褐色离合器片紫色压盘、绿色分离轴承离合叉、离合器片外圈特殊摩擦材料、一边压飞轮一边压压盘、飞轮固定在发动机端变速箱输入轴插进来、输入轴一头定位轴承一头分离轴承两侧自由转动、中间带齿离合器片孔内带齿套上成一体转动、把离合器片用力压到飞轮上就合上松手分离、压盘和飞轮螺丝固定、中间像爪子的是膜片弹簧、压膜片弹簧蓝色部分向后移动、两个支点固定压下去蓝色翘起来松手顶回去、现实中压膜片弹簧的是绿色分离轴承、踩离合踏板液压往前顶风梦推离合叉推分离轴承、分离状态正是手动变速箱换挡时机、脚一松风梦缩回分离轴承被膜片弹簧弹回、压盘把离合片紧紧压在飞轮上飞轮和离合片合为一体、动力通过离合片传到变速箱、半联动是压盘压上去又没全压上去、起步第一次咬合要有半联动先带速度再完全咬合否则闯动、这种半联动不可避免属正常使用、上坡停车靠半联动不靠手刹过度磨损离合器片、离合踩到底嗡嗡响松开没异响、问题在支撑输入轴前端的定位轴承、不踩离合飞轮和输入轴同步转动轴承内外圈无相对运动没异响、踩到底转速不同内外圈相对运动异响出现等。"
    },
    "car-window-film": {
        "practice": [
            ["说三件事", "Shading, heat rejection, and UV are separate."],
            ["说TSER", "Check the official total solar energy rejection number."],
            ["说吸热反射", "Ceramic absorbs; metal reflects."],
            ["说金属膜缺点", "It blocks signals—pair ceramic front with metal sides."],
            ["说寿命", "Adhesive decides bubbles; substrate decides clarity."],
            ["说性价比", "30% to 50% is a big feel; beyond that costs soar."]
        ],
        "pitfalls": [
            ["Pick film by how dark it is.",
             "Darkness only means shading, not heat rejection.",
             "黑不代表隔热。"],
            ["Trust the heat-lamp demo.",
             "It tests a narrow IR band—a marketing trick.",
             "烤灯测试是营销。"],
            ["Follow single parameters like 90% IR.",
             "Trust the official TSER instead.",
             "认准TSER总阻隔率。"],
            ["Buy unknown white-label brands.",
             "Check the manufacturer's association list.",
             "避开白牌贴牌货。"],
            ["Roll windows down right after install.",
             "Wait 3-7 days for the adhesive to set.",
             "贴膜后别急着升降窗。"]
        ],
        "shifts": [
            ["说贴膜只会说 window film",
             "用 heat rejection（隔热）、TSER（总太阳能阻隔率）、shading（遮光）"],
            ["说测试只会说 test",
             "用 heat-lamp demo（烤灯测试）、selective testing（选择性测试）、official spec（官方参数）"],
            ["说隔热原理只会说 insulate",
             "用 ceramic particles（陶瓷颗粒）、magnetron sputtering（磁控溅射）、infrared（红外线）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：9块9窗膜1000块热销款13000块旗舰款真的有区别吗、白天空调开最大胳膊晒得刺痛车内如蒸笼、晚上变睁眼瞎看不见没开灯的小电驴、这不叫贴膜叫花钱找罪受、膜颜色越黑只代表遮光效果不错、遮光隔热防晒是三件事、太阳光约46%可见光50%红外线热量大头来自可见光和红外线、黑得像锅底没有红外组合技术只能挡可见光、烤灯测试红外线阻隔率90%是利用红外线漏洞的营销、烤灯能量集中800-1500nm只是太阳光一小部分、相当于只考选择题满分其他题全空、劣质吸热膜吸热量小晒一会儿漏馅、不到半年隔热效果断崖式下跌、开空调依然闷热根本原因、劣质膜工业胶水玻璃晒五六十度疯狂挥发甲醛苯有毒气体、打开车门闻到刺鼻酸臭味、4S店送免费贴膜要问品牌型号、能搜到正常官网一般不会太差、普通人买膜看两点认准官方TSER总太阳能阻隔率、不要被单一参数迷惑、TSER是国际窗膜协会认可综合衡量隔热唯一标准、前挡透光率不得低于70%国标强制、同TSER 50%价格差一倍、膜至少五层结构中间三层影响价格、吸热膜反射膜两派、陶瓷膜氧化烟芯氮化钛陶瓷颗粒嵌入PET基材、热容量大扛两三小时爆晒、陶瓷不挡信号不氧化、金属膜磁控溅射金银钛一层层打上像透明金属镜子、银反射率高但接触硫化物氧化发黑、钛耐腐蚀用钛把银夹中间三明治、三层镀银工艺是行业天花板、金属膜屏蔽电磁信号、前挡陶瓷侧后挡金属、注意别把前挡贴满留出小黑点区保信号、安装胶层决定起不起泡、差胶几年暴晒加加热丝烘烤大面积鼓包、换膜时得用铲子铲加热丝全废、拒止层PET基材决定看出去晕不晕、好膜几年透亮差膜像毛玻璃、白牌非标品尽量不要碰、阻隔率30%提到50%空调28度到24度、再往上多花几千只多10%体感微乎其微、查国际窗膜协会制造商认证12个制造商26个品牌、伊士曼威固龙膜酷破光学圣科、3M多层光学膜、圣戈班量子膜高透光、马迪克收强生、航天山由央企代工山由性价比高、土诺飞尊膜、前排车窗选浅色、后排无所谓、千元以内全系陶瓷膜、航天山由摘星摘星Pro前挡阻隔率50%陶瓷膜600起、强生冰清二代859前挡41%、3M博径26%、千元到两千航天山由懒约61%、强生冰清二代全车陶瓷前挡53%侧后65%、量子膜M9前陶瓷后金属、圣佳NZ80陶瓷光学级PET、尊膜紫耀70多层光学膜不挡信号、微固轻粤加云畅、3000以上前挡阻隔率低于50%直接Pass、贴膜三分膜七分贴、贴膜后3到7天不要升降车窗、一个月内不要开后挡加热丝、一周内微小水泡正常硬币大小气泡是施工失误要求重贴等。"
    },
    "car-chassis-suspension": {
        "practice": [
            ["说悬挂第一要义", "Keep tires glued to the road—safety first."],
            ["说两大派系", "Independent vs. beam axle."],
            ["说麦弗逊双叉臂", "MacPherson: simple, cheap; wishbone: precise, costly."],
            ["说多连杆", "3-5 arms with bushings give the most tuning freedom."],
            ["说磁铁测试", "Sticks = steel; falls = aluminum."],
            ["说空悬为何流行", "EV weight demands pressure-adjustable suspension."]
        ],
        "pitfalls": [
            ["Judge a chassis by the parts list alone.",
             "It's 30% hardware, 70% tuning.",
             "底盘七分靠调教。"],
            ["Assume soft = comfortable.",
             "Too soft means float, roll, and motion sickness.",
             "太软反而晕车。"],
            ["Trust the 'multi-link' label blindly.",
             "Thin chopstick links behave far worse.",
             "当心筷子悬架。"],
            ["Buy air suspension without checking maintenance.",
             "Air bags age and replacements are pricey.",
             "空悬维护成本高。"],
            ["Rely only on videos and tests.",
             "The ultimate test is a real test drive.",
             "终极判断是试驾。"]
        ],
        "shifts": [
            ["说悬挂只会说 suspension",
             "用 independent suspension（独立悬挂）、beam axle（非独立）、torsion beam（扭力梁）"],
            ["说调教只会说 tune",
             "用 tuning freedom（调教自由度）、chassis tuning（底盘调教）、70% tuning（七分调教）"],
            ["说配置只会说 spec",
             "用 unsprung mass（簧下质量）、subframe（副车架）、active suspension（全主动悬挂）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：120时速撑住身家性命的是四个轮胎接触面和底盘悬挂、一旦闪失可能就重开了、花大几万选装冰箱彩电大沙发却对底盘一无所知、底盘不像零百加速被直接量化、后天调教作用远大于堆料、悬挂第一要义是保命、死死按住轮胎让轮胎贴合地面、轮胎离地抓地力瞬间归零打滑失控、底盘是三大件之一悬挂归属底盘系统、独立非独立两大派系、多连杆大于双叉臂大于麦弗逊大于扭力梁、前三者是独立悬挂扭力梁是非独立、独立悬挂左右轮互不干涉、非独立像同一条绳上的蚂蚱、前轮需要转向基本独立悬挂后轮非独立凑合、麦弗逊结构最简单一根减震支柱下摆臂、省钱省空间普及率高、支柱既扛车身重量又顶横向撕扯力、逼近操控极限暴露侧向支撑不足过弯侧倾明显重刹点头、双叉臂上下两把叉子死死嵌入车轮、有效分担侧向力减震器专注垂直方向、操控精准F1也用、代价是昂贵造价和侵占发动机舱空间、多连杆本质是把上下两把叉子打散拆成3-5根独立连杆、每个连接点有橡胶衬套缓冲自带滤震、每根连杆有独立KPI各司其职、调教自由度极高、缩水多连杆三根细杆筷子悬架动态表现天差地别、扭力梁像柔韧扁担能吸收路面震动、几乎不占底盘空间把空间让给后排后备箱、经济型家轿最爱、底盘三分靠堆料七分靠调教、法系车能把扭力梁调出贴地飞行质感、静态观察底盘平整度好底盘有大面积护板、带磁铁吸摆臂吸住是钢吸不住是铝、铝合金轻30%-40%降低簧下质量、留意完整前后全框式副车架像金属外骨架、隔离路面震动噪音、成本轻松突破5000块、终极杀招永远是线下试驾、底盘软就是舒适硬就是运动是误区、太软起步抬头过弯晃容易晕车、太硬颠人疼也不叫运动、优秀的运动底盘保留清晰路感同时化解没必要冲击、麋鹿飞坡测试考验极限性普通人日常开不到那么大强度、飞坡稳只能证明极限操控好未必日常高级、10万以内前麦弗逊后扭力梁试驾压井盖、10-20万前麦弗逊后多连杆留意甩尾感、20万以上空悬MRC别过度迷信、国产电车卷空悬被物理特性逼出来的、大电池包两三吨传统螺旋弹簧不够用、调太软过弯托底伤电池调太硬太颠、空气悬挂根据载重自动调气压、本土供应链突破成本从一万二降到五千、单枪空悬高度软硬绑死双枪以上才能解耦独立调节、空悬弹风本质橡胶气囊5年10万公里故障高发期、全主动悬挂独立动力源四个电磁电机带避震器、过坑前主动施加相反方向力把轮子顶回去、刹车不点头过弯不侧倾、底盘技术演变是响应速度的生死时速、被动悬挂听天由命全主动悬挂一毫秒不用、物理定律从未改变底盘悬挂的物理极限就是生命的底线等。"
    },
    "standing-longjump": {
        "practice": [
            ["说起跳", "Don't go backward—go upward."],
            ["说摆臂", "Keep arms straight to swing the body."],
            ["说落地", "Push legs forward instead of spreading wide."],
            ["说视线", "Look forward, not down."]
        ],
        "pitfalls": [
            ["Lean backward on takeoff.",
             "Drive your weight upward.",
             "起跳要向上。"],
            ["Bend your arms when swinging.",
             "Straight arms pull the body further.",
             "摆臂要直臂。"],
            ["Spread legs wide on landing.",
             "Push forward to extend the distance.",
             "落地向前顶。"],
            ["Look down during the jump.",
             "Forward focus keeps momentum.",
             "视线向前。"]
        ],
        "shifts": [
            ["说跳远只会说 long jump",
             "用 takeoff（起跳）、landing（落地）、forward momentum（向前冲劲）"],
            ["说动作只会说 move",
             "用 straight-arm swing（直臂摆动）、push forward（向前顶）、look forward（向前看）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：别向后要向上、别去避要直臂、别去宽要顶宽、别向下要向前、关注我学习更多知识等。"
    },
    "waterproof-hiking-shoes": {
        "practice": [
            ["说选择逻辑", "It depends on where you go and what you do."],
            ["说涉水场景", "Stream crossings favor quick-drying non-waterproof."],
            ["说冷湿场景", "Cold, wet, no deep wading favors waterproof."],
            ["说一双鞋的选择", "Non-waterproof covers 90% of scenarios."],
            ["说袜子策略", "Always pack a spare and waterproof socks."]
        ],
        "pitfalls": [
            ["Buy waterproof for summer streams.",
             "It traps water and dries far slower.",
             "涉水选防水会闷水。"],
            ["Ignore breathability.",
             "The membrane seals but suffocates hot feet.",
             "防水牺牲透气。"],
            ["Buy one pair and expect everything.",
             "Pair the shoe with sock strategies.",
             "鞋配袜子策略。"],
            ["Choose waterproof in sleet-free heat.",
             "Hot, dry, sweaty days punish boots.",
             "炎热旱脚别防水。"],
            ["Forget spare socks.",
             "They cover the last 10% of scenarios.",
             "备袜兜底。"]
        ],
        "shifts": [
            ["说防水鞋只会说 waterproof shoes",
             "用 membrane boots（防水膜鞋）、breathable shoes（透气鞋）、quick-dry（速干）"],
            ["说选鞋只会说 choose shoes",
             "用 scenario-based choice（场景选择题）、stream crossings（涉水过溪）、sleet（雨夹雪）"],
            ["说装备只会说 gear",
             "用 spare socks（备用袜）、waterproof socks（防水袜）、dry time（干燥时间）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：土布鞋该穿防水的还是不防水的、两拨人吵得不可开交、一拨认为必须整双雨鞋出门没防水膜像没穿裤子、另一拨认为防水膜像裹塑料布捂脚糟糕、但这并非非此即彼问题而是一道选择题、取决于去什么地方做什么、两者各有各的好也各有各的坑、夏天涉水过溪觉得需要防水鞋实际上可能适得其反、频繁涉水过河非防水鞋往往是更好选择、过溪湿了不怕走几步很快就干、实验数据同一款鞋湿透后非防水干燥速度比防水快很多、防水鞋内部进水晾干时间长得多大概相差两个段时、春末夏天干旱炎热长线旱脚选非防水、防水膜能挡雨水湿气但透气性大打折扣、早春深秋冬天偏冷偏潮路面积雪薄冰冻土水坑选防水鞋、低温脚汗没那么严重保住温度比透气重要、湿雪雨加雪魔法攻击必须上防水鞋、防水鞋雪泡加一样魔化、只想买一双徒步鞋非防水覆盖90%场景、剩下10%用备用袜子或防水袜扛过去、无论选什么鞋都别忘了带双备用袜子和防水袜、平凡过溪选非防水、炎热旱脚选非防水、还冷湿潮但不深涉水选防水、雨加雪选防水、没有一双鞋能让你永远不失脚但总有一种智慧能让你永远走下去等。"
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
