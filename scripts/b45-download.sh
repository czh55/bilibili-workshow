#!/bin/bash
# b45 下载：--no-audio 下载视频，结束后手动抽音频（脚本内 ffmpeg 在后台易中断）
cd /Users/chenzhiheng/Projects/bilibili-workshop
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
FFMPEG=/opt/homebrew/bin/ffmpeg
KEYS=(e01 e02 e03 e04 e05 e06 e07 e08 e09)
URLS=(
  "http://xhslink.cn/o/2NnOyOfdlo3"
  "http://xhslink.cn/o/8nlFEp6PEU9"
  "http://xhslink.cn/o/61osLfkUpoT"
  "http://xhslink.cn/o/520YpUSJNKL"
  "http://xhslink.cn/o/2k1fCkClN7q"
  "http://xhslink.cn/o/cOwg6z2hk0"
  "http://xhslink.cn/o/8KywZvpaNFR"
  "http://xhslink.cn/o/7K4F5QCUxGV"
  "http://xhslink.cn/o/3bZGd47sE3f"
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
    echo "--- $k 第 $attempt 次失败，重试 ---"
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
