"""Generate bestiary snippets: flattened stat-block bodies, table rows, and level/type/summon indices.

Creature entries live under `bestiary/level/<N>/<name>.md` and `bestiary/summon/<name>.md`. Unlike the
other card types they open with an h1 lore intro (and optional h2/h5 lore); the stat blocks themselves are
the h3 sections. Each h3 block is extracted and flattened (h3->h5, deeper->h6) into its own insertion
snippet — one per variant form, named by the heading slug (bestial-spirit-land.md, ...-sea.md, ...-sky.md)
— so a host page (a summoning feature, a ship, an item) can nest a form while the source page still renders.

Indices mirror the spell layout:
- level/<N>: creatures of one level, grouped by first letter (letter jump-nav).  | Creature | Level | Type |
- type/<type>: creatures of one type across all levels, grouped by level.        | Creature | Level | Type |
- summon: player-only creatures with no level, grouped by first letter.          | Summon | Variants | Source |
Summons carry no creature level, so they appear only in the summon index, never in level/type.
"""

import re

import genSnippetCommon as C

BESTIARY_ROOT = C.DOCS / "bestiary"
MIRROR_ROOT = C.MIRROR / "bestiary"
LEVEL_ROOT = BESTIARY_ROOT / "level"
SUMMON_ROOT = BESTIARY_ROOT / "summon"

# The 14 creature types (parallel to the type/ index pages); each gets a table even when empty so its
# `--8<--` include always resolves.
CREATURE_TYPES = (
    "Aberration", "Beast", "Celestial", "Construct", "Dragon", "Elemental", "Fey",
    "Fiend", "Giant", "Humanoid", "Monstrosity", "Ooze", "Plant", "Undead",
)
LEVEL_HEADER = ("Creature", "Level", "Type")
SUMMON_HEADER = ("Summon", "Variants", "Source")


def FirstH3Index(lines):
    """Index of the first h3 line (the stat-block heading), or -1 when there is none."""
    found = -1
    for i, line in enumerate(lines):
        if found < 0 and C.HeadingLevel(line) == 3:
            found = i
    return found


def StatSubtitle(text):
    """The '<Size> <Type>, <Alignment>' line directly under the first h3."""
    lines = text.split("\n")
    start = FirstH3Index(lines)
    hasLine = 0 <= start < len(lines) - 1
    return lines[start + 1].strip() if hasLine else ""


def CreatureTypes(text):
    """Creature type words present in the stat-block subtitle, in the order they appear there."""
    subtitle = StatSubtitle(text)
    present = [(subtitle.find(t), t) for t in CREATURE_TYPES if re.search(rf"\b{t}\b", subtitle)]
    return [t for (pos, t) in sorted(present)]


def CreatureLevel(text):
    """The numeric creature level from the Traits `Level` row."""
    value = C.MetaValue(text, "Level")
    return value if value is not None else C.BLANK


def H3Titles(text):
    """Every h3 heading title in a card (the stat block's variant forms)."""
    return [line.lstrip("#").strip() for line in text.split("\n") if C.HeadingLevel(line) == 3]


def VariantLabel(cardTitle, h3Title):
    """The short variant name: the h3 title with the shared creature-name prefix stripped."""
    if h3Title.startswith(cardTitle):
        return h3Title[len(cardTitle):].lstrip(" :-–—") or h3Title
    return h3Title


def Variants(card):
    """Variant forms of a summon as links to each form's heading, or blank for a single form."""
    titles = H3Titles(card.text)
    if len(titles) <= 1:
        return C.BLANK
    links = [f"[{VariantLabel(card.title, t)}]({card.sitePath}#{C.Slugify(t)})" for t in titles]
    return ", ".join(links)


def SourceLabel(source):
    """Human-readable label for a `source:` path, derived from its anchor or file stem."""
    url, _, anchor = source.partition("#")
    if anchor:
        slug = anchor
    else:
        stem = url.rstrip("/").split("/")[-1]
        stem = stem[:-3] if stem.endswith(".md") else stem
        slug = url.rstrip("/").split("/")[-2] if stem == "index" else stem
    slug = re.sub(r"^\d+-", "", slug)  # drop a leading feature-level prefix like "1-"
    return " ".join(word.capitalize() for word in slug.replace("-", " ").split())


def Source(card):
    """The feature/spell that summons a creature, as a link from the `source:` front-matter field.

    An optional `label:` field overrides the link text exactly; otherwise it is derived from the path.
    """
    meta = C.FrontMatter(card.text)
    source = meta.get("source")
    if not source:
        return C.BLANK
    label = meta.get("label") or SourceLabel(source)
    return f"[{label}]({source})"


def LevelRow(card):
    """`| Creature | Level | Type |` row for a leveled creature."""
    return C.RenderRow([C.Link(card), CreatureLevel(card.text), ", ".join(CreatureTypes(card.text))])


