# Handoff: IDIU mockup: NEXT, one system with one front door (public site → sign in / register → role dashboard)
_Date: 2026-10-13 01:10 · Author: Claude_

**Read this first, then `2026-10-13-0051-idiu-pms-complete-state-for-new-session.md` (everything built so far),
then `PLAN.md` and `README.md`.** This note is the work for the new session; the 0051 note is the state it
starts from.

## Goal of the next session
The user reviewed the supplier portal and called the structure wrong:
- the mockup **starts at supplier registration** as if it were a separate system;
- portal links **don't click**;
- there is **no sign-in** for suppliers.

Rebuild the entry and the supplier side so the mockup reads as **one system with one front door**, the way
real apps are linked:

```
Public site (no sign-in)              Sign in / Register (one door)        Dashboard, shaped by who signed in
Home · About · FAQs · Notices   ──►   Sign in (staff AND suppliers)   ──►  staff → the console (built, w-screens)
                                      Register (suppliers only)       ──►  supplier → the supplier portal (rebuild)
                                      Forgot password                      pending applicant → their application status
```

The user's words: "the dashboard can change depending… get ideas from Alpha, it has an investor portal… you
design as if it's an essay, you don't reason how a system should be linked."

## The two references, read before designing (both confirmed this session)
**SDS** (`../../mops sds/sds new/sds-mops-workspace/sdstool-nextjs`):
- Public landing at `sdstool.ug`: Home · About · FAQs in the top bar, a moon toggle, **Sign in**, a hero, and "Sign in to the portal" / "How the standards work".
- `/login`: a split screen with branding on the left and the form on the right ("Good morning", email/phone, password, Remember me, Login, Sign in with Google, Back to home).
- `AuthContext` + `AppSidebar` filtered by `lib/routeAccess.ts`; Dashboard is common to every role and shaped by the role.

**Alpha** (`../../CPA accounts system/alpha-fund-system-workspace/alpha-fund-nextjs/app`):
- route groups `(main)` (about, faqs, support, home `page.tsx`), `(auth)` (login, register, onboarding,
  forgot-password, shared `BrandingPanel.tsx`), and `dashboard/` with **parallel slots `@admin` and `@investor`**;
- `dashboard/layout.tsx` picks the slot by role: **investor → client portal, any other signed-in role → staff**;
- the investor portal has its own pages (accounts, transactions, statements, subscribe, profile, support), all real.

## The plan (decide details as you build, but keep this shape)
1. **Public site (new, no session):** `Home`, `About`, `FAQs`, `Notices`.
   - **Notices** is IDIU's procurement notices: an open prequalification round (Nov 2026, categories), and award notices for transparency.
   - The public header has Home · About · FAQs · Notices, the moon toggle and **Sign in**.
   - The **Home hero** carries "Sign in" and "Register as a supplier", with IDIU's identity and a fresh design, not a copy of SDS.
2. **Auth (new):**
   - **One Sign in page** for staff and suppliers: a split layout like SDS / Alpha's BrandingPanel, a "Register as a supplier" link, Forgot password, Back to home, and the demo "sign in as" panel. That panel includes **supplier accounts**: Busoga Tech (prequalified) and Mpumudde (application pending).
   - **Register:** today's w70 → w70b → w70c become the register flow, reached from Sign in and Home. After submitting, the applicant's "dashboard" is their **application status** until approved.
   - **Forgot password:** a small screen.
3. **Dashboard by role (Alpha's `@admin` / `@investor`):**
   - **Staff:** the console exactly as built (sessions, per-person dashboards w01-<person>).
   - **Suppliers:** a **real supplier portal in which every menu entry has its screen**:
     - Home (dashboard);
     - RFQs (open and past) → Submit quotation (w72);
     - Purchase orders → LPO detail and acknowledge;
     - Payments (paid LPOs with EFT refs);
     - Company profile;
     - Documents (expiry and renew).
   - Choose a sidebar or the current top nav for the portal, consistently.
   - Suppliers are **sessions** too: the person and company never change on a click.
4. **Viewer:** no hash opens the **public Home**, not staff sign-in. The bottom-bar buttons Staff console / Supplier portal become "Public site · Sign in". Sessions extend to supplier accounts (`settle` / `allowed` in `build.py` PROTO, `menu_for` in `data.py`).
5. **Keys:** pick a scheme that keeps ordering sane. `_order` in build.py parses `int(key[1:3])`, so either keep `w` keys in free number ranges (e.g. public w80–w84, auth w85–w89, supplier portal w70–w79), or extend `_order`.
6. **Tests:** extend `check.py` (supplier sessions closed; public pages reach Sign in and Register; every portal menu entry resolves) and `smoke.py` walks:
   - Public Home → Sign in → each staff dashboard;
   - Home → Register → submitted → application status;
   - Sign in → Busoga Tech → RFQ → quote → POs → payments → profile → documents;
   - sign out → Home.
7. **Docs:** update PLAN.md (§1 decision: one front door; §6 screen map) and README (viewer, keys, presenting
   script starts at the public Home). Then `/handoff`.

## Acceptance (what "done" looks like)
- Opening `prototype.html` with no hash shows the **public Home**. Every public link works. Sign in and Register are reachable from Home and from each other.
- Signing in as any staff person or either supplier lands on **their** dashboard. Every visible menu entry in their sidebar or nav opens a screen; nothing visible in a menu is dead.
- **No screen shows a different person or company than the one signed in.** check.py proves it for every session (staff and suppliers).
- `check.py` and `smoke.py` pass. Look at the PNGs of every new screen before reporting.

## Rules the user has set (keep)
- **Reason about how a real system is linked before drawing screens:** public → auth → role-shaped dashboard (memory: `mockup-architecture-front-door`).
- **One signed-in person per session; System Admin sees every menu; others only theirs** (memory: `mockup-sessions-like-real-app`).
- **Master data first; maker-checker on financial records; don't over-build; web only; fresh look;** run `check.py` + `smoke.py` after every change.

## State to verify at the start
- Nothing is committed (repo `bloodykheeng/idiu-pms`, branch `main`, no commits). Commit and push only when the user says so.
- `cd _src && python build.py && PYTHONIOENCODING=utf-8 python check.py` should report 70 screens and pass.

## Gotchas
Same as the 0051 note. The ones that bite most:
- **Patch scripts:** write them with the Write tool; bash heredocs break on apostrophes.
- **Owned screens:** `owner=True` for any screen showing one person.
- **New menu entries:** a new console menu entry needs `data.MENU`, `PERMS` and `shell.NAV`.
- **Running the tests:** don't run `smoke.py` during a PNG render; use `PYTHONIOENCODING=utf-8` for check/smoke.
