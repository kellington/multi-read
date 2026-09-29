# Tasks

**Now** is 1–2 items. **Next** is what the agent proposes at the start of a
session. **Later** is a holding pen, not a backlog.

Keep Now + Next under ~10 items between them. Later can breathe, but anything
sitting there untouched across two milestones gets deleted, not re-filed.

When Done gets long, move it to `project/status/` history or drop it — git log
is the real record. Don't let this file become the project's second STATE.md.

## Now

Actively being worked on right now.

- [ ] Read Chapter 1 in the vocabulary-aware app and collect app, vocabulary, and schema ideas for Chapter 2 in `project/ideas/feeback-c01.md`.

## Next

The next handful, ordered.

- [ ] Review the reading notes, then revise the app, vocabulary rules, or chapter schema; decide whether and when to generate sentence meanings.
- [ ] Process Chapter 2 into `data/monte-cristo/c02.json` and `c02.js` using the reviewed rules.

## Later

Small near-term ideas that don't deserve an issue yet.

- [ ] Add optional LLM-backed transformations behind the chapter processor.
- [ ] Add an in-app chapter picker once more than one chapter is processed.
- [ ] Add a small smoke-test checklist or browser test for file-mode reader interactions.

## Done (recent)

Cleared at each milestone.

- [x] Replace starter project docs with Multi-Read product docs.
- [x] Build first static adaptive-reader visual slice.
- [x] Add chapter-by-chapter processing workflow.
- [x] Process Chapter 1 from the Monte-Cristo EPUB.
- [x] Analyze Chapter 1 vocabulary against the available volume with spaCy, FLELex, and Lexique; generate vocabulary records and a difficulty map.
- [x] Rebuild Chapter 1 and the static reader with vocabulary guidance and selected Plain substitutions.

---

**Bigger than a session?** Most work doesn't need more than a line here. But if
an item will run for several sessions, has hard out-of-scope boundaries, or will
be driven by `/goal`, copy `optional/subtask.md` to `tasks/<slug>.md` and link
it from the section above:

```
- [ ] Auth migration → tasks/auth-migration.md
```

Don't create the `tasks/` folder until something actually needs it.
