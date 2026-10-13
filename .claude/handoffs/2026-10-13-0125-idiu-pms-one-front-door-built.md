# Handoff: IDIU mockup: one front door built (public site → sign in / register → role dashboard)
_Date: 2026-10-13 01:25 · Author: Claude_

**Read this note, then `PLAN.md` (§1 decisions, §6 screen map) and `README.md`.** It supersedes the 0110 note (the plan,
now done) and builds on the 0051 note (state before this session; still accurate for the staff console).

## Goal
Rebuild the mockup's entry as one system with one front door, the way SDS and Alpha are linked: public site → one
Sign in for staff and suppliers (Register, Forgot password) → a dashboard chosen by who signed in. The supplier side
becomes a real portal where every menu entry opens a screen, and suppliers are sessions like staff.

## Status
**Done. check.py and smoke.py pass; every new screen has been looked at in PNG (light, and dark for the new frames). Nothing committed.**
83 screens (was 70) + 108 staff sidebars.

## What changed
- **New module [public.py](../../_src/public.py):**
  - w80 Home, w81 About, w82 FAQs and w83 Notices. Notices covers the 2027 prequalification round (open until Fri 20 Nov) and award notices.
  - w00 Sign in, rebuilt as one door: a branding panel and a form, Register, Forgot password, and Back to home. Its demo "sign in as" lists 9 staff and 2 supplier accounts.
  - w00b Forgot password.
  - The old w00 is gone from [home.py](../../_src/home.py).
