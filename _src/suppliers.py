"""Suppliers (w20–w21b), registering (w70–w70c) and the supplier portal (w70d, w71–w77b).

Suppliers sign in at the same door as staff (w00). Busoga Tech (prequalified) lands on w71 and has the full
portal: Home, RFQs, Purchase orders, Payments, Company profile, Documents. Mpumudde (applied, pending) lands on
its application (w70d) and sees only that. Every portal screen is the company's own (owner).

Prequalification is a maker-checker record: the supplier applies in the portal, Procurement reviews and
recommends, the Country Director decides. Only prequalified suppliers in a category can be invited to its
RFQs without a reason (see w12b).
"""
from __future__ import annotations

from data import APPLICATIONS, CATEGORIES, DOC_TYPES, MPUMUDDE, PREQUAL_ROUND, SUPPLIERS
from kit import (AMBER_D, BLUE, BRAND, BRAND_M, CARD, FAINT, FIELD_BG, INK, INK2, LIME, LIME_D, LINE, LINE2,
                 MUTED, RED, TEAL, VIOLET, GREY, avatar, button, checkbox, chip, field, ref, status_chip, tint, tw)
from shell import (approval_panel, CW, H, PCW, PX0, X0, X1, Y0, c_chip, c_money, c_ref, c_status, c_text, c_two, console, data_table,
                   decision_panel, dialog, kv, list_card, note, page_head, pager, portal, record_header, register_frame,
                   stat_card, tabs, toolbar)

CAT_COLOUR = {"ICT": BLUE, "Furniture": BRAND_M, "Printing": TEAL, "Works": VIOLET, "Solar": AMBER_D}


def _m(n):
    return f"{n:,.0f}"


def _cats(cats):
    def f(s_, x, y, w, h):
        cx = x + 14
        for c in cats.split(" · "):
            cx += chip(s_, cx, y + h / 2 - 12, c, CAT_COLOUR.get(c, MUTED)) + 6
    return f


# =====================================================================================
def w20_register():
    s = console("20 Supplier register", "Supplier register", ["Suppliers", "Supplier register"], "ivan")
    y = page_head(s, "Supplier register", "Prequalified suppliers by category. Only they can be invited to an RFQ in "
                  "that category without a reason.", actions=[("Applications · 3 open", "secondary", "fileplus", "w21")])
    rows, links = [], []
    for name, cats, tin, dist, st, until, lpos, val, exp in SUPPLIERS:
        rows.append([c_two(name, f"TIN {tin}"), _cats(cats), c_text(dist, INK2), c_status(st),
                     c_text(until, AMBER_D if st == "Expiring" else INK2), c_two(f"{lpos} LPOs", f"UGX {_m(val)}" if val else "—", bold=False),
                     _docs_cell(exp, st)])
        links.append("w20b" if name.startswith("Busoga Tech") else None)
    cols = [("Supplier", 360, "start"), ("Categories", 210, "start"), ("District", 130, "start"), ("Status", 170, "start"),
            ("Prequalified until", 180, "start"), ("FY 2026", 170, "start"), ("Documents", 292, "start")]
    list_card(s, y, 58 + 78 + 44 + 60 * len(rows) + 58)
    tabs(s, X0 + 24, y + 14, [("All", 47), ("Prequalified", 41), ("Expiring", 4), ("Suspended", 2)], "All")
    toolbar(s, X0, y + 50, CW, "Search by name, TIN or category…", filters=["All categories"])
    end = data_table(s, X0, y + 128, cols, rows, links=links, row_h=60, sort={"Supplier"}, hl=0)
    pager(s, X0, end, CW, (1, 10), 47, pages=5)
    return s


def _docs_cell(expiring, status):
    def f(s_, x, y, w, h):
        if status == "Suspended":
            s_.icon("ban", x + 16, y + h / 2 - 8, 16, RED, 2)
            s_.text(x + 40, y + h / 2 + 5, "Tax clearance not renewed", 13, 600, RED)
        elif expiring:
            s_.icon("alert", x + 16, y + h / 2 - 8, 16, AMBER_D, 2)
            s_.text(x + 40, y + h / 2 + 5, f"{expiring} expiring or expired", 13, 600, AMBER_D)
        else:
            s_.icon("check", x + 16, y + h / 2 - 8, 16, BRAND_M, 2.6)
            s_.text(x + 40, y + h / 2 + 5, "All valid", 13, 500, INK2)
    return f


def w20b_profile():
    s = console("20b Supplier: Busoga Tech Supplies Ltd", "Supplier register",
                ["Suppliers", "Supplier register", "Busoga Tech Supplies Ltd"], "ivan")
    y = record_header(s, Y0, "SUP-0012 · TIN 1003 4721 88", "Busoga Tech Supplies Ltd",
                      chips=[("Prequalified", None, "status"), ("ICT", BLUE, "chip")],
                      facts=[("District", "Jinja"), ("Contact", "Amos Waiswa · 0772 610 224"), ("Since", "2019"),
                             ("Prequalified until", "31 Dec 2026 · approved 12 Jan by Samuel Kato")],
                      actions=[("Edit", "secondary", "edit", None), ("Suspend", "danger", "ban", None)])
    y += 20
    lw = 960
    s.rect(X0, y, lw, 560, fill=CARD, rx=16, stroke=LINE, name="documents")
    s.text(X0 + 24, y + 38, "Documents", 17, 700, INK)
    s.text(X0 + 132, y + 38, "uploaded by the supplier in the portal, checked by Procurement", 13, 400, MUTED)
    docs = [("Certificate of incorporation", "80020001184310", "—", "Valid"), ("TIN certificate", "1003 4721 88", "—", "Valid"),
            ("Trading licence", "Jinja City · 2026", "31 Dec 2026", "Valid"), ("URA tax clearance", "TCC-26-104552", "30 Jun 2027", "Valid"),
            ("Bank letter", "Stanbic Bank, Jinja", "—", "Valid"), ("Company profile & references", "4 references", "—", "Valid"),
            ("Signed declaration of eligibility", "Signed 5 Jan 2026", "This round", "Valid")]
    rows = [[c_text(d, INK, 600), c_text(r, INK2), c_text(e, INK2), c_status(st)] for d, r, e, st in docs]
    cols = [("Document", 330, "start"), ("Reference", 260, "start"), ("Expires", 180, "start"), ("Check", 190, "start")]
    data_table(s, X0, y + 56, cols, rows, row_h=62, check=False)
    rx, rw = X0 + lw + 20, CW - lw - 20
    s.rect(rx, y, rw, 330, fill=CARD, rx=16, stroke=LINE, name="orders")
    s.text(rx + 24, y + 38, "Orders from IDIU", 17, 700, INK)
    s.text(rx + rw - 24, y + 38, "FY 2026 · UGX 58,900,000", 13, 600, MUTED, anchor="end")
    lpos = [("LPO-2026-0051", "10 laptops · Kasese ICT Hub", 36_400_000, "Closed", "w14b"),
            ("LPO-2026-0038", "Network switches · Jinja head office", 9_800_000, "Closed", None),
            ("LPO-2026-0024", "Printers and toner · Kamuli", 7_350_000, "Closed", None),
            ("LPO-2026-0011", "UPS units · Kasese ICT Hub", 5_350_000, "Closed", None)]
    ly = y + 60
    for code, what, v, st, tgt in lpos:
        s.line(rx + 24, ly, rx + rw - 24, ly, LINE2)
        ref(s, rx + 24, ly + 26, code, 13, BRAND if tgt else INK2, 600)
        s.text(rx + 24, ly + 46, what, 13, 500, MUTED, maxw=rw - 220)
        s.text(rx + rw - 24, ly + 26, _m(v), 14, 700, INK, anchor="end")
        status_chip(s, rx + rw - 24, ly + 34, st, h=20, size=11, anchor="end")
        if tgt:
            s.link(rx + 12, ly + 4, rw - 24, 58, tgt)
        ly += 64
    s.rect(rx, y + 350, rw, 210, fill=CARD, rx=16, stroke=LINE, name="performance")
    s.text(rx + 24, y + 388, "Performance", 17, 700, INK)
    stats = [("On time", "4 of 4"), ("Rejected items", "0"), ("RFQs answered", "6 of 7")]
    sw = (rw - 48) / 3
    for i, (lab, v) in enumerate(stats):
        s.text(rx + 24 + i * sw, y + 424, lab, 12.5, 600, MUTED)
        s.text(rx + 24 + i * sw, y + 456, v, 22, 700, INK, family="display")
    s.rect(rx + 24, y + 480, rw - 48, 56, fill=FIELD_BG, rx=10)
    s.para(rx + 38, y + 504, "“Delivered the laptops a week early and installed the screen readers on site.” · Peter Mukasa, 9 Oct",
           rw - 76, 12.5, 500, INK2, lh=18)
    return s


