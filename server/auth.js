// Stateless session tokens — HMAC-signed, no external JWT dependency.
//
// Format: base64url(payloadJSON).base64url(hmacSHA256(payload, secret))
// Payload: { sub: playerId, iat, exp }
//
// Production notes:
//   - Set ASHGATE_SECRET to a long random value (rotate periodically).
//   - For OAuth (Google / Apple / Play Games) verify the provider's id_token
//     against their JWKS and use the verified `sub` as providerSub. The
//     verifyOAuth() stub below marks where that goes; NEVER trust an unverified
//     id token in production.

import { createHmac, timingSafeEqual } from 'node:crypto';

const SECRET = process.env.ASHGATE_SECRET || 'dev-insecure-secret-change-me';
const TTL_SECONDS = 60 * 60 * 24 * 30; // 30 days

const b64url = (buf) => Buffer.from(buf).toString('base64url');
const fromB64url = (s) => Buffer.from(s, 'base64url');

export function signToken(playerId) {
  const payload = { sub: playerId, iat: Math.floor(Date.now() / 1000), exp: Math.floor(Date.now() / 1000) + TTL_SECONDS };
  const body = b64url(JSON.stringify(payload));
  const sig = createHmac('sha256', SECRET).update(body).digest('base64url');
  return `${body}.${sig}`;
}

export function verifyToken(token) {
  if (!token || typeof token !== 'string' || !token.includes('.')) return null;
  const [body, sig] = token.split('.');
  const expected = createHmac('sha256', SECRET).update(body).digest('base64url');
  const a = fromB64url(sig), b = fromB64url(expected);
  if (a.length !== b.length || !timingSafeEqual(a, b)) return null;
  let payload;
  try { payload = JSON.parse(fromB64url(body).toString('utf8')); } catch { return null; }
  if (!payload.sub || (payload.exp && payload.exp < Math.floor(Date.now() / 1000))) return null;
  return payload;
}

// Stub: in production, verify the provider id_token against its JWKS.
// Returns { provider, providerSub } on success or null on failure.
export async function verifyOAuth(provider, idToken) {
  if (!provider || !idToken) return null;
  // DEV ONLY: accept "provider:sub" style tokens so the flow is testable
  // without real Google/Apple credentials. Replace with real verification.
  if (process.env.NODE_ENV === 'production') {
    throw new Error('verifyOAuth: real provider verification not implemented');
  }
  const sub = String(idToken).includes(':') ? String(idToken).split(':').pop() : String(idToken);
  return { provider, providerSub: `${provider}:${sub}` };
}
