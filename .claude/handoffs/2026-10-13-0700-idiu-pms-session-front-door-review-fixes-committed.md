# Handoff: IDIU mockup: one front door, review fixes, patterns doc, first commits pushed
_Date: 2026-10-13 07:00 · Author: Claude_

**This note stands alone for the whole session.** Read it, then [`PATTERNS.md`](../../PATTERNS.md) (the reusable
rules), [`PLAN.md`](../../PLAN.md) (§1 decisions, §6 screen map) and [`README.md`](../../README.md) (§5 viewer, §6 tests,
§7 rules). The 0125, 0530 and 0630 notes in this folder are the steps along the way; this one supersedes them.

## Goal
Make the mockup one system with one front door (public site → sign in / register → a dashboard by who signed in),
then fix everything the user found when they clicked through it. Finally, document the patterns, and commit and push
professionally.

## Status
**Done and pushed.**
- 98 screens (light + dark) and 108 per-person sidebars.
- `check.py` and `smoke.py` pass: 13 walks plus door, forms, modal, full-screen and dark checks.
- `main` is on GitHub (`bloodykheeng/idiu-pms`) in 12 logical commits; nothing is unpushed.
- **One open question from the user is not yet answered on screen:** see "Still open" (two Requesters).

## What changed this session
**1. One front door** (the user: "you design as if it's an essay, you don't reason how a system should be linked"):
- Public site: w80 Home, w81 About, w82 FAQs, w83 Notices (the 2027 prequalification round, award notices).
- w00 is one Sign in for staff and suppliers; w00b is Forgot password.
- Register: w70 → w70b → w70c → w70d, the applicant's status page.
- Supplier portal (Busoga Tech) with its own sidebar: w71–w77b.
- Suppliers are sessions too. No hash opens Home; sign-out goes to Home.

**2. Review round 1** (user screenshots):
- Viewer: one **Web dashboard** button.
- Under a dialog or drawer nothing is clickable, and the sidebar is dimmed; hotspot boxes hug what they cover.
- Create/edit buttons now work as shared `write` forms (the Auditor is never allowed):
  - New requisition w10c;
  - New budget w30e;
  - Request a revision w31c;
  - New financial year w50b;
  - Add user w60c.
- Highlighted rows are the clickable ones (w12 laptops, w15 LPO-0051, w40 PR-0087).
- An application or revision opened from its list stays in that menu, and Samuel can decide there:
  - w21c / w21c-samuel;
  - w31d / w31d-samuel;
  - `<key>-<person>` own copies, via `resolve()`.

**3. Review round 2:**
- **Add user** (renamed from Invite) gains phone, password and "email the sign-in details".
- Every setup list's **New** works: w52b office, w53b donor, w55b account code, w56b category, w57b document type, w58b unit.
- **Dialogs only for small forms.** Applications, revisions and New budget are full pages (the user: "I didn't tell you we need dialogs… be wise, not everywhere").
- Full screen: the viewer bar appears only at the very bottom edge, so footer links work.
- Sign-in demo accounts are in **process order** with quiet step numbers (01…09); the numbered badges on the avatars were rejected as ugly.

**4. Docs and git:**
- New `PATTERNS.md` covers:
  - the front door, roles and sessions, dashboards;
  - page vs dialog vs drawer;
  - approval in place;
  - buttons and highlights, demo order;
  - the tests that hold all this.
- PLAN, README and `.vercelignore` updated.
- Memory: `mockup-every-button-works`, `mockup-architecture-front-door`.
- Commits (oldest first):

```
3ca6ff9 chore: add repository scaffolding and deploy config
d7c76fb feat(kit): add SVG drawing kit, embedded fonts and dark theme
de0ce15 feat(data): add illustrative IDIU data, roles and permission matrix
793b0fd feat(shell): add screen frames and shared UI patterns
96627e2 feat(console): add staff console screens
22d0784 feat(front-door): add public site, sign in and forgot password
bad3852 feat(suppliers): add supplier register, registration and supplier portal
3b6e785 feat(build): add build pipeline, prototype viewer and XD export
ce20f8c test: add structural checks and Playwright smoke tests
61bdce4 build: generate screens, sidebars and prototype
c0f5a77 docs: add plan, readme and UI patterns
eb7f30a chore(claude): add handoff commands and session notes
```

## Uncommitted / in-flight
- This note (it gets its own `docs(handoff)` commit).

