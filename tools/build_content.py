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
    statuses_path = DATA / "statuses.json"
    skill_files = sorted(DATA.glob("skills*.json"))
    if not skill_files or not statuses_path.exists():
        return
    status_ids = {s["id"] for s in json.loads(statuses_path.read_text())["statuses"]}
    skills: dict[str, dict] = {}
    for path in skill_files:
        for sid, sk in json.loads(path.read_text())["skills"].items():
            if sid in skills:
                err(f"{sid}: defined in multiple skill files")
            skills[sid] = sk
    kits: dict[str, set[str]] = {}
    for sid, sk in skills.items():
        if sk["unit"] not in unit_ids:
            err(f"{sid}: references unknown unit {sk['unit']}")
        kits.setdefault(sk["unit"], set()).add(sk["slot"])
        for eff in sk.get("effects", []):
            st = eff.get("status")
            if st and st not in status_ids:
                err(f"{sid}: references unknown status {st}")
    for uid in sorted(unit_ids):
        slots = kits.get(uid, set())
        if slots != {"S1", "S2", "S3", "S4"}:
            err(f"{uid}: incomplete kit, has {sorted(slots)}")
    print(f"skills: {len(skills)} across {len(skill_files)} files, {len(kits)} complete kits")


ENEMY_ID_RE = re.compile(r"^ENM-(SLM|GNT|GRD|UND)-(M|E|B|X)(\d{2})$")
STAGE_ID_RE = re.compile(r"^STG-CAMP-[1-4]-(0[1-9]|10)$")


def check_enemies_and_stages() -> None:
    enemy_ids: set[str] = set()
    for path in sorted(DATA.glob("enemies.ch*.json")):
        for e in json.loads(path.read_text())["enemies"]:
            eid = e["id"]
            m = ENEMY_ID_RE.match(eid)
            if not m:
                err(f"{eid}: bad enemy id format")
            elif m.group(1) != e["family"] or m.group(2) != e["tier"]:
                err(f"{eid}: id tags != family/tier columns")
            if eid in enemy_ids:
                err(f"{eid}: duplicate enemy id")
            enemy_ids.add(eid)
            for t in e.get("telegraphs", []):
                if not 1 <= t["windup"] <= 3:
                    err(f"{eid}: telegraph windup {t['windup']} outside 1-3")
    for path in sorted(DATA.glob("stages.ch*.json")):
        for s in json.loads(path.read_text())["stages"]:
            sid = s["id"]
            if not STAGE_ID_RE.match(sid):
                err(f"{sid}: bad stage id format")
            if not 1 <= len(s["waves"]) <= 3:
                err(f"{sid}: {len(s['waves'])} waves outside 1-3")
            for wave in s["waves"]:
                for eid in wave:
                    if eid not in enemy_ids:
                        err(f"{sid}: references unknown enemy {eid}")


GEAR_ID_RE = re.compile(r"^GEAR-(WPN|ARM|HLM|CHM|SGL)-([A-Z]+)-(T[1-4])$")


def load_reward_ids() -> tuple[set[str], set[str]]:
    """Returns (valid reward item ids incl. gear combos + virtual ids, drop table ids)."""
    valid: set[str] = set()
    gear_sets: set[str] = set()
    items_path = DATA / "items.json"
    gear_path = DATA / "gear.json"
    drops_path = DATA / "droptables.json"
    if items_path.exists():
        valid |= {i["id"] for i in json.loads(items_path.read_text())["items"]}
    if gear_path.exists():
        g = json.loads(gear_path.read_text())
        gear_sets = set(g["sets"])
        for slot in g["slots"]:
            for gset in gear_sets:
                for tier in g["tiers"]:
                    valid.add(f"GEAR-{slot}-{gset}-{tier}")
    tables: set[str] = set()
    if drops_path.exists():
        d = json.loads(drops_path.read_text())
        tables = set(d["tables"])
        valid |= set(d.get("virtualItems", {})) - {"_comment"}
        for tid, t in d["tables"].items():
            for entry in t.get("guaranteed", []) + t.get("chance", []):
                if entry["item"] not in valid:
                    err(f"{tid}: unknown item {entry['item']}")
    return valid, tables


