#!/bin/bash
# b51 自动流水线：轮询检测新下载的 e*.source.mp4 -> 抽音频兜底 -> Whisper 转录
# 与 b51-download.sh 并行运行，下载完成一个即处理一个。
cd /Users/chenzhiheng/Projects/bilibili-workshop

KEYS=(e01 e02 e03 e04 e05 e06 e07 e08 e09 e10 e11 e12 e13 e14 e15 e16 e17 e18 e19 e20 e21 e22 e23)

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
      elif [ -f "$k.source.mp4" ] && [ "$k.json" -ot "$k.source.mp4" ]; then
        echo "=== $k 转录早于视频，重转 ==="
        rm -f "$k.json" "$k.txt" "$k.srt" "$k.vtt" "$k.tsv"
        need=1
      fi
    fi
    if [ "$need" -eq 1 ]; then
      dur=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$k.m4a" 2>/dev/null | cut -d. -f1)
      echo "=== 转录 $k (${dur}s) ==="
      python3 -m whisper "$k.m4a" --model medium --language Chinese --output_dir . 2>&1 | tail -3
      [ -f "$k.json" ] && echo "=== $k 转录完成 ===" || echo "=== $k 转录可能失败 ==="
    fi
  done

  done_count=0
  for k in "${KEYS[@]}"; do
    [ -f "$k.json" ] && done_count=$((done_count + 1))
  done
  dl_count=$(ls e*.source.* 2>/dev/null | wc -l | tr -d ' ')
  echo "=== 进度: 转录 $done_count/23，已下载 $dl_count/23 ==="

  if [ "$done_count" -ge 23 ]; then
    break
  fi
  # 若下载已全部结束且没有更多可转的，仍等一会儿再退出检查
  sleep 30
done

echo "=== b51 全量抽音频+转录结束 ==="
