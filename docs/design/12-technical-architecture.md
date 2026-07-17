# 12 — Technical Architecture Recommendation

## 1. Engine & Client

- **Engine: Unity 2022 LTS+ (URP, 2D).** Reasons: 2D toolchain maturity, Spine/DragonBones integration for cut-in and idle animation, Addressables for content streaming, proven gacha-RPG track record, hiring pool. (Godot viable but weaker mobile live-ops ecosystem; Unreal wrong-sized for 2D.)
- Rendering: sprite/mesh 2D with URP 2D lights for rim/aura effects; VFX via particle prefab library keyed to the class color pairs (one VFX kit per class, tinted — not bespoke per character; doc 03 §3 makes this legal).
- Target spec: mid-range Android 2019+ (Snapdragon 665 / 3GB RAM) at 30fps battle, 60fps UI; iPhone 8+. Texture budget: character master atlases 2048², downscaled variants per device tier; battle memory budget 600MB.
- App size: ≤300MB install; chapters 2–4 art via Addressables CDN download (store-compliance friendly, patchable).

## 2. Backend

- **Authoritative server for everything that matters:** accounts, inventory, gacha rolls, stamina, rewards, co-op state. Client never computes a reward.
- Recommendation: managed backend stack (e.g. Nakama on managed infra, or custom Go/Node services on k8s) with: Auth, Player/Inventory, GachaService, BattleValidation, CoopLockstep (websocket rooms), GuildService, LiveOpsConfig, Mail/Notification.
- **Battle validation model:** battles run client-side from a **server-issued seed + server-known team/enemy data**; client submits the action log; server replays deterministically (same sim code compiled server-side — write the battle sim as a pure, engine-independent C# library shared between client and server). Cost: cheap. Benefit: near-total anti-cheat for PvE rewards.
- **Co-op:** server-relayed lockstep (doc 07 §2.2/2.5): server owns round checkpoints, timers, AI-takeover. 15s action timer makes latency tolerance trivial; no realtime netcode risk.

## 3. Account & Save Logic

- Account = server identity. Client stores only a session token + settings cache.
- Sign-in: guest → prompt binding (Apple/Google/email) at first meaningful investment (post first Epic pull — highest conversion moment). Cross-device via binding; iOS↔Android same account (store-policy-safe: purchases via platform, entitlements server-side).
- Offline: read-only roster browsing; all progression actions require connection (acceptable for this genre; removes an entire cheat/merge-conflict class).

## 4. Data-Driven Content (the live-ops backbone)

- ALL gameplay content — units, skills, enemies, stages, banners, shops, events, status effects — is **data, not code** (schemas in doc 15). Client ships a baked snapshot; server pushes versioned config bundles (JSON, signed, delta-patched).
- New banner/event/balance patch = config push + Addressables art bundle. **No app-store binary release for content.** Binary releases only for features/engine (~every 6–8 weeks).
- Config pipeline: Google-Sheets/CSV source of truth → validation CLI (schema check, ID lint, balance-guardrail checks like doc 04 §4) → JSON build → staging env → promote to prod. Every config version tagged + one-click rollback.

## 5. Localization Readiness

- Zero hardcoded strings; every string a key in locale tables (`loc/<lang>.json`), source language English. String keys follow content IDs (`unit.ASH-ASN-L01.name`).
- Fonts: TMP with fallback chains (Latin + CJK ready even if launch is EN-only). UI layouts tolerate +35% text expansion (German test) from day one.
- Dates/numbers/currency via ICU formatting; art contains no baked text (rule already in STYLE_NEGATIVE, doc 11).

## 6. Analytics Hooks (instrument at build time, not retrofitted)

Event taxonomy (client → analytics pipeline, e.g. Firebase + warehouse export):
- `session_start/end`, `stage_start/result` (stage id, team comp, rounds, manual/auto, stars), `pull` (banner, pity counter, result), `currency_delta` (every faucet/sink, tagged source), `upgrade_action`, `coop_segment` (party size, contribution, timeouts), `shop_view/purchase`, `funnel_ftue` (step-level).
Core dashboards from day one: FTUE funnel, D1/D7/D30, pull-income percentiles, stall-stage heatmap, currency faucet/sink balance, Expedition completion %.

## 7. Anti-Cheat / Anti-Exploit

- Server authority + deterministic replay validation (above) covers 90%.
- Additional: signed config (no local table tampering), server-side rate/pity state, receipt validation for IAP (server-to-store), anomaly detection on currency_delta outliers, replay spot-audits, device-integrity attestation (Play Integrity / App Attest) as a signal not a wall.
- Gacha rate integrity: CI simulation harness proving configured rates match published rates on every banner config (doc 08 §6) — protects against both bugs and store-compliance incidents.

## 8. Patchability & Live Ops Readiness

- Feature flags on every system (kill-switch for co-op, banners, events independently).
- Server-side maintenance mode with client-graceful messaging.
- Content calendar tooling: banners/events scheduled in config with start/end — no deploy at 5am for a banner rotation.
- Crash/ANR: Crashlytics + symbolicated native reports; performance budget CI (startup time, battle load time) per release.

## 9. Team-Shape Note (for the production plan, doc 13)

The architecture above is intentionally operable by a small team: one battle-sim engineer (pure C# lib), one backend engineer, two client engineers (UI + combat presentation), one tech-artist owning the VFX kit + Addressables pipeline, plus design/art/production. Nothing here requires an MMO-scale team.
