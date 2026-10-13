# Handoff: IDIU mockup: one role per person, named as in the proposal
_Date: 2026-10-13 07:50 · Author: Claude_

**Read `2026-10-13-0700-…-committed.md` first (the whole session); this note adds the last change.** It answers the
open question in that note ("why are Grace and Esther both Requester?").

## Goal
The user found two Requesters doing different jobs confusing. After reading IDIU's resources together, the user
agreed: "let's make everything match so everyone has one role."

## What the resources say (the basis)
- **Proposal §15 (User Roles):** Requesting Officer, Department Head, Budget Holder, Finance Officer, Procurement Officer, **Evaluation Committee Member**, Procurement Manager, Executive Approver, Inspection Officer/Committee, System Administrator, Auditor/Read-only, Supplier. "The final role and permission matrix will be agreed during requirements validation."
- **§7:** committee members are *appointed* per procurement and sign a conflict-of-interest declaration; only authorised participants see evaluations.
- **The user's swimlane sketch:** Finance · Requester · Approver · Supplier.
- **The client's email:** "test user permissions, approval workflows and data entry".

## Status
**Done. check.py and smoke.py pass; PNGs checked; committed and pushed.**

## What changed
- **Roles** (`data.ROLES`, `PERMS`, `WORKFLOWS`, `PEOPLE`, `USERS`): Requesting Officer, Department Head, Finance Officer, Procurement Officer, Evaluation Committee Member, Executive Approver (Samuel; his job stays Country Director), Inspection Officer, System Administrator, Auditor. `ROLE_SHORT` is for tight spots.
- **The committee is a role:** Esther, Brian and Moses have menu Dashboard + Evaluations, and the `APPOINTED` special case is gone.
- **Esther:**
  - Her dashboard is committee work: Your turn, To score, Declarations, and My evaluations.
  - She raises no requisitions. **Harriet Kyomuhendo** (Requesting Officer, new, not a demo sign-in) raised PR-0084 to PR-0095, so Daniel's inbox, the w03b decision and the stationery inspection now show Harriet.
- **Acting approver:** Daniel's stand-in is **Rebecca Achan, Department Head, Administration** (also that department's head in Setup), not Esther.
- **Screens:**
  - w61 has 9 columns including Committee, with a note on the Budget Holder and Procurement Manager mapping. Its "raise requisitions" row now matches the menus.
  - w60b and w60c: a radio per role, and the "can be appointed" toggle is removed.
  - w00 sign-in cards and w62b steps use the new names.
- **Docs:** PLAN §1 (decision), §2 cast, §3 roles, §5 approvals, §6, §8; README §7; PATTERNS §2. Memory `mockup-every-button-works` gains the one-role rule.

## Decisions settled
- **One role per person, named as in the proposal's §15.** The committee is a role granted by appointment (§7). A stand-in has the same role as the person they stand in for.
- **Budget Holder and Procurement Manager stay folded in** (Finance Officer; Executive Approver), stated on w61 and asked of IDIU in PLAN §8.
- **"Country Director" is Samuel's job title** (text across screens); his role is Executive Approver.

## Next steps
1. User reviews (Ctrl+F5): sign in as Esther (2 menus), look at w61 and Users.
2. Open question still standing: requisition approvals and the award as pages from their lists (never dialogs)?

## How to verify
`cd _src && python build.py && python combine.py && PYTHONIOENCODING=utf-8 python check.py && PYTHONIOENCODING=utf-8 python smoke.py`
(the check shows `esther 4 screens, 2 menu entries`)
