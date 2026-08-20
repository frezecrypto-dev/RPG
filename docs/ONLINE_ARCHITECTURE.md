# Project ASHGATE — Online Architecture

How the offline single-file prototype (`web/prototype/index.html`) becomes a
real online game with accounts, globally-unique names, cloud saves, and live
leaderboards / PvP / guilds. A **runnable backend scaffold** lives in
[`/server`](../server) — zero external dependencies, `node server/index.js`.

---

## 1. Where we are

- The prototype is **client-authoritative**: the entire game state lives in
  `localStorage` (`ashgate_save_v1`), and leaderboards / arena opponents / guild
  rivals are **simulated locally** from deterministic bot data.
- Usernames are checked only against a local reserved list — not globally unique.
- All art is **base64-embedded** in the one HTML file (~15.8 MB, at the 16 MB cap).

None of that is wrong for a prototype — but four things must move server-side to
ship online.

## 2. The four pillars

| Pillar | Today (offline) | Online target |
| --- | --- | --- |
| **Accounts** | device-only `ashgate_auth` flag | Guest + Google / Apple / Play Games, one durable account per person |
| **Identity** | local name check | globally-unique username (DB `UNIQUE` constraint) |
| **Save** | localStorage, trusted | server-authoritative sync, validated, conflict-safe |
| **Social** | simulated boards | real leaderboards, arena vs real players, guild sync |

## 3. Backend scaffold (`/server`)

Runnable now, dependency-free, file-backed store — the shape of the production
API without the ops:

```
server/
  index.js        HTTP API (Node http, no framework)
  auth.js         HMAC-signed session tokens; OAuth verification seam
  store.js        persistence interface (JSON file today → Postgres later)
  validate.js     server-authoritative save validation (anti-cheat seam)
  client-sdk.js   browser SDK: offline-first wrapper the game calls
  test.mjs        23-assertion end-to-end test  (node server/test.mjs)
```

Run it:

```bash
node server/index.js       # http://localhost:8787
node server/test.mjs       # 23 passed, 0 failed
```

### Endpoints

```
POST /api/auth/guest                      -> { token, player }
POST /api/auth/oauth {provider,idToken}   -> { token, player, needsName }
GET  /api/name/check?name=Foo             -> { available }
POST /api/name/claim {name}       (auth)  -> 200 | 409 {reason:'taken'}
GET  /api/me                      (auth)  -> { player }
GET  /api/save                    (auth)  -> { save, version }
PUT  /api/save {save,version}     (auth)  -> { ok, version } | 409 conflict | 422 invalid
GET  /api/leaderboard                     -> { top[100], me, total }
GET  /api/arena/opponents         (auth)  -> { opponents }  (real player pool)
POST /api/arena/result {...}      (auth)  -> { ok, rp, delta }
POST /api/guild/create {name,tag} (auth)  -> { guild }
GET  /api/guild/leaderboard               -> { guilds }
```

## 4. Accounts & unique usernames

- **Sign-in** issues a stateless HMAC session token (`auth.js`). Guest accounts
  are real rows so they can be upgraded to Google/Apple later by attaching a
  verified `providerSub`.
- **OAuth**: `verifyOAuth()` is a stub. Production verifies the provider
  `id_token` against Google/Apple JWKS and trusts only the verified `sub`.
- **Uniqueness**: the normalized (lowercased, trimmed) name is stored with a
  `UNIQUE` constraint. That constraint — not app code — is the real guarantee
  under concurrency. The client shows live "available?" feedback but the
  authoritative answer is the 200/409 from `POST /api/name/claim`.
- Client change: the username modal's Confirm gates on `claimName()` instead of
  the local `nameTaken()` check.

## 5. Server-authoritative saves

- The client stays **offline-first**: it writes `localStorage` instantly, and
  `client-sdk.pushSave()` debounces an authoritative `PUT /api/save`.
- **Optimistic concurrency**: each save carries a `version`; a stale write gets
  `409` with the newer server state (multi-device safety).
- **Anti-cheat** (`validate.js`): structural + bounds checks reject impossible
  currencies and out-of-cap hero states with `422`. **Combat Power is derived
  server-side**, never trusted from the client — extract the CP formula from the
  game into a shared isomorphic module so client and server compute it identically.
- Migration: `saveGame()`'s tail calls `pushSave(save)`; on login, `pullSave()`
  reconciles the newer of local vs cloud.

## 6. Leaderboards, Arena, Guilds

- **Power Ranking**: `setCp()` is fed by the *validated* save on every sync;
  `GET /api/leaderboard` returns the real top 100 + the caller's rank. The
  client keeps its bot-filled board only as an offline fallback.
- **Arena**: `arenaOpponents()` returns real players near your RP (bots fill a
  thin pool); `arenaResult()` moves RP for both sides. Production runs the fight
  against a **defense snapshot** of the opponent's team (async PvP), not live.
- **Guilds**: create/join + a renown league; production adds membership,
  Guild War scheduling, and boss-damage aggregation server-side.
- **Frames**: monthly ranking seasons close server-side and grant the exclusive
  #1–#10 frames from the real final standings.

## 7. Assets & the 16 MB cap

The single embedded file is at the artifact limit. For a real client, move
base64 art (`ART`, `CUT`, `EART`, `ECUT`, `STORYART`, `SKINART`, `FRAMEART`,
`NAVICON`, …) to a **CDN** and lazy-load by key. That alone drops the HTML to a
few hundred KB and unblocks unlimited future content — do this as part of the
online cutover, not before.

## 8. Production hardening (checklist)

- Postgres (or SQLite via `node:sqlite`) behind `store.js`; real transactions.
- `ASHGATE_SECRET` from a secret manager; rotate tokens.
- Rate limiting + per-account currency-delta anomaly checks.
- TLS termination, CORS locked to the game origin (scaffold allows `*`).
- Structured audit log of rejected/suspicious saves.
- Backups + GDPR delete/export for accounts.

## 8b. Client integration (done in the prototype)

The offline-first client is already wired into `web/prototype/index.html`
as the inlined `NET` object (a compact form of `client-sdk.js`):

- It stays **offline** unless a backend URL is provided via
  `window.ASHGATE_SERVER` or `localStorage['ashgate_server']`.
- On boot it calls `NET.init()` (guest auth). When online, the username
  modal gates **Confirm** on `NET.claimName()` — a server `409` shows
  "name already taken" — giving globally-unique names; offline it keeps
  the local reserved-name check. The modal shows an Online/Offline badge.
- `saveGame()` fires a debounced `NET.pushSave()`; `NET.pullSave()` and
  `NET.leaderboard()` are available for cloud-save reconciliation and the
  real Power Ranking once the server is live.

To activate: deploy `/server` (or a production API implementing the same
endpoints) and set `window.ASHGATE_SERVER` to its base URL.

## 9. Suggested cutover order

1. Stand up the API (Postgres, OAuth verify, TLS).
2. Client SDK for auth + **unique name claim** (smallest visible win).
3. Cloud save sync (offline-first) with conflict prompt.
4. Real Power Ranking, then async Arena, then Guilds.
5. Move art to CDN; shrink the client.
6. Season jobs (ranking resets, frame grants) on a scheduler.
