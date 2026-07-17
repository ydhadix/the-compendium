"""Generate feat table-row snippets + one example table per feat category.

Row schema: | Feat | Other Prerequisite | Class+Level Prerequisite |
Category comes from the top-level subdir under `feat/` (Ancestry, Dragonmark, Fighting Style,
General, Origin); prerequisites are parsed from the optional `Prerequisite:` subtitle, split into a
class fragment and everything else. Fighting Style is split further, one table per subcategory
folder (dual-wield, ranged, ...) rather than a single aggregate.
"""

import genSnippetCommon as C

# Epic Boons are left out: that subdir holds only an index today, so it yields no rows.
CATEGORIES = ("ancestry", "dragonmark", "fighting-style", "general", "origin")
# These categories emit one table per immediate subfolder instead of a single aggregate.
SPLIT_CATEGORIES = ("fighting-style",)
HEADER = ("Feat", "Prerequisite", "Class + Level")
SOURCE_ROOT = C.DOCS / "character/feat"
MIRROR_ROOT = C.MIRROR / "character/feat"
PREREQ_TAG = "Prerequisite:"

# Conscious, category-wide decision: feats are NOT decomposed for nesting. The Dragonmarks and the
# "learn a spell" feats (fey-touched, planar-wanderer, scion-of-crossroads, shadow-touched,
# magic-initiate) carry two sub-heading tiers, which can't flatten to a single h6 tier
# (see genSnippetCommon.IsSafelyDemotable). Revisit only if that structure is normalized.
DECOMPOSABLE = False


def Prereqs(card):
    """(Class+Level, Other) prerequisite cells for a feat card."""
    hasPrereq = card.subtitle is not None and card.subtitle.startswith(PREREQ_TAG)
    body = card.subtitle[len(PREREQ_TAG):].strip() if hasPrereq else ""
    classLevel, other = C.SplitPrereq(body) if body != "" else ("", "")
    return (classLevel, other)


def FolderCards(folder):
    """Every feat card file under a folder (any depth), excluding index pages."""
    found = []
    for path in sorted(folder.rglob("*.md")):
        if path.name != "index.md":
            found.append(path)
    return found


def TableGroups(category):
    """(sourceFolder, cardPaths) groups for a category: one group per immediate subfolder
    for split categories, otherwise a single group covering the whole category."""
    root = SOURCE_ROOT / category
    folders = sorted(p for p in root.iterdir() if p.is_dir()) if category in SPLIT_CATEGORIES else [root]
    return [(folder, FolderCards(folder)) for folder in folders]


# Tables this generator used to emit but no longer does; removed so stale copies don't linger.
LEGACY_TABLES = (MIRROR_ROOT / "_table_feat.md", MIRROR_ROOT / "fighting-style" / "_index_table.md")


def Main():
    written = []
    tables = 0
    for category in CATEGORIES:
        for folder, paths in TableGroups(category):
            records = []
            for path in paths:
                card = C.ReadCard(path)
                classLevel, other = Prereqs(card)
                row = C.RenderRow([C.Link(card), other, classLevel])
                written.append(C.WriteSnippet(path, row))
                records.append((card.title, row))
            records.sort(key=lambda rec: rec[0].lower())
            rows = [row for (title, row) in records]
            C.WriteText(C.MIRROR / folder.relative_to(C.DOCS) / "_index_table.md", C.TableBlock(HEADER, rows))
            tables += 1
    for legacy in LEGACY_TABLES:
        if legacy.exists():
            legacy.unlink()
    removed = C.PruneOrphans(MIRROR_ROOT, written)
    print(f"Feats: wrote {len(written)} rows across {tables} tables, pruned {removed}.")


if __name__ == "__main__":
    Main()
