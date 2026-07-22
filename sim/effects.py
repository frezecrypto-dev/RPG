"""Skill verb interpreter for the ASHGATE sim.

Implements the doc 15 s2 verb whitelist to the fidelity a Phase-0 balance
sweep needs. Verbs not yet modelled are counted in battle.unhandled so the
balance report can state coverage honestly rather than silently no-op.
"""
from __future__ import annotations


def _targets(battle, src, target: str):
    if target in ("single_enemy",):
        t = battle.pick_target(src, "single")
        return [t] if t else []
    if target == "splash2":
        foes = battle.foes(src)
        if not foes:
            return []
        primary = battle.pick_target(src, "single") or foes[0]
        rest = [f for f in foes if f is not primary]
        return [primary] + rest[:1]
    if target == "all_enemies":
        return battle.foes(src)
    if target == "self":
        return [src]
    if target in ("single_ally", "lowest_hp_ally"):
        friends = battle.friends(src)
        return [min(friends, key=lambda f: f.hp / f.max_hp)] if friends else []
    if target == "team_ally":
        return battle.friends(src)
    return []


# verbs that carry no runtime effect in a balance sweep (identity/among-existing
# reroll flavour, or handled structurally elsewhere) — not counted as gaps
_NOOP_VERBS = {"battleStartChoice", "ignore"}


def run_skill(battle, src, skill: dict) -> None:
    target = skill.get("target", "single_enemy")
    power = skill.get("power", 0) or 0
    root = skill.get("subtag") and _root_for_subtag(skill["subtag"]) or src.damage_root
    subtag = skill.get("subtag")
    hits = skill.get("hits", 1)
    tgts = _targets(battle, src, target)

    # primary damage component
    if power and target not in ("self", "team_ally", "single_ally", "lowest_hp_ally"):
        for t in tgts:
            battle.deal_damage(src, t, power, root, subtag, hits)
            _lifesteal(battle, src, skill, power)

    for eff in skill.get("effects", []):
        verb = eff.get("verb")
        if verb == "applyStatus":
            _apply(battle, src, eff, tgts, target)
        elif verb == "heal":
            _heal(battle, src, eff, tgts, target)
        elif verb == "shield":
            _shield(battle, src, eff, tgts, target)
        elif verb == "cleanse":
            for t in (battle.friends(src) if target == "team_ally" else tgts):
                _cleanse(battle, t, eff.get("count", 1))
        elif verb in ("strip", "steal"):
            for t in tgts:
                _strip(battle, t, eff.get("count", 1))
        elif verb == "dotTick":
            for t in tgts:
                battle.tick_dots(t)
        elif verb in ("consumeStatus",):
            for t in tgts:
                _consume_bleed(battle, src, t, eff)
        elif verb == "execute":
            for t in tgts:
                _execute(battle, src, t, eff)
        elif verb == "rageMod":
            src.rage = min(10, src.rage + eff.get("amount", 1))
        elif verb == "selfCost":
            src.hp = max(1, src.hp - int(src.max_hp * eff.get("hpPct", 0.05)))
        elif verb == "surgeMod":
            if eff.get("trigger") in (None, "immediate"):
                battle.gain_surge(eff.get("amount", 0))
        elif verb == "summon":
            _summon(battle, src, eff)
        elif verb == "lifesteal":
            pass  # applied with primary damage
        elif verb == "revive":
            _revive(battle, src, eff, tgts, target)
        elif verb == "damageMod":
            _bonus_damage(battle, src, eff, tgts)
        elif verb in _NOOP_VERBS:
            pass
        else:
            battle.unhandled[verb] = battle.unhandled.get(verb, 0) + 1

    # rage-scaling for berserker ults that spend/scale on stacks
    if any(e.get("per") == "rage_stack" for e in skill.get("effects", [])) and tgts:
        for t in tgts:
            bonus = power * 0.08 * src.rage
            battle.deal_damage(src, t, bonus, root, subtag)


def _root_for_subtag(subtag: str) -> str:
    return {"bleed": "physical", "pierce": "physical",
            "arcane": "magical", "shadow": "magical",
            "holy": "magical", "decay": "magical"}.get(subtag, "physical")


def _apply(battle, src, eff, tgts, target):
    override = eff.get("targetOverride")
    if override == "self":
        dests = [src]
    elif override == "team_ally":
        dests = battle.friends(src)
    elif override in ("adjacent_enemies", "summons", "random_ally"):
        dests = tgts
    else:
        dests = (battle.friends(src) if target == "team_ally" else tgts)
    for t in dests:
        battle.apply_status(src, t, eff["status"], eff.get("duration", 2),
                            eff.get("stacks", 1), eff.get("chance", 1.0))


