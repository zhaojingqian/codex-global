# Global Agent Rules

## Design philosophy

- **Mechanisms over cases**: prefer general mechanisms that scale with data
  and compute. Common behavior is the default; real differences are typed data
  at narrow interfaces. Judge changes by steps and tokens saved, lines
  deletable, and errors made mechanically impossible.
- **One owner, stable boundaries**: every invariant has one authoritative
  owner. Keep different authorities, lifecycles, and failure domains separate;
  state and locks live with the resource they protect. Do not create cycles or
  shared mutable state merely to save lines.
- **Panorama, then subtraction**: map the end-to-end lifecycle before a
  structural change and present the plan and cost first. Delete, merge, or
  default before adding. Do not add hashes, timestamps, caches, incremental
  stores, compatibility branches, or parallel implementations without a proved
  invariant. Mutable source names stay stable and unversioned; genuine
  protocol, schema, asset, and historical identities remain versioned. Major
  changes use independently revertable commits.
- **Evidence and compatibility**: use authoritative evidence and preserve
  unresolved facts as `unknown`. Persisted history, identity, and provenance
  remain backward compatible; disposable projections may be rebuilt. Remove
  code-only compatibility after proving it has no live consumer.
- **Layered automation and documentation**: machines own deterministic work;
  the model handles judgment using the cheapest sufficient signal. One unit's
  failure must not stop unrelated units. Always-loaded documents contain only
  hard constraints and routing; generated usage, parameters, and state are
  referenced rather than copied by hand.

## Hash gate

Use the cheapest authoritative evidence. Do not compute a content hash unless
byte identity is an explicit acceptance criterion. Git status/diff answers
which tracked files changed; real entrypoints and tests answer behavior; an
existing compiler, artifact, Revision, manifest, or provider identity answers
equality when it already owns that invariant. Files outside the current diff
do not need hashes merely to show they were untouched.

A new hash computation is allowed only when all are true:

1. The contract requires byte identity, transport integrity, or
   content-addressed deduplication.
2. No existing identity or cheaper evidence answers the question.
3. Equal and unequal results have different, predetermined actions.
4. The value is computed once and reused; persist it only when its owning
   contract defines the lifecycle.

Before hashing, state:

`Hash gate: invariant=<...>; existing authority=none; equal=> <action>;
different=> <action>.`

If any field cannot be filled objectively, do not hash. A published checksum
is valid evidence for an untrusted downloaded artifact.

## Scope and authority

- System, platform, security, sandbox, and permission constraints precede the
  current task and nearest `AGENTS.md`; lower levels may tighten but never
  expand external-write, destructive, or history-rewriting authority.
- Modify only the exact owned workspace, Codex-owned files under `~/.codex`
  required by the current request, and a uniquely scoped temporary directory.
  A nested task owns only that subtree; delegation inherits the same or a
  narrower boundary. All other visible paths are read-only unless the user
  explicitly expands scope. Temporary paths never hold permanent source,
  history, credentials, or evidence.
- Read-only diagnosis never authorizes edits; diagnosis never authorizes
  repair; monitoring never authorizes retry. Filesystem access is not write
  authority. Standing external permissions live in `~/.codex/authorities/`
  and apply only to their declared scope.
- Unresolved targets, scope expansion, credential/security changes, and
  destructive or hard-to-recover actions require approval. Resolve high-risk
  targets, current state, impact, recovery, and authority before acting. Never
  use broad globs, unresolved variables, or an implicit `latest`. Outer status
  alone never proves success or failure.

## Files and Git

- Follow existing architecture and naming. Read current content and diff before
  editing shared rules, schemas, locks, or entrypoints. Preserve unrelated
  modified, staged, deleted, and untracked work; never restore, move, delete,
  format, or stage it.
- Use native Git. After an authorized change is complete and validation passes,
  show the exact file list and full commit message, stage only the owned change,
  and create one complete logical commit. Push it when the repository has an
  unambiguous configured remote/upstream; with no remote, stop after commit.
  Report validation, commit, push, boundary, and remaining dirty state.
- Do not commit or push read-only, failed, incomplete, unrelated, or ambiguous
  work. A current-task prohibition takes precedence. Reset, rebase, amend,
  force-push, history rewriting, and branch deletion require separate
  authorization and a recovery plan. Serialize writes to one Git index.

## Validation

- Start with the cheapest relevant check and expand with risk: code uses
  compile/type/unit/integration/real entrypoint; config and docs use parsing and
  actual routing; data uses schema, count, stable-key uniqueness, failure
  budget, and representative review.
- Platform terminal state is not business acceptance. Analyze a failed command
  and its side effects before retrying; report completion only with required
  acceptance evidence.

## SQL cardinality

- Never create a Cartesian product in production, validation, or diagnostic
  SQL: no `CROSS JOIN`, comma join, `ON TRUE`, `ON 1=1`, or join without an
  explicit key predicate.
- Before changing a join, state its row atom and expected cardinality.
  Many-to-many requires explicit task authorization and bounded fanout
  evidence; otherwise deduplicate or pre-aggregate one side to the key.
- Use conditional aggregation for same-source metrics and vertical `UNION ALL`
  for independent checks; express one global value through a proven scalar
  subquery or window. Combine independent aggregates only after reducing each
  to one row and joining through an explicit documented one-to-one key.

## Delegation and automation

- Delegate only when context isolation, independent parallelism, or cheaper
  execution repays coordination cost. The main agent owns requirements,
  architecture, authority, Git, and final acceptance.
- Give agents fresh bounded scopes; subagents do not delegate further. One
  writable file has one owner, and overlapping or uncertain writes run
  serially. A failed writer gets at most one focused same-scope repair before
  re-planning.
- Every automation declares scope, allowed and prohibited actions, source of
  truth, termination, and fallback. Expanding observation into mutation is a
  new contract; report only meaningful milestones.

## Knowledge placement

`AGENTS.md`: stable rules and stop conditions. Authority: standing external
permission. Skill: reusable judgment. Script/hook: deterministic gate. Memory:
durable context, never live state. Run ledger: attempts and evidence.
Conversation: current goals and one-time authorization. One rule has one home;
link instead of duplicating.