## Next steps
1. **Answer the two-Requesters question** (below) and change the screens accordingly.
2. Ask the user whether requisition approvals (PR-0096, PR-0095) and the award (PR-0089) should open as **pages** from their lists, with the approver deciding in place (never dialogs).
3. Still unlinked by design: Import from Excel on the setup lists, row edit/view icons, Export/Download/Print. Wire them only if asked.
4. Connect Vercel (preset Other, no build command, output = repo root) → https://idiu-pms.vercel.app. Each push to `main` redeploys.

## Decisions settled this session
- **One front door**: public → one Sign in (staff and suppliers) → a dashboard by role (Alpha `dashboard/layout.tsx`). Rejected: registration as the entry; a portal without sign-in.
- **The supplier portal is a sidebar frame like the console's**, and every page in it is the company's own.
- **Dialogs only for small forms** (setup lists, users, a financial year); records are full pages in the menu they were opened from. Rejected: record dialogs (the Alpha `RecordDetailsDialog` was "a clue", the idea not the form).
- **Approve in context**: the approver decides on the record page from its list as well as from My approvals.
- **Every create/edit button opens a form** for the roles allowed (`shell.writes`); the Auditor never fills anything in; budgets are Finance's (and the Admin's), and the Country Director approves.
- **An active budget is edited by a revision** (old → new); drafts are edited line by line.
- **The highlighted row is clickable for everyone who sees the list**; nothing is clickable under a dialog.
- **One viewer button "Web dashboard"**; the full-screen bar shows only at the bottom edge.
- **Sign-in demo accounts follow the work**: 01 Ivan sets up, 02 Ruth budgets, 03 Grace requests, 04 Daniel, 05 Samuel approve, 06 Joseph owns the purchase, 07 Esther scores, 08 Peter receives, 09 Agnes audits. Step numbers are quiet text in the corner, never badges on avatars.
- **Commits are logical and dependency-ordered**, never one bulk commit; conventional subjects with a body.

## Still open
| Question | Blocks | Recommendation |
| --- | --- | --- |
| **Why are Grace and Esther both "Requester"?** The user finds the same role doing two things confusing | How Esther is labelled on Sign in, her sidebar and w61 | Keep committee work as an **appointment per procurement** (PPDA practice: any staff member can be appointed, with a conflict-of-interest declaration each time). But show it: on Sign in and in her identity block, "Requester + appointed to evaluation committees", plus an "Appointments" line on w60b and w61. Alternative: a separate "Evaluation Committee Member" role for Esther, which would mean moving her requisitions (PR-0089…0095) to another requester. **Ask the user before changing.** |
| Requisition approvals and the award as pages from their lists? | nothing | Yes, as pages (same builder pattern as `_application_page`) |
| IDIU's manual, thresholds, chart of accounts, Finance Manager, financial year, committees, sandbox (PLAN §8) | as before | ask IDIU |

## Gotchas & context
- **Generated files are committed** (Vercel serves the root). Always rebuild (`build.py`, `combine.py`) before a commit that touches `_src`, and commit sources and outputs in separate commits.
- **`<key>-<person>` silently replaces `<key>`** for that person (viewer and check.py). Don't reuse the pattern for unrelated screens.
- `overlay()` clears the links under a dialog: add the dialog's own links after it. New frames merge `meta` (`|=`).
- `writes()` takes roles, not people. The default is every role but the Auditor.
- Browser caching: after a rebuild, review with Ctrl+F5. A user screenshot can show an old version.
- Patch scripts: write them with the Write tool (heredocs break on apostrophes); `PYTHONIOENCODING=utf-8` for check and smoke; don't run smoke during a PNG render.

## Where the record lives
- Docs: `PATTERNS.md`, `PLAN.md`, `README.md`; earlier notes in this folder.
- Memory: `mockup-every-button-works`, `mockup-architecture-front-door`, `mockup-sessions-like-real-app`, `mockup-testing-practice`.
- Live prototype: https://idiu-pms.vercel.app (once Vercel is connected).
- Session transcript: `~/.claude/projects/d--coding-new-wave-idiu-pms-procuremnt-managment-system/2d67113b-7e4e-4649-b797-7a6dcc72c91d.jsonl` (~12 MB). **Grep it, never read it whole.**

## How to verify
- `cd _src && python build.py && python combine.py` (98 screens)
- `PYTHONIOENCODING=utf-8 python check.py` → "98 screens · … 98 reachable from w80 ✓"
- `PYTHONIOENCODING=utf-8 python smoke.py` → door, 13 walks, forms, modal, fullscr, dark, "✓ smoke test passed"
- `git log --oneline` shows the 12 commits above plus this note; `git status` is clean
