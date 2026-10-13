"""Procurement (w10–w15d): requisitions, the procurement file, RFQs and quotations, evaluation, LPOs, deliveries.

One procurement file per purchase. The lists (Requisitions, RFQs, Evaluations, LPOs, Deliveries) are views of
the same files; the flagship PR-2026-0087 (10 laptops, Kasese ICT Hub) is complete and closed today, and its
eight tabs (Overview · Approvals · Sourcing · Evaluation · LPO · Delivery · Payment · Documents & history) show
the whole trail. Action screens use files that are genuinely waiting today (PLAN.md §2).
"""
from __future__ import annotations

from charts import budget_bar, budget_legend, file_track, mini_track
from data import (DESKS, FILES, LAPTOPS, PEOPLE, PROJECT, STATIONERY, WASHROOM)
from kit import (AMBER_D, BRAND, BRAND_D, BRAND_M, CARD, FAINT, FIELD_BG, INK, INK2, KOICA, LIME, LIME_D, LINE,
                 LINE2, MUTED, ORANGE, RED, TEAL, VIOLET, avatar, button, checkbox, chip, field, radio, ref, status_chip,
                 textarea, tint, tw)
from shell import (writes, decision_panel, CW, X0, X1, Y0, c_chip, c_money, c_person, c_ref, c_status, c_text, c_two, console, data_table,
                   list_card, note, page_head, pager, record_header, tabs, toolbar)

L = LAPTOPS


def _m(n):
    return f"{n:,.0f}"


# ---------------------------------------------------------------- the procurement file (PR-2026-0087)
FILE_TABS = [("Overview", "w11"), ("Approvals", "w11b"), ("Sourcing", "w12c"), ("Evaluation", "w13d"), ("LPO", "w14b"),
             ("Delivery", "w15d"), ("Payment", "w15c"), ("Documents & history", "w11c")]


def file_header(s, tab):
    """PR-2026-0087's header (track complete) and its tabs. Returns the y where tab content starts."""
    y = record_header(
        s, Y0, L["no"], L["title"],
        chips=[("Closed", None, "status"), ("KOICA", KOICA, "chip"), ("RFQ + committee", VIOLET, "chip")],
        facts=[("Project", "Kasese ICT Hub"), ("Requested by", "Grace Atim · 14 Sep"), ("Line", "5210 ICT equipment"),
               ("LPO value", "UGX 36,400,000")],
        actions=[("Download complete file", "secondary", "download", "w11c")],
        track=lambda s_, x, y_, w: file_track(s_, x, y_, w, "Closed", complete=True, waiting="Mon 12 Oct, 09:41",
                                              since="28 days from request to close"))
    tabs(s, X0 + 4, y + 18, [t if t != "Approvals" else ("Approvals", 6) for t, _ in FILE_TABS], tab,
         {t: k for t, k in FILE_TABS if t != tab})
    return y + 80


def _card(s, x, y, w, h, title, sub=None, name=None):
    s.rect(x, y, w, h, fill=CARD, rx=16, stroke=LINE, name=name or title)
    s.text(x + 24, y + 38, title, 17, 700, INK)
    if sub:
        s.text(x + 24 + tw(title, 17, 700) + 12, y + 38, sub, 13, 400, MUTED)


def _tile(s, x, y, w, label, value, sub, color=INK, mono=False):
    s.text(x, y, label, 12.5, 600, MUTED)
    if mono:
        ref(s, x, y + 26, value, 15, color, 600)
    else:
        s.text(x, y + 27, value, 17, 700, color, maxw=w - 10)
    s.text(x, y + 48, sub, 12.5, 400, MUTED, maxw=w - 10)


def w10c_new_requisition():
    """A blank requisition for whoever is signed in (Grace's half-finished one is w10b, from her dashboard)."""
    s = writes(console("10c New requisition", "Requisitions", ["Procurement", "Requisitions", "New requisition"], "ivan"))
    y = page_head(s, "New requisition", "Requested by you: your department and office come from your account.",
                  actions=[("Submit for approval", "primary", "send", "w10"), ("Save draft", "secondary", None, "w10"),
                           ("Cancel", "secondary", None, "!back:w10")])
    lw = 1040
    s.rect(X0, y, lw, 760, fill=CARD, rx=16, stroke=LINE, name="form")
    x, w = X0 + 28, lw - 56
    hw = (w - 24) / 2
    s.text(x, y + 40, "What you need", 17, 700, INK)
    yy = y + 60
    yy += field(s, x, yy, w, "Title", "e.g. Projector and screen for training room 2", required=True, placeholder=True,
                focus=True) + 16
    s.text(x, yy + 14, "Items", 13, 600, INK2)
    s.text(x + 44, yy + 14, "*", 13, 600, RED)
    yy += 24
    cols = [("Description", 470, "start"), ("Qty", 80, "start"), ("Unit", 120, "start"), ("Est. unit price", 160, "end"),
            ("Total", 154, "end")]
    rows = [[c_text("Describe the item", FAINT), c_text("1", FAINT), c_text("Piece", FAINT),
             lambda s_, x_, y_, w_, h_: s_.text(x_ + w_ - 16, y_ + h_ / 2 + 5, "0", 13.5, 400, FAINT, anchor="end"),
             c_money(0, bold=False)]]
    end = data_table(s, x, yy, cols, rows, row_h=52, check=False, head_h=38, size=13.5)
    button(s, x, end + 12, "Add item", "soft", icon="plus", h=36, size=13)
    s.text(x + w, end + 36, "Estimated total  UGX 0", 16, 700, INK, anchor="end", family="display")
    yy = end + 66
    field(s, x, yy, hw, "Needed by", "Choose a date", required=True, icon="calendar", placeholder=True)
    field(s, x + hw + 24, yy, hw, "Delivery to", "Choose an office", required=True, icon="pin", placeholder=True,
          dropdown=True)
    yy += 90
    textarea(s, x, yy, w, 72, "Justification", "Why it is needed, and for whom", required=True, placeholder=True)
    yy += 108
    s.line(X0, yy, X0 + lw, yy, LINE2)
    s.text(x, yy + 40, "Charge to", 17, 700, INK)
    yy += 56
    field(s, x, yy, hw, "Project", "Choose a project", required=True, dropdown=True, icon="folder", placeholder=True)
    field(s, x + hw + 24, yy, hw, "Budget line", "Choose a line (active budgets only)", required=True, dropdown=True,
          icon="wallet", placeholder=True)
    yy += 100
    s.rect(x, yy, w, 44, fill=FIELD_BG, rx=10, stroke=LINE, dash="5 4")
    s.icon("paperclip", x + 16, yy + 13, 18, BRAND, 2)
    s.text(x + 44, yy + 27, "Attach quotes, specifications or photos", 13.5, 500, MUTED)
    s.text(x + w - 16, yy + 27, "Browse", 13, 600, BRAND, anchor="end")
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 250, fill=CARD, rx=16, stroke=LINE, name="budget check")
    s.text(rx + 24, y + 40, "Budget check", 17, 700, INK)
    s.rect(rx + 24, y + 66, rw - 48, 156, fill=FIELD_BG, rx=12, stroke=LINE, dash="5 4")
    s.icon("wallet", rx + rw / 2 - 14, y + 96, 28, FAINT, 2)
    s.text(rx + rw / 2, y + 156, "Choose a budget line to see what is left", 14, 600, INK2, anchor="middle")
    s.text(rx + rw / 2, y + 180, "A requisition can't go over the line's available amount", 12.5, 400, MUTED,
           anchor="middle")
    s.rect(rx, y + 270, rw, 330, fill=CARD, rx=16, stroke=LINE, name="approval path")
    s.text(rx + 24, y + 310, "Approval path", 17, 700, INK)
    s.text(rx + 24, y + 332, "Worked out from the value when you submit", 13, 400, MUTED)
    steps = [("1  Department review", "Your Department Head"), ("2  Funds check", "Finance Officer"),
             ("3  Executive approval", "Country Director · only above UGX 30M")]
    sy = y + 372
    for i, (step, who) in enumerate(steps):
        if i < 2:
            s.line(rx + 44, sy + 18, rx + 44, sy + 56, LINE, 2)
        s.circle(rx + 44, sy + 4, 14, fill=CARD, stroke=FAINT, sw=1.5)
        s.text(rx + 72, sy, step, 14, 700, INK)
        s.text(rx + 72, sy + 19, who, 12.5, 400, MUTED)
        sy += 64
    note(s, rx + 24, y + 540, rw - 48, "Whoever raises a requisition can't approve any of its steps.", icon="shield")
    return s


