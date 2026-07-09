"""Generate magic-item (infusion) table-row snippets + per-rarity example tables.

Row schema: | Item | Type | Rarity | Attunement |
Type/Attunement come from the card subtitle (`<Rarity> <Type>[, Attunement[ (<qual>)]]`);
Rarity comes from the source subdir, which is unambiguous where the subtitle's leading word is not
(e.g. "Very Rare").
"""

import genSnippetCommon as C

# Artifacts and Unique items are left hand-maintained: complex and stable enough that they
# don't warrant regeneration, so they stay on their existing snippets.
RARITIES = ("common", "uncommon", "rare", "very-rare", "legendary")
HEADER = ("Item", "Type", "Rarity", "Attunement")
SOURCE_ROOT = C.DOCS / "item/magic/infusion"
MIRROR_ROOT = C.MIRROR / "item/magic/infusion"
ATTUNE_MARK = ", Attunement"
CONSUMABLE_MARK = ", Consumable"


def DisplayRarity(dirName):
    """Subdir name -> display rarity, e.g. 'very-rare' -> 'Very Rare'."""
    words = [word.capitalize() for word in dirName.split("-")]
    return " ".join(words)


def TypeAndAttunement(subtitle, rarityDisplay):
    """Split a magic-item subtitle into (Type, Attunement) given its display rarity."""
    prefix = rarityDisplay + " "
    body = subtitle[len(prefix):] if subtitle.startswith(prefix) else subtitle
    hasAttune = ATTUNE_MARK in body
    rawType = (body.split(ATTUNE_MARK, 1)[0] if hasAttune else body).strip()
    typeText = rawType[:-len(CONSUMABLE_MARK)].strip() if rawType.endswith(CONSUMABLE_MARK) else rawType
    qualifier = body.split(ATTUNE_MARK, 1)[1].strip() if hasAttune else ""
    attunement = ("Yes " + qualifier).strip() if hasAttune else "No"
    return (typeText, attunement)


def SourceCards(rarity):
    """Card files for one rarity, excluding its index and any legacy `_list.md` snippets."""
    found = []
    for path in sorted((SOURCE_ROOT / rarity).glob("*.md")):
        keep = path.name != "index.md" and not path.name.endswith("_list.md")
        if keep:
            found.append(path)
    return found


def Main():
    written = []
    for rarity in RARITIES:
        rarityDisplay = DisplayRarity(rarity)
        rows = []
        for path in SourceCards(rarity):
            card = C.ReadCard(path)
            typeText, attunement = TypeAndAttunement(card.subtitle, rarityDisplay)
            row = C.RenderRow([C.Link(card), typeText, rarityDisplay, attunement])
            written.append(C.WriteSnippet(path, row))
            rows.append(row)
        C.WriteText(MIRROR_ROOT / rarity / "_index_table.md", C.TableBlock(HEADER, rows))
    removed = C.PruneOrphans(MIRROR_ROOT, written)
    print(f"Magic items: wrote {len(written)} rows, pruned {removed}.")


if __name__ == "__main__":
    Main()
