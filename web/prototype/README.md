# ASHGATE — Playable Combat Slice

A single-file, self-contained browser prototype of ASHGATE's core loop —
**summon a roster, equip and upgrade your five, and fight the full four-chapter
campaign** (Slimes → Giants → Guardians → Undead). It turns the spec into
something you can actually tap and play.

## What it demonstrates

- The **doc 02 combat model** running live: SPD-ordered turn engine, the s5
  damage formula (DEF mitigation, damage-type resistance, Holy-vs-Undead, crit,
  variance, DR, barriers), status effects, DoT ticks.
- **Shared Surge** (doc 02 s3) — the team fills one bar; when a hero lights up,
  tap them to fire their ultimate. Manual ults over auto basics = the skill hook.
- The **doc 03 class-VFX identity** — each hero card wears its class hue
  (Roland steel-blue tank, Branwen blood-orange berserker, The Hollow Smile
  crimson assassin, Ordan violet mage, Aurelia gold healer).
- A **telegraphed detonation** (Krul's Umbral Spray) with a windup pip row —
  bank Surge for Roland's team-immunity or answer with Aurelia's heal.
- Ultimate **cut-ins**, floating damage numbers, budding Slimelet adds.
- **Hero progression** on the detail screen: level, star up, equip gear,
  **skill-ups** — level each of S1/S2/S3 (to 5) with Gold to scale that skill's
  damage, healing, and shielding live in the engine (+6% per level) — and
  **Ascension** (A1–A6), the endgame power tier that unlocks at max stars: each
  rank adds +4% core stats and milestone passives (+crit rate at A3, +crit
  damage at A6), paid with **Ash Relics** farmed from Hard mode and the raid.
- **Synthesized sound** — hits, crits, heals, telegraph warnings, ultimate
  swells, and gacha fanfares are generated live with the Web Audio API (no
  audio files, CSP-safe). Toggle with the speaker button; the choice persists.

## Faithful data

Hero stats, skill kits, and enemy stats are extracted from the real
`data/` + `content/` tables via `sim/ashsim.py` (the same numbers the balance
harness uses). The combat math mirrors `sim/ashsim.deal_damage`.

**One deliberate exception:** the demo Krul is scaled (HP ×3.2, ATK ×1.25) for
showcase *pacing* — long enough to see Surge fill and a telegraph fire. That is
a demo knob, not campaign balance; the real tuning lives in the data + sim.

## Mercy Forge (doc 08 s5)

Every summon banks an **Ember Sigil**, and the gate's **Mercy Forge** spends them
on guaranteed units — a Rare Vow (40), an Epic Vow (120), or a **Legendary Vow
(400) you pick yourself** from all fourteen Legendaries. It's the bad-luck floor
under the RNG: pull enough and you choose exactly who you want. Claims prefer new
units and turn dupes into Soul Shards, just like a pull.

## Equipment (doc 09 s5)

The 5-slot gear system is live, not a placeholder multiplier. Each hero has
**Weapon / Armor / Helm / Charm / Sigil** slots; pieces roll a main stat by
slot, 1–4 substats by rarity (C/R/E/L), a tier (T1–T4), and one of six sets.
Enhancing to +5/+10/+15 rerolls a substat higher (the bounded-grind rule).
Gear stats feed the same `computeStats` the battle engine reads, so ATK%, HP%,
DEF, SPD, **crit rate/damage**, and **lifesteal** all change how fights play;
**Aegis 4-pc** grants a battle-start barrier and **Mending** boosts heals.
Pieces come from **stage drops** (bosses drop better) and a gold **Forge**;
**Auto-Equip** fills a hero from the bag. Browsing a slot shows each candidate's
**Gear-Power delta** (▲/▼) vs. what's equipped, and unwanted pieces **scrap for
Gold** (single or bulk "Scrap Commons"). Each hero also keeps **three saveable
loadout presets** (doc 09) — snapshot the current gear, then swap builds in one
tap; applying a preset pulls its pieces back even if another hero borrowed them.
Two set 4-pc effects that aren't pure numbers in the doc (Vanguard/Gravebind)
use a stat proxy here.

## Co-op Raid

A weekly **multi-phase raid boss** — Krul Ascended, the Drowned Crown (120k HP)
— fought as a 30-round **damage race**. She enrages and summons Drowned Hands at
66%, raises a ward and rises into Tidal Cataclysm at 33%. True to doc 07, raids
pay out **by damage percent**: every run banks Crystals and Gold scaled to how
far you got, gear drops at 50%+, and your **best damage %** is tracked — a full
kill is 100%. It's the reason to keep pushing a stronger five even when you
can't one-shot the boss yet.

## PvP Arena

An 8-tier ladder (Bronze → Diamond) of AI **defense squads** built from the real
roster — each a balanced five (tank, two DPS, mage captain, healer) scaled by
rank, with the captain throwing a telegraphed **signature** hit you answer like
a mini-boss. Beat the squad at your rank to climb; each first clear pays out
Crystals and Gold that grow with the tier. It reuses the same turn engine and
damage math as the campaign — the opponents are just heroes fighting back.

## Faction synergies (doc 03/04)

Every hero belongs to one of five factions (Emberguard, Freeblades, Hollowed,
Choir, Gravebound). Field **2+ of the same faction** and the team gains a
matching bonus that scales with the count (+8/14/20/28% at 2/3/4/5): Emberguard
buffs DEF+HP, Freeblades and Gravebound ATK, Hollowed crit, Choir healing+ATK.
The bonus previews live as chips on the team-select screen and fires at battle
start, so thematic teams are a real, visible payoff — not just flavour.

## Home / lobby (doc 16)

The map doubles as a lobby: a persistent **resource header** (Crystals / Gold /
Shards / Ash Relics), a **Featured Summon** card for the rotating banner unit
(Branwen Oathbreaker) with a **Try** button that runs a **banner trial** (doc
08) — test-drive her in a showcase fight against Guardians before you pull, no
reward or roster change — and **Daily Objectives** (win 3 battles, summon once,
enhance gear once) that track your play and pay out on claim, resetting each day.

## Hard mode (endgame farm)

Clearing a chapter's boss on Normal unlocks a **Normal / Hard** toggle on the
map. Any stage you've beaten on Normal can be replayed on **Hard**, where
enemies hit far harder (HP ×1.6, ATK ×1.45, DEF ×1.3) and rewards are the
endgame loop: **doubled** gold and shards every run, a one-time Crystal bonus on
first Hard clear, and gear drops biased to **T3/T4** and Epic/Legendary. It's
the repeatable reason to keep building your five after the story ends.

## Scope / honesty

This is a **playable slice**, not the game. It now covers the core loop —
summon → equip/upgrade → team-build → multi-wave combat across the full
four-chapter campaign (Slimes, Giants, Guardians, Undead — each family flips the
damage-type puzzle, and the finale boss reknits once at the Gate) → **Hard-mode
farm** → **PvP-Arena ladder** → **co-op raid** → persist — but not the backend,
real multiplayer, or the remaining 20 stages of the 40-stage design, which are
specified in `docs/` and `data/` but not built. Class art is CSS/emoji
placeholders (the AI art canon in `art/canon-manifest.json` isn't integrated).
It's the fastest bridge from "validated spec" to "something you can hold."

## Run

Open `index.html` in any browser — no build, no server, no external requests.
Verified end-to-end in headless Chromium (loads clean, plays to a result, no
console errors).
