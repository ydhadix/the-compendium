"""Generate the two magic-item indices from one set of cards: by rarity and by item type.

Magic items are organized on two axes at once — the rarity folder a card lives in, and the item
type its subtitle names — so this parallels genSpells rather than the declarative genTables specs:
one pass over the cards writes a row snippet per item, then the same rows are grouped twice. The
rarity axis renders letter-grouped tables, falling back to one flat table for the short tiers that
would not fill a letter rail. The type axis renders rarity sections behind a rarity rail. Rows are
exported so a class feature's item list can cherry-pick them.

Row schema: | Item | Type | Rarity | Attunement |. Type and Attunement are parsed out of the
subtitle, whose form is `<Rarity> <Type>[, Consumable][, Attunement|Harmonic[ <qualifier>]]`;
Rarity comes from the card's folder. Attunement is three-valued, since a Harmonic infusion
requires attunement without occupying an Attunement Slot.
"""

from collections import namedtuple

import genSnippetCommon as C

# One magic item, reduced to what both axes need to place and order its shared row.
Record = namedtuple("Record", "rarity title itemType row")

# Rarity folders under the source root, weakest first — also the order of the rarity rail.
RARITIES = ("common", "uncommon", "rare", "very-rare", "legendary", "artifact", "unique", "cursed")
HEADER = ("Item", "Type", "Rarity", "Attunement")
# Item types, as (subtitle head, page slug). The head is the type word(s) before any parenthetical
# subtype; slugs match the mundane gear folders each type mirrors.
TYPES = (
   ("Armor", "armor"),
   ("Clothing", "clothing"),
   ("Container", "container"),
   ("Shield", "shield"),
   ("Spellcasting Focus", "spell-focus"),
   ("Tool", "tool"),
   ("Weapon", "weapon"),
   ("Wondrous Item", "wondrous"),
)
# Rows a rarity needs before its letter rail earns the space; below this the tier renders flat.
LETTER_MIN = 25
ITEM_ROOT = C.DOCS / "item/magic/rarity"
RARITY_TABLE_DIR = C.MIRROR / "item/magic/rarity"
TYPE_TABLE_DIR = C.MIRROR / "item/magic/type"
MIRROR_ROOT = C.MIRROR / "item/magic"
CONSUMABLE_MARK = ", Consumable"
# Attunement marks, as (subtitle mark, Attunement cell value). Ordered as the subtitle writes them.
ATTUNE_MARKS = ((", Attunement", "Yes"), (", Harmonic", "Harmonic"))


def rarityDisplay(rarity):
   """Display name for a rarity folder, e.g. 'very-rare' -> 'Very Rare'."""
   return " ".join(word.capitalize() for word in rarity.split("-"))


def subtitleBody(card, rarity):
   """The subtitle with its leading '<Rarity> ' prefix removed."""
   prefix = rarityDisplay(rarity) + " "
   return card.subtitle[len(prefix):] if card.subtitle.startswith(prefix) else card.subtitle


def attuneSplit(body):
   """Subtitle body split at its attunement mark: (type, cell value, qualifier); value '' when absent."""
   found = (body.strip(), "", "")
   for mark, value in ATTUNE_MARKS:
      if found[1] == "" and mark in body:
         head, tail = body.split(mark, 1)
         found = (head.strip(), value, tail.strip())
   return found


def typeCell(body):
   """Item type: the subtitle body up to the attunement mark, sans a trailing Consumable mark."""
   rawType = attuneSplit(body)[0]
   trimmed = rawType[:-len(CONSUMABLE_MARK)] if rawType.endswith(CONSUMABLE_MARK) else rawType
   return trimmed.strip()


def attuneCell(body):
   """Attunement cell: 'No', or the attunement kind plus any qualifier after its mark."""
   rawType, value, qualifier = attuneSplit(body)
   return (value + " " + qualifier).strip() if value != "" else "No"


def typeHead(itemType):
   """The taxonomy head of an item type: 'Clothing (Jewelry)' -> 'Clothing'."""
   return itemType.split(" (", 1)[0].strip()


def buildRow(card, rarity):
   """The full 4-cell table row for one magic-item card."""
   body = subtitleBody(card, rarity)
   cells = [C.link(card), typeCell(body), rarityDisplay(rarity), attuneCell(body)]
   return C.renderRow(cells)


def sourceCards(rarity):
   """Magic-item card files for one rarity, excluding the index and underscore-prefixed files."""
   found = []
   folder = ITEM_ROOT / rarity
   if folder.exists():
      for path in sorted(folder.glob("*.md")):
         if path.name != "index.md" and not path.name.startswith("_"):
            found.append(path)
   return found


def rarityTable(records):
   """One rarity's table: letter-grouped once it is long enough, otherwise flat and alphabetical."""
   ordered = sorted(records, key=lambda rec: rec.title.lower())
   if len(ordered) >= LETTER_MIN:
      text = C.letterGrouped(HEADER, [(rec.title, rec.row) for rec in ordered])
   else:
      text = C.tableBlock(HEADER, [rec.row for rec in ordered])
   return text


def rarityRail(populated):
   """The rarity rail for a type page: links the populated rarities and greys the empty ones."""
   buckets = [("Rarity", "")]
   active = set()
   for rarity in RARITIES:
      display = rarityDisplay(rarity)
      anchor = C.slugify(display)
      buckets.append((display, anchor))
      if rarity in populated:
         active.add(anchor)
   return C.jumpNav(buckets, active)


def typeTable(records):
   """One type's page: the rarity rail, then a `## <Rarity>` table per populated rarity."""
   populated = set(rec.rarity for rec in records)
   parts = [rarityRail(populated), ""]
   for rarity in RARITIES:
      rows = [rec.row for rec in records if rec.rarity == rarity]
      if len(rows) > 0:
         parts.append(f"## {rarityDisplay(rarity)}")
         parts.append("")
         parts.append(C.tableBlock(HEADER, rows).rstrip("\n"))
         parts.append("")
   return "\n".join(parts).rstrip("\n") + "\n"


def readRecords():
   """Row snippet + Record for every magic-item card, ordered by rarity then title."""
   written = []
   records = []
   for rarity in RARITIES:
      for path in sourceCards(rarity):
         card = C.readCard(path)
         written.append(C.writeRowSnippet(path, buildRow(card, rarity)))
         itemType = typeCell(subtitleBody(card, rarity))
         records.append(Record(rarity, card.title, itemType, C.rowInclude(path)))
   records.sort(key=lambda rec: (RARITIES.index(rec.rarity), rec.title.lower()))
   return (written, records)


def unplacedTypes(records):
   """Type heads found on cards that no TYPES entry claims, so a new type can't go unlisted."""
   known = set(head for head, slug in TYPES)
   return sorted(set(typeHead(rec.itemType) for rec in records) - known)


def main():
   written, records = readRecords()
   for rarity in RARITIES:
      rows = [rec for rec in records if rec.rarity == rarity]
      if len(rows) > 0:
         C.writeText(RARITY_TABLE_DIR / rarity / C.TABLE_NAME, rarityTable(rows))
   for head, slug in TYPES:
      rows = [rec for rec in records if typeHead(rec.itemType) == head]
      C.writeText(TYPE_TABLE_DIR / slug / C.TABLE_NAME, typeTable(rows))
   removed = C.pruneRows(MIRROR_ROOT, written)
   print(f"Magic items: wrote {len(written)} rows, pruned {removed}.")
   for head in unplacedTypes(records):
      print(f"  ! item type not in TYPES, so it has no page: {head}")


if __name__ == "__main__":
   main()
