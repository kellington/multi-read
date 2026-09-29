# Chapter data and lexical sources

`c01.json` is the static reader input. `c01.js` is the file-mode wrapper.
`c01.tokens.json` contains the token-level surface forms, lemmas, parts of
speech, and passage offsets. `c01.vocabulary.json` contains the Chapter 1
lemma/POS records and source coverage. `c01.difficulty-map.json` records the first-pass classification
rules and candidates. These are processing artifacts, not claims that every
candidate has already been rewritten in Plain mode.

The recurrence counts cover the 55 chapters in the French EPUB checked into
`Books/`, not the complete *Le Comte de Monte-Cristo*. `futureFrequency` means
occurrences in later chapters of that available volume. The spaCy French model
supplies the lemmas and coarse parts of speech. The pipeline has known OCR,
tagging, and historical-language errors, so the classifications need reading
review.

Learner levels come from [FLELex / Beacco with TreeTagger tags](https://cental.uclouvain.be/cefrlex/flelex/download/),
by François, Gala, Watrin and Fairon, and Pintard and François. FLELex is
licensed [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Modern lemma frequencies come from [Lexique 4](https://lexique.org/), by New,
Pallier, Schalchli, Bourgin and Gimenes, licensed
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The source
tables are downloaded locally to `data/lexical-sources/`, which is ignored by
Git. Missing joins remain null in the generated chapter data.

The word definitions and selected Plain substitutions are project-curated.
The generated classifications are suggestions for review, not proficiency
assessments or a full literary simplification.
