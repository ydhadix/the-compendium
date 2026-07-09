"""Generate spelljammer-component table-row snippets + one example table per officer.

Row schema: | Component | Type |
Type is the noun after the officer word in the `<Officer> <Noun>` subtitle (Weapon / Component / Helm);
the officer itself is already implied by the grouping.
"""

import genSnippetCommon as C

HEADER = ("Component",)
OFFICERS = ("pilot", "quartermaster", "spelljammer")
COMPONENT_ROOT = C.DOCS / "spelljammer/creation/component"
MIRROR_ROOT = C.MIRROR / "spelljammer/creation/component"


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
    for officer in OFFICERS:
        rows = []
        for path in OfficerCards(officer):
            card = C.ReadCard(path)
            row = C.RenderRow([C.Link(card)])
            written.append(C.WriteSnippet(path, row))
            rows.append((card.title, row))
        ordered = [row for (title, row) in sorted(rows, key=lambda entry: entry[0].lower())]
        C.WriteText(MIRROR_ROOT / officer / "_index_table.md", C.TableBlock(HEADER, ordered))
    removed = C.PruneOrphans(MIRROR_ROOT, written)
    print(f"Components: wrote {len(written)} rows, pruned {removed}.")


if __name__ == "__main__":
    Main()
