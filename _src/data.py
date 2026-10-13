"""Illustrative data shared by every screen, so names, numbers and dates agree everywhere.

IDIU's name, offices, projects and donors are real (idiu.org); people, suppliers, figures, codes and IDs are
made up for the demo. The story and its dates are in PLAN.md §2: change them there first.

Today is Monday 12 October 2026, financial year FY 2026 (1 Jan to 31 Dec).
"""
from __future__ import annotations

from kit import AMBER_D, BLUE, BRAND, BRAND_M, GREY, INK2, KOICA, ORANGE, RED, TEAL, VIOLET

TODAY = "Mon 12 Oct 2026"
TODAY_LONG = "Monday, 12 October 2026"
FY = "FY 2026"

# ---------------------------------------------------------------- people
# key: (name, initials, role, department, office, avatar colour)
PEOPLE = {
    "grace": ("Grace Atim", "GA", "Requesting Officer", "Programmes", "Kasese", VIOLET),
    "harriet": ("Harriet Kyomuhendo", "HK", "Requesting Officer", "Programmes", "Jinja HQ", BRAND_M),
    "daniel": ("Daniel Okello", "DO", "Department Head", "Programmes", "Jinja HQ", BLUE),
    "ruth": ("Ruth Nakato", "RN", "Finance Officer", "Finance", "Jinja HQ", TEAL),
    "joseph": ("Joseph Waiswa", "JW", "Procurement Officer", "Procurement & Logistics", "Jinja HQ", BRAND),
    "samuel": ("Samuel Kato", "SK", "Executive Approver", "Country Director's office", "Jinja HQ", AMBER_D),
    # the committee is a role of its own (proposal §15), given by appointment per procurement with a declaration (§7)
    "esther": ("Esther Namutebi", "EN", "Evaluation Committee Member", "Programmes", "Jinja HQ", ORANGE),
    "brian": ("Brian Ouma", "BO", "Evaluation Committee Member", "ICT", "Jinja HQ", KOICA),
    "moses": ("Moses Tumusiime", "MT", "Evaluation Committee Member", "Finance", "Jinja HQ", TEAL),
    "peter": ("Peter Mukasa", "PM", "Inspection Officer", "Administration", "Jinja HQ", INK2),
    "ivan": ("Ivan Ssemanda", "IS", "System Administrator", "ICT", "Jinja HQ", BLUE),
    "agnes": ("Agnes Akello", "AA", "Auditor", "Internal Audit", "Jinja HQ", RED),
}


def person(key):
    return PEOPLE[key]


# Role titles shown under a name (a role can differ from the job title)
JOB = {
    "grace": "Programme Officer · Kasese ICT Hub",
    "harriet": "Programme Officer · field projects",
    "daniel": "Head of Programmes",
    "ruth": "Finance Officer",
    "joseph": "Procurement Officer",
    "samuel": "Country Director",
    "esther": "Programme Manager · committee chair",
    "brian": "ICT Officer",
    "moses": "Accountant",
    "peter": "Stores & Inspection Officer",
    "ivan": "Systems Administrator",
    "agnes": "Internal Auditor",
}

# ---------------------------------------------------------------- roles and the sidebar each one sees
# One role per person, named as in the proposal's role table (§15). The proposal's Budget Holder (funds check) is done by
# the Finance Officer and its Procurement Manager (oversight) by the Executive Approver until IDIU's manual says otherwise.
ROLES = [
    ("Requesting Officer", "Raise requisitions and follow them", 16),
    ("Department Head", "First approval of their department's requisitions", 6),
    ("Finance Officer", "Budgets, funds checks, payment references", 2),
    ("Procurement Officer", "Suppliers, RFQs, comparison, awards, LPOs, close-out", 2),
    ("Evaluation Committee Member", "Scores the evaluations they are appointed to, after a declaration", 3),
    ("Executive Approver", "High-value and final approvals (the Country Director)", 1),
    ("Inspection Officer", "Goods received and inspection", 2),
    ("System Administrator", "Setup lists, users, roles, approval workflows", 1),
    ("Auditor", "Read everything, change nothing", 1),
]
# where a full role name is too long (the sidebar's user card, the sign-in cards)
ROLE_SHORT = {"Evaluation Committee Member": "Evaluation Committee"}

# Menu entries per role: like SDS's routeAccess.ts, the one list the sidebar is drawn from (and w61 shows).
# Every menu entry, in sidebar order. System Admin sees all of them; the Auditor all but My approvals.
_ALL_SETUP = ["Financial years", "Departments", "Offices & cost centres", "Donors", "Projects", "Account codes",
              "Procurement categories", "Supplier document types", "Units of measure"]
_PROCUREMENT = ["Requisitions", "RFQs & quotations", "Evaluations", "Purchase orders", "Deliveries"]
MENU = ["Dashboard", "My approvals", *_PROCUREMENT, "Supplier register", "Applications", "Budgets", "Budget revisions",
        "Procurement register", "Budget utilisation", *_ALL_SETUP, "Users", "Roles & permissions",
        "Approval workflows", "Audit trail"]
