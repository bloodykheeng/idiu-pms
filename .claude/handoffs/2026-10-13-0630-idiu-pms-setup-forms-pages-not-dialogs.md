# Handoff: IDIU mockup: setup "New" forms, Add user, records as pages (not dialogs), full-screen bar, sign-in order
_Date: 2026-10-13 06:30 · Author: Claude_

**Read this, then `PLAN.md` (§1, §6) and `README.md` (§5–§7).** It supersedes the 0530 note's "record dialog"
decision. Everything else in the 0530 and 0125 notes still holds.

## Status
**Done. check.py and smoke.py pass (98 screens, 13 walks + door, forms, modal, full screen, dark); PNGs checked. Nothing committed.**

## What changed (since 0530)
- **Add user** (w60c, was "Invite user"): name, phone, email, department, office, role, first password (Generate), "Email the sign-in details" on, committee toggle. The Users button reads "Add user".
- **Every setup list's New works**, as dialogs (small forms):
  - w52b office, w53b donor, w55b account code, w56b category (with required documents), w57b document type, w58b unit.
  - w51b and w54b are now shared `write` forms instead of Ivan's own.
  - Each opens for any role whose menu has the list; never the Auditor.
- **Records are full pages, not dialogs** (user: "I didn't tell you we need dialogs… leave dialogs in these small modules… be wise"):
  - w21c / w21c-samuel are the application page under Suppliers › Applications. They are built by `_application_page`, which w21b (My approvals) also uses.
  - w31d / w31d-samuel are the revision page under Budget revisions (`_revision_page`, also w31b).
  - Non-approvers get `shell.approval_panel` (timeline + "Waiting on …"); Samuel's own copy gets `decision_panel`.
  - `record_dialog` and `action_bar` were removed.
- **New budget (w30e) is a page**: the header (FY, project), lines line by line or from Excel, and a "what happens" timeline.
- **Full screen:** the viewer bar now appears only at the very bottom edge and stays while hovered, so the public footer links are clickable. smoke.py has a `fullscr` check.
- **Sign-in demo order = the process**:
  - Staff: 1 Ivan (sets up), 2 Ruth (budgets, funds, payment), 3 Grace (requests), 4 Daniel (step 1), 5 Samuel (final), 6 Joseph (owns RFQ to LPO), 7 Esther (scores), 8 Peter (receives), 9 Agnes (audits).
  - Suppliers: 1 Mpumudde applies, 2 Busoga quotes.
  - Each card shows a step number and a line saying that person's part.
- smoke.py `modal` test now uses w50b (a real dialog) as Ruth.
- Docs and memory (`mockup-every-button-works`) are corrected to "pages for records, dialogs for small forms".

## Next steps
1. User reviews. Open question to put to them: should requisition approvals (PR-0096, PR-0095) and the printing award (PR-0089) also open as pages from their lists, where the approver decides in place? (No dialogs.)
2. Still unlinked by design: Import from Excel on the setup lists, row edit/view icons, Export/Download/Print. Add `write` forms or pages if the user asks.
3. Commit and push on the user's go.

## Gotchas
- `_application_page(..., decide=True)` makes the page the viewer's own (`owner`); a `<key>-<person>` copy is opened by `resolve()` in the viewer and in check.py.
- Dialog height: buttons are placed from `1080/2 + h/2`; keep the content inside it (`_new()` in setup.py does this).
- The other gotchas are as in the 0530 note.

## Where the record lives
PLAN.md, README.md, earlier notes; memory `mockup-every-button-works`. Transcript:
`~/.claude/projects/d--coding-new-wave-idiu-pms-procuremnt-managment-system/2d67113b-7e4e-4649-b797-7a6dcc72c91d.jsonl` (grep only).

## How to verify
`cd _src && python build.py && python combine.py && PYTHONIOENCODING=utf-8 python check.py && PYTHONIOENCODING=utf-8 python smoke.py`
