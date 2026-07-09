"""Phase 0 (one-time): split subfeature collection files into h3 one-file-per-option cards.

Each `<type>.md` (metamagic / imprint / invocation) becomes a `<type>/` directory: every h5
entry is written to `<type>/<slug>.md` with an h3 title, and `<type>/index.md` keeps the original
intro, level headers, and link-tables but replaces each inline entry with an `--8<--` include of
its new card. Included h3 cards still emit the `#slug` anchors the link-tables point at, so those
tables keep working untouched.
"""

from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"
COLLECTIONS = (
    "character/class/sorcerer/metamagic.md",
    "character/class/ranger/imprint.md",
    "character/class/warlock/invocation.md",
)


def HeadingLevel(line):
    """Markdown heading depth of a line (1-6), or 0 when it is not a heading."""
    hashes = len(line) - len(line.lstrip("#"))
    isHeading = hashes >= 1 and line[hashes:hashes + 1] == " "
    level = hashes if isHeading else 0
    return level


def Slugify(title):
    """Lowercase slug matching MkDocs' toc anchors (apostrophes dropped, spaces -> hyphens)."""
    lowered = title.strip().lower()
    kept = "".join(ch for ch in lowered if ch.isalnum() or ch in " -")
    slug = "-".join(kept.split())
    return slug


def EntryEnd(lines, start):
    """Index of the first line after `start` that opens a new h1-h5 section (h6 stays in-entry)."""
    cursor = start + 1
    total = len(lines)
    searching = True
    while searching:
        atEnd = cursor >= total
        level = 0 if atEnd else HeadingLevel(lines[cursor])
        if atEnd or 1 <= level <= 5:
            searching = False
        else:
            cursor = cursor + 1
    return cursor


def CardText(entryLines):
    """Entry block as a standalone card: h5 title -> h3, trailing blank lines trimmed."""
    title = entryLines[0].lstrip("#").strip()
    body = ["### " + title] + entryLines[1:]
    while len(body) > 0 and body[-1].strip() == "":
        body = body[:-1]
    result = "\n".join(body) + "\n"
    return result


def SplitCollection(collectionPath):
    """Write per-option cards + a rebuilt index for one collection, then drop the original file."""
    dirPath = collectionPath.with_suffix("")
    relDir = dirPath.relative_to(DOCS).as_posix()
    dirPath.mkdir(exist_ok=True)

    lines = collectionPath.read_text(encoding="utf-8").split("\n")
    indexLines = []
    cardCount = 0
    i = 0
    total = len(lines)
    while i < total:
        isEntry = HeadingLevel(lines[i]) == 5
        if isEntry:
            end = EntryEnd(lines, i)
            entryLines = lines[i:end]
            slug = Slugify(entryLines[0].lstrip("#"))
            (dirPath / f"{slug}.md").write_text(CardText(entryLines), encoding="utf-8")
            indexLines.append(f'--8<-- "{relDir}/{slug}.md"')
            indexLines.append("")
            cardCount = cardCount + 1
            i = end
        else:
            indexLines.append(lines[i])
            i = i + 1

    indexText = "\n".join(indexLines).rstrip("\n") + "\n"
    (dirPath / "index.md").write_text(indexText, encoding="utf-8")
    collectionPath.unlink()
    print(f"Split {relDir}: {cardCount} cards.")


def Main():
    for rel in COLLECTIONS:
        SplitCollection(DOCS / rel)


if __name__ == "__main__":
    Main()