def w11_file():
    s = console("11 File PR-2026-0087: Overview", "Requisitions", ["Requisitions", L["no"]], "ivan")
    y = file_header(s, "Overview")
    lw = 1010
    # what was asked for
    _card(s, X0, y, lw, 228, "Requirement", "as Grace raised it on 14 Sep")
    rows = [[c_two("Laptop, Core i5 (13th gen), 16 GB, 512 GB SSD, 14\"", "Windows 11 Pro · screen-reader ready · 3-year warranty"),
             c_text("10 Piece", INK2), c_money(L["unit_est"], "estimate", bold=False), c_money(L["est"], "estimate"),
             c_money(L["lpo_value"], "awarded")]]
    cols = [("Item", 470, "start"), ("Qty", 100, "start"), ("Unit price", 140, "end"), ("Total", 140, "end"),
            ("LPO", 160, "end")]
    data_table(s, X0, y + 56, cols, rows, row_h=60, check=False)
    s.text(X0 + 24, y + 186, "Why", 12.5, 700, MUTED)
    s.para(X0 + 64, y + 186, L["justification"], lw - 300, 13.5, 400, INK2, lh=20)
    s.text(X0 + lw - 24, y + 186, "Needed by Fri 16 Oct", 13, 600, INK2, anchor="end")
    # how it went
    y2 = y + 248
    _card(s, X0, y2, lw, 300, "How it went")
    tiles = [("Method", "RFQ + committee", "Above UGX 30M"),
             ("Sourcing", L["rfq"], "4 invited · 3 quoted · 1 non-compliant"),
             ("Award", "Busoga Tech Supplies", "Score 88.4 · approved 5 Oct"),
             ("Order", L["lpo"], "Issued 6 Oct · acknowledged the same day"),
             ("Delivery", L["grn"], "9 Oct · 10 of 10 accepted"),
             ("Payment", L["payment_ref"], "12 Oct · voucher PV-2026-1184")]
    tw_ = (lw - 48) / 3
    for i, (lab, val, sub) in enumerate(tiles):
        tx = X0 + 24 + (i % 3) * tw_
        ty = y2 + 82 + (i // 3) * 92
        _tile(s, tx, ty, tw_, lab, val, sub, BRAND if val.startswith(("RFQ-", "LPO-", "GRN-", "EFT-")) else INK,
              mono=val.startswith(("RFQ-", "LPO-", "GRN-", "EFT-")))
    s.line(X0 + 24, y2 + 250, X0 + lw - 24, y2 + 250, LINE2)
    s.icon("trendup", X0 + 24, y2 + 264, 18, BRAND_M, 2.2)
    s.text(X0 + 50, y2 + 278, "UGX 1,600,000 under the estimate", 13.5, 700, BRAND_M)
    s.text(X0 + 290, y2 + 278, "· requisition to LPO in 22 days (IDIU average this year: 19)", 13.5, 400, MUTED)
    # right column
    rx, rw = X0 + lw + 20, CW - lw - 20
    _card(s, rx, y, rw, 228, "Three-way match")
    mx = rx + 24
    for i, (lab, code, val) in enumerate([("LPO", L["lpo"], "36,400,000"), ("Goods received", L["grn"], "10 of 10"),
                                          ("Invoice", L["invoice"], "36,400,000")]):
        my = y + 66 + i * 40
        s.circle(mx + 10, my + 6, 10, fill=tint(BRAND_M, 0.15))
        s.icon("check", mx + 3, my - 1, 14, BRAND_M, 3)
        s.text(mx + 30, my + 11, lab, 13.5, 600, INK)
        ref(s, mx + 150, my + 11, code, 12.5, INK2)
        s.text(rx + rw - 24, my + 11, val, 13.5, 700, INK, anchor="end")
    s.rect(rx + 24, y + 182, rw - 48, 30, fill=tint(BRAND_M, 0.1), rx=8)
    s.text(rx + 38, y + 202, "All three agree: payment was released", 12.5, 700, BRAND_D)
    _card(s, rx, y2, rw, 300, "Budget line", "5210 ICT equipment")
    s.text(rx + 24, y2 + 74, "UGX 160,000,000", 20, 700, INK, family="display")
    s.text(rx + 24, y2 + 96, "Kasese ICT Hub · FY 2026 · BUD-2026-001", 12.5, 400, MUTED)
    budget_bar(s, rx + 24, y2 + 116, rw - 48, 160_000_000, 99_800_000)
    budget_legend(s, rx + 24, y2 + 152, size=11.5)
    for i, (lab, v) in enumerate([("This file (paid)", 36_400_000), ("Spent on the line", 99_800_000),
                                  ("Available", 60_200_000)]):
        ly = y2 + 196 + i * 30
        s.text(rx + 24, ly, lab, 13, 500, INK2)
        s.text(rx + rw - 24, ly, _m(v), 13.5, 700, BRAND_M if lab == "Available" else INK, anchor="end")
    s.link(rx, y2, rw, 300, "w30b")
    return s


def w11b_approvals():
    s = console("11b File PR-2026-0087: Approvals", "Requisitions", ["Requisitions", L["no"], "Approvals"], "ivan")
    y = file_header(s, "Approvals")
    lw = 1010
    groups = [
        ("Requisition", "submitted by Grace Atim · Mon 14 Sep, 09:12", L["approvals"]),
        ("Award recommendation", "prepared by Joseph Waiswa · Fri 2 Oct, 16:30",
         [("samuel", "Award approval", "Mon 5 Oct, 09:20", "Approved",
           "Approved: Busoga Tech Supplies, best score and within budget.")]),
        ("LPO", "prepared by Joseph Waiswa · Mon 5 Oct, 11:02",
         [("ruth", "Commitment check", "Mon 5 Oct, 15:10", "Approved", "Committed on 5210. Available after: UGX 60.2M."),
          ("samuel", "Signature", "Tue 6 Oct, 10:55", "Approved", "Signed.")]),
    ]
    s.rect(X0, y, lw, 650, fill=CARD, rx=16, stroke=LINE, name="approvals card")
    gy = y + 40
    for title, sub, steps in groups:
        s.text(X0 + 28, gy, title, 16, 700, INK)
        s.text(X0 + 28 + tw(title, 16, 700) + 12, gy, sub, 13, 400, MUTED)
        status_chip(s, X0 + lw - 28, gy - 17, "Approved", anchor="end")
        gy += 26
        for i, (who, step, when, dec, comment) in enumerate(steps):
            name, ini, role, *_rest, col = PEOPLE[who]
            if i < len(steps) - 1:
                s.line(X0 + 50, gy + 40, X0 + 50, gy + 80, LINE, 2)
            avatar(s, X0 + 50, gy + 24, 18, ini, col)
            s.text(X0 + 80, gy + 19, f"{step} · {name}", 14, 700, INK)
            s.text(X0 + 80, gy + 38, f"{role} · {when}", 12.5, 400, MUTED)
            chip(s, X0 + lw - 28, gy + 8, dec, BRAND_M, icon="check", anchor="end")
            s.rect(X0 + 80, gy + 48, lw - 300, 30, fill=FIELD_BG, rx=8)
            s.text(X0 + 94, gy + 68, f"“{comment}”", 13, 500, INK2, maxw=lw - 330)
            gy += 92
        gy += 22
    rx, rw = X0 + lw + 20, CW - lw - 20
    _card(s, rx, y, rw, 304, "Rules applied")
    items = [("lock", "Steps were fixed when Grace submitted. Changing the workflow later does not change this file."),
             ("trendup", "Executive approval applied because UGX 38,000,000 is above the UGX 30M threshold."),
             ("shield", "Joseph prepared the award and the LPO, so he could not approve either."),
             ("message", "Every decision carries a comment: returns and rejections need one.")]
    iy = y + 70
    for ic, txt in items:
        s.icon(ic, rx + 24, iy - 4, 18, BRAND, 2)
        h = s.para(rx + 54, iy + 9, txt, rw - 80, 13, 500, INK2, lh=19)
        iy += h + 18
    note(s, rx, y + 324, rw, "Approval workflows are set in Administration › Approval workflows (thresholds are examples "
         "until IDIU's procurement manual is applied).", icon="workflow")
    return s


def w11c_documents():
    s = console("11c File PR-2026-0087: Documents & history", "Requisitions",
                ["Requisitions", L["no"], "Documents & history"], "ivan")
    y = file_header(s, "Documents & history")
    lw = 900
    docs = [("Requisition", [("Requisition PR-2026-0087.pdf", "Grace Atim", "14 Sep"), ("Laptop specification.pdf", "Grace Atim", "14 Sep")]),
            ("Sourcing", [("RFQ-2026-0031.pdf", "Joseph Waiswa", "17 Sep"), ("3 quotations (Busoga Tech, Kagulu, Source Point)", "Suppliers", "24–28 Sep")]),
            ("Evaluation", [("Conflict-of-interest declarations (3)", "Committee", "30 Sep"), ("Evaluation report.pdf", "Esther Namutebi", "1 Oct"),
                            ("Award approval memo.pdf", "Samuel Kato", "5 Oct")]),
            ("Order & delivery", [("LPO-2026-0051 (signed).pdf", "Samuel Kato", "6 Oct"), ("Delivery note DN-4471.jpg", "Peter Mukasa", "9 Oct"),
                                  ("GRN-2026-0064.pdf + 4 photos", "Peter Mukasa", "9 Oct")]),
            ("Payment", [("Invoice BTS-INV-0912.pdf", "Ruth Nakato", "12 Oct"), ("Payment voucher PV-2026-1184.pdf", "Ruth Nakato", "12 Oct")])]
    s.rect(X0, y, lw, 650, fill=CARD, rx=16, stroke=LINE, name="documents card")
    s.text(X0 + 24, y + 38, "Documents", 17, 700, INK)
    s.text(X0 + 128, y + 38, "23 files in this procurement file", 13, 400, MUTED)
    gy = y + 66
    for grp, items in docs:
        s.text(X0 + 24, gy + 16, grp.upper(), 10.5, 700, MUTED, spacing=0.8)
        gy += 26
        for name, by, on in items:
            s.rect(X0 + 24, gy, lw - 48, 33, fill=FIELD_BG, rx=8)
            s.icon("file" if not name.endswith(".jpg") else "image", X0 + 36, gy + 8, 17, BRAND, 1.9)
            s.text(X0 + 64, gy + 21.5, name, 13.5, 600, INK, maxw=lw - 360)
            s.text(X0 + lw - 70, gy + 21.5, f"{by} · {on}", 12.5, 400, MUTED, anchor="end")
            s.icon("download", X0 + lw - 58, gy + 8, 17, INK2, 1.9)
            gy += 37
        gy += 4
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 650, fill=CARD, rx=16, stroke=LINE, name="history card")
    s.text(rx + 24, y + 38, "History", 17, 700, INK)
    s.text(rx + 104, y + 38, "every action on this file, from the audit trail", 13, 400, MUTED)
    events = [("joseph", "Closed the file", "Mon 12 Oct, 09:41"),
              ("ruth", "Recorded payment EFT-STB-26-10-0331", "Mon 12 Oct, 09:38"),
              ("ruth", "Recorded invoice BTS-INV-0912 (3-way match passed)", "Mon 12 Oct, 09:12"),
              ("peter", "Recorded GRN-2026-0064: 10 of 10 accepted", "Fri 9 Oct, 14:42"),
              ("joseph", "Issued LPO-2026-0051 to Busoga Tech Supplies", "Tue 6 Oct, 11:30"),
              ("samuel", "Approved the award", "Mon 5 Oct, 09:20"),
              ("esther", "Submitted the evaluation report", "Thu 1 Oct, 17:05"),
              ("joseph", "Closed RFQ-2026-0031: 3 quotations", "Mon 28 Sep, 12:00"),
              ("joseph", "Sent RFQ-2026-0031 to 4 suppliers", "Thu 17 Sep, 10:20"),
              ("samuel", "Approved the requisition (step 3 of 3)", "Wed 16 Sep, 08:47"),
              ("grace", "Raised the requisition", "Mon 14 Sep, 09:12")]
    ey = y + 74
    for i, (who, what, when) in enumerate(events):
        name, ini, *_rest, col = PEOPLE[who]
        if i < len(events) - 1:
            s.line(rx + 40, ey + 18, rx + 40, ey + 50, LINE, 2)
        avatar(s, rx + 40, ey + 4, 13, ini, col)
        s.text(rx + 64, ey + 0, what, 13.5, 600, INK, maxw=rw - 90)
        s.text(rx + 64, ey + 18, f"{name} · {when}", 12, 400, MUTED)
        ey += 52
    s.link(rx, y + 600, rw, 50, "w63")
    s.text(rx + 24, y + 630, "Open the full audit trail →", 13, 700, BRAND)
    return s


