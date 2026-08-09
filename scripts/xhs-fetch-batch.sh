#!/bin/bash
# 批量下载小红书视频（单实例；每篇前过限流器，请求开始时间间隔 >=60 秒）
# 用法: bash scripts/xhs-fetch-batch.sh v01 v02 ...
# 下载到工作区根目录（前缀命名，如 v01.source.mp4）
cd /Users/chenzhiheng/Projects/bilibili-workshop
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
ALL_KEYS=(v01 v02 v03 v04 v05 v06 v07 v08 v09 v10 v11 v12 v13 v14 v15)
ALL_URLS=(
  "http://xhslink.cn/o/8bnTzqVAMvT"
  "http://xhslink.cn/o/4J6bjUXtIsl"
  "http://xhslink.cn/o/1zBETKHZTC6"
  "http://xhslink.cn/o/kpR88JaAih"
  "http://xhslink.cn/o/24f7rAJOsDK"
  "http://xhslink.cn/o/2m3URy7Jyox"
  "http://xhslink.cn/o/2c438JwDNNG"
  "http://xhslink.cn/o/7QAxf2iYJP6"
  "http://xhslink.cn/o/2H7qD1cvv1c"
  "http://xhslink.cn/o/7LTACoUc8e3"
  "http://xhslink.cn/o/APxuTRL0nik"
  "http://xhslink.cn/o/6I0Gsupwsyf"
  "http://xhslink.cn/o/qjE7KV6b46"
  "http://xhslink.cn/o/4dCILnS6h6J"
  "http://xhslink.cn/o/12eJ5bjRLUB"
)
for k in "$@"; do
  u=""
  for i in "${!ALL_KEYS[@]}"; do
    if [ "${ALL_KEYS[$i]}" = "$k" ]; then u="${ALL_URLS[$i]}"; break; fi
  done
  if [ -z "$u" ]; then echo "=== 未知 key: $k ==="; continue; fi
  if [ -f "$k.source.mp4" ] && [ -s "$k.source.mp4" ]; then
    echo "=== $k 已存在，跳过 ==="
    continue
  fi
  node xhs-rate-limit.mjs
  echo "=== 下载 $k: $u ==="
  $PY scripts/xhs-fetch.py "$u" "$k" || echo "FAILED: $k"
  echo "=== 完成 $k ==="
done
echo "全部下载流程结束"
