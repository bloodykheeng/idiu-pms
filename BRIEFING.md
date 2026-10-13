# IDIU Procurement Management System: team briefing

> **For the New Wave Technologies (NWT) team** presenting the mockup to IDIU. Share it freely inside the team: this
> page is public (GitHub and Vercel), so it holds **no prices and nothing confidential**.
>
> **Prototype:** https://idiu-pms.vercel.app. Every screen link below opens that screen directly.
> **This page:** https://github.com/bloodykheeng/idiu-pms/blob/main/BRIEFING.md

**Contents:** [1. In 30 seconds](#1-in-30-seconds) · [2. What they asked for, and where it is](#2-what-they-asked-for-and-where-it-is) ·
[3. Words they will use](#3-words-they-will-use) · [4. Roles and who plays them](#4-roles-and-who-plays-them) ·
[5. How a purchase moves](#5-how-a-purchase-moves) · [6. Walkthrough script](#6-walkthrough-script-about-12-minutes) ·
[7. Likely questions](#7-likely-questions-and-short-answers) · [8. Questions to clear with IDIU](#8-questions-to-clear-with-idiu) ·
[9. Watch-outs before the demo](#9-watch-outs-before-the-demo) · [10. Screen index](#10-screen-index)

---

## 1. In 30 seconds

- **The client:** International Development Institute Uganda (IDIU), Plot 45 Wilson Avenue, Jinja (idiu.org). A
  Christian non-profit working with Korea Food for the Hungry International (KFHI), with KOICA as a donor. Projects
  in Kasese, Kamuli, Luuka, Mayuge, Amuria and Kumi.
- **The ask (12 Oct 2026, Mutungi Rodgers, Procurement Officer):** after reading our proposal, a demo so their team can
  *"thoroughly test user permissions, approval workflows, and data entry without altering any live configurations."*
- **What we show:** a clickable mockup of the whole system:
  - **a public site and one sign-in** for staff and suppliers;
  - **a staff console** where each person sees only their role's menus;
  - **a supplier portal**;
  - **one procurement file per purchase**, from budget to the payment reference, approved maker-checker and fully audited.
- **The honest limit:** it is a mockup (screens and clicks), not a working system. Their "data entry" test needs a
  sandbox build, which comes after requirements (see §7).
- All people, figures and suppliers are **illustrative**. IDIU's name, logo, offices, projects and donors are real.
  Thresholds are **examples** until IDIU shares its procurement manual.

---

## 2. What they asked for, and where it is

| They asked for | Where to show it |
|---|---|
| **User permissions** | Sign in as different people on [Sign in](https://idiu-pms.vercel.app/prototype.html#w00): each sidebar shows only that role's menus. The full matrix: [Roles & permissions](https://idiu-pms.vercel.app/prototype.html#w61) |
| **Approval workflows** (thresholds aligned with their manual) | [Approval workflows](https://idiu-pms.vercel.app/prototype.html#w62) and [editing one](https://idiu-pms.vercel.app/prototype.html#w62b) (the change itself needs approval); decisions: [requisition](https://idiu-pms.vercel.app/prototype.html#w02b), [award](https://idiu-pms.vercel.app/prototype.html#w13c), [budget revision](https://idiu-pms.vercel.app/prototype.html#w31b) |
| **Data entry** | [New requisition](https://idiu-pms.vercel.app/prototype.html#w10c), [New budget](https://idiu-pms.vercel.app/prototype.html#w30e), [budget line by line](https://idiu-pms.vercel.app/prototype.html#w30c), [Excel import with errors caught](https://idiu-pms.vercel.app/prototype.html#w30d), [Add user](https://idiu-pms.vercel.app/prototype.html#w60c), every setup list's New ([example](https://idiu-pms.vercel.app/prototype.html#w56b)) |
| **Supplier registration and prequalification** | [Register](https://idiu-pms.vercel.app/prototype.html#w70) → [documents](https://idiu-pms.vercel.app/prototype.html#w70b) → [submitted](https://idiu-pms.vercel.app/prototype.html#w70c) → [application status](https://idiu-pms.vercel.app/prototype.html#w70d); staff side: [Applications](https://idiu-pms.vercel.app/prototype.html#w21), [the decision](https://idiu-pms.vercel.app/prototype.html#w21c-samuel); [Supplier register](https://idiu-pms.vercel.app/prototype.html#w20) |
| **Requisitions, RFQs, quotation comparison** | [Requisitions](https://idiu-pms.vercel.app/prototype.html#w10), [New RFQ](https://idiu-pms.vercel.app/prototype.html#w12b), [quotation comparison](https://idiu-pms.vercel.app/prototype.html#w12c) |
| **Committee evaluations** | [Committee scoring](https://idiu-pms.vercel.app/prototype.html#w13b) (declaration first), [the file's evaluation](https://idiu-pms.vercel.app/prototype.html#w13d) |
| **LPOs, deliveries and inspections** | [LPO](https://idiu-pms.vercel.app/prototype.html#w14b), [goods received with a partial delivery](https://idiu-pms.vercel.app/prototype.html#w15b), [the file's delivery](https://idiu-pms.vercel.app/prototype.html#w15d) |
| **Budget tracking by centre, project and line** | [Budgets](https://idiu-pms.vercel.app/prototype.html#w30), [Kasese ICT Hub FY 2026](https://idiu-pms.vercel.app/prototype.html#w30b), [Budget utilisation](https://idiu-pms.vercel.app/prototype.html#w41) |
| **Accounting compatibility** (consult Finance) | [Payment & close-out](https://idiu-pms.vercel.app/prototype.html#w15c): three-way match, the EFT reference Finance records; [Account codes](https://idiu-pms.vercel.app/prototype.html#w55) map to the accounting package |
| **Export data and documents** | [Documents & history](https://idiu-pms.vercel.app/prototype.html#w11c) (download the complete file); export icons on every list |
| **Audit** | [Audit trail](https://idiu-pms.vercel.app/prototype.html#w63) and [one entry, old → new](https://idiu-pms.vercel.app/prototype.html#w63b) |
| **Ease of use** | [Each person's dashboard](https://idiu-pms.vercel.app/prototype.html#w01-joseph) opens on "Your turn": what is waiting on them |

---

## 3. Words they will use

| Word | Means |
|---|---|
| **Requisition (PR)** | A staff request to buy something, charged to a project's budget line. Every purchase starts here |
| **RFQ** | Request for quotations, sent to prequalified suppliers in a category |
| **Prequalification** | A supplier is checked (documents, sometimes a visit) and approved for categories before it can be invited |
| **Evaluation committee** | Staff appointed per purchase to score quotations; each signs a no-conflict-of-interest declaration first |
| **Award** | The decision on which supplier wins, recommended by Procurement and approved by the Executive Approver |
| **LPO** | Local purchase order: the order sent to the winning supplier |
| **GRN** | Goods received note: what arrived, what was accepted or rejected, at inspection |
| **Three-way match** | LPO, GRN and the supplier's invoice agree before payment |
| **Maker-checker** | Whoever prepares a record can't approve it |
| **Budget line, cost centre** | Where the money comes from (account code + project + office) |
| **Reserved, committed, spent** | Approved requisitions reserve money, LPOs commit it, payments spend it; what is left is "available" |
| **Revision** | The only way to change an approved budget: old → new, approved by the Executive Approver |
| **PPDA** | Uganda's Public Procurement and Disposal of Public Assets Authority; NGOs often follow its practice |
| **KOICA, KFHI** | Korea International Cooperation Agency (a donor); Korea Food for the Hungry International (IDIU's partner) |

---

## 4. Roles and who plays them

**One role per person, named as in our proposal's role table (§15).** The demo sign-in lists them in the order the work
flows. "Country Director" is Samuel's *job*; his *role* is Executive Approver.

| # | Person (illustrative) | Role | Their part | Starts on |
|---|---|---|---|---|
| 01 | Ivan Ssemanda | System Administrator | Sets up lists and users; sees every menu | [Dashboard](https://idiu-pms.vercel.app/prototype.html#w01-ivan) |
| 02 | Ruth Nakato | Finance Officer | Budgets, funds checks, payment references | [Dashboard](https://idiu-pms.vercel.app/prototype.html#w01-ruth) |
| 03 | Grace Atim | Requesting Officer | Raises requisitions | [Dashboard](https://idiu-pms.vercel.app/prototype.html#w01-grace) |
| 04 | Daniel Okello | Department Head | Approves step 1 for Programmes | [Dashboard](https://idiu-pms.vercel.app/prototype.html#w01-daniel) |
| 05 | Samuel Kato | Executive Approver (Country Director) | Final approvals: large requisitions, awards, LPOs, budgets, suppliers | [Dashboard](https://idiu-pms.vercel.app/prototype.html#w01-samuel) |
| 06 | Joseph Waiswa | Procurement Officer | Owns the purchase: suppliers, RFQs, comparison, award, LPO, close-out | [Dashboard](https://idiu-pms.vercel.app/prototype.html#w01-joseph) |
| 07 | Esther Namutebi | Evaluation Committee Member | Scores the evaluations she is appointed to | [Dashboard](https://idiu-pms.vercel.app/prototype.html#w01-esther) |
| 08 | Peter Mukasa | Inspection Officer | Receives and inspects goods | [Dashboard](https://idiu-pms.vercel.app/prototype.html#w01-peter) |
| 09 | Agnes Akello | Auditor | Reads everything, changes nothing | [Dashboard](https://idiu-pms.vercel.app/prototype.html#w01-agnes) |
| S1 | Mpumudde Furniture Works (Fatuma Nabirye) | Supplier, applying | Applies to prequalify | [Application](https://idiu-pms.vercel.app/prototype.html#w70d) |
| S2 | Busoga Tech Supplies (Amos Waiswa) | Supplier, prequalified | Quotes, delivers, sees payments | [Portal home](https://idiu-pms.vercel.app/prototype.html#w71) |

The proposal's **Budget Holder** (funds check) and **Procurement Manager** (oversight) are folded into the Finance
Officer and the Executive Approver for now. The roles screen says so, and it's a question for IDIU (§8).

---

## 5. How a purchase moves

```
Budget approved → Requisition → Department Head → Finance (funds) → Executive Approver (above UGX 30M)
  → RFQ to prequalified suppliers → quotations (sealed until closing) → comparison / committee evaluation
  → award approved → LPO (Finance, then Executive Approver above UGX 5M) → delivery + inspection (GRN)
  → invoice, three-way match → Finance records the payment reference → file closed
```

- **The flagship file, [PR-2026-0087](https://idiu-pms.vercel.app/prototype.html#w11):** 10 laptops for the Kasese ICT
  Hub (KOICA), UGX 38M estimated, LPO UGX 36.4M to Busoga Tech. It is **paid and closed today**, so its eight tabs tell
  the whole story with no gaps.
- **Other files are mid-way**, so every action screen has something real waiting:
  - a requisition with the Executive Approver;
  - one with the Department Head;
  - an RFQ open for quotes;
  - a committee scoring;
  - an award waiting;
  - a delivery arriving today.
- **Methods by value (examples):** up to UGX 5M direct purchase; 5M to 30M request for quotations (3 or more); above
  30M an evaluation committee.
- **The system does not pay suppliers.** Finance pays as today and records the payment reference.

---

## 6. Walkthrough script (about 12 minutes)

**Before you start:** open https://idiu-pms.vercel.app while online, wait for **"✓ Offline-ready"** in the bottom
bar, then press **F** for full screen. Say once: *"Names and figures are illustrative; IDIU, its projects, offices
and donors are real."*

1. **One front door** (1 min):
   - [Home](https://idiu-pms.vercel.app/prototype.html#w80), then [Notices](https://idiu-pms.vercel.app/prototype.html#w83): the open prequalification round and award notices.
   - [Sign in](https://idiu-pms.vercel.app/prototype.html#w00): one page for staff and suppliers, accounts in the order the work flows.
2. **Permissions** (1 min): [Roles & permissions](https://idiu-pms.vercel.app/prototype.html#w61) is the matrix every sidebar is drawn from. Sign in as two different people and compare their menus.
3. **Setup** as Ivan (1 min): [Departments](https://idiu-pms.vercel.app/prototype.html#w51) → [New department](https://idiu-pms.vercel.app/prototype.html#w51b); [Projects](https://idiu-pms.vercel.app/prototype.html#w54) (the order things must exist in); [Add user](https://idiu-pms.vercel.app/prototype.html#w60c); [Approval workflows](https://idiu-pms.vercel.app/prototype.html#w62).
4. **Budgets** as Ruth (2 min):
   - [Kasese FY 2026](https://idiu-pms.vercel.app/prototype.html#w30b): spent · committed · reserved · available.
   - [A FY 2027 draft, line by line](https://idiu-pms.vercel.app/prototype.html#w30c).
   - [Excel import catching three bad rows](https://idiu-pms.vercel.app/prototype.html#w30d).
   - [Editing an active budget = a revision](https://idiu-pms.vercel.app/prototype.html#w31c).
5. **Requisition** as Grace (1 min): [her draft](https://idiu-pms.vercel.app/prototype.html#w10b), with the live budget check and the approval path.
6. **Approvals** (2 min):
   - As Daniel, [step 1 of 2](https://idiu-pms.vercel.app/prototype.html#w03b).
   - As Samuel, [step 3 of 3](https://idiu-pms.vercel.app/prototype.html#w02b), with the maker-checker note and Approve / Return / Reject.
   - Then show he can decide [from Requisitions too](https://idiu-pms.vercel.app/prototype.html#w10d-samuel), not only from My approvals.
7. **Sourcing** as Joseph (1 min): his [dashboard](https://idiu-pms.vercel.app/prototype.html#w01-joseph) "your turn" → [the desks RFQ](https://idiu-pms.vercel.app/prototype.html#w12b) (only two prequalified, a third added with a reason).
8. **Evaluation** (1 min): as Esther, [scoring after her declaration](https://idiu-pms.vercel.app/prototype.html#w13b); as Samuel, [approving the printing award](https://idiu-pms.vercel.app/prototype.html#w13e-samuel).
9. **The complete file** (1 min): [PR-2026-0087](https://idiu-pms.vercel.app/prototype.html#w11), every tab from Overview to [Payment](https://idiu-pms.vercel.app/prototype.html#w15c); download the complete file.
10. **Delivery** as Peter (30 s): [a partial delivery](https://idiu-pms.vercel.app/prototype.html#w15b) with rejected and outstanding items.
11. **Suppliers** (1 min):
    - [Mpumudde registering](https://idiu-pms.vercel.app/prototype.html#w70) → [their status](https://idiu-pms.vercel.app/prototype.html#w70d) → [Samuel prequalifying](https://idiu-pms.vercel.app/prototype.html#w21c-samuel).
    - Busoga Tech [quoting](https://idiu-pms.vercel.app/prototype.html#w72), [the LPO they acknowledged](https://idiu-pms.vercel.app/prototype.html#w74b), [payments](https://idiu-pms.vercel.app/prototype.html#w75).
12. **Audit** as Agnes (30 s): [the trail](https://idiu-pms.vercel.app/prototype.html#w63) → [one entry, old → new](https://idiu-pms.vercel.app/prototype.html#w63b).

Close on their ask: permissions and approvals are shown; **testing real data entry needs a sandbox build**, which we
set up after requirements are agreed.

---

## 7. Likely questions, and short answers

| They may ask | Say |
|---|---|
| Can we enter our own data and test it? | Not in a mockup: these are designed screens. After requirements we set up a **sandbox** with your lists and users, separate from live, which is exactly the "test without altering live configuration" you asked for |
| Are these our thresholds and approvers? | **Examples** (UGX 5M / 30M). We configure them from your procurement manual; the workflow screen shows how a change is itself approved |
| Who are these people? | Illustrative. Your real staff and roles come from requirements; the role matrix is agreed then (proposal §15) |
| Why do approvers decide in two places? | The same record is in My approvals and in its list (Requisitions, Applications…): they decide wherever they are |
| Does it pay suppliers? | No. Finance pays as today and records the payment reference; the file then closes |
| Will it link to our accounting system? | At least by reference and Excel export, mapped to your chart of accounts; deeper integration is agreed with Finance |
| Does it work on phones? | It's a responsive web app (proposal §16); approvers can act from a phone. The mockup is shown at desktop size |
| Can someone approve while away? | Yes: an acting approver with dates, set on the user ([example](https://idiu-pms.vercel.app/prototype.html#w60b)) |
| Can suppliers see our RFQs publicly? | No. RFQs go only to prequalified suppliers in the category; the public site shows prequalification rounds and award notices |
| Can records be changed after approval? | No. Changes are revisions (old → new), and the audit trail can't be edited |
| Can we get our data out? | Yes: every list exports, and each file downloads complete with its documents |

---

## 8. Questions to clear with IDIU

- Their **procurement manual**: methods, thresholds, who approves at each level.
- **Accounting package and chart of accounts.**
- Is there a **Finance Manager**, **Budget Holder** or **Procurement Manager** separate from the Finance Officer and the Country Director?
- **Financial year** (Jan–Dec or Jul–Jun) and donor budget periods.
- **Evaluation committees**: standing or per procurement, and who sits on them.
- When they want the **sandbox** for hands-on testing.

---

## 9. Watch-outs before the demo

- **Hard-refresh (Ctrl+F5)** before presenting, so nobody sees an old cached version.
- Wait for **"✓ Offline-ready"**: then it keeps working if the venue's internet drops.
- **Full screen: F.** The bottom bar comes back when the mouse touches the very bottom edge. **Esc** exits.
- **H** shows every clickable area. **D** switches dark mode. **← →** step through screens in order.
- **Web dashboard** (bottom bar) always returns to the public Home.
- To switch person, click the name at the bottom of the sidebar (back to Sign in). The red button signs out to Home.
- Keep saying **"illustrative data"** and **"example thresholds"**. Don't promise features we've left out (payments, stores and inventory, contracts, a public tender portal).

---

## 10. Screen index

The full map, with every link, is in [PLAN.md §6](PLAN.md#6-screens-and-links). The most useful starting points:

| Area | Start here |
|---|---|
| Public site | [Home](https://idiu-pms.vercel.app/prototype.html#w80) · [About](https://idiu-pms.vercel.app/prototype.html#w81) · [FAQs](https://idiu-pms.vercel.app/prototype.html#w82) · [Notices](https://idiu-pms.vercel.app/prototype.html#w83) |
| Sign in | [Sign in](https://idiu-pms.vercel.app/prototype.html#w00) · [Forgot password](https://idiu-pms.vercel.app/prototype.html#w00b) · [Register](https://idiu-pms.vercel.app/prototype.html#w70) |
| Procurement | [Requisitions](https://idiu-pms.vercel.app/prototype.html#w10) · [RFQs](https://idiu-pms.vercel.app/prototype.html#w12) · [Evaluations](https://idiu-pms.vercel.app/prototype.html#w13) · [LPOs](https://idiu-pms.vercel.app/prototype.html#w14) · [Deliveries](https://idiu-pms.vercel.app/prototype.html#w15) |
| Suppliers | [Register](https://idiu-pms.vercel.app/prototype.html#w20) · [Applications](https://idiu-pms.vercel.app/prototype.html#w21) |
| Budgets and reports | [Budgets](https://idiu-pms.vercel.app/prototype.html#w30) · [Revisions](https://idiu-pms.vercel.app/prototype.html#w31) · [Procurement register](https://idiu-pms.vercel.app/prototype.html#w40) · [Budget utilisation](https://idiu-pms.vercel.app/prototype.html#w41) |
| Setup | [Financial years](https://idiu-pms.vercel.app/prototype.html#w50) through [Units of measure](https://idiu-pms.vercel.app/prototype.html#w58) |
| Administration | [Users](https://idiu-pms.vercel.app/prototype.html#w60) · [Roles & permissions](https://idiu-pms.vercel.app/prototype.html#w61) · [Workflows](https://idiu-pms.vercel.app/prototype.html#w62) · [Audit trail](https://idiu-pms.vercel.app/prototype.html#w63) |
| Supplier portal | [Busoga Tech home](https://idiu-pms.vercel.app/prototype.html#w71) · [Mpumudde's application](https://idiu-pms.vercel.app/prototype.html#w70d) |
