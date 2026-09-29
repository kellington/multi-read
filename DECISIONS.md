# Decisions

Append-only log of meaningful decisions. Never edit past entries — if a
decision is reversed, add a new entry that references the old one.

## How to write an entry

```
## [YYYY-MM-DD] — Short title

**Decision:** What we decided, in one sentence.
**Why:** The reasoning that drove it.
**Trade-off:** What we're giving up.
**Impact:** What changes because of this (code, scope, process).
```

Keep entries short. If you need more than ~8 lines, you're probably
writing a design doc, which belongs elsewhere.

---

## [2026-09-28] — Keep v0.1 static and local

**Decision:** Build the first reader slice as static HTML, CSS, and vanilla JavaScript.
**Why:** The interesting question is the adaptive reading loop, not framework setup or infrastructure.
**Trade-off:** No production app architecture yet.
**Impact:** The prototype runs with `python3 -m http.server 5173` and stores learner events only in browser `localStorage`.

## [2026-09-28] — Serve through vault dashboard

**Decision:** Treat `http://127.0.0.1:8765/multi-read/` as the canonical local app URL.
**Why:** The Knowledge vault dashboard provides an always-on HTTP origin and avoids `file://` browser limits.
**Trade-off:** The dashboard is read-only static hosting, so app writes still stay in `localStorage`.
**Impact:** The app can fetch chapter JSON directly; `localStorage` under `127.0.0.1:8765` is the real progress store.
