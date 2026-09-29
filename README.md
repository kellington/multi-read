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

- Vocabulary-aware first-pass processing of chapter 1 of the French EPUB:
  `Books/Le_comte_de_Monte-Cristo_Tome_[...]Dumas_Alexandre_btv1b8600196s.epub`
- A visual cover asset extracted from that EPUB:
  `assets/monte-cristo-cover.jpg`
- Three checked-in passage representations:
  - `plain`: selected low-value nautical and literary terms eased, plus segmentation into smaller reading units. This still needs reading review.
  - `guided`: original prose with highlighted vocabulary guidance.
  - `original`: normalized source text from the EPUB.
- Contextual word help with a teaching choice and later-occurrence count from the available volume.
- A visible set of words worth learning in each passage.
- Sentence-level meaning data hooks; C01 has no translations, so the reader hides those controls for now.
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
Books/...epub (55 available French chapters)
  -> spaCy + local FLELex and Lexique tables
  -> scripts/process_chapter.py
  -> data/monte-cristo/c01.tokens.json + c01.vocabulary.json + c01.difficulty-map.json
  -> data/monte-cristo/c01.json
  -> index.html
```

The vocabulary record includes lemma, part of speech, Chapter 1 and available-volume recurrence, later occurrences, modern-frequency band, CEFR level when matched, name handling, and an inspectable teach/simplify/light-gloss decision. See [chapter data notes](data/monte-cristo/README.md) for source attribution and limits. Raw lexical tables stay in the ignored `data/lexical-sources/` folder.

The [Chapter 1 review notes](data/monte-cristo/c01.simplification-notes.md) list which decisions actually changed Plain mode and what to watch during the fresh reading pass.

To rebuild Chapter 1, use Python 3.13 for the processing environment. Download the source tables from the [FLELex](https://cental.uclouvain.be/cefrlex/flelex/download/) and [Lexique 4](https://lexique.org/databases/Lexique400/) sites into `data/lexical-sources/`, then run:

```sh
uv venv --python /usr/local/bin/python3.13 .venv
uv pip install --python .venv/bin/python -r requirements-processing.txt
.venv/bin/python -m spacy download fr_core_news_sm
.venv/bin/python scripts/process_chapter.py \
  --epub 'Books/Le_comte_de_Monte-Cristo_Tome_[...]Dumas_Alexandre_btv1b8600196s.epub' \
  --chapter-path OEBPS/e08600196_c01.html --chapter-id c01 \
  --title 'Marseille. L’arrivee.' \
  --flelex data/lexical-sources/FleLex_TT_Beacco.tsv \
  --lexique data/lexical-sources/Lexique400.tsv \
  --out-json data/monte-cristo/c01.json --out-js data/monte-cristo/c01.js
```

Restart Chapter 1 with this baseline and keep product notes in `project/ideas/feeback-c01.md`. Before processing Chapter 2, review those notes and adjust the app, schema, or processing rules.

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
