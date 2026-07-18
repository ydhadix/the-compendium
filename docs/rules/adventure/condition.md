# Conditions
Conditions are named states a creature can take on, like Blinded, Frightened, or Invisible. Each one bundles a set of effects that change what a creature can do until the condition ends.
{ .subtitle }

| Condition | Description |
|---|---|
| [Anchoring](#anchoring) | Anchored in place, impossible to move. |
| [Bleeding](#bleeding) | Bleeding freely and progressively weakening. |
| [Blindness](#blindness) | Unable to see. |
| [Burn](#burn) | Caught in spreading flames. |
| [Charm](#charm) | Manipulated into trusting another creature. |
| [Corrosion](#corrosion) | Eaten away by acid. |
| [Daze](#daze) | Rattled and slow to react. |
| [Deafness](#deafness) | Unable to hear. |
| [Down](#down) | Fallen and fighting for life. |
| [Drifting](#drifting) | Caught in uncontrolled, ongoing movement. |
| [Exhaustion](#exhaustion) | Worn down by mounting fatigue. |
| [Fear](#fear) | Frightened of a specific threat. |
| [Grapple](#grapple) | Caught in another creature's grip. |
| [Hidden](#hidden) | Concealed from notice. |
| [Immobile](#immobile) | Unable to move. |
| [Incapacitation](#incapacitation) | Unable to act or react. |
| [Invisible](#invisible) | Impossible to see, even in plain sight. |
| [Marked](#marked) | Singled out by a lingering effect. |
| [Paralysis](#paralysis) | Frozen and helpless. |
| [Petrification](#petrification) | Transformed into lifeless stone. |
| [Prone](#prone) | Knocked to the ground. |
| [Restraint](#restraint) | Bound and held in place. |
| [Sickness](#sickness) | Wracked by illness or toxin. |
| [Stable](#stable) | Stabilized and slowly recovering. |
| [Stun](#stun) | Reeling and defenseless. |
| [Unconscious](#unconscious) | Knocked out and unaware. |

#### Stacking Conditions
The same Condition can be applied by several sources at once.

Some Condition effects compound, while others play out the same no matter how many sources apply them. Either way, each source is tracked individually: a Condition lasts until every source that applied it has ended, and an effect that removes a Condition may remove one or all of its sources at once.

Many Conditions build on others; for example, a creature that is Paralyzed is also Incapacitated and Restrained, and has every effect of those Conditions.  Defenses against an effect of a Condition don't extend to the Condition.

## Conditions
##### Anchoring
- You are Immobile.
- You can't be moved by any effect.
- You can't be knocked Prone _(If you are already prone, you remain prone)_.
- You automatically fail Reflex Saves.

##### Bleeding
The effect that causes this condition sets a Bleed Die.

- After your Turn begins, you take a roll of the Bleed Die as Slashing Damage, and the number of Bleed Dice you roll increases by **1**.

###### Ending the Condition
This condition ends after you heal, or after a creature Stabilizes you.

##### Blindness
- You can't see.
- You automatically fail Ability Checks that require sight
- Your Attack Rolls gain Disadvantage.
- Attack Rolls against you gain Advantage.

##### Burn
The effect that causes this condition sets a Burn Die.

- After your Turn begins, you take a roll of the Burn Die as Fire Damage.

###### Ending the Condition
This condition ends after you spend **15** feet of movement while Prone, or after the fire is doused or submerged.

##### Charm
- You can't target the source of the Charm with harmful Attacks, features, or Spells.
- The source of the Charm gains Advantage on Ability Checks to interact with you socially.

##### Corrosion
The effect that causes this condition sets a Caustic Die.

- After your Turn begins, you take a roll of the Caustic Die as Acid Damage.

###### Ending the Condition
This condition ends after **1** minute, or after you are doused or submerged in clean water or a neutralizing substance.

##### Daze
- On your Turn, you can either Move or take an Action, not both.
- You can take a Bonus Action only by spending a Normal Action.
- You can't take Reactions.

##### Deafness
- You can't hear.
- You automatically fail Ability Checks that require hearing.

##### Down
- You are Dazed and Prone
- You drop anything you're holding.
- Before you take an Action, you make a Fortitude Save _(DC = **11**)_; on a failure, the Action has no effect.
- After your Turn begins, you make a Death Save.
- After you take damage, you fail a Death Save — or two if the damage is from a Critical Hit.

###### Death Saves
A Death Save has a DC of **11** and adds no Ability.

- On a roll of **1** it counts as two failures.
- On a roll of **20** you instead heal **1** Hit Point.

After you fail **3** Death Saves, you die. After you succeed on **3**, you become Stable.

###### Ending the Condition
This condition ends after you become Stable or have more than **0** Hit Points, and you remain Prone when it ends.

##### Drifting
Drifting has a distance and a direction.

- After your Turn begins, you are moved that distance in that direction.
- You can't Move, but you can spend your movement to reduce the Drifting distance — each foot spent reduces it by **1** foot.

###### Ending the Condition
This condition ends after the distance reaches **0**.

##### Exhaustion
Exhaustion is tracked in levels.

- Each time you become Exhausted, you gain **1** Exhaustion level.
- You die if you reach **6** Exhaustion levels.
- Before you make a D20 Test, you reduce the total by twice your Exhaustion level.
- Your Speed decreases by **5** feet for each Exhaustion level.
- After you finish a Long Rest, you remove **1** Exhaustion level.

###### Ending the Condition
This condition ends after you have no Exhaustion levels.

##### Fear
- While you can see the source of the Fear, your Attack Rolls and Ability Checks gain Disadvantage.
- You can't willingly Move closer to the source.

##### Grapple
- You are Immobile.
- Your Attack Rolls against any creature other than the grappler gain Disadvantage.
- The grappler can drag or carry you when it Moves, but each foot of that movement costs it **1** extra foot unless you are Tiny or at least two Size Categories smaller than it.

###### Ending the Condition
This condition ends after you leave the grappler's Reach.

##### Hidden
The effect that causes this condition sets a Hide DC.  A creature whose Passive Perception exceeds your Hide DC ignores this condition.

- Other creatures don't know your location.
- You gain Advantage on Initiative Checks and Attack Rolls.
- Attack Rolls against you gain Disadvantage.

###### Ending the Condition
This condition ends after:

- you make an Attack Roll.
- you cast a spell with Verbal components.
- an Enemy sees you.
- an Enemy uses the Search action and its total exceeds your Hide DC.

##### Immobile
- Your Speed is **0** and can't change.
- Your Reflex Saves gain Disadvantage.

##### Incapacitation
- You can't take Actions, Bonus Actions, or Reactions.
- You can't speak.
- Your Concentration is broken.

##### Invisible
- You and anything you're wearing or carrying can't be seen.
- Your Attack Rolls gain Advantage.
- Attack Rolls against you gain Disadvantage.

##### Marked
Marked has no effect on its own. It marks a creature as the target of an ongoing effect so that effect can track it; the feature or Spell that applies this condition defines what it does and when it ends.

##### Paralysis
- You are Incapacitated and Restrained.
- Before you are hit by an attack while the attacker is within **5** feet, that attack becomes a Critical Hit.

##### Petrification
- You are Incapacitated and Restrained.
- You are Blinded, Deafened, and unaware of your surroundings.
- You gain Resistance to all damage.
- You and nonmagical objects you are wearing or carrying turn into a solid, inanimate substance, usually stone.
- Your weight is multiplied by **10**.
- You stop aging.

##### Prone
- Each foot you Move costs **1** extra foot.
- Your Attack Rolls and Reflex Saves gain Disadvantage.
- Attack Rolls against you gain Advantage if the attacker is within **5** feet, and Disadvantage otherwise.

###### Ending the Condition
This condition ends after you spend half your Speed to stand up; before you stand, each creature within Reach can use a Reaction to make an Opportunity Attack against you _(those creatures don't need special training to make this Opportunity Attack)_.

##### Restraint
- You are Immobile.
- You automatically fail Reflex Saves.
- Your Attack Rolls gain Disadvantage.
- Attack Rolls against you gain Advantage.

##### Sickness
- Your Attack Rolls and Ability Checks gain Disadvantage.

##### Stable
- You are Dazed.
- Before you take an Action, you make a Fortitude Save _(DC = **11**)_; on a failure, the Action has no effect.
- After **1d4** hours pass, you heal **1** Hit Point.
- After you take damage, you become Downed, and you also fail a Death Save if the damage is from a Critical Hit.

###### Ending the Condition
This condition ends after you become Downed or have more than **0** Hit Points.

##### Stun
- You are Incapacitated and Restrained.

##### Unconscious
- You are Incapacitated, Restrained, and Prone _(you remain Prone when Unconscious ends)_.
- You are Blinded and Deafened.
- You drop anything you're holding.
- Before you are hit by an attack while the attacker is within **5** feet, that attack becomes a Critical Hit.