# ---------------------------------------------------------------- requisitions
def _stage_cell(stage, status, waiting=None, since=None):
    def f(s_, x, y, w, h):
        mini_track(s_, x + 16, y + h / 2 - 13, stage, 126, status)
        lab = status
        s_.text(x + 16, y + h / 2 + 15, lab, 12.5, 700, INK2)
    return f


def _waiting_cell(waiting, since, status):
    def f(s_, x, y, w, h):
        if waiting == "—":
            s_.text(x + 16, y + h / 2 + 5, "—", 13.5, 500, FAINT)
            return
        s_.text(x + 16, y + h / 2 - 3, waiting, 13.5, 600, INK, maxw=w - 26)
        late = since.endswith("days") and int(since.split()[0]) >= 3
        s_.text(x + 16, y + h / 2 + 15, since, 12, 600 if late else 400, AMBER_D if late else MUTED)
    return f


def w10_requisitions():
    s = console("10 Requisitions", "Requisitions", ["Procurement", "Requisitions"], "ivan")
    y = page_head(s, "Requisitions", "Every purchase starts here. Each row is one procurement file, from request to close.",
                  actions=[("New requisition", "primary", "plus", "w10c")])
    files = FILES[:10]   # page 1 of 98 (FY 2026: 21 open, 74 closed, 3 cancelled)
    row_h = 60
    list_card(s, y, 58 + 78 + 44 + row_h * len(files) + 58)
    tabs(s, X0 + 24, y + 14, [("All", 98), ("Awaiting approval", 2), ("Returned", 1), ("Drafts", 1),
                              ("In progress", 17), ("Closed", 74)], "All")
    toolbar(s, X0, y + 50, CW, "Search by number, title or supplier…", filters=["FY 2026"])
    rows, links = [], []
    targets = {"PR-2026-0087": "w11", "PR-2026-0098": "w10b", "PR-2026-0091": "w12b"}
    for no, title, proj, office, acc, req, val, stage, st, waiting, since, method in files:
        rows.append([c_ref(no, title), c_two(PROJECT[proj][1], f"{acc} · {office}", bold=False), c_person(req, False),
                     c_money(val), _stage_cell(stage, st), _waiting_cell(waiting, since, st)])
        links.append(targets.get(no))
    cols = [("File", 360, "start"), ("Project · line", 330, "start"), ("Requested by", 200, "start"),
            ("Value (UGX)", 150, "end"), ("Stage", 200, "start"), ("Waiting on", 272, "start")]
    end = data_table(s, X0, y + 50 + 78, cols, rows, links=links, row_h=row_h, sort={"File", "Value (UGX)"},
                     hl=[f[0] for f in files].index("PR-2026-0087"))
    pager(s, X0, end, CW, (1, 10), 98, pages=10)
    return s


def w10b_new_requisition():
    s = console("10b New requisition (Grace)", "Requisitions", ["Procurement", "Requisitions", "New requisition"], "grace", owner=True)
    y = page_head(s, "New requisition", None,
                  actions=[("Submit for approval", "primary", "send", "w10"), ("Save draft", "secondary", None, "w10")],
                  ref_line=("PR-2026-0098", "draft saved 09:31 · Kasese ICT Hub"))
    lw = 1040
    s.rect(X0, y, lw, 820, fill=CARD, rx=16, stroke=LINE, name="form")
    x, w = X0 + 28, lw - 56
    s.text(x, y + 40, "What you need", 17, 700, INK)
    yy = y + 60
    yy += field(s, x, yy, w, "Title", "Projector and screen for training room 2", required=True) + 16
    s.text(x, yy + 14, "Items", 13, 600, INK2)
    s.text(x + 44, yy + 14, "*", 13, 600, RED)
    yy += 24
    items = [("Projector, 4,000 lumens, HDMI, 3-year warranty", "1", "Piece", 3_400_000),
             ("Motorised projection screen, 120\"", "1", "Piece", 800_000)]
    cols = [("Description", 470, "start"), ("Qty", 80, "start"), ("Unit", 120, "start"), ("Est. unit price", 160, "end"),
            ("Total", 154, "end")]
    rows = [[c_text(d, INK, 500), c_text(q), c_text(u, INK2), c_money(p, bold=False), c_money(p * int(q))]
            for d, q, u, p in items]
    end = data_table(s, x, yy, cols, rows, row_h=52, check=False, head_h=38, size=13.5)
    button(s, x, end + 12, "Add item", "soft", icon="plus", h=36, size=13)
    s.text(x + w, end + 36, "Estimated total  UGX 4,200,000", 16, 700, INK, anchor="end", family="display")
    yy = end + 66
    hw = (w - 24) / 2
    field(s, x, yy, hw, "Needed by", "Fri 30 Oct 2026", required=True, icon="calendar")
    field(s, x + hw + 24, yy, hw, "Delivery to", "Kasese field office · training room 2", required=True, icon="pin")
    yy += 90
    textarea(s, x, yy, w, 72, "Justification",
             "Training room 2 opens this month. Trainers need to project screen-reader sessions for 20 learners.",
             required=True)
    yy += 108
    s.line(X0, yy, X0 + lw, yy, LINE2)
    s.text(x, yy + 40, "Charge to", 17, 700, INK)
    yy += 56
    field(s, x, yy, hw, "Project", "KSE-ICT · Kasese ICT Hub (KOICA)", required=True, dropdown=True, icon="folder")
    field(s, x + hw + 24, yy, hw, "Budget line", "5210 · ICT equipment · KSE", required=True, dropdown=True,
          icon="wallet", ok="Active budget BUD-2026-001")
    yy += 100
    s.rect(x, yy, w, 44, fill=FIELD_BG, rx=10, stroke=LINE, dash="5 4")
    s.icon("paperclip", x + 16, yy + 13, 18, BRAND, 2)
    s.text(x + 44, yy + 27, "Projector specification.pdf", 13.5, 600, INK)
    s.text(x + w - 16, yy + 27, "Drop more files or browse", 13, 500, BRAND, anchor="end")
    # right column: budget check + approval path
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 330, fill=CARD, rx=16, stroke=LINE, name="budget check")
    s.text(rx + 24, y + 40, "Budget check", 17, 700, INK)
    s.text(rx + 24, y + 62, "5210 ICT equipment · Kasese ICT Hub · FY 2026", 13, 400, MUTED)
    budget_bar(s, rx + 24, y + 86, rw - 48, 160_000_000, 99_800_000, request=4_200_000, h=12)
    budget_legend(s, rx + 24, y + 124, request=True, size=11.5)
    for i, (lab, v, col) in enumerate([("Line budget", 160_000_000, INK), ("Spent", 99_800_000, INK2),
                                       ("Available now", 60_200_000, INK), ("This request", 4_200_000, AMBER_D)]):
        ly = y + 162 + i * 30
        s.text(rx + 24, ly, lab, 13.5, 500, INK2)
        s.text(rx + rw - 24, ly, _m(v), 14, 700, col, anchor="end")
    s.rect(rx + 24, y + 270, rw - 48, 40, fill=tint(BRAND_M, 0.1), rx=10)
    s.icon("check", rx + 36, y + 281, 18, BRAND_M, 2.6)
    s.text(rx + 62, y + 295, "Within budget: UGX 56,000,000 left after this request", 13, 700, BRAND_D, maxw=rw - 90)
    s.rect(rx, y + 350, rw, 300, fill=CARD, rx=16, stroke=LINE, name="approval path")
    s.text(rx + 24, y + 390, "Approval path", 17, 700, INK)
    chip(s, rx + rw - 24, y + 372, "Direct purchase · up to UGX 5M", BRAND, anchor="end")
    steps = [("daniel", "Department review", "Head of Programmes", True),
             ("ruth", "Funds check", "Finance Officer", True),
             ("samuel", "Executive approval", "Only above UGX 30M · skipped", False)]
    sy = y + 424
    for i, (who, step, sub, applies) in enumerate(steps):
        name, ini, *_rest, col = PEOPLE[who]
        if i < 2:
            s.line(rx + 44, sy + 22, rx + 44, sy + 58, LINE, 2, dash=None if applies else "4 4")
        if applies:
            avatar(s, rx + 44, sy + 4, 17, ini, col)
        else:
            s.circle(rx + 44, sy + 4, 16, fill=CARD, stroke=FAINT, sw=1.5, dash="3 3")
        s.text(rx + 72, sy, f"{i + 1}  {step}", 14, 700, INK if applies else FAINT)
        s.text(rx + 72, sy + 19, f"{name} · {sub}" if applies else sub, 12.5, 400, MUTED if applies else FAINT)
        sy += 62
    note(s, rx + 24, y + 600, rw - 48, "You can't approve your own requisition.", icon="shield", h=36)
    return s


# ---------------------------------------------------------------- RFQs and quotations
RFQS = [
    ("RFQ-2026-0036", "PR-2026-0091 · Desks and chairs", "Furniture", "—", "Not sent", "Draft", "Joseph preparing", "w12b"),
    ("RFQ-2026-0035", "PR-2026-0093 · Network switches and cabling", "ICT", "2 of 4", "Wed 14 Oct, 12:00", "Open", "Closes in 2 days", None),
    ("RFQ-2026-0033", "PR-2026-0090 · Washroom block, Busalamu P/S", "Construction & works", "3 of 3", "Closed 5 Oct", "Evaluation", "Committee scoring", None),
    ("RFQ-2026-0032", "PR-2026-0089 · Printing teacher training manuals", "Printing & stationery", "3 of 3", "Closed 2 Oct", "Award", "Award with the Country Director", None),
    ("RFQ-2026-0031", "PR-2026-0087 · 10 laptops for training room 2", "ICT", "3 of 4", "Closed 28 Sep", "Closed", "Busoga Tech Supplies · 36,400,000", "w12c"),
    ("RFQ-2026-0029", "PR-2026-0084 · Stationery for vocational classes", "Printing & stationery", "3 of 3", "Closed 25 Sep", "LPO issued", "Main Street Stationers · 6,620,000", None),
    ("RFQ-2026-0027", "PR-2026-0079 · Office chairs, Jinja head office", "Furniture", "3 of 3", "Closed 14 Sep", "Closed", "Iganga Office Furnishers · 7,300,000", None),
]


