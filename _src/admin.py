"""Administration (w60–w63b): users, roles & permissions, approval workflows, audit trail.

Viewer: Ivan Ssemanda (System Admin) for users, roles and workflows; Agnes Akello (Auditor, read-only) for
the audit trail. A change to an approval workflow is itself approved by the Country Director, and applies
only to records submitted after it (requests in flight keep the steps they were given).
"""
from __future__ import annotations

from data import AUDIT, AUDIT_COUNT, METHODS, PERMS, ROLES, USERS, WORKFLOWS
from kit import (AMBER_D, BLUE, BRAND, BRAND_D, BRAND_M, CARD, FAINT, FIELD_BG, INK, INK2, LIME, LINE, LINE2, MUTED,
                 ORANGE, RED, TEAL, VIOLET, avatar, button, chip, field, radio, ref, status_chip, tint, toggle, tw)
from shell import (dialog, writes, CW, X0, X1, c_chip, c_person, c_status, c_text, c_two, console, data_table, drawer, list_card, note,
                   page_head, pager, tabs, toolbar)

ROLE_COLOUR = {"Requester": VIOLET, "Head of Department": BLUE, "Finance Officer": TEAL, "Procurement Officer": BRAND,
               "Country Director": AMBER_D, "Stores / Inspection Officer": INK2, "System Admin": BLUE, "Auditor": RED,
               "Evaluation Committee Member": ORANGE}


def w60_users(title="60 Users"):
    s = console(title, "Users", ["Administration", "Users"], "ivan")
    y = page_head(s, "Users", "Each user belongs to a department and an office and has one role. Accounts in use are "
                  "deactivated, never deleted.", actions=[("Add user", "primary", "userplus", "w60c")])
    rows, links = [], []
    for key, name, email, role, dept, office, st, seen in USERS:
        rows.append([c_two(name, email), c_chip(role, ROLE_COLOUR[role]), c_text(dept, INK2), c_text(office, INK2),
                     c_status(st), c_text(seen, INK2)])
        links.append("w60b" if key == "daniel" else None)
    cols = [("User", 380, "start"), ("Role", 300, "start"), ("Department", 260, "start"), ("Office", 170, "start"),
            ("Status", 150, "start"), ("Last seen", 252, "start")]
    list_card(s, y, 58 + 78 + 44 + 62 * len(rows) + 58)
    tabs(s, X0 + 24, y + 14, [("All", 34), ("Active", 32), ("Inactive", 2)], "All")
    toolbar(s, X0, y + 50, CW, "Search by name or email…", filters=["All roles"])
    end = data_table(s, X0, y + 128, cols, rows, links=links, row_h=62, sort={"User"}, hl=0)
    pager(s, X0, end, CW, (1, 10), 34, pages=4)
    return s


