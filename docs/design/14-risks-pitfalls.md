# 14 — Risks, Balance Pitfalls & What to Avoid

## 1. Design/Balance Risks

| Risk | Why it kills games like this | Mitigation (already wired into docs) |
|---|---|---|
| **Legendary-only meta** | Gacha feels punitive; low-rarity pulls feel like losses; F2P churns | Exclusive verbs on C/R units, utility doesn't scale with rarity, cost-efficiency curve, encounter verb-checks (docs 04, 05) — *audit every new unit against the verb table* |
| **Power creep spiral** | Each banner must outsell the last → stats inflate → old content trivial → old units dead | Uniform kit structure + standardized tokens (doc 02 §8) caps design surface; new units add *new synergy axes*, not bigger numbers; quarterly power-curve audit vs. launch Legendaries |
| **Speed-stat tyranny** | In turn games SPD becomes the only stat; gear RNG on SPD becomes the whole endgame | Round-start-only re-sorting, team-shared Surge (tempo isn't hoarded per-unit), SPD confined to Charm slot with bounded substat rerolls |
| **Heal/stall degeneracy** | Infinite-sustain teams trivialize content and stretch battle time | 20-round cap, boss enrage, Decay/anti-heal tools, 1-revive-per-battle cap |
| **CC-lock degeneracy** | Stun-chains delete boss design | Resolve rule (CC-immunity window after any hard CC) |
| **Economy faucet drift** | Event-by-event generosity creep silently doubles pull income → revenue collapse | Single owned number: 75 pulls/month F2P budget (doc 10 §2); every event's grants debited against it in the content calendar sheet |
| **Currency bloat** | Each feature team adds a currency → players stop understanding value | Hard cap ≤8 + swap-only rule (doc 10 §1) |
| **Co-op leech/toxicity** | Weekly-locked group content + strangers = rage-quits and churn | Contribution floor w/ support-fair scoring, AI-takeover, identical rewards, retry-friendly segments, tier-lowering (doc 07 §2) |
| **FTUE overload** | 10 systems in hour one → uninstall | Unlock schedule tied to chapter progress (doc 06 §1); one new system per 20–30 min |

## 2. Production Risks

- **AI-art consistency drift** is the #1 production risk for this project. Mitigations: locked prompt blocks, canonical refs, class-batch generation, monthly contact-sheet audits (doc 11 §3). *Never* let individual contributors freestyle prompts into shipped assets.
- **70 characters is a content cliff.** The uniform 4-skill structure + shared VFX kits per class + standardized tokens exist to make 70 kits a data-entry problem, not 70 bespoke engineering problems. Guard that boundary: a designer asking for "just one custom mechanic" per unit re-creates the cliff.
- **Co-op is the riskiest engineering line item.** That's why it's lockstep-turn-based with 15s timers and AI takeover — no realtime netcode. If Phase 2 slips, ship 2p-only first; 4p is additive.
- **Balancing without simulation = launch disaster.** The headless sim (doc 13 Phase 0) is not optional; the guardrail suite (all-Common clears 3-10, F2P 90-day curve) runs in CI on every data change.

## 3. Compliance / Store Risks

- Gacha odds disclosure: required by Apple/Google — the CI rate-verification harness doubles as the compliance artifact.
- Regional gacha law (JP/CN/KR/BE/NL): no complete-gacha ("kompu") mechanics anywhere; loot-boxed IAP already banned by our own monetization policy; keep legal review before entering regulated markets.
- Ratings: dark fantasy imagery — target 12+/Teen; art checklist adds "no gore, wounds stylized as light/energy" rule.
- IP distance: original names/world audited against Solo Leveling terms (no "hunters", "gates" → we use *Ashgates/Gatewardens* — verify trademark clearance on final title before marketing spend).

## 4. What NOT to Do (standing orders)

1. Do not nerf player-owned units to fix content; fix content or buff alternatives (nerfs only for genuine exploits, with compensation).
2. Do not sell power directly, ever — the first exception destroys the positioning permanently (doc 10 §4).
3. Do not add a second stamina-like throttle.
4. Do not ship a boss without its counterplay-matrix rows filled (doc 05 §3).
5. Do not add mechanics via skill-level-ups (stability rule, doc 02 §4).
6. Do not create limited-forever units.
7. Do not let the event calendar outrun banked content — 8 weeks of buffer, always (doc 13).
