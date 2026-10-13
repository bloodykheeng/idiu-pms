"""The front door: the public site (w80–w83) and sign in (w00, w00b). Nobody is signed in on these screens.

w80  Home: what IDIU's procurement is, Sign in and Register as a supplier
w81  About  ·  w82  FAQs  ·  w83  Notices (the open prequalification round, award notices)
w00  Sign in: one door for staff and suppliers (demo: sign in as any account)
w00b Forgot password
Register is w70 → w70b → w70c (suppliers.py). Who signs in decides the dashboard (Alpha's dashboard/layout.tsx):
a staff person gets their console dashboard, a supplier the supplier portal, an applicant their application.
"""
from __future__ import annotations

from data import METHODS, PEOPLE, PREQUAL_ROUND, PROJECTS, SUPPLIER_ACCOUNTS, CATEGORIES, home_key
from kit import (AMBER_D, BRAND, BRAND_M, CARD, FAINT, INK, INK2, LIME, LIME_D, LINE, LINE2, MUTED,
                 avatar, button, chip, field, ref, status_chip, tint, tw)
from shell import (AUTH_RW, AUTH_RX, FOOT, H, PUB_TOP, QCW, QX0, QX1, W, auth, c_text, c_two, data_table, note,
                   public)

# who signs in as what (PLAN.md §2 cast). Each lands on their own dashboard and stays signed in until they switch.
# The demo accounts in the order the work flows: who sets things up, who starts a purchase, who approves it, who owns
# it to the end, who receives it, who checks it afterwards. (person, role, their part)
STAFF_SIGN_IN = [("ivan", "System Administrator", "Sets up lists and users"),
                 ("ruth", "Finance Officer", "Budgets, funds, payment"),
                 ("grace", "Requesting Officer", "Raises the requisition"),
                 ("daniel", "Department Head", "Approves step 1"),
                 ("samuel", "Executive Approver", "Final approvals (CD)"),
                 ("joseph", "Procurement Officer", "Owns it: RFQ to LPO"),
                 ("esther", "Evaluation Committee", "Scores when appointed"),
                 ("peter", "Inspection Officer", "Receives the goods"),
                 ("agnes", "Auditor (read-only)", "Checks it all afterwards")]
SUPPLIER_SIGN_IN = [("mpumudde", "Application pending", "Applies to prequalify"),
                    ("busoga", "Prequalified · ICT", "Quotes, delivers, gets paid")]

STAGES_PUBLIC = [("Budget approved", "Finance · Country Director"),
                 ("Requisition raised", "Any IDIU staff member"),
                 ("Approvals", "Department Head · Finance · Executive Approver"),
                 ("Request for quotations", "Procurement → prequalified suppliers"),
                 ("Evaluation", "Procurement or an appointed committee"),
                 ("LPO issued", "Finance · Country Director"),
                 ("Delivery & inspection", "Stores"),
                 ("Payment reference", "Finance, then the file closes")]

# Award notices: published once the LPO is issued (values agree with the supplier register and the budgets)
AWARDS = [("Tue 6 Oct 2026", "LPO-2026-0051", "10 laptops for training room 2", "Kasese ICT Hub",
           "Busoga Tech Supplies Ltd", 36_400_000),
          ("Tue 29 Sep 2026", "LPO-2026-0049", "Stationery for vocational classes", "Women's Vocational Training",
           "Main Street Stationers", 6_620_000),
          ("Thu 17 Sep 2026", "LPO-2026-0046", "Office chairs, Jinja head office", "Head office operations",
           "Iganga Office Furnishers", 7_300_000),
          ("Mon 10 Aug 2026", "LPO-2026-0036", "Printer and scanner, Kamuli ICT centre", "Teacher ICT Initiative, Kamuli",
           "Kagulu Computers Ltd", 6_200_000)]


def _m(n):
    return f"{n:,.0f}"


def _band(s, h):
    """The soft lime band under the header that public pages open with."""
    s.rect(0, PUB_TOP + 1, W, h, fill=tint(LIME, 0.32), name="hero band")


def _page_title(s, eyebrow, title, sub, y=PUB_TOP + 70):
    s.text(QX0, y, eyebrow, 12, 700, BRAND, spacing=1.2)
    s.text(QX0, y + 58, title, 46, 700, INK, family="display")
    s.text(QX0, y + 96, sub, 17, 400, INK2)


