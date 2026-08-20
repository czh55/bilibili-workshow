#!/bin/bash
# b49 自动流水线：轮询检测新下载的 .source.mp4 -> 抽音频 -> Whisper 转录
# 与 b49-download.sh 并行运行，下载完成一个即处理一个。
cd /Users/chenzhiheng/Projects/bilibili-workshop

KEYS=(c01 c02 c03 c04 c05 c06 c07 c08 c09 c10 c11 c12 c13 c14 c15 c16 c17 c18 c19 c20 c21 c22 c23 c24)

FFMPEG=$(command -v ffmpeg)
WHISPER=$(command -v whisper)

if [ -z "$FFMPEG" ]; then FFMPEG=/opt/homebrew/bin/ffmpeg; fi

while true; do
  # 1) 抽音频：有 mp4 无 m4a
  for k in "${KEYS[@]}"; do
    if [ -f "$k.source.mp4" ] && [ ! -f "$k.m4a" ]; then
      "$FFMPEG" -y -i "$k.source.mp4" -vn -acodec aac -b:a 128k "$k.m4a" 2>/dev/null \
        && echo "=== 音频 $k 完成 ($(du -h "$k.m4a" 2>/dev/null | cut -f1)) ==="
    fi
  done

  # 2) 转录：有 m4a 无转录 json（whisper 对 cNN.m4a 输出 cNN.json，去掉扩展名）
  for k in "${KEYS[@]}"; do
    if [ -f "$k.m4a" ] && [ ! -f "$k.json" ]; then
      dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.m4a" 2>/dev/null | cut -d. -f1)
      echo "=== 转录 $k (${dur}s) ==="
      python3 -m whisper "$k.m4a" --model medium --language Chinese --output_dir . 2>&1 | tail -1
      echo "=== $k 完成 ==="
    fi
  done

  done_count=0
  for k in "${KEYS[@]}"; do
    [ -f "$k.json" ] && done_count=$((done_count + 1))
  done
  dl_count=$(ls c*.source.mp4 2>/dev/null | wc -l | tr -d ' ')
  echo "=== 进度: 转录 $done_count/24，已下载 $dl_count/24 ==="

  if [ "$done_count" -ge 24 ]; then
    break
  fi
  sleep 45
done

echo "=== b49 全量抽音频+转录结束 ==="
