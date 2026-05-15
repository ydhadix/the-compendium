#!/usr/bin/env python3
"""
Generate docs/magic-items/{rarity}.md pages by scanning all snippet files in
docs/magic-items/_infusions/*.md and grouping them by rarity.

Run from any directory:
    python3 docs/magic-items/_infusions/gen_rarity_pages.py
"""

import os
import re

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
ITEMS_DIR   = os.path.dirname(SCRIPT_DIR)          # docs/magic-items/

# Rarity order and output file names
RARITIES = [
    ("common",    "common",    "Common Magic Items"),
    ("uncommon",  "uncommon",  "Uncommon Magic Items"),
    ("rare",      "rare",      "Rare Magic Items"),
    ("very rare", "very-rare", "Very Rare Magic Items"),
    ("legendary", "legendary", "Legendary Magic Items"),
    ("artifact",  "artifacts", "Artifacts"),
]


def rarity_from_file(filepath):
    """Return the lowercase rarity string from the first table header row."""
    with open(filepath) as f:
        for line in f:
            # Match the first table cell: | Rarity Type... |
            m = re.match(r'\|\s*([^|]+)\|', line)
            if m:
                cell = m.group(1).strip().lower()
                for rarity, _, _ in RARITIES:
                    if cell.startswith(rarity):
                        return rarity
    return None


def main():
    # Collect snippets by rarity, sorted alphabetically by filename
    rarity_files = {r: [] for r, _, _ in RARITIES}

    for filename in sorted(f for f in os.listdir(SCRIPT_DIR) if f.endswith(".md")):
        filepath = os.path.join(SCRIPT_DIR, filename)
        rarity = rarity_from_file(filepath)
        if rarity and rarity in rarity_files:
            rarity_files[rarity].append(filename)

    for rarity, page_slug, page_title in RARITIES:
        files = rarity_files[rarity]
        if not files:
            continue

        lines = [f"# {page_title}", ""]
        for filename in files:
            lines.append(f'--8<-- "magic-items/_infusions/{filename}"')
            lines.append("")

        content = "\n".join(lines)
        output_path = os.path.join(ITEMS_DIR, f"{page_slug}.md")
        with open(output_path, "w") as f:
            f.write(content)

        print(f"  magic-items/{page_slug}.md  ({len(files)} items)")

    print(f"Done — {len(RARITIES)} pages written.")


if __name__ == "__main__":
    main()