PERMS = {
    "Requesting Officer": ["Dashboard", "Requisitions", "Deliveries"],
    "Department Head": ["Dashboard", "My approvals", "Requisitions", "Budgets", "Budget utilisation"],
    "Finance Officer": ["Dashboard", "My approvals", *_PROCUREMENT, "Budgets", "Budget revisions",
                        "Procurement register", "Budget utilisation", "Financial years", "Account codes"],
    "Procurement Officer": ["Dashboard", *_PROCUREMENT, "Supplier register", "Applications", "Budgets",
                            "Procurement register", "Budget utilisation", "Procurement categories",
                            "Supplier document types", "Units of measure"],
    "Evaluation Committee Member": ["Dashboard", "Evaluations"],
    "Executive Approver": ["Dashboard", "My approvals", *_PROCUREMENT, "Supplier register", "Applications",
                         "Budgets", "Budget revisions", "Procurement register", "Budget utilisation",
                         "Approval workflows", "Audit trail"],
    "Inspection Officer": ["Dashboard", "Purchase orders", "Deliveries"],
    "System Administrator": list(MENU),
    "Auditor": [m for m in MENU if m != "My approvals"],
}
PERMS = {role: [m for m in MENU if m in labels] for role, labels in PERMS.items()}   # always in sidebar order

def menu_for(person):
    """The sidebar entries one person sees: their role's list (one role per person)."""
    return list(PERMS[PEOPLE[person][2]])


# Everyone who can sign in to the console, and the screens that are theirs alone
SESSIONS = ["ivan", "joseph", "samuel", "daniel", "ruth", "grace", "esther", "peter", "agnes"]
INBOX_KEY = {"samuel": "w02", "daniel": "w03", "ruth": "w02-ruth", "ivan": "w02-ivan"}


def dashboard_key(person):
    return f"w01-{person}"


def menu_target(label, person):
    """Where a menu entry goes for this person when it is theirs alone (else the shared screen, shell.NAV)."""
    if label == "Dashboard":
        return dashboard_key(person)
    if label == "My approvals":
        return INBOX_KEY[person]
    if label == "Evaluations" and person == "esther":
        return "w13-esther"
    return None


# ---------------------------------------------------------------- supplier accounts
# Suppliers sign in at the same door as staff and land on the supplier portal (Alpha: investor → client portal).
# key: (contact person, initials, company, standing, avatar colour)
SUPPLIER_ACCOUNTS = {
    "busoga": ("Amos Waiswa", "AW", "Busoga Tech Supplies Ltd", "Prequalified supplier", BRAND),
    "mpumudde": ("Fatuma Nabirye", "FN", "Mpumudde Furniture Works", "Application pending", AMBER_D),
}
SUPPLIER_SESSIONS = list(SUPPLIER_ACCOUNTS)
# The portal's menu per account: (label, icon, target). A pending applicant sees only their application.
SUPPLIER_MENU = {
    "busoga": [("Home", "home", "w71"), ("RFQs", "send", "w73"), ("Purchase orders", "receipt", "w74"),
               ("Payments", "banknote", "w75"), ("Company profile", "building", "w76"), ("Documents", "file", "w77")],
    "mpumudde": [("My application", "clipboard", "w70d")],
}
SUPPLIER_HOME = {p: SUPPLIER_MENU[p][0][2] for p in SUPPLIER_SESSIONS}
PREQUAL_ROUND = {"year": "2027", "opened": "Thu 1 Oct 2026", "closes": "Fri 20 Nov 2026, 17:00"}


def home_key(account):
    """Where an account lands after signing in: a staff person's dashboard, or the supplier's portal home."""
    return SUPPLIER_HOME.get(account) or dashboard_key(account)


# Each person's dashboard: what is waiting on them. (icon, title, reference, detail, target)
YOUR_TURN = {
    "ivan": [("users", "Review inactive accounts", "34 users", "2 have not signed in for 90 days", "w60"),
             ("workflow", "Workflow change", "Requisition", "Executive approval from UGX 25M · draft", "w62b"),
             ("file", "Supplier document types", "9 types", "Confirm validity periods before November", "w57")],
    "joseph": [("send", "Send the RFQ", "PR-2026-0091", "Desks and chairs, Kamuli · approved 3 days ago", "w12b"),
               ("building", "Review a supplier application", "SUP-APP-0143", "Victoria Builders & Plumbing · 9 of 9 documents", "w21"),
               ("clock", "Quotations closing", "RFQ-2026-0035", "Network switches · closes Wed 14 Oct · 2 of 4 in", "w12")],
    "samuel": [("clipboard", "Approve a requisition", "PR-2026-0096", "Solar backup system · UGX 34.5M · step 3 of 3", "w02b"),
               ("award", "Approve an award", "PR-2026-0089", "Printing manuals · Jinja Print & Pack · 2 days", "w13c"),
               ("swap", "Approve a budget revision", "BR-2026-0007", "Kamuli · move UGX 9M to furniture", "w31b")],
    "daniel": [("clipboard", "Approve a requisition", "PR-2026-0095", "Hygiene kits · UGX 3.6M · step 1 of 2", "w03b"),
               ("calendar", "Away 19–30 Oct", "Acting approver", "Rebecca Achan approves for you", None),
               ("gauge", "Programmes budgets", "FY 2026", "4 projects · 61% used with 12 weeks to go", "w41")],
    "ruth": [("edit", "Finish a draft budget", "BUD-2027-002", "Model Home Health · 1 line left to add", "w30c"),
             ("sheet", "Fix an import", "BUD-2027-001", "Kasese ICT Hub FY 2027 · 3 rows to fix", "w30d"),
             ("swap", "Revision with the Country Director", "BR-2026-0007", "Kamuli · waiting 3 days", "w31")],
    "grace": [("edit", "Finish your requisition", "PR-2026-0098", "Projector and screen · draft saved 09:31", "w10b"),
              ("clock", "With the Executive Approver", "PR-2026-0096", "Solar backup system · step 3 of 3", "w10d"),
              ("check", "Delivered and paid", "PR-2026-0087", "10 laptops · file closed today", "w11")],
    "esther": [("scale", "Score an evaluation", "PR-2026-0090", "Washroom block · due tomorrow · you chair", "w13b"),
               ("clock", "With the Executive Approver", "PR-2026-0089", "Printing manuals · your committee's recommendation",
                "w13-esther"),
               ("check", "Evaluation closed", "PR-2026-0087", "10 laptops · awarded to Busoga Tech and paid", "w13d")],
    "peter": [("truck", "Delivery due today", "LPO-2026-0049", "Stationery · Main Street Stationers · Mayuge", "w15b"),
              ("package", "Delivery due Thursday", "LPO-2026-0045", "Hygiene kits batch 1 · Kumi", "w15"),
              ("receipt", "LPOs issued this month", "6 LPOs", "UGX 74.9M · 2 still to deliver", "w14")],
    "agnes": [("history", "Activity today", "38 entries", "1 failed sign-in · 2 approvals", "w63"),
              ("folder", "File closed today", "PR-2026-0087", "10 laptops · all documents complete", "w11c"),
              ("swap", "Budget changes this quarter", "3 revisions", "BR-2026-0006 approved 22 Sep", "w63b")],
}