def w60b_edit_user():
    s = writes(console("60b Edit user: Daniel Okello", "Users", ["Administration", "Users", "Daniel Okello"], "ivan"),
               ["System Admin"])
    y = page_head(s, "Daniel Okello", "d.okello@idiu.org · Head of Programmes · last seen today 08:12",
                  actions=[("Save changes", "primary", "check", "w60"), ("Cancel", "secondary", None, "w60")])
    lw = 1000
    s.rect(X0, y, lw, 800, fill=CARD, rx=16, stroke=LINE, name="user form")
    x, w = X0 + 28, lw - 56
    hw = (w - 24) / 2
    s.text(x, y + 40, "Account", 17, 700, INK)
    field(s, x, y + 58, hw, "Full name", "Daniel Okello", required=True)
    field(s, x + hw + 24, y + 58, hw, "Email", "d.okello@idiu.org", required=True, icon="mail")
    field(s, x, y + 138, hw, "Department", "PRG · Programmes", required=True, dropdown=True, icon="building",
          ok="From Setup › Departments · head of this department")
    field(s, x + hw + 24, y + 138, hw, "Office", "JIN · Jinja head office", required=True, dropdown=True, icon="pin",
          ok="From Setup › Offices & cost centres")
    s.line(X0, y + 262, X0 + lw, y + 262, LINE2)
    s.text(x, y + 300, "Role", 17, 700, INK)
    s.text(x + 56, y + 300, "one per user; it decides the menus and the approval steps", 13, 400, MUTED)
    roles = ["Requester", "Head of Department", "Finance Officer", "Procurement Officer", "Country Director",
             "Stores / Inspection Officer", "System Admin", "Auditor"]
    rw2 = (w - 24) / 2
    for i, r in enumerate(roles):
        rx_ = x + (i % 2) * (rw2 + 24)
        ry = y + 322 + (i // 2) * 50
        on = r == "Head of Department"
        s.rect(rx_, ry, rw2, 42, fill=tint(LIME, 0.5) if on else CARD, rx=10, stroke=BRAND if on else LINE)
        radio(s, rx_ + 22, ry + 21, on)
        s.text(rx_ + 42, ry + 26, r, 14, 700 if on else 500, INK)
    s.rect(x, y + 532, w, 44, fill=FIELD_BG, rx=10)
    toggle(s, x + 14, y + 544, True)
    s.text(x + 62, y + 559, "Can be appointed to evaluation committees", 14, 600, INK)
    s.line(X0, y + 600, X0 + lw, y + 600, LINE2)
    s.text(x, y + 638, "Away and acting approver", 17, 700, INK)
    toggle(s, x + w - 36, y + 624, True)
    tw3 = (w - 48) / 3
    field(s, x, y + 656, tw3, "Away from", "Mon 19 Oct 2026", icon="calendar")
    field(s, x + tw3 + 24, y + 656, tw3, "Back on", "Fri 30 Oct 2026", icon="calendar")
    field(s, x + 2 * (tw3 + 24), y + 656, tw3, "Acting approver", "Esther Namutebi", dropdown=True, icon="user",
          focus=True)
    s.text(x, y + 770, "While away, Daniel's step-1 approvals go to Esther. Both appear on the record.", 13, 500, MUTED)
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 440, fill=CARD, rx=16, stroke=LINE, name="what daniel can do")
    s.text(rx + 24, y + 40, "What this role can do", 17, 700, INK)
    can = [("check", "Approve step 1 of Programmes requisitions"), ("eye", "See Programmes requisitions and their files"),
           ("eye", "See budgets and the budget utilisation report"), ("ban", "Cannot approve a requisition he raised"),
           ("ban", "Cannot change setup, users or workflows")]
    cy = y + 76
    for ic, txt in can:
        col = RED if ic == "ban" else (BRAND_M if ic == "check" else INK2)
        s.icon(ic, rx + 24, cy - 13, 17, col, 2.2)
        s.text(rx + 52, cy, txt, 13.5, 500, INK2, maxw=rw - 76)
        cy += 38
    s.line(rx + 24, cy - 6, rx + rw - 24, cy - 6, LINE2)
    s.text(rx + 24, cy + 24, "MENUS", 10.5, 700, MUTED, spacing=0.8)
    mx, my = rx + 24, cy + 40
    for lab in PERMS["Head of Department"]:
        cw = tw(lab, 12, 600) + 22
        if mx + cw > rx + rw - 24:
            mx, my = rx + 24, my + 32
        chip(s, mx, my, lab, BRAND)
        mx += cw + 8
    note(s, rx, y + 460, rw, "Role and department changes are recorded in the audit trail with the old and new value.",
         icon="history")
    return s

