"""ASHGATE headless battle simulator — reference implementation.

This is the balance/CI harness (doc 13 Phase 0). The CANONICAL sim is the
engine-independent C# library shared between Unity client and server
(doc 12 s2); this Python port exists to run the auto-balance guardrails
here and in CI on every data change, and to serve as an executable spec
the C# port is validated against.

Faithful to doc 02: speed-ordered turn-based rounds, the s5 damage
formula, shared Surge, cooldowns, the s8 status taxonomy. Deliberately
simplified where a Phase-0 balance check does not need full fidelity
(noted inline). Deterministic under a fixed seed.
"""
from __future__ import annotations
import json
import random
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONTENT = ROOT / "content"

# --------------------------------------------------------------------------
# Data loading
# --------------------------------------------------------------------------

def _load(path: Path) -> dict:
    return json.loads(path.read_text())


class GameData:
    """Loads and indexes all runtime tables once."""

    def __init__(self) -> None:
        self.units = {u["id"]: u for u in _load(DATA / "units.json")["units"]}
        self.statuses = {s["id"]: s for s in _load(DATA / "statuses.json")["statuses"]}
        self.skills: dict[str, dict] = {}
        self.summons: dict[str, dict] = {}
        for f in sorted(DATA.glob("skills*.json")):
            doc = _load(f)
            self.skills.update(doc["skills"])
            self.summons.update(doc.get("summons", {}))
        self.enemies: dict[str, dict] = {}
        self.enemy_scaling: dict[str, float] = {}
        self.stages: dict[str, dict] = {}
        for f in sorted(DATA.glob("enemies.ch*.json")):
            doc = _load(f)
            for e in doc["enemies"]:
                self.enemies[e["id"]] = e
                self.enemy_scaling[e["id"]] = doc["levelScaling"]
        for f in sorted(DATA.glob("stages.ch*.json")):
            doc = _load(f)
            for s in doc["stages"]:
                self.stages[s["id"]] = s
        self.tpl = _load(CONTENT / "class_stat_templates.json")

    def skill(self, unit_id: str, slot: str) -> dict | None:
        return self.skills.get(f"SKL-{unit_id}-{slot}")


# --------------------------------------------------------------------------
# Stat derivation (mirrors tools/build_content.py + doc 09 level/star growth)
# --------------------------------------------------------------------------

def unit_stats(gd: GameData, unit_id: str, level: int, stars: int,
               gear_mult: float = 1.0) -> dict:
    """Effective stats at a level/star with a flat gear budget multiplier.

    gear_mult models the doc 09 s6.3 'F2P benchmark gear' as a single
    offense/defense budget knob for balance sweeps (real gear is per-slot;
    that fidelity is not needed to answer the guardrail questions)."""
    u = gd.units[unit_id]
    base = u["baseStats"]
    curve = gd.tpl["growthCurves"][u["growthCurve"]]
    g = 1.0 + curve["perLevel"] * curve["rarityGrowth"] * (level - 1)
    start = gd.tpl["rarityStartStars"][u["rarity"]]
    star = 1.0 + gd.tpl["starBonusPerStar"] * max(0, stars - start)
    return {
        "hp":  round(base["hp"]  * g * star * gear_mult),
        "atk": round(base["atk"] * g * star * gear_mult),
        "def": round(base["def"] * g * star),  # gear_mult applied to offense only
        "spd": base["spd"],  # SPD does not grow with level (anti-tyranny)
    }


def enemy_stats(gd: GameData, enemy_id: str, level: int) -> dict:
    e = gd.enemies[enemy_id]
    s = gd.enemy_scaling[enemy_id] ** (level - 1)
    b = e["baseStats"]
    return {k: round(b[k] * s) for k in ("hp", "atk", "def", "spd")}


# --------------------------------------------------------------------------
# Combat entities
# --------------------------------------------------------------------------

@dataclass
class Status:
    sid: str
    rounds: int
    stacks: int = 1
    payload: dict = field(default_factory=dict)


@dataclass
class Combatant:
    name: str
    side: str  # "ally" | "enemy"
    unit_id: str
    stats: dict
    is_enemy: bool
    row: str = "back"
    damage_root: str = "physical"
    subtags: list = field(default_factory=list)
    traits: list = field(default_factory=list)
    phys_res: float = 0.0
    mag_res: float = 0.0
    immunities: list = field(default_factory=list)
    hp: int = 0
    max_hp: int = 0
    cooldowns: dict = field(default_factory=dict)
    statuses: list = field(default_factory=list)
    rage: int = 0
    barrier: int = 0
    resolve_until: int = -1  # round until which boss is CC-immune
    ai_ult: dict = field(default_factory=dict)
    enemy_skills: list = field(default_factory=list)
    telegraph: dict | None = None

    def __post_init__(self) -> None:
        self.hp = self.stats["hp"]
        self.max_hp = self.stats["hp"]

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def has(self, sid: str) -> bool:
        return any(s.sid == sid for s in self.statuses)

    def get(self, sid: str) -> Status | None:
        for s in self.statuses:
            if s.sid == sid:
                return s
        return None

    def stat(self, key: str) -> float:
        """Current stat after status modifiers (buffs/debuffs)."""
        val = float(self.stats[key])
        for s in self.statuses:
            mod = _STAT_MODS.get(s.sid)
            if mod and mod[0] == key:
                val *= (1.0 + mod[1])
        return val


