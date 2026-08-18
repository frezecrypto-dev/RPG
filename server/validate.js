// Server-authoritative save validation (anti-cheat seam).
//
// The prototype is currently client-authoritative (localStorage). Going online,
// the server must not blindly trust the client's save. This module is where
// that trust boundary lives. For the scaffold it does structural + bounds
// checks and derives a clamped CP; in production you would:
//   - Recompute Combat Power from hero states using the SAME rules the client
//     uses (share the formula as an isomorphic module), never the client's number.
//   - Rate-limit currency deltas against elapsed time and known faucets.
//   - Reject states referencing unknown hero/item ids.
//   - Keep an append-only audit log of suspicious diffs.

const CEIL = {
  crystals: 5_000_000, gold: 2_000_000_000, starShards: 5_000_000,
  relics: 2_000_000, insight: 5_000_000, gleam: 2_000_000, vowTickets: 100000,
};

export function validateSave(save) {
  if (!save || typeof save !== 'object') return { ok: false, reason: 'not_object' };

  // currencies must be finite, non-negative, within plausible ceilings
  for (const [k, max] of Object.entries(CEIL)) {
    if (k in save) {
      const v = save[k];
      if (typeof v !== 'number' || !Number.isFinite(v) || v < 0) return { ok: false, reason: `bad_${k}` };
      if (v > max) return { ok: false, reason: `ceil_${k}` };
    }
  }

  // owned roster sanity
  if (save.owned && !Array.isArray(save.owned)) return { ok: false, reason: 'owned_shape' };
  if (Array.isArray(save.owned) && save.owned.length > 500) return { ok: false, reason: 'owned_count' };

  // progress map sanity (levels/stars within hard caps)
  if (save.progress && typeof save.progress === 'object') {
    for (const pr of Object.values(save.progress)) {
      if (!pr || typeof pr !== 'object') continue;
      if (pr.level != null && (pr.level < 1 || pr.level > 120)) return { ok: false, reason: 'level_cap' };
      if (pr.stars != null && (pr.stars < 1 || pr.stars > 6)) return { ok: false, reason: 'star_cap' };
      if (pr.over != null && (pr.over < 0 || pr.over > 5)) return { ok: false, reason: 'over_cap' };
    }
  }

  // CP: production recomputes from progress; here we accept a client hint but
  // clamp it to a sane maximum so it can't poison the leaderboard.
  let cp = 0;
  if (typeof save._accountCP === 'number' && Number.isFinite(save._accountCP)) {
    cp = Math.max(0, Math.min(50_000_000, Math.floor(save._accountCP)));
  }

  return { ok: true, cp };
}
