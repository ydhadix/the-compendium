# Stage 1 Pilot — Feats · COMPLETE

Domain: `docs/character/feat/` — 94 files. **58 files changed.** `genAll.py` clean.

> **Coverage correction.** My first worksheet claimed the domain was fully read. It wasn't — I had read `_initiate`, `_expert`, `_ancestry`, `_origin`, and `_general`, but not `_master` (20 files), `dragonmark.md`, or `epic/index.md`. Caught by the post-apply audit. All are now read and converted. The claim was wrong when made.

---

## Verdict: the grammar holds

Every `can` remaining in the domain is accounted for by one of the four sanctioned positions, with **one** block outstanding on a pre-existing open decision.

| Position | Count | Example |
|---|---|---|
| Capability grant (§1.4) | 26 | `You can wield a Medium Shield as a Hammer` |
| Exposition / character management (§1.4) | 19 | `You can take this feat more than once` |
| Nested option inside an act block (§3.1) | 2 | Cloudy Escape, Riposte |
| Another creature's decision | 3 | `A creature can Utilize to eat a treat` |
| `can't` (negation, not volition) | 4 | `You can't swap if you or the target are Incapacitated` |

**Zero act blocks retain `can` on their primary effect.**

### The design's central claim, validated

All four chooser≠subject collision cases came out correct **with no edit**: Protection, Lucky's Disadvantage, Sap, Slow. Moving volition out of the effect sentence dissolved them, as predicted.

The nested-option form validated against two features neither of us had looked at when designing it — Cloudy Escape (`After that attack, you can teleport up to **30** feet`) and Fence Master's Riposte (`If that Attack misses, you can attack the attacker`). Both are genuine sequences, so both keep `can` correctly.

---

## What was applied (49 files)

- **`can` dropped from the primary effect of an act block** — 48 blocks across feats, all three Fighting Style tiers, and Dragonmarks.
- **Rest act lines (§1.5)** — 6 blocks converted from `After a Short/Long Rest, you can …` to a `Short Rest` / `Long Rest` act line with the occasion clause dropped: Chef ×2, Inspiring Leader, Planar Wanderer, Musician, Technician, Integrated Protection.
- **Act lines added where missing** — Alert/Initiative Swap and Healer/Healing Reroll (`Free Action`); Warcasting Master ×2 (`Free Action`, following the Searing Ignition / Stone Throw precedent for attack-replacement).
- **Shared pool (§1.6)** — Lucky now declares `**PB** Luck uses per Long Rest` with each act line spending `1 Luck use`, per the Channel Divinity pattern.

## Resolved 2026-08-15 (all open items closed)

- **§3.2 Enhanced Criticals** — ruled *mandatory triggers, all the same form*, not the `phrase-continuous-damage` static form. Crusher and Slasher were already correct; Piercer lost its `can`. The static form stays for **weapon** properties (Weapon of Smiting et al., where the weapon is the subject); these are **character** features, where you are.
- **§3.3 Technique Training** — restructured on the magic-item command-word shape. A governing block carries the general cost and the one-per-Attack timing; each technique carries its own trigger, effect, and usage restriction. Fixes both defects Taj identified: Nick no longer reads mandatory, and the one-per-Attack rule is now stated.
- **`dragonmark`/Slippery** — became `Free Action, 5 feet of movement`. No Move Action equivalent exists, so this is the closest form without inventing one. First use of movement as a cost.
- **`healer`/Battle Medic** — the expended resource belongs to *another creature*. Kept in the subtitle for parity: `Utilize Action, 1 Healer's Kit use, 1 of the target's Hit Dice`.

## Option tables (2026-08-15)

Technique Training's nine techniques became **table rows** rather than sub-headings, per §1.7. This resolved the h4/h5 inconsistency the first restructure introduced: the governing block is now `##### Use Technique` like every other act block in the domain, and the technique names no longer occupy h5 while not being actions.

Final heading state: **65 act blocks at h5**, 1 at h6 (`planar-wanderer`/Revert Portal, correctly gated by Portal Cracker), 3 at h3 (card-level act lines on single-action feats: Lucky, Protection, Savage).

**Incidental defects — all fixed:** `blind-fighting` + `skulker` (`have`→`gain`), `technique-training`/Nick (passive), `pugilist` (passive), `opportunity-master`/Sentinel (passive), `healer`/Battle Medic (bare imperative).

---

## Stage 2 readiness

The grammar generated **no exceptions** in this domain once §1.4–§1.6 were added. Magic items are next and are the worst-affected domain; the categories to expect there are capability grants (very common on items) and the `use`/`Charge` split, which this domain barely exercised.
