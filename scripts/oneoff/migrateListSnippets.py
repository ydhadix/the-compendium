"""One-time migration off the legacy beside-source `_list.md` snippets.

Full-list host pages (spell level indexes, spell class pages, the 5 migrated magic rarity
indexes) drop their hand legend/header + per-row include stacks in favour of a single aggregate
`_table_<type>.md` include. The artificer page keeps its curated per-row includes but repoints
them to `_row.md`, flips its headers to Type-before-Rarity, and normalises its hand rows. Legacy
`_list.md` files that nothing references any more are then deleted, and the obsolete spell
exclusion glob is dropped. Artifacts and Unique magic items keep their hand-maintained `_list.md`.
"""

from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"
MKDOCS = Path(__file__).resolve().parents[2] / "mkdocs.yml"
SPELL_LEVELS = (0, 1, 2, 3, 4, 5, 6)
SPELL_CLASSES = ("artificer", "bard", "cleric", "druid", "paladin", "ranger", "sorcerer", "warlock", "wizard")
MIGRATED_RARITIES = ("common", "uncommon", "rare", "very-rare", "legendary")
LEGEND_MARK = "- Components with"
MAGIC_HEADER_OLD = "| Item | Rarity | Type | Attunement |"
MAGIC_HEADER_NEW = "| Item | Type | Rarity | Attunement |"
ARTIFICER = DOCS / "character/class/artificer/index.md"


def RewireToAggregate(path, marker, includePath):
    """Replace everything from the first `marker` line to EOF with one aggregate include."""
    lines = path.read_text(encoding="utf-8").split("\n")
    cut = len(lines)
    i = 0
    while cut == len(lines) and i < len(lines):
        if lines[i].lstrip().startswith(marker):
            cut = i
        else:
            i = i + 1
    kept = lines[:cut]
    while len(kept) > 0 and kept[-1].strip() == "":
        kept = kept[:-1]
    newText = "\n".join(kept) + "\n\n" + f'--8<-- "{includePath}"' + "\n"
    path.write_text(newText, encoding="utf-8")


def IsSeparator(line):
    """True for a markdown table separator row like `|---|---|`."""
    stripped = line.strip()
    residue = stripped.replace("|", "").replace("-", "").replace(" ", "")
    return stripped.startswith("|") and residue == ""


def RepointInclude(line):
    """Point a legacy magic `_list.md` include at its mirror `_row.md`."""
    return line.replace("item/magic/infusion/", "_generated/item/magic/infusion/").replace("_list.md", "_row.md")


def ReorderRow(line):
    """Flip a 4-cell magic row to Type-before-Rarity, blanks to em-dash, plus a spacing typo fix."""
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    reordered = [cells[0], cells[2], cells[1], cells[3]] if len(cells) == 4 else cells
    filled = ["—" if c == "-" else c for c in reordered]
    row = "| " + " | ".join(filled) + " |"
    return row.replace("Tool(Artisan's Tool)", "Tool (Artisan's Tool)")


def TransformArtificer():
    """Repoint includes, flip headers, and normalise hand rows in the artificer infusion tables."""
    lines = ARTIFICER.read_text(encoding="utf-8").split("\n")
    out = []
    inTable = False
    for line in lines:
        isHeader = line.strip() == MAGIC_HEADER_OLD
        isInclude = line.startswith("--8<--") and "_list.md" in line
        isBlankEnd = inTable and line.strip() == ""
        isRow = inTable and line.startswith("|") and not IsSeparator(line)
        if isHeader:
            out.append(MAGIC_HEADER_NEW)
            inTable = True
        elif isInclude:
            out.append(RepointInclude(line))
        elif isBlankEnd:
            out.append(line)
            inTable = False
        elif isRow:
            out.append(ReorderRow(line))
        else:
            out.append(line)
    ARTIFICER.write_text("\n".join(out), encoding="utf-8")


def DeleteLegacySnippets():
    """Remove `_list.md` files nothing references any more (spells; the 5 migrated rarities)."""
    removed = 0
    for path in sorted(DOCS.glob("spell/level/*/*_list.md")):
        path.unlink()
        removed = removed + 1
    for rarity in MIGRATED_RARITIES:
        for path in sorted(DOCS.glob(f"item/magic/infusion/{rarity}/*_list.md")):
            path.unlink()
            removed = removed + 1
    return removed


def DropSpellExclusion():
    """Remove the now-obsolete spell `_list.md` exclusion glob (artifact/unique magic keep theirs)."""
    lines = MKDOCS.read_text(encoding="utf-8").split("\n")
    kept = [line for line in lines if line.strip() != "spell/level/*/*_list.md"]
    MKDOCS.write_text("\n".join(kept), encoding="utf-8")


def Main():
    for level in SPELL_LEVELS:
        index = DOCS / f"spell/level/{level}/index.md"
        if index.exists():
            RewireToAggregate(index, LEGEND_MARK, f"_generated/spell/level/_table_{level}.md")
    for className in SPELL_CLASSES:
        page = DOCS / f"spell/class/{className}.md"
        if page.exists():
            RewireToAggregate(page, LEGEND_MARK, f"_generated/spell/class/_table_{className}.md")
    for rarity in MIGRATED_RARITIES:
        index = DOCS / f"item/magic/infusion/{rarity}/index.md"
        if index.exists():
            RewireToAggregate(index, MAGIC_HEADER_OLD, f"_generated/item/magic/_table_{rarity}.md")
    TransformArtificer()
    removed = DeleteLegacySnippets()
    DropSpellExclusion()
    print(f"Migration done: rewired host pages, deleted {removed} legacy _list.md files.")


if __name__ == "__main__":
    Main()
