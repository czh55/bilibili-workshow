#!/bin/bash
# b51 下载：23 个小红书视频串行下载（xhs-fetch.py 内置 60s 限流），
# 下载含抽音频，一次性产出 .source.mp4 + .m4a + .meta.json
# 跳过用户消息中的无效占位符 ${shortLink}（服装人干货｜网感细节图）
cd /Users/chenzhiheng/Projects/bilibili-workshop
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
[ -x "$PY" ] || PY=python3
KEYS=(e01 e02 e03 e04 e05 e06 e07 e08 e09 e10 e11 e12 e13 e14 e15 e16 e17 e18 e19 e20 e21 e22 e23)
URLS=(
  "https://xhslink.cn/o/AQP25hbPuL4"  # 咖啡饮品分层技巧
  "https://xhslink.cn/o/4PxLVPhJmrg"  # 箭头运镜详解
  "https://xhslink.cn/o/92s0axkNIX2"  # 轻美式复古穿搭 第5期
  "https://xhslink.cn/o/7RdjZLr0LOU"  # 旅行感来自人和环境的距离
  "https://xhslink.cn/o/9IOmy4ojBC0"  # 北外老师英语水平
  "https://xhslink.cn/o/3kYdwLBxKIf"  # 生命力出片6步
  "https://xhslink.cn/o/A3ZolOYhxrS"  # 便宜房子便宜车
  "https://xhslink.cn/o/3HFvas4qHz6"  # 甜酷亚系 coyseio
  "https://xhslink.cn/o/5D56l6F0aCR"  # 清冷少年感 林珍娜
  "https://xhslink.cn/o/HOlpyysG0v"   # 高质姐系 日系少年感
  "https://xhslink.cn/o/5TsysWZ6dtC"  # 鲸味穿搭
  "https://xhslink.cn/o/7PdkTfkPvvG"  # 韩女氛围感 4单品
  "https://xhslink.cn/o/4bd4CB5e9nR"  # 低噪穿搭 秋冬通勤
  "https://xhslink.cn/o/9JYjSNHOlvH"  # 审美附录 日杂街拍
  "https://xhslink.cn/o/79Vjd6VP5mf"  # 日杂街拍融入生活
  "https://xhslink.cn/o/4GxgHK1vXcY"  # 咖啡拉花 流距
  "https://xhslink.cn/o/9P6m0d1xOI"   # 均匀萃取 tips
  "https://xhslink.cn/o/89ICbrxOSb9"  # 色调大师课
  "https://xhslink.cn/o/9Y7xZ6BNuNY"  # 沉浸式调色保姆级
  "https://xhslink.cn/o/6zVuul0S9wV"  # 网球发球手臂
  "https://xhslink.cn/o/7WbgyyXKCud"  # 抽象VLOG三个公式
  "https://xhslink.cn/o/AZ3AYoYsNzj"  # 三大调色扭曲器
  "https://xhslink.cn/o/3UOax2nm5cF"  # 明度与纯度区别
)

for i in "${!KEYS[@]}"; do
  k="${KEYS[$i]}"; u="${URLS[$i]}"
  if [ -f "$k.source.mp4" ] && [ -s "$k.source.mp4" ] && [ -f "$k.meta.json" ]; then
    echo "=== $k 已存在，跳过 ==="
    continue
  fi
  echo "=== 开始 $k $u ==="
  "$PY" scripts/xhs-fetch.py "$u" "$k"
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "=== $k 失败 (rc=$rc)，继续下一个 ==="
  else
    echo "=== $k 完成 ==="
  fi
done
echo "=== 全部下载流程结束 ==="
