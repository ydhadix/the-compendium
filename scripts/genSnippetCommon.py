"""Shared helpers for the snippet generators.

Each generator reads h3 "card" files, emits one `<slug>_row.md` row per card into the
`docs/_generated/` mirror tree, then composes `_index_table.md` aggregates that `--8<--` include
those row snippets — so each row lives in exactly one file and refreshing a card re-flows every
table that reuses it. Rows whose source has gone are pruned. Aggregate tables are shaped like the
real host indices. Row links use the `/`-prefixed absolute form the site's
`absolute_links: relative_to_docs` resolver expects; blank cells render as an em-dash.
"""

import string
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


def HeadingLevels(text):
    """Every heading depth in a card, in order (title first); empty when there are none."""
    return [lvl for lvl in (HeadingLevel(line) for line in text.split("\n")) if lvl >= 1]


def IsSafelyDemotable(text):
    """True when a card can be flattened for nesting inside a larger stat block.

    Demotion maps the h3 title to h5 and every deeper heading to a single h6 tier, so
    the card is only safe when its title is an h3 and its sub-headings occupy at most one
    level below it; two distinct sub-levels would collapse into one and lose their structure.

    Whether a category is decomposed at all is a conscious, category-wide decision made in each
    generator; this predicate is the all-or-nothing validator for that decision, not a per-card gate.
    """
    levels = HeadingLevels(text)
    hasTitle = len(levels) > 0 and levels[0] == 3
    sub = set(levels[1:])
    return hasTitle and all(lvl > 3 for lvl in sub) and len(sub) <= 1


def DemoteHeadings(text):
    """Flatten a card one nesting deeper: the h3 title becomes h5, deeper headings become h6.

    Only apply to cards that pass IsSafelyDemotable; the body is otherwise returned verbatim.
    """
    out = []
    for line in text.split("\n"):
        level = HeadingLevel(line)
        if level == 3:
            out.append("#####" + line[level:])
        elif level >= 4:
            out.append("######" + line[level:])
        else:
            out.append(line)
    return "\n".join(out)


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


def FrontMatter(text):
    """Parse a leading `---`-fenced YAML front-matter block into a flat `{key: value}` dict."""
    result = {}
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            for line in text[4:end].split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    result[key.strip()] = value.strip()
    return result


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


def AnchorLink(card):
    """Markdown link to a card's on-page toc anchor (`#<slug>`).

    Use when the card's demoted body renders alongside the table (its h3 source page is
    build-excluded), so the live target is the same-page heading, not the source path.
    """
    return f"[{card.title}](#{Slugify(card.title)})"


def SplitPrereq(prereqText):
    """Split a 'Prerequisite:' body into (Class+Level, Other) cells.

    The class-gate comma-fragment becomes the Class+Level cell: 'Level N <Class>' renders as
    '<Class> N' (e.g. 'Level 5 Warlock' -> 'Warlock 5'), and a bare '<Class> Class' renders as
    '<Class>'. Every other fragment joins Other.
    """
    classLevel = ""
    otherParts = []
    for fragment in [part.strip() for part in prereqText.split(",")]:
        words = fragment.split()
        isLevelClass = (
            len(words) == 3 and words[0] == "Level"
            and words[1].isdigit() and words[2] in CLASS_NAMES
        )
        isBareClass = len(words) == 2 and words[0] in CLASS_NAMES and words[1] == "Class"
        if classLevel == "" and isLevelClass:
            classLevel = f"{words[2]} {words[1]}"
        elif classLevel == "" and isBareClass:
            classLevel = words[0]
        elif fragment != "":
            otherParts.append(fragment)
    other = ", ".join(otherParts)
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


def LetterKey(title):
    """Jump-nav bucket for a title: its uppercased first letter, or '0-9' for a digit/symbol."""
    first = title.strip()[:1].upper()
    return first if first.isalpha() else "0-9"


