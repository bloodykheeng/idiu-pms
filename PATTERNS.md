# Patterns: how a mockup system is linked, and which UI pattern goes where

The rules this mockup follows, with the reason for each, so the next screen (or the next client's mockup) starts from
them instead of rediscovering them in review. `PLAN.md` says *what* IDIU's screens show; `README.md` says *how* they
are generated; this file says *how a real system is shaped* and *which pattern to use where*.

Every rule here came from a review of a real build: the user's words are quoted where they settled it.

---

## 1. One system, one front door

A real system has one entrance. Draw the entry map **before** any screen.

```
Public site (no session)            The door (no session)              Dashboard, chosen by who signed in
Home · About · FAQs · Notices  ──►  Sign in (staff AND suppliers)  ──► staff     → the console
                                    Register (suppliers only)      ──► supplier  → the supplier portal
                                    Forgot password                    applicant → their application status
```

| Rule | Why | IDIU |
|---|---|---|
| Opening the mockup with no `#` shows the **public Home** | That is what a visitor sees first | `w80` |
| Every public page has **Sign in**; Home, Notices and FAQs also lead to **Register** | Nobody should hunt for the door | header, hero, footer |
| **One Sign in page** for every kind of user; the dashboard depends on the role | Alpha `app/dashboard/layout.tsx`: investor → `@investor`, anyone else → `@admin` | `w00` → `data.home_key()` |
| Staff **never register**; the System Administrator adds them | Accounts are controlled | Add user `w60c` |
| A pending applicant sees **only their application** | Nothing in a menu may be dead | `w70d`, menu "My application" |
| Signing out returns to the **public Home**; clicking your name returns to Sign in (to switch, in a demo) | How real apps behave | red button → `w80`, name → `w00` |

Rejected: starting the mockup at registration, a supplier portal with no sign-in, separate "staff" and "supplier"
entry buttons. (The user: "you design as if it's an essay, you don't reason how a system should be linked.")

**References:** Alpha `alpha-fund-nextjs/app/(main)`, `(auth)`, `dashboard/layout.tsx` with `@admin` / `@investor`;
SDS `sdstool-nextjs/app/(main)`, `(auth)/login`, `lib/routeAccess.ts`, `components/dashboard/layout/AppSidebar`.

---

## 2. Roles, permissions and sessions

### One matrix decides every sidebar
- `data.PERMS`: role → menu entries, kept in sidebar order (SDS `routeAccess.ts`). The Roles & permissions screen
  (`w61`) draws the same matrix, so what the client reads is what the sidebars do.
- **One role per person**, named as in the client's role table (the proposal's §15). Two people with the same role
  doing different jobs confuses everyone (the user: "isn't this confusion, same role doing two different things").
- **A job title is not a role.** Steps, decisions and "waiting on" always name the role (Executive Approver); a job title
  (Country Director) appears only beside the person's name on their own profile or dashboard. (The user: "am I still
  seeing Country Director there, is that correct?")
