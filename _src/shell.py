"""Frames and patterns every screen is built from.

console()  the staff console: sidebar (only the menu entries the viewer's role may open) and top bar
chrome()   just the sidebar and identity for one person, laid over shared screens by the prototype
portal()   the supplier portal: the same frame, the supplier's own menu (data.SUPPLIER_MENU)
public()   the public site: Home · About · FAQs · Notices, Sign in (nobody signed in)
auth()     sign in and forgot password: branding panel + form; register_frame() for registering
Patterns:  page_head, list toolbar + table + pager (the SDS list pattern), tabs, dialogs, drawers, key/value rows
"""
from __future__ import annotations

from data import PEOPLE, PERMS, SUPPLIER_ACCOUNTS, SUPPLIER_HOME, SUPPLIER_MENU, dashboard_key, menu_for, menu_target
from kit import (AMBER, AMBER_D, BG, BRAND, BRAND_D, BRAND_M, CARD, FAINT, FIELD_BG, INK, INK2, LIME, LIME_D, LINE, LINE2, MUTED, RED,
                 SVG, avatar, button, checkbox, chip, icon_button, kbd, logo, ref, status_chip, textarea, tint, tw, wordmark, wrap)

W, H = 1920, 1080
SB = 276            # sidebar width
TOP = 72            # top bar height
X0 = SB + 40        # content left
X1 = W - 40         # content right
CW = X1 - X0
Y0 = TOP + 30       # content top

# ---------------------------------------------------------------- navigation
# (section, [(label, icon, target) | (group label, icon, [(label, target)])]). Targets are the SHARED screens;
# Dashboard, My approvals and an appointed member's Evaluations are each person's own (data.menu_target).
NAV = [
    ("WORK", [
        ("Dashboard", "grid", None),
        ("My approvals", "inbox", None),
        ("Procurement", "package", [("Requisitions", "w10"), ("RFQs & quotations", "w12"), ("Evaluations", "w13"),
                                    ("Purchase orders", "w14"), ("Deliveries", "w15")]),
        ("Suppliers", "building", [("Supplier register", "w20"), ("Applications", "w21")]),
        ("Budgets", "wallet", [("Budgets", "w30"), ("Budget revisions", "w31")]),
        ("Reports", "bars", [("Procurement register", "w40"), ("Budget utilisation", "w41")]),
    ]),
    ("ADMINISTRATION", [
        ("Setup", "layers", [("Financial years", "w50"), ("Departments", "w51"), ("Offices & cost centres", "w52"),
                             ("Donors", "w53"), ("Projects", "w54"), ("Account codes", "w55"),
                             ("Procurement categories", "w56"), ("Supplier document types", "w57"),
                             ("Units of measure", "w58")]),
        ("Users", "users", "w60"),
        ("Roles & permissions", "shield", "w61"),
        ("Approval workflows", "workflow", "w62"),
        ("Audit trail", "history", "w63"),
    ]),
]
APPROVAL_BADGE = {"samuel": "4", "daniel": "1"}
# The signed-in person's name sits in a fixed block at the top right, so the viewer can redraw it per session
# without anything else in the top bar moving.
IDENT_W = 300
IDENT = (X1 - IDENT_W, 0, W - (X1 - IDENT_W), TOP - 1)   # x, y, w, h of the identity block


def writes(s: SVG, roles=None):
    """Mark a screen as a form that creates or changes a record: only these roles may open it (default: every role
    with the menu except the read-only Auditor)."""
    s.meta["write"] = list(roles) if roles else [r for r in PERMS if r != "Auditor"]
    return s


def nav_target(label, person, shared):
    return menu_target(label, person) or shared


def console(title: str, active: str, crumbs: list[str], viewer="ivan", owner=False):
    """The staff console frame, as `viewer` sees it. `active` is a menu label; its group opens.

    owner=True: this screen is the viewer's own (their dashboard, their decision). A shared screen is drawn as
    the System Admin sees it; the prototype redraws the sidebar and identity for whoever is signed in."""
    s = SVG(W, H, title)
    s.soft = True
    s.meta |= {"label": active, "viewer": viewer, "owner": viewer if owner else None, "area": "staff"}
    s.rect(0, 0, W, H, fill=BG, name="page background")
    draw_sidebar(s, viewer, active)
    _top_bar(s, crumbs)
    draw_identity(s, viewer)
    return s


def _top_bar(s: SVG, crumbs, search="Search files, suppliers, LPOs…", fy=True):
    with s.g("top bar"):
        s.rect(SB, 0, W - SB, TOP, fill=CARD, name="top bar bg")
        s.line(SB, TOP, W, TOP, LINE)
        s.icon("menu", X0 - 4, 24, 22, INK2, 2)
        x = X0 + 38
        s.icon("home", x, 27, 18, MUTED, 1.9)
        x += 30
        for i, c in enumerate(crumbs):
            last = i == len(crumbs) - 1
            s.icon("chevright", x - 6, 28, 16, FAINT)
            x += 16
            x += s.text(x, 41, c, 14, 600 if last else 500, INK if last else MUTED, name=f"crumb {c}") + 10
        rx = IDENT[0]
        s.line(rx - 4, 20, rx - 4, 52, LINE)
        rx -= 50
        with s.g("notifications"):
            s.icon("bell", rx, 25, 22, INK2, 1.9)
            s.circle(rx + 19, 26, 8, fill=RED)
            s.text(rx + 19, 30, "3", 10.5, 700, "#FFFFFF", anchor="middle")
        rx -= 48
        with s.g("theme switch"):
            s.icon("moon", rx, 25, 21, INK2, 1.9)
        s.link(rx - 9, 15, 40, 40, "!theme")
        rx -= 24
        dw = tw("Demo · illustrative data", 12, 700) + 30
        rx -= dw
        with s.g("demo pill"):
            s.rect(rx, 22, dw, 28, fill=LIME, rx=14)
            s.circle(rx + 13, 36, 4, fill=LIME_D)
            s.text(rx + 22, 40.5, "Demo · illustrative data", 12, 700, LIME_D)
        if not fy:
            return
        rx -= 16
        fw = tw("FY 2026", 13, 700) + 46
        rx -= fw
        with s.g("financial year"):
            s.rect(rx, 18, fw, 36, fill=CARD, rx=10, stroke="#D3DCD6", shadow=False)
            s.icon("calendar", rx + 11, 27, 17, BRAND, 2)
            s.text(rx + 34, 41, "FY 2026", 13, 700, INK)
        rx -= 14
        sw = 300
        rx -= sw
        with s.g("search"):
            s.rect(rx, 18, sw, 36, fill=FIELD_BG, rx=10, stroke=LINE, shadow=False)
            s.icon("search", rx + 12, 27, 18, MUTED)
            s.text(rx + 40, 41, search, 13, 400, FAINT)
            kx = rx + sw - 58
            kx += kbd(s, kx, 26, "Ctrl") + 4
            kbd(s, kx, 26, "K")


