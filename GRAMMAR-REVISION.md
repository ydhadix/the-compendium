# Effect Grammar Revision — Plan

Settled 2026-08-15. Replaces the volition/timing rules that have reversed four times during the porting work.

**Why this one should hold:** the previous rules were derived outward from whatever examples were in front of us, so every new permutation arrived as an exception. This grammar is derived from the dimensions an effect statement actually has, with one rule enforced throughout — **one dimension, one slot; no slot signals a second dimension.** Every reversal so far traces to a slot doing two jobs.

---

## 1. The grammar

An effect statement encodes four things, each in its own slot.

| Slot | Carries | Form | Absence means |
|---|---|---|---|
| **Cost line** | the holder's volition, its cost, its rate limit | an inline **bold lead-in** — `**<cost>:** <effect>` (see §1.10) | nobody chose this — the effect is automatic |
| **Occasion** | when it fires; for mandatory effects, also *how often* | leading `Before <event>,` / `After <event>,` | standing property, always in force |
| **Effect** | the state change, on whomever it lands | plain declarative; may state a Charge depleting | — |
| **Other's volition** | a *second* decision, by a creature who isn't the holder | `<that creature> can <verb>` | they get no say |

### 1.1 Volition is structural, never lexical

The holder's volition is carried by the **presence of an act line** and nothing else. `can` does not appear in an effect resolution describing what the holder does.

This is what dissolves the collision that recurred three times (Lucky, Protection, Sap/Slow): `can` marks its grammatical subject as the chooser, but the chooser is often not the subject. Moving volition out of the sentence frees the effect clause to take whatever subject the mechanic needs.

`can` survives for exactly one job — a **different creature's** decision, where the decider *is* the subject and no collision is possible: `A shackled creature can make an Athletics Check.`

**This marker is deterministic, not defaulted.** `can` never appears for the holder, so its absence is never a signal. Every prior attempt failed because the marker was present "usually," which made its absence meaningful.

### 1.2 Cap is not a dimension

For a **mandatory** effect, frequency is fully determined by the trigger. It belongs in the occasion, never in a subtitle:

> ✓ `After each of your Turns starts, …`
> ✗ `1 use per Turn` on a mandatory effect

`use` is a volitional noun — you cannot be *using* something you had no say in. A use limit is therefore only ever a constraint on how many times the holder may elect, and lives on the act line.

### 1.3 Cost does not imply volition

A resource can deplete with nobody choosing. What requires an agent is *use*, not expenditure — so the presence of a resource cost does not by itself mark an effect elective.

**Resource unit words are not volition markers.** `Charges` is a mechanical keyword meaning a **replenishing item resource**, and other mechanics reference expending or replenishing the Charges *of other items*. Repurposing it to signal optionality would change those mechanics. Unit words stay governed by [vocab-limited-uses](.claude/style-appendix/vocabulary.md) and its replenishment tiers (Type 1–4).

The two axes are scoped apart instead:

| | Carries | Volition? |
|---|---|---|
| **Pool line** (item-level) | how much resource exists, and how it replenishes | none implied |
| **Action Cost** | what is spent to invoke | elective — because it is an Action Cost, not because of the unit word |
| **Mandatory effect** | no cost line at all; states any depletion in the body | automatic |

**A mandatory effect carries no cost line.** Splitting volition across clauses of the subtitle — an action type meaning elective, a bare resource meaning automatic — hides the distinction from the player: nothing in `1 use` tells a reader that the missing action type is what makes the effect mandatory. The rule would exist without being readable.

The body is also the **only** place a conditional expenditure can be stated. Nine Lives Stealer spends a use only when the target actually dies, which no cost line can express:

```
| Fail | The target dies, and you expend **1** use. |
```

So the pool is linked to its spender by the effect text, which is where a reader is already looking.

### 1.4 Scope — standing capabilities are outside these rules

A **standing capability** widens what you're permitted to do (`You can wield a Medium Shield as a Hammer`, `You can cast those Spells using Intelligence as your Spellcasting Ability`). It sits outside action timing entirely.

**Test:** if it isn't an action option, and it wouldn't make more sense phrased as one, it isn't governed by these rules. Ordinary English `can` is correct and stays.

Likewise **character-management procedures** — `You can take this feat more than once`, `Whenever you level up, you can replace one of these Cantrips`. Not in-play effects; `can` stays. The exposition boundary is a **content test, not a location test** — this occurs inside feat and class cards, not only on rules pages.

