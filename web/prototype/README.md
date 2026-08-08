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

## Skill Dungeon & Insight (doc 09)

Skill levels no longer cost Gold — they cost **Insight** (📖), a dedicated
skill-essence currency you farm in the **Skill Dungeon** ("Rite of Insight",
reached from the 🗝️ Dungeons button on the home screen). Three difficulty tiers
(Apprentice / Adept / Master) scale the Warden foes up and pay out more Insight,
each flagged with a **recommended-power** check so you can see when you're
under-geared. Clears run on the full combat engine (Break, spotlight, tactical),
and the Insight you win is spent on S1/S2/S3 skill-ups in a hero's Kit.

The same hub holds four **Equipment Dungeons** — Forge of Edges (Weapon),
Drowned Reliquary (Necklace), Ossuary Vault (Bracelet), and Warden Signet
(Ring) — each with three tiers that scale the foes and drop **slot-specific
gear**: harder tiers drop higher gear tiers (T2 → T3 → T4) and better rarities,
and the piece rolls its main-stat and set just like a campaign drop. So each
accessory slot has a dedicated farm.

## Hero view & accessory slots

Tapping a hero in the Heroes' Hall opens a **full-size character sheet**: the
whole background-removed cut-out stands full-body in a rarity-framed panel next
to its **five equipment slots — Weapon, Necklace, Bracelet, Ring I, Ring II** —
each showing the equipped piece's rarity and set (or an empty slot), and tapping
one jumps straight into the gear screen filtered to that slot. Level, stars,
core stats, Gear Power, Ascension, and the skill kit sit below.

## Equipment (doc 09 s5)

The 5-slot gear system is live, not a placeholder multiplier. Each hero has
**Weapon / Necklace / Bracelet / Ring I / Ring II** slots; pieces roll a main
stat by slot, 1–4 substats by rarity (C/R/E/L), a tier (T1–T4), and one of six
sets. Enhancing to +5/+10/+15 rerolls a substat higher (the bounded-grind rule).
Gear stats feed the same `computeStats` the battle engine reads, so ATK%, HP%,
DEF, SPD, **crit rate/damage**, and **lifesteal** all change how fights play;
**Aegis 4-pc** grants a battle-start barrier and **Mending** boosts heals.

**Weapons are class-locked.** Every class wields its own weapon type — Dagger
(Assassin), Greatshield (Tank), Waraxe (Berserker), Staff (Mage), Grimoire
(Necro), Reliquary (Healer), Longbow (Ranger) — shown as a **class sign** on the
piece, and a hero can only equip its own type; a wrong-class weapon renders
🔒 class-locked. Accessories (necklace / bracelet / rings) stay universal, and
`canEquip()` enforces the rule in manual equip, auto-equip and loadout presets.

Pieces come only from **raid & dungeon drops** (bosses and gear dungeons — no
forge shortcut). **Auto-Equip** fills a hero from the bag, skipping wrong-class
weapons. Browsing a slot shows each candidate's **Gear-Power delta** (▲/▼) vs.
what's equipped; unwanted pieces **sell for Gold** individually or via a
**rarity-select quick-sell** (toggle C/R/E/L, one tap to clear all matching
unequipped pieces). Each hero also keeps **three saveable loadout presets** (doc
09) — snapshot the current gear, then swap builds in one tap; applying a preset
pulls its pieces back even if another hero borrowed them. Two set 4-pc effects
that aren't pure numbers in the doc (Vanguard/Gravebind) use a stat proxy here.

## Guild (doc 07)

A **Guild** system (bottom-bar 🛡️) simulates the co-op social layer. First you
**Create or Join**: a searchable **directory** of guilds (each with its own
crest, tag, member count, and Open/Request status) to join or request, or
**create your own** for a little Gold — pick a **name, a 3–4-letter tag, a
description, and a banner** (choose an emblem — wolf, dragon, skull, lion… — a
colour, and a shield/round/kite shape, rendered as a self-contained SVG crest
with a live preview). Create it and you're the **Leader**, with a **Manage** tab
to **broadcast** a message to all members, **re-style the banner**, and
**invite / kick** members.

