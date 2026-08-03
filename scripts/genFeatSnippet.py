"""Generate one letter-grouped card index per feat category.

Each category (Ancestry, Fighting Style, General, Origin) is a hub that inlines its hand-authored leaf
cards under alphabetical `## <Letter>` headings behind a `{ .keyword-jump }` letter rail. The leaf files
are excluded from the build as standalone pages (see mkdocs `exclude_docs`); this generated include is
where they render, so a card lives in exactly one place and editing it re-flows the hub.

Dragonmarks are a hand-authored single page, and Epic Boons are an unpopulated stub — neither is generated.
"""

import shutil

import genSnippetCommon as C

# Category folders under feat/ that render as a letter-grouped card hub. Dragonmark and Epic are excluded.
CATEGORIES = ("ancestry", "fighting-style", "general", "origin")
SOURCE_ROOT = C.DOCS / "character/feat"
MIRROR_ROOT = C.MIRROR / "character/feat"


def CategoryCards(folder):
    """Every leaf card file in a category folder (any depth), excluding the index page."""
    return [p for p in sorted(folder.rglob("*.md")) if p.name != "index.md"]


def CardInclude(path):
    """A `--8<--` directive that inlines a feat leaf's full card by its `docs`-relative path."""
    return f'--8<-- "{path.relative_to(C.DOCS).as_posix()}"'


def LetterGroupedCards(records):
    """Records (title, includeDirective) as a letter jump-nav + `## <Letter>` sections of inline cards.

    Leads with the jump nav (every bucket shown, active ones linked); an empty set yields the nav alone.
    """
    ordered = sorted(records, key=lambda entry: entry[0].lower())
    letters = sorted(set(C.LetterKey(title) for title, _ in ordered))
    parts = [C.LetterJumpNav(set(letter.lower() for letter in letters)), ""]
    for letter in letters:
        parts.append(f"## {letter}")
        parts.append("")
        for title, include in [(t, i) for t, i in ordered if C.LetterKey(t) == letter]:
            parts.append(include)
            parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


def Main():
    for category in CATEGORIES:
        # Wipe the category's mirror (drops stale _row snippets and any old sub-folders) and rebuild fresh.
        shutil.rmtree(MIRROR_ROOT / category, ignore_errors=True)
        records = [(C.ReadCard(p).title, CardInclude(p)) for p in CategoryCards(SOURCE_ROOT / category)]
        C.WriteText(MIRROR_ROOT / category / "_index_table.md", LetterGroupedCards(records))
    print(f"Feats: wrote {len(CATEGORIES)} card indices.")


if __name__ == "__main__":
    Main()