def chrome(viewer, active):
    """Just the sidebar and the identity block, as `viewer` sees them with `active` open. The prototype lays this
    over a shared screen, so the sidebar and the person never change while someone is signed in."""
    s = SVG(W, H, f"chrome {viewer} {active}")
    s.soft = True
    s.meta |= {"label": active, "viewer": viewer, "owner": None, "area": "staff"}
    draw_sidebar(s, viewer, active)
    draw_identity(s, viewer)
    return s


def draw_identity(s: SVG, viewer):
    name, ini, role, *_rest, col = PEOPLE[viewer]
    x, y, w, h = IDENT
    with s.g("signed in person"):
        s.rect(x, y, w, h, fill=CARD, name="identity bg")
        avatar(s, X1 - 20, 36, 20, ini, col, solid=True)
        s.text(X1 - 50, 31, name, 14, 700, INK, anchor="end", maxw=IDENT_W - 70)
        s.text(X1 - 50, 49, role, 12, 500, MUTED, anchor="end", maxw=IDENT_W - 70)
    s.link(X1 - 58 - max(tw(name, 14, 700), tw(role, 12, 500)), 12, max(tw(name, 14, 700), tw(role, 12, 500)) + 82, 48,
           "w00")


def draw_sidebar(s: SVG, viewer, active):
    allowed = set(menu_for(viewer))
    name, ini, role, *_rest, col = PEOPLE[viewer]
    with s.g("sidebar"):
        s.rect(0, 0, SB, H, fill=CARD, name="sidebar bg")
        s.line(SB, 0, SB, H, LINE)
        wordmark(s, 24, 22, 22, "Procurement")
        s.link(14, 14, 150, 52, dashboard_key(viewer))
        y = 104
        for section, items in NAV:
            visible = [it for it in items if (it[0] in allowed if not isinstance(it[2], list)
                                               else any(lab in allowed for lab, _ in it[2]))]
            if not visible:
                continue
            s.text(28, y, section, 10.5, 700, FAINT, spacing=1.2, name=f"nav section {section}")
            y += 14
            for label, icon, target in visible:
                if not isinstance(target, list):
                    _nav_item(s, y, label, icon, label == active, nav_target(label, viewer, target),
                              APPROVAL_BADGE.get(viewer) if label == "My approvals" else None)
                    y += 44
                else:
                    subs = [(lab, nav_target(lab, viewer, t)) for lab, t in target if lab in allowed]
                    open_ = any(lab == active for lab, _ in subs)
                    _nav_group(s, y, label, icon, open_, subs[0][1])
                    y += 44
                    if open_:
                        s.line(41, y - 2, 41, y + len(subs) * 38 - 8, LINE)
                        for lab, t in subs:
                            on = lab == active
                            with s.g(f"nav {lab}"):
                                if on:
                                    s.rect(52, y, SB - 68, 34, fill=tint(BRAND, 0.08), rx=9, shadow=False)
                                s.circle(41, y + 17, 3.5 if on else 2.5, fill=BRAND if on else "#B5C2BA")
                                s.text(66, y + 22, lab, 13.5, 600 if on else 500, BRAND if on else INK2)
                            s.link(52, y, SB - 68, 34, t)
                            y += 38
                        y += 4
            y += 10
        # who is signed in; clicking the card switches role (demo shortcut to the sign-in screen)
        with s.g("signed in user"):
            s.rect(0, H - 79, SB - 1, 79, fill=CARD)
            s.line(16, H - 78, SB - 16, H - 78, LINE)
            avatar(s, 44, H - 39, 19, ini, col, solid=True)
            s.text(72, H - 44, name, 14, 700, INK, maxw=SB - 130)
            s.text(72, H - 25, role, 12, 500, MUTED, maxw=SB - 130)
            s.rect(SB - 54, H - 58, 38, 38, fill=tint(RED, 0.1), rx=10, name="sign out", shadow=False)
            s.icon("logout", SB - 45, H - 49, 20, RED, 2)
        s.link(14, H - 66, SB - 82, 54, "w00")    # the name: sign in as someone else (demo)
        s.link(SB - 54, H - 58, 38, 38, "w80")    # sign out: back to the public site


def _nav_item(s: SVG, y, label, icon, on, target, badge=None):
    with s.g(f"nav {label}"):
        if on:
            s.rect(14, y, SB - 28, 38, fill=tint(BRAND, 0.09), rx=10, name="active bg", shadow=False)
            s.rect(14, y + 9, 3, 20, fill=BRAND, rx=1.5)
        s.icon(icon, 30, y + 10, 19, BRAND if on else "#7F8F86", 1.9)
        s.text(60, y + 24, label, 14, 700 if on else 500, BRAND if on else INK2, name="label")
        if badge:
            bw = tw(badge, 11, 700) + 14
            s.rect(SB - 30 - bw, y + 10, bw, 18, fill=AMBER, rx=9, name="badge")
            s.text(SB - 30 - bw / 2, y + 23, badge, 11, 700, "#3B2600", anchor="middle")
    s.link(14, y, SB - 28, 38, target)


