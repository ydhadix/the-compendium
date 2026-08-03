"""Generate the race table: one row snippet per race + the aggregate `_index_table.md`.

Each race lives at `character/race/<name>.md` and opens with a `| Key | Value |` stat table (Abilities,
Creature Type, Size Category, Speed, Reach, Hit Points, and an optional Senses row). This pulls those
cells into a single alphabetical index table for the Races hub. The Abilities cell is rewritten to the
formula shorthand used elsewhere: a fixed ability becomes its three-letter code (`Constitution and
choose **1**` -> `CON + **1**`); a pure `Choose **N**` grant is kept verbatim. A missing Senses cell
renders as the em-dash blank.
"""

import re

import genSnippetCommon as C

RACE_ROOT = C.DOCS / "character/race"
MIRROR_ROOT = C.MIRROR / "character/race"
HEADER = ("Race", "Abilities", "Creature Type", "Size", "Speed", "Reach", "Hit Points", "Senses")
ABILITY_ABBR = {
    "Strength": "STR", "Dexterity": "DEX", "Constitution": "CON",
    "Intelligence": "INT", "Wisdom": "WIS", "Charisma": "CHA",
}


def AbilityShorthand(value):
    """Rewrite an Abilities cell to formula shorthand; pass anything unrecognized through unchanged."""
    if value is None:
        return None
    match = re.match(r"^(\w+) and choose (\*\*\d+\*\*)$", value)
    if match and match.group(1) in ABILITY_ABBR:
        return f"{ABILITY_ABBR[match.group(1)]} + {match.group(2)}"
    return value


def CreatureType(value):
    """Join a dual creature type with an ambersand: `Humanoid and Celestial` -> `Humanoid & Celestial`."""
    if value is None:
        return None
    return value.replace(" and ", "<br>& ")


def SizeCategory(value):
    """Join a dual size category with a slash: `Medium or Small` -> `Medium / Small`."""
    if value is None:
        return None
    return value.replace(" or ", "<br>/ ")


def RaceRow(card):
    """`| Race | Abilities | Creature Type | Size | Speed | Reach | Hit Points | Senses |` row."""
    return C.RenderRow([
        C.Link(card),
        AbilityShorthand(C.MetaValue(card.text, "Abilities")),
        CreatureType(C.MetaValue(card.text, "Creature Type")),
        SizeCategory(C.MetaValue(card.text, "Size Category")),
        C.MetaValue(card.text, "Speed"),
        C.MetaValue(card.text, "Reach"),
        C.MetaValue(card.text, "Hit Points"),
        C.MetaValue(card.text, "Senses"),
    ])


def RaceFiles():
    """Race card files under character/race, excluding the index page."""
    return [p for p in sorted(RACE_ROOT.glob("*.md")) if p.name != "index.md"]


def Main():
    written = []
    records = []
    for path in RaceFiles():
        card = C.ReadCard(path)
        written.append(C.WriteSnippet(path, RaceRow(card)))
        records.append((card.title, C.RowInclude(path)))
    records.sort(key=lambda rec: rec[0].lower())
    rows = [row for (title, row) in records]
    C.WriteText(MIRROR_ROOT / "_index_table.md", C.TableBlock(HEADER, rows))
    removed = C.PruneOrphans(MIRROR_ROOT, written)
    print(f"Races: wrote {len(written)} rows, pruned {removed}.")


if __name__ == "__main__":
    Main()
