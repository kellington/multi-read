# Vocabulary-Aware Preprocessing for Le Comte de Monte-Cristo

This note sketches a practical direction for improving Multi-Read's preprocessing for French source texts, using *Le Comte de Monte-Cristo* as the first target.

The core idea is not to make the book merely easy. The goal is to teach enough French, in the right order, that the original gradually becomes readable.

Multi-Read should simplify where simplification protects flow, teach where a word is useful for this book, and ignore or lightly gloss vocabulary that is rare, decorative, archaic, or unlikely to pay off again.

## Existing Signals

There is already public evidence that *Monte-Cristo* can be analyzed usefully through vocabulary frequency.

### Monte-Cristo text mining

A Wikiversity text-mining project analyzed the full French Wikisource text of *Le Comte de Monte-Cristo*:

- Source: https://fr.wikiversity.org/wiki/Utilisateur%3ATaniaKET/Analyses_textuelles_%28M2_D2SN%2C_2024-2025%29
- Reported corpus: about 217,648 words.
- Reported sentences: about 9,066.
- Useful observation: terms such as "Pharaon", "Marseille", and "Monte-Cristo" cluster in different parts of the novel, which suggests that vocabulary difficulty and usefulness should be tracked locally, not only globally.

### speak.tatar frequency bands

speak.tatar has already processed sections of *Le Comte de Monte-Cristo, Tome I* against French frequency bands:

- Section 27: https://speak.tatar/en/lit/fra/text/le-comte-de-monte-cristo-tome-i-27/
  - 2,376 word tokens.
  - 960 unique words.
  - 41.7% of words are in the 2,000 most common words.
  - 54.3% are in the 5,000 most common words.
  - 60.0% are in the 8,000 most common words.
- Section 14: https://speak.tatar/en/lit/fra/text/le-comte-de-monte-cristo-tome-i-14/
  - 4,499 word tokens.
  - 1,533 unique words.
  - 40.3% of words are in the 2,000 most common words.
  - 53.4% are in the 5,000 most common words.
  - 59.0% are in the 8,000 most common words.

This is close to one piece of the Multi-Read preprocessing pipeline: chapter-by-chapter vocabulary profiling. Multi-Read can go further by combining this with CEFR levels, local recurrence, proper-name handling, and simplification decisions.

## Lexical Sources

### FLELex: French CEFR vocabulary

FLELex is the most relevant pedagogical resource because it maps French lemmas to CEFR-oriented learner levels.

- Download page: https://cental.uclouvain.be/cefrlex/flelex/download/
- Description: graded lexical resource for French foreign learners.
- Useful fields: lemma, part of speech, CEFR information, normalized frequencies by CEFR level.
- TreeTagger version: 14,236 lemmas, useful for NLP pipelines because its tagset matches TreeTagger.
- CRF Tagger version: 17,871 lemmas and includes multiword expressions, useful pedagogically.
- License noted on the FLELex site: CC BY-NC-SA 4.0.

Why it matters: a raw frequency rank says whether a word is common in general. FLELex helps decide whether a learner is likely to have seen the word by A1, A2, B1, B2, C1, or C2.

### Lexique: modern French frequency

Lexique is useful as a modern French frequency source.

- Main site: https://www.lexique.org/
- English info/download page: https://www.lexique.org/?lang=en&page_id=790
- Current release note: https://www.lexique.org/?lang=en&p=953
- Description: lexical database for roughly 140,000 French word forms with frequency counts, lemmas, grammatical category, phonological information, syllables, and related fields.

Why it matters: *Monte-Cristo* is 19th-century literary French. Multi-Read needs a way to distinguish:

- common modern French words,
- book-specific words,
- old-fashioned or literary words,
- names and places,
- words that are rare everywhere and not worth actively teaching.

Lexique can provide the modern-frequency baseline that FLELex does not fully cover.

## Proposed Workflow

```text
EPUB
  |
  v
extract chapter
  |
  v
tokenize + lemmatize
  |
  v
lexical enrichment
  |-- FLELex / CEFR
  |-- Lexique / modern frequency
  |-- novel / local frequency
  |-- rules / names-expressions
  |
  v
difficulty map
  |
  v
LLM simplification
  |
  v
B1-ish chapter
```

The "difficulty map" is the key handoff between deterministic preprocessing and LLM rewriting. The LLM should not be asked to guess blindly which words are hard, important, archaic, recurring, or safe to preserve. Preprocessing should hand it a structured map.

## Enriched Vocabulary Record

For each token or lemma in a chapter, generate an enriched vocabulary record.