- **The System Administrator sees every menu. The Auditor sees everything but My approvals and fills in nothing.** Everyone else
  sees only their own. (The user: "system admin has to see all these, other people see only what they're supposed to
  see.")
- Groups stay collapsed but visible; a group with no allowed entry is hidden.
- A committee is a role granted by appointment: Evaluation Committee Members are appointed per procurement, sign a
  declaration, and see only the evaluations they are on. They don't raise requisitions. A stand-in (acting approver)
  has the same role as the person they stand in for.

### A session is one signed-in account, and it never changes on a click
| Kind of screen | Built as | In the viewer |
|---|---|---|
| **Own** (a dashboard, an inbox, a decision, a draft): `owner=True` | the person it belongs to | opening it signs that person in |
| **Shared** (lists, the procurement file, setup, reports) | the System Administrator (`viewer="ivan"`) | the signed-in person's sidebar and name are laid over it (`chrome/`) |
| **Own copy of a shared record**: `<key>-<person>`, e.g. `w21c-samuel` | that person, with their decision | a link to `<key>` opens their copy (`resolve()`) |
| **Form** that creates or changes a record: `shell.writes(s, roles)` | shared | opens only for the roles listed; **never the Auditor** |
| **Supplier portal** page | that company (`owner`) | the company can never change on a click |

The viewer hides any hotspot to another account's own screen, a menu their role lacks, or a form their role may not
fill in. `check.py` walks every session and fails otherwise. (The user, when the person changed between screens:
"confusion for nothing".)

### Who may create what (maker-checker)
| Record | Maker (may open the form) | Checker |
|---|---|---|
| Requisition | any role with Requisitions, except the Auditor | Department Head → Finance Officer → Executive Approver (above the threshold) |
| Budget, budget revision | Finance Officer, System Administrator | Executive Approver |
| Award, LPO, prequalification recommendation | Procurement Officer | Executive Approver (LPO: Finance first) |
| Setup lists, users | System Administrator (Finance: years, account codes; Procurement: categories, document types, units) | none: plain lists |

Whoever prepares a record can't approve any step of it, and a return or reject needs a comment. A live record is
never edited directly: **an active budget changes by revision** (old → new), a draft is edited freely.

---

## 3. Dashboards

- **Everyone has their own** (`w01-<person>`), shaped by their role. It is not one dashboard with things hidden.
- The top of each is **"Your turn"**: up to three things waiting on that person, each a link to where they act.
- Four figures, each from a menu that person may open (a figure never links somewhere they can't go).
- Office roles (Procurement, Finance, Executive Approver, Admin, Auditor) see the organisation's picture; requesters and
  stores see their own rows.
- A supplier's dashboard is their portal Home: open RFQs, orders, the latest payment, documents to renew.

---

## 4. Page, dialog or drawer

**The rule: dialogs for small, self-contained forms; full pages for records and anything with an approval.** (The
user: "I didn't tell you we need dialogs, I was just giving you a clue… leave dialogs in these small modules of setup,
users etc., be wise, not everywhere.")

| Use | When | IDIU examples |
|---|---|---|
| **Dialog** over its list | A short form (≤ ~8 fields), one record type, no approval, no lines | New department / office / donor / account code / category / document type / unit; New financial year; Add user; Renew prequalification (supplier) |
| **Drawer** from the right | Reading one row's details without leaving the list; nothing to decide | Audit entry (old → new) `w63b` |
| **Full page** | A record people work on: lines, documents, an approval timeline, a decision; or a form with lines or a running total | Requisition, New requisition, budget, New budget, budget revision, Request revision, application, the procurement file and its tabs, LPO, goods received |
| **Page inside the menu it was opened from** | Any record opened from a list | Application under Suppliers › Applications (`w21c`), not under My approvals |

Rules for dialogs and drawers:
- **Nothing under the backdrop is clickable or highlighted**: `shell.overlay()` clears the page's hotspots, and the
  viewer dims the person's sidebar with the page (`meta.modal`). The dialog's own buttons (Save, Cancel, ✕) are the
  only way out, and there must be one.
- Buttons sit inside the dialog, on a divider, primary on the right.

---

## 5. Records and approvals

- **One record per real thing**: a purchase is one procurement file; every list (Requisitions, RFQs, Evaluations,
  LPOs, Deliveries) opens that file at the right tab, never a disconnected page.
- **A record opened from a list stays in that list's menu**, and the approver decides there as well as from My
  approvals. Build the page once (`_application_page`, `_revision_page`, `_requisition_decision`, `_award_page`) and
  call it three ways: from the inbox
  (approver), from the list (everyone, read only), and the approver's own copy from the list. (The user: "it takes me
  back up to approvals… I can approve under the approvals or even under the supplier themselves." Alpha's
  `RecordDetailsDialog` + `ApprovalActionBar` give the idea: details, timeline, and the action for whoever's turn it
  is.)
- **The right-hand panel** of a record page: `decision_panel` (who prepared it, the path, comment, Approve / Return /
  Reject) for the approver at the current step; `approval_panel` (timeline + "Waiting on …") for everyone else.
- **The file track** (Requested → … → Closed, "Waiting on: <person> · <time>") is the signature: on the file and as a
  mini-track in lists.

---

## 6. Buttons, links and highlights

| Rule | Why |
|---|---|
| **Every create or edit button opens its form**, for every role allowed to use it | The user found Invite user, New financial year, New budget, New requisition and budget editing dead |
| Never point "New X" at one person's own draft | It is dead for everyone else |
| Name things as the client does: **Add user**, not Invite user | The user's correction |
| A button may stay unlinked **only** if it would export, download or print | There is no screen to show for a file |
| **Never link to another person's or company's screen** | A link that changes who is signed in breaks the session |
| **Menu entries are never unlinked**; a menu shows only what has a screen | "Nothing visible in a menu is dead" |
| **The highlighted row in a list is the one to click**, and everyone who sees the list may click it | The presenter's cue (the user: "highlight laptops which is clickable so it's easy to identify") |
| Hotspot boxes **hug** what they cover (logo, name, user card) | `H` shows them; loose boxes look broken |
| Every action returns to where it came from: Save / Submit → the list; Cancel → `!back:<list>` | The demo never dead-ends |

---

## 7. Lists, forms and pages (the SDS patterns)

- **List:** title + one-line relation subtitle; tabs with counts; toolbar (search · filter · active filter chips ·
  + New · export · columns); table with status chips; "Showing 1 to 10 of N" and a page-size picker. Row action icons
  (edit · view · deactivate) sit quietly at the end. Master data rows in use are **deactivated, never deleted**, and
  show "used by" counts.
- **Form page:** actions top right (primary · Save draft · Cancel), the form on the left, help on the right (budget
  check, approval path, "what happens"). Blank forms use placeholders; a pre-filled one tells a story.
- **Record page:** a header card (reference in mono, title, status chips, facts), content on the left, the approval
  panel on the right.

---

## 8. The demo itself

- **Accounts on the sign-in page follow the work:** who sets up, who starts, who approves, who owns the purchase, who
  receives, who audits, numbered, each card saying that person's part. (The user: "why aren't users organised
  according to who starts and who owns the process.") Suppliers likewise: who applies, who quotes.
- Illustrative people and figures; the client's name, places, projects and donors real. One "today" for every screen.
- **Viewer:** one button for a one-app system (**Web dashboard** → the public Home). Keys: ← → · H hotspots ·
  F full screen · D dark · Esc. In full screen the bar returns only at the very bottom edge, so links near the bottom
  of a screen stay clickable.
- Light and dark for every screen; dark is derived (`theme.py`). Colours meant to stay white are `#FFFFFF`.

---

## 9. Tests that hold the patterns

`check.py` fails on:
- a dead link, an unreachable screen, or overlapping text;
- a session reaching another account's screen, or a menu entry that opens nothing;
- a form the Auditor could open;
- hotspots under a dialog;
- a highlighted row nobody can click;
- a broken front door.

`smoke.py` clicks through it in Chromium: every screen, 13 walks, the forms per role, a dialog as a non-owner, full
screen, dark mode.

**Adding a screen:**
1. Is it a page, a dialog or a drawer (§4)?
2. Whose is it: own, shared, own copy, form (§2)?
3. Which menu does it live in?
4. Where do its buttons go?
5. Is the highlighted row clickable?
6. Build, then run `check.py` and `smoke.py`, add a walk step, and look at the PNG.
