# State

*Last updated: 2026-09-28 00:00*

## Summary

Multi-Read now has a real project brief and a runnable static v0.1 reader slice. The canonical local URL is `http://127.0.0.1:8765/multi-read/`, served by the Knowledge vault dashboard. The app fetches processed Chapter 1 data from `data/monte-cristo/c01.json`, with plain/guided/original representations, contextual glossary help, original comparison, local event tracking, passage navigation, and a rule-based adaptation recommendation.

## What's working

- Static browser app in `index.html`, `src/app.js`, and `src/styles.css`.
- Chapter 1 processor output in `data/monte-cristo/c01.json`; `c01.js` remains optional for file-mode fallback.
- EPUB processing script in `scripts/process_chapter.py`.
- Feedback scratch file in `project/ideas/feeback-c01.md`.
- Extracted cover image at `assets/monte-cristo-cover.jpg`.
- Product docs in `PROJECT.md`, `PLAN.md`, and `README.md` are no longer starter templates.
- The actual French source EPUB path is identified in docs and sample data.

## In progress

- Chapter 1 is processed first pass. Next work is to read it and collect feedback before changing schema or generating Chapter 2.

## Known issues

- The learner model is intentionally naive: lookup and translation counts are rough friction signals, not a real proficiency estimate.
- Plain mode is currently mechanical segmentation, not a high-quality simplification.
- Sentence translations are not generated in schema v1; the app disables `Show meaning` when no translation exists.

## Business snapshot

No separate business workstream yet.

## Environment / setup

Only what's non-obvious about the dev loop. Stable commands and stack facts
belong in CLAUDE.md's Project Reference, not here — this file is rewritten
constantly and reference material rots in it.

Canonical app URL: `http://127.0.0.1:8765/multi-read/`.

The Knowledge vault dashboard serves this repo from `/Users/rob/Documents/GitHub/Rob/Knowledge` via LaunchAgent `com.robkellington.vault-dashboard` on `127.0.0.1:8765`. `python3 -m http.server 5173` is only a fallback. `localStorage` under `127.0.0.1:8765` is the real progress store; `file://` and `localhost:5173` state are throwaway.

## Open questions

- Whether sentence meaning support should be generated for every sentence.
- How much simplification is acceptable before a passage stops feeling like Dumas.
- What changes Chapter 1 feedback requires before processing C02.

## Resolved this session

- Replaced starter-kit docs with Multi-Read docs.
- Added the first static visual reader slice.
- Added chapter-by-chapter processing workflow and processed C01.

---

*Updated at the end of every session by `/end-session`. This is the file the
agent reads first next session — if it's stale, everything downstream is wrong.*
