"""Budgets (w30–w31b) and reports (w40–w41).

Budgets are maker-checker records: Finance prepares (line by line, or from Excel), the Country Director
approves, and an active budget changes only through a revision. Every figure is computed from data.py.
"""
from __future__ import annotations

from charts import budget_bar, budget_legend, column_chart, donut, legend_dot, mini_track
from data import (ACCOUNT, BUDGETS, FILES, FY_SPEND_BY_MONTH, KASESE_2027_IMPORT, KASESE_LINES, KASESE_TOTAL,
                  KUMI_2027_LINES, KUMI_2027_NEW, PROJECT, REVISION, REVISIONS, line_available)
from kit import (AMBER_D, BRAND, BRAND_D, BRAND_M, CARD, FAINT, FIELD_BG, INK, INK2, KOICA, LIME, LIME_D, LINE,
                 LINE2, MINT, MUTED, RED, TEAL, avatar, button, chip, field, ref, status_chip, textarea, tint, tw)
from shell import (approval_panel, tabs, timeline, writes, decision_panel, CW, X0, X1, Y0, c_chip, c_money, c_person, c_ref, c_status, c_text, c_two, console,
                   data_table, list_card, note, page_head, pager, record_header, stat_card, toolbar)

DONOR_COLOUR = {"KOICA": KOICA, "KFHI": BRAND_M, "IDIU": AMBER_D}


def _m(n):
    return f"{n:,.0f}"


def _use_cell(budget, spent, committed, reserved):
    def f(s_, x, y, w, h):
        used = spent + committed + reserved
        budget_bar(s_, x + 16, y + h / 2 - 9, w - 90, budget, spent, committed, reserved, h=9)
        s_.text(x + w - 16, y + h / 2 - 1, f"{used / budget:.0%}", 13.5, 700, INK, anchor="end")
        s_.text(x + 16, y + h / 2 + 18, f"{_m(used)} used", 11.5, 500, MUTED)
    return f


# =====================================================================================
def w30_budgets(title="30 Budgets"):
    s = console(title, "Budgets", ["Budgets"], "ivan")
    y = page_head(s, "Budgets", "Project budgets for FY 2026, line by line. Requisitions draw only on active budgets.",
                  actions=[("New budget", "primary", "plus", "w30e"), ("Import from Excel", "secondary", "upload", "w30e")])
    tot = sum(b[3] for b in BUDGETS)
    spent = sum(b[4] for b in BUDGETS)
    comm = sum(b[5] for b in BUDGETS)
    res = sum(b[6] for b in BUDGETS)
    avail = tot - spent - comm - res
    gw = (CW - 3 * 20) / 4
    stat_card(s, X0, y, gw, 140, "wallet", BRAND, "Approved budget FY 2026", f"UGX {tot / 1e6:,.1f}M",
              sub="6 projects · 3 donors")
    stat_card(s, X0 + gw + 20, y, gw, 140, "receipt", BRAND_D, "Spent", f"UGX {spent / 1e6:,.1f}M",
              sub_parts=[(f"{spent / tot:.0%}", BRAND_D), (" of the budget · payment references recorded", MUTED)])
    stat_card(s, X0 + 2 * (gw + 20), y, gw, 140, "stamp", TEAL, "Committed & reserved", f"UGX {(comm + res) / 1e6:,.1f}M",
              sub_parts=[(f"{comm / 1e6:,.1f}M", TEAL), (" on issued LPOs · ", MUTED), (f"{res / 1e6:,.1f}M", INK2),
                         (" on approved requisitions", MUTED)])
    stat_card(s, X0 + 3 * (gw + 20), y, gw, 140, "coins", BRAND_M, "Available", f"UGX {avail / 1e6:,.1f}M",
              sub=f"{avail / tot:.0%} left with 12 weeks of FY 2026 to go")
    y += 160
    rows, links = [], []
    for code, proj, donor, total, sp, cm, rs, st, lines, appr in BUDGETS:
        p = PROJECT[proj]
        rows.append([c_ref(code, p[1]), c_chip(donor, DONOR_COLOUR[donor]), c_text(str(lines)),
                     c_money(total), _use_cell(total, sp, cm, rs), c_money(total - sp - cm - rs, bold=False),
                     c_status(st), c_two(appr.split(" · ")[0], "by " + appr.split(" · ")[1], bold=False)])
        links.append("w30b" if code == "BUD-2026-001" else None)
    cols = [("Budget", 380, "start"), ("Donor", 130, "start"), ("Lines", 90, "start"), ("Budget (UGX)", 170, "end"),
            ("Use", 290, "start"), ("Available (UGX)", 170, "end"), ("Status", 130, "start"), ("Approved", 152, "start")]
    row_h = 62
    list_card(s, y, 78 + 44 + row_h * len(rows) + 58)
    toolbar(s, X0, y, CW, "Search budgets…", filters=["FY 2026"])
    end = data_table(s, X0, y + 78, cols, rows, links=links, row_h=row_h, sort={"Budget"})
    pager(s, X0, end, CW, (1, len(rows)), len(rows), pages=1)
    budget_legend(s, X0 + 620, end + 33)
    # FY 2027, in preparation
    y = end + 78
    s.text(X0, y + 14, "FY 2027 in preparation", 16, 700, INK)
    s.text(X0 + 196, y + 14, "Drafts are Finance's working copies: they count for nothing until approved.", 13, 400, MUTED)
    tiles = [("BUD-2027-002", "Model Home Health, Kumi", "Entered line by line · 4 of 5 lines", "w30c", "pencil"),
             ("BUD-2027-001", "Kasese ICT Hub", "Imported from Excel · 3 rows to fix", "w30d", "sheet")]
    tw_ = (CW - 20) / 2
    for i, (code, name, sub, tgt, ic) in enumerate(tiles):
        tx = X0 + i * (tw_ + 20)
        s.rect(tx, y + 30, tw_, 74, fill=CARD, rx=14, stroke=LINE)
        s.rect(tx + 18, y + 47, 40, 40, fill=tint(BRAND, 0.1), rx=11)
        s.icon("sheet" if ic == "sheet" else "edit", tx + 28, y + 57, 20, BRAND, 2)
        ref(s, tx + 72, y + 62, code, 12.5, BRAND)
        s.text(tx + 72 + tw(code, 12.5, 500, "mono") + 10, y + 62, name, 14, 700, INK)
        s.text(tx + 72, y + 83, sub, 13, 400, MUTED)
        status_chip(s, tx + tw_ - 112, y + 55, "Draft")
        s.icon("chevright", tx + tw_ - 36, y + 57, 20, FAINT)
        s.link(tx, y + 30, tw_, 74, tgt)
    return s


