# Core Skills Library — Architecture Showcase

**Agent infrastructure · Reusable workflows · Evaluation and handoff**

An architecture for reusable agent instructions and tools that keeps client configuration separate from general operating logic.

**My role:** system owner and principal designer; architecture, authoring standards, ownership boundaries, and versioning approach.

[Architecture](docs/architecture.md) · [Runnable approval-gate example](examples/approval_gate.py) · [Regression tests](tests/test_approval_gate.py) · [Sara Ward](https://saraward.ai)

## The problem

Agent workflows become difficult to maintain when general instructions, platform mechanics, client rules, and one-off fixes accumulate in the same prompt. A change for one deployment can then affect unrelated work, and it becomes unclear which version is running.

The Core Skills Library gives each responsibility a home and defines how deployments consume reusable components.

| Layer | Responsibility |
| --- | --- |
| Skills | Reusable judgment, standards, and decision methods |
| Scripts | Deterministic mechanical operations |
| Workflows | Coordination and review routing |
| Adapters | Platform-specific integration behavior |
| Client configuration | Isolated terminology, policies, credentials, and operating context |
| Evals | Expected decisions, failure cases, and regression protection |

## What exists

The private library's **v0.1.0 foundation** contains the repository architecture, an authoring-standard skill, templates, versioning guidance, and shared discovery paths for Claude Code and Codex. One canonical skills directory supports both tools.

Adapter, workflow, script, and eval directories establish the intended structure. A complete production adapter collection and executable library-wide regression harness are future work.

## A small example you can run

This repository adds a **standalone illustrative reference implementation** of one boundary: an artifact becomes ready for handoff only when required checks pass and a human approves the same revision. It is a public teaching example, not an export of the private library or a claim that its regression harness is complete.

```bash
python3 examples/approval_gate.py
python3 -m unittest discover -s tests -v
```

Python 3.9+; standard library only. The example uses synthetic inputs, makes no network calls, and performs no delivery action.

It demonstrates:

- Exact boolean validation for required checks.
- Explicit handling of failed or ambiguous evaluation.
- Rejection of stale evaluation and stale human approval.
- A visible decision and reason for the caller.
- Regression cases that exercise failure paths.

## Versioning and operational handoff

Skills have independent versions and creation/modification metadata. Deployments should consume a pinned revision and supply their own configuration. A reviewed failure should become an eval case, lead to a change in the responsible component, and be checked before release.

The showcase explains the architecture and provides a neutral example. The canonical library, proprietary operating methods, and client deployments remain private.
