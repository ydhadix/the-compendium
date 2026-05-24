#!/usr/bin/env python3
"""
Generate docs/magic-items/{rarity}.md pages by scanning snippet files in
docs/magic-items/_infusions/_{rarity}/ subfolders.

Run from any directory:
    python3 docs/magic-items/_infusions/_gen_rarity_pages.py
"""

import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ITEMS_DIR  = os.path.dirname(SCRIPT_DIR)   # docs/magic-items/

# (subfolder, output-slug, page-title)
RARITIES = [
    ("_common",    "common",    "Common Magic Items"),
    ("_uncommon",  "uncommon",  "Uncommon Magic Items"),
    ("_rare",      "rare",      "Rare Magic Items"),
    ("_very-rare", "very-rare", "Very Rare Magic Items"),
    ("_legendary", "legendary", "Legendary Magic Items"),
    ("_artifact",  "artifact",  "Artifacts"),
]


def main():
    for subfolder, page_slug, page_title in RARITIES:
        subfolder_path = os.path.join(SCRIPT_DIR, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        files = sorted(f for f in os.listdir(subfolder_path) if f.endswith(".md"))
        if not files:
            continue

        lines = [f"# {page_title}", ""]
        for filename in files:
            lines.append(f'--8<-- "magic-items/_infusions/{subfolder}/{filename}"')
            lines.append("")

        output_path = os.path.join(ITEMS_DIR, f"{page_slug}.md")
        with open(output_path, "w") as f:
            f.write("\n".join(lines))

        print(f"  magic-items/{page_slug}.md  ({len(files)} items)")

    print(f"Done.")


if __name__ == "__main__":
    main()