# =====================================================================================
def w80_home():
    s = public("80 Public site: Home", "Home")
    _band(s, 602)
    s.text(QX0, 180, "INTERNATIONAL DEVELOPMENT INSTITUTE UGANDA · PROCUREMENT", 12, 700, BRAND, spacing=1.2)
    s.text(QX0, 256, "Open, fair buying", 66, 700, INK, family="display")
    s.text(QX0, 332, "for every project.", 66, 700, BRAND, family="display")
    s.para(QX0 + 2, 392, "IDIU buys the goods, works and services its projects need in Kasese, Kamuli, Luuka, Mayuge, "
           "Amuria and Kumi. Suppliers prequalify once and are invited to quote in their categories; IDIU staff raise, "
           "approve and follow every purchase here, from budget to closed file.", 720, 19, 400, INK2, lh=31)
    bw = button(s, QX0, 528, "Sign in", "primary", icon="arrowright", h=54, size=16, target="w00")
    button(s, QX0 + bw + 14, 528, "Register as a supplier", "secondary", icon="building", h=54, size=16, target="w70")
    cx = QX0
    for t in ["Maker-checker approvals", "Sealed quotations", "Full audit trail"]:
        s.icon("check", cx, 614, 16, BRAND_M, 2.6)
        cx += 24 + s.text(cx + 24, 627, t, 14, 600, INK2) + 28
    # how a purchase moves: the procurement file, stage by stage, and who acts at each
    cx0, cw, cy = 1060, QX1 - 1060, 140
    s.rect(cx0, cy, cw, 470, fill=CARD, rx=22, stroke=LINE, name="how a purchase moves")
    s.text(cx0 + 32, cy + 46, "How a purchase moves", 21, 700, INK, family="display")
    s.text(cx0 + 32, cy + 70, "One procurement file, from the budget to the payment reference", 13.5, 400, MUTED)
    ry = cy + 112
    s.line(cx0 + 44, ry, cx0 + 44, ry + 7 * 44, tint(BRAND_M, 0.35), 2)
    for i, (st, who) in enumerate(STAGES_PUBLIC):
        last = i == len(STAGES_PUBLIC) - 1
        s.circle(cx0 + 44, ry, 9 if last else 7, fill=LIME if last else BRAND_M, stroke=LIME_D if last else None,
                 sw=2)
        s.text(cx0 + 70, ry + 5, st, 15, 700, INK)
        s.text(cx0 + cw - 32, ry + 5, who, 13, 500, MUTED, anchor="end")
        ry += 44
    # the round that is open now
    ny = 640
    s.rect(cx0, ny, cw, 44, fill=CARD, rx=22, stroke=LINE, name="open notice")
    chip(s, cx0 + 12, ny + 10, "Open now", BRAND_M, solid=True)
    s.text(cx0 + 112, ny + 27, f"Supplier prequalification {PREQUAL_ROUND['year']} · closes {PREQUAL_ROUND['closes'][:15]}",
           14, 600, INK)
    s.icon("arrowright", cx0 + cw - 40, ny + 13, 18, BRAND, 2)
    s.link(cx0, ny, cw, 44, "w83")
    # the three ways in
    y, gw = 724, (QCW - 64) / 3
    cards = [
        ("building", "For suppliers", [("1", "Register and upload your company documents"),
                                       ("2", "IDIU checks them; the Country Director prequalifies you"),
                                       ("3", "Quote on RFQs in your categories, follow LPOs and payments")],
         "Register as a supplier", "w70"),
        ("users", "For IDIU staff", [("1", "Sign in with your IDIU email"),
                                     ("2", "See only what your role allows"),
                                     ("3", "Accounts come from the System Administrator")],
         "Sign in", "w00"),
    ]
    for i, (ic, title, steps, cta, tgt) in enumerate(cards):
        x = QX0 + i * (gw + 32)
        s.rect(x, y, gw, 262, fill=CARD, rx=18, stroke=LINE, name=title)
        s.rect(x + 28, y + 28, 44, 44, fill=tint(BRAND, 0.1), rx=12)
        s.icon(ic, x + 39, y + 39, 22, BRAND, 2)
        s.text(x + 88, y + 57, title, 20, 700, INK, family="display")
        sy = y + 112
        for n, t in steps:
            s.circle(x + 40, sy - 5, 12, fill=tint(BRAND_M, 0.14))
            s.text(x + 40, sy, n, 12, 700, BRAND, anchor="middle")
            s.text(x + 64, sy, t, 14, 500, INK2, maxw=gw - 92)
            sy += 38
        w = s.text(x + 28, y + 236, cta + "  →", 14.5, 700, BRAND)
        s.link(x + 18, y + 214, w + 20, 34, tgt)
    x = QX0 + 2 * (gw + 32)
    s.rect(x, y, gw, 262, fill=CARD, rx=18, stroke=LINE, name="notices")
    s.rect(x + 28, y + 28, 44, 44, fill=tint(BRAND, 0.1), rx=12)
    s.icon("flag", x + 39, y + 39, 22, BRAND, 2)
    s.text(x + 88, y + 57, "Notices", 20, 700, INK, family="display")
    items = [("Open", f"Prequalification {PREQUAL_ROUND['year']}", "All categories · until Fri 20 Nov"),
             ("Award", "10 laptops, Kasese ICT Hub", "Busoga Tech Supplies Ltd · UGX 36,400,000")]
    ny = y + 96
    for kind, a, b in items:
        s.line(x + 28, ny, x + gw - 28, ny, LINE2)
        status_chip(s, x + 28, ny + 16, kind if kind == "Open" else "Issued", label=kind)
        s.text(x + 104, ny + 32, a, 14, 700, INK, maxw=gw - 132)
        s.text(x + 104, ny + 52, b, 12.5, 400, MUTED, maxw=gw - 132)
        ny += 60
    w = s.text(x + 28, y + 236, "All notices  →", 14.5, 700, BRAND)
    s.link(x + 18, y + 214, w + 20, 34, "w83")
    return s


