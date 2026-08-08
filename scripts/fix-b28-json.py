#!/usr/bin/env python3
"""批28：为10篇旅行转场/运镜/相机噪点JSON补全 practice/pitfalls/shifts/footer_notes。"""
import json
from pathlib import Path

DATA = Path("/Users/chenzhiheng/Projects/bilibili-workshop/scripts/scene-data")

ENRICH = {
"travel-10-transitions": {
 "practice": [
   ["说走路转场的核心", "A walking match cut is the most brainless travel trick."],
   ["说动作匹配的精髓", "Repeat the same move in every scene, then stitch them together."],
   ["说擦肩而过的宿命感", "Shot one brushes past, shot two turns back—pure destiny."],
   ["说躺平转场的细节", "The fall direction must match the next shot's motion."],
   ["说同构图转场原理", "Similar mood or motion in different shots fools the brain."]
 ],
 "pitfalls": [
   ["Using flashy transitions", "Using action matches", "动作匹配最丝滑，不需要花哨特效"],
   ["Turning too late in the shot", "Turning at the edit point", "转身时机要落在剪辑点上"],
   ["Changing motion direction", "Keeping one fall direction", "躺平转场前后运动方向必须一致"],
   ["Shooting random clips", "Repeating the same move", "每个场景重复相同动作才能串联"]
 ],
 "shifts": [
   ["以前以为转场靠特效", "现在用动作匹配+连续运动方向"],
   ["以前每个镜头都想不同", "现在相同动作重复成为风格"],
   ["以前剪不好就加转场", "现在先检查运动方向是否一致"]
 ],
 "footer": "动作匹配是转场万金油：相同动作+连续运动方向即可骗过大脑。四种转场（走路/转身/躺平/同构图）本质都是『画面有连续性，观众自己脑补过渡』。"
},
"travel-7-camera-moves": {
 "practice": [
   ["说自拍拉远的瞬间", "Pull the lens back suddenly while self-shooting."],
   ["说遮挡物转场", "End shot one on an obstacle, start shot two emerging from it."],
   ["说希区柯克变焦", "Changing the camera-subject distance freezes time."],
   ["说环绕运镜的构图", "Turn on the rule of thirds and center the subject."]
 ],
 "pitfalls": [
   ["Pulling back too fast", "Pulling back on the turn moment", "拉远过快会失去回头瞬间感"],
   ["Entering the frame instantly", "Emerging from the obstacle", "第二画面入镜太快会穿帮"],
   ["Varying the orbit distance", "Keeping one orbit radius", "环绕距离忽远忽近构图不稳"],
   ["Shooting one long take", "One move per take, then join", "一条镜头只做一个动作再拼接"]
 ],
 "shifts": [
   ["以前运镜就是一条长镜头", "现在一条镜头只做一个动作，多拍组合"],
   ["以前觉得好镜头靠设备", "现在回头时机与遮挡物更出效果"],
   ["以前构图凭感觉", "现在开三分线保证构图一致"]
 ],
 "footer": "7 种运镜都基于推拉摇移+遮挡+变焦的组合。核心心法：一条镜头只表达一个动作，通过后期拼接实现『意外感』和『无缝感』。"
},
"yunjing-rs4mini-tips": {
 "practice": [
   ["说先环境后人物", "Push in on the scenery, then reveal the subject."],
   ["说环绕镜头细节", "Let their gaze follow the camera for a natural look."],
   ["说格莱美运镜", "As the subject turns, glide the camera the opposite way."],
   ["说组合运镜", "Tilt down and push in to go from sky to subject."],
   ["说智能追踪", "A simple gesture locks the subject and auto-orbits."]
 ],
 "pitfalls": [
   ["Long opening before the reveal", "Reveal the subject within seconds", "开场前摇太长观众会划走"],
   ["Orbiting too small an arc", "Orbiting a full half circle", "环绕幅度太小看不出环绕感"],
   ["Walking out of range", "Staying within ten meters", "追踪模块十米外会丢人物"],
   ["Keeping the camera locked", "Adding one move per shot", "固定机位拍多了会无聊"]
 ],
 "shifts": [
   ["以前运镜等于手持乱晃", "现在运镜是有起承转合的一个句子"],
   ["以前一个机位拍到底", "现在先环境后人物/环绕/反向运镜讲故事"],
   ["以前一个人拍不了跟拍", "现在手势追踪实现第三视角"]
 ],
 "footer": "运镜不是炫技，是为叙事服务。『先环境后人物』适合开场收尾，『环绕』表现空间，『格莱美反向』制造张力。新手从这 4 招起步即可。"
},
"pocket4p-4-transitions": {
 "practice": [
   ["说广角引入", "Shoot wide at 20mm, let them run in, then dolly back."],
   ["说中焦压缩感", "60mm gives obvious spatial compression."],
   ["说超广角灵魂帧", "With the accessory the focal length drops to 16mm."],
   ["说慢动作后退", "Shoot the middle at 4K/240fps and step back fast."],
   ["说动态范围", "Open the low-light cover early for 17 stops of dynamic range."]
 ],
 "pitfalls": [
   ["Blocking the lens too early", "Blocking as the prop flies past", "遮挡时机要落在动作节点"],
   ["Cutting the middle frame short", "Keeping the blackout beat", "敲击转场中间帧要留黑场"],
   ["Using one lens for everything", "Swapping wide/mid/ultra-wide", "转场靠多焦段分工"],
   ["Shaking during the fall shot", "Locking focus in PV mode", "摔倒转场先锁焦再晃机"]
 ],
 "shifts": [
   ["以前转场靠后期特效", "现在转场是拍摄现场设计的动作"],
   ["以前一支镜头拍到底", "现在广角/中焦/超广角各司其职"],
   ["以前夜晚只拍黑", "现在敢用17档动态范围拍大光比"]
 ],
 "footer": "OP4P 四转场共同点：都靠『遮镜头黑场』或『动作匹配』完成。广角拍环境、60mm 拍人像、超广角做灵魂帧——镜头的选择就是叙事的选择。"
},
"travel-transition-4tips": {
 "practice": [
   ["说制造擦肩而过", "Rotate near the shoulder, then cut to turning from behind it."],
   ["说躺平转场反差", "The lie-down cut gets better with bigger contrast."],
   ["说走路转场构图", "Center the subject and use the rule of thirds."],
   ["说相似动作转场", "Any visual similarity can carry a transition."]
 ],
 "pitfalls": [
   ["Panning wide of the subject", "Keeping the walker centered", "走路转场人物出画会断"],
   ["Over-matching the action", "Accepting loose similarity", "相似动作过度贴合反而僵硬"],
   ["Using a tiny prop", "Using a bag or large object", "遮挡物太小观众一眼看穿"],
   ["Editing without a rhythm", "Letting motion direction flow", "忽略运动方向拼接会跳"]
 ],
 "shifts": [
   ["以前旅拍靠运气", "现在转场运镜都能现场人为制造"],
   ["以前每画面独立好看", "现在画面间有相似性就能转场"],
   ["以前追求完美贴合", "现在有相似性即可，松弛感更重要"]
 ],
 "footer": "四组合本质：运镜创造运动，转场连接运动。不用追求完美贴合，画面间只要有相似性（动作/构图/情绪）就能完成丝滑转场。"
},
"action-cam-vlog-5-tips": {
 "practice": [
   ["说磁吸第一视角", "Tape magnets to a pen and film its first-person view."],
   ["说新奇视角", "Place the camera where it can't normally go for novelty."],
   ["说慢动作", "Use slow motion and let chopped veggies fall slowly."],
   ["说小车运镜", "Mount it on an RC car to shoot push-pull solo."],
   ["说Vlog调色", "Before grading Vlog footage, do a color restore."]
 ],
 "pitfalls": [
   ["Handheld shake", "Holding with both hands", "第一视角太晃要扶稳或开防抖"],
   ["Shooting only eye-level", "Placing it on doors or in snow", "视角不够新奇就没有记忆点"],
   ["Grading without a restore", "Doing a color restore first", "Vlog模式调色前必须先色彩还原"],
   ["Over-cropping in post", "Using the 8K headroom", "放大超过200%画质会崩"]
 ],
 "shifts": [
   ["以前运动相机只拍运动", "现在磁吸视角让日常物件开口说话"],
   ["以前第三人称镜头死板", "现在放到门里雪里做新奇视角"],
   ["以前直出颜色发灰", "现在Vlog模式+还原，先调光再调色"]
 ],
 "footer": "运动相机正确打开方式=视角创新+慢动作+自动运镜+Vlog 调色。重点不是参数，而是『让观众看到平时看不到的视角』。"
},
"vlog-panorama-8-tricks": {
 "practice": [
   ["说特写引入", "Open on a close-up, then follow an object to reveal the person."],
   ["说凑近反差", "To emphasize something, bring it close for contrast."],
   ["说镜子场景", "Use the full view for mirror scenes without catching the camera."],
   ["说先环境后人物", "Panorama lets you do environment-first reveals."],
   ["说甩镜转场", "Whip in the same direction and join them in the editor."]
 ],
 "pitfalls": [
   ["Misplaying the invisible stick", "Aligning body and stick in a line", "手持时杆子不对齐会穿帮"],
   ["Setting up a tripod in wind", "Shooting in windless conditions", "有风环境画面会晃动"],
   ["Forgetting night mode", "Using super-night mode", "夜景忘记开超级夜景噪点多"],
   ["Mixing motion directions", "Keeping both clips aligned", "甩镜转场方向不一致会跳"]
 ],
 "shifts": [
   ["以前vlog靠剪辑", "现在拍摄选全景，后期随时重构图"],
   ["以前转场要重拍", "现在一次全景视频后期反复取景"],
   ["以前人物必须正对镜头", "现在先环境后人物，出场即叙事"]
 ],
 "footer": "全景相机的核心优势是『后期取景』：一次拍摄，无数种运镜可能。8 招本质都是利用全景信息密度+后期视角调整，一个人也能拍出团队感。"
},
"cinematic-vlog-tips": {
 "practice": [
   ["说快切", "Insert short detail shots between longer takes."],
   ["说跳切", "Delete the middle frames to tighten the rhythm."],
   ["说移动延时", "Try a hyper-lapse so one long shot stops feeling flat."],
   ["说陌生化", "Shooting through glass creates defamiliarization."],
   ["说关键帧放大", "Slowly zoom with keyframes and add captions for depth."]
 ],
 "pitfalls": [
   ["Cutting every second", "Keeping breathing room", "快切太多观众会看晕"],
   ["Deleting the story beats", "Cutting only redundant frames", "跳切删太多叙事会断裂"],
   ["Zooming past 200%", "Staying within the 8K headroom", "裁切超过200%画质崩"],
   ["Using strange angles everywhere", "Reserving them for key shots", "陌生化视角滥用会出戏"]
 ],
 "shifts": [
   ["以前电影感等于贵设备", "现在节奏和质感两个法宝就能实现"],
   ["以前一个镜头拍很久", "现在快切跳切让时间由剪辑掌控"],
   ["以前画质等于像素", "现在8K的意义是裁切空间大"]
 ],
 "footer": "电影感=节奏×质感。节奏靠快切/跳切/延时/移动延时，质感靠高画质/色调/陌生化视角。设备只是载体，思维才是核心。"
},
"high-iso-less-noise": {
 "practice": [
   ["说等亮度对比", "Brighten the low-ISO shot to match and noise is about the same."],
   ["说电压放大", "At ISO 400 the voltage is amplified 4x."],
   ["说ISO不变性", "Strong read-noise control makes high ISO pointless."],
   ["说曝光取舍", "If you just need brightness on the subject, raise ISO boldly."]
 ],
 "pitfalls": [
   ["Comparing only straight-out shots", "Comparing at equal brightness", "不控制亮度变量的对比不公平"],
   ["Blaming ISO alone", "Blaming low light and signal", "噪点多源于进光量不足而非ISO"],
   ["Cranking ISO without limit", "Weighing dynamic range", "无脑拉高ISO会损失动态范围"],
   ["Forgetting back-end noise", "Noting front/back read noise", "忽略前端后端读出噪声之分"]
 ],
 "shifts": [
   ["以前高ISO等于噪点多", "现在等亮度下高ISO反而略干净"],
   ["以前ISO是画质杀手", "现在ISO只是模拟放大，后端读出噪声才是放大主因"],
   ["以前一套ISO走天下", "现在按场景权衡信噪比与动态范围"]
 ],
 "footer": "核心结论：进光量决定散粒噪声信噪比，ISO 只是模拟放大。同亮度对比下高 ISO 因压制后端读出噪声反而略优，这就是 ISO 不变性。"
},
"image-noise-snr": {
 "practice": [
   ["说噪声的本质", "Every stage—capture, transfer, convert, quantize—adds error."],
   ["说散粒噪声", "Photons arrive randomly, so pixels catch uneven numbers of them."],
   ["说向右曝光", "The best SNR boost is more light without clipping."],
   ["说读出噪声", "Raising ISO amplifies front-end read noise too."]
 ],
 "pitfalls": [
   ["Blaming the sensor size", "Blaming photon randomness", "散粒噪声源于光子随机性而非像素大小"],
   ["Exposing to the right blindly", "Stopping before clipping", "向右曝光过头会丢失高光"],
   ["Only denoising in post", "Adding light at capture time", "后期降噪治标，进光量才治本"],
   ["Treating noise as one thing", "Separating shot and read noise", "散粒噪声与读出噪声机制不同"]
 ],
 "shifts": [
   ["以前噪点是玄学", "现在两种机制都能量化"],
   ["以前ISO越低越好", "现在信噪比由光子数量决定，曝光优先"],
   ["以前拼命后期降噪", "现在拍摄时增加进光量才是治本"]
 ],
 "footer": "噪点=信号采集传输量化误差的累积。散粒噪声靠进光量改善（向右曝光），读出噪声靠 ISO 模拟放大压制后端部分。理解信噪比，噪点就不可怕。"
}
}

for p in sorted(DATA.glob("*.json")):
    slug = p.stem
    if slug not in ENRICH:
        continue
    d = json.loads(p.read_text(encoding="utf-8"))
    d["practice"] = ENRICH[slug]["practice"]
    d["pitfalls"] = ENRICH[slug]["pitfalls"]
    d["shifts"] = ENRICH[slug]["shifts"]
    d["footer_notes"] = ENRICH[slug]["footer"]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ {slug}")
print("完成")
