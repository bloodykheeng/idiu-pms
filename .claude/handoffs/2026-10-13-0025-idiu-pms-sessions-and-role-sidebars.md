# Handoff: IDIU mockup: sessions, per-person dashboards and role-scoped sidebars
_Date: 2026-10-13 00:25 · Author: Claude_

## Goal
Fix what the user hit while clicking through: the person and the sidebar changed from screen to screen
(Deliveries showed Peter, Setup showed Ivan with no procurement menus, Dashboard from the Country Director's
sidebar opened the Procurement Officer's). Make it behave like SDS: one signed-in person per session.

## Status
Done: 70 screens + 108 per-person sidebars; `check.py` (session closure for all 9 people) and `smoke.py`
(10 walks asserting the person never changes) pass. Still nothing committed or pushed.

## What changed
- `data.py`: `MENU`, `PERMS` (System Admin = all 26 entries, Auditor = all but My approvals, Procurement
  Officer lost My approvals), `APPOINTED`, `menu_for(person)`, `SESSIONS`, `INBOX_KEY`, `menu_target()`,
  `YOUR_TURN` per person.
- `shell.py`: `console(..., viewer, owner=False)` sets `s.meta` (label, viewer, owner); `draw_sidebar`,
  `draw_identity` (fixed-width block `IDENT`) and `chrome(person, label)`; Dashboard / My approvals /
  Esther's Evaluations route per person.
- `home.py`: `w01-<person>` dashboards for all 9 (`_dashboard`), `w02-ruth`, `w02-ivan` (empty inboxes),
  sign-in tiles land on dashboards; Sign in button = Ivan.
- `procurement.py`: shared screens built as Ivan; `w13` = all evaluations, `w13-esther` = hers; `w13d` under
  Evaluations and `w15d` under Deliveries (so Peter can open the GRN); owned: w10b, w12b, w13b, w13c, w15b.
- budgets/suppliers/setup/admin: shared screens as Ivan; owned: w30c, w30d, w31b, w21b, w51b, w54b, w60b, w62b.
- `build.py`: `screen_key()` (explicit `fn.key`), `build_chromes()` → `chrome/`, `chrome-dark/`; prototype
  `settle()` / `allowed()` / overlay / "Signed in" pill; a full build deletes stale SVGs.
- `check.py`: session walk per person; `smoke.py`: walks per person with session + sidebar assertions.
- Docs: PLAN.md §1 decisions + §6 sessions; README §2, §3, §5, §6, §7.

## Uncommitted / in-flight
- Everything (repo has no commits yet). Ask before committing and pushing.

## Next steps
1. User clicks through `prototype.html` as several people and confirms the sidebar stays put.
2. Commit + push on the user's go; connect Vercel.

## Decisions settled this session
- **Sessions like SDS** (AuthContext + AppSidebar + routeAccess.ts, read from `sdstool-nextjs`): the
  signed-in person decides the sidebar on every screen; Dashboard is each person's own. Rejected: baking
  each screen with whoever does that step (the user: "confusion for nothing").
- **System Admin sees every menu**; others only their own; groups collapsed but visible.
- **A link never switches person**: hidden in the viewer, proven by `check.py` for all 9 sessions.
- **Overlay, not variants**: one sidebar SVG per (person, menu entry) laid over shared screens, instead of
  re-rendering ~160 screens per person.

## Gotchas & context
- Bash heredocs break on apostrophes in this environment: write patch scripts with the Write tool.
- A person's own screen must be `owner=True`, or another session could reach it; check.py will say so.
- A new menu entry needs its label in `data.MENU` and `shell.NAV`, or no sidebar is generated for it.
- File-tab screens take the label of the menu that leads to them; that label decides who can open the tab.

## How to verify
- `cd _src && python build.py && python combine.py`
- `PYTHONIOENCODING=utf-8 python check.py` → 9 session lines, "70 screens · … ✓ all checks passed"
- `PYTHONIOENCODING=utf-8 python smoke.py` → 10 walks, "✓ smoke test passed"