def _nav_group(s: SVG, y, label, icon, open_, target):
    with s.g(f"nav group {label}"):
        s.icon(icon, 30, y + 10, 19, BRAND if open_ else "#7F8F86", 1.9)
        s.text(60, y + 24, label, 14, 700 if open_ else 500, INK if open_ else INK2, name="label")
        s.icon("chevup" if open_ else "chevdown", SB - 44, y + 11, 16, FAINT, 2)
    s.link(14, y, SB - 28, 38, target)


# ---------------------------------------------------------------- page patterns
def page_head(s: SVG, title, subtitle=None, y=Y0, actions=(), eyebrow=None, ref_line=None):
    """Title in the display face, a one-line subtitle, actions on the right: [(label, kind, icon, target)].
    ref_line: (code, text) instead of a subtitle: a reference number in the mono face, then plain text."""
    ty = y + 34
    if eyebrow:
        s.text(X0, y + 6, eyebrow, 11, 700, BRAND, spacing=1.0, name="eyebrow")
        ty += 14
    s.text(X0, ty, title, 30, 700, INK, family="display", name="page title")
    if ref_line:
        code, rest = ref_line
        cw = ref(s, X0, ty + 28, code, 13.5, BRAND, 600)
        s.text(X0 + cw + 8, ty + 28, rest, 14.5, 400, MUTED, name="page subtitle")
        subtitle = True
    elif subtitle:
        s.text(X0, ty + 28, subtitle, 14.5, 400, MUTED, name="page subtitle")
    x = X1
    for label, kind, icon, target in actions:
        w = button(s, x, y + 6, label, kind, icon=icon, anchor="end", h=42)
        s.link(x - w, y + 6, w, 42, target)
        x -= w + 12
    return ty + (44 if subtitle else 22)


def list_card(s: SVG, y, h, x=X0, w=CW, name="list"):
    s.rect(x, y, w, h, fill=CARD, rx=16, stroke=LINE, name=f"{name} card")


def toolbar(s: SVG, x, y, w, search="Search…", new=None, new_target=None, filters=(), export=True, extra=None):
    """The SDS list toolbar: search, filter, active filter chips · + New, export, columns. Returns its height."""
    with s.g("toolbar"):
        s.rect(x + 20, y + 18, 320, 42, fill=CARD, rx=10, stroke="#CFD9D2", shadow=False)
        s.icon("search", x + 34, y + 30, 18, MUTED)
        s.text(x + 60, y + 44, search, 14, 400, FAINT)
        icon_button(s, x + 352, y + 18, "filter", 42)
        cx = x + 408
        for lab in filters:
            cw = tw(lab, 12.5, 600) + 40
            s.rect(cx, y + 25, cw, 28, fill=tint(BRAND, 0.08), rx=14)
            s.text(cx + 12, y + 43.5, lab, 12.5, 600, BRAND_D)
            s.icon("x", cx + cw - 22, y + 32, 13, BRAND_D, 2.2)
            cx += cw + 8
        rx = x + w - 20
        icon_button(s, rx - 42, y + 18, "columns", 42)
        rx -= 54
        if export:
            icon_button(s, rx - 42, y + 18, "download", 42)
            rx -= 54
        if extra:
            label, icon, target = extra
            bw = button(s, rx, y + 18, label, "secondary", icon=icon, anchor="end", h=42)
            s.link(rx - bw, y + 18, bw, 42, target)
            rx -= bw + 12
        if new:
            bw = button(s, rx, y + 18, new, "primary", icon="plus", anchor="end", h=42)
            s.link(rx - bw, y + 18, bw, 42, new_target)
    return 78


def data_table(s: SVG, x, y, cols, rows, links=None, row_h=60, check=True, sort=(), hl=None, size=13.5,
               head_h=44, name="table"):
    """cols: [(label, width, align)]. A cell is a str or callable(s, x, y, w, h). links: per-row target or None.
    Returns the y below the last row."""
    tot = sum(c[1] for c in cols) + (52 if check else 0)
    with s.g(name):
        s.rect(x, y, tot, head_h, fill=FIELD_BG, name="header bg")
        s.line(x, y, x + tot, y, LINE2)
        s.line(x, y + head_h, x + tot, y + head_h, LINE2)
        cx = x
        if check:
            checkbox(s, x + 22, y + head_h / 2 - 9)
            cx += 52
        for label, w, align in cols:
            lw = tw(label.upper(), 11, 700) + 0.7 * len(label)
            tx = cx + w - 16 - lw if align == "end" else cx + 16
            s.text(tx, y + head_h / 2 + 4, label.upper(), 11, 700, MUTED, spacing=0.7)
            if label in sort:
                s.icon("swap", tx + lw + 6, y + head_h / 2 - 7, 13, FAINT, 2)
            cx += w
        ry = y + head_h
        for i, row in enumerate(rows):
            with s.g(f"row {i + 1}"):
                if hl is not None and i == hl:
                    s.rect(x, ry, tot, row_h, fill=tint(LIME, 0.45))
                    s.rect(x, ry, 3, row_h, fill=BRAND)
                cx = x
                if check:
                    checkbox(s, x + 22, ry + row_h / 2 - 9)
                    cx += 52
                for (label, w, align), cell in zip(cols, row):
                    if callable(cell):
                        cell(s, cx, ry, w, row_h)
                    elif cell is not None and cell != "":
                        if align == "end":
                            s.text(cx + w - 16, ry + row_h / 2 + 5, cell, size, 500, INK, anchor="end")
                        else:
                            s.text(cx + 16, ry + row_h / 2 + 5, cell, size, 400, INK, maxw=w - 26)
                    cx += w
                ry += row_h
                s.line(x, ry, x + tot, ry, LINE2)
            if links and i < len(links) and links[i]:
                s.link(x + (52 if check else 0), ry - row_h, tot - (52 if check else 0), row_h, links[i])
        if links and hl is not None:
            s.meta["hl"].append(links[hl] if hl < len(links) else None)
        return ry


