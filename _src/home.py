"""The dashboard and the approvers' inboxes (w01–w03b). Sign in (w00) is in public.py, the front door.

w01-<person>  each person's own dashboard: what is waiting on them, figures from what their role can open
w02  my approvals (Samuel, Country Director) → w02b approve requisition PR-2026-0096
w02-ruth, w02-ivan  my approvals with nothing waiting
w03  my approvals (Daniel, Department Head) → w03b approve requisition PR-2026-0095 (step 1 of 2)
"""
from __future__ import annotations

from charts import budget_bar, column_chart, file_track, hbars
from charts import mini_track
from data import (BUDGETS, FILES, FY_SPEND_BY_MONTH, INBOX, JOB, PEOPLE, PROJECT, SESSIONS, STAGE_COUNTS, TODAY_LONG,
                  VALUE_BY_CATEGORY, YOUR_TURN, dashboard_key, menu_for)
from procurement import DELIVERIES
from kit import (AMBER_D, BLUE, BRAND, BRAND_D, BRAND_M, CARD, FAINT, FIELD_BG, INK, INK2, KOICA, LIME, LIME_D, LINE,
                 LINE2, MUTED, ORANGE, RED, TEAL, VIOLET, ref, status_chip, tint, tw)
from shell import (approval_panel, CW, X0, Y0, c_chip, c_money, c_person, c_ref, c_status, c_text, c_two, console, data_table, decision_panel, list_card,
                   note, page_head, record_header, stat_card, tabs)

def _m(n):
    return f"{n:,.0f}"


FIRST = {p: PEOPLE[p][0].split()[0] for p in PEOPLE}

# Four figures per person, from what their role can open: (icon, colour, label, value, sub or sub_parts, target)
_OPEN = ("folder", BRAND, "Open files", "21", [("2", AMBER_D), (" awaiting approval · ", MUTED), ("1", ORANGE), (" returned", MUTED)], "w10")
_LPOS = ("receipt", TEAL, "LPOs this month", "6", "UGX 74.9M committed since 1 Oct", "w14")
_CYCLE = ("clock", AMBER_D, "Requisition → LPO", "19 days", [("7 days faster", BRAND_M), (" than FY 2025", MUTED)], None)
_DOCS = ("alert", RED, "Supplier documents", "4", [("1 expired", RED), (" · 3 expire within 30 days", MUTED)], "w20")
_BUDGET = ("wallet", BRAND_M, "Budget available", "UGX 364.9M", "36% of FY 2026 budgets left", "w30")
STATS = {
    "ivan": [("users", BLUE, "Users", "34", [("32", BRAND_M), (" active · ", MUTED), ("2", MUTED), (" inactive", MUTED)], "w60"),
             ("history", INK2, "Audit entries today", "38", [("1", RED), (" failed sign-in", MUTED)], "w63"), _OPEN, _DOCS],
    "joseph": [_OPEN, _LPOS, _CYCLE, _DOCS],
    "samuel": [("inbox", AMBER_D, "Waiting on you", "4", "Oldest: Mpumudde, 2 days", "w02"), _OPEN, _BUDGET, _CYCLE],
    "daniel": [("inbox", AMBER_D, "Waiting on you", "1", "Hygiene kits, 4 hours", "w03"),
               ("clipboard", BLUE, "Programmes requisitions", "9 open", "58 approved by you this year", "w10"),
               ("wallet", BRAND_M, "Programmes budgets", "61% used", "4 projects · FY 2026", "w41"), _CYCLE],
    "ruth": [("edit", TEAL, "Drafts", "2", "FY 2027 budgets in preparation", "w30"), _BUDGET,
             ("swap", AMBER_D, "Revisions waiting", "1", "BR-2026-0007 · 3 days", "w31"), _LPOS],
    "grace": [("clipboard", BLUE, "My requisitions", "4", [("1", MUTED), (" draft · ", MUTED), ("1", AMBER_D), (" awaiting approval", MUTED)], "w10"),
              ("check", BRAND_M, "Delivered to you", "1", "10 laptops · 9 Oct", "w11"),
              ("clock", AMBER_D, "Waiting longest", "1 day", "PR-2026-0096 with Samuel Kato", None),
              ("x", RED, "Rejected this year", "1", "PR-2026-0077 · covered by KOICA", None)],
    "esther": [("scale", VIOLET, "To score", "1", "PR-2026-0090 · due tomorrow", "w13-esther"),
               ("award", BRAND_M, "Evaluations this year", "4", "Chair of 2", "w13-esther"),
               ("shield", BRAND, "Declarations signed", "4", "No conflict of interest declared", "w13-esther"),
               ("clock", AMBER_D, "Time to score", "2.5 days", "on average, from bids opened", None)],
    "peter": [("truck", AMBER_D, "Due today", "1", "LPO-2026-0049 · Mayuge", "w15"),
              ("package", TEAL, "Expected this week", "2", "Stationery · hygiene kits", "w15"),
              ("receipt", BRAND, "LPOs this month", "6", "4 delivered · 2 to come", "w14"),
              ("check", BRAND_M, "Accepted in full", "11 of 12", "GRNs since 1 Sep", None)],
    "agnes": [("history", INK2, "Audit entries today", "38", [("1", RED), (" failed sign-in", MUTED)], "w63"), _OPEN,
              ("swap", TEAL, "Budget revisions", "5", "FY 2026 · 1 pending", "w31"), _DOCS],
}
# The lower half: the organisation's picture for office roles, the person's own rows for the rest
PERSONAL = {"grace", "esther", "peter"}


