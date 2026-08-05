"""Shared helpers for the snippet generators.

Two mechanisms consume this module: a generic inline-hub lister (genInlineHub) and the
metadata index-table generators (spells, items, magic items, races, protocols, bestiary).
Card sources are heading-led markdown files; generated output lands in the docs/_generated
mirror tree and is pulled into built hub pages with pymdownx `--8<--` includes.
"""

import string
from collections import namedtuple
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"
MIRROR = DOCS / "_generated"

BLANK = "—"
SUBTITLE_TAG = "{ .subtitle }"
ROW_SUFFIX = "_row.md"
LIST_NAME = "_list.md"
TABLE_NAME = "_index_table.md"
AGGREGATE_NAMES = (LIST_NAME, TABLE_NAME)

CLASS_NAMES = (
   "Artificer", "Barbarian", "Bard", "Cleric", "Druid", "Fighter", "Monk",
   "Paladin", "Ranger", "Rogue", "Sorcerer", "Warlock", "Wizard",
)

Card = namedtuple("Card", "title subtitle sitePath text path")


def headingLevel(line):
   """Markdown heading depth of a line (1-6), or 0 when it is not a heading."""
   hashes = len(line) - len(line.lstrip("#"))
   isHeading = hashes >= 1 and line[hashes:hashes + 1] == " "
   level = hashes if isHeading else 0
   return level


def demoteHeadings(text):
   """Flatten a block one nesting deeper: the h3 title becomes h5, deeper headings become h6."""
   lines = []
   for line in text.split("\n"):
      level = headingLevel(line)
      if level == 3:
         lines.append("#####" + line[level:])
      elif level >= 4:
         lines.append("######" + line[level:])
      else:
         lines.append(line)
   result = "\n".join(lines)
   return result


def slugify(title):
   """Lowercase anchor slug matching MkDocs' toc (apostrophes dropped, spaces to hyphens)."""
   lowered = title.strip().lower()
   kept = "".join(ch for ch in lowered if ch.isalnum() or ch in " -")
   slug = "-".join(kept.split())
   return slug


def titleIndex(lines):
   """Index of the first heading line in a card, or -1 when there is none."""
   found = -1
   for i, line in enumerate(lines):
      if found < 0 and headingLevel(line) >= 1:
         found = i
   return found


def firstSubtitle(lines, titleAt):
   """The styled line right under the title (text immediately followed by the subtitle tag)."""
   textAt = titleAt + 1
   tagAt = titleAt + 2
   hasPair = tagAt < len(lines) and lines[tagAt].strip() == SUBTITLE_TAG
   subtitle = lines[textAt].strip() if hasPair else None
   return subtitle


def readCard(path):
   """Parse a card file into its title, subtitle, site link path, and raw text."""
   text = path.read_text(encoding="utf-8")
   lines = text.split("\n")
   at = titleIndex(lines)
   title = lines[at].lstrip("#").strip()
   subtitle = firstSubtitle(lines, at)
   sitePath = "/" + path.relative_to(DOCS).as_posix()
   card = Card(title, subtitle, sitePath, text, path)
   return card


def frontMatter(text):
   """Parse a leading `---`-fenced YAML block into a flat {key: value} dict."""
   result = {}
   hasBlock = text.startswith("---\n")
   end = text.find("\n---", 4) if hasBlock else -1
   if end != -1:
      for line in text[4:end].split("\n"):
         if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
   return result


def metaValue(text, key):
   """Value from a `| Key | Value |` metadata row, or None when the key is absent."""
   value = None
   for line in text.split("\n"):
      stripped = line.strip()
      cells = [c.strip() for c in stripped.strip("|").split("|")] if stripped.startswith("|") else []
      if value is None and len(cells) >= 2 and cells[0] == key:
         value = cells[1]
   return value


def link(card):
   """Markdown link to a card using its `/`-prefixed site path."""
   return f"[{card.title}]({card.sitePath})"


def anchorLink(card):
   """Markdown link to a card's on-page toc anchor (`#<slug>`)."""
   return f"[{card.title}](#{slugify(card.title)})"


def renderRow(cells):
   """One markdown table row; empty cells become the em-dash blank; no trailing newline."""
   filled = []
   for cell in cells:
      text = str(cell) if cell is not None else ""
      filled.append(text if text.strip() != "" else BLANK)
   return "| " + " | ".join(filled) + " |"


def separatorRow(columnCount):
   """The `|---|---|` separator line for a table of the given width."""
   return "|" + "---|" * columnCount


