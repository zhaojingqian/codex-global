---
name: codex-work-review
description: "Run and archive periodic Codex work-system audits: immutable snapshots, metrics, append-only intervention ledger. Use for monthly/weekly reviews, measuring past optimizations, detecting recurring failures."
---

# Codex Work Review

## Cadence

- Global review: monthly.
- Project review: weekly when a project defines that cadence.
- Run ad hoc reviews only for incidents or major architecture changes.

## Required inputs

- complete accessible-snapshot coverage audit;
- report and machine-readable metrics;
- conversation or task inventory;
- evidence index;
- source path, hash, size, and time range;
- active interventions due for review.
- active Agent profiles and routing configuration.

Do not describe a partial scan as complete. Preserve unavailable or truncated evidence explicitly.

## Procedure

1. Complete the scan and evidence review.
2. Load the previous period and active interventions.
3. Evaluate each due intervention as `improved`, `unchanged`, `regressed`, or `insufficient-evidence`.
4. Review each Agent profile by task type using success, failure, escalation, fallback, token, and latency metrics.
5. Review permission efficiency using approval-review rate, allow rate, review token share, and fail-then-escalate retries by operation type.
6. Change a profile only when the quality floor is met and the sample is sufficient. Change at most one of model or reasoning effort per profile.
7. Change permissions only from audited operation classes; preserve destructive, unresolved-target, credential, and out-of-scope gates.
8. Separate current-period metrics from historical comparisons.
9. Archive an immutable revision:

   ```bash
   python scripts/review_archive.py archive \
     --root <review-root> --scope <scope> --cadence <monthly|weekly> \
     --period <period> --revision 1 --report <report.md> \
     --metrics <metrics.json> --artifact <inventory.csv> \
     --artifact <evidence.csv> --source <source-path>
   ```

10. Append new or reviewed interventions with `record-intervention` or `record-interventions`.
11. Generate the scope trend table with `trend`.
12. End with the next review period and measurable open questions.

## Archive contract

- Store one immutable directory per period and revision.
- Keep large raw exports outside the archive. Record path, hash, and size instead.
- Store reports, compact inventories, evidence indexes, metrics, and manifests.
- Create a new revision for corrections; never edit an archived revision.
- Treat generated trend files as derived indexes, not evidence.

## Intervention contract

Every intervention requires:

- stable ID and scope;
- introduction period;
- objective change statement;
- expected effect;
- metric or evidence used for review;
- due period;
- status.

Append review events. Do not rewrite earlier events.

## Resources

- Use `scripts/review_archive.py` for immutable archive creation, intervention events, comparison, and trends.
- Read `references/review-metrics.schema.json` before producing metrics.
- Read `references/intervention-event.schema.json` before recording an intervention.