def _dashboard(person):
    name, ini, role, *_rest = PEOPLE[person]
    s = console(f"01 Dashboard: {name} ({role})", "Dashboard", ["Dashboard"], person, owner=True)
    s.text(X0, Y0 + 34, f"Good morning, {FIRST[person]}", 30, 700, INK, family="display")
    s.text(X0, Y0 + 62, f"{TODAY_LONG} · FY 2026, week 42 · {JOB[person]}", 14.5, 400, MUTED)
    y = Y0 + 90
    turns = YOUR_TURN[person]
    s.text(X0, y + 6, "YOUR TURN", 11, 700, LIME_D, spacing=1.0)
    s.text(X0 + 90, y + 6, f"{sum(1 for t in turns if t[4])} things are waiting on you", 13, 500, MUTED)
    y += 20
    tw3 = (CW - 40) / 3
    for i, (ic, title, code, sub, tgt) in enumerate(turns):
        tx = X0 + i * (tw3 + 20)
        s.rect(tx, y, tw3, 96, fill=CARD, rx=16, stroke=LINE)
        s.rect(tx, y, 6, 96, fill="#8CC152" if tgt else FAINT, rx=3)
        s.rect(tx + 22, y + 22, 44, 44, fill=LIME if tgt else LINE2, rx=12)
        s.icon(ic, tx + 33, y + 33, 22, LIME_D if tgt else INK2, 2)
        s.text(tx + 82, y + 38, title, 15.5, 700, INK, maxw=tw3 - 130)
        if code[:2] in ("PR", "RF", "LP", "BR", "BU", "SU"):
            ref(s, tx + 82, y + 60, code, 12.5, BRAND, 600)
        else:
            s.text(tx + 82, y + 60, code, 12.5, 700, BRAND)
        s.text(tx + 82, y + 80, sub, 12.5, 400, MUTED, maxw=tw3 - 130)
        if tgt:
            s.icon("chevright", tx + tw3 - 38, y + 37, 20, FAINT)
            s.link(tx, y, tw3, 96, tgt)
    y += 116
    gw = (CW - 60) / 4
    for i, (ic, col, lab, val, sub, tgt) in enumerate(STATS[person]):
        kw = {"sub_parts": sub} if isinstance(sub, list) else {"sub": sub}
        stat_card(s, X0 + i * (gw + 20), y, gw, 128, ic, col, lab, val, value_size=30, target=tgt, **kw)
    y += 148
    if person in PERSONAL:
        _personal_rows(s, person, y)
    else:
        _office_panels(s, person, y)
    return s