def pager(s: SVG, x, y, w, shown, total, page=1, pages=5, per=10):
    """'Showing 1 to 10 of 146' with page buttons and a per-page picker."""
    with s.g("pager"):
        s.text(x + 20, y + 30, f"Showing {shown[0]} to {shown[1]} of {total:,}", 13, 500, MUTED)
        cx = x + w - 20 - 92
        s.rect(cx, y + 10, 92, 36, fill=CARD, rx=10, stroke="#CFD9D2", shadow=False)
        s.text(cx + 14, y + 33, f"{per} / page", 13, 600, INK)
        s.icon("chevdown", cx + 68, y + 20, 15, MUTED)
        cx -= 16
        items = ["‹"] + [str(p) for p in range(1, min(pages, 5) + 1)] + (["…", str(pages)] if pages > 5 else []) + ["›"]
        bx = cx - len(items) * 40
        for it in items:
            on = it == str(page)
            if on:
                s.rect(bx + 2, y + 10, 36, 36, fill=BRAND, rx=10)
            s.text(bx + 20, y + 33, it, 13.5, 700 if on else 500, "#FFFFFF" if on else INK2, anchor="middle")
            bx += 40


def tabs(s: SVG, x, y, items, active, targets=None, name="tabs"):
    """Underline tabs. items: [label] or [(label, count)]. targets: {label: key} (tab switches use !tab:)."""
    with s.g(name):
        cx = x
        for it in items:
            label, count = (it, None) if isinstance(it, str) else it
            on = label == active
            w = s.text(cx, y + 20, label, 14.5, 700 if on else 500, BRAND if on else INK2)
            tw_ = w
            if count is not None:
                cw = tw(str(count), 11, 700) + 14
                s.rect(cx + w + 8, y + 6, cw, 18, fill=tint(BRAND, 0.12) if on else LINE2, rx=9)
                s.text(cx + w + 8 + cw / 2, y + 19, str(count), 11, 700, BRAND if on else MUTED, anchor="middle")
                tw_ += 8 + cw
            if on:
                s.rect(cx, y + 36, tw_, 3, fill=BRAND, rx=1.5)
            if targets and targets.get(label):
                s.link(cx - 10, y - 4, tw_ + 20, 44, "!tab:" + targets[label])
            cx += tw_ + 34
        s.line(x, y + 39, x + max(cx - x, 400), y + 39, LINE)


def overlay(s: SVG, modal="dialog"):
    """Dim the page for a dialog or drawer. Nothing under the backdrop stays clickable: the page's hotspots go, and
    the viewer dims the signed-in person's sidebar with it (meta modal)."""
    s.rect(0, 0, W, H, fill="#0B1A12", op=0.38, name="overlay")
    s.layer += 1
    s.links.clear()
    s.meta["modal"] = modal


def dialog(s: SVG, w, h, title, subtitle=None, close_target=None, cx=None, cy=None):
    """A centred dialog over a dimmed page. Returns (x, y) of its content area."""
    overlay(s)
    x = (cx if cx is not None else (W + SB) / 2) - w / 2
    y = (cy if cy is not None else H / 2) - h / 2
    s.rect(x, y, w, h, fill=CARD, rx=20, stroke=LINE, shadow=True, name="dialog")
    s.text(x + 32, y + 46, title, 22, 700, INK, family="display")
    if subtitle:
        s.text(x + 32, y + 72, subtitle, 14, 400, MUTED)
    s.icon("x", x + w - 46, y + 28, 22, MUTED, 2)
    if close_target:
        s.link(x + w - 56, y + 18, 42, 42, close_target)
    return x + 32, y + (100 if subtitle else 76)


def drawer(s: SVG, w, title, subtitle=None, close_target=None):
    """A panel sliding in from the right over a dimmed page. Returns (x, y) of its content area."""
    overlay(s, "drawer")
    x = W - w
    s.rect(x, 0, w, H, fill=CARD, name="drawer")
    s.text(x + 32, 52, title, 22, 700, INK, family="display")
    if subtitle:
        s.text(x + 32, 78, subtitle, 14, 400, MUTED)
    s.icon("x", W - 52, 32, 22, MUTED, 2)
    if close_target:
        s.link(W - 62, 22, 42, 42, close_target)
    s.line(x, 104, W, 104, LINE)
    return x + 32, 130


# ---------------------------------------------------------------- approval on a record page
def timeline(s: SVG, x, y, w, steps, title="Approval timeline"):
    """Steps of a record: (what, who and when, 'done' | 'now' | 'next'). Returns the y below it."""
    s.text(x, y + 6, title.upper(), 10.5, 700, MUTED, spacing=0.8)
    y += 36
    for i, (what, who, st) in enumerate(steps):
        if i < len(steps) - 1:
            s.line(x + 12, y + 16, x + 12, y + 58, tint(BRAND_M, 0.4) if st == "done" else LINE, 2)
        if st == "done":
            s.circle(x + 12, y, 12, fill=BRAND_M)
            s.icon("check", x + 5, y - 7, 14, "#FFFFFF", 3)
        elif st == "now":
            s.circle(x + 12, y, 12, fill=LIME, stroke=LIME_D, sw=2)
            s.circle(x + 12, y, 4.5, fill=LIME_D)
        else:
            s.circle(x + 12, y, 10, fill=CARD, stroke="#C2CEC6", sw=2)
        s.text(x + 38, y + 5, what, 14.5, 700, INK if st != "next" else INK2, maxw=w - 40)
        s.para(x + 38, y + 25, who, w - 40, 12.5, 400, AMBER_D if st == "now" else MUTED, lh=18, max_lines=2)
        y += 70
    return y


