#!/bin/bash
# b50 下载：14 个小红书视频串行下载（xhs-fetch.py 内置 60s 限流），
# 下载含抽音频，一次性产出 .source.mp4 + .m4a + .meta.json
cd /Users/chenzhiheng/Projects/bilibili-workshop
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
[ -x "$PY" ] || PY=python3
KEYS=(d01 d02 d03 d04 d05 d06 d07 d08 d09 d10 d11 d12 d13 d14)
URLS=(
  "https://xhslink.cn/o/9MqPNKA33FQ"
  "https://xhslink.cn/o/6DWfzldxlgw"
  "https://xhslink.cn/o/AevRrQbFItb"
  "https://xhslink.cn/o/874xMKvHEdF"
  "https://xhslink.cn/o/947KAfQ6d2o"
  "https://xhslink.cn/o/470wpG6zFLv"
  "https://xhslink.cn/o/8b4HbiFni3b"
  "https://xhslink.cn/o/7CwyoYiyoib"
  "https://xhslink.cn/o/1dcUcoV877r"
  "https://xhslink.cn/o/7wttcbBXnW"
  "https://xhslink.cn/o/4K2ablmHHbj"
  "https://xhslink.cn/o/2XIklA1WYa6"
  "https://xhslink.cn/o/85o21bnOryy"
  "https://xhslink.cn/o/95ranq8YKok"
)

for i in "${!KEYS[@]}"; do
  k="${KEYS[$i]}"; u="${URLS[$i]}"
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
