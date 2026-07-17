"""Generate Officer Protocol (Spelljammer) table-row snippets + the aggregate protocol table.

Row schema: | Protocol | Level | Base Spell | Activation Time | Range | Target | Duration |
Level comes from the spell-like subtitle ('Evocation Cantrip' / '3rd-Level Evocation'); the
remaining cells come from the card's `| Key | Value |` metadata table. Reaction trigger clauses
are dropped from Activation Time and Concentration is shortened to `(C)` in Duration, matching
the spell tables. Rows sort by level, then alphabetically.
Pilot Maneuvers are a separate, non-spell-like format and are out of scope here.
"""

import genSnippetCommon as C

HEADER = ("Protocol", "Level", "Base Spell", "Activation Time", "Range", "Target", "Duration")
SOURCE_DIR = C.DOCS / "spelljammer/officer/spelljammer"
TABLE_DIR = C.MIRROR / "spelljammer/officer/spelljammer"
LEGEND = "- Durations with `(C)` require Concentration."

# Conscious, category-wide decision: protocols nest inside a helm/officer block, so we emit
# h5-demoted bodies. Enforced all-or-nothing (see genSnippetCommon.IsSafelyDemotable).
DECOMPOSABLE = True


def LevelNumber(subtitle):
    """Numeric spell level from a subtitle: 0 for a Cantrip, else the '3rd-Level' number."""
    isCantrip = subtitle.endswith("Cantrip")
    head = subtitle.split("-Level", 1)[0].strip()
    return 0 if isCantrip else int("".join(ch for ch in head if ch.isdigit()))


def LevelCell(level):
    """Level column text: 'Cantrip' for level 0, else the bare number."""
    return "Cantrip" if level == 0 else str(level)


def ActivationTime(text):
    """Activation Time with any Reaction trigger clause (everything after the comma) dropped."""
    return C.MetaValue(text, "Activation Time").split(",")[0].strip()


def Duration(text):
    """Duration with Concentration shortened to `(C)`, matching the spell tables."""
    return C.MetaValue(text, "Duration").replace("(Concentration)", "(C)")


def BuildRow(card):
    """The full 7-cell table row for one protocol card."""
    cells = [
        C.Link(card),
        LevelCell(LevelNumber(card.subtitle)),
        C.MetaValue(card.text, "Base Spell"),
        ActivationTime(card.text),
        C.MetaValue(card.text, "Range"),
        C.MetaValue(card.text, "Target"),
        Duration(card.text),
    ]
    return C.RenderRow(cells)


def ProtocolCards():
    """Every protocol card file in the source folder, excluding the index page."""
    found = []
    for path in sorted(SOURCE_DIR.glob("*.md")):
        if path.name != "index.md":
            found.append(path)
    return found


def Main():
    written = []
    cards = []
    records = []
    for path in ProtocolCards():
        card = C.ReadCard(path)
        cards.append(card)
        row = BuildRow(card)
        written.append(C.WriteSnippet(path, row))
        records.append((LevelNumber(card.subtitle), card.title.lower(), row))
    records.sort(key=lambda rec: (rec[0], rec[1]))

    rows = [row for (level, title, row) in records]
    C.WriteText(TABLE_DIR / "_index_table.md", C.TableBlock(HEADER, rows, preamble=LEGEND))

    bodies = C.EmitBodies(cards, DECOMPOSABLE, "Protocols")
    prunedBodies = C.PruneBodies(TABLE_DIR, bodies)
    removed = C.PruneOrphans(TABLE_DIR, written)
    print(f"Protocols: wrote {len(written)} rows, {len(bodies)} bodies, "
          f"pruned {removed} rows + {prunedBodies} bodies.")


if __name__ == "__main__":
    Main()
