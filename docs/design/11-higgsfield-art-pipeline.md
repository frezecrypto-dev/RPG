# 11 — Higgsfield Art Pipeline & Visual Bible

Goal: 70+ characters, 30+ enemies, 4 bosses, 40 stages of environment art — generated consistently enough to read as **one expensive game**, and derivable into every downstream asset (splash → portrait → cut-in → icon → card → marketing) from a single master generation per subject.

## 1. Art Direction Framework — "The ASHGATE Style Contract"

Every prompt is assembled from **locked blocks + variable blocks**. Locked blocks never change per asset; they ARE the art style. Variable blocks carry the subject. This is the whole consistency system: humans don't freestyle prompts, they fill slots.

### 1.1 The locked style block (prepended to every character/enemy/boss prompt, verbatim)

```
STYLE_CORE:
"dark fantasy anime illustration, premium mobile game quality, clean sharp
lineart with painterly rendering, high contrast rim lighting, deep blacks with
controlled bloom, cinematic color grading, crisp silhouette readable at small
scale, no visual clutter, single dominant light source plus one colored rim
accent, background minimal and atmospheric (soft gradient + faint particles),
character fills 70% of frame height, full body visible, 2:3 portrait canvas"
```

### 1.2 The locked negative block

```
STYLE_NEGATIVE:
"photorealism, western comic style, chibi, oversaturated rainbow palette,
busy background, motion blur, text, watermark, extra limbs, cluttered
accessories, low contrast, flat lighting"
```

### 1.3 Global rules (enforced by review checklist, §8)

- **Camera:** eye-level, slight low angle (+5–10°) for heroes (power fantasy), high angle for cowering minions, strong low angle for bosses. Lens feel: 50mm neutral; no fisheye, no dutch angles in base sheets (dynamism belongs to cut-ins only).
- **Lighting:** one key light (upper-left, warm-neutral), one rim light **in the unit's identity color** (class pair for heroes, family palette for enemies). Backgrounds are 2 stops darker than the subject — subject-pop is non-negotiable for mobile.
- **Clothing detail budget:** detail concentrates in the **upper third** (face, shoulders, weapon hand) where portrait crops live. Lower body simpler. Max 3 materials per outfit (e.g. steel + leather + cloth) — more reads as noise at phone scale.
- **Weapon readability:** the weapon must break the silhouette and be identifiable in a 128px icon. Weapon edge always catches the rim light. No weapon may cross the face in the base sheet (portrait crop safety).
- **Aura/VFX:** auras are *rims and wisps*, never full-body glow soup. VFX color = class pair only (doc 03 §3). Rarity scales aura complexity (§4), class sets its hue.

## 2. Prompt Template System

### 2.1 Character template (`HF-CHAR-*`)

```
[STYLE_CORE] +
"CLASS_BLOCK: {class silhouette rule + weapon language + VFX pair from doc 03 §3}" +
"RARITY_BLOCK: {from §4 table}" +
"SUBJECT: {name}, {gender/age/build}, {2-line visual concept from roster doc 04},
 {faction wardrobe motif: Emberguard=military plate & banners / Hollowed=corrupted
 elegance & exposed umbra veins / Choir=gold liturgical / Freeblades=practical
 mismatched gear / Gravebound=funerary & bone}" +
"POSE: confident idle, three-quarter stance, weapon visible, facing viewer-left" +
[STYLE_NEGATIVE]
```

Example (ASH-ASN-L01, The Hollow Smile):
```
[STYLE_CORE] CLASS_BLOCK: assassin, thin asymmetrical silhouette, blade edges
breaking the outline, crimson and black VFX identity, daggers. RARITY_BLOCK:
legendary — ornate costume tier, full ambient aura of crimson smoke threads,
one impossible visual element. SUBJECT: The Hollow Smile, tall androgynous male,
faceless cracked white porcelain mask with a painted grin, layered black silks,
his shadow cast in a different pose than his body, twin black daggers held
reversed. POSE: confident idle, three-quarter stance… [STYLE_NEGATIVE]
```

### 2.2 Enemy template (`HF-ENMY-*`)

```
[STYLE_CORE modified: "creature fills 60% of frame, high camera angle for
minions / eye-level for elites"] +
"FAMILY_BLOCK: {family palette + material language, doc 05 §1 — e.g. slimes:
 translucent toxic-teal gel, drowned debris suspended inside}" +
"TIER_BLOCK: minion = simple mass, one feature | elite = minion + armored or
 mutated element + faint aura | miniboss = elite + glowing core + battle scars" +
"THREAT_COLOR: warm rim = physical attacker / cool rim = magical attacker" +
"SUBJECT: {species description}" + [STYLE_NEGATIVE]
```

### 2.3 Boss template (`HF-BOSS-*`)

