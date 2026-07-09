"""Regenerate every snippet in one command:

    python3 scripts/genAll.py

Runs all seven section generators (magic items, spells, feats, subfeatures, items, components,
protocols). Each is idempotent and self-pruning, so this is safe to run any time sources change.
"""

import genComponentSnippet
import genFeatSnippet
import genItemSnippet
import genMagicItemSnippet
import genProtocolSnippet
import genSpellSnippet
import genSubfeatureSnippet

GENERATORS = (
    genMagicItemSnippet,
    genSpellSnippet,
    genFeatSnippet,
    genSubfeatureSnippet,
    genItemSnippet,
    genComponentSnippet,
    genProtocolSnippet,
)


def Main():
    for generator in GENERATORS:
        generator.Main()


if __name__ == "__main__":
    Main()
