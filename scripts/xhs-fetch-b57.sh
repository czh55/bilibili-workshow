#!/bin/bash
# b57: 9 条新小红书（主持表达 + 咖啡）；跳过已入库的 41kZeQUP6oQ / 32Grn8RIzTy
cd /Users/chenzhiheng/Projects/bilibili-workshop
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
KEYS=(b57a b57b b57c b57d b57e b57f b57g b57h b57i)
URLS=(
  "https://xhslink.cn/o/AuZje16MzUF"
  "https://xhslink.cn/o/AKsu46fhtFo"
  "https://xhslink.cn/o/4KwKxppQWJ"
  "https://xhslink.cn/o/5GUSBV1WqG7"
  "https://xhslink.cn/o/9NbGTZOCn14"
  "https://xhslink.cn/o/7h7ZbQWpbpY"
  "https://xhslink.cn/o/2D4CZQoofgP"
  "https://xhslink.cn/o/6EwQTplFPYE"
  "https://xhslink.cn/o/7HXJxpJzYjB"
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