# ---------------------------------------------------------------- master data (PLAN.md §4)
# name, start, end, status, budgets
FINANCIAL_YEARS = [
    ("FY 2027", "1 Jan 2027", "31 Dec 2027", "Planning", 0),
    ("FY 2026", "1 Jan 2026", "31 Dec 2026", "Open", 6),
    ("FY 2025", "1 Jan 2025", "31 Dec 2025", "Closed", 5),
    ("FY 2024", "1 Jan 2024", "31 Dec 2024", "Closed", 4),
]

# code, name, head, users, requisitions this FY, status
DEPARTMENTS = [
    ("PRG", "Programmes", "Daniel Okello", 21, 96, "Active"),
    ("FIN", "Finance", "Ruth Nakato", 3, 4, "Active"),
    ("PRC", "Procurement & Logistics", "Joseph Waiswa", 2, 2, "Active"),
    ("ADM", "Administration", "Rebecca Achan", 4, 11, "Active"),
    ("ICT", "ICT", "Brian Ouma", 2, 6, "Active"),
    ("CDO", "Country Director's office", "Samuel Kato", 2, 1, "Active"),
    ("AUD", "Internal Audit", "Agnes Akello", 1, 0, "Active"),
    ("MEL", "Monitoring & Evaluation", "—", 0, 3, "Inactive"),
]

# code, name, district, type, users, requisitions this FY, status
OFFICES = [
    ("JIN", "Jinja head office", "Jinja", "Head office", 19, 28, "Active"),
    ("KSE", "Kasese field office", "Kasese", "Field office", 4, 31, "Active"),
    ("KML", "Kamuli field office", "Kamuli", "Field office", 3, 22, "Active"),
    ("LUU", "Luuka project site", "Luuka", "Project site", 2, 9, "Active"),
    ("MAY", "Mayuge field office", "Mayuge", "Field office", 3, 14, "Active"),
    ("AMU", "Amuria field office", "Amuria", "Field office", 2, 7, "Active"),
    ("KUM", "Kumi field office", "Kumi", "Field office", 2, 11, "Active"),
]

# code, name, type, country, projects, status
DONORS = [
    ("KOICA", "Korea International Cooperation Agency", "Bilateral agency", "South Korea", 1, "Active"),
    ("KFHI", "Korea Food for the Hungry International", "Partner NGO", "South Korea", 4, "Active"),
    ("IDIU", "IDIU own funds", "Own funds", "Uganda", 1, "Active"),
]

# code, name, donor, department, office, start, end, FY 2026 budget, status
PROJECTS = [
    ("KSE-ICT", "Kasese ICT Hub", "KOICA", "Programmes", "KSE", "Mar 2025", "Feb 2028", 296_000_000, "Active"),
    ("KML-TICT", "Teacher ICT Initiative, Kamuli", "KFHI", "Programmes", "KML", "Jan 2026", "Dec 2027", 184_500_000, "Active"),
    ("LUU-WASH", "Busalamu School Sanitation, Luuka", "KFHI", "Programmes", "LUU", "Jul 2026", "Jun 2027", 142_000_000, "Active"),
    ("MAY-VOC", "Women's Vocational Training, Mayuge & Amuria", "KFHI", "Programmes", "MAY", "Jan 2025", "Dec 2026", 96_800_000, "Active"),
    ("KUM-MHH", "Model Home Health, Kumi", "KFHI", "Programmes", "KUM", "Jan 2026", "Dec 2026", 74_200_000, "Active"),
    ("HQ-OPS", "Head office operations", "IDIU", "Administration", "JIN", "Jan 2026", "Dec 2026", 210_000_000, "Active"),
]
PROJECT = {p[0]: p for p in PROJECTS}

