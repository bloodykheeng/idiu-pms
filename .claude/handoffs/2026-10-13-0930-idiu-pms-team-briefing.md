# Handoff: IDIU mockup: team briefing (BRIEFING.md) published and linked
_Date: 2026-10-13 09:30 · Author: Claude_

**Read `2026-10-13-0700-…-committed.md` (the session) first, then the 0750, 0830 and 0900 notes.** This is the
session's last step. All docs (PLAN, README, PATTERNS, BRIEFING) are current, and everything is committed and pushed.

## Goal
The user asked whether a BRIEFING.md existed (earlier notes listed it as optional; it didn't), then: "add it… I
should be able to get links and also share it to my colleagues, so I don't think it needs to be private."

## Status
**Done and pushed** (`3237b1b docs: add team briefing with a linked walkthrough`).

## What changed
- **New `BRIEFING.md`** (repo root), for the NWT team presenting to IDIU, modelled on Letshego's briefing. It covers:
  1. what IDIU is and what Mutungi asked for;
  2. their asks mapped to screens;
  3. words decoded (RFQ, LPO, GRN, prequalification, maker-checker, three-way match, PPDA…);
  4. the nine roles and who plays them;
  5. how a purchase moves;
  6. a 12-minute walkthrough;
  7. likely questions with short answers (above all: a mockup is not a sandbox);
  8. questions to clear with IDIU;
  9. watch-outs;
  10. a screen index.
- **108 direct links** to `https://idiu-pms.vercel.app/prototype.html#<key>`, covering 73 screens, all checked against `prototype.html`.
- **Public on purpose:** BRIEFING.md is not in `.vercelignore`, and the repo is public. It holds **no prices and nothing confidential**; keep it that way.
- README (top bullets, layout table, the Vercel note) and PLAN (header) link to it.

## Where to share it
- **Rendered (best):** https://github.com/bloodykheeng/idiu-pms/blob/main/BRIEFING.md
- **Raw on the deploy:** https://idiu-pms.vercel.app/BRIEFING.md
- **The prototype:** https://idiu-pms.vercel.app (live and current, confirmed this session)

## Decisions settled
- **The briefing is public and shareable**, so it never carries prices or confidential client details. (The user: it doesn't need to be private.) Rejected: keeping it internal via `.vercelignore`.

## Gotchas
- When a screen key changes or is removed, **re-run the link check** for BRIEFING.md (a short script: extract `prototype.html#key` links and compare them with the keys in `prototype.html`). `check.py` doesn't cover markdown.
- PLAN.md links inside BRIEFING (e.g. `PLAN.md#6-screens-and-links`) work on GitHub, not on Vercel, because PLAN is not deployed.

## Next steps
1. Share the GitHub link with the team; rehearse with the walkthrough (§6) and the watch-outs (§9).
2. After IDIU's feedback, update PLAN §8 (their answers) and BRIEFING §7 and §8.