def tableBlock(headerCells, rows, preamble=""):
   """A full table (optional preamble + header + separator + rows) as one text block."""
   lines = []
   if preamble != "":
      lines.append(preamble)
      lines.append("")
   lines.append(renderRow(headerCells))
   lines.append(separatorRow(len(headerCells)))
   lines.extend(rows)
   result = "\n".join(lines) + "\n"
   return result


def letterKey(title):
   """Jump-nav bucket for a title: its uppercased first letter, or '0-9' for a digit/symbol."""
   first = title.strip()[:1].upper()
   return first if first.isalpha() else "0-9"


def jumpNav(buckets, active):
   """A `{ .keyword-jump }` nav line over buckets [(label, anchor), ...]; active anchors link."""
   cells = []
   for label, anchor in buckets:
      cells.append(f"[{label}](#{anchor})" if anchor in active else label)
   return " · ".join(cells) + "\n{ .keyword-jump }"


def letterJumpNav(active):
   """Jump nav over the letter buckets `0-9 · A … Z`; letters in `active` link to their section."""
   buckets = [("0-9", "0-9")]
   for letter in string.ascii_uppercase:
      buckets.append((letter, letter.lower()))
   return jumpNav(buckets, active)


def letterGrouped(header, records):
   """Records (title, row) as a letter jump-nav + `## <Letter>` table sections, alphabetical."""
   ordered = sorted(records, key=lambda entry: entry[0].lower())
   letters = sorted(set(letterKey(title) for title, row in ordered))
   active = set(letter.lower() if letter != "0-9" else "0-9" for letter in letters)
   parts = [letterJumpNav(active), ""]
   for letter in letters:
      rows = [row for title, row in ordered if letterKey(title) == letter]
      parts.append(f"## {letter}")
      parts.append("")
      parts.append(tableBlock(header, rows).rstrip("\n"))
      parts.append("")
   result = "\n".join(parts).rstrip("\n") + "\n"
   return result


def mirrorPath(sourcePath):
   """Mirror-tree path for a source file (same relative path)."""
   return MIRROR / sourcePath.relative_to(DOCS)


def mirrorRowPath(sourcePath):
   """Mirror-tree `<slug>_row.md` snippet path for a source card."""
   rel = sourcePath.relative_to(DOCS)
   return MIRROR / rel.parent / (sourcePath.stem + ROW_SUFFIX)


def writeText(path, text):
   """Write text to a path, creating parent folders."""
   path.parent.mkdir(parents=True, exist_ok=True)
   path.write_text(text, encoding="utf-8")


def includeOf(docsPath):
   """A `--8<--` snippet directive for any file under docs, by its docs-relative path."""
   rel = docsPath.relative_to(DOCS).as_posix()
   return f'--8<-- "{rel}"'


def writeRowSnippet(sourcePath, rowText):
   """Write a single-row snippet (no trailing newline) for a source card; return its path."""
   target = mirrorRowPath(sourcePath)
   writeText(target, rowText)
   return target


def rowInclude(sourcePath):
   """The `--8<--` directive that reuses a card's `_row.md` snippet."""
   return includeOf(mirrorRowPath(sourcePath))


def removeEmptyDirs(root):
   """Delete empty folders under root, deepest first."""
   for folder in sorted(root.rglob("*"), reverse=True):
      if folder.is_dir() and not any(folder.iterdir()):
         folder.rmdir()


def pruneRows(mirrorRoot, keptRowPaths):
   """Delete `*_row.md` under mirrorRoot with no live source, then drop emptied folders."""
   kept = set(str(p) for p in keptRowPaths)
   removed = 0
   if mirrorRoot.exists():
      for path in sorted(mirrorRoot.rglob("*" + ROW_SUFFIX)):
         if str(path) not in kept:
            path.unlink()
            removed = removed + 1
      removeEmptyDirs(mirrorRoot)
   return removed


def pruneBodies(mirrorRoot, keptBodyPaths):
   """Delete body snippets (any `.md` that isn't a row or aggregate) under mirrorRoot with no live source."""
   kept = set(str(p) for p in keptBodyPaths)
   removed = 0
   if mirrorRoot.exists():
      for path in sorted(mirrorRoot.rglob("*.md")):
         isAggregate = path.name in AGGREGATE_NAMES
         isRow = path.name.endswith(ROW_SUFFIX)
         isBody = not isAggregate and not isRow
         if isBody and str(path) not in kept:
            path.unlink()
            removed = removed + 1
   return removed
