"""Generate the straightforward metadata index tables from one declarative spec per domain.

Races, items, and protocols are the same task: read each card, extract a fixed set of columns,
partition the cards by their source folder, and write one flat table per folder into the mirror. They
differ only in their columns, sort, preamble, and whether rows are exported for cherry-picking — all
captured in the TABLES specs below. Spells, magic items, and the bestiary keep their own scripts:
they run genuinely different algorithms (the same rows grouped twice, on two independent axes;
multi-block variant splitting with demoted bodies), not just different columns.
"""

from collections import namedtuple

import genSnippetCommon as C

# A table column: `key` pulls a `| Key | Value |` metadata cell; `fn` derives the cell from the card.
Column = namedtuple("Column", "header key fn")
# A domain: where its cards live, its columns, how each folder's table is sorted, an optional table
# preamble, whether per-card rows are exported, and the mirror roots to prune stale snippets from.
TableSpec = namedtuple("TableSpec", "name sources columns sortKey preamble exportRows pruneRoots")

PROTOCOL_LEGEND = "- Durations with `(C)` require Concentration."


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
def isThousandsComma(text, index):
   """Whether the comma at `index` is a digit separator (`20,000`) rather than a token break."""
   before = text[index - 1] if index > 0 else ""
   after = text[index + 1] if index + 1 < len(text) else ""
   return before.isdigit() and after.isdigit()


def splitTopLevel(text):
   """Comma-separated tokens, ignoring commas nested inside parentheses or separating digits."""
   tokens = []
   depth = 0
   start = 0
   for index, char in enumerate(text):
      if char == "(":
         depth += 1
      elif char == ")":
         depth -= 1
      elif char == "," and depth == 0 and not isThousandsComma(text, index):
         tokens.append(text[start:index].strip())
         start = index + 1
   tokens.append(text[start:].strip())
   return tokens


def itemTypeCell(card):
   """Item type: the subtitle's first comma-token, keeping a parenthesised subtype list intact."""
   return splitTopLevel(card.subtitle)[0]


def itemValueCell(card):
   """Item value: the subtitle's last comma-token, keeping a parenthesised subtype list intact."""
   return splitTopLevel(card.subtitle)[-1]


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
      sortKey=byTitle,
      preamble="",
      exportRows=True,
      pruneRoots=("item/gear", "item/material", "item/trade"),
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
   """One folder's table from its [(card, rowText), ...] entries, sorted per the spec."""
   ordered = sorted(entries, key=lambda entry: spec.sortKey(entry[0]))
   rows = [C.rowInclude(card.path) if spec.exportRows else row for card, row in ordered]
   return C.tableBlock(specHeader(spec), rows, spec.preamble)


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
      C.writeTable(mirrorFolder / C.TABLE_NAME, folderTable(spec, entries))
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
