"""Command-line entry point for the synthetic Abaqus contract demo."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from .checks import audit_contract
from .contract import ContractError, load_contract
from .report import DISCLAIMER, build_report, write_reports


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCENARIO_ROOT = REPOSITORY_ROOT / "examples" / "synthetic-tunnel-review"
DEFAULT_SCENARIO = "complete"
DEFAULT_OUTPUT_ROOT = REPOSITORY_ROOT / "build" / "demo"


class _ArgumentParser(argparse.ArgumentParser):
    """Argument parser whose errors can be converted to ``main``'s status."""

    def error(self, message):
        super().error(message)


def _path_argument(value: str) -> Path:
    if not value.strip():
        raise argparse.ArgumentTypeError("path must not be empty")
    return Path(value).expanduser()


def _parser() -> argparse.ArgumentParser:
    parser = _ArgumentParser(
        description="Run the deterministic synthetic Abaqus contract audit demo."
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--scenario",
        metavar="NAME",
        help=f"repository scenario to audit (default: {DEFAULT_SCENARIO})",
    )
    source.add_argument(
        "--contract",
        metavar="PATH",
        type=_path_argument,
        help="path to a custom JSON contract",
    )
    parser.add_argument(
        "--output-dir",
        metavar="PATH",
        type=_path_argument,
        help="directory for report.json and report.md",
    )
    return parser


def _scenario_contract_path(name: str) -> Path:
    if (
        not name
        or name in {".", ".."}
        or Path(name).name != name
        or "/" in name
        or "\\" in name
    ):
        raise ContractError(f"scenario must be a simple repository name: {name!r}")
    candidate = (SCENARIO_ROOT / name / "model-contract.json").resolve()
    try:
        candidate.relative_to(SCENARIO_ROOT.resolve())
    except ValueError as exc:
        raise ContractError(f"scenario must name a repository scenario: {name!r}") from exc
    if not candidate.is_file():
        raise ContractError(f"unknown scenario {name!r}")
    return candidate


def _safe_scenario_label(contract_path: Path, contract: dict, selected: str | None) -> str:
    if selected is not None:
        return selected
    value = contract.get("scenario_id")
    if isinstance(value, str) and value.strip():
        candidate = value.strip()
        try:
            if Path(candidate).name == candidate and candidate not in {".", ".."}:
                return candidate
        except (OSError, ValueError):
            pass
    return contract_path.stem


def _default_output_dir(label: str) -> Path:
    return DEFAULT_OUTPUT_ROOT / label


def _print_success(report, contract_path: Path, json_path: Path, markdown_path: Path) -> None:
    print(f"Scenario: {report.scenario_id}")
    print(f"Input: {contract_path}")
    print("Summary:")
    for status, count in report.summary().items():
        print(f"{status}: {count}")
    print(f"Report JSON: {json_path}")
    print(f"Report Markdown: {markdown_path}")
    print(DISCLAIMER)


def main(argv: Sequence[str] | None = None) -> int:
    """Run one deterministic contract audit and write its two reports."""

    parser = _parser()
    try:
        arguments = parser.parse_args(argv)
    except SystemExit as exc:
        code = exc.code
        return code if isinstance(code, int) else 2

    selected = arguments.scenario if arguments.scenario is not None else DEFAULT_SCENARIO
    try:
        if arguments.contract is not None:
            contract_path = arguments.contract.resolve()
            selected = None
        else:
            contract_path = _scenario_contract_path(selected)

        contract = load_contract(contract_path)
        findings = audit_contract(contract)
        report = build_report(contract_path, contract, findings)
        output_dir = arguments.output_dir
        if output_dir is None:
            output_dir = _default_output_dir(
                _safe_scenario_label(contract_path, contract, selected)
            )
        json_path, markdown_path = write_reports(report, output_dir)
    except (ContractError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    _print_success(report, contract_path, json_path, markdown_path)
    return 0


__all__ = ["main"]
