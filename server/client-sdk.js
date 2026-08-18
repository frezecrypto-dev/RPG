// Ashgate client SDK — the seam between the single-file game and the online API.
//
// The prototype is offline-first (localStorage). This wrapper keeps that model:
// the game always reads/writes locally and instantly; the SDK syncs in the
// background and falls back to pure-offline when there is no network or the
// player is a guest who hasn't gone online yet.
//
// Integration into web/prototype/index.html (sketch):
//   1. Load this file (or inline it) before the game script.
//   2. On login: `await Ashgate.net.authGuest()` / `authOAuth(provider, idToken)`.
//   3. On the username modal: gate "Confirm" on `await Ashgate.net.claimName(name)`
//      (server 409 => show "name taken"), instead of the local-only check.
//   4. Replace `saveGame()`'s tail with `Ashgate.net.pushSave(saveObject)` — it
//      writes localStorage immediately and debounces an authoritative PUT.
//   5. Replace the simulated leaderboard/arena data with `Ashgate.net.leaderboard()`
//      and `Ashgate.net.arenaOpponents()`, keeping the current bot fallback when offline.

export function createClient(baseUrl, storage = globalThis.localStorage) {
  const TOKEN_KEY = 'ashgate_net_token';
  let token = storage?.getItem(TOKEN_KEY) || null;
  let saveVersion = Number(storage?.getItem('ashgate_net_ver') || 0);
  let pushTimer = null, online = false;

  const setToken = (t) => { token = t; try { storage?.setItem(TOKEN_KEY, t); } catch {} };

  async function api(method, path, body) {
    const res = await fetch(baseUrl + path, {
      method,
      headers: { 'content-type': 'application/json', ...(token ? { authorization: 'Bearer ' + token } : {}) },
      body: body ? JSON.stringify(body) : undefined,
    });
    const json = await res.json().catch(() => ({}));
    return { status: res.status, json };
  }

  return {
    isOnline: () => online,

    async authGuest() {
      try {
        const r = await api('POST', '/api/auth/guest');
        if (r.json.token) { setToken(r.json.token); online = true; return r.json.player; }
      } catch { online = false; }
      return null; // caller falls back to local-only guest
    },

    async authOAuth(provider, idToken) {
      try {
        const r = await api('POST', '/api/auth/oauth', { provider, idToken });
        if (r.json.token) { setToken(r.json.token); online = true; return r.json.player; }
      } catch { online = false; }
      return null;
    },

    // Returns {available} — use for live typing feedback.
    async nameAvailable(name) {
      try { return (await api('GET', '/api/name/check?name=' + encodeURIComponent(name))).json.available; }
      catch { return true; } // offline: allow, server re-checks on claim
    },

    // Returns {ok} or {ok:false, reason:'taken'|'length'|'chars'}.
    async claimName(name) {
      if (!online) return { ok: true, offline: true };
      try {
        const r = await api('POST', '/api/name/claim', { name });
        return r.status === 200 ? { ok: true } : { ok: false, reason: r.json.reason || 'error' };
      } catch { return { ok: true, offline: true }; }
    },

    // Instant local write + debounced authoritative sync with conflict handling.
    pushSave(saveObject) {
      try { storage?.setItem('ashgate_save_v1', JSON.stringify(saveObject)); } catch {}
      if (!online) return;
      clearTimeout(pushTimer);
      pushTimer = setTimeout(async () => {
        try {
          const r = await api('PUT', '/api/save', { save: saveObject, version: saveVersion });
          if (r.status === 200) { saveVersion = r.json.version; storage?.setItem('ashgate_net_ver', String(saveVersion)); }
          else if (r.status === 409) {
            // another device wrote first — adopt server state (last-writer strategy is naive;
            // production merges per-field or shows a device-conflict prompt).
            saveVersion = r.json.version; storage?.setItem('ashgate_net_ver', String(saveVersion));
          }
        } catch { /* stay offline, retry on next push */ }
      }, 1500);
    },

    async pullSave() {
      if (!online) return null;
      try {
        const r = await api('GET', '/api/save');
        if (r.json && r.json.save) { saveVersion = r.json.version; return r.json.save; }
      } catch {}
      return null;
    },

    async leaderboard() {
      try { return (await api('GET', '/api/leaderboard')).json; }
      catch { return null; } // caller keeps the local simulated board
    },

    async arenaOpponents() {
      try { return (await api('GET', '/api/arena/opponents')).json.opponents; }
      catch { return null; }
    },

    async arenaResult(opponentId, win) {
      try { return (await api('POST', '/api/arena/result', { opponentId, win })).json; }
      catch { return null; }
    },
  };
}
