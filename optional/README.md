# Optional pieces

Nothing in this folder gets copied into a new project by default. Pull a file
across only when the project actually needs it, then delete this folder from
the copy.

## `subtask.md`

A structured brief for one piece of work that is bigger than a `TASKS.md` line:
several sessions long, hard out-of-scope boundaries, or destined to run under
`/goal`. Copy it to `tasks/<slug>.md` and link it from `TASKS.md`.

**Use it sparingly.** Across the whole workspace this has been copied into one
repo and never filled in — a `TASKS.md` line covers almost everything. The
format earns its weight only when a `/goal` run needs a machine-checkable
definition of done and explicit verification commands.

## Client-engagement variant

For consulting work (see `Clients/GenesisData`), the protocol shifts:

| Standard | Engagement variant |
|---|---|
| `PROJECT.md` | `ENGAGEMENT.md` — scope, sponsor, rate, contract status, phase |
| `PLAN.md` | a `project-plan.md` deliverable, usually client-facing |
| — | `PROJECT-CLOSEOUT.md` — written at the end, kept afterward |
| `CLAUDE.md` | leads with **STATUS** (active/closed, invoices outstanding, who asked for what) rather than stack conventions |

`STATE.md`, `DECISIONS.md` and `TASKS.md` work unchanged. Add
`deliverables/` and `meetings/` folders. The distinguishing rule is that
*"referencing client code is allowed, changes are not"* — write suggested
changes as prompt-shaped task documents instead, so they can be handed to an
agent working inside the client's own repo.

## `GLOSSARY.md`

Not shipped. The `/grill-me` skill creates it the first time a term needs
pinning down. Terms of art, domain definitions, and any word that means
something specific in this project belong there rather than scattered through
the protocol files.
