# 04 — Full Launch Roster Plan (70 Characters)

## 1. What Rarity Means

| Dimension | Common | Rare | Epic | Legendary |
|---|---|---|---|---|
| **Gameplay identity** | One job, done reliably. Simple, strong, no conditions | One job + one condition/synergy hook | Two interlocking mechanics; team-defining in a niche | Battlefield-warping ultimate; defines an archetype |
| **Kit complexity** | 0 conditional clauses | 1 conditional clause | 2 conditional clauses | 3 max — never more (readability pillar) |
| **Base stat budget** | 100% | 108% | 118% | 130% |
| **Stat growth/level** | 1.00× | 1.05× | 1.12× | 1.20× |
| **Max stars** | Start 1★, cap 5★ | Start 2★, cap 6★ | Start 3★, cap 6★ | Start 3★, cap 6★ |
| **Visual** | Clean outfit, minimal VFX aura | + weapon glow, small aura | + full aura, animated skill cut-in | + unique cut-in art, environmental VFX on ult, idle animation flourish |
| **Summon rate** | 45% | 38% | 14% | 3% (doc 08) |
| **Dupes needed to max** | Cheap (5 total) | 8 | 10 | 12 — but Legendary shards farmable (doc 09 §4) |
| **Upgrade cost efficiency** | Cheapest per power point — the "budget carry" promise | Cheap | Standard | Expensive (1.6× material cost) |

**Investment-efficiency rule:** a maxed Common ≈ 78% of a maxed Legendary's raw output **at ~35% of the material cost** — and several Commons/Rares own *utility verbs Legendaries don't get* (see tags below). That is the anti-"legendary-only" mechanism: Legendaries are ceilings, low rarities are efficient floors and unique tools.

## 2. Anti-"Legendary-Only" Synergy Design

Three enforced mechanisms:

