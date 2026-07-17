# 02 — Combat System

## 1. Combat Model Recommendation

**Chosen model: Speed-ordered turn-based combat with cooldown skills and a shared/manual ultimate resource ("Surge"), semi-auto by default.**

### Why this model (vs. alternatives)

| Model | Verdict | Reason |
|---|---|---|
| Real-time with energy (AFK-style) | Rejected | Weak strategic depth for boss counterplay; hard to make co-op contribution legible |
| Full ATB real-time (Summoners-War-like) | Rejected | Speed-stat tyranny distorts gear economy; punishing to autoplay |
| Pure turn-based, fixed order | Rejected | Too static; speed as a stat becomes meaningless |
| **Speed-ordered turn-based + cooldowns + manual ults (chosen)** | ✅ | Readable on mobile, deterministic enough for server validation and co-op sync, autoplay-friendly, boss telegraphs map cleanly to "turns until detonation" |

Determinism matters technically: turn-based with seeded RNG lets the server validate battle results cheaply and lets co-op run lockstep (doc 12 §6).

### Turn order
- Each round, all living units (allies + enemies) act once, ordered by **SPD** (ties: player units first, then slot order).
- SPD buffs/debuffs re-sort at round start only (prevents mid-round order chaos — readability rule).
- Boss "pressure turns" (extra actions) are explicit and telegraphed, never silent.

## 2. Combat Loop (one round)

```
Round start → resolve start-of-round effects (DoTs tick, buffs decrement)
→ units act in SPD order:
    unit turn: [auto: AI picks skill by priority] or [manual: player taps skill]
→ round end → check win/loss → next round
```
- Stage limit: 20 rounds (loss on timeout — prevents infinite heal stalls; bosses use enrage instead, §8).
- Player ultimates ("Surge skills") can be fired **manually at any point during any ally turn** — this is the manual-play hook that stays interesting even with auto basic skills.

## 3. Skill Resources

Two resources, deliberately simple:

1. **Cooldowns** — Skill 2 of every unit runs on a cooldown (2–4 rounds). No mana. Cooldowns are per-unit, tick at the unit's turn start.
2. **Surge (ultimate energy)** — a **team-shared bar, 0–100**, gained by: ally acts (+6), ally takes a hit (+4), enemy killed (+10). An ultimate costs **50 Surge** (Legendary ultimates: 60, they hit proportionally harder). Shared Surge is a core design choice: it forces a *team decision* ("whose ult do we bank for?") and lets support units generate value for carries.

**Autoplay Surge AI:** fires the highest-priority ult per unit's `aiUltPriority` field when Surge ≥ cost and its condition is met (e.g., Healer ult only under 60% team HP). Data-driven per unit (doc 15).

## 4. Skill Structure Per Character

Every character has exactly **4 skills at launch** (uniform structure = balance + UI + data sanity):

| Slot | Name | Type | Notes |
|---|---|---|---|
| S1 | Basic | Always available, no cost | Defines the unit's default damage/utility identity |
| S2 | Core | Cooldown 2–4 rounds | The tactical decision skill |
| S3 | Ultimate | Costs Surge (50/60) | The fantasy moment; gets a cut-in animation |
| S4 | Passive | Always on | Class identity + synergy hooks; upgrades via Ascension (doc 09) |

Skill levels: each skill upgradeable Lv1→Lv5 with class skill manuals (raid material). Skill-up = flat effect % increases only, never new mechanics (mechanics changes live in Ascension nodes — keeps skill text stable).

## 5. Stats

Primary: **HP, ATK, DEF, SPD**. Secondary: **Crit Rate (base 5%), Crit Damage (base 150%), Effect Hit, Effect Resist, Lifesteal, Damage Reduction**.

Damage formula (baseline):
```
damage = SkillPower% × ATK × (1000 / (1000 + targetDEF_effective)) × critMult × elementMod × varianceRoll(0.95–1.05)
```
- DEF uses diminishing-returns curve (1000-constant) so DEF stacking is good but not infinite.
- `elementMod` = damage-type interaction (§7): 1.25 / 1.0 / 0.85.

## 6. Damage Types & Sub-tags

Two root types every enemy has explicit resistances against:
- **Physical** (mitigated by DEF)
- **Magical** (mitigated by RES — a hidden stat folded into DEF for players, explicit for enemies)

Sub-tags (a skill has 0–1 sub-tag; sub-tags interact with enemy traits & status system, kept to six):

| Sub-tag | Root type | Identity | Primary class |
|---|---|---|---|
| Bleed | Physical | Stacking DoT, physical | Assassin |
| Pierce | Physical | Partially ignores DEF (30%) | Ranger |
| Arcane | Magical | Pure magic, dispel-interaction | Mage |
| Shadow | Magical | Umbra-themed, feeds Necromancer mechanics | Necromancer |
| Holy | Magical | Bonus vs Undead trait (+25%) | Healer (offense), some Tanks |
| Decay | Magical | Anti-heal interaction | Necromancer / enemies |

