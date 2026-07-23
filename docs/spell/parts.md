# Parts of a Spell
Every Spell is built from the same set of parts, the details that define what it does, how it's cast, and how far and how long its magic reaches.
{ .subtitle }

| Parts of a Spell | Description |
|---|---|
| [Spell Level](#spell-level) | The Spell's rank, and the Slot it takes to cast. |
| [Class List](#class-list) | The classes that can prepare the Spell. |
| [School of Magic](#school-of-magic) | The family of magic the Spell belongs to. |
| [Casting Time](#casting-time) | How long the Spell takes to cast. |
| [Components](#components) | What a caster must supply to cast it. |
| [Range](../rules/position/target.md#range) | How far the Spell's effect can reach. |
| [Targets](../rules/position/target.md) | What the Spell can be cast upon; sometimes including an Area. |
| [Duration](#duration) | How long the Spell's effect lasts. |
| [Concentration](#concentration) | Focus a caster must hold to sustain a Spell. |

## Spell Level
A Level **0** Spell is a Cantrip. Cantrips are always ready and never expend a [Spell Slot](casting.md#spell-slots).

Higher-Level Spells are more powerful and take larger Spell Slots to cast. A Spell can be [Upcast](casting.md#upcasting) with a Spell Slot above its Level for a stronger effect.

## Class List
Each class with a Spellcasting feature has its own Spell List, and a Spell belongs to every class whose List includes it. You can prepare a Spell from a class only if the Spell is on that class's Spell List.

A Spell you Learn from a class feature is treated as though it were on that class's Spell List, even if it isn't listed there.

## School of Magic
A School groups Spells by what they tend to do and lets other rules reference them together, but the Schools have no rules of their own. Most Spells belong to a single School, though some belong to more than one.

| School | Typical Effects |
|---|---|
| Abjuration | prevent or reverse harmful effects |
| Conjuration | transport creatures or objects |
| Divination | reveal information |
| Enchantment | influence minds |
| Evocation | channel energy into destructive effects |
| Illusion | deceive the mind or senses |
| Necromancy | manipulate life and death |
| Transmutation | transform creatures or objects |

## Casting Time
Casting a Spell usually takes the Magic Action, but some Spells take a Bonus Action, a Reaction, or longer.

### Triggered Spells
Every Spell with a Reaction Casting Time, and some Spells with a Bonus Action Casting Time, define a trigger that must occur before you can cast the Spell.

### Rituals
A Spell with a Ritual Casting Time can be cast as normal or cast as a Ritual. Casting it as a Ritual takes **10** minutes longer and expends no [Spell Slot](casting.md#casting-without-a-slot).

### Long Casting Times
Some Spells — including Spells cast as a Ritual — take **1** minute or longer to cast. While casting a Spell this way, you must maintain [Concentration](#concentration) and take the Magic Action on each of your Turns to keep casting it. If your Concentration breaks or you can't take the Magic Action, the Spell fails, but you don't expend a Spell Slot.

## Components
Spell Components are the spoken words, gestures, and materials a caster must supply to set a Spell's magic in motion. If you can't provide one or more of a Spell's Components, you can't cast it.

### Verbal
A Verbal Component is a string of esoteric words spoken at a normal speaking voice. The words themselves aren't the source of the Spell's power; their specific pitch and resonance set the threads of magic in motion. A creature that can't speak, or that is within an area of magical silence, can't cast a Spell with a Verbal Component.

### Somatic
A Somatic Component is a forceful or intricate gesture. You must use at least one hand to perform it.

### Material
A Material Component is an item used in the casting. You must have a free hand to access it, though it can be the same hand used for any Somatic Component.

If a Material Component is named, you must provide that specific item. The Spell states whether a named Component is consumed when the Spell is cast.

If a Material Component isn't named, you can use a Component Pouch. If you have the Spellcasting feature from a class the Spell belongs to, you can instead use the Spellcasting Focus described in that feature.

When you cast a Spell from an Item, the Item serves as the Spell's Material Component — even one that names a Component — and isn't consumed unless its description says otherwise.

## Duration
A Spell's Duration is how long its magic lingers. A Duration usually takes one of these forms:

- **A span of time.** The effect lasts a set number of Rounds, minutes, hours, or longer. You can dismiss it at any time _(no action required)_.
- **Concentration.** A span of time marked _(Concentration)_ lasts only while you maintain [Concentration](#concentration).
- **None (—).** The effect resolves at once and doesn't persist.

## Concentration
Concentration is the focus a caster holds to keep a lasting Spell in effect, a link that damage or distraction can break.

- **Time limit.** If the effect has a maximum duration, your Concentration ends when that time passes.
- **A second effect.** If you start Concentrating on another effect, you end one of them.
- **Damage.** After you take damage, you make a Concentration Save to keep Concentrating. The DC equals **10** or half the damage taken (rounded down), whichever is higher, to a maximum of **30**.
- **Incapacitation.** Your Concentration ends if you become Incapacitated or die.