def approval_panel(s: SVG, x, y, w, h, steps, waiting):
    """The right-hand panel of a record page for anyone whose turn it is not: the approval timeline and who it waits on.
    The approver at the current step gets decision_panel() in the same place, on their own copy of the page."""
    s.rect(x, y, w, h, fill=CARD, rx=16, stroke=LINE, name="approval panel")
    s.text(x + 24, y + 40, "Approval", 19, 700, INK, family="display")
    s.text(x + 24, y + 64, "Read only: it is not your turn", 13, 500, MUTED)
    timeline(s, x + 24, y + 92, w - 48, steps)
    wy = y + h - 104
    s.rect(x + 24, wy, w - 48, 80, fill=tint(AMBER, 0.12), rx=12)
    s.icon("clock", x + 40, wy + 18, 22, AMBER_D, 2)
    s.text(x + 74, wy + 32, "Waiting on " + waiting[0], 14.5, 700, INK, maxw=w - 110)
    s.para(x + 74, wy + 54, waiting[1], w - 110, 12.5, 400, MUTED, lh=18, max_lines=2)

def kv(s: SVG, x, y, w, label, value, vcolor=INK, mono=False, size=14):
    s.text(x, y, label, 13, 500, MUTED, name="label")
    if mono:
        s.text(x + w, y, value, size - 0.5, 500, vcolor, anchor="end", family="mono", name="value")
    else:
        s.text(x + w, y, value, size, 600, vcolor, anchor="end", name="value", maxw=w * 0.66)


def note(s: SVG, x, y, w, text, icon="info", color=BRAND, h=None, size=13):
    """A tinted note box with an icon; wraps the text. Returns its height."""
    lines = len(wrap(text, w - 56, size, 500))
    h = h or max(44, 20 + lines * 20)
    s.rect(x, y, w, h, fill=tint(color, 0.08), rx=12, name="note")
    s.icon(icon, x + 16, y + 13, 18, color, 2.1)
    s.para(x + 44, y + 27, text, w - 56, size, 500, INK2, lh=20)
    return h


# ---------------------------------------------------------------- supplier portal
# Suppliers sign in at the same door as staff and get their own dashboard: the same frame as the console, with the
# portal's menu (data.SUPPLIER_MENU). Every portal screen is the signed-in company's own (owner), so no click can
# show another company. Sections group the menu as Alpha's investor portal does.
PORTAL_SECTION = {"RFQs": "WORK", "Purchase orders": "WORK", "Payments": "WORK",
                  "Company profile": "MY COMPANY", "Documents": "MY COMPANY", "My application": "APPLICATION"}
PORTAL_BADGE = {("busoga", "RFQs"): "1"}
PX0, PX1 = 220, W - 220      # the registration pages (no sidebar) centre their content
PCW = PX1 - PX0


def portal(title, active, account="busoga", crumbs=None):
    """The supplier portal as `account` sees it: their sidebar, their company in the top bar."""
    s = SVG(W, H, title)
    s.soft = True
    s.meta |= {"label": active, "viewer": account, "owner": account, "area": "supplier"}
    s.rect(0, 0, W, H, fill=BG, name="page background")
    contact, ini, company, standing, col = SUPPLIER_ACCOUNTS[account]
    menu = SUPPLIER_MENU[account]
    with s.g("sidebar"):
        s.rect(0, 0, SB, H, fill=CARD, name="sidebar bg")
        s.line(SB, 0, SB, H, LINE)
        wordmark(s, 24, 22, 22, "Supplier portal")
        s.link(14, 14, 170, 52, SUPPLIER_HOME[account])
        y, section = 104, None
        for label, icon, target in menu:
            sec = PORTAL_SECTION.get(label)
            if sec != section and sec:
                y += 18 if y > 104 else 0
                s.text(28, y, sec, 10.5, 700, FAINT, spacing=1.2, name=f"nav section {sec}")
                y += 14
            section = sec
            _nav_item(s, y, label, icon, label == active, target, PORTAL_BADGE.get((account, label)))
            y += 44
        with s.g("signed in user"):
            s.rect(0, H - 79, SB - 1, 79, fill=CARD)
            s.line(16, H - 78, SB - 16, H - 78, LINE)
            avatar(s, 44, H - 39, 19, ini, col, solid=True)
            s.text(72, H - 44, contact, 14, 700, INK, maxw=SB - 130)
            s.text(72, H - 25, company, 12, 500, MUTED, maxw=SB - 130)
            s.rect(SB - 54, H - 58, 38, 38, fill=tint(RED, 0.1), rx=10, name="sign out", shadow=False)
            s.icon("logout", SB - 45, H - 49, 20, RED, 2)
        s.link(14, H - 66, SB - 82, 54, "w00")
        s.link(SB - 54, H - 58, 38, 38, "w80")
    _top_bar(s, crumbs or ["Supplier portal", active], search=None, fy=False)
    with s.g("signed in company"):
        x, y, w, h = IDENT
        s.rect(x, y, w, h, fill=CARD, name="identity bg")
        avatar(s, X1 - 20, 36, 20, ini, col, solid=True)
        s.text(X1 - 50, 31, company, 14, 700, INK, anchor="end", maxw=IDENT_W - 70)
        s.text(X1 - 50, 49, f"{contact} · {standing}", 12, 500, BRAND if account == "busoga" else AMBER_D,
               anchor="end", maxw=IDENT_W - 70)
    iw = max(tw(company, 14, 700), tw(f"{contact} · {standing}", 12, 500))
    s.link(X1 - 58 - iw, 12, iw + 82, 48, "w00")
    return s


