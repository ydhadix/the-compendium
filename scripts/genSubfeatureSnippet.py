"""Generate class-subfeature table-row snippets + example tables (invocations, imprints, metamagic).

Row schema: | <Type> | Other Prerequisite | Class+Level Prerequisite |
Invocations and imprints share one `Prerequisite: Level N <Class>[, ...]` subtitle format (an entry
with no `Prerequisite:` line defaults to <Class> 1); metamagic carries neither.
Invocation and imprint example tables are grouped by level to mirror their real indexes.

Like the Spelljammer Pilot maneuvers, each subfeature nests inside its class/feature block, so every
table is followed by the same entries' demoted h5 `<slug>.md` bodies, included by `--8<--` in the
same order — the h3 source pages are build-excluded and exist only as these snippets, so the body
includes are what render each card and supply its heading anchor. Body includes are gated on the
bodies actually being emitted: emission is category-wide all-or-nothing (see EmitBodies), so a
category with an offender falls back to table-only rather than including snippets that don't exist.
"""

import genSnippetCommon as C

PREREQ_TAG = "Prerequisite:"

# Conscious, category-wide decision: subfeatures nest inside a class/feature block, so we emit
# h5-demoted bodies. Enforced all-or-nothing per subfeature type (see genSnippetCommon.IsSafelyDemotable).
DECOMPOSABLE = True


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
    return (C.RenderRow([C.AnchorLink(card), other, classLevel]), LevelFromClass(classLevel))


def MetamagicRow(card):
    """(row, level) for a metamagic option; it has no prerequisite or level."""
    return (C.RenderRow([C.AnchorLink(card), "", ""]), 0)


SUBFEATURES = (
    ("character/class/warlock/invocation", "Invocation", lambda card: PrereqRow(card, "Warlock"), True),
    ("character/class/ranger/imprint", "Imprint", lambda card: PrereqRow(card, "Ranger"), True),
    ("character/class/sorcerer/metamagic", "Metamagic", MetamagicRow, False),
)


def BodyIncludes(cards, emitted):
    """Body-snippet `--8<--` lines for `cards` [(title, path), ...], each followed by a blank line.

    Only cards whose demoted body was actually emitted contribute a line, so a table-only fallback
    (no bodies emitted for the category) leaves the section as its table alone.
    """
    parts = []
    for (title, path) in cards:
        body = C.BodySnippetPath(path)
        if body in emitted:
            parts.append(C.SnippetInclude(body))
            parts.append("")
    return parts


def GroupedExample(header, records, emitted):
    """Level-grouped example: a `### Level N` section + table + demoted bodies for each level."""
    parts = []
    for level in sorted(set(lv for (lv, title, path) in records)):
        cards = [(title, path) for (lv, title, path) in records if lv == level]
        rows = [C.RowInclude(path) for (title, path) in cards]
        parts.append(f"### Level {level}")
        parts.append("")
        parts.append(C.TableBlock(header, rows).rstrip("\n"))
        parts.append("")
        parts.extend(BodyIncludes(cards, emitted))
    return "\n".join(parts).rstrip("\n") + "\n"


def FlatExample(header, records, emitted):
    """Single unsorted-by-level example table (metamagic), followed by its demoted bodies."""
    cards = [(title, path) for (lv, title, path) in records]
    rows = [C.RowInclude(path) for (title, path) in cards]
    parts = [C.TableBlock(header, rows).rstrip("\n"), ""]
    parts.extend(BodyIncludes(cards, emitted))
    return "\n".join(parts).rstrip("\n") + "\n"


def BuildSubfeature(relDir, label, rowFunc, grouped):
    """Write row snippets + one example table (+ demoted bodies) for a single subfeature type."""
    sourceDir = C.DOCS / relDir
    mirrorDir = C.MIRROR / relDir
    header = (label, "Prerequisite", "Class + Level")
    written = []
    cards = []
    records = []
    for path in sorted(sourceDir.glob("*.md")):
        if path.name != "index.md":
            card = C.ReadCard(path)
            cards.append(card)
            row, level = rowFunc(card)
            written.append(C.WriteSnippet(path, row))
            records.append((level, card.title, path))
    records.sort(key=lambda rec: (rec[0], rec[1].lower()))
    bodies = C.EmitBodies(cards, DECOMPOSABLE, label)
    emitted = set(bodies)
    example = (GroupedExample(header, records, emitted) if grouped
               else FlatExample(header, records, emitted))
    C.WriteText(mirrorDir / f"_index_table.md", example)
    prunedBodies = C.PruneBodies(mirrorDir, bodies)
    removed = C.PruneOrphans(mirrorDir, written)
    return (len(written), len(bodies), removed, prunedBodies)


def Main():
    for (relDir, label, rowFunc, grouped) in SUBFEATURES:
        wrote, bodies, removed, prunedBodies = BuildSubfeature(relDir, label, rowFunc, grouped)
        print(f"{label}: wrote {wrote} rows, {bodies} bodies, pruned {removed} rows + {prunedBodies} bodies.")


if __name__ == "__main__":
    Main()
