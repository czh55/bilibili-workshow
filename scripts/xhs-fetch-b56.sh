#!/bin/bash
# b56: 6 条小红书咖啡笔记下载（前缀 b56a–b56f，避免与旧 c01 冲突）
cd /Users/chenzhiheng/Projects/bilibili-workshop
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
KEYS=(b56a b56b b56c b56d b56e b56f)
URLS=(
  "https://xhslink.cn/o/41kZeQUP6oQ"
  "https://xhslink.cn/o/4bBnhgGAYAe"
  "https://xhslink.cn/o/5APTJtXX0eM"
  "https://xhslink.cn/o/32Grn8RIzTy"
  "https://xhslink.cn/o/53Oq6q9mHU2"
  "https://xhslink.cn/o/4M3PrjZbfhv"
)
for i in "${!KEYS[@]}"; do
  k="${KEYS[$i]}"
  u="${URLS[$i]}"
  if [ -f "$k.source.mp4" ] && [ -s "$k.source.mp4" ]; then
    echo "=== $k 已存在，跳过 ==="
    continue
  fi
  echo "=== 下载 $k: $u ==="
  "$PY" scripts/xhs-fetch.py "$u" "$k" || echo "FAILED: $k"
  echo "=== 完成 $k ==="
done
echo "全部下载流程结束"