def w60c_add_user():
    """A new account, filled in by the System Admin: who they are, how to reach them, where they work, their role and a
    first password. The sign-in details can be emailed to them; they change the password at first sign-in."""
    s = writes(w60_users("60c Add user"), ["System Admin"])
    h = 840
    x, y = dialog(s, 800, h, "Add user", "They sign in at the same door as everyone else.", close_target="w60")
    w = 800 - 64
    hw = (w - 24) / 2
    field(s, x, y, hw, "Full name", "Sarah Achieng", required=True, focus=True, icon="user")
    field(s, x + hw + 24, y, hw, "Phone number", "+256 772 418 903", required=True, icon="call")
    y += 90
    field(s, x, y, w, "Email", "s.achieng@idiu.org", required=True, icon="mail", ok="An IDIU address · she signs in with it")
    y += 104
    field(s, x, y, hw, "Department", "PRG · Programmes", required=True, dropdown=True, icon="building")
    field(s, x + hw + 24, y, hw, "Office", "MAY · Mayuge field office", required=True, dropdown=True, icon="pin")
    y += 90
    field(s, x, y, w, "Role", "Requester", required=True, dropdown=True, icon="shield",
          hint="Decides the menus and the approval steps: Dashboard, Requisitions, Deliveries")
    y += 104
    field(s, x, y, w - 150, "Password", "••••••••••••", required=True, icon="lock",
          hint="At least 10 characters. She must change it at first sign-in.")
    button(s, x + w, y + 22, "Generate", "secondary", icon="refresh", anchor="end", h=44)
    y += 104
    s.rect(x, y, w, 50, fill=tint(BRAND, 0.07), rx=10)
    toggle(s, x + 14, y + 14, True)
    s.text(x + 62, y + 31, "Email the sign-in details to Sarah", 14, 700, INK)
    s.text(x + w - 16, y + 31, "s.achieng@idiu.org", 13, 500, MUTED, anchor="end")
    y += 60
    s.rect(x, y, w, 50, fill=FIELD_BG, rx=10)
    toggle(s, x + 14, y + 14, False)
    s.text(x + 62, y + 31, "Can be appointed to evaluation committees", 14, 600, INK)
    by = 1080 / 2 + h / 2 - 76
    s.line(x - 32, by - 14, x + w + 32, by - 14, LINE)
    s.icon("history", x, by + 12, 18, MUTED, 2)
    s.text(x + 28, by + 26, "Recorded in the audit trail · deactivated, never deleted", 13, 500, MUTED)
    button(s, x + w, by, "Add user", "primary", icon="userplus", anchor="end", h=44, target="w60")
    button(s, x + w - 150, by, "Cancel", "secondary", anchor="end", h=44, target="w60")
    return s


