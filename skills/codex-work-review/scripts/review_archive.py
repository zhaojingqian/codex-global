#!/usr/bin/env python3
"""Archive periodic reviews, append intervention events, and build trends."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path
from typing import Any


def safe_segment(value: str, field: str) -> str:
    if (
        not value
        or value in {".", ".."}
        or "/" in value
        or "\\" in value
        or "\x00" in value
    ):
        fail(f"{field} must be one path segment")
    return value


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read JSON {path}: {exc}")


def atomic_text(path: Path, value: str, *, replace: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not replace:
        fail(f"refusing to overwrite: {path}")
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(value)
        os.replace(tmp_name, path)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)


def write_json(path: Path, value: Any, *, replace: bool = False) -> None:
    atomic_text(
        path,
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        replace=replace,
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_metrics(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        fail("metrics.schema_version must be 1")
    for field in ("scope", "period"):
        if not isinstance(value.get(field), str) or not value[field]:
            fail(f"metrics.{field} must be a non-empty string")
    if value.get("cadence") not in {"monthly", "weekly"}:
        fail("metrics.cadence must be monthly or weekly")
    metrics = value.get("metrics")
    if not isinstance(metrics, dict):
        fail("metrics.metrics must be an object")
    for name, item in metrics.items():
        if not isinstance(name, str) or not isinstance(item, dict):
            fail("each metric must be an object")
        if not isinstance(item.get("value"), (int, float)):
            fail(f"metric {name}.value must be numeric")
        if item.get("direction") not in {"higher", "lower", "neutral"}:
            fail(f"metric {name}.direction is invalid")
        if not isinstance(item.get("unit"), str) or not item["unit"]:
            fail(f"metric {name}.unit must be a non-empty string")
    return value


def validate_intervention(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        fail("intervention.schema_version must be 1")
    required = ("id", "event_type", "scope", "period", "status")
    for field in required:
        if not isinstance(value.get(field), str) or not value[field]:
            fail(f"intervention.{field} must be a non-empty string")
    if value["event_type"] not in {"introduced", "reviewed", "closed"}:
        fail("intervention.event_type is invalid")
    allowed_status = {
        "planned",
        "active",
        "improved",
        "unchanged",
        "regressed",
        "insufficient-evidence",
        "closed",
    }
    if value["status"] not in allowed_status:
        fail("intervention.status is invalid")
    if value["event_type"] == "introduced":
        for field in ("change", "expected_effect", "due_period"):
            if not isinstance(value.get(field), str) or not value[field]:
                fail(f"introduced intervention requires {field}")
    return value


def copy_evidence(source: Path, target: Path) -> dict[str, Any]:
    if not source.is_file():
        fail(f"artifact is not a file: {source}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        fail(f"artifact name collision: {target.name}")
    shutil.copy2(source, target)
    return {
        "path": str(target),
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
    }


def command_archive(args: argparse.Namespace) -> None:
    safe_segment(args.scope, "scope")
    safe_segment(args.period, "period")
    if args.revision < 1:
        fail("revision must be positive")
    metrics = validate_metrics(load_json(args.metrics))
    if metrics["scope"] != args.scope:
        fail("metrics.scope does not match --scope")
    if metrics["cadence"] != args.cadence:
        fail("metrics.cadence does not match --cadence")
    if metrics["period"] != args.period:
        fail("metrics.period does not match --period")
    target = (
        args.root.resolve()
        / args.scope
        / args.cadence
        / args.period
        / f"r{args.revision:03d}"
    )
    if target.exists():
        fail(f"archive revision already exists: {target}")
    target.mkdir(parents=True)
    files = [
        copy_evidence(args.report.resolve(), target / "report.md"),
        copy_evidence(args.metrics.resolve(), target / "metrics.json"),
    ]
    artifact_dir = target / "artifacts"
    seen: set[str] = set()
    for artifact in args.artifact:
        source = artifact.resolve()
        if source.name in seen:
            fail(f"duplicate artifact basename: {source.name}")
        seen.add(source.name)
        files.append(copy_evidence(source, artifact_dir / source.name))

    source = args.source.resolve()
    source_record: dict[str, Any] = {
        "path": str(source),
        "exists": source.exists(),
        "kind": "directory" if source.is_dir() else "file",
    }
    if args.source_sha256:
        source_record["sha256"] = args.source_sha256
    elif source.is_file():
        source_record["sha256"] = sha256(source)
    if args.source_size is not None:
        source_record["bytes"] = args.source_size
    elif source.is_file():
        source_record["bytes"] = source.stat().st_size

    manifest = {
        "schema_version": 1,
        "scope": args.scope,
        "cadence": args.cadence,
        "period": args.period,
        "revision": args.revision,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "source": source_record,
        "files": files,
    }
    write_json(target / "manifest.json", manifest)
    print(target)


def load_intervention_ledger(ledger: Path) -> list[dict[str, Any]]:
    existing: list[dict[str, Any]] = []
    if not ledger.exists():
        return existing
    for line_number, line in enumerate(
        ledger.read_text(encoding="utf-8").splitlines(), 1
    ):
        try:
            existing.append(json.loads(line))
        except json.JSONDecodeError as exc:
            fail(f"invalid intervention ledger line {line_number}: {exc}")
    return existing


def append_interventions(root: Path, events: list[dict[str, Any]]) -> None:
    ledger = root.resolve() / "interventions.jsonl"
    existing = load_intervention_ledger(ledger)
    introduced = {
        item.get("id")
        for item in existing
        if item.get("event_type") == "introduced"
    }
    pending: list[dict[str, Any]] = []
    for event in events:
        if event in existing or event in pending:
            fail(f"identical intervention event already exists: {event['id']}")
        if event["event_type"] == "introduced" and event["id"] in introduced:
            fail(f"intervention already introduced: {event['id']}")
        if event["event_type"] == "introduced":
            introduced.add(event["id"])
        pending.append(event)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle:
        for event in pending:
            handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def command_record_intervention(args: argparse.Namespace) -> None:
    event = validate_intervention(load_json(args.event))
    append_interventions(args.root, [event])
    print(event["id"])


def command_record_interventions(args: argparse.Namespace) -> None:
    events: list[dict[str, Any]] = []
    try:
        lines = args.events_jsonl.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        fail(f"cannot read intervention JSONL {args.events_jsonl}: {exc}")
    for line_number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError as exc:
            fail(f"invalid intervention JSONL line {line_number}: {exc}")
        events.append(validate_intervention(event))
    if not events:
        fail("intervention JSONL is empty")
    append_interventions(args.root, events)
    print("\n".join(event["id"] for event in events))


def latest_revisions(
    root: Path, scope: str, cadence: str
) -> list[tuple[str, Path, dict[str, Any]]]:
    base = root / scope / cadence
    if not base.exists():
        return []
    snapshots: list[tuple[str, Path, dict[str, Any]]] = []
    for period_dir in sorted(path for path in base.iterdir() if path.is_dir()):
        revisions = sorted(
            path for path in period_dir.iterdir() if path.is_dir() and path.name.startswith("r")
        )
        if not revisions:
            continue
        metrics_path = revisions[-1] / "metrics.json"
        snapshots.append(
            (period_dir.name, revisions[-1], validate_metrics(load_json(metrics_path)))
        )
    return snapshots


def command_compare(args: argparse.Namespace) -> None:
    safe_segment(args.scope, "scope")
    safe_segment(args.current, "current")
    safe_segment(args.previous, "previous")
    snapshots = {
        period: (path, metrics)
        for period, path, metrics in latest_revisions(
            args.root.resolve(), args.scope, args.cadence
        )
    }
    if args.current not in snapshots or args.previous not in snapshots:
        fail("current or previous period is missing")
    current_path, current = snapshots[args.current]
    _, previous = snapshots[args.previous]
    comparison: dict[str, Any] = {
        "schema_version": 1,
        "scope": args.scope,
        "cadence": args.cadence,
        "current": args.current,
        "previous": args.previous,
        "metrics": {},
    }
    for name in sorted(set(current["metrics"]) & set(previous["metrics"])):
        now = current["metrics"][name]
        before = previous["metrics"][name]
        if now["unit"] != before["unit"]:
            continue
        delta = now["value"] - before["value"]
        direction = now["direction"]
        if delta == 0 or direction == "neutral":
            outcome = "unchanged"
        elif (delta > 0 and direction == "higher") or (
            delta < 0 and direction == "lower"
        ):
            outcome = "improved"
        else:
            outcome = "regressed"
        comparison["metrics"][name] = {
            "previous": before["value"],
            "current": now["value"],
            "delta": delta,
            "unit": now["unit"],
            "outcome": outcome,
        }
    output = current_path / f"comparison-to-{args.previous}.json"
    write_json(output, comparison)
    print(output)


def command_trend(args: argparse.Namespace) -> None:
    safe_segment(args.scope, "scope")
    snapshots = latest_revisions(args.root.resolve(), args.scope, args.cadence)
    metric_names = sorted(
        {name for _, _, metrics in snapshots for name in metrics["metrics"]}
    )
    output = (
        args.root.resolve()
        / args.scope
        / args.cadence
        / "trend.csv"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=".trend.", dir=output.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["period", "revision", *metric_names])
            for period, path, metrics in snapshots:
                writer.writerow(
                    [
                        period,
                        path.name,
                        *[
                            metrics["metrics"].get(name, {}).get("value", "")
                            for name in metric_names
                        ],
                    ]
                )
        os.replace(tmp_name, output)
    finally:
        if os.path.exists(tmp_name):
            os.unlink(tmp_name)
    print(output)


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)

    archive = sub.add_parser("archive")
    archive.add_argument("--root", type=Path, required=True)
    archive.add_argument("--scope", required=True)
    archive.add_argument("--cadence", choices=("monthly", "weekly"), required=True)
    archive.add_argument("--period", required=True)
    archive.add_argument("--revision", type=int, default=1)
    archive.add_argument("--report", type=Path, required=True)
    archive.add_argument("--metrics", type=Path, required=True)
    archive.add_argument("--artifact", type=Path, action="append", default=[])
    archive.add_argument("--source", type=Path, required=True)
    archive.add_argument("--source-sha256")
    archive.add_argument("--source-size", type=int)
    archive.set_defaults(func=command_archive)

    record = sub.add_parser("record-intervention")
    record.add_argument("--root", type=Path, required=True)
    record.add_argument("--event", type=Path, required=True)
    record.set_defaults(func=command_record_intervention)

    record_many = sub.add_parser("record-interventions")
    record_many.add_argument("--root", type=Path, required=True)
    record_many.add_argument("--events-jsonl", type=Path, required=True)
    record_many.set_defaults(func=command_record_interventions)

    compare = sub.add_parser("compare")
    compare.add_argument("--root", type=Path, required=True)
    compare.add_argument("--scope", required=True)
    compare.add_argument("--cadence", choices=("monthly", "weekly"), required=True)
    compare.add_argument("--current", required=True)
    compare.add_argument("--previous", required=True)
    compare.set_defaults(func=command_compare)

    trend = sub.add_parser("trend")
    trend.add_argument("--root", type=Path, required=True)
    trend.add_argument("--scope", required=True)
    trend.add_argument("--cadence", choices=("monthly", "weekly"), required=True)
    trend.set_defaults(func=command_trend)
    return root


def main() -> None:
    args = parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