def w12_rfqs():
    s = console("12 RFQs & quotations", "RFQs & quotations", ["Procurement", "RFQs & quotations"], "ivan")
    y = page_head(s, "RFQs & quotations", "Requests for quotations sent to prequalified suppliers, and what came back.")
    rows, links = [], []
    for no, file, cat, quotes, close, st, result, tgt in RFQS:
        rows.append([c_ref(no, file), c_text(cat, INK2), c_text(quotes, INK, 600), c_text(close, INK2), c_status(st),
                     c_text(result, INK2)])
        links.append(tgt)
    cols = [("RFQ", 440, "start"), ("Category", 220, "start"), ("Quotes", 120, "start"), ("Closing", 200, "start"),
            ("Status", 170, "start"), ("Result", 362, "start")]
    list_card(s, y, 78 + 44 + 62 * len(rows) + 58)
    toolbar(s, X0, y, CW, "Search RFQs…", filters=["FY 2026"])
    end = data_table(s, X0, y + 78, cols, rows, links=links, row_h=62, sort={"RFQ"}, hl=links.index("w12c"))
    pager(s, X0, end, CW, (1, len(rows)), 31, pages=4, per=len(rows))
    return s


def w12b_new_rfq():
    s = console("12b New RFQ for PR-2026-0091", "RFQs & quotations", ["Procurement", "RFQs & quotations", "New RFQ"], "joseph", owner=True)
    y = page_head(s, "Request for quotations", None,
                  actions=[("Send RFQ to 3 suppliers", "primary", "send", "w12"), ("Save draft", "secondary", None, "w12")],
                  ref_line=(DESKS["rfq"], "from PR-2026-0091 Desks and chairs, Kamuli ICT centre · approved 9 Oct"))
    lw = 900
    s.rect(X0, y, lw, 790, fill=CARD, rx=16, stroke=LINE, name="rfq form")
    x, w = X0 + 28, lw - 56
    s.text(x, y + 40, "What you are asking for", 17, 700, INK)
    chip(s, x + w, y + 22, "Request for quotations · UGX 18.6M · 3 quotes or more", BRAND, anchor="end")
    cols = [("Item (from the requisition)", 450, "start"), ("Qty", 100, "start"), ("Unit", 120, "start"),
            ("Estimate", 174, "end")]
    rows = [[c_text(d, INK, 500), c_text(str(q)), c_text(u, INK2), c_money(q * p)] for d, q, u, p in DESKS["items"]]
    end = data_table(s, x, y + 60, cols, rows, row_h=52, check=False, head_h=38)
    yy = end + 20
    hw = (w - 24) / 2
    field(s, x, yy, hw, "Closing date and time", "Mon 19 Oct 2026, 12:00", required=True, icon="calendar")
    field(s, x + hw + 24, yy, hw, "Deliver to", "Kamuli field office", required=True, icon="pin", dropdown=True)
    yy += 90
    textarea(s, x, yy, w, 96, "Terms",
             "Delivery within 21 days of the LPO. Payment 30 days after accepted delivery. 1-year warranty on frames "
             "and tops. Quote in UGX, VAT shown separately; prices valid for 60 days.")
    yy += 132
    s.text(x, yy + 14, "How quotations will be compared", 13, 600, INK2)
    radio(s, x + 10, yy + 44, True)
    s.text(x + 30, yy + 49, "Lowest price among quotations that meet the specification", 14, 600, INK)
    radio(s, x + 10, yy + 78, False)
    s.text(x + 30, yy + 83, "Quality and price, scored by an evaluation committee (required above UGX 30M)", 14, 500, MUTED)
    yy += 110
    s.rect(x, yy, w, 44, fill=FIELD_BG, rx=10, stroke=LINE, dash="5 4")
    s.icon("paperclip", x + 16, yy + 13, 18, BRAND, 2)
    s.text(x + 44, yy + 27, "Desk and chair drawings.pdf · RFQ-2026-0036.pdf (generated)", 13.5, 600, INK)
    # suppliers
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 790, fill=CARD, rx=16, stroke=LINE, name="suppliers")
    s.text(rx + 24, y + 40, "Invite suppliers", 17, 700, INK)
    s.text(rx + 24, y + 62, "Prequalified in Furniture · only they can be invited without a reason", 13, 400, MUTED)
    sups = [("Wairaka Woodworks Ltd", "Prequalified · Jinja · 2 LPOs this year", True, "ok"),
            ("Iganga Office Furnishers", "Prequalified · Iganga · 1 LPO this year", True, "ok"),
            ("Mpumudde Furniture Works", "Prequalification awaiting the Country Director", False, "pending")]
    sy = y + 86
    for name, sub, on, kind in sups:
        dis = kind == "pending"
        s.rect(rx + 24, sy, rw - 48, 66, fill=FIELD_BG if dis else CARD, rx=12, stroke=LINE)
        checkbox(s, rx + 42, sy + 24, on, disabled=dis)
        s.text(rx + 74, sy + 29, name, 14.5, 700, FAINT if dis else INK)
        s.text(rx + 74, sy + 49, sub, 12.5, 500, AMBER_D if dis else MUTED)
        if dis:
            chip(s, rx + rw - 40, sy + 21, "Pending", AMBER_D, anchor="end")
        sy += 78
    note(s, rx + 24, sy + 4, rw - 48, "Only 2 Furniture suppliers are prequalified and this method needs 3 quotes. Add a "
         "supplier with a reason, or wait for Mpumudde's prequalification.", icon="alert", color=AMBER_D)
    sy += 96
    s.rect(rx + 24, sy, rw - 48, 190, fill=CARD, rx=12, stroke=BRAND, sw=1.5)
    checkbox(s, rx + 42, sy + 22, True)
    s.text(rx + 74, sy + 36, "Kamuli Carpentry Co-operative", 14.5, 700, INK)
    chip(s, rx + rw - 40, sy + 18, "Not prequalified", ORANGE, anchor="end")
    s.text(rx + 74, sy + 56, "Added by Joseph Waiswa · 0782 113 409", 12.5, 500, MUTED)
    textarea(s, rx + 42, sy + 70, rw - 84, 70, "Reason (recorded on the file)",
             "Local workshop 2 km from the site; Furniture prequalification round opens in November.", required=True)
    sy += 206
    button(s, rx + 24, sy, "Add a non-prequalified supplier", "ghost", icon="plus", h=36, size=13.5)
    s.line(rx + 24, y + 790 - 70, rx + rw - 24, y + 790 - 70, LINE2)
    s.text(rx + 24, y + 790 - 34, "3 suppliers will receive the RFQ by email and in the supplier portal.", 13, 600, INK2)
    return s


def w12c_comparison():
    s = console("12c File PR-2026-0087: Sourcing (quotation comparison)", "RFQs & quotations",
                ["Requisitions", L["no"], "Sourcing"], "ivan")
    y = file_header(s, "Sourcing")
    s.rect(X0, y, CW, 660, fill=CARD, rx=16, stroke=LINE, name="comparison")
    s.text(X0 + 24, y + 40, "Quotation comparison", 17, 700, INK)
    ref(s, X0 + 230, y + 40, L["rfq"], 13, BRAND)
    s.text(X0 + 350, y + 40, "· sent 17 Sep to 4 prequalified ICT suppliers · closed Mon 28 Sep, 12:00", 13, 400, MUTED)
    button(s, X1 - 24, y + 18, "Bid analysis (PDF)", "secondary", icon="download", anchor="end", h=38, size=13)
    lab_w = 300
    colw = (CW - 48 - lab_w) / 4
    tx = X0 + 24
    ty = y + 72
    q = L["quotes"]
    # supplier header row
    for i, (name, total, days, war, comp, tech, fin, score) in enumerate(q):
        cx = tx + lab_w + i * colw
        best = i == 0
        s.rect(cx + 6, ty, colw - 12, 64, fill=LIME if best else FIELD_BG, rx=12)
        s.text(cx + 22, ty + 28, name, 14.5, 700, LIME_D if best else INK, maxw=colw - 44)
        sub = "Recommended" if best else ("Non-compliant" if comp is False else ("No response" if total is None else "Compliant"))
        s.text(cx + 22, ty + 48, sub, 12.5, 700 if best else 500, LIME_D if best else (RED if comp is False else MUTED))
    rows = [("Total quoted (UGX)", lambda i: _m(q[i][1]) if q[i][1] else "—"),
            ("Unit price, 10 laptops", lambda i: _m(q[i][1] / 10) if q[i][1] else "—"),
            ("Delivery", lambda i: f"{q[i][2]} days" if q[i][2] else "—"),
            ("Warranty (3 years required)", lambda i: q[i][3] or "—"),
            ("Meets the specification", lambda i: {True: "Yes", False: "No: 1-year warranty", None: "—"}[q[i][4]]),
            ("Technical score (of 70)", lambda i: f"{q[i][5]:.1f}" if q[i][5] else "—"),
            ("Financial score (of 30)", lambda i: f"{q[i][6]:.1f}" if q[i][6] else "—"),
            ("Total score", lambda i: f"{q[i][7]:.1f}" if q[i][7] else "—")]
    ry = ty + 80
    for r, (lab, fn) in enumerate(rows):
        s.line(tx, ry, X1 - 24, ry, LINE2)
        last = r == len(rows) - 1
        s.text(tx + 4, ry + 34, lab, 13.5, 700 if last else 500, INK if last else INK2)
        for i in range(4):
            cx = tx + lab_w + i * colw
            v = fn(i)
            col = INK
            if v.startswith("No:"):
                col = RED
            elif v == "Yes":
                col = BRAND_M
            elif v == "—":
                col = FAINT
            if i == 0:
                s.rect(cx + 6, ry, colw - 12, 52, fill=tint(LIME, 0.35))
            s.text(cx + 22, ry + 34, v, 15 if last else 14, 700 if (last or i == 0) else 500, col)
        ry += 52
    s.line(tx, ry, X1 - 24, ry, LINE2)
    note(s, X0 + 24, ry + 20, CW - 48, "Busoga Tech Supplies has the best score and the lowest compliant price. Source "
         "Point ICT quoted less but offered a 1-year warranty against the 3 years required, so it was not scored. "
         "Nile Bridge Systems did not respond.", icon="award")
    return s


