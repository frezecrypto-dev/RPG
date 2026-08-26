// Ashgate online — API server (zero external dependencies).
//
//   node server/index.js        # starts on :8787
//   PORT=9000 node server/index.js
//
// Endpoints (all JSON):
//   POST /api/auth/guest                       -> { token, player }
//   POST /api/auth/oauth {provider,idToken}    -> { token, player, needsName }
//   GET  /api/me                       (auth)  -> { player }
//   GET  /api/name/check?name=Foo              -> { available }
//   POST /api/name/claim {name}        (auth)  -> { ok } | 409 {reason}
//   GET  /api/save                     (auth)  -> { save, version }
//   PUT  /api/save {save,version}      (auth)  -> { ok, version } | 409 conflict
//   POST /api/leaderboard/cp {cp}      (auth)  -> { ok }
//   GET  /api/leaderboard                      -> { top, me, total }
//   GET  /api/arena/opponents          (auth)  -> { opponents }
//   POST /api/arena/result {opponentId,win}(a) -> { ok, rp, delta }
//   POST /api/guild/create {name,tag}  (auth)  -> { guild }
//   GET  /api/guild/leaderboard                -> { guilds }
//   GET  /health                               -> { ok }

import { createServer } from 'node:http';
import { Store, normalizeName } from './store.js';
import { signToken, verifyToken, verifyOAuth } from './auth.js';
import { validateSave } from './validate.js';

const PORT = process.env.PORT || 8787;
// Lock CORS to the game's origin in production; '*' stays the local-dev default.
const ORIGIN = process.env.ASHGATE_ORIGIN || '*';
const store = new Store();

const json = (res, code, obj) => {
  const body = JSON.stringify(obj);
  res.writeHead(code, {
    'content-type': 'application/json',
    'access-control-allow-origin': ORIGIN,
    ...(ORIGIN === '*' ? {} : { vary: 'Origin' }),
    'access-control-allow-headers': 'authorization,content-type',
    'access-control-allow-methods': 'GET,POST,PUT,OPTIONS',
  });
  res.end(body);
};

function readBody(req) {
  return new Promise((resolve) => {
    let data = '';
    req.on('data', (c) => { data += c; if (data.length > 1_500_000) req.destroy(); });
    req.on('end', () => { try { resolve(data ? JSON.parse(data) : {}); } catch { resolve({}); } });
    req.on('error', () => resolve({}));
  });
}

function authed(req) {
  const h = req.headers['authorization'] || '';
  const token = h.startsWith('Bearer ') ? h.slice(7) : null;
  const payload = verifyToken(token);
  return payload ? payload.sub : null;
}

const publicPlayer = (p) => p && ({ id: p.id, name: p.name, cp: p.cp, arenaRp: p.arenaRp, guildId: p.guildId, needsName: !p.name });

