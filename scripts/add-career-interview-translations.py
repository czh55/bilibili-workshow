#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为求职/职场话题的 60 条图注追加英文翻译到 translations.json（幂等）。"""
import json
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "translations.json"
t = json.loads(P.read_text(encoding="utf-8"))

NEW = {
    # barber-price-difference（理发价格差异）
    "向楼下开理发店的阿姨请教：30块和80块差在哪": "Asked the auntie who runs the barbershop downstairs: what's the real difference between a 30-yuan and an 80-yuan haircut?",
    "超低价活动79块三次=学徒练手，别贪便宜": "A rock-bottom deal of 79 yuan for three cuts means apprentice practice — don't chase the bargain",
    "不会货不对板：高价位托尼不拿底薪，宁可闲着": "You'll never get bait-and-switch here: premium Tonys aren't on a base salary, so they'd rather sit idle than take a discount client",
    "剪发不赚钱，烫发染发才是理发店的利润核心": "Cuts barely make money — perms and color are where a salon actually profits",
    "药水毛利率翻10倍都不止，老板不会告诉你": "Salon chemicals carry a 10x-plus gross margin — something the boss will never tell you",
    # big-company-jargon-evolution（大厂黑话进化）
    "第一年：说人话，加宣传内容，明天下班前交付": "Year one: speak plainly, sprinkle in some self-promotion, deliver before tomorrow's end of day",
    "第二年：宣传看似简单实则不然，需要一到两周": "Year two: the self-promotion looks easy but really isn't — it needs one to two weeks",
    "第五年：黑话连篇，感知赛道、归因分析、信息透传": "Year five: jargon galore — track sensing, attribution analysis, info pass-through",
    "各部门对焦抓手、串联咬合，方案要100万预算": "Departments all align on the key lever and mesh together — and the plan needs a 1 million budget",
    "老板：要这么多钱啊，那还是算了吧": "Boss: that much money? Then let's just forget it",
    # childfree-life-preparation（不婚不育的准备）
    "选择不结婚不生子，要做好两个准备": "If you choose no marriage and no kids, be prepared for two things",
    "头疼脑热、身体衰弱时，身边没有至亲陪伴": "When you get sick or grow frail, there's no close family by your side",
    "五十多岁再后悔就迟了，世上没有后悔药": "Regret in your fifties is too late — there's no cure for regret in this world",
    "婚姻本质是经济合伙人制，抗风险能力更强": "Marriage is essentially an economic partnership — it makes you far more resilient to risk",
    # company-research-interview（面试前研究公司）
    "「我不太了解你们公司」=三个丢分信号：不重视、兴趣一般、没认真对待": "“I don't know much about your company” equals three lost-point signals: you don't value them, you're mildly interested, and you didn't take it seriously",
    "基础一：行业、业务、盈利模式、成立时长、规模": "Basics one: industry, business, profit model, years in operation, and scale",
    "基础三：产品或服务有哪些特点": "Basics three: what stands out about their products or services",
    "加分项：业绩口碑、竞争对手、相对竞品的优劣势": "Bonus points: track record and reputation, competitors, and strengths and weaknesses against rivals",
    # competency-interview-answer（胜任力面试）
    "压力题：答不好直接影响面试结果和定级水平": "Pressure questions: a weak answer directly hurts your interview result and the level you're graded at",
    "四步框架：先观点→再理由→补案例→重申观点": "Four-step framework: state your point → give reasons → back it with a case → restate your point",
    "第一步表明观点：和岗位非常匹配，很适合这份工作": "Step one, state your point: a strong match, a great fit for this job",
    "数据案例：8年经验、合同超4000万、营收破1000万": "Data case: 8 years of experience, contracts worth over 40 million, revenue past 10 million",
    # housing-market-asset-allocation（房产与资产配置）
    "房价在跌还要不要买房：要买你就买，置换的正在买": "Should you buy while prices fall? If you're going to buy, buy — the trade-up buyers already are",
    "经济越不好越集中大中城市，大城市安全垫最厚": "The worse the economy, the more people crowd into big cities, where the safety cushion is thickest",
    "M2 12.9%：换到以前，房价就涨上天了": "M2 at 12.9%: back in the day, that alone would've sent home prices through the roof",
    "该买的保险买、该存的款存、该买的房买": "Buy the insurance you need, save the savings you need, buy the house you need",
    # judge-future-boss-interview（面试判断领导）
    "痛点开场：工作越干越没劲、看不到成长是因为跟错领导": "Pain-point opening: work drains you and growth stalls because you followed the wrong leader",
    "看尊重：面试体验好、热情解答问题，趾高气扬的不是好领导": "Check respect: a good interview experience, eager answers — a condescending one is not a good leader",
    "看专业：深度探讨业务细节，专业不如你的成长有限": "Check expertise: dig deep into business details — a leader less skilled than you caps your growth",
    "看开放：是否接纳合理建议，一味否定打击你被PUA概率高": "Check openness: do they accept sound suggestions? Constant rejection means a high chance of getting PUA'd",
    "看激情：讲业务讲团队时眼睛放光的领导值得跟随": "Check passion: a leader whose eyes light up talking business and team is worth following",
    # marital-status-interview-answer（婚姻状况回答）
    "问婚姻状况的两个用意：工作精力投入度＋稳定性": "The two intentions behind asking marital status: how much energy you'll give the job, plus your stability",
    "未婚未孕有对象：说工作计划＋已定居的强稳定性": "Single, no kids, in a relationship: talk your work plan plus the strong stability of having settled down",
    "已婚已孕：职业目标＋给孩子树榜样＋无后顾之忧": "Married with kids: career goals, setting an example for the child, and no worries behind you",
    "已婚未孕：先打基础＋近期无生育计划＋家人一致": "Married, no kids yet: build the foundation first, no baby plans soon, and family is on the same page",
    # no-promotion-pressure-interview（多年未晋升压力题）
    "场景设定：上一份工作干了四五年没升职": "The setup: you spent four or five years at your last job without a promotion",
    "面试官质疑「为什么这么久没有晋升」，典型压力面试题": "The interviewer challenges: “why no promotion in all that time?” — a classic stress-interview question",
    "顺着面试官意思解释就会把自己带进坑里": "Explaining along the interviewer's line of thinking walks you straight into a trap",
    "破法：跳出坑，从自己角度、三个维度回答": "The way out: step off the trap and answer from your own angle, across three dimensions",
    "维度一：行业经验与专业能力成长明显，才是最实惠的": "Dimension one: clear growth in industry experience and skills — that's what really pays off",
    # save-money-critical-thinking（存钱与批判性思维）
    "存不下钱的根因：大学缺一门批判性思维通识课": "The root cause of not saving: college missed a required course in critical thinking",
    "广场绳索比喻：每根绳子都拉在商家手里": "The town-square rope metaphor: every rope is pulled by the merchants' hands",
    "批判性思维是抵抗营销影响的思想免疫系统": "Critical thinking is the mental immune system that resists marketing influence",
    "肉松小贝网红店排队一小时，半年后关门": "The viral meat-floss cake shop had an hour-long line — and closed six months later",
    "把税后工资÷22÷7算时薪，计入排队成本": "Divide your after-tax salary by 22 then by 7 for an hourly wage, and count that queue time as cost",
    # self-intro-story-framework（自我介绍框架）
    "开场：自我介绍决定面试官对你的第一印象": "Opening: your self-introduction decides the first impression you leave on the interviewer",
    "最大误区：把简历简单复述一遍，等于面试官看简历就够": "The biggest mistake: simply reciting your resume — then the interviewer might as well have just read it",
    "面试官的目的：热身+建立第一印象，要短时间抓住注意力": "The interviewer's goal: warm-up plus first impression — you must grab attention in a short time",
    "四步法一二：履历分阶段，讲每阶段的重要产出与成长": "Steps one and two: split your career into phases and talk about each phase's key output and growth",
    "四步法三四：总结核心优势、讲清求职诉求": "Steps three and four: summarize your core strengths and spell out what you're seeking",
    # settle-for-offer-or-wait（将就offer还是等待）
    "粉丝困境：毕业玩了好几个月，找不到满意工作越来越慌": "A fan's dilemma: months of fun after graduation, no satisfying job found, and the panic grows",
    "立场：通常不建议仓促入职然后骑驴找马": "My stance: normally I wouldn't rush into a job while still scouting for something better",
    "将就的后果：交不出业绩恶性循环，或忘了求职初心": "The cost of settling: a vicious cycle of missing targets, or forgetting why you started job hunting",
    "两面看：一般岗位求职周期1-3个月": "Look at both sides: for average roles, the job search takes 1-3 months",
    "三个月全力以赴仍无满意offer，说明目标与实际差异大": "If three months of full effort still yields no satisfying offer, your goal and reality are far apart",
    # workplace-task-pushback-solutions（任务推不动的解法）
    "推不动的事大概率跟KPI没关系": "Things that won't move usually have nothing to do with your KPI",
    "大家心里：办你的事就没时间办自己的事": "What everyone thinks: do your thing, and there's no time left for mine",
    "把「我的事」变成「我们的事」：挂钩利益或造成风险": "Turn “my business” into “our business”: tie it to their interests or make it a risk to them",
    "拆解任务：拆到实习生都能做的傻瓜程度": "Break the task down — to fool-proof steps even an intern can do",
    "只选一条？我选利益挂钩": "Only pick one? I'd go with tying it to interests",
}

assert len(NEW) == 60, f"expected 60 entries, got {len(NEW)}"

added = skipped = 0
for zh, en in NEW.items():
    if zh in t:
        skipped += 1
    else:
        t[zh] = en
        added += 1

P.write_text(json.dumps(t, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

missing = [k for k in NEW if not t.get(k)]
print(f"added={added} skipped={skipped} total={len(t)}")
print(f"missing_or_empty={len(missing)}")