def w30b_budget():
    s = console("30b Budget: Kasese ICT Hub FY 2026", "Budgets", ["Budgets", "Kasese ICT Hub · FY 2026"], "ivan")
    y = record_header(s, Y0, "BUD-2026-001", "Kasese ICT Hub · FY 2026",
                      chips=[("Active", None, "status"), ("KOICA", KOICA, "chip")],
                      facts=[("Department", "Programmes"), ("Cost centre", "KSE · Kasese field office"),
                             ("Approved", "9 Jan 2026 by Samuel Kato"), ("Last revision", "BR-2026-0005 · 2 Sep · +UGX 20M on 5210")],
                      actions=[("Request revision", "primary", "swap", "w31c"), ("Export", "secondary", "download", None)])
    y += 20
    spent = sum(l[4] for l in KASESE_LINES)
    comm = sum(l[5] for l in KASESE_LINES)
    res = sum(l[6] for l in KASESE_LINES)
    avail = KASESE_TOTAL - spent - comm - res
    # the budget in one bar
    s.rect(X0, y, CW, 150, fill=CARD, rx=16, stroke=LINE, name="summary")
    figs = [("Budget", KASESE_TOTAL, INK), ("Spent", spent, BRAND), ("Committed", comm, MINT), ("Reserved", res, "#8CC152"),
            ("Available", avail, BRAND_D)]
    fx = X0 + 28
    for lab, v, col in figs:
        s.text(fx, y + 34, lab, 13, 600, MUTED)
        s.text(fx, y + 64, f"UGX {_m(v)}", 21, 700, col if lab != "Budget" else INK, family="display")
        fx += 270
    budget_bar(s, X0 + 28, y + 88, CW - 56, KASESE_TOTAL, spent, comm, res, h=12)
    budget_legend(s, X0 + 28, y + 128)
    y += 170
    # lines, and what is drawing on the selected one
    lw = 1080
    rows = []
    for acc, desc, cc, b, sp, cm, rs in KASESE_LINES:
        rows.append([c_ref(acc, ACCOUNT[acc][1]), c_text(desc, INK2), c_money(b), c_money(sp, bold=False),
                     c_money(cm, bold=False), c_money(line_available((acc, desc, cc, b, sp, cm, rs))),
                     _use_cell(b, sp, cm, rs)])
    cols = [("Account", 200, "start"), ("Line", 225, "start"), ("Budget", 125, "end"), ("Spent", 115, "end"),
            ("Committed", 120, "end"), ("Available", 125, "end"), ("Use", 170, "start")]
    list_card(s, y, 60 + 44 + 64 * len(rows) + 16, w=lw)
    s.text(X0 + 24, y + 38, "Budget lines", 17, 700, INK)
    s.text(X0 + 150, y + 38, "6 lines · all in UGX", 13, 400, MUTED)
    data_table(s, X0, y + 60, cols, rows, row_h=64, check=False, hl=0, size=13)
    # the right panel: commitments on 5210
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 504, fill=CARD, rx=16, stroke=LINE, name="line panel")
    ref(s, rx + 24, y + 36, "5210", 13, BRAND)
    s.text(rx + 70, y + 36, "ICT equipment: what draws on it", 16, 700, INK)
    s.text(rx + 24, y + 58, "Available now: UGX 60,200,000", 13, 600, BRAND_M)
    items = [("PR-2026-0087", "10 laptops for training room 2", "LPO-2026-0051 · committed", 36_400_000, "Delivered", "w11"),
             ("PR-2026-0098", "Projector and screen", "Draft · reserves nothing until approved", 4_200_000, "Draft", "w10b"),
             ("4 closed files", "Desktops and network, training room 1", "Paid Feb–Jul", 63_400_000, "Paid", None)]
    iy = y + 82
    for code, title, sub, v, st, tgt in items:
        s.line(rx + 24, iy, rx + rw - 24, iy, LINE2)
        if code.startswith("PR"):
            ref(s, rx + 24, iy + 28, code, 12.5, BRAND if tgt else INK2)
        else:
            s.text(rx + 24, iy + 28, code, 12.5, 700, INK2)
        s.text(rx + rw - 24, iy + 28, _m(v), 14, 700, INK, anchor="end")
        s.text(rx + 24, iy + 50, title, 13.5, 600, INK, maxw=rw - 160)
        s.text(rx + 24, iy + 70, sub, 12, 400, MUTED, maxw=rw - 160)
        status_chip(s, rx + rw - 24, iy + 44, st, anchor="end")
        if tgt:
            s.link(rx + 12, iy + 6, rw - 24, 78, tgt)
        iy += 88
    note(s, rx + 24, y + 504 - 88, rw - 48, "An active budget changes only through a revision the Country Director approves.",
         icon="lock")
    return s