### 1.5 Rests are not costs

**Reversed 2026-08-16.** An earlier draft of this section made `Short Rest` / `Long Rest` valid cost lines. They are not: a rest is downtime, not action economy, so it never belonged in the cost slot. `temp-metadata`'s original ban was correct.

A rest-gated effect states the rest as an occasion clause in the body:

```
##### Replenishing Meal
After you finish a Short Rest, you can choose up to **4 + PB** creatures that used one or more Hit Dice to heal during this rest.
```

Use `After`, not `Whenever` — [phrase-trigger-words] scopes `Whenever` to meta-level events (leveling up, Proficiency Bonus increasing), never play events.

### 1.6 Shared pools are named resources

When several acts draw on one pool, the pool is **named**, declared once on the parent, and each act line spends from it by name — the Channel Divinity pattern (`Magic Action, 1 Channel Divinity use`).

```
### Lucky
**PB** Luck uses per Long Rest
{ .subtitle }

#### Advantage
Free Action, 1 Luck use
{ .subtitle }
```

### 1.7 Distinct options of an action go in a table

When one act offers a menu of named options, the options are **table rows, not sub-headings**. This keeps h5 reserved for action initiation and stops the option names from occupying the level that marks an action.

```
##### Use Technique
Free Action, 1 use per Attack
{ .subtitle }

You use one Weapon Technique you know.

| Technique | |
|---|---|
| Cleave | **1 use per Turn.** After you hit with a Cleave weapon, you make a Melee Attack … |
| Graze  | After you miss with a Graze weapon, you deal damage to the target … |
```

The table folds its section name into the first header cell, matching the stat block tables. An option's own restriction leads its cell as a bold lead-in (`**1 use per Turn.**`) — the same within-cell device `temp-creature` uses for subsections.

**Unnamed options stay as bullets** — a table needs a first-column label, and inventing names for options that don't have them collides with §1.9's rule against manufacturing names.

**Consequence:** a non-action sub-block beneath an h4 skips h5 and takes h6, since h5 would falsely mark it as an action.

### 1.8 `Free Action` is an act, not a cost

As a cost it is incoherent — a spend of nothing. As an act it is exact: *the holder does something, and it costs nothing.* Its sole job is declaring that the holder acts. This is why it was the form abused by all 17 false action lines while `Bonus Action` and `Reaction` were not — real action types carry economy and resist misuse.

### 1.10 The cost line is an inline bold lead-in

Settled 2026-08-16, replacing the `{ .subtitle }` act line.

```
##### Wither
**Free Action; 1 Charge:** Before you deal damage with this weapon, you add **2d10** Necrotic Damage.
```

**Why inline.** A subtitle can be skipped — the eye jumps the blank line and reads the effect without ever reading the cost. Inline, the cost is in the sentence you must read. That fixes the problem in the **source**, so it survives raw markdown, print, and any path where CSS never runs. (The `.subtitle` class renders at `opacity: 0.65` italic — the faintest element on the card was carrying the most load-bearing information.)

**Bold is emphasis, and cost warrants it.** Bold already marks numbers and formulas so they can be found while scanning (`**60**` vs `**120**` is a common table confusion). A cost is the same kind of scan target. **Bold at the start of a line means a cost to pay.**

**The trigger stays in prose.** Only the cost goes in the bold — never the occasion. Triggers run to 15–24 words and are not uniform; costs are 2–6 words and always parse the same way. This follows Magic's split between activation costs and triggered abilities.

- ✓ `**Reaction:** Before a creature within Reach is hit with an Attack, you add your Shield's bonus…`
- ✗ `**Reaction, before a creature within Reach is hit with an Attack:** you add…`

**Components are separated by semicolons**, since a component may contain its own comma: `**Utilize Action; 1 Healer's Kit use; 1 of the target's Hit Dice:**`.

**Cost lines are formulas** — `PB`, `DEX`, `CHA` and other shorthands are used as they are in any other formula. *(Expanding the shorthand set to cover Spellcasting Ability and similar is a separate open task.)*

**Absence is the automatic marker.** No bold lead-in means nobody chose it. Dagger of Venom shows both in one card — `**Bonus Action; Once per Day:**` on Coat Weapon, nothing on Envenom.

**What stays in `{ .subtitle }`.** Everything *static and descriptive*: flavor caption, item type line, Prerequisite, and the resource pool line. Everything *transactional* moves to the bold lead-in. This resolves the class's former four-role overload.

