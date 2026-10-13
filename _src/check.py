"""Check every screen before anyone clicks through it.

    python check.py        # exits 1 if anything is wrong

Builds each screen in memory (no files written) and checks:
  links       every hotspot opens a screen that exists (after !tab: / !back:; !theme is the light/dark switch)
  reach       every screen can be reached by clicking from the public Home (w80), the page with no hash
  bounds      hotspots and text stay inside the canvas
  overlap     no text is drawn over other text on the same layer (a dialog's text is a layer above the page)
  buried      no hotspot is covered by a later one that opens something else (the lower one could never be clicked)
  files       the light and dark SVG of every screen exist (run build.py first)
  sessions    signed in as each person or supplier, clicking never changes who is signed in: no screen that is
              someone else's own (another person's, another company's), nothing outside their role's menu, and their
              sidebar exists for every shared screen they can reach
  door        one front door: every public page links to Sign in; Home and Sign in link to Register; Register links
              back to Sign in; Sign in signs in every staff person and every supplier account at their own dashboard
  menus       every entry in every account's menu opens a screen of theirs (nothing visible in a menu is dead)
  forms       a form (meta write) opens only for the roles allowed to fill it in; never for the read-only Auditor
  modal       under a dialog or drawer nothing is clickable: only the dialog's own hotspots, never the sidebar's
  highlight   a list's highlighted row opens a screen everyone who sees the list may open (the presenter's cue)
"""
from __future__ import annotations

import os
import sys
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import shell  # noqa: E402
from build import OUT, screen_key, screens, slug  # noqa: E402
from data import PEOPLE, SESSIONS, SUPPLIER_MENU, SUPPLIER_SESSIONS, home_key, menu_for  # noqa: E402


def _overlaps(boxes):
    """Pairs of texts whose boxes intersect by more than a sliver (same layer only)."""
    found = []
    for i in range(len(boxes)):
        x1, y1, w1, h1, l1, t1 = boxes[i]
        for j in range(i + 1, len(boxes)):
            x2, y2, w2, h2, l2, t2 = boxes[j]
            if l1 != l2:
                continue
            ix = min(x1 + w1, x2 + w2) - max(x1, x2)
            iy = min(y1 + h1, y2 + h2) - max(y1, y2)
            if ix > 2 and iy > 3:
                small = min(w1 * h1, w2 * h2)
                if ix * iy > 0.15 * small:
                    found.append((t1, t2, round(x1), round(y1)))
    return found


