# ASHGATE — Playable Combat Slice

A single-file, self-contained browser prototype of ASHGATE's core loop —
**summon a roster, equip and upgrade your five, and fight the full four-chapter
campaign** (Slimes → Giants → Guardians → Undead). It turns the spec into
something you can actually tap and play.

## What it demonstrates

- The **doc 02 combat model** running live: SPD-ordered turn engine, the s5
  damage formula (DEF mitigation, damage-type resistance, Holy-vs-Undead, crit,
  variance, DR, barriers), status effects, DoT ticks.
- **A real battlefield, not cards** — combat is staged with **full-body
  character standees**: your five stand in formation on the painted chapter
  key-art, facing a line of enemies, each on the background-removed cutout art
  (70 hero cutouts + generated enemy cutouts). Everyone **idle-breathes**,
  **lunges** when they strike, **recoils** on a hit, and **falls** on death,
  with floating name + HP bars and a ground shadow — so a fight reads like a
  scene, not a spreadsheet of tiles. (Arena stages both squads as hero standees;
  a handful of Undead foes awaiting cutouts fall back to a soft-masked portrait.)
- **Tactical turns** (doc 02 s11) — the manual-play layer the spec calls for:
  on each of your heroes' turns the fight **pauses** and a command bar offers the
  unit's **Basic / Core (cooldown) / Ultimate (Surge)** skills; you pick the
  skill *and* tap the target. One tap of **Auto** hands the whole fight to the
  same data-driven AI for farming, and you can flip Manual/Auto mid-battle.
- **Break / Toughness** (the weakness core, à la Honkai: Star Rail). Every enemy
  shows its **weakness types** (⚔ physical / ✦ magical / ☀ holy) and a cyan
  **toughness bar**. Hitting a weakness drains toughness; empty it and the enemy
  **BREAKS** — stunned for a turn, hit by a burst, and left **+25% vulnerable**.
  This turns the damage-type triangle into the central tactical loop and the real
  reason to build a broad, varied roster instead of one team.
- **Cinematic focus** — the unit taking its turn is spotlit in **full vision**
  (enlarged, lit, the rest of the field dimmed), with a **turn-order timeline**
  across the top so you can read who acts next and plan your breaks.
- **Shared Surge** (doc 02 s3) — the team fills one bar; ultimates cost 50/60 and
  are chosen from the command bar (or, in Auto, tap a lit hero to fire early).
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

## Codex

A collection screen (Heroes ▸ Codex) tracks completion — owned / 70 with a big
percentage — and breaks the roster down **by rarity, by class, and by faction**.
Each faction card shows its roster as class glyphs (owned lit, missing greyed)
and its synergy bonus; tapping an owned glyph jumps to that hero's detail page,
which now names their faction alongside role and class.

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

## Battle Pass (doc 10 s5)

A **Gatewarden's Vow** season pass (Heroes ▸ *Pass* from the map) — 50 levels,
1000 XP each, earned by winning battles and claiming daily objectives. A
two-track reward rail (free + premium) mirrors the doc's economy: every level
pays Gold on the free track and Crystals + gear ore on premium, with milestone
levels (5/10/20/30/40/50) dropping summon **Vow tickets**, Ash Relics, star
crates, and cosmetics. Rewards claim per-node or **Claim All**, and state
persists. A clearly-labelled **Unlock Premium (demo)** button opens the paid
track — faithful to doc 10's rule that the pass sells **cosmetics and
acceleration only, never exclusive units or stats**.

## Events / Live-Ops (doc 10 s3)

A **Live-Ops** hub (bottom-bar *Events*) runs the retention cadence from the
design's `data/events.json`:

- **Faction Week** — a 5-week rotation (Emberguard → Hollowed → Choir →
  Freeblades → Gravebound, keyed off the real calendar) grants **+15% ATK / DEF /
  HP** to every unit of the featured faction. It's not a banner — it fires at
  battle start in every campaign, raid, and arena fight, stacking on top of the
  faction-synergy bonus, so the rotating spotlight actually changes which of your
  heroes are worth fielding this week.
- **Point-farm event** ("Ember Reclamation") — clearing any PvE stage banks
  **Ember Cinders** (bosses and Hard runs pay more). A **milestone rail**
  (500 / 2,000 / 5,000) drops Crystals, a Featured Vow ticket, and a cut-in
  cosmetic, while an **event shop** spends the same Cinders on Featured Vow
  tickets, Ash Relics, Star Crates, Gleam, and Gold — each with a purchase cap,
  exactly as the config specifies. A live countdown shows the 2-week window.
- **28-day login track** — one claim per calendar day, in order; miss a day and
  it *pauses, never resets* (doc 10). Milestone days (7 / 14 / 21 / 28) carry
  Featured Vow tickets and Crystal drops — the F2P retention anchor.

All of it persists in the save (schema v3) alongside your progress.

## Shop / Store (doc 10 s4)

