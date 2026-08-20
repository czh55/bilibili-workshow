#!/bin/bash
# b49 下载：24 个小红书视频串行下载（xhs-fetch.py 内置 60s 限流），
# --no-audio 下载视频，结束后统一抽音频。
cd /Users/chenzhiheng/Projects/bilibili-workshop
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
FFMPEG=/opt/homebrew/bin/ffmpeg
KEYS=(c01 c02 c03 c04 c05 c06 c07 c08 c09 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24)
URLS=(
  "https://xhslink.cn/o/4ecxjgKmcvn"
  "https://xhslink.cn/o/4QKZKMKi6TA"
  "https://xhslink.cn/o/2QtqKPrcUq8"
  "https://xhslink.cn/o/75EwmlsxSZl"
  "https://xhslink.cn/o/4FUwRukpITx"
  "https://xhslink.cn/o/6QD3nFkpiNA"
  "https://xhslink.cn/o/3t2zYvu2ACl"
  "https://xhslink.cn/o/6V1AjjXSsMf"
  "https://xhslink.cn/o/AWHaQ0F3AJW"
  "https://xhslink.cn/o/3tGRIxQrARt"
  "https://xhslink.cn/o/3Ktkep3cUh2"
  "https://xhslink.cn/o/7q1tTJKAgZp"
  "https://xhslink.cn/o/7akVbmgtweL"
  "https://xhslink.cn/o/32YP6XFDbVd"
  "https://xhslink.cn/o/Ad8AIwVNoLm"
  "https://xhslink.cn/o/CvmNqVh9YC"
  "https://xhslink.cn/o/2Q164NO4tsx"
  "https://xhslink.cn/o/3IBCA7A91Ql"
  "https://xhslink.cn/o/5P9dgZdWcX1"
  "https://xhslink.cn/o/5pL2JTYIJxG"
  "https://xhslink.cn/o/6GOX8FDv7O0"
  "https://xhslink.cn/o/9GEu0Ozo9WH"
  "https://xhslink.cn/o/7fXZzEbgErz"
  "https://xhslink.cn/o/AdnHRS4Fk1t"
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