def _office_panels(s, person, y):
    allowed = set(menu_for(person))
    lw = 1010
    s.rect(X0, y, lw, 280, fill=CARD, rx=16, stroke=LINE, name="files by stage")
    s.text(X0 + 24, y + 38, "Open files by stage", 17, 700, INK)
    s.text(X0 + 214, y + 38, "where the 21 open procurement files are today", 13, 400, MUTED)
    s.text(X0 + lw - 24, y + 38, "All requisitions →", 13, 700, BRAND, anchor="end")
    s.link(X0 + lw - 160, y + 20, 140, 28, "w10")
    n = len(STAGE_COUNTS)
    colw = (lw - 48) / n
    mx = max(c for _, c in STAGE_COUNTS)
    for i, (st, c) in enumerate(STAGE_COUNTS):
        cx = X0 + 24 + i * colw
        bh = 120 * c / mx
        s.rect(cx + 14, y + 210 - bh, colw - 28, bh, fill=tint(BRAND_M, 0.35), rx=8)
        s.text(cx + colw / 2, y + 200 - bh, str(c), 20, 700, INK, anchor="middle", family="display")
        s.text(cx + colw / 2, y + 236, st, 12.5, 600, INK2, anchor="middle")
        if i < n - 1:
            s.icon("chevright", cx + colw - 8, y + 224, 14, FAINT, 2)
    rx, rw = X0 + lw + 20, CW - lw - 20
    if "Supplier register" in allowed:
        s.rect(rx, y, rw, 280, fill=CARD, rx=16, stroke=LINE, name="expiring documents")
        s.text(rx + 24, y + 38, "Supplier documents", 17, 700, INK)
        s.text(rx + rw - 24, y + 38, "Register →", 13, 700, BRAND, anchor="end")
        s.link(rx + rw - 110, y + 20, 90, 28, "w20")
        docs = [("Nile Bridge Systems Ltd", "URA tax clearance expired 30 Sep", "Expired"),
                ("Nile Bridge Systems Ltd", "Trading licence expires 31 Oct", "Expiring"),
                ("Source Point ICT Ltd", "NSSF clearance expires 6 Nov", "Expiring"),
                ("SunPower Busoga Ltd", "Suspended: tax clearance not renewed", "Suspended")]
        dy = y + 64
        for nm, sub, st in docs:
            s.line(rx + 24, dy, rx + rw - 24, dy, LINE2)
            s.text(rx + 24, dy + 26, nm, 13.5, 700, INK)
            s.text(rx + 24, dy + 45, sub, 12.5, 400, MUTED)
            status_chip(s, rx + rw - 24, dy + 18, st, anchor="end")
            dy += 52
    else:
        s.rect(rx, y, rw, 280, fill=CARD, rx=16, stroke=LINE, name="budgets by project")
        s.text(rx + 24, y + 38, "Budget used by project", 17, 700, INK)
        rows = [(PROJECT[b[1]][1].split(",")[0], (b[4] + b[5] + b[6]) / b[3] * 100, BRAND_M) for b in BUDGETS[:5]]
        hbars(s, rx + 24, y + 64, rw - 48, rows, row_h=38, label_w=210, fmt=lambda v: f"{v:.0f}%")
    y += 300
    s.rect(X0, y, lw, 1060 - y, fill=CARD, rx=16, stroke=LINE, name="committed by month")
    s.text(X0 + 24, y + 38, "Committed each month", 17, 700, INK)
    s.text(X0 + 240, y + 38, "LPOs issued, UGX millions, FY 2026", 13, 400, MUTED)
    column_chart(s, X0 + 24, y + 62, lw - 48, 1060 - y - 110, FY_SPEND_BY_MONTH,
                 ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"], hl=9, unit="M", y_step=20, y_max=80)
    s.rect(rx, y, rw, 1060 - y, fill=CARD, rx=16, stroke=LINE, name="by category")
    s.text(rx + 24, y + 38, "LPO value by category", 17, 700, INK)
    hbars(s, rx + 24, y + 60, rw - 48, VALUE_BY_CATEGORY[:5], row_h=30, label_w=200)


def _personal_rows(s, person, y):
    """Requesting officers, committee members and stores see their own rows, not the organisation's figures."""
    if person == "esther":
        title, sub = "My evaluations", "the committees you are appointed to, and where each one is"
        evals = [("PR-2026-0090", "Washroom block, Busalamu P/S", "Chair", "To score", "Due tomorrow", "w13b"),
                 ("PR-2026-0089", "Printing teacher training manuals", "Member", "Scored", "Award with the Executive Approver",
                  "w13e"),
                 ("PR-2026-0087", "10 laptops for training room 2", "Chair", "Scored", "Awarded to Busoga Tech", "w13d"),
                 ("PR-2026-0079", "Office chairs, Jinja head office", "Member", "Scored", "Awarded to Iganga Office Furnishers",
                  None)]
        rows = [[c_ref(no, what), c_chip(part, VIOLET if part == "Chair" else TEAL), c_status(st),
                 c_text(where, AMBER_D if st == "To score" else INK2, 700 if st == "To score" else 400)]
                for no, what, part, st, where, _ in evals]
        links = [e[5] for e in evals]
        cols = [("Procurement", 560, "start"), ("Your part", 200, "start"), ("Your scores", 260, "start"),
                ("Where it is", 544, "start")]
    elif person == "peter":
        title, sub = "Deliveries", "expected and received against issued LPOs"
        rows, links = [], []
        for no, file, sup, to, due, grn, st, tgt in DELIVERIES:
            rows.append([c_ref(no, file), c_text(sup, INK, 600), c_text(to, INK2),
                         c_text(due, AMBER_D if due == "Today" else INK2, 700 if due == "Today" else 400), c_status(st)])
            links.append(tgt)
        cols = [("LPO", 460, "start"), ("Supplier", 340, "start"), ("Deliver to", 300, "start"), ("Due", 220, "start"),
                ("Status", 244, "start")]
    else:
        mine = [f for f in FILES if f[5] == person]
        title = "My requisitions"
        sub = f"{len(mine)} this year · each one is a procurement file you can follow to the end"
        targets = {"PR-2026-0087": "w11", "PR-2026-0098": "w10b", "PR-2026-0096": "w10d"}
        rows, links = [], []
        for no, ttl, proj, office, acc, req, val, stage, st, waiting, since, method in mine:
            rows.append([c_ref(no, ttl), c_text(PROJECT[proj][1], INK2), c_money(val),
                         _stage(stage, st), c_text(waiting if waiting != "—" else "Nobody: done", INK2)])
            links.append(targets.get(no))
        cols = [("File", 420, "start"), ("Project", 360, "start"), ("Value (UGX)", 180, "end"), ("Stage", 230, "start"),
                ("Waiting on", 374, "start")]
    s.rect(X0, y, CW, 1060 - y, fill=CARD, rx=16, stroke=LINE, name="my rows")
    s.text(X0 + 24, y + 40, title, 17, 700, INK)
    s.text(X0 + 24 + tw(title, 17, 700) + 12, y + 40, sub, 13, 400, MUTED)
    data_table(s, X0, y + 60, cols, rows, links=links, row_h=62, check=False)


def _stage(stage, status):
    def f(s_, x, y, w, h):
        mini_track(s_, x + 16, y + h / 2 - 13, stage, 126, status)
        s_.text(x + 16, y + h / 2 + 15, status, 12.5, 700, INK2)
    return f


def _person_screen(key, build, person):
    """A screen that is one person's own: its key carries their name (w01-ruth)."""
    def f():
        return build(person)
    f.__name__ = key.replace("-", "_")
    f.key = key
    return f


DASHBOARDS = [_person_screen(dashboard_key(p), _dashboard, p) for p in SESSIONS]


# ---------------------------------------------------------------- approvals
def _waiting(since, reminded=False):
    def f(s_, x, y, w, h):
        late = since.endswith("days") and int(since.split()[0]) >= 2
        s_.text(x + 16, y + h / 2 - 3 if reminded else y + h / 2 + 5, since, 13.5, 700 if late else 500,
                AMBER_D if late else INK2)
        if reminded:
            s_.text(x + 16, y + h / 2 + 15, "reminder sent today", 12, 500, AMBER_D)
    return f


TYPE_COLOUR = {"Requisition": BLUE, "Award": VIOLET, "Budget revision": TEAL, "Prequalification": BRAND,
               "LPO": BRAND_D}


def w02_my_approvals():
    s = console("02 My approvals (Country Director)", "My approvals", ["My approvals"], "samuel", owner=True)
    y = page_head(s, "My approvals", "Waiting on you: 4. Each was prepared by someone else; your comment goes on the record.")
    rows, links = [], []
    for typ, code, what, val, step, by, since, tgt in INBOX:
        rows.append([c_chip(typ, TYPE_COLOUR[typ]), c_ref(code, what), c_money(val) if val else c_text("—", FAINT),
                     c_text(step, INK2), c_person(by), _waiting(since, since == "2 days" and typ == "Award")])
        links.append(tgt)
    cols = [("Type", 200, "start"), ("What", 480, "start"), ("Value (UGX)", 160, "end"), ("Step", 270, "start"),
            ("Prepared by", 230, "start"), ("Waiting", 172, "start")]
    list_card(s, y, 58 + 44 + 70 * len(rows) + 20)
    tabs(s, X0 + 24, y + 14, [("Waiting on me", 4), ("Decided by me", 37), ("All", 41)], "Waiting on me")
    end = data_table(s, X0, y + 58, cols, rows, links=links, row_h=70, sort={"Waiting"})
    y = end + 40
    s.text(X0, y + 10, "Recently decided by you", 16, 700, INK)
    y += 26
    recent = [("Award", "PR-2026-0087", "10 laptops · Busoga Tech Supplies", 36_400_000, "Approved", "Mon 5 Oct, 09:20", "w11b"),
              ("LPO", "LPO-2026-0051", "Signature · Busoga Tech Supplies", 36_400_000, "Approved", "Tue 6 Oct, 10:55", "w14b"),
              ("Budget revision", "BR-2026-0006", "Head office operations · move UGX 4.5M", 4_500_000, "Approved", "Tue 22 Sep, 10:14", None)]
    rows = [[c_chip(t, TYPE_COLOUR[t]), c_ref(code, what), c_money(v), c_status(st), c_text(on, INK2)]
            for t, code, what, v, st, on, _ in recent]
    cols = [("Type", 200, "start"), ("What", 560, "start"), ("Value (UGX)", 180, "end"), ("Decision", 260, "start"),
            ("When", 312, "start")]
    list_card(s, y, 44 + 60 * len(rows) + 4)
    data_table(s, X0, y, cols, rows, links=[r[6] for r in recent], row_h=60)
    return s


def _requisition_decision(key, title, viewer, no, item_title, items, project_line, line, maker, steps, comment,
                          track_since, budget, back, placeholder=False, active="My approvals", crumbs=None, decide=True,
                          approver=None, waiting=None):
    """A requisition waiting on an approver, as a full record page. decide=True: the approver's own copy (from My
    approvals, or from Requisitions) with Approve / Return / Reject. decide=False: the same page for everyone else who
    opens it from Requisitions, read only, with who it waits on."""
    s = console(title, active, crumbs or ["My approvals", no], viewer, owner=decide)
    name = PEOPLE[approver or viewer][0] + (" (you)" if decide else "")
    y = record_header(s, Y0, no, item_title,
                      chips=[("Awaiting approval", None, "status"), (project_line[0], project_line[1], "chip")],
                      facts=[("Requested by", f"{PEOPLE[maker][0]} · {project_line[2]}"), ("Line", line),
                             ("Method", project_line[3])],
                      track=lambda s_, x, y_, w: file_track(s_, x, y_, w, "Requested", waiting=name,
                                                            since=track_since))
    y += 20
    lw = 1090
    s.rect(X0, y, lw, 220, fill=CARD, rx=16, stroke=LINE, name="requirement")
    s.text(X0 + 24, y + 38, "What is being asked for", 17, 700, INK)
    cols = [("Item", 560, "start"), ("Qty", 120, "start"), ("Unit price", 190, "end"), ("Total", 220, "end")]
    rows = [[c_two(d, sub, bold=True), c_text(q, INK2), c_money(p, bold=False), c_money(t)] for d, sub, q, p, t, *_ in items]
    end = data_table(s, X0, y + 56, cols, rows, row_h=64, check=False)
    s.text(X0 + 24, end + 34, "Why", 12.5, 700, MUTED)
    s.para(X0 + 64, end + 34, items[0][5] if len(items[0]) > 5 else "", lw - 100, 13.5, 400, INK2, lh=20)
    y2 = y + 240
    s.rect(X0, y2, lw, 380, fill=CARD, rx=16, stroke=LINE, name="budget check")
    bud, spent, avail_before, req = budget
    s.text(X0 + 24, y2 + 38, "Budget check", 17, 700, INK)
    s.text(X0 + 160, y2 + 38, line, 13, 400, MUTED)
    budget_bar(s, X0 + 24, y2 + 66, lw - 48, bud, spent, request=req, h=12)
    for i, (lab, v, col) in enumerate([("Line budget", bud, INK), ("Spent, committed and reserved", spent, INK2),
                                       ("Available before this request", avail_before, INK),
                                       ("This request", req, AMBER_D), ("Left after approval", avail_before - req, BRAND_M)]):
        ly = y2 + 112 + i * 32
        s.text(X0 + 24, ly, lab, 13.5, 500, INK2)
        s.text(X0 + 420, ly, _m(v), 14, 700, col, anchor="end")
    s.rect(X0 + 470, y2 + 96, lw - 494, 160, fill=FIELD_BG, rx=12)
    s.text(X0 + 490, y2 + 126, "Funds are reserved when the last step approves", 13.5, 700, INK)
    s.para(X0 + 490, y2 + 152, "Until then this request reserves nothing, so other requisitions on the line see the "
           "available balance above. On approval it is reserved; the LPO later commits it.", lw - 534, 13, 400, INK2, lh=20)
    if decide:
        decision_panel(s, X0 + lw + 20, y, CW - lw - 20, viewer=viewer, maker=maker, what="requisition", comment=comment,
                       steps=steps, back=back, h=620, placeholder=placeholder)
    else:
        approval_panel(s, X0 + lw + 20, y, CW - lw - 20, 620, steps, waiting)
    return s


def _solar(title, **kw):
    """PR-2026-0096, Grace's solar backup system, waiting on the Executive Approver (step 3 of 3)."""
    items = [("Solar backup system, installed", "10 kVA hybrid inverter · 20 kWh lithium batteries · 3-year service",
              "1 Lot", 34_500_000, 34_500_000,
              "Power cuts stop training 2–3 days a week; the hub's diesel generator costs UGX 1.1M a month in fuel.")]
    return _requisition_decision(
        None, title, kw.pop("viewer", "samuel"), "PR-2026-0096", "Solar backup system",
        items, ("KOICA", KOICA, "Fri 9 Oct", "RFQ + committee (above UGX 30M)"), "5230 Solar & electrical · Kasese ICT Hub",
        "grace",
        [("Department review", "Daniel Okello · approved Sat 10 Oct", "done"),
         ("Funds check", "Ruth Nakato · approved Sun 11 Oct", "done"),
         ("Executive approval", "Samuel Kato · above UGX 30M", "now")],
        "Approved. Run the RFQ with an evaluation committee; include a service contract.", "1 day",
        (48_000_000, 6_200_000, 41_800_000, 34_500_000), kw.pop("back", "w02"), approver="samuel",
        waiting=("Samuel Kato", "Executive Approver · step 3 of 3 · since Sun 11 Oct · he decides from My approvals "
                 "or from here"), **kw)


REQ_CRUMBS = lambda no: ["Procurement", "Requisitions", no]   # noqa: E731


def w02b_approve_requisition():
    return _solar("02b Approve requisition PR-2026-0096 (Executive Approver)")


def w10d_solar():
    return _solar("10d Requisition PR-2026-0096: Solar backup system", viewer="ivan", decide=False,
                  active="Requisitions", crumbs=REQ_CRUMBS("PR-2026-0096"))


def w10d_samuel():
    return _solar("10d Requisition PR-2026-0096: Solar backup system (your decision)", active="Requisitions",
                  crumbs=REQ_CRUMBS("PR-2026-0096"), back="w10")


w10d_samuel.key = "w10d-samuel"


def w03_hod_approvals():
    s = console("03 My approvals (Department Head)", "My approvals", ["My approvals"], "daniel", owner=True)
    y = page_head(s, "My approvals", "Requisitions from Programmes come to you first (step 1).")
    note(s, X0, y, CW, "You're away 19–30 Oct: Rebecca Achan (Department Head, Administration) approves for you then, set by Ivan Ssemanda in Users.",
         icon="calendar")
    y += 64
    rows = [[c_chip("Requisition", BLUE), c_ref("PR-2026-0095", "Hygiene kits for model homes · Model Home Health, Kumi"),
             c_money(3_600_000), c_text("Department review · 1 of 2", INK2), c_person("harriet"), _waiting("4 h")]]
    cols = [("Type", 200, "start"), ("What", 480, "start"), ("Value (UGX)", 160, "end"), ("Step", 270, "start"),
            ("Prepared by", 230, "start"), ("Waiting", 172, "start")]
    list_card(s, y, 58 + 44 + 70 + 20)
    tabs(s, X0 + 24, y + 14, [("Waiting on me", 1), ("Decided by me", 58), ("All", 59)], "Waiting on me")
    end = data_table(s, X0, y + 58, cols, rows, links=["w03b"], row_h=70)
    y = end + 40
    s.text(X0, y + 10, "Recently decided by you", 16, 700, INK)
    y += 26
    recent = [("PR-2026-0096", "Solar backup system · Kasese ICT Hub", 34_500_000, "Approved", "Sat 10 Oct, 08:30"),
              ("PR-2026-0093", "Network switches and cabling · Kamuli", 14_200_000, "Approved", "Wed 7 Oct, 16:02"),
              ("PR-2026-0091", "Desks and chairs, Kamuli ICT centre", 18_600_000, "Approved", "Tue 6 Oct, 11:47"),
              ("PR-2026-0090", "Washroom block, Busalamu P/S", 86_000_000, "Approved", "Thu 24 Sep, 09:15"),
              ("PR-2026-0087", "10 laptops for training room 2", 38_000_000, "Approved", "Mon 14 Sep, 15:40")]
    rows = [[c_chip("Requisition", BLUE), c_ref(code, what), c_money(v), c_status(st), c_text(on, INK2)]
            for code, what, v, st, on in recent]
    cols = [("Type", 200, "start"), ("What", 560, "start"), ("Value (UGX)", 180, "end"), ("Decision", 260, "start"),
            ("When", 312, "start")]
    list_card(s, y, 44 + 60 * len(rows) + 4)
    data_table(s, X0, y, cols, rows, links=["w10d", None, None, None, "w11b"], row_h=60)
    return s


def _hygiene(title, **kw):
    """PR-2026-0095, Harriet's hygiene kits, waiting on the Department Head (step 1 of 2)."""
    items = [("Household hygiene kits", "Soap, jerrycan, basin, sanitary pads, nail clipper · packed per household",
              "120 Kits", 30_000, 3_600_000,
              "For the November household visits in Kumi: one kit per model home enrolled this quarter.")]
    return _requisition_decision(
        None, title, kw.pop("viewer", "daniel"), "PR-2026-0095",
        "Hygiene kits for model homes", items, ("KFHI", BRAND_M, "Today 05:40", "Direct purchase (up to UGX 5M)"),
        "5610 Health supplies · Model Home Health, Kumi", "harriet",
        [("Department review", "Daniel Okello · Department Head", "now"),
         ("Funds check", "Ruth Nakato · Finance Officer", "next"),
         ("Executive approval", "Only above UGX 30M · not needed", "skipped")],
        "Write a comment (required to return or reject)", "4 hours", (26_000_000, 15_400_000, 10_600_000, 3_600_000),
        kw.pop("back", "w03"), placeholder=True, approver="daniel",
        waiting=("Daniel Okello", "Department Head · step 1 of 2 · since 05:40 today · he decides from My approvals "
                 "or from here"), **kw)


def w03b_hod_decision():
    return _hygiene("03b Approve requisition PR-2026-0095 (Department Head)")


def w10e_hygiene():
    return _hygiene("10e Requisition PR-2026-0095: Hygiene kits for model homes", viewer="ivan", decide=False,
                    active="Requisitions", crumbs=REQ_CRUMBS("PR-2026-0095"))


def w10e_daniel():
    return _hygiene("10e Requisition PR-2026-0095: Hygiene kits for model homes (your decision)", active="Requisitions",
                    crumbs=REQ_CRUMBS("PR-2026-0095"), back="w10")


w10e_daniel.key = "w10e-daniel"


# Ruth's and Ivan's My approvals: nothing waiting today, which is a state worth showing (PLAN.md §5)
OWN_DECIDED = {
    "ruth": [("Requisition", "PR-2026-0096", "Solar backup system · funds check", 34_500_000, "Approved", "Sun 11 Oct, 10:22", None),
             ("LPO", "LPO-2026-0051", "Commitment check · Busoga Tech Supplies", 36_400_000, "Approved", "Mon 5 Oct, 15:10", "w14b"),
             ("Requisition", "PR-2026-0094", "Salon and sewing kits · funds check", 12_800_000, "Returned", "Sat 10 Oct, 09:40", None),
             ("Requisition", "PR-2026-0087", "10 laptops · funds check", 38_000_000, "Approved", "Tue 15 Sep, 10:05", "w11b")],
    "ivan": [],
}
EMPTY_NOTE = {
    "ruth": "Funds checks come to you after the Department Head; LPO commitment checks after Procurement prepares one.",
    "ivan": "Changes you submit to approval workflows go to the Country Director; you can't approve your own.",
}


def _own_inbox(person):
    name, *_rest = PEOPLE[person]
    s = console(f"02 My approvals ({name})", "My approvals", ["My approvals"], person, owner=True)
    y = page_head(s, "My approvals", "Nothing is waiting on you right now.")
    list_card(s, y, 58 + 230)
    tabs(s, X0 + 24, y + 14, [("Waiting on me", 0), ("Decided by me", len(OWN_DECIDED[person]) or 0)], "Waiting on me")
    cx = X0 + CW / 2
    s.circle(cx, y + 118, 30, fill=LIME)
    s.icon("check", cx - 15, y + 103, 30, LIME_D, 3)
    s.text(cx, y + 178, "You're up to date", 19, 700, INK, anchor="middle", family="display")
    s.text(cx, y + 204, EMPTY_NOTE[person], 13.5, 400, MUTED, anchor="middle")
    y += 58 + 230 + 30
    if OWN_DECIDED[person]:
        s.text(X0, y + 10, "Recently decided by you", 16, 700, INK)
        y += 26
        rows = [[c_chip(t, TYPE_COLOUR[t]), c_ref(code, what), c_money(v), c_status(st), c_text(on, INK2)]
                for t, code, what, v, st, on, _ in OWN_DECIDED[person]]
        cols = [("Type", 200, "start"), ("What", 560, "start"), ("Value (UGX)", 180, "end"), ("Decision", 260, "start"),
                ("When", 312, "start")]
        list_card(s, y, 44 + 60 * len(rows) + 4)
        data_table(s, X0, y, cols, rows, links=[r[6] for r in OWN_DECIDED[person]], row_h=60)
    return s


OWN_INBOXES = [_person_screen("w02-ruth", _own_inbox, "ruth"), _person_screen("w02-ivan", _own_inbox, "ivan")]


SCREENS = [*DASHBOARDS, w02_my_approvals, w02b_approve_requisition, *OWN_INBOXES, w03_hod_approvals,
           w03b_hod_decision, w10d_solar, w10d_samuel, w10e_hygiene, w10e_daniel]
