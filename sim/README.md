# ASHGATE Battle Sim & Balance Harness

Reference implementation of the combat model (doc 02) plus the Phase-0
auto-balance guardrails (doc 13, doc 14 s4). Pure Python, reads the live
data files under `data/`, deterministic under a fixed seed.

## Relationship to the canonical sim

The **shipping** battle sim is the engine-independent **C# library** shared
between the Unity client and the authoritative server (doc 12 s2) — that is
what validates battles for anti-cheat and drives co-op lockstep. This Python
sim is **not** that. It exists to:

1. run the balance guardrails here and in CI on every data change, and
2. serve as an executable spec the C# port is checked against (same data in,
   same win/loss and damage numbers out, within variance).

Keep the two in sync: a rule change lands in `data/` + this sim first, proves
out against the guardrails, then is ported to C#.

## Run

```bash
python3 -m sim.balance        # auto-balance report; exit 1 if a guardrail fails
python3 tools/build_content.py # schema/reference validation (separate, lighter)
```

`sim.balance` is the CI balance gate. `build_content.py` is the CI schema
gate. Both must exit 0.

## Guardrails (doc 04 s4, doc 14)

| ID | Claim | Ship-blocking |
|----|-------|:---:|
| G1 | maxed all-Common team (5*/L55/benchmark gear) clears STG-CAMP-3-10 | yes |
| G2 | maxed all-Rare team (6*/L60/benchmark gear) clears STG-CAMP-4-10 | yes |
| G3 | level-appropriate Epic team clears every chapter boss | ladder |
| G4 | a fresh under-geared team finds the finale a *real* fight (not trivial, not a wall) | yes |

`gear` is a single offense-budget multiplier standing in for the doc 09 s6.3
"F2P benchmark gear" — enough to answer "is the content clearable by the
rosters the docs promise", which is what a Phase-0 sweep needs. Per-slot gear
fidelity lives in the C# port.

## Modelling scope & known gaps

Faithful: SPD-ordered rounds, the s5 damage formula (DEF diminishing returns,
pierce, damage-type res, Holy-vs-Undead, crit, variance, DR, barriers, bleed
pierces barrier), shared Surge with manual-ult AI, cooldowns, the s8 status
taxonomy, DoT ticking, summons, telegraph windups + detonation patterns,
boss enrage and CC Resolve.

Simplified (documented, not silent): telegraphs fire probabilistically rather
than on a scripted timeline; phase transitions and per-boss scripted mechanics
(Vigil phase-lock, Annor-Vhol's three phases, Doorwright Wardgate) are modelled
as their damage/HP envelope, not their exact scripting; gear is a budget knob.

Unmodelled verbs (no-op, counted in `battle.unhandled`, safe to run): `copyStatus`,
`equalizeHp`, `extendStatus`, `sacrifice` — niche utility on Cantor Vhel,
Requiem, and Morgause. None sit in a guardrail roster; the C# port implements
them fully.

## Provenance note

The very first run of this harness found that enemy stats scaled geometrically
(`levelScaling` 1.065/level) while the documented player growth curve is
additive, diverging 7.7x by the finale and making chapters 3–4 unclearable by
any roster. The fix was content-side per doc 14 s4 rule 1 (never nerf players):
`levelScaling` retuned to 1.035 across all four enemy files, which tracks the
player curve, keeps the maxed-roster guardrails green, and leaves the finale a
~73% challenge for a fresh team. This is the harness doing its job.
