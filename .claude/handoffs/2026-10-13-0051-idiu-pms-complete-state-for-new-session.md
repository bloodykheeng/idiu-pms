# Handoff: IDIU procurement mockup: complete state for a new session (70 screens, sessions, tested)
_Date: 2026-10-13 00:51 · Author: Claude_

This note stands alone: read it, then `PLAN.md` and `README.md`. The three earlier notes in this folder are
history, already folded in here.

## Goal
A clickable mockup of the Procurement Management System that **New Wave Technologies (NWT)** proposed to
**International Development Institute Uganda (IDIU, idiu.org, Jinja)**. IDIU's Procurement Officer (Mutungi
Rodgers) asked on 12 Oct 2026 for a demo "to test user permissions, approval workflows and data entry without
altering any live configurations". The user (Eisah's team at NWT) is building it the same way as the Letshego
mockup: Python → SVG screens → one clickable `prototype.html`, deployed on Vercel.

## Status
**Built, checked and smoke-tested; nothing committed yet.**
- 70 screens (65 staff console, 5 supplier portal), light and dark, plus 108 per-person sidebars.
- `check.py` and `smoke.py` both pass.
- The repo is initialised on `main` with remote `https://github.com/bloodykheeng/idiu-pms.git`, but has no
  commits. Every file is untracked.

## Where everything is
| Path | What |
|---|---|
| `../resorces/` | NWT technical proposal (.docx), financials (.xlsm, mockups = line 2.0, UGX 4.5M), NWT profile (.pdf), the user's swimlane sketch (.jpg) |
| `../idiu pms procureent system notes.txt`, `../idiu pms notes my summary.txt` | The client's request and the user's short list |
| `PLAN.md` | **The design record**: decisions (§1), the story and cast (§2), roles (§3), master data order (§4), approvals (§5), every screen with its links (§6), look (§7), open questions (§8) |
| `README.md` | How it is generated, the kit, keys, viewer, **testing (§6)**, rules (§7), style, environment, XD, **presenting script (§11)** |
| `_src/` | The generator (below). Never hand-edit `web/`, `web-dark/`, `chrome*/`, `prototype.html`, `all-screens.svg` |
| `.claude/commands/handoff.md`, `handoffpass.md` | `/handoff` and `/handoffpass` |

`_src` modules:
- **Drawing kit and assets:** `kit.py` (SVG builder, palette, icons, components, text boxes and layers for checks), `fonts.py` (subset fonts embedded per SVG), `charts.py` (file track, budget bar, charts), `make_fonts.py`, `make_assets.py` (favicon, `og-image.jpg`).
- **Shared data:** `data.py` (people, roles, `PERMS`/`menu_for`, `SESSIONS`, `YOUR_TURN`, master data, budgets, files, suppliers, audit).
- **Frame:** `shell.py` (console/sidebar/identity/`chrome()`, portal frame, list pattern, tabs, dialogs, drawers, decision panel).
- **Screens:** `home.py`, `procurement.py`, `suppliers.py`, `budgets.py`, `setup.py`, `admin.py`.
- **Build and test:** `theme.py` (dark remap), `build.py` (screens, chromes, viewer `PROTO`, stale-file cleanup), `check.py`, `smoke.py`, `combine.py` (XD file).

## How to run and verify (do this first in a new session)
```
cd "D:/coding/new wave/idiu pms procuremnt managment system/mockups/_src"
python build.py                     # 70 screens + 108 sidebars + prototype.html (removes stale SVGs)
python combine.py                   # all-screens.svg for Adobe XD
PYTHONIOENCODING=utf-8 python check.py    # 9 "session" lines, then "70 screens · … ✓ all checks passed"
PYTHONIOENCODING=utf-8 python smoke.py    # Playwright: 10 walks, "✓ smoke test passed" (~2-3 min)
python build.py --png w11           # PNGs into _previews/ (git-ignored); --png --dark for both
```
Needs Python 3 with pillow, fonttools, brotli, playwright (+chromium), autoflake and pyflakes for linting.

## What the mockup contains (one line per area; details in PLAN §6)
- **Sign in (w00):** "sign in as" for 9 people, each landing on their own dashboard; plus the supplier portal.
- **Dashboards w01-<person>:** ivan, samuel, daniel, joseph, ruth, grace, esther, peter, agnes, each with "Your turn".
- **Approvals:**
  - Samuel (Country Director): w02 inbox → w02b requisition, w13c award, w31b budget revision, w21b prequalification.
  - Daniel (Head of Department): w03 → w03b.
  - Ruth and Ivan: w02-ruth and w02-ivan, empty states.
- **Procurement:**
  - Lists: w10 Requisitions, w12 RFQs, w13 / w13-esther Evaluations, w14 LPOs, w15 Deliveries.
  - Actions: w10b new requisition (Grace), w12b new RFQ (Joseph), w13b scoring (Esther), w15b GRN (Peter).