```json
{
  "word": "demeure",
  "lemma": "demeure",
  "part_of_speech": "NOUN",
  "monte_cristo_frequency": {
    "chapter_count": 1,
    "book_count": 12,
    "first_seen_chapter": 1,
    "future_frequency": 11
  },
  "general_french_frequency": {
    "source": "Lexique",
    "rank_or_frequency": null,
    "band": "mid"
  },
  "cefr_level": "B2",
  "archaic_or_literary": true,
  "proper_noun": false,
  "future_frequency": 11
}
```

Required fields for a first implementation:

- `word`: surface form from the chapter.
- `lemma`: normalized dictionary form.
- `part_of_speech`: coarse POS is enough at first.
- `monte_cristo_frequency`: local counts from this book.
- `general_french_frequency`: modern French frequency from Lexique or a local derived frequency band.
- `cefr_level`: A1-C2 when available from FLELex.
- `archaic_or_literary`: boolean or score. Start heuristic, improve later.
- `proper_noun`: boolean. Important for names, ships, places, and titles.
- `future_frequency`: how often this lemma appears after the current chapter.

The duplicate `future_frequency` at top level is intentional for early ergonomics. Later, keep one canonical location after the schema settles.

## Difficulty x Usefulness-To-This-Book

Do not rank words by difficulty alone. Rank them by:

```text
difficulty x usefulness-to-this-book
```

Difficulty asks: "Will a learner understand this now?"

Usefulness-to-this-book asks: "Will learning this help the reader keep reading *Monte-Cristo*?"

This creates three practical classes:

### Teach

Teach words that are moderately difficult and useful.

Examples:

- recurring verbs or nouns,
- words central to the plot,
- literary words that repeat enough to become worth knowing,
- B1-B2 words that unlock many sentences.

Treatment:

- preserve the French word when possible,
- add a short inline gloss or hover note,
- repeat support across chapters,
- prefer "teach once, reinforce often" over translating every occurrence.

### Simplify

Simplify words or constructions that are too hard for the current target level but not worth teaching yet.

Examples:

- rare literary adjectives,
- long abstract phrases,
- unusual syntax,
- passe simple forms that block comprehension before the reader is ready.

Treatment:

- replace with easier French,
- keep the meaning faithful,
- optionally retain the original in a note if it is beautiful, famous, or thematically important.

### Ignore Or Lightly Gloss

Ignore or lightly gloss words that should not consume learner attention.

Examples:

- proper names,
- ship names,
- place names,
- one-off rare objects,
- archaic words with low future frequency,
- terms understandable from context.

Treatment:

- mark as known-by-context,
- avoid overloading the reader with vocabulary cards,
- do not simplify names unless they cause genuine confusion.

## Design Principle

Multi-Read should not produce a flat "easy French" version of *Monte-Cristo*.

It should produce a guided reading path toward the original.

That means each chapter version should make deliberate tradeoffs:

- Preserve high-value original vocabulary.
- Simplify low-value difficulty.
- Keep recurring book-specific words visible.
- Identify names and places so they are not mistaken for unknown vocabulary.
- Track what the reader has already been taught.
- Let later chapters become closer to the original as the learner's book-specific vocabulary grows.

The reader should feel the French getting richer, not permanently replaced.

## Implementation Notes

### Tokenization and lemmatization

Start with a reliable French NLP stack rather than hand-rolled token rules. Good candidates:

- spaCy French model for tokenization, POS, lemmatization, and named entities.
- TreeTagger if aligning tightly with FLELex-TT becomes important.

For the prototype, spaCy is likely faster to wire into the existing app. Add a later compatibility layer if FLELex tag mapping requires it.

### Frequency joins

Build small local lookup tables:

- `flelex_lemma_pos -> cefr_level`
- `lexique_word_or_lemma -> frequency/rank/band`
- `monte_cristo_lemma -> total_count, chapter_counts, first_seen_chapter`
- `monte_cristo_lemma_chapter -> count`

Normalize casing and apostrophes before matching. Keep the raw surface form too.

### Proper nouns and names

Names are unusually important in *Monte-Cristo*:

- Edmond
- Dantès
- Mercédès
- Morrel
- Danglars
- Fernand
- Pharaon
- Marseille

The preprocessor should mark these as proper nouns and avoid counting them as ordinary vocabulary difficulty. Some names still need reader support, but they belong in a character/place index, not in the same queue as learner vocabulary.

### Archaic or literary detection

Start with heuristics:

- high frequency in *Monte-Cristo* but low frequency in Lexique,
- not found in FLELex,
- POS patterns common in literary narration,
- manually curated list from review of Chapter 1,
- passe simple verb forms detected by morphology.

This should be a score eventually, but a boolean is enough for the first prototype.

