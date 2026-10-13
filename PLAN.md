# IDIU Procurement Management System: mockup plan

The design record for the clickable mockup: what the system is, who uses it, how records move, and every
screen with where it links. **Read this before adding or changing a screen.** The README explains how
screens are generated; this file explains what they must say. [`PATTERNS.md`](PATTERNS.md) holds the reusable
rules (front door, roles and sessions, page vs dialog, approvals in place).

- **Client:** International Development Institute Uganda (IDIU), Plot 45 Wilson Avenue, Jinja (idiu.org).
  A Christian non-profit linked to Korea Food for the Hungry International (KFHI); KOICA is a donor. Projects
  in Kasese, Kamuli, Luuka, Mayuge, Amuria and Kumi.
- **Vendor:** New Wave Technologies (NWT). Technical proposal and financials: `../resorces/`.
- **Why the mockup exists:** IDIU's Procurement Officer asked (12 Oct 2026) for a demo "to test user
  permissions, approval workflows and data entry without altering any live configurations". Mockups are
  line item 2.0 (System Design) of the financial proposal.
- **Live:** https://idiu-pms.vercel.app (repo `bloodykheeng/idiu-pms`).

---

## 1. Decisions (settled; do not reopen without the user)

| Decision | Why | Rejected |
|---|---|---|
| **One system, one front door**: public site (Home · About · FAQs · Notices) → one Sign in for staff and suppliers (Register as a supplier, Forgot password) → a dashboard chosen by who signed in: staff get the console, a supplier the supplier portal, an applicant their application status | How real systems are linked (Alpha: `(main)` → `(auth)` → `dashboard/layout.tsx` picks `@investor` or `@admin` by role; SDS: landing → `/login` → role-shaped sidebar). The user: the mockup "starts at supplier registration" as if it were a separate system, "you design as if it's an essay, you don't reason how a system should be linked" | Registration as the entry; a supplier portal with no sign-in and dead menu entries |
| **A record opens as a full page inside the menu it was opened from, and the approver decides on it there** (the idea of Alpha's `RecordDetailsDialog`: details, approval timeline, action; not its dialog). **Dialogs only for small forms**: setup lists, users, a financial year | The user: an application "takes me back up to approvals… I can approve under the approvals or even under the supplier themselves"; then "leave dialogs in these small modules of setup, users etc., be wise, not everywhere". Samuel gets his own copy with the decision panel (`w21c-samuel`); everyone else sees the approval timeline and who it waits on | Rows that jump to My approvals; record dialogs for applications, revisions, budgets |
| **Every create / edit button works for whoever may use it** (forms are `write` screens with the roles allowed to fill them in) | The user found Add user, New financial year, New budget, New requisition and budget edits dead. The Auditor reads everything and fills in nothing; budgets and revisions are Finance's (and the System Administrator's); the Executive Approver approves them | Linking "New" buttons to one person's own draft (dead for everyone else) |
| **Under a dialog nothing is clickable**, and **the highlighted row in a list is the one to click** | The user: sidebar and theme buttons showed hotspots under the audit drawer; RFQs highlighted a row only Joseph could open | |
| **Suppliers are sessions too**, with a sidebar like the console's | Alpha's investor portal is a sidebar like its staff side; one frame reads as one system. Every portal screen is the company's own, so the company never changes on a click | A separate top-nav portal |
| **Web only**: staff console + supplier portal, all 1920×1080 | Proposal §16 promises a responsive web app; no app line in the budget | A mobile app; phone-width renders ("it's web only, this is just a mockup") |
| **One procurement file per purchase** (`PR-2026-0087`) holding RFQ, quotations, evaluation, LPO, GRN, payment reference | Every stage list opens the same file, so screens never link to a disconnected page | Separate unlinked RFQ / LPO records |
| **Every master list is its own menu item and screen** (like SDS) | A client sees a real system; one combined "setup" page looks vague | One Setup screen with tabs |
| **Master data first, in dependency order** (§4) | You cannot create a department user before the department exists | Starting from transactions |
| **Maker-checker on financial and supplier records** (§5), Alpha's engine | Budgets, requisitions, awards, LPOs and prequalification are controlled records | Approval on plain lists (departments, units) |
| **Budgets: line by line or Excel import, then approval; live budgets change only by revision** | Finance enters budgets both ways; an approved budget must not be silently edited | One-way upload |
| **One role per person, named as in the proposal's role table (§15)**: Requesting Officer, Department Head, Finance Officer, Procurement Officer, Evaluation Committee Member, Executive Approver, Inspection Officer, System Administrator, Auditor (+ Supplier) | The user: "why are we having two requesters… isn't this confusion, same role doing two different things" → "let's make everything match so everyone has one role". IDIU will hold each demo account against the proposal's table. The committee is a role (§15) granted by appointment per procurement with a declaration (§7). The proposal's Budget Holder (funds check → Finance Officer) and Procurement Manager (oversight → Executive Approver) stay folded in: IDIU is small, and w61 says so | Committee as an appointment on top of a Requester role; renamed or merged role names that don't match the proposal |
| **Illustrative names**, real organisation, places, projects and donors | Real IDIU staff evaluate it; guessing their roles would be presumptuous | Real staff names |
| **Example thresholds** UGX 5M / 30M, labelled "to be set from IDIU's procurement manual" | IDIU has not shared its manual | Inventing "official" numbers |
| **The system does not pay suppliers**: Finance records the payment reference | Proposal §10: reference-level integration is the guaranteed minimum | Showing a payment or accounting module |
| **Fresh 2026 look**, only identity taken from idiu.org (greens, logo) | Their WordPress site is old | Copying the website |
| **Sign in as any role** (demo) and an "Illustrative data" pill | Their ask: test permissions per role | |
| **Sessions, like the real app** (SDS: AuthContext + AppSidebar + routeAccess): whoever signs in keeps their own sidebar, name and Dashboard on every screen until they switch; a link never opens another person's own screen or a menu their role lacks | Presenting: the person and the menus changed from screen to screen, and Dashboard from the Country Director's sidebar opened the Procurement Officer's (the user: "confusion for nothing") | Baking each screen with whoever performs that step |
| **"Country Director" is a job title, "Executive Approver" the role**: every step, decision and "waiting on" on screen names the role; the job title appears only beside Samuel's name on his dashboard, in the department "Country Director's office", and in the note that the Executive Approver is the Country Director | The user, seeing "With the Country Director" on the applicant's page: "am I still seeing Country Director there, is that correct?" Mixing a person's job and a role is the confusion one-role-per-person removed | Using the job title for approval steps |
| **The System Administrator sees every menu; the Auditor all but My approvals; everyone else only theirs**, groups collapsed but visible | SDS: System Administrator is unscoped; the user: "system admin has to see all these, other people see only what they're supposed to see" | Admin seeing only Setup and Users |

