# Handoff: IDIU procurement mockup: all 59 screens built, checked and smoke-tested
_Date: 2026-10-12 22:45 · Author: Claude_

## Goal
Build the full clickable mockup of the Procurement Management System NWT proposed to IDIU (staff console and
supplier portal), so IDIU can walk through permissions and approval workflows by role.

## Status
Done for a first review: 59 screens (54 console, 5 portal), light and dark, `check.py` and `smoke.py` both
pass. **Nothing committed or pushed yet** (repo initialised, remote set).

## What changed
- `_src/`: kit (fonts embedded per SVG), fonts, charts (file track, budget bar), data, shell, theme, build
  (viewer), check, smoke, combine, make_assets, make_fonts; screen modules home, procurement, suppliers,
  budgets, setup, admin. See README §2 for the map, PLAN.md §6 for every screen and its links.
- Generated: `web/`, `web-dark/`, `prototype.html`, `all-screens.svg`, `index.html`, icons, `og-image.jpg`.
- Docs: `PLAN.md` (decisions, story, roles, master data, approvals, screen map), `README.md` (method,
  testing, rules, presenting walkthrough).

## Uncommitted / in-flight
- Everything (15 untracked paths). The user hasn't asked for a commit; ask before committing and pushing.

## Next steps
1. User reviews `prototype.html` (open locally, or after pushing). Fix what they flag; re-run `check.py` and
   `smoke.py` after every change.
2. When the user says go: `git add -A && git commit` (attribution per system reminder) and
   `git push -u origin main`. The session proxy blocked GitHub once (502); the user may need to push.
3. Connect the repo on Vercel (preset Other, no build, output = root) for idiu-pms.vercel.app.
4. Optional: a short team BRIEFING.md (like Letshego's) if the user wants talking points for Eisah.

## Decisions settled this session
(Planning decisions are in PLAN.md §1; these were settled while building.)
- **PR-2026-0087 is paid and closed today (09:38 / 09:41).** While it waited for payment, every later tab
  contradicted the file view. Its 8 tabs now show the complete trail; the Payment tab (w15c) is a record.
  Data entry is shown where something is genuinely pending today: w10b, w12b, w13b, w15b, w30c, w30d, w72.
- **Active budgets take no new lines.** Line-by-line entry is on a FY 2027 draft (Model Home Health, w30c);
  the Excel import is Kasese FY 2027 (w30d). All FY 2026 budgets are active (PR-0095 draws on Kumi's).
- **Committee membership is an appointment, not a role.** Esther, Brian and Moses are Requesters;
  Requesters get an Evaluations menu showing only appointed evaluations.
- **The Head of Department has his own inbox and decision screens** (w03, w03b); "My approvals" routes per viewer
  (`APPROVALS_FOR` in shell.py).
- **Never link to a screen that shows someone else.** The portal menu is unlinked except Home; a supplier
  who applies lands on their own confirmation (w70c), not Busoga Tech's home.
- **Fonts are embedded subsets per SVG** (Figtree, Bricolage Grotesque, IBM Plex Mono, OFL). Rejected:
  system fonts (they fell back to Roboto on phones in Letshego).
- **Look:** IDIU greens refreshed (field green #1A683F, mint, fresh lime for "your turn" / current stage),
  sage canvas, SDS list pattern; signature = the file track.
- **Required documents:** 7 for every category, 9 for works (NSSF clearance and UNABCEC licence added).

## Still open
| Question | Blocks | Recommendation |
| --- | --- | --- |
| IDIU procurement manual, thresholds, approvers | nothing (labelled examples) | Ask at the demo |
| Accounting package and chart of accounts | nothing | Illustrative 5xxx codes, payment reference only |
| Finance Manager separate from the Finance Officer? | nothing | Country Director approves budgets |
| A working sandbox for "data entry" | their literal ask | Tell Eisah the mockup is not a sandbox |
| Commit and push | the live URL | Wait for the user's go |

## Gotchas & context
- **Run `check.py` and `smoke.py` after every change**; both caught real bugs a screenshot review missed.
- Python `-I` ignores PYTHONIOENCODING; run check/smoke with `PYTHONIOENCODING=utf-8` on Windows.
- Big edits with quotes break bash heredocs: write the patch script to a file (scratchpad), then run it.
- A full `build.py --png --dark` takes over 2 minutes; run it in the background, and don't run `smoke.py`
  while it renders (CPU contention made the preload time out once).
- `combine.py` strips per-screen `<style>` blocks and embeds one subset; keep it that way or glyphs go missing.
- Text boxes and overlay layers (`s.boxes`, `s.layer`) exist only for `check.py`; dialogs and drawers raise the layer.
- Renaming a screen title changes its file name: delete the old SVG in `web/` and `web-dark/`.

## Where the record lives
- Docs: `PLAN.md`, `README.md`; earlier note: `2026-10-12-2150-idiu-pms-plan-and-kickoff.md`
- Source material: `../resorces/` (technical proposal, financials, NWT profile, the user's swimlane sketch)
- Live mockup: https://idiu-pms.vercel.app (after push + Vercel)
- Session transcript: `~/.claude/projects/d--coding-new-wave-idiu-pms-procuremnt-managment-system/e8bb9b9e-029d-448f-9371-02eac36284af.jsonl`
  (~30 MB). **Grep it, never read it whole.** Last resort only.

## How to verify
- `cd _src && python build.py && python combine.py && python make_assets.py`
- `PYTHONIOENCODING=utf-8 python check.py` → "59 screens · 968 hotspots · 59 reachable · ✓ all checks passed"
- `PYTHONIOENCODING=utf-8 python smoke.py` → 13 walks and "✓ smoke test passed"
- `python build.py --png` and look at `_previews/`