def SummonRow(card):
    """`| Summon | Variants | Source |` row for a summon."""
    return C.RenderRow([C.Link(card), Variants(card), Source(card)])


def VariantBlocks(text):
    """(h3Title, blockText) for each h3 stat block, split at the next h3/h2/h1 or end of file."""
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines) if C.HeadingLevel(line) == 3]
    blocks = []
    for n, start in enumerate(starts):
        end = len(lines)
        for j in range(start + 1, len(lines)):
            if C.HeadingLevel(lines[j]) in (1, 2, 3):
                end = j
                break
        title = lines[start].lstrip("#").strip()
        block = "\n".join(lines[start:end]).rstrip("\n") + "\n"
        blocks.append((title, block))
    return blocks


def WriteBodies(card):
    """Write one flattened (h5) insertion snippet per variant, named by its heading slug; return paths."""
    mirrorDir = C.MIRROR / card.path.parent.relative_to(C.DOCS)
    paths = []
    for title, block in VariantBlocks(card.text):
        target = mirrorDir / (C.Slugify(title) + ".md")
        C.WriteText(target, C.DemoteHeadings(block))
        paths.append(target)
    return paths


MAX_LEVEL = 30


def LevelJumpNav(active):
    """Jump nav over `Level 0 · 1 … 20`; levels in `active` link to their `## Level <N>` section."""
    buckets = [(("Level 0" if n == 0 else str(n)), f"level-{n}") for n in range(MAX_LEVEL + 1)]
    return C.JumpNav(buckets, active)


def LevelGrouped(header, records):
    """Records (level, title, row) as a level jump-nav + `## Level <N>` sections, by level then name.

    Always leads with the jump nav (every level shown, active ones linked); an empty record set
    yields the nav alone so the include still resolves.
    """
    ordered = sorted(records, key=lambda entry: (entry[0], entry[1].lower()))
    active = set(f"level-{level}" for (level, title, row) in ordered)
    parts = [LevelJumpNav(active), ""]
    for level in sorted(set(level for (level, title, row) in ordered)):
        rows = [row for (lv, title, row) in ordered if lv == level]
        parts.append(f"## Level {level}")
        parts.append("")
        parts.append(C.TableBlock(header, rows).rstrip("\n"))
        parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


def LevelDirs():
    """Numeric level folders under bestiary/level, in ascending order."""
    dirs = [p for p in LEVEL_ROOT.iterdir() if p.is_dir() and p.name.isdigit()]
    return sorted(dirs, key=lambda p: int(p.name))


def CreatureFiles(folder):
    """Creature card files in a folder, excluding the index page."""
    return [p for p in sorted(folder.glob("*.md")) if p.name != "index.md"]


def Main():
    rows = []
    bodies = []
    byType = {t: [] for t in CREATURE_TYPES}

    # Leveled creatures: row + flattened body per creature, one letter-grouped table per level.
    for folder in LevelDirs():
        levelNum = int(folder.name)
        levelRecords = []
        for path in CreatureFiles(folder):
            card = C.ReadCard(path)
            row = LevelRow(card)
            rows.append(C.WriteSnippet(path, row))
            bodies.extend(WriteBodies(card))
            include = C.RowInclude(path)
            levelRecords.append((card.title, include))
            for t in CreatureTypes(card.text):
                byType[t].append((levelNum, card.title, include))
        C.WriteText(MIRROR_ROOT / "level" / folder.name / "_index_table.md",
                    C.LetterGrouped(LEVEL_HEADER, levelRecords))

    # One level-grouped table per creature type (emitted for every type so every include resolves).
    for t in CREATURE_TYPES:
        C.WriteText(MIRROR_ROOT / "type" / t.lower() / "_index_table.md",
                    LevelGrouped(LEVEL_HEADER, byType[t]))

    # Summons: row + flattened body per summon, one letter-grouped table.
    summonRecords = []
    for path in CreatureFiles(SUMMON_ROOT):
        card = C.ReadCard(path)
        row = SummonRow(card)
        rows.append(C.WriteSnippet(path, row))
        bodies.extend(WriteBodies(card))
        summonRecords.append((card.title, C.RowInclude(path)))
    C.WriteText(MIRROR_ROOT / "summon" / "_index_table.md", C.LetterGrouped(SUMMON_HEADER, summonRecords))

    prunedBodies = C.PruneBodies(MIRROR_ROOT, bodies)
    prunedRows = C.PruneOrphans(MIRROR_ROOT, rows)
    print(f"Bestiary: wrote {len(rows)} rows, {len(bodies)} bodies, "
          f"pruned {prunedRows} rows + {prunedBodies} bodies.")


if __name__ == "__main__":
    Main()
