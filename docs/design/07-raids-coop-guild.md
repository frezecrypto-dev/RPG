# 07 — Raids, Co-op Raid & Guild System

## 1. Farming Raids (solo, stamina-driven)

### 1.1 Raid categories (exactly three at launch — one per progression system)

| Raid | Drops | Feeds (doc 09) | Theme |
|---|---|---|---|
| **Starfall Depths** | Star Shards (class-tagged) + Starstone | Star upgrades | Collapsed observatory under the Gate |
| **The Foundry Below** | Gear, gear-enhance ore, set tokens | Equipment (5 slots) | Guardian weapon-forge still producing |
| **Ash Reliquary** | Ascension relics + class skill manuals | Ascension + skill levels | Vault of dead gods' remains |

Each raid: 4 difficulty tiers (T1 unlock ch.1-3 → T4 unlock ch.4-10), each tier a single 2-wave stage + mini-boss, tuned for ~60–90s autoplay at appropriate power.

### 1.2 Rotation & stamina logic
- All three raids open daily, but each day one raid is **"Surging" (+50% drops)** on a fixed weekly rotation (Mon/Thu = Starfall, Tue/Fri = Foundry, Wed/Sat = Reliquary, Sun = all Surging). Fixed rotation = plannable, no FOMO randomness.
- Cost: 12 Aether/run, no daily entry cap — **stamina is the only throttle** (single-throttle rule, doc 10 §1). Sweep (instant-clear at best score) unlocks per tier after a 3-star manual clear.

### 1.3 Anti-frustration reward logic (applies to raids AND boss repeats)
- **No empty runs:** every run drops baseline materials; rare drops (set tokens, high relics) use a **visible pity counter** — guaranteed at 10 runs, counter shown on the raid screen.
- **Selectable class-tag crates:** Star Shards drop as class-choice crates (player picks the class) — kills the "wrong-class shard" frustration entirely.
- **Overflow conversion:** maxed-material overflow auto-converts to Gold at a fair rate, never wasted.

## 2. Co-op Weekly Raid — "The Gatefall Expedition"

The flagship social mode. One colossal Gate entity is fought **across an entire week in daily segments**, in fixed teams of **2 or 4 players**.

### 2.1 Structure
- **Week cycle:** starts Monday 05:00 server, ends Sunday 23:59.
- **7 daily segments** (Seg 1–7), one unlocking per day. Each segment = one 5–8 minute co-op battle: Seg 1–2 outer horrors (adds + miniboss), Seg 3–6 the boss's four "Anchors" (each Anchor is a distinct mechanic check mapped to a class-verb: redirect, cleanse, armor-break, add-control), Seg 7 the **Heart** — the finale using all four mechanics.
- **Catch-up rule:** any unlocked-but-uncleared segment stays available all week; a day's segment takes ~50% longer if the previous one was skipped-then-stacked, but **nothing is permanently missable inside the week**. Full rewards require all 7 cleared by Sunday — pacing pressure without daily-login tyranny.
- **Expedition Lodge:** a party (2p or 4p) is formed once per week (guild board, friends, or matchmaking) and persists for the whole week. Members can be replaced only if they haven't cleared any segment yet (anti-abuse).

