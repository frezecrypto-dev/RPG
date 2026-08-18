// End-to-end smoke test for the Ashgate API. Zero deps (uses global fetch).
//   node server/test.mjs
import { rmSync } from 'node:fs';

process.env.ASHGATE_NO_LISTEN = '1';
process.env.ASHGATE_DB = './server/.data/test-db.json';
process.env.ASHGATE_SECRET = 'test-secret';
try { rmSync('./server/.data/test-db.json', { force: true }); } catch {}

const { server } = await import('./index.js');
await new Promise((r) => server.listen(0, r));
const base = `http://localhost:${server.address().port}`;

let pass = 0, fail = 0;
const ok = (c, l) => { if (c) { pass++; } else { fail++; console.log('  FAIL:', l); } };
const call = async (method, path, { token, body } = {}) => {
  const res = await fetch(base + path, {
    method,
    headers: { 'content-type': 'application/json', ...(token ? { authorization: 'Bearer ' + token } : {}) },
    body: body ? JSON.stringify(body) : undefined,
  });
  return { status: res.status, json: await res.json().catch(() => ({})) };
};

// health
ok((await call('GET', '/health')).json.ok, 'health');

// two guest accounts
const a = (await call('POST', '/api/auth/guest')).json;
const b = (await call('POST', '/api/auth/guest')).json;
ok(a.token && a.player.id, 'guest A token');
ok(b.token && b.player.id && b.player.id !== a.player.id, 'guest B distinct');
ok(a.player.needsName === true, 'new account needs a name');

// name uniqueness
ok((await call('GET', '/api/name/check?name=FrezeLord')).json.available === true, 'name free before claim');
ok((await call('POST', '/api/name/claim', { token: a.token, body: { name: 'FrezeLord' } })).status === 200, 'A claims name');
ok((await call('GET', '/api/name/check?name=frezelord')).json.available === false, 'name taken (case-insensitive)');
const dup = await call('POST', '/api/name/claim', { token: b.token, body: { name: 'FrezeLord' } });
ok(dup.status === 409 && dup.json.reason === 'taken', 'B cannot take taken name (409)');
ok((await call('POST', '/api/name/claim', { token: b.token, body: { name: 'ab' } })).status === 400, 'reject short name');
ok((await call('POST', '/api/name/claim', { token: b.token, body: { name: 'Vowbound' } })).status === 200, 'B claims another name');
ok((await call('GET', '/api/me', { token: a.token })).json.player.name === 'FrezeLord', 'me reflects name');

// save sync + optimistic concurrency
const s1 = await call('PUT', '/api/save', { token: a.token, body: { save: { crystals: 1600, gold: 20000, owned: ['ASH-TNK-C01'], _accountCP: 4200 }, version: 0 } });
ok(s1.status === 200 && s1.json.version === 1, 'save v0->v1');
const got = await call('GET', '/api/save', { token: a.token });
ok(got.json.save.crystals === 1600 && got.json.version === 1, 'get save back');
const stale = await call('PUT', '/api/save', { token: a.token, body: { save: { crystals: 99 }, version: 0 } });
ok(stale.status === 409, 'stale write rejected (409 version conflict)');
const cheat = await call('PUT', '/api/save', { token: a.token, body: { save: { crystals: 9_999_999_999 }, version: 1 } });
ok(cheat.status === 422, 'impossible currency rejected (422)');

// leaderboard reflects server-derived CP from the save
await call('PUT', '/api/save', { token: b.token, body: { save: { _accountCP: 9000 }, version: 0 } });
const lb = await call('GET', '/api/leaderboard', { token: b.token });
ok(lb.json.top[0].cp >= lb.json.top[1].cp, 'leaderboard sorted desc');
ok(lb.json.top[0].name === 'Vowbound', 'higher CP ranks first');
ok(lb.json.me && lb.json.me.rank === 1, 'own rank reported');

// arena vs real opponents
const opp = await call('GET', '/api/arena/opponents', { token: a.token });
ok(Array.isArray(opp.json.opponents) && opp.json.opponents.length >= 1, 'arena opponents from real pool');
const ar = await call('POST', '/api/arena/result', { token: a.token, body: { opponentId: opp.json.opponents[0].id, win: true } });
ok(ar.json.ok && ar.json.rp > 0, 'arena win grants RP');

// guild
const g = await call('POST', '/api/guild/create', { token: a.token, body: { name: 'Ashen Wardens', tag: 'ASH' } });
ok(g.json.guild && g.json.guild.tag === 'ASH', 'guild created');
ok((await call('GET', '/api/guild/leaderboard')).json.guilds.length >= 1, 'guild leaderboard');

// auth required
ok((await call('GET', '/api/save')).status === 401, 'save requires auth');

await new Promise((r) => server.close(r));
console.log(`\n${pass} passed, ${fail} failed`);
try { rmSync('./server/.data/test-db.json', { force: true }); } catch {}
process.exit(fail ? 1 : 0);