# code, name, group, budget lines using it, accounting code
ACCOUNT_CODES = [
    ("5110", "Office supplies & stationery", "Supplies", 6, "6110-00"),
    ("5120", "Printing & publications", "Supplies", 3, "6120-00"),
    ("5210", "ICT equipment", "Equipment", 3, "1520-10"),
    ("5220", "Furniture & fittings", "Equipment", 4, "1530-10"),
    ("5230", "Solar & electrical equipment", "Equipment", 2, "1540-10"),
    ("5310", "Construction & civil works", "Works", 1, "1410-00"),
    ("5410", "Training materials", "Programme costs", 4, "7210-00"),
    ("5420", "Venues & meals", "Programme costs", 5, "7220-00"),
    ("5510", "Vehicles & motorcycles", "Transport", 1, "6410-00"),
    ("5610", "Health supplies", "Programme costs", 1, "7310-00"),
]
ACCOUNT = {a[0]: a for a in ACCOUNT_CODES}

# Supplier document types: name, expires, validity, required for
DOC_TYPES = [
    ("Certificate of incorporation", False, "—", "All categories"),
    ("TIN certificate", False, "—", "All categories"),
    ("Trading licence", True, "12 months", "All categories"),
    ("URA tax clearance", True, "12 months", "All categories"),
    ("NSSF clearance", True, "12 months", "Construction & works"),
    ("Bank letter", False, "—", "All categories"),
    ("Professional licence (UNABCEC)", True, "12 months", "Construction & works"),
    ("Company profile & references", False, "—", "All categories"),
    ("Signed declaration of eligibility", True, "Each prequalification", "All categories"),
]

# code, name, default account code, prequalified suppliers, open RFQs, status
CATEGORIES = [
    ("ICT", "ICT equipment & services", "5210", 4, 1, "Active"),
    ("FUR", "Furniture", "5220", 2, 0, "Active"),
    ("PRN", "Printing & stationery", "5120", 5, 1, "Active"),
    ("WRK", "Construction & works", "5310", 3, 0, "Active"),
    ("SOL", "Solar & electrical", "5230", 1, 0, "Active"),
    ("TRN", "Training & events", "5420", 4, 0, "Active"),
    ("VEH", "Vehicles & spares", "5510", 2, 0, "Active"),
    ("HLT", "Health supplies", "5610", 2, 0, "Active"),
]

# code, name, used on lines
UNITS = [
    ("PC", "Piece", 214), ("SET", "Set", 38), ("BOX", "Box", 41), ("REAM", "Ream", 19), ("CTN", "Carton", 12),
    ("LOT", "Lot", 9), ("LTR", "Litre", 6), ("DAY", "Day", 23), ("TRIP", "Trip", 7), ("PAX", "Person", 15),
]

# ---------------------------------------------------------------- approval workflows (PLAN.md §5)
# record type: [(step name, role, only above UGX or None)]
WORKFLOWS = {
    "Requisition": [("Department review", "Department Head", None), ("Funds check", "Finance Officer", None),
                    ("Executive approval", "Executive Approver", 30_000_000)],
    "Award recommendation": [("Award approval", "Executive Approver", None)],
    "LPO": [("Commitment check", "Finance Officer", None), ("Signature", "Executive Approver", 5_000_000)],
    "Budget": [("Budget approval", "Executive Approver", None)],
    "Budget revision": [("Revision approval", "Executive Approver", None)],
    "Supplier prequalification": [("Prequalification decision", "Executive Approver", None)],
    "Approval workflow change": [("Change approval", "Executive Approver", None)],
}
# value up to, method, quotes, evaluation
METHODS = [
    ("Up to UGX 5M", "Direct purchase", "1", "Procurement Officer"),
    ("UGX 5M to 30M", "Request for quotations", "3 or more", "Quotation comparison"),
    ("Above UGX 30M", "RFQ + evaluation committee", "3 or more", "Evaluation committee"),
]

# ---------------------------------------------------------------- budgets
# Kasese ICT Hub FY 2026, line by line. 5210's spent includes PR-2026-0087 (LPO 36.4M, paid 12 Oct).
# account, description, cost centre, budget, spent, committed, reserved
KASESE_LINES = [
    ("5210", "Laptops, desktops and network for the two training rooms", "KSE", 160_000_000, 99_800_000, 0, 0),
    ("5230", "Solar backup and electrical works", "KSE", 48_000_000, 6_200_000, 0, 0),
    ("5220", "Accessible desks and chairs", "KSE", 24_000_000, 21_350_000, 0, 0),
    ("5410", "Training materials and screen-reader licences", "KSE", 30_000_000, 12_800_000, 3_100_000, 0),
    ("5420", "Training venues and meals", "KSE", 26_000_000, 9_450_000, 0, 0),
    ("5110", "Office supplies and stationery", "KSE", 8_000_000, 4_720_000, 0, 0),
]


def line_available(line):
    _, _, _, b, s, c, r = line
    return b - s - c - r


KASESE_TOTAL = sum(l[3] for l in KASESE_LINES)              # 296,000,000

