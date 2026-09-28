#!/usr/bin/env python3
"""Build the public, approved-only portrait indexes. Standard library only."""
import argparse
import hashlib
import json
import re
import struct
import unicodedata
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def normalize(name):
    name = "".join(c for c in unicodedata.normalize("NFKD", name) if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()

def build(root):
    people, aliases, categories = {}, {}, {}
    config = json.loads((root / "config/production.json").read_text())
    pngs = set((root / "people").glob("*/portrait.png"))
    handled = set()
    for meta_path in sorted((root / "people").glob("*/metadata.json")):
        p = json.loads(meta_path.read_text())
        required = {"schema_version", "id", "name", "aliases", "categories", "alt", "status",
                    "style_version", "created_at", "last_generated_at", "last_reviewed_at",
                    "next_review_due", "approved_by", "approval_reference", "sources"}
        missing = required - p.keys()
        if missing:
            raise ValueError(f"{meta_path}: missing {sorted(missing)}")
        pid = p["id"]
        if not isinstance(pid, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", pid) or pid != meta_path.parent.name:
            raise ValueError(f"{meta_path}: invalid permanent ID")
        if pid in people:
            raise ValueError(f"Duplicate ID {pid}")
        if p["schema_version"] != 1 or p["status"] != "approved":
            raise ValueError(f"{pid}: only approved schema-v1 assets may enter people/")
        if not config["style_approved"] or not config["publication_enabled"]:
            raise ValueError("Publication is gated pending owner approval")
        for key in ("name", "alt", "style_version", "approved_by", "approval_reference"):
            if not isinstance(p[key], str) or not p[key].strip():
                raise ValueError(f"{pid}: missing {key}")
        if not isinstance(p["aliases"], list) or not all(isinstance(a, str) and normalize(a) for a in p["aliases"]):
            raise ValueError(f"{pid}: invalid aliases")
        if not isinstance(p["categories"], list) or not p["categories"]:
            raise ValueError(f"{pid}: categories required")
        if not all(isinstance(c, str) and re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", c) for c in p["categories"]):
            raise ValueError(f"{pid}: invalid category")
        if not isinstance(p["sources"], list) or not p["sources"]:
            raise ValueError(f"{pid}: sources required")
        if not all(isinstance(s, dict) and str(s.get("url", "")).startswith("https://") and s.get("reason") for s in p["sources"]):
            raise ValueError(f"{pid}: each source needs https URL and reason")
        dates = {k: date.fromisoformat(p[k]) for k in ("created_at", "last_generated_at", "last_reviewed_at", "next_review_due")}
        if dates["created_at"] > dates["last_generated_at"] or dates["last_generated_at"] > dates["last_reviewed_at"]:
            raise ValueError(f"{pid}: inconsistent dates")
        if dates["last_reviewed_at"] > date.today():
            raise ValueError(f"{pid}: future review date")
        if dates["next_review_due"] != dates["last_generated_at"] + timedelta(days=90):
            raise ValueError(f"{pid}: next_review_due must be 90 days from generation")
        png = meta_path.parent / "portrait.png"
        data = png.read_bytes()
        if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
            raise ValueError(f"{pid}: invalid PNG header")
        width, height, depth, color = struct.unpack(">IIBB", data[16:26])
        if width != height or width < 512 or depth != 8 or color != 6:
            raise ValueError(f"{pid}: require square 8-bit RGBA PNG, at least 512 px")
        handled.add(png)
        # Header check does not prove transparency or likeness; approval certifies visual QA.
        entry = {k: p[k] for k in ("id", "name", "aliases", "categories", "alt", "style_version", "last_generated_at")}
        entry.update(image=f"people/{pid}/portrait.png", metadata=f"people/{pid}/metadata.json",
                     width=width, height=height, sha256=hashlib.sha256(data).hexdigest())
        people[pid] = entry
        for label in [p["name"], *p["aliases"]]:
            key = normalize(label)
            if not key:
                raise ValueError(f"{pid}: add an explicit Latin alias")
            if key in aliases and aliases[key] != pid:
                raise ValueError(f"Ambiguous alias {label!r}; disambiguate explicitly")
            aliases[key] = pid
        for category in sorted(set(p["categories"])):
            categories.setdefault(category, []).append(pid)
    if pngs != handled:
        raise ValueError("Portraits without approved metadata: " + str(sorted(str(p) for p in pngs - handled)))
    return {
        "catalog.json": {"schema_version": 1, "people": people, "aliases": dict(sorted(aliases.items()))},
        "categories.json": {"schema_version": 1, "categories": dict(sorted(categories.items()))}
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate without modifying files")
    args = parser.parse_args()
    outputs = build(ROOT)
    for name, value in outputs.items():
        text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text() != text:
                raise SystemExit(f"{name} is stale; run python3 scripts/build_catalog.py")
        else:
            path.write_text(text)
    print(f"Validated {len(outputs['catalog.json']['people'])} published portraits.")

if __name__ == "__main__":
    main()
