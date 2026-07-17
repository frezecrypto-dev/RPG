# 16 — Home Screen / Main Hub UX

## 1. Layout (portrait, one-thumb reachable)

```
┌──────────────────────────────────────┐
│ TOP BAR: [Avatar/Lv] [Gold] [Vow Crystals] [Aether ▮▮▮ +] [Settings]│
├──────────────────────────────────────┤
│ EVENT/BANNER CAROUSEL (auto-rotating, max 3 cards:        │
│  current Featured Gate · active event · battle pass promo)│
├──────────────────────────────────────┤
│                                      │
│   HUB SCENE: chapter key art of the  │
│   player's current campaign chapter  │
│   (living background, doc 11 env art)│
│   Featured hero idle (player-chosen  │
│   "Vanguard" unit with idle anim)    │
│                                      │
│  Floating contextual chip: "Continue │
│  2-7" or "Expedition segment ready!" │
├──────────────────────────────────────┤
│ SIDE RAIL (right, collapsible):      │
│  [Mail] [Quests] [Codex] [Friends]   │
├──────────────────────────────────────┤
│ BOTTOM NAV (5 fixed):                │
│ [Heroes] [Summon] [⚔ BATTLE] [Guild] [Shop] │
└──────────────────────────────────────┘
```

## 2. Navigation Model

- **BATTLE (center, largest)** opens the mode select: **Campaign · Raids · Bosses · Expedition (co-op)** as four large thematic cards with live state ("Surging today: Foundry +50%", "Boss attempts 2/3", "Segment 4/7 ready"). One tap deep = every core activity (≤2 taps to any gameplay, hard UX rule).
- **Heroes:** roster grid → unit page (stats/skills/gear/star/ascend tabs) → team presets.
- **Summon:** the Gacha Tower scene — banner tabs (Beginner/Featured/Standard), pity counters always on screen, Mercy Forge entry, trial-stage buttons.
- **Guild:** guild home + Expedition Board (doc 07 §3) + guild shop. Badge-dot when the Board has open Lodges matching your saved role tags.
- **Shop:** tabs — Value (monthly card/pass) · Crystals · Cosmetics · Guild/Gleam exchange. No shop popups on login, ever (one interstitial max per day, only for genuinely new offers — trust posture, doc 10).
- **Side rail** handles the "inbox layer": Mail (rewards), Quests (daily/weekly/Path), Codex, Friends. Red-dot discipline: dots only for claimable value, never for "go look at a thing" (dot fatigue kills trust in dots).

## 3. State & Flow Rules

- The contextual chip is the **single smart CTA**: priority = unclaimed Expedition segment > continue campaign > daily quests near-complete > Surging raid. One suggestion at a time — the hub tells you *the* next thing, not everything.
- Top-bar currencies tap-through to their source screens ( Aether "+" → refresh sheet with today's cap state).
- Event banners come from LiveOps config (doc 12 §8) — art slot + deep-link, no client release per event.
- First-week FTUE progressively reveals nav: only BATTLE + Summon visible day one; Heroes appears with first pull; Guild appears at ch.2-3 unlock (doc 06 §1) — an empty locked button row is demoralizing, a growing hub feels like progress.