# code, project, donor, total, spent, committed, reserved, status, lines, approved
BUDGETS = [
    ("BUD-2026-001", "KSE-ICT", "KOICA", KASESE_TOTAL, sum(l[4] for l in KASESE_LINES), sum(l[5] for l in KASESE_LINES),
     sum(l[6] for l in KASESE_LINES), "Active", len(KASESE_LINES), "9 Jan · Samuel Kato"),
    ("BUD-2026-002", "KML-TICT", "KFHI", 184_500_000, 71_300_000, 31_200_000, 18_600_000, "Active", 7, "12 Jan · Samuel Kato"),
    ("BUD-2026-003", "LUU-WASH", "KFHI", 142_000_000, 18_400_000, 0, 86_000_000, "Active", 5, "3 Jul · Samuel Kato"),
    ("BUD-2026-004", "MAY-VOC", "KFHI", 96_800_000, 58_900_000, 6_800_000, 0, "Active", 6, "14 Jan · Samuel Kato"),
    ("BUD-2026-005", "KUM-MHH", "KFHI", 74_200_000, 41_250_000, 2_300_000, 0, "Active", 5, "15 Jan · Samuel Kato"),
    ("BUD-2026-006", "HQ-OPS", "IDIU", 210_000_000, 141_600_000, 4_850_000, 0, "Active", 12, "8 Jan · Samuel Kato"),
]

# FY 2027 budgets in preparation (FY 2027 is "Planning" in Setup › Financial years)
# Model Home Health, entered line by line by Ruth (w30c): account, description, cost centre, amount
KUMI_2027_LINES = [
    ("5610", "Hygiene kits and first-aid supplies", "KUM", 31_200_000),
    ("5410", "Household health training materials", "KUM", 15_800_000),
    ("5420", "Community session venues and meals", "KUM", 13_000_000),
    ("5110", "Office supplies and stationery", "KUM", 3_400_000),
]
KUMI_2027_NEW = ("5510", "Motorcycle fuel and maintenance", "KUM", 17_600_000)   # the line being added

# Kasese ICT Hub FY 2027, imported from Excel (w30d): row, account, description, cost centre, amount, problem
KASESE_2027_IMPORT = [
    (2, "5210", "Replacement laptops, training room 1", "KSE", 92_000_000, None),
    (3, "5210", "Assistive devices (braille displays, headsets)", "KSE", 46_500_000, None),
    (4, "5230", "Solar maintenance contract", "KSE", 9_600_000, None),
    (5, "5410", "Screen-reader licence renewals", "KSE", 18_000_000, None),
    (6, "5420", "Training venues and meals", "KSE", 28_000_000, None),
    (7, "5299", "Internet bandwidth", "KSE", 21_600_000, "Account code 5299 doesn't exist (Setup › Account codes)"),
    (8, "5110", "Office supplies and stationery", "KSE", 8_400_000, None),
    (9, "5210", "Replacement laptops, training room 1", "KSE", 92_000_000, "Same as row 2: remove one or change it"),
    (10, "5220", "Accessible desks, training room 3", "KSN", 26_000_000, "Cost centre KSN doesn't exist (did you mean KSE?)"),
]

# Budget revision awaiting the Country Director (w31b)
REVISION = {
    "no": "BR-2026-0007",
    "budget": "BUD-2026-002",
    "project": "KML-TICT",
    "by": "ruth",
    "on": "Fri 9 Oct, 16:12",
    "reason": ("Enrolment at the Kamuli ICT centre rose from 40 to 60 teachers, so a second classroom set of "
               "desks is needed. Venue costs fell because training moved into the centre."),
    # account, description, old budget, new budget, spent+committed+reserved
    "lines": [
        ("5420", "Training venues and meals", 38_000_000, 29_000_000, 14_250_000),
        ("5220", "Classroom desks and chairs", 22_000_000, 31_000_000, 18_600_000),
    ],
}
REVISIONS = [
    ("BR-2026-0007", "Teacher ICT Initiative, Kamuli", "Move UGX 9M: venues → furniture", 9_000_000, "ruth", "9 Oct", "Pending approval"),
    ("BR-2026-0006", "Head office operations", "Move UGX 4.5M: stationery → vehicles", 4_500_000, "ruth", "21 Sep", "Approved"),
    ("BR-2026-0005", "Kasese ICT Hub", "Raise ICT equipment by UGX 20M (KOICA top-up)", 20_000_000, "ruth", "2 Sep", "Approved"),
    ("BR-2026-0004", "Women's Vocational Training", "Move UGX 2M: meals → training materials", 2_000_000, "ruth", "18 Aug", "Returned"),
    ("BR-2026-0003", "Busalamu School Sanitation", "Add line 5310 Construction & works", 86_000_000, "ruth", "1 Jul", "Approved"),
]

