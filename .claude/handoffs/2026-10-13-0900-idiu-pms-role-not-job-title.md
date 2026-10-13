# Handoff: IDIU mockup: approval steps name the role (Executive Approver), not the job title
_Date: 2026-10-13 09:00 · Author: Claude_

**Read `2026-10-13-0700-…-committed.md` (the session), then the 0750 and 0830 notes.** This note is the last change of
the session. Docs (PLAN, README, PATTERNS) are current as of this note.

## Goal
The user saw "With the Country Director" on the applicant's page (w70d) and asked whether that was correct. It wasn't:
since every person has one role, Samuel's role is **Executive Approver**, and "Country Director" is only his job title.

## Status
**Done. check.py and smoke.py pass (104 screens, 13 walks); screens checked; committed and pushed.**

## What changed
- **Every approval step, decision, status and "waiting on" in `_src` names the role:**
  - "With the Executive Approver", "Executive Approver's decision", "Samuel Kato · Executive Approver";
  - covering the public Home and FAQs, the supplier portal, budgets, setup notes, workflows, evaluations and My approvals titles;
  - 51 replacements.
- **"Country Director" remains only where it is a job title or a name:**
  - `data.JOB["samuel"]` (his dashboard line);
  - the department "Country Director's office";
  - the role description "High-value and final approvals (the Country Director)".
- **The public Home's "Stores"** (delivery) and the GRN history line now say "Inspection Officer".
- **Docs:**
  - PLAN §1 has a new decision row ("A job title is not a role") and all role references updated;
  - PATTERNS §2 gets the rule;
  - "System Admin" → "System Administrator" everywhere in the docs.
  - Memory: `mockup-every-button-works` gains the rule.

## Decisions settled
- **A job title is not a role.** Screens name roles for steps and decisions; a job title appears only beside the person's name (their dashboard). This follows one role per person (0750 note).

## Next steps
- User review (Ctrl+F5): the applicant (w70d), Home, and Samuel's pages.
- Nothing else is open from the user. PLAN §8 questions are for IDIU; connect Vercel when ready.

## How to verify
- `cd _src && python build.py && python combine.py && PYTHONIOENCODING=utf-8 python check.py && PYTHONIOENCODING=utf-8 python smoke.py`
- `grep -n "Country Director" _src/*.py` shows only `data.py` (job, department, role description).
