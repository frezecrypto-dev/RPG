# 01 — Game Pillars & Core Loop

## 1. Game Pillars

Every feature must serve at least one pillar. A feature that serves none gets cut.

### Pillar 1 — "Power you can read"
Dark power-fantasy where strength is *legible*. When a Legendary Berserker ults, the screen tells you it matters — but a well-built Rare unit visibly carrying a fight must also be a designed moment, not an accident. Readability beats spectacle: every effect must be parseable on a 6-inch screen in sunlight.

### Pillar 2 — "The squad is the hero"
No single unit wins alone. All content is tuned around 5-unit composition: frontline pressure, damage, sustain, and utility are all check-boxes the encounter design actively tests. Team-building is the core skill expression, not reflexes.

### Pillar 3 — "Every pull has a job"
No dead pulls. Commons and Rares carry unique utility that Legendaries don't replace (see doc 04, §2). Duplicates always convert into progression. The gacha is a collection engine, not a trash generator.

### Pillar 4 — "Respect the 6 minutes"
The core session is 5–8 minutes. Every daily-loop activity must be completable inside three such sessions. Long-form content (co-op raid) is split into daily segments precisely so it never demands a long sitting.

### Pillar 5 — "Fair by design, profitable by desire"
Monetization sells *acceleration and identity* (speed, cosmetics, collection), never *exclusive power gates*. Hard pity, published rates, and farmable viability for F2P are non-negotiable (doc 08, doc 10).

## 2. Core Loop (moment-to-moment → session → week)

### Battle loop (~90 seconds per stage)
```
Pick stage → auto-suggested or manual team → combat (semi-auto, manual ultimates)
→ result screen (loot, stars, XP) → immediate "next stage / repeat" affordance
```

### Session loop (5–8 min, 2–3× daily)
```
Login → collect idle/mail rewards → spend Aether (stamina) on:
   campaign push OR raid farm OR boss attempt
→ do daily co-op raid segment (if in guild pair/squad)
→ 1–2 upgrade actions (level, gear, star) → check summon currency → maybe pull
→ daily quest claim → out
```

### Weekly loop
```
Mon: co-op raid week starts (7 daily segments)
Daily: raids rotate materials (doc 07 §1.2)
Weekly: boss reset, guild activity chest, shop refresh, event banner cadence
Sun: co-op raid final segment + full-clear bonus claim
```

### Meta loop (the "why I keep playing")
```
Summon heroes → build/upgrade them → clear harder content
→ harder content drops better materials + gacha currency
→ new banners introduce new team puzzles → repeat
```
The loop is closed: **content produces gacha material** (notably the weekly co-op raid, doc 07 §2.7), so playing well literally generates pulls.

## 3. Session Design Rules

- **First-time user:** reach first summon within 3 minutes of app open; first Epic guaranteed in tutorial summon; first full 5-unit party by stage 1-3.
- **Interrupt-safe:** every activity ≤ 3 min per atomic step; combat can be backgrounded and resumed (client-authoritative replay of committed seed, doc 12 §6).
- **No forced waiting mid-session:** stamina gates *volume*, never a timer mid-activity.
- **Autoplay unlock:** stage auto-repeat unlocks after first 3-star clear of a stage — manual first, convenience after mastery.

## 4. Player Fantasy Statement (for all content/art decisions)

> "I command a squad of beautifully dangerous people who are barely holding back something worse than death — and every week we get strong enough to go one gate deeper."

Marketing, splash art, boss design, and event copy all point at this sentence.
