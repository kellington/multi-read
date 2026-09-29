# Project Protocol — Multi-Read

This file tells AI agents how to operate in this repo. Content about *what* the
project is lives in the five sibling files — this file is about *how we work*,
plus durable project reference that agents need on hand.

> **This is the protocol file.** `AGENTS.md` is a pointer back here for
> non-Claude tools. Edit this one.

## What this repo is, in one line

Multi-Read is a static local-first prototype for adaptive language reading, starting with chapter-by-chapter processing of *Le Comte de Monte-Cristo*.

## Source of truth

- **PROJECT.md** — why this exists, who it's for, success criteria, non-goals.
- **PLAN.md** — current milestone and roadmap. Rewritten at milestone boundaries.
- **STATE.md** — snapshot of where things are right now. Updated every session.
- **DECISIONS.md** — append-only log of decisions and their trade-offs. Never rewrite entries.
- **TASKS.md** — active and near-term work. Rolls over constantly.

If any of these conflict, ask me which one is right. Don't silently reconcile.

Only the main session writes these files — subagents read them but never edit them.

<!-- If this project carries a business workstream alongside the build, say so
     here. Three sibling projects landed on the same wording:

     These protocol files are company-level: they carry both the product
     workstream (building the thing) and the business workstream (customers,
     revenue, pilots, validation). STATE.md carries a Business Snapshot pointing
     at `project/business/business-status.md`; TASKS.md tags items
     **Product —** / **Business —**; DECISIONS.md is the single decision log for
     both. Detailed business artifacts live in `project/business/`.
-->

## Session protocol

Use the **`/start-session`** and **`/end-session`** skills. They are global
(`~/.claude/skills/`) and carry the full loop — read state, check git, flag
drift, propose, then update STATE.md / TASKS.md / DECISIONS.md on the way out.
Don't restate the loop here; it will drift.

`/start-session` explicitly scans this file for **session supplements**, so put
anything repo-specific under the heading below and it will be picked up.

### Session supplements for this repo

<!-- Delete this section if there's nothing. Real examples from sibling repos:
     - Run the test suite before proposing work; STATE.md claims it's green.
     - At end of session, append the next session's opening prompt to
       `project/diary/diary-YYYY-MM.md` under a `### Next Prompt` heading.
     - Running a second interactive session in parallel? Use a manual
       `git worktree` on a feature branch and don't touch the protocol files
       from it.
-->

- 

The canonical local app URL is `http://127.0.0.1:8765/multi-read/`, served by the Knowledge vault dashboard (`com.robkellington.vault-dashboard`). Treat this HTTP origin as the real reading environment; `localStorage` there is the real progress store. `file://` and `localhost:5173` are fallback/test contexts.

## Milestones

When I say "milestone" or "checkpoint":

1. Rewrite PLAN.md against reality, not against the old plan.
2. Prune TASKS.md — archive done items, drop anything that no longer matters.
3. Re-read PROJECT.md's success criteria. Confirm they still hold, or propose edits.
4. Summarize what shipped since the last milestone.

Between milestones PLAN.md is read-only. Note drift in STATE.md under "open
questions" instead.

## Status reporting

Run **`/project-status`** (`.claude/commands/project-status.md`) to generate a
dated, self-contained HTML page at `project/status/status-YYYY-MM-DD.html` plus
`project/status/STATUS-SUMMARY.md`, which feeds the workspace portfolio roll-up.

Customize that command for this project — it is meant to be tailored, not
generic. See its header comments.

## Guardrails

Always ask before:

- Installing new dependencies
- Schema or migration changes
- Destructive file operations (delete, overwrite outside the working set)
- Commits or pushes
- Running anything that touches production data or external services

Prefer small, reversible changes. If you're unsure, stop and ask. These
guardrails bind subagents too — a team member who hits one flags it in their
report instead of proceeding.

### Guardrails specific to this repo

<!-- The highest-value section in this file. Generic guardrails stop generic
     mistakes; these stop the mistake that would actually hurt *this* project.
     Write them as absolutes, and say *why* — the reason is what makes an agent
     honour it under pressure. Real examples:

     - **Never `git add` anything under `data/`.** It holds PII for ~1,000 real
       people. If you catch yourself force-adding past `.gitignore`, stop.
     - **Never add a git remote.** This repo is local-only by decision.
     - **Writes to live accounts are opt-in and dry-run by default.**
     - **Snapshot before you mutate.** Any command that rewrites the master
       writes a timestamped copy first.
     - **Anything that collects real consumer health data** — privacy and
       consent are part of the product, not paperwork.

     Delete this comment and the placeholder if the project has none yet. -->

- 

## Conventions

<!-- Fill in per project. Leave a line blank until it's actually decided —
     an invented convention is worse than a missing one. -->