def w30c_draft_budget():
    s = console("30c Budget: Model Home Health FY 2027 (draft, line by line)", "Budgets",
                ["Budgets", "FY 2027", "Model Home Health, Kumi"], "ruth", owner=True)
    y = record_header(s, Y0, "BUD-2027-002", "Model Home Health, Kumi · FY 2027",
                      chips=[("Draft", None, "status"), ("KFHI", BRAND_M, "chip")],
                      facts=[("Department", "Programmes"), ("Cost centre", "KUM · Kumi field office"),
                             ("Prepared by", "Ruth Nakato (you)"), ("Approves", "Samuel Kato · Country Director")],
                      actions=[("Submit for approval", "primary", "send", "w30"), ("Save draft", "secondary", None, "w30"),
                               ("Import from Excel", "secondary", "upload", "w30d")])
    y += 20
    lw = 1120
    lines = KUMI_2027_LINES
    rows = [[c_ref(a, ACCOUNT[a][1]), c_text(d, INK2), c_text(cc, INK2, mono=True), c_money(v),
             _row_actions()] for a, d, cc, v in lines]
    cols = [("Account", 250, "start"), ("Line description", 380, "start"), ("Cost centre", 150, "start"),
            ("Amount (UGX)", 190, "end"), ("", 150, "start")]
    total = sum(l[3] for l in lines) + KUMI_2027_NEW[3]
    h = 60 + 44 + 62 * len(rows) + 74 + 110
    list_card(s, y, h, w=lw)
    s.text(X0 + 24, y + 38, "Budget lines", 17, 700, INK)
    s.text(X0 + 150, y + 38, "Add each line, or import the whole budget from Excel", 13, 400, MUTED)
    end = data_table(s, X0, y + 60, cols, rows, row_h=62, check=False, size=13)
    # the line being added, in place
    ny = end
    s.rect(X0, ny, lw, 74, fill=tint(LIME, 0.35), name="new line row")
    s.rect(X0, ny, 3, 74, fill=BRAND)
    field(s, X0 + 14, ny - 12, 222, "", "5510 · Vehicles & motorcycles", h=40, dropdown=True, size=13)
    field(s, X0 + 250, ny - 12, 366, "", "Motorcycle fuel and maintenance", h=40, size=13)
    field(s, X0 + 630, ny - 12, 136, "", "KUM", h=40, dropdown=True, mono=True, size=13)
    field(s, X0 + 780, ny - 12, 176, "", "17,600,000", h=40, size=13, focus=True)
    button(s, X0 + 974, ny + 17, None, "primary", icon="check", w=40, h=40)
    button(s, X0 + 1022, ny + 17, None, "secondary", icon="x", w=40, h=40)
    ny += 74
    s.line(X0, ny, X0 + lw, ny, LINE2)
    button(s, X0 + 20, ny + 20, "Add line", "soft", icon="plus", h=40)
    s.text(X0 + 780 + 176 - 2, ny + 46, f"Total  UGX {_m(total)}", 17, 700, INK, anchor="end", family="display")
    s.text(X0 + 780 + 176 - 2, ny + 70, "Matches the KFHI grant agreement for 2027", 12.5, 600, BRAND_M, anchor="end")
    # before you submit
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 330, fill=CARD, rx=16, stroke=LINE, name="checks")
    s.text(rx + 24, y + 38, "Before you submit", 17, 700, INK)
    checks = [("Every line has an account code", True), ("Every cost centre exists in Setup", True),
              ("Total matches the grant (UGX 81,000,000)", True), ("FY 2027 is open for budgets (Planning)", True)]
    cy = y + 74
    for lab, ok in checks:
        s.circle(rx + 36, cy - 5, 11, fill=tint(BRAND_M, 0.15))
        s.icon("check", rx + 29, cy - 12, 14, BRAND_M, 3)
        s.text(rx + 58, cy, lab, 13.5, 500, INK2, maxw=rw - 80)
        cy += 40
    s.line(rx + 24, cy - 6, rx + rw - 24, cy - 6, LINE2)
    s.text(rx + 24, cy + 22, "APPROVAL PATH", 10.5, 700, MUTED, spacing=0.8)
    avatar(s, rx + 42, cy + 56, 17, "SK", AMBER_D)
    s.text(rx + 68, cy + 51, "Budget approval", 14, 700, INK)
    s.text(rx + 68, cy + 70, "Samuel Kato · Country Director", 12.5, 400, MUTED)
    note(s, rx, y + 350, rw, "You prepared this budget, so you can't approve it. Until Samuel approves it, no "
         "requisition can draw on it.", icon="shield")
    return s


