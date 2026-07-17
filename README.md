# Project ASHGATE (Working Title)

**Genre:** 2D anime dark-fantasy gacha RPG — party-based PvE hero collector
**Platforms:** iOS / Android (portrait-first UI, landscape combat optional later)
**Working codename:** `ASHGATE`
**IP status:** Original IP. Tone inspiration: dark power-fantasy intensity (Solo Leveling-adjacent mood), but original world, characters, and terminology.

## World Premise (one paragraph, enough to anchor art + content)

Decades ago, the **Ashgates** opened — wounds in reality that bleed monsters and a corrupting energy called **Umbra**. Humanity survives behind warded cities and fights back with **Vowbound**: humans who bound their souls to fragments of dead gods and gained combat classes. The player is a **Gatewarden**, commanding a squad of Vowbound to push back through four fallen regions and close the Gates — while something on the other side is learning to push back.

## Documentation Index

| # | File | Contents |
|---|------|----------|
| 01 | [Game Pillars & Core Loop](docs/design/01-game-pillars-core-loop.md) | Pillars, core/meta loop, session design |
| 02 | [Combat System](docs/design/02-combat-system.md) | Combat model, skills, buffs/debuffs, status taxonomy, counterplay |
| 03 | [Class Framework](docs/design/03-class-framework.md) | 7 classes: role, kit rules, VFX/color identity |
| 04 | [Launch Roster](docs/design/04-launch-roster.md) | All 70 launch characters, rarity philosophy, synergy tags |
| 05 | [Enemy & Boss Framework](docs/design/05-enemy-boss-framework.md) | Enemy families, boss mechanics, telegraph rules, boss sheets |
| 06 | [Campaign](docs/design/06-campaign.md) | 4 chapters × 10 stages, unlock schedule, difficulty curve |
| 07 | [Raids, Co-op & Guild](docs/design/07-raids-coop-guild.md) | Farming raids, weekly co-op raid, guild system |
| 08 | [Gacha System](docs/design/08-gacha.md) | Banners, rates, pity, dupes, beginner banner |
| 09 | [Progression & Upgrades](docs/design/09-progression-upgrades.md) | Levels, stars, ascension, gear (5 slots), dupe economy |
| 10 | [Economy, Retention & Monetization](docs/design/10-economy-retention-monetization.md) | Currencies, sources/sinks, loops, monetization policy |
| 11 | [Higgsfield Art Pipeline](docs/design/11-higgsfield-art-pipeline.md) | Visual bible, prompt templates, consistency rules, asset derivation |
| 12 | [Technical Architecture](docs/design/12-technical-architecture.md) | Engine, backend, live ops, data-driven content, anti-cheat |
| 13 | [MVP vs Full Roadmap](docs/design/13-roadmap-mvp.md) | Phased build plan and release gates |
| 14 | [Risks & Balance Pitfalls](docs/design/14-risks-pitfalls.md) | What will break this game if ignored |
| 15 | [Data Schemas & Naming](docs/design/15-data-schemas-naming.md) | JSON table structures, ID conventions, spreadsheet layout |
| 16 | [Home Screen / Hub UX](docs/design/16-home-screen-ux.md) | Main hub layout, navigation model, top bar, event surfacing |

## How to read these docs

- Every number in these documents is a **tuned starting value**, not a guess to be discarded. Change numbers through the balancing spreadsheets (doc 15), not ad hoc.
- Cross-doc terms are canonical: if doc 02 calls the ultimate resource **Surge**, every doc and every data table calls it Surge.
- Content IDs follow the conventions in doc 15 from day one. Retrofitting IDs after launch is not possible without migration pain.