def w81_about():
    s = public("81 Public site: About", "About")
    _band(s, 230)
    _page_title(s, "ABOUT", "Procurement at IDIU",
                "How IDIU buys for its projects, and what this system keeps track of.")
    y, lw = 360, 930
    rx, rw = QX0 + lw + 32, QCW - lw - 32
    s.rect(QX0, y, lw, 286, fill=CARD, rx=18, stroke=LINE, name="who we are")
    s.text(QX0 + 32, y + 48, "Who we are", 21, 700, INK, family="display")
    s.para(QX0 + 32, y + 88, "International Development Institute Uganda (IDIU) is a Christian non-profit based in Jinja, "
           "working with Korea Food for the Hungry International (KFHI) and donors such as KOICA. Its projects reach "
           "communities in six districts:", lw - 64, 15.5, 400, INK2, lh=25)
    py = y + 176
    for i, p in enumerate(PROJECTS[:5]):
        px = QX0 + 32 + (i % 2) * ((lw - 64) / 2)
        s.circle(px + 5, py + (i // 2) * 30 - 5, 4, fill=BRAND_M)
        s.text(px + 18, py + (i // 2) * 30, p[1], 14.5, 600, INK)
    s.rect(QX0, y + 310, lw, 318, fill=CARD, rx=18, stroke=LINE, name="what the system does")
    s.text(QX0 + 32, y + 358, "What this system does", 21, 700, INK, family="display")
    does = [("wallet", "Budgets", "Each project's budget, line by line; a purchase must fit an active line."),
            ("clipboard", "Requisitions and approvals", "Raised by staff, approved step by step by the right people."),
            ("send", "Quotations and evaluation", "RFQs to prequalified suppliers, compared or scored by a committee."),
            ("receipt", "LPOs, delivery and payment", "Orders, goods received, and the payment reference Finance records.")]
    dy = y + 396
    for ic, a, b in does:
        s.icon(ic, QX0 + 32, dy, 20, BRAND, 2)
        s.text(QX0 + 64, dy + 15, a, 15, 700, INK)
        s.text(QX0 + 64 + tw(a, 15, 700) + 12, dy + 15, b, 14, 400, MUTED, maxw=lw - 120 - tw(a, 15, 700))
        dy += 54
    # how we buy
    s.rect(rx, y, rw, 380, fill=CARD, rx=18, stroke=LINE, name="how we buy")
    s.text(rx + 32, y + 48, "How we buy", 21, 700, INK, family="display")
    rules = [("scale", "Value for money", "The best value, not just the lowest price."),
             ("users", "Fair competition", "Three or more quotes from prequalified suppliers."),
             ("shield", "Separate duties", "Whoever prepares a record never approves it."),
             ("history", "Open records", "Every step is kept in the audit trail.")]
    ry = y + 86
    for ic, a, b in rules:
        s.rect(rx + 32, ry, 44, 44, fill=tint(BRAND, 0.09), rx=12)
        s.icon(ic, rx + 43, ry + 11, 22, BRAND, 2)
        s.text(rx + 92, ry + 19, a, 15.5, 700, INK)
        s.text(rx + 92, ry + 39, b, 13.5, 400, MUTED, maxw=rw - 124)
        ry += 70
    s.rect(rx, y + 404, rw, 224, fill=CARD, rx=18, stroke=LINE, name="methods")
    s.text(rx + 32, y + 450, "Method by value", 19, 700, INK, family="display")
    s.text(rx + rw - 32, y + 450, "Example, to be set from IDIU's manual", 12.5, 600, AMBER_D, anchor="end")
    my = y + 492
    for value, method, quotes, _ in METHODS:
        s.line(rx + 32, my - 22, rx + rw - 32, my - 22, LINE2)
        s.text(rx + 32, my + 4, value, 14, 700, INK)
        s.text(rx + 220, my + 4, method, 14, 500, INK2)
        s.text(rx + rw - 32, my + 4, f"{quotes} quote{'s' if quotes != '1' else ''}", 13.5, 500, MUTED, anchor="end")
        my += 44
    return s


FAQS = [("How do I become a prequalified supplier?",
         "Register as a supplier, choose your categories and upload the documents each one needs. IDIU Procurement "
         "checks them, may visit your premises, and recommends; the Country Director decides. You get an email either "
         "way, and your account shows where your application is."),
        ("Which documents do I need?", None),
        ("Can I quote if I'm not prequalified?", None),
        ("How are quotations kept fair?", None),
        ("What happens when a document expires?", None),
        ("Can several people in my company use the portal?", None)]


def w82_faqs():
    s = public("82 Public site: FAQs", "FAQs")
    _band(s, 230)
    _page_title(s, "FAQS", "Questions, answered", "For suppliers and IDIU staff. Can't find yours? Write to Procurement.")
    y = 360
    # topics
    tw_ = 300
    s.rect(QX0, y, tw_, 230, fill=CARD, rx=18, stroke=LINE, name="topics")
    for i, (t, n) in enumerate([("Suppliers", 6), ("IDIU staff", 4), ("Payments", 3)]):
        on = i == 0
        ty = y + 20 + i * 64
        if on:
            s.rect(QX0 + 14, ty, tw_ - 28, 52, fill=tint(BRAND, 0.09), rx=12)
            s.rect(QX0 + 14, ty + 14, 3, 24, fill=BRAND, rx=1.5)
        s.text(QX0 + 36, ty + 32, t, 15.5, 700 if on else 500, BRAND if on else INK2)
        s.text(QX0 + tw_ - 36, ty + 32, str(n), 13, 700, BRAND if on else FAINT, anchor="end")
    # questions
    qx, qw = QX0 + tw_ + 32, 860
    qy = y
    for q, a in FAQS:
        h = 196 if a else 64
        s.rect(qx, qy, qw, h, fill=CARD, rx=16, stroke=LINE, name="question")
        s.text(qx + 28, qy + 39, q, 16, 700, INK)
        s.icon("chevup" if a else "chevdown", qx + qw - 48, qy + 23, 20, BRAND if a else FAINT, 2)
        if a:
            s.para(qx + 28, qy + 78, a, qw - 80, 15, 400, INK2, lh=24)
            w = s.text(qx + 28, qy + 170, "Register as a supplier  →", 14, 700, BRAND)
            s.link(qx + 18, qy + 150, w + 20, 32, "w70")
        qy += h + 12
    # help
    hx, hw = qx + qw + 32, QX1 - (qx + qw + 32)
    s.rect(hx, y, hw, 330, fill=CARD, rx=18, stroke=LINE, name="help")
    s.icon("message", hx + 28, y + 30, 24, BRAND, 2)
    s.text(hx + 28, y + 86, "Still need help?", 19, 700, INK, family="display")
    s.para(hx + 28, y + 118, "Write to IDIU Procurement. We answer within two working days.", hw - 56, 14, 400, INK2, lh=21)
    s.text(hx + 28, y + 182, "procurement@idiu.org", 14.5, 700, BRAND)
    s.line(hx + 28, y + 212, hx + hw - 28, y + 212, LINE2)
    s.text(hx + 28, y + 248, "Forgot your password?", 14, 600, INK)
    w = s.text(hx + 28, y + 274, "Reset it  →", 14, 700, BRAND)
    s.link(hx + 18, y + 254, w + 20, 30, "w00b")
    return s


def w83_notices():
    s = public("83 Public site: Notices", "Notices")
    _band(s, 230)
    _page_title(s, "NOTICES", "Procurement notices",
                "Prequalification rounds and contract awards. RFQs are not advertised: they go to prequalified suppliers.")
    r = PREQUAL_ROUND
    y, lw = 350, 1040
    s.rect(QX0, y, lw, 290, fill=CARD, rx=18, stroke=LINE, name="prequalification round")
    s.rect(QX0, y, 6, 290, fill=BRAND_M, rx=3)
    chip(s, QX0 + 32, y + 28, "Open", BRAND_M, solid=True)
    s.text(QX0 + 32, y + 92, f"Supplier prequalification for {r['year']}", 26, 700, INK, family="display")
    s.text(QX0 + 32, y + 122, f"Opened {r['opened']} · closes {r['closes']} · for 1 Jan to 31 Dec {r['year']}",
           14.5, 500, MUTED)
    s.para(QX0 + 32, y + 162, "IDIU invites suppliers to prequalify in the categories below. Suppliers prequalified for "
           "2026 renew in their portal. New suppliers register online; there is no fee.", lw - 64, 15, 400, INK2, lh=23)
    cx, cy = QX0 + 32, y + 222
    for code, name, *_ in CATEGORIES:
        w = tw(name, 12.5, 600) + 24
        if cx + w > QX0 + lw - 32:
            cx, cy = QX0 + 32, cy + 34
        chip(s, cx, cy, name, BRAND_M)
        cx += w + 8
    # how to apply
    rx, rw = QX0 + lw + 32, QCW - lw - 32
    s.rect(rx, y, rw, 290, fill=CARD, rx=18, stroke=LINE, name="how to apply")
    s.text(rx + 28, y + 44, "How to apply", 19, 700, INK, family="display")
    steps = ["Register your company and categories", "Upload the documents each category needs",
             "Sign the declaration of eligibility and submit"]
    sy = y + 84
    for i, t in enumerate(steps):
        s.circle(rx + 40, sy - 5, 12, fill=tint(BRAND_M, 0.14))
        s.text(rx + 40, sy, str(i + 1), 12, 700, BRAND, anchor="middle")
        s.text(rx + 62, sy, t, 14, 500, INK2, maxw=rw - 90)
        sy += 36
    button(s, rx + 28, y + 200, "Register as a supplier", "primary", icon="building", w=rw - 56, h=44, target="w70")
    w = tw("Already a supplier? Sign in to renew", 13.5, 600)
    s.text(rx + rw / 2, y + 268, "Already a supplier? Sign in to renew", 13.5, 600, BRAND, anchor="middle")
    s.link(rx + rw / 2 - w / 2 - 8, y + 248, w + 16, 30, "w00")
    # award notices
    ay = y + 310
    s.rect(QX0, ay, QCW, H - FOOT - 30 - ay, fill=CARD, rx=18, stroke=LINE, name="award notices")
    s.text(QX0 + 28, ay + 44, "Award notices", 19, 700, INK, family="display")
    s.text(QX0 + 190, ay + 44, "published when the LPO is issued", 13.5, 400, MUTED)
    rows = [[c_text(d, INK2), c_two(what, proj), c_text(sup, INK, 600), c_text(_m(v), INK, 700),
             lambda s_, x, y_, w, h, no=no: ref(s_, x + 16, y_ + h / 2 + 5, no, 13, INK2)]
            for d, no, what, proj, sup, v in AWARDS]
    cols = [("Date", 230, "start"), ("What", 520, "start"), ("Awarded to", 380, "start"), ("Value (UGX)", 210, "start"),
            ("Reference", QCW - 1340, "start")]
    data_table(s, QX0, ay + 66, cols, rows, row_h=50, check=False)
    return s


# =====================================================================================
def w00_sign_in():
    s = auth("00 Sign in")
    rx, rw = AUTH_RX, AUTH_RW
    s.text(rx, 172, "Sign in", 36, 700, INK, family="display")
    s.text(rx, 204, "One sign-in for IDIU staff and registered suppliers.", 15, 400, MUTED)
    field(s, rx, 230, rw, "Email", "i.ssemanda@idiu.org", icon="mail", h=48)
    field(s, rx, 312, rw, "Password", "••••••••••••", icon="lock", h=48)
    w = s.text(rx + rw, 326, "Forgot password?", 13, 600, BRAND, anchor="end")
    s.link(rx + rw - w - 8, 308, w + 16, 26, "w00b")
    button(s, rx, 402, "Sign in", "primary", w=rw, h=50, size=15, target="w01-ivan")
    t1, t2 = "New supplier?  ", "Register as a supplier"
    w1, w2 = tw(t1, 14, 500), tw(t2, 14, 700)
    sx = rx + (rw - w1 - w2) / 2
    s.text(sx, 486, t1, 14, 500, MUTED)
    s.text(sx + w1, 486, t2, 14, 700, BRAND)
    s.link(sx + w1 - 8, 466, w2 + 16, 30, "w70")
    # demo: sign in as any account
    s.line(rx, 518, rx + rw, 518, LINE)
    s.text(rx, 552, "DEMO · SIGN IN AS", 11, 700, MUTED, spacing=1.0)
    s.text(rx + rw, 552, "In the order the work flows · each sees only their menus", 12.5, 500, MUTED, anchor="end")
    s.text(rx, 578, "IDIU staff", 13, 700, INK2)
    s.text(rx + 76, 578, "set up → request → approve → buy → receive → audit", 12.5, 500, MUTED)
    bw = (rw - 16) / 3

    def card(bx, by, w, n, ini, col, line1, line2, part, target):
        s.rect(bx, by, w, 72, fill=CARD, rx=14, stroke=LINE)
        avatar(s, bx + 30, by + 36, 17, ini, col, solid=True)
        ref(s, bx + w - 12, by + 22, f"{n:02d}", 11.5, FAINT, 600, anchor="end")   # the step, quietly
        s.text(bx + 56, by + 23, line1, 13.5, 700, INK, maxw=w - 92)
        s.text(bx + 56, by + 40, line2, 12, 500, MUTED, maxw=w - 62)
        s.text(bx + 56, by + 58, part, 12, 600, BRAND, maxw=w - 62)
        s.link(bx, by, w, 72, target)

    for i, (who, role, part) in enumerate(STAFF_SIGN_IN):
        name, ini, *_rest, col = PEOPLE[who]
        card(rx + (i % 3) * (bw + 8), 592 + (i // 3) * 80, bw, i + 1, ini, col, name, role, part, home_key(who))
    s.text(rx, 852, "Suppliers", 13, 700, INK2)
    s.text(rx + 76, 852, "apply → quote → deliver → get paid", 12.5, 500, MUTED)
    bw2 = (rw - 8) / 2
    for i, (acc, standing, part) in enumerate(SUPPLIER_SIGN_IN):
        contact, ini, company, _, col = SUPPLIER_ACCOUNTS[acc]
        card(rx + i * (bw2 + 8), 866, bw2, i + 1, ini, col, company, f"{contact} · {standing}", part, home_key(acc))
    note(s, rx, 954, rw, "Demo environment with illustrative data: nothing here touches IDIU's live records.",
         icon="shield", color=BRAND)
    return s


def w00b_forgot_password():
    s = auth("00b Forgot password")
    rx, rw = AUTH_RX, AUTH_RW
    s.rect(rx, 250, 64, 64, fill=tint(BRAND, 0.1), rx=18)
    s.icon("lock", rx + 18, 268, 28, BRAND, 2)
    s.text(rx, 380, "Reset your password", 36, 700, INK, family="display")
    s.para(rx, 414, "Enter the email you sign in with. We'll send a link that works for 30 minutes.", rw, 15, 400,
           MUTED, lh=23)
    field(s, rx, 456, rw, "Email", "s.kato@idiu.org", icon="mail", h=48)
    button(s, rx, 552, "Send reset link", "primary", icon="send", w=rw, h=50, size=15, target="w00")
    t1, t2 = "Remembered it?  ", "Sign in"
    w1, w2 = tw(t1, 14, 500), tw(t2, 14, 700)
    sx = rx + (rw - w1 - w2) / 2
    s.text(sx, 640, t1, 14, 500, MUTED)
    s.text(sx + w1, 640, t2, 14, 700, BRAND)
    s.link(sx + w1 - 8, 620, w2 + 16, 30, "w00")
    note(s, rx, 690, rw, "IDIU staff without access to their email: ask the System Administrator (ICT) to reset the account. "
         "Suppliers: use the email you registered with.", icon="info")
    return s


SCREENS = [w80_home, w81_about, w82_faqs, w83_notices, w00_sign_in, w00b_forgot_password]
