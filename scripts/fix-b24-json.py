#!/usr/bin/env python3
"""批24：为简化场景JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "w4Qh1I72MK": {
        "practice": [
            ["说前推后拉", "Push in to focus, pull back to reveal."],
            ["说前推半环绕", "Push in and sweep a half circle for depth."],
            ["说上升接斜摇", "Rise to show height, tilt to follow."],
            ["说横摇", "Pan horizontally to sweep the scene."],
            ["说收工", "That's a wrap for today's practice."]
        ],
        "pitfalls": [
            ["Push only straight ahead.",
             "Add a half-orbit to make the move lively.",
             "直推太单调，加半环绕。"],
            ["Keep the camera locked.",
             "A subtle shake gives a breathing feel.",
             "微晃更有呼吸感。"],
            ["Skip the pull-back.",
             "It reveals the environment after the push.",
             "后拉用来展示环境。"],
            ["Rush each move.",
             "Steady, smooth practice builds the muscle memory.",
             "练习要平稳。"],
            ["Shoot everything at chest height.",
             "Rising or tilting adds a new dynamic.",
             "变化机位增加动感。"]
        ],
        "shifts": [
            ["说运镜只会说 camera move",
             "用 push in（前推）、pull back（后拉）、pan（横摇）、tilt（斜摇）"],
            ["说拍摄只会说 shoot",
             "用 frame（画面）、orbit（环绕）、steady（平稳）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：手机运镜每日轻松练习、前推接后拉运镜、前推半环绕接后拉运镜、前推运镜、上升接斜摇运镜、横摇运镜、收工等。"
    },
    "2zJFokTBwsM": {
        "practice": [
            ["说45度机位", "Shoot from a 45° side angle for a relaxed feel."],
            ["说过肩拍", "Over-the-shoulder separates and layers the shot."],
            ["说偷拍视角", "A candid view pulls the audience in."],
            ["说手里拿东西", "Holding something makes hands look natural."],
            ["说镜头微晃", "A subtle shake adds a breathing feel."]
        ],
        "pitfalls": [
            ["Shoot everything head-on.",
             "Side angles and over-the-shoulder add life.",
             "正面直拍太呆板。"],
            ["Leave hands empty.",
             "Have the subject hold something for natural limbs.",
             "手里拿东西更自然。"],
            ["Lock the camera dead still.",
             "A gentle shake makes the frame feel alive.",
             "完全静止没呼吸感。"],
            ["Stage every shot.",
             "Candid angles build more immersion.",
             "偷拍视角更带人。"],
            ["Ignore the foreground.",
             "An over-the-shoulder frame adds depth.",
             "前景增加层次。"]
        ],
        "shifts": [
            ["说机位只会说 angle",
             "用 45° side angle（45度侧机位）、over-the-shoulder（过肩拍）、candid view（偷拍视角）"],
            ["说感觉只会说 feeling",
             "用 relaxed vibe（松弛感）、breathing feel（呼吸感）、immersion（代入感）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：短视频拍摄技巧、视频不要这样拍、要侧面45度拍更有松弛感、要侧面拍更加亲切、过肩拍主持更加分明、用偷拍视角拍带入感更强、手上拿点东西会更自然、镜头微晃更加有呼吸感等。"
    },
    "42u6PCAZwG5": {
        "practice": [
            ["说降低机位", "Lower the camera to eye level and carry the relationship."],
            ["说外反打", "Outside reverse carries the relationship and adds depth."],
            ["说内反打", "Inside reverse expresses the character's inner world."],
            ["说轴线机位", "Two side positions plus a center two-shot."],
            ["说骑轴", "Riding the axis breaks the fourth wall with a POV feel."],
            ["说越轴", "Crossing the axis is allowed when the story calls for it."]
        ],
        "pitfalls": [
            ["Shoot dialogue from eye level only.",
             "Lowering the camera and adding relationship builds the scene.",
             "机位平视加关系。"],
            ["Treat inside and outside reverses as the same.",
             "Outside carries the relationship; inside shows the inner world.",
             "内外反打别混用。"],
            ["Never cross the axis.",
             "Crossing it is fine when the story demands it.",
             "越轴要看情节。"],
            ["Forget the center position.",
             "A centered two-shot feels ceremonial and dramatic.",
             "中间机位有仪式感。"],
            ["Overuse jump cuts.",
             "Use them deliberately for rhythm, not by accident.",
             "跳切要刻意。"]
        ],
        "shifts": [
            ["说正反打只会说 shot-reverse-shot",
             "用 outside reverse（外反打）、inside reverse（内反打）、over-the-shoulder（过肩）"],
            ["说轴线只会说 axis",
             "用 ride the axis（骑轴）、cross the axis（越轴）、center position（中间机位）"],
            ["说镜头语言只会说 camera language",
             "用 break the fourth wall（打破第四堵墙）、POV（主观视角）、drama（戏剧效果）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：万能对话戏拍法来了、对话戏这么拍没感觉、把机位降下来和演员平视并带着关系立马有戏了、正反打中的外反打、外反打带着人物关系且画面更有层次、内反打表达人物内心、对话戏就是外反打和内反打轮着打、二人对话时中间有一条轴线、两边的机位是外反打和内反打、还有一个机位在中间可以拍二人、这个机位好有仪式感再推紧一些还能制造戏剧效果、所有的拍摄都必须在轴线的其中一边来进行、也可以骑轴拍、骑轴其实就是机位在二人中间、类似打破第四堵墙、骑轴还有主观视角效果能将观众带入角色、但还有很多人讲再怎么样都不能越轴、谁说不可以越要根据情节来、不要为了眼前一点蝇头小利而放弃了长远规划、我从来不教你表面的技巧而是教你真正的导演思维等。"
    },
    "female-parking-skill": {
        "practice": [
            ["说核心思路", "Plant the tail at the corner and seat the rear wheel first."],
            ["说贴近障碍物", "Hug the obstacle for swing room on the other side."],
            ["说后轮过障碍点", "Pass the obstacle point before stopping."],
            ["说走一点倒一点", "Nudge right-forward, then reverse a bit, repeating."],
            ["说车身角度", "Ignore the body angle—it self-corrects."]
        ],
        "pitfalls": [
            ["Park by body angle.",
             "Seat the rear wheel; the angle sorts itself out.",
             "别管车身角度。"],
            ["Nudge forward too far.",
             "It pulls the rear wheel out and the body sits off.",
             "走太多后轮被拉出。"],
            ["Stop before the obstacle point.",
             "Pass it first to gain swing angle.",
             "后轮要过障碍点。"],
            ["Leave space beside the obstacle.",
             "Hug it to free swing room on the other side.",
             "贴近障碍物留空间。"],
            ["Give up after one bad attempt.",
             "A quick adjustment re-seats the wheel.",
             "调整一下就能进。"]
        ],
        "shifts": [
            ["说停车只会说 park",
             "用 plant the tail（车尾落位）、seat the rear wheel（后轮到位）、swing room（外摆空间）"],
            ["说调整只会说 adjust",
             "用 nudge forward（往前轻挪）、reverse a bit（倒一点）、repeat（重复）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：这位女士进行侧方停车、由于两边停满了电动车而且车位也不长、第一次倒进去发现位置不合适、然后她通过自己熟练的操作进行了调整、全程没有犹豫一气呵成、这一套操作一看就是老司机、但入场方式其实还可以再改进一些、目的性非常强就是把车位停到假角处让后车轮先找到位置、但是倒进来之后她发现位置还是不合适因为后轮还是偏外、车房停车就是把你的车尾尽可能停到假角处让后轮先挺好位置、车身的角度你完全不用管、我们只需要右前方走一点反方向倒一点重复这个操作我们的车头也就进去了而且车身不会偏外、第一点入场时尽可能贴近库位这一边的障碍物给另一侧甩出足够的外摆空间、第二点后车轮一定要过了障碍点再停车因为距离越长能甩过去的角度也就越大、这两个能甩角度的条件全部满足、倒车的角度是不是大了很多、但切记不要走太多不然后轮被拉出来的多车身也就会偏外、所以我们不管前方多少空间就走一点然后反方向倒一点重复这个操作就可以了、哪怕后轮找到位置之后车身的角度是这个样子也是完全一样的操作、所以你现在还认为侧方停车很难吗等。"
    },
    "parallel-parking-adjust": {
        "practice": [
            ["说两种失败", "Too sharp: nose stuck. Too shallow: wheel out."],
            ["说正确进库", "Aim the tail at the back half and seat the wheel."],
            ["说角度大调整", "Drive out and swing the tail outward."],
            ["说角度小调整", "Steer outward and the tail swings across."],
            ["说调整核心", "It's the adjustment logic that matters."]
        ],
        "pitfalls": [
            ["Restart from scratch every time.",
             "A simple swing-out re-aligns the tail.",
             "甩尾一次就能进。"],
            ["Memorize by rote.",
             "Understand the logic and watch it again.",
             "别死记硬背。"],
            ["Forget the back half of the spot.",
             "Always aim the tail there.",
             "车尾对库尾后半部。"],
            ["Fix the angle but disturb the wheel.",
             "Keep the rear wheel seated while steering.",
             "调角不扰后轮。"],
            ["Give up when the body sits out.",
             "Steer outward and the tail swings back in.",
             "偏外就外打方向。"]
        ],
        "shifts": [
            ["说停车问题只会说 problem",
             "用 too sharp（角度大）、too shallow（角度小）、nose stuck（车头卡住）"],
            ["说调整只会说 fix",
             "用 swing-out（甩尾）、steer outward（往外打）、seat the rear wheel（后轮到位）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：側方停车进不去应该怎么调整、无非就两种情况、第一种角度大了车身偏离车头被卡住、第二种角度小了车身偏外后轮进不去、怎么样进最简单、靠近白车观察后视镜、镜子里能看到障碍点和库位、让你的车尾朝着库位的后半部分去倒车、其他的你不用管什么回轮这些你不用去想、先让内侧的后轮贴了边、后轮送到位前面有空间就等于是进库了、只需要右前方走一点反方向倒一点、车尾比较长车尾的空间就不用刻意去压榨、不管前面有多少空间我们都是走这一点、然后反方向倒一点、这样的话后轮是不会被拉出来的、车身也就停正了侧方就是这么简单、即使车身角度倒成了这个样子只要后轮送到位车前有空间同样是右前方走一点反方向倒一点重复此操作也就进库了、角度大了车身偏底车头被卡住了、把车开出去进行一下甩尾就可以了、往前走后轮过了障碍点之后往里打方向车尾的角度就往外甩了、之后我们朝着库尾的后半部分去倒车把后轮先送到位、车身偏外怎么办、那肯定是往外打方向车尾才能甩过来、往前走往外打方向车尾不就甩过来了吗、之后还是同样的操作倒进去把后轮送到位、这些东西不要去死记理解不了就多看两遍、主要是把调整的思路搞清楚等。"
    },
    "narrow-parking-adjust": {
        "practice": [
            ["说失败原因", "Centering the wheel too early unseats the rear wheel."],
            ["说正确倒法", "Keep increasing the angle while backing."],
            ["说进库标准", "Rear wheel seated plus nose room equals success."],
            ["说不要走太多", "A small nudge keeps the rear wheel in place."],
            ["说核心目标", "Seat the rear wheel first—angle follows."]
        ],
        "pitfalls": [
            ["Center the wheels mid-backup.",
             "Keep turning to feed the rear wheel in.",
             "倒到一半别回正。"],
            ["Chase the body angle.",
             "It fixes itself once the wheel seats.",
             "车身角度会自己好。"],
            ["Nudge forward too much.",
             "The rear wheel gets pulled out.",
             "走太多拉出后轮。"],
            ["Ignore the front swing room.",
             "The nose needs space as the rear goes in.",
             "车头要留外摆空间。"],
            ["Assume the spot is impossible.",
             "One extra angle keeps the wheel feeding in.",
             "加大角度还能进。"]
        ],
        "shifts": [
            ["说窄路只说 narrow road",
             "用 narrow street（窄路）、short spot（短车位）、tight space（狭小空间）"],
            ["说倒车只说 reverse",
             "用 keep backing（继续倒）、increase the angle（加大角度）、seat the wheel（后轮到位）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：来看案例这位司机进行侧方停车、由于路不是很宽调整了很多次都没有成功入库、整体来说还是车身偏外最终还是放弃了车位、问题出现在哪里、它前面的操作没有任何问题先贴近旁边车给左侧车头留出外摆的空间、但倒到一半它把前轮回正了所以就导致后车轮没有送进去、车身偏外的主要原因就是因为后车轮没有送到位、所以我们在倒车的同时随着后轮往库里面走车头外摆的空间也会越来越大、这时候不应该回正方向而是加大角度继续倒车、目的就一个把后车轮先送进去、你不用管车身角度停成什么样子、只要后车轮能到位并且车头右前方有空间就等于已经进库了、之后只需要右前方走一点反方向倒一点重复此操作也就可以了、车身角度是最好调整的即使你倒成这个样子也是同样的操作、但切记右前方走的时候不要走太多不然后车轮会被拉出去车身还是会偏外、好下一期咱们缩短车位、就是在你倒车时已经打死方向了但因为车位很短后车轮还是送不进去、或者你的车感不是很好车头外摆时总是害怕刮到前车头、这种车位有没有办法可以进好我们下期见等。"
    },
    "parallel-parking": {
        "practice": [
            ["说两种情况", "Steering too early or too late ruins the entry."],
            ["说离牙子远", "Steer hard left, pull out, then re-enter."],
            ["说离牙子近", "Steer hard right, then hard left, adjusting the gap."],
            ["说回正时机", "Center only after the mirror shows the whole car."],
            ["说压线入库", "Steer hard left as the rear wheel nears the line."]
        ],
        "pitfalls": [
            ["Fumble the wheel when too far from the curb.",
             "A defined pattern re-seats the car in seconds.",
             "远了一气呵成调整。"],
            ["Restart when the wheel is too close.",
             "A small two-step pattern fixes it.",
             "近了也能就地调整。"],
            ["Center the wheel at the wrong time.",
             "Center after the rear car's nose appears in the mirror.",
             "回正要选时机。"],
            ["Ignore the curb distance.",
             "Judge it and pick the matching fix.",
             "先判断离牙子远近。"],
            ["Panic in a tight spot.",
             "Both fixes are quick two-step patterns.",
             "两种情况都简单。"]
        ],
        "shifts": [
            ["说停车问题只说 problem",
             "用 too far from the curb（离牙子远）、too close（离牙子近）、cross the line（压线）"],
            ["说方向盘只说 turn",
             "用 steer hard left（左打满）、center（回正）、reverse in（倒库）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：側方停车入库时难免会出现方向打早或者打晚了、导致出现车身只停进半个车位或者后轮压马路牙子了、遇到这两个情况该怎么调整、第一种情况停下来以后发现车离马路牙子远了、很多新手会左打方向往前掉然后右往后倒在库内来回折腾、其实很简单我们先把方向左打满往左前上再出去、那往前出多少你只需要看左后视镜出现后车的整个车头后回正方向盘继续往后倒、左后轮即将压线时方向盘向左打满入库看右后视镜、车身与路沿平行的时候把方向回正停车、车子也顺利入库成功、第二种情况就是后轮离马路牙子近了、这个时候很多新手朋友会选择出去重来一次、其实你只需要把方向向右打满往前上一上、然后方向左打满往后倒一倒、车身跟马路牙子平行的时候调整前后距离、车子也能顺利入库成功、关注主页还分享了更多驾驶小技巧等。"
    },
    "suspension-underrated": {
        "practice": [
            ["说没有悬架", "Accelerate, corner, and bump all crash without it."],
            ["说悬架演变", "Leaf springs → coil springs → shock absorbers."],
            ["说麦弗逊双叉臂", "MacPherson merges strut and arm; wishbone adds an upper arm."],
            ["说五连杆空悬", "Five links spread load; air bags adjust height and firmness."],
            ["说CDC魔毯", "A solenoid valve tunes damping; sensors pre-tune for potholes."],
            ["说悬架即历史", "Suspension records the car's every leap."]
        ],
        "pitfalls": [
            ["Judge suspension by parts alone.",
             "Tuning matters as much as the hardware.",
             "悬架七分靠调教。"],
            ["Equate soft with comfortable.",
             "Too soft means float, roll, and motion sickness.",
             "太软反而晕车。"],
            ["Ignore damping.",
             "Springs alone keep bouncing—shocks absorb.",
             "弹簧会弹跳。"],
            ["Think air suspension is only for luxury.",
             "EV weight practically demands it.",
             "电车重量逼出空悬。"],
            ["Skip the final test drive.",
             "Nothing beats real-world feel.",
             "终极是试驾。"]
        ],
        "shifts": [
            ["说悬架只会说 suspension",
             "用 leaf springs（板簧）、coil springs（螺旋弹簧）、shock absorber（减震器）"],
            ["说结构只会说 structure",
             "用 MacPherson strut（麦弗逊）、double wishbone（双叉臂）、five-link（五连杆）"],
            ["说科技只会说 tech",
             "用 air suspension（空气悬架）、CDC（电磁阀阻尼）、magic-carpet（魔毯悬架）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：如果你的汽车没有悬架会发生什么、踩油门会这样过弯会这样过减速带会这样、直接就颠骨折了、这是最初的汽车过颠簸路段的时候是这样的、我们把马车上的板簧加上、把板簧换成螺旋弹簧、开过去颠簸之后又会弹起来一段、劳斯莱斯兄弟用一个充满油的缸体加活塞杆造了一个减震器、活塞在油液中移动油通过小口流动形成阻力从而减少震动、转弯的时候侧倾非常严重一边轮胎抓地力好一边弱很容易甩出弯道、福特工程师麦博逊把减震器弹簧通过转向节跟下叉臂集成在一起悬架就可以抵消侧倾的力、路特斯的查普曼觉得还是不够想要更快更稳的过弯还得再多一根上叉臂、双叉臂能精准控制轮胎与地面接触的姿态高速过弯更咬地更容易实现低重心布局、拥有双叉臂悬架在F1拿下了七个冠军、奔驰选择一次性拉满发明了五连杆结构的悬架、凯迪拉克把钢弹簧换成了气囊靠打气和放气来控制软硬和高度、带空悬的车高速自动降低重心下烂路自动升高底盘切运动悬架变硬切舒适悬架变软、保马工程师在油液通道旁边多加了一个电磁阀控制油口的大小来控制阻尼的软硬、新能源车激光雷达摄像头惯性传感器可以提前看到坑洼在到达之前ECU就把减震器调软或者调硬、这就是大家说的魔毯悬架、悬架是所有汽车技术进化当中最内在的演化它记录了汽车从马车到汽车再到新能源汽车的每一次跃迁、每一次震动被悄悄收住都是人类试图掌控混沌的微小胜利、底盘到底要怎么选还得看大家要什么样的体验、下面这张表格我们把常见的用车类型悬架配置适合建议都列出来了一目了然等。"
    },
    "exhaust-bang": {
        "practice": [
            ["说放炮是结果", "Backfire is a result of anti-lag, not the goal."],
            ["说涡轮迟滞", "Re-spooling the turbo after lift-off takes time."],
            ["说偏时点火", "Delay the spark so fuel burns in the exhaust and spins the turbo."],
            ["说二次进气", "A bypass feeds air to burn fuel in the manifold."],
            ["说放炮代价", "These fixes gut the turbo's lifespan."],
            ["说其他放炮", "Rich NA cars and faulty parts also pop."]
        ],
        "pitfalls": [
            ["Call every backfire anti-lag.",
             "Anti-lag causes it, but not all pops are anti-lag.",
             "放炮≠偏时点火。"],
            ["Keep the throttle open to kill lag.",
             "That runs the car flat-out—dangerous.",
             "节气门常开不可行。"],
            ["Think popping is harmless.",
             "It rapidly wears the manifold and turbo.",
             "放炮很伤涡轮寿命。"],
            ["Tune for pops on a street car.",
             "A few hundred km and the turbo's gone.",
             "家用车刷放炮别贪。"],
            ["Blame anti-lag for every fault pop.",
             "Timing, plugs, or fuel faults also backfire.",
             "故障也会放炮。"]
        ],
        "shifts": [
            ["说排气只会说 exhaust",
             "用 backfire（放炮）、exhaust manifold（排气歧管）、tailpipe（排气尾端）"],
            ["说涡轮只说 turbo",
             "用 turbo lag（涡轮迟滞）、anti-lag（偏时点火）、re-spool（重新起压）"],
            ["说原理只说 principle",
             "用 delay the spark（延迟点火）、secondary air（二次进气）、rich mixture（超浓混合气）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：排气放炮令人兴奋的话题、先讲涡轮的相关东西、偏时点火会引起排气放炮而排气放炮不一定就是偏时点火、排气放炮只是一个结果它并不是目的、松油门节气门基本上就关上了发动机只吸入很少的空气、排气变少没有足够排气吹动涡轮转速下降、重新踩油门把变慢的涡轮吹起来需要一段时间这就是涡轮迟滞、油门踩到底车子好像没什么反应要过了一秒甚至两秒才会猛的窜出去、最简单的解法是节气门一直开着但那样松不松油门没有区别车子马力全开往前冲非常危险、偏时点火：节气门保留一点开度继续喷油、电脑控制点火延后到做工冲程快结束排气冲程才点、汽油只来得及燃烧一小部分维持发动机运转、绝大部分没烧完的油气被排入排气歧管遇到滚烫的排气管被高温点燃、燃爆的高温高压气体继续吹动涡轮保持转速解决迟滞、说白了就是把本来应该在缸内燃爆的汽油拿到排气管里燃爆、排气放炮就是汽油在排气歧管中劈里啪啦燃烧的声音、另外还有二次进气旁通阀直接在排气管开路送新鲜空气进去、松油门时节气门照常关闭但排气管需要的空气通过旁通阀直接送进去、里面需要的汽油在缸内喷出来只喷油不点火排气冲程送到排气管、旁通阀打开新鲜空气遇到汽油加高温排气管直接爆炸继续吹动涡轮、这两种技术都是把汽油放到排气管里来烧统称抗涡轮迟滞、下面是偏时点火和二次进气旁通阀两个分支、排气放炮只是整个抗涡轮迟滞过程中烧带出来的产物、这两种方法虽然简单粗暴但排气管和涡轮设计时不是用来爆炸的、长时间高强度使用会大幅缩短排气管和涡轮寿命、民用车上开猛一点涡轮的制保器可能只有三天两百公里、刷程序调喷油量和点火时机就能刷出放炮效果但家用车要考虑耐用性和可靠性、自吸车在超浓混合气下工作排气管温度够高也会在排气尾端放炮、正常家用车正时火花塞油路出故障也可能放炮、油喷多了会放炮油喷太少汽油燃烧变慢也可能放炮等。"
    },
    "esp-principle": {
        "practice": [
            ["说ESP是什么", "Electronic Stability Program—many names, one system."],
            ["说传感器", "Steering, yaw, wheel-speed, and acceleration sensors."],
            ["说紧急介入", "Brake one wheel to counter understeer or oversteer."],
            ["说电子限滑", "Brake the spinning wheel, feed power to the gripping one."],
            ["说关ESP时机", "Drifting, getting unstuck, and wheel-spin diagnosis."],
            ["说ESP边界", "Within grip limits only—it lowers crash odds by 35%."]
        ],
        "pitfalls": [
            ["Think ESP boosts cornering.",
             "It only lowers the odds of losing control.",
             "ESP不提高转弯性能。"],
            ["Rely on ESP beyond grip limits.",
             "Physics wins—no system saves you past the tires.",
             "超出抓地极限谁也救不了。"],
            ["Turn ESP off for daily driving.",
             "Keep it on; it's a proven lifesaver.",
             "平时别关ESP。"],
            ["Miss the sensors' story.",
             "They compare intent with actual motion to catch loss of control.",
             "传感器对比意图与实态。"],
            ["Ignore the flashing light.",
             "It's ESP telling you it just saved you.",
             "指示灯闪就是ESP在救你。"]
        ],
        "shifts": [
            ["说ESP只会说 stability",
             "用 Electronic Stability Program（电子稳定程序）、yaw sensor（横摆传感器）、understeer（转向不足）"],
            ["说制动只说 brake",
             "用 brake one wheel（单轮制动）、electronic LSD（电子限滑）、spin（打滑）"],
            ["说安全只说 safety",
             "用 loss of control（失控）、grip limit（抓地极限）、crash probability（撞车概率）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：越来越多的车标配车身稳定系统英文大多叫ESP、ESP是Electronic Stability Program首字母缩写翻译就是电子稳定程序、也有车叫ESC Electronic Stability Control、本田现代叫VSA丰田叫VSC日产斯巴鲁叫VDC宝马捷豹路虎叫DSC保时捷叫PSM名字五花八门实质都是车身稳定系统、ESP就是基于行车电脑通过监测打滑和车身动态实现限制打滑和失控的系统、监测主要靠传感器：方向盘角度传感器告诉电脑驾驶员想要的方向、横摆传感器实时监测车身摆动幅度摆动大就说明要失控甚至翻车、四个轮子上的速度传感器也就是ABS传感器检测每个轮子转速、哪个轮子突然打滑转得比其它轮子快很多电脑就知道哪个轮子打滑、还有若干个加速度传感器配合横摆传感器让电脑知道车身是侧翻前倾还是后仰、稳定车身主要依靠ABS系统另外有时电脑会通过限制发动机动力输出配合ABS制动、ABS泵在刹车油管路径上可以对任意一条管路单独控制给哪个轮子踩刹车就单独给哪个轮子踩刹车不需要驾驶员介入、高速120遇到前车急停刹车来不及一把方向往右打、没有ESP很大可能出现转向不足实际转过的幅度小于方向盘打的幅度、回打方向车身晃动最厉害最容易产生转向过度然后彻底失控甩出去、有ESP时第一把方向电脑知道你想去右边但横摆传感器说车身还在直冲、电脑通过ABS只对右后轮制动其他三个轮子正常转车子绕这个点向右转动修正转向不足、回打方向时电脑只对右前轮制动产生向右摆动趋势抵消转向过度、成功避开一场事故、雨天压水坑水把轮胎和路面接触隔离压水一侧轮胎瞬间失去抓地力、方向盘被抢一下手没握紧又没有ESP很容易失控、ESP既能刹慢有抓地力的轮子把车身修正回安全方向、也能刹慢甚至刹停失去抓地力打滑的车轮让动力更有效给到有抓地力的轮子这就是电子限滑、特殊情况需要关闭ESP：玩漂移驱动轮打滑方向盘指向与车身运动方向不一致开着ESP永远飘不起来、陷雪坑泥坑必须依靠驱动轮一个劲打滑靠惯性冲出来要关闭ESP、修车师傅顶到架子让轮子空转判断异响也要关闭ESP不然电脑检测四个轮子都在打滑会限制发动机油门输出还踩刹车、平时不要按关闭按钮ESP是保障日常行车安全非常重要的功能、安全驾驶最主要的因素还是人ESP只是辅助、ESP指示灯闪烁就是告诉你系统正在保护你、车辆最终极限取决于轮胎抓地极限ESP只能在抓地极限内控制车身、超出抓地极限谁也救不了你、ESP不属于提高转弯性能的功能只能降低车辆失控的概率、NHTSA公布同等条件下ESP降低撞车概率35%、SUV车型中带ESP的事故比不带少67%、加拿大2011年强制标配美国2012欧盟2014、我国还不是强制标配一些低端或低配车型可能没有、买车时强烈推荐考虑ESP功能等。"
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
