"""Setup: the master data every transaction depends on (w50–w58), one menu item and one screen each.

Order matters (PLAN.md §4): financial years → departments → offices → donors → projects → account codes →
procurement categories → supplier document types → units of measure. Each subtitle says what the list
belongs to and what uses it. Lists are Active / Inactive; a row in use is deactivated, never deleted.
Viewer: Ivan Ssemanda, System Admin.
"""
from __future__ import annotations

from data import (ACCOUNT_CODES, CATEGORIES, DEPARTMENTS, DOC_TYPES, DONORS, FINANCIAL_YEARS, OFFICES, PROJECTS,
                  UNITS)
from kit import (AMBER_D, BLUE, BRAND, BRAND_M, CARD, GREY, INK, INK2, KOICA, LINE, MUTED, TEAL, VIOLET, button,
                 checkbox, chip, field, money, textarea, toggle, tw)
from shell import (writes, CW, X0, X1, c_actions, c_chip, c_num, c_ref, c_status, c_text, c_two, console, data_table, dialog,
                   list_card, note, page_head, pager, toolbar)

ADMIN = "ivan"
DONOR_COLOUR = {"KOICA": KOICA, "KFHI": BRAND_M, "IDIU": AMBER_D}


def _master(key_title, active, title, subtitle, cols, rows, search, new, new_target=None, filters=(), hl=None,
            total=None, footnote=None, links=None):
    s = console(key_title, active, ["Setup", active], ADMIN)
    y = page_head(s, title, subtitle, actions=[("Import from Excel", "secondary", "upload", None)])
    total = total or len(rows)
    row_h = 62
    card_h = 78 + 44 + row_h * len(rows) + 58
    list_card(s, y, card_h)
    toolbar(s, X0, y, CW, search, new=new, new_target=new_target, filters=filters)
    end = data_table(s, X0, y + 78, cols, rows, row_h=row_h, hl=hl, links=links, sort={cols[1][0]})
    pager(s, X0, end, CW, (1, len(rows)), total, pages=max(1, -(-total // 10)))
    if footnote:
        note(s, X0, y + card_h + 20, CW, footnote)
    return s


def _status(st):
    return c_status(st)


# =====================================================================================
def w50_financial_years():
    rows = [[c_text(n, INK, 700), c_text(a), c_text(b), c_num(budgets, "budgets" if budgets != 1 else "budget"),
             _status(st), c_actions("edit", "lock" if st == "Open" else "eye")]
            for n, a, b, st, budgets in FINANCIAL_YEARS]
    cols = [("Financial year", 300, "start"), ("Starts", 260, "start"), ("Ends", 260, "start"), ("Budgets", 180, "end"),
            ("Status", 280, "start"), ("Actions", 232, "start")]
    return _master("50 Setup: Financial years", "Financial years", "Financial years",
                   "Budgets belong to a financial year. Only an open year takes new requisitions.",
                   cols, rows, "Search financial years…", "New financial year", "w50b", hl=1,
                   footnote="Closing FY 2026 will lock its budgets: open requisitions must be finished or moved to "
                            "FY 2027 first. Closing a year needs the Country Director's approval.")


def w50b_new_financial_year():
    s = writes(w50_financial_years(), ["Finance Officer", "System Admin"])
    s.title = "50b Setup: New financial year"
    x, y = dialog(s, 640, 560, "New financial year", "Budgets can be drafted for it straight away.", close_target="w50")
    w = 576
    hw = (w - 24) / 2
    y += field(s, x, y, 240, "Name", "FY 2028", required=True, focus=True, hint="Unique") + 14
    field(s, x, y, hw, "Starts", "1 Jan 2028", required=True, icon="calendar")
    field(s, x + hw + 24, y, hw, "Ends", "31 Dec 2028", required=True, icon="calendar")
    y += 90
    s.text(x, y + 14, "Status", 13, 600, INK2)
    chip(s, x, y + 26, "Planning", BLUE)
    s.para(x + 96, y + 43, "Opens for requisitions when FY 2027 closes.", w - 96, 13, 400, MUTED)
    y += 70
    note(s, x, y, w, "A year can't overlap another. Opening and closing a year need the Country Director's approval.",
         icon="shield")
    by = 1080 / 2 + 560 / 2 - 66
    s.line(x - 32, by - 14, x + w + 32, by - 14, LINE)
    button(s, x + w, by, "Save financial year", "primary", icon="check", anchor="end", target="w50")
    button(s, x + w - 200, by, "Cancel", "secondary", anchor="end", target="w50")
    return s


def w51_departments():
    rows = []
    for code, name, head, users, reqs, st in DEPARTMENTS:
        rows.append([c_ref(code), c_two(name, f"Head: {head}" if head != "—" else "No head assigned"),
                     c_num(users), c_num(reqs), _status(st),
                     c_actions("edit", "ban" if st == "Active" and users == 0 else ("check" if st == "Inactive" else "eye"))])
    cols = [("Code", 150, "start"), ("Department", 520, "start"), ("Users", 170, "end"),
            ("Requisitions FY 2026", 230, "end"), ("Status", 220, "start"), ("Actions", 222, "start")]
    return _master("51 Setup: Departments", "Departments", "Departments",
                   "Every user and requisition belongs to a department; its head approves step 1 of the department's "
                   "requisitions.", cols, rows, "Search departments…", "New department", "w51b",
                   footnote="Departments in use are deactivated, never deleted, so past requisitions keep their "
                            "department. Monitoring & Evaluation was deactivated on 1 Jul 2026 (merged into Programmes).")


def w51b_new_department():
    s = w51_departments()
    s.title = "51b Setup: New department"
    writes(s)
    x, y = dialog(s, 640, 600, "New department", "Users and requisitions can use it once it is saved.",
                  close_target="w51")
    w = 576
    y += field(s, x, y, 180, "Code", "PRM", required=True, mono=True, focus=True,
               hint="2–4 letters, unique") + 14
    y += field(s, x, y, w, "Department name", "Partnerships & Resource Mobilisation", required=True) + 14
    y += field(s, x, y, w, "Head of department", "Choose a user (you can add one later)", placeholder=True,
               dropdown=True, icon="user", hint="Approves step 1 of this department's requisitions") + 14
    y += field(s, x, y, w, "Description", "Donor relations, proposals and grant reporting") + 18
    s.text(x, y + 14, "Status", 13, 600, INK2)
    toggle(s, x, y + 26, True)
    s.text(x + 48, y + 41, "Active", 14, 600, INK)
    by = y + 80
    s.line(x - 32, by - 14, x + w + 32, by - 14, LINE)
    button(s, x + w, by, "Save department", "primary", icon="check", anchor="end", target="w51")
    button(s, x + w - 172, by, "Cancel", "secondary", anchor="end", target="w51")
    return s


def w52_offices():
    type_col = {"Head office": BRAND, "Field office": TEAL, "Project site": VIOLET}
    rows = [[c_ref(code), c_two(name, f"{district} district"), c_chip(typ, type_col[typ]), c_num(users), c_num(reqs),
             _status(st), c_actions("edit", "eye")] for code, name, district, typ, users, reqs, st in OFFICES]
    cols = [("Code", 140, "start"), ("Office / cost centre", 400, "start"), ("Type", 230, "start"),
            ("Users", 150, "end"), ("Requisitions FY 2026", 230, "end"), ("Status", 180, "start"),
            ("Actions", 182, "start")]
    return _master("52 Setup: Offices & cost centres", "Offices & cost centres", "Offices & cost centres",
                   "Users work from an office; requisitions and budget lines are charged to its cost centre.",
                   cols, rows, "Search offices…", "New office", "w52b")


def w53_donors():
    rows = [[c_ref(code, color=DONOR_COLOUR[code]), c_two(name, typ), c_text(country), c_num(projects, "projects" if projects != 1 else "project"),
             _status(st), c_actions("edit", "eye")] for code, name, typ, country, projects, st in DONORS]
    cols = [("Code", 160, "start"), ("Donor / funding source", 560, "start"), ("Country", 230, "start"),
            ("Projects", 180, "end"), ("Status", 200, "start"), ("Actions", 182, "start")]
    return _master("53 Setup: Donors", "Donors", "Donors",
                   "Projects are funded by a donor; reports and exports group spending by donor.",
                   cols, rows, "Search donors…", "New donor", "w53b",
                   footnote="Donor rules (for example KOICA's bidding thresholds) are recorded on the donor and shown "
                            "to Procurement when they source for that donor's projects.")


def w54_projects():
    rows = []
    for code, name, donor, dept, office, start, end, budget, st in PROJECTS:
        rows.append([c_ref(code), c_two(name, f"{dept} · {office}"), c_chip(donor, DONOR_COLOUR[donor]),
                     c_text(f"{start} – {end}", INK2), c_num(money(budget, short=True, ugx=False), "FY 2026 budget"),
                     _status(st), c_actions("edit", "eye")])
    cols = [("Code", 150, "start"), ("Project", 470, "start"), ("Donor", 150, "start"), ("Period", 240, "start"),
            ("Budget", 170, "end"), ("Status", 150, "start"), ("Actions", 182, "start")]
    return _master("54 Setup: Projects", "Projects", "Projects",
                   "Projects belong to a donor, a department and an office, and hold the budget lines requisitions "
                   "draw on.", cols, rows, "Search projects…", "New project", "w54b", filters=["FY 2026"],
                   links=[None] * len(rows))


def w54b_new_project():
    s = writes(console("54b Setup: New project", "Projects", ["Setup", "Projects", "New project"], ADMIN))
    y = page_head(s, "New project", "A project needs its donor, department and office to exist first.")
    fx, fw = X0, 980
    s.rect(fx, y, fw, 652, fill=CARD, rx=16, stroke=LINE, name="form card")
    x, yy, w = fx + 32, y + 30, fw - 64
    hw = (w - 24) / 2
    s.text(x, yy + 8, "Project details", 17, 700, INK)
    yy += 30
    field(s, x, yy, 200, "Code", "AMU-WATER", required=True, mono=True, hint="Unique; used in budget codes")
    field(s, x + 224, yy, w - 224, "Project name", "Amuria Community Water Points", required=True)
    yy += 100
    field(s, x, yy, hw, "Donor", "KFHI · Korea Food for the Hungry International", required=True, dropdown=True,
          icon="landmark", ok="From Setup › Donors")
    field(s, x + hw + 24, yy, hw, "Department", "Programmes", required=True, dropdown=True, icon="building",
          ok="From Setup › Departments")
    yy += 100
    field(s, x, yy, hw, "Office / cost centre", "AMU · Amuria field office", required=True, dropdown=True,
          icon="pin", ok="From Setup › Offices & cost centres")
    field(s, x + hw + 24, yy, hw, "Project manager", "Esther Namutebi", dropdown=True, icon="user")
    yy += 100
    field(s, x, yy, hw, "Starts", "1 Jan 2027", required=True, icon="calendar")
    field(s, x + hw + 24, yy, hw, "Ends", "31 Dec 2028", required=True, icon="calendar")
    yy += 84
    textarea(s, x, yy, w, 96, "Description",
             "Drill and equip six boreholes with community water committees in Amuria district.")
    by = y + 652 - 70
    s.line(fx, by - 18, fx + fw, by - 18, LINE)
    button(s, fx + fw - 32, by, "Save project", "primary", icon="check", anchor="end", target="w54")
    button(s, fx + fw - 192, by, "Cancel", "secondary", anchor="end", target="w54")

    # what this project depends on, and what comes next
    rx, rw = fx + fw + 24, X1 - fx - fw - 24
    s.rect(rx, y, rw, 380, fill=CARD, rx=16, stroke=LINE, name="setup order card")
    s.text(rx + 28, y + 40, "Setup order", 17, 700, INK)
    s.text(rx + 28, y + 62, "What must exist before, and what follows", 13, 400, MUTED)
    steps = [("Financial years", True), ("Departments", True), ("Offices & cost centres", True), ("Donors", True),
             ("Projects", None), ("Budgets & budget lines", False), ("Requisitions", False)]
    sy = y + 96
    for i, (lab, done) in enumerate(steps):
        cy = sy + i * 40
        if i < len(steps) - 1:
            s.line(rx + 40, cy + 12, rx + 40, cy + 40, LINE, 2)
        if done:
            s.circle(rx + 40, cy, 11, fill=BRAND_M)
            s.icon("check", rx + 33, cy - 7, 14, "#FFFFFF", 3)
        elif done is None:
            s.circle(rx + 40, cy, 11, fill="#D9F0B8")
            s.circle(rx + 40, cy, 4.5, fill="#2F5A0F")
        else:
            s.circle(rx + 40, cy, 10, fill=CARD, stroke="#C2CEC6", sw=2)
        s.text(rx + 64, cy + 5, lab, 14, 700 if done is None else 500, INK if done is not False else MUTED)
        if done is None:
            chip(s, rx + rw - 28, cy - 12, "You are here", BRAND, anchor="end")
    note(s, rx, y + 400, rw, "Once saved, Finance can enter the project's budget line by line or import it from Excel, "
         "and submit it to the Country Director for approval.", icon="wallet")
    return s


def w55_account_codes():
    group_col = {"Supplies": TEAL, "Equipment": BLUE, "Works": VIOLET, "Programme costs": BRAND_M, "Transport": AMBER_D}
    rows = [[c_ref(code), c_text(name, INK, 600), c_chip(grp, group_col[grp]), c_text(acc, INK2, mono=True),
             c_num(lines, "budget lines"), _status("Active"), c_actions("edit", "eye")]
            for code, name, grp, lines, acc in ACCOUNT_CODES]
    cols = [("Code", 140, "start"), ("Account", 420, "start"), ("Group", 230, "start"),
            ("Accounting code", 230, "start"), ("Used on", 170, "end"), ("Status", 150, "start"),
            ("Actions", 162, "start")]
    return _master("55 Setup: Account codes", "Account codes", "Account codes",
                   "Budget lines use an account code; each maps to Finance's chart of accounts for the export.",
                   cols, rows, "Search account codes…", "New account code", "w55b",
                   footnote="Codes are illustrative. During inception they are copied from IDIU's accounting package so "
                            "every commitment and payment exports to the right ledger account.")


def w56_categories():
    rows = []
    for code, name, acc, preq, rfqs, st in CATEGORIES:
        docs = 9 if code == "WRK" else 7   # Setup › Supplier document types: 7 for all, +2 for works
        rows.append([c_ref(code), c_two(name, f"Default account {acc}"), c_chip(f"{docs} documents", BLUE, icon="file"),
                     c_num(preq, "prequalified"), c_num(rfqs, "open RFQs" if rfqs != 1 else "open RFQ"), _status(st),
                     c_actions("edit", "eye")])
    cols = [("Code", 140, "start"), ("Category", 440, "start"), ("Required documents", 260, "start"),
            ("Suppliers", 180, "end"), ("RFQs", 160, "end"), ("Status", 150, "start"), ("Actions", 182, "start")]
    return _master("56 Setup: Procurement categories", "Procurement categories", "Procurement categories",
                   "Suppliers prequalify in categories; an RFQ can only invite suppliers prequalified in its category.",
                   cols, rows, "Search categories…", "New category", "w56b")


def w57_document_types():
    rows = []
    for name, expires, validity, req in DOC_TYPES:
        rows.append([c_text(name, INK, 600),
                     c_chip("Expires", AMBER_D, icon="clock") if expires else c_chip("No expiry", GREY),
                     c_text(validity, INK2), c_text(req, INK2),
                     c_text("30 days before" if expires else "—", INK2), _status("Active"), c_actions("edit")])
    cols = [("Document", 400, "start"), ("Expiry", 180, "start"), ("Valid for", 200, "start"),
            ("Required for", 260, "start"), ("Alert", 170, "start"), ("Status", 150, "start"), ("Actions", 152, "start")]
    return _master("57 Setup: Supplier document types", "Supplier document types", "Supplier document types",
                   "What suppliers must upload to prequalify; documents that expire alert the supplier and Procurement.",
                   cols, rows, "Search document types…", "New document type", "w57b")


def w58_units():
    rows = [[c_ref(code), c_text(name, INK, 600), c_num(used, "requisition and LPO lines"), _status("Active"),
             c_actions("edit")] for code, name, used in UNITS]
    cols = [("Code", 200, "start"), ("Unit", 520, "start"), ("Used on", 340, "end"), ("Status", 250, "start"),
            ("Actions", 202, "start")]
    return _master("58 Setup: Units of measure", "Units of measure", "Units of measure",
                   "Requisition and LPO lines count items in these units.", cols, rows, "Search units…", "New unit", "w58b")


# ---------------------------------------------------------------- "New …" on every setup list
# One dialog per list over the list itself. It opens for every role whose menu has the list (System Admin all of them;
# Finance: financial years and account codes; Procurement: categories, document types and units), never the Auditor.
def _new(base, title, heading, sub, back, h, save):
    s = writes(base())
    s.title = title
    x, y = dialog(s, 760, h, heading, sub, close_target=back)
    by = 1080 / 2 + h / 2 - 66
    s.line(x - 32, by - 14, x + 760 - 32, by - 14, LINE)
    button(s, x + 696, by, save, "primary", icon="check", anchor="end", h=42, target=back)
    button(s, x + 696 - tw(save, 14, 600) - 74, by, "Cancel", "secondary", anchor="end", h=42, target=back)
    return s, x, y, 696, (696 - 24) / 2


def _active(s, x, y, label="Active"):
    s.text(x, y + 14, "Status", 13, 600, INK2)
    toggle(s, x, y + 26, True)
    s.text(x + 48, y + 41, label, 14, 600, INK)


def w52b_new_office():
    s, x, y, w, hw = _new(w52_offices, "52b Setup: New office", "New office or cost centre",
                          "Users, requisitions and budget lines can use it once saved.", "w52", 560, "Save office")
    field(s, x, y, 180, "Code", "IGA", required=True, mono=True, focus=True, hint="2–4 letters, unique")
    field(s, x + 204, y, w - 204, "Name", "Iganga field office", required=True)
    y += 104
    field(s, x, y, hw, "District", "Iganga", required=True, dropdown=True, icon="pin")
    field(s, x + hw + 24, y, hw, "Type", "Field office", required=True, dropdown=True, icon="building")
    y += 90
    field(s, x, y, w, "Delivery address", "Plot 7 Main Street, Iganga · for LPOs delivered here", icon="truck")
    y += 90
    _active(s, x, y)
    return s


def w53b_new_donor():
    s, x, y, w, hw = _new(w53_donors, "53b Setup: New donor", "New donor",
                          "Projects are funded by a donor; it must exist before the project.", "w53", 600, "Save donor")
    field(s, x, y, 180, "Code", "Short code", required=True, placeholder=True, focus=True, hint="Shown on projects")
    field(s, x + 204, y, w - 204, "Name", "The donor's full name", required=True, placeholder=True)
    y += 104
    field(s, x, y, hw, "Type", "Bilateral agency", required=True, dropdown=True)
    field(s, x + hw + 24, y, hw, "Country", "Choose a country", dropdown=True, icon="globe", placeholder=True)
    y += 90
    field(s, x, y, hw, "Contact person", "Name", placeholder=True, icon="user")
    field(s, x + hw + 24, y, hw, "Contact email", "name@donor.org", placeholder=True, icon="mail")
    y += 90
    field(s, x, y, hw, "Reporting currency", "USD", dropdown=True, icon="coins")
    _active(s, x + hw + 24, y)
    return s


def w55b_new_account_code():
    s, x, y, w, hw = _new(w55_account_codes, "55b Setup: New account code", "New account code",
                          "Budget lines use it; the export maps it to the accounting package.", "w55", 500,
                          "Save account code")
    field(s, x, y, 180, "Code", "5710", required=True, mono=True, focus=True, hint="4 digits, unique")
    field(s, x + 204, y, w - 204, "Name", "Communication & internet", required=True)
    y += 104
    field(s, x, y, hw, "Group", "Programme costs", required=True, dropdown=True, icon="layers")
    field(s, x + hw + 24, y, hw, "Accounting package code", "6150-00", required=True, mono=True, icon="sheet",
          hint="Used by the Excel export")
    y += 104
    _active(s, x, y)
    note(s, x + 200, y + 10, w - 200, "Once a budget line uses it, it can be deactivated, never deleted.",
         icon="info")
    return s


def w56b_new_category():
    s, x, y, w, hw = _new(w56_categories, "56b Setup: New procurement category", "New procurement category",
                          "Suppliers prequalify per category; RFQs go to a category's suppliers.", "w56", 620,
                          "Save category")
    field(s, x, y, 180, "Code", "CLN", required=True, mono=True, focus=True, hint="2–4 letters, unique")
    field(s, x + 204, y, w - 204, "Name", "Cleaning & hygiene services", required=True)
    y += 104
    field(s, x, y, w, "Default account code", "5110 · Office supplies & stationery", required=True, dropdown=True,
          icon="hash", hint="Suggested on requisition lines in this category")
    y += 104
    s.text(x, y + 14, "Documents suppliers must upload", 13, 600, INK2)
    y += 28
    cw = (w - 12) / 2
    for i, (name, *_rest, req) in enumerate([d for d in DOC_TYPES if d[3] == "All categories"]):
        cx, cy = x + (i % 2) * (cw + 12), y + (i // 2) * 34
        checkbox(s, cx, cy, True)
        s.text(cx + 28, cy + 14, name, 13.5, 500, INK, maxw=cw - 30)
    return s


def w57b_new_document_type():
    s, x, y, w, hw = _new(w57_document_types, "57b Setup: New supplier document type", "New supplier document type",
                          "Asked for at registration; IDIU checks each upload.", "w57", 570, "Save document type")
    field(s, x, y, w, "Name", "Fire safety certificate", required=True, focus=True)
    y += 90
    s.text(x, y + 14, "Expires", 13, 600, INK2)
    toggle(s, x, y + 26, True)
    s.text(x + 48, y + 41, "Yes", 14, 600, INK)
    field(s, x + 160, y, hw - 160, "Valid for", "12", required=True, suffix="months")
    field(s, x + hw + 24, y, hw, "Reminder", "30", suffix="days before expiry", icon="bell")
    y += 96
    field(s, x, y, w, "Required for", "Construction & works", required=True, dropdown=True, icon="tag",
          hint="One or more procurement categories, or all")
    y += 104
    _active(s, x, y)
    return s


def w58b_new_unit():
    s, x, y, w, hw = _new(w58_units, "58b Setup: New unit of measure", "New unit of measure",
                          "Requisition and LPO lines count items in it.", "w58", 460, "Save unit")
    field(s, x, y, 180, "Code", "KG", required=True, mono=True, focus=True, hint="Unique")
    field(s, x + 204, y, w - 204, "Name", "Kilogram", required=True)
    y += 104
    field(s, x, y, w, "Allows decimals", "Yes (2.5 kg)", dropdown=True)
    y += 90
    _active(s, x, y)
    return s


SCREENS = [w52b_new_office, w53b_new_donor, w55b_new_account_code, w56b_new_category,
           w57b_new_document_type, w58b_new_unit, w50_financial_years, w50b_new_financial_year, w51_departments, w51b_new_department, w52_offices, w53_donors, w54_projects,
           w54b_new_project, w55_account_codes, w56_categories, w57_document_types, w58_units]