def w61_roles():
    s = console("61 Roles & permissions", "Roles & permissions", ["Administration", "Roles & permissions"], "ivan")
    y = page_head(s, "Roles & permissions", "What each role can open and do. The sidebar each person sees comes from "
                  "this matrix.", actions=[("Edit roles", "secondary", "edit", None)])
    roles = [r[0] for r in ROLES if r[0] != "Evaluation Committee Member"]
    short = {"Requester": "Requester", "Head of Department": "Head of dept", "Finance Officer": "Finance",
             "Procurement Officer": "Procurement", "Country Director": "Country Dir.", "Stores / Inspection Officer": "Stores",
             "System Admin": "Admin", "Auditor": "Auditor"}
    # ✓ do · ◐ see only · — none
    D, V, N = "do", "view", "none"
    rows = [
        ("Raise requisitions", [D, D, D, D, D, D, N, N]),
        ("Approve requisitions (by step)", [N, D, D, N, D, N, N, N]),
        ("Prepare budgets and revisions", [N, N, D, N, N, N, N, N]),
        ("Approve budgets and revisions", [N, N, N, N, D, N, N, N]),
        ("See budgets and utilisation", [N, V, D, V, V, N, N, V]),
        ("Review supplier applications", [N, N, N, D, N, N, N, V]),
        ("Prequalify or suspend suppliers", [N, N, N, N, D, N, N, V]),
        ("Send RFQs and compare quotations", [N, N, N, D, V, N, N, V]),
        ("Score evaluations (when appointed)", [D, D, D, D, N, D, N, N]),
        ("Approve awards and sign LPOs", [N, N, N, N, D, N, N, V]),
        ("Record goods received", [N, N, N, N, N, D, N, V]),
        ("Record invoices and payments", [N, N, D, N, N, N, N, V]),
        ("Setup lists", [N, N, V, V, N, N, D, V]),
        ("Users and roles", [N, N, N, N, N, N, D, V]),
        ("Change approval workflows", [N, N, N, N, D, N, D, V]),
        ("Audit trail", [N, N, N, N, V, N, V, V]),
    ]
    s.rect(X0, y, CW, 1060 - y, fill=CARD, rx=16, stroke=LINE, name="matrix")
    lab_w = 420
    colw = (CW - lab_w - 24) / len(roles)
    hy = y + 20
    for i, r in enumerate(roles):
        cx = X0 + lab_w + i * colw
        s.text(cx + colw / 2, hy + 22, short[r], 13, 700, INK, anchor="middle")
        users = {"Requester": 14, "Head of Department": 6, "Finance Officer": 2, "Procurement Officer": 2,
                 "Country Director": 1, "Stores / Inspection Officer": 2, "System Admin": 1, "Auditor": 1}[r]
        s.text(cx + colw / 2, hy + 40, f"{users} user{'s' if users != 1 else ''}", 11.5, 500, MUTED, anchor="middle")
    ry = hy + 58
    rh = (1060 - 20 - 54 - ry) / len(rows)
    for j, (lab, vals) in enumerate(rows):
        if j % 2:
            s.rect(X0 + 1, ry, CW - 2, rh, fill=FIELD_BG)
        s.text(X0 + 24, ry + rh / 2 + 5, lab, 13.5, 600, INK)
        for i, v in enumerate(vals):
            cx = X0 + lab_w + i * colw + colw / 2
            if v == D:
                s.circle(cx, ry + rh / 2, 11, fill=tint(BRAND_M, 0.16))
                s.icon("check", cx - 7, ry + rh / 2 - 7, 14, BRAND_M, 3)
            elif v == V:
                s.icon("eye", cx - 9, ry + rh / 2 - 9, 18, BLUE, 1.9)
            else:
                s.text(cx, ry + rh / 2 + 5, "—", 13, 500, FAINT, anchor="middle")
        ry += rh
    ly = 1060 - 30
    lx = X0 + 24
    s.circle(lx + 10, ly - 5, 9, fill=tint(BRAND_M, 0.16))
    s.icon("check", lx + 4, ly - 11, 12, BRAND_M, 3)
    lx += 26 + s.text(lx + 26, ly, "Can do", 12.5, 600, INK2) + 24
    s.icon("eye", lx, ly - 13, 16, BLUE, 1.9)
    lx += 22 + s.text(lx + 22, ly, "Can see", 12.5, 600, INK2) + 24
    s.text(lx, ly, "—  No access", 12.5, 600, INK2)
    s.text(X1 - 24, ly, "Nobody can approve what they prepared, whatever their role.", 12.5, 700, BRAND_D, anchor="end")
    return s


