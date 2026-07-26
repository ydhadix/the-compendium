"""Generate spell table-row snippets + per-level and per-class example tables.

Row schema: | Spell | School | Components | Cast Time | Range | Target | Duration |
Most cells come from the card's `| Key | Value |` metadata table; School comes from the subtitle.
Shorthand added here that the source spells out: `($)`/`($C)` for valuable/consumed materials,
`(R)` for ritual cast times, `(C)` for Concentration.
"""

import genSnippetCommon as C

LEVELS = (0, 1, 2, 3, 4, 5, 6)
CLASSES = ("artificer", "bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard")
HEADER = ("Spell", "School", "Components", "Cast Time", "Range", "Target", "Duration")
ORDINALS = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th", 5: "5th", 6: "6th"}
LEGEND = (
    "- Components with `($)` require valuable components. Components with `($C)` consume those components.\n"
    "- Cast Times with `(R)` can be cast as a Ritual.\n"
    "- Durations with `(C)` require Concentration."
)
SPELL_ROOT = C.DOCS / "spell/level"
LEVEL_TABLE_DIR = C.MIRROR / "spell/level"
CLASS_TABLE_DIR = C.MIRROR / "spell/class"
RITUAL_MARK = ", or Ritual"

# Conscious, category-wide decision: spells are NOT decomposed for nesting. Dozens carry two
# sub-heading tiers (h5 + h6), which can't flatten to a single h6 tier
# (see genSnippetCommon.IsSafelyDemotable).
DECOMPOSABLE = False


def School(subtitle):
    """School word from a subtitle like 'Evocation Cantrip' or '1st-Level Enchantment'."""
    result = subtitle.replace(" Cantrip", "") if subtitle.endswith("Cantrip") else subtitle.split("-Level ", 1)[1]
    return result.strip()


def Components(text):
    """Component letters plus a `($)`/`($C)` marker derived from the material gloss."""
    raw = C.MetaValue(text, "Components")
    letters = raw.split(" _(", 1)[0].strip()
    lowered = raw.lower()
    hasGloss = "_(" in raw
    marker = ""
    if hasGloss and "consume" in lowered:
        marker = " ($C)"
    elif hasGloss and "worth" in lowered and "gold" in lowered:
        marker = " ($)"
    return letters + marker


def CastTime(text):
    """Casting time with any trigger clause dropped and a `(R)` ritual marker appended."""
    raw = C.MetaValue(text, "Casting Time")
    isRitual = RITUAL_MARK in raw
    base = raw.replace(RITUAL_MARK, "").split(",")[0].strip()
    return base + (" (R)" if isRitual else "")


def Duration(text):
    """Duration with Concentration shortened to `(C)`."""
    return C.MetaValue(text, "Duration").replace("(Concentration)", "(C)")


def ClassList(text):
    """Classes the spell belongs to, lowercased, from its Classes metadata row."""
    raw = C.MetaValue(text, "Classes")
    return [name.strip().lower() for name in raw.split(",")]


def BuildRow(card):
    """The full 7-cell table row for one spell card."""
    cells = [
        C.Link(card),
        School(card.subtitle),
        Components(card.text),
        CastTime(card.text),
        C.MetaValue(card.text, "Range"),
        C.MetaValue(card.text, "Target"),
        Duration(card.text),
    ]
    return C.RenderRow(cells)


def LevelName(level):
    """Section label for a level: 'Cantrips' for 0, else '1st-Level' and so on."""
    return "Cantrips" if level == 0 else ORDINALS[level] + "-Level"


def SourceCards(level):
    """Spell card files for one level, excluding the index and legacy `_list.md` snippets."""
    found = []
    folder = SPELL_ROOT / str(level)
    if folder.exists():
        for path in sorted(folder.glob("*.md")):
            keep = path.name != "index.md" and not path.name.endswith("_list.md")
            if keep:
                found.append(path)
    return found


def ClassExample(className, records):
    """Per-class example: the legend, then a `## Level` section + table for each populated level."""
    parts = [LEGEND, ""]
    for level in LEVELS:
        rows = [row for (lv, slug, row, classes) in records if lv == level and className in classes]
        if len(rows) > 0:
            parts.append(f"## {LevelName(level)}")
            parts.append("")
            parts.append(C.TableBlock(HEADER, rows).rstrip("\n"))
            parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


def Main():
    written = []
    records = []
    for level in LEVELS:
        for path in SourceCards(level):
            card = C.ReadCard(path)
            row = BuildRow(card)
            written.append(C.WriteSnippet(path, row))
            records.append((level, path.stem, C.RowInclude(path), ClassList(card.text)))
    records.sort(key=lambda rec: (rec[0], rec[1]))

    for level in LEVELS:
        rows = [row for (lv, slug, row, classes) in records if lv == level]
        if len(rows) > 0:
            table = C.TableBlock(HEADER, rows, preamble=LEGEND)
            C.WriteText(LEVEL_TABLE_DIR / str(level) / "_index_table.md", table)

    for className in CLASSES:
        C.WriteText(CLASS_TABLE_DIR / className / "_index_table.md", ClassExample(className, records))

    removed = C.PruneOrphans(LEVEL_TABLE_DIR, written)
    print(f"Spells: wrote {len(written)} rows, pruned {removed}.")


if __name__ == "__main__":
    Main()