def _row_actions():
    def f(s_, x, y, w, h):
        for i, ic in enumerate(("edit", "trash")):
            bx = x + 14 + i * 42
            s_.rect(bx, y + h / 2 - 17, 34, 34, fill=CARD, rx=9, stroke=LINE, shadow=False)
            s_.icon(ic, bx + 8, y + h / 2 - 9, 18, RED if ic == "trash" else INK2, 1.9)
    return f


def w30d_import():
    s = console("30d Budget import from Excel: Kasese ICT Hub FY 2027", "Budgets",
                ["Budgets", "FY 2027", "Import from Excel"], "ruth", owner=True)
    y = page_head(s, "Import a budget from Excel", "Kasese ICT Hub · FY 2027 · rows are checked against Setup before anything is saved")
    # steps
    steps = ["Download the template", "Upload the file", "Check the rows", "Save as a draft"]
    sw = CW / 4
    for i, lab in enumerate(steps):
        sx = X0 + i * sw
        done, cur = i < 2, i == 2
        s.rect(sx, y, sw - 12, 6, fill=BRAND_M if done else (LIME_D if cur else LINE), rx=3)
        s.text(sx, y + 30, f"{i + 1}", 13, 700, BRAND_M if done else (LIME_D if cur else FAINT), family="display")
        s.text(sx + 18, y + 30, lab, 14, 700 if cur else 500, INK if (done or cur) else MUTED)
        if done:
            s.icon("check", sx + 24 + tw(lab, 14, 500), y + 17, 15, BRAND_M, 2.6)
    y += 56
    ok = [r for r in KASESE_2027_IMPORT if not r[5]]
    bad = [r for r in KASESE_2027_IMPORT if r[5]]
    # file + summary
    s.rect(X0, y, CW, 96, fill=CARD, rx=16, stroke=LINE, name="file")
    s.rect(X0 + 24, y + 22, 52, 52, fill=tint(BRAND_M, 0.14), rx=12)
    s.icon("sheet", X0 + 38, y + 36, 24, BRAND_M, 2)
    s.text(X0 + 92, y + 44, "KSE-ICT_FY2027_budget.xlsx", 15, 700, INK)
    s.text(X0 + 92, y + 66, "Uploaded today 09:24 by Ruth Nakato · sheet “Budget” · 9 rows", 13, 400, MUTED)
    tiles = [("Rows read", "9", INK), ("Ready", str(len(ok)), BRAND_M), ("Need fixing", str(len(bad)), RED),
             ("Total of ready rows", f"UGX {_m(sum(r[4] for r in ok))}", INK)]
    tx = X0 + 720
    for lab, val, col in tiles:
        s.text(tx, y + 38, lab, 12.5, 600, MUTED)
        s.text(tx, y + 68, val, 22, 700, col, family="display")
        tx += 200 if lab != "Need fixing" else 190
    y += 116
    rows = []
    for r, acc, desc, cc, amt, problem in KASESE_2027_IMPORT:
        rows.append([c_text(str(r), MUTED), c_text(acc, RED if problem and "Account" in problem else INK, mono=True),
                     c_text(desc, INK2), c_text(cc, RED if problem and "Cost centre" in problem else INK2, mono=True),
                     c_money(amt, bold=False), _check_cell(problem)])
    cols = [("Row", 80, "start"), ("Account", 140, "start"), ("Description", 420, "start"), ("Cost centre", 150, "start"),
            ("Amount (UGX)", 180, "end"), ("Check", 594, "start")]
    list_card(s, y, 44 + 52 * len(rows) + 4)
    end = data_table(s, X0, y, cols, rows, row_h=52, check=False, size=13)
    for i, (*_, problem) in enumerate(KASESE_2027_IMPORT):
        if problem:
            s.rect(X0 + 1, y + 44 + i * 52, 3, 52, fill=RED)
    y = end + 22
    note(s, X0, y, 900, "Nothing is saved yet. Fix the three rows in Excel and upload again, or save the six ready rows "
         "as a draft and add the rest line by line. A draft counts for nothing until the Country Director approves it.",
         icon="info")
    button(s, X1, y + 4, "Save 6 ready lines as a draft", "primary", icon="check", anchor="end", target="w30")
    bw = tw("Save 6 ready lines as a draft", 14, 600) + 50
    button(s, X1 - bw - 12, y + 4, "Upload again", "secondary", icon="upload", anchor="end")
    return s


