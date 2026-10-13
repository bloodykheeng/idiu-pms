"""Cut the static font weights the screens use out of the downloaded variable fonts.

Run once after cloning (the results are committed, so normally never):

    python make_fonts.py

The static files serve two jobs: kit.tw() measures text with them, and fonts.py subsets and embeds them
in every SVG, so a screen looks the same on any device. All three families are SIL Open Font Licence
(see fonts/OFL-*.txt), which allows embedding and redistribution.
"""
from __future__ import annotations

import os

from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "fonts")
OUT = os.path.join(SRC, "static")

# (variable source, output name, axis settings)
CUTS = [
    ("Figtree[wght].ttf", "Figtree-400.ttf", {"wght": 400}),
    ("Figtree[wght].ttf", "Figtree-500.ttf", {"wght": 500}),
    ("Figtree[wght].ttf", "Figtree-600.ttf", {"wght": 600}),
    ("Figtree[wght].ttf", "Figtree-700.ttf", {"wght": 700}),
    ("BricolageGrotesque[opsz,wdth,wght].ttf", "Bricolage-600.ttf", {"opsz": 36, "wdth": 100, "wght": 600}),
    ("BricolageGrotesque[opsz,wdth,wght].ttf", "Bricolage-700.ttf", {"opsz": 36, "wdth": 100, "wght": 700}),
]
COPIES = [("IBMPlexMono-Medium.ttf", "PlexMono-500.ttf"), ("IBMPlexMono-SemiBold.ttf", "PlexMono-600.ttf")]


def main():
    os.makedirs(OUT, exist_ok=True)
    for src, name, axes in CUTS:
        font = instantiateVariableFont(TTFont(os.path.join(SRC, src)), axes)
        font.save(os.path.join(OUT, name))
        print(name)
    for src, name in COPIES:
        TTFont(os.path.join(SRC, src)).save(os.path.join(OUT, name))
        print(name)


if __name__ == "__main__":
    main()
