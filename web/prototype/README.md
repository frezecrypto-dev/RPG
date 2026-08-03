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
Gold** (single or bulk "Scrap Commons"). Two set 4-pc effects that aren't pure
numbers in the doc (Vanguard/Gravebind) use a stat proxy here.

## Scope / honesty

This is a **playable slice**, not the game. It now covers the core loop —
summon → equip/upgrade → team-build → multi-wave combat across the full
four-chapter campaign (Slimes, Giants, Guardians, Undead — each family flips the
damage-type puzzle, and the finale boss reknits once at the Gate) → farm →
persist — but not the backend, PvP/co-op, hard mode, or the remaining 20 stages
of the 40-stage design, which are specified in `docs/` and `data/` but not
built. Class art is CSS/emoji
placeholders (the AI art canon in `art/canon-manifest.json` isn't integrated).
It's the fastest bridge from "validated spec" to "something you can hold."

## Run

Open `index.html` in any browser — no build, no server, no external requests.
Verified end-to-end in headless Chromium (loads clean, plays to a result, no
console errors).
