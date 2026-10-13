"""Charts and the two signature devices: the file track and the budget bar."""
from __future__ import annotations

import math

from kit import (BRAND, BRAND_D, BRAND_M, CARD, FAINT, INK, INK2, LIME, LIME_D, LINE, LINE2, MINT, MUTED, STAGES,
                 SVG, tint, tw)

# Budget money, in the order it is used up (PLAN.md §5)
SPENT, COMMITTED, RESERVED = BRAND, MINT, "#B7DB8E"
BUDGET_PARTS = [("Spent", SPENT), ("Committed", COMMITTED), ("Reserved", RESERVED)]


# ---------------------------------------------------------------- the file track
def file_track(s: SVG, x, y, w, current, skipped=(), waiting=None, since=None, complete=False, name="file track"):
    """The procurement file's stages as one track: done (mint, ticked), current (lime pill), still to come.

    current: a stage name from STAGES. waiting / since: who holds it and for how long, drawn on the right.
    complete: the file is closed; every stage is done and the right side says when it closed."""
    ci = len(STAGES) if complete else STAGES.index(current)
    right = 0
    if waiting:
        right = max(tw("WAITING ON", 11.5, 700), tw(waiting, 14, 700), tw(since or "", 12, 500)) + 56
    tw_ = w - right
    n = len(STAGES)
    step = tw_ / (n - 1) if n > 1 else 0
    with s.g(name):
        s.line(x, y, x + tw_, y, LINE, 3, cap="round")
        if ci > 0:
            s.line(x, y, x + step * min(ci, n - 1), y, MINT, 3, cap="round")
        for i, st in enumerate(STAGES):
            cx = x + i * step
            if st in skipped:
                s.circle(cx, y, 6, fill=CARD, stroke=FAINT, sw=1.5, dash="2 2")
                s.text(cx, y + 26, st, 11.5, 500, FAINT, anchor="middle")
                s.text(cx, y + 41, "skipped", 10.5, 400, FAINT, anchor="middle")
            elif i < ci:
                s.circle(cx, y, 9, fill=MINT)
                s.icon("check", cx - 6, y - 6, 12, "#FFFFFF", 3.2)
                s.text(cx, y + 28, st, 12, 600, INK2, anchor="middle")
            elif i == ci:
                lw = tw(st, 12.5, 700) + 30
                s.rect(cx - lw / 2, y - 14, lw, 28, fill=LIME, rx=14)
                s.circle(cx - lw / 2 + 13, y, 4.5, fill=LIME_D)
                s.text(cx - lw / 2 + 22, y + 4.5, st, 12.5, 700, LIME_D)
            else:
                s.circle(cx, y, 6.5, fill=CARD, stroke="#C2CEC6", sw=2)
                s.text(cx, y + 26, st, 12, 500, MUTED, anchor="middle")
        if waiting:
            rx = x + w
            s.text(rx, y - 5, "CLOSED" if complete else ("WAITING ON" if since else "NEXT"), 10.5, 700,
                   BRAND_M if complete else MUTED, anchor="end", spacing=0.8)
            s.text(rx, y + 14, waiting, 14, 700, INK, anchor="end")
            if since:
                s.text(rx, y + 31, since, 12, 500, MUTED, anchor="end")


def mini_track(s: SVG, x, y, current, w=118, status=None, name="mini track"):
    """The file track in a table row: nine ticks, the current one a lime pill. Returns its width."""
    ci = STAGES.index(current)
    n = len(STAGES)
    gap = 3
    seg = (w - gap * (n - 1)) / n
    with s.g(name):
        for i in range(n):
            sx = x + i * (seg + gap)
            if i < ci:
                s.rect(sx, y, seg, 6, fill=MINT, rx=3)
            elif i == ci:
                col = {"Returned": "#DB6A1F", "Rejected": "#D1443C", "Draft": "#A3B2A9"}.get(status, "#8CC152")
                s.rect(sx, y - 1, seg, 8, fill=col, rx=4)
            else:
                s.rect(sx, y, seg, 6, fill=LINE2, rx=3)
    return w


# ---------------------------------------------------------------- the budget bar
def budget_bar(s: SVG, x, y, w, budget, spent, committed=0, reserved=0, request=0, h=10, name="budget bar"):
    """Spent · committed · reserved, the rest available. `request` (this requisition) is drawn hatched on top."""
    with s.g(name):
        s.rect(x, y, w, h, fill=LINE2, rx=h / 2)
        cx = x
        parts = [(spent, SPENT), (committed, COMMITTED), (reserved, RESERVED)]
        total = sum(v for v, _ in parts)
        if total:
            s.rect(x, y, max(w * min(total / budget, 1), h), h, fill=SPENT, rx=h / 2)   # rounded left end
        for v, col in parts:
            if v <= 0:
                continue
            pw = w * v / budget
            s.rect(cx, y, pw, h, fill=col, rx=0 if cx > x else h / 2)
            cx += pw
        if request:
            pw = min(w * request / budget, x + w - cx)
            s.rect(cx, y, pw, h, fill=tint("#F2A93B", 0.35), stroke="#C8811C", sw=1.2, dash="3 2")


