// Build the deployable client from the single-file prototype.
//
// The prototype (web/prototype/index.html) is a *body fragment*: it has styles,
// markup and script but no <html>/<head>. A browser tolerates that, but without
// a viewport meta a phone renders it at desktop width — so shipping the raw file
// is not an option. This wraps it in a real document and injects the backend URL.
//
//   node tools/build-web.mjs                       -> dist/index.html (offline)
//   ASHGATE_SERVER=https://api.example.com node tools/build-web.mjs   (online)

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';

const SRC = 'web/prototype/index.html';
const OUT_DIR = 'dist';
const OUT = `${OUT_DIR}/index.html`;

const TITLE = 'Project ASHGATE';
const DESC = 'A dark-fantasy squad RPG — summon a roster of Vowbound, forge a party of five, and fight through the gates.';

const server = (process.env.ASHGATE_SERVER || '').trim().replace(/\/+$/, '');

let body = readFileSync(SRC, 'utf8');
// The fragment carries its own charset meta; the wrapper supplies the real one.
body = body.replace(/^\s*<meta charset="utf-8">\s*\n?/i, '');

const serverTag = server
  ? `<script>window.ASHGATE_SERVER=${JSON.stringify(server)};</script>`
  : `<!-- offline build: no ASHGATE_SERVER configured -->`;

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,maximum-scale=1">
<title>${TITLE}</title>
<meta name="description" content="${DESC}">
<meta name="theme-color" content="#0a0910">
<meta name="color-scheme" content="dark">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta property="og:title" content="${TITLE}">
<meta property="og:description" content="${DESC}">
<meta property="og:type" content="website">
<style>html,body{margin:0;padding:0;background:#0a0910}</style>
${serverTag}
</head>
<body>
${body}
</body>
</html>
`;

mkdirSync(OUT_DIR, { recursive: true });
writeFileSync(OUT, html);
const mb = (Buffer.byteLength(html) / 1048576).toFixed(2);
console.log(`[build] ${OUT} — ${mb} MB — backend: ${server || '(offline)'}`);
