#!/usr/bin/env python3
"""批23：为10篇视频生成完整场景英译JSON（含场景/练习/避坑/思维转变/生词）。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

ARTICLES = {}

ARTICLES["at-transmission-1"] = {
    "title_zh": "AT自动变速箱是怎么传动的？【上集】",
    "title_en": "How Does an AT Automatic Transmission Work? (Part 1)",
    "duration": "11:42",
    "topic": "汽车 · AT变速箱",
    "scenes": [
        {"id": "s1", "scene_zh": "齿轮变速的原理", "scene_en": "How Gears Change Speed", "time": "00:00",
         "context": "变速箱变速的根就是两个尺寸不同的齿轮：小齿轮带大齿轮速度减小但力气变大，大齿轮带小齿轮速度变大但力气变小。",
         "sentences": [
            ["变速箱中的变速，根就在两个尺寸不同的齿轮。", "A transmission's job comes down to two gears of different sizes.", "different-sized gears（不同尺寸的齿轮）"],
            ["小齿轮带着大齿轮转，大齿轮的转速就一定会减小。", "A small gear driving a big gear slows the big one down.", "drive（带动）"],
            ["但速度减小的同时，它会变得更加有力气。", "But as speed drops, the turning force grows.", "turning force（扭矩）"],
            ["反过来大齿轮带小齿轮，速度变大但力气变小。", "Reversed, a big gear driving a small one raises speed but cuts force.", "reverse（反过来）"]
         ]},
        {"id": "s2", "scene_zh": "用山地车理解齿比", "scene_en": "Gear Ratios via a Mountain Bike", "time": "01:28",
         "context": "山地自行车高档位是小带大：踩踏板轻松但车速慢；低档位大带小：踩得费力但提速快。",
         "sentences": [
            ["用最高的挡位去骑，实际上就是一种小带大的情况。", "Riding the highest gear is exactly a small-driving-big setup.", "highest gear（最高挡位）"],
            ["你踩踏板非常轻松，但自行车前进的速度还是很慢。", "You pedal easily, yet the bike creeps along.", "pedal easily（轻松踩踏）"],
            ["低档位大带小，你踩起来非常吃力，但速度能上来很快。", "In the lowest gear, pedaling is hard work but speed builds fast.", "hard work（吃力）"]
         ]},
        {"id": "s3", "scene_zh": "齿比与传动比", "scene_en": "Gear Ratio and Drive Ratio", "time": "03:26",
         "context": "齿比（传动比）就是从动轮和驱动轮的尺寸比值；齿轮尺寸和齿数直接挂钩，所以也叫齿比。",
         "sentences": [
            ["齿比或传动比，指的就是从动轮和驱动轮的尺寸比值。", "Gear ratio is the size ratio of the driven gear to the driving gear.", "driven gear（从动轮）"],
            ["由于齿轮尺寸一般和它有几个齿直接挂钩，所以传动比也叫齿比。", "Since gear size tracks tooth count, drive ratio is also called gear ratio.", "tooth count（齿数）"],
            ["比如从动轮20个齿，驱动轮10个齿，齿比就是2比1。", "20 driven teeth over 10 driving teeth gives a 2:1 ratio.", "2:1 ratio（2比1）"],
            ["经过这一组齿轮，力放大两倍，速度减小两倍。", "Through this pair, force doubles while speed halves.", "force doubles（力翻倍）"]
         ]},
        {"id": "s4", "scene_zh": "汽车为什么要变速", "scene_en": "Why Cars Need Gears", "time": "04:28",
         "context": "自行车变速为了照顾人的感受；发动机不会累，汽车变速是为了照顾车轮的感受——用低档位获得大扭矩起步，用高档位高速巡航。",
         "sentences": [
            ["上坡骑车累，挂高档位车速慢但腿省力；要迅速提速就换低档位。", "Uphill, a high gear saves your legs; a low gear gives quick acceleration.", "save your legs（省力）"],
            ["汽车的低档位是小带大，高档位是大带小，和自行车正好相反。", "In cars, low gear is small-driving-big—opposite to a bike.", "opposite（正好相反）"],
            ["发动机不会累，只要给它汽油它就能源源不断输出动力。", "An engine never tires; give it fuel and it keeps delivering power.", "endless power（源源不断的动力）"],
            ["所以汽车的变档机构，是为了照顾车轮的感受。", "So a car's gearing exists to serve the wheels' needs.", "serve the wheels（服务车轮）"]
         ]},
        {"id": "s5", "scene_zh": "档位与推背感", "scene_en": "Gears and Launch Feel", "time": "05:50",
         "context": "一档齿比约3.5:1，力放大3.5倍推背感强但车速慢；档位越高速度越快但力越小，所以高速巡航用高档、超车要降档。",
         "sentences": [
            ["挂着一档油门踩到六七千转，车速才五六十，但特别有力气。", "In first gear, revving to 6-7k RPM barely reaches 50-60 km/h, yet pulls hard.", "pulls hard（动力十足）"],
            ["一档齿比一般在3.5比1左右，力放大3.5倍，速度缩小3.5倍。", "First gear's ratio is about 3.5:1—force multiplied, speed divided.", "ratio of 3.5 to 1（3.5比1）"],
            ["越往高档，驱动齿轮越来越大，到轮上的力越来越小但速度越来越快。", "Higher gears shrink the driven gear, trading force for speed.", "trade force for speed（以力换速）"],
            ["高速巡航用高档位，想迅速超车时降档用低档位。", "Cruise in a high gear, but downshift for quick overtaking.", "downshift（降档）"]
         ]},
        {"id": "s6", "scene_zh": "行星齿轮组的部件", "scene_en": "The Planetary Gearset", "time": "07:21",
         "context": "AT变速箱用行星齿轮组实现变速：太阳齿轮居中，行星齿轮绕它转，行星架把它们架起来，外齿圈包裹在外。",
         "sentences": [
            ["AT自动变速箱采用的结构更加巧妙，占的体积也更小。", "The AT transmission uses a cleverer, more compact structure.", "compact structure（紧凑结构）"],
            ["中间的粉色是太阳齿轮，绿色的三个是行星齿轮。", "The pink sun gear sits at the center; the three green ones are planet gears.", "sun gear（太阳齿轮）"],
            ["橘黄色的三角形是行星架，最外面的褐色部分是外齿圈。", "The orange carrier holds the planets; the brown outer ring surrounds them.", "planet carrier（行星架）"],
            ["行星齿轮被外齿圈和太阳齿轮夹在了中间。", "The planet gears are sandwiched between the ring and sun gears.", "sandwiched（夹在中间）"]
         ]},
        {"id": "s7", "scene_zh": "三部件定一驱一出", "scene_en": "Hold One, Drive One, Output One", "time": "08:10",
         "context": "行星齿轮组主要看三个部件：任意一个固定住，剩下两个转动其中一个，另一个就会被驱动起来。",
         "sentences": [
            ["行星齿轮组运行时，主要看三个部件，不用看行星齿轮本身。", "In operation, watch the three main parts, not the planets themselves.", "main parts（主要部件）"],
            ["三样东西中任意一样固定住，剩下的两样转动其中一个，另一个就会被驱动。", "Hold any one part still; turning one of the rest drives the other.", "hold it still（固定住）"],
            ["按住太阳轮转行星架，行星轮自转带动外齿圈同向转，就是行星架驱动外齿圈。", "Hold the sun, turn the carrier, and the planets spin the ring the same way.", "spin the ring（带动外齿圈）"]
         ]},
        {"id": "s8", "scene_zh": "倒挡的原理", "scene_en": "Reverse Comes from Holding the Carrier", "time": "09:01",
         "context": "按住行星架转太阳轮，行星轮只能原地自转，带动外齿圈反向旋转——这就成了倒挡。",
         "sentences": [
            ["按住行星架，顺时针转动太阳齿轮，行星轮只能原地自转。", "Hold the carrier and turn the sun clockwise; the planets just spin in place.", "spin in place（原地自转）"],
            ["顺时针的太阳轮让行星齿轮逆时针转，行星齿轮再带动外齿圈逆时针转。", "The clockwise sun makes planets spin counterclockwise, reversing the ring.", "reverse direction（反转）"],
            ["这样太阳齿轮就驱动着外齿圈反转了，拿来做倒挡再合适不过。", "The sun drives the ring in reverse—perfect for the reverse gear.", "reverse gear（倒挡）"]
         ]}
    ]
}

ARTICLES["at-transmission-2"] = {
    "title_zh": "AT自动变速箱是怎么传动的？【下集】",
    "title_en": "How Does an AT Automatic Transmission Work? (Part 2)",
    "duration": "12:31",
    "topic": "汽车 · AT变速箱",
    "scenes": [
        {"id": "s1", "scene_zh": "变速箱的整体结构", "scene_en": "The Overall Layout", "time": "00:00",
         "context": "这台4E T1四速自动变速箱由前后两组行星齿轮组和五组离合片构成，用离合来切换传动路径。",
         "sentences": [
            ["输入轴永远在转动，输出端最终连接到车轮。", "The input shaft always spins, and the output eventually reaches the wheels.", "input shaft（输入轴）"],
            ["这台四速自动变速箱的主要结构是前后两组行星齿轮组，加上五组离合片。", "This 4-speed AT consists of two planetary gear sets and five clutches.", "planetary gear set（行星齿轮组）"],
            ["连接输入端的离合决定哪个齿轮输入，锁止离合把部件固定住。", "Input clutches pick which gear is driven; lock-up clutches hold parts still.", "lock-up clutch（锁止离合）"]
         ]},
        {"id": "s2", "scene_zh": "一档：最小带最大", "scene_en": "First Gear: Smallest Drives Largest", "time": "01:35",
         "context": "一档时后太阳轮变输入端，后外齿圈被锁住，后行星架输出——最小带最大，速度最小、发力最大。",
         "sentences": [
            ["一档时，低档位离合和低倒档离合咬合，后太阳轮变成输入端。", "In first gear, the low clutch engages and the rear sun gear becomes the input.", "low clutch（低档位离合）"],
            ["外齿圈被锁住不能动，剩下的行星架就变成了输出。", "With the ring locked, the planet carrier becomes the output.", "the output（输出端）"],
            ["尺寸最小的太阳轮驱动尺寸最大的行星架，最小带最大。", "The smallest sun gear drives the largest carrier—smallest driving biggest.", "smallest drives biggest（最小带最大）"],
            ["结果就是速度最小、发力最大，这就是一档的特点。", "The result is the lowest speed and the highest force—that's first gear.", "lowest speed（最低速度）"]
         ]},
        {"id": "s3", "scene_zh": "二档与三档", "scene_en": "Second and Third Gear", "time": "03:04",
         "context": "二档外齿圈加入驱动，行星架转速更快；三档两组离合同时咬合，整个齿轮组1比1直传。",
         "sentences": [
            ["二档时锁住前太阳轮，外齿圈加入进来帮着太阳轮一起驱动行星架。", "In second, the front sun locks and the ring joins the sun to drive the carrier.", "join in（加入驱动）"],
            ["后行星架转速更快一点，速度起来了，出力自然变小。", "The carrier spins faster—speed rises, force falls.", "speed rises（速度提升）"],
            ["三档时两组离合同时咬合，行星齿轮被夹在中间无法自转。", "In third, both clutches engage and the planets can't spin on their own.", "can't self-spin（无法自转）"],
            ["整个齿轮组像一个整体在旋转，就是1比1的传动比。", "The whole set rotates as one—a 1:1 ratio.", "1:1 ratio（1比1传动比）"]
         ]},
        {"id": "s4", "scene_zh": "四档与倒挡", "scene_en": "Fourth Gear and Reverse", "time": "06:22",
         "context": "四档锁住前太阳轮，前行星架驱动前外齿圈，大带小速度放大；倒挡锁住前行星架，太阳轮驱动外齿圈反向输出。",
         "sentences": [
            ["四档锁住前太阳轮，输入驱动前行星架，前外齿圈就是输出。", "In fourth, the front sun locks; the carrier drives and the ring outputs.", "front sun locks（锁住前太阳轮）"],
            ["大的驱动中的，速度放大、出力变小，是典型的高档位特征。", "Big drives medium—speed up, force down: classic high-gear behavior.", "high-gear behavior（高档位特征）"],
            ["倒挡锁住前行星架，输入驱动前太阳齿轮。", "In reverse, the front carrier locks and the sun gear is driven.", "reverse（倒挡）"],
            ["行星架不动、太阳轮顺时针转，外齿圈就逆时针转，输入输出方向相反。", "With the carrier still, a clockwise sun spins the ring backward—input and output oppose.", "opposing directions（方向相反）"]
         ]},
        {"id": "s5", "scene_zh": "空挡与P挡", "scene_en": "Neutral and Park", "time": "08:49",
         "context": "空挡和P挡都让一挡的离合处于待命咬合状态，区别只在P挡多了防止溜车的锁止机构。",
         "sentences": [
            ["空挡和P挡其实一样，都只需要一组离合处于待命状态。", "Neutral and Park are similar—one clutch set stands ready.", "stand ready（待命）"],
            ["在P挡或空挡时，下一步要么一挡起步，要么倒挡倒车。", "From Park or Neutral, the next move is either first gear or reverse.", "next move（下一步）"],
            ["P挡和空挡唯一的区别，是P挡后方多了一个防溜车的锁止机构。", "The only difference: Park adds a parking pawl that stops the car rolling.", "parking pawl（驻车锁止机构）"]
         ]},
        {"id": "s6", "scene_zh": "复杂变速箱的本质", "scene_en": "The Essence of Complex Transmissions", "time": "09:26",
         "context": "8速9速10速变速箱只是用了更多、更复杂的行星齿轮组组合，原理的根依然是同一套。",
         "sentences": [
            ["更复杂的8速9速10速变速箱，无非是用了更多的行星齿轮组。", "8-, 9-, and 10-speed units simply use more planetary gear sets.", "more gear sets（更多齿轮组）"],
            ["辛普森齿轮组是两组行星齿轮共用一个行星架。", "A Simpson gearset pairs two planetary sets sharing one carrier.", "Simpson gearset（辛普森齿轮组）"],
            ["拉维尼奥齿轮组是两组行星齿轮共用一个太阳齿轮。", "A Ravigneaux gearset merges two sets into one, sharing the sun gear.", "Ravigneaux gearset（拉维尼奥齿轮组）"],
            ["不管多复杂，原理的根依然还是行星齿轮组本身。", "No matter the complexity, the root principle stays the same.", "root principle（根本原理）"]
         ]}
    ]
}

ARTICLES["manual-transmission-1"] = {
    "title_zh": "硬核拆解，科普手动变速箱原理【上集】",
    "title_en": "Hardcore Teardown: Manual Transmission Basics (Part 1)",
    "duration": "14:57",
    "topic": "汽车 · 手动变速箱",
    "scenes": [
        {"id": "s1", "scene_zh": "变速的原理", "scene_en": "The Principle of Gearing", "time": "00:36",
         "context": "变速箱主打变速：小齿轮带大齿轮速度降低，大齿轮带小齿轮速度升高；发动机正常工作转速区间有限，所以需要变速箱。",
         "sentences": [
            ["变速箱主打的就是一个变速，改变速度。", "A transmission exists to change speed.", "change speed（变速）"],
            ["小齿轮带大齿轮，大齿轮的速度就降低了。", "A small gear driving a big one slows it down.", "slow it down（降速）"],
            ["发动机正常工作的转速区间很有限，一般每分钟1000到6000转。", "An engine's working rev range is narrow—roughly 1,000 to 6,000 RPM.", "rev range（转速区间）"],
            ["如果不变速，发动机直接连轮子，车速就非常有限。", "Without gearing, engine-to-wheel means a very limited top speed.", "limited top speed（有限的车速）"]
         ]},
        {"id": "s2", "scene_zh": "一档齿比3.643", "scene_en": "First-Gear Ratio 3.643", "time": "01:25",
         "context": "以这台变速箱为例，1档齿比3.643，即被驱动大齿轮齿数是驱动小齿轮的3.643倍，转速被降低3.643倍。",
         "sentences": [
            ["1档的齿比是3.643，被驱动齿轮的齿数是驱动齿轮的3.643倍。", "First gear has a 3.643 ratio: the driven gear has 3.643× the teeth.", "3.643 ratio（3.643齿比）"],
            ["在齿轮接触点上，两个齿轮总是以一个齿带一个齿前进。", "At the contact point, one tooth always drives one tooth.", "contact point（接触点）"],
            ["小齿轮转完3.643圈，大齿轮才够转完一整圈，这样就完成了变速。", "The small gear turns 3.643 times for each turn of the big one—that's the speed change.", "complete one turn（转完一圈）"],
            ["经过一档变速，整体转速降低了3.643倍。", "Through first gear, overall speed drops by a factor of 3.643.", "drop by a factor（降低倍数）"]
         ]},
        {"id": "s3", "scene_zh": "扭矩被放大", "scene_en": "Torque Gets Multiplied", "time": "03:15",
         "context": "一档不仅变速还变矩：发动机输出100牛米，通过齿比3.643后，车轮获得364.3牛米的扭矩，所以起步推背感强。",
         "sentences": [
            ["一档不仅变了速度，而且还变了扭矩。", "First gear changes not just speed but also torque.", "change torque（变矩）"],
            ["假设发动机输出100牛米，作用在接触点上的力是100牛。", "Say the engine puts out 100 N·m—the force at the contact point is 100 N.", "100 N·m（100牛米）"],
            ["大齿轮半径是小的3.643倍，乘上100牛的力，就有了364.3牛米的扭矩。", "With 3.643× the radius, the 100 N yields 364.3 N·m at the wheel gear.", "multiply the radius（半径倍数）"],
            ["来自发动机的扭矩被放大了3.643倍，加速能不猛吗？", "Engine torque multiplied 3.643×—no wonder acceleration feels strong.", "strong acceleration（猛加速）"]
         ]},
        {"id": "s4", "scene_zh": "齿比即转速降低与扭矩放大", "scene_en": "Ratio = Slowdown and Torque Boost", "time": "04:44",
         "context": "齿比是从动轮和主动轮的半径比、周长比、齿数比，它既是转速降低的倍数，也是扭矩放大的倍数。",
         "sentences": [
            ["齿比就是从动轮和主动轮的半径之比、周长之比、齿数之比。", "Gear ratio is the driven-to-driving ratio of radius, circumference, and teeth.", "circumference（周长）"],
            ["这个齿比，就是转速降低的倍数。", "That ratio is exactly how much speed drops.", "speed drop（降速倍数）"],
            ["同时也是扭矩放大的倍数。", "And exactly how much torque multiplies.", "torque boost（扭矩放大倍数）"],
            ["起步用齿比最大的一档，既能匹配低车速，又有最大的扭矩放大。", "First gear matches low launch speed and gives the biggest torque boost.", "launch（起步）"]
         ]},
        {"id": "s5", "scene_zh": "档位越高速度越快", "scene_en": "Higher Gears, More Speed", "time": "05:30",
         "context": "从一档到六档，驱动齿轮越来越大、被驱动齿轮越来越小，齿比一路减小，最高速度越来越高但扭矩越来越小。",
         "sentences": [
            ["从二档到六档，驱动齿轮越来越大，被驱动齿轮越来越小。", "From second to sixth, the driving gears grow and the driven ones shrink.", "drive gear grows（驱动齿轮变大）"],
            ["齿比一路减小，车辆能达到的速度就越来越高。", "The ratio keeps shrinking, so attainable speed keeps climbing.", "attainable speed（可达速度）"],
            ["但车轮能输出的扭矩越来越小。", "But wheel torque keeps shrinking.", "wheel torque（车轮扭矩）"],
            ["超车的时候要降档，用更大的扭矩快速提速。", "Downshift to overtake—use bigger torque for a quick surge.", "overtake（超车）"]
         ]},
        {"id": "s6", "scene_zh": "一死一活的齿轮组合", "scene_en": "One Fixed, One Free Gear", "time": "06:33",
         "context": "6组齿轮装到两根轴上：输入轴1、2档固定其余活动，输出轴3-6档固定其余活动，互补搭配让动力不卡死。",
         "sentences": [
            ["6个档位对应6组不同尺寸的齿轮，分别装到两根轴上。", "Six gears mean six gear pairs mounted on two shafts.", "gear pairs（齿轮组）"],
            ["输入轴上1、2档定死跟轴一体，3到6档都是活动的。", "On the input shaft, 1st and 2nd are fixed; 3rd through 6th are loose.", "fixed vs loose（定死与活动）"],
            ["输出轴上1、2档是活动的，剩下的3、4、5、6都是定死的。", "On the output shaft it's reversed—1st and 2nd are loose, the rest fixed.", "reversed（互补相反）"],
            ["两根轴互补，才能正常啮合，不会互相卡死。", "The complementary layout lets the shafts mesh without locking up.", "mesh without locking（正常啮合）"]
         ]},
        {"id": "s7", "scene_zh": "动力传递路线", "scene_en": "The Power Path", "time": "08:00",
         "context": "发动机带动输入轴，输入轴上固定的齿轮带动输出轴上活动的齿轮空转，动力止于空转齿轮，输出轴不转。",
         "sentences": [
            ["发动机启动离合结合，连着发动机的输入轴就跟着转起来。", "With the clutch engaged, the input shaft spins with the engine.", "clutch engaged（离合结合）"],
            ["输入轴上1、2档齿轮是死的被带动，但输出轴上1、2档是活动的。", "The fixed 1st/2nd gears spin, but the loose ones on the output shaft don't.", "loose gears（活动齿轮）"],
            ["动力就被空转齿轮给转没了，输出轴根本没有转动。", "The free gears just spin in place—no power reaches the output shaft.", "spin in place（空转）"],
            ["想用几档开，就把那个档位齿轮组中活动的齿轮也定死。", "To use a gear, lock the loose gear in that pair too.", "lock the gear（锁死齿轮）"]
         ]},
        {"id": "s8", "scene_zh": "同步器登场", "scene_en": "Enter the Synchronizer", "time": "09:52",
         "context": "同步器以结合套和花键毂为中心，两侧各有滑块、卡环和同步环，用来把活动的齿轮锁死在轴上。",
         "sentences": [
            ["怎么把活的齿轮定死在轴上？大名鼎鼎的同步器登场了。", "How to lock a loose gear to its shaft? Meet the famous synchronizer.", "synchronizer（同步器）"],
            ["一个同步器以结合套和花键毂为中心，两侧各有滑块、卡环和同步环。", "A synchronizer centers on the sleeve and hub, with blocks, rings, and cones each side.", "sleeve and hub（结合套与花键毂）"],
            ["结合套套在花键毂外面，左右滑动就能锁死左边的或右边的档位齿轮。", "Sliding the sleeve left or right locks the gear on that side.", "slide the sleeve（滑动结合套）"],
            ["花键毂和轴卡死，结合套和花键毂卡死，结合套再伸出去卡死档位齿轮。", "The hub locks to the shaft, the sleeve locks to the hub, and the sleeve bites the gear.", "chain of locks（环环相扣）"]
         ]},
        {"id": "s9", "scene_zh": "同步转速避免打齿", "scene_en": "Syncing Speed Prevents Grinding", "time": "11:37",
         "context": "换挡时，空转齿轮转速和输出轴转速不同，直接锁死会打齿；同步环先通过锥面摩擦把转速同步再锁死。",
         "sentences": [
            ["挂二档前，输出轴转速823转，而空转的二档齿轮是1422转。", "Before shifting to 2nd, the shaft runs at 823 RPM while the loose 2nd gear spins at 1422.", "mismatched speeds（转速不同）"],
            ["直接滑过去把823转的轴和1400多转的齿轮锁死，会把齿轮打掉。", "Locking mismatched speeds instantly would shatter the gears.", "shatter the gears（打齿）"],
            ["同步环的锥面先被推上去，切开润滑油膜，靠摩擦把转速同步。", "The cone ring first wipes the oil film and syncs speeds by friction.", "sync by friction（靠摩擦同步）"],
            ["转速同步了，结合套再划过去锁死，换挡才安全顺畅。", "Once synced, the sleeve slides over and locks—smooth, safe shifts.", "smooth shift（顺畅换挡）"]
         ]}
    ]
}

ARTICLES["manual-transmission-2"] = {
    "title_zh": "硬核拆解，科普手动变速箱原理【下集】",
    "title_en": "Hardcore Teardown: Manual Transmission Basics (Part 2)",
    "duration": "11:50",
    "topic": "汽车 · 手动变速箱",
    "scenes": [
        {"id": "s1", "scene_zh": "拨叉控制同步器", "scene_en": "Forks Move the Synchronizers", "time": "00:00",
         "context": "拨叉像插板一样卡在同步器的结合套上，左右拨动同步器来选择档位。",
         "sentences": [
            ["拨叉很像一个插板，负责左右拨动同步器。", "A shift fork looks like a paddle and slides the synchronizers.", "shift fork（拨叉）"],
            ["它分别卡在各自的结合套上，总共有三个。", "Each fork sits in a sleeve's groove—three in total.", "three forks（三个拨叉）"],
            ["空挡时，所有拨叉都在同步器最中间的位置，没有档位齿轮被锁死。", "In neutral, every fork sits centered and no gear is locked.", "neutral（空挡）"]
         ]},
        {"id": "s2", "scene_zh": "挡杆如何变成拨叉动作", "scene_en": "From Stick to Fork", "time": "00:28",
         "context": "挡杆的左右游走对应选择三组拨叉中的哪一组，上推下拉对应拨叉往哪个档位介入。",
         "sentences": [
            ["挡杆的铁块在凹槽里来回游动，其实是在三个拨叉之间待命。", "The shifter block slides in its gate, choosing among the three forks.", "shift gate（换挡槽）"],
            ["挡杆往上一推，对应的拨叉把同步器推着和一档齿轮结合。", "Pushing the stick up makes the fork engage first gear.", "engage first gear（挂一档）"],
            ["往下推就挂入二档，停留中间再推就是三档或四档。", "Push down for 2nd; stay centered and push for 3rd or 4th.", "stay centered（停留中间）"]
         ]},
        {"id": "s3", "scene_zh": "切开壳体看换挡", "scene_en": "Cutting Open the Case", "time": "02:05",
         "context": "把变速箱壳体切开一个窗口，装上摇柄模拟发动机输入，就能直接看到换挡时内部的实际动作。",
         "sentences": [
            ["把变速箱壳体切开一个窗口，能观察到换挡时实际的内部动作。", "Cutting a window in the case reveals the real shifting motion.", "cut a window（切开口子）"],
            ["我给输入轴装上小摇柄，手摇来模拟发动机的输入。", "A hand crank on the input shaft simulates the engine.", "simulate the engine（模拟发动机）"],
            ["慢动作下可以看到：先挂空挡，同步器和轴一起转，左右档位齿轮空转。", "In slow motion: in neutral, the sync spins with the shaft while side gears freewheel.", "freewheel（空转）"]
         ]},
        {"id": "s4", "scene_zh": "先同步再锁死", "scene_en": "Sync First, Then Lock", "time": "03:39",
         "context": "推进五档后，六档齿轮被输入轴上的固定齿轮带着空转，转速不同；换六档时同步环先把速度带下来再锁死。",
         "sentences": [
            ["推进五档，五档齿轮被同步器定死，动力传到了输出轴。", "Into 5th, the synchronizer locks the gear and power reaches the output shaft.", "reach the output（传到输出轴）"],
            ["六档齿轮被输入轴上的固定齿轮带着空转，因为齿比不同转速也不同。", "The 6th gear freewheels at a different speed because the ratios differ.", "different speeds（转速不同）"],
            ["换六档时，结合套先把黄色同步环压上去，靠锥面摩擦快速把速度带下来。", "Shifting to 6th, the sleeve presses the cone ring to drag speed down by friction.", "drag the speed（把速度带下来）"],
            ["先同步再彻底锁上，完成换挡。", "Sync first, then lock fully—that completes the shift.", "sync then lock（先同步再锁死）"]
         ]},
        {"id": "s5", "scene_zh": "尾牙：主减速器", "scene_en": "The Final Drive", "time": "04:36",
         "context": "尾牙学名主减速器：既说明位置（汽车尾部、一牙一牙）也说明作用（最后再减一次速）。",
         "sentences": [
            ["变速把动力传到车轮前，还差最后一个关键环节——尾牙。", "Before power reaches the wheels, one last key part remains—the final drive.", "final drive（主减速器）"],
            ["尾牙这个名字说清楚了位置和形状，在尾部、一牙一牙的。", "The name 'tail tooth' describes its position at the rear and its toothed shape.", "tail tooth（尾牙）"],
            ["主减速器说明它的作用：主要靠它来最终减速。", "It's called a reducer because its job is the final speed reduction.", "final reduction（最终减速）"],
            ["发动机动力经过档位后转速还是太快、扭矩太小，不足以驱动车辆。", "After the gears, speed is still too high and torque too low to drive the car.", "drive the car（驱动车辆）"]
         ]},
        {"id": "s6", "scene_zh": "中传比4.105", "scene_en": "The 4.105 Final Ratio", "time": "05:50",
         "context": "这台变速箱中传比4.105：不管几档，输出到车轮前转速再减4.105倍，扭矩再增4.105倍。",
         "sentences": [
            ["输入轴小齿轮带动一个特别大的齿轮，这台变速箱的中传比是4.105。", "A small pinion drives a huge gear—this box has a 4.105 final ratio.", "final ratio（中传比）"],
            ["经过变速箱变速变矩之后，转速还要再减掉4.105倍。", "After the gearbox, speed is divided once more by 4.105.", "divide by 4.105（再减4.105倍）"],
            ["扭矩也就要对应增加4.105倍，这才是真正到驱动轮上的最终数值。", "Torque multiplies by 4.105—that's the final number at the drive wheels.", "final torque（最终扭矩）"]
         ]},
        {"id": "s7", "scene_zh": "改装尾牙", "scene_en": "Upgrading the Final Drive", "time": "08:31",
         "context": "改装尾牙就是把齿比从4.105改成4.5，所有档位扭矩同比例放大、加速更猛，但所有档位车速同比减小。",
         "sentences": [
            ["改装尾牙指的就是改装尾牙的齿比，比如从4.105改成4.5。", "Upgrading the final drive means changing its ratio, say from 4.105 to 4.5.", "upgrade the ratio（改装齿比）"],
            ["改一个尾牙，相当于所有档位的扭矩都一起提高了。", "One change boosts torque in every gear at once.", "boost all gears（所有档位提升）"],
            ["代价就是所有档位的车速都会同比减小。", "The cost: top speed in every gear drops by the same factor.", "top speed drops（车速下降）"],
            ["尾牙改大主要针对发动机动力较小的车，牺牲极速换加速。", "A taller final drive suits low-power engines—trading top speed for punch.", "trade speed for punch（以速换力）"]
         ]},
        {"id": "s8", "scene_zh": "倒挡没有同步器", "scene_en": "Reverse Has No Synchro", "time": "10:50",
         "context": "倒挡通过一根单独的小轴实现反向，没有同步器是直齿啮合，所以要停稳后才能挂入，噪音也更大。",
         "sentences": [
            ["倒挡是单独一根小轴，齿轮一直和输入轴啮合转动。", "Reverse uses a separate shaft whose gear always meshes with the input.", "separate shaft（单独小轴）"],
            ["一般的倒挡没有同步器，是齿轮直接卡死。", "Reverse typically has no synchronizer—gears bite directly.", "no synchro（没有同步器）"],
            ["这就是为什么挂倒挡一定要等车停稳，否则马上打齿。", "That's why you must come to a full stop before selecting reverse.", "come to a stop（停车挂挡）"],
            ["倒挡是直齿设计，噪音比较大，所以倒车能听到嗡嗡声。", "Reverse gears are straight-cut, so they whine loudly.", "straight-cut（直齿）"]
         ]}
    ]
}

ARTICLES["engine-cooling"] = {
    "title_zh": "发动机冷却系统原理",
    "title_en": "How the Engine Cooling System Works",
    "duration": "8:02",
    "topic": "汽车 · 冷却系统",
    "scenes": [
        {"id": "s1", "scene_zh": "冷却系统的主要部件", "scene_en": "The Main Components", "time": "00:00",
         "context": "冷却系统由水泵、节温器、水箱、风扇、副水箱等构成，水泵是整个循环的动力来源。",
         "sentences": [
            ["今天来聊一聊汽车发动机的冷却系统是怎样运行的。", "Today we look at how an engine's cooling system works.", "cooling system（冷却系统）"],
            ["发动机前端固定的水泵，是冷却系统循环运行的动力来源。", "The water pump on the engine front drives the whole cooling loop.", "water pump（水泵）"],
            ["水泵由发动机曲轴通过皮带带动，一半在发动机内、一半在发动机外。", "Belt-driven off the crankshaft, the pump straddles the engine block.", "belt-driven（皮带带动）"]
         ]},
        {"id": "s2", "scene_zh": "水箱与风扇", "scene_en": "The Radiator and Fan", "time": "00:55",
         "context": "水箱在车头位置，上下两根水管形成循环；堵车没风时，温度传感器命令风扇强制撞风降温。",
         "sentences": [
            ["冷却水箱在车头位置，上下两根粗水管，一根最上、一根最下。", "The radiator sits up front with two thick hoses—one top, one bottom.", "radiator（水箱）"],
            ["滚烫的冷却液从上面进水箱，从下面流回发动机。", "Hot coolant enters at the top and returns at the bottom.", "coolant（冷却液）"],
            ["堵车没风的时候，温度传感器发现冷却液不够低，就命令风扇启动。", "In traffic, the temp sensor sees coolant still hot and commands the fan on.", "temp sensor（温度传感器）"],
            ["风扇强行给水箱制造撞风降温。", "The fan forces airflow through the radiator to cool it.", "forced airflow（强制撞风）"]
         ]},
        {"id": "s3", "scene_zh": "副水箱的膨胀缓冲", "scene_en": "The Expansion Tank", "time": "02:04",
         "context": "副水箱（膨胀水箱）在冷却液高温膨胀时储存一部分，熄火降温收缩时再吸回，主水箱液位应永远满。",
         "sentences": [
            ["副水箱也叫膨胀水箱，主要功能是引流一部分高温膨胀的冷却液。", "The expansion tank stores coolant that swells from high heat.", "expansion tank（膨胀水箱）"],
            ["发动机熄火冷却液降温收缩时，再从副水箱吸回一部分。", "As the engine cools, coolant contracts and is drawn back from the tank.", "contract（收缩）"],
            ["主水箱液位应该永远都是满的，副水箱液位随温度上下浮动。", "The main tank stays full; the expansion tank level floats with temperature.", "float with temperature（随温度浮动）"],
            ["大家常规检查冷却液液位，看的其实都是副水箱。", "That's why routine coolant checks look at the expansion tank.", "routine check（常规检查）"]
         ]},
        {"id": "s4", "scene_zh": "小循环与大循环", "scene_en": "Small Loop and Big Loop", "time": "02:47",
         "context": "冷车启动时节温器关闭，冷却液只在发动机内部小循环快速升温；温度到80多度节温器打开进入大循环。",
         "sentences": [
            ["发动机冷启动时，唯一运行的部分只有水泵，冷却液在内部循环。", "At cold start, only the pump runs, circulating coolant internally.", "cold start（冷启动）"],
            ["这就是所谓的小循环，一点点水很快就烧到80多度。", "That's the small loop—a little coolant heats to 80°C fast.", "small loop（小循环）"],
            ["达到节温器设计的打开温度，冷却液进入水箱，发动机进入大循环。", "Past the thermostat's set point, coolant flows through the radiator in the big loop.", "big loop（大循环）"],
            ["小循环保证发动机不低温，大循环保证发动机不高温。", "The small loop prevents cold running; the big loop prevents overheating.", "prevent overheating（防高温）"]
         ]},
        {"id": "s5", "scene_zh": "暖风水箱", "scene_en": "The Heater Core", "time": "05:04",
         "context": "暖风水箱从冷却系统接两根小管子引冷却液走一圈，鼓风机一吹就变成车内暖气。",
         "sentences": [
            ["暖风水箱属于冷却系统的一个挂件，原理很简单。", "The heater core is an add-on to the cooling system with a simple idea.", "heater core（暖风水箱）"],
            ["从冷却系统接两根小管子，把冷却液引过来走一圈。", "Two small hoses route hot coolant through it.", "route coolant（引冷却液）"],
            ["在它前面加一个鼓风机一吹，车内的暖气就是这么来的。", "A blower fan over it produces your cabin heat.", "cabin heat（车内暖气）"],
            ["冬天刚启动车辆时暖气来得慢，因为要先等小循环把冷却液烧热。", "Cold mornings have slow heat because the small loop must warm up first.", "slow heat（暖气来得慢）"]
         ]},
        {"id": "s6", "scene_zh": "故障诊断案例", "scene_en": "Diagnosing Faults", "time": "05:53",
         "context": "水温120度但上水管不烫手，是节温器卡在关闭位置；上水管下水管都烫手，是风扇的问题。",
         "sentences": [
            ["水温表120度，但摸上水管一点也不烫手——故障在节温器。", "Temp reads 120°C yet the top hose is cold—the thermostat is stuck closed.", "stuck closed（卡在关闭位）"],
            ["节温器打不开，发动机保持在小循环，大循环水箱流程走不了就过热。", "With the thermostat stuck, only the small loop runs and the engine overheats.", "overheat（过热）"],
            ["上水管和下水管都很烫手，答案就是风扇的问题。", "Both hoses scorching hot points to the cooling fan.", "fan problem（风扇问题）"],
            ["冬天风扇坏了影响不大，因为外界温度足够低给水箱冷却。", "In winter a dead fan matters less—ambient air cools the radiator.", "ambient air（外界空气）"]
         ]}
    ]
}

ARTICLES["clutch-principle"] = {
    "title_zh": "离合器工作原理与故障赏析",
    "title_en": "How the Clutch Works, Plus Faults",
    "duration": "7:59",
    "topic": "汽车 · 离合器",
    "scenes": [
        {"id": "s1", "scene_zh": "离合是什么", "scene_en": "What Clutch Means", "time": "00:00",
         "context": "离是把发动机和变速箱分离，合是把它们结合；就像山地车换挡时要松开脚上的劲。",
         "sentences": [
            ["离指的就是把发动机和变速箱分离，合指的是把它们结合。", "Disengaging separates the engine from the gearbox; engaging joins them.", "disengage（分离）"],
            ["不懂的朋友可以理解为：骑山地车换挡时，脚上需要松一下劲。", "Think of a bike: to shift gears you ease off the pedals for a moment.", "ease off（松劲）"],
            ["不松劲一边发力一边换挡，就会听到链条和齿轮磨损的声音。", "Shifting under full power grinds the chain and gears.", "grind（磨损）"]
         ]},
        {"id": "s2", "scene_zh": "三个关键零件", "scene_en": "Three Key Parts", "time": "00:40",
         "context": "飞轮固定在发动机端，离合器片固定在变速箱输入轴，压盘把离合器片压向飞轮实现结合。",
         "sentences": [
            ["灰色的是飞轮，黄褐色的是离合器片，紫色的是压盘。", "Gray is the flywheel, tan the clutch disc, purple the pressure plate.", "flywheel（飞轮）"],
            ["离合器片外圈有一圈特殊的摩擦材料。", "The disc carries a ring of special friction material.", "friction material（摩擦材料）"],
            ["把离合器片用力压到飞轮上，发动机和变速箱就合上了；一松手就又分离。", "Press the disc against the flywheel and power joins; release and it parts.", "press together（压合）"]
         ]},
        {"id": "s3", "scene_zh": "压盘与膜片弹簧", "scene_en": "Pressure Plate and Diaphragm Spring", "time": "02:29",
         "context": "压盘通过膜片弹簧实现翘起和压回：压下膜片弹簧中心，压盘蓝色部分向后翘起分离；松手就顶回压紧。",
         "sentences": [
            ["压盘和飞轮通过外面一圈螺丝固定在一起。", "The pressure plate bolts to the flywheel around its rim.", "bolt together（螺丝固定）"],
            ["压盘中间像爪子一样的东西是膜片弹簧。", "The claw-like center is the diaphragm spring.", "diaphragm spring（膜片弹簧）"],
            ["压下膜片弹簧，压盘的蓝色部分就向后翘起，离合器分离。", "Depress the spring and the plate's face tilts back—the clutch disengages.", "tilt back（向后翘起）"],
            ["松手后，蓝色部分被顶回去，压盘把离合器片紧紧压在飞轮上。", "Release and the face returns, clamping the disc to the flywheel.", "clamp（压紧）"]
         ]},
        {"id": "s4", "scene_zh": "踩踏板到分离轴承", "scene_en": "From Pedal to Release Bearing", "time": "03:34",
         "context": "踩下离合踏板，液压系统顶动分离叉和分离轴承，推动膜片弹簧实现分离；松脚则恢复结合。",
         "sentences": [
            ["现实中压膜片弹簧的不是手，而是绿色的分离轴承。", "In practice, the green release bearing, not a hand, presses the spring.", "release bearing（分离轴承）"],
            ["你离合踏板踩下去，液压系统往前顶，把分离叉向前推。", "Press the pedal and hydraulics push the release fork forward.", "release fork（分离叉）"],
            ["分离状态就是手动变速箱换挡的时机。", "The disengaged state is the moment to shift gears.", "time to shift（换挡时机）"]
         ]},
        {"id": "s5", "scene_zh": "半联动", "scene_en": "Half Engagement", "time": "05:02",
         "context": "起步时必须半联动，先压一半力把变速箱侧速度带起来再完全咬合，否则会有闯动。",
         "sentences": [
            ["半联动就是压盘压上去了，但又没有全压上去。", "Half engagement means the plate is partly engaged.", "half engagement（半联动）"],
            ["从静止到一挡起步，第一次离合片咬合就要有半联动。", "Pulling away in first gear demands a moment of half engagement.", "pull away（起步）"],
            ["先压一半力把变速箱侧速度带起来，再完全咬合，不然车辆会突然闯动。", "Ease the load in first so the car doesn't jerk.", "avoid jerking（避免闯动）"],
            ["上坡停车靠半联动而不是手刹，会过度磨损离合器片。", "Holding a hill with the clutch instead of the handbrake wears it out.", "wears it out（磨损）"]
         ]},
        {"id": "s6", "scene_zh": "踩离合嗡嗡响", "scene_en": "Whining When Depressed", "time": "06:31",
         "context": "离合踩到底有嗡嗡异响、松开就消失，问题在支撑变速箱输入轴前端的定位轴承。",
         "sentences": [
            ["离合一踩到底就听到嗡嗡嗡的异响，松开又没有了。", "A whine appears when the pedal is fully down and vanishes on release.", "whine（嗡嗡异响）"],
            ["问题出在支撑变速箱输入轴前端的定位轴承。", "The culprit is the pilot bearing that supports the input shaft's front end.", "pilot bearing（定位轴承）"],
            ["不踩离合时，飞轮和输入轴同步转动，轴承内外圈没有相对运动。", "With the clutch engaged, flywheel and shaft spin together, so the bearing is quiet.", "spin together（同步转动）"],
            ["踩下离合后两者转速不同，轴承内外圈有了相对运动，异响就出现了。", "Depressed, their speeds differ and the bearing's races rub—hence the noise.", "relative motion（相对运动）"]
         ]}
    ]
}

ARTICLES["car-window-film"] = {
    "title_zh": "车窗贴膜到底怎么选",
    "title_en": "How to Choose Car Window Film",
    "duration": "15:03",
    "topic": "汽车 · 车窗膜",
    "scenes": [
        {"id": "s1", "scene_zh": "遮光隔热防晒是三件事", "scene_en": "Shading, Insulation, UV: Three Things", "time": "00:00",
         "context": "膜的颜色越黑只代表遮光好，遮光、隔热、防晒是三件事；太阳热量大头来自可见光和红外线。",
         "sentences": [
            ["膜的颜色越黑，只能代表它的遮光效果不错。", "A darker film only means better shading.", "shading（遮光）"],
            ["遮光、隔热、防晒是三件事，别混为一谈。", "Shading, heat rejection, and UV blocking are three separate things.", "heat rejection（隔热）"],
            ["太阳光中约46%是可见光，50%是红外线，热量的大头来自它们。", "Roughly 46% of sunlight is visible and 50% infrared—that's where the heat is.", "infrared（红外线）"],
            ["没有针对红外线的组合技术，能挡住的只有可见光。", "Without infrared tech, a film only blocks visible light.", "block visible light（只挡可见光）"]
         ]},
        {"id": "s2", "scene_zh": "烤灯测试是营销陷阱", "scene_en": "The Heat-Lamp Demo Is Marketing", "time": "01:05",
         "context": "烤灯测试的能量集中在800-1500nm，只是太阳光的一小部分，相当于只考选择题满分其他全空。",
         "sentences": [
            ["烤灯测试说红外线阻隔率90%，是利用红外线漏洞的营销。", "A demo quoting 90% IR rejection exploits a loophole in the test.", "marketing trick（营销陷阱）"],
            ["烤灯能量集中在800到1500纳米，只是太阳光能量的一小部分。", "The lamp's energy sits at 800-1500 nm—a tiny slice of sunlight.", "a tiny slice（一小部分）"],
            ["相当于考试只选选择题满分，其他题全空。", "Like acing the multiple-choice section and leaving everything else blank.", "selective testing（选择性测试）"],
            ["劣质吸热膜晒一会儿就漏馅，隔热效果不到半年断崖式下跌。", "Cheap heat-absorbing films fail fast, losing insulation within months.", "lose insulation（隔热失效）"]
         ]},
        {"id": "s3", "scene_zh": "认准TSER参数", "scene_en": "Trust the TSER Number", "time": "02:55",
         "context": "普通人买膜只看两点：认准官方参数表上的TSER总太阳能阻隔率，不要被任何单一参数迷惑。",
         "sentences": [
            ["普通人买膜应该看什么？就两点，首先认准官方参数表上的TSER。", "What should buyers check? First, the official TSER—total solar energy rejection.", "TSER（总太阳能阻隔率）"],
            ["不要被任何单一参数迷惑，什么红外线阻隔率90%都不要轻信。", "Don't fall for single numbers like 90% IR rejection.", "don't be fooled（别被迷惑）"],
            ["TSER是国际窗膜协会认可的衡量隔热效果的综合标准。", "TSER is the industry-recognized measure of overall heat rejection.", "overall standard（综合标准）"],
            ["重点关注前挡风玻璃，因为有透光率不得低于70%的国标强制要求。", "Focus on the windshield—a national standard demands at least 70% light transmission.", "70% transmission（70%透光率）"]
         ]},
        {"id": "s4", "scene_zh": "吸热膜与反射膜", "scene_en": "Absorbing vs. Reflective Films", "time": "03:47",
         "context": "根据隔热原理分两派：吸热膜靠陶瓷颗粒吸收热量，反射膜靠金属镀层把热量反射出去。",
         "sentences": [
            ["根据隔热原理的不同，窗膜分成两派：吸热膜和反射膜。", "By principle, films split into heat-absorbing and heat-reflecting types.", "absorb vs reflect（吸热与反射）"],
            ["陶瓷膜把氧化烟芯等陶瓷颗粒嵌入PET基材，像海绵一样热容量很大。", "Ceramic films embed nano-ceramic particles—a sponge with huge heat capacity.", "ceramic film（陶瓷膜）"],
            ["金属膜利用磁控溅射技术把金属一层层打在膜上，像一面透明的镜子。", "Metal films sputter metals into layers—a transparent mirror bouncing heat away.", "metal film（金属膜）"],
            ["金属膜会屏蔽电磁信号，前挡建议陶瓷、侧后挡金属。", "Metal films block signals; pair a ceramic windshield with metal side glass.", "block signals（屏蔽信号）"]
         ]},
        {"id": "s5", "scene_zh": "胶层与基材决定寿命", "scene_en": "Adhesive and Substrate Decide Lifespan", "time": "05:42",
         "context": "安装胶层决定会不会起泡，PET基材决定看出去清不清楚，这两点才是容易缩水的地方。",
         "sentences": [
            ["大家只关心隔热性能，但安装胶层和基材才是缩水的重灾区。", "Everyone chases insulation, but the adhesive and substrate are where corners get cut.", "cut corners（缩水）"],
            ["安装胶层决定窗膜以后会不会起泡。", "The adhesive layer decides whether bubbles appear later.", "bubbles（起泡）"],
            ["差胶经过几年暴晒和加热丝烘烤，就会大面积鼓包。", "Poor adhesive bubbles out after years of sun and defroster heat.", "bubbling out（鼓包）"],
            ["PET基材决定眼睛往外看晕不晕，好膜用几年依旧透亮。", "The PET substrate determines clarity—good film stays crystal clear for years.", "clarity（清晰度）"]
         ]},
        {"id": "s6", "scene_zh": "避坑与性价比", "scene_en": "Avoiding Traps on a Budget", "time": "07:39",
         "context": "避开劣质膜最简单的方法是查国际窗膜协会的制造商认证，看品牌是不是有自己工厂的实体企业。",
         "sentences": [
            ["想避开市面上劣质膜，最简单的方法是查国际窗膜协会的制造商认证。", "The easiest way to skip junk is checking the industry association's manufacturer list.", "manufacturer list（制造商认证）"],
            ["成为制造商会员，品牌必须是拥有自有生产线的实体企业，不是贴牌货。", "Members must own real production lines—not white-label re-branding.", "white label（贴牌）"],
            ["窗膜的性能边际递减很严重：阻隔率从30%提到50%体感明显，再往上多花几千块只有10%。", "Diminishing returns: 30% to 50% is a big feel, but beyond that costs soar for tiny gains.", "diminishing returns（边际递减）"],
            ["贴膜是三分膜七分贴，贴完三到七天不要升降车窗。", "Film is 30% product, 70% install—don't roll the windows for 3-7 days.", "30/70 rule（三分膜七分贴）"]
         ]}
    ]
}

ARTICLES["car-chassis-suspension"] = {
    "title_zh": "一期视频看懂底盘悬挂",
    "title_en": "Understand Suspension in One Video",
    "duration": "14:00",
    "topic": "汽车 · 底盘悬挂",
    "scenes": [
        {"id": "s1", "scene_zh": "悬挂的第一要义是保命", "scene_en": "Suspension's First Job: Safety", "time": "00:00",
         "context": "120时速下撑住性命的只有四个轮胎接触面和底盘悬挂；悬挂第一要义是死死按住轮胎让轮胎贴合地面。",
         "sentences": [
            ["高速狂飙时撑住身家性命的，是四个轮胎接触面和底盘悬挂。", "At speed, your life rests on four tire patches and the suspension.", "tire patch（轮胎接触面）"],
            ["悬挂的第一要义是保命，它必须死死按住轮胎贴合地面。", "Suspension's first duty is safety—keeping the tires glued to the road.", "glued to the road（贴合地面）"],
            ["如果轮胎离地，抓地力瞬间归零，汽车分分钟打滑失控。", "Lift a tire and grip hits zero—the car loses control in a flash.", "lose grip（失去抓地力）"],
            ["底盘是汽车三大件之一，悬挂则归属于底盘系统。", "The chassis is one of the big three; suspension is its core subsystem.", "chassis（底盘）"]
         ]},
        {"id": "s2", "scene_zh": "独立与非独立悬挂", "scene_en": "Independent vs. Beam Axle", "time": "01:17",
         "context": "悬挂分两大派系：独立和非独立。独立悬挂左右轮互不干涉，非独立悬挂两个车轮装在同一根梁上跟着一起动。",
         "sentences": [
            ["悬挂整体分两大派系：独立和非独立。", "Suspension splits into independent and non-independent types.", "independent suspension（独立悬挂）"],
            ["独立悬挂左右轮相互独立、互不干涉。", "Independent suspension keeps left and right wheels independent.", "independent wheels（左右独立）"],
            ["非独立悬挂像同一条绳上的蚂蚱，两个车轮按在同一根梁上。", "Beam-axle suspension ties both wheels to one rigid beam.", "beam axle（非独立梁式）"],
            ["大多数家用车前轮需要转向，基本采用独立悬挂。", "Because front wheels steer, most cars use independent front suspension.", "front steering（前轮转向）"]
         ]},
        {"id": "s3", "scene_zh": "麦弗逊与双叉臂", "scene_en": "MacPherson and Double Wishbone", "time": "01:55",
         "context": "麦弗逊结构最简单省钱省空间，但极限工况侧倾点头明显；双叉臂用上下两把叉子分工协作，操控好但造价高。",
         "sentences": [
            ["麦弗逊结构最为简单，仅由一根减震支柱和下摆臂构成。", "MacPherson strut is simplest—one strut and a lower arm.", "MacPherson strut（麦弗逊）"],
            ["麦弗逊的支柱不仅要扛车身重量，过弯时还得顶住横向撕扯力。", "Its strut bears the body weight and lateral loads in corners.", "lateral load（横向力）"],
            ["一旦逼近操控极限，麦弗逊会暴露出侧向支撑不足、点头明显的问题。", "Near the limit, MacPherson shows body roll and brake dive.", "body roll（侧倾）"],
            ["双叉臂通过上下两把叉子死死嵌入车轮，有效分担侧向力。", "Double wishbones clamp the wheel top and bottom, sharing lateral loads.", "double wishbone（双叉臂）"],
            ["双叉臂操控精准，F1赛车也用，但造价高且侵占发动机舱空间。", "Precise and F1-proven, wishbones cost more and eat engine-bay space.", "engine bay（发动机舱）"]
         ]},
        {"id": "s4", "scene_zh": "多连杆与筷子悬架", "scene_en": "Multi-Link and 'Chopstick' Links", "time": "02:57",
         "context": "多连杆把上下两把叉子拆解成3-5根独立连杆，调教自由度最高；但连杆数量可以缩水，三根细杆就是筷子悬架。",
         "sentences": [
            ["多连杆本质是把上下两把叉子打散，拆解成3到5根独立的连杆。", "Multi-link splits the wishbones into 3–5 independent arms.", "multi-link（多连杆）"],
            ["每个连接点都有橡胶衬套做缓冲，自带滤震功底。", "Rubber bushings at each joint absorb vibration.", "rubber bushing（橡胶衬套）"],
            ["这种精细化分工给车厂极高的调教自由度。", "Fine-grained control gives engineers huge tuning freedom.", "tuning freedom（调教自由度）"],
            ["注意别被缩水多连杆骗了：三根细杆的筷子悬架，动态表现天差地别。", "Beware watered-down 'multi-link'—thin chopstick arms behave far worse.", "chopstick links（筷子悬架）"]
         ]},
        {"id": "s5", "scene_zh": "扭力梁也能调出好质感", "scene_en": "Even a Torsion Beam Can Feel Great", "time": "04:48",
         "context": "扭力梁几乎不占底盘空间，经济型家轿最爱；底盘三分靠堆料七分靠调教，法系车能把扭力梁调出贴地飞行质感。",
         "sentences": [
            ["扭力梁更像一根柔韧的扁担，能吸收不少路面震动。", "A torsion beam flexes like a springy bar, absorbing road shock.", "torsion beam（扭力梁）"],
            ["扭力梁最大优势是几乎不占底盘空间，把空间让给后排和后备箱。", "Its biggest win: it barely eats floor space, freeing room for seats and trunk.", "floor space（底盘空间）"],
            ["网上说前麦弗逊后扭力梁最垃圾，这话对但也不对。", "The 'torsion beam is worst' claim is true and false at once.", "partly true（对也不对）"],
            ["底盘三分靠堆料、七分靠调教，法系车能把扭力梁调出贴地飞行质感。", "Chassis is 30% hardware, 70% tuning—French makers work wonders on beams.", "70% tuning（七分调教）"]
         ]},
        {"id": "s6", "scene_zh": "一眼看穿底盘好坏", "scene_en": "Spotting Chassis Quality at a Glance", "time": "05:40",
         "context": "静态看底盘平整度和护板，带磁铁吸摆臂判断钢或铝合金，中高端车留意有没有完整的前后全框式副车架。",
         "sentences": [
            ["静态观察底盘平整度，好底盘通常有大面积护板。", "Check the underbody: good chassis have large protective covers.", "protective covers（护板）"],
            ["带一块磁铁往摆臂上一吸，吸住是钢，吸不住大概率是铝合金。", "A magnet on the arm: sticks = steel, falls = aluminum.", "magnet test（磁铁测试）"],
            ["铝合金比钢材轻30%到40%，能大幅降低簧下质量。", "Aluminum is 30-40% lighter, sharply cutting unsprung mass.", "unsprung mass（簧下质量）"],
            ["留意有没有完整的前后全框式副车架，它像给底盘加装金属外骨架。", "Look for full front and rear subframes—a metal exoskeleton for the chassis.", "subframe（副车架）"]
         ]},
        {"id": "s7", "scene_zh": "空气悬挂为何流行", "scene_en": "Why Air Suspension Took Over", "time": "09:06",
         "context": "电车大电池包整车两三吨，螺旋弹簧要么过软支撑不住要么过硬太颠，空气悬挂能根据载荷自动调气压解决矛盾。",
         "sentences": [
            ["国产电车卷空气悬挂，不是做慈善，而是被电车物理特性逼出来的。", "EV makers adopt air suspension out of physics, not charity.", "forced by physics（物理所迫）"],
            ["大电池包让整车重量轻松突破两三吨，传统螺旋弹簧有点不够用。", "Huge battery packs push weight past two tons—coil springs struggle.", "battery pack（电池包）"],
            ["弹簧调太软过弯撑不住，调太硬日常太颠。", "Coils too soft bottom out in corners; too hard rides harshly.", "bottom out（托底）"],
            ["空气悬挂根据载重自动调节气压，还能更细致过滤颠簸保护电池。", "Air suspension adjusts pressure by load and filters bumps to protect the pack.", "air suspension（空气悬挂）"]
         ]},
        {"id": "s8", "scene_zh": "全主动悬挂与终极判断", "scene_en": "Active Suspension and the Final Test", "time": "11:50",
         "context": "全主动悬挂带独立动力源，过坑前主动把轮子顶回去，理论上完全隔离震动；但终极判断永远是线下试驾。",
         "sentences": [
            ["全主动悬挂拥有独立动力源，用电磁电机带轮胎避震器。", "Fully active suspension has its own power source—electric motors on each damper.", "active suspension（全主动悬挂）"],
            ["过坑时在轮子还没掉下去前，就主动施加方向相反的力把轮子顶回去。", "Before the wheel drops, it pushes back with an opposing force.", "push back（顶回去）"],
            ["真正做到刹车不点头、过弯不侧倾，舒适操控两手抓。", "No brake dive, no body roll—comfort and handling together.", "no brake dive（刹车不点头）"],
            ["但评判底盘好坏的终极杀招，永远是线下试驾。", "Still, the ultimate chassis test is a real test drive.", "test drive（试驾）"]
         ]}
    ]
}

ARTICLES["standing-longjump"] = {
    "title_zh": "立定跳远口诀",
    "title_en": "Standing Long Jump Cheat Sheet",
    "duration": "19秒",
    "topic": "运动 · 立定跳远",
    "scenes": [
        {"id": "s1", "scene_zh": "别向后，要向上", "scene_en": "Not Backward, but Up", "time": "00:00",
         "context": "起跳时别把身体重心向后倒，要向上发力，跳远第一步是把力量用在垂直方向。",
         "sentences": [
            ["别向后，要向上。", "Don't go backward—go upward.", "don't go backward（别向后）"],
            ["起跳时重心要往上走，而不是向后倒。", "Drive your weight upward instead of falling back.", "drive upward（向上发力）"]
         ]},
        {"id": "s2", "scene_zh": "别屈臂，要直臂", "scene_en": "Not Bent Arms, Straight Arms", "time": "00:04",
         "context": "摆臂时别弯曲手臂，要伸直手臂摆动，用直臂带动身体向前。",
         "sentences": [
            ["别屈臂，要直臂。", "Don't bend your arms—keep them straight.", "straight arms（直臂）"],
            ["直臂摆动能带动整个身体向前上方。", "Straight-arm swings pull your whole body forward and up.", "swing the arms（摆臂）"]
         ]},
        {"id": "s3", "scene_zh": "别去宽，要顶宽", "scene_en": "Don't Spread Wide, Push Wide", "time": "00:08",
         "context": "落地时别把腿分得过宽，要向前顶宽，把腿尽量往前伸让落点更远。",
         "sentences": [
            ["别去宽，要顶宽。", "Don't spread your legs wide—push them forward.", "push forward（向前顶）"],
            ["落地瞬间把腿往前顶，才能让落点更远。", "Drive your legs forward on landing to extend the distance.", "extend the distance（延长落点）"]
         ]},
        {"id": "s4", "scene_zh": "别向下，要向前", "scene_en": "Not Down, but Forward", "time": "00:12",
         "context": "最后别把视线和身体朝下，要向前看、向前冲，保持向前的动力。",
         "sentences": [
            ["别向下，要向前。", "Don't look down—look forward.", "look forward（向前看）"],
            ["保持向前冲的势头，跳远才有距离。", "Keep your forward momentum to carry the distance.", "forward momentum（向前冲劲）"]
         ]}
    ]
}

ARTICLES["waterproof-hiking-shoes"] = {
    "title_zh": "你真的需要防水徒步鞋吗？",
    "title_en": "Do You Really Need Waterproof Hiking Shoes?",
    "duration": "2:33",
    "topic": "户外 · 防水徒步鞋",
    "scenes": [
        {"id": "s1", "scene_zh": "这不是非此即彼的问题", "scene_en": "Not an Either-Or Question", "time": "00:00",
         "context": "防水和不防水徒步鞋两拨人吵得不可开交，但其实是一道选择题：取决于你去什么地方、做什么。",
         "sentences": [
            ["防水鞋和不防水鞋两拨人各执一词，互相看对方都像大冤种。", "Waterproof and non-waterproof camps clash, each sure the other is wrong.", "opposing camps（对立的阵营）"],
            ["但这并非是一个非此即彼的问题，而是一道选择题。", "This isn't either-or—it's a matter of choice.", "either-or（非此即彼）"],
            ["取决于你去什么地方，取决于你做什么。", "It depends on where you go and what you do.", "depends on（取决于）"],
            ["两者是各有各的好，也是各有各的坑。", "Both have strengths, and both have traps.", "each has traps（各有各的坑）"]
         ]},
        {"id": "s2", "scene_zh": "涉水过溪选非防水", "scene_en": "For Stream Crossings, Go Non-Waterproof", "time": "00:36",
         "context": "夏天频繁涉水过河，非防水鞋往往是更好的选择：过溪湿了走几步很快就干，防水鞋进水后晾干要慢很多。",
         "sentences": [
            ["夏天涉水过溪，你可能觉得需要防水鞋，但实际上可能适得其反。", "Stream crossings in summer sound like a case for waterproof boots—but often the reverse.", "the opposite（适得其反）"],
            ["对于频繁涉水过河的人来说，非防水鞋往往是更好的选择。", "For frequent creek-forders, non-waterproof shoes are usually the better pick.", "creek fording（涉水过河）"],
            ["过溪湿了也不怕，走几步很快就干了。", "Get wet, keep walking, and they dry out in no time.", "dry out fast（很快干）"],
            ["实验数据表明，湿透后非防水鞋的干燥速度比防水鞋快很多。", "Tests show non-waterproof shoes dry far faster once soaked.", "dry faster（干燥更快）"]
         ]},
        {"id": "s3", "scene_zh": "冷湿环境选防水", "scene_en": "For Cold and Wet, Go Waterproof", "time": "01:21",
         "context": "早春深秋冬天，路面积雪薄冰、没完没了的水坑，防水鞋更好；低温下脚汗没那么严重，保温度比透气更重要。",
         "sentences": [
            ["如果主要是在早春深秋或冬天活动，路面是积雪、薄冰和水坑，防水鞋更好。", "For early spring, late autumn, or winter—snow, ice, endless puddles—waterproof wins.", "winter conditions（寒冷环境）"],
            ["防水膜虽然能挡雨水湿气，但透气性大打折扣。", "The membrane blocks rain but badly hurts breathability.", "breathability（透气性）"],
            ["低温环境下脚汗没那么严重，保住温度比透气更重要。", "In the cold you sweat less, so warmth beats breathability.", "warmth beats breathability（保温度优先）"],
            ["如果你面对的是湿雪、雨加雪的魔法攻击，那必须上防水鞋。", "Sleet and rain-snow mixes demand waterproof boots, no question.", "sleet（雨夹雪）"]
         ]},
        {"id": "s4", "scene_zh": "只买一双怎么选", "scene_en": "If You Buy Just One Pair", "time": "02:01",
         "context": "如果只想买一双徒步鞋，非防水鞋是更好的选择：覆盖90%的场景，剩下10%用备用袜子或防水袜扛过去。",
         "sentences": [
            ["如果你只想买一双徒步鞋，那非防水鞋可能是更好的选择。", "If you'll own one pair, non-waterproof is likely the smarter buy.", "one pair（一双鞋）"],
            ["因为它能覆盖你90%的场景。", "It covers about 90% of your scenarios.", "90% of scenarios（90%的场景）"],
            ["那剩下的10%呢？用备用袜子或者防水袜就能扛过去。", "The other 10%? A spare pair or waterproof socks carry you through.", "waterproof socks（防水袜）"],
            ["无论选什么鞋，都别忘了带双备用袜子和防水袜。", "Whichever you choose, always pack a spare pair and some waterproof socks.", "spare socks（备用袜子）"]
         ]},
        {"id": "s5", "scene_zh": "选择总结", "scene_en": "The Rule of Thumb", "time": "02:17",
         "context": "平凡过溪选非防水，炎热旱脚选非防水，寒冷湿潮不深涉水选防水，雨加雪选防水。",
         "sentences": [
            ["平凡过溪选非防水。", "For everyday creek crossings, choose non-waterproof.", "everyday use（日常使用）"],
            ["炎热旱脚选非防水。", "For hot, sweaty days, choose non-waterproof.", "hot and sweaty（炎热汗脚）"],
            ["还冷湿潮但不深涉水，选防水。", "Cold and damp without deep wading? Go waterproof.", "cold and damp（冷湿）"],
            ["没有一双鞋能让你永远不失脚，但总有一种智慧能让你永远走下去。", "No shoe keeps you dry forever—but the right choice keeps you walking.", "keep walking（一直走下去）"]
         ]}
    ]
}


def build(slug, art):
    full_scenes = []
    for i, s in enumerate(art["scenes"], 1):
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
