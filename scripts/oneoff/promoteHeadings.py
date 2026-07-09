"""Phase 0 (one-time): promote fighting-style and spelljammer-component card titles h5 -> h3.

Each such card holds exactly one h5 (its title) plus h6 sub-blocks; only the title moves.
"""

from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"
OLD_TITLE = "##### "
NEW_TITLE = "### "
CARD_GLOBS = (
    "character/feat/fighting-style/*/*.md",
    "spelljammer/component/*/*.md",
)


def PromoteTitle(text):
    """Rewrite the first h5 line (the card title) to h3, leaving h6 sub-blocks untouched."""
    lines = text.split("\n")
    rewritten = []
    moved = False
    for line in lines:
        isTitle = (not moved) and line.startswith(OLD_TITLE)
        if isTitle:
            rewritten.append(NEW_TITLE + line[len(OLD_TITLE):])
            moved = True
        else:
            rewritten.append(line)
    result = "\n".join(rewritten)
    return result


def CardFiles():
    """Every card file across the target globs, excluding each folder's index.md."""
    found = []
    for glob in CARD_GLOBS:
        for path in sorted(DOCS.glob(glob)):
            if path.name != "index.md":
                found.append(path)
    return found


def Main():
    changed = 0
    for path in CardFiles():
        original = path.read_text(encoding="utf-8")
        promoted = PromoteTitle(original)
        if promoted != original:
            path.write_text(promoted, encoding="utf-8")
            changed = changed + 1
    print(f"Promoted {changed} card titles h5 -> h3.")


if __name__ == "__main__":
    Main()
