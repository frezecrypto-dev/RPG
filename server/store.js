// Ashgate online — persistence layer.
//
// This scaffold uses a single JSON file so the server runs with ZERO external
// dependencies (`node server/index.js` just works). The API below is the seam:
// swap this module for a Postgres/SQLite-backed one in production without
// touching the route handlers. Every method is async so that swap is trivial.
//
// Tables (conceptual):
//   players(id, provider, providerSub, name, nameKey UNIQUE, cp, save JSON,
//           saveVersion, arenaRp, guildId, createdAt, updatedAt)
//   names(nameKey UNIQUE) -> enforced here via a lookup map
//   guilds(id, name, tag, leaderId, renown, members[])
//
// Production notes:
//   - `nameKey` is the normalized (lowercased, trimmed) name and carries a
//     UNIQUE constraint — that constraint is what actually guarantees global
//     username uniqueness under concurrency. Here we emulate it with a Map +
//     a serialized write queue.
//   - Replace saveToDisk() debounce with real transactions.

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';

const DEFAULT_PATH = process.env.ASHGATE_DB || './server/.data/db.json';

function nowISO() { return new Date().toISOString(); }
export function normalizeName(name) { return String(name || '').trim().toLowerCase(); }

export class Store {
  constructor(path = DEFAULT_PATH) {
    this.path = path;
    this.db = { players: {}, names: {}, guilds: {}, seq: 0 };
    this._dirty = false;
    this._timer = null;
    this._load();
  }

  _load() {
    try {
      if (existsSync(this.path)) {
        this.db = JSON.parse(readFileSync(this.path, 'utf8'));
        this.db.players ||= {}; this.db.names ||= {}; this.db.guilds ||= {}; this.db.seq ||= 0;
      }
    } catch (e) { console.error('[store] load failed, starting fresh:', e.message); }
  }

  // Debounced persistence. In production this is one DB transaction per write.
  _save() {
    this._dirty = true;
    if (this._timer) return;
    this._timer = setTimeout(() => {
      this._timer = null;
      if (!this._dirty) return;
      this._dirty = false;
      try {
        mkdirSync(dirname(this.path), { recursive: true });
        writeFileSync(this.path, JSON.stringify(this.db));
      } catch (e) { console.error('[store] save failed:', e.message); }
    }, 120);
  }

  _id(prefix) { this.db.seq += 1; return `${prefix}_${Date.now().toString(36)}${this.db.seq.toString(36)}`; }

  // ---- players ----
  async createPlayer({ provider = 'guest', providerSub = null } = {}) {
    // Returning provider users log back into the same account.
    if (providerSub) {
      const existing = Object.values(this.db.players).find(p => p.provider === provider && p.providerSub === providerSub);
      if (existing) return existing;
    }
    const id = this._id('p');
    const p = {
      id, provider, providerSub, name: null, nameKey: null,
      cp: 0, arenaRp: 0, guildId: null,
      save: null, saveVersion: 0,
      createdAt: nowISO(), updatedAt: nowISO(),
    };
    this.db.players[id] = p; this._save();
    return p;
  }

  async getPlayer(id) { return this.db.players[id] || null; }

  // Atomic-ish username claim. Rejects if the normalized name is taken by
  // anyone else. This is the client-facing guarantee of global uniqueness.
  async claimName(playerId, name) {
    const key = normalizeName(name);
    if (key.length < 3 || key.length > 16) return { ok: false, reason: 'length' };
    if (!/^[a-z0-9 _-]+$/.test(key)) return { ok: false, reason: 'chars' };
    const owner = this.db.names[key];
    if (owner && owner !== playerId) return { ok: false, reason: 'taken' };
    const p = this.db.players[playerId];
    if (!p) return { ok: false, reason: 'no_player' };
    // release the player's previous name, if any
    if (p.nameKey && this.db.names[p.nameKey] === playerId) delete this.db.names[p.nameKey];
    this.db.names[key] = playerId;
    p.name = String(name).trim(); p.nameKey = key; p.updatedAt = nowISO();
    this._save();
    return { ok: true, name: p.name };
  }

  async nameAvailable(name) {
    const key = normalizeName(name);
    return !this.db.names[key];
  }

  async putSave(playerId, save, expectedVersion) {
    const p = this.db.players[playerId];
    if (!p) return { ok: false, reason: 'no_player' };
    // optimistic concurrency: reject stale writes
    if (typeof expectedVersion === 'number' && expectedVersion !== p.saveVersion) {
      return { ok: false, reason: 'version_conflict', version: p.saveVersion, save: p.save };
    }
    p.save = save; p.saveVersion += 1; p.updatedAt = nowISO();
    this._save();
    return { ok: true, version: p.saveVersion };
  }

  async getSave(playerId) {
    const p = this.db.players[playerId];
    if (!p) return null;
    return { save: p.save, version: p.saveVersion };
  }

  async setCp(playerId, cp) {
    const p = this.db.players[playerId];
    if (!p) return;
    p.cp = Math.max(0, Math.floor(cp) || 0); p.updatedAt = nowISO();
    this._save();
  }

  // Global Power Ranking: top N by CP, plus the caller's own rank.
  async leaderboard(playerId, limit = 100) {
    const ranked = Object.values(this.db.players)
      .filter(p => p.name)
      .sort((a, b) => b.cp - a.cp);
    const top = ranked.slice(0, limit).map((p, i) => ({
      rank: i + 1, id: p.id, name: p.name, cp: p.cp,
      me: p.id === playerId,
    }));
    const myIndex = ranked.findIndex(p => p.id === playerId);
    const me = myIndex >= 0
      ? { rank: myIndex + 1, cp: ranked[myIndex].cp, name: ranked[myIndex].name }
      : null;
    return { top, me, total: ranked.length };
  }

  // Arena: real opponents near the caller's RP; bots fill in if the pool is thin.
  async arenaOpponents(playerId, count = 3) {
    const me = this.db.players[playerId];
    const pool = Object.values(this.db.players)
      .filter(p => p.id !== playerId && p.name)
      .sort((a, b) => Math.abs((a.arenaRp || 0) - (me?.arenaRp || 0)) - Math.abs((b.arenaRp || 0) - (me?.arenaRp || 0)));
    return pool.slice(0, count).map(p => ({ id: p.id, name: p.name, rp: p.arenaRp || 0, cp: p.cp }));
  }

  async arenaResult(playerId, opponentId, win) {
    const me = this.db.players[playerId];
    const opp = this.db.players[opponentId];
    if (!me) return { ok: false };
    const delta = win ? 24 : -14;
    me.arenaRp = Math.max(0, (me.arenaRp || 0) + delta);
    if (opp) opp.arenaRp = Math.max(0, (opp.arenaRp || 0) + (win ? -12 : 8)); // zero-sum-ish
    this._save();
    return { ok: true, rp: me.arenaRp, delta };
  }

  // ---- guilds (minimal) ----
  async createGuild(leaderId, name, tag) {
    const id = this._id('g');
    const g = { id, name, tag, leaderId, renown: 0, members: [leaderId], createdAt: nowISO() };
    this.db.guilds[id] = g;
    const p = this.db.players[leaderId]; if (p) p.guildId = id;
    this._save();
    return g;
  }
  async guildLeaderboard(limit = 50) {
    return Object.values(this.db.guilds).sort((a, b) => b.renown - a.renown)
      .slice(0, limit).map((g, i) => ({ rank: i + 1, id: g.id, name: g.name, tag: g.tag, renown: g.renown, members: g.members.length }));
  }
}
