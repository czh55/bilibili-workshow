#!/bin/bash
# b52 自动流水线：轮询 h01–h106，有 m4a 即 Whisper medium 中文转录
# 与 b52-download.sh 并行运行
cd /Users/chenzhiheng/Projects/video-notes

KEYS=()
for n in $(seq 1 106); do
  KEYS+=("$(printf 'h%02d' "$n")")
done

FFMPEG=$(command -v ffmpeg)
[ -z "$FFMPEG" ] && FFMPEG=/opt/homebrew/bin/ffmpeg

while true; do
  for k in "${KEYS[@]}"; do
    src=$(ls "$k".source.* 2>/dev/null | head -1)
    if [ -n "$src" ] && [ ! -f "$k.m4a" ]; then
      "$FFMPEG" -y -i "$src" -vn -acodec aac -b:a 128k "$k.m4a" 2>/dev/null \
        && echo "=== 音频 $k 完成 ==="
    fi
  done

  for k in "${KEYS[@]}"; do
    need=0
    if [ -f "$k.m4a" ]; then
      if [ ! -f "$k.json" ]; then
        need=1
      elif [ -n "$(ls "$k".source.* 2>/dev/null)" ] && [ "$k.json" -ot "$(ls "$k".source.* 2>/dev/null | head -1)" ]; then
        # 仅当转录明显早于本批新视频时重转；避免误伤
        :
      fi
    fi
    if [ "$need" -eq 1 ]; then
      dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.m4a" 2>/dev/null | cut -d. -f1)
      echo "=== 转录 $k (${dur}s) ==="
      python3 -m whisper "$k.m4a" --model medium --language Chinese --output_dir . 2>&1 | tail -5
      [ -f "$k.json" ] && echo "=== $k 转录完成 ===" || echo "=== $k 转录可能失败 ==="
    fi
  done

  done_count=0
  for k in "${KEYS[@]}"; do
    [ -f "$k.json" ] && done_count=$((done_count + 1))
  done
  dl_count=$(ls h*.source.* 2>/dev/null | wc -l | tr -d ' ')
  echo "=== 进度: 转录 $done_count/106，已下载 $dl_count/106 ==="

  if [ "$done_count" -ge 106 ]; then
    break
  fi
  # 下载脚本结束后若仍有缺口，继续等一会儿
  if ! pgrep -f 'b52-download.sh' >/dev/null 2>&1; then
    pending=0
    for k in "${KEYS[@]}"; do
      if [ -f "$k.m4a" ] && [ ! -f "$k.json" ]; then pending=$((pending+1)); fi
    done
    if [ "$pending" -eq 0 ]; then
      echo "=== 下载已结束且无可转录项，退出（完成 $done_count/106）==="
      break
    fi
  fi
  sleep 30
done

echo "=== b52 全量抽音频+转录结束 ==="
