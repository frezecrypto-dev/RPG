#!/usr/bin/env node
// Download the canon character portraits into web/prototype/art/<hero-id>.png
//
// Run this on a machine WITH internet access (the ASHGATE sandbox cannot reach
// the art host). From the repo root:
//
//     node tools/fetch_portraits.mjs
//
// Then commit the web/prototype/art/ folder. The prototype already prefers
// art/<id>.png over the remote URL, so the portraits then work offline and can
// be embedded into the published artifact.

import { readFileSync, mkdirSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const outDir = join(root, 'web', 'prototype', 'art');
mkdirSync(outDir, { recursive: true });

const manifest = JSON.parse(readFileSync(join(root, 'art', 'canon-manifest.json'), 'utf8'));
const chars = manifest.characters || {};
const ids = Object.keys(chars).filter((id) => chars[id] && chars[id].raw);

console.log(`Fetching ${ids.length} portraits -> ${outDir}`);
let ok = 0, skip = 0, fail = 0;

for (const id of ids) {
  const dest = join(outDir, `${id}.png`);
  if (existsSync(dest)) { skip++; continue; }
  try {
    const res = await fetch(chars[id].raw);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const buf = Buffer.from(await res.arrayBuffer());
    writeFileSync(dest, buf);
    ok++;
    process.stdout.write(`\r  ${ok + skip}/${ids.length}  ${id}         `);
  } catch (e) {
    fail++;
    console.warn(`\n  ! ${id}: ${e.message}`);
  }
}

console.log(`\nDone. downloaded=${ok} skipped=${skip} failed=${fail}`);
if (fail) process.exitCode = 1;