**Out of scope** (the user: "don't add a lot of unnecessary functionality"): payments, stores / inventory /
assets, contract management, public tender portal, sealed e-bidding, procurement plan, SMS, AI, mobile app.

---

## 2. The story the screens tell

"Today" is **Monday 12 October 2026**, financial year **FY 2026** (1 Jan to 31 Dec). One flagship file is
complete and closed this morning; other files are in flight so every action screen has something real waiting.
(Why closed: had PR-0087 still been waiting for payment, every tab after it would contradict the file view.)

| File | What | Project | Value (UGX) | Where it is today | Shown on |
|---|---|---|---|---|---|
| **PR-2026-0087** | 10 laptops for the second training room | Kasese ICT Hub (KOICA) | 38,000,000 est. · LPO 36,400,000 | Paid (09:38) and closed (09:41) today | The file's 8 tabs: w11 Overview, w11b Approvals, w12c Sourcing, w13d Evaluation, w14b LPO, w15d Delivery, w15c Payment, w11c Documents & history |
| PR-2026-0096 | Solar backup system | Kasese ICT Hub | 34,500,000 | Awaiting Executive Approver (step 3 of 3) | Approval decision (w02b) |
| PR-2026-0095 | Hygiene kits for model homes | Model Home Health, Kumi | 3,600,000 | Awaiting the Department Head (step 1 of 2) | Daniel's decision (w03b) |
| PR-2026-0093 | Network switches and cabling | Teacher ICT Initiative, Kamuli | 14,200,000 | RFQ-2026-0035 open, closes Wed 14 Oct | Busoga Tech quotes in the portal (w72) |
| PR-2026-0091 | Desks and chairs | Teacher ICT Initiative, Kamuli | 18,600,000 | Approved, waiting for an RFQ | New RFQ (w12b) |
| PR-2026-0090 | Washroom block, Busalamu P/S | Busalamu School Sanitation, Luuka | 86,000,000 | Committee evaluation | Committee scoring (w13b) |
| PR-2026-0089 | Printing teacher training manuals | Teacher ICT Initiative, Kamuli | 31,200,000 | Award awaiting the Executive Approver | Award approval (w13c) |
| PR-2026-0084 | Stationery for vocational classes | Women's Vocational Training, Mayuge | 6,800,000 | Delivery arriving today | Goods received (w15b) |
| PR-2026-0098 | Projector and screen | Kasese ICT Hub | 4,200,000 | Being drafted by Grace | New requisition (w10b) |

