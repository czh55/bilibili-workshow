#!/usr/bin/env python3
"""b46：Whisper medium 转录单个音频到 {key}.json（MPS 加速）。"""
from __future__ import annotations

import json
import sys

import whisper

key = sys.argv[1]
audio = f"{key}.m4a"
model = whisper.load_model("medium", device="mps")
result = model.transcribe(audio, language="Chinese")
with open(f"{key}.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=1)
segs = len(result.get("segments", []))
print(f"{key}: {segs} segments")