# ---------------------------------------------------------------- evaluation
def w13_evaluations():
    """Every evaluation, as Procurement, Finance, the Country Director and the auditor see them."""
    s = console("13 Evaluations", "Evaluations", ["Procurement", "Evaluations"], "ivan")
    y = page_head(s, "Evaluations", "Committee evaluations for procurements above UGX 30M. Members score alone; the "
                  "chair's report goes to the Country Director.")
    rows = [[c_ref("PR-2026-0090", "Washroom block, Busalamu P/S · RFQ-2026-0033"), c_person("esther", "Chair"),
             c_text("3 bids", INK2), c_text("2 of 3 submitted", INK, 600), c_status("Evaluation", "Scoring"),
             c_two("Tue 13 Oct", "due tomorrow", bold=False)],
            [c_ref("PR-2026-0089", "Printing teacher training manuals · RFQ-2026-0032"), c_person("moses", "Chair"),
             c_text("3 bids", INK2), c_text("3 of 3 · report sent", INK2), c_status("Award", "Award pending"),
             c_two("Thu 1 Oct", "with the Country Director", bold=False)],
            [c_ref("PR-2026-0087", "10 laptops for training room 2 · RFQ-2026-0031"), c_person("esther", "Chair"),
             c_text("3 bids", INK2), c_text("3 of 3 · awarded", INK2), c_status("Closed", "Awarded"),
             c_two("Thu 1 Oct", "awarded to Busoga Tech", bold=False)],
            [c_ref("PR-2026-0079", "Office chairs, Jinja head office · RFQ-2026-0027"), c_person("brian", "Chair"),
             c_text("3 bids", INK2), c_text("3 of 3 · awarded", INK2), c_status("Closed", "Awarded"),
             c_two("Wed 16 Sep", "awarded to Iganga Office Furnishers", bold=False)]]
    cols = [("Procurement", 470, "start"), ("Chair", 230, "start"), ("Bids", 110, "start"), ("Committee", 230, "start"),
            ("Status", 180, "start"), ("Report due", 292, "start")]
    list_card(s, y, 78 + 44 + 66 * len(rows) + 58)
    toolbar(s, X0, y, CW, "Search evaluations…", filters=["FY 2026"], export=False)
    end = data_table(s, X0, y + 78, cols, rows, links=[None, None, "w13d", None], row_h=66, hl=2)
    pager(s, X0, end, CW, (1, 4), 9, pages=3, per=4)
    note(s, X0, end + 76, CW, "Scores stay hidden from everyone, members included, until all members have submitted.",
         icon="eye")
    return s


def w13_mine():
    s = console("13 My evaluations (Esther)", "Evaluations", ["Procurement", "Evaluations"], "esther", owner=True)
    y = page_head(s, "My evaluations", "Evaluations you are appointed to. You see only these, and others' scores only "
                  "after everyone has submitted.")
    rows = [[c_ref("PR-2026-0090", "Washroom block, Busalamu P/S · RFQ-2026-0033"), c_chip("Chair", VIOLET),
             c_text("3 bids", INK2), c_status("To score", "To score: you"), c_text("2 of 3 submitted", INK, 600),
             c_two("Tue 13 Oct", "due tomorrow", bold=False)],
            [c_ref("PR-2026-0089", "Printing teacher training manuals · RFQ-2026-0032"), c_chip("Member", TEAL),
             c_text("3 bids", INK2), c_status("Scored", "Submitted 1 Oct"), c_text("3 of 3 · report sent", INK2),
             c_two("Thu 1 Oct", "award with the Country Director", bold=False)],
            [c_ref("PR-2026-0087", "10 laptops for training room 2 · RFQ-2026-0031"), c_chip("Chair", VIOLET),
             c_text("3 bids", INK2), c_status("Scored", "Submitted 30 Sep"), c_text("3 of 3 · awarded", INK2),
             c_two("Thu 1 Oct", "awarded to Busoga Tech", bold=False)],
            [c_ref("PR-2026-0079", "Office chairs, Jinja head office · RFQ-2026-0027"), c_chip("Member", TEAL),
             c_text("3 bids", INK2), c_status("Scored", "Submitted 16 Sep"), c_text("3 of 3 · awarded", INK2),
             c_two("Wed 16 Sep", "awarded to Iganga Office Furnishers", bold=False)]]
    cols = [("Procurement", 470, "start"), ("Your role", 140, "start"), ("Bids", 110, "start"), ("Your scores", 230, "start"),
            ("Committee", 240, "start"), ("Due", 322, "start")]
    list_card(s, y, 78 + 44 + 66 * len(rows) + 58)
    toolbar(s, X0, y, CW, "Search evaluations…", export=False)
    end = data_table(s, X0, y + 78, cols, rows, links=["w13b", None, "w13d", None], row_h=66, hl=0)
    pager(s, X0, end, CW, (1, 4), 4, pages=1)
    return s


w13_mine.key = "w13-esther"


def w13b_scoring():
    s = console("13b Committee scoring PR-2026-0090 (Esther)", "Evaluations",
                ["Procurement", "Evaluations", "PR-2026-0090"], "esther", owner=True)
    y = record_header(s, Y0, "PR-2026-0090", "Washroom block, Busalamu P/S",
                      chips=[("Evaluation", None, "status"), ("Construction & works", VIOLET, "chip")],
                      facts=[("RFQ", WASHROOM["rfq"]), ("Project", "Busalamu School Sanitation, Luuka"), ("Your role", "Chair"),
                             ("Due", "Tue 13 Oct")],
                      actions=[("Submit my scores", "primary", "send", "w13"), ("Save", "secondary", None, "w13")])
    y += 20
    lw = 1130
    # declaration
    s.rect(X0, y, lw, 66, fill=tint(BRAND_M, 0.08), rx=14, name="declaration")
    s.icon("shield", X0 + 22, y + 22, 22, BRAND_M, 2)
    s.text(X0 + 58, y + 30, "You declared no conflict of interest with any bidder", 14.5, 700, INK)
    s.text(X0 + 58, y + 50, "Signed Fri 9 Oct, 10:02 · scoring opened only after the declaration", 12.5, 400, MUTED)
    y += 86
    bids = WASHROOM["bids"]
    s.rect(X0, y, lw, 600, fill=CARD, rx=16, stroke=LINE, name="score sheet")
    s.text(X0 + 24, y + 40, "Score sheet", 17, 700, INK)
    s.text(X0 + 140, y + 40, "Technical scores are yours; the financial score is calculated from the prices", 13, 400, MUTED)
    lab_w = 380
    colw = (lw - 48 - lab_w) / 3
    tx = X0 + 24
    hy = y + 64
    for i, (name, price) in enumerate(bids):
        cx = tx + lab_w + i * colw
        s.rect(cx + 6, hy, colw - 12, 60, fill=FIELD_BG, rx=12)
        s.text(cx + 20, hy + 26, name, 14, 700, INK, maxw=colw - 40)
        s.text(cx + 20, hy + 46, f"UGX {_m(price)}", 12.5, 600, MUTED)
    crit = [("Experience in similar works", 20, [17, 15, 18]), ("Method and work plan", 20, [16, 14, 17]),
            ("Key staff", 15, [12, 11, 13]), ("Equipment", 15, [13, 12, 14])]
    ry = hy + 76
    s.text(tx + 4, ry + 4, "TECHNICAL · 70", 10.5, 700, MUTED, spacing=0.8)
    ry += 14
    for lab, mx, vals in crit:
        s.line(tx, ry, tx + lw - 48, ry, LINE2)
        s.text(tx + 4, ry + 32, lab, 14, 500, INK2)
        s.text(tx + lab_w - 20, ry + 32, f"of {mx}", 12.5, 500, FAINT, anchor="end")
        for i, v in enumerate(vals):
            cx = tx + lab_w + i * colw
            focus = (lab == "Equipment" and i == 2)
            s.rect(cx + 20, ry + 10, 96, 34, fill=CARD, rx=8, stroke=BRAND if focus else "#CFD9D2", sw=1.6 if focus else 1)
            s.text(cx + 36, ry + 32, str(v), 15, 600, INK)
        ry += 52
    techs = [sum(c[2][i] for c in crit) for i in range(3)]
    low = min(p for _, p in bids)
    fins = [30 * low / p for _, p in bids]
    for lab, vals, bold in [("Technical total", techs, False), ("Financial (lowest price scores 30)", fins, False),
                            ("Your total", [t + f for t, f in zip(techs, fins)], True)]:
        s.line(tx, ry, tx + lw - 48, ry, LINE2 if not bold else LINE)
        s.text(tx + 4, ry + 32, lab, 14, 700 if bold else 600, INK)
        for i, v in enumerate(vals):
            cx = tx + lab_w + i * colw
            s.text(cx + 20, ry + 32, f"{v:.1f}", 16 if bold else 14.5, 700, BRAND_D if bold else INK)
        ry += 50
    textarea(s, tx, ry + 6, lw - 48, 60, "Comment for the report",
             "Lake Basin has the strongest plan and staff but the highest price. Kakira's plan relies on one site manager.")
    # committee
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, Y0 + 148, rw, 400, fill=CARD, rx=16, stroke=LINE, name="committee")
    s.text(rx + 24, Y0 + 188, "Committee", 17, 700, INK)
    s.text(rx + 24, Y0 + 210, "Appointed by Joseph Waiswa on 5 Oct", 13, 400, MUTED)
    mem = [("esther", "Chair", "Scoring now", "To score"), ("brian", "Member", "Submitted Sun 11 Oct, 16:20", "Scored"),
           ("moses", "Member", "Submitted Sat 10 Oct, 11:05", "Scored")]
    my = Y0 + 240
    for who, role, sub, st in mem:
        name, ini, *_rest, col = PEOPLE[who]
        avatar(s, rx + 44, my + 20, 18, ini, col)
        s.text(rx + 72, my + 15, f"{name}" + (" (you)" if who == "esther" else ""), 14, 700, INK)
        s.text(rx + 72, my + 34, f"{role} · {sub}", 12.5, 400, MUTED, maxw=rw - 200)
        status_chip(s, rx + rw - 24, my + 8, st, anchor="end")
        my += 62
    note(s, rx + 24, my + 6, rw - 48, "Members' scores stay hidden from each other until all three are submitted; then "
         "the averages go into the evaluation report.", icon="eye")
    return s