### 1.11 Cost vocabulary — rate limits vs pool draws

| Kind | Form |
|---|---|
| Rate limit | `Once per Turn` · `Once per Day` · `3 times per Day` |
| Rate limit, per option | `Once each per Day` — **`each` sits early**, not trailing; it is semantically load-bearing and easy to miss at the end |
| Pool draw | `1 Charge` · `1 Luck use` · `1 Healer's Kit use` |

This retires `use` as a word doing two jobs. A **rate limit** caps frequency; a **pool draw** spends a countable resource. `Charges` keeps its `vocab-limited-uses` meaning untouched (§1.3).

### 1.12 Scope of a cost line

A cost line is scoped by its **heading**, and headings divide scope:

- An **h5 action** is its own visually marked card; the cost covers everything in it — prose, outcome tables, trailing sentences.
- A **dependent h6 action** is the dividing line; it carries its own cost.
- **In a table, a bold lead-in is scoped to its cell** (Technique Training's per-technique restrictions). This is the same convention at a smaller scope, not a separate device.
- **A feature or item with a single effect needs no heading at all** — one cost line scopes the whole card. `### Savage` + `**Free Action; Once per Turn:** After you hit…` is complete.

Headings appear when costed effects coexist with other costed or uncosted effects. Uncosted effects coexist naturally.

**An action granted to another creature carries its grant inside its own block**, above the cost line — not as a lead-in sentence before the heading:

```
###### Revert Portal
Any creature holding the portal's key can attempt to end this effect.

**Magic Action:** The creature makes an Arcana Check _(DC **20**)_.
```

`A creature … can take the following Action.` is a **forward reference** — it points at a heading by position, so it breaks silently when content moves and forces the reader to look ahead before knowing who the grant is for. Moving it inside makes the block self-contained: *who may act*, then *what it costs*, then *what happens*.

The grant sentence is a standing capability (§1.4), so it correctly keeps `can`. It sits inside the heading's scope but **outside the cost line's** — it states who is permitted, not part of what the action does.

**Only a grant statement may precede a cost line.** Any other prose in that position pushes the cost down the block and weakens the line-initial bold as a scan target.

### 1.13 Grants name their source when an agent acts

Settled 2026-08-16. Restores a visible `can` to prose by giving every effect a form that can carry it.

**The collision this fixes.** `can` marks its grammatical subject as the chooser. Where the elector isn't the recipient (Lucky, Protection, Sap, Slow), no placement of `can` said the right thing — so `can` couldn't be used at all, and volition had to move to the cost line. Naming the source restores the form.

**This is not a new pattern.** `phrase-condition` already mandates source-subject for conditions — *"the source is the grammatical subject"* — used 41 times (`you sicken the target`, `the mummy frightens the target`). The collision only ever hit **grants**, because conditions already had a source-subject form to hang `can` on. This closes the gap.

**Agent vs possession.**

| Source | Subject | Example |
|---|---|---|
| An acting creature | the creature | `you can give the target Disadvantage on Attack Rolls` |
| An environmental hazard | the hazard | `The lava deals **6d10** Fire Damage.` |
| A worn item, tool, or weapon | stays implicit — recipient/trait-subject | `Your Armor Class increases by **2**` |
| A state or area with no agent | recipient/trait-subject | condition-page effects, area properties |

`phrase-grant`'s ban on naming a **concrete inanimate source** is untouched — it never covered creatures. Trace a trap or item back to the agent that set or used it.

**Verbs.** `give` for categorical grants where no verb exists (Advantage, tiers); transitive `increase`/`decrease` for numeric. `phrase-condition`'s ban on `<Source> gives <target> <Name>` stays — conditions have real verbs.

**Saves: `force`, narrowly scoped.** An effect that is **(1) optional and (2) entirely contingent on a Saving Throw** gives the holder a verb so `can` has somewhere to attach:

```
**Bonus Action:** You can force one creature within **30** feet to make a Fortitude Save _(DC **8 + INT, WIS, or CHA + PB**)_.
```

**This is not a global reform of Save phrasing.** The corpus holds **282 Save declarations** — 168 in spells, 59 in items, 30 in the bestiary — plus 35 recurring Saves. Converting them all would add four words of boilerplate to every damaging spell (`You force each creature in a **20**-foot radius Sphere to make a Reflex Save`) while saying nothing the card didn't already say, since casting *is* the election. And Saves with no acting agent — area effects, recurring Saves, environmental hazards — keep recipient-subject under §1.13's agent/state boundary regardless.

Both conditions must hold. Only ~3 blocks per domain qualify.

`force` here is an **active, source-subject action verb** and must not be confused with `phrase-optionality`'s ban on `forced to`, which targets the *passive* construction used to mark a mandatory effect (`the target is forced to make a Save`). Different subject, different job.

Where a damage category is already the subject, it takes the verb directly: `Critical Hits with this weapon deal an additional **14** Slashing Damage and give the target **1** Exhaustion level.`

### 1.14 Roll-recipient vs creature-recipient

The two forms are inter-derivable, because neither exists without the other — a roll has no existence apart from its maker, and a modifier on a creature applies to the rolls it makes:

- roll-recipient extends to **any creature making that roll** — `give Attacks against the target Disadvantage` = *give any creature that attacks the target Disadvantage on the Attack Roll*
- creature-recipient extends to **any roll that creature makes** — `give the target Disadvantage on Attack Rolls` = *give the target's Attack Rolls Disadvantage*

**Choose by whether a possessor can be named:**

| Condition | Form |
|---|---|
| A single creature is the only recipient | **creature-recipient** — `you can give the target Disadvantage on Attack Rolls` |
| No specific creature can be named as possessor | **roll-recipient** — `Attack Rolls against you gain Disadvantage` |

**Conditions on the recipient trail the grant.** A recipient carrying qualifiers obfuscates the effect when it sits before the thing granted:

- ✓ `You can give the target Disadvantage on Attack Rolls against anything within your Reach.`
- ✗ `You can give the target's Attack Rolls against anything within your Reach Disadvantage.`

This also resolves long recipient phrases: Guiding Bolt's `the next creature to attack the target` names no specific creature, so it takes roll-recipient — `you give the next Attack Roll against the target Advantage`.

**Corpus split: 23 roll-recipient, 32 creature-recipient.** The 23 revert to their pre-2026-08-14 form; that sweep established possessor-subject correctly but over-applied it to cases with no nameable possessor.

### 1.9 Headings carry hierarchy only

Heading level is a document-structure device and signals nothing about volition. The h5/h6 convention (h6 for an act gated by a parent act) is pure hierarchy and is unchanged. The spell card template needs no revision.

**One-way invariant: an act line requires a header** to attach to. The converse does not hold — a header with no act line is fine, and means structural scaffolding or a named mandatory effect.

**Prefer fewer headings.** Do not invent names for subfeatures that don't need them: invented names collide, and they dilute the pool of mechanically significant names available when one is genuinely needed. A name-reference between effects on the same card is usually a symptom of imprecise phrasing — state the condition instead. (Dagger of Venom's "until its Envenom damage is dealt" dissolved into "until you hit a creature with this weapon" once the trigger was stated precisely.)