# ---------------------------------------------------------------- procurement files
# no, title, project, office, account, requester, value, stage, status label, waiting on, since, method
FILES = [
    ("PR-2026-0098", "Projector and screen for training room 2", "KSE-ICT", "KSE", "5210", "grace", 4_200_000,
     "Requested", "Draft", "Grace Atim", "today", "Direct purchase"),
    ("PR-2026-0096", "Solar backup system", "KSE-ICT", "KSE", "5230", "grace", 34_500_000, "Requested",
     "Awaiting approval", "Samuel Kato (3 of 3)", "1 day", "RFQ + committee"),
    ("PR-2026-0095", "Hygiene kits for model homes", "KUM-MHH", "KUM", "5610", "harriet", 3_600_000, "Requested",
     "Awaiting approval", "Daniel Okello (1 of 2)", "4 h", "Direct purchase"),
    ("PR-2026-0094", "Salon and sewing starter kits", "MAY-VOC", "MAY", "5410", "harriet", 12_800_000, "Requested",
     "Returned", "Harriet Kyomuhendo", "2 days", "Request for quotations"),
    ("PR-2026-0091", "Desks and chairs, Kamuli ICT centre", "KML-TICT", "KML", "5220", "harriet", 18_600_000,
     "Sourcing", "Approved", "Joseph Waiswa (RFQ)", "3 days", "Request for quotations"),
    ("PR-2026-0090", "Washroom block, Busalamu P/S", "LUU-WASH", "LUU", "5310", "harriet", 86_000_000,
     "Evaluation", "Evaluation", "Committee (2 of 3 scored)", "4 days", "RFQ + committee"),
    ("PR-2026-0089", "Printing teacher training manuals", "KML-TICT", "KML", "5120", "harriet", 31_200_000,
     "Award", "Award", "Samuel Kato", "2 days", "RFQ + committee"),
    ("PR-2026-0093", "Network switches and cabling", "KML-TICT", "KML", "5210", "harriet", 14_200_000,
     "Sourcing", "Sourcing", "Suppliers (RFQ closes Wed)", "5 days", "Request for quotations"),
    ("PR-2026-0087", "10 laptops for training room 2", "KSE-ICT", "KSE", "5210", "grace", 38_000_000,
     "Closed", "Closed", "—", "today", "RFQ + committee"),
    ("PR-2026-0084", "Stationery for vocational classes", "MAY-VOC", "MAY", "5110", "harriet", 6_800_000,
     "Delivered", "LPO issued", "Peter Mukasa (delivery today)", "today", "Request for quotations"),
    ("PR-2026-0082", "Motorcycle tyres and service", "HQ-OPS", "JIN", "5510", "peter", 2_450_000, "Closed",
     "Closed", "—", "30 Sep", "Direct purchase"),
    ("PR-2026-0079", "Office chairs, Jinja head office", "HQ-OPS", "JIN", "5220", "peter", 7_300_000, "Closed",
     "Closed", "—", "24 Sep", "Request for quotations"),
    ("PR-2026-0077", "Extra internet bandwidth, Q4", "KSE-ICT", "KSE", "5210", "grace", 5_400_000, "Requested",
     "Rejected", "—", "18 Sep", "Request for quotations"),
]
FILE = {f[0]: f for f in FILES}

# The flagship file, PR-2026-0087 (PLAN.md §2)
LAPTOPS = {
    "no": "PR-2026-0087",
    "title": "10 laptops for training room 2",
    "item": "Laptop, Core i5 (13th gen), 16 GB RAM, 512 GB SSD, 14\", Windows 11 Pro, screen-reader ready, 3-year warranty",
    "qty": 10,
    "unit_est": 3_800_000,
    "est": 38_000_000,
    "needed": "Fri 16 Oct 2026",
    "justification": ("Training room 2 opens in October for 20 learners with disabilities. Laptops must run "
                      "NVDA and JAWS screen readers."),
    "approvals": [
        ("daniel", "Department review", "Mon 14 Sep, 15:40", "Approved", "Needed for the second training room opening in October."),
        ("ruth", "Funds check", "Tue 15 Sep, 10:05", "Approved", "Funds available on 5210: UGX 96.6M before this request."),
        ("samuel", "Executive approval", "Wed 16 Sep, 08:47", "Approved", "Approved. Make sure the accessibility software is included."),
    ],
    "rfq": "RFQ-2026-0031",
    "rfq_sent": "Thu 17 Sep",
    "rfq_close": "Mon 28 Sep, 12:00",
    # supplier, total, delivery days, warranty, compliant, technical (of 70), financial (of 30), total score
    "quotes": [
        ("Busoga Tech Supplies Ltd", 36_400_000, 10, "3 years", True, 59.2, 29.2, 88.4),
        ("Kagulu Computers Ltd", 39_900_000, 7, "3 years", True, 57.5, 26.6, 84.1),
        ("Source Point ICT Ltd", 35_200_000, 21, "1 year", False, None, None, None),
        ("Nile Bridge Systems Ltd", None, None, None, None, None, None, None),
    ],
    "committee": ["esther", "brian", "moses"],
    "award_on": "Mon 5 Oct, 09:20",
    "lpo": "LPO-2026-0051",
    "lpo_value": 36_400_000,
    "lpo_issued": "Tue 6 Oct, 11:30",
    "delivery_by": "Fri 16 Oct 2026",
    "dn": "DN-4471",
    "grn": "GRN-2026-0064",
    "delivered": "Fri 9 Oct, 14:15",
    "invoice": "BTS-INV-0912",
    "invoice_on": "Mon 12 Oct, 09:12",
    "payment_ref": "EFT-STB-26-10-0331",
    "paid": "Mon 12 Oct, 09:38",
    "voucher": "PV-2026-1184",
    "bank": "Stanbic Bank · KOICA project account",
    "closed": "Mon 12 Oct, 09:41",
}

# Desks RFQ (w12b): PR-2026-0091, Furniture
DESKS = {"no": "PR-2026-0091", "rfq": "RFQ-2026-0036", "items": [
    ("Classroom desk, 2-seater, laminated top", 30, "Piece", 340_000),
    ("Stackable chair, steel frame", 60, "Piece", 140_000),
]}

# Washroom evaluation (w13b): PR-2026-0090, Works, Esther scoring
WASHROOM = {"no": "PR-2026-0090", "rfq": "RFQ-2026-0033", "bids": [
    ("Kakira Builders Ltd", 82_600_000), ("Mutai Engineering Ltd", 79_900_000), ("Lake Basin Contractors", 88_400_000)]}