def _check_cell(problem):
    def f(s_, x, y, w, h):
        if problem:
            s_.icon("alert", x + 16, y + h / 2 - 8, 16, RED, 2)
            s_.text(x + 40, y + h / 2 + 5, problem, 13, 600, RED, maxw=w - 50)
        else:
            s_.icon("check", x + 16, y + h / 2 - 8, 16, BRAND_M, 2.6)
            s_.text(x + 40, y + h / 2 + 5, "Ready", 13, 600, BRAND_M)
    return f


def w31_revisions(title="31 Budget revisions", viewer="ivan", owner=False):
    s = console(title, "Budget revisions", ["Budgets", "Budget revisions"], viewer, owner=owner)
    y = page_head(s, "Budget revisions", "Changes to active budgets. The live budget keeps running until the Country "
                  "Director approves the change.", actions=[("New revision", "primary", "plus", "w31c")])
    rows, links = [], []
    for no, proj, change, amt, by, on, st in REVISIONS:
        waiting = {"Pending approval": "Samuel Kato · 3 days", "Approved": "Samuel Kato", "Returned": "Ruth Nakato"}[st]
        rows.append([c_ref(no, proj), c_text(change, INK, 600), c_money(amt), c_person(by, "Finance Officer"),
                     c_text(on, INK2), c_status(st), c_text(waiting, INK2)])
        links.append("w31d" if no == REVISION["no"] else None)
    cols = [("Revision", 330, "start"), ("Change", 380, "start"), ("Amount (UGX)", 160, "end"), ("Raised by", 230, "start"),
            ("Raised", 110, "start"), ("Status", 170, "start"), ("Decided / waiting on", 132, "start")]
    list_card(s, y, 78 + 44 + 64 * len(rows) + 58)
    toolbar(s, X0, y, CW, "Search revisions…", filters=["FY 2026"])
    end = data_table(s, X0, y + 78, cols, rows, links=links, row_h=64, hl=0)
    pager(s, X0, end, CW, (1, len(rows)), len(rows), pages=1)
    return s


def _revision_page(title, active, crumbs, viewer="ivan", decide=False, back="w02"):
    """BR-2026-0007 as a full record page. The Country Director decides on his own copy, from My approvals or from
    Budgets › Budget revisions; everyone else sees it read only, with who it waits on."""
    s = console(title, active, crumbs, viewer, owner=decide)
    y = record_header(s, Y0, REVISION["no"], "Move UGX 9M: venues → furniture",
                      chips=[("Pending approval", None, "status")],
                      facts=[("Budget", "BUD-2026-002 · Teacher ICT Initiative, Kamuli"), ("Raised by", "Ruth Nakato · Fri 9 Oct, 16:12"),
                             ("Step", "1 of 1 · Revision approval")])
    y += 20
    lw = 1090
    s.rect(X0, y, lw, 330, fill=CARD, rx=16, stroke=LINE, name="change card")
    s.text(X0 + 24, y + 38, "Proposed change", 17, 700, INK)
    s.text(X0 + 190, y + 38, "Two lines move; the budget total stays UGX 184,500,000", 13, 400, MUTED)
    rows = []
    for acc, desc, old, new, used in REVISION["lines"]:
        rows.append([c_ref(acc, desc), c_money(old, bold=False), _arrow_cell(new), _change_cell(new - old),
                     c_money(used, bold=False), c_money(new - used)])
    rows.append([c_text("Budget total", INK, 700), c_money(184_500_000, bold=False), _arrow_cell(184_500_000),
                 _change_cell(0), c_text(""), c_text("")])
    cols = [("Line", 300, "start"), ("Now", 150, "end"), ("Proposed", 170, "end"), ("Change", 150, "end"),
            ("Used so far", 150, "end"), ("Available after", 170, "end")]
    data_table(s, X0, y + 60, cols, rows, row_h=62, check=False, size=13.5)
    s.text(X0 + 24, y + 316, "Used so far = spent + committed + reserved. Neither line goes below what it has already used.",
           12.5, 500, MUTED)
    y2 = y + 350
    s.rect(X0, y2, lw, 250, fill=CARD, rx=16, stroke=LINE, name="reason card")
    s.text(X0 + 24, y2 + 38, "Why", 17, 700, INK)
    s.para(X0 + 24, y2 + 70, REVISION["reason"], lw - 48, 14.5, 400, INK2, lh=23)
    s.text(X0 + 24, y2 + 150, "ATTACHMENTS", 10.5, 700, MUTED, spacing=0.8)
    ax = X0 + 24
    for name in ["Kamuli enrolment, Oct 2026.pdf", "KFHI reallocation email, 8 Oct.pdf"]:
        w = tw(name, 13, 600) + 50
        s.rect(ax, y2 + 166, w, 40, fill=FIELD_BG, rx=10, stroke=LINE)
        s.icon("paperclip", ax + 12, y2 + 177, 17, INK2, 1.9)
        s.text(ax + 36, y2 + 191, name, 13, 600, INK)
        ax += w + 12
    if decide:
        decision_panel(s, X0 + lw + 20, Y0 + 148, CW - lw - 20, viewer="samuel", maker="ruth", what="revision",
                       comment="Agreed. KFHI confirmed the reallocation on 8 Oct.",
                       steps=[("Revision approval", "Samuel Kato · Country Director", "now")], back=back)
    else:
        approval_panel(s, X0 + lw + 20, Y0 + 148, CW - lw - 20, 600, [
            ("Submitted", "Ruth Nakato · Finance Officer · Fri 9 Oct, 16:12", "done"),
            ("Revision approval", "Samuel Kato · Country Director · waiting 3 days", "now"),
            ("Budget updated", "Old → new recorded in the audit trail", "next")],
            ("Samuel Kato", "Country Director · step 1 of 1 · he decides from My approvals or from here"))
    return s


