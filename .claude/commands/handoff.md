---
description: Write a structured handoff note capturing the current state of the mockups so another session can resume cleanly.
argument-hint: "[optional short title for the handoff]"
allowed-tools: Read, Glob, Grep, Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Bash(git rev-list:*), Write
---

# /handoff

Produce a **handoff note** for the work done this session on the IDIU procurement mockups, so a fresh
session (or another developer) can pick up exactly where things stand. Title hint: $ARGUMENTS

> ⚠️ **Make this session identifiable.** Sessions are auto-titled from your first reply, so
> every `/handoff` otherwise collapses to the same generic "Handoff" title. The **very first
> line** of your reply MUST name the actual work being saved (from `$ARGUMENTS` if given, else
> the session's main theme). Format:
>
> `Handoff: <specific topic of this session>`
>
> e.g. `Handoff: approval engine + setup screens`. Do NOT lead with generic
> "Handoff note" boilerplate.

## Gather state
This folder (`idiu pms procuremnt managment system/mockups`) is **one git repo** (remote `bloodykheeng/idiu-pms`, deployed to
Vercel on every push to `main`). Collect:

- Current branch: `git branch --show-current`
- Working-tree changes: `git status --short`
- Uncommitted diff summary: `git diff --stat`
- Recent commits this session: `git log --oneline -15`
- Whether those commits are pushed: `git rev-list --left-right --count origin/<branch>...<branch>`

Do not rebuild the screens or run Chrome just to gather state.

Also note the **session transcript path** for the Record section below. Transcripts live at
`~/.claude/projects/<project-slug>/<session-id>.jsonl`; the session id is the directory name in
your own scratchpad path. Record it, never read it: they run to tens of megabytes.

## Write the note
Save to `.claude/handoffs/YYYY-MM-DD-HHmm-<kebab-title>.md` (use the real current date/time).
Use this template, be concrete and specific, no filler:

```markdown
# Handoff: <title>
_Date: <YYYY-MM-DD HH:mm> · Author: Claude_

## Goal
<What we set out to do this session, in 1-2 sentences.>

## Status
<Done / In progress / Blocked: one line.>

## What changed
- <bullet list of concrete changes, by screen key (w10b, w31b…) and file, e.g. [procurement.py](_src/procurement.py#Lnn)>

## Uncommitted / in-flight
- <Files with pending edits, why they are not finished. State "none: all committed and pushed" if clean.>

## Next steps
1. <The very next action, specific enough to start immediately.>
2. ...

## Decisions settled this session
- **<What was decided>**: <why, in the user's own reasoning where they gave it.>
  Rejected: <the alternative and why it lost, if one was weighed.>
- ...

## Still open
| Question | Blocks | Recommendation |
| --- | --- | --- |
| <the open question> | <what it stops, or "nothing"> | <the leaning, and why> |

## Gotchas & context
- <Dead ends, things to NOT redo, build caveats, screens that must stay consistent with each other.>

## Where the record lives
- Docs written or updated: <PLAN.md, README.md, BRIEFING.md, …: the next session reads those before the note>
- Live prototype: https://idiu-pms.vercel.app (if the Vercel project is renamed, see README §8)
- Session transcript: `~/.claude/projects/<slug>/<session-id>.jsonl` (~NN MB).
  **Grep it, never read it whole.** Last resort only, for something this note failed to capture.

## How to verify
- `cd _src && python build.py && python combine.py` (both must run clean)
- Link check: every hotspot target in `prototype.html` exists and every screen is reachable
  (targets may be prefixed `!back:` / `!tab:`; `!theme` is the light/dark switch)
- Look at the screens: `python build.py --png <key>` renders PNGs into `_previews/`
  (headless Chrome won't render narrower than ~500 px)
- Open `prototype.html?show#<key>` to see the hotspots
```

### On the Decisions section
This is the part a future session cannot reconstruct from the code, and it is why the note
exists. Write the **reasoning**, not just the conclusion: a conclusion can be re-derived from
good reasoning, never the reverse. Record what the user settled explicitly so it is not
relitigated, and record what was rejected so the same dead end is not walked twice.

A long design session can settle dozens of things across many messages. If the volume is large,
put the detail in `PLAN.md` (decisions) or `README.md` (rules) and let this section carry the
headlines plus the link. The note should stay readable in one sitting.

After writing, print the saved path and a 3-line summary. Do **not** commit anything unless asked.
