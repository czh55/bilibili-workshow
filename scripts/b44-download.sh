#!/bin/bash
# b44 下载：--no-audio 下载视频，结束后手动抽音频（脚本内 ffmpeg 在后台易中断）
cd /Users/chenzhiheng/Projects/bilibili-workshop
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
FFMPEG=/opt/homebrew/bin/ffmpeg
KEYS=(d01 d02 d03 d04 d05)
URLS=(
  "http://xhslink.cn/o/1EUOZAyW3oG"
  "http://xhslink.cn/o/gHWOvGdtC0"
  "http://xhslink.cn/o/42FBD3uWSZk"
  "http://xhslink.cn/o/kxX3TMQ6AY"
  "http://xhslink.cn/o/2u24mQwbYJm"
)
for i in "${!KEYS[@]}"; do
  k="${KEYS[$i]}"; u="${URLS[$i]}"
  if [ ! -f "$k.source.mp4" ]; then
    echo "=== 下载 $k ==="
    $PY scripts/xhs-fetch.py "$u" "$k" --no-audio
    echo "=== 完成 $k ==="
  else
    echo "=== $k 已下载，跳过 ==="
  fi
done
echo "=== 统一抽音频 ==="
for k in "${KEYS[@]}"; do
  if [ -f "$k.source.mp4" ] && [ ! -f "$k.m4a" ]; then
    $FFMPEG -y -i "$k.source.mp4" -vn -acodec aac -b:a 128k "$k.m4a" 2>/dev/null && echo "音频 $k.m4a 完成"
  fi
done
echo "全部下载流程结束"