- **Language / stack:** Static HTML, CSS, and vanilla JavaScript modules for v0.1.
- **Code style:** Small modules, plain browser APIs, no build step until the prototype needs one.
- **Naming:**
- **Testing:** For now, run a local static server and smoke-test the reader in a browser.
- **Commits:** (message format, squash vs merge)
- **Branching:**
- **Secrets / env:** (where `.env.example` lives; `SECRETS.PRIVATE.YAML` is the
  local scratchpad, gitignored, copied from the `.example` twin — never the
  deployed secret store)

## AI team

The orchestrator doctrine — how **Alice** behaves, activation, handoffs,
statelessness, and routing to the shared members **Harry** (hiring), **Rex**
(research), **Peter** (project-room prep) and **Quincy** (QA) — is global in
`~/.claude/CLAUDE.md`. Add only this project's specialists here.

<!-- Delete this section if the project has no specialists. Example (conforma):

     - **Team docs:** roster at `project/team/_Roster.md`.
     - **Specialists** (`.claude/agents/`):
       - Frontend (React/Vite/Tailwind) → **Fred** (`subagent_type: fred`)
       - Backend (Flask/SQLAlchemy/Postgres) → **Betty** (`subagent_type: betty`)
     - **Parallel work:** Fred and Betty own different trees and can run
       concurrently. If two agents must mutate the same files, give them
       `isolation: "worktree"` — never hand-roll worktree checkouts.
     - **Handoff shortcut:** spec → Betty → API contract → Fred.
-->

## Notes to the agent

- Short, direct writing over hedging. "I don't know" beats a guess.
- If a task takes more than ~3 tool calls of exploration without progress, stop and check in.
- Don't reformat or restructure the protocol files unless I ask. Small content edits only.
- Terms of art for this project go in `GLOSSARY.md` — create it the first time a
  term needs pinning down (the `/grill-me` skill expects it there).

---

## Project Reference

Durable facts agents need while working. **Update only when reality changes —
not every session.** This is the section that keeps stack detail, data models
and business rules out of STATE.md, where they'd rot.

<!-- Delete the headings you don't need. Drawn from what sibling repos actually
     found worth writing down. -->

### Data model

Processed chapter data lives in `data/monte-cristo/`: each chapter has canonical JSON. Chapter 1 also has token, vocabulary, and difficulty-map JSON plus simplification notes, generated or informed by the offline spaCy/FLELex/Lexique workflow described in `README.md`. The vault dashboard serves JSON, so the app can load chapters with `fetch()`. Runtime learner state is local browser state in `localStorage` under `multi-read-v0.1`; the canonical copy is under `http://127.0.0.1:8765`.

### User roles

<!-- Who can do what. -->

### Key flows

1. Choose a passage representation: plain, guided, or original.
2. Tap highlighted words for contextual help.
3. Show sentence meaning when the French blocks comprehension.
4. Compare against the original source text.
5. Let local reading events update the visible adaptation recommendation.

### Business rules

<!-- Rules that aren't obvious from the code and that agents keep re-deriving. -->

### Commands

```
# canonical local app
open http://127.0.0.1:8765/multi-read/

# fallback local server
python3 -m http.server 5173

# process chapter 1 (set up .venv and local lexical source tables per README.md first)
.venv/bin/python scripts/process_chapter.py --epub 'Books/Le_comte_de_Monte-Cristo_Tome_[...]Dumas_Alexandre_btv1b8600196s.epub' --chapter-path OEBPS/e08600196_c01.html --chapter-id c01 --title 'Marseille. L’arrivee.' --flelex data/lexical-sources/FleLex_TT_Beacco.tsv --lexique data/lexical-sources/Lexique400.tsv --out-json data/monte-cristo/c01.json --out-js data/monte-cristo/c01.js

# test
open http://127.0.0.1:8765/multi-read/ and smoke-test mode switching, word help, navigation and reset

# build / deploy
n/a for v0.1 static prototype
```

### Known gotchas

- The French source EPUB is `Books/Le_comte_de_Monte-Cristo_Tome_[...]Dumas_Alexandre_btv1b8600196s.epub`; chapter 1 text is in `OEBPS/e08600196_c01.html`.
- The French EPUB is a 55-chapter volume, not the whole novel. Vocabulary `futureFrequency` is relative to later chapters in that volume. Raw FLELex and Lexique tables are local and gitignored; source attribution is in `data/monte-cristo/README.md`.
- The Penguin Classics and HarperCollins EPUBs were removed from Git history before the public push. Do not reintroduce them; review rights before tracking any new EPUB.
- Chapter feedback goes in `project/ideas/feeback-c01.md` before processing C02.
- The vault dashboard is read-only static hosting. If persistence beyond `localStorage` is needed, coordinate with the Knowledge/vault dashboard session rather than adding an API here.
