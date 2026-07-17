# 15 — Data Schemas, Naming Conventions & Spreadsheet Structure

## 1. ID & Naming Conventions (immutable after first use)

```
Units:        ASH-<CLS>-<R><nn>      CLS ∈ {TNK,ASN,RNG,MAG,NEC,HLR,BSK}, R ∈ {C,R,E,L}
Skills:       SKL-<unitId>-S<1..4>            e.g. SKL-ASH-ASN-L01-S3
Status:       STS-<NAME>                      e.g. STS-BLEED, STS-ARMOR-BREAK
Enemies:      ENM-<FAM>-<TIER><nn>            FAM ∈ {SLM,GNT,GRD,UND}, TIER ∈ {M,E,B(miniboss),X(boss)}
Stages:       STG-<mode>-<ch>-<st>[-H]        e.g. STG-CAMP-2-07, STG-CAMP-2-07-H, STG-RAID-FND-T3
Banners:      BNR-<type>-<yyyy>-W<ww>
Items:        ITM-<family>-<name>-<tier>      e.g. ITM-STAR-SHARD-TNK, ITM-GEAR-ORE-T2
Gear:         GEAR-<slot>-<set>-<tier>        slot ∈ {WPN,ARM,HLM,CHM,SGL}
Quests:       QST-<track>-<nnn>
Loc keys:     <domain>.<id>.<field>           e.g. unit.ASH-ASN-L01.name, skill.SKL-...-S3.desc
Art files:    art/<type>/<id>__<asset>__v<NN>.png   (doc 11 §5)
Config vers:  cfg-<yyyy.mm.dd>-<n>
```
Rules: IDs are ASCII, stable, and never encode balance data. Display names live only in loc tables. Deleting an ID is forbidden — deprecate with `"status": "retired"`.

## 2. Core JSON Table Schemas (server-pushed config bundles, doc 12 §4)

### units.json (per unit — full example in doc 04 §5)
```json
{ "id": "ASH-TNK-C01", "class": "TNK", "rarity": "C", "faction": "Emberguard",
  "row": "front", "damageRoot": "physical", "subtags": [],
  "baseStats": {"hp":1450,"atk":95,"def":132,"spd":96},
  "growthCurve": "common_std", "starCap": 5, "ascensionNodes": ["..."],
  "skills": ["SKL-ASH-TNK-C01-S1","...S2","...S3","...S4"],
  "aiProfile": {"ultPriority": 60, "ultCondition": "team_hp_pct<70"},
  "artRef": "ASH-TNK-C01", "status": "live" }
```

### skills.json (effects are a composable verb list — the whole combat data model)
```json
{ "id": "SKL-ASH-TNK-C01-S3", "slot": "S3", "surgeCost": 50,
  "target": "team_ally",
  "effects": [
    {"verb":"applyStatus","status":"STS-DR-25","duration":2,"chance":1.0}
  ],
  "power": null, "cutinArt": null, "upgrades": {"perLevel":"dr +2%","maxLevel":5} }
```
Verb whitelist (engine-implemented, data-composed): `damage, heal, shield, applyStatus, cleanse, strip, steal, summon, sacrifice, revive, surgeMod, taunt, reposition`. New verbs = engineering ticket; new skills = data only.

### statuses.json
```json
{ "id": "STS-BLEED", "kind": "dot", "root": "physical", "stackMax": 5,
  "tickPower": 0.08, "tickStat": "applier_atk", "piercesShield": true,
  "dispellable": true, "icon": "sts_bleed" }
```

### enemies.json / stages.json
```json
{ "id": "ENM-GNT-E01", "family": "GNT", "tier": "E",
  "traits": ["colossal","armored"], "physRes": 0.25, "magRes": 0,
  "immunities": ["STS-STUN"], "skills": ["..."], "aiScript": "brute_v1",
  "telegraphs": [{"skill":"...","windup":3,"pattern":"single_highest_atk"}] }

{ "id": "STG-CAMP-2-07", "waves": [["ENM-GNT-M02","ENM-GNT-M02","ENM-GNT-E01"], ["..."]],
  "enemyLevel": 34, "aetherCost": 8, "roundLimit": 20,
  "starRules": ["clear","no_deaths","rounds<=10"],
  "firstClear": [{"item":"ITM-CRYSTAL","qty":50}], "repeatDrops": "DRT-CAMP-2", "backdrop": "ENV-CH2-B3" }
```

### droptables.json, banners.json (doc 08 §7), shops.json, events.json — same pattern: id + rules + references, no prose.

## 3. Content Spreadsheet Structure (source of truth → JSON build)

Workbook per domain, one row per entity, columns mirror schema fields:
1. **Units** (tabs: Units, Skills, AscensionNodes, GrowthCurves)
2. **Combat** (Statuses, Verbs-reference, AIProfiles)
3. **Enemies&Stages** (Enemies, Telegraphs, Stages, DropTables)
4. **Economy** (Currencies, Faucets [every grant in the game, one row each], Sinks, PullIncomeBudget — the doc 10 §2 ledger)
5. **LiveOps** (Banners, Events, Shops, Calendar)
6. **Loc** (exported keys + EN strings)

Build CLI: `content build → validate → diff vs prod → publish to staging`. Validation includes schema, dangling-ID lint, and balance guardrails (doc 04 §4, doc 10 §2) as failing checks.

## 4. Balancing Sheets (companions, not shipped)
- **StatCurves:** rarity multipliers × growth curves × star/ascension bonuses → auto-computed effective stats at benchmark points (Lv30/2★, Lv50/4★A1, Lv60/6★A3).
- **DamageModel:** the doc 02 §5 formula live, for skill-power sanity checks (S1 ≈ 100–120%, S2 ≈ 160–200%, S3 ≈ 280–340% single / 180–220% AoE).
- **F2P-90d:** simulated daily income/spend per player archetype vs. content power requirements — the CI guardrail source.