# ---------------------------------------------------------------- public site
PUB_NAV = [("Home", "w80"), ("About", "w81"), ("FAQs", "w82"), ("Notices", "w83")]
QX0, QX1 = 160, W - 160      # public pages' content edges
QCW = QX1 - QX0
PUB_TOP = 88
FOOT = 72                    # footer height
DEEP = "#0F3D25"             # deep field green: stays dark in dark mode (not remapped)


def public(title, active):
    """A public page: no one is signed in. Header: Home · About · FAQs · Notices, the moon and Sign in."""
    s = SVG(W, H, title)
    s.soft = True
    s.meta |= {"label": active, "viewer": None, "owner": None, "area": "public"}
    s.rect(0, 0, W, H, fill=BG, name="page background")
    with s.g("public header"):
        s.rect(0, 0, W, PUB_TOP, fill=CARD, name="header bg")
        s.line(0, PUB_TOP, W, PUB_TOP, LINE)
        wordmark(s, QX0, 24, 24, "Procurement")
        s.link(QX0, 14, 200, 60, "w80")
        x = 760
        for label, target in PUB_NAV:
            on = label == active
            w = s.text(x, 52, label, 15.5, 700 if on else 500, BRAND if on else INK2)
            if on:
                s.rect(x, PUB_TOP - 3, w, 3, fill=BRAND, rx=1.5)
            else:
                s.link(x - 12, 22, w + 24, 48, target)
            x += w + 44
        bw = button(s, QX1, 22, "Sign in", "primary", icon="arrowright", anchor="end", h=44, target="w00")
        mx = QX1 - bw - 60
        s.circle(mx + 22, 44, 22, fill=CARD, stroke=LINE, name="theme switch")
        s.icon("moon", mx + 11, 33, 22, INK2, 1.9)
        s.link(mx, 22, 44, 44, "!theme")
        dw = tw("Demo · illustrative data", 12, 700) + 30
        dx = mx - 18 - dw
        s.rect(dx, 30, dw, 28, fill=LIME, rx=14)
        s.circle(dx + 13, 44, 4, fill=LIME_D)
        s.text(dx + 22, 48.5, "Demo · illustrative data", 12, 700, LIME_D)
    footer(s)
    return s


def footer(s: SVG):
    with s.g("footer"):
        s.rect(0, H - FOOT, W, FOOT, fill=DEEP, name="footer bg")
        s.text(QX0, H - FOOT + 43, "International Development Institute Uganda · Plot 45 Wilson Avenue, Jinja · idiu.org",
               13, 500, "#B9D3C2")
        x = QX1
        for label, target in reversed(PUB_NAV + [("Sign in", "w00")]):
            w = tw(label, 13, 600)
            s.text(x, H - FOOT + 43, label, 13, 600, "#FFFFFF", anchor="end")
            s.link(x - w - 8, H - FOOT + 22, w + 16, 32, target)
            x -= w + 32


# ---------------------------------------------------------------- sign in, forgot password (the one door)
AUTH_LW = 820                # the branding panel
AUTH_RX = AUTH_LW + 190      # the form column
AUTH_RW = 640


def auth(title):
    """Sign in and its neighbours: IDIU's branding on the left (Alpha's BrandingPanel, SDS's login), the form on the
    right. Nobody is signed in. Returns the SVG; the form goes in AUTH_RX .. AUTH_RX + AUTH_RW."""
    s = SVG(W, H, title)
    s.soft = True
    s.meta |= {"label": None, "viewer": None, "owner": None, "area": "auth"}
    s.rect(0, 0, W, H, fill=BG, name="page background")
    with s.g("branding panel"):
        s.rect(0, 0, AUTH_LW, H, fill=DEEP, name="panel bg")
        # contour lines: the land IDIU's projects sit on, quiet behind the words
        for i in range(9):
            yy = 980 - i * 96
            s.path(f"M-40 {yy} C 160 {yy - 30}, 300 {yy + 22}, 470 {yy - 8} S 700 {yy - 40}, 860 {yy - 12}",
                   stroke="#FFFFFF", sw=1, sop=0.05 + i * 0.006)
        s.rect(80, 64, 64, 50, fill="#FFFFFF", rx=12, name="logo tile")
        logo(s, 88, 70, 48)
        s.text(160, 92, "IDIU", 26, 700, "#FFFFFF", family="display")
        s.text(161, 113, "Procurement", 14, 600, LIME)
        s.link(70, 54, 220, 72, "w80")
        s.text(80, 330, "From budget to", 56, 700, "#FFFFFF", family="display")
        s.text(80, 394, "closed file.", 56, 700, LIME, family="display")
        s.para(82, 446, "Requisitions, quotations, evaluation, LPOs, delivery and payment: one record per purchase, "
               "approved by the right people, open to auditors.", 620, 18, 400, "#CFE3D6", lh=28)
        facts = [("shield", "Maker-checker", "whoever prepares never approves"),
                 ("lock", "Sealed quotations", "opened together at closing"),
                 ("history", "Full audit trail", "every change, old → new")]
        fy = 600
        for ic, a, b in facts:
            s.rect(80, fy, 48, 48, fill="#FFFFFF", op=0.08, rx=12)
            s.icon(ic, 92, fy + 12, 24, "#FFFFFF", 2)   # white: dark mode keeps it
            s.text(146, fy + 21, a, 16, 700, "#FFFFFF")
            s.text(146, fy + 41, b, 14, 400, "#B9D3C2")
            fy += 76
        s.text(80, H - 52, "International Development Institute Uganda · Plot 45 Wilson Avenue, Jinja", 13, 500,
               "#B9D3C2")
    s.text(AUTH_RX, 76, "←  Back to home", 14, 600, BRAND)
    s.link(AUTH_RX - 8, 54, 150, 34, "w80")
    with s.g("theme switch"):
        s.circle(W - 70, 70, 22, fill=CARD, shadow=True)
        s.icon("moon", W - 81, 59, 22, INK, 2)
    s.link(W - 94, 46, 48, 48, "!theme")
    return s