Once in a guild, the hub has these tabs:
- **Chat** — member bubbles seeded and drip-fed for liveliness; you can type and
  send, and a guildmate replies. Persists.
- **Donate** — give Gold or Crystals (daily cap) for **Guild Marks** and guild
  XP that levels the guild, with a **roster leaderboard** ranked by weekly boss
  contribution.
- **Shop** — spend Guild Marks on Star Crates, Ash Relics, gear ore, and an Epic
  Vow ticket (weekly-limited, per doc 07 §3.2's "discount channel, not a power
  gate").
- **Guild Boss** — a weekly co-op boss (The Sunken Colossus) where **every
  member's damage stacks** toward a shared HP bar; you run it on the full combat
  engine (your damage adds to your weekly contribution), members contribute in
  parallel, and the **weekly Guild Chest unlocks only when the guild defeats the
  boss** — drives the shared bar to zero and the run shows "Boss defeated!" before
  the chest can be claimed. Solo-killing the boss in a single run also drops
  personal **boss loot** (gear) on top of your contribution.

## Weekly Boss Raid

The raid is now a **weekly** loop. A **rotating boss** cycles every 7 days through
a four-boss pool (Krul, Gorthaug, the Vaultwarden, Mortmain — each with its own
weakness for the Break system and its own battlefield), shown on a dedicated
**Weekly Raid** hub (bottom-bar *Raid*) with a live reset countdown. You bank a
**weekly best damage %**, and a **milestone reward rail** (20 / 40 / 60 / 80 /
100%) pays out Gold, Crystals, gear ore, Ash Relics, and Featured Vow tickets —
claimed by how far you got, and the track (and boss) **reset each week**, so
there's a fresh chase every week on top of the all-time best. **Boss loot (gear)
now drops only when you actually defeat the boss** — a partial run still pays
currency by damage %, but no kill means no gear, so the chase has a real prize.

## Co-op Raid (per-run)

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

## Login & Energy

The app opens on a **login screen** — the Vow Gate keyart with **Sign in with
Google / Apple** or **Continue as Guest** — the first thing a new player sees;
the choice is remembered device-side, so returning players skip straight in
(onboarding then runs once, after login).

An **Energy** system (⚡, doc 09 s6) gates battles so the game can't be cleared
in one sitting: campaign fights cost 6 (8 on Hard), dungeons and Gold/EXP raids
8, and the weekly/guild bosses 10; Arena stays free. Energy **regenerates 1 per
5 minutes** (with a live countdown in the header) and can be **refilled with
Crystals**; a low-Energy attempt offers that refill. It's shown in the home and
campaign headers and persists in the save.

## Commander level

The player has a **Commander level** (1 → **100**) shown as a pill with an XP bar
in the home header. **Everything you defeat grants XP** — campaign stages, raids,
dungeons, Arena, and the guild boss all feed it through the single victory path,
scaled by how many foes fell and whether it was a boss or Hard run. Each level-up
**raises your maximum Energy** (+5 per level, so the cap climbs from 120 toward
615 at Lv 100) and hands you the newly unlocked Energy for free, so pushing
content literally expands how much you can play. Level and XP persist in the save.

## In-app dialogs

All confirmations and notices use a built-in modal/toast instead of the browser's
native `confirm()`/`alert()` — those are blocked inside the sandboxed artifact
iframe, which is why sell / quick-sell / purchase buttons appeared to "do
nothing." Selling a hero, quick-selling gear, buying a shop pack, using a potion,
leaving a guild, and resetting all now pop a proper in-game dialog and confirm.

## Quests (daily / weekly / monthly)

A **📋 Quests** panel (home top-right, with a live claimable badge) tracks three
tiers that auto-reset on their own clock — **Daily** (midnight), **Weekly**, and
**Monthly** (rollovers detected on load and on every progress tick). Objectives
count real play: win battles, summon, clear dungeons, spend Energy, fight raids,
donate to your guild, claim daily logins. Progress bars fill live and a pulsing
**Claim** unlocks when a goal is met; rewards span Crystals, Gold, Insight,
Vow tickets, relics, **Energy** and **Energy Potions** — closing the Energy loop
so active players top themselves back up. Claimed state and progress persist per
period in the save.

## Inventory (satchel)

A **🎒 Bag** panel holds usable items and spare gear across two tabs. **Items**
lists consumables — **Energy Potion** (+40) and **Big Energy Potion** (+120) —
earned from quests and login rewards; **Use** restores Energy on the spot (and
is disabled at full). **Gear** shows every unequipped piece, rarity-sorted, with
a per-piece **sell for Gold** button (scrap-value, Legendary/Epic confirm) — a
lightweight sell-only view; equipping and enhancing still live on the hero.

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

## Difficulty & scaling (balance pass)

Enemies now **scale with their stage level**. Every campaign wave already encodes
an enemy level (`ENM-SLM-M02@8`), but the engine had been ignoring it — so a
maxed team steam-rolled everything. Enemy ATK/DEF/HP now grow ~4%/level (bosses
keep their hand-tuned base HP and scale only ATK/DEF, so they stay a *damage
race* rather than an HP sponge), and boss/dungeon fights get a longer round cap
(25) for that race. The result, verified by headless auto-battles: a geared,
ascended team clears the **Chapter-4 finale on Normal on the last round**, its
**Hard version resists even that team** (you need manual weakness-breaking or
more investment), an **under-geared team fails the finale outright**, while a
starter five still clears Chapter 1. Progression finally *demands* the gear and
skill farms — you can't march through the back half.

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

## Guided tutorial (Ivory)

New players are met by **Ivory, the Gate Guide** — a chibi mascot who pops in at
the bottom of the screen right after login and walks them through the whole game
in 15 steps. She **auto-navigates** to each area and **spotlights** the exact
button she's talking about: the Heroes' Hall and your two starter heroes, a
hero's Level/Star/Skill/Ascend upgrades, Equipment (equip, enhance, and how to
**sell/quick-sell** gear), the Bag, Shop, Quests, the Raid Portal, Guild, the
Commander level, and finally the Vow Gate — where she hands over the **free
guaranteed-Epic summon**. Skippable, and replayable any time from ⚙ Settings ▸
Replay guided tour. (The classic five-slide text primer is still there under
"How to play".) The guide art is a built-in chibi placeholder wired to a single
`GUIDEART` slot, so a custom illustration can be dropped in without touching the
tutorial logic.

