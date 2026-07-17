# 08 — Gacha System

Design goal: **commercially strong, fair by modern standards, zero dark patterns.** Published rates, visible pity counters, carryover, strong low rarities (doc 04 §1–2), and no gacha-exclusive gameplay verbs.

## 1. Banner Structure at Launch

| Banner | Contents | Availability | Currency |
|---|---|---|---|
| **Beginner's Vow** | 30-pull discounted track; guarantees 1 *selectable* Legendary from a curated set of 4 within 30 pulls | First 7 days of account, one-time | Discounted premium (~40% off) |
| **Standard Gate** | Full permanent pool (all 70 launch units) | Always | Vow Crystals or Standard Tickets |
| **Featured Gate** | Standard pool with 1 rate-up Legendary + 2 rate-up Epics | 2-week rotations | Vow Crystals or Featured Tickets |
| **Mercy Forge** (not a banner, but adjacent) | Direct crafting of any non-newest Legendary via Ember Sigils (dupes/pity byproduct) | Always | Ember Sigils (doc §5) |

Clarity rules: every banner screen shows — full rates table, pity counter (current/threshold), featured units' full kits playable in a **free trial stage**, and banner end date. No "step-up" ladders, no gamble-boxes, no limited-collab-vanish pressure at launch.

## 2. Rates by Rarity

| Rarity | Standard rate | Featured banner | Consolidated notes |
|---|---|---|---|
| Legendary | **3.0%** | 3.0% total — **50% chance it's the featured unit** | Industry-fair (higher than hostile 0.6–1% school; sustainable because dupes matter less here, see doc 09 §4) |
| Epic | **14.0%** | 14.0% — featured Epics take 40% of Epic hits | |
| Rare | **38.0%** | 38.0% | |
| Common | **45.0%** | 45.0% | Commons are real units with exclusive verbs (doc 04) — a Common hit is a shard-progress hit, not an insult |

10-pull guarantee: **at least 1 Epic-or-better per 10-pull** (slot-independent bonus roll if none occurred naturally).

## 3. Pity System

- **Soft pity:** from pull **51**, Legendary rate rises +6% per pull (3% → 9% → 15% …).
- **Hard pity:** guaranteed Legendary at pull **70**.
- **Featured 50/50 with carryover ("Vowkeeping"):** if a featured-banner Legendary hit is *not* the featured unit, the next Legendary on any featured banner **is guaranteed featured**. The 50/50-lost state **carries across banner rotations** (stored on account, shown in UI).
- **Pity counter carryover:** the pull counter itself carries between successive Featured Gates, and separately on Standard. Counters are always visible ("37/70").
- Expected cost math (for economy tuning, doc 10): worst-case featured Legendary = 140 pulls; average ≈ 62 pulls with soft pity. Monthly F2P income target ≈ 70–80 pulls (doc 10 §3) → an engaged F2P player gets ~1 featured Legendary per banner cycle on average, guaranteed at worst one per two cycles.

## 4. Beginner Experience

- Tutorial summon: scripted first 10-pull, guarantees an Epic DPS (from a curated trio) — pull fantasy delivered in minute 3 (doc 01 §3).
- Beginner's Vow banner (above): guarantees a **chosen** Legendary ≤30 pulls — the modern "pick your carry" standard.
- New accounts get 20 free Standard pulls across the 7-day login track (doc 10 §4).

## 5. Duplicate Handling

- Duplicate → converts to that unit's **Soul Shards** (star/awakening fuel, doc 09 §4) + **Ember Sigils** (universal pity-dust).
- Ember Sigil rates: Common dupe = 1, Rare = 5, Epic = 40, Legendary = 300.
- **Mercy Forge:** 1,500 Ember Sigils = any Legendary older than 2 banner cycles; 300 = any Epic. This is the hard cap on worst-case luck: *every* pull permanently advances collection.
- Legendary Soul Shards are additionally farmable in tiny weekly quantities via Expedition full-clears (doc 07 §2.6) — dupe progression is never gacha-exclusive.

## 6. Anti-Frustration & Fairness Checklist (ship-blocking requirements)

- [ ] All rates published in-game, per banner, per unit.
- [ ] Pity + 50/50 state visible at all times; survives app reinstall (server-side).
- [ ] No time-limited units that never return: featured Legendaries enter Standard pool + Mercy Forge after 2 cycles.
- [ ] Trial stages for every featured unit before spending.
- [ ] Spending confirm on every real-money purchase; daily premium-purchase soft-cap warning (self-regulation UX); parental controls honor platform settings.
- [ ] No rate manipulation per-account, ever (also a legal/store-compliance issue).
- [ ] Drop simulation harness in CI validates published rates == configured rates on every banner config change (doc 12 §7).

## 7. Example Banner Config (data shape — full schema in doc 15)

```json
{
  "bannerId": "BNR-FEAT-2026-W3",
  "type": "featured",
  "start": "2026-11-02T05:00:00Z", "end": "2026-11-16T04:59:59Z",
  "pool": "standard_v1",
  "featured": { "legendary": ["ASH-BSK-L02"], "epic": ["ASH-BSK-E01", "ASH-HLR-E02"] },
  "rates": { "legendary": 0.03, "epic": 0.14, "rare": 0.38, "common": 0.45 },
  "featuredShare": { "legendary": 0.5, "epic": 0.4 },
  "pity": { "soft": { "from": 51, "step": 0.06 }, "hard": 70, "carryGroup": "featured" },
  "tenPullFloor": "epic",
  "costs": { "single": { "vowCrystal": 150 }, "ten": { "vowCrystal": 1500 }, "ticket": "TKT-FEAT" }
}
```
