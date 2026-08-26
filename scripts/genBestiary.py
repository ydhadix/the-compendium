"""Generate bestiary snippets: flattened stat-block bodies, table rows, and level/type/summon indices.

Creatures live under `bestiary/level/<N>/<name>.md` and `bestiary/summon/<name>.md`. They open with an
h1 lore intro; the stat blocks are the h3 sections. Each h3 block is extracted and flattened (h3->h5,
deeper->h6) into its own body snippet — one per variant form — so a host page (a summoning spell, a
ship) can nest a form via `--8<--` while the source page still renders. This is the one card type that
keeps runtime flattening, because each creature renders at h3 on its own page and h5 when nested.

Indices mirror the spell layout:
- level/<N>: creatures of one level, grouped by first letter.   | Creature | Level | Type |
- type/<type>: creatures of one type, grouped by level.         | Creature | Level | Type |
- summon: player-only creatures with no level, by first letter. | Summon | Variants | Source |
"""

import re

import genSnippetCommon as C

BESTIARY_ROOT = C.DOCS / "bestiary"
MIRROR_ROOT = C.MIRROR / "bestiary"
LEVEL_ROOT = BESTIARY_ROOT / "level"
SUMMON_ROOT = BESTIARY_ROOT / "summon"
MAX_LEVEL = 30

CREATURE_TYPES = (
   "Aberration", "Beast", "Celestial", "Construct", "Dragon", "Elemental", "Fey",
   "Fiend", "Giant", "Humanoid", "Monstrosity", "Ooze", "Plant", "Undead",
)
LEVEL_HEADER = ("Creature", "Level", "Type")
SUMMON_HEADER = ("Summon", "Variants", "Source")


def firstH3Index(lines):
   """Index of the first h3 line (the stat-block heading), or -1 when there is none."""
   found = -1
   for i, line in enumerate(lines):
      if found < 0 and C.headingLevel(line) == 3:
         found = i
   return found


def statSubtitle(text):
   """The '<Size> <Type>, <Alignment>' line directly under the first h3."""
   lines = text.split("\n")
   start = firstH3Index(lines)
   hasLine = 0 <= start < len(lines) - 1
   return lines[start + 1].strip() if hasLine else ""


def creatureTypesOf(text):
   """Creature type words present in the stat-block subtitle, in the order they appear."""
   subtitle = statSubtitle(text)
   present = [(subtitle.find(t), t) for t in CREATURE_TYPES if re.search(rf"\b{t}\b", subtitle)]
   return [t for (pos, t) in sorted(present)]


def creatureLevel(text):
   """The numeric creature level from the Traits `Level` row, or the em-dash blank."""
   value = C.metaValue(text, "Level")
   return value if value is not None else C.BLANK


def h3Titles(text):
   """Every h3 heading title in a card (the stat block's variant forms)."""
   return [line.lstrip("#").strip() for line in text.split("\n") if C.headingLevel(line) == 3]


def variantLabel(cardTitle, h3Title):
   """The short variant name: the h3 title with the shared creature-name prefix stripped."""
   if h3Title.startswith(cardTitle):
      stripped = h3Title[len(cardTitle):].lstrip(" :-–—")
      result = stripped if stripped != "" else h3Title
   else:
      result = h3Title
   return result


def variants(card):
   """Variant forms of a summon as links to each form's heading, or blank for a single form."""
   titles = h3Titles(card.text)
   if len(titles) <= 1:
      result = C.BLANK
   else:
      links = [f"[{variantLabel(card.title, t)}]({card.sitePath}#{C.slugify(t)})" for t in titles]
      result = ", ".join(links)
   return result


def sourceLabel(reference):
   """Human-readable label for a `source:` path, derived from its anchor or file stem."""
   url, _, anchor = reference.partition("#")
   if anchor:
      slug = anchor
   else:
      stem = url.rstrip("/").split("/")[-1]
      stem = stem[:-3] if stem.endswith(".md") else stem
      slug = url.rstrip("/").split("/")[-2] if stem == "index" else stem
   trimmed = re.sub(r"^\d+-", "", slug)
   return " ".join(word.capitalize() for word in trimmed.replace("-", " ").split())


def summonSource(card):
   """The feature/spell that summons a creature, as a link from the `source:` front-matter field."""
   meta = C.frontMatter(card.text)
   reference = meta.get("source")
   if not reference:
      result = C.BLANK
   else:
      label = meta.get("label") or sourceLabel(reference)
      result = f"[{label}]({reference})"
   return result


def levelRow(card):
   """`| Creature | Level | Type |` row for a leveled creature."""
   return C.renderRow([C.link(card), creatureLevel(card.text), ", ".join(creatureTypesOf(card.text))])


