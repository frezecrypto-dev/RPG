# 03 — Class Design Framework

## 1. The 7 Launch Classes — Role Matrix

| Class | Primary role | Secondary role | Root damage | Signature verbs | Row |
|---|---|---|---|---|---|
| Tank | Frontline | Utility | Physical | Taunt-Me, Barrier, DR, Guard | Front |
| Assassin | Single-target DPS | Debuff | Physical (Bleed) | Bleed, Stealth, backline dive | Back |
| Ranger | Sustained DPS | Enabler | Physical (Pierce) | Mark, Armor Break, focus-fire | Back |
| Mage | AoE DPS | Control | Magical (Arcane) | AoE, Strip/Steal, Bind | Back |
| Necromancer | Attrition DPS | Summoner | Magical (Shadow/Decay) | Summon undead, Decay, sacrifice | Back |
| Healer | Sustain | Cleanse/Buff | Magical (Holy) | Heal, Cleanse, Barrier, Revive | Back |
| Berserker | Burst DPS | Frontline pressure | Physical | Rage scaling, Execute, self-cost | Front |

**Party grammar:** 5 slots, 2 front + 3 back by default (front slots absorb single-target aggro weighting 60/40). Recommended baseline comp taught by tutorial: Tank + Berserker (front), DPS + flex + Healer (back).

## 2. Class Kit Rules (constraints every character of the class obeys)

These rules are what make "class identity" real across 10+ units each. A character may bend **one** rule (that's what makes them special); never two.

### Tank
- S1 or S2 must include a self-survivability or ally-protection verb.
- Every Tank has access to Taunt-Me somewhere in the kit.
- Tanks never exceed 70% of a same-rarity DPS unit's damage output.
- Passive interacts with *being hit* (counter, Surge gen, stacking DEF).

### Assassin
- Kit must apply or exploit Bleed. Bleed ticks pierce Barriers (class-exclusive rule).
- Highest single-target burst per rarity tier, lowest HP pool multiplier (0.8×).
- At least one mobility/evasion verb (Stealth, untargetable, dodge-up) per kit.

### Ranger
- Kit must contain Mark or Armor Break (the "enabler" contract — Rangers make the *team* hit harder).
- Damage profile: consistent multi-hit (crit-scaling), not spike.
- Ultimates favor "execute the Marked target" or "team focus-fire" fantasies.

### Mage
- Best AoE per rarity tier; S3 is always AoE or a battlefield-state changer.
- Owns the Strip/Steal/Bind verbs (control without hard stun spam).
- Squishiest backline (HP 0.85×), SPD mid.

### Necromancer
- Every kit interacts with **Summons**: skeletal units occupying a virtual 6th/7th slot (max 2 active; summons have 1 skill, act after their master, can be targeted — they are the Necromancer's "HP bank").
- Summon damage root type varies **per character** (physical skeleton bruisers vs magical wraiths) — this is the build-identity promise from the vision doc.
- Owns Decay (anti-heal). Sacrifice verbs (consume summon for effect) appear at Epic+.

### Healer
- Every kit heals; scaling stat is caster ATK or maxHP per unit (data-defined).
- Owns Cleanse and Revive (Revive at Epic+ only, hard-limited: max 1 revive per battle per team — anti-stall rule).
- Offensive Holy sub-tag gives Healers a damage niche vs Undead (chapter 4 relevance so autoplay healers aren't dead slots).

### Berserker
- Rage mechanic: personal stacking buff (+4% ATK per stack, max 10) gained on dealing/taking damage; stacks reset on battle end, some kits spend stacks.
- Self-cost verbs (pay %HP for power) and Execute (<25% HP targets) are class-exclusive.
- Front-row eligible; HP 1.1× but no self-sustain unless a kit's "bent rule."

## 3. Visual & VFX Class Identity (contract with the art pipeline, doc 11)

Each class owns a **silhouette rule + a two-color VFX identity**. Rarity changes *intensity and complexity*, never the class hue (so players read class instantly, rarity second).

| Class | Silhouette rule | VFX primary / secondary | Weapon language |
|---|---|---|---|
| Tank | Widest silhouette; shield always visible in outline | Steel blue / white | Tower shields, bulwarks, gauntlets |
| Assassin | Thinnest, asymmetrical, blade edges break the outline | Crimson / black | Daggers, hooks, wire |
| Ranger | Long horizontal line (bow/rifle) crossing the frame | Amber / teal | Bows, arbalests, hex-rifles |
| Mage | Floating elements around silhouette (books, orbs, halos) | Violet / cyan | Staves, foci, glyphs |
| Necromancer | Tattered verticality + always accompanied by a minion shape | Sickly green / bone white | Scythes, censers, grave-bells |
| Healer | Rounded, symmetrical, light source inside the figure | Gold / soft white | Chalices, reliquaries, wands |
| Berserker | Oversized weapon, forward-leaning mass, exposed skin/scars | Blood orange / ash grey | Greataxes, cleavers, chained blades |

These seven color pairs are **reserved**: no enemy family may use a class's exact VFX pair (enemy palettes defined in doc 05 §1).
