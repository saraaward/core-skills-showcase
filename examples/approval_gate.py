"""Synthetic reference example: decide readiness; never deliver an artifact."""

from dataclasses import dataclass
from typing import Mapping, Optional


@dataclass(frozen=True)
class Decision:
    state: str
    reason: str


REQUIRED_CHECKS = frozenset({"required_fields", "output_format", "destination"})


def decide(
    *,
    revision: str,
    checks: Mapping[str, object],
    evaluation: str,
    evaluated_revision: str,
    approved_revision: Optional[str] = None,
) -> Decision:
    """Assumes revision and approval records come from trusted application state."""
    if not isinstance(revision, str) or not revision.strip():
        return Decision("blocked", "Artifact revision is required.")
    if not REQUIRED_CHECKS.issubset(checks):
        return Decision("blocked", "Required check results are missing.")
    if any(checks[name] is not True for name in REQUIRED_CHECKS):
        return Decision("blocked", "Every required check must explicitly pass.")
    if evaluated_revision != revision:
        return Decision("blocked", "Evaluation belongs to a different revision.")
    if evaluation == "fail":
        return Decision("blocked", "Evaluation failed; revise the artifact.")
    if evaluation == "review":
        return Decision("needs_human_review", "Resolve the ambiguous evaluation first.")
    if evaluation != "pass":
        return Decision("blocked", "Evaluation must be pass, review, or fail.")
    if approved_revision != revision:
        return Decision("needs_human_review", "Approve the current revision.")
    return Decision("ready", "Required checks and review cover this revision.")


if __name__ == "__main__":
    checks = {name: True for name in REQUIRED_CHECKS}
    cases = [
        ("Awaiting approval", {}),
        ("Current approval", {"approved_revision": "example-v2"}),
        ("Stale approval", {"approved_revision": "example-v1"}),
    ]
    for label, extra in cases:
        result = decide(
            revision="example-v2", checks=checks, evaluation="pass",
            evaluated_revision="example-v2", **extra,
        )
        print(f"{label}: {result.state} — {result.reason}")