def main():
    built = {}
    problems = []
    for fn in screens():
        key = screen_key(fn)
        s = fn()
        built[key] = s
        for x, y, w, h, t in s.links:
            if w <= 0 or h <= 0 or x < 0 or y < 0 or x + w > s.w + 1 or y + h > s.h + 1:
                problems.append(f"{key}: hotspot to {t} outside the canvas ({x}, {y}, {w}, {h})")
        for x, top, w, h, layer, text in s.boxes:
            if x < -1 or x + w > s.w + 1 or top < -1 or top + h > s.h + 1:
                problems.append(f"{key}: text off the canvas: “{text[:50]}” at ({x:.0f}, {top:.0f})")
        for a, b, x, y in _overlaps(s.boxes):
            problems.append(f"{key}: text overlaps at ({x}, {y}): “{a[:40]}” × “{b[:40]}”")
        for i, (x, y, w, h, t) in enumerate(s.links):
            for x2, y2, w2, h2, t2 in s.links[i + 1:]:
                if t2 != t and x2 <= x and y2 <= y and x2 + w2 >= x + w and y2 + h2 >= y + h:
                    problems.append(f"{key}: hotspot to {t} at ({x}, {y}) is buried under one to {t2}")
        name = slug(s.title)
        for folder in ("web", "web-dark"):
            if not os.path.exists(os.path.join(OUT, folder, name + ".svg")):
                problems.append(f"{key}: {folder}/{name}.svg is missing (run build.py)")

    # every person's sidebar, as the prototype lays it over shared screens
    chromes = {p: {lab: shell.chrome(p, lab) for lab in menu_for(p)} for p in SESSIONS}

    def dest_of(t):
        return t.split(":", 1)[1] if t.startswith(("!tab:", "!back:")) else t

    for key, s in list(built.items()) + [(f"sidebar {p}/{lab}", c) for p, cs in chromes.items() for lab, c in cs.items()]:
        for *_, t in s.links:
            if t != "!theme" and dest_of(t) not in built:
                problems.append(f"{key}: hotspot opens {t}, which does not exist")

    def is_console(k):
        """A shared staff screen: the viewer lays the signed-in person's sidebar over it."""
        return built[k].meta["area"] == "staff"

    def in_session(k):
        """Opening it keeps (or starts) a session: an account's own screen or a shared console screen."""
        return bool(built[k].meta["owner"]) or is_console(k)

    def role(p):
        return PEOPLE[p][2] if p in SESSIONS else "Supplier"

    def resolve(k, p):
        """A record with the signed-in person's own copy (w21c-samuel) opens that copy, as the viewer does."""
        return f"{k}-{p}" if f"{k}-{p}" in built else k

    def allowed(p, k):
        m = built[k].meta
        if m["owner"]:
            return m["owner"] == p
        if m["write"] and role(p) not in m["write"]:
            return False
        if is_console(k):
            return p in SESSIONS and m["label"] in menu_for(p)
        return True   # the public site and sign in: leaving the session

    for k, s in built.items():
        if s.meta["area"] not in ("public", "auth", "staff", "supplier"):
            problems.append(f"{k}: no area (public, auth, staff or supplier)")

    x0, y0, w0, h0 = shell.IDENT

    def under(link):
        x, y, *_ = link
        return x < shell.SB or (x >= x0 - 1 and y < y0 + h0)

    reached = {"w80"}
    for p in SESSIONS + SUPPLIER_SESSIONS:
        seen, todo = set(), deque([home_key(p)])
        if home_key(p) not in built:
            problems.append(f"session {p}: no dashboard {home_key(p)}")
            continue
        while todo:
            k = todo.popleft()
            if k in seen:
                continue
            seen.add(k)
            s, m = built[k], built[k].meta
            if not allowed(p, k):
                problems.append(f"session {p}: reached {k}, which is not theirs to open")
            links = s.links
            if is_console(k) and m["viewer"] != p:
                chrome = chromes[p].get(m["label"])
                if chrome is None:
                    problems.append(f"session {p}: no sidebar for {m['label']} (screen {k})")
                    continue
                if not m["modal"]:   # under a dialog the (dimmed) sidebar is not clickable
                    links = [ln for ln in s.links if not under(ln)] + chrome.links
            for *_, t in links:
                if t == "!theme":
                    continue
                d = dest_of(t)
                d = resolve(d, p) if d in built else d
                if d not in built or not in_session(d) or not allowed(p, d):
                    continue   # the prototype hides it, or it signs out (public site, sign in)
                todo.append(d)
        reached |= seen
        # every menu entry they can see opens one of their screens
        if p in SESSIONS:
            entries = menu_for(p)
        else:
            entries = [lab for lab, _, _ in SUPPLIER_MENU[p]]
            for lab, _, tgt in SUPPLIER_MENU[p]:
                if tgt not in built or built[tgt].meta["owner"] != p or built[tgt].meta["label"] != lab:
                    problems.append(f"session {p}: menu entry {lab} opens {tgt}, which is not their {lab} screen")
        for lab in entries:
            if not any(built[k].meta["label"] == lab for k in seen):
                problems.append(f"session {p}: menu entry {lab} reaches no screen")
        print(f"session   {p:8} {len(seen):3} screens, {len(entries)} menu entries")
    # the public site, sign in and register: nobody signed in
    todo = deque(["w80"])
    while todo:
        k = todo.popleft()
        for *_, t in built[k].links:
            d = dest_of(t) if t != "!theme" else None
            if d in built and d not in reached:
                reached.add(d)
                if not in_session(d):
                    todo.append(d)

    # forms: the Auditor reads everything and fills in nothing
    for k, s in built.items():
        if s.meta["write"] and "Auditor" in s.meta["write"]:
            problems.append(f"{k}: a form the read-only Auditor could open")
    # dialogs and drawers: nothing under the backdrop is clickable
    for k, s in built.items():
        if s.meta["modal"]:
            stray = [t for x, y, w, h, t in s.links if x < shell.SB]
            if stray or not s.links:
                problems.append(f"{k}: {'hotspots under the backdrop ' + str(stray) if stray else 'a dialog with no way out'}")
    # the highlighted row is the one to click
    for k, s in built.items():
        for tgt in s.meta["hl"]:
            if tgt is None:
                problems.append(f"{k}: the highlighted row opens nothing (highlight a row that does)")
            elif tgt in built and built[tgt].meta["owner"] not in (None, s.meta["owner"]):
                problems.append(f"{k}: the highlighted row opens {tgt}, which is {built[tgt].meta['owner']}'s own: "
                                "others can't click it")

    # one front door
    def targets(k):
        return {dest_of(t) for *_, t in built[k].links if t != "!theme"}
    public = [k for k, s in built.items() if s.meta["area"] == "public"]
    for k in public:
        if "w00" not in targets(k):
            problems.append(f"{k}: public page with no Sign in")
    for k in ("w80", "w00", "w83"):
        if "w70" not in targets(k):
            problems.append(f"{k}: no way to Register as a supplier")
    if "w00" not in targets("w70"):
        problems.append("w70: Register has no way to Sign in")
    for p in SESSIONS + SUPPLIER_SESSIONS:
        if home_key(p) not in targets("w00"):
            problems.append(f"w00: Sign in cannot sign in {p} (to {home_key(p)})")
    if "w70d" not in targets("w70c"):
        problems.append("w70c: a new applicant cannot follow their application")
    print(f"door      {len(public)} public pages · sign in reaches {len(SESSIONS)} staff + {len(SUPPLIER_SESSIONS)} suppliers")
    for key, s in built.items():
        if key not in reached:
            problems.append(f"{key}: cannot be reached by clicking from the public Home")
        if not s.links:
            problems.append(f"{key}: dead end (no links out)")
    seen = reached

    links = sum(len(s.links) for s in built.values())
    print(f"{len(built)} screens · {links} hotspots · {len(seen)} reachable from w80")
    if problems:
        print(f"\n{len(problems)} problem(s):")
        for p in problems:
            print("  ✗", p)
        sys.exit(1)
    print("✓ all checks passed")


if __name__ == "__main__":
    main()
