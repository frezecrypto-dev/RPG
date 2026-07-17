# 09 — Upgrade & Progression Systems

Four interlocking tracks per character: **Level → Stars → Ascension → Gear**. Each has a distinct material source (one system ↔ one raid, doc 07 §1.1) so farming intent is always clear.

## 1. Levels (baseline growth)

- Character Lv 1–60 at launch (raised by 10 per major patch). Cost: Gold + XP Tomes (campaign/idle drops).
- Level cap gated by star grade: 1★→Lv20, 2★→30, 3★→40, 4★→50, 5★→55, 6★→60.
- Growth curves are data (`growth_curve` per rarity, doc 04 §1 multipliers); no per-unit bespoke curves at launch (balance sanity).

## 2. Star Upgrades (the long spine)

- Stars raise base stats (+8% all stats per star) and level cap.
- Cost per star-up: **class-tagged Star Shards** (Starfall Depths raid; class-choice crates, doc 07 §1.3) + Starstone + Gold. Costs grow ~1.8×/star.
- **Rarity fairness mechanic:** star-up costs scale with rarity (Legendary 1.6× Epic), so building a Common to 5★ is genuinely cheap — the "budget carry" economy from doc 04 §1 is enforced here, not just promised.

## 3. Ascension (depth + kit evolution)

- Unlocks at 3★, chapter 3-5. Three Ascension ranks (A1/A2/A3) per character.
- Cost: Ascension Relics (Ash Reliquary raid + Expedition weekly) + faction-tagged relics.
- Each rank grants: stat block + **one kit node** (from the character's `ascension_nodes` list, doc 04 §5) — cooldown reductions, threshold improvements, passive extensions. Nodes deepen the existing kit; they never add brand-new mechanics (skill-text stability rule, doc 02 §4).
- **A3 also raises the star cap** for Commons: a Common at A3 can push 5★→6★ ("Transcendent Common") — the endgame badge-of-honor build that keeps low rarities relevant forever.

## 4. Duplicates / Soul Shards ("Awakening")

- Dupes → Soul Shards (doc 08 §5). Awakening grades W1–W5 per character: +3% stats each, W3 = +1 Surge gen on that unit's actions, W5 = cosmetic aura tint + title.
- Shards needed: Common 5 / Rare 8 / Epic 10 / Legendary 12 total to W5.
- **Deliberately modest:** W5 total = +15% stats + minor utility. A W0 Legendary is fully functional; whales get breadth/coolness, not gated mechanics. This is the anti-P2W keystone: **no skill or mechanic is ever locked behind dupes.**
- Legendary shards drip from Expedition full-clears and Mercy Forge — every unit is eventually maxable F2P (slowly).

## 5. Equipment — exactly 5 slots

| Slot | Main stat pool | Identity |
|---|---|---|
| Weapon | ATK / ATK% | Offense scaler |
| Armor | DEF / HP% | Survival scaler |
| Helm | HP / DEF% | Survival flex |
| Charm | SPD / Crit Rate / Crit Dmg | The chase slot (SPD rolls = endgame currency) |
| Sigil | Effect Hit / Effect Res / Lifesteal | Utility identity slot |

- Gear rarity C/R/E/L, tiers T1–T4 (Foundry raid tiers). Each piece: 1 main stat + up to 4 substats; enhance +0→+15 with ore (substat upgrade every +5, weighted reroll among existing substats — **no new-substat gambling**, keeps gear grind bounded).
- **Sets (launch: 6):** Vanguard (2pc: +12% DEF, 4pc: Taunt-Me grants 15% DR), Slaughter (4pc: +20% Crit Dmg), Swiftvow (4pc: +18% SPD), Mending (4pc: +20% healing), Gravebind (4pc: DoTs +15%), Aegis (2pc: +10% HP, 4pc: battle-start Barrier).
- Gear is unit-agnostic and freely re-equippable for Gold (no equip-lock rent-seeking). Gear score shown; loadout presets per unit; "optimize" auto-equip button (QoL is retention).

## 6. Progression Fairness Rules (anti hard-P2W)

1. Money buys **speed and breadth** (more stamina refreshes/day cap: 3; more pulls), never exclusive stats, gear, or mechanics.
2. Everything farmable: all materials from raids/expedition; all units eventually via Mercy Forge.
3. Content is tuned against **gear + level benchmarks reachable F2P on schedule** (benchmark table lives with the balancing sheets, doc 15 §4) — never against whale stat ceilings.
4. Power deltas: a day-1 whale should peak at ~2× an engaged F2P at day 30, converging to ~1.3× by day 120 (dupe modesty + material caps do this math). PvE-only design makes this tolerable — no one is farmed *by* whales.
5. Weekly material caps on the fastest paid paths (stamina refresh cap) prevent infinite-spend blowout and protect long-term pacing.