def w62_workflows():
    s = console("62 Approval workflows", "Approval workflows", ["Administration", "Approval workflows"], "ivan")
    y = page_head(s, "Approval workflows", "Who approves what, in which order. Steps are copied onto each record when it "
                  "is submitted, so a change never affects records already in flight.")
    lw = 1060
    s.rect(X0, y, lw, 1060 - y, fill=CARD, rx=16, stroke=LINE, name="workflows")
    wy = y + 22
    for name, steps in WORKFLOWS.items():
        on = name == "Requisition"
        if on:
            s.rect(X0 + 12, wy - 6, lw - 24, 88, fill=tint(LIME, 0.4), rx=12)
        s.text(X0 + 28, wy + 22, name, 15.5, 700, INK)
        s.text(X0 + 28, wy + 42, f"{len(steps)} step{'s' if len(steps) > 1 else ''}", 12.5, 500, MUTED)
        sx = X0 + 260
        for i, (step, role, above) in enumerate(steps):
            pw = max(tw(step, 13, 700), tw(role, 12, 500), tw(f"only ≥ UGX {above / 1e6:.0f}M", 11.5, 600) if above else 0) + 34
            s.rect(sx, wy + 2, pw, 66, fill=CARD, rx=12, stroke=LINE)
            s.text(sx + 16, wy + 24, step, 13, 700, INK)
            s.text(sx + 16, wy + 42, role, 12, 500, MUTED)
            if above:
                s.text(sx + 16, wy + 59, f"only ≥ UGX {above / 1e6:.0f}M", 11.5, 700, AMBER_D)
            sx += pw
            if i < len(steps) - 1:
                s.icon("arrowright", sx + 6, wy + 26, 16, FAINT, 2)
                sx += 28
        if on:
            button(s, X0 + lw - 28, wy + 16, "Edit", "secondary", icon="edit", anchor="end", h=38, size=13)
            s.link(X0 + 12, wy - 6, lw - 24, 88, "w62b")
        wy += 98
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 360, fill=CARD, rx=16, stroke=LINE, name="methods")
    s.text(rx + 24, y + 40, "Methods by value", 17, 700, INK)
    chip(s, rx + rw - 24, y + 22, "Example thresholds", AMBER_D, anchor="end")
    my = y + 70
    for val, method, quotes, ev in METHODS:
        s.line(rx + 24, my, rx + rw - 24, my, LINE2)
        s.text(rx + 24, my + 28, val, 14, 700, INK)
        s.text(rx + 24, my + 50, method, 13, 600, BRAND)
        s.text(rx + 24, my + 70, f"{quotes} quote{'s' if quotes != '1' else ''} · {ev}", 12.5, 400, MUTED, maxw=rw - 48)
        my += 90
    note(s, rx, y + 380, rw, "These values are placeholders. During inception they are set from IDIU's procurement manual "
         "and each donor's rules.", icon="alert", color=AMBER_D)
    return s


