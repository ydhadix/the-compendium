"""Generic inline-hub lister.

For each registered `_<category>/` source dir of build-excluded leaves (authored at their final
heading level), write one `_list.md` aggregate into the mirror that `--8<--` includes every leaf.
The sibling hub page includes that single file, so adding a leaf refreshes the hub with no edits.
"""

import re

import genSnippetCommon as C

FLAT = "flat"
LETTER = "letter"
LEVEL = "level"

PREREQ_LEVEL_RE = re.compile(r"Level (\d+)")
NO_PREREQ_LEVEL = 1

# (source dir relative to docs, grouping). FLAT = one alphabetical list; LETTER = A-Z sections
# behind a jump rail (for large hubs).
HUBS = (
   ("character/feat/fighting-style/_initiate", FLAT),
   ("character/feat/fighting-style/_expert", FLAT),
   ("character/feat/fighting-style/_master", FLAT),
   ("character/feat/_ancestry", LETTER),
   ("character/feat/_general", LETTER),
   ("character/feat/_origin", LETTER),
   ("character/class/warlock/_invocation", LEVEL),
   ("character/class/ranger/_imprint", LEVEL),
   ("character/class/sorcerer/_metamagic", FLAT),
   ("rules/_condition", FLAT),
   ("spelljammer/creation/component/_pilot", FLAT),
   ("spelljammer/creation/component/_quartermaster", FLAT),
   ("spelljammer/creation/component/_spelljammer", FLAT),
)


def leafCards(sourceDir):
   """Every markdown leaf in a `_<category>/` source dir, sorted by title."""
   cards = [C.readCard(path) for path in sorted(sourceDir.glob("*.md"))]
   ordered = sorted(cards, key=lambda card: card.title.lower())
   return ordered


def flatList(cards):
   """An alphabetical list of leaf `--8<--` includes, blank-line separated."""
   parts = []
   for card in cards:
      parts.append(C.includeOf(card.path))
      parts.append("")
   result = "\n".join(parts).rstrip("\n") + "\n"
   return result


def letterList(cards):
   """A letter jump-nav + `## <Letter>` sections of leaf includes, alphabetical."""
   letters = sorted(set(C.letterKey(card.title) for card in cards))
   active = set(letter.lower() if letter != "0-9" else "0-9" for letter in letters)
   parts = [C.letterJumpNav(active), ""]
   for letter in letters:
      inLetter = [card for card in cards if C.letterKey(card.title) == letter]
      parts.append(f"## {letter}")
      parts.append("")
      for card in inLetter:
         parts.append(C.includeOf(card.path))
         parts.append("")
   result = "\n".join(parts).rstrip("\n") + "\n"
   return result


def prereqLevel(card):
   """The prerequisite level from a card's subtitle (`Prerequisite: Level N ...`), or 1 when absent."""
   match = PREREQ_LEVEL_RE.search(card.subtitle) if card.subtitle else None
   return int(match.group(1)) if match else NO_PREREQ_LEVEL


def levelList(cards):
   """`### Level N` sections of leaf includes, grouped by prerequisite level then title."""
   levels = sorted(set(prereqLevel(card) for card in cards))
   parts = []
   for level in levels:
      inLevel = sorted((c for c in cards if prereqLevel(c) == level), key=lambda c: c.title.lower())
      parts.append(f"### Level {level}")
      parts.append("")
      for card in inLevel:
         parts.append(C.includeOf(card.path))
         parts.append("")
   result = "\n".join(parts).rstrip("\n") + "\n"
   return result


def buildList(cards, grouping):
   """The aggregate text for a hub's leaves under the chosen grouping."""
   if grouping == LETTER:
      result = letterList(cards)
   elif grouping == LEVEL:
      result = levelList(cards)
   else:
      result = flatList(cards)
   return result


def buildHub(sourceDirRel, grouping):
   """Write one hub's `_list.md` aggregate; return its mirror path."""
   cards = leafCards(C.DOCS / sourceDirRel)
   text = buildList(cards, grouping)
   target = C.MIRROR / sourceDirRel / C.LIST_NAME
   C.writeText(target, text)
   return target


def pruneLists(keptLists):
   """Delete `_list.md` aggregates under the mirror that no hub produced this run."""
   kept = set(str(p) for p in keptLists)
   removed = 0
   if C.MIRROR.exists():
      for path in sorted(C.MIRROR.rglob(C.LIST_NAME)):
         if str(path) not in kept:
            path.unlink()
            removed = removed + 1
   return removed


def main():
   written = [buildHub(sourceDirRel, grouping) for sourceDirRel, grouping in HUBS]
   removed = pruneLists(written)
   print(f"Inline hubs: wrote {len(written)} lists, pruned {removed}.")


if __name__ == "__main__":
   main()