def w31b_revision_approval():
    return _revision_page("31b Approve budget revision BR-2026-0007", "My approvals", ["My approvals", "BR-2026-0007"],
                          "samuel", decide=True, back="w02")


# ---------------------------------------------------------------- making and changing budgets
FINANCE = ["Finance Officer", "System Admin"]   # who prepares budgets and revisions (the maker); the CD approves


def w30e_new_budget():
    """A new budget: its header (financial year, project) and its lines, entered one by one or imported from Excel.
    It is saved as a draft; Finance submits it and the Country Director approves it."""
    s = writes(console("30e New budget", "Budgets", ["Budgets", "New budget"], "ivan"), FINANCE)
    y = page_head(s, "New budget", "Saved as a draft. Submit it when the lines are in; the Country Director approves it.",
                  actions=[("Save draft", "primary", "check", "w30"), ("Cancel", "secondary", None, "!back:w30")])
    lw = 1090
    s.rect(X0, y, lw, 176, fill=CARD, rx=16, stroke=LINE, name="budget header")
    x, w = X0 + 28, lw - 56
    hw = (w - 24) / 2
    s.text(x, y + 40, "Budget", 17, 700, INK)
    field(s, x, y + 58, hw, "Financial year", "FY 2027 · planning", required=True, dropdown=True, icon="calendar",
          hint="From Setup › Financial years")
    field(s, x + hw + 24, y + 58, hw, "Project", "Choose a project", required=True, dropdown=True, icon="folder",
          placeholder=True, focus=True, hint="Its donor, department and cost centre fill in")
    y2 = y + 196
    s.rect(X0, y2, lw, 336, fill=CARD, rx=16, stroke=LINE, name="lines")
    s.text(x, y2 + 40, "Lines", 17, 700, INK)
    tabs(s, x + 80, y2 + 18, ["Line by line", "Import from Excel"], "Line by line")
    cols = [("Account code", 300, "start"), ("Description", 420, "start"), ("Cost centre", 160, "start"),
            ("Amount (UGX)", 210, "end")]
    rows = [[c_text("Choose an account code", FAINT), c_text("What the money is for", FAINT), c_text("From the project", FAINT),
             lambda s_, x_, y_, w_, h_: s_.text(x_ + w_ - 16, y_ + h_ / 2 + 5, "0", 13.5, 400, FAINT, anchor="end")]]
    end = data_table(s, X0, y2 + 76, cols, rows, row_h=58, check=False)
    button(s, x, end + 16, "Add a line", "soft", icon="plus", h=38, size=13)
    s.text(x + w, end + 42, "Total  UGX 0", 17, 700, INK, anchor="end", family="display")
    note(s, x, end + 80, w, "Account codes and cost centres come from Setup; the Excel import checks every row against "
         "them before anything is saved.", icon="info")
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 270, fill=CARD, rx=16, stroke=LINE, name="what happens")
    timeline(s, rx + 24, y + 24, rw - 48, [
        ("Draft, prepared by you", "Lines can change freely while it is a draft", "now"),
        ("Budget approval", "Samuel Kato · Country Director", "next"),
        ("Active", "Requisitions can draw on it; changes only by revision", "next")], title="What happens")
    note(s, rx, y + 290, rw, "Whoever prepares a budget can't approve it.", icon="shield")
    return s


