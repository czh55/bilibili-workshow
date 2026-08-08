#!/usr/bin/env python3
"""批19：将简化场景JSON补全为 gen-scene-en.py 所需的完整结构。"""
import json, re
from pathlib import Path

ROOT = Path("/Users/chenzhiheng/Projects/bilibili-workshop")
DATA = ROOT / "scripts" / "scene-data"

EXTRA = {
    "4WZk6YpzMa8": {
        "duration": "3:30", "topic": "效率 · 一人公司",
        "practice": [
            ["说一人公司困境", "All trivial tasks land on you and create no value."],
            ["说甩掉重复劳动", "Offload repetitive work to tools and people."],
            ["说盯行业信息", "A scheduled AI scans trends and pushes relevant news."],
            ["说工作框架库", "Record structures so drafts generate from key points."],
            ["说数据复盘", "Feed platform data to auto-generate a review report."]
        ],
        "pitfalls": [
            ["Do everything yourself from zero.",
             "Offload repetitive labor to tools.",
             "重复劳动要甩给工具。"],
            ["Decide without information.",
             "Judgment rests on information quality.",
             "判断力建立在信息质量上。"],
            ["Write every document from scratch.",
             "Build a framework library for instant drafts.",
             "建框架库秒出初稿。"],
            ["Skip the review after publishing.",
             "Review what worked and where to push.",
             "复盘决定下一步方向。"],
            ["Value tools by word count.",
             "Value them by freeing you for high-level decisions.",
             "工具的价值是解放精力。"]
        ],
        "shifts": [
            ["说低效只会说 inefficient",
             "用 repetitive labor（重复劳动）、assembly line（流水化）、offload（甩掉）"],
            ["说信息只会说 info",
             "用 industry dynamics（行业动态）、topic bank（选题库）、judgment（判断力）"],
            ["说复盘只会说 review",
             "用 data source（数据源）、retention（留存）、auto report（自动报告）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：上班和艺人公司最大的区别、上班族、明确的分工、做好你那一摊事、艺人公司、所事都会砸在你一个人头上、消耗我们的时间、创造价值、高的业绩、重复性的劳动、甩给别人甩给工具、有限的精力、重要的决策、直接拆给你、流水化运作、三个场景、腾讯的work body、搜后的大厦、海报、一键做浩款、饭办公模板、自媒体模板、电商模板、第一条流水键、盯着行业信息、搜集信息、判断力、信息的质量、定时任务、每天早上自动扫描行业的动态、竞品的动向、热门的话题、删选出跟我的业务相关的方向、推给我、同性的work body、pc端的灵感、现成的模板、抓捧的圈、做同款、提示词、看热点出选题、热点选题的模板、赛道的关键词、生成一版选题库、挑一些顺眼的、细化修改、市场工作、监控竞品动态、做产品、追踪行业趋势、做销售、自动收集客户行业的讯息、花时间找信息、变成花时间看信息、方案TPT、课程大纲变成流水线、非常知名的问题、每一件事你都得自己做、从零开始做、经历效率、扛得住、解法、工作框架库、常用的一些结构、方案模板、录进去、擅长输出、要点丢进去、产生一版出稿、选题课的大纲、核心内容、关键的模块、完整的带钢框架、钢结怎么分、每些讲什么、逻辑怎么递进、列好、添具体的案例、调一调细节、表达习惯、几天时间、打磨、一天结束、数据复盘交给它、动作非常重要、经常忽略、复盘、内容发了项目做了课上了、回头去看看、哪个是有效的、哪个方向该继续、哪个该调整、哪个环节该删了、各个平台的数据员、生成一个复盘的报告、哪一个内容表现最好、开头的留存最高、格外的感兴趣、下个月往哪个方向使劲、最大的价值、写了多少字、重复性的劳动中解放出来、更加系统、有限的精力、最感兴趣的最需要动脑子、一个人在成立他人事、试着去、做短视屏个人IP、提高工作效率的干货视频、新粉、主义服务客、关注等。"
    },
    "VCTwn3d4Uw": {
        "duration": "2:13", "topic": "Vlog · 倒金字塔结构",
        "practice": [
            ["说倒金字塔", "Put the most newsworthy content first."],
            ["说反面示范", "Plain event-telling fails to grab interest."],
            ["说第一步改开头", "Lead with the most satisfying result."],
            ["说第二步细节", "Then show details and process."],
            ["说第三步价值观", "Convey method, emotion, or values."]
        ],
        "pitfalls": [
            ["Record daily life and expect views.",
             "Structure matters—put value first.",
             "只记生活没人看。"],
            ["Start with a plain intro.",
             "Lead with the best result, then process.",
             "平平开头没吸引力。"],
            ["Reveal the payoff at the end.",
             "Front-load the most satisfying result.",
             "结果要前置。"],
            ["List sports without emotion.",
             "Add passion and achievement to the process.",
             "过程要带情绪。"],
            ["Compare nothing with the original.",
             "Compare to see the huge difference.",
             "对照原版看差异。"]
        ],
        "shifts": [
            ["说结构只会说 structure",
             "用 inverted pyramid（倒金字塔）、front-load the result（结果前置）、most newsworthy（最有新闻价值）"],
            ["说开头只会说 intro",
             "用 the satisfying result（最爽结果）、plain telling（平平无奇）、hook（钩子）"],
            ["说剪辑只会说 edit",
             "用 reassemble footage（重组素材）、separate events（独立事件）、universal formula（万能公式）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：Vlog只記錄自己的生活、別人不愛看的、保持素材普遍、調整Vlog的結構、數據翻倍、碼住、具體的實操、本科專業、廣播電視新聞、道金字塔結構、新聞學、新聞價值大、放在最前面、短視頻、更重要更新鮮、觀眾更感興趣的信息、基於一個又一個單獨的事件、逛超市喝咖啡見朋友、組接鏡頭、萬能Vlog公視、回看、原本大概率是這樣的、Hello我是達寶、一直運動跟簡直、堅持了一週、成功減重了兩斤、平平無期、引起觀眾的興趣、先給我最爽的結果、描述過程、手把手、一步一步調整、第一步、觀眾最關心最爽的結果、減重成功、第一句改成、一周時間、成功減掉兩斤、最重要的是、靠的不是自律、靠的是熱愛、第二步、展示更多的細節和過程、探索了非常多種不同的運動、不停地篩選、游泳跟騎行、日常能做起、非常熱愛且喜歡、激發減脂熱情、專業的提示證、更有成就感、刷膚的儀器、非常非常喜歡、每次刷完都很好、第三步、去體驗你的方法情緒或者價值觀、完全不愛運動、怎麼能夠做到、幾乎每天都去游泳、對運動很上癮、很重要的點、跟開頭的圓板相比較、非常大的差異、回去把你的vlog重組一下、評論區、一一查看、好玩的乾貨、主頁、追蹤我、點贊點關注等。"
    },
    "J0DEshr2fz": {
        "duration": "2:25", "topic": "剪辑 · 效率提升",
        "practice": [
            ["说一定要写脚本", "A detailed script saves 80% of shooting troubles."],
            ["说一定要用快捷键", "Don't memorize shortcuts—use Q/W, Ctrl+B, arrows, Alt+G."],
            ["说拍完马上剪", "Instant editing keeps momentum and efficiency."],
            ["说折叠电脑", "An 18-inch foldable PC enables editing anywhere."],
            ["说搭建灵感库", "Watch, record, think—then decide fast when editing."]
        ],
        "pitfalls": [
            ["Shoot without a script.",
             "A detailed script saves 80% of shooting troubles.",
             "没脚本拍摄麻烦多。"],
            ["Try to memorize all shortcuts.",
             "Don't memorize—just use them.",
             "快捷键不用背直接用。"],
            ["Delay editing after shooting.",
             "The longer you delay, the less you want to edit.",
             "越拖越不想剪。"],
            ["Rely on a phone for travel editing.",
             "A foldable big-screen laptop handles anywhere editing.",
             "外出剪辑用大屏折叠本。"],
            ["Start editing with no references.",
             "Build an inspiration library for fast decisions.",
             "灵感库让决策更快。"]
        ],
        "shifts": [
            ["说脚本只会说 script",
             "用 outline and storyboard（大纲分镜）、execute the plan（按计划执行）、AI production（AI生产）"],
            ["说快捷键只会说 shortcuts",
             "用 Q keeps after W keeps before（Q留后W留前）、split cut（切一刀）、frame jump（帧定位）"],
            ["说剪辑只会说 edit",
             "用 edit instantly（即拍即剪）、dual screens（双屏）、waterfall screen（瀑布屏）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：看完这期视频、剪辑效率、第一次写的脚本、现在写的脚本、详尽的脚本、省去百分之八十以上的麻烦、剪音里的创作脚本页面、大纲分镜和网案、按照计划执行变革、AI生产能力爆发时增长、脚本的重要性一定会越来越强、一定要用快捷键、刚开始剪辑的新手、底处心理、这么多案件、记不住记不住、方案是不用记、直接用、只保留指神前面或者后面的情况、敲动键盘上这两个箱铃键、Q和W、Q有个小尾巴、留下后面的W、Ctrl加B快速切一刀、左键把指神快速定位到上一针和下一针、Alt加G快速新件幅的片段、常用非常好用的快捷键、整理成清单送给大家、一定要拍完马上剪、一大堆素材、越拖越不想剪、急拍机剪、出外景或出差、一大坨台式机、用手机呢功能当然找效率很低、展开就能用到18英寸大屏笔记本、红萌折叠电脑、随时随地剪辑、多场景办公、折叠形态下13英寸、日常出门随时生活装包都不重、剪印、红萌系统适配、桌面上打开Apple、单纸对窗口代价进行缩放、一遍搜素材同时剪辑、三个手指这样上下抛出来、同时拥有两块屏幕、比较精细的内容、半屏确实勉强、五指对窗口进行放大、瀑布屏、全场开转台下景、手指操作、比较流暂的、日常剪辑、搭配上键盘和鼠标、用家很爽、看报告、浏览数据处理思路、出门万代键盘、八指换出虚拟键盘、周末看电影、隔空滑动功能、刷视频、不用触碰屏幕、有灵感的画面、轻松抓取截图、丰富自己的灵感库、回到主题、一定要搭建自己的灵感库、平时多看多记录多思考、快速列出方案、完成决策、红萌哲队电脑、轻薄、关键时刻能敞开用等。"
    },
    "7rktjUoQDK9": {
        "duration": "2:40", "topic": "拍摄 · 希区柯克变焦",
        "practice": [
            ["说电影感来源", "Beyond story and color, master shots add cinema."],
            ["说希区柯克原理", "Push in while zooming wide: still subject, receding background."],
            ["说低成本拍摄", "A 50-yuan dolly or a rag-and-cup system pushes the phone."],
            ["说拍摄要点", "Keep subject centered and push at a steady speed."],
            ["说后期关键帧", "Scale keyframes from push-end size to start create the zoom."]
        ],
        "pitfalls": [
            ["Rely on expensive gear for the effect.",
             "A cheap dolly plus keyframe zoom works at home.",
             "手机加后期就能实现。"],
            ["Zoom without pushing.",
             "The dolly push is essential; the zoom is post-added.",
             "推镜是基础。"],
            ["Push at uneven speed.",
             "Steady speed is the key to the final effect.",
             "匀速是效果关键。"],
            ["Shoot below 4K.",
             "4K gives more post-production headroom.",
             "拍4K后期空间大。"],
            ["Treat the technique as the goal.",
             "Techniques are tools for bright moments in your work.",
             "手法只是工具。"]
        ],
        "shifts": [
            ["说镜头只会说 shot",
             "用 Hitchcock zoom（希区柯克变焦）、ghostly effect（鬼魅效果）、receding background（背景远离）"],
            ["说拍摄只会说 shoot",
             "用 push-in（向前推）、steady speed（匀速）、phone dolly（手机推车）"],
            ["说后期只会说 post",
             "用 scale keyframe（缩放关键帧）、fake the zoom（模拟变焦）、diamond tool（菱形工具）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：除去故事色調質感、手機拍攝的視頻、電影感、電影大師的鏡頭、關於導演之名的西虛柯克編繳、1958年、迷魂記、前景不動背景不斷遠離觀眾、鬼魅鏡頭、主角驚恐的情緒、攝影機不斷推向主體、焦段由長焦改變至廣角、廣角鏡頭、更大的取景範圍、更廣闊的背景、人物變大相互抵消、人物不動背景遠離、昂貴的設備、跟焦源、在家裡、手機和後期、同一款效果、平穩的向天推的鏡頭、額外的小道具、大概50塊左右、某寶搜的手機攝影小推車、品牌不推薦、行李箱、帶滾輪的東西、輪子都找不到、媽布加一個紙杯、QBS全B系統、拍攝的時候、物體放在畫面中心、推手機的時候盡量保持均速、最終效果的關鍵、拍4K、後期空間更大、比較簡單、放大的關鍵針模擬出變焦的效果、導入素材、多餘的部分給剪掉、鏡頭停下的那一針、打上一個關鍵針、工具欄裡這個小零型、記一下主體在這一針的大小、截個圖記一下、拖到視頻開始的地方、把主體放大到跟推進結束差不多的大小、自動生成一個關鍵針、放大的效果、完成了、C3哥哥變焦、用途已經非常廣泛、動畫作品中也能見到、表現驚恐的情緒、兩個角色內心慢慢靠攏、拍攝手法終究只是工具、靈活運用、大師的鏡頭、亮眼的瞬間、三連、點個關注、我是布肚頭、下次再見等。"
    },
    "9vCBl4EFPpt": {
        "duration": "4:44", "topic": "剪辑 · 蒙太奇",
        "practice": [
            ["说库里肖夫效应", "The same shot means different things cut with different images."],
            ["说蒙太奇词源", "Montage means assembly; it's cinema's essence."],
            ["说最早蒙太奇", "1903's fireman film first spliced simultaneous spaces."],
            ["说本质是脑补", "Montage works when design meets audience inference."],
            ["说交叉与对比蒙太奇", "Cross-cutting builds tension; contrast strengthens theme."]
        ],
        "pitfalls": [
            ["Equate montage with plain editing.",
             "Montage's essence is audience inference.",
             "蒙太奇本质是脑补。"],
            ["Film a single space sequentially.",
             "Early cinema without editing told only same-space stories.",
             "没剪辑只能顺时叙事。"],
            ["Assume the audience sees everything.",
             "Montage uses cuts to trigger imagined omitted plot.",
             "省略要靠观众脑补。"],
            ["Focus only on your shots.",
             "Audience imagination and experience complete the montage.",
             "观众联想成就蒙太奇。"],
            ["Forget practical montage uses.",
             "Cross-cutting and contrast montage are classic tools.",
             "交叉对比都是实战法。"]
        ],
        "shifts": [
            ["说剪辑只会说 editing",
             "用 montage（蒙太奇）、Kuleshov effect（库里肖夫效应）、assembly（构筑装配）"],
            ["说叙事只会说 narrative",
             "用 inference（脑补）、last-minute rescue（最后一分钟营救）、narrative efficiency（叙事效率）"],
            ["说画面只会说 shot",
             "用 contrast montage（对比蒙太奇）、cross-cutting（交叉剪辑）、off-screen meaning（画外深意）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：猛男、如何定義他、和什麼畫面剪到一起、雞腿、飢餓的猛男、變態的猛男、驚恐的我、三組鏡頭、猛男的表演沒有任何變化、同樣的表演呈現出不同的感覺、蘇聯導演庫里蕭夫、一百多年前、庫里蕭夫效應、蒙泰奇理論的有力證據、源於法語的詞彙、Mondage、構築裝配、電影發明後、剪輯、電影的精髓、連蒙達是Elezon的Cinema、基本上所有的蒙泰奇都是由剪輯創造的、電影發明之初、沒有剪輯、影像更接近我們的日常體驗、同一空間順時發生的故事、1903年的影片、一個美國消防員的生活、第一次通過剪輯、不同空間同時發生的兩段畫面、拼接在一起、完成敘事、最早的蒙泰奇、簡單地把蒙泰奇理解為剪輯、菜雞阿不楚美肌士兵、創造幾十次蒙泰奇、1加1大於2的效果、蒙太奇鼻祖、怎麼創造蒙泰奇、導演跟郭忠祐、救過剩根本的鏡頭、女主角被困於人工的房間內的鏡頭、交叉剪輯到一起、勞捕的消防員出動、只是救這個女主角、接下來的大概狙擊、從火箱中被救出來、蒙泰奇本質並不是剪輯本身、而是勞捕、有機剪輯到一起、引發觀眾腦補鏡頭之間省略的情節、提升敘事效率、畫面之間的衝撞、聯想到畫面之外的深層含義、導演的設計和觀眾的腦補結合到一起、畫面的組合成為敘事整體、蒙泰奇因而成立、觀眾的聯想經驗和理解、佔據著非常重要的位置、最有魅力的地方、搞複雜、運用自己的視頻裡、請回蒙南、常見的蒙泰奇用法、沃克兄弟、英雄救美的畫面、蒙南快救我、緊張刺激的交叉蒙泰奇、英雄趕來營製的畫面、美麗遭遇危險的畫面、來回切換、住手、最後兩條現為相交於英雄救美之一點、最後一分鐘營救、非常經典的交叉蒙泰奇手法、反差較大的兩組鏡頭、剪刀越洗的對比蒙泰奇、進一步加強要表達的主題、領袖、大目水告訴我、表達了什麽主題、非常多樣的呈現形式、貫穿銀屎的電影語言、魅力所在、成為UP主以後、特別喜歡留意每道畫面中導演使用的電影語言、著彩蛋一樣的純淨式觀影、真的很有樂趣、猛太機好牛逼、法爾也、猛太機等。"
    },
    "ANY4pwNEHVy": {
        "duration": "3:28", "topic": "剪辑 · 调色曲线",
        "practice": [
            ["说毛线类比", "Sort yarn balls bright to dark to judge overall tone."],
            ["说降低对比度", "Lower highlights and lift shadows to cut contrast."],
            ["说像素与直方图", "Pixels sort dark-to-bright into the histogram."],
            ["说曲线原理", "A curve maps a pixel attribute; pulling changes it."],
            ["说RGB与色相曲线", "White maps brightness; red maps red amount; hue maps hue."]
        ],
        "pitfalls": [
            ["Judge brightness by gut feeling.",
             "Sort and compare systematically.",
             "凭直觉看偏亮偏暗不严谨。"],
            ["Want a single curve to do everything.",
             "Each curve maps one pixel attribute.",
             "一条曲线管一种属性。"],
            ["Forget what the white line controls.",
             "RGB's white line maps overall brightness.",
             "白线管整体亮暗。"],
            ["Only use RGB for color shifts.",
             "The red curve shifts red vs cyan in highlights/shadows.",
             "红线管红青偏移。"],
            ["Treat the curve as complex.",
             "Its principle is simple—just know the mapping.",
             "原理简单重在理解。"]
        ],
        "shifts": [
            ["说调色只会说 color grade",
             "用 color curve（调色曲线）、histogram（直方图）、pixel mapping（像素映射）"],
            ["说亮度只会说 brightness",
             "用 highlights and shadows（亮部暗部）、contrast（对比度）、dark-toned/bright-toned（暗调亮调）"],
            ["说颜色只会说 color",
             "用 hue curve（色相曲线）、red vs cyan（红青）、saturation（饱和度）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：朋友不吐头、兩堆毛線、哪一堆毛線整體更偏岸、好奇怪的要求、明顯是這一堆、拍腦門、更嚴謹的方法、換一副能量視線、黑白的眼鏡、毛線團的亮暗、更明顯、從亮到暗分類排去、左邊這一堆偏岸的毛線團更多、整體更偏岸、很嚴謹、上进两个币、織一件毛衣、不想要對比度那麼高、先降低亮部、把最亮的毛線團換成稍微暗一點的、再提高暗部、把偏暗的毛線團換成稍微亮一點的、搞定、藍色不太適合我、把藍色的毛線全變成綠色的、偏輕一點、再偏藍一點、黃一點、有完沒完、崩潰了、計算機的世界、組成像的方向像素、數量和顏色都更加繁多、4K分辨率的圖像、像素塊、880萬以上、巴比特色身、1600萬種顏色、用毛線團代替像素、拼出4K巴比特的動態視頻、幾千萬個不同顏色的毛線團、處理顏色、耗費布圖头的一生、計算機、分秒之間、三連、調色功能、像素分割、排列毛線團那樣、從左到右從暗到亮、直方圖、直觀地看到、暗部偏多、亮部偏多、暗調、亮調、計算機會如何對圖像的亮度色相和保護度進行調整、像素轉回為毛線團、拉出一根線、所有的毛線團都牽引到這條線上、調整這根主線的某一段、相關連的毛線團就會受到影響、調色曲線也是類似的原理、曲線關連的像素的什麼屬性、拉動曲線時變化的是什麼、快速上手所有軟件中的調色曲線、最常見的RJP曲線、白色線、不同亮暗的像素、整體的亮暗、亮部更亮、暗部更暗、增加對比度、減小對比度、紅色的線、像素紅色的數量、亮部和暗部分別偏向於紅色或青色、傷痛腦筋的藍色毛線團變綠色、關連像素色相的色相曲線、調色師們必不可少的工具、原理並不複雜、隨心所欲地調整現實生活中難以改變的顏色、揮雜審美和對畫面的理解、構建起屬於我們的影像世界等。"
    },
    "5upRwqlKeix": {
        "duration": "4:37", "topic": "剪辑 · 排版审美",
        "practice": [
            ["说排版困境", "Text placement and fonts often ruin an otherwise great vlog."],
            ["说渠道一节目纪录片", "Design shows and Graphic Means teach layout basics."],
            ["说渠道二App UI", "Analyze app UIs for layout and sectioning ideas."],
            ["说UI细节迁移", "Light-gray bases and fewer blocks create clean looks."],
            ["说渠道三BRAND杂志", "A topic-based Chinese design magazine teaches systematically."]
        ],
        "pitfalls": [
            ["Add text at random positions.",
             "Learn layout logic from shows and apps.",
             "文字乱放显土。"],
            ["Use pure white on busy frames.",
             "Add a shadow or a base tone for readability.",
             "纯白看不清。"],
            ["Over-decorate with shapes.",
             "Fewer blocks and shapes read cleaner.",
             "过多装饰更乱。"],
            ["Learn design only from scattered sites.",
             "Use topic-focused magazines for system.",
             "零碎信息不如专题学习。"],
            ["Fear analyzing UI without training.",
             "Screenshot and analyze—you'll learn from volume.",
             "分析多了总能学到。"]
        ],
        "shifts": [
            ["说排版只会说 layout",
             "用 typography（文字排版）、block division（区块分割）、visual logic（视觉逻辑）"],
            ["说审美只会说 taste",
             "用 color palette（配色）、design principles（设计原理）、layout basics（基础排版）"],
            ["说学习只会说 learn",
             "用 topic-focused（专题聚焦）、screenshot analysis（截图分析）、systematic design（系统设计）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：困扰、新版的相机、非常不错的视频和照片、马不停提、检测成超级满意的Vlog、最后一步、加上一些文字、给照片排一下板、怎么有点土、字应该放在画面的哪里、什么字体、白色看起来比较简洁、看不清楚、换成其他颜色、直接灾难、加点阴影往前冰框、弄弄弄的、发在相机上、一家人厉害的朋友、同样的困扰、视频排板和文字设计、没有别人那么有质感、自学做视频的第一要意、多看、系统地告诉你们该怎么改善、看得多、三种能够提升排版思路、提升配色审美和视频灵感的渠道、马上拥挡、文字排版、排版之歌、超洗脑的、1分20秒、讲清楚了基础的文字排版、日本的设计类节目、超级保障、各种生活物品的设计原理、生活常见物品做的定格动画、面向儿童、知识展现得非常直观、浅浅易懂、记录片、graphic memes、平面之道、数字时代之前的平面设计制作的演变史、复古风格的排版和设计效果、启发灵感的画面和配色、片头、反复看了十几遍、第二种、排版学习渠道、每天都在浏览、手机app的UI、最简洁的方法去匹配用户的视觉逻辑、设计细节完全是可以跟视频排版相通的、不专业的眼光、通过升级UI来改变视觉风格、经常用的简洁app估估剪辑、更新UI、小细节、简单好学、视频预览区和操作区域进行分区、给预览区加浅灰色底、浅灰色本身建议整体白色的击掉、分割区块也不会让画面太乱、简洁风格的画面排版、相近的颜色、整体观感更简洁一体、取消了快捷工具栏的快撞浮层、工具栏直接融合在界面中、减少页面中过多的形状、不会被太多区块分割、简洁的观感、更加注重软件的IP形象了、不断变装的格子、软件开屏、各级采用的推荐功能图标上都会出现、等待选案的过程中也会跳出来变装、软件在陪我一起剪辑的感觉、识别度高的IP形象、植入在简洁的操作界面里、很好的平衡了软件的专业性、典型用户群体的幽默感和创意的需求、理想界面更有辨识度、很妙的设计语言、除了不顾剪辑之外、个人比较喜欢的UI设计、偏厂、Point、看到喜欢的AppUI、更新前把界面截图保存一下、分析一些设计细节、不用怕自己不专业、分析的多了总能学到一点、喜欢直接看图、比较小众的实体杂志、BRAND、官网、扑面而来的审美气息、比较少有的中文设计杂志、不用只看图了、设计类杂志、文字图片排版和配色都非常实用好学、设计网站相比较零碎的信息、每一期都会聚焦于一个专题、更系统的学习设计知识、电子扫描版、导到iPad里随时翻语、比看网站有那位多了、本期视频、提高视频排版审美的渠道、不定期更新、布鲁头、下次再见、拜拜等。"
    },
    "7ge4YJvkMge": {
        "duration": "0:47", "topic": "随笔 · 直接表达",
        "practice": [
            ["说直接的要求", "Being direct is what we're always asked to do."],
            ["说自我介绍", "Tell people directly who you are."],
            ["说直接说事", "State what you're doing plainly, like the giveaway."],
            ["说费力之处", "Indirect things cost the most effort."],
            ["说乐在其中", "It's a waste of time—but I enjoy it."]
        ],
        "pitfalls": [
            ["Drown the message in decoration.",
             "A few direct words reach the audience.",
             "直接才让人听懂。"],
            ["Assume more effort means more value.",
             "Indirect details consume time without value.",
             "不直接的小事最费神。"],
            ["Avoid the direct statement.",
             "Directly state who you are and what you're doing.",
             "直说你是谁要干什么。"],
            ["Regret the time spent on craft.",
             "It's a waste, but also enjoyment.",
             "浪费却享受。"],
            ["Judge directness as cheap.",
             "Only directness makes the audience understand.",
             "直接是让观众懂。"]
        ],
        "shifts": [
            ["说表达只会说 express",
             "用 direct statement（直接表达）、no dead air（不空场）、few words（几个字）"],
            ["说创作只会说 create",
             "用 indirect details（不直接的小事）、finishing touches（呈现方式）、waste yet joy（浪费却享受）"],
            ["说取舍只会说 choose",
             "用 spend effort（花精力）、enjoy the craft（享受它）、direct wins（直接取胜）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：直接一点是我们做什么一直被要求的事情、直接的告诉别人是谁、我是一个可以让你的视频做得更有趣的博主、非常非常都有创意、够了、直接的说出你要干什么、抽奖、今天我要抽奖、一台大江Pokey的3、全新的、直接一点怎么抽、就像这样、很棒非常直接、直接多好、直接一点才能让客人听懂的、用几个字盖空的跟别人分享、回想一下、过去我花飞最多经历的、不太直接的东西、这里应该有什么音乐、这一段能不能从不同的角度看到顿头的歌词、要不要跟画面有点一样、简单的几个字应该有什么方式呈现、太浪费了、不直接的事情上面耗费了太多时间、很享受它等。"
    },
    "3BZHNvnMJQY": {
        "duration": "5:31", "topic": "Vlog · 奔跑生命力",
        "practice": [
            ["说跑起来的作用", "Running lifts emotion and quickens the video's pace."],
            ["说长焦与参照物", "Telephoto plus passing objects create speed."],
            ["说ND与快门", "Use ND and keep shutter within double the frame rate."],
            ["说稳定器选择", "A tracking gimbal with framing handles running shots."],
            ["说表情规避", "Hide the face; group runs add vitality."]
        ],
        "pitfalls": [
            ["Cut a passionate track with no lift shot.",
             "Running is a controllable, infectious emotion shot.",
             "缺个带情绪的镜头。"],
            ["Use only telephoto without references.",
             "Speed needs passing objects, not just the zoom.",
             "没参照物无速度感。"],
            ["Shoot in daylight with a high shutter.",
             "Use an ND filter to control motion blur.",
             "白天要ND控快门。"],
            ["Hand-follow the runner.",
             "A tracking gimbal keeps framing while you run.",
             "手跟拍晃到没法看。"],
            ["Stare at the runner's face the whole time.",
             "Cut to feet, backs, or group runs.",
             "全程盯脸没生命力。"]
        ],
        "shifts": [
            ["说节奏只会说 pace",
             "用 quicken the pace（提快节奏）、break the rhythm（打断节奏）、emotion shot（情绪镜头）"],
            ["说速度感只会说 speed",
             "用 reference objects（参照物）、space compression（空间压缩）、motion blur（运动模糊）"],
            ["说拍摄只会说 shoot",
             "用 tracking gimbal（追踪稳定器）、smart framing（智能构图）、360° reverse（360反拍）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：LOG更有生命力、奇怪的男人、不斷重複這句話、竿子跟著我、口中念念一次、生命力想要嘛很簡單、跑起來跑起來就可以了、看給他嘛、展示了跑起來在vlog里非常重要的作用、引導音樂、提快節奏、經常遇到的問題、剪輯的時候需要進一段激情音樂、總感覺很突兀、突兀舞、缺少了把情緒帶起來的鏡頭、鏡頭有很多、更可控更有感染力、更適合旅行LOG、跑得太慢、同樣的速度、明顯右邊比左邊看起來跑得更快、兩個要點、長焦和參照物、前後快速略過的參照物、顯得你跑得更快、長焦帶來的空間壓縮、前後景看起來離你更近、在畫面中運動得更快、只用長焦但沒有參照物、速度感也是出不來的、選擇一個合適的場景、有前景的地方、柵欄樹林花叢人群、准兩邊有快速略過的東西、隧道、很適合排奔跑的場景、畫面的運動模糊也很關鍵、白天拍攝、準備一塊ND濾鏡、快門速度的分母、不要超過真實的兩倍、非常棘手、展示並解決它之前、讓剛才的拍攝變得更高效、手指跟拍、晃得人都不知道在哪裡、穩定器但純靠自己去跟也很難、拍的人也要跑起來、很難兼顧構圖、拍個石頭不一定有一套能用的、旅行青蛙、愛旅行渴跑、青蛙一樣粗暴、搞背書生命也生命都要沒了、大根蔥的穩定器、長焦下追蹤人、有東西對個人理事、最多也不會丟、幫你構圖的手機穩定器、很有必要、Insta360 Floor 2 Pro、很簡單、不需要調瓶、手機吸上去就可以直接開牌、沒有多餘的學習成本、唯一款有Apple Docky的協議認真的穩定器、iPhone元相機、熟悉的App、實現更重、協議的打通、直接用旋鈕來切換手機的長焦、智能美學構圖的功能、基本上什麼都不用想、效率會高非常多、一直盯著這樣一張臉、生命力也是無從貪棄的、極受問題、跑的時候很難做好表情管理、幾個方法來規避、穿插一些看不到臉的角度、跟腳步或者跟背影都可以、拍些帶運鏡的畫面、一幫朋友一直出去玩、多人奔跑的畫面、人數就是和生命力成正比、觀眾應該不會再盯著你的臉看、Blood 2 Pro依然發揮了重要作用、同時追蹤多人、往地上一放大概直觀跑就行了、輔養範圍也很大、各種角度都不會受限制、加入了一些功能、充分發揮這個靈活角度的優勢、一鍵360度反拍、拍全景照片、腳架自拍桿子都是直接自帶的、整體又輕便、一個人出去玩、拍到很多帶運鏡的生命力畫面、新的問題又出現了、提快視頻節奏、不可能一直跑下去吧、該怎麼打斷或者說改變節奏、最簡單的方法、把高昂情緒抽離出來的世界、省下、就吃了他一口麵包嘛、掌握了關於拍跑步你所需要的大部分知識了、一次奔跑可以包含很多東西、壓抑的釋放、青春的自由、離別的不捨、看到這個動作、心跳澎湃、想起自己生命力綻放的時刻、讓這種生命力跑進你的Blog、So understanding and so kind、You are everything to me等。"
    },
    "34Jp2Yl9pFR": {
        "duration": "3:27", "topic": "Vlog · 闲逛找灵感",
        "practice": [
            ["说闲逛找灵感", "Wandering the city gathers inspiration directly."],
            ["说收集街头文字", "Street lettering becomes typography inspiration."],
            ["说线路式延展", "Follow threads like subway lines to new topics."],
            ["说城市电影对照", "A film set in your city mirrors the places you visited."],
            ["说公园灵感", "Even parks—or the lack of it—feed creativity."]
        ],
        "pitfalls": [
            ["Wait for inspiration indoors.",
             "Go wander the city to collect it.",
             "灵感靠出门闲逛。"],
            ["Capture only scenery.",
             "Collect street lettering and elements for vlogs.",
             "街头文字也是素材。"],
            ["Explore without threads.",
             "Follow a clue like a subway line.",
             "沿线索一站站延展。"],
            ["Ignore where you are.",
             "A film set in the city echoes your day.",
             "城市电影对照回忆。"],
            ["Force inspiration everywhere.",
             "Even a dead end can spark the next idea.",
             "没有灵感也是灵感。"]
        ],
        "shifts": [
            ["说灵感只会说 inspiration",
             "用 wandering（闲逛）、inspiration library（灵感库）、threads（线索）"],
            ["说素材只会说 material",
             "用 street lettering（街头文字）、elements（元素）、cages as frames（笼子做框）"],
            ["说创作只会说 create",
             "用 city films（城市电影）、screenshot moments（抓取瞬间）、device boundary（设备界限）"]
        ],
        "footer": "转录基于图文实录完整口播。已校正：都市凭个灵感从哪、当然从闲逛中来、在北京遛在两天、收获了一些灵感、三分钟以后、全部变成你的灵感、夜风商场、维持五多海保留老师国营横计的商场、很多人和设施、三三年前开业第一天、在这里工作、老员工对视一番、有趣的字体、收集街头文字、非常适合闲逛的时候干的事情、直接把它们用在Vlog里、首写自己的灵感来源、营业员们大声聊着家常理短、场景和这样的商场一样越来越少见了、很多笼子、北京动物园里关大动物的大笼子、石礼和天椒市场里关小动物的小笼子、不错的元素、往里面装一些画面或是装自己、不知道能用在什么地方、先记下来、每多做一站北京一号线或者二号线、苏联风格建筑的兴趣就会多一份、顺着这个线索找到了这个地方、闲逛中最有意思的环节、地铁线路一样、从一个地方找到另一个地方、继续延展、下单一本书、展开一些电影、把线路铺开、与这并列的更多主题、分拆出未来可能觉得目的地和可以拍的内容、线路组上的任意一站、停在你的灵感库里、差点忘了、苹果邀请我来北京的主要活动、观看五部Apple创意引领的创作者、用iPhone拍摄的短片、非常清楚iPhone拍视频的能力、前面很多画面都是用哪拍的、看过很多iPhone拍的片子、这么大的屏幕上看到、还是很震撼、有些人已经不会有哦这是手机拍的这种想法去干扰你观看、设备对于创作的线是真的越来越小、看电影这件事情很奇怪、很长时间不看、一旦看了一部、影子就会被勾起来、接下来几天又进了好几次影院、回到酒店一直在看电影、挺值得推荐的活动、去了一个地方玩了一天、不知道要干嘛的话、打开一部跟这个城市有关的电影、白天去过的地方很可能就会出现在画面里、电影结束以后、立刻回到故事发生的城市种、这种对照还是挺有意思的、同样令人上瘾了、北京的公园、去了一个又想去另一个、公园可以产生什么灵感、我真的受不了了、公园这种地方还想有什么灵感、简直是在摧残你的灵感、想想下次可以去哪里找灵感、有没有人能给我一点灵感、能不能让我回家好好想一想、喝了几杯儿说的话总是叫人害怕等。"
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