**PR-2026-0087, step by step** (the trail its history, approvals and audit entries must agree with):

1. 14 Sep 09:12, Grace Atim raises it: 10 × laptop (Core i5, 16 GB, 512 GB SSD, 14", Windows 11 Pro,
   screen reader ready, 3-year warranty) at UGX 3,800,000 = 38,000,000. Line 5210 ICT equipment, Kasese
   field office. Needed by 16 Oct.
2. 14 Sep 15:40 Daniel Okello (Head of Programmes) approves. 15 Sep 10:05 Ruth Nakato (Finance) confirms
   funds. 16 Sep 08:47 Samuel Kato (Executive Approver) approves: above UGX 30M, so step 3 applies.
3. 17 Sep Joseph Waiswa sends RFQ-2026-0031 to 4 prequalified ICT suppliers, closing 28 Sep 12:00.
4. Quotes: Busoga Tech Supplies 36,400,000 (10 days, 3-yr warranty); Source Point ICT 35,200,000 (21 days,
   1-yr warranty, **non-compliant**); Kagulu Computers 39,900,000 (7 days, 3-yr). Nile Bridge Systems did
   not respond.
5. 30 Sep to 1 Oct the committee (Esther Namutebi, chair; Brian Ouma; Moses Tumusiime) declares no
   conflict and scores (technical 70, financial 30): Busoga Tech 88.4, Kagulu 84.1.
6. 2 Oct Joseph submits the award recommendation; 5 Oct 09:20 Samuel approves it.
7. LPO-2026-0051, 36,400,000 to Busoga Tech Supplies: Finance 5 Oct, Executive Approver 6 Oct, issued 6 Oct
   11:30. Deliver to Kasese ICT Hub by 16 Oct.
8. 9 Oct delivery note DN-4471; Brian Ouma (ICT) and Grace Atim inspect at Kasese: 10 received, 10 accepted.
   Peter Mukasa records GRN-2026-0064.
9. Invoice BTS-INV-0912 (36,400,000) recorded 12 Oct 09:12: three-way match passes. **Today** 09:38 Ruth records
   payment reference EFT-STB-26-10-0331 (voucher PV-2026-1184); 09:41 Joseph closes the file.

**Second story:** Mpumudde Furniture Works applies for prequalification in *Furniture* (w70, w70b, w70c); Joseph
reviews it and recommends; it waits for the Executive Approver (w21b). Until approved it cannot be invited:
the New RFQ for desks (w12b) shows it greyed "prequalification pending", and Joseph adds a non-prequalified
local workshop with a recorded reason to reach 3 quotes.

**Budgets:** FY 2026 budgets are all active (w30). FY 2027 (planning) has two drafts: Model Home Health entered
line by line (w30c) and Kasese ICT Hub imported from Excel with 3 rows to fix (w30d). A revision to an active
budget (BR-2026-0007, Kamuli) waits for the Executive Approver (w31b).

### Cast (illustrative)