def w62b_edit_workflow():
    s = console("62b Edit workflow: Requisition", "Approval workflows",
                ["Administration", "Approval workflows", "Requisition"], "ivan", owner=True)
    y = page_head(s, "Edit workflow: Requisition", "Your change goes to the Country Director; it applies to "
                  "requisitions submitted after it is approved.",
                  actions=[("Submit change for approval", "primary", "send", "w62"), ("Cancel", "secondary", None, "w62")])
    lw = 1060
    s.rect(X0, y, lw, 620, fill=CARD, rx=16, stroke=LINE, name="steps editor")
    s.text(X0 + 24, y + 40, "Steps, in order", 17, 700, INK)
    steps = [("Department review", "Head of Department", "Always", None),
             ("Funds check", "Finance Officer", "Always", None),
             ("Executive approval", "Country Director", "25,000,000", "30,000,000")]
    sy = y + 64
    for i, (name, role, above, was) in enumerate(steps):
        changed = was is not None
        s.rect(X0 + 24, sy, lw - 48, 112, fill=tint(LIME, 0.35) if changed else FIELD_BG, rx=14,
               stroke=BRAND if changed else None)
        s.icon("menu", X0 + 42, sy + 46, 18, FAINT, 2)
        s.circle(X0 + 86, sy + 55, 15, fill=CARD, stroke=LINE)
        s.text(X0 + 86, sy + 61, str(i + 1), 14, 700, INK, anchor="middle", family="display")
        fw = (lw - 48 - 140 - 60) / 3
        fx = X0 + 120
        field(s, fx, sy + 14, fw, "Step name", name, h=42, size=13.5)
        field(s, fx + fw + 16, sy + 14, fw, "Approver role", role, h=42, size=13.5, dropdown=True)
        if above == "Always":
            field(s, fx + 2 * (fw + 16), sy + 14, fw, "Applies", "Always", h=42, size=13.5, dropdown=True)
        else:
            field(s, fx + 2 * (fw + 16), sy + 14, fw, "Applies from (UGX)", above, h=42, size=13.5, focus=True)
            s.text(fx + 2 * (fw + 16), sy + 100, f"was {was}", 12, 700, AMBER_D)
        s.icon("trash", X0 + lw - 64, sy + 47, 18, RED, 1.9)
        sy += 126
    button(s, X0 + 24, sy + 4, "Add step", "soft", icon="plus", h=40)
    s.line(X0, sy + 64, X0 + lw, sy + 64, LINE2)
    s.text(X0 + 24, sy + 100, "Reason for the change", 13, 600, INK2)
    s.rect(X0 + 24, sy + 112, lw - 48, 52, fill=CARD, rx=10, stroke="#CFD9D2")
    s.text(X0 + 38, sy + 143, "KOICA's 2027 guidelines need executive approval from UGX 25M.", 14, 400, INK)
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 400, fill=CARD, rx=16, stroke=LINE, name="what changes")
    s.text(rx + 24, y + 40, "What this changes", 17, 700, INK)
    s.text(rx + 24, y + 72, "Requisitions from UGX 25M to 30M will need the", 13.5, 500, INK2)
    s.text(rx + 24, y + 92, "Country Director too.", 13.5, 500, INK2)
    s.text(rx + 24, y + 134, "LAST 90 DAYS", 10.5, 700, MUTED, spacing=0.8)
    s.text(rx + 24, y + 172, "3 requisitions", 22, 700, INK, family="display")
    s.text(rx + 24, y + 194, "were between UGX 25M and 30M", 13, 400, MUTED)
    s.line(rx + 24, y + 218, rx + rw - 24, y + 218, LINE2)
    s.text(rx + 24, y + 250, "APPROVAL OF THIS CHANGE", 10.5, 700, MUTED, spacing=0.8)
    avatar(s, rx + 42, y + 286, 17, "SK", AMBER_D)
    s.text(rx + 68, y + 282, "Samuel Kato", 14, 700, INK)
    s.text(rx + 68, y + 301, "Country Director · approves workflow changes", 12.5, 400, MUTED)
    s.text(rx + 24, y + 350, "Requisitions already submitted keep their steps.", 13, 600, BRAND_D)
    note(s, rx, y + 420, rw, "You prepared this change, so you can't approve it: the maker-checker rule covers "
         "workflow changes too.", icon="shield")
    return s


MOD_COLOUR = {"Procurement file": BRAND, "Requisition": BLUE, "Security": RED, "Evaluation": VIOLET, "Budget": TEAL,
              "Delivery": INK2, "Users": BLUE, "Purchase order": BRAND_D}


def _audit_page(viewer="ivan", hl=None):
    s = console("63 Audit trail", "Audit trail", ["Administration", "Audit trail"], viewer)
    y = page_head(s, "Audit trail", "Every recorded action: who did it, to which record, what changed, when and from "
                  "where. Nobody can edit or delete it.", actions=[("Export", "primary", "download", None)])
    rows, links = [], []
    for ev, mod, desc, who, when, ago, outcome in AUDIT:
        rows.append([c_text(ev, INK, 600), c_chip(mod, MOD_COLOUR[mod]), c_text(desc, INK2),
                     c_person(who, False) if who else c_text("Unknown user", MUTED),
                     c_two(when, ago, bold=False), c_status(outcome)])
        links.append("w63b" if ev == "Budget revision approved" else None)
    cols = [("Event", 270, "start"), ("Module", 180, "start"), ("Description", 480, "start"), ("Performed by", 200, "start"),
            ("When", 220, "start"), ("Outcome", 162, "start")]
    list_card(s, y, 78 + 44 + 60 * len(rows) + 58)
    toolbar(s, X0, y, CW, "Search the trail…", filters=["Last 30 days"], export=False)
    end = data_table(s, X0, y + 78, cols, rows, links=links, row_h=60, sort={"When"}, hl=hl)
    pager(s, X0, end, CW, (1, 10), AUDIT_COUNT, pages=1844)
    return s