def w13c_award():
    s = console("13c Approve award PR-2026-0089", "My approvals", ["My approvals", "PR-2026-0089 · award"], "samuel", owner=True)
    y = record_header(s, Y0, "PR-2026-0089", "Printing teacher training manuals",
                      chips=[("Award", None, "status"), ("Printing & stationery", TEAL, "chip")],
                      facts=[("Project", "Teacher ICT Initiative, Kamuli"), ("Line", "5120 Printing · reserved 31,200,000"),
                             ("Recommended by", "Joseph Waiswa · Sat 10 Oct")],
                      track=lambda s_, x, y_, w: file_track(s_, x, y_, w, "Award", waiting="Samuel Kato (you)",
                                                            since="2 days"))
    y += 20
    lw = 1090
    s.rect(X0, y, lw, 560, fill=CARD, rx=16, stroke=LINE, name="evaluation report")
    s.text(X0 + 24, y + 40, "Evaluation report", 17, 700, INK)
    s.text(X0 + 190, y + 40, "RFQ-2026-0032 · committee of 3 · 1 Oct · declarations signed", 13, 400, MUTED)
    rows = []
    for i, (name, price, score) in enumerate([("Jinja Print & Pack Ltd", 29_750_000, 91.0),
                                              ("Busoga Printers Ltd", 28_900_000, 86.5),
                                              ("Source Line Graphics", 32_400_000, 80.2)]):
        rows.append([c_text(name, INK, 700 if i == 0 else 500), c_money(price, bold=i == 0), c_text("14 days" if i else "10 days", INK2),
                     c_text(f"{score:.1f}", INK, 700), c_status("Recommended") if i == 0 else c_text(f"{['', 'Second', 'Third'][i]}", MUTED)])
    cols = [("Bidder", 330, "start"), ("Price (UGX)", 180, "end"), ("Delivery", 150, "start"), ("Score", 140, "start"),
            ("Result", 242, "start")]
    end = data_table(s, X0, y + 60, cols, rows, row_h=58, check=False, hl=0)
    yy = end + 24
    s.text(X0 + 24, yy + 10, "Recommendation", 13, 700, MUTED)
    s.para(X0 + 24, yy + 36, "Award to Jinja Print & Pack Ltd at UGX 29,750,000: the highest combined score. Busoga Printers "
           "was cheaper by UGX 850,000 but its sample binding failed the 200-page durability test.", lw - 48, 14.5, 400, INK2, lh=23)
    yy += 110
    for i, (lab, v, col) in enumerate([("Reserved on 5120 by the requisition", "31,200,000", INK),
                                       ("This award", "29,750,000", INK),
                                       ("Released back to the line on approval", "1,450,000", BRAND_M)]):
        s.text(X0 + 24, yy + i * 30, lab, 13.5, 500, INK2)
        s.text(X0 + lw - 24, yy + i * 30, v, 14, 700, col, anchor="end")
    decision_panel(s, X0 + lw + 20, y, CW - lw - 20, viewer="samuel", maker="joseph", what="award recommendation",
                    comment="Approved. Jinja Print & Pack's sample was the only one that passed.",
                    steps=[("Award approval", "Samuel Kato · Country Director", "now")], back="w02", approve="Approve award",
                    h=560)
    return s


def w13d_file_evaluation():
    s = console("13d File PR-2026-0087: Evaluation", "Evaluations", ["Requisitions", L["no"], "Evaluation"], "ivan")
    y = file_header(s, "Evaluation")
    lw = 1100
    s.rect(X0, y, lw, 650, fill=CARD, rx=16, stroke=LINE, name="scores")
    s.text(X0 + 24, y + 40, "Committee scores", 17, 700, INK)
    s.text(X0 + 196, y + 40, "technical out of 70 by each member, averaged; financial out of 30 from the price", 13, 400, MUTED)
    rows = [[c_text("Busoga Tech Supplies Ltd", INK, 700), c_text("60.0"), c_text("58.5"), c_text("59.0"), c_text("59.2", INK, 700),
             c_text("29.2", INK, 600), c_text("88.4", BRAND_D, 700)],
            [c_text("Kagulu Computers Ltd", INK, 500), c_text("57.0"), c_text("58.0"), c_text("57.5"), c_text("57.5", INK, 700),
             c_text("26.6", INK, 600), c_text("84.1", INK, 700)],
            [c_text("Source Point ICT Ltd", MUTED, 500), c_text("—", FAINT), c_text("—", FAINT), c_text("—", FAINT),
             c_text("Not scored", RED, 600), c_text("—", FAINT), c_text("Non-compliant", RED, 600)]]
    cols = [("Bidder", 310, "start"), ("Esther (chair)", 130, "start"), ("Brian", 110, "start"), ("Moses", 110, "start"),
            ("Technical", 140, "start"), ("Financial", 130, "start"), ("Total", 170, "start")]
    end = data_table(s, X0, y + 60, cols, rows, row_h=58, check=False, hl=0)
    yy = end + 30
    s.text(X0 + 24, yy, "DECLARATIONS", 10.5, 700, MUTED, spacing=0.8)
    yy += 18
    for i, who in enumerate(L["committee"]):
        name, ini, *_rest, col = PEOPLE[who]
        cx = X0 + 24 + i * 350
        s.rect(cx, yy, 334, 60, fill=FIELD_BG, rx=12)
        avatar(s, cx + 30, yy + 30, 16, ini, col)
        s.text(cx + 56, yy + 26, name, 14, 700, INK)
        s.text(cx + 56, yy + 45, "No conflict · signed 30 Sep", 12.5, 400, MUTED)
        s.icon("check", cx + 300, yy + 21, 18, BRAND_M, 2.6)
    yy += 90
    s.text(X0 + 24, yy, "Recommendation", 13, 700, MUTED)
    s.para(X0 + 24, yy + 26, "Award RFQ-2026-0031 to Busoga Tech Supplies Ltd at UGX 36,400,000: highest total score and lowest "
           "compliant price. Report signed by the chair on Thu 1 Oct.", lw - 48, 14.5, 400, INK2, lh=23)
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 290, fill=CARD, rx=16, stroke=LINE, name="award")
    s.text(rx + 24, y + 40, "Award", 17, 700, INK)
    s.text(rx + 24, y + 80, "Busoga Tech Supplies Ltd", 19, 700, INK, family="display")
    s.text(rx + 24, y + 104, "UGX 36,400,000 · 10 days delivery · 3-year warranty", 13, 500, INK2)
    s.line(rx + 24, y + 126, rx + rw - 24, y + 126, LINE2)
    avatar(s, rx + 42, y + 162, 17, "SK", AMBER_D)
    s.text(rx + 70, y + 157, "Approved by Samuel Kato", 14, 700, INK)
    s.text(rx + 70, y + 176, "Country Director · Mon 5 Oct, 09:20", 12.5, 400, MUTED)
    s.rect(rx + 24, y + 200, rw - 48, 60, fill=FIELD_BG, rx=10)
    s.para(rx + 38, y + 225, "“Approved: Busoga Tech Supplies, best score and within budget.”", rw - 76, 13, 500, INK2, lh=19)
    s.rect(rx, y + 310, rw, 60, fill=CARD, rx=14, stroke=LINE)
    s.icon("file", rx + 22, y + 330, 20, BRAND, 2)
    s.text(rx + 52, y + 346, "Evaluation report.pdf · 6 pages", 14, 600, INK)
    s.icon("download", rx + rw - 44, y + 330, 18, INK2, 2)
    return s


# ---------------------------------------------------------------- LPOs
LPOS = [
    ("LPO-2026-0051", "PR-2026-0087 · 10 laptops", "Busoga Tech Supplies Ltd", 36_400_000, "6 Oct", "Received 9 Oct", "Closed", "w14b"),
    ("LPO-2026-0050", "PR-2026-0086 · Accessible desks, Kasese", "Wairaka Woodworks Ltd", 21_350_000, "1 Oct", "Received 8 Oct", "Paid", None),
    ("LPO-2026-0049", "PR-2026-0084 · Stationery for vocational classes", "Main Street Stationers", 6_620_000, "2 Oct", "Due today", "Issued", None),
    ("LPO-2026-0048", "PR-2026-0082 · Motorcycle tyres and service", "Masese Motors & Spares", 2_450_000, "22 Sep", "Received 25 Sep", "Closed", None),
    ("LPO-2026-0047", "PR-2026-0079 · Office chairs, Jinja", "Iganga Office Furnishers", 7_300_000, "17 Sep", "Received 23 Sep", "Closed", None),
    ("LPO-2026-0046", "PR-2026-0078 · Screen-reader licences", "Source Point ICT Ltd", 3_100_000, "14 Sep", "Delivered 15 Sep", "Closed", None),
]


def w14_lpos():
    s = console("14 Purchase orders (LPOs)", "Purchase orders", ["Procurement", "Purchase orders"], "ivan")
    y = page_head(s, "Purchase orders", "Local purchase orders issued from approved awards. Each commits its budget line.")
    rows, links = [], []
    for no, file, sup, val, issued, deliv, st, tgt in LPOS:
        rows.append([c_ref(no, file), c_text(sup, INK, 600), c_money(val), c_text(issued, INK2),
                     c_text(deliv, AMBER_D if deliv == "Due today" else INK2, 600 if deliv == "Due today" else 400),
                     c_status(st)])
        links.append(tgt)
    cols = [("LPO", 440, "start"), ("Supplier", 330, "start"), ("Value (UGX)", 170, "end"), ("Issued", 140, "start"),
            ("Delivery", 220, "start"), ("Status", 212, "start")]
    list_card(s, y, 78 + 44 + 62 * len(rows) + 58)
    toolbar(s, X0, y, CW, "Search LPOs or suppliers…", filters=["FY 2026"])
    end = data_table(s, X0, y + 78, cols, rows, links=links, row_h=62, sort={"LPO", "Value (UGX)"}, hl=0)
    pager(s, X0, end, CW, (1, 6), 61, pages=11, per=6)
    return s


