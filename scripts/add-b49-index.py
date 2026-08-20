#!/usr/bin/env python3
"""b49：为批内新视频追加 index.json 条目（幂等，已存在跳过）。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
INDEX = DOCS / "index.json"

DATE = "2026-08-20"

ENTRIES = [
    {
        "slug": "fast-serve-return", "title": "2招，接发快球不再怕！",
        "duration": "34秒", "tags": ["网球", "接发球", "教学"],
        "url": "https://xhslink.cn/o/4ecxjgKmcvn",
        "summary": "核心判断：接快球靠「前顶+挥长」两大要领——小引拍前顶身体（不拉大架势，像墙一样向前迎击）应对高速平击的短反应时间，充分挥长（轨迹越长弹道越稳）保证回球稳健；反面对照是过早过短收拍、重心过早向上。",
        "shots": 6, "segs": 6, "height": 5852,
    },
    {
        "slug": "tulip-latte-fix", "title": "拯救郁金香拉花：推得太小变形怎么办",
        "duration": "1分38秒", "tags": ["咖啡", "拉花", "郁金香", "教学"],
        "url": "https://xhslink.cn/o/4QKZKMKi6TA",
        "summary": "核心判断：新手郁金香拉花失败（图案小/变形）来自「出流受限+位置无参照」两个可修复参数——操作上用橡皮筋中轴线圈定推花范围（落点与收勾不越线），工具上换更大缸体、更宽缸嘴的拉花缸，让奶泡大胆释放。",
        "shots": 8, "segs": 39, "height": 2235,
    },
    {
        "slug": "latte-froth-lesson2", "title": "在家学拉花第二课：如何打发好奶泡",
        "duration": "3分58秒", "tags": ["咖啡", "拉花", "奶泡", "教学"],
        "url": "https://xhslink.cn/o/2QtqKPrcUq8",
        "summary": "核心判断：奶泡打发是原料（巴氏冷藏全脂）×工具（打奶缸/全能缸）×原理（进气+打棉两阶段）×实操（三点钟贴棒、按机型进气时间、65度停点）四环节的可控叠加；核心纪律是打棉期间不乱动防二次进气。",
        "shots": 9, "segs": 162, "height": 2342,
    },
    {
        "slug": "espresso-extraction-latte", "title": "在家学拉花第一课：如何萃取适合拉花的浓缩咖啡",
        "duration": "7分35秒", "tags": ["咖啡", "浓缩萃取", "拉花", "教学"],
        "url": "https://xhslink.cn/o/75EwmlsxSZl",
        "summary": "核心判断：适合拉花的浓缩 = 传统拼配中深烘焙豆（1-3月内、防空气保存、养豆10-15天）×专业咖啡机与电磨×结果导向参数（流速三态调研磨；粉18.5-20g/水温88-90度/23-30秒/液重比1:1.5-1.7）；增粉量或降液重可更适配拉花但不保证更好喝。",
        "shots": 10, "segs": 239, "height": 2433,
    },
    {
        "slug": "extraction-latte-impact", "title": "萃取对拉花的影响：浓度决定图案",
        "duration": "3分07秒", "tags": ["咖啡", "萃取", "拉花", "浓度"],
        "url": "https://xhslink.cn/o/4FUwRukpITx",
        "summary": "核心判断：拉花成败由浓缩浓度决定——低浓度（14克粉）颜色浅偏水、图案变形带锯齿（偏酸无支撑）；高浓度（20克粉）像融化巧克力、图案最完整丝滑对比度高；拉花需要中高浓度，调节手段除粉量外还有研磨度与萃取比例。",
        "shots": 10, "segs": 22, "height": 2219,
    },
    {
        "slug": "asymmetric-beauty", "title": "不对称才美：国画构图的不平衡美学",
        "duration": "1分01秒", "tags": ["国画", "构图", "摄影", "美学"],
        "url": "https://xhslink.cn/o/5X3zqHfWLWy",
        "summary": "核心判断：构图好看的关键是拒绝对称——大块面避开上下中线（一半一半最难看，宁可偏天偏地）；主体放黄金分割点不放正中间；花叶枝统一朝右成「势」，用一片朝左的反叶四两拨千斤把势掰回来；拍人靠左靠右放三七出枝位。底层美学：在不平衡中求平衡，最忌四平八稳。",
        "shots": 8, "segs": 30, "height": 2295,
    },
    {
        "slug": "bone-face-over-skin", "title": "骨相脸一定大于皮相脸",
        "duration": "1分56秒", "tags": ["变美", "骨相", "审美"],
        "url": "https://xhslink.cn/o/3t2zYvu2ACl",
        "summary": "核心判断：自测定位风格（侧脸/拍照好看=骨相，正脸/本人好看=皮相），底层标准是面部高光点不同。三点区别——①调整重心：骨相讲眉弓转折（与额骨阶梯呼应）、颧骨高微凸、下颌角有角度，皮相线条柔和；②抗老：骨相越老特征越明显，皮相鼻基底凹陷+颧骨低→软组织下垂→鼻唇沟，三五年必垮；③上镜：骨相上镜更好看，保留适当缺陷=辨识度。",
        "shots": 12, "segs": 86, "height": 2465,
    },
    {
        "slug": "skirt-shoes-socks-outfit", "title": "裙子鞋袜万能穿搭技巧",
        "duration": "21秒", "tags": ["穿搭", "裙子", "鞋子"],
        "url": "https://xhslink.cn/o/6V1AjjXSsMf",
        "summary": "核心判断：裙鞋搭配=视觉量感与繁简的互补匹配——短裙露肤多配量感足、长裙配轻量平底；紧身裙配细跟、轻飘裙配重鞋；花哨裙配简洁鞋。具体方案：长裙→平底、短裙→长靴、开叉裙→高跟、碎花裙→小白鞋。",
        "shots": 9, "segs": 9, "height": 2388,
    },
    {
        "slug": "latte-champion-interview", "title": "提前感受拉花冠军的氛围",
        "duration": "6分51秒", "tags": ["咖啡", "拉花", "冠军", "采访"],
        "url": "https://xhslink.cn/o/AWHaQ0F3AJW",
        "summary": "核心判断：冠军拉花方法论——①深烘焙+新鲜豆（油脂丰富→线条稳定→对比分明）；②萃取习惯20克按杯型（300ml）微调；③奶温看油脂与图案复杂度动态调；④对比度=底色干净+线条清晰，底色一致性要高；⑤比赛心态：接受扣分但训练提前规避瑕疵。初学者先过浓缩+奶泡两关（选豆、流速标准偏慢、浓缩奶泡同时做、打好立刻拉）。",
        "shots": 12, "segs": 195, "height": 2480,
    },
    {
        "slug": "ultra-clear-video", "title": "3分钟学会拍出超清晰视频",
        "duration": "3分20秒", "tags": ["拍摄", "清晰度", "光线", "视频"],
        "url": "https://xhslink.cn/o/3tGRIxQrARt",
        "summary": "核心判断：视频清晰的本质是『反差』而非分辨率——光线不足产生噪点、细节模糊、主体背景糊在一起。两路解法：拍摄时制造明暗反差（45度单独打亮主体）+色彩反差（对比色）；后期补救（提对比度、调饱和度）。参数：4K拍摄（能二次构图）、4K导出、最高码率、H.264、电脑端网页上传。",
        "shots": 12, "segs": 84, "height": 2480,
    },
    {
        "slug": "forehead-beauty-standards", "title": "刘亦菲和张柏芝的额头，你更想do哪款？",
        "duration": "1分03秒", "tags": ["变美", "审美", "额头", "医美"],
        "url": "https://xhslink.cn/o/3Ktkep3cUh2",
        "summary": "核心判断：两款额头核心差异是额面起伏度——刘亦菲款=直面型（额面垂直、额结节浑圆、天庭与眉心无起伏，柔和温婉）；张柏芝款=起伏型（额结节精致清晰、花瓣型发际线、印堂眉心有高低落差，轻瘦高挺、精致明艳）。选款取决于浓颜/淡颜基础：浓颜衬起伏精致，淡颜适合柔和温婉。",
        "shots": 10, "segs": 31, "height": 2433,
    },
    {
        "slug": "flaws-to-classic", "title": "为何他们的缺点，能美成经典？",
        "duration": "2分35秒", "tags": ["变美", "审美", "辨识度", "明星"],
        "url": "https://xhslink.cn/o/7q1tTJKAgZp",
        "summary": "核心判断：辨识度的本质是『缺点与气质适配』——王祖贤的地包天成就美人三分抛的古典韵味（额面+上颌骨量充足、下巴不后缩）；李嘉欣的颧骨外阔因颞部包裹+头包脸趋势+颧结节内收曲线而明艳张扬；黄圣依的高眼位长中庭换得高智清冷感、虎牙换得少女感。结论：缺陷在美人脸上是辨识度，变美要保留特色。",
        "shots": 15, "segs": 102, "height": 2250,
    },
    {
        "slug": "luxury-brand-preference", "title": "为什么他们深受顶奢品牌的追捧",
        "duration": "3分05秒", "tags": ["审美", "面部美学", "电影脸", "顶奢"],
        "url": "https://xhslink.cn/o/7akVbmgtweL",
        "summary": "核心判断：顶奢品牌（LV、香奈儿、古驰、迪奥）钟爱的脸=有空间透视的电影脸——轮廓流畅之外还有从前向后的延伸感与横平竖直的骨骼结构，核心是上下两个平行四边形（上面部：颞线/太阳穴发际线/鬓角发际线/眉弓-颧弓连线，AB平行CD平行；下面部：颧弓后段/颧骨表现点/下颌拐点/下颌-颏部转折点，下颌两条线）。淡系平面脸上镜摊开；菱形脸/高颧骨=平行四边形缺失；错误审美只加宽太阳穴得到圆滚滚上庭；头重脚轻不符合顶奢审美。",
        "shots": 18, "segs": 84, "height": 2372,
    },
    {
        "slug": "high-cheekbone-forehead", "title": "高颧骨的他们算是把额头彻底玩明白了",
        "duration": "3分14秒", "tags": ["审美", "额头", "骨相", "发际线"],
        "url": "https://xhslink.cn/o/32YP6XFDbVd",
        "summary": "核心判断：发际线形状=额头骨相的外在表现，不是装饰品——无底子硬做花瓣发际线=贴片子违和。好看额头=上窄下宽梯形：额结节点位合适+眉弓视觉高光点外移→梯形成立→开阔额头弱化脸宽、包裹眉弓、呼应颧骨；反面=正方形额面扁平局促显脸长，调整后正梯形+外框C包裹颧弓。两个骨点分额顶（承接头骨）/额面（衔接T区）；额颞转折线（额结节+眉弓高光点）决定球形还是T面。隐藏细节：颞部饱满+卢米斯之圆=头包脸，而非单一高颅顶。",
        "shots": 19, "segs": 114, "height": 2372,
    },
    {
        "slug": "jianying-architecture", "title": "一个视频教会你剪映专业版底层架构",
        "duration": "12分34秒", "tags": ["剪映", "剪辑", "教程", "视频制作"],
        "url": "https://xhslink.cn/o/Ad8AIwVNoLm",
        "summary": "核心判断：剪映底层架构=界面三板块（效果栏/预览区/时间线）+效果栏功能链路。打开界面记住三点（模板直接出片/云空间同步/官方介绍不管），开始创作=主界面、退出实时保存草稿。素材（导入/收藏/AI素材/官方库）→音频（提取/链接/收藏/AI音乐/音乐库/音效）→文本（新建/智能包装/花字/模板/智能字幕+歌词+文稿匹配）→贴纸→特效（画面管环境/人物管人）→转场→字幕→滤镜（一键预设）→调节（调色：调节=整条时间线、调整=单片段）→模板（替换素材）→数字人。结语：上手才记住。",
        "shots": 18, "segs": 392, "height": 2633,
    },
    {
        "slug": "ai-digital-human", "title": "一个视频教会你 AI 数字人",
        "duration": "4分18秒", "tags": ["剪映", "AI数字人", "教程", "视频制作"],
        "url": "https://xhslink.cn/o/CvmNqVh9YC",
        "summary": "核心判断：剪映 AI 数字人=7步流水线。①入口=开始创作→数字人工具；②形象=定制（上传正面照生成）或内置（热门/超仿真/绿幕背景透明方便换背景，点形象预览听旁白）；③背景=先留空后续素材补充；④文案=粘贴或智能文案自动生成几组；⑤声音=克隆音色/主题/超仿真试听+勾选同时生成字幕；⑥合成=自动匹配语音动作、口型同步；⑦成片=素材库拖风景背景（长视频多段）、Ctrl+B分割删多余、分离原声一键删除、改9:16抖音格式。",
        "shots": 17, "segs": 118, "height": 2586,
    },
    {
        "slug": "jianying-editing-guide", "title": "从思路到精剪，剪映专业版剪辑全攻略",
        "duration": "23分13秒", "tags": ["剪映", "剪辑", "教程", "完整流程"],
        "url": "https://xhslink.cn/o/2Q164NO4tsx",
        "summary": "核心判断：剪映完整剪辑流程=八步。①思路=先定主题（新手最易忽略）；②素材=加号/拖拽导入媒体池，预览分清空镜/人物/同场景；③初剪=片头空镜开场、I/O键入出点、同场景成组异场景空镜过渡、分离音频去原声；④精剪=自由轨道逐段对齐音乐节奏、Command+B分割/Delete删除、Command+R变速（人物0.25倍空镜0.5倍，需120帧防掉帧）；⑤音乐=通用先剪再加、踩点先放按节拍剪；⑥歌词=智能文本识别；⑦音效=按画面联想（知了/风/布料/草地/鸟叫/海浪）音量调小点缀；⑧导出=1080P/MP4/30帧。心法：氛围靠慢放、节奏靠对齐、音效靠联想、学习靠练习。",
        "shots": 26, "segs": 558, "height": 2541,
    },
    {
        "slug": "jianying-hidden-features", "title": "剪映隐藏功能！让剪辑效率直接起飞",
        "duration": "12分07秒", "tags": ["剪映", "剪辑", "教程", "隐藏功能"],
        "url": "https://xhslink.cn/o/3IBCA7A91Ql",
        "summary": "核心判断：剪映时间线功能=三组。①顶部按钮：加号多时间线=多个独立工作区（Command+C复制→新建→Command+V粘贴=版本管理，改坏了回原版）；分割模式B（Command+B多轨同步分割）；左右全选（左括号/右括号）；撤销/重置；向左裁剪Q/向右裁剪W一步到位；Delete删除；标记=便利贴+音乐踩点；智能剪口播自动去语气词/重复/停顿。②右侧：麦克风配音录音、主轨道吸附（默认开=无缝，关=随意移）、磁铁（默认开=自动贴剪切点）、关闭联动（默认开=字幕音效跟主轨动，关=独立调整）、关闭预览S（卡顿就开）。③轨道左侧：小锁=锁定防误操作、隐藏轨道、关闭原声、独奏监听。④时间线操作：拖尾部双括号调时长、底部圆点=原声淡入淡出、音频中间横线=直接调音量、Command+R变速、右键/图标栏更多功能。心法：先搞清每个功能默认状态，短剪辑用快捷键、长剪辑用锁定，效率靠熟练。",
        "shots": 21, "segs": 336, "height": 2754,
    },
]


def main() -> None:
    data = json.loads(INDEX.read_text(encoding="utf-8"))
    existing = {
        e.get("outputs", {}).get("html", ""): e
        for e in data
        if isinstance(e.get("outputs"), dict)
    }

    added = 0
    for e in ENTRIES:
        slug = e["slug"]
        html_name = f"{slug}-图文实录.html"
        if html_name in existing:
            print(f"  ~ {slug} 已存在，跳过")
            continue
        entry = {
            "date": DATE,
            "title": e["title"],
            "summary": e["summary"],
            "tags": e["tags"],
            "platform": "xiaohongshu",
            "url": e["url"],
            "duration": e["duration"],
            "outputs": {
                "html": html_name,
                "svg": f"{slug}-理性分析.svg",
                "html_en": f"{slug}-场景英译.html",
                "html_en_type": "scene-english",
            },
            "screenshot_count": e["shots"],
            "transcript_segments": e["segs"],
            "svg_height": e["height"],
        }
        data.append(entry)
        added += 1
        print(f"  ✓ 新增 {slug}")

    json.dump(data, open(INDEX, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"新增 {added} 条，index.json 共 {len(data)} 条")


if __name__ == "__main__":
    main()
