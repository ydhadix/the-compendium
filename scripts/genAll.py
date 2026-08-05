"""Regenerate every snippet in one command:

    python3 scripts/genAll.py

Runs the metadata index-table generators — genTables (races, items, magic items, protocols),
genSpells, and genBestiary — plus the generic inline-hub lister. Each is idempotent and
self-pruning, so this is safe to run any time sources change.
"""

import genBestiary
import genInlineHub
import genSpells
import genTables

GENERATORS = (
   genTables,
   genSpells,
   genBestiary,
   genInlineHub,
)


def main():
   for generator in GENERATORS:
      generator.main()


if __name__ == "__main__":
   main()