def _heal(battle, src, eff, tgts, target):
    override = eff.get("targetOverride")
    if override == "team_ally" or target == "team_ally":
        dests = battle.friends(src)
    elif override == "lowest_hp_ally":
        f = battle.friends(src)
        dests = [min(f, key=lambda x: x.hp / x.max_hp)] if f else []
    elif override == "self":
        dests = [src]
    else:
        dests = tgts if tgts else battle.friends(src)
    stat = eff.get("powerStat", "caster_atk")
    base = src.stat("atk") if "atk" in stat else src.max_hp if "maxhp" in stat else src.stat("def")
    amt = int(base * eff.get("power", 1.0))
    for t in dests:
        if t.side == "ally":
            t.hp = min(t.max_hp, t.hp + amt)


def _shield(battle, src, eff, tgts, target):
    dests = battle.friends(src) if target == "team_ally" else (tgts or battle.friends(src))
    stat = eff.get("powerStat", "caster_def")
    base = src.stat("def") if "def" in stat else src.stat("atk")
    amt = int(base * eff.get("power", 1.0))
    for t in dests:
        if t.side == "ally":
            t.barrier = max(t.barrier, amt)


def _cleanse(battle, t, count):
    debuffs = [s for s in t.statuses
               if battle.gd.statuses.get(s.sid, {}).get("kind") in ("debuff", "dot", "control")]
    for s in debuffs[:count]:
        t.statuses.remove(s)


def _strip(battle, t, count):
    buffs = [s for s in t.statuses
             if battle.gd.statuses.get(s.sid, {}).get("kind") in ("buff", "shield")]
    for s in buffs[:count]:
        t.statuses.remove(s)


def _consume_bleed(battle, src, t, eff):
    st = t.get("STS-BLEED")
    if not st:
        return
    per = eff.get("perStackPower", 0.6)
    battle.deal_damage(src, t, per * st.stacks, "physical", "bleed")
    t.statuses.remove(st)


def _execute(battle, src, t, eff):
    thresh = eff.get("threshold", 0.25)
    is_boss = "boss" in t.traits or (t.is_enemy and t.max_hp > 5000)
    if not is_boss and t.hp / t.max_hp <= thresh:
        battle._on_kill(src, t)


def _bonus_damage(battle, src, eff, tgts):
    # conditional flat bonus multipliers applied as extra damage when condition met
    cond = eff.get("condition", "")
    amt = eff.get("amount", 0)
    for t in tgts:
        ok = False
        if "target_hp_pct<" in cond:
            ok = t.hp / t.max_hp < float(cond.split("<")[1])
        elif "target_has:" in cond:
            ok = t.has(cond.split(":")[1])
        elif cond == "target_has_buff":
            ok = any(battle.gd.statuses.get(s.sid, {}).get("kind") == "buff" for s in t.statuses)
        if ok:
            battle.deal_damage(src, t, amt, src.damage_root, None)


def _lifesteal(battle, src, skill, power):
    for eff in skill.get("effects", []):
        if eff.get("verb") == "lifesteal":
            heal = int(src.stat("atk") * power * eff.get("pct", 0.2))
            src.hp = min(src.max_hp, src.hp + heal)


def _revive(battle, src, eff, tgts, target):
    dead = [f for f in battle.team(src.side) if not f.alive]
    if dead:
        t = dead[0]
        t.hp = int(t.max_hp * eff.get("hpPct", 0.35))


def _summon(battle, src, eff):
    from sim.ashsim import Combatant
    sid = eff.get("summonId")
    smeta = battle.gd.summons.get(sid)
    if not smeta or sid == "BUILD_CHOICE":
        smeta = battle.gd.summons.get("SMN-SKEL-BRUISER") or {
            "statsPctOfMaster": {"hp": 0.45, "atk": 0.6, "def": 0.5, "spd": -8},
            "skill": {"power": 0.9}, "damageRoot": "physical"}
    cap = eff.get("max", 2)
    current = [c for c in battle.allies if c.name.startswith(src.name + "'s")]
    if len(current) >= cap:
        return
    pcts = smeta["statsPctOfMaster"]
    st = {"hp": int(src.max_hp * pcts["hp"]), "atk": int(src.stat("atk") * pcts["atk"]),
          "def": int(src.stat("def") * pcts["def"]), "spd": int(src.stat("spd") + pcts["spd"])}
    summon = Combatant(name=f"{src.name}'s {smeta.get('name', 'Summon')}", side="ally",
                       unit_id=f"SUMMON:{sid}", stats=st, is_enemy=False,
                       damage_root=smeta.get("damageRoot", "physical"))
    summon.enemy_skills = [smeta.get("skill", {"power": 0.9})]
    battle.allies.append(summon)
