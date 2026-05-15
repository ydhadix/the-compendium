#!/usr/bin/env python3
"""
Extract Adventuring Gear items from remaining/gear-glossary.md into
individual snippet files under docs/equipment/_gear/.

Run from any directory:
    python3 docs/equipment/_gear/extract_gear.py
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR   = os.path.dirname(os.path.dirname(SCRIPT_DIR))
RAW_FILE   = os.path.join(os.path.dirname(DOCS_DIR), "remaining", "gear-glossary.md")
OUT_DIR    = SCRIPT_DIR

ACTION_PREFIXES = (
    "Utilize Action",
    "Bonus Action",
    "Reaction",
    "Free Action",
    "Magic Action",
    "Short Rest",
    "Long Rest",
)


def slugify(name):
    s = name.lower()
    s = re.sub(r"[‘’‚‛',.]", "", s)  # straight + curly apostrophes
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") + ".md"


def extract_cost(heading):
    """Return (name, cost_str) by stripping trailing (...)."""
    m = re.search(r'\(([^)]+)\)\s*$', heading)
    if m:
        return heading[:m.start()].strip(), m.group(1)
    return heading.strip(), None


def add_paragraph_breaks(text):
    """
    Insert blank lines between adjacent non-blank lines, except inside
    table blocks (consecutive lines starting with |) which must stay together.
    """
    lines = text.split("\n")
    result = []
    for i, line in enumerate(lines):
        prev = result[-1] if result else ""
        # Don't insert blank line between consecutive table rows, but DO
        # allow a blank line before the first row of a table.
        in_table = line.startswith("|") and prev.startswith("|")
        if i > 0 and line.strip() and prev.strip() and not in_table:
            result.append("")
        result.append(line)
    return "\n".join(result)


def convert_bold_table(text):
    """
    Convert blocks of >=2 consecutive **Key**: Value lines into a markdown
    table (first line = header row, rest = data rows).
    """
    lines = text.split("\n")
    result = []
    i = 0
    while i < len(lines):
        if re.match(r"\*\*[^*]+\*\*:\s*.+", lines[i]):
            block = []
            while i < len(lines) and re.match(r"\*\*[^*]+\*\*:\s*.+", lines[i]):
                m = re.match(r"\*\*([^*]+)\*\*:\s*(.+)", lines[i])
                if m:
                    block.append((m.group(1), m.group(2)))
                i += 1
            if len(block) >= 2:
                hk, hv = block[0]
                result.append(f"| {hk} | {hv} |")
                result.append("|---|---|")
                for k, v in block[1:]:
                    result.append(f"| {k} | {v} |")
            else:
                k, v = block[0]
                result.append(f"**{k}**: {v}")
            continue
        result.append(lines[i])
        i += 1
    return "\n".join(result)


def format_snippet(name, cost, description):
    lines = [f"### {name}", ""]
    if cost:
        lines += [f"**cost**: {cost}", ""]
    if description:
        # Process description
        desc = description.strip()
        desc = convert_bold_table(desc)
        desc = add_paragraph_breaks(desc)
        lines.append(desc)
    return "\n".join(lines) + "\n"


def main():
    with open(RAW_FILE) as f:
        raw = f.read()

    # Extract the Adventuring Gear section
    sec_m = re.search(r"^# Adventuring Gear\n", raw, re.MULTILINE)
    if not sec_m:
        print("ERROR: '# Adventuring Gear' section not found")
        return

    next_sec = re.search(r"^# ", raw[sec_m.end():], re.MULTILINE)
    section = raw[sec_m.end(): sec_m.end() + next_sec.start()] if next_sec else raw[sec_m.end():]

    # Split by ### headings
    item_re   = re.compile(r"^### (.+)$", re.MULTILINE)
    item_hits = list(item_re.finditer(section))

    os.makedirs(OUT_DIR, exist_ok=True)
    seen = {}
    count = 0

    for idx, hit in enumerate(item_hits):
        heading = hit.group(1).strip()
        istart  = hit.end()
        iend    = item_hits[idx + 1].start() if idx + 1 < len(item_hits) else len(section)
        desc    = section[istart:iend].strip()

        name, cost = extract_cost(heading)
        slug = slugify(name)

        if slug in seen:
            base = slug[:-3]
            slug = f"{base}-2.md"
            print(f"  WARNING: Duplicate slug for '{name}' — saved as {slug}")

        seen[slug] = True
        snippet = format_snippet(name, cost, desc)

        with open(os.path.join(OUT_DIR, slug), "w") as f:
            f.write(snippet)

        print(f"  {slug}")
        count += 1

    print(f"\nDone — {count} snippet files written to {OUT_DIR}")


if __name__ == "__main__":
    main()
