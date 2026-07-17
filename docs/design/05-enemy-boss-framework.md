# 05 — Enemy & Boss Design Framework

## 1. Enemy Families

Enemies are built from **families** (shared silhouette + palette + mechanic theme) with 3 tiers each: **Minion → Elite → Miniboss**. Family palettes must not collide with the 7 reserved class VFX pairs (doc 03 §3).

| Family | Chapter | Traits | Palette | Mechanic theme |
|---|---|---|---|---|
| Slimes (Umbral Ooze) | 1 | Swarm | Toxic teal / murk green | Split on death, absorb, DoT residue |
| Giants (Gatecrushed) | 2 | Colossal, Armored | Granite / rust red | Slow heavy telegraphs, AoE slams, armor phases |
| Guardians (Failed Wards) | 3 | Construct, Armored | Marble / dead gold | Shields, buff auras, damage-type phase-locks |
| Undead (Gravetide) | 4 | Undead | Bone / grave green | Resurrection, Decay, attrition, anti-heal pressure |

Each family: 4 minion species, 2 elite species, 1 miniboss species, 1 chapter boss (doc 06 stage math). Elites = minion + one *new verb*; minibosses = elite + one *telegraphed detonation*.

## 2. Enemy Readability Rules (mobile contract)

1. **Size = threat.** Minions ≤ 0.8× hero height, elites ≈ 1.2×, minibosses ≈ 2×, bosses 3–4× (multi-cell units).
2. **Color = damage type.** Warm rim-light = physical attacker, cool rim-light = magical. Consistent across all families.
3. **One telegraph language.** Charging attacks show a countdown pip row above the enemy (`◆◆◇` = 2 of 3 turns charged). Every player must learn exactly one telegraph grammar.
4. **Weakness icons on contact.** Tapping any enemy shows res/weak/traits/immunities — no hidden rules, ever (fairness pillar).

## 3. Boss Design Framework

Bosses are single creatures, multi-phase, built from this sheet structure:

### Boss anatomy (every boss must define all rows)

| Field | Rule |
|---|---|
| Phases | 2 (campaign) or 3 (endgame/raid); phase break at 60%/30% HP with a free "stagger round" |
| Telegraphed detonation | 1 per phase, 2–3 turn countdown, always answerable by ≥2 counterplay rows from doc 02 §10 |
| Aggro rule | 60/40 front/back weighting; Taunt-Me overrides; some bosses "target lowest HP" (stated on info panel) |
| Debuff immunities | Max 2, displayed. Never immune to *both* Strip-bait buffs and CC (must have one openable lever) |
| Resolve | CC-immunity 2 rounds after any hard CC lands (doc 02 §8) |
| Enrage | Round 15: +15% ATK per round thereafter (kills heal-stall; replaces round-timeout loss for bosses) |
| Add spawns | Optional; adds must matter (heal boss, shield boss, detonate) — never filler HP |
| Class counterplay | The sheet names which 2–3 class verbs the boss is "about" |
| Reward logic | First-kill: milestone chest (premium currency + gear). Repeat: weekly loot lockout with daily "boss ticket" partial rewards (doc 07 §1.3) |
| Replay reason | Weekly rotating mutator (e.g. "boss is Swarm-flanked this week") + score-tiered material payouts |

### Punishing lazy team-building (mandated per boss)
Every boss must include **at least one hard comp-check and one soft comp-check**:
- Hard check example: detonation that one-shots without Taunt redirect, DR, or a burst-kill of a summoned "conduit" add.
- Soft check example: stacking DoTs that make Cleanse-less teams finish at half speed but not fail.

## 4. Example Boss Sheets (the 4 chapter bosses)

### 4.1 KRUL, THE MOTHER-MASS (Chapter 1 — Slimes)
- **Traits:** Swarm, magRes+25% | **Immune:** Bind | **Phases:** 2
- **Identity check taught:** AoE damage + burst discipline.
- P1: splits a Slimelet pair every 2 rounds; slimelets detonate (team AoE) on a ◆◆◇ 2-turn telegraph → *answer: Mage AoE or focus-fire.*
- P2 (60%): absorbs living slimelets to heal 8%/each → *answer: clear adds BEFORE phase push; teaches phase-timing.*
- **Counterplay classes:** Mage (clear), Ranger (Mark focus), Necromancer (Decay stops absorb-heal).

### 4.2 HARROWJAW, GATECRUSHED TITAN (Chapter 2 — Giants)
- **Traits:** Colossal, Armored (30% DR) | **Immune:** Stun, ATK Down | **Phases:** 2
- **Check taught:** frontline + Armor Break.
- P1: "Skyfall Fist" 3-turn telegraph on the highest-ATK ally; unmitigated = near-oneshot → *answer: Taunt-Me, Barrier, or Stealth.*
- P2 (60%): gains DEF Up every round → *answer: Strip or Armor Break race (Fletch's job — Common relevance by design).*
- **Counterplay classes:** Tank (redirect), Ranger (Armor Break/Pierce), Berserker (Chainbreak-style anti-armor).

### 4.3 THE VIGIL AT WORLD'S SHOULDER (Chapter 3 — Guardians)
- **Traits:** Construct, Armored | **Immune:** Bleed, Decay | **Phases:** 3
- **Check taught:** damage-type flexibility + buff management.
- Phase-lock mechanic: alternates "Null Plating" (immune to Physical) and "Ward Lattice" (immune to Magical) every 3 rounds, telegraphed → *answer: bring both damage roots (kills mono-damage teams by design — the doc 02 §7 team-check flagship).*
- Casts self-buffs (ATK Up, Counter) → *answer: Strip/Steal.*
- **Counterplay classes:** Mage (Strip/Steal + magical root), any physical DPS, Healer (chip sustain through long fight).

### 4.4 ANNOR-VHOL, THE GRAVETIDE CHORUS (Chapter 4 — Undead, launch finale)
- **Traits:** Undead (Holy +25%) | **Immune:** Stun, Poison | **Phases:** 3
- **Check taught:** anti-heal, Cleanse, and revive economy — the full curriculum exam.
- P1: stacks Decay on the team every round → *answer: Cleanse cadence (Father Ambrose viable — Common relevance).*
- P2 (60%): raises 2 Bonewrought adds that channel a mass-fear detonation; boss heals 5%/round while they live → *answer: add-burst + anti-heal (Widow Isolde viable).*
- P3 (30%): "Chorus of Ending" — 3-turn full-team detonation, repeats every 4 rounds → *answer: Tank ult DR / Immunity cycling / execute race.*
- **Counterplay classes:** Healer (Holy offense + Cleanse), Necromancer (anti-heal), Berserker (P3 race).

## 5. Boss Reward & Replay Logic (summary; economy detail in doc 10)

- First clear per difficulty: premium currency (roughly one multi-pull across a chapter's boss set), guaranteed gear piece of the boss's set.
- Weekly repeat: 3 free attempts/week/boss + boss tickets from dailies; score tiers (S/A/B) scale material payouts ~1.5×/1.2×/1.0×.
- Rotating weekly mutators change optimal comps → roster breadth incentive (retention pillar, doc 10 §4).
