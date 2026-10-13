# Handoff: IDIU mockup: session close (front door, review fixes, one role per person, briefing), all pushed
_Date: 2026-10-13 · Author: Claude_

**Start here.** This note is the state at the end of the session and indexes the others. For the details of each step,
read the notes listed under "The trail". Then read `PATTERNS.md`, `PLAN.md` and `README.md`.

## Links
| What | Link |
|---|---|
| Prototype (live, current) | https://idiu-pms.vercel.app |
| README | https://github.com/bloodykheeng/idiu-pms/blob/main/README.md |
| Plan (design record) | https://github.com/bloodykheeng/idiu-pms/blob/main/PLAN.md |
| Patterns (reusable rules) | https://github.com/bloodykheeng/idiu-pms/blob/main/PATTERNS.md |
| Team briefing (share it) | https://github.com/bloodykheeng/idiu-pms/blob/main/BRIEFING.md |
| Repo | https://github.com/bloodykheeng/idiu-pms (public; Vercel redeploys `main` on every push) |

## Status
**Done. Everything is committed and pushed; `main` matches GitHub with nothing uncommitted.**
- 104 screens (light and dark) and 106 per-person sidebars.
- `check.py` and `smoke.py` pass (13 walks, plus door, forms, modal, full-screen and dark checks).

## What the mockup is now
- **One front door:**
  - public site: Home, About, FAQs, Notices;
  - one Sign in for staff and suppliers, plus Register and Forgot password;
  - a dashboard chosen by who signed in: the staff console, the supplier portal, or the applicant's status.
- **One role per person**, using the proposal's names (§15): Requesting Officer, Department Head, Finance Officer, Procurement Officer, Evaluation Committee Member, Executive Approver, Inspection Officer, System Administrator, Auditor, plus Supplier. Job titles (Country Director, Budget Holder, Procurement Manager) are not roles.
- **Records waiting on an approver open as full pages from their lists**, in that menu: requisitions, award, application, revision. The approver decides on their own copy (`<key>-<person>`); everyone else sees "Waiting on …".
- **Dialogs only for small forms** (setup lists' New, Add user, New financial year, Renew). Every create/edit button opens its form for the roles allowed; the Auditor reads only.
- **Viewer:**
  - one "Web dashboard" button;
  - sessions that never change on a click;
  - the sidebar dimmed under dialogs;
  - in full screen, the bar appears only at the bottom edge.

## Decisions settled this session (details in PLAN §1)
1. One system with one front door (Alpha `dashboard/layout.tsx`, SDS landing and login).
2. The supplier portal uses a sidebar frame; suppliers are sessions.
3. Every create/edit button works, as `write` forms; budgets belong to Finance and the System Administrator, and the Executive Approver approves.
4. Dialogs for small forms only; records are pages ("be wise, not everywhere").
5. Approve in context: from the record's list as well as from My approvals.
6. The highlighted row is the clickable one; nothing is clickable under a dialog.
7. Sign-in accounts appear in the order the work flows, with quiet step numbers (no badges on avatars).
8. **One role per person**, named as in the proposal; the committee is a role given by appointment; a stand-in shares the role (Daniel → Rebecca Achan).
9. **A job title is not a role**: steps and decisions name the role (Executive Approver).
10. **Budget Holder and Procurement Manager are job titles**: the nine roles are enough (the user: "what we have now is enough and good… some could just have been job titles"). Don't reopen this.
11. Commits are logical and dependency-ordered with conventional messages; never one bulk commit.
12. BRIEFING.md is public and shareable, so it holds no prices or confidential details.

## Still open
| Question | Blocks | Recommendation |
| --- | --- | --- |
| IDIU's procurement manual, thresholds, approvers | final workflows | ask IDIU (PLAN §8); the mockup uses labelled examples |
| Accounting package and chart of accounts; financial year; committees | Finance integration | ask IDIU |
| Does IDIU need a separate approval step for a Budget Holder or Procurement Manager? | nothing | only then add a role |
| Is "Country Director" IDIU's real title for its final approver? | nothing (it is only a job title on Samuel's dashboard) | confirm in the meeting |
| A sandbox for hands-on "data entry" testing | their full ask | a build after requirements (BRIEFING §7) |

## The trail (this session's notes, oldest first)
- `0110`: the plan for the front door (written in the previous session).
- `0125`: the front door built (public site, sign in, register, supplier portal).
- `0530`: review round 1 (forms, record handling, modal fixes, highlights, one viewer button).
- `0630`: review round 2 (Add user, setup "New" dialogs, pages not dialogs, full-screen bar, sign-in order).
- `0700`: the comprehensive session note and the first 12 commits.
- `0750`: one role per person (the proposal's names), Harriet and Rebecca added.
- `0830`: requisition approvals and the award as pages from their lists.
- `0900`: steps name the role, not the job title.
- `0930`: BRIEFING.md published.
- `0945` (this note): session close; Budget Holder and Procurement Manager are job titles.

## Gotchas (the ones that bite)
- **Screens are generated.** Change `_src/*.py`, then run `python build.py && python combine.py`; never hand-edit `web/`, `chrome/` or `prototype.html`. Commit sources and generated output in separate commits.
- **A new frame must set `meta.area`.** A form uses `shell.writes(s, roles)` (roles, not people). `overlay()` clears the links under a dialog, so add the dialog's own links after it.
- **An own copy `<key>-<person>` replaces `<key>`** for that person, in the viewer and in check.py.
- **After renaming or removing a screen key, re-check BRIEFING.md's links** (a short script: compare its `prototype.html#key` links with the keys in `prototype.html`).
- **Practicalities:**
  - write patch scripts with the Write tool (heredocs break on apostrophes);
  - run check and smoke with `PYTHONIOENCODING=utf-8`;
  - don't run smoke during a PNG render;
  - review with Ctrl+F5.
- **Note filenames run ahead of the clock.** This session's notes were timestamped ahead of the real time so they sort in order. Keep naming new notes later than `0945`.

## How to verify
```
cd _src
python build.py && python combine.py               # 104 screens
PYTHONIOENCODING=utf-8 python check.py              # "104 screens · … 104 reachable from w80 ✓"
PYTHONIOENCODING=utf-8 python smoke.py              # "✓ smoke test passed"
git status --short                                  # empty
git rev-list --left-right --count origin/main...main   # 0 0
```

## Where the record lives
- Docs: PATTERNS.md, PLAN.md, README.md, BRIEFING.md.
- Memory:
  - `mockup-every-button-works` (one role per person, job titles vs roles, pages vs dialogs, buttons, highlights);
  - `mockup-architecture-front-door`;
  - `mockup-sessions-like-real-app`;
  - `mockup-testing-practice`.
- Session transcript: `~/.claude/projects/d--coding-new-wave-idiu-pms-procuremnt-managment-system/2d67113b-7e4e-4649-b797-7a6dcc72c91d.jsonl`. **Grep it, never read it whole.**
