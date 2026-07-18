#!/usr/bin/env python3
"""ASHGATE content build CLI (doc 15 s3).

Reads source-of-truth tables in content/, validates them against the
conventions in docs/design/15-data-schemas-naming.md, computes derived
stats, and emits runtime config JSON into data/.

Usage:  python3 tools/build_content.py
Exit codes: 0 = built, 1 = validation failure (CI-blocking).
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
DATA = ROOT / "data"

UNIT_ID_RE = re.compile(r"^ASH-(TNK|ASN|RNG|MAG|NEC|HLR|BSK)-(C|R|E|L)(\d{2})$")
CLASSES = ["TNK", "ASN", "RNG", "MAG", "NEC", "HLR", "BSK"]
RARITY_QUOTA = {"C": 2, "R": 3, "E": 3, "L": 2}  # per class, launch roster
FACTIONS = {"Emberguard", "Hollowed", "Choir", "Freeblades", "Gravebound"}
DAMAGE_ROOTS = {"physical", "magical"}
SUBTAGS = {"bleed", "pierce", "arcane", "shadow", "holy", "decay"}
ROWS = {"front", "back"}
GROWTH_BY_RARITY = {"C": "common_std", "R": "rare_std", "E": "epic_std", "L": "legendary_std"}

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def load_units() -> list[dict]:
    with open(CONTENT / "units.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    seen = set()
    for r in rows:
        uid = r["id"]
        if not UNIT_ID_RE.match(uid):
            err(f"{uid}: bad unit id format")
        if uid in seen:
            err(f"{uid}: duplicate id")
        seen.add(uid)
        m = UNIT_ID_RE.match(uid)
        if m:
            if m.group(1) != r["class"]:
                err(f"{uid}: id class tag != class column {r['class']}")
            if m.group(2) != r["rarity"]:
                err(f"{uid}: id rarity tag != rarity column {r['rarity']}")
        if r["faction"] not in FACTIONS:
            err(f"{uid}: unknown faction {r['faction']}")
        if r["damageRoot"] not in DAMAGE_ROOTS:
            err(f"{uid}: unknown damageRoot {r['damageRoot']}")
        if r["row"] not in ROWS:
            err(f"{uid}: unknown row {r['row']}")
        for tag in filter(None, r["subtags"].split("|")):
            if tag not in SUBTAGS:
                err(f"{uid}: unknown subtag {tag}")
    return rows


def check_roster_shape(rows: list[dict]) -> None:
    for cls in CLASSES:
        for rarity, quota in RARITY_QUOTA.items():
            n = sum(1 for r in rows if r["class"] == cls and r["rarity"] == rarity)
            if n != quota:
                err(f"roster shape: {cls}/{rarity} has {n} units, expected {quota}")


def compute_stats(row: dict, tpl: dict) -> dict:
    base = tpl["classTemplates"][row["class"]]
    mult = tpl["rarityMultipliers"][row["rarity"]]
    bias = tpl["biases"][row["bias"]]
    return {
        "hp": round(base["hp"] * mult["stat"] * bias["hp"]),
        "atk": round(base["atk"] * mult["stat"] * bias["atk"]),
        "def": round(base["def"] * mult["stat"] * bias["def"]),
        "spd": base["spd"] + mult["spdBonus"] + bias["spdBonus"],
    }


def check_skills(unit_ids: set[str]) -> None:
    skills_path = DATA / "skills.mvp.json"
    statuses_path = DATA / "statuses.json"
    if not skills_path.exists() or not statuses_path.exists():
        return
    skills = json.loads(skills_path.read_text())["skills"]
    status_ids = {s["id"] for s in json.loads(statuses_path.read_text())["statuses"]}
    kits: dict[str, set[str]] = {}
    for sid, sk in skills.items():
        if sk["unit"] not in unit_ids:
            err(f"{sid}: references unknown unit {sk['unit']}")
        kits.setdefault(sk["unit"], set()).add(sk["slot"])
        for eff in sk.get("effects", []):
            st = eff.get("status")
            if st and st not in status_ids:
                err(f"{sid}: references unknown status {st}")
    for uid, slots in kits.items():
        if slots != {"S1", "S2", "S3", "S4"}:
            err(f"{uid}: incomplete kit, has {sorted(slots)}")


def main() -> int:
    tpl = json.loads((CONTENT / "class_stat_templates.json").read_text())
    rows = load_units()
    check_roster_shape(rows)
    check_skills({r["id"] for r in rows})

    if errors:
        print(f"VALIDATION FAILED ({len(errors)} errors):")
        for e in errors:
            print(f"  - {e}")
        return 1

    units = []
    for r in rows:
        units.append({
            "id": r["id"],
            "class": r["class"],
            "rarity": r["rarity"],
            "faction": r["faction"],
            "row": r["row"],
            "damageRoot": r["damageRoot"],
            "subtags": [t for t in r["subtags"].split("|") if t],
            "baseStats": compute_stats(r, tpl),
            "growthCurve": GROWTH_BY_RARITY[r["rarity"]],
            "startStars": tpl["rarityStartStars"][r["rarity"]],
            "starCap": tpl["rarityStarCap"][r["rarity"]],
            "skills": [f"SKL-{r['id']}-S{i}" for i in range(1, 5)],
            "artRef": r["id"],
            "status": "live",
        })

    DATA.mkdir(exist_ok=True)
    out = DATA / "units.json"
    out.write_text(json.dumps({"schema": "units_v1", "units": units}, indent=2) + "\n")
    print(f"OK: {len(units)} units -> {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
