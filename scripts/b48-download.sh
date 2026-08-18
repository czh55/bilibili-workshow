#!/bin/bash
# b48 下载：12 个小红书视频串行下载（xhs-fetch.py 内置 60s 限流），
# --no-audio 下载视频，结束后统一抽音频（避免后台 ffmpeg 中断）。
cd /Users/chenzhiheng/Projects/bilibili-workshop
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
FFMPEG=/opt/homebrew/bin/ffmpeg
KEYS=(v01 v02 v03 v04 v05 v06 v07 v08 v09 v10 v11 v12)
URLS=(
  "https://xhslink.cn/o/1gqVKXOrNVY"
  "https://xhslink.cn/o/8TsYSymGw4o"
  "https://xhslink.cn/o/6lkYQliTehU"
  "https://xhslink.cn/o/75VSx2Jf71c"
  "https://xhslink.cn/o/8lHE9mjVYTv"
  "https://xhslink.cn/o/8wSI0L4wwFP"
  "https://xhslink.cn/o/37FdIdE1s6i"
  "https://xhslink.cn/o/9Ak8T6Ytfaf"
  "https://xhslink.cn/o/32blN5npW1r"
  "https://xhslink.cn/o/AhYuW8cvrKR"
  "https://xhslink.cn/o/Ab8mwlYPLOp"
  "https://xhslink.cn/o/424nLiPriOE"
)
for i in "${!KEYS[@]}"; do
  k="${KEYS[$i]}"; u="${URLS[$i]}"
  if [ -f "$k.source.mp4" ]; then
    echo "=== $k 已下载，跳过 ==="
    continue
  fi
  echo "=== 下载 $k ==="
  ok=0
  for attempt in 1 2 3; do
    echo "--- $k 尝试 $attempt ---"
    if $PY scripts/xhs-fetch.py "$u" "$k" --no-audio; then
      if [ -s "$k.source.mp4" ]; then ok=1; break; fi
    fi
    echo "--- $k 第 $attempt 次失败，等待重试 ---"
    sleep 5
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
