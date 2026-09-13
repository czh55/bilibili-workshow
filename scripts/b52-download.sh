#!/bin/bash
# b52 下载：5 个 B 站 + 101 个小红书（串行；xhs-fetch 内置 60s 限流）
# 键位 h01–h106，映射见 scripts/b52-slug-map.json
cd /Users/chenzhiheng/Projects/video-notes
PY=/opt/homebrew/Cellar/yt-dlp/2026.7.4/libexec/bin/python
[ -x "$PY" ] || PY=python3
YTDLP=$(command -v yt-dlp)
FFMPEG=$(command -v ffmpeg)
[ -z "$FFMPEG" ] && FFMPEG=/opt/homebrew/bin/ffmpeg

download_bili() {
  local k="$1" u="$2"
  if [ -f "$k.source.mp4" ] && [ -s "$k.source.mp4" ] && [ -f "$k.m4a" ] && [ -s "$k.m4a" ]; then
    echo "=== $k 已存在，跳过 ==="
    return 0
  fi
  echo "=== 开始 B站 $k $u ==="
  "$YTDLP" -f "bestaudio[ext=m4a]/bestaudio/best" -o "${k}.%(ext)s" "$u" || true
  # 统一音频名为 .m4a（yt-dlp 可能产出 webm/opus）
  if [ ! -f "$k.m4a" ]; then
    aud=$(ls "$k".m4a "$k".webm "$k".opus "$k".mp3 2>/dev/null | head -1)
    if [ -n "$aud" ] && [ "$aud" != "$k.m4a" ]; then
      "$FFMPEG" -y -i "$aud" -vn -acodec aac -b:a 128k "$k.m4a" 2>/dev/null
    fi
  fi
  "$YTDLP" -f "bestvideo[height<=1080][ext=mp4]/bestvideo[height<=1080]/best[height<=1080]" \
    -o "${k}.source.%(ext)s" "$u" || true
  # 若只有混合文件，抽出音频
  src=$(ls "$k".source.* 2>/dev/null | head -1)
  if [ -n "$src" ] && [ ! -f "$k.m4a" ]; then
    "$FFMPEG" -y -i "$src" -vn -acodec aac -b:a 128k "$k.m4a" 2>/dev/null
  fi
  # 写简易 meta
  if [ ! -f "$k.meta.json" ]; then
    title=$("$YTDLP" --print title "$u" 2>/dev/null | head -1)
    dur=$("$YTDLP" --print duration_string "$u" 2>/dev/null | head -1)
    id=$("$YTDLP" --print id "$u" 2>/dev/null | head -1)
    python3 -c "import json; json.dump({'id':'''$id''','title':'''$title''','duration':'''$dur''','url':'''$u''','platform':'bilibili'}, open('$k.meta.json','w'), ensure_ascii=False, indent=2)"
  fi
  if [ -f "$k.source.mp4" ] || [ -n "$(ls "$k".source.* 2>/dev/null)" ]; then
    echo "=== $k 完成 ==="
  else
    echo "=== $k 失败 ==="
    return 1
  fi
}

# ---- B 站 h01-h05 ----
BILI_KEYS=(h01 h02 h03 h04 h05)
BILI_URLS=(
  "https://b23.tv/VEZrk9Y"
  "https://b23.tv/enZwYDx"
  "https://b23.tv/5wyboFM"
  "https://b23.tv/gQP3Joc"
  "https://b23.tv/6fG6mEk"
)
for i in "${!BILI_KEYS[@]}"; do
  download_bili "${BILI_KEYS[$i]}" "${BILI_URLS[$i]}"
done

# ---- 小红书 h06-h106 ----
XHS_KEYS=()
for n in $(seq 6 106); do
  XHS_KEYS+=("$(printf 'h%02d' "$n")")
done
# h100-h106 上面 printf h%02d 会得到 h100 等，正确

