"""Embed the fonts a screen uses inside its SVG.

An SVG shown through <img> (as the viewer does) cannot fetch web fonts, so each screen carries its own:
every (family, weight) it used, subset to exactly the characters it drew, as base64 WOFF2 in an @font-face
rule. A screen costs a few KB of font and looks identical on any laptop or phone.
"""
from __future__ import annotations

import base64
import io

from fontTools import subset
from fontTools.ttLib import TTFont

from kit import FAMILY, font_file

_cache: dict[tuple, str] = {}


def _woff2(family: str, weight: int, chars: str) -> str:
    key = (family, weight, chars)
    if key not in _cache:
        font = TTFont(font_file(family, weight))
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["kern", "liga", "calt", "tnum", "lnum"]
        opts.name_IDs = []
        opts.notdef_outline = True
        opts.drop_tables += ["meta"]
        sub = subset.Subsetter(opts)
        sub.populate(text=chars + " ")
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        _cache[key] = base64.b64encode(buf.getvalue()).decode()
    return _cache[key]


def style(used: dict[tuple[str, int], set[str]]) -> str:
    """The <style> block for a screen, or '' when it drew no text."""
    rules = []
    for (family, weight), chars in sorted(used.items()):
        if not chars:
            continue
        data = _woff2(family, weight, "".join(sorted(chars)))
        rules.append(f"@font-face{{font-family:'{FAMILY[family][0]}';font-weight:{weight};font-style:normal;"
                     f"src:url(data:font/woff2;base64,{data}) format('woff2')}}")
    return f"<style>{''.join(rules)}</style>" if rules else ""