---

## 2. What this reverses

Stated plainly, because these are live rules that content already follows.

| Rule | Was | Becomes |
|---|---|---|
| `phrase-optionality` | `can` marks optional; its absence marks mandatory | the act line marks volition; `can` leaves holder resolutions entirely |
| `phrase-bonus-damage` | canonical form is `Before you deal damage, you can add **XdY**` | `can` drops when an act line is present |
| `temp-creature` | "A Reaction states what the creature **can** do" | Reactions lose `can` — the `\| Reactions \|` table *is* the act declaration |
| Item resource pools | `uses` used for both elective and automatic depletion | `uses` for elective only; `Charges` for automatic |

**`temp-creature`'s Reaction rule was set earlier in this same conversation.** It reverses here. That is the pattern the revision is meant to end, and the difference is that this reversal is derived from the dimension model rather than from the next counterexample — but it should be watched, not assumed.

**Not affected:** `phrase-continuous-damage` (already correct — mandatory every-instance effects are static with no trigger), `phrase-grant` (numeric vs categorical subject rules are orthogonal to volition), possessor-subject for Advantage/Disadvantage (the objection to it was the chooser≠subject collision, which this grammar dissolves).

---

## 3. Open decisions

These need answers, but not before Stage 0.

1. **Nested optionality — resolved 2026-08-15, but the least-tested part of the design.**

   `can` is scoped to **inside an act block only**, where it marks a decision the holder may decline while still having spent the act. The primary effect of an act block is always mandatory — invoking the act is what makes it happen.

   **Invariant: `can` never appears outside an act block.** A mandatory effect has no act line and therefore contains no `can` at all, so the two contexts never overlap and neither marker's absence is ambiguous.

   Two shapes, by whether the option modifies a value:

   - **Numerical** — modify the value stated above it; no timing clause. `You heal a creature within Reach by **2d8**.  You can expend a Hit Die to increase the healing by **1d8**.` This produces one instance rather than two. Requires adjacency (the definite `the healing` must point at the immediately preceding statement), and requires a cost — a free numerical option isn't a real choice and should be folded into the primary.
   - **Non-numerical** — state timing only when the sequence is genuine. `Before you deal damage with a Melee Attack, you add **2d6** Force Damage.  After you do, you can knock the target Prone.`

   **Hazard:** never add a timing clause for clarity alone. `After you do` on an effect that isn't genuinely sequenced splits one instance into two — the bug `phrase-bonus-damage` bans for damage, which cost three staff cards a fix on 2026-08-14, and which applies equally to healing and anything else measured per instance.

   **Watch item:** `can` now does two jobs — sub-decisions inside act blocks, and another creature's decision (`A shackled creature can make an Athletics Check`). They don't collide (one is scoped inside an act block, the other names a different subject), but one word doing two jobs is the pattern that has bitten us repeatedly. Verify in the pilot.