def budget_legend(s: SVG, x, y, request=False, size=12):
    items = BUDGET_PARTS + [("Available", LINE2)] + ([("This request", "#F7C978")] if request else [])
    cx = x
    for lab, col in items:
        s.rect(cx, y - 9, 10, 10, fill=col, rx=3, stroke="#C2CEC6" if col == LINE2 else None)
        cx += 16 + s.text(cx + 16, y, lab, size, 500, INK2) + 18
    return cx - x


# ---------------------------------------------------------------- charts
def donut(s: SVG, cx, cy, r, thick, parts, gap=0.012, name="donut"):
    """parts: [(value, colour)]."""
    total = sum(v for v, _ in parts) or 1
    a = -math.pi / 2
    with s.g(name):
        for v, col in parts:
            sweep = 2 * math.pi * v / total
            a0, a1 = a + gap, a + sweep - gap
            if a1 > a0:
                s.path(_arc(cx, cy, r, r - thick, a0, a1), fill=col)
            a += sweep


def _arc(cx, cy, ro, ri, a0, a1):
    large = 1 if a1 - a0 > math.pi else 0
    p = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))
    x0, y0 = p(ro, a0)
    x1, y1 = p(ro, a1)
    x2, y2 = p(ri, a1)
    x3, y3 = p(ri, a0)
    return (f"M{x0:.1f} {y0:.1f} A{ro} {ro} 0 {large} 1 {x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f} "
            f"A{ri} {ri} 0 {large} 0 {x3:.1f} {y3:.1f} Z")


def ring(s: SVG, cx, cy, r, thick, frac, color=BRAND, bg=LINE2, name="ring"):
    with s.g(name):
        s.circle(cx, cy, r - thick / 2, fill="none", stroke=bg, sw=thick)
        if frac > 0:
            a0, a1 = -math.pi / 2, -math.pi / 2 + 2 * math.pi * min(frac, 0.9999)
            rr = r - thick / 2
            x0, y0 = cx + rr * math.cos(a0), cy + rr * math.sin(a0)
            x1, y1 = cx + rr * math.cos(a1), cy + rr * math.sin(a1)
            large = 1 if a1 - a0 > math.pi else 0
            s.path(f"M{x0:.1f} {y0:.1f} A{rr} {rr} 0 {large} 1 {x1:.1f} {y1:.1f}", stroke=color, sw=thick)


def column_chart(s: SVG, x, y, w, h, values, labels, color=BRAND_M, hl=None, fmt=lambda v: f"{v:.0f}",
                 y_max=None, y_step=None, unit="", name="column chart"):
    """Rounded columns with a light grid. hl: index of the column to highlight (drawn in the brand colour)."""
    y_max = y_max or max(values) * 1.15
    y_step = y_step or y_max / 4
    with s.g(name):
        v = 0
        while v <= y_max + 0.01:
            gy = y + h - h * v / y_max
            s.line(x + 36, gy, x + w, gy, LINE2, 1)
            s.text(x + 28, gy + 4, fmt(v) + unit, 11, 500, FAINT, anchor="end")
            v += y_step
        n = len(values)
        slot = (w - 44) / n
        bw = min(slot * 0.56, 38)
        for i, (val, lab) in enumerate(zip(values, labels)):
            bx = x + 44 + i * slot + (slot - bw) / 2
            bh = h * val / y_max
            col = BRAND if i == hl else (tint(color, 0.55) if hl is not None else color)
            s.rect(bx, y + h - bh, bw, bh, fill=col, rx=6)
            if i == hl:
                s.text(bx + bw / 2, y + h - bh - 8, fmt(val) + unit, 11.5, 700, BRAND_D, anchor="middle")
            s.text(bx + bw / 2, y + h + 18, lab, 11.5, 500, MUTED, anchor="middle")


def hbars(s: SVG, x, y, w, rows, row_h=34, label_w=190, fmt=lambda v: f"{v:,.1f}M", name="bars"):
    """rows: [(label, value, colour)]; the longest bar spans the width."""
    vmax = max(v for _, v, _ in rows) or 1
    with s.g(name):
        for i, (lab, v, col) in enumerate(rows):
            ry = y + i * row_h
            s.text(x, ry + 16, lab, 13, 500, INK2, maxw=label_w - 12)
            bw = (w - label_w - 70) * v / vmax
            s.rect(x + label_w, ry + 5, w - label_w - 70, 14, fill=LINE2, rx=7)
            s.rect(x + label_w, ry + 5, max(bw, 14), 14, fill=col, rx=7)
            s.text(x + w, ry + 16, fmt(v), 13, 700, INK, anchor="end")


def sparkline(s: SVG, x, y, w, h, vals, color=BRAND_M, area=True, name="sparkline"):
    vmax, vmin = max(vals), min(vals)
    rng = (vmax - vmin) or 1
    pts = [(x + i * w / (len(vals) - 1), y + h - (v - vmin) / rng * h) for i, v in enumerate(vals)]
    with s.g(name):
        if area:
            d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts) + f" L{x + w:.1f} {y + h:.1f} L{x:.1f} {y + h:.1f} Z"
            s.path(d, fill=tint(color, 0.18))
        s.poly(pts, stroke=color, sw=2, closed=False)
        s.circle(*pts[-1], 3.5, fill=color)


def legend_dot(s: SVG, x, y, label, color, size=12):
    s.circle(x + 5, y - 4, 5, fill=color)
    return 14 + s.text(x + 14, y, label, size, 500, INK2)

