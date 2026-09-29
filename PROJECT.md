# Multi-Read

> A local-first reader that teaches the French worth learning for a book, eases less useful difficulty, and helps learners move toward the original text.

## Why This Exists

Language learners quickly outgrow textbook passages, but real novels are often too hard to read without drowning in dictionary lookups. Multi-Read asks whether a reader can stay inside an authentic book while learning the vocabulary that will make later chapters easier. It should preserve useful recurring French, simplify difficulty with little learning payoff, and offer help without losing sight of the original.

The prototype starts with Chapter 1 of *Le Comte de Monte-Cristo*. Before the first fresh reading pass, Chapter 1 and the reader should include vocabulary-aware analysis and guidance. The learner will then restart the book, record friction and desired changes while reading, and use that evidence to revise the app and chapter schema before processing later chapters. Chapters are processed into JSON as needed, not all at once.

## Who It's For

- Primary user: an intermediate French learner who wants to read classic literature without constantly leaving the page.
- Secondary user: the builder, using the prototype to learn what adaptation signals are worth collecting before adding heavier AI machinery.

## Success Criteria

- [ ] A learner can read a processed French chapter in three difficulty representations: plain, guided, and original.
- [ ] Chapter 1 preprocessing identifies vocabulary by lemma, chapter and available-book recurrence (including later occurrences), learner difficulty, and names; its inspectable rules decide what to teach, simplify, or lightly gloss.
- [ ] The Chapter 1 reader uses those decisions to preserve useful original French, provide relevant word help, and make Plain mode a genuine bridge toward the original rather than mechanical segmentation.
- [ ] The UI offers contextual word help and original-text comparison without hiding the French.
- [ ] The app records local learning events such as word lookups, translation requests, and difficulty changes.
- [ ] A simple rule-based learner model recommends an easier, harder, or steady representation from those events.
- [ ] The prototype runs without an API key by using processed chapter JSON.
- [ ] A fresh Chapter 1 reading pass can produce concrete app and schema feedback before Chapter 2 is processed.

## Non-Goals

- Authentication, accounts, sync, or cloud infrastructure.
- Whole-book preprocessing up front.
- Automatically rewriting the whole novel or proving that vocabulary classifications are perfect.
- A complete EPUB library.
- Spaced repetition, TTS, embeddings, grammar tutoring, or social features.
- Production-quality AI text transformation.
- Storing personal learning data outside the browser.

## Constraints

- Keep v0.1 deliberately tiny: one book, one processed chapter at a time, one local browser app.
- Use Chapter 1 as the first vocabulary-aware baseline. Keep the analysis and its decisions inspectable and correctable.
- Do not require paid APIs for the first visual slice.
- Put any future LLM transformation behind the chapter-processing workflow so the UI can run against static processed JSON.
- Treat the supplied Monte-Cristo EPUB as source material; do not build around a proprietary service.
- Use `http://127.0.0.1:8765/multi-read/` as the canonical local app URL; `localStorage` under that origin is the real progress store.