def w31c_new_revision():
    """Editing an active budget = asking for a revision: old → new per line, a reason, the Country Director decides."""
    s = writes(console("31c Request a budget revision: Kasese ICT Hub FY 2026", "Budget revisions",
                       ["Budgets", "Budget revisions", "New revision"], "ivan"), FINANCE)
    y = page_head(s, "Request a budget revision", ref_line=("BUD-2026-001", "Kasese ICT Hub · FY 2026 · active · "
                  "UGX 296,000,000"), actions=[("Submit for approval", "primary", "send", "w31"),
                                              ("Save draft", "secondary", None, "w31"),
                                              ("Cancel", "secondary", None, "!back:w31")])
    lw = 1090
    s.rect(X0, y, lw, 420, fill=CARD, rx=16, stroke=LINE, name="lines to change")
    s.text(X0 + 24, y + 38, "Lines to change", 17, 700, INK)
    s.text(X0 + 170, y + 38, "Moving money between lines keeps the total at UGX 296,000,000", 13, 400, MUTED)
    lines = [("5230", "Solar backup and electrical works", 48_000_000, 6_200_000, 40_000_000),
             ("5220", "Accessible desks and chairs", 24_000_000, 21_350_000, 32_000_000)]
    rows = [[c_ref(acc, d), c_money(old, bold=False), c_money(used, bold=False), _input_cell(new),
             _change_cell(new - old)] for acc, d, old, used, new in lines]
    rows.append([c_text("Budget total", INK, 700), c_money(KASESE_TOTAL, bold=False), c_text(""),
                 c_money(KASESE_TOTAL), _change_cell(0)])
    cols = [("Line", 380, "start"), ("Now", 160, "end"), ("Used so far", 160, "end"), ("New budget", 220, "start"),
            ("Change", 170, "end")]
    end = data_table(s, X0, y + 60, cols, rows, row_h=64, check=False)
    button(s, X0 + 24, end + 16, "Add a line", "soft", icon="plus", h=36, size=13)
    s.text(X0 + 24, y + 400, "A line can't go below what it has already used (spent + committed + reserved).", 12.5,
           500, MUTED)
    s.rect(X0, y + 440, lw, 254, fill=CARD, rx=16, stroke=LINE, name="reason")
    s.text(X0 + 24, y + 478, "Why", 17, 700, INK)
    textarea(s, X0 + 24, y + 494, lw - 48, 84, "Reason", "Training room 3 needs accessible desks; the solar works came in "
             "UGX 8M under estimate.", required=True)
    s.rect(X0 + 24, y + 620, lw - 48, 44, fill=FIELD_BG, rx=10, stroke=LINE, dash="5 4")
    s.icon("paperclip", X0 + 40, y + 633, 18, BRAND, 2)
    s.text(X0 + 68, y + 647, "Solar works completion certificate.pdf", 13.5, 600, INK)
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 270, fill=CARD, rx=16, stroke=LINE, name="what happens")
    timeline(s, rx + 24, y + 24, rw - 48, [
        ("Prepared by you", "Submitted for approval when you send it", "now"),
        ("Revision approval", "Samuel Kato · Country Director", "next"),
        ("The budget changes", "Old → new is kept in the audit trail", "next")], title="What happens")
    note(s, rx, y + 290, rw, "The live budget keeps running unchanged until the revision is approved. Draft budgets "
         "(FY 2027) are edited directly, line by line.", icon="lock")
    return s


def _input_cell(v):
    def f(s_, x, y, w, h):
        s_.rect(x + 14, y + h / 2 - 19, w - 30, 38, fill=CARD, rx=8, stroke=BRAND, sw=1.4)
        s_.text(x + 28, y + h / 2 + 5, f"{v:,.0f}", 14, 700, INK)
    return f


# ---------------------------------------------------------------- the revision, opened from Budgets › Budget revisions
CRUMBS_REV = ["Budgets", "Budget revisions", "BR-2026-0007"]


def w31d_revision():
    return _revision_page("31d Budget revision BR-2026-0007", "Budget revisions", CRUMBS_REV)


def w31d_samuel():
    return _revision_page("31d Budget revision BR-2026-0007 (your decision)", "Budget revisions", CRUMBS_REV, "samuel",
                          decide=True, back="w31")


w31d_samuel.key = "w31d-samuel"


def _arrow_cell(new):
    def f(s_, x, y, w, h):
        s_.text(x + w - 16, y + h / 2 + 5, f"{new:,.0f}", 14, 700, INK, anchor="end")
        s_.icon("arrowright", x + 6, y + h / 2 - 8, 16, FAINT, 2)
    return f


def _change_cell(d):
    def f(s_, x, y, w, h):
        if d == 0:
            s_.text(x + w - 16, y + h / 2 + 5, "no change", 13, 600, MUTED, anchor="end")
        else:
            col = BRAND_M if d > 0 else RED
            chip(s_, x + w - 16, y + h / 2 - 12, f"{'+' if d > 0 else '−'}{abs(d):,.0f}", col, anchor="end")
    return f



