# ASHGATE — Playable Combat Slice

A single-file, self-contained browser prototype of one boss fight — **five
Vowbound vs. Krul, the Mother-Mass** (Chapter 1 finale). It turns the spec into
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

## Faithful data

Hero stats, skill kits, and enemy stats are extracted from the real
`data/` + `content/` tables via `sim/ashsim.py` (the same numbers the balance
harness uses). The combat math mirrors `sim/ashsim.deal_damage`.

**One deliberate exception:** the demo Krul is scaled (HP ×3.2, ATK ×1.25) for
showcase *pacing* — long enough to see Surge fill and a telegraph fire. That is
a demo knob, not campaign balance; the real tuning lives in the data + sim.

## Scope / honesty

This is a **combat vertical slice**, not the game. No gacha, roster, progression,
backend, audio, or the other 39 stages — those are specified in `docs/` and
`data/` but not built. Class art is CSS/emoji placeholders (the AI art canon in
`art/canon-manifest.json` isn't integrated). It's the fastest bridge from
"validated spec" to "something you can hold."

## Run

Open `index.html` in any browser — no build, no server, no external requests.
Verified end-to-end in headless Chromium (loads clean, plays to a result, no
console errors).
