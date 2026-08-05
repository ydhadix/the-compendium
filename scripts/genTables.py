"""Generate the straightforward metadata index tables from one declarative spec per domain.

Races, items, magic items, and protocols are the same task: read each card, extract a fixed set of
columns, partition the cards by their source folder, and write one table per folder into the mirror.
They differ only in their columns, grouping, sort, preamble, and whether rows are exported for
cherry-picking — all captured in the TABLES specs below. Spells and the bestiary keep their own
scripts: they run genuinely different algorithms (dual per-level/per-class tables with a level rail;
multi-block variant splitting with demoted bodies), not just different columns.
"""

from collections import namedtuple

import genSnippetCommon as C

FLAT = "flat"
LETTER = "letter"

# A table column: `key` pulls a `| Key | Value |` metadata cell; `fn` derives the cell from the card.
Column = namedtuple("Column", "header key fn")
# A domain: where its cards live, its columns, how each folder's table is grouped/sorted, an optional
# table preamble, whether per-card rows are exported, and the mirror roots to prune stale snippets from.
TableSpec = namedtuple("TableSpec", "name sources columns grouping sortKey preamble exportRows pruneRoots")

PROTOCOL_LEGEND = "- Durations with `(C)` require Concentration."
RARITY_ATTUNE_MARK = ", Attunement"
RARITY_CONSUMABLE_MARK = ", Consumable"


def meta(header, key):
   """A column filled straight from the card's `| key | value |` metadata row."""
   return Column(header, key, None)


def derived(header, fn):
   """A column whose cell is computed from the card by `fn`."""
   return Column(header, None, fn)


def cellValue(column, card):
   """The cell text for one column of one card."""
   if column.fn is not None:
      value = column.fn(card)
   else:
      value = C.metaValue(card.text, column.key)
   return value


def byTitle(card):
   """Sort key: the card title, case-folded."""
   return card.title.lower()


# --- Races -------------------------------------------------------------------------------------
ABILITY_ABBR = {
   "Strength": "STR", "Dexterity": "DEX", "Constitution": "CON",
   "Intelligence": "INT", "Wisdom": "WIS", "Charisma": "CHA",
}


def abilitiesCell(card):
   """The Abilities cell in formula shorthand (`Constitution and choose **1**` -> `CON + **1**`)."""
   value = C.metaValue(card.text, "Abilities")
   result = value
   if value is not None and " and choose " in value:
      fixed, choose = value.split(" and choose ", 1)
      if fixed in ABILITY_ABBR:
         result = f"{ABILITY_ABBR[fixed]} + {choose}"
   return result


def creatureTypeCell(card):
   """The Creature Type cell, dual types split onto two lines with an ampersand."""
   value = C.metaValue(card.text, "Creature Type")
   return value.replace(" and ", "<br>& ") if value is not None else None


def sizeCell(card):
   """The Size cell, dual sizes split onto two lines with a slash."""
   value = C.metaValue(card.text, "Size Category")
   return value.replace(" or ", "<br>/ ") if value is not None else None


# --- Items -------------------------------------------------------------------------------------
def itemTypeCell(card):
   """Item type: the first comma-token of the subtitle."""
   return card.subtitle.split(",")[0].strip()


def itemValueCell(card):
   """Item value: the last comma-token of the subtitle."""
   return card.subtitle.split(", ")[-1].strip()


# --- Magic items -------------------------------------------------------------------------------
def rarityDisplay(card):
   """Display rarity from the card's rarity subdir, e.g. 'very-rare' -> 'Very Rare'."""
   words = [word.capitalize() for word in card.path.parent.name.split("-")]
   return " ".join(words)


def rarityBody(card):
   """The subtitle with its leading '<Rarity> ' prefix removed."""
   prefix = rarityDisplay(card) + " "
   return card.subtitle[len(prefix):] if card.subtitle.startswith(prefix) else card.subtitle


def magicTypeCell(card):
   """Magic-item type: the subtitle body up to the Attunement mark, sans a trailing Consumable mark."""
   body = rarityBody(card)
   rawType = (body.split(RARITY_ATTUNE_MARK, 1)[0] if RARITY_ATTUNE_MARK in body else body).strip()
   trimmed = rawType[:-len(RARITY_CONSUMABLE_MARK)] if rawType.endswith(RARITY_CONSUMABLE_MARK) else rawType
   return trimmed.strip()


def magicAttuneCell(card):
   """Attunement cell: 'No', or 'Yes' plus any qualifier after the Attunement mark."""
   body = rarityBody(card)
   hasAttune = RARITY_ATTUNE_MARK in body
   qualifier = body.split(RARITY_ATTUNE_MARK, 1)[1].strip() if hasAttune else ""
   return ("Yes " + qualifier).strip() if hasAttune else "No"


# --- Protocols ---------------------------------------------------------------------------------
def protocolLevel(card):
   """Numeric spell level from a protocol subtitle: 0 for a Cantrip, else the '3rd-Level' number."""
   if card.subtitle.endswith("Cantrip"):
      level = 0
   else:
      head = card.subtitle.split("-Level", 1)[0].strip()
      level = int("".join(ch for ch in head if ch.isdigit()))
   return level