# ---------------------------------------------------------------- reports
def w40_register():
    s = console("40 Report: Procurement register", "Procurement register", ["Reports", "Procurement register"], "ivan")
    y = page_head(s, "Procurement register", "Every procurement file this financial year, its method, value and stage.",
                  actions=[("Export", "primary", "download", None), ("Print", "secondary", "printer", None)])
    gw = (CW - 3 * 20) / 4
    stat_card(s, X0, y, gw, 128, "folder", BRAND, "Files FY 2026", "98", sub="21 open · 74 closed · 3 cancelled", value_size=30)
    stat_card(s, X0 + gw + 20, y, gw, 128, "clipboard", TEAL, "Value requested", "UGX 1.21B", sub="Estimates on approved requisitions", value_size=30)
    stat_card(s, X0 + 2 * (gw + 20), y, gw, 128, "receipt", BRAND_D, "LPOs issued", "UGX 742.6M", sub="61 LPOs to 23 suppliers", value_size=30)
    stat_card(s, X0 + 3 * (gw + 20), y, gw, 128, "clock", AMBER_D, "Requisition → LPO", "19 days", sub="Average this year · 26 days in FY 2025", value_size=30)
    y += 148
    rows, links = [], []
    for no, title, proj, office, acc, req, val, stage, st, waiting, since, method in FILES[:10]:
        rows.append([c_ref(no, title), c_text(PROJECT[proj][1], INK2), c_text(method, INK2), c_money(val),
                     _stage_cell(stage, st), c_person(req, False)])
        links.append("w11" if no == "PR-2026-0087" else None)
    cols = [("File", 380, "start"), ("Project", 290, "start"), ("Method", 210, "start"), ("Value (UGX)", 150, "end"),
            ("Stage", 230, "start"), ("Requested by", 252, "start")]
    list_card(s, y, 78 + 44 + 58 * len(rows) + 58)
    toolbar(s, X0, y, CW, "Search the register…", filters=["FY 2026", "All projects", "All methods"], export=False)
    end = data_table(s, X0, y + 78, cols, rows, links=links, row_h=58, sort={"File", "Value (UGX)"}, hl=links.index("w11"))
    pager(s, X0, end, CW, (1, 10), 98, pages=10)
    return s


def _stage_cell(stage, status):
    def f(s_, x, y, w, h):
        mini_track(s_, x + 16, y + h / 2 - 12, stage, 118, status)
        s_.text(x + 16, y + h / 2 + 16, status if status != stage else stage, 12.5, 600, INK2)
    return f


def w41_utilisation():
    s = console("41 Report: Budget utilisation", "Budget utilisation", ["Reports", "Budget utilisation"], "ivan")
    y = page_head(s, "Budget utilisation", "How much of each FY 2026 budget is spent, committed and still available.",
                  actions=[("Export", "primary", "download", None)])
    # monthly commitments + by donor
    lw = 1010
    s.rect(X0, y, lw, 300, fill=CARD, rx=16, stroke=LINE)
    s.text(X0 + 24, y + 38, "Committed each month", 17, 700, INK)
    s.text(X0 + 24, y + 60, "LPOs issued, UGX millions, Jan–Oct 2026", 13, 400, MUTED)
    column_chart(s, X0 + 24, y + 86, lw - 48, 172, FY_SPEND_BY_MONTH,
                 ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"], hl=8, unit="M", y_step=20,
                 y_max=80)
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 300, fill=CARD, rx=16, stroke=LINE)
    s.text(rx + 24, y + 38, "By donor", 17, 700, INK)
    s.text(rx + 24, y + 60, "Approved FY 2026 budgets", 13, 400, MUTED)
    by = {}
    for b in BUDGETS:
        by[b[2]] = by.get(b[2], 0) + b[3]
    parts = [(by["KFHI"], BRAND_M), (by["KOICA"], KOICA), (by["IDIU"], AMBER_D)]
    donut(s, rx + 120, y + 186, 86, 24, parts)
    s.text(rx + 120, y + 186, f"{sum(by.values()) / 1e6:,.0f}M", 22, 700, INK, anchor="middle", family="display")
    s.text(rx + 120, y + 206, "UGX", 12, 500, MUTED, anchor="middle")
    ly = y + 140
    for d, col in [("KFHI", BRAND_M), ("KOICA", KOICA), ("IDIU", AMBER_D)]:
        legend_dot(s, rx + 250, ly, {"KFHI": "KFHI", "KOICA": "KOICA", "IDIU": "IDIU own funds"}[d], col, 13)
        s.text(rx + rw - 24, ly, f"{by[d] / 1e6:,.1f}M", 14, 700, INK, anchor="end")
        ly += 36
    y += 320
    rows, links = [], []
    for code, proj, donor, total, sp, cm, rs, st, lines, appr in BUDGETS:
        rows.append([c_two(PROJECT[proj][1], code), c_chip(donor, DONOR_COLOUR[donor]), c_money(total),
                     c_money(sp, bold=False), c_money(cm + rs, bold=False), c_money(total - sp - cm - rs),
                     _use_cell(total, sp, cm, rs)])
        links.append("w30b" if code == "BUD-2026-001" else None)
    cols = [("Project", 380, "start"), ("Donor", 120, "start"), ("Budget", 160, "end"), ("Spent", 160, "end"),
            ("Committed & reserved", 200, "end"), ("Available", 160, "end"), ("Use", 384, "start")]
    list_card(s, y, 44 + 60 * len(rows) + 60)
    end = data_table(s, X0, y, cols, rows, links=links, row_h=60, check=False)
    budget_legend(s, X0 + 24, end + 36)
    return s


SCREENS = [w30_budgets, w30b_budget, w30c_draft_budget, w30d_import, w30e_new_budget, w31_revisions,
           w31b_revision_approval, w31c_new_revision, w31d_revision, w31d_samuel,
           w40_register, w41_utilisation]