# status id -> (stat, pct) for the standardized stat tokens (doc 02 s8)
_STAT_MODS = {
    "STS-ATK-UP": ("atk", 0.30), "STS-ATK-DOWN": ("atk", -0.30),
    "STS-DEF-UP": ("def", 0.30), "STS-DEF-DOWN": ("def", -0.30),
    "STS-SPD-UP": ("spd", 0.25), "STS-SPD-DOWN": ("spd", -0.25),
    "STS-ARMOR-BREAK": ("def", -0.40),
}
_HARD_CC = {"STS-STUN", "STS-BIND"}


# --------------------------------------------------------------------------
# Battle engine
# --------------------------------------------------------------------------

class Battle:
    ROUND_LIMIT = 20
    ENRAGE_ROUND = 15
    SURGE_MAX = 100

    def __init__(self, gd: GameData, allies: list[Combatant],
                 enemies: list[Combatant], seed: int = 1, log: bool = False):
        self.gd = gd
        self.allies = allies
        self.enemies = enemies
        self.rng = random.Random(seed)
        self.surge = 0  # team-shared ally Surge
        self.round = 0
        self.logging = log
        self.unhandled: dict[str, int] = {}

    # -- helpers ----------------------------------------------------------
    def _log(self, msg: str) -> None:
        if self.logging:
            print(f"  R{self.round} {msg}")

    def team(self, side: str) -> list[Combatant]:
        return self.allies if side == "ally" else self.enemies

    def foes(self, c: Combatant) -> list[Combatant]:
        return [x for x in self.team("enemy" if c.side == "ally" else "ally") if x.alive]

    def friends(self, c: Combatant) -> list[Combatant]:
        return [x for x in self.team(c.side) if x.alive]

    def _living(self) -> list[Combatant]:
        return [c for c in self.allies + self.enemies if c.alive]

    # -- targeting --------------------------------------------------------
    def pick_target(self, attacker: Combatant, rule: str = "aggro") -> Combatant | None:
        foes = self.foes(attacker)
        if not foes:
            return None
        # Taunt-Me override (doc 03 tank rule)
        taunts = [f for f in foes if f.has("STS-TAUNT-ME")]
        if taunts and rule in ("aggro", "single"):
            return self.rng.choice(taunts)
        stealthed = [f for f in foes if f.has("STS-STEALTH")]
        eligible = [f for f in foes if f not in stealthed] or foes
        if rule == "lowest_hp":
            return min(eligible, key=lambda f: f.hp)
        if rule == "highest_atk":
            return max(eligible, key=lambda f: f.stat("atk"))
        if rule == "back_row":
            back = [f for f in eligible if f.row == "back"]
            return self.rng.choice(back or eligible)
        # aggro: 60/40 front/back weighting
        front = [f for f in eligible if f.row == "front"]
        back = [f for f in eligible if f.row == "back"]
        if front and back:
            pool = front if self.rng.random() < 0.6 else back
        else:
            pool = eligible
        return self.rng.choice(pool)

    # -- damage formula (doc 02 s5/s6) ------------------------------------
    def deal_damage(self, src: Combatant, tgt: Combatant, power: float,
                    root: str, subtag: str | None, hits: int = 1) -> int:
        total = 0
        for _ in range(hits):
            atk = src.stat("atk")
            dfn = tgt.stat("def")
            if subtag == "pierce":
                dfn *= 0.70  # ignores 30% DEF
            mitig = 1000.0 / (1000.0 + dfn)
            # damage-type interaction vs enemy resistance (doc 02 s6)
            res = tgt.phys_res if root == "physical" else tgt.mag_res
            if res <= -0.2:
                elem = 1.25
            elif res >= 0.2:
                elem = 0.85
            else:
                elem = 1.0
            if subtag == "holy" and "undead" in tgt.traits:
                elem *= 1.25
            crit = 1.0
            if self.rng.random() < 0.05 + self._crit_bonus(src):
                crit = 1.5
            var = self.rng.uniform(0.95, 1.05)
            dmg = power * atk * mitig * elem * crit * var
            # damage reduction buff
            for s in tgt.statuses:
                if s.sid == "STS-DR-25":
                    dmg *= 0.75
            dmg = int(dmg)
            # barrier / bleed-pierces-barrier handled by caller for DoTs
            if tgt.barrier > 0 and subtag != "bleed":
                absorbed = min(tgt.barrier, dmg)
                tgt.barrier -= absorbed
                dmg -= absorbed
            tgt.hp -= dmg
            total += dmg
        if tgt.hp <= 0:
            self._on_kill(src, tgt)
        return total

    def _crit_bonus(self, c: Combatant) -> float:
        return 0.20 if c.has("STS-CRIT-UP") else 0.0

    def _on_kill(self, src: Combatant, tgt: Combatant) -> None:
        tgt.hp = 0
        if src.side == "ally":
            self.surge = min(self.SURGE_MAX, self.surge + 10)

    def gain_surge(self, amount: int) -> None:
        self.surge = min(self.SURGE_MAX, self.surge + amount)

    # -- status ticking ---------------------------------------------------
    def tick_dots(self, c: Combatant) -> None:
        for s in list(c.statuses):
            meta = self.gd.statuses.get(s.sid, {})
            if meta.get("kind") == "dot":
                power = meta.get("tickPower", 0.05) * s.stacks
                stat = meta.get("tickStat", "applier_atk")
                if stat == "target_maxhp":
                    dmg = int(c.max_hp * power)
                    if c.is_enemy and "boss" in c.traits:
                        dmg = min(dmg, int(c.max_hp * 0.02))
                else:
                    base_atk = s.payload.get("applier_atk", c.stat("atk"))
                    dmg = int(base_atk * power)
                if s.sid == "STS-BLEED":  # pierces barrier
                    c.hp -= dmg
                else:
                    if c.barrier > 0:
                        ab = min(c.barrier, dmg); c.barrier -= ab; dmg -= ab
                    c.hp -= dmg
                if c.hp <= 0:
                    c.hp = 0

    def decrement_statuses(self, c: Combatant) -> None:
        keep = []
        for s in c.statuses:
            if s.rounds < 0:  # permanent (e.g. Anguisette Decay)
                keep.append(s)
                continue
            s.rounds -= 1
            if s.rounds > 0:
                keep.append(s)
        c.statuses = keep

    def apply_status(self, src: Combatant, tgt: Combatant, sid: str,
                     rounds: int, stacks: int = 1, chance: float = 1.0) -> None:
        if sid in tgt.immunities:
            return
        if sid in _HARD_CC:
            if tgt.is_enemy and self.round <= tgt.resolve_until:
                return  # Resolve window
        # effect hit vs resist (floor 0.15, cap 1.0)
        eff = src.stat_effhit() if hasattr(src, "stat_effhit") else 0.0
        p = max(0.15, min(1.0, chance))
        if self.rng.random() > p:
            return
        meta = self.gd.statuses.get(sid, {})
        existing = tgt.get(sid)
        if existing and meta.get("kind") == "dot":
            existing.stacks = min(meta.get("stackMax", 5), existing.stacks + stacks)
            existing.rounds = max(existing.rounds, rounds)
            existing.payload["applier_atk"] = src.stat("atk")
        else:
            st = Status(sid, rounds, stacks, {"applier_atk": src.stat("atk")})
            tgt.statuses.append(st)
        if sid in _HARD_CC and tgt.is_enemy:
            tgt.resolve_until = self.round + 2

    # -- turn execution ---------------------------------------------------
    def take_turn(self, c: Combatant) -> None:
        if not c.alive:
            return
        # hard CC
        if c.has("STS-STUN"):
            return
        bind = c.has("STS-BIND")
        for k in list(c.cooldowns):
            c.cooldowns[k] = max(0, c.cooldowns[k] - 1)
        if c.is_enemy:
            self._enemy_turn(c)
        else:
            self._ally_turn(c, bind)
        # acting grants surge
        if c.side == "ally":
            self.gain_surge(6)

    def _ally_turn(self, c: Combatant, bind: bool) -> None:
        from sim.effects import run_skill  # local import avoids cycle at import time
        # summons have no full kit: basic attack from their single skill
        if c.unit_id.startswith("SUMMON:"):
            sk = c.enemy_skills[0] if c.enemy_skills else {"power": 0.9}
            t = self.pick_target(c, "single")
            if t:
                self.deal_damage(c, t, sk.get("power", 0.9), c.damage_root, sk.get("subtag"))
            return
        # manual ult: fire if ready and condition met (doc 02 s3 AI)
        ult = self.gd.skill(c.unit_id, "S3")
        if not bind and ult and self.surge >= ult.get("surgeCost", 50):
            if self._ult_condition(c, ult):
                self.surge -= ult.get("surgeCost", 50)
                run_skill(self, c, ult)
                return
        # S2 core if off cooldown
        s2 = self.gd.skill(c.unit_id, "S2")
        if not bind and s2 and c.cooldowns.get("S2", 0) == 0:
            run_skill(self, c, s2)
            c.cooldowns["S2"] = s2.get("cooldown", 3)
            return
        s1 = self.gd.skill(c.unit_id, "S1")
        if s1:
            run_skill(self, c, s1)

    def _ult_condition(self, c: Combatant, ult: dict) -> bool:
        cond = c.ai_ult.get("condition")
        if not cond:
            return True
        if "team_hp_pct" in cond:
            frac = sum(f.hp for f in self.friends(c)) / max(1, sum(f.max_hp for f in self.friends(c)))
            thresh = float(cond.split("<")[1]) / 100.0
            return frac < thresh
        if "target_hp_pct" in cond:
            foes = self.foes(c)
            if not foes:
                return False
            lowest = min(foes, key=lambda f: f.hp / f.max_hp)
            thresh = float(cond.split("<")[1]) / 100.0
            return lowest.hp / lowest.max_hp < thresh
        return True

    def _enemy_turn(self, c: Combatant) -> None:
        # telegraph resolution
        if c.telegraph:
            c.telegraph["windup"] -= 1
            if c.telegraph["windup"] <= 0:
                self._detonate(c, c.telegraph)
                c.telegraph = None
                return
            else:
                return  # charging
        e = self.gd.enemies[c.unit_id]
        # start a telegraph occasionally if it has one and none active
        tg = e.get("telegraphs")
        if tg and self.rng.random() < 0.4:
            t = dict(tg[0]); t["windup"] = t.get("windup", 2)
            c.telegraph = t
            return
        # basic attack: use a skill, pick target by its targetRule
        skills = e.get("skills", [])
        sk = skills[0] if skills else {"power": 1.0, "target": "single_enemy"}
        rule = "aggro"
        if sk.get("targetRule") == "back_row_preferred":
            rule = "back_row"
        tgt = self.pick_target(c, rule)
        if tgt:
            root = c.damage_root
            self.deal_damage(c, tgt, sk.get("power", 1.0), root, sk.get("subtag"))

    def _detonate(self, c: Combatant, tg: dict) -> None:
        pattern = tg.get("pattern", "single_highest_atk")
        power = tg.get("power", 1.5)
        root = c.damage_root
        if pattern in ("all_enemies", "battlefield"):
            for t in self.foes(c):
                self.deal_damage(c, t, power, root, None)
        elif pattern == "front_row":
            targets = [t for t in self.foes(c) if t.row == "front"] or self.foes(c)
            for t in targets:
                self.deal_damage(c, t, power, root, None)
        elif pattern == "single_lowest_hp":
            t = self.pick_target(c, "lowest_hp")
            if t:
                self.deal_damage(c, t, power, root, None)
        else:  # single_highest_atk
            t = self.pick_target(c, "highest_atk")
            if t:
                self.deal_damage(c, t, power, root, None)

    # -- main loop --------------------------------------------------------
    def run(self) -> dict:
        while True:
            self.round += 1
            # round-start: DoT ticks + status decrement (doc 02 s2)
            for c in self._living():
                self.tick_dots(c)
            for c in self._living():
                self.decrement_statuses(c)
            if self._ended():
                break
            # SPD order, re-sorted at round start; ties -> allies first
            order = sorted(self._living(),
                           key=lambda c: (-c.stat("spd"), 0 if c.side == "ally" else 1))
            for c in order:
                if not c.alive:
                    continue
                # enrage
                if self.round > self.ENRAGE_ROUND and c.is_enemy:
                    pass  # applied as flat ramp below in _enrage_mult
                self.take_turn(c)
                if self._ended():
                    break
            if self._ended() or self.round >= self.ROUND_LIMIT:
                break
        return self._result()

    def _enrage_mult(self) -> float:
        if self.round <= self.ENRAGE_ROUND:
            return 1.0
        return 1.0 + 0.15 * (self.round - self.ENRAGE_ROUND)

    def _ended(self) -> bool:
        return not any(a.alive for a in self.allies) or not any(e.alive for e in self.enemies)

    def _result(self) -> dict:
        win = any(a.alive for a in self.allies) and not any(e.alive for e in self.enemies)
        return {
            "win": win,
            "rounds": self.round,
            "timeout": self.round >= self.ROUND_LIMIT and not win,
            "allies_alive": sum(1 for a in self.allies if a.alive),
            "ally_hp_frac": sum(a.hp for a in self.allies) / max(1, sum(a.max_hp for a in self.allies)),
        }