# Printing award (w13c): PR-2026-0089, awaiting the Country Director
PRINTING = {"no": "PR-2026-0089", "rfq": "RFQ-2026-0032", "bids": [
    ("Jinja Print & Pack Ltd", 29_750_000, 91.0), ("Busoga Printers Ltd", 28_900_000, 86.5),
    ("Source Line Graphics", 32_400_000, 80.2)]}

# Stationery delivery (w15b): PR-2026-0084, LPO-2026-0049, arriving today
STATIONERY = {"no": "PR-2026-0084", "lpo": "LPO-2026-0049", "supplier": "Main Street Stationers", "lines": [
    # item, unit, ordered, received, accepted
    ("A4 paper, 80 gsm", "Ream", 120, 120, 120),
    ("Flip chart pads", "Piece", 40, 40, 38),
    ("Marker pens, assorted", "Box", 25, 25, 25),
    ("Sewing thread, 500 m spools", "Box", 30, 18, 18),
]}

# ---------------------------------------------------------------- suppliers
# name, categories, TIN, district, status, prequalified until, LPOs FY, value FY, expiring docs
SUPPLIERS = [
    ("Busoga Tech Supplies Ltd", "ICT", "1003 4721 88", "Jinja", "Prequalified", "31 Dec 2026", 4, 58_900_000, 0),
    ("Kagulu Computers Ltd", "ICT", "1009 2215 40", "Kamuli", "Prequalified", "31 Dec 2026", 1, 6_200_000, 0),
    ("Source Point ICT Ltd", "ICT", "1012 5532 17", "Kampala", "Prequalified", "31 Dec 2026", 0, 0, 1),
    ("Nile Bridge Systems Ltd", "ICT · Solar", "1007 8890 03", "Jinja", "Expiring", "31 Oct 2026", 1, 3_400_000, 2),
    ("Jinja Print & Pack Ltd", "Printing", "1004 1180 62", "Jinja", "Prequalified", "31 Dec 2026", 3, 12_700_000, 0),
    ("Main Street Stationers", "Printing", "1002 6654 21", "Jinja", "Prequalified", "31 Dec 2026", 6, 15_300_000, 0),
    ("Kakira Builders Ltd", "Works", "1005 4401 39", "Jinja", "Prequalified", "31 Dec 2026", 0, 0, 0),
    ("Wairaka Woodworks Ltd", "Furniture", "1008 3307 75", "Jinja", "Prequalified", "31 Dec 2026", 2, 21_350_000, 0),
    ("Iganga Office Furnishers", "Furniture", "1011 7720 58", "Iganga", "Prequalified", "31 Dec 2026", 1, 7_300_000, 0),
    ("SunPower Busoga Ltd", "Solar", "1006 9934 12", "Jinja", "Suspended", "—", 0, 0, 1),
]
SUPPLIER_COUNT = 47        # all suppliers in the register (rows above are the first page)

# Prequalification applications: name, categories, submitted, documents, status, reviewer
APPLICATIONS = [
    ("Mpumudde Furniture Works", "Furniture", "Tue 6 Oct", "7 of 7", "Pending approval", "Joseph Waiswa → Samuel Kato"),
    ("Victoria Builders & Plumbing", "Construction & works", "Mon 5 Oct", "9 of 9", "Under review", "Joseph Waiswa"),
    ("Kyabazinga Caterers", "Training & events", "Fri 2 Oct", "5 of 7", "Returned", "Joseph Waiswa"),
    ("Masese Motors & Spares", "Vehicles & spares", "28 Sep", "7 of 7", "Approved", "Samuel Kato"),
    ("Busoga Printers Ltd", "Printing & stationery", "21 Sep", "7 of 7", "Approved", "Samuel Kato"),
    ("Quick Fix Electricals", "Solar & electrical", "15 Sep", "5 of 7", "Rejected", "Samuel Kato"),
]

MPUMUDDE = {
    "name": "Mpumudde Furniture Works",
    "tin": "1013 2268 91",
    "reg": "80020004417652",
    "address": "Plot 12, Mpumudde Industrial Road, Jinja",
    "contact": "Fatuma Nabirye · 0772 405 118",
    "email": "sales@mpumuddefurniture.ug",
    "since": "2017",
    "staff": "14",
    "categories": ["Furniture"],
    "docs": [
        ("Certificate of incorporation", "80020004417652", "—", "Valid"),
        ("TIN certificate", "1013 2268 91", "—", "Valid"),
        ("Trading licence", "Jinja City · 2026", "31 Dec 2026", "Valid"),
        ("URA tax clearance", "TCC-26-118734", "30 Jun 2027", "Valid"),
        ("Bank letter", "Centenary Bank, Jinja", "—", "Valid"),
        ("Company profile & references", "3 references", "—", "Valid"),
        ("Signed declaration of eligibility", "Signed 6 Oct 2026", "This round", "Valid"),
        ("Trading licence (previous year)", "Jinja City · 2025", "31 Dec 2025", "Expired"),
    ],
}

# ---------------------------------------------------------------- my approvals (Samuel, today)
# type, reference, what, value, step, submitted by, waiting, target
INBOX = [
    ("Requisition", "PR-2026-0096", "Solar backup system · Kasese ICT Hub", 34_500_000, "Executive approval · 3 of 3", "grace", "1 day", "w02b"),
    ("Award", "PR-2026-0089", "Printing teacher training manuals · Jinja Print & Pack", 29_750_000, "Award approval · 1 of 1", "joseph", "2 days", "w13c"),
    ("Budget revision", "BR-2026-0007", "Teacher ICT Initiative, Kamuli · move UGX 9M", 9_000_000, "Revision approval · 1 of 1", "ruth", "3 days", "w31b"),
    ("Prequalification", "SUP-APP-0142", "Mpumudde Furniture Works · Furniture", None, "Prequalification decision · 1 of 1", "joseph", "2 days", "w21b"),
]