def w21_applications(title="21 Prequalification applications", viewer="ivan", owner=False):
    s = console(title, "Applications", ["Suppliers", "Applications"], viewer, owner=owner)
    y = page_head(s, "Prequalification applications", "Suppliers apply in the supplier portal. Procurement reviews and "
                  "recommends; the Country Director decides.")
    rows, links = [], []
    for name, cats, sub, docs, st, who in APPLICATIONS:
        rows.append([c_text(name, INK, 700), c_text(cats, INK2), c_text(sub, INK2),
                     c_text(docs, RED if docs.split()[0] != docs.split()[-1] else INK2, 600),
                     c_status(st), c_text(who, INK2)])
        links.append("w21c" if name.startswith("Mpumudde") else None)
    cols = [("Supplier", 360, "start"), ("Categories", 280, "start"), ("Submitted", 150, "start"),
            ("Documents", 140, "start"), ("Status", 220, "start"), ("With", 362, "start")]
    list_card(s, y, 58 + 78 + 44 + 62 * len(rows) + 58)
    tabs(s, X0 + 24, y + 14, [("Open", 3), ("Decided", 23), ("All", 26)], "Open")
    toolbar(s, X0, y + 50, CW, "Search applications…", export=False)
    end = data_table(s, X0, y + 128, cols, rows, links=links, row_h=62, hl=0)
    pager(s, X0, end, CW, (1, 6), 26, pages=3, per=6)
    return s


def _application_page(title, active, crumbs, viewer="ivan", decide=False, back="w02"):
    """Mpumudde's application as a full record page. The Country Director decides on his own copy (decide=True),
    reached from My approvals or from Suppliers › Applications; everyone else sees the same page, read only, with
    who it waits on. The menu stays the one the person came from."""
    s = console(title, active, crumbs, viewer, owner=decide)
    m = MPUMUDDE
    y = record_header(s, Y0, "SUP-APP-0142 · applied Tue 6 Oct", m["name"],
                      chips=[("Pending approval", None, "status"), ("Furniture", BRAND_M, "chip")],
                      facts=[("TIN", m["tin"]), ("Address", m["address"]), ("Contact", m["contact"]),
                             ("In business since", m["since"])])
    y += 20
    lw = 1090
    s.rect(X0, y, lw, 470, fill=CARD, rx=16, stroke=LINE, name="documents")
    s.text(X0 + 24, y + 38, "Documents", 17, 700, INK)
    s.text(X0 + 132, y + 38, "7 required for Furniture · all received and checked", 13, 400, MUTED)
    rows = [[c_text(d, INK if st == "Valid" else MUTED, 600), c_text(r, INK2), c_text(e, INK2),
             c_status(st, "Checked" if st == "Valid" else "Replaced by the 2026 licence")]
            for d, r, e, st in m["docs"] if st == "Valid"]
    cols = [("Document", 330, "start"), ("Reference", 260, "start"), ("Expires", 170, "start"), ("Check", 330, "start")]
    data_table(s, X0, y + 56, cols, rows, row_h=49, check=False, size=13)
    y2 = y + 490
    s.rect(X0, y2, lw, 160, fill=CARD, rx=16, stroke=LINE, name="recommendation")
    avatar(s, X0 + 44, y2 + 42, 18, "JW", BRAND)
    s.text(X0 + 72, y2 + 38, "Recommendation · Joseph Waiswa", 15, 700, INK)
    s.text(X0 + 72, y2 + 57, "Procurement Officer · Sat 10 Oct, 15:20", 12.5, 400, MUTED)
    s.para(X0 + 24, y2 + 92, "Prequalify for Furniture until 31 Dec 2026. I visited the workshop on 8 Oct: 14 staff, capacity "
           "about 40 desks a week, three references confirmed. It would give the Kamuli desks RFQ its third prequalified "
           "supplier.", lw - 48, 14, 400, INK2, lh=22)
    if decide:
        decision_panel(s, X0 + lw + 20, y, CW - lw - 20, viewer="samuel", maker="joseph", what="recommendation",
                       comment="Approved for Furniture until 31 Dec 2026.",
                       steps=[("Review and recommendation", "Joseph Waiswa · Sat 10 Oct", "done"),
                              ("Prequalification decision", "Samuel Kato · Country Director", "now")],
                       back=back, approve="Prequalify", h=650)
    else:
        approval_panel(s, X0 + lw + 20, y, CW - lw - 20, 650, [
            ("Submitted by the supplier", "Fatuma Nabirye · Tue 6 Oct, 16:05", "done"),
            ("Review and recommendation", "Joseph Waiswa · Procurement Officer · Sat 10 Oct", "done"),
            ("Prequalification decision", "Samuel Kato · Country Director · waiting 2 days", "now"),
            ("Prequalified for Furniture", "Until 31 Dec 2026", "next")],
            ("Samuel Kato", "Country Director · step 2 of 2 · he decides from My approvals or from here"))
    return s


def w21b_application_review():
    return _application_page("21b Prequalification decision: Mpumudde Furniture Works", "My approvals",
                             ["My approvals", "SUP-APP-0142"], "samuel", decide=True, back="w02")


# ---------------------------------------------------------------- the application, opened from Suppliers › Applications
CRUMBS_APP = ["Suppliers", "Applications", "SUP-APP-0142"]


def w21c_application():
    return _application_page("21c Application: Mpumudde Furniture Works", "Applications", CRUMBS_APP)


def w21c_samuel():
    return _application_page("21c Application: Mpumudde Furniture Works (your decision)", "Applications", CRUMBS_APP,
                             "samuel", decide=True, back="w21")


w21c_samuel.key = "w21c-samuel"

# ---------------------------------------------------------------- registering (nobody signed in yet)
def _portal_steps(s, y, cur):
    steps = ["Company & categories", "Documents & declaration", "Application submitted"]
    sw = PCW / len(steps)
    for i, lab in enumerate(steps):
        sx = PX0 + i * sw
        done, on = i < cur, i == cur
        s.rect(sx, y, sw - 12, 6, fill=BRAND_M if done else (LIME_D if on else LINE), rx=3)
        s.text(sx, y + 30, f"{i + 1}", 13, 700, BRAND_M if done else (LIME_D if on else FAINT), family="display")
        s.text(sx + 18, y + 30, lab, 14, 700 if on else 500, INK if (done or on) else MUTED)