def register_frame(title):
    """Registering as a supplier: nobody is signed in yet. A light header with the way back and the way to sign in."""
    s = SVG(W, H, title)
    s.soft = True
    s.meta |= {"label": None, "viewer": None, "owner": None, "area": "auth"}
    s.rect(0, 0, W, H, fill=BG, name="page background")
    with s.g("register header"):
        s.rect(0, 0, W, 76, fill=CARD)
        s.line(0, 76, W, 76, LINE)
        wordmark(s, PX0, 20, 22, "Supplier registration")
        s.link(PX0, 10, 220, 56, "w80")
        w = tw("Already registered? ", 14, 500) + tw("Sign in", 14, 700)
        s.text(PX1 - w, 44, "Already registered? ", 14, 500, MUTED)
        s.text(PX1, 44, "Sign in", 14, 700, BRAND, anchor="end")
        s.link(PX1 - 76, 22, 84, 34, "w00")
        mx = PX1 - w - 64
        s.icon("moon", mx + 10, 27, 21, INK2, 1.9)
        s.link(mx, 18, 40, 40, "!theme")
        dw = tw("Demo · illustrative data", 12, 700) + 30
        dx = mx - 16 - dw
        s.rect(dx, 24, dw, 28, fill=LIME, rx=14)
        s.circle(dx + 13, 38, 4, fill=LIME_D)
        s.text(dx + 22, 42.5, "Demo · illustrative data", 12, 700, LIME_D)
    return s


# ---------------------------------------------------------------- table cells (callables for data_table)
def c_status(status, label=None):
    def f(s_, x, y, w, h):
        status_chip(s_, x + 14, y + h / 2 - 12, status, label=label)
    return f


def c_chip(label, color, solid=False, icon=None):
    def f(s_, x, y, w, h):
        chip(s_, x + 14, y + h / 2 - 12, label, color, solid=solid, icon=icon)
    return f


def c_ref(code, sub=None, color=INK):
    def f(s_, x, y, w, h):
        if sub:
            ref(s_, x + 16, y + h / 2 - 3, code, 13, color)
            s_.text(x + 16, y + h / 2 + 15, sub, 12, 400, MUTED, maxw=w - 26)
        else:
            ref(s_, x + 16, y + h / 2 + 5, code, 13, color)
    return f


def c_two(title, sub, bold=True, color=INK):
    def f(s_, x, y, w, h):
        s_.text(x + 16, y + h / 2 - 3, title, 14, 600 if bold else 500, color, maxw=w - 26)
        s_.text(x + 16, y + h / 2 + 15, sub, 12, 400, MUTED, maxw=w - 26)
    return f


def c_person(key, sub=None):
    def f(s_, x, y, w, h):
        name, ini, role, *_rest, col = PEOPLE[key]
        avatar(s_, x + 32, y + h / 2, 15, ini, col)
        if sub is False:
            s_.text(x + 56, y + h / 2 + 5, name, 13.5, 600, INK, maxw=w - 64)
        else:
            s_.text(x + 56, y + h / 2 - 3, name, 13.5, 600, INK, maxw=w - 64)
            s_.text(x + 56, y + h / 2 + 14, sub or role, 12, 400, MUTED, maxw=w - 64)
    return f


def c_money(n, sub=None, bold=True):
    def f(s_, x, y, w, h):
        v = f"{n:,.0f}" if n is not None else "—"
        if sub:
            s_.text(x + w - 16, y + h / 2 - 3, v, 14, 700 if bold else 500, INK, anchor="end")
            s_.text(x + w - 16, y + h / 2 + 15, sub, 12, 400, MUTED, anchor="end")
        else:
            s_.text(x + w - 16, y + h / 2 + 5, v, 14, 700 if bold else 500, INK, anchor="end")
    return f


def c_num(n, sub=None):
    def f(s_, x, y, w, h):
        s_.text(x + w - 16, y + h / 2 + (-3 if sub else 5), f"{n:,}" if isinstance(n, int) else n, 14, 600, INK,
                anchor="end")
        if sub:
            s_.text(x + w - 16, y + h / 2 + 15, sub, 12, 400, MUTED, anchor="end")
    return f


def c_actions(*icons, target=None):
    """Row action buttons (edit, view, deactivate…), drawn quietly at the start of the cell."""
    def f(s_, x, y, w, h):
        bx = x + 14
        for ic in icons:
            col = RED if ic == "ban" else (BRAND if ic in ("check", "refresh") else INK2)
            s_.rect(bx, y + h / 2 - 17, 34, 34, fill=CARD, rx=9, stroke=LINE, shadow=False)
            s_.icon(ic, bx + 8, y + h / 2 - 9, 18, col, 1.9)
            bx += 42
    return f


def c_text(text, color=INK, weight=400, mono=False):
    def f(s_, x, y, w, h):
        if mono:
            ref(s_, x + 16, y + h / 2 + 5, text, 13, color)
        else:
            s_.text(x + 16, y + h / 2 + 5, text, 13.5, weight, color, maxw=w - 26)
    return f