| Person | Role | Department · office | Signs in to |
|---|---|---|---|
| Grace Atim | Requesting Officer (Programme Officer, Kasese ICT Hub) | Programmes · Kasese | w10b her new requisition |
| Harriet Kyomuhendo | Requesting Officer (Programme Officer, field projects): raised PR-0084 to PR-0095 | Programmes · Jinja HQ | not a demo sign-in |
| Daniel Okello | Department Head (Head of Programmes); away 19–30 Oct, Rebecca Achan acts | Programmes · Jinja HQ | w03 his approvals |
| Ruth Nakato | Finance Officer | Finance · Jinja HQ | w30 Budgets |
| Joseph Waiswa | Procurement Officer | Procurement & Logistics · Jinja HQ | w01-joseph Dashboard |
| Samuel Kato | Executive Approver (job: Country Director) | Country Director's office · Jinja HQ | w02 My approvals |
| Esther Namutebi, Brian Ouma, Moses Tumusiime | Evaluation Committee Members, appointed per procurement (Esther chairs) | Programmes / ICT / Finance | w13-esther My evaluations (Esther) |
| Peter Mukasa | Inspection Officer (stores) | Administration · Jinja HQ | w15 Deliveries |
| Rebecca Achan | Department Head, Administration: Daniel's acting approver | Administration · Jinja HQ | not a demo sign-in |
| Ivan Ssemanda | System Administrator | ICT · Jinja HQ | w60 Users |
| Agnes Akello | Auditor (read-only) | Internal Audit · Jinja HQ | w63 Audit trail |
| Amos Waiswa (Busoga Tech Supplies) | Supplier, prequalified (ICT) | | w71 Supplier portal home |
| Fatuma Nabirye (Mpumudde Furniture Works) | Supplier, applied and pending | | w70d My application (registered through w70 → w70c) |

Suppliers (fictional): **ICT** Busoga Tech Supplies Ltd, Source Point ICT Ltd, Kagulu Computers Ltd, Nile
Bridge Systems Ltd · **Furniture** Wairaka Woodworks Ltd, Iganga Office Furnishers, Mpumudde Furniture Works
(applying) · **Printing** Jinja Print & Pack Ltd, Busoga Printers Ltd, Source Line Graphics · **Works**
Kakira Builders Ltd, Mutai Engineering Ltd, Lake Basin Contractors · **Stationery** Main Street Stationers,
Jinja Office Mart · **Solar** SunPower Busoga Ltd.

---

## 3. Roles

| Role | Does | Lands on |
|---|---|---|
| Requesting Officer | Raises requisitions, follows them, answers returns | Dashboard (my requisitions) |
| Department Head | Step 1 of requisitions from their department | My approvals |
| Finance Officer | Budgets (maker), funds check on requisitions and LPOs, payment reference | Budgets |
| Procurement Officer | Supplier review, RFQs, comparison, award recommendation, LPOs, close-out | Dashboard |
| Evaluation Committee Member | Scores the evaluations they are appointed to (per procurement, after a declaration); menu: Dashboard, Evaluations | Dashboard (my evaluations) |
| Executive Approver | The Country Director: high-value requisitions, awards, LPOs, budgets, revisions, prequalification, workflow changes (also the proposal's Procurement Manager oversight) | My approvals |
| Inspection Officer | Goods received and inspection | Deliveries |
| System Administrator | Setup lists, users, roles, approval workflows (changes approved by the Executive Approver) | Users |
| Auditor | Reads everything, changes nothing, audit trail | Audit trail |
| Supplier (external) | Registers, documents, quotations, LPOs, sees payment references | Supplier portal home (w71); a pending applicant, their application (w70d) |

**Permissions are visible:** each role's sidebar only shows what that role may open (from the role matrix
in `data.py`, the same matrix w61 shows).

---

## 4. Master data, in the order it must exist

```
Financial years → Departments → Offices & cost centres → Donors → Projects → Account codes
  → Budgets & budget lines → Procurement categories → Supplier document types → Units of measure
  → Approval workflows → Users (department, office, role, acting approver)
```

