# Art assets — drop images here

This folder is the drop-off point for artwork Claude should embed into the
prototype (guide character, hero portraits, backgrounds, etc.).

## How to add an image

**Easiest (no git needed) — GitHub web upload:**
1. Open the repo on github.com → switch to branch `claude/gacha-rpg-design-doc-49ya05`.
2. Go into `web/prototype/assets/`.
3. **Add file ▸ Upload files** → drag the image in → **Commit** to this branch.
4. Tell Claude the filename (e.g. "use `guide-chibi.png` for Ivory").

**Or:** paste a **public image URL** in chat and Claude will download it here.

## Naming hints
- Tutorial guide: `guide-chibi.png`
- Anything else: a short descriptive name, PNG or WEBP.

Claude compresses large images to WEBP before embedding (the single-file
prototype is close to the 16 MB artifact limit, so raster art is kept small).
