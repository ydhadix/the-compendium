"""Generate nonmagical-item table-row snippets + one example table per source folder.

Row schema: | Item | Type | Rarity | Attunement |
Type is the first comma-token of the subtitle (the trailing token is always cost); nonmagical items
have no rarity or attunement, so those cells are blank. Weapons and armor are rendered as their own
tables elsewhere and are not cards, so they are out of scope.
"""

import genSnippetCommon as C

HEADER = ("Item", "Type", "Value")
SOURCE_GLOBS = ("item/gear/*/*.md", "item/material/*.md", "item/trade/*.md", "item/trade/artisan/*.md")
PRUNE_ROOTS = ("item/gear", "item/material", "item/trade")


def ItemType(subtitle):
    """Item type: the first comma-token of the subtitle (cost token discarded)."""
    return subtitle.split(",")[0].strip()


def ItemValue(subtitle):
    """Item value: the last comma-token of the subtitle."""
    return subtitle.split(", ")[-1].strip()


def ItemCards():
    """Every nonmagical item card file across the source globs, excluding index pages."""
    found = []
    for glob in SOURCE_GLOBS:
        for path in sorted(C.DOCS.glob(glob)):
            if path.name != "index.md":
                found.append(path)
    return found


def Main():
    written = []
    byFolder = {}
    for path in ItemCards():
        card = C.ReadCard(path)
        row = C.RenderRow([C.Link(card), ItemType(card.subtitle), ItemValue(card.subtitle)])
        written.append(C.WriteSnippet(path, row))
        byFolder.setdefault(path.parent, []).append((card.title, row))

    for folder, entries in byFolder.items():
        rows = [row for (title, row) in sorted(entries, key=lambda entry: entry[0].lower())]
        mirrorFolder = C.MIRROR / folder.relative_to(C.DOCS)
        C.WriteText(mirrorFolder / "_index_table.md", C.TableBlock(HEADER, rows))

    removed = 0
    for root in PRUNE_ROOTS:
        removed = removed + C.PruneOrphans(C.MIRROR / root, written)
    print(f"Items: wrote {len(written)} rows, pruned {removed}.")


if __name__ == "__main__":
    Main()
