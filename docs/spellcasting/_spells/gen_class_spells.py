#!/usr/bin/env python3
"""
Generate docs/classes/{class}/spells.md for each spellcasting class by
scanning all spell snippet files in docs/spellcasting/_spells/level-*/

Run from any directory:
    python3 docs/spellcasting/_spells/gen_class_spells.py
"""

import os
import re

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
SPELLS_DIR  = SCRIPT_DIR
DOCS_DIR    = os.path.dirname(os.path.dirname(SCRIPT_DIR))
CLASSES_DIR = os.path.join(DOCS_DIR, "classes")

CLASSES = [
    "artificer", "bard", "cleric", "druid",
    "paladin", "ranger", "sorcerer", "warlock", "wizard",
]

CLASS_TITLE = {
    "artificer": "Artificer",
    "bard":      "Bard",
    "cleric":    "Cleric",
    "druid":     "Druid",
    "paladin":   "Paladin",
    "ranger":    "Ranger",
    "sorcerer":  "Sorcerer",
    "warlock":   "Warlock",
    "wizard":    "Wizard",
}

LEVELS = [
    ("level-0", "Cantrips"),
    ("level-1", "1st-Level"),
    ("level-2", "2nd-Level"),
    ("level-3", "3rd-Level"),
    ("level-4", "4th-Level"),
    ("level-5", "5th-Level"),
    ("level-6", "6th-Level"),
]


def classes_from_file(filepath):
    """Return list of class names found in the spell's header row."""
    with open(filepath) as f:
        for line in f:
            m = re.search(r'\|\s*\*([^*]+)\*\s*\|', line)
            if m:
                return [c.strip() for c in m.group(1).split(",")]
    return []


def main():
    # class_spells[cls][level_dir] = [filename, ...]
    class_spells = {cls: {} for cls in CLASSES}

    for level_dir, _ in LEVELS:
        level_path = os.path.join(SPELLS_DIR, level_dir)
        if not os.path.isdir(level_path):
            continue
        for filename in sorted(f for f in os.listdir(level_path) if f.endswith(".md")):
            filepath = os.path.join(level_path, filename)
            for cls in classes_from_file(filepath):
                if cls in class_spells:
                    class_spells[cls].setdefault(level_dir, []).append(filename)

    for cls in CLASSES:
        lines = [f"# {CLASS_TITLE[cls]} Spells", ""]

        for level_dir, heading in LEVELS:
            spells = class_spells[cls].get(level_dir, [])
            if not spells:
                continue
            lines.append(f"## {heading}")
            lines.append("")
            for filename in spells:
                lines.append(f'--8<-- "spellcasting/_spells/{level_dir}/{filename}"')
                lines.append("")

        content = "\n".join(lines)
        output_path = os.path.join(CLASSES_DIR, cls, "spells.md")
        with open(output_path, "w") as f:
            f.write(content)

        total = sum(len(v) for v in class_spells[cls].values())
        print(f"  classes/{cls}/spells.md  ({total} spells)")

    print(f"Done — {len(CLASSES)} files written.")


if __name__ == "__main__":
    main()