| List | Example rows | Depends on | Used by |
|---|---|---|---|
| Financial years | FY 2025 (closed), **FY 2026 (open)**, FY 2027 (planning) | | Budgets |
| Departments | Programmes, Finance, Procurement & Logistics, Administration, ICT, Country Director's office, Internal Audit | | Users, requisitions, HoD routing |
| Offices & cost centres | JIN Jinja HQ, KSE Kasese, KML Kamuli, LUU Luuka, MAY Mayuge, AMU Amuria, KUM Kumi | | Requisitions, budgets, delivery address |
| Donors | KOICA, KFHI, IDIU own funds | | Projects |
| Projects | Kasese ICT Hub (KOICA) · Teacher ICT Initiative, Kamuli (KFHI) · Busalamu School Sanitation, Luuka (KFHI) · Women's Vocational Training, Mayuge & Amuria (KFHI) · Model Home Health, Kumi (KFHI) · Head office operations (IDIU) | Donor, department, office | Budgets, requisitions |
| Account codes | 5110 Office supplies & stationery · 5120 Printing · 5210 ICT equipment · 5220 Furniture · 5230 Solar & electrical · 5310 Construction & works · 5410 Training materials · 5420 Venues & meals · 5510 Vehicles & motorcycles · 5610 Health supplies | | Budget lines, accounting export |
| Procurement categories | ICT · Furniture · Printing & stationery · Construction & works · Solar & electrical · Training & events · Vehicles & spares · Health supplies | Document types | Suppliers, RFQs |
| Supplier document types | Certificate of incorporation · TIN certificate · Trading licence (expires) · URA tax clearance (expires) · NSSF clearance (expires) · Bank letter · Professional licence (works, expires) · Company profile & references | | Registration, expiry alerts |
| Units of measure | Piece, Set, Box, Ream, Carton, Lot, Litre, Day, Trip | | Requisition and LPO lines |

Rules: Admin creates and edits; a list row is **Active / Inactive**; a row already used is **deactivated,
never deleted** (the list shows "used by" counts). No approval on plain lists.

---

## 5. Approvals (Alpha's engine)

```
Draft ──Submit──▶ Pending approval ──Approve (last step)──▶ Approved / Active / Issued
  ▲                     │
  └──Return / Reject────┘   reason required · a return goes back to the maker as Draft
```

- One workflow per record type; ordered steps, each needing a role; a step may apply only **above an amount**.
- The steps are **copied onto the request when submitted**: editing a workflow never changes one in flight.
- **Maker-checker:** whoever prepared or submitted a record can't approve or reject any of its steps.
- **Comment required** on Return and Reject.
- Live records are never edited directly: a change to an active budget is a **revision** (old → new).
- **Overdue:** a step waiting more than 2 working days reminds its approvers, then the Executive Approver.
- **Acting approver:** set on a user while away; their approvals route to that person.

