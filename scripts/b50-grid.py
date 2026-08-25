#!/usr/bin/env python3
"""b50 预览帧拼网格：把每篇的预览帧拼成 4 列网格图供审阅（PIL 实现）。"""
from __future__ import annotations

from PIL import Image
from pathlib import Path

PREV = Path("/Users/chenzhiheng/Projects/bilibili-workshop/_work/b50-preview")

keys = [f"d{i:02d}" for i in range(1, 15)]
for k in keys:
    files = sorted(PREV.glob(f"{k}_[0-9]*.jpg"), key=lambda p: int(p.stem.split("_")[1]))
    if not files:
        continue
    cols = 4
    thumbs = [Image.open(f).convert("RGB") for f in files]
    cell_w = max(im.width for im in thumbs)
    cell_h = max(im.height for im in thumbs)
    rows = (len(thumbs) + cols - 1) // cols
    grid = Image.new("RGB", (cols * cell_w, rows * cell_h), (255, 255, 255))
    for i, im in enumerate(thumbs):
        r, c = divmod(i, cols)
        grid.paste(im, (c * cell_w, r * cell_h))
    out = PREV / f"{k}_grid.jpg"
    grid.save(out, quality=82)
    print(f"{k}: {len(files)} 帧 -> {out.name}")
print("完成")