2. **In-cell outcome tables — criterion RESOLVED 2026-08-16; sweep pending.** Command Words will take the §1.7 shape (h5 act line + option table), which forces outcomes into table cells. Two tiers:

   - **One outcome carries an effect** (the other — a succeeded Save, a missed Attack, a failed Check — does nothing): stay inline, `phrase-inline-outcome`'s semicolon chain.
     `makes a Fortitude Save _(DC **13**)_; on a failure, the ghoul paralyzes the target until the end of its next Turn.`
   - **Both outcomes carry an effect**: expand to labeled lines.
     `makes a Reflex Save _(DC **18**)_.<br>**Fail.** You deal **7d6** Bludgeoning Damage and knock the target Prone.<br>**Success.** You deal half as much damage.`

   **The rule of thumb: if a second semicolon is needed, expand.** `<br>` is already established in the corpus (45 uses, class tables and hub pages); only its use for outcomes is new, and the labeled form appears nowhere yet.

   **This reverses `phrase-inline-outcome`'s half-damage carve-out** (canonized 2026-08-14), which kept `, or half as much on a success.` as a trailing idiom rather than a second clause. Half damage *is* a second outcome with an effect, so it expands.

   **Measured scope — 11 of 47 in-cell outcomes expand; 36 stay inline:**

   | | count |
   |---|---|
   | two semicolon clauses | 2 |
   | half-damage trailing idiom | 9 |
   | single outcome (unchanged) | 36 |

   **The sweep lands in the bestiary, not items** — 23 of the 47 are creature stat blocks, 12 spells, 3 rules pages, 1 item. So the criterion is settled for Stage 2's Command Words, but the conversion work falls in Stage 5.


3. **Non-damage riders on a trigger — RESOLVED 2026-08-15.** Crusher, Slasher, and Piercer's Enhanced Criticals are all **mandatory triggers taking the same form**, not the `phrase-continuous-damage` static form. The line: the static form (`Critical Hits with this weapon deal an additional **7**`) is for **weapon properties**, where the weapon is the subject; a **character feature** keeps the trigger form, where you are. This is why the three swords converted to static on 2026-08-14 and these did not.

4. **Technique Training restructure — RESOLVED 2026-08-15.** Rebuilt on the §1.7 option-table form: one `##### Use Technique` act block carrying `Free Action, 1 use per Attack`, with the nine techniques as table rows. Fixes both original defects — Nick no longer reads mandatory, and the one-per-Attack rule is stated rather than implied.

5. **Compelled acts.** Does anything force the holder to spend an action? If so, an act line would wrongly imply choice. No known instance; flag if one appears.

---

## 4. Staging

Rules first, then content by domain. **Each stage completes before the next begins** — running two at once is what produced the current mess.

### Stage 0 — Cement the rules · **recurring, not one-time**

Each stage surfaces rules worth recording, so the appendix is updated **at the close of every stage**, not once at the start. Running the pilot before Stage 0 was correct — §1.4–§1.7 and §1.10–§1.12 all came out of it, and cementing first would have meant rewriting twice.

