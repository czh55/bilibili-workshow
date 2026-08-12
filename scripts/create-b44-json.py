#!/usr/bin/env python3
"""b44 JSON 生成脚本：旅行穿搭/山居旅行/摆姿教程/城市研究/建筑设计（5篇）"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scripts" / "scene-data"
OUT.mkdir(parents=True, exist_ok=True)

DATE = "2026-08-12"
PLATFORM = "xiaohongshu"

V = [
(
 "no-many-clothes", "不想带一堆衣服又想出片的，看这篇！", "Pack Light, Shoot Great", "3分03秒", "穿搭 · 极简衣橱", "http://xhslink.cn/o/1EUOZAyW3oG",
 [
  ("开场：行李越小越能出片", "Opening: Pack Less, Shoot More", "00:00", "博主用十余天行程证明：想拍出多套 look，关键不是带多少衣服，而是带对能任意组合的基础款。",
   [("怎么带最少的衣服拍最多的片。", "How to shoot the most looks with the least clothes.", "look（造型）"),
    ("这件事我太有发言权了。", "I'm the right person to talk about this.", "have a say（有发言权）")]),
  ("思路一：小设计基础款", "Basic Pieces, Clever Twists", "00:10", "带「有小设计」的基础款：白色T恤可以换成无袖蛋糕领或船领，白背心换成鱼骨背心，黑色背心换成交叉大肋背连体款。",
   [("有小设计的基础款任意切换。", "Basics with small details switch up easily.", "basic（基础款）"),
    ("下半身全部带基础款。", "Everything on the bottom is a basic.", "bottom（下半身）"),
    ("整个一身显得简约又有质感。", "The whole fit looks simple yet classy.", "classy（有质感的）"),
    ("基础款真的太不占地方。", "Basics barely take up any space.", "space（空间）")]),
  ("思路二：基础内搭+彩色罩衫", "Basics Under a Color Pop", "00:38", "基础款内搭加色彩强烈的罩衫，一件罩衫罩在上半身或围在下半身，就变成两套 look。",
   [("带基础款内搭加彩色罩衫。", "Pack basics plus a colorful topper.", "topper（罩衫）"),
    ("这个思路是我的命。", "This trick is my life.", "trick（妙招）"),
    ("是不是又变成两套 look。", "Now it's two looks out of one piece.", "two looks（两套造型）"),
    ("叠穿增加层次感。", "Layer it to add depth.", "layer（叠穿）")]),
  ("思路三：纯色基础+亮色设计款", "Plain Base, Statement Piece", "00:67", "纯色基础款搭配有设计感的亮色单品：油画感鱼骨衣配白色短裙或牛仔裤，明艳又不显精致土。",
   [("纯色基础加亮色设计款。", "Pair a plain base with a loud piece.", "loud（张扬的）"),
    ("下面简单穿个白色短裙。", "Keep it simple with a white skirt.", "simple（简单的）"),
    ("很明艳但不会显得精致土。", "Bold, but not tacky.", "tacky（土气的）")]),
  ("思路四：统一色调不同材质", "One Tone, Mixed Textures", "00:79", "同一色调但材质不同：粉色纯棉T恤配缎面短裙或亮片裙，既有对比又和谐耐看。",
   [("统一色调但不同材质。", "One color family, different fabrics.", "fabric（材质）"),
    ("上身穿纯棉T恤，下身是缎面裙。", "Cotton tee on top, satin skirt below.", "satin（缎面）"),
    ("有微微对比又很和谐。", "A gentle contrast that still feels harmonious.", "harmonious（和谐的）")]),
  ("思路五：成套设计感衣服", "Designed Sets Do the Work", "00:96", "直接买成套的设计感衣服：纯色基础款套装不用搭配就能撑起造型；挂脖背心拆开又能和其他单品组合出 double look。",
   [("直接买成套的设计感衣服。", "Just buy designed sets.", "set（套装）"),
    ("不需要再搭配就能撑起完整造型。", "No matching needed to complete the outfit.", "outfit（造型）"),
    ("上下拆开又能搭配出 double look。", "Separate the pieces for a double look.", "double look（双造型）")]),
  ("思路六：基础款靠配饰撑起", "Accessories Carry the Fit", "00:123", "基础款太素？用一个夸张的配饰去撑起整套 look：大包、民族包、双肩包、耳饰、头饰、墨镜、丝巾都能当点睛之笔。",
   [("基础款就要多利用配饰。", "Basics call for bold accessories.", "accessory（配饰）"),
    ("用一个夸张配饰撑起整套 look。", "One bold piece carries the whole look.", "bold（夸张的）"),
    ("这套白衬衣全靠配饰撑起来。", "This white shirt is carried entirely by accessories.", "carry（撑起）")]),
  ("配饰清单：包与饰品", "The Accessory Arsenal", "00:140", "旅行本身就带大容量包，不妨选有设计感的：民族风大包撑风格，学院风配小双肩包，黑色背心配糖果色饺子包。",
   [("选一个有设计感的大包。", "Pick a big bag with some design.", "design（设计感）"),
    ("学院风可以配小双肩包。", "Go academic with a small backpack.", "backpack（双肩包）"),
    ("黑色背心配糖果色饺子包。", "A black tank with a candy-colored bag.", "candy color（糖果色）")]),
  ("配饰玩法：墨镜发饰皮带", "Accessories as Style Switches", "00:149", "耳饰、发圈、头饰、墨镜、复古耳机、有造型感的帽子、logo丝巾都能改变基础款的氛围；金属感皮带增加运动健康感。",
   [("大耳饰发圈头饰墨镜都行。", "Earrings, hair ties, caps, shades—all work.", "shades（墨镜）"),
    ("复古耳机空壳子很便宜。", "Vintage headphones come cheap as props.", "prop（道具）"),
    ("金属感皮带增加运动感。", "A metal belt adds an athletic edge.", "edge（锋芒）")]),
  ("结尾：更多旅行穿搭", "Wrap-up: More Travel Looks", "00:176", "分享结束，之后还会带来更多关于旅行穿搭和出片的内容。",
   [("分享完了，下次见。", "That's all for today—see you next time.", "wrap-up（收尾）"),
    ("之后还有更多旅行穿搭内容。", "More travel styling content is on the way.", "styling（穿搭）")]),
 ],
),
(
 "wulingshan-aranya", "雾灵山阿那亚🍃住进山里的2天1夜", "Two Days in Wulingshan Aranya", "5分13秒", "旅行 · 山居度假", "http://xhslink.cn/o/gHWOvGdtC0",
 [
  ("开场：两天一夜的山居推荐", "Opening: A Two-Day Mountain Escape", "00:00", "只有两天时间、想找远离城市温度适宜还能带小狗度假的地方，博主推荐雾灵山阿那亚：不赶行程、不挤人潮，吹风泡汤看山看日落。",
   [("想找远离城市又舒适的地方。", "Looking for a cool escape from the city.", "escape（逃离）"),
    ("推荐你们来雾灵山阿那亚。", "I really recommend Wulingshan Aranya.", "recommend（推荐）"),
    ("吹风泡汤看山看日落。", "Feel the breeze, soak, and watch the sunset.", "soak（泡汤）")]),
  ("出发：金海湖服务区", "On the Road: Jinhaihu Service Area", "00:15", "早晨8点多出发，路过金海湖服务区，穿过几个长隧道，就到了承德兴隆的地界。",
   [("早晨八点多就出发。", "We set off just after eight in the morning.", "set off（出发）"),
    ("一路开过来路过金海湖服务区。", "Along the way we pass the Jinhaihu service area.", "service area（服务区）"),
    ("穿过几个长长的隧道。", "We drive through a few long tunnels.", "tunnel（隧道）")]),
  ("入住蓝椰酒店", "Check-in at Blue Coconut", "00:22", "入住蓝椰酒店，车停在酒店入口，办理入住后送早餐代金券，几家食堂通用，先寄存行李。",
   [("我们住的是蓝椰酒店。", "We're staying at the Blue Coconut.", "stay（住宿）"),
    ("入住后送早餐代金券。", "Check-in comes with breakfast vouchers.", "voucher（代金券）"),
    ("先寄存一下行李。", "Let's store the luggage first.", "luggage（行李）")]),
  ("酒店小花园遛狗", "The Garden and the Dog", "00:30", "酒店门前的小花园非常漂亮，小狗能在这里开心地转悠，画面像小狗的朋友圈现场。",
   [("酒店门前的小花园非常漂亮。", "The garden in front of the hotel is gorgeous.", "gorgeous（漂亮的）"),
    ("在这里能刷到小狗的朋友圈了吧。", "This must be where dogs post their moments.", "moments（朋友圈）")]),
  ("小狗托管", "Leaving the Dog in Good Hands", "00:40", "把小狗送到民宿托管，主人放心去吃饭：它不是独居，有家人陪着。",
   [("把小狗送到民宿托管。", "We leave the pup at the guesthouse.", "guesthouse（民宿）"),
    ("不用担心，它有家人陪着。", "Don't worry, it has company.", "company（陪伴）")]),
  ("第一食堂午餐", "Lunch at the First Canteen", "00:47", "第一食堂覆盖早中晚饭，山楂红烧肉、鱼肉、素菜、主食汤品选择很多，适合一家人。",
   [("第一食堂覆盖早中晚饭。", "The First Canteen covers all three meals.", "canteen（食堂）"),
    ("选择很多，适合一家人。", "Lots of choices, great for families.", "choice（选择）")]),
  ("榻榻米房间", "The Tatami Room", "00:59", "饭后上楼休息，榻榻米设计简单干净，卫生间空间很大、敞亮。",
   [("榻榻米简单又干净。", "The tatami room is simple and clean.", "tatami（榻榻米）"),
    ("卫生间空间很大。", "The bathroom is extra spacious.", "spacious（宽敞的）")]),
  ("酒店大堂与集合店", "Lobby and Lifestyle Store", "00:73", "酒店大堂太适合拍照，旁边还有一家集合店，卖摆件、家居小物和精致生活方式用品。",
   [("酒店大堂太适合拍照了。", "The lobby is perfect for photos.", "lobby（大堂）"),
    ("旁边是一家集合店。", "Right next to it is a lifestyle store.", "lifestyle store（集合店）")]),
  ("山间漫步与小瀑布", "Mountain Walks and a Waterfall", "00:83", "沿着山里小路慢慢逛，汤泉后有一处山泉，水特别清凉，走到小瀑布边听流水声整个人都静下来。",
   [("沿着山路慢慢逛一圈。", "We wander the mountain trails at our own pace.", "wander（漫步）"),
    ("泉水特别清凉。", "The spring water is wonderfully cool.", "spring（山泉）"),
    ("听流水声整个人都静下来。", "The sound of the stream just calms you down.", "calm down（静下来）")]),
  ("灯塔自然乐园", "The Lighthouse Nature Park", "00:103", "从一期走到二期会路过售楼处，外景和样板间特别出片；再往前是灯塔自然乐园，特别适合带小朋友玩。",
   [("外景和样板间都特别出片。", "The showroom and grounds photograph beautifully.", "showroom（样板间）"),
    ("灯塔自然乐园适合带小朋友玩。", "The lighthouse park is great for kids.", "lighthouse（灯塔）")]),
  ("抹茶店与温泉", "Matcha Stop, Then the Hot Spring", "00:115", "下午5点约了温泉，时间还富裕，先来小山口的抹茶店：招牌抹茶饮和抹茶奶油双拼冰淇淋不太苦、一点点甜。去温泉的路上被绿植包围，顺着台阶走有取景通幽的感觉。",
   [("先来这家专门的抹茶店。", "We drop by the dedicated matcha shop first.", "matcha（抹茶）"),
    ("不太苦，但一点点甜。", "Not too bitter, just a touch of sweet.", "bitter（苦的）"),
    ("去温泉的路上被绿植包围。", "The path to the spring is wrapped in greenery.", "greenery（绿植）")]),
 ],
),
(
 "easy-pose-simple", "看了就会相当简单的pose教程", "Poses You'll Learn in Seconds", "2分01秒", "摄影 · 摆姿教程", "http://xhslink.cn/o/42FBD3uWSZk",
 [
  ("开场：别再站军姿", "Opening: Stop Standing at Attention", "00:00", "每次拍照都像站军姿？两个知识点——交叉和支点，记住就能立刻实操。",
   [("每次拍照跟站军姿一样。", "Every photo makes me look like I'm at attention.", "at attention（站军姿）"),
    ("记住两个知识点：交叉和支点。", "Remember two keywords: cross and pivot.", "keyword（关键词）")]),
  ("知识点一：交叉", "Keyword One: Cross", "00:10", "人站好时四肢和身体平行；摆姿势时把一个平行的人变成交叉的，让四肢和身体保持交叉。",
   [("正常站好四肢和身体平行。", "Standing normally, your limbs parallel your body.", "parallel（平行的）"),
    ("把平行的人变成交叉的。", "Turn a straight person into a crossed one.", "cross（交叉）"),
    ("让四肢和身体保持交叉。", "Keep your limbs crossing your body.", "limb（四肢）")]),
  ("站姿交叉实操", "Crossing in Practice", "00:24", "站姿：腿交叉、手也可以交叉；坐姿一样，插兜也是一种交叉。",
   [("腿交叉，手也可以交叉。", "Cross your legs, or cross your arms.", "cross（交叉）"),
    ("插兜也是一种交叉。", "Hands in pockets count as a cross too.", "pockets（裤兜）"),
    ("肢体只要舒展开。", "As long as your body opens up.", "open up（舒展开）")]),
  ("坐姿交叉与插兜", "Seated Crosses", "00:38", "坐在板凳或马路牙子上也是交叉：让四肢和脑袋躯干做互动，动作就会自然。",
   [("坐在路边也是交叉。", "Sitting on a curb still counts as crossing.", "curb（马路牙子）"),
    ("让四肢和躯干做互动。", "Let your limbs play off your torso.", "torso（躯干）")]),
  ("三角形规律", "The Triangle Rule", "00:50", "你会发现很多动作都有三角形：插腰是三角形，搭头是三角形，一交叉还是三角形。把躯干想成方块，拿三角形往身上拼。",
   [("很多动作都有三角形。", "Many of your poses form a triangle.", "triangle（三角形）"),
    ("插腰是三角形，搭头也是。", "Hand on hip is a triangle; hand on head too.", "hip（胯）"),
    ("把躯干想成方块往上拼。", "Think of the torso as a box and build triangles on it.", "torso（躯干）")]),
  ("知识点二：支点", "Keyword Two: Pivot", "00:79", "支点就是你身边的环境：有桌子可以倚靠，有凳子可以靠，有墙、门、窗户也可以倚靠，主要和环境做互动。",
   [("支点就是你身边的环境。", "A pivot is whatever surrounds you.", "pivot（支点）"),
    ("单手靠个桌子也行。", "Rest one hand on a table.", "rest（倚靠）"),
    ("有墙门窗都可以倚靠。", "Walls, doors, windows—all fair game.", "fair game（都可以）")]),
  ("交叉+支点总结", "Cross Plus Pivot", "00:95", "交叉是身体的互动，倚靠是环境的互动。拍照时记住这两个词，身体行动就能跟上。",
   [("交叉是身体的互动。", "Crossing is interacting with your body.", "interact（互动）"),
    ("倚靠是环境的互动。", "Leaning is interacting with the space.", "lean（倚靠）"),
    ("脑子里有关键词，身体就能跟上。", "Keep the keywords in mind and your body follows.", "follow（跟上）")]),
  ("结尾：多练就有效", "Wrap-up: Practice Makes the Pose", "00:104", "下次拍照照这个方法，多练几次就好，这套方法简单又耐用。",
   [("多练几次就好了。", "A few more tries and you'll get it.", "get it（掌握）"),
    ("这个方法简单又耐用。", "This trick is simple and reusable.", "reusable（可复用的）")]),
 ],
),
(
 "urban-village-answer", "城中村拆不拆？我在这里找到了一些答案", "Should We Tear Down Urban Villages?", "4分53秒", "城市 · 更新研究", "http://xhslink.cn/o/kxX3TMQ6AY",
 [
  ("开场：东京握手楼像城中村", "Opening: Tokyo Looks Like Our Villages", "00:00", "东京市中心没有绿化，楼与楼之间超级密集，这不就是中国的城中村吗？但这种握手楼是东京的常态，对我们却是城市之痛。",
   [("楼与楼之间超级密集。", "The buildings are packed impossibly close.", "packed（密集的）"),
    ("这不就是我们的城中村吗。", "Isn't this just our urban village?", "urban village（城中村）"),
    ("对我们是城市之痛。", "For us it's a pain point of the city.", "pain point（痛点）")]),
  ("道路与电动车", "Streets vs. E-bikes", "00:31", "东京的道路很窄，但单车和杂物严格摆放在路边，给行人留出空间；我们享受了电动车的便利，却失去了步行的体验。",
   [("他们的单车严格摆放在路边。", "Their bikes are strictly parked along the curb.", "curb（路沿）"),
    ("给行人留出空间。", "It leaves room for pedestrians.", "pedestrian（行人）"),
    ("电动车便利却失去步行体验。", "E-bikes are convenient, but walking suffers.", "convenient（便利的）")]),
  ("电动车的规则对比", "E-bike Rules Compared", "00:60", "深圳城中村停满电动车，道路只剩不到60%空间；日本对电动车有严格法案，宽度限60公分、时速限20公里，比新国标还慢。",
   [("电动车只给道路留不到60%空间。", "E-bikes leave less than 60% of the street.", "leave（留出）"),
    ("日本对电动车速度有要求。", "Japan regulates e-bike speed.", "regulate（管制）"),
    ("最高时速20公里每小时。", "The top speed is 20 kilometers an hour.", "speed limit（限速）")]),
  ("电线杆与配色", "Poles, Colors, and Harmony", "00:86", "日本电线杆出了名的乱，3552万根电线落在路面，但走在城市小道上却不觉得混乱，原因是材质和配色的选择。",
   [("日本电线杆出了名的乱。", "Japan's utility poles are famously messy.", "utility pole（电线杆）"),
    ("但走在路上却不觉得混乱。", "Yet the streets don't feel chaotic.", "chaotic（混乱的）"),
    ("原因是材质和配色的选择。", "It comes down to materials and colors.", "color palette（配色）")]),
  ("清水市案例", "The Shimizu Case", "00:113", "樱桃小丸子的家乡清水市，坐摩天轮俯瞰一片握手楼，比不上中国五线城市，但颜色基本是黑白灰和低饱和，跟电线同色系，外立面统一所以协调。",
   [("俯瞰全是握手楼。", "From above, it's nothing but packed houses.", "packed（密集的）"),
    ("颜色基本是黑白灰和低饱和。", "Colors stay in black, white, grey, and low saturation.", "saturation（饱和度）"),
    ("外立面统一所以协调。", "Unified facades make it feel coherent.", "facade（外立面）")]),
  ("大芬油画村对比", "The Dafen Comparison", "00:135", "深圳最艺术的城中村大芬油画村，每栋楼单看都还行，但不同材质配色放在一起，加上广告和汽车，就不那么艺术了。",
   [("每栋楼单独看都还可以。", "Each building looks fine on its own.", "on its own（单独地）"),
    ("不同材质配色放在一起就乱了。", "Mixed materials and colors clash when stacked.", "clash（冲突）")]),
  ("防盗网", "The Steel Burglar Bars", "00:157", "由于历史原因，城中村加装了大量不锈钢防盗网，防盗效果好，但也太影响颜色。把不锈钢拆掉，其实和东京高级公寓差不多。",
   [("大量不锈钢防盗网。", "Steel security bars cover every window.", "security bars（防盗网）"),
    ("防盗效果好但太影响颜色。", "Great for security, terrible for looks.", "looks（外观）")]),
  ("小巧思优化生活", "Small Tricks to Upgrade Life", "00:175", "东京中央区握手楼酒店窗外种上绿植，窗户设计成柜本状，让人忘记窗外是一堵墙；一户建的小天井也给人呼吸感。",
   [("窗外种上绿植。", "They plant greenery outside the window.", "greenery（绿植）"),
    ("让人忘记窗外是一堵墙。", "It makes you forget a wall is behind it.", "forget（忘记）"),
    ("小天井给人呼吸感。", "A small courtyard gives you room to breathe.", "courtyard（天井）")]),
  ("分布图与全拆不可能", "The Map and the Impossible Demolition", "00:219", "深圳城中村分布图显示，除核心片区基本都被城中村占领，有些村面积占一半。想靠全拆完成城市更新，基本不太可能。",
   [("基本都为城中村所占领。", "Urban villages claim nearly the whole city.", "claim（占领）"),
    ("全拆完成更新不太可能。", "Tearing it all down is simply not realistic.", "realistic（现实的）")]),
  ("南头古城示范与结论", "Nantou: A Better Way", "00:237", "南头古城在保留握手楼的同时改造外立面，成为热门旅游景点；结论是：大拆大建道阻且长，不如一点一点优化城市细节。城中村没有阳光，但我们可以创造光。",
   [("保留握手楼的同时改造外立面。", "Keep the old houses, upgrade the facades.", "upgrade（升级）"),
    ("一点一点优化城市细节。", "Polish the city's details little by little.", "polish（打磨）"),
    ("城中村没有阳光，但我们可以创造光。", "Villages lack sunlight, but we can create light.", "create light（创造光）")]),
 ],
),
(
 "one-house-vs-zijian", "一户建为何比自建房好看很多？", "Why Japanese Houses Look Better", "2分00秒", "建筑 · 住宅设计", "http://xhslink.cn/o/2u24mQwbYJm",
 [
  ("开场：好看的问题出在哪", "Opening: Why Does It Look Better?", "00:00", "日本一户建明明没啥复杂设计，看着就是很舒服。问题出在哪？有没有简单通用的设计规律？",
   [("明明没什么复杂设计。", "It has no fancy design at all.", "fancy（花哨的）"),
    ("看着就是很舒服。", "Yet it just looks right.", "comfortable（舒服的）"),
    ("有没有通用的设计规律。", "Is there a simple universal rule?", "universal（通用的）")]),
  ("结构：上小下大", "Structure: Small Top, Big Bottom", "00:13", "动漫里的房子都是下大上小的结构，降低整体重心，给人温馨感；我们的房子上下一样，像一块笨重的水泥压在地上。",
   [("动漫里的房子下大上小。", "Anime houses are wider at the base.", "base（底座）"),
    ("降低整体重心更温馨。", "A low center of gravity feels cozy.", "center of gravity（重心）"),
    ("我们的房子像笨重的水泥块。", "Ours sit like a heavy block of concrete.", "block（块状物）")]),
  ("小新家在中国", "Xiaoxin's House in China", "00:30", "如果小新家在中国，可能会变成上下一样厚重的样子，而且三楼恐怕还是空的。",
   [("小新家在中国会变成这样。", "Xiaoxin's house in China might look like this.", "imagine（想象）"),
    ("三楼恐怕还是空的。", "The third floor would probably be empty.", "probably（恐怕）")]),
  ("外墙：协调足矣", "Facade: Harmony Is Enough", "00:38", "糟糕的外立面是丑感的精髓。自建房反光的不锈钢、彩色窗户、窗帘、细碎小瓷砖都是不协调因素，统一就能好看。",
   [("糟糕的外立面是丑感的精髓。", "A bad facade is the secret to ugly.", "facade（外立面）"),
    ("不锈钢和彩色窗户都不协调。", "Steel and colorful windows break the harmony.", "harmony（协调）"),
    ("统一就能好看点。", "Unifying it makes it look better.", "unify（统一）")]),
  ("材质与颜色", "Materials and Colors", "00:57", "一户建材质不超过两种且反光度相似，颜色也是每层各一种、色调相近、饱和度低；细碎小瓷砖缝隙太多显得乱，碎墙面只能做装饰不能做主体。",
   [("材质不超过两种。", "They use at most two materials.", "material（材质）"),
    ("色调相近饱和度低。", "Close tones, low saturation.", "saturation（饱和度）"),
    ("过多缝隙显得很乱。", "Too many joints look messy.", "joint（缝隙）")]),
  ("错落感：设计感的核心", "Stepping: The Core of Design", "00:72", "错落感是决定房子有无设计感的核心：工地板房看起来很呆板，稍微给些凹凸设计感觉就来了。",
   [("错落感是设计感的核心。", "Stepping is the heart of design.", "stepping（错落感）"),
    ("呆板的房子加些凹凸就活了。", "A plain box gains life with a few recesses.", "recess（凹进）")]),
  ("增加错落感的原理", "Three Ways to Add Stepping", "00:91", "给廉价的建筑加上光影，给冰冷的建筑加上绿植，给单薄的建筑加上院墙，都是增加错落感的原理。",
   [("给廉价建筑加上光影。", "Add light and shadow to cheap buildings.", "light and shadow（光影）"),
    ("给冰冷建筑加上绿植。", "Add plants to cold ones.", "plants（绿植）"),
    ("给单薄建筑加上院墙。", "Add a courtyard wall to thin ones.", "courtyard wall（院墙）")]),
  ("总结公式", "The Formula", "00:104", "做一栋好看房子的公式：先搭上小下大、有些错落感的结构，选一组色调相近颜色低的颜色，最后摆上一些绿植，一个平平无奇的房子就盖好了。",
   [("先搭上小下大的结构。", "Start with a top-light, bottom-wide frame.", "frame（结构）"),
    ("选一组色调相近的颜色。", "Pick one family of close tones.", "tone（色调）"),
    ("最后摆上一些绿植。", "Finish with a few plants.", "finish（收尾）")]),
 ],
),
]

def paraphrase_for(sentences):
    out = []
    for zh, en, note in sentences:
        word = note.split("（")[0].strip()
        out.append([f"用{word}换一种说法", en])
    return out

def main():
    for slug, title, title_en, duration, topic, url, scenes in V:
        data = {
            "meta": {
                "slug": slug, "title": title, "title_en": title_en,
                "duration": duration, "scenes": len(scenes),
                "sentences": sum(len(s[4]) for s in scenes),
                "date": DATE, "platform": PLATFORM, "source_url": url, "topic": topic,
            },
            "scene_imgs": [f"shot-{i+1:02d}" for i in range(len(scenes))],
            "scenes": [],
        }
        for i, (tc, te, t, ctx, sents) in enumerate(scenes, 1):
            data["scenes"].append({
                "id": f"s{i}", "title_cn": tc, "title_en": te, "time": t,
                "context": ctx,
                "sentences": [list(s) for s in sents],
                "paraphrase": paraphrase_for(sents),
                "speak": " ".join(en for _, en, _ in sents),
            })
        data["practice"] = []
        data["pitfalls"] = []
        data["shifts"] = []
        data["difficult_words"] = []
        data["footer_notes"] = f"来源：{title}（小红书，时长{duration}）"
        p = OUT / f"{slug}.json"
        p.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"✓ {slug} {len(scenes)} scenes")

if __name__ == "__main__":
    main()