| Record | Maker | Steps (example) |
|---|---|---|
| Requisition | Requesting Officer | 1 Department Head · 2 Finance Officer (funds; the proposal's Budget Holder) · 3 Executive Approver, **only ≥ UGX 30M** |
| Award recommendation | Procurement Officer | 1 Executive Approver |
| LPO | Procurement Officer | 1 Finance Officer (commitment) · 2 Executive Approver, **only ≥ UGX 5M** |
| Budget | Finance Officer | 1 Executive Approver |
| Budget revision | Finance Officer | 1 Executive Approver |
| Supplier prequalification | Procurement Officer (recommends) | 1 Executive Approver |
| Approval workflow change | System Administrator | 1 Executive Approver |

**Methods by value (example, to be set from IDIU's procurement manual):**

| Value (UGX) | Method | Quotes | Evaluation |
|---|---|---|---|
| up to 5M | Direct purchase | 1 | Procurement Officer |
| 5M to 30M | Request for quotations | 3 or more | Quotation comparison |
| above 30M | Request for quotations + committee | 3 or more | Evaluation committee |

**Budget money:** Budget − Reserved (approved requisitions) − Committed (issued LPOs) − Spent (payment
references) = Available. Requisitions use **active** lines only.

**Procurement file stages (the file track):**
Requested → Approved → Sourcing → Evaluation → Award → LPO → Delivered → Paid → Closed.
Side states: Returned · Rejected · Cancelled. Direct purchases skip Evaluation (shown as skipped).

---

## 6. Screens and links

**The front door.** No hash opens the public Home (w80). Every public page has Sign in; Home, Notices and FAQs lead to Register. Sign in is one page for everyone; the demo "sign in as" lists the 9 staff and the 2 supplier accounts, each landing on their own dashboard (`data.home_key`). Signing out (the red button in any sidebar) returns to Home; clicking the name returns to Sign in to switch accounts.

**Sessions.** A screen is either one person's own (their dashboard, their decisions: `owner`) or shared (lists, the procurement file, setup, reports), drawn as the System Administrator sees it. The prototype keeps whoever signed in: on a shared screen it lays that person's own sidebar and name over it (`chrome/`), and it hides any hotspot to another person's own screen or to a menu their role lacks. Menus per role are `PERMS` in `data.py` (System Administrator: all 26; Auditor: all but My approvals). A file's tabs belong to the menu that leads to them (Delivery → Deliveries, Evaluation → Evaluations), so Peter can open the GRN from his Deliveries list but not the rest of the file.

Keys are what hotspots and URLs use (`prototype.html#w11`). The viewer lists the public site first (w80–w83), then w00 onwards. Every list row opens the procurement file; every
action returns to the file or the list it came from.

### Public site and the door (nobody signed in)

| Key | Screen | Links out |
|---|---|---|
| w80 | Home: what IDIU's procurement is, how a purchase moves, For suppliers · For staff · Notices | Sign in → w00; Register → w70; the open round → w83; header and footer |
| w81 | About: who IDIU is, what the system does, how we buy, method by value (example) | header, footer |
| w82 | FAQs (Suppliers · IDIU staff · Payments), still need help | Register → w70; Reset it → w00b |
| w83 | Notices: prequalification for 2027 (open until Fri 20 Nov), award notices | Register → w70; Sign in to renew → w00 |
| w00 | Sign in: one door for staff and suppliers; demo "sign in as" in the order the work flows (1 Ivan sets up, 2 Ruth budgets, 3 Grace requests, 4 Daniel, 5 Samuel approve, 6 Joseph owns the purchase, 7 Esther scores, 8 Peter receives, 9 Agnes audits; suppliers: 1 Mpumudde applies, 2 Busoga quotes) | each account's own dashboard; Register → w70; Forgot password → w00b; Back to home → w80 |
| w00b | Forgot password | Send link / Sign in → w00 |
| w70 | Register: company, sign-in and categories (Mpumudde) | Continue → w70b; Back; Sign in → w00 |
| w70b | Register: documents and declaration | Submit → w70c; Back → w70 |
| w70c | Application submitted (what happens next) | Follow my application → w70d; Back to home → w80 |

### Staff console

| Key | Screen (viewer) | Links out |
|---|---|---|
| w01-<person> | Each person's own Dashboard (ivan, samuel, daniel, joseph, ruth, grace, esther, peter, agnes): Your turn, four figures from what their role opens, the organisation's panels or their own rows | their own actions; shared lists they may open |
| w02-ruth, w02-ivan | My approvals with nothing waiting (empty state, recently decided) | decided rows → file tabs, LPO |
| w02 | My approvals (Samuel) | rows → w02b, w13c, w31b, w21b; recently decided → w11b, w14b |
| w02b | Approve requisition PR-0096, step 3 of 3 (Samuel) | Approve / Return / Reject → w02 |
| w03 | My approvals (Daniel, Department Head) | PR-0095 (Harriet's) → w03b |
| w03b | Approve requisition PR-0095, step 1 of 2 (Daniel) | Approve / Return / Reject → w03 |
| w10 | Requisitions (page 1 of 98) | New requisition → w10c; PR-0087 → w11; PR-0096 → w10d; PR-0095 → w10e; PR-0098 → w10b (Grace's); PR-0091 → w12b (Joseph's) |
| w10b | Grace's draft requisition PR-0098 (from her dashboard) | Submit / Save draft → w10 |
| w10c | New requisition, blank, for whoever is signed in (not the Auditor) | Submit / Save draft / Cancel → w10 |
| w10d, w10d-samuel | Requisition PR-0096 page under Requisitions: read only with "Waiting on Samuel Kato"; Samuel decides on his copy | from w10, Grace's dashboard, Daniel's recently decided; → w10 |
| w10e, w10e-daniel | Requisition PR-0095 page under Requisitions; Daniel decides on his copy | from w10; → w10 |
| w11 | File PR-0087: Overview | tabs; budget line → w30b |
| w11b | File: Approvals (requisition, award, LPO steps) | tabs |
| w11c | File: Documents & history | tabs; full audit trail → w63 |
| w12 | RFQs & quotations (RFQ-0031, the laptops, highlighted) | RFQ-0031 → w12c; RFQ-0036 → w12b (Joseph's) |
| w12b | New RFQ for PR-0091 (Joseph) | Send / Save draft → w12 |
| w12c | File: Sourcing (quotation comparison) | tabs |
| w13 | Evaluations: all committees (Procurement, Finance, Executive Approver, auditor) | PR-0087 → w13d |
| w13-esther | My evaluations (Esther, Evaluation Committee Member) | PR-0090 → w13b; PR-0087 → w13d |
| w13b | Committee scoring PR-0090 (Esther) | Submit / Save → w13 |
| w13c | Approve award PR-0089 (Samuel) | Approve / Return / Reject → w02 |
| w13d | File: Evaluation | tabs |
| w13e, w13e-samuel | Award PR-0089 page under Evaluations: report, recommendation, timeline; Samuel decides on his copy | from w13, w13-esther, w12 (RFQ-0032), Esther's dashboard; → w13 |
| w14 | Purchase orders | LPO-0051 → w14b |
| w14b | File: LPO-2026-0051 document | tabs |
| w15 | Deliveries (LPO-0051 highlighted) | LPO-0051 → w15d; LPO-0049 → w15b (Peter's) |
| w15b | Goods received & inspection LPO-0049 (Peter) | Save GRN / draft → w15 |
| w15c | File: Payment & close-out (three-way match, payment reference, closed) | tabs |
| w15d | File: Delivery (GRN-0064) | tabs |
| w20 | Supplier register | Busoga Tech → w20b; Applications → w21 |
| w20b | Supplier profile: Busoga Tech Supplies | LPO-0051 → w14b |
| w21 | Prequalification applications | Mpumudde → w21c |
| w21b | Prequalification decision: Mpumudde (Samuel, from My approvals) | Prequalify / Return / Reject → w02 |
| w21c | Application page under Suppliers › Applications: documents, recommendation; approval panel "Waiting on Samuel Kato" | sidebar, crumbs |
| w21c-samuel | The same page as Samuel sees it: Prequalify / Return / Reject | → w21 |
| w30 | Budgets FY 2026 | Kasese → w30b; New budget / Import from Excel → w30e; Model Home Health 2027 → w30c; Kasese 2027 → w30d (Ruth's drafts) |
| w30b | Budget: Kasese ICT Hub FY 2026 | Request revision → w31c; PR-0087 → w11; PR-0098 → w10b |
| w30e | New budget (page): financial year, project, lines one by one or from Excel (Finance, System Administrator) | Save draft / Cancel → w30 |
| w30c | Draft budget FY 2027, line by line: Model Home Health | Submit / Save → w30; Import → w30d |
| w30d | Import budget from Excel: Kasese ICT Hub FY 2027 (3 rows to fix) | Save ready lines → w30 |
| w31 | Budget revisions | New revision → w31c; BR-0007 → w31d |
| w31b | Approve budget revision BR-0007 (Samuel, from My approvals) | Approve / Return / Reject → w02 |
| w31c | Request a budget revision: Kasese, 5230 −8M → 5220 +8M, total unchanged (how an active budget is edited) | Submit / Save draft / Cancel → w31 |
| w31d, w31d-samuel | Revision page under Budgets › Budget revisions (read only with who it waits on; Samuel decides on his copy) | → w31 |
| w40 | Report: Procurement register | PR-0087 → w11 |
| w41 | Report: Budget utilisation | Kasese → w30b |
| w50b | New financial year (dialog: FY 2028, planning) | Save / Cancel → w50 |
| w52b, w53b, w55b–w58b | New office, donor, account code, procurement category, supplier document type, unit (dialogs; any role whose menu has the list, never the Auditor) | Save / Cancel → the list |
| w50–w58 | Setup: financial years, departments, offices, donors, projects, account codes, procurement categories, supplier document types, units of measure (one screen each) | sidebar |
| w51b | New department (dialog) | Save / Cancel → w51 |
| w54b | New project (form, with the setup order) | Save / Cancel → w54 |
| w60 | Users | Add user → w60c; Daniel → w60b |
| w60b | Edit user: Daniel (one role, acting approver Rebecca Achan 19–30 Oct; System Administrator only) | Save / Cancel → w60 |
| w60c | Add user (dialog: name, phone, email, department, office, role, first password; email the sign-in details) | Add user / Cancel → w60 |
| w61 | Roles & permissions (matrix) | |
| w62 | Approval workflows + methods by value | Requisition → w62b |
| w62b | Edit workflow: Requisition (threshold 30M → 25M, goes to the Executive Approver) | Submit / Cancel → w62 |
| w63 | Audit trail (Agnes) | BR-0006 → w63b |
| w63b | Audit entry: budget revision approved (old → new, where from) | close → w63; full history → w31 |

### Supplier portal (signed in as a supplier; every screen is the company's own)

Menu (`data.SUPPLIER_MENU`): Busoga Tech: Home · WORK RFQs, Purchase orders, Payments · MY COMPANY Company profile,
Documents. Mpumudde (pending): My application only, until the Executive Approver prequalifies it (w21b).

| Key | Screen | Links |
|---|---|---|
| w70d | My application (Mpumudde): where it is (with the Executive Approver), documents checked, what opens when prequalified | sidebar; sign out → w80 |
| w71 | Home (Busoga Tech): renew for 2027, four figures, the open RFQ, latest payment, LPOs | RFQ-0035 → w72; All RFQs → w73; LPO-0051 → w74b; Payments → w75; Renew → w77b |
| w72 | Submit quotation RFQ-0035 (sealed until 14 Oct) | Submit / Save draft → w73 |
| w73 | RFQs: 1 open, 7 past (6 quoted, 4 awarded) | RFQ-0035 → w72; RFQ-0031 → w74b |
| w74 | Purchase orders (4, all delivered and paid) | LPO-0051 → w74b |
| w74b | LPO-2026-0051: the order and its progress (acknowledged 6 Oct 14:02 → paid 12 Oct) | Payments → w75 |
| w75 | Payments: payment references Finance recorded (the system does not move money) | LPO-0051 → w74b |
| w76 | Company profile: details, bank account (changes checked by IDIU), people on the account | Documents → w77 |
| w77 | Documents: 7 on file; the declaration renews for 2027 | Renew → w77b |
| w77b | Renew prequalification for 2027 (dialog) | Submit / Cancel → w77 |

Every screen is reachable from the public Home, every menu entry opens a screen, and no click shows another
person's or company's screen; all checked on each build (README §6).

---

## 7. Look

| Token | Hex | Use |
|---|---|---|
| Forest ink | `#102A1E` | Text |
| Field green | `#1A683F` | IDIU's brand green: buttons, active states |
| Mint | `#4EAE8B` | Logo green: progress, done, charts |
| Fresh lime | `#D9F0B8` | "Your turn", the current stage |
| Sage canvas | `#F3F6F2` | Page background |
| Signal amber | `#F2A93B` | Waiting, overdue (red `#D1443C` only for rejected) |

KOICA blue `#1855A5` only on donor tags. Type: **Bricolage Grotesque** (titles, big figures), **Figtree**
(everything else), **IBM Plex Mono** (reference numbers only), all embedded in each SVG.

**Signature:** the file track (stages + "Waiting on: <person> · <time>") on the file and as a mini-track in
lists. **Supporting:** the budget bar (spent · committed · reserved · available).

From SDS (`sdstool.ug`): collapsible sidebar groups, greeting header, KPI cards with help icons, the list
toolbar (search · filter · + New · export · columns), a relation subtitle under each list title, status
chips, "Showing 1 to 10 of N", audit trail with module chips. New: view opens a side drawer, "used by"
counts with Deactivate instead of Delete, Ctrl+K search.

---

## 8. Open questions for IDIU

| Question | Blocks | Default in the mockup |
|---|---|---|
| Their procurement manual: methods, thresholds, who approves | Approval workflows | Example 5M / 30M thresholds, labelled |
| Accounting package and chart of accounts | Account codes, the export | Illustrative 5xxx codes; Excel export + payment reference |
| Is there a Finance Manager separate from the Finance Officer? | Budget approval step | Executive Approver approves budgets |
| Financial year (Jan–Dec or Jul–Jun) and donor budget periods | Budgets | FY 2026 = Jan to Dec |
| Who sits on evaluation committees; standing or per procurement? | Committee screens | A role, appointed per procurement |
| Do they use a Budget Holder or Procurement Manager separate from Finance and the Executive Approver? | Roles | Folded in (w61 note) |
| A working sandbox (enter data, run approvals) after the mockup? | Their "test data entry" ask | Mockup shows flows; a sandbox needs a build |
