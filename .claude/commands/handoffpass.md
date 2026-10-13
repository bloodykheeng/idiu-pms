---
description: Pick up the baton, load the latest (or named) handoff note, verify the repo state matches, and resume work on the IDIU procurement mockups.
argument-hint: "[handoff filename or title fragment, defaults to most recent]"
allowed-tools: Read, Glob, Grep, Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*)
---

# /handoffpass

Resume work from a handoff note written by `/handoff`. Selector: $ARGUMENTS

> ⚠️ **Make this session identifiable.** Sessions are auto-titled from your first reply, so
> every `/handoffpass` otherwise collapses to the same generic "Handoff pass" title. The
> **very first line** of your reply MUST name the actual work being resumed, taken from the
> handoff's title/goal, not the handoff mechanics. Format:
>
> `Resuming: <specific topic from the note> · <status>`
>
> e.g. `Resuming: IDIU procurement mockups · setup screens done`.
> Do NOT lead with "Handoff pass", "picking up the baton", or similar boilerplate.

## Steps
1. **Locate the note.** Look in `.claude/handoffs/`.
   - If `$ARGUMENTS` is given, match it against filenames (filename or title fragment).
   - Otherwise pick the most recent file by timestamp in the name.
   - If the folder is empty or no match, say so and stop: do not guess.

2. **Lead with the identifiable line above**, then restate in 3-5 lines: the goal, the status,
   and the listed next steps.

3. **Verify reality matches the note.** Run `git status --short`, `git branch --show-current` and
   `git log --oneline -5` in this folder. Flag any drift: e.g. the note says files are uncommitted
   but the tree is clean, newer commits exist, or you are on a different branch. Surface
   mismatches before doing anything else; the note reflects state when written, which may be stale.

4. **Read what the note points at, before acting.** Read `PLAN.md` (what the system is, the story, every screen and its links), `README.md` (how screens are generated,
   the rules that keep the story consistent) and anything else the note mentions.
   The note carries headlines, those carry the reasoning. Treat the "Decisions settled" section
   as closed unless the user reopens it, and do not re-propose anything listed as rejected.

5. **Surface the open questions.** If the note has a "Still open" table, restate it. An entry
   marked as blocking means that work cannot start until the user answers, so ask before
   beginning it rather than picking a default and building on the guess.

6. **Confirm the plan.** Briefly state the next action you will take (the first "Next step" from the
   note, adjusted for any drift you found). Then proceed with the work unless it is risky or
   ambiguous, in which case ask first.

Screens are **generated**: never edit `web/*.svg`, the `-dark` folder or
`prototype.html` by hand; change the Python in `_src/` and rebuild.

The session transcript path in the note is a **last resort**, not a starting point. Those files
run to tens of megabytes and are mostly tool calls; grep for a specific string if the note and
its docs genuinely fail to answer something, and never read one whole.

Do not modify the handoff file. When the resumed work reaches a good stopping point, suggest
running `/handoff` again to refresh it.