- **[shell.py](../../_src/shell.py):**
  - Frames: `portal()` (the supplier's sidebar, same frame as the console), `public()` + `footer()`, `auth()` (branding panel) and `register_frame()`.
  - The console top bar is now `_top_bar()`, shared with the portal.
  - Every frame sets `meta["area"]`: public, auth, staff or supplier.
  - Sign-out (the red button) → w80; clicking the name → w00.
- **[suppliers.py](../../_src/suppliers.py):**
  - w70 → w70b → w70c are the register flow (no session). w70 now has the contact person and password, with 3 steps; w70c leads to "Follow my application".
  - New: w70d My application (Mpumudde, pending: the only menu entry).
  - Portal (Busoga Tech): w71 Home (renew banner, figures, open RFQ, latest payment, LPOs), w72 quotation (Submit → w73), w73 RFQs (1 open, 7 past), w74 Purchase orders, w74b LPO-2026-0051 (acknowledged 6 Oct 14:02 → paid), w75 Payments, w76 Company profile (bank changes checked by IDIU), w77 Documents, w77b Renew for 2027 (dialog).
- **[data.py](../../_src/data.py):** `SUPPLIER_ACCOUNTS`, `SUPPLIER_SESSIONS`, `SUPPLIER_MENU` (label, icon, target), `SUPPLIER_HOME`, `PREQUAL_ROUND`, `home_key()`.
- **[build.py](../../_src/build.py):**
  - `_order` lists the public site first; `MODULES` includes `public`.
  - PROTO changes:
    - no hash or an unknown key opens w80;
    - the bar buttons are Public site / Sign in;
    - `settle()`: an owner screen signs that account in, and public/auth pages end the session;
    - `allowed()` blocks another account's own screens;
    - supplier names are in NAMES, with an empty PERM;
    - each screen's JSON carries `area`.
- **[check.py](../../_src/check.py)** adds:
  - an area on every screen;
  - sessions for all 11 accounts;
  - every menu entry reaching a screen of theirs;
  - door checks: every public page has Sign in; Home, Sign in and Notices have Register; Register has Sign in; Sign in reaches every account's dashboard; w70c → w70d;
  - reach measured from w80.
- **[smoke.py](../../_src/smoke.py)** adds:
  - a no-hash → w80 check;
  - 12 walks: public → register → application; Home → Sign in for every staff walk; the full supplier portal; the applicant; sign out → Home;
  - the preload wait raised to 120 s.
- **PLAN.md**: §1 two new decisions, cast/roles, §6 the door and portal tables. **README**: counts, layout, key ranges + areas, viewer, tests, rules, presenting script (starts at the public Home).

## Uncommitted / in-flight
- Everything (the repo `bloodykheeng/idiu-pms`, branch `main`, still has no commits). The user said: don't commit until they say so.

## Next steps
1. User reviews `prototype.html` (Ctrl+F5) starting with no hash: Home → Notices → Sign in → each account; Register → application. Fix anything flagged; rerun build, check and smoke.
2. On the user's go: `git add -A`, commit (attribution from the system reminder), `git push -u origin main` (the proxy blocked GitHub once; the user may need to push).
3. Connect Vercel (preset Other, no build, output = repo root) → https://idiu-pms.vercel.app.

## Decisions settled this session
- **One front door** (user: "you design as if it's an essay, you don't reason how a system should be linked"): public → Sign in / Register → dashboard by who signed in (Alpha `dashboard/layout.tsx`: investor → portal, anyone else → staff). Rejected: registration as the entry; a portal without sign-in.
- **Supplier portal uses a sidebar like the console** (Alpha's investor portal does), so it reads as one system. Rejected: the old top-nav portal.
- **A pending applicant sees only My application.** No locked or greyed menu entries, because "nothing visible in a menu is dead".
- **Sign-out goes to the public Home; clicking the name goes to Sign in** (to switch accounts in the demo).
- **Notices carries the prequalification round and award notices only.** RFQs are not advertised (they go to prequalified suppliers), which keeps "no public tender portal" out of scope.
- **The prequalification round for 2027** (opened 1 Oct, closes Fri 20 Nov 2026) explains Busoga's "Renew for 2027" (sign the new declaration; the trading licence is uploaded in January).
- **Busoga's story stays closed and consistent:** 4 LPOs, all delivered and paid (UGX 58.9M); LPO-0051 shows acknowledgement as done (6 Oct 14:02, matching w14b). There is no pending LPO to acknowledge: adding one would contradict w20b and w71.
- **Award notices reuse existing facts:** LPO-0051 Busoga 36.4M; LPO-0049 Main Street 6.62M (from w12); Iganga chairs 7.3M (w12); Kagulu 6.2M (supplier register).

## Still open
| Question | Blocks | Recommendation |
| --- | --- | --- |
| Should a signed-in person see the public site with "Dashboard" instead of "Sign in" (as SDS does)? | nothing | Not now: in the demo, visiting the public site signs out, which is simpler to present |
| IDIU's real procurement email and notice practice (do they publish awards?) | nothing (illustrative) | Ask at requirements; procurement@idiu.org is illustrative |
| The rest of PLAN §8 (manual, thresholds, chart of accounts, sandbox) | as before | unchanged |

## Gotchas & context
- **Keys:** w80–w83 public · w00/w00b · w01–w63 staff · w70–w70c register · w70d, w71–w77b portal. `_order` sorts w8x first.
- **Areas drive everything.** A new frame must set `s.meta["area"]`, or check.py fails. The supplier `portal()` sets `owner=account`, so every portal screen is that company's own.
- **New supplier menu entries:** add them to `data.SUPPLIER_MENU` (and `shell.PORTAL_SECTION` for the group). check.py asserts the target's `owner` and `label` match.
- **Dark mode:** the deep panel colour `DEEP #0F3D25` is not remapped. Light-lime *strokes* become dark (use white `#FFFFFF`, which is kept), while light text keeps its colour.
- **The smoke preload can time out on a busy machine** (once at 60 s this session; it passed on rerun, and the wait is now 120 s). Don't run smoke during a PNG render.
- Same as before: write patch scripts with Write (heredocs break on apostrophes); `PYTHONIOENCODING=utf-8` for check/smoke; lint with autoflake + pyflakes.

## Where the record lives
- Docs updated: `PLAN.md` (§1, §2 cast, §3, §6), `README.md` (§2, §4, §5, §6, §7, §11).
- Live prototype: https://idiu-pms.vercel.app (not deployed yet)
- Session transcript: `~/.claude/projects/d--coding-new-wave-idiu-pms-procuremnt-managment-system/2d67113b-7e4e-4649-b797-7a6dcc72c91d.jsonl` (~11 MB).
  **Grep it, never read it whole.** Last resort only.

## How to verify
- `cd _src && python build.py && python combine.py` (both clean; 83 screens)
- `PYTHONIOENCODING=utf-8 python check.py` → 11 session lines, a door line, "83 screens · … 83 reachable from w80 ✓"
- `PYTHONIOENCODING=utf-8 python smoke.py` → door, 12 walks, "✓ smoke test passed"
- `python build.py --png w80 w00 w71` (PNGs in `_previews/`); `prototype.html?show` with no hash shows Home's hotspots
