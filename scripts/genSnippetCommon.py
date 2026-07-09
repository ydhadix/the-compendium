"""Shared helpers for the snippet generators.

Each generator reads h3 "card" files, emits one `<slug>_row.md` row per card into the
`docs/_generated/` mirror tree, prunes rows whose source has gone, and writes `_table_<type>.md`
aggregate tables shaped like the real host indices. Row links use the `/`-prefixed absolute form the site's
`absolute_links: relative_to_docs` resolver expects; blank cells render as an em-dash.
"""

from collections import namedtuple
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"
MIRROR = DOCS / "_generated"
BLANK = "—"
SUBTITLE_TAG = "{ .subtitle }"
CLASS_NAMES = (
    "Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
    "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard",
)

Card = namedtuple("Card", "title subtitle sitePath text path")


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


def TitleIndex(lines):
    """Index of the first heading line in a card, or -1 when there is none."""
    found = -1
    i = 0
    while found < 0 and i < len(lines):
        if HeadingLevel(lines[i]) >= 1:
            found = i
        else:
            i = i + 1
    return found


def FirstSubtitle(lines, titleIndex):
    """The styled line right under the title (text immediately followed by the subtitle tag)."""
    subtitle = None
    textIndex = titleIndex + 1
    tagIndex = titleIndex + 2
    hasPair = tagIndex < len(lines)
    if hasPair and lines[tagIndex].strip() == SUBTITLE_TAG:
        subtitle = lines[textIndex].strip()
    return subtitle


def ReadCard(path):
    """Parse a card file into title, first subtitle, site link path, and raw text."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    idx = TitleIndex(lines)
    title = lines[idx].lstrip("#").strip()
    subtitle = FirstSubtitle(lines, idx)
    sitePath = "/" + path.relative_to(DOCS).as_posix()
    return Card(title, subtitle, sitePath, text, path)


def MetaValue(text, key):
    """Value from a `| Key | Value |` metadata row, or None when the key is absent."""
    value = None
    for line in text.split("\n"):
        stripped = line.strip()
        cells = [c.strip() for c in stripped.strip("|").split("|")] if stripped.startswith("|") else []
        if value is None and len(cells) >= 2 and cells[0] == key:
            value = cells[1]
    return value


def Link(card):
    """Markdown link to a card using its `/`-prefixed site path."""
    return f"[{card.title}]({card.sitePath})"


def SplitPrereq(prereqText):
    """Split a 'Prerequisite:' body into (Class+Level, Other) cells.

    The first comma-fragment naming a class becomes the Class+Level cell (a trailing ' Class' word
    is dropped, a level number is kept, e.g. 'Warlock 5'); every other fragment joins Other.
    """
    classLevel = ""
    otherParts = []
    for fragment in [part.strip() for part in prereqText.split(",")]:
        head = fragment.split()[0] if fragment != "" else ""
        isClass = head in CLASS_NAMES and classLevel == ""
        if isClass and fragment.endswith(" Class"):
            classLevel = fragment[:-len(" Class")].strip()
        elif isClass:
            classLevel = fragment
        else:
            otherParts.append(fragment)
    other = ", ".join(part for part in otherParts if part != "")
    return (classLevel, other)


def RenderRow(cells):
    """One markdown table row; empty cells become the em-dash blank; no trailing newline."""
    filled = [str(c) if (c is not None and str(c).strip() != "") else BLANK for c in cells]
    result = "| " + " | ".join(filled) + " |"
    return result


def SeparatorRow(columnCount):
    """The `|---|---|` separator line for a table of the given width."""
    result = "|" + "---|" * columnCount
    return result


def TableBlock(headerCells, rows, preamble=""):
    """A full table (optional preamble + header + separator + rows) as one text block."""
    lines = []
    if preamble != "":
        lines.append(preamble)
        lines.append("")
    lines.append(RenderRow(headerCells))
    lines.append(SeparatorRow(len(headerCells)))
    lines.extend(rows)
    result = "\n".join(lines) + "\n"
    return result


def MirrorRowPath(sourcePath):
    """Mirror-tree `<slug>_row.md` snippet path for a source card."""
    rel = sourcePath.relative_to(DOCS)
    result = MIRROR / rel.parent / (sourcePath.stem + "_row.md")
    return result


def WriteText(path, text):
    """Write text to a mirror path, creating parent folders."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def WriteSnippet(sourcePath, rowText):
    """Write a single-row snippet (no trailing newline) for a source card; return its path."""
    target = MirrorRowPath(sourcePath)
    WriteText(target, rowText)
    return target


def PruneOrphans(mirrorRoot, keptPaths):
    """Delete `*_row.md` under mirrorRoot with no live source, then drop emptied folders."""
    kept = set(str(p) for p in keptPaths)
    removed = 0
    if mirrorRoot.exists():
        for path in sorted(mirrorRoot.rglob("*_row.md")):
            if str(path) not in kept:
                path.unlink()
                removed = removed + 1
        for folder in sorted(mirrorRoot.rglob("*"), reverse=True):
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()
    return removed