const server = createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);
  const path = url.pathname;
  const method = req.method;

  if (method === 'OPTIONS') return json(res, 204, {});
  if (path === '/health') return json(res, 200, { ok: true, time: Date.now() });

  try {
    // ---- auth ----
    if (path === '/api/auth/guest' && method === 'POST') {
      const p = await store.createPlayer({ provider: 'guest' });
      return json(res, 200, { token: signToken(p.id), player: publicPlayer(p) });
    }
    if (path === '/api/auth/oauth' && method === 'POST') {
      const { provider, idToken } = await readBody(req);
      const v = await verifyOAuth(provider, idToken);
      if (!v) return json(res, 401, { error: 'invalid_oauth' });
      const p = await store.createPlayer(v);
      return json(res, 200, { token: signToken(p.id), player: publicPlayer(p), needsName: !p.name });
    }

    // ---- name (uniqueness) ----
    if (path === '/api/name/check' && method === 'GET') {
      const available = await store.nameAvailable(url.searchParams.get('name') || '');
      return json(res, 200, { available });
    }

    // ---- everything below needs a valid session ----
    const pid = authed(req);

    if (path === '/api/me' && method === 'GET') {
      if (!pid) return json(res, 401, { error: 'unauthorized' });
      return json(res, 200, { player: publicPlayer(await store.getPlayer(pid)) });
    }

    if (path === '/api/name/claim' && method === 'POST') {
      if (!pid) return json(res, 401, { error: 'unauthorized' });
      const { name } = await readBody(req);
      const r = await store.claimName(pid, name);
      if (!r.ok) return json(res, r.reason === 'taken' ? 409 : 400, r);
      return json(res, 200, r);
    }

    if (path === '/api/save' && method === 'GET') {
      if (!pid) return json(res, 401, { error: 'unauthorized' });
      return json(res, 200, (await store.getSave(pid)) || { save: null, version: 0 });
    }
    if (path === '/api/save' && method === 'PUT') {
      if (!pid) return json(res, 401, { error: 'unauthorized' });
      const { save, version } = await readBody(req);
      const check = validateSave(save);
      if (!check.ok) return json(res, 422, { error: 'invalid_save', detail: check.reason });
      const r = await store.putSave(pid, save, version);
      if (!r.ok && r.reason === 'version_conflict') return json(res, 409, r);
      if (!r.ok) return json(res, 400, r);
      // derive the leaderboard CP from the validated save (server-authoritative)
      if (typeof check.cp === 'number') await store.setCp(pid, check.cp);
      return json(res, 200, r);
    }

    // ---- leaderboard ----
    if (path === '/api/leaderboard/cp' && method === 'POST') {
      if (!pid) return json(res, 401, { error: 'unauthorized' });
      const { cp } = await readBody(req);
      await store.setCp(pid, cp);
      return json(res, 200, { ok: true });
    }
    if (path === '/api/leaderboard' && method === 'GET') {
      return json(res, 200, await store.leaderboard(pid, 100));
    }

    // ---- arena ----
    if (path === '/api/arena/opponents' && method === 'GET') {
      if (!pid) return json(res, 401, { error: 'unauthorized' });
      return json(res, 200, { opponents: await store.arenaOpponents(pid, 3) });
    }
    if (path === '/api/arena/result' && method === 'POST') {
      if (!pid) return json(res, 401, { error: 'unauthorized' });
      const { opponentId, win } = await readBody(req);
      return json(res, 200, await store.arenaResult(pid, opponentId, !!win));
    }

    // ---- guild ----
    if (path === '/api/guild/create' && method === 'POST') {
      if (!pid) return json(res, 401, { error: 'unauthorized' });
      const { name, tag } = await readBody(req);
      return json(res, 200, { guild: await store.createGuild(pid, name, tag) });
    }
    if (path === '/api/guild/leaderboard' && method === 'GET') {
      return json(res, 200, { guilds: await store.guildLeaderboard(50) });
    }

    return json(res, 404, { error: 'not_found', path });
  } catch (e) {
    console.error('[api]', e);
    return json(res, 500, { error: 'server_error' });
  }
});

// Don't listen when imported by the test harness.
if (process.env.ASHGATE_NO_LISTEN !== '1') {
  // Session tokens are HMAC-signed: shipping the dev secret lets anyone forge a
  // login for any account. Fail loudly instead of starting an insecure server.
  if (!process.env.ASHGATE_SECRET && process.env.ASHGATE_ALLOW_DEV_SECRET !== '1') {
    console.error('[ashgate] FATAL: ASHGATE_SECRET is not set.\n' +
      '  Generate one:  node -e "console.log(require(\'crypto\').randomBytes(48).toString(\'base64url\'))"\n' +
      '  For local dev only, set ASHGATE_ALLOW_DEV_SECRET=1 to bypass this check.');
    process.exit(1);
  }
  if (ORIGIN === '*') console.warn('[ashgate] WARNING: ASHGATE_ORIGIN unset — CORS is open to any origin.');
  server.listen(PORT, () => console.log(`[ashgate] api listening on http://localhost:${PORT}`));
}

export { server, store };
