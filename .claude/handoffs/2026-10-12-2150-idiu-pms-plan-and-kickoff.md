# Handoff: IDIU procurement mockup: plan settled, build starting
_Date: 2026-10-12 21:50 · Author: Claude_

## Goal
Design and build a clickable mockup of the Procurement Management System NWT proposed to IDIU, using the
Letshego Python → SVG → prototype.html method, so IDIU can walk through permissions and approval workflows.

## Status
Plan settled with the user; docs written (PLAN.md, README.md, commands); fonts downloaded and cut; build
of `_src/` starting. Nothing committed yet (repo initialised, remote set, nothing pushed).

## What changed
- `PLAN.md`: the design record (decisions, story, roles, master data order, approvals, 56-screen map).
- `README.md`: how the generator works (to update once the code exists).
- `_src/make_fonts.py`, `_src/fonts/` (variable fonts + OFL licences), `_src/fonts/static/` (cut weights).
- `.claude/commands/handoff.md`, `handoffpass.md` adapted from Letshego.
- `.gitignore`, `.vercelignore`.

## Uncommitted / in-flight
- Everything above: no commits yet. First commit once the first screens build.

## Next steps
1. Write `_src/kit.py`, `fonts.py`, `charts.py`, `data.py`, `shell.py`, `theme.py`, `build.py`, `combine.py`.
2. Build Setup (w50–w58) first, then budgets, suppliers, procurement, approvals, admin, portal.
3. Link check, render PNGs, look at every screen, fix.
4. Commit and push (`git push -u origin main`; the sandbox proxy blocked GitHub once, so the user may push).

## Decisions settled this session
See PLAN.md §1. Headlines:
- **Web only**: console + supplier portal, 1920×1080. Rejected: mobile app, phone-width renders ("it's
  web only, this is just a mockup").
- **Each master list is its own menu item and screen**, like SDS. Rejected: one Setup screen with tabs
  ("the client won't like it, it will look vague").
- **Master data first** (department before user, project/account code before budget). The user caught this
  gap: "how can you create a department user without first creating a department".
- **Maker-checker (Alpha engine) on budgets, revisions, requisitions, awards, LPOs, prequalification,
  workflow changes**; budgets entered line by line or imported from Excel, then approved.
- **One procurement file per purchase**; stage lists open the same file.
- **Fresh 2026 look**, identity only from idiu.org ("their site is very old, do something fresh").
- **Illustrative names**; real organisation, places, projects and donors. **Example thresholds 5M / 30M.**
- **Don't over-build**: no payments, stores, contracts, tender portal, procurement plan.
- Repo `bloodykheeng/idiu-pms`, URL `idiu-pms.vercel.app`.

## Still open
| Question | Blocks | Recommendation |
| --- | --- | --- |
| IDIU procurement manual / thresholds | nothing (labelled examples) | Ask at the demo |
| Accounting package, chart of accounts | nothing | Illustrative 5xxx codes |
| Finance Manager role? | nothing | Country Director approves budgets |
| A working sandbox after the mockup | their "data entry" ask | Tell Eisah the mockup is not a sandbox |

## Gotchas & context
- Fonts are embedded per SVG (subset WOFF2, verified rendering through `<img>` in headless Chrome).
- Python `-I` ignores PYTHONIOENCODING: write files with `encoding="utf-8"`, don't print non-ASCII on Windows.
- Reference code to copy from: `../../letshego/mockups/_src` (kit, theme, build, combine);
  approval rules from `../../CPA accounts system/alpha-fund-system-workspace/alpha-fund-laravel/docs`.

## Where the record lives
- Docs: `PLAN.md`, `README.md`
- Source material: `../resorces/` (technical proposal, financials, NWT profile, the user's swimlane sketch)
- Live mockup: https://idiu-pms.vercel.app (once pushed and connected)

## How to verify
- `cd _src && python build.py && python combine.py` (both must run clean)
- Link check: every hotspot target in `prototype.html` exists and every screen is reachable
- `python build.py --png` and look at the screens
