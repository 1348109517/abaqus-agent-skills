from dataclasses import dataclass


VALID_STATUSES = ("PASS", "WARNING", "REVIEW_REQUIRED")


@dataclass(frozen=True)
class Finding:
    code: str
    status: str
    message: str
    location: str
    skill: str
    next_action: str


@dataclass(frozen=True)
class AuditReport:
    schema_version: str
    runner_version: str
    scenario_id: str
    input_digest: str
    findings: tuple[Finding, ...]

    def summary(self) -> dict[str, int]:
        return {
            status: sum(item.status == status for item in self.findings)
            for status in VALID_STATUSES
        }
