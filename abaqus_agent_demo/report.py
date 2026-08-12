import dataclasses
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from . import __version__
from .contract import input_digest
from .findings import AuditReport, Finding


DISCLAIMER = (
    "Static contract review only. No Abaqus solver execution or physical "
    "engineering validation was performed."
)


def build_report(
    contract_path: Path,
    contract: Mapping[str, Any],
    findings: Sequence[Finding],
) -> AuditReport:
    return AuditReport(
        schema_version="1.0",
        runner_version=__version__,
        scenario_id=str(contract.get("scenario_id", contract_path.stem)),
        input_digest=input_digest(contract_path),
        findings=tuple(findings),
    )


def report_payload(report: AuditReport) -> dict[str, Any]:
    return {
        "schema_version": report.schema_version,
        "runner_version": report.runner_version,
        "scenario_id": report.scenario_id,
        "input_digest": report.input_digest,
        "summary": report.summary(),
        "findings": [dataclasses.asdict(item) for item in report.findings],
        "boundary": DISCLAIMER,
    }


def render_json(report: AuditReport) -> str:
    return json.dumps(report_payload(report), indent=2, sort_keys=True) + "\n"


def render_markdown(report: AuditReport) -> str:
    lines = [
        f"# Audit report: {report.scenario_id}",
        "",
        f"Input SHA-256: `{report.input_digest}`",
        "",
        "| Status | Count |",
        "|---|---:|",
    ]
    lines.extend(
        f"| {status} | {count} |"
        for status, count in report.summary().items()
    )
    lines.extend(["", "## Findings", ""])
    for item in report.findings:
        lines.extend(
            [
                f"### {item.code}: {item.status}",
                "",
                item.message,
                "",
                f"- Location: `{item.location}`",
                f"- Related skill: `{item.skill}`",
                f"- Next action: {item.next_action}",
                "",
            ]
        )
    lines.extend(["## Boundary", "", DISCLAIMER, ""])
    return "\n".join(lines)


def write_reports(report: AuditReport, output_dir: Path) -> tuple[Path, Path]:
    json_path = output_dir / "report.json"
    markdown_path = output_dir / "report.md"
    planned = ((json_path, render_json(report)), (markdown_path, render_markdown(report)))
    for path, content in planned:
        if path.exists() and path.read_text(encoding="utf-8") != content:
            raise FileExistsError(f"refusing to replace non-identical report: {path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    for path, content in planned:
        if not path.exists():
            path.write_text(content, encoding="utf-8")
    return json_path, markdown_path
