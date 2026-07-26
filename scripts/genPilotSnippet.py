"""Generate Officer Pilot Maneuver (Spelljammer) table-row snippets + the aggregate level tables.

Maneuvers are a non-spell-like format: each card gates on a `Class List` metadata row such as
'Level 5 Fighter, Monk, Ranger, or Rogue'. That single field drives everything — the tier a
maneuver belongs to (its Level) and the class columns it is checked for. Each `<slug>_row.md`
is the maneuver's class-grid row (its link followed by a ✓ per qualifying class), and it is the
single derived source of truth for that row: `_index_table.md` composes the three shown tables
by `--8<--` including those row files under one `## Level N Maneuvers` header per tier, sorted
alphabetically within a tier, so refreshing a maneuver re-flows every table that reuses its row.
Each tier's table is followed by the same maneuvers' demoted h5 `<slug>.md` bodies, also included
by `--8<--`; the h3 source pages are excluded from the build and exist only as these snippets.
Unlike the spell/protocol tables, empty grid cells stay blank rather than em-dashed.
"""

import genSnippetCommon as C

SOURCE_DIR = C.DOCS / "spelljammer/officer/pilot"
TABLE_DIR = C.MIRROR / "spelljammer/officer/pilot"
CHECK = "✓"

# Conscious, category-wide decision: maneuvers nest inside the Pilot officer block, so we emit
# h5-demoted bodies. Enforced all-or-nothing (see genSnippetCommon.IsSafelyDemotable).
DECOMPOSABLE = True


def ManeuverLevel(classList):
    """Numeric tier from a `Class List` value: the N in its leading 'Level N', else 0."""
    words = classList.split()
    level = 0
    for i, word in enumerate(words):
        if level == 0 and word == "Level" and i + 1 < len(words) and words[i + 1].isdigit():
            level = int(words[i + 1])
    return level


def ManeuverClasses(classList):
    """The class names named in a `Class List` value, in the order they appear.

    'Level', the tier digits, commas, and the 'or' conjunction all fall away because only bare
    class names survive the CLASS_NAMES filter.
    """
    tokens = classList.replace(",", " ").split()
    return [token for token in tokens if token in C.CLASS_NAMES]


def ClassColumns(cards):
    """The grid's class columns: every class any maneuver gates on, in CLASS_NAMES order."""
    present = set()
    for card in cards:
        present.update(ManeuverClasses(C.MetaValue(card.text, "Class List")))
    return [name for name in C.CLASS_NAMES if name in present]


def BuildRow(card, columns):
    """One class-grid row: the maneuver link, then a ✓ or blank cell per column class.

    The name links to the maneuver's on-page anchor (`#<slug>`), not its source path: the h3 source
    pages are build-excluded, so the live target is the h5 body card composed alongside this row.
    Built directly rather than through C.RenderRow so absent classes stay blank; the grid reads as
    a checklist, and an em-dash in every empty cell would drown the ✓ marks.
    """
    link = f"[{card.title}](#{C.Slugify(card.title)})"
    classes = set(ManeuverClasses(C.MetaValue(card.text, "Class List")))
    cells = [link] + [CHECK if name in classes else "" for name in columns]
    return "| " + " | ".join(cells) + " |"


def IndexTable(header, records):
    """Compose records [(level, title, card), ...] into one `## Level N Maneuvers` block per tier.

    Each tier is a hand-built header + separator, an `--8<--` `_row.md` include per maneuver (so the
    row files stay the sole source of each row rather than being re-inlined), then the tier's demoted
    h5 body cards included in the same order — the source pages are build-excluded snippet sources,
    so these includes are what render each maneuver's card and supply its heading anchor.
    """
    levels = sorted(set(level for (level, title, card) in records))
    parts = []
    for level in levels:
        cards = [card for (lvl, title, card) in sorted(records, key=lambda rec: rec[1]) if lvl == level]
        parts.append(f"## Level {level} Maneuvers")
        parts.append("")
        parts.append(C.RenderRow(header))
        parts.append(C.SeparatorRow(len(header)))
        parts.extend(C.RowInclude(card.path) for card in cards)
        parts.append("")
        for card in cards:
            parts.append(C.SnippetInclude(C.BodySnippetPath(card.path)))
            parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


def ManeuverCards():
    """Every maneuver card file in the source folder, excluding the index page."""
    found = []
    for path in sorted(SOURCE_DIR.glob("*.md")):
        if path.name != "index.md":
            found.append(path)
    return found


def Main():
    cards = [C.ReadCard(path) for path in ManeuverCards()]
    columns = ClassColumns(cards)
    header = ("Maneuver",) + tuple(columns)

    written = []
    records = []
    for card in cards:
        row = BuildRow(card, columns)
        written.append(C.WriteSnippet(card.path, row))
        records.append((ManeuverLevel(C.MetaValue(card.text, "Class List")), card.title.lower(), card))

    C.WriteText(TABLE_DIR / "_index_table.md", IndexTable(header, records))

    bodies = C.EmitBodies(cards, DECOMPOSABLE, "Pilot Maneuvers")
    prunedBodies = C.PruneBodies(TABLE_DIR, bodies)
    removed = C.PruneOrphans(TABLE_DIR, written)
    print(f"Pilot Maneuvers: wrote {len(written)} rows, {len(bodies)} bodies, "
          f"pruned {removed} rows + {prunedBodies} bodies.")


if __name__ == "__main__":
    Main()