XHS_URLS=(
  "https://xhslink.cn/o/AqJsgbsKZF3"
  "https://xhslink.cn/o/hqSO1wCEJ0"
  "https://xhslink.cn/o/hljaSZQ43a"
  "https://xhslink.cn/o/61uQRyCowGt"
  "https://xhslink.cn/o/9zr2F4rMlGS"
  "https://xhslink.cn/o/7dLtKfUjCZO"
  "https://xhslink.cn/o/5Zd4jiMczqY"
  "https://xhslink.cn/o/AWaIGS56YSn"
  "https://xhslink.cn/o/65oym3n8EgF"
  "https://xhslink.cn/o/AHpHYIropek"
  "https://xhslink.cn/o/7HVsME0Rlpb"
  "https://xhslink.cn/o/4JsvDEt90vA"
  "https://xhslink.cn/o/5nNhQhLWnpX"
  "https://xhslink.cn/o/8csW9QaOtbp"
  "https://xhslink.cn/o/8uYR5RVJK2l"
  "https://xhslink.cn/o/8c3KG8p4jjJ"
  "https://xhslink.cn/o/30ITGmNrFn3"
  "https://xhslink.cn/o/A3RxRyA6IjC"
  "https://xhslink.cn/o/48MgxMuTpwX"
  "https://xhslink.cn/o/1ROZGJJbQRs"
  "https://xhslink.cn/o/ALLx7vyfQfk"
  "https://xhslink.cn/o/AQFtyuHqkGe"
  "https://xhslink.cn/o/13dKO2oYdxj"
  "https://xhslink.cn/o/5Lh3s6BqrXc"
  "https://xhslink.cn/o/7pPRsq2VHuq"
  "https://xhslink.cn/o/Qvr6gBYwca"
  "https://xhslink.cn/o/6MEgD4a4TIJ"
  "https://xhslink.cn/o/4son0WFRX48"
  "https://xhslink.cn/o/2TXPgE0LcDp"
  "https://xhslink.cn/o/3YWYtqeUu19"
  "https://xhslink.cn/o/HB5WFAJ2Jy"
  "https://xhslink.cn/o/8oQ7K9rV6ia"
  "https://xhslink.cn/o/2tcjYfTm6fd"
  "https://xhslink.cn/o/7eBRuxcuez8"
  "https://xhslink.cn/o/77Jdx6aBsXG"
  "https://xhslink.cn/o/A3pK2S3Ac23"
  "https://xhslink.cn/o/7613ZcM42kn"
  "https://xhslink.cn/o/4dQz9iqeCkS"
  "https://xhslink.cn/o/6vyu6a34w7c"
  "https://xhslink.cn/o/6f5yUcgphc0"
  "https://xhslink.cn/o/4YybIfEQh1S"
  "https://xhslink.cn/o/8FUFu38tCE9"
  "https://xhslink.cn/o/41woLRwfJ82"
  "https://xhslink.cn/o/9w8dfSL0YWQ"
  "https://xhslink.cn/o/dpW99sp1VZ"
  "https://xhslink.cn/o/9jmcCvFNYCb"
  "https://xhslink.cn/o/8IjJAeYsZ5T"
  "https://xhslink.cn/o/3eFlkPnS4J0"
  "https://xhslink.cn/o/333BTienUji"
  "https://xhslink.cn/o/65WO3Yqakhi"
  "https://xhslink.cn/o/U53jBqAiKi"
  "https://xhslink.cn/o/12mmh7SZWEs"
  "https://xhslink.cn/o/1U9u21oww6k"
  "https://xhslink.cn/o/Aob8TBzIdu5"
  "https://xhslink.cn/o/88qKJVoiHzj"
  "https://xhslink.cn/o/3LR0ZgekPCQ"
  "https://xhslink.cn/o/5cAp3II4tOh"
  "https://xhslink.cn/o/6YjFqgvsnav"
  "https://xhslink.cn/o/4edNXZ0iaNQ"
  "https://xhslink.cn/o/9e8eK19E0U5"
  "https://xhslink.cn/o/1ygbwRYWvk9"
  "https://xhslink.cn/o/4DQENKiGr0m"
  "https://xhslink.cn/o/6P6D9uk6LYO"
  "https://xhslink.cn/o/6eEfTaNhtbW"
  "https://xhslink.cn/o/AnjQQlcieHR"
  "https://xhslink.cn/o/AlYyIs2RRDj"
  "https://xhslink.cn/o/AbROAU1m4fs"
  "https://xhslink.cn/o/9eDOAkIeOlI"
  "https://xhslink.cn/o/1AsZHWZgqpD"
  "https://xhslink.cn/o/AD1u7aAV7Dy"
  "https://xhslink.cn/o/7flDH69qTo6"
  "https://xhslink.cn/o/5yzlaoBPYp8"
  "https://xhslink.cn/o/AeZoUTHkFo2"
  "https://xhslink.cn/o/4BF208NMwYK"
  "https://xhslink.cn/o/9bwFcYuimYs"
  "https://xhslink.cn/o/5nIypIawAHz"
  "https://xhslink.cn/o/7LMeVHTPiJA"
  "https://xhslink.cn/o/89PUq7nOTkb"
  "https://xhslink.cn/o/7VFN9CUYTRo"
  "https://xhslink.cn/o/4xoStZEGGMX"
  "https://xhslink.cn/o/AxmOqFMVuNl"
  "https://xhslink.cn/o/2gkjBWrDYQh"
  "https://xhslink.cn/o/LRZC2Bj2m7"
  "https://xhslink.cn/o/1oddahTXBCO"
  "https://xhslink.cn/o/7CXGr8IaJs5"
  "https://xhslink.cn/o/2D3TQrKrmnw"
  "https://xhslink.cn/o/8UTvxLcId6o"
  "https://xhslink.cn/o/64xG3NDAP57"
  "https://xhslink.cn/o/7Gf7zU6nNxH"
  "https://xhslink.cn/o/A7myJaO8C9u"
  "https://xhslink.cn/o/3FADbvd6nTY"
  "https://xhslink.cn/o/7XPflshIdp6"
  "https://xhslink.cn/o/1vvpCdl1cW9"
  "https://xhslink.cn/o/4W69PpIpBVo"
  "https://xhslink.cn/o/3WtA0rhTwXU"
  "https://xhslink.cn/o/3agCqgRTEwa"
  "https://xhslink.cn/o/42xPX9ws0Iw"
  "https://xhslink.cn/o/63yp3VpeMUe"
  "https://xhslink.cn/o/9Fu7q0ymYPC"
  "https://xhslink.cn/o/1FynErXo88P"
  "https://xhslink.cn/o/NWMxdjXcoz"
)

# 校验数量
if [ "${#XHS_KEYS[@]}" -ne "${#XHS_URLS[@]}" ]; then
  echo "ERROR: XHS keys ${#XHS_KEYS[@]} != urls ${#XHS_URLS[@]}"
  exit 1
fi

for i in "${!XHS_KEYS[@]}"; do
  k="${XHS_KEYS[$i]}"; u="${XHS_URLS[$i]}"
  if [ -f "$k.source.mp4" ] && [ -s "$k.source.mp4" ] && [ -f "$k.meta.json" ]; then
    echo "=== $k 已存在，跳过 ==="
    continue
  fi
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
