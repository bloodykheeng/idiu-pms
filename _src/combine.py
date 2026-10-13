"""Write all-screens.svg: every IDIU screen on one canvas, for a single import into Adobe XD.

Each screen embeds its own font subset; stacked in one file those rules would clash (same family and
weight, different characters), so they are stripped and one subset covering every screen is embedded.
"""
import glob
import html
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.dirname(HERE))

import fonts  # noqa: E402
from kit import FAMILY  # noqa: E402

nat = lambda f: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", os.path.basename(f))]
web = sorted(glob.glob("web/*.svg"), key=nat)
NAME_TO_FAMILY = {v[0]: k for k, v in FAMILY.items()}
TEXT = re.compile(r"<text\b[^>]*font-family=\"'([^']+)'[^\"]*\"[^>]*font-weight=\"(\d+)\"[^>]*>(.*?)</text>", re.S)
GAP, LABEL, COLS, W, H = 200, 60, 4, 1920, 1080

used, parts = {}, []
for i, f in enumerate(web):
    t = open(f, encoding="utf-8").read()
    for fam, weight, content in TEXT.findall(t):
        used.setdefault((NAME_TO_FAMILY[fam], int(weight)), set()).update(html.unescape(content))
    t = re.sub(r"^.*?<svg[^>]*>\s*", "", t, flags=re.S)
    t = re.sub(r"</svg>\s*$", "", t)
    t = re.sub(r"<title>.*?</title>", "", t)
    t = re.sub(r"<style>.*?</style>", "", t, flags=re.S)
    x = (i % COLS) * (W + GAP)
    y = (i // COLS) * (H + GAP + LABEL) + LABEL
    n = os.path.basename(f)[:-4]
    parts.append(f'<text x="{x}" y="{y - 16}" font-family="Figtree" font-size="36" font-weight="600" fill="#102A1E">{n}</text>')
    parts.append(f'<g id="{n}" transform="translate({x} {y})">{t}</g>')
used[("body", 600)] = used.get(("body", 600), set()) | set("".join(os.path.basename(f)[:-4] for f in web))

TW = COLS * W + (COLS - 1) * GAP
TH = ((len(web) + COLS - 1) // COLS) * (H + GAP + LABEL) + LABEL
with open("all-screens.svg", "w", encoding="utf-8") as out:
    out.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}">\n'
              f"<defs>{fonts.style(used)}</defs>\n" + "\n".join(parts) + "\n</svg>\n")
print(len(web), "screens in all-screens.svg", os.path.getsize("all-screens.svg") // 1024, "KB")