def w70_register():
    s = register_frame("70 Register as a supplier: company and categories (Mpumudde)")
    y = 120
    s.text(PX0, y + 30, "Register as a supplier to IDIU", 32, 700, INK, family="display")
    s.text(PX0, y + 60, "Prequalified suppliers are invited to IDIU's requests for quotations in their categories.",
           15, 400, MUTED)
    _portal_steps(s, y + 90, 0)
    y += 150
    lw = 960
    s.rect(PX0, y, lw, 650, fill=CARD, rx=16, stroke=LINE, name="company")
    x, w = PX0 + 28, lw - 56
    hw = (w - 24) / 2
    s.text(x, y + 40, "Company and your sign-in", 17, 700, INK)
    field(s, x, y + 60, hw, "Registered name", MPUMUDDE["name"], required=True)
    field(s, x + hw + 24, y + 60, hw, "Registration number (URSB)", MPUMUDDE["reg"], required=True, mono=True)
    field(s, x, y + 140, hw, "TIN", MPUMUDDE["tin"], required=True, mono=True, ok="Checked format")
    field(s, x + hw + 24, y + 140, hw, "Email (you sign in with it)", MPUMUDDE["email"], required=True, icon="mail")
    field(s, x, y + 240, hw, "Contact person", "Fatuma Nabirye · 0772 405 118", required=True, icon="user")
    field(s, x + hw + 24, y + 240, hw, "Create a password", "••••••••••", required=True, icon="lock",
          ok="Strong")
    s.line(PX0, y + 350, PX0 + lw, y + 350, LINE2)
    s.text(x, y + 390, "Categories", 17, 700, INK)
    s.text(x, y + 412, "Choose what you supply. Each category lists the documents it needs.", 13, 400, MUTED)
    cy = y + 432
    cw = (w - 36) / 4
    for i, (code, name, *_rest) in enumerate(CATEGORIES):
        on = code == "FUR"
        cx = x + (i % 4) * (cw + 12)
        yy = cy + (i // 4) * 70
        s.rect(cx, yy, cw, 58, fill=tint(LIME, 0.5) if on else CARD, rx=12, stroke=BRAND if on else LINE,
               sw=1.5 if on else 1)
        checkbox(s, cx + 14, yy + 20, on)
        s.text(cx + 42, yy + 26, name, 13.5, 700 if on else 600, INK, maxw=cw - 52)
        s.text(cx + 42, yy + 44, "9 documents" if code == "WRK" else "7 documents", 12, 400, MUTED)
    by = y + 650 - 66
    button(s, PX0 + lw - 28, by, "Continue to documents", "primary", icon="arrowright", anchor="end", target="w70b")
    button(s, PX0 + lw - 270, by, "Back", "secondary", anchor="end", target="!back:w80")
    rx, rw = PX0 + lw + 24, PCW - lw - 24
    s.rect(rx, y, rw, 470, fill=CARD, rx=16, stroke=LINE, name="what you need")
    s.text(rx + 24, y + 40, "What you will need", 17, 700, INK)
    s.text(rx + 24, y + 62, "For Furniture", 13, 400, MUTED)
    dy = y + 92
    for name, expires, validity, req in DOC_TYPES:
        if req == "Construction & works":
            continue
        s.icon("file", rx + 24, dy - 13, 17, BRAND, 1.9)
        s.text(rx + 50, dy, name, 13.5, 600, INK, maxw=rw - 130)
        if expires:
            s.text(rx + rw - 24, dy, "expires", 12, 600, AMBER_D, anchor="end")
        dy += 40
    note(s, rx, y + 490, rw, "IDIU checks every document. You'll be told by email when your application is decided, "
         "and 30 days before a document expires.", icon="mail")
    return s


def w70b_documents():
    s = register_frame("70b Register as a supplier: documents (Mpumudde)")
    y = 120
    s.text(PX0, y + 30, "Upload your documents", 32, 700, INK, family="display")
    s.text(PX0, y + 60, "Mpumudde Furniture Works · Furniture · PDF, JPG or PNG, up to 10 MB each", 15, 400, MUTED)
    _portal_steps(s, y + 90, 1)
    y += 150
    lw = 1100
    s.rect(PX0, y, lw, 640, fill=CARD, rx=16, stroke=LINE, name="documents")
    docs = [("Certificate of incorporation", "Certificate_of_incorporation.pdf", None),
            ("TIN certificate", "TIN_certificate.pdf", None),
            ("Trading licence", "Trading_licence_2026.pdf", "31 Dec 2026"),
            ("URA tax clearance", "URA_TCC_2026.pdf", "30 Jun 2027"),
            ("Bank letter", "Centenary_bank_letter.pdf", None),
            ("Company profile & references", "Mpumudde_profile.pdf", None),
            ("Signed declaration of eligibility", None, None)]
    dy = y + 24
    for name, file, exp in docs:
        s.rect(PX0 + 24, dy, lw - 48, 72, fill=FIELD_BG if file else CARD, rx=12, stroke=LINE if file else BRAND,
               dash=None if file else "5 4")
        s.icon("file", PX0 + 44, dy + 26, 20, BRAND, 1.9)
        s.text(PX0 + 76, dy + 32, name, 14.5, 700, INK)
        s.text(PX0 + 76, dy + 52, file or "Download the form, sign it, upload it", 12.5, 500, MUTED if file else BRAND)
        if exp:
            s.text(PX0 + 640, dy + 32, "Expires", 12, 600, MUTED)
            s.rect(PX0 + 640, dy + 38, 170, 26, fill=CARD, rx=7, stroke="#CFD9D2")
            s.text(PX0 + 652, dy + 56, exp, 12.5, 600, INK)
        if file:
            chip(s, PX0 + lw - 44, dy + 24, "Uploaded", BRAND_M, icon="check", anchor="end")
        else:
            button(s, PX0 + lw - 44, dy + 16, "Upload", "soft", icon="upload", anchor="end", h=38)
        dy += 84
    rx, rw = PX0 + lw + 24, PCW - lw - 24
    s.rect(rx, y, rw, 360, fill=CARD, rx=16, stroke=LINE, name="submit")
    s.text(rx + 24, y + 40, "Declaration", 17, 700, INK)
    checkbox(s, rx + 24, y + 66, True)
    s.para(rx + 54, y + 80, "The information and documents are true. We have no conflict of interest with IDIU staff, "
           "and we are not debarred by PPDA or any donor.", rw - 80, 13.5, 500, INK2, lh=21)
    s.text(rx + 24, y + 180, "6 of 7 documents uploaded", 14, 700, AMBER_D)
    s.text(rx + 24, y + 202, "Upload the signed declaration to submit.", 13, 400, MUTED)
    button(s, rx + 24, y + 236, "Submit application", "primary", icon="send", w=rw - 48, h=46, target="w70c")
    button(s, rx + 24, y + 292, "Back", "secondary", w=rw - 48, h=42, target="w70")
    return s


def w70c_submitted():
    s = register_frame("70c Register as a supplier: application submitted (Mpumudde)")
    _portal_steps(s, 120, 2)
    cx = PX0 + PCW / 2
    s.circle(cx, 260, 48, fill=LIME)
    s.icon("check", cx - 24, 236, 48, LIME_D, 3)
    s.text(cx, 370, "Application submitted", 34, 700, INK, anchor="middle", family="display")
    s.text(cx, 406, "Mpumudde Furniture Works · Furniture · Tue 6 Oct 2026, 16:05", 15, 500, MUTED, anchor="middle")
    ref(s, cx, 436, "Reference SUP-APP-0142", 14, BRAND, 600, anchor="middle")
    bw = 900
    bx = cx - bw / 2
    s.rect(bx, 476, bw, 300, fill=CARD, rx=18, stroke=LINE, name="what happens next")
    s.text(bx + 32, 520, "What happens next", 18, 700, INK)
    steps = [("Submitted", "Tue 6 Oct · all 7 documents received", "done"),
             ("Review by IDIU Procurement", "Documents checked, and a visit to your workshop", "next"),
             ("Decision by the Country Director", "You will get an email either way", "next"),
             ("Prequalified for Furniture", "You start receiving IDIU's furniture RFQs", "next")]
    sy = 562
    for i, (lab, sub, st) in enumerate(steps):
        if i < len(steps) - 1:
            s.line(bx + 50, sy + 14, bx + 50, sy + 46, LINE, 2)
        if st == "done":
            s.circle(bx + 50, sy, 12, fill=BRAND_M)
            s.icon("check", bx + 43, sy - 7, 14, "#FFFFFF", 3)
        else:
            s.circle(bx + 50, sy, 10, fill=CARD, stroke="#C2CEC6", sw=2)
        s.text(bx + 76, sy + 5, lab, 15, 700, INK if st == "done" else INK2)
        s.text(bx + 76 + tw(lab, 15, 700) + 12, sy + 5, sub, 13, 400, MUTED)
        sy += 52
    s.text(cx, 812, "Your account is ready: sign in with sales@mpumuddefurniture.ug to follow your application.",
           14, 500, INK2, anchor="middle")
    button(s, cx - 12, 846, "Back to home", "secondary", anchor="end", h=44, target="w80")
    button(s, cx + 12, 846, "Follow my application", "primary", icon="arrowright", h=44, target="w70d")
    return s


# ---------------------------------------------------------------- the applicant, signed in (Mpumudde)
def w70d_application_status():
    s = portal("70d Supplier portal: My application (Mpumudde)", "My application", "mpumudde")
    m = MPUMUDDE
    y = page_head(s, "Your application", ref_line=("SUP-APP-0142", f"{m['name']} · Furniture · submitted Tue 6 Oct 2026"))
    status_chip(s, X1, Y0 + 14, "Pending approval", label="With the Country Director", anchor="end")
    lw = 1000
    s.rect(X0, y, lw, 274, fill=CARD, rx=16, stroke=LINE, name="where it is")
    s.text(X0 + 28, y + 42, "Where your application is", 17, 700, INK)
    steps = [("Submitted", "Tue 6 Oct · 7 of 7 documents", "done"),
             ("Reviewed by Procurement", "Sat 10 Oct · recommended", "done"),
             ("Country Director's decision", "Waiting since Sat 10 Oct", "now"),
             ("Prequalified for Furniture", "RFQs start coming to you", "next")]
    sw = (lw - 56) / len(steps)
    ty = y + 104
    for i, (lab, sub, st) in enumerate(steps):
        sx = X0 + 28 + i * sw
        if i < len(steps) - 1:
            s.line(sx + 26, ty, sx + sw - 4, ty, BRAND_M if st == "done" else LINE, 3)
        if st == "done":
            s.circle(sx + 12, ty, 13, fill=BRAND_M)
            s.icon("check", sx + 4, ty - 8, 16, "#FFFFFF", 3)
        elif st == "now":
            s.circle(sx + 12, ty, 13, fill=LIME, stroke=LIME_D, sw=2)
            s.circle(sx + 12, ty, 5, fill=LIME_D)
        else:
            s.circle(sx + 12, ty, 11, fill=CARD, stroke="#C2CEC6", sw=2)
        s.text(sx, ty + 44, lab, 14.5, 700, INK if st != "next" else INK2, maxw=sw - 12)
        s.text(sx, ty + 64, sub, 12.5, 400, AMBER_D if st == "now" else MUTED, maxw=sw - 12)
    note(s, X0 + 28, y + 206, lw - 56, "IDIU Procurement visited your workshop on 8 Oct and recommended you for Furniture. "
         "You'll get an email as soon as the Country Director decides.", icon="info")
    y2 = y + 294
    s.rect(X0, y2, lw, 1050 - y2, fill=CARD, rx=16, stroke=LINE, name="documents")
    s.text(X0 + 28, y2 + 40, "Your documents", 17, 700, INK)
    s.text(X0 + 172, y2 + 40, "all 7 checked by IDIU", 13, 400, MUTED)
    rows = [[c_text(d, INK, 600), c_text(r, INK2), c_text(e, INK2), c_status(st, "Checked")]
            for d, r, e, st in m["docs"] if st == "Valid"]
    cols = [("Document", 360, "start"), ("Reference", 260, "start"), ("Expires", 190, "start"), ("Check", lw - 810, "start")]
    data_table(s, X0, y2 + 60, cols, rows, row_h=52, check=False, size=13)
    rx, rw = X0 + lw + 24, CW - lw - 24
    s.rect(rx, y, rw, 380, fill=CARD, rx=16, stroke=LINE, name="company")
    s.text(rx + 24, y + 42, "Company", 17, 700, INK)
    fy = y + 84
    for lab, v in [("Registered name", m["name"]), ("TIN", m["tin"]), ("Registration", m["reg"]),
                   ("Address", m["address"]), ("Contact", m["contact"]), ("Email", m["email"])]:
        kv(s, rx + 24, fy, rw - 48, lab, v, mono=lab in ("TIN", "Registration"))
        s.line(rx + 24, fy + 18, rx + rw - 24, fy + 18, LINE2)
        fy += 48
    s.rect(rx, y + 400, rw, 1050 - y - 400, fill=CARD, rx=16, stroke=LINE, name="when prequalified")
    s.text(rx + 24, y + 442, "When you're prequalified", 17, 700, INK)
    opens = [("send", "Requests for quotations", "IDIU's furniture RFQs come to this portal"),
             ("receipt", "Purchase orders", "Acknowledge LPOs and follow deliveries"),
             ("banknote", "Payments", "See each payment reference Finance records"),
             ("bell", "Reminders", "30 days before any document expires")]
    oy = y + 478
    for ic, a, b in opens:
        s.rect(rx + 24, oy, 40, 40, fill=tint(BRAND, 0.08), rx=11)
        s.icon(ic, rx + 34, oy + 10, 20, BRAND, 2)
        s.text(rx + 78, oy + 17, a, 14.5, 700, INK)
        s.text(rx + 78, oy + 36, b, 12.5, 400, MUTED, maxw=rw - 102)
        oy += 62
    return s


# ---------------------------------------------------------------- the supplier portal (Busoga Tech, signed in)
BUSOGA_LPOS = [  # lpo, what, project, value, issued, delivered, invoice, invoiced, paid, eft, voucher, target
    ("LPO-2026-0051", "10 laptops for training room 2", "Kasese ICT Hub", 36_400_000, "Tue 6 Oct", "Fri 9 Oct · 10 of 10",
     "BTS-INV-0912", "Mon 12 Oct", "Mon 12 Oct", "EFT-STB-26-10-0331", "PV-2026-1184", "w74b"),
    ("LPO-2026-0038", "Network switches", "Head office operations", 9_800_000, "Tue 11 Aug", "Fri 21 Aug · 6 of 6",
     "BTS-INV-0841", "Tue 25 Aug", "Fri 4 Sep", "EFT-STB-26-09-0112", "PV-2026-0967", None),
    ("LPO-2026-0024", "Printers and toner", "Teacher ICT Initiative, Kamuli", 7_350_000, "Wed 17 Jun",
     "Tue 30 Jun · 12 of 12", "BTS-INV-0763", "Thu 2 Jul", "Wed 15 Jul", "EFT-STB-26-07-0208", "PV-2026-0712", None),
    ("LPO-2026-0011", "UPS units", "Kasese ICT Hub", 5_350_000, "Mon 2 Mar", "Thu 12 Mar · 8 of 8",
     "BTS-INV-0602", "Mon 16 Mar", "Thu 2 Apr", "EFT-STB-26-04-0057", "PV-2026-0263", None),
]
BUSOGA_RFQS = [  # rfq, what, deliver to, closes, your quote, result, target
    ("RFQ-2026-0035", "Network switches and cabling", "Kamuli field office", "Wed 14 Oct, 12:00", "Draft saved", "Open", "w72"),
    ("RFQ-2026-0031", "10 laptops for training room 2", "Kasese ICT Hub", "Closed 28 Sep", "36,400,000", "Awarded to you", "w74b"),
    ("RFQ-2026-0026", "Projectors for the Kamuli ICT centre", "Kamuli field office", "Closed 7 Sep", "8,900,000", "Not awarded", None),
    ("RFQ-2026-0019", "Network switches, Jinja head office", "Jinja head office", "Closed 3 Aug", "9,800,000", "Awarded to you", None),
    ("RFQ-2026-0015", "Tablets for teacher trainers", "Kamuli field office", "Closed 20 Jul", "Did not quote", "Closed", None),
    ("RFQ-2026-0012", "Printers and toner", "Kamuli field office", "Closed 8 Jun", "7,350,000", "Awarded to you", None),
    ("RFQ-2026-0007", "CCTV for Jinja head office", "Jinja head office", "Closed 22 Apr", "12,600,000", "Not awarded", None),
    ("RFQ-2026-0004", "UPS units", "Kasese ICT Hub", "Closed 24 Feb", "5,350,000", "Awarded to you", None),
]
RESULT_COLOUR = {"Open": BRAND_M, "Awarded to you": BRAND, "Not awarded": GREY, "Closed": GREY}
PAID_TOTAL = sum(l[3] for l in BUSOGA_LPOS)


def _renew_banner(s, y, target="w77b"):
    s.rect(X0, y, CW, 64, fill=tint(LIME, 0.55), rx=14, stroke="#B9DB8C", name="renewal banner")
    s.icon("award", X0 + 22, y + 21, 22, LIME_D, 2)
    s.text(X0 + 56, y + 29, f"Prequalification for {PREQUAL_ROUND['year']} is open", 15, 700, INK)
    s.text(X0 + 56, y + 48, "Renew by Fri 20 Nov: sign this year's declaration; your other documents carry over.",
           13, 500, INK2)
    button(s, X1 - 20, y + 12, "Renew for 2027", "primary", icon="arrowright", anchor="end", h=40, target=target)


def w71_supplier_home():
    s = portal("71 Supplier portal: Home (Busoga Tech Supplies)", "Home", crumbs=["Home"])
    s.text(X0, Y0 + 34, "Good morning, Amos", 30, 700, INK, family="display")
    s.text(X0, Y0 + 62, "Monday, 12 October 2026 · Busoga Tech Supplies Ltd · prequalified for ICT until 31 Dec 2026",
           14.5, 400, MUTED)
    y = Y0 + 88
    _renew_banner(s, y)
    y += 84
    gw = (CW - 60) / 4
    cards = [("send", BRAND, "Open RFQs for you", "1", "RFQ-2026-0035 closes Wed 14 Oct", "w73"),
             ("receipt", TEAL, "Purchase orders", "4", "FY 2026 · all delivered", "w74"),
             ("banknote", BRAND_M, "Paid this year", f"UGX {PAID_TOTAL / 1e6:.1f}M", "4 of 4 LPOs paid", "w75"),
             ("file", BLUE, "Documents", "All valid", "Declaration renews for 2027", "w77")]
    for i, (ic, col, lab, v, sub, tgt) in enumerate(cards):
        stat_card(s, X0 + i * (gw + 20), y, gw, 128, ic, col, lab, v, sub=sub, value_size=30, target=tgt, help=False)
    y += 148
    lw = 1000
    s.rect(X0, y, lw, 206, fill=CARD, rx=16, stroke=LINE, name="open rfq")
    s.text(X0 + 24, y + 40, "Waiting for your quotation", 17, 700, INK)
    w = s.text(X0 + lw - 24, y + 40, "All RFQs →", 13, 700, BRAND, anchor="end")
    s.link(X0 + lw - 34 - w, y + 20, w + 20, 30, "w73")
    s.rect(X0 + 24, y + 62, lw - 48, 120, fill=tint(LIME, 0.4), rx=14, stroke="#B9DB8C")
    ref(s, X0 + 48, y + 98, "RFQ-2026-0035", 14, BRAND, 600)
    s.text(X0 + 190, y + 98, "Network switches and cabling · Kamuli ICT centre", 15, 700, INK)
    s.text(X0 + 48, y + 124, "4 managed switches, 20 boxes of Cat6, installation · deliver to Kamuli field office",
           13, 400, INK2)
    s.text(X0 + 48, y + 150, "Closes Wed 14 Oct 2026, 12:00 · 2 days left · draft saved", 13, 700, AMBER_D)
    button(s, X0 + lw - 48, y + 100, "Submit quotation", "primary", icon="send", anchor="end", target="w72")
    rx, rw = X0 + lw + 24, CW - lw - 24
    s.rect(rx, y, rw, 206, fill=CARD, rx=16, stroke=LINE, name="latest payment")
    s.text(rx + 24, y + 40, "Latest payment", 17, 700, INK)
    w = s.text(rx + rw - 24, y + 40, "Payments →", 13, 700, BRAND, anchor="end")
    s.link(rx + rw - 34 - w, y + 20, w + 20, 30, "w75")
    s.text(rx + 24, y + 98, "UGX 36,400,000", 28, 700, INK, family="display")
    status_chip(s, rx + rw - 24, y + 76, "Paid", anchor="end")
    s.text(rx + 24, y + 128, "LPO-2026-0051 · paid Mon 12 Oct, 09:38", 13.5, 500, INK2)
    ref(s, rx + 24, y + 156, "EFT-STB-26-10-0331", 13, BRAND, 600)
    s.text(rx + 24, y + 180, "Stanbic Bank · check it against your statement", 12.5, 400, MUTED)
    y += 226
    s.rect(X0, y, CW, 1050 - y, fill=CARD, rx=16, stroke=LINE, name="orders")
    s.text(X0 + 24, y + 40, "Purchase orders from IDIU", 17, 700, INK)
    w = s.text(X1 - 24, y + 40, "All purchase orders →", 13, 700, BRAND, anchor="end")
    s.link(X1 - 34 - w, y + 20, w + 20, 30, "w74")
    rows, links = [], []
    for lpo, what, proj, v, iss, dl, inv, invd, paid, eft, pv, tgt in BUSOGA_LPOS:
        rows.append([c_ref(lpo, f"{what} · {proj}"), c_money(v), c_text(f"Delivered {dl}", INK2),
                     c_two(f"Paid {paid}", eft, bold=False), c_status("Paid")])
        links.append(tgt)
    cols = [("LPO", 520, "start"), ("Value (UGX)", 190, "end"), ("Delivery", 330, "start"), ("Payment", 320, "start"),
            ("Status", CW - 1360, "start")]
    data_table(s, X0, y + 60, cols, rows, links=links, row_h=58, check=False)
    return s


def w72_quotation():
    s = portal("72 Supplier portal: Submit quotation RFQ-2026-0035", "RFQs", crumbs=["RFQs", "RFQ-2026-0035"])
    y = page_head(s, "Submit your quotation", ref_line=("RFQ-2026-0035", "Network switches and cabling · closes Wed 14 Oct "
                  "2026, 12:00"), actions=[("Submit quotation", "primary", "send", "w73"), ("Save draft", "secondary", None, "w73")])
    lw = 1060
    s.rect(X0, y, lw, 640, fill=CARD, rx=16, stroke=LINE, name="prices")
    s.text(X0 + 24, y + 38, "Your prices", 17, 700, INK)
    s.text(X0 + 140, y + 38, "in UGX, VAT shown separately", 13, 400, MUTED)
    # under the requisition's UGX 14.2M estimate (PR-2026-0093)
    items = [("24-port managed switch, PoE+", 4, "Piece", 1_450_000), ("Cat6 cable, 305 m box", 20, "Box", 185_000),
             ("Patch panels, faceplates and installation", 1, "Lot", 1_100_000)]
    sub = sum(q * p for _, q, _, p in items)
    rows = [[c_text(d, INK, 600), c_text(str(q)), c_text(u, INK2), _price_cell(p), c_text(_m(q * p), INK, 700)]
            for d, q, u, p in items]
    cols = [("Item (from the RFQ)", 440, "start"), ("Qty", 80, "start"), ("Unit", 100, "start"), ("Unit price", 220, "start"),
            ("Amount", 220, "start")]
    end = data_table(s, X0, y + 56, cols, rows, row_h=64, check=False)
    ty = end + 24
    for lab, v, bold in [("Subtotal", sub, False), ("VAT 18%", round(sub * 0.18), False), ("Total", round(sub * 1.18), True)]:
        s.text(X0 + lw - 260, ty, lab, 14, 700 if bold else 500, INK if bold else INK2, anchor="end")
        s.text(X0 + lw - 24, ty, _m(v), 16 if bold else 14, 700, INK, anchor="end", family="display" if bold else "body")
        ty += 30
    ty += 10
    tw3 = (lw - 48 - 48) / 3
    field(s, X0 + 24, ty, tw3, "Delivery", "10", required=True, suffix="days after LPO")
    field(s, X0 + 48 + tw3, ty, tw3, "Warranty", "3", required=True, suffix="years")
    field(s, X0 + 72 + 2 * tw3, ty, tw3, "Prices valid until", "13 Dec 2026", required=True, icon="calendar")
    rx, rw = X0 + lw + 24, CW - lw - 24
    s.rect(rx, y, rw, 330, fill=CARD, rx=16, stroke=LINE, name="attachments")
    s.text(rx + 24, y + 38, "Attachments", 17, 700, INK)
    for i, name in enumerate(["Quotation BTS-Q-2210.pdf", "Switch datasheet.pdf"]):
        s.rect(rx + 24, y + 58 + i * 52, rw - 48, 42, fill=FIELD_BG, rx=10)
        s.icon("paperclip", rx + 36, y + 70 + i * 52, 18, BRAND, 2)
        s.text(rx + 62, y + 84 + i * 52, name, 13.5, 600, INK)
    s.rect(rx + 24, y + 170, rw - 48, 44, fill=CARD, rx=10, stroke="#CFD9D2", dash="5 4")
    s.text(rx + rw / 2, y + 197, "Add a file", 13.5, 600, BRAND, anchor="middle")
    checkbox(s, rx + 24, y + 238, True)
    s.para(rx + 54, y + 252, "We confirm the prices and terms, and have no conflict of interest with IDIU staff.",
           rw - 80, 13, 500, INK2, lh=20)
    note(s, rx, y + 350, rw, "Quotations stay sealed until the RFQ closes: IDIU opens them all together at 12:00 on "
         "Wed 14 Oct.", icon="lock")
    return s


def _price_cell(p):
    def f(s_, x, y, w, h):
        s_.rect(x + 14, y + h / 2 - 19, w - 40, 38, fill=CARD, rx=8, stroke="#CFD9D2")
        s_.text(x + 28, y + h / 2 + 5, f"{p:,.0f}", 14, 600, INK)
    return f


def w73_rfqs():
    s = portal("73 Supplier portal: Requests for quotations", "RFQs", crumbs=["RFQs"])
    y = page_head(s, "Requests for quotations", "Sent to you because you are prequalified for ICT. Quotations stay "
                  "sealed until the RFQ closes.")
    rows, links = [], []
    for rfq, what, to, closes, quote, result, tgt in BUSOGA_RFQS:
        rows.append([c_ref(rfq, what), c_text(to, INK2),
                     c_text(closes, AMBER_D if result == "Open" else INK2, 700 if result == "Open" else 400),
                     c_text(quote, MUTED if quote[0].isalpha() else INK, 400 if quote[0].isalpha() else 700),
                     c_chip(result, RESULT_COLOUR[result], solid=result == "Awarded to you")])
        links.append(tgt)
    cols = [("RFQ", 520, "start"), ("Deliver to", 280, "start"), ("Closes", 230, "start"),
            ("Your quotation (UGX)", 250, "start"), ("Result", CW - 1280, "start")]
    list_card(s, y, 58 + 78 + 44 + 58 * len(rows) + 58)
    tabs(s, X0 + 24, y + 14, [("All", 8), ("Open", 1), ("Past", 7)], "All")
    toolbar(s, X0, y + 50, CW, "Search RFQs…", export=False)
    end = data_table(s, X0, y + 128, cols, rows, links=links, row_h=58, check=False, hl=0)
    pager(s, X0, end, CW, (1, 8), 8, pages=1)
    return s


def w74_purchase_orders():
    s = portal("74 Supplier portal: Purchase orders", "Purchase orders", crumbs=["Purchase orders"])
    y = page_head(s, "Purchase orders", "LPOs IDIU has issued to you. Acknowledge each one, deliver, then invoice "
                  "against it.")
    rows, links = [], []
    for lpo, what, proj, v, iss, dl, inv, invd, paid, eft, pv, tgt in BUSOGA_LPOS:
        rows.append([c_ref(lpo, what), c_text(proj, INK2), c_money(v), c_text(iss, INK2), c_text(dl, INK2),
                     c_status("Paid")])
        links.append(tgt)
    cols = [("LPO", 420, "start"), ("For", 330, "start"), ("Value (UGX)", 200, "end"), ("Issued", 170, "start"),
            ("Delivered", 250, "start"), ("Status", CW - 1370, "start")]
    list_card(s, y, 58 + 78 + 44 + 62 * len(rows) + 58)
    tabs(s, X0 + 24, y + 14, [("All", 4), ("To acknowledge", 0), ("To deliver", 0), ("Paid", 4)], "All")
    toolbar(s, X0, y + 50, CW, "Search LPOs…")
    end = data_table(s, X0, y + 128, cols, rows, links=links, row_h=62, check=False, hl=0)
    pager(s, X0, end, CW, (1, 4), 4, pages=1)
    note(s, X0, end + 80, CW, "When IDIU issues an LPO you get an email; it shows here under \"To acknowledge\" until "
         "you accept its prices, quantities and delivery date.", icon="info")
    return s


def w74b_lpo():
    s = portal("74b Supplier portal: LPO-2026-0051", "Purchase orders", crumbs=["Purchase orders", "LPO-2026-0051"])
    y = page_head(s, "LPO-2026-0051", ref_line=("PR-2026-0087", "10 laptops for training room 2 · Kasese ICT Hub · "
                  "UGX 36,400,000"), actions=[("Download PDF", "secondary", "download", None)])
    lw, ch = 1000, 640
    s.rect(X0, y, lw, ch, fill=CARD, rx=16, stroke=LINE, name="order")
    s.text(X0 + 28, y + 42, "The order", 17, 700, INK)
    status_chip(s, X0 + lw - 28, y + 24, "Paid", anchor="end")
    blocks = [("From", ["International Development Institute Uganda", "Plot 45 Wilson Avenue, Jinja"]),
              ("Deliver to", ["Kasese ICT Hub, training room 2", "Kasese field office · by Fri 16 Oct"]),
              ("Reference", ["RFQ-2026-0031 · your quote 36,400,000", "Issued Tue 6 Oct 2026, 11:30"])]
    bw = (lw - 56) / 3
    for i, (lab, lines) in enumerate(blocks):
        bx = X0 + 28 + i * bw
        s.text(bx, y + 84, lab.upper(), 10.5, 700, MUTED, spacing=0.8)
        for j, ln in enumerate(lines):
            s.text(bx, y + 108 + j * 20, ln, 13, 700 if j == 0 else 400, INK if j == 0 else INK2, maxw=bw - 16)
    rows = [[c_two("Laptop, Core i5 (13th gen), 16 GB, 512 GB SSD, 14\"", "Windows 11 Pro, screen-reader ready, 3-year warranty"),
             c_text("10"), c_text("Piece", INK2), c_money(3_084_746, bold=False), c_money(30_847_458)]]
    cols = [("Item", 470, "start"), ("Qty", 80, "start"), ("Unit", 100, "start"), ("Unit price", 170, "end"),
            ("Amount (UGX)", lw - 820, "end")]
    end = data_table(s, X0, y + 164, cols, rows, row_h=66, check=False)
    ty = end + 34
    for lab, v, bold in [("Subtotal", "30,847,458", False), ("VAT 18%", "5,552,542", False), ("Total", "36,400,000", True)]:
        s.text(X0 + lw - 220, ty, lab, 14, 700 if bold else 500, INK if bold else INK2, anchor="end")
        s.text(X0 + lw - 28, ty, v, 16 if bold else 14, 700, INK, anchor="end", family="display" if bold else "body")
        ty += 30
    s.para(X0 + 28, ty + 20, "Terms: delivery within 10 days; payment 30 days after accepted delivery against this LPO, "
           "the goods received note and a tax invoice; 3-year warranty; screen readers installed.", lw - 56, 13.5, 400,
           MUTED, lh=21)
    s.rect(X0 + 28, ty + 76, lw - 56, 64, fill=tint(BRAND_M, 0.08), rx=12)
    s.icon("check", X0 + 46, ty + 97, 22, BRAND_M, 2.6)
    s.text(X0 + 80, ty + 104, "You acknowledged this LPO on Tue 6 Oct, 14:02", 14.5, 700, INK)
    s.text(X0 + 80 + tw("You acknowledged this LPO on Tue 6 Oct, 14:02", 14.5, 700) + 12, ty + 104,
           "Amos Waiswa · accepted prices, quantities and delivery date", 13, 400, MUTED)
    rx, rw = X0 + lw + 24, CW - lw - 24
    s.rect(rx, y, rw, ch, fill=CARD, rx=16, stroke=LINE, name="progress")
    s.text(rx + 24, y + 42, "Progress", 17, 700, INK)
    track = [("Issued by IDIU", "Tue 6 Oct, 11:30 · Joseph Waiswa", None),
             ("Acknowledged by you", "Tue 6 Oct, 14:02 · Amos Waiswa", None),
             ("Delivered to Kasese", "Fri 9 Oct, 14:15 · delivery note DN-4471", None),
             ("Inspected and accepted", "10 of 10 · GRN-2026-0064", None),
             ("Invoice received", "Mon 12 Oct, 09:12 · BTS-INV-0912", None),
             ("Paid", "Mon 12 Oct, 09:38 · EFT-STB-26-10-0331", "w75")]
    ty = y + 92
    for i, (lab, sub, tgt) in enumerate(track):
        if i < len(track) - 1:
            s.line(rx + 38, ty + 14, rx + 38, ty + 62, tint(BRAND_M, 0.4), 2)
        s.circle(rx + 38, ty, 12, fill=BRAND_M)
        s.icon("check", rx + 31, ty - 7, 14, "#FFFFFF", 3)
        s.text(rx + 64, ty + 5, lab, 15, 700, INK)
        s.text(rx + 64, ty + 26, sub, 13, 400, MUTED, maxw=rw - 90)
        if tgt:
            w = s.text(rx + rw - 24, ty + 5, "Payments →", 13, 700, BRAND, anchor="end")
            s.link(rx + rw - 34 - w, ty - 15, w + 20, 30, tgt)
        ty += 76
    note(s, rx + 24, ty + 4, rw - 48, "Acknowledging an LPO confirms you accept it. IDIU records delivery and payment; "
         "you see each step here.", icon="info")
    return s


def w75_payments():
    s = portal("75 Supplier portal: Payments", "Payments", crumbs=["Payments"])
    y = page_head(s, "Payments", "What IDIU has paid you, with the reference Finance recorded for each transfer.")
    gw = (CW - 40) / 3
    cards = [("banknote", BRAND_M, "Paid this year", f"UGX {_m(PAID_TOTAL)}", "4 payments · FY 2026"),
             ("clock", AMBER_D, "Waiting for payment", "UGX 0", "Nothing outstanding"),
             ("calendar", TEAL, "Delivery to payment", "13 days", "average this year; terms are 30 days")]
    for i, (ic, col, lab, v, sub) in enumerate(cards):
        stat_card(s, X0 + i * (gw + 20), y, gw, 128, ic, col, lab, v, sub=sub, value_size=30, help=False)
    y += 148
    rows, links = [], []
    for lpo, what, proj, v, iss, dl, inv, invd, paid, eft, pv, tgt in BUSOGA_LPOS:
        rows.append([c_ref(eft, f"Voucher {pv}", BRAND), c_ref(lpo, what), c_text(inv, INK2, mono=True), c_money(v),
                     c_two(paid, f"invoiced {invd}", bold=False), c_status("Paid")])
        links.append(tgt)
    cols = [("Payment reference", 320, "start"), ("LPO", 380, "start"), ("Your invoice", 220, "start"),
            ("Amount (UGX)", 200, "end"), ("Paid", 230, "start"), ("Status", CW - 1350, "start")]
    list_card(s, y, 58 + 78 + 44 + 62 * len(rows) + 58 - 58)
    s.text(X0 + 24, y + 40, "Payments received", 17, 700, INK)
    toolbar(s, X0, y + 50, CW, "Search payments…")
    end = data_table(s, X0, y + 128, cols, rows, links=links, row_h=62, check=False)
    note(s, X0, end + 28, CW, "IDIU pays by bank transfer from the project's account. This portal shows the reference "
         "Finance recorded; it does not move money. Check each reference against your bank statement.", icon="info")
    return s


def w76_company_profile():
    s = portal("76 Supplier portal: Company profile", "Company profile", crumbs=["Company profile"])
    y = record_header(s, Y0, "SUP-0012 · TIN 1003 4721 88", "Busoga Tech Supplies Ltd",
                      chips=[("Prequalified", None, "status"), ("ICT", BLUE, "chip")],
                      facts=[("District", "Jinja"), ("In business since", "2019"),
                             ("Prequalified until", "31 Dec 2026 · approved 12 Jan by IDIU")],
                      actions=[("Request a change", "secondary", "edit", None)])
    y += 20
    cw3 = (CW - 48) / 3
    x = X0
    s.rect(x, y, cw3, 600, fill=CARD, rx=16, stroke=LINE, name="company details")
    s.text(x + 24, y + 42, "Company details", 17, 700, INK)
    fy = y + 86
    for lab, v in [("Registered name", "Busoga Tech Supplies Ltd"), ("Registration", "80020001184310"),
                   ("TIN", "1003 4721 88"), ("Address", "Plot 9 Main Street, Jinja"), ("Phone", "0772 610 224"),
                   ("Email", "sales@busogatech.co.ug"), ("Category", "ICT equipment & services")]:
        kv(s, x + 24, fy, cw3 - 48, lab, v, mono=lab in ("Registration", "TIN"))
        s.line(x + 24, fy + 18, x + cw3 - 24, fy + 18, LINE2)
        fy += 52
    x += cw3 + 24
    s.rect(x, y, cw3, 600, fill=CARD, rx=16, stroke=LINE, name="bank account")
    s.text(x + 24, y + 42, "Bank account for payments", 17, 700, INK)
    fy = y + 86
    for lab, v in [("Bank", "Stanbic Bank Uganda"), ("Branch", "Jinja"), ("Account name", "Busoga Tech Supplies Ltd"),
                   ("Account number", "•••• •••• 4417"), ("Confirmed by IDIU", "Tue 6 Jan 2026")]:
        kv(s, x + 24, fy, cw3 - 48, lab, v, mono=lab == "Account number")
        s.line(x + 24, fy + 18, x + cw3 - 24, fy + 18, LINE2)
        fy += 52
    note(s, x + 24, fy + 6, cw3 - 48, "A change to bank details is checked by IDIU Procurement and approved before any "
         "payment uses it.", icon="shield")
    x += cw3 + 24
    s.rect(x, y, cw3, 600, fill=CARD, rx=16, stroke=LINE, name="people")
    s.text(x + 24, y + 42, "People on this account", 17, 700, INK)
    people = [("AW", BRAND, "Amos Waiswa", "Director · account owner", "Signed in now"),
              ("SN", TEAL, "Sarah Nambi", "Sales · quotations only", "Last seen Fri 9 Oct")]
    py = y + 76
    for ini, col, nm, role, seen in people:
        s.line(x + 24, py, x + cw3 - 24, py, LINE2)
        avatar(s, x + 46, py + 38, 19, ini, col, solid=True)
        s.text(x + 76, py + 33, nm, 14.5, 700, INK)
        s.text(x + 76, py + 53, role, 12.5, 400, MUTED)
        s.text(x + cw3 - 24, py + 43, seen, 12.5, 600, BRAND_M if seen.startswith("Signed") else MUTED, anchor="end")
        py += 76
    button(s, x + 24, py + 16, "Add a person", "soft", icon="userplus", h=40)
    dy = y + 624
    s.rect(X0, dy, CW, 72, fill=CARD, rx=16, stroke=LINE, name="documents link")
    s.icon("file", X0 + 24, dy + 25, 22, BRAND, 2)
    s.text(X0 + 58, dy + 43, "Documents", 16, 700, INK)
    s.text(X0 + 58 + tw("Documents", 16, 700) + 14, dy + 43, "7 on file, all valid · the declaration renews for 2027",
           13.5, 400, MUTED)
    w = s.text(X1 - 24, dy + 43, "Open documents →", 13.5, 700, BRAND, anchor="end")
    s.link(X1 - 34 - w, dy + 20, w + 20, 32, "w77")
    return s


BUSOGA_DOCS = [  # document, reference, expires, status, note
    ("Certificate of incorporation", "80020001184310", "—", "Valid", ""),
    ("TIN certificate", "1003 4721 88", "—", "Valid", ""),
    ("Trading licence", "Jinja City · 2026", "31 Dec 2026", "Valid", "Upload the 2027 licence when it is issued in January"),
    ("URA tax clearance", "TCC-26-104552", "30 Jun 2027", "Valid", ""),
    ("Bank letter", "Stanbic Bank, Jinja", "—", "Valid", ""),
    ("Company profile & references", "4 references", "—", "Valid", ""),
    ("Signed declaration of eligibility", "Signed 5 Jan 2026", "This round (2026)", "Expiring", "Sign the 2027 declaration by Fri 20 Nov"),
]


def _documents(s):
    y = page_head(s, "Documents", "IDIU checks each one. You get a reminder 30 days before one expires.")
    _renew_banner(s, y)
    y += 84
    rows, links = [], []
    for d, r, e, st, why in BUSOGA_DOCS:
        rows.append([c_text(d, INK, 600), c_text(r, INK2), c_text(e, AMBER_D if st == "Expiring" else INK2),
                     c_status(st, "Renew for 2027" if st == "Expiring" else "Checked"),
                     c_text(why or "—", AMBER_D if st == "Expiring" else MUTED, 600 if st == "Expiring" else 400)])
        links.append("w77b" if st == "Expiring" else None)
    cols = [("Document", 380, "start"), ("Reference", 250, "start"), ("Expires", 220, "start"), ("Status", 220, "start"),
            ("What to do", CW - 1070, "start")]
    list_card(s, y, 66 + 44 + 60 * len(rows) + 20)
    s.text(X0 + 24, y + 42, "On file", 17, 700, INK)
    s.text(X0 + 98, y + 42, "ICT · prequalified until 31 Dec 2026", 13, 400, MUTED)
    data_table(s, X0, y + 66, cols, rows, links=links, row_h=60, check=False)


def w77_documents():
    s = portal("77 Supplier portal: Documents", "Documents", crumbs=["Documents"])
    _documents(s)
    return s


def w77b_renew():
    s = portal("77b Supplier portal: Renew prequalification for 2027", "Documents", crumbs=["Documents", "Renew for 2027"])
    _documents(s)
    x, y = dialog(s, 760, 720, "Renew prequalification for 2027", "Busoga Tech Supplies Ltd · closes Fri 20 Nov 2026, 17:00",
                  close_target="w77")
    w = 760 - 64
    s.text(x, y + 10, "CATEGORIES", 11, 700, MUTED, spacing=0.8)
    s.rect(x, y + 24, w, 52, fill=tint(LIME, 0.5), rx=12, stroke=BRAND, sw=1.5)
    checkbox(s, x + 16, y + 41, True)
    s.text(x + 46, y + 56, "ICT equipment & services", 14.5, 700, INK)
    s.text(x + w - 16, y + 56, "Add a category", 13, 600, BRAND, anchor="end")
    s.text(x, y + 112, "DOCUMENTS", 11, 700, MUTED, spacing=0.8)
    dy = y + 146
    for d, r, e, st, why in BUSOGA_DOCS:
        if st == "Expiring":
            s.icon("upload", x, dy - 14, 18, BRAND, 2)
            s.text(x + 30, dy, "Signed declaration 2027", 14, 700, INK)
            chip(s, x + w, dy - 17, "Declaration_2027_signed.pdf", BRAND_M, icon="check", anchor="end")
        elif e == "31 Dec 2026":
            s.icon("clock", x, dy - 14, 18, AMBER_D, 2)
            s.text(x + 30, dy, d, 14, 600, INK)
            s.text(x + w, dy, "2027 licence: upload in January", 13, 600, AMBER_D, anchor="end")
        else:
            s.icon("check", x, dy - 14, 18, BRAND_M, 2.6)
            s.text(x + 30, dy, d, 14, 500, INK2)
            s.text(x + w, dy, "carries over", 13, 500, MUTED, anchor="end")
        dy += 40
    note(s, x, dy, w, "IDIU Procurement checks the renewal and the Country Director approves it, as for a new "
         "application. You keep receiving RFQs meanwhile.", icon="info")
    by = H / 2 + 720 / 2 - 76
    button(s, x + w, by, "Submit renewal", "primary", icon="send", anchor="end", h=44, target="w77")
    button(s, x + w - 190, by, "Cancel", "secondary", anchor="end", h=44, target="w77")
    return s


SCREENS = [w20_register, w20b_profile, w21_applications, w21b_application_review, w21c_application, w21c_samuel, w70_register, w70b_documents,
           w70c_submitted, w70d_application_status, w71_supplier_home, w72_quotation, w73_rfqs, w74_purchase_orders,
           w74b_lpo, w75_payments, w76_company_profile, w77_documents, w77b_renew]
