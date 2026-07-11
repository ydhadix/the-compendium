"""Generate class-subfeature table-row snippets + example tables (invocations, imprints, metamagic).

Row schema: | <Type> | Other Prerequisite | Class+Level Prerequisite |
Invocations and imprints share one `Prerequisite: Level N <Class>[, ...]` subtitle format (an entry
with no `Prerequisite:` line defaults to <Class> 1); metamagic carries neither.
Invocation and imprint example tables are grouped by level to mirror their real indexes.
"""

import genSnippetCommon as C

PREREQ_TAG = "Prerequisite:"


def LevelFromClass(classLevel):
    """Trailing level number of a 'Class N' cell, defaulting to 1."""
    parts = classLevel.split()
    last = parts[-1] if len(parts) > 0 else ""
    return int(last) if last.isdigit() else 1


def PrereqRow(card, defaultClass):
    """(row, level) for a prerequisite-gated subfeature; no `Prerequisite:` means a <Class> 1 baseline."""
    hasPrereq = card.subtitle is not None and card.subtitle.startswith(PREREQ_TAG)
    body = card.subtitle[len(PREREQ_TAG):].strip() if hasPrereq else ""
    classLevel, other = C.SplitPrereq(body) if body != "" else ("", "")
    if classLevel == "":
        classLevel = f"{defaultClass} 1"
    return (C.RenderRow([C.Link(card), other, classLevel]), LevelFromClass(classLevel))


def MetamagicRow(card):
    """(row, level) for a metamagic option; it has no prerequisite or level."""
    return (C.RenderRow([C.Link(card), "", ""]), 0)


SUBFEATURES = (
    ("character/class/warlock/invocation", "Invocation", lambda card: PrereqRow(card, "Warlock"), True),
    ("character/class/ranger/imprint", "Imprint", lambda card: PrereqRow(card, "Ranger"), True),
    ("character/class/sorcerer/metamagic", "Metamagic", MetamagicRow, False),
)


def GroupedExample(header, records):
    """Level-grouped example: a `### Level N` section + table for each populated level."""
    parts = []
    for level in sorted(set(lv for (lv, title, row) in records)):
        rows = [row for (lv, title, row) in sorted(records) if lv == level]
        parts.append(f"### Level {level}")
        parts.append("")
        parts.append(C.TableBlock(header, rows).rstrip("\n"))
        parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


def FlatExample(header, records):
    """Single unsorted-by-level example table (metamagic)."""
    rows = [row for (lv, title, row) in sorted(records, key=lambda rec: rec[1].lower())]
    return C.TableBlock(header, rows)


def BuildSubfeature(relDir, label, rowFunc, grouped):
    """Write row snippets + one example table for a single subfeature type."""
    sourceDir = C.DOCS / relDir
    mirrorDir = C.MIRROR / relDir
    header = (label, "Prerequisite", "Class + Level")
    written = []
    records = []
    for path in sorted(sourceDir.glob("*.md")):
        if path.name != "index.md":
            card = C.ReadCard(path)
            row, level = rowFunc(card)
            written.append(C.WriteSnippet(path, row))
            records.append((level, card.title, row))
    records.sort(key=lambda rec: (rec[0], rec[1].lower()))
    example = GroupedExample(header, records) if grouped else FlatExample(header, records)
    C.WriteText(mirrorDir / f"_index_table.md", example)
    removed = C.PruneOrphans(mirrorDir, written)
    return (len(written), removed)


def Main():
    for (relDir, label, rowFunc, grouped) in SUBFEATURES:
        wrote, removed = BuildSubfeature(relDir, label, rowFunc, grouped)
        print(f"{label}: wrote {wrote} rows, pruned {removed}.")


if __name__ == "__main__":
    Main()
