---
name: schema-aware-data-viewer
description: Generate a local self-contained HTML viewer via DPH dataset_html_viewer. Use for bounded review of indexed CSV/JSON/JSONL under data/, model-output comparison, or annotation support.
---

# Schema-Aware Data Viewer

Use `execution_types/dataset_html_viewer` from the current Data Process Hub repository. Do not
maintain or generate a parallel viewer implementation in this Skill.

## Contract

- Read `<DPH_ROOT>/execution_types/dataset_html_viewer/README.md` and
  `config.schema.yaml` before use.
- Treat the viewer as a local review/demo tool, never a task step, pipeline artifact, or
  acceptance evidence.
- Use `dph` from `PATH`; do not invoke a bundled renderer, system Python, or a copied template.

Require:

- the resolved DPH repository root;
- one CSV, JSON, or JSONL input under `<DPH_ROOT>/data/`;
- a stable, non-empty, unique `index` or an explicitly named equivalent;
- a bookkeeping task ID and demo ID that do not correspond to a real task step;
- optional YAML configuration conforming to the execution type's current schema.

If the source is outside `data/`, materialize an explicit safe copy through the appropriate DPH
workflow before generating the viewer. Do not make the viewer query ODPS or OSS.

## Procedure

1. Inspect the source format, row count, fields, index integrity, and sensitive-field risk.
2. Fail on missing, empty, mixed-type, or duplicate index values. Do not synthesize an index.
3. Create a concise YAML config under `data/<task_id>/.../cache/` only when defaults are
   insufficient. Use only fields supported by the current DPH schema.
4. From `<DPH_ROOT>`, generate the viewer:

   ```bash
   dph python -m execution_types.dataset_html_viewer.cli \
     --repo-root <DPH_ROOT> \
     --task-id <bookkeeping_task_id> \
     --demo-id demo_html_viewer \
     --input <DPH_ROOT>/data/<input> \
     [--index-column <field>] \
     [--config <DPH_ROOT>/data/<config.yaml>]
   ```

5. Read `viewer_output` from stdout and the same-run DPH manifest. Require `status=success`,
   matching input/output paths, index statistics, record counts, field count, and explicit
   truncation state.
6. Open the HTML locally and verify parsing, search, filtering, sorting, field visibility,
   empty-value handling, and configured images.
7. Deliver the HTML path and manifest path with the verified counts and limitations.

## Safety

- The DPH execution type embeds records in the HTML. Do not pass credentials, tokens, cookies,
  signed URLs, private endpoints, or unnecessary sensitive fields.
- The execution type does not redact source fields. Create and verify a sanitized derived input
  when sensitive fields must be removed.
- Remote image URLs can trigger network requests when the page is opened. Resolve their scope
  before opening the viewer.
- Do not enable truncation implicitly. If `allow_truncate: true` is explicitly required, report
  source and embedded record counts.
- Do not use this Skill for production dashboards, live-query applications, editing or annotation
  write-back, or data-quality acceptance.
