# SubTask · {Title}

## Brief
[1-2 sentences. Context + outcome. State the goal, not the steps.]

## Definition of Done
[One verifiable sentence. The whole plan funnels here. Phrased so a small evaluator can judge it from the transcript. No vibe words.]

**NOTE:** DoD becomes the /goal condition; Verification commands run each turn

## Stack
- Tool, framework, API, or model that will be used
- One bullet each, name version when load-bearing
- Flag paid APIs that need cost approval

## Scope
**Visuals**
- [Bullets describing what it looks like - only when the task is visual]

**Functionality**
- [Bullets describing what it does]

For non-visual tasks (refactor, content batch, ops), drop the Visuals sub-header and flatten to bullets under Scope.

## Out of Scope
- Explicit non-goals
- At least 2 bullets - empty negative space is where /goal burns tokens

## Constraints
- What must hold throughout the work
- e.g. single file, no build step, no new deps, brand rules, perf budget
- Unless explicitly required, no changes to the project's stack should be made

## Acceptance Criteria & Verification
- Bulleted sub-checks flowing from DoD
- Format: "acceptance criteria" → "verification test"
- Each independently verifiable as true / false
- Exact commands or visual checks /goal will run each turn to produce evidence
- Aim for 5-10 bullets

## Turn Budget
Stop after {N} turns, or sooner once the DoD condition holds.

## References
- Links, files, screenshots, prior art (optional - skip if empty)

## Risks / Open Questions
- Known failure modes, judgment calls flagged for the user (optional - skip if empty)