def w63_audit():
    return _audit_page()


def w63b_audit_entry():
    s = _audit_page(hl=[a[0] for a in AUDIT].index("Budget revision approved"))
    s.title = "63b Audit entry: budget revision approved"
    x, y = drawer(s, 720, "Budget revision approved", "Budget · Tue 22 Sep 2026, 10:14:32", close_target="w63")
    w = 656
    status_chip(s, x, y - 2, "Success")
    chip(s, x + 96, y - 2, "Budget", TEAL)
    y += 44
    facts = [("Who", "Samuel Kato · s.kato@idiu.org · Country Director"), ("Record", "BR-2026-0006 · Head office operations"),
             ("Approval request", "Step 1 of 1 · comment: “Agreed, vehicle repairs are overdue.”")]
    for lab, v in facts:
        s.text(x, y, lab, 12.5, 600, MUTED)
        s.text(x + 150, y, v, 13.5, 600, INK, maxw=w - 150)
        y += 30
    y += 10
    s.text(x, y + 10, "What changed", 16, 700, INK)
    y += 26
    s.rect(x, y, w, 40, fill=FIELD_BG, rx=8)
    for lab, cx in [("FIELD", 14), ("BEFORE", 300), ("AFTER", 480)]:
        s.text(x + cx, y + 25, lab, 10.5, 700, MUTED, spacing=0.7)
    y += 40
    diffs = [("Line 5110 · Office supplies", "18,000,000", "13,500,000"),
             ("Line 5510 · Vehicles & motorcycles", "9,000,000", "13,500,000"),
             ("Budget total", "210,000,000", "210,000,000"),
             ("Status", "Pending approval", "Approved")]
    for lab, a, b in diffs:
        same = a == b
        s.line(x, y, x + w, y, LINE2)
        s.text(x + 14, y + 30, lab, 13.5, 600, INK)
        s.text(x + 300, y + 30, a, 13.5, 500, MUTED if same else RED)
        if not same:
            s.rect(x + 470, y + 10, tw(b, 13.5, 700) + 20, 28, fill=tint(BRAND_M, 0.14), rx=6)
        s.text(x + 480, y + 30, b, 13.5, 700, MUTED if same else BRAND_D)
        y += 48
    y += 20
    s.text(x, y + 10, "Where from", 16, 700, INK)
    y += 34
    where = [("IP address", "102.85.14.72 · Jinja, Uganda"), ("Device", "Chrome 141 on Windows 11"),
             ("Request ID", "01K5RB3Z9T4HQXW2C6JN8VFM0E")]
    for lab, v in where:
        s.text(x, y, lab, 12.5, 600, MUTED)
        if lab == "Request ID":
            ref(s, x + 150, y, v, 12.5, INK2)
        else:
            s.text(x + 150, y, v, 13.5, 600, INK)
        y += 30
    y += 10
    s.rect(x, y, w, 50, fill=FIELD_BG, rx=10)
    s.icon("lock", x + 14, y + 15, 18, BRAND, 2)
    s.text(x + 42, y + 30, "This entry can't be edited or deleted. Corrections are new entries.", 13, 600, INK2)
    button(s, x, y + 76, "View this record's full history", "secondary", icon="history", h=42, target="w31")
    return s


SCREENS = [w60_users, w60b_edit_user, w60c_add_user, w61_roles, w62_workflows, w62b_edit_workflow, w63_audit, w63b_audit_entry]