# ---------------------------------------------------------------- stat cards and record headers
def stat_card(s: SVG, x, y, w, h, icon, color, label, value, sub=None, sub_parts=None, help=True, frac=None,
              target=None, value_size=34):
    """SDS-style figure card: icon tile, label with a help mark, a big display-face number, a sub line.
    sub_parts: [(text, colour)] for a sub line with coloured inline counts."""
    with s.g(f"stat {label}"):
        s.rect(x, y, w, h, fill=CARD, rx=16, stroke=LINE, name="bg")
        lw = s.text(x + 24, y + 38, label, 14, 600, INK2, maxw=w - 100)
        if help:
            _help(s, x + 24 + lw + 8, y + 25)
        s.rect(x + w - 62, y + 18, 40, 40, fill=tint(color, 0.13), rx=11, name="icon tile")
        s.icon(icon, x + w - 52, y + 28, 20, color, 2)
        s.text(x + 24, y + 38 + value_size + 12, value, value_size, 700, INK, family="display", name="value")
        sy = y + 38 + value_size + 38
        if sub_parts:
            cx = x + 24
            for t, col in sub_parts:
                cx += s.text(cx, sy, t, 13, 600 if col != MUTED else 400, col)
        elif sub:
            s.text(x + 24, sy, sub, 13, 400, MUTED, maxw=w - 48)
        if frac is not None:
            s.rect(x + 24, y + h - 20, w - 48, 6, fill=LINE2, rx=3)
            s.rect(x + 24, y + h - 20, max((w - 48) * min(frac, 1), 6), 6, fill=color, rx=3)
    if target:
        s.link(x, y, w, h, target)


def _help(s: SVG, x, y, size=16):
    s.circle(x + size / 2, y + size / 2, size / 2 - 0.5, fill="none", stroke=FAINT, sw=1.3)
    s.text(x + size / 2, y + size / 2 + 4, "?", 10.5, 700, FAINT, anchor="middle")


def record_header(s: SVG, y, code, title, chips=(), facts=(), actions=(), x=X0, w=CW, h=None, track=None):
    """The header card of one record (a budget, a revision, a procurement file).
    chips: [(label, colour, kind)] kind 'status' or 'chip'. facts: [(label, value)]. actions: [(label, kind, icon, target)].
    track: callable(s, x, y, w) drawing a file track under the facts. Returns the y below the card."""
    h = h or (196 if track else 128)
    s.rect(x, y, w, h, fill=CARD, rx=16, stroke=LINE, name="record header")
    ref(s, x + 28, y + 36, code, 13.5, BRAND, 600)
    tx = x + 28
    s.text(tx, y + 72, title, 26, 700, INK, family="display", name="record title")
    cx = tx + tw(title, 26, 700, "display") + 16
    for label, col, kind in chips:
        if kind == "status":
            cx += status_chip(s, cx, y + 52, label) + 8
        else:
            cx += chip(s, cx, y + 52, label, col) + 8
    fx = tx
    for label, value in facts:
        lw = s.text(fx, y + 104, label + " ", 13, 500, MUTED)
        vw = s.text(fx + lw, y + 104, value, 13, 600, INK2)
        fx += lw + vw + 26
    bx = x + w - 28
    for label, kind, icon, target in actions:
        bw = button(s, bx, y + 26, label, kind, icon=icon, anchor="end", h=42)
        s.link(bx - bw, y + 26, bw, 42, target)
        bx -= bw + 12
    if track:
        s.line(x, y + 126, x + w, y + 126, LINE2)
        track(s, x + 60, y + 156, w - 120)
    return y + h


# ---------------------------------------------------------------- the approver's panel
def decision_panel(s, x, y, w, viewer, maker, what, comment, steps, back, approve="Approve", h=None,
                   placeholder=False):
    """The approver's panel: who prepared it (and so can't decide it), the comment, Approve / Return / Reject."""
    name = PEOPLE[maker][0]
    h = h or 600
    s.rect(x, y, w, h, fill=CARD, rx=16, stroke=LINE, name="decision panel")
    s.text(x + 24, y + 40, "Your decision", 19, 700, INK, family="display")
    s.text(x + 24, y + 64, f"{PEOPLE[viewer][0]} · {PEOPLE[viewer][2]}", 13, 500, MUTED)
    cy = y + 92
    s.rect(x + 24, cy, w - 48, 62, fill=tint(BRAND, 0.06), rx=12)
    s.icon("shield", x + 40, cy + 20, 20, BRAND, 2)
    s.para(x + 70, cy + 26, f"{name} prepared this {what}, so only someone else can approve or reject it.",
           w - 110, 12.5, 500, INK2, lh=18)
    cy += 84
    s.text(x + 24, cy, "APPROVAL PATH", 10.5, 700, MUTED, spacing=0.8)
    cy += 24
    for i, (stp, who, state) in enumerate(steps):
        # state: "done", "now", "next" or "skipped"
        on = state == "now"
        if state == "done":
            s.circle(x + 36, cy + 12, 11, fill=tint(BRAND_M, 0.15))
            s.icon("check", x + 29, cy + 5, 14, BRAND_M, 3)
        elif on:
            s.circle(x + 36, cy + 12, 11, fill=LIME)
            s.circle(x + 36, cy + 12, 4.5, fill=LIME_D)
        else:
            s.circle(x + 36, cy + 12, 10, fill=CARD, stroke=FAINT, sw=1.5, dash="3 3" if state == "skipped" else None)
        s.text(x + 58, cy + 9, stp, 13.5, 700, FAINT if state == "skipped" else INK)
        s.text(x + 58, cy + 27, who + (" · you" if on else ""), 12, 400, FAINT if state == "skipped" else MUTED,
               maxw=w - 90)
        cy += 46
    cy += 6
    textarea(s, x + 24, cy, w - 48, 92, "Comment", comment, placeholder=placeholder)
    s.text(x + 24, cy + 132, "Required when you return or reject.", 12, 400, MUTED)
    cy += 152
    button(s, x + 24, cy, approve, "primary", icon="check", w=w - 48, h=46, target=back)
    bw = (w - 48 - 12) / 2
    button(s, x + 24, cy + 58, "Return", "warn", icon="undo", w=bw, h=42, target=back)
    button(s, x + 24 + bw + 12, cy + 58, "Reject", "danger", icon="x", w=bw, h=42, target=back)
