"""Regenerate every snippet in one command:

    python3 scripts/genAll.py

Runs all six section generators (magic items, spells, feats, subfeatures, items, components).
Each is idempotent and self-pruning, so this is safe to run any time sources change.
"""

import genComponentSnippet
import genFeatSnippet
import genItemSnippet
import genMagicItemSnippet
import genSpellSnippet
import genSubfeatureSnippet

GENERATORS = (
    genMagicItemSnippet,
    genSpellSnippet,
    genFeatSnippet,
    genSubfeatureSnippet,
    genItemSnippet,
    genComponentSnippet,
)


def Main():
    for generator in GENERATORS:
        generator.Main()


if __name__ == "__main__":
    Main()
