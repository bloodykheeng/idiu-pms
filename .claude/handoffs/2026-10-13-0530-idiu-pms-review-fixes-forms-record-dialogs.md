# Handoff: IDIU mockup: review fixes (working forms, record dialogs, clean dialogs, clickable highlights)
_Date: 2026-10-13 05:30 · Author: Claude_

**Read this, then `PLAN.md` (§1 decisions, §6 screen map) and `README.md` (§5 viewer, §6 tests, §7 rules).** It
builds on `2026-10-13-0125-idiu-pms-one-front-door-built.md` (the front door), which is still accurate.

## Goal
Fix what the user found clicking through the prototype: dead create/edit buttons, an application that jumped to My
approvals, hotspots and theme buttons showing under the audit drawer, sloppy hotspot boxes, highlighted rows that
weren't clickable, and two viewer buttons where one was wanted.

## Status
**Done. check.py and smoke.py pass; new screens checked in PNG and in the live viewer with `?show`. Nothing committed.** 92 screens.

## What changed
- **Viewer ([build.py](../../_src/build.py) PROTO):**
  - One **Web dashboard** button (→ w80) replaces Public site / Sign in.
  - `resolve()` opens a person's own copy of a record (`<key>-<person>`).
  - `allowed()` adds the `write` rule (ROLE per account).
  - On `modal` screens the chrome is dimmed (`brightness(.62)`; a drawer is clipped to the sidebar) and its links aren't added.
- **[shell.py](../../_src/shell.py):**
  - `overlay()` clears every hotspot under the backdrop and sets `meta.modal`.
  - New helpers: `writes(s, roles)`, `record_dialog()`, `timeline()`, `action_bar()` (Alpha's ApprovalActionBar: Approve/Return/Reject for the approver, "Waiting on …" for everyone else).
  - `data_table` records its highlighted row's target in `meta.hl`.
  - Hotspots for the logo, the name/identity and the user card now hug what they cover.
  - Frames merge `meta` (`|=`) instead of replacing it.
- **New screens:**
  - w10c New requisition (blank, any role but the Auditor).
  - w30e New budget dialog (Finance, System Admin); both "New budget" and "Import from Excel" open it.
  - w31c Request a budget revision (how an active budget is edited).
  - w31d + w31d-samuel revision dialog.
  - w21c + w21c-samuel application dialog.
  - w50b New financial year.
  - w60c Invite user.
- **Changed links:**
  - w10 New → w10c; w30b Request revision → w31c; w31 New revision → w31c.
  - w31 BR-0007 → w31d; w21 Mpumudde → w21c (no longer w21b).
  - w63b "full history" → w31.
- **Highlights:**
  - w12 now highlights RFQ-0031 (the laptops); w15 highlights LPO-0051; w40 highlights PR-0087.
  - w60b is now a System-Admin `write` form rather than Ivan's own screen, so the Users highlight is legal.
- **check.py:**
  - forms (no Auditor), modal (no hotspots under the backdrop, a way out), highlight (the row opens a shared screen);
  - sessions resolve the own copies, and modal screens add no sidebar links.
- **smoke.py:**
  - walks for every new screen (Ivan, Samuel, Joseph, Ruth, Grace);
  - a **forms** test (Agnes can't see Invite/New requisition/New budget; Samuel can't see New budget; Daniel can see New requisition);
  - a **modal** test (Ruth on w31d: no sidebar hotspots, chrome dimmed).
- **Docs:** PLAN §1 (3 decisions) and §6 rows; README counts, §5, §6 and §7. Memory: `mockup-every-button-works`.

## Uncommitted / in-flight
- Everything (still no commits on `main`). The user said not to commit until asked.

## Next steps
1. User re-reviews (Ctrl+F5): as Samuel open Suppliers › Applications → Mpumudde (decide in the dialog); as Ivan try Invite user, New financial year, New budget, New requisition, Budget › Request revision; the audit drawer with H on.
2. If more "New …" buttons should work (New department exists; New RFQ is Joseph's own w12b; Setup's "Import from Excel", Export/Download stay unlinked), add `write` forms the same way.
3. Commit and push on the user's go; connect Vercel.

## Decisions settled this session
- **A record opens as a details dialog over its list (Alpha `RecordDetailsDialog`)**; the approver decides there as well as from My approvals. The user said: "it takes me back up to approvals… I can approve under the approvals or even under the supplier themselves." Applied to applications and budget revisions.
  Rejected: a list row linking to the approver's My approvals screen.
- **Create/edit buttons open shared `write` forms for every allowed role**:
  - the Auditor never fills anything in;
  - budgets and revisions are prepared by the Finance Officer and the System Admin; the Country Director approves (so Samuel sees no New budget hotspot: by design, not a bug).
  Rejected: "New" pointing at one person's own draft.
- **An active budget is edited by a revision** (w31c, old → new, total unchanged); drafts (FY 2027) are edited line by line (w30c).
- **Nothing is clickable under a dialog; the highlighted row is the clickable one; one viewer button "Web dashboard"** (user's words).

## Still open
| Question | Blocks | Recommendation |
| --- | --- | --- |
| Should other approvals (requisitions PR-0096/0095, award PR-0089) also open as record dialogs from their lists? | nothing | Yes if the user asks; same helpers (`record_dialog` + `<key>-samuel`) |
| Should the Country Director be able to prepare a budget? | nothing | No: maker-checker; he approves |

## Gotchas & context
- **Own copies:** a key `w21c-samuel` silently replaces `w21c` for Samuel in the viewer *and* in check.py. Don't name an unrelated screen `<key>-<person>`. Existing ones (w02-ruth, w13-esther) already behave this way.
- **`overlay()` clears links:** add a dialog's own links *after* `dialog()` / `drawer()`.
- **New frames must merge meta** (`s.meta |= {...}`) or `meta["hl"]` is lost (a KeyError in `data_table`).
- **`writes()` takes roles** (`PEOPLE[p][2]`), not people. Defaults to every role but the Auditor.
- The smoke preload wait is 120 s; don't run smoke during a PNG render.

## Where the record lives
- Docs: `PLAN.md`, `README.md`; previous notes in this folder; memory `mockup-every-button-works`.
- Session transcript: `~/.claude/projects/d--coding-new-wave-idiu-pms-procuremnt-managment-system/2d67113b-7e4e-4649-b797-7a6dcc72c91d.jsonl`. **Grep it, never read it whole.**

## How to verify
- `cd _src && python build.py && python combine.py` (92 screens)
- `PYTHONIOENCODING=utf-8 python check.py` → "92 screens · … ✓ all checks passed"
- `PYTHONIOENCODING=utf-8 python smoke.py` → door, 12 walks, forms, modal, dark, "✓ smoke test passed"
- `prototype.html?show#w21c` / `#w63b` to see the hotspots