def w14b_lpo():
    s = console("14b File PR-2026-0087: LPO-2026-0051", "Purchase orders", ["Requisitions", L["no"], "LPO"], "ivan")
    y = file_header(s, "LPO")
    # the document
    dw = 1000
    dx = X0
    s.rect(dx, y, dw, 660, fill=FIELD_BG, rx=16, stroke=LINE, name="document viewer")
    px, pw = dx + 60, dw - 120
    s.rect(px, y + 24, pw, 612, fill=CARD, rx=4, stroke=LINE, shadow=True, name="A4 page")
    from kit import logo
    logo(s, px + 40, y + 54, 56)
    s.text(px + 110, y + 76, "International Development Institute Uganda", 15, 700, INK)
    s.text(px + 110, y + 96, "Plot 45 Wilson Avenue, Jinja · P.O. Box 1005, Jinja", 12, 400, MUTED)
    s.text(px + pw - 40, y + 76, "LOCAL PURCHASE ORDER", 15, 700, BRAND, anchor="end", spacing=0.6)
    ref(s, px + pw - 40, y + 98, L["lpo"], 14, INK, 600, anchor="end")
    s.line(px + 40, y + 124, px + pw - 40, y + 124, LINE)
    cw2 = (pw - 80) / 3
    blocks = [("Supplier", ["Busoga Tech Supplies Ltd", "Plot 9 Main Street, Jinja", "TIN 1003 4721 88"]),
              ("Deliver to", ["Kasese ICT Hub, training room 2", "Kasese field office", "By Fri 16 Oct 2026"]),
              ("Reference", ["PR-2026-0087 · RFQ-2026-0031", "Kasese ICT Hub · 5210", "Issued Tue 6 Oct 2026"])]
    for i, (lab, lines) in enumerate(blocks):
        bx = px + 40 + i * cw2
        s.text(bx, y + 152, lab.upper(), 10, 700, MUTED, spacing=0.8)
        for j, ln in enumerate(lines):
            s.text(bx, y + 174 + j * 19, ln, 12.5, 700 if j == 0 else 400, INK if j == 0 else INK2)
    ty = y + 250
    s.rect(px + 40, ty, pw - 80, 30, fill=FIELD_BG)
    for lab, xx, anc in [("ITEM", 12, "start"), ("QTY", 470, "start"), ("UNIT PRICE", 640, "end"), ("AMOUNT (UGX)", pw - 92, "end")]:
        s.text(px + 40 + xx, ty + 20, lab, 10, 700, MUTED, anchor=anc, spacing=0.6)
    s.para(px + 52, ty + 54, L["item"], 440, 12.5, 500, INK, lh=18)
    s.text(px + 510, ty + 54, "10", 12.5, 500, INK)
    s.text(px + 680, ty + 54, "3,084,746", 12.5, 500, INK, anchor="end")
    s.text(px + pw - 52, ty + 54, "30,847,458", 12.5, 600, INK, anchor="end")
    ty += 110
    for lab, v, bold in [("Subtotal", "30,847,458", False), ("VAT 18%", "5,552,542", False), ("Total", "36,400,000", True)]:
        s.text(px + pw - 220, ty, lab, 13 if bold else 12.5, 700 if bold else 500, INK if bold else INK2, anchor="end")
        s.text(px + pw - 52, ty, v, 14 if bold else 12.5, 700 if bold else 500, INK, anchor="end")
        ty += 24
    s.para(px + 52, ty + 16, "Terms: delivery within 10 days; payment 30 days after accepted delivery against this LPO, the "
           "goods received note and a tax invoice; 3-year warranty; screen readers installed.", pw - 104, 11.5, 400, MUTED, lh=17)
    sy = ty + 76
    for i, (who, role) in enumerate([("Joseph Waiswa", "Prepared"), ("Ruth Nakato", "Commitment checked"),
                                     ("Samuel Kato", "Authorised")]):
        sx = px + 40 + i * cw2
        s.path(f"M{sx + 6:.1f} {sy + 18:.1f} c 14 -18 22 8 34 -6 s 16 10 30 -4", stroke=BRAND_D, sw=1.6)
        s.line(sx, sy + 28, sx + cw2 - 30, sy + 28, LINE)
        s.text(sx, sy + 46, who, 12, 700, INK)
        s.text(sx, sy + 62, role, 11, 500, MUTED)
    # side
    rx, rw = X0 + dw + 20, CW - dw - 20
    s.rect(rx, y, rw, 452, fill=CARD, rx=16, stroke=LINE, name="lpo details")
    ref(s, rx + 24, y + 40, L["lpo"], 15, BRAND, 600)
    status_chip(s, rx + rw - 24, y + 22, "Closed", anchor="end")
    facts = [("Supplier", "Busoga Tech Supplies Ltd"), ("Value", "UGX 36,400,000"), ("Issued", "Tue 6 Oct, 11:30 · by email + portal"),
             ("Acknowledged", "Tue 6 Oct, 14:02 · supplier portal"), ("Deliver by", "Fri 16 Oct · delivered 9 Oct"),
             ("Budget line", "5210 ICT equipment · paid")]
    fy = y + 80
    for lab, v in facts:
        s.text(rx + 24, fy, lab, 12.5, 500, MUTED)
        s.text(rx + 24, fy + 20, v, 14, 600, INK, maxw=rw - 48)
        fy += 50
    button(s, rx + 24, y + 452 - 66, "Download PDF", "primary", icon="download", w=(rw - 60) / 2, h=42)
    button(s, rx + 36 + (rw - 60) / 2, y + 452 - 66, "Print", "secondary", icon="printer", w=(rw - 60) / 2, h=42)
    note(s, rx, y + 472, rw, "The LPO is generated from the approved award: nobody retypes prices, and it carries the "
         "three approvals as signatures.", icon="stamp")
    return s


# ---------------------------------------------------------------- deliveries
DELIVERIES = [
    ("LPO-2026-0049", "PR-2026-0084 · Stationery", "Main Street Stationers", "Mayuge field office", "Today", "—", "Due today", "w15b"),
    ("LPO-2026-0045", "PR-2026-0081 · Hygiene kits batch 1", "Jinja Office Mart", "Kumi field office", "Thu 15 Oct", "—", "Issued", None),
    ("LPO-2026-0051", "PR-2026-0087 · 10 laptops", "Busoga Tech Supplies Ltd", "Kasese field office", "Fri 16 Oct", "GRN-2026-0064 · 10 of 10", "Accepted", "w15d"),
    ("LPO-2026-0050", "PR-2026-0086 · Accessible desks", "Wairaka Woodworks Ltd", "Kasese field office", "Fri 9 Oct", "GRN-2026-0063 · 24 of 24", "Accepted", None),
    ("LPO-2026-0048", "PR-2026-0082 · Motorcycle tyres", "Masese Motors & Spares", "Jinja head office", "Fri 25 Sep", "GRN-2026-0061 · 8 of 8", "Accepted", None),
]


def w15_deliveries():
    s = console("15 Deliveries", "Deliveries", ["Procurement", "Deliveries"], "ivan")
    y = page_head(s, "Deliveries", "Goods and services expected against issued LPOs. Record what arrived and what was accepted.")
    rows, links = [], []
    for no, file, sup, to, due, grn, st, tgt in DELIVERIES:
        rows.append([c_ref(no, file), c_text(sup, INK, 600), c_text(to, INK2),
                     c_text(due, AMBER_D if due == "Today" else INK2, 700 if due == "Today" else 400),
                     c_text(grn, INK2 if grn != "—" else FAINT), c_status(st)])
        links.append(tgt)
    cols = [("LPO", 380, "start"), ("Supplier", 280, "start"), ("Deliver to", 230, "start"), ("Due", 150, "start"),
            ("Goods received", 270, "start"), ("Status", 202, "start")]
    list_card(s, y, 58 + 78 + 44 + 64 * len(rows) + 58)
    tabs(s, X0 + 24, y + 14, [("Expected", 2), ("Received", 3)], "Expected")
    toolbar(s, X0, y + 50, CW, "Search LPOs or suppliers…", export=False)
    end = data_table(s, X0, y + 128, cols, rows, links=links, row_h=64, hl=links.index("w15d"))
    pager(s, X0, end, CW, (1, 5), 5, pages=1)
    return s


def w15b_grn():
    s = console("15b Goods received & inspection LPO-2026-0049 (Peter)", "Deliveries",
                ["Procurement", "Deliveries", "LPO-2026-0049"], "peter", owner=True)
    y = page_head(s, "Goods received & inspection", None,
                  actions=[("Save goods received note", "primary", "check", "w15"), ("Save draft", "secondary", None, "w15")],
                  ref_line=(STATIONERY["lpo"], "Main Street Stationers · Stationery for vocational classes (PR-2026-0084) · Mayuge"))
    lw = 1130
    s.rect(X0, y, lw, 760, fill=CARD, rx=16, stroke=LINE, name="grn form")
    x, w = X0 + 28, lw - 56
    tw3 = (w - 48) / 3
    field(s, x, y + 24, tw3, "Supplier's delivery note", "MSS-DN-2207", required=True, mono=True)
    field(s, x + tw3 + 24, y + 24, tw3, "Received", "Mon 12 Oct 2026, 10:15", required=True, icon="calendar")
    field(s, x + 2 * (tw3 + 24), y + 24, tw3, "Received at", "Mayuge field office", required=True, icon="pin", dropdown=True)
    yy = y + 118
    s.text(x, yy + 10, "What arrived", 17, 700, INK)
    yy += 26
    rows = []
    for item, unit, ordered, recd, acc in STATIONERY["lines"]:
        rej = recd - acc
        out = ordered - recd
        rows.append([c_text(item, INK, 600), c_text(unit, INK2), c_text(str(ordered)), _input_cell(recd, recd != ordered),
                     _input_cell(acc, False), c_text(str(rej) if rej else "—", RED if rej else FAINT, 700 if rej else 400),
                     c_text(("Torn covers" if rej else (f"{out} outstanding" if out else "—")),
                            RED if rej else (AMBER_D if out else FAINT), 600 if (rej or out) else 400)])
    cols = [("Item", 290, "start"), ("Unit", 90, "start"), ("Ordered", 100, "start"), ("Received", 130, "start"),
            ("Accepted", 130, "start"), ("Rejected", 100, "start"), ("Note", 234, "start")]
    end = data_table(s, x, yy, cols, rows, row_h=60, check=False)
    yy = end + 24
    s.text(x, yy + 10, "Photos", 13, 600, INK2)
    for i, lab in enumerate(["Cartons on arrival", "Torn flip chart covers", "Delivery note"]):
        px = x + i * 180
        s.rect(px, yy + 24, 166, 110, fill=["#DCE6D9", "#E9DCCB", "#E4E8EE"][i], rx=10)
        s.icon(["package", "alert", "file"][i], px + 70, yy + 56, 26, INK2, 1.8)
        s.text(px + 10, yy + 154, lab, 12, 500, MUTED)
    s.rect(x + 3 * 180, yy + 24, 166, 110, fill=CARD, rx=10, stroke="#CFD9D2", dash="5 4")
    s.icon("camera", x + 3 * 180 + 70, yy + 56, 26, BRAND, 1.8)
    s.text(x + 3 * 180 + 83, yy + 110, "Add photo", 12.5, 600, BRAND, anchor="middle")
    yy += 186
    textarea(s, x, yy, w, 70, "Inspection notes",
             "2 flip chart pads rejected (torn covers); supplier will replace them. 12 boxes of thread to follow by Fri 16 Oct.")
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 330, fill=CARD, rx=16, stroke=LINE, name="result")
    s.text(rx + 24, y + 40, "Result", 17, 700, INK)
    status_chip(s, rx + 24, y + 58, "Partly delivered")
    for i, (lab, v, col) in enumerate([("Lines fully accepted", "2 of 4", INK), ("Rejected", "2 flip chart pads", RED),
                                       ("Outstanding", "12 boxes of thread", AMBER_D), ("Value accepted", "UGX 5,912,000", INK)]):
        ly = y + 118 + i * 44
        s.text(rx + 24, ly, lab, 13.5, 500, INK2)
        s.text(rx + rw - 24, ly, v, 14, 700, col, anchor="end")
    s.rect(rx, y + 350, rw, 210, fill=CARD, rx=16, stroke=LINE, name="inspection team")
    s.text(rx + 24, y + 390, "Inspection team", 17, 700, INK)
    for i, (who, sub) in enumerate([("peter", "Inspection Officer · recording"), ("harriet", "Requesting Officer · Programmes")]):
        name, ini, *_rest, col = PEOPLE[who]
        avatar(s, rx + 44, y + 432 + i * 58, 17, ini, col)
        s.text(rx + 70, y + 428 + i * 58, name, 14, 700, INK)
        s.text(rx + 70, y + 447 + i * 58, sub, 12.5, 400, MUTED, maxw=rw - 100)
    note(s, rx, y + 580, rw, "Finance can only match the invoice to accepted quantities; the outstanding thread stays open "
         "on the LPO.", icon="receipt")
    return s


