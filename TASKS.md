# Tasks

**Now** is 1–2 items. **Next** is what the agent proposes at the start of a
session. **Later** is a holding pen, not a backlog.

Keep Now + Next under ~10 items between them. Later can breathe, but anything
sitting there untouched across two milestones gets deleted, not re-filed.

When Done gets long, move it to `project/status/` history or drop it — git log
is the real record. Don't let this file become the project's second STATE.md.

## Now

Actively being worked on right now.

- [ ] Read Chapter 1 and collect notes in `project/ideas/feeback-c01.md`.
- [ ] Before C02, review feedback and revise the chapter JSON schema / processing rules.

## Next

The next handful, ordered.

- [ ] Process Chapter 2 into `data/monte-cristo/c02.json` and `c02.js`.
- [ ] Decide whether sentence meaning support should be generated for every sentence or only on demand.
- [ ] Improve Plain mode beyond mechanical segmentation.
- [ ] Add a small smoke-test checklist or browser test for file-mode reader interactions.

## Later

Small near-term ideas that don't deserve an issue yet.

- [ ] Add optional LLM-backed transformations behind the chapter processor.
- [ ] Add an in-app chapter picker once more than one chapter is processed.

## Done (recent)

Cleared at each milestone.

- [x] Replace starter project docs with Multi-Read product docs.
- [x] Build first static adaptive-reader visual slice.
- [x] Add chapter-by-chapter processing workflow.
- [x] Process Chapter 1 from the Monte-Cristo EPUB.

---

**Bigger than a session?** Most work doesn't need more than a line here. But if
an item will run for several sessions, has hard out-of-scope boundaries, or will
be driven by `/goal`, copy `optional/subtask.md` to `tasks/<slug>.md` and link
it from the section above:

```
- [ ] Auth migration → tasks/auth-migration.md
```

Don't create the `tasks/` folder until something actually needs it.