```
[STYLE_CORE modified: "3:2 landscape canvas, strong low angle, boss fills frame
edge-to-edge, hero-scale figure optional in foreground for scale"] +
"FAMILY_BLOCK + TIER_BLOCK: boss — colossal, one glowing WEAK-POINT element
 that will be referenced by combat mechanics, silhouette readable as a
 threat-icon at 64px" +
"PHASE VARIANTS: generate base + one 'phase 2' variant (damaged/transformed,
 same silhouette, escalated VFX)" + [STYLE_NEGATIVE]
```

### 2.4 Environment key art template (`HF-ENV-*`)

```
"dark fantasy anime background art, painterly, cinematic wide 16:9,
no characters, strong depth layering (foreground silhouette / midground
subject / background atmosphere), single environmental light story,
readable as a blurred battle backdrop AND as a chapter title card" +
"CHAPTER_BLOCK: {chapter palette + motifs from doc 06 §3}" +
"VARIANT: {stage sub-location, e.g. 'flooded arcade of shops, lantern jellies
 drifting between pillars'}"
```
Per chapter: 1 hero key art + 4 stage-backdrop variants (10 stages share 4 backdrops + lighting shifts — cost control with perceived variety).

## 3. Style Control & Consistency Ops

- **Seed & reference discipline:** first approved generation of each character becomes its **canonical reference image**; all re-generations (skins, cut-ins, marketing) use image-reference/character-consistency features against it. Canonical refs live in the asset repo under `art/canon/<unitId>/`.
- **Batch by class:** generate all 10 units of a class in one session with identical locked blocks; consistency drifts across sessions, so never interleave classes.
- **Two-pass workflow:** pass 1 = 4 candidates per subject → art lead picks/annotates; pass 2 = refine winner (fix hands/weapon/face) → canonize. Budget ~30 generations per shipped character including derivations.
- **Style drift audit:** monthly contact-sheet of every canonical ref at thumbnail size; any unit that no longer reads as "same game" gets regenerated. The contact sheet IS the visual bible's living page.

## 4. Rarity Differentiation (visual)

| Rarity | Costume tier | Aura | Frame (UI) | Extra |
|---|---|---|---|---|
| Common | Practical, worn, 2 materials | None (weapon glint only) | Grey steel | — |
| Rare | Fitted, maintained, faction motif visible | Weapon glow + small accent wisps | Blue | — |
| Epic | Ornamented, one animated-feeling element | Partial aura (one side / one limb) | Purple | Skill cut-in art |
| Legendary | Ornate + **one impossible element** (floating shield-fragment, shadow acting independently, halo array) | Full ambient aura + environmental interaction (ground scorch, floating debris) | Gold + animated shimmer | Unique cut-in, idle flourish, ult screen-effect |

Rule: rarity NEVER changes the class hue — a Common assassin and Legendary assassin are both crimson/black. Rarity = *intensity*, class = *color*, family = *enemy color*. Three axes, never mixed.

## 5. Downstream Asset Derivation (from one canonical master per subject)

| Asset | Method | Spec |
|---|---|---|
| Splash art | Master itself (2:3, 2048×3072 upscaled) | Roster screen, banner hero |
| Battle portrait | Crop upper-third of master, 512×512 | Team bar, turn order |
| Icon | Bust crop 256×256 + rarity frame overlay | Everywhere |
| Skill cut-in | Re-generate: canonical ref + "dynamic action pose, {skill fantasy line}, speed-lines background in class colors, extreme perspective" 16:9 | Ultimate activation |
| Enemy card | Enemy master + card frame template | Codex (doc 06 §5) |
| Marketing screenshots | Key art + character masters composited via template PSDs | Store pages, ads |
| Skins | Canonical ref + new OUTFIT block (silhouette + palette rules still locked) | Cosmetic shop |

Naming: `art/<type>/<unitId>__<asset>__v<NN>.png` (e.g. `art/char/ASH-ASN-L01__cutin__v02.png`) — matches data IDs (doc 15) so tooling can auto-wire assets.

## 6. Production Order

1. Style lock sprint: 1 unit per class (7) + 1 enemy per family (4) + 4 chapter key arts → freeze STYLE_CORE.
2. Class batches (10 units each ×7).
3. Enemy batches per chapter, in campaign order.
4. Bosses + phase variants.
5. Cut-ins for Epic/Legendary (30 units).
6. Marketing set last (style is mature by then).

## 7. Review Checklist (every asset, 60 seconds, pass/fail)

- [ ] Silhouette identifies class/family at 96px?
- [ ] Class/family color pair correct and dominant?
- [ ] Rarity tier readable next to a same-class unit of adjacent rarity?
- [ ] Weapon identifiable at icon size, not crossing face?
- [ ] Upper-third crop works as portrait?
- [ ] Reads against BOTH dark UI and bright battle backdrop?
- [ ] No style drift vs. class contact sheet?