**Done 2026-08-15** (post-pilot): `phrase-optionality` rewritten around structural volition and the four `can` positions; `temp-metadata` gained rest costs, shared pools, and the ban on splitting volition across cost clauses; `temp-feature` gained heading levels and option tables; `phrase-bonus-damage` and `phrase-inline-outcome` updated; `temp-creature`'s Reaction note reversed; `vocab-limited-uses` annotated.

**Pending:** the §1.10–§1.12 inline cost form is recorded here but **not yet in the appendix** — `temp-metadata` still describes the `{ .subtitle }` act line.

### Stage 1 — Pilot: feats and fighting styles · **grammar pass COMPLETE, presentation pass PENDING**

58 files converted 2026-08-15. Zero exceptions generated; every collision case resolved with no edit. Full results in [GRAMMAR-PILOT-WORKSHEET.md](GRAMMAR-PILOT-WORKSHEET.md).

**Re-opened 2026-08-16** to serve as the testing ground for the §1.10 inline cost form. The domain's 65 act-line subtitles convert to bold lead-ins, single-effect feats lose their headings, and rate limits convert per §1.11.

### Stage 2 — Items · **COMPLETE 2026-08-17**

**338 cost blocks** converted across `docs/item/` — all gear subdirectories, every magic rarity, `armor.md`, and `weapon.md`.  Zero act-line subtitles, zero old rate vocabulary, zero container lines.

Beyond the conversion, the section produced substantial rule work, all recorded in the appendix:

- **Potions and Poisons merged** into one type with `Ingested` / `Contact` / `Injury` delivery types; delivery rules live on the potion index, cards state one effect on `the target`.
- **Physical units** (`34 cards`, `1d6 + 3 beads`) as a stylistic alternative to `uses`; compound units defer back.
- **Dismissal tiers** — free, repeat-the-act, or a distinct act; items inherit no default dismissal.
- **`Choosing to Fail`** added to `dice/index.md` — an undocumented rule Shield of Protectors depended on.
- **Damage-type replacement** is a standing capability, not a per-instance election.
- **`temp-infusion` rewritten** — the Command Word dispatcher is an h5 Action with an option table, and a mandatory triggered effect carries **no** cost line.  Its previous rule requiring `Free Action` on every triggered effect is what produced the 17 false action lines.
- **§1.7 has no exceptions.**  Two items resisted the option table; both yielded to factoring shared content out rather than to an exemption.

### Stage 2 — Magic items

Largest and worst-affected domain. Batch by rarity tier.

### Stage 3 — Class features · Stage 4 — Spells · Stage 5 — Creature stat blocks

Stat blocks last: different structure (tables rather than headers+subtitles), and the Reaction reversal lands there.

### Stage 6 — Rules pages

Mostly exposition, which is **out of scope** — the ~891 `can`s in explanatory prose (`You can create your own background`) are not effect resolutions. Confirm the boundary holds; expect few edits.

---

## 5. Correctness mechanism

**The classification cannot be derived from the text.** Whether an effect *should* be volitional or mandatory is a design fact about the mechanic, and the existing corpus is known-unreliable in both directions — effects that should be mandatory are marked optional and vice versa. Counting what the corpus currently does is not evidence.

So every stage runs in three passes:

1. **Classify** — for each effect block: current form, proposed classification (volitional / mandatory), proposed new form, and an explicit **uncertainty flag**. No edits.
2. **Review** — the worksheet goes to Taj. Every flagged item gets a ruling; unflagged items are spot-checked. Corrections feed back before anything is written.
3. **Apply** — mechanical once classification is settled, then `genAll.py` and greps.

Rules for the classify pass:
- **Never infer intent from the current markup.** A `Free Action` line is not evidence the effect is elective; a missing `can` is not evidence it is mandatory.
- **Flag anything where the mechanic's intent isn't unambiguous from what the effect does.** Over-flagging is cheap; a wrong silent classification is not.
- **Do not batch semantic judgment for speed.** Mechanical substitution can be scripted; classification cannot.

## 6. Verification

Per stage:

- `python3 scripts/genAll.py` exits clean.
- No `can` in a holder resolution under an act line: `grep -n "can" <domain>` reviewed by hand.
- No act line without a header; no act line on a mandatory effect.
- No `uses` on a mandatory effect; no `1 use per Turn` where an occasion belongs.
- Spot-render the domain's index page.
