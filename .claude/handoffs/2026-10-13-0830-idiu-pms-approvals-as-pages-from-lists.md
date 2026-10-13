# Handoff: IDIU mockup: requisition approvals and the award open as pages from their lists
_Date: 2026-10-13 08:30 · Author: Claude_

**Read `2026-10-13-0700-…-committed.md` (the session) and `…-0750-…-one-role-per-person.md` first.** This note closes
the last open question there; the user's answer: "yah let them open".

## Status
**Done. check.py and smoke.py pass (104 screens, 13 walks); PNGs checked; committed and pushed.**

## What changed
- **PR-2026-0096 (solar, waiting on Samuel, step 3 of 3):**
  - `home._solar()` builds w02b (from My approvals), w10d (under Requisitions, read only, "Waiting on Samuel Kato") and w10d-samuel (his decision, back to w10).
  - Opened from: w10, Grace's dashboard and rows, and Daniel's "recently decided".
- **PR-2026-0095 (hygiene kits, waiting on Daniel, step 1 of 2):**
  - `home._hygiene()` builds w03b, w10e and w10e-daniel.
  - Opened from: w10.
- **PR-2026-0089 (printing award, waiting on Samuel):**
  - `procurement._award_page()` builds w13c (My approvals), w13e (under Evaluations, read only: committee → recommendation → award approval → LPO) and w13e-samuel.
  - Opened from: w13, w13-esther, w12 (RFQ-0032) and Esther's dashboard.
- `_requisition_decision()` takes `active`, `crumbs`, `decide`, `approver` and `waiting`. With `decide=False` it draws `approval_panel`.
- smoke.py:
  - new walk steps for Samuel, Daniel, Joseph, Grace and Esther;
  - the walk labels use the new role names.
- Docs: PLAN §6 rows; README counts (104 screens, 85 staff, 5 own copies); PATTERNS §5 lists all four page builders.

## Decisions settled
- **Every record waiting on an approver opens as a full page from its list, in that list's menu.** The approver decides on their own copy (`<key>-<person>`); everyone else reads the timeline. Never dialogs.

## Next steps
1. User review (Ctrl+F5):
   - as Samuel: Requisitions → PR-0096, and Evaluations → PR-0089;
   - as Daniel: Requisitions → PR-0095;
   - as Grace: her dashboard → PR-0096 (read only).
2. Nothing else open from the user. PLAN §8's questions are for IDIU. Connect Vercel when ready.

## How to verify
`cd _src && python build.py && python combine.py && PYTHONIOENCODING=utf-8 python check.py && PYTHONIOENCODING=utf-8 python smoke.py`