Rule: sub-tags are *hooks*, not a full elemental wheel. No fire/water/wind circle at launch — it multiplies roster demands by element and punishes small rosters. Revisit post-launch only if roster > 120.

## 7. Enemy Resistance & Weakness Logic

Every enemy has:
- `physRes` / `magRes`: −25% (weak) / 0 (neutral) / +25% (resistant) — shown as icons on the enemy info panel and stage-prep screen.
- `traits[]`: e.g. `Undead`, `Armored`, `Swarm`, `Colossal`, `Construct` — traits interact with sub-tags and skills ("+25% vs Undead", "Armor Break removes Armored's DR").
- `debuffImmunities[]`: bosses only, max 2, always displayed (e.g. immune to Stun, not to Slow).

**Team-check rule:** every chapter's enemy mix must make at least 2 of the 4 role boxes (frontline / damage / sustain / utility) mandatory, and each chapter biases one damage root type so mono-damage teams stall (doc 06).

## 8. Buff / Debuff Framework

- Buffs/debuffs are **standardized tokens** — same icon, same math, whoever applies them. Character uniqueness comes from *when/how/how many*, not from bespoke stat math. This is the single most important balance-scalability rule in the game.
- Duration in rounds, decrement at owner's turn start. Max 8 visible effects per unit (UI cap; excess refreshes shortest).
- **Effect Hit vs Effect Resist:** applyChance × (1 + EffHit − EffRes), floor 15%, cap 100%.
- Dispel verbs: `Cleanse` (remove ally debuffs), `Strip` (remove enemy buffs), `Steal` (Mage-exclusive rare verb), `Block` (immunity shield).

### Status Effect Taxonomy (launch set — 18 total, do not exceed 24 in year 1)

**Offensive buffs:** ATK Up (+30%), Crit Up (+20%), SPD Up (+25%), Focus (+30% Effect Hit)
**Defensive buffs:** DEF Up (+30%), Barrier (flat shield, scales on caster), Immunity (blocks next N debuffs), Stealth (untargetable, breaks on acting offensively), Taunt-Me (Tank self-buff: forces enemy targeting)
**Stat debuffs:** ATK Down (−30%), DEF Down (−30%), SPD Down (−25%), Armor Break (−40% DEF, physical-only mitigation, Ranger signature)
**DoTs:** Bleed (physical, stacks ×5, each stack 8% ATK of applier/round), Poison (magical, %maxHP-capped vs bosses), Burn-equivalent **Decay** (magical DoT + 50% healing reduction)
**Control:** Stun (skip turn, 1 round, bosses immune-after-1: see below), Slow-lock **Freeze-equivalent "Bind"** (can act but only S1), **Mark** (Ranger signature: +20% damage taken from all sources, focus-fire enabler)

**Control anti-abuse:** bosses gain `Resolve` — after any hard CC lands, boss is CC-immune for 2 rounds. Prevents stun-lock, keeps CC valuable as an *interrupt* tool (see telegraph counterplay, doc 05 §3).

## 9. Class Interaction Logic (rock-paper-scissors of roles, not stats)

- **Tanks** make Taunt-Me + DR the answer to boss single-target detonations.
- **Rangers** answer `Armored`/high-DEF via Armor Break + Pierce; Mark makes everyone else better.
- **Assassins** answer backline threats and heal-stallers (bleed ignores Barrier: bleeds tick through shields — their designed niche).
- **Mages** answer `Swarm` waves (AoE) and buff-reliant enemies (Strip/Steal).
- **Necromancers** answer attrition fights: summons soak targeting, Decay answers regenerating enemies.
- **Healers** answer DoT/Decay pressure (Cleanse) and burst chapters (Barrier/revive).
- **Berserkers** answer HP-sponge enemies: damage scales with own missing HP + Execute (<25% HP bonus) — the enrage-race class.

## 10. Counterplay Logic (player-side checklist the AI director tests)

Every stage is authored against this matrix — at least two rows must be "tested" per stage, four per boss:

| Threat authored | Player answer |
|---|---|
| Big single-target telegraph | Taunt / Stealth the target / Barrier / kill before detonation |
| AoE detonation | Team-wide DR (Tank ult) / burst-heal after / Immunity pre-cast |
| Enemy buffs (Enrage, DEF Up) | Strip / Steal |
| Stacked DoTs on allies | Cleanse / Immunity |
| Adds spawning (Swarm) | Mage AoE / Necro summons body-block |
| Heal-stalling enemy | Decay (anti-heal) / burst windows / Bleed pressure |
| High-DEF wall | Armor Break / Pierce / magical damage swap |
| Boss enrage timer | Berserker execute race / Surge banking |

## 11. Manual vs Auto

- **Manual:** choose targets, choose S2 timing, fire ults at chosen moments (the skill ceiling: banking 100 Surge to double-ult inside a boss's vulnerability window).
- **Semi-auto (default):** S1/S2 automatic by AI priority list; ults manual.
- **Full auto:** everything automatic; unlocked per-stage after a 3-star clear. Auto uses the same data-driven AI as enemy units — no hidden player-favoring logic, so auto results are reproducible and server-verifiable.
