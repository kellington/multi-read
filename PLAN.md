# Plan

*Last rewritten: 2026-09-28*

## Current Milestone

**v0.1 readable slice** - prove the adaptive-reading loop with Chapter 1 of *Le Comte de Monte-Cristo*.

### Definition of Done

- [x] Project docs describe the product vision, learner model, prototype constraints, and non-goals.
- [x] Repo identifies the actual French Monte-Cristo EPUB filename.
- [x] Static UI displays Chapter 1 passages in plain, guided, and original representations.
- [x] Reader supports contextual word help, sentence translation, and original-text comparison.
- [x] Local event model tracks lookups, translations, and representation changes.
- [x] Rule-based adaptation engine surfaces a visible next-step recommendation.
- [x] EPUB parser extracts Chapter 1 into processed JSON and a file-friendly JS wrapper.
- [ ] Feedback from reading Chapter 1 is reviewed before processing Chapter 2.

### In Scope

- Chapter 1, "Marseille. L'arrivee."
- Three checked-in text representations.
- Local-only browser state using `localStorage`.
- A simple, inspectable learner state panel.
- No build step.

### Out of Scope For This Milestone

- Authentication, account history, or cloud sync.
- Full EPUB library navigation.
- Automated translation quality evaluation.
- TTS, SRS flashcards, embeddings, and personalization beyond local heuristics.
- Backend service work.

## Roadmap

1. **Chapter 1 feedback pass** - read C01, collect notes, and revise schema/rules.
2. **Process Chapter 2** - generate `c02.json` / `c02.js` using the revised schema.
3. **Transformation interface** - add a module that can improve Plain/Guided generation locally or through an LLM later.

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
