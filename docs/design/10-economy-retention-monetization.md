# 10 — Economy, Retention & Monetization

## 1. Currency Map (complete — adding a currency post-launch requires removing or merging one: anti-bloat rule)

| Currency | Kind | Sources | Sinks |
|---|---|---|---|
| **Vow Crystals** | Premium (paid + earned) | IAP; first-clears, achievements, codex, events, mail | Summons, stamina refresh (capped 3/day), cosmetics |
| **Summon Tickets** (Standard/Featured) | Pull instruments | Expedition weekly (the big one), battle pass, events, login | Their banner type only |
| **Gold** | Soft | Everywhere (stages, raids, idle, overflow conversion) | Levels, gear enhance, skill-ups, guild creation, re-equip |
| **Aether** | Stamina | Time (1/6 min, cap 240), level-ups, daily gifts ×2 | Campaign, raids, hard mode (co-op Expedition costs **no** Aether — social play never competes with farming budget) |
| **Ember Sigils** | Pity-dust | Dupes, raid pity byproduct | Mercy Forge (doc 08 §5) |
| **Guild Marks** | Guild | Check-in, guild segments, guild weekly | Guild shop |
| **Gleam** | Cosmetic | Expedition score tiers, events, codex | Cosmetics shop only (never power — clean separation) |
| Materials (not currencies): XP Tomes, Star Shards, Starstone, gear + ore, Ascension Relics, skill manuals | — | Doc 07 §1.1 raid mapping | Doc 09 tracks |

**Single-throttle rule:** Aether is the only pacing throttle for solo farming. No per-mode entry keys except boss weekly attempts (which have their own reward-lockout logic). Kills the "seventeen energy types" disease.

## 2. Pacing Targets

| Phase | Feel | Concrete targets |
|---|---|---|
| Early (D1–D7) | Generous flood | Ch.1–2 cleared; ~40 free pulls; 2 units to 3★; all systems unlocked by D3; session value obvious |
| Mid (D8–D45) | Purposeful grind | Ch.3–4 + Hard 1–2; first A2 ascensions; gear sets forming; first full Expedition weeks; 70–80 pulls/month F2P income |
| Late (D45+) | Optimization + cadence | Hard 3–4, Breach III, 6★ pushes, substat hunting in Charm/Sigil slots, banner-cycle roster puzzles |

F2P monthly pull income budget (~75): dailies 20, weeklies (incl. Expedition 10-pull) 18, events 20, codex/achievement drip 7, login 10. This is the number the whole economy is tuned around — change it consciously or not at all.

## 3. Retention Loops

- **Daily (≤20 min):** 2 daily gifts of Aether at fixed clock windows (habit anchors), daily quests (7 tasks, "do 3 → claim all" — no checklist tyranny), Surging raid of the day, Expedition segment with your Lodge. The Expedition segment is the *social appointment* — the strongest daily driver.
- **Weekly:** Expedition arc Mon→Sun with the 10-pull jackpot (doc 07 §2.6); boss lockouts + mutators; guild chest; shop refresh.
- **Login rewards:** rolling 28-day track (no punishing reset on a missed day — track pauses, doesn't reset); day-7-equivalents carry Featured Tickets.
- **Progression missions:** long "Gatewarden's Path" quest chain (200+ steps) that narrates the meta-game: "Ascend any unit to A1", "Full-clear an Expedition", "Field a team of 4 factions"… teaches systems while dripping premium currency.
- **Events (cadence from week 2):** 2-week cycles alternating: (a) point-farm event over existing stages with event shop, (b) mini-story with 5 bespoke stages reusing an enemy family + 1 new elite (cheap content, doc 11 makes the art cheap too). Faction bonus weeks rotate roster relevance (doc 04 §2).
- **Chapter pressure:** next-chapter teaser visible from the map (locked gate silhouette + "power recommendation" — an explicit goal ladder).
- **Roster investment reasons:** weekly boss mutators, faction weeks, Expedition role checks, codex — four independent systems asking for breadth, not one meta team.

## 4. Monetization Design

### Sold at launch
1. **Battle Pass — YES, recommended.** "Gatewarden's Vow", 4-week seasons aligned to Expedition weeks. Free track: real value (tickets, relics). Paid ($9.99): cosmetics, Gleam, tickets, gear ore, *no exclusive units/stats*. Premium+ tier ($19.99) adds instant levels + an exclusive **cosmetic** only.
2. **Monthly Vow Card ($4.99):** 300 Crystals now + 90/day for 30 days — the F2P-adjacent best-value anchor; most important SKU for retention-revenue correlation.
3. **Crystal packs** with standard first-purchase double.
4. **Targeted value packs:** chapter-clear pack, level-milestone packs (fixed contents, clearly priced — no randomized IAP, which also keeps store compliance simple).
5. **Cosmetics (growing over time):** character skins (Higgsfield pipeline makes skin production cheap — same character sheet, new outfit prompt block, doc 11 §5), ult cut-in frames, home-screen themes, guild emblems. Long-term margin lives here.

### Never monetized (published internally as policy)
- Gear, substats, or any stat item for direct money
- Revives / continues in combat (kills difficulty integrity)
- Energy beyond the 3/day refresh cap
- Exclusive-forever units; loot-boxed IAP; rate-up manipulation
- Anything in co-op that creates paid carry pressure

### Positioning statement
"Anime squad RPG where money makes you *faster and prettier*, never *unbeatable*." All store copy, streamer kits, and community messaging align to this. PvE-only launch makes the promise structurally credible.

## 5. Currency-Bloat & Economy Health Guardrails

- Hard cap: ≤8 currencies + material families as listed. New feature must reuse an existing currency or trade one out.
- Every currency has a **terminal sink** (overflow conversion → Gold; Gleam → rotating cosmetic archive) so nothing accumulates meaninglessly.
- Economy telemetry from day one: per-currency faucet/sink dashboards, pull-income percentile tracking, material-wall detection (where players stall) — doc 12 §7 analytics hooks.