1. **Exclusive verbs at low rarity.** Some battlefield verbs exist *only* on Common/Rare units at launch (marked ⭐ below): e.g. the only launch unit with team-wide SPD Up is a Rare; the cheapest reliable Armor Break is a Common. Encounter design (docs 05–07) tests these verbs, so "5 Legendaries" is often a *worse* answer than "3 Legendary + 2 budget tools."
2. **Faction/tag synergy.** Every unit carries 1 faction tag — `Emberguard` (city military), `Hollowed` (Umbra-touched), `Choir` (holy order), `Freeblades` (mercenaries), `Gravebound` (necro-cult) — and content mutators grant +15% stats to a featured faction weekly. Factions are rarity-mixed by design.
3. **Co-op raid role checks** (doc 07 §2) explicitly require Cleanse/Taunt/Armor-Break slots that budget units fill at equal effectiveness (utility verbs don't scale with rarity — only stats do).

## 3. Roster Tables

Codename format: `ASH-<CLS>-<R><nn>` (doc 15). Damage: P=Physical, M=Magical (+sub-tag).

### 3.1 TANK — steel blue/white, widest silhouettes

| ID | Name | Rarity | Role | Dmg | Combat identity & skill fantasy | Visual concept |
|---|---|---|---|---|---|---|
| ASH-TNK-C01 | **Garrick, Gatehouse Door** | Common | Pure frontline | P | The reliable wall: Taunt-Me + flat DR self-buff; ult = 2-round team-wide 25% DR. Simplest, always-useful tank ⭐(cheapest team DR in game) | Grizzled militia veteran, dented tower shield taller than himself, sandbag-grey cloak |
| ASH-TNK-C02 | **Bram Coalhide** | Common | Counter tank | P | Punishes attackers: counterattacks when hit, stacks DEF per hit taken; ult taunts all enemies 1 round | Squat foundry worker in riveted furnace plate, glowing coal seams in armor |
| ASH-TNK-R01 | **Sera Ironvow** | Rare | Barrier tank | P | Converts damage taken into Barriers for the weakest ally; passive shares 15% of damage aimed at backline | Young oath-knight, chained gauntlet linked to a floating kite shield |
| ASH-TNK-R02 | **Odo of the Ninth Wall** | Rare | Anti-magic tank | P | Magic-damage specialist wall: self magRes, ult grants team Immunity (1 debuff) ⭐(cheapest Immunity) | Monk-engineer with rune-etched pavise, blue ward-script circling him |
| ASH-TNK-R03 | **Kellan Vice** | Rare | Aggro controller | P | Lockdown: S2 Binds one enemy + forces it to target him; boss-fight aggro tool | Freeblade duelist-turned-bodyguard, hooked chain shield, scarred grin |
| ASH-TNK-E01 | **Vashti, Bulwark of Glass** | Epic | Barrier specialist | M (Arcane) | Rule-bender: *magical* tank. Casts crystal Barriers on lowest-HP allies each round; shattered Barriers deal AoE arcane damage back | Elegant Hollowed woman, translucent crystal armor growing from her skin |
| ASH-TNK-E02 | **Morholt Gravemantle** | Epic | Attrition tank | P | Self-resurrecting anchor (once/battle, 40% HP); DoT-immune passive; pairs with Necromancers (Gravebound tag) | Exhumed knight, coffin-lid shield, green grave-light through visor slits |
| ASH-TNK-E03 | **Sigrun Aegisdottir** | Epic | Offensive tank | P | Tank that enables: her Taunt-Me also grants her Counter + team ATK Up on ult — the "aggressive comp" tank | Shield-maiden with twin bucklers, valkyrie-esque winged helm, storm-blue aura |
| ASH-TNK-L01 | **Roland, the Last Rampart** | Legendary | Ultimate protector | P | Team-defining: intercepts the first fatal hit on any ally per round; ult = 2-round team Immunity + massive Barrier. The boss-mechanic answer key | Colossal paladin in cathedral-plate; shield is a fragment of a city gate, white-and-steel light |
| ASH-TNK-L02 | **Kaela Nightwarden** | Legendary | Control tank | M (Shadow) | Umbra-corrupted tank: taunted enemies take Decay; ult drags all enemies' targeting onto her mirror-clone. High-skill misdirection fantasy | Black-armored warden holding a gate of shadow as a shield, violet-steel fire eyes |

### 3.2 ASSASSIN — crimson/black, thin asymmetry

| ID | Name | Rarity | Role | Dmg | Combat identity & skill fantasy | Visual concept |
|---|---|---|---|---|---|---|
| ASH-ASN-C01 | **Whisper (Ilo)** | Common | Bleed applier | P (Bleed) | Baseline bleeder: every skill applies Bleed; simple, best budget DoT engine ⭐(most reliable cheap Bleed stacks) | Street orphan in patched leathers, twin shivs, red thread bracelets |
| ASH-ASN-C02 | **Ratchet Anna** | Common | Finisher | P | Execute-lite: bonus damage vs targets under 30% HP; teaches finishing discipline | Bounty clerk with a mechanical crossbow-dagger, ledger of marks on her belt |
| ASH-ASN-R01 | **Vesk Halfsmile** | Rare | Backline diver | P (Bleed) | Ignores frontline: S2 hits the enemy backline directly; Stealth on kill | Lanky knife-juggler, half his face paralyzed into a grin, coat of hidden blades |
| ASH-ASN-R02 | **Mireille Threadcut** | Rare | Anti-support | P | Support-killer: bonus damage to enemies with buffs, S2 Strips one buff on hit ⭐(cheapest Strip) | Seamstress-assassin with monofilament wire gloves, funeral-lace dress |
| ASH-ASN-R03 | **Joss Emberknife** | Rare | Bleed detonator | P (Bleed) | Consumes Bleed stacks to burst: "rupture" fantasy; pairs with C01 | Freeblade pyro-cutthroat, heated dagger leaving cauterized wounds, ember trail |
| ASH-ASN-E01 | **Nyx Serrata** | Epic | Bleed engine | P (Bleed) | Bleed scaling: her passive makes team Bleeds tick twice/round; the bleed-comp keystone | Hollowed woman with serrated bone-blades growing from forearms, black-red aura |
| ASH-ASN-E02 | **Cassian Veil** | Epic | Assassin-controller | P | Stealth master: opens battles Stealthed, S2 Binds isolated targets, ult chains 3 executions if each kills | Aristocrat duelist in smoke-silk, rapier and misericorde, face never fully lit |
| ASH-ASN-E03 | **Ten-Knives Orla** | Epic | AoE assassin | P (Bleed) | Rule-bender: *AoE* assassin — ult hits all enemies, applying Bleed to each; raid-farm favorite | Whirling dervish with a skirt of hanging knives, ribbons of red light |
| ASH-ASN-L01 | **The Hollow Smile** | Legendary | Burst executioner | P (Bleed) | Apex predator: resets his own turn on kill (once/round); ult executes below 25% instantly. The "screen goes dark, one slash" fantasy | Faceless figure in a cracked porcelain mask; his shadow moves before he does |
| ASH-ASN-L02 | **Seraphine Redveil** | Legendary | Debuff empress | P (Bleed) | Team-warping: enemies bleeding from any source take +20% damage from everyone (passive aura). Makes budget bleeders scale forever | Crimson-veiled noblewoman conducting blood like ribbon-silk, bladed fans |

### 3.3 RANGER — amber/teal, long horizontal lines

| ID | Name | Rarity | Role | Dmg | Combat identity & skill fantasy | Visual concept |
|---|---|---|---|---|---|---|
| ASH-RNG-C01 | **Fletch** | Common | Armor breaker | P (Pierce) | The budget enabler: S2 = reliable Armor Break ⭐(cheapest Armor Break in game — permanently metagame-relevant) | Teen scout with an oversized salvaged arbalest, quiver of mismatched bolts |
| ASH-RNG-C02 | **Marta Longwatch** | Common | Consistent DPS | P | Steady multi-hit volley damage, +crit vs Marked targets; the tutorial carry | Weathered wall-sentry with a longbow and tally-scarred bracer |
| ASH-RNG-R01 | **Corvo Hexlock** | Rare | Marker | P (Pierce) | Mark specialist: S1 applies Mark, passive extends Mark duration; focus-fire captain | Witch-hunter with a rune-engraved hex-rifle, coat of warding charms |
| ASH-RNG-R02 | **Brenna Two-Strings** | Rare | Hybrid support-ranger | P | Enabler: arrows grant allies SPD Up ⭐(only team SPD Up at launch); modest damage, huge tempo value | Bard-archer with a bow strung like a lyre, teal light trailing arrows |
| ASH-RNG-R03 | **Silent Aldous** | Rare | Sniper | P (Pierce) | Single-shot burst: long-cooldown S2 with highest Rare single-hit damage; crit-fishing fantasy | Hooded marksman with a greatbow, one amber lens over a lost eye |
| ASH-RNG-E01 | **Yara Stormfletch** | Epic | AoE ranger | P | Rule-bender: arrow-storm AoE; ult carpets the field and Marks all survivors | Sky-caller with a recurve of storm-wood, arrows splitting into forks of light |
| ASH-RNG-E02 | **Dunstan Ironquill** | Epic | Anti-armor core | P (Pierce) | Armored-content specialist: damage scales with target DEF; deletes walls; chapter-3 answer key | Siege-engineer with a shoulder-mounted ballista-quill, blueprint scrolls |
| ASH-RNG-E03 | **Lys of the Last Light** | Epic | Finisher-enabler | P | Focus-fire engine: allies attacking her Marked target regain Surge; the ult-cycling battery | Choir-trained archer, halo-sight floating above her bow, gold-teal glow |
| ASH-RNG-L01 | **Vigil, the Unblinking** | Legendary | Hyper-carry | P (Pierce) | Ramping carry: consecutive hits on the same target stack +8% damage (max 10); ult fires 10 pierce bolts. Boss-melter | Sentinel in a watchtower-crest cloak, mechanical eye array, bow of pale light |
| ASH-RNG-L02 | **Freya Gatepiercer** | Legendary | Team enabler | P | Warping enabler: her Mark makes targets take Pierce sub-tag damage from *all* allies; ult = team instant-attack on the Marked | Huntress astride nothing — she stands on floating arrow-platforms, amber wind |

### 3.4 MAGE — violet/cyan, floating elements

| ID | Name | Rarity | Role | Dmg | Combat identity & skill fantasy | Visual concept |
|---|---|---|---|---|---|---|
| ASH-MAG-C01 | **Pip Emberling** | Common | AoE clearer | M (Arcane) | The wave-clear workhorse: every skill hits 2+ targets; best stamina-per-minute farmer ⭐(efficiency icon) | Apprentice with a crackling primer book, singed sleeves, floating sparks |
| ASH-MAG-C02 | **Old Maren** | Common | Slower | M (Arcane) | Tempo control: AoE SPD Down, single-target Bind; teaches control value | Village hedge-witch with a kettle-censer staff, cyan mist at her hem |
| ASH-MAG-R01 | **Castor Nullbrand** | Rare | Stripper | M (Arcane) | Anti-buff: S2 Strips 2 buffs from one enemy, ult Strips one from all ⭐(best budget Strip) | Inquisitor-scholar, brand-scarred palms, pages orbiting like knives |
| ASH-MAG-R02 | **Ione Glasswake** | Rare | Burst mage | M (Arcane) | Glass cannon: highest Rare AoE burst, self ATK Up ramp; dies if looked at (teaches frontline value) | Prodigy in mirror-shard robes, staff refracting violet light |
| ASH-MAG-R03 | **Tobias Wardlow** | Rare | Control mage | M (Arcane) | Lockdown: Bind + Stun toolkit on cooldowns; boss-interrupt budget pick | Locksmith-mage with keyring focus, chains of cyan glyphs |
| ASH-MAG-E01 | **Zerelda Voidquill** | Epic | Buff thief | M (Shadow) | Steal specialist (rare verb): takes enemy buffs for herself/team; unravels enrage bosses | Ink-drinker with quill-staff writing enemies' power out of the air, void-ink robes |
| ASH-MAG-E02 | **Ashvander the Third** | Epic | Nuker | M (Arcane) | Channel fantasy: S2 charges 1 round then detonates huge AoE; telegraphed power the team protects | Aged archmage in campaign-worn regalia, meteor glyphs assembling above him |
| ASH-MAG-E03 | **Liora Tidebinder** | Epic | Sustain mage | M (Arcane) | Rule-bender: mage-healer hybrid — damage skills leave "residue" that heals allies; solo-content queen | Sea-cloister mystic, water-halo rings, staff of drowned coral |
| ASH-MAG-L01 | **Ordan, Arc of Ruin** | Legendary | AoE apex | M (Arcane) | The screen-wipe: ult damages all enemies and reduces all their SPD; passive makes team AoEs Strip 1 buff. Raid-defining | Living conduit — armor split by light seams, seven orbiting rune-rings, violet storm |
| ASH-MAG-L02 | **Selune Mirrorveil** | Legendary | Control empress | M (Arcane) | Battlefield law: ult Binds all enemies 1 round + team Immunity; passive: enemy buffs have −1 round duration | Twin-mirrored sorceress — her reflection casts a half-second later, cyan-silver |

### 3.5 NECROMANCER — sickly green/bone white, minion shapes

| ID | Name | Rarity | Role | Dmg | Combat identity & skill fantasy | Visual concept |
|---|---|---|---|---|---|---|
| ASH-NEC-C01 | **Gravedigger Tam** | Common | Summoner baseline | P (via summons) | Simple summoner: raises 1 skeleton bruiser (physical); skeleton taunts when Tam is targeted ⭐(budget bodyguard engine) | Cheerful cemetery worker, shovel-staff, one loyal skeleton carrying his lunch |
| ASH-NEC-C02 | **Widow Isolde** | Common | Decay applier | M (Decay) | Anti-heal workhorse: stacks Decay; the answer to regenerating enemies ⭐(cheapest anti-heal) | Veiled mourner, censer dripping green smoke, bone-bead rosary |
| ASH-NEC-R01 | **Oswin Marrowcall** | Rare | Physical summoner | P | Twin skeleton bruisers (physical build); passive: summons gain his ATK buffs — the "undead warband" starter | Deserter-sergeant drilling skeleton soldiers, rusted officer's coat |
| ASH-NEC-R02 | **Nerys Palegrasp** | Rare | Magical summoner | M (Shadow) | Wraith summoner (magical build); wraiths are untargetable but fragile; backline-harass fantasy | Drowned-looking girl, wraiths trailing her like a bridal train |
| ASH-NEC-R03 | **Cantor Vhel** | Rare | Debuff necro | M (Decay) | DoT-spreader: S2 copies all DoTs on one enemy to adjacent enemies; bleed/decay comp glue | Plague-chanter with a grave-bell staff, notes visible as green script |
| ASH-NEC-E01 | **Morgause Ossuary** | Epic | Sacrifice engine | M (Shadow) | Spends summons: consume a skeleton → big burst + self Barrier; risk-reward resource loop | Bone-armored matriarch, ossuary backpack-shrine, candles of green flame |
| ASH-NEC-E02 | **Hollow-King Edric** | Epic | Summon commander | P | Summon-carry: his summons inherit 60% of his stats and act twice if he skips his own attack; the "general" fantasy | Dead king on a walking throne carried by four skeletal knights |
| ASH-NEC-E03 | **Sister Vesper** | Epic | Necro-support | M (Decay/Holy) | Rule-bender: heals allies by draining enemies (Decay lifesteal aura); sustain without a Healer slot | Excommunicated nun, split iconography — half halo, half green grave-light |
| ASH-NEC-L01 | **Mordrahl, Gravetide** | Legendary | Army apex | P/M (build) | The horde: maintains 2 summons whose damage type is chosen at battle start (physical bruisers or magical wraiths) — the build-choice flagship; ult = mass raise + all summons act | Tidal wave of bone crowned by a robed colossus, green riptide light |
| ASH-NEC-L02 | **Anguisette, Last Lament** | Legendary | Attrition apex | M (Decay) | Inevitable death: her Decay never expires and stacks; ult converts all enemy DoT stacks into instant damage. The long-fight closer | Song-made-flesh — a mourning diva whose dress dissolves into singing spirits |

### 3.6 HEALER — gold/soft white, rounded symmetry

| ID | Name | Rarity | Role | Dmg | Combat identity & skill fantasy | Visual concept |
|---|---|---|---|---|---|---|
| ASH-HLR-C01 | **Novice Bree** | Common | Single-target healer | M (Holy) | The reliable medic: big single heal, small HoT; simplest sustain ⭐(best heal-per-cost) | Nervous choir novice, oversized reliquary backpack, bandage sashes |
| ASH-HLR-C02 | **Father Ambrose** | Common | Cleanser | M (Holy) | Debuff answer: S2 Cleanses 2 debuffs team-wide ⭐(cheapest mass Cleanse — forever relevant) | Weary field-chaplain, thurible flail, faded gold vestments |
| ASH-HLR-R01 | **Sable Thornwick** | Rare | HoT specialist | M | Regen engine: stacking heal-over-time on the team; excels in long fights, weak to burst (teaches triage) | Herbalist with a living thorn-staff that blooms as she heals |
| ASH-HLR-R02 | **Cantrice Elowen** | Rare | Shield-healer | M (Holy) | Pre-emptive: Barriers instead of raw heals; passive converts overheal to Barrier | Choir cantor whose sung notes crystallize into gold shields |
| ASH-HLR-R03 | **Dr. Halvard Quist** | Rare | Combat medic | M | Hybrid: decent damage, heals strongest when an ally is under 40% (clutch fantasy); solo-content pick | Battlefield surgeon with syringe-gauntlet, lantern of white light |
| ASH-HLR-E01 | **Seraphel of the Ninth Choir** | Epic | Revive healer | M (Holy) | The safety net: revive (1/battle, 35% HP) + mass heal ult; co-op raid staple | Six-winged choir sister, wings made of hymn-script, gold halo array |
| ASH-HLR-E02 | **Warden Ysolt** | Epic | Tank-healer hybrid | M (Holy) | Rule-bender: front-row healer; heals scale off her maxHP; taunt-adjacent kit for tankless comps | Armored abbess with a crozier-halberd, shield-halo |
| ASH-HLR-E03 | **Lumen the Kindled** | Epic | Offensive healer | M (Holy) | Smiter: strong vs Undead trait (+25% Holy), heals team when she crits; the chapter-4 farm queen | Living candle-spirit in human shape, wax-gold robes, flame halo |
| ASH-HLR-L01 | **Aurelia Dawnvow** | Legendary | Sustain apex | M (Holy) | The heartbeat: passive team HoT aura; ult = full-team massive heal + Cleanse all + 1-round Immunity. The co-op anchor | Radiant high priestess, sunrise-gradient robes, halo like a rising sun over her back |
| ASH-HLR-L02 | **Requiem** | Legendary | Life-manipulator | M (Holy/Decay) | Rule-bender: redistributes HP — equalizes team HP percentages, converts enemy healing into team healing; anti-heal boss answer | Genderless psychopomp in half-gold half-ash robes, scales-of-life motif |

### 3.7 BERSERKER — blood orange/ash grey, oversized weapons

| ID | Name | Rarity | Role | Dmg | Combat identity & skill fantasy | Visual concept |
|---|---|---|---|---|---|---|
| ASH-BSK-C01 | **Brick** | Common | Rage baseline | P | Honest violence: gains Rage fast, spends nothing, just hits harder as fights go on; the budget bruiser ⭐(best gold-to-damage ratio) | Pit-fighter with a paving-hammer, taped fists, ash-grey wraps |
| ASH-BSK-C02 | **Hedda Ironjaw** | Common | Self-cost starter | P | Teaches the class deal: pays 5% HP for +50% skill damage; simple risk lever | Scarred lumberjill with a two-woman saw wielded solo, orange war-paint |
| ASH-BSK-R01 | **Cormac Redmist** | Rare | Executioner | P | Execute specialist: S2 deals triple damage below 25% HP targets; finisher discipline | Headsman in a rust-stained hood, greataxe with a bell on the haft |
| ASH-BSK-R02 | **Ulla Grindstone** | Rare | AoE bruiser | P | Spin-to-win: AoE cleave scaling with Rage stacks; farm-content favorite | Millwright swinging a chained millstone, sparks and grit aura |
| ASH-BSK-R03 | **Feral Jonas** | Rare | Lifesteal brawler | P | Rule-bender: sustain berserker — lifesteal scales with missing HP; solo-lane survivor | Half-Hollowed drifter, claw-gauntlets, eyes that glow when hurt |
| ASH-BSK-E01 | **Ragna Pyrelight** | Epic | Burst window | P | All-in: ult spends ALL Rage stacks for a nuke scaling per stack; the "bank and detonate" fantasy | Funeral-pyre knight, greatsword perpetually smoldering, ash cloak |
| ASH-BSK-E02 | **Torvald Chainbreak** | Epic | Anti-frontline | P | Wall-smasher: bonus damage vs Barriers/Armored, his hits reduce target DEF; opens fights for assassins | Escaped slave-gladiator, broken chains as flails, brand-scarred back |
| ASH-BSK-E03 | **Maeve Halfdeath** | Epic | Edge-rider | P | Lives at 1: cannot drop below 1 HP once per battle (2-round window of +100% ATK); the highlight-reel unit | Pale duelist who fights bleeding out beautifully — orange thread of life visible around her |
| ASH-BSK-L01 | **Kargh, the Unfinished** | Legendary | Rage apex | P | Perpetual motion: killing blows grant an immediate extra S1 and refund 20 Surge; snowball incarnate; ult damage scales with his missing HP | Hollowed colossus mid-transformation — half man, half something the Gate started building |
| ASH-BSK-L02 | **Branwen Oathbreaker** | Legendary | Team berserker | P | Warping: her Rage stacks apply team-wide at half value (everyone gets angrier); ult = team instant S1 barrage. The tempo-comp flagship | Fallen knight-commander, snapped oath-blade reforged with orange light, torn banner cloak |

## 4. Roster Balance Notes

- **Per-class damage-type spread** is intentional: Tanks include one magical option (Vashti, Kaela), Necromancers split P/M by summon build, Healers get Holy offense. No class is mono-answer.
- **Verb coverage audit (must stay true as roster grows):** Taunt ×(all tanks), Cleanse ×4 (C02 Healer cheapest), Strip ×4 (R Mirelle/Castor cheapest), Armor Break ×3 (C Fletch cheapest), Mark ×4, team SPD Up ×1 (Rare Brenna — deliberate scarcity), Revive ×2 (Epic+, 1/battle cap).
- **Launch meta targets** (what we *want* the community to discover): Bleed comp (C01/R03/E01/L02 Assassin + Cantor Vhel), Summon wall comp (Necro ×2 + Morholt), Budget speed-tempo comp (Brenna + Branwen), Holy anti-undead farm comp (ch.4).
- **Tuning guardrail:** in internal sims, a maxed all-Common team must clear campaign stage 3-10; a maxed all-Rare team must clear 4-10. If not, buff the Commons — never nerf campaign.

## 5. Example Full Kit (character kit template — use for all 70 during production)

```yaml
id: ASH-ASN-L01
name: The Hollow Smile
class: Assassin
rarity: Legendary
faction: Hollowed
row: Back
damage_root: Physical
subtags: [Bleed]
base_stats_lv1: { hp: 980, atk: 172, def: 88, spd: 112 }
growth_curve: legendary_std   # doc 09 §1
skills:
  S1_basic:
    name: Smilecut
    target: single_enemy
    power: 110%ATK
    effect: "Apply 1 Bleed (2 rounds). +30% damage vs targets below 50% HP."
  S2_core:
    name: Between Heartbeats
    cooldown: 3
    target: single_enemy
    power: 190%ATK
    effect: "Ignore Stealth/Barrier. If target has 3+ Bleed stacks, detonate all stacks instantly."
  S3_ultimate:
    name: The Last Thing You Never Saw
    surge_cost: 60
    target: single_enemy
    power: 320%ATK
    effect: "Executes targets below 25% HP (bosses: deals +40% instead). On kill: gain Stealth 1 round."
    cutin: full-screen, mask-crack VFX, doc 11 §6
  S4_passive:
    name: Encore
    effect: "Once per round: killing an enemy resets The Hollow Smile's turn."
ai_ult_priority: { weight: 90, condition: "target_hp_pct < 40" }
ascension_nodes: [A1: "+10% CritDmg", A2: "S2 cd 3→2", A3: "Execute threshold 25→30%"]  # doc 09 §3
dupes: legendary_std          # doc 09 §4
voice_tags: [whisper, amused, hollow]
art_prompt_ref: HF-CHAR-ASN-L01   # doc 11 templates
```
