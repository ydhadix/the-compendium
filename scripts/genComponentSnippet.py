"""Generate spelljammer-component table-row snippets + one example table per officer.

Row schema: | Component | Type |
Type is the noun after the officer word in the `<Officer> <Noun>` subtitle (Weapon / Component / Helm);
the officer itself is already implied by the grouping.

Components are also emitted as h5-demoted body snippets so a host stat block (e.g. a ship) can nest
one via `--8<--`. That is a conscious, category-wide decision (DECOMPOSABLE below), not a per-card
judgement: components are structurally simple enough to flatten, so every component is decomposed.
It is enforced all-or-nothing — if any single component ever stops being safely demotable, the whole
category emits no bodies (see C.IsSafelyDemotable) and the decision has to be revisited here.
"""

import genSnippetCommon as C

HEADER = ("Component",)
OFFICERS = ("pilot", "quartermaster", "spelljammer")
COMPONENT_ROOT = C.DOCS / "spelljammer/creation/component"
MIRROR_ROOT = C.MIRROR / "spelljammer/creation/component"

# Conscious, category-wide decision: components nest inside ship stat blocks, so we decompose them.
# Other generated card types (spells, feats, items, ...) are evaluated separately and stay False
# until a category is deliberately cleared for nesting.
DECOMPOSABLE = True


def ComponentType(subtitle):
    """The component-type noun: everything after the leading officer word."""
    return subtitle.split(None, 1)[1].strip()


def OfficerCards(officer):
    """Component card files for one officer, excluding the officer index."""
    found = []
    for path in sorted((COMPONENT_ROOT / officer).glob("*.md")):
        if path.name != "index.md":
            found.append(path)
    return found


def Main():
    written = []
    officerCards = {officer: [C.ReadCard(p) for p in OfficerCards(officer)] for officer in OFFICERS}

    # Row snippets + one example table per officer (always generated).
    for officer, cards in officerCards.items():
        rows = []
        for card in cards:
            row = C.RenderRow([C.Link(card)])
            written.append(C.WriteSnippet(card.path, row))
            rows.append((card.title, C.RowInclude(card.path)))
        ordered = [row for (title, row) in sorted(rows, key=lambda entry: entry[0].lower())]
        C.WriteText(MIRROR_ROOT / officer / "_index_table.md", C.TableBlock(HEADER, ordered))

    # Category-wide body decomposition, enforced all-or-nothing.
    allCards = [card for cards in officerCards.values() for card in cards]
    bodies = C.EmitBodies(allCards, DECOMPOSABLE, "Components")
    prunedBodies = C.PruneBodies(MIRROR_ROOT, bodies)
    removed = C.PruneOrphans(MIRROR_ROOT, written)
    print(f"Components: wrote {len(written)} rows, {len(bodies)} bodies, "
          f"pruned {removed} rows + {prunedBodies} bodies.")


if __name__ == "__main__":
    Main()