- **The flagship file PR-2026-0087** (10 laptops, Kasese ICT Hub, KOICA) is closed today. Its 8 tabs: w11 Overview, w11b Approvals, w12c Sourcing, w13d Evaluation, w14b LPO, w15d Delivery, w15c Payment, w11c Documents & history.
- **Suppliers:** w20 register, w20b profile, w21 applications, w21b decision.
- **Supplier portal:** w70 register → w70b documents → w70c submitted; w71 home → w72 quotation.
- **Budgets:** w30, w30b (Kasese FY 2026), w30c (FY 2027 draft, line by line), w30d (Excel import with 3 bad rows), w31 revisions, w31b. **Reports:** w40, w41.
- **Setup (each list its own screen):** w50 financial years, w51 departments (+ w51b dialog), w52 offices, w53 donors, w54 projects (+ w54b form), w55 account codes, w56 procurement categories, w57 supplier document types, w58 units.
- **Admin:** w60 users, w60b edit user (acting approver), w61 roles & permissions, w62 approval workflows (+ w62b edit), w63 audit trail, w63b entry (old → new).

## Decisions settled (do not reopen without the user)
- **Web only**, 1920×1080, console + supplier portal. Rejected: a mobile app and phone renders ("it's web only, this is just a mockup").
- **Master data first, each list its own menu item and screen** (like SDS). Rejected: one Setup page ("the client won't like it, it will look vague").
- **Maker-checker on budgets, revisions, requisitions, awards, LPOs, prequalification and workflow changes** (the Alpha engine pattern). Comments are required on return and reject. Live budgets change only by revision.
- **One procurement file per purchase**: the lists open the same file; its tabs belong to the menu that leads to them.
- **Sessions like the real app** (SDS: AuthContext + AppSidebar + routeAccess):
  - The signed-in person keeps their own sidebar, name and Dashboard on every screen.
  - A click never opens another person's own screen or a menu their role lacks.
  - **System Admin sees every menu**; the Auditor sees all but My approvals; everyone else sees only their own.
  - Rejected: baking each screen with whoever does that step ("confusion for nothing").
- **Committee members are appointed, not a role** (Esther, Brian and Moses are Requesters).
- **PR-2026-0087 is paid and closed today** (09:38 / 09:41), so its tabs never contradict each other. Data entry is shown on files genuinely pending.
- **Illustrative names**; IDIU's name, logo, offices, projects and donors are real. **Example thresholds 5M / 30M**, labelled.
- **The system does not pay suppliers**: Finance records the payment reference.
- **Fresh 2026 look:**
  - colours: field green `#1A683F`, mint, fresh lime, sage canvas;
  - fonts: Bricolage Grotesque / Figtree / IBM Plex Mono, embedded in each SVG;
  - signature element: the file track.
- **Don't over-build:** no payments, stores, contracts, tender portal or procurement plan.
- **Never link a button to the wrong screen**: if no screen exists for it, it stays visible but unlinked.

## Next steps
1. User reviews `prototype.html` (Ctrl+F5) as several people; fix anything flagged; re-run check + smoke.
2. **On the user's go:** `git add -A`, commit (attribution line from the system reminder), and
   `git push -u origin main`. The sandbox proxy blocked GitHub once with a 502, so the user may need to push.
3. Connect Vercel (preset Other, no build command, output = repo root) → https://idiu-pms.vercel.app.
4. Optional, if asked: a short BRIEFING.md for Eisah. Tell him the mockup is **not a sandbox**: IDIU's "test
   data entry" ask needs a working demo instance.

## Still open (questions for IDIU, PLAN §8)
- Their procurement manual: methods, thresholds, approvers. The mockup uses labelled examples.
- Accounting package and chart of accounts. The mockup uses illustrative 5xxx codes.
- Is there a Finance Manager separate from the Finance Officer? Currently the Country Director approves budgets.
- Financial-year dates; standing or per-procurement committees; a sandbox after the mockup.

## Gotchas
- **Bash heredocs break on apostrophes here.** Write patch scripts with the Write tool into the scratchpad, then `python -I script.py`.
- **Python `-I` ignores PYTHONIOENCODING.** Write files with `encoding="utf-8"`; run check/smoke with `PYTHONIOENCODING=utf-8`.
- **A screen showing one person must be `console(..., viewer, owner=True)`.** Shared screens use `viewer="ivan"`. Person-specific screens get an explicit key (`fn.key = "w01-ruth"`).
- **A new menu entry** needs its label in `data.MENU`, `PERMS` and `shell.NAV`, or no sidebar is generated for it.
- **Don't run `smoke.py` while a `--png --dark` render runs.** CPU contention timed out the preload once.
- **`combine.py` strips per-screen `<style>` blocks** and embeds one font subset for all screens; keep it that way.
- **Lint after edits:** `python -m autoflake --in-place --remove-all-unused-imports <file>` and `python -m pyflakes *.py`.
- **Reference projects:**
  - Letshego mockup: `../../letshego/mockups`.
  - SDS sidebar: `../../mops sds/sds new/sds-mops-workspace/sdstool-nextjs/lib/routeAccess.ts`, `sdsMenuItems.ts`, `components/dashboard/layout/AppSidebar`.
  - Alpha approval engine: `../../CPA accounts system/alpha-fund-system-workspace/alpha-fund-laravel/docs`.

## Where the record lives
- `PLAN.md`, `README.md`; earlier notes in this folder (kickoff, first build, sessions).
- Memory (auto-loaded): mockup method, Alpha approval engine, master data and maker-checker first, testing practice, sessions like the real app, and the IDIU demo.
- Session transcript: `~/.claude/projects/d--coding-new-wave-idiu-pms-procuremnt-managment-system/e8bb9b9e-029d-448f-9371-02eac36284af.jsonl`
  (~36 MB). **Grep it, never read it whole.** Last resort only.