def check_rewards_and_banners(unit_ids: set[str]) -> None:
    valid_items, drop_tables = load_reward_ids()
    if not valid_items:
        return
    for path in sorted(DATA.glob("stages.ch*.json")):
        doc = json.loads(path.read_text())
        chest_rewards = [r for rl in doc["chapter"].get("starChests", {}).values() for r in rl]
        for r in chest_rewards:
            if r["item"] not in valid_items:
                err(f"{doc['chapter']['id']} starChests: unknown item {r['item']}")
        for s in doc["stages"]:
            for r in s.get("firstClear", []):
                if r["item"] not in valid_items:
                    err(f"{s['id']}: unknown firstClear item {r['item']}")
            if drop_tables and s.get("repeatDrops") not in drop_tables:
                err(f"{s['id']}: unknown drop table {s.get('repeatDrops')}")
    banners_path = DATA / "banners.json"
    if banners_path.exists():
        b = json.loads(banners_path.read_text())
        for bn in b["banners"]:
            rates = bn.get("rates", {})
            if rates and abs(sum(rates.values()) - 1.0) > 1e-9:
                err(f"{bn['bannerId']}: rates sum to {sum(rates.values())}, not 1.0")
            featured = bn.get("featured", {})
            named = list(bn.get("selectableLegendaries", []))
            for group in featured.values():
                named += group
            for uid in named:
                if uid not in unit_ids:
                    err(f"{bn['bannerId']}: unknown unit {uid}")
        for uid in b.get("tutorialSummon", {}).get("curatedTrio", []):
            if uid not in unit_ids:
                err(f"tutorialSummon: unknown unit {uid}")


def check_liveops(valid_items: set[str]) -> None:
    """Every reward/cost item ref in shops/events/battlepass must resolve.
    Cosmetic ids (COS-*) and event-scoped currencies (EVC-*) are free-form
    (catalogued elsewhere); everything else must be a real item."""
    def ok(item_id: str) -> bool:
        return (item_id in valid_items or item_id.startswith("COS-")
                or item_id.startswith("EVC-"))

    def check_reward_list(rewards: list, where: str) -> None:
        for r in rewards:
            iid = r.get("item") or r.get("cosmeticId")
            if iid and not ok(iid):
                err(f"{where}: unknown reward {iid}")

    def check_cost(cost: dict, where: str) -> None:
        for cid in cost:
            if not ok(cid):
                err(f"{where}: unknown cost currency {cid}")

    shops = DATA / "shops.json"
    if shops.exists():
        for shop in json.loads(shops.read_text())["shops"]:
            for e in shop.get("entries", []):
                for key in ("grantNow", "grantDaily"):
                    check_reward_list(e.get(key, []), f"{shop['id']}")
                if "item" in e and not ok(e["item"]):
                    err(f"{shop['id']}: unknown item {e['item']}")
                if "cost" in e:
                    check_cost(e["cost"], shop["id"])
    events = DATA / "events.json"
    if events.exists():
        ev = json.loads(events.read_text())
        for e in ev["events"]:
            for entry in e.get("shop", []):
                if "item" in entry and not ok(entry["item"]):
                    err(f"{e['id']} shop: unknown item {entry['item']}")
                check_cost(entry.get("cost", {}), f"{e['id']} shop")
            for m in e.get("milestones", []):
                check_reward_list(m.get("reward", []), f"{e['id']} milestone")
            check_reward_list(e.get("firstClearTotal", []), e["id"])
        for day, rl in ev.get("loginTrack", {}).get("notableDays", {}).items():
            check_reward_list(rl, f"loginTrack day {day}")
    bp = DATA / "battlepass.json"
    if bp.exists():
        b = json.loads(bp.read_text())
        for track in b.get("perLevelPattern", {}).values():
            if isinstance(track, list):
                check_reward_list(track, "battlepass pattern")
        for m in b.get("milestones", []):
            check_reward_list(m.get("free", []), f"BP L{m['level']} free")
            check_reward_list(m.get("paid", []), f"BP L{m['level']} paid")


def main() -> int:
    tpl = json.loads((CONTENT / "class_stat_templates.json").read_text())
    rows = load_units()
    unit_ids = {r["id"] for r in rows}
    check_roster_shape(rows)
    check_skills(unit_ids)
    check_enemies_and_stages()
    check_rewards_and_banners(unit_ids)
    valid_items, _ = load_reward_ids()
    check_liveops(valid_items)

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
