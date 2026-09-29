# Plan

*Last rewritten: 2026-09-29*

## Current Milestone

**v0.1 vocabulary-aware Chapter 1 baseline** - make the first readable slice teach useful book vocabulary and ease low-value difficulty before the learner restarts *Le Comte de Monte-Cristo*.

### Definition of Done

- [x] Project docs describe the product vision, learner model, prototype constraints, and non-goals.
- [x] Repo identifies the actual French Monte-Cristo EPUB filename.
- [x] Static UI displays Chapter 1 passages in plain, guided, and original representations.
- [x] Reader supports first-pass contextual word help and original-text comparison.
- [ ] Reader supports vocabulary decisions from Chapter 1 analysis, with relevant explanations visible while reading.
- [ ] Chapter 1 preprocessing produces inspectable vocabulary records and a difficulty map using lemma, part of speech, chapter/available-book recurrence and later occurrences, modern frequency or learner level where available, and proper-name handling.
- [ ] Chapter 1 Plain/Guided representations are revised using the map: preserve words worth learning, ease low-value difficulty, and keep the original accessible.
- [x] Local event model tracks lookups, translations, and representation changes.
- [x] Rule-based adaptation engine surfaces a visible next-step recommendation.
- [x] EPUB parser extracts Chapter 1 into processed JSON and a file-friendly JS wrapper.

### After This Milestone

The learner restarts the book with the vocabulary-aware baseline and records app and schema feedback before Chapter 2 is processed.

### In Scope

- Chapter 1, "Marseille. L'arrivee."
- Three checked-in text representations.
- A transparent first-pass vocabulary classification: teach, simplify, or ignore/lightly gloss. Use a provisional B1-ish target and review the results by hand.
- Chapter 1 artifacts that connect vocabulary analysis to the generated data and the reader UI.
- Local-only browser state using `localStorage`.
- A simple, inspectable learner state panel.
- No build step.

### Out of Scope For This Milestone

- Authentication, account history, or cloud sync.
- Full EPUB library navigation.
- Automated translation quality evaluation.
- TTS, SRS flashcards, embeddings, and personalization beyond local heuristics.
- Backend service work.
- Perfect lemmatization, comprehensive literary-word detection, or a complete vocabulary model for the novel.

## Roadmap

1. **Vocabulary-aware Chapter 1 baseline** - generate the vocabulary profile and difficulty map, integrate their decisions into Chapter 1 data and reader help, and improve Plain/Guided output.
2. **Fresh reading pass** - restart the book, collect Chapter 1 feedback, then adjust the app, analysis rules, and schema based on observed friction.
3. **Process Chapter 2** - generate `c02.json` / `c02.js` using the reviewed rules and carry useful vocabulary forward.
4. **Transformation interface** - add a module that can improve Plain/Guided generation locally or through an LLM later.

## Easier With The Vault Dashboard Origin

- Load canonical `data/*.json` files directly with `fetch()` instead of relying on JavaScript wrappers.
- Lazy-load one chapter at a time once C02 exists, keeping the first page lighter.
- Use dynamic chapter manifests and a real chapter picker without directory listing.
- Treat `localStorage` under `127.0.0.1:8765` as stable reading progress instead of juggling `file://` state.
- Keep Markdown feedback files browser-readable for review while remembering the dashboard is read-only.

## Open Risks

- The Gallica EPUB includes OCR quirks and old punctuation that may need cleanup before automated passage extraction feels good.
- "Simplifying" a literary passage can erase too much style; the product needs comparison tools to keep the original visible.
- Lookup count alone is noisy. The model should remain humble until there are better signals.
- Vocabulary frequency and learner-level sources may have coverage or licensing limits; record source and uncertainty instead of presenting guesses as facts.
- Sentence translation is only a UI/data hook today. Chapter 1 has no generated translations; decide its scope from the fresh reading pass.
