---
description: Generate a dated HTML status page (project/status/status-YYYY-MM-DD.html) plus project/status/STATUS-SUMMARY.md, summarising this project from the protocol files, the latest diary entry, and recent git history.
---

<!-- ===========================================================================
     TEMPLATE — customize this file for the project.

     Every repo in the workspace has its own version of this command and no two
     are the same. That is deliberate: a marketing site's status page and a
     two-sided marketplace's status page should not look alike. Treat what
     follows as the floor, then adapt:

       - Add the sections this project actually needs (business funnel,
         infrastructure reference card, test/coverage counts, pilot metrics).
       - Delete the ones it doesn't.
       - Pick a palette and stick with it across runs so pages compare cleanly.
       - Set `group` / `profile` / `priority` in the summary block below — they
         drive the workspace portfolio roll-up.

     Delete this comment once customized.
     =========================================================================== -->

Generate a project status HTML report for **[Project Name]**.

## What to read first (do all reads in parallel)

**Protocol files:**
1. `PROJECT.md` — mission, users, success criteria, non-goals
2. `PLAN.md` — current milestone, definition of done, roadmap, open risks
3. `STATE.md` — what works, what's in progress, known issues
4. `TASKS.md` — Now / Next / Later / Done
5. `DECISIONS.md` — scan from the bottom for the most recent entries
6. `CLAUDE.md` — the Project Reference section (stack, data model, gotchas)

**Baseline for change tracking:**
7. The most recent **prior** status page — `ls -t project/status/status-*.html 2>/dev/null`,
   newest that is not today's output. Skim it for the previous milestone, the
   previous "Now" items, and previously listed decisions so the delta section
   shows real change. If none exists, state "First status page — no prior baseline."

**Activity:**
8. Newest file under `project/diary/`
9. `git log --oneline -20` (skip gracefully if not a git repo)
10. Source freshness: `git log -1 --format=%cs -- <file>` for `PLAN.md`,
    `TASKS.md`, `STATE.md`, `DECISIONS.md`, `PROJECT.md`. If not a git repo, use
    file mtimes and label the column "(file mtime)".

**AI+PROCESS:**
11. `ls AI+PROCESS.html 2>/dev/null` — if present, extract any inline logo SVG
    and the footer `LAST UPDATE:` date for a callout card. If only
    `AI+PROCESS.md` exists, link to that instead.

## Output

A single self-contained HTML file at:

```
project/status/status-YYYY-MM-DD.html
```

No external dependencies — all CSS and SVG inline, system font stack, responsive.

## Section order

1. **Header bar** — project name, stage badge, live URL if any, date
2. **Snapshot pills** — stack, hosting, current milestone, task counts
3. **Purpose, one sentence** — from PROJECT.md
4. **Since last status** — the delta against the prior page. Milestone moved?
   Tasks shipped? New decisions? This is the section that makes the page worth
   generating; if there is no prior page, say so explicitly.
5. **Current milestone** — definition of done as a checklist with real state
6. **What's working / in progress / known issues** — from STATE.md
7. **Task board** — Now / Next / Later
8. **Recent decisions** — last 3–5 from DECISIONS.md, dated
9. **Risks** — open risks from PLAN.md, plus anything in STATE.md that reads
   like one
10. **Source freshness** — table of protocol files and their last-change dates,
    flagging anything stale (amber > 30 days, red > 90)
11. **Footer** — "Generated YYYY-MM-DD · derived from PROJECT/PLAN/STATE/TASKS/DECISIONS, diary, git log"

## Rules

- **Report, don't invent.** No infrastructure, tests, users, or deployments that
  the files don't evidence. A concept-stage project with no code says so.
- **Label sources.** Where a number comes from a file, say which file.
- Deterministic colour rules — green/amber/red thresholds stated in the page, so
  two runs a month apart are comparable.
- Write the file directly; don't ask for confirmation first.
- After writing, confirm the path and list the sections included.

## Also write STATUS-SUMMARY.md

Then write (or overwrite) `project/status/STATUS-SUMMARY.md`. YAML frontmatter
only, no markdown body:

```
---
name: [Project Name]
tagline: <one sentence — what this project is; stable, changes rarely>
group: <SKYideas Revenue | Consulting | Personal | Utilities>
profile: <Business Product | Early Concept | Prototype Evaluation | Marketing Site | Consulting Engagement | Personal Project | Utility>
priority: <integer — rank within the workspace portfolio>
status: <one to three sentences — the most important things about current state; something that could change next week>
generated: <YYYY-MM-DD>
---
```

Overwrite every run — no date suffix, always one file. The workspace portfolio
roll-up reads these across all repos, so keep `group`, `profile` and `priority`
consistent with the sibling projects.
