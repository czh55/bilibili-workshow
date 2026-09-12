#!/usr/bin/env python3
"""Propose (and optionally apply) primary/skills/creator/tool/series from taxonomy.json.

Default: write preview only (docs/taxonomy-preview.{json,md}).
Apply:   python3 scripts/propose-taxonomy.py --apply
Dry-run: python3 scripts/propose-taxonomy.py --apply --dry-run
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_PATH = ROOT / "docs" / "taxonomy.json"
INDEX_PATH = ROOT / "docs" / "index.json"
OUT_JSON = ROOT / "docs" / "taxonomy-preview.json"
OUT_MD = ROOT / "docs" / "taxonomy-preview.md"


def slug_of(item: dict) -> str:
    html = (item.get("outputs") or {}).get("html") or ""
    if html.endswith("-图文实录.html"):
        return html[: -len("-图文实录.html")]
    if html:
        return Path(html).stem
    url = item.get("url") or ""
    if url.startswith("personal:"):
        return url[len("personal:") :]
    return ""


def load() -> tuple[dict, list]:
    tax = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    idx = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    return tax, idx


def propose(item: dict, tax: dict) -> dict:
    tags = list(item.get("tags") or [])
    noise = set(tax.get("noise_tags") or [])
    tag_map = tax.get("tag_to_primary") or {}
    priority = tax.get("priority") or []
    pri_rank = {p: i for i, p in enumerate(priority)}
    slug = slug_of(item)

    label_by_id = {p["id"]: p["label"] for p in tax.get("primaries") or []}

    is_personal = item.get("platform") == "personal" or "个人专栏" in tags

    hits: dict[str, list[str]] = defaultdict(list)

    for t in tags:
        if t in noise:
            continue
        pid = tag_map.get(t)
        if pid:
            hits[pid].append(f"tag:{t}")

    for prefix, pid in (tax.get("slug_hints") or {}).items():
        if slug.startswith(prefix) or (prefix in slug if len(prefix) > 3 else False):
            hits[pid].append(f"slug:{prefix}")

    if hits:
        primary = sorted(hits.keys(), key=lambda p: pri_rank.get(p, 999))[0]
        confidence = "high" if len(hits[primary]) >= 2 or primary != "photo" else "medium"
        if len(hits) > 1:
            confidence = "medium"
    else:
        primary = "other"
        confidence = "low"

    if is_personal:
        primary = "other"
        confidence = "skip-personal"

    creators = []
    tools = []
    series = []
    for t in tags:
        if t in (tax.get("creators") or {}):
            creators.append(tax["creators"][t])
        if t in (tax.get("tools") or {}):
            tools.append(tax["tools"][t])
        if t in (tax.get("series") or {}):
            series.append(tax["series"][t])

    skill_set = set(tax.get("skills") or [])
    skills = [t for t in tags if t in skill_set][:4]

    clean_tags = [t for t in tags if t not in noise]

    return {
        "slug": slug,
        "title": item.get("title") or "",
        "date": item.get("date") or "",
        "platform": item.get("platform") or "",
        "old_tags": tags,
        "primary": primary,
        "primary_label": label_by_id.get(primary, primary),
        "confidence": confidence,
        "evidence": hits.get(primary, [])[:6] if primary in hits else [],
        "alt_primaries": [
            {"id": p, "label": label_by_id.get(p, p), "evidence": hits[p][:4]}
            for p in sorted(hits.keys(), key=lambda x: pri_rank.get(x, 999))
            if p != primary
        ],
        "skills": skills,
        "creator": creators[0] if creators else None,
        "tool": tools[0] if tools else None,
        "series": series[0] if series else None,
        "suggested_clean_tags": clean_tags[:12],
        "is_personal": is_personal,
    }


def apply_fields(item: dict, prop: dict, tax: dict) -> None:
    """Mutate index item with taxonomy fields."""
    noise = set(tax.get("noise_tags") or [])
    slug = prop.get("slug") or ""
    if slug:
        item["slug"] = slug

    if prop.get("is_personal"):
        item.pop("primary", None)
        item.pop("skills", None)
        item.pop("creator", None)
        item.pop("tool", None)
        item.pop("series", None)
        # keep 个人专栏 in tags; still strip platform noise
        tags = [t for t in (item.get("tags") or []) if t not in noise or t == "个人专栏"]
        item["tags"] = tags
        return

    item["primary"] = prop["primary"]
    if prop.get("skills"):
        item["skills"] = list(prop["skills"])
    else:
        item.pop("skills", None)

    for key in ("creator", "tool", "series"):
        val = prop.get(key)
        if val:
            item[key] = val
        else:
            item.pop(key, None)

    tags = [t for t in (item.get("tags") or []) if t not in noise]
    item["tags"] = tags


def write_reports(proposals: list[dict], tax: dict, *, applied: bool = False) -> None:
    by_primary = Counter(p["primary"] for p in proposals if not p["is_personal"])
    by_conf = Counter(p["confidence"] for p in proposals if not p["is_personal"])
    label = {p["id"]: p["label"] for p in tax["primaries"]}

    OUT_JSON.write_text(
        json.dumps(
            {
                "taxonomy_version": tax.get("version"),
                "item_count": len(proposals),
                "applied": applied,
                "distribution": {label.get(k, k): v for k, v in by_primary.most_common()},
                "confidence": dict(by_conf),
                "items": proposals,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    header = (
        "# 分类预览（已写入 index.json）"
        if applied
        else "# 分类预览（自动提案，未写入 index）"
    )
    lines = [
        header,
        "",
        f"词表版本：`taxonomy.json` v{tax.get('version')} · 条目 {len(proposals)}",
        "",
        "## 主类分布（不含个人专栏）",
        "",
        "| 主类 | 数量 | 占比 |",
        "|------|------|------|",
    ]
    video_n = sum(by_primary.values()) or 1
    for pid, _ in [(p["id"], p["label"]) for p in tax["primaries"]]:
        n = by_primary.get(pid, 0)
        lines.append(f"| {label[pid]} (`{pid}`) | {n} | {100 * n / video_n:.1f}% |")

    lines += [
        "",
        f"置信度：{dict(by_conf)}",
        "",
        "## 待审：`other` 与 `low` 置信度",
        "",
    ]
    review = [
        p
        for p in proposals
        if not p["is_personal"] and (p["primary"] == "other" or p["confidence"] == "low")
    ]
    lines.append(f"共 {len(review)} 条需要人工看一眼。\n")
    for p in review[:80]:
        tags = ", ".join(p["old_tags"][:8])
        lines.append(
            f"- **{p['title'][:50]}** `{p['slug']}` → `{p['primary_label']}` · tags: {tags}"
        )
    if len(review) > 80:
        lines.append(f"\n… 另有 {len(review) - 80} 条，见 `taxonomy-preview.json`\n")

    lines += ["", "## 多命中冲突样例（medium，有 alt）", ""]
    conflicts = [p for p in proposals if p.get("alt_primaries") and not p["is_personal"]][:40]
    for p in conflicts:
        alts = ", ".join(a["label"] for a in p["alt_primaries"])
        lines.append(
            f"- **{p['title'][:45]}** → **{p['primary_label']}**（备选: {alts}） evidence={p['evidence']}"
        )

    lines += [
        "",
        "## 维护",
        "",
        "1. 审 `other` / 冲突样例，改 `docs/taxonomy.json` 的映射或 priority",
        "2. 重跑：`python3 scripts/propose-taxonomy.py --apply`",
        "3. 首页读 `taxonomy.json` + `item.primary`；二级面用 `creator` / `tool`",
        "",
    ]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="Write fields into index.json")
    parser.add_argument("--dry-run", action="store_true", help="With --apply, do not write index")
    args = parser.parse_args()

    tax, idx = load()
    proposals = [propose(it, tax) for it in idx]
    write_reports(proposals, tax, applied=False)

    video = [p for p in proposals if not p["is_personal"]]
    dist = Counter(p["primary"] for p in video)
    label = {p["id"]: p["label"] for p in tax["primaries"]}
    print(f"Wrote {OUT_MD.relative_to(ROOT)} and {OUT_JSON.relative_to(ROOT)}")
    print(f"Video items: {len(video)}  primary_sum={sum(dist.values())}")
    for pid in tax["priority"]:
        print(f"  {label[pid]:8s} {dist.get(pid, 0):4d}")
    other_n = dist.get("other", 0)
    print(f"其他占比: {100 * other_n / max(len(video), 1):.1f}%")

    if not args.apply:
        return

    changed = 0
    for item, prop in zip(idx, proposals):
        before = json.dumps(
            {k: item.get(k) for k in ("slug", "primary", "skills", "creator", "tool", "series", "tags")},
            ensure_ascii=False,
            sort_keys=True,
        )
        apply_fields(item, prop, tax)
        after = json.dumps(
            {k: item.get(k) for k in ("slug", "primary", "skills", "creator", "tool", "series", "tags")},
            ensure_ascii=False,
            sort_keys=True,
        )
        if before != after:
            changed += 1

    print(f"{'Would update' if args.dry_run else 'Updated'} {changed} / {len(idx)} items")
    if args.dry_run:
        return

    INDEX_PATH.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_reports(proposals, tax, applied=True)
    print(f"Wrote {INDEX_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
