# Going live

Two independent pieces:

| Piece | What it is | Where it runs |
| --- | --- | --- |
| **Client** | `web/prototype/index.html`, wrapped into a real HTML page | GitHub Pages (static) |
| **API** | `/server` — accounts, unique names, cloud saves, leaderboards | Any Node/Docker host |

The client works **without** the API (offline, local saves). Deploy the client
first to have something playable, then add the API to unlock global names,
cloud saves and real leaderboards.

---

## 1. Client → GitHub Pages

The prototype is a *body fragment*: no `<html>`/`<head>`, so no viewport meta —
served raw, a phone renders it at desktop width. `tools/build-web.mjs` wraps it
into a proper document (viewport, title, theme colour) and injects the API URL.

```bash
node tools/build-web.mjs          # -> dist/index.html (offline build)
```

**One-time setup**

1. Push this branch to `main` (the workflow triggers on `main`).
2. Repo → **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Done. Every push that touches the client redeploys it.
   Run it now via **Actions → Deploy client to Pages → Run workflow**.

Your URL: `https://<user>.github.io/<repo>/` — for this repo,
`https://frezecrypto-dev.github.io/rpg/`.

> The page is ~16 MB because all art is embedded. It caches after first load,
> but first paint on mobile data is slow — moving art to a CDN (see
> `ONLINE_ARCHITECTURE.md` §7) is the fix when that starts to matter.

---

## 2. API → Render (or any Docker host)

`render.yaml` is a ready blueprint; `server/Dockerfile` works on any host
(Fly.io, Railway, a VPS).

1. [render.com](https://render.com) → **New → Blueprint** → pick this repo.
2. Render reads `render.yaml`, builds `server/Dockerfile`, and generates
   `ASHGATE_SECRET` for you.
3. Edit **`ASHGATE_ORIGIN`** to your exact Pages origin
   (`https://frezecrypto-dev.github.io`) — this locks CORS.
4. Deploy. Check `https://<service>.onrender.com/health` → `{"ok":true}`.

### Environment variables

| Var | Required | Purpose |
| --- | --- | --- |
| `ASHGATE_SECRET` | **yes** | Signs session tokens. The server **refuses to start** without it (a known secret lets anyone forge any login). Generate: `node -e "console.log(require('crypto').randomBytes(48).toString('base64url'))"` |
| `ASHGATE_ORIGIN` | strongly | Locks CORS to your client origin. Unset = open to every site (warns on boot). |
| `ASHGATE_DB` | no | Save-file path. Default `./server/.data/db.json`; the image uses `/data/db.json`. |
| `PORT` | no | Render/Fly set this automatically. |

### ⚠️ Free tier loses saves

Render free instances have **no persistent disk** — `/data` is wiped on every
deploy and restart, so cloud saves and claimed names disappear. For real
persistence switch `plan: free` → `plan: starter` in `render.yaml` and
uncomment the `disk:` block. (Long term: swap the JSON store for Postgres
behind `store.js`, per `ONLINE_ARCHITECTURE.md` §8.)

---

## 3. Connect the two

1. Repo → **Settings → Secrets and variables → Actions → Variables → New
   repository variable**
   - Name: `ASHGATE_SERVER`
   - Value: `https://<your-service>.onrender.com`
2. Re-run **Actions → Deploy client to Pages**.

The build bakes `window.ASHGATE_SERVER` into the page. On boot the client does
guest auth; the name modal then shows **"Online — this name is reserved
globally"** and Confirm is gated on the server (`409` → "name already taken").

Verify end-to-end:

```bash
curl -s https://<service>.onrender.com/health
# {"ok":true,...}
```

Then open the page, pick a name, and try the same name in a private window —
the second attempt must be rejected.

---

## 4. Before real players arrive

- [ ] `ASHGATE_SECRET` set (server enforces this) and never committed
- [ ] `ASHGATE_ORIGIN` locked to the client origin
- [ ] Persistent disk (or Postgres) — otherwise saves vanish on restart
- [ ] Backups of the save store
- [ ] Rate limiting in front of the API (Cloudflare, or a reverse proxy)
- [ ] `node server/test.mjs` green (23 assertions)

## Local full-stack run

```bash
ASHGATE_SECRET=dev-only ASHGATE_ORIGIN=http://localhost:8080 node server/index.js &
ASHGATE_SERVER=http://localhost:8787 node tools/build-web.mjs
cd dist && python3 -m http.server 8080     # open http://localhost:8080
```
