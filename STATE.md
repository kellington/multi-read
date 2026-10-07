# State

*Last updated: 2026-09-29*

## Summary

Multi-Read has a vocabulary-aware first-pass Chapter 1 baseline. The processor analyzes the 55 chapters in the available French volume with spaCy, joins FLELex learner levels and Lexique modern frequencies, and generates vocabulary records, a difficulty map, and rebuilt chapter JSON. The reader uses curated vocabulary decisions in contextual help and eases selected low-value terms in Plain mode. The learner is starting a fresh Chapter 1 reading pass to collect improvements for Chapter 2. The canonical URL is `http://127.0.0.1:8765/multi-read/`.

## What's working

- Static browser app in `index.html`, `src/app.js`, and `src/styles.css`.
- Vocabulary-aware Chapter 1 data in `data/monte-cristo/c01.json`; `c01.js` remains optional for file-mode fallback.
- Reproducible processing in `scripts/process_chapter.py` and `scripts/vocabulary.py`; `c01.vocabulary.json` and `c01.difficulty-map.json` expose the analysis.
- Reader modes: Plain eases selected terms and separates some long units, Guided keeps original wording with vocabulary buttons, and Original presents unmarked source text.
- Feedback scratch file in `project/ideas/feedback-c01.md`.
- Extracted cover image at `assets/monte-cristo-cover.jpg`.
- Product docs in `PROJECT.md`, `PLAN.md`, and `README.md` are no longer starter templates.
- The actual French source EPUB path is identified in docs and sample data.

## In progress

- The learner's fresh Chapter 1 reading and feedback pass in `project/ideas/feedback-c01.md`. Capture app, vocabulary, and schema ideas for Chapter 2, then review them before processing C02.

## Known issues

- The learner model is intentionally naive: lookup and translation counts are rough friction signals, not a real proficiency estimate.
- Plain mode has selected curated substitutions but is not a reviewed B1 simplification; many passages still retain literary syntax.
- Automatic lemmas, proper names, lexical joins, and classification rules can be wrong, especially with OCR and historical French. Reader meanings are curated for a subset of Chapter 1 terms rather than generated for every lemma.
- Frequency counts cover the 55-chapter available volume, not the entire novel.
- Sentence translations are not generated in Chapter 1 schema v2; the reader hides `Show meaning` when no translation exists.

## Business snapshot

No separate business workstream yet.

## Environment / setup

Only what's non-obvious about the dev loop. Stable commands and stack facts
belong in CLAUDE.md's Project Reference, not here — this file is rewritten
constantly and reference material rots in it.

Canonical app URL: `http://127.0.0.1:8765/multi-read/`.

The Knowledge vault dashboard serves this repo from `/Users/rob/Documents/GitHub/Rob/Knowledge` via LaunchAgent `com.robkellington.vault-dashboard` on `127.0.0.1:8765`. `python3 -m http.server 5173` is only a fallback. `localStorage` under `127.0.0.1:8765` is the real progress store; `file://` and `localhost:5173` state are throwaway.

## Open questions

- Whether sentence meaning support should be generated for every sentence or only where a reader needs it.
- How much simplification is acceptable before a passage stops feeling like Dumas.
- How much vocabulary guidance is helpful before highlighting becomes distracting.
- What the fresh Chapter 1 reading pass will reveal before C02.
- PLAN.md still shows the three vocabulary-analysis and integration criteria unchecked, although the baseline is implemented. Reconcile the checklist when the current milestone is closed.

## Resolved this session

- Rebuilt Chapter 1 with vocabulary analysis, contextual help, and selected Plain substitutions; previously smoke-tested the static reader.
- Removed two non-public-domain EPUBs from Git history before pushing the repository to GitHub. At closeout, `main` and `origin/main` are at `ce9e9f3`; these STATE.md and TASKS.md updates are uncommitted.
- Set the next handoff: use the app to gather Chapter 2 improvements before changing the processor or chapter schema.

---

*Updated at the end of every session by `/end-session`. This is the file the
agent reads first next session — if it's stale, everything downstream is wrong.*
