---
name: refactor
description: "Explicit opt-in workflow for panorama-first refactor review and implementation toward the smallest functionally complete framework. Use only when the user explicitly invokes `$refactor` or explicitly asks to use the refactor skill. Do not auto-trigger for ordinary requests to review, refactor, optimize, simplify, restructure, clean up, move files, reduce duplication, or improve architecture or documentation."
---

# Refactor

This skill is opt-in. Do not infer activation from the task; proceed only after
an explicit `$refactor` invocation or an explicit request to use this skill.

Refactor toward the minimal framework that remains functionally complete. Optimize framework clarity and efficiency, model token economy, and file-structure clarity together. Apply the owner's design philosophy and the nearest `AGENTS.md`.

## Select the mode

- For a review, remain read-only and deliver findings plus a quantified plan.
- For implementation, complete the same review first. Present the plan and wait for approval before structural edits.
- Treat diagnosis, review, planning, implementation, Git operations, and production mutation as separate authorities.

## Build the panorama

Before proposing changes:

1. Read the current source of truth and inspect Git state. Preserve unrelated dirty files.
2. Map the capability end to end. For every lifecycle stage, record:
   - current owning layer: core, shared, platform-specific, or caller;
   - inputs, outputs, identities, persisted evidence, and side effects;
   - call sites and downstream consumers.
3. Inventory with hard numbers:
   - files and lines;
   - live references;
   - duplicate implementations and import dialects;
   - dead files with zero live references;
   - hand-written copies of machine-derivable knowledge;
   - always-loaded documentation lines or tokens when relevant.
4. Classify each finding by its essential dimension: place knowledge where it belongs, not where it was first encountered.
5. Separate code compatibility from persisted-data compatibility:
   - remove code shims that only preserve old wiring or tests;
   - preserve ledgers, receipts, checkpoints, archives, provenance, and historical artifacts forever.

Do not design from one failing example. Verify the entire lifecycle and all claim, replay, retry, recovery, projection, and public-entry paths that share the invariant.

## Evaluate the architecture

Apply these rules in order:

1. **Delete first.** Remove dead files, unused parameters, unconsumed hashes, unproven caches, and duplicate behavior. Require a zero-live-reference search before deletion.
2. **Keep one implementation per behavior.** Extract one pure function at the layer matching the essential dimension. Parameterize only real differences.
3. **Prefer mechanisms over enumerations.** Turn recurring manual knowledge into a machine-enforced invariant with a self-explaining remedy.
4. **Keep pure boundaries pure.** Reducers, decisions, ranking, normalization, and projection derivations must not perform I/O.
5. **Keep side effects at explicit edges.** Providers adapt platform evidence; orchestration owns lifecycle; projections never reinterpret private provider payloads.
6. **Do not create parallel state machines.** Extend the existing Fact, lifecycle, or contract when it naturally owns the behavior.
7. **Preserve unit isolation.** One unit's failure must not block unrelated units.
8. **Fail closed on identity, authority, writer, or provenance ambiguity.** Preserve unresolved facts as `unknown`.

Reject task IDs, Stage IDs, queue names, table names, or incident-specific branches in framework logic unless they are typed data in a general contract.

## Review documentation economics

- Keep always-loaded entry files to hard gates and one intent-to-target routing table.
- Keep one authoritative home per concept; replace duplicate narratives with links.
- Reference generated help, status, schemas, or command output for facts the system can describe itself.
- Retain prose only for semantics generation cannot carry: when, why, pitfalls, and authority.
- Prefer compact tables and imperative bullets.
- Report before/after always-loaded line and token totals when documentation changes.

## Review file structure

- Group by domain, not file type or implementation technique.
- Keep directory roots for public path contracts and entrypoints only.
- Treat paths invoked by another repository as APIs.
- For proposed moves:
  1. use `git mv`;
  2. enumerate imports, module invocations, shell commands, docs, and fixtures;
  3. audit every relative-root derivation such as `parents[n]`;
  4. require zero residual old-path references;
  5. smoke-test real entrypoints, not only unit tests.
- Compare moved or rewritten bodies against the current source, never memory.

## Prove findings

For each material finding:

- cite the exact file and narrow line;
- show the call path or persisted-data path;
- explain the violated invariant and concrete impact;
- distinguish confirmed fact, inference, and unknown;
- give the smallest general correction;
- state the regression test that would fail before and pass after.

Severity:

- **P0:** data loss, corruption, security, or irreversible production risk.
- **P1:** wrong lifecycle, identity, writer, replay, or cross-unit behavior.
- **P2:** bounded correctness, compatibility, maintainability, or validation gap.
- **P3:** local clarity or efficiency issue without current correctness impact.

If no material findings remain, say so explicitly and list residual risks or untested boundaries.

## Plan changes

Before editing, present a table with:

- delete, merge, move, or parameterize action;
- exact files and call sites;
- essential owning layer;
- lines changed or deleted;
- cross-repository or persisted-data impact;
- expected line, token, or operator-step savings;
- validation and rollback boundary.

Wait for approval before structural edits. Always stop before cross-repository writes, running-production changes, or any change that could invalidate persisted runtime data.

## Validate implementation

- Run the smallest relevant checks first, then expand by risk.
- Run the full affected suite with its real exit code as the commit gate. Do not hide the test exit code behind a pipe.
- Treat flaky tests as findings. Pin the documented contract instead of retrying until green.
- Test replay of historical data, current behavior, public entrypoints, and failure isolation when applicable.
- Smoke-test real entrypoints after moves or routing changes.
- Keep one independently revertible logical change per commit.
- Never stage, commit, push, amend, rebase, or rewrite history without the corresponding authority.

## Report

For a review, lead with findings ordered by severity. Then provide:

1. lifecycle panorama;
2. quantified duplication and ownership inventory;
3. smallest coherent refactor plan;
4. expected savings;
5. validation matrix;
6. unknowns and explicitly deferred work.

For completed implementation, report a table per commit:

- what died, merged, moved, or became parameterized;
- before/after line counts;
- exact tests and pass counts;
- real entrypoints smoke-tested;
- remaining risks and deferred items;
- current Git state.

Include before/after always-loaded token cost whenever documentation was touched.