def _input_cell(v, warn):
    def f(s_, x, y, w, h):
        s_.rect(x + 14, y + h / 2 - 18, w - 34, 36, fill=CARD, rx=8, stroke=AMBER_D if warn else "#CFD9D2",
                sw=1.6 if warn else 1)
        s_.text(x + 28, y + h / 2 + 5, str(v), 14, 600, INK)
    return f


def w15c_payment():
    s = console("15c File PR-2026-0087: Payment & close-out", "Requisitions", ["Requisitions", L["no"], "Payment"], "ivan")
    y = file_header(s, "Payment")
    lw = 1010
    s.rect(X0, y, lw, 330, fill=CARD, rx=16, stroke=LINE, name="three way match")
    s.text(X0 + 24, y + 40, "Three-way match", 17, 700, INK)
    s.text(X0 + 190, y + 40, "the invoice was checked against what was ordered and what was accepted", 13, 400, MUTED)
    colw = (lw - 48 - 2 * 40) / 3
    docs = [("Ordered", L["lpo"], "10 laptops × 3,640,000", "36,400,000", "Tue 6 Oct"),
            ("Accepted", L["grn"], "10 received · 10 accepted", "10 of 10", "Fri 9 Oct"),
            ("Invoiced", L["invoice"], "10 laptops × 3,640,000", "36,400,000", "Mon 12 Oct")]
    for i, (lab, code, sub, val, on) in enumerate(docs):
        cx = X0 + 24 + i * (colw + 40)
        s.rect(cx, y + 64, colw, 170, fill=FIELD_BG, rx=14)
        s.text(cx + 20, y + 94, lab.upper(), 10.5, 700, MUTED, spacing=0.8)
        ref(s, cx + 20, y + 120, code, 14, BRAND, 600)
        s.text(cx + 20, y + 162, val, 22, 700, INK, family="display")
        s.text(cx + 20, y + 186, sub, 12.5, 500, INK2)
        s.text(cx + 20, y + 212, on, 12.5, 400, MUTED)
        if i < 2:
            s.circle(cx + colw + 20, y + 149, 14, fill=tint(BRAND_M, 0.15))
            s.text(cx + colw + 20, y + 155, "=", 17, 700, BRAND_M, anchor="middle")
    s.rect(X0 + 24, y + 254, lw - 48, 52, fill=tint(BRAND_M, 0.1), rx=12)
    s.icon("check", X0 + 40, y + 270, 20, BRAND_M, 2.8)
    s.text(X0 + 70, y + 286, "Match: quantities and prices agree, so the invoice could be paid in full", 14, 700, BRAND_D)
    y2 = y + 350
    s.rect(X0, y2, lw, 300, fill=CARD, rx=16, stroke=LINE, name="payment")
    s.text(X0 + 24, y2 + 40, "Payment", 17, 700, INK)
    s.text(X0 + 112, y2 + 40, "recorded by Finance from the accounting system; this system does not pay", 13, 400, MUTED)
    hw = (lw - 48 - 24) / 2
    field(s, X0 + 24, y2 + 60, hw, "Payment reference", L["payment_ref"], mono=True, readonly=True, icon="hash")
    field(s, X0 + 48 + hw, y2 + 60, hw, "Paid on", "Mon 12 Oct 2026", readonly=True, icon="calendar")
    field(s, X0 + 24, y2 + 140, hw, "Paid from", L["bank"], readonly=True, icon="landmark")
    field(s, X0 + 48 + hw, y2 + 140, hw, "Payment voucher", L["voucher"], mono=True, readonly=True, icon="receipt")
    avatar(s, X0 + 42, y2 + 254, 16, "RN", TEAL)
    s.text(X0 + 66, y2 + 259, "Recorded by Ruth Nakato · Mon 12 Oct, 09:38", 13.5, 600, INK2)
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 330, fill=CARD, rx=16, stroke=LINE, name="close out")
    s.text(rx + 24, y + 40, "Close-out", 17, 700, INK)
    checks = ["Requisition and approvals", "RFQ and 3 quotations", "Evaluation report and award", "Signed LPO",
              "Goods received note and photos", "Invoice and payment reference"]
    cy = y + 74
    for c in checks:
        s.icon("check", rx + 24, cy - 12, 16, BRAND_M, 2.8)
        s.text(rx + 50, cy, c, 13.5, 500, INK2)
        cy += 34
    s.rect(rx, y + 350, rw, 120, fill=LIME, rx=16, name="closed")
    s.text(rx + 24, y + 392, "File closed", 19, 700, LIME_D, family="display")
    s.text(rx + 24, y + 416, "by Joseph Waiswa · Mon 12 Oct, 09:41", 13, 600, LIME_D)
    s.text(rx + 24, y + 440, "Nothing on this file can change now.", 13, 500, LIME_D)
    note(s, rx, y + 490, rw, "Export for accounting: the commitment, the payment and its account code (1520-10) go to "
         "Finance's monthly export.", icon="sheet")
    return s


def w15d_delivery():
    s = console("15d File PR-2026-0087: Delivery", "Deliveries", ["Requisitions", L["no"], "Delivery"], "ivan")
    y = file_header(s, "Delivery")
    lw = 1010
    s.rect(X0, y, lw, 650, fill=CARD, rx=16, stroke=LINE, name="grn")
    s.text(X0 + 24, y + 40, "Goods received note", 17, 700, INK)
    ref(s, X0 + 230, y + 40, L["grn"], 13, BRAND)
    status_chip(s, X0 + lw - 24, y + 20, "Accepted", anchor="end")
    tiles = [("Delivered", "Fri 9 Oct, 14:15"), ("Delivery note", L["dn"]), ("Received at", "Kasese ICT Hub, room 2"),
             ("Recorded by", "Peter Mukasa · 14:42")]
    tw4 = (lw - 48) / 4
    for i, (lab, v) in enumerate(tiles):
        _tile(s, X0 + 24 + i * tw4, y + 82, tw4, lab, v, "", mono=v.startswith("DN-"))
    rows = [[c_two("Laptop, Core i5, 16 GB, 512 GB SSD, 14\"", "Serials BTS-L5G-20871 to 20880"), c_text("10"),
             c_text("10"), c_text("10", BRAND_M, 700), c_text("—", FAINT)]]
    cols = [("Item", 520, "start"), ("Ordered", 110, "start"), ("Received", 110, "start"), ("Accepted", 110, "start"),
            ("Rejected", 112, "start")]
    end = data_table(s, X0, y + 150, cols, rows, row_h=64, check=False)
    yy = end + 26
    s.text(X0 + 24, yy, "INSPECTION", 10.5, 700, MUTED, spacing=0.8)
    s.para(X0 + 24, yy + 26, "All 10 powered on, Windows 11 Pro activated, NVDA screen reader installed and tested by Brian "
           "Ouma (ICT). Packaging intact. Accepted in full.", lw - 48, 14, 400, INK2, lh=22)
    yy += 84
    s.text(X0 + 24, yy, "PHOTOS", 10.5, 700, MUTED, spacing=0.8)
    for i, lab in enumerate(["Sealed cartons", "Serial labels", "Screen-reader test", "Delivery note"]):
        px = X0 + 24 + i * 236
        s.rect(px, yy + 16, 222, 130, fill=["#DCE6D9", "#E4E8EE", "#DDE4F2", "#ECE6DA"][i], rx=10)
        s.icon(["package", "hash", "eye", "file"][i], px + 98, yy + 66, 26, INK2, 1.8)
        s.text(px + 6, yy + 166, lab, 12.5, 500, MUTED)
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 250, fill=CARD, rx=16, stroke=LINE, name="inspected by")
    s.text(rx + 24, y + 40, "Inspected by", 17, 700, INK)
    for i, (who, sub) in enumerate([("brian", "ICT · technical check"), ("grace", "User department · Programmes"),
                                    ("peter", "Stores · recorded the GRN")]):
        name, ini, *_rest, col = PEOPLE[who]
        avatar(s, rx + 44, y + 86 + i * 52, 17, ini, col)
        s.text(rx + 70, y + 82 + i * 52, name, 14, 700, INK)
        s.text(rx + 70, y + 101 + i * 52, sub, 12.5, 400, MUTED)
    s.rect(rx, y + 270, rw, 130, fill=CARD, rx=16, stroke=LINE, name="against lpo")
    s.text(rx + 24, y + 308, "Against the LPO", 17, 700, INK)
    s.text(rx + 24, y + 340, "On time: due Fri 16 Oct, delivered Fri 9 Oct", 13.5, 600, BRAND_M)
    s.text(rx + 24, y + 364, "Nothing outstanding · nothing rejected", 13.5, 500, INK2)
    return s


SCREENS = [w13_mine, w10_requisitions, w10b_new_requisition, w10c_new_requisition, w11_file, w11b_approvals, w11c_documents, w12_rfqs, w12b_new_rfq,
           w12c_comparison, w13_evaluations, w13b_scoring, w13c_award, w13d_file_evaluation, w14_lpos, w14b_lpo,
           w15_deliveries, w15b_grn, w15c_payment, w15d_delivery]