A **Gate Market** (🛒 on the home screen) implements the launch monetization
surface from `data/shops.json`, faithful to the doc's "money makes you *faster
and prettier*, never *unbeatable*" policy:

- **Monthly Vow Card** — the best-value anchor: **300 Crystals now + 90/day for
  30 days** (3,000 total). Buying it activates a daily claim that pays out once
  per calendar day and expires after 30, with a progress bar and a home-screen
  notify dot when today's 90 is waiting.
- **Crystal packs** with the standard **first-purchase double** (badged, and the
  bonus is consumed after the first buy of each pack), plus **daily crystal-spend
  deals** (Gold, Star Crates) that reset each day.
- **Value packs** — the Gatewarden's Bundle, Chapter Clear, and Ascension packs:
  fixed contents, clearly priced, **no randomized boxes**.
- **Cosmetics** bought with **Gleam only** — a clean cosmetic-only currency
  (skins, cut-in frames, home themes) that never touches power. Gleam is now a
  real balance earned from the Battle Pass premium track and the event shop, so
  the cross-system loop closes.

Real-money SKUs are clearly marked **demo** and grant their contents free with a
spend-confirm (no payment), so the whole store is explorable. All of it persists.

## Hard mode (endgame farm)

Clearing a chapter's boss on Normal unlocks a **Normal / Hard** toggle on the
map. Any stage you've beaten on Normal can be replayed on **Hard**, where
enemies hit far harder (HP ×1.6, ATK ×1.45, DEF ×1.3) and rewards are the
endgame loop: **doubled** gold and shards every run, a one-time Crystal bonus on
first Hard clear, and gear drops biased to **T3/T4** and Epic/Legendary. It's
the repeatable reason to keep building your five after the story ends.

## Accessibility & polish

The combat log and result screen are `aria-live` regions, so screen readers
announce each action and the outcome. Party cards are real buttons — focusable
and **keyboard-operable (Enter/Space fires the ultimate)** — and enemy cards
carry labels. A focus-visible ring and a gentle screen-fade transition round it
off, both respecting `prefers-reduced-motion`.

## Onboarding

First launch opens a five-slide primer — what ASHGATE is, roles & faction
synergy, shared Surge and manual ultimates, reading boss telegraphs, and the
progression/endgame loop — so a new player knows the hooks before the first
fight. Returning players skip it; anyone can replay it from ⚙ Settings ▸ How to
play.

## Settings

A ⚙ menu (top-right) holds sound, default battle speed, and default Auto-Ult
toggles — all persisted — plus **save export/import**: your whole save encodes to
a text code you can copy to back up or move to another browser, and paste back to
restore. A guarded Reset wipes everything. It's the practical answer to
localStorage-only progress.

## Scope / honesty

This is a **playable slice**, not the game. It now covers the core loop —
summon → equip/upgrade → team-build → multi-wave combat across the full
four-chapter campaign (Slimes, Giants, Guardians, Undead — each family flips the
damage-type puzzle, and the finale boss reknits once at the Gate) → **Hard-mode
farm** → **PvP-Arena ladder** → **co-op raid** → persist — but not the backend,
real multiplayer, or the remaining 20 stages of the 40-stage design, which are
specified in `docs/` and `data/` but not built.

**Character art:** all 70 heroes' real generated portraits (the AI art canon in
`art/canon-manifest.json`) are **embedded** into the page as compact WebP `data:`
URIs — so they render everywhere, offline and inside the CSP-locked artifact,
with no external requests. Each portrait sits over a **procedural class crest**
(inline SVG line-art: shield, axe, dagger, bow, star, skull, halo-cross, in the
class hue) that shows through if an image is ever missing. On the hero-detail
screen every hero is a **living, background-separated portrait**: a
background-removed cut-out of the character floats in front of a blurred,
dimmed backdrop of the same art, and a `requestAnimationFrame` loop drifts the
two layers by different amounts (idle sway, or pointer tilt) for a real sense of
depth — plus a breathing class-hue aura and rising ember motes. **Enemies use their real generated art too** — the
36 monster/boss portraits (Slimes, Giants, Guardians, Undead) are embedded, and
most are **background-removed into battlefield standees** (the rest use a
soft-masked portrait until their cutout is generated); arena opponents stand as
the real hero cutouts since they're heroes fighting back. Fights also play over the chapter's **key-art
background** (the four environment paintings from the manifest, embedded and
dimmed for readability); arena, raid, and trial pick a themed one. The **title
screen and the map/lobby** wear the key-art too — the map's backdrop follows how
far you've pushed the campaign.
`tools/fetch_portraits.mjs` can pull the full-resolution originals into
`web/prototype/art/` if you want them. It's the fastest bridge from "validated
spec" to "something you can hold."

## Run

Open `index.html` in any browser — no build, no server, no external requests.
Verified end-to-end in headless Chromium (loads clean, plays to a result, no
console errors).
