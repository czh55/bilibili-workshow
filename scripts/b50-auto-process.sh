#!/bin/bash
# b50 自动流水线：轮询检测新下载的 d*.source.mp4 -> 抽音频 -> Whisper 转录
# 与 b50-download.sh 并行运行，下载完成一个即处理一个。
cd /Users/chenzhiheng/Projects/bilibili-workshop

KEYS=(d01 d02 d03 d04 d05 d06 d07 d08 d09 d10 d11 d12 d13 d14)

FFMPEG=$(command -v ffmpeg)
[ -z "$FFMPEG" ] && FFMPEG=/opt/homebrew/bin/ffmpeg
PY=$(command -v python3)

while true; do
  # 1) 抽音频：有 mp4 无 m4a（xhs-fetch.py 一般已产出 m4a，这里兜底）
  for k in "${KEYS[@]}"; do
    src=$(ls "$k".source.* 2>/dev/null | head -1)
    if [ -n "$src" ] && [ ! -f "$k.m4a" ]; then
      "$FFMPEG" -y -i "$src" -vn -acodec aac -b:a 128k "$k.m4a" 2>/dev/null \
        && echo "=== 音频 $k 完成 ==="
    fi
  done

  # 2) 转录：有 m4a 无转录 json
  for k in "${KEYS[@]}"; do
    if [ -f "$k.m4a" ] && [ ! -f "$k.json" ]; then
      dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.m4a" 2>/dev/null | cut -d. -f1)
      echo "=== 转录 $k (${dur}s) ==="
      python3 -m whisper "$k.m4a" --model medium --language Chinese --output_dir . 2>&1 | tail -1
      [ -f "$k.json" ] && echo "=== $k 转录完成 ===" || echo "=== $k 转录可能失败 ==="
    fi
  done

  done_count=0
  for k in "${KEYS[@]}"; do
    [ -f "$k.json" ] && done_count=$((done_count + 1))
  done
  dl_count=$(ls d*.source.* 2>/dev/null | wc -l | tr -d ' ')
  echo "=== 进度: 转录 $done_count/14，已下载 $dl_count/14 ==="

  if [ "$done_count" -ge 14 ]; then
    break
  fi
  sleep 45
done

echo "=== b50 全量抽音频+转录结束 ==="
