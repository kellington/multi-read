# Multi-Read

Multi-Read is a local-first prototype for adaptive reading. It starts with Chapter 1 of Alexandre Dumas's *Le Comte de Monte-Cristo* and lets a French learner move between three representations of each passage: plain, guided, and original.

The point is not to build a big reading platform yet. The point is to make the core loop visible: read, ask for help, compare against the original, record friction, and adapt the next representation.

## Run It

The canonical local URL is served by the Knowledge vault dashboard:

<http://127.0.0.1:8765/multi-read/>

Progress in `localStorage` under this origin is the real reading state.

No dependencies are required for the fallback server:

```sh
python3 -m http.server 5173
```

Then open <http://localhost:5173/>.

Opening `index.html` directly is a throwaway fallback. The app is designed around an HTTP origin so it can fetch processed chapter JSON directly.

## Current Slice

- Full first-pass processing of chapter 1 of the French EPUB:
  `Books/Le_comte_de_Monte-Cristo_Tome_[...]Dumas_Alexandre_btv1b8600196s.epub`
- A visual cover asset extracted from that EPUB:
  `assets/monte-cristo-cover.jpg`
- Three checked-in passage representations:
  - `plain`: mechanical first-pass segmentation into smaller reading units.
  - `guided`: authentic prose with glossary highlighting.
  - `original`: normalized source text from the EPUB.
- Contextual word help.
- Sentence-level meaning hooks; C01 shows a clear placeholder until we decide whether to generate translations.
- Original-text comparison.
- Previous/next passage navigation.
- Local event log for lookups, translations, and difficulty changes.
- Rule-based adaptation recommendation.

## Architecture

This is intentionally just static HTML, CSS, and JavaScript.

```text
index.html            App shell
src/styles.css        Responsive UI and reading surface
src/app.js            Reader state, events, adaptation rules
data/monte-cristo/    Processed chapter JSON plus optional file-friendly JS wrappers
scripts/              EPUB extraction and chapter processing scripts
assets/               Local visual assets
Books/                Source EPUBs
```

## Chapter Workflow

The app reads processed chapter data, not the EPUB directly. Each chapter has a canonical JSON file. The vault dashboard serves `.json`, so the app loads chapter data with `fetch()`.

```text
Books/...epub
  -> scripts/process_chapter.py
  -> data/monte-cristo/c01.json
  -> index.html
```

While reading Chapter 1, keep product notes in `project/ideas/feeback-c01.md`. Before processing Chapter 2, review those notes and adjust the schema or processing rules.

## Learner Model

The v0.1 learner model is deliberately simple. It keeps local counts for:

- word lookups
- sentence translation requests
- representation changes
- current representation

The adaptation rule is visible in the UI:

- many lookups or translations means the current representation is probably too hard
- no help requests on an easier representation means the learner can try a harder one
- otherwise, stay steady

This is a starting hypothesis, not a claim of intelligence.

## Non-Goals

Multi-Read v0.1 does not include accounts, cloud sync, a complete EPUB library, TTS, SRS, embeddings, or production AI transformation. Those can come later if the reading loop proves interesting.
