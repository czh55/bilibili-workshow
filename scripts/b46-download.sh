#!/bin/bash
# b46 下载：14 篇小红书，--no-audio 下载视频，结束后统一抽音频（后台运行 ffmpeg 易中断，故手动抽）
cd /Users/chenzhiheng/Projects/bilibili-workshop
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
FFMPEG=/opt/homebrew/bin/ffmpeg
KEYS=(f01 f02 f03 f04 f05 f06 f07 f08 f09 f10 f11 f12 f13 f14)
URLS=(
  "https://xhslink.cn/o/4BDSExAjKUZ"
  "https://xhslink.cn/o/6b69ZMrCcN5"
  "https://xhslink.cn/o/8gPYy4wTknF"
  "https://xhslink.cn/o/2g1D7cSYouu"
  "https://xhslink.cn/o/32blN5npW1r"
  "https://xhslink.cn/o/1rgHYtXW0lg"
  "https://xhslink.cn/o/ABYsItc0eGS"
  "https://xhslink.cn/o/rAS0m3ji1g"
  "https://xhslink.cn/o/AsYxaJBYRig"
  "https://xhslink.cn/o/89RPYhvmqMe"
  "https://xhslink.cn/o/5XVVLHQH1gX"
  "https://xhslink.cn/o/9odWCpnTXJk"
  "https://xhslink.cn/o/SEcA7gwdfZ"
  "https://xhslink.cn/o/6e5xXTYdpXa"
)
for i in "${!KEYS[@]}"; do
  k="${KEYS[$i]}"; u="${URLS[$i]}"
  if [ -f "$k.source.mp4" ] && [ -f "$k.meta.json" ]; then
    echo "=== $k 已下载，跳过 ==="
    continue
  fi
  echo "=== 下载 $k ==="
  ok=0
  for attempt in 1 2 3 4 5 6; do
    echo "--- $k 尝试 $attempt ---"
    if $PY scripts/xhs-fetch.py "$u" "$k" --no-audio; then
      if [ -s "$k.source.mp4" ] && [ -s "$k.meta.json" ]; then ok=1; break; fi
    fi
    echo "--- $k 第 $attempt 次失败，180 秒冷却后重试（风控窗口） ---"
    sleep 180
  done
  if [ "$ok" = "1" ]; then
    echo "=== 完成 $k ==="
  else
    echo "=== $k 多次尝试仍失败 ==="
  fi
done
echo "=== 统一抽音频 ==="
for k in "${KEYS[@]}"; do
  if [ -f "$k.source.mp4" ] && [ ! -f "$k.m4a" ]; then
    $FFMPEG -y -i "$k.source.mp4" -vn -acodec aac -b:a 128k "$k.m4a" 2>/dev/null && echo "音频 $k.m4a 完成"
  fi
done
echo "全部下载流程结束"