# ---------------------------------------------------------------- users
# key or None, name, email, role, department, office, status, last seen
USERS = [
    ("daniel", "Daniel Okello", "d.okello@idiu.org", "Department Head", "Programmes", "Jinja HQ", "Active", "Today 08:12"),
    ("grace", "Grace Atim", "g.atim@idiu.org", "Requesting Officer", "Programmes", "Kasese", "Active", "Today 09:31"),
    ("ruth", "Ruth Nakato", "r.nakato@idiu.org", "Finance Officer", "Finance", "Jinja HQ", "Active", "Today 09:02"),
    ("joseph", "Joseph Waiswa", "j.waiswa@idiu.org", "Procurement Officer", "Procurement & Logistics", "Jinja HQ", "Active", "Today 09:40"),
    ("samuel", "Samuel Kato", "s.kato@idiu.org", "Executive Approver", "Country Director's office", "Jinja HQ", "Active", "Today 07:55"),
    ("esther", "Esther Namutebi", "e.namutebi@idiu.org", "Evaluation Committee Member", "Programmes", "Jinja HQ", "Active", "Today 09:18"),
    ("peter", "Peter Mukasa", "p.mukasa@idiu.org", "Inspection Officer", "Administration", "Jinja HQ", "Active", "Today 08:47"),
    ("harriet", "Harriet Kyomuhendo", "h.kyomuhendo@idiu.org", "Requesting Officer", "Programmes", "Jinja HQ", "Active", "Today 09:05"),
    ("ivan", "Ivan Ssemanda", "i.ssemanda@idiu.org", "System Administrator", "ICT", "Jinja HQ", "Active", "Today 09:36"),
    ("agnes", "Agnes Akello", "a.akello@idiu.org", "Auditor", "Internal Audit", "Jinja HQ", "Active", "Fri 9 Oct"),
]
USER_COUNT = 34

# ---------------------------------------------------------------- audit trail
# event, module, description, who, when, ago, outcome
AUDIT = [
    ("Procurement file closed", "Procurement file", "PR-2026-0087: all documents complete", "joseph", "12 Oct 2026, 09:41", "just now", "Success"),
    ("Payment reference recorded", "Procurement file", "PR-2026-0087: EFT-STB-26-10-0331, UGX 36,400,000", "ruth", "12 Oct 2026, 09:38", "3 minutes ago", "Success"),
    ("Sign-in failed", "Security", "Wrong password for s.kato@idiu.org (attempt 1 of 5)", None, "12 Oct 2026, 07:54", "2 hours ago", "Failed"),
    ("Evaluation scores submitted", "Evaluation", "PR-2026-0090: Brian Ouma scored 3 bids", "brian", "11 Oct 2026, 16:20", "Yesterday", "Success"),
    ("Budget revision submitted", "Budget", "BR-2026-0007: Teacher ICT Initiative, Kamuli", "ruth", "9 Oct 2026, 16:12", "3 days ago", "Success"),
    ("Goods received note recorded", "Delivery", "GRN-2026-0064 against LPO-2026-0051: 10 of 10 accepted", "peter", "9 Oct 2026, 14:42", "3 days ago", "Success"),
    ("User updated", "Users", "Daniel Okello: acting approver set to Rebecca Achan (19–30 Oct)", "ivan", "8 Oct 2026, 11:05", "4 days ago", "Success"),
    ("LPO issued", "Purchase order", "LPO-2026-0051 to Busoga Tech Supplies Ltd, UGX 36,400,000", "joseph", "6 Oct 2026, 11:30", "6 days ago", "Success"),
    ("Award approved", "Evaluation", "PR-2026-0087: Busoga Tech Supplies Ltd recommended", "samuel", "5 Oct 2026, 09:20", "7 days ago", "Success"),
    ("Budget revision approved", "Budget", "BR-2026-0006: Head office operations", "samuel", "22 Sep 2026, 10:14", "3 weeks ago", "Success"),
]
AUDIT_COUNT = 18_436

# ---------------------------------------------------------------- dashboard figures (Joseph, today)
STAGE_COUNTS = [("Requested", 6), ("Approved", 2), ("Sourcing", 3), ("Evaluation", 2), ("Award", 1), ("LPO", 4),
                ("Delivered", 2), ("Paid", 1)]   # open files; the Paid one is LPO-2026-0050, awaiting close-out
OPEN_FILES = sum(c for _, c in STAGE_COUNTS)
FY_SPEND_BY_MONTH = [18.2, 24.6, 41.3, 38.9, 29.4, 52.1, 47.8, 61.5, 72.3, 74.9]   # UGX M committed, Jan–12 Oct (Oct = "LPOs this month")
CYCLE_DAYS = 19   # average requisition → LPO, this FY

VALUE_BY_CATEGORY = [("ICT equipment & services", 182.4, KOICA), ("Construction & works", 104.4, VIOLET),
                     ("Furniture", 47.25, BRAND_M), ("Printing & stationery", 41.6, TEAL),
                     ("Training & events", 28.9, AMBER_D), ("Other", 19.7, GREY)]