## Chapter 1 Prototype

Codex can validate the approach with Chapter 1 before building the full pipeline.

### Goal

Generate a vocabulary-aware preprocessing artifact for Chapter 1 and use it to produce a better B1-ish simplified chapter.

### Inputs

- Existing Chapter 1 source text from the Multi-Read project.
- FLELex download.
- Lexique download.
- A simple per-book frequency table generated from the available *Monte-Cristo* source text.

### Prototype output files

Suggested outputs:

- `chapter-001.tokens.json`
- `chapter-001.vocabulary.json`
- `chapter-001.difficulty-map.json`
- `chapter-001.simplification-notes.md`
- optionally, a regenerated B1-ish Chapter 1 text using the difficulty map.

Exact paths should follow the app's existing data layout.

### Minimal vocabulary record for prototype

```json
{
  "word": "arriva",
  "lemma": "arriver",
  "part_of_speech": "VERB",
  "chapter_count": 2,
  "book_count": 120,
  "future_frequency": 118,
  "general_french_frequency_band": "common",
  "cefr_level": "A1",
  "archaic_or_literary": false,
  "proper_noun": false,
  "classification": "teach"
}
```

### Classification rules for first pass

Use transparent rules before adding model judgment:

- `proper_noun = true` -> `ignore_or_gloss`
- `cefr_level in A1,A2` and modern frequency is common -> `keep`
- `cefr_level in B1,B2` and `future_frequency >= 5` -> `teach`
- missing CEFR, rare modern frequency, and `future_frequency >= 5` -> `teach_or_gloss`
- missing CEFR, rare modern frequency, and `future_frequency < 5` -> `simplify`
- archaic/literary and low future frequency -> `simplify`
- archaic/literary but high future frequency -> `teach`

Keep the rules data-driven and inspectable. The point is not to be perfect; it is to make the LLM's rewriting job less vague.

### LLM prompt shape

For each paragraph or scene, pass:

- original French,
- target level, initially B1-ish,
- vocabulary records for words in that span,
- list of words to preserve and teach,
- list of words to simplify,
- list of names/place terms to preserve,
- style instruction: preserve plot, tone, and important recurring vocabulary.

The model should return:

- simplified French paragraph,
- preserved teaching vocabulary,
- changed difficult words,
- short rationale for major substitutions.

### Validation checks

For Chapter 1, inspect:

- Does the output preserve the plot accurately?
- Are names preserved and not treated as vocabulary burden?
- Are high-value recurring words retained?
- Are one-off hard words simplified?
- Does the text feel like a bridge toward Dumas rather than a replacement summary?
- Can the app show why a word was taught, simplified, or ignored?

## Practical Next Steps

1. Add a small preprocessing script or task that extracts Chapter 1 tokens, lemmas, POS, and named entities.
2. Download or document how to load FLELex and Lexique into local lookup tables.
3. Generate book-level and chapter-level frequency counts for *Monte-Cristo*.
4. Produce `chapter-001.vocabulary.json`.
5. Add classification rules for `teach`, `simplify`, and `ignore_or_gloss`.
6. Generate `chapter-001.difficulty-map.json`.
7. Run one LLM simplification using the difficulty map.
8. Compare the result against the current Chapter 1 reading experience and record feedback in the existing Chapter 1 notes.

## Open Questions

- Should Multi-Read target B1, B1/B2, or a reader-configurable level?
- Should passe simple be taught early as a recurring literary pattern, or normalized until later chapters?
- Should FLELex multiword expressions be used from the start, or deferred until single-word records work?
- How should learned vocabulary persist across chapters and across books?
- Should proper nouns live in a separate character/place memory from vocabulary?
- What license constraints apply if FLELex or Lexique-derived fields are bundled with the app rather than generated locally?

## References

- FLELex download: https://cental.uclouvain.be/cefrlex/flelex/download/
- Lexique: https://www.lexique.org/
- Lexique English download/info page: https://www.lexique.org/?lang=en&page_id=790
- Lexique 4 release note: https://www.lexique.org/?lang=en&p=953
- Wikiversity Monte-Cristo text-mining analysis: https://fr.wikiversity.org/wiki/Utilisateur%3ATaniaKET/Analyses_textuelles_%28M2_D2SN%2C_2024-2025%29
- speak.tatar *Le Comte de Monte-Cristo*, Tome I, section 14: https://speak.tatar/en/lit/fra/text/le-comte-de-monte-cristo-tome-i-14/
- speak.tatar *Le Comte de Monte-Cristo*, Tome I, section 27: https://speak.tatar/en/lit/fra/text/le-comte-de-monte-cristo-tome-i-27/
