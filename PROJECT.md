# Multi-Read

> A local-first adaptive reader for language learners who want to read real books with just enough help to stay in the story.

## Why This Exists

Language learners quickly outgrow textbook passages, but real novels are often too hard to read without drowning in dictionary lookups. Multi-Read explores a narrower question: can a reader keep someone inside an authentic book by adjusting the representation of a passage, showing contextual help, and learning from moments of friction?

The prototype starts with Chapter 1 of *Le Comte de Monte-Cristo* because the French source text is available in the repo and the opening scene is vivid enough to make the interaction feel real. Chapters are processed into JSON as they are needed so the schema can evolve from actual reading feedback.

## Who It's For

- Primary user: an intermediate French learner who wants to read classic literature without constantly leaving the page.
- Secondary user: the builder, using the prototype to learn what adaptation signals are worth collecting before adding heavier AI machinery.

## Success Criteria

- [ ] A learner can read a processed French chapter in three difficulty representations: plain, guided, and original.
- [ ] The UI offers contextual word help and original-text comparison without hiding the French.
- [ ] The app records local learning events such as word lookups, translation requests, and difficulty changes.
- [ ] A simple rule-based learner model recommends an easier, harder, or steady representation from those events.
- [ ] The prototype runs without an API key by using processed chapter JSON.

## Non-Goals

- Authentication, accounts, sync, or cloud infrastructure.
- Whole-book preprocessing up front.
- A complete EPUB library.
- Spaced repetition, TTS, embeddings, grammar tutoring, or social features.
- Production-quality AI text transformation.
- Storing personal learning data outside the browser.

## Constraints

- Keep v0.1 deliberately tiny: one book, one processed chapter at a time, one local browser app.
- Do not require paid APIs for the first visual slice.
- Put any future LLM transformation behind the chapter-processing workflow so the UI can run against static processed JSON.
- Treat the supplied Monte-Cristo EPUB as source material; do not build around a proprietary service.
- Use `http://127.0.0.1:8765/multi-read/` as the canonical local app URL; `localStorage` under that origin is the real progress store.