def JumpNav(buckets, active):
    """A `{ .keyword-jump }` nav line over `buckets` [(label, anchor), ...]; active anchors link."""
    cells = [f"[{label}](#{anchor})" if anchor in active else label for (label, anchor) in buckets]
    return " · ".join(cells) + "\n{ .keyword-jump }"


def LetterJumpNav(active):
    """Jump nav over the letter buckets `0-9 · A … Z`; letters in `active` link to their section."""
    buckets = [("0-9", "0-9")] + [(letter, letter.lower()) for letter in string.ascii_uppercase]
    return JumpNav(buckets, active)


def LetterGrouped(header, records):
    """Records (title, row) as a letter jump-nav + `## <Letter>` sections, alphabetical.

    Always leads with the jump nav (every bucket shown, active ones linked); an empty record set
    yields the nav alone so the include still resolves.
    """
    ordered = sorted(records, key=lambda entry: entry[0].lower())
    letters = sorted(set(LetterKey(title) for (title, row) in ordered))
    parts = [LetterJumpNav(set(letter.lower() for letter in letters)), ""]
    for letter in letters:
        rows = [row for (title, row) in ordered if LetterKey(title) == letter]
        parts.append(f"## {letter}")
        parts.append("")
        parts.append(TableBlock(header, rows).rstrip("\n"))
        parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


def MirrorRowPath(sourcePath):
    """Mirror-tree `<slug>_row.md` snippet path for a source card."""
    rel = sourcePath.relative_to(DOCS)
    result = MIRROR / rel.parent / (sourcePath.stem + "_row.md")
    return result


def BodySnippetPath(sourcePath):
    """Mirror-tree full-body snippet path (same relative path and stem as the source)."""
    return MIRROR / sourcePath.relative_to(DOCS)


def WriteText(path, text):
    """Write text to a mirror path, creating parent folders."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def WriteSnippet(sourcePath, rowText):
    """Write a single-row snippet (no trailing newline) for a source card; return its path."""
    target = MirrorRowPath(sourcePath)
    WriteText(target, rowText)
    return target


def SnippetInclude(mirrorPath):
    """A `--8<--` snippet directive for a mirror-tree file, by its `docs`-relative path."""
    rel = mirrorPath.relative_to(DOCS).as_posix()
    return f'--8<-- "{rel}"'


def RowInclude(sourcePath):
    """The `--8<--` directive that reuses a card's `_row.md` row snippet.

    Aggregate tables embed this instead of the row text so each `_row.md` is the single source of
    its row; refreshing the card re-flows every table that includes it.
    """
    return SnippetInclude(MirrorRowPath(sourcePath))


def WriteBodySnippet(sourcePath, text):
    """Write a full-body snippet mirroring a source card (demote before calling); return its path."""
    target = BodySnippetPath(sourcePath)
    WriteText(target, text)
    return target


def EmitBodies(cards, decomposable, label):
    """Category-wide, all-or-nothing demoted-body emission; returns the written body paths.

    Whether a category is decomposed at all is the caller's conscious decision (`decomposable`);
    this only enforces the contract behind it: if any card can't be safely demoted, the whole
    category emits nothing and the offenders are reported so the decision can be revisited.
    """
    if not decomposable:
        return []
    offenders = sorted(card.path.name for card in cards if not IsSafelyDemotable(card.text))
    if offenders:
        print(f"{label}: {', '.join(offenders)} can't be safely demoted; "
              f"emitting NO bodies (category is all-or-nothing).")
        return []
    return [WriteBodySnippet(card.path, DemoteHeadings(card.text)) for card in cards]


def PruneBodies(mirrorRoot, keptBodies):
    """Delete orphaned full-body snippets (any `.md` that isn't a `_row`/`_index_table`) under mirrorRoot."""
    kept = set(str(p) for p in keptBodies)
    removed = 0
    if mirrorRoot.exists():
        for path in sorted(mirrorRoot.rglob("*.md")):
            if path.name.endswith("_row.md") or path.name == "_index_table.md":
                continue
            if str(path) not in kept:
                path.unlink()
                removed = removed + 1
    return removed


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