### New-player start & first summons

A fresh account starts with **2 heroes** and **1,600 Crystals** (a full 10-pull).
The Vow Gate shows a glowing one-time **FREE Summon with a guaranteed Epic**, so
everyone lands a strong unit immediately, and the starting Crystals cover a
10-pull (which itself guarantees an Epic or better) — enough to field a party of
five out of the gate.

### Vow Tickets

**Vow Tickets** (🎟️) are premium summon tickets — **each one is a free single
summon** on the Featured Gate, with the same rates and pity as a Crystal pull.
They're earned from the Battle Pass, quests, weekly raids, and the guild shop
(reward tables that used to convert "tickets" into Crystals now grant real
tickets). A ticket count sits on the summon bar and a ticket-summon button
appears whenever you hold at least one.

## Settings

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

## Story — The World of Ash Gates

A dedicated **Story** screen (home ▸ 📖 Story) presents the campaign lore with the
uploaded key art: the Ash Gate world map, the world/faction intro (The Dark Order
vs. **The Vow**), dossier cards for the **Triarch** (Serin Vale, Lyra Ashenquill,
Kael Thorne) and the **Faces of the Dark Order** (Lady Vorena Ashfall, General
Darius Cinderhelm, the Dark Sovereign) plus the Order's creatures (Ashbound Titan,
Hollow Seraph) — each tappable for a full-art dossier with bio — and the three-act
arc (Embers in the Ash · Fractures in the Chain · Eclipse or Dawn). Character art
is embedded as compact WEBP; the large source PNGs are kept out of the build.