### 2.2 Combat model in co-op
Turn-based lockstep on a shared timeline: each player controls their **own 5-unit team**; player teams act in alternating unit-interleaved SPD order on the same field. Each player has their **own Surge bar**. Turn timer 15s per unit action (auto-resolves via that unit's AI on timeout — a lagging player slows nothing).

### 2.3 2-player vs 4-player scaling

| | 2-player | 4-player |
|---|---|---|
| Boss HP / segment | 1.0× baseline | 2.3× (not 2.0× — more coordination = slight efficiency demand) |
| Mechanic load | 2 simultaneous checks max | Up to 4 simultaneous checks (each Anchor tags a player) |
| Rewards | 100% | 110% (coordination premium, small enough that duos aren't punished) |

### 2.4 Contribution & anti-leech
- Per segment, each player must reach **60% of the party-average contribution score** (score = damage + healing×0.8 + shielding×0.8 + verb-completions like Cleansed-detonation ×flat bonus — supports score fairly by construction).
- Below threshold: that player gets segment rewards at 50% and a private warning; two failed segments in a week = removable by party vote even mid-week.
- AFK detection: 3 consecutive timeout-auto turns flags the segment as "assisted" for that player (50% segment reward). Full-auto is allowed *after* that player has manually cleared the same segment number in any previous week (earned convenience).

### 2.5 Reconnect / drop handling
- Lockstep state checkpointed server-side at each round boundary; reconnect resumes at current round with the AI having played the absent turns.
- If a player fully disconnects >3 rounds, remaining players may **finish with AI control** of the absent team; the absent player keeps rewards if their contribution was ≥60% before dropping (no punishment for real-life interruptions — anti-frustration).
- A segment can be retried unlimited times; retry restores the segment's starting state (no partial-damage banking within a segment — keeps segments tight and retryable).

### 2.6 Reward fairness
- All party members receive **identical clear rewards** per segment (contribution rules only gate leeching, never create winners/losers inside a party — cooperation pillar).
- Weekly full-clear (all 7 segments): **the gacha-material jackpot** — 10 Summon Ticket shards ×7 segments + full-clear bonus = **1 full multi-summon (10-pull ticket) per completed week**, plus Ascension relics and an exclusive cosmetic currency. This is the loop-closer: co-op play literally funds pulls (doc 01 §2).
- Score tiers (party total) add cosmetic-currency bonuses only — power rewards never scale with elite performance (anti-hardcore-gatekeeping).

### 2.7 Difficulty tiers
Three Expedition tiers (Breach I/II/III) selected at Lodge creation; higher tiers = same mechanics, higher checks, +Ascension relic quality. Tier recommendation shown from party power. Tier can be lowered mid-week (keeping progress), never raised (prevents reward sniping).

## 3. Guild System ("Wardens' Compact")

Purpose-built to support co-op; deliberately thin at launch.

### 3.1 Structure
- Create: 50,000 Gold, name + emblem (compose from generated emblem set). Join: open / apply / invite. Size: 30 members.
- **Roles:** Warden-Commander (1, full admin), Officer (up to 5: accept members, pin messages, schedule expeditions), Member.
- **Chat:** text channel + a structured **Expedition Board** — members post "LFG: Breach II, need Cleanse+Tank, evenings" cards; one tap forms/joins a Lodge. The board is the guild's real job; plain chat is secondary.

### 3.2 Guild participation benefits
- **Guild Marks** currency earned from: daily check-in, completing co-op segments with guildmates (×1.5 vs pug), guild weekly quest ("guild clears 60 segments").
- **Guild Shop:** rotating stock — star shard crates, Ascension relics, gear-enhance ore, an occasional Epic-selector fragment (slow-drip: ~1 selector per 10 weeks of full participation). No exclusive power; the shop is a *discount channel*, not a gate.
- **Guild Boons:** small QoL buffs bought by collective activity (e.g. +5% Gold from raids for 3 days). Never combat-power in co-op or bosses (keeps guilds optional-feeling for soloists while genuinely rewarding).

### 3.3 Weekly guild loop
```
Mon: expedition week opens → Board fills with Lodge posts
Daily: check-in, segment runs with guildmates, Marks accrue
Sat/Sun: full-clear push, officers nudge stragglers via Board pings
Sun night: guild weekly chest (Marks + cosmetic currency) based on total segments cleared — thresholds sized so ~60% participation maxes it (no 100%-attendance tyranny)
```

### 3.4 Explicitly deferred (post-launch)
Guild-vs-guild anything, guild bosses, guild territory, donation systems. Launch guilds do one thing well: **get people into weekly Lodges**.