def summonRow(card):
   """`| Summon | Variants | Source |` row for a summon."""
   return C.renderRow([C.link(card), variants(card), summonSource(card)])


def variantBlocks(text):
   """(h3Title, blockText) for each h3 stat block, split at the next h3/h2/h1 or end of file."""
   lines = text.split("\n")
   starts = [i for i, line in enumerate(lines) if C.headingLevel(line) == 3]
   blocks = []
   for start in starts:
      end = len(lines)
      for j in range(start + 1, len(lines)):
         if end == len(lines) and C.headingLevel(lines[j]) in (1, 2, 3):
            end = j
      title = lines[start].lstrip("#").strip()
      block = "\n".join(lines[start:end]).rstrip("\n") + "\n"
      blocks.append((title, block))
   return blocks


def writeBodies(card):
   """Write one flattened (h5) body snippet per variant, named by its heading slug; return paths."""
   mirrorDir = C.MIRROR / card.path.parent.relative_to(C.DOCS)
   paths = []
   for title, block in variantBlocks(card.text):
      target = mirrorDir / (C.slugify(title) + ".md")
      C.writeText(target, C.demoteHeadings(block))
      paths.append(target)
   return paths


def levelJumpNav(active):
   """Jump nav over `Level 0 · 1 … 30`; levels in `active` link to their `## Level <N>` section."""
   buckets = [(("Level 0" if n == 0 else str(n)), f"level-{n}") for n in range(MAX_LEVEL + 1)]
   return C.jumpNav(buckets, active)


def levelGrouped(header, records):
   """Records (level, title, row) as a level jump-nav + `## Level <N>` sections, by level then name."""
   ordered = sorted(records, key=lambda entry: (entry[0], entry[1].lower()))
   active = set(f"level-{level}" for (level, title, row) in ordered)
   parts = [levelJumpNav(active), ""]
   for level in sorted(set(level for (level, title, row) in ordered)):
      rows = [row for (lv, title, row) in ordered if lv == level]
      parts.append(f"## Level {level}")
      parts.append("")
      parts.append(C.tableBlock(header, rows).rstrip("\n"))
      parts.append("")
   return "\n".join(parts).rstrip("\n") + "\n"


def levelDirs():
   """Numeric level folders under bestiary/level, in ascending order."""
   dirs = [p for p in LEVEL_ROOT.iterdir() if p.is_dir() and p.name.isdigit()]
   return sorted(dirs, key=lambda p: int(p.name))


def creatureFiles(folder):
   """Creature card files in a folder, excluding the index page."""
   return [p for p in sorted(folder.glob("*.md")) if p.name != "index.md"]


def buildLeveled():
   """Row + body per leveled creature and one letter-grouped table per level; return (rows, bodies, byType)."""
   rows = []
   bodies = []
   byType = {t: [] for t in CREATURE_TYPES}
   for folder in levelDirs():
      levelNum = int(folder.name)
      levelRecords = []
      for path in creatureFiles(folder):
         card = C.readCard(path)
         rows.append(C.writeRowSnippet(path, levelRow(card)))
         bodies.extend(writeBodies(card))
         include = C.rowInclude(path)
         levelRecords.append((card.title, include))
         for t in creatureTypesOf(card.text):
            byType[t].append((levelNum, card.title, include))
      C.writeTable(MIRROR_ROOT / "level" / folder.name / C.TABLE_NAME, C.letterGrouped(LEVEL_HEADER, levelRecords))
   return (rows, bodies, byType)


def buildSummons():
   """Row + body per summon and the letter-grouped summon table; return (rows, bodies)."""
   rows = []
   bodies = []
   records = []
   for path in creatureFiles(SUMMON_ROOT):
      card = C.readCard(path)
      rows.append(C.writeRowSnippet(path, summonRow(card)))
      bodies.extend(writeBodies(card))
      records.append((card.title, C.rowInclude(path)))
   C.writeTable(MIRROR_ROOT / "summon" / C.TABLE_NAME, C.letterGrouped(SUMMON_HEADER, records))
   return (rows, bodies)


def main():
   leveledRows, leveledBodies, byType = buildLeveled()
   for t in CREATURE_TYPES:
      C.writeTable(MIRROR_ROOT / "type" / t.lower() / C.TABLE_NAME, levelGrouped(LEVEL_HEADER, byType[t]))
   summonRows, summonBodies = buildSummons()
   rows = leveledRows + summonRows
   bodies = leveledBodies + summonBodies
   prunedBodies = C.pruneBodies(MIRROR_ROOT, bodies)
   prunedRows = C.pruneRows(MIRROR_ROOT, rows)
   print(f"Bestiary: wrote {len(rows)} rows, {len(bodies)} bodies, "
         f"pruned {prunedRows} rows + {prunedBodies} bodies.")


if __name__ == "__main__":
   main()