def protocolLevelCell(card):
   """Level column: 'Cantrip' for level 0, else the bare number."""
   level = protocolLevel(card)
   return "Cantrip" if level == 0 else str(level)


def protocolActivationCell(card):
   """Activation Time with any Reaction trigger clause dropped."""
   return C.metaValue(card.text, "Activation Time").split(",")[0].strip()


def protocolDurationCell(card):
   """Duration with Concentration shortened to `(C)`."""
   return C.metaValue(card.text, "Duration").replace("(Concentration)", "(C)")


def byProtocolLevelThenTitle(card):
   """Sort key: protocol level, then title."""
   return (protocolLevel(card), card.title.lower())


TABLES = (
   TableSpec(
      name="Races",
      sources=("character/race/*.md",),
      columns=(
         derived("Race", C.link),
         derived("Abilities", abilitiesCell),
         derived("Creature Type", creatureTypeCell),
         derived("Size", sizeCell),
         meta("Speed", "Speed"),
         meta("Reach", "Reach"),
         meta("Hit Points", "Hit Points"),
         meta("Senses", "Senses"),
      ),
      grouping=FLAT,
      sortKey=byTitle,
      preamble="",
      exportRows=False,
      pruneRoots=("character/race",),
   ),
   TableSpec(
      name="Items",
      sources=("item/gear/*/*.md", "item/material/*.md", "item/trade/*.md", "item/trade/artisan/*.md"),
      columns=(
         derived("Item", C.link),
         derived("Type", itemTypeCell),
         derived("Value", itemValueCell),
      ),
      grouping=FLAT,
      sortKey=byTitle,
      preamble="",
      exportRows=True,
      pruneRoots=("item/gear", "item/material", "item/trade"),
   ),
   TableSpec(
      name="Magic items",
      sources=(
         "item/magic/infusion/common/*.md", "item/magic/infusion/uncommon/*.md",
         "item/magic/infusion/rare/*.md", "item/magic/infusion/very-rare/*.md",
         "item/magic/infusion/legendary/*.md",
      ),
      columns=(
         derived("Item", C.link),
         derived("Type", magicTypeCell),
         derived("Rarity", rarityDisplay),
         derived("Attunement", magicAttuneCell),
      ),
      grouping=LETTER,
      sortKey=byTitle,
      preamble="",
      exportRows=True,
      pruneRoots=("item/magic/infusion",),
   ),
   TableSpec(
      name="Protocols",
      sources=("spelljammer/officer/spelljammer/*.md",),
      columns=(
         derived("Protocol", C.link),
         derived("Level", protocolLevelCell),
         meta("Base Spell", "Base Spell"),
         derived("Activation Time", protocolActivationCell),
         meta("Range", "Range"),
         meta("Target", "Target"),
         derived("Duration", protocolDurationCell),
      ),
      grouping=FLAT,
      sortKey=byProtocolLevelThenTitle,
      preamble=PROTOCOL_LEGEND,
      exportRows=True,
      pruneRoots=("spelljammer/officer/spelljammer",),
   ),
)


def specCards(spec):
   """Every card across a spec's source globs, excluding index and underscore-prefixed files."""
   cards = []
   for glob in spec.sources:
      for path in sorted(C.DOCS.glob(glob)):
         if path.name != "index.md" and not path.name.startswith("_"):
            cards.append(C.readCard(path))
   return cards


def specHeader(spec):
   """The header tuple for a spec's table."""
   return tuple(column.header for column in spec.columns)


def rowText(spec, card):
   """The rendered table row for one card."""
   return C.renderRow([cellValue(column, card) for column in spec.columns])


def folderTable(spec, entries):
   """One folder's table from its [(card, rowText), ...] entries, grouped per the spec."""
   header = specHeader(spec)
   if spec.grouping == LETTER:
      records = [(card.title, C.rowInclude(card.path)) for card, row in entries]
      text = C.letterGrouped(header, records)
   else:
      ordered = sorted(entries, key=lambda entry: spec.sortKey(entry[0]))
      rows = [C.rowInclude(card.path) if spec.exportRows else row for card, row in ordered]
      text = C.tableBlock(header, rows, spec.preamble)
   return text


def buildSpec(spec):
   """Write a spec's per-folder tables (+ row snippets when exported) and prune stale snippets."""
   written = []
   byFolder = {}
   for card in specCards(spec):
      row = rowText(spec, card)
      if spec.exportRows:
         written.append(C.writeRowSnippet(card.path, row))
      byFolder.setdefault(card.path.parent, []).append((card, row))
   for folder, entries in byFolder.items():
      mirrorFolder = C.MIRROR / folder.relative_to(C.DOCS)
      C.writeText(mirrorFolder / C.TABLE_NAME, folderTable(spec, entries))
   removedRows = 0
   removedBodies = 0
   for root in spec.pruneRoots:
      removedRows = removedRows + C.pruneRows(C.MIRROR / root, written)
      removedBodies = removedBodies + C.pruneBodies(C.MIRROR / root, [])
   return (len(byFolder), removedRows, removedBodies)


def main():
   for spec in TABLES:
      tables, removedRows, removedBodies = buildSpec(spec)
      print(f"{spec.name}: wrote {tables} tables, pruned {removedRows} rows + {removedBodies} bodies.")


if __name__ == "__main__":
   main()
